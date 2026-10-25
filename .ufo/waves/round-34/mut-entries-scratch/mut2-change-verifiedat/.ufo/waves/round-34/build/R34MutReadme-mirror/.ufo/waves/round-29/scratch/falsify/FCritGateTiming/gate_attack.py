#!/usr/bin/env python3
"""Run the unchanged lane gate_timing_check.py against synthetic round-29 admitting trees.

Every repository is created under /tmp; the lane repo is only read (draft bytes,
falsify registry, checker path). Output: one JSON line per scenario.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CHECKER = LANE / "plans/gate_timing_check.py"
DRAFT = LANE / ".ufo/waves/round-29/drafts/webarena-config-projection.md"
REGISTRY = LANE / ".ufo/waves/round-29/falsify/swarm-registry.json"
CANON = "corpus/knowledge/webarena-config-projection.md"
FROZEN = "7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc"
F = ".ufo/waves/round-29/falsify"

ENV = {"PATH": os.environ.get("PATH", os.defpath), "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": os.devnull, "PYTHONDONTWRITEBYTECODE": "1"}


def report(seat: str, verdict: str = "PASS", names: str = CANON, extra: str = "") -> str:
    return (f"writer: KengakuR29-2.{seat}-2\n# {seat}\nReviewed {names} sha256 {FROZEN}.\n"
            f"{extra}VERDICT: {verdict}\n")


def base_files() -> dict[str, bytes | None]:
    return {
        CANON: DRAFT.read_bytes(),
        f"{F}/swarm-registry.json": REGISTRY.read_bytes(),
        f"{F}/FEntryNumbers.md": report("FEntryNumbers").encode(),
        f"{F}/FEntrySources.md": report("FEntrySources").encode(),
        f"{F}/FOracleText.md": report("FOracleText").encode(),
        f"{F}/FMutUrlOnly.md": report("FMutUrlOnly").encode(),
        ".ufo/waves/round-29/build/R29DraftEntry.md": b"writer: R29DraftEntry\nVERDICT: PASS\n",
    }


GOOD = f"Returned `{F}/FEntryNumbers.md` and `{F}/FEntrySources.md` on {FROZEN}."


def lesson(reason: str = GOOD, candidate: str = "`knowledge/webarena-config-projection.md`",
           decision: str = "admit", heading: str = "## Gate", header: str = "| candidate | decision | reason |",
           extra_rows: str = "") -> bytes:
    return (f"# Round 29 — sandbox\n\n{heading}\n\n{header}\n|---|---|---|\n"
            f"| {candidate} | {decision} | {reason} |\n{extra_rows}").encode()


def scenarios():
    yield "A green: two eligible full-path reports", {}, lesson()
    yield "B cited report VERDICT: FAIL", {f"{F}/FEntryNumbers.md": report("FEntryNumbers", "FAIL").encode()}, lesson()
    yield "B2 cited report VERDICT: PARTIAL", {f"{F}/FEntrySources.md": report("FEntrySources", "PARTIAL").encode()}, lesson()
    yield "C plus executor oracle FOracleText", {}, lesson(GOOD + f" Oracle `{F}/FOracleText.md`.")
    yield "D plus mutation-tester FMutUrlOnly", {}, lesson(GOOD + f" Witness `{F}/FMutUrlOnly.md`.")
    yield "E bare SOURCES.md in reason", {}, lesson(GOOD + " S070–S073 used-by updated in SOURCES.md.")
    yield "E2 path corpus/SOURCES.md in reason", {}, lesson(GOOD + " S070–S073 used-by updated in `corpus/SOURCES.md`.")
    yield "E3 bare README.md index row", {}, lesson(GOOD + " Index row added to README.md.")
    yield "E4 bare SOURCES.md mid-sentence", {}, lesson(GOOD + " SOURCES.md used-by cells updated")
    yield "E5 backticked `README.md` index row", {}, lesson(GOOD + " Index row added to `README.md`")
    yield "E6 bare SCORECARD.md mid-sentence", {}, lesson(GOOD + " SCORECARD.md capability row follows")
    yield "F 'second seat' with space", {}, lesson(GOOD + " Complete second seat re-reads.")
    yield "F2 'second-seat' hyphen", {}, lesson(GOOD + " Complete second-seat re-reads.")
    yield "F3 'falsify reports'", {}, lesson(GOOD + " Other falsify reports are advice.")
    yield "G report names only drafts path", {f"{F}/FEntrySources.md": report(
        "FEntrySources", names=".ufo/waves/round-29/drafts/webarena-config-projection.md").encode()}, lesson()
    yield "H falsify registry not committed", {f"{F}/swarm-registry.json": None}, lesson()
    yield "I report quotes candidate writer line at column 0", {f"{F}/FEntryNumbers.md": report(
        "FEntryNumbers", extra="Candidate header:\nwriter: KengakuR29-2\n").encode()}, lesson()
    yield "J extra admit row for source rows", {}, lesson(extra_rows="| S070–S073 | admit | opened this round |\n")
    yield "K decision 'admit-pending'", {}, lesson(decision="admit-pending", reason="awaiting rereads by `falsify/FEntryNumbers.md`")
    yield "L entry bytes differ from frozen 7006b93 digest", {CANON: DRAFT.read_bytes() + b"\nedited after review\n"}, lesson()
    yield "M corpus-prefixed candidate, report omits corpus/", {f"{F}/FEntrySources.md": report(
        "FEntrySources", names="knowledge/webarena-config-projection.md").encode()}, lesson(
        candidate="`corpus/knowledge/webarena-config-projection.md`")
    yield "N heading-form verdict (r28 M85 repeat)", {f"{F}/FEntryNumbers.md": (
        report("FEntryNumbers").replace("VERDICT: PASS\n", "## VERDICT: PASS\n")).encode()}, lesson()
    yield "P admission table under non-Gate H2", {}, lesson(heading="## Admission decision")
    yield "P2 reason column named 'rationale'", {}, lesson(header="| candidate | decision | rationale |")
    yield "R plus build scribe citation", {}, lesson(GOOD + " Draft origin `build/R29DraftEntry.md`.")
    yield "U relative and bare forms", {}, lesson("Returned `falsify/FEntryNumbers.md` and `FEntrySources.md`.")
    yield "V candidate entry absent from tree", {CANON: None}, lesson()


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-c", "commit.gpgSign=false", "-c", f"core.hooksPath={os.devnull}",
                           "-C", str(repo), *args], capture_output=True, text=True, env=ENV, check=True)


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="fcrit-gate-timing-", dir="/tmp"))
    rows = []
    for label, overrides, lesson_bytes in scenarios():
        repo = root / f"s{len(rows):02d}"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.name", "FCritGateTiming sandbox")
        git(repo, "config", "user.email", "sandbox@example.invalid")
        files = base_files()
        files.update(overrides)
        files["corpus/lessons/round-29.md"] = lesson_bytes
        for rel, data in files.items():
            if data is None:
                continue
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", label)
        commit = git(repo, "rev-parse", "HEAD").stdout.strip()
        result = subprocess.run([sys.executable, str(CHECKER), "--lesson", "corpus/lessons/round-29.md",
                                 "--commit", commit, "--repo", str(repo)],
                                capture_output=True, text=True, env=ENV)
        detail = [line.strip() for line in result.stdout.splitlines()
                  if line.lstrip().startswith(("invalid", "unresolved", "generic", "reasons", "existing", "gate_timing_check:"))]
        rows.append({"scenario": label, "exit": result.returncode, "detail": detail,
                     "stderr": result.stderr.strip()[:200]})
        print(json.dumps(rows[-1], ensure_ascii=False))
    shutil.rmtree(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
