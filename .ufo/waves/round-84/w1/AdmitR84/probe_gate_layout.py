#!/usr/bin/env python3
"""Probe how plans/gate_timing_check.py treats round-84 wave layouts.

Read-only against the lane. Builds a throwaway fixture repository in TMPDIR and
runs the real checker four times:

  1. Gate cites .ufo/waves/round-84/w1/ReviewerW1.md with a w1 registry;
  2. Gate cites .ufo/waves/round-84/falsify/ReviewerF.md with a falsify registry;
  3. Gate cites .ufo/waves/round-84/falsify/ReviewerF.md with no registry;
  4. Gate cites .ufo/waves/round-84/w1/ReviewerW1/report.txt (a .txt report).

The point is to record, not to change, the checker's directory contract.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CHECKER = LANE / "plans/gate_timing_check.py"
CANDIDATE = "corpus/knowledge/tb2-code-from-image-offline.md"

ENTRY = (
    "source: S000 - https://example.invalid/example.py\n"
    "verified-at: 2026-11-04\n"
    "recheck: re-run python3 plans/fixture.py --lane . on 2027-01-04; cadence monthly; "
    "pin nothing\n"
    "writer: FixtureWriter\n"
    "# fixture entry\n"
)

REPORT = f"Re-read {CANDIDATE}\nVERDICT: PASS\n"


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=False,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(repo, "git", "-C", str(repo), *args)


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    result = git(repo, "-c", "user.name=AdmitR84 Probe", "-c",
                 "user.email=admitr84-probe@example.invalid", "-c", "commit.gpgsign=false",
                 "commit", "-q", "-m", message)
    if result.returncode:
        raise SystemExit(f"commit failed: {result.stderr}")
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def gate(lesson: Path, cite: str) -> str:
    return (
        "# Round 84 fixture lesson\n\n## Gate\n\n"
        "| candidate | decision | reason |\n|---|---|---|\n"
        f"| `{CANDIDATE}` | admit | re-read by `{cite}` |\n"
    )


def registry(role: str, agent: str) -> str:
    return (
        '{"members": {"ReviewerW1": {"role": "%s", "agentId": "%s"},'
        ' "ReviewerF": {"role": "%s", "agentId": "%s"}}}\n'
        % (role, agent, role, agent)
    )


def check(repo: Path, rev: str) -> subprocess.CompletedProcess[str]:
    return run(repo, sys.executable, str(CHECKER), "--lesson", "corpus/lessons/round-84.md",
               "--commit", rev, "--repo", str(repo))


def show(label: str, result: subprocess.CompletedProcess[str]) -> None:
    print(f"\n=== {label} === exit={result.returncode}")
    for line in (result.stdout + result.stderr).splitlines():
        if line.strip():
            print("  " + line)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="admitr84-gate-layout-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
        if top != str(repo):
            print(f"FATAL top-level {top!r} != {repo!s}")
            return 2
        write(repo, CANDIDATE, ENTRY)

        # 1. w1 layout with a w1 registry and a .md report inside w1.
        write(repo, ".ufo/waves/round-84/w1/ReviewerW1.md", REPORT)
        write(repo, ".ufo/waves/round-84/w1/swarm-registry.json",
              registry("reviewer", "Round84.ReviewerW1"))
        write(repo, "corpus/lessons/round-84.md",
              gate(repo / "corpus/lessons/round-84.md",
                   ".ufo/waves/round-84/w1/ReviewerW1.md"))
        rev_w1 = commit(repo, "w1 layout")
        show("w1 citation (.md, w1 registry)", check(repo, rev_w1))

        # 2. falsify layout with a falsify registry.
        write(repo, ".ufo/waves/round-84/falsify/ReviewerF.md",
              REPORT.replace("Re-read", "Re-read"))
        write(repo, ".ufo/waves/round-84/falsify/swarm-registry.json",
              registry("reviewer", "Round84.ReviewerF"))
        write(repo, "corpus/lessons/round-84.md",
              gate(repo / "corpus/lessons/round-84.md",
                   ".ufo/waves/round-84/falsify/ReviewerF.md"))
        rev_f = commit(repo, "falsify layout")
        show("falsify citation + falsify registry", check(repo, rev_f))

        # 3. Same citation, registry removed.
        git(repo, "rm", "-q", ".ufo/waves/round-84/falsify/swarm-registry.json")
        rev_noreg = commit(repo, "falsify layout, no registry")
        show("falsify citation, registry absent", check(repo, rev_noreg))

        # 4. w1 directory holding a report.txt (the round-84 seat output shape).
        write(repo, ".ufo/waves/round-84/w1/ReviewerW1/report.txt", REPORT)
        write(repo, ".ufo/waves/round-84/falsify/swarm-registry.json",
              registry("reviewer", "Round84.ReviewerF"))
        write(repo, "corpus/lessons/round-84.md",
              gate(repo / "corpus/lessons/round-84.md",
                   ".ufo/waves/round-84/w1/ReviewerW1/report.txt"))
        rev_txt = commit(repo, "w1 report.txt citation")
        show("w1 report.txt citation", check(repo, rev_txt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
