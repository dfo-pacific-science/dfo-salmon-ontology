# DFO Salmon Ontology - FSAR Tracer MVP Todo List

**Focus:** 8-week path to Barkley Sockeye FSAR evidence chain demo  
**Goal:** Six-node trace (Data → Method → RefPoints → Status → Advice → Decision) with badges

**Last Updated:** 2025-01-27  
**Status:** Active development for FSAR Advice Trace (2-month critical path)

**Important Notes:**

- **NO instance data in `ontology/dfo-salmon.ttl`** - Schema only; instances go in `ontology/examples/`
- **Brett's tasks** (marked with 🔧) are application/infrastructure work, not ontology development
- **Ontology tasks** focus on schema, classes, properties, SKOS schemes, and validation rules

---

## PR-000: Requirements and Design Review

**Priority:** Critical | **Scope:** Foundation and alignment

### Commit 0.1: Review and Refine FSAR Tracer PRD

- [ ] Review `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md` for completeness
- [ ] Clarify terminology: "Scientific Output" vs "Advice", "Decision" vs "DecisionContext"
- [ ] Finalize six-node evidence chain requirements
- [ ] Document required fields checklist (v1.0)
- [ ] Ensure alignment with SPSR data model

### Commit 0.2: Review Competency Questions

**File:** `docs/COMPETENCY_QUESTIONS.md`

- [ ] Review existing stock assessment competency questions
- [ ] Add FSAR Tracer-specific competency questions (Q1-Q9)
- [ ] Verify each question maps to ontology classes/properties
- [ ] Ensure questions cover all six evidence chain nodes
- [ ] Add genetics/GSI competency questions for GRD linkage

### Commit 0.3: Review Minh Doan's SIL/SEN PR

- [ ] Review Minh Doan's Stream Inspection Logs (SIL) terms
- [ ] Review Escapement Narratives (SEN) terms
- [ ] Identify SKOS concept schemes relevant to FSAR Tracer
- [ ] Map SIL/SEN enumeration methods to existing `:EnumerationMethodScheme`
- [ ] Document integration plan for SIL/SEN classes
- [ ] Prioritize SKOS schemes that benefit both FSAR Tracer and SIL/SEN work

---

## PR-001: BFO MIREOT Import and DwC Mapping

**Priority:** High | **Scope:** Upper ontology grounding via BFO

### Commit 1.1: Add BFO MIREOT Definitions

**File:** `ontology/dfo-salmon.ttl`

- [x] Keep BFO prefix declaration at line 2: `@prefix bfo: <http://purl.obolibrary.org/obo/BFO_>`
- [x] Add BFO MIREOT section after line 240
- [x] Import `bfo:0000015` (process) with label and oboInOwl:hasDefinition
- [x] Import `bfo:0000040` (material entity) with label and oboInOwl:hasDefinition
- [x] Import `bfo:0000031` (generically dependent continuant) with label and oboInOwl:hasDefinition
- [x] Add section comment: "Upper ontology grounding for process/entity/quality hierarchy"
- [ ] Test ontology loads in Protégé without errors

### Commit 1.2: Update DwC-to-BFO Mappings

**File:** `ontology/dfo-salmon.ttl`

- [x] Update lines 219-234 (Class Mappings section)
- [x] Change `dwc:Organism rdfs:subClassOf bfo:0000040` to use actual BFO class (not comment)
- [x] Change `dwc:Event rdfs:subClassOf bfo:0000015` to use actual BFO class
- [x] Change `dwc:MaterialEntity rdfs:subClassOf bfo:0000040`
- [x] Change `dwc:Agent rdfs:subClassOf bfo:0000040`
- [x] Update section title to "Class Mappings to Darwin Core and BFO Upper Ontology"
- [ ] Verify reasoning works with ELK reasoner

---

## PR-002: DQV MIREOT Import for Quality Framework

**Priority:** High | **Scope:** Evidence completeness and quality tracking

### Commit 2.1: Add DQV MIREOT Definitions

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add DQV prefix declaration at line 9: `@prefix dqv: <http://www.w3.org/ns/dqv#>`
- [ ] Add DQV MIREOT section after BFO section (~line 250)
- [ ] Import `dqv:Dimension` with rdfs:label and rdfs:comment
- [ ] Import `dqv:QualityAnnotation` with rdfs:label and rdfs:comment
- [ ] Import `dqv:inDimension` object property with rdfs:label and rdfs:comment
- [ ] Add rdfs:isDefinedBy for each term pointing to DQV namespace
- [ ] Test DQV terms are recognized in Protégé

### Commit 2.2: Create Evidence Completeness Dimensions

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add section comment: "Evidence Completeness Framework (DQV-based)"
- [ ] Create `dfo:EvidenceCompletenessDimension` as instance of `dqv:Dimension`
- [ ] Create `dfo:DataCurrencyDimension` as instance of `dqv:Dimension`
- [ ] Add skos:prefLabel and skos:definition for both dimensions
- [ ] Add rdfs:isDefinedBy for each dimension

### Commit 2.3: Create Quality Annotations (Evidence Badges)

**File:** `ontology/dfo-salmon.ttl`

- [ ] Create `dfo:CompleteEvidence` as `dqv:QualityAnnotation`
- [ ] Create `dfo:GapsEvidence` as `dqv:QualityAnnotation`
- [ ] Create `dfo:MissingCriticalEvidence` as `dqv:QualityAnnotation`
- [ ] Link each to `dfo:EvidenceCompletenessDimension` via `dqv:inDimension`
- [ ] Add skos:prefLabel for each badge (Complete, Gaps, Missing-Critical)
- [ ] Add rdfs:isDefinedBy for each annotation

---

## PR-003: FSAR Tracer Core Classes

**Priority:** High | **Scope:** Evidence chain ontology classes

### Commit 3.1: Add PROV-O Prefix and Documentation

**File:** `ontology/dfo-salmon.ttl`

- [ ] Verify PROV-O prefix exists at line 9: `@prefix prov: <http://www.w3.org/ns/prov#>`
- [ ] Add FSAR Tracer Provenance Pattern section after genetics classes (~line 1260)
- [ ] Add section comment explaining prefix-only approach (NO owl:imports)
- [ ] Document PROV-O usage pattern with examples:
  - `StatusAssessment prov:used Dataset`
  - `StatusAssessment prov:used ReferencePoint`
  - `StatusAssessment prov:wasGeneratedBy AnalysisMethod`
  - `StatusAssessment prov:wasAttributedTo Agent`
  - `ScientificOutput prov:wasDerivedFrom StatusAssessment`
  - `ManagementDecision prov:used ScientificOutput`

### Commit 3.2: Add FSAR Tracer Evidence Chain Classes

**File:** `ontology/dfo-salmon.ttl`

- [ ] Create "FSAR Tracer Evidence Chain Classes (MVP)" section after line 850
- [ ] Add `dfo:StatusAssessment` class
  - Set as subclass of `bfo:0000015` (process)
  - Add rdfs:label "Status Assessment"@en
  - Add rdfs:comment explaining stock status assessment relative to reference points
  - Add rdfs:isDefinedBy
- [ ] Add `dfo:ScientificOutput` class
  - Set as subclass of `iao:0000030` (information content entity)
  - Add rdfs:label "Scientific Output"@en
  - Add rdfs:comment explaining FSAR advice text, recommendations, summaries
  - Add rdfs:isDefinedBy
- [ ] Add `dfo:ManagementDecision` class
  - Set as subclass of `bfo:0000015` (process)
  - Add rdfs:label "Management Decision"@en
  - Add rdfs:comment explaining TAC/HCR/rebuilding decisions
  - Add rdfs:isDefinedBy
- [ ] Add `dfo:AnalysisMethod` class
  - Set as subclass of `bfo:0000015` (process)
  - Add rdfs:label "Analysis Method"@en
  - Add rdfs:comment explaining SR benchmark, run reconstruction methods
  - Add rdfs:isDefinedBy

---

## PR-004: Genetics Classes for GRD Integration

**Priority:** High | **Scope:** Link to Genetics Results Database

### Commit 4.1: Review Existing Genetics Classes

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review existing genetics classes (lines 885-923): GeneticSample, GSIRun, GSICompositionMeasurement, ReportingUnit, Assay, MarkerPanel, Protocol
- [ ] Document current genetics class limitations and gaps
- [ ] Verify properties link samples to survey events and stocks
- [ ] Check if `GSIRun` adequately models GRD run identifiers
- [ ] Verify `GSICompositionMeasurement` can link to FSAR Tracer data products

### Commit 4.2: Add GRD Linkage Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:grdRunID` DatatypeProperty for GRD Run_ID
- [ ] Add `dfo:grdSampleID` DatatypeProperty for GRD Sample_ID  
- [ ] Add `dfo:grdAssayID` DatatypeProperty for GRD Assay_ID (optional)
- [ ] Add `dfo:gsi_sample_size` DatatypeProperty for uncertainty tracking
- [ ] Add `dfo:gsi_ci` DatatypeProperty for confidence intervals
- [ ] Set appropriate domains and ranges
- [ ] Add comments explaining GRD integration

### Commit 4.3: Document Genetics-to-FSAR Linkage Pattern

**File:** `docs/CONVENTIONS.md`

- [ ] Add section 6.x "Genetics Results Database (GRD) Integration"
- [ ] Document how GSICompositionMeasurement links to StatusAssessment
- [ ] Explain Run_ID, Sample_ID, Assay_ID usage
- [ ] Add example pattern for GRD→SPSR→FSAR trace
- [ ] Document uncertainty propagation from GSI to status assessment

---

## PR-005: SIL/SEN SKOS Schemes Integration

**Priority:** High | **Scope:** Align with Minh Doan's escapement measurement work

### Commit 5.1: Integrate SIL Enumeration Methods

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review Minh Doan's enumeration method concepts
- [ ] Integrate missing concepts into `:EnumerationMethodScheme`
- [ ] Ensure all concepts have skos:prefLabel, skos:definition, skos:broader
- [ ] Add skos:inScheme links
- [ ] Verify no duplicate or conflicting concepts

### Commit 5.2: Integrate SEN Estimate Methods

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review Minh Doan's estimate method concepts
- [ ] Integrate missing concepts into `:EstimateMethodScheme`
- [ ] Ensure consistency with existing methods (AreaUnderTheCurve, PeakCountAnalysis, etc.)
- [ ] Add skos:prefLabel, skos:definition, skos:broader for all
- [ ] Verify scheme completeness

### Commit 5.3: Add SIL/SEN Classes (if needed)

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:StreamInspectionLog` class if not already present
- [ ] Add `dfo:EscapementNarrative` class if not already present
- [ ] Link to existing `dfo:EscapementSurveyEvent` hierarchy
- [ ] Add properties for SIL/SEN metadata
- [ ] Document relationship to EscapementMeasurement

---

## PR-006: FSAR Required Fields

**Priority:** High | **Scope:** Evidence completeness tracking properties

### Commit 6.1: Add Data Source Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Create "FSAR Tracer Required Fields (Evidence Completeness)" section (~line 1400)
- [ ] Add `dfo:data_source_type` DatatypeProperty
  - Set domain to `dfo:EscapementMeasurement`, range to `xsd:string`
  - Add label and comment explaining source types (direct, proxy, genetic proxy)
- [ ] Add `dfo:spawner_origin` DatatypeProperty
  - Set domain to `dfo:EscapementMeasurement`, range to `xsd:string`
  - Add comment explaining wild, hatchery, mixed origins
- [ ] Add `dfo:proxy_justification` DatatypeProperty
  - Set domain to `dfo:EscapementMeasurement`, range to `xsd:string`
  - Add comment: required when data_source_type contains "proxy"

### Commit 6.2: Add Method Reproducibility Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:method_name` DatatypeProperty
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
- [ ] Add `dfo:method_version` DatatypeProperty
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
- [ ] Add `dfo:code_commit` DatatypeProperty
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
  - Add comment: Git commit hash/tag for reproducibility

### Commit 6.3: Add Reference Point Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:reference_point_type` DatatypeProperty
  - Set range to `xsd:string`
  - Add comment: Sgen, USR, LRP, SMSY, etc.
- [ ] Add `dfo:benchmark_method` DatatypeProperty
  - Set range to `xsd:string`
  - Add comment: SR model, percentile, expert judgment
- [ ] Add `dfo:benchmark_sensitivity` DatatypeProperty
  - Set range to `xsd:boolean`
  - Add comment: flag indicating sensitivity to assumptions

### Commit 6.4: Add Status and Review Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:status_value` DatatypeProperty (if not exists)
  - Set range to `xsd:decimal`
  - Add comment: numeric status value
- [ ] Add `dfo:status_ci` DatatypeProperty
  - Set range to `xsd:decimal`
  - Add comment: confidence interval for status
- [ ] Add `dfo:reviewer` ObjectProperty
  - Set range to `dwc:Agent`
  - Add comment: person or committee who reviewed assessment
- [ ] Add `dfo:review_date` DatatypeProperty
  - Set range to `xsd:date`
  - Add comment: date of assessment review or decision

---

## PR-007: SHACL Shapes for Evidence Completeness

**Priority:** High | **Scope:** Validation rules

### Commit 7.1: Update SHACL File Header

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [ ] Add clarifying comment at top: "Validation shapes for data quality, NOT classification"
- [ ] Add note: "Estimate types are manually assigned based on Hyatt 1997 criteria"
- [ ] Add note: "No instance data in main ontology file; instances go in examples/"

### Commit 7.2: Create Decision Context Shape

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [ ] Create `dfo:TAC_HCR_DecisionShape` for TAC/HCR decision context
- [ ] List required fields as sh:property constraints:
  - `dfo:status_value` (sh:minCount 1)
  - `dfo:reference_point_type` (sh:minCount 1)
  - `dfo:method_name` (sh:minCount 1)
  - `dfo:reviewer` (sh:minCount 1)
  - `dfo:review_date` (sh:minCount 1)
- [ ] List optional fields (no minCount):
  - `dfo:status_ci`
  - `dfo:gsi_sample_size`
  - `dfo:benchmark_sensitivity`

### Commit 7.3: Add Conditional Validation Rules

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [ ] Create `dfo:ProxyJustificationShape`
  - Rule: IF data_source_type contains "proxy" THEN proxy_justification required
  - Add sh:message: "Proxy data sources must include justification"
- [ ] Create `dfo:MethodCompletenessShape`
  - Rule: AnalysisMethod must have name AND version AND code_commit
  - Add sh:message for each missing field
- [ ] Create `dfo:StatusReviewShape`
  - Rule: StatusAssessment must have reviewer AND review_date
  - Add sh:message: "Status assessments require reviewer and date"

### Commit 7.4: Add Provenance Validation

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [ ] Create `dfo:StatusProvenanceShape`
  - Require at least one prov:used link to Dataset
  - Require prov:wasGeneratedBy link to AnalysisMethod
  - Require prov:wasAttributedTo link to Agent
  - Add friendly error messages
- [ ] Create `dfo:AdviceProvenanceShape`
  - Require ScientificOutput has prov:wasDerivedFrom StatusAssessment
  - Require prov:wasAttributedTo for reviewer
  - Add friendly error messages

---

## PR-008: SPARQL Query Pack

**Priority:** High | **Scope:** Competency queries for UI

### Commit 8.1: Create Query File

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] Create new file for FSAR Tracer queries
- [ ] Add header with query pack version and date
- [ ] Add prefix declarations for all namespaces
- [ ] Add table of contents listing Q1-Q9

### Commit 8.2: Core Evidence Queries (Q1-Q4)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] Implement Q1: Evidence Completeness by Decision
  - Check required vs optional fields
  - Return state: Complete, Gaps, or Missing-Critical
- [ ] Implement Q2: Proxy Without Justification
  - Find records where data_source_type contains "proxy" but no proxy_justification
- [ ] Implement Q3: Method Reproducibility
  - Return method_name, method_version, code_commit
  - Flag if any missing
- [ ] Implement Q4: Reference Points Used
  - Return reference_point_type, benchmark_method, benchmark_sensitivity
  - List all reference points used in status assessment

### Commit 8.3: Data Currency and Quality Queries (Q5-Q8)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] Implement Q5: Missing Uncertainty
  - Find StatusAssessments without status_ci
  - Find GSIResults without gsi_sample_size or gsi_ci
- [ ] Implement Q6: Data Currency
  - Return last modified timestamp per component (Dataset, Method, ReferencePoint, Status, Advice)
  - Return version pins (owl:versionInfo)
  - Flag stale data (>12 months)
- [ ] Implement Q7: Scientific Output Text + Review
  - Return scientific_output_text, reviewer, review_date
- [ ] Implement Q8: Linked Documents
  - Return FSAR/Tech/Research document metadata
  - Include doc_type, title, identifier, issued date, URL

### Commit 8.4: Genetics Integration Query (Q9)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] Implement Q9: GRD Data Product Integration
  - Return GSIRun linked to StatusAssessment
  - Include grdRunID, grdSampleID, grdAssayID
  - Return GSICompositionMeasurement with CIs
  - Show linkage: GRD → Measurement → Status → Advice

---

## PR-009: Relations Ontology Alignment

**Priority:** Medium | **Scope:** Documentation only (no code changes for MVP)

### Commit 9.1: Document RO Alignment

**File:** `ontology/dfo-salmon.ttl`

- [ ] Update membership relations section comment (lines 1010-1020)
- [ ] Add note: "Aligned with RO:0002131 (has_member) and RO:0002350 (member_of)"
- [ ] Add note: "Implemented as independent properties to avoid RO import overhead"
- [ ] Add `rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002131>` to `dfo:hasMember`
- [ ] Add `rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002350>` to `dfo:isMemberOf`
- [ ] Update comment explaining semantic alignment without import

---

## PR-010: Documentation Updates

**Priority:** High | **Scope:** README and CONVENTIONS

### Commit 10.1: Update CONVENTIONS.md Import Policy

**File:** `docs/CONVENTIONS.md`

- [ ] Add new section 2.3.6 "Ontology Import Strategy"
- [ ] Document three approaches: Full import, MIREOT, Prefix only
- [ ] Add decision matrix table (BFO, IAO, DQV, PROV-O, RO, DPROD, SKOS, DwC)
- [ ] Explain when to use each approach with examples
- [ ] Add FSAR Tracer import decisions and rationale
- [ ] Document MIREOT implementation pattern

### Commit 10.2: Add FSAR Tracer Patterns to CONVENTIONS

**File:** `docs/CONVENTIONS.md`

- [ ] Add section "FSAR Tracer Evidence Chain Pattern"
- [ ] Document six-node chain: Data → Method → RefPoints → Status → Advice → Decision
- [ ] Show PROV-O property usage examples
- [ ] Explain DQV quality annotation pattern
- [ ] Document required fields for evidence completeness

### Commit 10.3: Update README.md Technical Overview

**File:** `README.md`

- [ ] Update Technical Overview section (lines 67-75)
- [ ] Add: "Pragmatic imports: MIREOT for BFO/IAO/DQV (~12 terms)"
- [ ] Add: "Upper ontology: BFO grounding for process/entity hierarchy"
- [ ] Add: "Provenance: PROV-O properties for FSAR evidence chains"
- [ ] Add: "Quality: DQV dimensions for evidence completeness tracking"

### Commit 10.4: Add FSAR Tracer Section to README

**File:** `README.md`

- [ ] Add FSAR Tracer subsection to Ontology Scope (after line 130)
- [ ] List core classes: StatusAssessment, ScientificOutput, ManagementDecision, AnalysisMethod
- [ ] List PROV-O properties used
- [ ] List DQV dimensions and quality annotations
- [ ] List required fields for evidence completeness
- [ ] Note: No instance data in main ontology file

---

## PR-011: Sample Data and JSON-LD Export

**Priority:** Medium | **Scope:** Example instances for testing (NOT in main ontology)

### Commit 11.1: Create Barkley Sockeye Sample Instances

**File:** `ontology/examples/barkley-2025-sample.ttl` (NEW FILE)

- [ ] Create sample `dfo:EscapementMeasurement` for Barkley 2025
  - Include data_source_type, spawner_origin
  - Link to Stock using dfo:aboutStock
  - Link to SurveyEvent using dfo:observedDuring
- [ ] Create sample `dfo:AnalysisMethod` (SR benchmark)
  - Include method_name, method_version, code_commit
- [ ] Create sample `dfo:ReferencePoint` (Sgen)
  - Include reference_point_type, benchmark_method
- [ ] Create sample `dfo:StatusAssessment` for Barkley 2025
  - Include status_value, status_ci, reviewer, review_date
- [ ] Create sample `dfo:ScientificOutput` (FSAR advice)
- [ ] Create sample `dfo:ManagementDecision` (TAC 2025)

### Commit 11.2: Link Instances with PROV-O

**File:** `ontology/examples/barkley-2025-sample.ttl`

- [ ] Link StatusAssessment to EscapementMeasurement via `prov:used`
- [ ] Link StatusAssessment to ReferencePoint via `prov:used`
- [ ] Link StatusAssessment to AnalysisMethod via `prov:wasGeneratedBy`
- [ ] Link StatusAssessment to Agent via `prov:wasAttributedTo`
- [ ] Link ScientificOutput to StatusAssessment via `prov:wasDerivedFrom`
- [ ] Link ManagementDecision to ScientificOutput via `prov:used`

### Commit 11.3: Annotate with DQV Quality

**File:** `ontology/examples/barkley-2025-sample.ttl`

- [ ] Add `dqv:hasQualityAnnotation` to StatusAssessment
- [ ] Link to `dfo:CompleteEvidence` annotation
- [ ] Add data currency timestamps using `dcterms:modified`
- [ ] Add version pins using `owl:versionInfo`
- [ ] Document quality annotation pattern in comments

### Commit 11.4: Create JSON-LD Context

**File:** `ontology/examples/fsar-tracer-context.jsonld` (NEW FILE)

- [ ] Create @context with all FSAR Tracer prefixes
- [ ] Map dfo, prov, dqv, bfo, iao, dwc, skos, dcterms, schema namespaces
- [ ] Define short aliases for common properties
- [ ] Add @vocab for default namespace
- [ ] Test context validates with JSON-LD playground

### Commit 11.5: Export Sample Data as JSON-LD

**File:** `ontology/examples/barkley-2025-sample.jsonld` (NEW FILE)

- [ ] Export Barkley sample as JSON-LD using context
- [ ] Validate JSON-LD syntax
- [ ] Document export process in README
- [ ] Add note: This is example data for testing, not production

---

## 🔧 Brett's Tasks (Application/Infrastructure - Not Ontology)

**Note:** These are outside the scope of ontology development but necessary for FSAR Tracer

### Task B.1: Graph Database Setup

- [ ] 🔧 Install Docker Desktop
- [ ] 🔧 Pull Apache Jena Fuseki Docker image
- [ ] 🔧 Create docker-compose.yml for Fuseki
- [ ] 🔧 Start Fuseki container
- [ ] 🔧 Create graphs: `graph:vocab`, `graph:shapes`, `graph:fsar:2025:barkley`
- [ ] 🔧 Test Fuseki UI accessible at http://localhost:3030

### Task B.2: Load Ontology into Fuseki

- [ ] 🔧 Load `ontology/dfo-salmon.ttl` into `graph:vocab`
- [ ] 🔧 Load `ontology/shapes/dfo-salmon-shapes.ttl` into `graph:shapes`
- [ ] 🔧 Load `ontology/examples/barkley-2025-sample.ttl` into `graph:fsar:2025:barkley`
- [ ] 🔧 Verify data loaded correctly via SPARQL query

### Task B.3: SHACL Validation in Fuseki

- [ ] 🔧 Run SHACL validation against Barkley sample data
- [ ] 🔧 Review validation report for errors
- [ ] 🔧 Fix any data quality issues
- [ ] 🔧 Document validation process

### Task B.4: Run SPARQL Queries

- [ ] 🔧 Execute Q1-Q9 from query pack against Barkley data
- [ ] 🔧 Verify queries return expected results
- [ ] 🔧 Document query results
- [ ] 🔧 Create query performance benchmarks

### Task B.5: Django HTMX Interface (Weeks 5-8)

- [ ] 🔧 Set up Django project structure
- [ ] 🔧 Create HTMX timeline view for six-node trace
- [ ] 🔧 Implement Evidence Drawer UI component
- [ ] 🔧 Connect to Fuseki via SPARQL adapter
- [ ] 🔧 Implement evidence badges calculation
- [ ] 🔧 Add document linking functionality
- [ ] 🔧 Create Advice Trace Pack export

---

## PR-012: W3ID URI Publication

**Priority:** Medium | **Scope:** Persistent identifiers

### Commit 12.1: Prepare W3ID Request

- [ ] Review W3ID.org submission guidelines
- [ ] Prepare .htaccess file for content negotiation
- [ ] Document redirection rules for ontology versions
- [ ] Create README for w3id.org/dfo/salmon
- [ ] Test redirection locally

### Commit 12.2: Submit W3ID Request

- [ ] Fork w3id.org GitHub repository
- [ ] Add dfo/salmon directory with configuration
- [ ] Submit pull request to w3id.org
- [ ] Respond to reviewer feedback
- [ ] Monitor PR for merge

### Commit 12.3: Update Ontology IRIs Post-Publication

- [ ] Update ontology IRI to use w3id.org
- [ ] Update version IRI to use w3id.org
- [ ] Update rdfs:isDefinedBy for all terms
- [ ] Test that all IRIs resolve correctly
- [ ] Document w3id.org usage in README

---

## Deferred to Post-MVP

### DPROD Investigation

- [ ] Investigate DPROD namespace resolution (`https://www.omg.org/spec/DPROD/1.0/`)
- [ ] Compare DPROD vs dcat:Dataset + schema:Dataset
- [ ] Decide on data product modeling approach
- [ ] Document DPROD integration plan if adopted
- [ ] Update FSAR Tracer to use DPROD if beneficial

### Full RO Integration

- [ ] Create subproperties of RO relations
- [ ] Import RO terms via MIREOT or prefix
- [ ] Test reasoning with RO alignment
- [ ] Update all membership relations to use RO subproperties

### Estimate Type Automated Assignment

- [ ] Review Hyatt 1997 criteria automation requirements
- [ ] Create decision tree for automated type assignment
- [ ] Implement SHACL rules for automated classification
- [ ] Test classification accuracy with historical data

### Multi-SMU Support

- [ ] Extend sample data beyond Barkley
- [ ] Test SPARQL queries across multiple SMUs
- [ ] Add SMU/CU/Stock hierarchy instances
- [ ] Document multi-SMU patterns

---

## Import Strategy Decision Matrix

| Ontology | Approach    | Terms Used                                                            | Rationale                        |
| -------- | ----------- | --------------------------------------------------------------------- | -------------------------------- |
| BFO      | MIREOT      | 3 (process, material entity, generically dependent continuant)        | Upper ontology grounding         |
| IAO      | MIREOT      | 4 (measurement datum, value spec, information entity, directive)      | Information artifacts            |
| DQV      | MIREOT      | 5 (Dimension, QualityAnnotation, inDimension, Metric, Category)       | Evidence completeness            |
| PROV-O   | Prefix only | ~6 properties (wasGeneratedBy, wasDerivedFrom, used, wasAttributedTo) | Provenance relations             |
| RO       | Prefix only | Alignment via rdfs:seeAlso                                            | Semantic alignment documentation |
| DPROD    | Defer       | TBD                                                                   | Investigate post-MVP             |
| SKOS     | Prefix only | Extensive (schemes, concepts)                                         | Core W3C vocab                   |
| DwC      | Prefix only | Extensive (classes, properties)                                       | Biodiversity standard            |

---

## Why MIREOT vs Full Import

**Full owl:imports** (NOT used in FSAR Tracer MVP)

- Use ONLY when: Using >20 terms AND need reasoning over imported axioms
- Risk: Imports entire ontology (100s-1000s of terms); slow loading; potential conflicts

**MIREOT (Minimum Information to Reference an External Ontology Term)**

- Use when: Need 3-20 specific terms with labels/definitions
- Method: Copy term IRI, label, definition into our ontology
- Benefits: Lightweight; no import bloat; clear documentation

**Prefix declarations only**

- Use when: Using properties only OR terms are universally known
- Method: Declare prefix; use terms directly; no local definitions
- Benefits: Minimal overhead; assumes external ontology is accessible

---

## Key Decisions

- **Import strategy:** MIREOT for BFO/IAO/DQV; prefix-only for PROV-O/RO
- **BFO decision:** Keep and use properly via MIREOT; provides upper ontology grounding
- **DPROD decision:** Defer to post-MVP; use schema:Dataset for now
- **RO decision:** Document alignment but don't create subproperties yet
- **Instance data:** NO instances in main ontology file; all examples go in `ontology/examples/`
- **Genetics:** Review and extend existing classes for GRD linkage
- **SIL/SEN:** Integrate Minh Doan's SKOS schemes and classes
- **Focus:** Shortest path to working FSAR Tracer demo for Barkley Sockeye
