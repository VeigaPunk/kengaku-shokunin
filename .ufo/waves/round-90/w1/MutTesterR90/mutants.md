# R90 MutTesterR90 — mutation battery over the three instruments

Seat: MutTesterR90 (leaf). No subagents, no commits, no mutating git in any repo. Lane clone
`$S/lane` was only read (`git -C … show | cat-file | archive`). Scratch removed after receipts were copied.

Revisions: BASE `dcdd494e` (do-nothing), pin commit B `664435cf` (instruments), lane HEAD during this
run `a2b22609` (receipt + ledger flip). `git diff --stat 664435cf a2b22609 -- plans/` names only
`plans/grader-population-ledger.json`; the three instruments and the probe are byte-identical at B and
HEAD. The C3 gate reads `corpus/routed-findings.jsonl`, identical at BASE, B and HEAD.

Pristine instrument sha256 (bytes at B): round90_c1_replay.py `611226af23d5831c`,
round90_counter_pin.py `fa841f5906609274`, round90_burndown.py `bacaf2521c5acdf2`;
probe `2c4f0ab1e0d4…` equals `TRUSTED_TOOL_SHA`.

## Method
- **Mutants**: 35 single-site mutants (C1 17, C2 7, C3 11), one scratch copy of the B bytes each, edited
  with hashline `edit` (one site per copy; diffs in `receipts/mutant-diffs.patch`). Two composites
  (`C2-BYT+STG`, `C3-SUP+STG`) show what the always-green mutants hide. Mutants were applied to scratch
  copies, never to the clone's working tree; the clone was not checked out, and each instrument was run
  by path with `--lane <clone> --rev <rev>`.
- **Committed-battery observables** (stdout + stderr + rc): C1 at BASE, B and HEAD (`c1-base`, `c1-B`,
  `c1-tip`); C2 at BASE, B, HEAD and `--selftest` (`c2-*`); C3 at BASE, B, HEAD (`--freeze-round 90`) and
  `--selftest` (`c3-*`). 123 runs. A mutant is "killed by the committed battery" when any of them differs
  from the pristine run, "survivor" otherwise.
- **Fixtures** (not committed; built as plumbing commits in a bare fixture repo under scratch): C1 F0–F13
  (F0 base sanity; F1 receipt absent / ledger-only control; F2 forged non-ancestor LANE_TIP; F3 probe bytes
  changed with unchanged behaviour; F4 grader comment; F5 stamp SUBJECT_SHA; F6 CASE drift; F7 EXIT drift;
  F8 non-CASE line inside the block; F9 predicate drift; F10 table drift; F11 ledger row unexecuted;
  F12 executed total moved by an unfrozen class; F13 one class cell moved). The fixture repo holds
  the freeze commit A's table path objects imported with `cat-file` (so L4 resolves) and a fixture
  ancestor commit used in place of B for `LANE_TIP` (so L3 resolves). C2 F0–F6 (pinned files at B with
  one edit each). C3 real-mode fixtures (two, so checks run) and file-mode fixtures (eight, `--file`).
  About 430 fixture runs. A fixture kill = stdout or rc differs from the pristine run on the same fixture.
- **Necessary vs redundant (Q65)**: "redundant" names the leg that still catches the same defect; a
  mutant is "necessary" when no other leg or fixture catches its defect at the verdict level.

## Results
- Committed battery kills **15 of 35** single mutants (C1-G1, G4, G7, G8, L7E, L7C, TGT; C2-ABS, BYT,
  BLB, MIS; C3-FRZ, CHK, CFD, SUP). **20 survive** the committed battery: C1-G2, G3, G5, G6, L2S, L3A,
  L5P, L5E, L5C, L6; C2-RAB, DUP, STG; C3-FRB, MAL, DUP, SUN, CLO, BLK, STG. Each survivor has a fixture
  that catches it, except C2-STG and C3-STG, which no single-defect run exposes (only the composites:
  the selftest exit is the single signal, and it is green when a red case exists).
- Verdict-level catches: 30 of 35 single mutants flip the rc in some run (C1 14 of 17, C2 6 of 7,
  C3 10 of 11). The five that do not: C1-L5P and C1-L5C (line-level only; L6 holds the rc on the same
  receipt), C1-TGT (informational TARGET field), and C2-STG and C3-STG (flip only inside their composites).
- Redundant (Q65): C1-L5P (caught by L6-reproduce), C1-L5C (caught by L6-reproduce, under the pinned
  probe), C1-TGT (caught by the L7 defect lines). Partial redundancy: C1-G2 capture half (L6 in F4),
  C1-G5 CASE/summary/predicate sub-checks (L6), C1-L7E for frozen-class drift (L7 cell check).
  Everything else is necessary.

## Findings (frozen elements: reported, not repaired)
1. **F-C3-1 — selftest red for the wrong reason.** `round90_burndown.py --selftest` case
   `closed-check-fails` is red because `evaluate()` calls `run_check(command, lane.root)` in `--file`
   mode, where `FileLane` has no `root` attribute: `AttributeError: 'FileLane' object has no attribute
   'root'` (line 305), rc 1. The case therefore passes `want=1` without testing that a failing check is
   a defect. Consequence: C3-CFD (non-zero check rc not recorded as a defect) survives the selftest; C3-CHK
   turns the selftest red only because removing the check call removes the crash. Repro: a dir with
   `notes.md` and `fixture.jsonl` (`OLD-1` open, `OLD-1-res` closed with `check: "exit 3"`), run with
   `--file fixture.jsonl --freeze-round 90`.
2. **F-C3-2 — two selftest cases are masked.** `supersede-unknown` is red because of the open `OLD-1`
   refusal, and `malformed-refuses` because of the open `OTHER-1` refusal; neither isolates its branch
   (C3-SUN and C3-MAL survive the selftest).
3. **F-C3-3 — checks are not revision-scoped; R82-V8 reads the fleet root.** `run_check` runs each row's
   `check` with `cwd` = `--lane` (the working tree), not `--rev`, and with env limited to PATH/HOME/LANE.
   The `R82-V8` check runs `plans/round83_c2_checks.py v8`, which reads `origin.parent` (the fleet root)
   and the `R83_*` env vars that the gate does not pass. In the real tree it passes (`CHECK v8 ok`, rc 0);
   in any clone it fails (`CHECK v8 fail`, rc 1), so the clone runs at BASE, B and HEAD print an extra
   `DEFECT check-failed R82-V8` line that the BASE transcript does not show. The freeze verdict therefore
   depends on the working tree and where the lane is cloned; the ledger and source lines are rev-scoped,
   the checks are not. The claim's measured-revision wording covers only the ledger.
4. **F-C3-4 — dead code.** `load_ledger` (line 128) and `effective_state` (line 155) are never called;
   `effective_state` also contains two no-op loops (`pass`). Not repaired.
5. **F-C1-1 — coverage gap in the committed C1 battery.** C1-G2, G3, G5, G6, L2S, L3A, L5E, L5C, L5P and
   L6 survive it: the committed runs never exercise L2, L3, L5 or L6 with a defect. The ledger-only and
   forged-tip controls the claim names are realised here as F1 and F2 (not committed). The forged-probe echo
   control was not built; F3 (bytes-only probe edit, same behaviour) exercises the same L8 leg.
6. **F-C3-5 — coverage gap in the committed C3 battery.** The freeze boundary (FRB), malformed rows
   (MAL), duplicate ids (DUP), supersede-unknown (SUN), closed-without-evidence (CLO) and blank source line
   (BLK) are untested by any committed run (plus C2-RAB and C2-DUP on the C2 side).
7. **Design note (not an error).** C1-L5C and C1-L5P are redundant with L6 for the pinned probe: L6 rejects
   any receipt whose observation block differs from the re-run, and the predicate and summary lines are
   inside that block. L5E is necessary because EXIT sits in the stamp, outside the block.

## Mispredicts recorded (predicted vs measured; not repaired)
- C2 BASE: predicted `PIN-MISMATCH absent` rc 1 for each created path; measured `DEFECT SETUP unreadable
  plans/counter-pins-r90.json` rc 2 (the pin file is absent at `dcdd494e`; the setup branch fires before
  any per-path check). Same as the L1 transcript; confirmed here, not a new defect.
- C1 BASE: predicted `defects=N` with N=5; measured `defects=10` (the L7 leg prints one DEFECT line per
  failed count and cell: executed total, five cells, and the row).
- C3 BASE in a clone: one extra `DEFECT check-failed R82-V8` (F-C3-3); the real-tree BASE transcript
  has `R42-R2` only. The `freeze=refused … pending=33` summary line is the same.

## Current-state observations
- Lane HEAD `a2b22609`: C1 positive pass (`executed_rows=34 … cases=8 legs=40`, rc 0); C2 positive pass
  (`PINS checked=7 matched=7`, rc 0); C3 still `freeze=refused oldest_pending_round=39 pending=33`, rc 1
  (the triage the claim lands is not at HEAD). Reported as state, not as a claim result.

## Tooling and environment
- No tool installed or upgraded in this seat. Host python 3.14.8 and git 2.56.0 (`/usr/bin`) were used as is.
  No pacman, no sysctl change (`user.max_user_namespaces` = 122865, read-only observation).
- Writes: only this directory (`receipts/` and `table.md` / `mutants.md`) plus scratch under
  `/fast/scratch/hyaku/kengaku-r90/MutTesterR90`, removed at exit.

## Dead or failing commands (rc, stderr tail)
- `git -C <lane> show dcdd494e:plans/round90_polydiff_probe.py` (probe absent at BASE, my probe) rc 128:
  `fatal: path 'plans/round90_polydiff_probe.py' exists on disk, but not in 'dcdd494e…'`.
- `python3 plans/round83_c2_checks.py v8` in the clone rc 1 `CHECK v8 fail` (F-C3-3; the real tree gives
  rc 0 `CHECK v8 ok`, read-only).
- `round90_burndown.py --file … closed-check-fails` rc 1, Traceback `AttributeError: 'FileLane' object has
  no attribute 'root'` (F-C3-1; reproduced in a fixture dir).
- Two `read` calls raced a file copy once (path not found); repeated after the copy.
- No other committed-battery command returned an unexpected rc: C1 BASE 1, B 1, HEAD 0; C2 BASE 2, B 0,
  HEAD 0, selftest 0; C3 BASE 1, B 1, HEAD 1, selftest 0 (C3 rc values include F-C3-3 in a clone).

## Table (one row per mutant)
Observed values are generated from the stored runs (`receipts/committed-runs.json`,
`receipts/fixture-runs.json`); `RC-FLIP` = return code changed, `line-only` = output changed, rc held.

| id | file | mutation | observable run(s) | expected effect | observed (committed battery; fixtures) | necessary\|redundant | caught_by |
|---|---|---|---|---|---|---|---|
| C1-G1 | round90_c1_replay.py | defect() returns for leg L1-receipt (no record, no DEFECT line) | committed battery + F1-receipt-absent | BASE/B: DEFECT L1 line lost, rc unchanged; ledger-only control F1 (receipt absent, ledger flipped) fails at L1 and would pass with L1 off | committed: c1-base line-only, c1-B line-only; F1-receipt-absent: rc 1->0 (flip) | necessary | committed c1-base, c1-B (line-level); verdict-level: F1 ledger-only control |
| C1-G2 | round90_c1_replay.py | defect() returns for leg L2-subject (both the capture and the stamp site) | committed battery + F5-stamp-subject, F4-grader-bytes | no committed run changes (capture present and stamp matching at every committed rev); F5 stamp drift flips; F4 grader edit: L2 line lost, rc held by L6 because the probe itself refuses an edited grader (rc 2) | committed: unchanged; F5-stamp-subject: rc 1->0 (flip); F4-grader-bytes: rc 1->1 (line-only) | necessary (stamp half); capture half redundant with L6 in F4 | none committed; F5 (verdict); F4 (L6 holds rc) |
| C1-G3 | round90_c1_replay.py | defect() returns for leg L3-tip | committed battery + F2-forged-tip | forged LANE_TIP (not an ancestor) must fail at L3; with L3 off rc 0 | committed: unchanged; F2-forged-tip: rc 1->0 (flip) | necessary | none committed; F2 forged-tip control |
| C1-G4 | round90_c1_replay.py | defect() returns for leg L4-table | committed battery + F10-table-drift | BASE: DEFECT L4 line (table absent at measured) lost; F10 drifted table must flip | committed: c1-base line-only; F10-table-drift: rc 1->0 (flip) | necessary | committed c1-base (line-level); verdict-level: F10 |
| C1-G5 | round90_c1_replay.py | defect() returns for leg L5-vectors | committed battery + F7-exit-drift, F6-case-drift, F9-predicate-drift | F7 EXIT 1 in stamp (outside observation block) must fail at L5; with L5 off rc 0. F6/F9 are also caught by L6 (inside the block) | committed: unchanged; F7-exit-drift: rc 1->0 (flip); F6-case-drift: rc 1->1 (line-only); F9-predicate-drift: rc 1->1 (line-only) | necessary (EXIT line); CASE/summary/predicate sub-checks redundant with L6 | none committed; F7 (verdict) |
| C1-G6 | round90_c1_replay.py | defect() returns for leg L6-reproduce | committed battery + F8-block-note | a non-CASE line added inside the observation block passes L5 and must fail L6 only; with L6 off rc 0 | committed: unchanged; F8-block-note: rc 1->0 (flip) | necessary | none committed; F8 (only L6 sees it) |
| C1-G7 | round90_c1_replay.py | defect() returns for leg L7-ledger | committed battery + F11-ledger-unexecuted, F12-extra-executed-unfrozen-class, F13-class-cell-drift | BASE/B: DEFECT L7 lines lost, rc unchanged; ledger drift fixtures must flip | committed: c1-base line-only, c1-B line-only; F11-ledger-unexecuted: rc 1->0 (flip); F12-extra-executed-unfrozen-class: rc 1->0 (flip); F13-class-cell-drift: rc 1->0 (flip) | necessary | committed c1-base, c1-B (line-level); verdict-level: F11, F12, F13 |
| C1-G8 | round90_c1_replay.py | defect() returns for leg L8-tool | committed battery + F3-probe-bytes | BASE: DEFECT L8 line (probe absent) lost; F3 behaviour-preserving probe edit must flip (L6 cannot see it) | committed: c1-base line-only; F3-probe-bytes: rc 1->0 (flip) | necessary | committed c1-base (line-level); verdict-level: F3 |
| C1-L2S | round90_c1_replay.py | stamp SUBJECT_SHA check (receipt half of L2) replaced by if False | committed battery + F5-stamp-subject | stamp SUBJECT_SHA drift must fail; with check off rc 0 | committed: unchanged; F5-stamp-subject: rc 1->0 (flip) | necessary | none committed; F5 |
| C1-L3A | round90_c1_replay.py | ancestor test in L3 replaced by elif False (resolution kept) | committed battery + F2-forged-tip | forged non-ancestor tip must fail at L3; with ancestor test off rc 0 | committed: unchanged; F2-forged-tip: rc 1->0 (flip) | necessary | none committed; F2 |
| C1-L5P | round90_c1_replay.py | PREDICATE-line check in L5 replaced by if False | committed battery + F9-predicate-drift | predicate line changed to fail must fail at L5 and at L6 (line sits inside the observation block) | committed: unchanged; F9-predicate-drift: rc 1->1 (line-only) | redundant | L6-reproduce (F9 rc held at 1 by L6) |
| C1-L5E | round90_c1_replay.py | EXIT-line check in L5 replaced by if False | committed battery + F7-exit-drift | EXIT 1 in the stamp must fail; L6 does not read the stamp, so only L5 catches it | committed: unchanged; F7-exit-drift: rc 1->0 (flip) | necessary | none committed; F7 |
| C1-L5C | round90_c1_replay.py | per-case observed==predicted check in L5 replaced by if False | committed battery + F6-case-drift | a CASE observed drift must fail at L5 and at L6; with the per-case check off, L6 still holds rc 1 | committed: unchanged; F6-case-drift: rc 1->1 (line-only) | redundant under the pinned probe (L6 rejects any receipt whose CASE lines differ from the re-run; the TOOL_SHA pin rules out a self-consistent mispredict) | L6-reproduce (F6 rc held at 1 by L6) |
| C1-L6 | round90_c1_replay.py | re-run comparison in L6 replaced by elif False | committed battery + F8-block-note | block-internal non-CASE drift must fail at L6 only; with L6 off rc 0 | committed: unchanged; F8-block-note: rc 1->0 (flip) | necessary | none committed; F8 |
| C1-L7E | round90_c1_replay.py | executed-total check in L7 replaced by if False | committed battery + F12-extra-executed-unfrozen-class | executed total moved by a member whose classes are outside the frozen cells must fail; L7 cell check cannot see it | committed: c1-base line-only, c1-B line-only; F12-extra-executed-unfrozen-class: rc 1->0 (flip) | necessary for unfrozen-class drift; redundant with L7 cell check for frozen-class drift (F11, F13 keep rc 1) | committed c1-base, c1-B (line-level); verdict-level: F12, redundant-leg L7C for frozen classes |
| C1-L7C | round90_c1_replay.py | class-cell check in L7 replaced by if False | committed battery + F13-class-cell-drift | a class cell drift with executed total unchanged must fail; executed-total check cannot see it | committed: c1-base line-only, c1-B line-only; F13-class-cell-drift: rc 1->0 (flip) | necessary | committed c1-base, c1-B (line-level); verdict-level: F13 |
| C1-TGT | round90_c1_replay.py | TARGET executed flag set to located only (ignores L7) | committed battery + F11-ledger-unexecuted | informational TARGET field changes; predicate verdict should be unchanged because defect count still drives it | committed: c1-base line-only, c1-B line-only; F11-ledger-unexecuted: rc 1->1 (line-only) | redundant for the predicate (L7 legs still catch every ledger defect) | L7-ledger defect lines (F11, F12, F13 rc 1) |
| C2-ABS | round90_counter_pin.py | absent pinned path: skip instead of PIN-MISMATCH absent | committed battery + C2-F6-absent-pin | absent pinned path must be a mismatch (fail closed); selftest T3 must go red | committed: c2-selftest RC-FLIP; C2-F6-absent-pin: rc 1->0 (flip) | necessary | committed C2 selftest absent-path (rc 0->1); verdict-level: C2-F6 |
| C2-BYT | round90_counter_pin.py | bytes-compare branch replaced by elif False | committed battery + C2-F4-byte-drift | modified pinned bytes must mismatch; selftest modified-counter must go red | committed: c2-selftest RC-FLIP; C2-F4-byte-drift: rc 1->0 (flip) | necessary | committed C2 selftest modified-counter (rc 0->1); verdict-level: C2-F4 |
| C2-BLB | round90_counter_pin.py | record-table blob compare replaced by blob-is-not-None | committed battery + C2-F5-record-drift | modified record-table blob must mismatch; selftest modified-record-table must go red | committed: c2-selftest RC-FLIP; C2-F5-record-drift: rc 1->0 (flip) | necessary | committed C2 selftest modified-record-table (rc 0->1); verdict-level: C2-F5 |
| C2-RAB | round90_counter_pin.py | record-table absent branch: mismatch not counted (pass) | committed battery + C2-F1-record-absent | absent record table must fail closed; no committed fixture has the record table absent (selftest T3 is red by its ghost path) | committed: unchanged; C2-F1-record-absent: rc 1->0 (flip) | necessary | none committed; C2-F1 (verdict) |
| C2-MIS | round90_counter_pin.py | pin-file-missing-entry loop emptied | committed battery + C2-F3-missing-entry | pin ledger missing an expected entry must mismatch; selftest incomplete-pin-set must go red | committed: c2-selftest RC-FLIP; C2-F3-missing-entry: rc 1->0 (flip) | necessary | committed C2 selftest incomplete-pin-set (rc 0->1); verdict-level: C2-F3 |
| C2-DUP | round90_counter_pin.py | duplicate-path check off | committed battery + C2-F2-dup-pin | duplicate pin entry must mismatch | committed: unchanged; C2-F2-dup-pin: rc 1->0 (flip) | necessary | none committed; C2-F2 (verdict) |
| C2-STG | round90_counter_pin.py | selftest exit replaced by return 0 (always green) | committed battery + C2-BYT+STG composite (selftest) | a red selftest case must turn the selftest exit red; on the all-green tree the mutant is identical to pristine | committed: unchanged; selftest rc 0 with red-green-ok=4 of 5 (C2-BYT alone: rc 1, red-green-ok=4) | necessary for the selftest exit code; no single-defect run exposes it | none committed; composite C2-BYT+STG: selftest rc 0 with red-green-ok=4 of 5 (BYT alone rc 1) |
| C3-FRZ | round90_burndown.py | freeze refusal off (refuse = False) | committed battery + C3F-open-round39 | BASE/B/tip: freeze=refused must become admitted; selftest old-open-refuses must go red; open round-39 fixture must flip | committed: c3-base line-only, c3-B line-only, c3-tip line-only, c3-selftest RC-FLIP; C3F-open-round39: rc 1->0 (flip) | necessary | committed c3-base, c3-B, c3-tip (freeze line), c3-selftest (rc 0->1); verdict-level: C3F-open-round39 |
| C3-FRB | round90_burndown.py | freeze boundary changed from < N-2 to <= N-2 | committed battery + C3F-open-round88 | pending finding opened exactly at N-2 must be admitted at N; mutant refuses | committed: unchanged; C3F-open-round88: rc 0->1 (flip) | necessary | none committed; C3F-open-round88 (verdict) |
| C3-CHK | round90_burndown.py | check command forced to None (checks never run) | committed battery + C3R1-check-fail | failing check must be a defect; mutant admits the closed row | committed: c3-base line-only, c3-B line-only, c3-tip line-only, c3-selftest RC-FLIP; C3R1-check-fail: rc 1->0 (flip) | necessary | committed c3-base, c3-B, c3-tip (checks_run and check-failed lines), c3-selftest (rc 0->1, see finding F-C3-2); verdict-level: C3R1-check-fail |
| C3-CFD | round90_burndown.py | non-zero check rc no longer recorded as a defect | committed battery + C3R1-check-fail | failing check must be a defect and rc 1; committed selftest cannot see this (its red case is an AttributeError) | committed: c3-base line-only, c3-B line-only, c3-tip line-only; C3R1-check-fail: rc 1->0 (flip) | necessary | committed c3-base, c3-B, c3-tip (line-level); verdict-level: C3R1-check-fail |
| C3-MAL | round90_burndown.py | malformed-line term removed from the predicate | committed battery + C3F-malformed-only | a malformed ledger line must fail the predicate; selftest malformed-refuses is masked by an unrelated refusal | committed: unchanged; C3F-malformed-only: rc 1->0 (flip) | necessary | none committed; C3F-malformed-only (verdict) |
| C3-SUP | round90_burndown.py | supersedes ignored (resolution rows never applied) | committed battery + C3-selftest resolved-admits / refused-admits | resolved rows must clear pending; selftest must go red | committed: c3-selftest RC-FLIP | necessary | committed c3-selftest (resolved-admits, refused-admits red, rc 0->1); base/B/tip carry no resolution rows |
| C3-DUP | round90_burndown.py | duplicate-id rejection off in pass 1 | committed battery + C3F-dup-id | duplicate id must be a malformed/duplicate defect | committed: unchanged; C3F-dup-id: rc 1->0 (flip) | necessary | none committed; C3F-dup-id (verdict) |
| C3-SUN | round90_burndown.py | supersede-unknown defect off | committed battery + C3F-supersede-unknown | resolution naming a nonexistent id must be a defect; selftest supersede-unknown is masked by the open OLD-1 refusal | committed: unchanged; C3F-supersede-unknown: rc 1->0 (flip) | necessary | none committed; C3F-supersede-unknown (verdict) |
| C3-CLO | round90_burndown.py | closed-without-closing-evidence rejection off | committed battery + C3F-closed-no-evidence | closed row with no close evidence must be invalid | committed: unchanged; C3F-closed-no-evidence: rc 1->0 (flip) | necessary | none committed; C3F-closed-no-evidence (verdict) |
| C3-BLK | round90_burndown.py | blank/past-end source-line check off | committed battery + C3F-blank-source-line | source naming a blank line must be invalid | committed: unchanged; C3F-blank-source-line: rc 1->0 (flip) | necessary | none committed; C3F-blank-source-line (verdict) |
| C3-STG | round90_burndown.py | selftest exit replaced by return 0 (always green) | committed battery + C3-SUP+STG composite (selftest) | a red selftest case must turn the selftest exit red; on the all-green tree the mutant is identical to pristine | committed: unchanged; selftest rc 0 with red-green-ok=5 of 7 (C3-SUP alone: rc 1, red-green-ok=5) | necessary for the selftest exit code; no single-defect run exposes it | none committed; composite C3-SUP+STG: selftest rc 0 with red-green-ok=5 of 7 (SUP alone rc 1) |


Report: .ufo/waves/round-90/w1/MutTesterR90/mutants.md
