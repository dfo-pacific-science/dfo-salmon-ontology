# Final Conventions Adherence Audit (alpha/0.0.6)

**Date:** 2026-02-25  
**Auditor:** `fc-conventions-adherence` subagent  
**Branch:** `fc/conventions-adherence-20260225`  
**Scope:**
- `ontology/dfo-salmon.ttl`
- `scripts/sparql/*` lint queries
- `docs/CONVENTIONS.md` (rule references)

---

## Execution Notes

### Lint execution status
- Attempted: `make alpha-lint`
- Result: blocked by missing Java runtime (`Java runtime is not available`), after installing `tools/robot.jar`.
- Fallback: executed equivalent SPARQL lint queries with `rdflib` against `ontology/dfo-salmon.ttl`.

### Fallback lint results (rdflib)
All four alpha lint queries returned **0 rows**:
- `scripts/sparql/missing-year-basis.rq`
- `scripts/sparql/missing-variable-decomposition.rq`
- `scripts/sparql/no-legacy-variablehas.rq`
- `scripts/sparql/skos-match-on-owl-properties.rq`

Additional targeted checks were run to validate convention-level adherence beyond current lint coverage.

---

## Findings

## 1) **HIGH** — SKOS mapping predicates are used on OWL classes (semantic alignment drift)

**Why this matters**  
Conventions require SKOS `*Match` mappings only for concept-to-concept mappings. OWL class alignments should use `rdfs:subClassOf` / `owl:equivalentClass`.

**Rule references**
- `docs/CONVENTIONS.md:291-295`
- `docs/CONVENTIONS.md:1749-1753`
- `docs/CONVENTIONS.md:1775-1777`

**Evidence (ontology class + skos:closeMatch):**
- `ontology/dfo-salmon.ttl:1384` — `gcdfo:ReportingOrManagementStratum skos:closeMatch sosa:FeatureOfInterest`
- `ontology/dfo-salmon.ttl:1635` — `gcdfo:Escapement skos:closeMatch odo:SALMON_00000479`
- `ontology/dfo-salmon.ttl:1641` — `gcdfo:SurveyEvent skos:closeMatch sosa:Sampling`
- `ontology/dfo-salmon.ttl:1652` — `gcdfo:EscapementSurveyEvent skos:closeMatch sosa:Sampling`
- `ontology/dfo-salmon.ttl:1660` — `gcdfo:EscapementMeasurement skos:closeMatch sosa:Result`
- `ontology/dfo-salmon.ttl:2114` — `gcdfo:SpawnerAbundance skos:closeMatch odo:SALMON_00000479`

**Recommended fix**
1. Replace each class-level `skos:closeMatch` with OWL/RDFS alignment where confidence allows:
   - `rdfs:subClassOf` for hierarchy-level alignment.
   - `owl:equivalentClass` only where true equivalence is justified.
2. If confidence is uncertain, remove `skos:closeMatch` and track as candidate mapping (issue/ADR note) per confidence ladder.

---

## 2) **MEDIUM** — Canonical I-ADOPT decomposition is incomplete for one variable-like concept

**Why this matters**  
Conventions define canonical authoring for variable concepts with local annotation decomposition (including `gcdfo:iadoptProperty` and `gcdfo:iadoptEntity`).

**Rule references**
- `docs/CONVENTIONS.md:429-430` (canonical authoring)
- `docs/CONVENTIONS.md:405-409` (annotation property set)

**Evidence**
- `ontology/dfo-salmon.ttl:1878-1885` — `gcdfo:RapidStatusMetric` is modeled as a SKOS metric/variable concept with `gcdfo:iadoptEntity` + `gcdfo:usedProcedure`, but no `gcdfo:iadoptProperty`.

**Additional lint-coverage evidence**
- `scripts/sparql/missing-variable-decomposition.rq:24-37` uses a scheme-name filter that does not include `gcdfo:RapidStatusMetricScheme` (or generic “metric scheme” logic), so this gap is not currently caught by lint.

**Recommended fix**
1. Decide intent for `gcdfo:RapidStatusMetric`:
   - If it is a true variable concept: add `gcdfo:iadoptProperty` (and any required constraints/procedure metadata).
   - If it is a grouping node only: document exception and/or move to non-variable scheme semantics.
2. Update `missing-variable-decomposition.rq` to include `gcdfo:RapidStatusMetricScheme` (or robust pattern matching for variable/metric schemes).

---

## 3) **MEDIUM** — `gcdfo:iadoptConstraint` values are OWL classes in multiple metric terms

**Why this matters**  
Conventions describe constraints as constraint concepts (typically SKOS concepts in schemes). Current usage mixes in OWL classes for constraint role fillers.

**Rule references**
- `docs/CONVENTIONS.md:406-407` (`gcdfo:iadoptConstraint` role)
- `docs/CONVENTIONS.md:414` (constraints as SKOS concepts in existing schemes)

**Evidence (constraint assertions):**
- `ontology/dfo-salmon.ttl:1910` — `LongTermTrendMetric gcdfo:iadoptConstraint gcdfo:WSPRapidStatus`
- `ontology/dfo-salmon.ttl:1926` — `PercentChangeMetric gcdfo:iadoptConstraint gcdfo:WSPRapidStatus`
- `ontology/dfo-salmon.ttl:1941` — `BenchmarkRatioMetric gcdfo:iadoptConstraint gcdfo:LowerBiologicalBenchmark, gcdfo:UpperBiologicalBenchmark`
- `ontology/dfo-salmon.ttl:1956` — `ProbabilityDeclineBelowLowerBenchmarkMetric gcdfo:iadoptConstraint gcdfo:LowerBiologicalBenchmark`
- `ontology/dfo-salmon.ttl:1971` — `AbundancePercentileMetric gcdfo:iadoptConstraint gcdfo:WSPRapidStatus`
- `ontology/dfo-salmon.ttl:1986` — `RapidStatusScoreMetric gcdfo:iadoptConstraint gcdfo:WSPRapidStatus`

**Evidence (constraint targets are OWL classes):**
- `ontology/dfo-salmon.ttl:1738` — `gcdfo:WSPRapidStatus a owl:Class`
- `ontology/dfo-salmon.ttl:1756` — `gcdfo:LowerBiologicalBenchmark a owl:Class`
- `ontology/dfo-salmon.ttl:1765` — `gcdfo:UpperBiologicalBenchmark a owl:Class`

**Recommended fix**
1. Introduce/normalize SKOS constraint concepts for workflow context/benchmark qualifiers.
2. Use those SKOS terms in `gcdfo:iadoptConstraint`.
3. Keep class-level semantics via separate OWL alignments (e.g., class ↔ concept mapping in an alignment module) if needed.

---

## 4) **LOW** — `gcdfo:usedProcedure` target typing is weakly aligned to procedure/plan semantics

**Why this matters**  
Conventions define `gcdfo:usedProcedure` as the canonical procedure hook aligned to `sosa:usedProcedure`, expecting procedure/method concepts or classes aligned to procedure/plan semantics.

**Rule reference**
- `docs/CONVENTIONS.md:408`

**Evidence**
- `ontology/dfo-salmon.ttl:1532-1536` — `gcdfo:usedProcedure` declaration and subproperty alignment.
- `ontology/dfo-salmon.ttl:1738-1745` — `gcdfo:WSPRapidStatus` is `owl:Class` under `iao:0000030` (information content entity), not clearly typed/aligned as `sosa:Procedure` or `iao:0000104` plan specification.
- `ontology/dfo-salmon.ttl:1883,1896,1911,1927,1942,1957,1972,1987` — all `gcdfo:usedProcedure` values point to `gcdfo:WSPRapidStatus`.

**Recommended fix**
- Either:
  1. Reclassify/align `gcdfo:WSPRapidStatus` to procedure/plan semantics, or
  2. Introduce a dedicated procedure term and use that as the `gcdfo:usedProcedure` target.

---

## 5) **LOW** — Prefix hygiene drift (duplicate namespace alias + unused prefixes)

**Why this matters**  
Not logically fatal, but increases maintenance noise and can hide real namespace issues over time.

**Evidence**
- Duplicate URI aliasing:
  - `ontology/dfo-salmon.ttl:17` — `@prefix unit: <http://qudt.org/vocab/unit/> .`
  - `ontology/dfo-salmon.ttl:19` — `@prefix qudtunit: <http://qudt.org/vocab/unit/> .`
- Declared but unused in this file:
  - `iop:` (`ontology/dfo-salmon.ttl:12`)
  - `dwciri:` (`ontology/dfo-salmon.ttl:16`)
  - `qudt:` (`ontology/dfo-salmon.ttl:18`)
  - `qudtunit:` (`ontology/dfo-salmon.ttl:19`)
  - `org:` (`ontology/dfo-salmon.ttl:23`)

**Recommended fix**
- Keep a single QUDT unit prefix alias.
- Remove unused prefixes (or annotate intentionally reserved prefixes in comments/module docs).

---

## Requested Check Matrix

### 1) SKOS vs OWL decision rule adherence
- **Pass with caveat**: no direct punning (`owl:Class` + `skos:Concept`) found.
- **Caveat**: class-level `skos:closeMatch` usage indicates semantic-alignment drift (Finding #1).

### 2) I-ADOPT annotation-centric canonical pattern adherence
- **Partial pass**: canonical annotation properties exist (`gcdfo:iadoptEntity`, `gcdfo:iadoptProperty`, `gcdfo:iadoptConstraint`, `gcdfo:usedProcedure`), and legacy `variableHas*` / `iadoptMethod` not present.
- **Gaps**: Findings #2–#4.

### 3) Property alignment rule adherence (no `skos:*Match` on OWL properties)
- **Pass**: no `skos:*Match` triples found on OWL/RDF properties.

### 4) Year-basis SKOS migration consistency
- **Pass**: `YearBasisScheme` exists; no legacy class-based year terms detected; lint query returned 0 rows.

### 5) Namespace/prefix misuse and semantic drift
- **Low-severity drift identified**: prefix hygiene issues and class-level SKOS mapping drift.

---

## Top 5 Risks (ranked)
1. **High** — OWL class alignments currently encoded with `skos:closeMatch` (weakens semantic rigor/interoperability).
2. **Medium** — `RapidStatusMetric` decomposition incompleteness + lint blind spot may allow silent canonical drift.
3. **Medium** — `iadoptConstraint` currently points to OWL classes in several cases, conflicting with SKOS-constraint intent.
4. **Low** — `usedProcedure` target semantics are under-specified vs procedure/plan expectation.
5. **Low** — duplicate/unused prefixes add avoidable namespace maintenance debt.

---

## Suggested Follow-up (non-blocking)
- Add one focused lint query for **SKOS `*Match` on OWL classes** (parallel to existing property-only lint).
- Extend decomposition lint scope to include `RapidStatusMetricScheme` (or generic metric/variable inference).
- Add a lint query checking `iadoptConstraint` values are SKOS concepts (or codified approved exception set).
