# Add Missing SPSR Terms to DFO Salmon Ontology

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document must be maintained in accordance with `agent-config/PLANS.md`.

## Purpose / Big Picture

After this change, the DFO Salmon Ontology will include all critical terms needed to fully represent data from the Salmon Population Summary Repository (SPSR) database schema. This enables seamless integration between SPSR's PostgreSQL database and the ontology-based graph knowledge service, supporting the FSAR Tracer application and other downstream uses.

Users will be able to:
- Map SPSR database records to ontology classes without loss of semantic information
- Query SPSR data using SPARQL with proper ontological relationships
- Validate SPSR data imports against ontology constraints
- Generate FSAR trace packs with complete provenance chains

To see this working, after implementation you should be able to:
1. Load SPSR data into the graph database using ontology terms
2. Query for run sizes, mortality rates, and PFMA data using SPARQL
3. Validate that all SPSR core concepts have corresponding ontology classes

## Progress

- [ ] (2025-12-03) Analysis completed: comparison document created
- [ ] Decompose SPSR compound columns and publish mapping table (`docs/notes/spsr-column-to-ontology-mapping.md`)
- [ ] Add `gcdfos:SalmonRunSize` + `:RunComponentTypeScheme` + `gcdfos:runComponentType` (no per-column subclasses)
- [ ] Add `gcdfos:MortalityRate` + `:MortalityComponentTypeScheme` + `gcdfos:mortalityComponentType`
- [ ] Add `gcdfos:PacificFisheryManagementArea` class
- [ ] Add age classification properties (numeric) and reuse AgeType scheme
- [ ] Add YearType and AgeType SKOS schemes
- [ ] Add LifeHistoryType and CUType SKOS schemes
- [ ] Add DFOArea SKOS scheme
- [ ] Add InformationQuality and IndexQuality (DQV-based)
- [ ] Add Broodstock class/properties with origin decomposition
- [ ] Add EnhancementObjective and EnhancementTarget properties
- [ ] Add method documentation properties (methodCollectionNotes, methodAnalysisNotes)
- [ ] Validate ontology consistency and run reasoner tests
- [ ] Update w3id core terms document if applicable
- [ ] Update comparison and mapping documents with implementation status

## Surprises & Discoveries

_To be populated during implementation_

## Decision Log

- Decision: Focus on high-priority Category B terms first (Run, MortalityRate, PFMA, Age)
  Rationale: These are fundamental to SPSR data model and most critical for integration
  Date/Author: 2025-12-03 / Analysis phase

- Decision: Use SKOS schemes for controlled vocabularies (YearType, AgeType, LifeHistoryType, CUType, DFOArea)
  Rationale: Consistent with existing ontology pattern; allows for future expansion. Per `onto_spsr_graph_review.md`, lookup/code tables → SKOS concept schemes.
  Date/Author: 2025-12-03 / Analysis phase

- Decision: Extend DQV framework for InformationQuality and IndexQuality
  Rationale: Ontology already uses DQV; maintains consistency. These are domain attributes, so DQV-based annotations are appropriate.
  Date/Author: 2025-12-03 / Analysis phase

- Decision: Make Run and MortalityRate as classes (not just properties)
  Rationale: Per conventions, these are domain concepts that appear in FSARs/reports, so classes are appropriate. Consistent with existing pattern (`gcdfos:Catch`, `gcdfos:SpawnerAbundance` are classes). They represent measurement types, not just values.
  Date/Author: 2025-12-03 / After reviewing conventions

- Decision: Add object properties for controlled vocabularies (not just SKOS schemes)
  Rationale: Per conventions section 5.2: "Controlled, domain-specific categorical value? → Map as object property pointing to SKOS concepts." So we need both the SKOS scheme AND object properties to link classes to concepts.
  Date/Author: 2025-12-03 / After reviewing conventions

- Decision: Age as datatype properties (numeric) rather than SKOS
  Rationale: Age in SPSR is numeric (1-7), not categorical. Per conventions, numeric measurements → datatype properties. If age classes become categorical vocabularies later, we can add SKOS.
  Date/Author: 2025-12-03 / After reviewing conventions

- Decision: Decompose compound SPSR column names before modeling
  Rationale: Many SPSR columns fuse quantity, stratum, age, time basis, and origin; decomposition prevents baking current column names into ontology classes/properties and keeps dimensions orthogonal.
  Date/Author: 2025-12-07 / Feedback from DFO Salmon Data Standards Assistant

- Decision: Use component-type schemes for run and mortality instead of multiple subclasses
  Rationale: Run and mortality variants differ by reporting stratum; modeling them as component types (SKOS + object property) avoids class explosion while preserving reasoning flexibility. Subclasses only added if decomposition + CQs show distinct logic.
  Date/Author: 2025-12-07 / Feedback from DFO Salmon Data Standards Assistant

## Outcomes & Retrospective

_To be populated upon completion_

## Context and Orientation

The DFO Salmon Ontology is located in `draft/dfo-salmon-draft.ttl`. This is a Turtle/RDF file containing OWL classes, SKOS concept schemes, and properties for representing salmon stock assessment data.

**Critical Convention**: This ontology is **TBox only** (schema/vocabulary). We do **not** model SPSR data instances (ABox) in the ontology files. The ontology defines concepts and relationships; data instances are generated via ETL into a separate knowledge graph. See `onto_spsr_graph_review.md` for full conventions.

The ontology follows these patterns (per `onto_spsr_graph_review.md`):
- **OWL classes** for domain entities that appear in reports/governance (e.g., `gcdfos:Stock`, `gcdfos:ConservationUnit`)
- **SKOS concept schemes** for controlled vocabularies/lookup tables (e.g., `:WSPMetricScheme`)
- **Object properties** for relationships between classes and to SKOS concepts
- **Datatype properties** for domain attributes (numeric/text/date measurements)
- **Do NOT model**: Technical columns (IDs, timestamps, ETL flags), purely operational fields

**Triage rules** (from conventions):
- Entity tables → OWL classes
- Lookup/code tables → SKOS concept schemes  
- Foreign keys → Object properties
- Controlled categorical values → Object property to SKOS concepts
- Domain measurements → Datatype properties
- Technical/operational → Not modeled

The ontology uses these prefixes:
- `gcdfos:` for DFO Salmon Ontology terms (`https://w3id.org/gcdfos/salmon#`)
- `iao:` for Information Artifact Ontology
- `dqv:` for Data Quality Vocabulary
- `skos:` for SKOS
- `rdfs:` for RDF Schema
- `owl:` for OWL

The comparison analysis is documented in `docs/notes/2025-12-03-spsr-ontology-comparison.md`, which identifies:
- **Category A**: Terms already in ontology (no action needed)
- **Category B**: Terms missing but critical (this execplan addresses these)
- **Category C**: Terms missing but lower priority (deferred)

## Plan of Work

This plan adds the high and medium priority Category B terms identified in the comparison analysis, following the conventions in `onto_spsr_graph_review.md`. Work proceeds in logical groups:

0. **Decompose SPSR columns first**: Build a mapping table that decomposes compound SPSR column names into quantity type, stratum/location, temporal semantics, age semantics, and origin/composition before minting new ontology terms.

1. **Run components**: Add a single `gcdfos:SalmonRunSize` measurement class plus a `:RunComponentTypeScheme` and `gcdfos:runComponentType` object property (e.g., total, ocean, terminal, mainstem components). Add further subclasses only if decomposition and competency questions prove distinct logic is needed.

2. **Mortality components**: Keep a single `gcdfos:MortalityRate` measurement class, add `:MortalityComponentTypeScheme`, and `gcdfos:mortalityComponentType` object property (e.g., ocean, in-river/terminal, total) instead of multiple subclasses.

3. **PFMA class**: Add Pacific Fishery Management Area as a reporting stratum. Keep PFMA orthogonal to run/mortality component types.

4. **Age classifications**: Keep age numeric via datatype properties (freshwaterAge, oceanAge, totalAge/ageClass) and tie age semantics to AgeType scheme; do not create per-age classes or properties.

5. **Controlled vocabularies**: Add SKOS schemes for YearType, AgeType, LifeHistoryType, CUType, DFOArea plus object properties to link to those schemes.

6. **Data quality**: Extend DQV framework for InformationQuality and IndexQuality.

7. **Broodstock and enhancement**: Add Broodstock class with origin decomposition (hatchery vs natural) and enhancement properties without encoding context into class names.

8. **Method documentation**: Add datatype properties for collection and analysis method notes.

**Modeling decisions per conventions**:
- Run/MortalityRate: Use a single measurement class + component-type SKOS scheme + object property (e.g., runComponentType, mortalityComponentType). Add subclasses only if decomposition + competency questions require distinct logical behavior. Use `gcdfos:SalmonRunSize` for run-size measurements.
- Age: Numeric values → datatype properties. Age semantics captured via AgeType scheme; no per-age classes/properties.
- Controlled vocabularies: SKOS schemes + object properties to link (e.g., `gcdfos:yearType` object property to YearTypeScheme concepts).
- Technical fields: NOT modeled (IDs, timestamps, ETL flags are excluded).

Each addition follows existing ontology patterns:
- Classes include `rdfs:label`, `iao:0000115` (definition), `iao:0000119` (definition source), `rdfs:isDefinedBy`
- SKOS concepts include `skos:prefLabel`, `skos:definition`, `skos:inScheme`
- Properties include `rdfs:label`, `iao:0000115`, `rdfs:isDefinedBy` (no global domain/range - use class restrictions or SHACL instead)
- Object properties for controlled vocabularies link classes to SKOS concepts (not just datatype properties)
- **Domain/range guidance**: Per CONVENTIONS.md, prefer class restrictions and SHACL for validation over global `rdfs:domain`/`rdfs:range` declarations. Global domain/range propagate broadly and can cause unintended logical consequences. Use them conservatively only when the constraint is always true.

## Concrete Steps

All ontology edits from this plan are applied to `draft/dfo-salmon-draft.ttl` using the `gcdfos:` namespace.

### Step 0: Decompose SPSR compound terms

- Review `demo/datadictionary.py` and list every column where multiple semantic dimensions are fused into one name (quantity type, stratum/location, temporal semantics, age semantics, origin/composition).
- For each, decompose into `{quantity type, stratum/location, time basis, age basis, origin}` and propose the OWL/SKOS/predicate pattern that represents it.
- Publish the mapping table at `docs/notes/spsr-column-to-ontology-mapping.md`. No new ontology term is added until it has a row in this mapping table.

### Step 1: Add SalmonRunSize + component type scheme

- Add a single measurement class `gcdfos:SalmonRunSize` (subClassOf `gcdfos:ObservedRateOrAbundance`) with definition and source, aligned with existing measurement classes (e.g., `gcdfos:Catch`).
- Add a SKOS scheme `:RunComponentTypeScheme` with concepts such as `:TotalRun`, `:OceanComponent`, `:TerminalComponent`, `:MainstemComponent` (final list driven by Step 0).
- Add an object property `gcdfos:runComponentType` linking `gcdfos:SalmonRunSize` to `:RunComponentTypeScheme` concepts.
- Use existing numeric value property for the count; do not create per-component subclasses. Only add specific subclasses later if decomposition + competency questions show distinct logical behavior.

### Step 2: Add MortalityRate + component type scheme

- Keep a single measurement class `gcdfos:MortalityRate` (subClassOf `gcdfos:ObservedRateOrAbundance`) with definition and source.
- Add a SKOS scheme `:MortalityComponentTypeScheme` with concepts such as `:OceanMortality`, `:InRiverMortality`, `:TerminalMortality`, `:TotalMortality` (final list driven by Step 0).
- Add an object property `gcdfos:mortalityComponentType` linking `gcdfos:MortalityRate` to that scheme.
- Do not add per-component subclasses unless decomposition + competency questions require distinct reasoning.

### Step 3: Add Pacific Fishery Management Area

After the `gcdfos:StockManagementUnit` class definition (around line 1392), add:

    gcdfos:PacificFisheryManagementArea a owl:Class ;
      rdfs:label "Pacific Fishery Management Area"@en ;
      skos:altLabel "PFMA"@en ;
      iao:0000115 "A geographic area defined for Pacific salmon fishery management purposes, used for catch reporting and management planning."@en ;
      rdfs:subClassOf gcdfos:ReportingOrManagementStratum ;
      iao:0000119 "Fisheries and Oceans Canada. (2024). Pacific Fishery Management Areas. Available at https://www.pac.dfo-mpo.gc.ca/fm-gp/maps-cartes/pfma-zpag-eng.html [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
- Modeling note: PFMA is a stratum that combines with run/mortality components in data; do not create PFMA-specific run or mortality classes.

### Step 4: Add Age Classification Properties and Scheme

After the existing SKOS schemes section (around line 188), add a new scheme:

    :AgeClassScheme a skos:ConceptScheme ;
      skos:prefLabel "Age Class Scheme"@en ;
      skos:definition "Controlled vocabulary for salmon age classes (typically 1-7 years)."@en ;
      gcdfos:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

Then add datatype properties after the existing datatype properties section (around line 2255):

    gcdfos:ageClass a owl:DatatypeProperty ;
      rdfs:label "age class"@en ;
      skos:prefLabel "age class"@en ;
      iao:0000115 "The age class of salmon (typically 1-7 years), which may refer to freshwater age, ocean age, or total age depending on context."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run, Recruitment) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:oceanAge a owl:DatatypeProperty ;
      rdfs:label "ocean age"@en ;
      skos:prefLabel "ocean age"@en ;
      iao:0000115 "The number of years a salmon spent in the ocean before returning to spawn."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:freshwaterAge a owl:DatatypeProperty ;
      rdfs:label "freshwater age"@en ;
      skos:prefLabel "freshwater age"@en ;
      iao:0000115 "The number of years a salmon spent in freshwater before migrating to the ocean."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.
- Modeling note: Age-specific SPSR columns (e.g., *_age_3) are represented as a SalmonRunSize/Catch/etc. measurement + `gcdfos:ageType` + numeric age value; no per-age classes or properties.

### Step 5: Add YearType and AgeType SKOS Schemes and Object Properties

After the `:EstimateTypeScheme` definition (around line 147), add:

    :YearTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Year Type Scheme"@en ;
      skos:definition "Controlled vocabulary for year definition types used in datasets (e.g., calendar year, brood year)."@en ;
      gcdfos:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :CalendarYear a skos:Concept ;
      skos:prefLabel "Calendar year"@en ;
      skos:definition "Year defined by calendar dates (January 1 to December 31)."@en ;
      skos:inScheme :YearTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :BroodYearType a skos:Concept ;
      skos:prefLabel "Brood year"@en ;
      skos:definition "Year defined by the spawning year of the parental generation."@en ;
      skos:inScheme :YearTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :AgeTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Age Type Scheme"@en ;
      skos:definition "Controlled vocabulary for age definition types used in datasets (e.g., freshwater age, ocean age, total age)."@en ;
      gcdfos:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :FreshwaterAgeType a skos:Concept ;
      skos:prefLabel "Freshwater age"@en ;
      skos:definition "Age defined as the number of years spent in freshwater before ocean migration."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :OceanAgeType a skos:Concept ;
      skos:prefLabel "Ocean age"@en ;
      skos:definition "Age defined as the number of years spent in the ocean."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :TotalAgeType a skos:Concept ;
      skos:prefLabel "Total age"@en ;
      skos:definition "Age defined as the total number of years (freshwater + ocean)."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

Then add object properties to link classes to these SKOS concepts (after the existing object properties section, around line 1920):

    gcdfos:yearType a owl:ObjectProperty ;
      rdfs:label "year type"@en ;
      skos:prefLabel "year type"@en ;
      iao:0000115 "The type of year definition used in a dataset (e.g., calendar year, brood year)."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:ageType a owl:ObjectProperty ;
      rdfs:label "age type"@en ;
      skos:prefLabel "age type"@en ;
      iao:0000115 "The type of age definition used in a dataset (e.g., freshwater age, ocean age, total age)."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 6: Add LifeHistoryType and CUType Schemes and Object Properties

After the `:RapidStatusConfidenceScheme` definition (around line 188), add:

    :LifeHistoryTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Life History Type Scheme"@en ;
      skos:definition "Controlled vocabulary for salmon life cycle patterns."@en ;
      gcdfos:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :CUTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Conservation Unit Type Scheme"@en ;
      skos:definition "Controlled vocabulary for Conservation Unit groupings for Pacific salmon (currently nine types)."@en ;
      gcdfos:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

Then add object properties (after the ageType property from Step 5):

    gcdfos:lifeHistoryType a owl:ObjectProperty ;
      rdfs:label "life history type"@en ;
      skos:prefLabel "life history type"@en ;
      iao:0000115 "The life cycle pattern classification for a salmon population or conservation unit."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (ConservationUnit, Stock) and range (skos:Concept) should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:cuType a owl:ObjectProperty ;
      rdfs:label "conservation unit type"@en ;
      skos:prefLabel "conservation unit type"@en ;
      iao:0000115 "The Conservation Unit type classification (one of nine groupings for Pacific salmon)."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (ConservationUnit) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 7: Add DFOArea Scheme and Object Property

After the organizational structure section (around line 733), add:

    :DFOAreaScheme a skos:ConceptScheme ;
      skos:prefLabel "DFO Area Scheme"@en ;
      skos:definition "Controlled vocabulary for Fisheries and Oceans Canada geographic areas (South Coast, North Coast, Fraser and Interior, Yukon Transboundary)."@en ;
      gcdfos:theme :PolicyGovernanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :SouthCoast a skos:Concept ;
      skos:prefLabel "South Coast"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :NorthCoast a skos:Concept ;
      skos:prefLabel "North Coast"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :FraserAndInterior a skos:Concept ;
      skos:prefLabel "Fraser and Interior"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    :YukonTransboundary a skos:Concept ;
      skos:prefLabel "Yukon Transboundary"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

Then add object property (after the cuType property from Step 6):

    gcdfos:dfoArea a owl:ObjectProperty ;
      rdfs:label "DFO area"@en ;
      skos:prefLabel "DFO area"@en ;
      iao:0000115 "The Fisheries and Oceans Canada geographic area in which a unit resides."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (ConservationUnit, StockManagementUnit, PacificFisheryManagementArea) 
      # and range (skos:Concept) should be enforced via class restrictions or SHACL, 
      # not global domain/range declarations.
- Modeling note: DFO area is orthogonal to PFMA and run/mortality component type; combine in data, not in class names.

### Step 8: Add InformationQuality and IndexQuality (DQV-based)

After the existing DQV dimensions (around line 822), add:

    gcdfos:InformationQualityRating a dqv:QualityAnnotation ;
      skos:prefLabel "Information Quality Rating"@en ;
      dqv:inDimension gcdfos:DataCurrencyDimension ;
      skos:definition "Quality rating of a dataset quantified from 1-5 based on the data quality framework in Ogden 2015, section 2.3."@en ;
      gcdfos:theme gcdfos:DataModelProvenanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    gcdfos:IndexQualityRating a dqv:QualityAnnotation ;
      skos:prefLabel "Index Quality Rating"@en ;
      dqv:inDimension gcdfos:DataCurrencyDimension ;
      skos:definition "Quality rating of a dataset quantified from 1-5 based on New Zealand Quality Index."@en ;
      gcdfos:theme gcdfos:DataModelProvenanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    gcdfos:informationQuality a owl:DatatypeProperty ;
      rdfs:label "information quality"@en ;
      skos:prefLabel "information quality"@en ;
      iao:0000115 "Information quality rating (1-5) based on Ogden 2015 data quality framework."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:indexQuality a owl:DatatypeProperty ;
      rdfs:label "index quality"@en ;
      skos:prefLabel "index quality"@en ;
      iao:0000115 "Index quality rating (1-5) based on New Zealand Quality Index."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 9: Add Broodstock Classes and Properties

After the `gcdfos:HatcheryProduction` class (around line 1142), add:

    gcdfos:Broodstock a owl:Class ;
      rdfs:label "Broodstock"@en ;
      iao:0000115 "Adult fish selected for breeding purposes in hatchery or enhancement programs."@en ;
      rdfs:subClassOf dwc:Organism ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    gcdfos:HatcheryOriginBroodstock a owl:Class ;
      rdfs:label "Hatchery-origin broodstock"@en ;
      iao:0000115 "Broodstock fish that were born or reared in a hatchery and later selected for breeding purposes."@en ;
      rdfs:subClassOf gcdfos:Broodstock ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .

    gcdfos:NaturalOriginBroodstock a owl:Class ;
      rdfs:label "Natural-origin broodstock"@en ;
      iao:0000115 "Broodstock fish that were born and reared in the wild and later collected for breeding purposes."@en ;
      rdfs:subClassOf gcdfos:Broodstock ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
- Modeling note: Use an origin property (e.g., to a SalmonOrigin scheme) rather than separate classes for every context; keep counts/context in data, not class names.

Then add properties after the enhancement-related properties:

    gcdfos:totalBroodstockRemoved a owl:DatatypeProperty ;
      rdfs:label "total broodstock removed"@en ;
      skos:prefLabel "total broodstock removed"@en ;
      iao:0000115 "Total number of broodstock fish removed from the population for hatchery or enhancement purposes."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Stock) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 10: Add Enhancement Objective and Target Properties

After the `gcdfos:Enhancement` class definition (around line 1035), add properties:

    gcdfos:enhancementObjective a owl:DatatypeProperty ;
      rdfs:label "enhancement objective"@en ;
      skos:prefLabel "enhancement objective"@en ;
      iao:0000115 "The stated objective or goal of an enhancement program."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Enhancement) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:enhancementTarget a owl:DatatypeProperty ;
      rdfs:label "enhancement target"@en ;
      skos:prefLabel "enhancement target"@en ;
      iao:0000115 "The target metric or goal value for an enhancement program."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Enhancement) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 11: Add Method Documentation Properties

After the existing method-related properties (around line 1919), add:

    gcdfos:methodCollectionNotes a owl:DatatypeProperty ;
      rdfs:label "method collection notes"@en ;
      skos:prefLabel "method collection notes"@en ;
      iao:0000115 "Notes on data collection methods, including data sources, field methods, and collection protocols."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:methodAnalysisNotes a owl:DatatypeProperty ;
      rdfs:label "method analysis notes"@en ;
      skos:prefLabel "method analysis notes"@en ;
      iao:0000115 "Notes on data analysis methods, including infill methods, analytical approaches, and statistical treatments."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain (Dataset) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 12: Add General Time Series Properties

After the existing datatype properties, add:

    gcdfos:startYear a owl:DatatypeProperty ;
      rdfs:label "start year"@en ;
      skos:prefLabel "start year"@en ;
      iao:0000115 "The start year of a time series index or dataset."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (Dataset, StockManagementUnit, ConservationUnit) and range (xsd:gYear) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    gcdfos:endYear a owl:DatatypeProperty ;
      rdfs:label "end year"@en ;
      skos:prefLabel "end year"@en ;
      iao:0000115 "The end year of a time series index or dataset."@en ;
      rdfs:isDefinedBy <https://w3id.org/gcdfos/salmon> .
      # Note: Domain constraints (Dataset, StockManagementUnit, ConservationUnit) and range (xsd:gYear) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

## Validation and Acceptance

After completing the additions:

1. **Validate Turtle syntax**: Run a Turtle parser to ensure the file is valid RDF
   - Command: `rapper -i turtle -c draft/dfo-salmon-draft.ttl` (if rapper is available)
   - Or use `rdflib` in Python: `python -c "from rdflib import Graph; g = Graph(); g.parse('draft/dfo-salmon-draft.ttl', format='turtle')"`
   - Expected: No syntax errors

2. **Check for duplicate definitions**: Search for any class/property names that appear twice
   - Command: `grep -E "^gcdfos:[A-Za-z]+" draft/dfo-salmon-draft.ttl | sort | uniq -d`
   - Expected: No duplicates

3. **Verify namespace consistency**: Ensure all new terms use `gcdfos:` prefix and `https://w3id.org/gcdfos/salmon#` namespace
   - Command: `grep -E "^(gcdfos:|:)[A-Za-z]+" draft/dfo-salmon-draft.ttl | head -20`
   - Expected: All use correct prefix
4. **Mapping table gate**: Every new term must have a row in `docs/notes/spsr-column-to-ontology-mapping.md` showing decomposition and selected pattern. No TTL changes without an entry.

5. **Test SPARQL queries (CQ-RUN-1)**: Verify decomposed run structure
   ```sparql
   PREFIX gcdfos: <https://w3id.org/gcdfos/salmon#>
   PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
   SELECT ?year ?componentLabel ?value WHERE {
     ?run a gcdfos:SalmonRunSize ;
          gcdfos:aboutConservationUnit <YOUR_CU_IRI_HERE> ;
          gcdfos:observationYear ?year ;
          gcdfos:runComponentType ?component ;
          gcdfos:hasValue ?value .
     ?component skos:prefLabel ?componentLabel .
   }
   ORDER BY ?year ?componentLabel
   ```
   - Expected: Returns total/ocean/terminal/mainstem components per year when data is loaded.

6. **Cross-reference with SPSR schema**: Verify decomposed mappings for Category B high-priority terms in `docs/notes/2025-12-03-spsr-ontology-comparison.md` and the new mapping table.

7. **Update comparison/mapping documents**: Mark implemented terms and decomposition status in both comparison and mapping documents.

## Idempotence and Recovery

All steps are additive and can be repeated safely. If a class or property already exists, the Turtle parser will catch duplicate definitions. To recover from errors:

1. **Syntax errors**: Fix the specific line indicated by the parser
2. **Duplicate definitions**: Remove the duplicate, keeping the more complete definition
3. **Namespace errors**: Ensure all terms use the correct `gcdfos:` prefix

If you need to remove additions:
- Search for the class/property name and delete its definition block
- Re-validate the file

## Artifacts and Notes

_To be populated during implementation with evidence of successful additions_

## Interfaces and Dependencies

New classes extend existing ontology hierarchies:
- `gcdfos:SalmonRunSize` → `gcdfos:ObservedRateOrAbundance`
- `gcdfos:MortalityRate` → `gcdfos:ObservedRateOrAbundance`
- `gcdfos:PacificFisheryManagementArea` → `gcdfos:ReportingOrManagementStratum`
- `gcdfos:Broodstock` → `dwc:Organism`

New properties follow existing patterns:
- All include `rdfs:label`, `iao:0000115`, `rdfs:isDefinedBy`
- Domain/range constraints are enforced via class restrictions or SHACL (not global `rdfs:domain`/`rdfs:range`)
- SKOS concepts include `skos:prefLabel`, `skos:definition`, `skos:inScheme`

No external dependencies are added. All terms use existing ontology patterns and imported vocabularies (DQV, SKOS, IAO, DwC).

