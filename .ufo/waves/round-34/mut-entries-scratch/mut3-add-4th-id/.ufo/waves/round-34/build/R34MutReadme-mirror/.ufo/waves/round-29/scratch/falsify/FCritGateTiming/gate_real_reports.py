#!/usr/bin/env python3
"""Cite actual returned round-29 falsify report bytes in a /tmp admitting-tree sandbox."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
F = ".ufo/waves/round-29/falsify"
CANON = "corpus/knowledge/webarena-config-projection.md"
ENV = {"PATH": os.environ.get("PATH", os.defpath), "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_CONFIG_GLOBAL": os.devnull, "PYTHONDONTWRITEBYTECODE": "1"}
SEATS = sys.argv[1:] or ["FReopenS070", "FReopenS072", "FReopenS073"]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "commit.gpgSign=false", "-c", f"core.hooksPath={os.devnull}",
                           "-C", str(repo), *args], capture_output=True, text=True, env=ENV,
                          check=True).stdout


root = Path(tempfile.mkdtemp(prefix="fcrit-gate-real-", dir="/tmp"))
try:
    repo = root / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "FCritGateTiming sandbox")
    git(repo, "config", "user.email", "sandbox@example.invalid")
    copies = {CANON: LANE / ".ufo/waves/round-29/drafts/webarena-config-projection.md",
              f"{F}/swarm-registry.json": LANE / f"{F}/swarm-registry.json"}
    for seat in SEATS:
        copies[f"{F}/{seat}.md"] = LANE / f"{F}/{seat}.md"
    for rel, src in copies.items():
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    cites = " and ".join(f"`{F}/{seat}.md`" for seat in SEATS)
    (repo / "corpus/lessons").mkdir(parents=True, exist_ok=True)
    (repo / "corpus/lessons/round-29.md").write_text(
        "# Round 29 — sandbox\n\n## Gate\n\n| candidate | decision | reason |\n|---|---|---|\n"
        f"| `knowledge/webarena-config-projection.md` | admit | Source re-reads returned in {cites} |\n",
        encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "real-report sandbox")
    commit = git(repo, "rev-parse", "HEAD").strip()
    result = subprocess.run([sys.executable, str(LANE / "plans/gate_timing_check.py"), "--lesson",
                             "corpus/lessons/round-29.md", "--commit", commit, "--repo", str(repo)],
                            capture_output=True, text=True, env=ENV)
    print(json.dumps({"seats": SEATS, "source_sha256": {
        seat: subprocess.run(["sha256sum", str(LANE / f"{F}/{seat}.md")], capture_output=True,
                             text=True).stdout.split()[0] for seat in SEATS}}))
    sys.stdout.write(result.stdout.replace(commit, "<sandbox-commit>"))
    print(f"exit={result.returncode}")
finally:
    shutil.rmtree(root)
