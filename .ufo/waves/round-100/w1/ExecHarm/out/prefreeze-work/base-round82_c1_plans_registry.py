#!/usr/bin/env python3
"""R82-C1 counter — registry completeness in the direction no counter has priced.

Frozen before data on 2026-11-04 (L1 KengakuR82); see plans/round-82-claims.md §R82-C1. The
universe is derived from bytes at BASE_REV, never listed; the registry is read at the measured tip.

Universe (derived, printed every run):
    U = plans/**/*.py that exist at BASE_REV, outside plans/fixtures/ (support code since round 52,
        plans/round52_c2_registry.py:35), and are referenced as a literal path by SCORECARD.md,
        LOG.md or corpus/README.md at BASE_REV
    registered = scripts named by a registry row's ENTRY cell at the tip
    for p in U:  p in registered            -> ok
                 EXCLUSIONS[p].class verified from p's bytes at BASE_REV -> excluded
                 else                        -> MISSING   (a CLI instrument with no row)
                                                UNCLASSIFIED (an unreferenced support module)

    reverse leg: every registry row's entry cell names a script that exists at BASE_REV
                 (ENTRY-MISSING otherwise) — the audit must not buy the forward direction by
                 breaking the other one.
    row-quality leg: every row that is NOT present at BASE_REV (i.e. added at the tip) has eight
                 non-empty cells, kind in {gate, probe}, an entry naming a script that exists and
                 `ast.parse`s, a gate map declaring `0` and (`1` or a failed class), a probe map
                 declaring `0`, a self-test cell naming a script+flag present in that script or the
                 literal `none declared`, and pinned-values / write-scope cells non-empty and not
                 `n/a`.

    python3 plans/round82_c1_plans_registry.py --lane .                    # verdict
    python3 plans/round82_c1_plans_registry.py --lane . --tip REV          # rows read at another tip
    python3 plans/round82_c1_plans_registry.py --selftest --work DIR
    python3 plans/round82_c1_plans_registry.py --mutants --work DIR
    python3 plans/round82_c1_plans_registry.py --control-empty-rows --work DIR
    python3 plans/round82_c1_plans_registry.py --control-exclude-cli --work DIR
    python3 plans/round82_c1_plans_registry.py --control-name-only --work DIR

Printed: UNIVERSE / MISSING / UNCLASSIFIED / ROW / EXCLUSION / ENTRY-MISSING / ROWS / DEFECT /
DEFECTS n= / TARGET / PREDICATE. Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_REV = "a3a03ac31451e58f1742b9bccb73b72c2d90a95c"   # round-82 base (round-81 tip)
DOCS = ("SCORECARD.md", "LOG.md", "corpus/README.md")
REGISTRY_HEADING = "## Gate/probe registry"
SCRIPT_RE = re.compile(r"(plans/[A-Za-z0-9_./-]+\.py)")
CMD_RE = re.compile(r"python3\s+(plans/[A-Za-z0-9_./-]+\.py)")
SELFTEST_RE = re.compile(r"python3\s+(?:-B\s+)?(plans/[A-Za-z0-9_./-]+\.py)([^`|]*)")
FLAG_RE = re.compile(r"(--[a-z][a-z0-9-]*)")
KINDS = ("gate", "probe")
NA = {"n/a", "n.a.", "na", "-", "none"}
# The frozen exclusion table: a path here must prove it cannot be a CLI instrument from its own
# bytes at BASE_REV (no argparse import, no __main__ block). A CLI script cannot be excluded.
EXCLUSIONS_FILE = "plans/round82-exclusions.json"   # absent at BASE_REV by design
EXCLUSIONS: dict[str, str] = {}


def load_exclusions(lane: Path) -> dict[str, str]:
    fp = lane / EXCLUSIONS_FILE
    if not fp.is_file():
        return {}
    try:
        doc = json.loads(fp.read_text())
    except Exception:
        return {}
    out = {}
    for path, meta in (doc.get("exclusions") or {}).items():
        if isinstance(meta, dict) and meta.get("class") == "support-module":
            out[path] = meta["class"]
    return out
ADDED_CHECK = True


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def show(root: Path, rev: str, rel: str) -> str | None:
    p = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{rel}"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def tracked(root: Path, rev: str) -> set[str]:
    return set(git(root, "ls-tree", "-r", "--name-only", rev).split())


def registry_block(text: str):
    lines = text.split("\n")
    st = [i for i, l in enumerate(lines) if l.startswith(REGISTRY_HEADING)]
    if not st:
        return None
    st = st[0]
    en = next((i for i in range(st + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[st:en]


def parse_rows(block) -> list[list[str]]:
    rows = []
    for line in block:
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8:
            rows.append(cells)
    return rows


def has_cli(body: str) -> bool:
    if "argparse" in body:
        return True
    return bool(re.search(r"if\s+__name__\s*==", body))


def parses(body: str) -> bool:
    try:
        ast.parse(body)
        return True
    except SyntaxError:
        return False


def row_defects(cells: list[str], lane: Path, files: set[str], bodies: dict) -> list[str]:
    out = []
    name = cells[0].strip("`")
    if any(not c for c in cells):
        out.append("INCOMPLETE")
    kind = cells[1].strip().lower()
    if kind not in KINDS:
        out.append("KIND")
    m = CMD_RE.search(cells[2])
    if not m:
        out.append("ENTRY")
    else:
        rel = m.group(1)
        if rel not in files:
            out.append("ENTRY-MISSING")
        elif not parses(bodies.get(rel, "")):
            out.append("ENTRY-UNPARSED")
    vm = cells[3]
    if kind == "gate":
        if "`0`" not in vm or ("`1`" not in vm and "failed" not in vm):
            out.append("VERDICT-MAP")
    elif kind == "probe" and "`0`" not in vm:
        out.append("VERDICT-MAP")
    st = cells[4]
    if "none declared" not in st:
        sm = SELFTEST_RE.search(st)
        if not sm:
            out.append("SELFTEST-UNBACKED")
        else:
            rel = sm.group(1)
            if rel not in files:
                out.append("SELFTEST-UNBACKED")
            else:
                flags = FLAG_RE.findall(sm.group(2))
                body = bodies.get(rel, "")
                for f in flags:
                    if f not in body:
                        out.append("SELFTEST-FLAG:%s" % f)
                        break
    for leg, cell in (("PINS", cells[5]), ("SCOPE", cells[6])):
        if not cell or cell.strip().lower() in NA:
            out.append("%s-EMPTY" % leg)
    if not cells[7].lower().startswith("kengaku"):
        out.append("OWNER")
    return out


def evaluate(lane: Path, tip: str | None, collect=None, base_rev: str = BASE_REV) -> int:
    global EXCLUSIONS
    EXCLUSIONS = load_exclusions(lane)
    defects: list[tuple[str, str]] = []
    tip = tip or (git(lane, "rev-parse", "master").strip() or "HEAD")
    base_files = tracked(lane, base_rev)
    tip_files = tracked(lane, tip) | set(git(lane, "ls-files").split())
    skill = show(lane, tip, "SKILL.md") if tip != "WORKTREE" else (lane / "SKILL.md").read_text(errors="replace")
    if skill is None:
        skill = (lane / "SKILL.md").read_text(errors="replace")
    block = registry_block(skill)
    if block is None:
        print("SETUP no %r section in SKILL.md" % REGISTRY_HEADING)
        return 2
    rows = parse_rows(block)
    if not rows:
        print("SETUP registry has no eight-cell rows")
        return 2
    base_skill = show(lane, base_rev, "SKILL.md") or ""
    base_block = registry_block(base_skill) or []
    base_rows = parse_rows(base_block)
    base_names = {r[0].strip("`") for r in base_rows}
    registered = set()
    for r in rows:
        m = CMD_RE.search(r[2])
        if m:
            registered.add(m.group(1))
    # universe at BASE
    refs: set[str] = set()
    for doc in DOCS:
        text = show(lane, base_rev, doc) or ""
        refs |= set(SCRIPT_RE.findall(text))
    uni = sorted(p for p in refs
                 if p in base_files and p.endswith(".py")
                 and not p.startswith("plans/fixtures/"))
    base_body = {p: (show(lane, base_rev, p) or "") for p in set(uni) | registered | {x for r in rows for x in SCRIPT_RE.findall(r[2])}}
    print("UNIVERSE documents=%d instruments=%d referenced=%d registered=%d base_scripts=%d" % (
        len(DOCS), len([p for p in base_files if p.startswith("plans/") and p.endswith(".py")]),
        len(uni), len(registered), len(base_body)))
    for p in uni:
        if p in registered:
            continue
        if p in EXCLUSIONS:
            body = base_body.get(p, "")
            if has_cli(body):
                defects.append(("EXCLUSION-CLI", p))
                continue
            print("EXCLUSION %s class=%s cli=no" % (p, EXCLUSIONS[p]))
        else:
            if has_cli(base_body.get(p, "")):
                defects.append(("MISSING", p))
                print("MISSING %s" % p)
            else:
                defects.append(("UNCLASSIFIED", p))
                print("UNCLASSIFIED %s" % p)
    # reverse leg
    for r in rows:
        m = CMD_RE.search(r[2])
        if not m:
            continue
        rel = m.group(1)
        if r[0].strip("`") not in base_names:
            if rel not in tip_files and not (lane / rel).is_file():
                defects.append(("ENTRY-MISSING", "%s %s" % (r[0].strip("`"), rel)))
                print("ENTRY-MISSING %s %s" % (r[0].strip("`"), rel))
            continue
        if rel not in base_files and rel not in tip_files:
            defects.append(("ENTRY-MISSING", "%s %s" % (r[0].strip("`"), rel)))
            print("ENTRY-MISSING %s %s" % (r[0].strip("`"), rel))
    # row-quality leg on rows added at the tip
    if ADDED_CHECK:
        for r in rows:
            name = r[0].strip("`")
            if name in base_names:
                continue
            bodies = dict(base_body)
            for rel in set(SCRIPT_RE.findall(" ".join(r))):
                if not bodies.get(rel) and (lane / rel).is_file():
                    bodies[rel] = (lane / rel).read_text(errors="replace")
            files = set(base_files) | set(tip_files) | {rel for rel in set(SCRIPT_RE.findall(" ".join(r)))
                                                         if (lane / rel).is_file()}
            ds = row_defects(r, lane, files, bodies)
            print("ROW %s kind=%s entry=%s selftest=%s defects=%s" % (
                name, r[1].strip().lower(),
                (CMD_RE.search(r[2]).group(1) if CMD_RE.search(r[2]) else "-"),
                ("none" if "none declared" in r[4] else (SELFTEST_RE.search(r[4]).group(1) if SELFTEST_RE.search(r[4]) else "-")),
                ",".join(ds) if ds else "none"))
            for d in ds:
                defects.append(("ROW-" + d, name))
    names = [r[0].strip("`") for r in rows]
    for n in sorted({x for x in names if names.count(x) > 1}):
        defects.append(("DUPLICATE", n))
    for p in sorted(EXCLUSIONS):
        if p in registered:
            defects.append(("EXCLUDED-BUT-REGISTERED", p))
        elif not (lane / p).is_file() and p not in base_files and p not in tip_files:
            defects.append(("PHANTOM-EXCLUSION", p))
    print("ROWS registry=%d base=%d duplicates=%d" % (len(rows), len(base_rows), len(names) - len(set(names))))
    for code, detail in defects:
        print("DEFECT %s %s" % (code, detail))
    print("DEFECTS n=%d" % len(defects))
    n_missing = sum(1 for c, _ in defects if c in ("MISSING", "UNCLASSIFIED", "EXCLUSION-CLI"))
    n_entry = sum(1 for c, _ in defects if c == "ENTRY-MISSING")
    miss_set = {d for c, d in defects if c == "MISSING"}
    unclass_set = {d for c, d in defects if c == "UNCLASSIFIED"}
    n_missing = len(miss_set)
    n_unclass = len(unclass_set)
    n_excl = len([p for p in uni if p not in registered and p in EXCLUSIONS and not has_cli(base_body.get(p, ""))])
    print("TARGET missing=%d unclassified=%d excluded=%d rows=%d entry_missing=%d" % (
        n_missing, n_unclass, n_excl, len(rows), n_entry))
    ok = not defects
    print("PREDICATE R82-C1 %s" % ("pass" if ok else "fail"))
    if collect is not None:
        collect.update({"defects": defects, "rows": len(rows), "universe": uni, "registered": registered})
    return 0 if ok else 1


def _write(root: Path, rel: str, body: str) -> None:
    q = root / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_text(body)


def fixture(root: Path, mode: str = "green") -> str:
    """Two-commit fixture lane: BASE has the advertised scripts and one row; TIP adds rows.

    Returns the base revision so the counter prices exactly the rows the fixture adds.
    """
    tool_a = ("import argparse\nap = argparse.ArgumentParser()\n"
              "ap.add_argument('--selftest', action='store_true')\n"
              "if __name__ == '__main__':\n    pass\n")
    if mode == "selftest-unbacked":
        tool_a = "import argparse\nif __name__ == '__main__':\n    pass\n"
    _write(root, "SCORECARD.md", "see `plans/tool_a.py`\n")
    _write(root, "LOG.md", "see `plans/tool_b.py`\n")
    _write(root, "corpus/README.md", "see `plans/support_mod.py`\n")
    _write(root, "plans/tool_a.py", tool_a)
    _write(root, "plans/tool_b.py", "import argparse\nif __name__ == '__main__':\n    pass\n")
    _write(root, "plans/support_mod.py", "CASES = ()\n")
    _write(root, "plans/backer.py", "import argparse\nif __name__ == '__main__':\n    pass\n")
    header = ["| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |",
              "|---|---|---|---|---|---|---|---|"]
    backer = "| `backer` | gate | `python3 plans/backer.py --lane .` | `0` clean · `1` failed | none declared | x | y | kengaku |"
    if mode == "drop-entry":
        backer = "| `backer` | gate | `python3 plans/absent.py --lane .` | `0` clean · `1` failed | none declared | x | y | kengaku |"
    _write(root, "SKILL.md", "# SKILL\n\n" + REGISTRY_HEADING + "\n\n" + "\n".join(header + [backer]) + "\n")
    if mode != "no-exclusions":
        _write(root, EXCLUSIONS_FILE, json.dumps({"exclusions": {"plans/support_mod.py": {"class": "support-module", "reason": "fx"}}}))
    git_init(root)
    base = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    # tip adds the rows (and, for the laundering control, the exclusion lie)
    rows = [
        "| `tool-a` | gate | `python3 plans/tool_a.py --lane .` | `0` clean · `1` failed | `python3 plans/tool_a.py --selftest` | pins | read-only | kengaku |",
        "| `tool-b` | probe | `python3 plans/tool_b.py --lane .` | `0` completed | none declared | pins | read-only | kengaku |",
    ]
    if mode == "missing-row":
        rows = rows[:1]
    if mode == "empty-cells":
        rows = ["| `tool-a` | gate | `python3 plans/tool_a.py --lane .` | n/a | n/a | n/a | n/a | kengaku |"]
    if mode == "verdict-map":
        rows[0] = rows[0].replace("`0` clean · `1` failed", "`0` clean")
    if mode == "excluded-cli":
        rows = rows[1:]
        _write(root, EXCLUSIONS_FILE, json.dumps({"exclusions": {
            "plans/support_mod.py": {"class": "support-module", "reason": "fx"},
            "plans/tool_a.py": {"class": "support-module", "reason": "lied about"}}}))
    if mode == "prose-only":
        rows = []
        _write(root, "plans/round-9-claims.md", "run `python3 plans/tool_a.py --lane .`\n")
    if rows:
        _write(root, "SKILL.md", (root / "SKILL.md").read_text() + "\n".join(rows) + "\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=k", "-c", "user.email=k@k", "commit", "-qm", "tip"], check=True)
    return base


def git_init(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=k", "-c", "user.email=k@k", "commit", "-qm", "fx"], check=True)


CASES_SELFTEST = (
    ("green", "green", 0),
    ("missing-row", "missing-row", 1),
    ("empty-cells", "empty-cells", 1),
    ("drop-entry", "drop-entry", 1),
    ("excluded-cli", "excluded-cli", 1),
    ("prose-only", "prose-only", 1),
    ("selftest-unbacked", "selftest-unbacked", 1),
    ("verdict-map", "verdict-map", 1),
)


def _run_case(work: Path, mode: str) -> int:
    root = Path(tempfile.mkdtemp(dir=work))
    base = fixture(root, mode)
    rc = evaluate(root, None, base_rev=base)
    shutil.rmtree(root, ignore_errors=True)
    return rc


def selftest(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    failures = 0
    reds = 0
    for name, mode, want in CASES_SELFTEST:
        rc = _run_case(work, mode)
        if rc != 0:
            reds += 1
        if rc != want:
            failures += 1
            print("CASE %s FAIL want_rc=%d got_rc=%d" % (name, want, rc))
        else:
            print("CASE %s ok" % name)
    print("SELFTEST cases=%d red=%d failures=%d" % (len(CASES_SELFTEST), reds, failures))
    return 0 if failures == 0 else 1


def mutants(work: Path) -> int:
    work.mkdir(parents=True, exist_ok=True)
    killed = survived = 0
    for name, mode, want in CASES_SELFTEST:
        if want == 0:
            continue
        rc = _run_case(work, mode)
        if rc != 0:
            killed += 1
            print("MUTANT %s killed" % name)
        else:
            survived += 1
            print("MUTANT %s SURVIVED" % name)
    print("MUTANTS real=%d killed=%d survived=%d" % (killed + survived, killed, survived))
    return 0 if survived == 0 else 1


def control(work: Path, kind: str) -> bool:
    mode = {"empty-rows": "empty-cells", "exclude-cli": "excluded-cli", "name-only": "prose-only"}[kind]
    return _run_case(work, mode) != 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="R82-C1 registry-completeness counter")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--tip", default=None)
    ap.add_argument("--base", default=BASE_REV)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-empty-rows", action="store_true")
    ap.add_argument("--control-exclude-cli", action="store_true")
    ap.add_argument("--control-name-only", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest or a.mutants or a.control_empty_rows or a.control_exclude_cli or a.control_name_only:
        if not a.work:
            print("SETUP --work required")
            return 2
        w = Path(a.work)
        if a.selftest:
            return selftest(w)
        if a.mutants:
            return mutants(w)
        kind = ("empty-rows" if a.control_empty_rows else
                "exclude-cli" if a.control_exclude_cli else "name-only")
        lost = control(w, kind)
        print("CONTROL %s caught=%s target_reached=%s" % (kind, lost, "False" if lost else "True"))
        return 0 if lost else 1
    lane = Path(a.lane).resolve()
    return evaluate(lane, a.tip, base_rev=a.base)


if __name__ == "__main__":
    sys.exit(main())
