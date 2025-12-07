# ADR Template

An Architecture Decision Record (ADR) is a concise document that captures an important architectural decision made during the development of a project, along with its context, consequences, and rationale. Use an ADR whenever a significant decision is made that could affect the project's architecture, structure, technology choices, or development approach—especially decisions that might later be questioned or revisited. 

ADRs are useful because they create a permanent, discoverable history of why decisions were made, what alternatives were considered, and what trade-offs were accepted. This helps current and future contributors understand the reasoning behind the system's design, facilitates onboarding, and improves transparency and accountability across the team.


When creating new Architecture Decision Records (ADRs), use this template:

```markdown
# ADR-XXX: [Title]

**Date:** YYYY-MM-DD  
**Status:** Proposed/Accepted/Deprecated/Superseded  
**Context:** [Brief description of the context and problem statement]

## Decision

[The change that we're proposing or have agreed to implement]

## Rationale

[Why did we make this decision?]

## Alternatives Considered

[What other options were evaluated? Why were they rejected?]

## Consequences

**Positive:**

- [List positive consequences]

**Negative:**

- [List negative consequences]

## Implementation

[How will this be implemented? What are the next steps?]
```

## Status Values

- **Proposed**: Under discussion, not yet decided
- **Accepted**: Decision has been made and approved
- **Deprecated**: Decision is no longer recommended but still documented
- **Superseded**: Decision has been replaced by a newer ADR

## Guidelines

1. **Keep it concise**: ADRs should be focused and to the point
2. **Include context**: Explain why the decision was needed
3. **Document alternatives**: Always include an "Alternatives Considered" section showing what other options were evaluated and why they were rejected
4. **Be honest about trade-offs**: Include both positive and negative consequences
5. **Provide implementation details**: Include concrete next steps
6. **Use clear language**: Write for future developers who weren't part of the decision
