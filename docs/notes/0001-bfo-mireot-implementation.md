# Note 0001: BFO MIREOT Implementation

**Date:** 2025-01-27  
**Related Issue:** [#4](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/4)  
**Related PR:** [#5](https://github.com/dfo-pacific-science/dfo-salmon-ontology/pull/5)  
**Branch:** `feature/bfo-mireot-imports-issue-4`

## What Changed

Implemented upper ontology grounding for the DFO Salmon Ontology using BFO (Basic Formal Ontology) via the MIREOT methodology.

### Ontology Changes

**File:** `ontology/dfo-salmon.ttl`

1. **Added BFO MIREOT Section** (after line 234)
   - Imported 3 essential BFO classes with full metadata:
     - `bfo:0000015` (process)
     - `bfo:0000040` (material entity)
     - `bfo:0000031` (generically dependent continuant)
   - Each term includes: rdfs:label, oboInOwl:hasDefinition, rdfs:isDefinedBy

2. **Updated DwC-to-BFO Mappings** (lines 218-235)
   - Changed section title to "Class Mappings to Darwin Core and BFO Upper Ontology"
   - Updated comments for clarity (material entities, processes, information entities)
   - Clarified that IAO extends BFO (iao:0000030 is subclass of bfo:0000031)

### Documentation Changes

1. **README.md** - Technical Overview
   - Added: "Pragmatic imports: MIREOT for BFO/IAO/DQV (~12 terms)"
   - Added: "Upper ontology: BFO grounding for process/entity hierarchy"

2. **CONVENTIONS.md** - New Section 2.3.6
   - Comprehensive "Ontology Import Strategy" section
   - Explains three approaches: Full owl:imports, MIREOT, Prefix-only
   - Decision matrix showing which ontologies use which approach
   - Examples and rationale for each approach

3. **todo_list.md** - Reorganized
   - Split old PR-001 into two PRs:
     - **PR-001**: BFO MIREOT Import and DwC Mapping (commits 1.1, 1.2)
     - **PR-002**: DQV MIREOT Import for Quality Framework (commits 2.1, 2.2, 2.3)
   - Renumbered all subsequent PRs (PR-003 through PR-012)
   - Added genetics integration (PR-004) and SIL/SEN integration (PR-005)
   - Clarified Brett's infrastructure tasks vs ontology work

## Why This Matters

### For FSAR Tracer MVP

BFO grounding enables proper typing of FSAR Tracer evidence chain classes:
- **StatusAssessment** → subclass of bfo:0000015 (process)
- **AnalysisMethod** → subclass of bfo:0000015 (process)
- **ManagementDecision** → subclass of bfo:0000015 (process)
- **ScientificOutput** → subclass of iao:0000030 (information content entity, which extends BFO)

### For Interoperability

- **OBO Foundry Compliance**: Most OBO ontologies (including IAO) are BFO-grounded
- **Better Reasoning**: Proper upper ontology enables sophisticated logical inference
- **Semantic Clarity**: Clear distinction between processes, entities, and information

### Why MIREOT Instead of Full Import

- **Performance**: BFO has 100+ terms; we need only 3
- **Lightweight**: No dependency bloat
- **Documentation**: Terms are documented locally in our ontology
- **Flexibility**: Can update/evolve independently of BFO releases

## MIREOT Methodology Explained

**MIREOT** = Minimum Information to Reference an External Ontology Term

A term import approach that:
1. Identifies specific terms needed from external ontology
2. Copies IRI, label, and definition into local ontology
3. Uses `rdfs:isDefinedBy` to point back to source
4. Enables use without full import

**When to Use:**
- Need 3-20 terms (not 1-2, not 50+)
- Want local documentation
- Don't need full ontology reasoning
- Want to keep ontology lightweight

## Related Work

This PR is foundational for:
- **PR-002**: DQV MIREOT imports for evidence completeness
- **PR-003**: FSAR Tracer core classes (StatusAssessment, ScientificOutput, etc.)
- **PR-008**: SPARQL queries requiring proper class typing

Without BFO grounding, we'd have difficulty:
- Clearly distinguishing processes from entities
- Aligning with OBO Foundry standards
- Enabling sophisticated reasoning in Fuseki
- Integrating with other BFO-based ontologies

## Next Steps

1. **PR Review**: Awaiting review and merge of PR #5
2. **PR-002**: Implement DQV MIREOT imports for quality framework
3. **PR-003**: Add FSAR Tracer core classes using BFO grounding
4. **Testing**: Validate ontology in Protégé with ELK reasoner

## Open Questions

None - this PR is complete and ready for review.

## Lessons Learned

1. **MIREOT is ideal for selective imports** - No need to import entire upper ontologies
2. **Documentation is key** - Including labels/definitions makes MIREOT terms discoverable
3. **BFO + IAO work together** - IAO extends BFO; they're complementary
4. **Clear commit strategy** - Splitting BFO from DQV made this PR focused and reviewable

