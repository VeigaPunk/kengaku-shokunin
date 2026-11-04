#!/usr/bin/env python3
"""Probe the exact Q13 evidence contract of plans/gate_timing_check.py.

Builds one throwaway fixture repository and runs the real checker over eight
commits. Each commit changes exactly one condition, so the printed reason names
the failing rule:

  1. w1 citation of a .md report (round-84 seat-layout directory);
  2. falsify citation, no registry;
  3. falsify report carrying `writer: <candidate writer>`;
  4. falsify report naming only the short candidate name;
  5. falsify report without an anchored VERDICT line;
  6. good falsify report, entry has the line-start `writer:` field;
  7. good falsify report, entry has no `writer:` line;
  8. repair simulation: repaired recheck + writer line + good report.

6 and 8 are the shapes a round-84 admission must publish under the unchanged
checker; 1-5 and 7 are traps that must not be mistaken for it.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CHECKER = LANE / "plans/gate_timing_check.py"
CANDIDATE = "corpus/knowledge/tb2-code-from-image-offline.md"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
BASE_REV = "4087b2f8369fb0c317a8460725a607681ff2fd7f"

BASE = subprocess.run(
    ["git", "-C", str(LANE), "show", f"{BASE_REV}:{CANDIDATE}"],
    capture_output=True, text=True, check=True).stdout

WITH_WRITER = BASE.replace(
    "recheck: python3 plans/round83_c1_replay.py --lane . --work DIR",
    "recheck: python3 plans/round83_c1_replay.py --lane . --work DIR\nwriter: KengakuR84")

REPAIRED = BASE.replace(
    "recheck: python3 plans/round83_c1_replay.py --lane . --work DIR",
    f"recheck: re-run python3 plans/round84_c2_admission.py --lane . --work DIR --rev {PIN} "
    "on 2026-12-04; cadence weekly\nwriter: KengakuR84")

GOOD_REPORT = (
    "harness: outside re-read\n"
    "re-read-by: ReviewerR84\n"
    f"candidate: {CANDIDATE}\n"
    f"candidate mention: {CANDIDATE} lines 1-3 re-read\n"
    "VERDICT: agree\n"
)
TRAP_WRITER = (
    "re-read-by: ReviewerR84\n"
    f"candidate: {CANDIDATE}\n"
    "writer: KengakuR84\n"
    "VERDICT: agree\n"
)
TRAP_SHORT = (
    "re-read-by: ReviewerR84\n"
    "candidate: tb2-code-from-image-offline\n"
    "VERDICT: agree\n"
)
TRAP_NOVERDICT = (
    "re-read-by: ReviewerR84\n"
    f"candidate: {CANDIDATE}\n"
    "agreed with the entry, no verdict line\n"
)
REGISTRY = (
    '{"members": {"ReviewerR84": {"role": "reviewer", '
    '"agentId": "KengakuR84.ReviewerR84"}}}\n'
)
REPORT_PATH = ".ufo/waves/round-84/falsify/ReviewerR84.md"
REGISTRY_PATH = ".ufo/waves/round-84/falsify/swarm-registry.json"


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, capture_output=True, text=True, check=False)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(repo, "git", "-C", str(repo), *args)


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def remove(repo: Path, rel: str) -> None:
    path = repo / rel
    if path.exists():
        path.unlink()


def gate(cite: str) -> str:
    return (
        "# Round 84 fixture lesson\n\n## Gate\n\n"
        "| candidate | decision | reason |\n|---|---|---|\n"
        f"| `{CANDIDATE}` | admit | second-seat re-read at `{cite}` |\n"
    )


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    result = git(repo, "-c", "user.name=AdmitR84 Probe", "-c",
                 "user.email=admitr84-probe@example.invalid", "-c", "commit.gpgsign=false",
                 "commit", "-q", "-m", message)
    if result.returncode:
        raise SystemExit(f"commit failed: {result.stderr}")
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def check(repo: Path, rev: str) -> subprocess.CompletedProcess[str]:
    return run(repo, sys.executable, str(CHECKER), "--lesson", "corpus/lessons/round-84.md",
               "--commit", rev, "--repo", str(repo))


def show(label: str, result: subprocess.CompletedProcess[str]) -> None:
    print(f"\n=== {label} === exit={result.returncode}")
    for line in (result.stdout + result.stderr).splitlines():
        if line.strip():
            print("  " + line)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="admitr84-contract-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q")
        if git(repo, "rev-parse", "--show-toplevel").stdout.strip() != str(repo):
            print("FATAL fixture top-level mismatch")
            return 2
        write(repo, CANDIDATE, WITH_WRITER)

        # 1. w1 .md report + w1 registry.
        write(repo, ".ufo/waves/round-84/w1/ReviewerR84.md", GOOD_REPORT)
        write(repo, ".ufo/waves/round-84/w1/swarm-registry.json", REGISTRY)
        write(repo, "corpus/lessons/round-84.md", gate(".ufo/waves/round-84/w1/ReviewerR84.md"))
        show("1 w1 .md report", check(repo, commit(repo, "w1 report")))
        remove(repo, ".ufo/waves/round-84/w1/ReviewerR84.md")
        remove(repo, ".ufo/waves/round-84/w1/swarm-registry.json")

        # 2. falsify citation, no registry.
        write(repo, REPORT_PATH, GOOD_REPORT)
        write(repo, "corpus/lessons/round-84.md", gate(REPORT_PATH))
        show("2 falsify report, no registry", check(repo, commit(repo, "no registry")))

        # 3. report declares the candidate writer.
        write(repo, REGISTRY_PATH, REGISTRY)
        write(repo, REPORT_PATH, TRAP_WRITER)
        show("3 report says writer: KengakuR84", check(repo, commit(repo, "trap writer")))

        # 4. report names only the short candidate name.
        write(repo, REPORT_PATH, TRAP_SHORT)
        show("4 report names short candidate only", check(repo, commit(repo, "trap short")))

        # 5. report without VERDICT.
        write(repo, REPORT_PATH, TRAP_NOVERDICT)
        show("5 report without VERDICT", check(repo, commit(repo, "trap verdict")))

        # 6. good report, entry with writer line.
        write(repo, REPORT_PATH, GOOD_REPORT)
        show("6 good report, entry writer present", check(repo, commit(repo, "good")))

        # 7. good report, entry without writer line.
        write(repo, CANDIDATE, BASE)
        show("7 good report, entry writer absent", check(repo, commit(repo, "no entry writer")))

        # 8. repair simulation.
        write(repo, CANDIDATE, REPAIRED)
        show("8 repair simulation", check(repo, commit(repo, "repaired entry")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
