# DFO Salmon Ontology - Todo List

**Last Updated:** 2025-01-27  
**Status:** Active development for FSAR Advice Trace (2-month critical path)

## Priority 1: Ontology Investigation and Integration

### PR-001: Data Product Ontology (DPROD) Integration

**Priority:** High | **Timeline:** Week 1-2 | **Scope:** Ontology integration

#### Commit 1.1: DPROD Investigation and Mapping

- [ ] Research Data Product Ontology (DPROD) specification and classes
- [ ] Map existing DFO Salmon Ontology classes to DPROD classes
- [ ] Investigate how to replace generic `Dataset` with DPROD `DataProduct`
- [ ] Document integration strategy and requirements
- [ ] Create mapping between `dfo:EscapementMeasurement` and DPROD classes

#### Commit 1.2: DPROD Integration Implementation

- [ ] Import DPROD ontology into DFO Salmon Ontology
- [ ] Create subclasses of DPROD classes for salmon-specific data products
- [ ] Update existing dataset references to use DPROD classes
- [ ] Test integration with sample data
- [ ] Update documentation and examples

### PR-002: Genetics Classes Investigation and Updates

**Priority:** High | **Timeline:** Week 3-4 | **Scope:** Ontology extensions

#### Commit 2.1: Genetics Class Review

- [ ] Review existing genetics classes for completeness and accuracy
- [ ] Investigate replacement of `dfo:GSIRun` with `dfo:AnalysisRun`
- [ ] Document current genetics class limitations and gaps
- [ ] Create plan for genetics class improvements
- [ ] Consult with genetics domain experts

#### Commit 2.2: Genetics Class Updates

- [ ] Replace `dfo:GSIRun` with `dfo:AnalysisRun` throughout ontology
- [ ] Update related properties and relationships
- [ ] Add missing genetics classes and properties
- [ ] Test updated genetics classes with sample data
- [ ] Update documentation and examples

### PR-003: Terminology Investigation

**Priority:** High | **Timeline:** Week 3-4 | **Scope:** Terminology research

#### Commit 3.1: DFO CSAS Terminology Research

- [ ] Research DFO Canadian Science Advisory Secretariat terminology
- [ ] Investigate appropriate terms for scientific advice/recommendations
- [ ] Document DFO CSAS terminology and usage patterns
- [ ] Create recommendations for terminology updates

#### Commit 3.2: Decision Terminology Investigation

- [ ] Investigate "DecisionContext" vs "Decision" terminology
- [ ] Research fisheries management decision terminology
- [ ] Document decision-making terminology in DFO context
- [ ] Create recommendations for decision-related class names
- [ ] Update ontology with chosen terminology

### PR-004: SIL/SEN Integration Investigation

**Priority:** Medium | **Timeline:** Week 7-8 | **Scope:** Integration research

#### Commit 4.1: Minh Doan PR Review

- [ ] Review Minh Doan's PR for Stream Inspection Logs (SIL) terms
- [ ] Review Minh Doan's PR for Escapement Narratives (SEN) terms
- [ ] Document SIL/SEN terminology and relationships
- [ ] Investigate integration with existing escapement measurement classes
- [ ] Create integration plan for SIL/SEN terms

#### Commit 4.2: SIL/SEN Integration Implementation

- [ ] Integrate SIL terms into DFO Salmon Ontology
- [ ] Integrate SEN terms into DFO Salmon Ontology
- [ ] Create relationships between SIL/SEN and escapement measurements
- [ ] Test integration with sample data
- [ ] Update documentation and examples

## Priority 2: Graph Database Implementation

### PR-005: Graph Database Setup

**Priority:** High | **Timeline:** Week 1-2 | **Scope:** Infrastructure

#### Commit 5.1: Fuseki Graph Database Setup

- [ ] Set up Apache Jena Fuseki in Docker environment
- [ ] Create core graphs: `graph:vocab`, `graph:shapes`, `graph:fsar:2025:barkley`
- [ ] Configure Fuseki for JSON-LD data loading
- [ ] Test basic SPARQL querying capabilities
- [ ] Document setup and configuration procedures

#### Commit 5.2: Data Loading and Testing

- [ ] Load SKOS vocabulary terms into `graph:vocab`
- [ ] Load SHACL shapes into `graph:shapes`
- [ ] Load Barkley Sockeye data into `graph:fsar:2025:barkley`
- [ ] Test data loading procedures with sample data
- [ ] Create data loading automation scripts

### PR-006: Advanced Graph Database Features

**Priority:** Medium | **Timeline:** Week 5-6 | **Scope:** Infrastructure enhancement

#### Commit 6.1: Performance Optimization

- [ ] Optimize Fuseki configuration for performance
- [ ] Implement caching strategies for SPARQL queries
- [ ] Test performance with realistic data volumes
- [ ] Document performance optimization procedures
- [ ] Create monitoring and maintenance procedures

#### Commit 6.2: DPROD Integration Support

- [ ] Add `graph:dprod` for Data Product Ontology integration
- [ ] Implement DPROD-specific data loading procedures
- [ ] Test DPROD integration with sample data
- [ ] Create DPROD-specific SPARQL queries
- [ ] Document DPROD integration procedures

## Priority 3: SPARQL Query Implementation

### PR-007: Core SPARQL Query Pack

**Priority:** High | **Timeline:** Week 3-4 | **Scope:** Query implementation

#### Commit 7.1: MVP SPARQL Queries

- [ ] Implement Q1: Evidence Completeness by Decision
- [ ] Implement Q2: Proxy Without Justification
- [ ] Implement Q3: Method Reproducibility
- [ ] Implement Q4: Reference Points Used
- [ ] Test queries against sample Barkley data

#### Commit 7.2: Data Currency and Quality Queries

- [ ] Implement Q5: Missing Uncertainty
- [ ] Implement Q6: Data Currency
- [ ] Implement Q7: Scientific Output Text + Review
- [ ] Implement Q8: Linked Documents
- [ ] Test queries and validate results

#### Commit 7.3: DPROD Integration Queries

- [ ] Implement Q9: Data Product Integration
- [ ] Create additional DPROD-specific queries
- [ ] Test DPROD queries with sample data
- [ ] Document query usage and examples
- [ ] Create query performance benchmarks

## Priority 4: SHACL Validation Implementation

### PR-008: SHACL Validation Shapes

**Priority:** High | **Timeline:** Week 3-4 | **Scope:** Validation rules

#### Commit 8.1: Core Validation Shapes

- [ ] Create SHACL shapes for Advice Trace entities
- [ ] Add validation rules for required properties by decision context
- [ ] Add validation for data quality and completeness
- [ ] Test shapes against sample data
- [ ] Document validation rules and procedures

#### Commit 8.2: Quality Assurance Shapes

- [ ] Add shapes for uncertainty propagation validation
- [ ] Add shapes for provenance completeness
- [ ] Add shapes for document linking validation
- [ ] Create validation report templates
- [ ] Test comprehensive validation scenarios

## Priority 5: UI/UX Implementation

### PR-009: Django HTMX Timeline Interface

**Priority:** Medium | **Timeline:** Week 5-6 | **Scope:** Frontend implementation

#### Commit 9.1: Basic Timeline Structure

- [ ] Create Django templates for Advice Trace timeline
- [ ] Implement HTMX partials for Evidence Drawer
- [ ] Add SMU/Year picker interface
- [ ] Create responsive layout for timeline nodes
- [ ] Test basic UI functionality

#### Commit 9.2: Evidence Badges and Risk Chips

- [ ] Implement evidence completeness badges (Complete/Gaps/Missing-Critical)
- [ ] Add risk chip components for specific CQ findings
- [ ] Create hover tooltips with key facts
- [ ] Add click handlers for drawer navigation
- [ ] Test badge and chip functionality

#### Commit 9.3: Evidence Drawer Implementation

- [ ] Create drawer tabs (Overview, Inputs, Methods, Benchmarks, Quality, Documents, Currency)
- [ ] Implement provenance display with source, method, code commit
- [ ] Add document listing with download links
- [ ] Create currency panel with last-updated timestamps
- [ ] Test drawer functionality and navigation

### PR-010: Data Integration and API

**Priority:** Medium | **Timeline:** Week 5-6 | **Scope:** Backend integration

#### Commit 10.1: Django REST Framework (DRF) JSON-LD Endpoints

- [ ] Create `/api/advice-trace/{smu}/{year}` endpoint
- [ ] Create `/api/documents?smu=&year=` endpoint
- [ ] Create `/api/cq/{smu}/{year}` endpoint for CQ results
- [ ] Add JSON-LD context and serialization
- [ ] Test API endpoints with sample data

#### Commit 10.2: SPARQL Adapter Integration

- [ ] Create SPARQL adapter class for Fuseki integration
- [ ] Implement query execution and result mapping
- [ ] Add caching layer for SPARQL results
- [ ] Create data transfer objects (DTO) for UI data transfer
- [ ] Test SPARQL adapter with various queries

#### Commit 10.3: Anti-Corruption Layer

- [ ] Create ACL mappers for SPSR models to ontology terms
- [ ] Implement SKOS/JSON-LD context mapping
- [ ] Add validation for ontology term usage
- [ ] Create mapping documentation
- [ ] Test ACL with sample SPSR data

## Priority 6: Data Export and Documentation

### PR-011: Advice Trace Pack Export

**Priority:** Medium | **Timeline:** Week 5-6 | **Scope:** Export functionality

#### Commit 11.1: Export Pack Generation

- [ ] Create Advice Trace Pack export functionality
- [ ] Include trace.jsonld, evidence CSVs, figures, and PDF report
- [ ] Add SPARQL queries and PROV documentation
- [ ] Create README for exported packs
- [ ] Test export functionality with sample data

#### Commit 11.2: Document Integration

- [ ] Link to FSAR/Tech/Research documents
- [ ] Add pre-signed URL generation for internal docs
- [ ] Create document metadata extraction
- [ ] Add citation formatting
- [ ] Test document integration and access

### PR-012: Documentation Updates

**Priority:** Low | **Timeline:** Week 7-8 | **Scope:** Documentation

#### Commit 12.1: Ontology Documentation

- [ ] Update README with new classes and properties
- [ ] Create usage examples for Advice Trace entities
- [ ] Document SPARQL query patterns
- [ ] Add SHACL validation examples
- [ ] Update CONVENTIONS.md with new patterns

#### Commit 12.2: User Documentation

- [ ] Create FSAR Advice Trace user guide
- [ ] Document evidence completeness criteria
- [ ] Create troubleshooting guide
- [ ] Add executive summary for stakeholders
- [ ] Create developer documentation

## Priority 7: Testing and Validation

### PR-013: Comprehensive Testing

**Priority:** High | **Timeline:** Week 7-8 | **Scope:** Quality assurance

#### Commit 13.1: Unit Tests

- [ ] Test ontology extensions with sample data
- [ ] Test SPARQL queries with various scenarios
- [ ] Test SHACL validation rules
- [ ] Test Django views and API endpoints
- [ ] Create automated test suite

#### Commit 13.2: Integration Tests

- [ ] Test full Advice Trace workflow with Barkley data
- [ ] Test evidence completeness calculations
- [ ] Test document linking and export functionality
- [ ] Test performance with realistic data volumes
- [ ] Create integration test scenarios

#### Commit 13.3: Acceptance Testing

- [ ] Validate against UX specification requirements
- [ ] Test with stakeholder feedback
- [ ] Verify evidence badges and risk chips accuracy
- [ ] Test export pack completeness
- [ ] Create acceptance test criteria

## Completed Tasks

## Notes

- **Timeline:** Following 2-month critical path from ontology requirements document
- **Priority Order:** Bugs/security first, then by importance and dependencies
- **Scope:** Each commit is small and reversible for safe development
- **Integration:** Building on existing ontology structure rather than replacing it
- **Testing:** Comprehensive testing planned for Week 7-8 before stakeholder demo
- **Investigation Focus:** Many tasks require investigation before implementation
- **MVP Definition:** Clear separation between MVP features and future enhancements

## Dependencies

- **Week 1-2:** Graph database setup must be completed before SPARQL queries
- **Week 3-4:** Ontology investigations must be completed before implementation
- **Week 5-6:** SPARQL queries needed before UI implementation
- **Week 7-8:** All components needed before acceptance testing

## Risks and Mitigations

- **Ontology Changes:** Use versioned IRIs and backward compatibility
- **Data Integration:** Use anti-corruption layer to isolate SPSR changes
- **Performance:** Implement caching and optimize SPARQL queries
- **User Adoption:** Focus on stakeholder feedback and iterative improvement
- **Investigation Dependencies:** Some tasks depend on research outcomes
- **Terminology Changes:** May require significant refactoring if terminology changes
