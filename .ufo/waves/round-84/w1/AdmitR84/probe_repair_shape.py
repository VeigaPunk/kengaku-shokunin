#!/usr/bin/env python3
"""Probe the repaired-entry shape against the counter's own Q1/Q21 rules.

Part 1 varies only the recheck line and prints the counter's rule verdicts, so
the boundary is explicit (date alone, pin alone, pin+cadence escape, full line).
Part 2 builds a compliant end state (repaired recheck + writer line + corrected
falsify Gate + registry + report) and runs the counter's evaluate/emit path to
show it turning green.

No production file is touched; everything is written under the probe's TMPDIR.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
CANDIDATE = "corpus/knowledge/tb2-code-from-image-offline.md"
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"

spec = importlib.util.spec_from_file_location("admission", HERE / "round84_c2_admission.py")
admission = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = admission
spec.loader.exec_module(admission)

BASE = subprocess.run(
    ["git", "-C", str(LANE), "show", f"{admission.BASE}:{CANDIDATE}"],
    capture_output=True, text=True, check=True).stdout

VARIANTS = (
    ("command only (BASE)", "python3 plans/round83_c1_replay.py --lane . --work DIR"),
    ("date only", "python3 plans/round83_c1_replay.py --lane . --work DIR on 2026-12-04"),
    ("pin + date, no cadence",
     f"re-verify python3 plans/round84_c2_admission.py --lane . --work DIR --rev {PIN} "
     "on 2026-12-04"),
    ("re-pin cadence, no literal pin",
     "re-verify weekly and re-pin the source with python3 plans/round84_c2_admission.py "
     "--lane . --work DIR"),
    ("recommended full line",
     f"re-verify weekly against pinned source {PIN} with "
     "python3 plans/round84_c2_admission.py --lane . --work DIR; next review 2026-12-04"),
)

GATE = (
    "# Round 84 fixture lesson\n\n## Gate\n\n"
    "| candidate | decision | reason |\n|---|---|---|\n"
    f"| `{CANDIDATE}` | admit | second-seat re-read at "
    "`.ufo/waves/round-84/falsify/ReviewerR84.md` |\n"
)
REPORT = (
    "re-read-by: ReviewerR84\n"
    f"candidate: {CANDIDATE}\n"
    f"candidate mention: {CANDIDATE}\n"
    "VERDICT: agree\n"
)
REGISTRY = (
    '{"members": {"ReviewerR84": {"role": "reviewer", '
    '"agentId": "KengakuR84.ReviewerR84"}}}\n'
)


def entry_with(recheck: str) -> str:
    lines = BASE.splitlines()
    return "\n".join([lines[0], lines[1], f"recheck: {recheck}", "writer: KengakuR84",
                      *lines[3:]]) + "\n"


def main() -> int:
    print("== part 1: recheck-line rule boundary ==")
    for label, recheck in VARIANTS:
        entry = entry_with(recheck)
        q1, d1 = admission.check_q1(entry)
        q21, d21 = admission.check_q21(entry)
        print(f"VARIANT {label!r:44} q1={q1} ({d1}) q21={q21} ({d21})")

    print("\n== part 2: compliant end state through evaluate/emit ==")
    with tempfile.TemporaryDirectory(prefix="admitr84-repair-") as tmp:
        root = Path(tmp)
        repo = root / "repo"
        repo.mkdir()
        subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
        top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        if top != str(repo):
            print("FATAL fixture top-level mismatch")
            return 2
        files = {
            "plans/gate_timing_check.py": (LANE / "plans/gate_timing_check.py").read_text(),
            CANDIDATE: entry_with(VARIANTS[-1][1]),
            "corpus/lessons/round-84.md": GATE,
            ".ufo/waves/round-84/falsify/ReviewerR84.md": REPORT,
            ".ufo/waves/round-84/falsify/swarm-registry.json": REGISTRY,
        }
        for rel, text in files.items():
            path = repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=AdmitR84 Probe",
                        "-c", "user.email=admitr84-probe@example.invalid",
                        "-c", "commit.gpgsign=false", "commit", "-q", "-m", "repair"],
                       check=True)
        commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                capture_output=True, text=True, check=True).stdout.strip()
        clone = admission.ensure_clone(repo, root / "clone")
        verdict = admission.evaluate(files[CANDIDATE], files["corpus/lessons/round-84.md"],
                                     clone, commit, root)
        admission.emit(verdict)
        print(f"exit_path={'0' if verdict.defects == 0 else '1'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
