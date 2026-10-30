# S1CaseProse — report (kengaku round 55, wave 1)

Seat: S1CaseProse (scribe). Wave: `kengaku-r55-w1`. Date: 2026-10-30. Lane:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Axis judged: coverage (R55-C3).

## What this seat was for

Map each of the 12 frozen R55-C3 chess probe cases to the instruction requirement it exercises, so
E7KnowledgeEntry can ground the knowledge entry's mechanism section and any requirement-map row in
the captured grader's own assertion. Deliverable:
`.ufo/waves/round-55/w1/S1CaseProse/case-requirements.md`.

## What I ran (commands, exit codes)

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `sha256sum kengaku-shokunin/corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` | 0 | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` — equals the frozen S201 pin |
| 2 | `grep -n 'assert' <same capture>` | 0 | exactly one assertion, at **line 25** |
| 3 | `curl -sS -o $S/instruction.md https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/chess-best-move/instruction.md` | 0 | `http=200 bytes=260` (read-only GET) |
| 4 | `sha256sum $S/instruction.md` | 0 | `6ba25be4e291a4ad04ae42b2dddefcdaef67ca45ca9d5dce661a2e517b19ce7a` — equals the S202 row's pin |
| 5 | `python3 /fast/scratch/hyaku/kengaku-r55/S1CaseProse/derive_cases.py` | 0 | `cases=12 derived_agree=12 disagreements=[]` |
| 6 | `wc -l` / `grep -c` on my own deliverable | 0 | 114 lines; 12 `###` sections; 12× each of Requirement / Grader line / Why / If |
| 7 | `ls -la plans/round55_c3_chess_probe.py` | 0 / 2 | absent at 12:27, present at 12:28 (E5 landed it mid-wave); `corpus/evidence/round55/` still absent at 12:27 |

No mutating git/jj command was run anywhere (no add/commit/push/stash/checkout/reset; read-only
`ls`/`sha256sum`/`grep` only). No clone or worktree was created: this seat performed no
lane-mutating work, so every read was against the lane tree and every write went to a named
wave-dir path. Scratch was used only for the derivation script and the fetched instruction bytes,
under `/fast/scratch/hyaku/kengaku-r55/S1CaseProse/`, and was deleted before yielding.
No tooling was installed or upgraded (nothing needed it).

## What I derived (the substance)

The frozen 12 rows, taken from the wave spec (`.ufo/waves/round-55/w1-dispatch.json:783`, the
E5ChessProbe item), were re-derived independently from the assertion alone —
`move = Path("/app/move.txt").read_text().strip().split()` then
`sorted(move) == sorted(["g2g4","e2e4"])` at `tests/test_outputs.py:25` — including text-mode
universal-newline translation. **12/12 derived verdicts agree with the frozen predictions**, and
the derivation was done from the assertion, not from the instrument's own map.

Requirement atoms quoted from S202: R1 board image ("It is currently white to move"), R2 path
("/app/move.txt"), R3 form ("in the form [src][dst]"), R4 examples ("for example, e2e4 or h1h8"),
R5 all winners ("print them all"), R6 layout ("one per line"). Per-case prose names the
requirement, the grader line, the derivation of the predicted verdict, and what a contrary verdict
would mean (a grader finding vs an instrument/oracle defect).

Requirement map, Q28-shaped (every violating case listed, never one witness):
R1 — no case (the grader never opens `chess_board.png`); R2 — case 9; R3 — cases 5, 12;
R4 — case 11; R5 — cases 4, 6, 7, 9, 11; R6 — no grader-observable violation, cases 2 and 8
*violate the instruction text* and are forgiven.

## Files written

- `.ufo/waves/round-55/w1/S1CaseProse/case-requirements.md` — the deliverable (114 lines).
- `.ufo/waves/round-55/w1/S1CaseProse/derivation.txt` — receipt for command 5 (script + output).
- `.ufo/waves/round-55/w1/S1CaseProse/report.md` — this file.
- `.ufo/waves/round-55/w1/S1CaseProse.md` — the `Report:` trailer path from my seat card.

Nothing else was written. No sibling's file was edited.

## Defects found (reported, not fixed — sibling-owned files)

1. **`plans/round55_c3_chess_probe.py:67` (E5's file) — wrong comment on the `duplicate-move` case.**
   The comment reads "duplicate token leaves the multiset short of 'g2g4'". That is backwards: the
   multiset is long by one extra `e2e4`; `g2g4` is present exactly once. The case fails on
   cardinality (3 tokens vs 2), not on a missing token. Comment-level only — the prediction `F` is
   correct and the battery is unaffected — but the comment is the sentence a later reader would
   cite as the mechanism, so it should be corrected in E5's file, not mine.
2. **`plans/round55_c3_chess_probe.py:73` — incomplete comment on the `crlf-line-endings` case.**
   "split() treats \r\n as whitespace; strip() eats the trailing run" is true but incomplete:
   `read_text()` in text mode already performs universal-newline translation, so the grader never
   sees `\r` at all (verified locally: the text reads back `'g2g4\ne2e4\n'`). The verdict is
   unchanged; the comment understates the mechanism.
3. **Grader-side behaviour the frozen table does not cover (coverage gaps, not defects in a file):**
   a missing `/app/move.txt` raises `FileNotFoundError`, not `AssertionError`, so the instrument
   classifies it SETUP (exit 2), not FAIL; a non-UTF-8 artefact would likewise be SETUP; and a
   non-breaking space between the two moves **PASSES** (verified locally: `'g2g4\xa0e2e4'` →
   `['g2g4','e2e4']`), because `str.split()` splits on Unicode whitespace — no frozen case covers
   that, nor a UTF-8 BOM or a vertical-tab separator.
4. **Requirement-mapping hazard for E7 (spec-level, not a file defect).** The grader never opens
   `chess_board.png`, so the instruction's first requirement ("read a chess board image") is
   exercised by no case. Under Q28, a requirement-map row for "reads the board image" cannot cite
   a violating case; it must be recorded as untested rather than mapped to any of the 12 rows.
5. **Instruction-vs-grader seams recorded (for E7's mechanism/limits text):** "the best move" is
   singular but the grader demands both moves (case 4); "one per line" is never enforced (cases 2
   and 8 pass); and the instruction's own example token `h1h8` is rejected (case 11) while `e2e4` is
   accepted. The grader is stricter than the instruction on case and digit width (cases 5, 12) and
   looser on layout.

## Dead ends

- First draft of the deliverable was 183 lines — over the "under 120 lines" cap — because I wrote
  every case in a 5-bullet form with a per-case blank line. Rewritten at 127, then trimmed to 113.
- A bulk replace of `"\n\n### "` → `"\n### "` also swallowed the space after `###`, producing
  `###1.` — not a heading in CommonMark. Caught it on the read-back and repaired with a second
  `replace_all` (`"\n###"` → `"\n### "`); final file re-read and verified (12 sections, 114 lines).
- I looked for a prior-round precedent for this artefact shape (`.ufo/waves/**/case-requirements.md`
  and similar): none exists, so there was no house format to copy — the shape is new in round 55.
- I did **not** run the bwrap 12-case battery (E5/E6 own it) and did **not** import the captured
  grader for execution, so no `observed=` value anywhere in my file is claimed from execution; all
  twelve verdicts are labelled as re-derivations.

## Hand-off for the L1 / E7

`case-requirements.md` is ready to consume: 12 sections, each naming the requirement (with the
S202 words), the grader line (`tests/test_outputs.py:25`), the prediction rationale, and the
meaning of a contrary verdict; plus a Q28-shaped requirement map and an honest gaps list. It
asserts no `observed=` value and no capability or score claim.
