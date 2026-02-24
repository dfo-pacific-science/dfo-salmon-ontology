#!/usr/bin/env python3
"""Post-process WIDOCO HTML output for project-specific UX defaults.

- Rename ontology display title to "DFO Salmon Ontology"
- Remove "Ontology Specification Draft" badge wording
- Expand selected collapsibles by default
"""

from __future__ import annotations

import re
from pathlib import Path


def _canonicalize_change_lists(content: str) -> str:
    """Sort Added/Deleted changelog <ul> blocks to make docs generation idempotent.

    WIDOCO changelog item order can be unstable across runs. This normalizes any
    <ul> block where every <li> starts with "Added:" or "Deleted:".
    """

    ul_pattern = re.compile(r"<ul>\s*(?:<li>.*?</li>\s*)+</ul>", flags=re.S)

    def _normalize_ul(match: re.Match[str]) -> str:
        block = match.group(0)
        items = re.findall(r"<li>.*?</li>", block, flags=re.S)
        if not items:
            return block

        normalized = [re.sub(r"\s+", " ", item).strip() for item in items]
        if not all(
            item.startswith("<li>Added:") or item.startswith("<li>Deleted:")
            for item in normalized
        ):
            return block

        # Keep deterministic lexical order based on normalized item content.
        ordered = [raw for _, raw in sorted(zip(normalized, items), key=lambda t: t[0])]

        indent_match = re.search(r"\n(\s*)<li>", block)
        indent = indent_match.group(1) if indent_match else ""
        return "<ul>\n" + "\n".join(f"{indent}{item.strip()}" for item in ordered) + "\n</ul>"

    return ul_pattern.sub(_normalize_ul, content)


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

    # Stabilize WIDOCO changelog list ordering across regenerations.
    content = _canonicalize_change_lists(content)

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
