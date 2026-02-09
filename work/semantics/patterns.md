# SPSR measurement patterns (canonical)

_Generated from `column_dictionary.csv` on 2026-02-09._

This is the canonical pattern view for SPSR in `smn-data-gpt/assessments/spsr`.

## Entity defaults (by table prefix)
- `smu_*` → `https://w3id.org/gcdfo/salmon#StockManagementUnit`
- `cu_*`, `cuyear`, `custatus` → `https://w3id.org/gcdfo/salmon#ConservationUnit`
- `pfma_*` → `https://w3id.org/gcdfo/salmon#Stock`
- `pop_*`, `population`, `indicator_*` → `https://w3id.org/gcdfo/salmon#Population` (tracked in ontology PR #31 context)

## Pattern inventory

| Pattern | Unique columns | Rows | Dominant term(s) | Dominant property/unit | Missing `term_iri` rows | Example columns |
|---|---:|---:|---|---|---:|---|
| Catch totals by location | 4 | 14 | `http://rs.tdwg.org/dwc/terms/individualCount` (14) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `mainstem_catch, ocean_catch, terminal_catch …` |
| Spawner totals | 2 | 8 | `http://rs.tdwg.org/dwc/terms/individualCount` (8) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 0 | `spawners, total_spawners` |
| Run-size totals by location | 6 | 19 | `http://rs.tdwg.org/dwc/terms/individualCount` (19) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `ocean_run_size, terminal_run_size, total_ocean_run …` |
| Exploitation rates | 4 | 12 | `https://w3id.org/gcdfo/salmon#TotalExploitationRate` (6), `https://w3id.org/gcdfo/salmon#ExploitationRate` (6) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 0 | `er, ocean_exploitation_rate, total_exploitation_rate …` |
| Age spawner counts | 7 | 35 | `http://rs.tdwg.org/dwc/terms/individualCount` (35) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 0 | `spawners_age_1, spawners_age_2, spawners_age_3 …` |
| Age run counts | 7 | 28 | `http://rs.tdwg.org/dwc/terms/individualCount` (28) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `run_age_1, run_age_2, run_age_3 …` |
| Age catch counts | 7 | 28 | `http://rs.tdwg.org/dwc/terms/individualCount` (28) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `catch_age_1, catch_age_2, catch_age_3 …` |
| Age-location counts | 21 | 63 | `http://rs.tdwg.org/dwc/terms/individualCount` (63) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `mainstem_age_1, mainstem_age_2, mainstem_age_3 …` |
| Reference / benchmark points | 4 | 16 | `https://w3id.org/gcdfo/salmon#LowerBiologicalBenchmark` (8), `https://w3id.org/gcdfo/salmon#UpperBiologicalBenchmark` (8) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 0 | `lower_bio_benchmark, lower_wsp_benchmark, upper_bio_benchmark …` |
| Mortality / survival rates | 6 | 10 | `<MISSING>` (10) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 10 | `cwt_marine_survival_rate, in_river_mortality_rate, mainstem_mortality_rate …` |
| Recruit counts | 1 | 3 | `http://rs.tdwg.org/dwc/terms/individualCount` (3) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `recruits` |
| Hatchery-origin indicators | 2 | 2 | `<MISSING>` (1), `https://w3id.org/gcdfo/salmon#HatcheryOrigin` (1) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 1 | `hatchery_origin_broodstock, phos` |
| Broodstock removals | 1 | 1 | `http://rs.tdwg.org/dwc/terms/individualCount` (1) | `http://qudt.org/vocab/quantitykind/Count` / `http://qudt.org/vocab/unit/NUM` | 0 | `total_broodstock_removed` |
| Marine survival index | 1 | 2 | `<MISSING>` (2) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 2 | `marine_survival_index` |
| Expansion factors | 1 | 1 | `<MISSING>` (1) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 1 | `expansion_factor` |
| Spawner abundance indicators | 16 | 16 | `<MISSING>` (16) | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` / `http://qudt.org/vocab/unit/UNITLESS` | 16 | `relative_hatchery_spawner_abundance, relative_hatchery_spawner_abundance_change, relative_hatchery_spawner_abundance_percentile …` |

## Coherence checks (from canonical mapping)

- Measurement rows: **258**
- Missing `term_iri`: **30 rows / 25 unique columns**
- `individualCount` + non-count property/unit combos: **74 rows / 19 unique columns**

### Missing `term_iri` (current canonical gap)

`cwt_marine_survival_rate`, `expansion_factor`, `in_river_mortality_rate`, `mainstem_mortality_rate`, `marine_survival_index`, `ocean_mortality_rate`, `phos`, `relative_hatchery_spawner_abundance`, `relative_hatchery_spawner_abundance_change`, `relative_hatchery_spawner_abundance_percentile`, `relative_hatchery_spawner_abundance_trend`, `relative_spawner_abundance`, `relative_spawner_abundance_change`, `relative_spawner_abundance_percentile`, `relative_spawner_abundance_trend`, `relative_wild_spawner_abundance`, `relative_wild_spawner_abundance_change`, `relative_wild_spawner_abundance_percentile`, `relative_wild_spawner_abundance_trend`, `spawner_abundance`, `spawner_abundance_change`, `spawner_abundance_percentile`, `spawner_abundance_trend`, `terminal_mortality_rate`, `total_mortality_rate`

### Potential count/property incoherence

Rows where `term_iri = dwc:individualCount` but property/unit are not `qudt:Count` + `unit:NUM`.

`spawners`, `spawners_age_1`, `spawners_age_2`, `spawners_age_3`, `spawners_age_4`, `spawners_age_5`, `spawners_age_6`, `spawners_age_7`, `terminal_age_1`, `terminal_age_2`, `terminal_age_3`, `terminal_age_4`, `terminal_age_5`, `terminal_age_6`, `terminal_age_7`, `terminal_catch`, `terminal_run_size`, `total_spawners`, `total_terminal_run`

## Notes
- Use this file as the working pattern reference; mirror/snapshot copies in other repos should be synced from this canonical view.
- Ontology acceptance/backfill remains anchored to `dfo-salmon-ontology` PR #31.
