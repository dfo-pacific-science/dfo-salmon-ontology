#!/usr/bin/env python3
"""
Convert a Turtle (.ttl) ontology file into JSON-LD (.jsonld).

Why this exists:
- ROBOT v1.9.8 does not support writing JSON-LD via `robot convert` (it errors on
  the `.jsonld` extension).
- The project publishes `docs/gcdfo.jsonld`, so `make docs-refresh` needs a
  working JSON-LD generation path.

This script uses rdflib (provided by devenv) and writes a deterministic JSON-LD
file by:
- Sorting node objects by `@id`
- Sorting dictionary keys recursively
- Sorting list values recursively, except for JSON-LD `@list` payloads (order is
  significant there)
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any

from rdflib import Graph


def _sort_key(value: Any) -> tuple:
    if isinstance(value, dict):
        if "@id" in value:
            return ("id", str(value.get("@id")))
        if "@value" in value:
            return (
                "value",
                str(value.get("@value")),
                str(value.get("@language", "")),
                str(value.get("@type", "")),
            )
        return ("dict", json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
    return ("other", json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")))


def _normalize_json(value: Any, *, preserve_list_order: bool = False) -> Any:
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key in sorted(value.keys()):
            child = value[key]
            if key == "@list":
                normalized[key] = _normalize_json(child, preserve_list_order=True)
            else:
                normalized[key] = _normalize_json(child, preserve_list_order=False)
        return normalized

    if isinstance(value, list):
        normalized_items = [_normalize_json(item, preserve_list_order=preserve_list_order) for item in value]
        if preserve_list_order:
            return normalized_items
        return sorted(normalized_items, key=_sort_key)

    return value


def convert_ttl_to_jsonld(*, input_path: pathlib.Path, output_path: pathlib.Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input TTL file not found: {input_path}")

    graph = Graph()
    graph.parse(str(input_path), format="turtle")

    raw = graph.serialize(format="json-ld", auto_compact=False)
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    data = json.loads(raw)
    normalized = _normalize_json(data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Convert Turtle to JSON-LD deterministically.")
    parser.add_argument("input", type=pathlib.Path, help="Input Turtle file (e.g., ontology/dfo-salmon.ttl)")
    parser.add_argument("output", type=pathlib.Path, help="Output JSON-LD file (e.g., docs/gcdfo.jsonld)")
    args = parser.parse_args(argv)

    try:
        convert_ttl_to_jsonld(input_path=args.input, output_path=args.output)
    except Exception as exc:
        print(f"❌ JSON-LD conversion failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
