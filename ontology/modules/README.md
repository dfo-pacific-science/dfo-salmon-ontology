# Alignment Modules (SOSA / I-ADOPT / DwC)

These module files provide **optional** alignment overlays for the DFO Salmon Ontology.

The non-normative salmon metamodel view previously housed here now lives in the shared SMN repo under `ontology/views/`.

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

Use the **SMN metamodel view** (in the shared SMN repo under `ontology/views/`) when you want to:
- inspect only the shared upper-level/crosswalk model,
- facilitate architecture discussion with contributors/domain experts,
- review the entity/property/variable/method-event-result-provenance decomposition without making it DFO-owned content.

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

## Verifying a module

```bash
make check-modules
```

This is the entrypoint for these files, and it runs as part of `make test`. Every other target
loads `ontology/dfo-salmon.ttl` alone, which imports neither overlay and so reports nothing
about them; `check-modules` merges each overlay with core the way this README tells you to use
them, and checks what that merge produces.

It matters because the merge is where these files can fail silently. The OWL API supplies a
declaration for any otherwise-untyped IRI used in class or property position, so an overlay
naming a term core no longer declares does not fail loudly — it mints that term as a fresh
`owl:Class` or `owl:ObjectProperty`. That is how eight retired `gcdfo:` terms survived here
after the core migration to `smn:`; see
[ADR-007](../../docs/adr/007-alignment-overlays-follow-core-to-smn.md). Run against the
pre-fix overlays, the check reports the terms each one re-minted: two for `alignment-main`
(`gcdfo:hasDeme`, `gcdfo:hasPopulation`), five for `alignment-research`. It reports nothing for
the other three retired names, because those appeared only in annotation position, where the
OWL API mints nothing — retargeting them was still correct, but this check is not what proves
it.

What it checks, per module — each with the condition that would retire it:

| Check | Retires when |
|---|---|
| The merge declares no `gcdfo:`/`smn:` term that core does not | never in practice — it depends on the OWL API minting declarations for untyped IRIs |
| No pair of terms carries two different `skos:*Match` predicates | the overlays stop restating mappings the shared layer already makes |
| The merged closure is ELK-consistent | never; it is the minimum a loadable overlay must meet |

To inspect a merge by hand, `check-modules` leaves it in `release/tmp/modules/`, or build one
directly:

```bash
java -jar tools/robot.jar merge \
  --catalog release/tmp/robot-catalog.xml \
  --input ontology/dfo-salmon.ttl \
  --input ontology/modules/alignment-main.ttl \
  --output /tmp/merged.ttl
```

### Why these files use `skos:closeMatch` between OWL classes

`scripts/sparql/skos-match-on-owl-classes.rq` lints against `skos:*Match` where either side is
an OWL class, and it reports these overlays' class bridges. `check-modules` deliberately does
not run it, because that lint is scoped to the terms this repo authors and these bridges are
not the overlays' invention: the imported `smn` closure contributes **18** such rows before any
overlay is loaded — including `smn:SurveyEvent skos:closeMatch sosa:Sampling` and
`gcdfo:FisheriesReferencePointLower skos:closeMatch iadopt:Constraint`, which upstream asserts
about a DFO class. The shared layer also deliberately *demoted* a `sosa:Sampling` superclass
claim to `skos:closeMatch` (alignment finding F7). Rewriting the overlays as
`rdfs:subClassOf`/`owl:equivalentClass` would assert unconfirmed equivalence in the file whose
stated purpose is to avoid brittle equivalence axioms, and would contradict that upstream
decision.

This exemption retires if the shared layer moves off the `skos:*Match` idiom for class-to-class
alignment; at that point the class lint can run over the merged closure like any other check.
Individual rows graduate earlier: promote one to `rdfs:subClassOf`/`owl:equivalentClass` when
the pairing has been confirmed **and** the shared layer states it in OWL.

## SDP decomposition workflow (practical split)

For Salmon Data Package work (`term_iri`, `property_iri`, `entity_iri`, optional `constraint_iri`, `method_iri`):

- Keep the **normative DFO schema spine** in `ontology/dfo-salmon.ttl` (stable classes/properties contributors must rely on).
- Keep broader cross-framework and publication-profile mappings in these module files.
- Treat I-ADOPT Variables as **compound terms** in day-to-day data packaging (typically represented as SKOS concepts with decomposition annotations), while maintaining OWL-level bridge semantics for metamodel interoperability.

Rule of thumb:
- If contributors need it every day to encode SDP semantics, promote it to core.
- If it is a crosswalk hypothesis or publication-oriented mapping, keep it in a module.
