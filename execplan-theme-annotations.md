# Theme annotations for all ontology terms

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective must be kept up to date as work proceeds. Maintain this document in accordance with agent-config/PLANS.md.

## Purpose / Big Picture

Add a consistent theme annotation (`dfoc:theme`) to every OWL class, property, and SKOS concept/concept scheme in the ontology so that navigation, review, and filtering align with the DFO Pacific functional seams. After completion, a novice can see every term tagged with 1–3 themes from the defined scheme and run validation to ensure compliance.

## Progress

- [x] (2025-12-03) Define `dfoc:theme` annotation property and SKOS Theme scheme in ontology/dfo-salmon.ttl.
- [x] (2025-12-03) Tag all classes/properties/SKOS concepts and concept schemes with 1–3 themes (at least one required).
- [x] (2025-12-03) Add validation (SPARQL/ROBOT/SHACL) to fail when any term lacks a theme or exceeds 3 themes.
- [x] (2025-12-03) Update docs/CONVENTIONS.md with theme usage, required cardinality, and reviewer checklist.
- [x] (2025-12-03) Validate end-to-end and record outcomes (rdflib check; ROBOT pending Java).

## Surprises & Discoveries

- ROBOT query could not run locally because Java is missing; validated theme coverage with rdflib instead (0 missing/over-limit/out-of-scheme themes).
- MixedStockNoGSITrigger legitimately carries three themes (Genetics, Fisheries Management, Policy/Governance); all others fit within the 3-theme cap.

## Decision Log

- Adopted the nine themes exactly as listed in docs/context/themes-modules.md and minted them in `ontology/dfo-salmon.ttl` under `:ThemeScheme`.
- Stored the theme assignments as a single `# Theme annotations (dfoc:theme)` block in `ontology/dfo-salmon.ttl` generated via a rdflib + heuristic script (manual overrides for policy/assessment hotspots).
- Added `scripts/sparql/theme-coverage.rq` as the guardrail for missing/over-limit themes or out-of-scheme values; falls back to rdflib validation when Java is unavailable.

## Outcomes & Retrospective

- All 392 typed terms (classes, object/datatype/annotation properties, SKOS concepts/schemes) now carry 1–3 themes, with theme scheme and `dfoc:theme` self-tagged for navigation.
- rdflib validation confirms 0 missing, 0 over-limit, and 0 out-of-scheme themes; ROBOT query still needs to run once Java is installed.

## Context and Orientation

Theme definitions live in docs/context/themes-modules.md. The ontology source is ontology/dfo-salmon.ttl. The goal is to mint an annotation property `dfoc:theme`, define a Theme SKOS concept scheme with the nine themes listed in themes-modules.md, apply 1–3 theme values to every OWL class, property, SKOS concept, and concept scheme, and add validation to enforce presence and cardinality. Documentation should be updated in docs/CONVENTIONS.md to describe how to use themes.

## Plan of Work

Add `dfoc:theme` as an annotation property in ontology/dfo-salmon.ttl. Add a Theme SKOS concept scheme and nine theme concepts (per docs/context/themes-modules.md) with labels/definitions/isDefinedBy. Apply `dfoc:theme` to every term (classes, object/datatype/annotation properties, SKOS concepts, SKOS concept schemes), assigning 1–3 appropriate themes. Add a validation query or SHACL shape to fail when any term lacks a theme or has more than three. Update docs/CONVENTIONS.md to describe the required annotation, acceptable values, and cardinality rules. Validate the ontology and ensure the validation step passes.

## Concrete Steps

1. Edit ontology/dfo-salmon.ttl: declare `dfoc:theme` as an annotation property; create `:ThemeScheme` and the nine SKOS concepts with labels/definitions per docs/context/themes-modules.md; ensure all new terms have rdfs:isDefinedBy and align with existing prefix usage.
2. Apply themes: for each OWL class, object/datatype/annotation property, SKOS concept, and concept scheme, add 1–3 `dfoc:theme` values from the Theme scheme. Use multi-valued annotations where needed; ensure every term has at least one (stored under `# Theme annotations (dfoc:theme)`).
3. Add validation: create a SPARQL query (scripts/sparql/theme-coverage.rq) to flag terms missing `dfoc:theme`, having more than three themes, or using values outside `:ThemeScheme`. Wire into CI/Make and pre-commit if applicable.
4. Documentation: update docs/CONVENTIONS.md to document theme usage, allowed values (reference the Theme scheme), and the cardinality rule (min 1, max 3). Mention validation expectations.
5. Validation/acceptance: run the validation query/SHACL; ensure zero violations. Spot-check a few terms across modules to confirm sensible theme assignments (rdflib check done; ROBOT pending Java).

## Validation and Acceptance

Passes when: the Theme scheme and `dfoc:theme` are present in ontology/dfo-salmon.ttl; every term is annotated with 1–3 themes; validation returns no missing/over-limit theme violations; docs/CONVENTIONS.md describes the rule. Optional: run ROBOT/CI to confirm no regressions.

## Idempotence and Recovery

Re-applying themes is safe; validation will catch omissions. If a term is mis-tagged, adjust its annotations and re-run validation. The Theme scheme is stable; avoid adding themes ad hoc—update the scheme first if needed.

## Artifacts and Notes

New artifacts: Theme scheme and annotation block in ontology/dfo-salmon.ttl; validation query file scripts/sparql/theme-coverage.rq. Existing reference: docs/context/themes-modules.md for theme definitions.

## Interfaces and Dependencies

No new external dependencies; relies on existing ROBOT/SPARQL/SHACL tooling in CI. Ensure any new query file is wired into the existing validation pipeline.
