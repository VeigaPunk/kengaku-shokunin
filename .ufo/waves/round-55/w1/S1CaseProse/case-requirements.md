# R55-C3 — the 12 frozen chess probe cases mapped to the instruction requirement each exercises

Seat S1CaseProse (scribe), wave kengaku-r55-w1, 2026-10-30. Consumed by E7KnowledgeEntry. Prose only:
no grader execution, no instrument edit, no lane write outside this wave dir.

**Sources.** Grader S201 = `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`,
sha256 `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (re-hashed at this seat:
the in-repo capture hashes to exactly that, byte-identical to the pin). Its ONE assertion is
**tests/test_outputs.py:25** — `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"` —
over `move = Path("/app/move.txt").read_text().strip().split()` (line 23). Instruction S202 = upstream
`instruction.md` at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, sha256
`6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` (re-fetched at this seat: matches
the S202 row's pin byte-for-byte); it is one line — "The file chess_board.png has an image of a chess
board. It is currently white to move. Write the best move for white to play to /app/move.txt in the
form [src][dst], for example, e2e4 or h1h8. If there are multiple winning moves, print them all, one
per line." Case table = the frozen 12 rows in the wave spec
(`.ufo/waves/round-55/w1-dispatch.json:783`, E5ChessProbe); cross-check:
`plans/round55_c3_chess_probe.py:56-78` (landed 12:28) reproduces all 12 names, byte strings and
predictions verbatim.

**Requirement atoms (quoted from S202).** R1 board — "The file chess_board.png has an image of a chess
board. It is currently white to move." R2 path — "Write the best move for white to play to
/app/move.txt" R3 form — "in the form [src][dst]" R4 examples — "for example, e2e4 or h1h8" R5 all
winners — "If there are multiple winning moves, print them all" R6 layout — "one per line". Two
standing mismatches: the grader never opens `chess_board.png`, so **R1 is untested by every case**;
and the grader hardcodes the answer pair {g2g4, e2e4} — it never checks legality, it is *stricter*
than the instruction on case and digit width and *looser* on line layout (R6 is never enforced).

## The 12 cases

### 1. both-lowercase-two-lines — `g2g4\ne2e4\n` — predicted PASS
- **Requirement:** R5+R6 "print them all … one per line" — both winning moves, one per line, lowercase ASCII; satisfies R2–R6 as written (the canonical answer).
- **Grader line:** `tests/test_outputs.py:25` over `move = …read_text().strip().split()` (:23).
- **Why PASS:** `strip()` eats the trailing newline → `split()` → `['g2g4','e2e4']` → `sorted()` == `sorted(["g2g4","e2e4"]` → assertion holds → exit 0.
- **If FAIL:** the pipeline, not the grader, is broken (capture ≠ pinned bytes, or `/app/move.txt` unbound) — this is the battery's positive control and must PASS.
### 2. both-space-separated — `g2g4 e2e4` — predicted PASS
- **Requirement:** R6 "one per line" — **violates R6 as instruction text** (both moves on one line) yet is accepted: `split()` is whitespace-agnostic, so line layout is not score-critical.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why PASS:** `strip().split()` → `['g2g4','e2e4']` → sorted multisets equal → exit 0.
- **If FAIL:** the grader would have to enforce line structure — impossible from :23/:25; it would mean a test file other than the capture was executed (identity break, kill rule (c)).
### 3. reversed-order — `e2e4 g2g4` — predicted PASS
- **Requirement:** R5/R6 — the instruction fixes no order ("print them all, one per line"), so the grader must be order-blind; the case fixes the reverse order.
- **Grader line:** `tests/test_outputs.py:25` (`sorted()` on both sides).
- **Why PASS:** tokens `['e2e4','g2g4']` → sorted `['e2e4','g2g4']` == target → exit 0.
- **If FAIL:** the probe compared token *order* — a lane-side reimplementation of the assertion, i.e. an oracle defect, not a grader finding.
### 4. single-move-only — `g2g4\n` — predicted FAIL
- **Requirement:** R5 "print them all" — **violated**: only one of the two winning moves. It exposes the singular/plural seam: the instruction says "the best move", so an agent that finds one mate obeys R2 and still fails.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** tokens `['g2g4']` → sorted length 1 vs 2 → assertion false → `AssertionError` → exit 1.
- **If PASS:** the grader gives partial credit — contradicting S201's "no partial credit" and "full-multiset equality".
### 5. uppercase-white — `G2G4\ne2e4\n` — predicted FAIL
- **Requirement:** R3 "in the form [src][dst]" — **violated in the grader's exact-literal sense**: the instruction never states case, the grader compares raw code points.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** token `'G2G4'` != `'g2g4'` → sorted lists differ → `AssertionError` → exit 1.
- **If PASS:** the grader case-folds — contradicting S201's "no case or unicode normalization".
### 6. extra-decoy-move — `g2g4\ne2e4\na2a3\n` — predicted FAIL
- **Requirement:** R5 "print them all" — **violated**: a third token. `a2a3` is a legal pawn move that is not a mate; the grader has no legality notion, only cardinality.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** tokens `['g2g4','e2e4','a2a3']` → sorted length 3 vs 2 → `AssertionError` → exit 1.
- **If PASS:** the grader used membership rather than full multiset equality — the exact class confusion with r45's line-split membership F1.
### 7. duplicate-move — `g2g4\ne2e4\ne2e4\n` — predicted FAIL
- **Requirement:** R5 "print them all" — **violated**: a repeat of one winning move is not "all winning moves"; the multiset is long by one `e2e4`.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** sorted `['e2e4','e2e4','g2g4']` != `['e2e4','g2g4']` → `AssertionError` → exit 1.
- **If PASS:** the grader compared *sets* — under set semantics this case passes, contradicting "full-multiset equality".
### 8. whitespace-padded — `  g2g4   e2e4  \n\n` — predicted PASS
- **Requirement:** R6 — **violates R6 as instruction text** (both moves on one line, plus leading/trailing padding and a blank line) and is accepted: only the token multiset is score-critical.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why PASS:** `strip()` removes the leading spaces and the trailing run including the blank line, `split()` collapses the interior run → `['g2g4','e2e4']` → exit 0.
- **If FAIL:** the probe used a stricter parser than the captured :23 — it did not execute the pinned assertion.
### 9. empty-file — `` — predicted FAIL
- **Requirement:** R2 "Write the best move … to /app/move.txt" — **violated**: the file exists but nothing was written; R5 is violated too (no winning move at all).
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** `read_text()` → `''` → `strip()` → `''` → `split()` → `[]` → `sorted([])` != `['e2e4','g2g4']` → `AssertionError` → exit 1.
- **If PASS:** an empty submission scores 1 — the grader is vacuous; it would also mean the probe called a different function.
### 10. crlf-line-endings — `g2g4\r\ne2e4\r\n` — predicted PASS
- **Requirement:** R6 — the moves are still laid out one per line; only the newline *style* changes, and the instruction is silent on style.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why PASS (two independent reasons):** `read_text()` opens in text mode with universal-newline translation, so `\r\n` → `\n` (verified locally: the text reads back `'g2g4\ne2e4\n'`); and even without it `split()` treats `\r` as whitespace. Tokens `['g2g4','e2e4']` → exit 0.
- **If FAIL:** the read used `splitlines()`-style or binary semantics — contradicting `read_text()` at :23.
### 11. instruction-example-h1h8 — `h1h8\ne2e4\n` — predicted FAIL
- **Requirement:** R4 "for example, e2e4 or h1h8" — **violated in content**: `h1h8` is the instruction's own example token, form-valid under R3 but not one of the two accepted answers. The case separates *form* (satisfied) from *answer set* (violated): the grader hardcodes the pair, it does not check the form.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** sorted `['e2e4','h1h8']` != `['e2e4','g2g4']` → `AssertionError` → exit 1.
- **If PASS:** the grader accepts any well-formed pair of squares — contradicting the S201 anchor quote and S202's "the grader hardcodes the two-move pair".
### 12. fullwidth-unicode-digit — `g\uff12g4\ne2e4\n` — predicted FAIL
- **Requirement:** R3 "in the form [src][dst]" — **violated**: the "2" is U+FF12 FULLWIDTH DIGIT TWO, a different code point that renders like `2`; the instruction shows ASCII examples only, so the grader is stricter than the text here.
- **Grader line:** `tests/test_outputs.py:25`.
- **Why FAIL:** U+FF12 is not whitespace (`'\uff12'.isspace()` is False), so the token stays `'g\uff12g4'` ≠ `'g2g4'` → `AssertionError` → exit 1.
- **If PASS:** the grader applied Unicode normalization (NFKC-style) — contradicting "no case or unicode normalization".

## Requirement map (every violating case listed, Q28-shaped)

| Requirement | Cases exercising it | Violating cases (grader-observable) | Instruction-only violations the grader forgives |
|---|---|---|---|
| R1 board image | none | none — untestable: the grader never opens `chess_board.png` | — |
| R2 write to `/app/move.txt` | all 12 (the path is hardcoded at :23) | 9 (nothing written) | — |
| R3 form `[src][dst]` | 1,2,3,4,6,7,8,10,11 (form-valid) | 5 (case), 12 (digit width) | — |
| R4 examples `e2e4` / `h1h8` | 1–3,5–8,10,12 carry `e2e4` | 11 (`h1h8` rejected) | — |
| R5 "print them all" | 1,2,3,8,10 | 4, 6, 7, 9, 11 | — |
| R6 "one per line" | 1,3,4,5,6,7,9,10,11 | none (layout is never enforced) | 2, 8 (one-line layouts, both PASS) |

## Gaps: what this 12-case table still cannot say

- **Chess semantics are untested.** `a2a3` fails only by cardinality; the grader never checks that a token is a legal move, let alone a mate. A chess-correct agent that reads `chess_board.png` and finds one mate also fails (case 4).
- **Untested read paths and separators:** a missing `/app/move.txt` (`FileNotFoundError`, not an `AssertionError` → the instrument scores it SETUP, not FAIL), a wrong path (hardcoded at :23), and non-UTF-8 bytes (decode error → SETUP; the landed instrument pins `LANG`/`LC_ALL=C.UTF-8` and `PYTHONUTF8=1`, which closes that risk on this host); a non-breaking space between the moves is *accepted* by `split()` (verified locally: `'g2g4\xa0e2e4'` → `['g2g4','e2e4']` → PASS) — no case covers that, nor a UTF-8 BOM or a vertical-tab separator.
- **Not established:** task validity, the image's content, model performance, contamination. One task of 89; the graded artefact is an agent-authored token file, not the grader's own output.

## Verification performed at this seat (re-derivation, not a grader run)

All 12 predicted verdicts were re-derived locally from the assertion expression alone
(`sorted(text.strip().split()) == sorted(["g2g4","e2e4"])`, with `read_text()`'s universal-newline
translation applied): 12/12 agree with the frozen predictions. The real bwrap battery was not run here
— that is E5/E6's — so no `observed=` value in this file is claimed from execution.
