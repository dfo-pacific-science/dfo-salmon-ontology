# ADR-009: PFMA Subareas get their own scheme, class and file, linked by `skos:broader`

## Status

Accepted

## Context

PR #86 minted the 48 Pacific fishery management **Areas** prescribed by Schedule 2 of the
*Pacific Fishery Management Area Regulations, 2007* (SOR/2007-77) as
`gcdfo:PacificFisheryManagementAreaScheme`, and left the 604 **Subareas** unminted, with a
`skos:scopeNote` saying so. Brett took the deferred decision on 2026-08-24: mint the Subareas
in `gcdfo`, and mint all of them rather than the four the gold-standard example happens to
need — *"Is that for gcdfo? If so yeah I guess they should all be in there."*

**That second half is not a one-off scope call.** It is an instance of the standing policy
Brett stated as **Q6-4: mint from the source vocabulary always.** Where an authority documents
a vocabulary, the vocabulary that gets minted is the documented one — not the subset some
dataset happens to have observed. The rule has reach well past this ADR: it is also what
settles minting `PKE` (documented in the source, never observed in the data at hand) and the
sea-type life-history term. So the completeness argument below is applied policy, not a
judgement re-derived per vocabulary, and a future value list should reach for Q6-4 rather than
re-litigating scope.

Subarea (term of art): a subdivision of a management area. Section 1 of the Regulations
defines it in exactly those words, and paragraph (b) of each Schedule 2 item enumerates the
Subareas of that item's Area — for example, `Subarea 12-14` inside Area 12.

Two things about the source shape the decision:

1. **A Subarea is a part of an Area, not a kind of Area.** 604 Subareas sit inside 42 of the
   48 Areas; the other six (21, 22, 103, 109, 110, 111) are not subdivided at all.
2. **Both are the same sort of thing in this ontology's terms** — an information-defined
   grouping used for reporting and management, i.e. `smn:ReportingOrManagementStratum` — just
   at different resolutions.

The Area vocabulary is already load-bearing outside this repo. `spsr-data-dict`'s
`converted/spsr-inventory/metadata/columns.csv` maps a `PFMA_ID` column onto
`gcdfo:PacificFisheryManagementArea`, and the natural way to validate such a column is
"`skos:inScheme gcdfo:PacificFisheryManagementAreaScheme`". Whatever this ADR decides has to
keep that check meaning what it currently means.

### Where the concepts live (added 2026-08-25)

The first draft of this ADR put all 604 concepts in `ontology/dfo-salmon.ttl` alongside the
48 Areas, and recorded the file growth as an accepted cost. Brett raised the consequence
directly:

> *"I don't necessarily know that I want every single PFMA subarea showing up in the main
> ontology file. And I also noticed that the rendered HTML website from the Widoco package
> has all of those subareas as well, and I'm worried that it's going to become untenable for
> human navigation."*

The measurement backs it. Held in core, the vocabulary added:

| Artifact | Lines added |
|---|---|
| `ontology/dfo-salmon.ttl` | 10,305 |
| `docs/index.html` | 12,573 |
| `docs/gcdfo.ttl` / `.owl` / `.jsonld` | 13,937 / 15,753 / 54,528 |
| `docs/webvowl/data/ontology.json` | 98,685 |
| **total** | **206,124** |

Two of those are human-facing. `docs/index.html` is the published documentation; a reader
looking for a class now scrolls past 604 area codes. `docs/webvowl/data/ontology.json` drives
the WebVOWL graph — a node-link diagram of the ontology — and 604 extra nodes do not make it
harder to read, they make it useless.

One measurement in that table is worth isolating, because it is the surprise. WIDOCO runs
here with `-ignoreIndividuals`, and that flag works: `docs/index-en.html`, the raw WIDOCO
output, grew by **53 lines** — the new class, and nothing else. The 12,573 lines in
`docs/index.html` come from `scripts/generate_skos_section.py`, which reads the ontology file
as text, and the 98,685 in the WebVOWL graph come from OWL2VOWL, which does not honour
`-ignoreIndividuals` at all. **So `-ignoreIndividuals` protects the HTML entity list and
nothing else.** Anyone reasoning about the docs cost of a vocabulary from that flag alone
will be wrong by two orders of magnitude.

## Decision

**Mint a second class and a second concept scheme, and relate the concepts with
`skos:broader`.**

- `gcdfo:PacificFisheryManagementSubarea` — an `owl:Class`,
  `rdfs:subClassOf smn:ReportingOrManagementStratum`, a **sibling** of
  `gcdfo:PacificFisheryManagementArea`, not a subclass of it.
- `gcdfo:PacificFisheryManagementSubareaScheme` — a `skos:ConceptScheme` holding all 604
  Subarea concepts, flat, with no `skos:hasTopConcept` (following the Area scheme and
  `:BenchmarkLevelScheme`).
- Each concept is typed `a gcdfo:PacificFisheryManagementSubarea , skos:Concept` — the same
  class-plus-value-list pattern the Areas use — and carries exactly one
  `skos:broader` to its parent Area concept in the *other* scheme.
- Both schemes carry `rdfs:seeAlso` to each other, and the Area scheme's completeness scope
  note was rewritten to name the sibling instead of claiming Subareas are unminted.

**And put the 604 concepts in their own file:
`ontology/modules/vocabulary-pfma-subareas.ttl`.**

- The **class** `gcdfo:PacificFisheryManagementSubarea` stays in `ontology/dfo-salmon.ttl`.
  It is schema: it is what a data dictionary or a SHACL shape references, it is one line, and
  it belongs next to its sibling Area class. The **enumeration** moves out.
- The module reads `owl:imports <https://w3id.org/gcdfo/salmon>`, exactly as
  `alignment-main.ttl` and `alignment-research.ttl` do. Core does **not** import back.
- Consequently no generated artifact changes at all. `docs/index.html`, `docs/gcdfo.*` and
  `docs/webvowl/data/ontology.json` are all built from `ontology/dfo-salmon.ttl` and its
  import closure, and the module is outside it. The vocabulary's insertions drop from 206,124
  to 11,571 — all of it the module file itself, none of it generated.

### Why the import points that way, and not the other way

Brett's phrasing was "stored in a separate file … and then just imported or something". The
direction is the one part of that which is not free, and it is decided by which IRIs resolve:

- `https://w3id.org/gcdfo/salmon` resolves — HTTP 303 to the GitHub Pages site.
- `https://w3id.org/gcdfo/salmon/modules/<anything>` **404s.** The W3ID `.htaccess` matches
  the ontology IRI and a `X.Y.Z` version pattern, and nothing else. Verified 2026-08-25 with
  `curl -I` against both.

If core imported the module, the published `docs/gcdfo.ttl` would carry an `owl:imports` to
a URL that does not resolve. Every downstream consumer that loads the ontology without this
repo's ROBOT catalog — Protégé, `rdflib`, ROBOT anywhere else — would fail on it. That is a
worse defect than the one being fixed, and it would be introduced into a released artifact.
Adding the redirect is a change to the W3ID publication contract, which `AGENTS.md` lists as
requiring explicit instruction, so it is not made here.

**This retires when a module IRI resolves.** At that point core *may* import the module, and
the choice becomes a real one — but note that flipping the direction re-imports the 604
concepts into `release/tmp/dfo-salmon-docs-input.ttl`, which is built with
`merge --collapse-import-closure true`, and so puts them straight back into the WebVOWL
graph. The HTML would stay clean (`-ignoreIndividuals`, and `generate_skos_section.py` reads
the core file as text); the graph would not. Flipping the direction therefore requires a
WebVOWL exclusion step first, and the module is written so that flip touches only its own
header.

### Alternatives rejected

- **Add the 604 Subareas to `gcdfo:PacificFisheryManagementAreaScheme`.** This is the
  smallest diff and the worst outcome. `skos:inScheme` on that scheme is usable today as the
  value set for "this column holds a PFMA"; folding in 604 finer-grained concepts would widen
  that set by 13× without any consumer changing a line, and would contradict the scheme's own
  `skos:definition` ("the 48 Pacific fishery management areas"). Two granularities in one flat
  value list is precisely the confusion issue #67 was opened about, one level down.
- **`rdfs:subClassOf` the Subarea class under the Area class.** Would assert that every
  Subarea *is* an Area. The Regulations say the opposite: a Subarea is a subdivision of one.
  Under ELK this would also make every Subarea concept an Area concept, re-widening the value
  set through the reasoner instead of through the scheme.
- **`skos:broadMatch` instead of `skos:broader`.** `skos:broadMatch` is SKOS's *mapping*
  relation, for linking concepts that belong to independent vocabularies. These two schemes
  are one hierarchy from one legal instrument, split for value-set hygiene; calling the link a
  mapping would misdescribe it, and would put it in the same predicate family that
  `scripts/sparql/conflicting-mapping-strength.rq` polices. `skos:broader` is already this
  ontology's idiom for concept hierarchy, including across namespaces
  (`skos:broader smn:MeasurementContext`).
- **An OWL object property for the part-whole relation.** The Subareas are SKOS concepts
  (individuals), so this would be ABox data about instances; `skos:broader` is already declared
  as an `owl:AnnotationProperty` here and is what every other concept hierarchy in the file
  uses. Adding a parallel mechanism for one vocabulary is a second live path for no gain.
- **Mint only the four Subareas the gold-standard example needs.** Rejected under **Q6-4,
  "mint from the source vocabulary always"** (Brett). The observed subset is a property of one
  dataset on one day; the instrument's enumeration is the vocabulary. A partial value list is
  also worse than no value list, because it looks complete — a consumer validating against it
  gets a false negative on a real Subarea and has no way to tell that from a genuine one.
  Under Q6-4 the observed-subset option is not weighed and rejected each time; it is closed.

Rejected on the **file placement** question specifically:

- **Keep all 604 in `ontology/dfo-salmon.ttl`.** What the first draft did. It is the smallest
  structural change and it produces the 206,124 insertions in the table above, two entries of
  which are artifacts a human is supposed to read. Rejected on Brett's direction and on the
  measurement.
- **Keep them in core but exclude them from the WebVOWL export.** This addresses the worst
  single number (98,685) and nothing else: `ontology/dfo-salmon.ttl` still quadruples, and
  `docs/index.html` still grows by 12,573. It also means adding a filtering step to
  `make docs-widoco` that has to know about one vocabulary by name — a rule that decays the
  moment a second vocabulary arrives and nobody remembers to extend it. Rejected as treating
  the symptom that shouts loudest.
- **Put the vocabulary in `ontology/views/`.** That directory holds non-normative *review*
  views — deliberately partial renderings for human discussion, e.g.
  `wsp-composite-escapement-view.ttl`. This vocabulary is neither partial nor non-normative;
  it is the complete value list of a class in the ontology. Filing it there would misdescribe
  its status.
- **Publish it as a standalone ontology with its own namespace.** Rejected: the concepts are
  `gcdfo:` terms minted under `gcdfo:` governance, and a second namespace would fork the
  governance of one legal instrument's vocabulary across two identifiers for a file-layout
  reason.
- **Move the 48 Areas out too, so the whole vocabulary lives in one module.** Not rejected —
  deferred, deliberately. See *Consequences → The 48 Areas*.

### On geometry

Schedule 2 delimits each Subarea with prose about coordinates, parallels, meridians and
shorelines. **No geometry is encoded.** These concepts identify and label Subareas; they do
not delimit them. A `skos:scopeNote` on the scheme says so and points at the Regulations and
DFO spatial data for boundaries. This is not deferred work waiting on a later PR — an ontology
of identifiers is the right artifact, and a half-transcribed boundary would be worse than an
absent one.

## Consequences

### Positive

- There is now a stable IRI for every unit DFO actually reports Pacific fisheries data at.
- `skos:inScheme gcdfo:PacificFisheryManagementAreaScheme` still means exactly what it meant
  before this change: one of the 48 Areas.
- The Area↔Subarea relation is machine-followable in both directions (`skos:broader`, and
  `skos:narrower` by SKOS's own inverse), so a Subarea-level record can be rolled up to its
  Area without a lookup table.
- A record that carries `12-14` can now be typed as the Subarea it is, rather than being
  forced into the Area class it is not a member of.

- `ontology/dfo-salmon.ttl` gains 19 lines, not 10,305, and no generated artifact changes
  at all. The published documentation and the WebVOWL graph are exactly what they were.

### Negative

- **The vocabulary is split across two locations.** Areas in
  `ontology/dfo-salmon.ttl`, Subareas in `ontology/modules/vocabulary-pfma-subareas.ttl`, both
  from one legal instrument. Someone reading only core sees half of Schedule 2. The scope
  notes on the class and both schemes name the other half and say where it is, which mitigates
  the defect without removing it. See *The 48 Areas* below.
- **The 604 concepts are `gcdfo:` IRIs that are not retrievable from the `gcdfo:` document.**
  Dereferencing `https://w3id.org/gcdfo/salmon#PacificFisheryManagementSubarea12-14` gets you
  a document that does not contain it, and each concept still carries
  `rdfs:isDefinedBy <https://w3id.org/gcdfo/salmon>` — kept deliberately, so that the two
  halves of one vocabulary do not disagree about their own provenance, but it is a claim
  about governance rather than about retrieval. Recorded in `docs/tech-debt.md`. **Retires**
  when the module IRI resolves and core imports it (see above), or when the docs build
  publishes the module as a fetchable artifact.
- **Nothing loads the module by default**, so a consumer who does not know it exists validates
  a Subarea code against the Area scheme and gets a false negative. The class's scope note is
  the only signpost in core.
- Two schemes mean a consumer wanting "any PFMA unit, either resolution" must union them.
  That is the intended cost: the union is explicit, the widening is not silent.
- `skos:notation` is a plain string here (`"12-14"`) where the Areas use
  `xsd:integer`. A consumer reading notations across both schemes gets two datatypes. The
  alternative — forcing a compound code into an integer — is not available.

### The 48 Areas — should they follow?

**Not in this change, and probably not at all.** The argument for moving them is symmetry: a
vocabulary split across two files is the defect named above, and moving the Areas would close
it. The arguments against are stronger:

1. **Size is the whole reason for the split, and 48 is not a size problem.** The Areas cost
   `ontology/dfo-salmon.ttl` 768 lines and add 48 nodes to WebVOWL. Nobody has
   complained about navigating them, because there is nothing to complain about.
2. **The Areas are load-bearing today and the Subareas are not.** `spsr-data-dict` maps
   `PFMA_ID` onto `gcdfo:PacificFisheryManagementArea`; that consumer resolves the term from
   the published ontology. Moving the Areas into a module they do not load would break a live
   integration to fix a symmetry.
3. **It would make the retrieval problem universal instead of local.** Right now 604 of 652
   concepts are unretrievable from the `gcdfo:` document; moving the Areas makes it 652.

The honest resolution is the *other* direction: once a module IRI resolves and core can
import it, both vocabularies can live in modules and still be retrievable from the ontology
IRI, and the WebVOWL exclusion becomes the one thing that needs building. **Revisit when the
W3ID redirect for module IRIs exists** — that is the trigger, not a date.

### Where the vocabulary is browsable

Taking 604 concepts out of the published documentation raises the obvious question, and it
needs an answer rather than a silence: a value list nobody can look up is a value list nobody
will use.

**Today**: `gcdfo:PacificFisheryManagementSubarea` carries a `skos:scopeNote` naming the module
file and an `rdfs:seeAlso` to that file on GitHub, which renders Turtle with syntax
highlighting and in-page search. Both reach the published RDF — `docs/gcdfo.ttl`,
`docs/gcdfo.owl`, `docs/gcdfo.jsonld` — so a machine consumer that resolves the class finds
the pointer.

**They do not reach the published HTML.** This was checked rather than assumed: WIDOCO renders
a class's definition, its `iao:0000119` sources and its superclasses, and renders neither
`skos:scopeNote` nor `rdfs:seeAlso` for a class. The rendered entity block for
`gcdfo:PacificFisheryManagementSubarea` therefore says nothing about where its 604 values are.
A human reading the documentation site is told the class exists and is told nothing about how
to enumerate it — which is a real gap and is recorded in `docs/tech-debt.md`. It affects
exactly two terms today (the Area and Subarea classes are the only classes in this ontology
carrying `skos:scopeNote`, five statements between them), which is why the fix below is a
page, not a WIDOCO post-processing feature.

**What should exist**: a standalone rendered page, `docs/vocabularies/pfma-subareas.html`,
generated from the module and linked from the class entry — a table of notation, label,
parent Area and definition, with the parent link resolving into the main page's Area section.
It should be produced by **extending `scripts/generate_skos_section.py` to take a source
ontology and an output target**, not by a second script; this repo's rule is one live path per
behaviour, and a duplicate SKOS renderer is precisely the ghost code `AGENTS.md` forbids. It
would join `CI_ARTIFACT_PATHS` like any other generated artifact.

The same page fixes the HTML gap above, because linking to it from the class entry requires
WIDOCO post-processing either way.

**Not built here**, deliberately. It is a new generated artifact, a new drift-gate surface and
a new page shell, landing in the change whose purpose is to *shrink* generated output — and it
is separable, because the vocabulary is reachable from the repository and from the published
RDF meanwhile. **Build it when either of two things happens**: someone needs to look up a
Subarea from the documentation site, or a second vocabulary module lands. Two is when a
pattern has to exist; one is when a link would do — and the honest position is that right now
even the link is missing from the HTML.

Rejected for this role: `ontology/views/`, which holds non-normative partial review views (see
*Alternatives rejected*); and rendering the module through WIDOCO as its own site, which would
produce a second full ontology documentation site for one value list and split the reader's
entry point in two.

### Neutral

- WIDOCO's `-ignoreIndividuals` was already doing its job and is not what protects the docs
  here; see the measurement in *Context*. Recording it because the flag's name invites the
  opposite conclusion.
- `make check-modules` had to learn the difference between an alignment overlay and a
  vocabulary module. Its old first check — "the merge declares no `gcdfo:`/`smn:` term core
  does not" — is correct for an overlay and forbids a vocabulary module outright; run against
  this module unchanged it reported all 605 terms as defects. It is now two checks: no minted
  *class or property* ever (the ADR-008 guard, at full strength), and minted *individuals*
  only as members of a scheme the module itself declares. A fifth check runs the repo's
  `gcdfo:theme` coverage query over the merged closure, because moving 605 terms out of core
  would otherwise have moved them out of the only check that enforces that rule.

## More Information

The count was established from paragraph (b) of the 48 Schedule 2 items in the Justice Laws
XML (consolidation current to 2026-06-21, last amended 2017-04-13, retrieved 2026-08-25), and
checked against two further renderings of the same instrument: the Justice Laws HTML
consolidation, and the French consolidation (ANNEXE 2), which enumerates the identical 604
sous-secteurs under the identical 48 secteurs.

**Unlike the Areas, there was no second published DFO listing to check against.** DFO's area
pages carry maps only and refer the reader back to these Regulations for the written Subarea
descriptions; the per-area map PDFs have no extractable text; and DFO's
`gisp.dfo-mpo.gc.ca` Pacific Fishery Management Areas map service no longer resolves
(NXDOMAIN on a public resolver). The scheme's `skos:scopeNote` records this rather than
implying the Areas' two-source standard was met. **This retires when DFO publishes a
machine-readable Subarea list or restores that map service** — at which point the 604
identifiers should be diffed against it, and the scope note replaced with the result.

Subarea numbering is contiguous from 1 within its Area in every case but Area 2, which runs
2-1 to 2-19 and then 2-31 to 2-100 (confirmed in both language versions). The contiguity
argument that made the *Area* extraction self-checking is therefore unavailable for Subareas,
and a scope note says so.

## Related

- [ADR-001](001-hybrid-owl-skos-modeling.md) — SKOS for controlled vocabularies, OWL for
  domain entities; this is the pattern being applied
- [ADR-002](002-schema-data-separation.md) — why an enumerated value list is schema, not
  instance data
- Issue #67 and PR #86 — the Area vocabulary, and the granularity confusion that motivated
  keeping strata separate
- **Q6-4 (Brett, 2026-08-24), "mint from the source vocabulary always"** — the governing rule
  for the completeness half of this decision, and for later value lists. It also governs `PKE`
  and the sea-type life-history term, both documented in their sources and unobserved in the
  data to hand; this ADR is one application of it, not its statement.
