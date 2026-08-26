# Modules

These module files are **optional** loads alongside the DFO Salmon Ontology. They are
never imported by `ontology/dfo-salmon.ttl`; each one imports *it*.

The non-normative salmon metamodel view previously housed here now lives in the shared SMN repo under `ontology/views/`.

## Two kinds of module

Both kinds live here, and the distinction decides what `make check-modules` will let a
file do:

- an **alignment overlay** asserts relations between terms that already exist, and
  should declare nothing at all;
- a **vocabulary module** enumerates the members of one SKOS concept scheme, so
  declaring individuals is its entire job.

The rule that separates them: **a module never declares a class or a property.**
Schema is core content and lives in `ontology/dfo-salmon.ttl`. A vocabulary module may
declare its scheme and its concepts, and nothing else.

## Which way `owl:imports` points, and why

Every module here reads `owl:imports <https://w3id.org/gcdfo/salmon>`. Core does not
import back. That is not a stylistic preference, it is forced:

- `https://w3id.org/gcdfo/salmon` resolves (303 to the GitHub Pages site).
- `https://w3id.org/gcdfo/salmon/modules/<anything>` **404s**. The W3ID `.htaccess`
  matches the ontology IRI and a `X.Y.Z` version pattern, nothing else.

So a module can import core and stay loadable for anyone, anywhere. If core imported a
module, the published `docs/gcdfo.ttl` would carry an `owl:imports` to a URL that does
not resolve, and every downstream consumer — Protégé, `rdflib`, ROBOT without this
repo's catalog — would fail to load the ontology. Making core import a module is
therefore gated on a PR to `perma-id/w3id.org` adding the redirect; see
`docs/context/w3id.md`. Until then the arrow points this way.

**This retires** when a module IRI resolves. At that point the direction becomes a real
choice rather than a forced one, and for a vocabulary module it should be re-argued
rather than assumed — see [ADR-009](../../docs/adr/009-pfma-subarea-scheme-separation.md),
which records why the Subarea vocabulary would still be worth keeping out of the
rendered docs even then.

## Files

- `alignment-main.ttl` *(alignment overlay)*
  - Conservative, near-term merge-safe bridges.
  - Uses mostly `skos:closeMatch` and a few safe `rdfs:subPropertyOf` links.
  - Recommended default when contributors want context without strong logical commitments.

- `alignment-research.ttl` *(alignment overlay)*
  - Fuller exploratory alignment for analysis/design.
  - Includes stronger candidate subclass and property bridge axioms.
  - Not intended for immediate core merge without targeted review + competency-query checks.

- `vocabulary-pfma-subareas.ttl` *(vocabulary module)*
  - The 604 Pacific fishery management Subareas of SOR/2007-77 Schedule 2, as a SKOS
    concept scheme, each with `skos:broader` to its parent Area.
  - The class they are values of, `gcdfo:PacificFisheryManagementSubarea`, is core
    schema and stays in `ontology/dfo-salmon.ttl`; only the enumeration is here.
  - Load it when you need to resolve or validate a Subarea code. You do not need it to
    use Areas: the 48 Areas are core content and are unaffected.

## When to use each

Use **alignment-main** when you want to:
- give contributors metamodel context,
- improve discoverability in docs/WebVOWL,
- avoid introducing brittle equivalence axioms.

Use **alignment-research** when you want to:
- test broader alignment hypotheses,
- explore SOSA/I-ADOPT bridge patterns,
- design next-round SHACL + competency query updates.

Use **vocabulary-pfma-subareas** when you want to:
- resolve, label or validate a PFMA Subarea code such as `12-14`,
- roll Subareas up to their parent Area through `skos:broader`,
- check a dataset column whose values are Subareas rather than Areas.

Use the **SMN metamodel view** (in the shared SMN repo under `ontology/views/`) when you want to:
- inspect only the shared upper-level/crosswalk model,
- facilitate architecture discussion with contributors/domain experts,
- review the entity/property/variable/method-event-result-provenance decomposition without making it DFO-owned content.

## Why modules (instead of core-only)

The crosswalks from files 74/75/76/77 include a mix of:
- ontology-level semantics,
- representation-level mappings,
- data-profile conventions (e.g., DwC-DP `eventID` / `parentEventID`).

Keeping this in modules lets us preserve contributor context without over-constraining `ontology/dfo-salmon.ttl`.

For a **vocabulary module** the reason is different and it is quantitative. The 48
Areas are core content and at 48 members that is navigable. 604 Subareas are not: held
in core they added 10,305 lines to `ontology/dfo-salmon.ttl`, 12,573 to
`docs/index.html`, and 98,685 to `docs/webvowl/data/ontology.json` — a WebVOWL graph
with 604 extra nodes is not a diagram anyone can read. Splitting the enumeration out
keeps `ontology/dfo-salmon.ttl` and every generated artifact navigable, and does it
without changing a single concept. The size threshold is a judgement, not a rule; what
is not a judgement is that the generated docs are a human-facing artifact and a
vocabulary can destroy them.

## Source basis

The alignment overlays derive from the latest four alignment artifacts shared in chat:
- `file_74-...csv`
- `file_75-...csv`
- `file_76-...xlsx`
- `file_77-...csv`

`vocabulary-pfma-subareas.ttl` derives from Schedule 2 of the *Pacific Fishery
Management Area Regulations, 2007* (SOR/2007-77); every concept cites its item and
paragraph.

## Notes

- These modules are intended to be loaded **alongside** core ontology, not as replacements.
- Prefer `skos:closeMatch` unless exact equivalence has been confirmed.
- Validation rules should remain in SHACL where appropriate.

## Verifying a module

```bash
make check-modules
```

This is the entrypoint for these files, and it runs as part of `make test`. Every other target
loads `ontology/dfo-salmon.ttl` alone, which imports neither overlay and so reports nothing
about them; `check-modules` merges each overlay with core the way this README tells you to use
them, and checks what that merge produces.

It matters because the merge is where these files can fail silently. The OWL API supplies a
declaration for any otherwise-untyped IRI used in class or property position, so an overlay
naming a term core no longer declares does not fail loudly — it mints that term as a fresh
`owl:Class` or `owl:ObjectProperty`. That is how eight retired `gcdfo:` terms survived here
after the core migration to `smn:`; see
[ADR-008](../../docs/adr/008-alignment-overlays-follow-core-to-smn.md). Run against the
pre-fix overlays, the check reports the terms each one re-minted: two for `alignment-main`
(`gcdfo:hasDeme`, `gcdfo:hasPopulation`), five for `alignment-research`. It reports nothing for
the other three retired names, because those appeared only in annotation position, where the
OWL API mints nothing — retargeting them was still correct, but this check is not what proves
it.

What it checks, per module — each with the condition that would retire it:

| Check | Retires when |
|---|---|
| **A1** The merge declares no `gcdfo:`/`smn:` **class or property** that core does not | never in practice — it depends on the OWL API minting declarations for untyped IRIs |
| **A2** Every `gcdfo:`/`smn:` **individual** the merge adds is a `skos:Concept` in a `skos:ConceptScheme` the module itself declares | the repo stops holding controlled vocabularies in modules |
| **B** No pair of terms carries two different `skos:*Match` predicates | the overlays stop restating mappings the shared layer already makes |
| **C** The merged closure is ELK-consistent | never; it is the minimum a loadable module must meet |
| **D** The merged closure passes the same `gcdfo:theme` coverage query `make theme-coverage` runs over core | `gcdfo:theme` stops being required |

A1 and A2 were one check until the first vocabulary module arrived. The old rule was
"the merge declares nothing core does not", which is right for an alignment overlay and
forbids a vocabulary module outright — it reported all 605 Subarea terms as defects.
Splitting it keeps the ADR-008 guard at full strength where that incident actually
happened (all seven re-minted terms were `owl:Class` or `owl:ObjectProperty`) and adds
a rule for individuals that is **tighter** than "declare nothing" was, because it also
rejects a concept parked in a scheme nobody declares.

D exists because of the split itself. `make theme-coverage` loads core alone, so before
D, moving a concept out of `ontology/dfo-salmon.ttl` silently removed it from the only
check that enforces the theme rule — 605 terms would have left core and left that rule
behind in the same commit, and nothing would have said so.

All three new behaviours were demonstrated failing before being trusted green: a module
declaring `gcdfo:ReMintedClass` fails A1; one declaring a stray individual, or a concept
in an undeclared scheme, fails A2; one whose concept omits `gcdfo:theme` fails D.

To inspect a merge by hand, `check-modules` leaves it in `release/tmp/modules/`, or build one
directly:

```bash
java -jar tools/robot.jar merge \
  --catalog release/tmp/robot-catalog.xml \
  --input ontology/dfo-salmon.ttl \
  --input ontology/modules/alignment-main.ttl \
  --output /tmp/merged.ttl
```

### Why these files use `skos:closeMatch` between OWL classes

`scripts/sparql/skos-match-on-owl-classes.rq` lints against `skos:*Match` where either side is
an OWL class, and it reports these overlays' class bridges. `check-modules` deliberately does
not run it, because that lint is scoped to the terms this repo authors and these bridges are
not the overlays' invention: the imported `smn` closure contributes **18** such rows before any
overlay is loaded, including `smn:SurveyEvent skos:closeMatch sosa:Sampling` and
`smn:ReferencePoint skos:closeMatch iadopt:Constraint` — every row the retarget produces is
already one of them. The shared layer also deliberately *demoted* a `sosa:Sampling` superclass
claim to `skos:closeMatch` (alignment finding F7). Rewriting the overlays as
`rdfs:subClassOf`/`owl:equivalentClass` would assert unconfirmed equivalence in the file whose
stated purpose is to avoid brittle equivalence axioms, and would contradict that upstream
decision.

This exemption retires if the shared layer moves off the `skos:*Match` idiom for class-to-class
alignment; at that point the class lint can run over the merged closure like any other check.
Individual rows graduate earlier: promote one to `rdfs:subClassOf`/`owl:equivalentClass` when
the pairing has been confirmed **and** the shared layer states it in OWL.

## SDP decomposition workflow (practical split)

For Salmon Data Package work (`term_iri`, `property_iri`, `entity_iri`, optional `constraint_iri`, `method_iri`):

- Keep the **normative DFO schema spine** in `ontology/dfo-salmon.ttl` (stable classes/properties contributors must rely on).
- Keep broader cross-framework and publication-profile mappings in these module files.
- Treat I-ADOPT Variables as **compound terms** in day-to-day data packaging (typically represented as SKOS concepts with decomposition annotations), while maintaining OWL-level bridge semantics for metamodel interoperability.

Rule of thumb:
- If contributors need it every day to encode SDP semantics, promote it to core.
- If it is a crosswalk hypothesis or publication-oriented mapping, keep it in a module.
- If it is the *enumeration* of a controlled vocabulary large enough to swamp the
  generated docs, keep the class in core and the members in a vocabulary module. The
  class is what a schema references; the members are what a validator resolves, and a
  validator can load a second file.
