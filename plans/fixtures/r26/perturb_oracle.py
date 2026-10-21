#!/usr/bin/env python3
"""Independent stored-response perturbation oracle for round 26.

This deliberately does not import grader.py or grader_perturb.py.  Its JSON
extractor is a local port of the preregistered regex semantics; the response
verdict is independently reconstructed from stored want values (and the
recorded C-cell diagnostics where no want is stored).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FILES = (
    "corpus/evidence/round8-horizon/results.jsonl",
    "corpus/evidence/round9-replication/results-r9.jsonl",
    "corpus/evidence/round11-power/results-r11.jsonl",
    "corpus/evidence/round12-ladder/results-r12.jsonl",
)
FAMILIES = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "D1", "G1", "G2")
KINDS = {family: ("MC" if family in ("G1", "G2") else ("PC" if family == "D1" else "MP")) for family in FAMILIES}
FENCE_RE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S)
CANDIDATE_RE = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", re.S)


@dataclass
class Rec:
    file: str
    line: int
    cell: str
    pid: Any
    turn: Any
    grader: str
    raw: str
    want: Any
    stored_ok: bool
    row: dict[str, Any]
    extracted: Any
    meta: dict[str, Any] | None


def extract_json_block(text: str) -> Any:
    """Return the last parsable fenced JSON block, else last parsable candidate."""
    blocks = FENCE_RE.findall(text)
    if blocks:
        try:
            return json.loads(blocks[-1])
        except (TypeError, ValueError):
            pass
    for candidate in reversed(CANDIDATE_RE.findall(text)):
        try:
            return json.loads(candidate)
        except (TypeError, ValueError):
            continue
    return None


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
            if isinstance(value, dict):
                records.append({"_line": line_no, **value})
    return records


def _is_c_cell(file: str, row: dict[str, Any]) -> bool:
    return file == FILES[0] and str(row.get("cell", "")).startswith("C-")


def _meta_index(rows: list[dict[str, Any]]) -> dict[Any, dict[str, Any]]:
    return {
        row["pid"]: row
        for row in rows
        if "pid" in row and isinstance(row.get("init"), (dict, list)) and isinstance(row.get("truth"), list)
    }


def _truth_index(rec: Rec) -> int | None:
    """Identify the current truth state, including one-shot MONO responses."""
    if rec.meta is None or not isinstance(rec.meta.get("truth"), list):
        return None
    truths = rec.meta["truth"]
    if not truths:
        return None
    if isinstance(rec.want, (dict, list)):
        turn = rec.turn
        if isinstance(turn, int) and 1 <= turn <= len(truths) and truths[turn - 1] == rec.want:
            return turn - 1
        if "MONO" in rec.cell:
            for index in range(len(truths) - 1, -1, -1):
                if truths[index] == rec.want:
                    return index
        matching = [index for index, truth in enumerate(truths) if truth == rec.want]
        if matching:
            return matching[-1]
    return None


def _previous_truth(rec: Rec) -> Any:
    index = _truth_index(rec)
    if index is None or rec.meta is None:
        return None
    if index == 0:
        return rec.meta.get("init")
    return rec.meta["truth"][index - 1]


def _d1_eligible(rec: Rec) -> bool:
    if rec.grader not in ("state", "seq") or not rec.stored_ok:
        return False
    if not isinstance(rec.turn, int) or rec.turn <= 1:
        return False
    if rec.cell == "A-MONO" or rec.cell.startswith(("B-", "C-")):
        return False
    if not rec.cell.startswith(("A-", "T-")):
        return False
    previous = _previous_truth(rec)
    return previous is not None and previous != rec.want


def _valid_latin_square(square: Any) -> bool:
    symbols = {"A", "B", "C", "D"}
    if not isinstance(square, list) or len(square) != 4:
        return False
    if any(not isinstance(row, list) or len(row) != 4 or set(row) != symbols for row in square):
        return False
    return all({square[row][column] for row in range(4)} == symbols for column in range(4))


def _c_baseline(rec: Rec, answer: Any) -> bool:
    """Reconstruct the stored C-cell baseline from its visible check facts."""
    row = rec.row
    if answer != row.get("got"):
        return False
    if row.get("parse") is False:
        return False
    if rec.cell == "C-MONO":
        return _valid_latin_square(answer) and row.get("square_valid") is True
    square = answer.get("square") if isinstance(answer, dict) else None
    return (
        isinstance(answer, dict)
        and isinstance(answer.get("violations"), list)
        and _valid_latin_square(square)
        and row.get("viol_ok") is True
        and row.get("square_valid") is True
        and row.get("preserved") is True
    )


def regrade(rec: Rec, answer: Any) -> bool:
    """Independent answer check: exact stored truth, or C-cell recorded checks."""
    if rec.grader == "c":
        if answer == rec.extracted:
            return _c_baseline(rec, answer)
        # G1/G2 changes are selected to invalidate a claimed C-cell answer:
        # they alter its violation witness/square or remove a required structure.
        if isinstance(answer, dict) and isinstance(rec.extracted, dict):
            if answer.get("violations") != rec.extracted.get("violations"):
                return False
            if answer.get("square") != rec.extracted.get("square"):
                return False
        return False
    return answer == rec.want


def build_population(root: Path) -> tuple[list[Rec], int, int, dict[str, int]]:
    included: list[Rec] = []
    candidate_count = 0
    excluded = 0
    exclusion_reasons = {"baseline": 0, "missing_want": 0, "meta_truth": 0}
    loaded = {name: _load_jsonl(root / name) for name in FILES}
    for file, rows in loaded.items():
        metas = _meta_index(rows)
        for row in rows:
            if not isinstance(row.get("raw"), str) or not isinstance(row.get("ok"), bool):
                continue
            candidate_count += 1
            cell = str(row.get("cell", ""))
            is_c = _is_c_cell(file, row)
            want = row.get("want")
            grader = "c" if is_c else ("seq" if file == FILES[3] and isinstance(want, list) else "state")
            meta = metas.get(row.get("pid"))
            rec = Rec(
                file=file,
                line=int(row["_line"]),
                cell=cell,
                pid=row.get("pid"),
                turn=row.get("turn"),
                grader=grader,
                raw=row["raw"],
                want=want,
                stored_ok=row["ok"],
                row=row,
                extracted=extract_json_block(row["raw"]),
                meta=meta,
            )
            if not is_c and "want" not in row:
                excluded += 1
                exclusion_reasons["missing_want"] += 1
                continue
            if not is_c and meta is not None and isinstance(row.get("turn"), int):
                truth_index = _truth_index(rec)
                if truth_index is not None and meta["truth"][truth_index] != want:
                    excluded += 1
                    exclusion_reasons["meta_truth"] += 1
                    continue
            if regrade(rec, rec.extracted) != rec.stored_ok:
                excluded += 1
                exclusion_reasons["baseline"] += 1
                continue
            included.append(rec)
    return included, candidate_count, excluded, exclusion_reasons


def _render(value: Any, indented: bool) -> str:
    if indented:
        return json.dumps(value, ensure_ascii=False, indent=2)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _replace_extracted(raw: str, value: Any) -> str:
    blocks = list(FENCE_RE.finditer(raw))
    if blocks:
        match = blocks[-1]
        old_body = match.group(1)
        rendered = _render(value, "\n" in old_body)
        return raw[:match.start(1)] + rendered + raw[match.end(1):]
    return _render(value, "\n" in raw)


def _mutate_one(value: Any) -> Any | None:
    """Increment one integer, else replace a list scalar by a distinct token."""
    copied = json.loads(json.dumps(value, ensure_ascii=False))

    def visit(node: Any) -> bool:
        if isinstance(node, dict):
            for key, child in node.items():
                if isinstance(child, int) and not isinstance(child, bool):
                    node[key] = child + 1
                    return True
                if visit(child):
                    return True
        elif isinstance(node, list):
            for index, child in enumerate(node):
                if isinstance(child, int) and not isinstance(child, bool):
                    node[index] = child + 1
                    return True
                if isinstance(child, str):
                    node[index] = "__perturbed__" if child != "__perturbed__" else "__perturbed_2__"
                    return True
                if visit(child):
                    return True
        return False

    return copied if visit(copied) else None


def _delete_one(value: Any) -> Any | None:
    copied = json.loads(json.dumps(value, ensure_ascii=False))
    if isinstance(copied, dict) and copied:
        del copied[next(iter(copied))]
        return copied
    if isinstance(copied, list) and copied:
        del copied[0]
        return copied
    return None


def apply_family(fid: str, raw: str, extracted: Any, rec: Rec) -> str | None:
    if fid == "F1":
        blocks = list(FENCE_RE.finditer(raw))
        if not blocks:
            return None
        match = blocks[-1]
        return raw[:match.start()] + match.group(1) + raw[match.end():]
    if fid == "F2":
        blocks = list(FENCE_RE.finditer(raw))
        if not blocks or not blocks[-1].group(0).startswith("```json"):
            return None
        match = blocks[-1]
        block = match.group(0).replace("```json", "```JSON", 1)
        return raw[:match.start()] + block + raw[match.end():]
    if fid == "F3":
        return _replace_extracted(raw, extracted) if isinstance(extracted, (dict, list)) else None
    if fid == "F4":
        if not isinstance(extracted, dict):
            return None
        reversed_object = dict(reversed(list(extracted.items())))
        return _replace_extracted(raw, reversed_object)
    if fid == "F5":
        return "This response is below.\n" + raw
    if fid == "F6":
        return raw + "\nThe response is complete."
    if fid == "F7":
        if "\n" not in raw:
            return None
        return raw.replace("\r\n", "\n").replace("\n", "\r\n")
    if fid == "D1":
        if not _d1_eligible(rec):
            return None
        previous = _previous_truth(rec)
        return raw + "\n\n```json\n" + json.dumps(previous, ensure_ascii=False) + "\n```\nFor reference: the previous turn's truth."
    if fid == "G1":
        changed = _mutate_one(extracted) if extracted is not None else None
        return _replace_extracted(raw, changed) if changed is not None else None
    if fid == "G2":
        changed = _delete_one(extracted) if extracted is not None else None
        return _replace_extracted(raw, changed) if changed is not None else None
    raise ValueError(f"unknown family {fid}")


def family_counts(population: list[Rec]) -> dict[str, tuple[int, int]]:
    counts: dict[str, tuple[int, int]] = {}
    for fid in FAMILIES:
        kind = KINDS[fid]
        n = 0
        k = 0
        for rec in population:
            if kind == "MC" and not rec.stored_ok:
                continue
            transformed = apply_family(fid, rec.raw, rec.extracted, rec)
            if transformed is None:
                continue
            transformed_answer = extract_json_block(transformed)
            n += 1
            if kind == "MP":
                if regrade(rec, transformed_answer) == rec.stored_ok:
                    k += 1
            elif kind == "PC":
                if transformed_answer == _previous_truth(rec):
                    k += 1
            elif not regrade(rec, transformed_answer):
                k += 1
        counts[fid] = (n, k)
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    try:
        population, candidate_count, excluded, reasons = build_population(args.root.resolve())
        counts = family_counts(population)
    except (OSError, ValueError) as exc:
        print(f"oracle error: {exc}", file=sys.stderr)
        return 1
    print(f"POPULATION candidates={candidate_count} included={len(population)} excluded={excluded}")
    print("EXCLUDED " + " ".join(f"{key}={value}" for key, value in reasons.items()))
    for fid in FAMILIES:
        n, k = counts[fid]
        print(f"{fid} kind={KINDS[fid]} n={n} k={k}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
