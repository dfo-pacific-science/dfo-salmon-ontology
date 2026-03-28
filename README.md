# GC DFO Salmon Ontology

**Namespace:** `https://w3id.org/gcdfo/salmon#` (prefix: `gcdfo:`)  
**License:** CC-BY 4.0  
**Status:** Version 0.0.999 (pre-1.0 “beta”)

This README is the **technical runbook** for maintaining, building, and publishing the DFO-specific ontology repo.

- If you want to **propose a change or new term**, start with [CONTRIBUTING.md](CONTRIBUTING.md).
- If you want to know **who maintains the repo and how maintainership will expand**, see [GOVERNANCE.md](GOVERNANCE.md).

The GC DFO Salmon Ontology is a **data stewardship and operational process ontology** designed to provide a semantic framework for managing, integrating, and stewarding Pacific salmon data across Fisheries and Oceans Canada (DFO).

**Goal:** Make salmon data interoperable, discoverable, and analyzable with minimal friction for scientists, data stewards, and managers.

**Integration context:** See the Salmon Data Integration System overview page (https://br-johnson.github.io/salmon-data-integration-system/) and walkthrough video (https://youtu.be/B0Zqac49zng?si=VmOjbfMDMd2xW9fH).

**Rule of thumb:** `/ontology/dfo-salmon.ttl` contains **schema only** (no instance facts, measurements, or survey rows). Instance data examples belong in `/ontology/examples/` and are *not* shipped inside the core ontology file.

---

## Table of Contents

- [Documentation and Governance](#documentation-and-governance)
- [Related Repositories and Namespaces](#related-repositories-and-namespaces)
- [Technical Overview](#technical-overview)
- [Namespace Boundary and Shared-Layer Preference](#namespace-boundary-and-shared-layer-preference)
- [Quickstart](#quickstart)
- [Development Workflow](#development-workflow)
- [CI + Release Workflow](#ci--release-workflow-manual-steps)
- [IRI & Versioning Policy](#iri--versioning-policy)

## Documentation and Governance

**Start here:**
- [Contributing Guide](CONTRIBUTING.md) - how to propose changes, terms, and PRs
- [Governance](GOVERNANCE.md) - current maintainers and placeholder governance process
- [Competency Questions](docs/COMPETENCY_QUESTIONS.md) - specific questions the ontology must answer
- [Conventions Guide](docs/CONVENTIONS.md) - detailed modeling conventions and patterns

**Technical references:**
- [Architecture Decision Records](docs/ADR.md) - key architectural decisions
- [Entrypoints](docs/entrypoints.md) - canonical build/publish/test entrypoints
- [ROBOT Setup Guide](docs/ROBOT_SETUP.md) - tool setup and usage
- Published ontology docs: <https://dfo-pacific-science.github.io/dfo-salmon-ontology/>

---

## Related Repositories and Namespaces

- **DFO-specific namespace (`gcdfo:`):** <https://w3id.org/gcdfo/salmon#>
- **Shared Salmon Domain namespace (`smn:`):** <https://w3id.org/smn>
- **Shared Salmon Domain repo:** <https://github.com/salmon-data-mobilization/salmon-domain-ontology>
- **Local sibling checkout expected by default build tooling:** `../salmon-domain-ontology/`

If a term is clearly **cross-organization, policy-neutral, and reusable**, it probably belongs in the shared Salmon Domain Ontology rather than here. If it is **DFO-specific, policy-program-specific, or intentionally profile-scoped**, it belongs in `gcdfo:`.

---

## Technical Overview

- **One file**: `ontology/dfo-salmon.ttl` (OWL/Turtle)
- **Hybrid approach**: OWL for formal relationships, SKOS for controlled vocabularies
- **Darwin Core aligned**: Uses DwC classes as top-level framework for interoperability; **implements Darwin Core Conceptual Model (DwC-CM) patterns**
- **OBO Foundry principles**: Open, interoperable, logically well-formed, scientifically accurate
- **Pragmatic imports**: imports shared `smn` plus MIREOT for BFO/IAO/DQV (~12 terms); prefix-only for PROV-O/RO/SKOS
  - local build/docs default resolves `https://w3id.org/smn` to the flat root file `../salmon-domain-ontology/salmon-domain-ontology.ttl` (via ROBOT catalog) when available
- **Upper-level/metamodel views**: maintained upstream in `smn` under `ontology/views/` as optional non-normative material; this repo keeps DFO core + optional overlays
- **Units**: QUDT/OM IRIs stored as literals (starter convention)
- **Community-aligned**: builds on NCEAS Salmon Ontology, ENVO, and OBO Foundry vocabularies

---

## Namespace Boundary and Shared-Layer Preference

>This section is the canonical shared-vs-DFO boundary policy for this repo. Other maintainer docs should link here rather than restating it.

- **`gcdfo:` is the DFO-specific layer.** This repo publishes and maintains the GC DFO Salmon Ontology namespace at `https://w3id.org/gcdfo/salmon#`.
- **`smn:` is the shared cross-organization layer.** When the Salmon Domain Ontology shared namespace is used downstream, prefer `smn:` terms first **where an approved shared term exists**.
- **Use `gcdfo:` for DFO-specific or deferred-profile semantics.** Terms such as DFO program/policy constructs — and any term intentionally kept out of the shared layer — remain canonical in `gcdfo:`.
- **Practical resolution order for downstream tools:** use `smn:` wherever a shared term exists in the Salmon Domain Ontology; use `gcdfo:` only for DFO-specific terms with no shared replacement.
- `ontology/dfo-salmon.ttl` explicitly imports `https://w3id.org/smn`.
- Local build/docs pipeline resolves that import to flat root `../salmon-domain-ontology/salmon-domain-ontology.ttl` (settable via `SMN_FLAT_TTL`) when present; otherwise it falls back to remote `https://w3id.org/smn` resolution.
- This repo now uses the hard-migrated shared identifiers directly for overlapping shared terms (for example: `Stock`, `Deme`, `Population`, `SurveyEvent`, `Escapement`, `ReferencePoint`, `MetricBenchmark`, `EnumerationMethod`, and related shared SKOS schemes/concepts/properties).
- **Transition note:** some upstream migration artifacts may still show draft shared IRIs under `salmon:` / `http://w3id.org/salmon/`. Treat those as pre-`smn` placeholders rather than the preferred steady-state target.
- Historical conservative-boundary notes remain in `docs/plans/2026-03-13-smn-boundary-passable.md` as change history, not current policy.
- Optional salmon metamodel views now live in the shared `smn` repo (`ontology/views/`) rather than being owned here.

## Quickstart

### For Contributors
1. **Read the [Contributing Guide](CONTRIBUTING.md)** and [Governance file](GOVERNANCE.md) first.
2. **Read the [Conventions Guide](docs/CONVENTIONS.md)** for detailed modeling guidelines.
3. **Read the [Competency Questions](docs/COMPETENCY_QUESTIONS.md)** to understand scope and goals.
4. **Check the boundary policy above** before minting a new `gcdfo:` term.
5. **Use Protégé Desktop** to edit `ontology/dfo-salmon.ttl` with OntoGraf for visualization.
6. **Use project targets for quality control**: `make reason` (or `make quality-check` for the full ROBOT report).
7. **Discuss changes** in GitHub Issues before creating PRs.
8. **Run validations**: run `make theme-coverage` (smoke), `make alpha-lint` (alpha migration lints), or `make test` (theme coverage + alpha-lint + ELK reasoning); use `make quality-check` for the full ROBOT report. Note: if using `devenv`/`nix` (optional), prefix commands with `devenv shell`.
9. **Single local+CI entrypoint**: `make ci` (runs tests, ROBOT quality-check, and `make docs-refresh` so that ontology + docs + serializations stay in sync).

### For Users
1. **Browse terms** using Protégé or online ontology browsers.
2. **Query data** using SPARQL with the ontology as a schema.
3. **Integrate** with Darwin Core-compatible systems for interoperability.

---

## Development Workflow

- **Single source of truth**: edit and review `ontology/dfo-salmon.ttl` on a development branch; the draft file is only an idea bank and is not read by tests or canonical docs publishing.
- **SPSR mapping source boundary**: canonical SPSR assessment/mapping artifacts live in `Br-Johnson/smn-data-gpt/assessments/spsr`; this repo's `work/` folder is an integration snapshot/working cache for ontology work (see `work/README.md`).
- **Theme navigation**: tag every term with 1–3 `gcdfo:theme` values from `gcdfo:ThemeScheme` directly in the canonical file; `gcdfo:ThemeScheme` and its member theme concepts are excluded from the missing-theme check.
- **Deprecated term-table extraction flow**: generated term tables and generated term-table SPARQL queries from `scripts/extract-term-tables.py` are local ad hoc artifacts only; they are not canonical docs artifacts and are not used for DSU/FADS sync.
- **Docs publishing**: `make docs-refresh` regenerates `docs/gcdfo.{ttl,owl}` via ROBOT and `docs/gcdfo.jsonld` via `rdflib` (JSON-LD is a JSON-based RDF serialization) from `ontology/dfo-salmon.ttl`, then refreshes the SKOS sections inside `docs/index.html` (it also enforces OWL Classes appearing before the SKOS sections on the rendered page).
  - `make docs-widoco` now builds `release/tmp/dfo-salmon-docs-input.ttl` with collapsed import closure first, so WIDOCO consumes the flat SMN root file instead of traversing modular imports when `SMN_FLAT_TTL` is available.
- **Release paths**: root-level `release/` is for transient local/CI build outputs; canonical published artifacts and immutable version snapshots live under `docs/` and `docs/releases/X.Y.Z/`.
- **OBO-style workflow**: use ROBOT for quality control and release management.
- **Pre-commit validation**: install pre-commit hooks (`pre-commit install`) to validate ontology before commit.
- **CI validation**: pull requests to `main` and pushes to `main` run ROBOT ELK reasoning + ROBOT report (with custom profile); CI runs `make ci` and fails if it produces uncommitted diffs.
- **Windows**: use WSL2 + `nix`/`direnv` (optional) or Git Bash; `make install-robot` fetches the pinned ROBOT jar used by CI/pre-commit.
- **GitHub-based collaboration**: all changes via Pull Requests with Issues for discussion.
- **Quality first**: use competency questions and design patterns to guide development.
- **Before creating terms**: search existing terms and check competency questions.
- **Document everything per the conventions checklist**: for OWL terms use `rdfs:label`, `iao:0000115`, and `rdfs:isDefinedBy`; add `iao:0000119` and/or `dcterms:source` when authoritative provenance exists; use `rdfs:comment` only for editorial notes.
- **Test with data**: validate terms with sample data and SPARQL queries.

**For detailed modeling conventions, see [GC DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md).**

**For Darwin Core Conceptual Model (DwC-CM) implementation guidance, see [Conventions Guide - DwC-CM Section](docs/CONVENTIONS.md#44-darwin-core-conceptual-model-dwc-cm-alignment).**

---

## CI + Release Workflow (manual steps)

**CI entrypoint:** `make ci` (or `devenv shell make ci` if you use nix/devenv). This runs tests, ROBOT quality-check, and `make docs-refresh`, so it regenerates `docs/` artifacts that must be committed before you push.

**Manual release steps (manual means you must do these yourself; CI does not publish releases):**

1. Update ontology header fields in `ontology/dfo-salmon.ttl`:
   - `dcterms:modified`
   - `owl:versionInfo`
   - `owl:versionIRI` (example: `https://w3id.org/gcdfo/salmon/0.0.999`)
   - `owl:priorVersion` (previous version IRI)
2. Run `make ci-sync-artifacts` (or `devenv shell make ci-sync-artifacts`) and commit regenerated artifacts from `docs/` (including `docs/gcdfo.{ttl,owl,jsonld}`, `docs/index.html`, and `docs/index-en.html` when changed).
3. Run `make release-snapshot VERSION=X.Y.Z` (or `devenv shell make release-snapshot VERSION=X.Y.Z`) to create a release snapshot (an immutable copy under `docs/releases/X.Y.Z/`).
4. Commit and push `docs/releases/X.Y.Z/` so GitHub Pages serves the versioned files.
5. Optional: tag the release (a tag is a Git label for a specific commit, e.g., `v0.0.999`).

**W3ID redirects:** You do **not** need a new W3ID PR for each release unless the hosting base URL changes; the existing redirect rules already handle `X.Y.Z` versions.

---

## IRI & Versioning Policy

- **Base IRI**: `https://w3id.org/gcdfo/salmon#`
- **Instances**: mint under same base (e.g., `…#Stock/SkeenaSockeye`)
- **Versioning**: tag GitHub releases and maintain version info in ontology header
- **Version IRI (recommended)**: `https://w3id.org/gcdfo/salmon/<version>` (resolves via W3ID redirects)
- **Version artifacts (hosted)**: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/releases/<version>/` (immutable snapshot served by GitHub Pages)
- **For detailed conventions**: see [DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md)

---
