#!/usr/bin/env bash
# Thin wrapper to run ROBOT from the pinned jar inside devenv.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROBOT_JAR="$(cd "${SCRIPT_DIR}/.." && pwd)/tools/robot.jar"
if [ ! -f "${ROBOT_JAR}" ]; then
  echo "ROBOT jar not found at ${ROBOT_JAR}. Download it via 'make install-robot' or update the path." >&2
  exit 1
fi
exec java -jar "${ROBOT_JAR}" "$@"
