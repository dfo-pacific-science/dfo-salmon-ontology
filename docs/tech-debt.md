# Tech Debt Log

This file tracks active technical debt in the DFO Salmon Ontology repo.
Keep it short, specific, and tied to real boundary/publishing risks.

## Active Technical Debt

### 2026-08-16 — Nothing checks that `docs/releases/<version>/` still matches `docs/`

**What**: `make release-snapshot` copies `docs/gcdfo.{ttl,owl,jsonld}` into
`docs/releases/<version>/` once. Nothing re-checks the copy afterwards. A merge
into the release branch after the snapshot is cut leaves the snapshot holding
superseded bytes, and every gate stays green: CI's clean-tree check only
verifies that `make ci` regenerates `docs/` reproducibly, and `make ci` does not
write `docs/releases/` at all.

**Impact**: caught on this release. `docs/releases/0.0.9/` was cut before PR #77
merged, so it carried the pre-WSP "A group of fish…" `gcdfo:ConservationUnit`
definition while `docs/gcdfo.ttl` carried "A group of wild salmon…". Publishing
that would have frozen a known-superseded definition into an immutable release
snapshot — the exact outcome the decision to land #77 before 0.0.9 was meant to
prevent. Re-cut with `FORCE=1`; the diff was one line per serialization.

**Why it is debt rather than a fixed bug**: the re-cut fixes this release. The
next release branch that takes a merge after snapshotting has the same hole, and
the failure is silent, so it will be found by inspection or not at all.

**Intended fix path**: a CI check comparing each `docs/releases/<version>/` file
against `docs/` **only when `<version>` equals the current `owl:versionInfo`** —
older snapshots must keep diverging, that is what makes them snapshots. Cheap,
and it fails exactly when a release branch has moved under its own snapshot.

**Retires when**: a gate in `make ci` fails on a `docs/releases/<current
version>/` file that does not match its `docs/` counterpart.

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

### 2026-03-15 — `make ci` / `make docs-refresh` WebVOWL churn stabilized (first attempt; superseded)

**Resolved Date**: 2026-03-15, but **the fix did not hold** — see the 2026-08-16 entry above.
Read the two together; this one alone overstates the state of the repo between
2026-08-14 (PR #78) and 2026-08-16 (PR #82).

**What was actually done on 2026-03-15**: `make docs-widoco` fingerprinted the deterministic
merged ontology input plus the pinned WIDOCO version into `docs/webvowl/data/ontology.stamp`
and, whenever that fingerprint was unchanged, restored the pre-run
`docs/webvowl/data/ontology.json` bytes via `scripts/stabilize_webvowl_output.py`. Byte-restore
on an unchanged-input hash — not a semantic comparison.

**What superseded it**: PR #78 replaced that script with `scripts/normalize_webvowl_json.py`,
which compares the generated file against the tracked baseline *semantically*, restores the
exact baseline bytes for true no-op refreshes, and normalizes ids/order when the graph meaning
changes ([ADR-007](adr/007-webvowl-duplicate-node-disambiguation.md)). PR #78 removed the
stabilizer from the `docs-widoco` recipe and left both files behind as unreferenced ghost
code: `docs/webvowl/data/ontology.stamp` is deleted, and `scripts/stabilize_webvowl_output.py`
awaits the sign-off `AGENTS.md` requires before anything under `scripts/` is removed.

**Why this went unnoticed for five months**: the docs did not go stale — going stale leaves a
visible mismatch. PR #78 rewrote this entry's *Resolution* text **in place**, and
`docs/context/widoco.md` with it, so both read as accurate descriptions of the normalizer while
keeping the 2026-03-15 heading that had resolved a different implementation. That is the actual
defect. A stale doc says something the code no longer does and invites the question; an
in-place rewrite says something the code *does* do and destroys the only record that a
replacement ever happened, so nothing invites the question — the superseded approach keeps
looking current, its leftover files keep looking wired, and the log offers no seam where a
reader could notice the substitution.

**What made the claim false in the interim**: the replacement crashed on every run and the
build reported success anyway, so between PR #78 and PR #82 nothing stabilized the artifact at
all — while this entry sat in the Resolved section asserting that something did.

**Re-verification hook**: do not trust this entry on its own wording; it has been wrong before.
Run `SMN_FLAT_TTL=/nonexistent/smn.ttl make ci` twice and confirm
`git status --porcelain --untracked-files=all` is empty both times. Since PR #82 removed the
`docs/webvowl/data/ontology.json` exclusion from `.github/workflows/ci.yml`, CI runs that same
check on every PR, so a regression here fails the build rather than needing anyone to re-read
this file.

**Lessons Learned**: when a mechanism is replaced, do not edit the entry that resolved the old
one — append a new entry and mark the old one superseded. Rewriting in place is not
documentation maintenance; it is overwriting the evidence that a replacement happened, which
is why nobody went looking for the files the replacement orphaned. Keep the original date
attached to the original mechanism, name the successor, and attach a command that re-checks
the claim — otherwise the log reads as evidence of a working gate during exactly the window
when the gate was a placebo.

### 2026-03-15 — Shared-term overlap cleanup completed

**Resolved Date**: 2026-03-15
**Resolution**: overlapping shared terms in `ontology/dfo-salmon.ttl` now use `smn:` directly, eliminating duplicated local `gcdfo:` subjects for those shared identifiers.
**Lessons Learned**: use explicit boundary exceptions instead of broad textual substitution, and run overlap/self-loop checks immediately after migration.

### 2026-03-13 — Agent/doc scaffold files were being left gitignored in some repos

**Resolved Date**: 2026-03-13
**Resolution**: updated the shared `update-agent.sh` cleanup rules and removed stale ignore entries from this repo.
**Lessons Learned**: exact-line cleanup is too brittle for repo-template drift; remove common legacy variants, not just one spelling.
