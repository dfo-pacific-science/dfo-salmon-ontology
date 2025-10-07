# DFO Salmon Ontology

**Namespace:** `https://w3id.org/dfo/salmon#` (prefix: `dfo:`)  
**License:** CC-BY 4.0  
**Status:** Draft Work in Progress

The DFO Salmon Ontology is a **data stewardship and operational process ontology** designed to provide a semantic framework for managing, integrating, and stewarding Pacific salmon data across Fisheries and Oceans Canada (DFO).

**📋 For detailed purpose, competency questions, and scope, see [Ontology Purpose and Competency Guide](docs/COMPETENCY_QUESTIONS.md)**

**Goal:** Make salmon data interoperable, discoverable, and analyzable with minimal friction for scientists, data stewards, and managers.

## Repository Structure

This repository follows the [AGENTS.md](AGENTS.md) directory layout for ontology development:

```
/ontology/
  dfo-salmon.ttl            # main schema (OWL + SKOS + SHACL shapes as needed)
  shapes/                   # optional modular SHACL shapes
  imports/                  # pinned external imports (ENVO, QUDT, etc.) if vendored
  templates/                # ROBOT templates (CSV/TSV) for term generation
  sparql/                   # SPARQL queries/tests for competency questions
  examples/                 # minimal instance examples used only for tests/docs
/release/
  changelog.md
  artifacts/                # built artifacts (.owl, .ttl, .json) per release
/tools/
  robot.jar (optional)      # or rely on system-wide ROBOT
/scripts/                   # automation scripts and utilities
/docs/                      # documentation and guides
```

**Rule of thumb:** `/ontology/dfo-salmon.ttl` contains **schema only** (no instance facts, measurements, or survey rows). Instance data examples belong in `/ontology/examples/` and are *not* shipped inside the core ontology file.

---

## Table of Contents

- [Purpose & Competency Questions](docs/COMPETENCY_QUESTIONS.md)
- [Quickstart](#quickstart)
- [Current Scope](#ontology-scope-current)
- [Development Workflow](#contribution-workflow)
- [Conventions Guide](docs/CONVENTIONS.md)
- [Roadmap](#roadmap)
- [Acknowledgments](#acknowledgments)

---

## Technical Overview

- **One file**: `dfo-salmon.ttl` (OWL/Turtle)
- **Hybrid approach**: OWL for formal relationships, SKOS for controlled vocabularies
- **Darwin Core aligned**: Uses DwC classes as top-level framework for interoperability
- **OBO Foundry principles**: Open, interoperable, logically well-formed, scientifically accurate
- **Units**: QUDT/OM IRIs stored as literals (starter convention)
- **Community-aligned**: builds on NCEAS Salmon Ontology, ENVO, and OBO Foundry vocabularies

---

## Quickstart

### For Contributors
1. **Read the [Purpose & Competency Guide](docs/COMPETENCY_QUESTIONS.md)** to understand scope and goals
2. **Read the [Conventions Guide](docs/CONVENTIONS.md)** for detailed modeling guidelines
3. **Use Protégé Desktop** to edit `dfo-salmon.ttl` with OntoGraf for visualization
4. **Use ROBOT** for quality control: `robot reason --input dfo-salmon.ttl --reasoner ELK`
5. **Discuss changes** in GitHub Issues before creating PRs
6. **Follow OBO practices**: Use competency questions, design patterns, and quality checklists

### For Users
1. **Browse terms** using Protégé or online ontology browsers
2. **Query data** using SPARQL with the ontology as a schema
3. **Integrate** with Darwin Core-compatible systems for interoperability

---

## Development Workflow

- **Single source of truth**: One ontology file (`dfo-salmon.ttl`) on GitHub
- **OBO-style workflow**: Use ROBOT for quality control and release management
- **GitHub-based collaboration**: All changes via Pull Requests with Issues for discussion
- **Quality first**: Use competency questions and design patterns to guide development
- **Before creating terms**: Search existing terms and check competency questions
- **Document everything**: Always include `rdfs:comment` and `dcterms:source`
- **Test with data**: Validate terms with sample data and SPARQL queries

**For detailed modeling conventions, see [DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md).**

**For agent-specific development guidelines, see [AGENTS.md](AGENTS.md).**

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
- **For detailed conventions**: See [DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md)

---

## Roadmap

### Phase 1: Foundation (Current)
- ✅ Core class and property definitions
- ✅ Basic measurement patterns
- ✅ Stock hierarchy implementation
- ✅ Darwin Core alignment
- ✅ Competency questions with SPARQL queries
- ✅ Repository structure conforming to AGENTS.md

### Phase 2: Expansion
- Fill missing `rdfs:comment` definitions
- Add genetic analysis workflows
- Implement advanced measurement types
- External vocabulary integration
- Quality control patterns

### Phase 3: Integration
- NCEAS Salmon Ontology alignment
- International standard compliance
- Advanced querying capabilities
- Data validation tools

### Phase 4: Policy and Integration
- Policy benchmarks and reference points
- Integration with NCEAS Salmon Ontology
- Advanced querying and analytics
- Publish docs via pyLODE/Widoco
- Register W3ID redirects

---

## Acknowledgments

This ontology builds on:

- Darwin Core / GBIF (conceptual backbone)
- NCEAS Salmon Ontology, ENVO, and OBO Foundry ontologies
- Input from DFO biologists, data stewards, and the RDA Salmon Ontology WG
- Guidance from the Salmon Data Stewardship community
