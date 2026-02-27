# Entrypoints (What Is Actually Used?)

Purpose: one short, reliable map of what is canonical vs optional/deprecated.

## Run (human-facing)

- Start command(s): n/a (ontology repo; no long-running service)
- Local URL(s): n/a
- Required environment variables (names only, no secrets): none

## Build / Publish

- Canonical docs + artifacts refresh: `make docs-refresh`
  - regenerates WIDOCO HTML in `docs/`
  - regenerates `docs/gcdfo.{ttl,owl,jsonld}` from `ontology/dfo-salmon.ttl`
  - refreshes SKOS sections in `docs/index.html`
- Full CI-equivalent local run: `make ci`
- Optional helper to reduce generated-artifact drift after CI: `make ci-sync-artifacts`
- WIDOCO only: `make docs-widoco`
- Release snapshot (immutable docs version): `make release-snapshot VERSION=X.Y.Z`

### Deprecated optional utility flow (non-canonical)

- `python scripts/extract-term-tables.py`
  - local ad hoc utility only
  - not part of `make ci`
  - not part of `make docs-refresh`
  - not used for DSU/FADS sync

## Test

- Test command(s): `make test` (theme coverage + alpha-lint + ELK reasoning)
- Fast smoke: `make theme-coverage` or `make alpha-lint`

## App Entry Points / Wiring

- Canonical ontology source: `ontology/dfo-salmon.ttl`
- Runtime routes/handlers: none
- Background jobs: none

## UI Styling (docs site)

- Main HTML: `docs/index.html`
- CSS: `docs/resources/*.css`
- SKOS section generation/postprocess:
  - `scripts/generate_skos_section.py`
  - `scripts/postprocess_widoco_html.py`

## Release (manual)

1. Update ontology header metadata (`dcterms:modified`, `owl:versionInfo`, `owl:versionIRI`, `owl:priorVersion`)
2. Run `make ci` (or `make ci-sync-artifacts`) and commit generated docs artifacts
3. Run `make release-snapshot VERSION=X.Y.Z`
4. Commit/push `docs/` + `docs/releases/X.Y.Z/`

## Canonical vs Non-canonical Output Paths

- Canonical published outputs: `docs/`, `docs/releases/X.Y.Z/`
- Non-canonical transient build outputs: `release/`
- Deprecated local-only term-table outputs: `release/artifacts/term-tables/`, `scripts/sparql/*-terms.rq`
