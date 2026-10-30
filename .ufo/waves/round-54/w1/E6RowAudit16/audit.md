# R54-C2 entry re-execution audit

Executed in a shared clone of the current lane tip, each with a distinct scratch TMPDIR and environment produced by `round54_c2_entrytruth.hermetic_env(tmp)`. Timeout: 600 seconds per row. All three are entry-mode argv (no forbidden flags) and their script files exist in the clone. These ledger rows are green and carry no `evidence` fragment, so fragment-match is not applicable; no red-row fragment check was required.

## Commands and results

1. `python3 plans/round39_c1_audit.py --lane .` — declared exit 0; observed exit 0; CONFIRMED. Output tail:
   ```
   PINS final total=26 mismatched=0
   AUDIT nondeterministic_kills=0
   AUDIT C1 clean
   PREDICATE C1 pass
   ```
2. `python3 plans/round39_c1_verify.py --lane .` — declared exit 0; observed exit 0; CONFIRMED. Output tail:
   ```
   PINS final total=26 mismatched=0
   MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
   PREDICATE C1 pass
   ```
3. `python3 plans/round39_c2_verify.py --lane .` — declared exit 0; observed exit 0; CONFIRMED. Output tail:
   ```
   V6 ok census_exit=0
   V7 ok rows=4 tags=4 bad=0
   checks=7 defects=0
   PREDICATE C2 pass
   ```

All results completed without timeout. Recorded verdict lines are in `audit.json`.
