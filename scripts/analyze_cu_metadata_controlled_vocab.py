#!/usr/bin/env python3
"""
Analyze controlled vocabulary candidates in Metadata-Questionnaire CU metadata CSV
against existing DFO Salmon Ontology lexical terms.

Outputs:
- JSON: per-column values, frequencies, ontology matches, gaps
- CSV: flattened gap table
- Markdown: human-readable summary + modeling proposals

Usage:
  python3 scripts/analyze_cu_metadata_controlled_vocab.py \
    --csv /path/to/x_CU_Level_Metadata.csv \
    --ttl ontology/dfo-salmon.ttl \
    --outdir analysis/cu-metadata-controlled-vocab
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


LABEL_PREDICATES = {"rdfs:label", "skos:prefLabel", "skos:altLabel"}
SCHEME_PREDICATE = "skos:inScheme"


@dataclass
class OntTerm:
    iri: str
    labels: List[str]
    schemes: List[str]


def normalize_text(value: str) -> str:
    v = value.strip().lower()
    v = re.sub(r"[_\-/]+", " ", v)
    v = re.sub(r"[^a-z0-9 %]+", "", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v


def to_pascal(s: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", s)
    out = "".join(t.capitalize() for t in tokens if t)
    if not out:
        out = "Value"
    if out[0].isdigit():
        out = f"V{out}"
    return out


def parse_ttl_terms(ttl_path: Path) -> Dict[str, OntTerm]:
    """Very lightweight parser for the ontology's term blocks."""
    text = ttl_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    terms: Dict[str, OntTerm] = {}
    current_subject: Optional[str] = None
    current_lines: List[str] = []

    def flush_block(subject: Optional[str], block_lines: List[str]) -> None:
        if not subject:
            return
        block = "\n".join(block_lines)
        labels = []
        for pred in LABEL_PREDICATES:
            for m in re.finditer(rf"{re.escape(pred)}\s+\"([^\"]+)\"@en", block):
                labels.append(m.group(1).strip())
        schemes = [m.group(1).strip() for m in re.finditer(r"skos:inScheme\s+([^\s;]+)", block)]
        if labels:
            terms[subject] = OntTerm(iri=subject, labels=sorted(set(labels)), schemes=sorted(set(schemes)))

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        m_start = re.match(r"^([A-Za-z0-9_:.-]+)\s+a\s+", line)
        if m_start:
            flush_block(current_subject, current_lines)
            current_subject = m_start.group(1)
            current_lines = [line]
            if line.strip().endswith("."):
                flush_block(current_subject, current_lines)
                current_subject, current_lines = None, []
            continue

        if current_subject:
            current_lines.append(line)
            if line.strip().endswith("."):
                flush_block(current_subject, current_lines)
                current_subject, current_lines = None, []

    flush_block(current_subject, current_lines)
    return terms


def infer_categorical_columns(rows: List[Dict[str, str]], fieldnames: List[str], max_unique: int = 25, max_unique_ratio: float = 0.35) -> List[str]:
    cols: List[str] = []
    for col in fieldnames:
        values = [r.get(col, "").strip() for r in rows]
        non_empty = [v for v in values if v]
        if not non_empty:
            continue

        # Exclude obvious identifiers/free-text heavy columns
        if re.search(r"(_ID$|_Acro$|_Name$|_Notes$|_Description$|_References$|_Contact$|_Specific$|_Rationale$)", col):
            continue

        # Exclude very long narrative fields
        avg_len = sum(len(v) for v in non_empty) / len(non_empty)
        if avg_len > 35 or max(len(v) for v in non_empty) > 120:
            continue

        uniq = sorted(set(non_empty))
        u = len(uniq)
        ratio = u / max(len(non_empty), 1)

        # Identify likely numeric/parameter fields rather than controlled vocab labels
        numeric_like = sum(1 for v in non_empty if re.fullmatch(r"[-+]?\d+(\.\d+)?", v))
        alpha_like = sum(1 for v in non_empty if re.search(r"[A-Za-z]", v))
        numeric_ratio = numeric_like / len(non_empty)
        alpha_ratio = alpha_like / len(non_empty)

        if numeric_ratio > 0.7:
            continue
        if alpha_ratio < 0.5:
            continue

        if 2 <= u <= max_unique and ratio <= max_unique_ratio:
            cols.append(col)
    return cols


def build_lexical_index(terms: Dict[str, OntTerm]) -> Dict[str, List[Tuple[str, str, List[str]]]]:
    idx: Dict[str, List[Tuple[str, str, List[str]]]] = defaultdict(list)
    for iri, term in terms.items():
        for label in term.labels:
            norm = normalize_text(label)
            if norm:
                idx[norm].append((iri, label, term.schemes))
    return idx


def suggest_scheme_for_column(col: str) -> str:
    # heuristic proposal only
    if "Status" in col:
        return ":StatusScheme"
    if "Method" in col:
        return ":MethodScheme"
    if "Type" in col:
        return ":TypeScheme"
    if "Source" in col:
        return ":SourceScheme"
    if "Category" in col:
        return ":CategoryScheme"
    return f":{to_pascal(col)}Scheme"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, type=Path)
    ap.add_argument("--ttl", required=True, type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--max-unique", type=int, default=25)
    ap.add_argument("--max-unique-ratio", type=float, default=0.35)
    args = ap.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)

    with args.csv.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    terms = parse_ttl_terms(args.ttl)
    lex_idx = build_lexical_index(terms)
    categorical_cols = infer_categorical_columns(
        rows, fieldnames, max_unique=args.max_unique, max_unique_ratio=args.max_unique_ratio
    )

    analysis = {
        "metadata": {
            "csv": str(args.csv),
            "ttl": str(args.ttl),
            "row_count": len(rows),
            "column_count": len(fieldnames),
            "categorical_columns": len(categorical_cols),
            "ontology_terms_with_labels": len(terms),
        },
        "columns": [],
    }

    gap_rows = []
    global_missing_values = Counter()
    global_match_values = Counter()

    null_tokens = {"na", "n/a", "tbd", "", "none", "unknown", "not applicable", "?", "???"}

    for col in categorical_cols:
        vals = [r.get(col, "").strip() for r in rows]
        non_empty = [v for v in vals if v]
        freq = Counter(non_empty)
        values = sorted(freq.keys())

        matched = []
        missing = []
        placeholders = []

        for v in values:
            norm = normalize_text(v)
            if norm in null_tokens or norm in {"true", "false", "yes", "no", "pending"}:
                placeholders.append({"value": v, "count": freq[v]})
                continue
            if re.fullmatch(r"[-+]?\d+(\.\d+)?", v):
                placeholders.append({"value": v, "count": freq[v]})
                continue

            matches = lex_idx.get(norm, [])
            if matches:
                matched.append(
                    {
                        "value": v,
                        "count": freq[v],
                        "matches": [
                            {"iri": iri, "label": label, "schemes": schemes}
                            for iri, label, schemes in matches
                        ],
                    }
                )
                global_match_values[v] += freq[v]
            else:
                missing.append({"value": v, "count": freq[v]})
                global_missing_values[v] += freq[v]
                gap_rows.append(
                    {
                        "column": col,
                        "value": v,
                        "count": freq[v],
                        "proposed_term": to_pascal(v),
                        "proposed_scheme": suggest_scheme_for_column(col),
                    }
                )

        analysis["columns"].append(
            {
                "column": col,
                "non_empty_count": len(non_empty),
                "unique_values": len(values),
                "matched_values": len(matched),
                "missing_values": len(missing),
                "placeholder_values": len(placeholders),
                "matched": matched,
                "missing": missing,
                "placeholders": placeholders,
            }
        )

    # Write JSON
    json_path = args.outdir / "cu_metadata_controlled_vocab_analysis.json"
    json_path.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write CSV gaps
    csv_path = args.outdir / "cu_metadata_vocab_gaps.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["column", "value", "count", "proposed_term", "proposed_scheme"])
        w.writeheader()
        for row in sorted(gap_rows, key=lambda r: (r["column"], -r["count"], r["value"])):
            w.writerow(row)

    # Markdown report
    md_path = args.outdir / "cu_metadata_controlled_vocab_report.md"
    total_cols = len(categorical_cols)
    cols_with_gaps = sum(1 for c in analysis["columns"] if c["missing_values"] > 0)
    top_missing = global_missing_values.most_common(40)

    lines = []
    lines.append("# CU Metadata Controlled Vocabulary Gap Analysis")
    lines.append("")
    lines.append(f"- CSV: `{args.csv}`")
    lines.append(f"- Ontology: `{args.ttl}`")
    lines.append(f"- Rows: **{len(rows)}**")
    lines.append(f"- Columns scanned: **{len(fieldnames)}**")
    lines.append(f"- Categorical candidate columns analyzed: **{total_cols}**")
    lines.append(f"- Columns with at least one unmapped value: **{cols_with_gaps}**")
    lines.append("")

    lines.append("## Modeling strategy proposal (aligned with DFO conventions)")
    lines.append("")
    lines.append("1. **Use SKOS ConceptSchemes for controlled value lists** (status/type/source/category/method fields).")
    lines.append("2. **Use PascalCase term IRIs** and keep `rdfs:isDefinedBy`, `skos:prefLabel`, `skos:inScheme`, and `skos:definition`. Include `iao:0000119` and `dcterms:source` when provenance is available.")
    lines.append("3. **Add `skos:altLabel` first** when a CSV value is a lexical variant of an existing ontology term.")
    lines.append("4. **Mint new SKOS concepts** when no existing term semantically matches.")
    lines.append("5. For metrics/compound variables, follow **I-ADOPT annotation pattern** in `docs/CONVENTIONS.md` (SKOS concept + decomposition annotations).")
    lines.append("6. Keep schema-only ontology discipline: no instance data in ontology files.")
    lines.append("")

    lines.append("## Top missing values (by frequency)")
    lines.append("")
    lines.append("| Value | Count | Suggested term IRI local name |")
    lines.append("|---|---:|---|")
    for value, count in top_missing:
        lines.append(f"| `{value}` | {count} | `{to_pascal(value)}` |")
    lines.append("")

    lines.append("## Column-level comparison")
    lines.append("")
    for col in sorted(analysis["columns"], key=lambda c: c["column"]):
        lines.append(f"### `{col['column']}`")
        lines.append("")
        lines.append(f"- Unique values: **{col['unique_values']}**")
        lines.append(f"- Matched values: **{col['matched_values']}**")
        lines.append(f"- Missing values: **{col['missing_values']}**")
        if col["missing_values"]:
            lines.append(f"- Proposed scheme: `{suggest_scheme_for_column(col['column'])}`")
            missing_preview = ", ".join(f"`{m['value']}`" for m in col["missing"][:12])
            lines.append(f"- Missing preview: {missing_preview}")
        lines.append("")

    lines.append("## Reproducibility")
    lines.append("")
    lines.append("Re-run with:")
    lines.append("")
    lines.append("```bash")
    lines.append(
        f"python3 scripts/analyze_cu_metadata_controlled_vocab.py --csv {args.csv} --ttl {args.ttl} --outdir {args.outdir}"
    )
    lines.append("```")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote: {json_path}")
    print(f"Wrote: {csv_path}")
    print(f"Wrote: {md_path}")


if __name__ == "__main__":
    main()
