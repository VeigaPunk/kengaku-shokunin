"""battery43 module `o_excuse` (seat R43BatOrdExcuse): the order gate's single pre-execution excuse.

Frozen mutant NO7 narrows `EXECUTED_EXCUSE` in `plans/order_check.py` from `^receipt unreadable(?:: \\S+)?$` to
`^receipt unreadable$`, so the P2-shaped echo (`receipt unreadable: <path>`) stops counting as the "nothing ran yet"
excuse. On a claims blob carrying that echo the reference gate sees no hit and accepts (exit 0); the mutant sees a
`probe-executed-before-receipt` hit and rejects (exit 1). Declared direction `rc-mirror`.

Two killers reach the branch in different shapes -- the echo in the freeze commit's own claims file, and the
`gate: `-prefixed echo committed while the claims file itself stays clean -- plus one control the reference and the
mutant both accept (the bare sentence with no path), which pins the difference to the echoed path and not to the
`P10 DEFECT` sentence. Order fixtures declare `defects` [] (the gate prints no `DEFECT class=` lines).

Every build() fills its empty directory `d` with a repository of its own and returns the tool argv tail.
"""

CLAIMS_DIR = ".ufo/waves/round-43/claims"
CLAIMS = CLAIMS_DIR + "/round-43-claims.md"

# The freeze commit's own claims file. The gate output is quoted verbatim in a fenced block: this is the exact
# shape the do-nothing control writes when no receipt exists yet (echoed with the path the gate was given).
ECHO_CLAIMS = """# Round 43 — frozen claims (fixture o_excuse-echo)

Freeze precedes the first recorded run; nothing below may be edited after this commit.

## Order of operations

The gate was invoked once while no receipt existed on disk. Its one line, before anything executed:

```
    P10 DEFECT receipt unreadable: corpus/evidence/round-43/feal-probe.txt
```

## C1 — calibration (planned)

| item | axis | plan |
|------|------|------|
| C1 | calibration | nine carried near-variants |
| C2 | coverage | pinned grader entry |

## C2 — coverage (planned)

Twelve constructed cases, graded by the frozen probe; the receipt follows this file.
"""

# A claims file that carries no gate output at all, so the second killer's only hook is the later blob.
CLEAN_CLAIMS = """# Round 43 — frozen claims (fixture o_excuse-gate-prefix)

Freeze precedes the first recorded run.

## Order of operations

The claims directory records the stage check only; no gate line is quoted in this file.
"""

# A later claims transcript: the gate line arrives with the `gate: ` echo prefix the C2 counter adds.
GATE_PREFIX = "gate: P10 DEFECT receipt unreadable: evidence/round43/feal-probe.txt\n"

# The reference tool's own pre-execution sentence, with no echoed path.
BARE = """Round 43 control transcript (fixture o_excuse-bare)

The gate was invoked with no receipt on disk and printed exactly its pre-execution sentence:

```
    P10 DEFECT receipt unreadable
```

Nothing executed: no probe output was produced, so no case line exists.
"""


def land(ctx, repo, note):
    """Stage everything and commit it as `fixture` (Ctx pins the identity and the date)."""
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", note)


def echo_in_freeze_claims(ctx, d):
    """Killer 1: a multi-commit lane whose freeze commit's own claims file echoes `receipt unreadable: <path>`.

    Shape: repo at the fixture root, three claims blobs at freeze, a wave-1 control blob and a corpus receipt later.
    """
    repo = ctx.init(d)
    ctx.write(repo / CLAIMS_DIR / "control-c1-nothing.txt",
              "BATTERY fixtures=0\nMUTANTS total=9 killed=0 survived=9\nPREDICATE C1 fail\n")
    ctx.write(repo / CLAIMS_DIR / "c2-stage-check.txt", "stagecheck cases=12 failed=0\n")
    ctx.write(repo / CLAIMS, ECHO_CLAIMS)
    land(ctx, repo, "freeze: claims committed before any recorded run")
    ctx.write(repo / CLAIMS_DIR / "control-c1-mirror-as-battery.txt",
              "MUTANTS total=9 killed=9 survived=0\nPREDICATE C1 pass\n")
    land(ctx, repo, "wave-1 control runs, still before the recorded run")
    ctx.write(repo / "corpus/evidence/round-43/feal-probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\nregrade cases=12 differ=0\n")
    land(ctx, repo, "first recorded run")
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", "corpus/evidence/round-43/feal-probe.txt"]


def gate_prefix_late_blob(ctx, d):
    """Killer 2: the `gate: `-prefixed echo with a relative path enters a claims blob in a LATER commit.

    Shape: the claims file stays clean, the hook is a separate transcript blob, and the echoed path never exists.
    """
    repo = ctx.init(d)
    ctx.write(repo / CLAIMS, CLEAN_CLAIMS)
    land(ctx, repo, "freeze")
    ctx.write(repo / CLAIMS_DIR / "c2-stage-check.txt", "stagecheck cases=12 failed=0\n")
    land(ctx, repo, "stage check recorded before the run")
    ctx.write(repo / CLAIMS_DIR / "control-c2-nothing.txt", GATE_PREFIX)
    land(ctx, repo, "do-nothing control transcript appended")
    ctx.write(repo / "corpus/evidence/round43/feal-probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    land(ctx, repo, "first recorded run")
    return ["--lane", ".", "--claims", CLAIMS, "--receipt", "corpus/evidence/round43/feal-probe.txt"]


def bare_sentence_control(ctx, d):
    """Control: the bare `receipt unreadable` sentence, which the reference and mutant both excuse (no kill).

    Shape: the claims directory holds one transcript blob and the claims file lives outside it.
    """
    repo = ctx.init(d)
    ctx.write(repo / "plans/round-43-claims.md",
              "# Round 43 — frozen claims (fixture o_excuse-bare)\n\nFreeze precedes the recorded run.\n")
    ctx.write(repo / CLAIMS_DIR / "control.txt", BARE)
    land(ctx, repo, "freeze")
    ctx.write(repo / "corpus/evidence/round-43/probe.txt", "cases=12 observed_pass=8 observed_fail=4\n")
    land(ctx, repo, "first recorded run")
    return ["--lane", ".", "--claims", "plans/round-43-claims.md",
            "--receipt", "corpus/evidence/round-43/probe.txt"]


FIXTURES = [
    {"fid": "o_excuse-echo-freeze-claims", "tool": "order", "expect": "accept", "defects": [],
     "build": echo_in_freeze_claims},
    {"fid": "o_excuse-gate-prefix-late", "tool": "order", "expect": "accept", "defects": [],
     "build": gate_prefix_late_blob},
    {"fid": "o_excuse-bare-excused", "tool": "order", "expect": "accept", "defects": [],
     "build": bare_sentence_control},
]
