"""battery44 module `u14c_name_b` (seat R44BatU14b): the order gate's claims-name guard.

`plans/order_check.py:161-162` normalizes `--claims` and then refuses a file name its pattern
`^round-(\\d+)-claims\\.md$` does not match: `raise SetupError("claims file name is not
round-NN-claims.md: ...")`, which `main` turns into exit 2 (`Exit: 0 order holds · 1 order broken ·
2 setup error`, order_check.py:26-27). Frozen mutant U14c replaces `if not m:` with `if False:`, so
the guard is dead and the next statement dereferences the None match: the gate dies with exit 1.
Declared direction `error` -- reference 2, mutant 0 or 1 -- and `defects` is [] for every fixture,
because the order gate reports through its exit code only.

Every repo is built from nothing with `ctx.init`/`ctx.write`/`ctx.git`; no lane clone is read and
every path stays inside the fixture directory. Each fixture keeps the rest of the lane answerable --
claims and receipt are blobs at HEAD of a repo that is its own toplevel inside the fixture -- so the
guard is the only thing that moves, and the four histories share no shape with one another.

Fixture index (all `error`: the reference refuses the claims name, exit 2):
  u14c_name_b-registry-suffix     four-round registry, six commits, claims landed as `.md.orig`
  u14c_name_b-nested-uppercase    claims two directories deep with a capitalised file name
  u14c_name_b-round-xx-token      `round-xx-claims.md`, receipt committed before the claims file
  u14c_name_b-underscore-name     `round_44_claims.md`, one commit carries claims and receipt
"""


def _commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def build_registry_suffix(ctx, d):
    """A four-round registry over six commits; the new claims landed under the editor's `.orig` name."""
    repo = ctx.init(d / "registry")
    ctx.write(repo / "plans/registry.md",
              "# round registry, frozen\n\n"
              "| round | lane | axis | claims |\n"
              "|---|---|---|---|\n"
              "| 48 | kengaku | calibration | plans/round-48-claims.md |\n"
              "| 49 | kengaku | coverage | plans/round-49-claims.md |\n"
              "| 50 | kengaku | depth | plans/round-50-claims.md |\n")
    ctx.write(repo / "plans/round-50-claims.md", "# round 50 - frozen claims\n\nheld at the tip\n")
    _commit(ctx, repo, "registry: rounds 48-50 with the round-50 claims")
    ctx.write(repo / "plans/round-51-claims.md.orig",
              "# round 51 - frozen claims\n\n"
              "Written and frozen before any plans/battery44 fixture exists.\n")
    ctx.write(repo / ".ufo/waves/round-51/claims/freeze-note.md", "frozen 09:12; nothing executed yet\n")
    _commit(ctx, repo, "round 51: the claims file, saved by the editor as .orig")
    ctx.write(repo / "corpus/notes/round-51.md", "a corpus note carried beside the round\n")
    _commit(ctx, repo, "corpus note")
    ctx.write(repo / "plans/round-51-plan.md", "## plan\n\nfive mutants, one battery module\n")
    _commit(ctx, repo, "round 51 plan")
    ctx.write(repo / "corpus/evidence/round51/receipts/feal-linear-probe.txt",
              "cases=14 observed_pass=8 observed_fail=6 mismatches=0\n")
    _commit(ctx, repo, "round 51: first recorded output")
    ctx.write(repo / "plans/registry.md",
              "# round registry, frozen\n\n"
              "| round | lane | axis | claims |\n"
              "|---|---|---|---|\n"
              "| 48 | kengaku | calibration | plans/round-48-claims.md |\n"
              "| 49 | kengaku | coverage | plans/round-49-claims.md |\n"
              "| 50 | kengaku | depth | plans/round-50-claims.md |\n"
              "| 51 | kengaku | operability | plans/round-51-claims.md.orig |\n")
    _commit(ctx, repo, "registry: the round-51 row")
    return ["--lane", str(repo), "--claims", "plans/round-51-claims.md.orig",
            "--receipt", "corpus/evidence/round51/receipts/feal-linear-probe.txt"]


def build_nested_uppercase(ctx, d):
    """Claims two directories deep with a capitalised name; the same guard, a different path shape."""
    repo = ctx.init(d / "history")
    ctx.write(repo / "notes/history/README.md", "kept for the rounds before the claims pattern existed\n")
    ctx.write(repo / "notes/history/Round-7-claims.md", "# Round 7 - frozen claims\n\nFrozen before the run.\n")
    _commit(ctx, repo, "history: the round-7 claims, capitalised by hand")
    ctx.write(repo / ".ufo/waves/round-7/claims/order.md", "P7 ok pins\nP8 ok digests match\n")
    _commit(ctx, repo, "round 7 checks")
    ctx.write(repo / "corpus/evidence/round7/feal-linear-probe.txt", "cases=9 observed_pass=6 observed_fail=3\n")
    _commit(ctx, repo, "round 7: first recorded output")
    ctx.write(repo / "notes/history/README.md",
              "kept for the rounds before the claims pattern existed\n\nround 7 added\n")
    _commit(ctx, repo, "history: README note")
    return ["--lane", str(repo), "--claims", "notes/history/Round-7-claims.md",
            "--receipt", "corpus/evidence/round7/feal-linear-probe.txt"]


def build_round_xx_token(ctx, d):
    """A name with no digits at all, in a lane whose receipt commit precedes the claims commit."""
    repo = ctx.init(d / "inverted")
    ctx.write(repo / "corpus/evidence/round46/feal-linear-probe.txt", "cases=11 observed_pass=7 observed_fail=4\n")
    _commit(ctx, repo, "round 46: recorded output landed first")
    ctx.write(repo / "plans/round-xx-claims.md", "# round xx - frozen claims\n\nThe round number was never settled.\n")
    ctx.write(repo / ".ufo/waves/round-46/claims/hold.md", "order broken at the freeze\n")
    _commit(ctx, repo, "claims written after the output")
    ctx.write(repo / "SCORECARD.md", "## round 46\n\ncalibration 7\n")
    _commit(ctx, repo, "scorecard row")
    return ["--lane", str(repo), "--claims", "plans/round-xx-claims.md",
            "--receipt", "corpus/evidence/round46/feal-linear-probe.txt"]


def build_underscore_name(ctx, d):
    """Underscore spelling, one commit carrying claims and receipt (the freeze-contains-receipt shape)."""
    repo = ctx.init(d / "onecommit")
    ctx.write(repo / "plans/round_44_claims.md", "# round 44 - frozen claims\n\nFrozen with the receipt.\n")
    ctx.write(repo / "corpus/evidence/round44/feal-linear-probe.txt", "cases=14 observed_pass=8 observed_fail=6\n")
    _commit(ctx, repo, "the claims file and its output in one commit")
    ctx.write(repo / "plans/registry.md", "| 44 | kengaku | calibration | plans/round_44_claims.md |\n")
    _commit(ctx, repo, "registry row")
    return ["--lane", str(repo), "--claims", "plans/round_44_claims.md",
            "--receipt", "corpus/evidence/round44/feal-linear-probe.txt"]


FIXTURES = [
    # U14c: a six-commit registry whose only defect is the claims name ending `.md.orig`.
    {"fid": "u14c_name_b-registry-suffix", "tool": "order", "expect": "error", "defects": [],
     "build": build_registry_suffix},
    # U14c: the same guard reached through a nested, capitalised path with its own four commits.
    {"fid": "u14c_name_b-nested-uppercase", "tool": "order", "expect": "error", "defects": [],
     "build": build_nested_uppercase},
    # U14c: no round digits at all, and a history whose receipt precedes the claims commit.
    {"fid": "u14c_name_b-round-xx-token", "tool": "order", "expect": "error", "defects": [],
     "build": build_round_xx_token},
    # U14c: underscore spelling with claims and receipt in one commit, so history order cannot answer it.
    {"fid": "u14c_name_b-underscore-name", "tool": "order", "expect": "error", "defects": [],
     "build": build_underscore_name},
]
