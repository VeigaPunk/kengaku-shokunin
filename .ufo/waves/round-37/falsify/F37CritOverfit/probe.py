#!/usr/bin/env python3
"""Build every round-37 C1 fixture through the counter's own builders, run the genuine gate over each,
and dump a compact content feature sheet (no corpus tree is copied into the report dir).

Usage: python3 probe.py --lane CLONE --work SCRATCH/work --out features.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys


def load(lane):
    p = lane / "plans/round37_c1_verify.py"
    spec = importlib.util.spec_from_file_location("k37", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    try:
        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def tree(d, skip_git=True):
    out = {}
    for p in sorted(pathlib.Path(d).rglob("*")):
        rel = p.relative_to(d).as_posix()
        if skip_git and (rel == ".git" or rel.startswith(".git/")):
            continue
        if p.is_file():
            out[rel] = [sha(p), p.stat().st_size, p.read_text(errors="replace").count("\n")]
        elif p.is_dir():
            out[rel + "/"] = None
    return out


def features(fx, d, argv):
    rec = {"fid": fx["fid"], "expect": fx["expect"], "declared": fx["defects"], "argv": argv[1:]}
    d = pathlib.Path(d)
    rec["cmd"] = argv[0]
    rec["flags"] = [t for t in argv[1:] if t.startswith("--") and t not in ("--root", "--file", "--capture-dir")]
    if argv[0] == "package":
        rec["git"] = (d / ".git").exists()
        rec["tree"] = tree(d)
    elif argv[0] == "d4-line":
        f = pathlib.Path(argv[argv.index("--file") + 1])
        rec["file_rel"] = f.relative_to(d).as_posix() if str(f).startswith(str(d)) else str(f)
        rec["file_exists"] = f.is_file()
        rec["file_sha"] = sha(f)
        rec["file_lines"] = [] if not f.is_file() else [l for l in f.read_text().splitlines() if l.strip()]
    else:
        f = pathlib.Path(argv[argv.index("--file") + 1])
        cap = pathlib.Path(argv[argv.index("--capture-dir") + 1])
        rec["file_rel"] = f.relative_to(d).as_posix() if str(f).startswith(str(d)) else str(f)
        rec["file_exists"] = f.is_file()
        rec["file_lines"] = [] if not f.is_file() else [l for l in f.read_text().splitlines() if l.strip()]
        rec["capture"] = tree(cap)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    k37 = load(lane)
    gate_src = (lane / k37.GATE_REL).read_text()
    assert hashlib.sha256(gate_src.encode()).hexdigest() == k37.GATE_SHA256, "gate not at freeze digest"
    r36 = k37.load_r36(lane)
    ctx = k37.Ctx(lane, r36)
    fixtures = k37.r36_fixtures(r36) + k37.battery37_fixtures(lane / k37.BATTERY_REL)
    gdir = work / "gates"
    gdir.mkdir()
    ref = gdir / "ref.py"
    ref.write_text(gate_src)
    recs = []
    for i, fx in enumerate(fixtures):
        d = work / "fx" / f"f{i:03d}"
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        rc, bad = k37.run_gate(ref, ctx.spec_path, argv)
        rec = features(fx, d, argv)
        rec["dir"] = str(d)
        rec["ref_rc"] = rc
        rec["ref_defects"] = sorted(bad)
        recs.append(rec)
        print(f"{fx['fid']:34s} rc={rc} defects={','.join(sorted(bad)) or '-'}")
    pathlib.Path(a.out).write_text(json.dumps({"lane": str(lane), "fixtures": recs}, indent=1))
    print(f"WROTE {a.out} fixtures={len(recs)}")


if __name__ == "__main__":
    sys.exit(main())
