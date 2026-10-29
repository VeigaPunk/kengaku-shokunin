# Round 53 — facts (L1 KengakuR53) — read before you write a number

Every figure below carries its command or pointer. `[pending: …]` means the L1 has not measured it: write the placeholder, never a guess.

## Commits (lane branch `master`)
| what | hash |
|---|---|
| base tip (round-52 closure) | `536925b5320fa64298030b4ee76a58fc4b82723f` |
| claims, counters v0, pin tree, tests index, label shards, before receipts | `a34838f82c9e808577c646442797f5a15583eae7` |
| wave-1 spec/dispatch, P1 definition | `1373b6ca34c345635fe8d52f8130e71824f991c4` |
| amendment A1, final classifier + freeze file (one commit), README index repair | `d40b7055e0128d7998d09548fdeef431093ab321` |
| the eight label files (strictly after the freeze commit) | `db90a6b7ecc9501e2e5de239a8794c5aa19cbf8d` |
| registry rows `round53-c1`/`round53-c2`, initial ledger | `1ebf61f81f058a7a255cc23206e50a5331121b5b` |

## Wave 1 (35 seats; `.ufo/waves/round-53/w1/<seat>.md`)
Role mix: executor 13, scout 9, reviewer 6, critic 2, mutation-tester 2, scribe 1, connector 1, sentinel 1 (`python3 .ufo/waves/round-53/build_spec_w1.py`). Pending at writing: `C1RevCounter`, `C2RevCounter` queued behind the host's concurrency cap (they review the pre-A1 counters; their reports, if they arrive, are historical).

**Wave-1 attacks on the FROZEN counters (all landed; A1 in `plans/round-53-claims.md` closes them; none had scored a claim):**
- `C1CritCounterReach`: 13 routes; headline — an all-`P1` stand-in classifier + labels copied from it + forged evidence gave `PREDICATE R53-C1 pass` (`.ufo/waves/round-53/w1/C1CritCounterReach/results/composite-fixture.txt`).
- `C1MutCounter`: 81 mutants, the frozen selftest killed 25 (31 %), an extended 47-case selftest killed 77 (`.ufo/waves/round-53/w1/C1MutCounter/results-pristine-suite.json`, `results-kill-cases-suite.json`).
- `C2CritLedgerReach`: 20+ routes (zero rows, renamed heading, 70 of 75 rows, `python3 -c pass <script>` as argv, non-git source, older source) (`.ufo/waves/round-53/w1/C2CritLedgerReach/out/SUMMARY.txt`).
- `C2MutCounter`: 69 mutants, frozen selftest killed 28, an augmented 41-case selftest killed 60 (`.ufo/waves/round-53/w1/C2MutCounter/mutation-table.md`).
- `C1SentinelScreen`: 3 HIGH, 4 MEDIUM, 2 LOW; the capture corpus is clean (183/183 blob matches, no credential-shaped strings).
After A1: `python3 plans/round53_c1_triage.py --selftest` → `SELFTEST cases=<n> failures=0` and `python3 plans/round53_c2_tipstate.py --selftest` → `SELFTEST cases=50 failures=0` (n printed by the command; receipts `.ufo/waves/round-53/claims/c1-selftest.txt`, `c2-selftest.txt`).

## C1 — measured at `db90a6b` in a clean shared clone, under `bwrap --unshare-net` (receipt `.ufo/waves/round-53/claims/c1-after-oracle.txt`)
```
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4
ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)
ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes
CONFIRM candidates_never_read=28 new_confirmed=0 rejected=0 target>=3
PRIOR-ART rows=0 tasks_covered=0/0 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1
PREDICATE R53-C1 fail      (confirmations and prior art are wave 2's work)
```
- Classifier `plans/round53_c1_classify.py` sha256 `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6`: `P1=52 P0=253` over the 305 ids, P1 in 41 of 88 tasks (`.ufo/waves/round-53/w1/C1ExecClassifier/fix-round-receipt.txt`); own `--selftest` 83 cases.
- Independent adversarial set (`C1ExecAdvCases`, derived from the spec, not from labels): before the fix round 14 of 90 cases / 22 of 371 tests failed; after, 0 / 0 (`python3 .ufo/waves/round-53/w1/C1ExecAdvCases/check.py plans/round53_c1_classify.py`); the fix round moved 0 of the 305 population ids.
- A second implementation (`C1ExecClassifierAlt`, abstract interpretation over {path-exists-only, other}) disagreed with the classifier on 1 of 305 ids before the fix round (`financial-document-processor::test_original_documents_dir_empty`).
- Label seats: eight blind seats, each test labelled by exactly two seats of different role (scout and reviewer); Y counts per seat 13, 11, 12, 16, 14, 15, 13, 10 (sum 104 = 2 × 52); `contested=0`, `U` never used; each report states it read only the spec, its shard and the capture bytes. The perfect agreement is a RESULT to be attacked (`C1CritOracle`), not a verdict.
- Round-52 classifier on the same bytes: disagrees on 23 decided tests (control); an all-P0 classifier disagrees on 52.
- 28 never-read candidate tasks with a v2 P1 test: `.ufo/waves/round-53/claims/c1-candidates.txt` (`python3 plans/round53_c1_triage.py --lane . --candidates`).
- Confirmations: [pending: wave-2 readers `C1ConfRead*`]. Prior art: [pending: `C1PriorArt*`]. Touch-run (empty stub world, actual pytest): [pending: `C1ExecTouch*`]. Re-label (80 tests, blind): [pending: `C1RelabelRev*`].

## C2 — registry tip-state
- Registry rows: 75 at the base tip (`python3 plans/round53_c2_tipstate.py --lane . --dry` at `536925b` → `ROWS registry=75 ledger=0 missing=75`), 77 after the two new rows.
- Base-tip manual probe (one run per row in a clean shared clone, `.ufo/waves/round-53/claims/c2-before-manual-probe.txt`): 73 rows parsed, 60 runnable as written: 38 exit 0, 22 exit non-zero, 13 with a placeholder in the entry cell.
- Wave-1 ledger (`C2ExecRowsA…I`, 75 rows measured in clean clones at `1373b6c`): 45 green entry + 2 green selftest + 28 red entry (`plans/round53-tipstate.json` before the L1 re-measurement; 74 entry argv + 3 selftest in the 77-row ledger).
- One real defect explained ~16 of the red rows: `corpus/knowledge/fixture-honest-geometry.md` (round 50) had no row in `corpus/README.md`, so the package gate's check P8 saw 56 files against 55 index rows. Repaired in `d40b705` (index row added); `grep -c '^| `knowledge/' corpus/README.md` → 56, `ls corpus/knowledge | wc -l` → 56.
- Remaining red causes named by the seats (to be re-measured): `round51-surfaces` NUMBER-DRIFT (SF14 row claims 171 SOURCES rows), `state-assertion-check` (SHONEN box-4 pointer `PROVINCE.md:129` — the `### Adjacent` heading moved to line 130), `round35-c1-coverage` V4 hard-codes 42, `round52-c1` (literal 183/184 predicate), `anchor-digest-check` (21 rows S173–S193 carry a sha256 anchor but no capture locator), `gate-flip-check` (three unresolved round-52 refusals), `mutant-direction-check` (N21 mislabelled), `round38-c1-mutants` (N21 survives), `adoption-check` (hard-coded fleet path).
- Full-counter run on the 77-row ledger: [pending: `.ufo/waves/round-53/claims/c2-run1.txt`].

## Frontier
- Census round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 15 W04 duplicate-url warnings, `ok`, exit 0, 186 rows (`grep -c '^| S[0-9]' corpus/SOURCES.md` → 186).
- Wave-1 source scouts archived 4 groups under `.ufo/waves/round-53/w1/C1ScoutSrc*/fetched/` (draft rows `S9xx`/`S94x` are placeholders). Source scribes finalise; ids are assigned by the L1 from S194.
- Mistakes mined: the wave-1 attacks themselves (`counter-reachable-without-the-work` re-met a second time and captured), `rule-unit-leak` (repaired), `false-registry-cell` (the ledger).
