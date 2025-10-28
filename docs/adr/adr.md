# Architecture Decision Records (ADR)

This document records the key architectural decisions made for the DFO Salmon Ontology project, following the [ADR format](https://adr.github.io/).

## Table of Contents

- [ADR-001: Hybrid OWL+SKOS Modeling Approach](#adr-001-hybrid-owlskos-modeling-approach)
- [ADR-002: Darwin Core Integration Strategy](#adr-002-darwin-core-integration-strategy)
- [ADR-003: Single File vs Modular Ontology Structure](#adr-003-single-file-vs-modular-ontology-structure)
- [ADR-004: Schema vs Data Separation](#adr-004-schema-vs-data-separation)
- [ADR-005: SHACL for Automated Classification](#adr-005-shacl-for-automated-classification)
- [ADR-006: IRI and Versioning Policy](#adr-006-iri-and-versioning-policy)
- [ADR-007: External Vocabulary Alignment Strategy](#adr-007-external-vocabulary-alignment-strategy)
- [ADR-008: ROBOT Toolchain Selection](#adr-008-robot-toolchain-selection)
- [ADR-009: Quality Assurance Framework](#adr-009-quality-assurance-framework)
- [ADR-010: Competency-Driven Development](#adr-010-competency-driven-development)

---

## ADR-001: Hybrid OWL+SKOS Modeling Approach

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to model both formal relationships (OWL) and controlled vocabularies (SKOS) for automated classification systems.

### Decision

We will use a hybrid approach combining OWL and SKOS:

- **OWL classes** for formal relationships and structural entities (events, measurements, stocks)
- **SKOS concepts** for controlled vocabularies (methods, criteria, status categories)
- **SHACL shapes** for validation rules and automated classification

### Rationale

1. **Operational Focus**: The ontology models operational processes, not biological concepts
2. **Automated Classification**: Need both controlled vocabularies (methods) and rich data modeling (events with metadata)
3. **Separation of Concerns**: Methods as vocabulary terms, events as data carriers
4. **Industry Standards**: Aligns with OBO Foundry principles and community practices

### Consequences

**Positive:**

- Supports manual estimate type assignment (Hyatt 1997 framework) - automated classification deferred to post-MVP
- Supports both human-readable vocabularies and machine-processable relationships
- Aligns with existing salmon data management practices
- Facilitates data quality validation through SHACL rules

**Negative:**

- Increased complexity compared to pure OWL approach
- Requires understanding of both OWL and SKOS modeling patterns
- Potential confusion between OWL classes and SKOS concepts

### Implementation

- SKOS schemes for enumeration methods, estimate methods, downgrade criteria, and status categories
- OWL classes for survey events, measurements, and organizational structures
- SHACL shapes for method-specific validation and automated type assignment

---

## ADR-002: Schema vs Data Separation

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to maintain clean separation between ontology schema and instance data.

### Decision

We will strictly separate schema and data:

- **Ontology file**: Contains only schema elements (classes, properties, SKOS concepts)
- **Instance data**: Stored in separate files or systems
- **Examples**: Minimal test data in `ontology/examples/` for validation only

### Rationale

1. **Maintainability**: Schema changes independently of data updates
2. **Reusability**: Same schema can be used for multiple datasets
3. **Versioning**: Schema and data can have different versioning cycles
4. **Interoperability**: Other systems can import just the schema

### Consequences

**Positive:**

- Clean, focused ontology file
- Easier schema validation and maintenance
- Better separation of concerns
- Enables schema reuse across different datasets

**Negative:**

- Requires discipline to maintain separation
- May need additional tooling for data management
- Potential confusion about where to put certain elements

### Implementation

- `ontology/dfo-salmon.ttl` contains only schema elements
- `ontology/examples/` contains minimal test data for validation
- Instance data stored in separate RDF files or graph databases
- SHACL shapes validate data structure without containing data

---

## ADR-005: IRI and Versioning Policy

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for stable, persistent identifiers and clear versioning strategy.

### Decision

We will use:

- **Base IRI**: `https://w3id.org/dfo/salmon#`
- **Versioning**: Semantic versioning with `owl:versionInfo` and `owl:versionIRI`
- **Stability**: No breaking changes to existing IRIs

### Rationale

1. **Persistence**: W3ID provides stable, resolvable identifiers
2. **Versioning**: Clear versioning enables proper dependency management
3. **Stability**: Prevents breaking changes for existing users
4. **Standards Compliance**: Follows OBO Foundry and W3C best practices

### Consequences

**Positive:**

- Stable identifiers for long-term use
- Clear versioning enables proper dependency management
- W3ID provides reliable resolution
- Follows established community practices

**Negative:**

- Requires careful management of versioning
- W3ID setup and maintenance overhead
- Need to maintain backward compatibility

### Implementation

- Base IRI: `https://w3id.org/dfo/salmon#`
- Version IRIs: `https://w3id.org/dfo/salmon/0.2.0`
- GitHub releases with semantic versioning
- W3ID redirect configuration for stable resolution

---

## ADR-007: ROBOT Toolchain Selection

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for robust ontology development and validation toolchain.

### Decision

We will use ROBOT (ROBOT is an OWL Tool) for:

- Ontology validation and reasoning
- Format conversion (TTL, OWL, JSON)
- Quality control and metrics
- Release management

### Rationale

1. **OBO Foundry Standard**: ROBOT is the standard tool for OBO ontologies
2. **Comprehensive Functionality**: Provides all necessary ontology operations
3. **Community Support**: Well-maintained with active community
4. **Integration**: Works well with existing OBO workflows

### Consequences

**Positive:**

- Industry-standard tooling
- Comprehensive ontology operations
- Active community support
- Integrates well with OBO workflows

**Negative:**

- Requires Java installation
- Learning curve for new users
- Doesn't check SKOS concepts or schemes. In fact SKOS confuses ROBOT

### Implementation

- ROBOT 1.8.3 installed in `tools/robot.jar`
- Batch scripts for common operations
- Integration with CI/CD pipeline
- Documentation and training materials

---


