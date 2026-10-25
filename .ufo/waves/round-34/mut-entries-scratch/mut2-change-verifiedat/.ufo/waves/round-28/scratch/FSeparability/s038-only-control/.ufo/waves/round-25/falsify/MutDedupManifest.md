ATTACKS: round-25 C1 dedup identity, authoritative-block selection, and frozen P1 manifest; four isolated source mutants against 8ea41f9ed.
Axes: novelty → canonical coverage (construct identity), detector discrimination, exact byte restoration. No claim-admission judgment or live source fix.
Scratch: /tmp/k25w2-MutDedupManifest, populated with `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin archive 8ea41f9ed | tar -x -C /tmp/k25w2-MutDedupManifest` after creating that directory.
Detector: from scratch, `python3 plans/attrib_calibration.py --selftest` and separately `python3 plans/attrib_calibration.py --summary`; run concurrently per phase, bounded to 45 seconds each, TMPDIR confined to scratch/runtime-temp and PYTHONDONTWRITEBYTECODE=1.
Executed pristine, each mutant, and each exact restoration: 9 phases / 18 detector invocations; no timeout or inconclusive baseline. Existing Python 3.14.8; no other runtime or endpoint invoked.
Capture command: `python3 /tmp/k25w2-MutDedupManifest/probe-evidence/detector.py <phase>`; phase JSON plus full stdout/stderr remain under scratch/probe-evidence/ (supplementary; changes and observed outputs are recorded below).
Baseline --selftest: exit 0, `selftest: 14 checks, 0 failed`; baseline --summary: exit 0 and:
`TOTAL files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12 shares=12 n_ge_17=12 stored_verdicts=7 transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 stored_checks=119 mismatches=0 dup=[corpus/evidence/attrib-r22-legs.log:312-362=corpus/evidence/attrib-r22-opencode-trials.log:204-254]`

M1 — plans/attrib_calibration.py:519: `def analyze(root, dedup=True):` → `def analyze(root, dedup=False):`; expected detector: selftest F1 duplicate/sample totals.
Observed --selftest exit 1: `selftest FAIL F1` with `totals.correct: got 89 want 69; totals.duplicates: got 0 want 1; totals.scored_trials: got 99 want 79`; `selftest: 14 checks, 1 failed`.
Observed --summary exit 0: `unique_samples=5 duplicates=0 scored_trials=112 correct=112 estimates=44 PASS=14 INDETERMINATE=16 UNTESTED=14 mismatches=0 dup=[]` (selected TOTAL fields).
M1 verdict: KILLED by --selftest; --summary exit status alone does not catch double-counting.

M2 — plans/attrib_calibration.py:512: `(r[0], r[2], r[3], r[5])` → `(r[0], r[1], r[3], r[5])` inside `_table_key`; substitutes class for prediction.
Expected detector: a dedup identity fixture should distinguish equal trial/GT/chain rows with different predictions (frozen identity: plans/round-25-claims.md:28-32).
Observed --selftest exit 0: `selftest: 14 checks, 0 failed`; --summary exit 0 with the same baseline TOTAL above, including `duplicates=1 scored_trials=92 estimates=35 mismatches=0`.
Independent identity witness, not an existing gate: compare `_table_key({'rows':[left]}) == _table_key({'rows':[right]})` after importing the current scratch module.
`left=('T01','std','a','a','served','1/a OK 200','YES'); right=('T01','std','b','a','served','1/a OK 200','NO')`.
Observed witness: pristine false → M2 true → restored false; distinct prediction tables collapse under M2. This establishes a non-equivalent survivor, not merely unchanged corpus totals.
M2 verdict: SURVIVED both assigned detectors; missing discrimination for the prediction dimension is a coverage finding, not grounds to redefine the identity contract.

M3 — plans/attrib_calibration.py:551: `auth.append((rel, blocks[-1], roster))` → `auth.append((rel, blocks[0], roster))`; only the behavior-bearing block selection changed.
Expected detector: selftest F1 last-block fixture. Observed --selftest exit 1: `attrib-r22-fx-force.log accuracy: got (3, 4, 'FAIL', 'INDETERMINATE') want (20, 20, 'PASS', 'PASS')`; missing target:b/target:c expectations also reported; `14 checks, 1 failed`.
Observed --summary exit 0: `unique_samples=5 duplicates=0 scored_trials=92 estimates=44 PASS=10 INDETERMINATE=17 UNTESTED=17 mismatches=0 dup=[]` (selected TOTAL fields).
M3 verdict: KILLED by --selftest; the summary can remain internally consistent while selecting superseded blocks.

M4 — plans/attrib_calibration.py:472: P1_SHA256['attrib-r21-ds-trials.log'] full digest → empty string, preserving its manifest key.
Expected detector: frozen-manifest comparison / selftest G1. Observed --selftest exit 1: `selftest FAIL G1: green: unmodified lane copy of P1 passes the frozen manifest -- exit 1`; `14 checks, 1 failed`.
Observed --summary exit 1: `MISMATCH attrib-r21-ds-trials.log: sha256 7e6102461583c749 != frozen `; baseline TOTAL except `mismatches=1`.
M4 verdict: KILLED by both assigned detectors; blank expected SHA is not silently skipped.

Restoration evidence (SHA-256 of plans/attrib_calibration.py; before and after every detector pair were equal):
H0 = `92aa873986cb19a171421b88ba2a2362ff171c4ba2365ef7b0387f7a5d811a51`; independently matched `git show 8ea41f9ed:plans/attrib_calibration.py | sha256sum`.
M1 mutated = `13c752849d895d90de11ab330adc9e3e12508f05f30b66e0f2135030291085b2`.
M2 mutated = `29f7c93afd50e3374b82ee5b03ff93a0597684bc065faed5afbe5821090fa2a2`.
M3 mutated = `3fe071d63622153174bdc91fd6ada64dc3471b9856da12a2162ab7212bfb66a1`.
M4 mutated = `986ce5481eae5b9a812c772f992fe433a629502c796e9aa8f59f67dda153b17f`.
Every mutation started at H0; every revert returned to H0 before the next mutation. Phases r1-restored through r4-restored each produced --selftest exit 0 / `14 checks, 0 failed` and --summary exit 0 with the baseline TOTAL above.
Only this report was written in the live lane; all source mutations and generated detector fixtures/captures stayed under the assigned scratch root.
VERDICT: PARTIAL — 3/4 mutants killed; prediction→class key substitution survives both --selftest and --summary despite a demonstrated identity-contract violation. Installs: none.
