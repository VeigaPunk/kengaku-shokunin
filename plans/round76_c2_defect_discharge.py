#!/usr/bin/env python3
"""R76-C2 counter — the closure's routed defects become a burn-down: every id is registered,
every closed row's discharge re-derives at the tip, every close names an ancestor commit.

Frozen before data on 2026-11-04 (L1 KengakuR76); see plans/round-76-claims.md §R76-C2.
Receipts are stamped with the measured revision and the worktree state (R74-D1/R75 discipline).

    python3 plans/round76_c2_defect_discharge.py --lane .                    # verdict, worktree
    python3 plans/round76_c2_defect_discharge.py --lane . --rev 4c4249a2     # declared bytes at rev
    python3 plans/round76_c2_defect_discharge.py --selftest --work DIR        # fixture battery
    python3 plans/round76_c2_defect_discharge.py --mutants --work DIR         # attributed mutant matrix
    python3 plans/round76_c2_defect_discharge.py --control-status --work DIR  # the skip that must lose

Why this counter exists: the round-75 closure routed seven defects (R75-D1…D7) and none of them
entered the lane's ledger — `corpus/routed-findings.jsonl` still held only R34/R51/R56/R58 rows —
so nothing could price whether they were discharged. `considerthese/2026-10-26.md` proposal 1 asks
for exactly this: a routed-findings burn-down, not a defect prose list.

Universe: every `R<round>-D<n>` id named in the newest `corpus/lessons/round-*-verifier-spotcheck.md`
(the closing authority's own routed-defect list). Each must have a row in
`corpus/routed-findings.jsonl`; each closed row must carry `close_commit` (an ancestor of the
measured tip), `verified_at` (ISO date), a non-trivial `check`, and pass its discharge leg.

Legs (each printed; any failing leg or ledger defect fails the predicate). At a revision before
the discharge work the execution-dependent legs print PENDING, never FAIL, so the before receipt
names exactly what is missing rather than pretending to have run:
  D1  QUALITY.md carries a criterion citing R75-D1 and the lesson that produced it.
  D2  a SCORECARD.md line names R75-D2, the LANE_TIP stamped in round75/c1-after.txt, and 5d9a0ccc.
  D3  a SCORECARD.md line names R75-D3, the final-rule before total and its per-universe split,
      both derived natively at the round-75 base (rendered README rows + `git ls-tree`).
  D4  the round75-c1/c2 SKILL.md registry rows carry the selftest counts the gates actually print.
  D5  a LOG.md block within six lines of R75-D5 names those counts and the c1-after LANE_TIP.
  D6  the two round-76 receipts exist, carry their PREDICATE pass line, and stamp an ancestor tip.
  D7  corpus/lessons/round-74.md carries an appended correction naming R75-D7 (not a reflow).

Ledger (each printed; any defect fails the predicate):
  LEDGER <id> <ok|DEFECT ...>   row present, closed, close_commit ancestor, verified_at ISO, real check
  SCOPE ids=N registered=N closed=N open=0 legs_passed=N legs_pending=N wrong=0
  PREDICATE R76-C2 pass
Exit 0 pass, 1 fail, 2 setup.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import re
import shutil
import subprocess
import io
import sys
from pathlib import Path

LEDGER = "corpus/routed-findings.jsonl"
QUALITY = "corpus/QUALITY.md"
SCORECARD = "SCORECARD.md"
LOG = "LOG.md"
SKILL = "SKILL.md"
C1_AFTER = "corpus/evidence/round75/c1-after.txt"
R74C1 = "corpus/evidence/round76/r74-c1-tip.txt"
R74C2 = "corpus/evidence/round76/r74-c2-tip.txt"
ROUND74_LESSON = "corpus/lessons/round-74.md"
# R75-D3 measured its final-rule "before" at the round-75 freeze (Amendment A1) 43255758, where the
# disk has the round-75 lesson/evidence and the README does not yet index them: 60 = 4/36/20.
BASE75 = "43255758"
ID = re.compile(r"\bR(\d+)-D(\d+)\b")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
PATHISH = re.compile(r"(corpus/|plans/|SKILL\.md|LOG\.md|SCORECARD\.md|PROVINCE\.md|README\.md)")
QUOTED = re.compile(r"'[^']{3,}'|\"[^\"]{3,}\"")
CELLSPLIT = re.compile(r"(?<!\\)\|")
FIRST_CELL = re.compile(r"`(knowledge|lessons)/([^`]+)`")
EVIDENCE = re.compile(r"corpus/evidence/([A-Za-z0-9_.-]+)/")
COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^\s*```.*?^\s*```", re.S | re.M)
SHA40 = re.compile(r"\b[0-9a-f]{40}\b")
# A discharge line that also says the defect is not discharged is not a discharge (CriticR76).
NEGATION = re.compile(r"(not\s+discharged|remains?\s+open|still\s+open|undischarged|not\s+closed)", re.I)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


class Reader:
    """Reads lane paths from the worktree or a revision; git probes run against `probe`."""

    def __init__(self, lane: Path, rev: str, probe: Path | None = None) -> None:
        self.lane, self.rev = lane, rev
        self.probe = probe or lane
        proc = git(self.probe, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}" if rev not in ("worktree", "", None) else "master^{commit}")
        self.tip = proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else "unknown"

    def get(self, rel: str) -> str:
        if self.rev in ("worktree", "", None):
            p = self.lane / rel
            return p.read_text(errors="replace") if p.exists() else ""
        return git(self.lane, "show", f"{self.rev}:{rel}").stdout

    def exists(self, rel: str) -> bool:
        if self.rev in ("worktree", "", None):
            return (self.lane / rel).exists()
        return git(self.lane, "cat-file", "-e", f"{self.rev}:{rel}").returncode == 0

    def ancestry(self, sha: str) -> tuple[str, str]:
        """(state, full-sha) with S252's three states: ancestor / not-ancestor / error / unresolved."""
        proc = git(self.probe, "rev-parse", "--verify", "--quiet", f"{sha}^{{commit}}")
        full = proc.stdout.strip()
        if proc.returncode != 0 or not full:
            return "unresolved", ""
        target = self.tip
        if target == "unknown":  # worktree mode: ancestry is measured against the branch tip
            target = git(self.probe, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip()
        if not target:
            return "unknown", full
        anc = git(self.probe, "merge-base", "--is-ancestor", full, target)
        if anc.returncode == 0:
            return "ancestor", full
        if anc.returncode == 1:
            return "not-ancestor", full
        return "error", full

    def at_rev(self, sha: str, rel: str) -> str:
        """The blob of `rel` at commit `sha`; '' when the path is not in that tree.

        Fixture mode (probe != lane) falls back to the fixture's own file so a battery can test the
        evidence leg without inventing a git history; production reads the commit only."""
        if self.probe != self.lane:  # fixture mode reads its own bytes
            p = self.lane / rel
            return p.read_text(errors="replace") if p.exists() else ""
        return git(self.probe, "show", f"{sha}:{rel}").stdout

    def resolved(self, sha: str) -> tuple[bool, str]:
        state, full = self.ancestry(sha)
        return state == "ancestor", full


def worktree_dirty(lane: Path) -> bool:
    return bool(git(lane, "status", "--porcelain", "--untracked-files=no").stdout.strip())


# ---------------------------------------------------------------- scope + ledger
def scope_ids(reader: Reader) -> tuple[list[str], str]:
    pattern = re.compile(r"corpus/lessons/round-(\d+)-verifier-spotcheck\.md$")
    if reader.rev in ("worktree", "", None):
        names = [str(p.relative_to(reader.lane)) for p in (reader.lane / "corpus/lessons").glob("round-*-verifier-spotcheck.md")]
    else:
        names = git(reader.lane, "ls-tree", "-r", "--name-only", reader.rev, "corpus/lessons").stdout.splitlines()
    best: tuple[int, str] | None = None
    for name in names:
        m = pattern.match(name.strip())
        if m:
            key = int(m.group(1))
            if best is None or key > best[0]:
                best = (key, name.strip())
    if best is None:
        return [], ""
    text = reader.get(best[1])
    seen: list[tuple[int, int, str]] = []
    for m in ID.finditer(text):
        seen.append((int(m.group(1)), int(m.group(2)), f"R{m.group(1)}-D{m.group(2)}"))
    ids = sorted({ident for *_, ident in seen}, key=lambda s: (int(s[1:].split("-")[0]), int(s.split("-D")[1])))
    return ids, best[1]


def ledger_rows(reader: Reader) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in reader.get(LEDGER).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            rows[row["id"]] = row
    return rows


def check_trivial(cmd: str) -> bool:
    """A check must name a committed path and a literal; `true`/`:` proves nothing (R76 skip)."""
    return not (PATHISH.search(cmd) and QUOTED.search(cmd))


# ---------------------------------------------------------------- derivations
def visible(text: str) -> str:
    return FENCE.sub("", COMMENT.sub("", text))


def index_rows(readme: str) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for line in readme.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in CELLSPLIT.split(line.strip())[1:-1]]
        if len(cells) < 2 or not all(cells):
            continue
        m = FIRST_CELL.fullmatch(cells[0])
        if m:
            out.setdefault(m.group(1), set()).add(m.group(2))
    return out


def derive_index_split(probe: Path) -> tuple[int, str, str]:
    """Final-rule missing counts at BASE75 (rendered README rows + git ls-tree). Native, no r75 run."""
    readme = visible(git(probe, "show", f"{BASE75}:corpus/README.md").stdout)
    rows = index_rows(readme)
    tree = git(probe, "ls-tree", "-r", "--name-only", BASE75, "corpus").stdout.splitlines()
    missing: list[int] = []
    for kind, prefix in (("knowledge", "corpus/knowledge/"), ("lessons", "corpus/lessons/")):
        files = sorted({p.rsplit("/", 1)[1] for p in tree if p.startswith(prefix) and p.endswith(".md") and p.count("/") == 2})
        miss = [f for f in files if f not in rows.get(kind, set())]
        missing.append(len(miss))
    dirs = sorted({p.split("/")[2] for p in tree if p.startswith("corpus/evidence/") and p.count("/") >= 3})
    mentioned = set(EVIDENCE.findall(readme))
    missing.append(len([d for d in dirs if d not in mentioned]))
    return sum(missing), "/".join(str(x) for x in missing), f"{missing[0]}/{missing[1]}/{missing[2]}"


def derive_selftest_counts(probe: Path, work: Path) -> tuple[str, str, str]:
    """The counts the two round-75 gates actually print (D4/D5 re-derive them at check time)."""
    c1, c2 = "", ""
    proc = subprocess.run(
        [sys.executable, str(probe / "plans/round75_c1_index_parity.py"), "--selftest", "--work", str(work / "d4c1")],
        capture_output=True, text=True, cwd=str(probe),
    )
    m = re.search(r"^SELFTEST cases=(\d+) red=(\d+) failures=\d+ ok=\w+$", proc.stdout, re.M)
    if m:
        c1 = f"cases={m.group(1)} red={m.group(2)}"
    proc = subprocess.run(
        [sys.executable, str(probe / "plans/round75_c2_registry_audit.py"), "--selftest", "--work", str(work / "d4c2")],
        capture_output=True, text=True, cwd=str(probe),
    )
    m = re.search(r"^SELFTEST arms=(\d+) failures=\d+ ok=\w+$", proc.stdout, re.M)
    if m:
        c2 = f"arms={m.group(1)}"
    return c1, c2, ""


def block_after(text: str, token: str, span: int = 6) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if token in line:
            return "\n".join(lines[i : i + span])
    return ""


def c1_after_stamp(reader: Reader) -> str:
    m = re.search(r"^LANE_TIP (\S+)", reader.get(C1_AFTER), re.M)
    return m.group(1) if m else ""


# ---------------------------------------------------------------- legs
def derivations(probe: Path, work: Path, rev_mode: bool) -> dict[str, str]:
    """Values every value-bearing leg re-derives, or blanks in rev mode (legs then print PENDING)."""
    total, split, split_text = derive_index_split(probe)
    c1c, c2c = ("", "")
    if not rev_mode:
        c1c, c2c, _ = derive_selftest_counts(probe, work)
    return {"total": str(total), "split": split, "split_text": split_text, "c1c": c1c, "c2c": c2c}


def legs(reader: Reader, deriv: dict[str, str], rev_mode: bool) -> tuple[list[str], list[str]]:
    """(report lines, defect lines). Execution-dependent legs print PENDING before data."""
    report: list[str] = []
    defects: list[str] = []

    def leg(name: str, ok: bool | None, detail: str) -> None:
        state = "PENDING" if ok is None else ("ok" if ok else "FAIL")
        report.append(f"LEG {name} {state} {detail}".rstrip())
        if ok is False:
            defects.append(f"LEG-FAIL {name} {detail}")

    stamp = c1_after_stamp(reader)

    # D1 — QUALITY criterion grounded in the lesson
    d1 = block_after(visible(reader.get(QUALITY)), "R75-D1", span=4)
    leg("D1", bool(d1) and "round-75-verifier-spotcheck" in d1, "QUALITY criterion cites R75-D1 + lesson")

    # D2 — SCORECARD correction naming the real stamp and the report tip
    d2 = "\n".join(l for l in visible(reader.get(SCORECARD)).splitlines() if "R75-D2" in l)
    leg("D2", bool(d2) and bool(stamp) and stamp in d2 and "5d9a0ccc" in d2,
        f"SCORECARD line with R75-D2, stamp {stamp[:12]}, 5d9a0ccc")

    # D3 — SCORECARD correction naming the native final-rule before counts
    d3 = "\n".join(l for l in visible(reader.get(SCORECARD)).splitlines() if "R75-D3" in l)
    leg("D3", bool(d3) and deriv["total"] in d3 and deriv["split"] in d3,
        f"SCORECARD line with R75-D3, total {deriv['total']}, split {deriv['split']} at {BASE75}")

    # D4 — registry rows carry the printed selftest counts
    row75 = "\n".join(l for l in visible(reader.get(SKILL)).splitlines()
                       if "round75-c1-index-parity" in l or "round75-c2-registry-audit" in l)
    if rev_mode or not deriv["c1c"]:
        leg("D4", None, "needs the two round-75 selftests (rev mode)")
    else:
        leg("D4", deriv["c1c"] in row75 and deriv["c2c"] in row75,
            f"registry rows carry {deriv['c1c']} / {deriv['c2c']}")

    # D5 — LOG correction block within six lines of the id
    d5 = block_after(visible(reader.get(LOG)), "R75-D5", span=6)
    if rev_mode or not deriv["c1c"]:
        leg("D5", None, "needs the selftest counts (rev mode)")
    else:
        leg("D5", bool(d5) and deriv["c1c"] in d5 and stamp in d5,
            f"LOG block with R75-D5, {deriv['c1c']}, stamp {stamp[:12]}")

    # D6 — the two round-74 gate receipts at the tip
    ok6 = True
    detail6 = []
    for rel, pred in ((R74C1, "PREDICATE R74-C1 pass"), (R74C2, "PREDICATE R74-C2 pass")):
        text = reader.get(rel)
        m = re.search(r"^LANE_TIP (\S+)", text, re.M)
        hit = pred in text
        state = "no-stamp"
        if m:
            state, _ = reader.ancestry(m.group(1))
        ok6 = ok6 and hit and state == "ancestor"
        detail6.append(f"{rel.rsplit('/', 1)[1]}={'pass' if hit else 'missing'}/{state}")
    leg("D6", ok6, " ".join(detail6))

    # D7 — appended correction on the round-74 lesson
    d7 = visible(reader.get(ROUND74_LESSON))
    leg("D7", "R75-D7" in d7 and "## Correction" in d7, "round-74 lesson appended correction naming R75-D7")
    return report, defects


# ---------------------------------------------------------------- ledger
def ledger_report(reader: Reader, ids: list[str]) -> tuple[list[str], list[str]]:
    report: list[str] = []
    defects: list[str] = []
    rows = ledger_rows(reader)
    for ident in ids:
        row = rows.get(ident)
        if row is None:
            report.append(f"LEDGER {ident} MISSING-ROW")
            defects.append(f"DEFECT MISSING-ROW {ident}")
            continue
        problems: list[str] = []
        if row.get("status") != "closed":
            problems.append(f"OPEN status={row.get('status')}")
        if not ISO.search(str(row.get("verified_at", ""))):
            problems.append("NO-VERIFIED-AT")
        sha = str(row.get("close_commit", ""))
        if not SHA40.search(sha):
            problems.append("NO-CLOSE-COMMIT")
        else:
            state, _ = reader.ancestry(SHA40.search(sha).group(0))
            if state == "not-ancestor":
                problems.append("CLOSE-NOT-ANCESTOR")
            elif state != "ancestor":
                problems.append("CLOSE-UNRESOLVED")
        if check_trivial(str(row.get("check", ""))):
            problems.append("CHECK-TRIVIAL")
        if NEGATION.search(str(row.get("close", ""))):
            problems.append("NEGATED-DISCHARGE")
        # Evidence binding (seat ConnectorR76): an ancestor close_commit is not enough — the named
        # evidence must exist *in that commit's tree* and carry the literal the discharge cites.
        ev_path = str(row.get("evidence_path", ""))
        ev_lit = str(row.get("evidence_literal", ""))
        if not ev_path or not ev_lit:
            problems.append("NO-EVIDENCE-FIELD")
        elif SHA40.search(sha):
            full = SHA40.search(sha).group(0)
            blob = reader.at_rev(full, ev_path)
            if not blob:
                problems.append("EVIDENCE-ABSENT-AT-CLOSE")
            elif ev_lit not in blob:
                problems.append("EVIDENCE-LITERAL-MISSING")
            else:
                hit_lines = [l for l in blob.splitlines() if ident in l or ev_lit in l]
                if any(NEGATION.search(l) for l in hit_lines):
                    problems.append("NEGATED-DISCHARGE")
        if problems:
            report.append(f"LEDGER {ident} DEFECT {' '.join(problems)}")
            defects += [f"DEFECT {p} {ident}" for p in problems]
        else:
            report.append(f"LEDGER {ident} ok closed close_commit={sha[:12]}")
    return report, defects


# ---------------------------------------------------------------- emit
def emit(lane: Path, rev: str, out: Path | None, probe: Path | None = None,
         work: Path | None = None) -> int:
    if not lane.is_dir():
        print(f"SETUP ERROR: lane {lane} is not a directory", file=sys.stderr)
        return 2
    probe = probe or lane
    reader = Reader(lane, rev, probe)
    if not reader.get(LEDGER).strip() and not (lane / LEDGER).exists():
        print(f"SETUP ERROR: {LEDGER} absent", file=sys.stderr)
        return 2
    work = work or Path("/fast/scratch/hyaku/kengaku-r76/c2")
    work.mkdir(parents=True, exist_ok=True)
    rev_mode = rev not in ("worktree", "", None)
    ids, closure = scope_ids(reader)
    report = [f"SCOPE-SOURCE {closure}"]
    leg_lines, leg_defects = legs(reader, derivations(probe, work, rev_mode), rev_mode)
    ledger_lines, ledger_defects = ledger_report(reader, ids)
    defects = leg_defects + ledger_defects
    rows = ledger_rows(reader)
    registered = sum(1 for i in ids if i in rows)
    closed = sum(1 for i in ids if rows.get(i, {}).get("status") == "closed")
    discharged = sum(1 for i in ids if f"LEDGER {i} ok" in "\n".join(ledger_lines))
    legs_passed = sum(1 for l in leg_lines if l.split()[2] == "ok")
    legs_pending = sum(1 for l in leg_lines if l.split()[2] == "PENDING")
    if not ids:
        defects.append("DEFECT EMPTY-SCOPE ids=0 (the newest closer names no routed id, or no closer exists)")
    if legs_pending:
        defects.append(f"DEFECT LEG-PENDING n={legs_pending} (execution-dependent legs cannot pass by default)")
    report += leg_lines + ledger_lines
    report.append(
        f"SCOPE ids={len(ids)} registered={registered} closed={closed} open={len(ids) - closed} "
        f"discharged={discharged} legs_passed={legs_passed} legs_pending={legs_pending} wrong={len(defects)}"
    )
    if discharged != len(ids) and not defects:
        defects.append(f"TALLY-MISMATCH discharged={discharged} ids={len(ids)}")
    lines = report + defects
    lines.append(f"PREDICATE R76-C2 {'pass' if not defects else 'fail'}")
    tip, dirty = reader.tip, worktree_dirty(lane)
    text = "\n".join([f"LANE_TIP {tip}", f"WORKTREE {'dirty' if dirty else 'clean'}"] + lines) + "\n"
    print("\n".join(lines) + "\n", end="")
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    return 0 if not defects else 1


# ---------------------------------------------------------------- fixtures
def build_fixture(root: Path, lane_tip: str, *, drop_row: str = "", open_row: str = "",
                  no_commit: str = "", bad_commit: str = "", trivial: str = "",
                  drop_r74: bool = False, drop_d7: bool = False, prose_only: bool = False,
                  drop_d2_stamp: bool = False, bad_evidence: bool = False,
                  negate_d3: bool = False, empty_scope: bool = False,
                  comment_leg: bool = False) -> None:
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus/lessons").mkdir(parents=True)
    (root / "corpus/evidence/round75").mkdir(parents=True)
    (root / "corpus/evidence/round76").mkdir(parents=True)
    ids = [f"R75-D{n}" for n in range(1, 8)]
    (root / "corpus/lessons/round-75-verifier-spotcheck.md").write_text(
        "# fixture closure\n\n## 6. Routed defects\n\n"
        + ("" if empty_scope else "\n".join(f"- **{i}** routed." for i in ids)) + "\n"
    )
    (root / "corpus/evidence/round75/c1-after.txt").write_text(
        f"LANE_TIP {lane_tip}\nWORKTREE clean\nPREDICATE R75-C1 pass\n"
    )
    rows = []
    for i in ids:
        row = {
            "id": i, "status": "closed", "verified_at": "2026-11-04",
            "close_commit": lane_tip, "close": f"dated correction naming {i}",
            "check": f"grep -q '{i}' SCORECARD.md",
            "evidence_path": {
                "R75-D1": QUALITY, "R75-D2": SCORECARD, "R75-D3": SCORECARD, "R75-D4": SKILL,
                "R75-D5": LOG, "R75-D6": R74C1, "R75-D7": ROUND74_LESSON,
            }[i],
            "evidence_literal": {
                "R75-D1": "R75-D1", "R75-D2": "5d9a0ccc", "R75-D3": "R75-D3", "R75-D4": "round75-c1-index-parity",
                "R75-D5": "R75-D5", "R75-D6": "PREDICATE R74-C1 pass", "R75-D7": "R75-D7",
            }[i],
        }
        if i == drop_row:
            continue
        if i == open_row:
            row["status"] = "open"
        if i == no_commit:
            row["close_commit"] = ""
        if i == bad_commit:
            row["close_commit"] = "0" * 40
        if i == trivial:
            row["check"] = "true"
        if bad_evidence and i == "R75-D6":
            row["evidence_path"] = "corpus/evidence/round76/not-there.txt"
        rows.append(json.dumps(row))
    (root / LEDGER).write_text("\n".join([] if prose_only else rows) + "\n")
    (root / QUALITY).write_text(
        "| Q99 | fixture | corpus/lessons/round-75-verifier-spotcheck.md |\n"
        "| Q98 | fixture criterion | R75-D1 grounded in corpus/lessons/round-75-verifier-spotcheck.md |\n"
    )
    d2 = f"- R75-D2 correction: stamp {lane_tip} and report tip 5d9a0ccc." if not drop_d2_stamp else "- R75-D2 correction: no values."
    if comment_leg:
        d2 = "<!-- " + d2 + " -->"
    (root / SCORECARD).write_text(
        "\n".join([
            d2,
            ("- R75-D3 NOT discharged; defect remains OPEN; quoted values: the final-rule before is 60 (4/36/20)."
             if negate_d3 else "- R75-D3 correction: the final-rule before is 60 (4/36/20)."),
            "- R75-D4 fixture line.",
        ]) + "\n"
    )
    (root / LOG).write_text(
        "## Round 76\n\n- **R75-D5** correction: the C1 selftest prints cases=8 red=7 and the stamp is "
        f"{lane_tip}; the earlier line said cases=7 red=6.\n"
    )
    (root / SKILL).write_text(
        "| `round75-c1-index-parity` | gate | `--selftest` (cases=8 red=7) |\n"
        "| `round75-c2-registry-audit` | gate | `--selftest` (arms=5) |\n"
    )
    if not drop_r74:
        (root / R74C1).write_text(f"LANE_TIP {lane_tip}\nPREDICATE R74-C1 pass\n")
        (root / R74C2).write_text(f"LANE_TIP {lane_tip}\nPREDICATE R74-C2 pass\n")
    (root / ROUND74_LESSON).write_text(
        "# Round 74\n\nbody\n" + ("" if drop_d7 else "\n## Correction (round 76)\n\nR75-D7: appended, not reflowed.\n")
    )


def fixture_legs(root: Path) -> tuple[list[str], list[str]]:
    """Legs over a fixture; derived values come from the real lane (the fixture text pins them)."""
    lane = Path(__file__).resolve().parent.parent
    reader = Reader(root, "worktree", probe=lane)
    work = Path("/fast/scratch/hyaku/kengaku-r76/c2/_fixture")
    work.mkdir(parents=True, exist_ok=True)
    return legs(reader, derivations(lane, work, rev_mode=False), rev_mode=False)


def selftest(work: Path, lane_tip: str) -> int:
    cases = [
        ("clean", {}, 0),
        ("missing-row", {"drop_row": "R75-D4"}, 1),
        ("open-row", {"open_row": "R75-D2"}, 1),
        ("no-close-commit", {"no_commit": "R75-D1"}, 1),
        ("unresolved-commit", {"bad_commit": "R75-D3"}, 1),
        ("trivial-check", {"trivial": "R75-D5"}, 1),
        ("missing-r74-receipt", {"drop_r74": True}, 1),
        ("missing-d7", {"drop_d7": True}, 1),
        ("evidence-absent-at-close", {"bad_evidence": True}, 1),
        ("negated-discharge", {"negate_d3": True}, 1),
        ("empty-scope", {"empty_scope": True}, 1),
        ("comment-leg", {"comment_leg": True}, 1),
        ("prose-only", {"prose_only": True}, 1),
        ("wrong-stamp", {"drop_d2_stamp": True}, 1),
    ]
    fails = 0
    for name, kwargs, want_rc in cases:
        d = work / f"c2_{name}"
        build_fixture(d, lane_tip, **kwargs)
        ids, _ = scope_ids(Reader(d, "worktree", probe=d))
        leg_lines, leg_defects = fixture_legs(d)
        ledger_lines, ledger_defects = ledger_report(Reader(d, "worktree", probe=lane_tip_probe(lane_tip)), ids)
        defects = leg_defects + ledger_defects
        if not ids:
            defects.append("DEFECT EMPTY-SCOPE ids=0")
        rc = 0 if not defects else 1
        ok = rc == want_rc
        fails += 0 if ok else 1
        print(f"SELFTEST {'ok' if ok else 'FAIL'} {name} rc={rc} want={want_rc} defects={len(defects)}")
        shutil.rmtree(d, ignore_errors=True)
    print(f"SELFTEST cases={len(cases)} red={len(cases) - 1} failures={fails} ok={fails == 0}")
    return 0 if fails == 0 else 1


def lane_tip_probe(lane_tip: str) -> Path:
    return Path(__file__).resolve().parent.parent  # the lane repo whose history resolves commits


def mutants(work: Path, lane_tip: str) -> int:
    matrix = [
        ("M1-drop-row", {"drop_row": "R75-D4"}, "MISSING-ROW"),
        ("M2-open", {"open_row": "R75-D2"}, "OPEN"),
        ("M3-no-close-commit", {"no_commit": "R75-D1"}, "NO-CLOSE-COMMIT"),
        ("M4-unresolved", {"bad_commit": "R75-D3"}, "CLOSE-UNRESOLVED"),
        ("M5-trivial-check", {"trivial": "R75-D5"}, "CHECK-TRIVIAL"),
        ("M6-missing-receipt", {"drop_r74": True}, "LEG-FAIL D6"),
        ("M7-missing-d7", {"drop_d7": True}, "LEG-FAIL D7"),
        ("M8-wrong-stamp", {"drop_d2_stamp": True}, "LEG-FAIL D2"),
        ("M9-evidence-absent", {"bad_evidence": True}, "EVIDENCE-ABSENT-AT-CLOSE"),
        ("M10-negated-discharge", {"negate_d3": True}, "NEGATED-DISCHARGE"),
        ("M11-empty-scope", {"empty_scope": True}, "EMPTY-SCOPE"),
        ("M12-comment-leg", {"comment_leg": True}, "LEG-FAIL D2"),
    ]
    total = killed = matched = wrong = survived = 0
    for name, kwargs, expected in matrix:
        total += 1
        d = work / f"c2m_{name}"
        build_fixture(d, lane_tip, **kwargs)
        ids, _ = scope_ids(Reader(d, "worktree", probe=d))
        leg_lines, leg_defects = fixture_legs(d)
        ledger_lines, ledger_defects = ledger_report(Reader(d, "worktree", probe=lane_tip_probe(lane_tip)), ids)
        defects = leg_defects + ledger_defects
        if not ids:
            defects.append("DEFECT EMPTY-SCOPE ids=0")
        printed = "\n".join(leg_lines + ledger_lines + defects)
        if defects:
            killed += 1
            if expected in printed:
                matched += 1
            else:
                wrong += 1
        else:
            survived += 1
        print(f"MUTANT {name} killed={bool(defects)} expected={expected} matched={expected in printed}")
        shutil.rmtree(d, ignore_errors=True)
    print(f"MUTANTS total={total} killed={killed} expected_matched={matched} wrong_id={wrong} survived={survived}")
    return 0 if killed == total and matched == total else 1


def control_status(work: Path, lane_tip: str) -> int:
    """The cheapest skip: register every id as closed with a trivial check and no discharge.

    A burn-down that counts `status: closed` rows scores this as done. This gate must still report
    the ledger defects and the failed legs, so the skip cannot reach the target.
    """
    root = work / "c2_control_status"
    build_fixture(root, lane_tip, trivial="R75-D1", drop_r74=True, drop_d7=True, drop_d2_stamp=True)
    ids, _ = scope_ids(Reader(root, "worktree", probe=root))
    leg_lines, leg_defects = fixture_legs(root)
    # The control's own question: how many rows *claim* closed, and how many checks truly pass?
    rows = ledger_rows(Reader(root, "worktree", probe=root))
    claimed = sum(1 for i in ids if rows.get(i, {}).get("status") == "closed")
    trivial = sum(1 for i in ids if rows.get(i) and check_trivial(str(rows[i].get("check", ""))))
    failed_legs = sum(1 for l in leg_lines if l.split()[2] == "FAIL")
    print(f"CONTROL rows_claimed_closed={claimed} trivial_checks={trivial} failed_legs={failed_legs}")
    print("\n".join(leg_lines))
    ok = claimed == len(ids) and (failed_legs > 0 or trivial > 0)
    print(f"PREDICATE R76-C2-control {'pass' if ok else 'fail'}")
    shutil.rmtree(root, ignore_errors=True)
    return 0 if ok else 1


def selftest_git(work: Path) -> int:
    """S252's three exit states against a scratch repo (explicit -C on every call)."""
    d = work / "c2_git"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid"]
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if Path(top).resolve() != d.resolve():
        print(f"SELFTEST-GIT FAIL toplevel={top} want={d}")
        return 1
    (d / "f").write_text("1\n")
    git(d, "add", "f")
    git(d, *ident, "commit", "-qm", "one")
    first = git(d, "rev-parse", "HEAD").stdout.strip()
    (d / "f").write_text("2\n")
    git(d, *ident, "commit", "-qam", "two")
    tip = git(d, "rev-parse", "HEAD").stdout.strip()
    git(d, "checkout", "-q", "-b", "side", first)
    (d / "g").write_text("x\n")
    git(d, "add", "g")
    git(d, *ident, "commit", "-qm", "side")
    side = git(d, "rev-parse", "HEAD").stdout.strip()
    reader = Reader(d, tip, probe=d)
    cases = (
        ("ancestor", reader.ancestry(first)[0], "ancestor"),
        ("not-ancestor", reader.ancestry(side)[0], "not-ancestor"),
        ("unresolved", reader.ancestry("0" * 40)[0], "unresolved"),
    )
    fails = 0
    for name, got, want in cases:
        ok = got == want
        fails += 0 if ok else 1
        print(f"SELFTEST-GIT {'ok' if ok else 'FAIL'} {name} got={got} want={want}")
    shutil.rmtree(d, ignore_errors=True)
    print(f"SELFTEST-GIT cases={len(cases)} failures={fails} ok={fails == 0}")
    return 0 if fails == 0 else 1


class _Tee:
    """stdout passthrough that also keeps the bytes for the receipt."""

    def __init__(self, *streams: object) -> None:
        self.streams = streams

    def write(self, data: str) -> int:
        for stream in self.streams:
            stream.write(data)  # type: ignore[attr-defined]
        return len(data)

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()  # type: ignore[attr-defined]


def run_battery(args: argparse.Namespace, probe: Path, fn) -> int:
    buf = io.StringIO()
    with contextlib.redirect_stdout(_Tee(sys.stdout, buf)):
        rc = fn()
    if args.receipt is not None:
        tip = git(probe, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip() or "unknown"
        dirty = "dirty" if worktree_dirty(args.lane) else "clean"
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(f"LANE_TIP {tip}\nWORKTREE {dirty}\n" + buf.getvalue())
    return rc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lane", type=Path, default=Path("."), help="Lane root directory")
    parser.add_argument("--rev", default="worktree", help="Read declared bytes at this revision")
    parser.add_argument("--probe", type=Path, default=None, help="Repo whose history resolves close_commit")
    parser.add_argument("--receipt", type=Path, default=None, help="Write the verdict bytes here")
    parser.add_argument("--selftest", action="store_true", help="Run the fixture battery")
    parser.add_argument("--selftest-git", action="store_true", help="Run the three-exit-state git arms")
    parser.add_argument("--mutants", action="store_true", help="Run the attributed mutant matrix")
    parser.add_argument("--control-status", action="store_true", help="Run the status-only skip control")
    parser.add_argument("--work", type=Path, default=Path("/fast/scratch/hyaku/kengaku-r76/c2"), help="Scratch dir")
    args = parser.parse_args()
    probe = args.probe or (args.lane if (args.lane / ".git").exists() else Path(__file__).resolve().parent.parent)
    tip = git(probe, "rev-parse", "--verify", "--quiet", "master^{commit}").stdout.strip() or git(
        probe, "rev-parse", "--verify", "--quiet", "HEAD^{commit}").stdout.strip()

    if args.selftest:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, probe, lambda: selftest(args.work, tip))
    if args.selftest_git:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, probe, lambda: selftest_git(args.work))
    if args.mutants:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, probe, lambda: mutants(args.work, tip))
    if args.control_status:
        args.work.mkdir(parents=True, exist_ok=True)
        return run_battery(args, probe, lambda: control_status(args.work, tip))
    return emit(args.lane, args.rev, args.receipt, probe=probe, work=args.work)


if __name__ == "__main__":
    sys.exit(main())
