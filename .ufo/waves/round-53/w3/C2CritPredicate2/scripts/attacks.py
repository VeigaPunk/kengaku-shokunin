#!/usr/bin/env python3
"""C2CritPredicate2 — attack suite against plans/round53_c2_tipstate.py (A1/A3 amended).

Every attack is a concrete fixture + command.  Nothing touches the real lane tree: fixtures are
built by exporting the lane's committed tree into a `git init` repo under the seat scratch dir.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys, tarfile, tempfile, io
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
from harness import (SEAT, LANE, SCRIPT, COUNTER, git, lane_tree, make_fixture, registry,
                     row_scripts, load_ledger, save_ledger, stub_all, clone_source, run_counter,
                     report, results)

FIX = SEAT / "fix"
OUT = SEAT / "out"


def green_all(D):
    led = load_ledger(D)
    for n, e in led["rows"].items():
        e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
    save_ledger(D, led)


def uv_to_python(D):
    """Rewrite the one uv-based ledger row to plain python3 (network-free fixtures)."""
    led = load_ledger(D)
    for n, e in led["rows"].items():
        a = e.get("argv") or []
        if a and a[0] == "uv":
            i = a.index("python3")
            e["argv"] = a[i:]
    save_ledger(D, led)


def base_fixture(label, mutate=None, stub=True, green=True, uvfix=True):
    def _mut(D):
        if uvfix:
            uv_to_python(D)
        if green:
            green_all(D)
        if mutate:
            mutate(D)
    D = make_fixture(label, _mut, stub=stub)
    S = clone_source(D, label)
    return D, S


def drop_row(name):
    def _m(D):
        t = (D / "SKILL.md").read_text()
        lines = [l for l in t.splitlines()
                 if not (l.startswith("|") and re.match(r"^\|\s*`([^`]+)`\s*\|", l)
                         and re.match(r"^\|\s*`([^`]+)`\s*\|", l).group(1) == name)]
        (D / "SKILL.md").write_text("\n".join(lines) + "\n")
        led = load_ledger(D)
        led["rows"].pop(name, None)
        save_ledger(D, led)
    return _m


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- control: all rows green, all scripts stubbed -> the counter must pass -------------
    D, S = base_fixture("control")
    rc, out = run_counter(D, S, "control")
    report("control-honest-green", "PREDICATE R53-C2 pass", rc, out)

    # ---- A1: ledger zero rows, heading renamed ------------------------------------------
    def a1(D):
        t = (D / "SKILL.md").read_text()
        t = t.replace("## Gate/probe registry", "## Registry")
        (D / "SKILL.md").write_text(t)
        led = load_ledger(D)
        led["rows"] = {}
        save_ledger(D, led)
    D, S = base_fixture("a1-zero-rows-renamed-heading", a1)
    rc, out = run_counter(D, S, "a1-zero-rows-renamed-heading")
    report("A1-ledger-zero-rows-heading-renamed", "row_set_pinned=BAD", rc, out)

    # ---- A2: 77 of 78 rows --------------------------------------------------------------
    D, S = base_fixture("a2-77-of-78-rows", drop_row("adoption-check"))
    rc, out = run_counter(D, S, "a2-77-of-78-rows")
    report("A2-77-of-78-rows", "row_set_pinned=BAD", rc, out)

    # ---- A3: argv `python3 -c pass <script>` --------------------------------------------
    def a3(D):
        led = load_ledger(D)
        led["rows"]["adoption-check"]["argv"] = ["python3", "-c", "pass", "plans/adoption_check.py"]
        save_ledger(D, led)
    D, S = base_fixture("a3-python-c-pass", a3)
    rc, out = run_counter(D, S, "a3-python-c-pass")
    report("A3-argv-python3-c-pass", "ENTRY-MISMATCH adoption-check", rc, out)

    # ---- A3b: shell wrapper -------------------------------------------------------------
    def a3b(D):
        led = load_ledger(D)
        led["rows"]["adoption-check"]["argv"] = ["sh", "-c", "python3 plans/adoption_check.py; exit 0",
                                                 "plans/adoption_check.py"]
        save_ledger(D, led)
    D, S = base_fixture("a3b-shell-wrapper", a3b)
    rc, out = run_counter(D, S, "a3b-shell-wrapper")
    report("A3b-argv-shell-wrapper", "ENTRY-MISMATCH adoption-check", rc, out)

    # ---- A4: --source is a non-git directory --------------------------------------------
    D, S = base_fixture("a4-source-non-git")
    plain = Path(tempfile.mkdtemp(prefix="plain-src-", dir=str(FIX))) / "plain"
    shutil.copytree(S, plain)
    shutil.rmtree(plain / ".git")
    rc, out = run_counter(D, plain, "a4-source-non-git")
    report("A4-source-non-git-dir", "clean=NO", rc, out)

    # ---- A5: --source is an older commit than the lane -----------------------------------
    D, S = base_fixture("a5-source-older-commit")
    old = Path(tempfile.mkdtemp(prefix="old-src-", dir=str(FIX))) / "old"
    subprocess.run(["git", "clone", "-q", "--shared", str(D), str(old)], check=True)
    # make the tip differ: neuter one script at the tip, keep the old clone at the parent rev
    sp = D / "plans/adoption_check.py"
    sp.write_text("import sys\nprint('stub ok')\nsys.exit(0)\n" if False else
                  (sp.read_text() + "\n# tip change\n"))
    git(D, "add", "-A"); git(D, "commit", "-q", "-m", "tip change")
    rc, out = run_counter(D, old, "a5-source-older-commit")
    report("A5-source-older-commit", "lane_rev_equal=NO", rc, out)

    # ---- A6: red row whose evidence is another row's output fragment ---------------------
    # two rows: 'adoption-check' prints MARKER; 'anchor-digest-check' prints OTHER.
    def a6(D):
        (D / "plans/adoption_check.py").write_text("print('MARKER-FROM-OTHER-ROW')\n")
        (D / "plans/anchor_digest_check.py").write_text("print('OTHER-OUTPUT')\n")
        led = load_ledger(D)
        e = led["rows"]["anchor-digest-check"]
        e.update(exit=1, state="red", evidence="MARKER-FROM-OTHER-ROW",
                 reason="the evidence fragment is taken from the other row's output and is not present here")
        save_ledger(D, led)
    D, S = base_fixture("a6-evidence-from-other-row", a6, green=False)
    rc, out = run_counter(D, S, "a6-evidence-from-other-row")
    report("A6-red-evidence-borrowed-from-other-row", "EVIDENCE-MISSING anchor-digest-check", rc, out)

    # ---- A7: ledger timeout_s above the operator cap -------------------------------------
    def a7(D):
        (D / "plans/adoption_check.py").write_text("import time\ntime.sleep(60)\n")
        led = load_ledger(D)
        led["rows"]["adoption-check"]["timeout_s"] = 100000
        save_ledger(D, led)
    D, S = base_fixture("a7-timeout-above-operator-cap", a7)
    rc, out = run_counter(D, S, "a7-timeout-above-operator-cap", timeout=5)
    report("A7-ledger-timeout-above-operator-cap", "TIMEOUT adoption-check", rc, out)

    # ---- A8: a row commits inside its worker and leaks into the next row ------------------
    def a8(D):
        (D / "plans/adoption_check.py").write_text(
            "import subprocess\n"
            "subprocess.run(['git','-c','user.name=x','-c','user.email=x@x.invalid','commit','-q',"
            "'--allow-empty','-m','leak'],check=True)\n"
            "open('leak.txt','w').write('x')\n"
            "subprocess.run(['git','add','leak.txt'],check=True)\n"
            "subprocess.run(['git','-c','user.name=x','-c','user.email=x@x.invalid','commit','-q','-m','leak2'],check=True)\n"
            "subprocess.run(['git','init','-q','nested'],check=True)\n")
        (D / "plans/anchor_digest_check.py").write_text(
            "import os,sys\n"
            "sys.exit(1 if os.path.exists('leak.txt') or os.path.exists('nested') else 0)\n")
    D, S = base_fixture("a8-commit-leaks-to-next-row", a8)
    rc, out = run_counter(D, S, "a8-commit-leaks-to-next-row", jobs=1)
    report("A8-row-commit-leaks-to-next-row", "MISMATCH anchor-digest-check", rc, out)

    # ---- A9: a gate that cannot fail, declared green -------------------------------------
    #   (the instrument's bytes are replaced by an always-exit-0 stub; the ledger says green)
    def a9(D):
        (D / "plans/adoption_check.py").write_text("import sys\nprint('always green')\nsys.exit(0)\n")
    D, S = base_fixture("a9-always-exit-0-gate", a9)
    rc, out = run_counter(D, S, "a9-always-exit-0-gate")
    report("A9-gate-that-cannot-fail-declared-green", "PREDICATE R53-C2 pass", rc, out,
           notes="counter certifies green; instrument bytes are unpinned")

    # ---- A10: same script, different arguments than the registry cell documents -----------
    def a10(D):
        led = load_ledger(D)
        led["rows"]["adoption-check"]["argv"] = ["python3", "plans/adoption_check.py",
                                                  "--expect", ".ufo/waves/round-99/claims/other-expect.json"]
        save_ledger(D, led)
    D, S = base_fixture("a10-argv-argument-substitution", a10)
    rc, out = run_counter(D, S, "a10-argv-argument-substitution")
    report("A10-argv-argument-substitution", "PREDICATE R53-C2 pass", rc, out,
           notes="entry_mismatch is script-path-only")

    # ---- A11: .git/config contamination across rows in one worker ------------------------
    def a11(D):
        (D / "plans/adoption_check.py").write_text(
            "import subprocess\n"
            "subprocess.run(['git','config','--local','r53.leak','1'],check=True)\n")
        (D / "plans/anchor_digest_check.py").write_text(
            "import subprocess,sys\n"
            "p=subprocess.run(['git','config','--local','--get','r53.leak'],capture_output=True,text=True)\n"
            "sys.exit(0 if p.stdout.strip()=='1' else 1)\n")
        led = load_ledger(D)
        led["rows"]["anchor-digest-check"]["exit"] = 0
        led["rows"]["anchor-digest-check"]["state"] = "green"
        save_ledger(D, led)
    D, S = base_fixture("a11-git-config-contamination", a11)
    rc1, out1 = run_counter(D, S, "a11-git-config-contamination-jobs1", jobs=1)
    report("A11-git-config-contamination-jobs1", "PREDICATE R53-C2 pass", rc1, out1,
           notes="row order decides the observation")
    rc4, out4 = run_counter(D, S, "a11-git-config-contamination-jobs4", jobs=4)
    report("A11-git-config-contamination-jobs4", "MISMATCH anchor-digest-check", rc4, out4,
           notes="same tree+ledger, different --jobs")

    # ---- A12: malformed timeout_s (string) -----------------------------------------------
    def a12(D):
        led = load_ledger(D)
        led["rows"]["adoption-check"]["timeout_s"] = "2.5"
        save_ledger(D, led)
    D, S = base_fixture("a12-timeout-string", a12)
    rc, out = run_counter(D, S, "a12-timeout-string")
    report("A12-malformed-timeout_s", "PREDICATE R53-C2", rc, out,
           notes="no PREDICATE line => the counter died before the verdict")

    # ---- A13: the registry's own entry cell is rewritten to a different instrument -------
    #   (row NAMES stay pinned; the cell that says which script the row runs does not)
    def a13(D):
        t = (D / "SKILL.md").read_text()
        lines = []
        for l in t.splitlines():
            if l.startswith("|") and re.match(r"^\|\s*`adoption-check`\s*\|", l):
                l = l.replace("`python3 plans/adoption_check.py --lane . --expect "
                              "<expect.json> --census`",
                              "`python3 plans/always_ok.py`")
                if "always_ok.py" not in l:
                    cells = [c.strip() for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]
                    cells[2] = "`python3 plans/always_ok.py`"
                    l = "|" + "|".join(cells) + "|"
            lines.append(l)
        (D / "SKILL.md").write_text("\n".join(lines) + "\n")
        (D / "plans/always_ok.py").write_text("import sys\nprint('always green')\nsys.exit(0)\n")
        led = load_ledger(D)
        led["rows"]["adoption-check"]["argv"] = ["python3", "plans/always_ok.py"]
        save_ledger(D, led)
    D, S = base_fixture("a13-registry-cell-rewritten", a13)
    rc, out = run_counter(D, S, "a13-registry-cell-rewritten")
    report("A13-registry-entry-cell-rewritten-to-another-instrument", "PREDICATE R53-C2 pass", rc, out,
           notes="row names stay pinned; the cell that names the script does not")

    # ---- A14: a worker that runs `git gc` in a --shared clone of the source --------------
    def a14(D):
        (D / "plans/adoption_check.py").write_text(
            "import subprocess\nsubprocess.run(['git','gc','--quiet','--prune=now'],check=False)\n")
    D, S = base_fixture("a14-worker-git-gc", a14)
    before = subprocess.run(["git", "-C", str(S), "count-objects", "-v"], capture_output=True, text=True).stdout
    rc, out = run_counter(D, S, "a14-worker-git-gc", jobs=1)
    after = subprocess.run(["git", "-C", str(S), "count-objects", "-v"], capture_output=True, text=True).stdout
    ok = subprocess.run(["git", "-C", str(S), "fsck", "--no-progress"], capture_output=True, text=True)
    (OUT / "a14-worker-git-gc.before").write_text(before)
    (OUT / "a14-worker-git-gc.after").write_text(after + "\nfsck:\n" + ok.stdout + ok.stderr)
    report("A14-worker-runs-git-gc-in-shared-clone", "PREDICATE R53-C2", rc, out,
           notes=f"source fsck rc={ok.returncode}")

    # ---- A15: the same tree+ledger, two different --jobs ---------------------------------
    D, S = base_fixture("a15-nondeterminism-control", None)
    rc1, o1 = run_counter(D, S, "a15-jobs1", jobs=1)
    rc4, o4 = run_counter(D, S, "a15-jobs4", jobs=4)
    report("A15-same-tree-jobs1-vs-jobs4", "PREDICATE R53-C2", rc1, o1,
           notes=f"jobs1 rc={rc1} / jobs4 rc={rc4} (same tree, same ledger)")

    (OUT / "summary.json").write_text(json.dumps(results, indent=1))
    print("\n=== summary ===")
    for r in results:
        print(f"{r['verdict']:14s} {r['label']:48s} rc={r['rc']}  seen={r['seen']!r}")


if __name__ == "__main__":
    main()
