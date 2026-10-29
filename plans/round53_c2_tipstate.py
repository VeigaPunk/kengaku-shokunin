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
import hashlib
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

REGISTRY_HEADING = re.compile(r"(?m)^## Gate/probe registry(?: \([^\n]*\))?[ \t]*$")   # A1: line-anchored, exactly one
# A1 pins: the 75 registry names frozen at the claims commit (digest of the sorted names joined by newlines) plus the two
# rows this round adds; a deleted, renamed or extra row cannot pass.
FROZEN_NAMES_SHA = "df38a8fca5bc345cce62a8f8fcd31cd65dcb66b67270f4da7c8e6aaab4ddd0a4"
EXTRA_NAMES = frozenset({"round53-c1", "round53-c2", "stage-scan"})
SECRET_ENV = re.compile(r"(TOKEN|KEY|SECRET|PASSWORD|PASSWD|CREDENTIAL|^OP_|SSH_AUTH_SOCK|COOKIE)", re.I)
SHELLS = {"sh", "bash", "dash", "zsh", "env", "cat", "true", "-c"}
LEDGER = "plans/round53-tipstate.json"
SCHEMA = "r53-tipstate-v1"
NAME_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
SCRIPT = re.compile(r"python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)")
MIN_REASON_WORDS = 10
MAX_HELP_FRACTION = 0.10   # rows whose only runnable argv is --help (weak truth) may not exceed this share


def registry_block(text: str) -> tuple[str, int]:
    ms = list(REGISTRY_HEADING.finditer(text))
    if len(ms) != 1:
        return "", len(ms)
    i = ms[0].start()
    j = text.find("\n## ", ms[0].end())
    return (text[i:j] if j > 0 else text[i:]), 1


def registry_rows(skill_text: str):
    """(name -> row line, duplicate names, malformed table lines, heading count)."""
    block, nh = registry_block(skill_text)
    rows: dict[str, str] = {}
    dup: list[str] = []
    badname: list[str] = []
    for k, line in enumerate(block.splitlines()):
        if not line.startswith("|"):
            continue
        m = NAME_ROW.match(line)
        if not m:
            first = line.strip().strip("|").split("|")[0].strip()
            if k > 2 and not set(first) <= set("-: "):
                badname.append(first[:40])
            continue
        n = m.group(1)
        if n in rows:
            dup.append(n)
        rows[n] = line
    return rows, dup, badname, nh


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
        def no_dup(pairs):
            keys = [k for k, _ in pairs]
            if len(keys) != len(set(keys)):
                raise ValueError("duplicate JSON key")
            return dict(pairs)
        d = json.loads(p.read_text(), object_pairs_hook=no_dup)
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
        """A1: a failed reset is an error, never a silent contamination of the next row."""
        if self.git:
            subprocess.run(["git", "-C", str(self.dir), "clean", "-q", "-fdx"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(self.dir), "reset", "-q", "--hard"], check=True, capture_output=True)


def run_row(w: Worker, name: str, spec: dict, default_timeout: int, tmp_root: Path) -> dict:
    argv = spec.get("argv")
    t = int(spec.get("timeout_s") or default_timeout)
    tmp = tmp_root / f"tmp-{re.sub(r'[^A-Za-z0-9_.-]', '_', name)}"
    tmp.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not SECRET_ENV.search(k)}   # A1: no credentials reach a row or the ledger
    env["TMPDIR"] = str(tmp)
    t0 = time.time()
    try:
        w.reset()
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


def argv_ok(argv, script) -> bool:
    """A1: python3 <script> ... or uv run ... python3 <script> ...; no shells, no -c, the script is the interpreter's argument."""
    if not isinstance(argv, list) or len(argv) < 2 or not all(isinstance(a, str) for a in argv) or script is None:
        return False
    if any(a in SHELLS for a in argv):
        return False
    if argv[0] == "python3":
        return argv[1] == script
    if argv[0] == "uv":
        return any(argv[i] == "python3" and argv[i + 1] == script for i in range(len(argv) - 1))
    return False


def kind_ok(argv, kind) -> bool:
    k = "help" if "--help" in argv else "selftest" if "--selftest" in argv else "entry"
    return kind == k


def static_legs(root: Path, pins: bool = True):
    skill = root / "SKILL.md"
    if not skill.is_file():
        return None
    rows, dups, badname, nh = registry_rows(skill.read_text())
    ledger, err = load_ledger(root)
    res = {"rows": rows, "dups": dups, "badname": badname, "headings": nh, "ledger": ledger, "ledger_err": err,
           "missing": [], "extra": [], "entry_mismatch": [], "bad_decl": [], "bad_reason": [], "pinset": True}
    if pins:
        core = sorted(set(rows) - EXTRA_NAMES)
        res["pinset"] = (EXTRA_NAMES <= set(rows) and hashlib.sha256("\n".join(core).encode()).hexdigest() == FROZEN_NAMES_SHA)
    if ledger is None:
        res["missing"] = sorted(rows)
        return res
    lr = ledger["rows"]
    res["missing"] = sorted(set(rows) - set(lr))
    res["extra"] = sorted(set(lr) - set(rows))
    for n in sorted(set(rows) & set(lr)):
        sp = lr[n]
        if not isinstance(sp, dict):
            res["bad_decl"].append(n)
            continue
        argv = sp.get("argv")
        script = row_script(rows[n])
        if not argv_ok(argv, script):
            res["entry_mismatch"].append(n)
            continue
        ex, st = sp.get("exit"), sp.get("state")
        if (not isinstance(ex, int) or isinstance(ex, bool) or st not in ("green", "red") or (st == "green") != (ex == 0)
                or sp.get("kind") not in ("entry", "selftest", "help") or not kind_ok(argv, sp.get("kind"))):
            res["bad_decl"].append(n)
            continue
        if st == "red":
            reason = sp.get("reason")
            ev = sp.get("evidence")
            if (not isinstance(reason, str) or len(reason.split()) < MIN_REASON_WORDS
                    or not isinstance(ev, str) or len(ev.strip()) < 6):
                res["bad_reason"].append(n)
    return res


def _keep(work: Path, r: dict) -> None:
    """Diagnostic only (no leg): keep the output of a row that disagreed so the cause can be read without a rerun."""
    (work / f"disagreed-{re.sub(r'[^A-Za-z0-9_.-]', '_', r['name'])}.txt").write_text(f"exit={r['rc']} sec={r['sec']}\n{r['out']}")


def git_rev(d: Path):
    p = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def evaluate(lane: Path, source: Path | None, work: Path | None, jobs: int, timeout: int, only: set[str] | None,
             dry: bool, pins: bool = True):
    root = source if source is not None else lane          # A1: registry and ledger are read from the clean tree under test
    s = static_legs(root, pins)
    if s is None:
        print("SETUP SKILL.md absent", file=sys.stderr)
        return 2, []
    lines: list[str] = []
    n_reg = len(s["rows"])
    n_led = len(s["ledger"]["rows"]) if s["ledger"] else 0
    lines.append(f"ROWS registry={n_reg} ledger={n_led} missing={len(s['missing'])} extra={len(s['extra'])} "
                 f"entry_mismatch={len(s['entry_mismatch'])} bad_decl={len(s['bad_decl'])} "
                 f"bad_reason={len(s['bad_reason'])} duplicate_names={len(s['dups'])} bad_table_lines={len(s['badname'])} "
                 f"headings={s['headings']} row_set_pinned={'ok' if s['pinset'] else 'BAD'}")
    for k, lab in (("missing", "MISSING"), ("extra", "EXTRA"), ("entry_mismatch", "ENTRY-MISMATCH"),
                   ("bad_decl", "BAD-DECL"), ("bad_reason", "BAD-REASON"), ("badname", "BAD-NAME")):
        for n in s[k]:
            lines.append(f"  {lab} {n}")
    for n in s["dups"]:
        lines.append(f"  DUPLICATE {n}")
    if s["ledger_err"]:
        lines.append(f"  LEDGER {s['ledger_err']}")
    kinds = {"entry": 0, "selftest": 0, "help": 0}
    if s["ledger"]:
        for n in set(s["rows"]) & set(s["ledger"]["rows"]):
            sp = s["ledger"]["rows"][n]
            k = sp.get("kind") if isinstance(sp, dict) else None
            if k in kinds:
                kinds[k] += 1
    help_ok = kinds["help"] <= MAX_HELP_FRACTION * max(1, n_reg)
    lines.append(f"ARGV entry={kinds['entry']} selftest={kinds['selftest']} help={kinds['help']} "
                 f"help_limit={MAX_HELP_FRACTION * max(1, n_reg):.1f}")
    static_ok = (n_reg > 0 and s["headings"] == 1 and s["pinset"] and help_ok
                 and not (s["missing"] or s["extra"] or s["entry_mismatch"] or s["bad_decl"] or s["bad_reason"]
                          or s["dups"] or s["badname"] or s["ledger_err"]))
    executed = mism = tmo = evmiss = 0
    obs_green = obs_red = 0
    clean = False
    rev_ok = False
    if not dry and s["ledger"]:
        if source is None or work is None:
            print("SETUP --source and --work are required unless --dry", file=sys.stderr)
            return 2, []
        if (source / ".git").exists():
            st = subprocess.run(["git", "-C", str(source), "status", "--porcelain"], capture_output=True, text=True)
            clean = st.returncode == 0 and st.stdout.strip() == ""
            sr = git_rev(source)
            lr = git_rev(lane) if (lane / ".git").exists() else None
            rev_ok = sr is not None and (lr is None or lr == sr)
            lines.append(f"SOURCE rev={sr} clean={'yes' if clean else 'NO'} lane_rev_equal={'yes' if rev_ok else 'NO'}")
        else:
            lines.append("SOURCE not a git work tree clean=NO")
        work.mkdir(parents=True, exist_ok=True)
        names = [n for n in sorted(s["rows"]) if n in s["ledger"]["rows"] and n not in s["entry_mismatch"]
                 and n not in s["bad_decl"] and n not in s["bad_reason"]]
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
                _keep(work, r)
                continue
            if sp["state"] == "red" and sp["evidence"] not in r["out"]:
                evmiss += 1
                lines.append(f"  EVIDENCE-MISSING {r['name']} fragment not in output")
                _keep(work, r)
        for w in workers:
            shutil.rmtree(w.dir.parent, ignore_errors=True)
        dg = sum(1 for n in names if s["ledger"]["rows"][n]["state"] == "green")
        dr = len(names) - dg
        lines.append(f"RUN executed={executed} timeout={tmo} mismatched={mism} evidence_missing={evmiss}")
        lines.append(f"TIPSTATE declared_green={dg} declared_red={dr} observed_green={obs_green} observed_red={obs_red}")
    if dry:
        lines.append("DRY static legs only: no predicate")
        return (0 if static_ok else 1), lines
    ok = static_ok and executed == n_reg and tmo == 0 and mism == 0 and evmiss == 0 and clean and rev_ok and only is None
    lines.append(f"PREDICATE R53-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# --------------------------------------------------------------------------------------- selftest
HEAD_ROW = ["## Gate/probe registry", "", "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]


def _row(n, entry):
    return f"| `{n}` | gate | `{entry}` | `0` ok · `1` bad | none | none | none | kengaku |"


def _git(d: Path, *a):
    subprocess.run(["git", "-C", str(d), *a], check=True, capture_output=True)


def _commit_all(d: Path, msg="fixture"):
    if not (d / ".git").exists():
        _git(d, "init", "-q")
        _git(d, "config", "user.email", "t@t.invalid")
        _git(d, "config", "user.name", "selftest")
    _git(d, "add", "-A")
    _git(d, "commit", "-q", "--allow-empty", "-m", msg)


def _mk_lane(root: Path, rows: dict[str, tuple[str, int, str | None]], ledger_over=None, skill_over=None, git=True):
    """rows: name -> (script body, declared exit, evidence)."""
    (root / "plans").mkdir(parents=True, exist_ok=True)
    table = list(HEAD_ROW)
    ledger = {"schema": SCHEMA, "base": "selftest", "rows": {}}
    for n, (body, ex, ev) in rows.items():
        (root / "plans" / f"{n}.py").write_text(body)
        table.append(_row(n, f"python3 plans/{n}.py"))
        e = {"argv": ["python3", f"plans/{n}.py"], "exit": ex, "state": "green" if ex == 0 else "red", "kind": "entry"}
        if ex != 0:
            e["evidence"] = ev
            e["reason"] = "the selftest fixture exits non-zero on purpose so the red declaration has a real observed cause"
        ledger["rows"][n] = e
    skill = "\n".join(table) + "\n"
    if skill_over:
        skill = skill_over(skill)
    (root / "SKILL.md").write_text(skill)
    if ledger_over:
        ledger_over(ledger)
    (root / LEDGER).write_text(json.dumps(ledger))
    if git:
        _commit_all(root)


def selftest() -> int:
    base = Path(os.environ.get("TMPDIR") or tempfile.gettempdir())
    top = Path(tempfile.mkdtemp(prefix="r53c2-st-", dir=base))
    fails: list[str] = []
    ncase = [0]
    green = ("import sys\nprint('ok')\nsys.exit(0)\n", 0, None)
    red = ("import sys\nprint('DEFECT x')\nsys.exit(1)\n", 1, "DEFECT x")
    TEN = "one two three four five six seven eight nine ten"
    NINE = "one two three four five six seven eight nine"

    def check(label, rc, lines, want_rc, want_in, want_out):
        ncase[0] += 1
        text = "\n".join(lines)
        ok = rc == want_rc and all(w in text for w in want_in) and all(w not in text for w in want_out)
        print(f"SELFTEST {label} rc={rc} {'ok' if ok else 'FAIL'}")
        if not ok:
            fails.append(label)
            print(text)

    def case(label, rows, over=None, want_rc=0, want_in=(), want_out=(), dry=False, only=None, skill_over=None, git=True,
             pins=False, after=None, source_git=True, jobs=2, timeout=20):
        d = top / label
        lane = d / "lane"
        lane.mkdir(parents=True)
        _mk_lane(lane, rows, over, skill_over, git)
        if after:
            after(lane)
        rc, lines = evaluate(lane, lane, d / "work", jobs, timeout, only, dry, pins)
        check(label, rc, lines, want_rc, want_in, want_out)

    def set_(name, key, val):
        def f(l):
            l["rows"][name][key] = val
        return f

    two = {"a": green, "b": red}
    case("truthful", two, want_rc=0, want_in=("PREDICATE R53-C2 pass", "declared_green=1 declared_red=1 observed_green=1 observed_red=1",
                                              "clean=yes lane_rev_equal=yes"))

    def all_green(l):
        for e in l["rows"].values():
            e["exit"], e["state"] = 0, "green"
            e.pop("evidence", None)
    case("forged-all-green", two, all_green, want_rc=1, want_in=("MISMATCH b declared exit=0 observed exit=1", "PREDICATE R53-C2 fail"))

    def all_red(l):
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
        l["rows"]["a"]["argv"] = ["python3", "plans/b.py"]
    case("ledger-points-elsewhere", two, wrong_script, want_rc=1, want_in=("ENTRY-MISMATCH a",))
    case("red-evidence-absent", two, set_("b", "evidence", "text the output never prints"), want_rc=1, want_in=("EVIDENCE-MISSING b",))
    case("red-reason-thin", two, set_("b", "reason", "broken"), want_rc=1, want_in=("BAD-REASON b",))
    case("state-exit-inconsistent", two, set_("a", "state", "red"), want_rc=1, want_in=("BAD-DECL a",))
    hang = ("import time\ntime.sleep(60)\n", 0, None)
    case("timeout", {"a": green, "h": hang}, set_("h", "timeout_s", 2), want_rc=1, want_in=("TIMEOUT h",))

    def helpy(l):
        for e in l["rows"].values():
            e["kind"] = "help"
            e["argv"] = e["argv"] + ["--help"]
    case("help-only-argv", two, helpy, want_rc=1, want_in=("ARGV entry=0 selftest=0 help=2",))
    case("partial-run-never-passes", two, want_rc=1, want_in=("PREDICATE R53-C2 fail",), only={"a"})
    # ---- A1: routes found by wave-1 attacks (C2CritLedgerReach) and survivors (C2MutCounter) --------------------------
    case("zero-rows-no-heading", {}, skill_over=lambda t: "no registry here\n", want_rc=1, want_in=("registry=0",))
    case("heading-in-prose-above-table", two, skill_over=lambda t: "Note: see `## Gate/probe registry` below.\n\n" + t,
         want_rc=0, want_in=("headings=1", "PREDICATE R53-C2 pass"))
    case("heading-twice", two, skill_over=lambda t: t + "\n## Gate/probe registry\n\n" + "\n".join(HEAD_ROW[2:]) + "\n",
         want_rc=1, want_in=("headings=2",))
    case("heading-renamed", two, skill_over=lambda t: t.replace("## Gate/probe registry", "## Registry"), want_rc=1, want_in=("registry=0", "headings=0"))
    case("row-name-without-backticks", two, skill_over=lambda t: t + "| c | gate | python3 plans/c.py | x | x | x | x | x |\n",
         want_rc=1, want_in=("BAD-NAME c",))
    case("row-named-dups-marker", {"__dups__": red, "a": green}, want_rc=1, want_in=("MISMATCH",), want_out=("PREDICATE R53-C2 pass",),
         over=lambda l: l["rows"]["__dups__"].update(exit=0, state="green"))
    case("dead-argument-python-c-pass", two, set_("a", "argv", ["python3", "-c", "pass", "plans/a.py"]), want_rc=1, want_in=("ENTRY-MISMATCH a",))
    case("cat-as-the-gate", two, set_("a", "argv", ["cat", "plans/a.py"]), want_rc=1, want_in=("ENTRY-MISMATCH a",))

    def sh_wrap(l):
        l["rows"]["b"]["argv"] = ["sh", "-c", "python3 plans/b.py; exit 0", "plans/b.py"]
        l["rows"]["b"].update(exit=0, state="green")
        l["rows"]["b"].pop("evidence", None)
    case("shell-wrapper-swallows-exit", two, sh_wrap, want_rc=1, want_in=("ENTRY-MISMATCH b",))

    def help_as_entry(l):
        l["rows"]["b"]["argv"] = ["python3", "plans/b.py", "--help"]
    case("help-relabelled-entry", two, help_as_entry, want_rc=1, want_in=("BAD-DECL b",))
    case("uv-run-entry", two, set_("a", "argv", ["uv", "run", "--no-project", "python3", "plans/a.py"]), want_rc=0,
         want_in=("PREDICATE R53-C2 pass",))
    case("argv-one-element", two, set_("a", "argv", ["plans/a.py"]), want_rc=1, want_in=("ENTRY-MISMATCH a",))
    case("argv-nonstring-element", two, set_("a", "argv", ["python3", "plans/a.py", 7]), want_rc=1, want_in=("ENTRY-MISMATCH a",))
    case("exit-is-bool", two, set_("b", "exit", True), want_rc=1, want_in=("BAD-DECL b",))
    case("state-outside-domain", two, set_("b", "state", "amber"), want_rc=1, want_in=("BAD-DECL b",))
    case("kind-outside-domain", two, set_("a", "kind", "bogus"), want_rc=1, want_in=("BAD-DECL a",))
    case("reason-exactly-10-words", two, set_("b", "reason", TEN), want_rc=0, want_in=("PREDICATE R53-C2 pass",))
    case("reason-9-words", two, set_("b", "reason", NINE), want_rc=1, want_in=("BAD-REASON b",))
    case("evidence-null", two, set_("b", "evidence", None), want_rc=1, want_in=("BAD-REASON b",), want_out=("Traceback",))
    case("evidence-5-chars", two, set_("b", "evidence", "DEFEC"), want_rc=1, want_in=("BAD-REASON b",))
    case("evidence-padded-short", two, set_("b", "evidence", "   ab   "), want_rc=1, want_in=("BAD-REASON b",))
    case("help-at-exact-limit", {n: green for n in "abcdefghij"},
         lambda l: (l["rows"]["a"].update(kind="help", argv=["python3", "plans/a.py", "--help"])), want_rc=0, want_in=("PREDICATE R53-C2 pass",))
    case("help-fraction-quarter", {n: green for n in "abcd"},
         lambda l: (l["rows"]["d"].update(kind="help", argv=["python3", "plans/d.py", "--help"])), want_rc=1, want_in=("help=1 help_limit=0.4",))
    case("ledger-schema-foreign", two, lambda l: l.update(schema="r53-tipstate-v0"), want_rc=1, want_in=("ledger schema mismatch",))
    case("dry-truthful", two, want_rc=0, want_in=("DRY static legs only",), dry=True)
    case("dry-missing-row", two, drop, want_rc=1, want_in=("MISSING b",), dry=True)
    case("dry-entry-mismatch", two, wrong_script, want_rc=1, want_in=("ENTRY-MISMATCH a",), dry=True)

    # ---- A1: environment scrub and reset failure (C1SentinelScreen M2/M3) --------------------------------------------
    leak = ("import os,sys\nprint('TOKENSEEN' if os.environ.get('R53C2_FAKE_TOKEN') else 'scrubbed')\nsys.exit(0)\n", 0, None)
    os.environ["R53C2_FAKE_TOKEN"] = "fixture-not-a-secret"
    case("env-scrubbed-for-rows", {"a": leak}, set_("a", "kind", "entry"), want_rc=0, want_in=("PREDICATE R53-C2 pass",))
    d = top / "env-scrub-visible"
    lane = d / "lane"
    lane.mkdir(parents=True)
    _mk_lane(lane, {"a": ("import os,sys\nsys.exit(0 if os.environ.get('R53C2_FAKE_TOKEN') is None else 1)\n", 0, None)})
    rc, lines = evaluate(lane, lane, d / "work", 1, 20, None, False, False)
    check("env-token-not-visible-to-row", rc, lines, 0, ("observed_green=1",), ())
    os.environ.pop("R53C2_FAKE_TOKEN", None)

    # ledger with a duplicate JSON key
    d = top / "dup-json-key"
    lane = d / "lane"
    lane.mkdir(parents=True)
    _mk_lane(lane, two, git=False)
    txt = (lane / LEDGER).read_text()
    (lane / LEDGER).write_text(txt.replace('"a": {', '"a": {"argv": [], "x": 1}, "a": {', 1))
    _commit_all(lane)
    rc, lines = evaluate(lane, lane, d / "work", 2, 20, None, False, False)
    check("ledger-duplicate-json-key", rc, lines, 1, ("ledger unreadable",), ())

    # source not a git work tree, dirty source, older source than the lane, lane-vs-source registry
    d = top / "non-git-source"
    lane = d / "lane"
    lane.mkdir(parents=True)
    _mk_lane(lane, two, git=False)
    rc, lines = evaluate(lane, lane, d / "work", 2, 20, None, False, False)
    check("source-not-a-git-tree", rc, lines, 1, ("clean=NO",), ("PREDICATE R53-C2 pass",))
    d = top / "dirty-source"
    lane = d / "lane"
    lane.mkdir(parents=True)
    _mk_lane(lane, two)
    (lane / "plans" / "helper.py").write_text("x = 1\n")
    rc, lines = evaluate(lane, lane, d / "work", 2, 20, None, False, False)
    check("dirty-source-tree", rc, lines, 1, ("clean=NO",), ("PREDICATE R53-C2 pass",))
    d = top / "older-source"
    lane = d / "lane"
    lane.mkdir(parents=True)
    _mk_lane(lane, {"a": green, "b": green}, set_("b", "kind", "entry"))
    old = d / "old"
    subprocess.run(["git", "clone", "-q", "--shared", str(lane), str(old)], check=True)
    (lane / "plans" / "b.py").write_text(red[0])
    _commit_all(lane, "b turns red at the tip")
    rc, lines = evaluate(lane, old, d / "work", 2, 20, None, False, False)
    check("source-older-than-lane", rc, lines, 1, ("lane_rev_equal=NO",), ("PREDICATE R53-C2 pass",))
    # pins: deletion, rename and extra row against a fixture digest
    global FROZEN_NAMES_SHA, EXTRA_NAMES
    saved = (FROZEN_NAMES_SHA, EXTRA_NAMES)
    FROZEN_NAMES_SHA = hashlib.sha256("\n".join(["a", "b"]).encode()).hexdigest()
    EXTRA_NAMES = frozenset({"x1"})
    three = {"a": green, "b": red, "x1": green}
    case("pinned-row-set-honest", three, pins=True, want_rc=0, want_in=("row_set_pinned=ok", "PREDICATE R53-C2 pass"))
    case("pinned-row-set-deletion", {"a": green, "x1": green}, pins=True, want_rc=1, want_in=("row_set_pinned=BAD",))
    case("pinned-row-set-extra-row", {"a": green, "b": red, "x1": green, "c": green}, pins=True, want_rc=1, want_in=("row_set_pinned=BAD",))
    case("pinned-extra-name-missing", two, pins=True, want_rc=1, want_in=("row_set_pinned=BAD",))
    FROZEN_NAMES_SHA, EXTRA_NAMES = saved
    # the frozen constants the real run uses
    ncase[0] += 1
    ok = (FROZEN_NAMES_SHA == "df38a8fca5bc345cce62a8f8fcd31cd65dcb66b67270f4da7c8e6aaab4ddd0a4"
          and EXTRA_NAMES == {"round53-c1", "round53-c2", "stage-scan"} and MIN_REASON_WORDS == 10 and MAX_HELP_FRACTION == 0.10)
    print(f"SELFTEST frozen-constants {'ok' if ok else 'FAIL'}")
    if not ok:
        fails.append("frozen-constants")
    shutil.rmtree(top, ignore_errors=True)
    print(f"SELFTEST cases={ncase[0]} failures={len(fails)}")
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
                         Path(a.work).resolve() if a.work else None, a.jobs, a.timeout, only, a.dry, True)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
