# Q10/Q13 second-seat re-read — S201 grader, S202 instruction (kengaku round 55)

seat: R3ChessSourcesReopen (leaf, re-open only; no fixes). Date: 2026-10-30.
Frozen reference: `plans/round-55-claims.md` (commit 80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb),
Gate block in `corpus/lessons/round-55.md`. Pin: 2fd12b88aafdd04a52c298e3940bcb189f9766d6
(harbor-framework/terminal-bench-2). Both URLs re-fetched read-only (GET) this seat, from
scratch dir `/fast/scratch/hyaku/kengaku-r55/R3ChessSourcesReopen/` (deleted after the re-read).

## S201 — grader — tests/test_outputs.py

- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py (GET 2026-10-30, exit 0)
- Located quote (Gate): `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`
- (1) Verbatim at named location: **AGREE.** Fetched file line 25 (1-indexed) reads
  `    assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`; the quote is the
  line content verbatim after the 4-space indent. It is the only assertion in the file's
  only test (`test_move_correct`).
- (2) sha256 matches freeze pin: **AGREE.**
  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` measured on the
  re-fetched bytes; equals the Gate pin and the R55-C3 claim text. The in-repo capture
  `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` hashes to the
  same value and `diff` against the fresh fetch is empty (byte-identical, kill rule (c)
  surface clean).
- (3) Quote ≤ 25 words: **AGREE.** 8 words by whitespace split.
- (4) `teaches` claim follows from the quote: **AGREE.** Cell: "executed scoring predicate
  of this task's grader for its own behaviour". The quote is the file's single scoring
  assertion (sorted token-multiset equality against both mate-in-one moves); the claim
  follows directly.

Row verdict: **AGREE with admit A** (all four checks pass).

## S202 — instruction — instruction.md

- URL: https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md (GET 2026-10-30, exit 0)
- Located quote (Gate): `If there are multiple winning moves, print them all, one per line.`
- (1) Verbatim at named location: **AGREE.** The fetched instruction.md is a single line;
  line 1 is
  `The file chess_board.png has an image of a chess board. It is currently white to move. Write the best move for white to play to /app/move.txt in the form [src][dst], for example, e2e4 or h1h8. If there are multiple winning moves, print them all, one per line.`
  — the quote is a verbatim substring of line 1.
- (2) sha256 matches freeze pin: **AGREE.**
  `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` measured on the
  re-fetched bytes; equals the Gate pin.
- (3) Quote ≤ 25 words: **AGREE.** 12 words by whitespace split.
- (4) `teaches` claim follows from the quote: **AGREE.** Cell: "maintainer requirement the
  grader is mapped against". The quote is the maintainer-stated requirement to emit all
  winning moves; the S201 grader's multiset assertion is exactly this requirement
  operationalised (both `g2g4` and `e2e4` must appear). The mapping claim follows.

Row verdict: **AGREE with admit A** (all four checks pass).

## Observations (findings, not fixes — sibling/L1 files untouched)

- O1: Uncommitted `corpus/SOURCES.md` row S201 truncates the Gate quote to
  `assert sorted(move) == sorted(["g2g4", "e2e4"])` and labels it "(6 words)"; the
  whitespace-split count of that truncated quote is 5, and the full Gate quote (with
  `, "File is wrong"`) is 8 words. Either way the ≤25-words rule holds, so this is a
  label/consistency nit in a sibling-owned file, recorded only.
- O2: Uncommitted `corpus/SOURCES.md` row S202 labels its quote "(12 words)" — matches
  this seat's count (12). Consistent.
- O3: `corpus/knowledge/tb2-chess-best-move-grader.md` (the entry the Gate says cites
  both rows) does not exist yet at re-read time — expected mid-wave state (entry is a
  sibling/L1 deliverable under R55-C3 after-state); recorded for the closure checklist.
- O4: Amendment-A1 check: in-repo `corpus/evidence/round52/graders/chess-best-move/tests/test.sh`
  sha256 is `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`, equal to the
  Gate's stated S109 runner sha — consistent with the "dropped as duplicate" ruling.
- O5: No other row's status/recheck/used-by cells were inspected for change this seat;
  flip-check remains the closure's duty.
