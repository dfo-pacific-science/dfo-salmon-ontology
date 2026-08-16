# ADR-007: Alignment overlay modules follow core to `smn:`

## Status

Accepted

## Context

[ADR-006](006-shared-layer-boundary-and-conservative-smn-alignment.md) set a conservative
shared-layer policy and left a **deferred review set** — `gcdfo:Population`,
`gcdfo:hasPopulation`/`populationOf`, `gcdfo:ReferencePoint`, `gcdfo:MetricBenchmark`,
`gcdfo:EnumerationMethod` — to be resolved term by term rather than bulk-replaced.

That deferral has since been resolved in the canonical ontology, in two steps:

1. **2026-03-15** — `ontology/dfo-salmon.ttl` records the migration note
   *"overlapping shared terms now use `smn:` IRIs directly in this ontology;
   DFO-specific semantics remain only where no shared replacement exists."*
2. **2026-08-13** (commit 7489532, S9 step 3) — the object properties that duplicated
   their `smn:` twins verbatim were removed, and competency-question examples were
   retargeted at the `smn:` properties.

The core ontology now references `smn:ReferencePoint` (7×), `smn:ReportingOrManagementStratum`
(8×), `smn:Population` (8×), `smn:hasPopulation` (3×), `smn:SurveyEvent` (3×),
`smn:hasDeme` (2×), `smn:EscapementEstimate` (2×), `smn:IndicatorRiver`,
`smn:EscapementSurveyEvent` and `smn:Deme` — and declares none of their `gcdfo:` twins.

**The alignment overlay modules were not carried along.** `ontology/modules/alignment-main.ttl`
and `ontology/modules/alignment-research.ttl` each still named eight retired `gcdfo:` terms:
`SurveyEvent`, `EscapementSurveyEvent`, `EscapementMeasurement`, `IndicatorRiver`,
`ReferencePoint`, `ReportingOrManagementStratum`, `hasDeme`, `hasPopulation`. One term,
`smn:Stock`, had already been retargeted — the migration was started and not finished.

### Why this was not merely cosmetic

The overlays are absent from the Makefile and are not imported by `dfo-salmon.ttl`, so
`make test` never loaded them and CI stayed green. But `ontology/modules/README.md` tells
contributors these files are *"intended to be loaded **alongside** core ontology"* and names
`alignment-main.ttl` the *"recommended default"*. On that documented path the defect is not
inert: merging core + overlay through ROBOT/the OWL API **silently re-mints the retired terms
as fresh declarations** in the `gcdfo:` namespace, because the OWL API supplies a declaration
for any otherwise-untyped IRI used in class or property position.

Observed before this change, merging core with each overlay:

| Retired term | Re-minted as |
|---|---|
| `gcdfo:hasDeme`, `gcdfo:hasPopulation` | `owl:ObjectProperty` (both overlays) |
| `gcdfo:SurveyEvent`, `gcdfo:EscapementSurveyEvent`, `gcdfo:EscapementMeasurement` | `owl:Class` (research overlay) |

That recreates exactly the `gcdfo:`/`smn:` duplication S9 step 3 removed, in the namespace the
boundary work had just cleaned, without anything reporting it.

## Decision

**Retarget the overlay alignment axioms at the `smn:` counterparts of the retired terms.**
Subjects DFO still owns and declares (`gcdfo:ConservationUnit`, `gcdfo:StockManagementUnit`,
`gcdfo:LowerBiologicalBenchmark`, `gcdfo:FisheriesReferencePointLower`, `gcdfo:WSPRapidStatus`,
`gcdfo:hasConservationUnit`) keep their `gcdfo:` IRIs.

| Overlay subject (was) | Now |
|---|---|
| `gcdfo:SurveyEvent` | `smn:SurveyEvent` |
| `gcdfo:EscapementSurveyEvent` | `smn:EscapementSurveyEvent` |
| `gcdfo:EscapementMeasurement` | `smn:EscapementEstimate` — renamed upstream; SSSOM `skos:exactMatch` |
| `gcdfo:IndicatorRiver` | `smn:IndicatorRiver` |
| `gcdfo:ReferencePoint` | `smn:ReferencePoint` |
| `gcdfo:ReportingOrManagementStratum` | `smn:ReportingOrManagementStratum` |
| `gcdfo:hasDeme` | `smn:hasDeme` |
| `gcdfo:hasPopulation` | `smn:hasPopulation` |

Every target was confirmed present in the pinned upstream `smn` artifact
(commit `a5d4f28`) before retargeting.

### Alternatives rejected

- **Re-declare the `gcdfo:` twins in core.** This directly recreates the verbatim `smn:`
  duplication that 7489532 deliberately removed, and reopens a boundary question ADR-006
  answered. Backwards.
- **Delete the dangling axioms.** Under-fixes. The bridged concepts still exist — they moved
  namespace — so deleting would discard valid SOSA/I-ADOPT/DwC/PROV/RO alignment content to
  fix a naming problem. Deletion is right only where a concept genuinely no longer exists,
  which is true of none of the eight.

### On asserting axioms about `smn:`-owned terms

Retargeting means a DFO module asserts `rdfs:subClassOf` and `skos:closeMatch` about terms the
shared layer owns. This is already the established practice in both files: `smn:Stock
skos:closeMatch sosa:FeatureOfInterest` predates this change, and both overlays assert
`rdfs:subPropertyOf` about W3C-owned SOSA properties (`sosa:hasFeatureOfInterest
rdfs:subPropertyOf prov:used`). The modules are separately-namespaced, explicitly non-normative
overlays; the research module is labelled *"not intended for immediate merge without
validation."* Asserting candidate bridges about externally-owned terms is what these files are
for. No `smn:` term is redefined, renamed, or given DFO-specific semantics.

## Consequences

### Positive

- A core + overlay merge no longer resurrects retired `gcdfo:` terms.
- The bridges do real work for the first time since the migration. ELK over core +
  `alignment-research.ttl` now places `smn:SurveyEvent` under `prov:Activity`,
  `smn:EscapementSurveyEvent` under `sosa:Sampling`, and `smn:EscapementEstimate` under
  `sosa:Result` — alongside the superclasses `smn` asserts itself. Previously these axioms
  attached to phantom terms related to nothing.
- The overlays and core now tell one consistent story about where each concept lives.

### Negative

- The overlays now depend on upstream `smn:` term names, so an upstream rename breaks them.
  `smn:EscapementEstimate` is already one such rename, tracked in
  `mappings/gcdfo-to-smn.sssom.tsv`.
- These axioms are now semantically live rather than inert, which raises the cost of a
  careless merge of the research overlay. That module's existing "review before merge"
  warning matters more than it did.

### Neutral

- CI behaviour is unchanged; `make test` neither caught this nor validates the fix, because
  the build still does not load these modules. Verification is a core + overlay merge —
  see below. Wiring the overlays into automated validation is a separate, larger question
  (they use `skos:*Match` on OWL classes, which `scripts/sparql/skos-match-on-owl-classes.rq`
  lints against in core) and is deliberately not settled here.

## More Information

Verify with a merge of core and each overlay, then check that no IRI asserted about is
undeclared in the closure:

```bash
java -jar tools/robot.jar merge \
  --catalog release/tmp/robot-catalog.xml \
  --input ontology/dfo-salmon.ttl \
  --input ontology/modules/alignment-main.ttl \
  --output /tmp/merged.ttl
```

A green `make test` is **not** evidence for this change either way.

The last full definitions of the retired terms are recoverable with
`git show 7489532:ontology/07-dfo-salmon-terms.txt` (that snapshot was removed as an
unreferenced stray file in PR #80).

## Related

- [ADR-006](006-shared-layer-boundary-and-conservative-smn-alignment.md) — the conservative
  boundary policy and the deferred review set this ADR closes out for the overlay modules
- [ADR-005](005-external-vocabulary-integration.md) — how this ontology connects to external
  vocabularies
- `ontology/modules/README.md` — states the load-alongside-core contributor path
- `mappings/gcdfo-to-smn.sssom.tsv` — curated `gcdfo:` → `smn:` boundary mapping
