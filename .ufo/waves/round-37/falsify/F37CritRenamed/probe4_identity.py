#!/usr/bin/env python3
"""Probe 4: identity channels the renamed run leaves in place. Counts (a) fixtures whose tree content is
unique (so identity survives any rename), (b) identity-bearing interior file names, (c) mutant-id markers
written into fixture bytes."""
import hashlib
import importlib.util
import pathlib
import shutil
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
        h.update(rel.encode() + b"\0" + (hashlib.sha256(f.read_bytes()).digest() if f.is_file() else b"dir"))
    return h.hexdigest()


counter = load(LANE / "plans/round37_c1_verify.py", "c37")
r36 = counter.load_r36(LANE)
ctx = counter.Ctx(LANE, r36)
fixtures = counter.r36_fixtures(r36) + counter.battery37_fixtures(LANE / "plans/battery37")
root = pathlib.Path(tempfile.mkdtemp(prefix="k37-c1-probe4-", dir=S))
built = []
for i, fx in enumerate(fixtures):
    d = root / "fx" / f"f{i:03d}"
    d.mkdir(parents=True)
    built.append((fx, d, list(fx["build"](ctx, d))))

digests = {fx["fid"]: treedigest(d) for fx, d, _a in built}
print(f"IDENT content_unique_fixtures={len(set(digests.values()))}/{len(built)}")
accepts = [fx["fid"] for fx, _d, _a in built if fx["expect"] == "accept"]
print(f"IDENT accept_fixtures={accepts}")

names = {fx["fid"]: {p.name for p in d.rglob("*") if p.is_file()} for fx, d, _a in built}
uniq = {fid: sorted(ns - set().union(*[v for k, v in names.items() if k != fid])) for fid, ns in names.items()}
uniq = {fid: ns for fid, ns in uniq.items() if ns}
print(f"IDENT fixtures_with_identity_bearing_names={len(uniq)}")
for fid, ns in uniq.items():
    print(f"  UNIQNAME {fid} {','.join(ns)}")

marks = []
for fx, d, _a in built:
    hits = sorted({p.name for p in d.rglob("*") if p.is_file() and ".git" not in p.parts
                   and "appended by the M" in p.read_text(errors="ignore")})
    if hits:
        marks.append((fx["fid"], hits))
print(f"IDENT fixtures_with_mutant_id_marker_in_bytes={len(marks)}")
for fid, hits in marks:
    print(f"  MARK {fid} {','.join(hits)}")
shutil.rmtree(root, ignore_errors=True)
