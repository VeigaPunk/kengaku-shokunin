#!/usr/bin/env python3
"""Eight frozen C1 predicates for the Terminal-Bench 2.0 task audit."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from pathlib import Path

ENTRY = "terminal-bench-task-grader.md"
IDS = ("S105", "S106", "S107")
PIN = "2fd12b88aafdd04a52c298e3940bcb189f9766d6"
REQUIRED_FRONTIER = (
    "SWE-bench Pro V2 graders beyond round-31",
    "runtime task validity",
    "hosted judges",
    "contamination",
)

def checks(root: Path) -> list[tuple[str, bool, str]]:
    corpus = root / "corpus"
    entry_path = corpus / "knowledge" / ENTRY
    entry = entry_path.read_text(encoding="utf-8") if entry_path.is_file() else ""
    sources_path = corpus / "SOURCES.md"
    sources = sources_path.read_text(encoding="utf-8") if sources_path.is_file() else ""
    readme_path = corpus / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    cited = re.findall(r"(?m)^\s*source:\s*(.*?)\s*$", entry)
    cited_ids = [x for line in cited for x in re.findall(r"\bS\d{3}\b", line)]
    v1 = entry_path.is_file() and len(cited_ids) == 3 and set(cited_ids) == set(IDS) and len(set(cited_ids)) == 3
    v2 = bool(re.search(r"(?m)^verified-at:\s*2026-10-25\s*$", entry))
    rows_ok = True
    for sid in IDS:
        lines = [line for line in sources.splitlines() if re.search(rf"(?<!\w){sid}(?!\w)", line)]
        rows_ok &= len(lines) == 1 and "status=mined" in lines[0] and "opened=2026-10-25" in lines[0] and ENTRY in lines[0]
    index_rows = [line for line in readme.splitlines() if ENTRY in line]
    v4 = len(index_rows) == 1
    v5 = bool(re.search(r"(?is)Benchmark grader semantics", readme))
    frontier = re.search(r"(?ms)^## Frontier\s*\n(.*?)(?=^## |\Z)", readme)
    ftext = frontier.group(1) if frontier else ""
    v6 = all(clause in ftext for clause in REQUIRED_FRONTIER) and "protein-assembly" in ftext and PIN in ftext
    control_path = root / ".ufo/waves/round-34/claims/control-c1.txt"
    control = control_path.read_text(encoding="utf-8") if control_path.is_file() else ""
    v7 = control_path.is_file() and bool(re.search(r"(?m).*registry rows\s*=\s*97.*", control)) and bool(re.search(r"(?m).*rows S105\+\s*=\s*0.*", control))
    cap = root / ".ufo/waves/round-34/assimilation/captures/tb2-eval"
    sums_path = cap / "SHA256SUMS"
    sums = sums_path.read_text(encoding="utf-8") if sums_path.is_file() else ""
    v8 = sums_path.is_file() and _sums_valid(cap, sums)
    return [(f"V{i}", bool(ok), msg) for i, (ok, msg) in enumerate([
        (v1, "entry cites exactly S105/S106/S107"),
        (v2, "verified-at date"),
        (bool(rows_ok), "source rows mined/opened/used-by"),
        (v4, "exactly one README index row"),
        (v5, "coverage discharge names task and pin"),
        (v6, "frontier clauses retained and TB clause narrowed"),
        (v7, "freeze control receipt values"),
        (v8, "captured evaluator SHA256SUMS"),
    ], 1)]

def _sums_valid(directory: Path, text: str) -> bool:
    found = 0
    for line in text.splitlines():
        m = re.fullmatch(r"([0-9a-fA-F]{64})\s+[* ]?(.+?)\s*", line)
        if not m:
            return False
        digest, name = m.groups()
        target = directory / name
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest().lower() != digest.lower():
            return False
        found += 1
    return found > 0

def run(root: Path) -> tuple[int, list[tuple[str, bool, str]]]:
    results = checks(root)
    defects = 0
    for label, ok, message in results:
        if not ok:
            defects += 1
            print(f"DEFECT {label}: {message}")
    print(f"checks=8 defects={defects}")
    return defects, results

def selftest() -> int:
    cases = 0
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        good = base / "green"
        (good / "corpus/knowledge").mkdir(parents=True)
        (good / ".ufo/waves/round-34/claims").mkdir(parents=True)
        cap = good / ".ufo/waves/round-34/assimilation/captures/tb2-eval"
        cap.mkdir(parents=True)
        (good / "corpus/knowledge" / ENTRY).write_text("source: S105, S106, S107\nverified-at: 2026-10-25\n", encoding="utf-8")
        (good / "corpus/SOURCES.md").write_text("\n".join(f"{s} status=mined opened=2026-10-25 used-by={ENTRY}" for s in IDS), encoding="utf-8")
        (good / "corpus/README.md").write_text(f"- {ENTRY}\nBenchmark grader semantics Terminal-Bench protein-assembly {PIN}\n## Frontier\n- SWE-bench Pro V2 graders beyond round-31; runtime task validity; hosted judges; contamination; Terminal-Bench protein-assembly {PIN}\n", encoding="utf-8")
        (good / ".ufo/waves/round-34/claims/control-c1.txt").write_text("registry rows = 97\nrows S105+ = 0\n", encoding="utf-8")
        payload = b"fixture evaluator"
        (cap / "test.sh").write_bytes(payload)
        (cap / "SHA256SUMS").write_text(f"{hashlib.sha256(payload).hexdigest()}  test.sh\n", encoding="utf-8")
        if any(not ok for _, ok, _ in checks(good)):
            print("SELFTEST FAIL: green fixture")
            return 1
        cases += 1
        for idx in range(8):
            bad = base / f"red-{idx}"
            import shutil
            shutil.copytree(good, bad)
            paths = [bad / "corpus/knowledge" / ENTRY, bad / "corpus/knowledge" / ENTRY,
                     bad / "corpus/SOURCES.md", bad / "corpus/README.md", bad / "corpus/README.md",
                     bad / "corpus/README.md", bad / ".ufo/waves/round-34/claims/control-c1.txt",
                     bad / ".ufo/waves/round-34/assimilation/captures/tb2-eval/test.sh"]
            p = paths[idx]
            if idx in (0, 1):
                p.write_text(p.read_text().replace("S105, S106, S107", "S105, S106") if idx == 0 else p.read_text().replace("2026-10-25", "2026-10-24"), encoding="utf-8")
            elif idx == 2: p.write_text(p.read_text().replace("status=mined", "status=unopened", 1), encoding="utf-8")
            elif idx == 3: p.write_text(p.read_text().replace(f"- {ENTRY}\n", ""), encoding="utf-8")
            elif idx == 4: p.write_text(p.read_text().replace(PIN, "badpin", 1), encoding="utf-8")
            elif idx == 5: p.write_text(p.read_text().replace("hosted judges; ", ""), encoding="utf-8")
            elif idx == 6: p.write_text(p.read_text().replace("97", "96"), encoding="utf-8")
            else: p.write_bytes(b"tampered")
            if checks(bad)[idx][1]:
                print(f"SELFTEST FAIL: red V{idx+1} fixture passed")
                return 1
            cases += 1
    print(f"SELFTEST cases={cases} defects=0")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.lane is None:
        parser.error("--lane is required unless --selftest is used")
    defects, _ = run(args.lane.resolve())
    return 0 if defects == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
