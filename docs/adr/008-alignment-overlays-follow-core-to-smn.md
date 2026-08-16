# ADR-008: Alignment overlay modules follow core to `smn:`

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
  `mappings/gcdfo-to-smn.sssom.tsv`. `make check-modules` now fails on the next one instead of
  absorbing it silently: a renamed term stops being declared in core's closure, so the overlay's
  reference to the old name shows up as a minted term.
- These axioms are now semantically live rather than inert, which raises the cost of a
  careless merge of the research overlay. That module's existing "review before merge"
  warning matters more than it did.

### Neutral

- The overlays are now validated: `make check-modules` merges each with core and checks the
  result, and `make test` runs it. See "Wiring the overlays into validation" below.

## Wiring the overlays into validation

The first version of this ADR left the overlays outside automated validation and recorded the
`skos:*Match`-on-OWL-classes question as open. Review (PR #81) pushed on both. Resolved as
follows, from measurement rather than from argument.

### Measured: what `scripts/sparql/skos-match-on-owl-classes.rq` actually reports

Run over merged closures (ROBOT 1.9.8, 2026-08-16). Two `smn` resolutions are shown because
the build uses either: the pinned `SMN_PIN` commit `a5d4f28` when no sibling checkout exists,
or `SMN_FLAT_TTL` when one does. The numbers move by one row between them, and the conclusion
does not.

| Closure | Pinned `a5d4f28` | Sibling checkout at `78b4435` |
|---|---|---|
| core alone, import closure collapsed, **no overlay** | **18** | **18** |
| core + `alignment-main`, before the retarget | 31 | 30 |
| core + `alignment-main`, after the retarget | **24** | **24** |
| core + `alignment-research`, before the retarget | 34 | 33 |
| core + `alignment-research`, after the retarget | **27** | **27** |
| `ontology/dfo-salmon.ttl` as `make test` queries it (imports not merged) | 0 | 0 |

The one-row difference is `FisheriesReferencePointLower`: the pin asserts the match about
`smn:FisheriesReferencePointLower`, a term upstream minted but never declared, and `78b4435`
re-namespaces it to `gcdfo:FisheriesReferencePointLower`. Both baselines are 18 rows.

Three things follow. First, the retarget **reduced** the count — it removed six phantom-subject
rows per overlay and added none to `alignment-main`; the single row it adds to
`alignment-research` (`smn:ReportingOrManagementStratum skos:closeMatch iadopt:Entity`) replaces
the identical row on the retired `gcdfo:` name. Second, every retargeted row that remains is
**already asserted verbatim by upstream `smn`** — it is in the 18-row core baseline, so the
overlay contributes a duplicate triple, not a new claim. Third, `make test` reports 0 not
because core is clean but because `robot query` does not load the import closure; the 18 rows
are in the closure either way.

### Decision: keep `skos:*Match`; do not convert to `rdfs:subClassOf`/`owl:equivalentClass`

Class-to-class `skos:closeMatch` is the shared layer's own cross-framework idiom, not a slip in
these overlays. `smn` asserts it 18 times in the closure this repo imports, about its own OWL
classes (`smn:SurveyEvent skos:closeMatch sosa:Sampling`, `smn:ReferencePoint skos:closeMatch
iadopt:Constraint`, and the rest of the retargeted set) and about third-party pairs
(`sosa:Observation skos:closeMatch dwc:Occurrence`). Upstream `78b4435` goes further and asserts
one about a DFO class, `gcdfo:FisheriesReferencePointLower skos:closeMatch iadopt:Constraint`;
the pin predates that re-namespacing. `smn` also deliberately **demoted** a `sosa:Sampling`
superclass claim to
`skos:closeMatch` (alignment finding F7, mirrored in `dfo-salmon.ttl`). Converting the overlay
rows to OWL axioms would assert equivalences nobody has confirmed, in the file whose stated job
is to avoid brittle equivalence axioms, and would reverse F7. Rows graduate individually when
the pairing is confirmed and the shared layer states it in OWL.

`make check-modules` therefore does not run the class lint, and `ontology/modules/README.md`
records the condition that retires that exemption: the shared layer moving off the idiom.

### Decision: check the overlays for what they can actually get wrong

`make check-modules` (in `make test`) merges each overlay with core and checks:

1. **Minted terms** — no `gcdfo:`/`smn:` term declared in the merge that core does not declare.
   This is the defect above, made executable. Run against the pre-fix overlays it reports
   exactly the re-minting table: `gcdfo:hasDeme` and `gcdfo:hasPopulation` for
   `alignment-main`, those two plus `gcdfo:SurveyEvent`, `gcdfo:EscapementSurveyEvent` and
   `gcdfo:EscapementMeasurement` for `alignment-research`. Run against the fixed ones it
   reports none. It says nothing about the other three retired names — they appeared only in
   annotation position, where nothing is minted — so this check bounds the silent-resurrection
   failure, not the whole retarget.
2. **Mapping-strength conflicts** — no pair carrying two different `skos:*Match` predicates.
   This found a real defect that predates this PR: both overlays asserted
   `sosa:Sampling skos:closeMatch dwc:Event` while `smn` asserts `skos:broadMatch` on the same
   pair. Fixed here by mirroring upstream.
3. **ELK consistency** of the merged closure — the claim this ADR makes above, made executable.

The overlays restate several mappings `smn` already owns. Where a restatement agrees it is a
harmless duplicate triple; check 2 is what catches one that does not.

## More Information

```bash
make check-modules
```

A green `make test` **now** covers these files. Before this change it did not, and a green run
was not evidence about them either way.

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
