# Round 39 — frozen claims (kengaku, hyaku run 8, 2026-10-26)

Baseline lane tip `b2bdd425fbc042d3075994dae60fe88a51e277ab` (the round-38 non-author spot-check). L1 `KengakuR39`
holds the canonical planner seat. Written and frozen before any `plans/battery39` fixture exists and before the
first recorded run of `plans/git_leak_probe.py`.

**Order of operations (round-38 closure R3; `corpus/lessons/round-38.md` §Mistakes row 2).** Before this file was
committed the probe ran only as `--dry` (no sandbox) and `--stage-check` (builds each case's repository state in the
sandbox and prints stage exit codes only; the grader module is never imported — `plans/git_leak_probe.py` HARNESS_PY
exits before `spec_from_file_location` in `stage` mode): `stagecheck cases=25 failed=0`. The C2 do-nothing control
ran the gate with `--rerun`, but with no receipt on disk the gate's P10 returns `receipt unreadable` before it
executes anything (`plans/pkg_gate.py:268-270`; `control-c2-nothing.txt`: `P10 DEFECT receipt unreadable`), so the
probe did not run. No skip-control that would make P10 execute the probe is run before the first recorded probe run;
it is run, and committed, after that run.

Axis state carried (SCORECARD round 38): calibration 8, coverage 7, novelty 7, depth 9, operability 8, freshness 8,
adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. Coverage is chosen (tie-break as in rounds 35–38:
a pinned local source and an offline sandbox exist; the round-38 planning seat priced the novelty candidate — an
initial-state pass census — as published TB validation practice, `.ufo/waves/round-38/build/R38PlanNext.md` §4).
Coverage stays capped at 7 by the open L0 question `kengaku | round-33`, so C2 is judged on its counter, not on a
score move. No stagnation waiver. Controls are committed with this file under `.ufo/waves/round-39/claims/`.

## C1 — calibration: the gate behaviours still undemonstrated after round 38, directions witnessed before freeze

- **Surface:** `plans/pkg_gate.py` (unedited, digest `ea638822…`) and what the lane advertises about it — the gate
  docstring, `corpus/QUALITY.md` Q24/Q27, the SCORECARD capability row `package-gate`.
- **Self-assessment vs observed state (the calibration count):** the number of frozen mutants M01–M07 (each one
  advertised behaviour; its `adv` cell names the sentence and marks indirect coverage) that no battery fixture kills
  ATTRIBUTABLY in its declared direction. Sources: round-38 N21 carried with its reachable direction `mirror`
  (round-38 closure R2, `mutant_direction_check.py` `observed=mirror`); the three non-equivalent survivors of
  `F38XMutP` (X01 P1, X05 P3, X15 P7); three of the four survivors of `F38XMutRerunMain` (X07 RUN, X10 MAIN, X15 D5).
  Excluded, with reason: `F38XMutRerunMain` X04 (P10's OSError arm, reachable only through the gate's own
  interpreter/environment — the round-38 B4 exclusion, re-confirmed by that seat's probe A3); `F38XMutP` X06
  (observationally equivalent, withdrawn by that seat). 1 + 3 + 3 = 7.
- **Directions (QUALITY Q29):** every direction is declared in the counter and has a committed pre-freeze witness
  (the counter's `witness` cell: `plans/battery38/d5m.py` `d5m-n21-manifest-row-2`; `F38XMutP/witness-run.txt`
  W-X01/W-X05/W-X15; `F38XMutRerunMain/survivor-probes.txt` A1/A2; `survivor-probeB.txt`). Two exit-code legs are
  new: `rc-silence` (declared reject, reference exit 1, mutant exit 0) and `rc-mirror` (declared accept, reference
  exit 0, mutant exit 1) — round-38 wave 2 `F38XMutRerunMain` finding 2.
- **Counter:** `python3 plans/round39_c1_verify.py --lane .` (docstring = the full rule; pins 26 inputs; battery38 and
  battery39 modules are built in child processes and hand back only JSON — round-38 `R38CritClaims` §2).
- **Frozen predicate:** C1 passes iff `python3 plans/round39_c1_verify.py --lane .` prints `PINS total=26
  mismatched=0`, then `BATTERY fixtures=<n> wrong=0 renamed_disagree=0 sidechannel=0`, then `MUTANTS total=7
  killed=7 survived=0 invalid=0 null_detected=0`, then `PREDICATE C1 pass`, exit 0, measured on a clean clone of
  the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-39/claims/control-c1-nothing.txt` — the same
  command with no `plans/battery39`: `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7
  killed=3 survived=4`, `PREDICATE C1 fail`, exit 1. M01 is killed by the round-38 battery (the relabel alone), M05
  and M06 by round-36/37 fixtures through the new exit-code legs; the claimed work is the four survivors M02, M03,
  M04, M07. Other controls: `control-c1-gate-edited.txt` (one appended line in the gate → `PINS mismatched=1`,
  `invalid=7`); `control-c1-hostile-inproc.txt` (the round-38 in-process `run_gate` patch as a battery39 module,
  `control-c1-hostile-inproc-module.py` → unchanged `killed=3 survived=4`: the patch reaches only its child).
- **Work:** `plans/battery39/*.py` single-purpose fixtures (wave-1 executors), battery38 contract.
- **Kill rule:** any survivor, invalid mutant, null detection, `wrong>0`, `renamed_disagree>0`, `sidechannel>0` or a
  pin mismatch at landing → C1 not admitted, reported as an honest stop. A mutant later shown equivalent is reported
  as a limit, never removed or relabelled. The round-37 and round-38 counters, batteries and lists are not edited;
  at the landing tip the round-37 counter must still print `PREDICATE C1 pass` and the round-38 counter its landed
  `killed=21 survived=1` (no-harm checks).
- **Limits named now:** a kill records a result difference in the declared direction, not the fixture's intent; the
  side-channel scan is a token heuristic, so battery39 code review by a non-author seat remains part of admission;
  a child process can still leave a process that outlives it (the counter digest-checks the gate copies after each
  mutant, it does not police processes). Three of the seven `adv` cells cover their behaviour only indirectly
  (marked in the cell).

## C2 — coverage: the pinned TB2 `git-leak-recovery` grader, a fifth grader class (repository-history state)

- **Surface:** `corpus/knowledge/` (new entry `tb2-git-leak-recovery-grader.md`), `corpus/SOURCES.md` (S117
  `tests/test_outputs.py`, S118 `instruction.md`, terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`,
  opened 2026-10-26 03:27 -03 by the L1), README index row + coverage bullet, PROVINCE paragraph; one §Frontier TB2
  sub-bullet narrowed by one task. Edge class new to the lane: the graded state is a git repository's object store
  and refs plus one flag file, checked by `git log --all` greps, `git fsck` dangling objects and a work-tree checksum.
- **Probe (frozen):** `plans/git_leak_probe.py` (digest `4961a50f…`), 25 cases, predictions and `violates=` tags in
  `corpus/evidence/round39/git-leak-dry-cases-freeze.txt` (digest `e92a5d6d…`; `cases=25 predicted_pass=13
  predicted_fail=12`). Eight predictions copy the round-38 pilot's observations on this host (named in the probe
  docstring); the rest are a static reading. Captures `corpus/evidence/round39/tb2-git-leak-recovery/` (7 files +
  `SHA256SUMS`).
- **Counter:** `python3 plans/round39_c2_verify.py --lane .` — the round-38 counter's V1–V7 re-pointed at this package
  (spec, gate, probe, dry table and captures pinned); no check added or relaxed.
- **Frozen predicate:** C2 passes iff `python3 plans/round39_c2_verify.py --lane .` prints `checks=7 defects=0`,
  then `PREDICATE C2 pass`, exit 0, measured on a clean clone of the landing tip.
- **Before (do-nothing control, this freeze):** `.ufo/waves/round-39/claims/control-c2-nothing.txt` → `checks=7
  defects=4` (V2, V3, V4, V7), exit 1.
- **Kill rule:** predicate not met at landing → not admitted. Prediction mismatches are allowed only when each
  `match=NO` case is named in the entry (V4); they are reported, never edited out of the table.
- **Limits named now:** host git 2.56.0 and bash stand in for the image's Ubuntu git and dash; the image is never
  pulled; the setup runs unprivileged. The finding class "a do-nothing or partial agent passes most tests" is
  published TB validation practice (R38PlanNext §2.5, to be opened by a wave-1 seat); the entry claims a probed
  instance only. Known informed-filler limit of V1–V7 carried from round 38 (`R38CritC2Counter` §1).

## Separability

C1 reads only the gate, the round-35 spec, the round-36/37 counters, batteries 37/38 and `plans/battery39`; C2 reads
only its captures, spec, probe, receipt, entry, SOURCES and README. Neither counter reads the other's work product:
C1 can pass with C2 absent and vice versa. The gate digest is shared and frozen for both.

## Frontier step (not a claim)

- Sourced claim: C2 (S117/S118 opened this round).
- Mined mistake: the order-of-operations class recurred twice (round 37 lesson row 3, round 38 lesson row 2). Fix:
  a gate that reads git history and fails when a committed control shows the frozen probe executed before the
  first receipt commit — shown red on round 38's freeze, green on this round's — and the class recorded with
  `recurrence=2` in `corpus/defects.jsonl`. This is `considerthese/2026-10-25.md` proposal 2(b) (block
  pre-registration when a class recurs twice), the one still unbuilt.
- Routed items carried from `corpus/lessons/round-38-verifier-spotcheck.md` §5: R1 (commit and integrate round-38
  wave-2 outputs), R2 (C1 re-freeze — this C1; `adv` wording errata; direction-check redundant leg), R3 (the gate
  above + lesson correction), R4 (recheck commands that red as written), R5 (anchor-check locator union; ledger-tip
  stale ref provenance), R6 (carried wording).
