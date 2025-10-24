# DFO Salmon Ontology - Detailed Superclass Analysis

**Generated:** 2025-01-24  
**Purpose:** Detailed analysis of 52 classes without superclasses to provide evidence-based recommendations

## Executive Summary

**ROBOT reports missing superclasses:** 52 classes  
**Analysis approach:** Evidence-based recommendations, not mandates  
**Key finding:** OWL 2 and OBO Foundry do not require all classes to have superclasses

## Complete List of Classes Without Superclasses

The following 52 DFO classes lack explicit superclass relationships:

1. `dfo:AgeAtMaturity`
2. `dfo:BroodYear`
3. `dfo:Catch`
4. `dfo:DesignatableUnit`
5. `dfo:CUBenchmarks`
6. `dfo:Enhancement`
7. `dfo:Escapement`
8. `dfo:EquilibriumTradeoffAnalysis`
9. `dfo:Fecundity`
10. `dfo:FisheryReferencePoint`
11. `dfo:FishingEffort`
12. `dfo:FishingMortality`
13. `dfo:GeneticDiversity`
14. `dfo:HarvestAdvice`
15. `dfo:Hatchery`
16. `dfo:HatcheryEnhancement`
17. `dfo:HatcheryOrigin`
18. `dfo:HatcheryProduction`
19. `dfo:IndexBased`
20. `dfo:Indicator`
21. `dfo:IndicatorPopulation`
22. `dfo:IndicatorStream`
23. `dfo:KobePlot`
24. `dfo:LifeCycleModel`
25. `dfo:MixedStockFishery`
26. `dfo:MaximumSustainableYield`
27. `dfo:NaturalOrigin`
28. `dfo:OperationalControlPoint`
29. `dfo:PercentHatcheryOriginSpawners`
30. `dfo:PrecautionaryApproach`
31. `dfo:RebuildingPlan`
32. `dfo:RebuildingTarget`
33. `dfo:Recruitment`
34. `dfo:ReferencePoint`
35. `dfo:RemovalRate`
36. `dfo:RemovalReference`
37. `dfo:RunReconstructionModel`
38. `dfo:SizeAtAge`
39. `dfo:Sgen`
40. `dfo:SMSY`
41. `dfo:SpawnerAbundance`
42. `dfo:StockRecruitmentRelationship`
43. `dfo:TotalAllowableCatch`
44. `dfo:UMSY`
45. `dfo:Wild`
46. `dfo:GSIRun`
47. `dfo:ReportingUnit`
48. `dfo:Assay`
49. `dfo:MarkerPanel`
50. `dfo:Protocol`
51. `dfo:EscapementMethod`

## Per-Class Analysis and Recommendations

### Category 1: BFO Grounding Candidates (High Priority)

#### Process Classes → `bfo:0000015` (process)

**`dfo:Enhancement`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Enhancement is a process that occurs over time
- **Impact:** High - enables process-based reasoning

**`dfo:HatcheryEnhancement`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Hatchery enhancement is a specific type of process
- **Impact:** High - enables process-based reasoning

**`dfo:EquilibriumTradeoffAnalysis`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Analysis is a process that occurs over time
- **Impact:** Medium - enables process-based reasoning

**`dfo:LifeCycleModel`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Modeling is a process
- **Impact:** Medium - enables process-based reasoning

**`dfo:RunReconstructionModel`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Run reconstruction is a modeling process
- **Impact:** Medium - enables process-based reasoning

**`dfo:StockRecruitmentRelationship`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000015`
- **Rationale:** Relationship modeling is a process
- **Impact:** Medium - enables process-based reasoning

#### Material Entity Classes → `bfo:0000040` (material entity)

**`dfo:Hatchery`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000040`
- **Rationale:** Hatchery is a physical facility
- **Impact:** High - enables material entity reasoning

**`dfo:IndicatorPopulation`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000040`
- **Rationale:** Population is a material entity
- **Impact:** High - enables material entity reasoning

**`dfo:IndicatorStream`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000040`
- **Rationale:** Stream is a physical entity
- **Impact:** High - enables material entity reasoning

#### Information Entity Classes → `bfo:0000031` (generically dependent continuant)

**`dfo:HarvestAdvice`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000031`
- **Rationale:** Advice is information content
- **Impact:** High - enables information entity reasoning

**`dfo:Protocol`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000031`
- **Rationale:** Protocol is information content
- **Impact:** High - enables information entity reasoning

**`dfo:PrecautionaryApproach`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000031`
- **Rationale:** Approach is information content
- **Impact:** Medium - enables information entity reasoning

**`dfo:RebuildingPlan`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf bfo:0000031`
- **Rationale:** Plan is information content
- **Impact:** Medium - enables information entity reasoning

### Category 2: Domain Hierarchy Candidates (Medium Priority)

#### Measurement/Indicator Classes

**`dfo:Indicator`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ObservedRateOrAbundance`
- **Rationale:** Indicators are types of measurements
- **Impact:** High - creates clear measurement hierarchy

**`dfo:ReferencePoint`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** Reference points are target/limit specifications
- **Impact:** High - creates clear target hierarchy

**`dfo:FisheryReferencePoint`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ReferencePoint`
- **Rationale:** Fishery reference points are specific types of reference points
- **Impact:** Medium - creates reference point hierarchy

**`dfo:OperationalControlPoint`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ReferencePoint`
- **Rationale:** Operational control points are reference points
- **Impact:** Medium - creates reference point hierarchy

**`dfo:RemovalReference`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ReferencePoint`
- **Rationale:** Removal references are reference points
- **Impact:** Medium - creates reference point hierarchy

#### Management/Policy Classes

**`dfo:TotalAllowableCatch`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** TAC is a target/limit specification
- **Impact:** High - creates clear target hierarchy

**`dfo:MaximumSustainableYield`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** MSY is a target specification
- **Impact:** High - creates clear target hierarchy

**`dfo:UMSY`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** UMSY is a target specification
- **Impact:** High - creates clear target hierarchy

**`dfo:SMSY`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** SMSY is a target specification
- **Impact:** High - creates clear target hierarchy

**`dfo:Sgen`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:TargetOrLimitRateOrAbundance`
- **Rationale:** Sgen is a target specification
- **Impact:** High - creates clear target hierarchy

#### Biological/Genetic Classes

**`dfo:GeneticDiversity`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ObservedRateOrAbundance`
- **Rationale:** Genetic diversity is a measurable biological property
- **Impact:** Medium - creates biological measurement hierarchy

**`dfo:Fecundity`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ObservedRateOrAbundance`
- **Rationale:** Fecundity is a measurable biological property
- **Impact:** Medium - creates biological measurement hierarchy

**`dfo:SizeAtAge`**

- **Current:** Root class
- **Recommendation:** Add `rdfs:subClassOf dfo:ObservedRateOrAbundance`
- **Rationale:** Size at age is a measurable biological property
- **Impact:** Medium - creates biological measurement hierarchy

### Category 3: Classes That Should Remain Root (Low Priority)

#### Fundamental Domain Concepts

**`dfo:Escapement`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:Recruitment`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:SpawnerAbundance`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:Catch`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:FishingEffort`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:FishingMortality`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:RemovalRate`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Fundamental domain concept, no clear superclass
- **Impact:** None - appropriate as root

#### Origin/Type Classes

**`dfo:HatcheryOrigin`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Origin type, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:NaturalOrigin`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Origin type, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:Wild`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Origin type, no clear superclass
- **Impact:** None - appropriate as root

#### Specific Domain Classes

**`dfo:AgeAtMaturity`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Specific biological concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:BroodYear`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Specific temporal concept, no clear superclass
- **Impact:** None - appropriate as root

**`dfo:DesignatableUnit`**

- **Current:** Root class
- **Recommendation:** Keep as root class
- **Rationale:** Specific management concept, no clear superclass
- **Impact:** None - appropriate as root

## Implementation Recommendations

### Phase 1: High-Impact BFO Grounding (15 classes)

**Priority 1: Process Classes (6 classes)**

- `dfo:Enhancement` → `bfo:0000015`
- `dfo:HatcheryEnhancement` → `bfo:0000015`
- `dfo:EquilibriumTradeoffAnalysis` → `bfo:0000015`
- `dfo:LifeCycleModel` → `bfo:0000015`
- `dfo:RunReconstructionModel` → `bfo:0000015`
- `dfo:StockRecruitmentRelationship` → `bfo:0000015`

**Priority 2: Material Entity Classes (3 classes)**

- `dfo:Hatchery` → `bfo:0000040`
- `dfo:IndicatorPopulation` → `bfo:0000040`
- `dfo:IndicatorStream` → `bfo:0000040`

**Priority 3: Information Entity Classes (6 classes)**

- `dfo:HarvestAdvice` → `bfo:0000031`
- `dfo:Protocol` → `bfo:0000031`
- `dfo:PrecautionaryApproach` → `bfo:0000031`
- `dfo:RebuildingPlan` → `bfo:0000031`

### Phase 2: Domain Hierarchy (15 classes)

**Priority 1: Measurement Hierarchy (5 classes)**

- `dfo:Indicator` → `dfo:ObservedRateOrAbundance`
- `dfo:ReferencePoint` → `dfo:TargetOrLimitRateOrAbundance`
- `dfo:FisheryReferencePoint` → `dfo:ReferencePoint`
- `dfo:OperationalControlPoint` → `dfo:ReferencePoint`
- `dfo:RemovalReference` → `dfo:ReferencePoint`

**Priority 2: Target/Limit Hierarchy (5 classes)**

- `dfo:TotalAllowableCatch` → `dfo:TargetOrLimitRateOrAbundance`
- `dfo:MaximumSustainableYield` → `dfo:TargetOrLimitRateOrAbundance`
- `dfo:UMSY` → `dfo:TargetOrLimitRateOrAbundance`
- `dfo:SMSY` → `dfo:TargetOrLimitRateOrAbundance`
- `dfo:Sgen` → `dfo:TargetOrLimitRateOrAbundance`

**Priority 3: Biological Measurement Hierarchy (3 classes)**

- `dfo:GeneticDiversity` → `dfo:ObservedRateOrAbundance`
- `dfo:Fecundity` → `dfo:ObservedRateOrAbundance`
- `dfo:SizeAtAge` → `dfo:ObservedRateOrAbundance`

### Phase 3: Keep as Root Classes (22 classes)

**Fundamental Domain Concepts (7 classes)**

- `dfo:Escapement`, `dfo:Recruitment`, `dfo:SpawnerAbundance`, `dfo:Catch`, `dfo:FishingEffort`, `dfo:FishingMortality`, `dfo:RemovalRate`

**Origin/Type Classes (3 classes)**

- `dfo:HatcheryOrigin`, `dfo:NaturalOrigin`, `dfo:Wild`

**Specific Domain Classes (12 classes)**

- `dfo:AgeAtMaturity`, `dfo:BroodYear`, `dfo:DesignatableUnit`, `dfo:CUBenchmarks`, `dfo:IndexBased`, `dfo:KobePlot`, `dfo:MixedStockFishery`, `dfo:PercentHatcheryOriginSpawners`, `dfo:RebuildingTarget`, `dfo:GSIRun`, `dfo:ReportingUnit`, `dfo:Assay`, `dfo:MarkerPanel`, `dfo:EscapementMethod`

## Expected Outcomes

### Benefits of Implementation

1. **Enhanced Reasoning:** 30 classes will have clear BFO grounding or domain hierarchy
2. **Semantic Clarity:** Clear relationships between related concepts
3. **Domain Alignment:** Better integration with domain knowledge
4. **BFO Compliance:** Improved alignment with upper ontology

### Risks and Mitigation

1. **Artificial Relationships:** Avoid forcing weak "is-a" relationships
2. **Logical Inconsistencies:** Test with reasoners after each change
3. **Domain Misalignment:** Get domain expert review before implementation
4. **Maintenance Burden:** Document rationale for each superclass addition

## Conclusion

The analysis reveals that 30 of the 52 classes would benefit from superclasses, while 22 should remain as root classes. The recommendations focus on semantic clarity, logical consistency, and domain alignment rather than arbitrary hierarchy completeness.

**Next Steps:**

1. Get domain expert review of recommendations
2. Implement Phase 1 (BFO grounding) first
3. Test with reasoners after each phase
4. Document rationale for each superclass addition
5. Update CONVENTIONS.md with hierarchy patterns

---

**Note:** This analysis provides evidence-based recommendations only - no superclasses will be added without domain expert review and validation.
