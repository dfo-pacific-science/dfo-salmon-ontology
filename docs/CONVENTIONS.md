# DFO Salmon Ontology — Conventions Guide

This document orients new contributors to the modeling conventions used in the **GC DFO Salmon Ontology**. It explains how to create and refine ontology terms, how to model data in a way that aligns with our goals, and how to prepare new concepts for integration.

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

### Essential Elements (Canonical Checklist)

This checklist is canonical for “what must be on a term”; other summary sections link here to avoid drift.

**OWL terms (classes + properties):**

- **Label**: `rdfs:label "Human Name"@en`
- **Definition**: `iao:0000115 "1–2 sentence definition."@en`
- **Defined by**: `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>`
- **Definition provenance (optional)**: `iao:0000119 "Citation text here."@en` and/or `dcterms:source <https://doi.org/...>`

**SKOS concepts (controlled vocabulary terms):**

- **Preferred label**: `skos:prefLabel "Human Name"@en`
- **Scheme membership**: `skos:inScheme :SchemeName`
- **Definition (recommended)**: `skos:definition "1–2 sentence definition."@en`
- **Defined by**: `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>`
- **Code (optional)**: `skos:notation "CODE"^^ex:YourCodeSystemDatatype`
- **Definition provenance (optional)**: `iao:0000119 "Citation text here."@en` and/or `dcterms:source <https://doi.org/...>`

### Naming Conventions

- **Classes**: PascalCase (e.g., `EscapementMeasurement`)
- **Properties**: lowerCamelCase (e.g., `aboutStock`, `usesMethod`)
- **SKOS Concepts**: PascalCase (e.g., `SonarCounting`)

### Core Patterns

- **Hierarchy**: StockManagementUnit ▶ ConservationUnit ▶ Population using `hasConservationUnit` and `hasPopulation`
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
   - [6.3 Hierarchy and Relationship Conventions](#63-hierarchy-and-relationship-conventions)
   - [6.4 Membership and Roll-up Pattern](#64-membership-and-roll-up-pattern-smu--cu--population)
   - [6.5 Measurement and GSI Conventions](#65-measurement-and-gsi-conventions)
   - [6.6 External Alignments](#66-external-alignments)

7. [Resources](#7-resources)
   - [7.1 Tools and Workflows](#71-tools-and-workflows)
   - [7.2 Community Process](#72-community-process)
   - [7.3 Key Takeaways](#73-key-takeaways)

---

## 1. Fundamentals

This introductory material has moved to a dedicated onboarding guide for clarity and easier learning.

- This Conventions guide focuses on "how we do things" (operational guidance, patterns, QA, tools, workflows).

---

## 2. Getting Started

### 2.1 Essential Concepts

**What are classes?** Classes represent categories or types of things in your domain. For example, "Stock", "SurveyEvent", and "GeneticSample" are all classes. They're like the nouns in your vocabulary.

**What are properties?** Properties describe relationships between things or attributes of things. For example, "aboutStock" describes which stock a measurement is about, and "usesMethod" describes which method was used.

**What are instances?** Instances are specific examples of classes. For example, "SkeenaSockeye" is an instance of the "Stock" class.

### 2.2 Schema vs Data Separation

**Critical Rule: Keep the Ontology File Clean**

The `ontology/dfo-salmon.ttl` file must contain **schema elements only** - no instance data. This separation is essential for maintainability, versioning, and interoperability.

**What Goes in the Ontology File (`ontology/dfo-salmon.ttl`):**

- **OWL Classes**: `EscapementSurveyEvent`, `Stock`, `Measurement`
- **OWL Properties**: `usesEnumerationMethod`, `aboutStock`, `hasCountValue`
- **SKOS Concepts**: `SnorkelSurvey`, `Type2`, `VISITS`
- **Axioms and Rules**: Class restrictions and equivalence axioms (SHACL shapes are maintained in `ontology/shapes/`)
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
    iao:0000115 "A specific survey event with measured parameters"@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

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

- **Schema Validation**: SHACL shapes in `ontology/shapes/` validate data structure
- **Data Validation**: Apply those SHACL shapes to instance data files
- **Quality Assurance**: Ensures data conforms to schema requirements

### 2.3 Core Conventions

#### 2.3.1 Classes

**Required elements for every class:**

- **Type declaration:** `a owl:Class` - This tells the system this is a class
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name in English (required, one per language)
- **Definition:** `iao:0000115 "1–2 sentence definition."@en` - A clear explanation of what this class represents (required, one only)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>` - Links back to our ontology (required)

**Optional elements:**

- **Definition source (text):** `iao:0000119 "Citation text here."@en` - Human-readable citation for where the definition came from (optional, 0..*)
- **Definition source (link):** `dcterms:source <https://doi.org/...>` - Resolvable link to authoritative document or resource (optional, 0..*)
- **Examples:** `iao:0000112 "Concrete example of usage."@en` - Concrete examples of how this class is used (optional, 0..*)
- **Notes:** `rdfs:comment "Editorial note."@en` - Optional editorial notes (NOT a definition)
- **Alternative label:** `skos:altLabel "Alternative Label"@en` - Optional secondary label for SKOS consumers (non-normative)
- **SKOS mirror label:** When a class also carries `skos:prefLabel`, duplicate the same literal in `rdfs:label` so OWL tooling and SKOS consumers stay in sync.

**Why these are required:** Labels help humans understand what you mean, definitions prevent confusion about scope, and source attribution ensures proper credit and traceability. Using `rdfs:label` and `IAO:0000115` aligns with OBO Foundry standards and ROBOT tooling expectations. The `skos:prefLabel` can optionally be added on OWL terms for SKOS consumers, but `rdfs:label` is primary and required.

**Example:**

```turtle
:GeneticSample a owl:Class ;
    rdfs:label "Genetic Sample"@en ;
    iao:0000115 "Tissue or material used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    iao:0000119 "DFO Molecular Genetics Lab glossary 2024"@en ;
    iao:0000112 "Fin clip sample from Fraser River sockeye collected in 2023."@en ;
    dcterms:source <https://doi.org/10.1234/dfo-genetics-2024> ;
    skos:altLabel "DNA sample"@en .
```

#### 2.3.2 Object Properties

**What are object properties?** Object properties link instances of one class to instances of another class. For example, "aboutStock" links a measurement to a stock.

**Required elements for every object property:**

- **Type declaration:** `a owl:ObjectProperty`
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name (required, one per language)
- **Definition:** `iao:0000115 "1–2 sentence definition."@en` - A clear explanation of what this property represents (required, one only)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>` - Links back to our ontology (required)

**Optional but recommended:**

- **Definition source (text):** `iao:0000119 "Citation text here."@en` - Human-readable citation for where the definition came from
- **Definition source (link):** `dcterms:source <https://doi.org/...>` - Resolvable link to authoritative document or resource
- **Examples:** `iao:0000112 "Concrete example of usage."@en` - Concrete examples of how this property is used
- **SKOS mirror label:** If a property includes `skos:prefLabel`, repeat the same literal in `rdfs:label`; OWL labels remain the normative value.

**Optional domain and range:**

- **Domain:** `rdfs:domain :ClassName` - What type of thing this property describes
- **Range:** `rdfs:range :ClassName` - What type of thing this property points to

**Guidance on domain and range:** Prefer class restrictions (and SHACL for validation) over global `rdfs:domain`/`rdfs:range` unless the constraint is always true. Global domain/range declarations propagate broadly and can cause unintended logical consequences. Use them conservatively.

**Example:**

```turtle
:aboutStock a owl:ObjectProperty ;
    rdfs:label "about stock"@en ;
    iao:0000115 "Links a measurement or observation to the specific stock it describes."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    iao:0000119 "DFO stock assessment protocols 2024"@en ;
    iao:0000112 "A sockeye escapement measurement about Fraser River sockeye stock."@en ;
    rdfs:domain :Measurement ;  # Use conservatively - prefer class restrictions where possible
    rdfs:range :Stock ;
    dcterms:source <https://doi.org/10.1234/dfo-protocols-2024> .
```

**Alignment with Relations Ontology (RO):** Use `skos:exactMatch`/`skos:closeMatch` only for concept-level mappings. For OWL terms, use OWL/RDFS axioms only: `rdfs:subPropertyOf` or `owl:equivalentProperty` for properties, and `rdfs:subClassOf` or `owl:equivalentClass` for classes. Apply this confidence ladder:
1. **Candidate**: record as candidate only (no logical mapping axiom).
2. **Broadly aligned**: assert `rdfs:subPropertyOf` / `rdfs:subClassOf`.
3. **Semantically equivalent**: assert `owl:equivalentProperty` / `owl:equivalentClass`.
Do not use `rdfs:seeAlso` for semantic alignment.

#### 2.3.3 Datatype Properties

**What are datatype properties?** Datatype properties link instances to literal values (text, numbers, dates). For example, "measurementValue" links a measurement to its numeric value.

**Required elements for every datatype property:**

- **Type declaration:** `a owl:DatatypeProperty`
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name (required, one per language)
- **Definition:** `iao:0000115 "1–2 sentence definition."@en` - A clear explanation of what this property represents (required, one only)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>` - Links back to our ontology (required)

**Optional but recommended:**

- **Definition source (text):** `iao:0000119 "Citation text here."@en` - Human-readable citation for where the definition came from
- **Definition source (link):** `dcterms:source <https://doi.org/...>` - Resolvable link to authoritative document or resource
- **Examples:** `iao:0000112 "Concrete example of usage."@en` - Concrete examples of how this property is used
- **SKOS mirror label:** When a datatype property keeps `skos:prefLabel` for SKOS tooling, mirror the literal in `rdfs:label`.

**Optional domain and range:**

- **Domain:** `rdfs:domain :ClassName`
- **Range:** `rdfs:range xsd:datatype` (e.g., `xsd:string`, `xsd:integer`, `xsd:date`)

**Guidance on domain and range:** Prefer class restrictions (and SHACL for validation) over global `rdfs:domain`/`rdfs:range` unless the constraint is always true. Global domain/range declarations propagate broadly and can cause unintended logical consequences. Use them conservatively.

**Example:**

```turtle
:measurementValue a owl:DatatypeProperty ;
    rdfs:label "measurement value"@en ;
    iao:0000115 "The numeric value of a measurement."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    iao:0000112 "A count of 1,250 sockeye salmon."@en ;
    rdfs:domain :Measurement ;  # Use conservatively - prefer class restrictions where possible
    rdfs:range xsd:decimal .
```

#### 2.3.4 SKOS Concepts

**What are SKOS concepts?** SKOS concepts are for controlled vocabularies - lists of standardized terms like methods, categories, or codes. Use SKOS when you need a picklist rather than a complex class hierarchy. SKOS functions as a thesaurus.

**Terminology vs Ontology:**

- **Terminology**: A collection of terms with definitions and synonyms (like a dictionary)
- **Ontology**: A formal classification with logical relationships between terms (like a structured knowledge base)
- **Our approach**: We use OWL for formal relationships and SKOS for simple controlled vocabularies

**Required elements for every SKOS concept:**

- **Type declaration:** `a skos:Concept`
- **Label:** `skos:prefLabel "Human Name"@en` - A human-readable name (required, ≤1 per language)
- **Scheme membership:** `skos:inScheme :SchemeName` - The concept scheme this concept belongs to (required)
- **Definition:** `skos:definition "1–2 sentence definition."@en` - A clear explanation (recommended, 1×)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>` - Links back to our ontology (required)

**Optional elements:**

- **Alternative labels:** `skos:altLabel "Alternative"@en` - Alternative names (optional, 0..*)
- **Broader/narrower/related:** `skos:broader :BroaderConcept` - Hierarchical relationships (optional)
- **Definition source (link):** `dcterms:source <https://doi.org/...>` - Resolvable link to authoritative document (optional)
- **Definition source (text):** `iao:0000119 "Citation text here."@en` - Human-readable citation (optional)
- **Code (if applicable):** `skos:notation "CODE"^^ex:YourCodeSystemDatatype` - Formal scheme code (optional, typed literal)
- **External alignments:** Use `skos:exactMatch` / `skos:closeMatch` for IRIs that denote aligned concepts. Reserve `skos:altLabel` for text synonyms with language tags.

**Code guidance (skos:notation):**

- Value MUST be a typed literal (code string + datatype IRI naming the code system)
- Don't put codes in labels (`skos:prefLabel`) or in `dcterms:identifier`
- If multiple code systems apply, include multiple `skos:notation` values (one per datatype)
- Enforce: per concept per scheme, exactly one `skos:notation` with datatype per code system

**Note on ROBOT Validation:** ROBOT may report missing `rdfs:label` for SKOS concepts that have `skos:prefLabel`. Per W3C SKOS specification, `skos:prefLabel` is a subproperty of `rdfs:label`, so these concepts ARE properly labeled. Either configure ROBOT to accept `skos:prefLabel` without requiring `rdfs:label` on SKOS concepts, or document that SKOS concepts will duplicate `skos:prefLabel → rdfs:label` for ROBOT compatibility. **Project default:** duplicate `skos:prefLabel` into `rdfs:label` for SKOS concepts unless a validator profile explicitly waives it.

**Example:**

```turtle
# Declare the code-system datatype
ex:DFOEscMethodCode a rdfs:Datatype .

:SonarCounting a skos:Concept ;
    skos:inScheme :EscapementMethodScheme ;
    skos:prefLabel "Sonar counting"@en ;
    skos:definition "Counting fish using active acoustic methods (e.g., DIDSON/ARIS) under a defined protocol."@en ;
    skos:broader :CountingMethod ;
    skos:notation "ESC-001"^^ex:DFOEscMethodCode ;  # code lives here, not in the label
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    dcterms:source <https://doi.org/10.1234/dfo-esc-methods-2023> ;
    iao:0000119 "DFO (2023). Escapement Survey Manual, Pacific Region."@en .
```

##### 2.3.4.1 SKOS vs OWL decision rule (flat vs inheriting)

- Use **SKOS concept schemes** when the hierarchy is flat or tree-only (no property inheritance, no logical class expressions), when the terms act as picklist codes, and when you **do not need** to instantiate them as classes in data (i.e., they remain terminology values).
- Use **OWL classes** when you need property inheritance, logical constraints, class expressions, or when downstream data will type individuals with the term (e.g., `rdf:type gcdfo:StockAssessment`).
- Do **not** mix the two: a SKOS concept is an individual of `skos:Concept`; it is not a class. If you believe a term must be both, pause and record an ADR before introducing punning.
- Default posture: SKOS for code lists; OWL for behavioral/logical models. If in doubt, ask “Will this term ever need class-level semantics or property inheritance?” If yes → OWL; if no and hierarchy is purely lexical → SKOS.
- **Compound variables/metrics (I-ADOPT)**: model them as SKOS concepts in the appropriate scheme (e.g., WSP metrics), not as OWL classes. Capture decomposition on the SKOS concept with annotation properties for property, entity (in the ObjectOfInterest role), constraints, and procedure. Only introduce OWL classes for a metric if a competency question requires class-level reasoning.

###### 2.3.4.1.1 I-ADOPT + SSN/OMS/OBOE/PROV alignment pattern (variables only)

We adopt a **minimal, annotation-centric pattern** for I-ADOPT that plays nicely with SSN 2023, OMS, OBOE, and PROV, without changing core OWL class hierarchies:

- **Variables as SKOS concepts**:
  - Each compound metric/variable (e.g., WSP Metric 1–4, benchmarked exploitation rate, CU-level abundance index) is a `skos:Concept` in a dedicated SKOS scheme.
  - That SKOS concept is also treated as an **I-ADOPT Variable** and an **observable property**:
    - We may type it (in a separate alignment module) as `iop:Variable` and `sosa:Property` / OMS ObservableProperty / `oboe:Characteristic`, but the *authoritative variable identity* lives in SKOS.
- **I-ADOPT decomposition as annotations**:
  - We define a small set of **annotation properties** in the DFO Salmon namespace, instead of importing all I-ADOPT object properties into `dfo-salmon.ttl`:
    - `gcdfo:iadoptProperty` – points from a variable concept to the property (e.g., abundance, rate).
    - `gcdfo:iadoptEntity` – points to the entity term in the ObjectOfInterest role (e.g., Stock, CU, SpawningPopulation).
    - `gcdfo:iadoptConstraint` – points to constraint concepts (life stage, origin, benchmark, spatial subset; multiple allowed).
    - `gcdfo:usedProcedure` – **canonical (replaces `gcdfo:iadoptMethod`)** – an `owl:AnnotationProperty` subproperty of `sosa:usedProcedure` that points from a variable (SKOS) concept to the procedure/method concept or class (aligns to `sosa:Procedure`, `prov:Plan`, or `IAO:0000104` specification; NOT I-ADOPT). In instance data (observations/sampling), use `sosa:usedProcedure` directly.
  - These are declared as `owl:AnnotationProperty` (with `gcdfo:usedProcedure` as an annotation subproperty of `sosa:usedProcedure`) so they do **not** involve SKOS concepts in OWL class axioms (keeps us within our "no SKOS as OWL class in axioms" rule) but remain fully queryable via SPARQL.
- **Component IRIs**:
  - The values of the annotation properties (properties, entities, constraints, procedures) are **existing OWL classes or SKOS concepts**:
    - Properties: quantity kinds or observables (potentially I-ADOPT `iop:Property` or QUDT/ENVO/other).
    - Entities: DFO classes (CU, Stock, SurveyEvent, BiologicalSample) or relevant external classes.
    - Constraints: SKOS concepts in existing schemes (origin, life-stage, benchmark category, spatial strata, etc.).
    - Procedures: SKOS concepts in procedure/method schemes or OWL classes representing procedures.
- **MIREOT / imports**:
  - For Phase 0, we **do not import** the full I-ADOPT ontology into `dfo-salmon.ttl`. We only reference I-ADOPT IRIs (e.g., for typing or documentation) where needed.
  - If future needs require stronger alignment (e.g., SHACL validation or interoperability checks), we can:
    - MIREOT just the few I-ADOPT classes we need (`iop:Variable`, `iop:Property`, `iop:Entity`, `iop:Constraint`) into a small alignment module (e.g., `dfo-salmon-iadopt.ttl`)—ObjectOfInterest remains a role expressed via `iop:hasObjectOfInterest`, not a class—and
    - keep that module separate from the core ontology while using our local annotation properties for the decomposition links.

This gives us a **single canonical pattern**:

- Variable identity and human-facing semantics: SKOS (`skos:Concept` in variable schemes).
- Machine-facing decomposition and cross-ontology alignment: I-ADOPT roles + SSN/OMS/OBOE, via annotations.

**Canonical authoring pattern (explicit rule):**

- **Canonical authoring**: Use SKOS variable concepts + local annotation properties (`gcdfo:iadoptProperty`, `gcdfo:iadoptEntity`, `gcdfo:iadoptConstraint`, `gcdfo:usedProcedure`). Keep the core ontology lightweight and avoid importing I-ADOPT object properties.
- **Interop projection (generated)**: Optionally emit `iop:hasProperty` / `iop:hasObjectOfInterest` / `iop:hasConstraint` triples in a separate alignment/export layer, and type the variable as `iop:Variable`. When projecting object-of-interest, point `iop:hasObjectOfInterest` to an `iop:Entity` (ObjectOfInterest is a role, not a class). This projection is for downstream interoperability, not for canonical authoring.

###### 2.3.4.1.2 Extraction frame categories

Use the following extraction frame categories when capturing new terms from source material:

- **Entity**: physical, biological, organizational, or information-bearing thing.
- **Property**: quality/attribute measured or described for an entity.
- **Variable**: operationalized measurable concept (often compound) represented as a SKOS variable concept.
- **Constraint / StatModifier**: qualifiers that narrow interpretation (life stage, origin, benchmark, stratum, statistical condition).
- **Method / Protocol**: procedure, plan, assay, or survey protocol used to produce evidence.
- **Event / Observation**: temporally bounded activity where sampling/observation/analysis occurs.
- **Result / Provenance**: measurement/output artifacts and lineage metadata (source, agent, derivation).

##### 2.3.4.2 Theme / module annotation for navigation

- Tag every OWL class, property, and SKOS concept with a **theme/module annotation** to aid navigation and review.
- Annotation property: `gcdfo:theme` (annotation property) with values drawn from the SKOS concept scheme `gcdfo:ThemeScheme` (defined in `ontology/dfo-salmon.ttl`).
- Cardinality: 1–3 per term; choose the smallest set that reflects the owning bounded context.
- Exempt: `gcdfo:ThemeScheme` and its member theme concepts are excluded from the missing-theme check.
- Keep the annotation purely descriptive (no reasoning expected). Do not use it in logical axioms or SHACL constraints.
- Validation: `make theme-coverage` should report clean output (and keep `release/tmp/theme-coverage.tsv` empty); values must be members of `gcdfo:ThemeScheme`.
- Review checklist: ensure each new term is themed and stays under the 3-theme cap.



#### 2.3.5 Provenance and Citation Conventions

#### 2.3.5.1 Minimal provenance set (`IAO_0000115`, `IAO_0000119`, `dcterms:source`)

To keep provenance consistent and avoid redundancy:

| Property           | Purpose                                       | Expected Value Type | Example Use |
| ------------------ | --------------------------------------------- | ------------------- | ----------- |
| **`IAO_0000115`**  | Textual definition (always required).         | Literal (string, lang-tag) | `"The overall proportion of the total return removed by fishing."@en` |
| **`IAO_0000119`**  | Human-curated definition source (citation text). Only set when vetted. | Literal (string, lang-tag) | `"DFO (2023). Escapement Survey Manual, Pacific Region."@en` |
| **`dcterms:source`** | Resolvable URI (DOI, URL, Handle, w3id, ARK, PURL) to the source resource for the definition. Optional but preferred when available. | IRI | `<https://doi.org/10.1234/dfostock.2023>` |

Guideline:
- Always include `IAO_0000115`.
- Add `IAO_0000119` only when a human-vetted citation is available (do **not** auto-generate).
- Add `dcterms:source` when you have a resolvable URI (DOI/URL) to the source. If absent, leave it blank.
- Use `skos:notation` for scheme codes; avoid codes/IDs in labels or provenance fields.

---

#### 2.3.5.2 Example — Class Definition with Proper Citation

```turtle
:EscapementSurveyEvent a owl:Class ;
    rdfs:label "Escapement Survey Event"@en ;
    iao:0000115 "A survey event conducted to measure salmon escapement."@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;

    # Resolvable link to authoritative document (IRI)
    dcterms:source <https://doi.org/10.1234/dfostock.2023> ;

    # Human-readable citation text for definition source
    iao:0000119 "DFO (2023). Escapement Survey Manual, Pacific Region. Fisheries and Oceans Canada."@en ;

    # Optional: helpful extra link (landing page)
    rdfs:seeAlso <https://open.canada.ca/data/en/dataset/escapement-survey-manual-2023> .
```

**Explanation:**

- `dcterms:source` provides a _resolvable link_ (DOI IRI) to the authoritative document.
- `iao:0000119` provides a _human-readable citation_ specifically for where the definition text came from.
- `rdfs:seeAlso` provides a _helpful extra link_ (landing page) for easy access and browser navigation.

**Note:** This class definition is generic (no specific dataset DOI). For concrete resources, create them as instances in a data graph (e.g., `dcat:Dataset`) and link from there, rather than putting dataset-specific DOIs on OWL class definitions.

---

#### 2.3.5.3 Example — Class Definition (Generic, Not Instance-Specific)

```turtle
:BaselineGeneticDataset a owl:Class ;
    rdfs:label "Baseline Genetic Dataset"@en ;
    iao:0000115 "A curated collection of reference genotypes used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;

    # Resolvable link to authoritative document (IRI)
    dcterms:source <https://doi.org/10.1234/dfo-baseline-genotype-2024> ;

    # Human-readable citation text for definition source
    iao:0000119 "DFO Molecular Genetics Laboratory (2024). Baseline Genotype Reference Collection. Fisheries and Oceans Canada."@en ;

    # Optional: helpful extra link (data portal landing page)
    rdfs:seeAlso <https://open.canada.ca/data/en/dataset/dfo-baseline-genotype-reference-collection> .
```

**Note:** This class definition is generic. For specific dataset instances (e.g., the 2024 baseline genotype collection), create them as instances in a data graph (e.g., `dcat:Dataset`) rather than putting instance-specific DOIs on OWL class definitions.

---

#### 2.3.5.4 Key Points

- ✅ **`dcterms:identifier`** is a **literal** internal ID (e.g., "DFO-SALMON:000123"), not an IRI, not a scheme code
- ✅ Use **`dcterms:source`** for links to resources (IRIs), e.g., `<https://doi.org/10.1234/...>`
- ✅ Put scheme **codes** in **`skos:notation`** (typed literal), not in labels or identifiers
- ✅ Use **`iao:0000119`** strictly for definition textual provenance (citation text for where the definition came from)
- ✅ Use **`dcterms:bibliographicCitation`** for general bibliographic strings (not specifically definition source)
- ✅ Use **`rdfs:seeAlso`** optionally for helpful extra links, not as the primary provenance hook
- ✅ This pattern aligns with DCMI, W3C, and OBO Foundry best practices for provenance and citation

---

#### 2.3.6 Authoritative Templates

These templates represent the correct patterns for OWL and SKOS terms. All examples in this document should follow these patterns.

**OWL Class / Property (authoritative template):**

```turtle
:ExampleClass a owl:Class ;
  rdfs:label "Example class"@en ;           # required, 1× per lang
  IAO:0000115 "Definition text."@en ;       # required, 1×
  IAO:0000119 "DFO (2024) …"@en ;           # optional (definition citation string)
  IAO:0000112 "Example usage …"@en ;        # optional example
  rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;  # required
  dcterms:source <https://doi.org/10.xxxx/yyy> .    # optional (IRI link)
```

**SKOS Concept (authoritative template):**

```turtle
# Declare code-system datatype (if codes are used)
ex:DFOEscMethodCode a rdfs:Datatype .

:SonarCounting a skos:Concept ;
  skos:inScheme :EscMethodScheme ;             # required
  skos:prefLabel "Sonar counting"@en ;         # required, ≤1 per lang
  skos:definition "Counting fish via active acoustics …"@en ;  # recommended
  skos:notation "ESC-001"^^ex:DFOEscMethodCode ;  # optional, typed code
  rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;  # required
  dcterms:source <https://doi.org/10.xxxx/zzz> ;   # optional (IRI)
  IAO:0000119 "DFO (2023) Escapement Manual …"@en .  # optional (text)
```

**Key differences:**

See the canonical checklist in [Quick Start Cheatsheet → Essential Elements](#essential-elements-canonical-checklist).

---

#### 2.3.7 Language and Datatype Rules

**Language-tagged strings** (with `@en` or other language tags):
- `rdfs:label`, `skos:prefLabel`, `IAO:0000115`, `IAO:0000112`, `IAO:0000119`, `skos:definition`, `skos:altLabel`
- All human-readable text should be language-tagged

**Typed literals** (no language tag, with datatype IRI):
- `skos:notation` - e.g., `"ESC-001"^^ex:DFOEscMethodCode`
- Codes must be typed literals, not plain strings

**Plain string literals** (no language tag, no datatype):
- `dcterms:identifier` - e.g., `"DFO-SALMON:000123"`
- Internal textual identifiers should be plain strings

---

#### 2.3.8 Lexical Labels & Synonyms (OWL 2)

Synonyms are **lexical metadata**. In our OWL 2 authoring, synonyms are represented as **annotations only** (they do not affect reasoning).

**Preferred label**
- Use `rdfs:label` as the canonical human-facing label.

**Typed synonyms (recommended; interoperable with OBO tooling)**
- `oboInOwl:hasExactSynonym` — exact lexical synonyms
- `oboInOwl:hasRelatedSynonym` — related (not exact)
- `oboInOwl:hasBroadSynonym` — broader terms
- `oboInOwl:hasNarrowSynonym` — narrower terms

**Minimal fallback (untyped)**
- Use `IAO:0000118` ("alternative term") when scope typing is not needed. (Tradeoff: you lose exact/broad/narrow/related typing.)

**If a synonym needs metadata (type, provenance, xrefs)**
- Use OWL 2 axiom annotations (`owl:Axiom`) on the synonym annotation assertion.

**Do not**
- Do **not** use `rdfs:comment` to encode synonyms (reserve it for editorial notes/clarifications).
- Do **not** model lexical synonyms as `owl:equivalentClass`/`owl:sameAs`.

**SKOS note (convenience only)**
- If you also maintain SKOS concept schemes, use `skos:altLabel` there.
- Avoid using `skos:altLabel` as the primary synonym mechanism on OWL classes; if used at all, treat as convenience-only and non-normative.

**Example**
```turtle
:AgeAtMaturity a owl:Class ;
  rdfs:label "Age-at-maturity"@en ;
  oboInOwl:hasExactSynonym "Maturity age"@en ;
  rdfs:comment "Numeric age of fish (editorial note, not a synonym)."@en .

[] a owl:Axiom ;
  owl:annotatedSource :AgeAtMaturity ;
  owl:annotatedProperty oboInOwl:hasExactSynonym ;
  owl:annotatedTarget "Maturity age"@en ;
  oboInOwl:hasDbXref "Van Beveren 2024"@en .
```

---

#### 2.3.9 Punning Policy

**Default:** No punning (different IRIs for OWL classes vs SKOS concepts). This maintains OWL 2 DL profile compliance and avoids confusion.

**Strict separation:** Treat SKOS concept schemes as vocabulary artifacts only. Do not attach OWL structural axioms (`rdfs:subClassOf`, property domains/ranges, class expressions) to SKOS terms.

**Punning only with intent:** If a future competency question requires the same IRI to behave as both an OWL class and SKOS concept, capture the decision in an ADR first, add explicit comments in the ontology, and run ROBOT validation to confirm OWL 2 DL compliance.

In everyday modeling, mint distinct IRIs for OWL classes versus SKOS concepts and rely on SKOS properties (`skos:broader`, `skos:inScheme`, etc.) for hierarchical vocabulary structure.

---

#### 2.3.10 RDF 1.2 Stance

- **Quoted triples** are out of scope for the core OWL module (not in OWL 2 DL's entailment regime)
- Continue using **language-tagged literals** (optionally with language direction) per RDF 1.2
- Keep the core ontology in OWL 2 DL profile for maximum tool compatibility

---

### 2.3.11 Ontology Import Strategy

**Decision:** We use a pragmatic three-tier approach for external vocabulary integration. See [ADR-005: External Vocabulary Integration Strategy](../adr/005-external-vocabulary-integration.md) for the complete rationale and alternatives considered.

**Implementation:**

#### 2.3.11.1 MIREOT Implementation (BFO/IAO/DQV)

**Method:**
1. Copy the term IRI (e.g., `bfo:0000015`)
2. Add minimal metadata: `rdfs:label`, `iao:0000115` (definition)
3. Add `rdfs:isDefinedBy` pointing to source ontology
4. Use the term as if it were native

**Example - BFO MIREOT:**
```turtle
# Import specific BFO term via MIREOT
bfo:0000015 a owl:Class ;
  rdfs:label "process"@en ;
  iao:0000115 "An occurrent that has temporal parts."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

# Now use it in your ontology
dfo:StatusAssessment a owl:Class ;
  rdfs:subClassOf bfo:0000015 .  # process
```

**DFO Salmon MIREOT Terms:**

- **BFO** (4 terms): process, material entity, generically dependent continuant, specifically dependent continuant
- **IAO** (6 terms): measurement datum, information content entity, directive information entity, document, definition, definition source
- **OA** (1 term): Annotation
- **DQV** (5 terms): Dimension, QualityAnnotation, inDimension, Metric, Category
- **DWC** (5 terms): Organism, MaterialEntity, Event, Occurrence, Identification (classes only)
- **ODO** (5 terms): ECSO - year of measurement; SALMON - Fishery type, Fish measurement type, Salmon escapement count, Fish stock type
- **ENVO** (7 terms): lentic water body, lake, pond, lotic water body, river, stream, bayou
- **ORG** (4 terms): Organization, Organizational Unit, has unit, has sub-organization

**DwC strategy note:** We MIREOT only a small set of DwC *classes* so our OWL classes can subclass them (e.g., `dwc:Event`, `dwc:Organism`, `dwc:MaterialEntity`). We keep DwC *properties* prefix-only and validate their use with SHACL rather than global OWL domain/range axioms.


**Why BFO for FSAR Tracer:**

- Clarifies entity types: processes (events, methods) vs material entities (organisms, samples) vs information entities (datasets, documents)
- Enables OBO Foundry alignment: Most OBO ontologies (including IAO) are grounded in BFO
- Improves reasoning: Proper BFO grounding enables better logical inference
- Doesn't compete with PROV-O: BFO = what things ARE; PROV-O = how things were DERIVED

#### 2.3.11.2 Prefix Declarations Only

**Use when:**

- Using properties only (not classes)
- Terms are universally known (SKOS, Dublin Core)
- Pure data typing (xsd:)
- Lightweight alignment without local definitions

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
- **RO** (reuse + alignment): RO:0002351 (has member), RO:0002350 (member of); use `rdfs:subPropertyOf`/`owl:equivalentProperty` when you need a local refinement
- **SKOS** (extensive): Concept, ConceptScheme, prefLabel, definition, etc.
- **DwC properties** (extensive): eventDate, samplingProtocol, parentEventID, measurementType, measurementValue, measurementUnit, etc.

#### 2.3.11.3 Decision Matrix

| Ontology   | Approach    | Terms Used                 | Rationale                              |
| ---------- | ----------- | -------------------------- | -------------------------------------- |
| **BFO**    | MIREOT      | 4 classes                  | Upper ontology grounding               |
| **IAO**    | MIREOT      | 4 classes, 2 properties    | Information artifacts (extends BFO)    |
| **OA**     | MIREOT      | 1 class                    | Defines Annotation for DQV             |
| **DQV**    | MIREOT      | 4 classes, 1 property      | Evidence completeness tracking         |
| **DWC**    | Mixed       | 5 classes (MIREOT) + prefix-only properties | Biodiversity standard                  |
| **ODO**    | MIREOT      | 5 classes                  | DataOne measurement, salmon ontology   |
| **ENVO**   | MIREOT      | 7 classes                  | SIL/SEN environmental parameters       |
| **ORG**    | MIREOT      | 2 classes, 2 properties    | DFO Organizational Structure           |
| **PROV-O** | Prefix only | ~6 properties              | Provenance relations                   |
| **RO**     | Prefix only | Reuse RO IRIs; align via `rdfs:subPropertyOf` / `owl:equivalentProperty` | Interoperable relations                |
| **SKOS**   | Prefix only | Extensive                  | Core W3C vocabulary                    |
| **SHACL**  | Prefix only | Validation language        | Not a domain ontology                  |

**Why This Matters:**

- **Performance**: MIREOT = fast loading; full imports = slow
- **Clarity**: Local term definitions aid understanding in Protégé
- **Maintenance**: Fewer dependencies = easier updates
- **Interoperability**: Pragmatic balance between standards compliance and usability

**FSAR Tracer Specific Usage:**

BFO Classes (via MIREOT):

- `bfo:0000015` (process) → StatusAssessment, AnalysisMethod, ManagementDecision
- `bfo:0000040` (material entity) → Stock, GeneticSample
- `bfo:0000031` (generically dependent continuant) → ScientificOutput

DQV Classes (via MIREOT):

- `dqv:Dimension` → EvidenceCompletenessDimension, DataCurrencyDimension
- `dqv:QualityAnnotation` → CompleteEvidence, GapsEvidence, MissingCriticalEvidence

PROV-O Properties (prefix-only):

- `prov:used` → StatusAssessment uses Dataset/ReferencePoint
- `prov:wasGeneratedBy` → StatusAssessment generated by AnalysisMethod
- `prov:wasDerivedFrom` → ScientificOutput derived from StatusAssessment
- `prov:wasAttributedTo` → StatusAssessment attributed to Agent

---

### 2.3.12 Upper-Level Ontology Alignment Strategy

This section describes how to align `gcdfo:` (DFO Salmon Ontology) with established upper-level and domain ontologies. The alignment follows a **top-down approach**: we identify the most general ontological commitments first (BFO/IAO), then progressively specialize through observation/provenance patterns (SOSA/PROV), variable decomposition (I-ADOPT), and finally biodiversity interoperability (Darwin Core).

#### 2.3.12.1 Alignment Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  BFO (Basic Formal Ontology) - Top-Level Ontology          │
│    └── IAO (Information Artifact Ontology)                  │
│          └── PROV-O (Provenance Ontology)                   │
│                └── SOSA/SSN (Observations & Sensors)        │
│                      └── I-ADOPT (Variable Decomposition)   │
│                            └── Darwin Core (Biodiversity)   │
│                                  └── gcdfo: (Salmon Domain) │
└─────────────────────────────────────────────────────────────┘
```

**Key principle:** Each layer provides progressively more specialized semantics. BFO answers "what kind of thing is this?" (continuant vs occurrent); PROV-O answers "who/what produced this?"; SOSA answers "how was this measured?"; I-ADOPT answers "what property was measured?"; Darwin Core answers "how do I publish to GBIF?"

#### 2.3.12.2 BFO (Basic Formal Ontology)

**Namespace:** `http://purl.obolibrary.org/obo/BFO_`
**Purpose:** Provides the foundational ontological distinctions for all domain classes.

BFO is an ISO/IEC standard (ISO/IEC 21838-2:2021) top-level ontology that distinguishes:
- **Continuants** (entities that persist through time): Independent continuants (organisms, material entities) vs. dependent continuants (qualities, roles, functions)
- **Occurrents** (entities that unfold in time): Processes, temporal regions

**Alignment guidance for `gcdfo:`:**

| gcdfo: Class Type | BFO Alignment | Example |
|-------------------|---------------|---------|
| Physical entities (salmon, samples) | `BFO:0000040` (material entity) | `gcdfo:SalmonSpecimen rdfs:subClassOf BFO:0000040` |
| Qualities/properties | `BFO:0000019` (quality) | `gcdfo:ForkLength rdfs:subClassOf BFO:0000019` |
| Roles | `BFO:0000023` (role) | `gcdfo:BreederRole rdfs:subClassOf BFO:0000023` |
| Processes/activities | `BFO:0000015` (process) | `gcdfo:SpawningEvent rdfs:subClassOf BFO:0000015` |
| Temporal regions | `BFO:0000008` (temporal region) | Return year spans |

**When to use BFO alignment:**
- Creating new OWL classes that need rigorous ontological grounding
- Ensuring interoperability with OBO Foundry ontologies (ENVO, OBI, etc.)
- When reasoning over fundamental entity types is required

**References:**
- [BFO Official Site](https://basic-formal-ontology.org/)
- [OBO Foundry BFO](https://obofoundry.org/ontology/bfo.html)
- [BFO ISO Standard](https://www.iso.org/standard/74572.html)

#### 2.3.12.3 IAO (Information Artifact Ontology)

**Namespace:** `http://purl.obolibrary.org/obo/IAO_`
**Purpose:** Models information entities, data items, and their relationships to what they are about.

IAO extends BFO to handle information artifacts—entities whose function is to bear information quality. Key classes include:

| IAO Class | IRI | Use Case |
|-----------|-----|----------|
| `information content entity` | `IAO:0000030` | Parent class for all data/information |
| `data item` | `IAO:0000027` | Truthful statements about something |
| `measurement datum` | `IAO:0000109` | Results of measurements |
| `specification` | `IAO:0000104` | Protocols, methods |
| `document` | `IAO:0000310` | Reports, publications |

**Key property:** `IAO:0000136` (`is about`) – relates an information entity to what it describes.

**Alignment guidance for `gcdfo:`:**

```turtle
# A salmon assessment data item
gcdfo:EscapementEstimate rdfs:subClassOf IAO:0000027 ;
    IAO:0000136 gcdfo:SalmonPopulation .  # is about the population

# A sampling protocol specification
gcdfo:MarkRecaptureProtocol rdfs:subClassOf IAO:0000104 .
```

**When to use IAO alignment:**
- Modeling datasets, data items, or measurement results as first-class entities
- Distinguishing between the measured property (quality) and the recorded datum (information)
- Linking data to what it is about (especially for provenance)

**References:**
- [IAO GitHub](https://github.com/information-artifact-ontology/IAO)
- [OBO Foundry IAO](https://obofoundry.org/ontology/iao.html)

#### 2.3.12.4 PROV-O (Provenance Ontology)

**Namespace:** `http://www.w3.org/ns/prov#`
**Purpose:** Models provenance—how entities came to be, who/what was responsible, and what activities produced them.

PROV-O provides a W3C-standard vocabulary for provenance tracking:

| PROV Class | Description | gcdfo: Mapping |
|------------|-------------|----------------|
| `prov:Entity` | Things with provenance | Data products, samples, assessments |
| `prov:Activity` | Actions that transform/generate entities | Sampling events, observations, analyses |
| `prov:Agent` | Actors responsible for activities | Organizations, sensors, software |

**Key properties:**
- `prov:wasGeneratedBy` – Entity → Activity
- `prov:wasAttributedTo` – Entity → Agent
- `prov:used` – Activity → Entity
- `prov:wasAssociatedWith` – Activity → Agent
- `prov:wasDerivedFrom` – Entity → Entity

**PROV-SOSA Alignment (W3C standard):**

The W3C provides an official alignment between SOSA and PROV-O:

```turtle
# From W3C sosa-prov-mapping (SOSA↔PROV alignment)
sosa:Observation rdfs:subClassOf prov:Activity .
sosa:Sensor rdfs:subClassOf prov:Agent , prov:Entity .
sosa:Sample rdfs:subClassOf prov:Entity .
sosa:Result rdfs:subClassOf prov:Entity .
sosa:resultTime rdfs:subPropertyOf prov:endedAtTime .

# Procedure alignment is via an association node + a property chain:
# (sp:executionAssociation o sp:hadProcedure) ⊑ sosa:usedProcedure
sp:hadProcedure rdfs:subPropertyOf prov:hadPlan .
```

**Guidance for `gcdfo:`:**

```turtle
# An escapement survey is both a SOSA Sampling and a PROV Activity
gcdfo:EscapementSurvey rdfs:subClassOf sosa:Sampling , prov:Activity .

# The DFO agency as an agent
gcdfo:DFO rdf:type prov:Organization ;
    prov:actedOnBehalfOf gcdfo:GovernmentOfCanada .

# Derived data products
gcdfo:EscapementEstimate2024 prov:wasDerivedFrom gcdfo:RawCountData2024 ;
    prov:wasGeneratedBy gcdfo:MarkRecaptureAnalysis2024 ;
    prov:wasAttributedTo gcdfo:DFOStockAssessment .
```

**When to use PROV-O:**
- Tracking data lineage and derivation chains
- Attributing data products to responsible agents
- Documenting analytical workflows

**References:**
- [PROV-O W3C Recommendation](https://www.w3.org/TR/prov-o/)
- [SOSA-PROV Mapping](https://github.com/w3c/sdw/blob/gh-pages/ssn/rdf/sosa-prov-mapping.ttl)
- [PROV-to-BFO Mappings](https://github.com/BFO-Mappings/PROV-to-BFO)

#### 2.3.12.5 SOSA/SSN (Sensor, Observation, Sample, Actuator)

**Namespaces:**
- SOSA (lightweight core): `http://www.w3.org/ns/sosa/`
- SSN (full): `http://www.w3.org/ns/ssn/`

**Purpose:** Models observations, sampling, sensors, and the properties being observed.

SOSA/SSN is a joint W3C/OGC standard (W3C Recommendation 19 Oct 2017). A newer "2023 Edition" is in progress on the W3C Recommendation track as a First Public Working Draft (published 16 Sep 2025).

**Key SOSA classes for salmon data:**

| SOSA Class | Description | gcdfo: Example |
|------------|-------------|----------------|
| `sosa:Observation` | Act of observing a property | Count of fish at weir |
| `sosa:Sampling` | Act of creating/transforming samples | Collecting scale samples |
| `sosa:Sample` | Representative subset | Scale sample, tissue sample |
| `sosa:Sensor` | Device/agent making observations | Weir counter, human observer |
| `sosa:Procedure` | Method/protocol followed | Mark-recapture protocol |
| `sosa:FeatureOfInterest` | Entity being observed | Salmon population, river reach |
| `sosa:Property` | Quality being measured | Abundance, fork length |
| `sosa:Result` | Outcome of observation | Count value with uncertainty |

**Key SOSA properties:**

| Property | Domain | Range | Use |
|----------|--------|-------|-----|
| `sosa:hasFeatureOfInterest` | Observation/Sampling | FeatureOfInterest | What was observed |
| `sosa:observedProperty` | Observation | `sosa:Property` | What property was measured |
| `sosa:hasResult` | Observation | Result | The measurement outcome |
| `sosa:usedProcedure` | Observation | Procedure | Method used |
| `sosa:madeBySensor` | Observation | Sensor | What made the observation |
| `sosa:phenomenonTime` | Observation | time:TemporalEntity | When the property applied |
| `sosa:resultTime` | Observation | xsd:dateTime | When observation completed |
| `sosa:isSampleOf` | Sample | FeatureOfInterest | What the sample represents |

**When to use SOSA/SSN:**
- Modeling any measurement, observation, or count
- Representing sampling activities and sample provenance
- Linking observations to methods/protocols
- Distinguishing phenomenon time (when property applied) from result time (when recorded)

**References:**
- [SOSA/SSN W3C Recommendation (19 Oct 2017)](https://www.w3.org/TR/vocab-ssn/)
- [SSN/SOSA "2023 Edition" (First Public Working Draft, 16 Sep 2025)](https://www.w3.org/TR/vocab-ssn-2023/)
- [SOSA Namespace](http://www.w3.org/ns/sosa/)

#### 2.3.12.6 I-ADOPT Alignment

**See section 2.3.4.1.1 above** for full I-ADOPT alignment guidance, including:
- Variables as SKOS concepts
- I-ADOPT decomposition as annotations (Property, Entity in ObjectOfInterest role, Constraint)
- Canonical authoring pattern (local annotation properties)
- Interop projection (generated alignment layer)

**Key reminder:** I-ADOPT does NOT model methods/procedures. Use `sosa:Procedure`, `prov:Plan`, or `IAO:0000104` (specification) for method alignment.

#### 2.3.12.7 Darwin Core Alignment

**See section 6.6 External Alignments** for Darwin Core property alignment and section 6.9 for Darwin Core Conceptual Model usage.

**Key Darwin Core classes for salmon:**

| Class | Description | Salmon Use Case |
|-------|-------------|-----------------|
| `dwc:Event` | Action at a location/time | Survey event, sampling trip |
| `dwc:Occurrence` | Evidence of organism presence | Fish observation, catch record |
| `dwc:Organism` | Particular organism or group | Individual salmon, cohort |
| `dwc:MaterialEntity` | Physical object | Scale sample, tissue sample |
| `dwc:Taxon` | Taxonomic concept | *Oncorhynchus nerka* |
| `dwc:Location` | Spatial region | Fraser River, spawning grounds |

**Class alignment guidance:**

```turtle
# Event-type data
gcdfo:SurveyEvent rdfs:subClassOf dwc:Event .
gcdfo:SamplingTrip rdfs:subClassOf dwc:Event .

# Occurrence data
gcdfo:FishObservation rdfs:subClassOf dwc:Occurrence .

# Material samples
gcdfo:ScaleSample rdfs:subClassOf dwc:MaterialEntity .
gcdfo:TissueSample rdfs:subClassOf dwc:MaterialEntity .
```

**When to use Darwin Core:**
- Publishing biodiversity data to GBIF or other aggregators
- Modeling event-based sampling data
- Recording measurements about organisms, events, or materials
- Interoperability with the biodiversity informatics community

**References:**
- [Darwin Core Standard](https://www.tdwg.org/standards/dwc/)
- [Darwin Core RDF Guide](https://dwc.tdwg.org/rdf/)

#### 2.3.12.8 Decision Guide: Which Ontology to Use When

| Question | Primary Ontology | Secondary |
|----------|------------------|-----------|
| "What kind of thing is this?" | BFO | - |
| "Is this information or physical?" | IAO | BFO |
| "Who/what produced this data?" | PROV-O | - |
| "How was this measured?" | SOSA/SSN | PROV-O |
| "What property was measured?" | I-ADOPT | SOSA |
| "How do I publish to GBIF?" | Darwin Core | SOSA |
| "What constraints apply?" | I-ADOPT | gcdfo: SKOS |

---

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
    iao:0000115 "A specific survey event with measured parameters"@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

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
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .
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
**Properties:** Use lowerCamelCase (e.g., `aboutStock`, `usesMethod`, `hasConservationUnit`)
**SKOS Concepts:** Use PascalCase (e.g., `SonarCounting`, `MicrosatelliteAssay`)
**Instances:** Use PascalCase with descriptive names (e.g., `SkeenaSockeye`, `FraserCoho`)

**Why consistent naming matters:** It makes the ontology easier to read, understand, and maintain. It also helps prevent confusion when multiple people are contributing.

---

## 3. Design Patterns

### 3.1 Measurement Patterns

**Basic Measurement Pattern:**
Every measurement must have:

- `dwc:measurementType` / `dwciri:measurementType` - What was measured (text or controlled-vocabulary IRI in RDF)
- `dwc:measurementValue` - The measured value
- `dwc:measurementUnit` / `dwciri:measurementUnit` - The unit of measurement (text IRI or QUDT unit IRI in RDF)
- `dfo:aboutStock` - Which stock it describes
- `dfo:observedDuring` - Which event it was collected during
- `dfo:usesMethod` - Which method was used

**Example:**

```turtle
:EscapementCount2022 a dfo:EscapementMeasurement ;
    dwciri:measurementType <https://w3id.org/gcdfo/salmon#EscapementCount> ;
    dwc:measurementValue "1250"^^xsd:integer ;
    dwciri:measurementUnit <http://qudt.org/vocab/unit/Each> ;
    dfo:aboutStock :SkeenaSockeye ;
    dfo:observedDuring :SkeenaSurvey2022 ;
    dfo:usesMethod :SonarCounting .
```

### 3.2 Hierarchy Patterns

**Management Hierarchy Pattern:**

- Stock Management Units contain Conservation Units
- Conservation Units contain Populations
- Use explicit properties `dfo:hasConservationUnit` and `dfo:hasPopulation`
- Add inverse properties (`dfo:conservationUnitOf`, `dfo:populationOf`) when bidirectional queries matter

**Example:**

```turtle
:BCInteriorSMU a dfo:StockManagementUnit ;
    dfo:hasConservationUnit :FraserCUCoho .

:FraserCUCoho a dfo:ConservationUnit ;
    dfo:hasPopulation :FraserCohoPopulation .
```

### 3.3 Event Patterns

**Survey Event Pattern:**

- Surveys contain multiple measurement events
- Each measurement event has specific protocols
- Events can be nested (project > survey > measurement)

**Example:**

```turtle
:SalmonSurvey2023 a dfo:SurveyEvent ;
    dwc:eventDate "2023-05-01/2023-09-30"^^xsd:string ;
    dwc:samplingProtocol :DFOEscapementProtocol .

:DailyCount2023_06_15 a dfo:EscapementSurveyEvent ;
    dwc:parentEventID :SalmonSurvey2023 ;
    dwc:eventDate "2023-06-15"^^xsd:date ;
    dwc:samplingProtocol :SonarCountingProtocol .
```

---

## 4. Darwin Core Integration

**Why integrate with Darwin Core?** Darwin Core provides a widely-adopted standard for biodiversity data that enables interoperability with GBIF, OBIS, and other international biodiversity platforms. By aligning with Darwin Core, your salmon data becomes discoverable and usable by the broader scientific community.

> **📋 Complete Darwin Core Integration**: See the [README](../README.md) and [Architecture Decision Records](ADR.md) for the complete technical approach, including hybrid modeling strategy, core patterns, and Darwin Core integration details.

**Key Darwin Core Classes to Use:**

- `dwc:Event` - Actions, processes, or circumstances occurring at a place and time
- `dwc:Occurrence` - A state of an organism in an event
- `dwc:Organism` - A particular organism or defined group of organisms
- `dwc:MaterialEntity` - Physical samples/material entities that can be identified and managed
- `dwc:Identification` - Taxonomic determinations of organisms
- [DwC-CM] `dwc:Assertion` (under review) - A generalized assertion (e.g., measurement/occurrence) with provenance
- `dwc:Agent` - People, groups, organizations, machines, or software that can act
- `dwc:Media` - Digital media (images, videos, sounds, text)
- `dwc:Protocol` - Methods used during actions

**Note:** Use `dwc:MaterialEntity` for physical samples/materials in this project; we do not use `dwc:MaterialSample` (not part of DwC-CM).

**DFO Extensions:**

```turtle
# DFO-specific classes that extend Darwin Core (observation-centric interoperability)
dfo:SurveyEvent rdfs:subClassOf dwc:Event ;
    rdfs:label "Survey event"@en ;
    iao:0000115 "An event in which observations are made under a protocol at a place and time."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

dfo:EscapementSurveyEvent rdfs:subClassOf dfo:SurveyEvent ;
    rdfs:label "Escapement Survey Event"@en ;
    iao:0000115 "A survey event specifically for estimating escapement."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

dfo:Stock rdfs:subClassOf dwc:Organism ;
    rdfs:label "Stock"@en ;
    iao:0000115 "A population of salmon with distinct characteristics."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

dfo:GeneticSample rdfs:subClassOf dwc:MaterialEntity ;
    rdfs:label "Genetic Sample"@en ;
    iao:0000115 "A material entity used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

# Note: policy/reporting strata (e.g., CUs/SMUs) are information-defined groupings;
# model them under an information-content-entity superclass rather than forcing them under dwc:Event.
```

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
PREFIX dfo: <https://w3id.org/gcdfo/salmon#>
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

- **Warning**: `ERROR uk.ac.manchester.cs.jfact.datatypes.DatatypeFactory - A known datatype for https://w3id.org/gcdfo/salmon#EstimateType cannot be found; literal will be replaced with rdfs:Literal`
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
    iao:0000115 "A species of salmon (Oncorhynchus nerka)"@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .
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

### 6.4 Membership and Roll-up Pattern (SMU ▶ CU ▶ Population)

**What is the membership pattern?** This pattern represents the hierarchical relationship between Stock Management Units, Conservation Units, and Populations in salmon management.

**The Pattern:**

- Stock Management Units contain Conservation Units
- Conservation Units contain Populations
- Use explicit properties `hasConservationUnit` and `hasPopulation` (instead of a transitive generic `hasMember`)
- Add inverse properties when needed for query ergonomics (`conservationUnitOf`, `populationOf`)

**Implementation:**

```turtle
:hasConservationUnit a owl:ObjectProperty ;
    rdfs:label "has Conservation Unit"@en ;
    iao:0000115 "Relates a Stock Management Unit to one of its constituent Conservation Units."@en ;
    rdfs:domain :StockManagementUnit ;
    rdfs:range :ConservationUnit ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

:hasPopulation a owl:ObjectProperty ;
    rdfs:label "has population"@en ;
    iao:0000115 "Relates a Conservation Unit to one of its constituent populations."@en ;
    rdfs:domain :ConservationUnit ;
    rdfs:range :Population ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .

# Example usage
:BCInteriorSMU a :StockManagementUnit ;
    :hasConservationUnit :FraserCUCoho .

:FraserCUCoho a :ConservationUnit ;
    :hasPopulation :FraserCohoPopulation .
```

### 6.5 Measurement and GSI Conventions

#### 6.5.1 Escapement Measurements

**Required elements for every escapement measurement:**

- `dwc:measurementType` / `dwciri:measurementType` - What was measured (text or, in RDF, a controlled-vocabulary IRI when available)
- `dwc:measurementValue` - The measured value
- `dwc:measurementUnit` / `dwciri:measurementUnit` - The unit of measurement (text IRI or, in RDF, a QUDT unit IRI)
- `dfo:aboutStock` - Which stock it describes
- `dfo:observedDuring` - Which event it was collected during
- `dfo:usesMethod` - Which method was used

**Example:**

```turtle
:EscapementCount2022 a :EscapementMeasurement ;
    dwciri:measurementType <https://w3id.org/gcdfo/salmon#EscapementCount> ;  # controlled-vocabulary IRI for the measured variable
    dwc:measurementValue "1250"^^xsd:integer ;
    dwciri:measurementUnit <http://qudt.org/vocab/unit/Each> ;
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

**Terminology:** “Primary source” means we reuse an external IRI as the canonical identifier for a concept; “alignment” means our local IRI is canonical and we link to external IRIs with mapping predicates.

**Key external vocabularies:**

- **QUDT**: Units of measurement (http://qudt.org/vocab/unit/)
- **ENVO**: Environmental terms (http://purl.obolibrary.org/obo/ENVO_)
- **GBIF Backbone**: Taxonomic names (http://www.gbif.org/species/)
- **Darwin Core**: Biodiversity data standards (http://rs.tdwg.org/dwc/terms/)
- **RO (Relations Ontology)**: Standard relations (http://purl.obolibrary.org/obo/RO_)
- **AGROVOC**: Agricultural/fisheries thesaurus for broad concepts and indexing (usually alignment; OK as primary source for generic, non-salmon-specific concepts) (https://agrovoc.fao.org/)
- **Wikidata**: Broad, community-edited identifier hub (alignment-only; use for reconciliation/crosswalks, not canonical modeling) (https://www.wikidata.org/)
- **Schema.org/DCAT**: Web and catalog vocabularies for datasets and distributions
- **IAO**: Information artifact ontology for documents and datasets
- **ORG**: Organizational structure and units (https://www.w3.org/TR/vocab-org/)

**Darwin Core note:** In RDF, Darwin Core provides `dwciri:` properties (http://rs.tdwg.org/dwc/iri/) for cases where the object is an IRI (e.g., `dwciri:measurementType`, `dwciri:measurementUnit`, `dwciri:lifeStage`). Many Darwin Core terms are `rdf:Property`; align them like properties (e.g., `owl:equivalentProperty` / `rdfs:subPropertyOf`), not with `skos:*Match`.

**OBO Foundry Relation Reuse Requirements:**

- **Check RO first**: Before defining new relations, check if equivalent relations exist in RO
- **Import and reuse RO properties**: Import RO and use its properties directly where appropriate
- **Map via equivalence/subproperty**: Use `owl:equivalentProperty` or `rdfs:subPropertyOf` to align with RO
- **For classes**: Use `owl:equivalentClass` or `rdfs:subClassOf` to align with external ontologies
- **For SKOS concepts**: Use `skos:exactMatch` or `skos:closeMatch` for concept-level mappings (not for OWL properties)
- **Do NOT use `rdfs:seeAlso` for alignment**: `rdfs:seeAlso` is for helpful extra links, not semantic alignment
- **Avoid label conflicts**: OBO Foundry review flags non-RO relations with RO-equivalent labels

**Mapping confidence ladder (required):**

1. **Candidate (no axiom yet):** keep as an editorial candidate (notes/issue only), no logical mapping axiom.
2. **Hierarchy-level confidence:** use `rdfs:subPropertyOf` (properties) or `rdfs:subClassOf` (classes).
3. **Equivalence-level confidence:** use `owl:equivalentProperty` (properties) or `owl:equivalentClass` (classes).
4. **Concept mappings only:** use `skos:exactMatch` / `skos:closeMatch` only for concept-to-concept mappings.

**Promotion criteria (minimum evidence):**

- **Candidate -> hierarchy-level:** textual definitions + intended use are directionally compatible, and no known contradiction from competency questions.
- **Hierarchy-level -> equivalence-level:** reciprocal use in test queries shows substitutability in both directions and no contradictory domain/range intent.
- **Any promotion decision:** capture rationale in PR/issue notes so future contributors can trace why the axiom strength was chosen.

**Example RO Alignment:**

```turtle
# Option 1: Import RO and reuse directly
# (Import RO ontology, then use RO:0002351 directly)

# Option 2: Create subproperty of RO relation
:hasMember rdfs:subPropertyOf <http://purl.obolibrary.org/obo/RO_0002351> ; # RO:0002351 has member
    rdfs:label "has member"@en ;
    iao:0000115 "A transitive relationship indicating membership in a group."@en .

# Option 3: Map via equivalence
:hasMember owl:equivalentProperty <http://purl.obolibrary.org/obo/RO_0002351> ; # RO:0002351 has member
    rdfs:label "has member"@en .

# Do NOT do this for alignment:
# :hasMember rdfs:seeAlso <http://purl.obolibrary.org/obo/RO_0002351> .  # Wrong - seeAlso is not for alignment
```

**Implementation:**

- **Properties**: Import RO and reuse, or map via `owl:equivalentProperty` / `rdfs:subPropertyOf`
- **Classes**: Import external ontologies or map via `owl:equivalentClass` / `rdfs:subClassOf`
- **SKOS concepts**: Use `skos:exactMatch`/`skos:closeMatch` only for concept-level mappings
- **rdfs:isDefinedBy**: Point at your ontology/module IRI (required)
- **rdfs:seeAlso**: Use only for helpful extra links, not for semantic alignment
- Store external IRIs as literals in `…UnitIRI` properties (for units, may transition to object properties)
- Use `dcterms:source` to reference external vocabularies
- Check RO for existing relations before defining new ones

Practical guidance for new relationships:

- Before minting a custom property like `partOfRiver`, prefer the generic OBO relation `<http://purl.obolibrary.org/obo/BFO_0000050>` (part of) and model “river” via the class hierarchy (e.g., `dfo:RiverSegment`).
- When a domain-specific refinement is needed, define a custom subproperty aligned to RO (e.g., `dfo:hasConservationUnit rdfs:subPropertyOf <http://purl.obolibrary.org/obo/RO_0002351>`). This keeps reasoning consistent and improves interoperability.

**Unit Property Enhancement (Non-breaking):**
For richer unit semantics, consider adding object properties alongside datatype properties:

```turtle
# Current approach: Store QUDT IRIs as literals
:measurementUnitIRI a owl:DatatypeProperty ;
    rdfs:label "measurement unit IRI"@en ;
    iao:0000115 "IRI of the unit used in a measurement"@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    rdfs:domain :Measurement ;
    rdfs:range xsd:anyURI .

# Enhanced approach: Add object property for reasoning
:hasUnit a owl:ObjectProperty ;
    rdfs:label "has unit"@en ;
    iao:0000115 "Links a measurement to a unit (e.g., QUDT Unit)"@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> ;
    rdfs:domain :Measurement ;
    rdfs:range qudt:Unit .

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

**Base IRI:** `https://w3id.org/gcdfo/salmon#`

**Class IRIs:** `https://w3id.org/gcdfo/salmon#ClassName`
**Property IRIs:** `https://w3id.org/gcdfo/salmon#propertyName`
**Instance IRIs:** `https://w3id.org/gcdfo/salmon#InstanceName`

**Example:**
```turtle
@prefix dfo: <https://w3id.org/gcdfo/salmon#> .

dfo:EscapementMeasurement a owl:Class ;
    rdfs:label "Escapement Measurement"@en ;
    iao:0000115 "A measurement of salmon escapement"@en ;
    rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon> .
```

#### 6.7.2 Versioning

**Ontology versioning:**
- Use `owl:versionInfo` for version numbers
- Use `owl:versionIRI` for version-specific IRIs
- Use `owl:priorVersion` for the immediate previous version (previous version means the last published release)
- Tag releases in GitHub
- Maintain changelog
- Publish release snapshots under `docs/releases/X.Y.Z/` (a release snapshot is an immutable copy of the docs + serializations)

**Manual release steps (manual means you must run these yourself; CI does not publish releases):**
1. Update `ontology/dfo-salmon.ttl` header fields: `dcterms:modified`, `owl:versionInfo`, `owl:versionIRI`, `owl:priorVersion`.
2. Run `devenv shell make ci` (CI means automated checks on every push; it regenerates docs and must be committed).
3. Run `devenv shell make release-snapshot VERSION=X.Y.Z` and commit `docs/releases/X.Y.Z/`.

**Example:**
```turtle
<https://w3id.org/gcdfo/salmon> a owl:Ontology ;
    owl:versionInfo "1.0.0" ;
    owl:versionIRI <https://w3id.org/gcdfo/salmon/1.0.0> ;
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

### 6.9 Upper-level Alignment (DwC vs OBOE vs SOSA/SSN)

This project follows an explicit, top-down alignment hierarchy (mirrors the Salmon Data Mobilization `salmon-domain-ontology` conventions):

**Alignment hierarchy (top-down):**
BFO → IAO → PROV-O → SOSA/SSN → I-ADOPT → Darwin Core → `gcdfo:` (salmon domain)

**Rules of thumb (which one do I reach for?):**
- **BFO / IAO**: upper-level typing and the info-vs-physical split (what kind of thing is this?).
- **PROV-O**: provenance (who/what produced a dataset/record/result).
- **SOSA/SSN**: observation/measurement event structure (how was a result produced?).
- **I-ADOPT**: decomposable variable meaning (property + object of interest + constraints/context/matrix).
- **Darwin Core (DwC / DwC-CM)**: interoperability scaffold for publishing/aligning biodiversity records (GBIF/OBIS etc.).
- **`gcdfo:`**: salmon-specific domain terms that aren’t already standardized elsewhere.

**How this relates to OBOE:**
- OBOE is a valid observation/measurement model. In this ontology, SOSA/SSN is the preferred reference frame for observation structure, and we maintain crosswalk documentation where needed (see `docs/i-adopt-x-walk.md`).

**Darwin Core Conceptual Model note:**
- We implement DwC-CM patterns for record structure and interoperability; use DwC terms when the intent is explicitly to publish/consume Darwin Core-compatible data.

(See also: `docs/i-adopt-x-walk.md` for SSN/SOSA ↔ O&M ↔ OBOE ↔ I-ADOPT ↔ DwC-CM crosswalk.)

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
:SkeenaSurvey2023 a dfo:SurveyEvent ;
    dwc:eventDate "2023-08-15"^^xsd:date ;
    dwc:samplingProtocol :SonarCountingProtocol ;
    dwc:recordedBy :DFOFieldTeam .

:SkeenaSockeye a dfo:Stock ;
    rdfs:label "Skeena Sockeye"@en ;
    iao:0000115 "Sockeye salmon from the Skeena River watershed"@en .

:SonarCount2023_08_15 a dfo:EscapementMeasurement ;
    dwciri:measurementType <https://w3id.org/gcdfo/salmon#EscapementCount> ;
    dwc:measurementValue "1250"^^xsd:integer ;
    dwciri:measurementUnit <http://qudt.org/vocab/unit/Each> ;
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
    iao:0000115 "Genetic reporting unit for Fraser River sockeye"@en .

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
robot annotate --input dfo-salmon.ttl --ontology-iri "https://w3id.org/gcdfo/salmon" --version-iri "https://w3id.org/gcdfo/salmon/1.0.0" --output dfo-salmon-annotated.ttl
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

- See [Quick Start Cheatsheet → Essential Elements](#essential-elements-canonical-checklist) for the canonical “what every term needs” checklist.
- Use **OWL classes and properties** for formal structure and logical relationships; use **SKOS** when you need a picklist or controlled vocabulary.
- Follow **Darwin Core** as your interoperability scaffold for observations (events/organisms/material entities), not as a forced upper ontology for everything.

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
