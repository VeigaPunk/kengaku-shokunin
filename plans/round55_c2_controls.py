#!/usr/bin/env python3
"""Round 55, claim C2 controls: the two frozen laundering fixtures, before and after.

Frozen 2026-10-30 before any after-run data (plans/round-55-claims.md, R55-C2). The two
cases reproduce the round-54 attack routes (`.ufo/waves/round-54/w1/R2C2Counter/
laundering-probes.txt`) against one-row scratch git fixtures:

  abbreviated-selftest  ledger entry argv `python3 plans/fixture_gate.py --selft`
                        (argparse prefix abbreviation of --selftest) declared green;
                        the registry-declared entry `python3 plans/fixture_gate.py` exits 1.
  uv-decoy-script       ledger entry argv
                        `uv run --no-project --offline python3 -cprint('wrapper green')
                         python3 plans/fixture_gate.py` declared green; the wrapper's
                        inline program exits 0 and the true entry is never executed.

    python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r54
    python3 plans/round55_c2_controls.py --case uv-decoy-script     --against r55
    python3 plans/round55_c2_controls.py --selftest

`--against r54` expects the laundering route to PASS the r54 counter (PREDICATE R54-C2
pass, exit 0) while the registry-declared entry exits 1 — the red-before state.
`--against r55` expects the round-55 binding counter to FAIL the fixture with an
attributed ARGV-DEFECT/WRAPPER-DEFECT line naming the case (exit 1).
Exit 0 the demonstrated state holds, 1 it does not, 2 setup (e.g. r55 counter absent).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
HEAD_ROW = ["## Gate/probe registry", "",
            "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]
REGISTRY_ENTRY = ["python3", "plans/fixture_gate.py"]

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


def _load(name: str, path: Path):
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fixture(root: Path, ledger_entry_argv: list[str]) -> Path:
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [
        "| `fixture-gate` | gate | `python3 plans/fixture_gate.py` | `0` ok · `1` bad | none | none | none | kengaku |",
    ]) + "\n")
    (root / "plans" / "fixture_gate.py").write_text(GATE_SRC)
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps({
        "schema": "r54-entrytruth-v1",
        "rows": {"fixture-gate": {
            "entry_argv": ledger_entry_argv,
            "entry_exit": 0,
            "entry_state": "green",
            "timeout_s": 60,
        }},
    }, indent=1) + "\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                    "commit", "-qm", "fixture"], check=True)
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if Path(top).resolve() != root.resolve():
        raise RuntimeError(f"fixture root guard: toplevel {top} != {root}")
    return root


def run_case(case: str, against: str, work: Path) -> int:
    argv = CASES[case]
    root = _fixture(work / f"fixture-{against}-{case}", list(argv))
    if against == "r54":
        mod = _load("r54entry", LANE / "plans" / "round54_c2_entrytruth.py")
        if mod is None:
            print("SETUP r54 counter absent")
            return 2
        rc, lines = mod.evaluate(root, root, work / f"run-{case}", 1, 60, False)
        print(f"CASE {case}")
        print("ARGV", json.dumps(argv))
        print("== r54 counter over the laundering fixture (unchanged module) ==")
        print("\n".join(lines))
        print(f"COUNTER EXIT {rc}")
        # ground truth: the registry-declared entry, run directly
        true_env = mod.hermetic_env(work / f"truth-{case}")
        p = subprocess.run(REGISTRY_ENTRY, cwd=root, capture_output=True, text=True, env=true_env)
        print("TRUE REGISTRY ENTRY", json.dumps(REGISTRY_ENTRY), f"exit={p.returncode}",
              "out=" + (p.stdout or p.stderr).strip().splitlines()[0] if (p.stdout or p.stderr) else "")
        laundered = rc == 0 and p.returncode != 0
        print(f"ROUTE laundering {'demonstrated' if laundered else 'NOT demonstrated'} "
              f"(r54 rc={rc}, true entry exit={p.returncode})")
        return 0 if laundered else 1
    if against == "r55":
        mod = _load("r55entry", LANE / "plans" / "round55_c2_entryargv.py")
        if mod is None:
            print("SETUP plans/round55_c2_entryargv.py absent (built by the round-55 wave)")
            return 2
        rc, lines = mod.evaluate(root, root, work / f"run55-{case}", 1, 60, False)
        print(f"CASE {case}")
        print("ARGV", json.dumps(argv))
        print("== r55 binding counter over the laundering fixture ==")
        print("\n".join(lines))
        print(f"COUNTER EXIT {rc}")
        killed = rc == 1 and any(
            tag in "\n".join(lines)
            for tag in ("ARGV-DEFECT", "WRAPPER-DEFECT", "ABBREV-DEFECT", "PREDICATE R55-C2 fail"))
        print(f"ROUTE kill {'demonstrated' if killed else 'NOT demonstrated'} (r55 rc={rc})")
        return 0 if killed else 1
    print("SETUP --against must be r54 or r55")
    return 2


def _selftest() -> int:
    fails = 0
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        r54 = _load("r54entry", LANE / "plans" / "round54_c2_entrytruth.py")
        if r54 is None:
            print("SELFTEST FAIL r54 counter absent")
            return 1
        for case, argv in CASES.items():
            root = _fixture(work / f"st-{case}", list(argv))
            rc, lines = r54.evaluate(root, root, work / f"st-run-{case}", 1, 60, False)
            ok = rc == 0 and any("PREDICATE R54-C2 pass" in ln for ln in lines)
            print(f"SELFTEST {'ok' if ok else 'FAIL'} r54-passes-{case}")
            fails += 0 if ok else 1
        # truthful fixture (ledger argv == registry entry, declared red with evidence)
        root = _fixture(work / "st-truthful", list(REGISTRY_ENTRY))
        ledger = json.loads((root / "plans" / "round54-entrytruth.json").read_text())
        ledger["rows"]["fixture-gate"] = {
            "entry_argv": list(REGISTRY_ENTRY), "entry_exit": 1, "entry_state": "red",
            "reason": "the fixture gate's entry mode is broken on purpose for this control fixture",
            "evidence": "entry failed: fixture gate is broken on purpose", "timeout_s": 60,
        }
        (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(ledger, indent=1) + "\n")
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                        "commit", "-qm", "truthful"], check=True)
        rc, lines = r54.evaluate(root, root, work / "st-run-truthful", 1, 60, False)
        ok = rc == 0 and any("PREDICATE R54-C2 pass" in ln for ln in lines)
        print(f"SELFTEST {'ok' if ok else 'FAIL'} truthful-fixture-passes-r54")
        fails += 0 if ok else 1
        # the gate's argparse really accepts the abbreviation (the route is live)
        p = subprocess.run(["python3", "plans/fixture_gate.py", "--selft"], cwd=work / "st-abbreviated-selftest",
                           capture_output=True, text=True)
        ok = p.returncode == 0 and "selftest ok" in (p.stdout or "")
        print(f"SELFTEST {'ok' if ok else 'FAIL'} abbreviation-live (--selft exits 0)")
        fails += 0 if ok else 1
    print(f"SELFTEST cases=4 failures={fails}")
    return 0 if fails == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--case", choices=sorted(CASES))
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--against", choices=("r54", "r55"), default="r54")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    work = Path(tempfile.mkdtemp(prefix="kengaku-r55-controls-", dir="/fast/scratch/hyaku/kengaku-r55"))
    try:
        return run_case(a.case, a.against, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
