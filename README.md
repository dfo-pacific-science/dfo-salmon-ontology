# DFO Salmon Ontology

**Namespace:** `https://w3id.org/dfo/salmon#` (prefix: `dfo:`)  
**License:** CC-BY 4.0  
**Status:** Draft Work in Progress. 

The DFO Salmon Ontology is an ** OWL ontology** for salmon data at Fisheries and Oceans Canada (DFO). It's main focus is on describing operations, data, data flows, data analytics, and reporting in support of the *Fisheries Act* and the Wild Salmon Policy for the purposes of data quality assessment, data integration, and data stewardship generally. It broadly reflects the functional, operational, and organizational entities and relationships of salmon data collection through to publication. It's modularized into functional vertical domains including escapement, fisheries management, habitat, an enhancement as well as cross cutting domains such as genetics, policy, and management.

It aligns with the Darwin Core (DwC) Conceptual Model layer where helpful and adds DFO-specific concepts for stock assessment and genetics.  
**Goal:** Make salmon data interoperable, discoverable, and analyzable with minimal friction for scientists, data stewards, and managers.

---

## Table of Contents

- Overview
- Quickstart (WebProtégé & OntoGraf)
- Workflow & Editing Guidelines
- Modeling Approach
- Conventions (Updated)
- Hierarchy & Relationships
- Membership / Roll-up Pattern (MU ▶ CU ▶ Stock)
- Measurement & GSI Conventions
- External Alignments (Pragmatic)
- Ontology Scope
- IRI & Versioning Policy
- Contribution Workflow
- Roadmap
- Acknowledgments

---

## Overview

- **One file**: `dfo-salmon.ttl` (OWL/Turtle).
- **OWL + SKOS**: OWL for formal relationships, SKOS for controlled vocabularies.
- **Darwin Core aligned**: Uses DwC classes as top-level framework for interoperability.
- **OBO Foundry principles**: Open, interoperable, logically well-formed, scientifically accurate.
- **Units**: QUDT/OM **IRIs stored as literals** (starter convention).
- **Community-aligned**: builds on NCEAS Salmon Ontology, ENVO, and OBO Foundry vocabularies.

---

## Quickstart

### For Contributors
1. **Read the [Conventions Guide](DFO%20Salmon%20Ontology%20Conventions.md)** for detailed modeling guidelines
2. **Use Protégé Desktop** to edit `dfo-salmon.ttl` with OntoGraf for visualization
3. **Use ROBOT** for quality control: `robot reason --input dfo-salmon.ttl --reasoner ELK`
4. **Discuss changes** in GitHub Issues before creating PRs
5. **Follow OBO practices**: Use competency questions, design patterns, and quality checklists

### For Users
1. **Browse terms** using Protégé or online ontology browsers
2. **Query data** using SPARQL with the ontology as a schema
3. **Integrate** with Darwin Core-compatible systems for interoperability

---

## Workflow & Editing Guidelines

- **Single source of truth**: One ontology file (`dfo-salmon.ttl`) on GitHub
- **OBO-style workflow**: Use ROBOT for quality control and release management
- **GitHub-based collaboration**: All changes via Pull Requests with Issues for discussion
- **Quality first**: Use competency questions and design patterns to guide development
- **Before creating terms**: Search existing terms and check competency questions
- **Document everything**: Always include `rdfs:comment` and `dcterms:source`
- **Test with data**: Validate terms with sample data and SPARQL queries

---

## Modeling Approach

- **OWL + SKOS**: OWL for formal relationships, SKOS for controlled vocabularies
- **Darwin Core framework**: Uses DwC classes as top-level for international interoperability
- **OBO Foundry aligned**: Follows OBO principles for open, interoperable ontologies
- **Competency-driven**: Every term answers specific research questions
- **Quality assured**: Uses ROBOT validation and systematic quality checklists
- **Human + machine friendly**: Clear labels, definitions, and examples

---

## Conventions

**For detailed modeling conventions, see [DFO Salmon Ontology Conventions Guide](DFO%20Salmon%20Ontology%20Conventions.md).**

**Quick reference:**
- All terms need: `rdfs:label`, `rdfs:comment`, `rdfs:isDefinedBy`
- Use lowerCamelCase for property names (e.g., `aboutStock`, `usesMethod`)
- Store QUDT unit IRIs as literals in `…UnitIRI` properties
- Follow the membership pattern for MU ▶ CU ▶ Stock relationships

---

## Key Modeling Patterns

**For detailed modeling conventions, see [DFO Salmon Ontology Conventions Guide](DFO%20Salmon%20Ontology%20Conventions.md).**

**Key patterns:**
- **Membership hierarchy**: SMU ▶ CU ▶ Population with transitive `hasMember` relationships
- **Measurement requirements**: EscapementMeasurements must link to stock, event, and method
- **Darwin Core integration**: Use DwC classes and predicates where appropriate
- **Quality validation**: Use ROBOT and competency questions for validation

---

## Ontology Scope (Current)

**Core Classes**

- `dfo:Stock`, `dfo:ConservationUnit`, `dfo:ManagementUnit`
- `dfo:SurveyEvent` (⊑ `dwc:Event`)
- `dfo:EscapementMeasurement` (⊑ `dwc:MeasurementOrFact`)
- `dfo:Indicator`, `dfo:Dataset` (⊑ `schema:Dataset`)

**Stock Assessment Specializations**

- `dfo:EscapementSurveyEvent`
- `dfo:SonarCountMeasurement`, `dfo:WeirCountMeasurement`, `dfo:AerialCountMeasurement`
- `dfo:EscapementMethod` + subclasses (`AreaUnderTheCurve`, `AutomatedCountingMethods`, `CalibratedTimeSeries`, `ExpansionMethods`, `ExpertOpinion`, `FixedStationCountAnalysis`, `MarkRecaptureAnalysis`, `MathematicalOperations`, `PeakCountAnalysis`, `UnknownMethod`)

**Genetics (GSI)**

- Classes: `dfo:GeneticSample`, `dfo:GSIRun`, `dfo:GSICompositionMeasurement`, `dfo:ReportingUnit`, `dfo:Assay`, `dfo:MarkerPanel`, `dfo:Protocol`
- Object properties: `sampledDuring`, `ofStock`, `usedAssay`, `usedMarkerPanel`, `usedProtocol`, `analyzesSamples`, `producedMeasurement`, `derivedFromSample`, `aboutReportingUnit`, `hasReportingUnit`, `ruExactMatch`, `ruCloseMatch`
- Datatypes: `estimateValue`, `estimateUnitIRI`, `standardError`, `ciLower`, `ciUpper`, `confidenceLevel`, `methodName`, `baselineName`, `runDate`, `runNote`, `sampleID`, `tissueType`, `collectionMethod`

---

## IRI & Versioning Policy

- **Base IRI**: `https://w3id.org/dfo/salmon#`
- **Instances**: mint under same base (e.g., `…#Stock/SkeenaSockeye`)
- **Versioning**: Tag GitHub releases, maintain version info in ontology header
- **For detailed conventions**: See [DFO Salmon Ontology Conventions Guide](DFO%20Salmon%20Ontology%20Conventions.md)

---

## Contribution Workflow

### OBO-Style Development Process
1. **Start with competency questions** to guide design
2. **Use ROBOT for quality control**:
   ```bash
   robot reason --input dfo-salmon.ttl --reasoner ELK
   robot validate --input dfo-salmon.ttl
   ```
3. **Create terms following conventions** in the [Conventions Guide](DFO%20Salmon%20Ontology%20Conventions.md)
4. **Test with sample data** and competency questions
5. **Submit via GitHub Issues and PRs**

### Quality Standards
- **Competency-driven**: Every term answers specific research questions
- **OBO Foundry aligned**: Open, interoperable, logically well-formed
- **Darwin Core compatible**: Uses DwC framework for interoperability
- **Well-documented**: Clear labels, definitions, and examples
- **Tested**: Validated with sample data and SPARQL queries

---

## Roadmap

- Fill missing `rdfs:comment` definitions.
- Add minimal individuals for examples (docs/training).
- Consider SHACL validation later (ranges, required fields).
- Decide when to replace literal IRIs with object links (GBIF, QUDT).
- Publish docs via pyLODE/Widoco.
- Register W3ID redirects.

---

## Acknowledgments

This ontology builds on:

- Darwin Core / GBIF (conceptual backbone)
- NCEAS Salmon Ontology, ENVO, and OBO Foundry ontologies
- Input from DFO biologists, data stewards, and the RDA Salmon Ontology WG
- Guidance from the Salmon Data Stewardship community
