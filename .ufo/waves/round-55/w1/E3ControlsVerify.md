# E3ControlsVerify — seat findings (round 55, w1)

**Scope:** verify the frozen fixture builder `plans/round55_c2_controls.py`
(commit `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`). Lane writes: none.

## Verdict

The frozen before-state for R55-C2 **reproduces exactly**. No drift found.

## Runs (all exit 0)

1. `python3 plans/round55_c2_controls.py --selftest` →
   `SELFTEST cases=4 failures=0` (r54 passes both laundering fixtures; truthful
   red-declared fixture passes; `--selft` abbreviation confirmed live).
2. `--case abbreviated-selftest --against r54` → `PREDICATE R54-C2 pass`,
   `COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=1`,
   `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)`.
3. `--case uv-decoy-script --against r54` → identical predicate/route shape with the
   uv-wrapped argv; laundering demonstrated.

## Diff vs committed receipts

- vs `c2-before-abbreviated-selftest.txt`: byte-identical except the `SOURCE rev=`
  fixture hash (`82c52797…` → `e84abba1…`, expected per-run fixture commit id).
- vs `c2-before-uv-decoy-script.txt`: byte-identical except the `SOURCE rev=` fixture
  hash (`8d00e0a2…` → `1a8428b6…`).
- All PREDICATE / ROUTE / COUNTER-EXIT / TRUE-ENTRY / ROWS / RUN / TIPSTATE lines
  match the receipts exactly. `clean=yes lane_rev_equal=yes` holds.

## Drift / defects

None. The r54 counter's own `laundered=0` output on both red-before fixtures is the
exact committed evidence that the r54 entry-argv binding gap is live at base — the
premise of R55-C2's binding legs (L1–L4 of `plans/round55_c2_entryargv.py`).

## Notes

- Full outputs, environment, and analysis:
  `.ufo/waves/round-55/w1/E3ControlsVerify/report.md`.
- Builder's `--against r55` mode intentionally not run (counter still under
  construction; builder would exit 2 SETUP — out of this seat's frozen command set).
- Builder writes only under a self-cleaned temp dir in `/fast/scratch/hyaku/kengaku-r55`;
  verified zero leftover dirs and zero lane-tree writes from this seat.
