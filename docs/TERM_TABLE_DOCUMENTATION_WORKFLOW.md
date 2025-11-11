# Term Table Documentation Workflow

This document explains the end-to-end process for documenting Controlled Vocabularies and Thesauri from the DFO Salmon Ontology in the data-stewardship-unit website.

## Overview

The workflow transforms ontology terms into human-friendly documentation pages on the website:

1. **Define themes** in `scripts/config/themes.yml` to group related ontology terms
2. **Generate SPARQL queries** automatically from theme definitions
3. **Extract term tables** as CSV files from the ontology
4. **Publish to website** where Quarto generates documentation pages

## Workflow Components

### 1. Theme Configuration (`scripts/config/themes.yml`)

Themes define how ontology terms are grouped for documentation. Each theme specifies:

- `id`: Unique identifier (used in filenames)
- `label`: Human-readable title
- `query_file`: Name of generated SPARQL query file
- `output_csv`: Name of generated CSV file
- `schemes`: List of SKOS scheme IRIs to include
- `classes`: List of OWL class IRIs to include

**Example:**
```yaml
themes:
  - id: stock_assessment
    label: "Stock Assessment Methods"
    query_file: "stock-assessment-terms.rq"
    output_csv: "stock-assessment-terms.csv"
    schemes:
      - "https://w3id.org/dfoc/salmon#EnumerationMethodScheme"
      - "https://w3id.org/dfoc/salmon#EstimateMethodScheme"
    classes:
      - "https://w3id.org/dfoc/salmon#EscapementMethod"
      - "https://w3id.org/dfoc/salmon#Stock"
```

**To add a new theme:**
1. Add a new entry to `themes:` in `scripts/config/themes.yml`
2. Specify the schemes and/or classes you want to include
3. Run the extraction script (see below)

### 2. SPARQL Query Generation

The `scripts/extract-term-tables.py` script automatically generates SPARQL queries from theme definitions.

**How it works:**
- For each theme, it builds SPARQL queries that:
  - Query SKOS concepts within specified `schemes`
  - Query OWL classes from the `classes` list
  - Extract labels, definitions, related terms, and metadata
- Queries are written to `scripts/sparql/{theme-id}-terms.rq`

**You don't need to write SPARQL manually** - the script generates them from your theme configuration.

### 3. Term Table Extraction

Run the extraction script to generate CSV files:

```bash
cd /path/to/dfo-salmon-ontology
python scripts/extract-term-tables.py
```

**What it does:**
1. Reads `scripts/config/themes.yml`
2. Loads `ontology/dfo-salmon.ttl`
3. Generates SPARQL queries for each theme
4. Executes queries against the ontology
5. Writes CSV files to `release/artifacts/term-tables/{theme-id}-terms.csv`
6. Writes metadata JSON to `release/artifacts/term-tables/{theme-id}-terms.csv.meta.json`
7. Writes SPARQL queries to `scripts/sparql/{theme-id}-terms.rq`

**Output files:**
- `release/artifacts/term-tables/*.csv` - Term tables in CSV format
- `release/artifacts/term-tables/*.csv.meta.json` - Metadata (source commit, timestamp, query checksum)
- `scripts/sparql/*.rq` - Generated SPARQL queries

### 4. Website Integration

The data-stewardship-unit website automatically displays term tables.

**Website structure:**
- `reference_info/data_standards/index.qmd` - Main "Controlled Vocabulary & Thesauri" page with:
  - Semantic search across all themes
  - Tabbed interface for browsing by theme
  - All theme tables on a single page
- `reference_info/ontology/formal-documentation.qmd` - Link to full Widoco documentation

**The main page:**
1. Loads all CSV files from `data/ontology/release/artifacts/term-tables/` using R (`readr` package)
2. Displays a searchable interface with client-side JavaScript
3. Shows tabbed tables for each theme using R's `reactable` package with:
   - Interactive column resizing (built-in)
   - Sorting and search capabilities
   - Clickable Term ID links
   - Theme column showing which theme each term belongs to

**To update the website:**
1. Ensure the ontology submodule in `data-stewardship-unit/data/ontology/` is up to date
2. Run the extraction script in the ontology repo: `python scripts/extract-term-tables.py`
3. Copy/commit the updated CSV files to the website repo
4. Pre-commit hooks will automatically validate CSV structure and metadata before commit
5. Build the website locally using Quarto (R packages must be installed locally)
6. The website will display the new data using R code blocks that render `reactable` tables

**Note:** The website is built locally, not on GitHub Actions. Ensure you have R and the required R packages (`reactable`, `readr`, `jsonlite`, `htmltools`, `htmlwidgets`) installed locally before building. CSV validation happens automatically via pre-commit hooks (see `.pre-commit-config.yaml`).

## Complete Workflow Example

### Adding a New Theme

**Step 1: Update themes.yml**
```yaml
themes:
  - id: habitat
    label: "Habitat and Environment"
    query_file: "habitat-terms.rq"
    output_csv: "habitat-terms.csv"
    schemes:
      - "https://w3id.org/dfoc/salmon#HabitatTypeScheme"
    classes:
      - "https://w3id.org/dfoc/salmon#Habitat"
      - "https://w3id.org/dfoc/salmon#StreamReach"
```

**Step 2: Run extraction**
```bash
cd dfo-salmon-ontology
python scripts/extract-term-tables.py
```

**Step 3: Verify output**
- Check `release/artifacts/term-tables/habitat-terms.csv` exists
- Review `scripts/sparql/habitat-terms.rq` to see generated query

**Step 4: Update website (if needed)**
- Update `reference_info/data_standards/index.qmd` to include the new theme in:
  - The `themes` list for search functionality (R code block, around line 47)
  - The `themes` list for tabbed interface (R code block, around line 253)
- The tabbed interface will automatically display the new theme's table using `reactable`
- No separate theme page file is needed - all themes are on the main page

### Modifying Existing Themes

**To add/remove terms from a theme:**
1. Edit `scripts/config/themes.yml` - add/remove schemes or classes
2. Run `python scripts/extract-term-tables.py`
3. Commit the updated CSV files
4. Website automatically reflects changes (no page edits needed)

**To change a theme label:**
1. Update `label:` in `themes.yml`
2. If you want to update the page title, edit the corresponding `.qmd` file
3. Re-run extraction (optional, but good for consistency)

## File Structure

```
dfo-salmon-ontology/
├── scripts/
│   ├── config/
│   │   └── themes.yml              # Theme definitions (YOU EDIT THIS)
│   ├── extract-term-tables.py      # Extraction script (RUN THIS)
│   └── sparql/
│       └── *-terms.rq              # Generated SPARQL queries
├── ontology/
│   └── dfo-salmon.ttl              # Main ontology file
└── release/
    └── artifacts/
        └── term-tables/
            ├── *-terms.csv         # Generated term tables
            └── *-terms.csv.meta.json  # Metadata

data-stewardship-unit/
├── data/
│   └── ontology/                   # Submodule pointing to dfo-salmon-ontology
│       └── release/
│           └── artifacts/
│               └── term-tables/   # CSV files used by website
├── reference_info/
│   ├── data_standards/
│   │   └── index.qmd              # Main "Controlled Vocabulary & Thesauri" page (uses R)
│   └── ontology/
│       ├── index.qmd               # Controlled Vocabularies overview (redirect)
│       ├── formal-documentation.qmd  # Link to Widoco documentation
│       └── _partials/
│           └── helpers.R          # R helpers for rendering tables with reactable
└── _quarto.yml                     # Website configuration
```

## Key Concepts

### SKOS Schemes vs OWL Classes

- **SKOS Schemes**: Controlled vocabularies (e.g., enumeration methods, status codes)
  - Defined in `schemes:` list
  - Queried via `skos:inScheme` relationships
- **OWL Classes**: Formal ontology classes (e.g., `EscapementMethod`, `Stock`)
  - Defined in `classes:` list
  - Queried directly by IRI

### SPARQL Query Generation

The script automatically generates two types of queries per theme:
1. **Scheme query**: Finds all SKOS concepts in specified schemes
2. **Class query**: Finds specified OWL classes and their properties

Both queries extract:
- Term labels (`rdfs:label`)
- Definitions (`IAO_0000115`)
- Related terms and relationships
- Controlled vocabulary membership
- Canonical URIs

### Website Page Generation

The website uses Quarto to:
1. Execute R code blocks in `.qmd` files
2. Load CSV files using `readr` package via `helpers.R`
3. Render interactive tables using the `reactable` package with:
   - Built-in column resizing
   - Sorting and search
   - Pagination
   - Clickable Term ID links
   - Theme column

**R code is hidden** - the pages only show the rendered tables, not the code (using `#| echo: false`).

**Required R packages (install locally):**
- `reactable` - Interactive table rendering
- `readr` - CSV file reading
- `jsonlite` - JSON metadata reading
- `htmltools` - HTML utilities
- `htmlwidgets` - Widget framework for reactable

**Building the website:**
The website must be built locally using `quarto render` or `quarto preview`. R and the required packages must be installed on your local machine. CSV validation happens automatically via pre-commit hooks before commits (see `.pre-commit-config.yaml` in the website repo). The GitHub Actions workflow only renders and publishes the Quarto website.

## Troubleshooting

### CSV files not found
- Ensure extraction script ran successfully
- Check that CSV files are in `release/artifacts/term-tables/`
- Verify submodule path in website repo

### Empty term tables
- Check that schemes/classes in `themes.yml` match ontology IRIs exactly
- Verify terms exist in `ontology/dfo-salmon.ttl`
- Check SPARQL query files for syntax errors

### Website not updating
- Ensure CSV files are committed to website repo
- Check that `data/ontology/` submodule is up to date
- Verify file paths in `.qmd` files match actual CSV locations

### Theme tab not appearing
- Check that the theme is included in both `themes` lists in `reference_info/data_standards/index.qmd`
- Verify the CSV file exists in `data/ontology/release/artifacts/term-tables/`
- Ensure the theme `id` matches the CSV filename (e.g., `hatchery_enhancement` → `hatchery-enhancement-terms.csv`)

## Best Practices

1. **Always update themes.yml** when ontology changes affect term groupings
2. **Run extraction after ontology changes** to keep CSV files current
3. **Commit CSV files** with ontology changes so website stays in sync
4. **Use meaningful theme labels** that match page titles
5. **Keep theme IDs consistent** - changing them requires updating website files
6. **Test locally** before committing - run extraction and verify CSV output

## Related Documentation

- [Conventions Guide](CONVENTIONS.md) - How to model terms in the ontology
- [Contributing Guide](CONTRIBUTING.md) - General contribution workflow
- [Validation Guide](VALIDATION_README.md) - How to validate ontology changes

## Questions?

Contact the Data Stewardship Unit or file an issue in the repository.

