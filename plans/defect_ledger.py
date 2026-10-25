#!/usr/bin/env python3
"""Persistent routed-defect ledger checker (round 35, C2 calibration).

Mined from considerthese/2026-10-25.md proposal 2 ("one persistent routed-defect ledger instead of
a new plans/roundNN_defects.py per round"). `corpus/defects.jsonl` holds one JSON object per routed
defect: id, class, opened_round, source (spot-check path:line), check (a function name below),
status (open|closed), closed_round, recurrence_of. This script re-runs EVERY row's check at the
current tip, forever, and counts calibration mismatches: a row the ledger calls `closed` whose
check fails, or a row it calls `open` whose check passes (stale self-assessment).

Frozen predicate (same sentence in plans/round-35-claims.md and in the receipt label):
  C2 passes iff `python3 plans/defect_ledger.py --lane .` prints
  `rows=5 closed=5 observed_pass=5 mismatches=0` and `PREDICATE C2 pass`, exit 0.
  (The code's PREDICATE is ledger-generic: every row closed, every check passing, no mismatch;
  round 35 additionally requires the row count to read 5.)

Each check compares the lane's self-assessment text with an observation computed here from repo
bytes, so a text-only edit cannot pass a check whose observation is false.
"""
import argparse
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys

BRANCH = "refs/heads/master"
R34 = ".ufo/waves/round-34/"


def git(lane, *args):
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True, check=True).stdout


def r34_d1(lane):
    """Round-34 work left untracked (spot-check D1): nothing untracked under the round-34 wave
    tree or at the three round-34 plan-tool paths."""
    left = git(lane, "ls-files", "--others", "--exclude-standard", "--",
               "plans/round34_c1_verify.py", "plans/round34_defects.py", "plans/round34_mutate.py",
               R34.rstrip("/")).split("\n")
    left = [x for x in left if x]
    return (not left, f"untracked={len(left)}")


def r34_d2(lane):
    """Committed recursive corpus mirrors in round-34 scratch (spot-check D2): zero committed paths
    under the three mirror roots at the lane branch tip."""
    roots = [R34 + "mut-entries-scratch", R34 + "build/R34MutRegistry/mirror", R34 + "build/R34MutRegistry/mut"]
    n = len([x for x in git(lane, "ls-tree", "-r", "--name-only", BRANCH, "--", *roots).split("\n") if x])
    return (n == 0, f"committed_mirror_paths={n}")


def r34_d3(lane):
    """tb2-eval SHA256SUMS omitted the evaluator files (spot-check D3): the manifest lists
    test_outputs.py and test.sh, and every listed digest equals the file bytes."""
    d = lane / (R34 + "assimilation/captures/tb2-eval")
    listed = {}
    for line in (d / "SHA256SUMS").read_text().splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})\s+\*?(\S+)", line.strip())
        if m:
            listed[m.group(2)] = m.group(1)
    bad = [n for n, h in listed.items() if not (d / n).is_file() or hashlib.sha256((d / n).read_bytes()).hexdigest() != h]
    have = all(k in listed for k in ("test_outputs.py", "test.sh"))
    return (have and not bad, f"listed={len(listed)} evaluator_listed={have} bad={len(bad)}")


def r34_d4(lane):
    """SCORECARD round-34 C2 row misattributed the red selftest (spot-check D4). Observation: the
    counter draft's selftest line is green and the harness selftest is red. Self-assessment: an
    appended SCORECARD correction line says exactly that, citing both lines."""
    b = lane / (R34 + "build")
    draft = (b / "R34C2CounterDraft.md").read_text().splitlines()
    harness = (b / "R34MutC2Harness.md").read_text().splitlines()
    observed = (len(draft) >= 8 and "cases=10 failed=0" in draft[7]
                and any("SELFTEST green failed" in l for l in harness[11:13]))
    if not observed:
        return (False, "observation changed: cited draft/harness lines no longer hold")
    sc = (lane / "SCORECARD.md").read_text().splitlines()
    corr = [l for l in sc if l.startswith("- **D4 correction (round 34 C2):**")]
    ok = len(corr) == 1 and all(s in corr[0] for s in (
        "R34C2CounterDraft.md:8", "cases=10 failed=0", "R34MutC2Harness.md:12", "SELFTEST green failed"))
    return (ok, f"correction_lines={len(corr)}")


S091_QUOTE = "ただし、RAKUDAベンチマークは1ターンの対話かつ少数データでの評価のため、対話性能の一側面しか測れていないことには注意が必要となります。"


def r34_d5(lane):
    """S091 refused as "quote absent" although the round's own reopen capture holds it (spot-check
    D5). Observation: the tag-stripped capture contains the staged quote. Self-assessment: the
    round-34 lesson carries an appended erratum saying so, and the round-35 lesson's Mistakes table
    has an S091 row."""
    cap = (lane / (R34 + "assimilation/captures/nec-s091-reopen.html")).read_text(errors="replace")
    flat = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", cap)))
    present = re.sub(r"\s+", "", S091_QUOTE) in flat
    if not present:
        return (False, "observation changed: quote not in nec-s091-reopen.html")
    l34 = (lane / "corpus/lessons/round-34.md").read_text().splitlines()
    err = [l for l in l34 if l.startswith("Erratum (round 35):") and "nec-s091-reopen.html" in l and "present" in l]
    l35p = lane / "corpus/lessons/round-35.md"
    mist = False
    if l35p.is_file():
        t = l35p.read_text()
        sec = re.search(r"^## Mistakes\n(.*?)(?=^## |\Z)", t, re.S | re.M)
        mist = bool(sec) and any(l.startswith("|") and "S091" in l for l in sec.group(1).splitlines())
    return (len(err) == 1 and mist, f"erratum_lines={len(err)} r35_mistake_row={mist}")


CHECKS = {f.__name__: f for f in (r34_d1, r34_d2, r34_d3, r34_d4, r34_d5)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    rows = [json.loads(l) for l in (lane / "corpus/defects.jsonl").read_text().splitlines() if l.strip()]
    closed = passed = mism = 0
    for r in rows:
        fn = CHECKS.get(r.get("check"))
        if fn is None:
            ok, note = False, f"unknown check {r.get('check')!r}"
        else:
            try:
                ok, note = fn(lane)
            except Exception as e:  # a crash is an observed failure, never a pass
                ok, note = False, f"error {type(e).__name__}: {e}"
        st = r.get("status")
        is_closed = st == "closed"
        agree = (is_closed and ok) or (st == "open" and not ok)
        closed += is_closed
        passed += ok
        mism += not agree
        print(f"{r['id']} status={st} observed={'pass' if ok else 'fail'} agree={'yes' if agree else 'NO'} {note}")
    print(f"rows={len(rows)} closed={closed} observed_pass={passed} mismatches={mism}")
    good = bool(rows) and closed == len(rows) and passed == len(rows) and mism == 0
    print(f"PREDICATE C2 {'pass' if good else 'fail'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
