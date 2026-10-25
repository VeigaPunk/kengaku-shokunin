#!/usr/bin/env python3
"""Red fixtures for the frozen round-27 P4 population (C2, state_check v4).

Exports base b5719440 with `git archive` into a temp directory, applies one
minimal token mutation per P4 class (recipes: plans/fixtures/r27/p4_mutants/
P4a..P4e.json), and runs a state_check checker on each mutant with
`--root MUTANT --json`.

A mutant is RED for class Px only when the checker exits 1 and emits a MISMATCH
whose id starts with `Px.` and whose (id, observed) pair is absent from the
unmutated base's MISMATCH set. A base-stale Px mismatch therefore cannot make a
mutant look detected; the base control's per-class counts are printed.

Exit: 0 every mutant red; 1 any mutant not red (missed, unattributable, or a
recipe that does not apply exactly once); 2 usage, export, or unusable control.
Stdlib only. Writes only under a temp directory, removed unless --keep.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

BASE = "b5719440e5eee46c1886fddbdf7bdc1624829454"
CLASSES = ("P4a", "P4b", "P4c", "P4d", "P4e")
HERE = Path(__file__).resolve().parent
RECIPE_DIR = HERE / "p4_mutants"
DEFAULT_REPO = HERE.parents[2]
ANCHOR_FILES = (
    "SCORECARD.md", "SHONEN.md", "PROVINCE.md", "corpus/README.md",
    "corpus/SOURCES.md", "corpus/lessons/round-26.md",
    "corpus/knowledge/grader-perturbation-audit.md",
    "corpus/evidence/round26-calibration/state-check-final.txt",
    "plans/fixtures/r25/shonen-seed.txt", ".ufo/waves/round-26/build-spec.json",
)
CHECKER_TIMEOUT_S = 1200


class SetupError(Exception):
    """Unusable export, recipe set, or control: exit 2."""


class RecipeError(Exception):
    """Recipe does not apply exactly once: that mutant is not red (exit 1)."""


def class_of(assertion_id: str) -> str:
    return assertion_id.split(".", 1)[0]


def load_recipes() -> list[dict]:
    recipes: list[dict] = []
    for path in sorted(RECIPE_DIR.glob("*.json")):
        try:
            recipe = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise SetupError(f"unreadable recipe {path.name}: {exc}") from exc
        recipe["_source"] = path.name
        recipes.append(recipe)
    found = sorted(str(r.get("class")) for r in recipes)
    if found != sorted(CLASSES):
        raise SetupError(f"recipes must be exactly {list(CLASSES)}; found {found}")
    for r in recipes:
        valid = bool(r.get("file")) and bool(r.get("anchor")) and r.get("op") in ("replace", "delete_line")
        if r.get("op") == "replace":
            valid = valid and bool(r.get("old")) and "new" in r and r["old"] != r["new"]
        if not valid:
            raise SetupError(f"malformed recipe {r['_source']}")
    return sorted(recipes, key=lambda r: r["class"])


def export_base(repo: Path, base: str, dest: Path) -> None:
    listing = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only", base],
                             capture_output=True, check=False)
    if listing.returncode != 0:
        raise SetupError(f"git ls-tree {base[:12]}: {listing.stderr.decode(errors='replace').strip()}")
    archive = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", base],
                             capture_output=True, check=False)
    if archive.returncode != 0:
        raise SetupError(f"git archive {base[:12]}: {archive.stderr.decode(errors='replace').strip()}")
    dest.mkdir(parents=True)
    extra = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        tar.extractall(dest, **extra)
    expected = {name for name in listing.stdout.decode("utf-8").split("\0") if name}
    actual = {os.path.relpath(os.path.join(d, f), dest)
              for d, _, files in os.walk(dest) for f in files}
    if expected != actual:
        raise SetupError(f"export differs from ls-tree: missing={sorted(expected - actual)[:3]} "
                         f"extra={sorted(actual - expected)[:3]}")
    absent = [name for name in ANCHOR_FILES if not (dest / name).is_file()]
    if absent:
        raise SetupError(f"export lacks anchor files: {absent}")


def apply_recipe(tree: Path, recipe: dict) -> int:
    target = tree / recipe["file"]
    try:
        original = target.read_bytes().decode("utf-8").split("\n")
    except (OSError, UnicodeError) as exc:
        raise RecipeError(f"{recipe['file']}: not readable as UTF-8 text ({exc})") from exc
    hits = [i for i, line in enumerate(original) if recipe["anchor"] in line]
    if len(hits) != 1:
        raise RecipeError(f"{recipe['file']}: anchor matches {len(hits)} lines, need exactly 1")
    index = hits[0]
    mutated = list(original)
    if recipe["op"] == "replace":
        occurrences = original[index].count(recipe["old"])
        if occurrences != 1:
            raise RecipeError(f"{recipe['file']}:{index + 1}: old text occurs {occurrences}x, need 1")
        mutated[index] = original[index].replace(recipe["old"], recipe["new"], 1)
    else:
        del mutated[index]
    target.write_bytes("\n".join(mutated).encode("utf-8"))
    return index + 1


def run_checker(checker: Path, root: Path) -> dict:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result: dict = {"exit": None, "parsed": False, "mismatch": [], "summary": {}, "note": ""}
    try:
        proc = subprocess.run([sys.executable, str(checker), "--root", str(root), "--json"],
                              cwd=str(root), capture_output=True, env=env,
                              timeout=CHECKER_TIMEOUT_S, check=False)
    except subprocess.TimeoutExpired:
        result["note"] = f"timeout after {CHECKER_TIMEOUT_S}s"
        return result
    result["exit"] = proc.returncode
    result["note"] = proc.stderr.decode("utf-8", errors="replace").strip()[-300:]
    try:
        data = json.loads(proc.stdout.decode("utf-8", errors="replace"))
        assertions = data["assertions"]
        result["summary"] = data["summary"]
    except (ValueError, KeyError, TypeError):
        return result
    result["parsed"] = True
    result["mismatch"] = sorted({(a["id"], json.dumps(a["observed"], ensure_ascii=False, sort_keys=True))
                                 for a in assertions if a.get("verdict") == "MISMATCH"})
    return result


def judge(cls: str, control: dict, mutant: dict) -> dict:
    base_pairs = {tuple(pair) for pair in control["mismatch"]}
    named = [pair for pair in mutant["mismatch"] if class_of(pair[0]) == cls]
    new = [pair[0] for pair in named if tuple(pair) not in base_pairs]
    return {"named": len(named), "new": new,
            "red": bool(mutant["parsed"] and mutant["exit"] == 1 and new)}


def describe(recipe: dict) -> str:
    if recipe["op"] == "replace":
        return f"replace {recipe['old']!r} -> {recipe['new']!r}"
    return "delete_line"


def run_all(args: argparse.Namespace, checker: Path, tmp: Path) -> tuple[int, dict]:
    recipes = load_recipes()
    base_tree = tmp / "base"
    export_base(args.repo.expanduser().resolve(), args.base, base_tree)
    control = run_checker(checker, base_tree)
    if control["exit"] not in (0, 1) or not control["parsed"]:
        raise SetupError(f"checker unusable on unmutated base (exit={control['exit']}): {control['note']}")
    per_class = {cls: sum(1 for pair in control["mismatch"] if class_of(pair[0]) == cls) for cls in CLASSES}
    rows: list[dict] = []
    for recipe in recipes:
        cls = recipe["class"]
        row: dict = {"class": cls, "file": recipe["file"], "op": recipe["op"],
                     "edit": describe(recipe), "red": False}
        tree = tmp / f"mut-{cls}"
        shutil.copytree(base_tree, tree)
        try:
            row["line"] = apply_recipe(tree, recipe)
        except RecipeError as exc:
            row["error"] = str(exc)
            rows.append(row)
            continue
        mutant = run_checker(checker, tree)
        row.update(judge(cls, control, mutant))
        row["checker_exit"] = mutant["exit"]
        if not mutant["parsed"]:
            row["note"] = mutant["note"]
        rows.append(row)
    red = sum(1 for row in rows if row["red"])
    report = {
        "base": args.base, "checker": str(checker),
        "control": {"exit": control["exit"], "summary": control["summary"],
                    "mismatch": len(control["mismatch"]), "per_class": per_class},
        "mutants": rows, "red": red, "total": len(CLASSES),
    }
    return (0 if red == len(CLASSES) and len(rows) == len(CLASSES) else 1), report


def emit(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return
    control = report["control"]
    summary = " ".join(f"{k}={v}" for k, v in (control["summary"] or {}).items())
    per = " ".join(f"{k}={v}" for k, v in control["per_class"].items())
    print(f"CONTROL base={report['base'][:12]} checker_exit={control['exit']} {summary} "
          f"control_mismatch={control['mismatch']} control_per_class[{per}]")
    for row in report["mutants"]:
        if "error" in row:
            print(f"MUTANT {row['class']} {row['file']} RECIPE-ERROR: {row['error']} -> MISSED")
            continue
        verdict = "RED" if row["red"] else "MISSED"
        print(f"MUTANT {row['class']} {row['file']}:{row['line']} {row['edit']} "
              f"checker_exit={row['checker_exit']} named={row['named']} new={len(row['new'])} {verdict}")
        if row["new"]:
            print("    new: " + ", ".join(row["new"][:3]))
        if row.get("note"):
            print("    checker-stderr: " + row["note"].splitlines()[-1][:160])
    print(f"VERDICT: {report['red']}/{report['total']} mutants red for their own class "
          f"-> exit {0 if report['red'] == report['total'] else 1}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checker", required=True, type=Path,
                        help="state_check.py to run on each mutant (v3 or v4 CLI)")
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO,
                        help="git repository holding the base commit (default: this clone)")
    parser.add_argument("--base", default=BASE, help="base commit (default: b5719440)")
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    parser.add_argument("--keep", action="store_true", help="keep the temp directory")
    args = parser.parse_args(argv)
    checker = args.checker.expanduser().resolve()
    if not checker.is_file():
        print(f"p4_mutate: USAGE: --checker is not a file: {checker}", file=sys.stderr)
        return 2
    tmp = Path(tempfile.mkdtemp(prefix="p4mut-"))
    report: dict | None = None
    try:
        code, report = run_all(args, checker, tmp)
    except SetupError as exc:
        print(f"p4_mutate: SETUP: {exc}", file=sys.stderr)
        code = 2
    finally:
        if args.keep:
            print(f"p4_mutate: kept temp directory {tmp}", file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    if report is not None:
        emit(report, args.json)
    return code


if __name__ == "__main__":
    sys.exit(main())
