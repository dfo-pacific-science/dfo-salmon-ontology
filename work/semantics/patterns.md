# SPSR Measurement Pattern Proposals (Issue #189)

Entity defaults (by table prefix):
- smu_* → StockManagementUnit (`https://w3id.org/gcdfo/salmon#StockManagementUnit`)
- cu_*, cuyear, custatus → ConservationUnit (`https://w3id.org/gcdfo/salmon#ConservationUnit`)
- pfma_* → Stock (PFMA-constrained) (`https://w3id.org/gcdfo/salmon#Stock`)
- pop_*, population, indicator_* → Population (`https://w3id.org/gcdfo/salmon#Population`) — note: term not yet in ontology; tracked separately.

Property defaults:
- Counts → `http://qudt.org/vocab/quantitykind/Count` with unit `http://qudt.org/vocab/unit/NUM`
- Rates/indices/proportions → `http://qudt.org/vocab/quantitykind/DimensionlessRatio` with unit `http://qudt.org/vocab/unit/UNITLESS`

Constraint placeholder rules (record even if IRI unknown):
- Age N → `<age_N_constraint>`
- Location/phase → `<mainstem_phase>`, `<ocean_phase>`, `<terminal_phase>`
- Lifestage → `<spawner_stage>`
- Catch/run context → `<catch_context>`, `<run_context>`
- Origin → `<hatchery_origin>`

| # | Pattern | Example columns | Count | Proposed entity | Proposed property | Proposed constraints |
|---|---------|-----------------|-------|-----------------|-------------------|----------------------|
| 1 | Age-location catch counts | OCEAN_AGE_1, MAINSTEM_AGE_4, TERMINAL_AGE_7 … | 63 | Table default (SMU→SMU, CU→CU, PFMA→Stock) | Count | `<age_N_constraint>`; `<mainstem_phase>`/`<ocean_phase>`/`<terminal_phase>`; `<catch_context>` |
| 2 | Age catch counts (no location) | CATCH_AGE_1, CATCH_AGE_5 … | 28 | Table default | Count | `<age_N_constraint>`; `<catch_context>` |
| 3 | Age spawner counts | SPAWNERS_AGE_1 … | 35 | Table default | Count | `<age_N_constraint>`; `<spawner_stage>` |
| 4 | Age run counts | RUN_AGE_1 … | 28 | Table default | Count | `<age_N_constraint>`; `<run_context>` |
| 5 | Catch totals by location | TOTAL_CATCH, MAINSTEM_CATCH, OCEAN_CATCH … | 14 | Table default | Count | `<mainstem_phase>`/`<ocean_phase>`/`<terminal_phase>` (when present); `<catch_context>` |
| 6 | Run size totals by location | OCEAN_RUN_SIZE, TERMINAL_RUN_SIZE, TOTAL_RUN_SIZE | 11 | Table default | Count | `<mainstem_phase>`/`<ocean_phase>`/`<terminal_phase>` (when present); `<run_context>` |
| 7 | Spawner totals | SPAWNERS, TOTAL_SPAWNERS | 8 | Table default | Count | `<spawner_stage>` |
| 8 | Exploitation rates | TOTAL_EXPLOITATION_RATE, OCEAN_EXPLOITATION_RATE, ER | 11 | Table default | Dimensionless ratio | `<catch_context>`; `<mainstem_phase>`/`<ocean_phase>`/`<terminal_phase>` when implied |
| 9 | Mortality / survival rates | MAINSTEM_MORTALITY_RATE, OCEAN_MORTALITY_RATE, CWT_MARINE_SURVIVAL_RATE | 13 | Table default | Dimensionless ratio | `<mainstem_phase>`/`<ocean_phase>`/`<terminal_phase>`; `<survival_or_mortality_context>` |
|10 | Reference / benchmark points | LRP, USR, TR, RR, LOWER_BIO_BENCHMARK … | 41 | Table default | Dimensionless ratio (management threshold) | `<management_reference_type>` |
|11 | Quality indices | INDEX_QUALITY | 5 | Table default | Dimensionless ratio | `<data_quality_scheme>` |
|12 | Recruit counts | RECRUITS | 3 | Table default | Count | `<recruit_stage>` |
|13 | Hatchery-origin proportion | PHOS | 1 | Table default | Dimensionless ratio | `<hatchery_origin>` |
|14 | Marine survival index | MARINE_SURVIVAL_INDEX | 1 | Table default | Dimensionless ratio | `<marine_phase>` |
|15 | Expansion factors | EXPANSION_FACTOR | 1 | Table default | Dimensionless ratio (scalar) | `<expansion_method>` |

Notes
- Where multiple phases/locations apply, use `;` to join constraint placeholders (e.g., `<age_3_constraint>;<ocean_phase>`).
- If a precise constraint IRI is later identified (e.g., ENVO location, custom phase concept), replace the placeholder but keep age/location facets explicit.
- Reference/benchmark terms likely need new SKOS concepts (gpt_proposed_terms) with parent `gcdfo:TargetOrLimitRateOrAbundance`.
