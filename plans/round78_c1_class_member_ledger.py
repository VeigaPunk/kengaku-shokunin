#!/usr/bin/env python3
"""R78-C1 counter — the three partially-executed grader classes become a machine-checked member
ledger: every member accounted once, every executed member's receipt printing its passing verdict at
the measured revision, every unexecuted member's reason backed by a frozen detector over that task's
stored grader bytes, and the three SKILL.md class rows carrying `executed k of n` plus the pointer.

Frozen before data on 2026-11-04 (L1 KengakuR78); see plans/round-78-claims.md §R78-C1.

    python3 plans/round78_c1_class_member_ledger.py --lane .                  # verdict, worktree
    python3 plans/round78_c1_class_member_ledger.py --lane . --rev 3ae0ab54   # bytes at a revision
    python3 plans/round78_c1_class_member_ledger.py --selftest --work DIR     # fixture battery
    python3 plans/round78_c1_class_member_ledger.py --mutants --work DIR      # attributed mutants
    python3 plans/round78_c1_class_member_ledger.py --control-prose --work DIR # the skip that loses

Why this counter exists: `SKILL.md` §Decision table — grader class states `executed 4 of 8`,
`2 of 3` and `1 of 2` as prose over the round-62 census population
(`corpus/evidence/round62/class-survey.txt`). Nothing named the members or falsified an
`unexecuted` reason. The ledger `plans/grader-selected-members.json` does; this counter is its gate.

Universe (derived, never listed): classes := rows of `SKILL.md` whose `executed` cell matches
`executed <k> of <n>`; members := that class's `members=` list in the census receipt.

Ledger row (one per member, JSON object under `members`):
    {"status": "executed"|"unexecuted", "classes": [...], "round": 78,
     "receipt": "corpus/evidence/...", "predicate": "R70-C1", "reason": "browser-required"}

Detectors are frozen HERE, not in the ledger: a reason code maps to one regex over the task's
stored grader bytes (`corpus/evidence/round52/graders/<member>/tests/test_outputs.py` + `test.sh`).
An `unexecuted` row whose detector does not fire is `REASON-UNBACKED`.

Printed lines (all defects fail the predicate):
    UNIVERSE classes=<n> members=<m> pairs=<p>
    LEDGER rows=<r> executed=<e> unexecuted=<u>
    MEMBER <name> <status> classes=<csv> receipt=<path|-> verdict=<token|-|reason>
    CLASS <name> k=<k> n=<n> census=<c> ledger_k=<k'>
    COVERAGE recomputed_covered=<C> census_covered=<12> recomputed_uncovered=<csv>
    DEFECT <CLASS> <detail>
    DEFECTS n=<n>
    TARGET classes=3 members=<m> executed=<e> unexecuted=<u> unaccounted=<n> unbacked=<n>
    PREDICATE R78-C1 pass|fail
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = "SKILL.md"
CENSUS = "corpus/evidence/round62/class-survey.txt"
LEDGER = "plans/grader-selected-members.json"
GRADERS = "corpus/evidence/round52/graders"
TABLE_HEADING = "## Decision table — grader class → offline replay recipe"
PARTIAL = re.compile(r"executed\s+(\d+)\s+of\s+(\d+)")
CELLSPLIT = re.compile(r"(?<!\\)\|")
LINK = "ledger=" + LEDGER
REASON_ENUM = (
    "browser-required",
    "vm-required",
    "network-install-required",
    "external-db-required",
    "candidate-library-required",
)
# Frozen detectors: reason code -> regex over the stored grader bytes (test_outputs.py + test.sh).
DETECTORS = {
    "browser-required": r"selenium|webdriver\.Chrome|webdriver\.Firefox|chromedriver",
    "vm-required": r"qemu-system|qemu-img|/app/isos/",
    "network-install-required": r"apt-get install|apt-get update|uvx \\\n|-w selenium==|pip install",
    "external-db-required": r"GOLDEN_SQL_PATH|/tests/golden\.sql|sha256\(DB_PATH\.read_bytes\(\)\)",
    "candidate-library-required": r"from headless_terminal import|import headless_terminal|sys\.path\.append\(\"/app\"\)",
}
VECTOR = re.compile(r"^VECTOR .*frozen=match$", re.M)
VECTOR_BAD = re.compile(r"frozen=mismatch")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Tree:
    """Uniform read interface over the worktree, a git revision, or a fixture directory."""

    def __init__(self, label: str, tip: str, getter, tracked, exists, symlink=None):
        self.label = label
        self.tip = tip
        self._get = getter
        self._tracked = tracked
        self._exists = exists
        self._symlink = symlink or (lambda rel: False)

    def get(self, rel: str) -> str | None:
        return self._get(rel)

    def tracked(self, rel: str) -> bool:
        return self._tracked(rel)

    def exists(self, rel: str) -> bool:
        return self._exists(rel)

    def symlink(self, rel: str) -> bool:
        return self._symlink(rel)


def rev_tree(lane: Path, rev: str) -> Tree:
    ref = "master^{commit}" if rev in ("worktree", "", None) else f"{rev}^{{commit}}"
    proc = git(lane, "rev-parse", "--verify", "--quiet", ref)
    tip = proc.stdout.strip() if proc.returncode == 0 else ""
    if not tip:
        raise SystemExit(f"SETUP unresolved revision {rev!r}")
    if rev in ("worktree", "", None):
        return Tree("worktree", tip,
                    lambda rel: _read_file(lane / rel),
                    lambda rel: git(lane, "ls-files", "--error-unmatch", "--", rel).returncode == 0,
                    lambda rel: (lane / rel).exists(),
                    lambda rel: (lane / rel).is_symlink())
    return Tree(rev, tip,
                lambda rel: _git_show(lane, tip, rel),
                lambda rel: git(lane, "cat-file", "-e", f"{tip}:{rel}").returncode == 0,
                lambda rel: git(lane, "cat-file", "-e", f"{tip}:{rel}").returncode == 0,
                lambda rel: git(lane, "cat-file", "-e", f"{tip}:{rel}").returncode == 0
                and git(lane, "ls-tree", f"{tip}", "--", rel).stdout.startswith("120000"))


def fx_tree(root: Path) -> Tree:
    return Tree("fixture", "fixture",
                lambda rel: _read_file(root / rel),
                lambda rel: (root / rel).is_file(),
                lambda rel: (root / rel).exists(),
                lambda rel: (root / rel).is_symlink())


def _read_file(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _git_show(lane: Path, tip: str, rel: str) -> str | None:
    proc = git(lane, "show", f"{tip}:{rel}")
    return proc.stdout if proc.returncode == 0 else None


def cells_of(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in CELLSPLIT.split(body)]


def skill_partial_rows(tree: Tree) -> tuple[list[tuple[str, int, int, str]], list[str]]:
    """Rows of the class table whose executed cell is `executed k of n`."""
    text = tree.get(SKILL) or ""
    if TABLE_HEADING not in text:
        return [], [f"DEFECT SETUP 0 no `{TABLE_HEADING}` section in {SKILL}"]
    block = text.split(TABLE_HEADING, 1)[1]
    block = block.split("\n## ", 1)[0]
    rows, defects = [], []
    fenced = False
    for line in block.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not line.lstrip().startswith("|"):
            continue
        cells = cells_of(line)
        if len(cells) < 3 or cells[0] in ("class", "") or set(cells[0]) <= set("-: "):
            continue
        m = PARTIAL.search(cells[2])
        if not m:
            continue
        k, n = int(m.group(1)), int(m.group(2))
        if k >= n:
            defects.append(f"DEFECT CLASS-NOT-PARTIAL {cells[0]} row claims executed {k} of {n}")
        rows.append((cells[0], k, n, cells[2]))
        if LINK not in cells[2]:
            defects.append(f"DEFECT CLASS-ROW-UNLINKED {cells[0]} executed cell carries no `{LINK}`")
    return rows, defects


def census_classes(tree: Tree) -> dict[str, tuple[int, list[str]]]:
    text = tree.get(CENSUS) or ""
    out: dict[str, tuple[int, list[str]]] = {}
    for line in text.splitlines():
        if not line.startswith("CLASS "):
            continue
        m = re.match(r"CLASS (\S+) count=(\d+) members=(.*)$", line)
        if not m:
            continue
        name, count, members = m.group(1), int(m.group(2)), m.group(3).strip()
        ids = [] if members in ("-", "") else [t.strip() for t in members.split(",") if t.strip()]
        out[name] = (count, ids)
    return out


def census_coverage(tree: Tree) -> tuple[int, list[str]]:
    text = tree.get(CENSUS) or ""
    for line in text.splitlines():
        if line.startswith("EXECUTED-COVERAGE "):
            covered = re.search(r"classes-covered=(\d+)", line)
            uncovered = re.search(r"classes-uncovered=(\S*)", line)
            return (int(covered.group(1)) if covered else 0,
                    [t for t in (uncovered.group(1) if uncovered else "").split(",") if t and t != "-"])
    return 0, []


def _no_dup_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate member key {key!r}")
        seen[key] = value
    return seen


def load_ledger(tree: Tree) -> tuple[dict, list[str]]:
    text = tree.get(LEDGER)
    if text is None:
        return {}, []
    try:
        data = json.loads(text, object_pairs_hook=_no_dup_keys)
    except ValueError as exc:
        code = "MEMBER-DUPLICATE" if "duplicate" in str(exc) else "SETUP"
        return {}, [f"DEFECT {code} 0 ledger rejected: {exc}"]
    except json.JSONDecodeError as exc:
        return {}, [f"DEFECT SETUP 0 ledger unparsable: {exc}"]
    members = data.get("members")
    if not isinstance(members, dict):
        return {}, [f"DEFECT SETUP 0 ledger has no `members` object"]
    return members, []


def grader_bytes(tree: Tree, member: str) -> str:
    parts = [tree.get(f"{GRADERS}/{member}/tests/test_outputs.py") or "",
             tree.get(f"{GRADERS}/{member}/tests/test.sh") or ""]
    return "\n".join(parts)


def verdict_token(receipt: str, predicate: str) -> tuple[str, bool]:
    """Executed evidence: the instrument's own passing verdict, printed in the receipt's bytes."""
    if f"PREDICATE {predicate} pass" in receipt:
        return "predicate", True
    if len(VECTOR.findall(receipt)) >= 2 and not VECTOR_BAD.search(receipt):
        return "vectors", True
    return "-", False


def audit(tree: Tree) -> tuple[list[str], list[str], dict]:
    report: list[str] = []
    defects: list[str] = []
    rows, row_defects = skill_partial_rows(tree)
    defects.extend(row_defects)
    census = census_classes(tree)
    covered_census, uncovered_census = census_coverage(tree)
    ledger, ledger_defects = load_ledger(tree)
    defects.extend(ledger_defects)

    universe: dict[str, list[str]] = {}
    pairs = 0
    for name, k, n, cell in rows:
        if name not in census:
            defects.append(f"DEFECT CLASS-NOT-IN-CENSUS {name} no `CLASS {name}` line in {CENSUS}")
            continue
        ccount, members = census[name]
        pairs += len(members)
        for member in members:
            universe.setdefault(member, []).append(name)
        if ccount != n:
            defects.append(f"DEFECT COUNT-DRIFT {name} class row n={n} census count={ccount}")
        if n != len(members):
            defects.append(f"DEFECT COUNT-DRIFT {name} census count={ccount} members listed={len(members)}")
    report.append(f"UNIVERSE classes={len(rows)} members={len(universe)} pairs={pairs}")
    if not rows or not universe:
        defects.append("DEFECT SETUP 0 universe empty (no partial-execution class row derived)")

    unaccounted = 0
    for member in sorted(universe):
        if member not in ledger:
            unaccounted += 1
            defects.append(f"DEFECT MEMBER-UNACCOUNTED {member} in classes {','.join(universe[member])}")
    for member in sorted(ledger):
        if member not in universe:
            defects.append(f"DEFECT MEMBER-EXTRA {member} not a member of any partially-executed class")

    executed = unexecuted = 0
    unbacked = 0
    per_class: dict[str, int] = {name: 0 for name, *_ in rows}
    for member in sorted(universe):
        row = ledger.get(member)
        if not isinstance(row, dict):
            continue
        status = row.get("status")
        classes = row.get("classes")
        if not isinstance(classes, list) or sorted(classes) != sorted(universe[member]):
            defects.append(
                f"DEFECT COUNT-DRIFT {member} ledger classes {classes!r} != universe {universe[member]!r}")
        if status == "executed":
            executed += 1
            receipt_rel = str(row.get("receipt") or "")
            predicate = str(row.get("predicate") or "")
            token = "-"
            if receipt_rel.startswith("/") or ".." in Path(receipt_rel).parts:
                defects.append(f"DEFECT RECEIPT-ESCAPE {member} receipt {receipt_rel!r} leaves the lane")
                receipt_rel = ""
            elif tree.symlink(receipt_rel):
                defects.append(f"DEFECT RECEIPT-SYMLINK {member} receipt {receipt_rel} is a symlink")
            elif receipt_rel and member.lower() not in (tree.get(receipt_rel) or "").lower() \
                    and f"TASK-UNDER-TEST {member}" not in (tree.get(receipt_rel) or ""):
                defects.append(f"DEFECT TASK-MISMATCH {member} receipt {receipt_rel} does not name the task")
            if not receipt_rel or not tree.exists(receipt_rel):
                defects.append(f"DEFECT RECEIPT-MISSING {member} {receipt_rel or '<none>'}")
            elif not tree.tracked(receipt_rel):
                defects.append(f"DEFECT RECEIPT-UNTRACKED {member} {receipt_rel}")
            else:
                token, ok = verdict_token(tree.get(receipt_rel) or "", predicate)
                if not ok:
                    defects.append(f"DEFECT PREDICATE-ABSENT {member} {receipt_rel} has no "
                                   f"`PREDICATE {predicate} pass` and no frozen vector table")
            rnd = row.get("round")
            if not isinstance(rnd, int) or not 1 <= rnd <= 78:
                defects.append(f"DEFECT ROUND-INVALID {member} round={rnd!r}")
            for name in universe[member]:
                per_class[name] += 1
            report.append(f"MEMBER {member} executed classes={','.join(universe[member])} "
                          f"receipt={receipt_rel} verdict={predicate} token={token}")
        elif status == "unexecuted":
            unexecuted += 1
            reason = row.get("reason")
            if reason not in REASON_ENUM:
                defects.append(f"DEFECT REASON-UNKNOWN {member} reason={reason!r}")
            elif not re.fullmatch(r"[A-Za-z0-9._-]+", member) or ".." in member:
                defects.append(f"DEFECT MEMBER-NAME-ESCAPE {member} not a census-shaped task name")
            else:
                blob = grader_bytes(tree, member)
                if not blob.strip():
                    defects.append(f"DEFECT REASON-UNBACKED {member} no stored grader bytes under "
                                   f"{GRADERS}/{member}/tests/")
                    unbacked += 1
                elif not re.search(DETECTORS[reason], blob):
                    defects.append(f"DEFECT REASON-UNBACKED {member} reason `{reason}` detector "
                                   f"does not fire on the stored grader bytes")
                    unbacked += 1
            report.append(f"MEMBER {member} unexecuted classes={','.join(universe[member])} "
                          f"receipt=- verdict=reason:{reason}")
        else:
            defects.append(f"DEFECT STATUS-UNKNOWN {member} status={status!r}")

    for name, k, n, _cell in rows:
        ledger_k = per_class.get(name, 0)
        ccount = census.get(name, (0, []))[0]
        report.append(f"CLASS {name} k={k} n={n} census={ccount} ledger_k={ledger_k}")
        if k != n and not (0 <= k < n):
            defects.append(f"DEFECT COUNT-DRIFT {name} class row k={k} outside 0..n-1 for a partial class")
        if ledger_k != k:
            defects.append(f"DEFECT COUNT-DRIFT {name} class row k={k} ledger executed={ledger_k}")
    report.append(f"LEDGER rows={len(ledger)} executed={executed} unexecuted={unexecuted}")

    promoted = []
    for name in uncovered_census:
        members = census.get(name, (0, []))[1]
        if any(isinstance(ledger.get(m), dict) and ledger[m].get("status") == "executed" for m in members):
            promoted.append(name)
    recomputed_covered = covered_census + len(promoted)
    recomputed_uncovered = [c for c in uncovered_census if c not in promoted]
    report.append(f"COVERAGE recomputed_covered={recomputed_covered} census_covered={covered_census} "
                  f"promoted={','.join(promoted) or '-'} "
                  f"recomputed_uncovered={','.join(recomputed_uncovered) or '-'}")
    for name, k, _n, _cell in rows:
        if k > 0 and per_class.get(name, 0) == 0:
            defects.append(f"DEFECT COVERAGE-REGRESSION {name} row claims k={k} > 0 but no ledger "
                           f"executed member backs it")

    stats = {"classes": len(rows), "members": len(universe), "executed": executed,
             "unexecuted": unexecuted, "unaccounted": unaccounted, "unbacked": unbacked}
    return report, defects, stats


def emit(tree: Tree, stats_target: bool, out: Path | None = None, dirty: bool = False) -> int:
    report, defects, stats = audit(tree)
    lines = [f"LANE_TIP {tree.tip}", f"WORKTREE {'dirty' if dirty else 'clean'}"] + report
    lines += defects
    lines.append(f"DEFECTS n={len(defects)}")
    if stats_target:
        lines.append(f"TARGET classes={stats['classes']} members={stats['members']} "
                     f"executed={stats['executed']} unexecuted={stats['unexecuted']} "
                     f"unaccounted={stats['unaccounted']} unbacked={stats['unbacked']}")
    ok = not defects and stats["classes"] > 0
    lines.append(f"PREDICATE R78-C1 {'pass' if ok else 'fail'}")
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    return 0 if ok else 1


# ------------------------------------------------------------------ fixtures
def build_fixture(root: Path, *, ledger_extra: str = "", drop_member: str = "",
                  break_receipt: str = "", bad_reason: str = "", drop_link: str = "",
                  kill_detector: str = "", regress_coverage: str = "") -> Path:
    if root.exists():
        shutil.rmtree(root)
    (root / "plans").mkdir(parents=True)
    (root / "corpus/evidence/round62").mkdir(parents=True)
    (root / "corpus/evidence/round52/graders").mkdir(parents=True)
    skill = f"""# fixture SKILL

{TABLE_HEADING}

| class | count | executed | replay recipe | receipt pointer |
|---|---|---|---|---|
| alpha | 2 | executed 1 of 2 ({LINK}) | r | `x` |
| beta | 3 | executed 2 of 3 ({LINK}) | r | `y` |
"""
    if drop_link:
        skill = skill.replace(f" ({LINK})", "")
    (root / SKILL).write_text(skill, encoding="utf-8")
    (root / CENSUS).write_text(
        "CLASS alpha count=2 members=a1,a2\n"
        "CLASS beta count=3 members=b1,b2,b3\n"
        "CLASS gamma count=1 members=g1\n"
        "EXECUTED-COVERAGE executed=1 classified=1 classes-covered=1 classes-uncovered=gamma\n",
        encoding="utf-8")
    ledger = {
        "members": {
            "a1": {"status": "executed", "classes": ["alpha"], "round": 70,
                   "receipt": "corpus/evidence/r/a1.txt", "predicate": "R70-C1"},
            "a2": {"status": "unexecuted", "classes": ["alpha"], "reason": "vm-required"},
            "b1": {"status": "executed", "classes": ["beta"], "round": 71,
                   "receipt": "corpus/evidence/r/b1.txt", "predicate": "R71-C1"},
            "b2": {"status": "executed", "classes": ["beta"], "round": 72,
                   "receipt": "corpus/evidence/r/b2.txt", "predicate": "R72-C1"},
            "b3": {"status": "unexecuted", "classes": ["beta"], "reason": "browser-required"},
        }
    }
    if drop_member:
        ledger["members"].pop(drop_member, None)
    if bad_reason:
        ledger["members"][bad_reason]["reason"] = "because-it-is-hard"
    (root / LEDGER).write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    (root / "corpus/evidence/r").mkdir(parents=True)
    for name, pred in (("a1", "R70-C1"), ("b1", "R71-C1"), ("b2", "R72-C1")):
        body = f"TASK-UNDER-TEST {name}\nPREDICATE {pred} pass\n"
        if name == break_receipt:
            body = "PROBE ran\n"
        (root / f"corpus/evidence/r/{name}.txt").write_text(body, encoding="utf-8")
    graders = {
        "a2": "subprocess.run(['qemu-system-x86_64', '-m', '128'])\n",
        "b3": "from selenium import webdriver\n",
    }
    for name, body in graders.items():
        if name == kill_detector:
            body = "print('nothing to see')\n"
        d = root / GRADERS / name / "tests"
        d.mkdir(parents=True)
        (d / "test_outputs.py").write_text(body, encoding="utf-8")
    if ledger_extra:
        text = (root / LEDGER).read_text(encoding="utf-8").replace(
            '"members": {', '"members": {\n' + ledger_extra, 1)
        (root / LEDGER).write_text(text, encoding="utf-8")
    if regress_coverage:
        data = json.loads((root / LEDGER).read_text(encoding="utf-8"))
        for name in ("b1", "b2"):
            data["members"][name] = {"status": "unexecuted", "classes": ["beta"],
                                     "reason": "vm-required"}
        (root / LEDGER).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return root


def selftest(work: Path) -> int:
    cases = [
        ("clean", {}, None, 0),
        ("drop-link", {"drop_link": "1"}, "CLASS-ROW-UNLINKED", 1),
        ("drop-member", {"drop_member": "b3"}, "MEMBER-UNACCOUNTED", 1),
        ("ledger-extra", {"ledger_extra": '  "zzz": {"status": "unexecuted", "classes": ["beta"], "reason": "vm-required"},'},
         "MEMBER-EXTRA", 1),
        ("break-receipt", {"break_receipt": "b1"}, "PREDICATE-ABSENT", 1),
        ("bad-reason", {"bad_reason": "b3"}, "REASON-UNKNOWN", 1),
        ("kill-detector", {"kill_detector": "b3"}, "REASON-UNBACKED", 1),
        ("coverage-regression", {"regress_coverage": "1"}, "COVERAGE-REGRESSION", 1),
    ]
    red = 0
    for name, kwargs, expect, want in cases:
        root = build_fixture(work / f"fx-{name}", **kwargs)
        report, defects, _stats = audit(fx_tree(root))
        classes = [d.split()[1] for d in defects]
        ok = (want == 0 and not defects) or (expect in classes)
        if want and ok:
            red += 1
        print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={0 if not defects else 1} want={want} "
              f"defects={len(defects)}" + ("" if ok else f" classes={classes}"))
    fails = 0 if red == len(cases) - 1 else 1
    print(f"SELFTEST cases={len(cases)} red={red} failures={fails}")
    return 0 if fails == 0 else 1


def mutants(work: Path) -> int:
    """Attributed mutant matrix: each mutant names the defect class it must trigger."""
    base = build_fixture(work / "fx-base")
    _r, clean_defects, _ = audit(fx_tree(base))
    matrix = [
        ("drop-link", {"drop_link": "1"}, "CLASS-ROW-UNLINKED"),
        ("drop-member", {"drop_member": "a1"}, "MEMBER-UNACCOUNTED"),
        ("break-receipt", {"break_receipt": "a1"}, "PREDICATE-ABSENT"),
        ("bad-reason", {"bad_reason": "a2"}, "REASON-UNKNOWN"),
        ("kill-detector", {"kill_detector": "a2"}, "REASON-UNBACKED"),
        ("coverage-regression", {"regress_coverage": "1"}, "COVERAGE-REGRESSION"),
    ]
    if clean_defects:
        print(f"MUTANTS base-not-clean defects={len(clean_defects)}")
        return 1
    killed = wrong = survived = 0
    for name, kwargs, expected in matrix:
        root = build_fixture(work / f"mx-{name}", **kwargs)
        _r, defects, _s = audit(fx_tree(root))
        classes = [d.split()[1] for d in defects]
        if expected in classes:
            killed += 1
            print(f"MUTANT {name} killed={expected}")
        elif classes:
            wrong += 1
            print(f"MUTANT {name} wrong-class expected={expected} got={classes}")
        else:
            survived += 1
            print(f"MUTANT {name} SURVIVED expected={expected}")
    print(f"MUTANTS real={len(matrix)} killed={killed} wrong_id={wrong} survived={survived}")
    return 0 if killed == len(matrix) else 1


def control_prose(work: Path) -> int:
    """The skip that must lose: trust the class rows' prose numbers, name nothing, resolve nothing."""
    root = build_fixture(work / "fx-control")
    skill = (root / SKILL).read_text(encoding="utf-8")
    rows = [cells_of(l) for l in skill.splitlines() if l.startswith("| ") and PARTIAL.search(l)]
    named = receipts = reasons = 0
    claimed = 0
    for cells in rows:
        m = PARTIAL.search(cells[2])
        if m:
            claimed += int(m.group(1))
    (root / LEDGER).write_text(json.dumps({"members": {}, "prose_claim": claimed}), encoding="utf-8")
    _r, defects, stats = audit(fx_tree(root))
    target_ok = (not defects and stats["unaccounted"] == 0 and stats["unbacked"] == 0
                 and stats["executed"] > 0)
    print(f"CONTROL prose_rows={len(rows)} prose_claimed_executed={claimed} members_named={named} "
          f"receipts_resolved={receipts} reasons_backed={reasons} defects={len(defects)} "
          f"target_reached={target_ok}")
    return 0 if not target_ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", type=Path, default=Path("."))
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--receipt", type=Path, default=None)
    ap.add_argument("--expect-manifest", default="")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-prose", action="store_true")
    args = ap.parse_args()
    lane = args.lane.resolve()
    work = args.work or Path("/tmp") / "r78-c1"
    work.mkdir(parents=True, exist_ok=True)
    if args.selftest:
        return selftest(work)
    if args.mutants:
        return mutants(work)
    if args.control_prose:
        return control_prose(work)
    if not (lane / SKILL).exists():
        print(f"SETUP lane has no {SKILL}: {lane}")
        return 2
    tree = rev_tree(lane, args.rev)
    dirty = bool(git(lane, "status", "--porcelain", "--untracked-files=normal").stdout.strip())
    return emit(tree, stats_target=True, out=args.receipt, dirty=dirty)


if __name__ == "__main__":
    sys.exit(main())
