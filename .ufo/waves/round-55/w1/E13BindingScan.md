# E13BindingScan — scoped findings (R55-C2 pre-integration binding scan)

Pre-integration data for R55-C2: how the CURRENT ledger/registry pair scores under the frozen
binding legs before `plans/round55_c2_entryargv.py` exists. Clean shared clone at tip
`80afa613…` (round-55 freeze; base `798f5e9e…`). Full table: `.ufo/waves/round-55/w1/E13BindingScan/binding-scan.tsv`.

## Counts (reconcile: 61+16+1 = 78 rows)

- L1-OK: **61**; L1-DIFF: **16**; L1-NO-PY3-SPAN: **1** (`tb2-grader-probe`).
- L2 flagged: **1** (`tb2-grader-probe`, `uv` wrapper as `argv[0]` — cell-sanctioned).
- L3 flagged: **0**.
- Registry parse: 78 unique rows, 0 duplicates; every ledger key has a registry row.

## r54 laundering routes in the REAL ledger: ABSENT (both were fixture-only)

- argparse-prefix abbreviation (`--selft`-style): **0 rows** — no ledger flag is a strict
  prefix of a longer flag in its own script's body.
- `uv` wrapper around an inline `-c` program: **0 rows** — no ledger `entry_argv` contains
  `-c`; the only non-python `argv[0]` wraps a real script file, inline-free.

## Rows E4/L1 must correct as data (17)

`adoption-check`, `anchor-digest-check`, `coverage-census`, `gate-flip-check`, `gate-timing`,
`ledger-tip` (used documented `--lane` control mode, not the primary `--source/--work` entry),
`mutant-direction-check`, `package-gate`, `round-close-check` (census path is a fleet-root
absolute outside the lane), `round28-census`, `round50-c1`, `round53-c2` (omits
`--source/--work` binding flags), `scratch-root-guard` (multi-span cell), `sources-adopt`
(ledger inserts `--lane .`, which the script does not accept — declared-red by design),
`stage-scan` (ledger's `--lane .` is rejected by the script — declared-red by design),
`tb2-grader-probe` (no py3-starting span; `uv` argv[0] → L2), `tip-receipts`.

Category tags and exact token diffs per row are in `binding-scan.tsv`'s note column.
Rows `sources-adopt`/`stage-scan` are the lane's own honest red declarations of unnamed
entry contracts — reconcile as ledger data, not laundering. `tb2-grader-probe`'s L2 is
cell-sanctioned; landing fix must be data (a plain-`python3` entry that truly resolves), not
a hand-edited registry cell.

## Evidence

Commands and exit codes: see `E13BindingScan/report.md`. No installs, no network, no lane
writes beyond this receipt, no git mutations. Scratch `/fast/scratch/hyaku/kengaku-r55/E13BindingScan/` deleted after receipts copied.
