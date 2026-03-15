#!/bin/bash
# ROBOT Quality Check Script for DFO Salmon Ontology
# This script runs ROBOT with appropriate configuration for our hybrid OWL+SKOS ontology

set -e  # Exit on any error

# Configuration
ONTOLOGY_FILE="ontology/dfo-salmon.ttl"
PROFILE_FILE="robot-profile.yaml"
REPORT_FILE="release/artifacts/robot-quality-report.html"
LOG_FILE="release/artifacts/robot-quality-check.log"
ROBOT_CATALOG="${ROBOT_CATALOG:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 Running ROBOT quality check for DFO Salmon Ontology..."
echo "📁 Ontology: $ONTOLOGY_FILE"
echo "⚙️  Profile: $PROFILE_FILE"
echo "📊 Report: $REPORT_FILE"
echo ""

# Check if Java is available
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java is not installed or not in PATH${NC}"
    echo "Please install Java to run ROBOT"
    exit 1
fi

# Check if ROBOT JAR exists
if [ ! -f "tools/robot.jar" ]; then
    echo -e "${RED}❌ ROBOT JAR not found at tools/robot.jar${NC}"
    echo "Please download ROBOT and place it at tools/robot.jar"
    exit 1
fi

# Check if ontology file exists
if [ ! -f "$ONTOLOGY_FILE" ]; then
    echo -e "${RED}❌ Ontology file not found: $ONTOLOGY_FILE${NC}"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$REPORT_FILE")"
mkdir -p "$(dirname "$LOG_FILE")"

echo "🚀 Starting ROBOT report..."

CATALOG_ARGS=()
if [ -n "$ROBOT_CATALOG" ] && [ -f "$ROBOT_CATALOG" ]; then
    CATALOG_ARGS=(--catalog "$ROBOT_CATALOG")
    echo "📚 Using ROBOT catalog for import resolution: $ROBOT_CATALOG"
fi

# Run ROBOT with custom profile and fail-on ERROR
# This means:
# - The custom profile downgrades expected violations to INFO level
# - ERROR-level violations will still fail the build (genuine issues)
# - INFO-level violations won't fail the build (expected violations)

if [ -f "$PROFILE_FILE" ]; then
    echo "📋 Using custom profile: $PROFILE_FILE"
    java -jar tools/robot.jar report \
        "${CATALOG_ARGS[@]}" \
        --input "$ONTOLOGY_FILE" \
        --profile "$PROFILE_FILE" \
        --fail-on ERROR \
        --output "$REPORT_FILE" \
        > "$LOG_FILE" 2>&1
else
    echo "⚠️  Custom profile not found, using default settings"
    java -jar tools/robot.jar report \
        "${CATALOG_ARGS[@]}" \
        --input "$ONTOLOGY_FILE" \
        --fail-on ERROR \
        --output "$REPORT_FILE" \
        > "$LOG_FILE" 2>&1
fi

# Check exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ ROBOT quality check completed successfully${NC}"
    echo "📊 Report generated: $REPORT_FILE"
    echo "📝 Log file: $LOG_FILE"
    
    # Show summary of violations
    echo ""
    echo "📈 Violation Summary:"
    if [ -f "$LOG_FILE" ]; then
        grep -E "(ERROR|WARN|INFO)" "$LOG_FILE" | tail -10 || echo "No violations found"
    fi
    
elif [ $EXIT_CODE -eq 1 ]; then
    echo -e "${RED}❌ ROBOT found ERROR-level violations${NC}"
    echo "📊 Report generated: $REPORT_FILE"
    echo "📝 Log file: $LOG_FILE"
    echo ""
    echo "🔍 Check the report for details. ERROR-level violations need attention."
    
    # Show ERROR violations
    if [ -f "$LOG_FILE" ]; then
        echo "❌ ERROR violations found:"
        grep "ERROR" "$LOG_FILE" || echo "No ERROR violations in log"
    fi
    
    # Fail the build for ERROR-level violations
    exit 1
    
else
    echo -e "${RED}❌ ROBOT quality check failed with exit code $EXIT_CODE${NC}"
    echo "📝 Check log file: $LOG_FILE"
    
    if [ -f "$LOG_FILE" ]; then
        echo "🔍 Last 20 lines of log:"
        tail -20 "$LOG_FILE"
    fi
    
    exit $EXIT_CODE
fi

echo ""
echo "🎯 Expected violations (acceptable):"
echo "   • 31 SKOS label 'errors' (W3C SKOS compliant)"
echo "   • 8 Darwin Core label 'errors' (external imports)"
echo "   • 7 hybrid OWL+SKOS definition 'warnings' (ROBOT limitation)"
echo "   • 3 BFO definition 'warnings' (MIREOT approach)"
echo "   • 8 Darwin Core definition 'warnings' (external imports)"
echo ""
echo "📚 See docs/ROBOT_SETUP.md for detailed explanation of expected violations"
