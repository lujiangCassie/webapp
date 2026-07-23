"""
build_llm_wiki.py

Build a browsable Markdown "wiki" from a fab failure/action log, in the spirit
of Karpathy's approach: cluster raw records into recurring failure modes,
then use an LLM to write the actual wiki prose for each cluster/tool/failure
type, and stitch everything together with cross-links + an index.

Input dataframe (or CSV) must have columns:
    date_time, failure_description, tool_id, failure_type, actions

Pipeline:
    1. Load + clean the data.
    2. Cluster failure_description text within each (tool_id) group using
       TF-IDF + KMeans, to collapse thousands of near-duplicate free-text
       entries into a handful of recurring "failure modes" per tool.
    3. For each cluster, ask the LLM to write a short wiki entry: what the
       failure mode is, how often/when it happens, what actions were taken,
       and which actions seem to actually resolve it.
    4. Ask the LLM to write a one-paragraph overview for each tool page and
       each failure-type page, linking down to the failure-mode entries.
    5. Ask the LLM to write a top-level index/landing page.
    6. Write everything out as linked .md files under OUTPUT_DIR.

Requirements:
    pip install pandas scikit-learn anthropic

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python build_llm_wiki.py --csv failures.csv --out ./wiki
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import textwrap
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from viewer_template import render_viewer_html

try:
    import anthropic
except ImportError:  # allow --dry-run without the SDK installed
    anthropic = None


# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_CLUSTERS_PER_TOOL = 8       # cap on distinct failure modes per tool
MIN_RECORDS_PER_CLUSTER = 3     # merge/drop clusters smaller than this
CACHE_PATH = None               # set in main() once --out is known


# --------------------------------------------------------------------------
# 1. Load + clean
# --------------------------------------------------------------------------

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["date_time"])
    required = {"date_time", "failure_description", "tool_id", "failure_type", "actions"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {missing}")

    for col in ["failure_description", "tool_id", "failure_type", "actions"]:
        df[col] = df[col].astype(str).str.strip()

    df = df.dropna(subset=["failure_description"])
    df = df[df["failure_description"].str.len() > 0]
    df = df.sort_values("date_time").reset_index(drop=True)
    return df


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "unknown"


# --------------------------------------------------------------------------
# 2. Cluster failure descriptions within each tool
# --------------------------------------------------------------------------

def cluster_group(descriptions: list[str], max_clusters: int = MAX_CLUSTERS_PER_TOOL) -> list[int]:
    """Return a cluster label per description. Falls back to a single
    cluster if there isn't enough text diversity to bother clustering."""
    n = len(descriptions)
    if n < MIN_RECORDS_PER_CLUSTER * 2:
        return [0] * n

    k = max(2, min(max_clusters, n // MIN_RECORDS_PER_CLUSTER))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_df=0.9,
        min_df=1,
        ngram_range=(1, 2),
    )
    try:
        X = vectorizer.fit_transform(descriptions)
    except ValueError:
        # e.g. only stopwords left after filtering
        return [0] * n

    if X.shape[1] == 0:
        return [0] * n

    k = min(k, X.shape[0])
    km = KMeans(n_clusters=k, n_init=10, random_state=0)
    labels = km.fit_predict(X)

    # merge tiny clusters into their nearest neighbor by simple relabeling
    counts = Counter(labels)
    small = {c for c, ct in counts.items() if ct < MIN_RECORDS_PER_CLUSTER}
    if small and len(counts) > 1:
        # send small clusters into whichever surviving cluster is largest
        big_label = counts.most_common(1)[0][0]
        labels = [big_label if lbl in small and lbl != big_label else lbl for lbl in labels]

    return list(labels)


def build_clusters(df: pd.DataFrame) -> pd.DataFrame:
    """Adds a `cluster_id` column, unique per (tool_id, local cluster)."""
    df = df.copy()
    df["cluster_id"] = ""
    for tool_id, idx in df.groupby("tool_id").groups.items():
        sub_idx = list(idx)
        descs = df.loc[sub_idx, "failure_description"].tolist()
        labels = cluster_group(descs)
        for i, lbl in zip(sub_idx, labels):
            df.at[i, "cluster_id"] = f"{slugify(tool_id)}__c{lbl}"
    return df


def cluster_representative_terms(descriptions: list[str], top_n: int = 5) -> list[str]:
    """Cheap keyword summary of a cluster, used as a fallback title and to
    ground the LLM prompt without dumping hundreds of raw rows into it."""
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.95, ngram_range=(1, 2))
    try:
        X = vectorizer.fit_transform(descriptions)
    except ValueError:
        return []
    scores = X.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda t: -t[1])
    return [t for t, _ in ranked[:top_n]]


# --------------------------------------------------------------------------
# 3-5. LLM calls (with on-disk caching so re-runs are cheap)
# --------------------------------------------------------------------------

class LLMWriter:
    def __init__(self, cache_path: Path, dry_run: bool = False):
        self.dry_run = dry_run
        self.cache_path = cache_path
        self.cache: dict[str, str] = {}
        if cache_path.exists():
            self.cache = json.loads(cache_path.read_text())
        self.client = None if (dry_run or anthropic is None) else anthropic.Anthropic()

    def _save_cache(self):
        self.cache_path.write_text(json.dumps(self.cache, indent=2))

    def _key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def ask(self, prompt: str, max_tokens: int = 600) -> str:
        key = self._key(prompt)
        if key in self.cache:
            return self.cache[key]

        if self.dry_run or self.client is None:
            result = "[DRY RUN - no LLM call made]\n" + prompt[:300]
        else:
            resp = self.client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            result = "".join(block.text for block in resp.content if block.type == "text")

        self.cache[key] = result
        self._save_cache()
        return result


def summarize_actions(actions: pd.Series) -> str:
    """Turn a column of free-text actions into a compact bullet list the
    LLM prompt can reference, rather than pasting every raw row."""
    counts = Counter(a.strip() for a in actions if a.strip() and a.strip().lower() != "nan")
    top = counts.most_common(8)
    return "\n".join(f"- ({n}x) {a}" for a, n in top)


def write_cluster_entry(writer: LLMWriter, tool_id: str, failure_type_mode: str,
                         cluster_df: pd.DataFrame) -> str:
    n = len(cluster_df)
    date_min = cluster_df["date_time"].min()
    date_max = cluster_df["date_time"].max()
    sample_descriptions = cluster_df["failure_description"].drop_duplicates().head(10).tolist()
    keywords = cluster_representative_terms(cluster_df["failure_description"].tolist())
    action_summary = summarize_actions(cluster_df["actions"])

    prompt = textwrap.dedent(f"""
        You are writing one entry in an internal engineering wiki about
        semiconductor fab tool failures, for other engineers to consult
        when this failure mode recurs. Be concrete and specific; do not
        pad with generic advice.

        Tool: {tool_id}
        Dominant failure_type label(s) in this group: {failure_type_mode}
        Occurrences: {n}, spanning {date_min} to {date_max}
        Representative keywords: {", ".join(keywords)}

        Sample raw failure descriptions from this cluster:
        {chr(10).join("- " + d for d in sample_descriptions)}

        Most common recorded actions taken (with counts):
        {action_summary}

        Write a wiki entry with this exact structure in Markdown:
        ### <a short, specific title for this failure mode, not generic>
        **Symptom:** 1-2 sentences describing what engineers observe.
        **Frequency:** how often/when this occurs, based on the data above.
        **Typical response:** what actions are usually taken.
        **What seems to work:** call out which action(s), if any, appear
        most associated with resolution, and flag if the data is too thin
        or inconsistent to say confidently.

        Keep the whole entry under 150 words. Do not invent facts not
        supported by the data above.
    """).strip()

    return writer.ask(prompt, max_tokens=500)


def write_tool_overview(writer: LLMWriter, tool_id: str, tool_df: pd.DataFrame,
                         cluster_titles: list[str]) -> str:
    failure_type_counts = tool_df["failure_type"].value_counts().head(5)
    prompt = textwrap.dedent(f"""
        Write a 3-4 sentence overview paragraph for the wiki landing page
        of fab tool "{tool_id}". It has {len(tool_df)} logged failure
        records spanning {tool_df['date_time'].min()} to {tool_df['date_time'].max()}.

        Top failure types by count:
        {failure_type_counts.to_string()}

        The page below this overview will list these specific failure
        modes: {", ".join(cluster_titles)}.

        Write only the overview paragraph (no heading, no bullet list of
        the failure modes -- those are rendered separately). Be factual
        and specific to the numbers given, not generic.
    """).strip()
    return writer.ask(prompt, max_tokens=250)


def write_index_overview(writer: LLMWriter, df: pd.DataFrame, tool_ids: list[str]) -> str:
    top_failure_types = df["failure_type"].value_counts().head(8)
    prompt = textwrap.dedent(f"""
        Write a short (4-6 sentence) landing-page overview for an internal
        wiki summarizing tool failures across a semiconductor fab. There
        are {len(df)} total logged records across {len(tool_ids)} tools,
        spanning {df['date_time'].min()} to {df['date_time'].max()}.

        Top failure types fab-wide:
        {top_failure_types.to_string()}

        Mention which failure types dominate and roughly how many tools
        are involved. Do not list individual tool IDs. Be factual, not
        generic filler.
    """).strip()
    return writer.ask(prompt, max_tokens=250)


# --------------------------------------------------------------------------
# 6. Assemble markdown wiki
# --------------------------------------------------------------------------

def build_wiki(df: pd.DataFrame, out_dir: Path, writer: LLMWriter):
    """Generates a single self-contained viewer.html with a WIKI pane
    (browse tool / failure-type pages) and a GRAPH pane (tool <-> failure
    type node-link diagram). No markdown files, no chat/query UI."""
    out_dir.mkdir(parents=True, exist_ok=True)

    df = build_clusters(df)
    tool_ids = sorted(df["tool_id"].unique())

    tools_data = []
    for tool_id in tool_ids:
        tool_df = df[df["tool_id"] == tool_id]
        cluster_entries = []
        cluster_titles = []

        for cluster_id, cluster_df in tool_df.groupby("cluster_id"):
            failure_type_mode = cluster_df["failure_type"].mode().iat[0]
            entry_md = write_cluster_entry(writer, tool_id, failure_type_mode, cluster_df)
            cluster_entries.append(entry_md)
            title_match = re.search(r"###\s*(.+)", entry_md)
            cluster_titles.append(title_match.group(1).strip() if title_match else cluster_id)

        overview = write_tool_overview(writer, tool_id, tool_df, cluster_titles)

        tools_data.append({
            "id": tool_id,
            "record_count": len(tool_df),
            "date_min": str(tool_df["date_time"].min()),
            "date_max": str(tool_df["date_time"].max()),
            "overview": overview,
            "entries": cluster_entries,
        })

    failure_types_data = []
    for failure_type, type_df in df.groupby("failure_type"):
        tools_hit = type_df["tool_id"].value_counts()
        failure_types_data.append({
            "id": slugify(failure_type),
            "label": failure_type,
            "record_count": len(type_df),
            "tools": [{"id": t, "count": int(ct)} for t, ct in tools_hit.items()],
        })

    index_overview = write_index_overview(writer, df, tool_ids)

    wiki_data = {
        "total_records": len(df),
        "date_min": str(df["date_time"].min()),
        "date_max": str(df["date_time"].max()),
        "index_overview": index_overview,
        "tools": tools_data,
        "failure_types": failure_types_data,
    }

    html = render_viewer_html(wiki_data)
    out_path = out_dir / "viewer.html"
    out_path.write_text(html)

    # also drop the raw structured data, useful for debugging / re-styling
    (out_dir / "wiki_data.json").write_text(json.dumps(wiki_data, indent=2))

    return out_path


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to failure log CSV")
    parser.add_argument("--out", default="./wiki", help="Output directory for the wiki")
    parser.add_argument("--dry-run", action="store_true",
                         help="Skip real LLM calls (for testing the pipeline structure)")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / ".llm_cache.json"

    df = load_data(args.csv)
    writer = LLMWriter(cache_path=cache_path, dry_run=args.dry_run)
    viewer_path = build_wiki(df, out_dir, writer)

    print(f"Wiki built: {viewer_path}")
    print(f"Open {viewer_path} in a browser -- no server needed.")


if __name__ == "__main__":
    main()
