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
  - internally builds `release/tmp/dfo-salmon-docs-input.ttl` via `make docs-widoco-input` (collapsed import closure for deterministic docs rendering)
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
- Shared-layer ontology IRI import: `ontology/dfo-salmon.ttl` imports `https://w3id.org/smn`
- Shared-layer build resolution (default local): `make prepare-import-catalog` maps `https://w3id.org/smn` to `../salmon-domain-ontology/salmon-domain-ontology.ttl` (flat, import-free root artifact) when present.
- Shared-layer fallback resolution: if `SMN_FLAT_TTL` is missing, ROBOT/WIDOCO flows fall back to remote import resolution via `https://w3id.org/smn`.
- DFO namespace boundary: `gcdfo:` terms authored here are the DFO-specific canonical layer for this repo.
- Shared-layer preference: downstream consumers should use `smn:` wherever a shared term exists in the imported Salmon Domain Ontology, then use `gcdfo:` only for DFO-specific terms with no shared replacement.
- Migration state: overlapping shared identifiers have been hard-migrated to `smn:` in `ontology/dfo-salmon.ttl`; remaining `gcdfo:` terms are intended to be DFO-specific.
- Transition note: if an upstream migration artifact still references draft shared `salmon:` IRIs, treat that as a pre-`smn` placeholder rather than the preferred steady-state target.
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
