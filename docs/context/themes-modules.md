# DFO Salmon Ontology — Theme / Module Scheme (for `dfoc:theme` annotation)

## Purpose
- Provide a bounded-context oriented theme scheme to tag every OWL class, property, and SKOS concept via the `dfoc:theme` annotation.
- Align with Conway’s Law by mirroring the major Pacific Region functions (Science, Resource Management, Species at Risk, Habitat/Oceans, Salmon Enhancement, Policy/Legal, Data/IT).
- Keep navigation and review lightweight: themes are descriptive only (no reasoning).

## Proposed Themes (values for the SKOS `:ThemeScheme`)
1) **Stock Assessment & Reference Points** — Stock assessment workflow, WSP rapid/integrated status, benchmarks/thresholds, model executions. **Org anchor:** Science Branch (Stock Assessment & Science; Fisheries & Aquaculture Management Directorate Science integration).
2) **Monitoring & Field Programs** — Surveys/events, enumeration/estimate methods, QA/QC, SIL/SEN integration, observational metadata. **Org anchor:** Science Branch field programs; Conservation & Protection partners for observations.
3) **Genetics & Stock Composition** — Samples, assays, GSI runs, composition measurements, reporting units, uncertainty. **Org anchor:** Science Branch genetics/GRD.
4) **Fisheries Management & Harvest Decisions** — TAC/HCR logic, management decisions, advice consumption, CU accounting, mixed-stock considerations. **Org anchor:** Fisheries/Resource Management Branch.
5) **Species at Risk & Recovery** — COSEWIC/SARA status, recovery actions, critical habitat interactions. **Org anchor:** Oceans, Habitat & Species at Risk (OHSAR) programs.
6) **Salmon Enhancement & Hatcheries** — Hatchery influences, enhancement treatments, SEP operational data. **Org anchor:** Salmonid Enhancement Program (SEP) within Fisheries Management.
7) **Habitat, Ecosystem & Climate Pressures** — Threat factors, environmental drivers, habitat indicators, ocean conditions. **Org anchor:** OHSAR + Ecosystem Science.
8) **Policy, Governance & Org Structure** — Wild Salmon Policy (CU status/benchmarks), Fish Stocks Provisions (FSP) compliance, legal/policy frameworks, requirements/triggers, ORG hierarchy (sector/branch/division/section), projects, collaborations. **Org anchor:** Policy/Regulatory leads; corporate/program management; Science-policy interface.
9) **Data, Models & Provenance** — Datasets, provenance (PROV-O), quality (DQV), reproducibility (code commits, versions), data products/exports. **Org anchor:** Science data management & analytics teams.

_Notes:_ Themes are intentionally coarse and map to existing Pacific organizational seams; use multiple themes when a term is genuinely shared. Avoid inventing micro-themes that mirror individual teams.

## Personas × Domain Perspectives (for review lenses)
| Persona / Domain lens | Assessments | Monitoring | Genetics | Fisheries Mgmt | Species at Risk | Enhancement | Habitat/Climate | Policy/Gov/Org | Data/Provenance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stock assessment scientists | ✓ | ✓ | △ | △ | △ | △ | △ | ✓ | ✓ |
| Fisheries/resource managers | △ | △ | △ | ✓ | △ | ✓ | △ | ✓ | △ |
| Species-at-risk biologists | △ | △ | △ | △ | ✓ | △ | ✓ | ✓ | △ |
| Salmon enhancement (SEP) | △ | ✓ | △ | ✓ | △ | ✓ | △ | ✓ | △ |
| Habitat/oceans specialists | △ | ✓ | △ | △ | ✓ | △ | ✓ | △ | △ |
| Indigenous/co-governance partners | △ | △ | △ | ✓ | ✓ | △ | ✓ | ✓ | △ |
| Data/IT/analytics | △ | △ | ✓ | △ | △ | △ | △ | △ | ✓ |

Legend: ✓ primary lens, △ secondary/consulted.

## How to apply
- **Annotation property:** `dfoc:theme` (annotation property) → range: SKOS concept in `:ThemeScheme`.
- **Cardinality:** 1–3 per term; pick the owning bounded context(s).
- **Scope:** All OWL classes, object/datatype properties, annotation properties, SKOS concepts, and concept schemes.
- **Placement:** Keep alongside other annotations (label/definition/definition source) for each term.
- **Governance:** If a new theme is needed, update the Theme scheme first; avoid ad-hoc literals.

## Rationale and alignment
- Mirrors Pacific Region functional seams (Science, Fisheries Management/Resource Management, OHSAR/Species at Risk, SEP, Policy/Legal, Data/IT).
- Supports review checklists (e.g., all Assessment terms share a theme; reviewers can filter by theme).
- Keeps SKOS/OWL separation intact: themes are annotations only; no logical consequences.

## Open questions / to validate
- Confirm latest Pacific Region branch names (Resource Management vs Fisheries Management; OHSAR naming) and adjust labels accordingly.
- Decide whether Aquaculture-specific interactions merit a distinct theme or remain under Fisheries Management.
- Decide if Indigenous stewardship/co-governance warrants a dedicated theme or stays as a secondary tag across the above themes.
