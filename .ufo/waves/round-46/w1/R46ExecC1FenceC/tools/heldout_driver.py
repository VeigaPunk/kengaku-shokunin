#!/usr/bin/env python3
"""Replica of the round-45 counter path for held-out modules: c1.build_module + c1.run_fence, same sandboxes.
usage: heldout_driver.py LANE ROOT MODULE..."""
import hashlib, importlib.util, pathlib, sys

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

LANE = pathlib.Path(sys.argv[1]).resolve()
ROOT = pathlib.Path(sys.argv[2]).resolve()
MODS = [pathlib.Path(p).resolve() for p in sys.argv[3:]]
k44 = load(LANE / "plans/round44_c1_verify.py", "k44_ho")
c1 = load(LANE / "plans/round45_c1_verify.py", "k45_ho")
print(f"LANE {LANE}")
print(f"FENCE sha256={hashlib.sha256((LANE / 'plans/fixture_fence.py').read_bytes()).hexdigest()}")
ROOT.mkdir(parents=True, exist_ok=True)
(ROOT / "harness.py").write_text(c1.HARNESS)
(ROOT / "fence").mkdir(exist_ok=True)
fence_copy = ROOT / "fence" / "fixture_fence.py"
fence_copy.write_bytes((LANE / "plans/fixture_fence.py").read_bytes())
for i, f in enumerate(MODS):
    rel = str(f)
    try:
        fxs = c1.build_module(k44, LANE, ROOT, f)
    except Exception as e:  # noqa: BLE001
        print(f"HELDOUT-BUILD-ERROR {rel} {type(e).__name__}: {str(e)[:200]}")
        continue
    rows = []
    for j, fx in enumerate(fxs):
        v, why, opens = c1.run_fence(k44, LANE, ROOT, fence_copy, fx, i * 100 + j)
        print(f"FENCE-RUN {rel} {fx['fid']} {v} opens={opens}" + (f" -- {why}" if why else ""))
        rows.append((v, opens))
    n_adm = sum(v in ("ADMIT", "ERROR") for v, _ in rows)
    n_hung = sum(v == "HUNG" for v, _ in rows)
    n_open = sum(o for _, o in rows)
    if not rows or n_adm: verdict = "LEAKED"
    elif n_hung: verdict = "HUNG"
    elif n_open: verdict = "READ"
    else: verdict = "clean"
    print(f"HELDOUT {rel} {verdict} fixtures={len(rows)} admitted={n_adm} hung={n_hung} opens={n_open}")
