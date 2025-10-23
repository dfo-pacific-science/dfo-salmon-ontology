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

## ADR-002: Darwin Core Integration Strategy

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for international interoperability with biodiversity data systems (GBIF, OBIS).

### Decision

We will align with Darwin Core (DwC) as the top-level framework:
- Extend DwC classes (`dwc:Event`, `dwc:Organism`, `dwc:MeasurementOrFact`)
- Use DwC predicates where applicable (`dwc:samplingProtocol`, `dwc:eventDate`)
- Maintain DFO-specific extensions for salmon management concepts

### Rationale

1. **International Interoperability**: Enables data sharing with GBIF, OBIS, and other biodiversity platforms
2. **Community Standards**: Darwin Core is widely adopted in biodiversity informatics
3. **Future-Proofing**: Builds on stable, well-tested standards
4. **Data Discovery**: Makes DFO salmon data discoverable globally

### Consequences

**Positive:**
- Enables international data sharing and discovery
- Leverages existing DwC infrastructure and tools
- Provides standard predicates for common relationships
- Supports integration with global biodiversity databases

**Negative:**
- Some DwC concepts may not perfectly fit salmon management needs
- Requires careful mapping of DFO-specific concepts to DwC framework
- Potential tension between DwC simplicity and DFO complexity requirements

### Implementation

- DFO classes extend appropriate DwC classes via `rdfs:subClassOf`
- Use DwC predicates for standard relationships (dates, protocols, measurements)
- Maintain DFO-specific properties for domain-specific concepts

---

## ADR-003: Single File vs Modular Ontology Structure

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to balance simplicity with maintainability for ontology development.

### Decision

We will start with a single ontology file (`dfo-salmon.ttl`) with potential for future modularization:
- **Current**: One file containing all schema elements
- **Future**: May split into modules (stock, genetics, governance) as complexity grows
- **Shapes**: Separate SHACL shapes in `ontology/shapes/` directory

### Rationale

1. **Simplicity First**: Easier for contributors to understand and edit
2. **OBO Foundry Alignment**: Follows OBO best practices for initial development
3. **Gradual Complexity**: Can modularize when the ontology grows large
4. **Tool Compatibility**: Single file works well with existing ontology tools

### Consequences

**Positive:**
- Simpler development and maintenance initially
- Easier for new contributors to understand
- Better tool support and validation
- Follows established OBO Foundry patterns

**Negative:**
- May become unwieldy as ontology grows
- Potential for circular dependencies
- Harder to reuse specific modules independently

### Implementation

- Single `ontology/dfo-salmon.ttl` file for all schema elements
- Separate `ontology/shapes/dfo-salmon-shapes.ttl` for SHACL validation
- Clear organization within the single file using comment headers
- Future modularization plan documented in roadmap

---

## ADR-004: Schema vs Data Separation

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

## ADR-005: SHACL for Automated Classification

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for automated estimate type assignment based on survey metadata.

### Decision

We will use SHACL (Shapes Constraint Language) for:
- Data validation and quality control
- Manual estimate type assignment (Hyatt 1997 framework) - automated classification deferred to post-MVP
- Method-specific threshold enforcement

### Rationale

1. **Automated Classification**: Enables rule-based estimate type assignment
2. **Data Quality**: Validates survey metadata against method requirements
3. **Separation of Concerns**: Keeps validation logic separate from ontology schema
4. **Industry Standard**: SHACL is a W3C standard for data validation

### Consequences

**Positive:**
- Enables automated quality assessment
- Supports method-specific validation rules
- Separates validation logic from schema definition
- Provides clear error messages for data quality issues

**Negative:**
- Additional complexity in ontology development
- Requires understanding of SHACL syntax and patterns
- May need specialized tooling for SHACL validation

### Implementation

- SHACL shapes in `ontology/shapes/dfo-salmon-shapes.ttl`
- Validation rules for survey events and measurements
- Automated type assignment rules based on method-specific thresholds
- Integration with data entry systems for real-time validation

---

## ADR-006: IRI and Versioning Policy

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

## ADR-007: External Vocabulary Alignment Strategy

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to align with existing vocabularies while maintaining DFO-specific requirements.

### Decision

We will align with external vocabularies using:
- **Literal IRIs**: Store external vocabulary IRIs as literals (e.g., QUDT units)
- **Object Properties**: Future migration to object properties when appropriate
- **Cross-references**: Use `oboInOwl:hasDbXref` for external alignments

### Rationale

1. **Pragmatic Implementation**: Literal IRIs avoid complex import dependencies
2. **Future Flexibility**: Can migrate to object properties later
3. **Standards Alignment**: Leverages existing, well-maintained vocabularies
4. **Interoperability**: Enables data sharing with other systems

### Consequences

**Positive:**
- Avoids complex import dependencies
- Enables alignment with external standards
- Provides flexibility for future evolution
- Supports interoperability with other systems

**Negative:**
- Less formal than object property alignments
- May need migration strategy for future versions
- Requires documentation of alignment choices

### Implementation

- QUDT unit IRIs stored as literals in `countUnitIRI` properties
- GBIF taxon IRIs stored as literals in `taxonIRI` properties
- Cross-references to external vocabularies via `oboInOwl:hasDbXref`
- Documentation of alignment choices in README

---

## ADR-008: ROBOT Toolchain Selection

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
- Command-line interface may be intimidating

### Implementation

- ROBOT 1.8.3 installed in `tools/robot.jar`
- Batch scripts for common operations
- Integration with CI/CD pipeline
- Documentation and training materials

---

## ADR-009: Quality Assurance Framework

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for systematic quality control and validation processes.

### Decision

We will implement a multi-layered quality assurance framework:
- **ROBOT validation**: Logical consistency and basic quality checks
- **SHACL validation**: Data structure and business rule validation
- **SPARQL testing**: Competency question validation
- **Community review**: Domain expert and ontology modeler review

### Rationale

1. **Quality Assurance**: Ensures ontology meets scientific and technical standards
2. **Automated Validation**: Catches errors early in development
3. **Community Input**: Leverages domain expertise for accuracy
4. **Continuous Improvement**: Enables iterative quality enhancement

### Consequences

**Positive:**
- High-quality ontology output
- Early error detection and correction
- Community-driven quality improvement
- Systematic validation processes

**Negative:**
- Additional development overhead
- Requires expertise in multiple validation approaches
- May slow initial development

### Implementation

- ROBOT validation in CI/CD pipeline
- SHACL validation for data quality
- SPARQL tests for competency questions
- Two-reviewer requirement for all changes

---

## ADR-010: Competency-Driven Development

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to ensure ontology serves real-world research and management needs.

### Decision

We will use competency questions to drive ontology development:
- **Competency Questions**: Define what the ontology should be able to answer
- **Design Guidance**: Use questions to identify required terms and relationships
- **Validation**: Test ontology against competency questions
- **Documentation**: Maintain clear mapping between questions and ontology elements

### Rationale

1. **User-Centered Design**: Ensures ontology serves real user needs
2. **Validation Framework**: Provides concrete criteria for success
3. **Design Guidance**: Helps identify missing terms and relationships
4. **Community Alignment**: Ensures all stakeholders understand ontology purpose

### Consequences

**Positive:**
- User-focused ontology development
- Clear success criteria
- Systematic validation approach
- Community alignment on purpose

**Negative:**
- Requires upfront work to define questions
- May limit ontology scope initially
- Requires ongoing maintenance of question mappings

### Implementation

- Competency questions documented in `docs/COMPETENCY_QUESTIONS.md`
- SPARQL queries to test question answering
- Regular review and update of questions
- Clear mapping between questions and ontology elements

---

## Summary

These architectural decisions collectively establish a robust, standards-compliant, and community-aligned approach to developing the DFO Salmon Ontology. The hybrid OWL+SKOS approach enables both formal relationships and controlled vocabularies, while Darwin Core integration ensures international interoperability. The single-file structure with clear separation of schema and data provides simplicity while maintaining flexibility for future growth.

The quality assurance framework and competency-driven development approach ensure the ontology meets real-world needs while maintaining high technical standards. The use of industry-standard tools (ROBOT, SHACL) and alignment with external vocabularies positions the ontology for long-term success and community adoption.
