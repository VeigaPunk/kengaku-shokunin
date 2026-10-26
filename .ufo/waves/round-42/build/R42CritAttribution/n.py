import os, sys, pathlib, json
sys.dont_write_bytecode = True
S = pathlib.Path(os.environ["S"]); sys.path.insert(0, str(S)); import h
ctr = h.ctr
R = S / "run3"
R.mkdir(exist_ok=True)
runner = ctr.Runner(R, 8)
fx, side = ctr.build_battery(S / "wb", R, S / "lane")
FID = {f["fid"]: f for f in fx}
V = S / "run1" / "variants"
for fid, tool, name in (("w-x3-provurl-fallback", "anchor", "ref-anchor.py"),
                        ("w-x3-provurl-fallback", "anchor", "X6.py"),
                        ("w-x12-slashless-slug", "anchor", "X6.py"),
                        ("w-x13-staged-index", "anchor", "X13.py")):
    a = h.run2(runner, tool, V / name, FID[fid], "n1-%s-%s" % (fid, name), full=())
    b = h.run2(runner, tool, V / name, FID[fid], "n2-%s-%s" % (fid, name), full=())
    diffs = {}
    for d in a[2]["locs"]:
        if d not in b[2]["locs"]:
            continue
        line_diff = [n for n in a[2]["locs"][d] if n in b[2]["locs"][d]
                     and a[2]["locs"][d][n] != b[2]["locs"][d][n]]
        if line_diff:
            diffs[d] = line_diff
    print("%-28s %-12s same-variant-repeat diffs=%s" % (fid, name, {k: len(v) for k, v in diffs.items()}))
