"""battery44 module `u14c_name_a` (seat R44BatU14a): order-of-operations fixtures for the frozen order mutant
U14c of `plans/round44_c1_verify.py`.

U14c rewrites `plans/order_check.py:161 if not m:` to `if False:`, so the claims-name guard stops raising and the
advertised `Exit: ... 2 setup error (... unparseable round number, bad arguments)` (`plans/order_check.py:26-27`)
loses its only producer. Every fixture here hands the gate a committed claims BLOB whose file name does not match
`round-<digits>-claims.md` while the rest of the repo is well formed: the reference exits 2 at the guard, the
mutant walks past it and dies later on `m.group(1)` with exit 1 — never 2.

Shapes (deliberately unlike the pre-freeze direction set): a frozen multi-round registry that also holds the
canonical claims file beside the leftover draft it is handed; a lane kept in a subdirectory whose claims name lost
its hyphen, with a merge commit in the middle of its history; a case-shifted root-level claims/receipt pair that
landed in one commit; and one canonical control over the same registry that keeps the gate green, so the only thing
the four fixtures move is the name branch. Each repo is built from nothing with `ctx.init`/`ctx.write`/`ctx.git`;
no lane copy is read, and every path lies inside the fixture directory.

Fixture index (expect = the reference exit: accept 0, error 2; `defects` is always [] because `order_check.py`
prints no `class=` token):

  u14c_name_a-draft-suffix      error   the passed claims path is `plans/round-44-claims.md.draft`
  u14c_name_a-subdir-nohyphen   error   subdirectory lane, claims `plans/round44-claims.md`, merged history
  u14c_name_a-uppercase-pair    error   `ROUND-44-CLAIMS.md` and the receipt in one root-level commit
  u14c_name_a-canonical-control accept  the same registry with the canonical name frozen first
"""


def _commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def _note(tag, count):
    """Ordinary-looking prose, so a claims dir holds content the scan has to read and find nothing in."""
    return "".join(f"{tag} {i:02d}: plain status line, nothing executed here\n" for i in range(count))


CLAIMS44 = "plans/round-44-claims.md"
RECEIPT44 = "corpus/evidence/round44/probe.txt"
RECEIPT_BODY = "cases=14 observed_pass=8 observed_fail=6 mismatches=0\nregrade cases=14 differ=0\n"


def _registry(ctx, repo):
    """Three rounds of frozen claims plus this round's receipt path, as a real lane keeps them."""
    ctx.write(repo / "plans/round-42-claims.md", "# round 42 - frozen claims\n\nFrozen before any recorded run.\n")
    ctx.write(repo / "plans/round-43-claims.md", "# round 43 - frozen claims\n\nFrozen before any recorded run.\n")
    ctx.write(repo / ".ufo/waves/round-42/claims/notes.md", _note("r42", 4))
    ctx.write(repo / ".ufo/waves/round-43/claims/notes.md", _note("r43", 6))
    ctx.write(repo / "corpus/notes/index.md", "corpus index: rounds 42 and 43 recorded\n")
    _commit(ctx, repo, "registry: rounds 42 and 43 frozen")


def build_draft_suffix(ctx, d):
    """U14c: the canonical name is frozen, but the operator passes the leftover `.draft` beside it."""
    repo = ctx.init(d / "registry")
    _registry(ctx, repo)
    ctx.write(repo / CLAIMS44, "# round 44 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / (CLAIMS44 + ".draft"),
              "# round 44 - frozen claims (working draft)\n\nSame text, this copy was being edited.\n")
    ctx.write(repo / ".ufo/waves/round-44/claims/freeze-note.md",
              _note("r44", 8) + "frozen 20:04, the recorded run follows in a later commit\n")
    _commit(ctx, repo, "round 44 freeze, with the working draft left beside it")
    ctx.write(repo / "corpus/notes/round44.md", "round 44 corpus note, nothing executed\n")
    _commit(ctx, repo, "corpus note for round 44")
    ctx.write(repo / RECEIPT44, RECEIPT_BODY)
    _commit(ctx, repo, "first recorded output of round 44")
    return ["--lane", str(repo), "--claims", CLAIMS44 + ".draft", "--receipt", RECEIPT44]


def build_subdir_nohyphen(ctx, d):
    """U14c: the lane lives in a subdirectory and its claims name lost the hyphen, so no round number parses."""
    repo = ctx.init(d / "worktree")
    ctx.write(repo / "plans/round44-claims.md",
              "# round 44 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-44/claims/plan.md", _note("plan", 5))
    _commit(ctx, repo, "freeze on master")
    ctx.git(repo, "checkout", "-q", "-b", "record")
    ctx.write(repo / ".ufo/waves/round-44/claims/record.md", _note("record", 7))
    _commit(ctx, repo, "record branch: status notes")
    ctx.git(repo, "checkout", "-q", "master")
    ctx.write(repo / "corpus/notes/lane.md", "the lane root is this worktree directory\n")
    _commit(ctx, repo, "lane note on master")
    ctx.git(repo, "merge", "-q", "--no-ff", "-m", "merge the record branch", "record")
    ctx.write(repo / "corpus/evidence/round44/receipts/feal-linear-probe.txt", RECEIPT_BODY)
    _commit(ctx, repo, "first recorded output")
    return ["--lane", str(repo), "--claims", "plans/round44-claims.md",
            "--receipt", "corpus/evidence/round44/receipts/feal-linear-probe.txt"]


def build_uppercase_pair(ctx, d):
    """U14c: a case-shifted root-level claims file and its receipt, both added by the very first commit."""
    repo = ctx.init(d / "lane")
    ctx.write(repo / "ROUND-44-CLAIMS.md",
              "# round 44 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / "evidence/probe.txt", RECEIPT_BODY)
    ctx.write(repo / "notes.md", _note("root", 3))
    _commit(ctx, repo, "freeze and first recorded output in one commit")
    ctx.write(repo / "README.md", "a two-commit lane; the second commit touches nothing the gate reads\n")
    _commit(ctx, repo, "readme")
    return ["--lane", str(repo), "--claims", "ROUND-44-CLAIMS.md", "--receipt", "evidence/probe.txt"]


def build_canonical_control(ctx, d):
    """Control: the canonical name, frozen before its receipt; the name branch is never reached and the gate passes."""
    repo = ctx.init(d / "control")
    _registry(ctx, repo)
    ctx.write(repo / CLAIMS44, "# round 44 - frozen claims\n\nFrozen before any recorded output exists.\n")
    ctx.write(repo / ".ufo/waves/round-44/claims/freeze-note.md", _note("ctl", 8))
    _commit(ctx, repo, "round 44 freeze, canonical name")
    ctx.write(repo / RECEIPT44, RECEIPT_BODY)
    _commit(ctx, repo, "first recorded output of round 44")
    return ["--lane", str(repo), "--claims", CLAIMS44, "--receipt", RECEIPT44]


FIXTURES = [
    # the canonical file is frozen correctly, but the path handed to the gate is the `.draft` copy beside it
    {"fid": "u14c_name_a-draft-suffix", "tool": "order", "expect": "error", "defects": [],
     "build": build_draft_suffix},
    # same branch from a subdirectory lane whose claims name has no hyphen, reached through a merge commit
    {"fid": "u14c_name_a-subdir-nohyphen", "tool": "order", "expect": "error", "defects": [],
     "build": build_subdir_nohyphen},
    # the name is case-shifted and lives at the root, with the receipt in the same first commit
    {"fid": "u14c_name_a-uppercase-pair", "tool": "order", "expect": "error", "defects": [],
     "build": build_uppercase_pair},
    # control: the canonical name on the same registry keeps the gate green, so the name is the only mover
    {"fid": "u14c_name_a-canonical-control", "tool": "order", "expect": "accept", "defects": [],
     "build": build_canonical_control},
]
