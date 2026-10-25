#!/usr/bin/env python3
"""Re-derive an adoption round's landed state from committed bytes.

Round 29 attempt 2 (2026-10-25). One command, one line, exit 0 only when every
frozen expectation holds. It reads only committed corpus files, so a
do-nothing round scores zero.

Expectation file shape:
  {
    "round": 29,
    "access_date": "2026-10-25",
    "entries": [{"path": "corpus/knowledge/x.md", "sources": ["S077", ...]}]
  }

Counters printed:
  entries      expectation entries whose file exists
  indexed      entries with a `| `knowledge/<name>.md` |` row in corpus/README.md
  cited_rows   distinct source ids named by `source: S###` lines in those entries
  rows_present cited ids that hold a registry row
  rows_mined   cited ids whose `status` cell is `mined`
  usedby_ok    cited ids whose `used-by` cell names the citing entry
  census       `ok` only when the fleet census subprocess exits 0 (with --census)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROW_RE = re.compile(r"^( {0,3})\|[ \t]*(S[0-9]{3,})[ \t]*\|")
SOURCE_LINE_RE = re.compile(r"^source:[ \t]*(S[0-9]{3,})\b", re.MULTILINE)
CENSUS = Path("/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")


def registry_rows(path: Path) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(raw)
        if not match:
            continue
        cells = raw.rstrip()[1:-1].split("|")
        if len(cells) != 11:
            continue
        rows[match.group(2)] = [cell.strip() for cell in cells]
    return rows


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--expect", type=Path, required=True)
    parser.add_argument("--census", action="store_true")
    args = parser.parse_args(argv)

    lane = args.lane.resolve()
    expect = json.loads(args.expect.read_text(encoding="utf-8"))
    access_date = expect["access_date"]
    entries = expect["entries"]
    registry = registry_rows(lane / "corpus" / "SOURCES.md")
    readme = (lane / "corpus" / "README.md").read_text(encoding="utf-8")

    present = indexed = 0
    cited: set[str] = set()
    verified_at_ok = 0
    for entry in entries:
        rel = entry["path"]
        name = Path(rel).name
        path = lane / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if text:
            present += 1
        if f"| `knowledge/{name}` |" in readme:
            indexed += 1
        if f"verified-at: {access_date}" in text:
            verified_at_ok += 1
        cited.update(SOURCE_LINE_RE.findall(text))

    rows_present = sum(1 for row_id in cited if row_id in registry)
    rows_mined = sum(1 for row_id in cited if row_id in registry and registry[row_id][7] == "mined")
    usedby_ok = 0
    for entry in entries:
        rel = entry["path"]
        for row_id in entry["sources"]:
            cells = registry.get(row_id)
            if cells and rel in cells[10]:
                usedby_ok += 1
                break

    census_state = "skipped"
    census_code = 0
    if args.census:
        proc = subprocess.run(
            [str(CENSUS), "validate", "--root", str(lane.parent), lane.name],
            capture_output=True,
            text=True,
            check=False,
        )
        census_code = proc.returncode
        census_state = "ok" if proc.returncode == 0 else "fail"

    print(
        f"entries={present} indexed={indexed} cited_rows={len(cited)} "
        f"rows_present={rows_present} rows_mined={rows_mined} usedby_ok={usedby_ok} "
        f"verified_at={verified_at_ok} census={census_state}"
    )
    ok = (
        present == len(entries)
        and indexed == len(entries)
        and rows_present == len(cited)
        and rows_mined == len(cited)
        and usedby_ok == len(entries)
        and verified_at_ok == len(entries)
        and census_code == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
