# DFO Salmon Ontology Validation

This directory contains the DFO Salmon Ontology with SHACL validation for automated estimate type assignment.

## Files

- `dfo-salmon.ttl` - Main ontology file (schema only, no instance data)
- `dfo-salmon-shapes.ttl` - SHACL validation shapes and automated classification rules
- `sample-survey-data.ttl` - Sample survey data for testing (instance data)
- `test_shacl_validation.py` - Python script to test validation and classification
- `requirements.txt` - Python dependencies

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the validation test:
   ```bash
   python test_shacl_validation.py
   ```

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
