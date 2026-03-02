# Final Check — Documentation Coherence Audit (2026-02-25)

## Scope audited
- `README.md`
- `docs/entrypoints.md`
- `docs/todo_list.md`
- `docs/CONVENTIONS.md` (reference checks only)
- `docs/ROBOT_SETUP.md`
- `docs/context/*` key files

## Source of truth used for coherence checks
- `Makefile` (targets/workflows): `Makefile:L42-L250`
- CI workflow: `.github/workflows/ci.yml:L3-L84`

## Executive summary
Docs are mostly aligned on canonical make targets (`make ci`, `make docs-refresh`, `make release-snapshot`). Deprecated term-table flow is clearly marked as non-canonical in all key docs. Main remaining risks are command-path drift (`robot` CLI vs pinned jar/make targets), inconsistent release instructions, and a few stale/broken references.

---

## Findings

### 1) Quickstart command likely fails in a clean clone (wrong path + non-canonical ROBOT invocation)
- **Severity:** **HIGH**
- **Evidence:**
  - `README.md:L56` uses: `robot reason --input dfo-salmon.ttl --reasoner ELK`
  - Canonical repo path is `ontology/dfo-salmon.ttl` (`Makefile:L51`, `Makefile:L59`, `Makefile:L64`)
  - Canonical tooling is pinned jar via make/install flow (`Makefile:L5`, `Makefile:L47-L53`, `Makefile:L115-L126`), not a guaranteed global `robot` binary
- **Why this matters:** New contributors following Quickstart can hit an immediate command failure and think the repo/tooling is broken.
- **Recommended fix:** In README Quickstart, replace raw command with canonical command(s), e.g. `make reason` (or `java -jar tools/robot.jar reason --input ontology/dfo-salmon.ttl --reasoner ELK`).

### 2) Release instructions under-specify artifacts to commit after `make ci`
- **Severity:** **MEDIUM**
- **Evidence:**
  - `README.md:L109` says to commit `docs/gcdfo.{ttl,owl,jsonld}` and `docs/index.html`
  - `docs-widoco` can generate `index-en.html` and sync all docs outputs (`Makefile:L171-L177`)
  - Helper target explicitly stages `docs/index-en.html` too (`Makefile:L110-L112`)
  - CI fails on any uncommitted diff except one excluded file (`.github/workflows/ci.yml:L69-L75`)
- **Why this matters:** Contributors can follow README exactly and still fail CI due to uncommitted generated files.
- **Recommended fix:** Update README release step to say “commit all generated `docs/` artifacts” (or explicitly include `docs/index-en.html` and suggest `make ci-sync-artifacts`).

### 3) Local run/release instructions are inconsistent about `devenv` requirement
- **Severity:** **MEDIUM**
- **Evidence:**
  - Optional framing exists: `README.md:L59` (“if using devenv/nix (optional)…”)
  - But canonical release steps are written as `devenv shell ...` commands: `README.md:L100`, `README.md:L109-L110`, `docs/context/widoco.md:L34-L36`, `docs/CONVENTIONS.md:L1855-L1856`
  - `docs/entrypoints.md` presents plain make as canonical (`docs/entrypoints.md:L17`, `docs/entrypoints.md:L52-L53`)
  - CI itself runs plain `make ci` (`.github/workflows/ci.yml:L66-L67`)
- **Why this matters:** Readers get mixed signals on whether `devenv` is required or optional.
- **Recommended fix:** Normalize to “`make ...` (or `devenv shell make ...` if using nix/devenv)” everywhere release/test commands are listed.

### 4) `docs/ROBOT_SETUP.md` includes stale/non-canonical execution guidance
- **Severity:** **MEDIUM**
- **Evidence:**
  - Uses raw `robot ...` commands (`docs/ROBOT_SETUP.md:L11-L18`) while repo canonical path is pinned jar + make targets (`Makefile:L42-L53`, `Makefile:L115-L126`)
  - References non-existent helper: `scripts/robot-commands.bat` (`docs/ROBOT_SETUP.md:L197`) (file not present in `scripts/`)
  - Report filename example differs from script/CI artifact naming:
    - docs says `release/artifacts/quality-report.html` (`docs/ROBOT_SETUP.md:L14`, `L69`)
    - script/CI use `release/artifacts/robot-quality-report.html` (`scripts/robot-quality-check.sh:L10`, `.github/workflows/ci.yml:L83`)
- **Why this matters:** Increases support churn and false “tool is broken” reports.
- **Recommended fix:** Make `docs/ROBOT_SETUP.md` explicitly mirror Makefile targets (`make quality-check`, `make reason`, `make test`) and remove/replace dead `.bat` reference.

### 5) `docs/context/widoco.md` points to local reference files that are missing
- **Severity:** **MEDIUM**
- **Evidence:**
  - References: `docs/context/widoco_README.md`, `docs/context/widoc_metadata_guide.md`, `docs/context/widoco_bps.md` (`docs/context/widoco.md:L5-L7`)
  - These files are not present in `docs/context/` in this branch/worktree.
- **Why this matters:** Dead references in “guardrails” docs look sloppy and block self-service.
- **Recommended fix:** Either add the referenced files or replace those bullets with valid upstream links and a note that local copies are intentionally not vendored.

### 6) CI trigger wording in docs is overstated
- **Severity:** **LOW**
- **Evidence:**
  - “automated checks on every push” wording appears in `README.md:L79`, `README.md:L100`, and `docs/CONVENTIONS.md:L1855`
  - Actual workflow triggers only on push to `main` and PRs targeting `main` (`.github/workflows/ci.yml:L4-L7`)
- **Why this matters:** Can create false confidence for branch pushes without PRs.
- **Recommended fix:** Reword to “on pull requests to main and pushes to main.”

### 7) TODO file has stale/conflicting CI status note for theme coverage
- **Severity:** **LOW**
- **Evidence:**
  - Open TODO says to wire theme coverage into CI/pre-commit (`docs/todo_list.md:L59`)
  - Already effectively wired via `make ci -> make test -> make theme-coverage` (`Makefile:L100-L107`) and CI runs `make ci` (`.github/workflows/ci.yml:L66-L67`)
- **Why this matters:** Planning noise; can prompt duplicate work.
- **Recommended fix:** Mark item complete or rewrite as a narrower follow-up (e.g., improve lint messaging/perf).

---

## Deprecated-flow clarity check (explicitly requested)
**Pass** — deprecated term-table flow is clearly marked as non-canonical in all scoped operational docs:
- `README.md:L74`
- `docs/entrypoints.md:L22-L29`
- `docs/todo_list.md:L42-L49`

---

## Tiny safe fixes applied
- None (report-only as requested).

## Top 5 risks to prioritize
1. Quickstart `robot reason --input dfo-salmon.ttl` command mismatch (`README.md:L56`)
2. Release commit list likely incomplete after `make ci` (`README.md:L109` vs `Makefile:L110-L112`)
3. Inconsistent `devenv` requirement messaging across docs (`README.md`, `docs/entrypoints.md`, `docs/context/widoco.md`, `docs/CONVENTIONS.md`)
4. Stale/dead ROBOT setup references (`docs/ROBOT_SETUP.md:L197` and report filename drift)
5. Missing local WIDOCO reference docs listed as if present (`docs/context/widoco.md:L5-L7`)
