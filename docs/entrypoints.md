# Entrypoints (What Is Actually Used?)

Purpose: one short, reliable map of what is canonical vs optional/deprecated.

## Run (human-facing)

- Start command(s): n/a (ontology repo; no long-running service)
- Local URL(s): n/a
- Required environment variables (names only, no secrets): none

## Local prerequisites

- Java 17, plus `make install-robot` and `make install-widoco`
- Python deps: `pip install -r scripts/requirements.txt`
  - `rdflib` is pinned there to the exact version CI installs, because it decides the bytes of `docs/gcdfo.jsonld` and CI rejects any post-`make ci` difference

## Build / Publish

- Canonical docs + artifacts refresh: `make docs-refresh`
  - regenerates WIDOCO HTML in `docs/`
  - regenerates `docs/gcdfo.{ttl,owl,jsonld}` from `ontology/dfo-salmon.ttl`
  - refreshes SKOS sections in `docs/index.html`
- Full CI-equivalent local run: `make ci`
- Supported way to stage regenerated artifacts locally: `make ci-sync-artifacts`
  - runs `make ci`, then stages every tracked path it regenerates, listed once in the Makefile as `CI_ARTIFACT_PATHS`: `docs/gcdfo.{ttl,owl,jsonld}`, `docs/index.html`, `docs/index-en.html`, and the WIDOCO-owned `docs/provenance/`, `docs/resources/`, `docs/webvowl/` trees
  - that list is what CI's post-`make ci` clean-tree check enforces, so the two must not diverge; the CI failure message points here rather than repeating the paths
- WIDOCO only: `make docs-widoco`
  - internally builds `release/tmp/dfo-salmon-docs-input.ttl` via `make docs-widoco-input` (collapsed import closure for deterministic docs rendering)
  - then runs `scripts/normalize_webvowl_json.py` over `docs/webvowl/data/ontology.json` to stabilize OWL2VOWL's nondeterministic ids/ordering against the previously tracked copy; see [ADR-007](adr/007-webvowl-duplicate-node-disambiguation.md)
  - the recipe runs under `set -e`, so a normalizer or WIDOCO failure fails the build instead of printing success
- Release snapshot (immutable docs version): `make release-snapshot VERSION=X.Y.Z`

### Deprecated optional utility flow (non-canonical)

- `python scripts/extract-term-tables.py`
  - local ad hoc utility only
  - not part of `make ci`
  - not part of `make docs-refresh`
  - not used for DSU/FADS sync

## Test

- Test command(s): `make test` (mapping-set structure + theme coverage + alpha-lint + ELK reasoning)
- Fast smoke: `make theme-coverage` or `make alpha-lint`

## App Entry Points / Wiring

- Canonical ontology source: `ontology/dfo-salmon.ttl`
- Shared-layer ontology IRI import: `ontology/dfo-salmon.ttl` imports `https://w3id.org/smn`
- Shared-layer build resolution (default local): `make prepare-import-catalog` maps `https://w3id.org/smn` to `../salmon-domain-ontology/salmon-domain-ontology.ttl` (flat, import-free root artifact) when present.
- Shared-layer fallback resolution: if `SMN_FLAT_TTL` is missing, ROBOT/WIDOCO flows fall back to remote import resolution via `https://w3id.org/smn`.
- Namespace boundary policy (canonical): see [`README.md` — "Namespace Boundary and Shared-Layer Preference"](../README.md#namespace-boundary-and-shared-layer-preference).
- Optional metamodel/upper-level views are no longer owned here; use the shared SMN `ontology/views/` layer for that perspective.
- Boundary detail here is intentionally minimized; this file only records the import/wiring mechanics above.
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
