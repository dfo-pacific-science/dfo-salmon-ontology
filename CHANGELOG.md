# DFO Salmon Ontology - Changelog

> **Version-numbering note.** The sequence is `0.0.1 → 0.0.2 → … → 0.0.7 →
> 0.0.8 → 0.0.9`. The `[0.0.999]` entry dated 2026-01-30 is a **documented
> anomaly**, not a predecessor of 0.0.8: it recorded a short-lived pre-1.0
> "beta" numbering experiment that was abandoned when 0.0.7/0.0.8 resumed the
> ordinary sequence. It is kept for the historical record (and because
> `docs/releases/0.0.999/` is published) but the version line does **not** need
> to exceed it. Do not re-adopt `0.0.99x` numbering.

## [Unreleased]

### Removed
- `docs/webvowl/data/ontology.stamp`, the orphaned output of the pre-normalizer
  WebVOWL stabilization approach. It recorded a merged-input + WIDOCO-version
  hash so `scripts/stabilize_webvowl_output.py` could restore prior
  `ontology.json` bytes on an unchanged input. PR #78 removed that script from
  the `docs-widoco` recipe in favour of `scripts/normalize_webvowl_json.py` but
  left both the script and the stamp behind, so the file had no writer and no
  reader: `grep -rn stabilize_webvowl_output` and `grep -rn ontology.stamp`
  return nothing outside the dead script itself, and `make ci` run twice leaves
  the stamp byte-identical and untouched. It was frozen at
  `widoco-1.4.25:a70a3d52…` since 2026-03-15. `scripts/stabilize_webvowl_output.py`
  is the same dead path and is removed under separate sign-off, since `AGENTS.md`
  requires asking before deleting anything under `scripts/`.

### Changed
- `docs/tech-debt.md`'s 2026-03-15 "WebVOWL churn stabilized" entry no longer
  reads as a standing guarantee. PR #78 rewrote that entry **in place** — new
  mechanism, original date — so the log described `normalize_webvowl_json.py`
  under a heading that had resolved a different implementation, and the evidence
  that a replacement had happened at all was overwritten. The entry therefore
  asserted a working gate throughout the window (PR #78 → PR #82) in which the
  gate did nothing. It now records what the 2026-03-15 fix was, what superseded
  it, when the claim was false, and a command that re-checks it.
- `docs/context/widoco.md` now names `scripts/normalize_webvowl_json.py` as the
  only thing that touches `docs/webvowl/data/ontology.json` after WIDOCO writes
  it, links [ADR-007](docs/adr/007-webvowl-duplicate-node-disambiguation.md), and
  records the `set -e` recipe and the CI drift gate. It had the same in-place
  rewrite as the tech-debt entry and described the behaviour without naming any
  code, so a reader could not tell which of the two scripts in `scripts/` was
  live.

## [0.0.9] - 2026-08-16

First release cut after the S9 step-3 shared-layer boundary work (PR #78). This
release **removes four `gcdfo:` object properties** and **moves one class
between namespaces**; consumers holding the old IRIs should read
`mappings/gcdfo-to-smn.sssom.tsv` for the replacements.

### Added
- `mappings/gcdfo-to-smn.sssom.tsv`: the smn/gcdfo boundary published as data —
  **32 reviewed rows** (19 `skos:exactMatch` for terms smn migrated verbatim,
  12 `skos:closeMatch` for terms smn adapted, 1 `skos:relatedMatch` for the one
  cross-category concept-to-property link). Four of the exactMatch rows are
  *replacement rows* for the `gcdfo:` properties removed in this release, so a
  dataset holding a retired IRI can resolve it. Mapping-set version `0.1.0`;
  subject source `0.0.8+s9-step3`; object source smn **0.0.3** (release tag,
  commit `f7205eea45817cc6a58e4f15b4f31f344da8434f`) — see the pin correction
  below. Validated out of band with sssom-py and metasalmon's
  `read_sssom_mapping_set()`.
- `scripts/verify_mappings.py` and a `make verify-mappings` target: a
  stdlib-only, CI-fatal structural check of the mapping set (byte contract,
  required metadata, fixed column set, row completeness, uniqueness, declared
  CURIE prefixes, reviewed-predicate vocabulary). Wired as the first
  prerequisite of `make test`.
- `SMN_PIN` in the `Makefile`: the smn commit the import closure resolves to
  when no sibling `../salmon-domain-ontology` checkout is present.
- `make check-modules`: the validation entrypoint for `ontology/modules/*.ttl`.
  Merges each optional overlay with core — the path `ontology/modules/README.md`
  tells contributors to use — and fails on terms the merge mints in the
  `gcdfo:`/`smn:` namespaces, on a pair carrying two different `skos:*Match`
  predicates, and on an inconsistent merged closure. Wired into `make test`, so
  the overlays are no longer excluded from validation; documented in
  `docs/entrypoints.md` and [ADR-008](docs/adr/008-alignment-overlays-follow-core-to-smn.md).

### Removed
- The four object properties that duplicated their smn twins verbatim (same
  label, definition, domain, and range) — `gcdfo:hasFeatureOfInterest`,
  `gcdfo:hasObservationResult`, `gcdfo:usesObservationProcedure`,
  `gcdfo:isSampleOfStratum`. Use `smn:hasFeatureOfInterest`,
  `smn:hasObservationResult`, `smn:usesObservationProcedure`, and
  `smn:isSampleOfStratum` directly. Each removal leaves a pointer comment in
  `ontology/dfo-salmon.ttl`, an `skos:exactMatch` replacement row in the
  mapping set, and the competency-question examples in
  `docs/COMPETENCY_QUESTIONS.md` now use the smn properties. The parallel
  exploratory declarations in `ontology/modules/alignment-research.ttl` (an
  unwired staging module) were removed in the same pass.

### Changed
- `gcdfo:ConservationUnit`'s definition now reads "A group of **wild salmon**
  sufficiently isolated from other groups…" instead of "A group of **fish**…",
  matching the Wild Salmon Policy glossary it already cites (#76). The string
  is authored in four places and every authored copy was updated in the same
  change: `ontology/dfo-salmon.ttl` (canonical), the curated
  `ontology/views/wsp-composite-escapement-view.ttl` (`skos:definition`), the
  `draft/dfo-salmon-draft.ttl` idea bank, and the generated `docs/` artifacts
  (`gcdfo.{ttl,owl,jsonld}`, `index.html`, `index-en.html`, WebVOWL data).
  `docs/releases/0.0.8/` and earlier snapshots are immutable and deliberately
  keep the old wording. See `docs/tech-debt.md` for the duplication itself.
- **Alignment overlays retargeted at `smn:`** after the core migration
  (`ADR-008`): eight axiom subjects in `ontology/modules/alignment-main.ttl` and
  `alignment-research.ttl` named `gcdfo:` terms core had retired, which a
  core+overlay merge silently re-minted. Both overlays also asserted
  `sosa:Sampling skos:closeMatch dwc:Event` where the shared layer asserts
  `skos:broadMatch`; they now mirror upstream. The overlays keep `skos:*Match`
  for class-to-class bridges — that is the shared layer's own idiom, which
  contributes 18 such rows to the import closure before any overlay loads;
  ADR-008 carries the measurements.
- **Re-namespaced** `smn:FisheriesReferencePointLower` to
  `gcdfo:FisheriesReferencePointLower` (and its `rdfs:isDefinedBy` from
  `https://w3id.org/smn` to `https://w3id.org/gcdfo/salmon`): the term was
  minted in the smn namespace but never declared upstream, and it is
  DFO-policy-scoped like its sibling reference-point terms. Upstream smn has
  since ratified the move — smn 0.0.3 re-points its `skos:closeMatch` to
  `gcdfo:FisheriesReferencePointLower`.
- MIREOT mirrors refreshed against smn `main` (post methods-as-SKOS migration):
  `smn:EnumerationMethod` is now instance-typed `sosa:Procedure` and a member
  of `smn:MethodScheme` as well as the local
  `gcdfo:EnumerationMethodScheme`; the `smn:EscapementMeasurement` mirror
  follows the upstream rename to `smn:EscapementEstimate` (which also updates
  the `gcdfo:hasYearBasis` domain union); the `smn:SurveyEvent` mirror drops
  the `sosa:Sampling` superclass smn deliberately demoted to a
  `skos:closeMatch`.
- The smn import now resolves to a **pinned commit** (`SMN_PIN`) when no
  sibling checkout exists, and **fails loudly** if that fetch fails, instead of
  silently writing an empty catalog and falling back to remote-latest
  resolution. This makes the import closure — and therefore the generated
  `docs/` artifacts — citable.
- `docs/ADR.md` gains a numbering-correspondence note declaring the per-decision
  files under `docs/adr/` canonical and mapping the inline ADR numbers onto
  them.
- `README.md` and `docs/entrypoints.md` describe `make test` as
  "mapping-set structure + theme coverage + alpha-lint + ELK reasoning".
- Regenerated `docs/` publication artifacts (`gcdfo.ttl`, `gcdfo.owl`,
  `gcdfo.jsonld`, `index.html`, `index-en.html`, WebVOWL data) against the new
  import closure.

### Fixed
- The WebVOWL output-stabilization gate was reporting success while doing nothing, and had
  been since PR #78. Three compounding faults: `scripts/normalize_webvowl_json.py` aborted
  on every run (`Non-unique semantic class key`) because the merged closure emits three
  `xsd:gYear` datatype nodes and the class key required `(type, iri)` to be unique; the
  `docs-widoco` recipe was one `;`-chained shell with no `set -e`, so make took the trailing
  `echo`'s exit status and printed a success mark over the crash; and CI excluded
  `docs/webvowl/data/ontology.json` from its uncommitted-changes check, so nothing
  downstream noticed. Colliding class keys are now widened with the node's property-wiring
  context, `docs-widoco` and `release-snapshot` run under `set -e`, and the CI exclusion is
  removed. See [ADR-007](docs/adr/007-webvowl-duplicate-node-disambiguation.md).
- `make ci-sync-artifacts` staged only `docs/gcdfo.{ttl,owl,jsonld}` and `docs/index*.html`,
  so a contributor who committed exactly what the supported helper prepared still pushed a
  tree CI rejects as dirty. `make ci` also rewrites `docs/webvowl/`, `docs/resources/` and
  `docs/provenance/` — 26 further tracked files, including the
  `docs/webvowl/data/ontology.json` the drift check now covers. The helper stages all of
  them, by directory pathspec so a WIDOCO upgrade cannot emit a file it skips, and reports
  what it staged instead of printing a success mark through `|| true`. The path list now
  exists only as `CI_ARTIFACT_PATHS` in the Makefile: CI's failure message and `README.md`
  each carried their own incomplete copy, which is how the copies drifted apart.
- `scripts/requirements.txt` allowed `rdflib>=6.2,<7` while CI installs `rdflib==7.2.1`, and
  the two do not agree on `docs/gcdfo.jsonld`: rdflib 6.3.2 drops `"@type": "xsd:integer"`
  from 20 `skos:notation` values that 7.2.1 keeps. A contributor following the repo's own
  dependency file therefore could not produce a tree CI accepts, whatever they committed.
  Pinned to the CI version; `docs/entrypoints.md` now names the install step, which nothing
  documented before.
- `docs/webvowl/data/ontology.json` is re-baselined from raw generator output to the
  normalizer's own rendering, which lands the corrections it was always meant to apply:
  `owl:inverseOf` edges OWL2VOWL drops (13 properties) and `skos:prefLabel` preference over
  `rdfs:label` (2 classes, one of which — `smn:EscapementSurveyEvent` — carries two
  competing English `rdfs:label` values upstream).

### Changed (release preparation)

- `docs/releases/0.0.9/` was re-cut after PR #77 merged. The snapshot had been
  taken before that merge, so it still carried the superseded "A group of fish…"
  `gcdfo:ConservationUnit` definition while `docs/gcdfo.*` carried the WSP
  wording; nothing in `make ci` compares the two, because `make ci` does not
  write `docs/releases/` at all. Re-cutting an *unpublished* snapshot is not the
  `FORCE=1` overwrite the README warns against — 0.0.9 is not tagged yet — but
  the gap that let it drift is recorded in `docs/tech-debt.md`.
- `SMN_PIN` and the mapping set's `object_source_version` now cite the smn
  **0.0.3 release tag** (commit `f7205ee`) instead of an intermediate `main`
  commit. A downstream resolving this import closure must be able to point at
  a tagged, immutable artifact — pinning an unreleased commit defeated the
  purpose. Verified safe: the pin-to-release diff touches only module ontology
  headers, the smn version stamp, and the FisheriesReferencePointLower
  `closeMatch` re-point, so none of the 32 mapped terms change. All gates
  re-run green against the release pin. The mapping set's own repository
  reference is unchanged: this ontology lives under `dfo-pacific-science`,
  unlike the `salmon-data-mobilization` siblings.

## [0.0.8] - 2026-03-29

### Added
- Added `gcdfo:RemovalReference` as a DFO-specific fisheries-management reference point.
- Added `gcdfo:AbsoluteAbundanceDataType` and `gcdfo:RelativeIndexDataType` under `gcdfo:AbundanceDataType`.
- Added `gcdfo:PopulationEnhancementStatusScheme`, `gcdfo:PopulationEnhancementStatus`, `gcdfo:EnhancedPopulation`, and `gcdfo:NonEnhancedPopulation` using the repo's standard SKOS scheme pattern.

### Changed
- Clarified the enhancement-status vocabulary as a population-level source-workflow classification, not individual fish-origin semantics and not a pHOS threshold.
- Narrowed PR #66 to the intended ontology additions only, removing unrelated TTL churn before release generation.

## [0.0.7] - 2026-03-27

*Backfilled 2026-08-16. These three bullets sat unreleased in `[Unreleased]`
from PR #56 (2026-03-13) through the 0.0.8 cut and were never promoted; they
describe the first gcdfo↔smn boundary pass, which shipped in 0.0.7, not in
0.0.9.*

### Changed
- Added explicit `owl:imports` linkage to shared `smn` and conservative boundary alignment axioms for safe overlap terms.
- Kept `Population`, `hasPopulation`/`populationOf`, `ReferencePoint`, and `MetricBenchmark` as intentional DFO-local semantics in the boundary pass.
- Documented `EnumerationMethod` as an intentionally SKOS-modeled concept root (no OWL-class equivalence cutover in this pass).

## [0.0.999] - 2026-01-30

### Changed
- Pre-1.0 “beta” versioning adopted (current working version: 0.0.999)

### Technical
- Docs pipeline includes JSON-LD serialization generation (so `make ci` can publish `docs/gcdfo.jsonld`)

## [0.0.2] - 2025-01-07

### Added
- Initial ontology structure with core classes and properties
- Stock status zone scheme (SKOS)
- COSEWIC status scheme (SKOS)
- Survey and estimate event classes
- Measurement and unit classes
- Management unit hierarchy classes
- Object and data properties for salmon data integration

### Changed
- Fixed Turtle syntax error in language tag (line 681)
- Corrected SKOS property names (prefLabel instead of preflabel)

### Technical
- Set up ROBOT toolchain for ontology validation and processing
- Organized directory structure for ontology development
- Added quality control scripts and documentation

## [0.0.1] - Initial Release
- Basic ontology framework established
