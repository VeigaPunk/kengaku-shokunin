#!/usr/bin/env python3
"""R85-C1 counter — first offline replay of the captured `sqlite-db-truncate` grader.

Grades one frozen member at a measured revision: the receipt named by the round-85 claims
must exist, carry the full stamp, reproduce the frozen eight-case two-leg table with zero
mismatches, and the population ledger must mark it executed in round 85.  Beyond the receipt,
the counter re-runs the pinned probe from the measured tree and requires its observation block
to equal the receipt's block (REPRODUCE, unconditional — a hand-minted receipt is not evidence).

Frozen inputs live at FREEZE_REV (the claims commit), never at the measured revision: when the
freeze tree lacks the case table or the defect list the counter exits 2 (SETUP) instead of
scoring, so a table committed after the freeze cannot silently make the anchor inert.

Exit: 0 target reached, 1 a named defect, 2 could-not-evaluate.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_REV = "0de45354d7aff18e4a23a348ec13de3a1f707a44"   # round-84 closure tip
FREEZE_REV = "1a45aeb5e8706b1518ba58fd0fe882df1631e2a0"  # round-85 claims commit
MEMBER = "sqlite-db-truncate"
LEDGER = "plans/grader-population-ledger.json"
TABLE = "plans/round85-cases.json"
DEFECTS = "plans/round85-defects.json"
TOOL = "plans/round85_sqlite_truncate_probe.py"
TRUSTED_TOOL_SHA = "04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538"
CAPTURE = "corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py"
RECEIPT = "corpus/evidence/round85/sqlite-db-truncate-probe.txt"
LEDGER_ROUND = 85
LEDGER_SUBJECT = "tb2-header"
HEADER = "# tb2 sqlite-db-truncate grader probe"
SUBJECT_SHA = "8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881"
SUBJECT_PREFIX = SUBJECT_SHA[:16]
FROZEN = (("exact8", "8/P"), ("seven", "7/P"), ("six", "6/F"), ("empty", "0/F"),
          ("extras", "8/P"), ("duplicates", "8/P"), ("string-values", "0/F"),
          ("int-values", "6/F"))
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL",
            "TOOL_SHA", "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE",
            "COMMAND", "EXIT")
CASE_RE = re.compile(r"^CASE (\S+) predicted=(\d+)/([PF]) observed=(\d+)/([PF])$")
SUMMARY_RE = re.compile(r"^cases=(\d+) legs=(\d+) mismatches=(\d+)$")
PRED_RE = re.compile(r"^PREDICATE R85-PROBE (pass|fail)$")
STAMP_RE = re.compile(r"^([A-Z_]+) (.+)$")
BEGIN, END = "OBSERVATIONS_BEGIN", "OBSERVATIONS_END"


class SetupDefect(Exception):
    """The frozen replay could not be evaluated (exit 2, never a fail)."""


def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True)


def sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


class Tree:
    """A measured tree: a git revision extracted to disk, or a fixture directory."""

    def __init__(self, root: Path, tip: str, source: str):
        self.root = root
        self.tip = tip
        self.source = source

    def has(self, rel: str) -> bool:
        return (self.root / rel).is_file()

    def bytes(self, rel: str) -> bytes | None:
        try:
            return (self.root / rel).read_bytes()
        except OSError:
            return None


ARCHIVE_PATHS = ("plans", "corpus/evidence/round52/graders/sqlite-db-truncate",
                 "corpus/evidence/round85", "SKILL.md")


def extract_paths(lane: Path, tip: str, root: Path, paths: tuple[str, ...]) -> int:
    """Extract the paths that exist at `tip`; absent paths are skipped, never fatal."""
    extracted = 0
    for rel in paths:
        if git(lane, "cat-file", "-e", f"{tip}:{rel}").returncode != 0:
            continue
        arc = subprocess.run(["git", "-C", str(lane), "archive", "--format=tar", tip, rel],
                             capture_output=True)
        if arc.returncode != 0:
            continue
        subprocess.run(["tar", "-x", "-C", str(root)], input=arc.stdout, capture_output=True)
        extracted += 1
    return extracted


def rev_tree(lane: Path, rev: str, work: Path) -> Tree:
    proc = git(lane, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    tip = proc.stdout.decode().strip()
    if proc.returncode != 0 or not tip:
        raise SetupDefect(f"unresolved-revision {rev}")
    root = Path(tempfile.mkdtemp(prefix="tree-", dir=work))
    if not extract_paths(lane, tip, root, ARCHIVE_PATHS):
        raise SetupDefect(f"archive-failed {tip[:12]}")
    return Tree(root, tip, f"rev {tip[:12]}")


def fixture_tree(root: Path) -> Tree:
    return Tree(root, "fixture", "fixture")


def parse_receipt(text: str) -> tuple[dict, list[str], str]:
    lines = text.splitlines()
    try:
        begin, end = lines.index(BEGIN), lines.index(END)
    except ValueError:
        return {}, [], "no observation block"
    if end < begin:
        return {}, [], "block out of order"
    stamp: dict[str, str] = {}
    for line in lines[:begin]:
        if line == HEADER:          # the frozen subject line, exactly (population-gate shape)
            continue
        match = STAMP_RE.match(line)
        if not match:
            return {}, [], f"unstamped line {line[:40]!r}"
        stamp[match.group(1)] = match.group(2)
    return stamp, [ln.rstrip() for ln in lines[begin + 1:end]], ""


def parse_cases(block: list[str]) -> tuple[list[tuple[str, str, str]], int, int, int, str]:
    cases: list[tuple[str, str, str]] = []
    summary = (0, 0, 0)
    predicate = ""
    for line in block:
        match = CASE_RE.match(line)
        if match:
            cases.append((match.group(1), f"{match.group(2)}/{match.group(3)}",
                          f"{match.group(4)}/{match.group(5)}"))
            continue
        match = SUMMARY_RE.match(line)
        if match:
            summary = tuple(int(x) for x in match.groups())
            continue
        match = PRED_RE.match(line)
        if match:
            predicate = match.group(1)
            continue
        return cases, *summary, f"unexpected observation line {line[:60]!r}"
    return cases, *summary, predicate


def check(tree: Tree, work: Path, reproduce: bool = True) -> tuple[list[tuple[str, str]], dict]:
    defects: list[tuple[str, str]] = []
    stats = {"members": 1, "cases": 0, "legs": 0, "mismatches": 0,
             "located": 0, "executed": 0}

    table_bytes = tree.bytes(TABLE)
    if table_bytes is None:
        defects.append(("TABLE-MISSING", f"{TABLE}@" + tree.source))
    else:
        try:
            doc = json.loads(table_bytes)
        except json.JSONDecodeError:
            defects.append(("TABLE-MALFORMED", "not JSON"))
            doc = {}
        if doc.get("member") != MEMBER:
            defects.append(("TABLE-MEMBER", f"{doc.get('member')!r}"))
        frozen = tuple((c.get("id"), f"{c.get('predicted_score')}/{c.get('predicted_verdict')}")
                       for c in doc.get("cases") or [] if isinstance(c, dict))
        if frozen != FROZEN:
            defects.append(("TABLE-VECTORS", "frozen case table differs"))
        if doc.get("subject_sha") != SUBJECT_SHA:
            defects.append(("TABLE-SUBJECT", str(doc.get("subject_sha"))[:16]))

    capture = tree.bytes(CAPTURE)
    if capture is None:
        defects.append(("SUBJECT-MISSING", CAPTURE))
    elif sha256(capture) != SUBJECT_SHA:
        defects.append(("SUBJECT-SHA", sha256(capture)[:16]))

    tool = tree.bytes(TOOL)
    if tool is None:
        defects.append(("TOOL-MISSING", TOOL))
    elif sha256(tool) != TRUSTED_TOOL_SHA:
        defects.append(("TOOL-SHA", sha256(tool)[:16]))

    ledger_bytes = tree.bytes(LEDGER)
    if ledger_bytes is None:
        defects.append(("LEDGER-MISSING", LEDGER))
    else:
        try:
            row = json.loads(ledger_bytes)["members"][MEMBER]
        except (json.JSONDecodeError, KeyError):
            defects.append(("LEDGER-ROW", MEMBER))
            row = None
        if row is not None:
            if row.get("status") != "executed":
                defects.append(("LEDGER-UNEXECUTED", f"status={row.get('status')}"))
            else:
                stats["executed"] = 1
            if row.get("round") != LEDGER_ROUND:
                defects.append(("LEDGER-ROUND", str(row.get("round"))))
            if row.get("receipt") != RECEIPT:
                defects.append(("LEDGER-RECEIPT", str(row.get("receipt"))))
            if row.get("subject") != LEDGER_SUBJECT:
                defects.append(("LEDGER-SUBJECT", str(row.get("subject"))))
            if row.get("verdict") != "cases":
                defects.append(("LEDGER-VERDICT", str(row.get("verdict"))))

    receipt_bytes = tree.bytes(RECEIPT)
    block: list[str] = []
    if receipt_bytes is None:
        defects.append(("RECEIPT-MISSING", RECEIPT))
    else:
        stats["located"] = 1
        stamp, block, problem = parse_receipt(receipt_bytes.decode("utf-8", "replace"))
        if problem:
            defects.append(("RECEIPT-SHAPE", problem))
        missing = [field for field in REQUIRED if field not in stamp]
        if missing:
            defects.append(("RECEIPT-FIELD", ",".join(missing)))
        if stamp.get("MEMBER") != MEMBER:
            defects.append(("RECEIPT-MEMBER", str(stamp.get("MEMBER"))))
        if stamp.get("SUBJECT_CAPTURE") != CAPTURE:
            defects.append(("RECEIPT-SUBJECT-PATH", str(stamp.get("SUBJECT_CAPTURE"))))
        if capture is None or stamp.get("SUBJECT_SHA") != sha256(capture):
            defects.append(("RECEIPT-SUBJECT-SHA", str(stamp.get("SUBJECT_SHA"))[:16]))
        if table_bytes is not None and stamp.get("CASE_TABLE_SHA") != sha256(table_bytes):
            defects.append(("RECEIPT-TABLE-SHA", str(stamp.get("CASE_TABLE_SHA"))[:16]))
        if stamp.get("TOOL") != TOOL:
            defects.append(("RECEIPT-TOOL", str(stamp.get("TOOL"))))
        if stamp.get("TOOL_SHA") != TRUSTED_TOOL_SHA:
            defects.append(("RECEIPT-TOOL-SHA", str(stamp.get("TOOL_SHA"))[:16]))
        if stamp.get("EXIT") != "0":
            defects.append(("RECEIPT-EXIT", str(stamp.get("EXIT"))))
        if stamp.get("WORKTREE") != "clean":
            defects.append(("RECEIPT-WORKTREE", str(stamp.get("WORKTREE"))))
        tokens = stamp.get("COMMAND", "").split()
        if (len(tokens) < 6 or not tokens[0].startswith("python3")
                or not tokens[1].endswith("round85_sqlite_truncate_probe.py")
                or tokens[2:4] != ["--lane", "."] or tokens[4] != "--work"
                or tokens[5] == ""):
            defects.append(("RECEIPT-COMMAND", " ".join(tokens)[:80]))

        cases, ncases, nlegs, nmis, predicate = parse_cases(block)
        stats.update(cases=ncases, legs=nlegs, mismatches=nmis)
        if [c[0] for c in cases] != [c[0] for c in FROZEN]:
            defects.append(("CASE-ORDER", ",".join(c[0] for c in cases)[:80]))
        for case_id, predicted, observed in cases:
            if observed != predicted:
                # VECTOR-MISMATCH: the receipt's observed leg is not its predicted leg
                defects.append(("VECTOR-MISMATCH", f"{case_id} {predicted}!={observed}"))
        if predicate != "pass":
            defects.append(("PREDICATE-LINE", predicate or "absent"))
        if (ncases, nlegs, nmis) != (8, 16, 0):
            defects.append(("SUMMARY", f"cases={ncases} legs={nlegs} mismatches={nmis}"))

        if reproduce and tool is not None and (tree.root / TOOL).is_file():
            out = Path(tempfile.mkdtemp(prefix="repro-", dir=work))
            proc = subprocess.run([sys.executable, "-I", "-B", str(tree.root / TOOL),
                                   "--lane", str(tree.root), "--work", str(out)],
                                  capture_output=True, text=True, timeout=900,
                                  env={"PATH": "/usr/bin", "TMPDIR": str(work)})
            fresh_stamp, fresh_block, problem = parse_receipt(proc.stdout)
            if proc.returncode != 0 or problem or fresh_block != block:
                defects.append(("REPRODUCE-MISMATCH",
                                f"rc={proc.returncode} {problem or 'block differs'}"))
            shutil.rmtree(out, ignore_errors=True)
        elif reproduce:
            defects.append(("REPRODUCE-MISSING", "no tool to re-run"))

    return defects, stats


def result_code(defects: list, stats: dict) -> int:
    ok = (not defects and stats["members"] == 1 and stats["cases"] == 8
          and stats["legs"] == 16 and stats["mismatches"] == 0
          and stats["located"] == 1 and stats["executed"] == 1)
    return 0 if ok else 1


def emit(defects: list, stats: dict, quiet: bool = False) -> int:
    for code, detail in defects:
        print(f"DEFECT {code} {detail}")
    print(f"TARGET members={stats['members']} cases={stats['cases']} legs={stats['legs']} "
          f"mismatches={stats['mismatches']} located={stats['located']} "
          f"executed={stats['executed']} defects={len(defects)}")
    code = result_code(defects, stats)
    print(f"PREDICATE R85-C1 {'pass' if code == 0 else 'fail'}")
    return code


def setup_failure(detail: str) -> int:
    print(f"DEFECT SETUP {detail}")
    print("TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=0")
    print("PREDICATE R85-C1 fail")
    return 2


def ensure_freeze(lane: Path) -> None:
    """Frozen inputs are read at FREEZE_REV; absent there means could-not-evaluate."""
    is_git = git(lane, "rev-parse", "--git-dir").returncode == 0
    for rel in (TABLE, DEFECTS):
        if is_git:
            if git(lane, "cat-file", "-e", f"{FREEZE_REV}:{rel}").returncode != 0:
                raise SetupDefect(f"frozen-input-missing {rel}@{FREEZE_REV[:12]}")
        elif not (lane / rel).is_file():
            raise SetupDefect(f"frozen-input-missing {rel} (no git at {lane})")


def run(tree: Tree, work: Path, quiet: bool = False) -> int:
    defects, stats = check(tree, work)
    return emit(defects, stats, quiet)


# ---------------------------------------------------------------- fixtures

def copy_tree(source: Tree, work: Path, name: str) -> Path:
    root = Path(tempfile.mkdtemp(prefix=f"{name}-", dir=work))
    for rel in ARCHIVE_PATHS:
        src = source.root / rel
        dst = root / rel
        if src.is_dir():
            shutil.copytree(src, dst)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return root


def flip_ledger(root: Path, status: str = "executed") -> None:
    path = root / LEDGER
    doc = json.loads(path.read_bytes())
    row = doc["members"][MEMBER]
    row.update(status=status, round=LEDGER_ROUND, receipt=RECEIPT,
               subject=LEDGER_SUBJECT, verdict="predicate")
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def forge_receipt(root: Path, work: Path) -> None:
    """Mint a claims-only receipt: the plausible source-read error on the `six` case."""
    text = (root / RECEIPT).read_text(encoding="utf-8")
    text = text.replace("CASE six predicted=6/F observed=6/F",
                        "CASE six predicted=6/P observed=6/P")
    (root / RECEIPT).write_text(text, encoding="utf-8")


CONTROLS = {
    "do-nothing": "base",
    "ledger-only": "ledger-only",
    "fabricated-observations": "fabricated",
    "forged-receipt": "forged",
}


def control(lane: Path, work: Path, name: str) -> int:
    kind = CONTROLS[name]
    if kind == "base":
        tree = rev_tree(lane, BASE_REV, work)
    else:
        tip_tree = rev_tree(lane, "master", work)
        root = copy_tree(tip_tree, work, kind)
        tree = fixture_tree(root)
        if kind == "ledger-only":
            (root / RECEIPT).unlink()
            flip_ledger(root)
        elif kind == "ledger-bad":
            flip_ledger(root, status="unexecuted")
        elif kind == "fabricated":
            (root / RECEIPT).write_text(
                (root / RECEIPT).read_text(encoding="utf-8").replace(
                    "CASE extras predicted=8/P observed=8/P",
                    "CASE extras predicted=8/P observed=7/P"), encoding="utf-8")
        elif kind == "forged":
            forge_receipt(root, work)
        elif kind == "exit-one":
            (root / RECEIPT).write_text(
                (root / RECEIPT).read_text(encoding="utf-8").replace("EXIT 0", "EXIT 1"),
                encoding="utf-8")
    defects, stats = check(tree, work)
    code = result_code(defects, stats)
    reached = code == 0
    print(f"CONTROL {name} target_reached={reached} defects={len(defects)} "
          f"codes={','.join(sorted({c for c, _ in defects})) or 'none'}")
    return 0 if not reached else 1


MUTANTS = (
    # (name, fixture, [(needle, replacement), ...], expected defect the fixture must raise unmutated)
    ("no-reproduce", "forged",
     [("if proc.returncode != 0 or problem or fresh_block != block:", "if False:")],
     "REPRODUCE-MISMATCH"),
    ("no-vector-no-reproduce", "fabricated",
     [("if observed != predicted:", "if False:"),
      ("if proc.returncode != 0 or problem or fresh_block != block:", "if False:")],
     "VECTOR-MISMATCH"),
    ("no-ledger", "ledger-bad",
     [('if row.get("status") != "executed":', "if False:")], "LEDGER-UNEXECUTED"),
    ("no-tool-sha", "tool",
     [("elif sha256(tool) != TRUSTED_TOOL_SHA:", "elif False:")], "TOOL-SHA"),
    ("no-exit", "exit-one",
     [('if stamp.get("EXIT") != "0":', "if False:")], "RECEIPT-EXIT"),
    # Dropped deliberately: a receipt-TABLE_SHA mutant cannot reach the target on a drifted
    # table because the probe pins the same table itself (FROZEN_TABLE_SHA) and exits 2.
    # The receipt's table binding is therefore redundant defence, reported as such.
)


def mutant_fixture(lane: Path, work: Path, kind: str) -> Path:
    tip_tree = rev_tree(lane, "master", work)
    root = copy_tree(tip_tree, work, f"mut-{kind}")
    if kind == "tool":
        # bytes drift with identical output: only the TOOL-SHA leg can see it
        path = root / TOOL
        path.write_bytes(path.read_bytes() + b"\n# drifted copy\n")
    elif kind == "table":
        # a non-vector field drifts: only the receipt's TABLE_SHA binding can see it
        path = root / TABLE
        doc = json.loads(path.read_bytes())
        doc["cases"][0]["why"] = "drifted"
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    elif kind == "exit-one":
        path = root / RECEIPT
        path.write_text(path.read_text(encoding="utf-8").replace("EXIT 0", "EXIT 1"),
                        encoding="utf-8")
    elif kind == "ledger-bad":
        flip_ledger(root, status="unexecuted")
    elif kind == "fabricated":
        path = root / RECEIPT
        path.write_text(path.read_text(encoding="utf-8").replace(
            "CASE extras predicted=8/P observed=8/P",
            "CASE extras predicted=8/P observed=7/P"), encoding="utf-8")
    elif kind == "forged":
        forge_receipt(root, work)
    return root


def mutants(lane: Path, work: Path) -> int:
    """Each removed check must be load-bearing: dropping it lets the fixture through.

    A mutant is `necessary` when the mutated counter reaches the target on the fixture its
    removed check governs, while the unmutated counter rejects that fixture with the named
    defect.  A mutant that cannot reach the target has been caught by another leg (defence in
    depth) and is reported as `redundant`, not as a pass.
    """
    necessary = redundant = 0
    source = Path(__file__).resolve().read_text(encoding="utf-8")
    base = Path(__file__).resolve()
    for name, fixture, edits, expected in MUTANTS:
        if any(needle not in source for needle, _ in edits):
            print(f"MUTANT {name} NOT-APPLICABLE")
            redundant += 1
            continue
        root = mutant_fixture(lane, work, fixture)
        mutated = work / f"mutant-{name}.py"
        text = source
        for needle, replacement in edits:
            text = text.replace(needle, replacement, 1)
        mutated.write_text(text, encoding="utf-8")
        plain = subprocess.run([sys.executable, "-I", "-B", str(base), "--lane", str(root),
                                "--work", str(work / f"pw-{name}")],
                               capture_output=True, text=True, timeout=900,
                               env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        mutant = subprocess.run([sys.executable, "-I", "-B", str(mutated), "--lane", str(root),
                                 "--work", str(work / f"mw-{name}")],
                                capture_output=True, text=True, timeout=900,
                                env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        ok_plain = plain.returncode == 1 and expected in plain.stdout
        ok_mutant = "PREDICATE R85-C1 pass" in mutant.stdout
        print(f"MUTANT {name} fixture={fixture} unmutated_defect={ok_plain} "
              f"mutant_reaches_target={ok_mutant}")
        if ok_plain and ok_mutant:
            necessary += 1
        else:
            redundant += 1
        shutil.rmtree(root, ignore_errors=True)
    print(f"MUTANTS real={len(MUTANTS)} necessary={necessary} redundant={redundant}")
    return 0 if necessary == len(MUTANTS) else 1


def selftest(lane: Path, work: Path) -> int:
    failures = 0
    checks = 0

    def check_case(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    tip = rev_tree(lane, "master", work)
    defects, stats = check(tip, work, reproduce=False)
    check_case("tip-table-parses", not any(code.startswith("TABLE") for code, _ in defects))
    check_case("tip-vectors-frozen", not any(code.startswith("CASE-ORDER") for code, _ in defects))
    check_case("receipt-shape", not any(code.startswith("RECEIPT-SHAPE") for code, _ in defects))

    root = copy_tree(tip, work, "sel-test")
    (root / RECEIPT).unlink()
    defects, stats = check(fixture_tree(root), work, reproduce=False)
    check_case("absent-receipt-red", any(code == "RECEIPT-MISSING" for code, _ in defects)
               and result_code(defects, stats) == 1)

    root = copy_tree(tip, work, "sel-ledger")
    (root / RECEIPT).unlink()
    flip_ledger(root)
    defects, stats = check(fixture_tree(root), work, reproduce=False)
    check_case("ledger-only-red", any(code == "RECEIPT-MISSING" for code, _ in defects))

    root = copy_tree(tip, work, "sel-vector")
    (root / RECEIPT).write_text(
        (root / RECEIPT).read_text(encoding="utf-8").replace("7/P", "8/P", 1), encoding="utf-8")
    defects, stats = check(fixture_tree(root), work, reproduce=False)
    check_case("vector-mismatch-red", any(code == "VECTOR-MISMATCH" for code, _ in defects))

    root = copy_tree(tip, work, "sel-tool")
    path = root / TOOL
    path.write_bytes(path.read_bytes() + b"\n")
    defects, stats = check(fixture_tree(root), work, reproduce=False)
    check_case("tool-sha-red", any(code == "TOOL-SHA" for code, _ in defects))

    root = copy_tree(tip, work, "sel-exit")
    (root / RECEIPT).write_text(
        (root / RECEIPT).read_text(encoding="utf-8").replace("EXIT 0", "EXIT 3"), encoding="utf-8")
    defects, stats = check(fixture_tree(root), work, reproduce=False)
    check_case("receipt-exit-red", any(code == "RECEIPT-EXIT" for code, _ in defects))

    # Freeze anchor: the frozen inputs must exist at FREEZE_REV; a fixture tree without
    # the table fails closed at exit 2 rather than scoring zero.
    try:
        freeze = rev_tree(lane, FREEZE_REV, work)
    except SetupDefect:
        check_case("freeze-anchor-present", False)
    else:
        check_case("freeze-anchor-present",
                   freeze.has(TABLE) and freeze.has(DEFECTS))
        root = copy_tree(freeze, work, "sel-freeze")
        (root / TABLE).unlink()
        proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                               "--lane", str(root), "--work", str(work / "sel-freeze-w")],
                              capture_output=True, text=True, timeout=600,
                              env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        check_case("freeze-anchor-fails-closed", proc.returncode == 2
                   and "DEFECT SETUP" in proc.stdout
                   and "PREDICATE R85-C1 fail" in proc.stdout)

    print(f"SELFTEST cases={checks} red={checks - failures} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--work", required=True)
    parser.add_argument("--quiet", action="store_true")
    for flag in ("--selftest", "--mutants", "--control-do-nothing", "--control-ledger-only",
                 "--control-fabricated-observations", "--control-forged-receipt"):
        parser.add_argument(flag, action="store_true")
    args = parser.parse_args(argv)
    lane = Path(args.lane).resolve()
    work = Path(args.work).resolve()
    if not work.exists():
        work.mkdir(parents=True, exist_ok=True)
    if not work.is_dir():
        return setup_failure(f"work-not-a-directory {work}")
    try:
        if args.selftest:
            return selftest(lane, work)
        ensure_freeze(lane)
        if args.mutants:
            return mutants(lane, work)
        for flag, name in (("control_do_nothing", "do-nothing"),
                           ("control_ledger_only", "ledger-only"),
                           ("control_fabricated_observations", "fabricated-observations"),
                           ("control_forged_receipt", "forged-receipt")):
            if getattr(args, flag):
                return control(lane, work, name)
        if args.rev:
            return run(rev_tree(lane, args.rev, work), work, args.quiet)
        tree = fixture_tree(lane)
        defects, stats = check(tree, work)
        return emit(defects, stats, args.quiet)
    except SetupDefect as error:
        return setup_failure(str(error))
    except subprocess.TimeoutExpired as error:
        return setup_failure(f"timeout {error}")


if __name__ == "__main__":
    sys.exit(main())
