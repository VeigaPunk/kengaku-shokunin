#!/usr/bin/env python3
"""Build the R98-C2 mutation matrix in a fixture clone at T (scratch only).

Each mutant is a single commit on top of T in /fast/scratch/hyaku/kengaku-r98/MutC2/clone.
Nothing outside the scratch tree is written.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/fast/scratch/hyaku/kengaku-r98/MutC2")
CLONE = ROOT / "clone"
T = "8e37fc65d5649bb37166fdd6b1657445a8cb55b9"
PROV = "corpus/evidence/PROVENANCE.md"
SRC = "corpus/SOURCES.md"
CAP = "corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.py"
COPY = "corpus/evidence/round52/graders/bn-fit-modify/tests/test_outputs.copy.py"
PROV2 = "corpus/evidence/round52/graders/bn-fit-modify/tests/PROVENANCE.md"
GATE = "plans/anchor_digest_check.py"
LESSON = "corpus/lessons/round-37.md"

T181 = "364069f893e336a021c907dd0ac11ff4c9e7ca7b4fa7ab506c360166960e455b"
T182 = "5d4d57c43e6913bf3d0081da764ad36d1b7275e3bb114a05abda529afe563905"
T105 = "44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582"
ZERO = "0" * 64
BEEF = "beef" * 16
URL181 = ("https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/"
          "2fd12b88aafdd04a52c298e3940bcb189f9766d6/bn-fit-modify/tests/test_outputs.py")
URL306 = ("https://raw.githubusercontent.com/bottlepy/bottle/"
          "0207a34f0c5716cd292dd4480253ad35d3da49f3/bottle.py")

MUTANTS = [
    {"id": "M01", "desc": "PROVENANCE: delete the S181 binding line",
     "files": [PROV],
     "ops": [("del_line_prefix", PROV, "| S181 |")]},
    {"id": "M02", "desc": "PROVENANCE: delete the S181 and S323 binding lines (partial)",
     "files": [PROV],
     "ops": [("del_line_prefix", PROV, "| S181 |"), ("del_line_prefix", PROV, "| S323 |")]},
    {"id": "M03", "desc": "PROVENANCE: swap the capture paths of S181 and S182",
     "files": [PROV],
     "ops": [("replace", PROV, "| S181 | `round52/graders/bn-fit-modify/tests/test_outputs.py` |",
              "| S181 | `round52/graders/pytorch-model-recovery/tests/test_outputs.py` |"),
             ("replace", PROV, "| S182 | `round52/graders/pytorch-model-recovery/tests/test_outputs.py` |",
              "| S182 | `round52/graders/bn-fit-modify/tests/test_outputs.py` |")]},
    {"id": "M04", "desc": "PROVENANCE: rename the S181 row id to S999",
     "files": [PROV],
     "ops": [("replace", PROV, "| S181 |", "| S999 |")]},
    {"id": "M05", "desc": "PROVENANCE: change the S181 sha256 column to 64 zeros",
     "files": [PROV],
     "ops": [("replace", PROV, f"`{T181}`", f"`{ZERO}`")]},
    {"id": "M06", "desc": "PROVENANCE: point S181 at a non-committed path",
     "files": [PROV],
     "ops": [("replace", PROV, "| S181 | `round52/graders/bn-fit-modify/tests/test_outputs.py` |",
              "| S181 | `round52/graders/bn-fit-modify/tests/test_outputs.py.bak` |")]},
    {"id": "M07", "desc": "SOURCES: edit the S181 anchor token",
     "files": [SRC],
     "ops": [("replace", SRC, f"sha256 {T181}; line 14", f"sha256 {BEEF}; line 14")]},
    {"id": "M08", "desc": "SOURCES: append one space to the S181 row line (byte change, same cells)",
     "files": [SRC],
     "ops": [("append_suffix_to_line", SRC, "| S181 |", " ")]},
    {"id": "M09", "desc": "capture: append one newline byte to the S181 capture",
     "files": [CAP],
     "ops": [("append_bytes", CAP, b"\n")]},
    {"id": "M10", "desc": "capture: delete the S181 capture",
     "files": [CAP],
     "ops": [("delete_file", CAP)]},
    {"id": "M11", "desc": "second PROVENANCE.md under corpus/evidence binds S181 to a byte-identical copy",
     "files": [COPY, PROV2],
     "ops": [("copy_file", CAP, COPY),
             ("write_file", PROV2,
              "# mutant M11: second provenance file binding a POP row to a copy\n"
              f"| S181 | `test_outputs.copy.py` | {URL181} | `{T181}` |\n")]},
    {"id": "M12", "desc": "M11 plus the main PROVENANCE S181 line deleted (single binding, to the copy)",
     "files": [COPY, PROV2, PROV],
     "ops": [("copy_file", CAP, COPY),
             ("write_file", PROV2,
              "# mutant M12: second provenance file binding a POP row to a copy\n"
              f"| S181 | `test_outputs.copy.py` | {URL181} | `{T181}` |\n"),
             ("del_line_prefix", PROV, "| S181 |")]},
    {"id": "M13", "desc": "gate: append one comment line to plans/anchor_digest_check.py",
     "files": [GATE],
     "ops": [("append_bytes", GATE, b"\n# MUTANT M13: one comment line appended\n")]},
    {"id": "M14", "desc": "SOURCES: give the clean non-POP row S105 an unknown 64-hex token",
     "files": [SRC],
     "ops": [("replace", SRC, f"sha256 {T105}", f"sha256 {BEEF}")]},
    {"id": "M15", "desc": "SOURCES: change the S306 upstream URL subpath (same anchor-unbound class)",
     "files": [SRC],
     "ops": [("replace", SRC, URL306, URL306.replace("/bottle.py", "/src/bottle.py"))]},
    {"id": "M16", "desc": "PROVENANCE: duplicate the S181 binding line (same path twice)",
     "files": [PROV],
     "ops": [("dup_line_prefix", PROV, "| S181 |")]},
    {"id": "M17", "desc": "delete corpus/evidence/PROVENANCE.md entirely (do-nothing shape)",
     "files": [PROV],
     "ops": [("delete_file", PROV)]},
    {"id": "M18", "desc": "PROVENANCE: change the S181 pinned-URL column to a novel URL",
     "files": [PROV],
     "ops": [("replace", PROV, URL181, URL181.replace("/test_outputs.py", "/other.py"))]},
    {"id": "M19", "desc": "lessons: add an erratum line naming POP row S181 with an unresolved token",
     "files": [LESSON],
     "ops": [("append_bytes", LESSON,
              f"\n\nErratum (round 37): S181 anchor sha256 {BEEF}\n")]},
]


def git(*args: str) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", "-C", str(CLONE), *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed rc={p.returncode}: {p.stderr.strip()}")
    return p


def assert_toplevel() -> None:
    top = git("rev-parse", "--show-toplevel").stdout.strip()
    if top != str(CLONE):
        raise SystemExit(f"fixture toplevel {top!r} != {str(CLONE)!r}")


def read(path: str) -> bytes:
    return (CLONE / path).read_bytes()


def write(path: str, data: bytes) -> None:
    f = CLONE / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(data)


def apply_ops(ops: list) -> None:
    for op in ops:
        kind = op[0]
        if kind == "replace":
            _, path, old, new = op
            b = read(path)
            o, n = old.encode(), new.encode()
            if b.count(o) != 1:
                raise SystemExit(f"replace {path}: {b.count(o)} matches for {old[:70]!r}")
            write(path, b.replace(o, n))
        elif kind == "del_line_prefix":
            _, path, prefix = op
            lines = read(path).split(b"\n")
            keep = [ln for ln in lines if not ln.startswith(prefix.encode())]
            if len(keep) != len(lines) - 1:
                raise SystemExit(f"del_line_prefix {path}: removed {len(lines) - len(keep)} lines")
            write(path, b"\n".join(keep))
        elif kind == "dup_line_prefix":
            _, path, prefix = op
            out, hit = [], 0
            for ln in read(path).split(b"\n"):
                out.append(ln)
                if ln.startswith(prefix.encode()):
                    out.append(ln)
                    hit += 1
            if hit != 1:
                raise SystemExit(f"dup_line_prefix {path}: {hit} matching lines")
            write(path, b"\n".join(out))
        elif kind == "append_suffix_to_line":
            _, path, prefix, suffix = op
            lines, hit = read(path).split(b"\n"), 0
            for i, ln in enumerate(lines):
                if ln.startswith(prefix.encode()):
                    lines[i] = ln + suffix.encode()
                    hit += 1
            if hit != 1:
                raise SystemExit(f"append_suffix_to_line {path}: {hit} matching lines")
            write(path, b"\n".join(lines))
        elif kind == "append_bytes":
            _, path, data = op
            write(path, read(path) + (data if isinstance(data, bytes) else data.encode()))
        elif kind == "delete_file":
            (CLONE / op[1]).unlink()
        elif kind == "copy_file":
            _, src, dst = op
            write(dst, read(src))
        elif kind == "write_file":
            _, path, content = op
            write(path, content.encode())
        else:
            raise SystemExit(f"unknown op {kind}")


def sha(path: str) -> str:
    f = CLONE / path
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else "absent"


def main() -> int:
    assert_toplevel()
    pristine = {}
    for m in MUTANTS:
        for p in m["files"]:
            pristine.setdefault(p, sha(p))
    records = []
    for m in MUTANTS:
        git("checkout", "-q", "-f", "-B", m["id"], T)
        apply_ops(m["ops"])
        git("add", "-A")
        git("commit", "-q", "-m", f'{m["id"]}: {m["desc"]}')
        commit = git("rev-parse", "HEAD").stdout.strip()
        parent = git("rev-parse", "HEAD^").stdout.strip()
        if parent != T:
            raise SystemExit(f'{m["id"]}: parent {parent} != T')
        files = {p: {"pristine": pristine[p], "mutated": sha(p)} for p in m["files"]}
        changed = {p: v for p, v in files.items() if v["pristine"] != v["mutated"]}
        if not changed:
            raise SystemExit(f'{m["id"]}: no byte changed')
        records.append({"id": m["id"], "desc": m["desc"], "commit": commit,
                        "files": files, "changed": sorted(changed)})
        print(f'{m["id"]} {commit[:12]} changed={len(changed)} {m["desc"]}')
    git("checkout", "-q", "-f", "-B", "restored", T)
    restored = {p: sha(p) for p in pristine}
    bad = {p: (pristine[p], restored[p]) for p in pristine if pristine[p] != restored[p]}
    (ROOT / "mutants.json").write_text(json.dumps(
        {"T": T, "pristine": pristine, "mutants": records, "restored": restored,
         "restore_ok": not bad, "restore_bad": bad}, indent=2) + "\n")
    print(f"restored={not bad} files={len(pristine)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
