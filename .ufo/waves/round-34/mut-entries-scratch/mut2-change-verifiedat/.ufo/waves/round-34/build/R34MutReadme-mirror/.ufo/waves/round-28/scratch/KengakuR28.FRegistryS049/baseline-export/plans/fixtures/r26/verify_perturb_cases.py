#!/usr/bin/env python3
"""Verify the R26 synthetic perturbation oracle against grader.py and grader_perturb.py.

Usage: python3 plans/fixtures/r26/verify_perturb_cases.py --root DIR [--cases PATH]
--root selects a tree containing grader.py and plans/grader_perturb.py (the integrated
instrument). --cases defaults to the sibling perturb_cases.jsonl.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

C_SPECS_NAMES = {"C-conflict": ("CONFLICT_ROWS", True),
                 "C-benign": ("BENIGN_ROWS", True),
                 "C-norule": ("BENIGN_ROWS", False)}
FAMILIES = ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "D1", "G1", "G2")
FIXTURE_REL = "plans/fixtures/r26/perturb_cases.jsonl"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def grade(grader, case: dict, raw: str):
    got = grader.extract_json_block(raw)
    if case["grader"] == "state":
        ok = grader.grade_state(got, case["want"])[0]
    elif case["grader"] == "seq":
        ok = grader.grade_seq(got, case["want"])[0]
    elif case["grader"] == "c" and case["cell"] == "C-MONO":
        ok = grader.valid_latin(got)
    elif case["grader"] == "c":
        rows_name, with_rule = C_SPECS_NAMES[case["cell"]]
        ok = grader.grade_c(got, getattr(grader, rows_name), with_rule)["ok"]
    else:
        raise ValueError(f"unknown grader {case['grader']!r}")
    return got, bool(ok)


def expected_outcome(case: dict, regraded_ok: bool, metric_success):
    if not case["applicable"]:
        return "n/a"
    if case["kind"] == "PC":
        return "captured" if metric_success else "not-captured"
    if case["kind"] == "MP":
        return "invariant" if regraded_ok == case["baseline_ok"] else "flip"
    if case["kind"] == "MC":
        return "detected" if regraded_ok is False else "missed"
    raise ValueError(f"unknown kind {case['kind']!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path,
                        help="tree containing grader.py and plans/grader_perturb.py")
    parser.add_argument("--cases", type=Path,
                        help="fixture JSONL (default: this script's sibling perturb_cases.jsonl)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    cases_path = (args.cases or Path(__file__).with_name("perturb_cases.jsonl")).resolve()
    grader_path = root / "grader.py"
    core_path = root / "plans" / "grader_perturb.py"
    for required in (grader_path, core_path, cases_path):
        if not required.is_file():
            print(f"ERROR missing required file: {required}", file=sys.stderr)
            return 2
    try:
        grader = load_module("_r26_fixture_grader", grader_path)
        core = load_module("_r26_fixture_core", core_path)
        core._configure(root)
        with cases_path.open(encoding="utf-8") as stream:
            cases = [json.loads(line) for line in stream if line.strip()]
    except Exception as exc:
        print(f"ERROR loading verifier inputs: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    failures = []
    seen_ids = set()
    for line, case in enumerate(cases, 1):
        cid = case.get("id", f"line-{line}")
        if cid in seen_ids:
            failures.append((cid, "duplicate id"))
        seen_ids.add(cid)
        if case.get("file") != FIXTURE_REL or case.get("line") != line:
            failures.append((cid, "file/line identity"))
        if case.get("fid") not in FAMILIES:
            failures.append((cid, "unknown family"))
            continue
        if case.get("kind") != core.FAMILY_KIND[case["fid"]]:
            failures.append((cid, "family kind differs from live core"))
        try:
            baseline_got, baseline_ok = grade(grader, case, case["raw"])
        except Exception as exc:
            failures.append((cid, f"baseline grade raised {type(exc).__name__}: {exc}"))
            continue
        if baseline_got != case.get("baseline_got") or baseline_ok != case.get("baseline_ok"):
            failures.append((cid, "baseline extraction/regrade mismatch"))
        if baseline_ok != case.get("stored_ok"):
            failures.append((cid, "stored_ok differs from baseline"))

        try:
            transformed = case.get("perturbed")
            if case["applicable"]:
                if not isinstance(transformed, str):
                    failures.append((cid, "applicable case lacks perturbed text"))
                    continue
                regraded_got, regraded_ok = grade(grader, case, transformed)
                if (regraded_got != case.get("regraded_got")
                        or regraded_ok != case.get("regraded_ok")):
                    failures.append((cid, "expected regrade mismatch"))
                metric_success = (grader.extract_json_block(transformed) == case["prev_truth"]
                                  if case["kind"] == "PC" else None)
                if metric_success != case.get("metric_success"):
                    failures.append((cid, "expected PC capture metric mismatch"))
                outcome = expected_outcome(case, regraded_ok, metric_success)
                if outcome != case.get("outcome"):
                    failures.append((cid, f"outcome {case.get('outcome')!r} != {outcome!r}"))
                expected_counted = case["kind"] in ("MP", "PC") or baseline_ok is True
                if bool(case.get("counted")) != expected_counted:
                    failures.append((cid, "counted flag mismatch"))
            else:
                if (transformed is not None or case.get("regraded_got") is not None
                        or case.get("regraded_ok") is not None or case.get("metric_success") is not None):
                    failures.append((cid, "inapplicable case contains transformed expectations"))
                if case.get("outcome") != "n/a" or case.get("counted") is not False:
                    failures.append((cid, "inapplicable outcome/count mismatch"))

            rec = core.Rec(case["file"], case["line"], case["cell"], case["pid"], case["turn"],
                           case["grader"], case["raw"], case["want"], case["stored_ok"],
                           previous=case.get("prev_truth"), rep=case.get("rep"))
            extracted = grader.extract_json_block(case["raw"])
            applied = core.apply_family(case["fid"], case["raw"], extracted, rec)
            if case["scope"] == "family":
                if (applied is not None) != bool(case["applicable"]):
                    failures.append((cid, "live apply_family applicability mismatch"))
                if case["applicable"] and applied != case["perturbed"]:
                    failures.append((cid, "live apply_family transform differs from fixture"))
                if case["applicable"]:
                    live_metric = core._metric_success(case["fid"], rec, applied)
                    expected_metric = (case["metric_success"] if case["kind"] == "PC"
                                       else (case["regraded_ok"] == case["baseline_ok"]
                                             if case["kind"] == "MP"
                                             else case["regraded_ok"] is False))
                    if live_metric != expected_metric:
                        failures.append((cid, "live core metric differs from fixture outcome"))
        except Exception as exc:
            failures.append((cid, f"verification raised {type(exc).__name__}: {exc}"))

    print(f"CASES total={len(cases)} unique_ids={len(seen_ids)} family_checked="
          f"{sum(c.get('scope') == 'family' for c in cases)} instance_regrade_checked="
          f"{sum(c.get('scope') == 'instance' for c in cases)} failures={len(failures)}")
    for item in failures:
        print("FAIL", item)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
