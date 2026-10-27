#!/usr/bin/env python3
"""Name-independence control: copy each built fixture to a fresh random-token tree and re-run the fence on it.
Neither the parent directory name, the fixture directory name, nor the sibling count carries information here."""
import importlib.util, json, pathlib, secrets, shutil, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
LANE = pathlib.Path(sys.argv[1]).resolve(); ROOT = pathlib.Path(sys.argv[2]).resolve()
MODS = [pathlib.Path(p).resolve() for p in sys.argv[3:]]
k44 = load(LANE / "plans/round44_c1_verify.py", "k44_rn"); c1 = load(LANE / "plans/round45_c1_verify.py", "k45_rn")
fence = load(LANE / "plans/fixture_fence.py", "fence_rn")
for n in ("fx", "btmp", "mods", "empty"): (ROOT / n).mkdir(parents=True, exist_ok=True)
(ROOT / "harness.py").write_text(c1.HARNESS)
ok = bad = 0
for f in MODS:
    for fx in c1.build_module(k44, LANE, ROOT, f):
        tok = secrets.token_hex(8)
        newdir = ROOT / "rand" / tok / tok
        newdir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(fx["dir"], newdir, symlinks=True)
        v = fence.breach(newdir, fx["argv"], fx["tool"])
        tag = "BREACH" if v else "ADMIT"
        print(f"RANDOM {f.name} {fx['fid']} orig={json.dumps(fx['argv'])[:60]} -> {tag} -- {v or '-'}")
print(f"RANDOM-TOTAL fixtures={ok+bad}")
