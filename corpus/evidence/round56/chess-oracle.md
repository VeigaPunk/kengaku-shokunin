# chess-best-move maintainer oracle — round 56 (2026-10-31)

author: kengaku L1 (round 56, Windows host). Claim: R56-C3 (`plans/round-56-claims.md`,
freeze commit `8db18e23`). Sources: S203 (task.toml) and S204 (solution/solve.sh), opened
2026-10-31 at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` via `curl` GET of the pinned raw
URLs. No upstream bytes are committed in this round (the r52 GH013 push-protection L0 stays
unanswered), so this note records the fetched identity instead:

| file | sha256 (fetched 2026-10-31, `sha256sum` over the curl bytes) | bytes |
|---|---|---|
| `chess-best-move/task.toml` | `d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e` | 849 |
| `chess-best-move/solution/solve.sh` | `53b5c5e2278ca915b0930eedfd44565ca84ef21c7346fd6601434484cf76151f` | 7555 |
| `chess-best-move/tests/test_outputs.py` (re-fetched same pin as identity cross-check) | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` | — |

The third row re-derives the pin already held by S201 and
`plans/round55_c3_chess_probe.py` (`GRADER_SHA256`), so the oracle was read from the same
commit the grader was captured from.

## What the oracle says

`solution/solve.sh` embeds a python-chess program (`solve.py`, heredoc at `:14`) that:

1. reads the board image, reconstructs a FEN (`puzzle_to_fen`, `:58-144`);
2. walks **every legal move**, pushes it, and appends its UCI when the resulting position is
   checkmate — `for move in board.legal_moves:` (`:180`), `if board.is_checkmate():`
   (`:185`), `best_moves.append(move.uci())` (`:186`);
3. if at least one mating move exists, returns **all of them** (`if best_moves: ... return
   best_moves`, `:192-194`) — Stockfish is only consulted when none exists (`:198-207`);
4. writes the returned moves to `/app/move.txt` joined by newlines
   (`f.write("\n".join(best_moves))`, `:232`).

`task.toml` declares the same plural behaviour the oracle implements: `description`
(`:6`) — "Evaluates the agent's ability to analyze a chess position from an image, use a
chess engine to find the best move(s), and handle multiple valid solutions."

## Mapping to the grader (S201)

The executed scoring predicate at `tests/test_outputs.py:25` is
`assert sorted(move) == sorted(["g2g4", "e2e4"])` over `Path("/app/move.txt").read_text().strip().split()`
(`:23-24`). The oracle's all-mating-moves output is exactly the multiset that assertion
rewards for this task's fixed position: the reference run emits `{g2g4, e2e4}` (both moves
mate), which the grader accepts in any order, with any whitespace framing, and rejects under
any superset, subset, duplication, case or width variation — the twelve-case probe table
(`corpus/evidence/round55/chess-best-move-probe.txt`, `cases=12 observed_pass=5
observed_fail=7 mismatches=0`) is consistent with the oracle's behaviour line by line: the
five predicted passes are exactly the files a full-multiset grader accepts, and the oracle
would never produce the seven predicted-fail artefacts (it never emits one move when two
mate, never uppercases, never appends a third token, never duplicates).

The oracle is therefore a second primary source (maintainer code) for the reading this
lane's round-55 admission rested on the grader alone: "multiple winning moves" means the
grader's expected answer is the complete mating-move set, and the two-move literal in the
assertion is the expected multiset for this position, not a membership example.

## Kill rule status (R56-C3)

(a) the oracle does not contradict the grader's expected multiset — confirmed above;
(b) both upstream identity checks hold at the pin (table above, plus the S201 cross-check);
(c) the fleet census verdict at round end is recorded in the round report. No kill fired at
write time.
