# DFO Salmon Ontology - Product Requirements Document

**Namespace:** `https://w3id.org/dfo/salmon#` (prefix: `dfo:`)  
**License:** CC-BY 4.0  
**Status:** Draft Work in Progress  
**Version:** 0.2.0

---

## 1. Product Vision & Mission

### 1.1 Primary Purpose

The DFO Salmon Ontology is a **data stewardship and operational process ontology** designed to provide a semantic framework for managing, integrating, and stewarding Pacific salmon data across Fisheries and Oceans Canada (DFO). Fundamentally, this data ontology serves as a Salmon-science-wide, standard digital language that enables easy information sharing and collaboration.

**This is NOT a biological domain ontology** about salmon ecology or behavior, but rather an **operational ontology** that models:

- **Data collection processes** (surveys, sampling, monitoring)
- **Data analysis workflows** (stock assessments, genetic analyses, status evaluations)
- **Data management operations** (quality control, validation, integration)
- **Data products and outputs** (reports, visualizations, management advice)
- **Organizational structures** (management units, conservation units, stock hierarchies)
- **Regulatory and policy frameworks** (Wild Salmon Policy, Precautionary Approach, COSEWIC)

### 1.2 Mission Statement

Make salmon data interoperable, discoverable, and analyzable with minimal friction for scientists, data stewards, and managers across DFO and partner organizations.

---

## 2. Core Objectives

### 2.1 Data Stewardship & Quality
- Standardize terminology across DFO salmon data systems
- Enable data quality assessment through formal validation rules
- Support data lineage tracking from collection to publication
- Facilitate data governance and compliance with regulatory requirements

### 2.2 Data Integration & Interoperability
- Integrate data across stock assessment, genetics (GSI/PBT), and management domains
- Enable cross-system queries and data discovery
- Support data sharing with external partners (GBIF, OBIS, international organizations)
- Align with community standards (Darwin Core, OBO Foundry principles)

### 2.3 Operational Process Mapping
- Document DFO workflows from data collection to management decisions
- Model analytical processes (Kobe plots, run reconstruction, trade-off analyses)
- Track data transformations and processing steps
- Support process automation and workflow management

### 2.4 Regulatory Compliance & Reporting
- Support Wild Salmon Policy implementation and reporting
- Enable Precautionary Approach framework compliance
- Facilitate COSEWIC status assessments and reporting
- Support Fisheries Act requirements and data transparency

---

## 3. What This Ontology Models

### 3.1 Operational Entities (What DFO Does)
- Survey events and measurement protocols
- Stock assessment methodologies
- Genetic analysis workflows
- Data quality control processes
- Management decision frameworks

### 3.2 Organizational Structures (How DFO is Organized)
- Management Units (MUs)
- Conservation Units (CUs)
- Stock hierarchies and relationships
- Reporting unit structures
- Geographic and administrative boundaries

### 3.3 Regulatory Frameworks (What DFO Must Follow)
- Wild Salmon Policy requirements
- Precautionary Approach framework
- COSEWIC assessment criteria
- Fisheries Act compliance
- Data transparency obligations

---

## 4. Target Users & Use Cases

### 4.1 Data Stewards
**Primary Use Cases:**
- **Data quality assessment**: "What validation rules apply to escapement measurements?"
- **Data lineage tracking**: "What processes were used to generate this stock assessment?"
- **Data integration**: "How do genetic reporting units map to conservation units?"

**Success Criteria:**
- Reduced time to validate data quality
- Clear audit trails for all data transformations
- Automated quality control workflows

### 4.2 Scientists & Analysts
**Primary Use Cases:**
- **Method documentation**: "What analytical methods were used for 2022 assessments?"
- **Data discovery**: "What escapement data exists for Skeena River stocks?"
- **Process automation**: "What are the standard workflows for run reconstruction?"

**Success Criteria:**
- Faster data discovery and access
- Standardized analytical workflows
- Improved reproducibility of analyses

### 4.3 Managers & Policy Makers
**Primary Use Cases:**
- **Compliance reporting**: "What stocks are in critical status zones?"
- **Decision support**: "What reference points apply to this management unit?"
- **Policy implementation**: "How do we track Wild Salmon Policy compliance?"

**Success Criteria:**
- Automated compliance reporting
- Clear decision support frameworks
- Transparent policy implementation tracking

### 4.4 External Partners
**Primary Use Cases:**
- **Data sharing**: "What DFO salmon data is available for integration?"
- **Standard compliance**: "How does DFO data align with Darwin Core standards?"
- **Interoperability**: "Can we query DFO data using standard biodiversity protocols?"

**Success Criteria:**
- Seamless data sharing with international partners
- Full compliance with biodiversity data standards
- Global discoverability of DFO salmon data

---

## 5. Functional Requirements

### 5.1 Stock Assessment Domain
**Core Capabilities:**
- Model escapement survey events and measurement protocols
- Support automated estimate type assignment (Hyatt 1997 framework)
- Track methodology usage across stocks and time periods
- Enable trend analysis and population monitoring


### 5.2 Genetics/GSI Domain
**Core Capabilities:**
- Model genetic sample collection and analysis workflows
- Support GSI composition measurements and reporting
- Track assay and marker panel usage
- Enable genetic stock identification queries


### 5.3 Management & Policy Domain
**Core Capabilities:**
- Model conservation status and management zones
- Support regulatory compliance tracking
- Enable policy implementation monitoring
- Track management unit hierarchies

### 5.4 Data Stewardship Domain
**Core Capabilities:**
- Support data quality validation workflows
- Enable data lineage tracking
- Provide automated classification systems
- Support data governance frameworks

---

## 6. Non-Functional Requirements

### 6.1 Interoperability Requirements
- **Darwin Core Alignment**: Must extend DwC classes and use DwC predicates where applicable
- **OBO Foundry Compliance**: Must follow OBO Foundry principles for open, interoperable ontologies
- **External Vocabulary Integration**: Must align with QUDT (units), ENVO (environments), GBIF Backbone (taxa)
- **International Standards**: Must support data sharing with GBIF, OBIS, and other biodiversity platforms

### 6.2 Data Quality Requirements
- **Validation Rules**: Must provide SHACL-based validation for all data types
- **Automated Classification**: Must support automated estimate type assignment
- **Quality Metrics**: Must track and report data quality indicators
- **Audit Trails**: Must maintain complete lineage tracking for all data transformations

### 6.3 Performance Requirements
- **Query Performance**: Must support complex SPARQL queries with sub-second response times
- **Scalability**: Must handle datasets with millions of measurements and events
- **Reasoning Performance**: Must complete logical reasoning within acceptable time limits
- **Validation Performance**: Must validate large datasets within reasonable timeframes

### 6.4 Usability Requirements
- **Documentation**: Must provide comprehensive documentation for all user types
- **Training Materials**: Must include training resources for new users
- **Tool Support**: Must work with standard ontology tools (Protégé, ROBOT)
- **Community Support**: Must provide clear contribution guidelines and support channels

---

## 7. Success Metrics & Release Criteria

### 7.1 Competency Question Coverage
- **Target**: 100% of REQUIRED competency questions must be answerable
- **Measurement**: SPARQL query tests must return expected results
- **Current Status**: 2 of 3 REQUIRED questions implemented (67%)

### 7.2 Validation Pass Rates
- **Target**: 100% of validation checks must pass
- **Measurement**: ROBOT validation, SHACL validation, and reasoning checks
- **Current Status**: All current validation checks passing

### 7.3 External Alignment Completion
- **Target**: 100% alignment with required external vocabularies
- **Measurement**: All required external references must be valid and accessible
- **Current Status**: Darwin Core, QUDT, ENVO alignments in progress

### 7.4 Community Adoption Metrics
- **Target**: Active community of contributors and users
- **Measurement**: GitHub activity, issue resolution, documentation usage
- **Current Status**: Initial community engagement phase

### 7.5 Release Criteria for v1.0
- [ ] All REQUIRED competency questions implemented and tested
- [ ] Complete external vocabulary alignments
- [ ] Full documentation suite completed
- [ ] Community review and approval
- [ ] Production-ready validation and quality control systems

---

## 8. Stakeholder Requirements

### 8.1 Primary Stakeholders
- **DFO Data Stewards**: Need standardized terminology and quality control
- **DFO Scientists**: Need data integration and analysis capabilities
- **DFO Managers**: Need compliance and reporting support
- **External Partners**: Need interoperable data sharing capabilities

### 8.2 Secondary Stakeholders
- **International Organizations**: Need standards-compliant data access
- **Academic Researchers**: Need comprehensive salmon data for research
- **Conservation Groups**: Need transparent access to conservation status data
- **Industry Partners**: Need reliable data for sustainable fisheries management

---

## 9. Out of Scope

### 9.1 Explicitly Excluded
- **Biological Domain Modeling**: This is not a biological ontology about salmon ecology or behavior
- **Instance Data Storage**: The ontology repository does not store actual survey data or measurements
- **Data Collection Systems**: Does not include tools for data entry or collection
- **Visualization Tools**: Does not include user interfaces or visualization components

### 9.2 Future Considerations
- **Modular Architecture**: May split into domain-specific modules as complexity grows
- **Advanced Analytics**: May add support for complex analytical workflows
- **Real-time Integration**: May add support for real-time data integration
- **Machine Learning**: May add support for ML-based data quality assessment

---

## 10. Roadmap Alignment

### 10.1 Phase 1: Foundation (Current - v0.2.0)
- ✅ Core class and property definitions
- ✅ Basic measurement patterns
- ✅ Stock hierarchy implementation
- ✅ Darwin Core alignment
- ✅ Competency questions with SPARQL queries
- ✅ Repository structure conforming to AGENTS.md

### 10.2 Phase 2: Expansion (v0.3.0 - v0.5.0)
- Fill missing `rdfs:comment` definitions
- Add genetic analysis workflows
- Implement advanced measurement types
- External vocabulary integration
- Quality control patterns

### 10.3 Phase 3: Integration (v0.6.0 - v0.8.0)
- NCEAS Salmon Ontology alignment
- International standard compliance
- Advanced querying capabilities
- Data validation tools

### 10.4 Phase 4: Policy and Integration (v0.9.0 - v1.0.0)
- Policy benchmarks and reference points
- Integration with NCEAS Salmon Ontology
- Advanced querying and analytics
- Publish docs via pyLODE/Widoco
- Register W3ID redirects

---

## 11. Dependencies & Constraints

### 11.1 Technical Dependencies
- **Java 11+**: Required for ROBOT toolchain
- **Python 3.11+**: Required for validation scripts
- **W3ID Service**: Required for persistent identifier resolution
- **External Vocabularies**: Darwin Core, QUDT, ENVO, GBIF Backbone

### 11.2 Organizational Constraints
- **DFO Governance**: Must align with DFO data governance policies
- **Regulatory Compliance**: Must support Fisheries Act and Wild Salmon Policy requirements
- **Resource Limitations**: Development constrained by available personnel and budget
- **Timeline Constraints**: Must align with DFO planning cycles and reporting requirements

### 11.3 Community Constraints
- **OBO Foundry Standards**: Must maintain compliance with OBO Foundry principles
- **International Standards**: Must align with biodiversity informatics standards
- **Open Source Requirements**: Must maintain open source licensing and community access

---

*This Product Requirements Document serves as the authoritative source for product vision, user needs, functional and non-functional requirements, and success criteria for the DFO Salmon Ontology project.*

*For specific competency questions and technical implementation details, see [COMPETENCY_QUESTIONS.md](COMPETENCY_QUESTIONS.md).*

*For detailed modeling conventions and development guidelines, see [CONVENTIONS.md](CONVENTIONS.md).*
