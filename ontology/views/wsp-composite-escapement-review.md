# WSP composite-escapement review pack

This file is the human review surface for Wild Salmon Policy composite-escapement semantics. It complements `wsp-composite-escapement-view.ttl`; it does not replace the authoritative ontology definitions in `ontology/dfo-salmon.ttl`.

## Why this exists

WebVowl is a poor fit for this review problem because the important content is source-field mapping, SKOS concepts, and light one-level-up context rather than rich OWL class hierarchies. Use this Markdown file for discussion and the GraphML file for picture-based review in yEd.

## Files

- `ontology/views/wsp-composite-escapement-view.ttl` — machine-readable curated Turtle view
- `ontology/views/wsp-composite-escapement-review.md` — human review file
- `ontology/views/wsp-composite-escapement-review.graphml` — yEd/yEd Live graph

## Graph legend

| Node type | Color | Meaning |
| --- | --- | --- |
| Source field | yellow | Canonical WSP composite-escapement source column |
| Modeled canonical term | blue | First-class DFO Salmon Ontology term added or used to represent canonical WSP output semantics |
| WSP context term | orange | Wild Salmon Policy-themed DFO context term kept one level up for review |
| Salmon Domain Ontology term | green | Shared Salmon Domain context term |
| Scheme | pink | Scheme / grouping concept |
| External reference | gray | External semantics such as DwC/QUDT/SKOS |

## Coverage summary

- Source fields in canonical composite-escapement output: **37**
- Source fields mapped in the review view: **35**
- Source fields still explicitly unmapped: **2** (`CU_ID`, `Year`)
- Curated WSP review terms: **50**
- Modeled canonical WSP output terms: **21**

## Review hotspots

- `CU_ID` and `Year` remain intentionally unmapped.
- `DataType`, `BinLabel`, and `BinPath` are still helper-ish and may not deserve full ontology treatment.
- `IntStatus5`, `IntStatus3`, and `IntStatus2` remain in the graph because they are legacy output columns that colleagues may still recognize.
- The GraphML intentionally keeps only one-level-up context so the picture stays readable.

## Source-column mapping table

| Source field | Status | Mapped term | Property | Entity | Constraint | Unit | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AbsAbdCat | mapped | gcdfo:AbsoluteAbundanceMetricStatus |  |  |  |  |  |
| AbsLBM | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit | gcdfo:LowerBenchmark | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| AbsUBM | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit | gcdfo:UpperBenchmark | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| BinLabel | mapped | gcdfo:WSPRapidStatus |  |  |  |  |  |
| BinPath | mapped | gcdfo:WSPRapidStatus |  |  |  |  |  |
| ConfidenceRating | mapped | gcdfo:ConfidenceCategory |  | gcdfo:ConservationUnit |  |  |  |
| CU_ID | unmapped-in-current-wsp_column_dictionary |  |  |  |  |  | No explicit ontology mapping is currently asserted for this source variable in data_demo/SDP_Templates/wsp_column_dictionary.csv. |
| DataType | mapped | skos:Concept |  | gcdfo:ConservationUnit |  |  |  |
| GenAvgSpnForAbd | mapped | dwc:individualCount | quantitykind:Count | gcdfo:ConservationUnit | smn:NaturalOrigin | unit:NUM | legacy: https://w3id.org/gcdfo/salmon#NaturalOrigin |
| IntStatus2 | mapped | gcdfo:IntegratedStatusBinary |  |  |  |  |  |
| IntStatus3 | mapped | gcdfo:IntegratedStatusThreeCategory |  |  |  |  |  |
| IntStatus5 | mapped | gcdfo:IntegratedStatusFiveCategoryAlias |  |  |  |  |  |
| IntStatus_Short | mapped | gcdfo:IntegratedStatusCollapsedCode |  |  |  |  |  |
| IntStatusRaw | mapped | gcdfo:IntegratedStatusRaw |  |  |  |  |  |
| IntStatusRaw_Short | mapped | gcdfo:IntegratedStatusRawCode |  |  |  |  |  |
| LongTrend | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit |  | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| LongTrendCat | mapped | gcdfo:LongTermTrendMetricStatus |  |  |  |  |  |
| PercChange | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit |  | unit:PERCENT | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| PercChangeCat | mapped | gcdfo:PercentChangeMetricStatus |  |  |  |  |  |
| Percentile | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit |  | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| PercentileCat | mapped | gcdfo:AbundancePercentileMetricStatus |  |  |  |  |  |
| ProbDeclBelowLBM | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit |  | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| ProbDeclBelowLBMCat | mapped | gcdfo:ProbabilityDeclineBelowLowerBenchmarkMetricStatus |  |  |  |  |  |
| RapidScore | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit |  | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| RapidStatus | mapped | gcdfo:WSPRapidStatus |  | gcdfo:ConservationUnit |  |  |  |
| RelAbd_LBM | mapped | gcdfo:LowerBiologicalBenchmark | quantitykind:Count | gcdfo:ConservationUnit | gcdfo:LowerBenchmark | unit:NUM |  |
| RelAbd_UBM | mapped | gcdfo:UpperBiologicalBenchmark | quantitykind:Count | gcdfo:ConservationUnit | gcdfo:UpperBenchmark | unit:NUM |  |
| RelAbdCat | mapped | gcdfo:RelativeAbundanceMetricStatus |  |  |  |  |  |
| RelLBM | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit | gcdfo:LowerBenchmark | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| RelUBM | mapped | smn:ObservedRateOrAbundance | quantitykind:DimensionlessRatio | gcdfo:ConservationUnit | gcdfo:UpperBenchmark | unit:UNITLESS | legacy: https://w3id.org/gcdfo/salmon#ObservedRateOrAbundance |
| Species | mapped | gcdfo:Species |  |  |  |  |  |
| SpnForAbd_Total | mapped | dwc:individualCount | quantitykind:Count | gcdfo:ConservationUnit |  | unit:NUM |  |
| SpnForAbd_Wild | mapped | dwc:individualCount | quantitykind:Count | gcdfo:ConservationUnit | smn:NaturalOrigin | unit:NUM | legacy: https://w3id.org/gcdfo/salmon#NaturalOrigin |
| SpnForTrend_Total | mapped | dwc:individualCount | quantitykind:Count | gcdfo:ConservationUnit |  | unit:NUM |  |
| SpnForTrend_Wild | mapped | dwc:individualCount | quantitykind:Count | gcdfo:ConservationUnit | smn:NaturalOrigin | unit:NUM | legacy: https://w3id.org/gcdfo/salmon#NaturalOrigin |
| Stock | mapped | gcdfo:ConservationUnitName |  |  |  |  |  |
| Year | unmapped-in-current-wsp_column_dictionary |  |  |  |  |  | No explicit ontology mapping is currently asserted for this source variable in data_demo/SDP_Templates/wsp_column_dictionary.csv. |

## Modeled canonical WSP output terms

| Term | Deprecated | Broader / scheme | Entity | Property | Constraint | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Absolute abundance metric status (`gcdfo:AbsoluteAbundanceMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:LowerBiologicalBenchmark, gcdfo:UpperBiologicalBenchmark | Absolute abundance status uses 1,000 and 10,000 spawner thresholds under current WSP guidance. |
| Abundance percentile metric status (`gcdfo:AbundancePercentileMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:WSPBiologicalStatusZone | Canonical approved outputs contain non-NA values despite stale variable-description text indicating NA. |
| Amber/Green integrated status (`gcdfo:IntegratedStatusAmberGreen`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| Collapsed integrated status code (`gcdfo:IntegratedStatusCollapsedCode`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:IntegratedStatusOutcome |  | Observed canonical codes include R, A, G, DD, and UD. |
| Conservation Unit name (`gcdfo:ConservationUnitName`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit |  |  | The canonical WSP output column is labelled Stock but currently carries CU names. Entity-level stock semantics are represented with smn:Stock. |
| Data deficient integrated status (`gcdfo:IntegratedStatusDataDeficient`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| Integrated status (3-category collapsed) (`gcdfo:IntegratedStatusThreeCategory`) | yes | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:IntegratedStatusOutcome | gcdfo:WildSalmonPolicy | deprecated |
| Integrated status (5-category legacy alias) (`gcdfo:IntegratedStatusFiveCategoryAlias`) | yes | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme |  |  |  | Canonical variable descriptions mark this field as to be removed.<br>deprecated |
| Integrated status (binary red/not-red) (`gcdfo:IntegratedStatusBinary`) | yes | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:IntegratedStatusOutcome | gcdfo:WildSalmonPolicy | deprecated |
| Integrated status (raw) (`gcdfo:IntegratedStatusRaw`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:IntegratedStatusOutcome | gcdfo:WildSalmonPolicy | Observed canonical values include Red, Amber, Green, RedAmber, AmberGreen, DD, and UD. |
| Integrated status outcome (`gcdfo:IntegratedStatusOutcome`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| Long-term trend metric status (`gcdfo:LongTermTrendMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:WSPBiologicalStatusZone | Operational thresholds are typically 0.50 (lower) and 0.75 (upper) of long-term average abundance. |
| Not-red integrated status (`gcdfo:IntegratedStatusNotRed`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| Percent change metric status (`gcdfo:PercentChangeMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:WSPBiologicalStatusZone | Operational thresholds in current rapid-status implementations commonly use -25% and -15% boundaries. |
| Probability-of-decline-below-lower-benchmark metric status (`gcdfo:ProbabilityDeclineBelowLowerBenchmarkMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:LowerBiologicalBenchmark | Canonical approved output currently records this field as NA and variable metadata labels it as not currently in use. |
| Raw integrated status code (`gcdfo:IntegratedStatusRawCode`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:IntegratedStatusOutcome |  | Observed canonical codes include R, RA, A, AG, G, DD, and UD. |
| Red/Amber integrated status (`gcdfo:IntegratedStatusRedAmber`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| Relative abundance metric status (`gcdfo:RelativeAbundanceMetricStatus`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit | gcdfo:WSPBiologicalStatusZone | gcdfo:LowerBiologicalBenchmark, gcdfo:UpperBiologicalBenchmark |  |
| Species (`gcdfo:Species`) | no | gcdfo:WSPOutputVariable; gcdfo:WSPOutputVariableScheme | gcdfo:ConservationUnit |  |  | Use taxonomic IRIs (for example DwC/GBIF/ITIS) where available; canonical approved outputs currently use common-name strings such as Chinook, Sockeye, Coho, Chum, and Pink. |
| Undetermined integrated status (`gcdfo:IntegratedStatusUndetermined`) | no | gcdfo:IntegratedStatusOutcomeScheme |  |  |  |  |
| WSP output variable (`gcdfo:WSPOutputVariable`) | no | gcdfo:WSPOutputVariableScheme |  |  |  |  |

## One-level-up WSP context kept in the graph

| Term | Role in graph |
| --- | --- |
| Abundance percentile metric (`gcdfo:AbundancePercentileMetric`) | WSP-specific context term |
| Amber zone (`gcdfo:AmberZone`) | WSP-specific context term |
| Benchmark ratio metric (`gcdfo:BenchmarkRatioMetric`) | WSP-specific context term |
| Biological Benchmark and Indicator Scheme (`gcdfo:BiologicalBenchmarkAndIndicatorScheme`) | scheme / grouping context |
| Confidence category (`gcdfo:ConfidenceCategory`) | WSP-specific context term |
| Conservation Unit (`gcdfo:ConservationUnit`) | WSP-specific context term |
| Green zone (`gcdfo:GreenZone`) | WSP-specific context term |
| High confidence (`gcdfo:RapidStatusConfidenceHigh`) | WSP-specific context term |
| Integrated status outcome scheme (`gcdfo:IntegratedStatusOutcomeScheme`) | scheme / grouping context |
| Long-term trend metric (`gcdfo:LongTermTrendMetric`) | WSP-specific context term |
| Low confidence (`gcdfo:RapidStatusConfidenceLow`) | WSP-specific context term |
| Lower benchmark (`gcdfo:LowerBenchmark`) | WSP-specific context term |
| Lower biological benchmark (`gcdfo:LowerBiologicalBenchmark`) | WSP-specific context term |
| Medium confidence (`gcdfo:RapidStatusConfidenceMedium`) | WSP-specific context term |
| Percent change metric (`gcdfo:PercentChangeMetric`) | WSP-specific context term |
| Policy framework scheme (`gcdfo:PolicyFrameworkScheme`) | scheme / grouping context |
| Probability of decline below lower benchmark metric (`gcdfo:ProbabilityDeclineBelowLowerBenchmarkMetric`) | WSP-specific context term |
| Rapid status confidence scheme (`gcdfo:RapidStatusConfidenceScheme`) | scheme / grouping context |
| Rapid status metric (`gcdfo:RapidStatusMetric`) | WSP-specific context term |
| Rapid status metric scheme (`gcdfo:RapidStatusMetricScheme`) | scheme / grouping context |
| Red zone (`gcdfo:RedZone`) | WSP-specific context term |
| Upper benchmark (`gcdfo:UpperBenchmark`) | WSP-specific context term |
| Upper biological benchmark (`gcdfo:UpperBiologicalBenchmark`) | WSP-specific context term |
| Wild Salmon Policy (`gcdfo:WildSalmonPolicy`) | WSP-specific context term |
| Wild Salmon Policy biological status zone (`gcdfo:WSPBiologicalStatusZone`) | WSP-specific context term |
| Wild Salmon Policy Status Zone (`gcdfo:WSPBiologicalStatusZoneScheme`) | scheme / grouping context |
| WSP output variable scheme (`gcdfo:WSPOutputVariableScheme`) | scheme / grouping context |
| WSP rapid status (`gcdfo:WSPRapidStatus`) | WSP-specific context term |
| WSP rapid-status assessment method (`gcdfo:WSPRapidStatusAssessmentMethod`) | WSP-specific context term |
