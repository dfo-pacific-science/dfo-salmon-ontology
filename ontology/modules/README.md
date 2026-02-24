# Alignment Modules (SOSA / I-ADOPT / DwC)

These module files provide **optional** upper-level/data-model alignment layers for the DFO Salmon Ontology.

## Files

- `alignment-main.ttl`
  - Conservative, near-term merge-safe bridges.
  - Uses mostly `skos:closeMatch` and a few safe `rdfs:subPropertyOf` links.
  - Recommended default when contributors want context without strong logical commitments.

- `alignment-research.ttl`
  - Fuller exploratory alignment for analysis/design.
  - Includes stronger candidate subclass and property bridge axioms.
  - Not intended for immediate core merge without targeted review + competency-query checks.

## When to use each

Use **alignment-main** when you want to:
- give contributors metamodel context,
- improve discoverability in docs/WebVOWL,
- avoid introducing brittle equivalence axioms.

Use **alignment-research** when you want to:
- test broader alignment hypotheses,
- explore SOSA/I-ADOPT bridge patterns,
- design next-round SHACL + competency query updates.

## Why modules (instead of core-only)

The crosswalks from files 74/75/76/77 include a mix of:
- ontology-level semantics,
- representation-level mappings,
- data-profile conventions (e.g., DwC-DP `eventID` / `parentEventID`).

Keeping this in modules lets us preserve contributor context without over-constraining `ontology/dfo-salmon.ttl`.

## Source basis

Derived from the latest four alignment artifacts shared in chat:
- `file_74-...csv`
- `file_75-...csv`
- `file_76-...xlsx`
- `file_77-...csv`

## Notes

- These modules are intended to be loaded **alongside** core ontology, not as replacements.
- Prefer `skos:closeMatch` unless exact equivalence has been confirmed.
- Validation rules should remain in SHACL where appropriate.
