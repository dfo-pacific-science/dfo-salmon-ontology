# Term Table Documentation Workflow

This document explains the end-to-end process for documenting Controlled Vocabularies and Thesauri from the DFO Salmon Ontology in the data-stewardship-unit website.

## Overview

The workflow transforms ontology terms into human-friendly documentation pages on the FADS Open Science Doc Hub website:

1. **Define themes** in `scripts/config/themes.yml`; the theme annotations live in the canonical `ontology/dfo-salmon.ttl`.
2. **Generate SPARQL queries** automatically from theme definitions.
3. **Extract term tables** as CSV files from the canonical ontology (uses `gcdfo:theme` annotations directly).
4. **Publish to website** where Quarto generates documentation pages.

## Workflow Components

### 1. Theme Configuration (`scripts/config/themes.yml`)

Themes define how ontology terms are grouped for documentation. Each theme specifies:

- `id`: Unique identifier (used in filenames)
- `label`: Human-readable title
- `query_file`: Name of generated SPARQL query file
- `output_csv`: Name of generated CSV file
- `theme_iri`: Theme IRI to include.



**To add a new theme:**
1. Add a new entry to `themes:` in `scripts/config/themes.yml` (see that file for the current 9-theme list).
2. Specify the schemes and/or classes you want to include.
3. Run the extraction script (see below).

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
1. Reads `scripts/config/themes.yml` (ids/labels/output filenames).
2. Loads `ontology/dfo-salmon.ttl` (canonical ontology with theme annotations) and reads `gcdfo:theme` directly from that file.
3. Generates SPARQL queries for each theme.
4. Executes queries against the ontology.
5. Writes CSV files to `release/artifacts/term-tables/{theme-id}-terms.csv` (these are versioned in git).
6. Writes metadata JSON to `release/artifacts/term-tables/{theme-id}-terms.csv.meta.json` (also versioned).
7. Writes SPARQL queries to `scripts/sparql/{theme-id}-terms.rq`.

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

**To update the website (no submodule; term tables are checked in and copied over):**

1. From the ontology repo, regenerate term tables directly from the canonical ontology:
   ```bash
   python scripts/extract-term-tables.py
   ```

2. Commit updated term tables in the ontology repo (they are versioned under `release/artifacts/term-tables/`):
   ```bash
   git status   # verify only term tables + related changes
   git add release/artifacts/term-tables scripts/sparql
   git commit -m "Update term tables"
   ```

3. Copy term tables into the DSU repo (from the ontology repo):
   ```bash
   make dsu-sync-term-tables DSU_ONTOLOGY_DIR=/path/to/data-stewardship-unit/data/ontology
   ```

4. In the DSU repo, commit the copied tables:
   ```bash
   cd /path/to/data-stewardship-unit
   git add data/ontology/release/artifacts/term-tables
   git commit -m "Update ontology term tables"
   ```

   *Note:* The DSU repo no longer regenerates term tables in pre-commit. Generation happens in this ontology repo; DSU pre-commit only validates CSV/meta structure.

5. Build the website locally using Quarto (if using `devenv`/`nix` (optional), Quarto is provided via the environment; otherwise install Quarto separately. Ensure R packages are available):
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
    theme_iri: "https://w3id.org/gcdfo/salmon#HabitatTypeScheme"
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
- The website reads the generated CSVs in `data/ontology/release/artifacts/term-tables/` (Quarto does **not** read `themes.yml` directly).
- The tabbed/accordion interface will automatically display the new theme’s table using `reactable`.
- No separate theme page file is needed—all themes are on the main page.
- Regeneration is manual: run `python scripts/extract-term-tables.py`, then sync to DSU with `make dsu-sync-term-tables ...`.

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
