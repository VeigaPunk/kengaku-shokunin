# ReviewerC2 — R96-C2 scoped findings (T `09717e49`, residual call r1)

**Verdict: R96-C2 fails.** The frozen predicate at T prints `GROWS checked=6 tolerant=5` →
`PREDICATE R96-C2 fail`, rc 1 (`.ufo/waves/round-96/L1/c2-tip.txt:22,36-37`); the kill rule
(`plans/round-96-claims.md:109-110`) makes that verdict final. Independently, C lands a C2 repair
byte outside the candidate-bytes table, the re-pin makes the r87 counter red at r87's own measured
tip, and the repair byte-replaced frozen instruments of closed rounds (freeze-integrity
r93/r94/r95 PASS→FAIL). The repair was reverted after T at `3f300cbd`. On re-measurement the
battery passes (14/14, 12/12, 6/6), so the official failure is a non-deterministic instrument
failure, not a repair-mechanism failure — but the claim is not met as measured, and the instrument
has two further discrimination holes.

Full report and receipts: `.ufo/waves/round-96/r1/ReviewerC2/` (`report.md`, `battery-T-at-T.txt`,
`grow-r91-hand-fixture.txt`, `load-12x-r91-grow.txt`, `forgery-F1-fake-r90.txt`,
`forgery-F2-fake-r83.txt`, `forgery-F3-two-member-r90.txt`, `r87-own-new.txt`, `r87-own-old.txt`,
`r90-hist-new.txt`, `r90-hist-old.txt`, `r90-population-growth.txt`, `freeze-r93-at-T.txt`,
`static-checks.txt`, `post-T-revert.txt`, `r79-landing.txt`, `r87-landing.txt`).

## Assignment checks

1. **L7 condition retention — yes for the row/round/classes/receipt/subject/verdict and r90's
   `MEMBERS_TOTAL`; not "only the absolute pin".** r87 changes only `LEDGER_SUBJECT`. r90-r95 keep
   the member row, round, classes and (r95) `legacy_ok`; the absolute executed total is replaced by
   the BASE-set superset check. In addition, class-cell equality is relaxed to a lower bound in all
   six, and the set equality is relaxed to a superset in r94/r95 (the claimed growth tolerance).
   Removals are still caught by the set check.
2. **SET_BASE commits are each round's BASE.** r90 `dcdd494e` (claims:4, executed 33), r91
   `59764383` (34), r92 `4ba56182` (35), r93 `28e9f8bf` (36), r94 `0cbb9279` (37), r95 `4524072d`
   (38); all ancestors of T, counts match the claims' BASE figures. r94/r95 use their pre-existing
   `BASE` constants, which equal the claims' Base.
3. **r87 re-pin is truthful about the receipt's shape but breaks the historical counter.** Receipt
   line 1 `# tb2 mteb-retrieve grader probe` matches the r79 gate's first shape `tb2-header`
   (`plans/round79_c1_population_ledger.py:33,95`); at T the ledger cell and the counter both say
   `tb2-header` and no live `tb2-result-file` pin remains. But at r87's own measured tip `10de494d`
   the ledger cell is `tb2-result-file`, and the T bytes fail there (`DEFECT L7-ledger row {…
   "subject": "tb2-result-file" …}`, `PREDICATE R87-C1 fail` rc 1) while the F bytes pass (rc 0).
4. **The GREEN rule is satisfiable by a counter that does not evaluate.** A 3-line stub
   `print('PREDICATE R90-C1 pass'); exit 0` passes STANDING; BITE catches it for r90 (BITES 10/12,
   fail). The same stub in r83 — not in `BITE_SET` — passes STANDING 14/14, BITES 12/12, GROWS 6/6,
   `PREDICATE pass` rc 0. 8 of 14 seats (r79, r83-r89) are bite-free.
5. **The BITE "other" choice is one specific removal (`build-pmars` for all six rounds).** One
   removal is sufficient for a set-superset check, but a counter that checks only its own member
   plus `build-pmars` survives all three bites and the predicate (F3: 14/14, 12/12, 6/6, pass).

## Findings

FINDING C2-1 blocker frozen predicate not deterministic: official T `GROWS 6/5` → fail rc 1; my run of the same bytes at T is `GROWS 6/6` → pass rc 0, the hand grow fixture passes (defects=0), 12/12 concurrent grow runs pass; the battery keeps no per-run output, so the official failure is unattributable.
FINDING C2-2 major kill-rule byte scope: C lands `plans/grader-population-ledger.json` `mteb-retrieve.subject` (`tb2-result-file` → `tb2-header`) outside the seven-file candidate-bytes table; the seven files themselves are byte-exact.
FINDING C2-3 major non-author harm: the re-pinned r87 counter fails at r87's own measured tip `10de494d` (rc 1) while the F bytes pass (rc 0); reverted at `3f300cbd`.
FINDING C2-4 major non-author harm: the repair byte-replaced frozen instruments of closed rounds; gate v2 at T reports r93/r94/r95 `broken:rev-bytes-differ+touched-after-freeze=1` (`instruments=9 intact=8 broken=1`, `PREDICATE freeze-integrity fail` rc 1 for r93), PASS→FAIL; permanent after the revert.
FINDING C2-5 major battery GREEN rule satisfiable by a non-evaluating counter in the 8 bite-free seats (r79, r83-r89): a stub replacing `plans/round83_c1_replay.py` passes STANDING 14/14, BITES 12/12, GROWS 6/6, `PREDICATE R96-C2 pass` rc 0.
FINDING C2-6 minor the bite triple cannot distinguish a full-set L7 from a two-member L7: round90 checking only `{merge-diff-arc-agi-task, build-pmars}` passes all three bites and the predicate.
FINDING C2-7 major claim premise overstated: "six self-assessment mismatches" is 1 genuine (r79) + 5 growth-drift items (r90-r94 pass at the revs their SCORECARD rows name; r90 at `9cf98d90` passes before and after the repair).
FINDING C2-8 minor r90 keeps `MEMBERS_TOTAL = 88` and exact class totals, so one new ledger member row turns it red (`members=89`, `cell file-artifact 31 of 77 != frozen 25 of 76`); the battery's grow leg promotes only.
FINDING C2-9 info the repair also relaxes class-cell equality to a lower bound (r90-r95) and the set equality to a superset (r94/r95); removals are still caught by the set check.
FINDING C2-10 info the seven candidate files are byte-exact at T; `candidate-edits.diff` applies at F and yields exactly those bytes; frozen files unchanged F→T; the battery's sha256 matches the frozen table.
FINDING C2-11 info the repair was reverted after T at `3f300cbd`; at the landing tip r79 is back to `SUBJECT-MISMATCH` (rc 1) and the old r87 counter passes (rc 0).

## Residual risk and verification gaps

- The official r91 grow `DEFECT` line is unrecoverable (the battery discards per-run output); the
  cause is not attributable. Retry or output retention is needed (Q80).
- The battery's determinism depends on the host sandbox/load; my clean run and 12x grow stress do
  not reproduce the official failure.
- The 8 bite-free seats are only checked for the predicate line.
- The repair is reverted at the current lane tip; the six counters are red again at `3f300cbd`
  (landing receipts and the r79/r87 runs above establish the state; no full battery re-run there).
- Freeze-integrity history touches on r93/r94/r95 are permanent even after the revert.
