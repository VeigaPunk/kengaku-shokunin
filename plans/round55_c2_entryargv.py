#!/usr/bin/env python3
"""Round 55, claim C2: entry-argv structural binding on top of the unchanged r54 counter.

Frozen 2026-10-30 before any after-run data (plans/round-55-claims.md, R55-C2).  The round-54
entry-truth counter (``plans/round54_c2_entrytruth.py``) executes each ledger row's declared
``entry_argv`` without binding it to the SKILL registry's declared entry: a ledger row whose
argv is an argparse-prefix abbreviation (``--selft``) or a ``uv`` wrapper around an inline
``-c`` program passes while the registry-declared entry truly fails
(``.ufo/waves/round-54/w1/R2C2Counter/laundering-probes.txt``; fixtures in
``plans/round55_c2_controls.py``).  This counter IMPORTS the unchanged r54 module and reuses
its static legs, hermetic execution and ledger, adding three binding legs:

  L1 ledger<->registry argv identity (ARGV-DEFECT) — every ledger row's ``entry_argv`` must
    token-equal the registry row's declared entry command (the FIRST backtick span in the
    entry cell that starts with ``python3``, shlex-split); a mismatch fails statically.
  L2 interpreter identity, no wrappers (WRAPPER-DEFECT) — the declared argv's ``argv[0]``
    must be a real interpreter (``python3``/``python``) and no argv token may be a known
    wrapper (``uv``/``pipx``/``poetry``/``npx``/``uvx``) or start with ``-c`` (inline
    program).
  L3 no flag prefix abbreviation (ABBREV-DEFECT) — a flag token that does not appear
    verbatim in the script body but is a proper prefix of a flag string that does appear is
    an argparse abbreviation, checked without executing.
  L4 per-row ground truth — unchanged from r54: each row is executed hermetically with the
    REGISTRY cell argv (identical to the ledger argv once L1 is clean); green rows must
    exit 0, red rows must exit nonzero and print their declared evidence fragment.

Exit codes: 0 predicate holds · 1 predicate fails · 2 setup/usage.
Usage:
    python3 plans/round55_c2_entryargv.py --lane . --source CLEAN_CLONE --work SCRATCH \
        [--jobs 3] [--timeout 900]
    python3 plans/round55_c2_entryargv.py --lane . --dry
    python3 plans/round55_c2_entryargv.py --selftest [--work SCRATCH]
Honours TMPDIR/--work; never writes under a hard-coded /tmp path.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent

# Rebound from the unchanged r54 module at load time (see _load_r54); the r54 module is the
# single source of truth for the registry/ledger constants and helpers this counter reuses.
_R54 = None
REGISTRY = None   # r54.REGISTRY_HEADING
LEDGER = None     # r54.LEDGER  (plans/round54-entrytruth.json)
SCHEMA = None     # r54.SCHEMA  (r54-entrytruth-v1)
MIN_REASON_WORDS = None  # r54.MIN_REASON_WORDS

WRAPPERS = {"uv", "pipx", "poetry", "npx", "uvx"}
BODY_FLAG = re.compile(r"-{1,2}[A-Za-z0-9][A-Za-z0-9_-]*")
INTERPRETERS = ("python3", "python")


def _load_r54():
    """Import the unchanged round-54 module (same pattern as round55_c2_controls.py::_load)."""
    global _R54, REGISTRY, LEDGER, SCHEMA, MIN_REASON_WORDS
    if _R54 is not None:
        return _R54
    p = LANE / "plans" / "round54_c2_entrytruth.py"
    if not p.is_file():
        return None
    spec = importlib.util.spec_from_file_location("round54_c2_entrytruth", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _R54 = mod
    REGISTRY = mod.REGISTRY_HEADING
    LEDGER = mod.LEDGER
    SCHEMA = mod.SCHEMA
    MIN_REASON_WORDS = mod.MIN_REASON_WORDS
    return mod


def registry_entry_argv(line: str) -> list[str] | None:
    """Token list of the FIRST backtick span in the entry cell starting with ``python3``.

    shlex-split of that span; None when the cell has no such span (or it is unparseable).
    """
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    entry = cells[2] if len(cells) > 2 else ""
    for m in re.finditer(r"`([^`]*)`", entry):
        span = m.group(1).strip()
        if span.startswith("python3"):
            try:
                return shlex.split(span)
            except ValueError:
                return None
    return None


def _wrapper_defect(name: str, argv) -> str | None:
    """L2: argv[0] must be python3/python; no wrapper token, no inline ``-c`` program."""
    if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
        return f"{name}: argv is not a non-empty token list"
    if argv[0] not in INTERPRETERS:
        return f"{name}: argv[0]={argv[0]!r} is not an interpreter ({'/'.join(INTERPRETERS)})"
    for t in argv:
        if t in WRAPPERS:
            return f"{name}: wrapper token {t!r}"
        if t.startswith("-c"):
            return f"{name}: inline program token {t!r} (-c)"
    return None


def _abbrev_defect(name: str, argv, body_flags: set[str]) -> str | None:
    """L3: a flag token absent verbatim from the script body but a proper prefix of a body
    flag is an argparse prefix abbreviation (checked without executing)."""
    if not isinstance(argv, list):
        return None
    for t in argv[1:]:
        if not isinstance(t, str) or not t.startswith("-") or len(t) < 2:
            continue
        if t in body_flags:
            continue
        if any(f != t and f.startswith(t) for f in body_flags):
            return f"{name}: flag {t!r} abbreviates a script flag (prefix, not verbatim)"
    return None


def binding_static_legs(root: Path, m):
    """r54 static legs PLUS the three new binding defect lists.

    Returns the r54 result dict extended with ``binding_l1`` (ledger<->registry argv
    mismatches), ``wrapper_defect`` (L2) and ``abbrev_defect`` (L3); L1 entries are also
    appended to ``argv_defect`` so the ROWS ``argv_defect=N`` field and ``static_ok`` cover
    them exactly as the frozen after predicate requires.
    """
    s = m.static_legs(root)
    if s is None:
        return None
    s["binding_l1"] = []
    s["wrapper_defect"] = []
    s["abbrev_defect"] = []
    ledger = s["ledger"]
    if ledger is None:
        return s
    lr = ledger["rows"]
    for n in sorted(set(s["rows"]) & set(lr)):
        if any(d.startswith(f"{n}:") for d in s["argv_defect"]) or any(d.startswith(f"{n}:") for d in s["bad_decl"]):
            continue  # r54 legs already rejected this row; their defect lines stand
        sp = lr[n]
        if not isinstance(sp, dict):
            continue
        led = sp.get("entry_argv")
        reg = registry_entry_argv(s["rows"][n])
        if led != reg:
            why = (f"{n}: registry entry cell has no python3 command"
                   if reg is None else
                   f"{n}: ledger entry_argv != registry cell argv {led!r} != {reg!r}")
            s["binding_l1"].append(why)
            s["argv_defect"].append(why)
        w = _wrapper_defect(n, led)
        if w:
            s["wrapper_defect"].append(w)
        script = m.row_script(s["rows"][n])
        body_flags: set[str] = set()
        if script is not None:
            p = root / script
            if p.is_file():
                body_flags = set(BODY_FLAG.findall(p.read_text(errors="replace")))
        a = _abbrev_defect(n, led, body_flags)
        if a:
            s["abbrev_defect"].append(a)
    return s


def _keep(work: Path, r: dict) -> None:
    (work / f"disagreed-{re.sub(r'[^A-Za-z0-9_.-]', '_', r['name'])}.txt").write_text(
        f"exit={r['rc']} sec={r['sec']}\n{r['out']}")


def evaluate(lane: Path, source: Path | None, work: Path | None, jobs: int, timeout: int,
             dry: bool):
    m = _load_r54()
    if m is None:
        print("SETUP plans/round54_c2_entrytruth.py absent", file=sys.stderr)
        return 2, []
    root = source if source is not None else lane
    s = binding_static_legs(root, m)
    if s is None:
        print("SETUP SKILL.md absent", file=sys.stderr)
        return 2, []
    lines: list[str] = []
    n_reg = len(s["rows"])
    n_led = len(s["ledger"]["rows"]) if s["ledger"] else 0
    lines.append(f"ROWS registry={n_reg} ledger={n_led} missing={len(s['missing'])} extra={len(s['extra'])} "
                 f"argv_defect={len(s['argv_defect'])} wrapper_defect={len(s['wrapper_defect'])} "
                 f"abbrev_defect={len(s['abbrev_defect'])} bad_decl={len(s['bad_decl'])} "
                 f"duplicate_names={len(s['dups'])} bad_table_lines={len(s['badname'])} headings={s['headings']}")
    for k, lab in (("missing", "MISSING"), ("extra", "EXTRA"), ("bad_decl", "BAD-DECL")):
        for n in s[k]:
            lines.append(f"  {lab} {n}")
    for d in s["argv_defect"]:
        lines.append(f"  ARGV-DEFECT {d}")
    for d in s["wrapper_defect"]:
        lines.append(f"  WRAPPER-DEFECT {d}")
    for d in s["abbrev_defect"]:
        lines.append(f"  ABBREV-DEFECT {d}")
    for n in s["dups"]:
        lines.append(f"  DUPLICATE {n}")
    if s["ledger_err"]:
        lines.append(f"  LEDGER {s['ledger_err']}")
    lines.append(f"BINDING l1={len(s['binding_l1'])} l2={len(s['wrapper_defect'])} "
                 f"l3={len(s['abbrev_defect'])}")
    static_ok = (n_reg > 0 and s["headings"] == 1 and not s["ledger_err"]
                 and not (s["missing"] or s["extra"] or s["argv_defect"] or s["bad_decl"]
                          or s["dups"] or s["badname"] or s["wrapper_defect"] or s["abbrev_defect"]))
    executed = mism = tmo = evmiss = laundered = 0
    obs_green = obs_red = 0
    clean = rev_ok = False
    redeclared = 0
    if not dry and s["ledger"]:
        if source is None or work is None:
            print("SETUP --source and --work are required unless --dry", file=sys.stderr)
            return 2, []
        if (source / ".git").exists():
            st = subprocess.run(["git", "-C", str(source), "status", "--porcelain"], capture_output=True, text=True)
            clean = st.returncode == 0 and st.stdout.strip() == ""
            sr = m.git_rev(source)
            lr_ = m.git_rev(lane) if (lane / ".git").exists() else None
            rev_ok = sr is not None and (lr_ is None or lr_ == sr)
            lines.append(f"SOURCE rev={sr} clean={'yes' if clean else 'NO'} lane_rev_equal={'yes' if rev_ok else 'NO'}")
        else:
            lines.append("SOURCE not a git work tree clean=NO")
        work.mkdir(parents=True, exist_ok=True)
        names = sorted(set(s["rows"]) & set(s["ledger"]["rows"])
                       - {n for n in s["bad_decl"]})
        names = [n for n in names if not any(d.startswith(f"{n}:") for d in s["argv_defect"])]
        bad_binding = {d.split(":", 1)[0] for d in s["wrapper_defect"] + s["abbrev_defect"]}
        names = [n for n in names if n not in bad_binding]
        workers = [m.Worker(source, work, i) for i in range(max(1, jobs))]
        free = list(range(len(workers)))
        lock = threading.Lock()
        r53_green_nonentry = m.load_r53_green_nonentry(lane)

        def job(n):
            with lock:
                i = free.pop()
            try:
                # Execution uses the REGISTRY cell argv — identical to the ledger argv once
                # L1 is clean — through the unchanged r54 Worker/run_row hermetic path.
                spec = dict(s["ledger"]["rows"][n])
                spec["entry_argv"] = registry_entry_argv(s["rows"][n])
                return m.run_row(workers[i], n, spec, timeout, work)
            finally:
                with lock:
                    free.append(i)

        with ThreadPoolExecutor(max(1, jobs)) as ex:
            results = list(ex.map(job, names))
        for r in results:
            sp = s["ledger"]["rows"][r["name"]]
            executed += 1
            if r["rc"] == "TIMEOUT":
                tmo += 1
                lines.append(f"  TIMEOUT {r['name']} after {sp.get('timeout_s') or timeout}s")
                continue
            rc = r["rc"]
            if rc == 0:
                obs_green += 1
            else:
                obs_red += 1
            if rc != sp["entry_exit"]:
                if sp["entry_state"] == "green" and rc != 0:
                    laundered += 1
                    lines.append(f"  LAUNDERED {r['name']} declared green, entry exit={rc}")
                else:
                    mism += 1
                    lines.append(f"  MISMATCH {r['name']} declared exit={sp['entry_exit']} observed exit={rc} sec={r['sec']}")
                _keep(work, r)
                continue
            if rc != 0 and sp["entry_state"] == "red" and sp.get("evidence") not in r["out"]:
                evmiss += 1
                lines.append(f"  EVIDENCE-MISSING {r['name']} fragment not in output")
                _keep(work, r)
        for n in names:
            sp = s["ledger"]["rows"][n]
            if n in r53_green_nonentry and sp.get("entry_state") == "red":
                redeclared += 1
        for w in workers:
            shutil.rmtree(w.dir.parent, ignore_errors=True)
        dg = sum(1 for n in names if s["ledger"]["rows"][n]["entry_state"] == "green")
        dr = len(names) - dg
        lines.append(f"RUN executed={executed} timeout={tmo} mismatched={mism} evidence_missing={evmiss} "
                     f"laundered={laundered}")
        lines.append(f"TIPSTATE entry_declared_green={dg} entry_declared_red={dr} "
                     f"observed_green={obs_green} observed_red={obs_red}")
        lines.append(f"MIGRATION redeclared={redeclared} r53_green_nonentry={len(r53_green_nonentry)}")
    if dry:
        lines.append("DRY static legs only: no predicate")
        return (0 if static_ok else 1), lines
    ok = (static_ok and executed == n_reg and tmo == 0 and mism == 0 and evmiss == 0
          and laundered == 0 and clean and rev_ok)
    lines.append(f"PREDICATE R55-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# --------------------------------------------------------------------------------------- selftest
HEAD_ROW = ["## Gate/probe registry", "",
            "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]

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

REGISTRY_LINE = ("| `fixture-gate` | gate | `python3 plans/fixture_gate.py` | `0` ok · `1` bad | "
                 "none | none | none | kengaku |")
ENTRY_ARGV = ["python3", "plans/fixture_gate.py"]


def _mk_fixture(root: Path, ledger_rows: dict) -> Path:
    """Fixture-building shape of plans/round55_c2_controls.py::_fixture (git fixture with a
    toplevel guard, never a mutating git against the lane)."""
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW + [REGISTRY_LINE]) + "\n")
    (root / "plans" / "fixture_gate.py").write_text(GATE_SRC)
    (root / "plans" / "round54-entrytruth.json").write_text(json.dumps({
        "schema": "r54-entrytruth-v1", "rows": ledger_rows}, indent=1) + "\n")
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f",
                    "commit", "-qm", "fixture"], check=True)
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    if Path(top).resolve() != root.resolve():
        raise RuntimeError(f"fixture root guard: toplevel {top} != {root}")
    return root


def _case_ledger(argv: list[str], exit_: int, state: str) -> dict:
    row = {"entry_argv": list(argv), "entry_exit": exit_, "entry_state": state, "timeout_s": 60}
    if state == "red":
        row["reason"] = "the fixture gate entry mode fails on purpose so this row is declared red with evidence attached"
        row["evidence"] = "entry failed: fixture gate is broken on purpose"
    return {"fixture-gate": row}


def selftest(work: Path | None = None) -> int:
    if _load_r54() is None:
        print("[selftest] FAIL r54-counter-absent")
        return 1
    if work is not None:
        work.mkdir(parents=True, exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix="r55c2-selftest-", dir=str(work) if work else None))
    cases = []

    def run(case_no: int, ledger_rows: dict):
        root = _mk_fixture(base / f"t{case_no}", ledger_rows)
        return root, evaluate(root, root, base / f"w{case_no}", 1, 60, dry=False)

    def check(label, rc, lines, want_rc, want_in=()):
        ok = rc == want_rc and all(any(w in ln for ln in lines) for w in want_in)
        cases.append((label, ok, f"rc={rc}"))
        return ok

    # case 1: truthful fixture passes (row declared red at the true entry exit, evidence present)
    root, (rc, lines) = run(1, _case_ledger(ENTRY_ARGV, 1, "red"))
    check("truthful-fixture", rc, lines, 0,
          want_in=("PREDICATE R55-C2 pass", "BINDING l1=0 l2=0 l3=0", "RUN executed=1"))

    # case 2: ledger-tampered argv (positional decoy the r54 legs permit) -> L1 ARGV-DEFECT + fail
    root, (rc, lines) = run(2, _case_ledger(ENTRY_ARGV + ["decoy-positional"], 0, "green"))
    check("argv-tamper-flagged", rc, lines, 1,
          want_in=("ARGV-DEFECT fixture-gate:", "BINDING l1=1", "PREDICATE R55-C2 fail"))

    # case 3: uv wrapper around an inline -c program (controls' uv-decoy-script case) -> WRAPPER-DEFECT
    root, (rc, lines) = run(3, _case_ledger(
        ["uv", "run", "--no-project", "--offline", "python3", "-cprint('wrapper green')"]
        + ENTRY_ARGV, 0, "green"))
    check("uv-wrapper-flagged", rc, lines, 1,
          want_in=("WRAPPER-DEFECT fixture-gate:", "PREDICATE R55-C2 fail"))

    # case 4: --selft argparse prefix abbreviation (controls' abbreviated-selftest case) -> ABBREV-DEFECT
    root, (rc, lines) = run(4, _case_ledger(ENTRY_ARGV + ["--selft"], 0, "green"))
    check("abbrev-flag-flagged", rc, lines, 1,
          want_in=("ABBREV-DEFECT fixture-gate:", "PREDICATE R55-C2 fail"))

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, detail in cases:
        print(f"[selftest] {'PASS' if ok else 'FAIL'} {name} {detail}")
    print(f"[selftest] {passed}/{len(cases)} PASS")
    shutil.rmtree(base, ignore_errors=True)
    return 0 if passed == len(cases) else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--source", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(Path(args.work) if args.work else None)
    lane = Path(args.lane)
    source = Path(args.source) if args.source else None
    work = Path(args.work) if args.work else None
    if work is None and not args.dry:
        work = Path(tempfile.mkdtemp(prefix="r55c2-"))
    rc, lines = evaluate(lane, source, work, args.jobs, args.timeout, args.dry)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
