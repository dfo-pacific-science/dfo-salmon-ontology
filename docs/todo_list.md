# DFO Salmon Ontology

**Focus:** 8-week path to Barkley Sockeye FSAR evidence chain demo  

**Status:** Active development for FSAR Advice Trace (2-month critical path)

**Current Goals:**
- **Widoco site formally published:** End of November 2025
- **Quarto website pages for exploring controlled vocabulary:** Working within next 2 weeks
- **New:** Complete ontology deep review (class hierarchy sanity + genetics vocab refresh) before further term publication

- **Upcoming:** Run `execplan-add-spsr-terms.md` after column-to-ontology mapping is approved (do not run yet) /Users/brettjohnson/code/dfo-salmon-ontology/docs/notes/spsr-column-to-ontology-mapping.md



## 2025-12-17 — I-ADOPT compound variables (planning / doc-only now)
- [ ] Audit compound variable/metric terms currently modeled as OWL classes; list candidates to refactor as SKOS concepts with I-ADOPT annotations (variable, property, entity/object-of-interest, constraints, variable set).
- [ ] Draft the annotation properties to carry I-ADOPT decomposition on SKOS concepts (iadoptProperty, iadoptEntity, iadoptConstraint, iadoptVariableSet) and propose ranges/usage in notes; do **not** change `ontology/dfo-salmon.ttl` yet.
- [ ] Propose I-ADOPT decompositions for a starter set of WSP/indicator metrics and capture in notes for future TTL updates.
- [ ] Align delimiter guidance for multiple constraints with SDP (`constraint_iri` uses `;`-separated IRIs in one cell) and reflect in ontology docs when updated.

## 2025-12-08 — Repo-wide QA findings

- [ ] Fix ThemeScheme alignment: replace out-of-scheme theme values and assign valid themes for terms flagged in theme coverage reports (e.g., Stock, ConservationUnit, EscapementMeasurement, WSP classes). Run `make theme-coverage` to generate the report.
- [x] Add missing theme annotations in `ontology/dfo-salmon.ttl` to clear coverage check (publicationStatus is currently not in use).

## 2025-12-08 — Exploitation / Mortality / Abundance quick wins

- [x] Add `gcdfo:TotalExploitationRate` subclass under `gcdfo:ExploitationRate` (draft ontology).
- [x] Relabel `gcdfo:IndicatorStream` to primary label “Indicator river” with altLabel “Indicator stream”.
- [ ] Decide on `harvest rate` altLabel vs. distinct term treatment for exploitation rate.
- [ ] Design brood-year vs. catch-year total abundance pattern and brood-year recruitment specialization.
- [ ] Extend mapping to cover age-specific fishing mortality and catch-year total abundance (currently missing).

## 2025-12-08 — Deferred modeling follow-ups (post-0.1.0)

- [ ] Choose pattern for age-specific fishing mortality (attribute vs. subclass) and implement in 0.2.0.
- [ ] Add explicit catch-year total abundance subclass if the selected pattern requires it (0.2.0).
- [ ] Add brood-year recruitment subclass only if queries/shapes need it (0.2.0).
- [ ] When human-curated sources are available, populate `IAO_0000119`/`dcterms:source` for the PublishReady items that are currently intentionally blank (do not invent sources).

## DwC-CM / SOSA alignment and assertion wrapper (review before implementation)

- [ ] Decide whether to introduce `dwc:Assertion` / `gcdfo:SalmonAssessmentAssertion` wrappers around IAO measurement data; define properties like `gcdfo:assertsValue`, `gcdfo:aboutOccurrence`, `gcdfo:basedOnEvent` if adopted.
- [ ] Choose feature-of-interest layering: Observation → Occurrence → Organism vs Observation → stratum (CU/SMU/PFMA), and whether to add population classes (e.g., `gcdfo:PopulationInSpaceTime`, `gcdfo:CURealizedPopulation`) with `gcdfo:realizesStratum`.
- [ ] Set a convention for SKOS vs OWL punning (e.g., `HatcheryOrigin`, `NaturalOrigin`, `DowngradeCriteria`) to avoid inconsistent hybrids.
- [ ] Align SOSA with existing DwC mapping (e.g., `sosa:Observation ⊑ dwc:Event`, FOI choices including Occurrence vs stratum).
- [x] Decide and document the decomposition metamodel stack (DwC-CM primary, SOSA overlay, OBOE alignment via annotations) and apply it consistently in mappings.


## Term Table Automation

**Owner:** Brett  **Priority:** High  **Scope:** Generate and surface ontology term tables with provenance

### Extraction Pipeline

- [ ] GitHub workflow to generate term tables (not present; needs creation)
- [ ] Create virtual environment and install `scripts/requirements.txt` dependencies (local development)
- [ ] Run `python scripts/extract-term-tables.py` to publish initial CSV + metadata (blocked until Java/ROBOT available for publish slice)
- [x] Decide whether to version generated CSVs or rely solely on workflow artifacts (decision: versioned under `release/artifacts/term-tables/`)
- [x] Expand `scripts/config/themes.yml` to all 9 themes aligned to draft ontology
- [x] Add Makefile target to chain publish slice + extraction (`make publish-and-extract`)
- [x] Add Makefile target to clean publish temp artifacts (`make publish-clean`)
- [x] Add Makefile target to sync term tables into DSU submodule (`make dsu-sync-term-tables`; set `DSU_ONTOLOGY_DIR` as needed)

### Cross-Repo Automation

- [ ] Provision `REPO_DISPATCH_TOKEN` with `repo` scope for GitHub dispatch events
- [ ] Coordinate with documentation repo to consume workflow artifacts or submodule updates
- [ ] Add Widoco build step and update `widoco_base_url` once docs are hosted
- **GOAL**: Widoco site formally published by end of November 2025
- **GOAL**: Quarto website pages for exploring controlled vocabulary working within next 2 weeks

## Theme / Module Annotations (Conventions alignment)

- [] Define an annotation property for themes/modules (e.g., `gcdfo:theme`) in `ontology/dfo-salmon.ttl` with range constrained to a SKOS Theme scheme (values from `docs/context/themes-modules.md`, see `execplan-theme-annotations.md`)
- [] Create a SKOS concept scheme for themes/modules and document intended values
- [] Apply the theme annotation to every OWL class, property, and SKOS concept (1–3 themes per term; at least one required)
- [x] Add a ROBOT/SPARQL or SHACL check (e.g., `scripts/sparql/theme-coverage.rq` + Make target) that fails when any term lacks `dfoc:theme` or exceeds 3 values
- [x] Add documentation examples and reviewer checklist to `docs/CONVENTIONS.md`

- [ ] Wire `scripts/sparql/theme-coverage.rq` into CI/pre-commit once Java/ROBOT is available locally






## 2025-11-06 — FSAR Advice Trace Mockups

- [x] Build dark-themed progressive-disclosure mockup (`docs/ontology_applications/mockups/fsar-tracer-mockup.html`)
- [ ] Socialize the interaction flow with FSAR authors + policy reviewers and capture feedback deltas
- [ ] Replace the static sample data with a JSON-LD Advice Trace Pack feed once available
- [ ] Wire drawer tabs to live SPSR/GRD/CSAS endpoints or cached packs for provenance jumps
- [ ] Incorporate a Management Decision snapshot node in the Advice Trace flow (type/date/link) per updated PRD

---

## DFO Organizational Structure

**Owner:** Mel  
**Priority:** Medium  
**Scope:** Organizational hierarchy classes and properties

### Add ORG Ontology MIREOT and DFO Organizational Classes

**File:** `ontology/dfo-salmon.ttl`

- [x] **VERIFIED**: ORG prefix declaration exists: `@prefix org: <http://www.w3.org/ns/org#>`
- [x] **VERIFIED**: ORG MIREOT section exists with key terms (lines 621-643): `org:Organization`, `org:OrganizationalUnit`, `org:hasUnit`, `org:hasSubOrganization`
- [x] **VERIFIED**: DFO-specific organizational classes exist as subclasses of `org:OrganizationalUnit`:
  - `dfoc:Unit` (line 649, rdfs:subClassOf org:OrganizationalUnit)
  - `dfoc:Section` (line 657), `dfoc:Division` (line 664), `dfoc:Branch` (line 671), `dfoc:Region` (line 678), `dfoc:Sector` (line 685) - all subclasses of org:OrganizationalUnit
- [x] **VERIFIED**: Added comprehensive rdfs:label and rdfs:comment for each DFO class
- [x] **VERIFIED**: Added rdfs:isDefinedBy for all classes

### Add DFO-Specific Organizational Properties

**File:** `ontology/dfo-salmon.ttl`

- [x] **VERIFIED**: DFO-specific organizational properties exist as subproperties of ORG:
  - `dfoc:hasUnit` (line 692, rdfs:subPropertyOf org:hasUnit)
  - `dfoc:hasSection` (line 701, rdfs:subPropertyOf org:hasSubOrganization)
  - `dfoc:hasDivision` (line 710, rdfs:subPropertyOf org:hasSubOrganization)
  - `dfoc:hasBranch` (line 719, rdfs:subPropertyOf org:hasSubOrganization)
  - `dfoc:hasRegion` (line 728, rdfs:subPropertyOf org:hasSubOrganization)
  - `dfoc:hasSector` (line 737, rdfs:subPropertyOf org:hasSubOrganization)
- [x] **VERIFIED**: Set appropriate domains and ranges for each DFO property
- [ ] Add organizational metadata properties: `dfoc:organizationalUnitName`, `dfoc:organizationalUnitCode`
- [ ] Document ORG alignment in comments

### Add Project Class and Linkage Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:Project` class as subclass of `bfo:0000015` (process)
- [ ] Add `dfo:managedBy` property linking Project to Unit
- [ ] Add `dfo:collaboratesWith` symmetric property for cross-cutting collaborations
- [ ] Add inverse `dfo:manages` property
- [ ] Add basic project properties: `dfo:projectTitle`, `dfo:projectFirstYear`, `dfo:projectLastYear`

### Update CONVENTIONS.md

**File:** `docs/CONVENTIONS.md`

- [ ] Add section documenting ORG ontology integration approach
- [ ] Document DFO-specific organizational hierarchy pattern using ORG subclasses
- [ ] Document project cross-cutting collaboration pattern
- [ ] Add examples of organizational structure modeling with ORG alignment
- [ ] Add note about Program = Unit synonymy

### Create Example Organizational Structure

**File:** `ontology/examples/dfo-org-structure-example.ttl` (NEW FILE)

- [ ] Create example instances of organizational hierarchy (schema only in main file)
- [ ] Show Unit → Section → Division → Branch → Region → Sector relationships
- [ ] Create example project instances with organizational linkages
- [ ] Document that these are examples, not production data

---

## SIL/SEN Integration Review

**Owner:** Mel + Minh Doan  
**Priority:** High  
**Scope:** Align with Minh Doan's escapement measurement work

### Review Minh Doan's SIL/SEN PR

- [ ] Review Minh Doan's Stream Inspection Logs (SIL) terms
- [ ] Review Escapement Narratives (SEN) terms
- [ ] Identify SKOS concept schemes relevant to FSAR Tracer
- [ ] Map SIL/SEN enumeration methods to existing `:EnumerationMethodScheme`
- [ ] Document integration plan for SIL/SEN classes
- [ ] Prioritize SKOS schemes that benefit both FSAR Tracer and SIL/SEN work

---

## DONE BFO MIREOT Import and DwC Mapping

**Owner:** Brett  
**Priority:** High  
**Scope:** Upper ontology grounding via BFO

### Add BFO MIREOT Definitions

**File:** `ontology/dfo-salmon.ttl`

- [x] Keep BFO prefix declaration at line 2: `@prefix bfo: <http://purl.obolibrary.org/obo/BFO_>`
- [x] Add BFO MIREOT section after line 240
- [x] Import `bfo:0000015` (process) with label and oboInOwl:hasDefinition
- [x] Import `bfo:0000040` (material entity) with label and oboInOwl:hasDefinition
- [x] Import `bfo:0000031` (generically dependent continuant) with label and oboInOwl:hasDefinition
- [x] Add section comment: "Upper ontology grounding for process/entity/quality hierarchy"
- [x] Test ontology loads in Protégé without errors

### Update DwC-to-BFO Mappings

**File:** `ontology/dfo-salmon.ttl`

- [x] Update lines 219-234 (Class Mappings section)
- [x] Change `dwc:Organism rdfs:subClassOf bfo:0000040` to use actual BFO class (not comment)
- [x] Change `dwc:Event rdfs:subClassOf bfo:0000015` to use actual BFO class
- [x] Change `dwc:MaterialEntity rdfs:subClassOf bfo:0000040`
- [x] Change `dwc:Agent rdfs:subClassOf bfo:0000040`
- [x] Update section title to "Class Mappings to Darwin Core and BFO Upper Ontology"
- [x] Verify reasoning works with ELK reasoner
- [x] Implement DwC-CM alignment (dwc:Assertion transition)

### Clean Up Estimate Type Classification Code

- [x] Delete scripts/automated_classification.py (not needed for FSAR Tracer MVP)
- [x] Update docs/CONVENTIONS.md: Remove automated classification references
- [x] Update docs/VALIDATION_README.md: Change to manual classification
- [x] Update docs/ADR.md: Note automation deferred to post-MVP
- [x] Update scripts/test_shacl_validation.py: Remove assignedEstimateType query
- [x] Keep EstimateTypeScheme and assignedEstimateType property in ontology

### Enhance CONVENTIONS.md Import Policy

**File:** `docs/CONVENTIONS.md`

- [x] Add BFO rationale explaining why BFO is used for FSAR Tracer
- [x] Add FSAR Tracer specific usage examples for BFO, DQV, and PROV-O
- [x] Document how MIREOT terms map to FSAR evidence chain classes
- [x] Explain PROV-O property usage patterns for provenance tracking

### Update SHACL File Header

**File:** `ontology/shapes/dfo-salmon-shapes.ttl`

- [x] Clarify that SHACL shapes are for data quality validation, not automated classification
- [x] Add note that estimate types are manually assigned based on Hyatt 1997 criteria
- [x] Add note that no instance data goes in main ontology file; instances go in examples/

### Fix ROBOT Validation

**File:** `.github/workflows/ci.yml`

- [x] Comment out ROBOT validate step that was causing GitHub Actions failures
- [x] ROBOT validate command doesn't exist in v1.9.5 or needs profile setup
- [x] Keep reasoning step which works correctly
- [x] Add note to re-enable in PR-013: CI/CD and Quality Checks

---

## Darwin Core Conceptual Model (DwC-CM) Implementation

**Owner:** Brett  
**Priority:** High  
**Scope:** DwC-CM alignment and implementation

### Implement DwC-CM Patterns

**File:** `ontology/dfo-salmon.ttl`

- [x] Update ontology header with DwC-CM implementation comments
- [x] Update `dfo:EscapementMeasurement` to subclass `dwc:Assertion` (replace `dwc:MeasurementOrFact`)
- [x] Update `dfo:GSICompositionMeasurement` to subclass `dwc:Assertion` (replace `dwc:MeasurementOrFact`)
- [x] Update `dfo:Catch` to subclass `dwc:Assertion` (replace `dwc:MeasurementOrFact`)
- [x] Remove TODO comments for dwc:Assertion transition
- [ ] Review property domains/ranges for DwC-CM alignment
- [ ] Ensure DwC Data Package (DwC-DP) compatibility

### Update Documentation for DwC-CM

**Files:** `docs/CONVENTIONS.md`, `README.md`, `docs/onboarding.md`

- [x] Update CONVENTIONS.md with DwC-CM implementation guidance
- [x] Update README.md to reflect DwC-CM implementation
- [x] Update onboarding.md with DwC-CM concepts

---

## DQV MIREOT Import for Quality Framework

**Owner:** Mel  
**Priority:** High  
**Scope:** Evidence completeness and quality tracking

### Add DQV MIREOT Definitions

**File:** `ontology/dfo-salmon.ttl`

- [x] **VERIFIED**: DQV prefix declaration exists at line 9: `@prefix dqv: <http://www.w3.org/ns/dqv#>`
- [x] **VERIFIED**: DQV MIREOT section exists after BFO section (lines 415-440)
- [x] **VERIFIED**: Imported `dqv:Dimension` with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Imported `dqv:QualityAnnotation` with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Imported `dqv:inDimension` object property with rdfs:label and rdfs:comment
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each term pointing to DQV namespace
- [x] DQV terms are recognized in Protégé

### Create Evidence Completeness Dimensions

**File:** `ontology/dfo-salmon.ttl`

- [x] **VERIFIED**: Section comment exists: "Evidence Completeness Framework (DQV-based)"
- [x] **VERIFIED**: Created `dfoc:EvidenceCompletenessDimension` as instance of `dqv:Dimension` (line 823)
- [x] **VERIFIED**: Created `dfoc:DataCurrencyDimension` as instance of `dqv:Dimension` (line 828)
- [x] **VERIFIED**: Added skos:prefLabel and skos:definition for both dimensions
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each dimension

### Create Quality Annotations (Evidence Badges)

**File:** `ontology/dfo-salmon.ttl`

- [x] **VERIFIED**: Created `dfoc:CompleteEvidence` as `dqv:QualityAnnotation` (line 833)
- [x] **VERIFIED**: Created `dfoc:GapsEvidence` as `dqv:QualityAnnotation` (line 839)
- [x] **VERIFIED**: Created `dfoc:MissingCriticalEvidence` as `dqv:QualityAnnotation` (line 845)
- [x] **VERIFIED**: Linked each to `dfoc:EvidenceCompletenessDimension` via `dqv:inDimension`
- [x] **VERIFIED**: Added skos:prefLabel for each badge (Complete, Gaps, Missing-Critical)
- [x] **VERIFIED**: Added rdfs:isDefinedBy for each annotation

---

## FSAR Tracer Core Classes

**Owner:** Brett  
**Priority:** High  
**Scope:** Evidence chain ontology classes

### FSAR Module Implementation Status

**Note:** Policy readiness / decision nodes are deferred to post-MVP; core focus now is scientific evidence chain (Data → Method → RefPoints → Status → Advice) and class/ genetics alignment.

**File:** `docs/ontology_applications/dfo-fsar.ttl`  
**Latest Version:** `docs/ontology_applications/dfo-fsar-v4.ttl` (includes WSP rapid-status support)

- [x] **COMPLETED**: FSAR module ontology created with comprehensive class definitions
- [x] **COMPLETED**: Core FSAR classes implemented:
  - `dfoc:StockAssessment` (subclass of `dfo:StockAssessment`)
  - `dfoc:PolicyReadiness` (policy & legal readiness tracking)
  - `dfoc:ManagementDecision` (management decision records)
  - `dfoc:CUInclusion` (CU accounting entries)
  - `dfoc:GSIUsage` (genetic stock ID usage details)
  - `dfoc:ChangeLogEntry` (change log entries)
- [x] **COMPLETED**: Comprehensive object properties implemented:
  - `dfoc:assessesUnit`, `dfoc:hasStatusZone`, `dfoc:usesDataset`, `dfoc:usesMethod`
  - `dfoc:supportsAdvice`, `dfoc:ledToDecision`, `dfoc:hasPolicyReadiness`
  - `dfoc:hasCUInclusion`, `dfoc:hasGSIUsage`, `dfoc:hasChangeLogEntry`, `dfoc:hasThreatFactor`
- [x] **COMPLETED**: Comprehensive datatype properties implemented:
  - Policy readiness: `dfoc:belowLRP`, `dfoc:hcrIdentifier`, `dfoc:hcrParameters`, `dfoc:rebuildingPlanURL`
  - Assessment details: `dfoc:assessedYear`, `dfoc:uncertaintyNote`, `dfoc:statusCI`, `dfoc:downgradeReason`
  - CU accounting: `dfoc:cuDecision`, `dfoc:justification`, `dfoc:reviewedBy`, `dfoc:reviewDate`
  - GSI usage: `dfoc:gsiUsed`, `dfoc:gsiSampleSize`, `dfoc:gsiAssignmentUncertainty`
  - Change tracking: `dfoc:changeCategory`, `dfoc:changeDetail`
- [x] **COMPLETED**: Example instances created for Barkley Sockeye 2025 assessment
- [x] **COMPLETED**: PROV-O provenance patterns implemented with RDF-star annotations

### WSP Rapid-Status Support

**File:** `docs/ontology_applications/dfo-fsar-v4.ttl`

- [x] **COMPLETED**: WSP rapid-status support added to FSAR Tracer module (2025-01-27)
  - Added WSP metric classes (`dfoc:WSPMetric`, `dfoc:MetricBenchmark`, `dfoc:AlgorithmThreshold`)
  - Added status and confidence categories using SKOS
  - Added properties linking assessments to metrics, statuses, and confidence
  - Added example benchmark and threshold instances
  - Documented benchmark vs. algorithm threshold differences
- [x] **COMPLETED**: Updated PRD with WSP rapid-status section (2f) and 4 new CQs (CQ-WSP-1 through CQ-WSP-4)
- [ ] **NEXT**: Integrate WSP rapid-status into FSAR Tracer UI/application layer
- [ ] **NEXT**: Add validation rules for benchmark/threshold consistency
- [ ] **FUTURE**: Consider time-varying productivity support for relative abundance benchmarks

### Integration with Core Ontology

**File:** `ontology/dfo-salmon.ttl`

- [x] **COMPLETED (2025-11-03)**: Consolidated FSAR terminology into the core ontology
  - Converted WSP zone values into `dfoc:` rapid-status concepts
  - Added FSAR trigger, requirement, metric, confidence, and policy readiness classes/properties
  - Introduced shared vocabularies for rapid-status metrics and confidence categories
  - **NOTE**: `docs/ontology_applications/dfo-fsar-v4.ttl` is kept for reference (not removed)
- [x] **COMPLETED**: Added `dfoc:StockAssessment` class to core ontology (2025-01-27)
- [x] **COMPLETED (2025-11-03)**: Added supporting SKOS concept schemes for rapid-status metrics and confidence categories
- [ ] **NEXT**: Backfill remaining FSAR-adjacent vocabularies (threat factors, expanded method schemes) once downstream requirements are finalized

### Enhanced Requirements from PRD Updates

**Based on comprehensive PRD updates**

- [ ] **NEXT**: Add benchmark transparency properties:
  - `dfoc:reference_point_type` (controlled vocab: LRP/USR/Sgen/Smsy)
  - `dfoc:benchmark_method` (controlled vocab: SR model, percentile, expert judgment)
  - `dfoc:benchmark_sensitivity` (sensitivity flags)
- [ ] **NEXT**: Add uncertainty handling properties:
  - `dfoc:status_confidence` (probabilities/CI)
  - `dfoc:ciLower`, `dfoc:ciUpper` (confidence interval bounds)
  - `dfoc:probabilityGreen`, `dfoc:probabilityAmber`, `dfoc:probabilityRed`
- [ ] **NEXT**: Add GSI risk assessment properties:
  - `dfoc:baseline_reference` (baseline reference for GSI)
  - `dfoc:fisheryType` (mixed-stock/single-stock classification)
- [ ] **NEXT**: Add method reproducibility properties:
  - `dfoc:method_name`, `dfoc:method_version`, `dfoc:code_commit`
- [ ] **NEXT**: Add data source properties:
  - `dfoc:data_source_type` (direct, proxy, genetic proxy)
  - `dfoc:spawner_origin` (wild, hatchery, mixed)
  - `dfoc:proxy_justification` (required when data_source_type contains "proxy")

---

## W3ID Phase 1 Publication

**Owner:** Mel  
**Priority:** High
**Scope:** Publish stable core terms to w3id.org

### Core term subset (end-of-week target)

- [ ] Identify the minimal, stable subset of fundamental salmon stock assessment terms for initial w3id publication (definitions unlikely to change; stable class/subclass structure; definition sources present)
- [ ] Review and confirm definition quality and sources for the candidate list
- [ ] Produce and agree the initial publication list (see `docs/notes/2025-12-03-w3id-core-terms.md`)
- [ ] Update rdfs:isDefinedBy/versioning for the agreed subset and prep redirections

### Prepare Core Terms

- [ ] Review/finalize labels and definitions for core terms
- [ ] Update ontology IRI to https://w3id.org/dfoc/salmon (currently using this IRI)
- [ ] Create version IRI: https://w3id.org/dfoc/salmon/v0.1.0
- **NOTE**: Ontology currently uses `https://w3id.org/dfoc/salmon` (line 74)
- [ ] Update all rdfs:isDefinedBy for core terms to w3id URIs
- [ ] Document versioning strategy
- [x] **COMPLETED**: Changed namespace from `dfo:` to `dfoc:` since `dfo` is already taken on w3id
  - [x] Updated all prefix declarations to `@prefix dfoc: <https://w3id.org/dfoc/salmon#>`
  - [x] Updated all class and property references to use `dfoc:` prefix
  - [x] Updated all rdfs:isDefinedBy references to use dfoc: namespace
  - [ ] **TODO**: Update documentation (README.md, examples) to consistently reflect dfoc: namespace
  - **NOTE**: Core ontology uses `dfoc:` prefix and `https://w3id.org/dfoc/salmon#` IRI

### Create W3ID Configuration

- [ ] Fork w3id.org repository
- [ ] Create /dfo/salmon/.htaccess (content negotiation)
- [ ] Add redirections: ontology file and term URIs
- [ ] Create /dfo/salmon/README.md

### Test Locally

- [ ] Test ontology file redirection
- [ ] Test term URI redirection (#Stock, etc.)
- [ ] Test content negotiation (text/turtle, application/rdf+xml)
- [ ] Verify version URIs

### Submit W3ID PR

- [ ] Submit to w3id.org repository
- [ ] Document purpose in PR description
- [ ] Respond to reviewers
- [ ] Monitor for approval

### Update Post-Publication

- [ ] Confirm all rdfs:isDefinedBy use w3id URIs
- [ ] Test URI resolution
- [ ] Update README with w3id links
- [ ] Update CONVENTIONS with persistent URI guidelines

**Phase 1 Terms List:**

- Core: Stock, ConservationUnit, ManagementUnit
- Events: EscapementMeasurement, EscapementSurveyEvent
- Properties: aboutStock, hasMember, isMemberOf, usesEnumerationMethod, usesEstimateMethod, assignedEstimateType
- SKOS: EstimateTypeScheme (Type1-6), EnumerationMethodScheme, EstimateMethodScheme
- **Note**: All terms will use `dfoc:` namespace prefix instead of `dfo:` due to w3id namespace conflict

---

## Genetics Classes for GRD Integration

**Owner:** Brett  
**Priority:** High  
**Scope:** Link to Genetics Results Database

### Review Existing Genetics Classes

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review existing genetics classes (lines 885-923): GeneticSample, GSIRun, GSICompositionMeasurement, ReportingUnit, Assay, MarkerPanel, Protocol
- [ ] Document current genetics class limitations and gaps
- [ ] Verify properties link samples to survey events and stocks
- [ ] Check if `GSIRun` adequately models GRD run identifiers
- [ ] Verify `GSICompositionMeasurement` can link to FSAR Tracer data products

### Add GRD Linkage Properties

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:grdRunID` DatatypeProperty for GRD Run_ID
- [ ] Add `dfo:grdSampleID` DatatypeProperty for GRD Sample_ID
- [ ] Add `dfo:grdAssayID` DatatypeProperty for GRD Assay_ID (optional)
- [ ] Add `dfo:gsi_sample_size` DatatypeProperty for uncertainty tracking
- [ ] Add `dfo:gsi_ci` DatatypeProperty for confidence intervals
- [ ] Set appropriate domains and ranges
- [ ] Add comments explaining GRD integration

### Document Genetics-to-FSAR Linkage Pattern

**File:** `docs/CONVENTIONS.md`

- [ ] Add section 6.x "Genetics Results Database (GRD) Integration"
- [ ] Document how GSICompositionMeasurement links to StatusAssessment
- [ ] Explain Run_ID, Sample_ID, Assay_ID usage
- [ ] Add example pattern for GRD→SPSR→FSAR trace
- [ ] Document uncertainty propagation from GSI to status assessment

---

## SIL/SEN SKOS Schemes Integration

**Owner:** Mel + Minh Doan  
**Priority:** High  
**Scope:** Align with Minh Doan's escapement measurement work

### Integrate SIL Enumeration Methods

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review Minh Doan's enumeration method concepts
- [ ] Integrate missing concepts into `:EnumerationMethodScheme`
- [ ] Ensure all concepts have skos:prefLabel, skos:definition, skos:broader
- [ ] Add skos:inScheme links
- [ ] Verify no duplicate or conflicting concepts

### Integrate SEN Estimate Methods

**File:** `ontology/dfo-salmon.ttl`

- [ ] Review Minh Doan's estimate method concepts
- [ ] Integrate missing concepts into `:EstimateMethodScheme`
- [ ] Ensure consistency with existing methods (AreaUnderTheCurve, PeakCountAnalysis, etc.)
- [ ] Add skos:prefLabel, skos:definition, skos:broader for all
- [ ] Verify scheme completeness

### Add SIL/SEN Classes (if needed)

**File:** `ontology/dfo-salmon.ttl`

- [ ] Add `dfo:StreamInspectionLog` class if not already present
- [ ] Add `dfo:EscapementNarrative` class if not already present
- [ ] Link to existing `dfo:EscapementSurveyEvent` hierarchy
- [ ] Add properties for SIL/SEN metadata
- [ ] Document relationship to EscapementMeasurement

---

## Data Source Properties

**Owner:** Mel  
**Priority:** High  
**Scope:** Evidence completeness tracking properties

### Data Source Properties Status

**File:** `docs/ontology_applications/dfo-fsar.ttl`

- [x] **COMPLETED**: `dfoc:proxy_justification` implemented in FSAR module
  - Domain: `dfoc:CUInclusion`, Range: `xsd:string`
  - Comment: "Explanation for the CU decision if it's not simply 'included'"
- [x] **COMPLETED**: Data source tracking via `dfoc:usesDataset` property
  - Links assessments to input datasets
  - Subproperty of `prov:used` for provenance tracking

### Missing Data Source Properties (Need Integration)

**File:** `ontology/dfo-salmon.ttl`

- [ ] **NEXT**: Add `dfo:data_source_type` DatatypeProperty to core ontology
  - Set domain to `dfo:EscapementMeasurement`, range to `xsd:string`
  - Add label and comment explaining source types (direct, proxy, genetic proxy)
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:spawner_origin` DatatypeProperty to core ontology
  - Set domain to `dfo:EscapementMeasurement`, range to `xsd:string`
  - Add comment explaining wild, hatchery, mixed origins
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Integrate FSAR module `dfoc:proxy_justification` with core ontology
  - Consider if this should be a core property or remain FSAR-specific
  - Ensure alignment with PRD requirements for proxy justification

---

## Method Reproducibility Properties

**Owner:** Mel  
**Priority:** High  
**Scope:** Method reproducibility tracking

### Method Reproducibility Properties Status

**File:** `docs/ontology_applications/dfo-fsar.ttl`

- [x] **COMPLETED**: Method tracking via `dfoc:usesMethod` property
  - Links assessments to analytical methods (SKOS concepts)
  - Subproperty of `prov:wasGeneratedBy` for provenance tracking
- [x] **COMPLETED**: Method provenance via PROV-O patterns
  - RDF-star annotations for method generation provenance
  - Links to code commits and implementation details

### Missing Method Reproducibility Properties (Need Integration)

**File:** `ontology/dfo-salmon.ttl`

- [ ] **NEXT**: Add `dfo:method_name` DatatypeProperty to core ontology
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:method_version` DatatypeProperty to core ontology
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:code_commit` DatatypeProperty to core ontology
  - Set domain to `dfo:AnalysisMethod`, range to `xsd:string`
  - Add comment: Git commit hash/tag for reproducibility
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Integrate FSAR module method tracking with core ontology
  - Ensure `dfo:AnalysisMethod` class exists in core ontology
  - Align FSAR method tracking with core ontology patterns

---

## Reference Points and Review Properties

**Owner:** Mel  
**Priority:** High  
**Scope:** Reference points and review tracking

### Reference Points and Review Properties Status

**File:** `docs/ontology_applications/dfo-fsar.ttl`

- [x] **COMPLETED**: Policy readiness properties implemented:
  - `dfoc:belowLRP` (boolean flag for LRP status)
  - `dfoc:hcrIdentifier` (HCR identifier/name)
  - `dfoc:hcrParameters` (HCR parameters)
  - `dfoc:rebuildingPlanURL` (rebuilding plan link)
- [x] **COMPLETED**: Assessment review properties implemented:
  - `dfoc:uncertaintyNote` (uncertainty summary)
  - `dfoc:statusCI` (status confidence interval)
  - `dfoc:downgradeReason` (downgrade criteria)
- [x] **COMPLETED**: CU accounting review properties implemented:
  - `dfoc:reviewedBy` (reviewer name/identifier)
  - `dfoc:reviewDate` (review date)
- [x] **COMPLETED**: Reference point tracking via `dfoc:usesMethod` property
  - Links assessments to reference point calculation methods

### Missing Reference Points Properties (Need Integration)

**File:** `ontology/dfo-salmon.ttl`

- [ ] **NEXT**: Add `dfo:reference_point_type` DatatypeProperty to core ontology
  - Set range to `xsd:string`
  - Add comment: Sgen, USR, LRP, SMSY, etc.
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:benchmark_method` DatatypeProperty to core ontology
  - Set range to `xsd:string`
  - Add comment: SR model, percentile, expert judgment
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:benchmark_sensitivity` DatatypeProperty to core ontology
  - Set range to `xsd:boolean`
  - Add comment: flag indicating sensitivity to assumptions
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Add `dfo:status_value` DatatypeProperty to core ontology (if not exists)
  - Set range to `xsd:decimal`
  - Add comment: numeric status value
  - **Note**: This should be added to core ontology, not FSAR module
- [ ] **NEXT**: Integrate FSAR module policy readiness with core ontology
  - Consider if policy readiness should be core or FSAR-specific
  - Ensure alignment with PRD requirements for policy gates

---

## SHACL Header and Documentation

## SHACL Decision Context Shape

**Owner:** Mel  
**Priority:** High  
**Scope:** Decision context validation

### Create Decision Context Shape

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

---

## SHACL Conditional Validation Rules

**Owner:** Mel  
**Priority:** High  
**Scope:** Conditional validation logic

### Add Conditional Validation Rules

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

---

## Mel Provenance Validation

**Owner:** Mel  
**Priority:** High  
**Scope:** Provenance chain validation

### Add Provenance Validation

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

## W3ID Phase 2 Publication

**Owner:** Mel  
**Priority:** Medium (after FSAR implementation)  
**Scope:** Publish FSAR Tracer terms

### Prepare FSAR Terms

- [ ] Review/finalize FSAR Tracer classes and properties
- [ ] Update version IRI to https://w3id.org/dfoc/salmon/v0.5.0
- [ ] Update rdfs:isDefinedBy for FSAR terms to w3id URIs
- [ ] Test FSAR terms work correctly

### Update W3ID Configuration

- [ ] Update /dfo/salmon/.htaccess for new version
- [ ] Add redirections for FSAR term URIs
- [ ] Update /dfo/salmon/README.md with FSAR Tracer information

### Submit W3ID Update

- [ ] Submit PR to w3id.org repository
- [ ] Document FSAR Tracer additions
- [ ] Respond to reviewers
- [ ] Monitor for approval

**Phase 2 Terms List:**

- Classes: StatusAssessment, ScientificOutput, ManagementDecision, AnalysisMethod
- Properties: status_value, method_name, reviewer, review_date, data_source_type, spawner_origin
- **Note**: All terms will use `dfoc:` namespace prefix instead of `dfo:` due to w3id namespace conflict

---

## SPARQL Query Pack

**Owner:** Mel  
**Priority:** High  
**Scope:** Competency queries for UI

### Create Query File

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] **IN PROGRESS**: Create new file for FSAR Tracer queries
- [ ] Add header with query pack version and date
- [ ] Add prefix declarations for all namespaces
- [ ] Add table of contents listing Q1-Q9
- **NOTE**: Queries are documented in PRD but file not yet created

### Core Evidence Queries (Q1-Q4)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] **TODO**: Implement Q1: Evidence Completeness by Decision
  - Check required vs optional fields
  - Return state: Complete, Gaps, or Missing-Critical
  - Query pattern documented in PRD (CQ-EV-1)
- [ ] **TODO**: Implement Q2: Proxy Without Justification
  - Find records where data_source_type contains "proxy" but no proxy_justification
  - Query pattern documented in PRD
- [ ] **TODO**: Implement Q3: Method Reproducibility
  - Return method_name, method_version, code_commit
  - Flag if any missing
  - Query pattern documented in PRD
- [ ] **TODO**: Implement Q4: Reference Points Used
  - Return reference_point_type, benchmark_method, benchmark_sensitivity
  - List all reference points used in status assessment
  - Query pattern documented in PRD

### Data Currency and Quality Queries (Q5-Q8)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] **TODO**: Implement Q5: Missing Uncertainty
  - Find StatusAssessments without status_ci
  - Find GSIResults without gsi_sample_size or gsi_ci
  - Query pattern documented in PRD
- [ ] **TODO**: Implement Q6: Data Currency
  - Return last modified timestamp per component (Dataset, Method, ReferencePoint, Status, Advice)
  - Return version pins (owl:versionInfo)
  - Flag stale data (>12 months)
  - Query pattern documented in PRD
- [ ] **TODO**: Implement Q7: Scientific Output Text + Review
  - Return scientific_output_text, reviewer, review_date
  - Query pattern documented in PRD
- [ ] **TODO**: Implement Q8: Linked Documents
  - Return FSAR/Tech/Research document metadata
  - Include doc_type, title, identifier, issued date, URL
  - Query pattern documented in PRD

### Genetics Integration Query (Q9)

**File:** `ontology/sparql/fsar-tracer-queries.rq`

- [ ] **TODO**: Implement Q9: GRD Data Product Integration
  - Return GSIRun linked to StatusAssessment
  - Include grdRunID, grdSampleID, grdAssayID
  - Return GSICompositionMeasurement with CIs
  - Show linkage: GRD → Measurement → Status → Advice
  - Added GSI risk assessment queries for mixed-stock fisheries
  - Query pattern documented in PRD (CQ-GRD-1)

---

## Relations Ontology Alignment

**Owner:** Mel  
**Priority:** Medium  
**Scope:** Documentation only (no code changes for MVP)

### Document RO Alignment

**File:** `ontology/dfo-salmon.ttl`

- [ ] Update membership relations section comment (lines 1010-1020)
- [ ] Add note: "Aligned with RO:0002131 (has_member) and RO:0002350 (member_of)"
- [ ] Add note: "Implemented as independent properties to avoid RO import overhead"
- [ ] Add `rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002131>` to `dfo:hasMember`
- [ ] Add `rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002350>` to `dfo:isMemberOf`
- [ ] Update comment explaining semantic alignment without import

---

## Import Policy Documentation

**Owner:** Brett  
**Priority:** High  
**Scope:** CONVENTIONS documentation

### Update CONVENTIONS.md Import Policy

**File:** `docs/CONVENTIONS.md`

- [x] Add new section 2.3.6 "Ontology Import Strategy"
- [x] Document three approaches: Full import, MIREOT, Prefix only
- [x] Add decision matrix table (BFO, IAO, DQV, PROV-O, RO, DPROD, SKOS, DwC)
- [x] Explain when to use each approach with examples
- [x] Add FSAR Tracer import decisions and rationale
- [x] Document MIREOT implementation pattern


## README Updates

**Owner:** Mel  
**Priority:** High  
**Scope:** README documentation

### Update README.md Technical Overview

**File:** `README.md`

- [ ] Update Technical Overview section (lines 67-75)
- [ ] Add: "Pragmatic imports: MIREOT for BFO/IAO/DQV (~12 terms)"
- [ ] Add: "Upper ontology: BFO grounding for process/entity hierarchy"
- [ ] Add: "Provenance: PROV-O properties for FSAR evidence chains"
- [ ] Add: "Quality: DQV dimensions for evidence completeness tracking"

### Add FSAR Tracer Section to README

**File:** `README.md`

- [ ] Add FSAR Tracer subsection to Ontology Scope (after line 130)
- [ ] List core classes: StatusAssessment, ScientificOutput, ManagementDecision, AnalysisMethod
- [ ] List PROV-O properties used
- [ ] List DQV dimensions and quality annotations
- [ ] List required fields for evidence completeness
- [ ] Note: No instance data in main ontology file

---

## Sample Data Creation

**Owner:** Mel  
**Priority:** High  
**Scope:** Example instances for testing (NOT in main ontology)

### Create Barkley Sockeye Sample Instances

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

### Link Instances with PROV-O

**File:** `ontology/examples/barkley-2025-sample.ttl`

- [ ] Link StatusAssessment to EscapementMeasurement via `prov:used`
- [ ] Link StatusAssessment to ReferencePoint via `prov:used`
- [ ] Link StatusAssessment to AnalysisMethod via `prov:wasGeneratedBy`
- [ ] Link StatusAssessment to Agent via `prov:wasAttributedTo`
- [ ] Link ScientificOutput to StatusAssessment via `prov:wasDerivedFrom`
- [ ] Link ManagementDecision to ScientificOutput via `prov:used`

### Annotate with DQV Quality

**File:** `ontology/examples/barkley-2025-sample.ttl`

- [ ] Add `dqv:hasQualityAnnotation` to StatusAssessment
- [ ] Link to `dfo:CompleteEvidence` annotation
- [ ] Add data currency timestamps using `dcterms:modified`
- [ ] Add version pins using `owl:versionInfo`
- [ ] Document quality annotation pattern in comments

---

## JSON-LD Context and Export

**Owner:** Brett  
**Priority:** Medium  
**Scope:** JSON-LD export functionality

### Create JSON-LD Context

**File:** `ontology/examples/fsar-tracer-context.jsonld` (NEW FILE)

- [ ] Create @context with all FSAR Tracer prefixes
- [ ] Map dfo, prov, dqv, bfo, iao, dwc, skos, dcterms, schema namespaces
- [ ] Define short aliases for common properties
- [ ] Add @vocab for default namespace
- [ ] Test context validates with JSON-LD playground

### Export Sample Data as JSON-LD

**File:** `ontology/examples/barkley-2025-sample.jsonld` (NEW FILE)

- [ ] Export Barkley sample as JSON-LD using context
- [ ] Validate JSON-LD syntax
- [ ] Document export process in README
- [ ] Add note: This is example data for testing, not production

---

## W3ID Phase 3 Complete Publication

**Owner:** Mel  
**Priority:** Medium  
**Scope:** Complete W3ID publication

### Prepare Remaining Terms

- [ ] Review and finalize all remaining terms
- [ ] Update version IRI to https://w3id.org/dfoc/salmon/v1.0.0
- [ ] Update all rdfs:isDefinedBy to w3id URIs
- [ ] Document complete versioning strategy

### Final W3ID Update

- [ ] Update /dfo/salmon/.htaccess for v1.0.0
- [ ] Add redirections for all remaining term URIs
- [ ] Update /dfo/salmon/README.md with complete documentation
- [ ] Submit final PR to w3id.org repository

### Post-Publication Verification

- [ ] Test all URIs resolve correctly
- [ ] Verify content negotiation works
- [ ] Update all documentation with w3id links
- [ ] Document w3id.org usage in README

---

## CI/CD and Quality Checks

**Owner:** Brett  
**Priority:** Medium  
**Scope:** CI/CD pipeline improvements

### Add Quality Checks

- [ ] Add ontology linting checks
- [ ] Add SPARQL query validation
- [ ] Add SHACL validation in CI
- [ ] Add performance benchmarks


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

### ROBOT Validation Setup

- [ ] Investigate ROBOT validate command requirements
- [ ] Determine if newer ROBOT version needed (>1.9.5)
- [ ] Create OBO validation profile if needed
- [ ] Re-enable validation in CI/CD pipeline
- [ ] Add to PR-013: CI/CD and Quality Checks

---


## NCEAS Salmon Ontology Integration

### Immediate Actions (Next 3 months)

- [ ] **Review Current DFO to NCEAS Mappings**: Examine existing mappings in `dfo-salmon.ttl`
  - [ ] Review `dfo:SizeAtAge` → `odo:SALMON_00000167` (measurement type) mapping
  - [ ] Review `dfo:AgeAtMaturity` → `odo:SALMON_00000407` (age class) mapping
  - [ ] Review `dfo:PreTerminalFishery` → `odo:SALMON_00000137` (fishery type) mapping
  - [ ] Review `dfo:TerminalFishery` → `odo:SALMON_00000137` (fishery type) mapping
  - [ ] Validate semantic alignment and correctness of existing mappings
- [ ] **Review All External Mappings**: Audit all external ontology mappings in DFO ontology
  - [ ] Review BFO mappings (process, material entity, generically dependent continuant)
  - [ ] Review IAO mappings (measurement datum, value specification, information content entity, directive)
  - [ ] Review DwC mappings (Event, Organism, MaterialEntity, Agent)
  - [ ] Review PROV-O property usage patterns
  - [ ] Review SKOS scheme alignments
  - [ ] Document mapping quality and identify any issues
- [ ] **Complete NCEAS Alignment**: Implement remaining 3 classes from Phase 1
  - [ ] `dfo:GeneticDiversity` → `odo:SALMON_00000167` (measurement type)
  - [ ] `dfo:Fecundity` → `odo:SALMON_00000167` (measurement type)
  - [ ] `dfo:MixedStockFishery` → `odo:SALMON_00000137` (Fishery type)
- [ ] **Analyze Recruitment Relationship**: Examine `dfo:Recruitment` relationship to NCEAS age class recruits
- [ ] **Update Documentation**: Document integration strategy in CONVENTIONS.md

### Medium-term Actions (3-12 months)

- [ ] **Establish NCEAS Governance**: Work with NCEAS to establish cross-ontology coordination
- [ ] **Contribute to NCEAS**: Identify and contribute DFO concepts with multi-organizational relevance
- [ ] **Monitor NCEAS Changes**: Establish process to monitor and respond to NCEAS changes

### Long-term Actions (1-3 years)

- [ ] **Support NCEAS Development**: Participate in NCEAS development for general domain concepts
- [ ] **Evaluate Success**: Assess whether integration achieves intended benefits
- [ ] **Adapt Strategy**: Refine integration approach based on experience

### Contribution Heuristics

- **CONTRIBUTE TO NCEAS**: Multi-organizational relevance, scientific consensus, domain generality, methodological standards, environmental concepts, biological measurements, equipment and gear
- **KEEP IN DFO**: Organizational specificity, Canadian context, DFO protocols, management hierarchies, policy frameworks, assessment methods, reference points
- [ ] Consider design options for a `dwc:Assertion` / `gcdfo:SalmonAssessmentAssertion` wrapper around existing `iao:0000109` metrics (e.g., assertsValue/aboutOccurrence/basedOnEvent) and decide how generic vs FSAR-specific the pattern should be before tightening domains/ranges.
- [ ] Revisit SOSA alignment once DwC-CM modeling stabilizes (e.g., decide whether `sosa:Observation ⊑ dwc:Event`, which entities serve as `sosa:FeatureOfInterest` such as `dwc:Occurrence`, CU-in-year population proxies, or organisms, and how many layers we keep in Observation → Occurrence → Organism).
- [ ] Review with biologists/policy whether reporting/management strata (CU/DU/SMU/PFMA) should stay as information-defined strata or be paired with explicit population classes (e.g., `gcdfo:PopulationInSpaceTime`, `gcdfo:CURealizedPopulation`) linked via a `realizesStratum` property; update definitions accordingly after consultation.
- [ ] Decide which vocabularies should remain SKOS-only vs SKOS+OWL punning (e.g., origins, status zones, benchmarks), and record a simple convention in `docs/CONVENTIONS.md` after current SKOS cleanup so different user groups have clear guidance.
- [ ] Re-examine hybrid patterns like `:DowngradeCriteria` (SKOS concept subclassing `dwc:Protocol`) and similar cases; consider alternatives such as a separate OWL protocol class linked via `skos:exactMatch` once the punning convention is set.
