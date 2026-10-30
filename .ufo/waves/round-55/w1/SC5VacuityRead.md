# SC5VacuityRead — scoped findings (round 55 w1)

Seat: vacuity read of the chess-best-move grader — second pair of eyes beside the entry
(R55-C3 Q13/Q14 re-read). Full detail: `.ufo/waves/round-55/w1/SC5VacuityRead/vacuity.md`.

**Inputs verified**: captured `tests/test_outputs.py` sha256 `a540714e…cb8f286` = frozen pin;
fetched upstream `instruction.md` @ `2fd12b88` sha256 `6ba25be4…19ce7a` = round-lesson Gate
pin; runner `test.sh` = S109-identical per amendment A1.

**Grader semantics** (`test_outputs.py:22-25`): single assertion — full-multiset equality
(`sorted(move) == sorted(["g2g4","e2e4"])`) over no-arg `split()` tokens of
`/app/move.txt`. `.strip()` is dead code. Separator class = any Unicode-whitespace run
(space/tab/CRLF/blank lines/NBSP/U+2028/U+2029/`\x1c`-`\x1f`/VT all pass-separate);
ZWSP/NUL/BOM/punctuation/case/fullwidth digits/Cyrillic homoglyphs/SAN forms all poison
tokens → fail. Empty or whitespace-only file → `[]` → fail. Missing file /
non-UTF-8 bytes → traceback-fail, reward 0, same verdict class.

**Probe cross-check**: all 12 frozen predictions (`plans/round55_c3_chess_probe.py:54-79`)
agree with this independent read; no mismatch, no defect. R55-C3 kill rules (a)/(b)/(c) not
fired.

**Instruction-vs-grader gaps** (`instruction.md:1`): (1) oracle never reads the board image
— PNG is built at container build from FEN in upstream `environment/make.py:116-119`, and
the expected pair is a literal in the assertion (docstring = authors' self-report; that
docstring also labels `e2e4` a "pawn move" while the FEN rank 2 `1P2QPP1` has Qe2 — oddity
on record, no chess-truth claim); (2) the example literal `e2e4` is half the answer key —
example-anchoring is indistinguishable to the grader; (3) "one per line" guidance is
stricter than the oracle (any whitespace works), while human punctuation ("1. g2g4") fails;
(4) "print them all" is enforced as exactly-two by fiat.

**GAPS (what a 12-case table could still mispredict)**: BOM-prefixed answer fails;
exotic-Unicode-whitespace separators pass; ZWSP/NUL glue-and-fail; punctuation and
numbering fail; SAN/hyphen/mate-suffix notation fails; homoglyph/case cells untested;
whitespace-only ≠ empty but same observable; failure-class (traceback vs "File is wrong")
flattened by verdict tables; decode locale env-dependent in the wild (probe freezes
UTF-8); chess-truth of the answer key outside every case's reach.
