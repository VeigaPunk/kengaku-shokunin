"""Round-44 C1 battery44 — mutant U9 of `plans/anchor_digest_check.py`.

U9's advertised behaviour (plans/anchor_digest_check.py:106-107): "lessons are read from the working tree for
paths committed at HEAD, so a seat's erratum counts before it is committed". The frozen mutant replaces the
working-tree read in `load_errata` with `git show HEAD:<path>`, i.e. lessons read from HEAD instead, declared
direction `rc-mirror` (the unmodified tool accepts the tree, the mutant rejects it).

Every fixture below is an ordinary repository built from nothing: one or more evidence captures committed at
HEAD, a census-shaped `corpus/SOURCES.md` whose row carries a stale 64-hex anchor token, and a committed
`corpus/lessons/*.md` whose HEAD text is NOT the text that exempts that row. The unmodified tool reads the
working tree, finds the erratum, exempts the row and prints no defect (exit 0). A tool that reads HEAD finds
no usable erratum and rejects the same tree (exit 1). Three shapes:

  * a four-row registry whose erratum is appended to a committed lessons file and never committed;
  * a two-commit history whose committed erratum names a different row and is retargeted in the working tree;
  * a committed erratum that carries only the stale token and is completed in place in the working tree.

No fixture reads a lane, a clone or any path outside its own build directory.
"""

import hashlib

ALPHA = b"alpha capture: registry row 101 payload\n"
BETA = b"beta capture: registry row 102 notes\n"
GAMMA = b"gamma capture: manifest-listed payload\n"
DELTA = b"delta capture: in-place repair payload\n"

HEADER = ("# Sources\n\n"
          "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          + "|" + " --- |" * 11 + "\n")


def _hex(data):
    return hashlib.sha256(data).hexdigest()


def _stale(label):
    """A 64-lowercase-hex token that is a digest of no committed capture (the row's stale claim)."""
    return hashlib.sha256(("u9-worktree-b stale anchor: " + label).encode()).hexdigest()


def _row(sid, scope, anchor):
    """One census-shaped row: exactly 11 cells, the anchor claim in cell 6 (index 5)."""
    return (f"| {sid} | {scope} | file | A | r44 | {anchor} | fixture row | mined | 2026-10-26 | - | - |\n")


def _commit(ctx, d, msg):
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", msg)


def build_registry(ctx, d):
    """Four-row registry; the erratum that exempts S104 exists only in the working tree (never committed)."""
    ctx.init(d)
    ctx.write(d / "corpus/evidence/u9a/alpha.txt", ALPHA)
    ctx.write(d / "corpus/evidence/u9a/beta.md", BETA)
    notes = "# Round 44 seat notes\n\nNo errata recorded at the time of this commit.\n"
    ctx.write(d / "corpus/lessons/r44-notes.md", notes)
    ctx.write(d / "corpus/SOURCES.md",
              HEADER
              + _row("S101", "`corpus/evidence/u9a/alpha.txt`", "sha256 " + _hex(ALPHA))
              + _row("S102", "`corpus/evidence/u9a/beta.md`", "sha256 " + _hex(BETA))
              + _row("S103", "`corpus/evidence/u9a/alpha.txt`", "-")
              + _row("S104", "`corpus/evidence/u9a/alpha.txt`", "sha256 " + _stale("registry")))
    _commit(ctx, d, "registry: two captures, four rows, one stale anchor")
    # working tree only (this is the whole fixture): the erratum appended after the commit
    ctx.write(d / "corpus/lessons/r44-notes.md",
              notes + "\nErratum (round 37): S104 anchor sha256 " + _stale("registry")
              + " corrected by sha256 " + _hex(ALPHA) + "\n")
    return ["--lane", "."]


def build_retargeted(ctx, d):
    """Two commits: HEAD's erratum names a row needing no exemption; the working tree retargets it at S210."""
    ctx.init(d)
    ctx.write(d / "corpus/evidence/u9b/gamma.bin", GAMMA)
    ctx.write(d / "corpus/evidence/u9b/SHA256SUMS", _hex(GAMMA) + "  gamma.bin\n")
    ctx.write(d / "corpus/lessons/notes.md", "# Standing notes\n\nErrata are filed in `errata.md`.\n")
    ctx.write(d / "corpus/lessons/errata.md",
              "# Errata\n\nErratum (round 37): S211 anchor sha256 " + _hex(GAMMA) + "\n")
    rows = (_row("S210", "`corpus/evidence/u9b/gamma.bin`", "sha256 " + _stale("retargeted")))
    ctx.write(d / "corpus/SOURCES.md", HEADER + rows)
    _commit(ctx, d, "history 1: one row with a stale anchor, one standing erratum")
    ctx.write(d / "corpus/SOURCES.md", HEADER + rows + _row("S211", "-", "-"))
    _commit(ctx, d, "history 2: register S211, the row the erratum names")
    # working tree only: the same erratum line, retargeted at S210 with S210's exact stale token
    ctx.write(d / "corpus/lessons/errata.md",
              "# Errata\n\nErratum (round 37): S210 anchor sha256 " + _stale("retargeted")
              + " corrected by sha256 " + _hex(GAMMA) + "\n")
    return ["--lane", "."]


def build_completed(ctx, d):
    """Committed erratum carries only the stale token; the working tree adds the correction that exempts."""
    ctx.init(d)
    ctx.write(d / "corpus/evidence/u9c/delta.txt", DELTA)
    ctx.write(d / "corpus/SOURCES.md",
              HEADER + _row("S310", "`corpus/evidence/u9c/delta.txt`", "sha256 " + _stale("completed")))
    ctx.write(d / "corpus/lessons/repairs.md",
              "# Repairs\n\nErratum (round 37): S310 anchor sha256 " + _stale("completed") + "\n")
    _commit(ctx, d, "repair log: the stale anchor is recorded, the correction is not")
    # working tree only: the correction token that makes the erratum exempt the row
    ctx.write(d / "corpus/lessons/repairs.md",
              "# Repairs\n\nErratum (round 37): S310 anchor sha256 " + _stale("completed")
              + " corrected by sha256 " + _hex(DELTA) + "\n")
    return ["--lane", "."]


FIXTURES = [
    # multi-row registry: an erratum appended to a committed lessons file and never committed still exempts
    {"fid": "u9_worktree_b-registry-erratum-appended", "tool": "anchor", "expect": "accept",
     "defects": [], "build": build_registry},
    # multi-commit history: a committed erratum aimed elsewhere is retargeted in the working tree
    {"fid": "u9_worktree_b-erratum-retargeted-history", "tool": "anchor", "expect": "accept",
     "defects": [], "build": build_retargeted},
    # second trigger of the same branch: a committed erratum that lacks its correction is completed in place
    {"fid": "u9_worktree_b-erratum-completed-in-place", "tool": "anchor", "expect": "accept",
     "defects": [], "build": build_completed},
]
