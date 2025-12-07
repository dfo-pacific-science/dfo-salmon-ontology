# ADR-004: ROBOT Toolchain Selection

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for robust ontology development and validation toolchain.

## Decision

We will use ROBOT (ROBOT is an OWL Tool) for:

- Ontology validation and reasoning
- Format conversion (TTL, OWL, JSON)
- Quality control and metrics
- Release management

## Rationale

1. **OBO Foundry Standard**: ROBOT is the standard tool for OBO ontologies
2. **Comprehensive Functionality**: Provides all necessary ontology operations
3. **Community Support**: Well-maintained with active community
4. **Integration**: Works well with existing OBO workflows

## Alternatives Considered

1. **Protégé-only Workflow**: Using only Protégé for ontology development and validation
   - **Rejected**: Protégé lacks automated quality control, batch processing, and release management capabilities
   
2. **Custom Scripts**: Building custom validation and processing scripts
   - **Rejected**: Would require significant development effort and maintenance overhead; ROBOT already provides proven functionality
   
3. **OWL API Direct Usage**: Using OWL API directly in Java applications
   - **Rejected**: Requires Java development expertise and doesn't provide the high-level operations that ROBOT offers
   
4. **Alternative Tools**: Using other ontology tools like HermiT, Pellet, or FaCT++
   - **Rejected**: These are primarily reasoners, not comprehensive ontology development toolchains like ROBOT

## Consequences

**Positive:**

- Industry-standard tooling
- Comprehensive ontology operations
- Active community support
- Integrates well with OBO workflows

**Negative:**

- Requires Java installation
- Learning curve for new users
- Doesn't check SKOS concepts or schemes. In fact SKOS confuses ROBOT

## Implementation

- ROBOT 1.8.3 installed in `tools/robot.jar`
- Batch scripts for common operations
- Integration with CI/CD pipeline
- Documentation and training materials
