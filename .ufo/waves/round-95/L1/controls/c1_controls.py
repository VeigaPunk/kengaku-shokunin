#!/usr/bin/env python3
"""R95-C1 pre-freeze controls driver (round 95, L1 KengakuR95). Evidence script, not an instrument.

Builds a scratch clone of the lane at --base-rev (P1), then in that clone only (every git call
names -C <clone>, identity `fixture <fixture@invalid>`, toplevel asserted) commits a DRAFT claims
file whose frozen-instruments table holds the P1 instrument bytes, so the counter's L4/L8 legs can
pass, and runs plans/round95_c1_replay.py (from the clone) against:

  pos      honest: the probe's own receipt + ledger flip with legacy fields  -> want rc 0 (all legs)
  D4       probe swapped for a stub that prints predicted as observed, receipt regenerated from
           it (round-94 W-6 m11)                                            -> want rc 1, L8 fail
  D5       honest receipt with a foreign LANE_TIP (an orphan commit)  (m10) -> want rc 1, L3 fail
  D6       receipt with cases C02..C04 dropped from the observation block
           (m03+m04)                                                        -> want rc 1, L5+L6 fail
  D7       honest receipt with VULNERABLE_BOTTLE_SHA forged                  -> want rc 1, L6 fail
  D8       honest flip but the legacy fields omitted (routed defect 5)       -> want rc 1, L7 fail

Usage: python3 c1_controls.py --lane <lane> --base-rev <P1> --scratch <dir> --out <dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

GIT_ID = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
          "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null"]
INSTRUMENTS = ["plans/round95_vuln_probe.py", "plans/round95-cases.json", "plans/round95_c1_replay.py",
               "corpus/evidence/round95/graders/fix-code-vulnerability/tests/test_outputs.py",
               "corpus/evidence/round95/graders/fix-code-vulnerability/solution/solve.sh",
               "corpus/evidence/round95/graders/fix-code-vulnerability/environment/Dockerfile",
               "corpus/evidence/round95/graders/fix-code-vulnerability/upstream-bottle/bottle.py"]
RECEIPT = "corpus/evidence/round95/vuln-probe.txt"
LEDGER = "plans/grader-population-ledger.json"
MEMBER = "fix-code-vulnerability"
STUB = '''#!/usr/bin/env python3
import json, sys, hashlib
from pathlib import Path
a = sys.argv
lane = Path(a[a.index("--lane") + 1])
t = json.loads((lane / "plans/round95-cases.json").read_text())
print("# tb2 fix-code-vulnerability grader probe (round 95)")
print("OBSERVATIONS_BEGIN")
for c in t["cases"]:
    print("CASE %s predicted=%s observed=%s ok=True" % (c["id"], c["predicted"], c["predicted"]))
print("OBSERVATIONS_END")
print("mismatches 0")
'''


def git(d: Path, *args: str, check: bool = True) -> str:
    top = subprocess.run(["git", "-C", str(d), "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    if Path(top).resolve() != d.resolve():
        raise SystemExit(f"toplevel {top} != {d}")
    p = subprocess.run(["git", "-C", str(d), *GIT_ID, *args], capture_output=True, text=True, check=check)
    return p.stdout.strip()


def commit(d: Path, msg: str) -> str:
    git(d, "add", "-A")
    git(d, "commit", "-q", "--allow-empty", "-m", msg)
    return git(d, "rev-parse", "HEAD")


def flip(d: Path, legacy: bool) -> None:
    doc = json.loads((d / LEDGER).read_text())
    row = doc["members"][MEMBER]
    row.update({"status": "executed", "round": 95, "reason": "replayed",
                "evidence": "no-blocker: tests/test_outputs.py sha256=c006a5de95b69bd7; receipt " + RECEIPT})
    if legacy:
        row.update({"receipt": RECEIPT, "subject": "tb2-header", "verdict": "cases"})
    (d / LEDGER).write_text(json.dumps(doc, indent=1, sort_keys=False) + "\n")


def probe(d: Path, work: Path) -> str:
    p = subprocess.run([sys.executable, "-I", "-B", str(d / "plans/round95_vuln_probe.py"), "--lane", str(d),
                        "--work", str(work)], capture_output=True, text=True, timeout=1800)
    return p.stdout


def counter(d: Path, rev: str, work: Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-I", "-B", str(d / "plans/round95_c1_replay.py"), "--lane", str(d),
                        "--rev", rev, "--work", str(work)], capture_output=True, text=True, timeout=3600)
    return p.returncode, p.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    s = Path(a.scratch).resolve()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    d = s / "clone"
    if d.exists():
        shutil.rmtree(d)
    subprocess.run(["git", "clone", "-q", "--shared", a.lane, str(d)], check=True)
    git(d, "checkout", "-q", "--detach", a.base_rev)
    rows = "\n".join(f"{hashlib.sha256((d / p).read_bytes()).hexdigest()}  {p}" for p in INSTRUMENTS)
    (d / "plans/round-95-claims.md").write_text(
        f"# DRAFT claims (controls fixture only; never in the lane)\n\n```frozen-instruments\n{rows}\n```\n")
    draft = commit(d, "fixture: draft claims")

    def honest_receipt(tip: str) -> str:
        r = probe(d, s / "probe")
        return r

    results = []

    def record(name: str, want_rc: int, want_fail: list[str], rev: str) -> None:
        rc, text = counter(d, rev, s / f"w-{name}")
        legs = dict(re.findall(r"(L\d)=(pass|fail)", text))
        failed = sorted(k for k, v in legs.items() if v == "fail")
        ok = rc == want_rc and all(x in failed for x in want_fail) and (want_rc != 0 or not failed)
        (out / f"c1-{name}.txt").write_text(f"# control {name} at scratch rev {rev} (draft claims {draft[:12]}, base {a.base_rev[:12]})\n"
                                           f"# want rc={want_rc} failing legs include {want_fail or '-'}\n{text}rc={rc}\n")
        results.append(f"{name} rc={rc} want_rc={want_rc} failed={','.join(failed) or '-'} want_fail={','.join(want_fail) or '-'} {'OK' if ok else 'UNEXPECTED'}")
        git(d, "checkout", "-q", "--detach", draft)

    # pos: honest receipt + flip with legacy fields
    receipt = probe(d, s / "probe")
    (d / RECEIPT).write_text(receipt)
    flip(d, legacy=True)
    pos = commit(d, "fixture: honest receipt and flip")
    record("pos", 0, [], pos)

    # D4 probe swap with regenerated receipt
    (d / "plans/round95_vuln_probe.py").write_text(STUB)
    (d / RECEIPT).write_text(probe(d, s / "probe-stub"))
    flip(d, legacy=True)
    record("D4-probe-swap", 1, ["L8"], commit(d, "fixture: probe swapped"))

    # D5 foreign LANE_TIP
    git(d, "checkout", "-q", "--orphan", "foreign")
    foreign = commit(d, "fixture: foreign orphan")
    git(d, "checkout", "-q", "--detach", draft)
    (d / RECEIPT).write_text(re.sub(r"^LANE_TIP .*$", f"LANE_TIP {foreign}", receipt, flags=re.M))
    flip(d, legacy=True)
    record("D5-foreign-lane-tip", 1, ["L3"], commit(d, "fixture: foreign tip"))

    # D6 cases dropped
    (d / RECEIPT).write_text(re.sub(r"^CASE C0[234] .*\n", "", receipt, flags=re.M))
    flip(d, legacy=True)
    record("D6-cases-dropped", 1, ["L5", "L6"], commit(d, "fixture: cases dropped"))

    # D7 stamp forged
    (d / RECEIPT).write_text(re.sub(r"^VULNERABLE_BOTTLE_SHA .*$", "VULNERABLE_BOTTLE_SHA " + "0" * 64, receipt, flags=re.M))
    flip(d, legacy=True)
    record("D7-stamp-forged", 1, ["L6"], commit(d, "fixture: stamp forged"))

    # D8 legacy fields omitted
    (d / RECEIPT).write_text(receipt)
    flip(d, legacy=False)
    record("D8-legacy-fields-omitted", 1, ["L7"], commit(d, "fixture: legacy fields omitted"))

    (out / "c1-receipt-side-summary.txt").write_text("\n".join(results) + "\n")
    print("\n".join(results))
    shutil.rmtree(s, ignore_errors=True)
    return 0 if all(r.endswith("OK") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
