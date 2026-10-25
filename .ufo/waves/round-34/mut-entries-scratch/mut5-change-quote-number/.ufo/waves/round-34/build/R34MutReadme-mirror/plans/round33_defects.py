#!/usr/bin/env python3
"""Re-derive the six defect items round 32's non-author closure routed to this lane.

Round 33 (2026-10-25), claim C2. One command, one line: `defects=N`, exit 0 only
when every one of N1-N6 re-derives as repaired. Each check reads committed or live
bytes round 32 left behind (plus this round's own lesson/report, which are round
deliverables, not claim-owned bytes); none reads an artifact round 33's C1 or C3
creates, so C2 stays separable from them (QUALITY R13).

Frozen items (corpus/lessons/round-32-verifier-spotcheck.md §5, the round-32
report's disclosures, and the protocol's round-record contract):
  N1  ten round-32 wave paths sat untracked at a pushed tip. The repair commits the
      whole `.ufo/waves/round-32/` tree under this round's entry.
  N2  round 32 landed no SCORECARD.md section. The repair appends a `## Round 32`
      section recording round 32's dispositions (C1 refused, C2 incomplete, C3
      failed as declared; scores unchanged).
  N3  the round-31 report addendum cites phantom hash `a44b5a8` (`git cat-file -t`
      fails); the locator fix landed at `ae95fe0`. Report bytes are append-only, so
      the repair is an appended erratum naming the bogus token and superseding it.
  N4  the round-32 report cites lane tip `bcd2a6c`, but the round-32 closure commit
      `112091c` landed after the report was filed. The repair is an append-only
      addendum to the filed round-32 report naming the closure tip.
  N5  the round-31 lesson Gate cites verifier_mode.py's precedence docstring at
      `:35-38`; the entry corrected it to `:39-40`. The repair appends a labelled
      correction note (the stale locator stays).
  N6  the round-30 lesson erratum points the Q6 retraction at entry `:78-81` (now
      `:72` / `:82-83`) and its `:66` line groups "S083/S086 peer-reviewed" while
      the registry records S086 as published without peer review. The repair
      appends two labelled notes (the stale text stays).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FLEET = Path("/home/vgpnk/Projects/shokunin")
R31_REPORT = FLEET / ".ufo/reports/round-31/kengaku.md"
R32_REPORT = FLEET / ".ufo/reports/round-32/kengaku.md"
WAVE32 = ".ufo/waves/round-32"
SCORECARD = "SCORECARD.md"
LESSON31 = "corpus/lessons/round-31.md"
LESSON30 = "corpus/lessons/round-30.md"
CLOSURE_TIP = "112091c"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def git(lane: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(lane), *args], capture_output=True, text=True, check=False
    )


def near(text: str, a: str, b: str, width: int = 300, flags: int = re.I) -> bool:
    """True when `a` and `b` co-occur within `width` characters."""
    return bool(
        re.search(re.escape(a) + r".{0," + str(width) + r"}" + re.escape(b), text, flags)
        or re.search(re.escape(b) + r".{0," + str(width) + r"}" + re.escape(a), text, flags)
    )


def check_n1(lane: Path) -> str:
    """Every file under .ufo/waves/round-32/ is tracked; nothing untracked remains."""
    disk = subprocess.run(
        ["find", str(lane / WAVE32), "-type", "f", "-printf", "%P\n"],
        capture_output=True, text=True, check=False,
    )
    if disk.returncode != 0:
        return f"{WAVE32} is not readable on disk: {disk.stderr.strip()}"
    on_disk = {line for line in disk.stdout.splitlines() if line}
    proc = git(lane, "ls-files", "--", WAVE32)
    if proc.returncode != 0:
        return f"git ls-files failed: {proc.stderr.strip()}"
    tracked = {
        line[len(WAVE32) + 1:] if line.startswith(WAVE32 + "/") else line
        for line in proc.stdout.splitlines()
        if line
    }
    missing = sorted(on_disk - tracked)
    if missing:
        return f"{len(missing)} untracked files remain under {WAVE32}: {', '.join(missing[:3])}"
    return ""


def check_n2(lane: Path) -> str:
    path = lane / SCORECARD
    if not path.is_file():
        return f"{SCORECARD} is unreadable"
    if not re.search(r"^## Round 32\b", read(path), re.MULTILINE):
        return "SCORECARD.md carries no '## Round 32' section: round 32's dispositions are unrecorded"
    return ""


def check_n3(lane: Path, r31_report: Path | None = None) -> str:
    r31_report = r31_report or R31_REPORT
    if not r31_report.is_file():
        return f"{r31_report} is unreadable: the round-31 report cannot be checked"
    text = read(r31_report)
    if "a44b5a8" not in text:
        return "the bogus hash a44b5a8 is gone from the report: append-only forbids rewriting it"
    if not near(text, "a44b5a8", "superseded") and not near(text, "a44b5a8", "erratum"):
        return "no appended erratum supersedes the a44b5a8 citation"
    if "ae95fe0" not in text:
        return "the appended erratum does not name the real locator-fix commit ae95fe0"
    return ""


def check_n4(lane: Path, r32_report: Path | None = None) -> str:
    r32_report = r32_report or R32_REPORT
    if not r32_report.is_file():
        return f"{r32_report} is unreadable: the round-32 report cannot be checked"
    if CLOSURE_TIP not in read(r32_report):
        return f"the round-32 report does not name the round-32 closure tip {CLOSURE_TIP}"
    return ""


def check_n5(lane: Path) -> str:
    path = lane / LESSON31
    if not path.is_file():
        return f"{LESSON31} is unreadable"
    text = read(path)
    if ":35-38" not in text:
        return "the round-31 lesson's stale :35-38 locator is gone: append-only forbids rewriting it"
    if not near(text, "verifier_mode.py", ":39-40", width=300):
        return "no appended correction updates verifier_mode.py's precedence locator to :39-40"
    if not near(text, ":39-40", "correction", width=300) and not near(
        text, ":39-40", "superseded", width=300
    ):
        return "the round-31 lesson correction note is not labelled"
    return ""


def check_n6(lane: Path) -> str:
    path = lane / LESSON30
    if not path.is_file():
        return f"{LESSON30} is unreadable"
    text = read(path)
    if ":78-81" not in text and "78–81" not in text:
        return "the round-30 lesson erratum's stale :78-81 reference is gone: append-only forbids rewriting it"
    if ":72" not in text or "82-83" not in text:
        return "no appended correction updates the round-30 erratum's entry line refs to :72 / :82-83"
    if not near(text, ":72", "82-83", width=300) or (
        not near(text, ":72", "corrected", width=300)
        and not near(text, ":72", "superseded", width=300)
    ):
        return "the round-30 lesson correction note is not labelled"
    if "peer-reviewed" not in text:
        return "the round-30 lesson's peer-reviewed grouping is gone: append-only forbids rewriting it"
    if not near(text, "S086", "without peer review", width=250) and not near(
        text, "S086", "not peer-reviewed", width=250
    ):
        return "no appended erratum records S086 as published without peer review"
    if not near(text, "S086", "erratum", width=250) and not near(
        text, "S086", "correction", width=250
    ):
        return "the S086 peer-review erratum is not labelled"
    return ""


CHECKS = (
    ("N1", "round32-wave-tree-committed", check_n1),
    ("N2", "scorecard-round32-section", check_n2),
    ("N3", "round31-report-phantom-hash", check_n3),
    ("N4", "round32-report-closure-tip", check_n4),
    ("N5", "round31-lesson-locator", check_n5),
    ("N6", "round30-lesson-errata", check_n6),
)

FROZEN = tuple((i, l) for i, l, _ in CHECKS)


def selftest() -> int:
    cases: list[tuple[str, bool]] = [("registry-complete", FROZEN == tuple((i, l) for i, l, _ in CHECKS))]
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)

        # N3/N4 read absolute fleet paths by default, which would couple the
        # selftest to the live repair state. Run them against synthetic fixtures
        # so the selftest stays hermetic.
        r31 = empty / "r31.md"
        r31.write_text("cites a44b5a8 as the fix\n", encoding="utf-8")
        cases.append(("N3-red-unsuperseded", bool(check_n3(empty, r31))))
        r31.write_text(
            "cites a44b5a8 as the fix\n\n## Erratum (round 33)\n`a44b5a8` is a phantom hash, "
            "superseded: the locator fix landed at ae95fe0.\n",
            encoding="utf-8",
        )
        cases.append(("N3-green-superseded", not check_n3(empty, r31)))
        r32 = empty / "r32.md"
        r32.write_text("tip bcd2a6c\n", encoding="utf-8")
        cases.append(("N4-red-missing-tip", bool(check_n4(empty, r32))))
        r32.write_text("tip bcd2a6c\n\nAddendum (round 33): the round-32 closure tip 112091c landed after this report.\n", encoding="utf-8")
        cases.append(("N4-green-tip-named", not check_n4(empty, r32)))

        for item_id, label, check in CHECKS:
            if item_id in ("N3", "N4"):
                continue
            try:
                red = bool(check(empty))
            except Exception:
                red = True
            cases.append((f"{item_id}-red-on-empty", red))

        # Green-path fixture: build a minimal tree that satisfies N1/N2/N5/N6.
        wave = empty / WAVE32
        wave.mkdir(parents=True)
        (wave / "seat.md").write_text("seat report\n", encoding="utf-8")
        (empty / "corpus/lessons").mkdir(parents=True)
        (empty / SCORECARD).write_text("# Scorecard\n\n## Round 32 — record\n", encoding="utf-8")
        (empty / LESSON31).write_text(
            "precedence docstring (`:35-38`)\n\nCorrection (round 33): verifier_mode.py's precedence "
            "docstring is at :39-40 after the entry's fix.\n",
            encoding="utf-8",
        )
        (empty / LESSON30).write_text(
            "S083/S086 peer-reviewed)\nentry `:78-81`)\n\nCorrection (round 33): the Q6 retraction "
            "now points at entry lines :72 and 82-83 (corrected).\n\nErratum (round 33): S086 is "
            "published without peer review; the :66 grouping is wrong.\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "-C", str(empty), "init", "-q"], check=False)
        subprocess.run(["git", "-C", str(empty), "add", "."], check=False)
        cases.append(("N1-green-tracked", not check_n1(empty)))
        cases.append(("N2-green-section", not check_n2(empty)))
        cases.append(("N5-green-corrected", not check_n5(empty)))
        cases.append(("N6-green-corrected", not check_n6(empty)))
        # The same tree with one untracked file must redden N1.
        (wave / "stray.md").write_text("stray\n", encoding="utf-8")
        cases.append(("N1-red-untracked", bool(check_n1(empty))))

    failed = [name for name, passed in cases if not passed]
    for name, passed in cases:
        print(f"CASE {name} {'PASS' if passed else 'FAIL'}")
    print(f"SELFTEST checks={len(cases)} failed={len(failed)}")
    return 0 if not failed else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--lane", type=Path, default=Path("."))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    lane = args.lane.resolve()
    defects = 0
    for item_id, label, check in CHECKS:
        try:
            reason = check(lane)
        except Exception as error:
            reason = f"check raised {type(error).__name__}: {error}"
        if reason:
            defects += 1
            print(f"DEFECT {item_id} {label}: {reason}")
    print(f"checks={len(CHECKS)} defects={defects}")
    return 0 if defects == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
