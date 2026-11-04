#!/usr/bin/env python3
"""MutTesterR85 battery: eight independent mutants of the two new counters.

Every mutant is built by one exact textual edit of the pinned committed counter
(master 217910c5), never of the lane worktree.  Each mutant gets a fixture its
removed guard should let through; the pristine counter must reject the same
fixture first.  Results are printed as MUTANT lines and written to results.json.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path("/fast/scratch/hyaku/kengaku-r85/MutTesterR85")
L = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
import os
PIN = os.environ.get("BATTERY_PIN", "217910c513a46b5ff607561136e4beaac056ace0")
PY = sys.executable
ENV = {"PATH": "/usr/bin", "TMPDIR": str(S / "tmp")}

PRISTINE = Path(os.environ.get("BATTERY_PRISTINE", str(S / "pristine")))
MUTANTS = Path(os.environ.get("BATTERY_MUTANTS", str(S / "mutants")))
FIXTURES = Path(os.environ.get("BATTERY_FIXTURES", str(S / "fixtures")))
WORK = Path(os.environ.get("BATTERY_WORK", str(S / "work")))
TIP = Path(os.environ.get("BATTERY_TIP", str(S / "fixtures" / "tip")))
OUT = Path(os.environ.get("BATTERY_OUT", str(S / "logs" / "results.json")))

C1_PATHS = ("plans", "corpus/evidence/round52/graders/sqlite-db-truncate",
            "corpus/evidence/round85", "SKILL.md")
RECEIPT = "corpus/evidence/round85/sqlite-db-truncate-probe.txt"
TABLE = "plans/round85-cases.json"

C1_SPECS = [
    # name, needle, replacement, fixture kind, expected unmutated defect
    ("worktree-dirty",
     'if stamp.get("WORKTREE") != "clean":', "if False:",
     "receipt-worktree", "RECEIPT-WORKTREE"),
    ("exit-weak",
     'if stamp.get("EXIT") != "0":\n            defects.append(("RECEIPT-EXIT"',
     'if stamp.get("EXIT") not in {"0", "1", "3"}:\n            defects.append(("RECEIPT-EXIT"',
     "receipt-exit3", "RECEIPT-EXIT"),
    ("table-member",
     'if doc.get("member") != MEMBER:', "if False:",
     "table-member", "TABLE-MEMBER"),
    ("freeze-anchor",
     'if git(lane, "cat-file", "-e", f"{FREEZE_REV}:{rel}").returncode != 0:',
     "if False:",
     "freeze-unanchored", "SETUP"),
    ("predicate-absent",
     'if predicate != "pass":', 'if predicate == "fail":',
     "receipt-no-predicate", "PREDICATE-LINE"),
    ("table-subject",
     'if doc.get("subject_sha") != SUBJECT_SHA:', "if False:",
     "table-subject", "TABLE-SUBJECT"),
]

C2_SPECS = [
    ("indexed-always",
     'return EVIDENCE_ROW in text and "lessons/round-85.md" in text', "return True",
     "readme-unindexed", None),
    ("v8-ignores-exit",
     'ok = proc.returncode == 0 and "PREDICATE R82-C1 pass" in text',
     'ok = "PREDICATE R82-C1 pass" in text',
     "registry-nonzero", "v8"),
]

results = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], cwd: Path | None = None, timeout: int = 1800) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                          cwd=str(cwd) if cwd else None, env=ENV)


def git(repo: Path, *args: str, check_toplevel: bool = True) -> str:
    if check_toplevel:
        top = run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"]).stdout.strip()
        if top != str(repo.resolve()):
            raise SystemExit(f"toplevel mismatch: {top!r} != {repo!r}")
    proc = run(["git", "-C", str(repo), *args])
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


def build_mutants() -> tuple[dict[str, Path], dict[str, dict]]:
    built: dict[str, Path] = {}
    meta: dict[str, dict] = {}
    for counter, specs in (("c1.py", C1_SPECS), ("c2.py", C2_SPECS)):
        text = (PRISTINE / counter).read_text(encoding="utf-8")
        for name, needle, replacement, fixture, expected in specs:
            count = text.count(needle)
            if count == 0:
                meta[name] = {"counter": counter, "fixture": fixture,
                              "expected_unmutated_defect": expected,
                              "not_applicable": True, "needle_count": 0,
                              "pristine_sha": sha(PRISTINE / counter)}
                built[name] = None
                continue
            if count != 1:
                raise SystemExit(f"needle for {name} occurs {count} times")
            mutated = text.replace(needle, replacement, 1)
            path = MUTANTS / f"{name}.py"
            path.write_text(mutated, encoding="utf-8")
            built[name] = path
            meta[name] = {
                "counter": counter,
                "fixture": fixture,
                "expected_unmutated_defect": expected,
                "needle_count": count,
                "diff": "".join(difflib.unified_diff(
                    text.splitlines(True), mutated.splitlines(True),
                    fromfile=f"pristine/{counter}", tofile=f"mutants/{name}.py", n=3)),
                "pristine_sha": sha(PRISTINE / counter),
                "mutant_sha": sha(path),
            }
    return built, meta


# ---------------------------------------------------------------- C1 fixtures

def c1_fixture(kind: str) -> Path:
    root = Path(tempfile.mkdtemp(prefix=f"c1-{kind}-", dir=FIXTURES))
    for rel in C1_PATHS:
        src, dst = TIP / rel, root / rel
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    receipt = root / RECEIPT
    before = sha(receipt)
    if kind == "receipt-worktree":
        edit(receipt, "WORKTREE clean", "WORKTREE dirty")
    elif kind == "receipt-exit3":
        edit(receipt, "\nEXIT 0\n", "\nEXIT 3\n")
    elif kind == "receipt-no-predicate":
        text = receipt.read_text(encoding="utf-8")
        if text.count("PREDICATE R85-PROBE pass") != 1:
            raise SystemExit("predicate line count")
        path = root / RECEIPT
        path.write_text(text.replace("PREDICATE R85-PROBE pass\n", ""), encoding="utf-8")
    elif kind in ("table-member", "table-subject"):
        table = root / TABLE
        doc = json.loads(table.read_bytes())
        if kind == "table-member":
            doc["member"] = "sqlite-db-truncate-legacy"
        else:
            doc["subject_sha"] = doc["subject_sha"][:-1] + "0"
        table.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        rebind_table_sha(root, receipt)
    elif kind == "freeze-unanchored":
        git(root, "init", "-q", check_toplevel=False)
        git(root, "rev-parse", "--show-toplevel")
    else:
        raise SystemExit(f"unknown c1 fixture {kind}")
    return root


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"fixture edit {old!r} occurs {text.count(old)} times in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def rebind_table_sha(root: Path, receipt: Path) -> None:
    digest = sha(root / TABLE)
    text = receipt.read_text(encoding="utf-8")
    text, n = re.subn(r"(?m)^CASE_TABLE_SHA \S+$", f"CASE_TABLE_SHA {digest}", text)
    if n != 1:
        raise SystemExit("CASE_TABLE_SHA line not found")
    receipt.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- C2 fixtures

def c2_fixture(kind: str) -> tuple[Path, str]:
    repo = Path(tempfile.mkdtemp(prefix=f"c2-{kind}-", dir=FIXTURES))
    git(repo, "init", "-q", "--initial-branch=main", check_toplevel=False)
    git(repo, "rev-parse", "--show-toplevel")
    git(repo, "fetch", "--quiet", "--no-tags", str(L), f"{PIN}:refs/heads/master")
    git(repo, "switch", "-q", "master")
    if git(repo, "rev-parse", "HEAD") != PIN:
        raise SystemExit("fixture HEAD is not the pin")
    if kind == "readme-unindexed":
        readme = repo / "corpus/README.md"
        text = readme.read_text(encoding="utf-8")
        lines = text.splitlines(True)
        kept = [ln for ln in lines
                if "lessons/round-85.md" not in ln and "corpus/evidence/round85/" not in ln]
        if len(lines) - len(kept) < 2:
            raise SystemExit(f"README row count {len(lines) - len(kept)}")
        text = "".join(kept)
        if "lessons/round-85.md" in text or "corpus/evidence/round85/" in text:
            raise SystemExit("README markers survived")
        readme.write_text(text, encoding="utf-8")
    elif kind == "registry-nonzero":
        registry = repo / "plans/round82_c1_plans_registry.py"
        edit(registry,
             'if __name__ == "__main__":\n    sys.exit(main())\n',
             'if __name__ == "__main__":\n    code = main()\n'
             '    print("DEFECT POSTCHECK ledger-row-unreadable")\n    sys.exit(1)\n')
    else:
        raise SystemExit(f"unknown c2 fixture {kind}")
    git(repo, "-c", "user.name=MutTesterR85", "-c", "user.email=mut@example.invalid",
        "commit", "-qam", f"fixture: {kind}")
    return repo, git(repo, "rev-parse", "HEAD")


# ---------------------------------------------------------------- battery

def main() -> int:
    for path in (S / "tmp", MUTANTS, WORK):
        path.mkdir(parents=True, exist_ok=True)
    built = {name: (MUTANTS / f"{name}.py") if not META_REF[name].get("not_applicable") else None
             for name, *_ in C1_SPECS + C2_SPECS}
    for name, row in META_REF.items():
        if row.get("not_applicable"):
            results.append({"mutant": name, "fixture": row["fixture"],
                            "expected_unmutated": row["expected_unmutated_defect"],
                            "verdict": "not-applicable", "unmutated_rejected": None,
                            "mutant_accepted": None, "mutations": row})
            print(f"MUTANT {name} NOT-APPLICABLE (needle absent at this revision)")
    if any(row.get("not_applicable") for row in META_REF.values()):
        pass

    for name, needle, replacement, fixture, expected in C1_SPECS:
        if built[name] is None:
            continue
        root = c1_fixture(fixture)
        plain = run([PY, "-I", "-B", str(PRISTINE / "c1.py"), "--lane", str(root),
                     "--work", str(WORK / f"{name}-plain")])
        mutant = run([PY, "-I", "-B", str(built[name]), "--lane", str(root),
                      "--work", str(WORK / f"{name}-mutant")])
        if expected == "SETUP":
            plain_ok = plain.returncode == 2 and "DEFECT SETUP" in plain.stdout
        else:
            plain_ok = plain.returncode == 1 and expected in plain.stdout
        mutant_ok = "PREDICATE R85-C1 pass" in mutant.stdout and mutant.returncode == 0
        record(name, fixture, expected, plain, mutant, plain_ok, mutant_ok, root)

    for name, needle, replacement, fixture, check_name in C2_SPECS:
        if built[name] is None:
            continue
        repo, commit = c2_fixture(fixture)
        if check_name:
            plain_argv = [PY, "-I", "-B", str(PRISTINE / "c2.py"), "--lane", str(repo),
                          "--rev", commit, "--check-only", check_name,
                          "--work", str(WORK / f"{name}-plain")]
            mutant_argv = [PY, "-I", "-B", str(built[name]), "--lane", str(repo),
                           "--rev", commit, "--check-only", check_name,
                           "--work", str(WORK / f"{name}-mutant")]
            plain = run(plain_argv)
            mutant = run(mutant_argv)
            plain_ok = plain.returncode == 1 and "DEFECT" in plain.stdout
            mutant_ok = mutant.returncode == 0 and f"CHECK {check_name} ok" in mutant.stdout
            record(name, f"{fixture}@{commit[:12]}", f"CHECK {check_name}",
                   plain, mutant, plain_ok, mutant_ok, repo,
                   extra={"plain_argv": plain_argv[1:], "mutant_argv": mutant_argv[1:]})
        else:
            plain_argv = [PY, "-I", "-B", str(PRISTINE / "c2.py"), "--lane", str(repo),
                          "--rev", commit, "--work", str(WORK / f"{name}-plain")]
            mutant_argv = [PY, "-I", "-B", str(built[name]), "--lane", str(repo),
                           "--rev", commit, "--work", str(WORK / f"{name}-mutant")]
            plain = run(plain_argv)
            mutant = run(mutant_argv)
            plain_ok = plain.returncode == 1 and "indexed=no" in plain.stdout
            mutant_ok = mutant.returncode == 0 and "PREDICATE R85-C2 pass" in mutant.stdout
            record(name, f"{fixture}@{commit[:12]}", "TARGET indexed",
                   plain, mutant, plain_ok, mutant_ok, repo,
                   extra={"plain_argv": plain_argv[1:], "mutant_argv": mutant_argv[1:]})

    summary = {"pin": PIN, "pristine": {p.name: sha(p) for p in sorted(PRISTINE.glob("*.py"))},
               "results": results}
    OUT.write_text(json.dumps(summary, indent=2) + "\n",
                                             encoding="utf-8")
    necessary = sum(1 for row in results if row["verdict"] == "necessary")
    redundant = sum(1 for row in results if row["verdict"] == "redundant")
    print(f"BATTERY real={len(results)} necessary={necessary} redundant={redundant} "
          f"inconclusive={len(results) - necessary - redundant}")
    return 0 if all(row["verdict"] != "inconclusive" for row in results) else 1


def record(name, fixture, expected, plain, mutant, plain_ok, mutant_ok, root, extra=None):
    if plain_ok and mutant_ok:
        verdict = "necessary"
    elif not plain_ok:
        verdict = "inconclusive"
    else:
        verdict = "redundant"
    row = {
        "mutant": name, "fixture": fixture, "expected_unmutated": expected,
        "unmutated_rc": plain.returncode, "mutated_rc": mutant.returncode,
        "unmutated_rejected": plain_ok, "mutant_accepted": mutant_ok,
        "verdict": verdict,
        "unmutated_stdout": plain.stdout.strip(),
        "mutated_stdout": mutant.stdout.strip(),
        "fixture_root": str(root),
        "mutations": META_REF[name],
    }
    if extra:
        row.update(extra)
    results.append(row)
    tail = " ".join(ln for ln in mutant.stdout.strip().splitlines()[-2:])
    print(f"MUTANT {name} fixture={fixture} unmutated_rc={plain.returncode} "
          f"unmutated_rejected={plain_ok} mutant_rc={mutant.returncode} "
          f"mutant_accepted={mutant_ok} verdict={verdict}")
    print(f"  mutant_tail: {tail}")
    return row


META_REF: dict = {}


if __name__ == "__main__":
    for path in (S / "tmp", MUTANTS, WORK, FIXTURES):
        path.mkdir(parents=True, exist_ok=True)
    _, meta = build_mutants()
    META_REF.update(meta)
    sys.exit(main())
