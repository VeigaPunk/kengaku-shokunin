#!/usr/bin/env python3
"""Derive the overfit table for F37CritOverfit from the counter's own fixture builders.

For every fixture the round-37 C1 counter builds (14 round-36 + 50 battery37 = 64):
  * compute the overfit cue BEFORE the gate touches the fixture (a content fingerprint over working
    files: relative path + sha256, skipping .git and __pycache__);
  * run the genuine frozen gate (the counter's `run_gate` reference path) and record (exit, DEFECT set);
  * recompute the cue AFTER the run and fail loudly if the gate's side effects changed it;
  * copy the fixture to a differently named directory and recompute the cue (renamed invariance);
then emit `overfit_gate.py`, a gate that embeds the cue -> declared-output table and implements no
clause at all, plus a JSON audit.

Usage: python3 derive_table.py --lane CLONE --work SCRATCH/work2 --outdir SEATDIR
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys

SKIP_DIRS = {".git", "__pycache__"}


def csha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def walk_files(base):
    """(relpath, sha256) for every working file under base, .git and __pycache__ skipped."""
    base = pathlib.Path(base)
    out = []
    if not base.is_dir():
        return None
    for p in sorted(base.rglob("*")):
        rel = p.relative_to(base).as_posix()
        if any(part in SKIP_DIRS for part in pathlib.PurePosixPath(rel).parts):
            continue
        if p.is_file():
            try:
                out.append(f"{rel}:{csha(p)}")
            except OSError:
                out.append(f"{rel}:UNREADABLE")
        elif p.is_dir():
            out.append(f"{rel}/")
    return out


def diff(cmd, flags, opts):
    """The whole cue: invocation shape plus one canonical content fingerprint."""
    if cmd == "package":
        root = pathlib.Path(opts.get("--root") or ".")
        git = "dir" if (root / ".git").is_dir() else ("file" if (root / ".git").is_file() else "absent")
        entries = walk_files(root)
        body = "NO-ROOT" if entries is None else "GIT=" + git + "\n" + "\n".join(entries)
    elif cmd == "d4-line":
        f = pathlib.Path(opts.get("--file") or "")
        body = "FILE=" + ("ABSENT" if not f.is_file() else csha(f))
    else:
        f = pathlib.Path(opts.get("--file") or "")
        entries = walk_files(opts.get("--capture-dir") or "")
        body = "FILE=" + ("ABSENT" if not f.is_file() else csha(f)) + "\nCAP=\n" + \
            ("NO-CAPDIR" if entries is None else "\n".join(entries))
    return cmd + "|" + ",".join(sorted(flags)) + "|" + hashlib.sha256(body.encode()).hexdigest()


def load(lane, rel="plans/round37_c1_verify.py"):
    spec = importlib.util.spec_from_file_location("k37", lane / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def opts_of(argv):
    opts, flags, pos, i = {}, [], [], 0
    while i < len(argv):
        tok = argv[i]
        if tok in ("--spec", "--root", "--file", "--capture-dir"):
            opts[tok] = argv[i + 1] if i + 1 < len(argv) else ""
            i += 2
            continue
        if tok.startswith("--"):
            flags.append(tok)
        else:
            pos.append(tok)
        i += 1
    return pos, opts, flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--outdir", default=str(pathlib.Path(__file__).resolve().parent))
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    outdir = pathlib.Path(a.outdir).resolve()
    work.mkdir(parents=True, exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)
    k37 = load(lane)
    assert csha(lane / k37.GATE_REL) == k37.GATE_SHA256, "gate is not at the freeze digest"
    r36 = k37.load_r36(lane)
    ctx = k37.Ctx(lane, r36)
    fixtures = k37.r36_fixtures(r36) + k37.battery37_fixtures(lane / k37.BATTERY_REL)
    gdir = work / "gates"
    gdir.mkdir(exist_ok=True)
    ref = gdir / "ref.py"
    ref.write_text((lane / k37.GATE_REL).read_text())
    table, rows, problems = {}, [], []
    for i, fx in enumerate(fixtures):
        d = work / "fx" / f"f{i:03d}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        argv = list(fx["build"](ctx, d))
        pos, opts, flags = opts_of(argv)
        cmd = pos[0]
        key = diff(cmd, flags, opts)
        rc, bad = k37.run_gate(ref, ctx.spec_path, argv)
        key2 = diff(cmd, flags, opts)
        if key != key2:
            problems.append(f"{fx['fid']}: cue changed by the genuine gate's own side effects")
        nd = work / "renamed" / f"z{(len(fixtures) - i) * 104729 % 999983:06d}"
        if nd.exists():
            shutil.rmtree(nd)
        shutil.copytree(d, nd, symlinks=True)
        nargv = [t.replace(str(d), str(nd)) for t in argv]
        npos, nopts, nflags = opts_of(nargv)
        nkey = diff(npos[0], nflags, nopts)
        if nkey != key:
            problems.append(f"{fx['fid']}: cue not invariant under rename")
        if key in table and table[key] != [rc, sorted(bad)]:
            problems.append(f"{fx['fid']}: cue collides with a different declared output")
        table[key] = [rc, sorted(bad)]
        rows.append({"fid": fx["fid"], "declared": fx["defects"], "expect": fx["expect"],
                     "rc": rc, "defects": sorted(bad), "key": key})
        print(f"{fx['fid']:34s} rc={rc} defects={','.join(sorted(bad)) or '-'}")
    literal = "{\n" + "".join(f"    {k!r}: {tuple(v)!r},\n" for k, v in sorted(table.items())) + "}"
    template = pathlib.Path(__file__).with_name("overfit_gate_template.py").read_text()
    gate = outdir / "overfit_gate.py"
    gate.write_text(template.replace("%%TABLE%%", literal))
    classes = collections.Counter((tuple(r["defects"]), r["rc"]) for r in rows)
    (outdir / "overfit_table.json").write_text(json.dumps(
        {"fixtures": rows, "problems": problems,
         "class_sizes": {"|".join(sorted(str(x) for x in k[0])) or "accept": n for k, n in classes.items()}},
        indent=1))
    print(f"TABLE keys={len(table)} fixtures={len(rows)} problems={len(problems)}")
    for p in problems:
        print("PROBLEM", p)
    print(f"WROTE {gate}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
