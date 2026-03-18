# Contributing to GC DFO Salmon Ontology

This file covers how to propose terms, changes, and pull requests for the GC DFO Salmon Ontology.

- For the repo build/publish runbook, see [README.md](README.md).
- For current maintainers and placeholder decision rules, see [GOVERNANCE.md](GOVERNANCE.md).

## Contribution Workflow

### 1. Check the boundary first: does this belong in `gcdfo:` or `smn:`?

Before requesting a new DFO term, check whether the concept is actually:

- **DFO-specific, policy-program-specific, or intentionally profile-scoped** → it likely belongs in this repo (`gcdfo:`)
- **Cross-organization, policy-neutral, and reusable** → it may belong in the shared Salmon Domain Ontology (`smn:`)

Useful references:
- DFO namespace docs: <https://dfo-pacific-science.github.io/dfo-salmon-ontology/>
- Shared Salmon Domain namespace: <https://w3id.org/smn>
- Shared Salmon Domain repo: <https://github.com/salmon-data-mobilization/salmon-domain-ontology>
- Canonical boundary policy for this repo: [README.md#namespace-boundary-and-shared-layer-preference](README.md#namespace-boundary-and-shared-layer-preference)

If you are unsure, open an issue and flag it as a **boundary question** rather than guessing.

### 2. Check whether the term already exists

Before submitting a new term request, check whether the term already exists, either as a primary term or a synonym.

For DFO terms, search the ontology within the [published WIDOCO site](https://dfo-pacific-science.github.io/dfo-salmon-ontology/) or browse the [canonical ontology file](https://github.com/dfo-pacific-science/dfo-salmon-ontology/blob/main/ontology/dfo-salmon.ttl) directly.

If you think the concept may be shared, also check the Salmon Domain Ontology (`smn:`) before proposing a new `gcdfo:` term.

If a synonym is missing, or the textual definition of a term needs clarification, please submit a ticket for that instead of minting a duplicate term.

### 3. Gather the information needed to review the request

**For new term requests, please include:**
- proposed **name/label**
- **definition**
- **definition source**
- expected **position in hierarchy** or concept scheme
- expected **relationships** to other terms
- synonyms or alternate labels, if applicable
- one or two short **usage examples**, if helpful

**For updates to relationships, please include:**
- the current term IRI(s)
- what is wrong or insufficient today
- exactly what should be added, removed, or changed
- why the change is needed
- any likely downstream impact, if known

**For boundary questions, please include:**
- why the term might belong in shared `smn:` instead of DFO `gcdfo:` (or vice versa)
- whether the meaning depends on a DFO policy or program context
- any known cross-organization reuse case

### 4. Open an issue or PR through the normal repo workflow

1. **Preferred path:** create an issue in the [DFO Salmon Ontology issue tracker](https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues). This gives maintainers and contributors one place to discuss scope, boundary, and implementation.
2. **If you plan to open a PR:** discuss the change in an issue first unless it is a very small fix (for example: typo, broken link, or obvious doc correction).
3. **If you are making ontology edits:** the canonical source is `ontology/dfo-salmon.ttl`. The draft file is an idea bank, not the source of truth for tests or published docs.
4. **If your PR changes ontology or publication artifacts:** run the appropriate repo checks (`make test`, `make docs-refresh`, or `make ci`, depending on scope) before asking for review.
5. **If you need non-GitHub contact:** you can contact the DFO Pacific Fishery & Assessment Data Section [Data Stewardship Unit](mailto:FADSDataStewardship-GestiondesdonneesSFDA@dfo-mpo.gc.ca), but GitHub issues are preferred because they preserve review history.

### 5. Helpful reminders

1. **Be specific.** Include enough detail that a maintainer can understand the problem, assess the boundary, and implement the change without re-deriving the context.
2. **Provide references.** For new terms especially, include source documents, papers, standards, screenshots, or URLs that show the intended meaning.
3. **Do not assume same-label means same-meaning.** A shared `smn:` term and a DFO term can look similar while carrying meaningfully different semantics.
4. **Incomplete requests may be parked for follow-up.** If the repo does not have enough information to review the request safely, maintainers may ask for more detail before proceeding.

## Getting Help

- **Issues:** use GitHub issues for questions and discussions
- **Documentation:** check existing docs in the `docs/` directory
- **Governance / maintainer questions:** see [GOVERNANCE.md](GOVERNANCE.md)
- **Published ontology docs:** <https://dfo-pacific-science.github.io/dfo-salmon-ontology/>

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and constructive in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the same [CC-BY 4.0 license](LICENSE) as the project.
