#!/usr/bin/env python3
"""Round 54, claim C2: registry tip-state truth at the ENTRY argv, hermetically executed.

Q42/Q43 follow-up to the round-53 verifier spot-check (``corpus/lessons/round-53-verifier-spotcheck.md``
item 2 and ``.ufo/waves/round-53/w3/C2CritPredicate2.md``): a ledger row may not launder a failing
entry mode behind a green ``--selftest``/``--help`` argv, and a worker must not inherit the caller's
git configuration.  Every row of SKILL.md's *## Gate/probe registry* gets one entry in the committed
ledger ``plans/round54-entrytruth.json`` (schema ``r54-entrytruth-v1``) that declares the ENTRY argv
(no ``--selftest``/``--help``/``--dry``/``--version``/``-h`` in it), the exit code it returns on a
clean checkout, and — when red — a reason and a verbatim output fragment.  This counter re-executes
every entry argv in a scratch copy of ``--source`` under a hermetic git environment and compares.

Hermetic env: all ``GIT_*`` variables scrubbed, then ``GIT_CONFIG_GLOBAL`` pointed at a counter-owned
empty file, ``GIT_CONFIG_SYSTEM=/dev/null``, ``GIT_CONFIG_NOSYSTEM=1``, scratch ``HOME`` and
``XDG_CONFIG_HOME``, secrets scrubbed.  The frozen round-53 counter and its ledger
(``plans/round53_c2_tipstate.py``, ``plans/round53-tipstate.json``) are never read as truth and never
edited; the MIGRATION leg only counts r53 rows that declared green with ``kind != entry`` whose
entry-mode exit is nonzero — they are re-declared truthfully here.

Exit codes: 0 predicate holds · 1 predicate fails · 2 setup/usage.
Usage:
    python3 plans/round54_c2_entrytruth.py --lane . --source CLEAN_CLONE --work SCRATCH \
        [--jobs 3] [--timeout 900]
    python3 plans/round54_c2_entrytruth.py --lane . --dry
    python3 plans/round54_c2_entrytruth.py --selftest
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

REGISTRY_HEADING = re.compile(r"(?m)^## Gate/probe registry(?: \([^\n]*\))?[ \t]*$")
NAME_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
SCRIPT = re.compile(r"python3\s+((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py|grader\.py)")
LEDGER = "plans/round54-entrytruth.json"
SCHEMA = "r54-entrytruth-v1"
R53_LEDGER = "plans/round53-tipstate.json"
MIN_REASON_WORDS = 10
FORBIDDEN_ARGV_TOKENS = {"--selftest", "--help", "-h", "--dry", "--version"}
SECRET_ENV = re.compile(r"(TOKEN|KEY|SECRET|PASSWORD|PASSWD|CREDENTIAL|^OP_|SSH_AUTH_SOCK|COOKIE)", re.I)
SHELLS = {"sh", "bash", "dash", "zsh", "env", "cat", "true", "-c"}


def registry_block(text: str) -> tuple[str, int]:
    ms = list(REGISTRY_HEADING.finditer(text))
    if len(ms) != 1:
        return "", len(ms)
    i = ms[0].start()
    j = text.find("\n## ", ms[0].end())
    return (text[i:j] if j > 0 else text[i:]), 1


def registry_rows(skill_text: str):
    rows: dict[str, str] = {}
    dup: list[str] = []
    badname: list[str] = []
    block, nh = registry_block(skill_text)
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

    def no_dup(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate JSON key")
        return dict(pairs)

    try:
        d = json.loads(p.read_text(), object_pairs_hook=no_dup)
    except Exception as e:  # noqa: BLE001
        return None, f"ledger unreadable: {e}"
    if d.get("schema") != SCHEMA or not isinstance(d.get("rows"), dict):
        return None, "ledger schema mismatch"
    return d, ""


def load_r53_green_nonentry(lane: Path) -> dict[str, str]:
    """r53 rows declared green with kind != entry (migration comparison only; never truth)."""
    p = lane / R53_LEDGER
    if not p.is_file():
        return {}
    try:
        d = json.loads(p.read_text())
    except Exception:
        return {}
    out = {}
    for name, spec in (d.get("rows") or {}).items():
        if isinstance(spec, dict) and spec.get("state") == "green" and spec.get("kind") in ("selftest", "help"):
            out[name] = spec.get("kind", "?")
    return out


def hermetic_env(tmp: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not SECRET_ENV.search(k)}
    for k in list(env):
        if k.startswith("GIT_"):
            del env[k]
    home = tmp / "home"
    (home / ".config").mkdir(parents=True, exist_ok=True)
    (tmp / "empty-gitconfig").write_text("")   # counter-owned empty global config
    env["HOME"] = str(home)
    env["XDG_CONFIG_HOME"] = str(home / ".config")
    env["GIT_CONFIG_GLOBAL"] = str(tmp / "empty-gitconfig")
    env["GIT_CONFIG_SYSTEM"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.pop("GIT_CONFIG_COUNT", None)
    return env


def entry_mode_ok(argv, script) -> str | None:
    """None when argv is a legal entry invocation of script; a defect string otherwise."""
    if not isinstance(argv, list) or len(argv) < 2 or not all(isinstance(a, str) for a in argv) or script is None:
        return "argv shape"
    if any(a in SHELLS for a in argv):
        return "shell wrapper"
    low = [a for a in argv[1:] if a.startswith("-")]
    for a in low:
        if a in FORBIDDEN_ARGV_TOKENS:
            return f"non-entry flag {a}"
    if argv[0] == "python3":
        if argv[1] != script:
            return "script mismatch"
        return None
    if argv[0] == "uv":
        for i in range(len(argv) - 1):
            if argv[i] == "python3" and argv[i + 1] == script:
                return None
        return "script mismatch"
    return "interpreter not python3/uv"


class Worker:
    def __init__(self, source: Path, root: Path, idx: int):
        self.dir = root / f"w{idx}" / "src"
        self.dir.parent.mkdir(parents=True, exist_ok=True)
        if (source / ".git").exists():
            subprocess.run(["git", "clone", "-q", "--shared", str(source), str(self.dir)], check=True)
            self.git = True
            self.base = subprocess.run(["git", "-C", str(self.dir), "rev-parse", "HEAD"], capture_output=True,
                                       text=True, check=True).stdout.strip()
        else:
            shutil.copytree(source, self.dir)
            self.git = False

    def reset(self):
        if self.git:
            subprocess.run(["git", "-C", str(self.dir), "reset", "-q", "--hard", self.base], check=True,
                           capture_output=True)
            subprocess.run(["git", "-C", str(self.dir), "clean", "-q", "-ffdx"], check=True, capture_output=True)


def run_row(w: Worker, name: str, spec: dict, default_timeout: int, tmp_root: Path) -> dict:
    argv = spec.get("entry_argv")
    t = min(int(spec.get("timeout_s") or default_timeout), default_timeout)
    tmp = tmp_root / f"tmp-{re.sub(r'[^A-Za-z0-9_.-]', '_', name)}"
    tmp.mkdir(parents=True, exist_ok=True)
    env = hermetic_env(tmp)
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


def static_legs(root: Path):
    skill = root / "SKILL.md"
    if not skill.is_file():
        return None
    rows, dups, badname, nh = registry_rows(skill.read_text())
    ledger, err = load_ledger(root)
    res = {"rows": rows, "dups": dups, "badname": badname, "headings": nh, "ledger": ledger, "ledger_err": err,
           "missing": [], "extra": [], "argv_defect": [], "bad_decl": []}
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
        script = row_script(rows[n])
        defect = entry_mode_ok(sp.get("entry_argv"), script)
        if defect:
            res["argv_defect"].append(f"{n}: {defect}")
            continue
        ex, st = sp.get("entry_exit"), sp.get("entry_state")
        if (not isinstance(ex, int) or isinstance(ex, bool) or st not in ("green", "red") or (st == "green") != (ex == 0)):
            res["bad_decl"].append(n)
            continue
        if st == "red":
            reason, ev = sp.get("reason"), sp.get("evidence")
            if (not isinstance(reason, str) or len(reason.split()) < MIN_REASON_WORDS
                    or not isinstance(ev, str) or len(ev.strip()) < 6):
                res["bad_decl"].append(n)
    return res


def _keep(work: Path, r: dict) -> None:
    (work / f"disagreed-{re.sub(r'[^A-Za-z0-9_.-]', '_', r['name'])}.txt").write_text(
        f"exit={r['rc']} sec={r['sec']}\n{r['out']}")


def git_rev(d: Path):
    p = subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def evaluate(lane: Path, source: Path | None, work: Path | None, jobs: int, timeout: int,
             dry: bool):
    root = source if source is not None else lane
    s = static_legs(root)
    if s is None:
        print("SETUP SKILL.md absent", file=sys.stderr)
        return 2, []
    lines: list[str] = []
    n_reg = len(s["rows"])
    n_led = len(s["ledger"]["rows"]) if s["ledger"] else 0
    lines.append(f"ROWS registry={n_reg} ledger={n_led} missing={len(s['missing'])} extra={len(s['extra'])} "
                 f"argv_defect={len(s['argv_defect'])} bad_decl={len(s['bad_decl'])} "
                 f"duplicate_names={len(s['dups'])} bad_table_lines={len(s['badname'])} headings={s['headings']}")
    for k, lab in (("missing", "MISSING"), ("extra", "EXTRA"), ("bad_decl", "BAD-DECL")):
        for n in s[k]:
            lines.append(f"  {lab} {n}")
    for d in s["argv_defect"]:
        lines.append(f"  ARGV-DEFECT {d}")
    for n in s["dups"]:
        lines.append(f"  DUPLICATE {n}")
    if s["ledger_err"]:
        lines.append(f"  LEDGER {s['ledger_err']}")
    static_ok = (n_reg > 0 and s["headings"] == 1 and not s["ledger_err"]
                 and not (s["missing"] or s["extra"] or s["argv_defect"] or s["bad_decl"] or s["dups"] or s["badname"]))
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
            sr = git_rev(source)
            lr_ = git_rev(lane) if (lane / ".git").exists() else None
            rev_ok = sr is not None and (lr_ is None or lr_ == sr)
            lines.append(f"SOURCE rev={sr} clean={'yes' if clean else 'NO'} lane_rev_equal={'yes' if rev_ok else 'NO'}")
        else:
            lines.append("SOURCE not a git work tree clean=NO")
        work.mkdir(parents=True, exist_ok=True)
        names = sorted(set(s["rows"]) & set(s["ledger"]["rows"])
                       - {n for n in s["bad_decl"]})
        names = [n for n in names if not any(d.startswith(f"{n}:") for d in s["argv_defect"])]
        workers = [Worker(source, work, i) for i in range(max(1, jobs))]
        free = list(range(len(workers)))
        import threading
        lock = threading.Lock()
        r53_green_nonentry = load_r53_green_nonentry(lane)

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
    lines.append(f"PREDICATE R54-C2 {'pass' if ok else 'fail'}")
    return (0 if ok else 1), lines


# --------------------------------------------------------------------------------------- selftest
HEAD_ROW = ["## Gate/probe registry", "", "| name | kind | entry | verdict map | self-test | pinned | scope | owner |",
            "|---|---|---|---|---|---|---|---|"]


def _mk_fixture(root: Path, gates: dict[str, str], rows: list[tuple[str, str]], ledger_rows: dict, r53_rows=None,
                git: bool = True, poisoned_gitconfig: str | None = None) -> Path:
    (root / "plans").mkdir(parents=True, exist_ok=True)
    skill = "\n".join(HEAD_ROW + list(rows)) + "\n"
    (root / "SKILL.md").write_text(skill)
    (root / "plans" / "round54-entrytruth.json").write_text(
        json.dumps({"schema": SCHEMA, "rows": ledger_rows}, indent=1) + "\n")
    if r53_rows is not None:
        (root / "plans" / "round53-tipstate.json").write_text(
            json.dumps({"schema": "r53-tipstate-v1", "rows": r53_rows}, indent=1) + "\n")
    for name, body in gates.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    if poisoned_gitconfig is not None:
        (root / "poison.gitconfig").write_text(poisoned_gitconfig)
    if git:
        subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=f", "-c", "user.email=f@f", "commit", "-qm", "x"],
                       check=True)
    return root


GATE_BODY = """#!/usr/bin/env python3
import subprocess, sys
mode = sys.argv[1] if len(sys.argv) > 1 else "entry"
if mode == "--selftest":
    print("selftest ok"); sys.exit(0)
if mode == "who":
    p = subprocess.run(["git", "config", "--get", "user.name"], capture_output=True, text=True)
    print(p.stdout.strip()); sys.exit(0)
rc = {exit}
if rc != 0:
    print("entry failed rc=%d" % rc)
sys.exit(rc)
"""


def selftest() -> int:
    work = Path(tempfile.mkdtemp(prefix="r54c2-selftest-"))
    cases = []

    def check(label, rc, lines, want_rc, want_in=(), want_out=()):
        ok = rc == want_rc and all(any(w in ln for ln in lines) for w in want_in) \
            and all(not any(w in ln for ln in lines) for w in want_out)
        cases.append((label, ok, f"rc={rc}"))

    # case 1: truthful fixture passes
    root = work / "t1"
    gates = {"plans/gate_a.py": GATE_BODY.format(exit=0), "plans/gate_b.py": GATE_BODY.format(exit=3)}
    rows = [("| `gate-a` | gate | `python3 plans/gate_a.py` | `0` ok · `1` bad | none | none | none | kengaku |",),
            ("| `gate-b` | gate | `python3 plans/gate_b.py` | `0` ok · `1` bad | none | none | none | kengaku |",)]
    ledger_rows = {
        "gate-a": {"entry_argv": ["python3", "plans/gate_a.py"], "entry_exit": 0, "entry_state": "green"},
        "gate-b": {"entry_argv": ["python3", "plans/gate_b.py"], "entry_exit": 3, "entry_state": "red",
                   "reason": "the gate's entry mode is documented broken until its fixture parser is repaired",
                   "evidence": "entry failed rc=3"},
    }
    _mk_fixture(root, gates, [r[0] for r in rows], ledger_rows)
    rc, lines = evaluate(root, root, work / "w1", 1, 60, dry=False)
    check("truthful", rc, lines, 0, want_in=("PREDICATE R54-C2 pass",))

    # case 2: laundering fixture — declared green but entry exits nonzero
    root = work / "t2"
    gates = {"plans/gate_c.py": GATE_BODY.format(exit=2)}
    ledger_rows = {"gate-c": {"entry_argv": ["python3", "plans/gate_c.py"], "entry_exit": 0, "entry_state": "green"}}
    _mk_fixture(root, gates, ["| `gate-c` | gate | `python3 plans/gate_c.py` | `0` ok · `1` bad | none | none | none | kengaku |"],
                ledger_rows)
    rc, lines = evaluate(root, root, work / "w2", 1, 60, dry=False)
    check("laundered-flagged", rc, lines, 1, want_in=("LAUNDERED gate-c", "PREDICATE R54-C2 fail"))

    # case 3: non-entry argv rejected statically
    root = work / "t3"
    gates = {"plans/gate_d.py": GATE_BODY.format(exit=0)}
    ledger_rows = {"gate-d": {"entry_argv": ["python3", "plans/gate_d.py", "--selftest"], "entry_exit": 0,
                              "entry_state": "green"}}
    _mk_fixture(root, gates, ["| `gate-d` | gate | `python3 plans/gate_d.py` | `0` ok · `1` bad | none | none | none | kengaku |"],
                ledger_rows)
    rc, lines = evaluate(root, root, work / "w3", 1, 60, dry=False)
    check("selftest-argv-rejected", rc, lines, 1, want_in=("ARGV-DEFECT",))

    # case 4: hermetic env — caller's poisoned GIT_CONFIG_GLOBAL must not leak
    root = work / "t4"
    gates = {"plans/gate_e.py": GATE_BODY.format(exit=0)}
    ledger_rows = {"gate-e": {"entry_argv": ["python3", "plans/gate_e.py", "who"], "entry_exit": 0,
                              "entry_state": "green"}}
    _mk_fixture(root, gates, ["| `gate-e` | gate | `python3 plans/gate_e.py` | `0` ok · `1` bad | none | none | none | kengaku |"],
                ledger_rows, poisoned_gitconfig="[user]\n\tname = poisoned\n")
    # run the gate directly under a poisoned caller env (r53-style inherited env) vs the counter env
    poison_env = dict(os.environ)
    poison_env["GIT_CONFIG_GLOBAL"] = str(root / "poison.gitconfig")
    p = subprocess.run(["python3", "plans/gate_e.py", "who"], cwd=root, capture_output=True, text=True, env=poison_env)
    leaked = "poisoned" in (p.stdout or "")
    tmp = Path(tempfile.mkdtemp(dir=str(work)))
    p2 = subprocess.run(["python3", "plans/gate_e.py", "who"], cwd=root, capture_output=True, text=True,
                        env=hermetic_env(tmp))
    clean_out = "poisoned" not in (p2.stdout or "")
    cases.append(("env-poison-leaks-under-inherited-env", bool(leaked), (p.stdout or "").strip()))
    cases.append(("env-hermetic-under-counter-env", bool(clean_out), (p2.stdout or "").strip()))
    rc, lines = evaluate(root, root, work / "w4", 1, 60, dry=False)
    check("fixture-passes-hermetically", rc, lines, 0, want_in=("PREDICATE R54-C2 pass",))

    # case 5: dry mode on a missing ledger fails statically
    root = work / "t5"
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text("\n".join(HEAD_ROW) + "\n")
    rc, lines = evaluate(root, root, None, 1, 60, dry=True)
    check("dry-missing-ledger", rc, lines, 1, want_in=("LEDGER ledger absent",))

    passed = sum(1 for _, ok, _ in cases if ok)
    for name, ok, detail in cases:
        print(f"[selftest] {'PASS' if ok else 'FAIL'} {name} {detail}")
    print(f"[selftest] {passed}/{len(cases)} PASS")
    shutil.rmtree(work, ignore_errors=True)
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
        return selftest()
    lane = Path(args.lane)
    source = Path(args.source) if args.source else None
    work = Path(args.work) if args.work else None
    if work is None and not args.dry:
        work = Path(tempfile.mkdtemp(prefix="r54c2-"))
    rc, lines = evaluate(lane, source, work, args.jobs, args.timeout, args.dry)
    print("\n".join(lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
