#!/usr/bin/env python3
"""R45HoCommondir2 held-out driver.

Builds MY hostile modules with the frozen round-44 builder (plans/round44_c1_verify.py, imported unchanged)
and runs the LANED fence through the frozen round-45 counter's own `build_module`/`run_fence`
(plans/round45_c1_verify.py), exactly as its main() does — one module at a time, same sandboxes, same
strace counting. Nothing in the lane is read-modified; the lane is only imported and byte-copied.

usage: driver.py LANE ROOT MODDIR     (K45_KEEP_STRACE honoured by run_fence)
"""
import hashlib
import importlib.util
import pathlib
import sys


def load(p, n):
    spec = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    LANE = pathlib.Path(sys.argv[1]).resolve()
    ROOT = pathlib.Path(sys.argv[2]).resolve()
    MODDIR = pathlib.Path(sys.argv[3]).resolve()
    k44 = load(LANE / "plans/round44_c1_verify.py", "k44_holdout_driver")
    c1 = load(LANE / "plans/round45_c1_verify.py", "c45_holdout_driver")
    print(f"LANE {LANE}")
    print(f"FENCE plans/fixture_fence.py sha256={sha256(LANE / 'plans/fixture_fence.py')}")
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "harness.py").write_text(c1.HARNESS)
    (ROOT / "fence").mkdir(parents=True, exist_ok=True)
    fence_copy = ROOT / "fence" / "fixture_fence.py"
    fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
    print(f"FENCE-COPY sha256={sha256(fence_copy)}")
    mods = sorted(MODDIR.glob("g*_*.py"))
    if len(mods) != 4:
        print(f"SETUP expected 4 held-out modules, found {[f.name for f in mods]}")
        return 2
    allrows = {}
    for i, f in enumerate(mods):
        try:
            fxs = c1.build_module(k44, LANE, ROOT, f)
        except Exception as e:  # noqa: BLE001 — report, do not crash the batch
            print(f"HELDOUT-BUILD-ERROR {f.name} {type(e).__name__}: {str(e)[:200]}")
            continue
        for j, fx in enumerate(fxs):
            v, why, opens = c1.run_fence(k44, LANE, ROOT, fence_copy, fx, i * 10 + j)
            print(f"FENCE-RUN {f.name} {fx['fid']} {v} opens={opens}" + (f" -- {why}" if why else ""))
            allrows.setdefault(f.name, []).append((v, opens))
    for f in mods:
        rows = allrows.get(f.name, [])
        n_adm = sum(v in ("ADMIT", "ERROR") for v, _o in rows)
        n_hung = sum(v == "HUNG" for v, _o in rows)
        n_open = sum(o for _v, o in rows)
        if not rows or n_adm:
            verdict = "LEAKED"
        elif n_hung:
            verdict = "HUNG"
        elif n_open:
            verdict = "READ"
        else:
            verdict = "clean"
        print(f"HELDOUT {f.name} {verdict} fixtures={len(rows)} admitted={n_adm} hung={n_hung} opens={n_open}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
