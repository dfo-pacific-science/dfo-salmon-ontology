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
	@echo "  publish-validate  Validate publish-ready metadata"
	@echo "  publish-slice     Generate publish slice (PublishReady terms only)"
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

# Publish-ready validation (checks metadata for PublishReady terms)
publish-validate: check-robot
	@mkdir -p release/published
	@java -jar tools/robot.jar query \
		--input draft/dfo-salmon-draft.ttl \
		--query scripts/sparql/publish-ready-metadata.rq \
		release/published/publish-ready-metadata.tsv
	@if [ -s release/published/publish-ready-metadata.tsv ] && [ $$(wc -l < release/published/publish-ready-metadata.tsv) -gt 1 ]; then \
		echo "❌ PublishReady metadata issues found:"; \
		cat release/published/publish-ready-metadata.tsv; \
		exit 1; \
	else \
		echo "✅ No PublishReady metadata issues detected"; \
	fi

# Publish slice generation (extract PublishReady terms, strip publicationStatus)
publish-slice: check-robot
	@mkdir -p release/published
	@java -jar tools/robot.jar query \
		--input draft/dfo-salmon-draft.ttl \
		--query scripts/sparql/publish-ready-terms.rq \
		release/published/publish-ready-terms.tsv
	@tail -n +2 release/published/publish-ready-terms.tsv | cut -f1 > release/published/publish-ready-terms.txt || true
	@if [ ! -s release/published/publish-ready-terms.txt ]; then \
		echo "⚠️  No PublishReady terms found; writing empty publish slice."; \
		echo "# Empty publish slice (no terms marked PublishReady)" > release/published/dfoc-core.ttl; \
	else \
		java -jar tools/robot.jar extract \
			--method STAR \
			--input draft/dfo-salmon-draft.ttl \
			--term-file release/published/publish-ready-terms.txt \
			--output release/published/dfoc-core.raw.ttl; \
		java -jar tools/robot.jar remove \
			--input release/published/dfoc-core.raw.ttl \
			--select annotations \
			--term dfoc:publicationStatus \
			--output release/published/dfoc-core.ttl; \
		rm -f release/published/dfoc-core.raw.ttl; \
		echo "✅ Publish slice generated at release/published/dfoc-core.ttl"; \
	fi

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
