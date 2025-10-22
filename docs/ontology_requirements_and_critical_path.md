# Ontology Product Plan & Critical Path — DFO Salmon Ontology

**Purpose of this document**  
Define the *impetus* and product-context for the DFO Salmon Ontology, identify the **critical path** that delivers tangible value in 2 months, and align seven ongoing projects that will leverage the ontology.

**North‑star demo (highest impact):** **FSAR Advice Trace** for one SMU (Barkley Sockeye) — a transparent chain from **Data → Method → Reference Points → Status → Advice → Decision Context**, with evidence completeness, data‑currency pins, risk chips, and links to FSAR/Tech/Research documents.

---

## 7 Core Project Streams (updated)

### 1) Salmon Population Summary Repository (SPSR)
- **Purpose:** Centralized DB/web app for standardized reuse of data from Fisheries Science Reports (FSRs).
- **Ontology role:** Shared terms (population metrics, reference points, spawner origin, benchmark methods) + JSON‑LD contract for SPSR exports and intake.
- **Tangible output:** Excel template + SHACL + R validator; SPSR Intake Assistant (schema checks, vocab dropdowns, fix‑hints).

### 2) Genetics Results Database (GRD)
- **Purpose:** Repository of genetic assignment results (docID outputs) from molecular labs.
- **Ontology role:** Stable identifiers and relations (Run_ID, Sample_ID, Assay_ID) linking GRD results to SPSR records and assessments; uncertainty capture for GSI comp/CI.
- **Tangible output:** Join specification (**ADR‑001**) and GRD→SPSR mapping schema; upstream QC flags.

### 3) Stream Inspection Logs & Escapement Narratives (SILS/Narratives)
- **Purpose:** Standardize and automate generation of escapement narratives from stream inspections.
- **Ontology role:** Narrative bundle pattern (SILS→SEN), provenance and uncertainty properties, linkage to SPSR population summaries.
- **Tangible output:** Narrative bundle data model + provenance pattern (Phase 2) and validator hooks.

### 4) Fisheries Science Advice Reports (FSAR / FSR Reviews)
- **Purpose:** Deliver evidence‑based status/trend assessments.
- **Ontology role:** Encode reference points, benchmark methods, and provenance of advice; enable trace from datasets → figures → advice text.
- **Tangible output:** Competency questions, SPARQL pack, **Advice Trace** UI components.

### 5) Decision Contexts for Management
- **Purpose:** Support management decisions (TAC/HCR, rebuilding) with consistent indicators and reference points.
- **Ontology role:** Lightweight decision model (objectives → indicators → reference points) enabling **evidence completeness** checks.
- **Tangible output:** Completeness queries/shapes per decision context; policy mapping table.

### 6) Composite CU Escapement Metadata & Cookbook (NuSEDS / SIL / SEN alignment)
- **Purpose:** Harmonize CU‑level composite time‑series metadata and produce a practical *cookbook* with reusable code and case studies.
- **Why now:** Enables repeatable, transparent composites that downstream FSARs and Outlooks can trust.
- **Ontology role:** Formalizes metadata as an ontology module (.ttl), aligns synonyms/values with SKOS, and provides SHACL shapes for CU composites; adds provenance fields needed for Advice Trace.
- **Tangible outputs:**
  - **Metadata Fields v0.1** (list + definitions + examples) derived from ~55 vetted CU composites.
  - **Ontology module/knowledge model (.ttl)** with validation rules and example records.
  - **Escapement Data *Cookbook*** with runnable code (R/Python) and ≥2 **case studies** on unvetted CUs; consolidated code utilities (package).
  - **Prioritized NuSEDS backlog** (top‑10 fields) to capture key metadata at SIL/SEN level.
- **Notes for critical path:** Use fields like `data_source_type`, `spawner_origin`, `method_class`, `proxy_justification`, and provenance pins; these are directly consumed by Advice Trace evidence badges and currency panel.

### 7) Salmon Outlook Report (Reproducible Data Product)
- **Purpose:** Modernize the annual Outlook process (collection, tracking, formatting, visualization, reporting) into a reproducible pipeline.
- **Ontology role:** Standardizes inputs and document metadata; maps contributors/roles, submission windows, and outputs; supports canonical identifiers for documents and links (FSAR/Tech/Research) from the Advice Trace.
- **Tangible outputs:**
  - Documented workflow (contributors, formats, roles, timelines, audiences).  
  - Structured intake (survey/forms) to reduce email bloat; normalized JSON/CSV.
  - R / R Markdown build for Outlook tables, figures, and maps; publishable technical report with code/doc as a reproducible artifact.
- **Notes for critical path:** Provide Outlook *document* and *link metadata* (`:Document` nodes) so Advice Trace can surface authoritative downloads.

---

## Highest‑Impact Demo & Alternatives

### A) **FSAR Advice Trace (Hero)** — highest leverage
- **What it proves:** Transparent, reproducible line of evidence for one SMU (Barkley Sockeye). Shows **Evidence Completeness**, **Data Currency**, risk chips (e.g., proxy w/out justification), and **document links** (FSAR/Tech/Research).
- **Why it matters:** Executive‑ready view + analyst drill‑downs; reusable JSON‑LD contract and SPARQL pack for other SMUs.

### B) Alternative demos (if A is blocked)
1. **SPSR Intake Assistant** — validator + SHACL + fix‑hints + controlled vocab dropdowns; shows immediate value to authors.
2. **GRD↔SPSR Join Explorer** — Run_ID + Sample_ID (+ Assay_ID) linkage and uncertainty flags; small browser for GSI → Status inputs.
3. **SILS→Narrative Prototype** — one stream: inspection logs to a generated narrative bundle with provenance and variance.
4. **Decision‑Context Completeness Checker** — simple checklist widget driven by SHACL/queries for TAC/HCR.

---

## Critical Path (next 2 months)

**Week 1–2**
- Stand up **Jena Fuseki**; define JSON‑LD `@context` and IRIs.  
- Extract Barkley SPSR/GRD/FSAR snippets → **trace JSON‑LD** (Dataset/Method/RefPoint/Status/Advice/Document).  
- Publish **vocab v0.1** (SKOS) and **SHACL v0.1** for required/optional fields.

**Week 3–4**
- Implement SPARQL Q1–Q5 (evidence completeness, proxy, method, refs, uncertainty).  
- Build **Django HTMX** timeline + **Evidence Drawer** stubs; wire badges + risk chips from CQ/SHACL results.  
- Add **Documents** tab fed by DRF endpoint + `:Document` nodes.

**Week 5–6**
- Add **Data Currency** query (Q6) and UI panel; harden provenance pins (commit/timestamps).  
- Finish **Export Pack** (trace.jsonld, evidence CSVs, figures, SPARQL, PROV, README).  
- Walkthrough with Barkley stakeholders; capture gaps; prep demo.

**Week 7–8**
- Acceptance sweep against UX spec; tighten SHACL messages; finalize docs/one‑pager for execs.  
- Optional: lightweight publication (internal) of Advice Trace for reuse.

---

## Architectural Notes (how this plugs into SPSR)
- **Layered monolith + contract + graph sidecar.** The UI is Django‑native (HTMX/Alpine), backed by a DRF **JSON‑LD** endpoint and a **SPARQL adapter** to Fuseki; SPSR models are mapped via an anti‑corruption layer (ontology context).
- **Evidence badges** summarize evidence presence/quality (*Complete/Gaps/Missing‑Critical*). **Currency** pins last‑updated + version. **Risk chips** are CQ findings.
- **Documents** are first‑class `:Document` nodes with canonical URLs/IDs; surfaced in header and Drawer.

---

## Standards & Stack (brief)
- **Standards:** SKOS, PROV‑O/DQV, SHACL, JSON‑LD.  
- **Store/Query:** Jena Fuseki + SPARQL; `SPARQLWrapper`/`rdflib` in Django.  
- **UI:** Django templates + HTMX/Alpine; optional Cytoscape.js node‑link.
- **Validation:** R CLI + pySHACL; GitHub Actions for lint/validate/build.

---

## Risks & Mitigations (POC)
- **Source coupling / schema drift:** Use JSON‑LD contract + ACL mapper; snapshot trace per release.  
- **Auth for documents:** Pre‑signed or session‑protected links; cache metadata, not files.  
- **Bandwidth:** Keep the hero to **one SMU**; defer node‑link view and narrative bundles to Phase 2.

---

## Naming
Suggested title for this doc: **“Ontology Product Plan & Critical Path (DFO Salmon Ontology)”** — combines *impetus/context* with a concrete delivery path.

