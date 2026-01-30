# ExecPlan — W3ID + WIDOCO + Docs UX (High/Medium Priorities)

Date: 2026-01-29

## Purpose / Big Picture

Make the ontology’s public identifiers stable and usable for both humans and machines:

- Fix **version IRIs** (an *IRI* is a stable web identifier used as a term’s “name”) so they are **dereferenceable** (dereferenceable means fetching the IRI over HTTPS returns a useful representation instead of 404).
- Add **content negotiation** (content negotiation means choosing HTML vs RDF based on the HTTP `Accept` header) at the ontology IRI so clients can retrieve Turtle, RDF/XML, or JSON-LD from `https://w3id.org/gcdfo/salmon/`.
- Ensure docs regenerate reliably (WIDOCO output stays in sync with `ontology/dfo-salmon.ttl`) and repo-specific UI/UX enhancements persist.
- Implement the remaining medium-priority docs UX improvements (term search, mobile nav, heading permalinks).

## Progress

- [x] 2026-01-29 — Create immutable version snapshots under `docs/releases/<version>/` (GitHub Pages serves from `/docs`).
- [x] 2026-01-30 — Validate W3ID redirect targets and rules against current repo layout (latest artifacts + `docs/releases/0.0.999/` exist and match the `.htaccess` paths).
- [x] 2026-01-30 — Update `ontology/dfo-salmon.ttl` metadata to meet WIDOCO recommended fields (added `owl:priorVersion`; refreshed `dcterms:modified`).
- [x] 2026-01-30 — Open PR to `perma-id/w3id.org` updating `gcdfo/salmon/.htaccess` for content negotiation + version paths (awaiting merge/deploy).
- [x] 2026-01-30 — W3ID PR merged and deployed; verify redirects with `curl -I` checks.
- [x] 2026-01-29 — Add WIDOCO regeneration target and wire it into `make docs-refresh` and `make ci`.
- [x] 2026-01-30 — Post-process WIDOCO output idempotently (verified stable after full WIDOCO regeneration in `make ci`).
- [x] 2026-01-30 — Publish `docs/releases/0.0.999/` and verify GitHub Pages serves the snapshot.
- [x] 2026-01-30 — Publish `docs/releases/0.0.2/` so the previous-version link can dereference.
- [x] 2026-01-30 — Add medium-priority docs UX features (search, mobile TOC, permalink buttons).
- [x] 2026-01-30 — Reduce “double listing” confusion in the rendered docs (collapse Overview lists; consolidate SKOS headings; avoid duplicate TOC labels).
- [x] 2026-01-30 — Enable WebVOWL visualization in WIDOCO output (publish under `docs/webvowl/`; embed behind a collapsible in `docs/index.html`).

## Surprises & Discoveries

- W3ID redirects now return 303 for latest + version IRIs (verified with `curl -I` checks).
- `/gcdfo/` on `w3id.org` shows an Apache directory listing; the active redirect rules live under `/gcdfo/salmon/`.
  - Evidence: `curl https://w3id.org/gcdfo/ | head`
- In `perma-id/w3id.org`, the active namespace folder is `gcdfo/` (not `GCDFO/`); `https://w3id.org/GCDFO/salmon` returns 404.
  - Evidence: `curl -I https://w3id.org/GCDFO/salmon`
- WIDOCO best-practice docs recommend adding metadata **in the ontology** (instead of relying on a separate `.properties` file) so releases remain consistent.
  - References: `docs/context/widoco_bps.md`, `docs/context/widoc_metadata_guide.md`

## Decision Log

- 2026-01-29 — Prefer **ontology-embedded metadata** over WIDOCO `config.properties`.
  - Rationale: WIDOCO’s metadata guide recommends it; it keeps releases self-contained in `ontology/dfo-salmon.ttl`.
- 2026-01-29 — Keep **hash-based term IRIs** (e.g., `https://w3id.org/gcdfo/salmon#Term`).
  - Rationale: hash IRIs mean new terms automatically dereference via the ontology document IRI; no per-term redirect rules needed.
- 2026-01-29 — Make **version IRIs immutable** by publishing per-version snapshots under `docs/` and never rewriting them.
  - Rationale: a version IRI should always resolve to that historical version; the unversioned ontology IRI can track “latest”.
- 2026-01-29 — Use w3id for **version IRIs** and redirect them to GitHub Pages snapshots.
  - Rationale: w3id provides long-term stable identifiers, while GitHub Pages serves the actual immutable files.

## Outcomes & Retrospective

(Fill in after executing the plan.)

## Context and Orientation

### Who does what (so releases stay reliable)

#### What Codex can do (in this repo)

- Add Makefile targets that generate **immutable version snapshots** into `docs/releases/<version>/` for GitHub Pages.
- Update `ontology/dfo-salmon.ttl` metadata to match WIDOCO best practices (so docs don’t drift).
- Wire docs generation so `devenv shell make ci` reliably regenerates all required artifacts.
- Prepare the exact `.htaccess` content you should PR into `perma-id/w3id.org` (but Codex cannot merge it for you).

#### What you must do (outside this repo)

- Open the **w3id PR** to `https://github.com/perma-id/w3id.org` and wait for maintainers to merge/deploy it.
- Always: publish the docs/artifacts on GitHub Pages and keep per-version snapshots present under `docs/releases/<version>/`.

#### What you do each new release (repeatable checklist)

- Bump version metadata in `ontology/dfo-salmon.ttl` (`owl:versionInfo`, `owl:versionIRI`, `dcterms:modified`).
- Run `devenv shell make ci` and commit the updated artifacts (especially `docs/gcdfo.{ttl,owl,jsonld}` and `docs/index.html`).
- Create the version snapshot folder `docs/releases/<version>/` (commit it so GitHub Pages serves it).
- (Recommended) Create a git tag (e.g., `v0.0.3`) so the release is easy to reference externally.

### Key terms (quick definitions)

- **IRI**: the web identifier used as a stable, globally unique “name” for an ontology or term.
- **Dereferenceable**: fetching the IRI over HTTPS returns something useful (typically an HTML page or an RDF serialization), not a 404.
- **303 redirect**: an HTTP response meaning “the representation is at another URL” (common for publishing RDF resources).
- **Content negotiation**: selecting HTML vs Turtle/RDF/XML/JSON-LD based on the HTTP `Accept` header.
- **W3ID**: a community-run redirect service for stable `https://w3id.org/...` identifiers (you update redirects via PRs).
- **WIDOCO**: a documentation generator (“Wizard for Documenting Ontologies”) that produces an HTML site from an ontology.
- **OWL**: the Web Ontology Language (formal classes/properties/axioms).
- **SKOS**: Simple Knowledge Organization System (concept schemes + controlled vocabulary terms).
- **Turtle (TTL)** / **RDF/XML** / **JSON-LD**: common RDF serialization formats.
- **SemVer**: “semantic versioning” format `MAJOR.MINOR.PATCH` (e.g., `0.0.999`).

### Repo "source of truth"

- Canonical ontology: `ontology/dfo-salmon.ttl`
- Published docs + artifacts (GitHub Pages): `docs/` (notably `docs/index.html` + `docs/gcdfo.{ttl,owl,jsonld}`)
- One local+CI command: `devenv shell make ci`

### WIDOCO Reference Documentation (project context)

Upstream/reference docs live in:
- `docs/context/widoco_README.md` (WIDOCO capabilities and CLI flags)
- `docs/context/widoc_metadata_guide.md` (what metadata WIDOCO recognizes)
- `docs/context/widoco_bps.md` (recommended metadata checklist)

### Current public URLs

- Ontology IRI (latest): `https://w3id.org/gcdfo/salmon`
- Term namespace (hash): `https://w3id.org/gcdfo/salmon#`
- GitHub Pages (HTML): `https://dfo-pacific-science.github.io/dfo-salmon-ontology/`
- Current downloadable serializations:
  - `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.ttl`
  - `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.owl`
  - `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.jsonld`

## Plan of Work

### Milestone 1 — Decide and implement versioned publication layout (this repo)

Goal: make a stable, immutable target for `https://w3id.org/gcdfo/salmon/<version>`.

1. Pick a directory layout for version snapshots (required: `docs/releases/<version>/` since GitHub Pages serves from `/docs`).
2. Implement a Makefile target that, given a version string, writes:
   - `docs/releases/<version>/index.html` (human landing page for that version)
   - `docs/releases/<version>/gcdfo.ttl`
   - `docs/releases/<version>/gcdfo.owl`
   - `docs/releases/<version>/gcdfo.jsonld`
3. Add a guardrail: snapshots must be **immutable** (refuse to overwrite unless a `FORCE=1` flag is provided).

Acceptance:
- `docs/releases/0.0.999/` exists in-repo and contains `index.html` + `gcdfo.{ttl,owl,jsonld}`.
- `https://dfo-pacific-science.github.io/dfo-salmon-ontology/releases/0.0.999/` serves an HTML page and `.../releases/0.0.999/gcdfo.ttl` returns 200.

### Milestone 2 — Align ontology metadata with WIDOCO best practices

Goal: have the ontology carry the metadata Widoco expects/recommends so documentation stays correct.

**WIDOCO metadata rationale:**
WIDOCO best-practices docs recommend embedding key metadata in the ontology itself (instead of relying on a separate `.properties` file) so releases remain consistent. Recommended metadata includes:
- `vann:preferredNamespaceUri` and `vann:preferredNamespacePrefix` (namespace URI + prefix)
- `owl:versionIRI` and `owl:versionInfo` (version IRI + version string)
- `dcterms:creator` / `dcterms:contributor` / `dcterms:publisher` (attribution)
- `dcterms:license` (license)

See `docs/context/widoco_bps.md` and `docs/context/widoc_metadata_guide.md` for the full checklist and accepted properties.

**Tasks:**
1. Update `ontology/dfo-salmon.ttl` `owl:Ontology` header:
   - Add `vann:preferredNamespaceUri` and `vann:preferredNamespacePrefix` (WIDOCO best practices: namespace URI + prefix are **RECOMMENDED**).
   - Add `dcterms:contributor` (currently contributors appear in HTML but not in the ontology).
   - Add a "previous version" link (e.g., `prov:wasRevisionOf` or `dcterms:replaces`) when releasing `0.0.3+`.
2. After Milestone 3 is done, set "This version" in docs to the W3ID version IRI (not the GitHub Pages URL).

Acceptance:
- Running `devenv shell make ci` updates the docs metadata section consistently with the ontology header.
- WIDOCO metadata fields match the ontology annotations (no manual drift).

### Milestone 3 — Update W3ID redirect rules (external repo: perma-id/w3id.org)

Goal: make `w3id.org` do both (a) content negotiation for latest and (b) dereference version IRIs.

Edits to make in `https://github.com/perma-id/w3id.org`:

1. Update `gcdfo/salmon/.htaccess`:
   - Add `RewriteCond %{HTTP_ACCEPT} ...` rules for:
     - Turtle → redirect to `https://dfo-pacific-science.github.io/dfo-salmon-ontology/gcdfo.ttl`
     - RDF/XML → redirect to `.../gcdfo.owl`
     - JSON-LD → redirect to `.../gcdfo.jsonld`
   - Add version rules for `/<version>` (SemVer) that redirect to the immutable snapshot paths:
     - These targets assume you publish per-version artifacts at `/releases/<version>/` on GitHub Pages (from `docs/releases/<version>/` in this repo).
     - default (HTML) → `.../releases/<version>/`
     - Turtle/RDF/XML/JSON-LD → `.../releases/<version>/gcdfo.{ttl,owl,jsonld}`
2. Optionally update `gcdfo/salmon/readme.md` to document:
   - the canonical latest IRI
   - the version IRI pattern
   - contact + issue tracker
3. Open a PR and wait for the **w3id maintainers** to merge it and deploy it.

Acceptance (post-merge):
- `curl -I -H 'Accept: text/turtle' https://w3id.org/gcdfo/salmon` returns a 303 to the `.ttl` file.
- `curl -I https://w3id.org/gcdfo/salmon/0.0.999` returns a 303 to the version HTML landing page (not 404).
- `curl -I -H 'Accept: application/ld+json' https://w3id.org/gcdfo/salmon/0.0.999` returns a 303 to the versioned `.jsonld` file.

### Milestone 4 — Add a WIDOCO regeneration step (this repo)

Goal: keep OWL crossrefs/diagrams/provenance pages synced with `ontology/dfo-salmon.ttl` instead of relying on stale committed HTML.

**WIDOCO Guardrails (avoid "ghost" behavior):**
- Prefer adding/changing metadata in `ontology/dfo-salmon.ttl` rather than hand-editing `docs/index.html`.
- Any repo-specific HTML/CSS/JS tweaks should be applied **idempotently** (safe to rerun without duplicating markup).
- If WIDOCO regeneration is added to the pipeline, treat `docs/index.html` as **generated output** and keep customizations in:
  - post-processing scripts, and/or
  - standalone assets under `docs/resources/`

**Tasks:**
1. Add WIDOCO to the dev environment (pin a version; run it inside `devenv shell`).
2. Add a `make docs-widoco` target that regenerates the WIDOCO site into `docs/` (use `-uniteSections`; keep `-ignoreIndividuals` if we continue generating custom SKOS lists).
3. Update `make docs-refresh` to run:
   - `docs-widoco` (regenerate base HTML)
   - `docs-serializations` (regenerate downloadable RDF files)
   - `docs-skos` (inject SKOS-by-scheme and repo-specific UI tweaks)

Acceptance:
- `devenv shell make docs-refresh` causes OWL term crossrefs to reflect new ontology terms without manual edits.
- The repo-specific UI additions (TOC filter, active section highlight, "Copy IRI") persist after regeneration.

### Milestone 5 — Medium-priority docs UX improvements

1. Add “search terms” (not just TOC filtering): index OWL labels + SKOS labels into a lightweight JS search.
2. Improve mobile nav: make the TOC an off-canvas drawer on small screens.
3. Add heading permalink buttons (copy a stable `#fragment` URL).

Acceptance:
- Search finds terms by label/altLabel and scrolls to the section.
- Mobile sidebar can be opened/closed, traps focus, and works with keyboard navigation.
- “Copy link” works for all major headings/terms.

## Concrete Steps (Commands)

All commands run from repo root inside the dev shell:

1. Validate current repo baseline:
   - `devenv shell make ci`
2. Verify current w3id behavior:
   - `curl -I -H 'Accept: text/turtle' https://w3id.org/gcdfo/salmon/`
3. After W3ID PR merges, re-run the same `curl` commands and confirm redirects.

## Validation and Acceptance

Repo-side:

- `devenv shell make ci` succeeds and produces no diffs.

W3ID-side (after PR merge/deploy):

- Latest IRI:
  - `curl -I https://w3id.org/gcdfo/salmon` → 301 to trailing slash, then 303 to HTML
  - `curl -I -H 'Accept: text/turtle' https://w3id.org/gcdfo/salmon/` → 303 to `.ttl`
  - `curl -I -H 'Accept: application/ld+json' https://w3id.org/gcdfo/salmon/` → 303 to `.jsonld`
- Version IRI:
  - `curl -I https://w3id.org/gcdfo/salmon/<version>` → 303 to `.../releases/<version>/`
  - `curl -I -H 'Accept: application/rdf+xml' https://w3id.org/gcdfo/salmon/<version>` → 303 to `.../releases/<version>/gcdfo.owl`

## Idempotence and Recovery

- `make docs-refresh` must be safe to rerun repeatedly (no duplicated injected snippets, no duplicated UI nodes).
- If a W3ID `.htaccess` change is wrong:
  - revert in your fork and open a follow-up PR (W3ID is config-by-PR; there is no runtime knob).
- If a per-version snapshot was published incorrectly:
  - publish a *new* version (don’t rewrite the old snapshot); treat old version as immutable.
