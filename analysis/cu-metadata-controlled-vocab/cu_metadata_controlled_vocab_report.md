# CU Metadata Controlled Vocabulary Gap Analysis

- CSV: `/Users/alan/.openclaw/workspace/Metadata-Questionnaire-CU-Series/data/x_CU_Level_Metadata.csv`
- Ontology: `/Users/alan/.openclaw/workspace/dfo-salmon-ontology/ontology/dfo-salmon.ttl`
- Rows: **66**
- Columns scanned: **103**
- Categorical candidate columns analyzed: **57**
- Columns with at least one unmapped value: **36**

## Modeling strategy proposal (aligned with DFO conventions)

1. **Use SKOS ConceptSchemes for controlled value lists** (status/type/source/category/method fields).
2. **Use PascalCase term IRIs** and keep `rdfs:isDefinedBy`, `skos:prefLabel`, `skos:inScheme`, and `skos:definition`. Include `iao:0000119` and `dcterms:source` when provenance is available.
3. **Add `skos:altLabel` first** when a CSV value is a lexical variant of an existing ontology term.
4. **Mint new SKOS concepts** when no existing term semantically matches.
5. For metrics/compound variables, follow **I-ADOPT annotation pattern** in `docs/CONVENTIONS.md` (SKOS concept + decomposition annotations).
6. Keep schema-only ontology discipline: no instance data in ontology files.

## Top missing values (by frequency)

| Value | Count | Suggested term IRI local name |
|---|---:|---|
| `geomean` | 65 | `Geomean` |
| `regular` | 65 | `Regular` |
| `Link to SMU_Group Metadata` | 64 | `LinkToSmuGroupMetadata` |
| `Complete` | 64 | `Complete` |
| `Same as lower benchmark` | 63 | `SameAsLowerBenchmark` |
| `Spawner-Recruit` | 58 | `SpawnerRecruit` |
| `GStr` | 51 | `Gstr` |
| `Fraser` | 50 | `Fraser` |
| `Abs_Abd` | 46 | `AbsAbd` |
| `Status` | 37 | `Status` |
| `Chinook` | 32 | `Chinook` |
| `Sgen` | 32 | `Sgen` |
| `Same` | 30 | `Same` |
| `Same as lower BM` | 28 | `SameAsLowerBm` |
| `Sockeye` | 25 | `Sockeye` |
| `SK-Fraser` | 24 | `SkFraser` |
| `Fraser-BCI Sockeye Analytical Program` | 23 | `FraserBciSockeyeAnalyticalProgram` |
| `DFO` | 22 | `Dfo` |
| `SEL` | 21 | `Sel` |
| `Fraser-BCI Sockeye Analytical Program Lead` | 21 | `FraserBciSockeyeAnalyticalProgramLead` |
| `DFO Fraser-BCI Stock Assessment Sockeye Analytical staff` | 20 | `DfoFraserBciStockAssessmentSockeyeAnalyticalStaff` |
| `CK` | 19 | `Ck` |
| `Different` | 19 | `Different` |
| `Fraser Chinook` | 18 | `FraserChinook` |
| `CK-Fraser` | 17 | `CkFraser` |
| `DFO Area StAD` | 16 | `DfoAreaStad` |
| `80pSmsy` | 16 | `V80psmsy` |
| `Rel_Idx` | 16 | `RelIdx` |
| `MFR` | 14 | `Mfr` |
| `Watershed Area` | 13 | `WatershedArea` |
| `85pSmsy` | 13 | `V85psmsy` |
| `Stream-type Chinook` | 12 | `StreamTypeChinook` |
| `LFR` | 12 | `Lfr` |
| `Ber` | 12 | `Ber` |
| `Yukon` | 12 | `Yukon` |
| `CK-Yukon` | 12 | `CkYukon` |
| `None Available` | 12 | `NoneAvailable` |
| `Watershed Area?` | 12 | `WatershedArea` |
| `Yukon River Senior Biologist (Adam O'Dell)` | 12 | `YukonRiverSeniorBiologistAdamODell` |
| `Area staff generate annual update.` | 11 | `AreaStaffGenerateAnnualUpdate` |

## Column-level comparison

### `AbdMetric`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `AbsAbdMetric`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `ActiveInterventions_DataAdjustmentsFlag`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `ActiveInterventions_DataAdjustmentsType`

- Unique values: **3**
- Matched values: **0**
- Missing values: **1**
- Proposed scheme: `:TypeScheme`
- Missing preview: `Exclude estimated share of hatchery-origin fish`

### `ActiveInterventions_Flag`

- Unique values: **4**
- Matched values: **0**
- Missing values: **1**
- Proposed scheme: `:ActiveinterventionsFlagScheme`
- Missing preview: `Spawning channel`

### `ActiveInterventions_General`

- Unique values: **4**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:ActiveinterventionsGeneralScheme`
- Missing preview: `Release of hatchery-origin juveniles`, `Spawning channel started operations in 1965`

### `AvgGen_Trends`

- Unique values: **5**
- Matched values: **0**
- Missing values: **3**
- Proposed scheme: `:AvggenTrendsScheme`
- Missing preview: `Highly Stable`, `Slight increase in age-at-maturity`, `Stable age composition`

### `AvgGen_Variability`

- Unique values: **4**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:AvggenVariabilityScheme`
- Missing preview: `Highly Stable`, `Low`

### `AvgRecentExcl`

- Unique values: **2**
- Matched values: **0**
- Missing values: **0**

### `AvgSmooth`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `AvgType`

- Unique values: **2**
- Matched values: **0**
- Missing values: **1**
- Proposed scheme: `:TypeScheme`
- Missing preview: `geomean`

### `CU_Status_Assessed`

- Unique values: **2**
- Matched values: **0**
- Missing values: **0**

### `CU_Verification`

- Unique values: **2**
- Matched values: **0**
- Missing values: **0**

### `Cyc_Dom`

- Unique values: **4**
- Matched values: **0**
- Missing values: **0**

### `Cyc_Dom_Year`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Cyclic`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Cyclic_DUPLICATE`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `DFORegion`

- Unique values: **5**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:DforegionScheme`
- Missing preview: `Fraser`, `Okanagan`, `SouthCoast`, `Yukon`

### `DataQualkIdx`

- Unique values: **3**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:DataqualkidxScheme`
- Missing preview: `Abs_Abd`, `Rel_Idx`

### `DataUpdate_DFOLead`

- Unique values: **6**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:DataupdateDfoleadScheme`
- Missing preview: `Fraser Chinook Coho Analytical Lead`, `Fraser Chum Lead`, `Fraser-BCI Sockeye Analytical Program`, `Yukon Chinook Bio`

### `DataUpdate_ProcessType`

- Unique values: **5**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:TypeScheme`
- Missing preview: `Area staff generate annual update.`, `Area staff generate update`, `Compile survey results locally`, `Rerun the Bayesian Model`

### `Freshwater_Adaptive_Zone`

- Unique values: **18**
- Matched values: **0**
- Missing values: **16**
- Proposed scheme: `:FreshwaterAdaptiveZoneScheme`
- Missing preview: `BB`, `FRCany`, `FRCany + LFR`, `LFR`, `LFR + LILL`, `LILL`, `LTh`, `LTh + Nth`, `MFR`, `NTh`, `OK`, `STh`

### `LifeHistoryType_General`

- Unique values: **9**
- Matched values: **0**
- Missing values: **8**
- Proposed scheme: `:TypeScheme`
- Missing preview: `CK`, `CM`, `CO`, `Lake-type Sockeye`, `PKO`, `RT`, `SEL`, `Stream-type Chinook`

### `LifeHistory_DominantAgeClass`

- Unique values: **2**
- Matched values: **0**
- Missing values: **1**
- Proposed scheme: `:LifehistoryDominantageclassScheme`
- Missing preview: `4sub2`

### `Location_Rearing_Type`

- Unique values: **5**
- Matched values: **2**
- Missing values: **1**
- Proposed scheme: `:TypeScheme`
- Missing preview: `Ocean`

### `Location_Spawning_Type`

- Unique values: **4**
- Matched values: **2**
- Missing values: **0**

### `LongTrendMetric`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Marine_Adaptive_Zone`

- Unique values: **4**
- Matched values: **0**
- Missing values: **3**
- Proposed scheme: `:MarineAdaptiveZoneScheme`
- Missing preview: `Ber`, `GStr`, `ORWA`

### `PercentileMetric`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `RelAbd_AvgData`

- Unique values: **2**
- Matched values: **0**
- Missing values: **1**
- Proposed scheme: `:RelabdAvgdataScheme`
- Missing preview: `regular`

### `RelBM_UsedFor`

- Unique values: **7**
- Matched values: **0**
- Missing values: **6**
- Proposed scheme: `:RelbmUsedforScheme`
- Missing preview: `None Available`, `None Available??`, `Not Assessed`, `Not Used`, `Reference Only`, `Status`

### `Rel_LowerBM_BasedOn`

- Unique values: **9**
- Matched values: **0**
- Missing values: **6**
- Proposed scheme: `:RelLowerbmBasedonScheme`
- Missing preview: `Lake Productivity`, `Spawner-Recruit`, `Spawning Habitat Capacity`, `Watershed Area`, `Watershed Area; Spawner-Recruit`, `Watershed Area?`

### `Rel_LowerBM_Version`

- Unique values: **7**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:RelLowerbmVersionScheme`
- Missing preview: `20pSmax`, `Sgen`, `Sgen for Dominant Cycle`, `Sgen?`

### `Rel_UpperBM_BasedOn`

- Unique values: **9**
- Matched values: **0**
- Missing values: **6**
- Proposed scheme: `:RelUpperbmBasedonScheme`
- Missing preview: `Lake Productivity`, `Spawner-Recruit`, `Spawning habitat capacity`, `Watershed Area`, `Watershed Area; Spawner-Recruit`, `Watershed Area?`

### `Rel_UpperBM_MethodNotes`

- Unique values: **4**
- Matched values: **0**
- Missing values: **3**
- Proposed scheme: `:MethodScheme`
- Missing preview: `No available data for estimating rel abd BMs`, `Same as lower BM`, `Same as lower benchmark`

### `Rel_UpperBM_Version`

- Unique values: **7**
- Matched values: **0**
- Missing values: **5**
- Proposed scheme: `:RelUpperbmVersionScheme`
- Missing preview: `40pSmax`, `80pSmsy`, `80pSmsy for Dominant Cycle`, `80pSmsy?`, `85pSmsy`

### `Rel_UpperBM_VersionRationale`

- Unique values: **6**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:RelUpperbmVersionrationaleScheme`
- Missing preview: `Same as lower BM`, `Same as lower benchmark`, `Used 85p of Smsy for consistency with other Chinook status assessments.`, `Used default benchmark when appropriate SR model fits available.`

### `ShortTrendMetric`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Site_Adj_General`

- Unique values: **11**
- Matched values: **0**
- Missing values: **6**
- Proposed scheme: `:SiteAdjGeneralScheme`
- Missing preview: `Any low quality sites excluded????`, `Site selection`, `Site selection; infilling`, `Sites that don't meet site-level data standards`, `Sites that don't meet site-level data standards and sites with high enhancement classification were excluded.`, `Sites that don't meet site-level data standards were excluded.`

### `Site_Based`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Site_Records_Source_General`

- Unique values: **4**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:SourceScheme`
- Missing preview: `DFO`, `Okanagan Nation Alliance`

### `Site_Verification`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Site_Verification_nuSEDS_Match`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

### `Species`

- Unique values: **5**
- Matched values: **0**
- Missing values: **5**
- Proposed scheme: `:SpeciesScheme`
- Missing preview: `Chinook`, `Chum`, `Coho`, `Pink`, `Sockeye`

### `Spn_Coverage_QualAbd`

- Unique values: **5**
- Matched values: **0**
- Missing values: **3**
- Proposed scheme: `:SpnCoverageQualabdScheme`
- Missing preview: `Any guesses?`, `Estimates don't cover full CU; but expert consensus that total spawner abundance consistently well below 1500.`, `Expert consensus that Nahatlatch accounts for almost all the spawners.`

### `Spn_EstSource_General`

- Unique values: **7**
- Matched values: **0**
- Missing values: **5**
- Proposed scheme: `:SourceScheme`
- Missing preview: `DFO Area StAD`, `DFO Fraser-BCI Stock Assessment Sockeye Analytical staff`, `DFO Science`, `Okanagan Nation Alliance`, `Pacific Salmon Commission`

### `Spn_EstUnc_Type`

- Unique values: **5**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:TypeScheme`
- Missing preview: `Assumed CV`, `Bayesian Posterior`

### `Spn_TrendVsAbd`

- Unique values: **3**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:SpnTrendvsabdScheme`
- Missing preview: `Different`, `Same`

### `StatusGroup`

- Unique values: **11**
- Matched values: **0**
- Missing values: **10**
- Proposed scheme: `:StatusScheme`
- Missing preview: `CK-Columbia`, `CK-Fraser`, `CK-Inner_South_Coast`, `CK-Yukon`, `CM-Fraser_Lower`, `CO-Fraser_Int`, `CO-Fraser_Low`, `PK_Fraser`, `SK-Fraser`, `SK-Okanagan`

### `StatusProcess_AssessmentContact`

- Unique values: **5**
- Matched values: **0**
- Missing values: **4**
- Proposed scheme: `:StatusScheme`
- Missing preview: `Athena Ogden (DFO)`, `Dylan Glaser (DFO)`, `Fraser-BCI Sockeye Analytical Program Lead`, `Yukon River Senior Biologist (Adam O'Dell)`

### `StatusProcess_AssessmentStage`

- Unique values: **3**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:StatusScheme`
- Missing preview: `??? REMOVED???`, `Complete`

### `StatusProcess_LatestStatusYear`

- Unique values: **2**
- Matched values: **0**
- Missing values: **0**

### `StockMgmtUnit`

- Unique values: **19**
- Matched values: **0**
- Missing values: **17**
- Proposed scheme: `:StockmgmtunitScheme`
- Missing preview: `FRASER CHUM SALMON`, `FRASER FALL RUN 41 CHINOOK SALMON`, `FRASER PINK SALMON - ODD`, `FRASER SOCKEYE SALMON - EARLY STUART`, `FRASER SOCKEYE SALMON - EARLY SUMMER`, `FRASER SOCKEYE SALMON - LATE`, `FRASER SOCKEYE SALMON - SUMMER`, `FRASER SPRING RUN 42 CHINOOK SALMON`, `FRASER SPRING RUN 52 CHINOOK SALMON`, `FRASER SUMMER RUN 41 CHINOOK SALMON`, `FRASER SUMMER RUN 52 CHINOOK SALMON`, `INTERIOR FRASER COHO SALMON`

### `StockMgmtUnit_Group`

- Unique values: **7**
- Matched values: **0**
- Missing values: **5**
- Proposed scheme: `:StockmgmtunitGroupScheme`
- Missing preview: `Fraser Chinook`, `Fraser Chum`, `Fraser Coho`, `Fraser Sockeye`, `Okanagan Chinook`

### `StockMgmtUnit_MatchRationale`

- Unique values: **3**
- Matched values: **0**
- Missing values: **2**
- Proposed scheme: `:StockmgmtunitMatchrationaleScheme`
- Missing preview: `Link to SMU_Group Metadata`, `NEED RATIONALE`

### `TrendLog`

- Unique values: **2**
- Matched values: **0**
- Missing values: **0**

### `TrendSmooth`

- Unique values: **3**
- Matched values: **0**
- Missing values: **0**

## Reproducibility

Re-run with:

```bash
python3 scripts/analyze_cu_metadata_controlled_vocab.py --csv /Users/alan/.openclaw/workspace/Metadata-Questionnaire-CU-Series/data/x_CU_Level_Metadata.csv --ttl /Users/alan/.openclaw/workspace/dfo-salmon-ontology/ontology/dfo-salmon.ttl --outdir /Users/alan/.openclaw/workspace/dfo-salmon-ontology/analysis/cu-metadata-controlled-vocab
```