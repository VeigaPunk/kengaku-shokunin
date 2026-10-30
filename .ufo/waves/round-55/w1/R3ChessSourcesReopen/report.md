# R3ChessSourcesReopen — seat report (kengaku round 55, w1)

Seat: R3ChessSourcesReopen (leaf; no subagent dispatch). Date: 2026-10-30.
Assignment: Q10/Q13 second-seat re-read of the round's two new sources (S201 grader,
S202 instruction) at TB2 pin 2fd12b88aafdd04a52c298e3940bcb189f9766d6.

## What I ran

1. Read the freeze: `plans/round-55-claims.md` (commit 80afa613…) and the Gate block in
   `corpus/lessons/round-55.md`. Exit 0.
2. `mkdir -p /fast/scratch/hyaku/kengaku-r55/R3ChessSourcesReopen` — scratch root created. Exit 0.
3. Read-only GETs (authorized: raw.githubusercontent.com):
   - `curl -fsSL --max-time 60 -o s201_test_outputs.py https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/tests/test_outputs.py` — exit 0
   - `curl -fsSL --max-time 60 -o s202_instruction.md .../chess-best-move/instruction.md` — exit 0
4. `sha256sum` on both fetches — both match frozen pins (below). Exit 0.
5. `cat -n` on both fetches — located quotes confirmed verbatim at tests/test_outputs.py:25
   and instruction.md:1. 
6. Python whitespace word counts: S201 quote = 8 words, S202 quote = 12 words (both ≤25).
7. In-repo identity: `sha256sum` of `corpus/evidence/round52/graders/chess-best-move/tests/{test_outputs.py,test.sh}`
   → `a540714e…` and `4770437e…`; `diff` of the capture vs the fresh upstream fetch → empty
   (byte-identical). Exit 0.
8. No installs/upgrades this seat (no tool changes; pacman untouched per host guard).

## Files I wrote

- `.ufo/waves/round-55/w1/R3ChessSourcesReopen/reopen.md` — per-row re-read record (agree/disagree).
- `.ufo/waves/round-55/w1/R3ChessSourcesReopen.md` — scoped findings (Report trailer path).
- `.ufo/waves/round-55/w1/R3ChessSourcesReopen/report.md` — this report.

## Results

- S201 (grader): AGREE with admit A. Quote verbatim at :25; sha256
  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` matches the freeze pin;
  8 words ≤ 25; teaches claim ("executed scoring predicate…") follows (it is the file's only
  assertion in its only test).
- S202 (instruction): AGREE with admit A. Quote verbatim at :1 (single-line file); sha256
  `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` matches the freeze pin;
  12 words ≤ 25; teaches claim ("maintainer requirement the grader is mapped against")
  follows.

## Defects found

- F1 (nit, sibling-owned): uncommitted `corpus/SOURCES.md` S201 row truncates the Gate quote
  and its "(6 words)" label is off by one (5 for the truncated text; full Gate quote is 8).
  Rule holds either way; recorded, not fixed.
- F2 (state note): knowledge entry `corpus/knowledge/tb2-chess-best-move-grader.md` not yet
  present at re-read time (mid-wave; sibling/L1 deliverable). Closure checklist item.
- F3 (positive check): A1 duplicate-drop consistent — captured test.sh sha256 equals the
  S109-held runner `4770437e…`.

## Dead ends

None. Both URLs fetched on first attempt; pins matched; no retry needed.

## Cleanup

Scratch dir `/fast/scratch/hyaku/kengaku-r55/R3ChessSourcesReopen` deleted after receipts were
copied into the seat's wave outputs (rm -rf, verified).
