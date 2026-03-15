# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-03-15 — Shared-vs-DFO bridge guidance is spread across multiple docs

**Description**
Boundary guidance for `gcdfo:` vs `smn:` is documented in several places (`README.md`, `docs/entrypoints.md`, `docs/context/w3id.md`, and migration artifacts).

**Rationale**
This reduces duplication of source-of-truth questions while the namespace migration is still in active review, but it increases drift risk.

**Impact**
- **Severity**: Low
- **Affected Areas**: maintainer docs, onboarding, publication boundaries
- **User Impact**: contributors can land in stale guidance if they only read one doc
- **Maintenance Cost**: moderate doc-sync tax when a migration assumption changes

**Remediation**
- **Effort Estimate**: Small
- **Approach**: consolidate boundary policy into one canonical doc and move older notes to historical references only
- **Prerequisites**: migration contract stays stable for a few days
- **Risk**: low

**Status**: Active

**Related Issues/PRs**
- `README.md`
- `docs/entrypoints.md`
- `docs/context/w3id.md`

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

### 2026-03-15 — Shared-term overlap cleanup completed

**Resolved Date**: 2026-03-15
**Resolution**: overlapping shared terms in `ontology/dfo-salmon.ttl` now use `smn:` directly, eliminating duplicated local `gcdfo:` subjects for those shared identifiers.
**Lessons Learned**: use explicit boundary exceptions instead of broad textual substitution, and run overlap/self-loop checks immediately after migration.

### 2026-03-13 — Agent/doc scaffold files were being left gitignored in some repos

**Resolved Date**: 2026-03-13
**Resolution**: updated the shared `update-agent.sh` cleanup rules and removed stale ignore entries from this repo.
**Lessons Learned**: exact-line cleanup is too brittle for repo-template drift; remove common legacy variants, not just one spelling.
