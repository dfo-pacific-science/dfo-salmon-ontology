#!/usr/bin/env python3
"""
Generate the SKOS concept-section HTML for the Widoco landing page.

Reads `ontology/dfo-salmon.ttl`, extracts every SKOS concept scheme / concept,
and rewrites the block between the SKOS section comment and the CROSSREF comment
inside `docs/index.html`.
"""

from __future__ import annotations

import html
import pathlib
import re
from collections import defaultdict
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = ROOT / "ontology" / "dfo-salmon.ttl"
INDEX_PATH = ROOT / "docs" / "index.html"

LABEL_RE = re.compile(r"(?:skos:prefLabel|skos:label|rdfs:label)\s+\"([^\"]+)\"@en")
IN_SCHEME_RE = re.compile(r"skos:inScheme\s+([^;]+);")
HAS_TOP_RE = re.compile(r"skos:hasTopConcept\s+([^;]+);")
DEF_RE = re.compile(r"skos:definition\s+\"([^\"]+)\"@en")


def clean_list(source: str) -> List[str]:
    source = source.replace(",", " ")
    return [token.strip() for token in source.split() if token.strip()]


def to_iri(symbol: str) -> str:
    if ":" not in symbol:
        return f"https://w3id.org/gcdfo/salmon#{symbol}"
    prefix, local = symbol.split(":", 1)
    if prefix in ("", "gcdfo"):
        return f"https://w3id.org/gcdfo/salmon#{local}"
    return symbol


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "scheme"


def parse_ttl() -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, List[str]]]]:
    text = ONTOLOGY_PATH.read_text(encoding="utf-8")
    blocks = [blk for blk in text.split("\n\n") if blk.strip()]
    schemes: Dict[str, Dict[str, str]] = {}
    concepts: Dict[str, Dict[str, List[str]]] = {}
    labels: Dict[str, str] = {}

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        subject = lines[0].split()[0]
        label_match = LABEL_RE.search(block)
        if label_match:
            labels[subject] = label_match.group(1)
        if "skos:ConceptScheme" in block:
            desc_match = DEF_RE.search(block)
            desc = desc_match.group(1) if desc_match else ""
            top_concepts: List[str] = []
            for match in HAS_TOP_RE.findall(block):
                top_concepts.extend(clean_list(match))
            schemes[subject] = {
                "label": labels.get(subject, subject),
                "description": desc,
                "top": top_concepts,
            }
        if "skos:Concept" in block:
            in_scheme: List[str] = []
            for match in IN_SCHEME_RE.findall(block):
                in_scheme.extend(clean_list(match))
            concepts[subject] = {
                "label": labels.get(subject, subject),
                "schemes": in_scheme,
            }

    return schemes, concepts


def build_section(
    schemes: Dict[str, Dict[str, str]],
    concepts: Dict[str, Dict[str, List[str]]],
) -> str:
    scheme_concepts = defaultdict(dict)
    for subject, data in concepts.items():
        for scheme in data["schemes"]:
            scheme_concepts[scheme][subject] = data["label"]
    for scheme_id, info in schemes.items():
        for top in info["top"]:
            if top and top not in scheme_concepts[scheme_id]:
                scheme_concepts[scheme_id][top] = concepts.get(top, {}).get("label", top)

    ordered = sorted(
        ((sid, info) for sid, info in schemes.items()),
        key=lambda item: item[1]["label"].lower(),
    )

    lines: List[str] = [
        "<!--SKOS CONCEPT SCHEMES-->",
        "  <div id=\"concept-schemes\">",
        "<h2 id=\"skos\" class=\"list\">Concept schemes & SKOS concepts</h2>",
        "<p class=\"markdown\">Every SKOS concept scheme defined in the ontology is listed below with the current concepts assigned to it.</p>",
        "<ul class=\"hlist\">",
    ]
    nav_items = []
    for scheme_id, info in ordered:
        anchor = "scheme-" + slugify(info["label"])
        nav_items.append(f'  <li><a href="#{anchor}">{html.escape(info["label"])}</a></li>')
    lines.extend(nav_items)
    lines.append("</ul>")

    for scheme_id, info in ordered:
        anchor = "scheme-" + slugify(info["label"])
        lines.append(f'<div class="scheme" id="{anchor}">')
        lines.append(f'  <h3 class="list">{html.escape(info["label"])}</h3>')
        if info["description"]:
            lines.append(f'  <p class="markdown">{html.escape(info["description"])}</p>')
        entries = scheme_concepts.get(scheme_id, {})
        if entries:
            lines.append("  <ul>")
            for subj, lbl in sorted(entries.items(), key=lambda item: item[1].lower()):
                href = html.escape(to_iri(subj))
                lines.append(f'    <li><a href="{href}">{html.escape(lbl)}</a></li>')
            lines.append("  </ul>")
        else:
            lines.append("  <p class=\"markdown\"><em>Currently no SKOS concepts are declared under this scheme.</em></p>")
        lines.append("</div>")

    lines.append("  </div>")
    lines.append("<hr>")
    return "\n".join(lines)


def replace_section(section: str) -> None:
    content = INDEX_PATH.read_text(encoding="utf-8")
    start = content.find("<!--SKOS CONCEPT SCHEMES-->")
    end = content.find("<!--CROSSREF SECTION-->")
    if start == -1 or end == -1:
        raise RuntimeError("Could not find SKOS section markers in index.html")
    new_content = content[:start] + section + "\n" + content[end:]
    INDEX_PATH.write_text(new_content, encoding="utf-8")


def main() -> None:
    schemes, concepts = parse_ttl()
    section = build_section(schemes, concepts)
    replace_section(section)
    print("✅ Updated docs/index.html SKOS section with every scheme/concept.")


if __name__ == "__main__":
    main()
