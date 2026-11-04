#!/usr/bin/env python3
"""R81 receipt stamper — run a command and write its stdout under a locating stamp.

The round-80 spot-check's R79-V6 class: an "after" receipt without `LANE_TIP`/`WORKTREE`/`COMMAND`/
`EXIT` cannot say which tree it measured. Round 81's gate receipts carry the stamp; the gate's own
stdout follows verbatim so a reader can diff the counter's output.

    python3 plans/round81_stamp.py --lane DIR --receipt OUT -- python3 plans/x.py --lane .

Exit: the wrapped command's exit code (0/1) with `EXIT <n>` recorded in the receipt; 2 setup.
"""
from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                          text=True).stdout.strip()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--label", default=None)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        print("SETUP no command", file=sys.stderr)
        return 2
    lane = Path(a.lane).resolve()
    tip = git(lane, "rev-parse", "HEAD")
    if not tip:
        print("SETUP unresolved HEAD", file=sys.stderr)
        return 2
    dirty = git(lane, "status", "--porcelain")
    worktree = "clean" if not dirty else f"dirty ({len(dirty.splitlines())} paths)"
    proc = subprocess.run(cmd, cwd=str(lane), capture_output=True, text=True)
    head = [f"# {a.label or Path(a.receipt).name}",
            f"LANE_TIP {tip}",
            f"WORKTREE {worktree}",
            f"COMMAND {shlex.join(cmd)}",
            f"EXIT {proc.returncode}",
            "--- stdout ---"]
    body = proc.stdout.rstrip("\n")
    err = proc.stderr.strip()
    text = "\n".join(head) + "\n" + body + "\n"
    if err:
        text += "--- stderr ---\n" + err + "\n"
    out = Path(a.receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(text, end="")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
