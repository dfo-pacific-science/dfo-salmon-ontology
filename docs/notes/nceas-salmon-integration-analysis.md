# NCEAS Salmon Ontology Integration Analysis

**Generated:** 2025-01-24  
**Purpose:** Analyze NCEAS Salmon ontology to inform DFO superclass decisions and avoid reinventing domain hierarchies

## Executive Summary

**Key Finding:** The NCEAS Salmon ontology provides a well-established domain hierarchy that should inform your superclass decisions. Rather than creating new hierarchies, you should align with existing NCEAS patterns where appropriate.

**Integration Strategy:** Use NCEAS classes as superclasses for your DFO classes where there's semantic alignment, while maintaining your domain-specific focus on stock assessment and management.

## NCEAS Salmon Ontology Overview

### Domain Scope

- **Primary Focus:** General salmon biology, ecology, and fisheries
- **Geographic Scope:** Alaska and Pacific salmon (SASAP data portal)
- **Temporal Scope:** Historical and current data
- **Institutional Context:** NCEAS (National Center for Ecological Analysis and Synthesis)

### Key Domain Hierarchies

#### 1. Measurement Types

**Root Class:** `odo:SALMON_00000127` - "Fish length measurement type"

- **Subclasses:** Fork length, Total length, Standard length, etc.
- **Superclass:** `odo:SALMON_00000167` (measurement type)

#### 2. Fishery Types

**Root Class:** `odo:SALMON_00000137` - "Fishery type"

- **Subclasses:** Commercial fishery, Recreational fishery, Subsistence fishery, etc.
- **No explicit superclass** (root class)

#### 3. Fishing Gear/Equipment

**Root Class:** `odo:SALMON_00000142` - "Equipment which is used to harvest aquatic resources"

- **Subclasses:** Fish wheel, Weir, Pot, Troll, Netting, Hand collection, etc.
- **No explicit superclass** (root class)

#### 4. Water Bodies

**Root Class:** `odo:SALMON_00000125` - "Water body"

- **Subclasses:** Lotic water body, Lentic water body, Inlet, etc.
- **Superclass:** `odo:SALMON_00000202` (environmental feature)

#### 5. Age Classes and Recruitment

**Root Class:** `odo:SALMON_00000407` - "Age class"

- **Subclasses:** Age class 0.x recruits, Age class 1.x recruits, etc.
- **Pattern:** Detailed age-specific recruitment classes

## Integration Recommendations for DFO Classes

### Category 1: Direct NCEAS Alignment (High Priority)

#### Measurement Classes → NCEAS Measurement Hierarchy

**`dfo:SizeAtAge`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf odo:SALMON_00000127` (Fish length measurement type)
- **Rationale:** Size at age is a fish measurement type
- **Impact:** High - aligns with established measurement hierarchy

**`dfo:GeneticDiversity`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf odo:SALMON_00000167` (measurement type)
- **Rationale:** Genetic diversity is a measurable biological property
- **Impact:** Medium - creates biological measurement hierarchy

**`dfo:Fecundity`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf odo:SALMON_00000167` (measurement type)
- **Rationale:** Fecundity is a measurable biological property
- **Impact:** Medium - creates biological measurement hierarchy

#### Fishery Classes → NCEAS Fishery Hierarchy

**`dfo:MixedStockFishery`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf odo:SALMON_00000137` (Fishery type)
- **Rationale:** Mixed stock fishery is a type of fishery
- **Impact:** High - aligns with established fishery hierarchy

#### Age/Recruitment Classes → NCEAS Age Class Hierarchy

**`dfo:AgeAtMaturity`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf odo:SALMON_00000407` (Age class)
- **Rationale:** Age at maturity is related to age class concepts
- **Impact:** Medium - aligns with age class hierarchy

**`dfo:Recruitment`**

- **Current:** Root class
- **Recommendation:** Consider relationship to NCEAS age class recruits
- **Rationale:** Recruitment is conceptually related to age class recruitment
- **Impact:** Medium - potential alignment with recruitment concepts

### Category 2: NCEAS-Informed BFO Grounding (Medium Priority)

#### Process Classes → BFO with NCEAS Context

**`dfo:Enhancement`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015` (process)
- **NCEAS Context:** Consider relationship to hatchery operations
- **Impact:** High - enables process-based reasoning

**`dfo:HatcheryEnhancement`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015` (process)
- **NCEAS Context:** Hatchery operations are processes
- **Impact:** High - enables process-based reasoning

#### Material Entity Classes → BFO with NCEAS Context

**`dfo:Hatchery`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000040` (material entity)
- **NCEAS Context:** Hatcheries are physical facilities
- **Impact:** High - enables material entity reasoning

### Category 3: DFO-Specific Classes (Keep as Root)

#### Stock Assessment Specific Classes

These are DFO-specific and don't have NCEAS equivalents:

- `dfo:Escapement` - DFO-specific stock assessment concept
- `dfo:SpawnerAbundance` - DFO-specific stock assessment concept
- `dfo:Catch` - DFO-specific stock assessment concept
- `dfo:FishingEffort` - DFO-specific stock assessment concept
- `dfo:FishingMortality` - DFO-specific stock assessment concept
- `dfo:RemovalRate` - DFO-specific stock assessment concept

#### Management/Policy Classes

These are DFO-specific management concepts:

- `dfo:TotalAllowableCatch` - DFO management concept
- `dfo:MaximumSustainableYield` - DFO management concept
- `dfo:UMSY` - DFO management concept
- `dfo:SMSY` - DFO management concept
- `dfo:Sgen` - DFO management concept
- `dfo:ReferencePoint` - DFO management concept
- `dfo:FisheryReferencePoint` - DFO management concept
- `dfo:OperationalControlPoint` - DFO management concept
- `dfo:RemovalReference` - DFO management concept

#### Origin/Type Classes

These are DFO-specific origin concepts:

- `dfo:HatcheryOrigin` - DFO-specific origin type
- `dfo:NaturalOrigin` - DFO-specific origin type
- `dfo:Wild` - DFO-specific origin type

## Revised Implementation Plan

### Phase 1: NCEAS Alignment (8 classes)

**Priority 1: Measurement Hierarchy (3 classes)**

- `dfo:SizeAtAge` → `odo:SALMON_00000127` (Fish length measurement type)
- `dfo:GeneticDiversity` → `odo:SALMON_00000167` (measurement type)
- `dfo:Fecundity` → `odo:SALMON_00000167` (measurement type)

**Priority 2: Fishery Hierarchy (1 class)**

- `dfo:MixedStockFishery` → `odo:SALMON_00000137` (Fishery type)

**Priority 3: Age Class Hierarchy (1 class)**

- `dfo:AgeAtMaturity` → `odo:SALMON_00000407` (Age class)

**Priority 4: Recruitment Relationship (1 class)**

- `dfo:Recruitment` → Consider relationship to NCEAS age class recruits

### Phase 2: BFO Grounding with NCEAS Context (15 classes)

**Process Classes (6 classes)**

- `dfo:Enhancement` → `bfo:0000015`
- `dfo:HatcheryEnhancement` → `bfo:0000015`
- `dfo:EquilibriumTradeoffAnalysis` → `bfo:0000015`
- `dfo:LifeCycleModel` → `bfo:0000015`
- `dfo:RunReconstructionModel` → `bfo:0000015`
- `dfo:StockRecruitmentRelationship` → `bfo:0000015`

**Material Entity Classes (3 classes)**

- `dfo:Hatchery` → `bfo:0000040`
- `dfo:IndicatorPopulation` → `bfo:0000040`
- `dfo:IndicatorStream` → `bfo:0000040`

**Information Entity Classes (6 classes)**

- `dfo:HarvestAdvice` → `bfo:0000031`
- `dfo:Protocol` → `bfo:0000031`
- `dfo:PrecautionaryApproach` → `bfo:0000031`
- `dfo:RebuildingPlan` → `bfo:0000031`

### Phase 3: DFO-Specific Root Classes (29 classes)

**Stock Assessment Classes (6 classes)**

- `dfo:Escapement`, `dfo:SpawnerAbundance`, `dfo:Catch`, `dfo:FishingEffort`, `dfo:FishingMortality`, `dfo:RemovalRate`

**Management/Policy Classes (9 classes)**

- `dfo:TotalAllowableCatch`, `dfo:MaximumSustainableYield`, `dfo:UMSY`, `dfo:SMSY`, `dfo:Sgen`, `dfo:ReferencePoint`, `dfo:FisheryReferencePoint`, `dfo:OperationalControlPoint`, `dfo:RemovalReference`

**Origin/Type Classes (3 classes)**

- `dfo:HatcheryOrigin`, `dfo:NaturalOrigin`, `dfo:Wild`

**Other DFO-Specific Classes (11 classes)**

- `dfo:BroodYear`, `dfo:DesignatableUnit`, `dfo:CUBenchmarks`, `dfo:IndexBased`, `dfo:KobePlot`, `dfo:PercentHatcheryOriginSpawners`, `dfo:RebuildingTarget`, `dfo:GSIRun`, `dfo:ReportingUnit`, `dfo:Assay`, `dfo:MarkerPanel`, `dfo:EscapementMethod`

## Benefits of NCEAS Integration

### 1. Avoid Reinventing Domain Hierarchies

- Leverage established measurement, fishery, and age class hierarchies
- Maintain consistency with broader salmon domain knowledge
- Reduce maintenance burden

### 2. Improve Interoperability

- Enable cross-ontology reasoning and queries
- Support data integration between DFO and NCEAS datasets
- Facilitate knowledge sharing across salmon research communities

### 3. Enhance Semantic Richness

- Connect DFO-specific concepts to broader domain knowledge
- Enable more sophisticated reasoning and inference
- Support better data discovery and integration

## Risks and Mitigation

### 1. Dependency on External Ontology

- **Risk:** Changes to NCEAS ontology could affect DFO ontology
- **Mitigation:** Document dependencies and monitor NCEAS changes

### 2. Semantic Misalignment

- **Risk:** NCEAS classes might not perfectly match DFO concepts
- **Mitigation:** Careful review of class definitions and relationships

### 3. Maintenance Complexity

- **Risk:** More complex ontology with external dependencies
- **Mitigation:** Clear documentation of relationships and rationale

## Next Steps

1. **Review NCEAS Class Definitions:** Examine the specific definitions of proposed superclasses
2. **Validate Semantic Alignment:** Ensure DFO classes truly fit NCEAS hierarchies
3. **Implement Phase 1:** Start with clear measurement and fishery alignments
4. **Test Integration:** Verify reasoning and query capabilities
5. **Document Relationships:** Update CONVENTIONS.md with integration patterns

## Conclusion

The NCEAS Salmon ontology provides valuable domain hierarchies that should inform your superclass decisions. By aligning with NCEAS where appropriate, you can avoid reinventing domain knowledge while maintaining your DFO-specific focus on stock assessment and management.

**Key Recommendation:** Prioritize NCEAS alignment for measurement, fishery, and age class concepts, while keeping DFO-specific stock assessment and management concepts as root classes.

---

**Note:** This analysis provides integration recommendations only - implementation should include careful review of NCEAS class definitions and validation of semantic alignment.
