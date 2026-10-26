#!/usr/bin/env python3
"""Probe 1: what does the round-37 renamed run actually vary? Builds the frozen battery the way
plans/round37_c1_verify.py does, then reports per-fixture: rename string coverage, interior names,
identity cues, and whether a gate run mutates the fixture tree."""
import hashlib
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
S = pathlib.Path(sys.argv[2]).resolve()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load(LANE / "plans/round37_c1_verify.py", "c37")
r36 = counter.load_r36(LANE)
ctx = counter.Ctx(LANE, r36)
fixtures = counter.r36_fixtures(r36) + counter.battery37_fixtures(LANE / "plans/battery37")
print(f"FIXTURES n={len(fixtures)} r36={sum(1 for f in fixtures if f.get('r36'))} b37={sum(1 for f in fixtures if not f.get('r36'))}")

root = pathlib.Path(tempfile.mkdtemp(prefix="k37-c1-probe1-", dir=S))
built = []
for i, fx in enumerate(fixtures):
    d = root / "fx" / f"f{i:03d}"
    d.mkdir(parents=True)
    argv = list(fx["build"](ctx, d))
    built.append((fx, d, argv))

ref_gate = root / "gates" / "ref.py"
ref_gate.parent.mkdir()
ref_gate.write_text((LANE / "plans/pkg_gate.py").read_text())


def tree(d):
    out = {}
    for p in sorted(d.rglob("*")):
        rel = str(p.relative_to(d))
        if p.is_symlink():
            out[rel] = "symlink:" + os.readlink(p)
        elif p.is_file():
            out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        else:
            out[rel] = "dir"
    return out


def tree_digest(d):
    return hashlib.sha256(repr(sorted(tree(d).items())).encode()).hexdigest()[:16]


# --- renamed run, exactly as the counter does it
ren = root / "renamed"
ren.mkdir()
rows = []
for i, (fx, d, argv) in enumerate(built):
    nd = ren / f"x{(len(built) - i) * 7919 % 100003:05d}q"
    shutil.copytree(d, nd, symlinks=True)
    nargv = [t.replace(str(d), str(nd)) for t in argv]
    rows.append((i, fx["fid"], d, nd, argv, nargv))

no_touch = [r for r in rows if r[4] == r[5]]
print(f"RENAME argv_unchanged={len(no_touch)} of {len(rows)}")
for r in no_touch:
    print(f"  UNCHANGED {r[1]} argv={r[4]}")
print(f"RENAME newnames unique={len({r[3].name for r in rows})==len(rows)} pattern_set={sorted({'x..q' for r in rows})}")
print(f"RENAME same_length={len({len(r[3].name) for r in rows})==1} all_end_q={all(r[3].name.endswith('q') for r in rows)}")
print(f"RENAME ref_names_scheme=f{{i:03d}} renamed_scheme=x{{(N-i)*7919%100003:05d}}q deterministic=True")
print(f"RENAME shared_prefix_of_both_runs={str(root)}")
print(f"RENAME spect_path_shared={ctx.spec_path}")

# --- identity cues that the rename leaves in place
CUE_WORDS = ["junk", "absent", "unreadable", "two-lines", "relabelled", "altered", "duplicate",
             "queued", "extra", "alt-captures", "caps", "genuine", "swapped", "notoken", "negated"]
cue_rows = []
for i, fx, d, argv in ((r[0], r[1], r[2], r[4]) for r in rows):
    names = [rel for rel in tree(d) if rel != ".git" and not rel.startswith(".git/")]
    hits = sorted({w for w in CUE_WORDS for n in names if w in n})
    fid_in = [rel for rel in names if fx in rel]
    cue_rows.append((i, fx, hits, fid_in, len(names)))
print(f"CUES fixtures_with_interior_cue_words={sum(1 for r in cue_rows if r[2])} of {len(cue_rows)}")
for r in cue_rows:
    if r[2]:
        print(f"  CUE {r[1]} words={','.join(r[2])}")
print(f"CUES fixtures_with_fid_in_path={sum(1 for r in cue_rows if r[3])}")
print(f"CUES fixtures_with_junk_literal_in_content="
      f"{sum(1 for (i,fx,d,argv) in ((r[0],r[1],r[2],r[4]) for r in rows) if any('junk' in p.read_text(errors='ignore') for p in d.rglob('*') if p.is_file() and '.git' not in p.parts))}")

# --- does a gate run mutate the tree the reference saw?
samples = [built[0], built[7], built[-3]]  # r36-P0, a junk package, a d4/d5 line fixture
for fx, d, argv in samples:
    b = tree_digest(d)
    subprocess.run([sys.executable, str(ref_gate), *argv, "--spec", str(ctx.spec_path)],
                   capture_output=True, text=True)
    a = tree_digest(d)
    print(f"MUTATE {fx['fid']} before={b} after={a} same={a==b}")
shutil.rmtree(root, ignore_errors=True)
