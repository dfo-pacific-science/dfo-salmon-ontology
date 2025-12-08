# DFO Salmon Ontology Validation

This directory contains the DFO Salmon Ontology with SHACL shapes for automated estimate type assignment. The SHACL runner is currently deferred; shapes remain for reference and future automation.

## Files

- `dfo-salmon.ttl` - Main ontology file (schema only, no instance data)
- `dfo-salmon-shapes.ttl` - SHACL validation shapes and automated classification rules (runner deferred)
- `sample-survey-data.ttl` - Sample survey data for testing (instance data)

## SHACL status

- Automated SHACL execution is currently **deferred** (no maintained runner script).
- Shapes are retained for reference; reintroduce automation by adding a small fixture dataset and a script/workflow when ready.

## Architecture

### Hybrid Approach

- **SKOS Concepts**: Enumeration methods, estimate methods, downgrade criteria, estimate types
- **OWL Classes**: Survey events, measurements, stocks, genetic samples
- **SHACL Shapes**: Validation rules and automated classification logic

### Manual Classification

Estimate types are manually assigned based on Hyatt 1997 criteria. Automated classification is deferred to post-MVP.

### Example Classification Rules

- **Type 2**: Snorkel survey with ≥5 visits, ≥80% coverage, good/excellent visibility
- **Type 3**: Snorkel survey with ≥3 visits, ≥50% coverage
- **Type 4**: Snorkel survey with ≤2 visits
- **Downgrade criteria**: Applied when thresholds are not met

## Usage

1. **Create survey events** using the ontology classes
2. **Add metadata** using the datatype properties
3. **Run SHACL validation** to automatically assign estimate types
4. **Check downgrade criteria** for quality assessment

## Validation Results

The test script will show:

- Validation pass/fail status
- Automated type assignments
- Applied downgrade criteria
- Detailed validation messages

## Schema vs Data Separation

- **Ontology file**: Contains only schema (classes, properties, SKOS concepts)
- **Data files**: Contain instance data (specific surveys, measurements)
- **Shapes file**: Contains validation rules and classification logic

This separation ensures the ontology remains stable and reusable across different datasets.

## Automation (current state)

- **Pre-commit (local):** `scripts/pre-commit-validate-ontology.sh` downloads the pinned ROBOT v1.9.8 to `tools/robot.jar` if missing and runs ELK reasoning for fast consistency checks.
- **CI (push + PR on main/develop):** Runs `make reason` (ELK) and `./scripts/robot-quality-check.sh` (ROBOT report with `robot-profile.yaml`), uploading HTML/log artifacts. ROBOT jar is cached by version.
- **Publishing (merge to main):** CI additionally runs `make publish-validate` to enforce publish-ready SPARQL checks; build fails on violations and uploads the metadata TSV artifact.
- **ROBOT version:** Pinned to 1.9.8 across Makefile, scripts, and CI to avoid drift.
- **Windows:** Use WSL2 + `nix`/`direnv` or Git Bash; `make install-robot` downloads the shared ROBOT jar.
- **Report profile format:** `robot-profile.yaml` is a tab-separated profile (`LEVEL<TAB>check-id`); keep it comment-free so ROBOT parses it correctly.

## Additional SPARQL checks (provenance + year basis)

Run these as part of local or CI validation to surface missing metadata:

```
# Missing definition sources (IAO_0000119) on gcdfos terms
robot query \
  --input draft/dfo-salmon-draft.ttl \
  --query scripts/sparql/missing-definition-source.rq reports/missing-definition-source.tsv

# Measurements/rates missing hasYearBasis (on instance data, if present)
robot query \
  --input draft/dfo-salmon-draft.ttl \
  --query scripts/sparql/missing-year-basis.rq reports/missing-year-basis.tsv
```

The year-basis check will only report rows when instance data are present; it is expected to be empty when run against the schema TTL alone.
