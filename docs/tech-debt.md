# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-03-15 — `make ci` / `make docs-refresh` still emits nondeterministic WebVOWL artifact churn

**Description**
`docs/webvowl/data/ontology.json` can be reordered across repeated doc-generation runs even when `ontology/dfo-salmon.ttl` is unchanged.

**Rationale**
The current pipeline remains useful, but non-deterministic generated files are noisy for reviewers and make clean-tree checks difficult.

**Impact**
- **Severity**: Medium
- **Affected Areas**: local verification, review quality, CI artifact checks
- **User Impact**: low direct product risk, higher maintainer friction
- **Maintenance Cost**: repeated artifact triage and noisy diffs

**Remediation**
- **Effort Estimate**: Small-Medium
- **Approach**: add deterministic JSON serialization normalization after WebVOWL export (or formalize `webvowl/data/ontology.json` as non-gated output in CI)
- **Prerequisites**: decision on whether WebVOWL is canonical or convenience output
- **Risk**: low semantic risk, moderate workflow churn if we alter gating behavior

**Status**: Active

**Related Issues/PRs**
- `Makefile`
- `docs/webvowl/data/ontology.json`

## Resolved Technical Debt

### 2026-03-15 — Shared-vs-DFO bridge guidance canonicalized

**Resolved Date**: 2026-03-15
**Resolution**: kept `README.md#namespace-boundary-and-shared-layer-preference` as the canonical boundary policy, and reduced `docs/entrypoints.md` plus `docs/context/w3id.md` to scope/reference notes that link back to it.
**Lessons Learned**: keep namespace policy in one high-visibility maintainer doc; contextual docs should point at it rather than paraphrasing it.

### 2026-03-15 — Shared-term overlap cleanup completed

**Resolved Date**: 2026-03-15
**Resolution**: overlapping shared terms in `ontology/dfo-salmon.ttl` now use `smn:` directly, eliminating duplicated local `gcdfo:` subjects for those shared identifiers.
**Lessons Learned**: use explicit boundary exceptions instead of broad textual substitution, and run overlap/self-loop checks immediately after migration.

### 2026-03-13 — Agent/doc scaffold files were being left gitignored in some repos

**Resolved Date**: 2026-03-13
**Resolution**: updated the shared `update-agent.sh` cleanup rules and removed stale ignore entries from this repo.
**Lessons Learned**: exact-line cleanup is too brittle for repo-template drift; remove common legacy variants, not just one spelling.
