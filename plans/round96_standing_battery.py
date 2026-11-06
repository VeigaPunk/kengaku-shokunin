#!/usr/bin/env python3
"""R96-C2 counter — standing C1 counters whose verdict at a revision disagrees with the lane's
recorded `met` (round 96, calibration).

The lane's SCORECARD records each of the fourteen C1 counters below as met in its own round.
This battery re-runs every one of them, from its own bytes AT the measured revision, against
that revision, and counts the ones that no longer pass. A standing counter that is red while
the self-assessment says met is a calibration mismatch.

Population (frozen here): round79_c1_population_ledger.py and round{83..95}_c1_replay.py, each
with its own invocation (rounds 79/83/84 take --quiet; every counter gets --lane, --rev and
--work; round-96 BASE receipts showed round 84 is not evaluable without --lane — lesson M1).

Run: a `git clone --shared` of the lane under --work, detached at --rev; each counter runs with
cwd = that clone, `--lane <clone> --rev <rev>`. GREEN iff rc 0 and the output holds exactly one
PREDICATE line and it is `PREDICATE R<n>-C1 pass`. Anything else (rc 1, rc 2, no or several
PREDICATE lines, timeout) is RED.

Bite (L7 keyed to the member set must still discriminate): for each counter of BITE_SET that is
GREEN at --rev, two forged ledger commits are made in the clone on top of --rev
(fixture identity, clone-local):
    own      the counter's own member row demoted to `unexecuted`
    other    one other member of the counter's own frozen-round set (the lexicographically first
             member executed in an earlier round) demoted to `unexecuted`
The counter must then print `PREDICATE R<n>-C1 fail` with rc 1 (bitten). A growth-tolerant L7
that stops seeing removals is not a repair.

    PREDICATE R96-C2 pass  iff  STANDING red=0 of 14  AND  BITES bitten=12 of 12

Usage:  python3 plans/round96_standing_battery.py --lane <repo> --rev <rev> --work <dir> [--jobs N]
Exit:   0 predicate pass, 1 fail, 2 could-not-evaluate (cwd not the lane root, --work inside the
        lane, unresolved revision, clone failure).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

POPULATION = [
    ("r79", "plans/round79_c1_population_ledger.py", "R79-C1", ["--quiet"]),
    ("r83", "plans/round83_c1_replay.py", "R83-C1", ["--quiet"]),
    ("r84", "plans/round84_c1_replay.py", "R84-C1", ["--quiet"]),
    ("r85", "plans/round85_c1_replay.py", "R85-C1", []),
    ("r86", "plans/round86_c1_replay.py", "R86-C1", []),
    ("r87", "plans/round87_c1_replay.py", "R87-C1", []),
    ("r88", "plans/round88_c1_replay.py", "R88-C1", []),
    ("r89", "plans/round89_c1_replay.py", "R89-C1", []),
    ("r90", "plans/round90_c1_replay.py", "R90-C1", []),
    ("r91", "plans/round91_c1_replay.py", "R91-C1", []),
    ("r92", "plans/round92_c1_replay.py", "R92-C1", []),
    ("r93", "plans/round93_c1_replay.py", "R93-C1", []),
    ("r94", "plans/round94_c1_replay.py", "R94-C1", []),
    ("r95", "plans/round95_c1_replay.py", "R95-C1", []),
]
BITE_SET = {
    # id: (own member, round)
    "r90": ("merge-diff-arc-agi-task", 90),
    "r91": ("modernize-scientific-stack", 91),
    "r92": ("llm-inference-batching-scheduler", 92),
    "r93": ("schemelike-metacircular-eval", 93),
    "r94": ("write-compressor", 94),
    "r95": ("fix-code-vulnerability", 95),
}
LEDGER = "plans/grader-population-ledger.json"
TIMEOUT = 3600
PRED = re.compile(r"^PREDICATE (R\d+-C\d+) (\S+)", re.M)


class CouldNotEvaluate(Exception):
    pass


def git(root: Path, *args: str, ident: bool = False) -> subprocess.CompletedProcess:
    pre = ["-c", "user.name=round96-fixture", "-c", "user.email=fixture@invalid",
           "-c", "commit.gpgsign=false"] if ident else []
    return subprocess.run(["git", *pre, "-C", str(root), *args], capture_output=True, text=True, timeout=300)


def run_counter(clone: Path, rev: str, path: str, extra: list[str], work: Path) -> tuple[int, str]:
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    argv = [sys.executable, "-B", str(clone / path), "--lane", str(clone), "--rev", rev,
            "--work", str(work), *extra]
    try:
        proc = subprocess.run(argv, cwd=str(clone), capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return proc.returncode, proc.stdout + proc.stderr


def verdict(rc: int, out: str, label: str) -> tuple[str, str]:
    preds = PRED.findall(out)
    if rc == 0 and preds == [(label, "pass")]:
        return "green", "-"
    first = next((ln for ln in out.splitlines() if ln.startswith("DEFECT")), "")
    return "red", (first or (out.strip().splitlines() or ["no-output"])[-1])[:200]


def forge(clone: Path, rev: str, demote: str, tag: str) -> str:
    """Commit, in the clone only, a ledger with `demote` set to unexecuted on top of rev."""
    if git(clone, "rev-parse", "--show-toplevel").stdout.strip() != str(clone):
        raise CouldNotEvaluate(f"fixture clone toplevel mismatch {clone}")
    if git(clone, "checkout", "-q", "--detach", rev).returncode != 0:
        raise CouldNotEvaluate(f"checkout {rev} in clone failed")
    ledger_path = clone / LEDGER
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    row = data["members"][demote]
    data["members"][demote] = {"classes": row["classes"], "evidence": "round96 bite fixture",
                               "reason": "unattempted", "status": "unexecuted"}
    ledger_path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    if git(clone, "commit", "-q", "-m", f"round96 bite fixture {tag}", "--", LEDGER, ident=True).returncode != 0:
        raise CouldNotEvaluate(f"fixture commit {tag} failed")
    sha = git(clone, "rev-parse", "HEAD").stdout.strip()
    git(clone, "checkout", "-q", "--detach", rev)
    return sha


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    if Path.cwd().resolve() != lane:
        raise CouldNotEvaluate(f"cwd {Path.cwd().resolve()} is not the lane root {lane}")
    if work == lane or lane in work.parents:
        raise CouldNotEvaluate(f"--work inside the lane {work}")
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{a.rev}^{{commit}}")
    if proc.returncode != 0:
        raise CouldNotEvaluate(f"unresolved-revision {a.rev}")
    rev = proc.stdout.strip()
    work.mkdir(parents=True, exist_ok=True)
    clone = work / "clone"
    if clone.exists():
        shutil.rmtree(clone)
    if subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(lane), str(clone)],
                      capture_output=True, text=True).returncode != 0:
        raise CouldNotEvaluate("clone failed")
    if git(clone, "checkout", "-q", "--detach", rev).returncode != 0:
        raise CouldNotEvaluate(f"checkout {rev} failed")
    print(f"# round-96 standing-counter battery rev {rev} cwd {Path.cwd().resolve()}")

    def job(item):
        gid, path, label, extra = item
        if not (clone / path).is_file():
            return gid, label, 2, "ABSENT"
        rc, out = run_counter(clone, rev, path, extra, work / "runs" / gid)
        return gid, label, rc, out

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        results = list(pool.map(job, POPULATION))
    green = {}
    for gid, label, rc, out in results:
        v, why = verdict(rc, out, label)
        green[gid] = v == "green"
        print(f"GATE {gid} rc={rc} verdict={v} reason={why}")
    red = sum(1 for v in green.values() if not v)
    print(f"STANDING total={len(POPULATION)} green={len(POPULATION) - red} red={red}")

    # bites: forged commits are serial (one clone), runs parallel
    base_ledger = json.loads((clone / LEDGER).read_text(encoding="utf-8"))["members"]
    forged = []
    for gid, (own, rnd) in sorted(BITE_SET.items()):
        if not green.get(gid):
            print(f"BITE {gid} kind=own skipped=not-green")
            print(f"BITE {gid} kind=other skipped=not-green")
            continue
        others = sorted(n for n, v in base_ledger.items()
                        if v.get("status") == "executed" and isinstance(v.get("round"), int) and v["round"] < rnd)
        if own not in base_ledger or not others:
            raise CouldNotEvaluate(f"bite population for {gid} unresolved")
        forged.append((gid, "own", forge(clone, rev, own, f"{gid}-own")))
        forged.append((gid, "other", forge(clone, rev, others[0], f"{gid}-other-{others[0]}")))
    labels = {gid: (path, label, extra) for gid, path, label, extra in POPULATION}

    def bite(item):
        gid, kind, sha = item
        path, label, extra = labels[gid]
        rc, out = run_counter(clone, sha, path, extra, work / "bites" / f"{gid}-{kind}")
        preds = PRED.findall(out)
        return gid, kind, rc, preds == [(label, "fail")] and rc == 1

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        bites = list(pool.map(bite, forged))
    bitten = 0
    for gid, kind, rc, ok in bites:
        bitten += 1 if ok else 0
        print(f"BITE {gid} kind={kind} rc={rc} bitten={1 if ok else 0}")
    want = 2 * len(BITE_SET)
    print(f"BITES checked={want} bitten={bitten}")
    shutil.rmtree(clone, ignore_errors=True)
    ok = red == 0 and bitten == want
    print("PREDICATE R96-C2 " + ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except CouldNotEvaluate as error:
        print(f"DEFECT SETUP {error}")
        print("PREDICATE R96-C2 could-not-evaluate")
        sys.exit(2)
