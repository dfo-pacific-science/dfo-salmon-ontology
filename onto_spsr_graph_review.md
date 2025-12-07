Here’s a conventions guide you can hand to colleagues (and future you) to keep SPSR + the DFO Salmon Ontology + a standalone knowledge graph sane.

---

# 1. Overall intent

We are **not** turning SPSR into a graph database.

We are:

* Keeping **SPSR (Postgres + Django)** as the **system of record for measurements and operational data**.
* Using the **DFO Salmon Ontology** as the **conceptual schema and vocab layer** (TBox).
* Optionally building a **standalone knowledge graph (KG)** as a **derived semantic view** over SPSR, the CU registry (Oracle), and other systems (ABox).

The KG is **decoupled**: SPSR can run without it; the KG can serve other apps besides SPSR.

---

# 2. Roles of each system

### 2.1 SPSR (Postgres + Django)

* Stores:

  * Time series, composites, reference points, etc.
  * Operational metadata needed for apps and pipelines.
* Truth for:

  * “What numbers do we have, for which CU, indicator, method, and years?”
* Identifiers:

  * Internal PKs.
  * Possibly business-level codes (series codes, indicator codes, etc.).

### 2.2 CU registry (Oracle)

* Stores:

  * Authoritative list of Conservation Units and their codes (CUIDs).
* Truth for:

  * “Which CUs exist?”
  * “What’s their current status / structure?”

### 2.3 DFO Salmon Ontology (TBox only)

* Defines:

  * Classes (e.g. `ConservationUnit`, `Indicator`, `CompositeEscapementIndicator`, `SurveyEvent`).
  * Object properties (relationships between those classes).
  * Datatype properties (domain attributes).
  * SKOS vocabularies and concept schemes (run timing categories, life-stage codes, indicators, etc.).
* Truth for:

  * “What concepts exist, and how do they relate?”
  * “What does this column / category *mean*?”

### 2.4 Knowledge Graph (ABox + TBox)

* Hosted in **Apache Jena Fuseki** triplestore using a **single unified graph architecture** (dfo-salmon dataset).
* Loads:

  * The ontology TBox.
  * Data graphs (ABox) derived from SPSR, CU registry, and other systems.
* Truth for:

  * “What do we know about this specific CU/indicator/dataset in a graph form?”
  * Cross-system reasoning and semantic search.
* Access:

  * **Graph API Service** provides REST endpoints (not direct SPARQL access from SPSR).
  * MCP (Model Context Protocol) server provides additional query interface for AI agents.
  * The KG is **rebuildable** from authoritative sources (SPSR, CU registry); it is not a source of truth itself.

**Hard rule:**
Ontology dev maintains a strict **TBox/ABox separation**:

* TBox lives in curated ontology files (versioned, reviewed) in the ontology repo.
* ABox is generated from databases/pipelines and *not* hand-edited in the ontology repo.
* No SPSR data lives directly in the dfo-salmon.ttl ontology file.

### 2.5 Graph API Service

* **Purpose**: REST API wrapper around Fuseki SPARQL queries, providing a clean interface for applications to access the knowledge graph.
* **Location**: dfo-salmon-graph-service repository.
* **Architecture**: Python-based service (server.py) with FusekiClient wrapper connecting to Fuseki dfo-salmon dataset.
* **Endpoints** (planned for FSAR Tracer MVP):

  * `GET /api/evidence-chain` - Evidence chain queries for SMU/year
  * `GET /api/intake/vocab` - SKOS vocabularies for intake forms
  * `POST /api/intake/validate` - Validate intake data (SHACL + R)
* **Role**: Intermediary layer between SPSR and the knowledge graph, ensuring separation of concerns and stable API contracts.

---

# 3. Identifier & IRI conventions

### 3.1 IRIs

* All IRIs are **HTTP(S)**, **deterministic**, **stable**, and **resolvable**.
* Prefer `w3id.org` for public-facing IRIs.

**TBox (Ontology Terms) - Classes, Properties, SKOS Concepts:**
* **Base IRI**: `https://w3id.org/dfoc/salmon#`
* **Class IRIs**: `https://w3id.org/dfoc/salmon#ClassName` (e.g., `https://w3id.org/dfoc/salmon#ConservationUnit`)
* **Property IRIs**: `https://w3id.org/dfoc/salmon#propertyName` (e.g., `https://w3id.org/dfoc/salmon#aboutStock`)
* **SKOS Concept IRIs**: `https://w3id.org/dfoc/salmon#ConceptName` (e.g., `https://w3id.org/dfoc/salmon#SonarCounting`)
* **Namespace prefix**: Uses `dfoc:` prefix (changed from `dfo:` to avoid conflicts).

**ABox (Instance Data) - Individuals:**
* Instance IRIs may use path-based patterns for readability:
  * CU instances: `https://w3id.org/dfo-salmon/cu/{cuid}` (e.g., `https://w3id.org/dfo-salmon/cu/ECV-01`)
  * Indicator instances: `https://w3id.org/dfo-salmon/indicator/{indicator_code}` (e.g., `https://w3id.org/dfo-salmon/indicator/CompositeEscapement`)
* These are ABox individuals, not TBox terms, so they may follow different IRI patterns for operational convenience.

* IRI patterns must be **locked in and documented** to ensure consistency across systems.

### 3.2 Mapping from DB IDs to IRIs

We use **business-level codes** where they exist and are governed:

* CUIDs, indicator codes, method codes, series codes, etc.
* IRI pattern is deterministic:

  * CU: `https://w3id.org/dfo-salmon/cu/{cuid}`
  * Indicator: `https://w3id.org/dfo-salmon/indicator/{indicator_code}`

We do **not** move governance into the ontology:

* CU lifecycle remains in Oracle.
* IRIs are a semantic “view” over those governed identifiers.

Whether we *store* IRIs in Postgres is a separate design choice (see below).

---

# 4. Linking SPSR and the ontology/KG

### 4.1 Linking strategy (high-level)

We link SPSR and the KG via **stable identifiers / IRIs**, not by embedding the KG engine inside SPSR or sharing infrastructure.

**Core principle**: Link the two worlds using stable identifiers, not shared infrastructure. Keep the KG separate from SPSR.

* SPSR knows:

  * Its internal IDs.
  * Business codes (e.g. CUID, indicator code, method code).
  * Optionally: the IRI string (text column) for high-value entities.
* KG knows:

  * IRIs and their semantics.
  * How each IRI maps back to a CU/indicator/method/dataset row.
* **Graph API Service** acts as the intermediary layer:

  * SPSR consumes Graph API Service REST endpoints, not direct SPARQL.
  * IRIs are still used for linking, but accessed via the API.
  * This maintains separation: SPSR stores data; KG provides semantic view.

### 4.2 Two main patterns for linking

#### Pattern A — **IRI columns in key dimension tables**

* Add `ontology_iri` text columns to “dimension-like” tables:

  * `cu(ontology_iri)`
  * `indicator(ontology_iri)`
  * `method(ontology_iri)`
  * Possibly `dataset(ontology_iri)`

* Use them as “semantic foreign keys” to the KG.

* Pros: explicit, flexible, easy to query.

* Cons: adds ontology awareness to SPSR schema.

#### Pattern B — **Derive IRIs from existing codes (preferred early)**

* SPSR stores only business codes:

  * `cu.cuid`, `indicator.code`, `method.code`.
* A mapping layer (ETL, API, or KG loader) constructs the IRIs based on a stable, deterministic pattern.
* **Preference**: Use dynamic derivation from stable business codes where possible.
* Pros: SPSR schema stays clean; easy to retrofit later.
* Cons: IRIs aren’t visible in SPSR until/unless you decide to expose them.

**Recommendation**: Start with Pattern B and only add Pattern A (ontology_iri columns) selectively for high-value entities where seeing/copying the URI in SPSR is useful.

### 4.3 FSAR Tracer MVP Context

The **FSAR Tracer MVP** is the primary use case driving SPSR integration with the knowledge graph.

**Purpose**: Enable FSAR authors to trace evidence chains from data through methods, reference points, and status assessments to advice.

**Scope** (MVP):
* Simple trace viewer (linear chain, not complex graph visualization)
* Basic intake form (SMU/year + file upload)
* SHACL validation integration
* Evidence badges (Complete/Gaps/Missing-Critical)
* Basic evidence drawer (single tab)
* Basic export (JSON-LD)

**Integration via Graph API Service**:
* Evidence chain queries: `GET /api/evidence-chain` retrieves semantic evidence chains for SMU/year combinations
* Intake form vocabularies: `GET /api/intake/vocab` provides SKOS vocabularies for form dropdowns
* Intake validation: `POST /api/intake/validate` validates intake data using SHACL + R validation

**Core principles in action**:
* **SPSR stores data; ontology stores meaning**: SPSR remains source of truth for measurements; KG provides semantic relationships and vocabularies
* **KG is rebuildable**: Evidence chains are derived from SPSR data via ETL; corrections happen in SPSR, not KG
* **Stable identifiers**: Evidence chains use IRIs derived from business codes (CUIDs, indicator codes) to link SPSR data to semantic concepts

---

# 5. TBox modeling conventions (what goes into the ontology schema)

We do **not** mirror every table/column. We focus on domain semantics.

### 5.1 Tables → classes or vocabularies

* Entity tables → OWL classes:

  * `conservation_unit` → `:ConservationUnit`
  * `indicator` → `:Indicator`
  * `dataset` → `:Dataset`
  * `method` → `:SamplingMethod` or more specific subclasses.
* Lookup/code tables → SKOS concept schemes or OWL classes with individuals:

  * `run_timing_code` → `:RunTimingScheme` (SKOS)
  * `life_stage_code` → `:LifeStageScheme` (SKOS)
  * `status_code` → `:StatusScheme` (SKOS)

### 5.2 Columns → properties (not classes)

For each column, classify and handle as:

1. **Foreign key columns**
   → **Object properties** between classes.

   * `time_series.cu_id` → `:timeSeriesForCU`
   * `time_series.indicator_id` → `:reportsIndicator`
   * `series.method_id` → `:usesMethod`

2. **Domain attributes (real semantic content)**
   → Mostly **datatype properties**; sometimes object properties to SKOS concepts.

   * Numeric / dates / free text:

     * `:hasEscapementValue`, `:hasObservationYear`, `:hasReferencePointValue`.
   * Controlled categories:

     * `run_timing_category` → `:hasRunTimingCategory` (object property to a SKOS concept).
     * `quality_flag` → `:hasDataQualityFlag`.

3. **Technical / operational columns**
   → **Not modeled in core domain ontology**.

   * `created_at`, `updated_at`, `etl_batch_id`, `is_deleted`, internal audit columns.
   * If needed, they belong in a separate provenance/ops ontology, not the core DFO Salmon Ontology.

4. **Legacy / one-off junk**
   → Ignored unless it becomes a real domain concept.

   * Temporary flags, obscure ETL traces, etc.

### 5.2.1 Naming Conventions

All ontology terms must follow consistent naming conventions:

* **OWL Classes**: Use **PascalCase** (e.g., `ConservationUnit`, `EscapementMeasurement`, `GeneticSample`)
* **OWL Properties** (Object and Datatype): Use **lowerCamelCase** (e.g., `aboutStock`, `usesMethod`, `hasMember`, `hasEscapementValue`)
* **SKOS Concepts**: Use **PascalCase** (e.g., `SonarCounting`, `MicrosatelliteAssay`, `EarlyRunTiming`)
* **Instances**: Use **PascalCase** with descriptive names (e.g., `SkeenaSockeye`, `FraserCoho`)

**Why consistent naming matters:** It makes the ontology easier to read, understand, and maintain. It also helps prevent confusion when multiple people are contributing and ensures tooling compatibility.

### 5.3 Join tables → relationships or event-like classes

* Join tables **without additional attributes** → direct object properties.
* Join tables **with attributes** (e.g., method, year ranges) → dedicated classes like `:IndicatorSeries`, `:CompositeSeries`, `:Observation`, etc.

### 5.4 Publish-Ready Slice Workflow

The ontology uses a **publish-ready slice workflow** to control which terms are published to w3id.org.

**Publication Status Annotation**:
* `dfoc:publicationStatus` - Annotation property indicating publication readiness
* `dfoc:PublishReady` - Individual indicating term is ready for publication
* `dfoc:Draft` - Individual indicating term is still in draft

**Workflow**:
1. Terms in `ontology/dfo-salmon.ttl` (or `draft/dfo-salmon-draft.ttl`) are tagged with `dfoc:publicationStatus`
2. Only terms with `dfoc:publicationStatus dfoc:PublishReady` are included in the publish slice
3. Extraction pipeline generates `release/published/dfoc-core.ttl`:
   * Source: `ontology/dfo-salmon.ttl` (or draft file)
   * Filter: Terms with `dfoc:publicationStatus dfoc:PublishReady`
   * Output: `release/published/dfoc-core.ttl` (publicationStatus annotation stripped)
4. Downstream consumers (DSU theme tabs, term tables) read from the publish slice

**Required Annotations for All Terms** (not just PublishReady):

* **OWL Classes and Properties** (required):
  * `rdfs:label` - Human-readable name (required, one per language)
  * `IAO:0000115` - Definition (required, one only)
  * `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Source attribution (required)
  * Optional but recommended: `IAO:0000119` (definition source citation), `IAO:0000112` (examples), `dcterms:source` (resolvable link)

* **SKOS Concepts** (required):
  * `skos:prefLabel` - Human-readable name (required, ≤1 per language)
  * `skos:inScheme` - Concept scheme membership (required)
  * `skos:definition` - Definition (recommended, 1×)
  * `rdfs:isDefinedBy <https://w3id.org/dfoc/salmon>` - Source attribution (required)
  * Optional but recommended: `skos:altLabel`, `skos:broader`, `dcterms:source`, `IAO:0000119`

**Additional Validation Requirements for PublishReady Terms**:
* PublishReady terms must have all required annotations above PLUS:
  * Definition source (`IAO:0000119` or `dcterms:source`)
  * At least one `dfoc:theme` annotation

**Core principles**:
* **TBox-only**: Publish slice contains only curated ontology (TBox), not ABox data
* **Human-readable**: Published terms must have clear labels and definitions for governance

### 5.5 Theme Annotations

Terms in the ontology are organized using **theme annotations** for navigation and discovery.

**Theme Property**:
* `dfoc:theme` - Annotation property linking terms to themes/modules
* Range: SKOS concept scheme for themes
* Values: From controlled list (e.g., FSAR, Population Assessment, Genetics, Habitat)

**Validation**:
* Every term must have 1-3 `dfoc:theme` values
* Validation queries ensure coverage and prevent over-tagging

**Usage**:
* DSU (Data Stewardship Unit) uses themes for theme-based navigation tabs
* Term tables can be filtered by theme
* Helps organize ontology for different audiences (biologists, analysts, developers)

**Core principles**:
* **Human-readable**: Themes make the ontology more navigable and governance-friendly
* **TBox-only**: Theme annotations are part of the curated ontology, not ABox data

---

# 6. ABox / knowledge graph conventions (what becomes instances)

We maintain **strict TBox/ABox separation**:

* **Ontology repo (TBox):**

  * Classes, properties, SKOS schemes.
  * No SPSR data, no CU instances, no time-series rows.

* **Data graphs (ABox):**

  * Generated from SPSR, the CU registry, and other systems via ETL.
  * Stored in the KG store, separate from ontology files.

### 6.1 What *may* become individuals in the KG

We selectively create individuals where cross-system reasoning or reuse matters:

* **Indicators** (e.g. specific composite indicator definitions).
* **Datasets** / data products (e.g. SPSR as a dataset, CU-specific composites).
* **Methods** (survey methods, estimation methods).
* **Reference points** (if you need semantics around them).
* **Possibly CUs** (see below) if/when you want graph-level relationships at CU level.

We **do not** automatically materialize every time-series row as an individual unless there’s a strong use case.

### 6.2 CUs and the CU registry

We explicitly keep the **CU registry authoritative in Oracle**.

Two options for CUs in the KG:

* **Schema-only (no CU individuals)**:

  * Ontology defines `ConservationUnit` and properties like `hasCuid`, `hasRegion`, etc.
  * CUs remain rows in Oracle/SPSR only.
  * Good if you mainly use the ontology as a schema/column dictionary.

* **Virtual / generated individuals (recommended when needed)**:

  * CU individuals are **generated** from the CU registry.
  * IRI pattern: `https://w3id.org/dfo-salmon/cu/{cuid}` (ABox instance IRI, not TBox term).
  * Loaded into a data graph separate from the TBox.
  * Governance stays in Oracle; KG is a read-only semantic projection.

You can start with schema-only and add generated CU individuals later when you have concrete graph use cases.

---

# 7. Governance & change management

### 7.1 Sources of truth

* **Oracle CU registry**:

  * Truth for CU existence, codes, and governance.
* **SPSR (Postgres)**:

  * Truth for summary series and indicator values.
* **DFO Salmon Ontology repo**:

  * Truth for conceptual schema (classes/properties/vocabs).
* **Knowledge Graph store**:

  * Derived semantic integration layer.
  * Treat as *rebuildable* from SoT systems.

### 7.2 When to update the ontology

For any SPSR or CU-registry change, ask:

1. **Is this a new domain concept?**

   * New indicator type, new method category, new form of series, new kind of relationship.
   * **Yes** → Add/extend class, property, or SKOS scheme in the ontology (TBox).

2. **Is this a new individual of an existing concept that needs semantics across systems?**

   * New indicator defined by governance.
   * New official dataset or data product.
   * Possibly new CU, if you’re using CU individuals.
   * **Yes** → It’s ABox, handled via ETL into KG, *not* hand-edited ontology files.

3. **Is this purely implementation detail?**

   * New internal flag, index, ETL column, intermediate cache.
   * **Yes** → No ontology change.

### 7.3 TBox review rules

* Only add classes/properties that:

  * Are expected to be stable over time.
  * Capture concepts that matter outside a single database implementation.
* Favor:

  * Reuse of existing vocabularies (SKOS schemes, other ontologies) where sensible.
  * Simple, readable modeling over clever but opaque constructs.

---

# 8. The KG is not the master record for raw data

The KG is not the master record for raw data; it is a rebuildable semantic view with optional curated knowledge layers.

### 8.1 Authoritative sources for factual data

All factual data about CUs, indicators, measurements, and series are sourced from their authoritative systems (e.g., SPSR, CU registry, PSC databases).

These slices of the KG are fully rebuildable from upstream systems and never edited directly in the graph.

### 8.2 Curated knowledge layers

The KG may also contain curated knowledge slices (e.g., mappings, annotations, conceptual groupings) that do originate in the KG domain, but:

* They are **scoped**,
* **Clearly separated** from derived data,
* **Version-controlled or governed**,
* And must **never silently contradict** authoritative upstream data.

### 8.3 Correction workflow

Any correction to raw facts must occur in the upstream system, not inside the KG.

The KG reflects upstream truth + curated semantic enhancements, but does not override or replace upstream sources.

---

# 9. Triage rules for tables, columns, and values

Use this as a decision checklist.

### 9.1 Table-level triage

For each table:

1. Is this an **entity** we talk about in FSARs, governance, workflows, or reports?
   → Make/align an OWL **class** for it.

2. Is this a **lookup / code list** used by multiple systems or reports?
   → Make a **SKOS concept scheme** (or class + individuals) for its values.

3. Is this a **join / link** table?
   → Model as:

   * An **object property** (if no attributes), or
   * A new **class** (e.g., Observation/Series) if the link itself has important attributes.

4. Is this table purely internal / technical / ETL?
   → Don’t model it in the core ontology.

### 9.2 Column-level triage

For each column in a table:

**Compound SPSR column rule (decompose first):**
- SPSR columns often fuse multiple semantic dimensions (quantity type, stratum/location, temporal semantics, age semantics, origin/composition).
- Decompose each such column into a base measurement class (e.g., RunAbundance, Catch, MortalityRate, SpawnerAbundance) plus facet properties:
  - Stratum/location: PFMA, fishery type, run/mortality component type (SKOS)
  - Time basis: calendar vs brood vs season (SKOS)
  - Age basis + numeric age: total vs ocean vs freshwater age (SKOS + integer)
  - Origin/composition: hatchery vs natural vs mixed (SKOS)
- Do **not** mint a new class or property per compound column name. Represent facets with object properties to SKOS schemes and datatype properties for numeric values.
- Example: `TOTAL_OCEAN_RUN_AGE_3` → one `RunAbundance` datum + `runComponentType :OceanComponent` + `ageType :TotalAge` + numeric age 3 (+ PFMA/area/year context in data), not a new class or property.

1. **Foreign key to another entity table?**
   → Define an **object property** (e.g. `timeSeriesForCU`, `reportsIndicator`, `usesMethod`).

2. **Controlled, domain-specific categorical value?**
   → Map as **object property** pointing to **SKOS concepts**, and define/align the concept scheme.

3. **Numeric/text/date measurement that appears in stats or reports?**
   → Model as a **datatype property** on an appropriate class (e.g. `Observation`, `Series`, `ReferencePoint`).

4. **Purely local, technical, or one-off?**
   → Do not model. Keep it as a DB-only implementation detail.

### 9.3 Value-level triage (individual cells)

Most individual cell values **do not** become graph nodes.

Exceptions:

* Cells that *are* identifiers (CUIDs, series codes, DOIs, dataset IDs).
* Cells that represent a category from a controlled vocabulary (mapped via SKOS).
* Very occasionally, specific values that need to be referenced as entities (e.g. a particular dataset version, not just its number).

---

# 10. Summary: how to “keep it sane”

**Core Principles**:

1. **SPSR stores data; the ontology stores meaning.**
   * SPSR (Postgres) is the source of truth for measurements and operational schema.
   * The ontology defines domain concepts, relationships, and controlled vocabularies.

2. **Link the two worlds using stable identifiers, not shared infrastructure.**
   * Keep the KG separate from SPSR.
   * Use business codes (CUIDs, indicator codes, method codes) or IRIs derived from them as the "bridge."
   * Prefer dynamic derivation from stable business codes where possible.
   * Add ontology_iri columns selectively for high-value entities.

3. **Only model in the ontology what is conceptually important.**
   * Tables representing domain entities → OWL Classes.
   * Lookup/code lists → SKOS Concept Schemes.
   * Foreign keys → Object Properties.
   * Domain attributes → Datatype Properties.
   * Ignore operational/technical columns.
   * Use 3-layer triage: tables → columns → rows.

4. **Maintain strict TBox / ABox separation.**
   * TBox = curated ontology: classes, properties, vocabularies (in dfo-salmon.ttl).
   * ABox = generated data: individuals for indicators, datasets, methods, (optionally CUs), and other cross-system entities.
   * No SPSR data lives directly in the dfo-salmon.ttl ontology.

5. **The CU registry stays authoritative; the KG is a semantic view.**
   * Oracle governs CU lifecycle.
   * If CU individuals are needed, they are generated from the registry—not hand-authored.

6. **IRIs must be deterministic, stable, and resolvable.**
   * Prefer w3id.org patterns.
   * IRIs may be stored directly in SPSR or derived on the fly.
   * Lock in the IRI patterns and document them.

7. **Do not mirror the relational model 1:1.**
   * Not every table becomes a class.
   * Not every column becomes a property.
   * Not every row becomes an individual.
   * Model only what supports cross-system integration, reasoning, or communication.

8. **The KG is rebuildable and not a source of truth.**
   * All factual data about CUs, indicators, measurements, and series are sourced from authoritative systems (SPSR, CU registry, PSC databases).
   * These slices of the KG are fully rebuildable from upstream systems and never edited directly in the graph.
   * The KG may contain curated knowledge slices (mappings, annotations, conceptual groupings) that originate in the KG domain, but they are scoped, clearly separated from derived data, version-controlled or governed, and must never silently contradict authoritative upstream data.
   * Any correction to raw facts must occur in the upstream system, not inside the KG.

9. **Ontology evolution follows domain needs, not database design.**
   * New classes/properties added only when domain concepts or workflows require them.
   * Database internal changes do not automatically justify ontology changes.

10. **Keep everything human-readable and governance-friendly.**
    * Use labels, clear definitions, and controlled vocabularies.
    * Keep modeling minimal and intuitive so biologists, analysts, and developers can work together.

**Architecture Summary**:

* **Separate concerns:**

  * SPSR: numbers + operational schema (source of truth for data).
  * Ontology: concepts + relationships + controlled vocabularies (TBox).
  * KG: derived, shareable semantic view (ABox) using IRIs, accessed via Graph API Service.
  * Graph API Service: REST API intermediary between SPSR and KG.

* **Don’t over-ontologize:**

  * Not every table → class.
  * Not every column → property.
  * Not every row → individual.

* **Respect existing governance:**

  * CU registry remains SoT; ontology doesn’t take over its role.
  * Ontology consumes identifiers; it doesn’t own them.

* **Use identifiers as the bridge:**

  * Stable business codes in DBs.
  * Deterministic IRI patterns in KG.
  * Optional IRI columns where helpful.

* **Maintain strict TBox/ABox separation:**

  * TBox curated by ontology devs (in ontology repo).
  * ABox generated by ETL and kept out of the ontology repo.

* **FSAR Tracer MVP**: Primary use case driving integration, using Graph API Service for evidence chains, vocabularies, and validation.

If everyone follows these conventions, you get a hybrid architecture that’s:

* Understandable by biologists and developers,
* Governable without chaos,
* And powerful enough to support the semantic / KG / AI stuff you care about.

---

Do you want to see a concrete worked example for one SPSR table (e.g. `time_series` or `indicator`) showing the exact DB columns, the ontology pieces, and the KG ABox that would be generated from it?
