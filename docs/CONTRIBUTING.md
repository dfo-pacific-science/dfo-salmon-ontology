# Contributing to DFO Salmon Ontology

Thank you for your interest in contributing to the DFO Salmon Ontology! This document provides guidelines for contributing to the project.

## Getting Started

1. **Read the documentation**:
   - [README.md](../README.md) - Project overview
   - [COMPETENCY_QUESTIONS.md](COMPETENCY_QUESTIONS.md) - Project scope and goals
   - [CONVENTIONS.md](CONVENTIONS.md) - Modeling conventions and guidelines
   - [AGENTS.md](../AGENTS.md) - Detailed development guidelines

2. **Set up your development environment**:
   - Install Java 11+ for ROBOT
   - Install Python 3.11+ for validation scripts
   - See [ROBOT_SETUP.md](ROBOT_SETUP.md) for detailed setup instructions

## Contribution Workflow

### 1. Open an Issue
Before making changes, open a GitHub issue to discuss:
- The competency question your change addresses
- Proposed terms, definitions, and relationships
- External alignments or dependencies

Use the [ontology change template](../.github/ISSUE_TEMPLATE/ontology-change.md) for structured discussions.

### 2. Make Changes
- Create a feature branch from `main`
- Follow the [modeling conventions](CONVENTIONS.md)
- Add labels, definitions, and source attributions
- Ensure no instance data is added to the main ontology file

### 3. Quality Control
Before submitting a PR, run these checks:
```bash
# ROBOT validation
java -jar tools/robot.jar validate --input ontology/dfo-salmon.ttl

# ROBOT reasoning
java -jar tools/robot.jar reason --input ontology/dfo-salmon.ttl --reasoner ELK

# SHACL validation
python scripts/test_shacl_validation.py

# SPARQL tests (when implemented)
python scripts/test_sparql_queries.py
```

### 4. Submit Pull Request
- Use the [PR template](../.github/PULL_REQUEST_TEMPLATE.md)
- Ensure all checklist items are completed
- Request review from domain experts and ontology modelers

## Development Guidelines

### Ontology Modeling
- **One clear parent**: Avoid premature deep hierarchies
- **Competency-driven**: Every term should help answer a competency question
- **External alignment**: Use existing vocabularies (DwC, ENVO, QUDT) when possible
- **Documentation**: Include clear definitions and source attributions

### File Organization
- **Schema only**: Keep instance data in `ontology/examples/` for testing only
- **Modular shapes**: Use `ontology/shapes/` for SHACL validation rules
- **Templates**: Use `ontology/templates/` for ROBOT term generation
- **Tests**: Add SPARQL tests in `ontology/sparql/` for new competency questions

### Naming Conventions
- **Classes**: PascalCase (e.g., `EscapementSurveyEvent`)
- **Properties**: lowerCamelCase (e.g., `sampledDuring`)
- **Instances**: PascalCase with descriptive names (e.g., `SkeenaSockeye`)

## Review Process

All contributions require review from:
1. **Domain expert**: Validates scientific accuracy and completeness
2. **Ontology modeler**: Ensures proper modeling patterns and conventions

Review criteria:
- [ ] Scientific accuracy and completeness
- [ ] Proper modeling patterns and conventions
- [ ] Clear definitions and documentation
- [ ] External alignments are valid
- [ ] No breaking changes without proper deprecation
- [ ] Tests pass and coverage is maintained

## Release Process

Releases are managed through GitHub:
1. Version bump in ontology metadata
2. Automated CI/CD validation
3. Artifact generation (TTL, OWL, JSON)
4. GitHub release with changelog

## Getting Help

- **Issues**: Use GitHub issues for questions and discussions
- **Documentation**: Check existing docs in the `docs/` directory
- **Community**: Engage with the DFO data stewardship community

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and constructive in all interactions.

## License

By contributing, you agree that your contributions will be licensed under the same [CC-BY 4.0 license](../LICENSE) as the project.
