# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-08-16 — Alignment overlays restate mappings the shared layer already owns

**What**: `ontology/modules/alignment-main.ttl` and `alignment-research.ttl` assert
cross-framework `skos:*Match` rows that the imported `smn` closure already asserts —
`sosa:Observation`↔`dwc:Occurrence`, `sosa:Sample`↔`dwc:MaterialEntity`,
`sosa:Procedure`↔`dwc:Protocol`, `sosa:Property`↔`iadopt:Property` and, after the ADR-007
retarget, several `smn:` class and property bridges. Where the restatement agrees it is a
duplicate triple in the merged closure and changes nothing.

**Why it is debt**: where a restatement *disagrees*, it silently contradicts upstream. Two
cases found on 2026-08-16: `sosa:Sampling skos:closeMatch dwc:Event` against upstream's
`skos:broadMatch` (fixed, ADR-007), and `iadopt:Variable skos:closeMatch sosa:Property`
against upstream's more precise `skos:closeMatch sosa:ObservableProperty` (left as-is —
changing a crosswalk claim is a domain decision, not a review fix).

**Impact**: low and now bounded. `make check-modules` fails on any pair carrying two
different `skos:*Match` predicates, so a future divergence of this shape cannot land quietly.
It does not catch a restatement that is merely looser than upstream, like the
`iadopt:Variable` row.

**Intended fix**: decide per row whether the overlay should own a cross-framework mapping at
all. Rows that only echo `smn` belong upstream; the overlays should carry what DFO adds. Do
this with a domain reviewer, not as a cleanup pass.

## Resolved Technical Debt

### 2026-03-15 — Shared-vs-DFO bridge guidance canonicalized

**Resolved Date**: 2026-03-15
**Resolution**: kept `README.md#namespace-boundary-and-shared-layer-preference` as the canonical boundary policy, and reduced `docs/entrypoints.md` plus `docs/context/w3id.md` to scope/reference notes that link back to it.
**Lessons Learned**: keep namespace policy in one high-visibility maintainer doc; contextual docs should point at it rather than paraphrasing it.

### 2026-03-15 — `make ci` / `make docs-refresh` WebVOWL churn stabilized

**Resolved Date**: 2026-03-15
**Resolution**: `make docs-widoco` now compares the generated `docs/webvowl/data/ontology.json` against the prior tracked baseline semantically, restores the exact baseline bytes for no-op refreshes, and normalizes ids/order when the graph meaning changes. That keeps repeated doc refreshes readable without changing ontology semantics.
**Lessons Learned**: when a generator is semantically stable but serialization-noisy, compare meaning first; preserve prior bytes for true no-op runs and normalize deterministically when real changes land.

### 2026-03-15 — Shared-term overlap cleanup completed

**Resolved Date**: 2026-03-15
**Resolution**: overlapping shared terms in `ontology/dfo-salmon.ttl` now use `smn:` directly, eliminating duplicated local `gcdfo:` subjects for those shared identifiers.
**Lessons Learned**: use explicit boundary exceptions instead of broad textual substitution, and run overlap/self-loop checks immediately after migration.

### 2026-03-13 — Agent/doc scaffold files were being left gitignored in some repos

**Resolved Date**: 2026-03-13
**Resolution**: updated the shared `update-agent.sh` cleanup rules and removed stale ignore entries from this repo.
**Lessons Learned**: exact-line cleanup is too brittle for repo-template drift; remove common legacy variants, not just one spelling.
