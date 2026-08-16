# DFO Salmon Ontology - Changelog

## [Unreleased]

### Added
- `make check-modules`: the validation entrypoint for `ontology/modules/*.ttl`.
  Merges each optional overlay with core — the path `ontology/modules/README.md`
  tells contributors to use — and fails on terms the merge mints in the
  `gcdfo:`/`smn:` namespaces, on a pair carrying two different `skos:*Match`
  predicates, and on an inconsistent merged closure. Wired into `make test`, so
  the overlays are no longer excluded from validation; documented in
  `docs/entrypoints.md`.
- `mappings/gcdfo-to-smn.sssom.tsv`: the smn/gcdfo boundary published as data —
  28 reviewed rows (exactMatch for terms smn migrated verbatim, closeMatch for
  adapted terms, one cross-category relatedMatch), validated with sssom-py and
  metasalmon's `read_sssom_mapping_set()`; structural CI check in
  `scripts/verify_mappings.py` wired into `make test`.

### Changed
- **Alignment overlays retargeted at `smn:`** after the core migration
  (`ADR-007`): eight axiom subjects in `ontology/modules/alignment-main.ttl` and
  `alignment-research.ttl` named `gcdfo:` terms core had retired, which a
  core+overlay merge silently re-minted. Both overlays also asserted
  `sosa:Sampling skos:closeMatch dwc:Event` where the shared layer asserts
  `skos:broadMatch`; they now mirror upstream. The overlays keep `skos:*Match`
  for class-to-class bridges — that is the shared layer's own idiom, which
  contributes 18 such rows to the import closure before any overlay loads;
  ADR-007 carries the measurements.
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
