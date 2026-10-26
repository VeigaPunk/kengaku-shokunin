#!/usr/bin/env python3
"""Non-frozen P9/P10 mutants of plans/pkg_gate.py run over the frozen round-37 C1 battery.

Reuses the counter's machinery by importing plans/round37_c1_verify.py as a module
(load_r36, Ctx, r36_fixtures, battery37_fixtures, run_gate): the fixtures are built once and the
reference gate plus every mutant is measured against exactly those fixture directories, which is
how the counter itself attributes kills.

  python3 harness.py --lane <clone> --work <scratch> [--keep]

Prints, per mutant: `killed by=<fid>[+n]` or `SURVIVED`, and a final tally. Exit 0 when every
mutant is valid and the reference matches every fixture declaration.
"""
import argparse
import hashlib
import importlib.util
import pathlib
import py_compile
import shutil
import sys

# (id, clause, intent, old, new). Every `old` must occur exactly once in the frozen gate text.
MUTANTS = [
    ("X1", "P9", "untracked tolerance off-by-one: exactly one untracked file counts as clean",
     'return not left, f"untracked={len(left)} first={left[0] if left else 0}"',
     'return len(left) < 2, f"untracked={len(left)} first={left[0] if left else 0}"'),
    ("X2", "P9", "loosened guard: git's fatal exit 128 (not a repository) is exempted",
     'if r.returncode != 0:\n        return False, "root is not a readable git worktree"',
     'if r.returncode not in (0, 128):\n        return False, "root is not a readable git worktree"'),
    ("X3", "P10", "exit-status check narrowed to signals only: a non-zero exit is not a failure",
     'if r.returncode != 0:\n        return False, f"fresh probe exit={r.returncode} stderr={r.stderr.strip()[:80]!r}"',
     'if r.returncode < 0:\n        return False, f"fresh probe exit={r.returncode} stderr={r.stderr.strip()[:80]!r}"'),
    ("X4", "P9", "loosened exclusion: an untracked *.py file counts as clean",
     'left = [x for x in r.stdout.splitlines() if x]',
     'left = [x for x in r.stdout.splitlines() if x and not x.endswith(".py")]'),
    # Limit probes: expected to survive; each names a property the battery never exercises.
    ("L3", "P10", "byte-equality compared on the first output line only",
     'if r.stdout != want:\n        return False, "fresh probe output is not byte-equal to the receipt"',
     'if r.stdout.splitlines()[:1] != want.splitlines()[:1]:\n        return False, "fresh probe output is not byte-equal to the receipt"'),
    ("L1", "P10", "byte-equality tolerant of trailing whitespace",
     'if r.stdout != want:\n        return False, "fresh probe output is not byte-equal to the receipt"',
     'if r.stdout.rstrip() != want.rstrip():\n        return False, "fresh probe output is not byte-equal to the receipt"'),
    ("L2", "P10", "P10 rejects even the byte-equal success path",
     'return True, f"probe_rerun=byte-equal bytes={len(want)}"',
     'return False, f"probe_rerun=byte-equal bytes={len(want)}"'),
]


def load_counter(lane):
    spec = importlib.util.spec_from_file_location("k37_counter", lane / "plans/round37_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c = load_counter(lane)
    gate_src = (lane / c.GATE_REL).read_text()
    frozen = c.sha256(lane / c.GATE_REL) == c.GATE_SHA256
    print(f"GATE {c.GATE_REL} sha256={'frozen' if frozen else 'NOT-AT-FREEZE-DIGEST'}")
    if not frozen:
        return 2
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    fixtures = c.r36_fixtures(r36) + c.battery37_fixtures(lane / c.BATTERY_REL)
    root = pathlib.Path(a.work).resolve() / "fxroot"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True, exist_ok=True)
    built, wrong = [], 0
    for i, fx in enumerate(fixtures):
        d = root / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        if "--spec" in argv or not argv or argv[0] not in ("package", "d4-line", "d5-line"):
            print(f"SETUP fixture {fx['fid']} returned a forbidden argv", file=sys.stderr)
            return 2
        built.append((fx, d, argv))
    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    ref = []
    for fx, d, argv in built:
        res = c.run_gate(ref_gate, ctx.spec_path, argv)
        ref.append(res)
        want_rc = 0 if fx["expect"] == "accept" else 1
        declared = fx.get("defects")
        if not fx.get("r36") and (declared is None or fx.get("expect") not in ("accept", "reject")):
            ok = False
        else:
            ok = res[0] == want_rc and (declared is None or res[1] == frozenset(declared))
        if fx["expect"] == "accept":
            ok = ok and not res[1]
        wrong += not ok
    print(f"BATTERY fixtures={len(built)} wrong={wrong}")
    # P10 reachability: which fixtures actually run the re-run clause at all.
    reaching = [fx["fid"] for (fx, d, argv), res in zip(built, ref) if "--rerun" in argv]
    print(f"P10-exercised fixtures={len(reaching)} {','.join(reaching) or '-'}")
    ok_reaching = [fx["fid"] for (fx, d, argv), res in zip(built, ref) if "--rerun" in argv and "P10" not in res[1]]
    print(f"P10-passing fixtures={len(ok_reaching)} {','.join(ok_reaching) or '-'}")
    killed = survived = invalid = 0
    for mid, clause, intent, old, new in MUTANTS:
        if gate_src.count(old) != 1:
            invalid += 1
            print(f"MUTANT {mid} {clause} invalid -- anchor occurs {gate_src.count(old)}x -- {intent}")
            continue
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        try:
            py_compile.compile(str(mg), doraise=True, cfile=str(gdir / f"{mid}.pyc"))
        except py_compile.PyCompileError:
            invalid += 1
            print(f"MUTANT {mid} {clause} invalid(compile) -- {intent}")
            continue
        digest = hashlib.sha256(mg.read_bytes()).hexdigest()
        hits = []
        for j, (fx, d, argv) in enumerate(built):
            if c.run_gate(mg, ctx.spec_path, argv) != ref[j]:
                hits.append(fx["fid"])
        if hashlib.sha256(mg.read_bytes()).hexdigest() != digest:
            invalid += 1
            print(f"MUTANT {mid} {clause} invalid(mutant file changed during the run) -- {intent}")
            continue
        if hits:
            killed += 1
            print(f"MUTANT {mid} {clause} killed by={hits[0]}{'+%d' % (len(hits) - 1) if len(hits) > 1 else ''} -- {intent}")
            print(f"  killers {mid}: {','.join(hits)}")
        else:
            survived += 1
            print(f"MUTANT {mid} {clause} SURVIVED -- {intent}")
    print(f"MUTANTS total={len(MUTANTS)} killed={killed} survived={survived} invalid={invalid}")
    if a.keep:
        print(f"KEPT {root}")
    return 0 if (wrong == 0 and invalid == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
