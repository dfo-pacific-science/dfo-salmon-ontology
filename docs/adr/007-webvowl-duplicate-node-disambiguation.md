# ADR-007: Disambiguate duplicate WebVOWL datatype nodes instead of merging them

## Status

Accepted

## Context

`scripts/normalize_webvowl_json.py` stabilizes the ids and ordering that WIDOCO's bundled
OWL2VOWL step emits into `docs/webvowl/data/ontology.json`. It identifies each node by an
id-free "semantic key" so that a node keeps its id across regenerations.

For named classes that key was `(type, iri)`, and the script required it to be globally
unique — raising `ValueError: Non-unique semantic class key` otherwise. Once the merged
`gcdfo` + `smn` import closure gained three datatype properties ranging over `xsd:gYear`
(`smn:returnYear`, `smn:catchYear`, `smn:broodYear`), OWL2VOWL emitted three separate
`rdfs:Datatype` nodes for that one IRI and the key stopped being unique. That is not a
generator bug: VOWL renders a datatype as a leaf node per property that points at it, so
the three nodes are genuinely distinct positions in the drawn graph.

The abort was invisible because the `docs-widoco` recipe swallowed it (see ADR consequences
below), so raw, id-unstable generator output was committed from PR #78 onward while the
gate reported success.

Two competing repairs were available.

## Decision

**Widen the key for the nodes that collide; do not merge them, and do not abort.**

1. A colliding class key is extended with that node's id-free wiring context — the
   `(domainOf|rangeOf, property type, property IRI, other endpoint IRI)` tuples that already
   disambiguate union nodes. Each `xsd:gYear` node is then keyed by the property that ranges
   over it, which is stable across runs.
2. Widening applies **only** to nodes that actually collide. Non-colliding classes keep the
   short `(type, iri)` key, so they continue to hold their baseline id across ontology edits
   instead of churning whenever a neighbouring property changes.
3. If nodes remain indistinguishable after widening, the script assigns ids positionally in
   a deterministic order and prints a warning to stderr, rather than raising.

The rejected alternative was to collapse the duplicates into one node. That was rejected
because it changes the rendered graph: three leaf `gYear` boxes would become one shared hub
with three incoming edges. The normalizer's contract is stability of serialization, not
editorial control over the drawing — "the goal is stability, not cleverness."

## Consequences

### Positive

- A legitimate generator output no longer turns into a build abort.
- Class-key disambiguation now mirrors how property keys already work (property keys have
  always carried their domain/range refs, which is why same-IRI properties such as
  `sosa:observedProperty` never collided).
- Union-node keying and duplicate-node keying share one `_reference_context` helper instead
  of two copies of the same logic.

### Negative

- A colliding node's key now depends on its neighbouring properties, so renaming one of
  those properties reassigns that node's id. This is confined to the colliding nodes.
- The positional fallback is best-effort: truly indistinguishable nodes may still drift
  between runs. It warns loudly when it is used, and has not triggered on this ontology.

### Neutral

- `docs/webvowl/data/ontology.json` was re-baselined once to the normalizer's own rendering.
  The previously committed file was raw generator output, so the first genuine ontology
  change would otherwise have produced a whole-file reformat bundled with the real diff.
  The re-baseline also lands the corrections the normalizer was always meant to apply:
  `owl:inverseOf` edges that OWL2VOWL drops (13 properties) and `skos:prefLabel` preference
  over `rdfs:label` (2 classes).

- One of those two classes shows why the label rule matters beyond cosmetics.
  `smn:EscapementSurveyEvent` carries **two** English `rdfs:label` values —
  "Escapement Survey Event" and "Escapement survey event" — so which one OWL2VOWL emits is
  an unforced choice between equally valid inputs, exactly the kind of thing that drifts
  between runs. Preferring `skos:prefLabel` ("Escapement Survey Event") pins it. The other
  case, `ENVO_00000234`, renders as "slough" — the label this ontology declares via
  `skos:prefLabel` — rather than ENVO's `rdfs:label` "bayou". Fixing the duplicate label
  upstream in smn would remove the ambiguity at its source; the normalizer makes the output
  stable either way.

## More Information

Two supporting changes were required to make this gate real rather than decorative:

- The `docs-widoco` recipe was a single `;`-separated shell command with no `set -e`, so make
  took the exit status of its trailing `echo` and printed "✅ WIDOCO regenerated into docs/"
  even when the normalizer had crashed. Verified by A/B: with the same injected normalizer
  failure, the recipe exits 0 and claims success without `set -e`, and exits 2 with
  `make: *** [docs-widoco] Error 1` with it. `release-snapshot` had the same shape and got
  the same fix.
- `.github/workflows/ci.yml` excluded `docs/webvowl/data/ontology.json` from its
  "did `make ci` produce uncommitted changes" check. That exclusion was added 2026-02-19,
  five weeks before the normalizer existed (2026-03-27), as a pre-normalizer workaround for
  exactly the churn the normalizer now prevents. It is removed: the file is byte-stable
  across consecutive `make ci` runs, and excluding it defeated the gate's only purpose.

Verification: `SMN_FLAT_TTL=/nonexistent/smn.ttl make ci` run twice leaves
`docs/webvowl/data/ontology.json` byte-identical (sha256
`4d3505463d48fc69946d8352906a84db630722ad649f3ceab4fc0f78d76321e3` against this branch's
`SMN_PIN` `a5d4f28`), with a clean `git status` for all generated artifacts, no normalizer
fallback warnings, and referential integrity intact (155 classes, 169 properties, zero
dangling id references — the same node counts as the raw output, so nothing was merged or
dropped). The same fix was verified against the smn 0.0.3 release pin `f7205ee` used by the
0.0.9 release branch, which yields a different but equally stable file; whichever pin the
merge settles on, `make ci` regenerates the artifact and the drift check enforces it.

## Related

- [ADR-004](004-robot-toolchain-selection.md) - the ROBOT/WIDOCO toolchain this gate wraps
- `docs/entrypoints.md` - where the normalizer sits in the `make docs-widoco` wiring
- `docs/tech-debt.md` - the 2026-03-15 WebVOWL churn entry this decision repairs
