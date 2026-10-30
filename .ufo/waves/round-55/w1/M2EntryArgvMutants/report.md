# Seat report — M2EntryArgvMutants (kengaku round 55, wave 1)

Mutation probe of the NEW legs of `plans/round55_c2_entryargv.py` (R55-C2 instrument): L1
ledger↔registry argv identity, L2 interpreter/wrapper, L3 flag-abbreviation, L4 registry-cell
ground truth. Scratch copies only; lane untouched. Per-mutant evidence: `mutants.md` (same
dir); raw receipts: `receipts/`.

## What I ran (commands + exit codes)

All under scratch root `/fast/scratch/hyaku/kengaku-r55/M2EntryArgvMutants/` (created with
`mkdir -p`); cwd was the scratch dir for every command. No tool installs (python3 3.14.8 and
git already present).

1. `python3 mut_harness.py` — exit 0, wall 1.8 s (bound: 60 s steps / 25 min budget; the
   harness itself enforces a 1500 s deadline and 60 s `run_row` timeouts). It:
   - copies `plans/round55_c2_entryargv.py` + `plans/round54_c2_entrytruth.py` into six
     `mods/<variant>/plans/` trees (pristine + 4 single-leg mutants + 1 supplementary combined),
     applying exactly one unique-site string replacement per single-leg mutant (assert count==1,
     `py_compile` checked);
   - imports the lane's `round55_c2_controls.py` read-only for `CASES`, `GATE_SRC` and
     `_fixture`, building the two frozen controls fixtures byte-equivalently;
   - builds four leg-isolating one-row git fixtures (toplevel guard asserted, mirroring
     `controls._fixture`);
   - runs each variant's `evaluate(fixture, fixture, work, 1, 60, False)` over all 7 fixtures
     (42 runs) and computes flip verdicts vs pristine.
2. Detector-validity checks inside the harness: pristine `--selftest` → `[selftest] 4/4 PASS`,
   exit 0; truthful fixture F0 → `PREDICATE R55-C2 pass` rc 0 under all six variants.
3. Restoration check: `sha256sum` of both lane modules after the probe — identical to the
   pre-probe hashes (`2bf9e66c…6ea74`, `44c3f412…0da97`); the lane files were never opened for
   writing. Mutant bytes lived only in scratch and were deleted with the scratch dir.
4. Git usage: read-only `git -C` against the lane (log/status at start); `git init/add/commit`
   only inside scratch fixture dirs, each guarded by
   `git rev-parse --show-toplevel` == fixture root (host-guard rule). No mutating git anywhere
   else; no `uv`/wrapper execution needed (fixtures use plain `python3`).

## Files I wrote

- `.ufo/waves/round-55/w1/M2EntryArgvMutants/mutants.md` — per-mutant kill evidence (required).
- `.ufo/waves/round-55/w1/M2EntryArgvMutants/report.md` — this report.
- `.ufo/waves/round-55/w1/M2EntryArgvMutants.md` — scoped findings summary (fleet level).
- `.ufo/waves/round-55/w1/M2EntryArgvMutants/receipts/{matrix.json,matrix.txt,
  diff-M1-L1-silenced.patch,diff-M2-L2-silenced.patch,diff-M3-L3-silenced.patch,
  diff-M4-L4-ledger-argv.patch,diff-M1M4-combined-r54-behavior.patch,mut_harness.py}`.
- Scratch dir deleted afterwards (`rm -rf`), receipts copied out first.

## Results (verdicts; full evidence in mutants.md)

| mutant | verdict |
|---|---|
| M1 L1 comparison removed | KILLED (F1 flips: ARGV-DEFECT fail → `PREDICATE R55-C2 pass`) |
| M2 L2 wrapper check removed | KILLED (F2 flips: WRAPPER-DEFECT fail → pass) |
| M3 L3 abbreviation check removed | KILLED (F3 flips: ABBREV-DEFECT fail → pass) |
| M4 L4 registry-argv → ledger-argv (single-leg) | SURVIVED — vacuous (coverage finding) |
| M1+M4 combined (supplementary, r54 behavior) | laundering re-introduced (F4c flips → pass) |

No mutant broke the truthful baseline (F0 stays pass under all variants) — none of the legs is
over-firing on honest input.

## Defects / findings

1. **L4 single-leg silence is unobservable** (SURVIVED mutant): `evaluate` excludes L1-flagged
   rows from execution and L1-clean rows have ledger argv ≡ registry argv, so replacing L4's
   registry-cell argv with the ledger argv changes nothing on any input. L4's registry-binding
   is redundant *given L1* — but jointly load-bearing: with L1 silenced (M1), F4c is still
   caught at runtime (`LAUNDERED fixture-gate declared green, entry exit=1`), and only M1+M4
   (the exact r54 behavior) re-introduces laundering. The acceptance wording "the L4 mutant must
   re-introduce the laundering" is not achievable at single-leg granularity; the combined probe
   demonstrates it. This is a redundancy-ordering finding about the instrument, not a soundness
   break of R55-C2 — the frozen kill-rule attack (all static legs clean while the registry
   entry truly fails) remains impossible: with all static legs clean, ledger argv ≡ registry
   argv and L4 executes exactly that argv.
2. **L2's `argv[0]`-interpreter clause is unreachable as sole detector while L1 is intact**
   (derived, not run): a wrapper at `argv[0]` necessarily breaks token-identity with the
   registry span, so L1 always co-fires. Only the inline `-c` clause is independently
   load-bearing (proven by F2/M2).
3. **Third r54 laundering route demonstrated en passant**: F2's inline `-c`-suffix argv passes
   the unchanged r54 counter's `entry_mode_ok` (SHELLS contains bare `-c` only, so
   `-cprint(…)` slips through; `--selft`/`--go` are not exact FORBIDDEN tokens either — F3/F4c
   pass r54 as well), corroborating the r54→r55 claim surface. No action requested from this
   seat; r54 counter is not mine to change.

## Dead ends / honest non-results

- First F4c draft (`… --selftest` as the divergent token) was rejected by design before
  running: r54's `entry_mode_ok` hard-forbids exact `--selftest`, so r54 legs would have co-fired
  and the fixture would not isolate the L1×L4 pair; replaced with a gate-green `--go` flag,
  which every static leg tolerates. (Static reasoning, no run wasted.)
- F2 needed its own gate body (`GATE_NOC`): controls' argparse gate exits 2 on the
  `-cprint(…)` tokens (unrecognized arguments), which would have made L4 co-fire a MISMATCH;
  the `-c`-tolerant gate keeps the fixture L2-sole.
- No inconclusive cells: the pristine baseline held, so all 42 runs are valid observations.
  Probe used 1.8 s of its 25-minute budget; no provider calls, no installs.

## Bounds compliance

- Wrote only: the two `.ufo` receipt/evidence paths above + `w1/M2EntryArgvMutants.md` + scratch.
- No subagents spawned; no `agent://all`; no sibling files touched; no MANIFEST/.ufo-state/
  fleet-scripts writes; no pacman; no network; no model-serving/benchmark endpoints.
