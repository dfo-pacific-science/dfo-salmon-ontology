# Extraction Frame Use Cases (alpha 0.0.6)

This note shows how to apply the extraction-frame model to common salmon assessment workflows. Keep extraction order consistent: **Entity + Event/Observation first**, then **Variable decomposition**, then **Method/Protocol + Constraint/StatModifier**, then publish **Result/Provenance**.

## Canonical extraction categories

- **Entity**: What the record is about (e.g., Stock, CU, SMU, Indicator River, fishery, cohort).
- **Property**: Stable descriptors of an entity (e.g., species, run timing, management stratum, year basis type).
- **Variable**: Measured or derived quantity (count, rate, index, benchmark ratio, score).
- **Constraint/StatModifier**: Qualifiers that control interpretation (target/limit, confidence, uncertainty, data-quality class, censoring/imputation flags).
- **Method/Protocol**: How values were produced (enumeration method, estimate method, lab assay, model algorithm/version).
- **Event/Observation**: When/where data were observed or computed (survey event, sample event, analysis run, stock assessment event).
- **Result/Provenance**: Final value package + lineage (value, unit, interval, source dataset, code/version, analyst/run).

## High-level use cases

### 1) Escapement
- **What to extract first:** stock/river (Entity), return year (Property), and `SurveyEvent`/`EscapementSurveyEvent` (Event/Observation).
- **Variable decomposition:** observed spawner count, expanded count (if used), infill component (if used), final escapement estimate.
- **Event/protocol anchors:** enumeration method, estimate method, effort standardization status, survey window.
- **Expected outputs:** `EscapementMeasurement` result with value, uncertainty (if available), year basis, method tags, and source/provenance links.

### 2) Exploitation rate
- **What to extract first:** stock + assessment period + catch/removal observations and return/escapement observations.
- **Variable decomposition:** numerator = catch/removals; denominator = total return (catch + escapement or workflow-specific equivalent); derived observed rate; optional target/limit rate.
- **Event/protocol anchors:** fishery accounting event, run reconstruction or stock-assessment method, year-basis alignment.
- **Expected outputs:** `ObservedExploitationRate` (and optional `TargetOrLimitExploitationRate`) with formula basis, period, and provenance to input series.

### 3) Age composition
- **What to extract first:** sampled stock/stratum, sample event, sample size, and ageing basis/notation context.
- **Variable decomposition:** age class counts -> age proportions; plus basis terms (age-at-return vs age-at-sampling) and notation/dimension.
- **Event/protocol anchors:** biological sampling event, ageing protocol (e.g., scale/otolith), subsampling rules.
- **Expected outputs:** age-composition result set per stock-year (counts + proportions + sample-size metadata) with protocol and QA provenance.

### 4) GSI (genetic stock identification)
- **What to extract first:** sample batch identity, reporting unit(s), analysis run identity, and baseline/reference version.
- **Variable decomposition:** assignment proportions by stock group, effective sample size, uncertainty terms (CI or assignment error where available).
- **Event/protocol anchors:** sample collection event, lab/genotyping protocol, GSI analysis run configuration.
- **Expected outputs:** GSI composition results by reporting unit with uncertainty, baseline reference, and run-level provenance.

### 5) Rapid-status metric
- **What to extract first:** CU/assessment unit, assessment year, metric family (e.g., trend/ratio/percentile), and benchmark context.
- **Variable decomposition:** input abundance series -> derived metric(s) (e.g., generational average, benchmark ratio, percent change, score) -> threshold comparison.
- **Event/protocol anchors:** `StockAssessment` / rapid-status run, algorithm version, parameter set, threshold source.
- **Expected outputs:** metric values plus status-ready interpretation objects (zone/confidence/score context) and full computational provenance.

### 6) Environmental covariate
- **What to extract first:** covariate type (e.g., discharge, SST, PDO index), spatial anchor, temporal window, and stock life-stage linkage.
- **Variable decomposition:** raw series -> aggregation window -> lag/anomaly/standardized covariate used in model.
- **Event/protocol anchors:** monitoring/sensor observation event, data product version, transformation protocol.
- **Expected outputs:** covariate series aligned to assessment year basis (brood/return/catch year as specified) with transform metadata and source provenance.

### 7) Survey effort normalization
- **What to extract first:** raw observation counts plus effort descriptors (hours, distance, passes, area sampled) by survey event.
- **Variable decomposition:** raw count + effort term -> normalized index (e.g., CPUE or effort-adjusted abundance), with expansion factors if applied.
- **Event/protocol anchors:** `SurveyEvent`, enumeration protocol, effort-standardization method/class.
- **Expected outputs:** effort-normalized comparability-ready index values with explicit normalization equation, parameters, and provenance.
