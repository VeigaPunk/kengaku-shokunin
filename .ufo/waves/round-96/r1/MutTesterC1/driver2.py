#!/usr/bin/env python3
"""Round-96 C1 mutation seat driver: run (mutant, input) pairs and record rc + full stdout.

rc comes from subprocess.CompletedProcess.returncode (never a shell $? after a substitution).
Every run has cwd = the scratch clone root and --lane . (except the wrong-cwd input, which uses
an absolute --lane from /tmp). Every --work lives outside the lane (except the deliberate
work-inside-lane input). Work dirs are deleted after each run.
"""
import concurrent.futures as cf
import json
import pathlib
import shutil
import subprocess
import sys

S = pathlib.Path("/fast/scratch/hyaku/kengaku-r96/MutTesterC1")
LANE = S / "lane"
T = "09717e49ff46fad5b255619d671aaaae52dfc180"
P1B = "e8a80c0e23f8a2b365756b4e971b4210afa3f829"
E, G = str(S / "E"), str(S / "G")
OUT = S / "runs"
OUT.mkdir(parents=True, exist_ok=True)

fixtures = json.loads((S / "fixtures.json").read_text())
BOGUS = "1" * 64

ARGINPUTS = {
    "IA-bwrap": dict(rev=T, bwrap="/nonexistent/bwrap", cwd=str(LANE), lane="."),
    "IB-workin": dict(rev=T, work=str(LANE / ".mutation-work"), cwd=str(LANE), lane="."),
    "IC-revbogus": dict(rev=BOGUS, cwd=str(LANE), lane="."),
    "IT-cwdtmp": dict(rev=T, cwd="/tmp", lane=str(LANE)),
}

PLAN = json.loads((S / "plan.json").read_text())


def run_one(job):
    mut, inp = job
    work = S / f"work/{mut}--{inp}"
    args = dict(rev=T, bwrap="/usr/bin/bwrap", cwd=str(LANE), lane=".")
    if inp in fixtures:
        args["rev"] = fixtures[inp]
    else:
        args.update(ARGINPUTS[inp])
    args.setdefault("work", str(work))
    cmd = [sys.executable, str(S / "mut" / f"{mut}.py"),
           "--lane", args["lane"], "--rev", args["rev"], "--work", args["work"],
           "--env-venv", E, "--grader-venv", G, "--bwrap", args["bwrap"]]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=args["cwd"])
        rc, so, se = proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        rc, so, se = 124, (e.stdout or ""), (e.stderr or "")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    pred = ""
    for line in so.splitlines():
        if line.startswith("PREDICATE"):
            pred = line.strip()
    body = (f"# mutant {mut}\n# input {inp}\n# rev {args['rev']}\n# cwd {args['cwd']}\n"
            f"# cmd {' '.join(cmd)}\n# rc {rc}\n" + so + (("\n[stderr]\n" + se) if se.strip() else ""))
    (OUT / f"{mut}--{inp}.txt").write_text(body)
    return {"mutant": mut, "input": inp, "rc": rc, "predicate": pred}


def main(which, workers=6):
    if which == "baseline":
        jobs = [("M00-orig", inp) for inp in PLAN["_inputs"]]
    elif which == "controls":
        jobs = [tuple(x) for x in PLAN["_controls"]]
    elif which == "t":
        jobs = [tuple(x) for x in PLAN["_t"]]
    elif which == "redo":
        jobs = [tuple(x) for x in PLAN["_redo"]]
    elif which == "all":
        jobs = [(m, inp) for m, inps in PLAN.items() if not m.startswith("_") for inp in inps]
    else:
        jobs = [(which, inp) for inp in PLAN[which]]
    rows = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for row in ex.map(run_one, jobs):
            rows.append(row)
            print(f"{row['mutant']:30s} {row['input']:26s} rc={row['rc']} {row['predicate']}", flush=True)
    with (OUT / "summary.jsonl").open("a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6)
