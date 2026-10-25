#!/usr/bin/env python3
"""Re-derive the five defect items round 29's non-author closure routed to this lane.

Round 30 (2026-10-25), claim C2. One command, one line: `defects=N`, exit 0 only
when every one of D1-D5 re-derives as repaired. Each check is a command over
committed/live lane bytes; none reads an artifact round 30 creates, so C2 stays
separable from C1 (QUALITY R13).

Frozen items (corpus/lessons/round-29-verifier-spotcheck.md §5):
  D1 report cites corpus/evidence/round29-attempt2/control-nothing.txt, which was absent
  D2 the kappa sweep is rendered "0 hits in the lane" where the command scoped corpus/knowledge/*.md
  D3 the lesson prices S078's line-75 quote at 9 words; row and registry say 8
  D4 uncommitted wave evidence .ufo/waves/round-29/attempt2/build/R29a2CritEntry.md
  D5 S091 used-by names the entry while the entry carries no source: S091 line
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

D1_PATH = "corpus/evidence/round29-attempt2/control-nothing.txt"
LESSON = "corpus/lessons/round-29.md"
D4_PATH = ".ufo/waves/round-29/attempt2/build/R29a2CritEntry.md"
EXPECT = ".ufo/waves/round-29/attempt2/adoption-expect.json"
ENTRY = "corpus/knowledge/benchmark-task-validity-checklist.md"
REGISTRY = "corpus/SOURCES.md"

QUOTE = "The verifier never runs in the agent's sandbox."
D3_LESSON_RE = re.compile(re.escape('"' + QUOTE + '"') + r"\s*[—-]+\s*(\d+)\s+words")
D3_ROW_RE = re.compile(re.escape('"' + QUOTE + '"') + r"\s*\((\d+)\s+words\)")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|")


def words(text: str) -> int:
    return len(text.split())


def cell(text: str, row_id: str) -> list[str] | None:
    for raw in text.splitlines():
        match = ROW_RE.match(raw)
        if match and match.group(1) == row_id:
            body = raw.strip()
            cells = body[1:-1].split("|")
            if len(cells) != 11:
                return None
            return [item.strip() for item in cells]
    return None


QUOTED_LINE = (
    "entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=skipped"
)
WAVE_LINE = (
    "entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 verified_at=0 census=skipped"
)


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(lane), *args], capture_output=True, text=True, check=False
    )


def head_blob(lane: Path, path: str) -> str | None:
    proc = git(lane, "cat-file", "-p", f"HEAD:{path}")
    return proc.stdout if proc.returncode == 0 else None


def check_d1(lane: Path) -> str:
    path = lane / D1_PATH
    if not path.is_file():
        return f"receipt absent at the cited path {D1_PATH}"
    # The routed defect says the path is "not committed"; a worktree file alone is not the repair,
    # and a prefix test is gameable (both found by round-30 reviewers), so judge the HEAD blob.
    text = head_blob(lane, D1_PATH)
    if text is None:
        return f"receipt exists only in the worktree: {D1_PATH} is not committed at HEAD"
    lines = text.splitlines()
    if QUOTED_LINE not in lines:
        return "the committed receipt does not carry the report's quoted seven-field line verbatim"
    if WAVE_LINE not in lines:
        return "the committed receipt does not record the wave file's eight-field variant"
    if "exit code of that run: 1" not in text and "exit=1" not in text:
        return "the committed receipt carries no exit=1 line (a passing control proves nothing)"
    return ""


def check_d2(lane: Path) -> str:
    text = (lane / LESSON).read_text(encoding="utf-8")
    lines = [raw for raw in text.splitlines() if "kappa" in raw]
    if not lines:
        return "no kappa line in the lesson: the sweep the closure narrowed is gone"
    for raw in lines:
        # Markdown emphasis hides the banned phrase from a literal test ("in the **lane**");
        # strip it for that test only — the scope test must see the raw `*` of the glob.
        plain = re.sub(r"\*\*|__", "", raw)
        if "in the lane" in plain:
            return "kappa sweep still rendered 'in the lane' where the command scoped corpus/knowledge/*.md"
        if "corpus/knowledge/*.md" not in raw:
            return "kappa line names no measured scope (corpus/knowledge/*.md)"
    # A named scope is not enough: a falsified count beside it survives a scope-only check
    # (found by the round-30 mutation-tester). Re-derive the count the sentence states, in the
    # unit the lesson's own command reports: `grep -rn` prints one line per matching line.
    hit = re.search(r"→\s*(\d+)\s+hits?\b", " ".join(lines))
    if hit is None:
        return "kappa lines carry no '<n> hits' count to re-derive"
    actual = 0
    for path in sorted((lane / "corpus" / "knowledge").glob("*.md")):
        actual += sum(
            1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if "kappa" in line
        )
    if int(hit.group(1)) != actual:
        return f"kappa sentence states {hit.group(1)} hits, corpus/knowledge/*.md holds {actual}"
    return ""


def check_d3(lane: Path) -> str:
    lesson = (lane / LESSON).read_text(encoding="utf-8")
    registry = (lane / REGISTRY).read_text(encoding="utf-8")
    row = cell(registry, "S078")
    if row is None:
        return "S078 row missing or not 11 cells"
    row_match = D3_ROW_RE.search(row[5])
    if not row_match:
        return "S078 anchor cell carries no word count for the line-75 quote"
    row_count = int(row_match.group(1))
    if row_count != words(QUOTE):
        return f"registry S078 prices the line-75 quote at {row_count} words, actual {words(QUOTE)}"
    lesson_match = D3_LESSON_RE.search(lesson)
    if lesson_match and "line 75" not in lesson[lesson_match.end(): lesson_match.end() + 24]:
        return "lesson prices the quote but no longer locates it at line 75"
    if not lesson_match:
        return "lesson no longer prices the line-75 quote"
    lesson_count = int(lesson_match.group(1))
    if lesson_count != words(QUOTE):
        return (
            f"lesson prices the line-75 quote at {lesson_count} words, actual {words(QUOTE)} "
            f"(registry says {row_count})"
        )
    return ""


D4_MARKER = "### D. Addendum"


def check_d4(lane: Path) -> str:
    worktree = lane / D4_PATH
    if not worktree.is_file():
        return f"{D4_PATH} is absent altogether: the wave evidence was dropped, not landed"
    # A clean status is not the repair: a clone whose HEAD predates the addendum is clean too,
    # and so is a commit that discards the bytes. The committed blob must carry the addendum.
    text = head_blob(lane, D4_PATH)
    if text is None:
        return f"{D4_PATH} is not committed at HEAD"
    if D4_MARKER not in text:
        return f"HEAD:{D4_PATH} omits the addendum ({D4_MARKER!r}); the wave evidence is not landed"
    status = git(lane, "status", "--porcelain", "--", D4_PATH)
    if status.returncode != 0:
        return f"git status failed: {status.stderr.strip()}"
    if status.stdout.strip():
        return f"{D4_PATH} still differs from HEAD: {status.stdout.strip()}"
    return ""


def check_d5(lane: Path) -> str:
    expect_path = lane / EXPECT
    if not expect_path.is_file():
        return f"{EXPECT} absent"
    expect = json.loads(expect_path.read_text(encoding="utf-8"))
    entry = (lane / ENTRY).read_text(encoding="utf-8")
    # The closure offered two repairs and either satisfies it: cite S091 as a source, or record
    # the asymmetry. Only the second is reachable without moving round 29's frozen cited_rows.
    if re.search(r"^source:[ \t]*S091\b", entry, re.MULTILINE):
        return ""
    notes = expect.get("usedby_notes")
    if not isinstance(notes, dict) or "S091" not in notes:
        return "adoption-expect.json records no S091 used-by asymmetry note and the entry cites no S091"
    note = notes["S091"]
    # An empty or uninformative note is not a record (found by the round-30 mutation-tester).
    if not isinstance(note, str) or len(note.split()) < 10 or ENTRY not in note:
        return "the S091 note is empty, too short to be a record, or does not name the entry"
    registry = (lane / REGISTRY).read_text(encoding="utf-8")
    row = cell(registry, "S091")
    if row is None:
        return "S091 row missing or not 11 cells"
    if ENTRY not in [part.strip() for part in row[10].split(",")]:
        return "S091 used-by no longer names the entry the note explains"
    return ""


CHECKS = (
    ("D1", "receipt-at-cited-path", check_d1),
    ("D2", "kappa-sweep-scope", check_d2),
    ("D3", "s078-line75-word-count", check_d3),
    ("D4", "uncommitted-wave-evidence", check_d4),
    ("D5", "s091-usedby-asymmetry", check_d5),
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    lane = args.lane.resolve()
    defects = 0
    for item_id, label, check in CHECKS:
        reason = check(lane)
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
        else:
            print(f"ok {item_id} {label}: repaired")
    print(f"defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
