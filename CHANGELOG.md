# DFO Salmon Ontology - Changelog

## [Unreleased]

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
- `docs/webvowl/data/ontology.json` is re-baselined from raw generator output to the
  normalizer's own rendering, which lands the corrections it was always meant to apply:
  `owl:inverseOf` edges OWL2VOWL drops (13 properties) and `skos:prefLabel` preference over
  `rdfs:label` (2 classes, one of which — `smn:EscapementSurveyEvent` — carries two
  competing English `rdfs:label` values upstream).

### Added
- `mappings/gcdfo-to-smn.sssom.tsv`: the smn/gcdfo boundary published as data —
  28 reviewed rows (exactMatch for terms smn migrated verbatim, closeMatch for
  adapted terms, one cross-category relatedMatch), validated with sssom-py and
  metasalmon's `read_sssom_mapping_set()`; structural CI check in
  `scripts/verify_mappings.py` wired into `make test`.

### Changed
- **Removed** the four object properties that duplicated their smn twins
  verbatim (`gcdfo:hasFeatureOfInterest`, `gcdfo:hasObservationResult`,
  `gcdfo:usesObservationProcedure`, `gcdfo:isSampleOfStratum`): use
  `smn:hasFeatureOfInterest`, `smn:hasObservationResult`,
  `smn:usesObservationProcedure`, `smn:isSampleOfStratum` directly. The
  competency-question examples now do.
- **Re-namespaced** `smn:FisheriesReferencePointLower` to
  `gcdfo:FisheriesReferencePointLower`: the term was minted in the smn
  namespace but never declared upstream, and it is DFO-policy-scoped like its
  sibling reference-point terms.
- MIREOT mirrors refreshed against smn main (post methods-as-SKOS):
  `smn:EnumerationMethod` is instance-typed `sosa:Procedure` and a member of
  `smn:MethodScheme`; the `smn:EscapementMeasurement` mirror follows the
  upstream rename to `smn:EscapementEstimate`; the `smn:SurveyEvent` mirror
  drops the `sosa:Sampling` superclass smn deliberately demoted.
- The smn import now resolves to a **pinned commit** (`SMN_PIN` in the
  Makefile) when no sibling checkout exists, instead of silently fetching
  remote latest.
- `docs/ADR.md` gains a numbering-correspondence note declaring the
  `docs/adr/` files canonical.
- Added explicit `owl:imports` linkage to shared `smn` and conservative boundary alignment axioms for safe overlap terms.
- Kept `Population`, `hasPopulation`/`populationOf`, `ReferencePoint`, and `MetricBenchmark` as intentional DFO-local semantics in the boundary pass.
- Documented `EnumerationMethod` as an intentionally SKOS-modeled concept root (no OWL-class equivalence cutover in this pass).

## [0.0.8] - 2026-03-29

### Added
- Added `gcdfo:RemovalReference` as a DFO-specific fisheries-management reference point.
- Added `gcdfo:AbsoluteAbundanceDataType` and `gcdfo:RelativeIndexDataType` under `gcdfo:AbundanceDataType`.
- Added `gcdfo:PopulationEnhancementStatusScheme`, `gcdfo:PopulationEnhancementStatus`, `gcdfo:EnhancedPopulation`, and `gcdfo:NonEnhancedPopulation` using the repo's standard SKOS scheme pattern.

### Changed
- Clarified the enhancement-status vocabulary as a population-level source-workflow classification, not individual fish-origin semantics and not a pHOS threshold.
- Narrowed PR #66 to the intended ontology additions only, removing unrelated TTL churn before release generation.

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
