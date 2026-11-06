source: S326–S330, https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-chess/tests/test_outputs.py:35; companion files and quotes in corpus/lessons/round-98.md §Gate
verified-at: 2026-11-06 (round 98; measured T 8e37fc65d5649bb37166fdd6b1657445a8cb55b9)
recheck: on-release

# Per-line membership plus an equal count is not set equality

The captured `regex-chess` grader applies `/app/re.json` (a list of `[regex, replacement]` pairs) to
each tested FEN, splits the result on newlines, drops the last two fields of every line, and compares
with python-chess 1.11.2's successors (queen promotions only). Each output line must be in the
reference set — or become a member once its last remaining field is rewritten to `-` — and the
number of lines must equal the size of the reference set. The tested positions are every
white-to-move position of three published games (108 calls, 103 distinct FENs). A fourth test caps the
file at 10e6 characters and 1e5 pairs.

The replay runs the captured file unchanged under real `pytest.main` (an observe-only hook records each
test's outcome and exception type) with python 3.13 / chess 1.11.2 / pytest 8.4.1, the `test.sh` pins.
Twelve cases × five legs reproduce their P0 mechanism predictions (`plans/round98-cases.json`,
`corpus/evidence/round98/regexchess-probe.txt`).

| intervention | observed (immortal, century, naroditsky, not_long, reward) | interpretation |
|---|---|---|
| C01 captured solve.sh, unchanged (40460 pairs) | P,P,P,P,1 | positive control; one timed host run took 233 s (L1 timing run, not a committed receipt) |
| C02 no re.json | E:FileNotFoundError ×4, 0 | no-work is rejected (errors, not assertion failures) |
| C03 `[]` | F,F,F,P,0 | the identity transform returns the input position |
| C04 first successor duplicated, second removed | P,P,P,P,1 | **gap**: a missing legal move hides behind a duplicate; per-line membership plus an equal count is weaker than set equality |
| C05 one successor removed | F,F,F,P,0 | the count check catches an omission |
| C06 one successor duplicated without removal | F,F,F,P,0 | the count check catches an extra line |
| C07 en-passant square `h6` invented on every line whose true field is `-` | P,P,P,P,1 | **gap**: the `rpartition` fallback forgives any last field, so a wrong en-passant square is never caught when none is legal |
| C08 castling field forced to `-` | F,F,F,P,0 | mechanism negative: the fallback reaches only the last field, so a castling field is compared verbatim; at positions whose true castling field is already `-` this corruption is invisible (ScribeLesson B: 47 of 108 tested positions) |
| C09 lookup table: 103 anchored literal pairs, one per distinct tested FEN (108 calls), contents precomputed offline with python-chess | P,P,P,P,1 | **gap**: the hidden positions are a fixed public set; the artefact does no move generation at grading time, and the instruction's "tested on other positions as well" is not enforced by these bytes |
| C10 the same table minus its last entry (a Naroditsky–Ivanchuk position) | P,P,F,P,0 | that game has a witness; only the third game's witness was exercised here |
| C11 solution + one never-matching pair with a 10,000,001-char replacement | P,P,P,F,0 | the character cap has a witness |
| C12 solution padded to exactly 100000 pairs | P,P,P,F,0 | the pair cap has a witness, independently of the character cap |

## Reuse rule

When a grader checks a generated set, test duplicates and omissions together: a membership loop plus
a length check passes a list that trades one element for a copy of another. When a grader forgives a
field by rewriting it (`rpartition(" ")[0] + " -"`), write one case per forgiven value and one per
neighbouring field that must not be forgiven. When the hidden inputs are a small fixed public set,
price a lookup-table submission explicitly; a passing lookup table is a statement about the test set,
not the artefact.

## Limits

- The verifier side is modelled by a pinned venv, not the prebuilt image (S332 rejected); CTRF
  reporting (`pytest-json-ctrf`) is not staged.
- `check.py` (S331) is agent-side and checks a different game; not part of any case.
- The probe states what the captured bytes accept; it does not claim the gaps were exploited by any
  submitted solution or leaderboard entry.
