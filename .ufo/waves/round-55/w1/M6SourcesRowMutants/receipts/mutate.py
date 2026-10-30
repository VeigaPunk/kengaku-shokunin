#!/usr/bin/env python3
"""mutate.py — apply ONE SOURCES.md row defect to the scratch lane copy.

Usage: mutate.py <mutant-id>
Restores the pristine copy first, then applies the single defect to the S201 row
(the round-55 DRAFT row).  Exits non-zero if the mutation did not apply.
"""
import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PRISTINE = ROOT / "pristine" / "SOURCES.md"
TARGET = ROOT / "lane" / "corpus" / "SOURCES.md"

S201_SHA = "a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286"


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    mut = sys.argv[1]
    text = PRISTINE.read_text(encoding="utf-8")
    lines = text.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.startswith("| S201 |")]
    if len(idx) != 1:
        print("S201 row not found exactly once", file=sys.stderr)
        return 2
    i = idx[0]
    row = lines[i]
    cells = row.split("|")
    if len(cells) != 13:
        print(f"unexpected S201 column count {len(cells)-2}", file=sys.stderr)
        return 2

    # cell layout of a 11-column row: cells[0]='' cells[1]=id cells[2]=source
    # cells[3]=kind cells[4]=tier cells[5]=scope cells[6]=anchor cells[7]=teaches
    # cells[8]=status cells[9]=opened cells[10]=recheck cells[11]=used-by cells[12]=''
    if mut == "M1":
        # drop one pipe: the pipe between the anchor cell and the teaches cell
        # (column count 11 -> 10)
        new = "|".join(cells[:6] + [cells[6] + " " + cells[7]] + cells[8:])
    elif mut == "M2":
        # move the sha256 token out of the anchor cell into the teaches cell
        anchor = cells[6]
        teaches = cells[7]
        assert S201_SHA in anchor, "sha256 token not in anchor cell"
        new_anchor = anchor.replace("; sha256 " + S201_SHA, "").rstrip()
        new_teaches = teaches.rstrip() + "; sha256 " + S201_SHA
        new = "|".join(cells[:6] + [new_anchor, new_teaches] + cells[8:])
    elif mut == "M3":
        # tier 'A' -> 'D'
        assert cells[4].strip() == "A", cells[4]
        new = "|".join(cells[:4] + [" D "] + cells[5:])
    elif mut == "M4":
        # status 'mined' -> 'mined!'
        assert cells[8].strip() == "mined", cells[8]
        new = "|".join(cells[:8] + [" mined! "] + cells[9:])
    elif mut == "M5":
        # duplicate id: a verbatim copy of the S201 row
        lines.insert(i + 1, row)
        TARGET.write_text("\n".join(lines), encoding="utf-8")
        print(f"applied {mut}")
        return 0
    else:
        print(f"unknown mutant {mut}", file=sys.stderr)
        return 2

    lines[i] = new
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    # sanity: the row must still exist and the file must differ from pristine
    after = TARGET.read_text(encoding="utf-8")
    if "| S201 |" not in after:
        print("mutation destroyed the S201 row", file=sys.stderr)
        return 2
    if sha256(TARGET) == sha256(PRISTINE):
        print("mutation was a no-op", file=sys.stderr)
        return 2
    print(f"applied {mut} sha256={sha256(TARGET)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
