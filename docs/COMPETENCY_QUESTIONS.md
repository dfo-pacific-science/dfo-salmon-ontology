# DFO Salmon Ontology: Competency Questions

## Scope

This ontology models **operational processes and data structures** for Pacific salmon management at DFO, including:

- **Stock Assessment**: Escapement surveys, measurement protocols, estimate types
- **Genetics/GSI**: Genetic sample analysis, reporting units, composition measurements  
- **Management & Policy**: Conservation status, management units, regulatory compliance
- **Data Stewardship**: Quality control, validation rules, automated classification

**This is NOT a biological domain ontology** about salmon ecology or behavior, but rather an **operational ontology** for data management and integration.

# Competency Questions — DFO Salmon Ontology MVP (v0.1)

**Scope:** Questions the MVP must answer across SPSR (hero), GRD, and SILS→Narratives, plus near‑term (v0.3) questions. Each item lists required fields/terms and whether it’s answerable **Now** (v0.1) or **Next** (v0.3).

---

## A) Terminology, Validation, and Provenance
- Where are **spawner_origin** values used inconsistently (e.g., *wild* vs *unmarked*)?  
  *Needs:* `spawner_origin` (SKOS), template validation (SHACL). **Now**
- Which records use a **proxy** (e.g., mainstem index, GSI) **without** a `proxy_justification`?  
  *Needs:* `data_source_type`, `proxy_justification`. **Now**
- For each record derived from **GSI**, is an **uncertainty metric** present (e.g., `gsi_sample_size`, `gsi_confidence_interval`)?  
  *Needs:* `data_source_type=genetic_proxy`, `gsi_sample_size`, `gsi_confidence_interval`. **Now**
- Which assessments/narratives lack **minimum provenance** (data sources, method, code version, reviewer, date)?  
  *Needs:* provenance profile (PROV/DQV), `method`, `code_version`, `reviewer`. **Now**
- Which SPSR submissions fail **required‑field validation** and what are the **fix hints**?  
  *Needs:* SHACL shapes + validator outputs. **Now**

## B) CU↔SMU Crosswalk and Governance
- For a given **SMU**, which **CUs** participate and with what **rationale/version**?  
  *Needs:* CU↔SMU crosswalk (SKOS + CSV), `rationale`, `version_date`. **Now**
- Where does a **CU** appear in **multiple SMUs**, and what governance note explains it?  
  *Needs:* crosswalk notes, ambiguity flags. **Now**
- Show **status disagreements** or **data‑deficient** flags across CUs within an SMU.  
  *Needs:* CU status, DD flags, mapping to SMU. **Next**

## C) Reference Points / Benchmarks
- For each CU/SMU, which **reference_point_type** and **benchmark_method** were used?  
  *Needs:* `reference_point_type` (Sgen, Sref, FRP‑L, USR, LRP…), `benchmark_method` (SR, percentile, expert). **Now**
- Where is **benchmark_sensitivity** flagged (e.g., dependence on priors/assumptions)?  
  *Needs:* `benchmark_sensitivity` boolean/enum + note. **Now**
- Given an SMU, list component CU **LBMs** used to derive the **LRP**, with links to methods.  
  *Needs:* CU LBM values + SMU LRP derivation provenance. **Next**

## D) GRD ↔ SPSR Interoperability (GSI)
- For a given **Run_ID**/**Sample_ID**, what **assay/panel** produced the result and where is it applied in SPSR?  
  *Needs:* GRD keys (`Run_ID`, `Sample_ID`, `Assay_ID`), join table or mapping. **Now** (structure), **Next** (full linkage)
- List SPSR estimates that **consume GSI composition** without propagating **uncertainty**.  
  *Needs:* link from SPSR record → GRD result (or proxy flag) + uncertainty fields. **Next**

## E) SILS → Narrative Reproducibility
- Which **stream inspections** (SILS) were combined to form a **narrative**, and what rules were applied?  
  *Needs:* narrative bundle metadata (`inputs`, `ruleset_id`, `method`), provenance. **Next**
- Are **sample sizes** and **variation estimates** recorded for narratives?  
  *Needs:* `sample_size`, `variance/CI`, calculation method. **Next**

## F) Decision‑Context Readiness (Management & Advice)
- For a selected **decision context** (e.g., TAC/HCR), are all **required indicators** and **reference points** present and current for the target SMU(s)?  
  *Needs:* decision→indicator mapping, ref point registry. **Next**
- Where are **gaps** (missing data/uncertainty) that would block advice generation?  
  *Needs:* completeness checks over required sets. **Next**

---

## Minimal SPARQL Sketches (for inclusion in the repo)
> Keep these as templates; wire to your triplestore built from vocab + metadata extracts.

- **Proxy w/out justification**  
  ```sparql
  SELECT ?record WHERE {
    ?record :data_source_type :genetic_proxy .
    FILTER NOT EXISTS { ?record :proxy_justification ?j . FILTER(STRLEN(STR(?j)) > 0) }
  }
  ```

- **Benchmark method by unit**  
  ```sparql
  SELECT ?unit ?refPoint ?method WHERE {
    ?unit :hasReferencePoint ?refPoint .
    ?refPoint :benchmark_method ?method .
  }
  ```

- **Missing provenance minimum**  
  ```sparql
  SELECT ?artifact WHERE {
    ?artifact a :AssessmentOrNarrative .
    FILTER NOT EXISTS { ?artifact :data_source ?s }
    UNION FILTER NOT EXISTS { ?artifact :method ?m }
    UNION FILTER NOT EXISTS { ?artifact :code_version ?v }
    UNION FILTER NOT EXISTS { ?artifact :reviewer ?r }
  }
  ```

---

## Field/Term Checklist for v0.1 (must exist in templates & SHACL)
- `spawner_origin` (SKOS) — values + definitions + examples
- `data_source_type` (direct_observation | model_estimate | genetic_proxy)
- `proxy_justification` (string)
- `reference_point_type` (SKOS) + `benchmark_method` + `benchmark_sensitivity`
- `gsi_sample_size`, `gsi_confidence_interval`, `gsi_data_source`
- CU↔SMU crosswalk table with `rationale`, `version_date`
- Provenance minimum: `data_source`, `method`, `code_version`, `reviewer`, `date`

---

## Prioritization Notes
- **Now (v0.1)** answers: terminology consistency, proxy justification, GSI uncertainty presence/absence, benchmark/method registry, CU↔SMU mapping with rationale, provenance minimum, validator pass/fail.
- **Next (v0.3)** adds: narrative bundles, LRP derivation trace, decision‑context completeness checks, uncertainty propagation from GRD.

