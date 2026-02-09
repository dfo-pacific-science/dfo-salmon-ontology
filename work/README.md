# work/ (SPSR integration snapshot)

This directory contains working/intermediate artifacts used during ontology integration.

## Important boundary

- **Canonical SPSR assessment + mapping source**: `Br-Johnson/smn-data-gpt/assessments/spsr`
- **This folder (`work/`)**: local integration snapshot/cache for ontology-side authoring and review.

If values differ between `work/` and canonical SPSR artifacts, resolve in `smn-data-gpt/assessments/spsr` first, then refresh here as needed.

## Current integration anchor

SPSR term integration is currently tracked through:
- `dfo-pacific-science/dfo-salmon-ontology` PR #31
