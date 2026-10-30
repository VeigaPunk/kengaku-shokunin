#!/usr/bin/env python3
"""C2CritPredicate2 — focused attacks on the argv/argument surface of the C2 counter.

The counter's entry_mismatch leg compares the ledger argv's *script path* with the script
named in the registry row's entry cell.  It never compares the argv's *arguments* with the
command the cell documents, and it never compares the argv's observed exit with the exit
the *documented* command produces.  These attacks exploit that.
"""
from __future__ import annotations
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, "/fast/scratch/hyaku/kengaku-r53/C2CritPredicate2")
from harness import (SEAT, LANE, COUNTER, git, lane_tree, make_fixture, registry, row_scripts,
                     load_ledger, save_ledger, stub_all, clone_source, run_counter, report, results)

FIX = SEAT / "fix"
OUT = SEAT / "out"


def green_all(D):
    led = load_ledger(D)
    for n, e in led["rows"].items():
        e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
    save_ledger(D, led)


def uv_to_python(D):
    led = load_ledger(D)
    for n, e in led["rows"].items():
        a = e.get("argv") or []
        if a and a[0] == "uv":
            i = a.index("python3")
            e["argv"] = a[i:]
    save_ledger(D, led)


def real_script(D, rel):
    """Restore one script's real bytes from the lane (undo the stub)."""
    data = subprocess.run(["git", "-C", str(LANE), "show", f"HEAD:{rel}"],
                          capture_output=True, text=True)
    if data.returncode == 0:
        p = D / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data.stdout)


def fixture(label, mutate, keep_real=()):
    def _mut(D):
        uv_to_python(D)
        green_all(D)
        for rel in keep_real:
            real_script(D, rel)
        if mutate:
            mutate(D)
    D = make_fixture(label, _mut, stub=True)
    S = clone_source(D, label)
    return D, S


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # ---- B1: launder ONE genuinely-red row to green by pointing its argv at --help ------
    # real script kept: round51_surfaces.py exits 1 on its documented command (--lane .)
    # and 0 on --help.  The registry cell still documents `--lane .`.
    def b1(D):
        led = load_ledger(D)
        e = led["rows"]["round51-surfaces"]
        e["argv"] = ["python3", "plans/round51_surfaces.py", "--help"]
        e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
        e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("b1-launder-red-row-via-help", b1,
                   keep_real=("plans/round51_surfaces.py",))
    rc, out = run_counter(D, S, "b1-launder-red-row-via-help")
    report("B1-launder-one-red-row-to-green-via---help", "PREDICATE R53-C2 pass", rc, out,
           notes="the row's DOCUMENTED command exits 1; the ledger's argv (--help) exits 0")
    # what does the documented command actually do?
    doc = subprocess.run(["git", "-C", str(D), "show", "HEAD:SKILL.md"], capture_output=True, text=True).stdout
    cell = next(l for l in doc.splitlines() if l.startswith("| `round51-surfaces`"))
    (OUT / "b1.registry-cell.txt").write_text(cell)
    obs = subprocess.run(["python3", "plans/round51_surfaces.py", "--lane", "."],
                         cwd=str(D), capture_output=True, text=True)
    (OUT / "b1.documented-command-output.txt").write_text(
        f"documented argv: python3 plans/round51_surfaces.py --lane .\nexit={obs.returncode}\n"
        + obs.stdout[-800:] + obs.stderr[-800:])

    # ---- B2: launder SEVEN red rows at once (still inside the 10% help cap) ------------
    # 78 rows -> help_limit = 7.8, so 7 help-kind rows are allowed.
    def b2(D):
        led = load_ledger(D)
        for n in ["round51-surfaces", "gate-flip-check", "adoption-check", "anchor-digest-check",
                  "mutant-direction-check", "round28-census", "round35-c1-coverage"]:
            e = led["rows"][n]
            script = e["argv"][1]
            e["argv"] = ["python3", script, "--help"]
            e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("b2-launder-seven-red-rows", b2)
    rc, out = run_counter(D, S, "b2-launder-seven-red-rows")
    report("B2-launder-seven-red-rows-via---help", "PREDICATE R53-C2 pass", rc, out,
           notes="7 help-kind rows = 8.97% of 78, under the 10% cap")

    # ---- B3: launder ALL TWELVE red rows: --help for the rest, --selftest where it works
    RED_ROWS = [n for n, e in load_ledger(SEAT / "lane").get("rows", {}).items()
                if e.get("state") == "red"]
    (OUT / "b3.red-rows.txt").write_text("\n".join(RED_ROWS) + "\n")

    def b3(D):
        led = load_ledger(D)
        for n in RED_ROWS:
            e = led["rows"][n]
            script = e["argv"][1]
            e["argv"] = ["python3", script, "--help"]
            e["kind"] = "help"; e["exit"] = 0; e["state"] = "green"
            e.pop("evidence", None); e.pop("reason", None)
        save_ledger(D, led)
    D, S = fixture("b3-launder-twelve-red-rows", b3)
    rc, out = run_counter(D, S, "b3-launder-twelve-red-rows")
    report("B3-launder-all-twelve-red-rows", "help_limit", rc, out,
           notes="12 help-kind rows = 15.4% of 78 -> should trip the 10% cap")

    # ---- B4: the .git/config leak survives the A3 reset --------------------------------
    # Worker.reset() does `git reset --hard <rev>` + `git clean -ffdx`; neither restores
    # .git/config, so a row that runs `git config --local` still contaminates the next row.
    def b4(D):
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
    D, S = fixture("b4-git-config-leak-survives-reset", b4)
    rc1, out1 = run_counter(D, S, "b4-git-config-leak-jobs1", jobs=1)
    rc4, out4 = run_counter(D, S, "b4-git-config-leak-jobs4", jobs=4)
    (OUT / "b4.comparison.txt").write_text(
        f"=== jobs=1 (rc={rc1}) ===\n{out1}\n=== jobs=4 (rc={rc4}) ===\n{out4}")
    report("B4-git-config-leak-survives-A3-reset", "PREDICATE R53-C2", rc1, out1,
           notes=f"jobs1 rc={rc1} / jobs4 rc={rc4}: same tree, same ledger, different verdict")

    (OUT / "summary-b.json").write_text(json.dumps(results, indent=1))
    print("\n=== summary ===")
    for r in results:
        print(f"{r['verdict']:14s} {r['label']:52s} rc={r['rc']}  seen={r['seen']!r}")


if __name__ == "__main__":
    main()
