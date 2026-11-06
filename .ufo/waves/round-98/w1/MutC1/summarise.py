#!/usr/bin/env python3
"""Summarise out/<name>.out into a kill matrix (markdown + json)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC1")
LEG = re.compile(r"^L(\d+)=(pass|fail)")
PRED = re.compile(r"^PREDICATE R98-C1 (\S+)")


def parse(name: str) -> dict:
    out = ROOT / "out" / f"{name}.out"
    rc = (ROOT / "out" / f"{name}.rc").read_text().strip() if (ROOT / "out" / f"{name}.rc").exists() else "?"
    text = out.read_text(errors="replace") if out.exists() else ""
    legs = {}
    target = ""
    pred = "absent"
    defects = []
    for line in text.splitlines():
        if line.startswith("LEGS "):
            for tok in line[5:].split():
                m = LEG.match(tok)
                if m:
                    legs["L" + m.group(1)] = m.group(2)
        elif line.startswith("TARGET "):
            target = line
        elif line.startswith("PREDICATE "):
            pred = PRED.match(line).group(1) if PRED.match(line) else line
        elif line.startswith("DEFECT "):
            defects.append(line)
    return dict(name=name, rc=int(rc) if rc.lstrip("-").isdigit() else rc, legs=legs,
                failing=[k for k, v in legs.items() if v == "fail"], target=target, predicate=pred,
                defects=defects)


def main() -> int:
    manifest = {m["name"]: m for m in json.loads((ROOT / "manifest.json").read_text())}
    names = ["baseline"] + [n for n in manifest] + ["restored"]
    rows = [parse(n) for n in names if (ROOT / "out" / f"{n}.out").exists()]
    (ROOT / "matrix.json").write_text(json.dumps(rows, indent=1))
    print("| mutant | expected | rc | failing legs | predicate | verdict |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        m = manifest.get(r["name"], {})
        exp = m.get("expected", "pass (pristine)")
        if r["predicate"] == "pass":
            verdict = "SURVIVED"
        elif r["predicate"] == "fail":
            verdict = "killed"
        else:
            verdict = "could-not-evaluate"
        print(f"| {r['name']} | {exp} | {r['rc']} | {','.join(r['failing']) or '-'} | {r['predicate']} | {verdict} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
