#!/usr/bin/env python3
"""Frozen, literal source-reference coverage. Not a source-truth verifier."""
import argparse
import collections
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

POPULATION = "plans/fixtures/r28/registry/population.json"
POPULATION_SHA256 = "1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014"
REFERENCE = re.compile(r"(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])")
SOURCE_ID = re.compile(r"S[0-9]{3,}\Z")
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}


def safe_path(value):
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and ".." not in p.parts and "\\" not in value


def parse_registry(text):
    rows, findings = {}, []
    active, fenced = False, False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            active = line.strip() == "## Registry"
        if not active or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells or not SOURCE_ID.fullmatch(cells[0]):
            continue
        sid = cells[0]
        if len(cells) != 11:
            findings.append({"id": "malformed_source_row", "source": sid, "line": number})
            continue
        if sid in rows:
            findings.append({"id": "duplicate_source_id", "source": sid, "line": number})
            continue
        rows[sid] = dict(zip(("id", "source", "kind", "tier", "scope", "anchor", "teaches", "status", "opened", "recheck", "used_by"), cells))
    return rows, findings


def check(root, population):
    rows, findings = parse_registry((root / "corpus/SOURCES.md").read_text())
    refs = {sid: set() for sid in population["source_ids"]}
    for relative in population["knowledge_paths"]:
        if not safe_path(relative):
            findings.append({"id": "invalid_population_path", "path": relative})
            continue
        path = root / relative
        if not path.is_file():
            findings.append({"id": "knowledge_missing", "path": relative})
            continue
        for sid in set(REFERENCE.findall(path.read_text())) & refs.keys():
            refs[sid].add(relative)
    results = []
    for sid, citing in refs.items():
        row = rows.get(sid)
        if row is None:
            if not citing:
                continue
            findings.append({"id": "source_missing", "source": sid})
            results.append({"source": sid, "status": None, "citing_files": sorted(citing), "used_by": [], "missing_used_by": sorted(citing)})
            continue
        used_by = [] if row["used_by"] in ("", "—") else [p.strip().strip("`") for p in re.split(r"[,;]", row["used_by"])]
        if row["status"] not in {"queued", "mined", "rejected"} or row["tier"] not in {"A", "B", "C"} or row["kind"] not in KINDS or (row["kind"] == "community" and row["tier"] == "A"):
            findings.append({"id": "invalid_source_enum", "source": sid})
        for relative in used_by:
            if not safe_path(relative):
                findings.append({"id": "invalid_used_by", "source": sid, "path": relative})
            elif not (root / relative).is_file():
                findings.append({"id": "used_by_missing", "source": sid, "path": relative})
        missing = sorted(citing - set(used_by))
        if citing and row["status"] != "mined":
            findings.append({"id": "cited_not_mined", "source": sid, "status": row["status"]})
        for relative in missing:
            findings.append({"id": "missing_used_by", "source": sid, "path": relative})
        results.append({"source": sid, "status": row["status"], "citing_files": sorted(citing), "used_by": sorted(used_by), "missing_used_by": missing})
    return {"scope": "frozen literal references, not citation truth or whole-current-tree consistency", "population_revision": population.get("base_revision"), "source_rows_checked": len(refs), "knowledge_files_expected": len(population["knowledge_paths"]), "reference_links": sum(len(v) for v in refs.values()), "mismatch_sources": len({f["source"] for f in findings if "source" in f}), "finding_count": len(findings), "findings": findings, "sources": results}


def selftest():
    """CLI mode, isolated hand-authored miniature populations plus real CLI pin checks."""
    cases = []
    with tempfile.TemporaryDirectory(prefix="kengaku-r28-registry-") as temp:
        root = Path(temp)
        (root / "corpus/knowledge").mkdir(parents=True)
        path = "corpus/knowledge/a.md"
        (root / path).write_text("source: S038\n```\nS049\n```\nXS038 S038x\n")
        pop = {"source_ids": ["S038", "S049"], "knowledge_paths": [path]}
        def row(sid, status="mined", used=path):
            return f"| {sid} | source | paper | A | scope | anchor | teaches | {status} | 2026-10-21 | 90d | {used} |\n"
        def run(name, text, expected):
            (root / "corpus/SOURCES.md").write_text("## Registry\n" + text + "## Paths\n" + row("S038", "queued", "—"))
            result = check(root, pop)
            actual = {f["id"] for f in result["findings"]}
            assert actual == set(expected), (name, actual, expected)
            cases.append(name)
            return result
        baseline = run("valid_literal_fence", row("S038") + row("S049"), [])
        assert baseline["reference_links"] == 2
        run("queued_and_missing", row("S038", "queued", "—") + row("S049"), ["cited_not_mined", "missing_used_by"])
        run("missing_used_by", row("S038", "mined", "—") + row("S049"), ["missing_used_by"])
        run("duplicate", row("S038") * 2 + row("S049"), ["duplicate_source_id"])
        run("source_missing", row("S038"), ["source_missing"])
        run("unsafe_used_by", row("S038", used="../escape") + row("S049"), ["invalid_used_by", "missing_used_by"])
        run("bad_enum", row("S038", status="clean") + row("S049"), ["invalid_source_enum", "cited_not_mined"])
        run("extra_queued_source", row("S038") + row("S049") + row("S099", "queued", "—"), [])
        (root / "corpus/knowledge/new.md").write_text("S038 S099")
        result = run("new_file_excluded", row("S038") + row("S049"), [])
        assert result["reference_links"] == 2
        (root / path).unlink()
        run("missing_frozen_file", row("S038", used="—") + row("S049", used="—"), ["knowledge_missing"])
        (root / POPULATION).parent.mkdir(parents=True)
        (root / POPULATION).write_text("{}\n")
        command = [sys.executable, str(Path(__file__).resolve()), "--root", str(root), "--json"]
        probe = subprocess.run(command, capture_output=True, text=True)
        assert probe.returncode == 2 and json.loads(probe.stdout)["findings"][0]["id"] == "population_tampered"
        cases.append("cli_population_tampered")
        (root / POPULATION).unlink()
        probe = subprocess.run(command, capture_output=True, text=True)
        assert probe.returncode == 2 and json.loads(probe.stdout)["findings"][0]["id"] == "input_missing"
        cases.append("cli_population_missing")
    print("SELFTEST clean cases=" + str(len(cases)) + " " + ",".join(cases))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        raw = (args.root / POPULATION).read_bytes()
        if hashlib.sha256(raw).hexdigest() != POPULATION_SHA256:
            result = {"findings": [{"id": "population_tampered"}]}
            code = 2
        else:
            result = check(args.root, json.loads(raw))
            code = int(bool(result["findings"]))
    except (OSError, ValueError, KeyError, TypeError) as error:
        result, code = {"findings": [{"id": "input_missing" if isinstance(error, FileNotFoundError) else "input_invalid", "detail": str(error)}]}, 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("SCOPE frozen13 source rows / baseline35 knowledge files; literal mentions, not source truth; new files excluded")
        for finding in result["findings"]:
            print("FINDING " + json.dumps(finding, sort_keys=True))
        print("TOTAL " + " ".join(f"{key}={result.get(key, 'unavailable')}" for key in ("source_rows_checked", "knowledge_files_expected", "reference_links", "mismatch_sources", "finding_count")) + f" exit={code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
