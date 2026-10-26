#!/usr/bin/env python3
"""F37XMutP7: four NEW (non-frozen) mutants of gate clause P7, run against the frozen full battery.

Reuses the frozen counter's machinery by importing plans/round37_c1_verify.py as a module:
load_r36, Ctx, r36_fixtures, battery37_fixtures. Builds every fixture ONCE, runs the reference gate
(copy of the frozen pkg_gate.py) and then each mutant over the same built trees.

A mutant is `killed` iff some fixture's observable result (exit code, DEFECT clause set) differs
from the reference; the killing fixture is the first such fixture in battery order (all are listed).

Not part of the frozen claim: survivors are battery limits, reported only.
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import py_compile
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

CLAUSE_LINE = re.compile(r"^(P\d+|D4|D5) (ok|DEFECT) ")

# (id, category, target branch, old, new) -- old must occur exactly once in plans/pkg_gate.py.
MUTANTS = [
    ("X1", "check applied to the first row only",
     "source line: for sid, row in p.spec['rows'].items()",
     '    for sid, row in p.spec["rows"].items():\n'
     '        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     '    for sid, row in list(p.spec["rows"].items())[:1]:\n'
     '        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:'),
    ("X2", "threshold removed (verified-at accepts any ISO date)",
     "verified-at: frozen-date substring test",
     '    if f"verified-at: {rules[\'verified_at\']}" not in p.entry:',
     '    if not re.search(r"^verified-at: \\d{4}-\\d{2}-\\d{2}", p.entry, re.M):'),
    ("X3", "branch reordered so another check shadows it",
     "recheck line: ^recheck: search",
     '    if not re.search(r"^recheck:\\s*\\S", p.entry, re.M):\n'
     '        bad.append("recheck line absent")',
     '    if not re.search(r"^## Negative space", p.entry, re.M) and not re.search(r"^recheck:\\s*\\S", p.entry, re.M):\n'
     '        bad.append("recheck line absent")'),
    ("X4", "regex loosened (empty recheck line accepted)",
     "recheck line: ^recheck:\\s*\\S",
     '    if not re.search(r"^recheck:\\s*\\S", p.entry, re.M):',
     '    if not re.search(r"^recheck:", p.entry, re.M):'),
]

# Supplementary diagnostic, NOT one of the four: narrow the source-line check to the second registry
# row (S106) only, to show whether the X1 kill rests on S105/S107 coverage or only on S106 coverage.
DIAGNOSTICS = [
    ("D1", "source line: second registry row only (S106)",
     '    for sid, row in p.spec["rows"].items():\n'
     '        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:',
     '    for sid, row in list(p.spec["rows"].items())[1:2]:\n'
     '        if prov.get(sid) != [p.spec["raw_base"] + row["upstream"]]:'),
]


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("k37_c1", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_gate_full(gate, spec_path, argv):
    """(exit code, DEFECT clause frozenset, stdout) -- same invocation as the frozen counter."""
    try:
        r = subprocess.run([sys.executable, str(gate), *argv, "--spec", str(spec_path)],
                           capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return ("timeout", frozenset(), "")
    bad = frozenset(m.group(1) for m in map(CLAUSE_LINE.match, r.stdout.splitlines())
                    if m and m.group(2) == "DEFECT")
    return (r.returncode, bad, r.stdout)


def p7_note(stdout):
    for line in stdout.splitlines():
        if line.startswith("P7 "):
            return line[len("P7 "):]
    return "(no P7 line)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    c = load_counter(lane)
    gate_path = lane / c.GATE_REL
    gate_src = gate_path.read_text()
    digest = c.sha256(gate_path)
    print(f"GATE sha256={digest} frozen={digest == c.GATE_SHA256}")

    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
    ids = [f["fid"] for f in fixtures]
    if len(set(ids)) != len(ids):
        print("SETUP duplicate fixture id", file=sys.stderr)
        return 2
    print(f"BATTERY fixtures={len(fixtures)} r36={sum(1 for f in fixtures if f.get('r36'))}")

    built = []
    root = work / "fx"
    for i, fx in enumerate(fixtures):
        d = root / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        built.append((fx, d, argv))

    gdir = work / "gates"
    gdir.mkdir(exist_ok=True)
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)

    def run_all(gate):
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(run_gate_full, gate, ctx.spec_path, argv) for _fx, _d, argv in built]
            return [f.result() for f in futs]

    ref = run_all(ref_gate)
    wrong = 0
    for (fx, _d, _a), (rc, bad, out) in zip(built, ref):
        want_rc = 0 if fx["expect"] == "accept" else 1
        declared = fx.get("defects")
        ok = rc == want_rc and (declared is None or bad == frozenset(declared))
        if fx["expect"] == "accept":
            ok = ok and not bad
        if not fx.get("r36") and (declared is None or fx["expect"] not in ("accept", "reject")):
            ok = False
        if not ok:
            wrong += 1
        if fx["fid"].startswith("p7-"):
            print(f"P7FIXTURE {fx['fid']} declared={','.join(sorted(declared)) if declared else '-'} "
                  f"observed_rc={rc} defects={','.join(sorted(bad)) or '-'} "
                  f"p7='{p7_note(out)}' {'ok' if ok else 'WRONG'}")
    print(f"REFERENCE wrong={wrong}")

    def evaluate(mid, old, new):
        if gate_src.count(old) != 1:
            print(f"MUTANT {mid} INVALID old occurs {gate_src.count(old)} times")
            return None
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        try:
            py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        except py_compile.PyCompileError as e:
            print(f"MUTANT {mid} INVALID compile {e}")
            return None
        res = run_all(mg)
        hits = [fx["fid"] for (fx, _d, _a), r0, r1 in zip(built, ref, res)
                if (r0[0], r0[1]) != (r1[0], r1[1])]
        if hits:
            j = [i for i, ((fx, _d, _a), r0, r1) in enumerate(zip(built, ref, res))
                 if (r0[0], r0[1]) != (r1[0], r1[1])][0]
            r0, r1 = ref[j], res[j]
            print(f"DELTA {mid} on {hits[0]} ref=(rc={r0[0]},defects={','.join(sorted(r0[1])) or '-'}) "
                  f"mutant=(rc={r1[0]},defects={','.join(sorted(r1[1])) or '-'})")
        return hits

    print("--- designated extra mutants (killed<k>/4) ---")
    killed = 0
    for mid, cat, branch, old, new in MUTANTS:
        hits = evaluate(mid, old, new)
        if hits is None:
            continue
        state = "killed" if hits else "SURVIVED"
        killed += bool(hits)
        print(f"MUTANT {mid} {state} by={','.join(hits) if hits else '-'} -- {cat} [{branch}]")
    print(f"EXTRA total={len(MUTANTS)} killed={killed} survived={len(MUTANTS) - killed}")

    print("--- supplementary diagnostic (not counted) ---")
    for mid, cat, old, new in DIAGNOSTICS:
        hits = evaluate(mid, old, new)
        if hits is None:
            continue
        print(f"DIAG {mid} {'killed' if hits else 'SURVIVED'} by={','.join(hits) if hits else '-'} -- {cat}")

    # Witness trees for the two survivors: a tree the reference gate rejects on P7, built from the
    # genuine package with the one edit the battery is supposed to cover but does not.
    def witness(name, edit, mutant):
        d = work / "witness" / name
        d.mkdir(parents=True)
        ctx.genuine_package(d)
        entry = d / ctx.spec["entry"]
        before = entry.read_text()
        after = edit(before)
        if after == before:
            print(f"WITNESS {name} SETUP edit was a no-op")
            return
        entry.write_text(after)
        ctx.git_add(d)
        argv = ["package", "--root", str(d), "--require-clean-tree"]
        r0 = run_gate_full(ref_gate, ctx.spec_path, argv)
        r1 = run_gate_full(gdir / f"{mutant}.py", ctx.spec_path, argv)
        print(f"WITNESS {name} ref_rc={r0[0]} ref_defects={','.join(sorted(r0[1])) or '-'} "
              f"ref_p7='{p7_note(r0[2])}' | {mutant}_rc={r1[0]} "
              f"{mutant}_defects={','.join(sorted(r1[1])) or '-'} {mutant}_p7='{p7_note(r1[2])}'")

    witness("empty-recheck-line",
            lambda text: re.sub(r"(?m)^recheck:.*$", "recheck:", text, count=1), "X4")
    witness("s105-source-url-changed",
            lambda text: text.replace(
                "protein-assembly/tests/test_outputs.py",
                "protein-assembly/tests/test_outputs_other.py", 1), "D1")
    # X4 shape the battery lacks: the recheck line moved to the end with its instruction emptied, so
    # the reference rejects (no non-space after "recheck:") while X4 accepts. Proves X4 is killable.
    def recheck_last(text):
        lines = text.splitlines()
        kept = [l for l in lines if not l.startswith("recheck:")]
        if len(kept) != len(lines) - 1:
            raise RuntimeError("expected exactly one recheck line")
        return "\n".join(kept + ["recheck:"]) + "\n"
    witness("recheck-last-line-empty", recheck_last, "X4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
