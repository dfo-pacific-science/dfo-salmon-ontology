# DFO Salmon Ontology Makefile
# Provides convenient commands for ontology development and quality checking

.PHONY: help quality-check reason convert clean install-robot

# Default target
help:
	@echo "DFO Salmon Ontology - Available Commands:"
	@echo ""
	@echo "Quality & Validation:"
	@echo "  quality-check    Run ROBOT quality check with proper configuration"
	@echo "  reason          Run OWL reasoner (ELK) to check logical consistency"
	@echo "  reason-all      Run all available reasoners (ELK, HermiT, JFact)"
	@echo ""
	@echo "Format Conversion:"
	@echo "  convert-owl     Convert to OWL format"
	@echo "  convert-json    Convert to JSON-LD format"
	@echo ""
	@echo "Setup:"
	@echo "  install-robot   Download ROBOT JAR file"
	@echo "  clean          Remove generated files"
	@echo ""
	@echo "Documentation:"
	@echo "  docs           Open documentation in browser"

# Quality checking with proper ROBOT configuration
quality-check:
	@echo "🔍 Running ROBOT quality check..."
	@./scripts/robot-quality-check.sh

# OWL reasoning
reason:
	@echo "🧠 Running OWL reasoner (ELK)..."
	@mkdir -p release/artifacts
	@java -jar tools/robot.jar reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner ELK \
		--output release/artifacts/elk-inferred.ttl
	@echo "✅ Reasoning completed. Output: release/artifacts/elk-inferred.ttl"

reason-all: reason
	@echo "🧠 Running HermiT reasoner..."
	@java -jar tools/robot.jar reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner HermiT \
		--output release/artifacts/hermit-inferred.ttl
	@echo "🧠 Running JFact reasoner..."
	@java -jar tools/robot.jar reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner JFact \
		--output release/artifacts/jfact-inferred.ttl
	@echo "✅ All reasoners completed."

# Format conversion
convert-owl:
	@echo "🔄 Converting to OWL format..."
	@mkdir -p release/artifacts
	@java -jar tools/robot.jar convert \
		--input ontology/dfo-salmon.ttl \
		--output release/artifacts/dfo-salmon.owl
	@echo "✅ OWL conversion completed."

convert-json:
	@echo "🔄 Converting to JSON-LD format..."
	@mkdir -p release/artifacts
	@java -jar tools/robot.jar convert \
		--input ontology/dfo-salmon.ttl \
		--output release/artifacts/dfo-salmon.jsonld
	@echo "✅ JSON-LD conversion completed."

# Setup
install-robot:
	@echo "📥 Downloading ROBOT..."
	@mkdir -p tools
	@wget -O tools/robot.jar https://github.com/ontodev/robot/releases/download/v1.9.8/robot.jar
	@echo "✅ ROBOT installed at tools/robot.jar"

# Cleanup
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf release/artifacts/*.ttl
	@rm -rf release/artifacts/*.owl
	@rm -rf release/artifacts/*.jsonld
	@rm -rf release/artifacts/*.html
	@rm -rf release/artifacts/*.log
	@echo "✅ Cleanup completed."

# Documentation
docs:
	@echo "📚 Opening documentation..."
	@open docs/CONVENTIONS.md || xdg-open docs/CONVENTIONS.md || echo "Please open docs/CONVENTIONS.md manually"

# Check if ROBOT is installed
check-robot:
	@if [ ! -f "tools/robot.jar" ]; then \
		echo "❌ ROBOT not found. Run 'make install-robot' first."; \
		exit 1; \
	fi

# Ensure ROBOT is installed before running commands that need it
quality-check reason reason-all convert-owl convert-json: check-robot
