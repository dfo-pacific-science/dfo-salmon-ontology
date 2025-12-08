#!/bin/bash
# Pre-commit hook to validate ontology with ROBOT
# This runs the same validation as the CI workflow

set -e

# Configuration
ONTOLOGY_FILE="ontology/dfo-salmon.ttl"
ROBOT_VERSION="1.9.8"
ROBOT_JAR="tools/robot.jar"
ROBOT_URL="https://github.com/ontodev/robot/releases/download/v${ROBOT_VERSION}/robot.jar"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Validating ontology with ROBOT..."

# Check if Java is available
if ! command -v java &> /dev/null; then
    echo -e "${RED}Error: Java is not installed or not in PATH${NC}"
    echo "Please install Java 11 or later to run ROBOT validation"
    exit 1
fi

# Check if ROBOT JAR exists (try multiple locations)
if [ -f "$ROBOT_JAR" ]; then
    :
else
    echo -e "${YELLOW}ROBOT JAR not found. Downloading ROBOT v${ROBOT_VERSION}...${NC}"
    mkdir -p "$(dirname "$ROBOT_JAR")"
    # Use curl (available on macOS) or wget (available on Linux)
    if command -v curl &> /dev/null; then
        curl -L -s -o "$ROBOT_JAR" "$ROBOT_URL"
    elif command -v wget &> /dev/null; then
        wget -q "$ROBOT_URL" -O "$ROBOT_JAR"
    else
        echo -e "${RED}Error: Neither curl nor wget is available. Please install one to download ROBOT.${NC}"
        exit 1
    fi
    echo -e "${GREEN}ROBOT downloaded successfully${NC}"
fi

# Check if ontology file exists
if [ ! -f "$ONTOLOGY_FILE" ]; then
    echo -e "${RED}Error: Ontology file not found: $ONTOLOGY_FILE${NC}"
    exit 1
fi

# Run ROBOT reasoning as validation
# If reasoning succeeds, the ontology is valid
echo "Running ROBOT reasoning validation..."
TEMP_OUTPUT=$(mktemp /tmp/robot-reasoned-XXXXXX.ttl)
trap "rm -f $TEMP_OUTPUT" EXIT

# Run ROBOT and capture output
# Temporarily disable set -e to capture exit code
set +e
ROBOT_OUTPUT=$(java -jar "$ROBOT_JAR" reason \
    --input "$ONTOLOGY_FILE" \
    --reasoner ELK \
    --output "$TEMP_OUTPUT" 2>&1)
ROBOT_EXIT_CODE=$?
set -e

if [ $ROBOT_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Ontology validation passed${NC}"
    exit 0
else
    echo -e "${RED}✗ Ontology validation failed${NC}"
    echo "The ontology could not be reasoned, indicating validation errors."
    if [ -n "$ROBOT_OUTPUT" ]; then
        echo "ROBOT output:"
        echo "$ROBOT_OUTPUT"
    fi
    exit 1
fi
