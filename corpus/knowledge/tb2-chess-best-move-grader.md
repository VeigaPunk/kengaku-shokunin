source: S201 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py — the decisive assert at `tests/test_outputs.py:25` (`assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`) and the tokenization at `:23` (`move = move_file.read_text().strip().split()`), commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, sha256 `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`, accessed 2026-10-30
source: S202 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md — the one-line requirement at `instruction.md:1` ("If there are multiple winning moves, print them all, one per line."), same commit, sha256 `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a`, accessed 2026-10-30
source: S109 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh — the reward mapping at `tests/test.sh:26` ("echo 1 > /logs/verifier/reward.txt"), same commit, sha256 `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`, accessed 2026-10-30 — the chess-best-move `tests/test.sh` is byte-identical to this pinned regex-log runner (amendment A1, claims 2026-10-30, both files sha256 `4770437e…`), so no new SOURCES row was opened and this entry cites S109 for runner semantics
verified-at: 2026-10-30 — probe receipt `corpus/evidence/round55/chess-best-move-probe.txt` (sha256 `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca` at writing) and the in-repo captures named above
recheck: 180d — from the lane root re-run `python3 plans/round55_c3_chess_probe.py --lane . --work <scratch-dir> --receipt corpus/evidence/round55/chess-best-move-probe.txt` and require the byte-identical predicate block (`cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`, receipt sha256 `de082669…`); re-fetch the three pinned URLs at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and compare sha256 against the pins above; any probe, digest or receipt drift supersedes this entry
writer: E7KnowledgeEntry (round 55, wave 1) — second-seat re-read: pending (R3)

# Terminal-Bench 2.0 task grader, read and executed: `chess-best-move`

## Summary

At terminal-bench-2 commit `2fd12b88`, the `chess-best-move` task's whole score is one pytest
assertion — order-insensitive full-multiset equality between the whitespace-split tokens of the
agent-written `/app/move.txt` and the hard-coded pair `["g2g4", "e2e4"]` (`test_outputs.py:23,25`)
— mapped by `tests/test.sh` to a single-bit reward (S109). Offline execution of the captured
grader function against a frozen table of 12 synthetic `move.txt` artefacts matched every
prediction written from the static reading before the first run:
`cases=12 observed_pass=5 observed_fail=7 mismatches=0`
(`corpus/evidence/round55/chess-best-move-probe.txt`). The graded artefact class is new to this
lane's executed set: an agent-authored **token file** judged by full-multiset equality — where
round 45's `password-recovery` judged an agent-authored line file by membership.

## Source labels

S201 is the benchmark maintainers' own grader file: primary for *what the grader checks* and a
self-report for everything else — the docstring's "checkmate-in-one" reading
(`test_outputs.py:10-19`) is the authors' statement about their own position; no board was read
this round. S202 is the maintainers' own one-line requirement text the grader is mapped against.
S109 is the maintainers' runner, held since round 36; per amendment A1 the chess-best-move
`tests/test.sh` is byte-identical to it, so the entry cites S109 for runner semantics instead of a
duplicate row. The probe receipt is the lane's own re-runnable gate output (tier A for its own
scope: these 12 artefacts against this capture under the host Python, inside a bubblewrap sandbox
with the capture bound read-only at `/tests`). Instrument provenance: the probe was built and run
by sibling seats of round 55 wave 1 (`plans/round55_c3_chess_probe.py`, frozen with the claims at
commit `80afa613`); this entry copies the receipt without re-deriving it.

## What the grader checks (static reading, `test_outputs.py`)

| Step | Mechanism | Lines |
|---|---|---|
| File | `/app/move.txt` is read as text, then `.strip().split()` — whitespace runs collapse, and surrounding whitespace and blank lines carry no information | :23 |
| Oracle values | the literal two-element list `["g2g4", "e2e4"]`, hard-coded in the test file | :25 |
| Decision | `sorted(move) == sorted(["g2g4", "e2e4"])` — both sides sorted, then full list equality; the message on mismatch is `"File is wrong"` | :25 |

The authors' own description of the intended position (self-report, labelled as such): both
example moves are claimed to be checkmate-in-one ("- g2g4: Pawn move that delivers checkmate",
`- e2e4: Alternative pawn move that also delivers checkmate`, `test_outputs.py:14-15`), and the
test "expects the move.txt file to contain both valid checkmate moves in any order"
(`test_outputs.py:17`).

## Evidence table (12 frozen cases, receipt-verbatim)

Each row is one frozen case of `plans/round55_c3_chess_probe.py` (case bytes and predictions
frozen with the round-55 claims at `80afa613`); `Predicted` and `Observed` are copied verbatim
from the receipt, which records `CASE <name> predicted=<P|F> observed=<P|F> rc=<n>` per case
(exit 0 = P; nonzero exit carrying `AssertionError` = F). No prediction or verdict below is
re-derived by this entry. Case bytes are Python-escaped literals of the file contents.

| # | Case | Frozen `move.txt` bytes | Predicted | Observed (receipt) |
|---|---|---|---|---|
| 1 | `both-lowercase-two-lines` | `g2g4\ne2e4\n` | P | P (rc=0) |
| 2 | `both-space-separated` | `g2g4 e2e4` | P | P (rc=0) |
| 3 | `reversed-order` | `e2e4 g2g4` | P | P (rc=0) |
| 4 | `single-move-only` | `g2g4\n` | F | F (rc=1) |
| 5 | `uppercase-white` | `G2G4\ne2e4\n` | F | F (rc=1) |
| 6 | `extra-decoy-move` | `g2g4\ne2e4\na2a3\n` | F | F (rc=1) |
| 7 | `duplicate-move` | `g2g4\ne2e4\ne2e4\n` | F | F (rc=1) |
| 8 | `whitespace-padded` | `  g2g4   e2e4  \n\n` | P | P (rc=0) |
| 9 | `empty-file` | `` (zero bytes) | F | F (rc=1) |
| 10 | `crlf-line-endings` | `g2g4\r\ne2e4\r\n` | P | P (rc=0) |
| 11 | `instruction-example-h1h8` | `h1h8\ne2e4\n` | F | F (rc=1) |
| 12 | `fullwidth-unicode-digit` | `g２g4\ne2e4\n` (U+FF12) | F | F (rc=1) |

Receipt predicate block, verbatim:

```
cases=12 observed_pass=5 observed_fail=7 mismatches=0
PREDICATE R55-C3 pass
```

## Mechanism (five properties, each witnessed by receipt cases)

1. **Order-insensitive full-multiset equality over whitespace-split tokens.** `sorted(move) ==
   sorted(["g2g4", "e2e4"])` (`:25`) sorts both sides before comparing, so token order is free:
   `reversed-order` (row 3) passes with the moves on one line in reverse order, and
   `both-lowercase-two-lines` (row 1) passes one-per-line. The split is `str.split()` with no
   arguments (`:23`), so "one per line" is enforced only as a token discipline, never as a line
   discipline.
2. **No case or unicode normalization.** No `upper`/`lower`/`casefold` and no width folding exists
   anywhere in the capture; the comparison is plain string equality. `uppercase-white` (row 5)
   fails because `G2G4 != g2g4`, and `fullwidth-unicode-digit` (row 12) fails because U+FF12
   FULLWIDTH DIGIT TWO is not ASCII `2` — an artefact in fullwidth form scores 0.
3. **strip+split tolerance.** `.strip()` eats the surrounding run and `.split()` collapses
   interior whitespace runs (spaces, blank lines, and `\r\n` line endings, which are whitespace
   to `split()` regardless of the text-mode newline translation), so `both-space-separated` (row
   2), `whitespace-padded` (row 8) and `crlf-line-endings` (row 10) all pass.
4. **Duplicates and extras break equality — no partial credit.** Full-multiset equality requires
   exactly the two-element multiset: `single-move-only` (row 4, one of two) fails,
   `extra-decoy-move` (row 6, a third token) fails, and `duplicate-move` (row 7,
   `g2g4 e2e4 e2e4` — sorted length 3 against 2) fails. `empty-file` (row 9) fails because
   `"".strip().split()` is `[]`, not the two-move multiset. One right move plus noise is a fail,
   not half a pass.
5. **The instruction's example literal `h1h8` is not a winner per the grader pair.** The
   instruction states the format as "[src][dst], for example, e2e4 or h1h8" (`instruction.md:1`);
   the grader hard-codes `{g2g4, e2e4}` and nothing else. `instruction-example-h1h8` (row 11) —
   a legal-format artefact containing `h1h8` plus the winning `e2e4` — fails: of the
   instruction's two example literals, `e2e4` happens to be a graded winner and `h1h8` is not, and
   the grader cannot tell an example from an attempt.

## What `test.sh` does with the outcome (S109)

`tests/test.sh` runs the one test file under `uvx -p 3.13` with
`pytest==8.4.1`/`pytest-json-ctrf==0.3.5`, writing a CTRF report, then maps the pytest exit status
to the reward byte-for-byte as the regex-log runner already held:

```
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
```

(`test.sh:25-29`; the probe executes the grader function directly, not this script.) The score is
therefore single-bit: one assertion, one comparison, reward 1 or 0, with no partial-compliance
gradation — the pass/fail texture the 12 cases exhibit collapses to one bit at the reward file.

## Negative space

This entry does **not** establish:

- **chess correctness** — whether `g2g4`/`e2e4` are truly the winning moves in the pictured
  position; the docstring's mate-in-one reading (`test_outputs.py:10-19`) is the authors'
  self-report, and no board image was parsed and no engine consulted this round;
- **task validity** — no run of the task image, no agent, no trajectory;
- **the image's content** — `chess_board.png` was never inspected; the probe feeds synthetic
  artefacts to the grader, it never solves the task;
- **model or agent performance** — the 12 cases are lane-authored end states, not submissions;
- **contamination** — the capture carries the TB2 canary banner (`test_outputs.py:2`); the entry
  is a digest-pinned re-execution record, not a contamination measurement;
- **anything about the other TB2 tasks** — this is one task of 89 (the 13th grader this lane has
  executed offline; the frontier count moves 12 → 13 of 89, nothing more);
- **the runner's consumption** — S109 covers the script's own reward mapping; how Harbor consumes
  `reward.txt` is `benchmark-verifier-execution-model.md`'s scope, not this entry's.

**Class note (the r45 distinction).** The graded artefact here is an agent-authored **token file**
judged by full-multiset equality: exactly the multiset `{g2g4, e2e4}` passes, and every case with
a different multiset — missing, extra, duplicated, case-shifted, width-shifted — fails. Round 45's
`password-recovery` graded an agent-authored **line file** by membership: the answer's presence as
one line among arbitrary others sufficed, and 1000 decoys around it still passed. The two entries
bound the token-file grader designs this lane has executed: membership (partial credit possible)
versus full-multiset equality (none).

**Falsifier.** This entry is falsified if (a) a re-fetch of the three pinned URLs yields bytes
whose SHA-256 differs from the pins in the `source:` lines; (b) a fresh run of
`plans/round55_c3_chess_probe.py --lane .` prints anything other than the byte-identical receipt
block above — in particular if any of rows 1, 2, 3, 8, 10 is observed `F`, or any of rows 4, 5, 6,
7, 9, 11, 12 is observed `P`; (c) the captured grader is shown to compare by anything other than
`strip().split()` tokens against the literal pair `["g2g4", "e2e4"]` at `test_outputs.py:23,25`,
or to read a file other than `/app/move.txt`; (d) the chess-best-move `tests/test.sh` is shown to
differ from S109's pinned bytes; or (e) `instruction.md` is shown to name `h1h8` as a winning
move (it does not — it is a format example only).

## Connections

- `[[benchmark-verifier-execution-model]]` — that entry settles *where* a TB2 verifier runs
  (Harbor's default shared mode) and what the harness restores; this entry settles *what one TB2
  verifier decides*; S109's `test.sh` is the bridge both entries cite (pytest exit →
  `reward.txt`), from the same repository at the same pin as its S100.
- `[[tb2-password-recovery-grader]]` (round 45, with its round-46 errata) — the prior executed
  exemplar of an agent-authored answer file, of the line-split **membership** class; this entry is
  the **full-multiset equality** class, so the pair records both designs the lane has executed and
  why "the agent wrote a file" under-determines what a grader will reward.

## Admission state (Q13/Q14)

`second-seat re-read: pending (R3)` — admission is the L1's call; no second-seat report is cited
by this entry.
