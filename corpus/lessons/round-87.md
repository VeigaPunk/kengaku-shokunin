# Kengaku round 87 — a fifth executed Terminal-Bench 2.0 member, and the round-86 case-set wording repaired against the table

Round 87 (hyaku run 15, attempt 1), 2026-11-05. L1 `KengakuR87`. Lane `kengaku-shokunin`, branch `master`.
Frozen claims: commit `b0f076518dad55f62a89183c5a873957ad3cf6a5` (`plans/round-87-claims.md`,
`plans/round87-cases.json`), frozen before any instrument existed. Base `b9be687774e6b559470f5b0d9b936315b51ff311`.
Instruments: `21da383b44a399f40faf346eed89210c9114848d`. Receipt LANE_TIP is that commit.

Two claims on two distinct axes:

- `R87-C1` coverage (lowest non-retired axis, held at its L0 cap of 7): one more located offline replay,
  `mteb-retrieve`, by `plans/round87_c1_replay.py`, which also counts its executed rows from the ledger
  (closes round-86 routed defect R86-V4).
- `R87-C2` calibration (held at ceiling 10): the live current-state wording of the round-86 case set
  (`corpus/README.md`) agreed with the table-derived split (eight case shapes, six schema-drift, two controls)
  by `plans/round87_c2_wording.py` (closes round-86 routed defect R86-V3 in live docs).

## Gate

The L1 opened both sources below on 2026-11-05 (`curl`, HTTP 200) and byte-compared the first with the
round-52 capture before admitting the row. The capture is `sha256 e4e6b21fed6662adb4a42aba23d35609450392839a2282f3ba77c70c8d907c0b`;
`cmp` is silent. Two new rows were appended to `corpus/SOURCES.md`; no existing row's status, recheck or
used-by cell changed.

| id and decision | URL | access date | located quote (8 words, ≤25) | reason / flip |
|---|---|---|---|---|
| S275 admit, A for pinned grader acceptance semantics (member replay only) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-retrieve/tests/test_outputs.py | 2026-11-05 | `assert lines[0].strip() == expected, "result.txt contains unexpected value"` at line 15 | the grader's two predicates over `/app/result.txt` are the replay's acceptance surface; scope is member replay only, not a retrieval-benchmark or solved-task claim |
| S276 reject (`REJECTED:` row) | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/mteb-leaderboard/tests/test_outputs.py | 2026-11-05 | the same line 15 quote (the sibling grader differs only in its expected string) | same two-assert shape and file-artifact class as S275; a replay adds no class, edge or vector S275 lacks. Flip: a sibling grader that adds an edge class (a non-text artifact or a subprocess leg) |

Census, `sh scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`: exit 0 before
(266 rows) and after (268 rows); rows added by tier: A 2 (S275 admitted, S276 rejected). Status: mined 242 → 243,
rejected 16 → 17, queued 8 unchanged.

Candidates considered and not taken this round: `fix-git` (two stdlib tests, a crypto-credential class,
unopened this round, no row). It is the next candidate, not admitted.

Considerthese: no unimplemented proposal is mined this round. The latest `considerthese/2026-10-26.md` proposal
2 is Q61's per-entry form (round-86 spot-check, `corpus/lessons/round-86-verifier-spotcheck.md`); nothing new
was taken.

Assimilation: none. `merge/kengaku/` remains blocked by L0 `kengaku | round-54`.

## Claims and their measurements

- **R87-C1 (coverage).** Before (BASE `b9be6877`): `TARGET executed_rows=30 member=mteb-retrieve located=0 executed=0 cases=0 legs=0 mismatches=0 defects=3`, `PREDICATE R87-C1 fail`, exit 1. Three defects: `L4-table` (table absent at base), `L1-receipt` (receipt absent), `L7-ledger` (row unexecuted). The frozen claim text said `defects=7`, a figure carried over from round 86 and never measured for this member; see Mistakes 2. The measured BASE is the number of record; the predicate is unchanged.
- **R87-C2 (calibration).** Before (BASE): `TARGET mismatches=1 defects=2 total=8 schema=6 control=2`, `PREDICATE R87-C2 fail`, exit 1. The one mismatch is `corpus/README.md:941` asserting "eight frozen schema-drift cases" against 6 derived; the second defect is the canonical sentence absent from the row.

## Controls and battery

Committed before the measured tip is scored (see `.ufo/waves/round-87/L1/`):

- do-nothing controls at BASE (the two blocks above);
- the ledger-only and forged-receipt controls against the measured tip (fixtures in scratch clones, transcripts in `.ufo/waves/round-87/L1/controls.txt`);
- a C2 fixture whose derived sentence is wrong (`five` schema-drift, `three` controls) must report `mismatches >= 1`;
- the R86-V4-style pointer check: `plans/round87_report_paths.py` run on the round-86 filed report is red, `DEFECT pointer .ufo/waves/round-86/L1/outside-gates.txt (report line 59)`, `POINTERS n=26 missing=1`, exit 1.

## Mistakes

1. **Class `reference-drift`.** Evidence: round-86 filed report line 59 and `LOG.md:3317` cite
   `.ufo/waves/round-86/L1/outside-gates.txt`, which exists in no ref (round-86 spot-check routed defect 1).
   Captured-by: none (no criterion or check ran on the filed report). Fix: `plans/round87_report_paths.py`.
   Shown able to fail: exit 1 on the round-86 report (`.ufo/waves/round-87/L1/paths-red.txt`). It is green
   only on a report whose cited paths resolve. The round-86 bytes stay as filed; the correction is this entry,
   not an edit to the report (PROTOCOL: a filed report is a record).
2. **Class `number-drift` (a count carried into a frozen claim).** Evidence: `plans/round-87-claims.md`
   states `TARGET ... defects=7` at BASE; the counter measured `defects=3` at `b9be6877`
   (`.ufo/waves/round-87/L1/base-runs.txt`). The 7 came from round 86's C1 BASE figure, which measured a
   different receipt set. Captured-by: none. Fix: a criterion, not yet executable: a BASE count in a frozen
   claim is measured by its counter before the freeze commit, and the figure is copied from that output
   (`corpus/QUALITY.md` Q66). The freeze stays as committed; the predicate `defects=0` is untouched. Shown able to
   fail: not yet, routed to round 88 as a counter-side check.
3. **Class `vacuous` (a literal in a counter's summary line).** Evidence: round-86 `TARGET members=1` printed
   a constant, not a count (round-86 spot-check routed defect 4, R86-V4). Captured-by: none. Fix: the round-87
   counter prints `executed_rows`, counted from the ledger at the measured revision. Shown able to fail:
   `executed_rows=30` at BASE, `executed_rows=31` at the tip; a literal could not produce both.

## Frontier

Expansion moved by one member of the same replay method (the round-84/85/86 class of move, not a new kind of
source). The lesson keeps the expansion verdict at `unchanged` in the report, as round 86 did: the coverage axis
moves on counts, but the expansion observable is admitted knowledge on uncovered ground, which did not occur.
