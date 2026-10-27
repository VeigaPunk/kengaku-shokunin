#!/usr/bin/env python3
"""R46ExecC1Modules driver: prove each refusals46 module with the round-45 counter's OWN machinery.

Imports the BASE clone's `plans/round44_c1_verify.py` (builder) and `plans/round45_c1_verify.py`
(`build_module` / `run_fence` / `HARNESS`) unchanged — the exact detector of `PREDICATE C1 pass` — and runs every
module of MODDIR against the base fence (`plans/fixture_fence.py` @ 64ba8385, copied byte-for-byte). Per module it
prints the round-45 counter's own per-module rule (any ADMIT or ERROR -> LEAKED; else HUNG; else READ when the
fence's process tree opened a path outside d; else clean) so the conversion is judged by the rule, not by me.

usage: driver.py LANE ROOT MODDIR
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
    k44 = load(LANE / "plans/round44_c1_verify.py", "k44_r46_modules")
    c1 = load(LANE / "plans/round45_c1_verify.py", "c45_r46_modules")
    print(f"LANE {LANE} HEAD {__import__('subprocess').run(['git', '-C', str(LANE), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()}")
    print(f"FENCE plans/fixture_fence.py sha256={sha256(LANE / 'plans/fixture_fence.py')}")
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "harness.py").write_text(c1.HARNESS)
    (ROOT / "fence").mkdir(parents=True, exist_ok=True)
    fence_copy = ROOT / "fence" / "fixture_fence.py"
    fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
    print(f"FENCE-COPY sha256={sha256(fence_copy)}")
    mods = sorted(MODDIR.glob("f*.py"))
    print(f"MODULES {len(mods)}")
    allrows = {}
    for i, f in enumerate(mods):
        try:
            fxs = c1.build_module(k44, LANE, ROOT, f)
        except Exception as e:  # noqa: BLE001 — report, never crash the batch
            print(f"MODULE-BUILD-ERROR {f.name} {type(e).__name__}: {str(e)[:200]}")
            allrows[f.name] = None
            continue
        for j, fx in enumerate(fxs):
            v, why, opens = c1.run_fence(k44, LANE, ROOT, fence_copy, fx, i * 100 + j)
            print(f"FENCE-RUN {f.name} {fx['fid']} {v} opens={opens}" + (f" -- {why}" if why else ""))
            allrows.setdefault(f.name, []).append((v, opens))
    for f in mods:
        rows = allrows.get(f.name)
        if rows is None:
            print(f"MODULE {f.name} BUILD-ERROR")
            continue
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
        print(f"MODULE {f.name} {verdict} fixtures={len(rows)} admitted={n_adm} hung={n_hung} opens={n_open}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
