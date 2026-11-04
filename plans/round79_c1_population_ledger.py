#!/usr/bin/env python3
"""R79-C1 counter — the whole 16-class Terminal-Bench 2.0 grader population becomes a
machine-checked member ledger: every member accounted exactly once, every executed member's
receipt locating its own subject and carrying execution observations at the measured revision,
every unexecuted member's reason backed by a frozen detector over that task's stored grader bytes
(or the honest default `unattempted`), and all 16 SKILL.md class rows carrying a derived
`executed k of n` plus the ledger pointer.

Frozen before data on 2026-11-04 (L1 KengakuR79); see plans/round-79-claims.md §R79-C1.

    python3 plans/round79_c1_population_ledger.py --lane .                     # verdict, worktree
    python3 plans/round79_c1_population_ledger.py --lane . --rev 660ec0b9      # bytes at a revision
    python3 plans/round79_c1_population_ledger.py --selftest --work DIR        # fixture battery
    python3 plans/round79_c1_population_ledger.py --mutants --work DIR         # attributed mutants
    python3 plans/round79_c1_population_ledger.py --control-namegrep --work DIR
    python3 plans/round79_c1_population_ledger.py --control-default-reason --work DIR
    python3 plans/round79_c1_population_ledger.py --control-all-blocked --work DIR

Why this counter exists: `SKILL.md` §Decision table states class state as prose — thirteen rows say
a bare `executed`, three say `executed k of n` — over the round-62 census population
(`corpus/evidence/round62/class-survey.txt`), and nothing names the members or falsifies a reason.
`plans/grader-population-ledger.json` names every member; this counter is its gate.

Universe (derived, never listed): classes := `CLASS <name> count=<n> members=<csv>` lines of the
census receipt; members := the union of those member lists; pairs := sum of the lists.

Ledger row (one per member, JSON object under `members`):
    executed            {"status","classes","round","receipt","verdict","subject"}
    executed-unlocated  {"status","classes","round","receipt","instrument","debt"}
    unexecuted          {"status","classes","reason","evidence"}

Subject shapes (frozen, receipt bytes; the first that matches is the row's `subject`):
    tb2-header       `^# tb2 <member> grader probe`
    receipt-header   `^# R<n>-C<m> receipt -- TB2 <member> grader offline`
    grader-path      `^GRADER .*corpus/evidence/round52/graders/<member>/tests/`
    task-under-test  `^TASK-UNDER-TEST <member>$`
    capture-tree     `^grader=corpus/evidence/round<n>/tb2-<member>/`

Execution observations (frozen): `^PREDICATE R<n>-C<m> pass` (verdict `predicate`), else any
`^VECTOR ` line (verdict `vectors`), else any `^CASE ` or `^case=` line (verdict `cases`).

Blocker detectors (frozen HERE, not in the ledger) fire over the task's
`corpus/evidence/round52/graders/<member>/tests/test_outputs.py` only:
    browser-required            selenium | webdriver.Chrome/Firefox | chromedriver
    vm-required                 qemu-system | qemu-img | /app/isos/ | win311
    external-db-required        GOLDEN_SQL_PATH | /tests/golden.sql | DB_PATH = Path(
    candidate-library-required  sys.path.append("/app"
A blocker reason whose detector is silent is `REASON-UNBACKED`; an `unattempted` row whose
detector fires is `REASON-UNDERSTATED` — overclaiming is priced in both directions.

Printed lines (every defect fails the predicate):
    UNIVERSE classes=<n> members=<m> pairs=<p> census_executed=<x> census_covered=<c>
    LEDGER rows=<r> executed=<e> unlocated=<u> unexecuted=<x>
    MEMBER <name> <status> classes=<csv> evidence=<path|reason|instrument>
    CLASS <name> k=<k> n=<n> cell=<text|->
    COVERAGE replayed=<r> covered=<c> uncovered=<csv> census_covered=<c>
    DEFECT <CODE> <detail>
    DEFECTS n=<n>
    TARGET classes=<n> members=<m> pairs=<p> replayed=<r> located=<e> unlocated=<u> unexecuted=<x> unaccounted=<n> unbacked=<n> understated=<n> covered=<c>
    PREDICATE R79-C1 pass|fail
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

CENSUS = "corpus/evidence/round62/class-survey.txt"
LEDGER = "plans/grader-population-ledger.json"
GRADERS = "corpus/evidence/round52/graders"
SKILL = "SKILL.md"
TABLE_HEADING = "## Decision table — grader class → offline replay recipe"
LINK = "ledger=" + LEDGER
CELL = re.compile(r"^executed\s+(\d+)\s+of\s+(\d+)(?:\b|$)")
CELLSPLIT = re.compile(r"(?<!\\)\|")
CENSUS_CLASS = re.compile(r"^CLASS (\S+) count=(\d+) members=(.*)$", re.M)
CENSUS_EXEC = re.compile(r"^EXECUTED-COVERAGE executed=(\d+) classified=\d+ classes-covered=(\d+)", re.M)
STATUSES = ("executed", "executed-unlocated", "unexecuted")
BLOCKERS = {
    "browser-required": r"selenium|webdriver\.(?:Chrome|Firefox)|chromedriver",
    "vm-required": r"qemu-system|qemu-img|/app/isos/|win311",
    "external-db-required": r"GOLDEN_SQL_PATH|/tests/golden\.sql|DB_PATH\s*=\s*Path\(",
    "candidate-library-required": r"sys\.path\.append\(\s*[\"']/app",
}
OBS_PRED = re.compile(r"^PREDICATE R\d+-C\d+ pass", re.M)
OBS_VEC = re.compile(r"^VECTOR ", re.M)
OBS_CASE = re.compile(r"^(?:CASE |case=)", re.M)
SUBJECTS = (
    ("tb2-header", r"^# tb2 {m} grader probe"),
    ("receipt-header", r"^# R\d+-C\d+ receipt -- TB2 {m} grader offline"),
    ("grader-path", r"^GRADER .*corpus/evidence/round52/graders/{m}/tests/"),
    ("task-under-test", r"^TASK-UNDER-TEST {m}\s*$"),
    ("capture-tree", r"^grader=corpus/evidence/round\d+/tb2-{m}/"),
)
ROUND_OF = re.compile(r"round(\d+)")
REPLAY_RECEIPT_MAX_MEMBERS = 1  # a replay receipt names its own task, never the population


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Tree:
    """Uniform read interface over the worktree, a git revision, or a fixture directory."""

    def __init__(self, label: str, tip: str, getter, tracked, exists):
        self.label = label
        self.tip = tip
        self._get = getter
        self._tracked = tracked
        self._exists = exists

    def get(self, rel: str) -> str | None:
        return self._get(rel)

    def tracked(self, rel: str) -> bool:
        return self._tracked(rel)

    def exists(self, rel: str) -> bool:
        return self._exists(rel)

    def read(self, rel: str) -> str:
        return self.get(rel) or ""


def _read(path: Path) -> str | None:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return None


def rev_tree(lane: Path, rev: str) -> Tree:
    if rev in ("worktree", "", None):
        tip = git(lane, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip()
        if not tip:
            raise SystemExit("SETUP unresolved branch master")
        return Tree("worktree", tip,
                    lambda rel: _read(lane / rel),
                    lambda rel: git(lane, "ls-files", "--error-unmatch", "--", rel).returncode == 0,
                    lambda rel: (lane / rel).exists())
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    tip = proc.stdout.strip()
    if not tip:
        raise SystemExit(f"SETUP unresolved revision {rev!r}")
    listed = git(lane, "ls-tree", "-r", "--name-only", tip).stdout.splitlines()
    names = set(listed)

    def get(rel: str):
        if rel not in names:
            return None
        return git(lane, "show", f"{tip}:{rel}").stdout

    return Tree(rev, tip, get, lambda rel: rel in names, lambda rel: rel in names)


def fixture_tree(root: Path) -> Tree:
    return Tree("fixture", "fixture",
                lambda rel: _read(root / rel),
                lambda rel: (root / rel).is_file(),
                lambda rel: (root / rel).exists())


# ---------------------------------------------------------------- universe


def parse_census(text: str) -> tuple[dict[str, list[str]], int, int]:
    classes: dict[str, list[str]] = {}
    for name, count, members in CENSUS_CLASS.findall(text):
        members = [x.strip() for x in members.split(",") if x.strip() and x.strip() != "-"]
        classes[name] = members
    ex = CENSUS_EXEC.search(text)
    return classes, int(ex.group(1)) if ex else -1, int(ex.group(2)) if ex else -1


def observations(text: str) -> str | None:
    if OBS_PRED.search(text):
        return "predicate"
    if OBS_VEC.search(text):
        return "vectors"
    if OBS_CASE.search(text):
        return "cases"
    return None


def subject_shape(text: str, member: str) -> str | None:
    for name, pattern in SUBJECTS:
        if re.search(pattern.format(m=re.escape(member)), text, re.M):
            return name
    return None


def distinct_members_named(text: str, members: list[str]) -> int:
    return sum(1 for m in members if re.search(r"(?<![\w.-])" + re.escape(m) + r"(?![\w.-])", text))


# ---------------------------------------------------------------- ledger checks


def check(lane: Tree, ledger_doc: dict, universe: dict[str, list[str]], all_members: list[str],
          census_executed: int, census_covered: int) -> tuple[list[tuple[str, str]], dict]:
    defects: list[tuple[str, str]] = []
    rows = ledger_doc.get("members")
    stats = {"executed": 0, "unlocated": 0, "unexecuted": 0, "unaccounted": 0,
             "unbacked": 0, "understated": 0}
    if not isinstance(rows, dict):
        defects.append(("LEDGER-SHAPE", "members is not an object"))
        rows = {}
    extra = sorted(set(rows) - set(all_members))
    for m in extra:
        defects.append(("MEMBER-EXTRA", m))
    for m in all_members:
        row = rows.get(m)
        if not isinstance(row, dict):
            defects.append(("MEMBER-UNACCOUNTED", m))
            stats["unaccounted"] += 1
            continue
        status = row.get("status")
        if status not in STATUSES:
            defects.append(("STATUS-UNKNOWN", f"{m} {status!r}"))
            continue
        classes = row.get("classes")
        if not isinstance(classes, list) or sorted(classes) != sorted(
                [c for c, ms in universe.items() if m in ms]):
            defects.append(("PAIR-MISMATCH", f"{m} ledger={classes} census={[c for c, ms in universe.items() if m in ms]}"))
        if status == "executed":
            stats["executed"] += 1
            receipt = row.get("receipt")
            if not isinstance(receipt, str) or not lane.tracked(receipt):
                defects.append(("RECEIPT-UNTRACKED", f"{m} {receipt}"))
                continue
            text = lane.read(receipt)
            named = distinct_members_named(text, all_members)
            if named > REPLAY_RECEIPT_MAX_MEMBERS:
                defects.append(("RECEIPT-POPULATION", f"{m} {receipt} names {named} members"))
                continue
            seen = observations(text)
            if seen is None:
                defects.append(("RECEIPT-NO-OBS", f"{m} {receipt}"))
                continue
            if seen != row.get("verdict"):
                defects.append(("VERDICT-MISMATCH", f"{m} ledger={row.get('verdict')} receipt={seen}"))
            shape = subject_shape(text, m)
            if shape is None:
                defects.append(("SUBJECT-ABSENT", f"{m} {receipt}"))
            elif shape != row.get("subject"):
                defects.append(("SUBJECT-MISMATCH", f"{m} ledger={row.get('subject')} receipt={shape}"))
        elif status == "executed-unlocated":
            stats["unlocated"] += 1
            receipt, instrument = row.get("receipt"), row.get("instrument")
            if not isinstance(instrument, str) or not lane.tracked(instrument):
                defects.append(("INSTRUMENT-UNTRACKED", f"{m} {instrument}"))
                continue
            if not isinstance(receipt, str) or not lane.tracked(receipt):
                defects.append(("RECEIPT-UNTRACKED", f"{m} {receipt}"))
                continue
            lines = lane.read(instrument).splitlines()
            line2 = lines[1] if len(lines) > 1 else ""
            named = re.search(r"Offline probe of the pinned Terminal-Bench 2\.0 `([^`]+)` grader \(round (\d+)", line2)
            if not named or named.group(1) != m:
                defects.append(("INSTRUMENT-SUBJECT", f"{m} {instrument} line2 does not name it"))
                continue
            if int(named.group(2)) != row.get("round"):
                defects.append(("ROUND-MISMATCH", f"{m} instrument=r{named.group(2)} ledger=r{row.get('round')}"))
            if not receipt.startswith(f"corpus/evidence/round{row.get('round')}/"):
                defects.append(("UNLOCATED-RECEIPT-OUTSIDE-ROUND", f"{m} {receipt}"))
            if observations(lane.read(receipt)) is None:
                defects.append(("RECEIPT-NO-OBS", f"{m} {receipt}"))
            if subject_shape(lane.read(receipt), m) is not None:
                defects.append(("UNLOCATED-SUBJECT-PRESENT", f"{m} {receipt}"))
            if row.get("debt") != "no-subject-stamp":
                defects.append(("DEBT-UNNAMED", f"{m} {row.get('debt')!r}"))
        else:
            stats["unexecuted"] += 1
            reason = row.get("reason")
            body = lane.read(f"{GRADERS}/{m}/tests/test_outputs.py")
            fired = None
            for code, pattern in BLOCKERS.items():
                hit = re.search(pattern, body)
                if hit:
                    fired = (code, re.sub(r"\s+", " ", body[max(0, hit.start() - 50):hit.end() + 50]).strip())
                    break
            if reason == "unattempted":
                if fired is not None:
                    defects.append(("REASON-UNDERSTATED", f"{m} detector={fired[0]}"))
                    stats["understated"] += 1
                evidence = row.get("evidence")
                if not isinstance(evidence, str) or not evidence.startswith("no-blocker:"):
                    defects.append(("EVIDENCE-SHAPE", f"{m} {evidence!r}"))
                continue
            if reason not in BLOCKERS:
                defects.append(("REASON-UNKNOWN", f"{m} {reason!r}"))
                stats["unbacked"] += 1
                continue
            hit = re.search(BLOCKERS[reason], body)
            if hit is None:
                defects.append(("REASON-UNBACKED", f"{m} {reason}"))
                stats["unbacked"] += 1
                continue
            evidence = row.get("evidence")
            if not isinstance(evidence, str) or re.sub(r"\s+", " ", hit.group(0)) not in evidence:
                defects.append(("EVIDENCE-MISMATCH", f"{m} {reason} {evidence!r}"))
    return defects, stats


# ---------------------------------------------------------------- SKILL rows


def check_skill(lane: Tree, universe: dict[str, list[str]], ledger_doc: dict) -> tuple[list[tuple[str, str]], dict[str, tuple[int, int, str]]]:
    defects: list[tuple[str, str]] = []
    text = lane.read(SKILL)
    start = text.find(TABLE_HEADING)
    if start < 0:
        return [("TABLE-ABSENT", TABLE_HEADING)], {}
    rows: dict[str, tuple[int, int, str]] = {}
    for line in text[start:].splitlines()[1:]:
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in CELLSPLIT.split(line)[1:-1]]
        if len(cells) < 3 or cells[0] in ("class", "") or set(cells[0]) <= set("- "):
            continue
        rows[cells[0]] = (0, 0, cells[2])
    if LINK not in text[start:]:
        defects.append(("LINK-ABSENT", LINK))
    members = ledger_doc.get("members", {})
    for name, ms in universe.items():
        n = len(ms)
        k = sum(1 for m in ms if isinstance(members.get(m), dict)
                and members[m].get("status") in ("executed", "executed-unlocated"))
        got = rows.get(name)
        if got is None:
            defects.append(("CLASS-ROW-ABSENT", name))
            continue
        m = CELL.match(got[2])
        if not m:
            defects.append(("CLASS-ROW-UNQUANTIFIED", f"{name} cell={got[2][:40]!r}"))
            continue
        if (int(m.group(1)), int(m.group(2))) != (k, n):
            defects.append(("CLASS-K-MISMATCH", f"{name} cell={m.group(1)} of {m.group(2)} ledger={k} of {n}"))
        rows[name] = (k, n, got[2])
    return defects, rows


# ---------------------------------------------------------------- modes


def run(lane: Tree, universe: dict[str, list[str]], all_members: list[str],
        census_executed: int, census_covered: int, ledger_doc: dict, verbose: bool = True) -> int:
    pairs = sum(len(v) for v in universe.values())
    print(f"UNIVERSE classes={len(universe)} members={len(all_members)} pairs={pairs} "
          f"census_executed={census_executed} census_covered={census_covered}")
    rows = ledger_doc.get("members", {})
    print(f"LEDGER rows={len(rows)} executed={sum(1 for v in rows.values() if isinstance(v, dict) and v.get('status') == 'executed')} "
          f"unlocated={sum(1 for v in rows.values() if isinstance(v, dict) and v.get('status') == 'executed-unlocated')} "
          f"unexecuted={sum(1 for v in rows.values() if isinstance(v, dict) and v.get('status') == 'unexecuted')}")
    defects, stats = check(lane, ledger_doc, universe, all_members, census_executed, census_covered)
    skill_defects, cells = check_skill(lane, universe, ledger_doc)
    defects += skill_defects
    if verbose:
        for m in all_members:
            row = rows.get(m) if isinstance(rows, dict) else None
            if not isinstance(row, dict):
                continue
            ev = row.get("receipt") or row.get("reason") or "-"
            if row.get("status") == "executed-unlocated":
                ev = f"{row.get('instrument')} -> {row.get('receipt')}"
            elif row.get("status") == "executed":
                ev = f"{row.get('receipt')} [{row.get('subject')}/{row.get('verdict')}]"
            print(f"MEMBER {m} {row.get('status')} classes={','.join(row.get('classes') or [])} evidence={ev}")
        for name, ms in universe.items():
            k, n, cell = cells.get(name, (0, len(ms), "-"))
            print(f"CLASS {name} k={k} n={n} cell={cell[:80]}")
    replayed = {m for m, v in rows.items() if isinstance(v, dict) and v.get("status") in ("executed", "executed-unlocated")}
    covered = [c for c, ms in universe.items() if any(m in replayed for m in ms)]
    uncovered = [c for c, ms in universe.items() if c not in covered]
    print(f"COVERAGE replayed={len(replayed)} covered={len(covered)} "
          f"uncovered={','.join(uncovered) or '-'} census_covered={census_covered}")
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"DEFECTS n={len(defects)}")
    print(f"TARGET classes={len(universe)} members={len(all_members)} pairs={pairs} replayed={len(replayed)} "
          f"located={stats['executed']} unlocated={stats['unlocated']} unexecuted={stats['unexecuted']} "
          f"unaccounted={stats['unaccounted']} unbacked={stats['unbacked']} understated={stats['understated']} "
          f"covered={len(covered)}")
    ok = not defects and stats["unaccounted"] == 0 and stats["unbacked"] == 0 and stats["understated"] == 0
    print(f"PREDICATE R79-C1 {'pass' if ok else 'fail'}")
    return 0 if ok else 1


def load_lane(lane: Path, rev: str) -> tuple[Tree, dict, list[str], int, int]:
    tree = rev_tree(lane, rev)
    census = tree.read(CENSUS)
    if not census:
        raise SystemExit(f"SETUP census absent at {tree.label}")
    universe, census_executed, census_covered = parse_census(census)
    all_members = sorted({m for ms in universe.values() for m in ms})
    doc_text = tree.read(LEDGER)
    doc = json.loads(doc_text) if doc_text else {"members": {}}
    return tree, universe, all_members, census_executed, census_covered, doc


# ---------------------------------------------------------------- fixture battery


FIXTURE_CENSUS = """CLASS-CENSUS roster=4 tree-dirs=4
CLASS alpha count=2 members=m-one,m-two
CLASS beta count=1 members=m-three
CLASS empty count=0 members=-
UNCLASSIFIED count=0 members=-
EXECUTED-COVERAGE executed=1 classified=1 classes-covered=1 classes-uncovered=beta,empty
PREDICATE R62-C1 pass
"""

FIXTURE_SKILL = f"""# fixture skill

{TABLE_HEADING}

| class | count | executed | replay recipe | receipt pointer |
|---|---|---|---|---|
| alpha | 2 | executed 1 of 2 | probe | `x` |
| beta | 1 | executed 1 of 1 | probe | `x` |
| empty | 0 | executed 0 of 0 | probe | `x` |

{LINK}
"""

FIXTURE_RECEIPT = """# tb2 m-one grader probe (kengaku round 90) @ terminal-bench-2 deadbeef
CASE a predicted=pass observed=pass match=yes
CASE b predicted=fail observed=fail match=yes
"""

FIXTURE_INSTRUMENT = '''#!/usr/bin/env python3
"""Offline probe of the pinned Terminal-Bench 2.0 `m-three` grader (round 91, C1).

Usage: --receipt corpus/evidence/round91/probe.txt
"""
'''

FIXTURE_UNLOCATED = """CASE a predicted=pass observed=pass match=yes
"""


def build_fixture(root: Path) -> dict:
    files = {
        CENSUS: FIXTURE_CENSUS,
        SKILL: FIXTURE_SKILL,
        "corpus/evidence/round90/probe.txt": FIXTURE_RECEIPT,
        "corpus/evidence/round91/probe.txt": FIXTURE_UNLOCATED,
        "plans/fixture_probe.py": FIXTURE_INSTRUMENT,
        f"{GRADERS}/m-one/tests/test_outputs.py": "def test_a():\n    assert True\n",
        f"{GRADERS}/m-two/tests/test_outputs.py": "from selenium import webdriver\n\ndef test_a():\n    pass\n",
        f"{GRADERS}/m-three/tests/test_outputs.py": "def test_a():\n    assert True\n",
    }
    base_ledger = {
        "schema": "r79-population-ledger/1",
        "members": {
            "m-one": {"status": "executed", "classes": ["alpha"], "round": 90,
                      "receipt": "corpus/evidence/round90/probe.txt", "verdict": "cases",
                      "subject": "tb2-header"},
            "m-two": {"status": "unexecuted", "classes": ["alpha"], "reason": "browser-required",
                      "evidence": "from selenium import webdriver"},
            "m-three": {"status": "executed-unlocated", "classes": ["beta"], "round": 91,
                        "receipt": "corpus/evidence/round91/probe.txt",
                        "instrument": "plans/fixture_probe.py", "debt": "no-subject-stamp"},
        },
    }
    files[LEDGER] = json.dumps(base_ledger, indent=1) + "\n"
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return {"files": files, "ledger": base_ledger}


CASES = [
    ("clean", "pass"),
    ("member-missing", "MEMBER-UNACCOUNTED"),
    ("member-extra", "MEMBER-EXTRA"),
    ("receipt-untracked", "RECEIPT-UNTRACKED"),
    ("receipt-no-obs", "RECEIPT-NO-OBS"),
    ("subject-absent", "SUBJECT-ABSENT"),
    ("receipt-population", "RECEIPT-POPULATION"),
    ("reason-unbacked", "REASON-UNBACKED"),
    ("reason-understated", "REASON-UNDERSTATED"),
    ("unlocated-subject-present", "UNLOCATED-SUBJECT-PRESENT"),
    ("class-k-mismatch", "CLASS-K-MISMATCH"),
    ("class-row-unquantified", "CLASS-ROW-UNQUANTIFIED"),
    ("pair-mismatch", "PAIR-MISMATCH"),
]


def selftest(work: Path) -> int:
    root = work / "fixture"
    if root.exists():
        shutil.rmtree(root)
    fx = build_fixture(root)
    red = 0
    failures = 0
    for name, expect in CASES:
        if root.exists():
            shutil.rmtree(root)
        fx = build_fixture(root)
        doc = json.loads(json.dumps(fx["ledger"]))
        mem = doc["members"]
        if name == "member-missing":
            del mem["m-three"]
        elif name == "member-extra":
            mem["m-four"] = {"status": "unexecuted", "classes": ["alpha"], "reason": "unattempted",
                             "evidence": "no-blocker: x"}
        elif name == "receipt-untracked":
            mem["m-one"]["receipt"] = "corpus/evidence/round90/absent.txt"
        elif name == "receipt-no-obs":
            (root / "corpus/evidence/round90/probe.txt").write_text("# tb2 m-one grader probe\nnothing\n")
        elif name == "subject-absent":
            (root / "corpus/evidence/round90/probe.txt").write_text("CASE a predicted=pass observed=pass\n")
        elif name == "receipt-population":
            body = FIXTURE_RECEIPT + "".join(f"mentions {m}\n" for m in ("m-one", "m-two", "m-three"))
            (root / "corpus/evidence/round90/probe.txt").write_text(body)
        elif name == "reason-unbacked":
            (root / f"{GRADERS}/m-two/tests/test_outputs.py").write_text("def test_a():\n    pass\n")
        elif name == "reason-understated":
            mem["m-two"]["reason"] = "unattempted"
            mem["m-two"]["evidence"] = "no-blocker: tests/test_outputs.py sha256=0"
        elif name == "unlocated-subject-present":
            (root / "corpus/evidence/round91/probe.txt").write_text(FIXTURE_RECEIPT.replace("m-one", "m-three"))
        elif name == "class-k-mismatch":
            (root / SKILL).write_text(FIXTURE_SKILL.replace("executed 1 of 2", "executed 2 of 2"))
        elif name == "class-row-unquantified":
            (root / SKILL).write_text(FIXTURE_SKILL.replace("executed 1 of 1", "recipe-unexecuted"))
        elif name == "pair-mismatch":
            mem["m-two"]["classes"] = ["beta"]
        (root / LEDGER).write_text(json.dumps(doc, indent=1) + "\n")
        tree = fixture_tree(root)
        universe, census_executed, census_covered = parse_census(tree.read(CENSUS))
        all_members = sorted({m for ms in universe.values() for m in ms})
        defects, _ = check(tree, json.loads(tree.read(LEDGER)), universe, all_members,
                           census_executed, census_covered)
        defects += check_skill(tree, universe, json.loads(tree.read(LEDGER)))[0]
        codes = {c for c, _ in defects}
        if expect == "pass":
            good = not defects
        else:
            good = expect in codes
        red += 0 if good else 1
        if not good:
            failures += 1
        print(f"CASE {name} expect={expect} observed={','.join(sorted(codes)) or '-'} "
              f"{'ok' if good else 'FAIL'}")
    print(f"SELFTEST cases={len(CASES)} red={len(CASES) - 1} failures={failures}")
    if root.exists():
        shutil.rmtree(root)
    return 0 if failures == 0 else 1


# ---------------------------------------------------------------- mutants and controls


def copy_lane_min(lane: Path, dst: Path, doc: dict) -> None:
    """Copy only the bytes the checker reads: census, ledger, SKILL, the 88 grader test files,
    and every receipt/instrument the ledger names."""
    keep = [CENSUS, SKILL, LEDGER]
    for row in doc["members"].values():
        for key in ("receipt", "instrument"):
            if isinstance(row.get(key), str):
                keep.append(row[key])
    for rel in keep:
        src = lane / rel
        if not src.is_file():
            continue
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    for member in doc["members"]:
        src = lane / GRADERS / member / "tests" / "test_outputs.py"
        if src.is_file():
            out = dst / GRADERS / member / "tests" / "test_outputs.py"
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)


MUTANTS = [
    ("flip-executed-to-unattempted", "CLASS-K-MISMATCH"),
    ("swap-blocker-reason", "REASON-UNBACKED"),
    ("drop-a-row", "MEMBER-UNACCOUNTED"),
    ("fake-executed-row", "RECEIPT-POPULATION|SUBJECT-ABSENT|RECEIPT-NO-OBS|RECEIPT-UNTRACKED"),
    ("census-as-receipt", "RECEIPT-POPULATION"),
    ("class-cell-off-by-one", "CLASS-K-MISMATCH"),
]


def mutants(lane: Path, work: Path) -> int:
    doc = json.loads((lane / LEDGER).read_text())
    killed = survived = 0
    for name, expect in MUTANTS:
        root = work / f"mut-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        copy_lane_min(lane, root, doc)
        mut = json.loads(json.dumps(doc))
        mem = mut["members"]
        if name == "flip-executed-to-unattempted":
            first = sorted(m for m, v in mem.items() if v["status"] == "executed")[0]
            mem[first] = {"status": "unexecuted", "classes": mem[first]["classes"],
                          "reason": "unattempted", "evidence": "no-blocker: x"}
        elif name == "swap-blocker-reason":
            first = sorted(m for m, v in mem.items() if v.get("reason") == "browser-required")[0]
            mem[first]["reason"] = "vm-required"
        elif name == "drop-a-row":
            del mem[sorted(mem)[0]]
        elif name == "fake-executed-row":
            cand = sorted(m for m, v in mem.items() if v["status"] == "unexecuted")[0]
            mem[cand] = {"status": "executed", "classes": mem[cand]["classes"], "round": 99,
                         "receipt": "corpus/evidence/round62/class-survey.txt",
                         "verdict": "predicate", "subject": "tb2-header"}
        elif name == "census-as-receipt":
            first = sorted(m for m, v in mem.items() if v["status"] == "executed")[0]
            mem[first]["receipt"] = "corpus/evidence/round62/class-survey.txt"
        elif name == "class-cell-off-by-one":
            skill = (root / SKILL).read_text()
            hit = re.search(r"\| (\w[\w-]*) \| (\d+) \| executed (\d+) of (\d+)", skill)
            if not hit:
                print(f"MUTANT {name} SETUP-NO-CELL")
                survived += 1
                continue
            new = f"| {hit.group(1)} | {hit.group(2)} | executed {int(hit.group(3)) + 1} of {hit.group(4)}"
            (root / SKILL).write_text(skill.replace(hit.group(0), new))
        (root / LEDGER).write_text(json.dumps(mut, indent=1) + "\n")
        tree = fixture_tree(root)
        universe, ce, cc = parse_census(tree.read(CENSUS))
        all_members = sorted({m for ms in universe.values() for m in ms})
        d = json.loads(tree.read(LEDGER))
        defects, _ = check(tree, d, universe, all_members, ce, cc)
        defects += check_skill(tree, universe, d)[0]
        codes = {c for c, _ in defects}
        ok = any(re.search(pat, c) for c in codes for pat in expect.split("|"))
        killed += 1 if ok else 0
        survived += 0 if ok else 1
        print(f"MUTANT {name} expect={expect} observed={','.join(sorted(codes)) or '-'} "
              f"{'killed' if ok else 'SURVIVED'}")
        shutil.rmtree(root)
    print(f"MUTANTS real={len(MUTANTS)} killed={killed} survived={survived}")
    return 0 if survived == 0 else 1


def control(lane: Path, work: Path, kind: str) -> int:
    doc = json.loads((lane / LEDGER).read_text())
    root = work / f"ctl-{kind}"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    copy_lane_min(lane, root, doc)
    mut = json.loads(json.dumps(doc))
    mem = mut["members"]
    universe, ce, cc = parse_census((root / CENSUS).read_text())
    all_members = sorted({m for ms in universe.values() for m in ms})
    if kind == "namegrep":
        # The cheapest skip: call a member executed when ANY verdict-bearing receipt mentions it.
        receipts = [p for p in (root / "corpus/evidence").rglob("*.txt")]
        texts = {p: p.read_text(errors="replace") for p in receipts}
        rows = {}
        for m in all_members:
            row = {"status": "unexecuted", "classes": [c for c, ms in universe.items() if m in ms],
                   "reason": "unattempted", "evidence": "no-blocker: name-grep control"}
            for p, t in texts.items():
                if observations(t) and re.search(r"(?<![\w.-])" + re.escape(m) + r"(?![\w.-])", t):
                    rel = str(p.relative_to(root))
                    row = {"status": "executed", "classes": row["classes"], "round": 62,
                           "receipt": rel, "verdict": observations(t), "subject": "tb2-header"}
                    break
            rows[m] = row
        mut["members"] = rows
    elif kind == "default-reason":
        for m, row in mem.items():
            if row["status"] == "unexecuted":
                row["reason"] = "unattempted"
                row["evidence"] = "no-blocker: default-reason control"
    elif kind == "all-blocked":
        for m, row in mem.items():
            if row["status"] == "unexecuted":
                row["reason"] = "browser-required"
                row["evidence"] = "selenium"
    else:
        raise SystemExit(f"SETUP unknown control {kind}")
    (root / LEDGER).write_text(json.dumps(mut, indent=1) + "\n")
    tree = fixture_tree(root)
    defects, stats = check(tree, json.loads(tree.read(LEDGER)), universe, all_members, ce, cc)
    defects += check_skill(tree, universe, json.loads(tree.read(LEDGER)))[0]
    codes = sorted({c for c, _ in defects})
    rows = json.loads(tree.read(LEDGER))["members"]
    execd = sum(1 for v in rows.values() if v["status"] == "executed")
    print(f"CONTROL {kind} executed={execd} unexecuted={sum(1 for v in rows.values() if v['status'] == 'unexecuted')} "
          f"defects={len(defects)} codes={','.join(codes) or '-'}")
    reached = not defects
    print(f"CONTROL {kind} target_reached={reached}")
    shutil.rmtree(root)
    return 0 if not reached else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--control-namegrep", action="store_true")
    ap.add_argument("--control-default-reason", action="store_true")
    ap.add_argument("--control-all-blocked", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    lane = Path(a.lane).resolve()
    work = Path(a.work).resolve() if a.work else Path("/fast/scratch/hyaku/kengaku-r79/counter")
    work.mkdir(parents=True, exist_ok=True)
    if a.selftest:
        return selftest(work)
    if a.mutants:
        return mutants(lane, work)
    if a.control_namegrep:
        return control(lane, work, "namegrep")
    if a.control_default_reason:
        return control(lane, work, "default-reason")
    if a.control_all_blocked:
        return control(lane, work, "all-blocked")
    tree, universe, all_members, ce, cc, doc = load_lane(lane, a.rev)
    return run(tree, universe, all_members, ce, cc, doc, verbose=not a.quiet)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
