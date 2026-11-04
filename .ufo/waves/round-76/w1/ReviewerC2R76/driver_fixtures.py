#!/usr/bin/env python3
"""ReviewerC2R76 fixture experiments against a verbatim scratch copy of the C2 gate.

gate_fixture.py  = gate_orig.py + emit work-dir default redirected to this seat's scratch (1 line).
gate_visible.py  = gate_fixture.py + visible() applied to the six leg inputs (Q2 repair candidate).
All production files are read-only; every fixture lives under this seat's scratch tree.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r76/ReviewerC2R76")
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
BASE_SHA = "fda63968f29f8f58dc2b28831acac879405b8326"  # verified ancestor of lane master


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, S / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gf = load("gate_fixture")
gv = load("gate_visible")


def run(gate: str, lane: Path, probe: Path, receipt: Path, rev: str = "worktree"):
    cmd = [sys.executable, str(S / f"{gate}.py"), "--lane", str(lane),
           "--probe", str(probe), "--receipt", str(receipt)]
    if rev != "worktree":
        cmd += ["--rev", rev]
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(f"=== {gate} lane={lane} rev={rev} rc={p.returncode}")
    print(p.stdout, end="")
    if p.stderr.strip():
        print("STDERR:", p.stderr.strip())
    print(f"--- rc={p.returncode}")
    return p.returncode, p.stdout


def rewrite_row(root: Path, ident: str, **kw) -> None:
    led = root / "corpus/routed-findings.jsonl"
    rows = [json.loads(l) for l in led.read_text().splitlines() if l.strip()]
    for r in rows:
        if r["id"] == ident:
            r.update(kw)
    led.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


# E1 — Q1: vacuous-but-well-shaped check on an otherwise clean fixture
e1 = S / "fix/e1"
gf.build_fixture(e1, BASE_SHA)
rewrite_row(e1, "R75-D1", check="grep -q 'the' SCORECARD.md")
run("gate_fixture", e1, LANE, S / "work/e1-receipt.txt")

# E2 — Q2: every value-bearing leg satisfied from comments/fences only
e2 = S / "fix/e2"
gf.build_fixture(e2, BASE_SHA)
(e2 / "SCORECARD.md").write_text(
    "<!-- - R75-D2 correction: stamp fda63968f29f8f58dc2b28831acac879405b8326 and report tip 5d9a0ccc. -->\n"
    "<!-- - R75-D3 correction: the final-rule before is 60 (4/36/20). -->\n"
)
(e2 / "corpus/QUALITY.md").write_text(
    "<!-- | Q98 | fixture criterion | R75-D1 grounded in corpus/lessons/round-75-verifier-spotcheck.md | -->\n"
)
(e2 / "LOG.md").write_text(
    "## Round 76\n\n<!-- - **R75-D5** correction: the C1 selftest prints cases=8 red=7 and the stamp is "
    "fda63968f29f8f58dc2b28831acac879405b8326; the earlier line said cases=7 red=6. -->\n"
)
(e2 / "SKILL.md").write_text(
    "```\n| `round75-c1-index-parity` | gate | `--selftest` (cases=8 red=7) |\n"
    "| `round75-c2-registry-audit` | gate | `--selftest` (arms=5) |\n```\n"
)
(e2 / "corpus/lessons/round-74.md").write_text(
    "# Round 74\n\nbody\n\n```\n## Correction (round 76)\n\nR75-D7: appended, not reflowed.\n```\n"
)
run("gate_fixture", e2, LANE, S / "work/e2-receipt.txt")    # raw-byte legs: expect pass
run("gate_visible", e2, LANE, S / "work/e2b-receipt.txt")   # visible() legs: expect fail

# E2c — repair safety: visible() copy must keep the real lane green
run("gate_visible", LANE, LANE, S / "work/e2c-receipt.txt")

# E4 — Q4: a *newer* spotcheck that names no ids
e4 = S / "fix/e4"
gf.build_fixture(e4, BASE_SHA)
(e4 / "corpus/lessons/round-77-verifier-spotcheck.md").write_text(
    "# Round 77 — draft\n\nNo routed defects named yet.\n"
)
run("gate_fixture", e4, LANE, S / "work/e4-receipt.txt")

# E5 — Q5: closure lesson deleted entirely (no spotcheck at all)
e5 = S / "fix/e5"
gf.build_fixture(e5, BASE_SHA)
(e5 / "corpus/lessons/round-75-verifier-spotcheck.md").unlink()
run("gate_fixture", e5, LANE, S / "work/e5-receipt.txt")

# E6 — pass with pending legs: declared bytes at the row-commit revision on the real lane
run("gate_fixture", LANE, LANE, S / "work/e6-receipt.txt",
    rev="6977019bdf56a88921e14f728167da8f5726c1fc")
