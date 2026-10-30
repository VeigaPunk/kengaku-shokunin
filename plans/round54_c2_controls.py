#!/usr/bin/env python3
"""Round 54, claim C2 controls: demonstrate the laundering route, then its closure.

Modes
    --route-only   build a forged fixture lane (a gate whose ENTRY mode exits 1 while its
                   --selftest exits 0) and run the UNMODIFIED round-53 counter
                   (plans/round53_c2_tipstate.py, imported, ``evaluate(..., pins=False)``) over it.
                   The r53 predicate printing PASS on this fixture is the defect evidence:
                   the selected-argv laundering route exists today.  Receipt:
                   .ufo/waves/round-54/claims/c2-route-r53.txt (exit 0 == route demonstrated).
    --closed       the same fixture under the round-54 counter (plans/round54_c2_entrytruth.py,
                   ledger declaring entry truthfully): it must print LAUNDERED / MISMATCH and FAIL.
                   Receipt: .ufo/waves/round-54/claims/c2-route-closed.txt.
    --env-poison   a caller-supplied GIT_CONFIG_GLOBAL flips an r53-env execution of a config-reading
                   fixture gate but not the r54 counter's hermetic execution.
                   Receipt: .ufo/waves/round-54/claims/c2-env-poison.txt.

Scratch discipline: every fixture lives under --work (or TMPDIR); nothing is written under a
hard-coded /tmp path; the work tree is removed on exit unless --keep.  The r53 counter file is
imported unmodified and never edited.  Fixture repos are created in the scratch root and every git
call names -C explicitly (git-fixture rule).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HEAD_ROW = ["## Gate/probe registry", "", "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]

GATE_SRC = '''#!/usr/bin/env python3
import sys
mode = sys.argv[1] if len(sys.argv) > 1 else "entry"
if mode == "--selftest":
    print("selftest ok")
    sys.exit(0)
print("entry failed: fixture gate is broken on purpose")
sys.exit(1)
'''


def _fixture(root: Path, ledger: dict, git: bool = True) -> Path:
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [
        "| `fixture-gate` | gate | `python3 plans/fixture_gate.py` | `0` ok · `1` bad | none | none | none | kengaku |",
    ]) + "\n")
    (root / "plans" / "fixture_gate.py").write_text(GATE_SRC)
    if "r53-tipstate-v1" in (ledger.get("schema") or ""):
        (root / "plans" / "round53-tipstate.json").write_text(json.dumps(ledger, indent=1) + "\n")
    else:
        (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(ledger, indent=1) + "\n")
    if git:
        subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                        "commit", "-qm", "fixture"], check=True)
    return root


R53_LEDGER_LAUNDERING = {
    "schema": "r53-tipstate-v1",
    "rows": {
        "fixture-gate": {
            "argv": ["python3", "plans/fixture_gate.py", "--selftest"],
            "exit": 0,
            "state": "green",
            "kind": "selftest",
            "timeout_s": 60,
        },
    },
}

R54_LEDGER_TRUTHFUL = {
    "schema": "r54-entrytruth-v1",
    "rows": {
        "fixture-gate": {
            "entry_argv": ["python3", "plans/fixture_gate.py"],
            "entry_exit": 1,
            "entry_state": "red",
            "reason": "the fixture gate's entry mode is broken on purpose for this control fixture",
            "evidence": "entry failed: fixture gate is broken on purpose",
            "timeout_s": 60,
        },
    },
}


def route_only(work: Path) -> int:
    r53 = _load("r53tipstate", LANE / "plans" / "round53_c2_tipstate.py")
    root = _fixture(work / "fixture-r53", json.loads(json.dumps(R53_LEDGER_LAUNDERING)))
    rc, lines = r53.evaluate(root, root, work / "route", 1, 60, None, False, False)  # pins=False
    print("== r53 counter (unmodified, pins=False) over the laundering fixture ==")
    print("\n".join(lines))
    passed = any("PREDICATE R53-C2 pass" in ln for ln in lines) and rc == 0
    print(f"ROUTE laundering {'demonstrated' if passed else 'NOT demonstrated'} (r53 rc={rc})")
    return 0 if passed else 1


def closed(work: Path) -> int:
    c54 = _load("r54entry", LANE / "plans" / "round54_c2_entrytruth.py")
    root = _fixture(work / "fixture-r54", json.loads(json.dumps(R54_LEDGER_TRUTHFUL)))
    rc, lines = c54.evaluate(root, root, work / "closed", 1, 60, False)
    print("== r54 counter over the truthfully declared fixture ==")
    print("\n".join(lines))
    # and the laundering variant under the r54 counter must fail with LAUNDERED
    root2 = _fixture(work / "fixture-r54-launder", {
        "schema": "r54-entrytruth-v1",
        "rows": {"fixture-gate": {"entry_argv": ["python3", "plans/fixture_gate.py"],
                                  "entry_exit": 0, "entry_state": "green", "timeout_s": 60}},
    })
    rc2, lines2 = c54.evaluate(root2, root2, work / "closed2", 1, 60, False)
    print("== r54 counter over the laundering variant ==")
    print("\n".join(lines2))
    flagged = any("LAUNDERED fixture-gate" in ln for ln in lines2) and rc2 == 1
    # truthful fixture: entry_exit=1, observed=1 -> no mismatch; on a clean fixture clone the
    # predicate must pass
    truthful_ok = rc == 0
    print(f"ROUTE closed={'yes' if (flagged and truthful_ok) else 'NO'} "
          f"(truthful rc={rc}, laundering flagged={flagged})")
    return 0 if (flagged and truthful_ok) else 1


def env_poison(work: Path) -> int:
    c54 = _load("r54entry", LANE / "plans" / "round54_c2_entrytruth.py")
    r53 = _load("r53tipstate", LANE / "plans" / "round53_c2_tipstate.py")
    root = _fixture(work / "fixture-env", {
        "schema": "r54-entrytruth-v1",
        "rows": {"fixture-gate": {"entry_argv": ["python3", "plans/fixture_gate.py", "who"],
                                  "entry_exit": 0, "entry_state": "green", "timeout_s": 60}},
    })
    gate = root / "plans" / "gate_who.py"
    gate.write_text('''#!/usr/bin/env python3
import subprocess, sys
p = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True)
print("user=%s" % p.stdout.strip())
sys.exit(0)
''')
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                    "commit", "-qm", "gate"], check=True)
    poison = work / "poison.gitconfig"
    poison.write_text('[user]\n\tname = poisoned-identity\n')
    env = dict(os.environ)
    env["GIT_CONFIG_GLOBAL"] = str(poison)
    # r53-style inherited env: the poison reaches the row
    p = subprocess.run(["python3", "plans/gate_who.py"], cwd=root, capture_output=True, text=True, env=env)
    leaked = "poisoned-identity" in (p.stdout or "")
    # r54 counter env: the poison cannot reach the row
    tmp = Path(tempfile.mkdtemp(dir=str(work)))
    p2 = subprocess.run(["python3", "plans/gate_who.py"], cwd=root, capture_output=True, text=True,
                        env=c54.hermetic_env(tmp))
    hermetic = "poisoned-identity" not in (p2.stdout or "")
    print(f"ENV poison under r53-style inherited env: {'LEAKED' if leaked else 'not leaked'} ({p.stdout.strip()})")
    print(f"ENV poison under r54 hermetic env: {'BLOCKED' if hermetic else 'LEAKED'} ({p2.stdout.strip()})")
    ok = leaked and hermetic
    print(f"ENV control {'holds' if ok else 'FAILS'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--route-only", action="store_true")
    g.add_argument("--closed", action="store_true")
    g.add_argument("--env-poison", action="store_true")
    ap.add_argument("--work", default=None)
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="r54c2ctl-"))
    work.mkdir(parents=True, exist_ok=True)
    if args.route_only:
        rc = route_only(work)
    elif args.closed:
        rc = closed(work)
    else:
        rc = env_poison(work)
    if not args.keep:
        shutil.rmtree(work, ignore_errors=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
