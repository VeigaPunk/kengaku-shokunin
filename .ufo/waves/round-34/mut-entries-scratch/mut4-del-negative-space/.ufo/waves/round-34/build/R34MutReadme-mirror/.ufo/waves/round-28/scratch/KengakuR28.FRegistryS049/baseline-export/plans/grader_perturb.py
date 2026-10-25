#!/usr/bin/env python3
"""Offline metamorphic audit of the committed response-grader population."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BAR = 0.95
FAMILY_ORDER = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "D1", "G1", "G2")
FAMILY_KIND = {fid: ("PC" if fid == "D1" else "MC" if fid in ("G1", "G2") else "MP") for fid in FAMILY_ORDER}
FORMAT_CLASSES = ("FJ1", "FJM", "MULTI", "DANGLE", "BARE")
EXPECTED_POPULATION = 1964
POPULATION_FILES = (
    "corpus/evidence/round8-horizon/results.jsonl",
    "corpus/evidence/round9-replication/results-r9.jsonl",
    "corpus/evidence/round11-power/results-r11.jsonl",
    "corpus/evidence/round12-ladder/results-r12.jsonl",
)
# Frozen base-byte identities; do not update these to accommodate changed evidence.
POPULATION_SHA256 = {
    "corpus/evidence/round8-horizon/results.jsonl": "bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204",
    "corpus/evidence/round9-replication/results-r9.jsonl": "c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb",
    "corpus/evidence/round11-power/results-r11.jsonl": "918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad",
    "corpus/evidence/round12-ladder/results-r12.jsonl": "ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1",
}
FENCED_RE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S)
BARE_RE = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}|\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]", re.S)


@dataclass(frozen=True)
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
    previous: Any = None
    rep: Any = None


def format_class(raw: str) -> str:
    """Classify one response by the committed extractor's matched fence shape."""
    blocks = list(FENCED_RE.finditer(raw))
    if len(blocks) > 1:
        return "MULTI"
    if blocks:
        body = blocks[0].group(1).strip()
        return "FJM" if "\n" in body or "\r" in body else "FJ1"
    return "DANGLE" if "```" in raw else "BARE"

_GRADER = None
_CP = None
_ROOT = None
_LAST = {"errors": [], "candidate_count": 0, "excluded": 0, "pins": {}}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _configure(root: Path):
    global _GRADER, _CP, _ROOT
    root = root.resolve()
    if _ROOT == root and _GRADER is not None and _CP is not None:
        return
    grader_path = root / "grader.py"
    cp_path = root / "plans" / "attrib_calibration.py"
    _GRADER = _load_module("_r26_grader_" + hashlib.sha1(str(root).encode()).hexdigest()[:10], grader_path)
    calibration = _load_module("_r26_calibration_" + hashlib.sha1(str(root).encode()).hexdigest()[:10], cp_path)
    _CP = calibration.clopper_pearson
    _ROOT = root


def _read_jsonl(path: Path) -> list[tuple[int, dict[str, Any]]]:
    rows = []
    with path.open("r", encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if line.strip():
                rows.append((line_no, json.loads(line)))
    return rows


def _truth_by_pid(rows: list[tuple[int, dict[str, Any]]], cell: str) -> dict[Any, tuple[dict[str, Any], list[Any]]]:
    """Regenerate truth with the same state/list replay semantics as grader.py."""
    truth = {}
    for _line, meta in rows:
        if meta.get("cell") != cell:
            continue
        pid = meta.get("pid")
        if pid in truth:
            raise ValueError(f"duplicate {cell} pid {pid}")
        init = meta["init"]
        ops = meta["ops"]
        if cell == "meta2":
            states = _GRADER.seq_states_along(init, ops)
        else:
            states = _GRADER.states_along(init, [tuple(op) for op in ops])
        truth[pid] = (init, states)
    return truth


def _expected_for(path: str, row: dict[str, Any], state_truth, list_truth):
    cell = row.get("cell", "")
    pid = row.get("pid")
    turn = row.get("turn")
    if path.endswith("round8-horizon/results.jsonl"):
        if cell.startswith("A-") and not cell.endswith("-ack"):
            meta = state_truth.get(pid)
            if not meta:
                return None, None
            init, states = meta
            index = len(states) - 1 if cell == "A-MONO" else turn - 1
            if not isinstance(index, int) or not (0 <= index < len(states)):
                return None, None
            previous = init if index == 0 else states[index - 1]
            return states[index], previous
        if cell.startswith("B-"):
            meta = state_truth.get(pid)
            if not meta or not meta[1]:
                return None, None
            states = meta[1]
            return states[-1], states[-2] if len(states) > 1 else meta[0]
        if cell.startswith("C-"):
            return None, None
        return None, None
    if cell == "A-MONO":
        meta = state_truth.get(pid)
        if not meta or not meta[1]:
            return None, None
        init, states = meta
        return states[-1], states[-2] if len(states) > 1 else init
    if path.endswith("round12-ladder/results-r12.jsonl") and cell in ("T-DENSE", "T-SPARSE"):
        meta = list_truth.get(pid)
        if not meta:
            return None, None
        init, states = meta
        if not isinstance(turn, int) or not (1 <= turn <= len(states)):
            return None, None
        return states[turn - 1], init if turn == 1 else states[turn - 2]
    meta = state_truth.get(pid)
    if not meta:
        return None, None
    init, states = meta
    if not isinstance(turn, int) or not (1 <= turn <= len(states)):
        return None, None
    return states[turn - 1], init if turn == 1 else states[turn - 2]


def _grader_for(path: str, cell: str) -> str | None:
    if path.endswith("round8-horizon/results.jsonl"):
        if cell.startswith("C-"):
            return "c"
        if cell.startswith("A-") and not cell.endswith("-ack") or cell.startswith("B-"):
            return "state"
        return None
    if path.endswith("round9-replication/results-r9.jsonl"):
        return "state" if cell.startswith("A-") and not cell.endswith("-ack") else None
    if path.endswith("round11-power/results-r11.jsonl"):
        return "state" if cell in ("A-CKPT4710", "A-CKPT710") else None
    if path.endswith("round12-ladder/results-r12.jsonl"):
        if cell in ("T-DENSE", "T-SPARSE"):
            return "seq"
        if cell in _GRADER.GRADED_CELLS:
            return "state"
    return None


def build_population(root) -> list[Rec]:
    """Load the frozen four-file population and retain only exact baseline replays."""
    global _LAST
    root = Path(root).resolve()
    _configure(root)
    _LAST = {"errors": [], "candidate_count": 0, "excluded": 0, "pins": {}}
    loaded = {}
    for rel in POPULATION_FILES:
        path = root / rel
        try:
            data = path.read_bytes()
        except OSError as exc:
            _LAST["errors"].append(f"{rel}: unreadable: {exc}")
            _LAST["pins"][rel] = {"expected": POPULATION_SHA256[rel], "actual": None, "match": False}
            continue
        actual = hashlib.sha256(data).hexdigest()
        match = actual == POPULATION_SHA256[rel]
        _LAST["pins"][rel] = {"expected": POPULATION_SHA256[rel], "actual": actual, "match": match}
        if not match:
            _LAST["errors"].append(f"{rel}: sha256 {actual} != frozen {POPULATION_SHA256[rel]}")
        try:
            loaded[rel] = _read_jsonl(path)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            _LAST["errors"].append(f"{rel}: invalid JSONL: {exc}")

    population = []
    for rel, rows in loaded.items():
        state_truth = _truth_by_pid(rows, "meta")
        list_truth = _truth_by_pid(rows, "meta2")
        for line_no, row in rows:
            if "raw" not in row or "ok" not in row:
                continue
            _LAST["candidate_count"] += 1
            cell = row.get("cell", "")
            grader = _grader_for(rel, cell)
            if grader is None:
                _LAST["excluded"] += 1
                _LAST["errors"].append(f"{rel}:{line_no}: raw/ok record has no replay grader (cell={cell!r})")
                continue
            want, previous = _expected_for(rel, row, state_truth, list_truth)
            rec = Rec(rel, line_no, cell, row.get("pid"), row.get("turn"), grader,
                      row.get("raw"), want, row.get("ok"), previous, row.get("rep"))
            why = None
            if not isinstance(rec.raw, str):
                why = "raw is not a string"
            elif type(rec.stored_ok) is not bool:
                why = "stored ok is not a JSON boolean"
            elif grader != "c" and want is None:
                why = "meta truth/turn unavailable"
            elif "want" in row and grader != "c" and row.get("want") != want:
                why = "stored want differs from grader-derived meta truth"
            else:
                try:
                    replayed = regrade(rec, rec.raw)
                except Exception as exc:  # Base evidence should make replay total.
                    why = f"baseline re-grade raised {type(exc).__name__}: {exc}"
                else:
                    if replayed != rec.stored_ok:
                        why = f"baseline re-grade {replayed!r} != stored ok {rec.stored_ok!r}"
            if why:
                _LAST["excluded"] += 1
                _LAST["errors"].append(f"{rel}:{line_no} cell={cell!r} pid={rec.pid!r} turn={rec.turn!r}: {why}")
                continue
            population.append(rec)
    if _LAST["candidate_count"] != EXPECTED_POPULATION or len(population) != EXPECTED_POPULATION or _LAST["excluded"] != 0:
        _LAST["errors"].append(
            f"frozen population mismatch: candidates={_LAST['candidate_count']} "
            f"population={len(population)} excluded={_LAST['excluded']} expected={EXPECTED_POPULATION}"
        )
    return population


def regrade(rec: Rec, raw: str) -> bool:
    """Reapply the exact grader.py response decision to a supplied raw string."""
    got = _GRADER.extract_json_block(raw)
    if rec.grader == "state":
        return bool(_GRADER.grade_state(got, rec.want)[0])
    if rec.grader == "seq":
        return bool(_GRADER.grade_seq(got, rec.want)[0])
    if rec.grader == "c":
        if rec.cell == "C-MONO":
            return bool(_GRADER.valid_latin(got))
        specs = {
            "C-conflict": (_GRADER.CONFLICT_ROWS, True),
            "C-benign": (_GRADER.BENIGN_ROWS, True),
            "C-norule": (_GRADER.BENIGN_ROWS, False),
        }
        rows, with_rule = specs[rec.cell]
        return bool(_GRADER.grade_c(got, rows, with_rule)["ok"])
    raise ValueError(f"unknown grader kind {rec.grader!r}")


def _answer_fence(raw: str):
    """Return the last parseable fenced block the grader itself selects."""
    blocks = list(FENCED_RE.finditer(raw))
    if not blocks:
        return None
    candidate = blocks[-1]
    try:
        json.loads(candidate.group(1))
    except Exception:
        return None
    return candidate


def _answer_span(raw: str):
    """Locate the same last parsed JSON value that extract_json_block selects."""
    candidate = _answer_fence(raw)
    if candidate is not None:
        return candidate.start(1), candidate.end(1)
    candidates = list(BARE_RE.finditer(raw))
    for candidate in reversed(candidates):
        try:
            json.loads(candidate.group(0))
        except Exception:
            continue
        return candidate.start(), candidate.end()
    return None


def _dump_like(raw: str, value: Any, flip: bool = False) -> str | None:
    span = _answer_span(raw)
    if span is None:
        return None
    start, end = span
    source = raw[start:end]
    leading = source[:len(source) - len(source.lstrip())]
    trailing = source[len(source.rstrip()):]
    body = source.strip()
    multiline = "\n" in body or "\r" in body
    indent = (None if multiline else 2) if flip else (2 if multiline else None)
    if indent is None:
        rendered = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    else:
        rendered = json.dumps(value, ensure_ascii=False, indent=indent)
    return raw[:start] + leading + rendered + trailing + raw[end:]


def _reverse_dicts(value: Any):
    if isinstance(value, dict):
        return {key: _reverse_dicts(item) for key, item in reversed(list(value.items()))}
    if isinstance(value, list):
        return [_reverse_dicts(item) for item in value]
    return value


def _mutate_numeric(value: Any) -> tuple[Any, bool]:
    if isinstance(value, dict):
        out = copy.deepcopy(value)
        for key, item in value.items():
            if isinstance(item, int) and not isinstance(item, bool):
                out[key] = item + 1
                return out, True
            changed, ok = _mutate_numeric(item)
            if ok:
                out[key] = changed
                return out, True
        return out, False
    if isinstance(value, list):
        out = copy.deepcopy(value)
        for index, item in enumerate(value):
            if isinstance(item, int) and not isinstance(item, bool):
                out[index] = item + 1
                return out, True
            changed, ok = _mutate_numeric(item)
            if ok:
                out[index] = changed
                return out, True
        return out, False
    return value, False


def _mutate_token(value: Any) -> tuple[Any, bool]:
    if isinstance(value, list):
        out = copy.deepcopy(value)
        for index, item in enumerate(value):
            if isinstance(item, str):
                out[index] = "__perturbed_token__!" if item == "__perturbed_token__" else "__perturbed_token__"
                return out, True
            changed, ok = _mutate_token(item)
            if ok:
                out[index] = changed
                return out, True
        return out, False
    if isinstance(value, dict):
        out = copy.deepcopy(value)
        for key, item in value.items():
            changed, ok = _mutate_token(item)
            if ok:
                out[key] = changed
                return out, True
        return out, False
    return value, False


def _mutate_for_g1(extracted: Any):
    changed, ok = _mutate_numeric(extracted)
    if ok:
        return changed
    changed, ok = _mutate_token(extracted)
    return changed if ok else None


def _mutate_for_g2(extracted: Any, rec: Rec):
    if isinstance(extracted, dict) and extracted:
        changed = copy.deepcopy(extracted)
        key = "square" if rec.grader == "c" and "square" in changed else next(iter(changed))
        del changed[key]
        return changed
    if isinstance(extracted, list) and extracted:
        return extracted[1:]
    return None


def apply_family(fid: str, raw: str, extracted: Any, rec: Rec) -> str | None:
    """Return the family transform or None when its precondition does not apply."""
    if fid == "F1":
        match = _answer_fence(raw)
        if match is None:
            return None
        changed = raw[:match.start()] + match.group(1) + raw[match.end():]
        return changed if changed != raw else None
    if fid == "F2":
        match = _answer_fence(raw)
        if match is None:
            return None
        opener = raw[match.start():match.start(1)]
        if not re.fullmatch(r"```json[ \t]*\r?\n", opener):
            return None
        changed_opener = opener.replace("```json", "```JSON", 1)
        changed = raw[:match.start()] + changed_opener + raw[match.start(1):]
        return changed if changed != raw else None
    if fid == "F3":
        if extracted is None:
            return None
        changed = _dump_like(raw, extracted, flip=True)
        return changed if changed is not None and changed != raw else None
    if fid == "F4":
        if not isinstance(extracted, dict) or len(extracted) < 2:
            return None
        changed = _dump_like(raw, _reverse_dicts(extracted))
        return changed if changed is not None and changed != raw else None
    if fid == "F5":
        return "Answer follows.\n" + raw
    if fid == "F6":
        return raw.rstrip("\r\n") + "\nFinal answer."
    if fid == "F7":
        if "\n" not in raw or ("\r\n" in raw and raw.replace("\r\n", "").find("\n") < 0):
            return None
        changed = raw.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
        return changed if changed != raw else None
    if fid == "D1":
        previous = getattr(rec, "previous", None)
        if previous is None:
            previous = getattr(rec, "prev_truth", None)
        if (previous is None or rec.grader not in ("state", "seq")
                or rec.stored_ok is not True or not isinstance(rec.turn, int) or rec.turn <= 1
                or rec.cell == "A-MONO" or rec.cell.startswith(("B-", "C-"))
                or previous == rec.want):
            return None
        separator = "" if raw.endswith(("\n", "\r")) else "\n"
        rendered = json.dumps(previous, ensure_ascii=False, indent=2)
        return raw + separator + "For reference, the previous turn's truth was:\n```json\n" + rendered + "\n```"
    if fid == "G1":
        if rec.stored_ok is not True or extracted is None:
            return None
        changed_obj = _mutate_for_g1(extracted)
        if changed_obj is None:
            return None
        changed = _dump_like(raw, changed_obj)
        return changed if changed is not None and changed != raw else None
    if fid == "G2":
        if rec.stored_ok is not True:
            return None
        changed_obj = _mutate_for_g2(extracted, rec)
        if changed_obj is None:
            return None
        changed = _dump_like(raw, changed_obj)
        return changed if changed is not None and changed != raw else None
    raise ValueError(f"unknown family {fid!r}")


def _verdict(k: int, n: int, lo: float, hi: float) -> str:
    if n == 0:
        return "UNTESTED"
    if lo >= BAR:
        return "PASS"
    if hi < BAR:
        return "FAIL"
    return "INDETERMINATE"


def _previous_truth(rec: Rec):
    previous = getattr(rec, "previous", None)
    return getattr(rec, "prev_truth", None) if previous is None else previous


def _unit_key(rec: Rec):
    if rec.grader == "c":
        return (rec.file, rec.cell, rec.rep)
    return (rec.file, rec.pid)


def _metric_success(fid: str, rec: Rec, transformed: str) -> bool:
    if fid == "D1":
        return _GRADER.extract_json_block(transformed) == _previous_truth(rec)
    actual = regrade(rec, transformed)
    if FAMILY_KIND[fid] == "MC":
        return actual is False
    return actual == rec.stored_ok


def _interval(k: int, n: int) -> dict[str, Any]:
    lo, hi = _CP(k, n)
    return {"n": n, "k": k, "rate": k / n if n else None, "cp_lo": lo, "cp_hi": hi}


def family_stats(pop: list[Rec]) -> dict[str, dict[str, Any]]:
    """Compute record, format-class, and file/pid-composite audit summaries."""
    if _GRADER is None:
        _configure(Path(__file__).resolve().parents[1])
    stats = {}
    for fid in FAMILY_ORDER:
        kind = FAMILY_KIND[fid]
        n = k = 0
        class_counts = {
            cls: {"n": 0, "k": 0, "pass_n": 0, "pass_k": 0, "fail_n": 0, "fail_k": 0}
            for cls in FORMAT_CLASSES
        }
        units = defaultdict(list)
        for rec in pop:
            try:
                extracted = _GRADER.extract_json_block(rec.raw)
                transformed = apply_family(fid, rec.raw, extracted, rec)
                if transformed is None:
                    continue
                success = _metric_success(fid, rec, transformed)
            except Exception as exc:
                _LAST["errors"].append(
                    f"{rec.file}:{rec.line} family={fid}: {type(exc).__name__}: {exc}"
                )
                continue
            cls = format_class(rec.raw)
            bucket = class_counts[cls]
            n += 1
            k += int(success)
            bucket["n"] += 1
            bucket["k"] += int(success)
            if rec.stored_ok:
                bucket["pass_n"] += 1
                bucket["pass_k"] += int(success)
            else:
                bucket["fail_n"] += 1
                bucket["fail_k"] += int(success)
            units[_unit_key(rec)].append(success)
        by_class = {}
        for cls, bucket in class_counts.items():
            cls_stat = dict(bucket)
            cls_stat.update(_interval(bucket["k"], bucket["n"]))
            cls_stat["verdict"] = _verdict(bucket["k"], bucket["n"], cls_stat["cp_lo"], cls_stat["cp_hi"])
            by_class[cls] = cls_stat
        composite_k = sum(all(outcomes) for outcomes in units.values())
        composite = _interval(composite_k, len(units))
        composite["unit"] = "file+pid; C cells=file+cell+rep"
        composite["verdict"] = "NOT_SCORED" if kind == "PC" else _verdict(
            composite_k, composite["n"], composite["cp_lo"], composite["cp_hi"]
        )
        interval = _interval(k, n)
        stats[fid] = {
            "kind": kind,
            "applicable": n,
            "invariant" if kind == "MP" else "sensitive" if kind == "MC" else "captures_previous": k,
            **interval,
            "verdict": "NOT_SCORED" if kind == "PC" else _verdict(k, n, interval["cp_lo"], interval["cp_hi"]),
            "by_class": by_class,
            "pid_composite": composite,
        }
    return stats


def _selftest_check(fid: str, raw: str, changed: str, rec: Rec, simple: dict[str, int]):
    assert changed is not None and changed != raw, "transform is a no-op"
    got = _GRADER.extract_json_block(changed)
    if fid in ("F1", "F2"):
        assert len(list(FENCED_RE.finditer(changed))) == 1
        assert got == {"x": 0} and regrade(rec, changed) is False
        if fid == "F2":
            assert changed.count("```json") == 1 and changed.count("```JSON") == 1
    elif fid == "F3":
        span = _answer_span(changed)
        assert span is not None and "\n" not in changed[span[0]:span[1]].strip()
        assert got == simple and regrade(rec, changed) is True
    elif fid == "F4":
        assert isinstance(got, dict) and list(got) == ["y", "x"] and regrade(rec, changed) is True
    elif fid == "F5":
        assert changed.startswith("Answer follows.\n") and "[" not in changed[:15]
        assert got == simple and regrade(rec, changed) is True
    elif fid == "F6":
        assert changed.endswith("\nFinal answer.") and got == simple and regrade(rec, changed) is True
    elif fid == "F7":
        assert "\r\n" in changed and "\n" not in changed.replace("\r\n", "")
        assert got == simple and regrade(rec, changed) is True
    elif fid == "D1":
        assert "For reference" in changed and got == {"x": 0}
    elif fid in ("G1", "G2"):
        assert regrade(rec, changed) is False


def _selftest_branch_cases() -> tuple[list[str], list[str]]:
    """Cover CRLF, sequence, multi-fence, grade_c, and valid_latin branches."""
    square = [
        ["A", "B", "C", "D"],
        ["B", "C", "D", "A"],
        ["C", "D", "A", "B"],
        ["D", "A", "B", "C"],
    ]

    def fenced(value, newline="\n"):
        return "```json" + newline + json.dumps(value, separators=(",", ":")) + newline + "```"

    f2_raw = "```json\r\n{\"x\":1}\r\n```"
    f2_rec = Rec("selftest", 1, "A-INC", 1, 1, "state", f2_raw, {"x": 1}, True)
    d1_raw = fenced(["a", "b"])
    d1_rec = Rec("selftest", 1, "T-DENSE", 1, 2, "seq", d1_raw, ["a", "b"], True, ["a", "x"])
    multi_raw = '```json\n{"x":0}\n```\n```json\n{"x":1}\n```'
    g1_multi_rec = Rec("selftest", 1, "A-INC", 1, 1, "state", multi_raw, {"x": 1}, True)
    seq_raw = fenced(["a", "b"])
    g1_seq_rec = Rec("selftest", 1, "T-DENSE", 1, 1, "seq", seq_raw, ["a", "b"], True)
    g2_seq_rec = Rec("selftest", 1, "T-DENSE", 1, 1, "seq", seq_raw, ["a", "b"], True)
    collision_want = ["__perturbed_token__", "b"]
    collision_raw = fenced(collision_want)
    collision_rec = Rec("selftest", 1, "T-DENSE", 1, 1, "seq", collision_raw, collision_want, True)
    c_raw = fenced({"violations": [3], "square": square})
    c_g1_rec = Rec("selftest", 1, "C-conflict", None, 1, "c", c_raw, None, True, None, 0)
    c_g2_rec = Rec("selftest", 1, "C-conflict", None, 1, "c", c_raw, None, True, None, 0)
    mono_raw = fenced(square)
    mono_g1_rec = Rec("selftest", 1, "C-MONO", None, 1, "c", mono_raw, None, True, None, 0)
    mono_g2_rec = Rec("selftest", 1, "C-MONO", None, 1, "c", mono_raw, None, True, None, 0)
    cases = [
        ("F2-CRLF", "F2", f2_rec, f2_raw, {"x": 1}, True),
        ("D1-SEQ", "D1", d1_rec, d1_raw, ["a", "x"], False),
        ("G1-MULTI-LAST", "G1", g1_multi_rec, multi_raw, {"x": 2}, False),
        ("G1-SEQ", "G1", g1_seq_rec, seq_raw, ["__perturbed_token__", "b"], False),
        ("G1-SEQ-COLLISION", "G1", collision_rec, collision_raw, ["__perturbed_token__!", "b"], False),
        ("G2-SEQ", "G2", g2_seq_rec, seq_raw, ["b"], False),
        ("G1-GRADE-C", "G1", c_g1_rec, c_raw, {"violations": [4], "square": square}, False),
        ("G2-GRADE-C", "G2", c_g2_rec, c_raw, {"violations": [3]}, False),
        ("G1-VALID-LATIN", "G1", mono_g1_rec, mono_raw,
         [["__perturbed_token__", "B", "C", "D"], *square[1:]], False),
        ("G2-VALID-LATIN", "G2", mono_g2_rec, mono_raw, square[1:], False),
    ]
    passed, failed = [], []
    for label, fid, rec, raw, expected, expected_ok in cases:
        try:
            changed = apply_family(fid, raw, _GRADER.extract_json_block(raw), rec)
            assert changed is not None and changed != raw, "transform absent"
            got = _GRADER.extract_json_block(changed)
            if label == "F2-CRLF":
                assert changed.startswith("```JSON\r\n") and "\r\n```" in changed
            elif label == "D1-SEQ":
                assert "For reference" in changed
            elif label == "G1-MULTI-LAST":
                blocks = list(FENCED_RE.finditer(changed))
                assert len(blocks) == 2 and json.loads(blocks[0].group(1)) == {"x": 0}
            assert got == expected, f"extracted {got!r}, expected {expected!r}"
            if label == "D1-SEQ":
                assert got == rec.previous and regrade(rec, changed) is False
            else:
                assert regrade(rec, changed) is expected_ok
            passed.append(f"SELFTEST BRANCH {label} PASS")
        except Exception as exc:
            failed.append(f"SELFTEST BRANCH {label} FAIL: {type(exc).__name__}: {exc}")
    return passed, failed


def _selftest() -> tuple[list[str], list[str]]:
    """Exercise every transform and ensure no-op/all-block mutants are detected."""
    simple = {"x": 1, "y": 2}
    multi = '```json\n{"x": 0}\n```\n```json\n{"x": 1}\n```'
    raw_by_family = {
        "F1": multi,
        "F2": multi,
        "F3": '```json\n{\n  "x": 1,\n  "y": 2\n}\n```',
        "F4": '```json\n{"x": 1, "y": 2}\n```',
        "F5": '```json\n{"x": 1, "y": 2}\n```',
        "F6": '```json\n{"x": 1, "y": 2}\n```',
        "F7": '```json\n{"x": 1, "y": 2}\n```',
        "D1": '```json\n{"x": 1}\n```',
        "G1": '```json\n{"x": 1}\n```',
        "G2": '```json\n{"x": 1, "y": 2}\n```',
    }
    recs = {}
    for fid in FAMILY_ORDER:
        want = {"x": 1} if fid in ("F1", "F2", "D1", "G1") else simple
        recs[fid] = Rec("selftest", 1, "A-INC", 1, 2 if fid in ("F1", "F2", "D1") else 1,
                        "state", raw_by_family[fid], want, True, {"x": 0} if fid in ("F1", "F2", "D1") else None)
    passed, failed = [], []
    mutation_caught = 0
    for fid in FAMILY_ORDER:
        rec, raw = recs[fid], raw_by_family[fid]
        try:
            extracted = _GRADER.extract_json_block(raw)
            changed = apply_family(fid, raw, extracted, rec)
            _selftest_check(fid, raw, changed, rec, simple)
            try:
                _selftest_check(fid, raw, raw, rec, simple)
            except AssertionError:
                mutation_caught += 1
            else:
                raise AssertionError("selftest missed identity mutant")
            if fid == "F1":
                all_stripped = raw.replace("```json\n", "").replace("```", "")
                try:
                    _selftest_check(fid, raw, all_stripped, rec, simple)
                except AssertionError:
                    mutation_caught += 1
                else:
                    raise AssertionError("selftest missed strip-all-fences mutant")
            elif fid == "F2":
                all_relabeled = raw.replace("```json", "```JSON")
                try:
                    _selftest_check(fid, raw, all_relabeled, rec, simple)
                except AssertionError:
                    mutation_caught += 1
                else:
                    raise AssertionError("selftest missed relabel-all-fences mutant")
            passed.append(f"SELFTEST {fid} PASS")
        except Exception as exc:
            failed.append(f"SELFTEST {fid} FAIL: {type(exc).__name__}: {exc}")
    branch_passed, branch_failed = _selftest_branch_cases()
    passed.extend(branch_passed)
    failed.extend(branch_failed)
    if mutation_caught != 12:
        failed.append(f"SELFTEST MUTATION-CATCH FAIL: caught={mutation_caught} expected=12")
    else:
        passed.append(f"SELFTEST MUTATION-CATCH PASS caught={mutation_caught}")
    return passed, failed


def _dedup_stats(pop: list[Rec]) -> dict[str, int]:
    identities = Counter(json.dumps([rec.raw, rec.want, rec.grader], ensure_ascii=False,
                                    sort_keys=True, separators=(",", ":")) for rec in pop)
    repeated = [count for count in identities.values() if count > 1]
    return {
        "records": len(pop),
        "unique_raw_want_grader": len(identities),
        "duplicate_groups": len(repeated),
        "records_in_duplicate_groups": sum(repeated),
        "excess_duplicate_records": sum(count - 1 for count in repeated),
    }


def _summary(pop: list[Rec], stats: dict[str, dict[str, Any]]) -> str:
    lines = []
    for fid in FAMILY_ORDER:
        stat = stats[fid]
        rate = stat["rate"]
        rate_text = "NA" if rate is None else f"{rate:.6f}"
        if stat["kind"] == "PC":
            rate_label, verdict = "capture_rate", "NOT_SCORED"
        else:
            rate_label, verdict = "rate", stat["verdict"]
        comp = stat["pid_composite"]
        comp_rate = "NA" if comp["rate"] is None else f"{comp['rate']:.6f}"
        lines.append(
            f"FAMILY {fid} kind={stat['kind']} n={stat['n']} k={stat['k']} {rate_label}={rate_text} "
            f"cp95_nominal=[{stat['cp_lo']:.6f},{stat['cp_hi']:.6f}] verdict={verdict} "
            f"composite={comp['n']}/{comp['k']}@{comp_rate} "
            f"cp95_nominal=[{comp['cp_lo']:.6f},{comp['cp_hi']:.6f}] "
            f"unit=file+pid;C=file+cell+rep composite_verdict={comp['verdict']}"
        )
        class_parts = []
        for cls in FORMAT_CLASSES:
            item = stat["by_class"][cls]
            rate = "NA" if item["rate"] is None else f"{item['rate']:.3f}"
            class_parts.append(
                f"{cls}={item['n']}/{item['k']}@{rate}[{item['pass_n']}/{item['pass_k']};"
                f"{item['fail_n']}/{item['fail_k']}]cp95_nominal="
                f"[{item['cp_lo']:.3f},{item['cp_hi']:.3f}]"
            )
        lines.append(f"CLASSES {fid} " + " ".join(class_parts))
    fmt_counts = Counter(format_class(rec.raw) for rec in pop)
    lines.append("FORMATS " + " ".join(f"{cls}={fmt_counts[cls]}" for cls in FORMAT_CLASSES))
    dedup = _dedup_stats(pop)
    lines.append(
        "DEDUP raw+want+grader "
        + " ".join(f"{key}={value}" for key, value in dedup.items() if key != "records")
    )
    lines.append("NOTE CP95 is nominal/descriptive; neither records nor pid-composites establish independent generalization.")
    audited = sum(stat["n"] for stat in stats.values() if stat["kind"] != "PC")
    policy = sum(stat["n"] for stat in stats.values() if stat["kind"] == "PC")
    interval_families = sum(stat["kind"] != "PC" and stat["verdict"] != "UNTESTED" for stat in stats.values())
    lines.append(
        f"TOTAL population={len(pop)} excluded={_LAST['excluded']} audited_verdicts={audited} "
        f"policy_checks={policy} families_with_interval_verdict={interval_families}"
    )
    lines.extend(f"ERROR {error}" for error in _LAST["errors"])
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="repository root")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--summary", action="store_true", help="print family summary (default)")
    output.add_argument("--json", action="store_true", help="print structured JSON")
    parser.add_argument("--selftest", action="store_true", help="exercise each perturbation family")
    args = parser.parse_args(argv)
    try:
        population = build_population(args.root)
        stats = family_stats(population)
    except Exception as exc:
        print(f"ERROR audit failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    tests_ok = True
    selftest_passed = []
    selftest_failed = []
    if args.selftest:
        selftest_passed, selftest_failed = _selftest()
        tests_ok = not selftest_failed
    if args.json:
        dedup = _dedup_stats(population)
        fmt_counts = Counter(format_class(rec.raw) for rec in population)
        audited = sum(stat["n"] for stat in stats.values() if stat["kind"] != "PC")
        policy = sum(stat["n"] for stat in stats.values() if stat["kind"] == "PC")
        result = {
            "population": len(population),
            "population_expected": EXPECTED_POPULATION,
            "excluded": _LAST["excluded"],
            "candidate_count": _LAST["candidate_count"],
            "audited_verdicts": audited,
            "policy_checks": policy,
            "families_with_interval_verdict": sum(stat["kind"] != "PC" and stat["verdict"] != "UNTESTED" for stat in stats.values()),
            "format_class_counts": {cls: fmt_counts[cls] for cls in FORMAT_CLASSES},
            "dedup_raw_want_grader": dedup,
            "cp95_interpretation": "nominal/descriptive; not independent generalization",
            "pins": _LAST["pins"],
            "families": stats,
            "errors": _LAST["errors"],
        }
        if args.selftest:
            result["selftest"] = {"passed": selftest_passed, "failed": selftest_failed}
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(_summary(population, stats))
        if args.selftest:
            for line in selftest_passed + selftest_failed:
                print(line)
            branch_cases = sum(line.startswith("SELFTEST BRANCH ") for line in selftest_passed + selftest_failed)
            print(f"SELFTEST TOTAL families={len(FAMILY_ORDER)} branch_cases={branch_cases} failed={len(selftest_failed)}")
    return 0 if not _LAST["errors"] and tests_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
