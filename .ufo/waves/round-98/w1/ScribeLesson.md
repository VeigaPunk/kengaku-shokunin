# ScribeLesson — critique of the round-98 `regex-chess` knowledge-entry draft

Seat: ScribeLesson (scribe), round-98 wave 1, lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scope: critique of the knowledge-entry **draft** at `/fast/scratch/hyaku/kengaku-r98/L1/knowledge-draft.md`
against (a) the committed probe receipt at the measured tip T and (b) the captured grader bytes
`corpus/evidence/round98/tb2-regex-chess/test_outputs.py`. Plus two candidate `## Mistakes` rows for
the round lesson, drawn from `.ufo/waves/round-98/L1/dryrun/README.md`. **No production edits, no
commits, no repair of any frozen instrument.** Scratch: `/fast/scratch/hyaku/kengaku-r98/ScribeLesson`
(removed at end of seat).

## Verdict

**Admissible with corrections — every observed vector in the draft's table matches the committed
receipt byte-for-byte; three interpretations need narrowing before the entry is treated as
measured.** No row in the table contradicts the receipt. The findings below are about the
*interpretation* column and about evidence pointers, not about the vectors.

| # | severity | finding |
|---|---|---|
| A | medium | C10's "each game has a witness" overstates what C10 measured (only game 3's witness was exercised) |
| B | medium | C08's "castling rights are checked" overstates: the castling field is compared verbatim, but a corrupted castling field is indistinguishable from a genuinely empty one at 47 of the 108 tested positions |
| C | low | C09's "one anchored literal pair per tested position" is 103 pairs for 108 calls (the builder dedupes), and the table's *contents* were generated offline by python-chess — "no move generation" is true only of the artefact at grading time |
| D | low | the table has 11 rows for 12 cases (C05 and C06 are merged into one row); the receipt distinguishes them by chars/sha, so a reader cannot map that row to a single case |
| E | low | the table drops the receipt's `E:` prefix, so C02's four `FileNotFoundError` legs read as failures rather than errors |
| F | info | the draft at the reviewed path still carries the literal `@T@` placeholder; the tree's committed copy (4654ffc1) already resolves it |
| G | info | "about four minutes of grading per run" has no committed timing receipt in this round's wave dir |

## 1. Independent exercise (evidence that the receipt is what the round claims)

Both frozen counters were re-run by this seat, in an isolated `git clone --shared` checkout detached
at T (`8e37fc65d5649bb37166fdd6b1657445a8cb55b9`), with the replay venv built under scratch
(`uv venv -p 3.13` + `pytest==8.4.1 chess==1.11.2`).

```
C1  LEGS L1=pass … L10=pass
    TARGET executed_rows=42 member=regex-chess cells=file-artifact:33,serialization-schema:8
           set_equals_base_plus_member=1 located=1 executed=1 cases=12 legs=60 mismatches=0
           new_rows=8 new_rows_flagged=0 defects=0
    PREDICATE R98-C1 pass   rc=0        (831 s wall; receipts/c1-replay-at-T.txt)

C2  LEGS K1=pass … K7=pass
    GATE defects base=86 rev=45
    TARGET pop=39 cleared=39 still=0 unbound=0 rows_changed=0 captures_changed=0 new_old_row_defects=0
    PREDICATE R98-C2 pass   rc=0        (receipts/c2-replay-at-T.txt)
```

Both match the lane's committed receipts `.ufo/waves/round-98/L1/c1-tip.txt` and `c2-tip.txt`
line-for-line. All thirteen frozen-instrument hashes at T equal the freeze table
(`receipts/frozen-hashes-at-T.txt`); the anchor-digest gate at T reports `rows=325 tokens=209
defects=45` and **no `DEFECT` line names any of S326–S333** (`receipts/gate-at-T.txt`). The
sources census validates `rc=0` on the live lane. The committed probe receipt at T hashes to
`575e5298a7ca8f602f7244ad6411dca79f1a1a50c083e7b284ce1c50fe3e4092` (41 lines).

## 2. Row-by-row audit of the draft's table against the committed receipt

Receipt lines are `corpus/evidence/round98/regexchess-probe.txt` at T. Leg order is
`immortal,century,naroditsky,not_long,reward` (receipt line 14) — the draft's table legend uses the
same order.

| draft row | draft vector | receipt line | receipt observed | match |
|---|---|---|---|---|
| captured solve.sh, unchanged (40460 pairs) | P,P,P,P,1 | 16 (C01) | P,P,P,P,1 | ✔ |
| no re.json | FileNotFoundError ×4, 0 | 18 (C02) | E:FileNotFoundError ×4, 0 | ✔ (see E) |
| `[]` | F,F,F,P,0 | 20 (C03) | F,F,F,P,0 | ✔ |
| first successor duplicated, second removed | P,P,P,P,1 | 22 (C04) | P,P,P,P,1 | ✔ |
| one successor removed / one duplicated without removal | F,F,F,P,0 | 24 (C05) | F,F,F,P,0 | ✔ (see D) |
| ″ | ″ | 26 (C06) | F,F,F,P,0 | ✔ (see D) |
| en-passant `h6` invented where the true field is `-` | P,P,P,P,1 | 28 (C07) | P,P,P,P,1 | ✔ |
| castling field forced to `-` | F,F,F,P,0 | 30 (C08) | F,F,F,P,0 | ✔ |
| 103-entry lookup table | P,P,P,P,1 | 32 (C09) | P,P,P,P,1 | ✔ |
| the same table minus its last entry | P,P,F,P,0 | 34 (C10) | P,P,F,P,0 | ✔ |
| solution + one never-matching pair, 10,000,001-char replacement | P,P,P,F,0 | 36 (C11) | P,P,P,F,0 | ✔ |
| solution padded to exactly 100000 pairs | P,P,P,F,0 | 38 (C12) | P,P,P,F,0 | ✔ |

Supporting DETAIL lines also agree: C01 `pairs=40460` (line 17), C09
`built=recorded=108,unique=103,entries=103` (line 33), C10 `entries=102` (line 35), C11
`chars=12618152 pairs=40461` (line 37), C12 `pairs=100000` (line 39). The draft's parenthetical
figures (40460 pairs, 103 entries, 100000 pairs, 10,000,001-char replacement) are the receipt's own.

**Every vector in the draft table matches the committed receipt.** The one thing the draft does not
say, but should: the receipt closes `mismatches 0` (line 41), i.e. all twelve observed vectors equal
their frozen predictions — the table is the observation block, not a selection from it.

## 3. Interpretation audit — each claim against the captured bytes

Captured file: `corpus/evidence/round98/tb2-regex-chess/test_outputs.py` at T, sha
`4983c44d21c56dd8191381eff0304afc8b87bb714527ea9036b3319c015a30b4`; `test.sh` sha
`8f7f00a1c4dde7fcca6c918c768f2aba432b8c4007c15989716c68091950da87`; `instruction.md` sha
`a6ed3fcc54fc92d71a84af921942422d299ca89b410dcd92cd05a53d0d06436c`.

**Body prose — supported.**

- "applies `/app/re.json` (a list of `[regex, replacement]` pairs) to each tested FEN" — lines 12–13
  (`for pattern, repl in json.load(open("/app/re.json"))` / `fen = re.sub(pattern, repl, fen)`).
- "splits the result on newlines" — line 14 (`fen.split("\n")`).
- "drops the last two fields of every line" — line 14 (`x.split(" ")[:-2]`): a six-field FEN loses
  halfmove and fullmove, so the compared string is *board side castling ep*. The reference side is
  truncated identically at line 30 (`" ".join(board_copy.fen().split(" ")[:-2])`), so both sides of
  the comparison are four-field strings — the draft's claim is true in the way it matters.
- "compares with python-chess 1.11.2's successors (queen promotions only)" — lines 24–26 skip every
  promotion that is not a queen; version from receipt line 9 (`GRADER_SIDE python,chess,pytest 3.13
  1.11.2 8.4.1`).
- "Each output line must be in the reference set — or become a member once its last remaining field
  is rewritten to `-`" — line 35: `assert x in python_chess_moves or x.rpartition(" ")[0]+" -" in
  python_chess_moves`. Independently re-derived: the fallback rewrites field index 3 of 4 — the
  en-passant field — and leaves board/side/castling untouched
  (`receipts/mechanism-fallback-semantics.txt`).
- "the number of lines must equal the size of the reference set" — line 39:
  `assert len(our_moves) == len(python_chess_moves)`, where `our_moves` is the **list** returned by
  `run_solution` (lines 14–15, 20) and `python_chess_moves` is a **set** (line 23). The count is
  therefore line-count against distinct-successor-count — which is exactly the C04 mechanism and the
  entry's title.
- "The tested positions are every white-to-move position of three published games (108 calls, 103
  distinct FENs)" — `do_test_game` tests the initial position (lines 71–74) and, in the mainline
  loop, the position *before* every odd-numbered ply, i.e. before each white move (lines 79–90,
  `if move_count % 2 == 1` at line 82). Independently re-derived by monkey-patching
  `verify_legal_moves` in the captured module exactly as the probe's builder does: **108 calls, 103
  distinct FENs**, per game 24/42/42 calls with 23/41/41 distinct; the start position is called
  twice per game (line 73 and again at `move_count==1`), and the three games share it, which is
  105−2 = 103 globally (`receipts/mechanism-calls-distinct.txt`). Matches receipt lines 33 and 35
  (`recorded=108,unique=103`).
- "A fourth test caps the file at 10e6 characters and 1e5 pairs" — lines 148–149
  (`< 10e6` chars, `< 1e5` pairs), matching `instruction.md`'s "under 10 megabytes … under
  100,000 pairs".
- "the `test.sh` pins" — `test.sh` 18–23: `uvx -p 3.13 -w pytest==8.4.1 -w chess==1.11.2 -w
  pytest-json-ctrf==0.3.5`; reward is pytest's own exit code (`test.sh` 26–29), matching the case
  table's `reward_rule`. The draft's Limits section correctly discloses that CTRF reporting is not
  staged.
- The quoted contract "tested on other positions as well" is at `instruction.md:27` — verified in the
  captured file, and it is the row S329 was opened for.

**Finding A (medium) — C10's interpretation overclaims.** The draft says the table-minus-last-entry
row shows "each game has a witness: one missing position fails only its game". C10 removes **one**
entry and observes `P,P,F,P,0`: only the *third* game fails. The receipt does not show that games 1
and 2 have witnesses; it shows that the removed entry belongs to the third game and that only that
leg fails. My independent re-derivation (build the lookup order the way the captured builder does,
`dict.fromkeys` over the recorded positions) confirms the removed last entry is the third game's
final position (`5r2/1P6/3K2k1/2pP4/7R/1P6/5p1P/8 w - - 1 41`, unique to game 3), which is why leg 3
is the F (`receipts/mechanism-c08-c04.txt`). It is separately true that each game has positions unique
to it (measured: 22 / 40 / 40), but that is a different, unmeasured property. Suggested wording:
*"the removed entry is the third game's final position, so only the third leg fails; the other two
games' entries are untouched."*

**Finding B (medium) — C08's "castling rights are checked" overstates.** The mechanism statement is
right — the fallback rewrites only the last field, so it never reaches the castling field (line 35 vs.
field index 2) — but the effect is position-dependent and the draft presents it as uniform. I
replayed the grader's own acceptance test (`x in ref` or `x.rpartition(" ")[0]+" -" in ref`, line 35)
over all 108 tested positions with the castling field forced to `-` (the probe's own transform
`(?m)^(\S+ b) \S+ ` → `\1 - `): **47 of 108 positions accept every corrupted line** — wherever the
true successor's castling field is itself empty, a corrupted castling field is indistinguishable
from the truth — and **61 reject it**. The F,F,F legs come from the *start position* of each game,
which is the first position tested and rejects immediately (per game 2/22, 24/18, 21/21
forgiven/failing). Suggested wording: *"the fallback does not reach the castling field, so a
forged castling field is caught — but only at the 61 of 108 positions where the true castling field
is non-empty; at the other 47 the forged field is indistinguishable from a genuinely empty one."*

**Finding C (low) — C09's "one anchored literal pair per tested position, no move generation".**
Two corrections. (i) The builder dedupes: the order is `list(dict.fromkeys(seen))`, so there are
**103 pairs for 108 calls** (receipt line 33: `recorded=108,unique=103,entries=103`), one pair per
*distinct* FEN. (ii) The pairs' *contents* were produced by python-chess offline by the probe's
builder (`board.legal_moves` → successor FENs) before the artefact was staged; what is absent from
the artefact is move generation *at grading time*. The gap the row identifies is nonetheless real and
is the one that matters: the grader only ever tests those 108 positions, so a precomputed table
satisfies it while `instruction.md:27` promises "other positions as well". Suggested wording: *"a
precomputed table of 103 anchored literal pairs (one per distinct tested FEN, 108 calls) passes with
no move generation at grading time; the positions are fixed and public, so the instruction's promise
of other positions is not exercised by these bytes."*

**Finding D (low) — the table merges two cases.** Eleven rows cover twelve cases: "one successor
removed / one duplicated without removal" is C05 (`drop-last`, receipt line 25, `chars=2618157
sha=eb37c9e3c8c5c5f5`) and C06 (`extra-line`, line 27, `chars=2618165 sha=f8b4b0808f3b732d`). Their
vectors coincide, so nothing is falsified, but the two are distinct interventions (one short, one
long) and the count is short of the twelve the entry claims in prose. Split the row.

**Finding E (low) — notation.** The receipt encodes an exception leg as `E:<Type>`; the table writes
`FileNotFoundError ×4` for C02. In the table alone those legs are indistinguishable from `F`
(assertion failure) legs. The round-97 entry has the same shorthand, so this is a house convention
rather than a regression — but the `E:` prefix is the machine-readable distinction, and C02 is
precisely the case about *how* the artefact is missing.

**Finding F (info) — placeholder.** The reviewed draft carries the literal `verified-at: 2026-11-06
(round 98; measured T @T@)`. The tree's committed copy (4654ffc1) resolves it to
`8e37fc65d5649bb37166fdd6b1657445a8cb55b9`; the two files are otherwise identical
(`receipts/draft-vs-committed-entry.diff`). Nothing to fix in the tree; flagged because a draft
carrying `@T@` must not be the version that lands.

**Finding G (info) — the timing figure.** "about four minutes of grading per run on this host"
appears in the SOURCES cell for S328 and in the entry, but this round's wave directory has no
timing receipt — `capture-time.txt` records HTTP capture times, not grader runtime. My own C1 counter
run took 831 s of wall time for a run that re-executes the whole 12-case probe (8-way concurrent),
which is consistent with a few minutes per grading run but is not a per-run measurement. The claim is
traceable to a committed SOURCES row; it is simply not receipted inside the round.

**Not a finding, recorded because it is the load-bearing one:** the entry's title — "Per-line
membership plus an equal count is not set equality" — is exactly right and is proved by the captured
bytes. `our_moves` is a list (line 20), `python_chess_moves` is a set (line 23), membership is
checked per line (line 35) and the count compares list length to set size (line 39). A duplicate
standing in for a missing distinct successor keeps the length equal and passes. My independent
model of that exchange over the 24 first-game positions passes 24/24 in the duplicate-for-omission
form and 0/24 in each of the one-short and one-long forms (`receipts/mechanism-c08-c04.txt`) —
consistent with the receipt's C04/C05/C06 vectors.

## 4. Two candidate `## Mistakes` rows for the round lesson

The dry-run history (`L1/dryrun/README.md`) records two independent defects in the *observation
channel*, both caught before freeze. The lane's committed `corpus/lessons/round-98.md` currently
folds them into one `M1 | verdict-channel` row; the two defects have different mechanisms and
different fixes, so they are better carried separately. Format follows the round-97/98 lesson table
(`id | class | evidence | captured-by | fix / shown able to fail`).

| id | class | evidence | captured-by | fix / shown able to fail |
|---|---|---|---|---|
| M1 | verdict-channel | `.ufo/waves/round-98/L1/dryrun/probe-dryrun-1.txt` — every leg `MISSING`, `mismatches 12`, rc 1: the summary regex required the literal path `/tests/test_outputs.py` while pytest prints `test_outputs.py::name` relative to rootdir | P0 mechanism predictions (`5584a6f7`, `L1/predictions-mechanism.txt`) and the positive control C01 — the probe never reached freeze | anchor the leg regex on pytest's rootdir-relative node id (`test_outputs.py::name`), not on an absolute path; the case table sha `02f30e6a…` was unchanged across all three dry runs, so no prediction was re-fitted to the parser. Shown able to fail: dry run 1 is the committed red output of the old channel (12 × `MISSING`, rc 1) and dry run 2 — with the path fixed — still went red on 3 cases (rc 1), so the corrected channel is not a tautology |
| M2 | verdict-channel | `.ufo/waves/round-98/L1/dryrun/probe-dryrun-2.txt` — C11/C12 read `E:assert` and C02's third leg read `E:` (empty type): pytest's short summary prints the rewritten bare-assert text, so the summary line is not a type channel (`mismatches 3`, rc 1) | same P0 predictions + C01 positive control; the defect is invisible to a reader who only sees the summary text | read the type from `call.excinfo.typename` in an observe-only `pytest_runtest_makereport` hook under real `pytest.main`, and keep pytest's own exit code as the reward leg. Shown able to fail: dry run 2 is the committed red output of the old channel (rc 1, 3 mismatches) and dry run 3's 12/12 came only after the channel changed; the frozen counter's own P2 controls keep the channel falsifiable (`controls/c1-do-nothing-run{1,2}.txt` fails L1–L10, `controls/c1-forged-receipt-run{1,2}.txt` fails L3/L6) |

Both rows are drafted from the dry-run artefacts only; neither touches a frozen instrument, and the
`case table sha 02f30e6a…` is identical in all three dry runs, so the predictions were never moved to
fit the parser.

## 5. Out of scope / not done

- No production edit, commit, push, or mutation of the lane, the fleet repo, or sibling repos. The
  draft was read only; `corpus/knowledge/tb2-regex-chess-grader.md` and `corpus/lessons/round-98.md`
  were read for context and left untouched.
- No frozen instrument was repaired or re-run against a modified tree; the counters were run
  unmodified, in a detached `git clone --shared` checkout at T under scratch.
- No attempt to re-measure at BASE (the lane's committed `c1-base.txt` / `c2-base.txt` already record
  BASE failing, and the milestone for this wave is the T measurement).
- The lookup-table builder's *content* was re-derived, not the probe's staging path; the probe's own
  builder was not re-implemented beyond reading it.

## 6. Receipts (this seat's evidence directory)

`.ufo/waves/round-98/w1/ScribeLesson/`

| file | what |
|---|---|
| `c1-replay-at-T.txt` | my independent `plans/round98_c1_replay.py` run at T (rc 0, frozen TARGET line) |
| `c2-replay-at-T.txt` | my independent `plans/round98_c2_nested_bind.py` run at T (rc 0, frozen TARGET line) |
| `receipt-at-T.txt` | the committed probe receipt at T (41 lines, sha `575e5298…`) |
| `gate-at-T.txt` | `plans/anchor_digest_check.py` at T — 45 defects, none on S326–S333 |
| `frozen-hashes-at-T.txt` | the thirteen frozen-instrument hashes recomputed at T |
| `mechanism-calls-distinct.txt` | independent call/distinct-FEN counts from the captured grader (108 / 103; per game 24/42/42) |
| `mechanism-fallback-semantics.txt` | independent derivation of what the `rpartition` fallback rewrites and when it forgives |
| `mechanism-c08-c04.txt` | independent C08 acceptance map (47 forgiven / 61 failing of 108) and the C04/C05/C06 count models (24/24, 0/24, 0/24) |
| `draft-vs-committed-entry.diff` | the draft vs the tree's committed knowledge entry (one line: the `@T@` placeholder) |

Tooling used (recorded per the operator directive): `uv` (already on host) with `uv venv -p 3.13` and
`uv pip install pytest==8.4.1 chess==1.11.2` into a throwaway venv under scratch — official uv/PyPI
channel, reason: reproduce the pinned grader side. No pacman transaction, no host service or sysctl
touched, no PATH directory written. `python3` (host) and `git` (host) were used as-is.
