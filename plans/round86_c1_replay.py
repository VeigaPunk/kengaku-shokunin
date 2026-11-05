#!/usr/bin/env python3
"""R86-C1 counter — located offline replay of the captured `raman-fitting` grader.

Grades one frozen member at a measured revision.  Eight named legs, one verdict each; the
counter prints one `DEFECT <leg> <detail>` line per failed leg and nothing else:

  L1-receipt    the receipt named by the ledger row exists at the measured revision
  L2-stamp      its stamp carries every required field, and MEMBER/SUBJECT_CAPTURE/
                SUBJECT_SHA/CASE_TABLE_SHA/TOOL/TOOL_SHA agree with the measured bytes
  L3-tip        its LANE_TIP is a resolvable commit in this repo that is an ancestor of
                the measured revision (a receipt minted elsewhere names no such commit)
  L4-table      the case table at the measured revision is byte-identical to the frozen
                table at FREEZE_REV (read from FREEZE_REV, never from the measured tree)
  L5-vectors    the receipt's eight CASE lines carry the frozen predicted vectors with
                observed == predicted and a zero-mismatch summary
  L6-reproduce  re-running the pinned probe from the measured tree reproduces the
                receipt's observation block exactly
  L7-ledger     the population ledger marks the member executed in round 86 with this
                receipt, subject and verdict vocabulary
  L8-subject    the captured grader bytes hash to the frozen SUBJECT_SHA

The honest limit, stated so it is not overclaimed: a receipt whose observed vectors are
correct AND whose stamp names the measured tip and the true digests is not distinguishable
from a freshly minted one by observation alone — L6 reproduces the observation, it does not
authenticate an author.  L3/L2 are what a copy minted elsewhere cannot satisfy.

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

BASE_REV = "88651a72ef112ed9f5361e1c8c197babec691f96"   # round-85 closure tip
FREEZE_REV = "__FREEZE_REV__"                            # round-86 claims commit
MEMBER = "raman-fitting"
LEDGER = "plans/grader-population-ledger.json"
TABLE = "plans/round86-cases.json"
TOOL = "plans/round86_raman_probe.py"
TRUSTED_TOOL_SHA = "09731b3ebcf4448546184b39d21d9a28016693af935a20f7efddec5cff209cde"
CAPTURE = "corpus/evidence/round52/graders/raman-fitting/tests/test_outputs.py"
RECEIPT = "corpus/evidence/round86/raman-fitting-probe.txt"
LEDGER_ROUND = 86
LEDGER_SUBJECT = "tb2-header"
HEADER = "# tb2 raman-fitting grader probe"
SUBJECT_SHA = "171fae772ccf262aec8ddac5bd2c6c731eed842421f5d8439a330b158c9f8c13"
FROZEN = (("exact", "P/P/P"), ("missing-2D-key", "P/P/E"), ("g-amplitude-string", "P/E/P"),
          ("extra-schema-keys", "P/P/P"), ("absent-file", "F/F/F"),
          ("g-key-renamed", "P/E/P"), ("2D-null-value", "P/P/E"),
          ("g-amplitude-just-outside", "P/F/P"))
REQUIRED = ("MEMBER", "SUBJECT_CAPTURE", "SUBJECT_SHA", "CASE_TABLE_SHA", "TOOL",
            "TOOL_SHA", "HOST_PYTHON", "HOST_OPENSSL", "LANE_TIP", "WORKTREE",
            "COMMAND", "EXIT")
CASE_RE = re.compile(r"^CASE (\S+) predicted=(\S+) observed=(\S+)$")
SUMMARY_RE = re.compile(r"^cases=(\d+) legs=(\d+) mismatches=(\d+)$")
PRED_RE = re.compile(r"^PREDICATE R86-PROBE (pass|fail)$")
STAMP_RE = re.compile(r"^([A-Z_]+) (.+)$")
BEGIN, END = "OBSERVATIONS_BEGIN", "OBSERVATIONS_END"
LEGS = ("L1-receipt", "L2-stamp", "L3-tip", "L4-table", "L5-vectors",
        "L6-reproduce", "L7-ledger", "L8-subject")


_FREEZE: str | None = None
_REPO: Path | None = None


def freeze_args() -> list[str]:
    return ["--freeze", _FREEZE] if _FREEZE else []


def repo() -> Path:
    """The git repository the frozen inputs and the tip ancestry are read from."""
    return _REPO if _REPO is not None else Path(".").resolve()


def freeze_rev() -> str:
    """The revision the frozen inputs are read at (--freeze overrides for pre-freeze runs)."""
    return _FREEZE or FREEZE_REV


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


ARCHIVE_PATHS = ("plans", "corpus/evidence/round52/graders/raman-fitting",
                 "corpus/evidence/round86", "SKILL.md")


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
        if line == HEADER:          # the frozen subject line, exactly
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
            cases.append((match.group(1), match.group(2), match.group(3)))
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


def frozen_table(lane: Path) -> tuple[bytes, dict]:
    """The frozen case table, read at FREEZE_REV — never from the measured tree."""
    rev = freeze_rev()
    if git(repo(), "cat-file", "-e", f"{rev}:{TABLE}").returncode != 0:
        raise SetupDefect(f"frozen-input-missing {TABLE}@{rev[:12]}")
    data = git(repo(), "show", f"{rev}:{TABLE}").stdout
    try:
        doc = json.loads(data)
    except json.JSONDecodeError as error:
        raise SetupDefect("frozen-table-malformed") from error
    if doc.get("member") != MEMBER or doc.get("subject_sha") != SUBJECT_SHA:
        raise SetupDefect("frozen-table-identity")
    return data, doc


def check(tree: Tree, lane: Path, work: Path, reproduce: bool = True) -> tuple[list[str], dict]:
    defects: list[str] = []
    stats = {"members": 1, "cases": 0, "legs": 0, "mismatches": 0,
             "located": 0, "executed": 0}
    legs: dict[str, bool] = {}

    frozen_bytes, frozen_doc = frozen_table(lane)

    # L8 — the subject bytes are the pinned capture.
    capture = tree.bytes(CAPTURE)
    if capture is None:
        defects.append(f"L8-subject missing {CAPTURE}")
        legs["L8-subject"] = False
    elif sha256(capture) != SUBJECT_SHA:
        defects.append(f"L8-subject sha {sha256(capture)[:16]}")
        legs["L8-subject"] = False
    else:
        legs["L8-subject"] = True

    # L4 — the measured table is the frozen table, byte for byte.
    table_bytes = tree.bytes(TABLE)
    if table_bytes is None:
        defects.append(f"L4-table missing {TABLE}@{tree.source}")
        legs["L4-table"] = False
    elif table_bytes != frozen_bytes:
        defects.append(f"L4-table drift {sha256(table_bytes)[:16]} != {sha256(frozen_bytes)[:16]}")
        legs["L4-table"] = False
    else:
        legs["L4-table"] = True

    # L7 — the population ledger row.
    ledger_bytes = tree.bytes(LEDGER)
    row = None
    if ledger_bytes is None:
        defects.append(f"L7-ledger missing {LEDGER}")
        legs["L7-ledger"] = False
    else:
        try:
            row = json.loads(ledger_bytes)["members"][MEMBER]
        except (json.JSONDecodeError, KeyError):
            row = None
        if row is None:
            defects.append(f"L7-ledger row {MEMBER}")
            legs["L7-ledger"] = False
        else:
            problems = []
            if row.get("status") != "executed":
                problems.append(f"status={row.get('status')}")
            else:
                stats["executed"] = 1
            if row.get("round") != LEDGER_ROUND:
                problems.append(f"round={row.get('round')}")
            if row.get("receipt") != RECEIPT:
                problems.append(f"receipt={row.get('receipt')}")
            if row.get("subject") != LEDGER_SUBJECT:
                problems.append(f"subject={row.get('subject')}")
            if row.get("verdict") != "cases":
                problems.append(f"verdict={row.get('verdict')}")
            if problems:
                defects.append("L7-ledger " + ",".join(problems))
                legs["L7-ledger"] = False
            else:
                legs["L7-ledger"] = True

    # L1/L2/L3/L5/L6 — the receipt and what it claims.
    receipt_bytes = tree.bytes(RECEIPT)
    block: list[str] = []
    stamp: dict[str, str] = {}
    if receipt_bytes is None:
        defects.append(f"L1-receipt missing {RECEIPT}")
        for leg in ("L1-receipt", "L2-stamp", "L3-tip", "L5-vectors"):
            legs[leg] = False
    else:
        stats["located"] = 1
        legs["L1-receipt"] = True
        stamp, block, problem = parse_receipt(receipt_bytes.decode("utf-8", "replace"))
        if problem:
            defects.append(f"L2-stamp shape {problem}")
            legs["L2-stamp"] = False
        else:
            problems = []
            missing = [field for field in REQUIRED if field not in stamp]
            if missing:
                problems.append("missing=" + ",".join(missing))
            if stamp.get("MEMBER") != MEMBER:
                problems.append(f"member={stamp.get('MEMBER')}")
            if stamp.get("SUBJECT_CAPTURE") != CAPTURE:
                problems.append(f"capture={stamp.get('SUBJECT_CAPTURE')}")
            if stamp.get("SUBJECT_SHA") != SUBJECT_SHA:
                problems.append(f"subject_sha={str(stamp.get('SUBJECT_SHA'))[:16]}")
            if stamp.get("CASE_TABLE_SHA") != sha256(frozen_bytes):
                problems.append(f"table_sha={str(stamp.get('CASE_TABLE_SHA'))[:16]}")
            tool = tree.bytes(TOOL)
            if tool is None:
                problems.append(f"tool-missing={TOOL}")
            elif stamp.get("TOOL") != TOOL:
                problems.append(f"tool={stamp.get('TOOL')}")
            elif stamp.get("TOOL_SHA") != sha256(tool):
                problems.append(f"tool_sha={str(stamp.get('TOOL_SHA'))[:16]}")
            elif stamp.get("TOOL_SHA") != TRUSTED_TOOL_SHA:
                problems.append("tool_sha-not-trusted")
            if stamp.get("EXIT") != "0":
                problems.append(f"exit={stamp.get('EXIT')}")
            if problems:
                defects.append("L2-stamp " + ",".join(problems))
                legs["L2-stamp"] = False
            else:
                legs["L2-stamp"] = True

        declared = stamp.get("LANE_TIP") or ""
        anchor = (tree.tip if tree.tip != "fixture"
                  else git(repo(), "rev-parse", "master").stdout.decode().strip())
        resolvable = (re.fullmatch(r"[0-9a-f]{40}", declared) is not None
                      and git(repo(), "cat-file", "-e", f"{declared}^{{commit}}").returncode == 0)
        ancestor = resolvable and git(repo(), "merge-base", "--is-ancestor", declared,
                                      anchor).returncode == 0
        if not ancestor:
            defects.append(f"L3-tip {declared[:12]} not an ancestor of {anchor[:12]}")
            legs["L3-tip"] = False
        else:
            legs["L3-tip"] = True

        cases, ncases, nlegs, nmis, predicate = parse_cases(block)
        stats.update(cases=ncases, legs=nlegs, mismatches=nmis)
        problems = []
        if [c[0] for c in cases] != [c[0] for c in FROZEN]:
            problems.append("order=" + ",".join(c[0] for c in cases)[:80])
        for case_id, predicted, observed in cases:
            frozen_vector = dict(FROZEN).get(case_id)
            if predicted != frozen_vector:
                problems.append(f"{case_id} predicted={predicted}!={frozen_vector}")
            if observed != predicted:
                problems.append(f"{case_id} observed={observed}!={predicted}")
        if predicate != "pass":
            problems.append(f"predicate={predicate or 'absent'}")
        if (ncases, nlegs, nmis) != (8, 24, 0):
            problems.append(f"summary={ncases}/{nlegs}/{nmis}")
        if problems:
            defects.append("L5-vectors " + ";".join(problems)[:200])
            legs["L5-vectors"] = False
        else:
            legs["L5-vectors"] = True

    # L6 — reproduce the observation block from the measured tree.
    tool = tree.bytes(TOOL)
    if not reproduce:
        legs["L6-reproduce"] = True
    elif tool is None or not (tree.root / TOOL).is_file():
        defects.append(f"L6-reproduce no tool {TOOL}@{tree.source}")
        legs["L6-reproduce"] = False
    elif receipt_bytes is None:
        defects.append("L6-reproduce no receipt to compare")
        legs["L6-reproduce"] = False
    else:
        out = Path(tempfile.mkdtemp(prefix="repro-", dir=work))
        proc = subprocess.run([sys.executable, "-I", "-B", str(tree.root / TOOL),
                               "--lane", str(tree.root), "--work", str(out)],
                              capture_output=True, text=True, timeout=900,
                              env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        fresh_stamp, fresh_block, problem = parse_receipt(proc.stdout)
        if proc.returncode != 0 or problem or fresh_block != block:
            defects.append("L6-reproduce "
                           f"rc={proc.returncode} {problem or 'block differs'}")
            legs["L6-reproduce"] = False
        else:
            legs["L6-reproduce"] = True
        shutil.rmtree(out, ignore_errors=True)

    # exactly one defect line per failed leg, in leg order
    details: dict[str, list[str]] = {}
    for line in defects:
        leg, _, detail = line.partition(" ")
        details.setdefault(leg, []).append(detail)
    defects = [f"{leg} {'; '.join(details[leg])}" if leg in details else leg
               for leg in LEGS if not legs.get(leg)]
    return defects, stats


def result_code(defects: list, stats: dict) -> int:
    ok = (not defects and stats["members"] == 1 and stats["cases"] == 8
          and stats["legs"] == 24 and stats["mismatches"] == 0
          and stats["located"] == 1 and stats["executed"] == 1)
    return 0 if ok else 1


def emit(defects: list, stats: dict, quiet: bool = False) -> int:
    for line in defects:
        print(f"DEFECT {line}")
    print(f"TARGET members={stats['members']} cases={stats['cases']} legs={stats['legs']} "
          f"mismatches={stats['mismatches']} located={stats['located']} "
          f"executed={stats['executed']} defects={len(defects)}")
    code = result_code(defects, stats)
    print(f"PREDICATE R86-C1 {'pass' if code == 0 else 'fail'}")
    return code


def setup_failure(detail: str) -> int:
    print(f"DEFECT SETUP {detail}")
    print("TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=0")
    print("PREDICATE R86-C1 fail")
    return 2


# ---------------------------------------------------------------- controls

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


def working_tree(lane: Path, work: Path) -> Tree:
    """The tree the receipt lives in: the lane worktree when it carries one, else master.

    Controls need a receipt to mutate before it is committed; the measured tip stays
    `git rev-parse master` either way, so L3 keeps comparing against a real revision.
    """
    tip = git(lane, "rev-parse", "master").stdout.decode().strip()
    if (lane / RECEIPT).is_file() and (lane / TOOL).is_file():
        return fixture_tree(copy_tree(Tree(lane, tip, "worktree"), work, "src"))
    return rev_tree(lane, "master", work)


def flip_ledger(root: Path, status: str = "executed") -> None:
    path = root / LEDGER
    doc = json.loads(path.read_bytes())
    row = doc["members"][MEMBER]
    row.update(status=status, round=LEDGER_ROUND, receipt=RECEIPT,
               subject=LEDGER_SUBJECT, verdict="cases")
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")


CONTROLS = ("do-nothing", "ledger-only", "fabricated-observations", "forged-receipt")


def control(lane: Path, work: Path, name: str) -> int:
    if name == "do-nothing":
        tree = rev_tree(lane, BASE_REV, work)
    else:
        root = copy_tree(working_tree(lane, work), work, name)
        tree = fixture_tree(root)
        if name == "ledger-only":
            (root / RECEIPT).unlink()
            flip_ledger(root)
        elif name in ("fabricated-observations", "forged-receipt"):
            flip_ledger(root)      # isolate the receipt leg: the ledger row is data, not the control
        if name == "fabricated-observations":
            text = (root / RECEIPT).read_text(encoding="utf-8")
            (root / RECEIPT).write_text(
                text.replace("CASE extra-schema-keys predicted=P/P/P observed=P/P/P",
                             "CASE extra-schema-keys predicted=P/P/P observed=P/F/P"),
                encoding="utf-8")
        if name == "forged-receipt":
            # a receipt minted from the frozen table alone: correct vectors, correct table
            # digest, but no measured tip — the L3 binding is what refuses it.
            text = (root / RECEIPT).read_text(encoding="utf-8")
            text = re.sub(r"^LANE_TIP .*$", "LANE_TIP " + "0" * 40, text, flags=re.M)
            (root / RECEIPT).write_text(text, encoding="utf-8")
    defects, stats = check(tree, lane, work)
    code = result_code(defects, stats)
    reached = code == 0
    print(f"CONTROL {name} target_reached={reached} defects={len(defects)} "
          f"legs={','.join(sorted({d.split()[0] for d in defects})) or 'none'}")
    return 0 if not reached else 1


MUTANTS = (
    # (name, fixture, [(needle, replacement)], defect the unmutated counter must raise)
    ("no-vectors-no-reproduce", "fabricated",
     [("if observed != predicted:", "if False:"),
      ("if proc.returncode != 0 or problem or fresh_block != block:", "if False:")],
     "L5-vectors"),
    ("no-ledger", "ledger-bad",
     [('if row.get("status") != "executed":', "if False:")], "L7-ledger"),
    ("no-tool-sha", "tool",
     [('elif stamp.get("TOOL_SHA") != sha256(tool):', "elif False:")], "L2-stamp"),
    ("no-tip-binding", "tip", [("if not ancestor:", "if False:")], "L3-tip"),
    ("no-table-binding", "table",
     [("elif table_bytes != frozen_bytes:", "elif False:"),
      ('if stamp.get("CASE_TABLE_SHA") != sha256(frozen_bytes):', "if False:")],
     "L4-table"),
    ("no-exit", "exit",
     [('if stamp.get("EXIT") != "0":', "if False:")], "L2-stamp"),
)


def mutant_fixture(lane: Path, work: Path, kind: str) -> Path:
    root = copy_tree(working_tree(lane, work), work, f"mut-{kind}")
    if kind == "tool":
        # bytes drift with identical output: only the TOOL_SHA leg can see it
        path = root / TOOL
        path.write_bytes(path.read_bytes() + b"\n# drifted copy\n")
    elif kind == "table":
        # a non-vector field drifts AND the receipt's digest is re-minted to match it: only
        # the byte comparison against the frozen table can see the drift (L2 agrees).
        path = root / TABLE
        doc = json.loads(path.read_bytes())
        doc["cases"][0]["why"] = "drifted"
        drifted = (json.dumps(doc, indent=2) + "\n").encode()
        path.write_bytes(drifted)
        receipt = root / RECEIPT
        text = receipt.read_text(encoding="utf-8")
        receipt.write_text(re.sub(r"^CASE_TABLE_SHA .*$", "CASE_TABLE_SHA " + sha256(drifted),
                                  text, flags=re.M), encoding="utf-8")
    elif kind == "tip":
        path = root / RECEIPT
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r"^LANE_TIP .*$", "LANE_TIP " + "1" * 40, text, flags=re.M),
                        encoding="utf-8")
    elif kind == "exit":
        path = root / RECEIPT
        path.write_text(path.read_text(encoding="utf-8").replace("EXIT 0", "EXIT 1"),
                        encoding="utf-8")
    elif kind == "fabricated":
        path = root / RECEIPT
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace(
            "CASE extra-schema-keys predicted=P/P/P observed=P/P/P",
            "CASE extra-schema-keys predicted=P/P/P observed=P/F/P"), encoding="utf-8")
    # every mutant fixture carries the delivered ledger row, so only the mutated leg can
    # decide the verdict; `ledger-bad` is the one fixture whose row is deliberately red.
    flip_ledger(root, status="unexecuted" if kind == "ledger-bad" else "executed")
    return root


# Declared redundant defence: a drifted table also fails the probe's own FROZEN_TABLE_SHA
# pin, so L6 refuses that fixture whatever L4/L2 say.  The byte comparison is kept as
# defence in depth and is NOT claimed as the only gate.
DECLARED_REDUNDANT = {"no-table-binding"}


def mutants(lane: Path, work: Path) -> int:
    """Each removed check must be load-bearing on the fixture it governs."""
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
                                "--repo", str(lane), *freeze_args(),
                                "--work", str(work / f"pw-{name}")],
                               capture_output=True, text=True, timeout=900,
                               env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        mutant = subprocess.run([sys.executable, "-I", "-B", str(mutated), "--lane", str(root),
                                 "--repo", str(lane), *freeze_args(),
                                 "--work", str(work / f"mw-{name}")],
                                capture_output=True, text=True, timeout=900,
                                env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        ok_plain = plain.returncode == 1 and expected in plain.stdout
        ok_mutant = "PREDICATE R86-C1 pass" in mutant.stdout
        print(f"MUTANT {name} fixture={fixture} unmutated_defect={ok_plain} "
              f"mutant_reaches_target={ok_mutant}")
        if ok_plain and ok_mutant:
            necessary += 1
        else:
            redundant += 1
        shutil.rmtree(root, ignore_errors=True)
    declared = len(DECLARED_REDUNDANT)
    print(f"MUTANTS real={len(MUTANTS)} necessary={necessary} redundant={redundant} "
          f"declared_redundant={declared}")
    return 0 if necessary + declared == len(MUTANTS) else 1


def selftest(lane: Path, work: Path) -> int:
    failures = 0
    checks = 0

    def check_case(identifier: str, good: bool) -> None:
        nonlocal failures, checks
        failures += not good
        checks += 1
        print(f"SELFTEST {identifier} {'pass' if good else 'FAIL'}")

    tip = rev_tree(lane, "master", work)
    defects, stats = check(tip, lane, work, reproduce=False)
    check_case("tip-receipt-present", "L1-receipt" not in " ".join(defects))
    check_case("tip-table-frozen", "L4-table" not in " ".join(defects))
    check_case("tip-vectors-frozen", "L5-vectors" not in " ".join(defects))

    root = copy_tree(tip, work, "sel-receipt")
    (root / RECEIPT).unlink()
    defects, stats = check(fixture_tree(root), lane, work, reproduce=False)
    check_case("absent-receipt-red", any(d.startswith("L1-receipt") for d in defects)
               and result_code(defects, stats) == 1)

    root = copy_tree(tip, work, "sel-ledger")
    (root / RECEIPT).unlink()
    flip_ledger(root)
    defects, stats = check(fixture_tree(root), lane, work, reproduce=False)
    check_case("ledger-only-red", any(d.startswith("L1-receipt") for d in defects))

    root = copy_tree(tip, work, "sel-vector")
    (root / RECEIPT).write_text(
        (root / RECEIPT).read_text(encoding="utf-8").replace("observed=P/P/P", "observed=P/F/P", 1),
        encoding="utf-8")
    defects, stats = check(fixture_tree(root), lane, work, reproduce=False)
    check_case("vector-mismatch-red", any(d.startswith("L5-vectors") for d in defects))

    root = copy_tree(tip, work, "sel-tool")
    path = root / TOOL
    path.write_bytes(path.read_bytes() + b"\n")
    defects, stats = check(fixture_tree(root), lane, work, reproduce=False)
    check_case("tool-sha-red", any(d.startswith("L2-stamp") for d in defects))

    root = copy_tree(tip, work, "sel-table")
    path = root / TABLE
    doc = json.loads(path.read_bytes())
    doc["cases"][0]["why"] = "drifted"
    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    defects, stats = check(fixture_tree(root), lane, work, reproduce=False)
    check_case("table-drift-red", any(d.startswith("L4-table") for d in defects))

    try:
        freeze = rev_tree(lane, freeze_rev(), work)
    except SetupDefect:
        check_case("freeze-anchor-present", False)
    else:
        check_case("freeze-anchor-present", freeze.has(TABLE))
        root = copy_tree(freeze, work, "sel-freeze")
        (root / TABLE).unlink()
        proc = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                               "--lane", str(root), "--repo", str(lane), *freeze_args(),
                               "--work", str(work / "sel-freeze-w")],
                              capture_output=True, text=True, timeout=600,
                              env={"PATH": "/usr/bin", "TMPDIR": str(work)})
        check_case("freeze-anchor-fails-closed",
                   proc.returncode == 2 and "DEFECT SETUP" in proc.stdout
                   and "PREDICATE R86-C1 fail" in proc.stdout)

    print(f"SELFTEST cases={checks} red={checks - failures} failures={failures}")
    return 0 if failures == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", default=".")
    parser.add_argument("--rev")
    parser.add_argument("--work", required=True)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--freeze", help="override FREEZE_REV (pre-freeze runs only)")
    parser.add_argument("--repo", help="git repository for frozen inputs and tip ancestry")
    for flag in ("--selftest", "--mutants", "--control-do-nothing", "--control-ledger-only",
                 "--control-fabricated-observations", "--control-forged-receipt"):
        parser.add_argument(flag, action="store_true")
    args = parser.parse_args(argv)
    global _FREEZE, _REPO
    _FREEZE = args.freeze
    lane = Path(args.lane).resolve()
    _REPO = Path(args.repo).resolve() if args.repo else lane
    work = Path(args.work).resolve()
    if not work.exists():
        work.mkdir(parents=True, exist_ok=True)
    if not work.is_dir():
        return setup_failure(f"work-not-a-directory {work}")
    try:
        if args.selftest:
            return selftest(lane, work)
        if args.mutants:
            return mutants(lane, work)
        for flag, name in (("control_do_nothing", "do-nothing"),
                           ("control_ledger_only", "ledger-only"),
                           ("control_fabricated_observations", "fabricated-observations"),
                           ("control_forged_receipt", "forged-receipt")):
            if getattr(args, flag):
                return control(lane, work, name)
        if args.rev:
            return run(rev_tree(lane, args.rev, work), lane, work, args.quiet)
        tree = fixture_tree(lane)
        defects, stats = check(tree, lane, work)
        return emit(defects, stats, args.quiet)
    except SetupDefect as error:
        return setup_failure(str(error))
    except subprocess.TimeoutExpired as error:
        return setup_failure(f"timeout {error}")


def run(tree: Tree, lane: Path, work: Path, quiet: bool = False) -> int:
    defects, stats = check(tree, lane, work)
    return emit(defects, stats, quiet)


if __name__ == "__main__":
    sys.exit(main())
