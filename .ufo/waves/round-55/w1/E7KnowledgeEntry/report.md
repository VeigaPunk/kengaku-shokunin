# E7KnowledgeEntry — round 55, wave 1 — seat report

**Seat item:** R55-C3 knowledge entry `corpus/knowledge/tb2-chess-best-move-grader.md`.
**Verdict:** DONE — entry written and self-checked; the L1 admits (Q13/Q14 second-seat re-read
recorded inside the entry as `pending (R3)`).

## What I ran (commands, exit codes)

All from `/home/vgpnk/Projects/shokunin` or the lane `kengaku-shokunin` (read-only git; no
mutation anywhere).

1. Read `plans/round-55-claims.md` (frozen claims, commit `80afa613`) — exit 0.
2. Read `corpus/QUALITY.md` (Q1–Q17) — exit 0.
3. Digest verification of the in-repo captures against the frozen pins — exit 0:
   - `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py`
     → `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` (matches S201 pin).
   - `sha256sum corpus/evidence/round52/graders/chess-best-move/tests/test.sh`
     → `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` (matches S109 pin;
     amendment A1 says the chess runner is byte-identical to the regex-log runner — confirmed).
4. Read-only fetch of the pinned instruction (network GET allowed):
   `curl -s https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md`
   → sha256 `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` (matches S202
   pin); file is exactly one line; contains the example literals `e2e4 or h1h8`.
5. Wait loop for the probe receipt, 60 s steps / 25 min cap: the receipt was already present at
   step 1. Receipt bytes:
   `cases=12 observed_pass=5 observed_fail=7 mismatches=0` / `PREDICATE R55-C3 pass`;
   sha256 `de0826692f8b81c832b8d0633cfe8fa080f2d6142ee9d71b597eba6be9d8aaca`.
   A copy as read is retained at `probe-receipt-as-read.txt` beside this report.
6. Read `plans/round55_c3_chess_probe.py` (sibling-built instrument, frozen case table) to copy
   the 12 frozen case bytes verbatim into the entry — exit 0.
7. Quote byte-verification: 13 quoted fragments `grep -qF`'d against the captures — all present
   at the cited lines (`test_outputs.py:23,25`, `:10,14,15,17`, `test.sh:22,25,26,28,29`,
   `instruction.md:1`). Initial two "MISS" results were an artifact of my own checker invoking
   `grep -qF -- <pattern>` (the `--` became the pattern); re-run correctly, both hit at
   `test_outputs.py:14-15`. Not a repo defect.
8. Q21 mechanical check on the entry: pinned-source ⇒ pin named in `recheck:` — passes.
9. `grep -c capab` on the entry → 0; no score/capability claim inside the entry (acceptance).

## Files I wrote

- `kengaku-shokunin/corpus/knowledge/tb2-chess-best-move-grader.md` (the seat's only lane file;
  13,170 bytes) — header triad (`source:` S201/S202/S109 with anchors + sha256 pins,
  `verified-at: 2026-10-30`, `recheck:` with the exact probe re-run command and the pin),
  one-line thesis, receipt-verbatim 12-row evidence table (predicted/observed copied, not
  re-derived), mechanism section (the five required properties: order-insensitive full-multiset
  equality over whitespace-split tokens; no case/unicode normalization; strip+split tolerance;
  duplicates/extras break equality with no partial credit; the instruction's example literal
  `h1h8` is not a winner per the grader pair), S109 reward mapping, negative space + falsifier
  (chess correctness, task validity, image content, model performance, contamination,
  one-task-of-89, class distinction from r45's line-split membership), two connection lines,
  and the honest `second-seat re-read: pending (R3)` admission state.
- `.ufo/waves/round-55/w1/E7KnowledgeEntry/probe-receipt-as-read.txt` (evidence copy).
- `.ufo/waves/round-55/w1/E7KnowledgeEntry/report.md` (this file).

Scratch `/fast/scratch/hyaku/kengaku-r55/E7KnowledgeEntry/` (held one fetched instruction copy)
was deleted after the report landed. No installs/upgrades this seat (host `curl`, `python3`,
`sha256sum`, `grep` only) — nothing to record per the tooling directive.

## Coordination

- Replied to `E8SourcesRows` (IRC): confirmed this entry lands this round so its SOURCES census
  (E11) can re-run after landing. No changes requested on its rows.

## Defects found

None in scope. Observed, not mine to fix: the receipt and instrument
(`plans/round55_c3_chess_probe.py`) are untracked in the lane working tree at writing — the
probe seat or L1 commits them; my entry cites the paths only.

## Dead ends

None. The wait terminated immediately (receipt had landed during scope reading).
