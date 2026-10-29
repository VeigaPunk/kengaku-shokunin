#!/usr/bin/env python3
"""C2CritLedgerReach: routes against the FROZEN plans/round53_c2_tipstate.py counter.

Every fixture lives under /fast/scratch/hyaku/kengaku-r53/C2CritLedgerReach/fx. The counter is run from a
scratch copy (bin/counter.py, sha256 859ec38d...), never from the lane. Each run's full output is written to
out/<label>.txt next to this file.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r53/C2CritLedgerReach")
COUNTER = S / "bin" / "counter.py"
FX = S / "fx"
SEAT = Path(__file__).resolve().parent
OUT = SEAT / "out"
REAL_SKILL = (S / "lane" / "SKILL.md").read_text()
SCHEMA = "r53-tipstate-v1"
REASON = "the fixture gate exits one because the row defect is planted on purpose here"
DEFECT = "import sys\nprint('DEFECT missing fixture row')\nsys.exit(1)\n"
PASSS = "import sys\nsys.exit(0)\n"
HDR = ["| name | kind | entry | verdict map | self-test | pinned | scope | owner |", "|---|---|---|---|---|---|---|---|"]
RESULTS = []


def write_files(d, files):
    for rel, body in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)


def git(d, *a):
    return subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True, check=True)


def repo(name, files, dirty=None):
    d = FX / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    write_files(d, files)
    git(d, "add", "-A")
    git(d, "-c", "user.name=c2", "-c", "user.email=c2@fixture.invalid", "commit", "-qm", "fixture")
    if dirty:
        write_files(d, dirty)
    return d


def plain(name, files):
    d = FX / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    write_files(d, files)
    return d


def lane(name, skill_text, ledger):
    d = plain(f"{name}-lane", {})
    (d / "plans").mkdir()
    (d / "SKILL.md").write_text(skill_text)
    body = ledger if isinstance(ledger, str) else json.dumps({"schema": SCHEMA, "base": "fixture", "rows": ledger})
    (d / "plans" / "round53-tipstate.json").write_text(body)
    return d


def row(n, ticks=True, entry=None):
    nm = f"`{n}`" if ticks else n
    e = entry or f"`python3 plans/{n}.py`"
    return f"| {nm} | gate | {e} | `0` ok · `1` bad | none | none | none | kengaku |"


def section(rows, heading="## Gate/probe registry"):
    return "\n".join([heading, "", *HDR, *rows, ""]) + "\n"


def G(argv, kind="entry", timeout_s=None):
    e = {"argv": argv, "exit": 0, "state": "green", "kind": kind}
    if timeout_s is not None:
        e["timeout_s"] = timeout_s
    return e


def Rd(argv, ex, ev, reason=REASON, kind="entry"):
    return {"argv": argv, "exit": ex, "state": "red", "kind": kind, "evidence": ev, "reason": reason}


def run_counter(label, lane_dir, src, jobs=4, extra=()):
    base = FX / label
    shutil.rmtree(base, ignore_errors=True)
    (base / "tmp").mkdir(parents=True)
    work = base / "work"
    cmd = ["python3", str(COUNTER), "--lane", str(lane_dir)]
    if src is not None:
        cmd += ["--source", str(src)]
    cmd += ["--work", str(work), "--jobs", str(jobs), *extra]
    env = {**os.environ, "TMPDIR": str(base / "tmp")}
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=900)
    text = p.stdout + p.stderr
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{label}.txt").write_text(f"$ {' '.join(cmd)}\nexit={p.returncode}\n{text}")
    return p.returncode, text


def pred(text):
    if "PREDICATE R53-C2 pass" in text:
        return "pass"
    if "PREDICATE R53-C2 fail" in text:
        return "fail"
    return "none"


def summ(rc, text):
    keep = [l for l in text.splitlines() if l.startswith(("ROWS", "SOURCE", "RUN", "TIPSTATE", "PREDICATE", "ARGV"))
            or l.startswith(("  MISMATCH", "  TIMEOUT", "  BAD", "  MISSING", "  EXTRA", "  ENTRY", "  EVIDENCE", "  LEDGER"))]
    return " / ".join(l.strip() for l in keep)[:400]


def attack(label, lane_dir, src, note, cond=None, jobs=4, extra=()):
    rc, t = run_counter(label, lane_dir, src, jobs=jobs, extra=extra)
    landed = pred(t) == "pass" and (cond is None or cond(t))
    line = f"{'LANDED' if landed else 'NOT-LANDED'} {label} rc={rc} pred={pred(t)} :: {note} :: {summ(rc, t)}"
    print(line)
    RESULTS.append(line)
    return rc, t


def control(label, lane_dir, src, note, want_fail_in, jobs=4, extra=()):
    rc, t = run_counter(label, lane_dir, src, jobs=jobs, extra=extra)
    caught = pred(t) == "fail" and all(w in t for w in want_fail_in)
    line = f"{'CAUGHT' if caught else 'MISSED'} {label} rc={rc} pred={pred(t)} :: {note} :: {summ(rc, t)}"
    print(line)
    RESULTS.append(line)
    return rc, t


def main():
    FX.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- C0 baseline: the counter's own selftest (scratch TMPDIR)
    st = FX / "selftest"
    st.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["python3", str(COUNTER), "--selftest"], capture_output=True, text=True,
                       env={**os.environ, "TMPDIR": str(st)}, timeout=900)
    (OUT / "C0-selftest.txt").write_text(f"exit={p.returncode}\n{p.stdout}{p.stderr}")
    line = f"BASELINE C0-selftest rc={p.returncode} :: {[l for l in p.stdout.splitlines() if 'cases=' in l]}"
    print(line)
    RESULTS.append(line)

    # ---- controls: the counter must catch these
    src = repo("C1-src", {"plans/a.py": DEFECT, "plans/b.py": PASSS})
    ln = lane("C1", section([row("a"), row("b")]),
              {"a": Rd(["python3", "plans/a.py"], 1, "DEFECT missing fixture row"), "b": G(["python3", "plans/b.py"])})
    attack("C1-control-honest", ln, src, "control: honest red+green ledger", cond=None)
    ln = lane("C2", section([row("a"), row("b")]),
              {"a": G(["python3", "plans/a.py"]), "b": G(["python3", "plans/b.py"])})
    control("C2-control-forged-green", ln, src, "control: real defect declared green",
            ["MISMATCH a declared exit=0 observed exit=1"])
    control("C3-control-only", lane("C3", section([row("a"), row("b")]),
                                    {"a": Rd(["python3", "plans/a.py"], 1, "DEFECT missing fixture row"),
                                     "b": G(["python3", "plans/b.py"])}),
            src, "control: --only is never a pass", [], extra=("--only", "a"))
    src4 = repo("C4-src", {"plans/a.py": "import time\ntime.sleep(5)\n"})
    control("C4-control-timeout", lane("C4", section([row("a")]), {"a": G(["python3", "plans/a.py"], timeout_s=1)}),
            src4, "control: tight timeout_s on a slow gate", ["TIMEOUT a"])
    src5 = repo("C5-src", {"plans/a.py": PASSS}, dirty={"plans/untracked_helper.py": "x = 1\n"})
    control("C5-control-dirty-git", lane("C5", section([row("a")]), {"a": G(["python3", "plans/a.py"])}),
            src5, "control: dirty git source (porcelain not clean)", ["clean=no"])

    # ---- A: zero-row and registry-shape routes
    src_d = repo("A-src", {"plans/a.py": DEFECT})
    attack("A1-zero-no-heading", lane("A1", "# Fixture\n\nNo registry section here.\n", {}), src_d,
           "no registry heading at all, empty ledger; registry=0", cond=lambda t: "ROWS registry=0" in t)
    attack("A2-zero-empty-section", lane("A2", section([]), {}), src_d,
           "heading present, zero rows, empty ledger", cond=lambda t: "ROWS registry=0" in t)
    pre = "The table `## Gate/probe registry` below lists the rows.\n\n## Overview\n\nprose.\n\n"
    attack("A3-zero-prose-mention", lane("A3", pre + section([row("a")]), {}), src_d,
           "first occurrence of the heading is prose; real defective row a never executed",
           cond=lambda t: "ROWS registry=0" in t)
    srcA4 = repo("A4-src", {"plans/a.py": PASSS, "plans/b.py": DEFECT})
    attack("A4-two-headings", lane("A4", section([row("a")]) + "\n## Notes\n\nbetween the two tables.\n\n"
                                   + section([row("b")]),
                                   {"a": G(["python3", "plans/a.py"])}),
           srcA4, "heading appears twice; second block (row b, real defect) never counted",
           cond=lambda t: "ROWS registry=1" in t)
    attack("D1-row-no-backticks", lane("D1", section([row("a"), row("b", ticks=False)]),
                                       {"a": G(["python3", "plans/a.py"])}),
           srcA4, "row b with a plain (unbackticked) name cell is invisible to NAME_ROW",
           cond=lambda t: "ROWS registry=1" in t)
    srcD2 = repo("D2-src", {"plans/a.py": PASSS, "plans/__dups__.py": DEFECT})
    attack("D2-sentinel-name", lane("D2", section([row("a"), row("__dups__")]),
                                    {"a": G(["python3", "plans/a.py"])}),
           srcD2, "row named __dups__ overwritten by the duplicate-name sentinel",
           cond=lambda t: "ROWS registry=1" in t)
    skill_out = section([row("a")]) + "\n## Retired\n\n" + "\n".join(HDR) + "\n" + row("b") + "\n"
    attack("D3-row-outside-block", lane("D3", skill_out, {"a": G(["python3", "plans/a.py"])}),
           srcA4, "row b placed after an H2 is outside the registry block and never counted",
           cond=lambda t: "ROWS registry=1" in t)
    dup_json = ('{"schema":"%s","base":"fixture","rows":{"a":{"argv":["python3","plans/a.py"],"exit":1,'
                '"state":"red","kind":"entry","evidence":"DEFECT missing fixture row","reason":"%s"},'
                '"a":{"argv":["python3","plans/a.py"],"exit":0,"state":"green","kind":"entry"}}}') % (SCHEMA, REASON)
    attack("D4-duplicate-json-key", lane("D4", section([row("a")]), dup_json), src_d,
           "duplicate JSON key: json.loads keeps the last entry; counted ledger=1 hides the first",
           cond=None)

    # ---- argv routes: script named as a dead argument, --help relabelled, cat/true, wrapper swallowing exit
    attack("A5-dead-argument", lane("A5", section([row("a")]),
                                    {"a": G(["python3", "-c", "pass", "plans/a.py"])}),
           src_d, "argv runs `pass`; plans/a.py (exits 1) is only a dead argument")
    srcH = repo("A6-src", {"plans/a.py": "import sys\nif '--help' in sys.argv:\n    print('usage: a.py')\n"
                                         "    sys.exit(0)\nprint('DEFECT missing fixture row')\nsys.exit(1)\n"})
    attack("A6-help-as-entry", lane("A6", section([row("a")]),
                                    {"a": G(["python3", "plans/a.py", "--help"], kind="entry")}),
           srcH, "--help exit 0 declared kind=entry; ARGV entry=1 help=0",
           cond=lambda t: "ARGV entry=1 selftest=0 help=0" in t)
    attack("A7-cat-not-python", lane("A7", section([row("a")]), {"a": G(["cat", "plans/a.py"])}),
           src_d, "argv is `cat`: the script is never executed, exit 0 when the file exists")
    attack("A8-wrapper-swallows", lane("A8", section([row("a")]),
                                       {"a": G(["sh", "-c", "python3 plans/a.py; exit 0", "plans/a.py"])}),
           src_d, "shell wrapper appends `exit 0`; a.py (exits 1) reported green")

    # ---- source-cleanliness and source identity
    srcPlain = plain("A9-src", {"plans/a.py": "import os, sys\nsys.exit(0 if os.path.exists('plans/untracked_helper.py') else 1)\n",
                                "plans/untracked_helper.py": "x = 1\n"})
    attack("A9-plain-dir-source", lane("A9", section([row("a")]), {"a": G(["python3", "plans/a.py"])}),
           srcPlain, "non-git source: clean=None accepted; no SOURCE line printed",
           cond=lambda t: "SOURCE" not in t)
    srcGitUntracked = repo("A9b-src", {"plans/a.py": "import os, sys\nsys.exit(0 if os.path.exists('plans/untracked_helper.py') else 1)\n"},
                           dirty={"plans/untracked_helper.py": "x = 1\n"})
    control("A9b-control-git-untracked", lane("A9b", section([row("a")]), {"a": G(["python3", "plans/a.py"])}),
            srcGitUntracked, "same untracked helper in a git source (clean=no)", ["clean=no"])
    h1 = repo("H1-src", {"plans/a.py": PASSS})
    first = git(h1, "rev-parse", "HEAD").stdout.strip()
    write_files(h1, {"plans/a.py": DEFECT})
    git(h1, "add", "-A")
    git(h1, "-c", "user.name=c2", "-c", "user.email=c2@fixture.invalid", "commit", "-qm", "tip defect")
    old = FX / "H1-old"
    shutil.rmtree(old, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(h1), str(old)], check=True)
    subprocess.run(["git", "-C", str(old), "checkout", "-q", first], check=True)
    ln_h1 = lane("H1", section([row("a")]), {"a": G(["python3", "plans/a.py"])})
    attack("H1-old-commit-source", ln_h1, old,
           "source is an older commit (a.py green) while the tip (a.py red) is the landing tree; ledger base never read",
           cond=lambda t: "SOURCE rev=" + first in t)
    control("H1-control-tip-source", ln_h1, h1, "control: same ledger, the real tip source", ["MISMATCH a declared exit=0 observed exit=1"])

    # ---- lane registry vs clean source: the counter reads SKILL.md and ledger from --lane, not from the source
    srcI1 = repo("I1-src", {"SKILL.md": section([row("a"), row("b")]), "plans/a.py": PASSS, "plans/b.py": DEFECT})
    attack("I1-lane-registry-not-tip", lane("I1", section([row("a")]), {"a": G(["python3", "plans/a.py"])}),
           srcI1, "tip SKILL.md has rows a and b (b red); lane SKILL.md has only a; registry=1 passes",
           cond=lambda t: "ROWS registry=1" in t)

    # ---- cross-row state: reset is git-only; the clone's .git/config survives reset --hard and clean -fdx
    b1 = repo("B1-src", {
        "plans/a.py": "import subprocess, sys\nsubprocess.run(['git', 'config', 'c2.flag', '1'], check=True)\nsys.exit(0)\n",
        "plans/b.py": "import subprocess, sys\nr = subprocess.run(['git', 'config', '--get', 'c2.flag'], capture_output=True, text=True)\nsys.exit(0 if r.stdout.strip() == '1' else 1)\n"})
    lnB1 = lane("B1", section([row("a"), row("b")]), {"a": G(["python3", "plans/a.py"]), "b": G(["python3", "plans/b.py"])})
    attack("B1-git-config-carries", lnB1, b1, "row a writes clone .git/config; row b green only because of a (jobs=1)",
           jobs=1, cond=None)
    fresh = FX / "B1-fresh"
    shutil.rmtree(fresh, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(b1), str(fresh)], check=True)
    rcb = subprocess.run(["python3", "plans/b.py"], cwd=fresh, capture_output=True, text=True).returncode
    line = f"TRUTH B1-fresh-clone-row-b-alone exit={rcb} (a clean clone without row a)"
    print(line)
    RESULTS.append(line)
    for k in range(1, 6):
        attack(f"B2-jobs4-run{k}", lnB1, b1, "same ledger, jobs=4: pass/fail depends on scheduling", jobs=4)
    srcB3 = plain("B3-src", {
        "plans/a.py": "import sys\nopen('plans/flag.txt', 'w').write('1')\nsys.exit(0)\n",
        "plans/b.py": "import os, sys\nsys.exit(0 if os.path.exists('plans/flag.txt') else 1)\n"})
    attack("B3-plain-dir-no-reset", lane("B3", section([row("a"), row("b")]),
                                         {"a": G(["python3", "plans/a.py"]), "b": G(["python3", "plans/b.py"])}),
           srcB3, "non-git source: no reset between rows; a writes plans/flag.txt that b reads (jobs=1)", jobs=1)
    fresh3 = FX / "B3-fresh"
    shutil.rmtree(fresh3, ignore_errors=True)
    shutil.copytree(srcB3, fresh3)
    rcb3 = subprocess.run(["python3", "plans/b.py"], cwd=fresh3, capture_output=True, text=True).returncode
    line = f"TRUTH B3-fresh-copy-row-b-alone exit={rcb3}"
    print(line)
    RESULTS.append(line)

    # ---- evidence and reason: presence-only, not causal
    srcE1 = repo("E1-src", {"plans/a.py": "raise RuntimeError('fixture absent')\n"})
    attack("E1-generic-evidence", lane("E1", section([row("a")]),
                                       {"a": Rd(["python3", "plans/a.py"], 1, "Traceback (most recent call last)")}),
           srcE1, "any crash satisfies evidence 'Traceback (most recent call last)'")
    attack("E2-padded-reason-6char-evidence", lane("E2", section([row("a")]),
                                                   {"a": Rd(["python3", "plans/a.py"], 1, "DEFECT",
                                                            reason="one two three four five six seven eight nine ten")}),
           src_d, "10-word filler reason and 6-character evidence 'DEFECT' pass the red checks")
    srcE3 = repo("E3-src", {"plans/a.py": "import os, signal\nprint('FAULT injected', flush=True)\n"
                                          "os.kill(os.getpid(), signal.SIGKILL)\n"})
    attack("E3-signal-kill-as-red", lane("E3", section([row("a")]),
                                         {"a": Rd(["python3", "plans/a.py"], -9, "FAULT injected")}),
           srcE3, "a gate that kills itself with SIGKILL is declared red with exit -9 and accepted",
           cond=None)

    # ---- timeout_s type confusion and --dry exit code
    attack("F1-timeout-string", lane("F1", section([row("a")]), {"a": G(["python3", "plans/a.py"], timeout_s="2.5")}),
           src_d, "timeout_s '2.5': int() raises; counter exits by traceback, no PREDICATE line",
           cond=None)
    lnG1 = lane("G1", section([row("a")]), {"a": G(["python3", "plans/a.py"])})
    p = subprocess.run(["python3", str(COUNTER), "--lane", str(lnG1), "--dry"], capture_output=True, text=True,
                       timeout=300)
    (OUT / "G1-dry.txt").write_text(f"exit={p.returncode}\n{p.stdout}{p.stderr}")
    line = (f"{'LANDED' if p.returncode == 0 and 'PREDICATE' not in p.stdout else 'NOT-LANDED'} G1-dry rc={p.returncode} "
            f":: --dry exits 0 with no PREDICATE line; a caller that tests only $? sees success")
    print(line)
    RESULTS.append(line)

    # ---- real-tree routes: the frozen registry at the landed tree (HEAD of scratch clone)
    import importlib.util as iu
    spec = iu.spec_from_file_location("ctr", str(COUNTER))
    ctr = iu.module_from_spec(spec)
    spec.loader.exec_module(ctr)
    real_rows = ctr.registry_rows(REAL_SKILL)
    real_rows.pop("__dups__")
    names = sorted(real_rows)
    line = f"REAL registry rows={len(names)} heading_occurrences={REAL_SKILL.count(ctr.REGISTRY_HEADING)} script_none={sum(1 for n in names if ctr.row_script(real_rows[n]) is None)}"
    print(line)
    RESULTS.append(line)
    real_src = S / "lane"

    forged = {n: G(["python3", "-c", "pass", ctr.row_script(real_rows[n])]) for n in names}
    lnJ1 = lane("J1", REAL_SKILL, forged)
    srcJ1 = FX / "J1-src"
    shutil.rmtree(srcJ1, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", str(real_src), str(srcJ1)], check=True)
    attack("J1-real-registry-forged-green", lnJ1, srcJ1,
           "all 75 real rows declared green via `python3 -c pass <script>`",
           cond=lambda t: "ROWS registry=75 ledger=75" in t and "executed=75" in t)

    lnK1 = lane("K1", "Note: see `## Gate/probe registry` for the table.\n" + REAL_SKILL, {})
    attack("K1-real-one-line-prose-zeroes-registry", lnK1, srcJ1,
           "one prose line above the real table; empty ledger; registry=0",
           cond=lambda t: "ROWS registry=0" in t)

    block_rows = [l for l in ctr.registry_block(REAL_SKILL).splitlines() if ctr.NAME_ROW.match(l)]
    dropped = block_rows[-5:]
    reduced = REAL_SKILL
    for l in dropped:
        reduced = reduced.replace(l + "\n", "", 1)
    kept = [n for n in names if real_rows[n] not in dropped]
    lnK3 = lane("K3", reduced, {n: forged[n] for n in kept})
    attack("K3-real-five-rows-removed", lnK3, srcJ1,
           f"five real rows deleted from the lane SKILL.md and {len(kept)} ledger rows; the frozen 75 is not checked",
           cond=lambda t: f"ROWS registry={len(kept)} ledger={len(kept)}" in t)

    (OUT / "SUMMARY.txt").write_text("\n".join(RESULTS) + "\n")
    print("WROTE", OUT / "SUMMARY.txt")


if __name__ == "__main__":
    main()
