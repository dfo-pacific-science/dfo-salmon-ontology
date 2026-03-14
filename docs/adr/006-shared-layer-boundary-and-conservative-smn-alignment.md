# ADR-006: Shared-layer boundary and conservative `smn` alignment for DFO ontology terms

## Status

Accepted

## Context

The DFO Salmon Ontology now sits beside a live shared Salmon Domain Ontology namespace (`smn:`). Several DFO terms overlap in label or rough intent with shared-layer terms, but the overlap is uneven: some are safe reusable abstractions, while others carry DFO-specific policy framing, DFO-local relationship meaning, or a different modeling form (OWL class/property vs SKOS concept).

The bad option here is a vibe-based bulk replacement. Same label is not the same contract.

## Decision

Use a **conservative alignment policy**:

1. **Keep `gcdfo:` as the canonical DFO layer.**
   This repo remains the source of truth for DFO-specific terms and DFO-local publication artifacts.

2. **Align only the clearly safe overlaps to `smn:`.**
   Safe shared terms may be imported/aligned where semantics match closely enough to avoid contract drift.

3. **Do not bulk replace same-label overlaps.**
   If a DFO term has materially different scope, policy framing, or modeling shape, keep it local until reviewed term-by-term.

4. **For ambiguous cases, prefer explicit DFO-local retention or reminting over fake equivalence.**
   A misleading exact-match is worse than temporary duplication.

5. **Keep `EnumerationMethod` local as a SKOS concept for now.**
   Use `rdfs:seeAlso smn:EnumerationMethod` rather than asserting a stronger mapping until the concept/class boundary is intentionally resolved.

Deferred review set at the time of this decision:
- `gcdfo:Population`
- `gcdfo:hasPopulation` / `gcdfo:populationOf`
- `gcdfo:ReferencePoint`
- `gcdfo:MetricBenchmark`
- `gcdfo:EnumerationMethod`

## Consequences

### Positive

- Reduces the risk of semantic drift during shared-layer adoption.
- Gives downstream consumers a clear rule: prefer `smn:` where the shared term is truly approved/reusable, otherwise use `gcdfo:`.
- Preserves DFO-specific policy/assessment meaning instead of flattening it into generic shared labels.

### Negative

- Some boundary duplication remains for now.
- Contributors must review overlap cases deliberately instead of using a fast bulk-rewrite strategy.
- Docs need to explain the split clearly until the deferred set is resolved.

### Neutral

- This is a staging decision, not a permanent ban on future bridge extraction.
- Additional alignments can be added later as individual cases become safe and useful.

## More Information

Reference implementation/docs for this decision:
- `README.md`
- `docs/entrypoints.md`
- `docs/context/w3id.md`
- `docs/tech-debt.md`
- `docs/plans/2026-03-13-smn-boundary-passable.md`

## Related

- [ADR-003](003-iri-versioning-policy.md) - versioning/publication decisions for the DFO namespace
- [ADR-005](005-external-vocabulary-integration.md) - related guidance on how this ontology connects to external vocabularies
- [Salmon Domain Ontology namespace stabilization](https://w3id.org/smn) - shared-layer namespace this repo aligns to conservatively
