# Issue #40 — Process-branch disconnect reproduction and bridge verification

## Scope

Issue: <https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/40>

Goal: verify the process-branch disconnect on `origin/main`, then confirm the minimal bridge patch reconnects process classes to assessment/measurement/reference-point classes.

## Reproduction method (schema-level graph walk)

`ontology/dfo-salmon.ttl` was parsed with `rdflib` and inspected as a class graph where edges come from object-property `rdfs:domain -> rdfs:range` axioms (including `owl:unionOf` expansions).

Process branch seed: `bfo:0000015` and all subclasses.

Targets checked:

- `gcdfo:StockAssessment`
- `gcdfo:ReferencePoint`
- `gcdfo:ObservedRateOrAbundance`
- `gcdfo:TargetOrLimitRateOrAbundance`
- `iao:0000109` (measurement datum)

## Baseline on `origin/main` (before patch)

Process subclasses detected (8):

- `bfo:0000015`
- `dwc:Event`
- `dwc:Occurrence`
- `dwc:Identification`
- `gcdfo:SurveyEvent`
- `gcdfo:EscapementSurveyEvent`
- `gcdfo:Escapement`
- `gcdfo:StockAssessment`

Object properties touching the process branch: **4**

- `gcdfo:hasFeatureOfInterest`
- `gcdfo:hasObservationResult`
- `gcdfo:hasObservedVariable`
- `gcdfo:usesObservationProcedure`

Reachability from process branch to targets (domain/range walk):

- `StockAssessment`: **False**
- `ReferencePoint`: **False**
- `ObservedRateOrAbundance`: **False**
- `TargetOrLimitRateOrAbundance`: **False**
- `iao:0000109`: **False**

Interpretation: process connectivity existed only around `SurveyEvent`, with no explicit bridge into core stock-assessment + management-reference structure.

## Patch verification (current branch)

New bridge properties introduced:

- `gcdfo:hasAssessmentSubject` / `gcdfo:isAssessmentSubjectOf`
- `gcdfo:usesAssessmentDatum` / `gcdfo:isDatumUsedInAssessment`
- `gcdfo:hasAssessmentReferencePoint` / `gcdfo:isAssessmentReferencePointFor`

Process-touching object properties after patch: **10**

Reachability from process branch to targets after patch:

- `StockAssessment`: **True**
- `ReferencePoint`: **True**
- `ObservedRateOrAbundance`: **True**
- `TargetOrLimitRateOrAbundance`: **True**
- `iao:0000109`: **True**

## Example inferable paths enabled

1. `gcdfo:SurveyEvent`
   → `gcdfo:hasObservationResult`
   → `gcdfo:EscapementMeasurement`
   → `gcdfo:isDatumUsedInAssessment`
   → `gcdfo:StockAssessment`

2. `gcdfo:StockAssessment`
   → `gcdfo:hasAssessmentSubject`
   → `gcdfo:ReportingOrManagementStratum` / `gcdfo:Population`

3. `gcdfo:StockAssessment`
   → `gcdfo:hasAssessmentReferencePoint`
   → `gcdfo:ReferencePoint`

This closes the process-branch disconnect described in #40 while keeping the bridge surface intentionally small.
