"""
Generates a single self-contained viewer.html (no external CDN dependencies --
fabs frequently run on restricted or air-gapped networks) with two panes:
  - WIKI: browse tool pages / failure-type pages, rendered from the
    lightweight markdown produced by build_llm_wiki.py
  - GRAPH: a node-link diagram (tools <-> failure types), sized by record
    count, drawn with a small hand-rolled force layout (no D3 dependency)

No chat/query interface -- pure browse + visualize.
"""

import json

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fab Failure Wiki</title>
<style>
  :root {
    --bg: #10141a;
    --bg-panel: #161b22;
    --bg-panel-raised: #1b212a;
    --grid-line: #262e38;
    --text-primary: #e5e9ee;
    --text-muted: #7c8896;
    --text-dim: #4d5661;
    --accent-amber: #e8a33d;
    --accent-cyan: #4fc1e9;
    --accent-green: #5fbe8a;
    --accent-red: #e0707a;
    --mono: ui-monospace, "SF Mono", "Cascadia Code", "Consolas", "Roboto Mono", monospace;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }

  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--text-primary);
    font-family: var(--sans);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ---------- top bar ---------- */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 20px;
    border-bottom: 1px solid var(--grid-line);
    background: var(--bg-panel);
    flex-shrink: 0;
  }
  .brand {
    display: flex;
    align-items: baseline;
    gap: 10px;
  }
  .brand-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--accent-amber);
    box-shadow: 0 0 8px var(--accent-amber);
    flex-shrink: 0;
  }
  .brand-title {
    font-family: var(--mono);
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-primary);
  }
  .brand-sub {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
  }
  .view-toggle {
    display: flex;
    border: 1px solid var(--grid-line);
    border-radius: 3px;
    overflow: hidden;
  }
  .view-toggle button {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: var(--bg-panel);
    color: var(--text-muted);
    border: none;
    padding: 8px 18px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
  }
  .view-toggle button + button { border-left: 1px solid var(--grid-line); }
  .view-toggle button.active {
    background: var(--accent-amber);
    color: #1a1305;
  }
  .view-toggle button:not(.active):hover { color: var(--text-primary); background: var(--bg-panel-raised); }

  /* ---------- layout ---------- */
  .layout { flex: 1; display: flex; min-height: 0; }

  nav.rail {
    width: 280px;
    flex-shrink: 0;
    border-right: 1px solid var(--grid-line);
    background: var(--bg-panel);
    overflow-y: auto;
    padding: 16px 0;
  }
  .rail-section-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 4px 16px 8px;
    margin-top: 10px;
  }
  .rail-section-label:first-child { margin-top: 0; }
  .rail-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 16px;
    cursor: pointer;
    border-left: 2px solid transparent;
    transition: background 0.12s, border-color 0.12s;
  }
  .rail-item:hover { background: var(--bg-panel-raised); }
  .rail-item.active {
    background: var(--bg-panel-raised);
    border-left-color: var(--accent-amber);
  }
  .rail-item-dot {
    width: 6px; height: 6px; border-radius: 50%;
    flex-shrink: 0;
  }
  .rail-item-label {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-primary);
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .rail-item-count {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-dim);
  }

  main { flex: 1; min-width: 0; position: relative; overflow: hidden; }
  .pane { position: absolute; inset: 0; overflow-y: auto; }
  .pane[hidden] { display: none; }

  /* ---------- wiki pane ---------- */
  #wiki-pane .doc {
    max-width: 720px;
    margin: 0 auto;
    padding: 48px 40px 80px;
  }
  .doc-eyebrow {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 10px;
  }
  .doc-title {
    font-family: var(--sans);
    font-weight: 650;
    font-size: 28px;
    line-height: 1.25;
    margin: 0 0 6px;
    color: var(--text-primary);
  }
  .doc-meta {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--grid-line);
  }
  .doc-overview {
    font-size: 15px;
    line-height: 1.7;
    color: var(--text-muted);
    margin-bottom: 36px;
  }
  .doc h3 {
    font-family: var(--sans);
    font-weight: 650;
    font-size: 16px;
    color: var(--text-primary);
    margin: 30px 0 10px;
    padding-left: 12px;
    border-left: 2px solid var(--accent-amber);
  }
  .doc p { font-size: 14.5px; line-height: 1.75; color: var(--text-muted); margin: 8px 0; }
  .doc strong.field-label {
    font-family: var(--mono);
    font-size: 10.5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    display: block;
    margin-top: 14px;
  }
  .doc ul { margin: 8px 0; padding-left: 20px; }
  .doc li { font-size: 14px; line-height: 1.7; color: var(--text-muted); }
  .doc a { color: var(--accent-cyan); text-decoration: none; border-bottom: 1px solid rgba(79,193,233,0.3); }
  .doc a:hover { border-bottom-color: var(--accent-cyan); }
  .doc-empty {
    display: flex; align-items: center; justify-content: center;
    height: 100%; color: var(--text-dim); font-family: var(--mono); font-size: 13px;
  }

  /* ---------- graph pane ---------- */
  #graph-pane { display: flex; }
  #graph-svg-wrap { flex: 1; position: relative; }
  #graph-svg { width: 100%; height: 100%; }
  .graph-legend {
    position: absolute; top: 20px; left: 20px;
    background: rgba(22,27,34,0.9);
    border: 1px solid var(--grid-line);
    border-radius: 4px;
    padding: 12px 14px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
  }
  .graph-legend-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  .graph-legend-swatch { width: 10px; height: 10px; border-radius: 2px; }
  .graph-hint {
    position: absolute; bottom: 20px; left: 20px;
    font-family: var(--mono); font-size: 11px; color: var(--text-dim);
  }
  .node-tool circle { fill: var(--bg-panel-raised); stroke: var(--accent-amber); }
  .node-type circle { fill: var(--bg-panel-raised); stroke: var(--accent-cyan); }
  .node-label {
    font-family: var(--mono);
    font-size: 10px;
    fill: var(--text-primary);
    pointer-events: none;
  }
  .link-line { stroke: var(--grid-line); stroke-width: 1; }
  .link-line.highlight { stroke: var(--accent-amber); stroke-width: 1.6; }
  .node-group { cursor: pointer; }
  .node-group.dimmed { opacity: 0.25; }
</style>
</head>
<body>

<header>
  <div class="brand">
    <span class="brand-dot"></span>
    <span class="brand-title">Fab Failure Wiki</span>
    <span class="brand-sub" id="brand-sub"></span>
  </div>
  <div class="view-toggle">
    <button id="btn-wiki" class="active">Wiki</button>
    <button id="btn-graph">Graph</button>
  </div>
</header>

<div class="layout">
  <nav class="rail" id="rail"></nav>
  <main>
    <div class="pane" id="wiki-pane"><div class="doc" id="doc"></div></div>
    <div class="pane" id="graph-pane" hidden>
      <div id="graph-svg-wrap">
        <svg id="graph-svg"></svg>
        <div class="graph-legend">
          <div class="rail-section-label" style="padding:0 0 6px;">Legend</div>
          <div class="graph-legend-row"><span class="graph-legend-swatch" style="background:var(--accent-amber)"></span>Tool</div>
          <div class="graph-legend-row"><span class="graph-legend-swatch" style="background:var(--accent-cyan)"></span>Failure type</div>
        </div>
        <div class="graph-hint">Click a node to open its wiki page &middot; drag to reposition</div>
      </div>
    </div>
  </main>
</div>

<script>
const DATA = __WIKI_DATA_JSON__;

/* ---------------- lightweight markdown-ish renderer ----------------
   Our generated pages only ever contain: ### headings, **Field:** labels,
   plain paragraphs, "- " bullet lists, and [text](path) links. No need
   for a full markdown library. */
function renderDoc(md) {
  const lines = md.split("\n");
  let html = "";
  let inList = false;
  const closeList = () => { if (inList) { html += "</ul>"; inList = false; } };

  const inlineFmt = (s) => {
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, href) => {
      return `<a href="#" data-nav="${href}">${text}</a>`;
    });
    s = s.replace(/\*\*(.+?):\*\*/g, '<strong class="field-label">$1</strong>');
    s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    return s;
  };

  for (const raw of lines) {
    const line = raw.trim();
    if (!line) { closeList(); continue; }
    if (line.startsWith("### ")) {
      closeList();
      html += `<h3>${inlineFmt(line.slice(4))}</h3>`;
    } else if (line.startsWith("- ")) {
      if (!inList) { html += "<ul>"; inList = true; }
      html += `<li>${inlineFmt(line.slice(2))}</li>`;
    } else if (line.startsWith("---")) {
      closeList();
    } else if (line.startsWith("*") && line.endsWith("*") && !line.startsWith("**")) {
      closeList();
      html += `<p style="color:var(--text-dim);font-size:12px;">${inlineFmt(line.slice(1,-1))}</p>`;
    } else {
      closeList();
      html += `<p>${inlineFmt(line)}</p>`;
    }
  }
  closeList();
  return html;
}

/* ---------------- rail navigation ---------------- */
const rail = document.getElementById("rail");
const docEl = document.getElementById("doc");
let currentPageId = null;

function severityColor(count, max) {
  const t = max > 0 ? count / max : 0;
  if (t > 0.66) return "var(--accent-red)";
  if (t > 0.33) return "var(--accent-amber)";
  return "var(--accent-green)";
}

function buildRail() {
  const maxToolCount = Math.max(1, ...DATA.tools.map(t => t.record_count));
  const maxTypeCount = Math.max(1, ...DATA.failure_types.map(t => t.record_count));

  let html = '<div class="rail-section-label">Tools</div>';
  for (const t of DATA.tools) {
    html += `<div class="rail-item" data-page="tool:${t.id}">
      <span class="rail-item-dot" style="background:${severityColor(t.record_count, maxToolCount)}"></span>
      <span class="rail-item-label">${t.id}</span>
      <span class="rail-item-count">${t.record_count}</span>
    </div>`;
  }
  html += '<div class="rail-section-label">Failure types</div>';
  for (const ft of DATA.failure_types) {
    html += `<div class="rail-item" data-page="type:${ft.id}">
      <span class="rail-item-dot" style="background:${severityColor(ft.record_count, maxTypeCount)}"></span>
      <span class="rail-item-label">${ft.label}</span>
      <span class="rail-item-count">${ft.record_count}</span>
    </div>`;
  }
  rail.innerHTML = html;

  rail.querySelectorAll(".rail-item").forEach(el => {
    el.addEventListener("click", () => openPage(el.dataset.page));
  });
}

function findTool(id) { return DATA.tools.find(t => t.id === id); }
function findType(id) { return DATA.failure_types.find(t => t.id === id); }

function openPage(pageKey) {
  currentPageId = pageKey;
  rail.querySelectorAll(".rail-item").forEach(el => {
    el.classList.toggle("active", el.dataset.page === pageKey);
  });

  const [kind, id] = pageKey.split(/:(.+)/);
  if (kind === "tool") {
    const t = findTool(id);
    docEl.innerHTML = `
      <div class="doc-eyebrow">Tool</div>
      <h1 class="doc-title">${t.id}</h1>
      <div class="doc-meta">${t.record_count} records &middot; ${t.date_min} &rarr; ${t.date_max}</div>
      <div class="doc-overview">${t.overview}</div>
      ${t.entries.map(e => renderDoc(e)).join("")}
    `;
  } else if (kind === "type") {
    const ft = findType(id);
    docEl.innerHTML = `
      <div class="doc-eyebrow">Failure type</div>
      <h1 class="doc-title">${ft.label}</h1>
      <div class="doc-meta">${ft.record_count} records across ${ft.tools.length} tool(s)</div>
      <div class="doc-overview">Tools affected:</div>
      <ul>${ft.tools.map(tt => `<li><a href="#" data-nav="tool:${tt.id}">${tt.id}</a> &mdash; ${tt.count} occurrence(s)</li>`).join("")}</ul>
    `;
  } else if (kind === "index") {
    docEl.innerHTML = `
      <div class="doc-eyebrow">Overview</div>
      <h1 class="doc-title">Fab Failure Wiki</h1>
      <div class="doc-meta">${DATA.total_records} records &middot; ${DATA.tools.length} tools &middot; ${DATA.date_min} &rarr; ${DATA.date_max}</div>
      <div class="doc-overview">${DATA.index_overview}</div>
    `;
  }

  docEl.querySelectorAll("[data-nav]").forEach(a => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      openPage(a.dataset.nav);
    });
  });

  document.getElementById("wiki-pane").scrollTop = 0;
}

/* ---------------- view toggle ---------------- */
const btnWiki = document.getElementById("btn-wiki");
const btnGraph = document.getElementById("btn-graph");
const wikiPane = document.getElementById("wiki-pane");
const graphPane = document.getElementById("graph-pane");

btnWiki.addEventListener("click", () => {
  btnWiki.classList.add("active"); btnGraph.classList.remove("active");
  wikiPane.hidden = false; graphPane.hidden = true;
});
btnGraph.addEventListener("click", () => {
  btnGraph.classList.add("active"); btnWiki.classList.remove("active");
  graphPane.hidden = false; wikiPane.hidden = true;
  if (!graphInitialized) initGraph();
});

/* ---------------- graph view: small hand-rolled force layout ---------------- */
let graphInitialized = false;

function initGraph() {
  graphInitialized = true;
  const svg = document.getElementById("graph-svg");
  const wrap = document.getElementById("graph-svg-wrap");
  const W = wrap.clientWidth, H = wrap.clientHeight;
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);

  const nodes = [];
  const nodeIndex = {};
  const maxToolCount = Math.max(1, ...DATA.tools.map(t => t.record_count));
  const maxTypeCount = Math.max(1, ...DATA.failure_types.map(t => t.record_count));

  DATA.tools.forEach((t, i) => {
    const n = { id: "tool:" + t.id, kind: "tool", label: t.id,
      r: 14 + 16 * (t.record_count / maxToolCount),
      x: W/2 + Math.cos(i) * 120, y: H/2 + Math.sin(i) * 120 };
    nodeIndex[n.id] = n; nodes.push(n);
  });
  DATA.failure_types.forEach((ft, i) => {
    const n = { id: "type:" + ft.id, kind: "type", label: ft.label,
      r: 10 + 14 * (ft.record_count / maxTypeCount),
      x: W/2 + Math.cos(i*1.7+1) * 260, y: H/2 + Math.sin(i*1.7+1) * 260 };
    nodeIndex[n.id] = n; nodes.push(n);
  });

  const links = [];
  DATA.failure_types.forEach(ft => {
    ft.tools.forEach(tt => {
      links.push({ source: nodeIndex["tool:" + tt.id], target: nodeIndex["type:" + ft.id], weight: tt.count });
    });
  });

  // simple force simulation: repulsion + spring links + centering, few iterations
  function simulate(iterations) {
    for (let it = 0; it < iterations; it++) {
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j];
          let dx = a.x - b.x, dy = a.y - b.y;
          let dist = Math.sqrt(dx*dx + dy*dy) || 1;
          const minDist = a.r + b.r + 40;
          if (dist < minDist * 3) {
            const force = (minDist * minDist) / (dist * dist) * 0.6;
            dx /= dist; dy /= dist;
            a.x += dx * force; a.y += dy * force;
            b.x -= dx * force; b.y -= dy * force;
          }
        }
      }
      links.forEach(l => {
        let dx = l.target.x - l.source.x, dy = l.target.y - l.source.y;
        let dist = Math.sqrt(dx*dx + dy*dy) || 1;
        const targetDist = 130;
        const f = (dist - targetDist) * 0.02;
        dx /= dist; dy /= dist;
        l.source.x += dx * f; l.source.y += dy * f;
        l.target.x -= dx * f; l.target.y -= dy * f;
      });
      nodes.forEach(n => {
        n.x += (W/2 - n.x) * 0.003;
        n.y += (H/2 - n.y) * 0.003;
        n.x = Math.max(n.r + 10, Math.min(W - n.r - 10, n.x));
        n.y = Math.max(n.r + 10, Math.min(H - n.r - 10, n.y));
      });
    }
  }
  simulate(300);

  const svgNS = "http://www.w3.org/2000/svg";
  const linkGroup = document.createElementNS(svgNS, "g");
  const nodeGroup = document.createElementNS(svgNS, "g");
  svg.innerHTML = "";
  svg.appendChild(linkGroup);
  svg.appendChild(nodeGroup);

  const linkEls = links.map(l => {
    const line = document.createElementNS(svgNS, "line");
    line.setAttribute("class", "link-line");
    linkGroup.appendChild(line);
    return { el: line, l };
  });

  function redrawLinks() {
    linkEls.forEach(({el, l}) => {
      el.setAttribute("x1", l.source.x); el.setAttribute("y1", l.source.y);
      el.setAttribute("x2", l.target.x); el.setAttribute("y2", l.target.y);
    });
  }
  redrawLinks();

  nodes.forEach(n => {
    const g = document.createElementNS(svgNS, "g");
    g.setAttribute("class", "node-group node-" + n.kind);
    g.setAttribute("transform", `translate(${n.x},${n.y})`);

    const circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("r", n.r);
    g.appendChild(circle);

    const label = document.createElementNS(svgNS, "text");
    label.setAttribute("class", "node-label");
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("dy", n.r + 14);
    label.textContent = n.label;
    g.appendChild(label);

    g.addEventListener("click", () => {
      btnWiki.click();
      openPage(n.id);
    });
    g.addEventListener("mouseenter", () => highlightNode(n));
    g.addEventListener("mouseleave", () => clearHighlight());

    // dragging
    let dragging = false;
    g.addEventListener("mousedown", (e) => { dragging = true; e.preventDefault(); });
    window.addEventListener("mousemove", (e) => {
      if (!dragging) return;
      const rect = svg.getBoundingClientRect();
      const scaleX = W / rect.width, scaleY = H / rect.height;
      n.x = (e.clientX - rect.left) * scaleX;
      n.y = (e.clientY - rect.top) * scaleY;
      g.setAttribute("transform", `translate(${n.x},${n.y})`);
      redrawLinks();
    });
    window.addEventListener("mouseup", () => dragging = false);

    n.el = g;
    nodeGroup.appendChild(g);
  });

  function highlightNode(n) {
    const connected = new Set([n.id]);
    linkEls.forEach(({el, l}) => {
      const touches = l.source.id === n.id || l.target.id === n.id;
      el.classList.toggle("highlight", touches);
      if (touches) { connected.add(l.source.id); connected.add(l.target.id); }
    });
    nodes.forEach(nn => nn.el.classList.toggle("dimmed", !connected.has(nn.id)));
  }
  function clearHighlight() {
    linkEls.forEach(({el}) => el.classList.remove("highlight"));
    nodes.forEach(nn => nn.el.classList.remove("dimmed"));
  }
}

/* ---------------- init ---------------- */
document.getElementById("brand-sub").textContent =
  `${DATA.total_records} records · ${DATA.tools.length} tools · ${DATA.failure_types.length} failure types`;
buildRail();
openPage("index:overview");
</script>
</body>
</html>
"""


def render_viewer_html(wiki_data: dict) -> str:
    return HTML_TEMPLATE.replace("__WIKI_DATA_JSON__", json.dumps(wiki_data))
