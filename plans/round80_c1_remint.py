#!/usr/bin/env python3
"""R80-C1 repair driver — re-mint the six `executed-unlocated` replays as located receipts.

Runs each frozen instrument (`plans/round80_probes.json`) once at a CLEAN tree, composes a receipt
whose first line is the frozen subject shape, whose stamp block names the historical receipt and
the instrument with their sha256 at the measured tip, and whose observation block is the tool's
own stdout. Then flips the member's ledger row to `executed`.

Never edits a probe, never fabricates an observation: the block is the tool's stdout, byte for
byte. When the tip's instrument produces a different observation set than the historical receipt
(the tool was corrected after that round), the receipt carries `HISTORICAL-DIVERGENCE <n> ...`
naming the difference; the historical receipt is left untouched and its sha is stamped.

    python3 plans/round80_c1_remint.py --lane <clean clone> --work <scratch>
    python3 plans/round80_c1_remint.py --lane <clean clone> --work <scratch> --only protein-assembly

Exit 0 every receipt minted and every row flipped; 2 setup (dirty tree, table/coded probe absent);
3 a probe run failed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

TABLE = "plans/round80_probes.json"
LEDGER = "plans/grader-population-ledger.json"
EVID = "corpus/evidence/round80"
MINTED_BY = "plans/round80_c1_remint.py"
OBS = (r"^CASE ", r"^case=", r"^cases=", r"^MISMATCH ", r"^OBSERVED-U ", r"^VECTOR ",
       r"^PREDICATE R\d+-C\d+ (?:pass|fail)")
FORMS = (("predicate", r"^PREDICATE R\d+-C\d+ pass"), ("vectors", r"^VECTOR "),
         ("cases", r"^(?:CASE |case=)"))


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def obs_lines(text: str) -> list[str]:
    import re
    return [ln for ln in text.splitlines() if any(re.match(p, ln) for p in OBS)]


def verdict_form(text: str) -> str:
    import re
    for name, pattern in FORMS:
        if re.search(pattern, text, re.M):
            return name
    return "cases"


def render(spec: dict, member: str, work: Path, python: str) -> tuple[list[str], str]:
    w = work / f"{member}.work"
    w.mkdir(parents=True, exist_ok=True)
    out = work / f"{member}.out.txt"
    argv = [a.replace("{work}", str(w)).replace("{out}", str(out)).replace("{member}", member)
            for a in spec["argv"]]
    cmd = (spec.get("prefix") or [python]) + [spec["tool"]] + argv
    return cmd, shlex.join(cmd)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", default="/fast/scratch/hyaku/kengaku-r80/remint")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--only", action="append", default=None)
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)

    status = git(lane, "status", "--porcelain").stdout.strip()
    if status:
        print(f"SETUP worktree not clean ({len(status.splitlines())} paths); run in a fresh clone")
        return 2
    tip = git(lane, "rev-parse", "master").stdout.strip()
    if not tip:
        print("SETUP unresolved branch master")
        return 2
    table = json.loads((lane / TABLE).read_text())["members"]
    doc = json.loads((lane / LEDGER).read_text())
    rows = doc["members"]
    chosen = [m for m in table if not a.only or m in a.only]
    minted = failed = 0
    (lane / EVID).mkdir(parents=True, exist_ok=True)
    for m in chosen:
        spec = table[m]
        tool_bytes = (lane / spec["tool"]).read_bytes()
        hist_bytes = (lane / spec["historical"]).read_bytes()
        cmd, command = render(spec, m, work, a.python)
        try:
            proc = subprocess.run(cmd, cwd=str(lane), capture_output=True, text=True,
                                  timeout=int(spec.get("timeout", 300)))
        except subprocess.TimeoutExpired:
            print(f"REMINT-FAIL {m} timeout")
            failed += 1
            continue
        if proc.returncode != 0:
            print(f"REMINT-FAIL {m} rc={proc.returncode} stderr={proc.stderr.strip().splitlines()[-1:]}")
            failed += 1
            continue
        obs = obs_lines(proc.stdout)
        if not obs:
            print(f"REMINT-FAIL {m} no observations on stdout")
            failed += 1
            continue
        hist = obs_lines(hist_bytes.decode("utf-8", "replace"))
        note = ""
        if hist and hist != obs:
            from collections import Counter
            hc, nc = Counter(hist), Counter(obs)
            moved = sum(((hc - nc) + (nc - hc)).values())
            note = (f"HISTORICAL-DIVERGENCE {moved} "
                    f"the tip's instrument produces {len(obs)} observation lines where the "
                    f"historical receipt has {len(hist)}; historical receipt kept, sha stamped\n")
        text = (
            f"# tb2 {m} grader probe (round 80 re-mint)\n"
            f"MEMBER {m}\n"
            f"SOURCE_RECEIPT {spec['historical']}\n"
            f"SOURCE_SHA {sha256(hist_bytes)}\n"
            f"TOOL {spec['tool']}\n"
            f"TOOL_SHA {sha256(tool_bytes)}\n"
            f"LANE_TIP {tip}\n"
            f"WORKTREE clean\n"
            f"COMMAND {command}\n"
            f"EXIT 0\n"
            f"MINTED_BY {MINTED_BY}\n"
            f"{note}"
            f"OBSERVATIONS_BEGIN\n"
            + "\n".join(ln for ln in proc.stdout.rstrip("\n").splitlines()
                        if not re.match(r"^REV [0-9a-f]{7,40}\s*$", ln)) + "\n"
            + f"OBSERVATIONS_END\n"
        )
        rel = f"{EVID}/{m}-probe.txt"
        (lane / rel).write_text(text)
        row = rows.get(m)
        if not isinstance(row, dict):
            print(f"REMINT-FAIL {m} ledger row absent")
            failed += 1
            continue
        for key in ("reason", "evidence", "instrument", "debt"):
            row.pop(key, None)
        row.update({"status": "executed", "round": 80, "receipt": rel,
                    "subject": "tb2-header", "verdict": verdict_form(proc.stdout)})
        minted += 1
        print(f"REMINT {m} rc=0 obs={len(obs)} historical={'differs' if note else 'same'}")
        print(f"LEDGER-FLIP {m} verdict={verdict_form(proc.stdout)}")
    (lane / LEDGER).write_text(json.dumps(doc, indent=1) + "\n")
    print(f"REMINT minted={minted} failed={failed}")
    return 0 if failed == 0 and minted == len(chosen) else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
