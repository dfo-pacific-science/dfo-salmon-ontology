# Entrypoints (What Is Actually Used?)

Purpose: keep one short, reliable map of what starts the system, what is wired in, and where to edit things.

## Run (human-facing)

- Start command(s): n/a (ontology project; no long-running service)
- Local URL(s): n/a
- Required environment variables (names only, no secrets): none

## Build

- Build command(s): `devenv shell python scripts/extract-term-tables.py` (generates term tables + SPARQL under `release/artifacts/term-tables` and `scripts/sparql`)
- Docs refresh (WIDOCO + serializations + SKOS section): `make docs-refresh` (regenerates the base HTML docs via WIDOCO, then `docs/gcdfo.{ttl,owl}` via ROBOT and `docs/gcdfo.jsonld` via `scripts/convert_ttl_to_jsonld.py` from `ontology/dfo-salmon.ttl`, then refreshes the SKOS blocks in `docs/index.html` and enforces OWL-before-SKOS display ordering)
- WIDOCO regeneration only: `make docs-widoco` (runs WIDOCO and copies output into `docs/`)
- Release snapshot (immutable, GitHub Pages): `make release-snapshot VERSION=X.Y.Z` (creates `docs/releases/VERSION/` with `index.html` + `gcdfo.{ttl,owl,jsonld}`)
- SKOS-only refresh: `python3 scripts/generate_skos_section.py` (reparses `ontology/dfo-salmon.ttl` and rewrites the SKOS block inside `docs/index.html`)
- CI entrypoint: `devenv shell make ci` (CI means automated checks run on every push; it runs tests, quality-check, and `make docs-refresh`, so it will create doc diffs that must be committed)

## Test

- Test command(s): `devenv shell make test` (runs theme coverage + ELK reasoning) against the canonical `ontology/dfo-salmon.ttl`
- Fastest smoke test: `devenv shell make theme-coverage`

## App Entry Points / Wiring

- Main entry file(s): `ontology/dfo-salmon.ttl` (canonical ontology)
- Routes / handlers / commands: `scripts/extract-term-tables.py` (uses `scripts/config/themes.yml` and writes `scripts/sparql/*.rq`, `release/artifacts/term-tables/*.csv`)
- Background jobs (if any): none

## UI Styling

- Canonical styling system (repo-majority): global CSS stylesheets for the static WIDOCO HTML docs
- Style entry files / patterns: `docs/index.html` + `docs/resources/*.css` (notably `docs/resources/main.css` + `docs/resources/gcdfo-custom.css`)
- Design tokens / CSS variables live in: Bootstrap CSS variables in `docs/resources/main.css` (e.g., `--bs-*`) and dark-mode-toggle vars in `docs/resources/slider.css`
- Inline styles policy: avoid adding new inline styles; prefer classes + `docs/resources/*.css`
- UI behavior wiring: `scripts/generate_skos_section.py` injects the custom JS for TOC/search/permalinks into `docs/index.html`

## Release (manual steps)

- Manual release steps (manual means you must run these yourself; CI does not create releases):
  1. Update `ontology/dfo-salmon.ttl` header fields: `dcterms:modified`, `owl:versionInfo`, `owl:versionIRI`, and `owl:priorVersion` (previous version IRI).
  2. Run `devenv shell make ci` and commit the regenerated docs/serializations.
  3. Run `devenv shell make release-snapshot VERSION=X.Y.Z` to create the release snapshot (a release snapshot is an immutable copy under `docs/releases/X.Y.Z/`).
  4. Commit and push `docs/` and `docs/releases/X.Y.Z/` so GitHub Pages serves the version.
  5. Optional: tag the release (a tag is a Git label for a specific commit, e.g., `v0.0.999`).

## Canonical Implementations (Per Feature)

- Ontology schema → `ontology/dfo-salmon.ttl`
- Term tables/themes → `scripts/config/themes.yml`, generated `scripts/sparql/*.rq`, `release/artifacts/term-tables/*.csv`
