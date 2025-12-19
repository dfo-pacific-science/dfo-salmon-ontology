"""
Generate themed ontology term tables and matching SPARQL query files.

This script reads theme definitions from scripts/config/themes.yml, builds SPARQL
queries for each theme based on gcdfo:theme annotations, writes the queries to
scripts/sparql/, executes them against ontology/dfo-salmon.ttl using RDFLib, and
exports deterministically ordered CSV + metadata files under
release/artifacts/term-tables/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import textwrap
import os
import contextlib
import io
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import rdflib
import yaml


# Path resolution: get the repository root (two levels up from this script)
ROOT = Path(__file__).resolve().parent.parent
# Path to the main ontology file in Turtle format (canonical source)
ONTOLOGY_PATH = ROOT / "ontology" / "dfo-salmon.ttl"
# Path to YAML configuration file defining themes and their extraction criteria
CONFIG_PATH = ROOT / "scripts" / "config" / "themes.yml"
# Directory where generated SPARQL queries will be written
QUERY_DIR = ROOT / "scripts" / "sparql"
# Directory where CSV outputs and metadata files will be written
OUTPUT_DIR = ROOT / "release" / "artifacts" / "term-tables"
# IRI for IAO definition property (IAO_0000115 = "definition")
IAO_DEFINITION_IRI = rdflib.URIRef("http://purl.obolibrary.org/obo/IAO_0000115")

# SPARQL namespace prefixes used across all generated queries
# These define shortcuts for common RDF vocabularies:
# - gcdfo: DFO Salmon Ontology namespace
# - skos: Simple Knowledge Organization System (concepts, schemes, labels)
# - rdfs: RDF Schema (classes, labels, comments, subClassOf)
# - owl: Web Ontology Language (classes, properties)
# - dcterms: Dublin Core Terms (source citations)
COMMON_PREFIXES = """PREFIX gcdfo: <https://w3id.org/gcdfo/salmon#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
"""

# Reusable SPARQL OPTIONAL blocks for extracting term metadata
# This pattern is used in theme-based queries to ensure
# consistent extraction of labels, definitions, sources, and relationships
COMMON_OPTIONALS = textwrap.dedent(
    """\
# Extract term label: prefer skos:prefLabel, fall back to rdfs:label, then use IRI fragment
# Language filter ensures we only get English labels or untyped literals
OPTIONAL {
  ?term skos:prefLabel ?prefLabelRaw .
  FILTER(LANG(?prefLabelRaw) = "" || LANGMATCHES(LANG(?prefLabelRaw), "en"))
}
OPTIONAL {
  ?term rdfs:label ?rdfsLabelRaw .
  FILTER(LANG(?rdfsLabelRaw) = "" || LANGMATCHES(LANG(?rdfsLabelRaw), "en"))
}
# COALESCE returns first non-null value: prefLabel > rdfs:label > IRI fragment
BIND(COALESCE(?prefLabelRaw, ?rdfsLabelRaw, STRAFTER(STR(?term), "#")) AS ?termLabel) .

# Extract definition: check multiple properties in priority order
# 1. skos:definition (SKOS standard)
# 2. rdfs:comment (RDF Schema standard)
# 3. IAO_0000115 (Information Artifact Ontology definition property)
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
# Use first available definition source
BIND(COALESCE(?defSKOS, ?defRDFS, ?defIAO) AS ?definition) .

# Extract definition source: text citation (IAO_0000119) or link (dcterms:source)
# IAO_0000119 = "has definition source" (text citation)
OPTIONAL {
  ?term <http://purl.obolibrary.org/obo/IAO_0000119> ?definitionSourceText .
  FILTER(LANG(?definitionSourceText) = "" || LANGMATCHES(LANG(?definitionSourceText), "en"))
}
# dcterms:source = Dublin Core source property (typically a URL)
OPTIONAL {
  ?term dcterms:source ?definitionSourceLink .
}

# Extract related terms via four relationship types (UNION creates one result per relationship)
# This allows a term to have multiple related terms, each with its relationship type
OPTIONAL {
  # Broader term (parent concept in SKOS hierarchy)
  {
    ?term skos:broader ?related .
    BIND("skos:broader" AS ?relation) .
  }
  UNION
  # Narrower term (child concept in SKOS hierarchy)
  {
    ?term skos:narrower ?related .
    BIND("skos:narrower" AS ?relation) .
  }
  UNION
  # Subclass relationship (OWL/RDFS class hierarchy)
  {
    ?term rdfs:subClassOf ?related .
    BIND("rdfs:subClassOf" AS ?relation) .
  }
  UNION
  # In scheme relationship (SKOS concept to scheme)
  {
    ?term skos:inScheme ?related .
    BIND("skos:inScheme" AS ?relation) .
  }
  # Extract label for the related term (same pattern as term label extraction)
  OPTIONAL {
    ?related skos:prefLabel ?relatedPref .
    FILTER(LANG(?relatedPref) = "" || LANGMATCHES(LANG(?relatedPref), "en"))
  }
  OPTIONAL {
    ?related rdfs:label ?relatedLabelRaw .
    FILTER(LANG(?relatedLabelRaw) = "" || LANGMATCHES(LANG(?relatedLabelRaw), "en"))
  }
# Use first available label or fall back to IRI fragment
BIND(COALESCE(?relatedPref, ?relatedLabelRaw, STRAFTER(STR(?related), "#")) AS ?relatedLabel) .
}
"""
)

# SPARQL ORDER BY clause for deterministic sorting of query results
# Sort order:
# 1. Term label (case-insensitive) - primary sort for human readability
# 2. Term IRI (string) - secondary sort for consistent ordering when labels are identical
# 3. Related term label (case-insensitive) - tertiary sort for related terms
# 4. Related term IRI (string) - final sort for related terms
# This ensures reproducible output order across runs
ORDER_BY_CLAUSE = (
    "ORDER BY LCASE(?termLabel) STR(?term) "
    'LCASE(COALESCE(?relatedLabel, "")) STR(COALESCE(?related, ""))'
)


class Theme:
    """
    Definition for a themed extraction based on gcdfo:theme annotations.

    A theme groups related ontology terms that have been annotated with
    the same gcdfo:theme value. This captures both SKOS concepts and OWL
    classes automatically.
    """

    def __init__(
        self,
        *,
        id: str,
        label: str,
        theme_iri: str,
        query_file: str,
        output_csv: str,
    ) -> None:
        """
        Initialize a theme configuration.

        Args:
            id: Unique identifier for the theme (used in metadata)
            label: Human-readable theme name
            theme_iri: IRI of the theme (value of gcdfo:theme property)
            query_file: Filename for the generated SPARQL query (relative to QUERY_DIR)
            output_csv: Filename for the generated CSV (relative to OUTPUT_DIR)
        """
        self.id = id
        self.label = label
        self.theme_iri = theme_iri
        self.query_file = query_file
        self.output_csv = output_csv

    @property
    def query_path(self) -> Path:
        """Return the full path where the SPARQL query file will be written."""
        return QUERY_DIR / self.query_file

    @property
    def output_csv_path(self) -> Path:
        """Return the full path where the CSV output file will be written."""
        return OUTPUT_DIR / self.output_csv

    @property
    def output_meta_path(self) -> Path:
        """Return the full path for the metadata JSON file (same name as CSV, .meta.json extension)."""
        return self.output_csv_path.with_suffix(".meta.json")


def read_config() -> tuple[str, List[Theme]]:
    """
    Load YAML configuration and return widoco base url plus themes.

    Reads the themes.yml configuration file and constructs Theme objects
    for each theme definition. Validates that required fields are present.

    Returns:
        Tuple of (widoco_base_url, themes_list)

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        ValueError: If widoco_base_url is missing or no themes are defined
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing theme configuration: {CONFIG_PATH}")

    # Load YAML configuration (safe_load prevents code execution)
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)

    # Extract widoco_base_url: used to construct links to ontology documentation
    widoco_base_url = raw.get("widoco_base_url")
    if not widoco_base_url:
        raise ValueError("Theme configuration must set widoco_base_url.")

    # Build Theme objects from YAML entries
    # Each theme entry must have: id, label, theme_iri, query_file, output_csv
    themes = [
        Theme(
            id=entry["id"],
            label=entry["label"],
            theme_iri=entry["theme_iri"],
            query_file=entry["query_file"],
            output_csv=entry["output_csv"],
        )
        for entry in raw.get(
            "themes", []
        )  # Default to empty list if themes key missing
    ]

    if not themes:
        raise ValueError("No themes configured; update scripts/config/themes.yml.")

    return widoco_base_url, themes


def build_theme_query(theme: Theme) -> str:
    """
    Construct a SPARQL query for entities with a specific gcdfo:theme annotation.

    Builds a query that selects all entities (both SKOS concepts and OWL classes)
    that have been annotated with the specified theme IRI using the gcdfo:theme property.

    Args:
        theme: Theme configuration with theme_iri

    Returns:
        Complete SPARQL query string
    """
    # Indent the common optional blocks to match WHERE clause indentation
    optional_block = textwrap.indent(COMMON_OPTIONALS, "  ")

    # Construct the full SPARQL query:
    # - SELECT DISTINCT ensures no duplicate rows
    # - WHERE clause filters by gcdfo:theme annotation
    # - No type restrictions - captures both SKOS concepts and OWL classes
    # - COMMON_OPTIONALS extracts labels, definitions, sources, and relationships
    # - ORDER_BY_CLAUSE ensures deterministic output ordering
    return (
        f"{COMMON_PREFIXES}\n"
        "SELECT DISTINCT ?term ?termLabel ?definition ?definitionSourceText ?definitionSourceLink ?related ?relatedLabel ?relation\n"
        "WHERE {\n"
        f"  # Filter to entities with the specific theme annotation\n"
        f"  ?term gcdfo:theme <{theme.theme_iri}> .\n"
        f"  \n"
        f"  # Note: We don't restrict by type - this captures both SKOS concepts and OWL classes\n"
        f"  # that have been annotated with this theme\n"
        f"  \n"
        f"{optional_block}\n"
        "}\n"
        f"{ORDER_BY_CLAUSE}"
    )


def get_all_themes_query() -> str:
    """
    Construct a SPARQL query to discover all themes in the ontology.

    This query finds all unique theme IRIs that are used as values of the
    gcdfo:theme property, along with their labels if available.

    Returns:
        SPARQL query string to find all themes
    """
    return (
        f"{COMMON_PREFIXES}\n"
        "SELECT DISTINCT ?theme ?themeLabel\n"
        "WHERE {\n"
        "  # Find all entities that have a theme annotation\n"
        "  ?entity gcdfo:theme ?theme .\n"
        "  \n"
        "  # Get theme labels if available\n"
        "  OPTIONAL {\n"
        "    ?theme skos:prefLabel ?themePrefLabel .\n"
        '    FILTER(LANG(?themePrefLabel) = "" || LANGMATCHES(LANG(?themePrefLabel), "en"))\n'
        "  }\n"
        "  OPTIONAL {\n"
        "    ?theme rdfs:label ?themeRdfsLabel .\n"
        '    FILTER(LANG(?themeRdfsLabel) = "" || LANGMATCHES(LANG(?themeRdfsLabel), "en"))\n'
        "  }\n"
        '  BIND(COALESCE(?themePrefLabel, ?themeRdfsLabel, STRAFTER(STR(?theme), "#")) AS ?themeLabel) .\n'
        "}\n"
        "ORDER BY ?themeLabel"
    )


def get_repo_commit(root: Path) -> str:
    """
    Return current git commit SHA for the repository.

    Executes 'git rev-parse HEAD' to get the full commit hash of the current HEAD.
    This is used to track which version of the ontology was used to generate
    the term tables, enabling reproducibility and traceability.

    Args:
        root: Repository root directory path

    Returns:
        Full git commit SHA (40-character hex string)

    Raises:
        RuntimeError: If git command fails or git is not available
    """
    try:
        # Execute git rev-parse HEAD to get current commit SHA
        # text=True ensures output is returned as string, not bytes
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()  # Remove trailing newline
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        # Handle cases where git is not installed or not a git repository
        raise RuntimeError("Unable to resolve git commit SHA") from exc
    return sha


def ensure_directories() -> None:
    """
    Ensure output and query directories exist.

    Creates the directories if they don't exist, including any necessary
    parent directories. Does not raise an error if directories already exist.
    """
    # parents=True creates parent directories if needed
    # exist_ok=True prevents error if directory already exists
    QUERY_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def to_string(value: Optional[rdflib.term.Node]) -> str:
    """
    Convert RDFLib node to plain string.

    Safely converts RDFLib node objects (URIRef, Literal, BNode, etc.)
    to plain Python strings. Returns empty string for None values.

    Args:
        value: RDFLib node or None

    Returns:
        String representation of the node, or empty string if None
    """
    if value is None:
        return ""
    # RDFLib nodes have __str__ methods that return their string representation
    return str(value)


def make_anchor(iri: str) -> str:
    """
    Extract fragment or terminal path component for Widoco link construction.

    Extracts the anchor/fragment identifier from an IRI for use in constructing
    links to Widoco-generated ontology documentation. Handles two IRI patterns:
    - Hash-based IRIs (e.g., "http://example.org/ontology#Term" -> "Term")
    - Slash-based IRIs (e.g., "http://example.org/ontology/Term" -> "Term")

    Args:
        iri: Full IRI string

    Returns:
        Fragment identifier or last path component
    """
    # Hash-based IRIs: extract everything after the #
    if "#" in iri:
        return iri.split("#")[-1]
    # Slash-based IRIs: remove trailing slash, then extract last path component
    return iri.rstrip("/").split("/")[-1]


def normalize_relation(relation: str) -> str:
    """
    Simplify relation identifiers for display.

    Converts SPARQL relation identifiers (with namespace prefixes) to
    simplified display names for CSV output. Removes namespace prefixes
    to make the output more readable.

    Args:
        relation: SPARQL relation identifier (e.g., "skos:broader")

    Returns:
        Simplified relation name (e.g., "broader"), or original if not mapped
    """
    # Map SPARQL relation identifiers to simplified display names
    mapping = {
        "skos:broader": "broader",
        "skos:narrower": "narrower",
        "rdfs:subClassOf": "subClassOf",
        "skos:inScheme": "inScheme",
    }
    # Return mapped value if found, otherwise return original
    return mapping.get(relation, relation)


def process_results(
    rows: Iterable[Dict[str, Optional[rdflib.term.Node]]],
    widoco_base_url: str,
    query_checksum: str,
    source_version: str,
    source_timestamp: str,
) -> List[Dict[str, str]]:
    """
    Aggregate SPARQL results into deterministic CSV rows.

    Processes raw SPARQL query results and aggregates them by term IRI.
    Since SPARQL queries can return multiple rows per term (one per related term),
    this function consolidates them into a single row per term with all related
    terms combined into a semicolon-separated list.

    Args:
        rows: Iterable of SPARQL result rows (each row is a dict mapping variable names to RDFLib nodes)
        widoco_base_url: Base URL for Widoco documentation links
        query_checksum: SHA-256 hash of the SPARQL query (for reproducibility tracking)
        source_version: Git commit SHA of the ontology version used
        source_timestamp: ISO timestamp when extraction was performed

    Returns:
        List of dictionaries, one per unique term, ready for CSV export
    """
    # Dictionary keyed by term IRI to aggregate multiple SPARQL rows per term
    aggregated: Dict[str, Dict[str, object]] = {}

    # First pass: aggregate all SPARQL rows by term IRI
    for row in rows:
        term_iri = to_string(row.get("term"))
        # Skip rows without a term IRI (shouldn't happen, but defensive)
        if not term_iri:
            continue

        # Get or create entry for this term IRI
        # setdefault returns existing entry if present, otherwise creates new one
        entry = aggregated.setdefault(
            term_iri,
            {
                # Term name: prefer label from query, fall back to IRI fragment
                "term_name": to_string(row.get("termLabel")) or make_anchor(term_iri),
                "definition": "",  # Will be populated if found in any row
                "definition_source_text": "",  # IAO_0000119 property
                "definition_source_link": "",  # dcterms:source property
                "related": set(),  # Set of tuples: (label, relation, iri) for related terms
                "canonical_uri": term_iri,  # Full IRI of the term
                "widoco_link": widoco_base_url
                + make_anchor(term_iri),  # Link to documentation
                "source_version": source_version,  # Git commit SHA
                "source_timestamp": source_timestamp,  # When extraction ran
                "query_checksum": query_checksum,  # Hash of query for reproducibility
            },
        )

        # Update definition if found (only set once, prefer first non-empty value)
        definition = to_string(row.get("definition"))
        if definition and not entry["definition"]:
            entry["definition"] = definition

        # Prefer text citation (iao:0000119) over link (dcterms:source)
        # Text citations are more informative than bare links
        definition_source_text = to_string(row.get("definitionSourceText"))
        if definition_source_text and not entry["definition_source_text"]:
            entry["definition_source_text"] = definition_source_text

        definition_source_link = to_string(row.get("definitionSourceLink"))
        if definition_source_link and not entry["definition_source_link"]:
            entry["definition_source_link"] = definition_source_link

        # Collect related terms: each SPARQL row may have a different related term
        # Store as tuples in a set to avoid duplicates
        related_iri = to_string(row.get("related"))
        if related_iri:
            # Get label for related term, fall back to IRI fragment if no label
            related_label = to_string(row.get("relatedLabel")) or make_anchor(
                related_iri
            )
            # Normalize relation identifier (e.g., "skos:broader" -> "broader")
            relation = normalize_relation(to_string(row.get("relation")))
            # Store as tuple: (label, relation_type, iri)
            entry["related"].add((related_label, relation, related_iri))

    # Second pass: convert aggregated entries to CSV-ready format
    rows_out: List[Dict[str, str]] = []
    for entry in aggregated.values():
        # Sort related terms by label (case-insensitive) then by IRI for deterministic ordering
        relations = sorted(
            entry["related"],
            key=lambda triple: (
                triple[0].lower(),
                triple[2],
            ),  # Sort by label, then IRI
        )
        # Format related terms as: "Label (relation) [IRI]"
        related_terms = [
            f"{label} ({relation}) [{iri}]" for label, relation, iri in relations
        ]

        # Prefer text citation, fall back to link if no text
        # This provides a single "definition_source" field for convenience
        definition_source = (
            entry["definition_source_text"] or entry["definition_source_link"] or ""
        )

        # Build final CSV row with all fields as strings
        rows_out.append(
            {
                "term_name": entry["term_name"],
                "definition": entry["definition"],
                "definition_source": definition_source,  # Convenience field (text or link)
                "definition_source_text": entry[
                    "definition_source_text"
                ],  # Original text citation
                "definition_source_link": entry[
                    "definition_source_link"
                ],  # Original link
                "related_terms": "; ".join(related_terms),  # Semicolon-separated list
                "canonical_uri": entry["canonical_uri"],
                "widoco_link": entry["widoco_link"],
                "source_version": entry["source_version"],
                "source_timestamp": entry["source_timestamp"],
                "query_checksum": entry["query_checksum"],
            }
        )

    # Sort final rows by term name (case-insensitive) then by IRI for deterministic output
    rows_out.sort(key=lambda row: (row["term_name"].lower(), row["canonical_uri"]))
    return rows_out


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    """
    Write rows to CSV file.

    Writes the processed term data to a CSV file with UTF-8 encoding.
    Uses csv.DictWriter to ensure consistent column ordering and proper
    CSV escaping of special characters.

    Args:
        path: Output file path for the CSV
        rows: List of dictionaries, each representing one term row
    """
    # Define column order explicitly for consistent CSV structure
    fieldnames = [
        "term_name",
        "definition",
        "definition_source",  # Convenience field (text or link)
        "definition_source_text",  # Original text citation
        "definition_source_link",  # Original link
        "related_terms",
        "canonical_uri",
        "widoco_link",
        "source_version",
        "source_timestamp",
        "query_checksum",
    ]
    # newline="" prevents extra blank lines on Windows
    # encoding="utf-8" ensures proper handling of Unicode characters
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()  # Write column headers
        for row in rows:
            writer.writerow(row)  # Write each term row


def write_meta(path: Path, theme: Theme, rows: List[Dict[str, str]]) -> None:
    """
    Persist metadata summary alongside CSV output.

    Writes a JSON metadata file containing information about the extraction:
    theme details, row count, source version/timestamp, query checksum, etc.
    This enables tracking of provenance and reproducibility.

    Args:
        path: Output file path for the metadata JSON
        theme: Theme configuration used for this extraction
        rows: List of processed term rows (used to extract metadata values)
    """
    payload = {
        "theme": theme.id,  # Theme identifier
        "label": theme.label,  # Human-readable theme name
        "theme_iri": theme.theme_iri,  # IRI of the theme used for filtering
        "row_count": len(rows),  # Number of terms extracted
        # Extract metadata from first row (all rows have same values for these fields)
        "source_version": rows[0]["source_version"] if rows else "",  # Git commit SHA
        "source_timestamp": (
            rows[0]["source_timestamp"] if rows else ""
        ),  # Extraction timestamp
        "query_checksum": rows[0]["query_checksum"] if rows else "",  # Query hash
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),  # When metadata was written
        "source_file": str(ONTOLOGY_PATH),  # Path to source ontology file
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)  # Pretty-print JSON with 2-space indent


def write_query_file(path: Path, query: str) -> None:
    """
    Write the SPARQL query to the configured file.

    Persists the generated SPARQL query to a file for inspection and debugging.
    The file includes a header warning that it's auto-generated and should not
    be edited manually (since it will be overwritten on next run).

    Args:
        path: Output file path for the SPARQL query
        query: Complete SPARQL query string to write
    """
    # Header warning that file is auto-generated
    header = (
        "# Auto-generated by scripts/extract-term-tables.py; do not edit manually.\n\n"
    )
    with path.open("w", encoding="utf-8") as handle:
        handle.write(header)
        handle.write(query)
        handle.write("\n")  # Ensure file ends with newline


def discover_themes(graph: rdflib.Graph) -> List[tuple[str, str]]:
    """
    Discover all themes used in the ontology.

    Executes a SPARQL query to find all unique values of the gcdfo:theme property
    along with their labels.

    Args:
        graph: Parsed RDF graph of the ontology

    Returns:
        List of tuples (theme_iri, theme_label)
    """
    query = get_all_themes_query()
    results = graph.query(query)

    themes = []
    for row in results:
        theme_iri = to_string(row.get("theme"))
        theme_label = to_string(row.get("themeLabel")) or make_anchor(theme_iri)
        if theme_iri:
            themes.append((theme_iri, theme_label))

    return themes


def parse_graph_safely(graph: rdflib.Graph, path: Path) -> None:
    """
    Parse a TTL file while suppressing known benign warnings from the underlying parser.

    Some macOS environments emit "unhandled Platform key FamilyDisplayName" on stderr when
    parsing TTL. We suppress that specific line but surface any other stderr output.
    """
    with tempfile.TemporaryFile(mode="w+b") as tmp:
        tmp_fd = tmp.fileno()
        saved_fd = os.dup(2)
        try:
            os.dup2(tmp_fd, 2)  # redirect C-level stderr to tmp
            result = graph.parse(str(path))
        finally:
            os.dup2(saved_fd, 2)
            os.close(saved_fd)

        tmp.seek(0)
        stderr_out = tmp.read().decode(errors="ignore")

    if stderr_out:
        filtered = [
            line
            for line in stderr_out.splitlines()
            if "unhandled Platform key FamilyDisplayName" not in line.strip()
        ]
        if filtered:
            sys.stderr.write("\n".join(filtered) + "\n")
    return result


@contextlib.contextmanager
def filter_stderr_lines(skip_substrings: list[str]):
    """
    Capture stderr during a block and re-emit lines that do not contain skip strings.
    Useful for suppressing noisy platform warnings while preserving other output.
    """
    with tempfile.TemporaryFile(mode="w+b") as tmp:
        tmp_fd = tmp.fileno()
        saved_fd = os.dup(2)
        try:
            os.dup2(tmp_fd, 2)
            yield
        finally:
            os.dup2(saved_fd, 2)
            os.close(saved_fd)
            tmp.seek(0)
            stderr_out = tmp.read().decode(errors="ignore")
            if stderr_out:
                keep = []
                for line in stderr_out.splitlines():
                    if any(substr in line for substr in skip_substrings):
                        continue
                    keep.append(line)
                if keep:
                    sys.stderr.write("\n".join(keep) + "\n")

def main() -> None:
    """
    Main execution function (stderr-filtered to drop noisy platform warnings).
    """
    with filter_stderr_lines(["unhandled Platform key FamilyDisplayName"]):
        _run_main()


def _run_main() -> None:
    """
    Main execution logic.

    Orchestrates the entire extraction process:
    1. Ensures output directories exist
    2. Loads theme configuration
    3. Parses the ontology file
    4. Optionally discovers themes in the ontology
    5. For each configured theme:
       a. Builds and executes SPARQL query based on gcdfo:theme annotation
       b. Aggregates and processes results
       c. Writes CSV output and metadata files
       d. Writes generated SPARQL queries for inspection
    """
    # Ensure output directories exist before writing files
    ensure_directories()
    # Load theme configuration from YAML file
    widoco_base_url, themes = read_config()

    # Parse the ontology file into an RDFLib graph
    graph = rdflib.Graph()
    # parse() returns None on failure, raises exception on some errors
    if parse_graph_safely(graph, ONTOLOGY_PATH) is None:
        raise RuntimeError(f"Failed to parse ontology at {ONTOLOGY_PATH}")

    # Optional: Discover all themes in the ontology (useful for debugging/validation)
    print("\nDiscovering themes in the ontology...")
    discovered_themes = discover_themes(graph)
    if discovered_themes:
        print(f"Found {len(discovered_themes)} themes in the ontology:")
        for theme_iri, theme_label in discovered_themes:
            print(f"  - {theme_label}: {theme_iri}")
    else:
        print(
            "No themes found in the ontology (no entities with gcdfo:theme property)"
        )
    print()

    # Get source version information for provenance tracking
    source_version = get_repo_commit(ROOT)  # Git commit SHA
    source_timestamp = datetime.now(timezone.utc).isoformat()  # Current UTC time

    # Process each theme defined in the configuration
    for theme in themes:
        print(f"Processing theme: {theme.label}")

        # Build SPARQL query for this theme
        query = build_theme_query(theme)

        # Calculate SHA-256 hash of the query for reproducibility tracking
        checksum = hashlib.sha256(query.encode("utf-8")).hexdigest()

        # Write the query to file for inspection/debugging
        write_query_file(theme.query_path, query)

        # Execute query against the parsed graph
        raw_rows = list(graph.query(query))

        if not raw_rows:
            print(f"  No entities found with theme {theme.theme_iri}")
            # Still write empty CSV and metadata for consistency
            write_csv(theme.output_csv_path, [])
            write_meta(theme.output_meta_path, theme, [])
            continue

        # Process raw SPARQL results: aggregate by term, format for CSV
        processed_rows = process_results(
            raw_rows,
            widoco_base_url=widoco_base_url,
            query_checksum=checksum,
            source_version=source_version,
            source_timestamp=source_timestamp,
        )

        # Write outputs: CSV file with term data, JSON metadata file
        write_csv(theme.output_csv_path, processed_rows)
        write_meta(theme.output_meta_path, theme, processed_rows)

        # Print progress message with relative path for readability
        print(
            f"  Wrote {len(processed_rows)} rows to {theme.output_csv_path.relative_to(ROOT)}"
        )

    print("\nExtraction complete!")


if __name__ == "__main__":
    main()
