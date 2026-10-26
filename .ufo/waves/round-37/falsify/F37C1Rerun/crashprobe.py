#!/usr/bin/env python3
"""Falsify the frozen C1 kill criterion. The counter kills a mutant on the FIRST fixture whose result
(exit code, set of clauses printing DEFECT) differs from the unmodified gate's. Question: when that
first difference is a GATE CRASH (traceback / exit 2 / timeout) rather than a fixture the gate
rejects, the "kill" demonstrates no advertised clause. Prints one line per anomalous first-kill."""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

lane = pathlib.Path(sys.argv[1]).resolve()
work = pathlib.Path(sys.argv[2]).resolve()
CL = re.compile(r"^([A-Z]+\d+)\s+DEFECT\b")

spec = importlib.util.spec_from_file_location("c", lane / "plans/round37_c1_verify.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

gate_src = (lane / c.GATE_REL).read_text()
assert c.sha256(lane / c.GATE_REL) == c.GATE_SHA256, "gate not at freeze digest"
r36 = c.load_r36(lane)
ctx = c.Ctx(lane, r36)
fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
root = pathlib.Path(tempfile.mkdtemp(prefix="k37-crash-", dir=work))
try:
    built = []
    for i, fx in enumerate(fixtures):
        d = root / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        built.append((fx, d, list(fx["build"](ctx, d))))
    gdir = root / "gates"; gdir.mkdir()
    ref_gate = gdir / "ref.py"; ref_gate.write_text(gate_src)

    def run(gate, argv):
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(ctx.spec_path)],
                           capture_output=True, text=True, timeout=900)
        bad = frozenset(m.group(1) for m in map(c.CLAUSE_LINE.match, r.stdout.splitlines())
                        if m and m.group(2) == "DEFECT")
        return (r.returncode, bad), r

    ref = [run(ref_gate, argv)[0] for _fx, _d, argv in built]
    crash = exit2 = clause_gone = unrelated = survived = 0
    for mid, clause, label, old, new in c.MUTANTS:
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        by = None
        for j, (fx, _d, argv) in enumerate(built):
            res, r = run(mg, argv)
            if res == ref[j]:
                continue
            by = (fx["fid"], res, r)
            break
        if by is None:
            survived += 1
            print(f"SURVIVED {mid} {clause} -- {label}")
            continue
        fid, res, r = by
        tb = "Traceback (most recent call last)" in r.stderr
        if tb or res[0] not in (0, 1):
            crash += 1
            tail = [l for l in r.stderr.strip().splitlines() if l.strip()][-1:] or ["(no stderr)"]
            print(f"CRASHKILL {mid} {clause} by={fid} rc={res[0]} err={tail[0][:90]} -- {label}")
        elif clause in res[1]:
            unrelated += 1
            print(f"NOTTHE-CLAUSE {mid} {clause} by={fid} rc={res[0]} still={sorted(res[1])}")
        else:
            clause_gone += 1
    print(f"PROBE mutants={len(c.MUTANTS)} clause_gone={clause_gone} crashkill={crash} "
          f"clause_still_reported={unrelated} survived={survived}")
finally:
    shutil.rmtree(root, ignore_errors=True)
