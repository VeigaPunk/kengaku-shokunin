#!/usr/bin/env python3
"""Which end state kills X2/X4/X5/X11 on battery40's a_bind-a17-index-bytes?

Builds that fixture exactly as plans/battery40/a_bind.py does (a clone of this lane), runs the unmodified
anchor tool and each round-40 near-variant, and prints (rc, DEFECT sid/class) so the kill provenance is
visible: defects on S903 = the fixture's own row, defects on any other sid = the cloned lane.
"""
import importlib.util
import json
import pathlib
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42CritEquiv")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


c40 = load("c40", LANE / "plans/round40_c1_verify.py")
a_bind = load("a_bind", LANE / "plans/battery40/a_bind.py")

XMUT = {}
tx = load("tx", LANE / ".ufo/waves/round-40/falsify/F40XMutAnchor/xmut_table.py")
for row in tx.MUTANTS:
    XMUT[row[0]] = row


def defects(text):
    out = []
    for line in text.splitlines():
        if line.startswith("DEFECT "):
            toks = dict(t.split("=", 1) for t in line.split() if "=" in t)
            out.append((toks.get("anchor", "") or toks.get("token", ""), toks.get("class", "?")) if False
                       else (line.split()[1], toks.get("class", "?")))
    return out


def main():
    root = S / "fx_a17"
    if root.exists():
        import shutil
        shutil.rmtree(root)
    root.mkdir(parents=True)
    ctx = c40.Ctx(S / "lane", root)
    d = root / "a17"
    argv = a_bind.build_a17(ctx, d)
    argv = [t.replace(str(d), str(d)) for t in argv]
    src = (LANE / "plans/anchor_digest_check.py").read_text()
    variants = {"REF": src}
    for mid in ("X1", "X2", "X3", "X4", "X5", "X6", "X11", "X12"):
        r = XMUT[mid]
        assert src.count(r[6]) == 1, mid
        variants[mid] = src.replace(r[6], r[7], 1)
    res = {}
    for name, text in variants.items():
        p = root / f"v_{name}.py"
        p.write_text(text)
        r = subprocess.run([sys.executable, str(p)] + argv, cwd=str(d), env=ctx.ENV,
                           capture_output=True, text=True)
        ds = defects(r.stdout)
        res[name] = {"rc": r.returncode, "defects": ds, "stderr": r.stderr.strip()[-200:]}
        print(f"{name:4s} rc={r.returncode} defects={len(ds)} {ds}")
    (S / "probe_a17.json").write_text(json.dumps(res, indent=1))
    print("argv:", argv)


if __name__ == "__main__":
    main()
