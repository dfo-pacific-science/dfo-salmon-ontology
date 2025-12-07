# Completed Tasks — DFO Salmon Ontology

## 2025-11-02 — Convention Compliance Cleanup

- [x] Add missing `rdfs:label` annotations to OWL classes, object properties, and datatype properties.
- [x] Reinstate required `IAO:0000115` definitions for COSEWIC statuses, `:DowngradeCriteria`, and imported SKOS upper classes.
- [x] Replace `skos:altLabel` IRIs with `skos:exactMatch` or `rdfs:seeAlso` alignments and document intentional punning patterns.

## Requirements and Design Review

**Owner:** Brett  
**Priority:** Critical  
**Scope:** Foundation and alignment

### Review and Refine FSAR Tracer PRD

- [x] Review `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md` for completeness
- [x] Clarify terminology: "Scientific Output" vs "Advice", "Decision" vs "DecisionContext"
- [x] Finalize evidence chain requirements
- [x] Document required fields checklist (v1.0)
- [x] Ensure alignment with SPSR data model
- [x] Comprehensive PRD update with personas, user stories, acceptance criteria, competency questions, schema recommendations, and MVP enhancements

### Review Competency Questions

**File:** `docs/COMPETENCY_QUESTIONS.md`

- [x] Review existing stock assessment competency questions
- [x] Add FSAR Tracer-specific competency questions (Q1-Q9)
- [x] Verify each question maps to ontology classes/properties
- [x] Ensure questions cover all evidence chain nodes
- [x] Add genetics/GSI competency questions for GRD linkage

## DQV MIREOT Import for Quality Framework

**Owner:** Mel  
**Priority:** High  
**Scope:** Evidence completeness and quality tracking

### Add DQV MIREOT Definitions

- [x] **VERIFIED**: DQV prefix declaration exists at line 9: `@prefix dqv: <http://www.w3.org/ns/dqv#>`
- [x] **VERIFIED**: DQV MIREOT section exists after BFO section (lines 415-440)
- [x] **VERIFIED**: Imported `dqv:Dimension` with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Imported `dqv:QualityAnnotation` with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Imported `dqv:inDimension` object property with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each term pointing to DQV namespace
- [x] DQV terms are recognized in Protégé

### Create Evidence Completeness Dimensions

- [x] **VERIFIED**: Section comment exists: "Evidence Completeness Framework (DQV-based)"
- [x] **VERIFIED**: Created `dfoc:EvidenceCompletenessDimension` as instance of `dqv:Dimension` (line 823)
- [x] **VERIFIED**: Created `dfoc:DataCurrencyDimension` as instance of `dqv:Dimension` (line 828)
- [x] **VERIFIED**: Added skos:prefLabel and skos:definition for both dimensions
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each dimension

### Create Quality Annotations (Evidence Badges)

- [x] **VERIFIED**: Created `dfoc:CompleteEvidence` as `dqv:QualityAnnotation` (line 833)
- [x] **VERIFIED**: Created `dfoc:GapsEvidence` as `dqv:QualityAnnotation` (line 839)
- [x] **VERIFIED**: Created `dfoc:MissingCriticalEvidence` as `dqv:QualityAnnotation` (line 845)
- [x] **VERIFIED**: Linked each to `dfoc:EvidenceCompletenessDimension` via `dqv:inDimension`
- [x] **VERIFIED**: Added skos:prefLabel for each badge (Complete, Gaps, Missing-Critical)
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each annotation

## SHACL Header and Documentation

**Owner:** Mel  
**Priority:** High  
**Scope:** SHACL validation setup

### Update SHACL File Header

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [x] Add clarifying comment at top: "Validation shapes for data quality, NOT classification"
- [x] Add note: "Estimate types are manually assigned based on Hyatt 1997 criteria"
- [x] Add note: "No instance data in main ontology file; instances go in examples/"

## CI/CD Workflow Consolidation (2025-11-25)

- [x] Consolidated workflows from 4 to 2 (merged ci.yml and ontology-quality.yml)
- [x] Removed generate-term-tables.yml (moved to pre-commit hook)
- [x] Fixed release.yml (replaced deprecated actions, standardized ROBOT version)
- [x] Implemented pre-commit hook for ontology validation
- [x] Standardized ROBOT version to v1.9.8 across all workflows

