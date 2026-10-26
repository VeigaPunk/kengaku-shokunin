# R43RoutedQueue — round-42 wave-2 routed items into `corpus/routed-findings.jsonl` (closure R3)

Seat: scribe (leaf). Lane `kengaku-shokunin`, no write in the lane. Worktree HEAD
`d33350fdb01ce27cbff47b04642fd2c1471e5c26`; the ledger moved under this seat while it worked (§3), so every
measurement below is stamped with the time it was taken. Task: one routed row per round-42 wave-2 finding, with a
runnable `check` wherever one exists, no close claimed.

**Deliverable: 41 rows drafted** (`R42-R3-01` … `R42-R3-41`), one per numbered defect of the nine routed reports, in
the ledger's own key set. Because other seats landed most of the corrections while this seat was drafting, the draft is
delivered in three forms so the L1 can append something that is *consistent* under `routed_open.py --observe`:

| file (`.ufo/waves/round-43/build/R43RoutedQueue/`) | rows | what it is | measured |
|---|---|---|---|
| `appended-rows.jsonl` | 41 | the draft as first written, all `open`, every check red at `d33350f` | `rows=41 mismatched=0` §4a |
| `reconciled-rows.jsonl` | 38 | same rows: 3 duplicates dropped, 2 refuted → `check: null`, 6 checks re-pointed to where the fix actually landed; all `open` | `rows=38 mismatched=15` §4d (the 15 are the landed ones) |
| `recommended-rows.jsonl` | 23 | the subset that is `open` with a red (or absent) check **today** — the lines to append if the 15 landed items are closed | `rows=23 mismatched=0` §4b |
| `close-candidates.jsonl` | 15 | the 15 landed items as `closed` rows with measured closing evidence (same ids, so they replace rather than duplicate) | `rows=15 mismatched=0` §4c |
| `superseded.md` | 5 | the 3 duplicate rows (§A) and the 2 refuted findings (§B), with the covering row / refutation | — |

End state measured on the whole ledger: 57 rows, `mismatched=1` — and the one mismatch is **not** mine (it is the
sibling row `R42-R2.2`, open with a passing check); `routed_open=34 oldest_round=39` (§4e).

## 1. Where the 41 came from

Counts are the reports' own numbered defects, as routed by `corpus/lessons/round-42-verifier-spotcheck.md:129-131`:

| report (`.ufo/waves/round-42/falsify/`) | defects | rows |
|---|---|---|
| `F42RevC2Package.md` (D1–D9) | 9 | `01`…`09` |
| `F42RevLesson.md` (D1–D8) | 8 | `10`…`17` |
| `F42RevQuality.md` (D1–D6) | 6 | `18`…`23` |
| `F42RevRiders.md` (D1–D5) | 5 | `24`…`28` |
| `F42CritAdv.md` (X3, X7) | 2 | `29`…`30` |
| `F42CritScorecard.md` (M1) | 1 | `31` |
| `F42ConnClaims.md` (Drift 1) | 1 | `32` |
| `F42CritPlanNext.md` (D1–D5) | 5 | `33`…`37` |
| `F42EntryQuotes.md` (#1–#4) | 4 | `38`…`41` |

`source` on every row is the routing sentence (the defect's heading line); `opened_round: 42`; `close`/`blocker` null.
Checks are `grep`-on-the-artefact (26), a tool run (the guard's selftest count, `sources_appendonly.py --lane`, a
chmod-000 sentinel probe, `ls corpus/evidence/round43`), `test -f` on the two unlanded criteria tools, and two
id-anchored ledger greps. No check invokes `routed_open.py` itself — a row whose check called `--observe` would recurse.

## 2. The 41 rows and their state at 2026-10-26 19:25 -03

| id | class | source | state 19:25 -03 |
|---|---|---|---|
| `R42-R3-01` | `entry-false-arithmetic` | `F42RevC2Package.md:71` | landed — close candidate (check green) |
| `R42-R3-02` | `registry-row-line-citation` | `F42RevC2Package.md:80` | open — check red |
| `R42-R3-03` | `entry-internal-inconsistency` | `F42RevC2Package.md:86` | landed — close candidate (check green) |
| `R42-R3-04` | `entry-wrong-citation` | `F42RevC2Package.md:93` | landed — close candidate (check green) |
| `R42-R3-05` | `entry-line-ref-off-by-one` | `F42RevC2Package.md:98` | open — check red |
| `R42-R3-06` | `readme-provenance-label` | `F42RevC2Package.md:102` | open — check red |
| `R42-R3-07` | `registry-row-overstatement` | `F42RevC2Package.md:109` | open — check red |
| `R42-R3-08` | `gate-undeclared-dependency` | `F42RevC2Package.md:116` | open — check red |
| `R42-R3-09` | `entry-vacuous-clause` | `F42RevC2Package.md:124` | open — no check (§6) |
| `R42-R3-10` | `lesson-false-measurement` | `F42RevLesson.md:102` | landed — close candidate (check green) |
| `R42-R3-11` | `lesson-unsupported-carry-claim` | `F42RevLesson.md:109` | open — check red |
| `R42-R3-12` | `lesson-unpersisted-number` | `F42RevLesson.md:118` | open — check red |
| `R42-R3-13` | `lesson-wrong-pointer` | `F42RevLesson.md:128` | landed — close candidate (check green) |
| `R42-R3-14` | `lesson-line-ref-off-by-one` | `F42RevLesson.md:134` | **refuted** — no check (`superseded.md` §B) |
| `R42-R3-15` | `lesson-unreproducible-command` | `F42RevLesson.md:137` | landed — close candidate (check green) |
| `R42-R3-16` | `lesson-line-ref-off-by-one` | `F42RevLesson.md:142` | **refuted** — no check (`superseded.md` §B) |
| `R42-R3-17` | `lesson-fix-without-receipt` | `F42RevLesson.md:146` | open — no check (§6) |
| `R42-R3-18` | `criterion-nonlanded-tool` | `F42RevQuality.md:13` | open — check red |
| `R42-R3-19` | `criterion-cli-mismatch` | `F42RevQuality.md:26` | open — check red |
| `R42-R3-20` | `criterion-unreachable-receipt` | `F42RevQuality.md:35` | landed — close candidate (check green) |
| `R42-R3-21` | `criterion-false-sentence` | `F42RevQuality.md:50` | landed — close candidate (check green) |
| `R42-R3-22` | `criterion-wrong-line-pin` | `F42RevQuality.md:67` | landed — close candidate (check green) |
| `R42-R3-23` | `criterion-self-undermining-scope` | `F42RevQuality.md:73` | open — check red |
| `R42-R3-24` | `ledger-status-mismatch` | `F42RevRiders.md:121` | superseded — `superseded.md` §A |
| `R42-R3-25` | `ledger-stale-check` | `F42RevRiders.md:133` | superseded — `superseded.md` §A |
| `R42-R3-26` | `guard-exit-code` | `F42RevRiders.md:74` | open — check red |
| `R42-R3-27` | `guard-selftest-gap` | `F42RevRiders.md:85` | open — check red |
| `R42-R3-28` | `registry-missing-row` | `F42RevRiders.md:157` | superseded — `superseded.md` §A |
| `R42-R3-29` | `frozen-cell-wrong-citation` | `F42CritAdv.md:30` | landed — close candidate (check green) |
| `R42-R3-30` | `frozen-cell-wrong-citation` | `F42CritAdv.md:53` | landed — close candidate (check green) |
| `R42-R3-31` | `scorecard-overstatement` | `F42CritScorecard.md:66` | open — check red |
| `R42-R3-32` | `envelope-drift-record` | `F42ConnClaims.md:34` | open — check red |
| `R42-R3-33` | `plan-mutant-numerator` | `F42CritPlanNext.md:56` | open — no check (§6) |
| `R42-R3-34` | `plan-missing-restore-control` | `F42CritPlanNext.md:69` | open — no check (§6) |
| `R42-R3-35` | `plan-missing-refusals` | `F42CritPlanNext.md:79` | open — no check (§6) |
| `R42-R3-36` | `plan-class-from-unfrozen-probe` | `F42CritPlanNext.md:91` | open — check red |
| `R42-R3-37` | `plan-host-dependent-cheat` | `F42CritPlanNext.md:107` | open — no check (§6) |
| `R42-R3-38` | `entry-false-sentence` | `F42EntryQuotes.md:45` | landed — close candidate (check green) |
| `R42-R3-39` | `entry-wrong-citation` | `F42EntryQuotes.md:46` | landed — close candidate (check green) |
| `R42-R3-40` | `entry-overclaim` | `F42EntryQuotes.md:47` | landed — close candidate (check green) |
| `R42-R3-41` | `entry-counterfactual-error` | `F42EntryQuotes.md:48` | landed — close candidate (check green) |

## 3. What moved while this seat worked

- 19:16 the draft was written against HEAD `d33350f` (clean clone) and validated: `rows=41 mismatched=0` (§4a).
- 19:19 the lane ledger was still 16 rows (`routed_open=10 oldest_round=39`); the clone test with the draft appended gave
  `rows=57 mismatched=1` — the single mismatch being the pre-existing `R42-R4` (§4f). That is `F42RevRiders` D1.
- 19:22 the worktree had been integrated by another seat: the ledger is 60 rows
  (`sha256 c56fa2a24cd302a5eaf9a2996d6528c0c91a873f4970c2e1a0f009bca447f338`) — my 41 lines **plus** three rows a
  sibling seat drafted (`R42-R2.1`, `R42-R2.2`, `R42-R6`) and `R42-R4` flipped to `closed`. Three of my rows are now
  duplicates of those (`superseded.md` §A). This seat wrote no lane file; the run against the live worktree read
  `rows=60 mismatched=13` — 12 of them mine, because the corrections had landed while I drafted (§4d).
- 19:25 the same worktree: 15 of my 38 survivors have a green check (errata E1–E7 in the entry, the round-42 lesson
  errata block `:167/:186/:193/:206`, and `corpus/QUALITY.md:850/:860/:864`), 15 are still red, 8 carry no check.

## 4. Validation (envelope-pasted)

`routed_open.py --selftest` → `SELFTEST 12/12`, exit 0. Envelope for every run below:
`.ufo/waves/round-43/claims/envelope.sh "$S/env" <cmd>`; `$S=/fast/scratch/hyaku/kengaku-r43/R43RoutedQueue`;
`local_bin_content` digest `328be01808ba022f` unchanged in all of them (the round-43 envelope hashes each
`~/.local/bin` entry's name, type, target and content, and exits 4 on change).

**(a) the 41-row draft on a clean clone of `d33350f`** (`--file appended-rows.jsonl`):

```
ENVELOPE start 19:19:00 cwd=/fast/scratch/hyaku/kengaku-r43/R43RoutedQueue/lane
OBSERVE R42-R3-01 rc=1 observed=fail self=open
… 35 rows rc=1 ; R42-R3-09,17,33,34,35,37 observed=n/a (no check) …
OBSERVE rows=41 mismatched=0
ROWS total=41 open=41 blocked=0 closed=0 refused=0
routed_open=41 oldest_round=42
ENVELOPE end 19:19:02 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

**(b) the 23 rows that are genuinely open at the live tip** (`--file recommended-rows.jsonl`):

```
ENVELOPE start 19:25:17 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
OBSERVE R42-R3-02 rc=1 observed=fail self=open
OBSERVE R42-R3-05 rc=1 observed=fail self=open
OBSERVE R42-R3-06 rc=1 observed=fail self=open
OBSERVE R42-R3-07 rc=1 observed=fail self=open
OBSERVE R42-R3-08 rc=1 observed=fail self=open
OBSERVE R42-R3-09 self=open observed=n/a
OBSERVE R42-R3-11 rc=1 observed=fail self=open
OBSERVE R42-R3-12 rc=1 observed=fail self=open
OBSERVE R42-R3-14 self=open observed=n/a
OBSERVE R42-R3-16 self=open observed=n/a
OBSERVE R42-R3-17 self=open observed=n/a
OBSERVE R42-R3-18 rc=1 observed=fail self=open
OBSERVE R42-R3-19 rc=1 observed=fail self=open
OBSERVE R42-R3-23 rc=1 observed=fail self=open
OBSERVE R42-R3-26 rc=1 observed=fail self=open
OBSERVE R42-R3-27 rc=1 observed=fail self=open
OBSERVE R42-R3-31 rc=1 observed=fail self=open
OBSERVE R42-R3-32 rc=1 observed=fail self=open
OBSERVE R42-R3-33 self=open observed=n/a
OBSERVE R42-R3-34 self=open observed=n/a
OBSERVE R42-R3-35 self=open observed=n/a
OBSERVE R42-R3-36 rc=1 observed=fail self=open
OBSERVE R42-R3-37 self=open observed=n/a
OBSERVE rows=23 mismatched=0
ROWS total=23 open=23 blocked=0 closed=0 refused=0
routed_open=23 oldest_round=42
ENVELOPE end 19:25:18 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

**(c) the 15 landed items as closed rows with evidence** (`--file close-candidates.jsonl`):
`rows=15 mismatched=0`, `ROWS total=15 open=0 blocked=0 closed=15 refused=0`, `routed_open=0`, exit 0, envelope 19:25:21
unchanged. Evidence per row: `01` `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:457` (errata E1); `03` `:499` (E6);
`04` `:465` (E2); `38` `:457`; `39` `:465`; `40` `:477` (E3); `41` `:485` (E4); `10` `corpus/lessons/round-42.md:167`;
`13` `:206`; `15` `:186`; `29`/`30` `:193`; `20` `corpus/QUALITY.md:850`; `21` `:860`; `22` `:864`.

**(d) the 38-row reconciled form (all still `open`)** — what an unreconciled append looks like at this tip:

```
OBSERVE R42-R3-01 rc=0 observed=pass self=open MISMATCH
… the same for 03, 04, 10, 13, 15, 20, 21, 22, 29, 30, 38, 39, 40, 41 …
OBSERVE rows=38 mismatched=15
ROWS total=38 open=38 blocked=0 closed=0 refused=0
routed_open=38 oldest_round=42
ENVELOPE end 19:25:25 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

**(e) the end state if the L1 takes `recommended-rows.jsonl` + `close-candidates.jsonl`** (ledger with my 41 lines
replaced; 19 inherited/sibling rows + 23 open + 15 closed):

```
OBSERVE R42-R2.2 rc=0 observed=pass self=open MISMATCH
OBSERVE rows=57 mismatched=1
ROWS total=57 open=33 blocked=1 closed=23 refused=0
routed_open=34 oldest_round=39
ENVELOPE end 19:25:33 exit=1 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

The one remaining mismatch is the sibling row `R42-R2.2` (open, `grep -qs 'scratch-root-guard' SKILL.md` passes — the
registry row landed). Not mine and not adjusted by me.

**(f) the draft against the ledger of 19:19** (16 rows + my 41), for the record:
`OBSERVE R42-R4 rc=0 observed=pass self=open MISMATCH`, `OBSERVE rows=57 mismatched=1`,
`ROWS total=57 open=50 blocked=1 closed=6`, `routed_open=51 oldest_round=39`, exit 1 — the pre-existing `R42-R4`
defect that `F42RevRiders` D1 routed and the sibling row has since closed.

## 5. Controls — the checks are not vacuous

On a copy of the clone with staged corrections, each row observed alone (one envelope bracketing the set, 19:18:40,
digest unchanged):

```
CONTROL 01-baseline            OBSERVE R42-R3-01 rc=1 observed=fail
CONTROL 38-baseline            OBSERVE R42-R3-38 rc=1 observed=fail
-- stage `## Errata (round 43)` heading only (must stay red)
CONTROL 38-heading-only        OBSERVE R42-R3-38 rc=1 observed=fail
-- stage the :297 span (must go green)
CONTROL 38-with-span           OBSERVE R42-R3-38 rc=0 observed=pass  MISMATCH
-- stage the corrected arithmetic (must go green)
CONTROL 01-with-numbers        OBSERVE R42-R3-01 rc=0 observed=pass  MISMATCH
CONTROL 24-baseline            OBSERVE R42-R3-24 rc=1 observed=fail
CONTROL 24-after-closing-row   OBSERVE R42-R3-24 rc=0 observed=pass  MISMATCH
CONTROL 25-baseline            OBSERVE R42-R3-25 rc=1 observed=fail
CONTROL 25-wrong-row           OBSERVE R42-R3-25 rc=1 observed=fail   (a R42-R2.1 row without the tool path)
CONTROL 25-after-tool-row      OBSERVE R42-R3-25 rc=0 observed=pass  MISMATCH
```

Two behavioural probes of their own:

```
SENTINEL .ROUND-ROOT-SENTINEL present=no reason=sentinel-unreadable:Permission denied
CHECK red reason=sentinel-unreadable:Permission denied round=None want=* seats=0
guard_rc=1                     (row 26 wants 2; plans/scratch_guard.py:17-18 promises 2)
SELFTEST ok=36/36              (row 27 wants >= 37 reported cases)
```

**Two calibration defects found and fixed during this seat** (kept in the record, not quietly dropped):

1. The first observe run (19:17:44) gave `rows=41 mismatched=1`: row `R42-R3-25`'s check was a bare
   `grep -qF 'plans/scratch_guard.py' corpus/routed-findings.jsonl`, and *the row's own text* matched it. Replaced by an
   id-anchored pattern (`"id": "R42-R2(\.[0-9]+)?".*plans/scratch_guard\.py`) and re-verified by the `25-wrong-row`
   control. The row itself is now superseded (`superseded.md` §A).
2. Six checks were written as "the offending text is gone", which the lane's append-only correction rule makes
   unreachable (the entry and the lesson append errata instead of editing). Rows `13`, `15`, `20`, `38`, `39`, `40`
   were re-pointed to the correction's own text/facts during the reconciliation — exactly the drift §3 documents.

## 6. Plan mapping and the two integration options

Round-43 R1 (entry errata + the receipt-pointer correction) is what closes rows `01`, `04`, `13`, `38`, `39`, `40`, `41`;
those errata are in the worktree at this tip and every one of those checks is now green. `R42-R3-03` was closed by the
errata's E6 leg, which R1 did not name. R4/R5 (C1/C2 counters) are recorded as notes on `33`, `34`, `35`, `37`, none
closed. No R2 item (Gate row for S128, Dockerfile flip, the conditional-reject lesson/criterion) is among the 41: those
are spot-check defects D2/D3 routed as R2 in `corpus/lessons/round-42-verifier-spotcheck.md:125-128`; `R42-R3-06` (the
README source label for S128) is adjacent and its note claims nothing of R2.

Two honest options for the L1, both measured:

- **A (23 + 15 closed):** append `recommended-rows.jsonl` and `close-candidates.jsonl` in place of the 41 currently in
  the worktree ledger, drop `24`/`25`/`28`, and decide `14`/`16` (refused or dropped). Result §4e: 57 rows,
  `routed_open=34`, `mismatched=1` (the sibling's `R42-R2.2`).
- **B (all 38 open):** append `reconciled-rows.jsonl` as-is. Result §4d: `mismatched=15` until the L1 closes the 15
  landed items. This is the option this seat's rule points at ("mark them open, never claim a close"), and it needs the
  closes in the same integration pass or the ledger reproduces the R42-R4 defect it just routed.

`routed_open` therefore depends on the option: **34** with A, **51** with B on top of today's 10 (10 + 38 + 3 sibling),
and **52** if all 41 stay open (measured at 19:22).

## 7. Limits

- No close is claimed by this seat. The 15 `close` strings in `close-candidates.jsonl` are measurements with a
  file:line, offered so the L1 can close in one pass; they are never the basis of any C1/C2 admission.
- 8 rows carry no check: `09` (a nit with no stable text property), `17` (the defect is the absence of a receipt), `33`,
  `34`, `35`, `37` (the residual is per-mutant controls, substitute-shape red controls, and an unrun container image;
  the raw witness file is a round-42 artefact), plus the two refuted rows `14`/`16`.
- Every check is a token-anchored heuristic whose note names the token. A correction written in other words leaves the
  row red (six such cases already, §5). Checks are never widened after data.
- The checks read the tracked tip; `R42-R2`'s inherited check passes in a worktree (untracked-then-committed build copy)
  and that asymmetry is `superseded.md` §A's subject, not a validation artefact.
- This seat re-read the cited files while choosing checks and re-measured only what §4/§5 state; no round-42 measurement
  was re-run and no report number is restated as a fresh measurement.
- The ledger is being integrated by other seats concurrently; §3 pins the ledger sha256 at each measurement, and a later
  run may legitimately read differently.

Artifacts: `.ufo/waves/round-43/build/R43RoutedQueue/appended-rows.jsonl` (41 rows, sha256 `7ece1d44d424f502…`, 23251 B),
`reconciled-rows.jsonl` (38, `7b7459a5601dc163…`, 25585 B), `recommended-rows.jsonl` (23, `0d62841bdd085b2d…`,
13550 B), `close-candidates.jsonl` (15, `2056e6a3265e06bf…`, 14246 B), `superseded.md`, and this report. Scratch
`/fast/scratch/hyaku/kengaku-r43/R43RoutedQueue` removed at exit with `plans/scratch_guard.py safe-rm`. No tool
installed, no pacman, no network fetch, no lane git/jj mutation, no subagent.

VERDICT: routed-rows-drafted-41-routed_open-34
