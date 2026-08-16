# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-08-16 — Term definitions are authored in four places, not derived

**What**: a `gcdfo:` term definition string exists as four independently
authored copies. `gcdfo:ConservationUnit` is the worked example: `iao:0000115`
in `ontology/dfo-salmon.ttl` (canonical), `skos:definition` in the curated
`ontology/views/wsp-composite-escapement-view.ttl`, `iao:0000115` in the
`draft/dfo-salmon-draft.ttl` idea bank, and the `docs/` publication artifacts.

**Why it happened**: only the `docs/` copies are derived. `make docs-refresh`
regenerates `docs/gcdfo.{ttl,owl,jsonld}`, `docs/index*.html`, and
`docs/webvowl/data/ontology.json` from `ontology/dfo-salmon.ttl`, and the CI
drift gate enforces that. Nothing derives or checks the view or the draft, so
they drift silently and a definition edit looks complete when it is not.

**Impact**: PR #77 shipped the WSP wording fix to the canonical file alone and
the drift gate failed on the unregenerated `docs/` artifacts; the two authored
TTL copies would have kept the superseded "A group of fish…" wording with no
signal at all. Anyone loading the WSP composite-escapement view gets a
definition that contradicts the ontology it annotates.

**Intended fix path**: the view is the copy worth removing — it re-states a
definition it does not own, so either generate its `skos:definition` from
`ontology/dfo-salmon.ttl` at build time or drop the predicate and let consumers
dereference the term. The draft is a documented idea bank
(`README.md`, `CONTRIBUTING.md`) and stays authored; a lint that flags
definition strings differing between the draft and the canonical file would
make its drift visible. Do the view first — it is published material.

**Retires when**: no file outside `ontology/dfo-salmon.ttl`, the generated
`docs/` tree, and the immutable `docs/releases/*/` snapshots authors an
`iao:0000115`/`skos:definition` string for a `gcdfo:` term, or a CI check fails
when one diverges from the canonical file.

### 2026-08-16 — `ontology/views/` review artifacts regenerate nondeterministically

**What**: `scripts/generate_wsp_composite_escapement_review_artifacts.py`
writes a different `ontology/views/wsp-composite-escapement-review.graphml` on
every run. Three consecutive runs on an unchanged input produced three distinct
files (edge blocks re-ordered; the `.md` output is stable).

**Why it happened**: the graphml edge emission iterates unordered collections,
so ordering follows set/dict iteration rather than an explicit sort.

**Impact**: the script cannot be used to verify that a view edit propagated —
every run reports a change. It is not wired into `make ci`, so it does not
break the drift gate; it just makes the artifact untrustworthy as a diff, and
regenerating it buries a real edit under thousands of columns of churn. PR #77
therefore updated the view TTL without regenerating the graphml.

**Intended fix path**: sort the edge (and node) emission by a stable key —
IRI/label under C ordering — before writing, then regenerate once so the
committed artifact matches a deterministic run.

**Retires when**: two consecutive runs of the script on an unchanged
`ontology/views/wsp-composite-escapement-view.ttl` produce byte-identical
`.graphml` output.

### 2026-08-16 — Alignment overlays restate mappings the shared layer already owns

**What**: `ontology/modules/alignment-main.ttl` and `alignment-research.ttl` assert
cross-framework `skos:*Match` rows that the imported `smn` closure already asserts —
`sosa:Observation`↔`dwc:Occurrence`, `sosa:Sample`↔`dwc:MaterialEntity`,
`sosa:Procedure`↔`dwc:Protocol`, `sosa:Property`↔`iadopt:Property` and, after the ADR-008
retarget, several `smn:` class and property bridges. Where the restatement agrees it is a
duplicate triple in the merged closure and changes nothing.

**Why it is debt**: where a restatement *disagrees*, it silently contradicts upstream. Two
cases found on 2026-08-16: `sosa:Sampling skos:closeMatch dwc:Event` against upstream's
`skos:broadMatch` (fixed, ADR-008), and `iadopt:Variable skos:closeMatch sosa:Property`
against upstream's more precise `skos:closeMatch sosa:ObservableProperty` (left as-is —
changing a crosswalk claim is a domain decision, not a review fix).

**Impact**: low and now bounded. `make check-modules` fails on any pair carrying two
different `skos:*Match` predicates, so a future divergence of this shape cannot land quietly.
It does not catch a restatement that is merely looser than upstream, like the
`iadopt:Variable` row.

**Intended fix**: decide per row whether the overlay should own a cross-framework mapping at
all. Rows that only echo `smn` belong upstream; the overlays should carry what DFO adds. Do
this with a domain reviewer, not as a cleanup pass.

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
