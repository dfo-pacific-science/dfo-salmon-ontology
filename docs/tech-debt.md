# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-08-16 — A failed `make docs-widoco` can re-baseline WebVOWL output to raw generator bytes

**What**: `docs-widoco` snapshots the working-tree `docs/webvowl/data/ontology.json` as the
normalizer baseline, then `rsync` overwrites that path with fresh WIDOCO output before the
normalizer runs. If the recipe fails after the rsync — which it now does loudly — the working
tree is left holding raw generator bytes. Re-running `make docs-widoco` adopts those raw bytes
as the baseline, the normalizer finds the new raw output semantically equal to them, restores
them, and the build goes green over un-normalized output.

**Why it exists**: the baseline is taken from the working tree so that repeated local refreshes
compare against the previous local run rather than against the last commit.

**Impact**: local only. CI checks out clean, so its baseline is always the committed file, and
the drift check now covers `docs/webvowl/data/ontology.json`, so raw output pushed from a
poisoned local baseline fails CI. Locally, run
`git checkout -- docs/webvowl/data/ontology.json` before retrying a failed docs build.

**Intended fix**: take the baseline from `git show HEAD:docs/webvowl/data/ontology.json` —
which `scripts/normalize_webvowl_json.py` already implements as its fallback in
`load_git_head_text` — instead of from the working-tree copy.

## Resolved Technical Debt

### 2026-08-16 — WebVOWL output-stabilization gate was reporting success while doing nothing

**Resolved Date**: 2026-08-16
**Resolution**: three compounding faults, all in the path guarding
`docs/webvowl/data/ontology.json`. (1) `scripts/normalize_webvowl_json.py` aborted on every run
since PR #78 because the merged import closure emits three `xsd:gYear` datatype nodes and the
class key required `(type, iri)` to be unique; colliding keys are now widened with the node's
property-wiring context instead ([ADR-007](adr/007-webvowl-duplicate-node-disambiguation.md)).
(2) The `docs-widoco` recipe was one `;`-separated shell command with no `set -e`, so make took
the exit status of its trailing `echo` and printed success over the crash; the recipe now runs
under `set -e`, as does `release-snapshot`, which had the same shape. (3) `.github/workflows/ci.yml`
excluded the file from its uncommitted-changes check, so nothing downstream noticed; the
exclusion is removed now that the file is byte-stable across consecutive `make ci` runs. The
committed artifact was re-baselined once from raw generator output to the normalizer's own
rendering, so the next real ontology change produces a readable diff rather than a whole-file
reformat.

**Lessons Learned**: a quality gate needs a test that it can still fail. All three faults were
individually visible and individually survivable; what made them a placebo was that each one
hid the next. When a recipe chains commands with `;`, make only ever sees the last one — and an
exclusion added to silence pre-fix churn outlives the churn unless something forces the question.


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
