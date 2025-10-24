# DFO Salmon Ontology - Prioritized Action Items

**Generated:** 2025-10-24  
**Based on:** Comprehensive Quality Analysis Report  

## Action Item Summary

| Priority | Count | Effort | Timeline |
|----------|-------|--------|----------|
| P0 (Critical) | 2 | Small | Week 1-2 |
| P1 (High) | 2 | Large | Week 3-8 |
| P2 (Medium) | 2 | Medium | Week 9-12 |
| P3 (Low) | 1 | Small | Week 13+ |

---

## Priority 0 (Critical - Must Fix)

### P0-1: Resolve SKOS Label Strategy Conflict
**Issue**: 31 SKOS concepts have `skos:prefLabel` but ROBOT expects `rdfs:label`

**Impact**: 31 ERROR violations, blocks quality gates

**Effort**: Small (2-4 hours)

**Dependencies**: None

**Approach**: Add `rdfs:label` matching `skos:prefLabel` for all SKOS concepts

**Implementation Steps**:
1. Extract all SKOS concepts with `skos:prefLabel` but no `rdfs:label`
2. Add `rdfs:label` annotations matching the `skos:prefLabel` values
3. Test with ROBOT to confirm ERROR violations resolved
4. Update CONVENTIONS.md to document dual-label strategy

**Files to Modify**:
- `ontology/dfo-salmon.ttl` (add 31 rdfs:label annotations)
- `docs/CONVENTIONS.md` (document label strategy)

**Success Criteria**:
- 0 ERROR violations for missing labels on SKOS concepts
- All SKOS concepts have both `skos:prefLabel` and `rdfs:label`

---

### P0-2: Fix Annotation Whitespace
**Issue**: `ExploitationRate` has trailing whitespace in `dc:bibliographicCitation`

**Impact**: 1 WARN violation, affects annotation quality

**Effort**: Small (15 minutes)

**Dependencies**: None

**Approach**: Clean up whitespace in citation annotation

**Implementation Steps**:
1. Locate `ExploitationRate` annotation in `ontology/dfo-salmon.ttl`
2. Remove trailing whitespace from citation
3. Test with ROBOT to confirm WARN violation resolved

**Files to Modify**:
- `ontology/dfo-salmon.ttl` (fix whitespace)

**Success Criteria**:
- 0 WARN violations for annotation whitespace
- Clean, properly formatted annotations

---

## Priority 1 (High - Should Fix)

### P1-1: Add Missing Definitions for Core Terms
**Issue**: 147 DFO terms lack definitions, affecting ontology usability

**Impact**: 147 WARN violations, reduced ontology quality

**Effort**: Large (20-40 hours)

**Dependencies**: Domain expertise, competency questions review

**Approach**: Systematic definition addition prioritizing core terms

**Implementation Steps**:
1. **Week 3**: Identify top 20 core terms requiring definitions
   - Stock, ConservationUnit, EscapementMeasurement, etc.
   - Focus on terms directly supporting competency questions
2. **Week 4-5**: Add definitions for core terms
   - Use existing definitions as templates
   - Ensure consistency with domain terminology
3. **Week 6-7**: Add definitions for secondary terms
   - Methods, measurements, properties
   - Maintain consistent style and depth
4. **Week 8**: Review and refine all new definitions

**Files to Modify**:
- `ontology/dfo-salmon.ttl` (add definitions)
- `docs/CONVENTIONS.md` (add definition guidelines)

**Success Criteria**:
- 80%+ of DFO terms have definitions
- All core terms have clear, consistent definitions
- Definitions support competency questions

---

### P1-2: Review and Add Superclass Relationships
**Issue**: 52 classes lack explicit parent relationships

**Impact**: 52 INFO violations, unclear class hierarchy

**Effort**: Large (15-25 hours)

**Dependencies**: BFO understanding, domain expertise

**Approach**: Systematic review of class hierarchy

**Implementation Steps**:
1. **Week 3-4**: Review all 52 classes without superclasses
   - Identify appropriate BFO grounding
   - Document cases where no superclass is needed
2. **Week 5-6**: Add superclass relationships where appropriate
   - Use BFO classes (Entity, Process, Continuant, etc.)
   - Maintain logical consistency
3. **Week 7-8**: Validate hierarchy with reasoners
   - Ensure no unsatisfiable classes
   - Test classification results

**Files to Modify**:
- `ontology/dfo-salmon.ttl` (add superclass axioms)
- `docs/CONVENTIONS.md` (document hierarchy patterns)

**Success Criteria**:
- 90%+ of classes have explicit superclasses
- Clear, logical class hierarchy
- No unsatisfiable classes

---

## Priority 2 (Medium - Consider Fixing)

### P2-1: Document Darwin Core Import Strategy
**Issue**: 8 Darwin Core terms lack local labels, causing ROBOT warnings

**Impact**: 8 ERROR violations, unclear import strategy

**Effort**: Medium (2-4 hours)

**Dependencies**: Decision on import strategy

**Approach**: Document acceptable practice for external imports

**Implementation Steps**:
1. Review Darwin Core import strategy
2. Document decision in CONVENTIONS.md
3. Configure ROBOT or document as acceptable
4. Update AGENTS.md with import guidelines

**Files to Modify**:
- `docs/CONVENTIONS.md` (document import strategy)
- `docs/AGENTS.md` (add import guidelines)

**Success Criteria**:
- Clear documentation of import strategy
- Consistent approach to external terms
- Reduced confusion for contributors

---

### P2-2: Enhance BFO MIREOT Documentation
**Issue**: 3 BFO terms lack definitions, causing ROBOT warnings

**Impact**: 3 WARN violations, unclear MIREOT strategy

**Effort**: Medium (1-2 hours)

**Dependencies**: BFO documentation review

**Approach**: Document MIREOT strategy and expected limitations

**Implementation Steps**:
1. Review BFO MIREOT implementation
2. Document strategy in CONVENTIONS.md
3. Explain why BFO terms lack local definitions
4. Update AGENTS.md with MIREOT guidelines

**Files to Modify**:
- `docs/CONVENTIONS.md` (document MIREOT strategy)
- `docs/AGENTS.md` (add MIREOT guidelines)

**Success Criteria**:
- Clear documentation of MIREOT approach
- Contributors understand BFO import limitations
- Reduced confusion about external term handling

---

## Priority 3 (Low - Future Consideration)

### P3-1: Establish Ongoing Quality Assurance Process
**Issue**: Need systematic approach to maintain ontology quality

**Impact**: Long-term quality maintenance

**Effort**: Small (4-8 hours)

**Dependencies**: Completion of P0-P2 items

**Approach**: Create automated quality checks and contributor guidelines

**Implementation Steps**:
1. Create ROBOT report automation
2. Establish quality gates for PRs
3. Create contributor checklist
4. Set up regular quality reviews

**Files to Modify**:
- `scripts/quality-check.bat` (new file)
- `docs/CONTRIBUTING.md` (add quality guidelines)
- `.github/workflows/` (add CI quality checks)

**Success Criteria**:
- Automated quality checking
- Clear contributor guidelines
- Consistent quality maintenance

---

## Implementation Timeline

### Week 1-2: Critical Fixes
- [ ] P0-1: Resolve SKOS label strategy (2-4 hours)
- [ ] P0-2: Fix annotation whitespace (15 minutes)
- [ ] Test and validate fixes

### Week 3-8: High Priority Items
- [ ] P1-1: Add core term definitions (20-40 hours)
- [ ] P1-2: Review superclass relationships (15-25 hours)
- [ ] Regular testing and validation

### Week 9-12: Medium Priority Items
- [ ] P2-1: Document Darwin Core strategy (2-4 hours)
- [ ] P2-2: Enhance BFO documentation (1-2 hours)
- [ ] Update contributor guidelines

### Week 13+: Future Enhancements
- [ ] P3-1: Establish quality assurance process (4-8 hours)
- [ ] Ongoing maintenance and improvements

---

## Resource Requirements

### Domain Expertise
- Salmon biology and management knowledge
- Ontology modeling experience
- BFO and Darwin Core familiarity

### Technical Skills
- OWL/SKOS modeling
- ROBOT toolchain
- Documentation writing

### Time Estimates
- **Total Effort**: 40-80 hours
- **Critical Path**: 2-4 weeks for P0-P1 items
- **Full Implementation**: 3-4 months

---

## Success Metrics

### Immediate (Week 2)
- 0 ERROR violations
- 1 WARN violation (annotation whitespace fixed)
- 52 INFO violations (unchanged)

### Short-term (Week 8)
- 0 ERROR violations
- <50 WARN violations (definitions added)
- <20 INFO violations (superclasses added)

### Long-term (Week 12)
- 0 ERROR violations
- <20 WARN violations (documentation complete)
- <10 INFO violations (hierarchy complete)
- Established quality assurance process

---

## Risk Mitigation

### Technical Risks
- **Risk**: Adding superclasses creates logical inconsistencies
- **Mitigation**: Test with multiple reasoners after each change

### Resource Risks
- **Risk**: Insufficient domain expertise for definitions
- **Mitigation**: Collaborate with domain experts, use existing literature

### Timeline Risks
- **Risk**: Definition writing takes longer than estimated
- **Mitigation**: Prioritize core terms, use templates, iterative approach

---

## Next Steps

1. **Immediate**: Begin P0-1 (SKOS label strategy) - can start today
2. **This Week**: Complete P0-1 and P0-2 (critical fixes)
3. **Next Week**: Begin P1-1 (core definitions) planning
4. **Ongoing**: Regular testing and validation throughout implementation

**Contact**: For questions about implementation, refer to the comprehensive analysis report and CONVENTIONS.md guidelines.
