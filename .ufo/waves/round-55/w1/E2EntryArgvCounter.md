# E2EntryArgvCounter — scoped findings (round 55, w1)

## Deliverable
`plans/round55_c2_entryargv.py` written (the only file changed). Imports the unchanged r54
module (importlib, controls-style `_load`) and reuses its static legs, hermetic Worker/run_row,
ledger and constants; adds the three frozen binding legs on top:

- **L1 ARGV-DEFECT** — ledger `entry_argv` must token-equal the registry cell argv (first
  backtick span starting `python3`, shlex-split). Counted inside the ROWS `argv_defect=` field
  exactly as the frozen after predicate expects; separately broken out on the
  `BINDING l1 l2 l3` line.
- **L2 WRAPPER-DEFECT** — argv[0] ∉ {python3, python}, or any token ∈ {uv, pipx, poetry, npx,
  uvx}, or any token starting with `-c`.
- **L3 ABBREV-DEFECT** — argv flag token not verbatim in the script body but a proper prefix of
  a body flag (argparse abbreviation, static).

`evaluate` keeps the r54 output shape (ROWS/RUN/TIPSTATE/MIGRATION) plus `wrapper_defect=N
abbrev_defect=N` in ROWS and a `BINDING l1 l2 l3` line; execution runs the **registry cell
argv** hermetically through r54's Worker/run_row; `--dry` is static-only; CLI is exactly
`--lane --source --work --jobs --timeout --dry --selftest`; selftest fixtures live under
`--work`/TMPDIR (controls' argparse-gate shape with a git-toplevel guard).

## Verification (all run, receipts in `.ufo/waves/round-55/w1/E2EntryArgvCounter/`)
- `--selftest` → exit 0, one line per case, 4/4 PASS (truthful passes; tampered-argv →
  ARGV-DEFECT+fail; uv wrapper → WRAPPER-DEFECT+fail; `--selft` → ABBREV-DEFECT+fail).
- Frozen kills via `plans/round55_c2_controls.py`: `abbreviated-selftest --against r55` → kill
  demonstrated (counter exit 1, `ARGV-DEFECT` + `ABBREV-DEFECT fixture-gate:` lines);
  `uv-decoy-script --against r55` → kill demonstrated (counter exit 1, `ARGV-DEFECT` +
  `WRAPPER-DEFECT fixture-gate:` lines). Controls' own `--selftest` (before-state: the
  unchanged r54 counter passes both laundering fixtures) → exit 0, confirming the frozen
  do-nothing control.
- `--dry --lane <lane>` → exit 1 mid-wave with `ROWS registry=78 ledger=78 missing=0 extra=0
  argv_defect=17 wrapper_defect=1 abbrev_defect=0 bad_decl=0 duplicate_names=0 headings=1`,
  `BINDING l1=17 l2=1 l3=0`.
- Full run over the lane working tree (`--jobs 8 --timeout 45`) → exit 1 mid-wave; L4 executed
  61 rows hermetically.

## Defects the counter surfaces (DATA — left for the L1's frozen correction pass, untouched by this seat)
1. 16 L1 mismatches: registry cells with placeholder tokens (`<expect.json>`, `DIR`, `REV`,
   `PATH...`, `[--evidence-ref head or index]` …) vs resolved ledger argv — adoption-check,
   anchor-digest-check, coverage-census, gate-flip-check, gate-timing, ledger-tip,
   mutant-direction-check, package-gate, round-close-check, round28-census, round50-c1,
   round53-c2, scratch-root-guard, sources-adopt, stage-scan, tip-receipts.
2. `tb2-grader-probe`: registry cell has no `python3` span and the ledger argv is a
   `uv run … python3 …` wrapper → L1 + L2 both flag it. Needs a data correction (or a dated
   amendment) before the after-run can reach `wrapper_defect=0`.
3. Mid-wave execution noise (expected, resolved by other seats' landings): `round52-c2`
   LAUNDERED (the known r54 regression the R55-C1 seat is repairing), `round35-c1-coverage`
   EVIDENCE-MISSING (frozen ledger-truth correction (a) covers it), 9 TIMEOUTs at my 45 s
   smoke cap only.

## Dead ends
- Running the counter from a fresh `git clone` of the lane fails (clone carries committed
  bytes only; the file is uncommitted until integration) — expected, not a defect.
- Early draft skipped L2/L3 when L1 fired, which would have hidden the frozen
  WRAPPER/ABBREV attribution; corrected so all three legs run independently.

No tools installed, no mutating git, scratch deleted after staging receipts.
