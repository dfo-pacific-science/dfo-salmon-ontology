# DFO Salmon Ontology — Conventions Guide

This document orients new contributors to the modeling conventions used in the **DFO Salmon Ontology**. It explains how to create and refine ontology terms, how to model data in a way that aligns with our goals, and how to prepare new concepts for integration.

The conventions here are **practical starting points**, not immutable rules. As our community gains experience, we expect to refine and evolve them.

---

## 🚀 Quick Start Cheatsheet

**For experienced contributors who need a quick reference:**

### Essential Elements (Every Term Needs)

- **Label**: `rdfs:label "Human Name"@en`
- **Definition**: `iao:0000115 "1–2 sentence definition."@en`
- **Source**: `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>`

### Naming Conventions

- **Classes**: PascalCase (e.g., `EscapementMeasurement`)
- **Properties**: lowerCamelCase (e.g., `aboutStock`, `usesMethod`)
- **SKOS Concepts**: PascalCase (e.g., `SonarCounting`)

### Core Patterns

- **Measurements**: Must link to stock, event, and method
- **Hierarchy**: SMU ▶ CU ▶ Population with `hasMember` relationships (use correct OWL 2 transitivity syntax)
- **Units**: Store QUDT IRIs as literals in `…UnitIRI` properties
- **Darwin Core**: Use as top-level classes for interoperability
- **Hybrid Approach**: SKOS for methods, OWL for events with metadata
- **Manual Classification**: Estimate types are manually assigned based on Hyatt 1997 criteria
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
   - [2.5 Automated Classification](#25-automated-classification-with-shacl)
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

### 1.1 What is Knowledge Modeling?

Knowledge modeling (also called ontology engineering) is the practice of creating formal representations of knowledge that both humans and computers can understand. Think of it as creating a shared vocabulary and set of rules that describe how concepts in a domain relate to each other.

**Why do we need conventions?** Without consistent conventions, different people might model the same concept in different ways, leading to confusion and data that can't be easily combined or queried. Conventions ensure that:

- Everyone uses the same terms for the same concepts
- Data can be automatically validated and processed
- Different systems can exchange information seamlessly
- Future users can understand and extend the work

### 1.2 Ontology vs Knowledge Graph vs Graph Database

Understanding these distinctions is crucial for proper data management and system design.

**Ontology (Schema)**

- **What it is**: A formal specification of concepts, relationships, and rules in a domain
- **Contains**: Classes, properties, SKOS vocabularies, axioms, constraints
- **Purpose**: Defines the "vocabulary" and "grammar" for describing data
- **Example**: `EscapementSurveyEvent` class, `usesEnumerationMethod` property, `SnorkelSurvey` SKOS concept
- **File**: `dfo-salmon.ttl` (schema only, no instance data)

**Knowledge Graph (Data)**

- **What it is**: A collection of interconnected data instances following an ontology schema
- **Contains**: Specific instances, facts, measurements, events
- **Purpose**: Stores actual data using the ontology's vocabulary
- **Example**: `SkeenaSnorkel2022_001` survey event with specific measurements
- **File**: Separate data files (e.g., `survey-data-2022.ttl`)

**Graph Database (Storage)**

- **What it is**: A database system optimized for storing and querying graph-structured data
- **Contains**: Both schema and data, optimized for traversal and querying
- **Purpose**: Efficient storage and retrieval of graph data
- **Example**: Neo4j, Amazon Neptune, Apache Jena TDB
- **File**: Database files, not human-readable

**Why This Matters for DFO Salmon Ontology:**

1. **Schema vs Data Separation**: Keep the ontology file clean and focused on definitions
2. **Versioning**: Ontology changes independently of data updates
3. **Reusability**: Same schema can be used for multiple datasets
4. **Maintenance**: Easier to manage and validate schema separately
5. **Interoperability**: Other systems can import just the schema

### 1.3 Why This Ontology?

The **DFO Salmon Ontology** provides a domain-fit semantic layer for Pacific salmon data. It is designed to make datasets from **stock assessment, genetics, and management** interoperable and support **integration** across regional, national, and international systems.

> **📋 Complete Purpose & Objectives**: See the [DFO Salmon Ontology: Product Requirements Document](PRODUCT_REQUIREMENTS.md) for the complete overview of the ontology's purpose, objectives, and target users.

We take inspiration from:

- **Darwin Core (DwC) & the DwC Conceptual Model (DwC-CM)**
- **NCEAS Salmon Ontology (SALMON.ttl)**
- **Standard vocabularies** like QUDT (units), ENVO (environments), and GBIF Backbone (taxa)

### 1.4 Modeling Approach

- We model **primarily in OWL** (Web Ontology Language).
- We **also allow SKOS** for lightweight vocabularies (lists of methods, categories, codes).
- All terms must be represented in **Turtle (.ttl)** format.
- We emphasize **simplicity first**: one ontology file (`dfo-salmon.ttl`) is the starting point.
  - Later, we may modularize into separate files for stock, genetics, governance, etc.

**OBO Foundry Alignment:**

- Follow OBO Foundry principles for open, interoperable ontologies
- Use ROBOT for ontology development workflows
- Maintain logical well-formedness and scientific accuracy
- Ensure non-overlapping and strictly-scoped content
- Use standard OBO annotation properties and relations
- Follow OBO naming conventions and best practices

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
    iao:0000115 "A specific survey event with measured parameters"@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

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
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name in English (required, one per language)
- **Definition:** `iao:0000115 "1–2 sentence definition."@en` - A clear explanation of what this class represents (required, one only)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Links back to our ontology (required)

**Optional elements:**

- **Definition source (text):** `iao:0000119 "Citation text here."@en` - Human-readable citation for where the definition came from (optional, 0..*)
- **Definition source (link):** `dcterms:source <https://doi.org/...>` - Resolvable link to authoritative document or resource (optional, 0..*)
- **Examples:** `iao:0000112 "Concrete example of usage."@en` - Concrete examples of how this class is used (optional, 0..*)
- **Notes:** `rdfs:comment "Editorial note."@en` - Optional editorial notes (NOT a definition)
- **Alternative label:** `skos:prefLabel "Alternative Label"@en` - Optional secondary label for SKOS consumers (non-normative)
- **SKOS mirror label:** When a class also carries `skos:prefLabel`, duplicate the same literal in `rdfs:label` so OWL tooling and SKOS consumers stay in sync.

**Why these are required:** Labels help humans understand what you mean, definitions prevent confusion about scope, and source attribution ensures proper credit and traceability. Using `rdfs:label` and `IAO:0000115` aligns with OBO Foundry standards and ROBOT tooling expectations. The `skos:prefLabel` can optionally be added on OWL terms for SKOS consumers, but `rdfs:label` is primary and required.

**Example:**

```turtle
:GeneticSample a owl:Class ;
    rdfs:label "Genetic Sample"@en ;
    iao:0000115 "Tissue or material used in genetic stock identification analyses."@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
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
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Links back to our ontology (required)

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
    iao:0000119 "DFO stock assessment protocols 2024"@en ;
    iao:0000112 "A sockeye escapement measurement about Fraser River sockeye stock."@en ;
    rdfs:domain :Measurement ;  # Use conservatively - prefer class restrictions where possible
    rdfs:range :Stock ;
    dcterms:source <https://doi.org/10.1234/dfo-protocols-2024> .
```

**Alignment with Relations Ontology (RO):** When aligning to RO, import and reuse RO properties, or use `owl:equivalentProperty` / `rdfs:subPropertyOf` where appropriate. Use `skos:exactMatch`/`skos:closeMatch` only for concept-level mappings, not for OWL properties. Do not use `rdfs:seeAlso` for property alignment.

#### 2.3.3 Datatype Properties

**What are datatype properties?** Datatype properties link instances to literal values (text, numbers, dates). For example, "measurementValue" links a measurement to its numeric value.

**Required elements for every datatype property:**

- **Type declaration:** `a owl:DatatypeProperty`
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name (required, one per language)
- **Definition:** `iao:0000115 "1–2 sentence definition."@en` - A clear explanation of what this property represents (required, one only)
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Links back to our ontology (required)

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
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
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Links back to our ontology (required)

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

**Note on ROBOT Validation:** ROBOT may report missing `rdfs:label` for SKOS concepts that have `skos:prefLabel`. Per W3C SKOS specification, `skos:prefLabel` is a subproperty of `rdfs:label`, so these concepts ARE properly labeled. Either configure ROBOT to accept `skos:prefLabel` without requiring `rdfs:label` on SKOS concepts, or document that SKOS concepts will duplicate `skos:prefLabel → rdfs:label` for ROBOT compatibility.

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
    dcterms:source <https://doi.org/10.1234/dfo-esc-methods-2023> ;
    iao:0000119 "DFO (2023). Escapement Survey Manual, Pacific Region."@en .
```

#### 2.3.5 Provenance and Citation Conventions

#### 2.3.5.1 Use of `iao:0000119`, `dcterms:identifier`, `dcterms:source`, `dcterms:bibliographicCitation`, and `rdfs:seeAlso`

To ensure consistent provenance documentation and FAIR compliance, follow these conventions when citing the source of a definition, dataset, or external standard:

| Property                            | Purpose                                                               | Expected Value Type | Example Use                                                              |
| ----------------------------------- | --------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------ |
| **`iao:0000119`** | Human-readable citation text specifically for the **definition source** (where the definition text came from). | Literal (string, language-tagged)    | `"DFO (2023). Escapement Survey Manual, Pacific Region."@en`             |
| **`dcterms:bibliographicCitation`** | General bibliographic citation text (not specifically definition source). | Literal (string, language-tagged)    | `"Smith et al. (2020). Salmon Population Dynamics."@en`             |
| **`dcterms:identifier`** | Internal textual identifier (human-readable local ID). **NOT an IRI, NOT a scheme code.** | Literal (string, plain)                 | `"DFO-SALMON:000123"`                                |
| **`dcterms:source`** | Resolvable link to authoritative document or resource (DOI, Handle, w3id, ARK). | IRI                 | `<https://doi.org/10.1234/dfostock.2023>`                                |
| **`rdfs:seeAlso`** | Optional helpful extra links (landing pages, download URLs, related resources). | IRI                 | `<https://open.canada.ca/data/en/dataset/escapement-survey-manual-2023>` |

**Guideline:**  
- **`iao:0000119`**: Use strictly for definition textual provenance (citation text for where the definition came from)
- **`dcterms:bibliographicCitation`**: Use for general bibliographic strings that aren't specifically "definition source"
- **`dcterms:source`**: Use for resolvable links (IRI) to authoritative documents or resources
- **`dcterms:identifier`**: Use only for literal internal IDs (e.g., "DFO-SALMON:000123"), not IRIs, not codes
- **`rdfs:seeAlso`**: Use optionally for helpful extra links, not as the primary provenance hook
- **Codes**: Put scheme codes in `skos:notation` (typed literal), not in labels or identifiers

---

#### 2.3.5.2 Example — Class Definition with Proper Citation

```turtle
:EscapementSurveyEvent a owl:Class ;
    rdfs:label "Escapement Survey Event"@en ;
    iao:0000115 "A survey event conducted to measure salmon escapement."@en ;
    rdfs:subClassOf dwc:Event ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;

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
  rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;  # required
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
  rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;  # required
  dcterms:source <https://doi.org/10.xxxx/zzz> ;   # optional (IRI)
  IAO:0000119 "DFO (2023) Escapement Manual …"@en .  # optional (text)
```

**Key differences:**

- **OWL terms**: Use `rdfs:label` (required) and `IAO:0000115` (required) for definition
- **SKOS concepts**: Use `skos:prefLabel` (required) and `skos:definition` (recommended)
- **Codes**: Always use `skos:notation` with typed literal, never in labels or identifiers
- **Source links**: Use `dcterms:source` (IRI) for resolvable links, `IAO:0000119` (literal) for definition textual provenance
- **Identifiers**: Use `dcterms:identifier` only for literal internal IDs, not IRIs or codes

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

#### 2.3.8 Synonym Policy

**Default (recommended):** Use OBO In OWL synonym properties for typed synonyms:
- `oboInOwl:hasExactSynonym` - Exact synonyms
- `oboInOwl:hasRelatedSynonym` - Related but not exact synonyms
- `oboInOwl:hasBroadSynonym` - Broader terms
- `oboInOwl:hasNarrowSynonym` - Narrower terms

**Minimalist fallback:** Use `IAO:0000118` ("alternative term") if avoiding oboInOwl. Note that this loses synonym scope typing.

**On OWL terms:** If keeping `skos:altLabel` on OWL classes for convenience, state it's non-normative (no synonym scope). The primary approach should use oboInOwl properties.

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

**Three Approaches: Import vs MIREOT vs Prefix**

Understanding when to use each approach is critical for maintaining a lightweight, performant, and interoperable ontology.

#### 2.3.6.1 Full owl:imports (NOT used in DFO Salmon Ontology)

**Use ONLY when:**

- Using >20 terms from the ontology AND
- Need reasoning over imported axioms AND
- Ontology is small (<100 terms total)

**Risks:**

- Imports entire ontology (100s-1000s of terms)
- Slow loading and reasoning
- Potential conflicts with other imports
- Difficult to track which terms are actually used

**DFO Salmon Decision:** No full imports for MVP

#### 2.3.6.2 MIREOT (Minimum Information to Reference an External Ontology Term)

**Use when:**

- Need 3-20 specific terms with labels/definitions
- Want documentation in your ontology
- Don't need reasoning over the full imported ontology

**Method:**

1. Copy the term IRI (e.g., `bfo:0000015`)
2. Add minimal metadata: `rdfs:label`, `iao:0000115` (definition)
3. Add `rdfs:isDefinedBy` pointing to source ontology
4. Use the term as if it were native

**Benefits:**

- Lightweight (only terms you need)
- No import bloat
- Clear documentation
- Tools like Protégé recognize the terms
- Maintains semantic alignment with source

**Example - BFO MIREOT:**

```turtle
# Import specific BFO term via MIREOT
bfo:0000015 a owl:Class ;
  rdfs:label "process"@en ;
  iao:0000115 "An occurrent that has temporal parts."@en ;
  rdfs:isDefinedBy <http://purl.obolibrary.org/obo/bfo.owl> .

# Now use it in your ontology
dfo:StatusAssessment rdfs:subClassOf bfo:0000015 .  # process
```

**DFO Salmon MIREOT Terms:**

- **BFO** (4 terms): process, material entity, generically dependent continuant, specifically dependent continuant
- **IAO** (6 terms): measurement datum, information content entity, directive information entity, document, definition, definition source
- **OA** (1 term): Annotation
- **DQV** (5 terms): Dimension, QualityAnnotation, inDimension, Metric, Category
- **DWC** (8 terms): Organism, Material Entity, Agent, Media, Event, Occurrence, Identification, Protocol
- **ODO** (5 terms): ECSO - year of measurement; SALMON - Fishery type, Fish measurement type, Salmon escapement count, Fish stock type
- **ENVO** (7 terms): lentic water body, lake, pond, lotic water body, river, stream, bayou
- **ORG** (4 terms): Organization, Organizational Unit, has unit, has sub-organization


**Why BFO for FSAR Tracer:**

- Clarifies entity types: processes (events, methods) vs material entities (organisms, samples) vs information entities (datasets, documents)
- Enables OBO Foundry alignment: Most OBO ontologies (including IAO) are grounded in BFO
- Improves reasoning: Proper BFO grounding enables better logical inference
- Doesn't compete with PROV-O: BFO = what things ARE; PROV-O = how things were DERIVED

#### 2.3.6.3 Prefix Declarations Only

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

**Benefits:**

- Minimal overhead
- Clean separation
- Standard practice for well-known vocabularies

**Example - PROV-O Prefix Only:**

```turtle
# Declare prefix (no import, no local definitions)
@prefix prov: <http://www.w3.org/ns/prov#> .

# Use PROV-O properties directly
:BarkleyStatus2025 prov:used :EscapementDataset2025 ;
  prov:wasGeneratedBy :SRBenchmarkMethod ;
  prov:wasAttributedTo :StockAssessmentTeam .
```

**DFOC Salmon Prefix-Only:**

- **PROV-O** (~6 properties): wasGeneratedBy, wasDerivedFrom, used, wasAttributedTo, etc.
- **RO** (alignment via rdfs:seeAlso): has_member, member_of
- **SKOS** (extensive): Concept, ConceptScheme, prefLabel, definition, etc.
- **DwC** (extensive): Event, Organism, MeasurementOrFact, etc.

#### 2.3.6.4 Decision Matrix

| Ontology   | Approach    | Terms Used                 | Rationale                              |
| ---------- | ----------- | -------------------------- | -------------------------------------- |
| **BFO**    | MIREOT      | 4 classes                  | Upper ontology grounding               |
| **IAO**    | MIREOT      | 4 classes, 2 properties    | Information artifacts (extends BFO)    |
| **OA**     | MIREOT      | 1 class                    | Defines Annotation for DQV             |
| **DQV**    | MIREOT      | 4 classes, 1 property      | Evidence completeness tracking         |
| **DWC**    | MIREOT      | 8 classes                  | Biodiversity standard                  |
| **ODO**    | MIREOT      | 5 classes                  | DataOne measurement, salmon ontology   |
| **ENVO**   | MIREOT      | 7 classes                  | SIL/SEN environmental parameters       |
| **ORG**    | MIREOT      | 2 classes, 2 properties    | DFO Organizational Structure           |
| **PROV-O** | Prefix only | ~6 properties              | Provenance relations                   |
| **RO**     | Prefix only | Alignment via rdfs:seeAlso | Semantic documentation                 |
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

### 2.4 Hybrid Modeling Approach for Automated Classification

**Why a hybrid approach?** For automated classification systems (like Estimate Type assignment), we need both controlled vocabularies (methods) and rich data modeling (events with metadata). This hybrid approach separates concerns while enabling automation.

**Four-Layer Architecture:**

1. **Methods as SKOS Concepts** - Controlled vocabularies for enumeration and estimation methods
2. **Events as OWL Classes** - Survey/estimate events that extend Darwin Core Event
3. **Metadata on Events** - Rich data about how methods were applied in specific surveys
4. **Downgrade Criteria as SKOS** - Standardized criteria for automated type assignment

**Complete Example:**

```turtle
# Layer 1: SKOS Methods (Controlled Vocabularies)
:SnorkelSurvey a skos:Concept ;
    skos:prefLabel "Visual Snorkel Count"@en ;
    skos:definition "Two or more trained snorkelers conduct standardized passes within defined segments"@en ;
    skos:inScheme :EnumerationMethodScheme ;
    skos:broader :VisualSurveyMethod .

:AreaUnderCurve a skos:Concept ;
    skos:prefLabel "Area Under the Curve (AUC)"@en ;
    skos:definition "Integrates serial counts over time using a survey-life parameter"@en ;
    skos:inScheme :EstimateMethodScheme .

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
```

**Key Principles:**

- **Methods are vocabulary terms** - Use SKOS for enumeration methods, estimate methods, and downgrade criteria
- **Events carry the data** - OWL classes for survey events with rich metadata properties
- **Metadata on instances** - Observer efficiency, coverage, visibility are properties of specific surveys
- **Automated classification** - Rules engine checks event metadata against method-specific thresholds

### 2.5 Data Validation with SHACL

**Why SHACL?** SHACL (Shapes Constraint Language) provides validation rules that can enforce data quality and ensure required fields are present. It separates data validation from classification logic.

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
- `dwc:MaterialEntity` - Physical entities that can be identified and consist of matter
- `dwc:Identification` - Taxonomic determinations of organisms
- `dwc:Agent` - People, groups, organizations, machines, or software that can act
- `dwc:Media` - Digital media (images, videos, sounds, text)
- `dwc:Protocol` - Methods used during actions

**DFO Extensions:**

```turtle
# DFO-specific classes that extend Darwin Core
dfo:ManagementUnit rdfs:subClassOf dwc:Event ;
    rdfs:label "Management Unit"@en ;
    iao:0000115 "A geographic or administrative unit for salmon management"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

dfo:ConservationUnit rdfs:subClassOf dwc:Event ;
    rdfs:label "Conservation Unit"@en ;
    iao:0000115 "A biologically meaningful unit for conservation planning"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

dfo:Stock rdfs:subClassOf dwc:Organism ;
    rdfs:label "Stock"@en ;
    iao:0000115 "A population of salmon with distinct characteristics"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
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
PREFIX dfo: <https://w3id.org/dfoc/salmon#>
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

- **Warning**: `ERROR uk.ac.manchester.cs.jfact.datatypes.DatatypeFactory - A known datatype for https://w3id.org/dfoc/salmon#EstimateType cannot be found; literal will be replaced with rdfs:Literal`
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
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
```

#### 6.3.2 Equivalence

**What is equivalence?** Equivalence states that two classes are identical in meaning. Use this when two terms represent exactly the same concept.

**When to use equivalence:**

- When two classes have identical meaning but different names
- When aligning with external vocabularies
- When consolidating duplicate concepts

**Example:**

```turtle
:Escapement rdfs:subClassOf :Measurement ;
    owl:equivalentClass dwc:MeasurementOrFact ;
    rdfs:label "Escapement"@en .
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
    iao:0000115 "A transitive relationship indicating membership in a group"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

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

**OBO Foundry Relation Reuse Requirements:**

- **Check RO first**: Before defining new relations, check if equivalent relations exist in RO
- **Import and reuse RO properties**: Import RO and use its properties directly where appropriate
- **Map via equivalence/subproperty**: Use `owl:equivalentProperty` or `rdfs:subPropertyOf` to align with RO
- **For classes**: Use `owl:equivalentClass` or `rdfs:subClassOf` to align with external ontologies
- **For SKOS concepts**: Use `skos:exactMatch` or `skos:closeMatch` for concept-level mappings (not for OWL properties)
- **Do NOT use `rdfs:seeAlso` for alignment**: `rdfs:seeAlso` is for helpful extra links, not semantic alignment
- **Avoid label conflicts**: OBO Foundry review flags non-RO relations with RO-equivalent labels

**Example RO Alignment:**

```turtle
# Option 1: Import RO and reuse directly
# (Import RO ontology, then use ro:has_part directly)

# Option 2: Create subproperty of RO relation
:hasMember rdfs:subPropertyOf ro:has_part ;
    rdfs:label "has member"@en ;
    iao:0000115 "A transitive relationship indicating membership in a group."@en .

# Option 3: Map via equivalence
:hasMember owl:equivalentProperty ro:has_part ;
    rdfs:label "has member"@en .

# Do NOT do this for alignment:
# :hasMember rdfs:seeAlso ro:has_part .  # Wrong - seeAlso is not for alignment
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

**Unit Property Enhancement (Non-breaking):**
For richer unit semantics, consider adding object properties alongside datatype properties:

```turtle
# Current approach: Store QUDT IRIs as literals
:measurementUnitIRI a owl:DatatypeProperty ;
    rdfs:label "measurement unit IRI"@en ;
    iao:0000115 "IRI of the unit used in a measurement"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
    rdfs:domain :Measurement ;
    rdfs:range xsd:anyURI .

# Enhanced approach: Add object property for reasoning
:hasUnit a owl:ObjectProperty ;
    rdfs:label "has unit"@en ;
    iao:0000115 "Links a measurement to a unit (e.g., QUDT Unit)"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> ;
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

#### 6.7.1 IRI Structure

**Base IRI:** `https://w3id.org/dfoc/salmon#`

**Class IRIs:** `https://w3id.org/dfoc/salmon#ClassName`
**Property IRIs:** `https://w3id.org/dfoc/salmon#propertyName`
**Instance IRIs:** `https://w3id.org/dfoc/salmon#InstanceName`

**Example:**

```turtle
@prefix dfo: <https://w3id.org/dfoc/salmon#> .

dfo:EscapementMeasurement a owl:Class ;
    rdfs:label "Escapement Measurement"@en ;
    iao:0000115 "A measurement of salmon escapement"@en ;
    rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
```

#### 6.7.2 Versioning

**Ontology versioning:**

- Use `owl:versionInfo` for version numbers
- Use `owl:versionIRI` for version-specific IRIs
- Tag releases in GitHub
- Maintain changelog

**Example:**

```turtle
<https://w3id.org/dfoc/salmon> a owl:Ontology ;
    owl:versionInfo "1.0.0" ;
    owl:versionIRI <https://w3id.org/dfoc/salmon/1.0.0> ;
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
    iao:0000115 "Sockeye salmon from the Skeena River watershed"@en .

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
robot annotate --input dfo-salmon.ttl --ontology-iri "https://w3id.org/dfoc/salmon" --version-iri "https://w3id.org/dfoc/salmon/1.0.0" --output dfo-salmon-annotated.ttl
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

- **OWL terms**: Always use `rdfs:label` (required) and `IAO:0000115` (required) for definitions
- **SKOS concepts**: Use `skos:prefLabel` (required), `skos:inScheme` (required), and `skos:definition` (recommended)
- Use **OWL classes and properties** for formal structure and logical relationships
- Use **SKOS** when you need a picklist or controlled vocabulary
- Follow **Darwin Core** as your meta-framework for interoperability
- **Codes**: Use `skos:notation` with typed literal, never in labels or identifiers
- **Source links**: Use `dcterms:source` (IRI) for resolvable links, `IAO:0000119` (literal) for definition textual provenance

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
