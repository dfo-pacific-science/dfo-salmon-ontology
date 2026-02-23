# GC DFO Salmon Ontology

**Namespace:** `https://w3id.org/gcdfo/salmon#` (prefix: `gcdfo:`)  
**License:** CC-BY 4.0  
**Status:** Version 0.0.999 (pre-1.0 “beta”)

The GC DFO Salmon Ontology is a **data stewardship and operational process ontology** designed to provide a semantic framework for managing, integrating, and stewarding Pacific salmon data across Fisheries and Oceans Canada (DFO).

**Goal:** Make salmon data interoperable, discoverable, and analyzable with minimal friction for scientists, data stewards, and managers.

**Rule of thumb:** `/ontology/dfo-salmon.ttl` contains **schema only** (no instance facts, measurements, or survey rows). Instance data examples belong in `/ontology/examples/` and are *not* shipped inside the core ontology file.

---

## Table of Contents

- [Quickstart](#quickstart)
- [Current Scope](#ontology-scope-current)
- [Development Workflow](#development-workflow)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [Acknowledgments](#acknowledgments)

## Documentation

**For Contributors:**
- [Competency Questions](docs/COMPETENCY_QUESTIONS.md) - Specific questions the ontology must answer
- [Conventions Guide](docs/CONVENTIONS.md) - Detailed modeling conventions and patterns
- [Contributing Guide](CONTRIBUTING.md) - Contribution workflow and guidelines

**Technical References:**
- [Architecture Decision Records](docs/ADR.md) - Key architectural decisions
- [ROBOT Setup Guide](docs/ROBOT_SETUP.md) - Tool setup and usage

---

## Technical Overview

- **One file**: `dfo-salmon.ttl` (OWL/Turtle)
- **Hybrid approach**: OWL for formal relationships, SKOS for controlled vocabularies
- **Darwin Core aligned**: Uses DwC classes as top-level framework for interoperability; **implements Darwin Core Conceptual Model (DwC-CM) patterns**
- **OBO Foundry principles**: Open, interoperable, logically well-formed, scientifically accurate
- **Pragmatic imports**: MIREOT for BFO/IAO/DQV (~12 terms); prefix-only for PROV-O/RO/SKOS
- **Upper ontology**: BFO grounding for process/entity hierarchy
- **Units**: QUDT/OM IRIs stored as literals (starter convention)
- **Community-aligned**: builds on NCEAS Salmon Ontology, ENVO, and OBO Foundry vocabularies

---

## Quickstart

### For Contributors
1. **Read the [Conventions Guide](docs/CONVENTIONS.md)** for detailed modeling guidelines
2. **Read the [Competency Questions](docs/COMPETENCY_QUESTIONS.md)** to understand scope and goals
3. **Use Protégé Desktop** to edit `dfo-salmon.ttl` with OntoGraf for visualization
4. **Use ROBOT** for quality control: `robot reason --input dfo-salmon.ttl --reasoner ELK`
5. **Discuss changes** in GitHub Issues before creating PRs
6. **Follow OBO practices**: Use competency questions, design patterns, and quality checklists
7. **Run validations**: Run `make theme-coverage` (smoke) or `make test` (theme coverage + ELK reasoning); use `make quality-check` for the full ROBOT report. Note: If using `devenv`/`nix` (optional), prefix commands with `devenv shell`.
8. **Single local+CI entrypoint**: `make ci` (runs tests, ROBOT quality-check, and `make docs-refresh` so that ontology + docs + serializations stay in sync)

### For Users
1. **Browse terms** using Protégé or online ontology browsers
2. **Query data** using SPARQL with the ontology as a schema
3. **Integrate** with Darwin Core-compatible systems for interoperability

---

## Development Workflow

- **Single source of truth**: Edit and review `ontology/dfo-salmon.ttl` on a development branch; the draft file is only an idea bank and is not read by tests or term-table extraction.
- **SPSR mapping source boundary**: canonical SPSR assessment/mapping artifacts live in `Br-Johnson/smn-data-gpt/assessments/spsr`; this repo's `work/` folder is an integration snapshot/working cache for ontology work (see `work/README.md`).
- **Theme navigation**: Tag every term with 1–3 `gcdfo:theme` values from `gcdfo:ThemeScheme` directly in the canonical file; `gcdfo:ThemeScheme` and its member theme concepts are excluded from the missing-theme check; any term tables generated from these annotations are local build artifacts (not source-controlled outputs).
- **Docs publishing**: `make docs-refresh` regenerates `docs/gcdfo.{ttl,owl}` via ROBOT and `docs/gcdfo.jsonld` via `rdflib` (JSON-LD is a JSON-based RDF serialization) from `ontology/dfo-salmon.ttl`, then refreshes the SKOS sections inside `docs/index.html` (it also enforces OWL Classes appearing before the SKOS sections on the rendered page).
- **Release paths**: root-level `release/` is for transient local/CI build outputs; canonical published artifacts and immutable version snapshots live under `docs/` and `docs/releases/X.Y.Z/`.
- **OBO-style workflow**: Use ROBOT for quality control and release management
- **Pre-commit validation**: Install pre-commit hooks (`pre-commit install`) to validate ontology before commit
- **CI validation**: Pushes/PRs run ROBOT ELK reasoning + ROBOT report (with custom profile); CI (continuous integration, automated checks on every push) runs `make ci` and fails if it produces uncommitted diffs.
- **Windows**: Use WSL2 + `nix`/`direnv` (optional) or Git Bash; `make install-robot` fetches the pinned ROBOT jar used by CI/pre-commit
- **GitHub-based collaboration**: All changes via Pull Requests with Issues for discussion
- **Quality first**: Use competency questions and design patterns to guide development
- **Before creating terms**: Search existing terms and check competency questions
- **Document everything**: Always include `rdfs:comment` and `dcterms:source`
- **Test with data**: Validate terms with sample data and SPARQL queries

**For detailed modeling conventions, see [GC DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md).**

**For Darwin Core Conceptual Model (DwC-CM) implementation guidance, see [Conventions Guide - DwC-CM Section](docs/CONVENTIONS.md#44-darwin-core-conceptual-model-dwc-cm-alignment).**



---


---

## CI + Release Workflow (manual steps)

**CI entrypoint:** `devenv shell make ci` (CI means automated checks that run on every push; this command runs tests, ROBOT quality-check, and `make docs-refresh`, so it will regenerate `docs/` and must be committed before you push).

**Manual release steps (manual means you must do these yourself; CI does not publish releases):**

1. Update ontology header fields in `ontology/dfo-salmon.ttl`:
   - `dcterms:modified`
   - `owl:versionInfo`
   - `owl:versionIRI` (example: `https://w3id.org/gcdfo/salmon/0.0.999`)
   - `owl:priorVersion` (previous version IRI)
2. Run `devenv shell make ci` and commit regenerated artifacts (`docs/gcdfo.{ttl,owl,jsonld}` and `docs/index.html`).
3. Run `devenv shell make release-snapshot VERSION=X.Y.Z` to create a release snapshot (a release snapshot is an immutable copy under `docs/releases/X.Y.Z/`).
4. Commit and push `docs/releases/X.Y.Z/` so GitHub Pages serves the versioned files.
5. Optional: tag the release (a tag is a Git label for a specific commit, e.g., `v0.0.999`).

**W3ID redirects:** You do **not** need a new W3ID PR for each release unless the hosting base URL changes; the existing redirect rules already handle `X.Y.Z` versions.

---

## IRI & Versioning Policy

- **Base IRI**: `https://w3id.org/gcdfo/salmon#`
- **Instances**: mint under same base (e.g., `…#Stock/SkeenaSockeye`)
- **Versioning**: Tag GitHub releases, maintain version info in ontology header
- **Version IRI (recommended)**: `https://w3id.org/gcdfo/salmon/<version>` (resolves via w3id redirects)
- **Version artifacts (hosted)**: `https://dfo-pacific-science.github.io/dfo-salmon-ontology/releases/<version>/` (immutable snapshot served by GitHub Pages)
- **For detailed conventions**: See [DFO Salmon Ontology Conventions Guide](docs/CONVENTIONS.md)

---
