#!/usr/bin/env python3
"""Do the surviving mutants L1/L2/L3 have a cheap fixture that would kill them?

Builds three candidate fixtures that are NOT in the frozen battery and runs the reference gate plus
the L1/L2/L3 gate variants over them:
  A  genuine package, `--rerun` (kills L2: P10 always rejects)
  B  one receipt byte flipped on output line 5, not line 1 (kills L3: first-line-only comparison)
  C  probe edited to append one trailing space to byte-identical output (kills L1: rstrip tolerance)

  python3 correction_check.py --lane <clone> --work <scratch>
"""
import argparse
import importlib.util
import pathlib
import shutil
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    c = load(lane / "plans/round37_c1_verify.py", "k37_counter")
    p910 = load(lane / "plans/battery37/p910.py", "k37_p910")
    gate_src = (lane / c.GATE_REL).read_text()
    if c.sha256(lane / c.GATE_REL) != c.GATE_SHA256:
        print("gate not at freeze digest", file=sys.stderr)
        return 2
    r36 = c.load_r36(lane)
    ctx = c.Ctx(lane, r36)
    root = pathlib.Path(a.work).resolve() / "corr"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    gdir = root / "gates"
    gdir.mkdir()
    ref_gate = gdir / "ref.py"
    ref_gate.write_text(gate_src)
    variants = {}

    def genuine(d):
        ctx.genuine_package(d)
        p910._ignore_rule(ctx, d)

    # A
    dA = root / "A"
    dA.mkdir()
    genuine(dA)
    ctx.git_add(dA)
    variants["A genuine+rerun"] = (dA, p910._argv(dA, rerun=True))
    # B: flip a byte on receipt line 5 (line 1 untouched)
    dB = root / "B"
    dB.mkdir()
    genuine(dB)
    rc = dB / ctx.spec["receipt"]
    lines = rc.read_text().splitlines(keepends=True)
    i = lines[4].index("nt=2586") + len("nt=25")
    lines[4] = lines[4][:i] + ("7" if lines[4][i] != "7" else "6") + lines[4][i + 1:]
    rc.write_text("".join(lines))
    ctx.git_add(dB)
    variants["B byte-off-line5"] = (dB, p910._argv(dB, rerun=True))
    # C: probe prints byte-identical output plus one trailing space
    dC = root / "C"
    dC.mkdir()
    genuine(dC)
    probe = dC / "plans/tb2_grader_probe.py"
    text = probe.read_text()
    old = 'if __name__ == "__main__":\n    sys.exit(main())\n'
    new = ('if __name__ == "__main__":\n    _rc = main()\n    print(" ", end="")\n    sys.exit(_rc)\n')
    assert text.count(old) == 1
    probe.write_text(text.replace(old, new, 1))
    ctx.git_add(dC)
    variants["C trailing-space"] = (dC, p910._argv(dC, rerun=True))

    ref = {k: c.run_gate(ref_gate, ctx.spec_path, v[1]) for k, v in variants.items()}
    for k, res in ref.items():
        print(f"REF {k:20s} rc={res[0]} defects={','.join(sorted(res[1])) or '-'}")
    MUT = {
        "L1": ('if r.stdout != want:\n        return False, "fresh probe output is not byte-equal to the receipt"',
               'if r.stdout.rstrip() != want.rstrip():\n        return False, "fresh probe output is not byte-equal to the receipt"'),
        "L2": ('return True, f"probe_rerun=byte-equal bytes={len(want)}"',
               'return False, f"probe_rerun=byte-equal bytes={len(want)}"'),
        "L3": ('if r.stdout != want:\n        return False, "fresh probe output is not byte-equal to the receipt"',
               'if r.stdout.splitlines()[:1] != want.splitlines()[:1]:\n        return False, "fresh probe output is not byte-equal to the receipt"'),
    }
    for mid, (old, new) in MUT.items():
        assert gate_src.count(old) == 1, mid
        mg = gdir / f"{mid}.py"
        mg.write_text(gate_src.replace(old, new, 1))
        flips = [k for k, v in variants.items() if c.run_gate(mg, ctx.spec_path, v[1]) != ref[k]]
        print(f"MUT {mid} flips={','.join(flips) or 'NONE'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
