<!--
Draft for the SCORECARD.md `## Round 53` section. L1 owns the landed text; this file is the seat's proposal.
Every number below carries its command or a pointer. `[pending: ...]` marks anything the L1 has not measured.
Nothing here sets a score change: no claim is declared verified by this seat.
-->

## Round 53 (hyaku run 11, 2026-10-28 → 2026-10-30): a blind-oracle presence-only triage of the Terminal-Bench 2.0 graders (C1 fail on the prior-art leg only); every registry row's tip-state declared and re-executed (C2 re-measurement pending)

Base tip `536925b5320fa64298030b4ee76a58fc4b82723f`; claims frozen at `a34838f82c9e808577c646442797f5a15583eae7`
(`plans/round-53-claims.md`; amendments A1 at `d40b7055e0128d7998d09548fdeef431093ab321`, A2 at
`56fdff79911407a84f5ebf43d40c9fe04fab0427`, A3 at `7095e857…` — each dated before any scored after-run, frozen text
unedited). L1 `KengakuR53`; hyaku run 11 re-dispatch. Three waves: wave 1 build (35 seats,
`python3 -c "import json;print(len(json.load(open('.ufo/waves/round-53/w1-spec.json'))['items']))"` → `35`), wave 2
falsify/confirm (42 seats dispatched, same command on `w2-spec.json` → `42`; the 2026-10-28 operator wrap-up stopped it
after five of its seven confirmation readers had delivered), wave 3 (32 seats, `w3-spec.json` → `32`: pricing,
touch-run, blind re-label, re-attack, independent re-measurement, sources, entry/lesson/log). Attack share by role:
wave 1 — 2 critic + 2 mutation-tester + 1 sentinel of 35; wave 2 — 4 critic + 3 mutation-tester of 42; wave 3 —
4 critic + 2 mutation-tester + 1 sentinel of 32 (`w3-spec.json` roles). Lowest non-retired axis is coverage 7, capped
by the open L0 questions `kengaku | round-25`, `round-33` and `round-51` (`.ufo/l0-questions.md`), none answered; the
round works novelty (8→9) and calibration (9→10) as rounds 48–52 worked the 8s and 9s. Stagnation nudge not invoked
(coverage 7 < saturation line 8). Lane tip at this seat's clone time: `9ead4476bf55b1ea6490d0204b668195db4a4d1d`
(`git -C <clone> rev-parse HEAD`); the lane tip when the seat started was `b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe`
(`git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD`) — the lane advanced under the seat, so the
`9ead4476` measurements below are the ones that count.

| claim | axis | before (frozen command, base tip) | after target | measured after (revision `9ead4476bf55b1ea6490d0204b668195db4a4d1d`) |
|---|---|---|---|---|
| R53-C1 presence-only grader triage v2, TB2 pin `2fd12b88` | novelty 8→9 | `python3 plans/round53_c1_triage.py --lane .` on a clean clone of the base tip → receipt `.ufo/waves/round-53/claims/c1-before.txt`: `PINS population_sha=ok pin_tree_sha=BAD tests_index_sha=BAD captures_blob_match=0 blob_bad=0 absent=0 excluded_blob=BAD files=-1`, `FREEZE absent freeze=False classifier=False labels=False`, `ORACLE not evaluable (pins, classifier, freeze or labels absent)`, `CONFIRM new_confirmed=0`, `PRIOR-ART rows=0`, `PREDICATE R53-C1 fail` (exit 1) | all five legs hold: `PINS … ok`; `FREEZE clean=yes`; `ORACLE` decided = 305 with `disagree ≤ 3 %` and `contested ≤ 15 %`; `ORACLE-CONTROL control_ok=yes`; `CONFIRM new_confirmed ≥ 3` (one row per confirmed task, never-read, quoted inside the test span, reader neither author nor labeller); `PRIOR-ART` ≥ 3 distinct URLs, ≥ 1 `phenomenon-new`, one row per confirmed task | `PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok r52_audit_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184`; `FREEZE clean=yes classifier_and_freeze_one_commit=yes classifier_sha=ok label_files_pinned=ok shards_pinned=ok labels_after_freeze_and_untouched=yes authors=4`; `ORACLE tests=305 bad_label_files=0 bad_label_rows=0 decided=305 contested=0 oracle_Y=52 oracle_N=253 v2_P1=52 unclassified=0 disagree=0 limit=9.2 per_label_agree=1.000 (min 0.9)`; `ORACLE-CONTROL r52_classifier_disagree=23 all_P0_disagree=52 control_ok=yes`; `CONFIRM candidates_never_read=28 new_confirmed=20 rejected=0 target>=3`; `PRIOR-ART rows=0 tasks_covered=0/20 known=0 new=0 urls=0 rejected=0 target: urls>=3 new>=1`; `PREDICATE R53-C1 fail` (exit 1) — the four non-prior-art legs hold; the PRIOR-ART leg holds no rows |
| R53-C2 every registry row's tip-state declared and re-executed | calibration 9→10 | `python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of the base tip> --work <scratch>` → receipt `.ufo/waves/round-53/claims/c2-before-head.txt` (3 lines): `ROWS registry=75 ledger=0 missing=75 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0`, `  MISSING adoption-check`, `  MISSING anchor-digest-check`; the same before-run's `LEDGER ledger absent: plans/round53-tipstate.json` and `PREDICATE R53-C2 fail` are quoted in `plans/round-53-claims.md` | `ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok`; every argv re-executed with the declared exit code, `mismatched=0 timeout=0 evidence_missing=0`, `clean=yes` | static legs hold at `9ead4476`: `ROWS registry=78 ledger=78 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0 bad_table_lines=0 headings=1 row_set_pinned=ok` and `ARGV entry=74 selftest=4 help=0 help_limit=7.8` (`python3 plans/round53_c2_tipstate.py --lane . --source . --dry`; the receipt's own line `DRY static legs only: no predicate`, exit 0). The re-execution leg at the landing tip is `[pending: the wave-3 independent re-measurement seats C2MeasureExecA / C2MeasureExecB]` |

Receipts: `.ufo/waves/round-53/claims/` (`c1-before.txt`, `c1-after-oracle.txt`, `c1-candidates.txt`, `c1-selftest.txt`,
`c2-before-head.txt`, `c2-before-manual-probe.{py,txt}`, `c2-run1.txt`, `c2-selftest.txt`, `c2-a3-redbefore.txt`).

### Round 53 — verdicts

- **R53-C1 — not admitted at the measured revision; novelty stays 8 pending the prior-art pricing.**
  The frozen kill rule is failing on the **PRIOR-ART leg alone** (`PRIOR-ART rows=0 tasks_covered=0/20 …`,
  `PREDICATE R53-C1 fail`, exit 1). The other four legs hold at `9ead4476`: the pins (183/183 capture blobs match,
  the operator-excluded capture stays absent and its pin-tree blob still matches), the freeze (classifier sha256
  `935db122897149a6013ca06d0001feaba4da04d606adc8197c9ff1acf8f1d0e6` — `sha256sum plans/round53_c1_classify.py` — plus the
  label files added strictly after the freeze commit and untouched since), the oracle (305 of 305 decided,
  `disagree=0` against a 9.2 % limit, `contested=0`, `per_label_agree=1.000`, and the non-vacuous control
  `r52_classifier_disagree=23 ≥ 2 × 0`), and CONFIRM (`new_confirmed=20 rejected=0` — 20 distinct never-read tasks,
  four each from the five wave-2 readers `C1ConfReadA`, `C1ConfReadB`, `C1ConfReadC`, `C1ConfReadD`, `C1ConfReadG`;
  `python3 -c "import json,glob; …"` over `.ufo/waves/round-53/w2/C1ConfRead*/confirmations-part.json` → 20 rows,
  20 distinct tasks; the integrated receipt is `corpus/evidence/round53/confirmations.json`, 20 rows, all
  `confirmed: true`, committed at `9ead4476`). Prior-art pricing for those 20 tasks is wave-3 work in flight
  (`C1PriceScoutA`–`C1PriceScoutE`), so the round's final C1 verdict is
  `[pending: prior-art rows for the 20 confirmed tasks and the L1's scored run at the landing tip]`. The 305/305
  oracle agreement is a result to be attacked (`C1CritOracle2`), not a verdict.
- **R53-C2 — `[pending: the wave-3 independent re-measurement]`; calibration stays 9 until the L1 declares it.**
  The static legs of the amended counter hold at `9ead4476` (row set pinned, 78 = 78, no missing/extra/mismatched
  entry, no bad declaration or reason, one heading). The re-execution leg is the open question: the run-1 receipt
  `.ufo/waves/round-53/claims/c2-run1.txt` (clean shared clone of `1ebf61f`, 5 jobs, host load ~100–130) printed
  `ROWS registry=77 ledger=77 missing=0 extra=0 …`, `RUN executed=77 timeout=0 mismatched=18 evidence_missing=1`,
  `TIPSTATE declared_green=49 declared_red=28 observed_green=63 observed_red=14`, `PREDICATE R53-C2 fail`, exit 1; the
  L1 then corrected the ledger from those observations (commit `58746180`), and the committed ledger now declares
  78 rows (74 `entry` + 4 `selftest`; 66 green, 12 red —
  `python3 -c "import json,collections;d=json.load(open('plans/round53-tipstate.json'));print(len(d['rows']),collections.Counter(v['kind'] for v in d['rows'].values()),collections.Counter(v['state'] for v in d['rows'].values()))"`).
  Whether the corrected ledger survives a fresh re-execution at the landing tip is
  `[pending: C2MeasureExecA / C2MeasureExecB receipts]`. The red rows the facts name as real (not artefacts) —
  `round51-surfaces` (SF14 claims 171 SOURCES rows against 186), `state-assertion-check` and `round28-census`
  (SHONEN box-4 pointer `PROVINCE.md:129` is a blank line), `round35-c1-coverage` V4 (hard-coded 42),
  `round38-c1-mutants` / `mutant-direction-check` (frozen mutant N21), `round46-c3` V7/V8, `round52-c1` (literal
  183/184), `anchor-digest-check` (rows S173–S193 carry a sha256 anchor but no capture locator), `gate-flip-check`
  (S191–S193 flips unresolved), `adoption-check` (hard-coded fleet path), `round40-c1-mutants` — must each carry a
  declared red with a ≥ 10-word reason and a verbatim evidence fragment for the leg to pass.
- **No axis harmed and no axis moved:** coverage 7, calibration 9, depth 9, freshness 9, adjacency 9 held; novelty 8
  held; operability 9.

Axis state carried: calibration 9, coverage 7 (L0 `kengaku | round-25`, `round-33`, `round-51` cap), novelty 8,
depth 9, operability 9, freshness 9, adjacency 9.

### Round-53 capabilities

Rows enter the capabilities table only for a capability that RAN this round with a pointer, and only with a verdict the
facts support. Nothing enters yet this round; the two candidate rows are listed with their state.

| capability | state |
|---|---|
| presence-only grader triage counter (`plans/round53_c1_triage.py`) | **runs; verdict not admitted** — the amended counter runs clean at `9ead4476` (`PINS`/`FREEZE`/`ORACLE`/`ORACLE-CONTROL`/`CONFIRM` all hold) but the frozen predicate still fails on the PRIOR-ART leg (`rows=0`), so no row enters the capabilities table; `--selftest` `cases=47 failures=0` (`.ufo/waves/round-53/claims/c1-selftest.txt`) |
| registry tip-state counter (`plans/round53_c2_tipstate.py`) + ledger (`plans/round53-tipstate.json`) | **runs; re-execution verdict pending** — the static legs hold (78 = 78 rows, pinned row set) but the re-execution leg is the wave-3 re-measurement; `--selftest` `cases=52 failures=0` (`.ufo/waves/round-53/claims/c2-selftest.txt`); the counter is already a tool row in `SKILL.md`'s Gate/probe registry (`round53-c2`), which is an existence fact, not a truth gate |

Two further instruments ran this round and are recorded as evidence, not as capability rows: the frozen classifier
`plans/round53_c1_classify.py` (sha256 `935db122…`, `P1=52 P0=253` over the 305 ids, own `--selftest` 83 cases,
`.ufo/waves/round-53/w1/C1ExecClassifier/fix-round-receipt.txt`) and `plans/stage_scan.py` (33-case selftest, landed
with its registry row `stage-scan`).

### Planned (round 54)

Start from what this round left open, not from a new surface. (1) **C1**: land the prior-art pricing for the 20
confirmed never-read tasks (`corpus/evidence/round53/prior-art.json`, one row per confirmed task, ≥ 3 distinct URLs,
≥ 1 `phenomenon-new` with its negative sweep) and re-run the frozen counting command on a clean clone of the landing
tip so the PRIOR-ART leg is measured rather than assumed; the kill rule decides novelty, not the L1's preference.
(2) **C1's remaining attacks**: the 305/305 oracle agreement and the 20 never-read confirmations are both under
wave-3 attack (`C1CritOracle2`, `C1CritNeverRead`) — carry their verdicts into the admission decision; the blind
re-label of 80 tests (`C1RelabelRev1`–`C1RelabelRev4`) is the third-party check on the oracle.
(3) **C2**: re-measure the 78-row ledger at the landing tip from two independent runs (`C2MeasureExecA`/`B`) and land
the ledger correction the observations force; a row whose observed exit differs from its declared exit, any timeout,
any missing row or any `--only` run is a fail, not a narrowing.
(4) **Repair the reds that are real**: the eleven named red causes above (the SOURCES row count in SF14, the
`PROVINCE.md:129` pointer, the hard-coded 42 and 183/184 literals, the S173–S193 anchor rows without capture
locators, the three unresolved round-52 gate flips, the frozen mutant N21, the hard-coded fleet path) are round-54
work, and each repair must be able to fail.
(5) **Coverage** stays capped at 7 by the open L0 questions `kengaku | round-25`, `round-33`, `round-51`; no round-53
output changes that cap and none of it may be written as if it had.
