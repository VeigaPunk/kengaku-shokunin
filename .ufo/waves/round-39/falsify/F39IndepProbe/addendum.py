#!/usr/bin/env python3
"""Post-hoc addendum (disclosed as post-hoc in the report): the same worktree shape, but the linked worktree
is removed before the grader runs. Written AFTER the six-case run; prediction P P P P P from the mechanism
receipt (with-worktree rev-list --all=2 / fsck_dangling=0, worktree-removed rev-list --all=1 /
fsck_dangling=1: the commit becomes an ordinary dangling commit whose cat-file text carries no file content).

Usage: addendum.py <lane-at-tip> <work-parent>
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probe_extra as pe  # noqa: E402  (reads the same argv[1:3])

m = pe.m
SECRET = m.SECRET
CASE = m.Case(
    "worktree-added-then-removed",
    m.r(m.CLEAN, m.FLAG, "cd /app/repo",
        f"SB=$(printf '%s\\n' '{SECRET}' | git hash-object -w --stdin)",
        "ST=$(printf '100644 blob %s\\tsecret.txt\\n' \"$SB\" | git mktree)",
        "B=$(git commit-tree \"$ST\" -m 'chore: notes')",
        "git worktree add -q --detach /app/wt \"$B\"",
        "git worktree remove --force /app/wt"),
    "PPPPP", ("secret-gone",),
    "post-hoc addendum: the linked worktree is removed before grading, so no worktree HEAD names the commit")

case = CASE
root = pathlib.Path(pe.tempfile.mkdtemp(prefix="k39add-", dir=str(pe.WORK)))
try:
    rc, out = m.run_case(pe.LANE / m.CAP, root, case, "grade")
    print(f"ADDENDUM {case.cid} predicted_tests={case.predicted} rc={rc}")
    for line in out.splitlines():
        if line.startswith(("TEST ", "PROBE ")):
            print(line)
finally:
    pe.shutil.rmtree(root, ignore_errors=True)
