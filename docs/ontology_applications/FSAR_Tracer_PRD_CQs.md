# Advice Trace Demo — UX & Interface Spec (FSAR Hero)

**Goal:** For one SMU, show a transparent, reproducible chain: **data used → method → benchmarks/reference points → status → advice text → decision context**. Optimized for managers (clarity) and analysts (evidence).

---

## 1) Personas → Stories → Acceptance

### Persona A — Executives / Directors / Branch & Division Managers

- **Goal:** Rapid assurance that the **evidence underpinning advice** is defensible and current; see key risks and **data currency** (last‑updated/version pins). Also see coverage (how many SMUs have FSARs; proportion in zones).
- **Stories:** Select **SMU + Year** → see an **Evidence Completeness** gauge and **Data Currency** panel; **download Advice Trace Pack** for briefing/audit.
- **Acceptance:** **Evidence Completeness** reports *Complete* when all required evidence for the chosen decision context exists; *Gaps* lists missing optional items; *Missing‑Critical* lists missing required items. **Data Currency** shows last‑updated timestamps and version pins for **Datasets/Methods/Ref Points/Status/Advice**. **Export** downloads the pack (trace.jsonld, evidence, figures, queries, PROV) with valid hashes/versions.

### Persona B — Stock Assessment Biologist / FSAR Reviewer

- **Goal:** Verify methods, benchmarks, reproducibility; confirm uncertainty handling.
- **Stories:** Open **Method** → view parameters + **exact code commit/tag**; inspect **Reference Points** (type/value/derivation + **benchmark method**); toggle **Uncertainty overlay** to confirm GSI/CI presence and propagation.
- **Acceptance:** **Method** shows name/version/parameters + link to exact commit/tag used by figures/status. **Reference Points** include type/value/derivation + benchmark method; sensitivity flagged. **Uncertainty overlay** badges missing **GSI**, **sample sizes**, or **status CIs**; click reveals missing fields.

### Persona C — Data Steward / Analyst

- **Goal:** Meet standards (terms, provenance, uncertainty); fail fast; ship FSAR sections quickly.
- **Stories:** Use **Excel template + R validator + SHACL** to validate with fix hints; enter terms via **controlled‑vocab dropdowns**; open **Evidence Drawer** to verify provenance minimum.
- **Acceptance:** **Validator** returns non‑zero on violations with row/column + fix hint; passes after correction. **Controlled‑vocab** fields (`spawner_origin`, `data_source_type`, `reference_point_type`) enforce dropdowns; off‑list rejected with message. **Evidence** shows `data_source`, `method`, `code_version/hash`, `reviewer`, `date`; missing items block **Ready**.

## 2) UI/UX Inspiration (expanded but lean)

**Single page** flow focused on clarity and drill‑downs. The page is split into a left **Advice Trace** and a right **Evidence Drawer**.

### 2.1 Visual Flow

- **Header bar:** SMU + Year picker (Barkley Sockeye • 2025), Decision Context (e.g., TAC/HCR), **Documents** (FSAR / Tech Report / Research Document), Export.
  - **Documents quick links:** buttons to open/download the current cycle’s **FSAR PDF** and any **Technical Reports/Research Documents** (new tab). If multiple docs exist, a dropdown lists title • doc number • year.
- **Advice Trace timeline (left‑to‑right):** Six clickable nodes — **Data → Method → Reference Points → Status → Advice → Decision Context**.
  - Each node shows a title, short subtitle (e.g., *SR benchmark*), and an **Evidence badge** with small **risk chips** (*Proxy w/out justification*, *Missing CI*, *Sensitivity flagged*).
  - **Evidence badge states:** **Complete / Gaps / Missing‑Critical** (note: this reflects *evidence presence/quality*, not FSAR approval). Optionally show a **Review Stage** tag if the FSAR workflow exists (e.g., *Not started / In review / Approved*).
  - **Hover**: quick tooltip with 1–2 key facts (e.g., *Sgen=14.2k; SR method; prior=Ricker*).
  - **Click**: opens the right‑hand **Evidence Drawer** anchored to that node.
- **Evidence Drawer (right slide‑over):** Tabs **Overview • Inputs • Methods • Benchmarks • Quality • Documents • Currency**. Always shows **provenance minimum** (source, method, code commit, reviewer/date) at the top.
  - **Documents tab:** Lists linked artifacts with icon, title, doc number, year, size; actions: **Open**, **Download**, **Copy citation**.
- **Export button:** Packages the **Advice Trace Pack** (*figures/*.png, summary pdf of advice trace node metadata (risks, status, relevant advice reports/documents in pdfs from DFO catalogue). Includes a **/docs/** subfolder with cached PDFs if allowed and an optional /data/ folder if toggled.

This will be an interactive network graph/horizontal stepper (timeline) with clickable nodes. If we need richer relationships later (e.g., multiple datasets feeding multiple methods), we can add a **node‑link view** (toggle) using Cytoscape.js or D3. MVP keeps it simple.



### 2.2 Purpose of UI Elements

- **Evidence badges (replacement for “readiness”):** Summarize **evidence presence/quality** for the decision context at each node:\
  **Complete** = all required evidence present; **Gaps** = optional elements missing; **Missing‑Critical** = required evidence missing. These roll up SHACL/validator results and CQ checks. *(Does not imply review approval.)*
- **Risk chips:** Compact flags tied to specific CQs (e.g., *proxy justification missing*, *no status CI*). Clicking a chip focuses the Drawer on the missing field(s).
- **Evidence Drawer:** The audit lens—shows the *who/what/when/how* for the selected node: datasets, parameters, reference‑point derivations, code commit, reviewer/date, and links to figures or repos.
- **Documents:** Surface authoritative downloads (FSAR, Technical Reports, Research Documents). Each item shows **doc type**, **title**, **doc number/identifier**, **issued date**, **version**, **size**, and a **canonical URL/DOI**; if internal, use a **pre‑signed URL**. A small badge indicates **Public** or **Internal**.
- **Currency tab:** Shows last‑updated and version pins per component; highlights stale items with thresholds (e.g., >12 months).
- **Drill‑down:** From Drawer items (e.g., a dataset row, code commit, or document), jump to the source in SPSR (record view), GRD (run/sample), CSAS/DFO publications page, or GitHub (exact commit/tag) or Zenodo Release. Breadcrumbs let you pop back to the node.

### 2.3 Minimal Entities/Relations Needed in Ontology

- **Entities:** `Dataset`, `Method`, `ReferencePoint`, `StatusAssessment`, `Advice`, `DecisionContext`, `Figure`.
- **Relations (PROV‑O flavored):** `StatusAssessment used Dataset/ReferencePoint`, `StatusAssessment wasGeneratedBy Method`, `Advice wasDerivedFrom StatusAssessment`, `Advice supports DecisionContext`, `Figure wasDerivedFrom {Dataset,Method}`.

---

## 2b) Architecture Pattern & SPSR (Django) Integration

**Context:** SPSR is a **layered monolith** today (Presentation → Application → Domain → Infrastructure). The Advice Trace should respect that layering, add a thin ontology/graph layer, and keep a clean **contract** between SPSR data and the trace UI.

### Recommended Design Pattern

**"Layered Monolith + Contract + Graph Sidecar"**

- **Presentation (Django)**: Pages/templates (HTMX/Alpine) render the **Advice Trace** timeline and open the **Evidence Drawer**.
- **Application Services (Django)**: `AdviceTraceService` orchestrates pulls from SPSR, GRD, and the graph, assembles **DTOs** for the UI, and exposes a **DRF endpoint** returning **JSON‑LD**.
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

1. **POC (Weeks 1–8)** — *Django‑native*
   - Add `/api/advice-trace/{smu}/{year}` (DRF) returning JSON‑LD.
   - Add `/advice-trace/?smu=…&year=…` Django view rendering the timeline (HTMX partials for Drawer).
   - Stand up **Fuseki** in Docker; connect via a tiny **SPARQL adapter** (e.g., `SPARQLWrapper`).
   - Compute **Badges** server‑side (combine SHACL results + SPARQL CQ results) → render as HTMX fragments.
2. **Hardening**
   - Cache SPARQL results (Django cache) per SMU/Year; invalidate on data refresh.
   - Move JSON‑LD generation to a scheduled management command; publish to S3/bucket for archival.
3. **Optional external publishing**
   - Generate a Quarto **static site** that reads the same JSON‑LD + figures for external stakeholders; link it from SPSR.

### Concrete Touchpoints (Django)

- **Endpoints**
  - `GET /api/advice-trace/{smu}/{year}` → JSON‑LD (trace)
  - `GET /api/documents?smu=&year=` → PDFs/links metadata
  - `GET /api/cq/{smu}/{year}` → CQ results used by badges (optional; or compute inline)
- **Adapters**
  - **SPARQL adapter**: small class wrapping query files (Q1–Q8); returns rows → DTOs
  - **ACL mappers**: SPSR models → ontology JSON‑LD (via `rdflib` or hand‑rolled JSON)
- **Validators**
  - `python manage.py run_shacl` (pySHACL) against shapes; persist results for badge rollups
  - `validate_spsr.R` in CI; post results to a table or cache

### Libraries & Patterns (Django‑native)

- **UI:** HTMX, Alpine.js (no SPA); **Cytoscape.js** if/when node‑link needed
- **Graph:** `SPARQLWrapper` (Py) or `rdflib.plugins.sparql`
- **JSON‑LD:** `rdflib` or plain JSON with a context; keep a versioned `@context`
- **Caching:** `django‑redis` (per SMU/Year keyspace)
- **Testing:** pytest + snapshot tests for SPARQL responses; SHACL as CI gate

### Where Badges, Drawer, and Drill‑downs live

- **Badges**: computed server‑side from SPARQL + SHACL; rendered as small HTMX fragments per node (so they can refresh without full page reload).
- **Evidence Drawer**: a Django partial that takes a node `id` and queries (via service) for provenance, parameters, documents, figures; deep‑links to SPSR record pages and CSAS/DFO docs.
- **Drill‑downs**: standard Django routes for SPSR records (dataset, method configs), GRD run/sample pages, and external doc links (new tab). HTMX keeps the experience snappy.

### Migration/Scalability Notes

- If/when SPSR evolves toward services, the **JSON‑LD contract** and **SPARQL adapter** remain valid; you can swap the graph engine (e.g., Blazegraph, Neptune) without changing UI.
- The **anti‑corruption layer** keeps ontology terms from leaking into core domain models; rollouts are safer.

---

## 3) Competency Questions — Advice Trace (Barkley Sockeye)

— Advice Trace (Barkley Sockeye)

*(Each CQ backs a UI badge, drawer, or diff; fields listed must exist in data/template/SHACL.)*

**Data**

- What datasets feed Barkley Sockeye’s FSAR **status** this year, and do they declare `data_source_type`, `spawner_origin`, and **time coverage**? *(UI: Data node badge)*
- Where is **proxy** used (e.g., GSI, index) and is `proxy_justification` present? *(Badge + Drawer)*

**Method**

- Which **method** (name/version) and **parameters** produced the status, and what **code commit/tag**? *(Drawer: Method)*

**Reference Points**

- Which **reference\_point\_type** (Sgen/USR/LRP/…) and **benchmark\_method** (SR/percentile/expert) were applied; is **benchmark\_sensitivity** flagged? *(Badge + Drawer)*

**Status**

- What is the **status result** and **CI**; is **GSI uncertainty** recorded and propagated? *(Badge + Overlay)*

**Advice**

- What **advice text** and assumptions were issued; who reviewed/approved and when? *(Drawer: Advice)*

**Decision Context**

- For the chosen **context** (e.g., TAC/HCR), are all required **indicators/ref points** present? If not, which **gaps** exist that prevent **Complete** evidence? *(Completeness widget)*

**Provenance & Data Currency**

- When were the **Datasets/Methods/Ref Points/Status/Advice** last updated, and what version/commit is pinned? If not present, flag as a risk. *(Evidence Drawer + Currency panel)*

**Required Fields Checklist (v0.1)**\*\* `data_source_type`, `spawner_origin`, `proxy_justification`, `method_name`, `method_version`, `code_commit`, `reference_point_type`, `benchmark_method`, `benchmark_sensitivity`, `status_value`, `status_ci`, `gsi_sample_size/ci`, `advice_text`, `reviewer`, `date`, `decision_context_id`.

---

## 4) SPARQL Query Pack (v0.1) — Backing the UI

*(Prefixes omitted; assume : is ontology ns; dc: for DecisionContext; prov: for provenance.)*

**Q1 — Evidence Completeness by Decision Context**

```sparql
SELECT ?context (IF(?critMissing=0, IF(?optMissing=0, "Complete", "Gaps"), "Missing-Critical") AS ?state)
WHERE {
  BIND(:TAC_HCR AS ?context)
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

**Q7 — Advice Text + Review**

```sparql
SELECT ?advice ?text ?reviewer ?date WHERE {
  ?advice a :Advice ; :advice_text ?text ; :reviewer ?reviewer ; :date ?date .
}
```

**Q8 — Linked Documents (FSAR / Tech / Research)**

```sparql
SELECT ?doc ?type ?title ?id ?issued ?url ?contentUrl WHERE {
  ?advice a :Advice ; :hasDocument ?doc .
  ?doc a :Document ; :doc_type ?type ; dcterms:title ?title ; dcterms:identifier ?id ; dcterms:issued ?issued .
  OPTIONAL { ?doc schema:url ?url }
  OPTIONAL { ?doc schema:contentUrl ?contentUrl }
}
```

---

## 5) Triple Store & Data Ingest (2‑Month POC)

**Choice:** **Apache Jena Fuseki (Docker)** — fast to stand up; great for JSON‑LD loads; local or VM.

**Graphs**

- `graph:fsar:2025:barkley` — current cycle
- `graph:vocab` — SKOS terms; `graph:shapes` — SHACL

**Sources → JSON‑LD Extracts**

- SPSR extracts (status inputs, ref points, metadata)
- GRD subset (Barkley, `Run_ID`, `Sample_ID`, `Assay_ID`)
- FSAR advice block + provenance

**Load Steps**

1. Export CSV/JSON from SPSR/GRD/FSAR → convert to JSON‑LD via small scripts (R or Python + rdflib).
2. `tbdloader`/`s-put` (Jena) to load per‑graph; store prefixes; run SHACL report.
3. Run SPARQL pack; generate Advice Trace Pack assets (no cross‑cycle diffs; show data currency only).

---

## 6) SPSR Validator & Data Model Alignment (minimal changes)

- **Add/ensure fields:** `benchmark_method`, `reference_point_type`, `proxy_justification`, `code_commit`, `reviewer`, `date`, `gsi_sample_size`, `gsi_ci`.
- **SHACL shapes:** required vs optional by decision context; friendly messages.
- **R validator:** fail‑fast CLI (non‑zero on error), row/col pinpoint, fix‑hints mapping.
- **GRD join:** prefer `Run_ID + Sample_ID` (optional `Assay_ID`) for Barkley.

---

## 7) Tool Stack & Standards (recommended)

- **Standards:** SKOS (vocab), PROV‑O/DQV (provenance/quality), SHACL (validation), JSON‑LD (interchange).
- **Triple store:** Jena Fuseki (Docker); local dev + GitHub CI for lint/validate.
- **UI:** Quarto static site + light JS; optional R Shiny later.
- **Pipelines:** GitHub Actions (validate TTL/JSON‑LD, run SHACL, run R tests, build site).

---

## 8) 2‑Month POC Plan — Barkley Sockeye

**Weeks 1–2:** Extract Barkley data; publish vocab v0.1; define JSON‑LD context; stand up Fuseki; load `graph:vocab`/`graph:fsar:2025:barkley`.

**Weeks 3–4:** Implement SPARQL Q1–Q5; SHACL v0.1; Excel template + R validator v0.1; generate first Advice Trace Pack.

**Weeks 5–6:** Add **Data Currency** (Q6); harden provenance; wire minimal UI (picker, timeline, drawer, export); Stikine optional for parallel test.

**Weeks 7–8:** Acceptance sweep (badges, overlays, export validations); docs + exec one‑pager; demo handoff.

