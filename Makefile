# DFO Salmon Ontology Makefile
# Provides convenient commands for ontology development and quality checking

ROBOT_VERSION := 1.9.8
ROBOT_JAR := tools/robot.jar
ROBOT_URL := https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar
DSU_ONTOLOGY_DIR ?= ../data-stewardship-unit/data/ontology

.PHONY: help quality-check reason convert clean install-robot publish-clean dsu-sync-term-tables dsu-sync-and-stage theme-coverage test

# Default target
help:
	@echo "DFO Salmon Ontology - Available Commands:"
	@echo ""
	@echo "Quality & Validation:"
	@echo "  quality-check    Run ROBOT quality check with proper configuration"
	@echo "  reason          Run OWL reasoner (ELK) to check logical consistency"
	@echo "  reason-all      Run all available reasoners (ELK, HermiT, JFact)"
	@echo "  theme-coverage  Run gcdfo:theme coverage SPARQL check (writes release/tmp/theme-coverage.tsv)"
	@echo "  test            Run fast validation bundle: theme-coverage + ELK reasoning"
	@echo ""
	@echo "Format Conversion:"
	@echo "  convert-owl     Convert to OWL format"
	@echo "  convert-json    Convert to JSON-LD format"
	@echo ""
	@echo "Setup:"
	@echo "  install-robot   Download ROBOT JAR file"
	@echo "  clean          Remove generated files"
	@echo "  dsu-sync-term-tables Sync term tables into DSU submodule (DSU_ONTOLOGY_DIR)"
	@echo "  dsu-sync-and-stage  Sync term tables and stage DSU submodule (if clean)"
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
	@java -jar $(ROBOT_JAR) reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner ELK \
		--output release/artifacts/elk-inferred.ttl
	@echo "✅ Reasoning completed. Output: release/artifacts/elk-inferred.ttl"

reason-all: reason
	@echo "🧠 Running HermiT reasoner..."
	@java -jar $(ROBOT_JAR) reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner HermiT \
		--output release/artifacts/hermit-inferred.ttl
	@echo "🧠 Running JFact reasoner..."
	@java -jar $(ROBOT_JAR) reason \
		--input ontology/dfo-salmon.ttl \
		--reasoner JFact \
		--output release/artifacts/jfact-inferred.ttl
	@echo "✅ All reasoners completed."

# Format conversion
convert-owl:
	@echo "🔄 Converting to OWL format..."
	@mkdir -p release/artifacts
	@java -jar $(ROBOT_JAR) convert \
		--input ontology/dfo-salmon.ttl \
		--output release/artifacts/dfo-salmon.owl
	@echo "✅ OWL conversion completed."

convert-json:
	@echo "🔄 Converting to JSON-LD format..."
	@mkdir -p release/artifacts
	@java -jar $(ROBOT_JAR) convert \
		--input ontology/dfo-salmon.ttl \
		--output release/artifacts/dfo-salmon.jsonld
	@echo "✅ JSON-LD conversion completed."

theme-coverage: check-robot
	@echo "🔎 Running theme coverage check..."
	@mkdir -p release/tmp
	@java -jar $(ROBOT_JAR) query \
		--input ontology/dfo-salmon.ttl \
		--query scripts/sparql/theme-coverage.rq \
		release/tmp/theme-coverage.tsv
	@if [ -s release/tmp/theme-coverage.tsv ]; then \
		echo "⚠️ Theme coverage found issues. Inspect release/tmp/theme-coverage.tsv."; \
	else \
		echo "✅ Theme coverage clean (release/tmp/theme-coverage.tsv is empty)."; \
	fi

test: theme-coverage reason
	@echo "✅ Test bundle completed (theme coverage + ELK reasoning)."

# Setup
install-robot:
	@echo "📥 Downloading ROBOT..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -L $(ROBOT_URL) -o $(ROBOT_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(ROBOT_JAR) $(ROBOT_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch ROBOT."; \
		exit 1; \
	fi
	@echo "✅ ROBOT installed at $(ROBOT_JAR)"

# Cleanup
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf release/artifacts/*.ttl
	@rm -rf release/artifacts/*.owl
	@rm -rf release/artifacts/*.jsonld
	@rm -rf release/artifacts/*.html
	@rm -rf release/artifacts/*.log
	@echo "✅ Cleanup completed."

# Sync term tables into DSU submodule (local)
dsu-sync-term-tables:
	@./scripts/sync_term_tables_to_dsu.sh

# Sync and stage DSU submodule pointer when repo is otherwise clean
dsu-sync-and-stage: dsu-sync-term-tables
	@if [ ! -d "$(DSU_ONTOLOGY_DIR)" ]; then \
		echo "❌ DSU ontology dir not found: $(DSU_ONTOLOGY_DIR). Set DSU_ONTOLOGY_DIR or adjust path."; \
		exit 1; \
	fi
	@DSU_ROOT=$$(cd "$(DSU_ONTOLOGY_DIR)/../.." && pwd); \
	if [ ! -d "$$DSU_ROOT/.git" ]; then \
		echo "❌ DSU repo not found at $$DSU_ROOT"; exit 1; \
	fi; \
	OTHER=$$(cd "$$DSU_ROOT" && git status --porcelain | grep -v '^?? data/ontology' | grep -v '^ M data/ontology' || true); \
	if [ -n "$$OTHER" ]; then \
		echo "ℹ️ DSU repo has other changes; not staging data/ontology."; \
		echo "$$OTHER"; \
	else \
		cd "$$DSU_ROOT" && git add data/ontology && git status --short; \
		echo "✅ Staged data/ontology in DSU repo"; \
	fi

# Documentation
docs:
	@echo "📚 Opening documentation..."
	@open docs/CONVENTIONS.md || xdg-open docs/CONVENTIONS.md || echo "Please open docs/CONVENTIONS.md manually"

# Check if ROBOT is installed
check-robot:
	@if [ ! -f "$(ROBOT_JAR)" ]; then \
		echo "❌ ROBOT not found at $(ROBOT_JAR). Run 'make install-robot' first."; \
		exit 1; \
	fi

# Ensure ROBOT is installed before running commands that need it
quality-check reason reason-all convert-owl convert-json: check-robot
