# W2RevRowsB — round 52 wave 2 (falsify), reviewer, operability

Seat: `W2RevRowsB` (leaf reviewer, read-only). Axis: operability (R52-C2).
Lane tip checked: `87301bacca90c03fa915716fbe6d7023762c5ab3` (lane HEAD `master`).
Method: a fresh `git clone` of the lane at `/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane`
(`git rev-parse --show-toplevel` asserted equal to that path before any run). Every script was run
inside the clone, with `TMPDIR` and `--work` pointed at my scratch. The live lane was never run or
written. `git status --porcelain` in the clone was empty after all runs, including the heavy
sandbox counters. No install was made. `uv` (`/home/vgpnk/.local/bin/uv`) was already present and
was used only as the entry command documents.

## What I attacked

Population: the 14 base-tip new rows at positions 15–28 of the MISSING list in
`.ufo/waves/round-52/claims/c2-before.txt`, plus the existing `order-check` row.
Position 15–28 (the half W2RevRowsA did not take) is:
`round35_c1_verify`, `round35_hardening`, `round36_c2_verify`, `round45_c1_verify`,
`round45_c2_verify`, `round46_c1_verify`, `round46_c2_verify`, `round46_c3_verify`,
`round50_c1_verify`, `round50_c2_audit`, `round51_routing`, `round51_surfaces`, `routed_open`,
`tb2_grader_probe`.

Two sources were checked against each other:
- the wave-1 drafts under `.ufo/waves/round-52/w1/C2ScribeRows*/` (`rows.md`, `artifacts/rows.md`);
- the rows as they sit in `SKILL.md` § Gate/probe registry at HEAD (lines 590, 624–637).
The two are identical cell for cell for all 15 rows (checked by script: `receipts/probes/collect.py`,
`landed-rows.json`). So the landed rows are the ones verified below.

Each factual cell was checked against its script: entry flags (argparse), verdict strings and exit
codes, self-test spelling, pinned digests and literals, and write-scope claims. Measured numbers were
checked by running the entry command in the clone. Each `--selftest` or `--dry` spelling was run.

## Commands run (all in the clone, from scratch)

- Argparse and help survey: `grep -n "add_argument\|parse_args" plans/<script>.py` for all 14 scripts.
- Quick batch (`run-quick.sh`): `round35_c1_verify --lane .`; `round35_hardening --lane .`;
  `round36_c2_verify --lane .`; `round46_c2_verify --lane . --work <scratch>`;
  `round46_c3_verify --lane . --work <scratch>`; `round50_c2_audit --lane .` and `--selftest`;
  `round51_surfaces --lane .` and `--selftest`; `round51_routing --lane . --run-checks --scratch <scratch>`
  and `--selftest`; `routed_open --lane .` and `--selftest`;
  `order_check --lane . --claims plans/round-40-claims.md --receipt corpus/evidence/round40/db-wal-probe.txt`;
  the same with `--receipt corpus/evidence/round39/git-leak-probe.txt` (control 1) and
  `--claims plans/round-99-claims.md` (control 2); `uv run --no-project --with biopython==1.85
  python3 plans/tb2_grader_probe.py --lane .`.
- Heavy batch (`run-heavy.sh`): `round45_c2_verify`, `round45_c1_verify --jobs 8`,
  `round46_c1_verify --jobs 8`, `round50_c1_verify` (all with `--work <scratch>`).
- Targeted probes: `round46_c3_verify --filler`; `round35_c1_verify --selftest` (rc 2);
  `round35_hardening --skip H6` and with one untracked file planted in the clone; `round51_routing
  --bogus` and `--ledger <missing>`; `round51_surfaces --bogus` and `--manifest <missing>`;
  `routed_open --file <invalid row>`, `--file corpus/defects.jsonl`, `--file <missing>`, `--observe`
  (with and without `LANE` exported); `tb2_grader_probe.py` without uv (no Biopython) and `--dry`;
  `round50_c1_verify --work <missing parent>`; `--selftest` on the nine counters without one (all rc 2).
- Counter-level attack on `plans/round52_c2_registry.py` `selftest_unbacked()` (read-only import,
  `receipts/probes/a3-probe.py`, `a3-fix-probe.py`).
- Registry counter on the lane tree: `python3 plans/round52_c2_registry.py --lane .` →
  `ADVERTISED total=72 / REGISTERED total=72 rows=74 / MISSING 0 / INCOMPLETE 0 / ENTRY-MISSING 0 /
  SELFTEST-UNBACKED 0 / PREDICATE R52-C2 pass` (run in the clone; SKILL.md matches).

## Per-row verdicts

| row (SKILL.md line) | verdict | evidence in short |
|---|---|---|
| `order-check` (590) | TRUE | entry, verdict strings, controls, pins and scope all reproduced. Amendment A3 correctly accepts "no `--selftest`". |
| `round35-c1-coverage` (624) | TRUE | `checks=6 defects=1`, V4 DEFECT 55/54 as cell says; `--selftest` rc 2. |
| `round35-hardening` (625) | TRUE | `run=6 failed=0` rc 0; `--skip H6` → `H6 skipped`, `run=5 failed=0`; one planted untracked file → `H6 FAIL untracked_anywhere=1`, rc 1. Live-lane figure 2 is tree-dependent, not re-measured. |
| `round36-c2` (626) | TRUE | `W4 DEFECT knowledge files=55 index rows=54`, `checks=6 defects=1`, rc 1, as cell says; both control files read `checks=6 defects=4`. |
| `round45-c1` (627) | TRUE | `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10 leaked=0`, `HONEST fixtures=104 admitted=104`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass` rc 0; both named controls match. |
| `round45-c2` (628) | TRUE, disclosed tip result | `V11 states=48 grader_pass=18 grader_fail=30 disagree=0`; predictor controls 30/12/21/DEFECT/ok all match. At this tip V2 is DEFECT (embedded P8 55/54), `checks=11 defects=1`: the cell states it. |
| `round46-c1` (629) | TRUE except one count | every verdict string reproduced (`PINS total=65`, `REFUSALS 20/20`, `SEALED 12/12`, `HONEST 104/104`, `CALIBRATION 32`, `REASON -`, `PREDICATE C1 pass`). The control count is wrong (see C1). |
| `round46-c2` (630) | TRUE | `checks=4 defects=0`, `PREDICATE C2 pass`, lines A–D identical; SETUP returns 1 as the cell says; `--selftest` rc 2; pins match. |
| `round46-c3` (631) | FALSE in two claims | `--filler` run gives `checks=7 defects=6`, `PREDICATE C3 fail`, rc 1, not `defects=0`. P8 (not P9, untracked=0) is the gate defect in a clean clone. The `0` branch is not reached at the tip. |
| `round50-c1` (632) | TRUE | `POPULATION 126`, `HONEST 126/126`, `REFUSALS 20`, `SEALED 12` and `20`, `MUTANTS total=15 caught=15 floor=12 verdict=met`, `PREDICATE R50-C1 pass`; `--work` absent → FileNotFoundError rc 1. |
| `round50-c2` (633) | TRUE | `POINTERS total=292 … unresolved=0` and the exact `SELFTEST pristine_rc=0 bogus_rc=1 … verdict=ok` line, rc 0. |
| `round51-routing` (634) | FALSE in two places | `--bogus` → rc 2, so "no `2` path exists" is wrong. "writes only a mkdtemp scratch" is wrong under `--run-checks`, whose ledger checks run with cwd = lane (none wrote at this tip). Selftest 11 cases, 8 red / 3 green confirmed. |
| `round51-surfaces` (635) | TRUE | `ANCHORS 20`, `PROBES present=14 absent=6`, `RESOLVE 14 floor=13 met`, `PREDICATE R51-C1 pass`; `--selftest cases=9`; absent manifest rc 1; `--bogus` rc 2; pins match the live digests. |
| `routed-findings` (636) | FALSE in one number | `ROWS 75/31/1/41/2`, `routed_open=32 oldest_round=39`, `SELFTEST 12/12`, invalid-row DEFECT, defects.jsonl refusal rc 2 all match. The `--observe` "measured `mismatched=1`" does not reproduce: 43 with `LANE` unset, 12 with it exported. |
| `tb2-grader-probe` (637) | TRUE | `cases=18 observed_pass=5 observed_fail=13 mismatches=0` rc 0 under uv; byte-equal to receipt; `--dry` rc 2; missing Bio rc 1; arithmetic 2766 = 3·(842+80) correct. |

## Corrected cell text (the false claims)

1. **`round46-c3` verdict cell.** Replace
   "`checks=7 defects=0` under `--filler`, which runs V3, V4, V6, V7, V9, V10, V12"
   with "under `--filler` (the do-nothing control, expected red) `checks=7 defects=6`, `PREDICATE C3 fail`, exit 1; at 87301ba V4, V6, V7, V9, V10, V12 DEFECT and V3 ok (V13 is the filler's measured red)". Also state beside the `0` branch that it is not reached at 87301ba (V2, V7, V8 red).
2. **`round46-c3` scope cell.** Replace
   "(the gate's own `P8`/`P9` fired on the clone's untracked wave files, and V2 passes `--require-clean-tree`)"
   with "(in a clean clone at 87301ba the gate's `P8` fires on `knowledge files=55 index rows=54`, the round-36 W4 drift; `P9` reports `untracked=0`)".
3. **`round51-routing` verdict cell.** Replace "· no `2` path exists" with "· `2` argparse usage only (measured `--bogus` → exit 2); the script declares no setup exit; an absent `--ledger` path raises `FileNotFoundError` with exit 1 (measured)".
4. **`round51-routing` scope cell.** Replace "writes only a mkdtemp scratch (kept with `--scratch`)" with "the script itself writes only a mkdtemp scratch (kept with `--scratch`); the ledger `check` strings it runs under `--run-checks` execute with cwd = lane and are not sandboxed, so any write is the row's command (none at 87301ba: 41 ran, 41 passed, clean tree)".
5. **`routed-findings` verdict cell.** Replace "(:154-160; measured `mismatched=1`, exit 1)" with "(:154-160; measured at 87301ba in a clean clone: `OBSERVE rows=75 mismatched=43`, exit 1 with `LANE` unset, `mismatched=12` with `LANE` exported; host-state dependent, since the checks read host paths, loopback ports and `${LANE:?}`)".
6. **`round46-c1` selftest cell.** Replace "the 35 controls under `.ufo/waves/round-46/claims/`" with "the 34 `control-*.txt` files under `.ufo/waves/round-46/claims/` (generator `stage2_controls.py`)". Counted: 34 `control-*` files, 38 entries in the directory.

`order-check` and the other 10 rows need no cell change.

## Counter-level finding (not a cell; reported under the C2 counter)

`plans/round52_c2_registry.py` `selftest_unbacked()` returns False for the whole cell as soon as
any `no … --flag` appears within 24 characters of "no". Amendment A3 describes ignoring a flag that
is explicitly negated. The code suppresses every flag in the cell. Measured:
`no \`--selftest\` in the script; self-test \`python3 plans/order_check.py --selftest\` (exit 0)` →
`False` (a false positive for the script's missing flag is suppressed). A fix that only strips the negated
flag but keeps whole-cell attribution is wrong: it flags the landed `order-check` cell (its `--receipt`
and `--claims` are attributed to `round40_c1_verify.py`). A tested variant attributes flags only inside a
backtick span that begins `python3 <script>`. It gives identical verdicts on all 74 registry rows and
catches the masked claim. Prototype: `receipts/probes/a3-fix-probe.py`. The counter is the lane's, so I
did not edit it. The L1 may choose to adopt the span rule. Whether this breaks the frozen C2 predicate
is the L1's ruling, not mine.

## Verification gaps (honest)

- The `0` branches of `round35-c1` (V4), `round36-c2` (W4), `round45-c2` (V2), `round46-c3` (V2, V7, V8) and the `--filler` run are not reached at the tip. Their results were measured and recorded, not assumed.
- `round46-c3` `--filler` and `round50-c1` `TREE dirty` were checked by code reading and a measured filler run. A full `TREE dirty` rerun (6 min) was not repeated.
- Historical numbers I could not re-derive: `round36`/`round45` "measured on a clean clone at base tip", the 18 tb2 synthetic predictions (provenance), `round50-c2` before-count `12 at 71f5f5f`, and the round-51 `--run-checks`-free figures.
- Host-dependent numbers (round-51 probe counts, routed `--observe` counts, the live-lane `H6 untracked_anywhere=2`) are reported as they measured today, in a clone.

## Files

- Verdicts JSON: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsB/rows-review-b.json` (scratch original: `/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/rows-review-b.json`).
- Item-specified scoped findings: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsB.md`.
- Receipts (logs of each run, probes and extraction scripts): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2RevRowsB/receipts/`.
- Landed rows and draft-to-landed comparison: `receipts/probes/landed-rows.json`, `landed-rows.txt`, `drafts-mine.json`.

No lane file, sibling file, `.ufo/state`, `.ufo/watchdog.log`, `templates/`, `scripts/`, `MANIFEST.json`, or fleet file was written. No git mutation was run. Scratch was removed after these copies.
