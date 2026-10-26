"""C1 battery41: `plans/tip_receipts.py` control availability and dependency skip (round 41, seat R41BatRcvCtl).

Each fixture builds a small committed lane from nothing and returns the tool argv tail. Four fixtures, one
behaviour each, and every branch has a second trigger:

  r_ctl-t06-empty-equal-receipt  an empty committed receipt that its probe reproduces byte for byte is
                                 `equal`, but the automatic byte-flip control has no bytes to flip, so it
                                 reports `control:unavailable`; a failed control exits 1 (T06).
  r_ctl-t06-tamper-on-skipped    the same failed-control branch through `--tamper`: a mapped receipt that
                                 was skipped has no fresh output to compare, so its control is unavailable
                                 and the run exits 1 (second trigger of the T06 branch).
  r_ctl-t08-derived-uv-absent    a derived receipt whose `Run as:` line starts `uv run` while `uv` is
                                 not on the fixed PATH prints `skip:<rel>:dependency-missing`; the other
                                 receipt is equal and its control answers differ, so the run exits 0 (T08).
  r_ctl-t08-table-uv-absent      the same dependency branch in the table registry layout: two table-mapped
                                 receipts, one needing `uv`, exit 0 (second trigger of the T08 branch).

No witness module is read, copied or imported.
"""

EV_R41 = "corpus/evidence/round41/r-ctl-probe.txt"
EV_TB2 = "corpus/evidence/round35/tb2-grader-probe.txt"
EV_PMARS = "corpus/evidence/round38/build-pmars-probe.txt"
EV_REGEX = "corpus/evidence/round36/regex-log-probe.txt"

STUB = '''"""Stub probe used by one r_ctl fixture.

  {run} --lane .
"""
import sys

sys.stdout.write({out!r})
sys.exit({rc})
'''


def _tree(ctx, d, files, name):
    """A committed lane: git init in d/<name>, write every rel file, one commit by `fixture`."""
    root = ctx.init(d / name)
    for rel, text in files.items():
        ctx.write(root / rel, text)
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture")
    return root


def b_t06_empty(ctx, d):
    root = _tree(ctx, d, {
        "README.md": "# r_ctl lane\n",
        "SKILL.md": "registry row: plans/r_ctl_probe.py\n",
        EV_R41: "",
        "plans/r_ctl_probe.py": STUB.format(run="python3 plans/r_ctl_probe.py", out="", rc=0),
    }, "lane-empty")
    return ["--lane", str(root), "--work", "{WORK}"]


def b_t06_tamper_skipped(ctx, d):
    root = _tree(ctx, d, {
        "README.md": "# r_ctl lane\n",
        EV_R41: "a receipt whose probe needs uv\n",
        "plans/r_ctl_probe.py": STUB.format(
            run="uv run --no-project python3 plans/r_ctl_probe.py",
            out="a receipt whose probe needs uv\n", rc=0),
    }, "lane-tamper")
    return ["--lane", str(root), "--work", "{WORK}", "--tamper", EV_R41]


def b_t08_derived_uv(ctx, d):
    root = _tree(ctx, d, {
        "README.md": "# r_ctl lane\n",
        "SKILL.md": "registry rows: plans/r_ctl_probe.py, plans/tb2_grader_probe.py\n",
        EV_R41: "needs uv\n",
        "plans/r_ctl_probe.py": STUB.format(
            run="uv run --no-project python3 plans/r_ctl_probe.py", out="needs uv\n", rc=0),
        EV_TB2: "tb2 probe ok\n",
        "plans/tb2_grader_probe.py": STUB.format(
            run="python3 plans/tb2_grader_probe.py", out="tb2 probe ok\n", rc=0),
    }, "lane-derived")
    return ["--lane", str(root), "--work", "{WORK}"]


def b_t08_table_uv(ctx, d):
    root = _tree(ctx, d, {
        "README.md": "# r_ctl lane\n",
        EV_PMARS: "pmars probe output\n",
        "plans/build_pmars_probe.py": STUB.format(
            run="uv run --no-project python3 plans/build_pmars_probe.py",
            out="pmars probe output\n", rc=0),
        EV_REGEX: "regex probe ok\n",
        "plans/regex_log_probe.py": STUB.format(
            run="python3 plans/regex_log_probe.py", out="regex probe ok\n", rc=0),
    }, "lane-table")
    return ["--lane", str(root), "--work", "{WORK}"]


FIXTURES = [
    {"fid": "r_ctl-t06-empty-equal-receipt", "tool": "receipts", "expect": "reject",
     "defects": [f"equal:{EV_R41}", "control:unavailable"], "build": b_t06_empty},
    {"fid": "r_ctl-t06-tamper-on-skipped", "tool": "receipts", "expect": "reject",
     "defects": [f"skip:{EV_R41}:dependency-missing", "control:unavailable"],
     "build": b_t06_tamper_skipped},
    {"fid": "r_ctl-t08-derived-uv-absent", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_R41}:dependency-missing", f"equal:{EV_TB2}", "control:differ"],
     "build": b_t08_derived_uv},
    {"fid": "r_ctl-t08-table-uv-absent", "tool": "receipts", "expect": "accept",
     "defects": [f"skip:{EV_PMARS}:dependency-missing", f"equal:{EV_REGEX}", "control:differ"],
     "build": b_t08_table_uv},
]
