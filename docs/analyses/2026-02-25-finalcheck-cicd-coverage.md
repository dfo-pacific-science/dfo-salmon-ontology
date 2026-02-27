# Final Check — CI/CD Suitability + Coverage Audit (2026-02-25)

## Scope audited

- `.github/workflows/ci.yml`
- `Makefile`
- `scripts/run-sparql-lint.sh`
- `.pre-commit-config.yaml`
- release/docs generation behavior (`make docs-refresh`, post-processing, snapshot flow)

## Method

Static deep-dive + environment spot-checks (no full runtime `make ci` in this worktree because host Java runtime is currently missing). Focus was reproducibility assumptions, lint/validation coverage, artifact drift controls, and local-vs-CI parity.

---

## Current CI execution graph (as implemented)

`ci.yml` runs:
1. Java 17 + Python 3.x setup (`.github/workflows/ci.yml:24-38`)
2. JAR fetch/cache for ROBOT + WIDOCO (`.github/workflows/ci.yml:40-64`)
3. `make ci` (`.github/workflows/ci.yml:66-67`), which expands to:
   - `make test` = `theme-coverage` + `alpha-lint` + ELK reasoning (`Makefile:84-101`)
   - `make quality-check` (`Makefile:42-45`)
   - `make docs-refresh` (`Makefile:103-108`, `157-198`)
4. Dirty-tree guard after generation (`.github/workflows/ci.yml:69-76`)

This is a sensible single-entrypoint design and generally strong for docs/artifact coherence.

---

## Findings by check area

### 1) Reproducibility + environment assumptions

**Strengths**
- CI pins ROBOT/WIDOCO versions (`ci.yml:13-18`) and rdflib (`ci.yml:38`).
- Makefile pins same tool versions (`Makefile:4-9`).

**Risks**
- Python interpreter is not pinned (uses `3.x`), so upstream runner changes can alter behavior (`ci.yml:30-33`).
- Prior to this pass, pre-push hook preferred Java 11 while CI uses Java 17; this could create local false negatives/positives. (Now fixed in this pass.)
- JAR download integrity is still URL-based only (no checksum validation); improved with fail-fast/retry but not full supply-chain verification.

### 2) Validation/lint coverage gaps

**What is covered well**
- Fast migration guardrails in `run-sparql-lint.sh` include year-basis, variable decomposition, legacy variableHas*, and SKOS match misuse (`scripts/run-sparql-lint.sh:32-37`).
- ELK reasoning + ROBOT report are part of required CI (`Makefile:100-108`).

**Gaps where regressions can slip**
- `theme-coverage` is warning-only and never exits non-zero when violations exist (`Makefile:91-95`). CI can pass with missing/over-assigned/invalid themes.
- `scripts/sparql/missing-definition-source.rq` exists but is not wired into CI/test bundle, so missing `IAO:0000119` provenance can regress silently.
- CI only runs ELK; HermiT/JFact inconsistencies would not be caught unless run manually (`reason-all` exists but is not in CI).

### 3) Generated-artifact drift handling quality

**Strengths**
- CI regenerates docs in-band (`make docs-refresh`) and enforces clean repo afterward.
- Determinism hardening already exists:
  - JSON-LD canonicalization + bnode stabilization (`scripts/convert_ttl_to_jsonld.py:103-132`)
  - WIDOCO changelog list canonicalization (`scripts/postprocess_widoco_html.py:15-45`)

**Weak points**
- One file is intentionally excluded (`docs/webvowl/data/ontology.json`) in both CI and pre-push, so WebVOWL drift is tolerated by policy.
- Prior to this pass, CI dirty-tree check used `git diff`, which misses untracked generated files; fixed in this pass to use porcelain status with untracked included.

### 4) Local dev parity vs CI parity + likely failure modes

Likely failure modes for contributors:
- Local host missing Java / jars (`check-robot`, `check-widoco`) causes immediate fail (`Makefile:253-264`).
- If contributors run outside `devenv`, environment assumptions are looser than CI.
- Pre-push hook only triggers when `ontology/dfo-salmon.ttl` matches hook file regex (`.pre-commit-config.yaml:8`), so CI breakage introduced only by scripts/workflow edits may not be caught until remote CI.

---

## Tiny hardening edits applied (safe + narrow)

1. **Pre-push Java parity fix**
   - `.pre-commit-config.yaml:6`
   - Switched fallback JAVA_HOME probing from OpenJDK 11 to 17 to match CI/WIDOCO runtime expectations.

2. **CI drift guard now catches untracked generated files**
   - `.github/workflows/ci.yml:69-76`
   - Replaced `git diff --quiet` check with `git status --porcelain --untracked-files=all` (still excluding `docs/webvowl/data/ontology.json`).

3. **Fail-fast + retry for CI jar downloads**
   - `.github/workflows/ci.yml:51,64`
   - `curl -fL --retry 3 --retry-delay 2 ...`

4. **Fail-fast + retry for local make install targets**
   - `Makefile:119,133`
   - Same curl hardening applied to `install-robot` and `install-widoco`.

---

## Top 5 CI/CD risks and recommended fixes

1. **Theme coverage is non-blocking in CI**
   - **Risk:** ontology can drift on `gcdfo:theme` coverage while CI remains green.
   - **Fix:** make `theme-coverage` fail on non-empty TSV (or gate with explicit transitional flag).

2. **Python runtime not pinned (`3.x`)**
   - **Risk:** runner image updates change behavior unexpectedly.
   - **Fix:** pin explicit minor (e.g., `3.12`) in CI and document supported local version.

3. **No checksum verification for downloaded JARs**
   - **Risk:** corrupted or tampered downloads are not cryptographically detected.
   - **Fix:** publish expected SHA256 and verify after download (CI + local install targets).

4. **Validation gap for definition source provenance**
   - **Risk:** missing `IAO:0000119` can regress without detection.
   - **Fix:** wire `scripts/sparql/missing-definition-source.rq` into lint bundle (possibly warning-only first, then enforce).

5. **Single-reasoner CI (ELK only)**
   - **Risk:** reasoner-specific modeling issues can slip.
   - **Fix:** run HermiT/JFact on scheduled/nightly or release candidate workflow (keep PR CI fast).

---

## Bottom line

CI is structurally solid and already oriented around a single reproducible entrypoint (`make ci`) with artifact drift enforcement. Main remaining exposure is **policy-level coverage** (theme check non-blocking, missing-definition-source not wired, single-reasoner CI), not pipeline architecture.
