# Round-34 census-previous consistency check

## Observed

- Frozen baseline `.ufo/waves/round-34/claims/census-before.txt` has 15 W04 records, in order: S040, S048, S057, S058, S059, S064, S065, S066, S067, S068, S069, S071, S075, S076, S100; followed by `kengaku ok .../corpus/SOURCES.md` (lines 1–16). The round-33 after receipt has those identical 15 W04 lines and same `ok` line, then `exit=0` (lines 1–17). **Diff: no changes** to the warning rows; round-33 records explicit exit 0.
- Round-29 `corpus/evidence/round29-attempt2/census-after.txt` contains 14 W04 ids S040, S048, S057, S058, S059, S064, S065, S066, S067, S068, S069, S071, S075, S076; then `ok` (lines 1–15). It omits S100 and the file has no explicit `exit=0` line. Thus that receipt itself does not establish the exit code; contemporaneous round-29 report `R29a2rCalibration.md` reports fleet validation exit 0 and 14 lane W04 lines (lines 52–53; grep result).
- Round-30 `corpus/evidence/round30/census-after.txt` contains those same 14 ids, then `ok` and `exit=0` (lines 1–16). Round-31 `corpus/evidence/round31/census-after.txt` contains all 15 round-34 baseline ids, including S100, then `ok` (lines 1–16); its explicit exit code is not present in the read receipt. Round-31 corroborating report `R31FxTrends.md` says pristine-HEAD sandbox prints 15 W04 + ok, exit 0, and baseline prints the 14 warning rows (lines 21–22).

## Diff and interpretation

The 15 frozen round-34 ids exactly match round-31 and round-33 after, with no differences. Compared with round-29/30 after, the only additive warning is **S100** (`github.com/laude-institute/terminal-bench-2`); this is the known cross-scope duplicate (round-31 report `R31FxCensus7.md`, lines 25–26). No removals or other changes are evidenced. Exit 0 is explicit in round-30 and round-33 after receipts and reported for round-29/31 in the cited reports; the round-31 after receipt itself has no `exit=0` trailer.

## Evidence limits

This is a comparison of committed/stored receipt bytes, not a fresh invocation of the census command. Round-29/30 receipts document the earlier 14-warning state, whereas round-31/33 and the round-34 frozen baseline document the additive S100 state. No claim is made about a live current census run.

VERDICT: recon-census-consistent
