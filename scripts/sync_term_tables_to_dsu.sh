#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_DSU_DIR="${REPO_ROOT}/../data-stewardship-unit/data/ontology"
DSU_DIR="${DSU_ONTOLOGY_DIR:-$DEFAULT_DSU_DIR}"
SRC_DIR="${REPO_ROOT}/release/artifacts/term-tables"
DEST_DIR="${DSU_DIR}/release/artifacts/term-tables"
DSU_REPO_ROOT="$(cd "${DSU_DIR}/.." && pwd 2>/dev/null || true)"

echo "📂 Source term tables: ${SRC_DIR}"
echo "📂 DSU target: ${DEST_DIR}"

if [ ! -d "${SRC_DIR}" ]; then
  echo "❌ Source term tables not found at ${SRC_DIR}. Run make publish-and-extract first." >&2
  exit 1
fi

mkdir -p "${DEST_DIR}"
rsync -a --delete "${SRC_DIR}/" "${DEST_DIR}/"

echo "✅ Synced term tables to ${DEST_DIR}"
echo "ℹ️ Set DSU_ONTOLOGY_DIR to override the default target if needed."

# Offer to stage the submodule update if in a git repo
if [ -n "${DSU_REPO_ROOT}" ] && [ -d "${DSU_REPO_ROOT}/.git" ]; then
  echo "ℹ️ Detected DSU repo at ${DSU_REPO_ROOT}."
  echo "   If you want to stage the submodule pointer, run:"
  echo "     cd ${DSU_REPO_ROOT} && git add data/ontology && git status"
fi
