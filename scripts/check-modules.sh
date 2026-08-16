#!/usr/bin/env bash
# Validate the optional alignment overlays in ontology/modules/ the way a
# contributor actually uses them: merged with core.
#
# Why this exists: the overlays are not imported by ontology/dfo-salmon.ttl, so
# loading core alone says nothing about them. ontology/modules/README.md tells
# contributors to load them *alongside* core, and on that path the OWL API
# supplies a declaration for any otherwise-untyped IRI used in class or property
# position — so an overlay naming a term core no longer declares does not fail
# loudly, it silently mints that term. Eight retired gcdfo: terms survived that
# way after the core migration to smn:, five of them minted as fresh owl:Class /
# owl:ObjectProperty declarations. See ADR-007.
#
# Three checks per module, each of which states what would retire it:
#
#   A. Minted terms  — the merge must not declare any gcdfo:/smn: term that the
#      core closure does not already declare. Retires only if the OWL API stops
#      supplying declarations for untyped IRIs, i.e. never in practice.
#   B. Mapping-strength conflicts — the merge must not assert two different
#      skos:*Match predicates between the same ordered pair. Retires if the
#      overlays stop restating mappings the shared layer already makes, at which
#      point there is nothing left to contradict.
#   C. ELK consistency of the merged closure. Retires never; it is the minimum
#      claim a loadable overlay has to meet.
#
# Deliberately NOT checked here: skos:*Match between OWL classes
# (scripts/sparql/skos-match-on-owl-classes.rq). That is the shared layer's own
# cross-framework idiom — the imported smn closure contributes 18 such rows
# before any overlay is loaded, and smn deliberately demoted a subClassOf claim
# to skos:closeMatch (alignment finding F7). Linting the overlays for it would
# report upstream's modelling, not theirs. ADR-007 records the evidence. This
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

echo "🧩 Checking ${#modules[@]} alignment module(s) against $CORE_ONTOLOGY"

# Baseline: the core import closure on its own. Everything below is measured as
# a delta against this, so the overlays are judged only on what they add.
CORE_CLOSURE="$OUT_DIR/core-closure.ttl"
java -jar "$ROBOT_JAR" merge \
  "${ROBOT_CATALOG_ARGS[@]}" \
  --input "$CORE_ONTOLOGY" \
  --collapse-import-closure true \
  --output "$CORE_CLOSURE"

java -jar "$ROBOT_JAR" query \
  --input "$CORE_CLOSURE" \
  --query scripts/sparql/declared-owned-iris.rq "$OUT_DIR/core-declared.tsv"

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

  # A. Minted terms.
  java -jar "$ROBOT_JAR" query \
    --input "$merged" \
    --query scripts/sparql/declared-owned-iris.rq "$OUT_DIR/$name-declared.tsv"

  minted="$OUT_DIR/$name-minted.txt"
  LC_ALL=C comm -13 \
    <(tail -n +2 "$OUT_DIR/core-declared.tsv" | LC_ALL=C sort) \
    <(tail -n +2 "$OUT_DIR/$name-declared.tsv" | LC_ALL=C sort) \
    > "$minted"

  if [ -s "$minted" ]; then
    echo "❌ Minted terms: the merge declares gcdfo:/smn: terms core does not (see $minted)"
    sed 's/^/     /' "$minted"
    echo "     Each is a term this module names that core no longer declares."
    echo "     Retarget it at the term core uses, or delete the axiom — do not"
    echo "     re-declare the retired name. See ADR-007."
    failures=$((failures + 1))
  else
    echo "✅ Minted terms: none (module names no term core has retired)"
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
done

echo ""
if [ "$failures" -gt 0 ]; then
  echo "❌ Module checks found $failures problem(s)."
  exit 1
fi

echo "✅ All module checks passed."
