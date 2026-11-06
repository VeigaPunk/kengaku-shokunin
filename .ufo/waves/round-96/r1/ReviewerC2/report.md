# ReviewerC2 — R96-C2 review at T `09717e49` (residual call r1)

**Verdict: R96-C2 fails.** The frozen predicate at T prints `GROWS checked=6 tolerant=5` →
`PREDICATE R96-C2 fail`, rc 1 (official receipt `.ufo/waves/round-96/L1/c2-tip.txt:22,36-37`); the
claim's kill rule ("not met if the predicate is not `pass` at T", `plans/round-96-claims.md:109-110`)
fires and the verdict is final. Independently of the predicate, C lands a C2 repair byte outside
the candidate-bytes table (`plans/grader-population-ledger.json`, `mteb-retrieve.subject`), the
re-pin makes the r87 counter red at r87's own measured tip `10de494d`, and the repair byte-replaced
frozen instruments of closed rounds (freeze-integrity r93/r94/r95 PASS→FAIL). The repair was
reverted after T at `3f300cbd`. On re-measurement the battery's three legs pass (14/14, 12/12,
6/6), so the official failure is a non-deterministic instrument failure, not a repair-mechanism
failure — but the claim is not met as measured, and the instrument has two further discrimination
holes: a stub in any of the 8 bite-free seats passes the predicate, and a two-member L7 passes all
three bites.

No tools were installed or upgraded. Scratch: `/fast/scratch/hyaku/kengaku-r96/ReviewerC2` (removed
after the receipts below were copied).

## What I ran

All counters were run with cwd = the `--lane` root. Receipts are in
`.ufo/waves/round-96/r1/ReviewerC2/`.

| # | run | command | result | receipt |
|---|---|---|---|---|
| 1 | frozen battery at T, my clone | `python3 plans/round96_standing_battery.py --lane <clone> --rev 09717e49… --work <scratch>` | `STANDING 14/14`, `BITES 12/12`, `GROWS 6/6`, `PREDICATE R96-C2 pass`, rc 0 | `battery-T-at-T.txt` |
| 2 | hand-built r91 grow fixture (same `forge` transformation as the battery) | `python3 plans/round91_c1_replay.py --lane <clone> --rev <forged>` | `TARGET executed_rows=41 … defects=0`, `PREDICATE R91-C1 pass`, rc 0 | `grow-r91-hand-fixture.txt` |
| 3 | 12 concurrent copies of run 2 | same, 12 work dirs | 12/12 `PREDICATE R91-C1 pass`, rc 0 | `load-12x-r91-grow.txt` |
| 4 | F1: stub `plans/round90_c1_replay.py` (prints `PREDICATE R90-C1 pass`, exit 0) at T, battery | `--rev a66f0e1e` | `STANDING 14/14`; `BITE r90 own rc=0 bitten=0`, `other rc=0 bitten=0`; `BITES 10/12`; `PREDICATE fail`, rc 1 | `forgery-F1-fake-r90.txt` |
| 5 | F2: stub `plans/round83_c1_replay.py` at T, battery | `--rev f4fda775` | `STANDING 14/14`, `BITES 12/12`, `GROWS 6/6`, `PREDICATE pass`, rc 0 | `forgery-F2-fake-r83.txt` |
| 6 | F3: round90 L7 checks only `{merge-diff-arc-agi-task, build-pmars}` at T, battery | `--rev 54a623f4` | `STANDING 14/14`, `BITES 12/12`, `GROWS 6/6`, `PREDICATE pass`, rc 0 | `forgery-F3-two-member-r90.txt` |
| 7 | r87 T-bytes at r87's own measured tip `10de494d` | `python3 plans/round87_c1_replay.py --lane <clone> --rev 10de494d` | `DEFECT L7-ledger row {… "subject": "tb2-result-file" …}`, `PREDICATE fail`, rc 1 | `r87-own-new.txt` |
| 8 | r87 F-bytes at `10de494d` | same, old bytes | `TARGET … defects=0`, `PREDICATE pass`, rc 0 | `r87-own-old.txt` |
| 9 | r90 at its SCORECARD rev `9cf98d90`, T-bytes and F-bytes | `--rev 9cf98d90` | both `executed_rows=34 … defects=0`, `PREDICATE pass`, rc 0 | `r90-hist-new.txt`, `r90-hist-old.txt` |
| 10 | r90 at T + one new ledger member row | `--rev cdc88e2f` | `DEFECT L7-ledger executed=40 members=89 …`; `DEFECT L7-ledger cell file-artifact 31 of 77 != frozen 25 of 76`; `PREDICATE fail`, rc 1 | `r90-population-growth.txt` |
| 11 | freeze-integrity gate v2, r93 table, at T | `python3 plans/round94_freeze_integrity.py --lane <clone> --freeze d8d0a4b8… --rev 09717e49… --claims plans/round-93-claims.md` | `INSTRUMENT plans/round93_c1_replay.py … touched=1 verdict=broken:rev-bytes-differ+touched-after-freeze=1`; `FREEZE-INTEGRITY instruments=9 intact=8 broken=1`; `PREDICATE freeze-integrity fail`, rc 1 | `freeze-r93-at-T.txt` |
| 12 | landing tip `3f300cbd` state | r79 gate and r87 F-bytes at the landing tip | r79 `DEFECT SUBJECT-MISMATCH mteb-retrieve ledger=tb2-result-file receipt=tb2-header`, `DEFECTS n=1`, rc 1; r87 `PREDICATE pass`, rc 0 | `r79-landing.txt`, `r87-landing.txt`, `post-T-revert.txt` |

## 1. Frozen predicate at T — the verdict driver

Official: `BITE r91 kind=grow rc=1 tolerant=0` (`L1/c2-tip.txt:22`), `GROWS checked=6 tolerant=5`
(line 36), `PREDICATE R96-C2 fail` (line 37). My re-run of the same frozen bytes at the same rev:
14/14, 12/12, 6/6, `PREDICATE R96-C2 pass`, rc 0. The hand-built grow fixture passes (`TARGET
executed_rows=41 … defects=0`), and 12 concurrent copies pass. The battery keeps no per-run output
(`run_counter` deletes `--work` in `finally`, `plans/round96_standing_battery.py:91-103`; `bite()`
prints only `rc`, lines 202-208), so the official failing `DEFECT` line is unrecoverable. The
predicate is not deterministic; the claim's kill rule fires on the official receipt, and the
repair's mechanism passes on re-measurement. (Independently found by CriticClaimsR C2-F1; my runs
1-3 reproduce it.)

## 2. Kill-rule byte scope

`git diff F T -- plans/grader-population-ledger.json` (in `static-checks.txt`) shows the C2 repair
byte `mteb-retrieve.subject: "tb2-result-file" → "tb2-header"`. The candidate-bytes table
(`plans/round-96-claims.md:36-44`) lists only the seven counter files. The kill rule says "Not met
if … C lands bytes other than the candidate-bytes table" (lines 109-110). R96-C2 is therefore not
met on that clause independently of the predicate. (Lesson M5; CriticClaimsR C2-F3.)

The seven files themselves are byte-exact: their sha256 at T equals the candidate-bytes table; the
pre-committed `controls/candidate-edits.diff` applies cleanly at F and yields exactly those seven
shas; the frozen-instruments files are unchanged F→T; the battery's sha256 at T is
`989eb10f…d2c99`, the frozen value.

## 3. L7 condition retention (assignment check 1)

Read at T (`git show T:plans/round9*_c1_replay.py`). "Only replaces the absolute pin" is not exact:
the class-cell equality is also relaxed to a lower bound in all six, and the set equality is relaxed
to a superset in r94/r95 (the claimed growth tolerance).

| counter | retained unchanged | replaced | additional relaxation |
|---|---|---|---|
| r87 | row tuple `(status, round, receipt, subject, verdict)`, `LEDGER_ROUND`, `RECEIPT`, `LEDGER_VERDICT` | — | only `LEDGER_SUBJECT` changed (`tb2-result-file` → `tb2-header`); no absolute executed total in r87's L7 (it prints `executed_rows` but never compares it) |
| r90 | row tuple, `MEMBERS_TOTAL = 88`, class **totals** exact (`got[1] != want_total`) | `executed_rows != EXECUTED_AFTER` → `rev_set >= base_set \| {MEMBER}` | class **done** `==` → `>=` |
| r91 | `status`, `round == 91`, `classes == table["class"]` | `exec_total == EXECUTED_AFTER` → set check | class done `==` → `>=` |
| r92 | `status`, `round == 92`, `classes == MEMBER_CLASSES` | `exec_total == EXECUTED_AFTER` → set check | class done `==` → `>=` |
| r93 | `status`, `round == 93`, `classes == MEMBER_CLASSES` | `exec_total == EXECUTED_AFTER and cells == AFTER_CELLS` → set check + lower bound | class done `==` → `>=` |
| r94 | `status`, `round == 94`, `classes == MEMBER_CLASSES` | `exec_total == EXECUTED_AFTER` removed; set `==` → `>=` | class done `==` → `>=` |
| r95 | `status`, `round == 95`, `classes == MEMBER_CLASSES`, `legacy_ok` (receipt/subject/verdict) | `exec_total == EXECUTED_AFTER` removed; set `==` → `>=` | class done `==` → `>=` |

No other condition was dropped. The class-cell relaxation is redundant for removals (the set check
catches a demoted executed member) and is consistent with growth tolerance, but it is a second
change beyond the absolute pin.

## 4. SET_BASE commits (assignment check 2)

Each `SET_BASE` is the round's own BASE as its claims file states, is an ancestor of T, and has the
BASE executed count the claims record (`static-checks.txt`):

| counter | `SET_BASE` | claims citation | executed at BASE | ancestor of T |
|---|---|---|---|---|
| r90 | `dcdd494ef4b4a6c0ae349ecb597527124ee54f91` | `plans/round-90-claims.md:4` "Base: `dcdd494e…`" | 33 | yes |
| r91 | `59764383d4dd33d58faa50daad4c06d0cde410aa` | `plans/round-91-claims.md:4` | 34 | yes |
| r92 | `4ba56182307ccda1ec436bfe3d61cb3d92e56608` | `plans/round-92-claims.md:4` | 35 | yes |
| r93 | `28e9f8bf4e8a68b1a34babfa71be9de595b78c4e` | `plans/round-93-claims.md:4` | 36 | yes |
| r94 | `0cbb927914e07818e1aaee7e72d8b3c90a2d21c2` | `plans/round-94-claims.md:4` (pre-existing `BASE`) | 37 | yes |
| r95 | `4524072dfae9c5e8210592b7c1da26959aa29dae` | `plans/round-95-claims.md:4` (pre-existing `BASE`) | 38 | yes |

## 5. r87 re-pin (assignment check 3)

- The receipt's line 1 is `# tb2 mteb-retrieve grader probe`; the round-79 gate's frozen shape table
  (`plans/round79_c1_population_ledger.py:33,95`) defines `tb2-header` as `^# tb2 {m} grader probe`
  and takes the first matching shape. The re-pin is truthful about the receipt's shape.
- At T the ledger row is `subject: tb2-header` and the counter pins `tb2-header`; `git grep
  tb2-result-file T -- plans corpus` (excluding the round-95 lesson) finds nothing. Nothing else
  pinned `tb2-result-file` at T.
- **But the counter is a historical verifier.** At r87's own measured tip `10de494d` the ledger row
  is `tb2-result-file`; the T bytes fail there (`DEFECT L7-ledger row {… "subject":
  "tb2-result-file" …}`, `PREDICATE R87-C1 fail`, rc 1) while the F bytes pass (`PREDICATE R87-C1
  pass`, rc 0). The re-pin makes a historical counter red at the revision its claim measured. The
  revert `3f300cbd` restores the old bytes; the r79 gate at the landing tip is back to
  `SUBJECT-MISMATCH` (r79 red, r87 green).

## 6. Battery GREEN rule (assignment check 4)

`verdict()` (`plans/round96_standing_battery.py:106-111`) is GREEN iff `rc == 0` and exactly one
`PREDICATE R<n>-C1 pass` line. A counter that prints the predicate without evaluating satisfies it.

- **F1 (fake r90, a bite seat):** `print('PREDICATE R90-C1 pass'); exit 0` → STANDING green 14/14;
  the `own` and `other` bites both see `rc=0` → `bitten=0`; `BITES 10/12` → `PREDICATE fail` rc 1.
  The bite leg catches a fake in a bite seat.
- **F2 (fake r83, a bite-free seat):** the same 3-line stub replacing `plans/round83_c1_replay.py`
  → STANDING green 14/14, `BITES 12/12`, `GROWS 6/6`, `PREDICATE R96-C2 pass`, rc 0. r83 is not in
  `BITE_SET` (lines 67-75), and neither are r79 or r84-r89: 8 of 14 seats are only checked for the
  predicate line. A stub in any of them is invisible to the frozen predicate.

Answer to the assignment's question: yes, `print('PREDICATE R90-C1 pass')` and exit 0 passes
STANDING; BITE catches it for r90 (and the other five bite seats), but not for the eight bite-free
seats.

## 7. BITE "other" choice (assignment check 5)

`others[0]` is `build-pmars` for all six rounds (round 38; the lexicographically first executed
member with `round < rnd`). One removal is sufficient for a set-superset check (`rev_set >=
base_set | {MEMBER}` fails if any member is removed). But the bite population is exactly one
member, so a counter that checks only that member plus its own survives:

- **F3:** round90's `set_ok` replaced by `{"merge-diff-arc-agi-task", "build-pmars"} <= rev_set` →
  STANDING 14/14, `BITES 12/12`, `GROWS 6/6`, `PREDICATE pass`, rc 0. The `own` bite removes
  `merge-diff-arc-agi-task`, the `other` bite removes `build-pmars`, the `grow` bite promotes
  `adaptive-rejection-sampler`; the two-member check fails the first two and passes the third, so
  all three bites are satisfied. The battery cannot distinguish a full-set check from a two-member
  check.

## 8. Claim premise — "six self-assessment mismatches"

The BASE receipt is real (`STANDING 8 green 6 red`: r79, r90-r94), but five of the six are growth
drift, not self-assessment mismatches. The SCORECARD rows are historical measurements at their own
revs: the R90-C1 row names `9cf98d90` and says "met on its frozen predicate". At `9cf98d90` the r90
counter passes both before and after the repair (`executed_rows=34 … defects=0`, rc 0). The red at
BASE is the ledger moving from 34 to 39, i.e. the growth the L7 repair targets. Only r79 is a
genuine standing mismatch. (CriticClaimsR C2-F5; lesson M6.)

## 9. r90 population-growth brittleness

r90 keeps `len(members) != MEMBERS_TOTAL` (88) and exact class totals. One new ledger member row at
T turns r90 red: `DEFECT L7-ledger executed=40 members=89 …` and `DEFECT L7-ledger cell
file-artifact 31 of 77 != frozen 25 of 76`, `PREDICATE fail` rc 1. The battery's grow leg promotes
an existing unexecuted member, so it cannot detect this. The assignment asked that `MEMBERS_TOTAL`
be kept, so this is a residual risk (population growth is census-fixed at 88), not a deviation from
the instruction.

## 10. Freeze-integrity harm (ExecHarm major) — judgment

At T, gate v2 on the r93 table reports `plans/round93_c1_replay.py … touched=1
verdict=broken:rev-bytes-differ+touched-after-freeze=1`, `FREEZE-INTEGRITY instruments=9 intact=8
broken=1`, `PREDICATE freeze-integrity fail` rc 1; r94/r95 are the same per ExecHarm's receipts.
This is a true positive under the gate's contract (bytes at the freeze differ and the path was
touched after the freeze) and a PASS→FAIL for non-author standing gates. The round-96
reclassification ("claimed work, not instruments") does not bind the closed rounds' freeze tables.
It is a real non-author harm, not merely a disclosed cost; the revert restores the bytes but the
history touch is permanent (`touched-after-freeze=2` after the revert, per the lesson). Route:
round 97 (declared re-freeze or accepted breakage). It is not an axis harm to R96-C1.

## Findings

FINDING C2-1 blocker frozen predicate not deterministic: official T `GROWS 6/5` → `PREDICATE R96-C2 fail` rc 1 (`L1/c2-tip.txt:22,36-37`); my run of the same bytes at T is `GROWS 6/6` → pass rc 0, the hand grow fixture passes (defects=0), 12/12 concurrent grow runs pass; the battery keeps no per-run output, so the official failure is unattributable — the claim is not met on the official receipt and the instrument cannot support a stable verdict.
FINDING C2-2 major kill-rule byte scope: C lands `plans/grader-population-ledger.json` `mteb-retrieve.subject` (`tb2-result-file` → `tb2-header`) outside the seven-file candidate-bytes table, so "C lands exactly these seven files" and the kill rule's byte-scope clause are not satisfied as written (the seven files themselves are byte-exact).
FINDING C2-3 major non-author harm: the re-pinned r87 counter fails at r87's own measured tip `10de494d` (`DEFECT L7-ledger row {… "subject": "tb2-result-file" …}`, `PREDICATE R87-C1 fail` rc 1) while the F bytes pass there (rc 0); the repair makes a historical counter red at the revision its claim measured; reverted at `3f300cbd`.
FINDING C2-4 major non-author harm: the repair byte-replaced frozen instruments of closed rounds; gate v2 at T reports r93/r94/r95 `broken:rev-bytes-differ+touched-after-freeze=1` (`instruments=9 intact=8 broken=1`, `PREDICATE freeze-integrity fail` rc 1 for r93), a PASS→FAIL; permanent after the revert (`touched-after-freeze=2`).
FINDING C2-5 major battery GREEN rule is satisfiable by a non-evaluating counter in the 8 bite-free seats (r79, r83-r89): a 3-line stub replacing `plans/round83_c1_replay.py` passes STANDING 14/14, BITES 12/12, GROWS 6/6, `PREDICATE R96-C2 pass` rc 0; the bite leg catches the same stub only in the six bite seats (F1: BITES 10/12, fail).
FINDING C2-6 minor the bite triple cannot distinguish a full-set L7 from a two-member L7: round90 checking only `{merge-diff-arc-agi-task, build-pmars}` passes all three bites and the predicate (F3); `others[0]` is `build-pmars` for all six rounds, so one specific removal is tested, not "the BASE set".
FINDING C2-7 major claim premise overstated: "six self-assessment mismatches" is 1 genuine (r79 SUBJECT-MISMATCH at BASE) + 5 growth-drift maintenance items (r90-r94 pass at the revs their SCORECARD rows name; r90 at `9cf98d90` passes before and after the repair, rc 0).
FINDING C2-8 minor r90's L7 keeps `MEMBERS_TOTAL = 88` and exact class totals, so one new ledger member row turns it red (`members=89`, `cell file-artifact 31 of 77 != frozen 25 of 76`); the battery's grow leg promotes only, so growth tolerance is promotion-only for r90.
FINDING C2-9 info the repair also relaxes class-cell equality to a lower bound in r90-r95 and the set equality to a superset in r94/r95; removals are still caught by the set check, and the class relaxation is a second change beyond the absolute pin.
FINDING C2-10 info the seven candidate files are byte-exact at T (sha256 table), `controls/candidate-edits.diff` applies at F and yields exactly those bytes, the frozen-instruments files are unchanged F→T, and the battery's sha256 matches the frozen table.
FINDING C2-11 info the repair was reverted after T at `3f300cbd`; at the landing tip the r79 gate is back to `SUBJECT-MISMATCH` (rc 1) and the old r87 counter passes (rc 0), i.e. the BASE disagreement and the six absolute-pin counters are restored.

## Residual risk and verification gaps

- The official r91 grow failure's `DEFECT` line is unrecoverable (the battery discards per-run
  output); the cause is not attributable. A retry or output-retention policy is needed (Q80).
- The battery's determinism depends on the host sandbox/load; my clean run and 12x grow stress do
  not reproduce the official failure, so the failure mechanism is unproven.
- The 8 bite-free seats are only checked for the predicate line; a stub there is invisible.
- The repair is reverted at the current lane tip; the six counters are red again at `3f300cbd`
  (r79 red, r90-r95 absolute pins; not re-run as a full battery by me — the landing receipts and
  the r79/r87 runs above establish the state).
- Freeze-integrity history touches on r93/r94/r95 are permanent even after the revert.
