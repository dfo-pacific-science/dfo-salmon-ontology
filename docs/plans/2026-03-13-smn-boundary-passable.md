# SMN Boundary Passable Cleanup (2026-03-13)

## Goal

Reach a truthful, low-drama shared-layer boundary state in one conservative pass without broad refactors.

## Implemented in this pass

- Added `owl:imports <https://w3id.org/smn>` to `ontology/dfo-salmon.ttl`.
- Added conservative `gcdfo -> smn` alignment links for clearly safe overlaps:
  - OWL classes (examples): `Stock`, `Deme`, `ReportingOrManagementStratum`, `StockAssessment`, `Escapement`, `SurveyEvent`, `EscapementSurveyEvent`, `EscapementMeasurement`, `ObservedRateOrAbundance`, `TargetOrLimitRateOrAbundance`.
  - Object properties: `hasDeme`, `demeOf`, `hasFeatureOfInterest`, `hasObservationResult`, `usesObservationProcedure`, `isSampleOfStratum`.
  - SKOS concepts (examples): `MeasurementContext` family, `SalmonOrigin` family, `LifePhase` family.
- Resolved `EnumerationMethod` mismatch to a passable state:
  - kept as `skos:Concept` root in `gcdfo`
  - added explicit scope note that it is intentionally not an OWL-class equivalence cutover in this pass
  - added `rdfs:seeAlso smn:EnumerationMethod` only
- Added in-file boundary comments clarifying intentional local ownership.

## Explicitly retained as DFO-local in this pass

- `Population`
- `hasPopulation`
- `populationOf`
- `ReferencePoint`
- `MetricBenchmark`

## Deferred (intentional)

- No destructive delete/remint wave for same-name drift cases (`IndicatorRiver`, exploitation-rate family, benchmark/reference subtypes).
- No full bridge-module extraction; existing terms remain local with conservative alignment links.
- No broad docs regeneration via WIDOCO in this pass.

## Why this is passable

- Aligns with shared-layer direction without forcing risky semantic cutovers.
- Keeps corrected DFO-local semantics intact.
- Makes the repo boundary claims and ontology reality consistent enough for follow-on PRs.
