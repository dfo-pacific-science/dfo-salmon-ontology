#!/usr/bin/env python3
"""Post-process WIDOCO HTML output for project-specific UX defaults.

- Rename ontology display title to "DFO Salmon Ontology"
- Remove "Ontology Specification Draft" badge wording
- Expand selected collapsibles by default
"""

from __future__ import annotations

import re
from pathlib import Path


def patch_html(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    original = content

    # Title/name text normalization
    content = content.replace("GC DFO Salmon Ontology", "DFO Salmon Ontology")
    content = content.replace("Ontology Specification Draft", "Ontology Specification")

    # Expand overview sections by default (index.html structure)
    content = re.sub(
        r'(<details class="gcdfo-collapsible gcdfo-overview-collapsible")>',
        r'\1 open>',
        content,
    )

    # Expand WebVOWL box by default
    content = re.sub(
        r'(<details class="gcdfo-collapsible gcdfo-webvowl")>',
        r'\1 open>',
        content,
    )

    # Expand concept-scheme list details (the "19 schemes" block)
    content = re.sub(
        r'(<h3 id="skos-schemes" class="list">Concept schemes</h3>\s*<details class="gcdfo-collapsible")>',
        r'<h3 id="skos-schemes" class="list">Concept schemes</h3>\n<details class="gcdfo-collapsible" open>',
        content,
        flags=re.S,
    )

    # Ensure custom enhancement JS is loaded.
    if "resources/gcdfo-enhancements.js" not in content:
        content = content.replace(
            "</head>",
            '<script src="resources/gcdfo-enhancements.js" defer></script>\n</head>',
        )

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"Patched {path}")
    else:
        print(f"No changes for {path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for rel in ["docs/index.html", "docs/index-en.html"]:
        p = root / rel
        if p.exists():
            patch_html(p)


if __name__ == "__main__":
    main()
