# ROBOT Setup and Known Limitations

This document describes ROBOT configuration for the DFO Salmon Ontology and documents known limitations and expected violations.

## ROBOT Commands

### Basic Quality Checks

```bash
# Check logical consistency (canonical)
make reason

# Generate quality report (canonical)
make quality-check

# If you need raw ROBOT CLI, use the pinned jar from tools/
java -jar tools/robot.jar report \
  --input ontology/dfo-salmon.ttl \
  --profile robot-profile.yaml \
  --fail-on ERROR \
  --output release/artifacts/robot-quality-report.html
```

### Theme coverage (gcdfo:theme) check

Run the pinned SPARQL check that enforces every term has 1–3 themes from `gcdfo:ThemeScheme` (excluding `gcdfo:ThemeScheme` and its member theme concepts):

```bash
# From the repo root
make theme-coverage
# Or if using devenv/nix (optional):
# devenv shell make theme-coverage
```

- Output: theme coverage report (empty = passing; rows list issues). Run `make theme-coverage` to generate.
- Prereqs: `tools/robot.jar` (run `make install-robot` if missing) and Java. If using `devenv`/`nix` (optional), Java is provided inside the environment.

### Alpha migration SPARQL lints

Run the fast lint bundle used by `make test`:

```bash
# From the repo root
make alpha-lint
# Or if using devenv/nix (optional):
# devenv shell make alpha-lint
```

The lint runner (`scripts/run-sparql-lint.sh`) executes:

- `scripts/sparql/missing-year-basis.rq` (checks SKOS `YearBasisScheme` assumptions once present)
- `scripts/sparql/missing-variable-decomposition.rq` (requires `gcdfo:iadoptEntity` + `gcdfo:iadoptProperty` on variable concepts)
- `scripts/sparql/no-legacy-variablehas.rq` (blocks reintroduction of legacy `gcdfo:variableHas*` properties)
- `scripts/sparql/skos-match-on-owl-properties.rq` (blocks `skos:*Match` on OWL/RDF properties)
- `scripts/sparql/skos-match-on-owl-classes.rq` (blocks `skos:*Match` on OWL/RDFS classes)

Output files are written to `release/tmp/*.tsv`; non-empty output fails the lint step.

### CI/CD Configuration

**Problem:** ROBOT fails CI/CD pipelines due to expected violations that aren't actual errors.

**Solution:** Use the provided configuration to prevent false failures:

```bash
# Use the provided quality check script (recommended)
./scripts/robot-quality-check.sh

# Or run ROBOT directly with appropriate settings
java -jar tools/robot.jar report \
  --input ontology/dfo-salmon.ttl \
  --profile robot-profile.yaml \
  --fail-on ERROR \
  --output release/artifacts/robot-quality-report.html
```

**Key Configuration Options:**

1. **Custom Profile (`robot-profile.yaml`):** Downgrades violation severity for known acceptable issues
2. **`--fail-on ERROR`:** Still fails on genuine ERROR-level issues, but expected violations are downgraded to INFO level
3. **Quality Check Script:** Handles all configuration automatically

### Multi-Reasoner Analysis

```bash
# Test with multiple reasoners
robot reason --input ontology/dfo-salmon.ttl --reasoner ELK --output release/artifacts/elk-inferred.ttl
robot reason --input ontology/dfo-salmon.ttl --reasoner HermiT --output release/artifacts/hermit-inferred.ttl
robot reason --input ontology/dfo-salmon.ttl --reasoner JFact --output release/artifacts/jfact-inferred.ttl
```

## Known ROBOT Limitations with SKOS

### Missing Label Errors for SKOS Concepts

**Issue:** ROBOT reports 31 ERROR violations for SKOS concepts lacking `rdfs:label`.

**Root Cause:** ROBOT does not perform RDFS inference and doesn't recognize that `skos:prefLabel` is a subproperty of `rdfs:label` per W3C SKOS specification.

**Impact:** None - this is a tool limitation, not a modeling error:

- ✅ W3C SKOS compliant: `skos:prefLabel` is subproperty of `rdfs:label`
- ✅ OWL reasoning: All reasoners understand the relationship correctly
- ✅ SPARQL queries: SKOS-aware applications work correctly
- ✅ Semantic web tools: SKOS-compliant tools handle correctly

**Project default:** Mirror `skos:prefLabel` into `rdfs:label` for canonical ontology terms unless an explicit exception is documented in conventions.

**Baseline note:** Counts can change as ontology content evolves; treat static numbers below as historical context, not an invariant contract.

**Quality check:** Investigate any new missing-label errors and classify as either expected external-term noise or genuine local modeling drift.

### JFact Datatype Warning

**Issue:** JFact may report datatype-related warnings involving `gcdfo:EstimateType` when SKOS concept ranges are interpreted as datatypes by strict datatype checks.

**Root Cause:** `EstimateType` is correctly modeled as `skos:Concept` (not a datatype). JFact's datatype checking system is confused by SKOS concept usage as object property ranges.

**Impact:** None - all reasoners (ELK, HermiT, JFact) produce identical results (2183 lines). Ontology is logically consistent.

**Action:** This warning can be safely ignored.

## Expected Baseline Violations

When running ROBOT report, expect these violations as acceptable:

### ERROR Level (39 total)

- **31 SKOS concepts:** Missing `rdfs:label` (have `skos:prefLabel` - acceptable per W3C SKOS)
- **8 Darwin Core terms:** Missing `rdfs:label` (external imports - acceptable)

### WARN Level (159 total) - Updated after whitespace fix

- **147 missing definitions:**
  - 3 BFO MIREOT terms (expected - have `oboInOwl:hasDefinition`)
  - 8 Darwin Core terms (expected - external imports)
  - 7 hybrid OWL+SKOS concepts (ROBOT limitation - have `skos:definition`)
  - 129 DFO terms (ROBOT limitation - have `rdfs:comment` but not recognized)
- **1 other minor annotation issue**

### INFO Level (52 total)

- **52 missing superclasses:** To be analyzed for appropriateness (see superclass-analysis.md)

## 3. Definition Property Recognition Issues

**Issue:** ROBOT reports missing definitions for terms that actually have definitions using different properties.

**Root Cause:** ROBOT's definition checking is limited and doesn't recognize all definition properties used in hybrid OWL+SKOS ontologies.

**Affected Terms:**

1. **Hybrid OWL+SKOS Concepts (7 terms):**

   - Use `skos:definition` instead of `rdfs:comment`
   - Examples: terms modeled with SKOS definition patterns in this ontology
   - ROBOT expects `rdfs:comment` for OWL classes

2. **BFO MIREOT Terms (3 terms):**

   - Use `oboInOwl:hasDefinition` instead of `rdfs:comment`
   - ROBOT may not recognize this property

3. **Darwin Core Terms (8 terms):**
   - External imports without local definitions
   - Expected and acceptable

**Impact:** None - all terms have appropriate definitions per W3C standards.

**Recommendation:** Document these as expected violations rather than changing the ontology to accommodate ROBOT limitations.

## Quality Monitoring

### Automated Checks

Use canonical project targets (`make quality-check`, `make reason`, `make test`) for consistent quality checking.

### Regression Detection

When adding new terms:

1. Run ROBOT report before and after changes
2. Verify ERROR count doesn't increase beyond the accepted baseline in latest CI artifacts
3. Document any new violations and their acceptability
4. Update this document if new expected violations are identified

### Contributing Guidelines

Before submitting changes:

1. Run ROBOT reasoner to ensure logical consistency
2. Check that new violations are documented as acceptable
3. Update ROBOT_SETUP.md if new expected violations are introduced
4. Ensure all three reasoners (ELK, HermiT, JFact) produce consistent results

## Troubleshooting

### ROBOT Won't Start

- Ensure Java is installed and accessible
- Check that `tools/robot.jar` exists
- Verify file paths in commands are correct

### Inconsistent Reasoner Results

- All three reasoners should produce identical line counts
- If results differ, there may be a logical inconsistency
- Check for unsatisfiable classes or contradictory axioms

### Unexpected Violations

- Compare against baseline expected violations in this document
- Document new acceptable violations
- Investigate genuine new issues

---

_Last updated: 2026-02-25_
_ROBOT version: 1.9.8_
