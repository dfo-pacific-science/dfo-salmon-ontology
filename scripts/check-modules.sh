#!/usr/bin/env bash
# Validate the optional modules in ontology/modules/ the way a contributor
# actually uses them: merged with core.
#
# Why this exists: the modules are not imported by ontology/dfo-salmon.ttl, so
# loading core alone says nothing about them. ontology/modules/README.md tells
# contributors to load them *alongside* core, and on that path the OWL API
# supplies a declaration for any otherwise-untyped IRI used in class or property
# position — so a module naming a term core no longer declares does not fail
# loudly, it silently mints that term. Eight retired gcdfo: terms survived that
# way after the core migration to smn:, five of them minted as fresh owl:Class /
# owl:ObjectProperty declarations. See ADR-008.
#
# Two kinds of module live here, and the difference matters to check A only:
#
#   * an ALIGNMENT OVERLAY asserts relations between terms and should declare
#     nothing at all;
#   * a VOCABULARY MODULE enumerates the members of one SKOS concept scheme, so
#     declaring individuals is its entire job.
#
# Five checks per module, each of which states what would retire it:
#
#   A1. Minted schema terms — the merge must not declare any gcdfo:/smn: class
#       or property that the core closure does not already declare. This is the
#       ADR-008 guard, unchanged: every term in that incident was an owl:Class
#       or owl:ObjectProperty. Retires only if the OWL API stops supplying
#       declarations for untyped IRIs, i.e. never in practice.
#   A2. Minted individuals — every gcdfo:/smn: individual the merge adds must be
#       a member of a SKOS vocabulary the module itself declares (a skos:Concept
#       in a declared skos:ConceptScheme, or such a scheme). An individual that
#       is neither fails. This replaces the older blanket "declare nothing"
#       rule, which forbade vocabulary modules outright; it is strictly tighter
#       than that rule was for alignment overlays, which still add none.
#       Retires if the repo stops holding controlled vocabularies in modules.
#   B.  Mapping-strength conflicts — the merge must not assert two different
#       skos:*Match predicates between the same ordered pair. Retires if the
#       modules stop restating mappings the shared layer already makes, at which
#       point there is nothing left to contradict.
#   C.  ELK consistency of the merged closure. Retires never; it is the minimum
#       claim a loadable module has to meet.
#   D.  Theme coverage of the merged closure, using the same query `make
#       theme-coverage` runs over core. A term that leaves core for a module
#       must not thereby escape the gcdfo:theme rule — before this check
#       existed, moving a concept out of ontology/dfo-salmon.ttl silently
#       dropped it from the only check that enforces that rule. Retires if
#       gcdfo:theme stops being required.
#
# Deliberately NOT checked here: skos:*Match between OWL classes
# (scripts/sparql/skos-match-on-owl-classes.rq). That is the shared layer's own
# cross-framework idiom — the imported smn closure contributes 18 such rows
# before any overlay is loaded, and smn deliberately demoted a subClassOf claim
# to skos:closeMatch (alignment finding F7). Linting the overlays for it would
# report upstream's modelling, not theirs. ADR-008 records the evidence. This
# exemption retires if the shared layer moves off that idiom, at which point the
# class lint can be run over the merged closure like any other check.

set -euo pipefail

ROBOT_JAR="${ROBOT_JAR:-tools/robot.jar}"
ROBOT_CATALOG="${ROBOT_CATALOG:-release/tmp/robot-catalog.xml}"
CORE_ONTOLOGY="${CORE_ONTOLOGY:-ontology/dfo-salmon.ttl}"
MODULE_DIR="${MODULE_DIR:-ontology/modules}"
OUT_DIR="release/tmp/modules"

if ! command -v java >/dev/null 2>&1 || ! java -version >/dev/null 2>&1; then
  echo "❌ Java is required to run ROBOT module checks." >&2
  exit 1
fi

if [ ! -f "$ROBOT_JAR" ]; then
  echo "❌ ROBOT JAR not found at $ROBOT_JAR (run 'make install-robot')." >&2
  exit 1
fi

if [ ! -f "$CORE_ONTOLOGY" ]; then
  echo "❌ Core ontology not found: $CORE_ONTOLOGY" >&2
  exit 1
fi

ROBOT_CATALOG_ARGS=()
if [ -n "$ROBOT_CATALOG" ] && [ -f "$ROBOT_CATALOG" ]; then
  ROBOT_CATALOG_ARGS=(--catalog "$ROBOT_CATALOG")
fi

mkdir -p "$OUT_DIR"

shopt -s nullglob
modules=("$MODULE_DIR"/*.ttl)
shopt -u nullglob

if [ "${#modules[@]}" -eq 0 ]; then
  echo "❌ No modules found in $MODULE_DIR. This check exists to validate them; an" >&2
  echo "   empty directory means either the modules moved or the path is wrong." >&2
  exit 1
fi

echo "🧩 Checking ${#modules[@]} module(s) against $CORE_ONTOLOGY"

# Baseline: the core import closure on its own. Everything below is measured as
# a delta against this, so a module is judged only on what it adds.
CORE_CLOSURE="$OUT_DIR/core-closure.ttl"
java -jar "$ROBOT_JAR" merge \
  "${ROBOT_CATALOG_ARGS[@]}" \
  --input "$CORE_ONTOLOGY" \
  --collapse-import-closure true \
  --output "$CORE_CLOSURE"

java -jar "$ROBOT_JAR" query \
  --input "$CORE_CLOSURE" \
  --query scripts/sparql/declared-owned-iris.rq "$OUT_DIR/core-declared.tsv"

java -jar "$ROBOT_JAR" query \
  --input "$CORE_CLOSURE" \
  --query scripts/sparql/declared-owned-schema-iris.rq "$OUT_DIR/core-declared-schema.tsv"

failures=0

for module in "${modules[@]}"; do
  name="$(basename "$module" .ttl)"
  merged="$OUT_DIR/merged-$name.ttl"

  echo ""
  echo "── $module"

  # Core first: the module imports https://w3id.org/gcdfo/salmon, and the
  # catalog maps that IRI to the working-tree file, so the merge tests this
  # checkout rather than the published artifact.
  java -jar "$ROBOT_JAR" merge \
    "${ROBOT_CATALOG_ARGS[@]}" \
    --input "$CORE_ONTOLOGY" \
    --input "$module" \
    --output "$merged"

  # A1. Minted schema terms — classes and properties only. Must be empty.
  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/declared-owned-schema-iris.rq "$OUT_DIR/$name-declared-schema.tsv"

  minted_schema="$OUT_DIR/$name-minted-schema.txt"
  LC_ALL=C comm -13 \
    <(tail -n +2 "$OUT_DIR/core-declared-schema.tsv" | LC_ALL=C sort) \
    <(tail -n +2 "$OUT_DIR/$name-declared-schema.tsv" | LC_ALL=C sort) \
    > "$minted_schema"

  if [ -s "$minted_schema" ]; then
    echo "❌ Minted schema terms: the merge declares gcdfo:/smn: classes or properties core does not (see $minted_schema)"
    sed 's/^/     /' "$minted_schema"
    echo "     Each is a term this module names that core no longer declares."
    echo "     Retarget it at the term core uses, or delete the axiom — do not"
    echo "     re-declare the retired name. See ADR-008. A module may not add a"
    echo "     class or property; core is where schema is declared."
    failures=$((failures + 1))
  else
    echo "✅ Minted schema terms: none (module names no class or property core has retired)"
  fi

  # A2. Minted individuals — allowed only as members of a vocabulary this
  # module declares.
  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/declared-owned-iris.rq "$OUT_DIR/$name-declared.tsv"

  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/vocabulary-members.rq "$OUT_DIR/$name-vocabulary-members.tsv"

  minted="$OUT_DIR/$name-minted.txt"
  LC_ALL=C comm -13 \
    <(tail -n +2 "$OUT_DIR/core-declared.tsv" | LC_ALL=C sort) \
    <(tail -n +2 "$OUT_DIR/$name-declared.tsv" | LC_ALL=C sort) \
    > "$minted"

  # Anything minted that is not a schema term is an individual.
  minted_individuals="$OUT_DIR/$name-minted-individuals.txt"
  LC_ALL=C comm -13 \
    <(LC_ALL=C sort "$minted_schema") \
    <(LC_ALL=C sort "$minted") \
    > "$minted_individuals"

  stray="$OUT_DIR/$name-stray-individuals.txt"
  LC_ALL=C comm -23 \
    <(LC_ALL=C sort "$minted_individuals") \
    <(tail -n +2 "$OUT_DIR/$name-vocabulary-members.tsv" | LC_ALL=C sort) \
    > "$stray"

  vocabulary_count="$(wc -l < "$minted_individuals" | tr -d ' ')"

  if [ -s "$stray" ]; then
    echo "❌ Stray individuals: the merge declares gcdfo:/smn: individuals that are not vocabulary members (see $stray)"
    sed 's/^/     /' "$stray"
    echo "     A module may add individuals only as skos:Concept members of a"
    echo "     skos:ConceptScheme it declares itself. Anything else is an"
    echo "     addition nothing in this repo checks."
    failures=$((failures + 1))
  elif [ "$vocabulary_count" -gt 0 ]; then
    echo "✅ Minted individuals: $vocabulary_count, all members of a vocabulary this module declares"
  else
    echo "✅ Minted individuals: none"
  fi

  # B. Mapping-strength conflicts.
  conflicts="$OUT_DIR/$name-mapping-conflicts.tsv"
  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/conflicting-mapping-strength.rq "$conflicts"

  if [ -s "$conflicts" ]; then
    echo "❌ Mapping-strength conflicts in the merged closure (see $conflicts)"
    tail -n +2 "$conflicts" | sed 's/^/     /'
    echo "     Two skos:*Match predicates on one pair. Match the shared layer's"
    echo "     strength rather than restating it differently."
    failures=$((failures + 1))
  else
    echo "✅ Mapping strength: no pair carries two different skos:*Match predicates"
  fi

  # C. Consistency.
  if java -jar "$ROBOT_JAR" reason \
    --input "$merged" \
    --reasoner ELK \
    --output "$OUT_DIR/$name-reasoned.ttl" >"$OUT_DIR/$name-reason.log" 2>&1; then
    echo "✅ ELK: merged closure is consistent"
  else
    echo "❌ ELK: merged closure is inconsistent (see $OUT_DIR/$name-reason.log)"
    tail -n 20 "$OUT_DIR/$name-reason.log" | sed 's/^/     /'
    failures=$((failures + 1))
  fi

  # D. Theme coverage — the same query `make theme-coverage` runs over core.
  themes="$OUT_DIR/$name-theme-coverage.tsv"
  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/theme-coverage.rq "$themes"

  if [ -s "$themes" ]; then
    echo "❌ Theme coverage: the merged closure has gcdfo: terms with a theme problem (see $themes)"
    tail -n +2 "$themes" | head -n 20 | sed 's/^/     /'
    echo "     Same rule as core: every gcdfo: class, property, concept and"
    echo "     scheme carries 1-3 gcdfo:theme values drawn from gcdfo:ThemeScheme."
    failures=$((failures + 1))
  else
    echo "✅ Theme coverage: clean over the merged closure"
  fi
done

echo ""
if [ "$failures" -gt 0 ]; then
  echo "❌ Module checks found $failures problem(s)."
  exit 1
fi

echo "✅ All module checks passed."
