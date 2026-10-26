#!/usr/bin/env python3
"""Round-38 C1 battery, seat R38BatD4: single-fixture kills for the frozen D4 mutants N19 and N20.

Both mutants live in one clause of `plans/pkg_gate.py` (cmd_d4 -> check, at the freeze digest):

    bad = [f"pattern{i}" for i, pat in enumerate(spec["d4"]["patterns"], 1)
           if not re.search(pat, lines[0])]

  N19 `enumerate(spec["d4"]["patterns"], 1)` -> `enumerate(spec["d4"]["patterns"][:-1], 1)`
      advertises "every directional pattern is checked, the last included".
  N20 `if not re.search(pat, lines[0])]` -> `if not re.search(pat, lines[0], re.IGNORECASE)]`
      advertises "directional patterns match case-sensitively".

Fixture design, chosen so that each fixture kills exactly one mutant:

  d4m-n19-last-pattern-unmatched
      The genuine correction line with the LAST pattern's own phrase made false
      ("selftest was green" -> "selftest was fine"); patterns 1..n-1 still match. The unmodified gate
      prints `D4 DEFECT ... failed=['pattern3']`, the N19 mutant never looks at pattern 3 and prints
      `D4 ok`. The N20 mutant still checks pattern 3 case-sensitively, still fails it, and survives.
  d4m-n20-pattern-case-differs
      The genuine line with one word inside the FIRST pattern's phrase re-capitalised
      ("...md:8` records" -> "...md:8` Records"); every other byte untouched. Only pattern 1 fails,
      and only because of letter case. The unmodified gate prints `D4 DEFECT ... failed=['pattern1']`;
      the N20 mutant matches all patterns under IGNORECASE and prints `D4 ok`. The N19 mutant still
      checks pattern 1 (it drops only the last one), still fails it, and survives.

Each builder re-checks its premise against `ctx.spec["d4"]["patterns"]` with `re`, so a fixture whose
line stops isolating its mutant raises instead of quietly passing. Both declare defects ["D4"]:
`d4-line` runs that single clause and the unmodified gate prints exactly `D4 DEFECT ...` (exit 1) on
each, so the declared set is the observed set. Paths are built from the directory the counter hands
in, so the counter's renamed run moves the bytes with the fixture; nothing keys off a directory or
file name.
"""
import pathlib
import re

# Last pattern's unique phrase, made untrue for N19 (case untouched, so only the claim is broken).
_LAST_PHRASE = "selftest was green"
_LAST_REPLACEMENT = "selftest was fine"
# First pattern's unique phrase, re-capitalised for N20 (only the letter case differs).
_FIRST_PHRASE = "R34C2CounterDraft.md:8` records"
_FIRST_REPLACEMENT = "R34C2CounterDraft.md:8` Records"


def _genuine_line(ctx):
    line = ctx.d4_line()
    if line is None:
        raise RuntimeError("genuine D4 correction line absent from the lane")
    if not line.startswith(ctx.spec["d4"]["label"]):
        raise RuntimeError("genuine D4 correction line does not start with spec.d4.label")
    return line


def _patterns(ctx):
    pats = list(ctx.spec["d4"]["patterns"])
    if len(pats) < 2:
        raise RuntimeError("spec.d4.patterns has fewer than two entries")
    return pats


def _matches(pats, line, flags=0):
    return [bool(re.search(p, line, flags)) for p in pats]


def _one_substitution(line, needle, replacement):
    if line.count(needle) != 1:
        raise RuntimeError(f"genuine line carries {line.count(needle)} copies of {needle!r}, expected 1")
    altered = line.replace(needle, replacement)
    if altered == line:
        raise RuntimeError("substitution did not take")
    return altered


def _write(d, name, line):
    p = pathlib.Path(d) / name
    p.write_text(line + "\n", encoding="utf-8")
    return p


def build_n19(ctx, d):
    """Only the LAST directional pattern is unsatisfied, for a reason case-folding cannot fix."""
    pats = _patterns(ctx)
    altered = _one_substitution(_genuine_line(ctx), _LAST_PHRASE, _LAST_REPLACEMENT)
    got = _matches(pats, altered)
    want = [True] * (len(pats) - 1) + [False]
    if got != want:
        raise RuntimeError(f"premise broken: pattern matches = {got}, wanted {want}")
    if _matches(pats, altered, re.IGNORECASE) != got:
        raise RuntimeError("last-pattern failure is case-foldable; it would also isolate N20")
    p = _write(d, "d4-correction-last-pattern-unmatched.txt", altered)
    return ["d4-line", "--file", str(p)]


def build_n20(ctx, d):
    """Only the FIRST pattern fails, and only because of letter case."""
    pats = _patterns(ctx)
    altered = _one_substitution(_genuine_line(ctx), _FIRST_PHRASE, _FIRST_REPLACEMENT)
    strict = _matches(pats, altered)
    if strict != [False] + [True] * (len(pats) - 1):
        raise RuntimeError(f"premise broken: case-sensitive pattern matches = {strict}")
    if not all(_matches(pats, altered, re.IGNORECASE)):
        raise RuntimeError("premise broken: case-insensitive run still fails a pattern")
    p = _write(d, "d4-correction-pattern-case-differs.txt", altered)
    return ["d4-line", "--file", str(p)]


FIXTURES = [
    {"fid": "d4m-n19-last-pattern-unmatched", "expect": "reject", "defects": ["D4"], "build": build_n19},
    {"fid": "d4m-n20-pattern-case-differs", "expect": "reject", "defects": ["D4"], "build": build_n20},
]
