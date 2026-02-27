# WIDOCO in this repo (notes + guardrails)

This file is **repo-specific** guidance for using WIDOCO here. Upstream/reference docs live in:

- `docs/context/widoco_README.md` (WIDOCO capabilities and CLI flags)
- `docs/context/widoc_metadata_guide.md` (what metadata WIDOCO recognizes)
- `docs/context/widoco_bps.md` (recommended metadata checklist)

## What WIDOCO is

**WIDOCO** (“Wizard for Documenting Ontologies”) is a tool that generates an HTML documentation site from an OWL ontology file.

## What this repo currently does (today)

- Canonical ontology source: `ontology/dfo-salmon.ttl`
- Published site/artifacts (GitHub Pages): everything under `docs/`
- Immutable version snapshots (per release): `docs/releases/<version>/` (GitHub Pages serves from `/docs`)
- `make docs-refresh` regenerates:
  - `docs/` HTML via WIDOCO (`make docs-widoco`, uses `tools/widoco.jar`; runs with `-ignoreIndividuals` so SKOS concepts are not duplicated as “Named Individuals”, and `-webVowl` so a WebVOWL diagram is published under `docs/webvowl/`)
  - `docs/gcdfo.ttl` + `docs/gcdfo.owl` (ROBOT convert)
  - `docs/gcdfo.jsonld` (Python `rdflib` conversion)
  - SKOS blocks inside `docs/index.html` (via `scripts/generate_skos_section.py`)

## Release workflow (what you do vs what automation does)

### Per release (every new version `X.Y.Z`)

1. Update ontology header fields in `ontology/dfo-salmon.ttl`:
   - `dcterms:modified`
   - `owl:versionInfo`
   - `owl:versionIRI` (example: `https://w3id.org/gcdfo/salmon/0.0.999`)
   - `owl:priorVersion` (previous version IRI; previous version means the immediate earlier release)
2. Regenerate and verify:
   - `devenv shell make ci`
3. Create the immutable snapshot for that version (served by GitHub Pages):
   - `devenv shell make release-snapshot VERSION=X.Y.Z`
4. Commit and push the updated artifacts under `docs/` (including `docs/releases/X.Y.Z/`).
5. Optional: create a Git tag (a tag is a Git label for a specific commit) such as `vX.Y.Z`.

**Manual vs automated:** These release steps are manual (manual means you must run them yourself); CI (continuous integration, automated checks on every push) does **not** create release snapshots or tags.

### One-time (W3ID setup)

To make version IRIs dereferenceable and to support content negotiation at the ontology IRI, you must open a PR to the upstream W3ID repo (`perma-id/w3id.org`) updating `gcdfo/salmon/.htaccess`.

After the one-time W3ID PR is merged and deployed, you should **not** need another W3ID PR for each future release, as long as:

- the `.htaccess` rule matches all versions (e.g., a `X.Y.Z` pattern), and
- you keep publishing `docs/releases/X.Y.Z/` in this repo for each release.

### WIDOCO changelog note

WIDOCO can generate a changelog by comparing the current ontology to the prior version IRI; this requires the prior version files to be reachable (reachable means the HTTP URL resolves) at `https://dfo-pacific-science.github.io/dfo-salmon-ontology/releases/<version>/gcdfo.owl`.

### Clarifying “merge PR”

- When working on this repo, “merge PR” refers to merging PRs in `dfo-pacific-science/dfo-salmon-ontology`.
- When working on w3id redirects, “merge PR” refers to the W3ID maintainers merging your PR in `perma-id/w3id.org`.

## Guardrails (avoid “ghost” behavior)

- Prefer adding/changing metadata in `ontology/dfo-salmon.ttl` rather than hand-editing `docs/index.html`.
- Any repo-specific HTML/CSS/JS tweaks should be applied **idempotently** (safe to rerun without duplicating markup).
- If WIDOCO regeneration is added to the pipeline, treat `docs/index.html` as **generated output** and keep customizations in:
  - post-processing scripts, and/or
  - standalone assets under `docs/resources/`

## Metadata best practices (how to stay compliant)

WIDOCO best-practices docs recommend embedding key metadata in the ontology itself, notably:

- `vann:preferredNamespaceUri` and `vann:preferredNamespacePrefix` (namespace URI + prefix)
- `owl:versionIRI` and `owl:versionInfo` (version IRI + version string)
- `dcterms:creator` / `dcterms:contributor` / `dcterms:publisher` (attribution)
- `dcterms:license` (license)

See `docs/context/widoco_bps.md` and `docs/context/widoc_metadata_guide.md` for the full checklist and accepted properties.
