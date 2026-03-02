# Final Check — `docs/CONVENTIONS.md` Logic Review

Date: 2026-02-25  
Reviewer: `fc-conventions-logic`

## Scope
Deep logic-quality review of `docs/CONVENTIONS.md` focused on:
1. Internal contradictions, duplication, ambiguity
2. Overly strict vs overly vague guidance likely to cause contributor mistakes
3. Outdated references (classes/properties/workflows)
4. Missing decision criteria that could produce inconsistent modeling choices

## Method
- Full read-through of `docs/CONVENTIONS.md`
- Targeted cross-check against current ontology implementation (`ontology/dfo-salmon.ttl`)
- Targeted cross-check against shape location conventions (`ontology/shapes/`, ADR docs)

---

## Findings

### A) Internal contradictions / duplication / ambiguity

#### High
1. **Hierarchy guidance contradicted itself across sections**
   - Quick Start: `SMU ▶ CU ▶ Population` with transitive `hasMember`
   - Section 3.2 and 6.4: `MU ▶ CU ▶ Stock` with `hasMemberCU`/`hasMemberStock`
   - These are materially different patterns and lead to inconsistent modeling.

2. **Section numbering collision in import strategy**
   - Inside `2.3.11`, subheads were labeled `2.3.6.3` and `2.3.6.4`, creating structural inconsistency and navigation confusion.

#### Medium
3. **Multiple duplicate blocks and duplicate rule lines**
   - Duplicate “Essential Elements” block in Quick Start
   - Repeated bullet lines (`rdfs:isDefinedBy`, `skos:altLabel`, repeated guide statements)
   - Repeated identical example triples in snippets

4. **Table of Contents mismatch**
   - TOC referenced non-existent Fundamentals sub-sections and pointed `6.3` to the wrong topic.

### B) Too strict / too vague guidance

#### Medium
5. **SKOS labeling policy lacked a default project decision**
   - Existing text gave two options for ROBOT compatibility (`configure ROBOT` vs duplicate `rdfs:label`) but no default, which invites inconsistent contributor behavior.

6. **Measurement examples mixed literal-vs-IRI style without clear consistency**
   - Earlier examples used literal-ish `dwc:measurementType`/`dwc:measurementUnit` strings; later sections emphasized `dwciri:*` IRI usage.

### C) Outdated references

#### High
7. **Membership property examples were outdated vs current ontology**
   - `hasMember` / `hasMemberCU` / `hasMemberStock` and `ManagementUnit` examples do not reflect current pattern in ontology (`hasConservationUnit`, `hasPopulation`, `StockManagementUnit`).

#### Medium
8. **SHACL placement wording was outdated**
   - Conventions implied SHACL shapes are in the ontology file, while project structure and ADR docs use `ontology/shapes/`.

9. **Example typo/outdated prefix usage**
   - `eco:Survey` example in modeling scenarios was inconsistent with surrounding `dfo:` usage.

### D) Missing decision criteria

#### Medium (remaining)
10. **Mapping confidence ladder lacks promotion criteria**
   - Ladder defines states (candidate/subProperty/equivalent) but not a required evidence threshold for moving between levels.

#### Low (remaining)
11. **Known warning section includes brittle numeric claim**
   - “identical results (2183 lines)” is likely to drift as ontology evolves; no refresh rule is given.

---

## Focused edits applied (surgical)

Edited file: `docs/CONVENTIONS.md`

1. Removed duplicated Quick Start canonical checklist blocks and repeated bullets.
2. Corrected hierarchy summary in Quick Start to current pattern (`StockManagementUnit ▶ ConservationUnit ▶ Population` with `hasConservationUnit`/`hasPopulation`).
3. Fixed TOC drift:
   - Removed stale Fundamentals sub-items
   - Corrected Advanced Topics entries to match actual sections.
4. Removed repeated statements and duplicate triples in core-conventions examples.
5. Updated schema/SHACL location language to reflect `ontology/shapes/` usage.
6. Added explicit project default for SKOS label mirroring under ROBOT validation guidance.
7. Corrected `2.3.11` subheading numbering.
8. Removed duplicate Darwin Core note paragraph.
9. Harmonized measurement examples toward `dwciri:*` usage where guidance already expects IRIs.
10. Replaced outdated membership pattern examples (`hasMember*`) with current property pattern (`hasConservationUnit`, `hasPopulation`) and `StockManagementUnit` class naming.
11. Replaced inconsistent `eco:Survey` example with `dfo:SurveyEvent`.
12. Updated one RO refinement example from `hasMemberCU` to `hasConservationUnit`.

---

## Remaining gaps (not changed to keep edits minimal)

1. **Alignment promotion criteria** should be formalized (e.g., lexical + scope + competency-question evidence before `owl:equivalent*`).
2. **Prefix policy (`dfo:` vs `gcdfo:`)** should be explicitly standardized in one short rule to avoid stylistic drift.
3. **RO alignment example still uses generic `:hasMember`** as a pedagogic placeholder; consider swapping to a canonical in-project property example for less ambiguity.
4. **Known warning section should avoid hard-coded line counts** or include a reproducible command/date stamp.

---

## Outcome
- High-value contradictions/duplication were removed.
- Major outdated workflow/property references in hierarchy guidance were aligned with current ontology conventions.
- Document structure/readability and decision consistency improved without large rewrites.
