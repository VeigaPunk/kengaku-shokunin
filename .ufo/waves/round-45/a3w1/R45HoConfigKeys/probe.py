import importlib.util, json, pathlib, subprocess, sys, tempfile

lane = pathlib.Path(sys.argv[1]).resolve()
root = pathlib.Path(sys.argv[2]).resolve()
modpath = pathlib.Path(sys.argv[3]).resolve()
spec = importlib.util.spec_from_file_location("k45_counter", lane / "plans/round45_c1_verify.py")
k44spec = importlib.util.spec_from_file_location("k44_counter", lane / "plans/round44_c1_verify.py")
k44 = importlib.util.module_from_spec(k44spec)
k44spec.loader.exec_module(k44)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)
(root / "fx").mkdir(parents=True)
(root / "btmp").mkdir(parents=True)
fxs = c1.build_module(k44, lane, root, modpath)
(root / "harness.py").write_text(c1.HARNESS)
fence = root / "fence.py"
fence.write_bytes((lane / "plans/fixture_fence.py").read_bytes())
for i, fx in enumerate(fxs):
    print("FIXTURE", fx["fid"], fx["dir"])
    print("FENCE", c1.run_fence(k44, lane, root, fence, fx, i))
    repo = fx["dir"] / "lane"
    target = fx["dir"] / "marker"
    target.write_text("x\n")
    env = dict(k44.PIN_CHECK_ENV, GIT_CEILING_DIRECTORIES=str(root))
    r = subprocess.run(["git", "-C", str(repo), "check-attr", "hostile", "--", "marker"], text=True, capture_output=True, env=env)
    print("TOOL_CHECK_ATTR", "rc=" + str(r.returncode), "stdout=" + r.stdout.strip(), "stderr=" + r.stderr.strip())
