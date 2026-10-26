"""Round-41 battery module (seat R41BatRcvRun): receipt re-run verdicts.

Frozen mutants T03, T04 and T13 of `plans/round41_c1_verify.py` sit on the tip-receipts re-run verdict
path: a probe's non-zero exit, the declared-bounded `temp-paths` comparison, and the tamper control.
Every fixture builds a committed lane-shaped work tree in the empty fixture directory — the docs the
tool reads for provenance, `plans/` probes whose docstring carries the `Run as:` line, and receipts
under `corpus/evidence/` — and declares the exact class set the unmodified tool prints on it.
"""
from __future__ import annotations

RECEIPTS_DOC = "# fixture lane receipts\n"


def probe(name: str, out: str, rc: int = 0, body: str = "") -> str:
    """A committed stub probe: `Run as:` docstring, then `body` or a fixed stdout, then an exit code."""
    write = body or f"sys.stdout.write({out!r})\n"
    return (
        '"""Fixture probe.\n\n'
        f'  python3 plans/{name}.py --lane .\n'
        '"""\n'
        "import sys\n"
        + write
        + f"sys.exit({rc})\n"
    )


def lane(ctx, d, files, sub="lane"):
    """Commit a lane-shaped work tree: docs, plans/ probes and receipts, one `fixture lane` commit."""
    root = ctx.init(d / sub)
    base = {
        "README.md": "# fixture lane\n",
        "SKILL.md": "# fixture skill\n",
        "corpus/README.md": RECEIPTS_DOC,
        "corpus/knowledge/fixture.md": "# fixture knowledge note\n",
    }
    base.update(files)
    for rel in sorted(base):
        ctx.write(root / rel, base[rel])
    ctx.git(root, "add", "-A")
    ctx.git(root, "commit", "-q", "-m", "fixture lane")
    return root


def argv(root):
    return ["--lane", str(root), "--work", "{WORK}"]


def b_rc_nonzero_mixed(ctx, d):
    # T03: a mapped probe that prints its receipt bytes and exits non-zero is a `differ` (exit 1) even
    # though a second, clean receipt still supplies the automatic tamper control.
    good = "census probe\nrows=12\n"
    bad = "rc-ledger probe\nchecks=4\nresult=stable\n"
    root = lane(ctx, d, {
        "corpus/evidence/round42/census-probe.txt": good,
        "corpus/evidence/round42/rc-ledger-probe.txt": bad,
        "plans/census_probe.py": probe("census_probe", good),
        "plans/rc_ledger_probe.py": probe("rc_ledger_probe", bad, rc=7),
    })
    return argv(root)


def b_rc_nonzero_single(ctx, d):
    # T03, second trigger: the only mapped receipt is the one whose probe exits 1 after printing it, so a
    # verdict of `equal` would leave the run with no control at all.
    out = "audit probe\nrows=1\n"
    root = lane(ctx, d, {
        "corpus/evidence/round43/audit-probe.txt": out,
        "plans/audit_probe.py": probe("audit_probe", out, rc=1),
    })
    return argv(root)


def b_temp_paths(ctx, d):
    # T04: the table-mapped `temp-paths` receipt stays a declared-bounded skip (accept, exit 0) when the
    # fresh output differs only in the mkdtemp path the probe actually records.
    rel = "corpus/evidence/round36/regex-log-probe-first-run.txt"
    blob = "regex-log probe, first run\nscratch=/tmp/tmp8kq2zr41\nrows=3\n"
    body = (
        "import tempfile\n"
        'print("regex-log probe, first run")\n'
        'print("scratch=" + tempfile.mkdtemp())\n'
        'print("rows=3")\n'
    )
    root = lane(ctx, d, {
        rel: blob,
        "plans/regex_log_probe.py": probe("regex_log_probe", "", body=body),
    })
    return argv(root)


def b_control_differ(ctx, d):
    # T13: two byte-equal receipts; the automatic control on the cheapest one must answer `differ`, so a
    # green run exits 0 with that control line printed.
    a = "stable census probe\nrows=12\n"
    b = "slot audit probe\nslots=5\nwindows=2\n"
    root = lane(ctx, d, {
        "corpus/evidence/round42/stable-census-probe.txt": a,
        "corpus/evidence/round43/slot-audit-probe.txt": b,
        "plans/stable_census_probe.py": probe("stable_census_probe", a),
        "plans/slot_audit_probe.py": probe("slot_audit_probe", b),
    })
    return argv(root)


FIXTURES = [
    {"fid": "r_run-t03-rc-nonzero-mixed", "tool": "receipts", "expect": "reject",
     "defects": ["control:differ",
                 "differ:corpus/evidence/round42/rc-ledger-probe.txt",
                 "equal:corpus/evidence/round42/census-probe.txt"],
     "build": b_rc_nonzero_mixed},
    {"fid": "r_run-t03-rc-nonzero-single", "tool": "receipts", "expect": "reject",
     "defects": ["differ:corpus/evidence/round43/audit-probe.txt"],
     "build": b_rc_nonzero_single},
    {"fid": "r_run-t04-temp-paths-masked", "tool": "receipts", "expect": "accept",
     "defects": ["skip:corpus/evidence/round36/regex-log-probe-first-run.txt:"
                 "declared-nonreproducible-absolute-scratch-paths"],
     "build": b_temp_paths},
    {"fid": "r_run-t13-auto-control-differ", "tool": "receipts", "expect": "accept",
     "defects": ["control:differ",
                 "equal:corpus/evidence/round42/stable-census-probe.txt",
                 "equal:corpus/evidence/round43/slot-audit-probe.txt"],
     "build": b_control_differ},
]
