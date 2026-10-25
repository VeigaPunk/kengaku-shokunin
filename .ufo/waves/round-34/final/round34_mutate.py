#!/usr/bin/env python3
"""Round 34 mutation harness (landed by KengakuR34).

Mirrors the lane tip with git metadata, then applies eight mutations across the four
declared classes (index-vs-HEAD, heading-only, width/newline, token-co-occurrence) and
requires `round34_defects.py` to go red on every mutant and stay green on the clean
mirror. `--fleet-root` supplies a sandbox fleet copy for the N3/N4 fleet-report checks
so every class is testable without touching the read-only fleet repo.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
FLEET = Path("/home/vgpnk/Projects/shokunin")
HERE = Path(__file__).resolve().parent


def counter_path() -> Path:
    candidates = (
        Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round34_defects.py"),
        HERE / "round34_defects.py",
    )
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("round34_defects.py not found")


def run_counter(counter: Path, lane: Path, fleet: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(counter), "--lane", str(lane), "--fleet-root", str(fleet)],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )


def mirror_lane(dest: Path) -> None:
    subprocess.run(["git", "clone", "-q", str(LANE), str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "config", "user.name", "harness"], check=True)
    subprocess.run(
        ["git", "-C", str(dest), "config", "user.email", "harness@example.invalid"],
        check=True)


def mirror_fleet(dest: Path) -> None:
    """Sandbox fleet root carrying byte copies of the two reports N3/N4 read."""
    r31 = dest / ".ufo/reports/round-31"
    r32 = dest / ".ufo/reports/round-32"
    r31.mkdir(parents=True)
    r32.mkdir(parents=True)
    shutil.copyfile(FLEET / ".ufo/reports/round-31/kengaku.md", r31 / "kengaku.md")
    shutil.copyfile(FLEET / ".ufo/reports/round-32/kengaku.md", r32 / "kengaku.md")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise ValueError(f"token not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def mutate_lane(lane: Path, number: int) -> None:
    knowledge = lane / "corpus/knowledge"
    if number == 1:
        target = knowledge / "provider-selfreport-eval-limits.md"
        if not target.is_file():
            target = next(iter(sorted(knowledge.glob("*.md"))))
        target.unlink()
    elif number == 2:
        (knowledge / "round34-unindexed-fixture.md").write_text(
            "# Round 34 unindexed fixture\n", encoding="utf-8")
    elif number == 3:
        path = lane / "SCORECARD.md"
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^## Round 32\b.*$", text)
        if not match:
            raise ValueError("SCORECARD.md has no Round 32 heading")
        text = text[:match.start()] + "## Round 33\n\n" + text[match.start():]
        path.write_text(text, encoding="utf-8")
    elif number == 4:
        path = lane / "SCORECARD.md"
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^## Round 32\b[^\n]*\n", text)
        if not match:
            raise ValueError("SCORECARD.md has no Round 32 section")
        end = re.search(r"(?m)^##? ", text[match.end():])
        section_end = match.end() + end.start() if end else len(text)
        path.write_text(
            text[:match.start()] + text[match.start():match.end()].rstrip("\n") + "\n\n"
            + text[section_end:].lstrip("\n"), encoding="utf-8")
    elif number == 5:
        replace_once(lane / "corpus/lessons/round-31.md", "precedence docstring at `:35-38`", "precedence docstring at `:35-\n38`")
    elif number == 6:
        text = (lane / "corpus/lessons/round-30.md").read_text(encoding="utf-8")
        if ":78-81" in text:
            (lane / "corpus/lessons/round-30.md").write_text(
                text.replace(":78-81", ":78- 81"), encoding="utf-8")
        elif ":78–81" in text:
            (lane / "corpus/lessons/round-30.md").write_text(
                text.replace(":78–81", ":78– 81"), encoding="utf-8")
        else:
            raise ValueError("round-30.md has no 78-81 token")
    elif number == 7:
        report = lane / ".ufo/reports/round-31/kengaku.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            "# Report\n\nParagraph one references token a44b5a8 in an unrelated claim.\n\n"
            + ("Unrelated intervening text. " * 8) + "\n\n"
            "Paragraph two references token ae95fe0 in a different unrelated claim.\n",
            encoding="utf-8")
    elif number == 8:
        report = lane / ".ufo/reports/round-32/kengaku.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(
            "# Report\n\nRound 32 narrative.\n\nContext line mentions 112091c without any closure relation.\n",
            encoding="utf-8")


def mutate_fleet(fleet: Path, number: int) -> None:
    if number == 7:
        (fleet / ".ufo/reports/round-31/kengaku.md").write_text(
            "# Report\n\nParagraph one references token a44b5a8 in an unrelated claim.\n\n"
            + ("Unrelated intervening text. " * 8) + "\n\n"
            "Paragraph two references token ae95fe0 in a different unrelated claim.\n",
            encoding="utf-8")
    elif number == 8:
        (fleet / ".ufo/reports/round-32/kengaku.md").write_text(
            "# Report\n\nRound 32 narrative.\n\nContext line mentions 112091c without any closure relation.\n",
            encoding="utf-8")


EXPECTED = {
    1: "N8", 2: "N8", 3: "N7", 4: "N2",
    5: "N5", 6: "N6", 7: "N3", 8: "N4",
}


def selftest() -> int:
    with tempfile.TemporaryDirectory(prefix="r34-harness-") as tmp:
        root = Path(tmp)
        counter = counter_path()
        # green fixture: clean mirrors must pass
        lane = root / "green-lane"
        fleet = root / "green-fleet"
        mirror_lane(lane)
        mirror_fleet(fleet)
        clean = run_counter(counter, lane, fleet)
        if clean.returncode != 0 or "defects=0" not in clean.stdout:
            print("[selftest] clean mirror not green:")
            print(clean.stdout)
            return 1
        # red fixtures: every mutant detected under its expected check
        for n in range(1, 9):
            m = root / f"m{n}"
            fleet_m = root / f"fleet{n}"
            mirror_lane(m)
            mirror_fleet(fleet_m)
            mutate_lane(m, n)
            mutate_fleet(fleet_m, n)
            out = run_counter(counter, m, fleet_m)
            expected = EXPECTED[n]
            if out.returncode == 0 or expected not in out.stdout:
                print(f"[selftest] mutant M{n} not detected as {expected}:")
                print(out.stdout)
                return 1
    print("SELFTEST cases=10 failed=0")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    with tempfile.TemporaryDirectory(prefix="round34-mutate-") as tmp:
        root = Path(tmp)
        lane = root / "clean"
        fleet = root / "fleet"
        mirror_lane(lane)
        mirror_fleet(fleet)
        counter = counter_path()
        clean = run_counter(counter, lane, fleet)
        if clean.returncode != 0 or "defects=0" not in clean.stdout:
            print("CLEAN exit=%d" % clean.returncode)
            print(clean.stdout)
            return 1
        print("CLEAN exit=0")
        detected = 0
        for n in range(1, 9):
            m = root / f"m{n}"
            fleet_m = root / f"fleet{n}"
            mirror_lane(m)
            mirror_fleet(fleet_m)
            mutate_lane(m, n)
            mutate_fleet(fleet_m, n)
            out = run_counter(counter, m, fleet_m)
            expected = EXPECTED[n]
            if out.returncode != 0 and expected in out.stdout:
                detected += 1
            else:
                print(f"MUTANT M{n} UNDETECTED (expected {expected})")
                print(out.stdout)
        print(f"MUTANTS total=8 detected={detected}")
        return 0 if detected == 8 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
