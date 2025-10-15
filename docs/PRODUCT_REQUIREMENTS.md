Overview & Phased Plan — Five Projects Driving the DFO Salmon Ontology

The DFO Salmon Ontology initiative supports five major data integration and decision-support streams. Each stream provides both use cases (what the ontology enables) and requirements (what it must represent). The ontology program is structured into two phases — MVP (3 months) and Phase 2 (6 months) — to deliver tangible value quickly while building toward long-term interoperability.

Five Core Project Streams
1) Salmon Population Summary Repository (SPSR)

Purpose: Centralized database and web app for standardized reuse of data from Fisheries Science Reports (FSRs).
Ontology Role: Defines shared terms for population metrics, reference points, spawner origins, and benchmark methods. Enables automated validation of data submissions through the SPSR Intake Assistant.
Tangible output: Excel template + SHACL + R validator ensuring metadata consistency, provenance, and crosswalk compliance.

2) Genetics Results Database (GRD)

Purpose: Repository of genetic assignment results (docID outputs) from molecular labs.
Ontology Role: Provides consistent identifiers (Run_ID, Sample_ID, Assay_ID) and relationships linking genetic results to stock assessments and SPSR records. Supports uncertainty capture and future propagation of GSI composition error.
Tangible output: Join specification (ADR-001) and GRD→SPSR mapping schema.

3) Stream Inspection Logs & Escapement Narratives (SILS/Narratives)

Purpose: Standardize and automate the generation of escapement narratives from individual stream inspections.
Ontology Role: Describes how inspections combine into narratives, tracks sampling variation, uncertainty, and methods used. Connects field observations to population summaries and validation of derived metrics.
Tangible output: Data model + provenance pattern for narrative bundles (Phase 2).

4) Fisheries Science Advice Reports (FSAR/FSR Reviews)

Purpose: Deliver evidence-based status and trend assessments.
Ontology Role: Encodes reference points, benchmarks, and data provenance used in advice. Enables traceability from datasets to published advice figures.
Tangible output: Standard CQs for benchmark methods, proxy usage, and advice reproducibility (Phase 2).

5) Decision Contexts for Management

Purpose: Support management decisions (e.g., TAC/HCR triggers, rebuilding plans) that depend on consistent indicators and reference points.
Ontology Role: Provides a lightweight decision model linking goals, objectives, indicators, and reference points, allowing completeness checks for advice.
Tangible output: Decision-context completeness queries (Phase 2).

Phased Development Plan
Phase 1 — MVP (0–3 months) → Operational foundation

Deliver SPSR Intake Assistant (Excel + SHACL + R validator)

Publish core vocabularies (spawner_origin, data_source_type, reference_point_type, benchmark_method, benchmark_sensitivity)

Release CU↔SMU crosswalk (SKOS + CSV + rationale/version)

Implement 3 SPARQL queries (proxy justification, benchmark method, spawner origin summary)

Define join key ADR-001 for GRD↔SPSR (Run_ID + Sample_ID)

Phase 2 — Extended (3–6 months) → Interoperability and reasoning

Add SILS→Narrative bundle metadata model (inputs, methods, uncertainty)

Encode reference-point derivation (CU LBM → SMU LRP)

Implement decision-context completeness checks

Add uncertainty propagation pattern for GRD→SPSR integration

Pilot advice trace demo (data → status → advice → decision)

Strategic Fit

The ontology links operational databases (SPSR, GRD, SILS) with science-advice workflows, ensuring that data definitions, provenance, and cross-system relationships are consistent, traceable, and machine-readable. Each phase yields deliverables that biologists, analysts, and managers can directly use — from intake validation (Phase 1) to reproducible advice and decision transparency (Phase 2).

Competency Questions — DFO Salmon Ontology MVP (v0.1)

Scope: Questions the MVP must answer across SPSR (hero), GRD, and SILS→Narratives, plus near-term (v0.3) questions. Each item lists required fields/terms and whether it’s answerable Now (v0.1) or Next (v0.3).

A) Terminology, Validation, and Provenance

Where are spawner_origin values used inconsistently (e.g., wild vs unmarked)?
Needs: spawner_origin (SKOS), template validation (SHACL). Now

Which records use a proxy (e.g., mainstem index, GSI) without a proxy_justification?
Needs: data_source_type, proxy_justification. Now

For each record derived from GSI, is an uncertainty metric present (e.g., gsi_sample_size, gsi_confidence_interval)?
Needs: data_source_type=genetic_proxy, gsi_sample_size, gsi_confidence_interval. Now

Which assessments/narratives lack minimum provenance (data sources,