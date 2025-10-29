# Ontology Requirements — DFO Salmon Ontology

**Purpose of this document**  
Define the _impetus_ and product-context for the DFO Salmon Ontology, identify and align several ongoing projects that will leverage the ontology.

**North‑star demo (highest impact):** **FSAR Advice Trace** for one SMU (Barkley Sockeye) — a transparent chain from **Data → Method → Reference Points → Status → Advice → Decision Context**, with evidence completeness, data‑currency pins, risk chips, and links to FSAR/Tech/Research documents.

---

## Core Project Streams

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
- **Ontology role:** Narrative bundle pattern (SILS→SEN), provenance and uncertainty properties, linkage to SPSR population summaries, linkage to NuSEDS (historical salmon escapement database)
- **Tangible output:** Narrative bundle data model + provenance pattern (Phase 2) and validator hooks. 

### 4) Fisheries Science Advice Reports (FSAR / FSR Reviews)

- **Purpose:** Deliver evidence‑based status/trend assessments.
- **Ontology role:** Encode reference points, benchmark methods, and provenance of advice; enable trace from field methods → datasets → code → analytical methods → figures → advice reports → management decisions → legal and policy requirements and mandatte context. Integration with SPSR data schema
- **Tangible output:** Competency questions, SPARQL pack, **Advice Trace** UI components.

### 5) Decision Contexts for Management

- **Purpose:** Enable linkage of project proposals by scientists to DFO mandate, management requirements etc. Support management decisions (TAC/HCR, rebuilding) with consistent indicators and reference points.
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

### 8) AI and LLM supported Data Integration and Standardization and Knowledge Graph Upserting (Long term goal)

- **Purpose:** Make it easy for DFO staff to standardize their data, integrate their data from various external sources, or even upload data to the DFO Knowledge Graph.
- **Ontology Role:** Ingest context about non-standard data files, as well as the data files, and map them to DFO ontology concepts, classes etc. interactively with the user to ensure mappings make sense. Serve as a mediation layer between source datasystems within DFO. Facilitate plain language queries to the DFO Salmon Knowledge Graph.
- **Tangible Outputs:** DFO data integration tool and UI that enables easier data translation and graph insertion and plain language queries of the knowledge graph. Ability to import context and access MCP server with important DFO context and data.

### 9) Serve as the DFO specific salmon ontology and integrate with the broader salmon Domain Ontology hosted by NCEAS (at a later phase)
---

