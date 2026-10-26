#!/usr/bin/env python3
"""Probe 3: which name-ish channels does the round-37 renamed run vary, and which is it blind to?

Builds the frozen battery, then for four gate variants prints (reference result vs renamed-copy result)
using the counter's own observable and the counter's own rename transform."""
import collections
import hashlib
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(sys.argv[1]).resolve()
S = pathlib.Path(sys.argv[2]).resolve()
HONEST = pathlib.Path(sys.argv[3]).read_text()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load(LANE / "plans/round37_c1_verify.py", "c37")
r36 = counter.load_r36(LANE)
ctx = counter.Ctx(LANE, r36)
fixtures = counter.r36_fixtures(r36) + counter.battery37_fixtures(LANE / "plans/battery37")
root = pathlib.Path(tempfile.mkdtemp(prefix="k37-c1-probe3-", dir=S))
built = []
for i, fx in enumerate(fixtures):
    d = root / "fx" / f"f{i:03d}"
    d.mkdir(parents=True)
    built.append((fx, d, list(fx["build"](ctx, d))))

ren = root / "renamed"
ren.mkdir()
pairs = []
for i, (fx, d, argv) in enumerate(built):
    nd = ren / f"x{(len(built) - i) * 7919 % 100003:05d}q"
    shutil.copytree(d, nd, symlinks=True)
    pairs.append((fx, d, argv, nd, [t.replace(str(d), str(nd)) for t in argv]))

GY = root / "gates"
GY.mkdir()


def gate(tag, src):
    p = GY / f"{tag}.py"
    p.write_text(src)
    return p


def run(g, argv):
    return counter.run_gate(g, ctx.spec_path, argv)


def sweep(tag, src):
    g = gate(tag, src)
    disagree = wrong = 0
    declared_ok = 0
    for fx, d, argv, nd, nargv in pairs:
        a = run(g, argv)
        b = run(g, nargv)
        disagree += a != b
        want_rc = 0 if fx["expect"] == "accept" else 1
        decl = fx.get("defects")
        ok = a[0] == want_rc and (decl is None or a[1] == frozenset(decl))
        if fx["expect"] == "accept":
            ok = ok and not a[1]
        wrong += not ok
        declared_ok += ok
    print(f"VARIANT {tag} renamed_disagree={disagree} wrong={wrong} matching_declaration={declared_ok}/{len(pairs)}")


sweep("V0-honest", HONEST)

# V1: fires only on the renamed-run name pattern (a gate that answers to the harness's naming scheme)
v1 = HONEST.replace(
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n",
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n"
    "    if re.fullmatch(r\"x\\d{5}q\", pkg.root.name):\n        return 1\n")
assert v1 != HONEST
sweep("V1-top-name-keyed", v1)

# V2: fires on an interior file name (d4 fixture naming carries the defect word)
v2 = HONEST.replace(
    "def cmd_d4(args, spec):",
    "def cmd_d4(args, spec):\n    if \"relabelled\" in str(args.file):\n        return 0")
assert v2 != HONEST
sweep("V2-interior-name-keyed", v2)

# V3: fires on the harness's own temp prefix, shared by the reference and renamed runs
v3 = HONEST.replace(
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n",
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n"
    "    if \"k37-c1-\" in str(pkg.root):\n        return 0\n")
assert v3 != HONEST
sweep("V3-harness-prefix-keyed", v3)

# V4: fires on a content marker a battery module writes into a capture
v4 = HONEST.replace(
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n",
    "def cmd_package(args, spec):\n    pkg = Package.load(args.root, spec)\n"
    "    if any(\"appended by the M15 fixture\" in f.read_text(errors=\"ignore\")"
    " for f in pkg.root.rglob(\"*\") if f.is_file()):\n        return 0\n")
assert v4 != HONEST
sweep("V4-content-marker-keyed", v4)

# --- which identity cues live inside fixture trees (unmoved by the rename)?
base = {str(p.relative_to(built[0][1])) for p in built[0][1].rglob("*")}
cue = re.compile(r"(two-lines|relabelled|absent|swapped|notoken|negated|alt-captures|genuine|"
                 r"no-such-erratum|caps)")
name_rows = [(fx["fid"], sorted({p.name for p in d.rglob("*") if cue.search(p.name)})) for fx, d, _a, _n, _b in pairs]
withcue = [r for r in name_rows if r[1]]
print(f"CUES fixtures_with_cue_in_interior_name={len(withcue)}/{len(pairs)}")
for fid, names in withcue:
    print(f"  NAME {fid} {','.join(names)}")
marker = re.compile(rb"\bM\d\d\b")
mk = []
for fx, d, _a, _n, _b in pairs:
    hits = sorted({m.group().decode() for p in d.rglob("*")
                   if p.is_file() and ".git" not in p.parts
                   for m in marker.finditer(p.read_bytes())})
    if hits:
        mk.append((fx["fid"], hits))
print(f"CUES fixtures_with_mutant_id_marker_in_content={len(mk)}")
for fid, hits in mk:
    print(f"  MARK {fid} {','.join(hits)}")
ids = collections.Counter(fx["fid"].split("-")[0] for fx, _d, _a, _n, _b in pairs)
print(f"CUES fixture_id_prefix_counts={dict(ids)}")
print(f"CUES fixtures_whose_top_dir_was_a_fid={sum(1 for fx,_d,_a,_n,_b in pairs if fx['fid'] in str(_d))}")
shutil.rmtree(root, ignore_errors=True)
