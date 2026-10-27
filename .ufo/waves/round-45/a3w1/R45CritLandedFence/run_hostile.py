import importlib.util
import json
import os
import pathlib
import shutil

BASE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r45/R45CritLandedFence")
OUT = BASE / ".ufo/waves/round-45/a3w1/R45CritLandedFence"
LANE = S / "lane"
ROOT = S / "hostile-run"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


shutil.rmtree(ROOT, ignore_errors=True)
ROOT.mkdir(parents=True)
(ROOT / "fence").mkdir()
(ROOT / "empty").mkdir()
(ROOT / "strace").mkdir()
(ROOT / "harness.py").write_text(load(BASE / "plans/round45_c1_verify.py", "c1").HARNESS)
k44 = load(LANE / "plans/round44_c1_verify.py", "k44")
c1 = load(LANE / "plans/round45_c1_verify.py", "c1")
fence_copy = ROOT / "fence/fixture_fence.py"
shutil.copy2(LANE / "plans/fixture_fence.py", fence_copy)
mod_path = OUT / "hx_git_objects_link.py"
built = c1.build_module(k44, LANE, ROOT, mod_path)
print("BUILT", json.dumps([{k: str(v) if isinstance(v, pathlib.Path) else v for k, v in fx.items()} for fx in built]))
os.environ["K45_KEEP_STRACE"] = str(ROOT / "strace")
for i, fx in enumerate(built, 1):
    print("RESULT", c1.run_fence(k44, LANE, ROOT, fence_copy, fx, i))
