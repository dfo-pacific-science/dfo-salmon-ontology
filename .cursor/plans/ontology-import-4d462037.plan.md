<!-- 4d462037-1a4c-4461-91b6-11e2b157a027 ff9b9e1d-add3-4ed4-b300-ab9545cc0676 -->
# FSAR Tracer MVP-Focused Ontology Plan

## Critical Insight: Import Strategy for FSAR Tracer

**FSAR Tracer Core Need:** Six-node evidence chain with provenance and quality tracking.

**Ontology Requirements:**

1. **Provenance chain:** Data → Method → RefPoints → Status → Advice → Decision
2. **Quality tracking:** Evidence completeness badges (Complete/Gaps/Missing-Critical)
3. **Data currency:** Timestamps and version pins
4. **Document linkage:** FSAR/Tech/Research docs

**Import Strategy Decision Matrix:**

| Ontology | Approach | Rationale |

|----------|----------|-----------|

| **PROV-O** | Prefix only, NO import | Already has necessary properties; import adds 200+ terms we won't use |

| **DQV** | MIREOT (~5 terms) | Need only: Dimension, QualityAnnotation, Metric, inDimension |

| **DPROD** | Investigate first, likely prefix | Namespace unclear; may use schema:Dataset + dcat instead |

| **BFO/IAO** | MIREOT (~8 terms) | Keep existing IAO usage; add BFO for proper upper ontology grounding |

| **RO** | Prefix + selective alignment | Align hasMember but don't import 500+ relations |

| **SHACL** | Prefix only | Validation language, not domain ontology |

## BFO/IAO Analysis for FSAR Tracer

**Current IAO Usage (keep these):**

- `iao:0000109` (measurement datum) - used for EscapementMeasurement, Catch
- `iao:0000032` (value specification) - used for reference points
- `iao:0000030` (information content entity) - used for Dataset, StatusCategory
- `iao:0000643` (directive information entity) - used for WildSalmonPolicy

**BFO Would Add Upper Ontology Grounding:**

- `bfo:0000015` (process) - for Method, SurveyEvent, Decision
- `bfo:0000040` (material entity) - for Stock, GeneticSample
- `bfo:0000031` (generically dependent continuant) - for ScientificOutput, StatusAssessment

**Decision:** Use MIREOT for BFO + IAO terms we actually need; don't import full ontologies.

**Why BFO Doesn't Compete with PROV-O:**

- BFO = upper ontology (what things ARE: Entity, Process, Quality)
- PROV-O = provenance relations (how things were DERIVED: wasGeneratedBy, wasDerivedFrom)
- IAO = information artifacts (what information IS: Dataset, Document, Measurement)
- They're complementary, not competing

## MIREOT Implementation Strategy

**What is MIREOT?** Minimum Information to Reference an External Ontology Term - import only the specific terms you need with their labels/definitions, not entire ontologies.

**MIREOT for DFO Salmon Ontology:**

```turtle
# Import specific BFO terms via MIREOT
bfo:0000015 a owl:Class ;
  rdfs:label "process"@en ;
  obo:IAO_0000115 "An occurrent that has temporal parts and for some time t, p s-depends_on some material entity at t."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

bfo:0000040 a owl:Class ;
  rdfs:label "material entity"@en ;
  obo:IAO_0000115 "An independent continuant that is spatially extended whose identity is independent of that of other entities and can be maintained through time."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

# Keep existing IAO terms (already using these)
iao:0000109 a owl:Class ;
  rdfs:label "measurement datum"@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/iao.owl> .

# Add DQV terms via MIREOT
dqv:Dimension a owl:Class ;
  rdfs:label "Dimension"@en ;
  rdfs:comment "Represents criteria relevant for assessing quality."@en ;
  rdfs:isDefinedBy <http://www.w3.org/ns/dqv#> .

dqv:QualityAnnotation a owl:Class ;
  rdfs:label "Quality Annotation"@en ;
  rdfs:comment "Represents quality annotations about a dataset."@en ;
  rdfs:isDefinedBy <http://www.w3.org/ns/dqv#> .
```

**Conventions for Import vs Prefix vs MIREOT:**

1. **Full owl:imports** - ONLY when:

   - Using >20 terms from the ontology
   - Need reasoning over imported axioms
   - Ontology is small (<100 terms)
   - **FSAR Tracer:** NONE qualify

2. **MIREOT** - Use when:

   - Need 3-20 specific terms
   - Want label/definition for documentation
   - Don't need full ontology reasoning
   - **FSAR Tracer:** BFO (3 terms), IAO (keep existing 4), DQV (5 terms)

3. **Prefix only** - Use when:

   - Using properties, not classes
   - Terms are universally known (SKOS, DC)
   - Pure data typing (xsd:)
   - **FSAR Tracer:** PROV-O, RO, SKOS, DwC, Schema.org

## FSAR Tracer Ontology Additions (Minimal)

### 1. Core Provenance Classes (8-Week MVP)

**File:** `ontology/dfo-salmon.ttl`

Add after line 850 (after existing stock assessment classes):

```turtle
#################################################################
# FSAR Tracer Evidence Chain Classes (MVP)
#################################################################

dfo:StatusAssessment a owl:Class ;
  rdfs:label "Status Assessment"@en ;
  rdfs:comment "Assessment of stock status relative to reference points for a specific year and SMU."@en ;
  rdfs:subClassOf bfo:0000015 ;  # process (via MIREOT)
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:ScientificOutput a owl:Class ;
  rdfs:label "Scientific Output"@en ;
  rdfs:comment "FSAR advice text, recommendations, or assessment summaries with provenance."@en ;
  rdfs:subClassOf iao:0000030 ;  # information content entity
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:ManagementDecision a owl:Class ;
  rdfs:label "Management Decision"@en ;
  rdfs:comment "Fishery management decision (TAC, HCR, rebuilding) based on scientific advice."@en ;
  rdfs:subClassOf bfo:0000015 ;  # process
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:AnalysisMethod a owl:Class ;
  rdfs:label "Analysis Method"@en ;
  rdfs:comment "Statistical or computational method used in stock assessment (e.g., SR benchmark, run reconstruction)."@en ;
  rdfs:subClassOf bfo:0000015 ;  # process
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

### 2. PROV-O Properties (Use Directly, No Import)

**File:** `ontology/dfo-salmon.ttl`

Add prefix declaration (line 9):

```turtle
@prefix prov:    <http://www.w3.org/ns/prov#> .
```

Document usage patterns (NO owl:imports):

```turtle
#################################################################
# FSAR Tracer Provenance Pattern (PROV-O properties used directly)
#################################################################

# StatusAssessment prov:used Dataset
# StatusAssessment prov:used ReferencePoint
# StatusAssessment prov:wasGeneratedBy AnalysisMethod
# StatusAssessment prov:wasAttributedTo Agent

# ScientificOutput prov:wasDerivedFrom StatusAssessment
# ScientificOutput prov:wasAttributedTo PeerReviewCommittee

# ManagementDecision prov:used ScientificOutput
```

### 3. Evidence Completeness (DQV via MIREOT)

**File:** `ontology/dfo-salmon.ttl`

Add DQV prefix (line 9):

```turtle
@prefix dqv:     <http://www.w3.org/ns/dqv#> .
```

Import only needed DQV terms via MIREOT (~line 250):

```turtle
#################################################################
# Data Quality Vocabulary (DQV) - MIREOT Import
#################################################################

dqv:Dimension a owl:Class ;
  rdfs:label "Dimension"@en ;
  rdfs:comment "Represents criteria relevant for assessing quality."@en ;
  rdfs:isDefinedBy <http://www.w3.org/ns/dqv#> .

dqv:QualityAnnotation a owl:Class ;
  rdfs:label "Quality Annotation"@en ;
  rdfs:comment "Represents quality annotations, including ratings."@en ;
  rdfs:isDefinedBy <http://www.w3.org/ns/dqv#> .

dqv:inDimension a owl:ObjectProperty ;
  rdfs:label "in dimension"@en ;
  rdfs:comment "Links a quality annotation to the dimension it measures."@en ;
  rdfs:isDefinedBy <http://www.w3.org/ns/dqv#> .

# Evidence completeness dimensions
dfo:EvidenceCompletenessDimension a dqv:Dimension ;
  skos:prefLabel "Evidence Completeness"@en ;
  skos:definition "Dimension measuring presence of all required evidence fields."@en .

dfo:DataCurrencyDimension a dqv:Dimension ;
  skos:prefLabel "Data Currency"@en ;
  skos:definition "Dimension measuring how up-to-date data is (timestamp freshness)."@en .

# Evidence badges (quality annotations)
dfo:CompleteEvidence a dqv:QualityAnnotation ;
  skos:prefLabel "Complete"@en ;
  dqv:inDimension dfo:EvidenceCompletenessDimension .

dfo:GapsEvidence a dqv:QualityAnnotation ;
  skos:prefLabel "Gaps"@en ;
  dqv:inDimension dfo:EvidenceCompletenessDimension .

dfo:MissingCriticalEvidence a dqv:QualityAnnotation ;
  skos:prefLabel "Missing-Critical"@en ;
  dqv:inDimension dfo:EvidenceCompletenessDimension .
```

### 4. Required Fields for Evidence Completeness

**File:** `ontology/dfo-salmon.ttl`

Add datatype properties for FSAR Tracer fields (~line 1400):

```turtle
#################################################################
# FSAR Tracer Required Fields (Evidence Completeness)
#################################################################

dfo:data_source_type a owl:DatatypeProperty ;
  rdfs:label "data source type"@en ;
  rdfs:comment "Type of data source (direct, proxy, genetic proxy, etc.)"@en ;
  rdfs:domain dfo:EscapementMeasurement ;
  rdfs:range xsd:string .

dfo:proxy_justification a owl:DatatypeProperty ;
  rdfs:label "proxy justification"@en ;
  rdfs:comment "Justification for using proxy data when data_source_type is proxy."@en ;
  rdfs:domain dfo:EscapementMeasurement ;
  rdfs:range xsd:string .

dfo:method_name a owl:DatatypeProperty ;
  rdfs:label "method name"@en ;
  rdfs:domain dfo:AnalysisMethod ;
  rdfs:range xsd:string .

dfo:method_version a owl:DatatypeProperty ;
  rdfs:label "method version"@en ;
  rdfs:domain dfo:AnalysisMethod ;
  rdfs:range xsd:string .

dfo:code_commit a owl:DatatypeProperty ;
  rdfs:label "code commit"@en ;
  rdfs:comment "Git commit hash or tag for reproducibility."@en ;
  rdfs:domain dfo:AnalysisMethod ;
  rdfs:range xsd:string .

dfo:reviewer a owl:ObjectProperty ;
  rdfs:label "reviewer"@en ;
  rdfs:comment "Person or committee who reviewed the assessment."@en ;
  rdfs:range dwc:Agent .

dfo:date a owl:DatatypeProperty ;
  rdfs:label "date"@en ;
  rdfs:comment "Date of assessment, review, or decision."@en ;
  rdfs:range xsd:date .
```

### 5. BFO Upper Ontology Grounding (MIREOT)

**File:** `ontology/dfo-salmon.ttl`

Update BFO prefix to keep it (line 2):

```turtle
@prefix bfo:     <http://purl.obolibrary.org/obo/BFO_> .
```

Add MIREOT imports for BFO (~line 240):

```turtle
#################################################################
# Basic Formal Ontology (BFO) - MIREOT Import
# Upper ontology grounding for process/entity/quality hierarchy
#################################################################

bfo:0000015 a owl:Class ;
  rdfs:label "process"@en ;
  oboInOwl:hasDefinition "An occurrent that has temporal parts."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

bfo:0000040 a owl:Class ;
  rdfs:label "material entity"@en ;
  oboInOwl:hasDefinition "An independent continuant that is spatially extended."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

bfo:0000031 a owl:Class ;
  rdfs:label "generically dependent continuant"@en ;
  oboInOwl:hasDefinition "A continuant that is dependent on one or more independent continuants."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .
```

Update DwC mappings section (lines 219-234) to use BFO properly:

```turtle
#################################################################
# Class Mappings to Darwin Core and BFO Upper Ontology
#################################################################

# Material entities (BFO grounding)
dwc:Organism rdfs:subClassOf bfo:0000040 .  # material entity
dwc:MaterialEntity rdfs:subClassOf bfo:0000040 .
dwc:Agent rdfs:subClassOf bfo:0000040 .

# Processes (BFO grounding)
dwc:Event rdfs:subClassOf bfo:0000015 .  # process
dwc:Occurrence rdfs:subClassOf bfo:0000015 .
dwc:Identification rdfs:subClassOf bfo:0000015 .

# Information entities (IAO, not BFO)
dwc:Protocol rdfs:subClassOf iao:0000030 .  # information content entity
```

## DPROD Investigation (Defer to Week 3)

**Current Assessment:** DPROD namespace `https://www.omg.org/spec/DPROD/1.0/` may not be resolvable. Alternative: use `dcat:Dataset` + `schema:Dataset` which are W3C standards.

**MVP Approach:** Use existing `dfo:Dataset` + `schema:Dataset` for MVP. Investigate DPROD for post-MVP.

**Rationale:** Evidence chain works with basic Dataset concept; DPROD adds complexity without MVP value.

## Relations Ontology (RO) - Pragmatic Alignment

**Current:** `dfo:hasMember`, `dfo:isMemberOf` are custom properties.

**MVP Approach:** Document RO alignment in comments but DON'T import RO or create subproperties yet.

**File:** `ontology/dfo-salmon.ttl`

Update membership relations section (lines 1010-1020):

```turtle
#################################################################
# Roll-up / Partonomy pattern: SMU ▶ CU ▶ Stock
# NOTE: Aligned with RO:0002131 (has_member) and RO:0002350 (member_of)
# but implemented as independent properties to avoid RO import overhead
#################################################################

dfo:hasMember a owl:ObjectProperty , owl:TransitiveProperty ;
  rdfs:label "has member"@en ;
  rdfs:comment "Hierarchical membership. Semantically aligned with RO:0002131 (has_member)."@en ;
  rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002131> ;
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:isMemberOf a owl:ObjectProperty ;
  rdfs:label "is member of"@en ;
  rdfs:comment "Inverse of hasMember. Semantically aligned with RO:0002350 (member_of)."@en ;
  rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002350> ;
  owl:inverseOf dfo:hasMember ;
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

## Documentation Updates

### 1. CONVENTIONS.md - Import Policy Section

**File:** `docs/CONVENTIONS.md`

Add new section 2.3.6 after existing conventions:

#### 2.3.6 Ontology Import Strategy

**Three Approaches: Import vs MIREOT vs Prefix**

**1. Full owl:imports** (NOT used in FSAR Tracer MVP)

- Use ONLY when: Using >20 terms AND need reasoning over imported axioms
- Risk: Imports entire ontology (100s-1000s of terms); slow loading; potential conflicts
- **FSAR Tracer:** No full imports

**2. MIREOT (Minimum Information to Reference an External Ontology Term)**

- Use when: Need 3-20 specific terms with labels/definitions
- Method: Copy term IRI, label, definition into our ontology
- Benefits: Lightweight; no import bloat; clear documentation
- **FSAR Tracer:** BFO (3 terms), DQV (5 terms), IAO (existing 4 terms)

**3. Prefix declarations only**

- Use when: Using properties only OR terms are universally known
- Method: Declare prefix; use terms directly; no local definitions
- Benefits: Minimal overhead; assumes external ontology is accessible
- **FSAR Tracer:** PROV-O, RO (alignment only), SKOS, DwC, Schema.org

**FSAR Tracer Import Decisions:**

| Ontology | Approach | Terms Used | Rationale |

|----------|----------|------------|-----------|

| BFO | MIREOT | 3 (process, material entity, generically dependent continuant) | Upper ontology grounding |

| IAO | MIREOT | 4 (measurement datum, value spec, information entity, directive) | Information artifacts |

| DQV | MIREOT | 5 (Dimension, QualityAnnotation, inDimension, Metric, Category) | Evidence completeness |

| PROV-O | Prefix only | ~6 properties (wasGeneratedBy, wasDerivedFrom, used, wasAttributedTo) | Provenance relations |

| RO | Prefix only | Alignment via rdfs:seeAlso | Semantic alignment documentation |

| DPROD | Defer | TBD | Investigate post-MVP |

| SKOS | Prefix only | Extensive (schemes, concepts) | Core W3C vocab |

| DwC | Prefix only | Extensive (classes, properties) | Biodiversity standard |

**Why This Matters:**

- **Performance:** MIREOT = fast loading; full imports = slow
- **Clarity:** Local term definitions aid understanding
- **Maintenance:** Fewer dependencies = easier updates
- **Interoperability:** Pragmatic balance between standards compliance and usability

### 2. Update README.md

**File:** `README.md`

Update Technical Overview (lines 67-75):

```markdown
## Technical Overview

- **One file**: `dfo-salmon.ttl` (OWL/Turtle)
- **Hybrid approach**: OWL for formal relationships, SKOS for controlled vocabularies
- **Darwin Core aligned**: Uses DwC classes as top-level framework for interoperability
- **OBO Foundry principles**: Open, interoperable, logically well-formed, scientifically accurate
- **Pragmatic imports**: MIREOT for BFO/IAO/DQV (~12 terms); prefix-only for PROV-O/RO/SKOS
- **Upper ontology**: BFO grounding for process/entity hierarchy
- **Provenance**: PROV-O properties for FSAR evidence chains
- **Quality**: DQV dimensions for evidence completeness tracking
```

Add FSAR Tracer section to Ontology Scope (after line 130):

```markdown
**FSAR Tracer (Evidence Chain)**

- Classes: `dfo:StatusAssessment, dfo:ScientificOutput`, `dfo:ManagementDecision`, `dfo:AnalysisMethod`
- Provenance: PROV-O properties (`prov:wasGeneratedBy`, `prov:wasDerivedFrom`, `prov:used`)
- Quality: DQV dimensions (`dfo:EvidenceCompletenessDimension`, `dfo:DataCurrencyDimension`)
- Badges: `dfo:CompleteEvidence`, `dfo:GapsEvidence`, `dfo:MissingCriticalEvidence`
- Required fields: `data_source_type`, `proxy_justification`, `method_name`, `code_commit`, `reviewer`, `date`
```

### 3. Update todo_list.md (Complete Rewrite)

**File:** `docs/todo_list.md`

Replace entire file with FSAR Tracer-focused plan:

# DFO Salmon Ontology - FSAR Tracer MVP Todo List

**Focus:** 8-week path to Barkley Sockeye FSAR evidence chain demo

**Goal:** Six-node trace (Data → Method → RefPoints → Status → Advice → Decision) with badges

## Week 1: Core Ontology Updates

### Task 1.1: MIREOT Imports for BFO + DQV

- [ ] Add BFO MIREOT definitions (process, material entity, gen dependent continuant)
- [ ] Add DQV MIREOT definitions (Dimension, QualityAnnotation, inDimension)
- [ ] Keep existing IAO MIREOT terms
- [ ] Update DwC-to-BFO mappings to use proper BFO classes
- [ ] Test ontology loads in Protégé

### Task 1.2: FSAR Tracer Core Classes

- [ ] Add `dfo:StatusAssessment` (subclass of bfo:process)
- [ ] Add `dfo:ScientificOutput` (subclass of iao:information content entity)
- [ ] Add `dfo:ManagementDecision` (subclass of bfo:process)
- [ ] Add `dfo:AnalysisMethod` (subclass of bfo:process)
- [ ] Document PROV-O usage pattern (prefix-only, no import)

### Task 1.3: Evidence Completeness Dimensions

- [ ] Create `dfo:EvidenceCompletenessDimension` as dqv:Dimension
- [ ] Create `dfo:DataCurrencyDimension` as dqv:Dimension
- [ ] Create quality annotations: CompleteEvidence, GapsEvidence, MissingCriticalEvidence
- [ ] Link annotations to dimensions via dqv:inDimension

## Week 2: Required Fields & SHACL Shapes

### Task 2.1: Add FSAR Required Fields

- [ ] Add `dfo:data_source_type` property
- [ ] Add `dfo:proxy_justification` property
- [ ] Add `dfo:method_name`, `method_version`, `code_commit` properties
- [ ] Add `dfo:reviewer` property (range: dwc:Agent)
- [ ] Add `dfo:date` property

### Task 2.2: SHACL Shapes for Evidence Completeness

- [ ] Create shape for required fields by decision context (TAC/HCR)
- [ ] Add constraint: if data_source_type=proxy, proxy_justification required
- [ ] Add constraint: method must have name, version, code_commit
- [ ] Add constraint: status must have reviewer and date
- [ ] Test shapes with sample Barkley data

## Week 3: SPARQL Queries for UI

### Task 3.1: Core Competency Queries

- [ ] Implement Q1: Evidence Completeness by Decision
- [ ] Implement Q2: Proxy Without Justification
- [ ] Implement Q3: Method Reproducibility
- [ ] Implement Q4: Reference Points Used
- [ ] Test queries return expected results

### Task 3.2: Data Currency Queries

- [ ] Implement Q5: Missing Uncertainty
- [ ] Implement Q6: Data Currency (last updated per component)
- [ ] Implement Q7: Scientific Output Text + Review
- [ ] Implement Q8: Linked Documents
- [ ] Create query pack documentation

## Week 4: Sample Data & JSON-LD

### Task 4.1: Barkley Sockeye Sample Data

- [ ] Create sample StatusAssessment instance for Barkley 2025
- [ ] Create sample ScientificOutput instance
- [ ] Create sample ManagementDecision instance
- [ ] Link instances with PROV-O properties
- [ ] Annotate with DQV quality dimensions

### Task 4.2: JSON-LD Context & Export

- [ ] Create JSON-LD @context for FSAR terms
- [ ] Export sample data as JSON-LD
- [ ] Test JSON-LD loads into Fuseki
- [ ] Validate against SHACL shapes
- [ ] Document JSON-LD export process

## Weeks 5-8: Graph DB + UI (Outside Ontology Scope)

- Graph database setup (Fuseki)
- Django HTMX interface
- Evidence badges implementation
- Evidence drawer UI
- Export pack generation

## Deferred (Post-MVP)

- DPROD investigation and integration
- Full RO subproperty alignment
- Estimate type automated assignment
- SIL/SEN integration
- Multi-SMU support

## Notes

- **Import strategy:** MIREOT for BFO/IAO/DQV; prefix-only for PROV-O/RO
- **BFO decision:** Keep and use properly via MIREOT; provides upper ontology grounding
- **DPROD decision:** Defer to post-MVP; use schema:Dataset for now
- **RO decision:** Document alignment but don't create subproperties yet
- **Focus:** Shortest path to working FSAR Tracer demo for Barkley Sockeye