import importlib.util, pathlib, sys, subprocess
lane = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path(sys.argv[2]).resolve()
module = pathlib.Path(sys.argv[3]).resolve()
root.mkdir(parents=True, exist_ok=True)
for name in ("fx", "btmp", "mods", "empty", "fence"):
    (root / name).mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("k45", lane / "plans/round44_c1_verify.py")
k44 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k44)
c1spec = importlib.util.spec_from_file_location("c1", lane / "plans/round45_c1_verify.py")
c1 = importlib.util.module_from_spec(c1spec); c1spec.loader.exec_module(c1)
(root / "harness.py").write_text(c1.HARNESS)
fence_copy = root / "fence/fixture_fence.py"
fence_copy.write_bytes((lane / "plans/fixture_fence.py").read_bytes())
fxs = c1.build_module(k44, lane, root, module)
print("LANE", subprocess.check_output(["git", "-C", str(lane), "rev-parse", "HEAD"], text=True).strip())
for i, fx in enumerate(fxs):
    result = c1.run_fence(k44, lane, root, fence_copy, fx, i)
    print("RESULT", fx["fid"], result[0], "opens=" + str(result[2]), "reason=" + result[1])
