# ADR-003: IRI and Versioning Policy

**Date:** 2025-01-07  
**Status:** Accepted  
**Context:** Need for stable, persistent identifiers and clear versioning strategy.

## Decision

We will use:

- **Base IRI**: `https://w3id.org/dfo/salmon#`
- **Versioning**: Semantic versioning with `owl:versionInfo` and `owl:versionIRI`
- **Stability**: No breaking changes to existing IRIs

## Rationale

1. **Persistence**: W3ID provides stable, resolvable identifiers
2. **Versioning**: Clear versioning enables proper dependency management
3. **Stability**: Prevents breaking changes for existing users
4. **Standards Compliance**: Follows OBO Foundry and W3C best practices

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

- Base IRI: `https://w3id.org/dfo/salmon#`
- Version IRIs: `https://w3id.org/dfo/salmon/0.2.0`
- GitHub releases with semantic versioning
- W3ID redirect configuration for stable resolution
