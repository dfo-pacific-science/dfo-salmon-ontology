#!/usr/bin/env bash
# Run fast SPARQL lint checks used by make test / CI.

set -euo pipefail

ONTOLOGY_FILE="${1:-ontology/dfo-salmon.ttl}"
ROBOT_JAR="${ROBOT_JAR:-tools/robot.jar}"
ROBOT_CATALOG="${ROBOT_CATALOG:-}"
OUT_DIR="release/tmp"

if ! command -v java >/dev/null 2>&1; then
  echo "❌ Java is required to run ROBOT SPARQL checks." >&2
  exit 1
fi

if ! java -version >/dev/null 2>&1; then
  echo "❌ Java runtime is not available (install a JDK/JRE, then rerun)." >&2
  exit 1
fi

if [ ! -f "$ROBOT_JAR" ]; then
  echo "❌ ROBOT JAR not found at $ROBOT_JAR (run 'make install-robot')." >&2
  exit 1
fi

if [ ! -f "$ONTOLOGY_FILE" ]; then
  echo "❌ Ontology file not found: $ONTOLOGY_FILE" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

ROBOT_CATALOG_ARGS=()
if [ -n "$ROBOT_CATALOG" ] && [ -f "$ROBOT_CATALOG" ]; then
  ROBOT_CATALOG_ARGS=(--catalog "$ROBOT_CATALOG")
  echo "📚 Using ROBOT catalog for import resolution: $ROBOT_CATALOG"
fi

checks=(
  "scripts/sparql/missing-year-basis.rq|$OUT_DIR/missing-year-basis.tsv|Year-basis scheme migration"
  "scripts/sparql/missing-variable-decomposition.rq|$OUT_DIR/missing-variable-decomposition.tsv|Variable decomposition minimum"
  "scripts/sparql/no-legacy-variablehas.rq|$OUT_DIR/no-legacy-variablehas.tsv|No legacy variableHas* properties in canonical ontology"
  "scripts/sparql/skos-match-on-owl-properties.rq|$OUT_DIR/skos-match-on-owl-properties.tsv|No skos:*Match on OWL properties"
  "scripts/sparql/skos-match-on-owl-classes.rq|$OUT_DIR/skos-match-on-owl-classes.tsv|No skos:*Match on OWL classes"
)

failures=0

echo "🔎 Running SPARQL lint checks against $ONTOLOGY_FILE"
for check in "${checks[@]}"; do
  IFS='|' read -r query out label <<<"$check"

  if [ ! -f "$query" ]; then
    echo "❌ Missing query: $query" >&2
    failures=$((failures + 1))
    continue
  fi

  java -jar "$ROBOT_JAR" query \
    "${ROBOT_CATALOG_ARGS[@]}" \
    --input "$ONTOLOGY_FILE" \
    --query "$query" "$out"

  if [ -s "$out" ]; then
    echo "❌ $label failed (see $out)"
    failures=$((failures + 1))
  else
    echo "✅ $label passed"
  fi
done

if [ "$failures" -gt 0 ]; then
  echo "❌ SPARQL lint checks found $failures issue set(s)."
  exit 1
fi

echo "✅ All SPARQL lint checks passed."
