# R48C1PredCounter — path-keyed control attack

Axes named: calibration (C1); secondary concern: counter distinguishability.

## Counterexample and evidence

The strongest evidenced attack is the prior round-45 no-inspection path-keyed fence. Its entire decision was equivalent to `return "keyed-on-path" if "/refusals45-" in str(d) else None`; it passed that round's predicate while inspecting no fixture. The committed round-45 control receipt states `PREDICATE C1 pass`, exit 0, and the round-45 lesson records the bypass. This demonstrates a real false-positive class for the old counter, not that the current v3 counter is bypassed.

The stage-1 C1 contract explicitly carries forward that exact control as one that MUST print fail. Its counter delta also says fixture/build/module paths use per-run random tokens, padded parents and shuffled jobs. These measures remove the old stable `refusals45-<module>` path cue. A control keyed only to that literal path is therefore not a substantiated v3 bypass. I found no stronger keyed/path-keyed signal in the frozen-stage evidence that both distinguishes the hidden populations and yields the required hostile refusals plus all honest admissions.

## Freeze gate / no scored execution

Verified the stage-1 freeze exists in the committed lane tree: `a543d92083557dd9b33ee674e9b99b03411f80af`, timestamp `2026-10-27 06:53:29 -0300`; its committed claims file names “the round-45 keyed fence” among C1 controls that must fail. The scratch clone was checked out at that exact revision and `git rev-parse --show-toplevel` returned `/fast/scratch/hyaku/kengaku-r48/R48C1PredCounter/lane`.

Stage 1 expressly places the counter files, pins, frozen population, literals and before-control receipts in stage 2, after wave 1 returns and before claimed work is scored. They are absent at the assigned frozen base. Per the ordering rule, I did not run a counter/probe or any scored execution. This leaves the proposed v3-control outcome unmeasured; no claim of C1 admission or v3 bypass is made.

## Commands and observed outputs

- `git log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af` → `a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`.
- `git show a543d92083557dd9b33ee674e9b99b03411f80af:plans/round-48-claims.md` (first 30 lines) → includes the C1 frozen population/counter stage-2 sequencing and prior rejection summary; later search result at line 67 names “the round-45 keyed fence” as a must-fail control.
- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r48/R48C1PredCounter/lane`; `git checkout -q a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse HEAD` → `a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r48/R48C1PredCounter/lane`.
- Inspected frozen `plans/fixture_fence.py` and `plans/round46_c1_verify.py` only; no fixture Git calls and no scored runs.

Measured revision: `a543d92083557dd9b33ee674e9b99b03411f80af` (frozen base; not claimed work).

## Limits and smallest safe correction

No stage-2 v3 verifier/population/receipt existed in this revision, so whether a new path-derived key survives its actual harness cannot be established here. The prior `refusals45-` key is defeated in principle by per-run path randomization, but a stage-2 execution is needed to observe the frozen control fail. Smallest safe correction: stage 2 MUST run and retain the frozen historical keyed fence as a before-control, with its source digest and receipt, on the base/control tree before any claimed work is scored. The stage-1 claim already specifies this control; do not alter the predicate or kill rule.

Sources opened (local URL; accessed 2026-10-27):
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — “A control that passes refuses the counter: the claim stops honestly, it is never re-frozen after scoring.”
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — “repair over-refusal (9/9 novel honest controls refused) and broaden positive controls”
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1PredCounter/lane/.ufo/waves/round-45/claims/control-c1-fence-keyed_name.txt` — “PREDICATE C1 pass”, exit 0.
- `file:///fast/scratch/hyaku/kengaku-r48/R48C1PredCounter/lane/corpus/lessons/round-45.md` — “A fence that inspects nothing and keys on the counter's fixture path prints the same pass”.

VERDICT: no demonstrated v3 bypass at stage 1; historical keyed-control bypass is real for the prior counter. Scored testing blocked by the required absence of stage 2 at the measured frozen revision.
