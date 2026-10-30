# vacuity.md — SC5VacuityRead — independent semantic read of the chess-best-move grader

Round 55 w1, 2026-10-30. Second pair of eyes beside the entry
(`corpus/knowledge/tb2-chess-best-move-grader.md`, owned by the entry seat) — the Q13/Q14
second-seat re-read on record for R55-C3. Read-only seat: nothing outside this wave dir was
written.

## Inputs (verified before reading)

| Artefact | Source | sha256 | Verified |
|---|---|---|---|
| `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` (25 lines) | lane capture | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` | matches frozen pin (claims file, R55-C3) |
| `corpus/evidence/round52/graders/chess-best-move/tests/test.sh` (29 lines) | lane capture | `4770437e…716e6c334` (SHA256SUMS:18-19) | byte-identical to held S109 regex-log runner per amendment A1 |
| upstream `instruction.md` @ pin `2fd12b88` (260 bytes, single line) | fetched raw.githubusercontent.com | `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` | matches round-55 lesson Gate pin |
| upstream `environment/make.py` @ pin (122 lines) | fetched | not pinned by the round; used only for provenance of the board image | — |
| upstream `environment/Dockerfile` @ pin | fetched | not pinned; `RUN python3 make.py` then `rm make.py` | — |

## 1. Every pass/fail semantic derivable from the captured grader

One test function, no fixtures, no parametrization — the whole task reduces to one binary
assertion:

- **`test_outputs.py:9`** — single grader `test_move_correct()`; nothing else is scored.
- **`test_outputs.py:22`** — hard-coded absolute `Path("/app/move.txt")`. cwd-independent;
  the agent must write exactly there. Missing file → `FileNotFoundError`; a directory at
  that path → `IsADirectoryError`; chmod 000 → `PermissionError`. All three are exceptions
  inside the test body → pytest 8.4.1 reports FAILED (not fixture ERROR), runner
  (`test.sh:22-28`) writes reward 0 — verdict-equivalent to an assertion failure, but the
  output surface is a traceback, not the `"File is wrong"` message.
- **`test_outputs.py:23`** — `move_file.read_text().strip().split()`:
  - `read_text()` has **no explicit encoding** → interpreter-locale default decode. The
    frozen probe pins `LANG=C.UTF-8, PYTHONUTF8=1` (`plans/round55_c3_chess_probe.py` ENV),
    making it deterministic UTF-8 *inside the probe*; in the wild the same bytes can decode
    differently under another locale. Non-UTF-8 bytes → `UnicodeDecodeError` → F.
    Universal-newline translation applies (`\r\n` → `\n`) before strip/split.
  - `.strip()` is **dead code**: no-arg `split()` already drops all leading/trailing
    whitespace runs. Verified empirically on padded samples (`strip().split() ==
    split()` always). Harmless vacuity in the template.
  - `.split()` with no args splits on **runs of any Unicode whitespace** and discards empty
    tokens. Consequences (each empirically confirmed, §2): space, tab, blank lines, CRLF —
    all equivalent separators; NBSP `\xa0`, VT `\x0b`, U+2028, U+2029, ASCII `\x1c`-`\x1f`
    also separate (PASS separators); zero-width space `\u200b` and NUL do **not** (they glue
    into the token → FAIL).
- **`test_outputs.py:25`** — `assert sorted(move) == sorted(["g2g4", "e2e4"])`:
  - **Order-insensitive full-multiset equality** over exactly two required tokens. Order
    free; exactly-2 enforced: `sorted()` on both sides makes it multiset comparison, so
    duplicates (`e2e4` twice) fail, extras fail, one-of-two (partial answer) fails.
  - **Token equality is exact and code-point-wise**: case-sensitive (`G2G4` fails); no
    digit-width normalization (`g\uff12g4`, FULLWIDTH TWO, fails); homoglyphs fail
    (Cyrillic `\u0433` vs ASCII `g`); punctuation glues (`g2g4.` fails); coordinate form
    only (`g4`, `g2-g4`, `g4#` all fail); a UTF-8 BOM prefixes the first token
    (`\ufeffg2g4` fails).
  - Empty file → `[]` → fail with `"File is wrong"`; whitespace-only file → also `[]` → F
    (same observable, exercises strip+split on nonempty input).
  - Failure message is the literal `"File is wrong"`; nothing else in the file keys on
    output content.
- **`test_outputs.py:10-20` (docstring)** — no runtime effect; it is the authors'
  self-report that the position's mate-in-one set is exactly `{g2g4, e2e4}` (S201 admits it
  as "the authors' self-report"). The assertion never verifies the chess claim.
- **Runner (`test.sh:18-22`)** — `uvx -p 3.13 -w pytest==8.4.1 … pytest --ctrf …
  /tests/test_outputs.py -rA`; `test.sh:26/28` reward 1 iff pytest exit 0. Grader sees only
  `/tests/test_outputs.py`; the answer file is read from `/app` at test time.

## 2. Empirical probe (local evaluation of the exact L23-25 expression)

Ran in seat scratch (exit 0), same expression, bytes → decode as UTF-8 per the probe's
frozen ENV:

| Candidate `move.txt` | tokens after `strip().split()` | verdict |
|---|---|---|
| `g2g4\ne2e4\n` | `['g2g4','e2e4']` | P |
| `g2g4 e2e4` (same line) | same | P |
| tabs + blank lines | same | P |
| CRLF | same | P |
| NBSP `\xa0` separator | same | P |
| U+2028 / U+2029 separators (codepoint-verified in input) | same | P |
| ASCII FS `\x1c`, VT `\x0b` separators | same | P |
| `g2g4\u200be2e4` (zero-width space) | one glued token | F |
| UTF-8 BOM prefix (`\xef\xbb\xbf`) | `['\ufeffg2g4','e2e4']` | F |
| NUL byte glued | `['g2g4\x00','e2e4']` | F |
| `g2g4.` / `e2e4.` | punctuation glued | F |
| `1. g2g4` / `2. e2e4` | 4 tokens | F |
| `g4` / `e4` (SAN), `g2-g4`, `g4#` | exact-token mismatch | F |
| Cyrillic `\u04332\u04334` homoglyph (codepoint-verified) | mismatch | F |
| `G2G4` (either move uppercased) | mismatch | F |
| fullwidth `g\uff12g4` | mismatch | F |
| one move only / duplicate / third move | multiset cardinality off | F |
| empty file / whitespace-only | `[]` | F |

Cross-check against the frozen table (`plans/round55_c3_chess_probe.py:54-79`): its 12
predictions agree with every overlapping row above (both-on-two-lines P, space-separated P,
reversed P, padded P, CRLF P, single F, uppercase F, extra F, duplicate F, empty F, h1h8
decoy F, fullwidth F). No conflict found between the frozen table and an independent read.

## 3. Instruction-vs-grader gaps

`instruction.md:1` (the whole instruction, one line): "The file chess_board.png has an image
of a chess board. It is currently white to move. Write the best move for white to play to
/app/move.txt in the form [src][dst], for example, e2e4 or h1h8. If there are multiple
winning moves, print them all, one per line."

1. **The board image the grader never looks at.** The oracle never opens `chess_board.png`
   or any board representation; the expected token pair is a literal in
   `test_outputs.py:25`. The image is PIL-drawn at container build from a FEN hard-coded in
   upstream `environment/make.py:116-119`
   (`r1bq1r2/1p3pp1/p1n1p3/3nPkbP/8/P1N5/1P2QPP1/R1B1K2R w KQ - 0 16`, comment mislabels it
   "Standard starting position"; `Dockerfile` runs `python3 make.py`, then `rm make.py`).
   The entire FEN → mate-set chain is author-asserted (docstring), unobserved by the
   oracle. Residual inconsistency worth on-record: the docstring calls `e2e4` a "pawn
   move", but the FEN's rank 2 (`1P2QPP1`) puts a white **queen** on e2 — under that
   position `e2e4` is a queen move. I make no chess-truth claim either way; kill rule (b)
   correctly scopes the probe's oracle to the captured assertions. The point for the entry:
   the grader's pass set is fixed independently of the image, so an agent can pass without
   ever seeing the board (and the grader cannot tell the difference).
2. **The example literal `e2e4` is half the answer key.** `instruction.md:1`'s "for example,
   e2e4 or h1h8" literally contains one required token. An example-anchored agent (ignore
   board, echo the example) is indistinguishable to the grader from a board-solving agent
   that also found e2e4. (In the FEN, `e2e4`/`h1h8` are both at least *legal* — queen and
   h-file rook — so the examples were plausibly drawn from the real position; `h1h8` is
   nonetheless not in the pass set, and case `instruction-example-h1h8` in the frozen table
   shows a decoy + one real token still fails.)
3. **"one per line" vs `split()`.** The instruction's format guidance is stricter than the
   oracle: any whitespace run separates tokens (same line, tabs, CRLF, blank lines, even
   NBSP/U+2028 — §2). Benign leniency: a non-compliant-but-correct answer passes. The
   converse is *not* lenient: human-ish punctuation ("1. g2g4", trailing periods) fails.
4. **Multiple-winning-moves plural rule.** "print them all" reads as "at least all", but
   the grader enforces **exactly** `{g2g4, e2e4}` — a truthful agent printing a third
   mate-in-one (if one existed) fails, and the grader has no mechanism to check the
   mate-claim itself. "Winning" is defined by fiat in `test_outputs.py:25`.
5. **Coordinate form is implied, not enforced charitably.** `[src][dst]` plus examples pins
   the token shape; any SAN/UCI-hyphen/mate-suffix variant fails (§2). Consistent, but the
   grader allows zero formatting charity beyond whitespace.

## GAPS: what a 12-case table could still mispredict

The frozen table (probe:54-79) is internally consistent with the grader; these classes are
outside it — a reader generalizing from 12 cases could still mispredict:

1. **BOM-prefixed file** (`\xef\xbb\xbfg2g4\ne2e4`) → **F** despite correct content
   (BOM is not whitespace; glues to the first token). A "text looks right ⇒ pass" intuition
   breaks; editors/PowerShell redirects emit BOMs.
2. **Exotic Unicode whitespace separators pass**: NBSP U+00A0, U+2028, U+2029, VT `\x0b`,
   `\x1c`-`\x1f` all separate tokens → **P**. The table only shows ASCII space/tab/newline;
   the true separator class is "Unicode whitespace" (`str.isspace`), much wider.
3. **Zero-width space U+200B is the mirror trap** → **F** (glued token). Without an
   explicit probe, NBSP-passes/ZWSP-fails is unpredictable a priori.
4. **NUL byte** in or beside a token → **F** (`'g2g4\x00' ≠ 'g2g4'`); text mode does not
   reject NUL, it just poisons the token.
5. **Punctuation/numbering tolerance is zero** (`g2g4.`, `1. g2g4`) → **F**; nothing in the
   table shows the grader is punctuation-hostile.
6. **Coordinate-form exactness**: SAN (`g4`), hyphenated (`g2-g4`), mate-suffixed (`g4#`)
   → **F**; the table's h1h8 row shows wrong-move fails but not wrong-*notation*-fails.
7. **Homoglyphs and case**: Cyrillic `\u0433` for `g` → **F**; `E2E4` uppercase on the
   *second* move also F (table uppercases only the first move — same class, untested cell).
8. **Whitespace-only file** → F with the same `[]` observable as empty-file; table covers
   empty only.
9. **Failure-class differences a verdict table flattens**: missing file
   (`FileNotFoundError`), directory at path (`IsADirectoryError`), non-UTF-8 bytes
   (`UnicodeDecodeError`) are all verdict-F like assertion failures, but surface as
   tracebacks, not `"File is wrong"` — indistinguishable in reward, distinguishable in
   output text.
10. **Encoding is env-dependent in the wild**: `read_text()` (L23) pins no encoding; the
    probe's frozen `LANG=C.UTF-8`/`PYTHONUTF8=1` makes UTF-8 deterministic *inside the
    probe*, but the grader itself would decode differently under another locale — the 12
    cases inherit the probe's env, not the grader's.
11. **Chess-truth is outside every case**: no case can detect that `{g2g4, e2e4}` is wrong
    *as chess* (docstring self-report; FEN renders a position where the docstring's
    "pawn move e2e4" label conflicts with Qe2). Kill rule (b) scopes the oracle to the
    assertions — correctly — but a 12-case table therefore says nothing about whether the
    task's answer key is chess-correct.

No defect found in the captured grader, the runner, or the frozen case table's predictions;
all 12 frozen predictions agree with this independent read. Findings above are additive
semantics and instruction-vs-grader gaps, not counter-evidence to R55-C3.
