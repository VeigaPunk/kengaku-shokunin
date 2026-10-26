"""battery42 fixtures for the claims scan of `plans/order_check.py` (frozen mutants XO5, XO6, XO7).

Every repo is built from nothing with the counter's ctx helpers: a claims file and one or more blobs
under the round's claims directory, then the receipt commit, then (XO5) one further commit. Six
single-purpose fixtures, two per branch:

  XO5  the scan reads blobs up to the receipt commit, not to HEAD          (post-receipt additions)
  XO6  a gate verdict line alternation of DEFECT|ok, never PASS            (widened alternation)
  XO7  a `CASE ... observed=<value>` line matches any observed value       (narrowed value)

Shapes differ from the pre-freeze direction modules on purpose: new path vs amended path, a
multi-row verdict registry, the `gate: ` echo prefix next to an excused P10 DEFECT line, a
multi-row receipt echo, and a round-38 claims directory. Stdlib only.
"""

CLAIMS_42 = "plans/round-42-claims.md"
DIR_42 = ".ufo/waves/round-42/claims"
RECEIPT = "corpus/evidence/round42/fibsqrt-probe.txt"

HONEST = ("MUTANTS total=14 killed=0 survived=14\n"
          "MUTANTS-BY-TOOL anchor=0/9 order=0/5\n")


def _commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def _freeze(ctx, repo, claims, blobs, header):
    ctx.write(repo / claims, header)
    for rel, text in blobs.items():
        ctx.write(repo / rel, text)
    _commit(ctx, repo, "freeze: round claims and controls")
    return repo


def _receipt(ctx, repo):
    ctx.write(repo / RECEIPT,
              "cases=16 observed_pass=7 observed_fail=9 mismatches=0\n"
              "regrade cases=16 differ=0\n")
    _commit(ctx, repo, "receipt: first recorded probe run")


def _later(ctx, repo, rel, text, message):
    ctx.write(repo / rel, text)
    _commit(ctx, repo, message)


def _args(repo, claims):
    return ["--lane", str(repo), "--claims", claims, "--receipt", RECEIPT]


def xo5_new_path(ctx, d):
    # XO5: a claims/ verdict file committed AFTER the receipt shows P10 ok; the reference stops at the receipt.
    r = ctx.init(d / "repo")
    _freeze(ctx, r, CLAIMS_42,
            {f"{DIR_42}/control-c1-nothing.txt": HONEST,
             f"{DIR_42}/frozen-digests.txt": "plans/order_check.py 948d5e1d\n"},
            "# Round 42 frozen claims\n\norder of operations: dry run only before this commit\n")
    _receipt(ctx, r)
    _later(ctx, r, f"{DIR_42}/rerun-verdicts.txt",
           "# verdicts written after the receipt commit\n"
           "P10 ok fresh probe output is byte-equal to the receipt\n",
           "rerun verdicts")
    return _args(r, CLAIMS_42)


def xo5_amended(ctx, d):
    # XO5 second trigger: the SAME claims/ path is amended after the receipt (new blob, no new file name).
    r = ctx.init(d / "repo")
    rel = f"{DIR_42}/control-c1-nothing.txt"
    _freeze(ctx, r, CLAIMS_42, {rel: HONEST},
            "# Round 42 frozen claims\n\nbaseline tip recorded by the planner seat\n")
    _receipt(ctx, r)
    _later(ctx, r, rel, HONEST + "gate: P10 ok rerun exit=0\n", "amend the do-nothing control")
    return _args(r, CLAIMS_42)


def xo6_pass_row(ctx, d):
    # XO6: a freeze-time registry row `P10 PASS ...` is not a gate verdict the gate prints; the reference ignores it.
    r = ctx.init(d / "repo")
    _freeze(ctx, r, CLAIMS_42,
            {f"{DIR_42}/c1-verdicts.txt":
             "# C1 verdict registry\n"
             "P10 DEFECT receipt unreadable\n"
             "P10 PASS probe executed twice\n"
             "advertised rows priced=0\n"},
            "# Round 42 frozen claims\n\nverdict registry frozen with this file\n")
    _receipt(ctx, r)
    return _args(r, CLAIMS_42)


def xo6_echoed_pass(ctx, d):
    # XO6 second trigger: echo-prefixed `gate: P10 PASS ...`, next to the excused `gate: P10 DEFECT receipt unreadable`.
    r = ctx.init(d / "repo")
    _freeze(ctx, r, CLAIMS_42,
            {f"{DIR_42}/gate-echo.txt":
             "gate: P10 DEFECT receipt unreadable\n"
             "gate: P10 PASS receipt unreadable\n"
             "gate: P2 ok receipt readable\n"},
            "# Round 42 frozen claims\n\ngate echo captured by the planner seat\n")
    _receipt(ctx, r)
    return _args(r, CLAIMS_42)


def xo7_timeouts(ctx, d):
    # XO7: a multi-row receipt echo whose observed= values are timeout/skip/error, never pass|fail.
    r = ctx.init(d / "repo")
    _freeze(ctx, r, CLAIMS_42,
            {f"{DIR_42}/probe-echo.txt":
             "stagecheck cases=16 failed=0\n"
             "CASE lookup-28 observed=timeout rc=timeout\n"
             "CASE oracle observed=skip rc=0\n"
             "CASE nop observed=error rc=3\n"},
            "# Round 42 frozen claims\n\nstage check echo, probe not yet run\n")
    _receipt(ctx, r)
    return _args(r, CLAIMS_42)


def xo7_skipped_r38(ctx, d):
    # XO7 second trigger: a round-38 claims directory with one `observed=skipped` row (neither pass nor fail).
    claims = "plans/round-38-claims.md"
    cdir = ".ufo/waves/round-38/claims"
    r = ctx.init(d / "repo")
    _freeze(ctx, r, claims,
            {f"{cdir}/control-c2-nothing.txt": "checks=9 defects=0\nCASE c7 observed=skipped\n"},
            "# Round 38 frozen claims\n\nred as required control\n")
    _receipt(ctx, r)
    return _args(r, claims)


FIXTURES = [
    {"fid": "o_scan-xo5-post-receipt-verdicts", "tool": "order", "expect": "accept", "defects": [],
     "build": xo5_new_path},
    {"fid": "o_scan-xo5-amended-claims-blob", "tool": "order", "expect": "accept", "defects": [],
     "build": xo5_amended},
    {"fid": "o_scan-xo6-pass-verdict-row", "tool": "order", "expect": "accept", "defects": [],
     "build": xo6_pass_row},
    {"fid": "o_scan-xo6-echoed-pass-row", "tool": "order", "expect": "accept", "defects": [],
     "build": xo6_echoed_pass},
    {"fid": "o_scan-xo7-timeout-rows", "tool": "order", "expect": "reject", "defects": [],
     "build": xo7_timeouts},
    {"fid": "o_scan-xo7-skipped-row-r38", "tool": "order", "expect": "reject", "defects": [],
     "build": xo7_skipped_r38},
]
