# DFO Salmon Ontology — Conventions Guide

This document orients new contributors to the modeling conventions used in the **DFO Salmon Ontology**. It explains how to create and refine ontology terms, how to model data in a way that aligns with our goals, and how to prepare new concepts for integration.

The conventions here are **practical starting points**, not immutable rules. As our community gains experience, we expect to refine and evolve them.

---

## 🚀 Quick Start Cheatsheet

**For experienced contributors who need a quick reference:**

### Essential Elements (Every Term Needs)
- **Label**: `rdfs:label "Human Name"@en`
- **Definition**: `rdfs:comment "1–2 sentence definition."@en`
- **Source**: `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`
TODO: clarify format for DC TERMS and URI linkage
- **** **dcterms:source** ;

### Naming Conventions
- **Classes**: PascalCase (e.g., `EscapementMeasurement`)
- **Properties**: lowerCamelCase (e.g., `aboutStock`, `usesMethod`)
- **SKOS Concepts**: PascalCase (e.g., `SonarCounting`)

### Core Patterns
- **Measurements**: Must link to stock, event, and method
- **Hierarchy**: SMU ▶ CU ▶ Population with `hasMember` relationships
- **Units**: Store QUDT IRIs as literals in `…UnitIRI` properties
- **Darwin Core**: Use as top-level classes for interoperability
- **Hybrid Approach**: SKOS for methods, OWL for events with metadata
- **Automated Classification**: SHACL rules for type escapement estimate type assignment 1-6 (Hyatt 1997)

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
   - [What is Knowledge Modeling?](#11-what-is-knowledge-modeling)
   - [Ontology vs Knowledge Graph vs Graph Database](#12-ontology-vs-knowledge-graph-vs-graph-database)
   - [Why This Ontology?](#13-why-this-ontology)
   - [Modeling Approach](#14-modeling-approach)

2. [Getting Started](#2-getting-started)
   - [Essential Concepts](#21-essential-concepts)
   - [Schema vs Data Separation](#22-schema-vs-data-separation)
   - [Core Conventions](#23-core-conventions)
   - [Hybrid Modeling Approach](#24-hybrid-modeling-approach-for-automated-classification)
   - [Automated Classification](#25-automated-classification-with-shacl)
   - [Naming Conventions](#26-naming-conventions)

3. [Design Patterns](#3-design-patterns)
   - [Measurement Patterns](#31-measurement-patterns)
   - [Hierarchy Patterns](#32-hierarchy-patterns)
   - [Event Patterns](#33-event-patterns)

4. [Darwin Core Integration](#4-darwin-core-integration)
   - [Core Classes](#41-core-classes)
   - [DFO Extensions](#42-dfo-extensions)
   - [Predicate Alignment](#43-predicate-alignment)

5. [Quality Assurance](#5-quality-assurance)
   - [Pre-Submission Checklist](#51-pre-submission-checklist)
   - [Validation Steps](#52-validation-steps)
   - [Common Mistakes](#53-common-mistakes)

6. [Advanced Topics](#6-advanced-topics)
   - [Competency Questions](#61-competency-questions)
   - [Troubleshooting](#62-troubleshooting)
   - [External Alignments](#63-external-alignments)

7. [Resources](#7-resources)
   - [Tools and Workflows](#71-tools-and-workflows)
   - [Community Process](#72-community-process)
   - [Key Takeaways](#73-key-takeaways)

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

The **DFO Salmon Ontology** provides a domain-fit semantic layer for Pacific salmon data. It is designed to:

- Make datasets from **stock assessment, genetics, and management** interoperable.
- Support **integration** across regional, national, and international systems (GBIF, OBIS, ENVO, NCEAS Salmon Ontology).
- Allow scientists to ask questions like:  
  - *How many populations of salmon were monitored in 2022?*  
  - *What is the trend in regional abundance of Sockeye?*  
  - *How do GSI results map to Conservation Units and Management Units?*  
- Enable machine readability, FAIR data principles, and modern discovery tools.

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

#### Classes

**Required elements for every class:**
- **Type declaration:** `a owl:Class` - This tells the system this is a class
- **Label:** `rdfs:label "Human Name"@en` - A human-readable name in English
- **Definition:** `rdfs:comment "1–2 sentence definition."@en` - A clear explanation of what this class represents
- **Source attribution:** `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>` - Links back to our ontology
- **dcterms:source** "DFO Molecular Genetics Lab glossary 2024" ;

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

#### Object Properties

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

#### Datatype Properties

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

#### SKOS Concepts

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

**Example:**
```turtle
:SonarCounting a skos:Concept ;
    skos:prefLabel "Sonar Counting"@en ;
    skos:definition "Method of counting fish using sonar technology."@en ;
    rdfs:isDefinedBy <https://w3id.org/dfo/salmon> ;
    skos:broader :CountingMethod .
```

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
- **Automated classification** - Rules engine checks event metadata against method-specific thresholds

## 2.5 Framework and Upper Ontologies

Our ontology builds on widely adopted semantic frameworks to maximize interoperability and reuse. Each item below includes a canonical reference for contributors.

- **BFO — Basic Formal Ontology**  
  High-level categories (e.g., continuant, occurrent) used for consistent upper-level alignment.  
  Learn more: https://basic-formal-ontology.org/

- **SOSA/SSN — Sensor, Observation, Sample, and Actuator**  
  Patterns for observations, sampling, procedures, sensors, and results; we specialize salmon survey protocols from these.  
  Learn more: https://www.w3.org/TR/vocab-ssn/ (spec) • https://www.w3.org/TR/vocab-ssn/#SOSA (SOSA core)

- **Darwin Core Conceptual Model (DwC-CM)**  
  Our primary framework for Events, Occurrences, Organisms, Agents, Media, and Measurements, including nested Event hierarchies.  
  Learn more: https://dwc.tdwg.org/terms/ (terms) • https://dwc.tdwg.org/ (overview) • *Conceptual model page/diagram as adopted internally*

- **SKOS — Simple Knowledge Organization System**  
  Used for code lists/picklists (management groups, gear types, etc.) as SKOS concept schemes with persistent URIs.  
  Learn more: https://www.w3.org/TR/skos-reference/

- **PROV-O — Provenance Ontology**  
  Records data lineage (who/what/when/how), supporting FSAR traceability and auditability.  
  Learn more: https://www.w3.org/TR/prov-o/

- **DCAT — Data Catalog Vocabulary**  
  Describes datasets, distributions, and APIs for catalogs/portals.  
  Learn more: https://www.w3.org/TR/vocab-dcat-3/

- **QUDT — Quantities, Units, Dimensions and Data Types**  
  Canonical URIs for units and quantity kinds (e.g., counts, rates).  
  Learn more: https://qudt.org/

- **UCUM — Unified Code for Units of Measure**  
  Widely used machine-parsable unit codes; helpful for interoperability with clinical/engineering data.  
  Learn more: https://ucum.org/ and reference table: https://ucum.org/ucum.html

- **ENVO — Environment Ontology**  
  Environmental features, habitats, and related terms relevant to salmon ecosystems.  
  Learn more: https://environmentontology.org/ and OBO page: https://obofoundry.org/ontology/envo.html

- **CF Standard Names**  
  Standardized variable names for environmental/oceanographic data (temperature, salinity, etc.).  
  Learn more: https://cfconventions.org/ and name table: https://cfconventions.org/standard-names.html

**Contributor note (lookup order):**  
1) Check **DwC/DwC-CM** for classes/relations tied to events, occurrences, organisms, agents, and measurements.  
2) For observation/procedure patterns, reuse **SOSA/SSN** (and align to **OBI** patterns when needed).  
3) For labels/controlled values, mint as **SKOS** concepts when a formal OWL class is unnecessary.  
4) For units/quantities, prefer **QUDT** (URIs) and/or **UCUM** (codes).  
5) For environmental features/variables, reuse **ENVO** and **CF Standard Names**.  
6) Record lineage with **PROV-O** and describe published datasets with **DCAT**.

Only mint a new local term when no suitable external equivalent exists; when reusing, include mappings (e.g., `skos:exactMatch`, `owl:equivalentClass`) in the term’s annotations.

#### NCEAS Salmon Ontology

We check for overlap and reuse opportunities in the **Salmon Ontology (NCEAS, BioPortal)**, which provides a broad salmon-domain ontology.  

- **DFO-local vs. generic:** Terms that are specific to DFO operations (e.g., internal survey codes, methods) remain local. Terms with broad relevance (e.g., escapement survey, weir, hatchery release) should be proposed for inclusion in the Salmon Ontology through its community curation process.  
- **Reuse method:** When importing terms, we follow MIREOT-style referencing (importing only the necessary term with its IRI and definition).  
- **Alignment:** We use `owl:equivalentClass` or `skos:exactMatch` when a DFO-local class corresponds exactly to an external term. We use `skos:closeMatch`, `broadMatch`, or `narrowMatch` for partial alignments.  
- **Term requests:** Contributors proposing broadly reusable salmon concepts should open a local issue and flag it as “candidate for Salmon Ontology (BioPortal).” Maintainers will coordinate with the NCEAS ontology curators.  

**References:**  
- Salmon Ontology on BioPortal: https://bioportal.bioontology.org/ontologies/SALMON  
- OBO Foundry MIREOT guidelines: http://obi-ontology.org/page/MIREOT  

### 2.6 Automated Classification with SHACL

**Why SHACL?** SHACL (Shapes Constraint Language) provides validation rules that can enforce data quality and enable automated classification. It separates data validation from classification logic.

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

**Automated Type Assignment Rules:**
```turtle
# SHACL Rules for Estimate Type Assignment
:TypeAssignmentShape a sh:NodeShape ;
    sh:targetClass :EscapementSurveyEvent ;
    sh:rule [
        a sh:TripleRule ;
        sh:condition [
            sh:property [
                sh:path dfo:usesEnumerationMethod ;
                sh:hasValue :SnorkelSurvey
            ] ;
            sh:property [
                sh:path dfo:measuredVisits ;
                sh:minInclusive 5
            ] ;
            sh:property [
                sh:path dfo:measuredReachCoverage ;
                sh:minInclusive 0.8
            ] ;
            sh:property [
                sh:path dfo:measuredVisibility ;
                sh:in ( :Good :Excellent )
            ]
        ] ;
        sh:subject sh:this ;
        sh:predicate dfo:assignedEstimateType ;
        sh:object :Type2 ;
        sh:message "Snorkel survey meets Type 2 criteria"
    ] ;
    sh:rule [
        a sh:TripleRule ;
        sh:condition [
            sh:property [
                sh:path dfo:usesEnumerationMethod ;
                sh:hasValue :SnorkelSurvey
            ] ;
            sh:property [
                sh:path dfo:measuredVisits ;
                sh:minInclusive 3
            ] ;
            sh:property [
                sh:path dfo:measuredReachCoverage ;
                sh:minInclusive 0.5
            ]
        ] ;
        sh:subject sh:this ;
        sh:predicate dfo:assignedEstimateType ;
        sh:object :Type3 ;
        sh:message "Snorkel survey meets Type 3 criteria"
    ] .
```

**Implementation Pipeline:**
1. **Data Entry** - Users create survey events with metadata
2. **SHACL Validation** - Ensures required fields are present and valid
3. **Rule Application** - SHACL rules assign estimate types based on thresholds
4. **Downgrade Flags** - Attach downgrade criteria when thresholds aren't met
5. **Final Classification** - Apply downgrade rules to determine final type

### 2.7 Naming Conventions

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

**Examples:**
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

One example that ties this all together:

**Example:**
```turtle
# Event hierarchy per DwC-CM
:Project2025 a dwc:Event .
:Survey2025_08 a dwc:Event ; dwc:parentEventID :Project2025 ;
               dwc:samplingProtocol :DFOEscapementProtocol .
:CountEvent2025_08_15 a dwc:Event ; dwc:parentEventID :Survey2025_08 .

# Measurement attached to the event (DwC)
:CountMeasurement2025_08_15 a dfo:EscapementMeasurement ;
  dwc:measurementType "abundance" ;
  dwc:measurementValue "1250"^^xsd:integer ;
  dwc:measurementUnit "http://qudt.org/vocab/unit/Each" ;
  dfo:aboutStock :SkeenaSockeye ;
  dfo:observedDuring :CountEvent2025_08_15 ;
  dwc:recordedBy :DFOFieldTeam .
```

---

## 4. Darwin Core Integration

### 4.1 Core Classes

**Why integrate with Darwin Core?** Darwin Core provides a widely-adopted standard for biodiversity data that enables interoperability with GBIF, OBIS, and other international biodiversity platforms. By aligning with Darwin Core, your salmon data becomes discoverable and usable by the broader scientific community. 

Our backbone: We use the Darwin Core Conceptual Model to structure events, occurrences, organisms, agents, media and protocols, including nested Event hierarchies (project → survey → measurement). We treat DFO classes like EscapementSurveyEvent as specializations of dwc:Event, and we attach measurements via DwC measurement terms.

**Essential Core Classes:**
- `dwc:Event` - Actions, processes, or circumstances occurring at a place and time
- `dwc:Occurrence` - A state of an organism in an event
- `dwc:Organism` - A particular organism or defined group of organisms
- `dwc:MaterialEntity` - Physical entities that can be identified and consist of matter
- `dwc:Identification` - Taxonomic determinations of organisms
- `dwc:Agent` - People, groups, organizations, machines, or software that can act
- `dwc:Media` - Digital media (images, videos, sounds, text)
- `dwc:Protocol` - Methods used during actions

### 4.2 DFO Extensions

**Stock Management Hierarchy:**
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

### 4.3 Predicate Alignment

**Use Darwin Core predicates where appropriate:**
- `dwc:eventDate` for temporal information
- `dwc:locationID` for spatial references
- `dwc:recordedBy` for data collectors
- `dwc:identifiedBy` for taxonomic identifiers
- `dwc:samplingProtocol` for methods
- `dwc:measurementType` for measurement categories
- `dwc:measurementValue` for measurement values
- `dwc:measurementUnit` for units

**DFO-specific predicates:**
- `dfo:aboutStock` for stock relationships
- `dfo:usesMethod` for method relationships
- `dfo:hasMember` for hierarchical relationships
- `dfo:aboutReportingUnit` for genetic reporting units

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

### 5.2 Contributor Process

To propose a new term, contributors should follow this process:

1. **Open a GitHub Issue**  
   - Title: Proposed new term (e.g., “New Term: EscapementSurveyEvent”)  
   - Provide background and motivation, including competency questions the term should help answer.  
   - Suggest intended parent class (e.g., `dwc:Event`) and relationships.  

2. **Fill in the Term Request Template**  
   - Use the provided CSV or spreadsheet template with the following columns:  
     - **Label**: Human-readable name of the term  
     - **Definition**: Clear, genus-differentia style definition  
     - **Source**: Literature, dataset, or standard the definition is drawn from  
     - **Parent Class**: Intended superclass  
     - **Example Usage**: Example sentence or dataset context  
     - **Synonyms**: Optional, with type (exact, narrow, broad)  
     - **Notes**: Any additional clarifications  

3. **Provide a TTL Snippet (Optional for Stewards, Required for Maintainers)**  
   - Format according to existing ontology conventions (label, definition, annotations, subclass statement).  
   - Include mappings (`skos:exactMatch`, `skos:closeMatch`, `owl:equivalentClass`) where applicable.  

4. **Submit for Review**  
   - Attach the completed spreadsheet row (or CSV file) to the GitHub issue.  
   - Maintainers will review for compliance with design patterns, integration with hierarchy, and annotation completeness.  
   - Revisions may be requested before acceptance.  

5. **Integration and Validation**  
   - Once approved, the term will be added to the ontology source file.  
   - Automated validation (ROBOT, SHACL) will run to check logical consistency and required annotations.  
   - The issue will be closed once the term appears in the next ontology release.  

### 5.3 Validation Steps

**Logical Consistency:**
- [ ] Run reasoner (TODO: needs to be built first!) to check for unsatisfiable classes
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

### 5.4 Common Mistakes to Avoid

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


---

## 6. Advanced Topics

### 6.1 Competency Questions

**What are competency questions?** These are the specific questions your ontology should be able to answer. They guide design decisions and validate that the ontology serves its intended purpose. Competency questions are essential for ensuring your ontology can actually support the research and data integration needs of the salmon science community.

**Why competency questions matter:**
- **Design guidance**: Help determine what terms and relationships are needed
- **Validation mechanism**: Ensure the ontology can answer the questions it's designed to address
- **Testing framework**: Enable systematic validation of the ontology's utility
- **Community alignment**: Ensure all stakeholders understand the ontology's purpose

#### 6.1.1 Stock Assessment Competency Questions

**Population Monitoring:**
- "What escapement methods were used for Sockeye stocks in 2022?"
- "Which stocks showed declining trends over the last 5 years?"
- "What are all the measurement events for a specific Conservation Unit?"
- "Which Management Units contain stocks with critical status?"
- "What are all the stocks in a specific Management Unit?"

**Data Integration:**
- "Which datasets contain measurements for endangered stocks?"
- "What is the temporal coverage of escapement data for Skeena River stocks?"
- "Which measurement methods have been used for each stock over time?"

#### 6.1.2 Genetics (GSI) Competency Questions

**Sample Analysis:**
- "What GSI runs analyzed samples from Skeena River stocks?"
- "Which Reporting Units map to Conservation Unit X?"
- "What is the genetic composition of samples collected during Event Y?"
- "Which marker panels were used in GSI runs for 2023?"

**Population Genetics:**
- "What are the genetic relationships between different Reporting Units?"
- "Which samples show evidence of mixed stock origin?"
- "What is the temporal pattern of genetic diversity in a specific stock?"

#### 6.1.3 Management and Policy Competency Questions

**Conservation Status:**
- "Which Conservation Units are currently under recovery planning?"
- "What are the management actions associated with each Management Unit?"
- "Which stocks have been designated as critical or endangered?"

**Data Quality:**
- "What is the data quality assessment for measurements from 2022?"
- "Which datasets have been validated and by whom?"
- "What are the confidence intervals for abundance estimates?"

#### 6.1.4 Cross-Domain Integration Questions

**Spatial Integration:**
- "How do genetic Reporting Units align with Conservation Units geographically?"
- "What are the spatial relationships between Management Units and watersheds?"
- "Which stocks occur in multiple Management Units?"

**Temporal Integration:**
- "What is the temporal overlap between escapement surveys and genetic sampling?"
- "How have stock boundaries changed over time?"
- "What are the long-term trends in both abundance and genetic diversity?"

#### 6.1.5 Using Competency Questions

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

#### 6.2.4 Getting Help

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
:hasMember a owl:ObjectProperty ;
    rdfs:label "has member"@en ;
    rdfs:comment "A transitive relationship indicating membership in a group"@en ;
    owl:TransitiveProperty true .

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

**Implementation:**
- Store external IRIs as literals in `…UnitIRI` properties
- Use `dcterms:source` to reference external vocabularies
- Plan to convert to object properties in future versions

### 6.7 IRI and Versioning Policy

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

**Core Darwin Core classes to use:**
- `dwc:Event` for all events and activities
- `dwc:Occurrence` for organism observations
- `dwc:Organism` for individual organisms or groups
- `dwc:MaterialEntity` for physical samples
- `dwc:Identification` for taxonomic determinations
- `dwc:Agent` for people, organizations, and devices
- `dwc:Media` for digital media
- `dwc:Protocol` for methods and procedures

**DFO-specific extensions:**
- `dfo:ManagementUnit` extends `dwc:Event`
- `dfo:ConservationUnit` extends `dwc:Event`
- `dfo:Stock` extends `dwc:Organism`
- `dfo:EscapementMeasurement` extends `dwc:MeasurementOrFact`

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

*Maintainer: Data Stewardship Unit, DFO Pacific Science*  
*License: CC-BY 4.0*
