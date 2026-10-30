# SC6RegistryHealth — scoped findings (round 55 w1, tip 80afa613)

Full census: `.ufo/waves/round-55/w1/SC6RegistryHealth/health.md` · seat report: `.../SC6RegistryHealth/report.md`.

## Verbatim runs (clean shared clone at tip, cwd = clone, `--lane` = clone)

- `python3 plans/round54_c2_entrytruth.py --lane <clone> --dry` → exit 0:
  `ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1` / `DRY static legs only: no predicate`
- `python3 plans/round52_c2_registry.py --lane <clone>` → exit 1:
  `ADVERTISED total=79` / `REGISTERED total=77 rows=79` / `MISSING 2` (`plans/round54_c1_anchor.py`, `plans/round54_c2_entrytruth.py`) / `INCOMPLETE 0` / `ENTRY-MISSING 0` / `SELFTEST-UNBACKED 0` / `DUPLICATE 0` / `PREDICATE R52-C2 fail`
  — exactly the frozen R55-C1 before-state; regression still open at tip, as expected pre-integration.

## Counts

| count | value |
|---|---|
| registry rows (data rows) | 78 (79 counter `rows` incl. header) |
| ledger rows | 78 (`r54-entrytruth-v1`) |
| registry ↔ ledger name sets | equal (78 = 78) |
| entry_state red | 16 (62 green) |
| evidence-cell rows | 16 = exactly the red rows |
| flag-gap rows (5-row spot-check) | 1 — `db-wal-probe` (`--stage-check` absent from `plans/round40_c2_verify.py` named in its self-test cell; prose reference to the entry probe's own mode) |
| flag-gap rows (naive all-78 pairing) | 2 — adds `round50-c2` (absent `plans/round50_selftest_bogus.py` is the selftest's own quoted scratch fixture path) |

## Reconciliation

`MISSING 2 = ADVERTISED 79 − REGISTERED 77`; `REGISTERED 77 = 78 rows − coverage-census` (hyphenated `corpus/evidence/round13-coverage/…` outside the counter regex class, documented in that row's cell); `rows=79 = 78 + header`. `SELFTEST-UNBACKED 0` is correct under the frozen contract (exactly-one-script + all-flags-absent + `no … --flag` negation rule): both flag-gap rows fail the predicate by construction. No counter defect, no false verdict-map cell found.
