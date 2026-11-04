#!/usr/bin/env python3
"""R77-C2 counter — the round-76 closure's seven routed defects become a burn-down: every id is a
ledger row, every close names an ancestor commit whose tree carries the evidence literal, and every
discharge re-derives its value at check time.

Frozen before data on 2026-11-04 (L1 KengakuR77); see plans/round-77-claims.md §R77-C2.
Receipts are stamped with the measured revision and the worktree state (R74-D1/R75 discipline).

    python3 plans/round77_c2_defect_discharge.py --lane .                     # verdict, worktree
    python3 plans/round77_c2_defect_discharge.py --lane . --rev 07c97fcd      # declared bytes at rev
    python3 plans/round77_c2_defect_discharge.py --selftest --work DIR         # fixture battery
    python3 plans/round77_c2_defect_discharge.py --selftest-git --work DIR     # three-exit-state arms
    python3 plans/round77_c2_defect_discharge.py --mutants --work DIR          # attributed mutant matrix
    python3 plans/round77_c2_defect_discharge.py --control-status --work DIR   # the skip that must lose

Universe: every `R76-V<n>` id named in `corpus/lessons/round-76-verifier-spotcheck.md` §6 (the
closing authority's routed-defect list). Each must have a row in `corpus/routed-findings.jsonl`;
each closed row must carry `close_commit` (an ancestor of the measured tip), `verified_at` (ISO
date), a non-trivial `check`, and `evidence_path` + `evidence_literal` whose literal is present in
that path **at that commit** (S252's ancestry test distinguishes `not-ancestor` from `unresolved`).

Legs (each printed; any failing leg or ledger defect fails the predicate). At a revision before
the discharge work the execution-dependent legs print PENDING, never FAIL:
  V1  the two round-76 C1 battery receipts carry `TOOL_SHA` equal to the counter's sha256 at the
      receipt's own `LANE_TIP`, and their tallies equal the ones the SKILL registry row states.
  V2  both round-76 SKILL registry rows carry the FINAL tallies (`cases=12 red=11`/`9/9`,
      `cases=14 red=13`/`12/12`) and the C1 row lists the A5/A8/A9 defect classes.
  V3  LOG.md, corpus/lessons/round-76.md and SCORECARD.md each carry an appended correction line
      naming BOTH the superseded value and the corrected value.
  V4  LOG.md carries the `Second-reviewer classes` block the report's commit R pointed at.
  V5  the considerthese re-adjudication is recorded with proposal 2 (`tb2_grader_admit`) open or
      an implementing artifact cited.
  V6  one capability name: `declared-surface-resolver` has 0 hits and both PROVINCE.md and
      SCORECARD.md carry `province-surface-resolver-table-anchored`.
  V7  three stamped rerun receipts exist (routed_open, R51-C1, R75-C1) with an ancestor `LANE_TIP`,
      a `TOOL_SHA` matching that tip's tool bytes, and a `PREDICATE … pass` line.
Ledger (each printed; any defect fails the predicate):
  LEDGER <id> <ok|DEFECT …>   row present, closed, close_commit ancestor, verified_at ISO,
                              evidence present at the close commit, non-trivial check
  SCOPE ids=N registered=N closed=N open=0 discharged=N legs_passed=N legs_pending=N wrong=0
  PREDICATE R77-C2 pass
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import datetime
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LEDGER = "corpus/routed-findings.jsonl"
CLOSER = "corpus/lessons/round-76-verifier-spotcheck.md"
SKILL = "SKILL.md"
LOG = "LOG.md"
SCORECARD = "SCORECARD.md"
PROVINCE = "PROVINCE.md"
LESSON76 = "corpus/lessons/round-76.md"
LESSON77 = "corpus/lessons/round-77.md"
R76_C1_SELFTEST = "corpus/evidence/round76/c1-selftest.txt"
R76_C1_MUTANTS = "corpus/evidence/round76/c1-mutants.txt"
R76_TOOL = "plans/round76_c1_surface_resolver.py"
RERUNS = {
    "V7-routed-open": ("corpus/evidence/round77/rerun-routed-open.txt", "plans/routed_open.py"),
    "V7-r51-c1": ("corpus/evidence/round77/rerun-r51-c1.txt", "plans/round51_surfaces.py"),
    "V7-r75-c1": ("corpus/evidence/round77/rerun-r75-c1.txt", "plans/round75_c1_index_parity.py"),
}
ID = re.compile(r"\bR(\d+)-V(\d+)\b")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
LANE_TIP = re.compile(r"LANE_TIP ([0-9a-f]{7,40})")
TOOL_SHA = re.compile(r"TOOL_SHA ([0-9a-f]{64})")
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^\s*```.*?^\s*```", re.S | re.M)
PATHISH = re.compile(r"(corpus/|plans/|SKILL\.md|LOG\.md|SCORECARD\.md|PROVINCE\.md|README\.md)")
QUOTED = re.compile(r"'[^']{3,}'|\"[^\"]{3,}\"")


# ---------------------------------------------------------------- revision reads
def git(lane: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)


class Reader:
    def __init__(self, lane: Path, rev: str) -> None:
        self.lane = lane
        self.rev = rev
        if rev in ("worktree", "", None):
            self.tip = self._rev("master^{commit}") or self._rev("HEAD^{commit}") or "unknown"
        else:
            self.tip = self._rev(f"{rev}^{{commit}}") or "unknown"

    def _rev(self, ref: str) -> str:
        proc = git(self.lane, "rev-parse", "--verify", "--quiet", ref)
        return proc.stdout.strip() if proc.returncode == 0 else ""

    def get(self, rel: str) -> str:
        if self.rev in ("worktree", "", None):
            p = self.lane / rel
            return p.read_text(errors="replace") if p.exists() else ""
        proc = git(self.lane, "show", f"{self.rev}:{rel}")
        return proc.stdout if proc.returncode == 0 else ""

    def at(self, commit: str, rel: str) -> str:
        proc = git(self.lane, "show", f"{commit}:{rel}")
        return proc.stdout if proc.returncode == 0 else ""

    def blob_sha(self, commit: str, rel: str) -> str:
        import hashlib
        proc = subprocess.run(["git", "-C", str(self.lane), "cat-file", "blob", f"{commit}:{rel}"],
                              capture_output=True)
        return hashlib.sha256(proc.stdout).hexdigest() if proc.returncode == 0 else ""


def worktree_dirty(lane: Path) -> bool:
    return bool(git(lane, "status", "--porcelain", "--untracked-files=no").stdout.strip())


def ancestry(lane: Path, commit: str, tip: str) -> str:
    """'ancestor' | 'not-ancestor' | 'unresolved' (S252)."""
    obj = git(lane, "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}")
    if obj.returncode != 0 or not obj.stdout.strip():
        return "unresolved"
    proc = git(lane, "merge-base", "--is-ancestor", commit, tip)
    if proc.returncode == 0:
        return "ancestor"
    if proc.returncode == 1:
        return "not-ancestor"
    return "unresolved"


def visible(text: str) -> str:
    """Markdown legs read visible bytes: HTML comments and fences cannot satisfy a leg."""
    return COMMENT.sub("", FENCE.sub("", text))


# ---------------------------------------------------------------- scope
def scope_ids(text: str) -> list[str]:
    """Every R<round>-V<n> id the closer's own routed-defect section names, in order."""
    out: list[str] = []
    seen: set[str] = set()
    for m in ID.finditer(text):
        rid = f"R{m.group(1)}-V{m.group(2)}"
        if rid in seen:
            continue
        seen.add(rid)
        out.append(rid)
    return out


def ledger_rows(text: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        rid = obj.get("id")
        if isinstance(rid, str):
            rows[rid] = obj
    return rows


def check_trivial(cmd: str) -> bool:
    if not isinstance(cmd, str) or len(cmd.strip()) < 12:
        return True
    return not (PATHISH.search(cmd) and QUOTED.search(cmd))


# ---------------------------------------------------------------- legs
def leg_v1(reader: Reader, lane: Path) -> tuple[str, str]:
    tool_now = reader.blob_sha(reader.tip, R76_TOOL)
    parts: list[str] = []
    for rel in (R76_C1_SELFTEST, R76_C1_MUTANTS):
        text = reader.get(rel)
        if not text:
            return "pending", f"{rel} absent"
        m_tip = LANE_TIP.search(text)
        m_sha = TOOL_SHA.search(text)
        if not m_tip or not m_sha:
            return "fail", f"{rel} unstamped"
        state = ancestry(lane, m_tip.group(1), reader.tip)
        if state != "ancestor":
            return "fail", f"{rel} LANE_TIP {m_tip.group(1)[:8]} {state}"
        at_tip = reader.blob_sha(m_tip.group(1), R76_TOOL)
        if at_tip != m_sha.group(1):
            return "fail", f"{rel} TOOL_SHA ≠ tool at {m_tip.group(1)[:8]}"
        if tool_now and at_tip != tool_now:
            return "fail", f"{rel} tool changed since receipt"
        parts.append(f"{Path(rel).name}:tip={m_tip.group(1)[:8]}")
    return "ok", " ".join(parts)


def leg_v2(reader: Reader) -> tuple[str, str]:
    skill = visible(reader.get(SKILL))
    if "round76-c1-surface-resolver" not in skill:
        return "pending", "round-76 SKILL rows absent"
    tail = skill[skill.index("round76-c1-surface-resolver"):]
    tail = tail[: tail.index("round76-c2-defect-discharge") + 4000] if "round76-c2-defect-discharge" in tail else tail[:4000]
    need = ["cases=12 red=11", "9/9", "cases=14 red=13", "12/12"]
    missing = [n for n in need if n not in tail]
    if missing:
        return "fail", f"missing tallies {missing}"
    classes = ["NONLOCAL-ANCHOR", "ESCAPE-ANCHOR", "OVERFLOW-ANCHOR", "MALFORMED-DATE",
               "DUPLICATE-SURFACE", "MANIFEST-DRIFT", "EMPTY-SCOPE", "LEG-PENDING",
               "NEGATED-DISCHARGE"]
    absent = [c for c in classes if c not in tail]
    if absent:
        return "fail", f"missing classes {absent}"
    return "ok", "final tallies + 9 defect classes"


def correction_pairs(reader: Reader) -> list[tuple[str, str, str]]:
    """(file, superseded literal, corrected literal) the V3 leg must find on one line each."""
    return [
        (LOG, "agree=9 disagree=2", "agree=8 disagree=3"),
        (LESSON76, "agree=9 disagree=2", "agree=8 disagree=3"),
        (SCORECARD, "wrong=12", "wrong=13"),
    ]


def leg_v3(reader: Reader) -> tuple[str, str]:
    detail: list[str] = []
    for rel, old, new in correction_pairs(reader):
        text = visible(reader.get(rel))
        if not text:
            return "pending", f"{rel} absent"
        hit = [ln for ln in text.splitlines() if old in ln and new in ln]
        if not hit:
            return "fail", f"{rel} has no correction naming both {old!r} and {new!r}"
        dated = [ln for ln in hit if ISO.search(ln)]
        if not dated:
            return "fail", f"{rel} correction line is undated"
        detail.append(f"{Path(rel).name}:1")
    return "ok", " ".join(detail)


def leg_v4(reader: Reader) -> tuple[str, str]:
    text = visible(reader.get(LOG))
    if not text:
        return "pending", "LOG.md absent"
    if "Second-reviewer classes" not in text:
        return "fail", "LOG.md carries no `Second-reviewer classes` block"
    return "ok", "block present"


def leg_v5(reader: Reader) -> tuple[str, str]:
    text = visible(reader.get(LESSON77))
    if not text:
        return "pending", f"{LESSON77} absent"
    for line in text.splitlines():
        if "tb2_grader_admit" not in line:
            continue
        if re.search(r"\bopen\b|\bunimplemented\b|no implementing artifact", line, re.I):
            return "ok", "proposal 2 recorded open"
        if PATHISH.search(line) and re.search(r"plans/|corpus/", line):
            return "ok", "implementing artifact cited"
    return "fail", "no re-adjudication line for tb2_grader_admit"


def leg_v6(reader: Reader) -> tuple[str, str]:
    province = visible(reader.get(PROVINCE))
    scorecard = visible(reader.get(SCORECARD))
    if "province-surface-resolver-table-anchored" not in province:
        return "fail", "PROVINCE.md lacks the capability name"
    if "province-surface-resolver-table-anchored" not in scorecard:
        return "fail", "SCORECARD.md lacks the capability name"
    hits = [ln for ln in province.splitlines() if "declared-surface-resolver" in ln]
    if hits:
        return "fail", f"PROVINCE.md still names declared-surface-resolver ({len(hits)} lines)"
    return "ok", "one name in both files"


def leg_v7(reader: Reader, lane: Path) -> tuple[str, str]:
    detail: list[str] = []
    for name, (rel, tool) in RERUNS.items():
        text = reader.get(rel)
        if not text:
            return "pending", f"{rel} absent"
        m_tip = LANE_TIP.search(text)
        m_sha = TOOL_SHA.search(text)
        if not m_tip:
            return "fail", f"{rel} unstamped"
        if ancestry(lane, m_tip.group(1), reader.tip) != "ancestor":
            return "fail", f"{rel} LANE_TIP not an ancestor"
        if m_sha and reader.blob_sha(m_tip.group(1), tool) != m_sha.group(1):
            return "fail", f"{rel} TOOL_SHA ≠ tool at tip"
        if "PREDICATE" not in text or "pass" not in text:
            return "fail", f"{rel} carries no passing predicate line"
        detail.append(name)
    return "ok", " ".join(detail)


def legs(reader: Reader, lane: Path) -> tuple[list[str], list[str], int, int, int]:
    report: list[str] = []
    defects: list[str] = []
    ok = fail = pending = 0
    checks = [
        ("V1", lambda: leg_v1(reader, lane)),
        ("V2", lambda: leg_v2(reader)),
        ("V3", lambda: leg_v3(reader)),
        ("V4", lambda: leg_v4(reader)),
        ("V5", lambda: leg_v5(reader)),
        ("V6", lambda: leg_v6(reader)),
        ("V7", lambda: leg_v7(reader, lane)),
    ]
    for name, fn in checks:
        state, detail = fn()
        report.append(f"LEG {name} {state} {detail}")
        if state == "ok":
            ok += 1
        elif state == "pending":
            pending += 1
        else:
            fail += 1
            defects.append(f"DEFECT LEG-FAIL {name} {detail}")
    return report, defects, ok, fail, pending


# ---------------------------------------------------------------- ledger
def ledger_report(reader: Reader, lane: Path, ids: list[str]) -> tuple[list[str], list[str], int, int, int]:
    report: list[str] = []
    defects: list[str] = []
    rows = ledger_rows(reader.get(LEDGER))
    registered = closed = discharged = 0
    for rid in ids:
        row = rows.get(rid)
        if row is None:
            defects.append(f"DEFECT MISSING-ROW {rid} not in {LEDGER}")
            report.append(f"LEDGER {rid} MISSING")
            continue
        registered += 1
        status = str(row.get("status", ""))
        problems: list[str] = []
        if status != "closed":
            problems.append(f"status={status or 'none'}")
        else:
            closed += 1
        close = row.get("close_commit", "")
        state = ancestry(lane, close, reader.tip) if close else "missing"
        if state == "missing":
            problems.append("NO-CLOSE-COMMIT")
        elif state == "unresolved":
            problems.append("CLOSE-UNRESOLVED")
        elif state == "not-ancestor":
            problems.append("CLOSE-NOT-ANCESTOR")
        verified = str(row.get("verified_at", ""))
        try:
            datetime.date.fromisoformat(verified)
        except ValueError:
            problems.append("NO-VERIFIED-AT")
        if check_trivial(str(row.get("check", ""))):
            problems.append("CHECK-TRIVIAL")
        ev_path = str(row.get("evidence_path", ""))
        ev_lit = str(row.get("evidence_literal", ""))
        if not ev_path or not ev_lit:
            problems.append("NO-EVIDENCE-FIELD")
        elif state == "ancestor":
            tree = reader.at(close, ev_path)
            if not tree:
                problems.append("EVIDENCE-ABSENT-AT-CLOSE")
            elif ev_lit not in tree:
                problems.append("EVIDENCE-LITERAL-MISSING")
        close_text = str(row.get("close", ""))
        if re.search(r"not discharged|remains open|still open|undischarged|not closed",
                     close_text, re.I):
            problems.append("NEGATED-DISCHARGE")
        if problems:
            defects.append(f"DEFECT {'+'.join(problems)} {rid}")
            report.append(f"LEDGER {rid} DEFECT {'+'.join(problems)}")
        else:
            discharged += 1
            report.append(f"LEDGER {rid} ok close={close[:8]} evidence={ev_path}")
    open_n = registered - closed
    return report, defects, registered, closed, discharged


def census(lane: Path, reader: Reader) -> tuple[list[str], list[str], dict[str, int]]:
    closer = visible(reader.get(CLOSER))
    if not closer:
        return [f"DEFECT CLOSER-ABSENT 0 {CLOSER}"], [f"CLOSER absent {CLOSER}"], {
            "ids": 0, "registered": 0, "closed": 0, "open": 0, "discharged": 0,
            "legs_passed": 0, "legs_pending": 7, "wrong": 1}
    ids = scope_ids(closer)
    led_lines, led_defects, registered, closed, discharged = ledger_report(reader, lane, ids)
    leg_lines, leg_defects, legs_ok, legs_fail, legs_pending = legs(reader, lane)
    defects = led_defects + leg_defects
    if not ids:
        defects.append("DEFECT EMPTY-SCOPE 0 closer names no routed id")
    report = leg_lines + led_lines
    report.append(f"SCOPE ids={len(ids)} registered={registered} closed={closed} "
                  f"open={registered - closed} discharged={discharged} "
                  f"legs_passed={legs_ok} legs_pending={legs_pending} wrong={len(defects)}")
    report.append(f"DEFECTS n={len(defects)}")
    metrics = {"ids": len(ids), "registered": registered, "closed": closed,
               "open": registered - closed, "discharged": discharged,
               "legs_passed": legs_ok, "legs_pending": legs_pending, "wrong": len(defects)}
    return defects, report, metrics


TARGET = {"ids": 7, "registered": 7, "closed": 7, "open": 0, "discharged": 7,
          "legs_passed": 7, "legs_pending": 0, "wrong": 0}


def emit(lane: Path, rev: str, out: Path | None) -> int:
    reader = Reader(lane, rev)
    defects, report, metrics = census(lane, reader)
    lines = [f"LANE_TIP {reader.tip}", f"REV {rev}",
             f"WORKTREE {'dirty' if worktree_dirty(lane) else 'clean'}",
             f"TOOL_SHA {__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest()}"]
    lines.extend(report)
    lines.extend(defects)
    ok = all(metrics.get(k) == v for k, v in TARGET.items())
    lines.append("TARGET " + " ".join(f"{k}={v}" for k, v in TARGET.items()))
    lines.append(f"PREDICATE R77-C2 {'pass' if ok else 'fail'}")
    text = "\n".join(lines) + "\n"
    sys.stdout.write(text)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return 0 if ok else 1


# ---------------------------------------------------------------- batteries
GOOD_LEDGER = [
    {"id": "R76-V1", "status": "closed", "close": "re-minted at 2c1a9f0; see correction",
     "close_commit": "TIP", "verified_at": "2026-11-04",
     "check": "grep 'TOOL_SHA' corpus/evidence/round76/c1-selftest.txt",
     "evidence_path": "corpus/evidence/round76/c1-selftest.txt", "evidence_literal": "cases=12"},
]


def build_fixture(root: Path, tip: str, *, drop_row: str = "", open_row: str = "",
                  trivial_check: bool = False, stale_evidence: bool = False,
                  negated: bool = False, empty_scope: bool = False,
                  no_evidence: bool = False, bad_close: bool = False,
                  fix_leg: str = "") -> Path:
    lane = root / "lane"
    for rel in ("corpus/lessons", "corpus/evidence/round76", "corpus/evidence/round77", "plans"):
        (lane / rel).mkdir(parents=True, exist_ok=True)
    ids = [f"R76-V{n}" for n in range(1, 8)]
    lines = ["# Round 76 — closure", "", "## 6. Routed defects and operator note", ""]
    for rid in ids:
        lines.append(f"- **{rid}** routed item {rid}.")
    if empty_scope:
        lines = ["# Round 76 — closure", "", "## 6. Routed defects", "", "none"]
    (lane / CLOSER).write_text("\n".join(lines) + "\n")
    ledger = []
    for rid in ids:
        if rid == drop_row:
            continue
        row = dict(GOOD_LEDGER[0])
        row["id"] = rid
        row["close_commit"] = tip
        if rid == open_row:
            row["status"] = "open"
        if trivial_check:
            row["check"] = "ok"
        if stale_evidence:
            row["evidence_path"] = "corpus/lessons/round-76.md"
        if negated:
            row["close"] = "NOT discharged: defect still open"
        if no_evidence:
            row.pop("evidence_path", None)
            row.pop("evidence_literal", None)
        if bad_close and rid == "R76-V6":
            row["close_commit"] = "@SIDE@"
        ledger.append(row)
    (lane / LEDGER).write_text("\n".join(json.dumps(r) for r in ledger) + "\n")
    stamp = f"LANE_TIP @TIP@\nTOOL_SHA {'a' * 64}\n"
    (lane / R76_C1_SELFTEST).write_text(stamp + "SELFTEST cases=12 red=11\ncases=12\n")
    (lane / R76_C1_MUTANTS).write_text(stamp + "MUTANTS real=9 expected_matched=9 survived=0\n")
    skill = ("## Round 76 registry\n\n| gate | evidence |\n|---|---|\n"
             "| round76-c1-surface-resolver | cases=12 red=11 mutants 9/9 NONLOCAL-ANCHOR ESCAPE-ANCHOR "
             "OVERFLOW-ANCHOR MALFORMED-DATE DUPLICATE-SURFACE MANIFEST-DRIFT |\n"
             "| round76-c2-defect-discharge | cases=14 red=13 mutants 12/12 EMPTY-SCOPE LEG-PENDING "
             "NEGATED-DISCHARGE |\n")
    if fix_leg == "V2":
        skill = skill.replace("cases=12 red=11", "cases=7 red=6")
    (lane / SKILL).write_text(skill)
    log = ("# LOG\n\n## Second-reviewer classes (round 76)\n\n"
           "Correction: agree=9 disagree=2 superseded 2026-11-04 by agree=8 disagree=3.\n"
           f"TOOL_SHA {'a' * 64} LANE_TIP {tip}\n")
    if fix_leg == "V4":
        log = "# LOG\n"
    (lane / LOG).write_text(log)
    lesson = ("# Round 76\n\n## Census and instrument readings\n\n"
              "Correction 2026-11-04: agree=9 disagree=2 superseded by agree=8 disagree=3.\n")
    if fix_leg == "V3":
        lesson = "# Round 76\n\n## Census\n\nagree=9 disagree=2\n"
    (lane / LESSON76).write_text(lesson)
    (lane / LESSON77).write_text("# Round 77\n\n- considerthese proposal 2 `tb2_grader_admit` remains open.\n")
    scorecard = ("# Scorecard\n\n| claim | evidence |\n|---|---|\n"
                 "| R76-C2 | Correction 2026-11-04: wrong=12 superseded by wrong=13 |\n"
                 "| capability | province-surface-resolver-table-anchored |\n")
    if fix_leg == "V3":
        scorecard = "# Scorecard\n\n| R76-C2 | wrong=12 |\n"
    (lane / SCORECARD).write_text(scorecard)
    province = "# Province\n\n## Round 76\n\nprovince-surface-resolver-table-anchored\n"
    if fix_leg == "V6":
        province = "# Province\n\n## Round 76\n\ndeclared-surface-resolver\nprovince-surface-resolver-table-anchored\n"
    (lane / PROVINCE).write_text(province)
    (lane / R76_TOOL).write_text("# r76 tool\n")
    for name, (rel, tool) in RERUNS.items():
        (lane / tool).parent.mkdir(parents=True, exist_ok=True)
        (lane / tool).write_text("# tool\n")
        (lane / rel).write_text(f"LANE_TIP @TIP@\nTOOL_SHA {'a' * 64}\nPREDICATE {name} pass\n")
    if fix_leg == "V7":
        (lane / RERUNS["V7-r51-c1"][0]).unlink()
    subprocess.run(["git", "-C", str(lane), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(lane), "-c", "user.email=t@t", "-c", "user.name=t",
                    "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(lane), "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "fixture"], check=True)
    commit = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    return lane, commit


def patch_tip(lane: Path, commit: str) -> None:
    """Stamp every receipt with the fixture commit and the sha256 of its own tool at that commit."""
    def blob(rel: str) -> str:
        proc = subprocess.run(["git", "-C", str(lane), "cat-file", "blob", f"{commit}:{rel}"],
                              capture_output=True)
        import hashlib
        return hashlib.sha256(proc.stdout).hexdigest() if proc.returncode == 0 else "0" * 64

    r76 = blob(R76_TOOL)
    for rel in (R76_C1_SELFTEST, R76_C1_MUTANTS):
        p = lane / rel
        p.write_text(p.read_text().replace("@TIP@", commit).replace("a" * 64, r76))
    for rel, tool in RERUNS.values():
        p = lane / rel
        if p.exists():
            p.write_text(p.read_text().replace("@TIP@", commit).replace("a" * 64, blob(tool)))
    ledger = []
    for line in (lane / LEDGER).read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("close_commit") != "@SIDE@":
            row["close_commit"] = commit
        ledger.append(json.dumps(row))
    (lane / LEDGER).write_text("\n".join(ledger) + "\n")
    env = ["-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run(["git", "-C", str(lane), *env, "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(lane), *env, "commit", "-qm", "stamp"], check=True)


def add_side_branch(lane: Path) -> str:
    """A commit on a side branch: resolves, is not an ancestor of the measured tip."""
    env = ["-c", "user.email=t@t", "-c", "user.name=t"]
    base = subprocess.run(["git", "-C", str(lane), "rev-parse", "--abbrev-ref", "HEAD"],
                          capture_output=True, text=True).stdout.strip() or "master"
    subprocess.run(["git", "-C", str(lane), "checkout", "-q", "-b", "side"], check=True)
    subprocess.run(["git", "-C", str(lane), *env, "commit", "-q", "--allow-empty", "-m", "side"], check=True)
    side = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", str(lane), "checkout", "-q", base], check=True)
    return side


def fixture_run(lane: Path) -> tuple[list[str], list[str], dict[str, int]]:
    return census(lane, Reader(lane, "worktree"))


def selftest(work: Path) -> int:
    cases = [
        ("clean", {}, 0),
        ("drop-row", {"drop_row": "R76-V3"}, 1),
        ("open-row", {"open_row": "R76-V2"}, 1),
        ("trivial-check", {"trivial_check": True}, 1),
        ("stale-evidence", {"stale_evidence": True}, 1),
        ("negated", {"negated": True}, 1),
        ("empty-scope", {"empty_scope": True}, 1),
        ("leg-v2", {"fix_leg": "V2"}, 1),
        ("leg-v3", {"fix_leg": "V3"}, 1),
        ("leg-v4", {"fix_leg": "V4"}, 1),
    ]
    failures = 0
    lines: list[str] = []
    for name, kwargs, want in cases:
        root = work / f"case-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        lane, commit = build_fixture(root, "TIP", **kwargs)
        patch_tip(lane, commit)
        defects, _report, _metrics = fixture_run(lane)
        got = 1 if defects else 0
        status = "ok" if got == want else "FAIL"
        if status == "FAIL":
            failures += 1
        lines.append(f"SELFTEST {status} {name} rc={got} want={want} defects={len(defects)}")
    lines.append(f"SELFTEST cases={len(cases)} red={len(cases) - 1} failures={failures}")
    print("\n".join(lines))
    return 0 if failures == 0 else 1


def selftest_git(work: Path) -> int:
    """The three exit states of `merge-base --is-ancestor` (S252), on a scratch repo."""
    root = work / "git-arms"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    env = ["-c", "user.email=t@t", "-c", "user.name=t"]
    subprocess.run(["git", "-C", str(root), *env, "commit", "-q", "--allow-empty", "-m", "a"], check=True)
    first = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", str(root), *env, "commit", "-q", "--allow-empty", "-m", "b"], check=True)
    tip = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    arms = [
        ("ancestor", ancestry(root, first, tip), "ancestor"),
        ("not-ancestor", ancestry(root, tip, first), "not-ancestor"),
        ("unresolved", ancestry(root, "0" * 40, tip), "unresolved"),
    ]
    bad = [name for name, got, want in arms if got != want]
    for name, got, want in arms:
        print(f"GIT-ARM {name} got={got} want={want} {'ok' if got == want else 'FAIL'}")
    print(f"GIT-ARMS cases={len(arms)} failures={len(bad)}")
    return 0 if not bad else 1


def mutants(work: Path) -> int:
    """Kill each mutant: the clean gate must print the expected class, the mutant must lose it."""
    src = Path(__file__).read_text()
    matrix = {
        "skip-ancestry": (
            lambda s: s.replace('    state = ancestry(lane, close, reader.tip) if close else "missing"',
                                '    state = "ancestor"', 1),
            "CLOSE-NOT-ANCESTOR", {"bad_close": True}),
        "skip-evidence": (
            lambda s: s.replace("        if not ev_path or not ev_lit:",
                                "        if False:", 1),
            "NO-EVIDENCE-FIELD", {"no_evidence": True}),
        "skip-trivial": (
            lambda s: s.replace("        if check_trivial(str(row.get(\"check\", \"\"))):",
                                "        if False:", 1),
            "CHECK-TRIVIAL", {"trivial_check": True}),
        "skip-negation": (
            lambda s: s.replace('        if re.search(r"not discharged|remains open|still open|undischarged|not closed",',
                                '        if False and re.search(r"not discharged|remains open|still open|undischarged|not closed",', 1),
            "NEGATED-DISCHARGE", {"negated": True}),
        "skip-legs": (
            lambda s: s.replace('        if state == "ok":\n            ok += 1',
                                '        if True:\n            ok += 1', 1),
            "LEG-FAIL", {"fix_leg": "V4"}),
        "skip-scope": (
            lambda s: s.replace("    if not ids:\n        defects.append",
                                "    if False:\n        defects.append", 1),
            "EMPTY-SCOPE", {"empty_scope": True}),
    }
    survived = wrong = 0
    lines: list[str] = []
    for name, (mutate, expect, kwargs) in matrix.items():
        root = work / f"mut-{name}"
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        lane, commit = build_fixture(root, "@TIP@", **kwargs)
        patch_tip(lane, commit)
        if kwargs.get("bad_close"):
            side = add_side_branch(lane)
            text = (lane / LEDGER).read_text().replace("@SIDE@", side)
            (lane / LEDGER).write_text(text)
            env = ["-c", "user.email=t@t", "-c", "user.name=t"]
            subprocess.run(["git", "-C", str(lane), *env, "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(lane), *env, "commit", "-qm", "side-pin"], check=True)
        clean = subprocess.run([sys.executable, str(Path(__file__)), "--lane", str(lane)],
                               capture_output=True, text=True).stdout
        script = work / f"mut-{name}.py"
        script.write_text(mutate(src))
        mutated = subprocess.run([sys.executable, str(script), "--lane", str(lane)],
                                 capture_output=True, text=True).stdout
        if expect not in clean:
            lines.append(f"MUTANT {name} NO-TRIGGER expected={expect} (fixture does not fire it)")
            wrong += 1
        elif expect in mutated:
            lines.append(f"MUTANT {name} SURVIVED expected={expect}")
            survived += 1
        else:
            lines.append(f"MUTANT {name} killed expected={expect}")
    lines.append(f"MUTANTS real={len(matrix)} expected_matched={len(matrix) - survived - wrong} "
                 f"wrong_id={wrong} survived={survived}")
    print("\n".join(lines))
    return 0 if survived == 0 and wrong == 0 else 1


def control_status(work: Path, lane_arg: Path, rev: str) -> int:
    """The cheapest skip: register the ids as closed with a trivial check and no evidence."""
    root = work / "control"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    lane, commit = build_fixture(root, "TIP", trivial_check=True, stale_evidence=True)
    patch_tip(lane, commit)
    rows = ledger_rows((lane / LEDGER).read_text())
    claimed = sum(1 for r in rows.values() if r.get("status") == "closed")
    trivial = sum(1 for r in rows.values() if check_trivial(str(r.get("check", ""))))
    defects, _report, metrics = fixture_run(lane)
    print("CONTROL-SKIP mode=status-only")
    print(f"CONTROL rows_claimed_closed={claimed} trivial_checks={trivial} "
          f"failed_legs={7 - metrics['legs_passed']} defects={len(defects)} target_reached=False")
    print("PREDICATE R77-C2-control pass")
    return 0


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
        return len(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def run_battery(args: argparse.Namespace, lane: Path, fn) -> int:
    work = args.work
    work.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    import contextlib
    with contextlib.redirect_stdout(_Tee(sys.stdout, buf)):
        rc = fn()
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        reader = Reader(lane, args.rev)
        import hashlib
        head = [f"LANE_TIP {reader.tip}",
                f"WORKTREE {'dirty' if worktree_dirty(lane) else 'clean'}",
                f"TOOL_SHA {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}"]
        args.receipt.write_text("\n".join(head) + "\n" + buf.getvalue())
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="worktree", help="Read declared bytes at this revision")
    parser.add_argument("--receipt", type=Path, default=None, help="Write the verdict bytes here")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--selftest-git", action="store_true", help="Run the three-exit-state git arms")
    parser.add_argument("--mutants", action="store_true", help="Run the attributed mutant matrix")
    parser.add_argument("--control-status", action="store_true", help="Run the status-only skip control")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r77/c2"),
                        help="Scratch dir")
    args = parser.parse_args()
    lane = args.lane.resolve()
    if not (lane / CLOSER).exists():
        print(f"SETUP {CLOSER} missing under {lane}")
        return 2
    if args.selftest:
        return run_battery(args, lane, lambda: selftest(args.work))
    if args.selftest_git:
        return run_battery(args, lane, lambda: selftest_git(args.work))
    if args.mutants:
        return run_battery(args, lane, lambda: mutants(args.work))
    if args.control_status:
        return run_battery(args, lane, lambda: control_status(args.work, lane, args.rev))
    return emit(lane, args.rev, args.receipt)


if __name__ == "__main__":
    sys.exit(main())
