"""Specificity control for battery44 module `u14c_name_b` (seat R44BatU14b) -- NOT part of the battery.

The four `error` fixtures of `battery/u14c_name_b.py` reach `plans/order_check.py:161-162` only
because their claims file name is unparseable. These four twins carry the SAME histories with a
parseable claims name, so the gate runs past the guard and answers the question instead: two
accepts (a clean registry, a nested claims file) and two rejects (receipt committed before the
claims file; claims and receipt in one commit). If those four exit codes hold, the histories are
answerable on their own and the name is the only thing the delivered fixtures move.

Run: `python3 plans/round44_c1_verify.py --lane <clone> --battery-dir <this dir> --only U14c --work <scratch>`
Expected: every FIXTURE line `ok`, and `U14c ... SURVIVED exhibits=none` (the guard is not touched).
"""


def _commit(ctx, repo, message):
    ctx.git(repo, "add", "-A")
    ctx.git(repo, "commit", "-q", "-m", message)


def build_registry_parseable(ctx, d):
    """The six-commit registry with the claims name spelled `round-51-claims.md`: order holds."""
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
    ctx.write(repo / "plans/round-51-claims.md",
              "# round 51 - frozen claims\n\n"
              "Written and frozen before any plans/battery44 fixture exists.\n")
    ctx.write(repo / ".ufo/waves/round-51/claims/freeze-note.md", "frozen 09:12; nothing executed yet\n")
    _commit(ctx, repo, "round 51: the claims file")
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
              "| 51 | kengaku | operability | plans/round-51-claims.md |\n")
    _commit(ctx, repo, "registry: the round-51 row")
    return ["--lane", str(repo), "--claims", "plans/round-51-claims.md",
            "--receipt", "corpus/evidence/round51/receipts/feal-linear-probe.txt"]


def build_nested_parseable(ctx, d):
    """The nested four-commit history with a lowercase name: order holds."""
    repo = ctx.init(d / "history")
    ctx.write(repo / "notes/history/README.md", "kept for the rounds before the claims pattern existed\n")
    ctx.write(repo / "notes/history/round-7-claims.md", "# round 7 - frozen claims\n\nFrozen before the run.\n")
    _commit(ctx, repo, "history: the round-7 claims")
    ctx.write(repo / ".ufo/waves/round-7/claims/order.md", "P7 ok pins\nP8 ok digests match\n")
    _commit(ctx, repo, "round 7 checks")
    ctx.write(repo / "corpus/evidence/round7/feal-linear-probe.txt", "cases=9 observed_pass=6 observed_fail=3\n")
    _commit(ctx, repo, "round 7: first recorded output")
    ctx.write(repo / "notes/history/README.md",
              "kept for the rounds before the claims pattern existed\n\nround 7 added\n")
    _commit(ctx, repo, "history: README note")
    return ["--lane", str(repo), "--claims", "notes/history/round-7-claims.md",
            "--receipt", "corpus/evidence/round7/feal-linear-probe.txt"]


def build_inverted_parseable(ctx, d):
    """The receipt-before-claims history with `round-46-claims.md`: the gate rejects, exit 1."""
    repo = ctx.init(d / "inverted")
    ctx.write(repo / "corpus/evidence/round46/feal-linear-probe.txt", "cases=11 observed_pass=7 observed_fail=4\n")
    _commit(ctx, repo, "round 46: recorded output landed first")
    ctx.write(repo / "plans/round-46-claims.md", "# round 46 - frozen claims\n\nFrozen after the output.\n")
    ctx.write(repo / ".ufo/waves/round-46/claims/hold.md", "order broken at the freeze\n")
    _commit(ctx, repo, "claims written after the output")
    ctx.write(repo / "SCORECARD.md", "## round 46\n\ncalibration 7\n")
    _commit(ctx, repo, "scorecard row")
    return ["--lane", str(repo), "--claims", "plans/round-46-claims.md",
            "--receipt", "corpus/evidence/round46/feal-linear-probe.txt"]


def build_onecommit_parseable(ctx, d):
    """The one-commit history with `round-44-claims.md`: the gate rejects, exit 1."""
    repo = ctx.init(d / "onecommit")
    ctx.write(repo / "plans/round-44-claims.md", "# round 44 - frozen claims\n\nFrozen with the receipt.\n")
    ctx.write(repo / "corpus/evidence/round44/feal-linear-probe.txt", "cases=14 observed_pass=8 observed_fail=6\n")
    _commit(ctx, repo, "the claims file and its output in one commit")
    ctx.write(repo / "plans/registry.md", "| 44 | kengaku | calibration | plans/round-44-claims.md |\n")
    _commit(ctx, repo, "registry row")
    return ["--lane", str(repo), "--claims", "plans/round-44-claims.md",
            "--receipt", "corpus/evidence/round44/feal-linear-probe.txt"]


FIXTURES = [
    {"fid": "u14c_name_b-ctl-registry-parseable", "tool": "order", "expect": "accept", "defects": [],
     "build": build_registry_parseable},
    {"fid": "u14c_name_b-ctl-nested-parseable", "tool": "order", "expect": "accept", "defects": [],
     "build": build_nested_parseable},
    {"fid": "u14c_name_b-ctl-inverted-parseable", "tool": "order", "expect": "reject", "defects": [],
     "build": build_inverted_parseable},
    {"fid": "u14c_name_b-ctl-onecommit-parseable", "tool": "order", "expect": "reject", "defects": [],
     "build": build_onecommit_parseable},
]
