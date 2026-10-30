# SC6RegistryHealth — seat report (round 55, wave 1)

Date: 2026-10-30. Role: read-only registry/ledger health census at tip. No lane writes beyond this seat's named outputs. No subagents. No tool installs (used host `python3` and `git` only).

## What I ran (commands + exit codes)

Scratch: `/fast/scratch/hyaku/kengaku-r55/SC6RegistryHealth/` (created; deleted before yield). One live clone: `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/clone` → tip `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`, `git status --porcelain` empty.

1. `python3 plans/round54_c2_entrytruth.py --lane /fast/scratch/hyaku/kengaku-r55/SC6RegistryHealth/clone --dry` (cwd: clone) → **exit 0**
   ```
   ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
   DRY static legs only: no predicate
   ```
2. `python3 plans/round52_c2_registry.py --lane /fast/scratch/hyaku/kengaku-r55/SC6RegistryHealth/clone` (cwd: clone) → **exit 1**
   ```
   ADVERTISED total=79
   REGISTERED total=77 rows=79
   MISSING 2
     MISSING plans/round54_c1_anchor.py
     MISSING plans/round54_c2_entrytruth.py
   INCOMPLETE 0
   ENTRY-MISSING 0
   SELFTEST-UNBACKED 0
   DUPLICATE 0
   PREDICATE R52-C2 fail
   ```
   Byte-matches the frozen before-receipt state described in `plans/round-55-claims.md` (MISSING the two round-54 counters; fail; exit 1) — expected at tip, R55-C1 after-state not yet landed.

3. Census/spot-check: throwaway Python over the clone (`SKILL.md` registry block, `plans/round54-entrytruth.json`, script bodies of `grader.py`, `plans/round52_c2_registry.py`, `plans/round40_c2_verify.py`, `plans/round50_c2_audit.py`, `plans/stage_scan.py`), plus `grep` verifications for `--stage-check` and `round50_selftest_bogus`. All exit 0.

## Files I wrote

- `.ufo/waves/round-55/w1/SC6RegistryHealth/health.md` — full census (verbatim counter outputs + counts table + spot-check).
- `.ufo/waves/round-55/w1/SC6RegistryHealth.md` — scoped findings (Report trailer path).
- `.ufo/waves/round-55/w1/SC6RegistryHealth/report.md` — this report.

## Findings (summary)

| count | value |
|---|---|
| registry rows (data rows) | 78 (`rows=79` in counter = +header) |
| ledger rows | 78 (schema `r54-entrytruth-v1`) |
| entry_state red | 16 (green 62) |
| evidence-cell rows | 16 — exactly the red rows (bijection) |
| flag-gap rows | 1 of 5 spot rows (`db-wal-probe`: `--stage-check` absent from the `round40_c2_verify.py` its cell names — prose reference to the entry probe's own mode); 2 of 78 under naive all-rows pairing (adds `round50-c2`: absent `plans/round50_selftest_bogus.py` is the selftest's own quoted fixture path) |

Counter arithmetic reconciled: `ADVERTISED 79 − REGISTERED 77 = MISSING 2`; `REGISTERED 77 = 78 rows − coverage-census` (entry path `corpus/evidence/round13-coverage/…` hyphen excluded by the counter's command regex class, already documented in that row's verdict-map cell). Registry name set == ledger name set (78/78; r54 dry legs `missing=0 extra=0`).

## Defects found

- No instrument defect, no false verdict-map cell. The two flag/script artifacts above are prose/data attribution effects that the frozen r52 counter contract (exactly-one-script, all-flags-absent, `no … --flag` negation) intentionally does not flag; `SELFTEST-UNBACKED 0` at tip is correct under its contract.

## Dead ends

- First spot-check pass selected rows by unbackticked name → `StopIteration`; retried with backticked names. No output impact.
- None otherwise. LSP not applicable (markdown/JSON census + CLI runs).

## Honesty notes

- Both counter outputs are verbatim from real runs with observed exit codes (0, 1). The r54 run was `--dry` only — no hermetic execution was performed by me, per seat spec.
- An unrun check has not passed: I did not run the r54 counter's execution legs, any selftest, or any fixture; none is claimed.
