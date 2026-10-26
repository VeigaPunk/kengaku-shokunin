#!/usr/bin/env python3
"""F37XMutP4 falsification harness: extra non-frozen mutants of clause P4 (plans/pkg_gate.py) run
against the full frozen round-37 battery, reusing the counter's own machinery.

Imports plans/round37_c1_verify.py as a module (load_r36, Ctx, r36_fixtures, battery37_fixtures,
run_gate, MUTANTS) from a CLONE of the tip; builds every fixture once; runs the reference gate and
each mutant over the built fixtures. Also reports, per p4 fixture, which of the 55 frozen mutants
change its observable result (isolation check) and the full P4 note text for the reason-level check.

Never writes to the lane: --lane must be the clone.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import py_compile
import shutil
import subprocess
import sys

# (id, label, old, new) -- each old must occur exactly once in the unedited gate
NEW_MUTANTS = [
    ("X1", "off-by-one: single-line quote (start==end) rejected as range outside",
     "elif q.start > q.end or q.end > len(lines):",
     "elif q.start >= q.end or q.end > len(lines):"),
    ("X2", "check applied to the first quote only",
     "    for q in p.quotes:\n",
     "    for q in p.quotes[:1]:\n"),
    ("X3", "unreadable-capture branch reordered behind the range check (None shadows it)",
     '        if lines is None:\n'
     '            bad.append(f"{q.capture}: unreadable capture")\n'
     '        elif q.start > q.end or q.end > len(lines):\n',
     '        if q.start > q.end or q.end > len(lines):\n'),
    ("X4", "verbatim check loosened to a whole-capture substring search (cited line ignored)",
     'elif q.text not in "\\n".join(lines[q.start - 1:q.end]):',
     'elif q.text not in "\\n".join(lines):'),
    ("X5", "verbatim comparison loosened to case-insensitive (off-battery extra)",
     'elif q.text not in "\\n".join(lines[q.start - 1:q.end]):',
     'elif q.text.lower() not in "\\n".join(lines[q.start - 1:q.end]).lower():'),
    ("X6", "off-by-one: one line past the capture accepted (lax +1, off-battery extra)",
     "q.end > len(lines):",
     "q.end > len(lines) + 1:"),
]


def load_counter(lane):
    p = lane / "plans/round37_c1_verify.py"
    spec = importlib.util.spec_from_file_location("k37_counter", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_full(ref_gate, spec_path, argv):
    r = subprocess.run([sys.executable, str(ref_gate), *argv, "--spec", str(spec_path)],
                       capture_output=True, text=True, timeout=900)
    return r.returncode, r.stdout


def p4_note(stdout):
    for line in stdout.splitlines():
        if line.startswith("P4 "):
            return line
    return "<no P4 line>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if pathlib.Path(subprocess.run(["git", "-C", str(lane), "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True, check=True).stdout.strip()).resolve() != lane:
        raise SystemExit("refusing: --lane is not its own git top-level")
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    k = load_counter(lane)
    gate_src = (lane / k.GATE_REL).read_text()
    gate_ok = k.sha256(lane / k.GATE_REL) == k.GATE_SHA256
    print(f"LANE {lane} gate_frozen={gate_ok}")
    r36 = k.load_r36(lane)
    ctx = k.Ctx(lane, r36)
    fixtures = k.r36_fixtures(r36) + k.battery37_fixtures(lane / k.BATTERY_REL)
    print(f"FIXTURES {len(fixtures)}")

    root = work / "build"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    built = []
    for i, fx in enumerate(fixtures):
        d = root / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        assert argv and argv[0] in ("package", "d4-line", "d5-line") and "--spec" not in argv, fx["fid"]
        built.append((fx, d, argv))

    gdir = work / "gates"
    gdir.mkdir(parents=True, exist_ok=True)
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    spec_path = ctx.spec_path

    ref = [k.run_gate(ref_gate, spec_path, argv) for _fx, _d, argv in built]
    null_gate = gdir / "null.py"
    null_gate.write_text(gate_src)
    null_detected = [built[j][0]["fid"] for j in range(len(built))
                     if k.run_gate(null_gate, spec_path, built[j][2]) != ref[j]]
    print(f"NULL null_detected={len(null_detected)} {null_detected}")

    p4_idx = [j for j, (fx, _d, _a) in enumerate(built) if fx["fid"].startswith("p4-")]
    print("P4_FIXTURES " + " ".join(f"{built[j][0]['fid']}=rc{ref[j][0]}/{{{','.join(sorted(ref[j][1]))}}}"
                                    for j in p4_idx))

    # reason text of P4 on the unreadable-capture fixture, reference gate
    cap_idx = [j for j in p4_idx if built[j][0]["fid"] == "p4-capture-unreadable"]
    ref_cap_note = p4_note(run_full(ref_gate, spec_path, built[cap_idx[0]][2])[1]) if cap_idx else "<absent>"
    ref_offline_note = None
    off_idx = [j for j in p4_idx if built[j][0]["fid"] == "p4-line-outside"]
    if off_idx:
        ref_offline_note = p4_note(run_full(ref_gate, spec_path, built[off_idx[0]][2])[1])

    # isolation: which frozen mutant changes each p4 fixture's observable
    iso = {built[j][0]["fid"]: [] for j in p4_idx}
    for mid, clause, label, old, new in k.MUTANTS:
        if gate_src.count(old) != 1:
            print(f"ISO {mid} anchor-absent")
            continue
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        for j in p4_idx:
            if k.run_gate(mg, spec_path, built[j][2]) != ref[j]:
                iso[built[j][0]["fid"]].append(mid)

    # new mutants over the full battery
    results = []
    for mid, label, old, new in NEW_MUTANTS:
        n = gate_src.count(old)
        rec = {"id": mid, "label": label, "old": old, "new": new, "anchor_count": n}
        if n != 1:
            rec.update(status="invalid", killed_by=[], differing=[])
            results.append(rec)
            print(f"NEWMUT {mid} INVALID anchor_count={n}")
            continue
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        try:
            py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        except py_compile.PyCompileError as e:
            rec.update(status="invalid(compile)", killed_by=[], differing=[], error=str(e)[:200])
            results.append(rec)
            print(f"NEWMUT {mid} INVALID compile")
            continue
        diff = []
        for j, (fx, _d, argv) in enumerate(built):
            got = k.run_gate(mg, spec_path, argv)
            if got != ref[j]:
                diff.append({"fid": fx["fid"], "ref": [ref[j][0], sorted(ref[j][1])],
                             "mut": [got[0], sorted(got[1])]})
        rec["differing"] = diff
        rec["killed_by"] = [d["fid"] for d in diff]
        rec["status"] = "killed" if diff else "SURVIVED"
        if mid == "X3" and cap_idx:
            rec["p4_note_mutant_on_capture_unreadable"] = p4_note(run_full(mg, spec_path, built[cap_idx[0]][2])[1])
        results.append(rec)
        print(f"NEWMUT {mid} {rec['status']} differing={len(diff)} by={rec['killed_by'][:8]}")

    out = {
        "lane": str(lane), "gate_sha256": k.sha256(lane / k.GATE_REL), "gate_frozen": gate_ok,
        "fixtures_total": len(built), "null_detected": null_detected,
        "p4_fixtures": {built[j][0]["fid"]: {"declared": built[j][0]["defects"],
                                             "observed_rc": ref[j][0],
                                             "observed_defects": sorted(ref[j][1])} for j in p4_idx},
        "p4_isolation_killing_frozen_mutants": iso,
        "mutant_clauses": {m[0]: m[1] for m in k.MUTANTS},
        "ref_p4_note_capture_unreadable": ref_cap_note,
        "ref_p4_note_line_outside": ref_offline_note,
        "new_mutants": results,
    }
    pathlib.Path(a.out).write_text(json.dumps(out, indent=1))
    killed = sum(r["status"] == "killed" for r in results)
    print(f"NEWMUTANTS killed={killed} survived={sum(r['status']=='SURVIVED' for r in results)} "
          f"invalid={sum(r['status'].startswith('invalid') for r in results)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
