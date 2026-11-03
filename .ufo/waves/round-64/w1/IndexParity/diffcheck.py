#!/usr/bin/env python3
"""Differential check of the state_check legs that read corpus/README.md, base vs base+six-rows.

The scratch root is a symlink farm: every lane entry is symlinked to the real lane
(read-only) except corpus/README.md, which is a scratch copy. Nothing in the lane is
touched. Uses the lane's own plans/state_check.py functions — no second convention.
"""
import os, shutil, sys, pathlib, hashlib

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
SCRATCH = pathlib.Path("/fast/scratch/hyaku/kengaku-r64/IndexParity/diffroot")
sys.path.insert(0, str(LANE / "plans"))
import state_check  # noqa: E402

ROWS = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-64/w1/IndexParity/index-rows.md")


def make_root(name: str, patched: bool) -> pathlib.Path:
    root = SCRATCH / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for entry in LANE.iterdir():
        if entry.name == "corpus":
            continue
        os.symlink(entry, root / entry.name)
    corpus = root / "corpus"
    corpus.mkdir()
    for entry in (LANE / "corpus").iterdir():
        if entry.name == "README.md":
            continue
        os.symlink(entry, corpus / entry.name)
    readme = (LANE / "corpus/README.md").read_text(encoding="utf-8")
    if patched:
        lines = readme.splitlines()
        start = next(i for i, l in enumerate(lines) if l.startswith("### `lessons/`"))
        end = next(i for i, l in enumerate(lines) if l.startswith("Supporting corpus files:"))
        last = max(i for i in range(start, end) if lines[i].startswith("| `lessons/"))
        new_rows = [l for l in ROWS.read_text(encoding="utf-8").splitlines()
                    if l.startswith("| `lessons/round-")]
        lines = lines[: last + 1] + new_rows + lines[last + 1 :]
        readme = "\n".join(lines) + "\n"
    (corpus / "README.md").write_text(readme, encoding="utf-8")
    return root


def run(root: pathlib.Path):
    out = []
    state_check.check_readme_index(root, out)
    state_check.check_p3e(root, out)
    state_check.check_p4b(root, out)
    return out


base = make_root("base", patched=False)
patched = make_root("patched", patched=True)

b_out = run(base)
p_out = run(patched)


def summarize(assertions):
    rows = {}
    for a in assertions:
        rows.setdefault(a.verdict, []).append(a.id)
    return rows


bs, ps = summarize(b_out), summarize(p_out)
print("BASE   P2e+P3e+P4b verdicts:", {k: len(v) for k, v in sorted(bs.items())})
print("PATCH  P2e+P3e+P4b verdicts:", {k: len(v) for k, v in sorted(ps.items())})
print()
print("MISMATCH ids base :", bs.get("MISMATCH", []))
print("MISMATCH ids patch:", ps.get("MISMATCH", []))
print()
# per-id verdict diff (ids are path-keyed, so line shifts do not change ids)
bmap = {a.id: a.verdict for a in b_out}
pmap = {a.id: a.verdict for a in p_out}
diffs = []
for aid in sorted(set(bmap) | set(pmap)):
    bv, pv = bmap.get(aid), pmap.get(aid)
    if bv != pv:
        diffs.append((aid, bv, pv))
print(f"verdict changes per assertion id: {len(diffs)}")
for aid, bv, pv in diffs:
    print(f"   {aid}: {bv} -> {pv}")
print()
added = sorted(set(pmap) - set(bmap))
print(f"new assertion ids in patched run: {len(added)}")
for aid in added:
    print(f"   {aid}: {pmap[aid]}")
print()
print("patched README sha256:", hashlib.sha256((patched / "corpus/README.md").read_bytes()).hexdigest())
print("lane   README sha256:", hashlib.sha256((LANE / "corpus/README.md").read_bytes()).hexdigest())
