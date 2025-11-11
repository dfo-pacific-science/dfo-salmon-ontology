"""
Generate themed ontology term tables and matching SPARQL query files.

This script reads theme definitions from scripts/config/themes.yml,
builds SPARQL queries for each theme, writes the queries to scripts/sparql/,
executes them against ontology/dfo-salmon.ttl using RDFLib, and exports
deterministically ordered CSV + metadata files under release/artifacts/term-tables/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import rdflib
import yaml


ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = ROOT / "ontology" / "dfo-salmon.ttl"
CONFIG_PATH = ROOT / "scripts" / "config" / "themes.yml"
QUERY_DIR = ROOT / "scripts" / "sparql"
OUTPUT_DIR = ROOT / "release" / "artifacts" / "term-tables"
IAO_DEFINITION_IRI = rdflib.URIRef("http://purl.obolibrary.org/obo/IAO_0000115")

COMMON_PREFIXES = """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
"""

COMMON_OPTIONALS = textwrap.dedent(
    """\
OPTIONAL {
  ?term skos:prefLabel ?prefLabelRaw .
  FILTER(LANG(?prefLabelRaw) = "" || LANGMATCHES(LANG(?prefLabelRaw), "en"))
}
OPTIONAL {
  ?term rdfs:label ?rdfsLabelRaw .
  FILTER(LANG(?rdfsLabelRaw) = "" || LANGMATCHES(LANG(?rdfsLabelRaw), "en"))
}
BIND(COALESCE(?prefLabelRaw, ?rdfsLabelRaw, STRAFTER(STR(?term), "#")) AS ?termLabel) .

OPTIONAL {
  ?scheme skos:prefLabel ?schemePref .
  FILTER(LANG(?schemePref) = "" || LANGMATCHES(LANG(?schemePref), "en"))
}
BIND(COALESCE(?schemePref, STRAFTER(STR(?scheme), "#")) AS ?schemeLabel) .

OPTIONAL {
  ?term skos:definition ?defSKOS .
  FILTER(LANG(?defSKOS) = "" || LANGMATCHES(LANG(?defSKOS), "en"))
}
OPTIONAL {
  ?term rdfs:comment ?defRDFS .
  FILTER(LANG(?defRDFS) = "" || LANGMATCHES(LANG(?defRDFS), "en"))
}
OPTIONAL {
  ?term <http://purl.obolibrary.org/obo/IAO_0000115> ?defIAO .
  FILTER(LANG(?defIAO) = "" || LANGMATCHES(LANG(?defIAO), "en"))
}
BIND(COALESCE(?defSKOS, ?defRDFS, ?defIAO) AS ?definition) .

OPTIONAL {
  ?term <http://purl.obolibrary.org/obo/IAO_0000119> ?definitionSourceText .
  FILTER(LANG(?definitionSourceText) = "" || LANGMATCHES(LANG(?definitionSourceText), "en"))
}
OPTIONAL {
  ?term dcterms:source ?definitionSourceLink .
}

OPTIONAL {
  {
    ?term skos:broader ?related .
    BIND("skos:broader" AS ?relation) .
  }
  UNION
  {
    ?term skos:narrower ?related .
    BIND("skos:narrower" AS ?relation) .
  }
  UNION
  {
    ?term rdfs:subClassOf ?related .
    BIND("rdfs:subClassOf" AS ?relation) .
  }
  OPTIONAL {
    ?related skos:prefLabel ?relatedPref .
    FILTER(LANG(?relatedPref) = "" || LANGMATCHES(LANG(?relatedPref), "en"))
  }
  OPTIONAL {
    ?related rdfs:label ?relatedLabelRaw .
    FILTER(LANG(?relatedLabelRaw) = "" || LANGMATCHES(LANG(?relatedLabelRaw), "en"))
  }
BIND(COALESCE(?relatedPref, ?relatedLabelRaw, STRAFTER(STR(?related), "#")) AS ?relatedLabel) .
}
"""
)

ORDER_BY_CLAUSE = (
    "ORDER BY LCASE(?termLabel) STR(?term) "
    'LCASE(COALESCE(?relatedLabel, "")) STR(COALESCE(?related, ""))'
)


class Theme:
    """Definition for a themed extraction."""

    def __init__(
        self,
        *,
        id: str,
        label: str,
        query_file: str,
        output_csv: str,
        schemes: Optional[List[str]] = None,
        classes: Optional[List[str]] = None,
    ) -> None:
        self.id = id
        self.label = label
        self.query_file = query_file
        self.output_csv = output_csv
        self.schemes = schemes or []
        self.classes = classes or []
        if not (self.schemes or self.classes):
            raise ValueError(f"Theme {self.id} must define schemes or classes.")

    @property
    def query_path(self) -> Path:
        return QUERY_DIR / self.query_file

    @property
    def output_csv_path(self) -> Path:
        return OUTPUT_DIR / self.output_csv

    @property
    def output_meta_path(self) -> Path:
        return self.output_csv_path.with_suffix(".meta.json")


def read_config() -> tuple[str, List[Theme]]:
    """Load YAML configuration and return widoco base url plus themes."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing theme configuration: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    widoco_base_url = raw.get("widoco_base_url")
    if not widoco_base_url:
        raise ValueError("Theme configuration must set widoco_base_url.")

    themes = [
        Theme(
            id=entry["id"],
            label=entry["label"],
            query_file=entry["query_file"],
            output_csv=entry["output_csv"],
            schemes=entry.get("schemes", []),
            classes=entry.get("classes", []),
        )
        for entry in raw.get("themes", [])
    ]

    if not themes:
        raise ValueError("No themes configured; update scripts/config/themes.yml.")

    return widoco_base_url, themes


def build_schemes_query(theme: Theme) -> Optional[str]:
    """Construct a SPARQL query for SKOS concepts within configured schemes."""
    if not theme.schemes:
        return None

    scheme_values = " ".join(f"<{iri}>" for iri in theme.schemes)
    optional_block = textwrap.indent(COMMON_OPTIONALS, "  ")

    return (
        f"{COMMON_PREFIXES}\n"
        "SELECT DISTINCT ?term ?termLabel ?definition ?definitionSourceText ?definitionSourceLink ?related ?relatedLabel ?relation\n"
        "WHERE {\n"
        f"  VALUES ?scheme {{ {scheme_values} }}\n"
        "  ?term skos:inScheme ?scheme .\n"
        "  ?term a skos:Concept .\n"
        f"{optional_block}\n"
        "}\n"
        f"{ORDER_BY_CLAUSE}"
    )


def build_classes_query(theme: Theme) -> Optional[str]:
    """Construct a SPARQL query for explicit OWL classes within the theme."""
    if not theme.classes:
        return None

    class_values = " ".join(f"<{iri}>" for iri in theme.classes)
    optional_block = textwrap.indent(COMMON_OPTIONALS, "  ")

    return (
        f"{COMMON_PREFIXES}\n"
        "SELECT DISTINCT ?term ?termLabel ?definition ?definitionSourceText ?definitionSourceLink ?related ?relatedLabel ?relation\n"
        "WHERE {\n"
        f"  VALUES ?term {{ {class_values} }}\n"
        "  ?term a owl:Class .\n"
        f"{optional_block}\n"
        "}\n"
        f"{ORDER_BY_CLAUSE}"
    )


def get_repo_commit(root: Path) -> str:
    """Return current git commit SHA for the repository."""
    try:
        sha = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            )
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError("Unable to resolve git commit SHA") from exc
    return sha


def ensure_directories() -> None:
    """Ensure output and query directories exist."""
    QUERY_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def to_string(value: Optional[rdflib.term.Node]) -> str:
    """Convert RDFLib node to plain string."""
    if value is None:
        return ""
    return str(value)


def make_anchor(iri: str) -> str:
    """Extract fragment or terminal path component for Widoco link construction."""
    if "#" in iri:
        return iri.split("#")[-1]
    return iri.rstrip("/").split("/")[-1]


def normalize_relation(relation: str) -> str:
    """Simplify relation identifiers for display."""
    mapping = {
        "skos:broader": "broader",
        "skos:narrower": "narrower",
        "rdfs:subClassOf": "subClassOf",
    }
    return mapping.get(relation, relation)


def process_results(
    rows: Iterable[Dict[str, Optional[rdflib.term.Node]]],
    widoco_base_url: str,
    query_checksum: str,
    source_version: str,
    source_timestamp: str,
) -> List[Dict[str, str]]:
    """Aggregate SPARQL results into deterministic CSV rows."""
    aggregated: Dict[str, Dict[str, object]] = {}

    for row in rows:
        term_iri = to_string(row.get("term"))
        if not term_iri:
            continue

        entry = aggregated.setdefault(
            term_iri,
            {
                "term_name": to_string(row.get("termLabel")) or make_anchor(term_iri),
                "definition": "",
                "definition_source_text": "",
                "definition_source_link": "",
                "related": set(),
                "canonical_uri": term_iri,
                "widoco_link": widoco_base_url + make_anchor(term_iri),
                "source_version": source_version,
                "source_timestamp": source_timestamp,
                "query_checksum": query_checksum,
            },
        )

        definition = to_string(row.get("definition"))
        if definition and not entry["definition"]:
            entry["definition"] = definition

        # Prefer text citation (iao:0000119) over link (dcterms:source)
        definition_source_text = to_string(row.get("definitionSourceText"))
        if definition_source_text and not entry["definition_source_text"]:
            entry["definition_source_text"] = definition_source_text

        definition_source_link = to_string(row.get("definitionSourceLink"))
        if definition_source_link and not entry["definition_source_link"]:
            entry["definition_source_link"] = definition_source_link

        related_iri = to_string(row.get("related"))
        if related_iri:
            related_label = to_string(row.get("relatedLabel")) or make_anchor(related_iri)
            relation = normalize_relation(to_string(row.get("relation")))
            entry["related"].add((related_label, relation, related_iri))

    rows_out: List[Dict[str, str]] = []
    for entry in aggregated.values():
        relations = sorted(
            entry["related"],
            key=lambda triple: (triple[0].lower(), triple[2]),
        )
        related_terms = [
            f"{label} ({relation}) [{iri}]" for label, relation, iri in relations
        ]

        # Prefer text citation, fall back to link if no text
        definition_source = entry["definition_source_text"] or entry["definition_source_link"] or ""
        
        rows_out.append(
            {
                "term_name": entry["term_name"],
                "definition": entry["definition"],
                "definition_source": definition_source,
                "definition_source_text": entry["definition_source_text"],
                "definition_source_link": entry["definition_source_link"],
                "related_terms": "; ".join(related_terms),
                "canonical_uri": entry["canonical_uri"],
                "widoco_link": entry["widoco_link"],
                "source_version": entry["source_version"],
                "source_timestamp": entry["source_timestamp"],
                "query_checksum": entry["query_checksum"],
            }
        )

    rows_out.sort(key=lambda row: (row["term_name"].lower(), row["canonical_uri"]))
    return rows_out


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    """Write rows to CSV."""
    fieldnames = [
        "term_name",
        "definition",
        "definition_source",
        "definition_source_text",
        "definition_source_link",
        "related_terms",
        "canonical_uri",
        "widoco_link",
        "source_version",
        "source_timestamp",
        "query_checksum",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_meta(path: Path, theme: Theme, rows: List[Dict[str, str]]) -> None:
    """Persist metadata summary alongside CSV output."""
    payload = {
        "theme": theme.id,
        "label": theme.label,
        "row_count": len(rows),
        "source_version": rows[0]["source_version"] if rows else "",
        "source_timestamp": rows[0]["source_timestamp"] if rows else "",
        "query_checksum": rows[0]["query_checksum"] if rows else "",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(ONTOLOGY_PATH),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_query_file(path: Path, query: str) -> None:
    """Write the SPARQL query to the configured file."""
    header = "# Auto-generated by scripts/extract-term-tables.py; do not edit manually.\n\n"
    with path.open("w", encoding="utf-8") as handle:
        handle.write(header)
        handle.write(query)
        handle.write("\n")


def main() -> None:
    ensure_directories()
    widoco_base_url, themes = read_config()

    graph = rdflib.Graph()
    if graph.parse(str(ONTOLOGY_PATH)) is None:
        raise RuntimeError(f"Failed to parse ontology at {ONTOLOGY_PATH}")

    source_version = get_repo_commit(ROOT)
    source_timestamp = datetime.now(timezone.utc).isoformat()

    for theme in themes:
        query_sections: List[tuple[str, str]] = []
        raw_rows: List[Dict[str, Optional[rdflib.term.Node]]] = []

        scheme_query = build_schemes_query(theme)
        if scheme_query:
            query_sections.append(("# Scheme terms", scheme_query))
            raw_rows.extend(list(graph.query(scheme_query)))

        class_query = build_classes_query(theme)
        if class_query:
            query_sections.append(("# Class terms", class_query))
            raw_rows.extend(list(graph.query(class_query)))

        if not query_sections:
            print(f"Skipping theme '{theme.id}' (no schemes or classes defined).")
            continue

        combined_query = "\n\n".join(
            f"{label}\n{query.strip()}" for label, query in query_sections
        )
        checksum = hashlib.sha256(combined_query.encode("utf-8")).hexdigest()
        write_query_file(theme.query_path, combined_query)

        processed_rows = process_results(
            raw_rows,
            widoco_base_url=widoco_base_url,
            query_checksum=checksum,
            source_version=source_version,
            source_timestamp=source_timestamp,
        )

        write_csv(theme.output_csv_path, processed_rows)
        write_meta(theme.output_meta_path, theme, processed_rows)

        print(
            f"Wrote {len(processed_rows)} rows to {theme.output_csv_path.relative_to(ROOT)}"
        )


if __name__ == "__main__":
    main()
