#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from textwrap import shorten
import html
import math
import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL

ROOT = Path(__file__).resolve().parents[1]
VIEW_PATH = ROOT / "ontology" / "views" / "wsp-composite-escapement-view.ttl"
ONTOLOGY_PATH = ROOT / "ontology" / "dfo-salmon.ttl"
MD_PATH = ROOT / "ontology" / "views" / "wsp-composite-escapement-review.md"
GRAPHML_PATH = ROOT / "ontology" / "views" / "wsp-composite-escapement-review.graphml"

G = Graph().parse(VIEW_PATH, format="turtle")
ONTO = Graph().parse(ONTOLOGY_PATH, format="turtle")

GCD = Namespace("https://w3id.org/gcdfo/salmon#")
WSPVIEW = Namespace("https://w3id.org/gcdfo/salmon/views/wsp-composite-escapement#")
SMN = Namespace("https://w3id.org/smn/")
QK = Namespace("http://qudt.org/vocab/quantitykind/")
UNIT = Namespace("http://qudt.org/vocab/unit/")
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")

MAPPING_PREDS = [
    (WSPVIEW.mappedTerm, "mappedTerm"),
    (WSPVIEW.mappedProperty, "mappedProperty"),
    (WSPVIEW.mappedEntity, "mappedEntity"),
    (WSPVIEW.mappedConstraint, "mappedConstraint"),
    (WSPVIEW.mappedUnit, "mappedUnit"),
    (WSPVIEW.mappedMethod, "mappedMethod"),
]
TERM_CONTEXT_PREDS = [
    (SKOS.broader, "broader"),
    (SKOS.inScheme, "inScheme"),
    (SKOS.related, "related"),
    (GCD.iadoptEntity, "iadoptEntity"),
    (GCD.iadoptProperty, "iadoptProperty"),
    (GCD.iadoptConstraint, "iadoptConstraint"),
    (GCD.usedProcedure, "usedProcedure"),
]


def uri_local(uri: URIRef) -> str:
    s = str(uri)
    if "#" in s:
        return s.split("#", 1)[1]
    return s.rsplit("/", 1)[-1]


def curie(uri: URIRef | str) -> str:
    s = str(uri)
    for base, prefix in [
        (str(GCD), "gcdfo:"),
        (str(WSPVIEW), "wspview:"),
        (str(SMN), "smn:"),
        (str(DWC), "dwc:"),
        (str(QK), "quantitykind:"),
        (str(UNIT), "unit:"),
        (str(SKOS), "skos:"),
        (str(RDFS), "rdfs:"),
        (str(DCTERMS), "dcterms:"),
        (str(OWL), "owl:"),
    ]:
        if s.startswith(base):
            return prefix + s[len(base):]
    return s


def label_for(node: URIRef | Literal) -> str:
    if isinstance(node, Literal):
        return str(node)
    for pred in (SKOS.prefLabel, RDFS.label):
        val = next(G.objects(node, pred), None) or next(ONTO.objects(node, pred), None)
        if val:
            return str(val)
    return uri_local(node)


def literal_text(node: URIRef, pred: URIRef) -> str:
    vals = list(G.objects(node, pred)) or list(ONTO.objects(node, pred))
    if not vals:
        return ""
    return str(vals[0])


def bool_deprecated(node: URIRef) -> bool:
    vals = list(ONTO.objects(node, OWL.deprecated)) or list(G.objects(node, OWL.deprecated))
    return any(str(v).lower() == "true" for v in vals)


def is_wsp_themed(node: URIRef) -> bool:
    return (node, GCD.theme, GCD.WildSalmonPolicyTheme) in ONTO or (node, GCD.theme, GCD.WildSalmonPolicyTheme) in G


def collection_members(collection: URIRef) -> list[URIRef]:
    return [o for o in G.objects(collection, SKOS.member) if isinstance(o, URIRef)]


curated_terms = set(collection_members(WSPVIEW.CuratedWSPReviewTerms))
modeled_terms = set(collection_members(WSPVIEW.ModeledCanonicalWSPOutputTerms))
csv_aligned_terms = set(collection_members(WSPVIEW.CsvAlignedOntologyTerms))
source_vars = sorted(
    {s for s in G.subjects() if isinstance(s, URIRef) and str(s).startswith(str(WSPVIEW) + "var_")},
    key=lambda u: label_for(u).lower(),
)

included_nodes: set[URIRef] = set(source_vars) | curated_terms | modeled_terms | csv_aligned_terms
edges: list[tuple[URIRef, URIRef, str]] = []

for var in source_vars:
    for pred, name in MAPPING_PREDS:
        for obj in G.objects(var, pred):
            if isinstance(obj, URIRef):
                if obj == SKOS.Concept:
                    # Too generic to help the graph; keep it in the Markdown table only.
                    continue
                included_nodes.add(obj)
                edges.append((var, obj, name))

for term in list(curated_terms | modeled_terms | csv_aligned_terms):
    for pred, name in TERM_CONTEXT_PREDS:
        for obj in G.objects(term, pred) or ONTO.objects(term, pred):
            if isinstance(obj, URIRef):
                included_nodes.add(obj)
                edges.append((term, obj, name))

# Keep the graph compact: only one-hop context from curated/modelled terms, source vars, and key schemes.
# Drop collections and view-local mapping properties from visible nodes.
included_nodes = {
    n
    for n in included_nodes
    if not str(n).startswith(str(WSPVIEW)) or str(n).startswith(str(WSPVIEW) + "var_")
}


def node_category(node: URIRef) -> str:
    s = str(node)
    if s.startswith(str(WSPVIEW) + "var_"):
        status = literal_text(node, WSPVIEW.mappingStatus)
        return "source_unmapped" if "unmapped" in status else "source"
    if node in modeled_terms:
        return "modeled_term"
    if node in curated_terms and (s.startswith(str(GCD)) or s.startswith(str(SMN))):
        if s.startswith(str(SMN)):
            return "salmon_domain"
        if str(uri_local(node)).endswith("Scheme"):
            return "scheme"
        return "wsp_context"
    if s.startswith(str(SMN)):
        return "salmon_domain"
    if s.startswith(str(GCD)):
        if str(uri_local(node)).endswith("Scheme"):
            return "scheme"
        return "wsp_context" if is_wsp_themed(node) else "gcdfo_context"
    return "external"


CATEGORY_STYLE = {
    "source": {"fill": "#FFF2CC", "border": "#C9B458", "shape": "roundrectangle"},
    "source_unmapped": {"fill": "#F4CCCC", "border": "#CC0000", "shape": "roundrectangle"},
    "modeled_term": {"fill": "#C9DAF8", "border": "#3C78D8", "shape": "rectangle"},
    "wsp_context": {"fill": "#F9CB9C", "border": "#E69138", "shape": "rectangle"},
    "gcdfo_context": {"fill": "#D0E0E3", "border": "#76A5AF", "shape": "rectangle"},
    "salmon_domain": {"fill": "#D9EAD3", "border": "#6AA84F", "shape": "rectangle"},
    "scheme": {"fill": "#EAD1DC", "border": "#C27BA0", "shape": "hexagon"},
    "external": {"fill": "#E6E6E6", "border": "#999999", "shape": "rectangle"},
}


def node_label(node: URIRef) -> str:
    cat = node_category(node)
    name = label_for(node)
    cur = curie(node)
    if cat.startswith("source"):
        status = literal_text(node, WSPVIEW.mappingStatus)
        if "unmapped" in status:
            return f"{name}\n(unmapped source field)"
        return f"{name}\n(source field)"
    if bool_deprecated(node):
        return f"{name}\n(deprecated)"
    if cat == "scheme":
        return f"{name}\n(scheme)"
    return f"{name}\n{cur}"


# Stable node ids/order
ordered_nodes = sorted(included_nodes, key=lambda n: (node_category(n), label_for(n).lower(), str(n)))
node_ids = {n: f"n{i}" for i, n in enumerate(ordered_nodes)}

# Simple layered layout for yEd.
category_columns = {
    "scheme": 0,
    "source": 0,
    "source_unmapped": 0,
    "modeled_term": 1,
    "wsp_context": 2,
    "gcdfo_context": 2,
    "salmon_domain": 3,
    "external": 4,
}
category_groups: dict[str, list[URIRef]] = defaultdict(list)
for n in ordered_nodes:
    category_groups[node_category(n)].append(n)
positions: dict[URIRef, tuple[float, float]] = {}
for cat, nodes in category_groups.items():
    col = category_columns[cat]
    x = 80 + col * 260
    for i, node in enumerate(nodes):
        y = 80 + i * 90
        positions[node] = (x, y)

EDGE_COLORS = {
    "mappedTerm": "#3C78D8",
    "mappedProperty": "#3C78D8",
    "mappedEntity": "#3C78D8",
    "mappedConstraint": "#3C78D8",
    "mappedUnit": "#3C78D8",
    "mappedMethod": "#3C78D8",
    "broader": "#999999",
    "inScheme": "#C27BA0",
    "related": "#E69138",
    "iadoptEntity": "#76A5AF",
    "iadoptProperty": "#76A5AF",
    "iadoptConstraint": "#76A5AF",
    "usedProcedure": "#76A5AF",
}

# Build GraphML with yWorks markup.
NS_G = "http://graphml.graphdrawing.org/xmlns"
NS_Y = "http://www.yworks.com/xml/graphml"
NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
ET.register_namespace("", NS_G)
ET.register_namespace("y", NS_Y)
ET.register_namespace("xsi", NS_XSI)

root = ET.Element(
    f"{{{NS_G}}}graphml",
    {
        f"{{{NS_XSI}}}schemaLocation": (
            f"{NS_G} http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd"
        )
    },
)
ET.SubElement(root, f"{{{NS_G}}}key", id="d0", **{"for": "node", "yfiles.type": "nodegraphics"})
ET.SubElement(root, f"{{{NS_G}}}key", id="d1", **{"for": "edge", "yfiles.type": "edgegraphics"})
ET.SubElement(root, f"{{{NS_G}}}key", id="d2", **{"for": "node", "attr.name": "description", "attr.type": "string"})
graph_el = ET.SubElement(root, f"{{{NS_G}}}graph", id="G", edgedefault="directed")

for node in ordered_nodes:
    nid = node_ids[node]
    cat = node_category(node)
    style = CATEGORY_STYLE[cat]
    x, y = positions[node]
    width = 220
    height = 58 if "\n" in node_label(node) else 42
    node_el = ET.SubElement(graph_el, f"{{{NS_G}}}node", id=nid)
    desc = ET.SubElement(node_el, f"{{{NS_G}}}data", key="d2")
    desc.text = curie(node)
    data = ET.SubElement(node_el, f"{{{NS_G}}}data", key="d0")
    shape_node = ET.SubElement(data, f"{{{NS_Y}}}ShapeNode")
    ET.SubElement(shape_node, f"{{{NS_Y}}}Geometry", x=f"{x:.1f}", y=f"{y:.1f}", width=str(width), height=str(height))
    ET.SubElement(shape_node, f"{{{NS_Y}}}Fill", color=style["fill"], transparent="false")
    border_type = "dashed" if bool_deprecated(node) else "line"
    ET.SubElement(shape_node, f"{{{NS_Y}}}BorderStyle", color=style["border"], type=border_type, width="1.5")
    label_el = ET.SubElement(
        shape_node,
        f"{{{NS_Y}}}NodeLabel",
        alignment="center",
        autoSizePolicy="content",
        fontFamily="Helvetica",
        fontSize="12",
    )
    label_el.text = node_label(node)
    ET.SubElement(shape_node, f"{{{NS_Y}}}Shape", type=style["shape"])

# De-duplicate edges.
seen_edges = set()
edge_counter = 0
for src, tgt, label in edges:
    if src not in node_ids or tgt not in node_ids:
        continue
    key = (src, tgt, label)
    if key in seen_edges:
        continue
    seen_edges.add(key)
    edge_el = ET.SubElement(graph_el, f"{{{NS_G}}}edge", id=f"e{edge_counter}", source=node_ids[src], target=node_ids[tgt])
    edge_counter += 1
    data = ET.SubElement(edge_el, f"{{{NS_G}}}data", key="d1")
    poly = ET.SubElement(data, f"{{{NS_Y}}}PolyLineEdge")
    ET.SubElement(poly, f"{{{NS_Y}}}LineStyle", color=EDGE_COLORS.get(label, "#999999"), type="line", width="1.2")
    ET.SubElement(poly, f"{{{NS_Y}}}Arrows", source="none", target="standard")
    edge_label = ET.SubElement(poly, f"{{{NS_Y}}}EdgeLabel", alignment="center", fontFamily="Helvetica", fontSize="10")
    edge_label.text = label
    ET.SubElement(poly, f"{{{NS_Y}}}BendStyle", smoothed="false")

ET.ElementTree(root).write(GRAPHML_PATH, encoding="utf-8", xml_declaration=True)


def mapping_values(var: URIRef, pred: URIRef) -> str:
    vals = [curie(o) for o in G.objects(var, pred)]
    return ", ".join(vals) if vals else ""


def table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"

legend_rows = [
    ("Source field", "yellow", "Canonical WSP composite-escapement source column"),
    ("Modeled canonical term", "blue", "First-class DFO Salmon Ontology term added or used to represent canonical WSP output semantics"),
    ("WSP context term", "orange", "Wild Salmon Policy-themed DFO context term kept one level up for review"),
    ("Salmon Domain Ontology term", "green", "Shared Salmon Domain context term"),
    ("Scheme", "pink", "Scheme / grouping concept"),
    ("External reference", "gray", "External semantics such as DwC/QUDT/SKOS"),
]

md: list[str] = []
md.append("# WSP composite-escapement review pack")
md.append("")
md.append("This file is the human review surface for Wild Salmon Policy composite-escapement semantics. It complements `wsp-composite-escapement-view.ttl`; it does not replace the authoritative ontology definitions in `ontology/dfo-salmon.ttl`.")
md.append("")
md.append("## Why this exists")
md.append("")
md.append("WebVowl is a poor fit for this review problem because the important content is source-field mapping, SKOS concepts, and light one-level-up context rather than rich OWL class hierarchies. Use this Markdown file for discussion and the GraphML file for picture-based review in yEd.")
md.append("")
md.append("## Files")
md.append("")
md.append("- `ontology/views/wsp-composite-escapement-view.ttl` — machine-readable curated Turtle view")
md.append("- `ontology/views/wsp-composite-escapement-review.md` — human review file")
md.append("- `ontology/views/wsp-composite-escapement-review.graphml` — yEd/yEd Live graph")
md.append("")
md.append("## Graph legend")
md.append("")
md.append(table_row(["Node type", "Color", "Meaning"]))
md.append(table_row(["---", "---", "---"]))
for row in legend_rows:
    md.append(table_row(list(row)))
md.append("")
md.append("## Coverage summary")
md.append("")
modeled_source_fields = sum(1 for v in source_vars if literal_text(v, WSPVIEW.mappingStatus) == "mapped")
unmapped_source_fields = len(source_vars) - modeled_source_fields
md.append(f"- Source fields in canonical composite-escapement output: **{len(source_vars)}**")
md.append(f"- Source fields mapped in the review view: **{modeled_source_fields}**")
md.append(f"- Source fields still explicitly unmapped: **{unmapped_source_fields}** (`CU_ID`, `Year`)" if unmapped_source_fields else "- No currently unmapped source fields.")
md.append(f"- Curated WSP review terms: **{len(curated_terms)}**")
md.append(f"- Modeled canonical WSP output terms: **{len(modeled_terms)}**")
md.append("")
md.append("## Review hotspots")
md.append("")
md.append("- `CU_ID` and `Year` remain intentionally unmapped.")
md.append("- `DataType`, `BinLabel`, and `BinPath` are still helper-ish and may not deserve full ontology treatment.")
md.append("- `IntStatus5`, `IntStatus3`, and `IntStatus2` remain in the graph because they are legacy output columns that colleagues may still recognize.")
md.append("- The GraphML intentionally keeps only one-level-up context so the picture stays readable.")
md.append("")
md.append("## Source-column mapping table")
md.append("")
md.append(table_row(["Source field", "Status", "Mapped term", "Property", "Entity", "Constraint", "Unit", "Notes"]))
md.append(table_row(["---", "---", "---", "---", "---", "---", "---", "---"]))
for var in source_vars:
    status = literal_text(var, WSPVIEW.mappingStatus) or ""
    note = literal_text(var, WSPVIEW.notes) or ""
    legacy = ", ".join(str(o) for o in G.objects(var, WSPVIEW.legacyIri))
    note_parts = [p for p in [note, f"legacy: {legacy}" if legacy else ""] if p]
    md.append(
        table_row(
            [
                label_for(var),
                status,
                mapping_values(var, WSPVIEW.mappedTerm),
                mapping_values(var, WSPVIEW.mappedProperty),
                mapping_values(var, WSPVIEW.mappedEntity),
                mapping_values(var, WSPVIEW.mappedConstraint),
                mapping_values(var, WSPVIEW.mappedUnit),
                "<br>".join(note_parts),
            ]
        )
    )
md.append("")

md.append("## Modeled canonical WSP output terms")
md.append("")
md.append(table_row(["Term", "Deprecated", "Broader / scheme", "Entity", "Property", "Constraint", "Notes"]))
md.append(table_row(["---", "---", "---", "---", "---", "---", "---"]))
for term in sorted(modeled_terms, key=lambda t: label_for(t).lower()):
    broader = ", ".join(curie(o) for o in G.objects(term, SKOS.broader))
    schemes = ", ".join(curie(o) for o in G.objects(term, SKOS.inScheme))
    broader_scheme = "; ".join(x for x in [broader, schemes] if x)
    notes = []
    scope_note = literal_text(term, SKOS.scopeNote)
    if scope_note:
        notes.append(scope_note)
    if bool_deprecated(term):
        notes.append("deprecated")
    md.append(
        table_row(
            [
                f"{label_for(term)} (`{curie(term)}`)",
                "yes" if bool_deprecated(term) else "no",
                broader_scheme,
                ", ".join(curie(o) for o in ONTO.objects(term, GCD.iadoptEntity) or G.objects(term, GCD.iadoptEntity)),
                ", ".join(curie(o) for o in ONTO.objects(term, GCD.iadoptProperty) or G.objects(term, GCD.iadoptProperty)),
                ", ".join(curie(o) for o in ONTO.objects(term, GCD.iadoptConstraint) or G.objects(term, GCD.iadoptConstraint)),
                "<br>".join(notes),
            ]
        )
    )
md.append("")

md.append("## One-level-up WSP context kept in the graph")
md.append("")
md.append(table_row(["Term", "Role in graph"]))
md.append(table_row(["---", "---"]))
for term in sorted(curated_terms - modeled_terms, key=lambda t: label_for(t).lower()):
    cat = node_category(term)
    role = {
        "scheme": "scheme / grouping context",
        "wsp_context": "WSP-specific context term",
        "salmon_domain": "shared Salmon Domain context term",
        "external": "external reference term",
        "gcdfo_context": "DFO context term",
    }.get(cat, cat)
    md.append(table_row([f"{label_for(term)} (`{curie(term)}`)", role]))
md.append("")

MD_PATH.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
print(f"Wrote {MD_PATH}")
print(f"Wrote {GRAPHML_PATH}")
