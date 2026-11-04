#!/usr/bin/env python3
"""R77 evidence driver — re-mint a round-76 battery receipt with a `TOOL_SHA` stamp.

Why: the round-76 closure (R76-V1) routed two C1 battery receipts that stamped a `LANE_TIP` whose
tree did not yet carry the battery they measured. The repair is not a prose correction: the receipt
must name (a) the revision it was produced at and (b) the exact tool bytes that produced it, so a
reader can recompute `git show <tip>:<tool> | sha256sum` and compare. The round-76 counter stamps only
`LANE_TIP`; changing it would rewrite a frozen instrument, so the stamp is added here by a committed
driver instead of by hand.

    python3 plans/round77_remint_r76_batteries.py --lane . \\
        --receipt corpus/evidence/round76/c1-selftest.txt \\
        --tool plans/round76_c1_surface_resolver.py -- --selftest

The driver runs the tool with `--receipt <tmp>` (the tool's own writer), then writes the final
receipt as `LANE_TIP`, `TOOL_SHA`, `WORKTREE`, `MINTED_BY` (this driver + its own sha256), followed
by the tool's bytes verbatim. Nothing else is edited.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


def git(lane: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)
    return proc.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True, help="Final receipt path (lane-relative)")
    ap.add_argument("--tool", type=Path, required=True, help="Tool whose sha256 is stamped")
    ap.add_argument("--work", type=Path, default=None, help="Scratch dir for the battery")
    ap.add_argument("--plain", action="store_true", help="Tool has no --receipt: capture stdout")
    ap.add_argument("toolargs", nargs=argparse.REMAINDER, help="-- <tool flags>")
    args = ap.parse_args()
    lane = args.lane.resolve()
    tool = (lane / args.tool).resolve()
    if not tool.exists():
        print(f"SETUP tool missing: {tool}")
        return 2
    toolargs = [a for a in args.toolargs if a != "--"]
    tip = git(lane, "rev-parse", "refs/heads/master") or git(lane, "rev-parse", "HEAD")
    dirty = bool(git(lane, "status", "--porcelain", "--untracked-files=no"))
    work = args.work or Path(tempfile.mkdtemp(prefix="r77-remint-", dir="/fast/scratch/hyaku"))
    work.mkdir(parents=True, exist_ok=True)
    tmp = work / (args.receipt.name + ".tool")
    if args.plain:
        cmd = [sys.executable, str(tool), *toolargs]
    else:
        cmd = [sys.executable, str(tool), "--lane", str(lane), "--work", str(work),
               "--receipt", str(tmp), *toolargs]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    if proc.returncode not in (0, 1):
        print(f"SETUP tool exited {proc.returncode}: {proc.stderr.strip()[:400]}")
        return 2
    if args.plain:
        body = proc.stdout + ("\n" + proc.stderr if proc.stderr.strip() else "")
    else:
        body = tmp.read_text() if tmp.exists() else ""
    header = [
        f"LANE_TIP {tip}",
        f"TOOL_SHA {hashlib.sha256(tool.read_bytes()).hexdigest()}",
        f"TOOL {args.tool}",
        f"WORKTREE {'dirty' if dirty else 'clean'}",
        f"MINTED_BY plans/round77_remint_r76_batteries.py sha256="
        f"{hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}",
        f"COMMAND {' '.join(cmd)}",
    ]
    out = lane / args.receipt
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(header) + "\n" + body.rstrip("\n") + f"\nEXIT {proc.returncode}\n")
    print(f"REMINT {args.receipt} tip={tip[:8]} tool_sha={header[1].split()[1][:12]} rc={proc.returncode}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
