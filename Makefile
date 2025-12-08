# DFO Salmon Ontology Makefile
# Provides convenient commands for ontology development and quality checking

ROBOT_VERSION := 1.9.8
ROBOT_JAR := tools/robot.jar
ROBOT_URL := https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar
DSU_ONTOLOGY_DIR ?= ../data-stewardship-unit/data/ontology

.PHONY: help quality-check reason convert clean install-robot publish-clean dsu-sync-term-tables dsu-sync-and-stage

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
	@echo "  publish-clean     Remove publish temp artifacts (release/tmp/*)"
	@echo "  publish-and-extract  Run publish slice, validations, and term-table extraction"
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

# Publish-ready validation (checks metadata for PublishReady terms)
publish-validate: check-robot
	@mkdir -p release/tmp
	@java -jar $(ROBOT_JAR) query \
		--input draft/dfo-salmon-draft.ttl \
		--query scripts/sparql/publish-ready-metadata.rq \
		release/tmp/publish-ready-metadata.tsv
	@if [ -s release/tmp/publish-ready-metadata.tsv ] && [ $$(wc -l < release/tmp/publish-ready-metadata.tsv) -gt 1 ]; then \
		echo "❌ PublishReady metadata issues found:"; \
		cat release/tmp/publish-ready-metadata.tsv; \
		exit 1; \
	else \
		echo "✅ No PublishReady metadata issues detected"; \
	fi

# Publish slice generation (extract PublishReady terms, strip publicationStatus) -> ontology/dfo-salmon.ttl
publish-slice: check-robot
	@mkdir -p release/tmp
	@java -jar $(ROBOT_JAR) query \
		--input draft/dfo-salmon-draft.ttl \
		--query scripts/sparql/publish-ready-terms.rq \
		release/tmp/publish-ready-terms.tsv
	@tail -n +2 release/tmp/publish-ready-terms.tsv | cut -f1 | sed 's/[<>]//g' > release/tmp/publish-ready-terms.txt || true
	@TERMCOUNT=$$(grep -c '[^[:space:]]' release/tmp/publish-ready-terms.txt || true); \
	if [ "$$TERMCOUNT" -eq 0 ]; then \
		echo "⚠️  No PublishReady terms found; writing empty publish slice."; \
		echo "# Empty publish slice (no terms marked PublishReady)" > release/tmp/dfoc-core.ttl; \
	else \
		if java -jar $(ROBOT_JAR) extract \
			--method STAR \
			--input draft/dfo-salmon-draft.ttl \
			--term-file release/tmp/publish-ready-terms.txt \
			--output release/tmp/dfoc-core.raw.ttl; then \
			python -c "from rdflib import Graph, URIRef; from rdflib.namespace import RDF, RDFS, OWL; ONT='https://w3id.org/gcdfos/salmon'; PUB='https://w3id.org/gcdfos/salmon#publicationStatus'; EXTRA_PREFIXES={'gcdfos':'https://w3id.org/gcdfos/salmon#','bfo':'http://purl.obolibrary.org/obo/BFO_','dwc':'http://rs.tdwg.org/dwc/terms/','dwciri':'http://rs.tdwg.org/dwc/iri/','qudt':'http://qudt.org/schema/qudt/','qudtunit':'http://qudt.org/vocab/unit/','oa':'http://www.w3.org/ns/oa#','envo':'http://purl.obolibrary.org/obo/ENVO_'}; d=Graph(); d.parse('draft/dfo-salmon-draft.ttl', format='turtle'); s=Graph(); s.parse('release/tmp/dfoc-core.raw.ttl', format='turtle'); pub=URIRef(PUB); ont=URIRef(ONT); [s.remove(t) for t in list(s.triples((None,pub,None)))]; out=Graph(); [out.bind(p,n) for p,n in d.namespaces()]; [out.bind(p, URIRef(u)) for p,u in EXTRA_PREFIXES.items()]; out+=s; [out.remove(t) for t in list(out.triples((ont,None,None)))]; [out.add(t) for t in d.triples((ont,None,None)) if t[1]!=pub]; [out.add(t) for t in d.triples((None,RDF.type,OWL.AnnotationProperty))]; [out.add(t) for t in d.triples((None,RDF.type,RDFS.Datatype))]; [out.add(t) for t in d.triples((ont,OWL.imports,None))]; out.serialize('release/tmp/dfoc-core.ttl', format='turtle')" ; \
			rm -f release/tmp/dfoc-core.raw.ttl; \
			echo "✅ Publish slice generated at release/tmp/dfoc-core.ttl (publicationStatus stripped, header restored)"; \
		else \
			echo "⚠️  Publish slice extraction failed; writing empty publish slice."; \
			echo "# Empty publish slice (extraction failed)" > release/tmp/dfoc-core.ttl; \
		fi; \
	fi
	@if [ -s release/tmp/dfoc-core.ttl ] && ! grep -q "Empty publish slice" release/tmp/dfoc-core.ttl; then \
		cp release/tmp/dfoc-core.ttl ontology/dfo-salmon.ttl.tmp && mv ontology/dfo-salmon.ttl.tmp ontology/dfo-salmon.ttl; \
		echo "✅ Synced publish slice to ontology/dfo-salmon.ttl (master copy)"; \
		$(MAKE) reason; \
		./scripts/robot-quality-check.sh; \
	else \
		echo "ℹ️ Publish slice empty; leaving ontology/dfo-salmon.ttl unchanged."; \
	fi

# Publish, then extract term tables (skips extraction if slice is empty)
publish-and-extract: publish-slice
	@if [ -s release/tmp/dfoc-core.ttl ] && ! grep -q "Empty publish slice" release/tmp/dfoc-core.ttl; then \
		echo "▶️  Running term-table extraction against ontology/dfo-salmon.ttl"; \
		python scripts/extract-term-tables.py; \
	else \
		echo "ℹ️ Publish slice empty; skipping extraction."; \
	fi

# Remove publish temp artifacts
publish-clean:
	@echo "🧹 Cleaning publish temp artifacts..."
	@rm -f release/tmp/publish-ready-terms.tsv release/tmp/publish-ready-terms.txt release/tmp/publish-ready-metadata.tsv release/tmp/dfoc-core.raw.ttl release/tmp/dfoc-core.ttl
	@echo "✅ Temp artifacts removed from release/tmp/"

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
