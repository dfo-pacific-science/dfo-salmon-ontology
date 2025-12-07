# ADR-001: Hybrid OWL+SKOS Modeling Approach

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to model both formal relationships (OWL) and controlled vocabularies (SKOS) for automated classification systems.

## Decision

We will use a hybrid approach combining OWL and SKOS:

- **OWL classes** for formal relationships and structural entities (events, measurements, stocks)
- **SKOS concepts** for controlled vocabularies (methods, criteria, status categories)
- **SHACL shapes** for validation rules and automated classification

## Rationale

1. **Operational Focus**: The ontology models operational processes, not biological concepts
2. **Automated Classification**: Need both controlled vocabularies (methods) and rich data modeling (events with metadata)
3. **Separation of Concerns**: Methods as vocabulary terms, events as data carriers
4. **Industry Standards**: Aligns with OBO Foundry principles and community practices

## Alternatives Considered

1. **Pure OWL Approach**: Using only OWL classes for everything
   - **Rejected**: Would require complex OWL restrictions for controlled vocabularies, making the ontology harder to understand and maintain
   
2. **Pure SKOS Approach**: Using only SKOS concepts for everything
   - **Rejected**: Would lose formal reasoning capabilities needed for automated classification and data validation
   
3. **OWL Enumerations**: Using OWL enumerated classes instead of SKOS
   - **Rejected**: Less flexible for controlled vocabularies and doesn't align with community practices for method vocabularies

## Consequences

**Positive:**

- Supports manual estimate type assignment (Hyatt 1997 framework) - automated classification deferred to post-MVP
- Supports both human-readable vocabularies and machine-processable relationships
- Aligns with existing salmon data management practices
- Facilitates data quality validation through SHACL rules

**Negative:**

- Increased complexity compared to pure OWL approach
- Requires understanding of both OWL and SKOS modeling patterns
- Potential confusion between OWL classes and SKOS concepts

## Implementation

- SKOS schemes for enumeration methods, estimate methods, downgrade criteria, and status categories
- OWL classes for survey events, measurements, and organizational structures
- SHACL shapes for method-specific validation and automated type assignment
