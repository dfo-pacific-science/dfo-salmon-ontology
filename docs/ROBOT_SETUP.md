# ROBOT Setup and Known Limitations

This document describes ROBOT configuration for the DFO Salmon Ontology and documents known limitations and expected violations.

## ROBOT Commands

### Basic Quality Checks

```bash
# Check logical consistency
robot reason --input ontology/dfo-salmon.ttl --reasoner ELK

# Generate quality report (with custom profile to handle expected violations)
robot report --input ontology/dfo-salmon.ttl --profile robot-profile.yaml --fail-on ERROR --output release/artifacts/quality-report.html

# Convert formats
robot convert --input ontology/dfo-salmon.ttl --output release/artifacts/dfo-salmon.owl
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
  --output release/artifacts/quality-report.html
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

**Decision:** Do NOT add redundant `rdfs:label` properties to satisfy ROBOT.

**Baseline Expected Errors:** 31 missing labels on SKOS concepts (acceptable)

**Quality Check:** New terms should not add to this count - verify any new missing label errors are genuine issues, not SKOS concepts with `skos:prefLabel`.

### JFact Datatype Warning

**Issue:** JFact reports "A known datatype for https://w3id.org/dfo/salmon#EstimateType cannot be found"

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
   - Examples: `dfo:Extinct`, `dfo:Endangered`, `dfo:Threatened`
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

### Regression Detection

When adding new terms:

1. Run ROBOT report before and after changes
2. Verify ERROR count doesn't increase beyond baseline (39)
3. Document any new violations and their acceptability
4. Update this document if new expected violations are identified

### Expected vs Genuine Violations

**Expected (Acceptable):**

- 31 SKOS label "errors" (W3C SKOS compliant)
- 8 Darwin Core label "errors" (external imports)
- 3 BFO definition "warnings" (MIREOT approach)
- 8 Darwin Core definition "warnings" (external imports)
- 7 hybrid OWL+SKOS definition "warnings" (ROBOT limitation)
- 129 DFO definition "warnings" (ROBOT limitation)

**To Be Investigated:**

- 52 superclass info violations (see superclass-analysis.md)

## Quality Monitoring

### Automated Checks

Use the provided `scripts/robot-commands.bat` for consistent quality checking.

### Regression Detection

When adding new terms:

1. Run ROBOT report before and after changes
2. Verify ERROR count doesn't increase beyond baseline (39)
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

_Last updated: 2025-01-24_
_ROBOT version: 1.9.8_
