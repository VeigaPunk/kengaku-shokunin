"""battery40 — order gate (`plans/order_check.py`): the three frozen order mutants O04, O12, O14.

One fixture per advertised behaviour, each a two-commit claims-then-receipt repository built from
scratch (no clone of the lane: the gate only reads git history):

  o_gate-p10-ok-excuse   a claims blob shows `P10 ok receipt unreadable`; only a DEFECT line may
                         carry the executed-nothing excuse, so the reference reports
                         `hit:gate-p10` and exits 1 (O04: rc-silence).
  o_gate-claims-gitlink  a gitlink (mode 160000) entry sits under the round's claims/ directory;
                         the gate reads blobs, so a non-blob entry is skipped and the order holds
                         (O12: dropping that check makes `cat-file blob <gitlink>` fail, exit 2).
  o_gate-claims-bak-name a claims file named `round-42-claims.md.bak` is unparseable; the reference
                         exits 2 (setup error) and never decides (O14: an unanchored pattern
                         accepts the prefix and the gate returns a verdict).
"""

CLAIMS_BASE = "plans/round-42-claims.md"
CLAIMS_DIR = ".ufo/waves/round-42/claims"
RECEIPT = "corpus/evidence/round42/probe.txt"
# a commit id that is only ever named by the gitlink entry; it is not an object in the fixture repo
ABSENT_COMMIT = "3" * 40


def gate_repo(ctx, d, control_text, claims_name=CLAIMS_BASE, gitlink_ref=None):
    """Two commits: 1 freezes the claims file plus one file under claims/, 2 adds the receipt."""
    r = ctx.init(d / "repo")
    (r / "plans").mkdir()
    (r / claims_name).write_text("# round 42 frozen claims\n\nC1 and C2 frozen before any fixture exists.\n")
    (r / CLAIMS_DIR).mkdir(parents=True)
    (r / CLAIMS_DIR / "control-c1-nothing.txt").write_text(control_text)
    ctx.git(r, "add", "-A")
    if gitlink_ref:
        ctx.git(r, "update-index", "--add", "--cacheinfo",
                f"160000,{gitlink_ref},{CLAIMS_DIR}/vendored")
    ctx.git(r, "commit", "-q", "-m", "freeze")
    (r / "corpus/evidence/round42").mkdir(parents=True)
    (r / RECEIPT).write_text("probe receipt: 28 cases, 8 observed pass, 20 observed fail\n")
    ctx.git(r, "add", "-A")
    ctx.git(r, "commit", "-q", "-m", "receipt")
    return ["--lane", str(r), "--claims", claims_name, "--receipt", RECEIPT]


FIXTURES = [
    # O04: `P10 ok receipt unreadable` proves the probe ran behind an "ok" verdict — the reference
    # prints hit kind=gate-p10 and exits 1, while a mutant that honours the excuse for any verdict
    # stays silent and exits 0.
    {"fid": "o_gate-p10-ok-excuse", "tool": "order", "expect": "reject",
     "defects": ["hit:gate-p10"],
     "build": lambda ctx, d: gate_repo(ctx, d, "gate: P10 ok receipt unreadable\n")},
    # O12: a gitlink under claims/ is a tree entry, not a blob; the reference skips it and passes,
    # while a mutant that only checks the field count feeds the gitlink commit id to cat-file
    # (no such object) and exits 2.
    {"fid": "o_gate-claims-gitlink", "tool": "order", "expect": "accept",
     "defects": [],
     "build": lambda ctx, d: gate_repo(ctx, d, "P10 DEFECT receipt unreadable\n", gitlink_ref=ABSENT_COMMIT)},
    # O14: `round-42-claims.md.bak` is not a round-NN-claims.md name; the reference exits 2 without
    # deciding, while an unanchored pattern accepts the prefix and prints an order verdict.
    {"fid": "o_gate-claims-bak-name", "tool": "order", "expect": "error",
     "defects": [],
     "build": lambda ctx, d: gate_repo(ctx, d, "P10 DEFECT receipt unreadable\n",
                                      claims_name="plans/round-42-claims.md.bak")},
]
