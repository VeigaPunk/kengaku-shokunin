#!/usr/bin/env python3
"""R55 wave-1 seat M2EntryArgvMutants — bounded mutation probe.

Target: plans/round55_c2_entryargv.py NEW legs (L1 argv identity, L2 wrapper,
L3 abbreviation, L4 registry-cell ground truth). Scratch copies only; the lane
file is never written. Bounded: run_row timeout 60 s per execution, overall
probe deadline 1500 s (25 min).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import py_compile
import shutil
import subprocess
import sys
import time
from pathlib import Path

SEAT = "M2EntryArgvMutants"
SCRATCH = Path("/fast/scratch/hyaku/kengaku-r55/M2EntryArgvMutants")
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
R55 = LANE / "plans" / "round55_c2_entryargv.py"
R54 = LANE / "plans" / "round54_c2_entrytruth.py"
CONTROLS = LANE / "plans" / "round55_c2_controls.py"
PROBE_DEADLINE = time.time() + 1500  # 25 min, per assignment
STEP_TIMEOUT = 60                    # 60 s steps

T0 = time.time()


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def elapsed() -> float:
    return round(time.time() - T0, 1)


# ----------------------------------------------------------------- fixtures
HEAD_ROW = ["## Gate/probe registry", "",
            "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]
RED_DECL = {
    "reason": "the fixture gate entry mode fails on purpose so this row is declared red with evidence attached",
    "evidence": "entry failed: fixture gate is broken on purpose",
}

# controls' GATE_SRC is imported byte-exact from the lane (GATE_STD below).
GATE_NOC = '''#!/usr/bin/env python3
import sys
args = sys.argv[1:]
if "--selftest" in args:
    print("selftest ok")
    sys.exit(0)
print("entry failed: fixture gate is broken on purpose")
sys.exit(1)
'''
GATE_GO = '''#!/usr/bin/env python3
import sys
args = sys.argv[1:]
if "--selftest" in args or "--go" in args:
    print("selftest ok")
    sys.exit(0)
print("entry failed: fixture gate is broken on purpose")
sys.exit(1)
'''

REG_BARE = ("| `fixture-gate` | gate | `python3 plans/fixture_gate.py` | "
            "`0` ok · `1` bad | none | none | none | kengaku |")
REG_CTOK = ("| `fixture-gate` | gate | `python3 plans/fixture_gate.py -cprint('wrapper green')` | "
            "`0` ok · `1` bad | none | none | none | kengaku |")
REG_ABBREV = ("| `fixture-gate` | gate | `python3 plans/fixture_gate.py --selft` | "
              "`0` ok · `1` bad | none | none | none | kengaku |")

ARG_BARE = ["python3", "plans/fixture_gate.py"]


def git_fixture(root: Path, skill_line: str, gate_src: str, ledger_argv: list,
                exit_: int, state: str) -> Path:
    """One-row git fixture with the toplevel guard (mirrors controls._fixture)."""
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [skill_line]) + "\n")
    (root / "plans" / "fixture_gate.py").write_text(gate_src)
    row = {"entry_argv": list(ledger_argv), "entry_exit": exit_,
           "entry_state": state, "timeout_s": 60}
    if state == "red":
        row.update(RED_DECL)
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps(
        {"schema": "r54-entrytruth-v1", "rows": {"fixture-gate": row}}, indent=1) + "\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                    "commit", "-qm", "fixture"], check=True)
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert Path(top).resolve() == root.resolve(), f"toplevel guard: {top} != {root}"
    return root


def build_fixtures() -> dict:
    import shlex
    fx = {}
    fx["F0-truthful-baseline"] = git_fixture(
        FIX / "F0", REG_BARE, GATE_STD, ARG_BARE, 1, "red")
    fx["F1-L1sole-positional-decoy"] = git_fixture(
        FIX / "F1", REG_BARE, GATE_STD, ARG_BARE + ["decoy-positional"], 1, "red")
    fx["F2-L2sole-inline-c-token"] = git_fixture(
        FIX / "F2", REG_CTOK, GATE_NOC, shlex.split("python3 plans/fixture_gate.py -cprint('wrapper green')"),
        1, "red")
    fx["F3-L3sole-registry-abbrev"] = git_fixture(
        FIX / "F3", REG_ABBREV, GATE_STD, ARG_BARE + ["--selft"], 0, "green")
    fx["F4c-laundering-go-flag"] = git_fixture(
        FIX / "F4c", REG_BARE, GATE_GO, ARG_BARE + ["--go"], 0, "green")
    # the two FROZEN controls fixtures, built by the lane's own builder
    for case in ("abbreviated-selftest", "uv-decoy-script"):
        fx[f"FRZN-{case}"] = controls._fixture(FIX / f"FRZN-{case}", list(controls.CASES[case]))
    return fx


# ----------------------------------------------------------------- mutants
M1 = ("        if led != reg:\n",
      "        if False and led != reg:  # MUTANT M1: L1 comparison silenced\n")
M2 = ("        w = _wrapper_defect(n, led)\n",
      "        w = None  # MUTANT M2: L2 wrapper check silenced\n")
M3 = ("        a = _abbrev_defect(n, led, body_flags)\n",
      "        a = None  # MUTANT M3: L3 abbreviation check silenced\n")
M4 = ('                spec["entry_argv"] = registry_entry_argv(s["rows"][n])\n',
      '                spec["entry_argv"] = list(s["ledger"]["rows"][n]["entry_argv"])'
      '  # MUTANT M4: ledger-argv execution (r54 behavior)\n')

MUTANTS = {
    "M1-L1-silenced": [M1],
    "M2-L2-silenced": [M2],
    "M3-L3-silenced": [M3],
    "M4-L4-ledger-argv": [M4],
    "M1M4-combined-r54-behavior": [M1, M4],  # supplementary probe, not a single-leg mutant
}


def make_module(name: str) -> Path:
    d = MODS / name / "plans"
    d.mkdir(parents=True, exist_ok=True)
    src = R55.read_text()
    for old, new in MUTANTS.get(name, []):
        assert src.count(old) == 1, f"{name}: patch site not unique: {old!r} x{src.count(old)}"
        src = src.replace(old, new)
    (d / "round55_c2_entryargv.py").write_text(src)
    shutil.copyfile(R54, d / "round54_c2_entrytruth.py")
    out = d / "round55_c2_entryargv.py"
    py_compile.compile(str(out), doraise=True)
    return out


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(f"r55c2_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TAGS = ("ARGV-DEFECT", "WRAPPER-DEFECT", "ABBREV-DEFECT", "LAUNDERED", "MISMATCH",
        "TIMEOUT", "EVIDENCE-MISSING", "PREDICATE", "RUN executed", "ROWS registry",
        "BINDING l1", "SOURCE rev")


def detect(mod, fixture: Path, work: Path) -> dict:
    t0 = time.time()
    rc, lines = mod.evaluate(fixture, fixture, work, 1, STEP_TIMEOUT, False)
    keep = [ln for ln in lines if any(t in ln for t in TAGS)]
    return {"rc": rc, "secs": round(time.time() - T0, 2), "dur": round(time.time() - t0, 2),
            "salient": keep}


# ----------------------------------------------------------------- main
SCRATCH.mkdir(parents=True, exist_ok=True)
MODS, FIX, RUNS, REC = SCRATCH / "mods", SCRATCH / "fixtures", SCRATCH / "runs", SCRATCH / "receipts"
for d in (MODS, FIX, RUNS, REC):
    d.mkdir(exist_ok=True)

print(f"[{elapsed()}s] loading lane controls builder (read-only import)")
cspec = importlib.util.spec_from_file_location("r55controls", CONTROLS)
controls = importlib.util.module_from_spec(cspec)
cspec.loader.exec_module(controls)
GATE_STD = controls.GATE_SRC

print(f"[{elapsed()}s] building module variants (scratch copies)")
order = ["pristine"] + list(MUTANTS)
mods = {}
hashes = {"pristine_r55_lane": sha(R55), "pristine_r55_copy": None, "r54": sha(R54)}
for name in order:
    p = make_module(name)
    hashes.setdefault("mutants", {})[name] = sha(p)
    if name == "pristine":
        hashes["pristine_r55_copy"] = sha(p)
        assert hashes["pristine_r55_copy"] == hashes["pristine_r55_lane"], "pristine copy mismatch"
    mods[name] = load_mod(name, p)
print(f"[{elapsed()}s] modules ready: {', '.join(order)}")

print(f"[{elapsed()}s] pristine counter selftest (detector validity)")
st_rc = mods["pristine"].selftest(RUNS / "selftest")
print(f"[{elapsed()}s] pristine selftest exit={st_rc}")

print(f"[{elapsed()}s] building fixtures")
fixtures = build_fixtures()
print(f"[{elapsed()}s] fixtures: {', '.join(fixtures)}")

results = {}
for fname, froot in fixtures.items():
    for mname in order:
        if time.time() > PROBE_DEADLINE:
            results[f"{mname}|{fname}"] = {"rc": None, "secs": elapsed(), "salient": ["PROBE DEADLINE — INCONCLUSIVE"]}
            continue
        wd = RUNS / f"w-{mname}-{fname}"
        results[f"{mname}|{fname}"] = detect(mods[mname], froot, wd)
        shutil.rmtree(wd, ignore_errors=True)

# verdicts
prow = {f: results[f"pristine|{f}"]["rc"] for f in fixtures}
baseline_ok = prow["F0-truthful-baseline"] == 0
verdicts = {}
for mname in MUTANTS:
    flips = [f for f in fixtures if prow[f] == 1 and results[f"{mname}|{f}"]["rc"] == 0]
    overkill = [f for f in fixtures if prow[f] == 0 and results[f"{mname}|{f}"]["rc"] == 1]
    verdicts[mname] = {
        "flips_to_pass": flips,
        "breaks_truthful_baseline": overkill,
        "verdict": "KILLED" if flips else "SURVIVED",
        "baseline_ok": baseline_ok,
    }

out = {
    "seat": SEAT, "started_at_unix": T0, "probe_deadline_s": 1500, "step_timeout_s": STEP_TIMEOUT,
    "hashes": hashes, "baseline": {"pristine_selftest_exit": st_rc, "truthful_F0_rc": prow["F0-truthful-baseline"],
                                   "baseline_ok": baseline_ok},
    "results": results, "pristine_rc_by_fixture": prow, "verdicts": verdicts,
}
(REC / "matrix.json").write_text(json.dumps(out, indent=1))

# human matrix
cols = order
lines = ["RC MATRIX (pristine vs mutants) — fixture x module", "=" * 78]
for fname in fixtures:
    row = [f"{fname:34s}"]
    for mname in order:
        row.append(f"{results[f'{mname}|{fname}']['rc']!s:>4}")
    lines.append(" ".join(row))
lines.append("")
lines.append(f"{'fixture':34s} " + " ".join(f"{c[:4]:>4}" for c in cols))
for fname in fixtures:
    lines.append(f"{fname:34s} " + " ".join(f"{results[f'{mname}|{fname}']['rc']!s:>4}" for mname in order))
lines.append("")
lines.append("VERDICTS")
for mname, v in verdicts.items():
    lines.append(f"  {mname:30s} {v['verdict']:9s} flips_to_pass={v['flips_to_pass']} "
                 f"baseline_breaks={v['breaks_truthful_baseline']}")
lines.append(f"  baseline: pristine selftest exit={st_rc}, F0 truthful rc={prow['F0-truthful-baseline']} "
             f"(baseline_ok={baseline_ok})")
(REC / "matrix.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
print(f"\n[{elapsed()}s] probe complete; receipts in {REC}")
