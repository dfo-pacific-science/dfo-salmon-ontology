#!/usr/bin/env python3
"""Stabilize WIDOCO/WebVOWL ontology.json output.

Why this exists
---------------
WIDOCO's bundled OWL2VOWL step emits `docs/webvowl/data/ontology.json` with
nondeterministic internal ids and array ordering even when the ontology input is
unchanged. That causes noisy diffs from repeated `make docs-widoco` /
`make docs-refresh` runs.

What this script does
---------------------
1. If a baseline JSON is available (explicit `--baseline` or `git show HEAD:<path>`),
   compare graph semantics while ignoring transient ids and ordering.
2. If the generated file is semantically identical to the baseline, restore the
   baseline bytes exactly. That makes no-op docs refreshes produce zero diff.
3. Otherwise, preserve baseline ids/order where objects still match semantically,
   allocate deterministic ids for new objects, and write a normalized JSON file.

The goal is stability, not cleverness.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path
from typing import Any, Callable

from rdflib import Graph, Literal
from rdflib.namespace import OWL, RDFS, SKOS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to generated ontology.json")
    parser.add_argument(
        "--baseline",
        help="Optional baseline ontology.json. Defaults to git HEAD copy when available.",
    )
    parser.add_argument(
        "--ontology",
        help="Optional ontology TTL used to normalize labels and property hierarchy.",
    )
    parser.add_argument(
        "--max-inline",
        type=int,
        default=140,
        help="Max length for inline JSON fragments when emitting normalized output.",
    )
    return parser.parse_args()


def load_git_head_text(path: Path) -> str | None:
    try:
        repo_root = subprocess.check_output(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return None

    repo_root_path = Path(repo_root).resolve()
    try:
        rel = path.resolve().relative_to(repo_root_path)
    except ValueError:
        return None

    try:
        return subprocess.check_output(
            ["git", "-C", str(repo_root_path), "show", f"HEAD:{rel.as_posix()}"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None


def annotation_key(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple((k, annotation_key(v)) for k, v in value.items())
    if isinstance(value, list):
        return tuple(annotation_key(v) for v in value)
    return value


def semantic_sort_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def semantic_normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: semantic_normalize(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        normalized = [semantic_normalize(v) for v in value]
        return sorted(normalized, key=semantic_sort_key)
    return value


class OntologyHints:
    def __init__(self, path: Path | None) -> None:
        self.labels_by_iri: dict[str, str] = {}
        self.superprops_by_iri: dict[str, set[str]] = defaultdict(set)
        self.inverse_by_iri: dict[str, set[str]] = defaultdict(set)
        if path is None or not path.exists():
            return

        graph = Graph()
        graph.parse(path)

        def preferred_literal(subject: Any) -> str | None:
            for predicate in (SKOS.prefLabel, RDFS.label):
                english = [
                    obj
                    for obj in graph.objects(subject, predicate)
                    if isinstance(obj, Literal) and (obj.language or "") == "en"
                ]
                if english:
                    return str(english[0])
                unlabeled = [
                    obj
                    for obj in graph.objects(subject, predicate)
                    if isinstance(obj, Literal) and not obj.language
                ]
                if unlabeled:
                    return str(unlabeled[0])
            return None

        for subject in set(graph.subjects()):
            if not hasattr(subject, "toPython"):
                continue
            subject_iri = str(subject)
            label = preferred_literal(subject)
            if label:
                self.labels_by_iri[subject_iri] = label
            for obj in graph.objects(subject, RDFS.subPropertyOf):
                if hasattr(obj, "toPython"):
                    self.superprops_by_iri[subject_iri].add(str(obj))
            for obj in graph.objects(subject, OWL.inverseOf):
                if hasattr(obj, "toPython"):
                    self.inverse_by_iri[subject_iri].add(str(obj))
                    self.inverse_by_iri[str(obj)].add(subject_iri)

    def preferred_label(self, iri: str) -> str | None:
        return self.labels_by_iri.get(iri)


class WebVowlGraph:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.class_types = {item["id"]: item["type"] for item in data["class"]}
        self.class_attrs = {item["id"]: item for item in data["classAttribute"]}
        self.prop_types = {item["id"]: item["type"] for item in data["property"]}
        self.prop_attrs = {item["id"]: item for item in data["propertyAttribute"]}

        self.class_keys = {
            old_id: self._class_key(old_id) for old_id in self.class_attrs.keys()
        }
        self.prop_keys = {
            old_id: self._prop_key(old_id) for old_id in self.prop_attrs.keys()
        }

        self.class_key_to_id = self._invert_unique(self.class_keys, "class")
        self.prop_key_to_id = self._invert_unique(self.prop_keys, "property")

    @staticmethod
    def _invert_unique(mapping: dict[str, Any], label: str) -> dict[Any, str]:
        inverse: dict[Any, str] = {}
        for object_id, key in mapping.items():
            if key in inverse:
                raise ValueError(
                    f"Non-unique semantic {label} key for ids {inverse[key]} and {object_id}"
                )
            inverse[key] = object_id
        return inverse

    def _named_class_ref(self, class_id: str) -> tuple[Any, ...]:
        item = self.class_attrs[class_id]
        return ("named", self.class_types[class_id], item["iri"])

    def class_ref(self, class_id: str) -> tuple[Any, ...]:
        item = self.class_attrs[class_id]
        if "iri" in item:
            return self._named_class_ref(class_id)
        if "union" in item:
            members = tuple(
                sorted(
                    (self.class_types[mid], self.class_attrs[mid].get("iri", ""))
                    for mid in item["union"]
                )
            )
            context = []
            for prop_id, prop in self.prop_attrs.items():
                if prop["domain"] == class_id:
                    other = self.class_attrs[prop["range"]].get("iri", "")
                    context.append(
                        (
                            "domainOf",
                            self.prop_types[prop_id],
                            prop.get("iri", ""),
                            other,
                        )
                    )
                if prop["range"] == class_id:
                    other = self.class_attrs[prop["domain"]].get("iri", "")
                    context.append(
                        (
                            "rangeOf",
                            self.prop_types[prop_id],
                            prop.get("iri", ""),
                            other,
                        )
                    )
            return ("union", members, tuple(sorted(context)))
        return (
            "anon",
            self.class_types[class_id],
            tuple(sorted(item.get("attributes", []))),
        )

    def _class_key(self, class_id: str) -> tuple[Any, ...]:
        item = self.class_attrs[class_id]
        if "iri" in item:
            return self._named_class_ref(class_id)
        return self.class_ref(class_id)

    def prop_ref(self, prop_id: str) -> tuple[Any, ...]:
        if prop_id in self.prop_attrs:
            return self.prop_keys[prop_id]
        return ("dangling-property", prop_id)

    def _prop_key(self, prop_id: str) -> tuple[Any, ...]:
        item = self.prop_attrs[prop_id]
        label = tuple(item.get("label", {}).items()) if item.get("iri") else ()
        return (
            self.prop_types[prop_id],
            item.get("iri", ""),
            self.class_ref(item["domain"]),
            self.class_ref(item["range"]),
            label,
        )

    def _semanticize_class_item(self, class_id: str) -> Any:
        item = self.class_attrs[class_id]
        out: dict[str, Any] = {"type": self.class_types[class_id]}
        for key, value in item.items():
            if key == "id":
                continue
            if key in ("subClasses", "superClasses", "equivalent", "union"):
                out[key] = sorted((self.class_ref(v) for v in value), key=semantic_sort_key)
            else:
                out[key] = semantic_normalize(value)
        return semantic_normalize(out)

    def _semanticize_prop_item(self, prop_id: str) -> Any:
        item = self.prop_attrs[prop_id]
        out: dict[str, Any] = {"type": self.prop_types[prop_id]}
        for key, value in item.items():
            if key == "id":
                continue
            if key in ("domain", "range"):
                out[key] = self.class_ref(value)
            elif key in ("subproperty", "superproperty"):
                out[key] = sorted(
                    (self.prop_ref(v) for v in value if v in self.prop_attrs),
                    key=semantic_sort_key,
                )
            elif key == "inverse":
                if value in self.prop_attrs:
                    out[key] = self.prop_ref(value)
            elif key == "label" and "iri" not in item:
                # OWL2VOWL emits unstable synthetic labels for anonymous rdf:Property edges.
                continue
            else:
                out[key] = semantic_normalize(value)
        return semantic_normalize(out)

    def semantic_signature(self) -> tuple[Any, Any, Any]:
        non_graph = OrderedDict()
        for key in ("_comment", "header", "namespace"):
            non_graph[key] = semantic_normalize(self.data.get(key))
        class_signature = tuple(
            sorted(
                (
                    (self.class_keys[class_id], self._semanticize_class_item(class_id))
                    for class_id in self.class_attrs.keys()
                ),
                key=semantic_sort_key,
            )
        )
        prop_signature = tuple(
            sorted(
                (
                    (self.prop_keys[prop_id], self._semanticize_prop_item(prop_id))
                    for prop_id in self.prop_attrs.keys()
                ),
                key=semantic_sort_key,
            )
        )
        return (semantic_normalize(non_graph), class_signature, prop_signature)


class Normalizer:
    def __init__(
        self,
        current_text: str,
        current_data: dict[str, Any],
        baseline_text: str | None,
        baseline_data: dict[str, Any] | None,
        ontology_hints: OntologyHints,
        max_inline: int,
    ) -> None:
        self.current_text = current_text
        self.current_data = current_data
        self.current_graph = WebVowlGraph(current_data)
        self.baseline_text = baseline_text
        self.baseline_data = baseline_data
        self.baseline_graph = WebVowlGraph(baseline_data) if baseline_data else None
        self.ontology_hints = ontology_hints
        self.max_inline = max_inline

    def normalize(self) -> str:
        if self.baseline_graph and self._semantically_equal_to_baseline():
            return self.baseline_text  # exact byte-for-byte restore for no-op refreshes

        class_id_map, prop_id_map = self._build_id_maps()
        normalized = self._render_normalized_json(class_id_map, prop_id_map)

        if self.baseline_text:
            normalized_graph = WebVowlGraph(json.loads(normalized))
            if normalized_graph.semantic_signature() == self.baseline_graph.semantic_signature():
                return self.baseline_text

        return normalized

    def _semantically_equal_to_baseline(self) -> bool:
        assert self.baseline_graph is not None
        return self.current_graph.semantic_signature() == self.baseline_graph.semantic_signature()

    def _reserved_ids(self) -> set[str]:
        reserved = set(self.current_graph.class_attrs) | set(self.current_graph.prop_attrs)
        if self.baseline_graph:
            reserved |= set(self.baseline_graph.class_attrs) | set(self.baseline_graph.prop_attrs)

        for item in self.current_data["classAttribute"]:
            for field in ("subClasses", "superClasses", "equivalent", "union"):
                reserved.update(item.get(field, []))
        for item in self.current_data["propertyAttribute"]:
            reserved.add(item["domain"])
            reserved.add(item["range"])
            for field in ("subproperty", "superproperty"):
                reserved.update(item.get(field, []))
            if "inverse" in item:
                reserved.add(item["inverse"])
        return reserved

    def _allocate_ids(
        self,
        current_key_to_id: dict[Any, str],
        baseline_key_to_id: dict[Any, str] | None,
        reserved: set[str],
        start_at: int,
    ) -> tuple[dict[str, str], int]:
        mapping: dict[str, str] = {}
        if baseline_key_to_id:
            for key, old_id in current_key_to_id.items():
                if key in baseline_key_to_id:
                    mapping[old_id] = baseline_key_to_id[key]

        next_id = start_at
        for key in sorted(current_key_to_id.keys(), key=semantic_sort_key):
            old_id = current_key_to_id[key]
            if old_id in mapping:
                continue
            while str(next_id) in reserved:
                next_id += 1
            mapping[old_id] = str(next_id)
            reserved.add(str(next_id))
            next_id += 1
        return mapping, next_id

    def _build_id_maps(self) -> tuple[dict[str, str], dict[str, str]]:
        reserved = self._reserved_ids()
        start_at = max(int(value) for value in reserved) + 1 if reserved else 0

        baseline_class_keys = (
            self.baseline_graph.class_key_to_id if self.baseline_graph else None
        )
        baseline_prop_keys = (
            self.baseline_graph.prop_key_to_id if self.baseline_graph else None
        )

        class_id_map, next_id = self._allocate_ids(
            self.current_graph.class_key_to_id,
            baseline_class_keys,
            reserved,
            start_at,
        )
        prop_id_map, _ = self._allocate_ids(
            self.current_graph.prop_key_to_id,
            baseline_prop_keys,
            reserved,
            next_id,
        )
        return class_id_map, prop_id_map

    @staticmethod
    def _order_like(
        items: list[Any],
        keyfunc: Callable[[Any], Any],
        baseline_items: list[Any] | None = None,
    ) -> list[Any]:
        if baseline_items is not None:
            if Counter(keyfunc(item) for item in items) == Counter(
                keyfunc(item) for item in baseline_items
            ):
                buckets: dict[Any, list[Any]] = {}
                for item in items:
                    buckets.setdefault(keyfunc(item), []).append(item)
                ordered: list[Any] = []
                for item in baseline_items:
                    key = keyfunc(item)
                    ordered.append(buckets[key].pop(0))
                return ordered
        return sorted(items, key=keyfunc)

    @staticmethod
    def _normalize_small_dict(
        value: dict[str, Any], baseline_value: dict[str, Any] | None = None
    ) -> OrderedDict[str, Any]:
        if baseline_value and Counter(value.keys()) == Counter(baseline_value.keys()):
            key_order = [k for k in baseline_value.keys() if k in value]
        else:
            key_order = sorted(value.keys())
        return OrderedDict((k, value[k]) for k in key_order)

    def _normalize_annotation_list(
        self, values: list[dict[str, Any]], baseline_values: list[dict[str, Any]] | None = None
    ) -> list[OrderedDict[str, Any]]:
        normalized = [OrderedDict((k, v) for k, v in item.items()) for item in values]
        return self._order_like(normalized, annotation_key, baseline_values)

    def _normalize_annotation_dict(
        self,
        value: dict[str, list[dict[str, Any]]],
        baseline_value: dict[str, list[dict[str, Any]]] | None = None,
    ) -> OrderedDict[str, list[OrderedDict[str, Any]]]:
        if baseline_value and Counter(value.keys()) == Counter(baseline_value.keys()):
            key_order = [k for k in baseline_value.keys() if k in value]
        else:
            key_order = sorted(value.keys())
        out: OrderedDict[str, list[OrderedDict[str, Any]]] = OrderedDict()
        for key in key_order:
            out[key] = self._normalize_annotation_list(
                value[key], baseline_value.get(key) if baseline_value else None
            )
        return out

    @staticmethod
    def _sort_mapped_ids(values: list[str]) -> list[str]:
        return sorted(
            values,
            key=lambda x: (0, int(x)) if str(x).isdigit() else (1, str(x)),
        )

    def _normalize_ref_list(
        self,
        values: list[str],
        mapper: Callable[[str], str],
        baseline_values: list[str] | None = None,
    ) -> list[str]:
        mapped = [mapper(v) for v in values]
        if baseline_values is not None and Counter(mapped) == Counter(baseline_values):
            buckets: dict[str, list[str]] = {}
            for value in mapped:
                buckets.setdefault(value, []).append(value)
            ordered: list[str] = []
            for value in baseline_values:
                ordered.append(buckets[value].pop(0))
            return ordered
        return self._sort_mapped_ids(mapped)

    def _apply_preferred_label(
        self, iri: str | None, label_value: dict[str, Any], baseline_value: dict[str, Any] | None
    ) -> OrderedDict[str, Any]:
        normalized = self._normalize_small_dict(label_value, baseline_value)
        if iri:
            preferred = self.ontology_hints.preferred_label(iri)
            if preferred and "en" in normalized:
                normalized["en"] = preferred
        return normalized

    def _build_property_relationship_hints(
        self, current_prop_by_assigned: dict[str, str]
    ) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, str]]:
        iri_to_assigned_ids: dict[str, list[str]] = defaultdict(list)
        for assigned_id, old_id in current_prop_by_assigned.items():
            item = self.current_graph.prop_attrs[old_id]
            prop_type = self.current_graph.prop_types[old_id]
            iri = item.get("iri")
            if iri and prop_type in {"owl:objectProperty", "rdf:Property"}:
                iri_to_assigned_ids[iri].append(assigned_id)

        for values in iri_to_assigned_ids.values():
            values.sort(key=lambda x: int(x))

        desired_superprops: dict[str, list[str]] = {}
        desired_subprops: dict[str, list[str]] = defaultdict(list)
        desired_inverse: dict[str, str] = {}

        for assigned_id, old_id in current_prop_by_assigned.items():
            item = self.current_graph.prop_attrs[old_id]
            iri = item.get("iri")
            if not iri:
                continue

            super_ids: list[str] = []
            for super_iri in sorted(self.ontology_hints.superprops_by_iri.get(iri, set())):
                super_ids.extend(iri_to_assigned_ids.get(super_iri, []))
            if super_ids:
                desired_superprops[assigned_id] = self._sort_mapped_ids(super_ids)
                for super_id in desired_superprops[assigned_id]:
                    desired_subprops[super_id].append(assigned_id)

            inverse_ids: list[str] = []
            for inverse_iri in sorted(self.ontology_hints.inverse_by_iri.get(iri, set())):
                inverse_ids.extend(iri_to_assigned_ids.get(inverse_iri, []))
            if inverse_ids:
                desired_inverse[assigned_id] = self._sort_mapped_ids(inverse_ids)[0]

        return (
            desired_superprops,
            {
                prop_id: self._sort_mapped_ids(values)
                for prop_id, values in desired_subprops.items()
                if values
            },
            desired_inverse,
        )

    def _render_normalized_json(
        self, class_id_map: dict[str, str], prop_id_map: dict[str, str]
    ) -> str:
        current_class_by_assigned = {
            class_id_map[old_id]: old_id for old_id in self.current_graph.class_attrs.keys()
        }
        current_prop_by_assigned = {
            prop_id_map[old_id]: old_id for old_id in self.current_graph.prop_attrs.keys()
        }
        desired_superprops, desired_subprops, desired_inverse = self._build_property_relationship_hints(
            current_prop_by_assigned
        )

        baseline_class_attrs = self.baseline_graph.class_attrs if self.baseline_graph else {}
        baseline_prop_attrs = self.baseline_graph.prop_attrs if self.baseline_graph else {}
        baseline_header = self.baseline_data.get("header", {}) if self.baseline_data else {}

        def map_class_ref(ref: str) -> str:
            return class_id_map.get(ref, ref)

        def map_prop_ref(ref: str) -> str:
            return prop_id_map.get(ref, ref)

        def transform_class_attr(assigned_id: str) -> OrderedDict[str, Any]:
            old_id = current_class_by_assigned[assigned_id]
            item = self.current_graph.class_attrs[old_id]
            baseline_item = baseline_class_attrs.get(assigned_id)

            if baseline_item and Counter(item.keys()) == Counter(baseline_item.keys()):
                key_order = [k for k in baseline_item.keys() if k in item]
            else:
                key_order = list(item.keys())

            out: OrderedDict[str, Any] = OrderedDict()
            for key in key_order:
                value = item[key]
                if key == "id":
                    out[key] = assigned_id
                elif key in ("subClasses", "superClasses", "equivalent", "union"):
                    out[key] = self._normalize_ref_list(
                        value,
                        map_class_ref,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "attributes":
                    out[key] = self._order_like(
                        list(value),
                        lambda x: x,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "annotations":
                    out[key] = self._normalize_annotation_dict(
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "individuals":
                    normalized_individuals = []
                    baseline_values = baseline_item.get(key) if baseline_item else None
                    for individual in value:
                        baseline_match = None
                        if baseline_values:
                            baseline_match = next(
                                (
                                    candidate
                                    for candidate in baseline_values
                                    if candidate.get("iri") == individual.get("iri")
                                ),
                                None,
                            )
                        if baseline_match and Counter(individual.keys()) == Counter(
                            baseline_match.keys()
                        ):
                            individual_key_order = [
                                k for k in baseline_match.keys() if k in individual
                            ]
                        else:
                            individual_key_order = list(individual.keys())

                        individual_out: OrderedDict[str, Any] = OrderedDict()
                        for subkey in individual_key_order:
                            subvalue = individual[subkey]
                            if subkey == "annotations":
                                individual_out[subkey] = self._normalize_annotation_dict(
                                    subvalue,
                                    baseline_match.get(subkey)
                                    if baseline_match
                                    else None,
                                )
                            elif subkey in ("labels", "label", "comment"):
                                individual_out[subkey] = self._normalize_small_dict(
                                    subvalue,
                                    baseline_match.get(subkey)
                                    if baseline_match
                                    else None,
                                )
                            else:
                                individual_out[subkey] = subvalue
                        normalized_individuals.append(individual_out)
                    out[key] = self._order_like(
                        normalized_individuals,
                        lambda x: x.get("iri", ""),
                        baseline_values,
                    )
                elif key == "label":
                    out[key] = self._apply_preferred_label(
                        item.get("iri"),
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "comment":
                    out[key] = self._normalize_small_dict(
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                else:
                    out[key] = value
            return out

        def transform_prop_attr(assigned_id: str) -> OrderedDict[str, Any]:
            old_id = current_prop_by_assigned[assigned_id]
            item = self.current_graph.prop_attrs[old_id]
            baseline_item = baseline_prop_attrs.get(assigned_id)

            if baseline_item and Counter(item.keys()) == Counter(baseline_item.keys()):
                key_order = [k for k in baseline_item.keys() if k in item]
            else:
                key_order = list(item.keys())

            out: OrderedDict[str, Any] = OrderedDict()
            for key in key_order:
                value = item[key]
                if key == "id":
                    out[key] = assigned_id
                elif key in ("domain", "range"):
                    out[key] = map_class_ref(value)
                elif key == "subproperty":
                    desired = desired_subprops.get(assigned_id)
                    if desired:
                        out[key] = desired
                elif key == "superproperty":
                    desired = desired_superprops.get(assigned_id)
                    if desired:
                        out[key] = desired
                elif key == "inverse":
                    desired = desired_inverse.get(assigned_id)
                    if desired:
                        out[key] = desired
                elif key == "attributes":
                    out[key] = self._order_like(
                        list(value),
                        lambda x: x,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "annotations":
                    out[key] = self._normalize_annotation_dict(
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "label":
                    out[key] = self._apply_preferred_label(
                        item.get("iri"),
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                elif key == "comment":
                    out[key] = self._normalize_small_dict(
                        value,
                        baseline_item.get(key) if baseline_item else None,
                    )
                else:
                    out[key] = value

            if item.get("iri"):
                if desired_superprops.get(assigned_id) and "superproperty" not in out:
                    out["superproperty"] = desired_superprops[assigned_id]
                if desired_subprops.get(assigned_id) and "subproperty" not in out:
                    out["subproperty"] = desired_subprops[assigned_id]
                if desired_inverse.get(assigned_id) and "inverse" not in out:
                    out["inverse"] = desired_inverse[assigned_id]
            return out

        out: OrderedDict[str, Any] = OrderedDict()
        out["_comment"] = self.current_data["_comment"]

        current_header = self.current_data["header"]
        if baseline_header and Counter(current_header.keys()) == Counter(baseline_header.keys()):
            header_order = [k for k in baseline_header.keys() if k in current_header]
        else:
            header_order = list(current_header.keys())

        header: OrderedDict[str, Any] = OrderedDict()
        for key in header_order:
            value = current_header[key]
            baseline_value = baseline_header.get(key) if baseline_header else None
            if key in ("languages", "baseIris", "author"):
                header[key] = self._order_like(
                    list(value),
                    lambda x: x,
                    baseline_value,
                )
            elif key in ("title", "description", "comments"):
                header[key] = self._normalize_small_dict(value, baseline_value)
            elif key == "other":
                header[key] = self._normalize_annotation_dict(value, baseline_value)
            else:
                header[key] = value
        out["header"] = header

        out["namespace"] = self._order_like(
            list(self.current_data.get("namespace", [])),
            annotation_key,
            self.baseline_data.get("namespace", []) if self.baseline_data else None,
        )

        assigned_class_ids = sorted(current_class_by_assigned.keys(), key=lambda x: int(x))
        out["class"] = [
            OrderedDict(
                [
                    ("id", assigned_id),
                    (
                        "type",
                        self.current_graph.class_types[current_class_by_assigned[assigned_id]],
                    ),
                ]
            )
            for assigned_id in assigned_class_ids
        ]
        out["classAttribute"] = [transform_class_attr(assigned_id) for assigned_id in assigned_class_ids]

        assigned_prop_ids = sorted(current_prop_by_assigned.keys(), key=lambda x: int(x))
        out["property"] = [
            OrderedDict(
                [
                    ("id", assigned_id),
                    (
                        "type",
                        self.current_graph.prop_types[current_prop_by_assigned[assigned_id]],
                    ),
                ]
            )
            for assigned_id in assigned_prop_ids
        ]
        out["propertyAttribute"] = [transform_prop_attr(assigned_id) for assigned_id in assigned_prop_ids]

        rendered = self._render_lines(out, indent=0)
        return "\n".join(rendered) + "\n"

    def _inline_repr(self, value: Any) -> str | None:
        if isinstance(value, (str, int, float, bool)) or value is None:
            return json.dumps(value, ensure_ascii=False)

        if isinstance(value, dict):
            parts = []
            for key, subvalue in value.items():
                rendered = self._inline_repr(subvalue)
                if rendered is None:
                    return None
                parts.append(f'{json.dumps(key, ensure_ascii=False)} : {rendered}')
            text = "{ " + ", ".join(parts) + " }" if parts else "{ }"
            return text if len(text) <= self.max_inline else None

        if isinstance(value, list):
            parts = []
            for subvalue in value:
                rendered = self._inline_repr(subvalue)
                if rendered is None:
                    return None
                parts.append(rendered)
            text = "[ " + ", ".join(parts) + " ]" if parts else "[ ]"
            return text if len(text) <= self.max_inline else None

        return None

    def _render_lines(self, value: Any, indent: int) -> list[str]:
        inline = self._inline_repr(value)
        if inline is not None:
            return [(" " * indent) + inline]

        if isinstance(value, dict):
            lines = [(" " * indent) + "{"]
            items = list(value.items())
            for index, (key, subvalue) in enumerate(items):
                child_lines = self._render_lines(subvalue, indent + 2)
                prefix = (" " * (indent + 2)) + json.dumps(key, ensure_ascii=False) + " : "
                first_line = child_lines[0][indent + 2 :]
                lines.append(prefix + first_line)
                lines.extend(child_lines[1:])
                if index < len(items) - 1:
                    lines[-1] = lines[-1] + ","
            lines.append((" " * indent) + "}")
            return lines

        if isinstance(value, list):
            lines = [(" " * indent) + "["]
            for index, subvalue in enumerate(value):
                child_lines = self._render_lines(subvalue, indent + 2)
                lines.extend(child_lines)
                if index < len(value) - 1:
                    lines[-1] = lines[-1] + ","
            lines.append((" " * indent) + "]")
            return lines

        return [(" " * indent) + json.dumps(value, ensure_ascii=False)]


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    current_text = path.read_text(encoding="utf-8")
    current_data = json.loads(current_text)

    baseline_text: str | None = None
    if args.baseline:
        baseline_path = Path(args.baseline)
        if baseline_path.exists():
            baseline_text = baseline_path.read_text(encoding="utf-8")
    if baseline_text is None:
        baseline_text = load_git_head_text(path)

    baseline_data = json.loads(baseline_text) if baseline_text else None
    ontology_hints = OntologyHints(Path(args.ontology)) if args.ontology else OntologyHints(None)

    normalizer = Normalizer(
        current_text=current_text,
        current_data=current_data,
        baseline_text=baseline_text,
        baseline_data=baseline_data,
        ontology_hints=ontology_hints,
        max_inline=args.max_inline,
    )
    normalized = normalizer.normalize()

    if normalized != current_text:
        path.write_text(normalized, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
