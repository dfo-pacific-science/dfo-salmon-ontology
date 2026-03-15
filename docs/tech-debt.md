# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-03-15 — Shared-term overlap cleanup completed

**Description**
The DFO ontology now uses shared `smn:` IRIs directly for overlapping shared terms instead of maintaining parallel `gcdfo:` duplicates.

**Status**: Resolved

**Notes**
- Remaining `gcdfo:` identifiers are intended to be DFO-specific.
- Historical conservative-boundary notes remain in `docs/plans/2026-03-13-smn-boundary-passable.md` as history only.

### 2026-03-13 — Shared-vs-DFO bridge logic is documented in multiple places

**Description**
The repo currently explains the `gcdfo:` vs `smn:` split in several docs (`README.md`, `docs/entrypoints.md`, `docs/context/w3id.md`, migration notes, and branch-specific cleanup notes).

**Rationale**
This was the fastest honest way to stop boundary drift while the shared namespace was stabilizing.

**Impact**
- **Severity**: Low
- **Affected Areas**: maintainer docs, onboarding, publication coherence
- **User Impact**: low direct user pain, but contributors can read stale wording if one doc is updated and another is forgotten
- **Maintenance Cost**: small but annoying doc-sync tax

**Remediation**
- **Effort Estimate**: Small
- **Approach**: consolidate steady-state boundary guidance into one canonical maintainer doc and keep the other docs short/reference-style
- **Prerequisites**: boundary rules settle enough that we stop rewriting them every other day
- **Risk**: low

**Status**: Active

**Related Issues/PRs**
- `README.md`
- `docs/entrypoints.md`
- `docs/context/w3id.md`

### 2026-03-13 — `make ci` can leave nondeterministic generated docs churn

**Description**
Verification after the conservative `smn` boundary pass showed the ontology and human-authored boundary docs are aligned, but `make ci`/`make docs-refresh` can still rewrite tracked generated artifacts even when the source ontology has not changed.

Observed locally on this branch:
- `docs/webvowl/data/ontology.json` reorders repeated values between runs
- `docs/gcdfo.owl` can pick up whitespace-only churn

**Rationale**
This is a build determinism problem, not an ontology-boundary problem, but it now sits in the critical path because repo guidance says generated docs artifacts should stay commit-clean after `make ci`.

**Impact**
- **Severity**: Medium
- **Affected Areas**: local verification, clean-tree CI expectations, reviewability of generated docs commits
- **User Impact**: maintainers can get noisy diffs that do not represent real ontology changes
- **Maintenance Cost**: repeated artifact triage and unnecessary review noise

**Remediation**
- **Effort Estimate**: Small-Medium
- **Approach**: add a canonicalization/normalization step for generated WebVOWL/OWL outputs, or stop treating nondeterministic artifacts as clean-tree blockers until generation is stabilized
- **Prerequisites**: decide which generated files are publication-critical vs convenience artifacts
- **Risk**: low semantic risk, moderate workflow annoyance if left unresolved

**Status**: Active

**Related Issues/PRs**
- `Makefile`
- `docs/webvowl/data/ontology.json`
- `docs/gcdfo.owl`

## Resolved Technical Debt

### 2026-03-13 — Agent/doc scaffold files were being left gitignored in some repos

**Resolved Date**: 2026-03-13
**Resolution**: updated the shared `update-agent.sh` cleanup rules and removed the stale ignore entries from this repo.
**Lessons Learned**: exact-line cleanup is too brittle for repo-template drift; remove the common legacy variants, not just one spelling.
