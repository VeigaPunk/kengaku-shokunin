# R48C2MutVerdict — predicate mapping mutation probe

Axes named: **coverage** (assigned), with predicate false-success and false-failure detection as the measured sub-axes.

## Freeze and scope

The required frozen claims were read in full; the round-46 spot-check was read. The stage-1 freeze is present at `a543d92083557dd9b33ee674e9b99b03411f80af`; observed command output:

```text
FREEZE PRESENT at stage-1
a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27T06:53:29-03:00 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims
```

Revision inspected: `REV a543d92083557dd9b33ee674e9b99b03411f80af`. The current lane tip at inspection was `bf783c1`; `plans/round48_c2_verify.py` was absent from the lane tree, and stage 2 (which pins the counter, controls, and `<V>`) was not available. The only available counter was `plans/round46_c3_verify.py`, SHA-256 `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`.

## Commands and observed results

- `git cat-file -e a543d92083557dd9b33ee674e9b99b03411f80af:plans/round-48-claims.md` — succeeded; freeze present.
- `git show -s --format='%H %cI %s' a543d92083557dd9b33ee674e9b99b03411f80af` — output shown above; freeze predates this inspection.
- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`; `git checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse HEAD` → `a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C2MutVerdict/lane`.
- `sha256sum plans/round46_c3_verify.py` → `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`.
- Inspected mapping at lines 902–908: normal path prints `checks=... defects=...`, prints `PREDICATE C3 pass|fail`, and returns 0 iff defects are zero; package-unreadable path uses the same mapping.
- The counter itself states that V2 runs `pkg_gate.py --rerun` (P10, a fresh probe run), and that V2 is post-stage-2 only. This counter offers no P10-disabled switch. I did not execute it or any probe.
- `round48_c2_verify.py` lookup → not found.

## Mutation result

**Mutant:** none applied. **Expected detector:** the frozen R48-C2 counter must show a false-success control as fail/nonzero and a clean claimed tree as pass/zero; false-failure mutation must be detected against the clean tree. **Output/verdict:** inconclusive / blocked before mutation. Stage 2 and the R48 counter/disabled-P10 detector were unavailable; running the only available counter would invoke forbidden P10. Thus no pristine, mutant, or restored detector executions occurred and no false-success/false-failure claim is made. No counter bytes were changed; SHA-256 before/after remains `a971c24dd5d0cb880e97ad4dd80315fcf58afaa02f8cffb5cc2e803aa292a8d4`.

Limits: this report does not assess C2 admission, the eventual stage-2 mapping, or any scored counter result. No external source was opened, so no URL quote applies.

VERDICT: INCONCLUSIVE — stage-2 frozen counter and P10-disabled behavioral detector unavailable.
