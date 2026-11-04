#!/usr/bin/env python3
"""R84-C2 admission-bar counter for corpus/knowledge/tb2-code-from-image-offline.md.

Measured subject (one entry, one lesson):
  entry   corpus/knowledge/tb2-code-from-image-offline.md
  lesson  corpus/lessons/round-84.md          (Gate section is the successor admission)

Reads the entry (and the lesson) at the measured revision: `git show REV:path`
when --rev is present, the lane working tree when it is absent. Q13 is always
evaluated at a commit, because a Gate admission only exists once committed.

Rules as implemented (each is a line-level predicate on the entry bytes):

Q1  header contract. The first three lines must start, at column 0, with
    "source:", "verified-at:" and "recheck:" in that order. The recheck body
    (line 3 after "recheck:") must carry BOTH
      (a) a marker: an ISO YYYY-MM-DD date that is a real calendar date, or a
          cadence token (see CADENCE_RE: daily/weekly/bi-weekly/fortnightly/
          monthly/quarterly/semi-annual/annual/yearly/per-release/every <n> d|day|
          days|w|week|weeks|mo|month|months|h|hour|hours), and
      (b) a named re-check action: a command token (COMMAND_RE: python3, bash,
          npx, uv, make, git, jq, rg, go, cargo, npm, node, perl, ruby, curl,
          wget, bwrap, bubblewrap, or a plans/… .py / scripts/… .sh path), or the
          words re-verify/re-run (REVERB_RE) followed by a concrete action token
          (ACTION_TARGET_RE: a backticked span, a path-like token, a file with a
          .py/.sh/.json/.md/.txt/.yaml extension, or a command name).
    q1=1 if any component is missing; detail names the failures.

Q21 pin continuity. Every 40-hex token on the source line (PIN40_RE, with
    non-hex boundaries so a 64-hex digest cannot donate a 40-hex prefix) must be
    answered on the recheck line by either the same 40-hex value, or the words
    pin/re-pin (PIN_VERB_RE) together with a cadence token (CADENCE_RE, an ISO
    date is not a cadence here). q21=1 otherwise; q21=0 when the source line
    carries no 40-hex token (the rule is vacuous, not silently passed).

Q13 successor admission. `plans/gate_timing_check.py --lesson
    corpus/lessons/round-84.md --commit REV` must exit 0 in a scratch clone of
    the measured revision, using the checker bytes at REV. Exit 0 is q13=0.
    Any other exit, or an absent lesson, is q13=1. The checker itself requires a
    line-start "writer:" field on the candidate; that requirement is folded into
    q13 (the INFO line only observes it) so the frozen defect count stays three.

Counting: defects = q1 + q21 + q13 over entries=1. Exit 0 pass, 1 fail,
2 could-not-evaluate (entry absent at the revision, unreadable revision, or the
gate repository cannot be materialised). Could-not-evaluate prints one
COULD-NOT-EVALUATE line and no TARGET/PREDICATE line.

Modes (selftest/control/mutant write only under --work):
  --selftest          fixture battery (a) BASE bytes, (b) date-only recheck,
                      (c) pin+date but no cited Gate report, (d) green gate,
                      (e) q1-only isolation; then one mutant per rule.
  --mutant q1|q21|q13 relax that rule to always-true and require the fixture
                      that sets its defect to change verdict (killed).
  --control-filler    BASE bytes, no repair: must stay defects=3.
  --control-date-only BASE bytes with only the recheck date added: must keep
                      q21=1 and q13=1.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

LANE_DEFAULT = Path.cwd()
ENTRY = "corpus/knowledge/tb2-code-from-image-offline.md"
LESSON = "corpus/lessons/round-84.md"
BASE = "4087b2f8369fb0c317a8460725a607681ff2fd7f"
GATE_SCRIPT = "plans/gate_timing_check.py"
FIXTURE_COMMITTER = ("R84 C2 Fixture", "r84-c2-fixture@example.invalid")

ISO_DATE_RE = re.compile(r"(?<![0-9])(\d{4})-(\d{2})-(\d{2})(?![0-9])")
CADENCE_RE = re.compile(
    r"(?<![\w-])(?:daily|weekly|bi-?weekly|fortnightly|monthly|quarterly|"
    r"semi-?annual(?:ly)?|annual(?:ly)?|yearly|per[- ]release|"
    r"every\s+\d+\s*(?:days?|d|weeks?|w|months?|mo|hours?|h))(?![\w-])",
    re.IGNORECASE,
)
PIN40_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
PIN_VERB_RE = re.compile(r"(?<![\w-])(?:re-?pin(?:ned|ning)?|pin(?:ned|ning)?)(?![\w-])",
                         re.IGNORECASE)
COMMAND_RE = re.compile(
    r"(?<![\w./-])(?:python3?|bash|sh|zsh|npx|uv|make|git|jq|rg|go|cargo|npm|"
    r"node|perl|ruby|curl|wget|bwrap|bubblewrap)(?![\w-])"
    r"|(?<![\w./-])(?:plans|scripts)/[A-Za-z0-9_.-]+\.(?:py|sh)(?![\w-])"
)
REVERB_RE = re.compile(r"(?<![\w-])(?:re-?verify|re-?run)(?![\w-])", re.IGNORECASE)
ACTION_TARGET_RE = re.compile(
    r"(?:`[^`\n]+`|\S*/\S*|\S+\.(?:py|sh|json|md|txt|ya?ml)(?![\w-])"
    r"|\b(?:python3?|bash|sh|npx|uv|make|git)\b)"
)
WRITER_LINE_RE = re.compile(r"^writer:\s*\S", re.MULTILINE)

CHECK_LINE = "CHECK {name} {verdict} {detail}"


class CouldNotEvaluate(RuntimeError):
    """The measured bytes or revision do not exist, so nothing can be scored."""


@dataclass(frozen=True)
class Verdict:
    q1: int
    detail1: str
    q21: int
    detail21: str
    q13: int
    detail13: str
    writer: bool

    @property
    def defects(self) -> int:
        return self.q1 + self.q21 + self.q13


def safe_env() -> dict[str, str]:
    """Environment for git/python children: no repo selectors, no bytecode writes."""
    keep = ("PATH", "TMPDIR", "TEMP", "TMP", "LANG", "LC_ALL")
    env = {name: os.environ[name] for name in keep if name in os.environ}
    env.setdefault("PATH", os.defpath)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    return env


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True,
                          text=True, encoding="utf-8", errors="replace", check=False,
                          env=safe_env())


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return run(["git", "-C", str(repo), *args])


def is_real_iso_date(text: str) -> bool:
    for match in ISO_DATE_RE.finditer(text):
        try:
            date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            continue
        return True
    return False


def has_cadence(text: str) -> bool:
    return bool(CADENCE_RE.search(text))


def check_q1(entry: str) -> tuple[int, str]:
    lines = entry.splitlines()
    failures: list[str] = []
    if len(lines) < 3:
        failures.append(f"header-lines={len(lines)}")
    prefixes = ("source:", "verified-at:", "recheck:")
    for index, prefix in enumerate(prefixes):
        if index < len(lines) and not lines[index].startswith(prefix):
            failures.append(f"line{index + 1}-not-{prefix[:-1]}")
    recheck = lines[2][len("recheck:"):] if len(lines) > 2 and lines[2].startswith("recheck:") else None
    if recheck is None:
        failures.append("no-recheck-line")
    else:
        if not (is_real_iso_date(recheck) or has_cadence(recheck)):
            failures.append("recheck-no-date-or-cadence")
        verb = REVERB_RE.search(recheck)
        action = bool(COMMAND_RE.search(recheck)) or bool(
            verb and ACTION_TARGET_RE.search(recheck[verb.end():]))
        if not action:
            failures.append("recheck-no-action")
    return (1 if failures else 0), (";".join(failures) if failures else "ok")


def check_q21(entry: str) -> tuple[int, str]:
    lines = entry.splitlines()
    source = lines[0] if lines else ""
    pins: list[str] = []
    for match in PIN40_RE.finditer(source):
        if match.group(0) not in pins:
            pins.append(match.group(0))
    if not pins:
        return 0, "pin-absent"
    recheck = lines[2][len("recheck:"):] if len(lines) > 2 and lines[2].startswith("recheck:") else None
    if recheck is None:
        return 1, f"pins={len(pins)} no-recheck-line"
    repin_cadence = bool(PIN_VERB_RE.search(recheck)) and has_cadence(recheck)
    uncovered = [pin for pin in pins if pin not in recheck and not repin_cadence]
    if uncovered:
        return 1, f"pins={len(pins)} uncovered={','.join(uncovered)}"
    return 0, "pin-covered"


def revision_text(repo: Path, rev: str, path: str) -> str | None:
    result = git(repo, "show", f"{rev}:{path}")
    return result.stdout if result.returncode == 0 else None


def resolve_commit(repo: Path, rev: str) -> str:
    result = git(repo, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if result.returncode or not result.stdout.strip():
        raise CouldNotEvaluate(f"git revision {rev!r} is not readable in {repo}")
    return result.stdout.strip()


def ensure_clone(source: Path, dest: Path) -> Path:
    """Materialise a shared, checkout-free clone of `source` (objects via alternates)."""
    if (dest / ".git").exists():
        return dest
    if dest.exists():
        shutil.rmtree(dest)
    result = run(["git", "clone", "--shared", "--no-checkout", "--quiet",
                  str(source), str(dest)])
    if result.returncode:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise CouldNotEvaluate(
            f"cannot clone {source}: {detail[0] if detail else result.returncode}")
    return dest


def gate_script_at(clone: Path, commit: str, work: Path, path: str = GATE_SCRIPT) -> Path | None:
    text = revision_text(clone, commit, path)
    if text is None:
        return None
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    target = work / f"gate_timing_check.{commit[:12]}.{digest}.py"
    if not target.exists():
        target.write_text(text, encoding="utf-8")
    return target


def gate_reason(stdout: str, stderr: str) -> str:
    for line in stdout.splitlines():
        if line.startswith("  reasons: "):
            detail = line[len("  reasons: "):]
            break
    else:
        detail = ""
        for stream in (stderr, stdout):
            for line in stream.splitlines():
                if line.strip():
                    detail = line
                    break
            if detail:
                break
    detail = re.sub(r"\s+", " ", detail).strip().rstrip(".")
    return detail[:200] or "no-detail"


def check_q13(clone: Path | None, commit: str | None, lesson: str | None,
              work: Path) -> tuple[int, str]:
    if clone is None or commit is None:
        return 1, "lesson-absent"
    if lesson is None:
        return 1, "lesson-absent"
    script = gate_script_at(clone, commit, work)
    if script is None:
        return 1, "gate-script-absent"
    result = run([sys.executable, str(script), "--lesson", LESSON, "--commit", commit,
                  "--repo", str(clone)], cwd=work)
    if result.returncode == 0:
        return 0, "exit=0"
    return 1, f"exit={result.returncode} reason={gate_reason(result.stdout, result.stderr)}"


def evaluate(entry: str, lesson: str | None, clone: Path | None, commit: str | None,
             work: Path, mutant: str | None = None) -> Verdict:
    q1, detail1 = check_q1(entry)
    q21, detail21 = check_q21(entry)
    q13, detail13 = check_q13(clone, commit, lesson, work)
    if mutant == "q1":
        q1, detail1 = 0, "mutant-always-true"
    elif mutant == "q21":
        q21, detail21 = 0, "mutant-always-true"
    elif mutant == "q13":
        q13, detail13 = 0, "mutant-always-true"
    return Verdict(q1, detail1, q21, detail21, q13, detail13,
                   bool(WRITER_LINE_RE.search(entry)))


def emit(verdict: Verdict) -> None:
    print(CHECK_LINE.format(name="q1", verdict="ok" if verdict.q1 == 0 else "DEFECT",
                            detail=verdict.detail1))
    print(CHECK_LINE.format(name="q21", verdict="ok" if verdict.q21 == 0 else "DEFECT",
                            detail=verdict.detail21))
    print(CHECK_LINE.format(name="q13", verdict="ok" if verdict.q13 == 0 else "DEFECT",
                            detail=verdict.detail13))
    print(f"INFO writer={'present' if verdict.writer else 'absent'}")
    print(f"TARGET entries=1 q1={verdict.q1} q21={verdict.q21} q13={verdict.q13} "
          f"defects={verdict.defects}")
    print(f"PREDICATE R84-C2 {'pass' if verdict.defects == 0 else 'fail'}")


def load_measured(lane: Path, rev: str | None) -> tuple[str, str | None, str | None, str | None]:
    """Return (entry, lesson-or-None, clone, resolved-commit) for the measured bytes."""
    if rev is not None:
        commit = resolve_commit(lane, rev)
        entry = revision_text(lane, rev, ENTRY)
        if entry is None:
            raise CouldNotEvaluate(f"{ENTRY} is absent at {rev}")
        lesson = revision_text(lane, rev, LESSON)
        if lesson is None:
            return entry, None, None, None
        return entry, lesson, None, commit
    entry_path = lane / ENTRY
    if not entry_path.is_file():
        raise CouldNotEvaluate(f"{ENTRY} is absent from {lane}")
    entry = entry_path.read_text(encoding="utf-8")
    commit = resolve_commit(lane, "HEAD")
    committed_lesson = revision_text(lane, commit, LESSON)
    worktree_path = lane / LESSON
    worktree_lesson = worktree_path.read_text(encoding="utf-8") if worktree_path.is_file() else None
    if worktree_lesson is None:
        return entry, None, None, None
    if committed_lesson != worktree_lesson:
        # An uncommitted Gate cannot be the admitting tree's admission.
        return entry, None, None, None
    return entry, worktree_lesson, None, commit


def scratch_repo(root: Path, lane: Path) -> Path:
    repo = root / "repo"
    repo.mkdir(parents=True)
    result = git(repo, "init", "-q")
    if result.returncode:
        raise CouldNotEvaluate(f"git init failed: {result.stderr.strip()}")
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    if Path(top).resolve() != repo.resolve():
        raise CouldNotEvaluate(f"fixture top-level {top!r} is not {repo}")
    script = lane / GATE_SCRIPT
    if not script.is_file():
        raise CouldNotEvaluate(f"{script} is absent")
    target = repo / GATE_SCRIPT
    target.parent.mkdir(parents=True)
    shutil.copy2(script, target)
    return repo


def write_files(repo: Path, files: dict[str, str | None]) -> None:
    for rel, text in files.items():
        path = repo / rel
        if text is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def commit_state(repo: Path, message: str) -> str:
    name, email = FIXTURE_COMMITTER
    add = git(repo, "add", "-A")
    if add.returncode:
        raise CouldNotEvaluate(f"fixture git add failed: {add.stderr.strip()}")
    result = git(repo, "-c", f"user.name={name}", "-c", f"user.email={email}",
                 "-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
    if result.returncode:
        raise CouldNotEvaluate(f"fixture commit failed: {result.stderr.strip()}")
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def entry_fixture(base: str, *, source: str | None = None, recheck: str | None = None,
                  writer: str | None = None) -> str:
    lines = base.splitlines()
    out = [source if source is not None else lines[0], lines[1],
           f"recheck: {recheck}" if recheck is not None else lines[2]]
    if writer is not None:
        out.append(f"writer: {writer}")
    out.extend(lines[3:])
    return "\n".join(out) + "\n"


GREEN_REASON = "second-seat re-read at `.ufo/waves/round-84/falsify/FixtureReviewer.md`"
NOCITE_REASON = "repaired header; the qualifying re-read is not cited here"


def lesson_text(reason: str) -> str:
    return (
        "# Round 84 fixture lesson\n\n## Gate\n\n"
        "| candidate | decision | reason |\n|---|---|---|\n"
        f"| `{ENTRY}` | admit | {reason} |\n"
    )


REPORT_TEXT = (
    f"Re-read {ENTRY}\n"
    "writer: FixtureReviewer\n"
    "VERDICT: PASS\n"
)
REGISTRY_TEXT = (
    '{"members": {"FixtureReviewer": {"role": "reviewer", '
    '"agentId": "Round84.FixtureReviewer"}}}\n'
)


@dataclass(frozen=True)
class Fixture:
    ident: str
    expected: tuple[int, int, int]


FIXTURES = (
    Fixture("a-base", (1, 1, 1)),
    Fixture("date-only", (0, 1, 1)),
    Fixture("q21-only", (0, 1, 0)),
    Fixture("q13-only", (0, 0, 1)),
    Fixture("green", (0, 0, 0)),
    Fixture("q1-only", (1, 0, 0)),
)
MUTANT_FIXTURE = {"q1": "q1-only", "q21": "q21-only", "q13": "q13-only"}


def build_fixtures(lane: Path, work: Path) -> tuple[Path, dict[str, str], str]:
    base = revision_text(lane, BASE, ENTRY)
    if base is None:
        raise CouldNotEvaluate(f"BASE {BASE} has no {ENTRY}")
    root = Path(tempfile.mkdtemp(prefix="fixtures-", dir=work))
    repo = scratch_repo(root, lane)
    pins = PIN40_RE.findall(base.splitlines()[0] if base.splitlines() else "")
    pin = pins[0] if pins else "0" * 40
    date_only = entry_fixture(
        base, recheck="python3 plans/round83_c1_replay.py --lane . --work DIR on 2027-01-04")
    q21_entry = entry_fixture(
        base,
        recheck="python3 plans/round83_c1_replay.py --lane . --work DIR weekly (checked 2027-01-04)",
        writer="FixtureWriter")
    repaired = entry_fixture(
        base,
        recheck=f"re-run python3 plans/round84_c2_admission.py --lane . --work DIR weekly; "
                f"pin {pin} (checked 2027-01-04)",
        writer="FixtureWriter")
    q1_entry = entry_fixture(
        base, source="source: S999 — https://example.invalid/fixture.py",
        recheck="python3 plans/round84_c2_admission.py --lane . --work DIR",
        writer="FixtureWriter")
    states = (
        ("a-base", {ENTRY: base}),
        ("date-only", {ENTRY: date_only}),
        ("q21-only", {ENTRY: q21_entry, LESSON: lesson_text(GREEN_REASON),
                      ".ufo/waves/round-84/falsify/FixtureReviewer.md": REPORT_TEXT,
                      ".ufo/waves/round-84/falsify/swarm-registry.json": REGISTRY_TEXT}),
        ("q13-only", {ENTRY: repaired, LESSON: lesson_text(NOCITE_REASON)}),
        ("green", {LESSON: lesson_text(GREEN_REASON)}),
        ("q1-only", {ENTRY: q1_entry}),
    )
    commits: dict[str, str] = {}
    for ident, files in states:
        write_files(repo, files)
        commits[ident] = commit_state(repo, f"fixture {ident}")
    clone = ensure_clone(repo, root / "clone")
    return clone, commits, root


def selftest(lane: Path, work: Path) -> int:
    clone, commits, _root = build_fixtures(lane, work)
    script = lane / GATE_SCRIPT
    print(f"INFO gate-script-sha256={hashlib.sha256(script.read_bytes()).hexdigest()}")
    failures: list[str] = []
    verdicts: dict[str, Verdict] = {}
    for fixture in FIXTURES:
        commit = commits[fixture.ident]
        lesson = revision_text(clone, commit, LESSON)
        entry = revision_text(clone, commit, ENTRY)
        if entry is None:
            print(f"FIXTURE {fixture.ident} MISSING-ENTRY")
            failures.append(fixture.ident)
            continue
        verdict = evaluate(entry, lesson, clone, commit, work)
        verdicts[fixture.ident] = verdict
        observed = (verdict.q1, verdict.q21, verdict.q13)
        ok = observed == fixture.expected
        print(f"FIXTURE {fixture.ident} expect=q1={fixture.expected[0]} "
              f"q21={fixture.expected[1]} q13={fixture.expected[2]} "
              f"defects={sum(fixture.expected)} observed=q1={verdict.q1} "
              f"q21={verdict.q21} q13={verdict.q13} defects={verdict.defects} "
              f"{'OK' if ok else 'MISMATCH'}")
        print(f"  detail q1={verdict.detail1} | q21={verdict.detail21} | q13={verdict.detail13}")
        if not ok:
            failures.append(fixture.ident)
    for rule, ident in MUTANT_FIXTURE.items():
        commit = commits[ident]
        lesson = revision_text(clone, commit, LESSON)
        entry = revision_text(clone, commit, ENTRY)
        if entry is None:
            failures.append(f"mutant-{rule}")
            continue
        mutated = evaluate(entry, lesson, clone, commit, work, mutant=rule)
        base_verdict = verdicts[ident]
        killed = (mutated.q1, mutated.q21, mutated.q13) != \
                 (base_verdict.q1, base_verdict.q21, base_verdict.q13)
        print(f"MUTANT {rule} fixture={ident} baseline_defects={base_verdict.defects} "
              f"mutated_defects={mutated.defects} "
              f"{'KILLED' if killed else 'SURVIVED'}")
        if not killed:
            failures.append(f"mutant-{rule}")
    if failures:
        print(f"SELFTEST FAIL failures={','.join(failures)}")
        return 1
    print("SELFTEST PASS fixtures=%d mutants=%d" % (len(FIXTURES), len(MUTANT_FIXTURE)))
    return 0


def single_control(lane: Path, work: Path, entry: str, label: str,
                   expected: tuple[int, int, int]) -> int:
    root = Path(tempfile.mkdtemp(prefix=f"control-{label}-", dir=work))
    repo = scratch_repo(root, lane)
    write_files(repo, {ENTRY: entry})
    commit = commit_state(repo, f"control {label}")
    clone = ensure_clone(repo, root / "clone")
    verdict = evaluate(entry, None, clone, commit, work)
    observed = (verdict.q1, verdict.q21, verdict.q13)
    reached = verdict.defects == 0
    ok = observed == expected and not reached
    print(f"CONTROL {label} q1={verdict.q1} q21={verdict.q21} q13={verdict.q13} "
          f"defects={verdict.defects} target_reached={'True' if reached else 'False'} "
          f"expect=q1={expected[0]} q21={expected[1]} q13={expected[2]} "
          f"{'OK' if ok else 'MISMATCH'}")
    print(f"  detail q1={verdict.detail1} | q21={verdict.detail21} | q13={verdict.detail13}")
    return 0 if ok else 1


def control_filler(lane: Path, work: Path) -> int:
    base = revision_text(lane, BASE, ENTRY)
    if base is None:
        raise CouldNotEvaluate(f"BASE {BASE} has no {ENTRY}")
    return single_control(lane, work, base, "filler", (1, 1, 1))


def control_date_only(lane: Path, work: Path) -> int:
    base = revision_text(lane, BASE, ENTRY)
    if base is None:
        raise CouldNotEvaluate(f"BASE {BASE} has no {ENTRY}")
    entry = entry_fixture(
        base, recheck="python3 plans/round83_c1_replay.py --lane . --work DIR on 2027-01-04")
    return single_control(lane, work, entry, "date-only", (0, 1, 1))


def mutant_mode(lane: Path, work: Path, rule: str) -> int:
    if rule not in MUTANT_FIXTURE:
        raise CouldNotEvaluate(f"unknown mutant {rule!r}")
    clone, commits, _root = build_fixtures(lane, work)
    ident = MUTANT_FIXTURE[rule]
    failure = 0
    for label, target in (("designated", ident), ("base", "a-base")):
        commit = commits[target]
        lesson = revision_text(clone, commit, LESSON)
        entry = revision_text(clone, commit, ENTRY)
        if entry is None:
            print(f"MUTANT {rule} {label}-fixture={target} MISSING-ENTRY")
            failure = 1
            continue
        plain = evaluate(entry, lesson, clone, commit, work)
        mutated = evaluate(entry, lesson, clone, commit, work, mutant=rule)
        killed = (plain.q1, plain.q21, plain.q13) != (mutated.q1, mutated.q21, mutated.q13)
        print(f"MUTANT {rule} {label}-fixture={target} baseline_defects={plain.defects} "
              f"mutated_defects={mutated.defects} {'KILLED' if killed else 'SURVIVED'}")
        if not killed:
            failure = 1
    return failure


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="R84-C2 admission-bar counter (Q1, Q21, Q13) for one knowledge entry.")
    parser.add_argument("--lane", type=Path, default=LANE_DEFAULT,
                        help="lane repository root (default: the invocation directory)")
    parser.add_argument("--rev", help="measured revision (default: the working tree)")
    parser.add_argument("--work", type=Path, help="scratch directory for clones and fixtures")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--selftest", action="store_true", help="run the fixture and mutant battery")
    modes.add_argument("--mutant", choices=sorted(MUTANT_FIXTURE),
                       help="relax one rule to always-true and require the kill")
    modes.add_argument("--control-filler", action="store_true",
                       help="BASE bytes must stay red (defects=3)")
    modes.add_argument("--control-date-only", action="store_true",
                       help="recheck date-only repair must keep q21=1 and q13=1")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    lane = args.lane.expanduser().resolve()
    if not (lane / ".git").exists():
        print(f"COULD-NOT-EVALUATE lane is not a git repository: {lane}")
        return 2
    work: Path | None = None
    temporary: tempfile.TemporaryDirectory[str] | None = None
    try:
        if args.work is not None:
            work = args.work.expanduser().resolve()
            work.mkdir(parents=True, exist_ok=True)
        else:
            temporary = tempfile.TemporaryDirectory(prefix="r84-c2-")
            work = Path(temporary.name)
        if args.selftest:
            return selftest(lane, work)
        if args.mutant:
            return mutant_mode(lane, work, args.mutant)
        if args.control_filler:
            return control_filler(lane, work)
        if args.control_date_only:
            return control_date_only(lane, work)
        entry, lesson, clone, commit = load_measured(lane, args.rev)
        if lesson is not None and clone is None:
            clone = ensure_clone(lane, work / "gate-clone")
            if commit is None:
                commit = resolve_commit(lane, args.rev or "HEAD")
        verdict = evaluate(entry, lesson, clone, commit, work)
        emit(verdict)
        return 0 if verdict.defects == 0 else 1
    except CouldNotEvaluate as exc:
        print(f"COULD-NOT-EVALUATE {exc}")
        return 2
    finally:
        if temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    sys.exit(main())
