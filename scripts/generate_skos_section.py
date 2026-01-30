#!/usr/bin/env python3
"""
Generate the SKOS concept-section HTML for the Widoco landing page.

Reads `ontology/dfo-salmon.ttl`, extracts every SKOS concept scheme / concept,
and rewrites the block between the SKOS section comment and the CROSSREF comment
inside `docs/index.html`.

Also post-processes `docs/index.html` to ensure the OWL cross-reference section
renders before the SKOS sections (OWL Classes first) by injecting a small,
idempotent JavaScript snippet. This is necessary because Widoco regeneration
may overwrite manual edits to `docs/index.html`.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = ROOT / "ontology" / "dfo-salmon.ttl"
INDEX_PATH = ROOT / "docs" / "index.html"

LABEL_RE = re.compile(r"(?:skos:prefLabel|skos:label|rdfs:label)\s+\"([^\"]+)\"@en")
IN_SCHEME_RE = re.compile(r"skos:inScheme\s+([^;]+);")
HAS_TOP_RE = re.compile(r"skos:hasTopConcept\s+([^;]+);")
DEF_RE = re.compile(r"skos:definition\s+\"([^\"]+)\"@en")

REORDER_MARKER_BEGIN = "// BEGIN gcdfo custom: reorder sections (OWL before SKOS)"
REORDER_MARKER_END = "// END gcdfo custom: reorder sections (OWL before SKOS)"
UI_MARKER_BEGIN = "// BEGIN gcdfo custom: ui enhancements (TOC + IRI copy + search + permalinks)"
UI_MARKER_END = "// END gcdfo custom: ui enhancements (TOC + IRI copy + search + permalinks)"
OLD_UI_MARKER_BEGIN = "// BEGIN gcdfo custom: ui enhancements (TOC + IRI copy)"
OLD_UI_MARKER_END = "// END gcdfo custom: ui enhancements (TOC + IRI copy)"
HEAD_MARKER_BEGIN = "<!-- BEGIN gcdfo custom: head assets -->"
HEAD_MARKER_END = "<!-- END gcdfo custom: head assets -->"

CREATED_RE = re.compile(r'dcterms:created\s+"([^"]+)"\^\^xsd:date\s*;')
MODIFIED_RE = re.compile(r'dcterms:modified\s+"([^"]+)"\^\^xsd:date\s*;')
VERSION_INFO_RE = re.compile(r'owl:versionInfo\s+"([^"]+)"\s*;')
VERSION_IRI_RE = re.compile(r"owl:versionIRI\s+<([^>]+)>\s*;")
CODE_REPO_RE = re.compile(r"schema:codeRepository\s+<([^>]+)>\s*;")

DOCS_LATEST_URL = "https://w3id.org/gcdfo/salmon"


@dataclass(frozen=True)
class OntologyMetadata:
    created: str
    modified: str
    version_info: str
    version_iri: str
    code_repository: str


def extract_ontology_metadata() -> OntologyMetadata:
    text = ONTOLOGY_PATH.read_text(encoding="utf-8")
    created_match = CREATED_RE.search(text)
    modified_match = MODIFIED_RE.search(text)
    version_match = VERSION_INFO_RE.search(text)
    version_iri_match = VERSION_IRI_RE.search(text)
    code_repo_match = CODE_REPO_RE.search(text)
    if not (created_match and modified_match and version_match and version_iri_match and code_repo_match):
        raise RuntimeError(
            "Could not extract required metadata (dates/version/code repository) from ontology header"
        )
    return OntologyMetadata(
        created=created_match.group(1),
        modified=modified_match.group(1),
        version_info=version_match.group(1),
        version_iri=version_iri_match.group(1),
        code_repository=code_repo_match.group(1),
    )


def update_index_metadata(metadata: OntologyMetadata) -> None:
    """
    Keep human-facing docs metadata aligned with the ontology header.

    This avoids drift between `ontology/dfo-salmon.ttl` and `docs/index.html`.
    """
    content = INDEX_PATH.read_text(encoding="utf-8")

    # Release / modified dates.
    content, release_subs = re.subn(
        r"(<h2>Release:\s*)(\d{4}-\d{2}-\d{2})(</h2>)",
        rf"\g<1>{metadata.modified}\g<3>",
        content,
        count=1,
    )
    content, modified_subs = re.subn(
        r"(<dt>Modified on:\s*)(\d{4}-\d{2}-\d{2})(</dt>)",
        rf"\g<1>{metadata.modified}\g<3>",
        content,
        count=1,
    )
    if release_subs == 0 or modified_subs == 0:
        raise RuntimeError("Could not update Release/Modified dates in docs/index.html")

    # Revision line.
    content, revision_subs = re.subn(
        r"(<dt>Revision:</dt>\s*<dd>)([^<]*)(</dd>)",
        rf"\g<1>{html.escape(metadata.version_info)}\g<3>",
        content,
        count=1,
    )
    if revision_subs == 0:
        raise RuntimeError("Could not update Revision in docs/index.html")

    # This version link: keep it aligned with owl:versionIRI.
    content, this_version_subs = re.subn(
        r"(<dt>This version:</dt>\s*<dd><a href=\")([^\"]+)(\">)([^<]*)(</a></dd>)",
        rf"\g<1>{html.escape(metadata.version_iri)}\g<3>{html.escape(metadata.version_iri)}\g<5>",
        content,
        count=1,
    )
    if this_version_subs == 0:
        raise RuntimeError("Could not update This version link in docs/index.html")

    # Latest version link: point at the stable w3id IRI (insert if missing).
    content, latest_version_subs = re.subn(
        r"(<dt>Latest version:</dt>\s*<dd><a href=\")([^\"]+)(\">)([^<]*)(</a></dd>)",
        rf"\g<1>{DOCS_LATEST_URL}\g<3>{DOCS_LATEST_URL}\g<5>",
        content,
        count=1,
    )
    if latest_version_subs == 0:
        content, insert_subs = re.subn(
            r"(<dt>This version:</dt>\s*<dd><a href=\"[^\"]+\">[^<]*</a></dd>)",
            rf"\g<1>\n<dt>Latest version:</dt>\n<dd><a href=\"{DOCS_LATEST_URL}\">{DOCS_LATEST_URL}</a></dd>",
            content,
            count=1,
        )
        if insert_subs == 0:
            raise RuntimeError("Could not insert Latest version link in docs/index.html")

    # Bibliographic citation / cite as: keep it short and point at the stable w3id IRI.
    citation = (
        "Fishery & Assessment Data Section (FADS) Data Stewardship Unit. "
        f"GC DFO Salmon Ontology. Revision: {metadata.version_info}. "
        f"Retrieved from: {DOCS_LATEST_URL}"
    )
    content, citation_subs = re.subn(
        r"(<dt>Bibliographic citation:</dt>\s*<dd>)(.*?)(</dd>)",
        rf"\g<1>{html.escape(citation)}\g<3>",
        content,
        count=1,
        flags=re.DOTALL,
    )
    if citation_subs == 0:
        content, citation_subs = re.subn(
            r"(<dt>Cite as:</dt>\s*<dd>)(.*?)(</dd>)",
            rf"\g<1>{html.escape(citation)}\g<3>",
            content,
            count=1,
            flags=re.DOTALL,
        )
    if citation_subs == 0:
        raise RuntimeError("Could not update bibliographic citation in docs/index.html")

    # Normalize download links to the published artifact names.
    content = content.replace("ontology.jsonld", "gcdfo.jsonld")
    content = content.replace("ontology.owl", "gcdfo.owl")
    content = content.replace("ontology.ttl", "gcdfo.ttl")
    content = re.sub(r"\s*<span><a href=\"ontology\.nt\".*?</span>", "", content)

    # Repository link.
    content, repo_subs = re.subn(
        r"(<dt>Vocabulary maintained at:</dt>\s*<dd><a href=\")([^\"]+)(\">)([^<]*)(</a></dd>)",
        rf"\g<1>{html.escape(metadata.code_repository)}\g<3>{html.escape(metadata.code_repository)}\g<5>",
        content,
        count=1,
    )
    if repo_subs == 0:
        raise RuntimeError("Could not update Vocabulary maintained at in docs/index.html")

    # SCHEMA.ORG METADATA JSON: update key fields.
    schema_re = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.DOTALL)
    match = schema_re.search(content)
    if not match:
        raise RuntimeError("Could not find schema.org JSON-LD block in docs/index.html")

    raw_json = match.group(2).strip()
    data = json.loads(raw_json)
    data["url"] = DOCS_LATEST_URL
    data["dateReleased"] = metadata.created
    data["dateModified"] = metadata.modified
    data["version"] = metadata.version_info
    data["codeRepository"] = metadata.code_repository

    updated_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    content = content[: match.start(2)] + updated_json + content[match.end(2) :]

    INDEX_PATH.write_text(content, encoding="utf-8")


def clean_list(source: str) -> List[str]:
    source = source.replace(",", " ")
    return [token.strip() for token in source.split() if token.strip()]


def to_local_anchor(symbol: str) -> str:
    """Convert a symbol to a local anchor (e.g., ':Foo' or 'gcdfo:Foo' -> '#Foo')."""
    if ":" not in symbol:
        return f"#{symbol}"
    prefix, local = symbol.split(":", 1)
    if prefix in ("", "gcdfo"):
        return f"#{local}"
    # External prefix - fall back to full IRI (won't have local anchor)
    return symbol


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "scheme"


def to_iri(symbol: str) -> str:
    """Convert a symbol to a full IRI."""
    if ":" not in symbol:
        return f"https://w3id.org/gcdfo/salmon#{symbol}"
    prefix, local = symbol.split(":", 1)
    if prefix in ("", "gcdfo"):
        return f"https://w3id.org/gcdfo/salmon#{local}"
    return symbol


def to_local_name(symbol: str) -> str:
    """Extract the local name from a symbol (e.g., ':Foo' -> 'Foo')."""
    if ":" not in symbol:
        return symbol
    _, local = symbol.split(":", 1)
    return local


def normalize_symbol(symbol: str) -> str:
    """Normalize a symbol to a canonical form (e.g., 'gcdfo:Foo' and ':Foo' both become ':Foo')."""
    if ":" not in symbol:
        return f":{symbol}"
    prefix, local = symbol.split(":", 1)
    if prefix in ("", "gcdfo"):
        return f":{local}"
    return symbol


def parse_ttl() -> Tuple[Dict[str, Dict[str, str]], Dict[str, Dict[str, str]]]:
    text = ONTOLOGY_PATH.read_text(encoding="utf-8")
    blocks = [blk for blk in text.split("\n\n") if blk.strip()]
    schemes: Dict[str, Dict[str, str]] = {}
    concepts: Dict[str, Dict[str, str]] = {}
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
            # Normalize the scheme key for consistent lookups
            normalized_subject = normalize_symbol(subject)
            schemes[normalized_subject] = {
                "label": labels.get(subject, subject),
                "description": desc,
                "top": top_concepts,
            }
        if "skos:Concept" in block:
            in_scheme: List[str] = []
            for match in IN_SCHEME_RE.findall(block):
                # Normalize scheme references to match scheme keys
                in_scheme.extend(normalize_symbol(s) for s in clean_list(match))
            desc_match = DEF_RE.search(block)
            desc = desc_match.group(1) if desc_match else ""
            concepts[subject] = {
                "label": labels.get(subject, subject),
                "schemes": in_scheme,
                "definition": desc,
            }

    return schemes, concepts


def build_section(
    schemes: Dict[str, Dict[str, str]],
    concepts: Dict[str, Dict[str, str]],
) -> str:
    scheme_concepts = defaultdict(dict)
    for subject, data in concepts.items():
        for scheme in data["schemes"]:
            scheme_concepts[scheme][subject] = data["label"]
    for scheme_id, info in schemes.items():
        for top in info["top"]:
            if top and top not in scheme_concepts[scheme_id]:
                scheme_concepts[scheme_id][top] = concepts.get(top, {}).get("label", top)

    ordered_schemes = sorted(
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
    for scheme_id, info in ordered_schemes:
        anchor = "scheme-" + slugify(info["label"])
        nav_items.append(f'  <li><a href="#{anchor}">{html.escape(info["label"])}</a></li>')
    lines.extend(nav_items)
    lines.append("</ul>")

    for scheme_id, info in ordered_schemes:
        anchor = "scheme-" + slugify(info["label"])
        lines.append(f'<div class="scheme" id="{anchor}">')
        lines.append(f'  <h3 id="{anchor}" class="list">{html.escape(info["label"])}</h3>')
        if info["description"]:
            lines.append(f'  <p class="markdown">{html.escape(info["description"])}</p>')
        entries = scheme_concepts.get(scheme_id, {})
        if entries:
            lines.append("  <ul>")
            for subj, lbl in sorted(entries.items(), key=lambda item: item[1].lower()):
                href = html.escape(to_local_anchor(subj))
                lines.append(f'    <li><a href="{href}">{html.escape(lbl)}</a></li>')
            lines.append("  </ul>")
        else:
            lines.append("  <p class=\"markdown\"><em>Currently no SKOS concepts are declared under this scheme.</em></p>")
        lines.append("</div>")

    lines.append("  </div>")
    lines.append("<hr>")

    # Generate entity divs for all SKOS concepts
    lines.append('<div id="skos-concepts">')
    lines.append('<h2 id="skos-concepts-header" class="list">SKOS Concepts</h2>')
    lines.append("<p>This section provides details for each SKOS concept defined in the ontology.</p>")

    # Build a nav list of all concepts
    ordered_concepts = sorted(concepts.items(), key=lambda item: item[1]["label"].lower())
    lines.append('<ul class="hlist">')
    for subj, data in ordered_concepts:
        local_name = to_local_name(subj)
        lines.append(f'  <li><a href="#{html.escape(local_name)}" title="{html.escape(to_iri(subj))}">{html.escape(data["label"])}</a></li>')
    lines.append("</ul>")

    # Generate entity divs for each concept
    for subj, data in ordered_concepts:
        local_name = to_local_name(subj)
        iri = to_iri(subj)
        label = data["label"]
        definition = data.get("definition", "")
        concept_schemes = data.get("schemes", [])

        lines.append(f'<div class="entity" id="{html.escape(local_name)}">')
        lines.append(f'  <h3>{html.escape(label)}<sup class="type-skos" title="SKOS concept">skos</sup></h3>')
        lines.append(f'  <p><strong>IRI:</strong> {html.escape(iri)}</p>')

        if definition:
            lines.append('  <div class="comment">')
            lines.append(f'    <span class="markdown">{html.escape(definition)}</span>')
            lines.append("  </div>")

        lines.append('  <dl class="definedBy">')
        lines.append("    <dt>Is defined by</dt>")
        lines.append('    <dd><a href="https://w3id.org/gcdfo/salmon">https://w3id.org/gcdfo/salmon</a></dd>')
        lines.append("  </dl>")

        if concept_schemes:
            lines.append('  <dl class="description">')
            lines.append("    <dt>In scheme</dt>")
            for scheme_sym in concept_schemes:
                scheme_info = schemes.get(scheme_sym, {})
                if scheme_info:
                    scheme_label = scheme_info.get("label", scheme_sym)
                else:
                    # Fallback: use the local name as the label
                    scheme_label = to_local_name(scheme_sym)
                scheme_anchor = "scheme-" + slugify(scheme_label)
                lines.append(f'    <dd><a href="#{scheme_anchor}">{html.escape(scheme_label)}</a></dd>')
            lines.append("  </dl>")

        lines.append("</div>")

    lines.append("</div>")
    lines.append("<hr>")

    return "\n".join(lines)


def replace_section(section: str) -> None:
    content = INDEX_PATH.read_text(encoding="utf-8")
    start = content.find("<!--SKOS CONCEPT SCHEMES-->")
    end = content.find("<!--CROSSREF SECTION-->")
    if end == -1:
        raise RuntimeError("Could not find CROSSREF section marker in index.html")
    if start == -1:
        # First insertion: add the SKOS section immediately before the crossref block.
        new_content = content[:end] + section + "\n" + content[end:]
    else:
        new_content = content[:start] + section + "\n" + content[end:]
    INDEX_PATH.write_text(new_content, encoding="utf-8")


def ensure_owl_before_skos_ordering() -> None:
    """
    Ensure the OWL class cross-reference section appears before SKOS sections.

    Widoco generates a stable DOM with:
    - <div id="introduction"> (front matter)
    - <div id="crossref"> ... (class crossref)
    - <div id="concept-schemes"> ... (SKOS schemes + concepts)

    We keep the file generated by Widoco and enforce display order at runtime
    by injecting a tiny script that moves #crossref directly after #introduction
    before the TOC is built.
    """
    content = INDEX_PATH.read_text(encoding="utf-8")

    # If marker-wrapped snippet exists, we only need to ensure loadHash() calls reorderSections().
    has_snippet = REORDER_MARKER_BEGIN in content and REORDER_MARKER_END in content
    marker_idx = content.find(REORDER_MARKER_BEGIN) if has_snippet else -1

    # Cleanup: remove any legacy/unmarked reorderSections() definition to avoid duplicate live paths.
    # (Earlier manual edits inserted a reorderSections() between loadHash() and loadTOC().)
    if has_snippet and marker_idx != -1:
        legacy_start = content.find("function reorderSections()", 0, marker_idx)
        if legacy_start != -1:
            content = content[:legacy_start] + content[marker_idx:]

    # Locate loadHash() and the start of loadTOC() to keep changes localized.
    loadhash_start = content.find("function loadHash()")
    if loadhash_start == -1:
        raise RuntimeError("Could not find function loadHash() in docs/index.html")

    loadtoc_start = content.find("function loadTOC", loadhash_start)
    if loadtoc_start == -1:
        raise RuntimeError("Could not find function loadTOC in docs/index.html")

    pre = content[:loadhash_start]
    mid = content[loadhash_start:loadtoc_start]
    post = content[loadtoc_start:]

    # Ensure reorderSections() is called within loadHash().
    if "reorderSections();" not in mid:
        marker = 'jQuery(".markdown").each'
        pos = mid.find(marker)
        if pos == -1:
            # Fall back to injecting right after function signature line.
            brace = mid.find("{")
            if brace == -1:
                raise RuntimeError("Could not parse loadHash() body in docs/index.html")
            inject_at = mid.find("\n", brace)
            if inject_at == -1:
                raise RuntimeError("Could not locate insertion point in loadHash()")
            inject_at += 1
        else:
            inject_at = mid.find("\n", pos)
            if inject_at == -1:
                raise RuntimeError("Could not locate end of markdown parsing line in loadHash()")
            inject_at += 1
        mid = mid[:inject_at] + "  reorderSections();\n" + mid[inject_at:]

    if not has_snippet:
        snippet = "\n".join(
            [
                f"{REORDER_MARKER_BEGIN}",
                "function reorderSections() {",
                "  // Keep OWL classes ahead of SKOS sections in the rendered page + TOC.",
                "  var $crossref = $(\"#crossref\");",
                "  var $intro = $(\"#introduction\");",
                "  if ($crossref.length && $intro.length) {",
                "    $crossref.insertAfter($intro);",
                "    // Ensure visual separation after moving the block.",
                "    if (!$crossref.prev().is(\"hr\")) {",
                "      $crossref.before(\"<hr>\");",
                "    }",
                "    if (!$crossref.next().is(\"hr\")) {",
                "      $crossref.after(\"<hr>\");",
                "    }",
                "  }",
                "}",
                f"{REORDER_MARKER_END}",
                "",
            ]
        )
        content = pre + mid + snippet + post
    else:
        content = pre + mid + post

    INDEX_PATH.write_text(content, encoding="utf-8")


def ensure_custom_ui_enhancements() -> None:
    """
    Re-apply repo-specific UI/UX enhancements after WIDOCO regeneration.
    """
    content = INDEX_PATH.read_text(encoding="utf-8")

    # Ensure <html lang="en">
    content = re.sub(r"<html(?![^>]*\blang=)", "<html lang=\"en\"", content, count=1)

    # Ensure custom head assets are included.
    if "resources/gcdfo-custom.css" not in content:
        head_block = "\n".join(
            [
                HEAD_MARKER_BEGIN,
                '<link rel="stylesheet" href="resources/gcdfo-custom.css" media="screen"/>',
                '<link rel="stylesheet" href="resources/slider.css" media="screen"/>',
                '<meta name="color-scheme" content="dark light">',
                '<script type="module" src="resources/dark-mode-toggle.mjs"></script>',
                HEAD_MARKER_END,
                "",
            ]
        )
        content = content.replace("</head>", f"{head_block}</head>", 1)

    # Ensure skip link exists right after <body>.
    if "gcdfo-skip-link" not in content:
        content = re.sub(
            r"<body([^>]*)>",
            r"<body\1>\n  <a class=\"visually-hidden-focusable gcdfo-skip-link\" href=\"#maincontent\">Skip to content</a>",
            content,
            count=1,
        )

    # Ensure TOC nav has gcdfo-toc class and an accessible label.
    def _add_toc_class(match: re.Match) -> str:
        attrs = match.group(1)
        if "gcdfo-toc" in attrs:
            return match.group(0)
        label = attrs
        if "aria-label=" not in attrs:
            label = f'{attrs} aria-label="On this page"'
        return f'<nav class="toc gcdfo-toc"{label}>'

    content = re.sub(r'<nav class="toc"([^>]*)>', _add_toc_class, content, count=1)

    # Ensure dark mode toggle block exists inside TOC nav.
    if "<dark-mode-toggle" not in content:
        content = content.replace(
            '<div id="toc">',
            '  <div class="darkmode">\n'
            '    <dark-mode-toggle class="slider" aria-label="Toggle dark mode"></dark-mode-toggle>\n'
            "  </div>\n"
            '  <div id="toc">',
            1,
        )

    # Remove legacy UI snippet markers to avoid duplicate live paths.
    if OLD_UI_MARKER_BEGIN in content and OLD_UI_MARKER_END in content:
        pattern = re.compile(
            rf"{re.escape(OLD_UI_MARKER_BEGIN)}.*?{re.escape(OLD_UI_MARKER_END)}\n?",
            re.DOTALL,
        )
        content = pattern.sub("", content)

    # Ensure UI enhancement snippet exists.
    has_ui_snippet = UI_MARKER_BEGIN in content and UI_MARKER_END in content

    loadhash_start = content.find("function loadHash()")
    if loadhash_start == -1:
        raise RuntimeError("Could not find function loadHash() in docs/index.html")

    loadtoc_start = content.find("function loadTOC", loadhash_start)
    if loadtoc_start == -1:
        raise RuntimeError("Could not find function loadTOC in docs/index.html")

    pre = content[:loadhash_start]
    mid = content[loadhash_start:loadtoc_start]
    post = content[loadtoc_start:]

    # Ensure gcdfo enhancements are called inside loadHash().
    if "gcdfoEnhanceTOC();" not in mid:
        mid = mid.replace("loadTOC();", "loadTOC();\n  gcdfoEnhanceTOC();", 1)
    if "gcdfoEnhanceIRIs();" not in mid:
        mid = mid.replace("loadTOC();\n  gcdfoEnhanceTOC();", "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();", 1)
    if "gcdfoEnhanceSearch();" not in mid:
        mid = mid.replace(
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();",
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();\n  gcdfoEnhanceSearch();",
            1,
        )
    if "gcdfoEnhanceMobileTOC();" not in mid:
        mid = mid.replace(
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();\n  gcdfoEnhanceSearch();",
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();\n  gcdfoEnhanceSearch();\n  gcdfoEnhanceMobileTOC();",
            1,
        )
    if "gcdfoEnhancePermalinks();" not in mid:
        mid = mid.replace(
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();\n  gcdfoEnhanceSearch();\n  gcdfoEnhanceMobileTOC();",
            "loadTOC();\n  gcdfoEnhanceTOC();\n  gcdfoEnhanceIRIs();\n  gcdfoEnhanceSearch();\n  gcdfoEnhanceMobileTOC();\n  gcdfoEnhancePermalinks();",
            1,
        )

    if not has_ui_snippet:
        ui_snippet = "\n".join(
            [
                UI_MARKER_BEGIN,
                "function gcdfoCopyText(text) {",
                "  if (!text) return Promise.reject(new Error(\"No text to copy\"));",
                "  if (navigator.clipboard && navigator.clipboard.writeText) {",
                "    return navigator.clipboard.writeText(text);",
                "  }",
                "  return new Promise(function (resolve, reject) {",
                "    try {",
                "      var ta = document.createElement(\"textarea\");",
                "      ta.value = text;",
                "      ta.setAttribute(\"readonly\", \"\");",
                "      ta.style.position = \"absolute\";",
                "      ta.style.left = \"-9999px\";",
                "      document.body.appendChild(ta);",
                "      ta.select();",
                "      var ok = document.execCommand(\"copy\");",
                "      document.body.removeChild(ta);",
                "      if (ok) resolve();",
                "      else reject(new Error(\"Copy command failed\"));",
                "    } catch (e) {",
                "      reject(e);",
                "    }",
                "  });",
                "}",
                "",
                "function gcdfoGetHeadingText(heading) {",
                "  if (!heading) return \"\";",
                "  var clone = heading.cloneNode(true);",
                "  var sup = clone.querySelector(\"sup\");",
                "  if (sup) sup.remove();",
                "  return (clone.textContent || \"\").trim();",
                "}",
                "",
                "function gcdfoBuildSearchIndex() {",
                "  if (window.gcdfoSearchIndex) return window.gcdfoSearchIndex;",
                "  var items = [];",
                "  Array.prototype.slice.call(document.querySelectorAll(\".entity\")).forEach(function (entity) {",
                "    if (!entity || !entity.id) return;",
                "    var heading = entity.querySelector(\"h3\");",
                "    var label = gcdfoGetHeadingText(heading);",
                "    if (!label) return;",
                "    var sup = heading ? heading.querySelector(\"sup\") : null;",
                "    var type = sup ? (sup.textContent || \"\").trim() : \"\";",
                "    var iri = \"\";",
                "    var iriLine = entity.querySelector(\"p\");",
                "    if (iriLine && iriLine.textContent) {",
                "      iri = iriLine.textContent.replace(/^IRI:\\s*/, \"\").trim();",
                "    }",
                "    items.push({ id: entity.id, label: label, type: type, iri: iri });",
                "  });",
                "  window.gcdfoSearchIndex = items;",
                "  return items;",
                "}",
                "",
                "function gcdfoSearchTerms(query) {",
                "  var q = (query || \"\").trim().toLowerCase();",
                "  if (!q) return [];",
                "  var tokens = q.split(/\\s+/).filter(Boolean);",
                "  var items = gcdfoBuildSearchIndex();",
                "  return items.filter(function (item) {",
                "    var hay = (item.label + \" \" + item.id + \" \" + (item.iri || \"\")).toLowerCase();",
                "    return tokens.every(function (t) { return hay.indexOf(t) !== -1; });",
                "  });",
                "}",
                "",
                "function gcdfoEnsureTocNesting() {",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "  var rootList = toc.querySelector(\"ul\");",
                "  if (!rootList) return;",
                "",
                "  var children = Array.prototype.slice.call(rootList.children);",
                "  children.forEach(function (child) {",
                "    if (child && child.tagName === \"UL\") {",
                "      var prev = child.previousElementSibling;",
                "      while (prev && prev.tagName !== \"LI\") prev = prev.previousElementSibling;",
                "      if (prev) prev.appendChild(child);",
                "    }",
                "  });",
                "}",
                "",
                "function gcdfoFilterTOC(query) {",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "  var rootList = toc.querySelector(\"ul\");",
                "  if (!rootList) return;",
                "",
                "  var q = (query || \"\").trim().toLowerCase();",
                "  var topLis = Array.prototype.slice.call(rootList.children).filter(function (el) {",
                "    return el && el.tagName === \"LI\";",
                "  });",
                "",
                "  var anyVisible = false;",
                "  topLis.forEach(function (topLi) {",
                "    var topLink = null;",
                "    for (var i = 0; i < topLi.children.length; i++) {",
                "      if (topLi.children[i].tagName === \"A\") {",
                "        topLink = topLi.children[i];",
                "        break;",
                "      }",
                "      if (topLi.children[i].tagName === \"UL\") break;",
                "    }",
                "    var topText = (topLink ? topLink.textContent : topLi.textContent).toLowerCase();",
                "    var topMatches = q === \"\" || topText.indexOf(q) !== -1;",
                "",
                "    var subUl = null;",
                "    for (var j = 0; j < topLi.children.length; j++) {",
                "      if (topLi.children[j].tagName === \"UL\") {",
                "        subUl = topLi.children[j];",
                "        break;",
                "      }",
                "    }",
                "    var subLis = subUl ? Array.prototype.slice.call(subUl.children).filter(function (el) { return el && el.tagName === \"LI\"; }) : [];",
                "",
                "    var anyChildVisible = false;",
                "    subLis.forEach(function (subLi) {",
                "      var link = subLi.querySelector(\"a\");",
                "      var text = (link ? link.textContent : subLi.textContent).toLowerCase();",
                "      var matches = q === \"\" || topMatches || text.indexOf(q) !== -1;",
                "      subLi.style.display = matches ? \"\" : \"none\";",
                "      if (matches) anyChildVisible = true;",
                "    });",
                "",
                "    var showTop = q === \"\" || topMatches || anyChildVisible;",
                "    topLi.style.display = showTop ? \"\" : \"none\";",
                "    if (subUl) subUl.style.display = q === \"\" || topMatches || anyChildVisible ? \"\" : \"none\";",
                "",
                "    if (showTop) anyVisible = true;",
                "  });",
                "",
                "  var empty = toc.querySelector(\".gcdfo-toc-empty\");",
                "  if (empty) empty.hidden = anyVisible;",
                "}",
                "",
                "function gcdfoSetupActiveTOC() {",
                "  if (window.gcdfoTocObserver) return;",
                "",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "",
                "  var linkById = {};",
                "  Array.prototype.slice.call(toc.querySelectorAll('a[href^=\"#\"]')).forEach(function (a) {",
                "    var href = a.getAttribute(\"href\");",
                "    if (!href || href.length < 2) return;",
                "    var id = href.slice(1);",
                "    linkById[id] = a;",
                "  });",
                "",
                "  function setActive(id) {",
                "    if (!id || !linkById[id]) return;",
                "    if (window.gcdfoActiveTocLink) {",
                "      window.gcdfoActiveTocLink.classList.remove(\"gcdfo-active\");",
                "      window.gcdfoActiveTocLink.removeAttribute(\"aria-current\");",
                "    }",
                "    var next = linkById[id];",
                "    next.classList.add(\"gcdfo-active\");",
                "    next.setAttribute(\"aria-current\", \"true\");",
                "    window.gcdfoActiveTocLink = next;",
                "  }",
                "",
                "  var initial = location.hash ? location.hash.replace(\"#\", \"\") : \"\";",
                "  if (initial) setActive(initial);",
                "",
                "  if (!(\"IntersectionObserver\" in window)) return;",
                "  var headings = Array.prototype.slice",
                "    .call(document.querySelectorAll(\".list[id]\"))",
                "    .filter(function (el) {",
                "      return el && el.id && linkById[el.id];",
                "    });",
                "",
                "  var observer = new IntersectionObserver(",
                "    function (entries) {",
                "      entries.forEach(function (entry) {",
                "        if (entry.isIntersecting) setActive(entry.target.id);",
                "      });",
                "    },",
                "    { root: null, rootMargin: \"0px 0px -80% 0px\", threshold: 0.1 }",
                "  );",
                "  headings.forEach(function (h) {",
                "    observer.observe(h);",
                "  });",
                "  window.gcdfoTocObserver = observer;",
                "}",
                "",
                "function gcdfoEnhanceTOC() {",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "",
                "  gcdfoEnsureTocNesting();",
                "",
                "  if (!toc.querySelector(\"#toc-filter\")) {",
                "    var heading = toc.querySelector(\"h6\");",
                "    var controls = document.createElement(\"div\");",
                "    controls.className = \"gcdfo-toc-controls\";",
                "    controls.innerHTML =",
                "      '<label class=\"gcdfo-toc-filter-label\" for=\"toc-filter\">Filter</label>' +",
                "      '<input id=\"toc-filter\" class=\"gcdfo-toc-filter\" type=\"search\" placeholder=\"Filter sections…\" autocomplete=\"off\" />';",
                "    if (heading && heading.parentNode) heading.insertAdjacentElement(\"afterend\", controls);",
                "    else toc.insertBefore(controls, toc.firstChild);",
                "",
                "    var empty = document.createElement(\"div\");",
                "    empty.className = \"gcdfo-toc-empty\";",
                "    empty.hidden = true;",
                "    empty.textContent = \"No matching sections.\";",
                "    toc.appendChild(empty);",
                "  }",
                "",
                "  var input = toc.querySelector(\"#toc-filter\");",
                "  if (input && !input.dataset.gcdfoBound) {",
                "    input.dataset.gcdfoBound = \"1\";",
                "    input.addEventListener(\"input\", function () {",
                "      gcdfoFilterTOC(input.value);",
                "    });",
                "    input.addEventListener(\"keydown\", function (e) {",
                "      if (e.key === \"Escape\") {",
                "        input.value = \"\";",
                "        gcdfoFilterTOC(\"\");",
                "        input.blur();",
                "      }",
                "    });",
                "  }",
                "",
                "  gcdfoFilterTOC(input ? input.value : \"\");",
                "  gcdfoSetupActiveTOC();",
                "}",
                "",
                "function gcdfoEnhanceSearch() {",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "",
                "  if (!toc.querySelector(\".gcdfo-search\")) {",
                "    var controls = toc.querySelector(\".gcdfo-toc-controls\");",
                "    var search = document.createElement(\"div\");",
                "    search.className = \"gcdfo-search\";",
                "    search.innerHTML =",
                "      '<label class=\"gcdfo-search-label\" for=\"gcdfo-search\">Search terms</label>' +",
                "      '<input id=\"gcdfo-search\" class=\"gcdfo-search-input\" type=\"search\" placeholder=\"Search classes, properties, concepts…\" autocomplete=\"off\" />' +",
                "      '<div class=\"gcdfo-search-meta\" id=\"gcdfo-search-meta\">Type to search the ontology terms.</div>' +",
                "      '<ul class=\"gcdfo-search-results\" id=\"gcdfo-search-results\"></ul>';",
                "    if (controls && controls.parentNode) {",
                "      controls.insertAdjacentElement(\"afterend\", search);",
                "    } else {",
                "      toc.insertBefore(search, toc.firstChild);",
                "    }",
                "  }",
                "",
                "  var input = toc.querySelector(\"#gcdfo-search\");",
                "  var resultsEl = toc.querySelector(\"#gcdfo-search-results\");",
                "  var metaEl = toc.querySelector(\"#gcdfo-search-meta\");",
                "  if (!input || !resultsEl || !metaEl) return;",
                "",
                "  function render(results) {",
                "    resultsEl.innerHTML = \"\";",
                "    if (!results.length) {",
                "      metaEl.textContent = \"No matches.\";",
                "      resultsEl.hidden = true;",
                "      return;",
                "    }",
                "    metaEl.textContent = results.length + \" match\" + (results.length === 1 ? \"\" : \"es\") + \".\";",
                "    resultsEl.hidden = false;",
                "    results.slice(0, 50).forEach(function (item) {",
                "      var li = document.createElement(\"li\");",
                "      var link = document.createElement(\"a\");",
                "      link.href = \"#\" + item.id;",
                "      link.textContent = item.label;",
                "      li.appendChild(link);",
                "      if (item.type) {",
                "        var meta = document.createElement(\"span\");",
                "        meta.className = \"gcdfo-search-type\";",
                "        meta.textContent = item.type;",
                "        li.appendChild(meta);",
                "      }",
                "      resultsEl.appendChild(li);",
                "    });",
                "  }",
                "",
                "  if (!input.dataset.gcdfoBound) {",
                "    input.dataset.gcdfoBound = \"1\";",
                "    input.addEventListener(\"input\", function () {",
                "      var query = input.value;",
                "      if (query.trim().length < 2) {",
                "        resultsEl.hidden = true;",
                "        metaEl.textContent = \"Type to search the ontology terms.\";",
                "        return;",
                "      }",
                "      var results = gcdfoSearchTerms(query);",
                "      render(results);",
                "    });",
                "    input.addEventListener(\"keydown\", function (e) {",
                "      if (e.key === \"Escape\") {",
                "        input.value = \"\";",
                "        resultsEl.hidden = true;",
                "        metaEl.textContent = \"Type to search the ontology terms.\";",
                "        input.blur();",
                "      }",
                "    });",
                "  }",
                "}",
                "",
                "function gcdfoEnhanceMobileTOC() {",
                "  var toc = document.getElementById(\"toc\");",
                "  if (!toc) return;",
                "",
                "  var panel = document.querySelector(\".gcdfo-toc-panel\");",
                "  if (!panel) {",
                "    panel = document.createElement(\"div\");",
                "    panel.className = \"gcdfo-toc-panel\";",
                "    toc.parentNode.insertBefore(panel, toc);",
                "    panel.appendChild(toc);",
                "  }",
                "",
                "  if (!document.querySelector(\".gcdfo-toc-overlay\")) {",
                "    var overlay = document.createElement(\"div\");",
                "    overlay.className = \"gcdfo-toc-overlay\";",
                "    overlay.addEventListener(\"click\", function () {",
                "      document.body.classList.remove(\"gcdfo-toc-open\");",
                "    });",
                "    document.body.appendChild(overlay);",
                "  }",
                "",
                "  if (!document.querySelector(\".gcdfo-toc-toggle\")) {",
                "    var toggle = document.createElement(\"button\");",
                "    toggle.type = \"button\";",
                "    toggle.className = \"gcdfo-toc-toggle\";",
                "    toggle.textContent = \"Sections\";",
                "    toggle.setAttribute(\"aria-expanded\", \"false\");",
                "    toggle.addEventListener(\"click\", function () {",
                "      var open = document.body.classList.toggle(\"gcdfo-toc-open\");",
                "      toggle.setAttribute(\"aria-expanded\", open ? \"true\" : \"false\");",
                "    });",
                "    var head = document.querySelector(\".head\") || document.body;",
                "    head.insertBefore(toggle, head.firstChild);",
                "  }",
                "",
                "  Array.prototype.slice.call(toc.querySelectorAll('a[href^=\"#\"]')).forEach(function (link) {",
                "    if (link.dataset.gcdfoCloseBound) return;",
                "    link.dataset.gcdfoCloseBound = \"1\";",
                "    link.addEventListener(\"click\", function () {",
                "      document.body.classList.remove(\"gcdfo-toc-open\");",
                "      var toggle = document.querySelector(\".gcdfo-toc-toggle\");",
                "      if (toggle) toggle.setAttribute(\"aria-expanded\", \"false\");",
                "    });",
                "  });",
                "}",
                "",
                "function gcdfoEnhancePermalinks() {",
                "  gcdfoEnsureCopyStatusEl();",
                "  var headings = [];",
                "  Array.prototype.slice.call(document.querySelectorAll(\"h2.list[id], h3.list[id]\")).forEach(function (h) {",
                "    headings.push({ heading: h, target: h.id });",
                "  });",
                "  Array.prototype.slice.call(document.querySelectorAll(\".entity\")).forEach(function (entity) {",
                "    var heading = entity.querySelector(\"h3\");",
                "    if (heading && entity.id) headings.push({ heading: heading, target: entity.id });",
                "  });",
                "",
                "  headings.forEach(function (item) {",
                "    if (!item.heading || !item.target) return;",
                "    if (item.heading.querySelector(\".gcdfo-permalink\")) return;",
                "    var btn = document.createElement(\"button\");",
                "    btn.type = \"button\";",
                "    btn.className = \"gcdfo-permalink\";",
                "    btn.setAttribute(\"aria-label\", \"Copy link to \" + gcdfoGetHeadingText(item.heading));",
                "    btn.textContent = \"#\";",
                "    btn.addEventListener(\"click\", function () {",
                "      var url = window.location.origin + window.location.pathname + \"#\" + item.target;",
                "      gcdfoCopyText(url)",
                "        .then(function () {",
                "          gcdfoFlashCopied(btn, \"Link copied.\");",
                "        })",
                "        .catch(function () {",
                "          gcdfoFlashCopied(btn, \"Copy failed.\");",
                "        });",
                "      window.location.hash = item.target;",
                "    });",
                "    item.heading.appendChild(btn);",
                "  });",
                "}",
                "",
                "function gcdfoEnsureCopyStatusEl() {",
                "  if (document.getElementById(\"gcdfo-copy-status\")) return;",
                "  var el = document.createElement(\"div\");",
                "  el.id = \"gcdfo-copy-status\";",
                "  el.className = \"visually-hidden\";",
                "  el.setAttribute(\"aria-live\", \"polite\");",
                "  document.body.appendChild(el);",
                "}",
                "",
                "function gcdfoFlashCopied(button, message) {",
                "  var status = document.getElementById(\"gcdfo-copy-status\");",
                "  if (status) status.textContent = message || \"Copied.\";",
                "  if (!button) return;",
                "  var prev = button.textContent;",
                "  button.textContent = \"Copied\";",
                "  button.disabled = true;",
                "  window.setTimeout(function () {",
                "    button.textContent = prev;",
                "    button.disabled = false;",
                "  }, 1200);",
                "}",
                "",
                "function gcdfoEnhanceIRIs() {",
                "  gcdfoEnsureCopyStatusEl();",
                "",
                "  // Add copy buttons to entity IRI lines.",
                "  Array.prototype.slice.call(document.querySelectorAll(\".entity p\")).forEach(function (p) {",
                "    if (!p || p.querySelector(\".gcdfo-copy-btn\")) return;",
                "    var strong = p.querySelector(\"strong\");",
                "    if (!strong) return;",
                "    if (strong.textContent.trim() !== \"IRI:\") return;",
                "",
                "    var iri = p.textContent.replace(/^IRI:\\s*/, \"\").trim();",
                "    if (!iri || iri.indexOf(\"http\") !== 0) return;",
                "",
                "    // Rebuild the line to keep the visible IRI copy-friendly.",
                "    while (strong.nextSibling) p.removeChild(strong.nextSibling);",
                "    p.appendChild(document.createTextNode(\" \"));",
                "",
                "    var code = document.createElement(\"code\");",
                "    code.className = \"gcdfo-iri\";",
                "    code.textContent = iri;",
                "    p.appendChild(code);",
                "",
                "    p.appendChild(document.createTextNode(\" \"));",
                "    var btn = document.createElement(\"button\");",
                "    btn.type = \"button\";",
                "    btn.className = \"gcdfo-copy-btn\";",
                "    btn.textContent = \"Copy\";",
                "    btn.setAttribute(\"aria-label\", \"Copy IRI to clipboard\");",
                "    btn.dataset.copy = iri;",
                "    btn.addEventListener(\"click\", function () {",
                "      var toCopy = btn.dataset.copy || \"\";",
                "      gcdfoCopyText(toCopy)",
                "        .then(function () {",
                "          gcdfoFlashCopied(btn, \"Copied IRI to clipboard.\");",
                "        })",
                "        .catch(function () {",
                "          gcdfoFlashCopied(btn, \"Copy failed.\");",
                "        });",
                "    });",
                "    p.appendChild(btn);",
                "  });",
                "}",
                UI_MARKER_END,
                "",
            ]
        )
        content = pre + mid + ui_snippet + post
    else:
        content = pre + mid + post

    INDEX_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    schemes, concepts = parse_ttl()
    section = build_section(schemes, concepts)
    replace_section(section)
    update_index_metadata(extract_ontology_metadata())
    ensure_owl_before_skos_ordering()
    ensure_custom_ui_enhancements()
    print("✅ Updated docs/index.html SKOS section with every scheme/concept.")


if __name__ == "__main__":
    main()
