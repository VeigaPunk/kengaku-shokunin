"""Round-43 battery43 module `o_scan` (order gate): forbidden evidence that only a LATER claims commit carries,
and a reject repo whose only forbidden evidence is a gate `P10` line.

Each fixture builds one small lane from nothing: the round's claims file, sibling artefacts under the round's
claims directory, and the probe receipt. The lane repository IS the fixture directory and the gate is called with
`--lane .`, so the gate resolves its root at the fixture dir itself (not at a subdirectory of it). Claims and
receipt are named repo-relative. `defects` is always empty: the order gate reports through its exit code only.
"""

CLAIMS = "plans/round-43-claims.md"
RECEIPT = "corpus/evidence/round43/probe.txt"
CLAIMS_DIR = ".ufo/waves/round-43/claims"

HEAD = """# Round 43 — claims (fixture)

Baseline lane tip `317148c4b918fb2645e46ec0225cac720a8a57e9`.

**Order of operations.** The probe ran only as `--dry` and `--stage-check` before this file was committed.

## C1 — calibration

Nine advertised behaviours; the battery lives in `plans/battery43/`.
"""

RECEIPT_BODY = "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n"


def _init(ctx, d):
    """Init the lane repo at the fixture dir itself and return the gate argv tail."""
    ctx.init(d)
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", RECEIPT]


def _commit(ctx, d, message):
    ctx.git(d, "add", "-A")
    ctx.git(d, "commit", "-q", "-m", message)


def _n5a(ctx, d):
    """A gate `P10 ok` line enters as a NEW claims artefact in the second claims commit; the freeze commit and
    its two siblings stay clean, so only a scan past the oldest commit can reject."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD + "\n## Controls\n\n`control-c1-nothing.txt`: no battery exists yet.\n")
    ctx.write(d / CLAIMS_DIR / "control-c1-nothing.txt",
              "MUTANTS total=9 killed=0 survived=9\nPREDICATE C1 fail\n")
    ctx.write(d / CLAIMS_DIR / "c2-stage-check.txt", "stagecheck cases=12 failed=0\n")
    _commit(ctx, d, "freeze: round-43 claims")
    ctx.write(d / CLAIMS_DIR / "gate-transcript.txt",
              "gate: P2 receipt is readable\nP10 ok fresh probe output is byte-equal to the receipt\n")
    _commit(ctx, d, "claims: gate transcript for the C2 control")
    ctx.write(d / RECEIPT, RECEIPT_BODY)
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


def _n5b(ctx, d):
    """A five-commit history where ONE claims artefact is rewritten twice (the line arriving in the third
    commit, a clean artefact landing fourth) and the receipt last: the path's first-seen blob is clean."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD)
    ctx.write(d / CLAIMS_DIR / "control-c1-nothing.txt", "MUTANTS total=9 killed=0 survived=9\n")
    _commit(ctx, d, "freeze: round-43 claims")
    ctx.write(d / CLAIMS_DIR / "control-c1-nothing.txt", "MUTANTS total=9 killed=0 survived=9\n"
              "PREDICATE C1 fail\n")
    _commit(ctx, d, "claims: control verdict line")
    ctx.write(d / CLAIMS_DIR / "control-c1-nothing.txt", "MUTANTS total=9 killed=0 survived=9\n"
              "PREDICATE C1 fail\n"
              "P10 DEFECT fresh probe output is not byte-equal to the receipt\n")
    _commit(ctx, d, "claims: append the gate line")
    ctx.write(d / CLAIMS_DIR / "c1_controls.txt", "control-c1-no-mutants: PREDICATE C1 fail\n")
    _commit(ctx, d, "claims: sibling control file")
    ctx.write(d / RECEIPT, RECEIPT_BODY + "regrade cases=12 differ=0\n")
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


def _n5c(ctx, d):
    """The second trigger of the same branch: a receipt-shaped `CASE ... observed=` line enters in the third
    claims commit as a captured probe output, with a clean artefact added in the second."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD)
    _commit(ctx, d, "freeze: round-43 claims")
    ctx.write(d / CLAIMS_DIR / "control-c1-nothing.txt", "MUTANTS total=9 killed=0 survived=9\n")
    _commit(ctx, d, "claims: do-nothing control")
    ctx.write(d / CLAIMS_DIR / "probe-output.txt", "CASE r43-a1 observed=PASS wrong=0\n")
    _commit(ctx, d, "claims: captured probe output")
    ctx.write(d / RECEIPT, RECEIPT_BODY)
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


def _n22a(ctx, d):
    """A reject repo whose only forbidden evidence is a `P10 ok` line in a sibling gate log inside the freeze
    commit; no `CASE` line exists anywhere, so only the gate-line branch can reject."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD)
    ctx.write(d / CLAIMS_DIR / "gate-only.log",
              "gate: P2 receipt is readable\nP10 ok fresh probe output is byte-equal to the receipt\n")
    _commit(ctx, d, "freeze: round-43 claims and the gate log")
    ctx.write(d / RECEIPT, RECEIPT_BODY)
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


def _n22b(ctx, d):
    """The second trigger: an echoed `gate: P10 DEFECT fresh probe exit=1` line in a claims artefact of the
    freeze commit (DEFECT variant, echo prefix), with the receipt in its own later commit."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD)
    ctx.write(d / CLAIMS_DIR / "gate-transcript.txt",
              "gate: P2 receipt is readable\ngate: P10 DEFECT fresh probe exit=1\n")
    _commit(ctx, d, "freeze: round-43 claims and the gate transcript")
    ctx.write(d / RECEIPT, RECEIPT_BODY)
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


def _n22c(ctx, d):
    """A gate log whose `P10 ok` line is indented under a heading in the freeze commit, followed by a second
    claims commit that adds an unrelated artefact (the gate branch, not commit depth, decides)."""
    argv = _init(ctx, d)
    ctx.write(d / CLAIMS, HEAD)
    ctx.write(d / CLAIMS_DIR / "skip-control.txt",
              "skip control transcript\n  P10 ok receipt matches the committed bytes\n")
    _commit(ctx, d, "freeze: round-43 claims and the skip control")
    ctx.write(d / CLAIMS_DIR / "envelope.txt", "ENVELOPE local_bin_content unchanged\n")
    _commit(ctx, d, "claims: envelope line")
    ctx.write(d / RECEIPT, RECEIPT_BODY)
    _commit(ctx, d, "receipt: first recorded probe run")
    return argv


FIXTURES = [
    # NO5 shape 1: gate P10 line in a NEW claims file committed second (oldest commit is clean)
    {"fid": "o_scan-n5a-late-gate-file", "tool": "order", "expect": "reject", "defects": [], "build": _n5a},
    # NO5 shape 2: five commits; one artefact rewritten twice, the P10 DEFECT line only in the third
    {"fid": "o_scan-n5b-amended-claims", "tool": "order", "expect": "reject", "defects": [], "build": _n5b},
    # NO5 shape 3: receipt-shaped CASE line in a third claims commit (same branch, other pattern)
    {"fid": "o_scan-n5c-case-third-commit", "tool": "order", "expect": "reject", "defects": [], "build": _n5c},
    # NO22 shape 1: gate-P10-only evidence in a sibling log of the freeze commit, no CASE line at all
    {"fid": "o_scan-n22a-gate-only", "tool": "order", "expect": "reject", "defects": [], "build": _n22a},
    # NO22 shape 2: echoed `gate: P10 DEFECT fresh probe exit=1` in a claims artefact of the freeze commit
    {"fid": "o_scan-n22b-echoed-defect", "tool": "order", "expect": "reject", "defects": [], "build": _n22b},
    # NO22 shape 3: indented P10 ok line plus a later clean claims commit
    {"fid": "o_scan-n22c-indented-gate", "tool": "order", "expect": "reject", "defects": [], "build": _n22c},
]
