# DFO Salmon Ontology

**Namespace:** `https://w3id.org/dfo/salmon#` (prefix: `dfo:`)  
**License:** CC-BY 4.0  
**Status:** Draft Work in Progress. 

The DFO Salmon Ontology is an **OWL ontology** for salmon science data at Fisheries and Oceans Canada (DFO). It aligns with the Darwin Core (DwC) conceptual layer where helpful and adds DFO-specific concepts for stock assessment and genetics.  
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
- **No SKOS, no SHACL** for now; focus on **classes + properties**.
- **Reuse before invent**: align to DwC (`dwc:Event`, `dwc:MaterialSample`, `dwc:MeasurementOrFact`) via `rdfs:subClassOf`, but don’t import DwC yet.
- **Units**: QUDT/OM **IRIs stored as literals** (starter convention).
- **Community-aligned**: builds on NCEAS Salmon Ontology, ENVO, and OBO Foundry vocabularies.

---

## Quickstart (WebProtégé & OntoGraf)

1. Create a new project in **Protégé Desktop** and upload `dfo-salmon.ttl`.
2. Use **OntoGraf** to explore class/property relationships interactively.
3. Export the updated `.ttl` from Protégé.
4. Discuss proposed edits in **GitHub Issues**.
5. **Approved edits** become PRs applied directly to `dfo-salmon.ttl` in GitHub.
6. **IRIs are permanent**: update labels/comments, not IRIs.

---

## Workflow & Editing Guidelines

- We are maintaining **one ontology file** in OWL format (`.ttl`) on GitHub as the single source of truth.
- All editing is done via **GitHub Pull Requests (PRs)**.
- Use **WebProtégé + OntoGraf** to visualize and verify connections.
- **Before creating a new term**: search WebProtégé to ensure it doesn’t already exist.
- **Be consistent**: follow the conventions below.
- **Keep it simple**: avoid complex restrictions (e.g., `someValuesFrom`) unless agreed.
- **Document everything**: always include `rdfs:comment` and, if possible, a `dcterms:source`.
- **Discuss major changes**: use GitHub Issues for uncertain modeling decisions.

---

## Modeling Approach

- **OWL-only**: all terms are `owl:Class`, `owl:ObjectProperty`, or `owl:DatatypeProperty`.
- **Human + machine friendly**: every term has a label + definition.
- **Domain fit**: initial focus on stock assessment and genetics; expand iteratively.
- **Minimal constraints**: use domains/ranges only when they improve data quality.
- **Visualization**: OntoGraf in Protégé helps verify relationships and explain the ontology. WebVOWL is also handy for this.

---

## Conventions (Updated)

### Classes

Required:

- `a owl:Class`
- `rdfs:label "Human Name"@en`
- `rdfs:comment "1–2 sentence definition."@en`
- `rdfs:isDefinedBy <https://w3id.org/dfo/salmon>`

Optional:

- `dcterms:source <URL or citation>`
- `dcterms:description "Example usage."@en`
- `oboInOwl:hasExactSynonym` (if relevant)

### Object Properties

- `a owl:ObjectProperty`
- `rdfs:label` + `rdfs:comment`
- Domain/Range only when it helps data quality (avoid over-constraining early)
- **Naming**: lowerCamelCase from subject → object (e.g., `aboutStock`, `usesMethod`)
- Always add `rdfs:isDefinedBy`

### Datatype Properties

- `a owl:DatatypeProperty`
- `rdfs:label` + `rdfs:comment`
- Range must be an explicit XSD type (`xsd:string`, `xsd:decimal`, `xsd:date`, etc.)
- Units & IRIs as **literals** (starter convention)
- Always add `rdfs:isDefinedBy`

---

## Hierarchy & Relationships

- **Subclassing required**: If a new class is a type of an existing one, assert `rdfs:subClassOf`.  
  _Example_: `EscapementSurveyEvent ⊑ SurveyEvent`.
- **Equivalence (optional)**: Use `owl:equivalentClass` only when two classes are truly identical.
- **Disjointness (optional)**: Use `owl:disjointWith` or `owl:AllDisjointClasses` if sibling classes must not overlap.  
  _Example_: `AutomatedCountingMethods` vs `ExpertOpinion`.
- **Part–whole (optional)**: Use `hasPart` / `partOf` sparingly; for management hierarchies prefer the **membership** pattern below.
- **No SKOS broader/narrower** for taxonomies in v0.1; use OWL subclassing.

---

## Membership / Roll-up Pattern (MU ▶ CU ▶ Stock)

We explicitly model that **Management Units contain Conservation Units**, and **Conservation Units contain Stocks**.

**Generic transitive membership**

- `dfo:hasMember` (Transitive) and inverse `dfo:isMemberOf`.

**Tier-specific subproperties**

- MU ▶ CU: `dfo:hasMemberCU` / `dfo:isMemberOfMU`
- CU ▶ Stock: `dfo:hasMemberStock` / `dfo:isMemberOfCU`

**Why this pattern**

- Human-readable, type-safe properties per tier.
- Transitivity gives automatic roll-ups: MU `hasMemberCU` CU & CU `hasMemberStock` Stock ⇒ MU `hasMember` Stock (inferred).

**Deprecation note**

- Older `hasConservationUnit` (Stock→CU) is **deprecated**; prefer `isMemberOfCU` for clarity.

**Governance to decide**

- Can a **CU belong to multiple MUs**? If NO, later mark `isMemberOfMU` as `owl:FunctionalProperty`.
- Can a **Stock belong to multiple CUs**? If NO, later mark `isMemberOfCU` as `owl:FunctionalProperty`.
- Should **MU, CU, Stock** be declared **disjoint**? (recommended once stable)

**Query ideas**

- “All Stocks in MU X” → follow transitive `hasMember`.
- “All CUs in MU X” → `hasMemberCU`.
- “MU(s) for Stock Y” → chain `isMemberOf`.

---

## Measurement & GSI Conventions

- **EscapementMeasurement** must connect to:
  - `aboutStock` (which stock it describes)
  - `observedDuring` (which SurveyEvent)
  - `usesMethod` (family in `EscapementMethod`)
- **Units**:
  - Counts: store QUDT unit IRI in `countUnitIRI` (e.g., `http://qudt.org/vocab/unit/Each`).
  - Composition estimates: adopt **one** convention and stick to it:
    - **Fraction** 0–1 with `estimateUnitIRI = http://qudt.org/vocab/unit/One`, **or**
    - **Percent** 0–100 with `estimateUnitIRI = http://qudt.org/vocab/unit/Percent`.
  - Document the choice in this README; later enforce with SHACL.
- **GSI specifics**:
  - `GSICompositionMeasurement` is RU-centric; link via `aboutReportingUnit`.
  - Maintain RU↔CU mapping policy; use `ruExactMatch` / `ruCloseMatch` with documented criteria.
  - Future: property chain (e.g., `Sample ofStock` + `Stock isMemberOfCU` ⇒ `Sample ofConservationUnit`).

---

## External Alignments (Pragmatic)

- Store external references as **literal IRIs** for now (e.g., `taxonIRI`, QUDT unit IRIs).
- Plan a later move to **object links** via imports (GBIF, ENVO, OBI, QUDT) when stable.

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
- **External alignments**: literal IRIs for now (e.g., GBIF taxon → `dfo:taxonIRI`)
- **Units**: QUDT IRIs as literals in `…UnitIRI` properties
- **Versioning**
  - Maintain `owl:versionInfo` and `owl:versionIRI` in ontology header
  - Tag GitHub releases (e.g., `v0.1.0`)
  - Archive via Zenodo for DOI

---

## Contribution Workflow

- Propose changes in **GitHub Issues**.
- Discuss/agree on definitions before structural edits.
- Keep edits **atomic** (one conceptual change per PR).
- Do not rename IRIs; if refactoring, **deprecate** and add `rdfs:seeAlso`.

**Definition quality checklist**

- One clear concept per term
- Human-readable label and comment
- Example/source if contentious
- Avoid over-constraining with domains/ranges

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
