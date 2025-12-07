# ADR-002: Schema vs Data Separation

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need to maintain clean separation between ontology schema and instance data.

## Decision

We will strictly separate schema and data:

- **Ontology file**: Contains only schema elements (classes, properties, SKOS concepts)
- **Instance data**: Stored in separate files or systems
- **Examples**: Minimal test data in `ontology/examples/` for validation only

## Rationale

1. **Maintainability**: Schema changes independently of data updates
2. **Reusability**: Same schema can be used for multiple datasets
3. **Versioning**: Schema and data can have different versioning cycles
4. **Interoperability**: Other systems can import just the schema

## Alternatives Considered

1. **Mixed Schema and Data**: Including instance data directly in the ontology file
   - **Rejected**: Would create versioning conflicts, make the ontology file large and unwieldy, and reduce reusability
   
2. **Data-Only Approach**: Creating separate ontology files for each dataset
   - **Rejected**: Would lead to schema duplication and inconsistency across datasets
   
3. **Embedded Examples**: Including extensive example data within the schema file
   - **Rejected**: Would blur the line between schema and data, making it harder to identify the core ontology structure

## Consequences

**Positive:**

- Clean, focused ontology file
- Easier schema validation and maintenance
- Better separation of concerns
- Enables schema reuse across different datasets

**Negative:**

- Requires discipline to maintain separation
- May need additional tooling for data management
- Potential confusion about where to put certain elements

## Implementation

- `ontology/dfo-salmon.ttl` contains only schema elements
- `ontology/examples/` contains minimal test data for validation
- Instance data stored in separate RDF files or graph databases
- SHACL shapes validate data structure without containing data
