#!/usr/bin/env python3
"""battery40 module `l_refuse` — the three setup refusals `plans/ledger_tip.py` advertises at exit 2.

Frozen mutants of `plans/round40_c1_verify.py` this module witnesses, each in its declared direction
`error` (fixture `expect=error`, reference exit 2, mutant exit 0 or 1):

  L01  plans/ledger_tip.py:23-25  'Exit codes ... `2` usage/clone/setup refusal'
       old  `    raise SystemExit(2)\n\n\ndef load_module`
       new  `    raise SystemExit(1)\n\n\ndef load_module`
       The mutant relabels the single `refuse()` exit, so every refusal path below exits 1.

  L11  plans/ledger_tip.py:58  'The clone is created at <work>/lane (must not exist)'
       old  `    if dest.exists():\n        refuse`   new  `    if False:\n        refuse`
       The mutant reuses an existing `<work>/lane`: the clone succeeds into the empty directory and
       the run continues to the ledger rows instead of refusing.

  L21  plans/ledger_tip.py:44-45  'REFUSE stale pin ref ... (exit 2) the ref exists but resolves to a
       commit other than the one under audit'
       old  `        if rev and rev != tip:\n            refuse(f"stale pin ref`
       new  `        if False:\n            refuse(f"stale pin ref`
       Control mode on a clone whose `refs/heads/master` was rewound six commits: the reference
       refuses after printing `TIP commit=`, the mutant binds the pin row to the stale commit and
       evaluates the ledger against it.

Every fixture is a refusal: the tool prints `REFUSE ...` on stderr, exactly one `TIP commit=` line at
most on stdout in control mode, and no row statement (row lines are buffered), so the exact class set
the unmodified tool prints is the empty set for all three.  One fixture per behaviour: the L01 witness
(not-a-repository source) is the only one of the three whose refusal happens before any clone, the L11
witness is the only one that reaches the existing-destination test, and the L21 witness is the only one
that reaches the pin-ref audit.  Removing the stale-pin fixture is what makes L21 survive; the two
other refusal fixtures also exhibit L01's relabelled exit, which is stated in the report rather than
claimed away.
"""


def source_not_a_repo(ctx, d):
    """L01 witness: `--source` names a directory that is not a git repository -> clone_lane refuses."""
    plain = d / "plain"
    plain.mkdir()
    (plain / "README.md").write_text("not a repository\n")
    return ["--source", str(plain), "--work", "{WORK}"]


def work_lane_exists(ctx, d):
    """L11 witness: <work>/lane already exists -> clone_lane refuses instead of reusing it."""
    src = ctx.clone(d / "src")
    return ["--source", str(src), "--work", "{WORK:lane}"]


def stale_master_pin(ctx, d):
    """L21 witness: control-mode clone whose refs/heads/master was rewound -> stale pin ref refusal."""
    lane = ctx.clone(d / "lane")
    ctx.git(lane, "checkout", "-q", "--detach")
    ctx.git(lane, "branch", "-f", "master", "HEAD~6")
    return ["--lane", str(lane)]


FIXTURES = [
    {"fid": "l_refuse-source-not-a-repo", "tool": "ledger", "expect": "error", "defects": [],
     "build": source_not_a_repo},
    {"fid": "l_refuse-work-lane-exists", "tool": "ledger", "expect": "error", "defects": [],
     "build": work_lane_exists},
    {"fid": "l_refuse-stale-pin-ref", "tool": "ledger", "expect": "error", "defects": [],
     "build": stale_master_pin},
]
