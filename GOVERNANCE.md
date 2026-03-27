# Governance

## Purpose

This repository publishes and maintains the DFO-specific salmon ontology namespace:

- **Namespace:** `https://w3id.org/gcdfo/salmon#`
- **Canonical ontology source:** `ontology/dfo-salmon.ttl`

This governance file is the human-maintainer companion to the technical runbook in [README.md](README.md) and the contribution path in [CONTRIBUTING.md](CONTRIBUTING.md).

## Current Maintainers

### Maintainer

- **Tom Bird**
  - current maintainer for the repo
  - coordinates review/merge decisions
  - coordinates releases and publication-facing changes
  - is actively recruiting additional maintainers

## Organizational Stewardship

- **Fishery & Assessment Data Section (FADS) Data Stewardship Unit, DFO Pacific Science**
  - organizational stewardship home for the ontology work
  - contact route: <mailto:FADSDataStewardship-GestiondesdonneesSFDA@dfo-mpo.gc.ca>

## Interested in helping maintain this repo?

We are actively looking for additional maintainers.

Good candidates include people who want to help with one or more of the following:

- ontology modeling and semantic review
- DFO policy/program/domain review
- issue triage and contributor support
- release/publishing checks
- shared-vs-DFO boundary review (`smn:` vs `gcdfo:`)

You do **not** need to do all of those to be useful. A narrow, reliable maintainer role is better than a grand title with no follow-through.

### How to express interest

1. Open a GitHub issue in this repo and say you are interested in maintainership, or raise it in an existing coordination thread.
2. State the kind of role you want to help with (for example: domain review, ontology modeling, contributor support, or release support).
3. The maintainers follow up and, if it makes sense, this file gets updated.

## Additional Maintainers

- **No additional formal maintainers are named yet.**
- This is expected to change as people are invited and agree to take on maintainer responsibilities.
- When that happens, their names should be added here directly.

## What Maintainers Are Expected To Do

Maintainers are expected to:

- build consesus on authoritative term definitions and their relationships
- support on-boarding and use of the ontology
- review or route issues and pull requests
- guard the boundary between DFO-specific `gcdfo:` terms and shared `smn:` (salmon domain ontology) terms
- coordinate release/publishing steps when docs or ontology artifacts change
- keep contributor guidance usable and current

## Placeholder Decision Rules

Until a broader maintainer group is in place:

- **Routine documentation or low-risk repo changes:** the acting maintainer can decide.
- **Ontology boundary questions or publication-facing changes:** seek review and discussion where practical.
- **If a decision is time-sensitive and governance is still unclear:** Brett Johnson acts as the interim tie-breaker.

This is intentionally temporary and should be revised once more maintainers are active.

## Adding Maintainers (placeholder process)

For now, the process is simple:

1. A candidate is invited or volunteers.
2. The candidate agrees to take on maintainer responsibilities.
3. Repo access/review responsibilities are granted as appropriate.
4. This file is updated to name the maintainer.
5. Other docs or metadata can be updated afterward as needed.

## Relationship to the shared Salmon Domain Ontology

This repo governs the **DFO-specific** ontology/profile layer.

- Shared cross-organization terms belong in the Salmon Domain Ontology (`smn:`): <https://w3id.org/smn>
- Shared repo: <https://github.com/salmon-data-mobilization/salmon-domain-ontology>

The canonical shared-vs-DFO boundary policy for this repo lives in [README.md#namespace-boundary-and-shared-layer-preference](README.md#namespace-boundary-and-shared-layer-preference).

## Related Documents

- [README.md](README.md) - technical runbook
- [CONTRIBUTING.md](CONTRIBUTING.md) - how to propose changes
- [docs/CONVENTIONS.md](docs/CONVENTIONS.md) - modeling conventions
