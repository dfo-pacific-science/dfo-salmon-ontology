# ADR-010: Both method schemes keep their top concepts in this ontology

## Status

Accepted (Brett Johnson, 2026-10-23; hub item B-76 in salmon-data-mobilization/metasalmon)

## Context

This ontology has two method schemes. `:EnumerationMethodScheme` holds the field methods used
to count salmon (fences, visual surveys, sonar, traps and so on). `:EstimateMethodScheme` holds
the analytical methods used to turn those counts into abundance estimates (mark–recapture
estimators, area-under-the-curve, regression calibration and so on).

The two schemes ended up modelled differently:

- **Enumeration.** On 2026-03-15 this ontology stopped declaring `gcdfo:EnumerationMethod` and
  made the shared `smn:EnumerationMethod` the top concept of `:EnumerationMethodScheme`
  (the migration ADR-008 records). On 2026-08-13 smn moved its methods to SKOS and typed
  `smn:EnumerationMethod` as `sosa:Procedure`, and this ontology mirrored that concept.
  Releases 0.0.8 and 0.0.9 therefore declare no `gcdfo:EnumerationMethod`.
- **Estimate.** `:EstimateMethod` stayed a bare `skos:Concept`, with no `sosa:Procedure`
  typing and no `skos:broader` edge.

Two problems followed:

1. **B-148.** metasalmon's NuSEDS method crosswalks target 45 `gcdfo:` concepts that are not
   missing. Tested for whether each reaches a resource typed `sosa:Procedure` by zero or more
   `skos:broader` steps (with smn and the official SOSA ontology merged in), 22 passed,
   22 failed and 1 was not declared at all. The 22 failures are the whole estimate branch.
2. **The undeclared target.** metasalmon (`R/nuseds-method-crosswalk.R`) and metasalmonpy
   (`nuseds.py`) map the NuSEDS value "Based on Angling Catch" to `gcdfo:EnumerationMethod`,
   which no current release declares.

Hub item B-76 left one choice open: type `:EstimateMethod` as `sosa:Procedure`, or promote the
estimate branch into `smn:MethodScheme` as had been done for enumeration.

## Decision

Brett Johnson, 2026-10-23: *"enumeration method and estimation method were developed in GCDFO
and should probably stay there, actually."* Asked to confirm a ruling in which both method
branches stay here and this ontology gets its own enumeration-method top concept, mapped to
`smn:EnumerationMethod` rather than using it as the top, he answered *"Yes."*

1. **Estimate methods stay here.** `:EstimateMethod` is typed `skos:Concept, sosa:Procedure`.
   The branch is not promoted into `smn:MethodScheme`.
2. **Enumeration methods stay here.** `:EnumerationMethod` is declared again, with the same IRI
   and definition it had in releases 0.0.2 and 0.0.999. It is typed `skos:Concept,
   sosa:Procedure`, is the top concept of `:EnumerationMethodScheme`, and is
   `skos:exactMatch smn:EnumerationMethod`. Every DFO enumeration method's `skos:broader` is
   `:EnumerationMethod`.
3. **The smn mirror stays, outside the scheme.** The `smn:EnumerationMethod` mirror is kept so
   this ontology's published files describe the target of the `skos:exactMatch`. It is no
   longer a member of `:EnumerationMethodScheme`; it remains in `smn:MethodScheme`.

### Why these choices, and not because a validator passes

- **Typing `:EstimateMethod` as `sosa:Procedure` is a modelling choice.** SOSA defines a
  Procedure as a workflow, protocol, plan, algorithm or computational method that specifies how
  to make an Observation. That covers analytical methods: a Petersen estimator or an
  area-under-the-curve integration specifies how an abundance observation is produced. The
  enumeration branch already carried the same typing through `smn:EnumerationMethod`.
- **`skos:exactMatch` to smn, not `closeMatch` or `broadMatch`.** smn minted
  `smn:EnumerationMethod` from this ontology's release-0.0.2 concept, and the two definitions are
  word for word the same: "A method used to enumerate or count salmon in the field." A
  `closeMatch` would understate that, and a `broadMatch` would be false. The separate IRI records
  where the DFO enumeration-method taxonomy is maintained, which smn's own boundary rules leave
  to organisation profiles.

## Consequences

- **B-148 is fixed.** After the change, all 45 non-missing `gcdfo:` targets reach a
  `sosa:Procedure` (45 pass, 0 fail), measured against smn `main` and against the smn pin
  `f7205ee`. Before it, the result was 22 pass, 22 fail and 1 undeclared.
- **The angling row is valid as written.** "Based on Angling Catch" →
  `gcdfo:EnumerationMethod` resolves to a declared concept. metasalmon and metasalmonpy need no
  change for it; the four NuSEDS codes missing from their crosswalks are a separate matter
  (hub items B-438 and B-439).
- **Consumers walking `skos:broader`.** A consumer that walks `skos:broader` from a DFO
  enumeration method now reaches `gcdfo:EnumerationMethod`, and reaches
  `smn:EnumerationMethod` through `skos:exactMatch`. A consumer that requires
  `smn:EnumerationMethod` by direct `skos:broader` must also follow the mapping.
- **PSC.** The PSC controlled vocabulary's `psc-to-smn` mappings (`skos:broadMatch
  smn:EnumerationMethod`) are unaffected, because `smn:EnumerationMethod` is unchanged.
- **Earlier ADRs.** This supersedes, for enumeration methods only, the 2026-03-15 decision that
  ADR-008 records. It does not change the other terms that migration retargeted to smn.

## Alternatives considered

- **Promote the estimate branch into `smn:MethodScheme`.** This was B-76's second option, and
  the ruling rejected it.
- **Keep `smn:EnumerationMethod` as the top and only type `:EstimateMethod`.** This would fix
  B-148, but not the ruling that both branches stay here, and it would leave
  `gcdfo:EnumerationMethod` undeclared for the crosswalk row that names it.
