#!/usr/bin/env python3
"""R78-C2 repair driver — re-mint a receipt so its own bytes locate it (R78-C2).

Why: the round-77 closure routed receipts that stamped a `LANE_TIP` whose tree could not produce
their verdict (D1/D2), receipts whose `TOOL_SHA` named no tool (D5), and receipts with no command a
reader could re-run. R78-C2 prices that class; this driver is the repair it demands, and it never
edits a frozen instrument: it runs the tool's own writer and stamps the result.

Two modes (spec `plans/round78-restamp.json`):

  rerun   run the tool at the current clean tip and write a fully located receipt:
          `LANE_TIP` `TOOL` `TOOL_SHA` `WORKTREE` `COMMAND` `MINTED_BY` `EXIT`, then the tool's
          verdict bytes (the tool's own leading stamp lines are stripped so exactly one stamp
          block governs the receipt).
  retag   append a `## Re-stamp (round 78)` block to a historical receipt whose numbers are kept:
          the historical `LANE_TIP` is repeated, `WORKTREE dirty`, and either `TOOL`/`TOOL_SHA`
          (the tool bytes present in that tree, digest recomputed there) or `TOOL-SUPPLIED`
          (the tool did not exist at that revision and was supplied untracked).

    python3 plans/round78_restamp.py --lane . --spec plans/round78-restamp.json
    python3 plans/round78_restamp.py --lane . --spec plans/round78-restamp.json --only c1-selftest.txt
Exit 0 every entry applied and every receipt still parses; 2 setup; 3 a tool run failed.
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

STAMP_HEAD = re.compile(r"^(LANE_TIP|WORKTREE|TOOL|TOOL_SHA|COMMAND|MINTED_BY|EXIT) ")
TIP_LINE = re.compile(r"^LANE_TIP ([0-9a-f]{7,40})$", re.M)


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


def sha_at(lane: Path, tip: str, rel: str) -> str | None:
    proc = git(lane, "cat-file", "-p", f"{tip}:{rel}")
    if proc.returncode != 0:
        return None
    return hashlib.sha256(proc.stdout.encode("utf-8", "surrogateescape")).hexdigest()


def strip_stamp_head(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        if STAMP_HEAD.match(line):
            continue
        out.append(line)
    return "\n".join(out).lstrip("\n")


def apply_rerun(lane: Path, entry: dict, work: Path) -> tuple[bool, str]:
    tool = entry["tool"]
    tip = git(lane, "rev-parse", "master").stdout.strip()
    digest = sha_at(lane, tip, tool)
    if digest is None:
        return False, f"SETUP tool not in the tip tree: {tool}"
    receipt = lane / entry["receipt"]
    argv = entry.get("argv", [])
    env_cmd = [sys.executable, str(lane / tool)]
    if entry.get("mode", "receipt") == "receipt":
        tmp = work / (receipt.name + ".tool")
        if tmp.exists():
            tmp.unlink()
        cmd = env_cmd + ["--lane", str(lane), "--work", str(work), "--receipt", str(tmp)] + argv
    else:
        cmd = env_cmd + argv
    proc = subprocess.run(cmd, cwd=str(lane), capture_output=True, text=True)
    if entry.get("mode", "receipt") == "receipt":
        body = tmp.read_text(encoding="utf-8") if tmp.exists() else proc.stdout
    else:
        body = proc.stdout
    if not body.strip():
        return False, f"no output for {entry['receipt']} (rc={proc.returncode})"
    head = (f"LANE_TIP {tip}\nTOOL {tool}\nTOOL_SHA {digest}\nWORKTREE clean\n"
            f"COMMAND {' '.join(shlex.quote(a) for a in cmd)}\n"
            f"MINTED_BY plans/round78_restamp.py sha256={sha_at(lane, tip, 'plans/round78_restamp.py') or '-'}\n"
            f"EXIT {proc.returncode}\n")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(head + strip_stamp_head(body).rstrip("\n") + "\n", encoding="utf-8")
    return proc.returncode == 0, f"rerun rc={proc.returncode} {entry['receipt']}"


def apply_retag(lane: Path, entry: dict) -> tuple[bool, str]:
    receipt = lane / entry["receipt"]
    if not receipt.exists():
        return False, f"SETUP missing receipt {entry['receipt']}"
    text = receipt.read_text(encoding="utf-8")
    m = TIP_LINE.search(text)
    if not m:
        return False, f"SETUP no LANE_TIP in {entry['receipt']}"
    tip = m.group(1)
    if tip != entry["tip"]:
        return False, f"SETUP tip mismatch {entry['receipt']}: file {tip} spec {entry['tip']}"
    lines = [f"## Re-stamp (round 78, R78-C2) — the receipt's numbers are unchanged", f"LANE_TIP {tip}"]
    tool = entry["tool"]
    digest = sha_at(lane, tip, tool)
    if digest is None:
        lines.append(f"TOOL-SUPPLIED {tool}")
        lines.append("WORKTREE dirty")
        lines.append(f"NOTE the tool did not exist at {tip[:8]}; it was supplied untracked, so the "
                     f"`WORKTREE clean` line above was wrong")
    else:
        lines.append(f"TOOL {tool}")
        lines.append(f"TOOL_SHA {digest}")
        lines.append(f"WORKTREE {entry.get('worktree', 'dirty')}")
    lines.append(f"COMMAND {entry['command']}")
    lines.append(f"RE-STAMPED 2026-11-04 by KengakuR78 (plans/round78_restamp.py)")
    block = "\n" + "\n".join(lines) + "\n"
    if "## Re-stamp (round 78, R78-C2)" in text:
        return True, f"retag already present {entry['receipt']}"
    receipt.write_text(text.rstrip("\n") + "\n" + block, encoding="utf-8")
    return True, f"retag {entry['receipt']}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", type=Path, required=True)
    ap.add_argument("--spec", type=Path, required=True)
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--only", default="")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    lane = args.lane.resolve()
    spec = json.loads((lane / args.spec).read_text(encoding="utf-8"))
    work = args.work or Path("/fast/scratch/hyaku/kengaku-r78/restamp")
    work.mkdir(parents=True, exist_ok=True)
    rc_all = 0
    for entry in spec.get("rerun", []):
        if args.only and args.only not in entry["receipt"]:
            continue
        if args.dry:
            print(f"DRY rerun {entry['receipt']} tool={entry['tool']} argv={entry.get('argv')}")
            continue
        ok, msg = apply_rerun(lane, entry, work)
        print(("OK   " if ok else "FAIL ") + msg)
        if not ok:
            rc_all = 3
    for entry in spec.get("retag", []):
        if args.only and args.only not in entry["receipt"]:
            continue
        if args.dry:
            print(f"DRY retag {entry['receipt']} tip={entry['tip'][:8]}")
            continue
        ok, msg = apply_retag(lane, entry)
        print(("OK   " if ok else "FAIL ") + msg)
        if not ok:
            rc_all = rc_all or 2
    return rc_all


if __name__ == "__main__":
    sys.exit(main())
