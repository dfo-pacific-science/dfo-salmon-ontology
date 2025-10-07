# DFO Salmon Ontology: Purpose and Competency Guide

**Namespace:** `https://w3id.org/dfo/salmon#` (prefix: `dfo:`)  
**License:** CC-BY 4.0  
**Status:** Draft Work in Progress

---

## 🎯 Primary Purpose

The DFO Salmon Ontology is a **data stewardship and operational process ontology** designed to provide a semantic framework for managing, integrating, and stewarding Pacific salmon data across Fisheries and Oceans Canada (DFO). Fundamentally, this data ontology serves as a Salmon-science-wide, standard digital language that enables easy information sharing and collaboration. 

**This is NOT a biological domain ontology** about salmon ecology or behavior, but rather an **operational ontology** that models:

- **Data collection processes** (surveys, sampling, monitoring)
- **Data analysis workflows** (stock assessments, genetic analyses, status evaluations)
- **Data management operations** (quality control, validation, integration)
- **Data products and outputs** (reports, visualizations, management advice)
- **Organizational structures** (management units, conservation units, stock hierarchies)
- **Regulatory and policy frameworks** (Wild Salmon Policy, Precautionary Approach, COSEWIC)

---

## 🎯 COMPETENCY QUESTIONS

**The ontology succeeds when it can answer these specific questions:**

### Priority Classification

- **🔴 REQUIRED**: Core questions the ontology must answer for basic functionality
- **🟡 SHOULD**: Important questions that enhance utility and interoperability  
- **🟢 NICE**: Advanced questions that provide additional value

---

## 🔴 REQUIRED Competency Questions

### Stock Assessment - Population Monitoring

#### R1. What escapement methods were used for specific stocks in a given year?

**Purpose**: Track methodology usage across stocks and time for quality assessment and trend analysis.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?method ?year ?event WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dfo:usesMethod ?method ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate ?year .
  ?stock rdfs:label ?stockLabel .
  FILTER(CONTAINS(?stockLabel, "Sockeye"))
  FILTER(?year = "2022"^^xsd:gYear)
}
ORDER BY ?stock ?method
```

#### R2. Which stocks showed declining trends over the last 5 years?

**Purpose**: Identify stocks requiring management attention and conservation measures.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?year ?count ?trend WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dwc:measurementValue ?count ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate ?year .
  ?stock rdfs:label ?stockLabel .
  FILTER(?year >= "2018"^^xsd:gYear && ?year <= "2023"^^xsd:gYear)
}
ORDER BY ?stock ?year
```

#### R3. What are all the measurement events for a specific Conservation Unit?

**Purpose**: Support CU-level analysis and management decisions.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?cu ?stock ?event ?measurement ?count WHERE {
  ?cu dfo:hasMemberStock ?stock .
  ?measurement dfo:aboutStock ?stock ;
               dwc:measurementValue ?count ;
               dfo:observedDuring ?event .
  ?cu rdfs:label "Fraser Coho CU"@en .
}
ORDER BY ?event
```

#### R4. Which Management Units contain stocks with critical status?

**Purpose**: Identify management units requiring immediate attention and resource allocation.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?mu ?cu ?stock ?status WHERE {
  ?mu dfo:hasMemberCU ?cu .
  ?cu dfo:hasMemberStock ?stock .
  ?stock dfo:hasStockStatusZone dfo:CriticalZone .
  ?mu rdfs:label ?muLabel .
}
ORDER BY ?mu
```

#### R5. What are all the stocks in a specific Management Unit?

**Purpose**: Support MU-level management and reporting.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?mu ?cu ?stock WHERE {
  ?mu dfo:hasMemberCU ?cu .
  ?cu dfo:hasMemberStock ?stock .
  ?mu rdfs:label "Skeena MU"@en .
}
ORDER BY ?cu ?stock
```

### Stock Assessment - Data Integration

#### R6. Which datasets contain measurements for endangered stocks?

**Purpose**: Identify data sources for conservation planning and recovery efforts.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?dataset ?stock ?status WHERE {
  ?dataset dcterms:hasPart ?measurement .
  ?measurement dfo:aboutStock ?stock .
  ?stock dfo:hasCOSEWICStatusCategory dfo:Endangered .
  ?dataset rdfs:label ?datasetLabel .
}
ORDER BY ?dataset
```

#### R7. What is the temporal coverage of escapement data for specific river stocks?

**Purpose**: Assess data completeness and identify temporal gaps.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock (MIN(?year) AS ?earliest) (MAX(?year) AS ?latest) (COUNT(DISTINCT ?year) AS ?years) WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate ?year .
  ?stock rdfs:label ?stockLabel .
  FILTER(CONTAINS(?stockLabel, "Skeena"))
}
GROUP BY ?stock
ORDER BY ?stock
```

### Genetics (GSI) - Sample Analysis

#### R8. What GSI runs analyzed samples from specific river stocks?

**Purpose**: Track genetic analysis coverage and methodology.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?run ?stock ?sample ?date WHERE {
  ?run dfo:analyzesSamples ?sample .
  ?sample dfo:ofStock ?stock .
  ?run dfo:runDate ?date .
  ?stock rdfs:label ?stockLabel .
  FILTER(CONTAINS(?stockLabel, "Skeena"))
}
ORDER BY ?run ?date
```

#### R9. Which Reporting Units map to Conservation Unit X?

**Purpose**: Support genetic-to-management unit mapping for integrated analysis.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?ru ?cu ?matchType WHERE {
  ?ru dfo:ruExactMatch ?cu .
  BIND("exact" AS ?matchType)
  ?cu rdfs:label "Fraser Coho CU"@en .
}
UNION
SELECT ?ru ?cu ?matchType WHERE {
  ?ru dfo:ruCloseMatch ?cu .
  BIND("close" AS ?matchType)
  ?cu rdfs:label "Fraser Coho CU"@en .
}
ORDER BY ?matchType ?ru
```

#### R10. What is the genetic composition of samples collected during Event Y?

**Purpose**: Analyze genetic diversity and stock composition for specific events.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?event ?ru ?proportion ?confidence WHERE {
  ?measurement dfo:derivedFromSample ?sample .
  ?sample dfo:sampledDuring ?event .
  ?measurement dfo:aboutReportingUnit ?ru ;
               dfo:estimateValue ?proportion ;
               dfo:standardError ?confidence .
  ?event rdfs:label "Skeena Survey 2023-001"@en .
}
ORDER BY ?ru
```

### Management and Policy - Conservation Status

#### R11. Which Conservation Units are currently under recovery planning?

**Purpose**: Track recovery planning status and resource allocation.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?cu ?status ?mu WHERE {
  ?cu dfo:hasStockStatusZone dfo:CriticalZone .
  ?mu dfo:hasMemberCU ?cu .
  ?cu rdfs:label ?cuLabel .
  ?mu rdfs:label ?muLabel .
}
ORDER BY ?mu ?cu
```

#### R12. What are the management actions associated with each Management Unit?

**Purpose**: Support management planning and resource allocation.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?mu ?cu ?stock ?status ?action WHERE {
  ?mu dfo:hasMemberCU ?cu .
  ?cu dfo:hasMemberStock ?stock .
  ?stock dfo:hasStockStatusZone ?status .
  ?mu rdfs:label ?muLabel .
  # Note: Management actions would be linked via additional properties
  BIND("Management action based on status" AS ?action)
}
ORDER BY ?mu ?status
```

---

## 🟡 SHOULD Competency Questions

### Stock Assessment - Advanced Analysis

#### S1. Which measurement methods have been used for each stock over time?

**Purpose**: Track methodological evolution and assess consistency.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?method ?year (COUNT(?measurement) AS ?count) WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dfo:usesMethod ?method ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate ?year .
}
GROUP BY ?stock ?method ?year
ORDER BY ?stock ?year ?method
```

#### S2. What are the confidence intervals for abundance estimates?

**Purpose**: Assess estimate reliability and uncertainty.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?measurement ?stock ?estimate ?ciLower ?ciUpper ?confidenceLevel WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dwc:measurementValue ?estimate ;
               dfo:ciLower ?ciLower ;
               dfo:ciUpper ?ciUpper ;
               dfo:confidenceLevel ?confidenceLevel .
}
ORDER BY ?stock ?estimate
```

#### S3. Which stocks have been designated as critical or endangered?

**Purpose**: Support conservation planning and recovery efforts.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?stock ?cosewicStatus ?stockStatus ?cu ?mu WHERE {
  ?stock dfo:hasCOSEWICStatusCategory ?cosewicStatus ;
         dfo:hasStockStatusZone ?stockStatus ;
         dfo:isMemberOfCU ?cu .
  ?cu dfo:isMemberOfSMU ?mu .
  FILTER(?cosewicStatus = dfo:Endangered || ?cosewicStatus = dfo:Threatened || 
         ?stockStatus = dfo:CriticalZone)
}
ORDER BY ?mu ?cu ?stock
```

### Genetics (GSI) - Population Genetics

#### S4. What are the genetic relationships between different Reporting Units?

**Purpose**: Support genetic diversity analysis and conservation planning.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?ru1 ?ru2 ?relationship WHERE {
  ?ru1 dfo:ruExactMatch ?cu .
  ?ru2 dfo:ruExactMatch ?cu .
  ?ru1 rdfs:label ?ru1Label .
  ?ru2 rdfs:label ?ru2Label .
  FILTER(?ru1 != ?ru2)
  BIND("same CU" AS ?relationship)
}
ORDER BY ?ru1 ?ru2
```

#### S5. Which samples show evidence of mixed stock origin?

**Purpose**: Identify samples with uncertain or mixed genetic composition.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?sample ?ru ?proportion WHERE {
  ?measurement dfo:derivedFromSample ?sample ;
               dfo:aboutReportingUnit ?ru ;
               dfo:estimateValue ?proportion .
  FILTER(?proportion < 0.8)  # Less than 80% assignment confidence
}
ORDER BY ?sample ?proportion DESC
```

#### S6. What is the temporal pattern of genetic diversity in a specific stock?

**Purpose**: Monitor genetic diversity trends over time.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?year (COUNT(DISTINCT ?ru) AS ?diversity) WHERE {
  ?measurement dfo:derivedFromSample ?sample .
  ?sample dfo:ofStock ?stock ;
          dfo:sampledDuring ?event .
  ?event dwc:eventDate ?year .
  ?measurement dfo:aboutReportingUnit ?ru .
  ?stock rdfs:label "Skeena Sockeye"@en .
}
GROUP BY ?stock ?year
ORDER BY ?year
```

### Management and Policy - Data Quality

#### S7. What is the data quality assessment for measurements from a specific year?

**Purpose**: Assess data quality and identify areas for improvement.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?year ?method (COUNT(?measurement) AS ?count) (AVG(?confidence) AS ?avgConfidence) WHERE {
  ?measurement dfo:usesMethod ?method ;
               dfo:observedDuring ?event .
  ?event dwc:eventDate ?year .
  OPTIONAL { ?measurement dfo:confidenceLevel ?confidence }
  FILTER(?year = "2022"^^xsd:gYear)
}
GROUP BY ?year ?method
ORDER BY ?method
```

#### S8. Which datasets have been validated and by whom?

**Purpose**: Track data validation status and responsibility.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?dataset ?validator ?date ?status WHERE {
  ?dataset dcterms:creator ?validator .
  ?dataset dcterms:modified ?date .
  ?dataset rdfs:label ?datasetLabel .
  # Note: Validation status would be linked via additional properties
  BIND("validated" AS ?status)
}
ORDER BY ?dataset ?date
```

### Cross-Domain Integration

#### S9. How do genetic Reporting Units align with Conservation Units geographically?

**Purpose**: Support spatial integration of genetic and management data.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?ru ?cu ?matchType ?geographicArea WHERE {
  ?ru dfo:ruExactMatch ?cu .
  BIND("exact" AS ?matchType)
  ?cu rdfs:label ?cuLabel .
  ?ru rdfs:label ?ruLabel .
  # Note: Geographic area would be linked via additional properties
  BIND("Geographic area based on CU" AS ?geographicArea)
}
UNION
SELECT ?ru ?cu ?matchType ?geographicArea WHERE {
  ?ru dfo:ruCloseMatch ?cu .
  BIND("close" AS ?matchType)
  ?cu rdfs:label ?cuLabel .
  ?ru rdfs:label ?ruLabel .
  BIND("Geographic area based on CU" AS ?geographicArea)
}
ORDER BY ?matchType ?cu ?ru
```

#### S10. What are the spatial relationships between Management Units and watersheds?

**Purpose**: Support watershed-level analysis and management.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?mu ?watershed ?cu ?stock WHERE {
  ?mu dfo:hasMemberCU ?cu .
  ?cu dfo:hasMemberStock ?stock .
  ?mu rdfs:label ?muLabel .
  # Note: Watershed relationships would be linked via additional properties
  BIND("Watershed based on MU location" AS ?watershed)
}
ORDER BY ?mu ?watershed
```

---

## 🟢 NICE Competency Questions

### Advanced Analytics

#### N1. What are the long-term trends in both abundance and genetic diversity?

**Purpose**: Support comprehensive trend analysis across multiple data types.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?year ?abundance ?geneticDiversity WHERE {
  # Abundance data
  ?abundanceMeasurement dfo:aboutStock ?stock ;
                        dfo:observedDuring ?abundanceEvent .
  ?abundanceEvent dwc:eventDate ?year .
  ?abundanceMeasurement dwc:measurementValue ?abundance .
  
  # Genetic diversity data
  ?geneticMeasurement dfo:derivedFromSample ?sample .
  ?sample dfo:ofStock ?stock ;
          dfo:sampledDuring ?geneticEvent .
  ?geneticEvent dwc:eventDate ?year .
  ?geneticMeasurement dfo:aboutReportingUnit ?ru .
  
  ?stock rdfs:label "Skeena Sockeye"@en .
}
GROUP BY ?stock ?year ?abundance
ORDER BY ?year
```

#### N2. How have stock boundaries changed over time?

**Purpose**: Track evolution of stock definitions and management units.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?stock ?cu ?mu ?date ?changeType WHERE {
  ?stock dfo:isMemberOfCU ?cu .
  ?cu dfo:isMemberOfSMU ?mu .
  ?stock dcterms:modified ?date .
  # Note: Change tracking would require additional properties
  BIND("boundary change" AS ?changeType)
}
ORDER BY ?stock ?date
```

#### N3. What is the temporal overlap between escapement surveys and genetic sampling?

**Purpose**: Optimize sampling coordination and data integration.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?stock ?year ?surveyDate ?geneticDate ?overlap WHERE {
  # Escapement survey
  ?surveyMeasurement dfo:aboutStock ?stock ;
                     dfo:observedDuring ?surveyEvent .
  ?surveyEvent dwc:eventDate ?surveyDate .
  
  # Genetic sampling
  ?geneticSample dfo:ofStock ?stock ;
                 dfo:sampledDuring ?geneticEvent .
  ?geneticEvent dwc:eventDate ?geneticDate .
  
  BIND(YEAR(?surveyDate) AS ?year)
  BIND(ABS(?surveyDate - ?geneticDate) AS ?overlap)
  FILTER(?overlap < 30)  # Within 30 days
}
ORDER BY ?stock ?year
```

### Quality Assurance

#### N4. Which stocks occur in multiple Management Units?

**Purpose**: Identify stocks requiring coordinated management.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?stock (COUNT(DISTINCT ?mu) AS ?muCount) (GROUP_CONCAT(?muLabel) AS ?mus) WHERE {
  ?stock dfo:isMemberOfCU ?cu .
  ?cu dfo:isMemberOfSMU ?mu .
  ?mu rdfs:label ?muLabel .
}
GROUP BY ?stock
HAVING(?muCount > 1)
ORDER BY ?muCount DESC
```

#### N5. What are the confidence intervals for abundance estimates by method?

**Purpose**: Compare method reliability and uncertainty.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?method (COUNT(?measurement) AS ?count) (AVG(?ciLower) AS ?avgLower) (AVG(?ciUpper) AS ?avgUpper) WHERE {
  ?measurement dfo:usesMethod ?method ;
               dfo:ciLower ?ciLower ;
               dfo:ciUpper ?ciUpper .
}
GROUP BY ?method
ORDER BY ?count DESC
```

#### N6. Which measurement methods have the highest precision for specific stock types?

**Purpose**: Optimize method selection for different stock types.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?stockType ?method (AVG(?precision) AS ?avgPrecision) WHERE {
  ?measurement dfo:aboutStock ?stock ;
               dfo:usesMethod ?method .
  ?stock rdfs:label ?stockLabel .
  BIND(IF(CONTAINS(?stockLabel, "Sockeye"), "Sockeye", 
          IF(CONTAINS(?stockLabel, "Coho"), "Coho", "Other")) AS ?stockType)
  # Note: Precision would be calculated from confidence intervals
  BIND(1.0 AS ?precision)  # Placeholder
}
GROUP BY ?stockType ?method
ORDER BY ?stockType ?avgPrecision DESC
```

### Integration and Interoperability

#### N7. What DFO salmon data is available for integration with external systems?

**Purpose**: Support data sharing and interoperability.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?dataset ?type ?coverage ?format WHERE {
  ?dataset a dfo:Dataset .
  ?dataset dcterms:type ?type .
  ?dataset dcterms:coverage ?coverage .
  ?dataset dcterms:format ?format .
}
ORDER BY ?type ?coverage
```

#### N8. How does DFO data align with Darwin Core standards?

**Purpose**: Ensure compliance with international biodiversity standards.

```sparql
PREFIX dfo: <https://w3id.org/dfo/salmon#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?dfoClass ?dwcClass ?alignment WHERE {
  ?dfoClass rdfs:subClassOf ?dwcClass .
  ?dfoClass rdfs:label ?dfoLabel .
  ?dwcClass rdfs:label ?dwcLabel .
  BIND("subclass alignment" AS ?alignment)
}
ORDER BY ?dfoClass
```

---

## 🎯 Core Objectives

### 1. Data Stewardship & Quality
- Standardize terminology across DFO salmon data systems
- Enable data quality assessment through formal validation rules
- Support data lineage tracking from collection to publication
- Facilitate data governance and compliance with regulatory requirements

### 2. Data Integration & Interoperability
- Integrate data across stock assessment, genetics (GSI/PBT), and management domains
- Enable cross-system queries and data discovery
- Support data sharing with external partners (GBIF, OBIS, international organizations)
- Align with community standards (Darwin Core, OBO Foundry principles)

### 3. Operational Process Mapping
- Document DFO workflows from data collection to management decisions
- Model analytical processes (Kobe plots, run reconstruction, trade-off analyses)
- Track data transformations and processing steps
- Support process automation and workflow management

### 4. Regulatory Compliance & Reporting
- Support Wild Salmon Policy implementation and reporting
- Enable Precautionary Approach framework compliance
- Facilitate COSEWIC status assessments and reporting
- Support Fisheries Act requirements and data transparency

---

## ✅ What This Ontology Models

### Operational Entities (What DFO Does)
- Survey events and measurement protocols
- Stock assessment methodologies
- Genetic analysis workflows
- Data quality control processes
- Management decision frameworks

### Organizational Structures (How DFO is Organized)
- Management Units (MUs)
- Conservation Units (CUs)
- Stock hierarchies and relationships
- Reporting unit structures
- Geographic and administrative boundaries

### Regulatory Frameworks (What DFO Must Follow)
- Wild Salmon Policy requirements
- Precautionary Approach framework
- COSEWIC assessment criteria
- Fisheries Act compliance
- Data transparency obligations

---

## ❌ What This Ontology Does NOT Model

### Biological Domain Concepts
- Salmon life history details
- Ecological relationships
- Habitat characteristics
- Species behavior patterns
- Population genetics (beyond GSI/PBT)

### Instance Data
- Specific survey results
- Actual count values
- Year-specific data
- Location-specific measurements
- Raw data observations

---

## 🎯 Target Users & Use Cases

### 1. Data Stewards
- **Data quality assessment**: "What validation rules apply to escapement measurements?"
- **Data lineage tracking**: "What processes were used to generate this stock assessment?"
- **Data integration**: "How do genetic reporting units map to conservation units?"

### 2. Scientists & Analysts
- **Method documentation**: "What analytical methods were used for 2022 assessments?"
- **Data discovery**: "What escapement data exists for Skeena River stocks?"
- **Process automation**: "What are the standard workflows for run reconstruction?"

### 3. Managers & Policy Makers
- **Compliance reporting**: "What stocks are in critical status zones?"
- **Decision support**: "What reference points apply to this management unit?"
- **Policy implementation**: "How do we track Wild Salmon Policy compliance?"

### 4. External Partners
- **Data sharing**: "What DFO salmon data is available for integration?"
- **Standard compliance**: "How does DFO data align with Darwin Core standards?"
- **Interoperability**: "Can we query DFO data using standard biodiversity protocols?"

---

## 🎯 Success Metrics

The ontology succeeds when it enables:

1. **Data Integration**: Scientists can query across stock assessment, genetics, and management data systems
2. **Process Automation**: Workflows can be automated using formal process definitions
3. **Quality Assurance**: Data quality issues can be automatically detected and reported
4. **Regulatory Compliance**: Management decisions can be traced back to supporting data and processes
5. **External Interoperability**: DFO data can be shared with international partners using standard protocols

---

## 🎯 Key Design Principles

1. **Operational Focus**: Model what DFO does, not what salmon are
2. **Data Stewardship**: Support data quality, lineage, and governance
3. **Process Orientation**: Document workflows and analytical methods
4. **Regulatory Alignment**: Support policy and compliance requirements
5. **Interoperability**: Align with community standards (Darwin Core, OBO Foundry)
6. **Pragmatic Implementation**: Balance formal rigor with practical utility

---

## 🎯 Technical Approach

### Hybrid Modeling Strategy
- **OWL Classes**: For formal relationships and structural entities
- **SKOS Concepts**: For controlled vocabularies (methods, criteria, codes)
- **SHACL Shapes**: For validation rules and automated classification
- **Darwin Core Integration**: For international interoperability

### Core Patterns
- **Measurement Pattern**: Link value+unit+type to stock, method, and event
- **Hierarchy Pattern**: ManagementUnit ▶ ConservationUnit ▶ Stock via transitive relationships
- **Event Pattern**: Survey and estimate events extend Darwin Core Event
- **Automated Classification**: SHACL rules for estimate type assignment

### Quality Assurance
- **Competency-driven**: Every term answers specific research questions
- **OBO Foundry aligned**: Open, interoperable, logically well-formed
- **Darwin Core compatible**: Uses DwC framework for interoperability
- **Well-documented**: Clear labels, definitions, and examples
- **Tested**: Validated with sample data and SPARQL queries

---

## 🎯 Implementation Status

### Current Scope
- **Core Classes**: Stock, ConservationUnit, ManagementUnit, SurveyEvent, EscapementMeasurement
- **Stock Assessment**: EscapementSurveyEvent, SonarCountMeasurement, WeirCountMeasurement, AerialCountMeasurement
- **Genetics (GSI)**: GeneticSample, GSIRun, GSICompositionMeasurement, ReportingUnit, Assay, MarkerPanel, Protocol
- **Methods**: Comprehensive SKOS schemes for enumeration methods, estimate methods, and downgrade criteria

### Development Workflow
1. **Start with competency questions** to guide design (see sections above)
2. **Use ROBOT for quality control**: `robot reason --input dfo-salmon.ttl --reasoner ELK`
3. **Create terms following conventions** in the [DFO Salmon Ontology Conventions Guide](CONVENTIONS.md)
4. **Test with sample data** and competency questions
5. **Submit via GitHub Issues and PRs**

> **📋 Implementation Details**: For detailed guidance on creating terms, naming conventions, design patterns, and quality assurance, see the [DFO Salmon Ontology Conventions Guide](CONVENTIONS.md).

---

## 🎯 This Ontology is Fundamentally About...

**Enabling better data management and operational efficiency within DFO's salmon data ecosystem, not about modeling salmon biology or ecology.**

The DFO Salmon Ontology provides the semantic infrastructure needed to:
- **Integrate** disparate salmon data systems
- **Automate** data quality and classification processes  
- **Support** regulatory compliance and reporting
- **Enable** cross-domain scientific analysis
- **Facilitate** data sharing with international partners

By focusing on operational processes rather than biological concepts, this ontology serves as a practical tool for data stewardship and scientific workflow management within DFO's Pacific salmon program.

---

*Maintainer: Data Stewardship Unit — DFO Pacific Science*  
*License: CC-BY 4.0*