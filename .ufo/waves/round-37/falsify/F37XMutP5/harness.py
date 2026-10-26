#!/usr/bin/env python3
"""F37XMutP5 harness: four NEW (non-frozen) mutants of clause P5 of plans/pkg_gate.py, run against the
round-37 full battery using the frozen counter's own machinery.

Imports plans/round37_c1_verify.py as a module (load_r36, Ctx, r36_fixtures, battery37_fixtures, run_gate),
builds every fixture once, runs the reference gate once, then runs each new mutant over the same built
fixtures. Observable per run is the counter's: (exit code, set of clause ids printed `DEFECT`). A mutant is
killed iff some fixture's observable differs from the reference; the first such fixture is its killer.
Additionally the P5 detail line (`bad=<n>`) is captured so a fixture's defect count can be inspected.

Usage: python3 harness.py --lane <clone> --work <scratch>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import py_compile
import re
import subprocess
import sys
import tempfile

CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) (.*)$")

# Four new mutants of c_captures (P5), each an exact old -> new pair that must occur once in the gate.
NEW_MUTANTS = [
    ("X1", "P5", "row loop applied to the first registry row only (check narrowed to one row)",
     '    for sid, row in p.spec["rows"].items():\n'
     '        name = row["capture"]\n'
     '        if name not in pinned:',
     '    for sid, row in list(p.spec["rows"].items())[:1]:\n'
     '        name = row["capture"]\n'
     '        if name not in pinned:'),
    ("X2", "P5", "bytes-vs-digest comparison inverted (`!=` -> `==`, the >=/> operator-flip class)",
     "        if sha256(capdir / name) != digest:",
     "        if sha256(capdir / name) == digest:"),
    ("X3", "P5", "uncovered-file sweep applied to the first directory entry only",
     "    for f in sorted(capdir.iterdir()):",
     "    for f in sorted(capdir.iterdir())[:1]:"),
    ("X4", "P5", "row branches reordered so the off-pin check shadows the unpinned check",
     '        if name not in pinned:\n'
     '            bad.append(f"{sid}: capture {name} is not pinned in the manifest")\n'
     '        elif pinned[name] != row["sha256"]:\n'
     '            bad.append(f"{sid}: manifest digest differs from the spec pin")',
     '        if pinned.get(name) != row["sha256"]:\n'
     '            bad.append(f"{sid}: manifest digest differs from the spec pin")\n'
     '        elif name not in pinned:\n'
     '            bad.append(f"{sid}: capture {name} is not pinned in the manifest")'),
]


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("kengaku_r37_c1", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_full(gate, spec_path, argv):
    """One gate run: (rc, frozenset of DEFECT clause ids, {clause: detail}) — the counter's observable plus notes."""
    try:
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                           capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return ("timeout", frozenset(), {})
    defects, notes = set(), {}
    for line in r.stdout.splitlines():
        m = CLAUSE_LINE.match(line)
        if not m:
            continue
        notes[m.group(1)] = (m.group(2), m.group(3))
        if m.group(2) == "DEFECT":
            defects.add(m.group(1))
    return (r.returncode, frozenset(defects), notes)


def bad_count(note):
    m = re.search(r"\bbad=(\d+)", note or "")
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--battery-dir", default=None, help="development: battery37 dir to load instead of the lane's")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c1 = load_counter(lane)
    gate_src = (lane / c1.GATE_REL).read_text()
    gate_digest = c1.sha256(lane / c1.GATE_REL)
    print(f"GATE {c1.GATE_REL} sha256={gate_digest} frozen={gate_digest == c1.GATE_SHA256}")
    r36 = c1.load_r36(lane)
    ctx = c1.Ctx(lane, r36)
    bdir = pathlib.Path(a.battery_dir).resolve() if a.battery_dir else lane / c1.BATTERY_REL
    fixtures = c1.r36_fixtures(r36) + c1.battery37_fixtures(bdir)
    print(f"BATTERY-DIR {bdir}")
    print(f"BATTERY fixtures={len(fixtures)} battery37={sum(1 for f in fixtures if not f.get('r36'))}")

    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-mutp5-", dir=a.work))
    try:
        built = []
        for i, fx in enumerate(fixtures):
            d = root / "fx" / f"f{i:03d}"
            d.mkdir(parents=True)
            argv = list(fx["build"](ctx, d))
            built.append((fx, d, argv))
        gdir = root / "gates"
        gdir.mkdir()
        ref_gate = gdir / "ref.py"
        ref_gate.write_text(gate_src)
        ref = [run_full(ref_gate, ctx.spec_path, argv) for _fx, _d, argv in built]

        # observation equivalence with the frozen counter's run_gate on the reference
        disagree = 0
        for j, (fx, _d, argv) in enumerate(built):
            if (ref[j][0], ref[j][1]) != c1.run_gate(ref_gate, ctx.spec_path, argv):
                disagree += 1
                print(f"OBSERVE-MISMATCH {fx['fid']}")
        print(f"OBSERVE reference vs plan-run_gate mismatches={disagree}")

        decl_wrong = 0
        for j, (fx, _d, _argv) in enumerate(built):
            if fx.get("r36"):
                continue
            want_rc = 0 if fx["expect"] == "accept" else 1
            ok = ref[j][0] == want_rc and ref[j][1] == frozenset(fx["defects"] or ())
            decl_wrong += not ok
            if not ok:
                print(f"DECL-WRONG {fx['fid']} rc={ref[j][0]} clauses={','.join(sorted(ref[j][1])) or '-'}")
        print(f"DECLARATIONS wrong={decl_wrong}")

        print("--- reference P5 detail per p5.py fixture (defect isolation) ---")
        isolation = []
        for j, (fx, _d, _argv) in enumerate(built):
            if fx.get("r36") or not fx["fid"].startswith("p5-"):
                continue
            note = ref[j][2].get("P5", ("-", ""))[1]
            n = bad_count(note)
            clauses = ",".join(sorted(ref[j][1])) or "-"
            print(f"ISOLATION {fx['fid']} rc={ref[j][0]} clauses={clauses} p5_bad={n} note={note}")
            isolation.append({"fid": fx["fid"], "rc": ref[j][0], "clauses": sorted(ref[j][1]),
                              "p5_bad": n, "note": note})

        results = []
        for mid, clause, label, old, new in NEW_MUTANTS:
            count = gate_src.count(old)
            if count != 1:
                print(f"MUTANT {mid} invalid old occurs {count}x -- {label}")
                results.append({"id": mid, "clause": clause, "label": label, "status": "invalid",
                                "old_occurrences": count})
                continue
            mg = gdir / f"{mid}.py"
            mg.write_text(gate_src.replace(old, new, 1))
            try:
                py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
            except py_compile.PyCompileError as e:
                print(f"MUTANT {mid} invalid(compile) {e} -- {label}")
                results.append({"id": mid, "clause": clause, "label": label, "status": "invalid(compile)"})
                continue
            killers, changed = [], 0
            for j, (fx, _d, argv) in enumerate(built):
                got = run_full(mg, ctx.spec_path, argv)
                if (got[0], got[1]) != (ref[j][0], ref[j][1]):
                    changed += 1
                    killers.append({"fid": fx["fid"], "rc": got[0],
                                    "clauses": sorted(got[1]),
                                    "p5_bad": bad_count(got[2].get("P5", ("-", ""))[1]),
                                    "ref_rc": ref[j][0], "ref_clauses": sorted(ref[j][1])})
            status = "killed" if killers else "SURVIVED"
            print(f"MUTANT {mid} {clause} {status} killers={len(killers)} first={killers[0]['fid'] if killers else '-'} -- {label}")
            for k in killers[:4]:
                print(f"    kill fx={k['fid']} rc={k['rc']} clauses={','.join(k['clauses']) or '-'} p5_bad={k['p5_bad']} (ref rc={k['ref_rc']} clauses={','.join(k['ref_clauses']) or '-'})")
            results.append({"id": mid, "clause": clause, "label": label, "status": status,
                            "killers": killers, "old": old, "new": new})
        print("--- summary ---")
        for r in results:
            print(f"SUMMARY {r['id']} {r['status']}")
        print("JSON " + json.dumps({"gate_sha256": gate_digest, "fixtures": len(built),
                                    "isolation": isolation, "mutants": results}))
        return 0
    finally:
        print(f"WORK {root}")


if __name__ == "__main__":
    sys.exit(main())
