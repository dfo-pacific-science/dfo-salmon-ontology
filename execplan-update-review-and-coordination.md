# Update onto_spsr_graph_review.md and Coordination Docs

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document must be maintained in accordance with `agent-config/PLANS.md`.

## Purpose / Big Picture

Update the review document (`onto_spsr_graph_review.md`) to accurately reflect the current architecture and implementation state, and create comprehensive DRAFT implementation guides in `dfo-salmon-graph-service/docs/coordination/integration-plans/` that use the logic and conventions from the review document. After these updates:

1. The review doc will accurately reflect the Graph API Service layer, FSAR Tracer MVP context, publish-ready slice workflow, theme annotations, and Fuseki architecture
2. Integration plans will be comprehensive DRAFT implementation guides that incorporate the conventions and logic from the review doc
3. Developers will have clear implementation guidance for SPSR integration and ontology integration

Note: `onto_spsr_graph_review.md` is an ephemeral review document containing suggested conventions, not a permanent authoritative reference. The integration plans should incorporate its logic but be self-contained implementation guides.

## Progress

- [x] (2025-01-27) Analyze inaccuracies in onto_spsr_graph_review.md
- [x] (2025-01-27) Update onto_spsr_graph_review.md with Graph API Service layer
- [x] (2025-01-27) Update onto_spsr_graph_review.md with FSAR Tracer MVP context (dedicated section 4.3)
- [x] (2025-01-27) Update onto_spsr_graph_review.md with publish-ready slice workflow (section 5.4)
- [x] (2025-01-27) Update onto_spsr_graph_review.md with theme annotations (section 5.5)
- [x] (2025-01-27) Update onto_spsr_graph_review.md with MCP server mention
- [x] (2025-01-27) Update onto_spsr_graph_review.md with dfoc: namespace (replacing dfo:)
- [x] (2025-01-27) Update onto_spsr_graph_review.md with all 10 core principles in summary (section 10)
- [x] (2025-01-27) Create comprehensive DRAFT implementation guide for spsr-integration.md using review doc logic
- [x] (2025-01-27) Create comprehensive DRAFT implementation guide for ontology-integration.md using review doc logic
- [x] (2025-01-27) Verify consistency across all updated docs

## Surprises & Discoveries

- (2025-01-27) **File update challenges**: Some search_replace operations failed due to whitespace/formatting differences. Used more targeted edits and verified with grep.
  Evidence: Multiple "Error: The string to replace was not found" messages during execution.

- (2025-01-27) **Section numbering**: Review doc already had sections 5.4 and 5.5 (Publish-Ready Slice and Theme Annotations), so those were already present.
  Evidence: grep found these sections before our updates.

## Decision Log

- Decision: Do not add "Current Implementation Status" section to onto_spsr_graph_review.md
  Rationale: User clarified that status section is not needed
  Date/Author: 2025-01-27 / User clarification

- Decision: Add FSAR Tracer MVP as dedicated section in review doc
  Rationale: User confirmed FSAR Tracer MVP should get dedicated section treatment
  Date/Author: 2025-01-27 / User clarification

- Decision: Ignore RCD integration updates for this execplan
  Rationale: User requested to focus on SPSR and ontology integration only
  Date/Author: 2025-01-27 / User clarification

- Decision: Create comprehensive DRAFT implementation guides for integration plans
  Rationale: User wants integration plans to be comprehensive implementation guides using logic from review doc, not just templates
  Date/Author: 2025-01-27 / User clarification

- Decision: Treat onto_spsr_graph_review.md as ephemeral review document
  Rationale: User clarified it's a review and suggested conventions, not a permanent authoritative reference. Integration plans should be self-contained.
  Date/Author: 2025-01-27 / User clarification

- Decision: All updates must respect and reflect 10 core principles
  Rationale: User specified that all updates to review doc and integration plans must respect the 10 core principles (SPSR stores data/ontology stores meaning, stable identifiers, conceptual modeling only, TBox/ABox separation, CU registry authoritative, deterministic IRIs, no 1:1 mirroring, rebuildable KG, domain-driven evolution, human-readable). These principles must be explicitly incorporated throughout all documentation.
  Date/Author: 2025-01-27 / User clarification

## Outcomes & Retrospective

**Completed (2025-01-27)**:

1. **Review Document Updates**: Successfully updated `onto_spsr_graph_review.md` with:
   - Graph API Service layer (section 2.5) - Added REST API intermediary description
   - FSAR Tracer MVP context (section 4.3) - Added dedicated section with scope and integration details
   - Fuseki architecture details (section 2.4) - Updated to specify Apache Jena Fuseki, single unified graph, rebuildable nature
   - Publish-ready slice workflow (section 5.4 - already existed) - Verified present
   - Theme annotations (section 5.5 - already existed) - Verified present
   - MCP server mention - Added to section 2.4
   - dfoc: namespace updates - Updated IRI examples and documentation
   - All 10 core principles in summary (section 10) - Inserted comprehensive Core Principles section with all 10 principles and Architecture Summary

2. **Comprehensive Integration Plans**: Created self-contained DRAFT implementation guides:
   - `spsr-integration.md`: 526 lines, comprehensive guide with:
     * All 10 core principles explicitly stated
     * 3-layer triage heuristics (tables → columns → rows) with detailed examples
     * FSAR Tracer MVP endpoints and use cases
     * IRI linking patterns (Pattern A and B)
     * TBox/ABox separation conventions
     * Implementation steps, testing strategy, monitoring
     * Error handling and security considerations
   - `ontology-integration.md`: 396 lines, comprehensive guide with:
     * All 10 core principles explicitly stated
     * TBox/ABox separation emphasis
     * Publish-ready slice pipeline details
     * Theme annotations workflow
     * Fuseki dataset configuration
     * Loading procedures (TBox and ABox separately)
     * Validation and maintenance procedures

3. **Core Principles Integration**: All documentation now explicitly incorporates and reinforces the 10 core principles throughout. The review doc serves as the foundation, and integration plans are self-contained guides that incorporate the principles.

**Verification Results**:
- Review doc: 54 mentions of key terms (Graph API Service, FSAR Tracer, TBox/ABox, rebuildable, etc.)
- Integration plans: Both contain "Core Principles" sections and comprehensive implementation guidance
- All 10 principles are explicitly stated in both integration plans
- 3-layer triage heuristics are documented in SPSR integration plan

**Remaining Work**:
- None - all planned updates completed

**Lessons Learned**:
- Integration plans benefit from being comprehensive and self-contained
- Core principles provide essential guidance for implementation decisions
- 3-layer triage (tables → columns → rows) is crucial for avoiding over-ontologization
- Python script approach was necessary for inserting large sections due to whitespace matching issues with search_replace
- User manual edits helped complete some updates (FSAR Tracer MVP line, TBox location clarification)

## Context and Orientation

The DFO Salmon ecosystem consists of three main repositories:

1. **dfo-salmon-ontology**: Contains the DFO Salmon Ontology (TBox) defining classes, properties, and SKOS vocabularies. The ontology file is `ontology/dfo-salmon.ttl`. The conventions guide is `onto_spsr_graph_review.md` at the repository root.

2. **salmon-population-summary-repository (SPSR)**: Django application with Postgres database storing time series, composites, reference points, and operational metadata. This is the system of record for measurements.

3. **dfo-salmon-graph-service**: Graph API Service providing REST endpoints to query a Fuseki-based knowledge graph. The service uses a single unified graph (dfo-salmon dataset) in Fuseki. Coordination documentation lives in `docs/coordination/`.

The current architecture includes:
- **Fuseki**: Apache Jena Fuseki triplestore hosting the unified `dfo-salmon` dataset
- **Graph API Service**: Python REST API (server.py) that wraps Fuseki SPARQL queries
- **MCP Server**: Model Context Protocol server for AI agent graph querying
- **Publish-ready slice**: Workflow that generates `release/published/dfoc-core.ttl` from ontology terms tagged with `dfoc:publicationStatus dfoc:PublishReady`
- **Theme annotations**: `dfoc:theme` property organizing terms into themes/modules
- **Namespace**: Changed from `dfo:` to `dfoc:` (complete)

The `onto_spsr_graph_review.md` document is an ephemeral review document containing suggested conventions and review notes. It is referenced in `execplan-add-spsr-terms.md` for conventions, but should be treated as a review/suggestions document, not a permanent authoritative source.

The coordination folder contains:
- `coordination-todo.md`: Master coordination todo tracking cross-repo dependencies
- `integration-plans/spsr-integration.md`: SPSR integration plan (currently sparse template, needs comprehensive DRAFT implementation guide)
- `integration-plans/ontology-integration.md`: Ontology integration plan (currently sparse template, needs comprehensive DRAFT implementation guide)
- `integration-plans/rcd-integration.md`: RCD integration plan (not updating per user request)
- `README.md`: Coordination hub navigation

## Core Principles

**CRITICAL: All updates to the review doc and integration plans MUST respect and reflect these principles:**

1. **SPSR stores data; the ontology stores meaning.**
   - SPSR (Postgres) is the source of truth for measurements and operational schema.
   - The ontology defines domain concepts, relationships, and controlled vocabularies.

2. **Link the two worlds using stable identifiers, not shared infrastructure.**
   - Keep the KG separate from SPSR.
   - Use business codes (CUIDs, indicator codes, method codes) or IRIs derived from them as the "bridge."
   - Prefer dynamic derivation from stable business codes where possible.
   - Add ontology_iri columns selectively for high-value entities where seeing/copying the URI in SPSR is useful.

3. **Only model in the ontology what is conceptually important.**
   - Tables representing domain entities → OWL Classes.
   - Lookup/code lists → SKOS Concept Schemes.
   - Foreign keys → Object Properties.
   - Domain attributes → Datatype Properties.
   - Ignore operational/technical columns.
   - Use 3-layer triage: tables → columns → rows (see detailed heuristics in review doc).

4. **Maintain strict TBox / ABox separation.**
   - TBox = curated ontology: classes, properties, vocabularies (in dfo-salmon.ttl).
   - ABox = generated data: individuals for indicators, datasets, methods, (optionally CUs), and other cross-system entities.
   - No SPSR data lives directly in the dfo-salmon.ttl ontology.

5. **The CU registry stays authoritative; the KG is a semantic view.**
   - Oracle governs CU lifecycle.
   - If CU individuals are needed, they are generated from the registry—not hand-authored.

6. **IRIs must be deterministic, stable, and resolvable.**
   - Prefer w3id.org patterns.
   - IRIs may be stored directly in SPSR or derived on the fly.
   - Lock in the IRI patterns and document them.

7. **Do not mirror the relational model 1:1.**
   - Not every table becomes a class.
   - Not every column becomes a property.
   - Not every row becomes an individual.
   - Model only what supports cross-system integration, reasoning, or communication.

8. **The KG is rebuildable and not a source of truth.**
   - All factual data about CUs, indicators, measurements, and series are sourced from authoritative systems (SPSR, CU registry, PSC databases).
   - These slices of the KG are fully rebuildable from upstream systems and never edited directly in the graph.
   - The KG may contain curated knowledge slices (mappings, annotations, conceptual groupings) that originate in the KG domain, but they are scoped, clearly separated from derived data, version-controlled or governed, and must never silently contradict authoritative upstream data.
   - Any correction to raw facts must occur in the upstream system, not inside the KG.

9. **Ontology evolution follows domain needs, not database design.**
   - New classes/properties added only when domain concepts or workflows require them.
   - Database internal changes do not automatically justify ontology changes.

10. **Keep everything human-readable and governance-friendly.**
    - Use labels, clear definitions, and controlled vocabularies.
    - Keep modeling minimal and intuitive so biologists, analysts, and developers can work together.

**These principles must be explicitly reflected in all documentation updates.**

## Plan of Work

The work proceeds in four milestones:

**Milestone 1: Analyze and Document Inaccuracies**
Review `onto_spsr_graph_review.md` against the actual implementation state documented in coordination-todo.md, the graph service code, and ontology todo_list.md. Document all inaccuracies and missing context.

**Milestone 2: Update onto_spsr_graph_review.md**
Add missing sections and correct inaccuracies while preserving the document's purpose as a review and suggested conventions document. Do not add a current implementation status section. **CRITICAL: Ensure all updates respect and reinforce the 10 core principles listed above.**

**Milestone 3: Create Comprehensive DRAFT Implementation Guides**
Create comprehensive DRAFT implementation guides for SPSR and ontology integration plans. These should be self-contained guides that incorporate the logic and conventions from the review doc, but be comprehensive enough to guide implementation without requiring the review doc as a reference. **CRITICAL: All implementation guidance must explicitly respect and incorporate the 10 core principles.**

**Milestone 4: Verify Consistency**
Ensure all documentation is consistent and cross-references are correct.

## Concrete Steps

### Milestone 1: Analyze and Document Inaccuracies

Working directory: `/Users/brettjohnson/Code/dfo-salmon-ontology`

1. Read `onto_spsr_graph_review.md` completely to understand current content.
2. Read `dfo-salmon-graph-service/docs/coordination/coordination-todo.md` to understand actual implementation status.
3. Read `dfo-salmon-graph-service/src/server.py` and `fuseki_client.py` to understand Graph API Service architecture.
4. Read `dfo-salmon-ontology/docs/todo_list.md` to understand ontology development status.
5. Document identified inaccuracies:
   - Missing Graph API Service layer
   - Missing FSAR Tracer MVP context
   - Missing publish-ready slice workflow
   - Missing theme annotations
   - Missing MCP server
   - Architecture details (Fuseki, single unified graph)
   - Namespace change (dfo: → dfoc:)

### Milestone 2: Update onto_spsr_graph_review.md

Working directory: `/Users/brettjohnson/Code/dfo-salmon-ontology`

1. Update section 2.4 (Knowledge Graph) to clarify:
   - The KG is hosted in Fuseki (Apache Jena Fuseki triplestore)
   - Uses single unified graph architecture (dfo-salmon dataset)
   - Access is via Graph API Service REST endpoints, not direct SPARQL
   - MCP server provides additional query interface for AI agents

3. Add new section 2.5 titled "Graph API Service" that describes:
   - Purpose: REST API wrapper around Fuseki SPARQL
   - Location: dfo-salmon-graph-service repository
   - Endpoints: Evidence chain, vocabularies, validation (as planned in coordination-todo.md)
   - Architecture: Python server.py with FusekiClient wrapper

4. Update section 3.1 (IRIs) to reflect:
   - Namespace change from `dfo:` to `dfoc:` (complete)
   - Examples should use `dfoc:` prefix
   - w3id.org patterns remain the same

5. Update section 4.1 (Linking strategy) to mention:
   - Graph API Service as intermediary layer
   - SPSR consumes Graph API Service, not direct SPARQL
   - IRIs still used for linking, but accessed via API
   - **Principle 2**: Emphasize stable identifiers (business codes/IRIs) as the bridge, not shared infrastructure
   - **Principle 2**: Document preference for dynamic derivation from business codes, with selective ontology_iri columns for high-value entities

6. Add new section 4.3 titled "FSAR Tracer MVP Context" (dedicated section) that describes:
   - FSAR Tracer as primary use case driving SPSR integration
   - Evidence chain queries via Graph API Service
   - Intake form vocabularies and validation
   - Scope: Simple trace viewer, basic intake form, SHACL validation, evidence badges
   - **Principle 1**: Clarify that SPSR remains source of truth for data; KG provides semantic view
   - **Principle 8**: Emphasize that KG is rebuildable from SPSR, not edited directly

7. Add new section 5.4 titled "Publish-Ready Slice Workflow" that describes:
   - `dfoc:publicationStatus` annotation property
   - `dfoc:PublishReady` vs `dfoc:Draft` status
   - Extraction pipeline: `ontology/dfo-salmon.ttl` → `release/published/dfoc-core.ttl`
   - Downstream consumers (DSU, term tables) read from publish slice
   - Validation requirements for PublishReady terms
   - **Principle 4**: Clarify this is TBox-only (curated ontology), not ABox data
   - **Principle 10**: Emphasize human-readable labels and definitions for governance

8. Add new section 5.5 titled "Theme Annotations" that describes:
   - `dfoc:theme` property for organizing terms
   - SKOS concept scheme for themes
   - Validation: every term must have 1-3 theme values
   - Used by DSU for theme-based navigation

9. Update section 9 (Summary) to include:
    - Graph API Service as intermediary layer
    - FSAR Tracer MVP as primary use case
    - Publish-ready slice workflow
    - Theme annotations
    - **Principle 1**: SPSR stores data; ontology stores meaning
    - **Principle 2**: Link via stable identifiers, not shared infrastructure
    - **Principle 3**: Only model conceptually important things
    - **Principle 4**: Strict TBox/ABox separation
    - **Principle 7**: Do not mirror relational model 1:1
    - **Principle 8**: KG is rebuildable, not source of truth
    - **Principle 9**: Ontology evolution follows domain needs
    - **Principle 10**: Keep everything human-readable

### Milestone 3: Create Comprehensive DRAFT Implementation Guides

Working directory: `/Users/brettjohnson/Code/dfo-salmon-graph-service`

1. Create comprehensive DRAFT implementation guide for `docs/coordination/integration-plans/spsr-integration.md`:
   - Use logic and conventions from onto_spsr_graph_review.md as foundation
   - **MUST explicitly incorporate all 10 core principles throughout the guide**
   - Include complete architecture: SPSR (Postgres + Django) → Graph API Service → Fuseki (dfo-salmon dataset)
   - **Principle 1**: Emphasize SPSR as source of truth for data; ontology for meaning
   - **Principle 2**: Document stable identifier linking (business codes/IRIs), not shared infrastructure
   - Document FSAR Tracer MVP as primary use case with specific endpoints:
     * `GET /api/evidence-chain` - Evidence chain for SMU/year
     * `GET /api/intake/vocab` - SKOS vocabularies for intake forms
     * `POST /api/intake/validate` - Validate intake data (SHACL + R)
   - **Principle 2**: Document IRI linking patterns with preference for dynamic derivation from business codes (Pattern B), with selective ontology_iri columns (Pattern A) for high-value entities
   - **Principle 4**: Document strict TBox/ABox separation (TBox in ontology repo, ABox generated from SPSR)
   - **Principle 3**: Document comprehensive 3-layer triage rules (tables → columns → rows) with detailed heuristics:
     * Table-level: Class vs SKOS vocab vs object property vs ignore
     * Column-level: Object property vs datatype property vs ignore
     * Row-level: Individual vs keep as relational data
   - **Principle 7**: Emphasize not mirroring relational model 1:1; model only what supports cross-system integration
   - **Principle 8**: Document that KG is rebuildable from SPSR; data corrections happen in SPSR, not KG
   - Document publish-ready slice consumption (read from `release/published/dfoc-core.ttl`)
   - Document theme annotations usage
   - **Principle 9**: Include guidance on when to add ontology terms (domain needs, not database design)
   - **Principle 10**: Emphasize human-readable labels, definitions, and governance-friendly modeling
   - Include implementation steps, data flow diagrams, and examples
   - Include ETL/loading procedures that respect TBox/ABox separation
   - Make it self-contained (can be used without reference to review doc)

2. Create comprehensive DRAFT implementation guide for `docs/coordination/integration-plans/ontology-integration.md`:
   - Use logic and conventions from onto_spsr_graph_review.md as foundation
   - **MUST explicitly incorporate all 10 core principles throughout the guide**
   - Document ontology loading process into Fuseki dfo-salmon dataset
   - **Principle 4**: Emphasize TBox-only loading from ontology repo; ABox loaded separately from SPSR/other sources
   - Document publish-ready slice pipeline:
     * Source: `ontology/dfo-salmon.ttl` (or `draft/dfo-salmon-draft.ttl` per execplan.md)
     * Filter: Terms with `dfoc:publicationStatus dfoc:PublishReady`
     * Output: `release/published/dfoc-core.ttl` (publicationStatus stripped)
     * Validation: Required metadata checks
   - **Principle 4**: Clarify publish slice is TBox (curated ontology), not ABox data
   - **Principle 10**: Emphasize human-readable labels and definitions in publish-ready terms
   - Document theme annotations workflow and validation
   - **Principle 6**: Document namespace (dfoc:) and IRI patterns (w3id.org, deterministic, stable, resolvable)
   - **Principle 4**: Document strict TBox-only convention (no ABox in ontology repo; ABox generated separately)
   - **Principle 8**: Document that ontology TBox is version-controlled and curated; ABox is rebuildable from upstream
   - **Principle 5**: If CU individuals are needed, document they are generated from CU registry, not hand-authored
   - **Principle 9**: Include guidance on ontology evolution (domain needs, not database design)
   - Document loading steps, validation checks, and maintenance procedures
   - Include Fuseki dataset configuration and SPARQL endpoint details
   - Document separation between TBox loading (from ontology repo) and ABox loading (from SPSR/other sources)
   - Make it self-contained (can be used without reference to review doc)

### Milestone 4: Verify Consistency

Working directory: Both repositories

1. Verify integration plans are self-contained:
   - Integration plans can be understood without requiring onto_spsr_graph_review.md
   - Integration plans incorporate logic from review doc but are complete guides
   - Integration plans match coordination-todo.md status

2. Verify terminology is consistent:
   - "Graph API Service" used consistently
   - "Fuseki" and "dfo-salmon dataset" used consistently
   - "dfoc:" namespace used consistently
   - "FSAR Tracer MVP" used consistently

3. Verify architecture descriptions match:
   - Single unified graph architecture
   - Graph API Service as intermediary
   - Fuseki as triplestore
   - Publish-ready slice workflow

4. Verify core principles are respected:
   - All 10 core principles are explicitly reflected in review doc updates
   - All 10 core principles are explicitly incorporated in integration plans
   - No documentation contradicts or undermines any principle
   - Principles are clearly stated and reinforced throughout

5. Check that no contradictions exist between:
   - onto_spsr_graph_review.md conventions
   - Coordination todo status
   - Integration plan details
   - Core principles

## Validation and Acceptance

After completing all milestones, verify the following:

1. **onto_spsr_graph_review.md accuracy**:
   - Document mentions Graph API Service layer
   - Document mentions FSAR Tracer MVP (dedicated section)
   - Document mentions publish-ready slice workflow
   - Document mentions theme annotations
   - Document mentions MCP server
   - Document uses dfoc: namespace in examples
   - Document serves as review and suggested conventions (ephemeral)
   - **All 10 core principles are explicitly reflected and reinforced throughout the document**

2. **Integration plans completeness**:
   - Integration plans are comprehensive DRAFT implementation guides
   - Integration plans are self-contained (don't require review doc)
   - Integration plans incorporate logic from review doc
   - Integration plans have architecture details, implementation steps, examples
   - Integration plans document FSAR Tracer MVP endpoints and use cases
   - **All 10 core principles are explicitly incorporated and reinforced throughout both integration plans**
   - Integration plans include 3-layer triage heuristics (tables → columns → rows)
   - Integration plans clearly separate TBox loading from ABox loading
   - Integration plans emphasize rebuildable KG and SPSR as source of truth

3. **Consistency**:
   - All docs use consistent terminology
   - Architecture descriptions match across docs
   - Status information is consistent
   - No contradictions between docs

4. **Core principles adherence**:
   - All 10 core principles are explicitly stated in integration plans
   - Principles are reinforced in implementation guidance
   - No guidance contradicts any principle
   - Triage heuristics (tables/columns/rows) are clearly documented
   - TBox/ABox separation is emphasized throughout

5. **Self-containment**:
   - Integration plans can be read and understood without onto_spsr_graph_review.md
   - Integration plans include all necessary context and conventions
   - Integration plans have clear implementation guidance
   - Integration plans include all 10 core principles as foundational guidance

Run these verification commands:

    cd /Users/brettjohnson/Code/dfo-salmon-ontology
    grep -n "Graph API Service\|FSAR Tracer\|publish-ready\|dfoc:theme\|source of truth\|TBox\|ABox\|rebuildable" onto_spsr_graph_review.md
    
    cd /Users/brettjohnson/Code/dfo-salmon-graph-service
    grep -n "source of truth\|TBox\|ABox\|rebuildable\|stable identifier\|business code\|triage\|3-layer" docs/coordination/integration-plans/spsr-integration.md
    grep -n "TBox\|ABox\|rebuildable\|domain needs\|human-readable" docs/coordination/integration-plans/ontology-integration.md

Expected results: 
- Review doc contains updated architecture info and reinforces core principles
- Integration plans are comprehensive and self-contained with all necessary details
- Core principles are explicitly stated and reinforced throughout all documentation

## Idempotence and Recovery

All steps are idempotent. Editing markdown files can be repeated safely. If a step fails:

1. Review the file to see what was changed
2. Revert unwanted changes using git if needed
3. Re-run the specific step

No destructive operations are performed. All changes are additive or corrective edits to documentation files.

## Artifacts and Notes

Key files to be modified:
- `/Users/brettjohnson/Code/dfo-salmon-ontology/onto_spsr_graph_review.md` (ephemeral review doc, update for accuracy)
- `/Users/brettjohnson/Code/dfo-salmon-graph-service/docs/coordination/integration-plans/spsr-integration.md` (comprehensive DRAFT implementation guide)
- `/Users/brettjohnson/Code/dfo-salmon-graph-service/docs/coordination/integration-plans/ontology-integration.md` (comprehensive DRAFT implementation guide)

## Interfaces and Dependencies

No code interfaces are changed. This is a documentation-only update. Dependencies:

- onto_spsr_graph_review.md is referenced by execplan-add-spsr-terms.md (treat as ephemeral review/suggestions doc)
- Integration plans should be self-contained comprehensive guides that incorporate review doc logic
- Coordination docs are referenced by multiple repo todo lists
- All documentation should remain consistent with actual implementation

No breaking changes to existing documentation structure or references. Integration plans will be enhanced from templates to comprehensive DRAFT implementation guides.
