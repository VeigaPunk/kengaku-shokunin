# R48C1MutNames — Q39 name-shape mutation probe

Axes: calibration (C1); name-independence / Q39.

## Freeze and execution gate

Required source files read in full: `plans/round-48-claims.md` and `corpus/lessons/round-46-verifier-spotcheck.md` (local lane sources; no external URL was opened). The claims bind C1's stage-2 counter and fixture population before scored evaluation; Q39 requires per-run randomized fixture/build/module names and shuffled fence jobs. The routed spotcheck identifies prior name-sensitive/mutation-sensitivity concerns but does not provide the R48 counter.

Exact commands run and observed output:

```text
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -3
bf783c1 round-48: w1 ready handoff marker
453ddfd round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)
a543d92 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter)

git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse HEAD
bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767

git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-tree -r --name-only a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round48_c1_verify.py plans/fixture_fence.py
plans/fixture_fence.py

test -e /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round48_c1_verify.py && echo counter-present || echo counter-absent
counter-absent
```

Stage-1 freeze revision `a543d92083557dd9b33ee674e9b99b03411f80af` is committed and timestamps `2026-10-27T06:53:29-03:00`. However, it contains no `plans/round48_c1_verify.py`; the claims explicitly state that counter and its pins/population are to be supplied at stage 2 after wave 1, before claimed work is scored. Therefore the required measurement gate is not satisfied. I did not run a counter, probe, fence detector, or scored evaluation; no pristine/mutant behavioral outputs or hashes are claimed.

## Mutation / detector result

No fixture/build/module name mutation was applied. No paired pristine/mutant detector was run because the frozen R48 C1 detector and stage-2 freeze do not exist in the committed tree at this point; running an improvised substitute would not be the same bounded detector required for a valid paired result. Thus Q39 name dependence is **inconclusive**, not killed or survived. No claimed-work bytes were changed.

Revision measured: stage-1 freeze `a543d92083557dd9b33ee674e9b99b03411f80af` (inspection only; no behavior measurement). Scratch root was created with `TMPDIR=/fast/scratch/hyaku/kengaku-r48/R48C1MutNames` and removed; no scratch tree remains. No tools installed or updated.

Limits: this is a freeze-gate blocker, not a finding that the fence is name-independent. Paired results remain to be collected only after the stage-2 counter/population freeze is committed and the identical bounded detector can be run on pristine and name-mutated scratch fixtures.

VERDICT: INCONCLUSIVE — no mutation/detector run; stage-2 C1 freeze absent, so scored execution was correctly withheld.
