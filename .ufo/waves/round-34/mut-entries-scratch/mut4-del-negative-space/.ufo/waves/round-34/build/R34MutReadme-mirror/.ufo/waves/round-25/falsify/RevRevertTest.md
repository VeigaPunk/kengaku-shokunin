ATTACKS: QUALITY R13 separability — C1 novelty vs C2 calibration at `8ea41f9ed`

Axes attacked: novelty (C1) and calibration (C2).

Findings (severity order): none; the registered summary counts survive both reversions.

- C1 reverted in `/tmp/k25w2-RevRevertTest/revert-c1`: removed `corpus/SOURCES.md` rows S027–S037, `corpus/knowledge/attribution-interval-calibration.md`, `plans/attrib_calibration.py`, and the matching two `corpus/README.md` index rows. `python3 plans/state_check.py --root /tmp/k25w2-RevRevertTest/revert-c1 --summary` → `assertions=236 match=232 mismatch=0 superseded=1 offline_unverifiable=3`; exit 0. Full-tip copy produced the same summary and exit.
- C2 reverted in `/tmp/k25w2-RevRevertTest/revert-c2`: restored `SHONEN.md` and `PROVINCE.md` from `6180e4f` via `git archive`; removed `plans/state_check.py`. `python3 plans/attrib_calibration.py --root /tmp/k25w2-RevRevertTest/revert-c2 --summary` → `TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0`; exit 0. Full-tip copy produced the same TOTAL and exit.
- Preregistration: `plans/round-25-claims.md:95-96` states the separability claim. All mutations were confined to scratch copies; the lane tree was not changed.

Residual risk / verification gap: the state-check summary counters are invariant, but its `OUT_OF_POPULATION` diagnostic list changes as C1 index rows and files are removed; this attack compares the specified counts, not byte-identical full output. No other checks were run.
Installs: none.
VERDICT: SURVIVES — both requested cross-reversion summary counts equal their full-tip baselines.
