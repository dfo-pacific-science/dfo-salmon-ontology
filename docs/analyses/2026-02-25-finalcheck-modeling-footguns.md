# Final Check — Ontology Modeling Foot-guns / Embarrassment Risks (2026-02-25)

## Scope reviewed

- `ontology/dfo-salmon.ttl`
- `ontology/modules/upper-level-view.ttl`
- `docs/context/extraction-frame-use-cases.md`
- `docs/CONVENTIONS.md`

## Executive readout

The model is close, but there are **five high-risk foot-guns** that can still derail collaborator conversations and external review confidence. The biggest pattern is **canonical-vs-example drift**: current ontology semantics are stronger/cleaner than several visible docs and alignment cues.

---

## Top 5 modeling foot-guns (with safer formulations)

## 1) "Stock" semantic split (biological thing vs information-defined stratum)

**Why this is risky**
- This is the fastest way to trigger circular debate: one group will treat Stock as fish/biology, another as assessment/reporting construct.

**Concrete evidence**
- Ontology defines Stock as **non-biological management/reporting unit**:
  - `ontology/dfo-salmon.ttl:1572-1578` (`gcdfo:Stock` subclass of `gcdfo:ReportingOrManagementStratum`; definition says "not a biological organism").
- Conventions still show Stock as biological organism:
  - `docs/CONVENTIONS.md:1312-1315` (`dfo:Stock rdfs:subClassOf dwc:Organism`).
- Conventions also show outdated MU ▶ CU ▶ Stock membership pattern:
  - `docs/CONVENTIONS.md:1635-1658`.
- Current ontology hierarchy is different (SMU ▶ CU, with biological Population/Deme split):
  - `ontology/dfo-salmon.ttl:1426-1441`, `1572-1594`, `1617-1625`.

**Safer formulation**
- Keep `gcdfo:Stock` strictly as a **reporting/management stratum**.
- Use `gcdfo:Population` / `gcdfo:Deme` for biological grouping language.
- In docs, explicitly say: "Stock (management stratum) is not equivalent to Population (biological group)."

**Mitigation**
1. Replace stale Stock examples in `docs/CONVENTIONS.md` with current `gcdfo:` examples.
2. Add a short "Stock vs Population" disambiguation box near the first hierarchy section.

---

## 2) High-visibility docs drift/duplication (publication-facing weirdness)

**Why this is risky**
- Even when ontology logic is fine, docs that look copy-glitched or internally inconsistent reduce trust fast in collaborator review.

**Concrete evidence**
- Duplicate "Essential Elements" block and repeated bullets:
  - `docs/CONVENTIONS.md:25-57`.
- Repeated sentence lines:
  - `docs/CONVENTIONS.md:133-134`.
- Duplicate Darwin Core note:
  - `docs/CONVENTIONS.md:1294-1296`.
- Undefined/stale prefixes in examples (e.g., `eco:`) and older `dfo:` examples mixed with current conventions:
  - `docs/CONVENTIONS.md:1926`, `1931-1941`.

**Safer formulation**
- Treat one section as normative and demote legacy examples to an "archive" or remove.
- Ensure all examples use current namespace/patterns (`gcdfo:`) unless explicitly marked historical.

**Mitigation**
1. Run a docs hygiene pass focused on duplicate blocks + stale prefixes.
2. Add a minimal docs lint check (duplicate heading scan + undefined prefix scan in fenced Turtle snippets).

---

## 3) Canonical vs non-canonical boundary is stated, but still blurred

**Why this is risky**
- Collaborators may import or cite the upper-level module as authoritative because it contains strong axioms and "canonical" wording despite being labeled non-canonical.

**Concrete evidence**
- Module explicitly says non-canonical:
  - `ontology/modules/upper-level-view.ttl:16`.
- But same module includes heading "Canonical SOSA -> PROV alignment links":
  - `ontology/modules/upper-level-view.ttl:101-107`.
- It also includes strong OWL restrictions/object properties that look authoritative:
  - `ontology/modules/upper-level-view.ttl:35-41`, `53-57`.
- Conventions says canonical authoring is SKOS + local annotations; interop projection should be separate/generated:
  - `docs/CONVENTIONS.md:427-430`.

**Safer formulation**
- Rename module sections to "reference alignment hints" (not canonical).
- Keep explicit warning: "Do not treat this module as canonical authoring source."

**Mitigation**
1. Tighten language in module headings/comments.
2. Add CI guard that canonical release ontology does not import upper-level-view.

---

## 4) SKOS mapping semantics are internally contradictory and too weak for class alignment

**Why this is risky**
- Mapping intent becomes ambiguous for downstream users/tools (annotation-only vs semantic alignment), and reviewers may flag misuse.

**Concrete evidence**
- SKOS mapping predicates redeclared as annotation properties:
  - `ontology/dfo-salmon.ttl:46-53`.
- Class-level alignments are expressed with `skos:closeMatch` (concept mapping predicate):
  - `ontology/dfo-salmon.ttl:1641`, `1652`, `1660`.
- Scheme-to-scheme exactMatch appears:
  - `ontology/dfo-salmon.ttl:467-473`.
- Conventions says SKOS mapping predicates are for concept mappings, while OWL classes/properties should use subclass/equivalence ladders:
  - `docs/CONVENTIONS.md:359`, `1743-1753`.

**Safer formulation**
- For OWL class/property alignment, use `rdfs:subClassOf` / `owl:equivalentClass` / `rdfs:subPropertyOf` / `owl:equivalentProperty` when confidence supports it.
- Reserve SKOS mapping predicates for concept-to-concept mappings.

**Mitigation**
1. Publish a short "mapping confidence policy" addendum with 2-3 concrete examples from this ontology.
2. Refactor the highest-visibility class-level `skos:closeMatch` usages first.

---

## 5) I-ADOPT role conflation in rapid-status decomposition (+ profile hazard around `usedProcedure`)

**Why this is risky**
- Metric decomposition may be interpreted differently by different teams (procedure vs constraint vs measured property), leading to inconsistent downstream implementations.

**Concrete evidence**
- Conventions separates method/protocol from constraints and says I-ADOPT does not model methods:
  - `docs/CONVENTIONS.md:439-440`, `988`.
- But rapid-status metrics use `gcdfo:WSPRapidStatus` (a class representing an approach) as `iadoptConstraint`:
  - `ontology/dfo-salmon.ttl:1910`, `1926`, `1971`; class at `1738-1745`.
- `RapidStatusScoreMetric` sets `iadoptProperty` to `gcdfo:WSPBiologicalStatusZone` (zone concept) although definition says numeric score metric:
  - `ontology/dfo-salmon.ttl:1978-1987`.
- `gcdfo:usedProcedure` is an annotation property declared as subproperty of `sosa:usedProcedure`:
  - `ontology/dfo-salmon.ttl:1532-1536`.
- Conventions also claim strict OWL 2 DL adherence:
  - `docs/CONVENTIONS.md:17`.

**Safer formulation**
- Keep procedure in `gcdfo:usedProcedure`; keep `iadoptConstraint` for true qualifiers (e.g., benchmark type, year basis, origin, life stage).
- For score metrics, point `iadoptProperty` at a score/status property term (not the zone class itself).

**Mitigation**
1. Do a focused rapid-status decomposition review (term-by-term).
2. Decide and document whether annotation→object subproperty links are acceptable in this project profile; if yes, state profile limits explicitly; if no, replace with project-local annotation linkage.

---

## Additional note from extraction-frame doc

A smaller but real confusion point exists in extraction categories:
- `docs/context/extraction-frame-use-cases.md:7` treats Stock/CU/SMU as **Entity**,
- while `:8` lists "management stratum" under **Property**.

That dual treatment can cause inconsistent tagging in extraction sessions. Recommend making "management stratum" consistently an Entity-side construct (or explicitly split "stratum identity" vs "stratum descriptor").

---

## Check outcomes against requested review criteria

1. **Canonical vs non-canonical boundaries explicit and non-contradictory?**
   - **Partial pass / material risk remains.** Boundary is stated, but contradictory cues persist (especially in docs/module wording and examples).
2. **Confusing term choices/mappings likely to derail discussions?**
   - **Yes.** Stock semantics and rapid-status decomposition roles are the top discussion derailers.
3. **Semantically risky alignments (too strong/too weak)?**
   - **Yes.** SKOS mapping usage on OWL classes and mixed annotation/object-property alignment patterns are the key risks.
4. **High-visibility weirdness in published docs model view?**
   - **Yes.** Conventions duplication/stale snippets are noticeable and reputationally costly.

---

## Recommended mitigation plan (order of operations)

1. **Docs hotfix pass (same week):** clean duplicate/stale `docs/CONVENTIONS.md` sections and align examples to current ontology.
2. **Semantic policy note (short ADR):** lock mapping policy (OWL vs SKOS usage; profile stance on annotation/object-property bridging).
3. **Rapid-status decomposition cleanup plan:** review `iadoptProperty` / `iadoptConstraint` assignments for metric terms.
4. **Upper-level module labeling hardening:** remove "canonical" wording in non-canonical module and reinforce its status as visualization/alignment aid only.
5. **Add lightweight lint checks:** prevent reintroduction of stale prefixes, duplicate sections, and class-level SKOS mapping misuse.
