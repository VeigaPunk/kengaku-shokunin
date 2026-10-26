"""Round-42 battery42 module `o_clause`: two order-of-operations clauses, each in two history shapes.

Clause 1 (plans/order_check.py:183) rejects a freeze commit -- the first commit adding the claims file --
whose tree already carries the receipt. Clause 2 (plans/order_check.py:188) rejects a receipt whose first
adding commit is an ancestor of the freeze commit while the freeze tree itself does not carry it. Clause 3
(every blob ever committed under the round's claims/ directory up to the receipt commit) must stay clean in
every fixture here, so the only failure each reject fixture can report is the clause it is built for.

Every fixture builds its lane from nothing: `ctx.init` makes the repository, `ctx.write` lays down blobs,
`ctx.git` commits them at the pinned date, and the returned argv tail points the frozen gate at it. Shapes
differ from the pre-freeze direction modules on purpose: different repository and receipt paths, a receipt
edited after the freeze, a withdrawn early receipt, a side-line freeze merged back into master.
"""

M42 = ".ufo/waves/round-42/claims"
CLAIMS42 = "plans/round-42-claims.md"
PROBE42 = "corpus/evidence/round42/fibsqrt-probe.txt"
M9 = ".ufo/waves/round-9/claims"
CLAIMS9 = "plans/round-9-claims.md"
PROBE9 = "corpus/evidence/round9/build-pmars-probe.txt"
CLEAN = "no gate line and no case line was ever committed here\n"
RECEIPT_BODY = "cases=16 observed_pass=7 observed_fail=9 mismatches=0\nregrade cases=16 differ=0\n"


def commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def gate_argv(repo, claims, receipt):
    return ["--lane", str(repo), "--claims", claims, "--receipt", receipt]


def xo1_single(ctx, d):
    # clause 1, one commit: the freeze commit is also the commit that first adds the receipt
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS42, "# round 42 - frozen claims\n\nProbe frozen before its first run.\n")
    ctx.write(repo / M42 / "control.txt", CLEAN)
    ctx.write(repo / PROBE42, RECEIPT_BODY)
    commit(ctx, repo, "freeze, receipt already in the tree")
    return gate_argv(repo, CLAIMS42, PROBE42)


def xo1_edited_after(ctx, d):
    # clause 1, three commits: the freeze pair lands in the middle commit and the receipt is edited later,
    # so the first adding commit of the receipt is still the freeze commit
    repo = ctx.init(d / "lane")
    ctx.write(repo / "README.md", "# fixture lane\n")
    ctx.write(repo / M42 / "notes.txt", CLEAN)
    commit(ctx, repo, "scaffold the lane")
    ctx.write(repo / CLAIMS42, "# round 42 - frozen claims\n\nPredicate written before any measured run.\n")
    ctx.write(repo / PROBE42, "cases=16 observed_pass=7 observed_fail=9 mismatches=0\n")
    commit(ctx, repo, "freeze with the receipt in the same tree")
    ctx.write(repo / PROBE42, RECEIPT_BODY)
    ctx.write(repo / "LOG.md", "round 42 opened\n")
    commit(ctx, repo, "regrade the frozen cases")
    return gate_argv(repo, CLAIMS42, PROBE42)


def xo3_withdrawn(ctx, d):
    # clause 2: the receipt is added, withdrawn, the claims are frozen without it, and it is recorded again
    repo = ctx.init(d / "lane")
    ctx.write(repo / "README.md", "# fixture lane\n")
    ctx.write(repo / PROBE9, "early run, withdrawn before the freeze\n")
    commit(ctx, repo, "early run")
    ctx.git(repo, "rm", "-q", PROBE9)
    ctx.git(repo, "commit", "-q", "-m", "withdraw the early run")
    ctx.write(repo / CLAIMS9, "# round 9 - frozen claims\n\nOrder checked over commits only.\n")
    ctx.write(repo / M9 / "control.txt", CLEAN)
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE9, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return gate_argv(repo, CLAIMS9, PROBE9)


def xo3_side_line(ctx, d):
    # clause 2 with a branching history: the receipt lives on master before the freeze line exists, the
    # freeze happens on a side line, the receipt is recorded again on master, then the lines merge
    repo = ctx.init(d / "lane")
    ctx.write(repo / "evidence" / "probe.txt", "early run on master\n")
    ctx.write(repo / "docs" / "notes.md", "lane notes\n")
    commit(ctx, repo, "first recorded run")
    ctx.git(repo, "rm", "-q", "evidence/probe.txt")
    ctx.git(repo, "commit", "-q", "-m", "withdraw the early run")
    ctx.git(repo, "checkout", "-q", "-b", "freeze-line")
    ctx.write(repo / CLAIMS9, "# round 9 - frozen claims\n\nWritten on a side line.\n")
    ctx.write(repo / M9 / "control.txt", CLEAN)
    commit(ctx, repo, "freeze on the side line")
    ctx.git(repo, "checkout", "-q", "master")
    ctx.write(repo / "evidence" / "probe.txt", RECEIPT_BODY)
    commit(ctx, repo, "record the run again on master")
    ctx.git(repo, "merge", "-q", "--no-ff", "-m", "merge the freeze line", "freeze-line")
    return gate_argv(repo, CLAIMS9, "evidence/probe.txt")


def clean_order(ctx, d):
    # the pass path: claims frozen first, the receipt committed afterwards, nothing executed before it
    repo = ctx.init(d / "lane")
    ctx.write(repo / CLAIMS42, "# round 42 - frozen claims\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / M42 / "control.txt", "P10 DEFECT receipt unreadable\n")
    commit(ctx, repo, "freeze")
    ctx.write(repo / PROBE42, RECEIPT_BODY)
    commit(ctx, repo, "first recorded run")
    return gate_argv(repo, CLAIMS42, PROBE42)


FIXTURES = [
    {"fid": "o_clause-freeze-single", "tool": "order", "expect": "reject", "defects": [], "build": xo1_single},
    {"fid": "o_clause-freeze-pair-edited-after", "tool": "order", "expect": "reject", "defects": [],
     "build": xo1_edited_after},
    {"fid": "o_clause-receipt-withdrawn", "tool": "order", "expect": "reject", "defects": [],
     "build": xo3_withdrawn},
    {"fid": "o_clause-receipt-side-line", "tool": "order", "expect": "reject", "defects": [],
     "build": xo3_side_line},
    {"fid": "o_clause-clean-order", "tool": "order", "expect": "accept", "defects": [], "build": clean_order},
]
