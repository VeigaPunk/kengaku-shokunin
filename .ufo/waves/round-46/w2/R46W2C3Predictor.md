# R46W2C3Predictor — attack on C3 V11

## Axes

- **Coverage (judged):** whether the held-out predictor actually distinguishes semantic reading from memorized outcomes.
- **Calibration:** whether its randomized 60-state set defeats lookup predictors.

## Evidence and counterexample

Lane clone at `/fast/scratch/hyaku/kengaku-r46/R46W2C3Predictor/lane` was checked at HEAD `42d5043afac952fcb43bf4798757785dd258cf85`. The frozen counter and entry were tested via its own `v11()` on scratch copies of the entry; no lane file was modified.

Command: the round-46 `claims/envelope.sh "$S/env" python3 "$S/driver.py" "$S/lane" "$S"` invocation. Output:

```
ENVELOPE start 03:07:34 cwd=/home/vgpnk/Projects/shokunin
BASE LINT []
callorder lint ['>>']
callorder (True, 'states=60 grader_pass=15 grader_fail=45 disagree=0')
keyed lint ['>>']
keyed (True, 'states=60 grader_pass=15 grader_fail=45 disagree=0')
ENVELOPE end 03:07:38 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

The two displayed toy predictors were *not* lint-clean: their `>>` feature was rejected. The reported `v11()` result is consequently not evidence of those bodies passing lint; `v11()` reads the package entry’s unchanged, lint-clean reference predictor. They are not counted as bypasses. The reference predictor passes the randomized state batch exactly, as intended. Counter source lines 641–654 show the literal-token lint; lines 666–714 generate a newly shuffled 60-state sample from `os.urandom`; lines 798–811 grade then compare predictions. The seeded numeric tables from R45 do not directly transfer: state values and order are regenerated; straightforward shifts are linted.

I did not obtain a lint-clean memorizer or a held-out counterexample from the extra-state generator. No extra bespoke source states were separately evaluated. Thus observed bypass count is zero; that is bounded evidence, not proof that V11 excludes all memorization.

## Smallest safe correction / surviving claim

No demonstrated defect requiring a correction. The claim survives this attack in the narrow tested respect: the unchanged predictor matches the 60 fresh generated states, and the prior round’s direct shift-table pattern is lint-blocked. Residual: finite-sample equivalence remains possible with alternate arithmetic/feature encodings or a different wrong-but-close heuristic; source review remains necessary.

Scratch was removed with the required `scratch_guard.py safe-rm` command. No tools were installed.

VERDICT: c3-predictor-bypasses-0
