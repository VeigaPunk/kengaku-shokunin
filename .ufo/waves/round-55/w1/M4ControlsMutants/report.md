# M4ControlsMutants — final report

Seat: `M4ControlsMutants` (mutation-tester) · kengaku round 55, wave 1 (v2) · date 2026-10-30.
Assignment: mutation-test the **fixture realism** of `plans/round55_c2_controls.py` (scratch copy
only) with three mutants (A: argparse `allow_abbrev=False`; B: gate true-entry exit → 0; C: ledger
`entry_exit` → 1/red) and record observed outputs.

## Verdict

**All three mutants killed; none survived.** The laundering fixture is *not* vacuous: it genuinely
rides on argparse prefix abbreviation (A), on a truly-failing registry entry (B), and the r54
counter does not pass a ledger row whose declared entry exit contradicts the observed one (C/C′).
Full observed outputs: `.ufo/waves/round-55/w1/M4ControlsMutants/mutants.md`.

Two defects found in the round-55 instrument (reported, not fixed — they belong to the seat that
owns `plans/round55_c2_controls.py`): DEFECT-1 (the fixture's ledger writer can only emit a
statically valid *green* row, so a red flip is caught as `BAD-DECL`/`executed=0` rather than the
executed-leg `MISMATCH`), DEFECT-2 (the tool hardcodes `/fast/scratch/hyaku/kengaku-r55` as its
work dir and has no `--work` argument; on a host without that path it dies with an uncaught
`FileNotFoundError` instead of a clean SETUP exit). Neither touches a frozen predicate, counter or
kill rule; neither invalidates R55-C2's frozen before/after receipts.

## What I ran (all commands from `$S=/fast/scratch/hyaku/kengaku-r55/M4ControlsMutants`)

Setup (one lane-shaped scratch copy holding the two plan files the tool loads through `LANE`):

```
mkdir -p $S/lane/plans
cp <lane>/plans/round55_c2_controls.py  $S/lane/plans/
cp <lane>/plans/round54_c2_entrytruth.py $S/lane/plans/
sha256sum <lane>/plans/round55_c2_controls.py $S/lane/plans/round55_c2_controls.py
```
→ exit 0; both `c7591bc6d682c542a595b7fc959f74af61254c53863b8aafd72ecf7c50cbf13d` (byte-identical).

| # | command | exit | result |
|---|---|---|---|
| 1 | `python3 lane/plans/round55_c2_controls.py --case abbreviated-selftest --against r54` (pristine) | 0 | `PREDICATE R54-C2 pass`, `COUNTER EXIT 0`, `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)` |
| 2 | `python3 lane/plans/round55_c2_controls.py --case uv-decoy-script --against r54` (pristine) | 0 | same shape, `ROUTE laundering demonstrated` |
| 3 | `python3 lane/plans/round55_c2_controls.py --selftest` (pristine) | 0 | `SELFTEST cases=4 failures=0` |
| 4 | **Mutant A** (`p = argparse.ArgumentParser(allow_abbrev=False)`) → `--case abbreviated-selftest --against r54` | 1 | `LAUNDERED fixture-gate declared green, entry exit=2`, `PREDICATE R54-C2 fail`, `COUNTER EXIT 1`, `ROUTE laundering NOT demonstrated (r54 rc=1, true entry exit=1)` — **killed** |
| 5 | **Mutant A** → `--selftest` | 1 | `SELFTEST FAIL r54-passes-abbreviated-selftest`, `SELFTEST FAIL abbreviation-live (--selft exits 0)`, `failures=2` |
| 6 | restore pristine (`cp pristine-round55_c2_controls.py lane/plans/…` + sha256) | 0 | `c7591bc6…` == pristine |
| 7 | **Mutant B** (gate `sys.exit(1)`→`sys.exit(0)`) → `--case abbreviated-selftest --against r54` | 1 | `PREDICATE R54-C2 pass`, `COUNTER EXIT 0`, `TRUE REGISTRY ENTRY … exit=0`, `ROUTE laundering NOT demonstrated (r54 rc=0, true entry exit=0)` — **killed** |
| 8 | **Mutant B** → `--case uv-decoy-script --against r54` | 1 | same flip — **killed** |
| 9 | restore pristine + sha256 | 0 | `c7591bc6…` |
| 10 | **Mutant C** (ledger `entry_exit 0/green`→`1/red`) → `--case abbreviated-selftest --against r54` | 1 | `BAD-DECL fixture-gate`, `RUN executed=0`, `PREDICATE R54-C2 fail`, `COUNTER EXIT 1` — **killed** (not a pass) but the detector is `BAD-DECL`, not the predicted `MISMATCH` (DEFECT-1) |
| 11 | **Mutant C′** (C + statically-required red `reason`/`evidence`) → `--case abbreviated-selftest --against r54` | 1 | `MISMATCH fixture-gate declared exit=1 observed exit=0`, `RUN executed=1 … mismatched=1`, `PREDICATE R54-C2 fail` — **killed, predicted detector observed** |
| 12 | **Mutant C′** → `--case uv-decoy-script --against r54` | 1 | same `MISMATCH` line — **killed** |
| 13 | restore pristine + sha256 + re-run case | 0 | `c7591bc6…`; case exit 0, `ROUTE laundering demonstrated` |
| 14 | restore + re-run `--selftest` | 0 | `SELFTEST cases=4 failures=0` |
| 15 | `sha256sum <lane>/plans/{round55_c2_controls,round54_c2_entrytruth}.py`; `git -C <lane> status --porcelain -- plans/` | 0 | `c7591bc6…` / `44c3f412…`; only `?? plans/round55_c2_entryargv.py`, `?? plans/round55_c3_chess_probe.py` (other seats' untracked instruments) |
| 16 | `ls -d /fast/scratch/hyaku/kengaku-r55/kengaku-r55-controls-*` | 2 | no leftover fixture dirs |
| 17 | `python3 -c "tempfile.mkdtemp(dir='/fast/scratch/hyaku/kengaku-r55-absent')"` | 0 | `FileNotFoundError` — basis for DEFECT-2 |

## Files I wrote

- `.ufo/waves/round-55/w1/M4ControlsMutants/mutants.md` — per-mutant expected detector, observed
  output, exit codes, restoration evidence, summary table.
- `.ufo/waves/round-55/w1/M4ControlsMutants/report.md` — this report.
- `.ufo/waves/round-55/w1/M4ControlsMutants.md` — scoped findings for the L1.

Nothing else was written: no lane `plans/*.py`, no `LOG.md`/`SCORECARD.md`/`MANIFEST.json`, no
`.ufo/state/`, no `.ufo/watchdog.log`, no fleet-root `scripts/` or `templates/`, no sibling repo,
no `.scratch/`. The scratch tree `/fast/scratch/hyaku/kengaku-r55/M4ControlsMutants/` was deleted
after the receipts were copied into the files above.

## Bounds honoured

- Scratch copies only: every mutation was applied to `$S/lane/plans/round55_c2_controls.py`; the
  lane file's sha256 is unchanged (`c7591bc6…` before and after all cycles).
- No mutating git/jj command was issued by this seat against the lane or any repo. The only git
  activity was inside the tool's own throwaway fixture repos under the round scratch root, each of
  which asserts its own git toplevel (`_fixture()`'s `fixture root guard`).
- No subagents dispatched (leaf seat). No `agent://all` traffic. No network calls.
- No tools installed or upgraded (nothing to install; `uv` was already present at
  `/home/vgpnk/.local/bin/uv` and was only executed by the frozen fixture).
- An unrun check has not passed: every row above with an exit code was actually executed.

## Dead ends / notes

- The predicted detector for mutant C was not reachable by the literal one-field flip, because the
  fixture's own ledger writer never emits a statically valid red row. C′ restores the missing
  `reason`/`evidence` and then the predicted `MISMATCH` appears. Both runs are recorded; the
  contract ("must flag a MISMATCH (not pass)") is met by C′ and substantively met by C.
- The `--against r55` arm of the tool was not exercised: it needs `plans/round55_c2_entryargv.py`
  (an untracked instrument owned by another seat, still under construction) and is outside this
  seat's mutation assignment (A/B/C all target the r54 laundering route).
