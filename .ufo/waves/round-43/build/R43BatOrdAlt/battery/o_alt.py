"""battery43 module `o_alt` (seat R43BatOrdAlt): six order-of-operations fixtures for the frozen
order mutants NO5, NO7 and NO22 of `plans/round43_c1_verify.py`.

Every repo is built from nothing with `ctx.init`/`ctx.write`/`ctx.git`; no lane clone is used and every
path stays inside the fixture directory. Shapes chosen here are deliberately unlike the freeze-direction set:
histories of five and six commits, blobs edited in place, forbidden lines buried in multi-line prose,
receipts three directories deep, several claims files per repo, and the bare / echoed / prefixed forms
of one gate line each kept apart so the branch under test is the only thing that moves.

Fixture index (accept = reference exits 0, reject = reference exits 1; `defects` is always [] because
`order_check.py` prints no `class=` token):

  o_alt-late-case-blob        NO5   the CASE-shaped line lands in a claims blob added by commit 3
  o_alt-inplace-gate-rewrite  NO5   the same claims blob is rewritten at commit 4 and only then carries P10
  o_alt-fenced-echo           NO7   `P10 DEFECT receipt unreadable: <path>` inside a fenced transcript
  o_alt-two-echo-blobs        NO7   two blobs, two commits, both carrying the echoed excuse
  o_alt-bare-ok-late          NO22  a bare `P10 ok` (empty detail) added by a later edit of one blob
  o_alt-prefixed-ok-blob      NO22  `gate: P10 ok <detail>` inside a larger blob added later
"""


def _commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def _prose(tag, count):
    """Ordinary-looking lines so a forbidden one sits inside a larger blob."""
    return "".join(f"{tag} {i:02d}: ordinary prose kept beside the decisive line\n" for i in range(count))


def build_late_case_blob(ctx, d):
    """NO5: `for commit in commits[:1]` (oldest claims commit only) misses a blob added at commit 3."""
    repo = ctx.init(d / "registry")
    ctx.write(repo / "plans/round-51-claims.md",
              "# round 51 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-51/claims/freeze-note.md", "frozen 09:10; nothing executed yet\n")
    _commit(ctx, repo, "freeze")
    ctx.write(repo / "corpus/notes/index.md", "an unrelated corpus note\n")
    _commit(ctx, repo, "corpus note")
    ctx.write(repo / ".ufo/waves/round-51/claims/journal.md",
              _prose("journal-a", 14) + "CASE caplen observed=pass rc=0 elapsed=31s\n" + _prose("journal-b", 14))
    _commit(ctx, repo, "journal: recorded output pasted in before the receipt lands")
    ctx.write(repo / "corpus/evidence/round51/receipts/probe.txt",
              "cases=9 observed_pass=7 observed_fail=2 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-51-claims.md",
            "--receipt", "corpus/evidence/round51/receipts/probe.txt"]


def build_inplace_gate_rewrite(ctx, d):
    """NO5: the same shape from the other side - one blob, rewritten in a later commit, gate line then added."""
    repo = ctx.init(d / "history")
    ctx.write(repo / "plans/round-52-claims.md",
              "# round 52 - frozen claims\n\nFrozen before any recorded output exists.\n")
    journal = repo / ".ufo/waves/round-52/claims/journal.md"
    ctx.write(journal, "phase 1: frozen\n")
    _commit(ctx, repo, "freeze")
    ctx.write(repo / "corpus/notes/a.md", "first unrelated note\n")
    _commit(ctx, repo, "note a")
    ctx.write(repo / "corpus/notes/b.md", "second unrelated note\n")
    _commit(ctx, repo, "note b")
    ctx.write(journal, "phase 1: frozen\nphase 2: the gate spoke before the recorded output\n"
                       "P10 ok fresh probe output is byte-equal to the receipt\n")
    _commit(ctx, repo, "journal: phase 2 carries the gate line")
    ctx.write(repo / "corpus/evidence/round52/receipts/probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-52-claims.md",
            "--receipt", "corpus/evidence/round52/receipts/probe.txt"]


def build_fenced_echo(ctx, d):
    """NO7: `EXECUTED_EXCUSE` tightened to the bare form; the echoed `receipt unreadable: <path>` flips to a hit."""
    repo = ctx.init(d / "gate")
    ctx.write(repo / "plans/round-53-claims.md",
              "# round 53 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-53/claims/checks.md", "P7 ok pins\nP8 ok capture digests match\n")
    _commit(ctx, repo, "freeze")
    ctx.write(repo / "corpus/notes/c.md", "unrelated note\n")
    _commit(ctx, repo, "note c")
    transcript = ("```\n"
                  "P7 ok pins\n"
                  "P8 ok capture digests match\n"
                  "P10 DEFECT receipt unreadable\n"
                  "gate: P10 DEFECT receipt unreadable: corpus/evidence/round53/receipts/probe.txt\n"
                  "```\n")
    ctx.write(repo / ".ufo/waves/round-53/claims/transcript.md", transcript)
    _commit(ctx, repo, "transcript of the gate's refusal, echoed path included")
    ctx.write(repo / "corpus/evidence/round53/receipts/probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-53-claims.md",
            "--receipt", "corpus/evidence/round53/receipts/probe.txt"]


def build_two_echo_blobs(ctx, d):
    """NO7: the echoed excuse in two separate blobs of one round, two commits apart, different layouts."""
    repo = ctx.init(d / "double")
    ctx.write(repo / "plans/round-54-claims.md",
              "# round 54 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-54/claims/a.md",
              "P10 DEFECT receipt unreadable: corpus/evidence/round54/probe.txt\n")
    _commit(ctx, repo, "freeze with the first echo")
    ctx.write(repo / "corpus/notes/d.md", "unrelated note\n")
    _commit(ctx, repo, "note d")
    ctx.write(repo / ".ufo/waves/round-54/claims/nested/b.md",
              _prose("echo", 6) + "gate: P10 DEFECT receipt unreadable: "
                                  "corpus/evidence/round54/receipts/deep/probe.txt\n")
    _commit(ctx, repo, "second echo blob")
    ctx.write(repo / "corpus/notes/e.md", "one more unrelated note\n")
    _commit(ctx, repo, "note e")
    ctx.write(repo / "corpus/evidence/round54/receipts/deep/probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-54-claims.md",
            "--receipt", "corpus/evidence/round54/receipts/deep/probe.txt"]


def build_bare_ok_late(ctx, d):
    """NO22: `if m:` disabled leaves only CASE lines; a bare `P10 ok` with no detail must still be a hit."""
    repo = ctx.init(d / "bare")
    ctx.write(repo / "plans/round-55-claims.md",
              "# round 55 - frozen claims\n\nFrozen before any recorded output exists.\n")
    notes = repo / ".ufo/waves/round-55/claims/notes.md"
    ctx.write(notes, "phase 1: frozen\n")
    _commit(ctx, repo, "freeze")
    ctx.write(repo / "corpus/notes/f.md", "unrelated note\n")
    _commit(ctx, repo, "note f")
    ctx.write(notes, _prose("notes", 18) + "P10 ok\n")
    _commit(ctx, repo, "notes: the gate line added in a later edit")
    ctx.write(repo / "corpus/notes/g.md", "another unrelated note\n")
    _commit(ctx, repo, "note g")
    ctx.write(repo / "corpus/evidence/round55/receipts/deep/one/probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-55-claims.md",
            "--receipt", "corpus/evidence/round55/receipts/deep/one/probe.txt"]


def build_prefixed_ok_blob(ctx, d):
    """NO22: the `gate: ` echo prefix plus a non-excuse detail, inside a larger blob added by a later commit."""
    repo = ctx.init(d / "prefixed")
    ctx.write(repo / "plans/round-56-claims.md",
              "# round 56 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-56/claims/checks.md", "P1 ok pins\nP2 ok digests\n")
    _commit(ctx, repo, "freeze")
    ctx.write(repo / "corpus/notes/h.md", "unrelated note\n")
    _commit(ctx, repo, "note h")
    ctx.write(repo / ".ufo/waves/round-56/claims/deep/log.md",
              _prose("log-a", 5) + "gate: P10 ok fresh probe output is not byte-equal to the receipt\n"
              + _prose("log-b", 5))
    _commit(ctx, repo, "log blob added before the receipt")
    ctx.write(repo / "corpus/evidence/round56/receipts/nested/probe.txt",
              "cases=12 observed_pass=8 observed_fail=4 mismatches=0\n")
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round-56-claims.md",
            "--receipt", "corpus/evidence/round56/receipts/nested/probe.txt"]


FIXTURES = [
    # NO5: reference sees the CASE line in the blob added by commit 3 and rejects; commits[:1] sees only commit 1.
    {"fid": "o_alt-late-case-blob", "tool": "order", "expect": "reject", "defects": [],
     "build": build_late_case_blob},
    # NO5 through the other door: one blob, clean at the freeze commit, carrying P10 at a later commit.
    {"fid": "o_alt-inplace-gate-rewrite", "tool": "order", "expect": "reject", "defects": [],
     "build": build_inplace_gate_rewrite},
    # NO7: the echoed excuse path is the advertised exception; tightening the regex turns it into a hit.
    {"fid": "o_alt-fenced-echo", "tool": "order", "expect": "accept", "defects": [],
     "build": build_fenced_echo},
    # NO7 with two blobs and a deeper receipt: either blob alone must keep the lane green.
    {"fid": "o_alt-two-echo-blobs", "tool": "order", "expect": "accept", "defects": [],
     "build": build_two_echo_blobs},
    # NO22: no CASE line anywhere, so disabling the gate-line branch empties the hit list.
    {"fid": "o_alt-bare-ok-late", "tool": "order", "expect": "reject", "defects": [],
     "build": build_bare_ok_late},
    # NO22 with the `gate: ` prefix and a sentence detail in a larger blob.
    {"fid": "o_alt-prefixed-ok-blob", "tool": "order", "expect": "reject", "defects": [],
     "build": build_prefixed_ok_blob},
]
