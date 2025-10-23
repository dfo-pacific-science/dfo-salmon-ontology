# Ontology Product Plan & Critical Path — DFO Salmon Ontology

**Purpose of this document**  
Define the _impetus_ and product-context for the DFO Salmon Ontology, identify the **critical path** that delivers tangible value in 2 months, and align seven ongoing projects that will leverage the ontology.

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

- **Purpose:** Harmonize CU‑level composite time‑series metadata and produce a practical _cookbook_ with reusable code and case studies.
- **Why now:** Enables repeatable, transparent composites that downstream FSARs and Outlooks can trust.
- **Ontology role:** Formalizes metadata as an ontology module (.ttl), aligns synonyms/values with SKOS, and provides SHACL shapes for CU composites; adds provenance fields needed for Advice Trace.
- **Tangible outputs:**
  - **Metadata Fields v0.1** (list + definitions + examples) derived from ~55 vetted CU composites.
  - **Ontology module/knowledge model (.ttl)** with validation rules and example records.
  - **Escapement Data _Cookbook_** with runnable code (R/Python) and ≥2 **case studies** on unvetted CUs; consolidated code utilities (package).
  - **Prioritized NuSEDS backlog** (top‑10 fields) to capture key metadata at SIL/SEN level.
- **Notes for critical path:** Use fields like `data_source_type`, `spawner_origin`, `method_class`, `proxy_justification`, and provenance pins; these are directly consumed by Advice Trace evidence badges and currency panel.

### 7) Salmon Outlook Report (Reproducible Data Product)

- **Purpose:** Modernize the annual Outlook process (collection, tracking, formatting, visualization, reporting) into a reproducible pipeline.
- **Ontology role:** Standardizes inputs and document metadata; maps contributors/roles, submission windows, and outputs; supports canonical identifiers for documents and links (FSAR/Tech/Research) from the Advice Trace.
- **Tangible outputs:**
  - Documented workflow (contributors, formats, roles, timelines, audiences).
  - Structured intake (survey/forms) to reduce email bloat; normalized JSON/CSV.
  - R / R Markdown build for Outlook tables, figures, and maps; publishable technical report with code/doc as a reproducible artifact.
- **Notes for critical path:** Provide Outlook _document_ and _link metadata_ (`:Document` nodes) so Advice Trace can surface authoritative downloads.

---

## Highest‑Impact Demo & Detailed Alternatives

### A) **FSAR Advice Trace (Hero Demo)** — highest leverage

- **Purpose and Proof Points:**  
  Demonstrates a transparent, reproducible chain of evidence for a single management unit (SMU) — specifically Barkley Sockeye — covering the end-to-end process from raw data to science advice publication. Surfaces **Evidence Completeness** for all required fields, **Data Currency** with version and timestamp pinning, risk assessments (e.g., where proxies are used without justification), and robust document linkage (FSAR, Technical Reports, Research references).
- **Why this matters:**  
  Targets both executive summary needs (at-a-glance completeness/risk state for decisions) and deep analyst drill-downs (trace to the underlying data, method, and provenance). Establishes a reusable JSON-LD exchange contract, a SPARQL query pack to support analytical completeness checks, and UI patterns that are readily transferable to other SMUs and regions.
- **Engineering/Scope**:  
  Requires mature competency queries, robust ontology-backed shapes, well-defined essential fields (per product requirements), and example/test datasets for demonstration. Envisions a timeline viewer and evidence-drawer UI backed by live SPARQL.

### B) Alternative Demo Paths (Enabling Decoupled Progress)

If A is blocked (e.g., due to missing data, stakeholder availability, excessive integration risk, or technical debt), these alternatives can deliver meaningful, scoped wins — each aligned with a critical ontology function. Details for each:

1. **SPSR Intake Assistant**

   - **Purpose:**  
     Provide survey authors/data stewards with instant feedback and guidance during data submission and validation.
   - **Key Features:**
     - Interactive validator for the SPSR Excel or CSV intake template.
     - SHACL-based rules auto-check structural and vocabulary constraints.
     - Inline “fix-hints” for common errors and omissions (e.g. missing method or invalid enumeration).
     - Dropdowns for controlled vocabularies driven by SKOS schemes in the ontology.
   - **Value:**  
     Demonstrates practical ontology use for data quality at the point of entry — reducing reviewer workload and flagging standardization issues early.

2. **GRD↔SPSR Join Explorer**

   - **Purpose:**  
     Illustrate how stable identifier schemes and the ontology’s relations enable automated joins between Genetics Results Database (GRD) and Survey Population Status Records (SPSR).
   - **Key Features:**
     - Browser or visualizer for linking Run_ID, Sample_ID, (optionally Assay_ID) across systems.
     - Surfaces GSI composition and confidence intervals, along with uncertainty flags (status confidence based on genetic signal strength, flagged exceptions).
     - Supports spot checks and data lineage verification.
   - **Value:**  
     Showcases the interoperability and trust-building capacity of standardized identifiers and relationship modeling.

3. **SILS→Narrative Prototype**

   - **Purpose:**  
     Prototype automating the generation and structuring of escapement narratives from raw stream inspection log data.
   - **Key Features:**
     - Demonstrates one stream’s workflow, transforming SILS records into a structured narrative bundle (with provenance and uncertainty properties linked).
     - Highlights the narrative “bundle” data model and how uncertainty/variance is represented for summary fields.
     - Supports attachment of provenance nodes (who, when, instrument used).
   - **Value:**  
     Validates the narrative bundle pattern and its fit for downstream FSAR compilation and reporting; surfaces gaps in SILS data capture.

4. **Decision‑Context Completeness Checker**
   - **Purpose:**  
     Deliver a lightweight, interactive checklist or widget for management decision contexts (e.g., TAC/HCR), assessing whether all required indicators and reference points are present for evidence-based management.
   - **Key Features:**
     - Drives the UI checklist from SHACL shapes and query definitions.
     - Summarizes completeness state (e.g., “Complete”, “Missing Critical”, “Gaps”) as seen in the FSAR advice trace, but tailored for policy/management reviewer needs.
     - Offers actionable output (download or report) for missing evidence.
   - **Value:**  
     Provides a fast feedback mechanism for decision support workflows, decoupling evidence validation from full advice chain integration.

---

**Dependency/Isolation Strategy:** The alternatives above are designed to (a) reuse the same underlying ontology modules (SHACL shapes, SKOS concepts, test queries), (b) surface code and contract artifacts that support extensibility, and (c) avoid coupling to the full FSAR evidence chain, so progress or demos on any path do not block others. Each can serve as a proving ground for critical ontology features while informing and de-risking the flagship FSAR Advice Trace demo.
