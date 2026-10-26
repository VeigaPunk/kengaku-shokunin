#!/usr/bin/env python3
"""Compute the r36-P0 fixture tree digest exactly as the cheat gate will compute it, twice (determinism)."""
import hashlib
import importlib.util
import pathlib
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
S = pathlib.Path(sys.argv[2]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def treedigest(root):
    h = hashlib.sha256()
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root).as_posix()
        if rel == ".git" or rel.startswith(".git/"):
            continue
        if f.is_file():
            h.update(rel.encode() + b"\0" + hashlib.sha256(f.read_bytes()).digest())
        else:
            h.update(rel.encode() + b"\0dir")
    return h.hexdigest()


counter = load(LANE / "plans/round37_c1_verify.py", "c37")
r36 = counter.load_r36(LANE)
ctx = counter.Ctx(LANE, r36)
fixtures = counter.r36_fixtures(r36)
for trial in (1, 2):
    root = pathlib.Path(tempfile.mkdtemp(prefix="k37-c1-digest-", dir=S))
    d = root / "fx" / "f000"
    d.mkdir(parents=True)
    fx = fixtures[0]
    argv = list(fx["build"](ctx, d))
    print(f"TRIAL {trial} fid={fx['fid']} argv={argv} digest={treedigest(d)}")
    keep = S / f"p0-{trial}"
    if not keep.exists():
        import shutil
        shutil.copytree(d, keep, symlinks=True)
