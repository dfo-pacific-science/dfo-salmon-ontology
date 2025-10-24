# NCEAS Salmon Ontology Integration Analysis

**Generated:** 2025-01-24  
**Purpose:** Comprehensive analysis of NCEAS Salmon Ontology integration with DFO Salmon Ontology  
**Status:** Draft for Review

## Executive Summary

The NCEAS Salmon Ontology provides valuable domain hierarchies that should inform DFO superclass decisions, but full integration is not recommended. Instead, a **hybrid approach** should be adopted: align with NCEAS for general domain concepts while maintaining DFO-specific concepts locally.

**Key Recommendation:** Prioritize NCEAS alignment for measurement, fishery, and age class concepts, while keeping DFO-specific stock assessment and management concepts as root classes.

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Key Differences Between Ontologies](#2-key-differences-between-ontologies)
3. [Integration Opportunities](#3-integration-opportunities)
4. [Heuristics for Contribution Decisions](#4-heuristics-for-contribution-decisions)
5. [Assessment of NCEAS as Cross-Organizational Domain Ontology](#5-assessment-of-nceas-as-cross-organizational-domain-ontology)
6. [Implementation Plan](#6-implementation-plan)
7. [Benefits and Risks Analysis](#7-benefits-and-risks-analysis)
8. [Specific Integration Recommendations](#8-specific-integration-recommendations)
9. [Conclusion and Next Steps](#9-conclusion-and-next-steps)

---

## 1. Current State Analysis

### 1.1 DFO Ontology Current State

**Architecture:**

- **Hybrid OWL+SKOS approach**: Uses SKOS for controlled vocabularies (methods, criteria) and OWL for formal relationships
- **BFO grounding**: Uses MIREOT to import BFO classes (process, material entity, generically dependent continuant)
- **Darwin Core alignment**: Classes extend Darwin Core classes (Event, Organism, etc.)
- **Domain focus**: Stock assessment, genetics, management - very DFO-specific

**Import Strategy:**

- **BFO**: MIREOT (3 classes) - process, material entity, generically dependent continuant
- **IAO**: MIREOT (4 classes) - measurement datum, value specification, information content entity, directive information entity
- **DQV**: MIREOT (5 terms) - Dimension, QualityAnnotation, inDimension, Metric, Category
- **PROV-O**: Prefix only (~6 properties) - wasGeneratedBy, wasDerivedFrom, used, wasAttributedTo, etc.
- **RO**: Prefix only (alignment via rdfs:seeAlso) - has_member, member_of
- **SKOS**: Prefix only (extensive) - Concept, ConceptScheme, prefLabel, definition, etc.
- **DwC**: Prefix only (extensive) - Event, Organism, MeasurementOrFact, etc.

**Current NCEAS Alignment:**

- `dfo:SizeAtAge` → already subclasses `odo:SALMON_00000167` (measurement type) ✅
- `dfo:AgeAtMaturity` → already subclasses `odo:SALMON_00000407` (age class) ✅
- `dfo:PreTerminalFishery` and `dfo:TerminalFishery` → already subclass `odo:SALMON_00000137` (fishery type) ✅

### 1.2 NCEAS Ontology Current State

**Domain Scope:**

- **Primary Focus:** General salmon biology, ecology, and fisheries
- **Geographic Scope:** Alaska and Pacific salmon (SASAP data portal)
- **Temporal Scope:** Historical and current data
- **Institutional Context:** NCEAS (National Center for Ecological Analysis and Synthesis)

**Key Domain Hierarchies:**

1. **Measurement Types**: `odo:SALMON_00000127` (Fish length measurement type) with subclasses like Fork length, Total length, Standard length
2. **Fishery Types**: `odo:SALMON_00000137` (Fishery type) with subclasses like Commercial fishery, Recreational fishery, Subsistence fishery
3. **Fishing Gear/Equipment**: `odo:SALMON_00000142` (Equipment which is used to harvest aquatic resources) with subclasses like Fish wheel, Weir, Pot, Troll, Netting, Hand collection
4. **Water Bodies**: `odo:SALMON_00000125` (Water body) with subclasses like Lotic water body, Lentic water body, Inlet
5. **Age Classes and Recruitment**: `odo:SALMON_00000407` (Age class) with detailed age-specific recruitment classes

---

## 2. Key Differences Between Ontologies

### 2.1 Scope and Purpose

| Aspect         | NCEAS Salmon Ontology     | DFO Salmon Ontology     |
| -------------- | ------------------------- | ----------------------- |
| **Scope**      | General salmon domain     | Organization-specific   |
| **Focus**      | Academic research         | Government management   |
| **Geographic** | Alaska and Pacific salmon | Canadian Pacific salmon |
| **Purpose**    | Domain knowledge          | Operational management  |
| **Users**      | Research community        | DFO staff and partners  |

### 2.2 Import Strategies

| Ontology   | NCEAS Approach               | DFO Approach                |
| ---------- | ---------------------------- | --------------------------- |
| **BFO**    | Unknown (likely full import) | MIREOT (3 classes)          |
| **IAO**    | Unknown (likely full import) | MIREOT (4 classes)          |
| **PROV-O** | Unknown                      | Prefix only (~6 properties) |
| **SKOS**   | Unknown                      | Prefix only (extensive)     |
| **DwC**    | Unknown                      | Prefix only (extensive)     |

### 2.3 Modeling Approach

| Aspect           | NCEAS                         | DFO                                |
| ---------------- | ----------------------------- | ---------------------------------- |
| **Architecture** | Comprehensive domain ontology | Hybrid OWL+SKOS approach           |
| **Size**         | Large (comprehensive)         | Lightweight, focused               |
| **Maintenance**  | Centralized                   | Distributed with strategic imports |
| **Control**      | NCEAS institution             | DFO organization                   |

---

## 3. Integration Opportunities

### 3.1 OBVIOUS INTEGRATION (High Priority)

#### 3.1.1 Measurement Hierarchy Alignment

**Current State:**

- `dfo:SizeAtAge` → already subclasses `odo:SALMON_00000167` (measurement type) ✅

**Recommended Additions:**

- `dfo:GeneticDiversity` → `odo:SALMON_00000167` (measurement type)
- `dfo:Fecundity` → `odo:SALMON_00000167` (measurement type)

**Rationale:**

- These are clearly biological measurements that fit NCEAS measurement hierarchy
- Genetic diversity and fecundity are standard biological properties measured across organizations
- Alignment enables cross-ontology reasoning and queries

**Implementation:**

```turtle
dfo:GeneticDiversity a owl:Class ;
  rdfs:label "Genetic diversity"@en ;
  rdfs:comment "The variation at the level of individual genes, and provides a mechanism for populations to adapt to their ever-changing environment."@en ;
  rdfs:subClassOf odo:SALMON_00000167 ; # measurement type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:Fecundity a owl:Class ;
  rdfs:label "Fecundity"@en ;
  rdfs:comment "The number of eggs an animal produces during each reproductive cycle; the potential reproductive capacity of an organism or population."@en ;
  rdfs:subClassOf odo:SALMON_00000167 ; # measurement type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

#### 3.1.2 Fishery Hierarchy Alignment

**Current State:**

- `dfo:PreTerminalFishery` and `dfo:TerminalFishery` → already subclass `odo:SALMON_00000137` (fishery type) ✅

**Recommended Addition:**

- `dfo:MixedStockFishery` → `odo:SALMON_00000137` (Fishery type)

**Rationale:**

- Mixed stock fishery is clearly a type of fishery
- Fits established NCEAS fishery hierarchy
- Enables alignment with broader fishery classification

**Implementation:**

```turtle
dfo:MixedStockFishery a owl:Class ;
  rdfs:label "Mixed-stock fishery"@en ;
  rdfs:comment "Individual fish in different stocks might mix or migrate between different areas. Also referred to as 'multispecies fishery'."@en ;
  rdfs:subClassOf odo:SALMON_00000137 ; # Fishery type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

#### 3.1.3 Age Class Hierarchy Alignment

**Current State:**

- `dfo:AgeAtMaturity` → already subclasses `odo:SALMON_00000407` (age class) ✅

**Recommended Addition:**

- `dfo:Recruitment` → Consider relationship to NCEAS age class recruits

**Rationale:**

- Recruitment is conceptually related to age class recruitment
- Enables alignment with established age class hierarchy
- Supports cross-ontology reasoning about recruitment processes

**Implementation (Requires Analysis):**

```turtle
# Need to analyze semantic alignment with NCEAS age class recruits
# Consider: Is recruitment a process, a measurement, or an age class concept?
```

### 3.2 DISCUSSION WARRANTED (Medium Priority)

#### 3.2.1 Process Classes → BFO with NCEAS Context

**Classes to Consider:**

- `dfo:Enhancement` → `bfo:0000015` (process)
- `dfo:HatcheryEnhancement` → `bfo:0000015` (process)
- `dfo:EquilibriumTradeoffAnalysis` → `bfo:0000015` (process)
- `dfo:LifeCycleModel` → `bfo:0000015` (process)
- `dfo:RunReconstructionModel` → `bfo:0000015` (process)
- `dfo:StockRecruitmentRelationship` → `bfo:0000015` (process)

**Discussion Points:**

- These are processes but also DFO-specific management concepts
- Need to balance BFO grounding with organizational specificity
- Consider relationship to NCEAS hatchery operations

#### 3.2.2 Material Entity Classes → BFO with NCEAS Context

**Classes to Consider:**

- `dfo:Hatchery` → `bfo:0000040` (material entity)
- `dfo:IndicatorPopulation` → `bfo:0000040` (material entity)
- `dfo:IndicatorStream` → `bfo:0000040` (material entity)

**Discussion Points:**

- These are material entities but also DFO-specific concepts
- Hatcheries are physical facilities (material entities)
- Indicator populations and streams are DFO-specific management concepts

#### 3.2.3 Information Entity Classes → BFO with NCEAS Context

**Classes to Consider:**

- `dfo:HarvestAdvice` → `bfo:0000031` (generically dependent continuant)
- `dfo:Protocol` → `bfo:0000031` (generically dependent continuant)
- `dfo:PrecautionaryApproach` → `bfo:0000031` (generically dependent continuant)
- `dfo:RebuildingPlan` → `bfo:0000031` (generically dependent continuant)

**Discussion Points:**

- These are information entities but also DFO-specific policy concepts
- Need to balance BFO grounding with organizational specificity
- Consider relationship to NCEAS information concepts

### 3.3 KEEP AS DFO-SPECIFIC (Low Priority for NCEAS Integration)

#### 3.3.1 Stock Assessment Classes

- `dfo:Escapement` - DFO-specific stock assessment concept
- `dfo:SpawnerAbundance` - DFO-specific stock assessment concept
- `dfo:Catch` - DFO-specific stock assessment concept
- `dfo:FishingEffort` - DFO-specific stock assessment concept
- `dfo:FishingMortality` - DFO-specific stock assessment concept
- `dfo:RemovalRate` - DFO-specific stock assessment concept

#### 3.3.2 Management/Policy Classes

- `dfo:TotalAllowableCatch` - DFO management concept
- `dfo:MaximumSustainableYield` - DFO management concept
- `dfo:UMSY` - DFO management concept
- `dfo:SMSY` - DFO management concept
- `dfo:Sgen` - DFO management concept
- `dfo:ReferencePoint` - DFO management concept
- `dfo:FisheryReferencePoint` - DFO management concept
- `dfo:OperationalControlPoint` - DFO management concept
- `dfo:RemovalReference` - DFO management concept

#### 3.3.3 Origin/Type Classes

- `dfo:HatcheryOrigin` - DFO-specific origin type
- `dfo:NaturalOrigin` - DFO-specific origin type
- `dfo:Wild` - DFO-specific origin type

#### 3.3.4 Other DFO-Specific Classes

- `dfo:BroodYear` - DFO-specific temporal concept
- `dfo:DesignatableUnit` - DFO-specific conservation concept
- `dfo:CUBenchmarks` - DFO-specific management concept
- `dfo:IndexBased` - DFO-specific management concept
- `dfo:KobePlot` - DFO-specific visualization concept
- `dfo:PercentHatcheryOriginSpawners` - DFO-specific measurement concept
- `dfo:RebuildingTarget` - DFO-specific management concept
- `dfo:GSIRun` - DFO-specific genetics concept
- `dfo:ReportingUnit` - DFO-specific genetics concept
- `dfo:Assay` - DFO-specific genetics concept
- `dfo:MarkerPanel` - DFO-specific genetics concept
- `dfo:EscapementMethod` - DFO-specific methodology concept

---

## 4. Heuristics for Contribution Decisions

### 4.1 CONTRIBUTE TO NCEAS (Domain Ontology) IF:

#### 4.1.1 Multi-Organizational Relevance

- Concept is used by multiple organizations (DFO, NOAA, state agencies, research institutions)
- Concept has broad applicability across different management contexts
- Concept represents a standard that multiple organizations should follow

**Examples:**

- General measurement types (genetic diversity, fecundity)
- Standard fishery types (commercial, recreational, subsistence)
- Common equipment types (sonar, weir, net)
- Environmental concepts (water bodies, habitats)

#### 4.1.2 Scientific Consensus

- Concept has broad scientific acceptance and standardized definitions
- Concept is based on peer-reviewed research and established methodologies
- Concept represents a widely-accepted scientific standard

**Examples:**

- Biological measurement types
- Standard survey methods
- Common analytical approaches
- Established classification schemes

#### 4.1.3 Domain Generality

- Concept applies to salmon biology/ecology/fisheries broadly, not just management
- Concept is not specific to any particular organization's policies or procedures
- Concept represents general domain knowledge

**Examples:**

- General biological concepts
- Common ecological relationships
- Standard environmental classifications
- Widely-used methodologies

#### 4.1.4 Methodological Standards

- Concept represents a widely-used method or protocol
- Concept is based on established best practices
- Concept represents a standard that should be consistent across organizations

**Examples:**

- Standard survey protocols
- Common analytical methods
- Established quality control procedures
- Widely-used data collection standards

#### 4.1.5 Environmental Concepts

- Concept relates to habitats, water bodies, or environmental conditions
- Concept represents environmental factors that affect salmon across regions
- Concept is not specific to any particular management approach

**Examples:**

- Water body types (lotic, lentic, inlet)
- Habitat classifications
- Environmental quality indicators
- Climate-related concepts

#### 4.1.6 Biological Measurements

- Concept represents a standard biological measurement type
- Concept is used consistently across organizations
- Concept represents a measurable biological property

**Examples:**

- Fish length measurements
- Age class classifications
- Biological productivity indicators
- Standard biological parameters

#### 4.1.7 Equipment and Gear

- Concept represents fishing equipment or survey gear used across organizations
- Concept represents standard tools and technologies
- Concept is not specific to any particular organization's procedures

**Examples:**

- Sonar equipment
- Weir systems
- Net types
- Survey gear

### 4.2 KEEP IN DFO (Organization-Specific Ontology) IF:

#### 4.2.1 Organizational Specificity

- Concept is specific to DFO's management framework or policies
- Concept represents DFO's unique approach to salmon management
- Concept is not applicable to other organizations

**Examples:**

- DFO-specific management frameworks
- DFO-specific assessment methods
- DFO-specific reporting requirements
- DFO-specific organizational structures

#### 4.2.2 Canadian Context

- Concept is specific to Canadian regulations, policies, or management approaches
- Concept represents Canadian legal or regulatory requirements
- Concept is not applicable to other countries

**Examples:**

- Canadian fisheries regulations
- COSEWIC status categories
- Canadian environmental policies
- Canadian management frameworks

#### 4.2.3 DFO Protocols

- Concept represents DFO-specific procedures or methodologies
- Concept is based on DFO's internal standards and practices
- Concept is not used by other organizations

**Examples:**

- DFO survey protocols
- DFO data collection standards
- DFO quality control procedures
- DFO reporting formats

#### 4.2.4 Management Hierarchies

- Concept represents DFO's specific organizational structure
- Concept is based on DFO's management approach
- Concept is not applicable to other organizations

**Examples:**

- Management Units (MUs)
- Conservation Units (CUs)
- Stock Management Units (SMUs)
- DFO organizational structures

#### 4.2.5 Policy Frameworks

- Concept relates to DFO-specific policies
- Concept represents DFO's policy approach
- Concept is not applicable to other organizations

**Examples:**

- Wild Salmon Policy
- Precautionary Approach
- DFO management policies
- DFO conservation frameworks

#### 4.2.6 Assessment Methods

- Concept represents DFO-specific stock assessment approaches
- Concept is based on DFO's assessment methodologies
- Concept is not used by other organizations

**Examples:**

- DFO stock assessment methods
- DFO data analysis approaches
- DFO modeling techniques
- DFO assessment protocols

#### 4.2.7 Reference Points

- Concept represents DFO-specific management reference points and benchmarks
- Concept is based on DFO's management framework
- Concept is not applicable to other organizations

**Examples:**

- DFO reference points (UMSY, SMSY, Sgen)
- DFO management benchmarks
- DFO conservation targets
- DFO management thresholds

### 4.3 BORDERLINE CASES (REQUIRE DISCUSSION)

#### 4.3.1 Hatchery Concepts

**Could be general (hatchery operations) or DFO-specific (hatchery enhancement policies)**

**Discussion Points:**

- General hatchery operations vs DFO-specific enhancement policies
- Standard hatchery practices vs DFO-specific protocols
- Common hatchery equipment vs DFO-specific systems

**Decision Criteria:**

- If concept represents standard hatchery operations → Contribute to NCEAS
- If concept represents DFO-specific policies → Keep in DFO

#### 4.3.2 Enhancement Concepts

**Could be general (biological enhancement) or DFO-specific (enhancement policies)**

**Discussion Points:**

- General biological enhancement vs DFO-specific enhancement policies
- Standard enhancement methods vs DFO-specific approaches
- Common enhancement goals vs DFO-specific objectives

**Decision Criteria:**

- If concept represents general biological enhancement → Contribute to NCEAS
- If concept represents DFO-specific policies → Keep in DFO

#### 4.3.3 Survey Methods

**Could be general (sonar counting) or DFO-specific (DFO survey protocols)**

**Discussion Points:**

- Standard survey methods vs DFO-specific protocols
- Common survey equipment vs DFO-specific systems
- General survey procedures vs DFO-specific standards

**Decision Criteria:**

- If concept represents standard survey methods → Contribute to NCEAS
- If concept represents DFO-specific protocols → Keep in DFO

#### 4.3.4 Genetic Concepts

**Could be general (genetic diversity) or DFO-specific (GSI reporting units)**

**Discussion Points:**

- General genetic concepts vs DFO-specific GSI approaches
- Standard genetic methods vs DFO-specific protocols
- Common genetic classifications vs DFO-specific systems

**Decision Criteria:**

- If concept represents general genetic concepts → Contribute to NCEAS
- If concept represents DFO-specific GSI approaches → Keep in DFO

### 4.4 Decision Criteria

#### 4.4.1 Scope

- **Question:** Does the concept apply beyond DFO's organizational boundaries?
- **NCEAS:** If yes, consider contributing to NCEAS
- **DFO:** If no, keep in DFO

#### 4.4.2 Standardization

- **Question:** Is there a widely-accepted definition or method?
- **NCEAS:** If yes, consider contributing to NCEAS
- **DFO:** If no, keep in DFO

#### 4.4.3 Institutional Control

- **Question:** Does DFO need to control the definition for policy reasons?
- **NCEAS:** If no, consider contributing to NCEAS
- **DFO:** If yes, keep in DFO

#### 4.4.4 Interoperability

- **Question:** Would other organizations benefit from using this concept?
- **NCEAS:** If yes, consider contributing to NCEAS
- **DFO:** If no, keep in DFO

#### 4.4.5 Maintenance

- **Question:** Who is best positioned to maintain and update the concept definition?
- **NCEAS:** If NCEAS or broader community, consider contributing to NCEAS
- **DFO:** If DFO, keep in DFO

---

## 5. Assessment of NCEAS as Cross-Organizational Domain Ontology

### 5.1 Current State Analysis

#### 5.1.1 Strengths

1. **Comprehensive domain coverage**: Has measurement types, fishery types, equipment, water bodies, age classes
2. **Academic foundation**: NCEAS is a research institution with scientific credibility
3. **Geographic scope**: Covers Alaska and Pacific salmon (broader than just DFO)
4. **Domain expertise**: Focuses on general salmon biology, ecology, and fisheries
5. **Established hierarchies**: Well-developed classification systems for key domain concepts

#### 5.1.2 Challenges

1. **Geographic bias**: Currently focused on Alaska/Pacific (SASAP data portal)
2. **Academic focus**: May not include management/policy concepts needed by government agencies
3. **Institutional ownership**: NCEAS controls the ontology, which could limit other organizations' influence
4. **Scope boundaries**: Need to define what belongs in domain ontology vs organization-specific ontologies
5. **Maintenance responsibility**: Single institution responsible for maintaining comprehensive domain ontology

### 5.2 Potential for Cross-Organizational Use

#### 5.2.1 STRONG Potential

- **General biological concepts**: Basic salmon biology, ecology, and life history
- **Environmental concepts**: Water bodies, habitats, environmental conditions
- **Standard measurements**: Common biological measurements and parameters
- **Equipment and gear**: Standard fishing and survey equipment

#### 5.2.2 MODERATE Potential

- **Measurement types and methods**: If expanded to include more organizations' approaches
- **Survey protocols**: If standardized across organizations
- **Analytical methods**: If based on widely-accepted scientific standards
- **Classification schemes**: If based on scientific consensus

#### 5.2.3 WEAK Potential

- **Management and policy concepts**: Not in scope for academic research ontology
- **Organization-specific procedures**: Too specific for general domain ontology
- **Regulatory frameworks**: Too specific to particular jurisdictions
- **Institutional structures**: Too specific to particular organizations

### 5.3 Recommendation

**YES** - NCEAS can serve as a cross-organizational domain ontology for general salmon biology, ecology, and fisheries concepts, but it should be complemented by organization-specific ontologies for management and policy concepts.

**Rationale:**

1. **Complementary approach**: Domain ontology + organization-specific ontologies
2. **Clear boundaries**: General concepts in NCEAS, specific concepts in organizational ontologies
3. **Shared governance**: Multiple organizations contribute to and benefit from domain ontology
4. **Maintained specificity**: Organizations retain control over their specific concepts

---

## 6. Implementation Plan

### 6.1 IMMEDIATE ACTIONS (Next 3 months)

#### 6.1.1 Complete NCEAS Alignment

**Priority 1: Measurement Hierarchy (2 classes)**

- `dfo:GeneticDiversity` → `odo:SALMON_00000167` (measurement type)
- `dfo:Fecundity` → `odo:SALMON_00000167` (measurement type)

**Priority 2: Fishery Hierarchy (1 class)**

- `dfo:MixedStockFishery` → `odo:SALMON_00000137` (Fishery type)

**Implementation Steps:**

1. Review NCEAS class definitions for semantic alignment
2. Update DFO ontology with new subclass relationships
3. Validate logical consistency
4. Update documentation

#### 6.1.2 Analyze Recruitment Relationship

**Task:** Examine `dfo:Recruitment` relationship to NCEAS age class recruits

**Analysis Questions:**

1. Is recruitment a process, a measurement, or an age class concept?
2. How does DFO's recruitment concept align with NCEAS age class recruits?
3. What is the semantic relationship between these concepts?

**Deliverables:**

1. Semantic alignment analysis
2. Recommendation for integration approach
3. Implementation plan if integration is recommended

#### 6.1.3 Update Documentation

**Task:** Document integration strategy in CONVENTIONS.md

**Updates Needed:**

1. Add NCEAS integration patterns
2. Document decision criteria for contribution vs keeping local
3. Add examples of integration approaches
4. Update import strategy documentation

### 6.2 MEDIUM-TERM ACTIONS (3-12 months)

#### 6.2.1 Establish NCEAS Governance

**Task:** Work with NCEAS to establish cross-ontology coordination

**Objectives:**

1. Establish governance framework for cross-ontology coordination
2. Define roles and responsibilities for ontology maintenance
3. Establish communication channels for coordination
4. Create process for handling conflicts and changes

**Deliverables:**

1. Governance framework document
2. Communication protocols
3. Conflict resolution procedures
4. Change management process

#### 6.2.2 Contribute to NCEAS

**Task:** Identify and contribute DFO concepts with multi-organizational relevance

**Process:**

1. Identify DFO concepts that meet contribution criteria
2. Prepare contribution proposals
3. Submit to NCEAS for review
4. Implement approved contributions

**Potential Contributions:**

1. General measurement types
2. Standard fishery types
3. Common equipment types
4. Environmental concepts
5. Age class and recruitment concepts

#### 6.2.3 Monitor NCEAS Changes

**Task:** Establish process to monitor and respond to NCEAS changes

**Process:**

1. Establish monitoring system for NCEAS changes
2. Create review process for changes
3. Implement response procedures
4. Update DFO ontology as needed

**Monitoring Areas:**

1. Class definition changes
2. Hierarchy modifications
3. New class additions
4. Deprecation of classes

### 6.3 LONG-TERM ACTIONS (1-3 years)

#### 6.3.1 Support NCEAS Development

**Task:** Participate in NCEAS development for general domain concepts

**Activities:**

1. Participate in NCEAS development discussions
2. Contribute expertise on general domain concepts
3. Help establish standards for cross-organizational use
4. Support community building around NCEAS

#### 6.3.2 Evaluate Success

**Task:** Assess whether integration achieves intended benefits

**Evaluation Criteria:**

1. Improved interoperability with other organizations
2. Reduced maintenance burden for domain concepts
3. Enhanced semantic richness of DFO ontology
4. Better alignment with broader salmon research community

**Evaluation Methods:**

1. Interoperability testing
2. Maintenance burden analysis
3. Community feedback
4. Usage statistics

#### 6.3.3 Adapt Strategy

**Task:** Refine integration approach based on experience

**Adaptation Areas:**

1. Refine contribution criteria
2. Adjust governance framework
3. Improve communication protocols
4. Enhance monitoring processes

---

## 7. Benefits and Risks Analysis

### 7.1 Benefits

#### 7.1.1 Avoid Reinventing Domain Hierarchies

- **Benefit:** Leverage established measurement, fishery, and age class hierarchies
- **Impact:** Reduced development and maintenance effort
- **Example:** Use NCEAS measurement types instead of creating DFO-specific ones

#### 7.1.2 Improve Interoperability

- **Benefit:** Enable cross-ontology reasoning and queries
- **Impact:** Better data integration and analysis capabilities
- **Example:** Query across DFO and NCEAS data using shared concepts

#### 7.1.3 Enhance Semantic Richness

- **Benefit:** Connect DFO-specific concepts to broader domain knowledge
- **Impact:** More sophisticated reasoning and inference capabilities
- **Example:** Link DFO management concepts to general biological concepts

#### 7.1.4 Reduce Maintenance Burden

- **Benefit:** Don't need to maintain domain hierarchies that others already maintain
- **Impact:** Focus resources on DFO-specific concepts
- **Example:** Let NCEAS maintain general fishery types

#### 7.1.5 Community Alignment

- **Benefit:** Align with broader salmon research community
- **Impact:** Better collaboration and knowledge sharing
- **Example:** Use same concepts as other salmon research organizations

### 7.2 Risks

#### 7.2.1 Dependency on External Ontology

- **Risk:** Changes to NCEAS could affect DFO ontology
- **Impact:** Potential breaking changes or semantic conflicts
- **Mitigation:** Establish monitoring and response procedures

#### 7.2.2 Semantic Misalignment

- **Risk:** NCEAS classes might not perfectly match DFO concepts
- **Impact:** Incorrect reasoning or data interpretation
- **Mitigation:** Careful review of class definitions and relationships

#### 7.2.3 Maintenance Complexity

- **Risk:** More complex ontology with external dependencies
- **Impact:** Increased complexity in maintenance and updates
- **Mitigation:** Clear documentation of dependencies and relationships

#### 7.2.4 Loss of Control

- **Risk:** DFO loses control over domain concept definitions
- **Impact:** Cannot modify concepts to meet DFO-specific needs
- **Mitigation:** Maintain DFO-specific concepts locally

#### 7.2.5 Geographic Bias

- **Risk:** NCEAS focuses on Alaska/Pacific, may not cover DFO's Canadian focus
- **Impact:** Missing concepts relevant to Canadian salmon management
- **Mitigation:** Contribute Canadian-specific concepts to NCEAS

#### 7.2.6 Institutional Mismatch

- **Risk:** NCEAS is academic research, DFO is government management
- **Impact:** Different priorities and perspectives
- **Mitigation:** Establish governance framework for coordination

### 7.3 Mitigation Strategies

#### 7.3.1 Document Dependencies

- **Strategy:** Clearly document which terms depend on NCEAS
- **Implementation:** Maintain dependency documentation
- **Benefit:** Clear understanding of external dependencies

#### 7.3.2 Monitor Changes

- **Strategy:** Establish process to monitor NCEAS changes
- **Implementation:** Automated monitoring system
- **Benefit:** Early warning of potential issues

#### 7.3.3 Semantic Validation

- **Strategy:** Carefully review class definitions and relationships
- **Implementation:** Regular validation of semantic alignment
- **Benefit:** Ensure correct reasoning and interpretation

#### 7.3.4 Hybrid Approach

- **Strategy:** Use NCEAS for general concepts, keep DFO-specific concepts local
- **Implementation:** Clear boundaries between general and specific concepts
- **Benefit:** Best of both worlds

#### 7.3.5 Community Engagement

- **Strategy:** Participate in NCEAS development to influence direction
- **Implementation:** Active participation in NCEAS development
- **Benefit:** Influence NCEAS development to meet DFO needs

---

## 8. Specific Integration Recommendations

### 8.1 Phase 1: NCEAS Alignment (8 classes)

#### 8.1.1 Priority 1: Measurement Hierarchy (3 classes)

**Status:** 1 already implemented, 2 to implement

**Already Implemented:**

- `dfo:SizeAtAge` → `odo:SALMON_00000167` (measurement type) ✅

**To Implement:**

- `dfo:GeneticDiversity` → `odo:SALMON_00000167` (measurement type)
- `dfo:Fecundity` → `odo:SALMON_00000167` (measurement type)

**Implementation:**

```turtle
dfo:GeneticDiversity a owl:Class ;
  rdfs:label "Genetic diversity"@en ;
  rdfs:comment "The variation at the level of individual genes, and provides a mechanism for populations to adapt to their ever-changing environment."@en ;
  rdfs:subClassOf odo:SALMON_00000167 ; # measurement type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

dfo:Fecundity a owl:Class ;
  rdfs:label "Fecundity"@en ;
  rdfs:comment "The number of eggs an animal produces during each reproductive cycle; the potential reproductive capacity of an organism or population."@en ;
  rdfs:subClassOf odo:SALMON_00000167 ; # measurement type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

#### 8.1.2 Priority 2: Fishery Hierarchy (1 class)

**Status:** 2 already implemented, 1 to implement

**Already Implemented:**

- `dfo:PreTerminalFishery` → `odo:SALMON_00000137` (fishery type) ✅
- `dfo:TerminalFishery` → `odo:SALMON_00000137` (fishery type) ✅

**To Implement:**

- `dfo:MixedStockFishery` → `odo:SALMON_00000137` (Fishery type)

**Implementation:**

```turtle
dfo:MixedStockFishery a owl:Class ;
  rdfs:label "Mixed-stock fishery"@en ;
  rdfs:comment "Individual fish in different stocks might mix or migrate between different areas. Also referred to as 'multispecies fishery'."@en ;
  rdfs:subClassOf odo:SALMON_00000137 ; # Fishery type
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .
```

#### 8.1.3 Priority 3: Age Class Hierarchy (1 class)

**Status:** 1 already implemented, 1 to analyze

**Already Implemented:**

- `dfo:AgeAtMaturity` → `odo:SALMON_00000407` (age class) ✅

**To Analyze:**

- `dfo:Recruitment` → Consider relationship to NCEAS age class recruits

**Analysis Required:**

1. Review NCEAS age class recruit concepts
2. Analyze semantic alignment with DFO recruitment concept
3. Determine appropriate relationship (if any)

#### 8.1.4 Priority 4: Recruitment Relationship (1 class)

**Status:** Requires analysis

**Analysis Questions:**

1. Is recruitment a process, a measurement, or an age class concept?
2. How does DFO's recruitment concept align with NCEAS age class recruits?
3. What is the semantic relationship between these concepts?

**Deliverables:**

1. Semantic alignment analysis
2. Recommendation for integration approach
3. Implementation plan if integration is recommended

### 8.2 Phase 2: BFO Grounding with NCEAS Context (15 classes)

#### 8.2.1 Process Classes (6 classes)

**Objective:** Ground process classes in BFO while considering NCEAS context

**Classes:**

- `dfo:Enhancement` → `bfo:0000015` (process)
- `dfo:HatcheryEnhancement` → `bfo:0000015` (process)
- `dfo:EquilibriumTradeoffAnalysis` → `bfo:0000015` (process)
- `dfo:LifeCycleModel` → `bfo:0000015` (process)
- `dfo:RunReconstructionModel` → `bfo:0000015` (process)
- `dfo:StockRecruitmentRelationship` → `bfo:0000015` (process)

**Implementation:**

```turtle
dfo:Enhancement a owl:Class ;
  rdfs:label "Enhancement"@en ;
  rdfs:comment "The application of biological and technical knowledge and capabilities to increase the productivity of fish stocks."@en ;
  rdfs:subClassOf bfo:0000015 ; # process
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

# Similar implementation for other process classes
```

#### 8.2.2 Material Entity Classes (3 classes)

**Objective:** Ground material entity classes in BFO while considering NCEAS context

**Classes:**

- `dfo:Hatchery` → `bfo:0000040` (material entity)
- `dfo:IndicatorPopulation` → `bfo:0000040` (material entity)
- `dfo:IndicatorStream` → `bfo:0000040` (material entity)

**Implementation:**

```turtle
dfo:Hatchery a owl:Class ;
  rdfs:label "Hatchery"@en ;
  rdfs:comment "A hatchery is a facility where eggs are hatched under artificial conditions."@en ;
  rdfs:subClassOf bfo:0000040 ; # material entity
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

# Similar implementation for other material entity classes
```

#### 8.2.3 Information Entity Classes (6 classes)

**Objective:** Ground information entity classes in BFO while considering NCEAS context

**Classes:**

- `dfo:HarvestAdvice` → `bfo:0000031` (generically dependent continuant)
- `dfo:Protocol` → `bfo:0000031` (generically dependent continuant)
- `dfo:PrecautionaryApproach` → `bfo:0000031` (generically dependent continuant)
- `dfo:RebuildingPlan` → `bfo:0000031` (generically dependent continuant)

**Implementation:**

```turtle
dfo:HarvestAdvice a owl:Class ;
  rdfs:label "Harvest advice"@en ;
  rdfs:comment "The scientific recommendation provided to fisheries managers on allowable levels of fish removals."@en ;
  rdfs:subClassOf bfo:0000031 ; # generically dependent continuant
  rdfs:isDefinedBy <https://w3id.org/dfo/salmon> .

# Similar implementation for other information entity classes
```

### 8.3 Phase 3: DFO-Specific Root Classes (29 classes)

#### 8.3.1 Stock Assessment Classes (6 classes)

**Objective:** Keep DFO-specific stock assessment concepts as root classes

**Classes:**

- `dfo:Escapement`
- `dfo:SpawnerAbundance`
- `dfo:Catch`
- `dfo:FishingEffort`
- `dfo:FishingMortality`
- `dfo:RemovalRate`

**Rationale:** These are DFO-specific stock assessment concepts that don't belong in a general domain ontology.

#### 8.3.2 Management/Policy Classes (9 classes)

**Objective:** Keep DFO-specific management and policy concepts as root classes

**Classes:**

- `dfo:TotalAllowableCatch`
- `dfo:MaximumSustainableYield`
- `dfo:UMSY`
- `dfo:SMSY`
- `dfo:Sgen`
- `dfo:ReferencePoint`
- `dfo:FisheryReferencePoint`
- `dfo:OperationalControlPoint`
- `dfo:RemovalReference`

**Rationale:** These are DFO-specific management concepts that don't belong in a general domain ontology.

#### 8.3.3 Origin/Type Classes (3 classes)

**Objective:** Keep DFO-specific origin concepts as root classes

**Classes:**

- `dfo:HatcheryOrigin`
- `dfo:NaturalOrigin`
- `dfo:Wild`

**Rationale:** These are DFO-specific origin concepts that don't belong in a general domain ontology.

#### 8.3.4 Other DFO-Specific Classes (11 classes)

**Objective:** Keep DFO-specific concepts as root classes

**Classes:**

- `dfo:BroodYear`
- `dfo:DesignatableUnit`
- `dfo:CUBenchmarks`
- `dfo:IndexBased`
- `dfo:KobePlot`
- `dfo:PercentHatcheryOriginSpawners`
- `dfo:RebuildingTarget`
- `dfo:GSIRun`
- `dfo:ReportingUnit`
- `dfo:Assay`
- `dfo:MarkerPanel`
- `dfo:EscapementMethod`

**Rationale:** These are DFO-specific concepts that don't belong in a general domain ontology.

---

## 9. Conclusion and Next Steps

### 9.1 Summary

The NCEAS Salmon Ontology provides valuable domain hierarchies that should inform DFO superclass decisions, but full integration is not recommended. Instead, a **hybrid approach** should be adopted: align with NCEAS for general domain concepts while maintaining DFO-specific concepts locally.

**Key Findings:**

1. **Current State**: DFO ontology is already partially aligned with NCEAS (2 classes already integrated)
2. **Integration Opportunities**: Clear alignment opportunities for measurement hierarchies, fishery types, and age class concepts
3. **Integration Challenges**: Scope mismatch, institutional differences, geographic focus, control and governance
4. **NCEAS Potential**: Strong foundation for cross-organizational use with proper governance

### 9.2 Specific Recommendations

#### 9.2.1 Immediate Actions

1. **Complete NCEAS Alignment**: Implement remaining 3 classes from Phase 1
2. **Analyze Recruitment Relationship**: Carefully examine semantic alignment
3. **Update Documentation**: Document integration strategy in CONVENTIONS.md

#### 9.2.2 Medium-term Strategy

1. **Establish Governance**: Work with NCEAS to establish cross-ontology coordination
2. **Contribute to NCEAS**: Identify and contribute DFO concepts with multi-organizational relevance
3. **Monitor NCEAS Changes**: Establish process to monitor and respond to NCEAS changes

#### 9.2.3 Long-term Vision

1. **Support NCEAS Development**: Participate in NCEAS development for general domain concepts
2. **Evaluate Success**: Assess whether integration achieves intended benefits
3. **Adapt Strategy**: Refine integration approach based on experience

### 9.3 Heuristics for Contribution Decisions

#### 9.3.1 CONTRIBUTE TO NCEAS

- Multi-organizational relevance
- Scientific consensus
- Domain generality
- Methodological standards
- Environmental concepts
- Biological measurements
- Equipment and gear

#### 9.3.2 KEEP IN DFO

- Organizational specificity
- Canadian context
- DFO protocols
- Management hierarchies
- Policy frameworks
- Assessment methods
- Reference points

### 9.4 Assessment of NCEAS as Cross-Organizational Domain Ontology

**CURRENT STATE**: Good foundation for general biological/ecological concepts
**POTENTIAL**: Strong for cross-organizational use with proper governance
**RECOMMENDATION**: Support development while maintaining organizational boundaries

### 9.5 Next Steps

1. **Review and Approve**: Review this analysis and approve the recommended approach
2. **Implement Phase 1**: Begin with the immediate actions for NCEAS alignment
3. **Establish Governance**: Work with NCEAS to establish cross-ontology coordination
4. **Monitor Progress**: Track implementation progress and adjust as needed
5. **Evaluate Success**: Assess whether integration achieves intended benefits

---

**Document Status**: Draft for Review  
**Next Review Date**: 2025-02-24  
**Maintainer**: DFO Pacific Science — Data Stewardship Unit  
**License**: CC-BY 4.0

# Separate ChatGPT 5 Extended Thinking Analysis to Consider:

NCEAS SALMON vs DFO Salmon — deep-dive integration review

Quick heads-up: I couldn’t find a file named @nceas-salmon-integration-analysis.md in the materials you shared. So I did a direct, instrumented review of the NCEAS SALMON ontology file you uploaded (/mnt/data/SALMON.ttl, version IRI http://purl.dataone.org/odo/SALMON/0.4.0) and compared it to our own materials: DFO CONVENTIONS, ADR, our DFO Salmon content, OWL2, and OBO principles. If you intended a different doc, drop it in and I’ll fold it in as well.

I’ve also published a set of live summaries you can browse (prefixes, imports, declared classes & properties, named individuals, and likely MIREOTed terms) extracted directly from SALMON.ttl:

Browse the extracted tables in your workspace UI under:

“NCEAS SALMON.ttl — prefixes”

“ontology header & imports”

“classes / object properties / data properties / annotation properties”

“individuals (non-class/property)”

“namespace usage counts”

“likely MIREOTed classes/object properties/data properties”

“summary”

1. Snapshot of NCEAS SALMON.ttl (what’s actually there)

From automated parsing:

Ontology & version

Ontology IRI: http://purl.dataone.org/odo/SALMON_

Version IRI: http://purl.dataone.org/odo/SALMON/0.4.0

Imports (3):

http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl

http://purl.obolibrary.org/obo/envo/releases/2021-05-14/subsets/astronomical-body-part-hierarchy.owl

http://www.opengis.net/ont/geosparql

Prefixes present (19) include dwcterms, skos, w3ssn, w3time, obo, schema.org, oboInOwl, etc.

Declared entities (approx.)

Classes ≈ 432

Local SALMON classes ≈ 377 (under http://purl.dataone.org/odo/…SALMON_…)

ECSO classes ≈ 51

A few external classes (e.g., Schema.org, OBOE, one ENVO class) MIREOTed into the file

Object properties 15 (≈8 SALMON local; 3 DwC terms; 3 W3C Time; 1 SSN)

Datatype properties 1 (SALMON_00000596 / hasADF&GCode, range xsd:integer)

Annotation properties ≈ 30

Named individuals ≈ 41 (present in the ontology file)

Likely MIREOTs (declared externally but copied in):

oboe-core:MeasurementType, ENVO_00000032, schema:CreativeWork, schema:Dataset (no labels provided in-file)

Note: Darwin Core is present as a prefix, but I did not find any SALMON class that subclasses DwC core classes (e.g., dwc:Event, dwc:MeasurementOrFact). Instead, SALMON leans on OBOE/ECSO/SSN/TIME and GeoSPARQL.

2. Side-by-side: modeling stance & mechanics
   Upper framework & patterns

NCEAS SALMON: OBOE/ECSO/SSN/TIME + GeoSPARQL import; DwC used via prefix; SALMON\_ numeric IRIs; includes named individuals as enumerated values; Measurement “types/methods” modeled as OWL classes, not SKOS.

DFO Salmon: DwC is the meta-framework (subclassing dwc:Event, dwc:MeasurementOrFact); hybrid OWL + SKOS + SHACL; strict schema/data separation (no instances in dfo-salmon.ttl); minimal MIREOT of BFO/IAO/DQV; no full imports in MVP; PROV/RO, etc. used prefix-only; decision matrix explicitly documented.

Imports vs MIREOT vs Prefix-only

NCEAS SALMON:

Imports: OBOE core, ENVO subset, GeoSPARQL (3 imports).

MIREOT-like: a few external classes copied in (ENVO, OBOE, Schema.org).

Prefix-only: DwC, SKOS, SSN, TIME, OBO, DCTERMS, etc.

(As an OWL2 note: imports are fine, but they should be intentional and light. See OWL2 §3.4 on imports.)

DFO Salmon (per our CONVENTIONS):

No full imports for MVP; MIREOT a small set from BFO/IAO/DQV; prefix-only for DwC, PROV-O, RO, SKOS, SHACL. The decision matrix is written down.

Use of DwC

NCEAS SALMON: DwC appears only as a prefix; e.g., dwcterms:scientificName, dwcterms:vernacularName, typed in SALMON.ttl as owl:ObjectProperty (this is a red flag, as DwC terms are meant to carry literal values in practice).

DFO Salmon: Explicit alignment on DwC (classes & predicates), using rdfs:subClassOf and DwC predicates like dwc:eventDate and dwc:samplingProtocol.

SKOS vs OWL

NCEAS SALMON: No SKOS concepts declared (0). Code lists are represented either as classes or named individuals.

DFO Salmon: SKOS is the workhorse for vocabularies (methods, criteria, status categories, estimate type tiers, etc.).

Schema/data separation

NCEAS SALMON: Contains ~41 owl:NamedIndividual; some of these look like enumerated values or code entries.

DFO Salmon: Strict separation (schema only in dfo-salmon.ttl; examples in /ontology/examples/; no instance data allowed in schema).

Identifier policy & labels

NCEAS SALMON: Numeric IRIs under purl.dataone.org/odo/SALMON\_… with rdfs:labels (sometimes missing on MIREOTed terms).

DFO Salmon: Human-readable PascalCase for classes; lowerCamelCase for properties; all elements require rdfs:label, rdfs:comment, rdfs:isDefinedBy (per our conventions). (Our conventions also emphasize label+definition everywhere.)

OBO principles (for comparison): prefer PURLs of the form https://purl.obolibrary.org/obo/$namespace.owl and namespace policy; not a blocker for NCEAS, but relevant if they ever pursue OBO membership.

3. “Just integrate” items (low-risk, high-value)

Fix DwC property typing in NCEAS SALMON (upstream)
In SALMON.ttl, dwcterms:scientificName, dwcterms:vernacularName, and dwcterms:nameAccordingTo are declared as owl:ObjectProperty, but DwC terms are usually used with literal values; giving them ObjectProperty type will break OWL 2 DL typing and data usage downstream.
Action: Remove a owl:ObjectProperty for DwC terms; treat as datatype/annotation properties (or leave untyped as RDF properties) to avoid DL violations. (OWL2 requires consistent typing across imports; keep to the safe side.)
Why now? This is a straightforward change that increases interoperability immediately with DFO’s DwC-aligned model.

Move organization-specific codes out of NCEAS core
SALMON_00000596 (hasADF&GCode) is jurisdiction-specific (Alaska).
Action: Propose moving to an Alaska add-on or keeping such codes in organization-specific ontologies (e.g., DFO or ADF&G modules) rather than in the cross-org NCEAS core. This aligns with our separation strategy and makes NCEAS more universally reusable.

Adopt W3C TIME intervals & GeoSPARQL (DFO side; prefix-only or MIREOT)
NCEAS already imports W3C TIME and GeoSPARQL. DFO can prefix-only (or MIREOT minimally) adopt time:hasBeginning/hasEnd and geo:hasGeometry/geo:asWKT for richer temporal/spatial modeling of dwc:Event windows and footprints. This is fully compatible with our import strategy (prefix/MIREOT, not full imports) and improves cross-graph queries.

Schema/data separation (NCEAS upstream)
NCEAS has ~41 named individuals in SALMON.ttl.
Action: Split those into (a) SKOS concept schemes for controlled vocabularies, or (b) a separate data/examples file. This matches what we enforce in DFO (schema-only ontology file).

Schema.org Dataset alignment (both sides)
NCEAS MIREOTs schema:Dataset; DFO already uses schema:Dataset for dfo:Dataset subclasses.
Action: Declare alignment: dfo:Dataset rdfs:subClassOf schema:Dataset (already our pattern), and NCEAS to do the same where relevant, so cross-repo queries on datasets line up.

4. Items that warrant discussion (non-blocking, but important)

DwC vs OBOE/ECSO/SSN as the backbone
DFO is DwC-first (Events/Measurements), while NCEAS is OBOE/ECSO-first. We should pick a convergence pattern:

Option A (recommended for cross-org): Keep both, but bridge with explicit equivalences/subclassing patterns:

SALMON:Observation ≡/⊑ dwc:Occurrence (or declare mapping via SKOS mapping props if stricter semantics aren’t yet agreed).

Create a lightweight alignment module (no imports) that only contains mapping triples.

Methods & “types” — OWL class vs SKOS concept
In NCEAS, things like “Fish measurement method” are OWL classes; in DFO, methods are SKOS (picklists).

Trade-off: SKOS supports change management, multilingual labels, and controlled hierarchies, while keeping inference simple; OWL classes can over-constrain workflows and are heavier for enumerations.

Proposal: Keep methods as SKOS schemes (in NCEAS core), and use SHACL to validate method usage in data (consistent with DFO’s hybrid approach).

NCEAS identifier policy
SALMON IRIs are numeric ODO IRIs. DFO is human-readable with w3id.

Feasible compromise: Keep SALMON numeric IRIs, require rdfs:label + rdfs:comment everywhere; DFO contributes with human-readable labels and mappings. (If OBO membership is a long-term goal, revisit PURL policy.)

ENVO alignment instead of bespoke “waterbody” relations
NCEAS has hasNativeWaterbody as an object property. RO/ENVO patterns may cover this better (e.g., habitat/occurs_in/part_of). Our conventions emphasize reusing RO before minting new relations.

5. Is the NCEAS SALMON ontology suitable as a cross-org home as is?

Almost—but not yet. Two blockers and two “should-fix” items:

Blockers

DwC property typing: remove owl:ObjectProperty typing from DwC literal properties (scientific/vernacular/nameAccordingTo), otherwise cross-graph use will be brittle or inconsistent. (OWL2 DL typing/global restrictions.)

Schema/data separation: move named individuals out of the core schema file (either to SKOS or to an examples module). DFO (and OBO style) require the schema file to be instance-free.

Should-fix 3) Adopt SKOS for enumerations (methods, “types”); keep OWL classes for structural entities. This matches OBO-style hybrid modeling we use. 4) Add labels/comments/isDefinedBy to every element (especially the currently unlabeled MIREOT terms) for documentation quality. (Our conventions require this.)

If NCEAS accepts those changes, it becomes a robust cross-organization layer, with DFO housing agency-specific policy/process terms (WSP, internal codes, etc.) on top.

6. Where we have clear overlap & proposed treatment

A. Dataset & creative works

Overlap: NCEAS MIREOTs schema:Dataset; DFO already uses it.

Action: Keep schema:Dataset canonical in both; DFO’s dfo:Dataset ⊑ schema:Dataset. (Already aligned on our side.)

B. Event time & geometry

Overlap: NCEAS uses W3C TIME and GeoSPARQL; DFO uses DwC Event predicates.

Action: DFO adds prefix-only W3C TIME/GeoSPARQL; represent dwc:Event windows with time:hasBeginning/hasEnd and footprints with geo:hasGeometry. No import needed; optional MIREOT of a few terms to improve UX.

C. “Measurement types/methods”

Overlap: NCEAS has Fish length/age measurement types, Measurement method as OWL classes. DFO has EscapementMeasurement + method picklists (SKOS).

Action: In NCEAS, recast method/type enumerations as SKOS. DFO can reuse those SKOS concepts for non-escapement measurement vocabularies (e.g., biology/morphology). This makes cross-org picklists consistent and lets each org keep internal nuances in their own ontologies.

D. DwC taxon/vernacular/scientific naming

Overlap: Both reference DwC terms; DFO stores external taxonomy IRIs as literals (pragmatic).

Action: NCEAS should drop parallel SALMON properties like “has vernacular name” in favor of DwC predicates; keep one canonical path. (Per our external alignment rules: reuse before mint.)

7. Things we should debate before moving

Upper alignment axis: Do we agree to DwC at the top (our current stance) and keep OBOE/ECSO as supporting vocabularies via MIREOT/prefix? That’s the cleanest path for biodiversity interoperability—and matches our ADR.

Governance: NCEAS as “cross-org core” implies a change process and a release discipline (version IRI, per OWL2 §3.3) so terms don’t churn.

RO/ENVO vs bespoke relations: prefer RO relations (subproperty if needed) and ENVO classes instead of minting convenience properties whenever possible.

8. Heuristics — what goes to NCEAS vs what stays in DFO
   Contribute to NCEAS when the term is…

Organization-agnostic (applies across agencies, labs, and projects).

Domain-level salmon biology/domain concepts (e.g., general fish morphology measurement types, general survey method categories) not tied to DFO policy/process.

Technically foundational (time/space patterns, observation/measurement patterns, shared sampling method vocabularies).

Stable & broadly cited (literature-backed, not local jargon).

Free of instance data (schema only; enumerations via SKOS, not individuals).

Reuses external standards where possible (DwC, RO, ENVO, TIME, GeoSPARQL).

Keep in DFO when the term is…

Policy/procedure-specific (e.g., WSP Integrated/Rapid Status constructs and workflows).

Jurisdiction-specific codes/IDs (ADF&G, internal DFO codes).

Operational workflow glue (org roles, internal pipelines, DFO-specific quality dimensions or downgrades).

Under active change localized to DFO.

Data/instance content (always out of dfo-salmon.ttl, per ADR-004).

9. OWL 2 DL & OBO compliance checks to watch

Typing consistency: Do not type literal-carrying DwC terms as owl:ObjectProperty. Keep property typing consistent across the import closure. (OWL2 typing/global restrictions.)

Version IRIs & releases: ensure stable ontology IRI + version IRI discipline (OWL2 §3.3).

No instances in schema: enforce schema/data separation (ADR-004).

OBO alignment: if pursuing OBO membership later, plan for PURL namespace policy and durability.

10. Concrete contributions & who changes what
    Propose to NCEAS (upstream)

Fix DwC property typing (remove owl:ObjectProperty on DwC naming terms).

Split individuals out of SALMON core; recast enumerations as SKOS Schemes.

Replace SALMON “has vernacular/scientific name” with the DwC versions; deprecate the SALMON duplicates.

Discuss ENVO/RO alignment for environment/waterbody relations; avoid bespoke relation proliferation.

Plan for DFO

Add prefix-only W3C TIME & GeoSPARQL to augment DwC Event intervals & footprints.

Re-use NCEAS SKOS schemes (once available) for general fish measurement methods/types; keep DFO-specific method variants locally.

Maintain our import/MIREOT discipline (no full imports in MVP; MIREOT small, stable sets).

11. Competency Questions (CQs) & matching SPARQL

Add these to COMPETENCY_QUESTIONS.md when you’re happy with them.

CQ-A (cross-org): Which survey events in river X between dates Y–Z used method M, and what geometries/intervals were recorded?
SPARQL sketch (works if DFO adds TIME/GeoSPARQL and NCEAS keeps DwC+TIME/Geo terms):

PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX schema: <https://schema.org/>
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?event ?begin ?end ?wkt WHERE {
?event a dwc:Event ;
dfo:usesEnumerationMethod ?method ;
time:hasBeginning/time:inXSDDateTime ?begin ;
time:hasEnd/time:inXSDDateTime ?end ;
geo:hasGeometry/geo:asWKT ?wkt .
?event dfo:aboutWaterbody ?water . # or ENVO/RO alignment once agreed
FILTER(?method = :SnorkelSurvey) # example SKOS method IRI
FILTER(?begin >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?end <= "2022-12-31T23:59:59Z"^^xsd:dateTime)
}

CQ-B (quality): Which SALMON/DwC properties are incorrectly typed as ObjectProperty? (for NCEAS cleanup)

PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?p WHERE {
VALUES ?p { dwc:scientificName dwc:vernacularName dwc:nameAccordingTo }
?p a owl:ObjectProperty .
}

CQ-C (governance): List any named individuals lingering in schema files (for enforcing schema/data split)

PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?i ?t WHERE {
?i a owl:NamedIndividual ; a ?t .
FILTER(?t != owl:NamedIndividual)
}

CQ-D (reuse before mint): Find SALMON properties that duplicate well-known external ones (e.g., vernacular/scientific name)

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
PREFIX odo: <http://purl.dataone.org/odo/>

SELECT ?local ?localLabel ?external WHERE {
VALUES ?external { dwc:scientificName dwc:vernacularName }
?local rdfs:label ?localLabel .
FILTER(CONTAINS(LCASE(?localLabel), "vernacular") || CONTAINS(LCASE(?localLabel), "scientific"))
FILTER(STRSTARTS(STR(?local), "http://purl.dataone.org/odo/SALMON_"))
}

CQ-E (alignment): Which SALMON classes should map to DwC Event or MeasurementOrFact?
(After we propose bridging, we’ll populate a mapping graph and verify via a query.)

12. Final recommendations & next steps

Upstream PR to NCEAS SALMON

Remove owl:ObjectProperty on DwC literal terms.

Extract named individuals out of the schema file; convert enumerations to SKOS schemes.

Deprecate SALMON properties that duplicate DwC (e.g., vernacular/scientific name), and align with RO/ENVO where appropriate.

DFO updates

Add W3C TIME & GeoSPARQL prefix-only usage in DFO (optionally MIREOT a handful of key terms).

Reuse NCEAS SKOS vocabularies once they exist; keep DFO-specific policy/process items locally (WSP, codes).

Alignment module

Create a small, separate mapping file declaring minimal equivalences/subclassing between SALMON and DFO terms (no imports; just mappings).

Validate with ROBOT + reasoner + SPARQL checks from the CQs. (Our CONVENTIONS include ROBOT commands & QA workflow.)

Why this all fits our rules

OWL2: Respect import closure and type constraints; keep properties consistently typed; use version IRIs.

OBO principles: Prefer reuse, clear PURLs, and durable governance (should NCEAS pursue OBO membership later).

DFO CONVENTIONS: Hybrid OWL+SKOS+SHACL; MIREOT-first for small sets; no instances in schema; label+definition everywhere; RO before mint.

If you want, I can draft the exact Turtle diffs for an NCEAS PR (removing the DwC owl:ObjectProperty typings, carving out a SKOS “Fish Measurement Method” scheme, and stubbing a SALMON–DFO alignment module).NCEAS SALMON vs DFO Salmon — deep-dive integration review

Quick heads-up: I couldn’t find a file named @nceas-salmon-integration-analysis.md in the materials you shared. So I did a direct, instrumented review of the NCEAS SALMON ontology file you uploaded (/mnt/data/SALMON.ttl, version IRI http://purl.dataone.org/odo/SALMON/0.4.0) and compared it to our own materials: DFO CONVENTIONS, ADR, our DFO Salmon content, OWL2, and OBO principles. If you intended a different doc, drop it in and I’ll fold it in as well.

I’ve also published a set of live summaries you can browse (prefixes, imports, declared classes & properties, named individuals, and likely MIREOTed terms) extracted directly from SALMON.ttl:

Browse the extracted tables in your workspace UI under:

“NCEAS SALMON.ttl — prefixes”

“ontology header & imports”

“classes / object properties / data properties / annotation properties”

“individuals (non-class/property)”

“namespace usage counts”

“likely MIREOTed classes/object properties/data properties”

“summary”

1. Snapshot of NCEAS SALMON.ttl (what’s actually there)

From automated parsing:

Ontology & version

Ontology IRI: http://purl.dataone.org/odo/SALMON_

Version IRI: http://purl.dataone.org/odo/SALMON/0.4.0

Imports (3):

http://ecoinformatics.org/oboe/oboe.1.2/oboe-core.owl

http://purl.obolibrary.org/obo/envo/releases/2021-05-14/subsets/astronomical-body-part-hierarchy.owl

http://www.opengis.net/ont/geosparql

Prefixes present (19) include dwcterms, skos, w3ssn, w3time, obo, schema.org, oboInOwl, etc.

Declared entities (approx.)

Classes ≈ 432

Local SALMON classes ≈ 377 (under http://purl.dataone.org/odo/…SALMON_…)

ECSO classes ≈ 51

A few external classes (e.g., Schema.org, OBOE, one ENVO class) MIREOTed into the file

Object properties 15 (≈8 SALMON local; 3 DwC terms; 3 W3C Time; 1 SSN)

Datatype properties 1 (SALMON_00000596 / hasADF&GCode, range xsd:integer)

Annotation properties ≈ 30

Named individuals ≈ 41 (present in the ontology file)

Likely MIREOTs (declared externally but copied in):

oboe-core:MeasurementType, ENVO_00000032, schema:CreativeWork, schema:Dataset (no labels provided in-file)

Note: Darwin Core is present as a prefix, but I did not find any SALMON class that subclasses DwC core classes (e.g., dwc:Event, dwc:MeasurementOrFact). Instead, SALMON leans on OBOE/ECSO/SSN/TIME and GeoSPARQL.

2. Side-by-side: modeling stance & mechanics
   Upper framework & patterns

NCEAS SALMON: OBOE/ECSO/SSN/TIME + GeoSPARQL import; DwC used via prefix; SALMON\_ numeric IRIs; includes named individuals as enumerated values; Measurement “types/methods” modeled as OWL classes, not SKOS.

DFO Salmon: DwC is the meta-framework (subclassing dwc:Event, dwc:MeasurementOrFact); hybrid OWL + SKOS + SHACL; strict schema/data separation (no instances in dfo-salmon.ttl); minimal MIREOT of BFO/IAO/DQV; no full imports in MVP; PROV/RO, etc. used prefix-only; decision matrix explicitly documented.

Imports vs MIREOT vs Prefix-only

NCEAS SALMON:

Imports: OBOE core, ENVO subset, GeoSPARQL (3 imports).

MIREOT-like: a few external classes copied in (ENVO, OBOE, Schema.org).

Prefix-only: DwC, SKOS, SSN, TIME, OBO, DCTERMS, etc.

(As an OWL2 note: imports are fine, but they should be intentional and light. See OWL2 §3.4 on imports.)

DFO Salmon (per our CONVENTIONS):

No full imports for MVP; MIREOT a small set from BFO/IAO/DQV; prefix-only for DwC, PROV-O, RO, SKOS, SHACL. The decision matrix is written down.

Use of DwC

NCEAS SALMON: DwC appears only as a prefix; e.g., dwcterms:scientificName, dwcterms:vernacularName, typed in SALMON.ttl as owl:ObjectProperty (this is a red flag, as DwC terms are meant to carry literal values in practice).

DFO Salmon: Explicit alignment on DwC (classes & predicates), using rdfs:subClassOf and DwC predicates like dwc:eventDate and dwc:samplingProtocol.

SKOS vs OWL

NCEAS SALMON: No SKOS concepts declared (0). Code lists are represented either as classes or named individuals.

DFO Salmon: SKOS is the workhorse for vocabularies (methods, criteria, status categories, estimate type tiers, etc.).

Schema/data separation

NCEAS SALMON: Contains ~41 owl:NamedIndividual; some of these look like enumerated values or code entries.

DFO Salmon: Strict separation (schema only in dfo-salmon.ttl; examples in /ontology/examples/; no instance data allowed in schema).

Identifier policy & labels

NCEAS SALMON: Numeric IRIs under purl.dataone.org/odo/SALMON\_… with rdfs:labels (sometimes missing on MIREOTed terms).

DFO Salmon: Human-readable PascalCase for classes; lowerCamelCase for properties; all elements require rdfs:label, rdfs:comment, rdfs:isDefinedBy (per our conventions). (Our conventions also emphasize label+definition everywhere.)

OBO principles (for comparison): prefer PURLs of the form https://purl.obolibrary.org/obo/$namespace.owl and namespace policy; not a blocker for NCEAS, but relevant if they ever pursue OBO membership.

3. “Just integrate” items (low-risk, high-value)

Fix DwC property typing in NCEAS SALMON (upstream)
In SALMON.ttl, dwcterms:scientificName, dwcterms:vernacularName, and dwcterms:nameAccordingTo are declared as owl:ObjectProperty, but DwC terms are usually used with literal values; giving them ObjectProperty type will break OWL 2 DL typing and data usage downstream.
Action: Remove a owl:ObjectProperty for DwC terms; treat as datatype/annotation properties (or leave untyped as RDF properties) to avoid DL violations. (OWL2 requires consistent typing across imports; keep to the safe side.)
Why now? This is a straightforward change that increases interoperability immediately with DFO’s DwC-aligned model.

Move organization-specific codes out of NCEAS core
SALMON_00000596 (hasADF&GCode) is jurisdiction-specific (Alaska).
Action: Propose moving to an Alaska add-on or keeping such codes in organization-specific ontologies (e.g., DFO or ADF&G modules) rather than in the cross-org NCEAS core. This aligns with our separation strategy and makes NCEAS more universally reusable.

Adopt W3C TIME intervals & GeoSPARQL (DFO side; prefix-only or MIREOT)
NCEAS already imports W3C TIME and GeoSPARQL. DFO can prefix-only (or MIREOT minimally) adopt time:hasBeginning/hasEnd and geo:hasGeometry/geo:asWKT for richer temporal/spatial modeling of dwc:Event windows and footprints. This is fully compatible with our import strategy (prefix/MIREOT, not full imports) and improves cross-graph queries.

Schema/data separation (NCEAS upstream)
NCEAS has ~41 named individuals in SALMON.ttl.
Action: Split those into (a) SKOS concept schemes for controlled vocabularies, or (b) a separate data/examples file. This matches what we enforce in DFO (schema-only ontology file).

Schema.org Dataset alignment (both sides)
NCEAS MIREOTs schema:Dataset; DFO already uses schema:Dataset for dfo:Dataset subclasses.
Action: Declare alignment: dfo:Dataset rdfs:subClassOf schema:Dataset (already our pattern), and NCEAS to do the same where relevant, so cross-repo queries on datasets line up.

4. Items that warrant discussion (non-blocking, but important)

DwC vs OBOE/ECSO/SSN as the backbone
DFO is DwC-first (Events/Measurements), while NCEAS is OBOE/ECSO-first. We should pick a convergence pattern:

Option A (recommended for cross-org): Keep both, but bridge with explicit equivalences/subclassing patterns:

SALMON:Observation ≡/⊑ dwc:Occurrence (or declare mapping via SKOS mapping props if stricter semantics aren’t yet agreed).

Create a lightweight alignment module (no imports) that only contains mapping triples.

Methods & “types” — OWL class vs SKOS concept
In NCEAS, things like “Fish measurement method” are OWL classes; in DFO, methods are SKOS (picklists).

Trade-off: SKOS supports change management, multilingual labels, and controlled hierarchies, while keeping inference simple; OWL classes can over-constrain workflows and are heavier for enumerations.

Proposal: Keep methods as SKOS schemes (in NCEAS core), and use SHACL to validate method usage in data (consistent with DFO’s hybrid approach).

NCEAS identifier policy
SALMON IRIs are numeric ODO IRIs. DFO is human-readable with w3id.

Feasible compromise: Keep SALMON numeric IRIs, require rdfs:label + rdfs:comment everywhere; DFO contributes with human-readable labels and mappings. (If OBO membership is a long-term goal, revisit PURL policy.)

ENVO alignment instead of bespoke “waterbody” relations
NCEAS has hasNativeWaterbody as an object property. RO/ENVO patterns may cover this better (e.g., habitat/occurs_in/part_of). Our conventions emphasize reusing RO before minting new relations.

5. Is the NCEAS SALMON ontology suitable as a cross-org home as is?

Almost—but not yet. Two blockers and two “should-fix” items:

Blockers

DwC property typing: remove owl:ObjectProperty typing from DwC literal properties (scientific/vernacular/nameAccordingTo), otherwise cross-graph use will be brittle or inconsistent. (OWL2 DL typing/global restrictions.)

Schema/data separation: move named individuals out of the core schema file (either to SKOS or to an examples module). DFO (and OBO style) require the schema file to be instance-free.

Should-fix 3) Adopt SKOS for enumerations (methods, “types”); keep OWL classes for structural entities. This matches OBO-style hybrid modeling we use. 4) Add labels/comments/isDefinedBy to every element (especially the currently unlabeled MIREOT terms) for documentation quality. (Our conventions require this.)

If NCEAS accepts those changes, it becomes a robust cross-organization layer, with DFO housing agency-specific policy/process terms (WSP, internal codes, etc.) on top.

6. Where we have clear overlap & proposed treatment

A. Dataset & creative works

Overlap: NCEAS MIREOTs schema:Dataset; DFO already uses it.

Action: Keep schema:Dataset canonical in both; DFO’s dfo:Dataset ⊑ schema:Dataset. (Already aligned on our side.)

B. Event time & geometry

Overlap: NCEAS uses W3C TIME and GeoSPARQL; DFO uses DwC Event predicates.

Action: DFO adds prefix-only W3C TIME/GeoSPARQL; represent dwc:Event windows with time:hasBeginning/hasEnd and footprints with geo:hasGeometry. No import needed; optional MIREOT of a few terms to improve UX.

C. “Measurement types/methods”

Overlap: NCEAS has Fish length/age measurement types, Measurement method as OWL classes. DFO has EscapementMeasurement + method picklists (SKOS).

Action: In NCEAS, recast method/type enumerations as SKOS. DFO can reuse those SKOS concepts for non-escapement measurement vocabularies (e.g., biology/morphology). This makes cross-org picklists consistent and lets each org keep internal nuances in their own ontologies.

D. DwC taxon/vernacular/scientific naming

Overlap: Both reference DwC terms; DFO stores external taxonomy IRIs as literals (pragmatic).

Action: NCEAS should drop parallel SALMON properties like “has vernacular name” in favor of DwC predicates; keep one canonical path. (Per our external alignment rules: reuse before mint.)

7. Things we should debate before moving

Upper alignment axis: Do we agree to DwC at the top (our current stance) and keep OBOE/ECSO as supporting vocabularies via MIREOT/prefix? That’s the cleanest path for biodiversity interoperability—and matches our ADR.

Governance: NCEAS as “cross-org core” implies a change process and a release discipline (version IRI, per OWL2 §3.3) so terms don’t churn.

RO/ENVO vs bespoke relations: prefer RO relations (subproperty if needed) and ENVO classes instead of minting convenience properties whenever possible.

8. Heuristics — what goes to NCEAS vs what stays in DFO
   Contribute to NCEAS when the term is…

Organization-agnostic (applies across agencies, labs, and projects).

Domain-level salmon biology/domain concepts (e.g., general fish morphology measurement types, general survey method categories) not tied to DFO policy/process.

Technically foundational (time/space patterns, observation/measurement patterns, shared sampling method vocabularies).

Stable & broadly cited (literature-backed, not local jargon).

Free of instance data (schema only; enumerations via SKOS, not individuals).

Reuses external standards where possible (DwC, RO, ENVO, TIME, GeoSPARQL).

Keep in DFO when the term is…

Policy/procedure-specific (e.g., WSP Integrated/Rapid Status constructs and workflows).

Jurisdiction-specific codes/IDs (ADF&G, internal DFO codes).

Operational workflow glue (org roles, internal pipelines, DFO-specific quality dimensions or downgrades).

Under active change localized to DFO.

Data/instance content (always out of dfo-salmon.ttl, per ADR-004).

9. OWL 2 DL & OBO compliance checks to watch

Typing consistency: Do not type literal-carrying DwC terms as owl:ObjectProperty. Keep property typing consistent across the import closure. (OWL2 typing/global restrictions.)

Version IRIs & releases: ensure stable ontology IRI + version IRI discipline (OWL2 §3.3).

No instances in schema: enforce schema/data separation (ADR-004).

OBO alignment: if pursuing OBO membership later, plan for PURL namespace policy and durability.

10. Concrete contributions & who changes what
    Propose to NCEAS (upstream)

Fix DwC property typing (remove owl:ObjectProperty on DwC naming terms).

Split individuals out of SALMON core; recast enumerations as SKOS Schemes.

Replace SALMON “has vernacular/scientific name” with the DwC versions; deprecate the SALMON duplicates.

Discuss ENVO/RO alignment for environment/waterbody relations; avoid bespoke relation proliferation.

Plan for DFO

Add prefix-only W3C TIME & GeoSPARQL to augment DwC Event intervals & footprints.

Re-use NCEAS SKOS schemes (once available) for general fish measurement methods/types; keep DFO-specific method variants locally.

Maintain our import/MIREOT discipline (no full imports in MVP; MIREOT small, stable sets).

11. Competency Questions (CQs) & matching SPARQL

Add these to COMPETENCY_QUESTIONS.md when you’re happy with them.

CQ-A (cross-org): Which survey events in river X between dates Y–Z used method M, and what geometries/intervals were recorded?
SPARQL sketch (works if DFO adds TIME/GeoSPARQL and NCEAS keeps DwC+TIME/Geo terms):

PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX schema: <https://schema.org/>
PREFIX dfo: <https://w3id.org/dfo/salmon#>

SELECT ?event ?begin ?end ?wkt WHERE {
?event a dwc:Event ;
dfo:usesEnumerationMethod ?method ;
time:hasBeginning/time:inXSDDateTime ?begin ;
time:hasEnd/time:inXSDDateTime ?end ;
geo:hasGeometry/geo:asWKT ?wkt .
?event dfo:aboutWaterbody ?water . # or ENVO/RO alignment once agreed
FILTER(?method = :SnorkelSurvey) # example SKOS method IRI
FILTER(?begin >= "2022-01-01T00:00:00Z"^^xsd:dateTime && ?end <= "2022-12-31T23:59:59Z"^^xsd:dateTime)
}

CQ-B (quality): Which SALMON/DwC properties are incorrectly typed as ObjectProperty? (for NCEAS cleanup)

PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>

SELECT ?p WHERE {
VALUES ?p { dwc:scientificName dwc:vernacularName dwc:nameAccordingTo }
?p a owl:ObjectProperty .
}

CQ-C (governance): List any named individuals lingering in schema files (for enforcing schema/data split)

PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?i ?t WHERE {
?i a owl:NamedIndividual ; a ?t .
FILTER(?t != owl:NamedIndividual)
}

CQ-D (reuse before mint): Find SALMON properties that duplicate well-known external ones (e.g., vernacular/scientific name)

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dwc: <http://rs.tdwg.org/dwc/terms/>
PREFIX odo: <http://purl.dataone.org/odo/>

SELECT ?local ?localLabel ?external WHERE {
VALUES ?external { dwc:scientificName dwc:vernacularName }
?local rdfs:label ?localLabel .
FILTER(CONTAINS(LCASE(?localLabel), "vernacular") || CONTAINS(LCASE(?localLabel), "scientific"))
FILTER(STRSTARTS(STR(?local), "http://purl.dataone.org/odo/SALMON_"))
}

CQ-E (alignment): Which SALMON classes should map to DwC Event or MeasurementOrFact?
(After we propose bridging, we’ll populate a mapping graph and verify via a query.)

12. Final recommendations & next steps

Upstream PR to NCEAS SALMON

Remove owl:ObjectProperty on DwC literal terms.

Extract named individuals out of the schema file; convert enumerations to SKOS schemes.

Deprecate SALMON properties that duplicate DwC (e.g., vernacular/scientific name), and align with RO/ENVO where appropriate.

DFO updates

Add W3C TIME & GeoSPARQL prefix-only usage in DFO (optionally MIREOT a handful of key terms).

Reuse NCEAS SKOS vocabularies once they exist; keep DFO-specific policy/process items locally (WSP, codes).

Alignment module

Create a small, separate mapping file declaring minimal equivalences/subclassing between SALMON and DFO terms (no imports; just mappings).

Validate with ROBOT + reasoner + SPARQL checks from the CQs. (Our CONVENTIONS include ROBOT commands & QA workflow.)

Why this all fits our rules

OWL2: Respect import closure and type constraints; keep properties consistently typed; use version IRIs.

OBO principles: Prefer reuse, clear PURLs, and durable governance (should NCEAS pursue OBO membership later).

DFO CONVENTIONS: Hybrid OWL+SKOS+SHACL; MIREOT-first for small sets; no instances in schema; label+definition everywhere; RO before mint.

If you want, I can draft the exact Turtle diffs for an NCEAS PR (removing the DwC owl:ObjectProperty typings, carving out a SKOS “Fish Measurement Method” scheme, and stubbing a SALMON–DFO alignment module).
