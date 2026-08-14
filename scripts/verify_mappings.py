#!/usr/bin/env python3
"""Structural checks for mappings/gcdfo-to-smn.sssom.tsv (stdlib only, CI-fatal).

Deep validation is run out-of-band with sssom-py
(`uv run --prerelease=allow --with "sssom==0.4.21" -- sssom validate -V
JsonSchema mappings/gcdfo-to-smn.sssom.tsv`) and with metasalmon's
`read_sssom_mapping_set()`, both of which accepted this file when it was
authored. This CI check keeps the byte and structure contract from decaying
without adding heavy dependencies to the workflow:

- UTF-8, no BOM, LF-only line endings, trailing newline
- required metadata fields present (the superset metasalmon requires)
- fixed column set; every row fully populated
- subject/predicate/object rows unique
- every CURIE prefix used is declared in the curie_map
- predicates limited to the reviewed tier vocabulary
"""

import csv
import io
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "mappings" / "gcdfo-to-smn.sssom.tsv"
REQUIRED_METADATA = [
    "curie_map:",
    "mapping_set_id:",
    "mapping_set_description:",
    "license:",
    "mapping_set_version:",
    "subject_source:",
    "subject_source_version:",
    "object_source:",
    "object_source_version:",
    "mapping_date:",
    "sssom_version:",
]
COLUMNS = [
    "subject_id",
    "subject_label",
    "predicate_id",
    "object_id",
    "object_label",
    "mapping_justification",
    "mapping_date",
    "comment",
]
ALLOWED_PREDICATES = {"skos:exactMatch", "skos:closeMatch", "skos:relatedMatch",
                      "skos:broadMatch", "skos:narrowMatch"}


def main() -> None:
    failures = []
    raw = PATH.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        failures.append("file starts with a UTF-8 BOM")
    if b"\r" in raw:
        failures.append("file contains CR characters (must be LF-only)")
    if not raw.endswith(b"\n"):
        failures.append("file lacks a trailing newline")

    text = raw.decode("utf-8")
    meta = [l for l in text.splitlines() if l.startswith("# ")]
    joined = "\n".join(meta)
    for field in REQUIRED_METADATA:
        if field not in joined:
            failures.append(f"metadata missing required field: {field}")

    prefixes = set()
    in_map = False
    for line in meta:
        if line.startswith("# curie_map:"):
            in_map = True
            continue
        if in_map:
            stripped = line[2:]
            if stripped.startswith("  ") and ":" in stripped:
                prefixes.add(stripped.strip().split(":")[0])
            else:
                in_map = False

    table = [l for l in text.splitlines() if not l.startswith("#")]
    reader = csv.reader(io.StringIO("\n".join(table)), delimiter="\t")
    header = next(reader)
    if header != COLUMNS:
        failures.append(f"column set mismatch: {header}")

    seen = set()
    for i, row in enumerate(reader, start=2):
        if len(row) != len(COLUMNS):
            failures.append(f"row {i}: expected {len(COLUMNS)} fields, got {len(row)}")
            continue
        rec = dict(zip(COLUMNS, row))
        if not all(rec[c] for c in COLUMNS):
            failures.append(f"row {i}: empty field(s)")
        key = (rec["subject_id"], rec["predicate_id"], rec["object_id"])
        if key in seen:
            failures.append(f"row {i}: duplicate mapping {key}")
        seen.add(key)
        if rec["predicate_id"] not in ALLOWED_PREDICATES:
            failures.append(f"row {i}: predicate {rec['predicate_id']} outside the reviewed set")
        for value in (rec["subject_id"], rec["object_id"], rec["predicate_id"],
                      rec["mapping_justification"]):
            prefix = value.split(":", 1)[0]
            if prefix not in prefixes:
                failures.append(f"row {i}: prefix '{prefix}' not in curie_map ({value})")

    if failures:
        for failure in failures:
            print(failure)
        raise SystemExit(1)
    print(f"Mapping set verified: {len(seen)} unique rows, prefixes complete, "
          "byte contract holds.")


if __name__ == "__main__":
    main()
