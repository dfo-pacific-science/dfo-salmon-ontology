# Term Table Documentation Workflow

This document explains the end-to-end process for documenting Controlled Vocabularies and Thesauri from the DFO Salmon Ontology in the data-stewardship-unit website.

## Overview

The workflow transforms ontology terms into human-friendly documentation pages on the FADS Open Science Doc Hub website:

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
- `theme_iri`: Theme IRI to include. 

**Example:**
```yaml
themes:
  - id: stock_assessment
    label: "Stock Assessment Methods"
    query_file: "stock-assessment-terms.rq"
    output_csv: "stock-assessment-terms.csv"
    theme_iri: "https://w3id.org/gcdfos/salmon#StockAssessmentTheme"
```

**To add a new theme:**
1. Add a new entry to `themes:` in `scripts/config/themes.yml`
2. Specify the schemes and/or classes you want to include
3. Run the extraction script (see below)

### 2. SPARQL Query Generation

The `scripts/extract-term-tables.py` script automatically generates SPARQL queries from theme definitions.

**How it works:**
- For each theme, it builds SPARQL queries that:
  - Query all SKOS concepts and OWL classes within specified `theme_iri`
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

**First-time setup (adding the submodule):**

If this is your first time setting up the website with the ontology submodule:

1. Navigate to the data-stewardship-unit repository directory:
   ```bash
   cd /path/to/data-stewardship-unit
   ```
   (Replace `/path/to/data-stewardship-unit` with the actual path to your `data-stewardship-unit` repository)

2. Add the ontology repository as a Git submodule:
   ```bash
   git submodule add https://github.com/dfo-pacific-science/dfo-salmon-ontology.git data/ontology
   ```
   This creates the `data/ontology/` directory and links it to the ontology repository.

3. Initialize and update the submodule:
   ```bash
   git submodule update --init --recursive
   ```

4. Commit the submodule addition:
   ```bash
   git add .gitmodules data/ontology
   git commit -m "Add dfo-salmon-ontology as submodule"
   ```

**Regular updates (after submodule is set up):**

1. Navigate to the data-stewardship-unit repository directory:
   ```bash
   cd /path/to/data-stewardship-unit
   ```

2. Update the ontology submodule to get the latest changes:
   ```bash
   git submodule update --remote data/ontology
   ```
   Or, if you want to update to a specific commit/branch:
   ```bash
   cd data/ontology
   git checkout main  # or specific branch/commit
   git pull
   cd ../..
   ```

3. Navigate to the ontology repository directory:
   ```bash
   cd /path/to/dfo-salmon-ontology
   ```
   (Replace `/path/to/dfo-salmon-ontology` with the actual path to your `dfo-salmon-ontology` repository)

4. Run the extraction script to generate CSV files:
   ```bash
   python scripts/extract-term-tables.py
   ```
   This creates CSV files in `release/artifacts/term-tables/` within the ontology repository.

5. Navigate back to the data-stewardship-unit repository:
   ```bash
   cd /path/to/data-stewardship-unit
   ```

6. Update the submodule to include the newly generated CSV files:
   ```bash
   git submodule update --remote data/ontology
   git add data/ontology
   ```

7. Commit the updated submodule reference:
   ```bash
   git commit -m "Update ontology submodule with latest term tables"
   ```
   Pre-commit hooks will automatically validate CSV structure and metadata before the commit completes.

8. Build the website locally using Quarto (R packages must be installed locally):
   ```bash
   quarto render
   ```
   Or to preview:
   ```bash
   quarto preview
   ```

9. The website will display the new data using R code blocks that render `reactable` tables

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
    theme_iri: "https://w3id.org/dfoc/salmon#HabitatTypeScheme"
```

**Step 2: Run extraction**
```bash
cd dfo-salmon-ontology
python scripts/extract-term-tables.py
```

**Step 3: Verify output**
- Check `release/artifacts/term-tables/habitat-terms.csv` exists
- Review `scripts/sparql/habitat-terms.rq` to see generated query

**Step 4: Website automatically reflects changes**
- The website now reads themes directly from `themes.yml` - no manual updates needed
- The tabbed interface will automatically display the new theme's table using `reactable`
- No separate theme page file is needed - all themes are on the main page
- Pre-commit hooks will automatically update the submodule and regenerate term tables when you commit

### Modifying Existing Themes

**To add/remove terms from a theme:**
1. Edit `scripts/config/themes.yml` - add/remove schemes or classes
2. Run `python scripts/extract-term-tables.py`
3. Commit the updated CSV files
4. Website automatically reflects changes (no page edits needed)

**To change a theme label:**
1. Update `label:` in `themes.yml`
2. The website will automatically use the new label (no code changes needed)
3. Pre-commit hooks will regenerate term tables automatically



## Best Practices

1. **Always update themes.yml** when ontology changes affect term groupings
2. **Pre-commit hooks handle updates automatically** - they update the submodule and regenerate term tables
3. **Commit CSV files** with ontology changes so website stays in sync
4. **Use meaningful theme labels** - they appear automatically on the website
5. **Keep theme IDs consistent** - changing them requires updating CSV filenames
6. **Test locally** before committing - pre-commit hooks will validate CSV files automatically
7. **Install R package 'yaml'** - required for reading themes.yml: `install.packages('yaml')`


