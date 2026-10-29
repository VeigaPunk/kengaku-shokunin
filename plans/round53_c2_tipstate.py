#!/usr/bin/env python3
"""Round 53, claim C2: registry tip-state truth (executed leg per row).

Q42(c): a row-existence counter is claimed as existence only; "the registry is truthful" needs a second,
executed leg per row.  Every row of SKILL.md's *## Gate/probe registry* gets one entry in the committed
ledger ``plans/round53-tipstate.json`` that declares, for a frozen argv, the exit code the instrument
returns on a clean checkout of the tree under test and, when it is not clean, a verbatim output fragment
and a reason.  This counter re-executes every argv in a scratch copy of ``--source`` and compares.

Exit codes: 0 predicate holds · 1 predicate fails · 2 setup/usage.
Usage:
    python3 plans/round53_c2_tipstate.py --lane . --source CLEAN_CLONE --work SCRATCH [--jobs 4] [--timeout 900]
    python3 plans/round53_c2_tipstate.py --lane . --dry          # static legs only, nothing is executed
    python3 plans/round53_c2_tipstate.py --selftest
Honours TMPDIR/--work; never writes under a hard-coded /tmp path.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REGISTRY_HEADING = "## Gate/probe registry"
LEDGER = "plans/round53-tipstate.json"
SCHEMA = "r53-tipstate-v1"
NAME_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
SCRIPT = re.compile(r"python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)")
MIN_REASON_WORDS = 10
MAX_HELP_FRACTION = 0.10   # rows whose only runnable argv is --help (weak truth) may not exceed this share


def registry_block(text: str) -> str:
    i = text.find(REGISTRY_HEADING)
    if i < 0:
        return ""
    j = text.find("\n## ", i + 1)
    return text[i:j] if j > 0 else text[i:]


def registry_rows(skill_text: str) -> dict[str, str]:
    """name -> full row line (names are the first backticked cell; escaped pipes never split a name)."""
    rows: dict[str, str] = {}
    dup: list[str] = []
    for line in registry_block(skill_text).splitlines():
        m = NAME_ROW.match(line)
        if not m:
            continue
        n = m.group(1)
        if n in rows:
            dup.append(n)
        rows[n] = line
    rows["__dups__"] = ",".join(dup) if dup else ""
    return rows


def row_script(line: str) -> str | None:
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    entry = cells[2] if len(cells) > 2 else ""
    m = SCRIPT.search(entry)
    return m.group(1) if m else None


def load_ledger(lane: Path):
    p = lane / LEDGER
    if not p.is_file():
        return None, f"ledger absent: {LEDGER}"
    try:
        d = json.loads(p.read_text())
    except Exception as e:  # noqa: BLE001
        return None, f"ledger unreadable: {e}"
    if d.get("schema") != SCHEMA or not isinstance(d.get("rows"), dict):
        return None, "ledger schema mismatch"
    return d, ""


class Worker:
    """One scratch copy of the source, reset between rows."""

    def __init__(self, source: Path, root: Path, idx: int):
        self.dir = root / f"w{idx}" / "src"
        self.dir.parent.mkdir(parents=True, exist_ok=True)
        if (source / ".git").exists():
            subprocess.run(["git", "clone", "-q", "--shared", str(source), str(self.dir)], check=True)
            self.git = True
        else:
            shutil.copytree(source, self.dir)
            self.git = False

    def reset(self):
        if self.git:
            subprocess.run(["git", "-C", str(self.dir), "reset", "-q", "--hard"], check=False)
            subprocess.run(["git", "-C", str(self.dir), "clean", "-q", "-fdx"], check=False)


def run_row(w: Worker, name: str, spec: dict, default_timeout: int, tmp_root: Path) -> dict:
    argv = spec.get("argv")
    t = int(spec.get("timeout_s") or default_timeout)
    w.reset()
    tmp = tmp_root / f"tmp-{re.sub(r'[^A-Za-z0-9_.-]', '_', name)}"
    tmp.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "TMPDIR": str(tmp)}
    t0 = time.time()
    try:
        p = subprocess.run(argv, cwd=w.dir, capture_output=True, text=True, timeout=t, env=env)
        out = (p.stdout or "") + (p.stderr or "")
        rc: int | str = p.returncode
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""))
        rc = "TIMEOUT"
    except Exception as e:  # noqa: BLE001
        out, rc = f"ERROR {e}", "ERROR"
    shutil.rmtree(tmp, ignore_errors=True)
    return {"name": name, "rc": rc, "out": out, "sec": round(time.time() - t0, 1)}


def static_legs(lane: Path):
    skill = lane / "SKILL.md"
    if not skill.is_file():
        return None
    rows = registry_rows(skill.read_text())
    dups = [d for d in rows.pop("__dups__").split(",") if d]
    ledger, err = load_ledger(lane)
    res = {"rows": rows, "dups": dups, "ledger": ledger, "ledger_err": err,
           "missing": [], "extra": [], "entry_mismatch": [], "bad_decl": [], "bad_reason": []}
    if ledger is None:
        res["missing"] = sorted(rows)
        return res
    lr = ledger["rows"]
    res["missing"] = sorted(set(rows) - set(lr))
    res["extra"] = sorted(set(lr) - set(rows))
    for n in sorted(set(rows) & set(lr)):
        sp = lr[n]
        argv = sp.get("argv")
        script = row_script(rows[n])
        if (not isinstance(argv, list) or len(argv) < 2 or not all(isinstance(a, str) for a in argv)
                or script is None or script not in argv):
            res["entry_mismatch"].append(n)
            continue
        ex, st = sp.get("exit"), sp.get("state")
        if (not isinstance(ex, int) or isinstance(ex, bool) or st not in ("green", "red") or (st == "green") != (ex == 0)
                or sp.get("kind") not in ("entry", "selftest", "help")):
            res["bad_decl"].append(n)
            continue
        if st == "red":
            reason = str(sp.get("reason", ""))
            ev = sp.get("evidence")
            if len(reason.split()) < MIN_REASON_WORDS or not isinstance(ev, str) or len(ev.strip()) < 6:
                res["bad_reason"].append(n)
    return res


def evaluate(lane: Path, source: Path | None, work: Path | None, jobs: int, timeout: int, only: set[str] | None,
             dry: bool):
    s = static_legs(lane)
    if s is None:
        print("SETUP SKILL.md absent", file=sys.stderr)
        return 2, []
    lines: list[str] = []
    n_reg = len(s["rows"])
    n_led = len(s["ledger"]["rows"]) if s["ledger"] else 0
    lines.append(f"ROWS registry={n_reg} ledger={n_led} missing={len(s['missing'])} extra={len(s['extra'])} "
                 f"entry_mismatch={len(s['entry_mismatch'])} bad_decl={len(s['bad_decl'])} "
                 f"bad_reason={len(s['bad_reason'])} duplicate_names={len(s['dups'])}")
    for k, lab in (("missing", "MISSING"), ("extra", "EXTRA"), ("entry_mismatch", "ENTRY-MISMATCH"),
                   ("bad_decl", "BAD-DECL"), ("bad_reason", "BAD-REASON")):
        for n in s[k]:
            lines.append(f"  {lab} {n}")
    for n in s["dups"]:
        lines.append(f"  DUPLICATE {n}")
    if s["ledger_err"]:
        lines.append(f"  LEDGER {s['ledger_err']}")
    kinds = {"entry": 0, "selftest": 0, "help": 0}
    if s["ledger"]:
        for n in set(s["rows"]) & set(s["ledger"]["rows"]):
            k = s["ledger"]["rows"][n].get("kind")
            if k in kinds:
                kinds[k] += 1
    help_ok = kinds["help"] <= MAX_HELP_FRACTION * max(1, n_reg)
    lines.append(f"ARGV entry={kinds['entry']} selftest={kinds['selftest']} help={kinds['help']} "
                 f"help_limit={MAX_HELP_FRACTION * max(1, n_reg):.1f}")
    static_ok = help_ok and not (s["missing"] or s["extra"] or s["entry_mismatch"] or s["bad_decl"] or s["bad_reason"]
                     or s["dups"] or s["ledger_err"])
    executed = mism = tmo = evmiss = 0
    obs_green = obs_red = 0
    clean = None
    if not dry and s["ledger"]:
        if source is None or work is None:
            print("SETUP --source and --work are required unless --dry", file=sys.stderr)
            return 2, []
        if (source / ".git").exists():
            st = subprocess.run(["git", "-C", str(source), "status", "--porcelain"], capture_output=True, text=True)
            rev = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True)
            clean = st.returncode == 0 and st.stdout.strip() == ""
            lines.append(f"SOURCE rev={rev.stdout.strip()} clean={'yes' if clean else 'no'}")
        work.mkdir(parents=True, exist_ok=True)
        names = [n for n in sorted(s["rows"]) if n in s["ledger"]["rows"] and n not in s["entry_mismatch"]
                 and n not in s["bad_decl"]]
        if only:
            names = [n for n in names if n in only]
        workers = [Worker(source, work, i) for i in range(max(1, jobs))]
        free = list(range(len(workers)))
        import threading
        lock = threading.Lock()

        def job(n):
            with lock:
                i = free.pop()
            try:
                return run_row(workers[i], n, s["ledger"]["rows"][n], timeout, work)
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
            if rc != sp["exit"]:
                mism += 1
                lines.append(f"  MISMATCH {r['name']} declared exit={sp['exit']} observed exit={rc} sec={r['sec']}")
                continue
            if sp["state"] == "red" and sp["evidence"] not in r["out"]:
                evmiss += 1
                lines.append(f"  EVIDENCE-MISSING {r['name']} fragment not in output")
        for w in workers:
            shutil.rmtree(w.dir.parent, ignore_errors=True)
        dg = sum(1 for n in names if s["ledger"]["rows"][n]["state"] == "green")
        dr = len(names) - dg
        lines.append(f"RUN executed={executed} timeout={tmo} mismatched={mism} evidence_missing={evmiss}")
        lines.append(f"TIPSTATE declared_green={dg} declared_red={dr} observed_green={obs_green} observed_red={obs_red}")
    ok = static_ok and (dry or (executed == n_reg and tmo == 0 and mism == 0 and evmiss == 0 and clean in (True, None)
                                and (only is None)))
    if dry:
        lines.append("DRY static legs only: no predicate")
        return (0 if static_ok else 1), lines
    lines.append(f"PREDICATE R53-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# --------------------------------------------------------------------------------------- selftest
def _mk_lane(root: Path, rows: dict[str, tuple[str, int, str | None]], ledger_over=None):
    """rows: name -> (script body, declared exit, evidence)."""
    (root / "plans").mkdir(parents=True)
    table = ["## Gate/probe registry", "", "| name | kind | entry | verdict map | self-test | pinned | scope | owner |", "|---|---|---|---|---|---|---|---|"]
    ledger = {"schema": SCHEMA, "base": "selftest", "rows": {}}
    for n, (body, ex, ev) in rows.items():
        (root / "plans" / f"{n}.py").write_text(body)
        table.append(f"| `{n}` | gate | `python3 plans/{n}.py` | `0` ok · `1` bad | none | none | none | kengaku |")
        e = {"argv": ["python3", f"plans/{n}.py"], "exit": ex, "state": "green" if ex == 0 else "red", "kind": "entry"}
        if ex != 0:
            e["evidence"] = ev
            e["reason"] = "the selftest fixture exits non-zero on purpose so the red declaration has a real observed cause"
        ledger["rows"][n] = e
    (root / "SKILL.md").write_text("\n".join(table) + "\n")
    if ledger_over:
        ledger_over(ledger)
    (root / LEDGER).write_text(json.dumps(ledger))


def selftest() -> int:
    base = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    top = Path(tempfile.mkdtemp(prefix="r53c2-st-", dir=base))
    fails = []
    green = ("import sys\nprint('ok')\nsys.exit(0)\n", 0, None)
    red = ("import sys\nprint('DEFECT x')\nsys.exit(1)\n", 1, "DEFECT x")

    def case(label, rows, over=None, want_rc=0, want_in=(), want_out=(), dry=False, only=None):
        d = top / label
        lane = d / "lane"
        lane.mkdir(parents=True)
        _mk_lane(lane, rows, over)
        rc, lines = evaluate(lane, lane, d / "work", 2, 20, only, dry)
        text = "\n".join(lines)
        ok = rc == want_rc and all(w in text for w in want_in) and all(w not in text for w in want_out)
        print(f"SELFTEST {label} rc={rc} {'ok' if ok else 'FAIL'}")
        if not ok:
            fails.append(label)
            print(text)

    two = {"a": green, "b": red}
    case("truthful", two, want_rc=0, want_in=("PREDICATE R53-C2 pass", "declared_green=1 declared_red=1 observed_green=1 observed_red=1"))

    def all_green(l):  # forged: declare every row green
        for e in l["rows"].values():
            e["exit"], e["state"] = 0, "green"
            e.pop("evidence", None)
    case("forged-all-green", two, all_green, want_rc=1, want_in=("MISMATCH b declared exit=0 observed exit=1", "PREDICATE R53-C2 fail"))

    def all_red(l):  # forged: declare every row red with a plausible fragment
        for e in l["rows"].values():
            e["exit"], e["state"] = 1, "red"
            e["evidence"] = "DEFECT x"
            e["reason"] = "a forged declaration that claims every instrument is red without having observed its output"
    case("forged-all-red", two, all_red, want_rc=1, want_in=("MISMATCH a declared exit=1 observed exit=0",))

    def drop(l):
        del l["rows"]["b"]
    case("missing-ledger-row", two, drop, want_rc=1, want_in=("MISSING b",))

    def extra(l):
        l["rows"]["ghost"] = dict(l["rows"]["a"])
    case("extra-ledger-row", two, extra, want_rc=1, want_in=("EXTRA ghost",))

    def wrong_script(l):
        l["rows"]["a"]["argv"] = ["python3", "plans/b.py"]  # script of another row, not this row's entry
    case("ledger-points-elsewhere", two, wrong_script, want_rc=1, want_in=("ENTRY-MISMATCH a",))

    def bad_ev(l):
        l["rows"]["b"]["evidence"] = "text the output never prints"
    case("red-evidence-absent", two, bad_ev, want_rc=1, want_in=("EVIDENCE-MISSING b",))

    def thin(l):
        l["rows"]["b"]["reason"] = "broken"
    case("red-reason-thin", two, thin, want_rc=1, want_in=("BAD-REASON b",))

    def inconsistent(l):
        l["rows"]["a"]["state"] = "red"
    case("state-exit-inconsistent", two, inconsistent, want_rc=1, want_in=("BAD-DECL a",))

    hang = ("import time\ntime.sleep(60)\n", 0, None)

    def tight(l):
        l["rows"]["h"]["timeout_s"] = 2
    case("timeout", {"a": green, "h": hang}, tight, want_rc=1, want_in=("TIMEOUT h",))

    def helpy(l):
        for e in l["rows"].values():
            e["kind"] = "help"
    case("help-only-argv", two, helpy, want_rc=1, want_in=("ARGV entry=0 selftest=0 help=2",))

    case("partial-run-never-passes", two, want_rc=1, want_in=("PREDICATE R53-C2 fail",), only={"a"})
    shutil.rmtree(top, ignore_errors=True)
    print(f"SELFTEST cases=12 failures={len(fails)}")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--source")
    ap.add_argument("--work")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    lane = Path(a.lane).resolve()
    only = set(a.only.split(",")) if a.only else None
    rc, lines = evaluate(lane, Path(a.source).resolve() if a.source else None,
                         Path(a.work).resolve() if a.work else None, a.jobs, a.timeout, only, a.dry)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
