# Tool Status Profile: RIE03

## 1. Executive Health Summary

RIE03 is a high-utilization etch tool with **chronic RF/bias compliance instability**, **recipe-specific fragility (N2O2 / TMR families)**, and **recurrent vacuum-transfer reliability issues** (slit valve, chuck seal, backside handling, pump seals). Over the 2024–mid‑2026 window, the tool has remained largely available for production, but only under **tight recipe whitelisting** and **frequent re‑qualification cycles**.

Key health themes:

- **RF / Bias / Matchbox / Generator Instability (Primary Chronic Issue)**
  - Dominant failure mode: “RF voltage is out of compliance” plus “Bias issues on RF or recipes”, “RF match box or connection issues”, “RF generator issues”.
  - Multiple hardware interventions:
    - RF1 and RF2 match box replacements and cable swaps (e.g., 8/30/2025, 9/8/2025, 2/2–2/3/2026, 2/21/2026, 2/26/2026).
    - RF generator stress tests and replacement (5/16–5/19/2025 dummy-load testing; generator replaced 2/13/2026).
    - Repeated tuning of RF1/2 load/tune capacitors and reflected power tolerances (6/3/2025, 8/26/2025, 9/3–9/4/2025, 10/8/2025, 8/30/2025, 1/5–1/6/2026, 2/17/2026).
  - Persistent **recipe-dependent RF compliance alarms**:
    - N2O2 family (N2O2_100S, N2O2_1.7/1.8/XXXsccm_115S) and TMR-FLTR-RIE family repeatedly fail RF/DC compliance and etch rate specs.
    - MPL1024 and PMR_MIX2 generally run clean and are used as “safe” monitor recipes.
  - Operational mitigations:
    - RF1 reflected tolerance adjusted (100W → 6W → 30W) to balance alarm sensitivity vs. high-power recipes.
    - Strict rule: any RF alarm on a recipe family → that family is declared down; tool only up for whitelisted recipes (MPL1024, PMR_MIX2, PP3_ASH_6W_7M, UU9Q, etc.).
    - Frequent dummy wafer runs to validate RF stability before returning to manufacturing (RTP/RTM).

- **Etch Rate / Process Stability Issues (Secondary Chronic Issue)**
  - Recurrent “Etch Rate issues” tied to:
    - Chamber condition (heavy coating on ICP head, clamp plate, feature plate; multiple wet cleans and Scotch-Brite scrubs).
    - MFC performance (O2 and N2 MFC replacements; flow stability checks).
    - RF timing (RF1/ICP/RF2 “Go On Delay” adjustments between 2000–5000 ms).
  - Extensive conditioning campaigns:
    - ALTIC and PR wafers used repeatedly for chamber conditioning and burn-in (5/6–5/7/2025, 7/19–7/21/2025, 8/10–8/13/2025, 8/25–8/30/2025, 12/9–12/10/2025, 2/23–2/26/2026, 4/7/2026, 5/10/2026, 6/22/2026).
  - MFC-related etch rate recovery:
    - O2 MFC replacement (8/29/2025) and N2 MFC replacement (1/3/2026) with documented qual passes (SLIM34, SLIM29).
    - Ongoing MFC part tracking and replacement planning (6/19–6/22/2024, 8/29–8/30/2025, 12/23/2025, 1/6/2026).

- **Vacuum Transfer / Mechanical Reliability**
  - **Slit valve issues**:
    - Frequent PM2 slit valve open timeouts and failures, often correlated with high TM pressure.
    - Most events cleared by reboot + manual TM pump-down + retry; error often non-repeatable.
    - Chronic but low-severity; rarely requires hardware replacement, but impacts throughput and wafer-at-risk handling.
  - **Chuck seal / helium stabilization / backside issues**:
    - Multiple alarms: “Chuck seal issues”, “helium took too long to stabilize”, “Backside issues”.
    - Actions include aborting wafers, dummy verification runs, venting PM to retrieve wafers, and adjusting robot Z-height to eliminate backside dragging.
    - Chuck clamp replacements and lift bellows/linear slide replacement (10/24/2025, 4/15/2026) to address mechanical and scratch-related defects.
  - **Pump / LL/TM sealing issues**:
    - Recurrent “Pump issues” resolved by cleaning LL door o-rings and seals (4/9/2026, 4/14/2026, 4/30/2026, 5/6/2026, 6/15/2026).
    - LL/TM routinely pumped down to ~40 mT after seal cleaning.

- **System Operating / Software / Mapping / Facility Issues**
  - System operating issues include keyboard failures, mapping sensor degradation, and PCS/ELOG anomalies.
    - Keyboard and PM2 computer replacements/reboots (1/23/2024).
    - Mapping sensor repair: mirror replacement, transmitter swap, light source swap, full cassette mapping verification (5/19/2026).
    - PCS/ELOG issues requiring D0 and qual flow before proceeding (6/28–6/29/2026).
  - Facility/power glitches:
    - Power glitch events requiring pump/chiller recovery and tool reboot (2/7/2024, 8/9/2024).
  - Overall, system/PCS issues are intermittent and resolved with standard IT/controls maintenance.

- **Recipe Governance / Qualification Failures**
  - Multiple explicit **EWAIV / “do not run” directives**:
    - Do not run UZ1W on #39887 (1/13/2025).
    - Do not run N2O2 family recipes (8/24/2025, 1/15–1/16/2026, 3/21/2026).
    - Do not run TMR-FLTR-RIE (7/1/2025, 1/24/2026, 3/16/2026).
    - Restrict tool to MPL1024, PMR_MIX2, PP3_ASH_6W_7M, UU9Q when RF/etch issues persist (3/14/2026).
  - Qualification failures and recipe-specific S/A (service action) requests for MPL1024 and others (1/29/2024, 6/27/2025, 6/29/2026, 7/5/2026).
  - Tool frequently toggles between “Ready for Qual”, “RTP”, and “Tool down for EE/MEVC” states depending on qual outcomes.

**Overall Health Assessment:**

- **Functional but fragile**: RIE03 can meet spec for selected recipes (MPL1024, PMR_MIX2, Slim etch rate) when RF hardware is freshly tuned and chamber/MFCs are conditioned.
- **Chronic RF/etch-rate sensitivity**: N2O2 and TMR families remain unstable despite extensive RF hardware work; these recipes should be treated as **high-risk** and kept under engineering-only operation until root cause is fully resolved.
- **Mechanical/vacuum reliability is manageable**: Slit valve, chuck seal, backside, and pump issues are frequent but typically cleared with standard mechanical maintenance and do not show catastrophic trends.
- **Recommendation**: Maintain strict recipe whitelisting, enforce RF tuning and MFC verification before any qual, and continue RF system root-cause work (matchbox, cabling, generator, control logic) focused on N2O2/TMR behavior.

---

## 2. Chronic Failure Modes & Cross-Links

Below are the dominant recurring failure modes for RIE03, formatted for cross-linking and with concise technical characterization.

### 2.1 RF / Bias / Matchbox / Generator Instability

- [[RF Voltage Out of Compliance]]
  - Symptoms: RF1 RF/DC voltage alarms, reflected power above tolerance, plasma strike failures, slot-dependent alarms (e.g., slots 2/4/6/8 only).
  - Root-cause cluster:
    - RF1/2 matchbox drift or failure.
    - Loose RF2 cable to ICP head.
    - Inadequate or mis-set RF load/tune presets.
    - Recipe steps with aggressive RF1 power and tight reflected tolerance.
  - Typical actions:
    - Reset RF generators and matchboxes; re-tune load/tune capacitors.
    - Adjust RF1 reflected tolerance (e.g., 30W compromise).
    - Run dummy wafers on monitor recipes (MPL1024, PMR_MIX2, N2O2-100S) to validate.
    - Replace RF1/RF2 matchboxes and RF cables; stress-test RF generators on dummy loads.
  - Cross-links:
    - [[Bias Issues on RF or Recipes]]
    - [[RF Match Box or Connection Issues]]
    - [[RF Generator Issues]]
    - [[Recipe Issues]]
    - [[Etch Rate Issues]]

- [[Bias Issues on RF or Recipes]]
  - Symptoms: DC bias not coming up, bias out of spec, no-bias conditions on certain recipes.
  - Actions:
    - Reset RF generator; inspect clamp plate and ICP head for coating; clean or replace hardware.
    - Clean RF feed-through rods, copper rings, plates; reassemble caps.
    - Tune RF2 match box to achieve near-zero reflected at target bias (e.g., 240W).
    - Validate bias behavior across recipe set (PMR_MIX2, PP3_ASH_6W_7M, MPL1024, N2O2 variants).
  - Cross-links:
    - [[RF Voltage Out of Compliance]]
    - [[Etch Rate Issues]]
    - [[Recipe Issues]]

- [[RF Match Box or Connection Issues]]
  - Symptoms: RF cannot tune, reflected power remains high, intermittent RF compliance alarms, recipe-specific failures.
  - Actions:
    - Replace RF1 and RF2 matchboxes.
    - Replace RF2 RF cable; verify mechanical integrity and connections at ICP head and matchbox.
    - Work with OEM FSE (Plasma-Therm) to swap matchboxes and validate performance.
    - Clean chamber surfaces and inspect RF2 connection before closing chamber.
  - Cross-links:
    - [[RF Voltage Out of Compliance]]
    - [[RF Generator Issues]]
    - [[Etch Rate Issues]]

- [[RF Generator Issues]]
  - Symptoms: RF output instability, suspected generator degradation, need to differentiate generator vs. matchbox/chamber issues.
  - Actions:
    - Place generator on RF dummy load at full power for 1 hour; verify stability.
    - If generator passes, run failing process and log load/tune capacitor movements and reflected power.
    - Replace RF generator when confirmed faulty; re-qualify with 5-wafer tests.
    - Coordinate expedited repair with Seren and Plasma-Therm.
  - Cross-links:
    - [[RF Voltage Out of Compliance]]
    - [[RF Match Box or Connection Issues]]

- [[Tuning Issues]]
  - Symptoms: RF cannot tune to low reflected power; manual tuning required; step-specific tuning failures (e.g., step 8 of N2O2_100S).
  - Actions:
    - Abort wafer; run dummy with same recipe; manually tune load/tune to <5W reflected.
    - Adjust RF1/2 presets and “Go On Delay” values; iterate qual.
    - Escalate persistent tuning failures to EE for recipe-level changes.
  - Cross-links:
    - [[RF Voltage Out of Compliance]]
    - [[Etch Rate Issues]]
    - [[Recipe Issues]]

### 2.2 Etch Rate / Process Stability

- [[Etch Rate Issues]]
  - Symptoms: Etch rate out of spec, high variability, qual failures on Slim etch rate and N2O2 monitors.
  - Root-cause cluster:
    - Chamber condition (coating on ICP head, clamp plate, feature plate).
    - MFC drift or failure (O2, N2).
    - RF timing (RF1/ICP/RF2 delays) and reflected power behavior.
  - Actions:
    - Wet clean chamber and spool; Scotch-Brite clean stainless surfaces.
    - Clean ICP head, clamp plate, feature plate; replace clamp when needed.
    - Run extensive conditioning (ALTIC, PR wafers) before qual.
    - Replace O2 and N2 MFCs; pump out gas lines; verify flow stability via TIM data.
    - Adjust RF1/ICP/RF2 “Go On Delay” (2000–5000 ms) and RF1 phase/mag to reduce reflected power.
    - Perform Slim etch rate and N2O2 quals; log B/A/D/ER metrics.
  - Cross-links:
    - [[MFC Issues]]
    - [[RF Voltage Out of Compliance]]
    - [[Bias Issues on RF or Recipes]]
    - [[Recipe Issues]]

- [[MFC Issues]]
  - Symptoms: Flow instability, need for extended gas flow flushing, qual dependencies on MFC performance.
  - Actions:
    - Replace O2 and N2 MFCs; flush gas lines for ≥1 hour.
    - Verify new MFC via dummy runs and TIM flow stability.
    - Track part numbers and coordinate EE review of qual data (RF1 DCV, TV positions).
  - Cross-links:
    - [[Etch Rate Issues]]
    - [[Recipe Issues]]

### 2.3 Vacuum Transfer / Mechanical

- [[Slit Valve Issues]]
  - Symptoms: Slit valve open timeout, failure to open/close, wafer stuck in TM/PM, high TM pressure preventing valve operation.
  - Actions:
    - Reboot system; manually pump down TM and LM.
    - Manually open PM2 slit valve and transfer wafer; repeat sequence as needed.
    - Retry slit valve operation; monitor for non-repeatable errors.
    - Degas ion gauge and verify pressure readings.
  - Cross-links:
    - [[Pump Issues]]
    - [[System Operating Issues]]

- [[Chuck Seal Issues]]
  - Symptoms: Helium seal failures, chuck leak alarms, wafers aborted mid-process, slot-specific chuck alarms.
  - Actions:
    - Abort wafer; return to cassette; leave suspect wafer for MEVC inspection.
    - Run dummy wafers to verify chuck seal stability.
    - Replace clamp, lift bellows, and linear slide; perform chamber burn-in and function tests.
    - Refer to prior MESA comments for detailed chuck diagnostics.
  - Cross-links:
    - [[Helium Took Too Long to Stabilize]]
    - [[Backside Issues]]
    - [[Scrath Issues]]

- [[Helium Took Too Long to Stabilize]]
  - Symptoms: He stabilization timeout, wafer at risk in PM, repeated alarms on specific recipes (TMR-FLTR-RIE, N2O2).
  - Actions:
    - Recover wafers in-process; vent PM to retrieve wafer when necessary.
    - Run dummy wafers to verify He stabilization; pump down and vent tool as needed.
    - Mark tool requiring qualification after He-related interventions.
  - Cross-links:
    - [[Chuck Seal Issues]]
    - [[Etch Rate Issues]]

- [[Backside Issues]]
  - Symptoms: Backside contact/dragging, wafer handling anomalies, dummy wafers failing backside checks.
  - Actions:
    - Stop process; unload wafer; test with clean dummy wafers.
    - Adjust robot Z-height (e.g., 0.366 → 0.346) to eliminate dragging on put/get.
    - Verify full transfer cycle; declare tool ready for qual; vent chamber if needed.
  - Cross-links:
    - [[Chuck Seal Issues]]
    - [[Material or Wafer Was Not Detected]]

- [[Pump Issues]]
  - Symptoms: LL/TM pump-down failures, pressure out-of-compliance, LL o-ring contamination.
  - Actions:
    - Manually pump down TM/LM; clean LL door o-ring and seals with acetone/IPA.
    - Retry pump; confirm LL/TM down to ~40 mT.
    - Qual as needed after pump/seal maintenance.
  - Cross-links:
    - [[Pressure Out of Compliance]]
    - [[Slit Valve Issues]]

- [[Pressure Out of Compliance]]
  - Symptoms: Ion gauge not turning on, slot-specific pressure alarms, LL/PM pressure high.
  - Actions:
    - Reboot system; re-enable ion gauge.
    - Clean LL o-rings; verify pump-down.
    - Track slot status (processed vs. unprocessed) and protect wafers.
  - Cross-links:
    - [[Pump Issues]]
    - [[System Operating Issues]]

- [[Scrath Issues]]
  - Symptoms: Wafer scratches attributed to clamp or mechanical interference.
  - Actions:
    - Vent tool; replace clamp; run multiple dummy sets; MEVC visual inspection.
    - Tool kept vented; qualification required before production.
  - Cross-links:
    - [[Chuck Seal Issues]]
    - [[Backside Issues]]

### 2.4 Handling / Detection / Mapping / Software

- [[Material or Wafer Was Not Detected]]
  - Symptoms: Wafer presence alarms despite wafer on robot arm or in TM; mapping inconsistencies; dummy wafers worn out.
  - Actions:
    - Verify wafer location (arm, TM, cassette); unload/reload as needed.
    - Replace worn Altic dummy wafers; avoid reusing degraded dummies.
    - Repair mapping sensor: swap light sources, replace cracked mirror, replace transmitter; validate with full cassette mapping.
  - Cross-links:
    - [[System Operating Issues]]
    - [[Backside Issues]]

- [[System Operating Issues]]
  - Symptoms: Keyboard failures, PM2 computer issues, mapping sensor degradation, PCS/ELOG anomalies.
  - Actions:
    - Reboot PM2 computer; reinitialize application; replace keyboard.
    - Home elevator and robot; test wafer mapping and transfer.
    - Repair mapping optics and electronics; validate mapping with full cassette.
    - For PCS/ELOG issues, perform D0 and qualification flow before production.
  - Cross-links:
    - [[Material or Wafer Was Not Detected]]
    - [[Software, PCS, ELOG Issues]]

- [[Software, PCS, ELOG Issues]]
  - Symptoms: PCS/ELOG alarms, need for D0 and qual flow, software-related run interruptions.
  - Actions:
    - Perform D0; execute qualification flow; prepare SLIM and monitor wafers.
    - Coordinate with maintenance/IT to recover PCS/ELOG functionality.
  - Cross-links:
    - [[System Operating Issues]]

- [[Facility Issues]]
  - Symptoms: Power glitches, facility-related tool down events.
  - Actions:
    - Recover pumps and chillers; reboot computer and tool.
    - Confirm stable facility power before resuming production.
  - Cross-links:
    - [[System Operating Issues]]

### 2.5 Recipe Governance / Qualification

- [[Recipe Issues]]
  - Symptoms: Recipe-specific alarms, persistent failures on N2O2 and TMR-FLTR-RIE, MPL1024 service actions, qualification failures.
  - Actions:
    - EWAIV / tool-down directives for problematic recipes (N2O2 family, TMR-FLTR-RIE, UZ1W).
    - Restrict tool to qualified recipes (MPL1024, PMR_MIX2, PP3_ASH_6W_7M, UU9Q).
    - Request EE/MEVC S/A for MPL1024 and other recipes; adjust RF delays and tuning parameters.
    - Run targeted quals (Slim etch rate, N2O2) after RF/MFC/chamber interventions.
  - Cross-links:
    - [[RF Voltage Out of Compliance]]
    - [[Etch Rate Issues]]
    - [[Qualification Failures]]

- [[Qualification Failures]]
  - Symptoms: Monitor/qual wafers out of spec; explicit “do not run” directives.
  - Actions:
    - Stop running affected recipe (e.g., UZ1W, N2O2 variants, TMR-FLTR-RIE).
    - Perform chamber conditioning and RF/MFC tuning; re-run quals.
    - MEVC/EE review of qual data logs (RF1 DCV, TV positions, etch metrics).
  - Cross-links:
    - [[Recipe Issues]]
    - [[Etch Rate Issues]]

- [[Others]]
  - Catch-all for non-categorized issues (sensor adjustments, TVP high, lift bellows replacement, EE-only investigations).
  - Typically associated with tool-down for engineering and non-standard diagnostics.

---

## 3. Standard Troubleshooting Operating Procedures (SOP)

This section defines **standardized response flows** for the major chronic failure modes on RIE03. These SOPs should be used by maintenance, production, and engineering teams to ensure consistent handling and documentation.

### 3.1 SOP – [[RF Voltage Out of Compliance]] / [[Bias Issues on RF or Recipes]]

**Trigger:** RF1 RF/DC voltage alarm, bias out-of-compliance, plasma strike failure, or repeated RF alarms on a specific recipe/slot.

**Step 1 – Immediate Wafer Protection**

1. Abort the current process step.
2. Record slot and recipe:
   - Note which slots are processed vs. unprocessed (e.g., “Slot2 wafer in PM1, Slots3–6 in LL unprocessed”).
3. Return wafers to safe locations:
   - If possible, return wafers to LL cassette.
   - If wafer is stuck in PM, document status and leave for engineering if removal risks damage.

**Step 2 – Quick RF Health Check**

1. Stop process and unload all wafers from PM.
2. Reset RF generators and matchboxes:
   - Power-cycle RF1 and RF2 generators.
   - Reset match controllers to known baseline (e.g., 50/50 or prior validated presets).
3. Run **dummy wafers** on a known-good monitor recipe:
   - Preferred: MPL1024 or PMR_MIX2.
   - Observe:
     - Reflected power (target <5W).
     - DC bias stability.
     - Plasma strike behavior.

**Step 3 – RF Tuning and Hardware Inspection**

1. Tune RF1/2 load/tune capacitors:
   - Use prior validated settings (e.g., RF1 L/T 55/65, 85/60, or recipe-specific presets).
   - Adjust until reflected power is minimized and DC bias is within spec.
2. Inspect RF hardware:
   - Verify RF2 cable to ICP head is tight; check connectors for arcing or damage.
   - Confirm matchbox cooling and mechanical integrity.
3. If alarms persist:
   - Swap or replace RF matchbox (RF1 or RF2 as indicated).
   - If generator suspected, perform dummy-load stress test:
     - Run generator at full power on dummy load for 1 hour.
     - If unstable, remove generator and send for expedited repair.

**Step 4 – Recipe-Level Governance**

1. If RF alarms occur **only on specific recipes** (e.g., N2O2_100S, TMR-FLTR-RIE, MPL1024):
   - Apply SL rule: **any RF alarm → recipe family is down**.
   - EWAIV tool not to run that recipe family until EE/MEVC clearance.
2. Restrict tool to **whitelisted recipes**:
   - MPL1024, PMR_MIX2, PP3_ASH_6W_7M, UU9Q, and other recipes with recent clean qual history.
3. Document:
   - RF1 reflected tolerance setting (e.g., 30W vs. 100W).
   - Load/tune positions at failure and after tuning.
   - Recipe step where alarm occurs (e.g., step 8).

**Step 5 – Qualification and Return to Manufacturing**

1. Run monitor/qual wafers:
   - Slim etch rate qual (SLIM ER).
   - N2O2 qual if recipe family is being re-enabled.
2. Confirm:
   - RF/DC compliance across all qual wafers.
   - Etch metrics within spec (B/A/D/ER).
3. If all passes:
   - Mark tool **RTP/RTM** for whitelisted recipes only.
   - Keep N2O2/TMR families down until explicit EE sign-off.

---

### 3.2 SOP – [[Etch Rate Issues]] / [[MFC Issues]]

**Trigger:** Etch rate qual failure, high variability, or explicit “Etch Rate issues” / MFC alarms.

**Step 1 – Stabilize Chamber Condition**

1. Stop production; put tool in engineering/qual mode.
2. Perform chamber maintenance:
   - Wet clean chamber and spool.
   - Scotch-Brite clean stainless surfaces, clamp plate, feature plate.
   - Inspect ICP head for coating; scrub as needed.
   - Replace clamp if edges are heavily coated or causing scratches.

**Step 2 – Gas Delivery / MFC Verification**

1. Identify suspect MFCs (O2, N2):
   - Review TIM data for flow stability and drift.
2. Replace MFCs:
   - Install new O2 and/or N2 MFCs per EE plan.
   - Flush gas lines with continuous flow for ≥1 hour.
3. Run dummy wafers:
   - Use ALTIC or PR wafers for conditioning.
   - Confirm stable flows and no gas-related alarms.

**Step 3 – RF Timing and Reflected Power Optimization**

1. Adjust RF “Go On Delay” parameters:
   - RF1/ICP/RF2 delays between 2000–5000 ms as per EE guidance.
   - Example: RF1 delay 2000 ms; RF2 delay 2000 ms; ICP delay 2000 or 5000 ms.
2. Null RF1/2 phase/magnitude:
   - Reduce reflected power (e.g., RF1 from 19W → 4W; RF2 from 2W → 0W).
3. Fine-tune RF1 load/tune:
   - Target reflected power <5W at recipe setpoint (e.g., 498W with 5W reflected).

**Step 4 – Conditioning and Qualification**

1. Run conditioning sequences:
   - ALTIC wafers (5–7 wafers typical).
   - PR wafers (3+ wafers) for PRC conditioning.
2. Execute qual recipes:
   - Slim etch rate (SLIM29, SLIM34).
   - N2O2_100S and other N2O2 variants if family is under test.
3. Evaluate:
   - B/A/D/ER metrics vs. spec.
   - RF/DC behavior during qual steps.

**Step 5 – Governance and Documentation**

1. If qual fails:
   - Keep affected recipe family down (N2O2, TMR).
   - Escalate to EE/MEVC; log detailed RF/MFC/etch data.
2. If qual passes:
   - Mark tool ready for qual/production for the validated recipe set.
   - Update wiki with new RF delay and MFC configuration baseline.

---

### 3.3 SOP – [[Slit Valve Issues]] / [[Pump Issues]] / [[Pressure Out of Compliance]]

**Trigger:** Slit valve open timeout, failure to transfer wafer, TM/LM pump-down issues, pressure out-of-compliance alarms.

**Step 1 – Wafer Status and Safety**

1. Identify wafer locations:
   - PM module, TM, LL cassette.
   - Record slot mapping (processed vs. unprocessed).
2. Avoid forced mechanical actions that risk wafer damage; prioritize controlled recovery.

**Step 2 – Vacuum Recovery**

1. Manually pump down TM and LM:
   - Use manual pump controls to reach target pressure (~40 mT).
2. Clean seals:
   - Wipe LL door o-ring and TM seals with acetone, then IPA.
   - Inspect for cracks or contamination.
3. Verify ion gauge:
   - If ion gauge fails to turn on, reboot system and re-enable gauge.

**Step 3 – Slit Valve Functional Check**

1. With TM at proper pressure, attempt slit valve operation:
   - Open PM2 slit valve manually; transfer wafer to/from PM.
   - Repeat sequence to confirm repeatability.
2. If slit valve fails due to high TM pressure:
   - Confirm pump performance; check for leaks.
   - Escalate to mechanical maintenance if valve actuation remains unreliable.

**Step 4 – Post-Recovery Testing**

1. Run dummy wafers:
   - Execute transfer cycles (LL → TM → PM → TM → LL) to validate slit valve and pump behavior.
2. Monitor:
   - No slit valve timeouts.
   - Stable pressure during transfers.

**Step 5 – Return to Production**

1. If transfer and pump behavior are stable:
   - RTP with caution; monitor first production lot closely.
2. If intermittent failures persist:
   - Log detailed pressure and valve actuation data.
   - Escalate for slit valve hardware inspection/replacement.

---

### 3.4 SOP – [[Chuck Seal Issues]] / [[Helium Took Too Long to Stabilize]] / [[Backside Issues]] / [[Scrath Issues]]

**Trigger:** Chuck seal alarms, He stabilization timeouts, backside contact/dragging, wafer scratches.

**Step 1 – Wafer Handling**

1. Abort affected wafer via alarm menu; return wafer to cassette if possible.
2. Mark suspect wafers for MEVC inspection (do not re-run until cleared).
3. Document slot and recipe for each chuck/He/backside alarm.

**Step 2 – Chuck / Clamp / Mechanical Inspection**

1. Vent PM as needed to access chuck/clamp.
2. Inspect:
   - Clamp plate for wear, coating, or mechanical damage.
   - Lift bellows and linear slide for leaks or misalignment.
   - Backside contact surfaces for contamination.
3. Replace hardware:
   - Clamp plate when scratches or seal issues are observed.
   - Lift bellows and linear slide if mechanical integrity is compromised.

**Step 3 – Robot and Backside Alignment**

1. Check robot arm Z-height:
   - Adjust Z to eliminate dragging (e.g., 0.366 → 0.346).
   - Apply same Z adjustment to both put and get operations.
2. Run transfer cycle tests:
   - Use clean dummy wafers.
   - Verify no backside dragging or misplacement.

**Step 4 – Helium Seal Verification**

1. Pump down PM; run dummy wafers with He seal monitoring.
2. Confirm:
   - He stabilization within allowed time.
   - No chuck seal alarms across multiple dummy runs.

**Step 5 – Burn-In and Qualification**

1. Perform chamber burn-in:
   - Run multiple dummy sets to stabilize chuck/He behavior.
2. Execute qual:
   - Slim etch rate or recipe-specific quals as required.
3. If all passes:
   - Return tool to production; update chuck/clamp configuration baseline.

---

### 3.5 SOP – [[Material or Wafer Was Not Detected]] / [[System Operating Issues]] / [[Software, PCS, ELOG Issues]]

**Trigger:** Wafer-not-detected alarms, mapping errors, keyboard/PCS/ELOG issues, system operating anomalies.

**Step 1 – Wafer Location Verification**

1. Physically verify wafer:
   - Check robot arm, TM, PM, and LL cassette.
2. Correct mapping:
   - If wafer is on arm or in TM but system reports missing, unload/reload wafer and update mapping.

**Step 2 – Mapping Sensor and Optics**

1. Inspect mapping sensor:
   - Check light sources (left/right), mirrors, prisms, and transmitters.
2. Replace defective components:
   - Swap weak light source with good one.
   - Replace cracked mirror and faulty transmitter.
3. Validate:
   - Run full cassette mapping test; confirm correct slot detection.

**Step 3 – System/PCS/ELOG Recovery**

1. Reboot PM2 computer and tool control software.
2. Replace faulty keyboard or HMI components.
3. For PCS/ELOG issues:
   - Perform D0 and qualification flow before resuming production.
   - Prepare SLIM and monitor wafers for post-reboot validation.

**Step 4 – Functional Test**

1. Home elevator and robot.
2. Map cassette; load/unload test wafer to PM and back.
3. Confirm:
   - No mapping errors.
   - No wafer-not-detected alarms.

**Step 5 – Documentation and Return to Manufacturing**

1. Log all replaced components and mapping test results.
2. Mark tool RTM once mapping and PCS/ELOG behavior are stable.

---

### 3.6 SOP – [[Recipe Issues]] / [[Qualification Failures]] / [[Others]]

**Trigger:** Recipe-specific alarms, explicit “do not run” directives, qualification failures, or engineering-only investigations.

**Step 1 – Immediate Recipe Governance**

1. When a recipe family (e.g., N2O2, TMR-FLTR-RIE, UZ1W) shows repeated alarms or qual failures:
   - Declare recipe family **down**.
   - EWAIV tool not to run that family until EE/MEVC clearance.
2. Restrict tool to **approved recipes**:
   - MPL1024, PMR_MIX2, PP3_ASH_6W_7M, UU9Q, and other recipes with recent clean quals.

**Step 2 – Engineering Investigation**

1. Collect data:
   - RF load/tune positions, reflected power, DC bias, etch metrics per step.
   - Chamber condition, MFC flows, RF delays.
2. Coordinate with EE/MEVC:
   - Request S/A for problematic recipes (e.g., MPL1024).
   - Adjust recipe parameters (RF power, delays, gas flows) under engineering control.
3. Run controlled test wafers:
   - Use dummy wafers first; then limited monitor wafers.
   - Do not run production wafers until recipe is re-qualified.

**Step 3 – Qualification and Release**

1. Execute full qual plan:
   - Slim etch rate, N2O2 qual, recipe-specific monitors.
2. If qual passes:
   - Update recipe status to “up”; document new baseline parameters.
3. If qual fails:
   - Keep recipe family down; continue engineering-only work.

**Step 4 – Wiki / MESA Documentation**

1. For each major recipe event:
   - Update cross-linked pages ([[Recipe Issues]], [[Etch Rate Issues]], [[RF Voltage Out of Compliance]]) with:
     - Date, recipe, failure mode, corrective actions, qual results.
2. Ensure production and maintenance teams reference latest recipe governance before scheduling lots on RIE03.

---

These SOPs should be treated as **living documents**. Any new RF hardware changes, recipe parameter updates, or qual methodologies must be reflected here and cross-linked to the relevant failure mode pages for RIE03.