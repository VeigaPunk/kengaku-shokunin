#!/usr/bin/env python3
"""Prove the drafted C1 erratum line satisfies r35_d4 of plans/round36_c1_verify.py.

Builds a mktemp lane tree holding the committed toolathlon package copy plus a fixture
corpus/lessons/round-36.md carrying the line under a `## Gate` heading, then imports the
frozen counter module and calls r35_d4 unmodified. Negative controls show the predicate
can fail (each mutation flips ok to False).
"""
import importlib.util
import pathlib
import shutil
import tempfile

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kengaku-shokunin")
PKG_REL = "corpus/evidence/round36/toolathlon-package.md"
LESSON_REL = "corpus/lessons/round-36.md"

ERRATUM = (
    "Erratum (round 36): S130's Outcome table's three leaf rows are 13 + 23 + 1 = 37 against the "
    "stated denominator 38 in the committed copy corpus/evidence/round36/toolathlon-package.md, so "
    "the table contradicts its own header and the row's \"13 of 38\" summary cannot corroborate "
    "the count; recorded as an erratum, not repaired."
)

LESSON = f"""# Round 36 — lesson (fixture)

Fixture lesson for the R36 D4 erratum proof. Body is not graded; only the Gate section is.

## Gate

The gate row of record carries the calibrated line below, one physical line, starting the
exact prefix the frozen counter greps for.

{ERRATUM}

## Notes

Anything after the next heading is outside the Gate section.
"""


def load_counter():
    spec = importlib.util.spec_from_file_location("c1v36", LANE / "plans/round36_c1_verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(root, lesson: str | None = LESSON, with_pkg: bool = True):
    lane = root / "lane"
    (lane / "corpus/evidence/round36").mkdir(parents=True)
    (lane / "corpus/lessons").mkdir(parents=True)
    if with_pkg:
        shutil.copy2(LANE / PKG_REL, lane / PKG_REL)
    if lesson is not None:
        (lane / LESSON_REL).write_text(lesson, encoding="utf-8")
    return lane


def main():
    c1 = load_counter()
    cases = []

    def case(name, lesson=LESSON, with_pkg=True):
        root = pathlib.Path(tempfile.mkdtemp(prefix="k36-d4-"))
        try:
            lane = build(root, lesson, with_pkg)
            ok, detail = c1.r35_d4(lane)
            cases.append((name, ok, detail))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    # positive: the drafted line, under ## Gate, exactly once
    case("fixture_with_erratum")

    # negatives
    case("lesson_without_gate_section", lesson="# Round 36\n\nno gate here\n")
    case("gate_without_erratum", lesson="## Gate\n\nnothing yet\n")
    case("two_erratum_lines",
         lesson="## Gate\n\n" + ERRATUM + "\n" + ERRATUM.replace('"13 of 38"', '"13 of 38" (again)') + "\n")
    case("denominator_equals_recount", lesson="## Gate\n\n" + ERRATUM.replace("denominator 38", "denominator 37") + "\n")
    case("no_S130", lesson="## Gate\n\n" + ERRATUM.replace("S130", "S1xx") + "\n")
    case("wrong_arithmetic", lesson="## Gate\n\n" + ERRATUM.replace("13 + 23 + 1 = 37", "13 + 23 + 1 = 38") + "\n")
    case("bullet_prefixed_line", lesson="## Gate\n\n- " + ERRATUM + "\n")
    case("package_absent", with_pkg=False)

    # state of the real lane today (read-only, no write)
    real_ok, real_detail = c1.r35_d4(LANE)

    print(f"DRAFTED ERRATUM ({len(ERRATUM.split())} words, 1 physical line):\n{ERRATUM}\n")
    good = True
    for name, ok, detail in cases:
        want = name == "fixture_with_erratum"
        verdict = "PASS" if ok == want else "FAIL"
        good &= ok == want
        print(f"{verdict:4} {name:28} r35_d4={ok}  {detail}")
    print(f"\nreal lane now: r35_d4={real_ok}  {real_detail}")
    print(f"\nPROOF {'holds' if good else 'BROKEN'}: drafted line satisfies r35_d4; every negative control flips it.")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
