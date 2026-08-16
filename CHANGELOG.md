# DFO Salmon Ontology - Changelog

> **Version-numbering note.** The sequence is `0.0.1 → 0.0.2 → … → 0.0.7 →
> 0.0.8 → 0.0.9`. The `[0.0.999]` entry dated 2026-01-30 is a **documented
> anomaly**, not a predecessor of 0.0.8: it recorded a short-lived pre-1.0
> "beta" numbering experiment that was abandoned when 0.0.7/0.0.8 resumed the
> ordinary sequence. It is kept for the historical record (and because
> `docs/releases/0.0.999/` is published) but the version line does **not** need
> to exceed it. Do not re-adopt `0.0.99x` numbering.

## [Unreleased]

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
  subject source `0.0.8+s9-step3`; object source smn `main` at commit
  `a5d4f284e859b4c878cbec5baa04d368ab1990d3`. Validated out of band with
  sssom-py and metasalmon's `read_sssom_mapping_set()`.
- `scripts/verify_mappings.py` and a `make verify-mappings` target: a
  stdlib-only, CI-fatal structural check of the mapping set (byte contract,
  required metadata, fixed column set, row completeness, uniqueness, declared
  CURIE prefixes, reviewed-predicate vocabulary). Wired as the first
  prerequisite of `make test`.
- `SMN_PIN` in the `Makefile`: the smn commit the import closure resolves to
  when no sibling `../salmon-domain-ontology` checkout is present.

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

### Changed (release preparation)

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
