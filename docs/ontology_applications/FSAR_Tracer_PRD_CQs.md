# Advice Trace Demo — UX & Interface Spec (FSAR Hero)

**Goal:** For one SMU, show a transparent, reproducible chain: **CU statuses → SMU aggregation → scientific advice → management decision → legal framework**. Optimized for managers (clarity) and analysts (evidence) with progressive disclosure starting from CU-level detail to high-level SMU aggregation and advice flow.

---

## 1) Personas → Stories → Acceptance

### Persona A — Executives / Directors / Branch & Division Managers

- **Goal:** Rapid assurance that the **evidence underpinning advice** is defensible, current, and **policy-ready**. Need to answer "Are we policy-ready and defensible today?" and "What changed since the last FSAR?"
- **Stories:** Select **SMU + Year** → see **Policy & Legal Readiness** panel with hard gates; **Evidence Completeness** gauge; **Delta since last FSAR** summary; **download Advice Trace Pack** for briefing/audit.
- **KPI Widgets:** Coverage (% SMUs with current FSAR), WSP status zone distribution, below-LRP triggers, evidence completeness (Complete / Gaps / Missing-Critical), timeliness (last update date)
- **Acceptance:** **Policy & Legal Readiness** panel (hard gate on "Ready"):
  - WSP status zone for the SMU (with explicit mapping to LRP/USR and how assessed this cycle)
  - Precautionary Approach compliance: harvest control rule named + parameterized, with source & version
  - Fisheries Act Fish Stocks provisions: below-LRP indicator (Yes/No), if Yes → Rebuilding Plan link + plan version/date
  - **Evidence Completeness** reports _Ready_ when all required evidence + policy gates pass; _Partial_ when optional items missing; _Blocked_ when required items missing
  - **Delta since last FSAR** (mandatory in Advice Trace Pack and on screen): Changed benchmarks, methods/code versions, data additions/removals, status zone, advice/rationale
  - **Export** downloads the pack with structured deltas vs. previous FSAR
  - **AC:** Exec sees a red "Policy trigger" chip whenever an SMU is below LRP and a Rebuilding Plan link is present

### Persona B — FSAR Lead Author

- **Goal:** Ensure narrative coherence, benchmark justification, proxy rationale, and reviewer response integration for submission-ready FSARs.
- **Responsibilities:** Narrative coherence, benchmark justification, proxy rationale, reviewer response integration
- **Stories:** Generate submission-ready trace packs with benchmarks, uncertainty notes, proxy decisions, and methods provenance; integrate reviewer feedback; ensure policy compliance.
- **Acceptance:** **AC:** Lead Author can generate a "submission-ready" trace pack with benchmarks, uncertainty notes, proxy decisions, and methods provenance in ≤2 clicks.

### Persona C — Reviewer / Stock Assessment Biologist

- **Goal:** Verify methods, benchmarks, reproducibility; confirm uncertainty handling and scientific rigor.
- **Stories:** Open **Method** → view parameters for both analytical and field methods (including field method downgrade criteria and Estimate Type Classification for specific SENs) + **exact code commit/tag/or dataset DOI**; inspect **Benchmarks** as first-class entities with derivation evidence; toggle **Uncertainty overlay** to confirm GSI/CI presence and propagation; review **CU inclusion/exclusion** transparency.
- **One-click panels for:** benchmark derivation (type, value, method, sensitivity flags), uncertainty treatment (CIs/probabilities), GSI usage (used?, n, misassignment/CI), and downgrade criteria used
- **Acceptance:** **Method** shows name/protocol/version/parameters + link to exact commit/tag/DOI used by figures/status. **Benchmarks** as explicit entities (dfo:LowerBenchmark, dfo:UpperBenchmark, dfo:TargetReference) with:
  - Derivation method, input dataset(s), time window, uncertainty method, and version/date
  - Back-calculable query (stored SPARQL and/or R script call) to regenerate the estimate
  - **Reference Points** include type/value/derivation + benchmark method; sensitivity flagged
  - **Uncertainty overlay** badges missing **GSI**, **sample sizes**, or **status CIs**; click reveals missing fields
  - **CU Accounting**: CU list for the SMU explicitly lists included, excluded, and proxied CUs with machine-readable justification; GSI usage (Yes/No), sample sizes, and assignment uncertainty
  - **Downgrade Criteria**: Display downgrade criteria (from SKOS scheme) and make violations/assumptions visible
  - **AC:** Reviewer can verify benchmark method & code version; GSI sample size & uncertainty are visible where relevant

### Persona D — Data Steward / FSAR Analyst Co-author

- **Goal:** Ensure data standards are met (terms, provenance, data quality, uncertainty); fail fast; identify missing metadata or poor data stewardship practices to help support FSAR authors meet best practices. Ship FSARs quickly. Upload draft data to check for compliance, completeness etc.
- **Stories:**
  - Start a new submission via a **Metadata Intake wizard**: select SMU + Year, fill required metadata using **controlled‑vocab dropdowns** sourced from SKOS, attach Excel/CSV.
  - Click **Validate** to run SHACL + R validator; see inline errors (row/column, severity, code, fix‑hint); correct and re‑validate until state = **Ready**.
  - Save/resume drafts; download a tailored **Excel template** for the selected scope (Population, CU, SMU, Indicator Stock, PFMA) pre‑filled with valid enumerations.
  - Open **Evidence Drawer** for provenance minimum and submission audit (who/when, validator versions).
- **Acceptance:**
  - **Validator gating:** "Ready" is blocked unless all required metadata are present: method registry term + version, benchmark derivation record, data coverage window, unit + scale, provenance (PROV-O), and person‑time stamps (who/when).
  - **Error contract:** Validation returns structured errors with severity (critical/optional), row/column/file, error code, message, and fix‑hint; non‑zero on critical errors; zero only when Ready.
  - **Controlled‑vocab** enforcement for `spawner_origin`, `data_source_type`, `reference_point_type`, `downgrade_criterion` via SKOS schemes in `graph:vocab`; off‑list values rejected with friendly messages.
  - **Provenance minimum** is visible at the top of the submission and in the Evidence Drawer: `data_source`, `method`, `code_version/hash`, `reviewer`, `date`.
  - **Schema alignment**: SPSR fields align with validator and FSAR reporting (explicit LRP/USR/TR records, status decision + rationale, CI fields).
  - **Submission lifecycle:** Draft → Validated → Ready → Ingested, with audit events (who/when/tool versions). Human review and approval required before ingestion.

## 1b) User Stories & Acceptance Criteria (Reflect Real FSAR Concerns)

### Benchmark Transparency (Core)

**Story:** As a Reviewer, I need to verify that all reference points have transparent derivation methods and sensitivity flags.

**Acceptance Criteria:**
- Add controlled vocab for `reference_point_type` (e.g., LRP/USR/Sgen/Smsy) and `benchmark_method`
- **AC:** Benchmarks must display type, value, method, sensitivity flags, and link to method/code provenance

### Data Gaps & Proxies (CU Accounting)

**Story:** As a Lead Author, I need to document CU inclusion decisions and proxy justifications with reviewer sign-off.

**Acceptance Criteria:**
- Add a CU inclusion/proxy table with fields: `decision` (included/excluded/proxied), `justification`, `reviewer`, `review_date`
- **AC:** Any CU ≠ "included" requires justification + reviewer sign-off or it fails validation (flagged Missing-Critical)

### Mixed-Stock Risk (GSI)

**Story:** As a Reviewer, I need to assess GSI usage and assignment uncertainty for mixed-stock fisheries.

**Acceptance Criteria:**
- Add fields: `gsiUsed` (bool), `gsiSampleSize` (int), `gsiAssignmentUncertainty` (text/CI or % misID), `baseline_reference`
- **AC:** If stock is mixed-fishery AND `gsiUsed` = false → show risk chip ("No GSI apportionment") and require rationale

### Uncertainty Handling

**Story:** As a Reviewer, I need to verify that key estimates include confidence intervals or documented rationale for absence.

**Acceptance Criteria:**
- Add `status_confidence` (probabilities/CI) and `downgradeReason` (controlled list) for quality-downgraded inputs
- **AC:** Key estimates must include CI or flagged rationale for absence; status shows P(Green/Amber/Red) or a CI note

### Policy Gates & Legal Readiness

**Story:** As an Executive, I need to ensure compliance with Fisheries Act Fish Stocks provisions and rebuilding requirements.

**Acceptance Criteria:**
- Add explicit checks: `belowLRP` (bool), `RebuildingPlanURL`, `hcrIdentifier`/`hcrParameters`
- **AC:** `belowLRP` = true requires a valid Rebuilding Plan link or shows Missing-Critical

## 2) UI/UX Inspiration

**Single page** flow focused on clarity and drill‑downs. The page is split into a left **Advice Trace** and a right **Evidence Drawer**.

### 2.1 Visual Flow

- **Header bar:** SMU + Year picker (Barkley Sockeye • 2025), Export.
- **Advice Trace Flow (hierarchical multi-branch tree, left-to-right with progressive disclosure):**
  
  **Level 0 (Initial View):**
  ```
  [CU₁] ┐
  [CU₂] ├─→ [SMU] → [Advice]
  [CU₃] ┘
  ```
  - **CU nodes**: Each shows CU name, status zone (color-coded: Red/Amber/Green), Evidence badge
  - **SMU node**: Shows SMU name, year, aggregated status zone (color-coded: Red/Amber/Green), Evidence badge
  - **Advice node**: Shows FSAR title, year, Evidence badge, Documents quick links (FSAR/Research/Tech Report)  

  **Level 1 (Click SMU - Reveals SMU Details):**
  ```
  [CU₁] ┐
  [CU₂] ├─→ [SMU + Methods/Benchmarks] → [Advice]
  [CU₃] ┘
  ```
  - **SMU expanded**: Shows aggregation methods, LRP calculation, USR, status derivation
  - **Status color rule**: SMU color = worst-case of CU colors (any Red → Red; else any Amber → Amber; else Green)
  
  **Level 2 (Click CU - Reveals CU Details):**
  ```
  [CU₁ + Data/Methods/Benchmarks] → [SMU] → [Advice]
  ```
  - **CU expanded**: Shows:
    - Data sources (escapement measurements, GSI, proxies with justifications)
    - Methods (enumeration methods, estimate methods, code commits/DOIs)
    - Benchmarks (Lower Benchmark, Upper Benchmark with derivation methods)
    - Quality indicators (estimate type, downgrade criteria, uncertainty measures)
  
  **Level 2 (Click Advice - Reveals Documents and Decisions):**
  ```
  [CU₁] ┐
  [CU₂] ├─→ [SMU] → [Advice + FSAR/Research Docs] → [Management Decision] → [Legal Framework]
  [CU₃] ┘
  ```
  - **Advice expanded**: Shows:
    - Documents quick links (FSAR/Research/Tech Report buttons)
    - FSAR document (title, doc number, year, DOI, download link)
    - Research Documents (precursors, with titles, doc numbers, DOIs)
    - Technical Reports
    - Advice text, reviewer, review date, version
    - **Management Decision sub-node**: Shows decision type, date, decision maker (branch or division), rationale, supporting advice
    - **Legal Framework sub-node**: Shows framework name, relevant sections, requirements, compliance status

- **Evidence Drawer (right slide‑over):** Tabs **Data • Methods • Benchmarks • Uncertainty • Policy/Legal • Changes**. Always shows **provenance minimum** (source, method, code commit, reviewer/date) at the top.
  - **Data tab:** Input datasets, data sources, coverage windows, units/scales, QC status
  - **Methods tab:** Method registry terms, versions, parameters, code commits/DOIs, reproducibility links
  - **Benchmarks tab:** LRP/USR/TR entities with derivation evidence, uncertainty methods, regeneration queries
  - **Uncertainty tab:** Status intervals, GSI sample sizes, assignment uncertainty, downgrade criteria
  - **Policy/Legal tab:** WSP zone mapping, HCR parameters, Fisheries Act triggers, rebuilding plan links
  - **Changes tab:** Delta vs. last FSAR (data, methods, benchmarks, status, advice, rationale)
  - **Documents tab:** Lists linked artifacts with icon, title, doc number, year, size; actions: **Open**, **Download**, **Copy citation**.
- **Top ribbon:** Readiness pill (Ready / Partial / Blocked) + "Why not Ready?" popover with specific missing items
- **Always show:** Last FSAR vs This Cycle mini-diff
- **Export button:** Packages the **Advice Trace Pack** (versioned JSON-LD bundle with structured deltas vs. previous FSAR, figures, summary pdf of advice trace node metadata). Includes a **/docs/** subfolder with cached PDFs if allowed and an optional /data/ folder if toggled.

This will be an interactive hierarchical tree style graph with progressive disclosure. The initial view shows all CUs for the selected SMU flowing to the SMU and then to Advice, with Management Decision and Legal Framework appearing as sub-nodes when Advice is expanded. Clicking any node reveals additional nodes and specific details in the Evidence Drawer. We need rich relationships (e.g., multiple datasets feeding multiple methods) and should use a **node‑link view** with a toggle for specific profiles for Biologist/Scientist, Data Steward/Custodian, and Executive/Director which shows different levels of details depending on their persona. Use Cytoscape.js or D3 or other custom javascript as needed.

### 2.2 Purpose of UI Elements

- **Evidence badges:** Summarize **evidence presence/quality** for the decision context at each node:\
  **Complete** = all required evidence present; **Gaps** = optional elements missing; **Missing‑Critical** = required evidence missing. These roll up SHACL/validator results and CQ checks. _(Does not imply review approval.)_
- **Risk chips:** Compact flags tied to specific CQs (e.g., _proxy justification missing_, _no status CI_). Clicking a chip focuses the Drawer on the missing field(s).
- **Evidence Drawer:** The audit lens—shows the _who/what/when/how_ for the selected node: datasets, parameters, reference‑point derivations, code commit, reviewer/date, and links to figures or repos.
- **Documents:** Surface authoritative downloads (FSAR, Technical Reports, Research Documents). Each item shows **doc type**, **title**, **doc number/identifier**, **issued date**, **version**, **size**, and a **canonical URL/DOI**; if internal, use a **pre‑signed URL**. A small badge indicates **Public** or **Internal**.
- **Currency tab:** Shows last‑updated and version pins per component; highlights stale items with thresholds (e.g., >12 months).
- **Drill‑down:** From Drawer items (e.g., a dataset row, code commit, or document), jump to the source in SPSR (record view), GRD (run/sample), CSAS/DFO publications page, or GitHub (exact commit/tag) or Zenodo Release. Breadcrumbs let you pop back to the node.

### 2.4 Metadata Intake (Data Steward Mode)

- **Header (Intake mode):** "Start New Submission" with SMU + Year selectors.
- **Step 1 — Metadata form:** Controlled‑vocab dropdowns for `spawner_origin`, `data_source_type`, `reference_point_type`, `downgrade_criterion` (SKOS in `graph:vocab`); provenance minimum fields pinned.
- **Step 2 — Attach files:** Upload `.xlsx` (current accepted format). Parse Metadata tab first; show a preview of parsed metadata fields.
- **Step 3 — Validate:** Run SHACL + R validator; render inline errors (severity, row/col, code, fix‑hint). Provide "Re‑run validation" and "Download error report".
- **Step 4 — Ready & Submit:** When no critical errors remain, mark **Ready**. Submissions require human review/approval before ingest to SPSR.
- **Utilities:** "Download tailored template" endpoint pre‑seeds enumerations and column headers by scope (Population, CU, SMU, Indicator Stock, PFMA); "Save draft" persists current progress.

## 2c) Usability & Data Input Workflow (Reduce Friction, Increase Trust)

### Excel + R/SHACL Validator Enhancements

**Story:** As a Data Steward, I need targeted error reporting with fix-hints to resolve validation issues efficiently.

**Acceptance Criteria:**
- Add row/column targeted errors with fix-hints, and mark error severity (Critical/High/Info)
- Provide template tabs for read-only vocab sheets (RP types, methods, status zones) powering data validation dropdowns
- **AC:** Authors resolve all Critical errors locally; validator returns 0 Critical before upload is permitted

### Import Wizard in the Web UI

**Story:** As a Data Steward, I need guided upload with preview and validation feedback to ensure data quality.

**Acceptance Criteria:**
- Add guided upload: preview parsed rows, validation report inline, diff vs last submission, idempotent re-upload
- **AC:** Users can correct flagged fields in-app or re-upload; system preserves stable IDs for re-uploads

### Evidence Drawer Quality of Life

**Story:** As a Reviewer, I need quick access to all evidence links and citation information.

**Acceptance Criteria:**
- Add quick links to dataset DOI, code commit/DOI, method concept; copy citation button; peek of data dictionary fields
- **AC:** From any status tile, user can open drawer and reach all evidence links ≤2 clicks

### Risk Chips & Completeness Meter

**Story:** As an Executive, I need visual indicators of coverage and completeness at a glance.

**Acceptance Criteria:**
- Add filterable risk chips (e.g., Missing CI, No GSI, Proxy w/o review, Below LRP w/o plan)
- Add Evidence Completeness gauge per SMU (Complete / Gaps / Missing-Critical) and section-level mini-gauges
- **AC:** Executive sees coverage and completeness at a glance; Reviewer filters by risk type to accelerate audits

### Controlled Vocab Pickers + "Suggest Term" Flow

**Story:** As a Data Steward, I need flexible vocab management that doesn't block workflow when new terms are needed.

**Acceptance Criteria:**
- Add inline pickers for methods/benchmarks; Suggest a new term creates a temporary local mapping and queues curation
- **AC:** Off-list entries can't block; they're tracked and reconciled later (with audit trail)

### Iteration & Comparison

**Story:** As a Lead Author, I need to track changes between cycles and generate comparison reports.

**Acceptance Criteria:**
- Add change-log auto-generation (data/method/benchmark/status/advice) + cycle diff view
- **AC:** Lead Author can export a Change Summary page between cycles

### Accessibility & Presentation

**Story:** As a user with accessibility needs, I need the interface to be usable with assistive technologies and printable.

**Acceptance Criteria:**
- Add color-blind-safe status palette, keyboard navigation, structured headings, printable Advice Trace Pack
- **AC:** Trace Pack includes figures + evidence appendix with live links

### 2.3 Ontology Integration and Open Questions

**Data Product Ontology Integration:**

- **Question:** How should we integrate the [Data Product Ontology (DPROD)](https://ekgf.github.io/dprod/) to handle dataset management instead of using generic `Dataset` classes?
- **Investigation needed:** Map existing DFO Salmon Ontology classes to DPROD's `DataProduct`, `DataService`, `Distribution`, and `Dataset` classes for standardized data product representation.

**Core Entity Questions (Requiring Investigation):**

- **Data Products:** How should we model data products using DPROD vs. existing `dfo:EscapementMeasurement` hierarchy?
- **Analysis Processes:** Should we replace `dfo:GSIRun` with `dfo:AnalysisRun` to better represent genetic analysis processes?
- **Scientific Outputs:** What is the most appropriate term for scientific advice/recommendations? (Investigate DFO CSAS terminology)
- **Decision Support:** Is `DecisionContext` the right term, or would `Decision` be sufficient for management decision support?
- **SIL/SEN Integration:** How should we align with Minh Doan's PR for Stream Inspection Logs (SIL) and Escapement Narratives (SEN) terms?

**Relations (PROV‑O flavored):** `StatusAssessment used DataProduct/ReferencePoint`, `StatusAssessment wasGeneratedBy Method`, `ScientificOutput wasDerivedFrom StatusAssessment`, `ScientificOutput supports Decision`, `Figure wasDerivedFrom {DataProduct,Method}`.

**WSP Rapid-Status Support:**

The ontology now supports WSP rapid-status assessments via `fsar:WSPMetric`, `fsar:MetricBenchmark`, and `fsar:AlgorithmThreshold` classes. The `dfo:StockAssessment` class links to WSP metrics via `fsar:assessesMetric`, and produces rapid statuses via `fsar:producesRapidStatus` with confidence categories via `fsar:hasConfidence`. Decision requirement patterns from v3 (e.g., `fsar:RebuildingPlanRequirement`) work with WSP trigger conditions linking metric positions to policy obligations.

---

### 2f. WSP Rapid-Status Support

The FSAR Tracer now supports WSP rapid-status assessments through integration with the Learning Tree 3 decision-tree algorithm. This support enables tracking of the four standard WSP metrics, their benchmarks and algorithm thresholds, rapid status assignments, and confidence categories.

**Four Standard WSP Metrics:**

1. **Absolute Abundance**: Compares generational average spawner abundance to COSEWIC criterion D1 thresholds. Lower benchmark: 1,000 spawners; Upper benchmark: 10,000 spawners.
2. **Relative Abundance**: Compares generational average spawner abundance to CU-specific benchmarks (typically Sgen lower, 80% SMSY upper, or habitat capacity-based).
3. **Long-Term Trend**: Compares current generational average to long-term average spawner abundance. Lower benchmark: 50% of long-term average; Upper benchmark: 75% of long-term average.
4. **Percent Change**: Quantifies linear change in spawner abundance over the most recent three generations. Lower benchmark: -25%; Upper benchmark: -15%.

**Learning Tree 3 Decision-Tree Integration:**

The Learning Tree 3 algorithm assigns rapid statuses (Red, Amber, Green) based on metric values and availability. The algorithm uses threshold values that differ from metric benchmarks by design, incorporating buffers and precautionary adjustments based on expert processes and CART analyses.

**Metric Benchmarks vs. Algorithm Thresholds:**

Algorithm thresholds intentionally diverge from benchmarks in several places:

- **Absolute Abundance**: Benchmark lower threshold is 1,000 spawners (COSEWIC criterion D1), but Learning Tree 3 algorithm uses 1,500 (benchmark plus 500 buffer) to account for uncertainty and how experts treated individual years in generational averages.
- **Relative Abundance**: Upper benchmark threshold in Learning Tree 3 equals the WSP upper benchmark plus 10% buffer to account for how this metric was treated in WSP integrated status processes.
- **Long-Term Trend**: Benchmark thresholds are 50% (lower) and 75% (upper), but Learning Tree 3 uses 79% (lower) and 233% (upper). These thresholds emerged from CART analyses and are applied conditionally with other metrics.
- **Percent Change**: Benchmark lower threshold is -25%, but Learning Tree 3 uses -70% (emerged from CART analyses). This threshold is only applied conditionally when long-term trend >= 79% and absolute abundance >= 10,000.

**Confidence Category Output:**

Each rapid status assessment includes a confidence category (High, Medium, or Low):

- **High confidence**: Status assigned using absolute abundance or relative abundance metrics (both requiring higher quality data and benchmarks).
- **Medium confidence**: Status based on long-term trend metrics with some abundance information available.
- **Low confidence**: Status based on trend metrics alone without abundance benchmarks.

These confidence ratings are derived from the algorithm branch (node) that determines the status, based on metric availability and data types used.

**Decision Requirements:**

WSP metric positions trigger decision requirements through `fsar:Condition` patterns that link to `fsar:DecisionRequirement` classes. For example, when rapid status is Red (below LRP), this triggers rebuilding plan requirements mandated by the Fisheries Act Fish Stocks Provisions.

---

## 2d) Global Acceptance Criteria

**A1. Benchmarks:** Each SMU year must include at least one LRP and one USR entity with derivation metadata (method, inputs, time window), version/DOI or commit, and an executable regeneration link (stored query or code pointer). Benchmarks must display type, value, method, sensitivity flags, and link to method/code provenance.

**A2. Uncertainty:** Status decision must include interval or categorical uncertainty; where estimates are downgraded, the downgrade criterion (from SKOS scheme) is recorded and shown. Key estimates must include CI or flagged rationale for absence; status shows P(Green/Amber/Red) or a CI note.

**A3. Policy & Legal Readiness:** "Ready" requires: WSP zone computed and justified; named Harvest Control Rule with parameters and version; Fisheries Act Fish Stocks check (below-LRP flag) and, if true, link to Rebuilding Plan. `belowLRP` = true requires a valid Rebuilding Plan link or shows Missing-Critical.

**A4. Change Log:** Advice Trace Pack must include structured deltas vs. previous FSAR: data, methods, benchmarks, status, advice, rationale. Lead Author can export a Change Summary page between cycles.

**A5. CU Accounting:** CU list for the SMU must explicitly list included, excluded, and proxied CUs with machine-readable justification; GSI usage (Yes/No), sample sizes, and assignment uncertainty. Any CU ≠ "included" requires justification + reviewer sign-off or it fails validation (flagged Missing-Critical).

**A6. Intake & Validation:** Controlled‑vocab fields are enforced via SKOS; SHACL + R validator must pass all critical checks before a submission becomes "Ready". Validation returns structured errors (severity, row/col, code, fix‑hint). Submission lifecycle is Draft → Validated → Ready → Ingested, with audit events and human approval before ingestion. Authors resolve all Critical errors locally; validator returns 0 Critical before upload is permitted.

**A7. GSI Risk Assessment:** If stock is mixed-fishery AND `gsiUsed` = false → show risk chip ("No GSI apportionment") and require rationale. GSI usage fields must include `gsiUsed` (bool), `gsiSampleSize` (int), `gsiAssignmentUncertainty` (text/CI or % misID), `baseline_reference`.

**A8. Executive KPIs:** Exec sees coverage and completeness at a glance; Reviewer filters by risk type to accelerate audits. Exec sees a red "Policy trigger" chip whenever an SMU is below LRP and a Rebuilding Plan link is present.

**A9. Lead Author Workflow:** Lead Author can generate a "submission-ready" trace pack with benchmarks, uncertainty notes, proxy decisions, and methods provenance in ≤2 clicks.

**A10. Reviewer Verification:** Reviewer can verify benchmark method & code version; GSI sample size & uncertainty are visible where relevant. From any status tile, user can open drawer and reach all evidence links ≤2 clicks.

---

## 2e) Architecture Pattern & SPSR (Django) Integration

**Context:** SPSR is a **layered monolith** today (Presentation → Application → Domain → Infrastructure). The Advice Trace should respect that layering, add a thin ontology/graph layer, and keep a clean **contract** between SPSR data and the trace UI.

### Recommended Design Pattern

**"Layered Monolith + Contract + Graph Sidecar"**

- **Presentation (Django)**: Pages/templates (HTMX/Alpine) render the **CU-first Advice Trace** flow and open the **Evidence Drawer**.
- **Application Services (Django)**: `AdviceTraceService` orchestrates pulls from SPSR, GRD, and the graph, assembles **DTOs** for the CU → SMU → Advice flow, and exposes a **DRF endpoint** returning **JSON‑LD**.
- **Domain (SPSR)**: Your existing models; add a small **anti‑corruption layer (ACL)** that maps SPSR terms/fields → ontology terms (SKOS/JSON‑LD context) without polluting domain models.
- **Infrastructure**:
  - **Graph sidecar** = **Jena Fuseki** (Docker) + SPARQL. It’s not embedded into SPSR; it sits alongside and is queried by the application service.
  - **Validators** (R + SHACL) run in CI or as a Django management command, writing results (pass/fail, messages) back to the AdviceTraceService cache.

```
Browser ──(HTMX)──▶ Django Templates
   ▲                     │
   │                 AdviceTraceService (App layer)
   │                 │        │
   │       SPSR ORM (Domain)  │ SPARQL Adapter ◀── Fuseki (Graph)
   │                 │        │
   │                 └── DRF JSON‑LD Endpoint (/api/advice-trace/{smu}/{year})
```

### Why this fits a layered monolith

- **Separation of concerns:** SPSR logic stays in the monolith; ontology mapping lives in the ACL; graph queries in a small adapter.
- **Low coupling:** The UI consumes a **JSON‑LD contract**, not raw models. You can refactor SPSR internals later without breaking the UI.
- **Incremental adoption:** Start with Barkley only; add more SMUs by adding exports + shapes, not rewriting UI.

**Build the front end directly in SPSR** (Django templates + HTMX/Alpine). Keep the **JSON‑LD contract** so the UI remains decoupled and you can still export/share. Use Quarto only for **documentation** or publishing the Advice Trace Pack as a static companion, not as the primary UI.

### Integration Strategy (phased)

1. **POC (Weeks 1–8)** — _Django‑native_
   - Add `/api/advice-trace/{smu}/{year}` (DRF) returning JSON‑LD for CU → SMU → Advice flow.
   - Add `/advice-trace/?smu=…&year=…` Django view rendering the CU-first hierarchical flow (HTMX partials for Drawer).
   - Stand up **Fuseki** in Docker; connect via a tiny **SPARQL adapter** (e.g., `SPARQLWrapper`).
   - Compute **Badges** server‑side (combine SHACL results + SPARQL CQ results) → render as HTMX fragments.
2. **Hardening**
   - Cache SPARQL results (Django cache) per SMU/Year; invalidate on data refresh.
   - Move JSON‑LD generation to a scheduled management command; publish to S3/bucket for archival.
3. **Optional external publishing**
   - Generate a Quarto **static site** that reads the same JSON‑LD + figures for external stakeholders; link it from SPSR.

### Concrete Touchpoints (Django)

- **Endpoints**
  - `GET /api/advice-trace/{smu}/{year}` → JSON‑LD (CU → SMU → Advice trace)
  - `GET /api/documents?smu=&year=` → PDFs/links metadata (accessible via Advice node)
  - `GET /api/cq/{smu}/{year}` → CQ results used by badges (optional; or compute inline)
  - `GET /advice-trace/intake` → Intake UI page (HTMX) for Persona C
  - `GET /api/intake/vocab?scheme=reference_point_type` → SKOS options (label, IRI, notation)
  - `POST /api/intake/validate` → Run SHACL + R; returns normalized error payload
  - `POST /api/intake/submit` → Mark as Ready, queue for human review/ingestion
  - `GET /api/intake/submissions` → List/filter drafts by user/state
  - `GET /api/intake/template?scope=SMU&smu=&year=` → Tailored XLSX template download
- **Adapters**
  - **SPARQL adapter**: small class wrapping query files (Q1–Q8); returns rows → DTOs
  - **ACL mappers**: SPSR models → ontology JSON‑LD (via `rdflib` or hand‑rolled JSON)
- **Validators**
  - `python manage.py run_shacl` (pySHACL) against shapes; persist results for badge rollups
  - `validate_spsr.R` in CI; post results to a table or cache
  - Investigation: R validator run mode (sync vs async) and error contract TBD; capture as decision in ADR/todo_list

### Libraries & Patterns (Django‑native)

- **UI:** HTMX, Alpine.js (no SPA); **Cytoscape.js** if/when node‑link needed
- **Graph:** `SPARQLWrapper` (Py) or `rdflib.plugins.sparql`
- **JSON‑LD:** `rdflib` or plain JSON with a context; keep a versioned `@context`
- **Caching:** `django‑redis` (per SMU/Year keyspace)
- **Testing:** pytest + snapshot tests for SPARQL responses; SHACL as CI gate
  - For intake: API contract tests for validator error payload; HTMX component tests for error rendering

### Where Badges, Drawer, and Drill‑downs live

- **Badges**: computed server‑side from SPARQL + SHACL; rendered as small HTMX fragments per CU/SMU/Advice node (so they can refresh without full page reload).
- **Evidence Drawer**: a Django partial that takes a node `id` and queries (via service) for provenance, parameters, documents, figures; deep‑links to SPSR record pages and CSAS/DFO docs.
- **Drill‑downs**: standard Django routes for SPSR records (dataset, method configs), GRD run/sample pages, and external doc links (new tab). HTMX keeps the experience snappy.
- **Documents**: accessible via Advice node expansion, showing FSAR/Research/Tech Report quick links and full document hierarchy.

### Migration/Scalability Notes

- If/when SPSR evolves toward services, the **JSON‑LD contract** and **SPARQL adapter** remain valid; you can swap the graph engine (e.g., Blazegraph, Neptune) without changing UI.
- The **anti‑corruption layer** keeps ontology terms from leaking into core domain models; rollouts are safer.

---

## 3) Minimum Viable Product (MVP) Definition

### 3.1 MVP Features (Essential for Initial Release)

**Core Functionality:**

- **Single SMU Focus:** Barkley Sockeye only for initial demonstration
- **Hierarchical Flow:** Progressive disclosure starting with all CUs → SMU → Advice, with Management Decision and Legal Framework as sub-nodes of Advice
- **Status Aggregation:** SMU status derived from constituent CU statuses using worst-case rule
- **Evidence Badges:** Complete/Gaps/Missing-Critical status indicators at CU, SMU, and Advice levels
- **Evidence Drawer:** Basic provenance display with source, method, code commit, reviewer/date
- **Document Hierarchy:** FSAR with precursor Research Documents
- **Export Functionality:** Basic Advice Trace Pack generation
- **Metadata Intake (Persona D):** Guided wizard to capture required metadata via controlled‑vocab dropdowns; attach `.xlsx`; validate and iterate until Ready
- **Benchmark Transparency:** Reference point types, methods, sensitivity flags with derivation evidence
- **CU Accounting:** Inclusion/exclusion/proxy decisions with justification and reviewer sign-off
- **GSI Risk Assessment:** Mixed-stock fishery risk chips and GSI usage tracking
- **Uncertainty Handling:** Status confidence intervals and downgrade reason tracking
- **Policy Gates:** Below-LRP triggers and rebuilding plan compliance checks
- **Risk Chips & Completeness Meter:** Visual indicators for coverage and completeness
- **Accessibility:** Color-blind-safe palette, keyboard navigation, printable trace packs

**Technical Requirements:**

- **Django HTMX Interface:** Single-page application with CU-first hierarchical flow and progressive disclosure
- **SPARQL Backend:** Core queries for CU-level, SMU-level, Advice-level evidence completeness, with Decision and Legal Framework as sub-queries
- **JSON-LD Contract:** Standardized data exchange format supporting CU → SMU → Advice → Decision/Legal Framework structure
- **Basic Validation:** SHACL shapes for status aggregation and evidence completeness
- **Validation Loop:** SHACL + R validator adapters with normalized error JSON (severity, row/col, code, fix‑hint); submission state machine persisted
- **Enhanced Error Reporting:** Row/column targeted errors with fix-hints, error severity (Critical/High/Info)
- **Template System:** Read-only vocab sheets powering data validation dropdowns
- **Risk Assessment Engine:** Mixed-stock fishery + GSI usage risk chip generation
- **Policy Compliance Engine:** Below-LRP trigger detection and rebuilding plan validation
- **Accessibility Features:** Color-blind-safe status palette, keyboard navigation, structured headings
- **Export Enhancement:** Printable Advice Trace Pack with figures and evidence appendix

### 3.2 Future Features (Post-MVP)

**Enhanced Functionality:**

- **Multi-SMU Support:** Expand beyond Barkley Sockeye with cross-SMU comparisons
- **Advanced Analytics:** Cross-cycle comparisons, trend analysis, status aggregation validation
- **Rich Visualizations:** Interactive CU-first hierarchical graphs, network views, status zone dashboards
- **Automated Classification:** SHACL-based estimate type assignment and status derivation
- **Integration APIs:** SPSR/GRD real-time data feeds with hierarchical data structure
- **Advanced Export:** Custom report generation, hierarchical data visualization packages

**Advanced Technical Features:**

- **Graph Database:** Full triple store implementation with advanced querying
- **Real-time Updates:** Live data currency monitoring
- **Advanced Validation:** Comprehensive data quality assessment
- **External Integrations:** CSAS document management, GitHub code linking

---

## 3b) Output Contract (Advice Trace Pack)

Ship a versioned JSON-LD bundle with:

- **dfo:StatusAssessment** (decision, uncertainty, inputs)
- **dfo:LowerBenchmark** / **dfo:UpperBenchmark** / **dfo:TargetReference** (as first-class entities with derivation evidence)
- **prov:wasGeneratedBy** links to code DOIs/commits and method registry terms
- **dfo:PolicyReadiness** node (WSP zone, HCR id+params, Fish Stocks trigger + rebuilding link)
- **dfo:ChangeLog** list of diffs vs last FSAR
- **dfo:CUAccounting** (included/excluded/proxied CUs with justification)
- **dfo:GSIUsage** (sample sizes, assignment uncertainty)

**Required Fields Checklist (v0.2)** `data_source_type`, `spawner_origin`, `proxy_justification`, `method_name`, `method_version`, `code_commit`, `reference_point_type`, `benchmark_method`, `benchmark_sensitivity`, `status_value`, `status_ci`, `gsi_sample_size/ci`, `gsiUsed`, `gsiAssignmentUncertainty`, `baseline_reference`, `status_confidence`, `downgradeReason`, `belowLRP`, `rebuildingPlanURL`, `hcrIdentifier`, `hcrParameters`, `scientific_output_text`, `reviewer`, `date`, `decision_id`, `policy_readiness_flags`, `change_log`.

---

## 4) Competency Questions — Advice Trace (Hierarchical Flow)

_(Each CQ backs a UI badge, drawer, or diff; fields listed must exist in data/template/SHACL. Questions marked with ⚠️ require ontology investigation.)_

### CU-Level Questions

**CQ-CU-1: What is the status of each Conservation Unit in an SMU?**
```sparql
SELECT ?cu ?cuLabel ?statusZone ?statusValue ?statusCI
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasMemberCU ?cu .
  ?cu rdfs:label ?cuLabel ;
      dfo:hasStatusAssessment ?assessment .
  ?assessment dfo:statusZone ?statusZone ;
              dfo:statusValue ?statusValue .
  OPTIONAL { ?assessment dfo:statusCI ?statusCI }
}
```

**CQ-CU-2: What data sources feed each CU's status assessment?**
```sparql
SELECT ?cu ?cuLabel ?dataSource ?dataType ?spawnerOrigin ?proxyJustification
WHERE {
  ?cu a dfo:ConservationUnit ;
      rdfs:label ?cuLabel ;
      dfo:hasStatusAssessment ?assessment .
  ?assessment prov:used ?dataSource .
  ?dataSource dfo:data_source_type ?dataType ;
              dfo:spawner_origin ?spawnerOrigin .
  OPTIONAL { ?dataSource dfo:proxy_justification ?proxyJustification }
}
```

**CQ-CU-3: What methods and benchmarks are used for each CU?**
```sparql
SELECT ?cu ?cuLabel ?method ?methodName ?lowerBenchmark ?upperBenchmark
WHERE {
  ?cu a dfo:ConservationUnit ;
      rdfs:label ?cuLabel ;
      dfo:hasStatusAssessment ?assessment .
  ?assessment prov:wasGeneratedBy ?method .
  ?method rdfs:label ?methodName .
  
  OPTIONAL {
    ?cu dfo:hasLowerBenchmark ?lb .
    ?lb dfo:benchmarkValue ?lowerBenchmark .
  }
  OPTIONAL {
    ?cu dfo:hasUpperBenchmark ?ub .
    ?ub dfo:benchmarkValue ?upperBenchmark .
  }
}
```

### SMU-Level Questions

**CQ-SMU-1: What is the SMU status and how does it derive from CU statuses?**
```sparql
SELECT ?smu ?smuStatus ?cu ?cuStatus
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasStatusAssessment ?smuAssessment ;
       dfo:hasMemberCU ?cu .
  ?smuAssessment dfo:statusZone ?smuStatus .
  ?cu dfo:hasStatusAssessment ?cuAssessment .
  ?cuAssessment dfo:statusZone ?cuStatus .
}
ORDER BY ?cuStatus
```

**CQ-SMU-2: What aggregation methods and reference points are used at the SMU level?**
```sparql
SELECT ?smu ?lrp ?lrpType ?lrpValue ?aggregationMethod
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasLimitReferencePoint ?lrp .
  ?lrp a dfo:CUStatusBasedLRP ;
       dfo:referencePointValue ?lrpValue ;
       prov:wasGeneratedBy ?aggregationMethod .
  ?aggregationMethod rdfs:label ?aggregationMethodLabel .
}
```

### Advice-Level Questions

**CQ-ADV-1: What scientific outputs (FSARs) exist for this SMU?**
```sparql
SELECT ?smu ?advice ?fsarTitle ?fsarYear ?fsarDOI ?researchDoc ?researchTitle
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasScientificOutput ?advice .
  ?advice dcterms:title ?fsarTitle ;
          dcterms:issued ?fsarYear .
  OPTIONAL { ?advice dcterms:identifier ?fsarDOI }
  OPTIONAL {
    ?advice dfo:hasPrecursorDocument ?researchDoc .
    ?researchDoc dcterms:title ?researchTitle .
  }
}
```

**CQ-ADV-2: What advice text and review information is available?**
```sparql
SELECT ?advice ?adviceText ?reviewer ?reviewDate ?version
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasScientificOutput ?advice .
  ?advice dfo:adviceText ?adviceText ;
          dfo:reviewer ?reviewer ;
          dfo:reviewDate ?reviewDate ;
          dfo:version ?version .
}
```

### Decision-Level Questions

**CQ-DEC-1: What management decisions are supported by this advice?**
```sparql
SELECT ?advice ?decision ?decisionType ?decisionDate ?decisionMaker
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasScientificOutput ?advice .
  ?advice dfo:supportsDecision ?decision .
  ?decision dfo:decisionType ?decisionType ;
            dfo:decisionDate ?decisionDate ;
            dfo:decisionMaker ?decisionMaker .
}
```

**CQ-DEC-2: What legal framework mandates this decision?**
```sparql
SELECT ?decision ?framework ?frameworkName ?relevantSections
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasScientificOutput ?advice .
  ?advice dfo:supportsDecision ?decision .
  ?decision dfo:requiredBy ?framework .
  ?framework rdfs:label ?frameworkName ;
             dfo:relevantSections ?relevantSections .
}
```

### Policy & Legal Questions

**CQ-POL-1: What is the WSP status zone and how was it derived from benchmarks?**
```sparql
SELECT ?smu ?wspZone ?lrp ?usr ?statusDecision ?hcrUsed
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasStatusAssessment ?assessment ;
       dfo:hasLimitReferencePoint ?lrp ;
       dfo:hasUpperStockReference ?usr .
  ?assessment dfo:statusZone ?wspZone ;
              dfo:statusDecision ?statusDecision ;
              dfo:harvestControlRule ?hcrUsed .
}
```

**CQ-POL-2: What Fisheries Act Fish Stocks provisions apply to this SMU?**
```sparql
SELECT ?smu ?belowLRP ?rebuildingPlan ?planVersion ?planDate
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasPolicyReadiness ?policy .
  ?policy dfo:belowLRP ?belowLRP .
  OPTIONAL {
    ?policy dfo:rebuildingPlan ?rebuildingPlan .
    ?rebuildingPlan dfo:version ?planVersion ;
                    dfo:issued ?planDate .
  }
}
```

### Change Intelligence Questions

**CQ-CHG-1: What changed since the last FSAR cycle?**
```sparql
SELECT ?smu ?currentCycle ?previousCycle ?dataChanges ?methodChanges ?benchmarkChanges ?statusChanges
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasChangeLog ?changeLog .
  ?changeLog dfo:currentCycle ?currentCycle ;
             dfo:previousCycle ?previousCycle ;
             dfo:dataChanges ?dataChanges ;
             dfo:methodChanges ?methodChanges ;
             dfo:benchmarkChanges ?benchmarkChanges ;
             dfo:statusChanges ?statusChanges .
}
```

### CU Accounting Questions

**CQ-CU-ACCT-1: Which CUs are included, excluded, or proxied in this SMU assessment?**
```sparql
SELECT ?smu ?cu ?inclusionStatus ?justification ?reviewer ?reviewDate
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasCUAccounting ?accounting .
  ?accounting dfo:cuInclusion ?cu ;
              dfo:inclusionStatus ?inclusionStatus ;
              dfo:justification ?justification ;
              dfo:reviewer ?reviewer ;
              dfo:reviewDate ?reviewDate .
}
```

**CQ-CU-ACCT-2: What GSI usage and uncertainty information is available?**
```sparql
SELECT ?smu ?gsiUsed ?sampleSize ?assignmentUncertainty ?gsiMethod
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasGSIUsage ?gsiUsage .
  ?gsiUsage dfo:gsiUsed ?gsiUsed ;
            dfo:sampleSize ?sampleSize ;
            dfo:assignmentUncertainty ?assignmentUncertainty ;
            dfo:gsiMethod ?gsiMethod .
}
```

### Benchmark Transparency Questions

**CQ-BENCH-1: What benchmark types and methods are used for each reference point?**
```sparql
SELECT ?rp ?rpType ?benchMethod ?sensitivity ?derivationMethod ?codeCommit
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasLimitReferencePoint ?rp .
  ?rp dfo:reference_point_type ?rpType ;
      dfo:benchmark_method ?benchMethod ;
      prov:wasGeneratedBy ?derivationMethod .
  ?derivationMethod dfo:code_commit ?codeCommit .
  OPTIONAL { ?rp dfo:benchmark_sensitivity ?sensitivity }
}
```

**CQ-BENCH-2: What are the sensitivity flags and derivation evidence for each benchmark?**
```sparql
SELECT ?rp ?sensitivity ?inputDataset ?timeWindow ?uncertaintyMethod ?version
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasLimitReferencePoint ?rp .
  ?rp dfo:benchmark_sensitivity ?sensitivity ;
      prov:used ?inputDataset ;
      dfo:time_window ?timeWindow ;
      dfo:uncertainty_method ?uncertaintyMethod ;
      dfo:version ?version .
}
```

### CU Proxy and Risk Questions

**CQ-CU-PROXY-1: Which CUs are proxied and what is the justification?**
```sparql
SELECT ?cu ?inclusionStatus ?justification ?reviewer ?reviewDate ?riskLevel
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasCUAccounting ?accounting .
  ?accounting dfo:cuInclusion ?cu ;
              dfo:inclusionStatus ?inclusionStatus ;
              dfo:justification ?justification ;
              dfo:reviewer ?reviewer ;
              dfo:reviewDate ?reviewDate .
  BIND(IF(?inclusionStatus != "included", "High", "Low") AS ?riskLevel)
}
```

**CQ-GSI-RISK-1: What is the GSI usage and assignment uncertainty for mixed-stock fisheries?**
```sparql
SELECT ?smu ?gsiUsed ?sampleSize ?assignmentUncertainty ?baselineReference ?riskChip
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasGSIUsage ?gsiUsage ;
       dfo:fisheryType "mixed-stock" .
  ?gsiUsage dfo:gsiUsed ?gsiUsed ;
            dfo:sampleSize ?sampleSize ;
            dfo:assignmentUncertainty ?assignmentUncertainty ;
            dfo:baseline_reference ?baselineReference .
  BIND(IF(?gsiUsed = false, "No GSI apportionment", "GSI Available") AS ?riskChip)
}
```

### Uncertainty and Quality Questions

**CQ-UNCERTAINTY-1: What uncertainty measures are available for status assessments?**
```sparql
SELECT ?assessment ?statusConfidence ?downgradeReason ?ciLower ?ciUpper ?probabilityGreen ?probabilityAmber ?probabilityRed
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasStatusAssessment ?assessment .
  ?assessment dfo:status_confidence ?statusConfidence .
  OPTIONAL { ?assessment dfo:downgradeReason ?downgradeReason }
  OPTIONAL { ?assessment dfo:ciLower ?ciLower ; dfo:ciUpper ?ciUpper }
  OPTIONAL { 
    ?assessment dfo:probabilityGreen ?probabilityGreen ;
                dfo:probabilityAmber ?probabilityAmber ;
                dfo:probabilityRed ?probabilityRed
  }
}
```

**CQ-UNCERTAINTY-2: Which estimates are missing confidence intervals or have downgrade reasons?**
```sparql
SELECT ?estimate ?estimateType ?missingCI ?downgradeReason ?qualityFlag
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasStatusAssessment ?assessment .
  ?assessment prov:used ?estimate .
  ?estimate dfo:estimate_type ?estimateType .
  BIND(NOT EXISTS { ?estimate dfo:confidenceInterval ?ci } AS ?missingCI)
  OPTIONAL { ?estimate dfo:downgradeReason ?downgradeReason }
  BIND(IF(?missingCI = true || BOUND(?downgradeReason), "Quality Concern", "Good") AS ?qualityFlag)
}
```

### Policy and Legal Compliance Questions

**CQ-POLICY-1: What policy triggers and legal requirements apply to this SMU?**
```sparql
SELECT ?smu ?belowLRP ?rebuildingPlanURL ?hcrIdentifier ?hcrParameters ?policyTrigger ?complianceStatus
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasPolicyReadiness ?policy .
  ?policy dfo:belowLRP ?belowLRP ;
          dfo:hcrIdentifier ?hcrIdentifier ;
          dfo:hcrParameters ?hcrParameters .
  OPTIONAL { ?policy dfo:rebuildingPlanURL ?rebuildingPlanURL }
  BIND(IF(?belowLRP = true && BOUND(?rebuildingPlanURL), "Compliant", "Policy Trigger") AS ?policyTrigger)
  BIND(IF(?belowLRP = true && !BOUND(?rebuildingPlanURL), "Missing-Critical", "Ready") AS ?complianceStatus)
}
```

### Cross-Cutting Questions

**CQ-TRACE-1: What is the complete evidence chain from CU data to management decision?**
```sparql
SELECT ?cu ?cuData ?cuMethod ?cuStatus ?smuStatus ?advice ?decision ?framework
WHERE {
  ?smu a dfo:StockManagementUnit ;
       rdfs:label "Barkley Sockeye"@en ;
       dfo:hasMemberCU ?cu ;
       dfo:hasStatusAssessment ?smuAssessment ;
       dfo:hasScientificOutput ?advice .

  ?cu dfo:hasStatusAssessment ?cuAssessment .
  ?cuAssessment prov:used ?cuData ;
                prov:wasGeneratedBy ?cuMethod ;
                dfo:statusZone ?cuStatus .

  ?smuAssessment dfo:statusZone ?smuStatus .

  ?advice dfo:supportsDecision ?decision .
  ?decision dfo:requiredBy ?framework .
}
```

**Required Fields Checklist (v0.2)** `data_source_type`, `spawner_origin`, `proxy_justification`, `method_name`, `method_version`, `code_commit`, `reference_point_type`, `benchmark_method`, `benchmark_sensitivity`, `status_value`, `status_ci`, `gsi_sample_size/ci`, `gsiUsed`, `gsiAssignmentUncertainty`, `baseline_reference`, `status_confidence`, `downgradeReason`, `belowLRP`, `rebuildingPlanURL`, `hcrIdentifier`, `hcrParameters`, `scientific_output_text`, `reviewer`, `date`, `decision_id`, `policy_readiness_flags`, `change_log`.

### WSP Rapid-Status Questions

**CQ-WSP-1: What are the metric benchmark values vs algorithm threshold values for each WSP metric?**

```sparql
SELECT ?metric ?metricLabel ?benchmarkType ?benchmarkValue ?benchmarkUnits ?thresholdValue ?thresholdUnits ?thresholdNote
WHERE {
  ?assessment a dfo:StockAssessment ;
              fsar:assessesMetric ?metric .
  ?metric rdfs:label ?metricLabel ;
          fsar:hasBenchmark ?benchmark ;
          fsar:hasAlgorithmThreshold ?threshold .
  ?benchmark rdfs:label ?benchmarkType ;
             fsar:numericValue ?benchmarkValue ;
             fsar:units ?benchmarkUnits .
  ?threshold fsar:numericValue ?thresholdValue ;
             fsar:units ?thresholdUnits .
  OPTIONAL { ?threshold fsar:note ?thresholdNote }
}
ORDER BY ?metricLabel ?benchmarkType
```

**CQ-WSP-2: What confidence category does the rapid status assessment have?**

```sparql
SELECT ?assessment ?rapidStatus ?confidence ?confidenceLabel
WHERE {
  ?assessment a dfo:StockAssessment ;
              fsar:producesRapidStatus ?rapidStatus ;
              fsar:hasConfidence ?confidence .
  ?confidence skos:prefLabel ?confidenceLabel .
  ?rapidStatus skos:prefLabel ?statusLabel .
}
```

**CQ-WSP-3: What decision requirements are triggered by the status/metric positions?**

```sparql
SELECT ?assessment ?rapidStatus ?condition ?conditionLabel ?requirement ?requirementLabel ?framework ?frameworkLabel
WHERE {
  ?assessment a dfo:StockAssessment ;
              fsar:producesRapidStatus ?rapidStatus .
  ?rapidStatus skos:prefLabel ?statusLabel .
  ?requirement a fsar:DecisionRequirement ;
               rdfs:label ?requirementLabel ;
               fsar:triggeredBy ?condition ;
               fsar:mandatedBy ?framework .
  ?condition rdfs:label ?conditionLabel .
  ?framework rdfs:label ?frameworkLabel .
  # Note: This query structure assumes conditions can be inferred from rapid status
  # Actual implementation may require additional logic to connect status to conditions
}
```

**CQ-WSP-4: How do WSP metric benchmarks relate to Learning Tree 3 algorithm thresholds?**

```sparql
SELECT ?metric ?metricLabel ?benchmarkValue ?benchmarkUnits ?thresholdValue ?thresholdUnits ?rationaleNote
WHERE {
  ?metric a fsar:WSPMetric ;
          rdfs:label ?metricLabel ;
          fsar:hasBenchmark ?benchmark ;
          fsar:hasAlgorithmThreshold ?threshold .
  ?benchmark fsar:numericValue ?benchmarkValue ;
             fsar:units ?benchmarkUnits .
  ?threshold fsar:numericValue ?thresholdValue ;
             fsar:units ?thresholdUnits .
  OPTIONAL { ?threshold fsar:note ?rationaleNote }
}
ORDER BY ?metricLabel
```

---

## 4) SPARQL Query Pack (v0.1) — Backing the UI

_(Prefixes omitted; assume : is ontology ns; dprod: for Data Product Ontology; prov: for provenance. Queries marked with ⚠️ require ontology investigation.)_

**Q1 — Evidence Completeness by Decision** ⚠️

```sparql
SELECT ?decision (IF(?critMissing=0, IF(?optMissing=0, "Complete", "Gaps"), "Missing-Critical") AS ?state)
WHERE {
  BIND(:TAC_HCR AS ?decision)
  {
    SELECT (SUM(?isCritMissing) AS ?critMissing) (SUM(?isOptMissing) AS ?optMissing)
    WHERE {
      # required=false means optional; required=true means required evidence
      VALUES (?field ?required) {
        (:status_value true)
        (:reference_point_type true)
        (:status_ci false)
      }
      BIND(IF(?required=true && NOT EXISTS { ?s :hasField ?field }, 1, 0) AS ?isCritMissing)
      BIND(IF(?required=false && NOT EXISTS { ?s :hasField ?field }, 1, 0) AS ?isOptMissing)
    }
  }
}
```

**Q2 — Proxy Without Justification**

```sparql
SELECT ?record WHERE {
  ?record :data_source_type :genetic_proxy .
  FILTER NOT EXISTS { ?record :proxy_justification ?j . FILTER(STRLEN(STR(?j))>0) }
}
```

**Q3 — Method Reproducibility**

```sparql
SELECT ?method ?name ?version ?commit WHERE {
  ?status :wasGeneratedBy ?method .
  ?method :method_name ?name ; :method_version ?version ; :code_commit ?commit .
}
```

**Q4 — Reference Points Used**

```sparql
SELECT ?rp ?type ?benchMethod ?sensitivity WHERE {
  ?status :used ?rp .
  ?rp :reference_point_type ?type ; :benchmark_method ?benchMethod .
  OPTIONAL { ?rp :benchmark_sensitivity ?sensitivity }
}
```

**Q5 — Missing Uncertainty**

```sparql
SELECT ?node WHERE {
  { ?status :status_value ?v FILTER(NOT EXISTS { ?status :status_ci ?ci }) }
  UNION { ?gsi a :GSIResult FILTER(NOT EXISTS { ?gsi :gsi_sample_size ?n }) }
}
```

**Q6 — Data Currency (last updated per component)**

```sparql
SELECT ?component ?id ?lastModified ?version WHERE {
  VALUES ?component { :Dataset :Method :ReferencePoint :Status :Advice }
  ?id a ?component ; :lastModified ?lastModified .
  OPTIONAL { ?id :version ?version }
}
```

**Q7 — Scientific Output Text + Review** ⚠️

```sparql
SELECT ?output ?text ?reviewer ?date WHERE {
  ?output a :ScientificOutput ; :scientific_output_text ?text ; :reviewer ?reviewer ; :date ?date .
}
```

**Q8 — Linked Documents (FSAR / Tech / Research)**

```sparql
SELECT ?doc ?type ?title ?id ?issued ?url ?contentUrl WHERE {
  ?output a :ScientificOutput ; :hasDocument ?doc .
  ?doc a :Document ; :doc_type ?type ; dcterms:title ?title ; dcterms:identifier ?id ; dcterms:issued ?issued .
  OPTIONAL { ?doc schema:url ?url }
  OPTIONAL { ?doc schema:contentUrl ?contentUrl }
}
```

**Q9 — Data Product Integration** ⚠️

```sparql
SELECT ?dataProduct ?title ?owner ?service WHERE {
  ?dataProduct a dprod:DataProduct ;
    dprod:title ?title ;
    dprod:dataProductOwner ?owner ;
    dprod:outputPort ?service .
  ?service a dprod:DataService ;
    dprod:endpointURL ?endpoint .
}
```

**Q10 — Controlled‑Vocab Options by Scheme**

```sparql
SELECT ?concept ?label ?notation WHERE {
  ?concept skos:inScheme :ReferencePointType ;
           skos:prefLabel ?label .
  OPTIONAL { ?concept skos:notation ?notation }
}
```

**Q11 — Downgrade Criteria**

```sparql
SELECT ?criterion ?label ?definition WHERE {
  ?criterion skos:inScheme :DowngradeCriteria ;
            skos:prefLabel ?label .
  OPTIONAL { ?criterion skos:definition ?definition }
}
```

---

## 5) Graph Database & Data Ingest (2‑Month POC)

**Choice:** **Apache Jena Fuseki (Docker)** — fast to stand up; great for JSON‑LD loads; local or VM.

**Graph Database Requirements:**

- **MVP:** Basic Fuseki setup with core graphs for Barkley Sockeye demonstration
- **Future:** Full triple store implementation with advanced querying capabilities
- **Integration:** Support for DPROD ontology classes and relationships
- **Performance:** Optimized for SPARQL queries supporting evidence completeness checks

**Graphs**

- `graph:fsar:2025:barkley` — current cycle
- `graph:vocab` — SKOS terms; `graph:shapes` — SHACL
- `graph:dprod` — Data Product Ontology integration (future)

**Sources → JSON‑LD Extracts**

- SPSR extracts (status inputs, ref points, metadata)
- GRD subset (Barkley, `Run_ID`, `Sample_ID`, `Assay_ID`)
- FSAR scientific output block + provenance
- **Investigation needed:** How to integrate DPROD data product descriptions

**Load Steps**

1. Export CSV/JSON from SPSR/GRD/FSAR → convert to JSON‑LD via small scripts (R or Python + rdflib).
2. `tbdloader`/`s-put` (Jena) to load per‑graph; store prefixes; run SHACL report.
3. Run SPARQL pack; generate Advice Trace Pack assets (no cross‑cycle diffs; show data currency only).
4. **Future:** Implement DPROD integration and advanced graph database features.

---

## 6) SPSR Schema Recommendations (minimal, high-leverage tweaks)

Your current SPSR tables already include LRP/USR/TR fields and rich age/harvest columns. To avoid a disruptive rewrite:

**Critical (do now):**

- **Add Benchmarks table** (or JSON field) with: `type` {LRP, USR, TR}, `value`, `units`, `method_ref`, `inputs_ref`, `time_window`, `uncertainty`, `version`, `derived_on`, `derived_by`, `reference_point_type` (controlled vocab), `benchmark_method` (controlled vocab), `benchmark_sensitivity` (flags)
- **Add StatusAssessment fieldset** per SMU-year: `status_zone`, `decision_basis` (link to benchmark ids), `uncertainty_summary`, `downgrade_reason?`, `reviewer`, `date`, `status_confidence` (probabilities/CI), `ciLower`, `ciUpper`, `probabilityGreen`, `probabilityAmber`, `probabilityRed`
- **Add PolicyReadiness flags**: `below_lrp` (bool), `hcr_id`, `hcr_params`, `rebuilding_plan_url`, `hcrIdentifier`, `hcrParameters`
- **Add Submission entities** (for intake):
  - `Submission`: `id`, `smu`, `year`, `user_id`, `state` {Draft|Validated|Ready|Ingested}, `provenance_minimum` fields (`method`, `version`, `code_commit`, `reviewer`, `date`), `created_at`, `updated_at`
  - `ValidationRun`: `submission_id`, `tool` {SHACL|R}, `version`, `timestamp`, `passed` (bool), `error_json`
- **Add CU inclusion/proxy table** with fields: `cu_id`, `decision` (included/excluded/proxied), `justification`, `reviewer`, `review_date`
- **Add GSI usage fields**: `gsiUsed` (bool), `gsiSampleSize` (int), `gsiAssignmentUncertainty` (text/CI or % misID), `baseline_reference`, `fisheryType` (mixed-stock/single-stock)

**Medium:**

- **Standardize units** using QUDT IRIs stored alongside numerics (keep current "pragmatic literal + unit IRI" convention)

**Validator & Data Model Alignment:**

- **Add/ensure fields:** `benchmark_method`, `reference_point_type`, `proxy_justification`, `code_commit`, `reviewer`, `date`, `gsi_sample_size`, `gsi_ci`, `gsiUsed`, `gsiAssignmentUncertainty`, `baseline_reference`, `status_confidence`, `downgradeReason`, `belowLRP`, `rebuildingPlanURL`, `hcrIdentifier`, `hcrParameters`
- **SHACL shapes:** required vs optional by decision context; friendly messages; error severity (Critical/High/Info)
- **R validator:** fail‑fast CLI (non‑zero on error), row/col pinpoint, fix‑hints mapping
- **GRD join:** prefer `Run_ID + Sample_ID` (optional `Assay_ID`) for Barkley
- **Error JSON contract:** Normalize validator output keys: `severity`, `code`, `message`, `row`, `column`, `file`, `hint`.
- **Permissions & gating:** Only whitelisted users (Django auth/email list) can submit; human review required before ingestion.
- **Template tabs:** Read-only vocab sheets (RP types, methods, status zones) powering data validation dropdowns
- **Risk assessment:** Mixed-stock fishery + `gsiUsed` = false → show risk chip and require rationale
- **Policy compliance:** `belowLRP` = true requires valid Rebuilding Plan link or shows Missing-Critical

These are small additive tables/columns that unlock everything above without refactoring your time-series or age structures.

---

## 7) Tool Stack & Standards (recommended)

- **Standards:** SKOS (vocab), PROV‑O/DQV (provenance/quality), SHACL (validation), JSON‑LD (interchange).
- **Triple store:** Jena Fuseki (Docker); local dev + GitHub CI for lint/validate.
- **UI:** Quarto static site + light JS; optional R Shiny later.
- **Pipelines:** GitHub Actions (validate TTL/JSON‑LD, run SHACL, run R tests, build site).

---

## 8) 2‑Month POC Plan — Barkley Sockeye

**Weeks 1–2:**

- Extract Barkley data; publish vocab v0.1; define JSON‑LD context
- **Stand up Fuseki graph database** with core graphs
- Load `graph:vocab`/`graph:fsar:2025:barkley`
- **Add SPSR schema enhancements** (Benchmarks table, StatusAssessment fieldset, PolicyReadiness flags)
- **Investigate DPROD integration** requirements
- Stand up **Intake UI skeleton** (HTMX) and vocab endpoints; persist `Submission` drafts
- Parse `.xlsx` Metadata tab server‑side; preview parsed metadata

**Weeks 3–4:**

- Implement SPARQL Q1–Q9 (enhanced MVP queries including Policy/Legal, Change Intelligence, CU Accounting)
- SHACL v0.1 for basic validation + policy readiness gates
- Excel template + R validator v0.1 with enhanced metadata requirements
- Generate first Advice Trace Pack with structured deltas vs. previous FSAR
- **Implement CU Accounting** (included/excluded/proxied CUs with justification)
- Integrate **SHACL + R** adapters; return normalized error JSON; add submission state machine (Draft/Validated/Ready)
- Define/decide **R validator run mode** (sync vs async) and document as decision

**Weeks 5–6:**

- Add **Policy & Legal Readiness** panel with hard gates
- Add **Change Intelligence** (delta vs. last FSAR)
- Wire enhanced UI (picker, CU-first hierarchical flow, drawer with new tabs, export)
- **Implement GSI Usage tracking** (sample sizes, assignment uncertainty)
- **Add Downgrade Criteria** display and validation
- Wire **intake submission review/approval** workflow (human gating) and ingestion stub
- Add **tailored template** generator endpoint and error report download

**Weeks 7–8:**

- Acceptance sweep (enhanced badges, policy overlays, export validations with deltas)
- **Implement Benchmark entities** as first-class objects with derivation evidence
- **Investigate SIL/SEN integration** with Minh Doan's PR
- Docs + exec one‑pager; demo handoff with policy readiness demonstration
- **Plan post-MVP features** and DPROD integration
- Acceptance sweep for **intake** (permissions, audit events, Ready gating)
- Document submission lifecycle and error contract; add API contract tests
