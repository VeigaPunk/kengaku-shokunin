<!--
Draft for the LOG.md round-53 entry. L1 owns the landed text; this file is the seat's proposal.
Numbers carry their command or a pointer. `[pending: ...]` = not measured by the L1 yet.
-->

## Round 53 (hyaku run 11, 2026-10-28 → 2026-10-30): a blind-oracle presence-only triage of the Terminal-Bench 2.0 graders (C1 pending on prior art); every registry row's tip-state declared and re-executed (C2 re-measurement pending)

L1 `KengakuR53`; hyaku run 11 re-dispatch. Inherited: the frozen claims and counters, wave-1 outputs, the wave-1
evidence commit (`58746180`), amendments A1–A3 (`plans/round-53-claims.md`; A1 at `d40b7055`, A2 at `56fdff79`, A3 at
`7095e857`), the eight blind label files (`db90a6b7`) and the classifier freeze file. Wave 1 built (35 seats); wave 2
falsified and confirmed (42 seats dispatched; the 2026-10-28 operator wrap-up stopped it after five of its seven
confirmation readers delivered); wave 3 (32 seats) prices the confirmed tasks, touch-runs them, re-labels the oracle
blind, re-attacks both counters and re-measures the tip-state ledger. Lane tip at this seat's clone time:
`9ead4476bf55b1ea6490d0204b668195db4a4d1d` (`git -C <clone> rev-parse HEAD`); the tip when the seat started was
`b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe` — the lane advanced under the seat, so only the `9ead4476` measurements
are cited below.

Motivating evidence and outcome:

- **R53-C1 (novelty)** — the Terminal-Bench 2.0 grader population at pin `2fd12b88`, read as one population:
  305 test functions over 88 tasks, 183 of 184 capture files committed (the operator-excluded
  `sanitize-git-repo/tests/test_outputs.py` stays absent by design and its pin-tree blob still matches). The frozen
  AST classifier `plans/round53_c1_classify.py` (sha256 `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6`)
  puts 52 tests in `P1` and 253 in `P0`; eight blind seats, each test labelled by exactly two seats of different role,
  decide all 305 with `disagree=0` against the frozen 9.2 % limit and `contested=0` (`ORACLE … decided=305
  oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000`), and the non-vacuous
  control fires (`ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes` — the round-52
  classifier disagrees on 23 decided tests). Wave 2 confirmed **20 never-read presence-only tasks** (`CONFIRM
  candidates_never_read=28 new_confirmed=20 rejected=0 target>=3`; five readers × 4 tasks; receipt
  `corpus/evidence/round53/confirmations.json`, 20 rows, all `confirmed: true`, committed at `9ead4476`).
  **The round's verdict is not admitted at the measured revision**: the PRIOR-ART leg holds no rows
  (`PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0 urls=0 rejected=0`), so the frozen predicate prints
  `PREDICATE R53-C1 fail` (exit 1) and novelty stays 8. Prior-art pricing for the 20 tasks is wave-3 work in flight;
  the final verdict is `[pending: prior-art rows for the 20 confirmed tasks and the L1's scored run at the landing tip]`.
- **R53-C2 (calibration)** — the registry's own tip-state was undeclared: 75 rows at the base tip with no ledger
  (`ROWS registry=75 ledger=0 missing=75`, receipt `.ufo/waves/round-53/claims/c2-before-head.txt`), and a manual
  base-tip probe found 22 rows exiting non-zero and 13 with no runnable argv in the cell
  (`.ufo/waves/round-53/claims/c2-before-manual-probe.txt`). The amended counter now pins the row set (78 names = the
  75 frozen + `round53-c1`, `round53-c2`, `stage-scan`), declares a tip-state per row in `plans/round53-tipstate.json`
  (78 rows: 74 `entry` + 4 `selftest`; 66 green, 12 red) and re-executes every argv. The static legs hold at
  `9ead4476` (`ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0
  duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok`, `--dry`). The re-execution leg is still open: the
  run-1 receipt (`.ufo/waves/round-53/claims/c2-run1.txt`, clean shared clone of `1ebf61f`, host load ~100–130) printed
  `RUN executed=77 timeout=0 mismatched=18 evidence_missing=1`,
  `TIPSTATE declared_green=49 declared_red=28 observed_green=63 observed_red=14`, `PREDICATE R53-C2 fail`, exit 1 —
  16 rows the wave-1 seats had measured red at `1373b6c` were green at `1ebf61f` (the `corpus/README.md` index repair
  of `d40b705` removed the package gate's P8 failure), `round46-c1` exited 1 under load although it exits 0 alone,
  and one red row's evidence fragment was absent. The L1 corrected the ledger from those observations (`58746180`);
  the verdict is `[pending: the wave-3 independent re-measurement seats C2MeasureExecA / C2MeasureExecB]`, and
  calibration stays 9 until then.
- **Confirmations (the C1 CONFIRM leg)** — 20 distinct never-read tasks with a v2 `P1` test, each confirmed by a
  reader who is neither an author nor a labeller, each with a quote inside the test function's own line span
  (`.ufo/waves/round-53/w2/C1ConfRead{A,B,C,D,G}.md`, parts under `.ufo/waves/round-53/w2/C1ConfRead*/`; the two
  dispatched reader seats `C1ConfReadE` and `C1ConfReadF` left no report). 28 never-read candidates carried a v2 `P1`
  test (`.ufo/waves/round-53/claims/c1-candidates.txt`); 20 of them were confirmed.
- **Sources** — `[pending: the L1 assigns SOURCES ids from S194 for the rows the wave-1 scouts and the wave-3
  literature scout open; the census round-start is 186 rows and 15 pre-existing W04 duplicate-url warnings, exit 0
  (`grep -c '^| S[0-9]' corpus/SOURCES.md` → 186)]`. The knowledge entry that lands cites them.
- **Mined mistakes** — the wave-1 attacks themselves are the round's mined mistakes: the frozen counters were
  reachable without the work (`counter-reachable-without-the-work`, re-met and captured: an all-`P1` stand-in
  classifier with labels copied from it gave `PREDICATE R53-C1 pass`), the C1 selftest killed 25 of 81 mutants and the
  C2 selftest 28 of 69, `rule-unit-leak` (repaired) and `false-registry-cell` (the ledger) are the carried lesson
  (`corpus/lessons/round-53.md` is drafted by the round's lesson seat).
- **Carried routed defects (closure of round 52)** — (2) the untracked `tb2-paper-full.html` is deleted before landing;
  (3) absolute host paths in the round-52 `confirmations.json` stay as landed history, while the round-53 evidence uses
  repo-relative paths only (enforced by the CONFIRM leg); (4) the C2 `SELFTEST-UNBACKED` span fix and the K5/K7
  controls stay carried, not claimed. `[pending: the revenger seat's verification of (2)–(4) at the landing tip]`.

Evidence: `plans/round-53-claims.md`, `.ufo/waves/round-53/facts.md`, `.ufo/waves/round-53/claims/`,
`.ufo/waves/round-53/w1/`, `.ufo/waves/round-53/w2/`, `.ufo/waves/round-53/w3/`,
`corpus/evidence/round53/confirmations.json`, `corpus/lessons/round-53.md`.
