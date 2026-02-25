# DFO Salmon Ontology Makefile
# Provides convenient commands for ontology development and quality checking

ROBOT_VERSION := 1.9.8
ROBOT_JAR := tools/robot.jar
ROBOT_URL := https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar
WIDOCO_VERSION := 1.4.25
WIDOCO_JAR := tools/widoco.jar
WIDOCO_URL := https://github.com/dgarijo/Widoco/releases/download/v$(WIDOCO_VERSION)/widoco-$(WIDOCO_VERSION)-jar-with-dependencies_JDK-17.jar
DSU_ONTOLOGY_DIR ?= ../data-stewardship-unit/data/ontology

.PHONY: help quality-check reason convert clean install-robot install-widoco publish-clean dsu-sync-term-tables dsu-sync-and-stage theme-coverage alpha-lint test docs-refresh docs-widoco docs-serializations docs-skos docs-postprocess release-snapshot

# Default target
help:
	@echo "DFO Salmon Ontology - Available Commands:"
	@echo ""
	@echo "Quality & Validation:"
	@echo "  quality-check    Run ROBOT quality check with proper configuration"
	@echo "  reason          Run OWL reasoner (ELK) to check logical consistency"
	@echo "  reason-all      Run all available reasoners (ELK, HermiT, JFact)"
	@echo "  theme-coverage  Run gcdfo:theme coverage SPARQL check (writes release/tmp/theme-coverage.tsv)"
	@echo "  alpha-lint      Run alpha migration SPARQL lints (year-basis scheme, variable decomposition, skos:*Match property lint)"
	@echo "  test            Run fast validation bundle: theme-coverage + alpha-lint + ELK reasoning"
	@echo ""
	@echo "Format Conversion:"
	@echo "  convert-owl     Convert to OWL format"
	@echo "  convert-json    Convert to JSON-LD format"
	@echo ""
	@echo "Setup:"
	@echo "  install-robot   Download ROBOT JAR file"
	@echo "  install-widoco  Download WIDOCO JAR file"
	@echo "  clean          Remove generated files"
	@echo ""
	@echo "Documentation:"
	@echo "  docs           Open documentation in browser"
	@echo "  docs-widoco    Regenerate WIDOCO HTML docs into docs/"
	@echo "  release-snapshot VERSION=X.Y.Z  Create an immutable docs snapshot under docs/releases/VERSION/"

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
	@python3 scripts/convert_ttl_to_jsonld.py ontology/dfo-salmon.ttl release/artifacts/dfo-salmon.jsonld
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

alpha-lint: check-robot
	@./scripts/run-sparql-lint.sh ontology/dfo-salmon.ttl

test: theme-coverage alpha-lint reason
	@echo "✅ Test bundle completed (theme coverage + alpha-lint + ELK reasoning)."

ci:
	@echo "🔁 Running full CI bundle (tests, quality, docs)..."
	@$(MAKE) test
	@$(MAKE) quality-check
	@$(MAKE) docs-refresh
	@echo "✅ CI bundle completed."

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

# WIDOCO setup
install-widoco:
	@echo "📥 Downloading WIDOCO..."
	@mkdir -p tools
	@if command -v curl >/dev/null 2>&1; then \
		curl -L $(WIDOCO_URL) -o $(WIDOCO_JAR); \
	elif command -v wget >/dev/null 2>&1; then \
		wget -O $(WIDOCO_JAR) $(WIDOCO_URL); \
	else \
		echo "Neither curl nor wget is available; please install one to fetch WIDOCO."; \
		exit 1; \
	fi
	@echo "✅ WIDOCO installed at $(WIDOCO_JAR)"

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

# Refresh docs artifacts (serializations + index.html SKOS section)
docs-widoco: check-widoco
	@echo "🧙 Regenerating WIDOCO docs..."
	@OUT="release/tmp/widoco"; \
	rm -rf "$$OUT"; \
	mkdir -p "$$OUT"; \
		java -jar $(WIDOCO_JAR) \
			-ontFile ontology/dfo-salmon.ttl \
			-outFolder "$$OUT" \
			-ignoreIndividuals \
			-uniteSections \
			-webVowl \
			-rewriteAll \
			-noPlaceHolderText; \
	if [ -f "$$OUT/index-en.html" ] && [ ! -f "$$OUT/index.html" ]; then \
		cp "$$OUT/index-en.html" "$$OUT/index.html"; \
	fi; \
	rsync -a --exclude "/ontology.*" "$$OUT/" docs/; \
	rm -f docs/ontology.jsonld docs/ontology.nt docs/ontology.owl docs/ontology.ttl; \
	rm -rf "$$OUT"; \
	echo "✅ WIDOCO regenerated into docs/"

docs-serializations: check-robot
	@echo "🔄 Regenerating docs/ downloadable serializations..."
	@mkdir -p docs
	@java -jar $(ROBOT_JAR) convert --input ontology/dfo-salmon.ttl --output docs/gcdfo.ttl
	@java -jar $(ROBOT_JAR) convert --input ontology/dfo-salmon.ttl --output docs/gcdfo.owl
	@python3 scripts/convert_ttl_to_jsonld.py ontology/dfo-salmon.ttl docs/gcdfo.jsonld
	@echo "✅ Wrote docs/gcdfo.ttl, docs/gcdfo.owl, docs/gcdfo.jsonld"

docs-skos:
	@echo "🧾 Refreshing SKOS sections in docs/index.html..."
	@python3 scripts/generate_skos_section.py
	@echo "✅ Updated docs/index.html SKOS section (and enforced OWL-before-SKOS ordering)"

docs-postprocess:
	@echo "🧩 Applying project-specific WIDOCO post-processing..."
	@python3 scripts/postprocess_widoco_html.py
	@echo "✅ WIDOCO post-processing complete."

docs-refresh: docs-widoco docs-serializations docs-skos docs-postprocess
	@echo "✅ Docs refresh complete."

# Create an immutable snapshot of the current published artifacts under docs/releases/<version>/.
#
# This is intended for GitHub Pages publishing when Pages is configured to serve from /docs.
# Snapshots are treated as immutable: by default, the target refuses to overwrite an existing folder.
#
# Usage:
#   make release-snapshot VERSION=0.0.999
#   make release-snapshot VERSION=0.0.999 FORCE=1   # overwrite (not recommended)
release-snapshot: docs-refresh
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ VERSION is required (e.g., make release-snapshot VERSION=0.0.999)"; \
		exit 1; \
	fi
	@DEST="docs/releases/$(VERSION)"; \
	if [ -d "$$DEST" ] && [ "$(FORCE)" != "1" ]; then \
		echo "❌ Snapshot already exists: $$DEST (set FORCE=1 to overwrite)"; \
		exit 1; \
	fi; \
	mkdir -p "$$DEST"; \
		cp docs/gcdfo.ttl "$$DEST/gcdfo.ttl"; \
		cp docs/gcdfo.owl "$$DEST/gcdfo.owl"; \
		cp docs/gcdfo.jsonld "$$DEST/gcdfo.jsonld"; \
		printf '%s\n' \
			'<!DOCTYPE html>' \
			'<html lang="en">' \
			'<head>' \
				'  <meta charset="UTF-8" />' \
				'  <meta name="viewport" content="width=device-width, initial-scale=1" />' \
				'  <link rel="canonical" href="https://w3id.org/gcdfo/salmon/$(VERSION)" />' \
				'  <title>DFO Salmon Ontology — Version $(VERSION)</title>' \
				'</head>' \
				'<body>' \
				'  <main>' \
			'    <h1>DFO Salmon Ontology — Version $(VERSION)</h1>' \
			'    <p>This is an immutable release snapshot hosted from GitHub Pages.</p>' \
			'    <h2>Download</h2>' \
			'    <ul>' \
			'      <li><a href="gcdfo.ttl">Turtle (TTL)</a></li>' \
			'      <li><a href="gcdfo.owl">RDF/XML (OWL)</a></li>' \
			'      <li><a href="gcdfo.jsonld">JSON-LD</a></li>' \
			'    </ul>' \
			'    <h2>Links</h2>' \
			'    <ul>' \
			'      <li>Latest documentation: <a href="https://w3id.org/gcdfo/salmon">https://w3id.org/gcdfo/salmon</a></li>' \
			'      <li>Repository: <a href="https://github.com/dfo-pacific-science/dfo-salmon-ontology">https://github.com/dfo-pacific-science/dfo-salmon-ontology</a></li>' \
			'    </ul>' \
			'  </main>' \
			'</body>' \
			'</html>' \
			> "$$DEST/index.html"
	@echo "✅ Wrote snapshot: docs/releases/$(VERSION)/ (index.html + gcdfo.{ttl,owl,jsonld})"

# Check if ROBOT is installed
check-robot:
	@if [ ! -f "$(ROBOT_JAR)" ]; then \
		echo "❌ ROBOT not found at $(ROBOT_JAR). Run 'make install-robot' first."; \
		exit 1; \
	fi

# Check if WIDOCO is installed
check-widoco:
	@if [ ! -f "$(WIDOCO_JAR)" ]; then \
		echo "❌ WIDOCO not found at $(WIDOCO_JAR). Run 'make install-widoco' first."; \
		exit 1; \
	fi

# Ensure ROBOT is installed before running commands that need it
quality-check reason reason-all convert-owl convert-json: check-robot
