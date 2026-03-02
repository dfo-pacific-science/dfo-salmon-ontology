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

- `upper-level-view.ttl`
  - Composition root for the standalone **Salmon Data Metamodel** view.
  - Imports seven focused decomposition slices for term extraction + ontological mapping:
    - `upper-level-view-entity.ttl` (entity/object of interest + matrix/context)
    - `upper-level-view-property.ttl` (measured characteristic/property)
    - `upper-level-view-variable.ttl` (entity + property + constraints + statistical modifier)
    - `upper-level-view-method-protocol.ttl` (how generated/measured)
    - `upper-level-view-event-observation.ttl` (when/where/by whom, survey/sampling context)
    - `upper-level-view-result-datum.ttl` (result/sample datum carriers)
    - `upper-level-view-provenance.ttl` (lineage/agent/activity links)
  - Deliberately does **not** import `https://w3id.org/gcdfo/salmon` so WebVOWL can show only the upper-level/metamodel graph.
  - Intended for review discussions and architecture orientation (not normative core inference).

## When to use each

Use **alignment-main** when you want to:
- give contributors metamodel context,
- improve discoverability in docs/WebVOWL,
- avoid introducing brittle equivalence axioms.

Use **alignment-research** when you want to:
- test broader alignment hypotheses,
- explore SOSA/I-ADOPT bridge patterns,
- design next-round SHACL + competency query updates.

Use **upper-level-view** when you want to:
- inspect only the upper-level/crosswalk model in WebVOWL,
- avoid import-closure noise from the full `gcdfo` ontology,
- facilitate architecture discussion with contributors/domain experts,
- review the 7-slice decomposition workflow (entity/property/variable/method-event-result-provenance) without editing one monolithic file.

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

## SDP decomposition workflow (practical split)

For Salmon Data Package work (`term_iri`, `property_iri`, `entity_iri`, optional `constraint_iri`, `method_iri`):

- Keep the **normative salmon metamodel spine** in `ontology/dfo-salmon.ttl` (stable classes/properties contributors must rely on).
- Keep broader cross-framework and publication-profile mappings in these module files.
- Treat I-ADOPT Variables as **compound terms** in day-to-day data packaging (typically represented as SKOS concepts with decomposition annotations), while maintaining OWL-level bridge semantics for metamodel interoperability.

Rule of thumb:
- If contributors need it every day to encode SDP semantics, promote it to core.
- If it is a crosswalk hypothesis or publication-oriented mapping, keep it in a module.
