#!/usr/bin/env python3
"""Second receipt for round 32's C1: the literals `adoption_check.py` does not read.

Round 32 (2026-10-25). The frozen C1 counter (`plans/adoption_check.py`, unchanged from
rounds 29-31) proves four things: an entry exists, it has an index row, its cited ids have
registry rows that are `mined` with a matching `used-by`, and the fleet census passes. The
round-31 C1 critic showed what that leaves open: a 63-byte stub with three `source:` lines
passes the whole line, because the frozen entry path, the access-date literal and the
*identity* of each cited row are read from an expect file rather than from the entry.

This script closes those three without touching the frozen counter. It reads only committed
lane bytes, so a do-nothing tree scores zero.

Checks (one line each, `checks=N defects=M`, exit 0 only when M = 0):
  V1  the entry exists at the frozen path with a `verified-at: <access date>` line
  V2  every cited id's registry `source` cell URL host+path appears in the entry's own
      `source: <id>` line (identity, not just presence)
  V3  the entry names all three pinned revisions it was re-grounded at
  V4  the index row for the entry carries a non-trivial title cell
  V5  the entry's body is long enough to be a document, not a header stub
  V6  the freeze control receipt carries its exit code and the expect file's digest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

ENTRY = "corpus/knowledge/benchmark-grader-semantics.md"
REGISTRY = "corpus/SOURCES.md"
README = "corpus/README.md"
EXPECT = ".ufo/waves/round-32/claims/adoption-expect.json"
CONTROL = ".ufo/waves/round-32/claims/control-nothing.txt"
PINS = ("66f92766", "9be8d8fe", "2412.05579")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S[0-9]{3,})[ \t]*\|")
URL_RE = re.compile(r"https?://\S+")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_v1(lane: Path, expect: dict) -> str:
    path = lane / ENTRY
    if not path.is_file():
        return f"the frozen entry path {ENTRY} does not exist"
    date = expect.get("access_date", "")
    if f"verified-at: {date}" not in read(path):
        return f"the entry carries no 'verified-at: {date}' line"
    return ""


def registry_sources(lane: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for raw in read(lane / REGISTRY).splitlines():
        match = ROW_RE.match(raw)
        if not match:
            continue
        cells = raw.strip()[1:-1].split("|")
        if len(cells) == 11:
            rows[match.group(1)] = cells[1]
    return rows


def check_v2(lane: Path, expect: dict) -> str:
    entry = read(lane / ENTRY)
    rows = registry_sources(lane)
    ids = [sid for item in expect.get("entries", []) for sid in item.get("sources", [])]
    if not ids:
        return "the expect file names no cited ids"
    for sid in ids:
        if sid not in rows:
            return f"{sid} has no registry row"
        url = URL_RE.search(rows[sid])
        if url is None:
            return f"the {sid} registry row cites no URL"
        host_path = re.sub(r"^https?://", "", url.group(0)).rstrip("/")
        line = next(
            (raw for raw in entry.splitlines() if re.match(rf"^source: {sid}\b", raw)), ""
        )
        if not line:
            return f"the entry has no 'source: {sid}' line"
        if host_path not in re.sub(r"^https?://", "", line):
            return f"the entry's {sid} line does not name the row's cited document ({host_path})"
    return ""


def check_v3(lane: Path, expect: dict) -> str:
    entry = read(lane / ENTRY)
    missing = [pin for pin in PINS if pin not in entry]
    if missing:
        return f"the entry names no pinned revision for {', '.join(missing)}"
    return ""


def check_v4(lane: Path, expect: dict) -> str:
    name = Path(ENTRY).name
    rows = [
        raw
        for raw in read(lane / README).splitlines()
        if raw.startswith(f"| `knowledge/{name}`")
    ]
    if len(rows) != 1:
        return f"the index carries {len(rows)} rows for {name}, not exactly one"
    cells = rows[0].strip().strip("|").split("|")
    if len(cells) < 2 or len(cells[1].strip()) < 20:
        return "the index row's title cell is empty or trivial"
    return ""


def check_v5(lane: Path, expect: dict) -> str:
    text = read(lane / ENTRY)
    lines = text.splitlines()
    if len(lines) < 40:
        return f"the entry is {len(lines)} lines: a header stub, not a document"
    if len(text) < 3000:
        return f"the entry is {len(text)} bytes: a header stub, not a document"
    return ""


def check_v6(lane: Path, expect: dict) -> str:
    control = lane / CONTROL
    expect_path = lane / EXPECT
    if not control.is_file() or not expect_path.is_file():
        return "the control receipt or the expect file is absent"
    digest = hashlib.sha256(expect_path.read_bytes()).hexdigest()
    text = read(control)
    if f"expect_sha256={digest}" not in text:
        return "the control receipt does not pin the expect file's digest"
    if "exit=1" not in text:
        return "the control receipt records no exit code (a passing control proves nothing)"
    return ""


CHECKS = (
    ("V1", "entry-at-frozen-path", check_v1),
    ("V2", "cited-row-identity", check_v2),
    ("V3", "pinned-revisions-named", check_v3),
    ("V4", "index-row-title", check_v4),
    ("V5", "entry-substance", check_v5),
    ("V6", "control-receipt-hardened", check_v6),
)


def selftest() -> int:
    cases: list[tuple[str, bool]] = [("registry-complete", len(CHECKS) == 6)]
    with tempfile.TemporaryDirectory() as tmp:
        lane = Path(tmp)
        expect = {"access_date": "2026-10-25", "entries": [{"sources": ["S093", "S094", "S097"]}]}
        for item_id, label, check in CHECKS:
            try:
                red = bool(check(lane, expect))
            except Exception:
                red = True
            cases.append((f"{item_id}-red-on-empty", red))
    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(CHECKS)} failed={len(failed)}")
    return 0 if not failed else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    lane = args.lane.resolve()
    expect_path = lane / EXPECT
    if not expect_path.is_file():
        print(f"DEFECT V0 expect: {EXPECT} is absent")
        print("checks=6 defects=1")
        return 1
    expect = json.loads(expect_path.read_text(encoding="utf-8"))
    defects = 0
    for item_id, label, check in CHECKS:
        try:
            reason = check(lane, expect)
        except Exception as error:
            reason = f"check raised {type(error).__name__}: {error}"
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
    print(f"checks={len(CHECKS)} defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
