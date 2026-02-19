# Proposal: Extend DFO Salmon Ontology for `x_CU_Level_Metadata.csv` Controlled Vocabularies

## Scope

This proposal is based on reproducible extraction of categorical values from:

- `Metadata-Questionnaire-CU-Series/data/x_CU_Level_Metadata.csv`

Compared against:

- `dfo-salmon-ontology/ontology/dfo-salmon.ttl`

Generated artifacts:

- `cu_metadata_controlled_vocab_analysis.json`
- `cu_metadata_vocab_gaps.csv`
- `cu_metadata_controlled_vocab_report.md`

## Executive findings

1. Many metadata columns are controlled vocab candidates but currently have no direct lexical mapping in the ontology.
2. Highest-value gaps are **not** random free text: they cluster into recurring domain code lists (SMU names/groups, adaptive zones, life-history shorthand, benchmark method/source version labels, status grouping labels).
3. A substantial subset are likely **lexical aliases** rather than true new concepts (e.g., `Chinook` vs existing species labels, `Rel_Idx`/`Abs_Abd`, `80pSmsy` style benchmark notation).

## Recommended modeling pattern (per `docs/CONVENTIONS.md`)

- Use **SKOS ConceptSchemes** for code lists.
- Use **SKOS concepts** for each controlled value (`skos:prefLabel`, `skos:inScheme`, `skos:definition`, `rdfs:isDefinedBy`, optional `iao:0000119` + `dcterms:source`).
- Use **`skos:altLabel`** to absorb common lexical variants and shorthand codes.
- Keep compound variables/metrics as SKOS concepts and attach I-ADOPT decomposition via annotation properties where needed.

## Prioritized extension bundles

### Bundle A — Assessment grouping and stock-management labels (high priority)

**Columns driving this:**
- `StockMgmtUnit`
- `StockMgmtUnit_Group`
- `StatusGroup`

**Proposal:**
- Add `:StockManagementUnitGroupScheme` (if not present) and `:StatusGroupScheme`.
- Mint concepts for recurring group codes and region-run groupings (e.g., `SK-Fraser`, `CK-Yukon`, Fraser run-group labels).
- For long human-readable SMU names, use:
  - canonical `skos:prefLabel` = full human-readable name
  - shorthand code in `skos:altLabel` (and optionally `skos:notation` with a scheme datatype)

### Bundle B — Life history + adaptive zone code lists (high priority)

**Columns driving this:**
- `LifeHistoryType_General`
- `Freshwater_Adaptive_Zone`
- `Marine_Adaptive_Zone`

**Proposal:**
- Add/extend `:LifeHistoryTypeScheme` with coded values (`CK`, `SEL`, `PKO`, etc.) represented as notation/alt labels tied to expanded labels.
- Add `:FreshwaterAdaptiveZoneScheme` and `:MarineAdaptiveZoneScheme` for short zone codes (`MFR`, `LFR`, `STh`, etc.).
- Link these concepts to existing habitat/biogeography concepts where possible via `skos:closeMatch`.

### Bundle C — Benchmark method/source/version semantics (high priority)

**Columns driving this:**
- `Rel_LowerBM_BasedOn`
- `Rel_UpperBM_BasedOn`
- `Rel_LowerBM_Version`
- `Rel_UpperBM_Version`
- `RelBM_UsedFor`

**Proposal:**
- Add `:BenchmarkBasisScheme` (`Spawner-Recruit`, `Watershed Area`, `Lake Productivity`, etc.).
- Add `:BenchmarkVersionScheme` for shorthand versions (`80pSmsy`, `85pSmsy`, `40pSmax`, etc.).
- Add `:BenchmarkUseScopeScheme` (`Status`, `Reference Only`, `Not Used`, `Not Assessed`).

### Bundle D — Data source/process actor vocabularies (medium priority)

**Columns driving this:**
- `Spn_EstSource_General`
- `DataUpdate_ProcessType`
- `DataUpdate_DFOLead`

**Proposal:**
- Add `:SpawnerEstimateSourceScheme` with organization-level concepts (`DFO Science`, `Pacific Salmon Commission`, `Okanagan Nation Alliance`, etc.).
- Add `:DataUpdateProcessTypeScheme` for controlled process categories.
- For person-name-like values in `DataUpdate_DFOLead`, do **not** model as SKOS controlled vocabulary unless governance requires canonical person registry. Keep these as data values in instance data.

### Bundle E — Site adjustment and intervention categories (medium priority)

**Columns driving this:**
- `Site_Adj_General`
- `ActiveInterventions_*`

**Proposal:**
- Add `:SiteAdjustmentScheme` for concise categories (`Site selection`, `Infilling`, exclusions due to standards).
- Add `:ActiveInterventionScheme` for intervention types (`Spawning channel`, hatchery release classes).
- Keep long narrative justification in data, not ontology.

## Compare/contrast guidance: existing vs missing

### Likely existing concept, missing lexical bridge (`skos:altLabel` candidate)

- Species short labels: `Chinook`, `Sockeye`, `Coho`, `Chum`, `Pink`.
- WSP data-type labels: `Abs_Abd`, `Rel_Idx` (if canonical term exists, use alt labels/notation).
- Benchmark shorthand and variants with punctuation differences (e.g., `Same as lower BM` vs `Same as lower benchmark`).

### Likely genuinely missing concept (new SKOS concept candidate)

- Adaptive-zone code systems (`MFR`, `LFR`, etc.) if not represented already.
- Status grouping tokens (`SK-Fraser`, `CK-Yukon`, etc.) where they denote domain-specific grouping entities.
- Benchmark-use scope values (`Reference Only`, `Not Assessed`) if not yet in ontology.

## Reproducible workflow

Use:

```bash
python3 scripts/analyze_cu_metadata_controlled_vocab.py \
  --csv /Users/alan/.openclaw/workspace/Metadata-Questionnaire-CU-Series/data/x_CU_Level_Metadata.csv \
  --ttl /Users/alan/.openclaw/workspace/dfo-salmon-ontology/ontology/dfo-salmon.ttl \
  --outdir /Users/alan/.openclaw/workspace/dfo-salmon-ontology/analysis/cu-metadata-controlled-vocab
```

## Suggested next implementation step

Create a follow-on script to convert `cu_metadata_vocab_gaps.csv` into a staged Turtle patch template:

- one proposed ConceptScheme per selected bundle,
- concept stubs with required annotations,
- placeholders for definition/citation review.

This keeps term minting reviewable and repeatable as the source CSV evolves.
