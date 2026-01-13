# DFO Salmon Ontology — Onboarding Guide (Fundamentals)

Purpose

- Provide an approachable introduction to the ontology: why it exists, how it differs from a knowledge graph or database, and the basic modeling approach.
- Help new contributors gain the necessary background before using the Conventions Guide.

Standards

- OWL 2 DL compliance (strict)
- SKOS 1.2 and RDF 1.2 support

1. What Is Knowledge Modeling?

Knowledge modeling (ontology engineering) creates formal representations of domain knowledge that both humans and machines can understand. It defines a shared vocabulary and rules for how concepts relate.

Why conventions matter:

- Consistent terms and structure across contributors
- Automated validation and processing
- Interoperability across systems
- Future maintainability and extensibility

2. Ontology vs Knowledge Graph vs Graph Database

Ontology (Schema)

- Formal specification of concepts, relationships, and rules
- Contains classes, properties, SKOS vocabularies, axioms, constraints
- Purpose: define the vocabulary and grammar for describing data
- Example: `EscapementSurveyEvent` class, `usesEnumerationMethod` property, `SnorkelSurvey` SKOS concept
- File: `dfo-salmon.ttl` (schema only; no instance data)

Knowledge Graph (Data)

- Interconnected instances conforming to the ontology
- Contains specific facts, measurements, events
- Purpose: store actual data using the ontology’s vocabulary
- Example: `SkeenaSnorkel2022_001` survey event with measurements
- Files: separate data files (e.g., `survey-data-2022.ttl`)

Graph Database (Storage)

- Database optimized for graph structures and queries
- Stores schema + data for efficient traversal
- Examples: Jena TDB, Neptune, Blazegraph

Why this separation matters

1) Clean schema; 2) Independent versioning; 3) Reuse across datasets; 4) Easier maintenance/validation; 5) Interoperability

3. Why This Ontology?

The DFO Salmon Ontology provides a domain-fit semantic layer for Pacific salmon, enabling integration across stock assessment, genetics, and management, and supporting evidence transparency.

See: [README](../README.md) for full purpose, objectives, and target users.

We build on:

- Darwin Core and the Darwin Core Conceptual Model (DwC-CM)
- NCEAS Salmon Ontology
- Standard vocabularies: QUDT (units), ENVO (environments), GBIF Backbone (taxa)

**Darwin Core Conceptual Model (DwC-CM):** The Darwin Core Conceptual Model provides a semantic layer for Darwin Core that addresses long-standing ambiguities. DFO Salmon Ontology implements DwC-CM patterns:

- **Occurrence redefined:** Now explicitly "a state of an Organism in an Event" (resolves ambiguity)
- **Assertion class:** Modern replacement for MeasurementOrFact with clearer semantics
- **Structured relationships:** Better domain/range constraints and property usage guidelines

DFO implements DwC-CM patterns, using `dwc:Assertion` for measurement classes and `dwc:Occurrence` for individual organism observations.

4. Basic Modeling Approach

- OWL 2 DL for domain classes and properties
- SKOS 1.2 for controlled vocabularies/code lists
- RDF 1.2 Turtle (.ttl) for representation
- Start simple; modularize later as needed
- **DwC-CM implementation:** Uses modern Darwin Core patterns for improved interoperability

**DwC-CM Usage Patterns:**

- **For Measurements:** Use `dwc:Assertion` as superclass for all measurement classes
- **For Events:** Use `dwc:Event` for survey events; use `dwc:parentEventID` for hierarchies
- **For Organisms:** Use `dwc:Organism` for stocks; use `dwc:Occurrence` for individual observations (when applicable)
- **For Samples:** Use `dwc:MaterialEntity` for physical samples

OBO alignment

- Follow OBO Foundry principles where practical
- Use RO for relations where possible
- Use ROBOT for QC, conversion, release

Next Steps

- Continue in docs/CONVENTIONS.md for “how we do things” (patterns, QA, tooling)
- Consult ADRs for rationale behind major decisions
