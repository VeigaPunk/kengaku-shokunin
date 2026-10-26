"""Battery38 module p10b: the P10 pass side — frozen mutant N15 (clause P10, direction mirror).

N15 replaces the frozen gate's successful `c_rerun` return with
`return False, f"probe_rerun=byte-equal ..."`, i.e. a gate that prints `P10 DEFECT` even when a fresh
probe run reproduces the receipt byte for byte. No round-36/37 fixture ever reaches that line (every
`--rerun` fixture there is a reject, R37PlanNext §3.2 shape B5), so a mirror fixture is needed: an
ACCEPT package whose `--rerun` probe output is byte-equal to its receipt. On that fixture the
reference gate prints `P10 ok probe_rerun=byte-equal` and N15 prints `P10 DEFECT`, which is the
attributed mirror kill (the fixture declares no DEFECT clauses, so its declared set `[]` is also the
exact reference set).

The fixture is the genuine round-35 package bytes (`ctx.genuine_package`: git-init, all pinned
instruments copied, index untouched) plus two owned inputs:

  * the receipt bytes are replaced by the fixture probe's known output (same relative path as the
    genuine receipt, so the README's coverage bullet and every spec pin stay coherent);
  * a spec derived from `dict(ctx.spec)` pins that receipt digest and points `probe_cmd` at a
    deterministic one-expression program (`["-c", ...]`), which the gate runs as
    `[sys.executable] + probe_cmd` when `import Bio` works and otherwise under
    `uv run --no-project --with biopython==1.85 python3 -c ...`, cwd = root. `-c` writes no
    `__pycache__`, so P9 stays clean without an ignore rule.

Every other clause (P1 pins, P3-P8 shape) is exercised on the unmodified genuine package bytes, and
the fixture expects the reference gate to accept with no DEFECT clause printed.

stdlib only; no import-time side effects.
"""
import copy
import hashlib
import json

PROBE_OUTPUT = "p10b probe: byte-equal under --rerun\n"
PROBE_PROGRAM = "import sys; sys.stdout.write(" + repr(PROBE_OUTPUT) + ")"


def _accept_with_byte_equal_rerun(ctx, d):
    """N15 mirror: an ACCEPT package whose fresh probe output equals its receipt byte for byte."""
    ctx.genuine_package(d)
    spec = copy.deepcopy(ctx.spec)
    spec["probe_cmd"] = ["-c", PROBE_PROGRAM]
    receipt = d / spec["receipt"]
    receipt.write_text(PROBE_OUTPUT)
    spec["receipt_sha256"] = hashlib.sha256(receipt.read_bytes()).hexdigest()
    spec_path = d / "p10b-spec.json"
    spec_path.write_text(json.dumps(spec, indent=1, sort_keys=True) + "\n")
    ctx.git_add(d)
    return ["package", "--root", str(d), "--require-clean-tree", "--rerun",
            "--spec", str(spec_path)]


FIXTURES = [
    {"fid": "p10b-rerun-byte-equal-accept", "expect": "accept", "defects": [],
     "build": _accept_with_byte_equal_rerun},
]
