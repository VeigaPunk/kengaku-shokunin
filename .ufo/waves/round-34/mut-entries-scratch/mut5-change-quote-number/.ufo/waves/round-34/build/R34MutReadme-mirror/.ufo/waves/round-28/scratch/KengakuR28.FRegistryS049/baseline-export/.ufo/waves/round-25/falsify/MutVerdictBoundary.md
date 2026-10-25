ATTACKS: attrib_calibration.py verdict equality boundaries, zero-data classification, and frozen alpha at 8ea41f9ed.
Axes: assigned novelty → canonical coverage; detector sensitivity; byte-exact restoration and isolation.
Scope: pristine `git archive 8ea41f9ed` extracted to `/tmp/k25w2-MutVerdictBoundary`; only this scratch source was mutated, one change at a time.
Commands: from scratch, `TMPDIR=/tmp/k25w2-MutVerdictBoundary/tmp PYTHONDONTWRITEBYTECODE=1 python3 plans/attrib_calibration.py --selftest` and the identical command with `--summary`.
Each command had a 120-second subprocess timeout; the two read-only detectors ran concurrently, with mutation/restoration phases sequential. No timeouts occurred.
Expected detector: frozen rule at `plans/round-25-claims.md:35-36`; verdict anchors A3 at `plans/attrib_calibration.py:860-861`, fixture expectations F1 at :870-873, fixed CP anchors A1 at :687-691,847-849.
Pristine source SHA-256 H0 = `92aa873986cb19a171421b88ba2a2362ff171c4ba2365ef7b0387f7a5d811a51`; initial live source had the same hash.
Pristine outputs: selftest exit 0, `selftest: 14 checks, 0 failed`; summary exit 0, stderr empty.
Pristine TOTAL excerpt: `files=9 scored_files=5 trial_only=4 blocks=10 superseded=5 unique_samples=4 duplicates=1 scored_trials=92 correct=92 incorrect=0 estimates=35 PASS=12 FAIL=0 INDETERMINATE=11 UNTESTED=12` and `stored_checks=119 mismatches=0`.

| Mutant (scratch path:line) | Actual selftest | Actual summary | Mutation verdict |
|---|---|---|---|
| `plans/attrib_calibration.py:171`, `lo >= bar` → `lo > bar` | exit 0; 14 checks, 0 failed | exit 0; entire stdout byte-identical to pristine | SURVIVED: lower-equals-bar coverage gap |
| `plans/attrib_calibration.py:173`, `hi < bar` → `hi <= bar` | exit 0; 14 checks, 0 failed | exit 0; entire stdout byte-identical to pristine | SURVIVED: upper-equals-bar coverage gap |
| `plans/attrib_calibration.py:169`, n==0 return `UNTESTED` → `INDETERMINATE` | exit 1; `selftest FAIL A3` then traceback | exit 1; no stdout, traceback | KILLED |
| `plans/attrib_calibration.py:76`, `ALPHA = 0.05` → `ALPHA = 0.10` | exit 1; `selftest: 14 checks, 3 failed` (A1, A3, F1) | exit 0; TOTAL unchanged, interval bytes changed | KILLED by selftest, not summary |

Mutated source SHA-256 (before and after each detector pair matched):
- lower-strict: `df9ae78c201191863dc316196a114a42f1bb82391e600fd582c9496c47df0e7d`.
- upper-inclusive: `9dd138a2875e85d15746c2d8cebdf5a0e435731c262ea34d4a1eb4e14d9968ca`.
- zero-indeterminate: `4cbda93a150c49c3440efe0546f5b5628356ceaf218d7e97d9b624891517e8af`.
- alpha-tenth: `feab5af1c6775c8fb50e5c7d80467dd38f15058f2873fe28bc9029bf91cf0797`.
Zero-data actual A3 output: `['INDETERMINATE', 'INDETERMINATE', 'PASS', 'FAIL']`; both modes then raised `TypeError: '>=' not supported between instances of 'float' and 'NoneType'` at `plans/attrib_calibration.py:411`, reached through :424 and trial-only handling :553.
Alpha actual A1 excerpt: `cp lo 7/50 scipy: got 0.0675966990035568 want 0.0581917003399734`; A3 became `['UNTESTED', 'PASS', 'PASS', 'FAIL']`.
Alpha summary example (`attrib-r21-impl-ds-trials.log 268-312 accuracy 20/20`): pristine `cp95=[0.831567,1.000000]`, mutant `cp95=[0.860892,1.000000]`; both still print `interval=PASS`.
`--summary` exit is a stored-line consistency check, not an independent interval-rule oracle (`plans/attrib_calibration.py:963`); its alpha exit 0 is not counted as selftest survival.
Restoration: after EACH mutant, exact H0 was restored before rerunning BOTH commands. All four restored pairs exited 0/0; all restored stdout/stderr were identical to pristine. Every phase's source hash was unchanged by its detector pair.
Common pristine/restored/surviving-mutant stdout SHA-256: selftest `e6a933f203ab8c3e45b309e8a4a1b9296420c6611e92101db7e6d1a68b546010`; summary `b009794d9a34bdcb1120eece141de1afd3e105d87fff2de3bf6b72dacf8baecd`.
Raw evidence: `/tmp/k25w2-MutVerdictBoundary/receipts/all-phases.json` contains all nine phases, full stdout/stderr, exact argv, exit statuses, and before/after hashes; individual phase JSON receipts are alongside it.
Finding boundary: two equality mutants evade the existing selftest and P1 summary; no changed verdict on the frozen nine-receipt population was demonstrated. No live lane implementation, receipts, Git index, or fleet state was edited.
VERDICT: PARTIAL — 2/4 mutants survive selftest (equality coverage gaps); zero-data and alpha mutants are killed; all scratch source bytes restored.
INSTALLS: none; used existing Python 3.14.8, Git archive, tar, and sha256sum.
