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
- [ ] Add `dfoc:Run` class hierarchy (Run, OceanRun, TerminalRun, MainstemRun)
- [ ] Add `dfoc:MortalityRate` class hierarchy (Mainstem, Ocean, Terminal, Total, InRiver)
- [ ] Add `dfoc:PacificFisheryManagementArea` class
- [ ] Add age classification properties and SKOS scheme
- [ ] Add YearType and AgeType SKOS schemes
- [ ] Add LifeHistoryType and CUType SKOS schemes
- [ ] Add DFOArea SKOS scheme
- [ ] Add InformationQuality and IndexQuality (DQV-based)
- [ ] Add Broodstock classes and properties
- [ ] Add EnhancementObjective and EnhancementTarget properties
- [ ] Add method documentation properties (methodCollectionNotes, methodAnalysisNotes)
- [ ] Validate ontology consistency and run reasoner tests
- [ ] Update w3id core terms document if applicable
- [ ] Update comparison document with implementation status

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
  Rationale: Per conventions, these are domain concepts that appear in FSARs/reports, so classes are appropriate. Consistent with existing pattern (`dfoc:Catch`, `dfoc:SpawnerAbundance` are classes). They represent measurement types, not just values.
  Date/Author: 2025-12-03 / After reviewing conventions

- Decision: Add object properties for controlled vocabularies (not just SKOS schemes)
  Rationale: Per conventions section 5.2: "Controlled, domain-specific categorical value? → Map as object property pointing to SKOS concepts." So we need both the SKOS scheme AND object properties to link classes to concepts.
  Date/Author: 2025-12-03 / After reviewing conventions

- Decision: Age as datatype properties (numeric) rather than SKOS
  Rationale: Age in SPSR is numeric (1-7), not categorical. Per conventions, numeric measurements → datatype properties. If age classes become categorical vocabularies later, we can add SKOS.
  Date/Author: 2025-12-03 / After reviewing conventions

## Outcomes & Retrospective

_To be populated upon completion_

## Context and Orientation

The DFO Salmon Ontology is located in `draft/dfo-salmon-draft.ttl`. This is a Turtle/RDF file containing OWL classes, SKOS concept schemes, and properties for representing salmon stock assessment data.

**Critical Convention**: This ontology is **TBox only** (schema/vocabulary). We do **not** model SPSR data instances (ABox) in the ontology files. The ontology defines concepts and relationships; data instances are generated via ETL into a separate knowledge graph. See `onto_spsr_graph_review.md` for full conventions.

The ontology follows these patterns (per `onto_spsr_graph_review.md`):
- **OWL classes** for domain entities that appear in reports/governance (e.g., `dfoc:Stock`, `dfoc:ConservationUnit`)
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
- `dfoc:` for DFO Salmon Ontology terms (`https://w3id.org/dfoc/salmon#`)
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

1. **Run classes**: Add `dfoc:Run` as a measurement class (domain concept appearing in FSARs/reports) with subclasses for ocean, terminal, and mainstem runs. These are measurement types, not just values, so classes are appropriate per conventions.

2. **Mortality rate classes**: Add `dfoc:MortalityRate` hierarchy for different mortality types. These are domain concepts (appear in stock assessments), so classes align with existing patterns (like `dfoc:FishingMortality`).

3. **PFMA class**: Add Pacific Fishery Management Area as a reporting stratum. This is an entity table in SPSR, so it becomes an OWL class.

4. **Age classifications**: Add datatype properties for age values (numeric) and consider SKOS if age classes become categorical. Age is numeric in SPSR, so datatype properties are primary.

5. **Controlled vocabularies**: Add SKOS schemes for YearType, AgeType, LifeHistoryType, CUType, DFOArea. These are lookup/code tables in SPSR, so SKOS is appropriate. **Also add object properties** to link classes to these SKOS concepts (per conventions: "controlled categorical value → object property to SKOS concepts").

6. **Data quality**: Extend DQV framework for InformationQuality and IndexQuality. These are domain attributes, so DQV-based annotations are appropriate.

7. **Broodstock and enhancement**: Add classes and properties for hatchery management. These are domain entities, so classes are appropriate.

8. **Method documentation**: Add datatype properties for collection and analysis method notes. These are domain attributes (text fields), so datatype properties are appropriate.

**Modeling decisions per conventions**:
- Run/MortalityRate subclasses: These represent distinct measurement types that appear in reports, so classes are appropriate (consistent with `dfoc:Catch`, `dfoc:SpawnerAbundance` pattern).
- Age: Numeric values → datatype properties. If age classes become categorical vocabularies later, add SKOS.
- Controlled vocabularies: SKOS schemes + object properties to link (e.g., `dfoc:yearType` object property to YearTypeScheme concepts).
- Technical fields: NOT modeled (IDs, timestamps, ETL flags are excluded).

Each addition follows existing ontology patterns:
- Classes include `rdfs:label`, `iao:0000115` (definition), `iao:0000119` (definition source), `rdfs:isDefinedBy`
- SKOS concepts include `skos:prefLabel`, `skos:definition`, `skos:inScheme`
- Properties include `rdfs:label`, `iao:0000115`, `rdfs:isDefinedBy` (no global domain/range - use class restrictions or SHACL instead)
- Object properties for controlled vocabularies link classes to SKOS concepts (not just datatype properties)
- **Domain/range guidance**: Per CONVENTIONS.md, prefer class restrictions and SHACL for validation over global `rdfs:domain`/`rdfs:range` declarations. Global domain/range propagate broadly and can cause unintended logical consequences. Use them conservatively only when the constraint is always true.

## Concrete Steps

### Step 1: Add Run Class Hierarchy

Edit `draft/dfo-salmon-draft.ttl`. After the `dfoc:Recruitment` class definition (around line 1303), add:

    dfoc:Run a owl:Class ;
      rdfs:label "Run"@en ;
      iao:0000115 "The number of salmon returning to a given system, typically calculated as spawners plus catch. May be disaggregated by life stage (ocean, terminal, mainstem) or age class."@en ;
      rdfs:subClassOf dfoc:ObservedRateOrAbundance ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:OceanRun a owl:Class ;
      rdfs:label "Ocean run"@en ;
      iao:0000115 "The number of salmon returning to a given system that have entered ocean fisheries, calculated as ocean catch plus terminal run."@en ;
      rdfs:subClassOf dfoc:Run ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:TerminalRun a owl:Class ;
      rdfs:label "Terminal run"@en ;
      iao:0000115 "The number of salmon returning to a given system that have reached terminal (in-river) fisheries, calculated as terminal catch plus escapement."@en ;
      rdfs:subClassOf dfoc:Run ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:MainstemRun a owl:Class ;
      rdfs:label "Mainstem run"@en ;
      iao:0000115 "The number of salmon returning to a given system that have entered mainstem (in-river) fisheries."@en ;
      rdfs:subClassOf dfoc:Run ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

### Step 2: Add Mortality Rate Class Hierarchy

After the `dfoc:FishingMortality` class definition (around line 1097), add:

    dfoc:MortalityRate a owl:Class ;
      rdfs:label "Mortality rate"@en ;
      iao:0000115 "The proportion of a fish population that dies during a specific life stage or phase, expressed as a rate (0.0 to 1.0) or percentage."@en ;
      rdfs:subClassOf dfoc:ObservedRateOrAbundance ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:MainstemMortalityRate a owl:Class ;
      rdfs:label "Mainstem mortality rate"@en ;
      iao:0000115 "The proportion of a population that dies during the freshwater phase (mainstem)."@en ;
      rdfs:subClassOf dfoc:MortalityRate ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:OceanMortalityRate a owl:Class ;
      rdfs:label "Ocean mortality rate"@en ;
      iao:0000115 "The proportion of a population that dies during the marine phase (ocean)."@en ;
      rdfs:subClassOf dfoc:MortalityRate ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:TerminalMortalityRate a owl:Class ;
      rdfs:label "Terminal mortality rate"@en ;
      iao:0000115 "The proportion of a population that dies during the terminal phase (e.g., in-river fishery, if applicable)."@en ;
      rdfs:subClassOf dfoc:MortalityRate ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:TotalMortalityRate a owl:Class ;
      rdfs:label "Total mortality rate"@en ;
      iao:0000115 "The proportion of a fish population that dies from all causes over the time period."@en ;
      rdfs:subClassOf dfoc:MortalityRate ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:InRiverMortalityRate a owl:Class ;
      rdfs:label "In-river mortality rate"@en ;
      iao:0000115 "The proportion of a population that dies during the in-river phase."@en ;
      rdfs:subClassOf dfoc:MortalityRate ;
      iao:0000119 "Pacific Salmon Foundation. (2025). Methods for Assessing Status and Trends in Pacific Salmon Conservation Units and their Freshwater Habitats. The Pacific Salmon Foundation, Vancouver BC, Canada. Version 13. Available at https://salmonwatersheds.ca/document/lib_475/ [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

### Step 3: Add Pacific Fishery Management Area

After the `dfoc:StockManagementUnit` class definition (around line 1392), add:

    dfoc:PacificFisheryManagementArea a owl:Class ;
      rdfs:label "Pacific Fishery Management Area"@en ;
      skos:altLabel "PFMA"@en ;
      iao:0000115 "A geographic area defined for Pacific salmon fishery management purposes, used for catch reporting and management planning."@en ;
      rdfs:subClassOf dfoc:ReportingOrManagementStratum ;
      iao:0000119 "Fisheries and Oceans Canada. (2024). Pacific Fishery Management Areas. Available at https://www.pac.dfo-mpo.gc.ca/fm-gp/maps-cartes/pfma-zpag-eng.html [Accessed 09-10-2025]."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

### Step 4: Add Age Classification Properties and Scheme

After the existing SKOS schemes section (around line 188), add a new scheme:

    :AgeClassScheme a skos:ConceptScheme ;
      skos:prefLabel "Age Class Scheme"@en ;
      skos:definition "Controlled vocabulary for salmon age classes (typically 1-7 years)."@en ;
      dfoc:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

Then add datatype properties after the existing datatype properties section (around line 2255):

    dfoc:ageClass a owl:DatatypeProperty ;
      rdfs:label "age class"@en ;
      skos:prefLabel "age class"@en ;
      iao:0000115 "The age class of salmon (typically 1-7 years), which may refer to freshwater age, ocean age, or total age depending on context."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run, Recruitment) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    dfoc:oceanAge a owl:DatatypeProperty ;
      rdfs:label "ocean age"@en ;
      skos:prefLabel "ocean age"@en ;
      iao:0000115 "The number of years a salmon spent in the ocean before returning to spawn."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    dfoc:freshwaterAge a owl:DatatypeProperty ;
      rdfs:label "freshwater age"@en ;
      skos:prefLabel "freshwater age"@en ;
      iao:0000115 "The number of years a salmon spent in freshwater before migrating to the ocean."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (Catch, SpawnerAbundance, Run) and range (xsd:integer) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

### Step 5: Add YearType and AgeType SKOS Schemes and Object Properties

After the `:EstimateTypeScheme` definition (around line 147), add:

    :YearTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Year Type Scheme"@en ;
      skos:definition "Controlled vocabulary for year definition types used in datasets (e.g., calendar year, brood year)."@en ;
      dfoc:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :CalendarYear a skos:Concept ;
      skos:prefLabel "Calendar year"@en ;
      skos:definition "Year defined by calendar dates (January 1 to December 31)."@en ;
      skos:inScheme :YearTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :BroodYearType a skos:Concept ;
      skos:prefLabel "Brood year"@en ;
      skos:definition "Year defined by the spawning year of the parental generation."@en ;
      skos:inScheme :YearTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :AgeTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Age Type Scheme"@en ;
      skos:definition "Controlled vocabulary for age definition types used in datasets (e.g., freshwater age, ocean age, total age)."@en ;
      dfoc:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :FreshwaterAgeType a skos:Concept ;
      skos:prefLabel "Freshwater age"@en ;
      skos:definition "Age defined as the number of years spent in freshwater before ocean migration."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :OceanAgeType a skos:Concept ;
      skos:prefLabel "Ocean age"@en ;
      skos:definition "Age defined as the number of years spent in the ocean."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :TotalAgeType a skos:Concept ;
      skos:prefLabel "Total age"@en ;
      skos:definition "Age defined as the total number of years (freshwater + ocean)."@en ;
      skos:inScheme :AgeTypeScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

Then add object properties to link classes to these SKOS concepts (after the existing object properties section, around line 1920):

    dfoc:yearType a owl:ObjectProperty ;
      rdfs:label "year type"@en ;
      skos:prefLabel "year type"@en ;
      iao:0000115 "The type of year definition used in a dataset (e.g., calendar year, brood year)."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    dfoc:ageType a owl:ObjectProperty ;
      rdfs:label "age type"@en ;
      skos:prefLabel "age type"@en ;
      iao:0000115 "The type of age definition used in a dataset (e.g., freshwater age, ocean age, total age)."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 6: Add LifeHistoryType and CUType Schemes and Object Properties

After the `:RapidStatusConfidenceScheme` definition (around line 188), add:

    :LifeHistoryTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Life History Type Scheme"@en ;
      skos:definition "Controlled vocabulary for salmon life cycle patterns."@en ;
      dfoc:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :CUTypeScheme a skos:ConceptScheme ;
      skos:prefLabel "Conservation Unit Type Scheme"@en ;
      skos:definition "Controlled vocabulary for Conservation Unit groupings for Pacific salmon (currently nine types)."@en ;
      dfoc:theme :StockAssessmentTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

Then add object properties (after the ageType property from Step 5):

    dfoc:lifeHistoryType a owl:ObjectProperty ;
      rdfs:label "life history type"@en ;
      skos:prefLabel "life history type"@en ;
      iao:0000115 "The life cycle pattern classification for a salmon population or conservation unit."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (ConservationUnit, Stock) and range (skos:Concept) should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    dfoc:cuType a owl:ObjectProperty ;
      rdfs:label "conservation unit type"@en ;
      skos:prefLabel "conservation unit type"@en ;
      iao:0000115 "The Conservation Unit type classification (one of nine groupings for Pacific salmon)."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (ConservationUnit) and range (skos:Concept) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 7: Add DFOArea Scheme and Object Property

After the organizational structure section (around line 733), add:

    :DFOAreaScheme a skos:ConceptScheme ;
      skos:prefLabel "DFO Area Scheme"@en ;
      skos:definition "Controlled vocabulary for Fisheries and Oceans Canada geographic areas (South Coast, North Coast, Fraser and Interior, Yukon Transboundary)."@en ;
      dfoc:theme :PolicyGovernanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :SouthCoast a skos:Concept ;
      skos:prefLabel "South Coast"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :NorthCoast a skos:Concept ;
      skos:prefLabel "North Coast"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :FraserAndInterior a skos:Concept ;
      skos:prefLabel "Fraser and Interior"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    :YukonTransboundary a skos:Concept ;
      skos:prefLabel "Yukon Transboundary"@en ;
      skos:inScheme :DFOAreaScheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

Then add object property (after the cuType property from Step 6):

    dfoc:dfoArea a owl:ObjectProperty ;
      rdfs:label "DFO area"@en ;
      skos:prefLabel "DFO area"@en ;
      iao:0000115 "The Fisheries and Oceans Canada geographic area in which a unit resides."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (ConservationUnit, StockManagementUnit, PacificFisheryManagementArea) 
      # and range (skos:Concept) should be enforced via class restrictions or SHACL, 
      # not global domain/range declarations.

### Step 8: Add InformationQuality and IndexQuality (DQV-based)

After the existing DQV dimensions (around line 822), add:

    dfoc:InformationQualityRating a dqv:QualityAnnotation ;
      skos:prefLabel "Information Quality Rating"@en ;
      dqv:inDimension dfoc:DataCurrencyDimension ;
      skos:definition "Quality rating of a dataset quantified from 1-5 based on the data quality framework in Ogden 2015, section 2.3."@en ;
      dfoc:theme dfoc:DataModelProvenanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:IndexQualityRating a dqv:QualityAnnotation ;
      skos:prefLabel "Index Quality Rating"@en ;
      dqv:inDimension dfoc:DataCurrencyDimension ;
      skos:definition "Quality rating of a dataset quantified from 1-5 based on New Zealand Quality Index."@en ;
      dfoc:theme dfoc:DataModelProvenanceTheme ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:informationQuality a owl:DatatypeProperty ;
      rdfs:label "information quality"@en ;
      skos:prefLabel "information quality"@en ;
      iao:0000115 "Information quality rating (1-5) based on Ogden 2015 data quality framework."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    dfoc:indexQuality a owl:DatatypeProperty ;
      rdfs:label "index quality"@en ;
      skos:prefLabel "index quality"@en ;
      iao:0000115 "Index quality rating (1-5) based on New Zealand Quality Index."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 9: Add Broodstock Classes and Properties

After the `dfoc:HatcheryProduction` class (around line 1142), add:

    dfoc:Broodstock a owl:Class ;
      rdfs:label "Broodstock"@en ;
      iao:0000115 "Adult fish selected for breeding purposes in hatchery or enhancement programs."@en ;
      rdfs:subClassOf dwc:Organism ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:HatcheryOriginBroodstock a owl:Class ;
      rdfs:label "Hatchery-origin broodstock"@en ;
      iao:0000115 "Broodstock fish that were born or reared in a hatchery and later selected for breeding purposes."@en ;
      rdfs:subClassOf dfoc:Broodstock ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

    dfoc:NaturalOriginBroodstock a owl:Class ;
      rdfs:label "Natural-origin broodstock"@en ;
      iao:0000115 "Broodstock fish that were born and reared in the wild and later collected for breeding purposes."@en ;
      rdfs:subClassOf dfoc:Broodstock ;
      iao:0000119 "DFO. (2018). Review of genetically based targets for enhanced contributions to Canadian Pacific Chinook Salmon populations. DFO Can. Sci. Advis. Sec. Sci. Advis. Rep. 2018/001. (Erratum: October 2023)"@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .

Then add properties after the enhancement-related properties:

    dfoc:totalBroodstockRemoved a owl:DatatypeProperty ;
      rdfs:label "total broodstock removed"@en ;
      skos:prefLabel "total broodstock removed"@en ;
      iao:0000115 "Total number of broodstock fish removed from the population for hatchery or enhancement purposes."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Stock) and range (xsd:integer) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 10: Add Enhancement Objective and Target Properties

After the `dfoc:Enhancement` class definition (around line 1035), add properties:

    dfoc:enhancementObjective a owl:DatatypeProperty ;
      rdfs:label "enhancement objective"@en ;
      skos:prefLabel "enhancement objective"@en ;
      iao:0000115 "The stated objective or goal of an enhancement program."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Enhancement) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    dfoc:enhancementTarget a owl:DatatypeProperty ;
      rdfs:label "enhancement target"@en ;
      skos:prefLabel "enhancement target"@en ;
      iao:0000115 "The target metric or goal value for an enhancement program."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Enhancement) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 11: Add Method Documentation Properties

After the existing method-related properties (around line 1919), add:

    dfoc:methodCollectionNotes a owl:DatatypeProperty ;
      rdfs:label "method collection notes"@en ;
      skos:prefLabel "method collection notes"@en ;
      iao:0000115 "Notes on data collection methods, including data sources, field methods, and collection protocols."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

    dfoc:methodAnalysisNotes a owl:DatatypeProperty ;
      rdfs:label "method analysis notes"@en ;
      skos:prefLabel "method analysis notes"@en ;
      iao:0000115 "Notes on data analysis methods, including infill methods, analytical approaches, and statistical treatments."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain (Dataset) and range (xsd:string) constraints should be enforced 
      # via class restrictions or SHACL, not global domain/range declarations.

### Step 12: Add General Time Series Properties

After the existing datatype properties, add:

    dfoc:startYear a owl:DatatypeProperty ;
      rdfs:label "start year"@en ;
      skos:prefLabel "start year"@en ;
      iao:0000115 "The start year of a time series index or dataset."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (Dataset, StockManagementUnit, ConservationUnit) and range (xsd:gYear) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

    dfoc:endYear a owl:DatatypeProperty ;
      rdfs:label "end year"@en ;
      skos:prefLabel "end year"@en ;
      iao:0000115 "The end year of a time series index or dataset."@en ;
      rdfs:isDefinedBy <https://w3id.org/dfoc/salmon> .
      # Note: Domain constraints (Dataset, StockManagementUnit, ConservationUnit) and range (xsd:gYear) 
      # should be enforced via class restrictions or SHACL, not global domain/range declarations.

## Validation and Acceptance

After completing the additions:

1. **Validate Turtle syntax**: Run a Turtle parser to ensure the file is valid RDF
   - Command: `rapper -i turtle -c draft/dfo-salmon-draft.ttl` (if rapper is available)
   - Or use `rdflib` in Python: `python -c "from rdflib import Graph; g = Graph(); g.parse('draft/dfo-salmon-draft.ttl', format='turtle')"`
   - Expected: No syntax errors

2. **Check for duplicate definitions**: Search for any class/property names that appear twice
   - Command: `grep -E "^dfoc:[A-Za-z]+" draft/dfo-salmon-draft.ttl | sort | uniq -d`
   - Expected: No duplicates

3. **Verify namespace consistency**: Ensure all new terms use `dfoc:` prefix and `https://w3id.org/dfoc/salmon#` namespace
   - Command: `grep -E "^(dfoc:|:)[A-Za-z]+" draft/dfo-salmon-draft.ttl | head -20`
   - Expected: All use correct prefix

4. **Test SPARQL queries**: Create test queries to verify new classes can be queried
   - Example query for Run classes:
     ```sparql
     SELECT ?run ?label WHERE {
       ?run rdfs:subClassOf* dfoc:Run .
       ?run rdfs:label ?label .
     }
     ```
   - Expected: Returns Run, OceanRun, TerminalRun, MainstemRun

5. **Cross-reference with SPSR schema**: Verify that SPSR database fields can be mapped to new ontology terms
   - Check `docs/notes/2025-12-03-spsr-ontology-comparison.md` mapping
   - Expected: All Category B high-priority terms have corresponding ontology classes

6. **Update comparison document**: Mark implemented terms in the comparison document
   - Edit `docs/notes/2025-12-03-spsr-ontology-comparison.md`
   - Add implementation status for each Category B term

## Idempotence and Recovery

All steps are additive and can be repeated safely. If a class or property already exists, the Turtle parser will catch duplicate definitions. To recover from errors:

1. **Syntax errors**: Fix the specific line indicated by the parser
2. **Duplicate definitions**: Remove the duplicate, keeping the more complete definition
3. **Namespace errors**: Ensure all terms use the correct `dfoc:` prefix

If you need to remove additions:
- Search for the class/property name and delete its definition block
- Re-validate the file

## Artifacts and Notes

_To be populated during implementation with evidence of successful additions_

## Interfaces and Dependencies

New classes extend existing ontology hierarchies:
- `dfoc:Run` → `dfoc:ObservedRateOrAbundance`
- `dfoc:MortalityRate` → `dfoc:ObservedRateOrAbundance`
- `dfoc:PacificFisheryManagementArea` → `dfoc:ReportingOrManagementStratum`
- `dfoc:Broodstock` → `dwc:Organism`

New properties follow existing patterns:
- All include `rdfs:label`, `iao:0000115`, `rdfs:isDefinedBy`
- Domain/range constraints are enforced via class restrictions or SHACL (not global `rdfs:domain`/`rdfs:range`)
- SKOS concepts include `skos:prefLabel`, `skos:definition`, `skos:inScheme`

No external dependencies are added. All terms use existing ontology patterns and imported vocabularies (DQV, SKOS, IAO, DwC).

