#!/usr/bin/env python3
"""Assemble the green-baseline fixture in the scratch clone from the R42PkgEntry drafts snapshot."""
import pathlib, subprocess, sys, shutil

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r42/R42MutProbe")
lane = S / "lane"
drafts = (S / "drafts.md").read_text()
BUILD = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42PkgEntry")

# --- parse drafts sections ---------------------------------------------------
sections, cur = {}, None
for line in drafts.splitlines():
    if line.startswith("## "):
        cur = line
        sections[cur] = []
    elif cur is not None:
        sections[cur].append(line)
def sec(prefix):
    hits = [v for k, v in sections.items() if k.startswith(prefix)]
    assert len(hits) == 1, prefix
    return [l for l in hits[0] if l.strip()]

src_rows  = sec("## corpus/SOURCES.md")
idx_row   = sec("## corpus/README.md — knowledge index row")
cov_row   = sec("## corpus/README.md — coverage bullet")
fro_row   = sec("## corpus/README.md — §Frontier sub-bullet")
prov_key  = [k for k in sections if k.startswith("## Round42 partial frontier admission")]
assert len(prov_key) == 1
prov_blk  = [prov_key[0][3:]] + sections[prov_key[0]]
assert len(src_rows) == 3 and len(idx_row) == 1 and len(cov_row) == 1 and len(fro_row) == 1 and len(prov_blk) >= 5

def insert_after(text, anchor_pred, new_lines, what):
    lines = text.splitlines()
    hits = [i for i, l in enumerate(lines) if anchor_pred(l)]
    assert len(hits) == 1, f"{what}: {len(hits)} anchors"
    i = hits[0]
    return "\n".join(lines[:i + 1] + new_lines + lines[i + 1:]) + "\n"

# --- SOURCES.md --------------------------------------------------------------
p = lane / "corpus/SOURCES.md"
t = p.read_text()
if "S125" not in t:
    t = insert_after(t, lambda l: l.startswith("| S124"), src_rows, "SOURCES S124")
    p.write_text(t)
# --- README.md ---------------------------------------------------------------
p = lane / "corpus/README.md"
t = p.read_text()
if "tb2-circuit-fibsqrt-grader.md" not in t:
    t = insert_after(t, lambda l: l.startswith("| `knowledge/tb2-constraints-scheduling-grader.md`"), idx_row, "README index")
    t = insert_after(t, lambda l: "(seventh task, embedded-scheduling-model class)" in l, cov_row, "README coverage")
    t = insert_after(t, lambda l: "*Partly discharged round 41 (2026-10-26):*" in l, fro_row, "README frontier")
    p.write_text(t)
# --- PROVINCE.md -------------------------------------------------------------
p = lane / "PROVINCE.md"
t = p.read_text()
if "Round42 partial frontier admission" not in t:
    p.write_text(t.rstrip("\n") + "\n\n" + "\n".join(prov_blk).rstrip("\n") + "\n")
# --- entry -------------------------------------------------------------------
dst = lane / "corpus/knowledge/tb2-circuit-fibsqrt-grader.md"
if not dst.exists():
    shutil.copyfile(BUILD / "tb2-circuit-fibsqrt-grader.md", dst)
subprocess.run(["git", "-C", str(lane), "add", "corpus/knowledge/tb2-circuit-fibsqrt-grader.md"], check=True)
r = subprocess.run(["git", "-C", str(lane), "status", "--porcelain"], capture_output=True, text=True, check=True)
print(r.stdout)
print("ASSEMBLE OK")
