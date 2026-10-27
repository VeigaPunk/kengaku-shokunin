#!/usr/bin/env python3
"""Apply plans/anchor_line_check.py's own row rule to the seven C3 rows, without git.

anchor_line_check.evidence_index() needs `git ls-files corpus/evidence`; the fixture is not a git repo, so this
script rebuilds the same digest->path index from the fixture's capture dir and then calls the real
row_defects()/parse_rows() from the lane's tool.
"""
import importlib.util, pathlib, sys, hashlib
sys.dont_write_bytecode = True
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PKG = pathlib.Path("/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/pkg")
spec = importlib.util.spec_from_file_location("alc", LANE / "plans/anchor_line_check.py")
alc = importlib.util.module_from_spec(spec); sys.modules["alc"] = alc; spec.loader.exec_module(alc)
capdir = PKG / "corpus/evidence/round46/tb2-polyglot-c-py"
idx = {}
for f in sorted(capdir.iterdir()):
    if f.name != "SHA256SUMS":
        idx.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(), []).append(
            str(f.relative_to(PKG)))
rows = alc.parse_rows((PKG / "corpus/SOURCES.md").read_text())
bad = 0
for sid, cells, line in rows:
    cited, cap, defs = alc.row_defects(cells, line, idx, PKG)
    bad += bool(defs) or not cited
    print(f"ROW {sid} cited={cited} capture={cap} defects={defs or 'none'}")
print(f"ANCHORRULE rows={len(rows)} defective={bad}")
sys.exit(0 if bad == 0 and len(rows) == 7 else 1)
