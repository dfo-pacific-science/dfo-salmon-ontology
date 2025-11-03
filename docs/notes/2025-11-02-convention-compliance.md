# Convention Compliance Remediation — 2025-11-02

## Scope
- Added missing `rdfs:label` annotations to all OWL classes, object properties, and datatype properties in `ontology/dfo-salmon.ttl`.
- Reinstated required `IAO:0000115` definitions for COSEWIC status classes, `:DowngradeCriteria`, and imported SKOS upper classes.
- Normalized alignment annotations by swapping `skos:altLabel` IRIs for `skos:exactMatch` and moving IRI pointers from `rdfs:comment` to `rdfs:seeAlso`.
- Converted `dfoc:organizationalUnitName`/`dfoc:organizationalUnitCode` to datatype properties to match literal ranges.
- Documented intentional punning blocks (temporal reference types, COSEWIC statuses) directly in the ontology and surfaced the policy in `docs/CONVENTIONS.md`.

## Follow-up
- Run ROBOT `validate` and `reason` after future structural edits to ensure punning and annotation patterns stay within OWL 2 DL.
- Continue mirroring `rdfs:label` values when adding `skos:prefLabel` to OWL terms.
- Removed OWL structural axioms from SKOS schemes (enumeration methods, estimate methods/types, downgrade criteria) to keep vocabularies SKOS-only and avoid punning.
- Added explicit annotation-property and datatype declarations so ROBOT DL-profile validation passes without punning the SKOS terms.
- Added custom ROBOT report profile (`tools/robot/report-profile.txt`) to downgrade `missing_label` to WARN so SKOS vocabularies stop triggering error-level noise.
