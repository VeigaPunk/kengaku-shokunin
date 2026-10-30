# R6RegistryCellAudit — scoped findings (round 55, w1)

Seat: R6RegistryCellAudit (reviewer, attack share, operability / R55-C1).
Target: per-row cell-truth audit of the five new SKILL.md `## Gate/probe registry` rows
`round54-c1`, `round54-c2`, `round55-c2`, `round55-c2-controls`, `round55-c3`.

## Headline

**All five rows are present and every audited cell is TRUE. No false cell found.**
The five rows arrived after a bounded wait (first 25-min window: absent, E1 `agentId:null`;
E1 was then observed actively building — `otsenv` venv under its scratch — and landed the rows
~135 s into a short re-wait). Once landed, each entry cell's command was run with care in a
scratch clone (`--dry`, bare, or the bounded `--case … --against …` / `--selftest` forms —
never a full 78-row run), each verdict-map's exit semantics were checked against observation,
and each self-test cell's flag was verified present in the script body. The authorised
SELFTEST-UNBACKED pre-check `python3 plans/round52_c2_registry.py --lane <tree>` reports
`MISSING 0 INCOMPLETE 0 ENTRY-MISSING 0 SELFTEST-UNBACKED 0 DUPLICATE 0 PREDICATE R52-C2 pass`
on the lane tree with the rows present.

## Per-row cell-truth table

Legend: T = cell true (observed == claimed). Evidence files under `R6RegistryCellAudit/evidence/`.

| row | entry cell | verdict map | self-test cell | pinned sha256 | overall |
|---|---|---|---|---|---|
| `round54-c1` | T | T | T | T | **TRUE** |
| `round54-c2` | T | T | T | T | **TRUE** |
| `round55-c2` | T | T | T | T | **TRUE** |
| `round55-c2-controls` | T | T | T | T | **TRUE** |
| `round55-c3` | T | T | T | T | **TRUE** |

### `round54-c1` → `plans/round54_c1_anchor.py` (kind gate — correct)
- **entry** `… anchor.py verify --anchor corpus/evidence/round54/anchor --claims plans/round-54-claims.md --source . --work … --controls`: ran it. On bare host python3 → exit 1, `ModuleNotFoundError: No module named 'opentimestamps'` (lazy import at `cmd_verify` :301). Under the `opentimestamps` venv → reaches `SETUP header.bin absent (attestation not yet confirmed or not yet landed)` + `PREDICATE R54-C1 fail`, exit 1. Both match the claimed exit-1 semantics exactly. `evidence/anchor-verify-bare-python3.txt`, `evidence/anchor-verify-otsenv.txt`.
- **verdict map**: claims (0 pass / 1 a leg recomputes otherwise, incl. bare-host `ModuleNotFoundError` exit 1 / 2 setup). Observed bare-host exit 1 via `ModuleNotFoundError` and venv exit 1 via `SETUP … PREDICATE fail` — both claimed, both true.
- **self-test** `python3 plans/round54_c1_anchor.py selftest`: correctly uses the **`selftest` subcommand**, NOT a `--selftest` flag (the file contains zero `--selftest` occurrences; `--selftest` exits 2 "cmd required"). Under the otsenv venv → exit 0 `[selftest] 8/8 PASS`; the cell honestly notes bare-host python3 exits 1 (`ModuleNotFoundError`). No false flag → SELFTEST-UNBACKED does not fire. `evidence/anchor-selftest-otsenv.txt`.
- **pinned** `sha256 e08152a55fefa54a` == measured `e08152a55fefa54a`. True.

### `round54-c2` → `plans/round54_c2_entrytruth.py` (kind gate — correct)
- **entry** `… entrytruth.py --lane .`: bare → exit 2 `SETUP --source and --work are required unless --dry`. Claimed, observed. `--lane . --dry` → exit 0 static legs + `DRY static legs only: no predicate`. `evidence/entrytruth-dry.txt`.
- **verdict map** 0/1/2 + `--dry` semantics — matches docstring and observation.
- **self-test** `… --selftest` → exit 0 `[selftest] 7/7 PASS`; `--selftest` present in body. `evidence/entrytruth-selftest.txt`.
- **pinned** `44c3f41285239645` == measured. True.

### `round55-c2` → `plans/round55_c2_entryargv.py` (kind gate — correct)
- **entry** `… entryargv.py`: bare → exit 2 `SETUP --source and --work are required unless --dry`. Claimed, observed. `evidence/entryargv-bare.txt`. (A `--dry` on the *base* clone exits 1 on 17 pre-existing placeholder ARGV-DEFECTs — that is the clone's base SKILL.md state, not a row defect; the landing tree is corrected by sibling seats.)
- **verdict map** 0/1/2 (adds `wrapper_defect`/`abbrev_defect`/`BINDING l1/l2/l3`) — matches the script's `evaluate`.
- **self-test** `… --selftest [--work <scratch>]` → exit 0 `[selftest] 4/4 PASS`; `--selftest` and `--work` both present in body. `evidence/entryargv-selftest.txt`.
- **pinned** `2bf9e66ce3d5bace` == measured. True. (entryargv is a live E2 file — reconfirm at the measured-after revision.)

### `round55-c2-controls` → `plans/round55_c2_controls.py` (kind gate — correct)
- **entry** `… controls.py`: bare → exit 2 argparse `one of the arguments --case --selftest is required`. Claimed, observed.
- **verdict map** — every concrete claim re-run and confirmed: `--case abbreviated-selftest --against r54` and `--case uv-decoy-script --against r54` each print `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)`; `--case abbreviated-selftest --against r55` prints `ARGV-DEFECT` + `ABBREV-DEFECT fixture-gate: …` `COUNTER EXIT 1` `ROUTE kill demonstrated`; `--case uv-decoy-script --against r55` prints `ARGV-DEFECT` + `WRAPPER-DEFECT fixture-gate: argv[0]='uv' is not an interpreter …` `COUNTER EXIT 1` `ROUTE kill demonstrated`. `evidence/controls-abbrev-r55.txt`, `controls-uvdecoy-r55.txt`, `controls-uvdecoy-r54.txt`.
- **self-test** `… --selftest` → exit 0 `SELFTEST cases=4 failures=0`; flag present. `evidence/controls-selftest.txt`.
- **pinned** `c7591bc6d682c542` == measured. True.

### `round55-c3` → `plans/round55_c3_chess_probe.py` (kind probe — correct)
- **entry** `… chess_probe.py`: bare (no `--receipt`) runs the 12-case battery → exit 0 `cases=12 observed_pass=5 observed_fail=7 mismatches=0` `PREDICATE R55-C3 pass`. This is byte-for-byte the verdict map's claimed "measured bare entry 2026-10-30" line. `evidence/chess-battery-bare.txt`.
- **verdict map** 0/1/2 — matches; capture at its pinned sha256 `a540714e…`, `/usr/bin/bwrap` 0.13.1 present.
- **self-test** `… --selftest [--work <scratch>]` → exit 0 `SELFTEST cases=2 failures=0`; `--selftest`/`--work` present. `evidence/chess-selftest.txt`.
- **pinned** `7bd2863ca745f165` == measured. True.

## Residual risk / notes (not false cells)
- `round54-c1`'s self-test and entry both require the `opentimestamps` Python package. The row
  states this honestly. **Risk to R55-C1 frozen leg 2:** if the L1's leg-2 execution host lacks
  `opentimestamps`, the named self-test `… anchor.py selftest` observes exit 1, not the cell's
  claimed exit 0 — the row would read false through no fault of the cell text. E1 built
  `/fast/scratch/hyaku/kengaku-r55/E1RegistryRows/otsenv` for exactly this; leg 2 must run
  under such a venv.
- The anchor assets are incomplete (`anchor.json`+`claims.ots` only; no `header.bin`/receipts —
  the r54 Bitcoin attestation was never confirmed), so the round54-c1 *entry* can only be red.
  This is a pre-existing r54 state the row discloses, not a round-55 cell defect.
- `round55-c2`'s pinned digest must be re-confirmed at the measured-after revision (entryargv is
  a live sibling file).
- My registry-counter pre-check was measured on the lane **working tree** at the moment the rows
  were present; the binding R55-C1 after-run must be re-executed on a clean clone at the
  measured-after revision (L1 duty). Mid-wave the legs read all-0 because E1's rows and all five
  scripts were present; no leg fired on an absent sibling file.

## Kill-rule relevance (R55-C1)
The R55-C1 kill rule fires only if a round-55-added row's verdict-map cell is *false* (the named
self-test exits otherwise than claimed) at the landing revision. I exercised every named
self-test and every claimed exit path; none exits otherwise than its cell claims (given the
documented `opentimestamps` venv for `round54-c1`). **No kill-rule trigger found.**
