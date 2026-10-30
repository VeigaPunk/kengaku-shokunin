# report.md — SC5VacuityRead — round 55 w1

Independent semantic read of the chess-best-move grader (second pair of eyes for R55-C3's
Q13/Q14). Read-only seat.

## What I ran

All work in `/fast/scratch/hyaku/kengaku-r55/SC5VacuityRead/` (created, then deleted before
yield). Fleet-root cwd respected; no lane file outside my wave dir touched; no git
mutations; no installs (uv/pacman/binary — none needed, record: zero installs).

| # | Command (cwd = scratch) | Exit | Result |
|---|---|---|---|
| 1 | `mkdir -p $S` | 0 | scratch ready |
| 2 | `sha256sum …/corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` | 0 | `a540714e…cb8f286` — matches frozen R55-C3 pin |
| 3 | `curl -fsSL -o instruction.md https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88…/chess-best-move/instruction.md && sha256sum instruction.md && od -c instruction.md` | 0 | `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` — matches round-55 lesson Gate pin; 260 bytes, single line |
| 4 | `curl -fsSL -o make.py …/environment/make.py` | 0 | 122 lines; FEN `r1bq1r2/1p3pp1/p1n1p3/3nPkbP/8/P1N5/1P2QPP1/R1B1K2R w KQ - 0 16` at make.py:116-119 (comment mislabels it "Standard starting position") |
| 5 | `curl -fsSL -o Dockerfile …/environment/Dockerfile` | 0 | `RUN python3 make.py` → `rm make.py`; PNG provenance confirmed |
| 6 | `python3 probe.py` (18-case empirical battery of the exact `read_text().strip().split()` + `sorted(...)==sorted(["g2g4","e2e4"])` expression) | 0 | see vacuity.md §2 table |
| 7 | `python3` re-run of 4 rows with explicit `\u` escapes (U+2028/U+2029/Cyrillic homoglyph/NBSP/ZWSP) + codepoint assertions | 0 | separator class and homoglyph verdicts confirmed unambiguously |
| 8 | `grep -n` line pins on captured `test_outputs.py` / `test.sh` | 0 | refs used in vacuity.md are exact |

Reads (read-only, others' files): `plans/round-55-claims.md`, `plans/round55_c3_chess_probe.py`
(frozen CASES table at :54-79), `corpus/evidence/round52/graders/chess-best-move/tests/{test_outputs.py,test.sh}`,
`corpus/evidence/round52/graders/SHA256SUMS`, `corpus/SOURCES.md` (S201/S202 rows),
`corpus/evidence/round53/pin-tree-2fd12b88.json`, `corpus/knowledge/../lessons/round-55.md` (Gate pins).

## Files I wrote

- `.ufo/waves/round-55/w1/SC5VacuityRead/vacuity.md` — the seat target: full semantics
  enumeration (line-ref'd), empirical probe table, instruction-vs-grader gaps, `GAPS:` list.
- `.ufo/waves/round-55/w1/SC5VacuityRead/report.md` — this file.
- `.ufo/waves/round-55/w1/SC5VacuityRead.md` — scoped findings (Report: trailer path).

## Findings summary

- Grader = one assertion (`test_outputs.py:25`): order-insensitive full-multiset equality
  over `read_text().strip().split()` of `/app/move.txt`; `strip()` is dead code; no-arg
  `split()` accepts any Unicode-whitespace run as separator; token equality is exact
  (case, width, punctuation, BOM, NUL, homoglyphs all poison). No defect in the capture.
- All 12 frozen case predictions in `plans/round55_c3_chess_probe.py:54-79` agree with my
  independent read — no counter-evidence to R55-C3; kill rules (a)/(b)/(c) untouched.
- Instruction-vs-grader gaps recorded: grader never observes the board image (PNG built
  from FEN in upstream make.py:116-119; answer pair is a literal); the instruction's
  example literal `e2e4` is half the answer key (anchoring undetectable by the oracle);
  "one per line" guidance is stricter than the oracle; "print them all" is enforced as
  exactly-two by fiat.
- `GAPS:` (11 entries) — BOM-fails, exotic-whitespace-passes, ZWSP/NUL-fails,
  punctuation/SAN/homoglyph-fails, whitespace-only-file, failure-class flattening,
  locale-dependent decode in the wild, chess-truth outside all cases. Full list with
  evidence in vacuity.md.
- One on-record oddity for the entry seat / L1: the upstream docstring labels `e2e4` a
  "pawn move" while the position FEN (`1P2QPP1` rank 2) has a white queen on e2. No
  chess-truth claim made; the probe's oracle (captured assertions) is unaffected.

## Defects found in siblings' files

None. The frozen probe table checked out against independent analysis.

## Dead ends

- Heredoc-embedded literal non-ASCII (U+2028/Cyrillic) rows in the first probe run were
  ambiguous on serialization; re-ran those rows with explicit `\u` escapes and codepoint
  assertions — resolved, no ambiguity remains.
- No local copy of `instruction.md` exists in the corpus (only the URL is pinned in
  S202); fetched it read-only from the pinned URL and verified sha256 against the round
  lesson instead. No new capture committed (GH013 L0 respected).

## Scratch

`/fast/scratch/hyaku/kengaku-r55/SC5VacuityRead/` deleted after writing the three outputs
above. Nothing left behind.
