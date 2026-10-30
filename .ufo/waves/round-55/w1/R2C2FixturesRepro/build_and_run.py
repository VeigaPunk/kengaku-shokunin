#!/usr/bin/env python3
"""Seat R2C2FixturesRepro — independent rebuild of the two frozen R55-C2 laundering
fixtures and re-demonstration of the red-before state.

This is MY OWN minimal fixture builder. It does NOT import, exec, or read
plans/round55_c2_controls.py. The fixture *content* (registry row, ledger row,
gate behaviour, laundered argv) is fixed by the frozen cases in
plans/round-55-claims.md (R55-C2, "Before (red, frozen, base)") and must match
what any correct builder produces; the code below is written from that spec.

Frozen cases:
  abbreviated-selftest  ledger entry_argv ["python3", "plans/fixture_gate.py", "--selft"]
                        (argparse prefix abbreviation of --selftest) declared green;
                        registry-declared entry ["python3", "plans/fixture_gate.py"] exits 1.
  uv-decoy-script       ledger entry_argv ["uv", "run", "--no-project", "--offline",
                        "python3", "-cprint('wrapper green')", "python3",
                        "plans/fixture_gate.py"] declared green; the wrapper's inline
                        -c program exits 0 and the true entry is never executed.

Runs the UNCHANGED r54 counter (plans/round54_c2_entrytruth.py, imported by path)
over each fixture, then runs the registry-declared entry directly for ground truth.

Usage: python3 build_and_run.py [--work DIR]
Exit 0 both fixtures reproduce the committed before-state, 1 otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
R54_COUNTER = LANE / "plans" / "round54_c2_entrytruth.py"

REGISTRY_HEADING_LINES = [
    "## Gate/probe registry",
    "",
    "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
    "|---|---|---|---|---|---|---|---|",
]
REGISTRY_ROW = ("| `fixture-gate` | gate | `python3 plans/fixture_gate.py` "
                "| `0` ok · `1` bad | none | none | none | kengaku |")
REGISTRY_ENTRY = ["python3", "plans/fixture_gate.py"]

# The gate: argparse with a --selftest flag. Abbreviation `--selft` is accepted by
# argparse's default allow_abbrev=True, so the laundered argv exits 0. The bare
# entry (no flag) prints the frozen failure line and exits 1.
GATE_SRC = '''#!/usr/bin/env python3
import argparse
import sys

p = argparse.ArgumentParser()
p.add_argument("--selftest", action="store_true")
a = p.parse_args()
if a.selftest:
    print("selftest ok")
    sys.exit(0)
print("entry failed: fixture gate is broken on purpose")
sys.exit(1)
'''

CASES = {
    "abbreviated-selftest": ["python3", "plans/fixture_gate.py", "--selft"],
    "uv-decoy-script": ["uv", "run", "--no-project", "--offline", "python3",
                        "-cprint('wrapper green')", "python3", "plans/fixture_gate.py"],
}

COMMITTED_RECEIPTS = {
    "abbreviated-selftest": LANE / ".ufo/waves/round-55/claims/c2-before-abbreviated-selftest.txt",
    "uv-decoy-script": LANE / ".ufo/waves/round-55/claims/c2-before-uv-decoy-script.txt",
}


def _load(name: str, path: Path):
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_fixture(root: Path, ledger_entry_argv: list[str]) -> Path:
    """Build ONE one-row scratch git fixture with the given laundered ledger argv."""
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "SKILL.md").write_text("\n".join(REGISTRY_HEADING_LINES + [REGISTRY_ROW]) + "\n")
    (root / "plans" / "fixture_gate.py").write_text(GATE_SRC)
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps({
        "schema": "r54-entrytruth-v1",
        "rows": {"fixture-gate": {
            "entry_argv": list(ledger_entry_argv),
            "entry_exit": 0,
            "entry_state": "green",
            "timeout_s": 60,
        }},
    }, indent=1) + "\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=fixture",
                    "-c", "user.email=fixture@fixture", "commit", "-qm", "fixture"], check=True)
    # host-guard style assertion: the fixture toplevel must be exactly root
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if Path(top).resolve() != root.resolve():
        raise RuntimeError(f"fixture root guard: toplevel {top!r} != {str(root)!r}")
    return root


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reproduce_case(case: str, r54, work: Path) -> tuple[int, str]:
    argv = CASES[case]
    root = build_fixture(work / f"fx-{case}", list(argv))
    rc, lines = r54.evaluate(root, root, work / f"run-{case}", 1, 60, False)
    # ground truth: the registry-declared entry, run directly under a hermetic env
    truth_env = r54.hermetic_env(work / f"truth-{case}")
    p = subprocess.run(REGISTRY_ENTRY, cwd=root, capture_output=True, text=True, env=truth_env)
    first = (p.stdout or p.stderr).strip().splitlines()
    out = []
    out.append(f"CASE {case}")
    out.append("ARGV " + json.dumps(argv))
    out.append("== r54 counter over the laundering fixture (unchanged module) ==")
    out.extend(lines)
    out.append(f"COUNTER EXIT {rc}")
    out.append(f"TRUE REGISTRY ENTRY {json.dumps(REGISTRY_ENTRY)} exit={p.returncode} "
               + ("out=" + first[0] if first else ""))
    laundered = rc == 0 and p.returncode != 0
    out.append(f"ROUTE laundering {'demonstrated' if laundered else 'NOT demonstrated'} "
               f"(r54 rc={rc}, true entry exit={p.returncode})")
    text = "\n".join(out) + "\n"
    (work / f"repro-{case}.txt").write_text(text)
    # structural record of the fixture bytes I produced (independent of controls code)
    (work / f"fx-{case}.files.txt").write_text("\n".join(
        f"{sha256(f)}  {f.relative_to(root)}" for f in sorted(root.rglob("*")) if f.is_file()) + "\n")
    return (0 if laundered else 1), text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", type=Path, default=Path(__file__).resolve().parent / "out")
    a = ap.parse_args()
    work = a.work.resolve()
    work.mkdir(parents=True, exist_ok=True)

    r54 = _load("r54entry_repro", R54_COUNTER)
    if r54 is None:
        print("SETUP r54 counter absent")
        return 2

    fails = 0
    for case in CASES:
        rc, text = reproduce_case(case, r54, work)
        print(text, end="")
        fails += rc
        committed = COMMITTED_RECEIPTS[case].read_text()
        # Compare everything except the per-fixture SOURCE rev line (each scratch
        # fixture is its own git repo, so its commit hash legitimately differs).
        def norm(t: str) -> list[str]:
            return [ln for ln in t.splitlines() if not ln.startswith("SOURCE rev=")]
        if norm(text) == norm(committed):
            print(f"COMPARE {case}: MATCH committed receipt modulo SOURCE rev line")
        else:
            print(f"COMPARE {case}: DIVERGENCE from committed receipt (modulo SOURCE rev):")
            import difflib
            for ln in difflib.unified_diff(norm(committed), norm(text),
                                           "committed", "repro", lineterm=""):
                print("  " + ln)
            fails += 1
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
