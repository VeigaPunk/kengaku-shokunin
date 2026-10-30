# SC6RegistryHealth — registry/ledger health census at tip (round 55, wave 1)

- Seat: SC6RegistryHealth (leaf, read-only lane census)
- Measured revision: `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (clean shared clone at `/fast/scratch/hyaku/kengaku-r55/SC6RegistryHealth/clone`; `git status --porcelain` empty; clone of lane `master`)
- Date: 2026-10-30
- Both counters run with cwd = the clone; `--lane` = the clone (absolute).

## 1. Verbatim counter outputs

### 1a. r54 entry-truth counter, dry

Command: `python3 plans/round54_c2_entrytruth.py --lane <clone> --dry` — **exit 0**

```
ROWS registry=78 ledger=78 missing=0 extra=0 argv_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
DRY static legs only: no predicate
```

All static legs clean at tip: the 78-row SKILL registry and the 78-row ledger cross-reference exactly (`missing=0 extra=0`), no argv/declaration defects, one registry heading.

### 1b. r52 registry counter

Command: `python3 plans/round52_c2_registry.py --lane <clone>` — **exit 1**

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

This is byte-for-byte the frozen R55-C1 before-state (`round-55-claims.md`, receipt `.ufo/waves/round-55/claims/c1-before.txt`): `MISSING 2` (the two round-54 counters), `PREDICATE R52-C2 fail`, exit 1. Expected at tip — the `round54-c1`/`round54-c2` registry rows are the round-55 integration's after-state, not yet landed.

## 2. Counts table

| count | value | derivation |
|---|---|---|
| registry rows (data rows) | **78** | `SKILL.md` block from `## Gate/probe registry (PROTOCOL §Gate standard)` to next `## `: 79 eight-cell table lines − 1 header. Cross-checks: r52 counter `rows=79` (counts header), r54 counter `registry=78` (named rows only) |
| ledger rows | **78** | `plans/round54-entrytruth.json` `rows` (schema `r54-entrytruth-v1`) |
| registry ↔ ledger set equality | **equal** | 78 names each; sets identical (registry names backticked, ledger bare) |
| rows with `entry_state` red | **16** | 62 green / 16 red |
| rows with evidence cell | **16** | `evidence` field present on exactly the 16 red rows — bijection; green rows carry none |
| registry cells carrying a flag the named script body lacks | **1 of 5** spot rows; **2 of 78** under naive all-rows pairing (both explained, see §4) | manual read of scripts, negation-aware |

Red rows (16): `adoption-check`, `anchor-digest-check`, `gate-flip-check`, `mutant-direction-check`, `round28-census`, `round35-c1-coverage`, `round38-c1-mutants`, `round40-c1-mutants`, `round46-c3`, `round51-surfaces`, `round52-c1`, `round53-c2`, `scratch-root-guard`, `sources-adopt`, `stage-scan`, `state-assertion-check`.

## 3. Flag spot-check — 5 rows, scripts read

| row | self-test cell names | flags checked | verdict |
|---|---|---|---|
| `hermetic-grader` | `grader.py` | `--selftest`; entry overrides `--r8-/--r9-/--r11-/--r12-` | backed — all tokens in `grader.py` bytes |
| `round52-c2` | `plans/round52_c2_registry.py` | `--selftest`, `--lane` | backed |
| `db-wal-probe` | `plans/round40_c2_verify.py` | `--dry`, `--lane`, `--stage-check` | **flag gap**: `--stage-check` occurs nowhere in `round40_c2_verify.py` |
| `round50-c2` | `plans/round50_c2_audit.py` + `plans/round50_selftest_bogus.py` | `--selftest` | backed flag-wise; second script name is absent at tip — it is the bogus-pointer fixture path that `round50_c2_audit.py --selftest` creates in its scratch copy, quoted as output data (`new_unresolved=['plans/round50_selftest_bogus.py']`), as the cell itself states |
| `stage-scan` | `plans/stage_scan.py` | `--selftest`, `--tmp` | backed |

## 4. Reconciliation of the two flag/script artifacts against the frozen counter contract

The r52 counter prints `SELFTEST-UNBACKED 0` at tip; its contract (Amendment A3, in code) flags a self-test cell only when it names **exactly one** script and **all** of the cell's flags are absent from that script's bytes; a `no … --flag` negation within 24 chars is ignored as a declaration.

- `db-wal-probe`: the cell names one script but carries `--dry`/`--lane`, which ARE in `round40_c2_verify.py`, so the all-flags-absent predicate is false by construction. The lone absent token `--stage-check` belongs — per the cell's own trailing prose ("the probe's own `--dry`/`--stage-check` modes are not a self-test of its verdicts") — to the entry probe `plans/db_wal_probe.py`, not to the verify script. Prose attribution the regex cannot see; not a false verdict-map cell.
- `round50-c2`: cell names two scripts, so the exactly-one-script predicate never applies. The absent name is fixture output data, not a claimed instrument.

Conclusion: no counter defect; no false verdict-map cell found in the spot-check. The 2-of-78 naive pairing (per-(script,flag) literalism) is reported for census completeness only.

## 5. Extra reconciliation of counter arithmetic

- `ADVERTISED 79 − REGISTERED 77 = MISSING 2` — the exact frozen R55-C1 before-state.
- `REGISTERED 77 = 78 rows − coverage-census`: the `coverage-census` row's entry `python3 corpus/evidence/round13-coverage/coverage_census.py` is not matched by the counter's command regex (`round13-coverage` contains a hyphen; the regex class is `[A-Za-z0-9_]+`), so it never enters the registered map. `rows=79 = 78 data rows + header`. Both effects are already documented in the row's own verdict-map cell.
- Every registry row name = every ledger name (78/78), so the ledger set already equals the parseable registry set at tip (`missing=0 extra=0` in r54 legs).

## 6. Methods / honesty notes

- All greps and parses above were re-implemented in one throwaway Python census script over the clone bytes; the two counter outputs are captured verbatim from real runs (exit codes 0 and 1 shown above).
- LSP device not applicable (census of markdown/JSON + counter CLI runs; no symbol resolution needed). Text/grep-level evidence only.
- One internal-only misstep: a first spot-check pass picked rows by unbackticked name and raised `StopIteration`; retried with backticked names. No output impact.
- Scratch `/fast/scratch/hyaku/kengaku-r55/SC6RegistryHealth/` deleted after copying this census; no lane file was written except this seat's named outputs.
