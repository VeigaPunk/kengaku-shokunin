#!/usr/bin/env python3
"""Extraction-policy comparison on the frozen round-26 response population (round 27, C1).

Responses and graders stay fixed; only the answer-extraction policy varies. E0..E8 are the
pre-registered table in plans/round-27-claims.md, each a pure function of the raw response.
Population, pins and per-record grader dispatch come from plans/grader_perturb.py; the exact
Clopper-Pearson interval comes from plans/attrib_calibration.py. Offline, stdlib only.

    python3 plans/parser_policy_compare.py [--root DIR] [--summary|--json] [--selftest]

Exit 0: ran, and the pins and the E0 baseline reproduce. Exit 1: pin/baseline inconsistency, a
policy or grader exception (a defect, never counted as FAIL), or selftest failure. Exit 2: usage.
CP95 is a descriptive exact interval over these records, not a guarantee for future responses.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import tempfile
from collections import OrderedDict
from contextlib import redirect_stdout
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import grader_perturb as gp  # noqa: E402  pins, population, regrade dispatch, format_class
import policy_cases  # noqa: E402  hand-expected bounded synthetic cases
from attrib_calibration import clopper_pearson  # noqa: E402


FENCE_ANY = re.compile(r"```[A-Za-z0-9_+-]*[ \t]*\r?\n(.*?)```", re.S)
DECODER = json.JSONDecoder()


# ---------- extraction policies: raw -> parsed value | None (none reads want, ok or the grader) ----------
def _loads(text):
    try:
        return True, json.loads(text)
    except Exception:  # grader.py:126 treats every parse failure alike
        return False, None


def _bare_last(raw):
    for cand in reversed(gp.BARE_RE.findall(raw)):
        ok, value = _loads(cand)
        if ok:
            return value
    return None


def e0_lane(raw):
    """grader.py:121-134: last fenced block if it parses, else last parseable bare candidate."""
    blocks = gp.FENCED_RE.findall(raw)
    if blocks:
        ok, value = _loads(blocks[-1])
        if ok:
            return value
    return _bare_last(raw)


def e1_first_fence(raw):
    blocks = gp.FENCED_RE.findall(raw)
    if blocks:
        ok, value = _loads(blocks[0])
        if ok:
            return value
    return _bare_last(raw)


def e2_bare_last(raw):
    return _bare_last(raw)


def e3_bare_first(raw):
    for cand in gp.BARE_RE.findall(raw):
        ok, value = _loads(cand)
        if ok:
            return value
    return None


def e4_strict_whole(raw):
    ok, value = _loads(raw.strip())
    return value if ok else None


def e5_fence_only(raw):
    blocks = gp.FENCED_RE.findall(raw)
    if blocks:
        ok, value = _loads(blocks[-1])
        if ok:
            return value
    return None


def e6_any_label_fence(raw):
    blocks = FENCE_ANY.findall(raw)
    if blocks:
        ok, value = _loads(blocks[-1])
        if ok:
            return value
    return _bare_last(raw)


def e7_decode_first(raw):
    for i, ch in enumerate(raw):
        if ch in "{[":
            try:
                return DECODER.raw_decode(raw, i)[0]
            except Exception:
                continue
    return None


def e8_decode_last(raw):
    last = None
    i = 0
    while i < len(raw):
        if raw[i] in "{[":
            try:
                value, end = DECODER.raw_decode(raw, i)
            except Exception:
                i += 1
                continue
            last = value
            i = end  # starts inside an already-decoded top-level span are not candidates
        else:
            i += 1
    return last


POLICIES = OrderedDict([
    ("E0", e0_lane),
    ("E1", e1_first_fence),
    ("E2", e2_bare_last),
    ("E3", e3_bare_first),
    ("E4", e4_strict_whole),
    ("E5", e5_fence_only),
    ("E6", e6_any_label_fence),
    ("E7", e7_decode_first),
    ("E8", e8_decode_last),
])
NAMES = {
    "E0": "lane", "E1": "first-fence", "E2": "bare-last", "E3": "bare-first", "E4": "strict-whole",
    "E5": "fence-only", "E6": "any-label-fence", "E7": "decode-first", "E8": "decode-last",
}


# ---------- per-record grading: grader_perturb.regrade verbatim, with only its extractor replaced ----------
class _FixedExtraction:
    """Stands in for grader_perturb._GRADER so that regrade() grades the supplied value."""

    def __init__(self, real, value):
        self._real = real
        self._value = value

    def extract_json_block(self, _text):
        return self._value

    def __getattr__(self, name):
        return getattr(self._real, name)


def grade_value(rec, value):
    real = gp._GRADER
    gp._GRADER = _FixedExtraction(real, value)
    try:
        return bool(gp.regrade(rec, rec.raw))
    finally:
        gp._GRADER = real


def _canon(value):
    return json.dumps(value, sort_keys=True)


def _short(rel):
    path = Path(rel)
    return f"{path.parent.name}/{path.name}"


def _rate(counts):
    return counts["pass"] / counts["n"] if counts["n"] else 0.0


def tally(population, results, pid):
    t = {"n": 0, "pass": 0, "agree": 0, "flip_pf": 0, "flip_fp": 0, "none": 0,
         "strata": {c: {"n": 0, "agree": 0, "pass": 0} for c in gp.FORMAT_CLASSES},
         "files": {}, "cells": {}}
    for rec, cell in zip(population, results[pid]):
        if cell is None:
            continue
        value, verdict = cell
        agree = verdict == rec.stored_ok
        t["n"] += 1
        t["pass"] += int(verdict)
        t["agree"] += int(agree)
        t["none"] += int(value is None)
        if not agree:
            t["flip_pf" if rec.stored_ok else "flip_fp"] += 1
        stratum = t["strata"][gp.format_class(rec.raw)]
        stratum["n"] += 1
        stratum["agree"] += int(agree)
        stratum["pass"] += int(verdict)
        for bucket in (t["files"].setdefault(rec.file, {"n": 0, "pass": 0}),
                       t["cells"].setdefault((rec.file, rec.cell), {"n": 0, "pass": 0})):
            bucket["n"] += 1
            bucket["pass"] += int(verdict)
    return t


def _population_failure(root, population):
    """Structured failure report; changed/unpinned inputs never reach a policy."""
    ids = list(POLICIES)
    return {
        "root": str(root),
        "population": len(population),
        "pins": gp._LAST["pins"],
        "defects": [f"POPULATION {msg}" for msg in gp._LAST["errors"]],
        "policies": [],
        "strata": {},
        "files": {},
        "cells": {},
        "cellshift": {pid: {"max_abs_pp": 0.0, "cell": None} for pid in ids if pid != "E0"},
        "matrix": {"ids": ids, "rows": [[0] * len(ids) for _ in ids]},
        "total": {
            "population": len(population),
            "policies": len(ids) - 1,
            "compared_verdicts": 0,
            "disagreements": 0,
            "policies_with_flips": 0,
        },
        "exit": 1,
    }


def compute(root):
    population = gp.build_population(root)
    if gp._LAST["errors"]:
        return _population_failure(root, population)

    defects = []
    results = {pid: [None] * len(population) for pid in POLICIES}
    for idx, rec in enumerate(population):
        where = f"{rec.file}:{rec.line} cell={rec.cell}"
        lane = gp._GRADER.extract_json_block(rec.raw)
        for pid, policy in POLICIES.items():
            try:
                value = policy(rec.raw)
            except Exception as exc:  # a raising policy is a defect, never a FAIL
                defects.append(f"POLICY-RAISE {pid} {where}: {type(exc).__name__}: {exc}")
                continue
            try:
                verdict = grade_value(rec, value)
            except Exception as exc:  # a raising grader is a defect, never a FAIL
                defects.append(f"GRADER-RAISE {pid} {where}: {type(exc).__name__}: {exc}")
                continue
            results[pid][idx] = (value, verdict)
            if pid == "E0" and _canon(value) != _canon(lane):
                defects.append(f"BASELINE E0 != grader.extract_json_block {where}")

    tallies = {pid: tally(population, results, pid) for pid in POLICIES}
    base = tallies["E0"]
    if base["n"] != gp.EXPECTED_POPULATION or base["agree"] != base["n"]:
        defects.append(f"BASELINE E0 agree={base['agree']} of n={base['n']} "
                       f"(expected {gp.EXPECTED_POPULATION} of {gp.EXPECTED_POPULATION})")

    ids = list(POLICIES)
    order = sorted(base["cells"], key=lambda key: (gp.POPULATION_FILES.index(key[0]), key[1]))

    def cell_shift(pid):
        best_pp, best_key = -1.0, None
        for key in order:
            mine = tallies[pid]["cells"].get(key)
            if mine is None:
                continue
            pp = abs(_rate(mine) - _rate(base["cells"][key])) * 100.0
            if pp > best_pp:
                best_pp, best_key = pp, key
        cell = f"{_short(best_key[0])}:{best_key[1]}" if best_key else None
        return {"max_abs_pp": max(best_pp, 0.0), "cell": cell}

    policies, strata, files, cells = [], {}, {}, {}
    for pid in ids:
        t = tallies[pid]
        lo, hi = clopper_pearson(t["agree"], t["n"])
        policies.append({
            "id": pid, "name": NAMES[pid], "n": t["n"], "agree": t["agree"],
            "flip_pf": t["flip_pf"], "flip_fp": t["flip_fp"], "none": t["none"], "pass": t["pass"],
            "pass_rate": _rate(t), "delta_pp": (_rate(t) - _rate(base)) * 100.0,
            "cp95_lo": lo, "cp95_hi": hi,
        })
        strata[pid] = {cls: dict(v, pass_rate=_rate(v)) for cls, v in t["strata"].items()}
        files[pid] = {rel: dict(v, pass_rate=_rate(v)) for rel, v in t["files"].items()}
        cells[pid] = {f"{_short(f)}:{c}": dict(v, pass_rate=_rate(v)) for (f, c), v in t["cells"].items()}

    matrix = [[0] * len(ids) for _ in ids]
    for idx in range(len(population)):
        row = [results[pid][idx] for pid in ids]
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if row[i] is not None and row[j] is not None and row[i][1] != row[j][1]:
                    matrix[i][j] += 1
                    matrix[j][i] += 1

    alt = [pid for pid in ids if pid != "E0"]
    flips = {pid: tallies[pid]["flip_pf"] + tallies[pid]["flip_fp"] for pid in alt}
    total = {
        "population": len(population),
        "policies": len(alt),
        "compared_verdicts": sum(tallies[pid]["n"] for pid in alt),
        "disagreements": sum(flips.values()),
        "policies_with_flips": sum(1 for pid in alt if flips[pid]),
    }
    return {
        "root": str(root), "population": len(population), "pins": gp._LAST["pins"],
        "defects": defects, "policies": policies, "strata": strata, "files": files, "cells": cells,
        "cellshift": {pid: cell_shift(pid) for pid in alt},
        "matrix": {"ids": ids, "rows": matrix}, "total": total,
        "exit": 1 if defects else 0,
    }


def render(res):
    lines = [f"DEFECT {msg}" for msg in res["defects"][:100]]
    if len(res["defects"]) > 100:
        lines.append(f"DEFECT ... {len(res['defects']) - 100} more (see --json)")
    for p in res["policies"]:
        lines.append(
            f"POLICY {p['id']} name={p['name']} n={p['n']} agree={p['agree']} flip_pf={p['flip_pf']} "
            f"flip_fp={p['flip_fp']} none={p['none']} pass={p['pass']} pass_rate={p['pass_rate']:.4f} "
            f"delta_pp={p['delta_pp']:+.2f} cp95_lo={p['cp95_lo']:.6f} cp95_hi={p['cp95_hi']:.6f}")
    for pid, classes in res["strata"].items():
        for cls, s in classes.items():
            lines.append(f"STRATUM {pid} {cls} n={s['n']} agree={s['agree']}")
    for pid, s in res["cellshift"].items():
        lines.append(f"CELLSHIFT {pid} max_abs_pp={s['max_abs_pp']:.2f} cell={s['cell']}")
    ids = res["matrix"]["ids"]
    lines.append("MATRIX cols " + " ".join(ids))
    for pid, row in zip(ids, res["matrix"]["rows"]):
        lines.append(f"MATRIX row {pid} " + " ".join(str(v) for v in row))
    t = res["total"]
    lines.append(f"TOTAL population={t['population']} policies={t['policies']} "
                 f"compared_verdicts={t['compared_verdicts']} disagreements={t['disagreements']} "
                 f"policies_with_flips={t['policies_with_flips']}")
    return lines


# ---------- selftest: probes written from the table text; every seeded mutant must be killed ----------
PROBES = {
    "E0": [
        ("fence-last-wins", '```json\n{"a": 1}\n```\nmid\n```json\n{"a": 2}\n```', {"a": 2}),
        ("bad-last-fence-to-bare", '```json\n{"a": 1}\n```\n```json\nnot json\n```\n{"b": 3}', {"b": 3}),
        ("no-fence-bare-last", 'x {"a": 1} y {"b": 2}', {"b": 2}),
        ("python-fence-not-json", '```python\n{"a": 1}\n```\n{"b": 2}', {"b": 2}),
        ("parsing-fence-beats-bare", '```json\n{"a": 1}\n```\n{"b": 2}', {"a": 1}),
    ],
    "E1": [
        ("first-fence-wins", '```json\n{"a": 1}\n```\n```json\n{"a": 2}\n```', {"a": 1}),
        ("bad-first-fence-to-bare", '```json\nxx\n```\n```json\n{"a": 2}\n```\n{"c": 3}', {"c": 3}),
        ("no-fence-bare-last", '{"a": 1} {"b": 2}', {"b": 2}),
    ],
    "E2": [
        ("fence-agnostic-last", '```json\n{"a": 1}\n```\n{"b": 2}', {"b": 2}),
        ("unparseable-last-skipped", '{"a": 1} {x: 2}', {"a": 1}),
        ("array-candidate", '[1, 2] {"a": 3}', {"a": 3}),
    ],
    "E3": [
        ("first-candidate-wins", '{"a": 1} {"b": 2}', {"a": 1}),
        ("unparseable-first-skipped", '{x: 2} {"b": 3}', {"b": 3}),
    ],
    "E4": [
        ("whole-json", '{"a": 1}', {"a": 1}),
        ("strip-form-feed", '\x0c{"a": 1}\x0c', {"a": 1}),
        ("prose-rejected", 'answer: {"a": 1}', None),
        ("fenced-rejected", '```json\n{"a": 1}\n```', None),
    ],
    "E5": [
        ("fence-parses", '```json\n{"a": 1}\n```', {"a": 1}),
        ("no-fence-no-fallback", '{"a": 1}', None),
        ("bad-fence-no-fallback", '```json\nxx\n```\n{"b": 2}', None),
    ],
    "E6": [
        ("any-label-fence-wins", '```python\n{"a": 1}\n```\n{"b": 2}', {"a": 1}),
        ("bad-label-fence-to-bare", '```text\nxx\n```\n{"b": 2}', {"b": 2}),
        ("json-fence", '```json\n{"a": 1}\n```', {"a": 1}),
        ("two-distinct-any-label-fences", '```python\n{"a": 1}\n```\n```json\n{"a": 2}\n```', {"a": 2}),
    ],
    "E7": [
        ("deep-nesting-outermost", 'prefix {"a": {"b": {"c": {"d": 1}}}} tail',
         {"a": {"b": {"c": {"d": 1}}}}),
        ("array-first", 'x [1, 2] {"a": 1}', [1, 2]),
        ("failed-start-skipped", '{bad {"a": 1}', {"a": 1}),
        ("no-brackets", 'no json here', None),
    ],
    "E8": [
        ("last-top-level", '{"a": 1} {"b": 2}', {"b": 2}),
        ("contained-span-skipped", '{"a": {"b": 1}}', {"a": {"b": 1}}),
        ("array-last", '{"a": 1} x [1]', [1]),
        ("no-brackets", 'nothing', None),
    ],
}




def _mutant_e4_no_strip(raw):
    ok, value = _loads(raw)
    return value if ok else None
def _mutant_e6_first_fence(raw):
    blocks = FENCE_ANY.findall(raw)
    if blocks:
        ok, value = _loads(blocks[0])
        if ok:
            return value
    return _bare_last(raw)




def _mutant_e7_bare_bounded(raw):
    for match in gp.BARE_RE.finditer(raw):
        try:
            return DECODER.raw_decode(raw, match.start())[0]
        except Exception:
            continue
    return None


def _mutant_e8_contained_reuse(raw):
    last = None
    for i, ch in enumerate(raw):
        if ch in "{[":
            try:
                last = DECODER.raw_decode(raw, i)[0]
            except Exception:
                continue
    return last


MUTANTS = OrderedDict([
    ("E0", ("E0-no-bare-fallback", e5_fence_only)),
    ("E1", ("E1-swapped-to-last-fence", e0_lane)),
    ("E2", ("E2-fence-leak", e0_lane)),
    ("E3", ("E3-order-reversed", e2_bare_last)),
    ("E4", ("E4-strip-omitted", _mutant_e4_no_strip)),
    ("E5", ("E5-fallback-leak", e0_lane)),
    ("E6", ("E6-label-restricted", e0_lane)),
    ("E7", ("E7-nesting-limited", _mutant_e7_bare_bounded)),
    ("E8", ("E8-contained-span-reuse", _mutant_e8_contained_reuse)),
])
EXTRA_MUTANTS = [
    ("E6", "E6-first-any-label-fence", _mutant_e6_first_fence),
]


def _differs(fn, raw, want):
    try:
        return _canon(fn(raw)) != _canon(want)
    except Exception:
        return True

def _selftest_policy_cases(out):
    failures = []
    for pid, name, raw, expected in policy_cases.CASES:
        try:
            actual = POLICIES[pid](raw)
            if _canon(actual) != _canon(expected):
                failures.append(f"{pid}/{name}: got {actual!r}, expected {expected!r}")
        except Exception as exc:
            failures.append(f"{pid}/{name}: raised {type(exc).__name__}: {exc}")
    print(f"SELFTEST {'FAIL' if failures else 'pass'} hand_cases={len(policy_cases.CASES)} "
          f"failed={failures}", file=out)
    return failures


def _selftest_pin_rejection(out):
    """Mutate a pinned file and prove both CLI modes reject before any policy runs."""
    source = Path(__file__).resolve().parents[1]
    poisoned_calls = []
    saved_policies = POLICIES.copy()

    def poisoned(_raw):
        poisoned_calls.append(True)
        raise AssertionError("policy ran before pin rejection")

    try:
        with tempfile.TemporaryDirectory(prefix="r27-policy-pin-") as temp:
            root = Path(temp)
            for rel in gp.POPULATION_FILES:
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / rel, target)
            for rel in ("grader.py", "plans/attrib_calibration.py"):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / rel, target)
            with (root / gp.POPULATION_FILES[0]).open("ab") as stream:
                stream.write(b"\n")

            for pid in POLICIES:
                POLICIES[pid] = poisoned
            summary_stream = io.StringIO()
            with redirect_stdout(summary_stream):
                summary_rc = main(["--root", str(root), "--summary"])
            json_stream = io.StringIO()
            with redirect_stdout(json_stream):
                json_rc = main(["--root", str(root), "--json"])
    except Exception as exc:
        print(f"SELFTEST FAIL pin-reject-before-policies raised={type(exc).__name__}: {exc}", file=out)
        return False
    finally:
        POLICIES.clear()
        POLICIES.update(saved_policies)

    summary = summary_stream.getvalue().splitlines()
    json_result = json.loads(json_stream.getvalue())
    pin_error = any("sha256" in msg for msg in json_result["defects"])
    ok = (summary_rc == 1 and json_rc == 1 and pin_error and not poisoned_calls
          and not json_result["policies"] and summary
          and summary[0].startswith("DEFECT POPULATION ")
          and summary[-1].startswith("TOTAL population="))
    print(f"SELFTEST {'pass' if ok else 'FAIL'} pin-reject-before-policies "
          f"summary_rc={summary_rc} json_rc={json_rc} pin_error={pin_error} "
          f"policy_calls={len(poisoned_calls)}", file=out)
    return ok


def selftest(out):
    failures = killed = 0
    for pid, policy in POLICIES.items():
        failed = [name for name, raw, want in PROBES[pid] if _differs(policy, raw, want)]
        failures += len(failed)
        status = "FAIL" if failed else "pass"
        print(f"SELFTEST {status} policy={pid} probes={len(PROBES[pid])} failed={failed}", file=out)
        mutant_name, mutant = MUTANTS[pid]
        by = next((name for name, raw, want in PROBES[pid] if _differs(mutant, raw, want)), None)
        if by is None:
            failures += 1
            print(f"SELFTEST SURVIVED {pid} mutant={mutant_name}", file=out)
        else:
            killed += 1
            print(f"SELFTEST KILLED {pid} mutant={mutant_name} by={by}", file=out)
    for pid, mutant_name, mutant in EXTRA_MUTANTS:
        by = next((name for name, raw, want in PROBES[pid] if _differs(mutant, raw, want)), None)
        if by is None:
            failures += 1
            print(f"SELFTEST SURVIVED {pid} mutant={mutant_name}", file=out)
        else:
            killed += 1
            print(f"SELFTEST KILLED {pid} mutant={mutant_name} by={by}", file=out)
    failures += len(_selftest_policy_cases(out))
    failures += int(not _selftest_pin_rejection(out))
    mutants = len(MUTANTS) + len(EXTRA_MUTANTS)
    print(f"SELFTEST total policies={len(POLICIES)} cases={len(policy_cases.CASES)} "
          f"mutants={mutants} killed={killed} failures={failures}", file=out)
    return 1 if failures else 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="parser_policy_compare.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]),
                    help="repository root holding grader.py, plans/ and corpus/ (default: this checkout)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--summary", action="store_true", help="one line per policy, then a TOTAL line (default)")
    mode.add_argument("--json", action="store_true", help="full machine-readable result")
    ap.add_argument("--selftest", action="store_true",
                    help="kill seeded mutants with probes; alone, runs only the selftest")
    args = ap.parse_args(argv)
    rc = 0
    if args.selftest:
        rc = selftest(sys.stderr if args.json else sys.stdout)
        if not (args.summary or args.json):
            return rc
    try:
        res = compute(Path(args.root))
    except Exception as exc:  # unreadable grader or population: setup failure, not a verdict
        print(f"ERROR audit failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        for line in render(res):
            print(line)
    return max(rc, res["exit"])


if __name__ == "__main__":
    sys.exit(main())
