# DFO Salmon Ontology — Conventions Guide

This document orients new contributors to the modeling conventions used in the **DFO Salmon Ontology**. It explains how to create and refine ontology terms, how to model data in a way that aligns with our goals, and how to prepare new concepts for integration.

The conventions here are **practical starting points**, not immutable rules. As our community gains experience, we expect to refine and evolve them.

### Scope and Standards

- Scope (this guide):
  - How to do things (operational guidance)
  - Standards and patterns (naming conventions, required annotations)
  - Quality checklists (what to check before submitting)
  - Tool usage (Protégé, ROBOT commands)
  - Modeling patterns (measurements, hierarchies, evidence, provenance)
  - Workflow processes (how to contribute, review)
- ADRs are for: why decisions were made, alternatives considered, high‑level strategy, technology/structural choices.
- Standards compliance: We strictly adhere to OWL 2 DL, and support SKOS 1.2 and RDF 1.2.

---

## 🚀 Quick Start Cheatsheet

**For experienced contributors who need a quick reference:**

### Essential Elements (Every Term Needs)

- **Label**: `rdfs:label "Human Name"@en`
- **Definition**: `rdfs:comment "1–2 sentence definition."@en`
- **Source**: `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`

### Naming Conventions

- **Classes**: PascalCase (e.g., `EscapementMeasurement`)
- **Properties**: lowerCamelCase (e.g., `aboutStock`, `usesMethod`)
- **SKOS Concepts**: PascalCase (e.g., `SonarCounting`)

### Core Patterns

- **Hierarchy**: SMU ▶ CU ▶ Population with `hasMember` relationships (use correct OWL 2 transitivity syntax)
- **Units**: Store QUDT IRIs as literals in `…UnitIRI` properties
- **Darwin Core**: Use as top-level classes for interoperability
- **Hybrid Approach**: SKOS for controlled vocab/enumerations/code lists (including methods); OWL for domain entities; SHACL for validation (not inference)
- **OBO Relations Ontology for Relations**: Check the [Relations Ontology](https://obofoundry.org/ontology/ro.html) first before defining new relations; use subproperties when extending

### Quality Checklist

- [ ] Can answer a competency question?
- [ ] Follows established design patterns?
- [ ] All required annotations present?
- [ ] Integrates with existing hierarchy?
- [ ] Tested with sample data?
- [ ] Schema only (no instance data in ontology file)?

---

## 📚 Table of Contents

1. [Fundamentals](#1-fundamentals)

   - [1.1 What is Knowledge Modeling?](#11-what-is-knowledge-modeling)
   - [1.2 Ontology vs Knowledge Graph vs Graph Database](#12-ontology-vs-knowledge-graph-vs-graph-database)
   - [1.3 Why This Ontology?](#13-why-this-ontology)
   - [1.4 Modeling Approach](#14-modeling-approach)

2. [Getting Started](#2-getting-started)

   - [2.1 Essential Concepts](#21-essential-concepts)
   - [2.2 Schema vs Data Separation](#22-schema-vs-data-separation)
   - [2.3 Core Conventions](#23-core-conventions)
   - [2.4 Hybrid Modeling Approach](#24-hybrid-modeling-approach-for-automated-classification)
   - [2.5 Data Validation with SHACL](#25-data-validation-with-shacl)
   - [2.6 Naming Conventions](#26-naming-conventions)

3. [Design Patterns](#3-design-patterns)

   - [3.1 Measurement Patterns](#31-measurement-patterns)
   - [3.2 Hierarchy Patterns](#32-hierarchy-patterns)
   - [3.3 Event Patterns](#33-event-patterns)

4. [Darwin Core Integration](#4-darwin-core-integration)

5. [Quality Assurance](#5-quality-assurance)

   - [5.1 Pre-Submission Checklist](#51-pre-submission-checklist)
   - [5.2 Validation Steps](#52-validation-steps)
   - [5.3 Common Mistakes](#53-common-mistakes)

6. [Advanced Topics](#6-advanced-topics)

   - [6.1 Competency Questions](#61-competency-questions)
   - [6.2 Troubleshooting](#62-troubleshooting)
   - [6.3 External Alignments](#63-external-alignments)

7. [Resources](#7-resources)
   - [7.1 Tools and Workflows](#71-tools-and-workflows)
   - [7.2 Community Process](#72-community-process)
   - [7.3 Key Takeaways](#73-key-takeaways)

---

## 1. Fundamentals

This introductory material has moved to a dedicated onboarding guide for clarity and easier learning.

- Read: docs/onboarding.md for Fundamentals (what is modeling, ontology vs knowledge graph, why this ontology, basic approach).
- This Conventions guide focuses on “how we do things” (operational guidance, patterns, QA, tools, workflows).

---

## 2. Getting Started

### 2.1 Essential Concepts

**What are classes?** Classes represent categories or types of things in your domain. For example, "Stock", "SurveyEvent", and "GeneticSample" are all classes. They're like the nouns in your vocabulary.

**What are properties?** Properties describe relationships between things or attributes of things. For example, "aboutStock" describes which stock a measurement is about, and "usesMethod" describes which method was used.

**What are instances?** Instances are specific examples of classes. For example, "SkeenaSockeye" is an instance of the "Stock" class.

### 2.2 Schema vs Data Separation

**Critical Rule: Keep the Ontology File Clean**

The `dfo-salmon.ttl` file must contain **schema elements only** - no instance data. This separation is essential for maintainability, versioning, and interoperability.

**What Goes in the Ontology File (`dfo-salmon.ttl`):**

- **OWL Classes**: `EscapementSurveyEvent`, `Stock`, `Measurement`
- **OWL Properties**: `usesEnumerationMethod`, `aboutStock`, `hasCountValue`
- **SKOS Concepts**: `SnorkelSurvey`, `Type2`, `VISITS`
- **Axioms and Rules**: Class restrictions, equivalence axioms, SHACL shapes
- **Metadata**: Labels, definitions, sources, examples

**What Does NOT Go in the Ontology File:**

- **Instance Data**: Specific survey events, stock measurements, count values
- **Temporal Data**: Data from specific years, seasons, or time periods
- **Location-Specific Data**: Data tied to specific rivers, regions, or sites
- **Raw Measurements**: Actual count values, efficiency rates, coverage percentages

**Where to Store Instance Data:**

- **Separate RDF files**: `survey-data-2022.ttl`, `stock-data-2023.ttl`
- **Graph databases**: Neo4j, Amazon Neptune, Apache Jena TDB
- **Data management systems**: Custom applications with RDF storage

**Example of Proper Separation:**

```turtle
# IN dfo-salmon.ttl (Schema Only)
:EscapementSurveyEvent a owl:Class ;
    rdfs:label "Escapement Survey Event"@en ;
    rdfs:comment "A specific survey event with measured parameters"@en ;
    rdfs:subClassOf dwc:Event .

:SnorkelSurvey a skos:Concept ;
    skos:prefLabel "Visual Snorkel Count"@en ;
    skos:definition "Two or more trained snorkelers conduct standardized passes"@en .

# IN survey-data-2022.ttl (Instance Data Only)
:SkeenaSnorkel2022_001 a :EscapementSurveyEvent ;
    dfo:usesEnumerationMethod :SnorkelSurvey ;
    dfo:measuredVisits 6 ;
    dfo:measuredReachCoverage 0.85 ;
    dwc:eventDate "2022-08-15"^^xsd:date .
```

**Benefits of This Separation:**

- **Stable Schema**: Ontology changes independently of data updates
- **Reusable**: Same schema can be used for multiple datasets
- **Maintainable**: Easier to validate and update schema separately
- **Interoperable**: Other systems can import just the schema
- **Versionable**: Schema and data can have different versioning cycles

**SHACL Validation:**

- **Schema Validation**: SHACL shapes in the ontology file validate data structure
- **Data Validation**: Apply SHACL shapes to instance data files
- **Quality Assurance**: Ensures data conforms to schema requirements

### 2.3 Core Conventions

#### 2.3.1 Classes

**Required elements for every class:**

- **Type declaration:** `a owl:Class` - This tells the system this is a class
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name in English
- **Definition:** `rdfs:comment "1–2 sentence definition."@en` - A clear explanation of what this class represents
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>` - Links back to our ontology

**Why these are required:** Labels help humans understand what you mean, definitions prevent confusion about scope, and source attribution ensures proper credit and traceability.

**Example:**

```turtle
:GeneticSample a owl:Class ;
    rdfs:label "Genetic Sample"@en ;
    rdfs:comment "Tissue or material used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;
    dcterms:source "DFO Molecular Genetics Lab glossary 2024" ;
    oboInOwl:hasExactSynonym "DNA sample"@en .
```

#### 2.3.2 Object Properties

**What are object properties?** Object properties link instances of one class to instances of another class. For example, "aboutStock" links a measurement to a stock.

**Required elements for every object property:**

- **Type declaration:** `a owl:ObjectProperty`
- **Label:** `rdfs:label "Human Name"@en`
- **Definition:** `rdfs:comment "1–2 sentence definition."@en`
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`

**Optional but recommended:**

- **Domain:** `rdfs:domain :ClassName` - What type of thing this property describes
- **Range:** `rdfs:range :ClassName` - What type of thing this property points to
- **Source:** `dcterms:source "Reference to where this came from"`
- **Example:** `dcterms:description "Example usage"`

**OBO annotation properties:**

- **Definition:** `oboInOwl:hasDefinition` - Formal definition
- **Exact synonym:** `oboInOwl:hasExactSynonym` - Alternative names with same meaning
- **Related synonym:** `oboInOwl:hasRelatedSynonym` - Related but not identical terms
- **Broad synonym:** `oboInOwl:hasBroadSynonym` - More general terms
- **Narrow synonym:** `oboInOwl:hasNarrowSynonym` - More specific terms
- **Database cross-reference:** `oboInOwl:hasDbXref` - Links to external databases

**Example:**

```turtle
:aboutStock a owl:ObjectProperty ;
    rdfs:label "about stock"@en ;
    rdfs:comment "Links a measurement or observation to the specific stock it describes."@en ;
    rdfs:domain :Measurement ;
    rdfs:range :Stock ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;
    dcterms:source "DFO stock assessment protocols 2024" .
```

#### 2.3.3 Datatype Properties

**What are datatype properties?** Datatype properties link instances to literal values (text, numbers, dates). For example, "measurementValue" links a measurement to its numeric value.

**Required elements for every datatype property:**

- **Type declaration:** `a owl:DatatypeProperty`
- **Label:** `rdfs:label "Human Name"@en`
- **Definition:** `rdfs:comment "1–2 sentence definition."@en`
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`

**Optional but recommended:**

- **Domain:** `rdfs:domain :ClassName`
- **Range:** `rdfs:range xsd:datatype` (e.g., `xsd:string`, `xsd:integer`, `xsd:date`)
- **Source:** `dcterms:source "Reference to where this came from"`

**Example:**

```turtle
:measurementValue a owl:DatatypeProperty ;
    rdfs:label "measurement value"@en ;
    rdfs:comment "The numeric value of a measurement."@en ;
    rdfs:domain :Measurement ;
    rdfs:range xsd:decimal ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

#### 2.3.4 SKOS Concepts

**What are SKOS concepts?** SKOS concepts are for controlled vocabularies - lists of standardized terms like methods, categories, or codes. Use SKOS when you need a picklist rather than a complex class hierarchy.

**Terminology vs Ontology:**

- **Terminology**: A collection of terms with definitions and synonyms (like a dictionary)
- **Ontology**: A formal classification with logical relationships between terms (like a structured knowledge base)
- **Our approach**: We use OWL for formal relationships and SKOS for simple controlled vocabularies

**Required elements for every SKOS concept:**

- **Type declaration:** `a skos:Concept`
- **Label:** `skos:prefLabel "Human Name"@en`
- **Definition:** `skos:definition "1–2 sentence definition."@en`
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`

**Note on ROBOT Validation:** ROBOT reports missing `rdfs:label` for SKOS concepts that have `skos:prefLabel`. This is a ROBOT limitation - per W3C SKOS specification, `skos:prefLabel` is a subproperty of `rdfs:label`, so these concepts ARE properly labeled. Do not add redundant `rdfs:label` properties to satisfy ROBOT.

**Example:**

```turtle
:SonarCounting a skos:Concept ;
    skos:prefLabel "Sonar Counting"@en ;
    skos:definition "Method of counting fish using sonar technology."@en ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;
    skos:broader :CountingMethod .
```

#### 2.3.5 Provenance and Citation Conventions

#### 2.3.5.1 Use of `dcterms:source`, `dcterms:bibliographicCitation`, and `rdfs:seeAlso`

To ensure consistent provenance documentation and FAIR compliance, follow these conventions when citing the source of a definition, dataset, or external standard:

| Property                            | Purpose                                                               | Expected Value Type | Example Use                                                              |
| ----------------------------------- | --------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| **`dcterms:source`**                | Persistent identifier (DOI/Handle/w3id/ARK) for the source resource.  | IRI                 | `<https://doi.org/10.1234/dfostock.2023>`                                |
| **`dcterms:bibliographicCitation`** | Human-readable citation text for the source.                          | Literal (string)    | `"DFO (2023). Escapement Survey Manual, Pacific Region."@en`             |
| **`rdfs:seeAlso`**                  | Optional landing page or download URL for browsers and accessibility. | IRI                 | `<https://open.canada.ca/data/en/dataset/escapement-survey-manual-2023>` |

**Guideline:**  
Use `dcterms:source` for the _persistent identifier_ (prefer DOI/Handle/w3id/ARK), `dcterms:bibliographicCitation` for the _human-readable citation text_, and optionally `rdfs:seeAlso` for _landing pages or download URLs_.

---

#### 2.3.5.2 Example — Class Definition with Proper Citation

```turtle
:EscapementSurveyEvent a owl:Class ;
    rdfs:label "Escapement Survey Event"@en ;
    rdfs:comment "A survey event conducted to measure salmon escapement."@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;

    # Non-literal source (preferred: DOI or other persistent IRI)
    dcterms:source <https://doi.org/10.1234/dfostock.2023> ;

    # Human-readable citation text
    dcterms:bibliographicCitation
        "DFO (2023). Escapement Survey Manual, Pacific Region. Fisheries and Oceans Canada."@en ;

    # Optional: landing page or download URL
    rdfs:seeAlso <https://open.canada.ca/data/en/dataset/escapement-survey-manual-2023> .
```

**Explanation:**

- `dcterms:source` provides a _persistent identifier_ (DOI) that machines can resolve.
- `dcterms:bibliographicCitation` provides a _human-readable citation_ following standard bibliographic format.
- `rdfs:seeAlso` provides a _landing page URL_ for easy access and browser navigation.

---

#### 2.3.5.3 Example — Dataset or External Resource Reference

```turtle
:BaselineGeneticDataset a owl:Class ;
    rdfs:label "Baseline Genetic Dataset"@en ;
    rdfs:comment "A curated collection of reference genotypes used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;

    # Persistent identifier for the dataset
    dcterms:source <https://doi.org/10.1234/dfo-baseline-genotype-2024> ;

    # Human-readable citation
    dcterms:bibliographicCitation
        "DFO Molecular Genetics Laboratory (2024). Baseline Genotype Reference Collection. Fisheries and Oceans Canada."@en ;

    # Optional: data portal landing page
    rdfs:seeAlso <https://open.canada.ca/data/en/dataset/dfo-baseline-genotype-reference-collection> .
```

---

#### 2.3.5.4 Key Points

- ✅ Use **IRI** for `dcterms:source` — prefer DOI/Handle/w3id/ARK for persistence
- ✅ Use **`dcterms:bibliographicCitation`** for human-readable citation text (not `dcterms:source`)
- ✅ Use **`rdfs:seeAlso`** optionally for landing pages or download URLs
- ✅ This pattern aligns with DCMI and W3C best practices for provenance and citation

### 2.3.6 External Vocabulary Integration Strategy

**Decision:** We use a pragmatic three-tier approach for external vocabulary integration. See [ADR-005: External Vocabulary Integration Strategy](../adr/005-external-vocabulary-integration.md) for the complete rationale and alternatives considered.

**Implementation:**

#### MIREOT Implementation (BFO/IAO/DQV)

**Method:**
1. Copy the term IRI (e.g., `bfo:0000015`)
2. Add minimal metadata: `rdfs:label`, `oboInOwl:hasDefinition` (or `rdfs:comment`)
3. Add `rdfs:isDefinedBy` pointing to source ontology
4. Use the term as if it were native

**Example - BFO MIREOT:**
```turtle
# Import specific BFO term via MIREOT
bfo:0000015 a owl:Class ;
  rdfs:label "process"@en ;
  oboInOwl:hasDefinition "An occurrent that has temporal parts."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

# Now use it in your ontology
dfo:StatusAssessment rdfs:subPropertyOf bfo:0000015 .  # process
```

**DFO Salmon MIREOT Terms:**
- **BFO** (3 terms): process, material entity, generically dependent continuant
- **IAO** (4 terms): measurement datum, value specification, information content entity, directive information entity
- **DQV** (5 terms): Dimension, QualityAnnotation, inDimension, Metric, Category

#### 2.3.6.1 Upper Ontology Rationale (BFO)

We use BFO as our upper ontology to anchor classes in a coherent hierarchy of continuants (e.g., stocks, samples) versus occurrents (events, processes). This improves consistency (no class should represent both a thing and an event) and aligns with OBO Foundry best practices. To keep the ontology lightweight, we MIREOT only a small set of BFO classes (e.g., process, material entity, generically dependent continuant) needed for high-level placement and documentation.

Note: This short rationale summarizes the why. If expanded with alternatives and trade-offs, consider capturing it as a dedicated ADR.

DwC positioning: The Darwin Core Conceptual Model is treated as a domain‑specific mid‑level model beneath BFO. We align DwC classes under appropriate BFO categories (e.g., `dwc:Event` ≈ BFO process; `dwc:Organism` ≈ BFO material entity; `dwc:Assertion`/occurrence records ≈ information content entities, when used that way), then subclass our domain classes under DwC terms.

#### Prefix-Only Implementation (PROV-O/RO/SKOS/DwC)

**Method:**
1. Declare prefix: `@prefix prov: <http://www.w3.org/ns/prov#>`
2. Use terms directly in your ontology
3. No local definitions needed
4. Assumes external ontology is accessible

**Example - PROV-O Prefix Only:**
```turtle
# Declare prefix (no import, no local definitions)
@prefix prov: <http://www.w3.org/ns/prov#> .

# Use PROV-O properties directly
:BarkleyStatus2025 prov:used :EscapementDataset2025 ;
  prov:wasGeneratedBy :SRBenchmarkMethod ;
  prov:wasAttributedTo :StockAssessmentTeam .
```

**DFO Salmon Prefix-Only:**
- **PROV-O** (~6 properties): wasGeneratedBy, wasDerivedFrom, used, wasAttributedTo, etc.
- **RO** (alignment via rdfs:seeAlso): has_member, member_of
- **SKOS** (extensive): Concept, ConceptScheme, prefLabel, definition, etc.
- **DwC** (extensive): Event, Organism, Assertion, MaterialSample, etc.

#### Key Ontologies and Recommended Usage (Concise)

- BFO (upper ontology): Retain as the top‑level; MIREOT only core classes (process, material entity, site) and assert domain classes under them for clarity.
- IAO (information artifacts): Use for documents and information entities (e.g., FSAR, advice text). MIREOT only needed terms; model `dfo:ScientificOutput ⊑ iao:0000030` (information content entity).
- Darwin Core (domain scaffolding): Subclass DFO domain classes under DwC (e.g., `dfo:SurveyEvent ⊑ dwc:Event`, `dfo:StatusAssessment ⊑ dwc:Assertion`). Treat DwC as mid‑level beneath BFO.
- Schema.org and DCAT (web/catalog): Keep `dfo:Dataset ⊑ schema:Dataset`; optionally align `dfo:Dataset ⊑ dcat:Dataset` for catalog compatibility; use DCAT properties (e.g., distributions) when publishing catalogs.
- PROV‑O (provenance): Prefix‑only; use relations (`prov:used`, `prov:wasGeneratedBy`, `prov:wasDerivedFrom`) without importing full classes.
- DQV (quality): Use `dqv:QualityAnnotation` and `dqv:inDimension` for evidence/quality badges; MIREOT minimal core.
- DPROD (data products): Evaluate post‑MVP; likely align `dfo:Dataset ⊑ dprod:Dataset` and describe services/distributions via DPROD.
- RO (relations): Prefer RO for fundamental relations; align custom properties as subproperties of RO (see 6.6).
- OBI (protocols/assays): Import specific terms only when clearly beneficial; avoid heavy imports.
- ENVO (environment): Use selectively for habitat/environment terms as annotations or links.
- ORG (organizations): Prefix‑only; use `org:Organization`/units for decision‑maker modeling.

#### Usage Guidelines

**When to use MIREOT:**
- Need 3-20 specific terms with labels/definitions
- Want documentation in your ontology
- Don't need reasoning over the full imported ontology

**When to use prefix-only:**
- Using properties only (not classes)
- Terms are universally known (SKOS, Dublin Core)
- Pure data typing (xsd:)
- Lightweight alignment without local definitions

**When NOT to use full imports:**
- Avoid importing entire external ontologies (100s-1000s of terms)
- Causes slow loading and reasoning
- Potential conflicts with other imports

### 2.3.7 PROV-O and DQV Usage Patterns

We use PROV-O for provenance and DQV for quality annotations that back UI badges and evidence checks.

Example (illustrative Turtle):

```turtle
:Assessment_X a dfo:StatusAssessment ;
  prov:used :Dataset_Y ;
  prov:wasGeneratedBy :AnalysisMethod_Z ;
  prov:wasDerivedFrom :ReferencePoint_Q .

:ReferencePoint_Q a dfo:ReferencePoint ;
  dfo:refPointType :LRP .

:Assessment_X_EvidenceComplete a dfo:CompleteEvidence ;
  dqv:inDimension dfo:EvidenceCompletenessDimension .

:Assessment_X dqv:hasQualityAnnotation :Assessment_X_EvidenceComplete .
```

How to apply:

- Before finalizing an assessment, attach a quality annotation indicating evidence state: `dfo:CompleteEvidence`, `dfo:GapsEvidence`, or `dfo:MissingCriticalEvidence`, linked by `dqv:hasQualityAnnotation` and categorized via `dqv:inDimension`.
- Use `prov:used`, `prov:wasGeneratedBy`, and `prov:wasDerivedFrom` to record datasets, methods, and reference points underpinning the assessment.

Uncertainty properties:

- For GSI composition measurements, record sample size via `dfo:gsi_sample_size` and 95% CI via `dfo:gsi_ci` (per GRD integration schema). Shapes in 2.5 can require these when applicable and flag omissions.

### 2.3.8 Modeling Choice: SKOS vs OWL Class vs Individual

Use this decision guide to choose the right modeling primitive:

- SKOS Concept
  - Use for controlled vocabulary/code-list values that don't need logical axioms or subclass hierarchies.
  - Examples: `spawner_origin` values (`:Wild`, `:Hatchery`), `data_source_type`, `reference_point_type`, `decision_type`, status zone values (`:RedZone`, `:AmberZone`, `:GreenZone`), **enumeration methods** (`:SnorkelSurvey`, `:SonarCounting`), and **estimate methods** (`:AreaUnderCurve`, `:FixedStationTally`).
  - Pattern: Use an object property whose range is `skos:Concept` (e.g., `dfo:statusZone` → `skos:Concept`, `dfo:usesEnumerationMethod` → `skos:Concept`).

- OWL Class
  - Use for fundamental domain entities or when hierarchy/specialization is needed.
  - Examples: `dfo:ConservationUnit`, `dfo:Stock`, `dfo:StatusAssessment`, `dfo:EscapementMethod` (methodological families for classification purposes).
  - Note: Enumeration and estimate methods (specific methods like Snorkel Survey, Area Under Curve) are modeled as SKOS concepts per ADR-001. The `dfo:EscapementMethod` OWL class hierarchy represents methodological families for broader classification, distinct from the SKOS enumeration/estimate method vocabularies.

- OWL Individual
  - Use for concrete, real-world instances (lives in data graphs, not the ontology schema file).
  - Examples: A specific CU instance (e.g., `:NanaimoRiverChinookCU_2024`), a policy document (e.g., `:WildSalmonPolicy_2005`), or a specific survey event instance (e.g., `:SkeenaSnorkel2022_001` a `:EscapementSurveyEvent`).
  - Note: Enumeration and estimate methods are SKOS concepts, not individuals. Use the SKOS concepts directly (e.g., `:SnorkelSurvey`, `:AreaUnderCurve`) in data instances rather than creating method instances.
  - Naming recommendation: PascalCase with disambiguators as needed (`:SkeenaSnorkel2022_001`, `:SkeenaSockeye`), or a short path-like fragment (`#Stock/SkeenaSockeye`). Avoid spaces; prefer stable, meaningful identifiers.

Do not duplicate the same concept as both an OWL class and a SKOS concept (or an individual) unless there is a deliberate bridge/mapping with documented rationale. Choose one approach based on the above rules to avoid ambiguity.

### 2.4 Hybrid Modeling Approach for Automated Classification

**Decision:** We use a hybrid approach combining OWL and SKOS for classification. Automated approaches are deferred; see [ADR-001: Hybrid OWL+SKOS Modeling Approach](../adr/001-hybrid-owl-skos-modeling.md) for the complete rationale and alternatives considered.

**Implementation:**

**Four-Layer Architecture:**

1. **Methods as SKOS Concepts** - Enumeration and estimation methods are SKOS concepts in controlled vocabularies (e.g., `:SnorkelSurvey`, `:SonarCounting`, `:AreaUnderCurve`, `:FixedStationTally`).
2. **Events as OWL Classes** - Survey/estimate events that extend Darwin Core Event
3. **Metadata on Events** - Rich data about how methods were applied in specific surveys
4. **Downgrade Criteria as SKOS** - Standardized criteria for type assignment (manual now; automation later)

**Complete Example:**

```turtle
# Layer 1: SKOS Methods (Controlled Vocabularies)
:SnorkelSurvey a skos:Concept ;
    skos:prefLabel "Visual Snorkel Count"@en ;
    skos:definition "Two or more trained snorkelers conduct standardized passes within defined segments"@en ;
    skos:inScheme :EnumerationMethodScheme ;
    skos:broader :EnumerationMethod .

:AreaUnderCurve a skos:Concept ;
    skos:prefLabel "Area Under the Curve (AUC)"@en ;
    skos:definition "Integrates serial counts over time using a survey-life parameter"@en ;
    skos:inScheme :EstimateMethodScheme ;
    skos:broader :EstimateMethod .

# Layer 2: SKOS Downgrade Criteria
:VISITS a skos:Concept ;
    skos:prefLabel "Number of visits"@en ;
    skos:definition "Too few site visits for the claimed precision tier"@en ;
    skos:inScheme :DowngradeCriteriaScheme .

:REACH_COVERAGE a skos:Concept ;
    skos:prefLabel "Spatial coverage"@en ;
    skos:definition "Fraction of intended reaches/segments not surveyed"@en ;
    skos:inScheme :DowngradeCriteriaScheme .

# Layer 3: OWL Event Classes
:EscapementSurveyEvent a owl:Class ;
    rdfs:label "Escapement Survey Event"@en ;
    rdfs:comment "A specific survey event with measured parameters"@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

# Layer 4: Event Instance with Metadata
:SkeenaSnorkel2022_001 a :EscapementSurveyEvent ;
    rdfs:label "Skeena Snorkel Survey 2022-001"@en ;
    dfo:usesEnumerationMethod :SnorkelSurvey ;
    dfo:usesEstimateMethod :AreaUnderCurve ;
    dfo:measuredVisits 6 ;
    dfo:measuredReachCoverage 0.85 ;
    dfo:measuredVisibility :Good ;
    dfo:measuredObserverEfficiency 0.8 ;
    dfo:percentRiverSwam 0.75 ;
    dfo:hasDocumentation :SIL_2022_001 ;
    dfo:hasQAReport :QA_2022_001 ;
    dfo:downgradeCriteriaMet :VISIBILITY, :REACH_COVERAGE ;
    dwc:eventDate "2022-08-15"^^xsd:date ;
    dwc:samplingProtocol :DFOSnorkelProtocol ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

**Key Principles:**

- **Methods are vocabulary terms** - Use SKOS for enumeration methods, estimate methods, and downgrade criteria
- **Events carry the data** - OWL classes for survey events with rich metadata properties
- **Metadata on instances** - Observer efficiency, coverage, visibility are properties of specific surveys
 - **Classification (current)** - Estimate types are manually assigned based on criteria; SHACL flags inconsistencies. Automated classification is deferred (see 2.5).

#### 2.4.1 Keep SKOS Concepts Separate from OWL Classes

- SKOS concepts are used strictly for controlled lists (e.g., categories, downgrade criteria, status zones) and must not be treated as OWL classes in axioms.
- Do not assert or infer SKOS concepts as `owl:Class` or use them as class expressions in restrictions.

What not to do (anti-pattern):

```turtle
# ❌ Do NOT model a SKOS concept as an OWL class
:RedZone a owl:Class .

# ❌ Do NOT use a SKOS concept as if it were an OWL class in restrictions
:EscapementSurveyEvent rdfs:subClassOf [
  a owl:Restriction ;
  owl:onProperty dfo:usesEnumerationMethod ;
  owl:allValuesFrom :RedZone  # :RedZone should be a skos:Concept, not a class
] .
```

Correct usage (pattern):

```turtle
# ✅ Keep :RedZone as a SKOS concept in a concept scheme
:RedZone a skos:Concept ;
  skos:prefLabel "Red Zone"@en ;
  skos:inScheme :StatusZoneScheme .

# ✅ Constrain with SHACL or document as guidance; keep OWL domain/range on properties
:statusZone a owl:ObjectProperty ;
  rdfs:domain :StatusAssessment ;
  rdfs:range skos:Concept .
```

Why: Per SKOS and OWL best practices (W3C SKOS Reference) and community guidance (e.g., Steven Baskauf), mixing SKOS individuals as OWL classes leads to punning and can break OWL DL reasoning assumptions. Keep SKOS for terminology, OWL for logical class hierarchies.

### 2.5 Data Validation with SHACL

**Why SHACL?** SHACL (Shapes Constraint Language) provides validation rules that can enforce data quality and ensure required fields are present. It separates data validation from classification logic. In our stack, shapes are used for validation only, not for inference or automated classification.

**Note:** Estimate types are manually assigned based on Hyatt 1997 criteria. Automated classification is deferred to post-MVP.

**SHACL Shape for Method Validation:**

```turtle
# SHACL Shape for Snorkel Survey Events
:SnorkelSurveyShape a sh:NodeShape ;
    sh:targetClass :EscapementSurveyEvent ;
    sh:property [
        sh:path dfo:usesEnumerationMethod ;
        sh:hasValue :SnorkelSurvey ;
        sh:message "Survey must use snorkel enumeration method"
    ] ;
    sh:property [
        sh:path dfo:measuredVisits ;
        sh:datatype xsd:integer ;
        sh:minInclusive 1 ;
        sh:message "Number of visits must be a positive integer"
    ] ;
    sh:property [
        sh:path dfo:measuredReachCoverage ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 0.0 ;
        sh:maxInclusive 1.0 ;
        sh:message "Reach coverage must be between 0.0 and 1.0"
    ] ;
    sh:property [
        sh:path dfo:measuredVisibility ;
        sh:in ( :Excellent :Good :Fair :Poor ) ;
        sh:message "Visibility must be one of: Excellent, Good, Fair, Poor"
    ] .
```

**Implementation Pipeline:**

1. **Data Entry** - Users create survey events with metadata
2. **SHACL Validation** - Ensures required fields are present and valid
3. **Manual Classification** - Estimate types assigned based on Hyatt 1997 criteria
4. **Quality Assessment** - Review data completeness and quality

### 2.6 Naming Conventions

**Classes:** Use PascalCase (e.g., `EscapementMeasurement`, `GeneticSample`)
**Properties:** Use lowerCamelCase (e.g., `aboutStock`, `usesMethod`, `hasMember`)
**SKOS Concepts:** Use PascalCase (e.g., `SonarCounting`, `MicrosatelliteAssay`)
**Instances:** Use PascalCase with descriptive names (e.g., `SkeenaSockeye`, `FraserCoho`)

**Why consistent naming matters:** It makes the ontology easier to read, understand, and maintain. It also helps prevent confusion when multiple people are contributing.

---

## 3. Design Patterns

### 3.1 Measurement Patterns

**Basic Measurement Pattern:**
Every measurement must have:

- `dwc:measurementType` - What was measured
- `dwc:measurementValue` - The measured value
- `dwc:measurementUnit` - The unit of measurement
- `dfo:aboutStock` - Which stock it describes
- `dfo:observedDuring` - Which event it was collected during
- `dfo:usesMethod` - Which method was used

**Example:**

```turtle
:EscapementCount2022 a dfo:EscapementMeasurement ;
    dwc:measurementType "abundance" ;
    dwc:measurementValue "1250"^^xsd:integer ;
    dwc:measurementUnit "http://qudt.org/vocab/unit/Each" ;
    dfo:aboutStock :SkeenaSockeye ;
    dfo:observedDuring :SkeenaSurvey2022 ;
    dfo:usesMethod :SonarCounting .
```

### 3.2 Hierarchy Patterns

**Management Hierarchy Pattern:**

- Management Units contain Conservation Units
- Conservation Units contain Stocks
- Use transitive `dfo:hasMember` relationships
- Create type-specific subproperties for clarity

**Example:**

```turtle
:BCInteriorMU a dfo:ManagementUnit ;
    dfo:hasMemberCU :FraserCUCoho .

:FraserCUCoho a dfo:ConservationUnit ;
    dfo:hasMemberStock :FraserCohoStock .

# Transitive inference: BCInteriorMU hasMember FraserCohoStock
```

### 3.3 Event Patterns

**Survey Event Pattern:**

- Surveys contain multiple measurement events
- Each measurement event has specific protocols
- Events can be nested (project > survey > measurement)

**Example:**

```turtle
:SalmonSurvey2023 a eco:Survey ;
    dwc:eventDate "2023-05-01/2023-09-30"^^xsd:gYear ;
    dwc:samplingProtocol :DFOEscapementProtocol .

:DailyCount2023_06_15 a dfo:EscapementSurveyEvent ;
    dwc:parentEventID :SalmonSurvey2023 ;
    dwc:eventDate "2023-06-15"^^xsd:date ;
    dwc:samplingProtocol :SonarCountingProtocol .
```

---

## 4. Darwin Core Integration

**Why integrate with Darwin Core?** Darwin Core provides a widely-adopted standard for biodiversity data that enables interoperability with GBIF, OBIS, and other international biodiversity platforms. By aligning with Darwin Core, your salmon data becomes discoverable and usable by the broader scientific community.

> **📋 Complete Darwin Core Integration**: See the [DFO Salmon Ontology: Product Requirements Document](PRODUCT_REQUIREMENTS.md) for the complete technical approach, including hybrid modeling strategy, core patterns, and Darwin Core integration details.

**Key Darwin Core Classes to Use:**

- `dwc:Event` - Actions, processes, or circumstances occurring at a place and time
- `dwc:Occurrence` - A state of an organism in an event
- `dwc:Organism` - A particular organism or defined group of organisms
- `dwc:MaterialSample` - Physical samples that can be identified and managed
- `dwc:Identification` - Taxonomic determinations of organisms
- [DwC-CM] `dwc:Assertion` (under review) - A generalized assertion (e.g., measurement/occurrence) with provenance
- `dwc:Agent` - People, groups, organizations, machines, or software that can act
- `dwc:Media` - Digital media (images, videos, sounds, text)
- `dwc:Protocol` - Methods used during actions

**DFO Extensions:**

```turtle
# DFO-specific classes that extend Darwin Core
dfo:ManagementUnit rdfs:subClassOf dwc:Event ;
    rdfs:label "Management Unit"@en ;
    rdfs:comment "A geographic or administrative unit for salmon management"@en .

dfo:ConservationUnit rdfs:subClassOf dwc:Event ;
    rdfs:label "Conservation Unit"@en ;
    rdfs:comment "A biologically meaningful unit for conservation planning"@en .

dfo:Stock rdfs:subClassOf dwc:Organism ;
    rdfs:label "Stock"@en ;
    rdfs:comment "A population of salmon with distinct characteristics"@en .
```

### 4.1 Conceptual Alignment (DwC-CM)

We align to the Darwin Core Conceptual Model (DwC-CM, under review) as our domain frame for biodiversity data. DwC-CM is treated as a mid-level model beneath our upper ontology (BFO):

- Operational entities are `dwc:Event`-based (surveys, analyses, runs) to preserve time/place semantics; we align these to BFO processes.
- Determinations and derived statements use `dwc:Assertion` where supported. We do not model or export legacy `dwc:MeasurementOrFact`.
- Organismal and occurrence context is explicit via `dwc:Organism` and `dwc:Occurrence` when needed by integration partners.

DFO specializations (illustrative):

- `dfo:EscapementSurveyEvent rdfs:subClassOf dwc:Event`
- `dfo:GSIRun rdfs:subClassOf dwc:Event`
- `dfo:Stock rdfs:subClassOf dwc:Organism`
- `dfo:StatusAssessment rdfs:subClassOf dwc:Assertion` (DwC-CM)

Early adopter note: We consciously apply DwC terms per the conceptual model under review, making this ontology among early adopters of DwC’s semantic layer. Where terms or ranges are still stabilizing, we document assumptions and keep changes localized via an anti‑corruption layer.

### 4.3 DwC Data Package Mapping (Outline)

For teams familiar with DwC tabular packages, here is a minimal mapping to DFO classes/properties:

- Event core (event.txt)
  - `eventID` → IRI of `dfo:EscapementSurveyEvent` or `dfo:GSIRun`
  - `eventDate`, `parentEventID`, `locationID` → time/place nesting for events
  - `samplingProtocol` → `dfo:usesEnumerationMethod` or `dfo:usedAssay` (DFO properties)

- Extension: Occurrence (occurrence.txt) when organismal presence is explicit
  - `occurrenceID` → occurrence instance IRI
  - `organismID` → `dfo:Stock` (linked via `dfo:aboutStock` in graph exports)

- Extension: Assertions (assertion.txt; DwC-CM)
  - `assertionID` → IRI of `dfo:StatusAssessment` (as `dwc:Assertion`)
  - `subjectID` → assessed entity (CU/SMU)
  - `predicate`/`object` → status/benchmark outcomes (or typed properties in RDF)
  - Provenance → see PROV usage in Section 2.3.7

This outline aims to let DwC users quickly map DFO semantics onto familiar DwC package structures while preserving richer semantics in RDF/JSON-LD.

### 4.4 Darwin Core Conceptual Model (DwC-CM) Alignment

**Context:** The Darwin Core Conceptual Model (DwC-CM) provides a semantic layer for Darwin Core that addresses long-standing ambiguities and provides clearer class definitions and relationships. DFO Salmon Ontology implements DwC-CM patterns for improved interoperability and semantic clarity.

#### 4.4.1 DwC-CM Implementation in DFO

**Occurrence Usage:**
- **Definition:** `dwc:Occurrence` is explicitly defined as "a state of an Organism in an Event"
- **DFO Usage:** Use `dwc:Occurrence` when modeling individual fish observations (e.g., genetic sampling data where each fish sampled is an Occurrence of that fish at the sampling event)
- **Aggregate Data:** For aggregate data (escapement counts, surveys), use `dwc:Event` and `dwc:Assertion` patterns
- **Avoid:** Conflating Occurrence with Event or with Organism

**Assertion Class Implementation:**
- **Purpose:** `dwc:Assertion` replaces `dwc:MeasurementOrFact` with clearer semantics
- **DFO Implementation:** `dfo:EscapementMeasurement ⊑ dwc:Assertion` and `dfo:GSICompositionMeasurement ⊑ dwc:Assertion`
- **Benefits:** Better semantic clarity, improved interoperability, alignment with modern DwC practices

**Structured Relationships:**
- **Property Domains/Ranges:** DwC-CM defines which properties apply to which classes with clear domain/range expectations
- **DFO Alignment:** DFO property usage aligns with DwC-CM constraints (e.g., `dwc:eventDate` on events, `dwc:measurementValue` on assertions)

#### 4.4.2 DwC-CM Usage Guidelines

**For Measurements:**
- Use `dwc:Assertion` as superclass for all measurement classes
- Ensure `dwc:measurementType`, `dwc:measurementValue`, `dwc:measurementUnit` are used appropriately
- Document the assertion pattern for measurements

**For Events:**
- Use `dwc:Event` as superclass for survey events
- Use `dwc:parentEventID` for event hierarchies when appropriate
- Ensure `dwc:eventDate` is used on event classes

**For Organisms:**
- Use `dwc:Organism` for stock classes
- Use `dwc:Occurrence` for individual organism observations (when applicable)
- Use `dwc:MaterialEntity` for physical samples

**For Data Packages:**
- Structure exports to align with DwC-CM classes
- Include proper metadata for dataset descriptions
- Ensure reference links exist between related entities

### 4.5 Contribution Guidance for DwC Alignment

- Prefer existing DwC classes when semantics match before creating a new class. Example: use `dwc:MaterialEntity` for tangible sample artifacts rather than introducing a parallel `dfo:Sample`.
- We typically subclass domain-specific classes under DwC terms (e.g., `dfo:EscapementSurveyEvent ⊑ dwc:Event`). We rarely use `dwc:Assertion` directly in schema; assertions arise by inference from specialized subclasses and are represented in data exports.
- Presence/absence and similar observation concepts may use `dwc:Occurrence` if/when these data are integrated. Coordinate with ontology leads before modeling new observational patterns.
- When a needed concept appears to overlap with DwC, open a discussion/issue or an ADR proposal to document rationale and trade-offs.
- **DwC-CM Alignment:** Ensure new terms align with DwC-CM patterns and use `dwc:Assertion` for measurement classes.

---

## 5. Quality Assurance

### 5.1 Pre-Submission Checklist

**Before submitting new terms:**

- [ ] Can you answer relevant competency questions with this term?
- [ ] Does the term follow established design patterns?
- [ ] Are all required annotations present (label, definition, source)?
- [ ] Does the term integrate properly with existing hierarchy?
- [ ] Have you tested the term with sample data?
- [ ] Is the term name consistent with naming conventions?
- [ ] Are all relationships properly typed (domain/range)?
- [ ] Does the term avoid duplicating existing functionality?

### 5.2 Validation Steps

**Logical Consistency:**

- [ ] Run reasoner to check for unsatisfiable classes
- [ ] Verify no classes appear under `owl:Nothing`
- [ ] Check for circular dependencies in hierarchies
- [ ] Validate domain/range restrictions are appropriate

**Content Quality:**

- [ ] Definitions are clear and unambiguous
- [ ] Labels follow naming conventions
- [ ] Synonyms are appropriate and well-sourced
- [ ] Examples are relevant and helpful

**Integration Quality:**

- [ ] Term integrates with existing classes
- [ ] Relationships are properly defined
- [ ] External references are valid and accessible
- [ ] Competency questions can be answered

**OBO Foundry Quality Standards:**

- [ ] **Open**: Freely available under CC-BY or CC0 license
- [ ] **Interoperable**: Uses standard OBO relations and formats
- [ ] **Logically well-formed**: No logical inconsistencies
- [ ] **Scientifically accurate**: Definitions reflect current scientific knowledge
- [ ] **Non-overlapping scope**: Clear boundaries with other ontologies
- [ ] **Common syntax**: Uses OBO format and standard annotation properties
- [ ] **OWL 2 compliant**: Uses correct OWL 2 syntax (e.g., `owl:TransitiveProperty` as type, not boolean)
- [ ] **RO relation reuse**: Checks RO for existing relations before defining new ones

### 5.3 Common Mistakes to Avoid

**Naming Issues:**

- Inconsistent naming conventions (e.g., mixing camelCase and snake_case)
- Using abbreviations without explanation
- Creating terms that are too specific or too general

**Relationship Issues:**

- Missing essential relationships
- Over-constraining with unnecessary restrictions
- Creating circular or contradictory relationships

**Content Issues:**

- Vague or unclear definitions
- Missing required annotations
- Duplicating existing terms with different names

**OWL 2 Syntax Issues:**

- Using `owl:TransitiveProperty true` instead of `a owl:TransitiveProperty`
- Incorrect transitivity declarations that violate OWL 2 specification
- Missing RO relation checks before defining new relations

---

## 6. Advanced Topics

### 6.1 Competency Questions

**What are competency questions?** These are the specific questions your ontology should be able to answer. They guide design decisions and validate that the ontology serves its intended purpose. Competency questions are essential for ensuring your ontology can actually support the research and data integration needs of the salmon science community.

**Why competency questions matter:**

- **Design guidance**: Help determine what terms and relationships are needed
- **Validation mechanism**: Ensure the ontology can answer the questions it's designed to address
- **Testing framework**: Enable systematic validation of the ontology's utility
- **Community alignment**: Ensure all stakeholders understand the ontology's purpose

> **📋 Complete Competency Questions**: See the [DFO Salmon Ontology: Competency Questions](COMPETENCY_QUESTIONS.md) for the complete, authoritative list of competency questions organized by domain (Stock Assessment, Genetics/GSI, Management & Policy, and Cross-Domain Integration).

#### 6.1.1 Using Competency Questions

**During Design:**

- Write competency questions before creating new terms
- Use them to identify missing relationships or classes
- Ensure each new term contributes to answering at least one question

**During Validation:**

- Convert competency questions to SPARQL queries when possible
- Test queries with sample data to ensure they return meaningful results
- Use them to validate that the ontology serves its intended purpose

**Example SPARQL Query:**

```sparql
# Find all escapement methods used for Sockeye stocks in 2022
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?method ?stock ?event WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dfo:usesMethod ?method ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate "2022"^^xsd:gYear .
  ?stock rdfs:label ?stockLabel .
  FILTER(CONTAINS(?stockLabel, "Sockeye"))
}
```

### 6.2 Troubleshooting

**Why troubleshooting matters:** Ontology development involves complex logical relationships that can lead to unexpected errors. Understanding common issues and their solutions helps you develop more effectively and avoid common pitfalls.

#### 6.2.1 Logical Consistency Issues

**Problem: Term appears under owl:Nothing**

- **Cause**: Logical inconsistency (e.g., conflicting restrictions, disjoint classes)
- **Solution**:
  1. Click the ? button next to owl:Nothing to see explanation
  2. Check for disjoint class assertions that conflict
  3. Look for contradictory domain/range restrictions
  4. Remove or modify conflicting axioms

**Problem: Missing inferred relationships**

- **Cause**: Reasoner not run or missing logical axioms
- **Solution**:
  1. Run the reasoner (ELK or HermiT)
  2. Add necessary equivalence axioms
  3. Check that subclass relationships are properly defined

**Problem: Unexpected classification results**

- **Cause**: Incorrect logical definitions or missing restrictions
- **Solution**:
  1. Review equivalence axioms carefully
  2. Check that restrictions use correct quantifiers (some vs. only)
  3. Verify that property chains are properly defined

#### 6.2.2 Content and Design Issues

**Problem: Can't find existing term**

- **Cause**: Search in wrong ontology or using wrong label
- **Solution**:
  1. Use broader search terms
  2. Check synonyms and alternative names
  3. Search in the correct ontology namespace
  4. Use partial string matching

**Problem: Term doesn't integrate with existing hierarchy**

- **Cause**: Missing subclass relationships or incorrect placement
- **Solution**:
  1. Identify the correct parent class
  2. Add appropriate subclass relationships
  3. Check that the term fits the intended hierarchy
  4. Consider if the term should be a different type (class vs. property)

**Problem: Relationships don't work as expected**

- **Cause**: Incorrect domain/range restrictions or missing properties
- **Solution**:
  1. Check that domain/range restrictions are appropriate
  2. Verify that properties are properly typed
  3. Ensure that relationships are defined in the correct direction
  4. Test with sample data

#### 6.2.3 Technical Issues

**Problem: Ontology won't load in Protégé**

- **Cause**: Syntax errors, missing imports, or file corruption
- **Solution**:
  1. Check for syntax errors in Turtle/RDF
  2. Verify that all imports are accessible
  3. Try loading a smaller subset of the ontology
  4. Check file encoding and line endings

**Problem: Reasoner runs very slowly**

- **Cause**: Complex logical definitions or large ontology
- **Solution**:
  1. Use a faster reasoner (ELK instead of HermiT)
  2. Simplify complex logical definitions
  3. Consider modularizing the ontology
  4. Remove unnecessary axioms

**Problem: SPARQL queries return no results**

- **Cause**: Incorrect query syntax or missing data
- **Solution**:
  1. Check query syntax carefully
  2. Verify that data exists for the query
  3. Test with simpler queries first
  4. Check that namespaces are properly declared

#### 6.2.4 Known Tool Warnings

**Problem: JFact datatype warning for EstimateType**

- **Warning**: `ERROR uk.ac.manchester.cs.jfact.datatypes.DatatypeFactory - A known datatype for https://w3id.org/dfo/salmon#EstimateType cannot be found; literal will be replaced with rdfs:Literal`
- **Root Cause**: `EstimateType` is correctly modeled as `skos:Concept` (not a datatype). JFact's datatype checking system is confused by SKOS concept usage as object property ranges.
- **Impact**: None - all reasoners (ELK, HermiT, JFact) produce identical results (2183 lines). Ontology is logically consistent.
- **Action**: This warning can be safely ignored.

#### 6.2.5 Getting Help

**When to ask for help:**

- You've tried the troubleshooting steps but the problem persists
- The issue affects multiple terms or relationships
- You're unsure about the correct modeling approach
- The problem seems to be a bug in the tools

**How to ask for help:**

- Provide a clear description of the problem
- Include relevant code snippets or error messages
- Explain what you've already tried
- Specify which tools and versions you're using

**Where to get help:**

- GitHub Issues for the DFO Salmon Ontology
- OBO Foundry community forums
- Protégé user mailing lists
- Ontology development workshops and training

### 6.3 Hierarchy and Relationship Conventions

#### 6.3.1 Subclassing

**What is subclassing?** Subclassing represents "is-a" relationships. For example, "Sockeye" is a subclass of "Salmon" because every sockeye is a salmon.

**When to use subclassing:**

- When one class is a more specific type of another
- When all instances of the subclass are also instances of the superclass
- When you want to inherit properties from the parent class

**Example:**

```turtle
:Sockeye rdfs:subClassOf :Salmon ;
    rdfs:label "Sockeye"@en ;
    rdfs:comment "A species of salmon (Oncorhynchus nerka)"@en .
```

#### 6.3.2 Equivalence

**What is equivalence?** Equivalence states that two classes are identical in meaning. Use this when two terms represent exactly the same concept.

**When to use equivalence:**

- When two classes have identical meaning but different names
- When aligning with external vocabularies
- When consolidating duplicate concepts

**Example:**

```turtle
:DFODataset rdfs:subClassOf :InformationEntity ;
    owl:equivalentClass schema:Dataset ;
    rdfs:label "Dataset"@en .
```

#### 6.3.3 Disjointness

**What is disjointness?** Disjointness states that two classes cannot have common instances. Use this when classes are mutually exclusive.

**When to use disjointness:**

- When classes represent mutually exclusive categories
- When you want to prevent logical inconsistencies
- When modeling taxonomic hierarchies

**Example:**

```turtle
:Freshwater rdfs:subClassOf :Environment ;
    owl:disjointWith :Marine .

:Marine rdfs:subClassOf :Environment ;
    owl:disjointWith :Freshwater .
```

### 6.4 Membership and Roll-up Pattern (MU ▶ CU ▶ Stock)

**What is the membership pattern?** This pattern represents the hierarchical relationship between Management Units, Conservation Units, and Stocks in salmon management.

**The Pattern:**

- Management Units contain Conservation Units
- Conservation Units contain Stocks
- Use transitive `hasMember` relationships
- Create type-specific subproperties for clarity

**Implementation:**

```turtle
# Define the base membership property
:hasMember a owl:ObjectProperty, owl:TransitiveProperty ;
    rdfs:label "has member"@en ;
    rdfs:comment "A transitive relationship indicating membership in a group"@en .

# Define type-specific subproperties
:hasMemberCU rdfs:subPropertyOf :hasMember ;
    rdfs:label "has member conservation unit"@en ;
    rdfs:domain :ManagementUnit ;
    rdfs:range :ConservationUnit .

:hasMemberStock rdfs:subPropertyOf :hasMember ;
    rdfs:label "has member stock"@en ;
    rdfs:domain :ConservationUnit ;
    rdfs:range :Stock .

# Example usage
:BCInteriorMU a :ManagementUnit ;
    :hasMemberCU :FraserCUCoho .

:FraserCUCoho a :ConservationUnit ;
    :hasMemberStock :FraserCohoStock .

# Transitive inference: BCInteriorMU hasMember FraserCohoStock
```

### 6.5 Measurement and GSI Conventions

#### 6.5.1 Escapement Measurements

**Required elements for every escapement measurement:**

- `dwc:measurementType` - What was measured (e.g., "abundance")
- `dwc:measurementValue` - The measured value
- `dwc:measurementUnit` - The unit of measurement (QUDT IRI)
- `dfo:aboutStock` - Which stock it describes
- `dfo:observedDuring` - Which event it was collected during
- `dfo:usesMethod` - Which method was used

**Example:**

```turtle
:EscapementCount2022 a :EscapementMeasurement ;
    dwc:measurementType "abundance" ;
    dwc:measurementValue "1250"^^xsd:integer ;
    dwc:measurementUnit "http://qudt.org/vocab/unit/Each" ;
    dfo:aboutStock :SkeenaSockeye ;
    dfo:observedDuring :SkeenaSurvey2022 ;
    dfo:usesMethod :SonarCounting .
```

#### 6.5.2 GSI Composition Measurements

**Required elements for every GSI measurement:**

- `dfo:aboutReportingUnit` - Which genetic reporting unit
- `dfo:proportion` - The proportion of the sample
- `dfo:confidence` - Confidence interval or quality measure
- `dfo:analyzedIn` - Which GSI run produced this result
- `dfo:basedOnSamples` - Which samples were analyzed

**Example:**

```turtle
:GSIResult2023_001 a :GSICompositionMeasurement ;
    dfo:aboutReportingUnit :FraserSockeyeRU ;
    dfo:proportion "0.85"^^xsd:decimal ;
    dfo:confidence "0.02"^^xsd:decimal ;
    dfo:analyzedIn :GSIRun2023_001 ;
    dfo:basedOnSamples :SampleSet2023_001 .
```

### 6.6 External Alignments

**Why external alignments matter:** They ensure your ontology can work with other systems and datasets, making your data more discoverable and useful.

**Key external vocabularies:**

- **QUDT**: Units of measurement (http://qudt.org/vocab/unit/)
- **ENVO**: Environmental terms (http://purl.obolibrary.org/obo/ENVO_)
- **GBIF Backbone**: Taxonomic names (http://www.gbif.org/species/)
- **Darwin Core**: Biodiversity data standards (http://rs.tdwg.org/dwc/terms/)
- **RO (Relations Ontology)**: Standard relations (http://purl.obolibrary.org/obo/RO_)
- **AGROVOC**: Agricultural/fisheries thesaurus for common concepts (https://agrovoc.fao.org/)
- **Schema.org/DCAT**: Web and catalog vocabularies for datasets and distributions
- **IAO**: Information artifact ontology for documents and datasets
- **ORG**: Organizational structure and units (https://www.w3.org/TR/vocab-org/)

**OBO Foundry Relation Reuse Requirements:**

- **Check RO first**: Before defining new relations, check if equivalent relations exist in RO
- **Use RO IRIs**: When equivalent relations exist, use the RO IRI directly or create subproperties
- **Avoid label conflicts**: OBO Foundry review flags non-RO relations with RO-equivalent labels
- **Subproperty alignment**: Create subproperties of RO relations when domain-specific extensions are needed

**Example RO Alignment:**

```turtle
# Instead of defining a new "hasMember" property, align with RO
:hasMember rdfs:subPropertyOf ro:has_part ;
    rdfs:label "has member"@en ;
    rdfs:comment "A transitive relationship indicating membership in a group"@en .

# Or use RO directly when appropriate
:populationOf ro:part_of :stock ;
    rdfs:label "population of"@en .
```

**Implementation:**

- Store external IRIs as literals in `…UnitIRI` properties
- Use `dcterms:source` to reference external vocabularies
- Plan to convert to object properties in future versions
- Check RO for existing relations before defining new ones

Practical guidance for new relationships:

- Before minting a custom property like `partOfRiver`, prefer the generic RO property `ro:part_of` and model “river” via the class hierarchy (e.g., `dfo:RiverSegment`).
- When a domain-specific refinement is needed, define a custom subproperty aligned to RO (e.g., `dfo:hasMemberCU rdfs:subPropertyOf ro:has_part`). This keeps reasoning consistent and improves interoperability.

**Unit Property Enhancement (Non-breaking):**
For richer unit semantics, consider adding object properties alongside datatype properties:

```turtle
# Current approach: Store QUDT IRIs as literals
:measurementUnitIRI a owl:DatatypeProperty ;
    rdfs:label "measurement unit IRI"@en ;
    rdfs:comment "IRI of the unit used in a measurement"@en ;
    rdfs:domain :Measurement ;
    rdfs:range xsd:anyURI .

# Enhanced approach: Add object property for reasoning
:hasUnit a owl:ObjectProperty ;
    rdfs:label "has unit"@en ;
    rdfs:comment "Links a measurement to a unit (e.g., QUDT Unit)"@en ;
    rdfs:domain :Measurement ;
    rdfs:range qudt:Unit ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

# Example usage with both approaches
:EscapementCount2022 a :EscapementMeasurement ;
    :measurementUnitIRI "http://qudt.org/vocab/unit/Each"^^xsd:anyURI ;
    :hasUnit qudt:Each .
```

**Trade-offs:**

- **Datatype approach**: Pragmatic storage and mapping, but reasoning can't follow strings to unit classes
- **Object property approach**: Enables richer unit semantics and reasoning, but requires unit ontology imports
- **Hybrid approach**: Use both for maximum flexibility and backward compatibility

### 6.7 IRI and Versioning Policy

**Decision:** We use W3ID-based IRIs with semantic versioning. See [ADR-003: IRI and Versioning Policy](../adr/003-iri-versioning-policy.md) for the complete rationale and alternatives considered.

#### 6.7.1 IRI Structure

**Base IRI:** `https://w3id.org/dfo/salmon#`

**Class IRIs:** `https://w3id.org/dfo/salmon#ClassName`
**Property IRIs:** `https://w3id.org/dfo/salmon#propertyName`
**Instance IRIs:** `https://w3id.org/dfo/salmon#InstanceName`

**Example:**
```turtle
@prefix dfo: <https://w3id.org/dfo/salmon#> .

dfo:EscapementMeasurement a owl:Class ;
    rdfs:label "Escapement Measurement"@en ;
    rdfs:comment "A measurement of salmon escapement"@en .
```

#### 6.7.2 Versioning

**Ontology versioning:**
- Use `owl:versionInfo` for version numbers
- Use `owl:versionIRI` for version-specific IRIs
- Tag releases in GitHub
- Maintain changelog

**Example:**
```turtle
<https://w3id.org/dfo/salmon> a owl:Ontology ;
    owl:versionInfo "1.0.0" ;
    owl:versionIRI <https://w3id.org/dfo/salmon/1.0.0> ;
    rdfs:label "DFO Salmon Ontology"@en .
```

### 6.8 Spreadsheet Templates for New Terms

**Why use templates?** Spreadsheet templates help domain experts contribute terms without needing to learn OWL syntax. They also ensure consistency and completeness.

**Template columns:**

- **Term Name**: The name of the term
- **Type**: Class, ObjectProperty, DatatypeProperty, or SKOS Concept
- **Label**: Human-readable name
- **Definition**: Clear definition
- **Parent**: Parent class or broader concept
- **Source**: Where the definition came from
- **Example**: Usage example
- **Notes**: Additional comments

**Example template row:**
| Term Name | Type | Label | Definition | Parent | Source | Example | Notes |
|-----------|------|-------|------------|--------|--------|---------|-------|
| EscapementMeasurement | Class | Escapement Measurement | A measurement of salmon escapement | Measurement | DFO protocols 2024 | Sonar count of 1,250 fish | Must link to stock and method |

### 6.9 Using Darwin Core Conceptual Model

**Why follow Darwin Core?** Darwin Core provides a widely-adopted standard for biodiversity data that enables interoperability with GBIF, OBIS, and other international platforms.

> **📋 Complete Darwin Core Integration**: See the [DFO Salmon Ontology: Product Requirements Document](PRODUCT_REQUIREMENTS.md) for the complete technical approach and Darwin Core integration strategy.

### 6.10 Common Modeling Scenarios

#### 6.10.1 Stock Assessment Scenario

**Scenario:** Modeling a sonar count of sockeye escapement

**Required elements:**

- Event (when and where the count occurred)
- Stock (which stock was counted)
- Method (sonar counting)
- Measurement (the count value and unit)
- Agent (who conducted the count)

**Example:**

```turtle
:SkeenaSurvey2023 a eco:Survey ;
    dwc:eventDate "2023-08-15"^^xsd:date ;
    dwc:samplingProtocol :SonarCountingProtocol ;
    dwc:recordedBy :DFOFieldTeam .

:SkeenaSockeye a dfo:Stock ;
    rdfs:label "Skeena Sockeye"@en ;
    rdfs:comment "Sockeye salmon from the Skeena River watershed"@en .

:SonarCount2023_08_15 a dfo:EscapementMeasurement ;
    dwc:measurementType "abundance" ;
    dwc:measurementValue "1250"^^xsd:integer ;
    dwc:measurementUnit "http://qudt.org/vocab/unit/Each" ;
    dfo:aboutStock :SkeenaSockeye ;
    dfo:observedDuring :SkeenaSurvey2023 ;
    dfo:usesMethod :SonarCounting .
```

#### 6.10.2 GSI Analysis Scenario

**Scenario:** Modeling genetic stock identification results

**Required elements:**

- GSI Run (when and how the analysis was performed)
- Samples (what was analyzed)
- Reporting Units (genetic populations)
- Composition Results (proportions and confidence)

**Example:**

```turtle
:GSIRun2023_001 a dfo:GSIRun ;
    dwc:eventDate "2023-06-15"^^xsd:date ;
    dfo:usedAssay :MicrosatelliteAssay ;
    dfo:usedMarkerPanel :PacificSalmonPanel .

:FraserSockeyeRU a dfo:ReportingUnit ;
    rdfs:label "Fraser Sockeye Reporting Unit"@en ;
    rdfs:comment "Genetic reporting unit for Fraser River sockeye"@en .

:GSIResult2023_001 a dfo:GSICompositionMeasurement ;
    dfo:aboutReportingUnit :FraserSockeyeRU ;
    dfo:proportion "0.85"^^xsd:decimal ;
    dfo:confidence "0.02"^^xsd:decimal ;
    dfo:analyzedIn :GSIRun2023_001 .
```

### 6.11 Review & Community Feedback

#### 6.11.1 Pre-Submission Review

**Before submitting new terms:**

1. **Self-review using competency questions**

   - Can this term answer a specific research question?
   - Does it integrate with existing terms?
   - Is it consistent with established patterns?

2. **Technical validation**

   - Run reasoner to check for logical consistency
   - Validate that all required annotations are present
   - Test with sample data

3. **Community consultation**
   - Discuss major changes in GitHub Issues
   - Get feedback from domain experts
   - Ensure alignment with community needs

#### 6.11.2 Submission Process

**How to submit new terms:**

1. **Create a GitHub Issue**

   - Describe the term and its purpose
   - Explain how it fits with existing terms
   - Provide examples of usage

2. **Create a Pull Request**

   - Include the new term in Turtle format
   - Follow all naming and annotation conventions
   - Include tests and examples

3. **Community Review**
   - At least two reviewers must approve
   - Address all feedback and concerns
   - Ensure quality and consistency

#### 6.11.3 Feedback Integration

**How to handle feedback:**

- **Be responsive**: Acknowledge all feedback promptly
- **Be collaborative**: Work with reviewers to improve terms
- **Be thorough**: Address all concerns before resubmitting
- **Be patient**: Good ontology development takes time

### 6.12 Roadmap

#### 6.12.1 Phase 1: Foundation (Current)

- Core class and property definitions
- Basic measurement patterns
- Stock hierarchy implementation
- Darwin Core alignment

#### 6.12.2 Phase 2: Expansion

- Genetic analysis workflows
- Advanced measurement types
- External vocabulary integration
- Quality control patterns

#### 6.12.3 Phase 3: Integration

- NCEAS Salmon Ontology alignment
- International standard compliance
- Advanced querying capabilities
- Data validation tools

#### 6.12.4 Phase 4: Policy and Integration

- Policy benchmarks and reference points
- Integration with NCEAS Salmon Ontology
- Advanced querying and analytics

---

## 7. Resources

### 7.1 Tools and Workflows

**Essential Tools:**

- **Protégé**: Visual ontology editor (https://protege.stanford.edu/)
- **WebProtégé**: Collaborative online editor
- **ROBOT**: Command-line ontology tools (http://robot.obolibrary.org/)
- **OntoGraf**: Protégé plugin for visualizing relationships

**OBO-Style Development Workflow:**

1. **Start with competency questions** to guide design
2. **Use ROBOT for quality control**:
   - `robot reason` to check logical consistency
   - `robot validate` to check for common issues
   - `robot template` for consistent term creation
3. **Create terms following core conventions**
4. **Test with sample data** and competency questions
5. **Use ROBOT for release management**:
   - `robot merge` to combine modules
   - `robot annotate` to add metadata
   - `robot convert` for format conversion
6. **Submit for community review**

**ROBOT Commands for DFO Salmon Ontology:**

```bash
# Check logical consistency
robot reason --input dfo-salmon.ttl --reasoner ELK

# Validate ontology
robot validate --input dfo-salmon.ttl

# Convert to other formats
robot convert --input dfo-salmon.ttl --output dfo-salmon.owl

# Add metadata
robot annotate --input dfo-salmon.ttl --ontology-iri "https://w3id.org/dfo/salmon" --version-iri "https://w3id.org/dfo/salmon/1.0.0" --output dfo-salmon-annotated.ttl
```

### 7.2 Community Process

**Getting Help:**

- GitHub Issues for the DFO Salmon Ontology
- OBO Foundry community forums
- Protégé user mailing lists
- Ontology development workshops and training

**Contributing:**

- Discuss major changes in GitHub Issues before implementing
- Use WebProtégé to visualize and verify your work
- Follow the quality assurance checklist
- Ask questions — the community is here to help!

### 7.3 Key Takeaways

**Essential Elements:**

- Always define: **Label + Definition**
- Use **OWL classes and properties** for structure
- Use **SKOS** when you need a picklist or controlled list
- Follow **Darwin Core** as your meta-framework for interoperability

**Getting Started:**

- Start with **competency questions** to guide your design
- Use **design patterns** to ensure consistency
- Don't stress about OWL syntax at first — focus on **clear terms and definitions**
- Use the spreadsheet templates to collect terms from domain experts
- Start simple and add complexity as needed

**Quality and Community Process:**

- Use the **quality assurance checklist** before submitting terms
- Test your terms with **sample data** and **competency questions**
- Discuss major changes in GitHub Issues before implementing
- Use WebProtégé to visualize and verify your work
- Ask questions — the community is here to help!

**Darwin Core Integration Benefits:**

- **International interoperability**: Your data becomes discoverable globally
- **Standard predicates**: Use established, well-tested relationships
- **Community alignment**: Follow patterns used by GBIF, OBIS, and others
- **Future-proofing**: Build on stable, widely-adopted standards

---

_Maintainer: Data Stewardship Unit, DFO Pacific Science_  
_License: CC-BY 4.0_
