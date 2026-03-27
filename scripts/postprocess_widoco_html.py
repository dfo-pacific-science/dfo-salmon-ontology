#!/usr/bin/env python3
"""Post-process WIDOCO HTML output for project-specific UX defaults.

- Rename ontology display title to "DFO Salmon Ontology"
- Remove "Ontology Specification Draft" badge wording
- Expand selected collapsibles by default
"""

from __future__ import annotations

import re
from pathlib import Path


INTRO_MARKER_START = "<!-- BEGIN gcdfo start-here -->"
INTRO_MARKER_END = "<!-- END gcdfo start-here -->"
INTRO_HTML = f"""
{INTRO_MARKER_START}
<section class=\"gcdfo-start-here\" id=\"start-here\" aria-labelledby=\"start-here-title\">
  <div class=\"gcdfo-start-here-hero\">
    <p class=\"gcdfo-eyebrow\">Start here</p>
    <h2 id=\"start-here-title\">A reviewer-friendly overview for scientists and biologists</h2>
    <p>This ontology is a shared vocabulary and relationship map for DFO Pacific salmon data. Its job is to make terms like Conservation Unit, survey event, spawner abundance, reference point, and status zone mean the same thing across datasets, methods, assessments, and reporting products.</p>
  </div>
  <div class=\"gcdfo-start-here-grid\">
    <section class=\"gcdfo-intro-card\" aria-labelledby=\"gcdfo-what-is\">
      <h3 id=\"gcdfo-what-is\">What this is</h3>
      <ul>
        <li>An operational ontology for Pacific salmon science, assessment, and data stewardship at DFO.</li>
        <li>A way to connect field observations -&gt; measurements/results -&gt; assessments -&gt; reference points and status concepts.</li>
        <li>A place to standardize controlled vocabularies such as status zones, benchmark types, and method schemes.</li>
      </ul>
    </section>
    <section class=\"gcdfo-intro-card\" aria-labelledby=\"gcdfo-what-is-not\">
      <h3 id=\"gcdfo-what-is-not\">What this is not</h3>
      <ul>
        <li>Not a complete ontology of salmon biology or ecology.</li>
        <li>Not a replacement for scientific judgment or program-specific methods.</li>
        <li>Not raw data; it is the schema and vocabulary that help raw data line up.</li>
      </ul>
    </section>
    <section class=\"gcdfo-intro-card\" id=\"gcdfo-review-paths\" aria-labelledby=\"gcdfo-review-paths-title\">
      <h3 id=\"gcdfo-review-paths-title\">Suggested review path</h3>
      <ol>
        <li><strong>Units:</strong> <a href=\"#ConservationUnit\">Conservation Unit</a>, <a href=\"#https://w3id.org/smn/Population\">Population</a>, <a href=\"#StockManagementUnit\">Stock Management Unit</a>, <a href=\"#https://w3id.org/smn/Stock\">Stock</a>.</li>
        <li><strong>Assessment flow:</strong> <a href=\"#https://w3id.org/smn/SurveyEvent\">Survey event</a> -&gt; <a href=\"#SpawnerAbundance\">Spawner abundance</a> / results -&gt; <a href=\"#https://w3id.org/smn/StockAssessment\">Stock assessment</a> -&gt; <a href=\"#WSPBiologicalStatusZoneScheme\">WSP status zone</a> and reference points.</li>
        <li><strong>Controlled vocabularies:</strong> go to the <a href=\"#skos\">SKOS</a> section for code-list style terms and approved value schemes.</li>
      </ol>
    </section>
    <section class=\"gcdfo-intro-card\" aria-labelledby=\"gcdfo-use-page\">
      <h3 id=\"gcdfo-use-page\">How to use this page</h3>
      <ul>
        <li>Use <strong>Search terms</strong> at the top right, or press <kbd>/</kbd>.</li>
        <li>Use the quick-jump chips for major sections.</li>
        <li>Browse <strong>Classes</strong> for entities and processes, and <strong>Object properties</strong> for relationships.</li>
        <li>Open <strong>WebVOWL</strong> for a high-level structure view, then use the detailed term pages when checking definitions and links.</li>
      </ul>
    </section>
  </div>
  <p class=\"gcdfo-start-here-note\"><strong>Bigger picture:</strong> an authoritative set of definitions becomes much more useful when those terms travel into data dictionaries and databases via their persistent identifiers. That gives you a semantic contract between what your columns mean and how other people or downstream tools will reinterpret and reuse the data later, which makes integration across field programs, assessments, dashboards, and reporting products far less brittle.</p>
</section>
{INTRO_MARKER_END}
""".strip()


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


def _upsert_intro_panel(content: str) -> str:
    if INTRO_MARKER_START in content and INTRO_MARKER_END in content:
        pattern = re.compile(
            rf"{re.escape(INTRO_MARKER_START)}.*?{re.escape(INTRO_MARKER_END)}",
            flags=re.S,
        )
        return pattern.sub(INTRO_HTML, content, count=1)

    if '<div class="status">' in content:
        return content.replace('<div class="status">', INTRO_HTML + '\n<div class="status">', 1)

    return content


OVERVIEW_OLD = """<span class=\"markdown\">\nThis ontology has the following classes and properties.</span>"""
OVERVIEW_NEW = """<span class=\"markdown\">\nThis section lists the formal classes, properties, and controlled vocabularies that implement the overview above. If you are reviewing from a science or biology perspective, start with the <a href=\"#start-here\">Start here</a> panel first.</span>"""


def patch_html(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    original = content

    # Title/name text normalization
    content = content.replace("GC DFO Salmon Ontology", "DFO Salmon Ontology")
    content = content.replace("Ontology Specification Draft", "Ontology Specification")

    # Add reviewer-friendly intro near the top of the page.
    content = _upsert_intro_panel(content)
    content = content.replace(OVERVIEW_OLD, OVERVIEW_NEW)

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
