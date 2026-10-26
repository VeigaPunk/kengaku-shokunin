#!/usr/bin/env python3
"""Build the frozen round-36/37/38 fixture set exactly as plans/round39_c1_verify.py builds it.

Usage: build_fixtures.py LANE DEST   -> DEST/fixtures.json
Reuses the counter's own helpers (in-process r36+b37, out-of-process battery38) so the pair matrix
measures the same inputs the frozen BATTERY line measures. No mutation, no gate edits here.
"""
import importlib.util
import json
import pathlib
import sys

LANE = pathlib.Path(sys.argv[1]).resolve()
DEST = pathlib.Path(sys.argv[2]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    c39 = load(LANE / "plans/round39_c1_verify.py", "c39")
    r37 = load(LANE / c39.R37_REL, "r37")
    r36 = r37.load_r36(LANE)
    ctx = r37.Ctx(LANE, r36)
    DEST.mkdir(parents=True, exist_ok=True)
    root = DEST / "fxroot"
    out = []
    inproc = r37.r36_fixtures(r36) + r37.battery37_fixtures(LANE / r37.BATTERY_REL)
    for i, fx in enumerate(inproc):
        d = root / "inproc" / f"f{i:03d}"
        d.mkdir(parents=True, exist_ok=True)
        argv = [str(t) for t in fx["build"](ctx, d)]
        out.append({"fid": fx["fid"], "expect": fx.get("expect"), "defects": fx.get("defects"),
                    "argv": argv, "dir": str(d), "module": "inproc", "r36": bool(fx.get("r36"))})
    more, side = c39.module_fixtures(LANE / c39.BATTERY38_REL, root, "battery38", LANE)
    for fx in more:
        out.append({k: fx[k] for k in ("fid", "expect", "defects", "argv", "dir", "module")} | {"r36": False})
    ids = [f["fid"] for f in out]
    assert len(set(ids)) == len(ids), "duplicate fid"
    meta = {"spec_path": str(ctx.spec_path), "sidechannel": side, "fixtures": out}
    (DEST / "fixtures.json").write_text(json.dumps(meta, indent=0))
    print(f"BUILT fixtures={len(out)} sidechannel={side} spec={ctx.spec_path}")
    fam = {}
    for f in out:
        fam[f["argv"][0]] = fam.get(f["argv"][0], 0) + 1
    print("FAMILIES", json.dumps(fam, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
