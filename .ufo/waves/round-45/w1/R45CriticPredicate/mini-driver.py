# Replica driver: calls the REAL counter's run_fence against a chosen fence + planted scratch.
import importlib.util, json, pathlib, sys, tempfile
LANE = pathlib.Path(sys.argv[1]).resolve()
FENCE = pathlib.Path(sys.argv[2]).resolve()
def load(p, n):
    spec = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
k45 = load(LANE / "plans/round45_c1_verify.py", "k45")
k44 = load(LANE / "plans/round44_c1_verify.py", "k44")
root = pathlib.Path(tempfile.mkdtemp(prefix="k45-mini-", dir=sys.argv[3] if len(sys.argv) > 3 else None)).resolve()
(root / "harness.py").write_text(k45.HARNESS)
(root / "empty").mkdir(); (root / "fence").mkdir()
fence_copy = root / "fence" / "fixture_fence.py"
fence_copy.write_bytes(FENCE.read_bytes())
# planted scratch layout like a real run: fx/<mod>/f000 = d; sibling plant in same module dir; btmp dir
mod = root / "fx" / "refusals45-t9"
d = (mod / "f000"); d.mkdir(parents=True); d = d.resolve()
(d / "claims.md").write_text("x\n")
(mod / "outside.cfg").write_text("OUTSIDE-SECRET\n")
(root / "btmp" / "refusals45-t9").mkdir(parents=True)
(root / "mods").mkdir(); (root / "mods" / "mod_refusals45_t9.py").write_text("# module source leak oracle\n")
print("ROOT", root)
fx = {"fid": "t9-mini", "tool": "anchor", "argv": ["--lane", "."], "dir": d, "module": "refusals45/t9"}
verdict, why, opens = k45.run_fence(k44, LANE, root, fence_copy, fx, 0)
print(f"RESULT verdict={verdict} opens={opens} why={why!r}")
