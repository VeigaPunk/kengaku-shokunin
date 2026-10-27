import importlib.util, pathlib, sys
S = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("k45", S/"lane/plans/round45_c1_verify.py")
k45 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k45)
k44 = k45.load(S/"lane/plans/round44_c1_verify.py", "k44")
root = S/"w3"; root.mkdir(exist_ok=True)
(root/"harness.py").write_text(k45.HARNESS)
(root/"fence").mkdir(exist_ok=True)
fc = root/"fence/fixture_fence.py"; fc.write_bytes((S/"lane/plans/fixture_fence.py").read_bytes())
print(f"FENCE-COPY sha256={k45.sha256(fc)}")
fxs = k45.build_module(k44, S/"lane", root, S/"selfattack.py")
n = admon = 0
for fx in fxs:
    n += 1
    verdict, why, opens = k45.run_fence(k44, S/"lane", root, fc, fx, n)
    admon += verdict in ("ADMIT", "ERROR")
    print(f"FENCE-RUN {fx['fid']} {verdict} opens={opens}" + (f" -- {why}" if why else ""))
print(f"SELFATTACK fixtures={n} admitted={admon}")
