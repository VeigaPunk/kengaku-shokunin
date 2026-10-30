# RV3R52PatchAnatomy — scoped findings (round 55, wave 1)

Full analysis: `.ufo/waves/round-55/w1/RV3R52PatchAnatomy/anatomy.md`. Seat report: `.ufo/waves/round-55/w1/RV3R52PatchAnatomy/report.md`.

## Findings

1. **Patch's claimed fix**: replace the cell-wide `no … --flag` early return (`plans/round52_c2_registry.py:74`) with a flag-local
   negation (`E3R52RegistryFix/round52_c2_registry.py:75-76`), plus K5/K7/span selftests (3 → 6 cases).
2. **order-check regression**: the `order-check` row (`SKILL.md:590`) names `plans/round40_c1_verify.py` as the only script in its
   self-test cell, but also documents `--receipt`/`--claims`, which belong to `plans/order_check.py:143-145`. The old blanket
   return hid this. Removing the blanket exposed it: `SELFTEST-UNBACKED \`order-check\``, exit 1. Only this row changes
   (old vs patched over 79 rows). Root cause is flag→script attribution, not the negation.
3. **K7 masking**: the in-tree K7 case keeps only the ghost row, so `MISSING 2` forces the verdict red. Its check
   (`"plans/ghost_tool.py" in entry_missing and verdict(t) == 1`, patched line 206) does not depend on `entry_missing`.
   Dropping that term from the verdict (line 133) still gives `cases=6 failures=0`. An isolated fixture (advertised scripts
   registered) kills the mutant (scratch run: rc 0 on the mutant, 1 on the patched counter).
4. **No-harm was never shown**: `E8NoharmR53C2.md` checks `round53_c2_tipstate.py`, not the R52 counter. The R4 review
   (`.ufo/waves/round-54/w1/R4R52Fix/review.md`, DO-NOT-INTEGRATE) is the only no-harm evidence and it is red. `--dry` is not
   implemented by either counter.
5. **Candidate fix (sketch, tested in scratch only)**: a self-test flag is unbacked only if it is absent from both the cell's
   sole script and the row's entry script. On the lane's 79 rows it changes zero verdicts and turns `order-check` green. Cost:
   a flag absent from the cell script but present in the entry script is no longer reported (zero current rows).
   Rejected: entry-only attribution (flips `package-gate` red) and command-span-only attribution (drops claims on 8 rows).
6. **Frozen-claims constraint**: `plans/round-55-claims.md:150-151` says the production r52 counter stays unchanged this round.
   Any fix therefore needs L1 decision (new counter or claims amendment).

## Name correction

The brief's `.ufo/waves/round-52/w2/*R4*/` does not exist. The R4 review is at `.ufo/waves/round-54/w1/R4R52Fix/review.md`.
`grader.py:1430 check_r11_ordering` is a different check (R11 preregistration ordering); the regressed `order-check` is the
registry row, not grader.py.

## Commands and exits (read-only)

- `ls -d .ufo/waves/round-52/w2/*R4*` → no match (dead end).
- `grep -n check_r11_ordering grader.py` → 1430; `grep -c order_check grader.py` → 0.
- Reads of E3, E8, R4R52Fix/review.md + evidence.json + independent-delta.diff, plans/round52_c2_registry.py, plans/order_check.py,
  plans/round40_c1_verify.py, plans/round-55-claims.md (exit 0).
- Scratch probes with `python3 -B` in `/fast/scratch/hyaku/kengaku-r55/RV3R52PatchAnatomy/`: parse all 79 rows, old vs patched vs
  candidate attribution, K7 mutant on an isolated fixture (exit 0 for reported runs). One probe exited 1 on a path bug in my own
  harness; rewritten, not a lane result. My first `mktemp -d /tmp/rv3.*` probe dir was not removed by a trap; I removed it
  afterward together with `/tmp/rv3.out`, a file whose origin I did not create (it matched my glob; flagged for L1 in case it was a peer's).
- No lane file, fleet-root file, or git/jj mutation written. The lane's own `plans/` may have had `__pycache__` touched by imports; I
  suppressed bytecode writes with `sys.dont_write_bytecode`/`-B`.

## Tooling

None installed. No pacman, uv, npm, or cargo use.
