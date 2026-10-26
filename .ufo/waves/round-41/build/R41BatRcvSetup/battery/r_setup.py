"""battery41 module r_setup: the tip-receipts setup refusals (frozen mutants T01, T02, T05, T07).

Every fixture builds a lane tree in its own empty dir and expects the tool's setup refusal: exit 2
with no `receipt ...` and no `control ...` line on stdout, so `defects` is empty for all of them.
One fixture per refusal branch, plus a second shape per mutant.

  r_setup-t01-lane-absent       --lane names a path that does not exist
  r_setup-t01-not-a-repo        --lane names a plain directory; git cannot answer for it
  r_setup-t02-no-evidence       work-tree root with no corpus/evidence at all
  r_setup-t02-evidence-is-file  corpus/evidence exists as a regular file, so it is no directory
  r_setup-t05-tamper-absent     --tamper names a path that is no receipt at all
  r_setup-t05-tamper-unmapped   --tamper names a committed candidate the mapping leaves unmapped
  r_setup-t07-lane-subdir       --lane is a subdirectory of the work tree (evidence inside it)
  r_setup-t07-nested-lane       --lane sits two levels inside a lane-shaped work tree
"""

EV = "corpus/evidence"
RECEIPT = "corpus/evidence/r/foo-probe.txt"
PROBE = ('"""Stub probe.\n\n  python3 plans/foo_probe.py --lane .\n"""\nimport sys\n'
         'sys.stdout.write("X\\n")\n')


def tree(ctx, dest, files):
    """Init one work tree at dest, write its files, commit them as the fixture identity."""
    root = ctx.init(dest)
    for rel, text in files.items():
        ctx.write(root / rel, text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def listing(lane):
    return ["--lane", str(lane), "--list"]


def runner(lane, *extra):
    return ["--lane", str(lane), "--work", "{WORK}", *extra]


def b_lane_absent(ctx, d):
    # the --lane directory check: a path that is simply not there
    return listing(d / "absent")


def b_not_a_repo(ctx, d):
    # the is-a-work-tree check: the layout is present but no work tree answers git
    ctx.write(d / "plain" / RECEIPT, "X\n")
    ctx.write(d / "plain" / "plans/foo_probe.py", PROBE)
    return listing(d / "plain")


def b_no_evidence(ctx, d):
    # the corpus/evidence directory check on a lane-shaped root that has none
    root = tree(ctx, d / "lane", {"README.md": "kengaku lane\n", "SKILL.md": "# skill\n",
                                  "plans/foo_probe.py": PROBE})
    return listing(root)


def b_evidence_is_file(ctx, d):
    # same branch, second trigger: the path exists but is a regular file, so it is no directory
    root = tree(ctx, d / "lane", {"README.md": "kengaku lane\n", "corpus/evidence": "flat file\n"})
    return listing(root)


def b_tamper_absent(ctx, d):
    # --tamper naming a receipt that does not exist: the unknown-id refusal
    root = tree(ctx, d / "lane", {RECEIPT: "X\n", "plans/foo_probe.py": PROBE})
    return runner(root, "--tamper", "corpus/evidence/nope.txt")


def b_tamper_unmapped(ctx, d):
    # same branch, second shape: the tampered path is a committed candidate, yet the mapping (table plus
    # derived stem) leaves it unmapped, so it is not a mapped receipt either
    root = tree(ctx, d / "lane", {RECEIPT: "X\n", "plans/foo_probe.py": PROBE,
                                  "corpus/evidence/r/bar-probe.log": "X\n"})
    return runner(root, "--tamper", "corpus/evidence/r/bar-probe.log")


def b_lane_subdir(ctx, d):
    # the work-tree-root check: the lane is the subdirectory, not the root
    root = tree(ctx, d / "repo", {"sub/corpus/evidence/r/foo-probe.txt": "X\n",
                                  "sub/plans/foo_probe.py": PROBE})
    return listing(root / "sub")


def b_nested_lane(ctx, d):
    # same branch, second shape: a lane-shaped root with the lane two levels deeper, both carrying
    # corpus/evidence, so evidence alone cannot settle which directory the tool was pointed at
    root = tree(ctx, d / "worktree", {
        "README.md": "kengaku lane\n",
        "SKILL.md": "# skill\n",
        "corpus/evidence/round35/tb2-grader-probe.txt": "X\n",
        "plans/foo_probe.py": PROBE,
        "nested/deeper/corpus/evidence/r/foo-probe.txt": "X\n",
        "nested/deeper/plans/foo_probe.py": PROBE,
    })
    return listing(root / "nested" / "deeper")


FIXTURES = [
    {"fid": "r_setup-t01-lane-absent", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_lane_absent},
    {"fid": "r_setup-t01-not-a-repo", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_not_a_repo},
    {"fid": "r_setup-t02-no-evidence", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_no_evidence},
    {"fid": "r_setup-t02-evidence-is-file", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_evidence_is_file},
    {"fid": "r_setup-t05-tamper-absent", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_tamper_absent},
    {"fid": "r_setup-t05-tamper-unmapped", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_tamper_unmapped},
    {"fid": "r_setup-t07-lane-subdir", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_lane_subdir},
    {"fid": "r_setup-t07-nested-lane", "tool": "receipts", "expect": "error", "defects": [],
     "build": b_nested_lane},
]
