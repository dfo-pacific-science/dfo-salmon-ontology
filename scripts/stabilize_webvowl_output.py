#!/usr/bin/env python3
"""Keep WebVOWL ontology.json byte-stable across no-op reruns.

WIDOCO's bundled OWL2VOWL step emits `docs/webvowl/data/ontology.json` with
nondeterministic ids and ordering even when the merged ontology input is
identical. For repeated runs against the same ontology input, keep the existing
tracked bytes instead of churning the generated JSON.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to generated ontology.json")
    parser.add_argument(
        "--baseline",
        required=True,
        help="Copy of ontology.json from before the WIDOCO run",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Deterministic merged ontology input consumed by WIDOCO",
    )
    parser.add_argument(
        "--stamp",
        required=True,
        help="Path to the persisted input/version fingerprint file",
    )
    parser.add_argument(
        "--generator",
        default="",
        help="Optional generator tag (for example widoco-1.4.25)",
    )
    return parser.parse_args()


def sha256_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stamp_value(source: Path, generator: str) -> str:
    source_hash = sha256_text(source)
    if generator:
        return f"{generator}:{source_hash}\n"
    return f"{source_hash}\n"


def main() -> int:
    args = parse_args()
    output_path = Path(args.path)
    baseline_path = Path(args.baseline)
    source_path = Path(args.source)
    stamp_path = Path(args.stamp)

    current_stamp = stamp_value(source_path, args.generator)
    previous_stamp = stamp_path.read_text(encoding="utf-8") if stamp_path.exists() else None

    if baseline_path.exists() and previous_stamp == current_stamp:
        baseline_bytes = baseline_path.read_bytes()
        if output_path.read_bytes() != baseline_bytes:
            output_path.write_bytes(baseline_bytes)

    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    stamp_path.write_text(current_stamp, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
