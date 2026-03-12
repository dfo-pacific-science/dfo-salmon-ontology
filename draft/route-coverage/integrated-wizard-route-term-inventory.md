# Integrated Wizard Route-Term Coverage Inventory

Date: 2026-03-02  
Scope: CU / SMU / PFMA / IndicatorRiver upload routes  
Issue: #51  
Kanban anchor: `step-1772475890-9a4b2c`

## Method
- Audited canonical ontology: `ontology/dfo-salmon.ttl` (origin/main).
- Cross-checked wizard scope language in: `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md`.
- Classified each route as `present`, `missing`, or `ambiguous` based on explicit in-repo terms.

## Route-Term Inventory Matrix

| Upload route | Ontology term coverage | Status | Evidence | Gap class | Notes |
|---|---|---|---|---|---|
| CU | `gcdfo:ConservationUnit` (`https://w3id.org/gcdfo/salmon#ConservationUnit`) + supporting CU population relations (`gcdfo:hasPopulation`, `gcdfo:populationOf`) | present | `ontology/dfo-salmon.ttl:1675`, `:1418`, `:1426` | none | Core route entity and immediate composition relations exist. |
| SMU | `gcdfo:StockManagementUnit` (`https://w3id.org/gcdfo/salmon#StockManagementUnit`) + CU linkage (`gcdfo:hasConservationUnit`, `gcdfo:conservationUnitOf`) | present | `ontology/dfo-salmon.ttl:1687`, `:1435`, `:1443` | none | Core route entity and CU composition linkage exist. |
| PFMA | No explicit PFMA class/IRI found in ontology (`PFMA`, `Pacific Fishery Management Area`, `PacificFisheryManagementArea`) | missing | Wizard scope includes PFMA in `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md:30,54,186`; ontology search returned no PFMA term matches | missing-term | Route exists in intake scope but lacks a corresponding ontology entity term. |
| IndicatorRiver | `gcdfo:IndicatorRiver` (`https://w3id.org/gcdfo/salmon#IndicatorRiver`) exists; wizard docs now use IndicatorRiver with an explicit "Indicator Stock" UI alias | ambiguous | `ontology/dfo-salmon.ttl:1914`; wizard scope wording in `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md:30,54,186` | terminology-alias + relation ambiguity | Core entity term exists, but route naming and expected relationship semantics need explicit policy mapping. |

## Gap Classes Identified
1. **Missing core entity term**
   - PFMA route has no matching ontology class.
2. **Terminology alias ambiguity**
   - Indicator route naming currently uses canonical `IndicatorRiver` plus an "Indicator Stock" UI alias that should be governed explicitly.
3. **Relationship-model ambiguity (IndicatorRiver/PFMA routes)**
   - Explicit route-level relation properties to CU/SMU/Population are not yet formalized for these scopes.

## Recommended Next Patch Slice
1. **Add PFMA as a minimal, evidence-backed class**
   - Introduce `gcdfo:PacificFisheryManagementArea` (or agreed canonical label) as subclass of `gcdfo:ReportingOrManagementStratum`.
   - Include `skos:altLabel "PFMA"@en` and citation-backed definition/source.
2. **Lock route naming contract in docs**
   - Keep `IndicatorRiver` as ontology term with "Indicator Stock" as UI alias (documented explicitly).
3. **Defer new relationship properties until evidence is cited**
   - Add relation terms only after confirming operational semantics from source policy/docs.

## Patch Slice Status Update (2026-03-02)
Applied in follow-up route-coverage patch:
- Added `gcdfo:PacificFisheryManagementArea` as a minimal class under `gcdfo:ReportingOrManagementStratum` with `skos:altLabel "PFMA"@en` and citation to the Pacific Fishery Management Area Regulations, 2007.
- Added explicit wizard route naming contract language in `docs/ontology_applications/FSAR_Tracer_PRD_CQs.md`:
  - canonical ontology terms (`IndicatorRiver`, `PacificFisheryManagementArea`) remain canonical for persistence/API
  - UI aliases `Indicator Stock` and `PFMA` are display-only mappings

### Remaining Gap Classes After This Slice
1. **Relationship-model ambiguity (IndicatorRiver/PFMA routes)**
   - Route-level relation property semantics to CU/SMU/Population are still intentionally deferred pending source-backed policy/operational evidence.

## Machine-readable Route Mapping Bundle (2026-03-03)
Published to support wizard template/dictionary generation inputs:

- `draft/route-coverage/integrated-wizard-route-mapping.bundle.json`
- `draft/route-coverage/integrated-wizard-route-mapping.bundle.csv`

Bundle contents:
- Canonical route entity IRIs for `CU`, `SMU`, `PFMA`, `IndicatorRiver`
- Route-level wizard table/example bindings currently used by SPSR route selection
- Relation-binding status (`present` vs `deferred`) by route
- Migration policy posture (`migrated`, `deferred_profile`, `not_migrated`) plus shared-layer candidate IRIs

Consumption note:
- Treat this as an implementation contract snapshot for downstream wizard generation, not as authority to promote deferred-profile terms into the shared `smn:` namespace.
