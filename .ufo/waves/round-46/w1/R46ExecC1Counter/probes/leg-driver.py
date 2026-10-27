import hashlib, json, os, pathlib, random, secrets, shutil, sys, tempfile
lane = pathlib.Path(sys.argv[1]).resolve()
mods = [pathlib.Path(p) for p in sys.argv[2:]]
WORK = os.environ.get("K46_WORK")
sys.path.insert(0, str(lane / "plans"))
import importlib.util
spec = importlib.util.spec_from_file_location("k46", lane / "plans/round46_c1_verify.py")
k46 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k46)
k44 = k46.load(lane / k46.K44_REL, "k44")
root = pathlib.Path(tempfile.mkdtemp(prefix="drv-", dir=WORK)).resolve()
empty = pathlib.Path(tempfile.mkdtemp(prefix=root.name+"-empty-", dir=root.parent))
rng = secrets.SystemRandom()
ctl = root / "ctl"; ctl.mkdir()
(ctl/"harness.py").write_text(k46.HARNESS)
fence = ctl/"fence.py"; fence.write_bytes(pathlib.Path(os.environ["K46_FENCE"]).read_bytes() if os.environ.get("K46_FENCE") else (lane/"plans/fixture_fence.py").read_bytes())
print("root", root)
try:
    n = 0
    for mp in mods:
        fxs = k46.build_module(k44, lane, root, empty, mp, rng, ctl)
        print("BUILT", mp.name, len(fxs), "parent", fxs[0]["dir"].parent.name, "children",
              len(list(fxs[0]["dir"].parent.iterdir())))
        if os.environ.get("K46_PLANT"):
            (fxs[0]["dir"].parent / "outside.cfg").write_text("OUTSIDE-SECRET\n")
        if os.environ.get("K46_FIFO"):
            os.mkfifo(fxs[0]["dir"].parent / "blocked.fifo")
        for fx in fxs:
            v, why, hits, calls = k46.run_fence(k44, lane, root, ctl, empty, fence, fx, n); n += 1
            print(f"  {fx['fid']:32s} {v:6s} touches={len(hits)} calls={calls} why={why[:80]}")
            for h in hits[:6]: print("      hit", h)
finally:
    shutil.rmtree(empty, ignore_errors=True); shutil.rmtree(root, ignore_errors=True)
