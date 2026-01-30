# ADR-003: IRI and Versioning Policy

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for stable, persistent identifiers and clear versioning strategy.

## Decision

We will use:

- **Base IRI**: `https://w3id.org/gcdfo/salmon#`
- **Versioning**: Semantic versioning with `owl:versionInfo` and `owl:versionIRI`
- **Stability**: No breaking changes to existing IRIs

## Rationale

1. **Persistence**: W3ID provides stable, resolvable identifiers
2. **Versioning**: Clear versioning enables proper dependency management
3. **Stability**: Prevents breaking changes for existing users
4. **Standards Compliance**: Follows OBO Foundry and W3C best practices

## Alternatives Considered

1. **GitHub-based IRIs**: Using GitHub raw URLs as identifiers
   - **Rejected**: GitHub URLs can change with repository moves, less stable than W3ID
   
2. **Local IRIs**: Using local identifiers without resolvable URLs
   - **Rejected**: Would prevent external systems from resolving and understanding our terms
   
3. **DOI-based IRIs**: Using Digital Object Identifiers for versioning
   - **Rejected**: DOIs are better for publications than ontology terms; W3ID is more appropriate for semantic web resources
   
4. **No Versioning**: Using only base IRIs without version information
   - **Rejected**: Would make it impossible to track changes and maintain backward compatibility

## Consequences

**Positive:**

- Stable identifiers for long-term use
- Clear versioning enables proper dependency management
- W3ID provides reliable resolution
- Follows established community practices

**Negative:**

- Requires careful management of versioning
- W3ID setup and maintenance overhead
- Need to maintain backward compatibility

## Implementation

- Base IRI: `https://w3id.org/gcdfo/salmon#`
- Version IRIs: `https://w3id.org/gcdfo/salmon/0.0.999` (example)
- GitHub releases with semantic versioning
- W3ID redirect configuration for stable resolution
