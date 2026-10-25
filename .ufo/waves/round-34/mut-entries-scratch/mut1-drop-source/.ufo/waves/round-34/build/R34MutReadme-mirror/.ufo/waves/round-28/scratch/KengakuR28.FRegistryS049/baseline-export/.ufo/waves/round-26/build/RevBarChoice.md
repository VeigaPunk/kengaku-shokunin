# RevBarChoice — C1 CP95 / clustering review

Scope: novelty axis; review of the frozen C1 bar and a read-only proxy replay, not the final instrument (absent at this lane head).

## Findings (highest severity first)

1. **HIGH — per-record exact CP95 is not justified as an exact interval under within-pid dependence.** The frozen rule is two-sided CP95 with PASS iff lower bound ≥0.95 (`plans/round-26-claims.md:69-73`; implementation splits alpha/2 at `plans/attrib_calibration.py:144-152`). It has exact binomial coverage only for independent Bernoulli trials; repeated turns within a pid are not independent by design (e.g. r8 A-INC: 100 records / 10 pids, 10 turns each; r12 A-INC: 640 / 64). `grader.py:121-134` also makes the parse path depend on which fenced block succeeds, so a pid's recurring response format can create correlated verdict changes.

   Proxy replay of the committed raw+ok population (actual `extract_json_block` and grade functions; F3/F4 applied to the extracted object, replacing the last fenced block): baseline reproduced stored ok on 1,948/1,948 state/sequence records; B-cell plain `grade_state` replay matched 32/32. F3: 17/1,803 verdict changes, pooled CP95 invariance [0.9849, 0.9945] PASS. F4: 17/1,650 changes, [0.9836, 0.9940] PASS. All 17 changes for each family were in r8-B records, across 7 `(file,pid)` clusters (pid counts 1:2, 2:4, 3:4, 4:2, 5:1, 6:1, 7:3); r8-B alone was 15/32 invariant, exact CP95 [0.2909, 0.6526]. Thus the pooled PASS hides a sharply fragile stratum.

   Verdict-flip check: a pre-specified *pid-composite* worst-case sensitivity (pid passes only if every applicable record is invariant) gives F3 171/178 pids, CP95 [0.9207, 0.9840], and F4 139/146, [0.9037, 0.9805] — both change PASS → INDETERMINATE. This is a different estimand, not an exact correction for per-record rate. A record-weighted bootstrap resampling whole `(file,pid)` blocks within file (100,000 reps, seed 26026) instead gives F3 [0.9853, 0.9956] and F4 [0.9841, 0.9951], so neither flips under that cluster-robust proxy interval. The methods therefore disagree; do not silently substitute worst-case pid CP for the frozen pooled estimand.

2. **MEDIUM — report stratum results; pooled bar can conceal a broken grader path.** The observed 15/32 F3/F4 r8-B invariance is below 0.95 even though pooled record-weighted intervals pass. Pre-register and publish family × response-cell/grade-family counts and intervals (at minimum r8-B separately); state explicitly that pooled results do not certify each stratum. C1 currently names state, sequence, and r8-C graders (`plans/round-26-claims.md:46-52`) but does not explicitly map r8-B; proxy state re-grade matched its stored verdicts, yet the mapping should be frozen.

## Pre-registerable sensitivity

- Keep the frozen CP95 as the primary descriptive pooled interval, but do not call it exact under clustered sampling.
- Before final instrument output, append a sensitivity specifying the independent unit as `(population file,pid)`. Within each file, resample eligible pid blocks with replacement, preserve all turns/cells in each block, recompute the record-weighted success proportion, and use a fixed-seed 100,000-replicate percentile 95% interval; apply the same 0.95 PASS/FAIL/INDETERMINATE thresholds. Freeze family applicability before computing outcomes.
- Also report the pid-composite worst-case interval as a clearly labeled stress test, not the primary correction; it can flip F3/F4 to INDETERMINATE here. Report stratum tables alongside it. A design-effect/ICC sensitivity is another option, but ICC is undefined for zero-failure families and unstable for these rare events.
- Because this proxy replay has already inspected the same committed responses, any amendment adopting these parameters now is post hoc relative to this proxy and must be labeled as such.

## Residual risk / verification gaps

- `plans/grader_perturb.py` was not present in the lane tree when checked; these counts are a scoped proxy, not official instrument results. I did not reproduce the 16 r8-C records because exact `grade_c` prior-row/rule inputs were not established; final P1 results must include or explicitly exclude them under the frozen rule.
- Two-sided CP with 0 failures needs at least 72 independent successes to pass (all successes: n=71 lower 0.94937; n=72 lower 0.95006). Sparse C / per-cell slices cannot certify the bar and must not be presented as passes.
- Family intervals share records and are not a joint 95% family-wise guarantee; disclose that when interpreting the ten family verdicts.
- Scratch analysis only; no installs, no lane/instrument edits, no verification of a final diff.

VERDICT: Do not treat per-record CP95 as exact under pid clustering; retain the frozen primary only with a pid-block bootstrap and stratum disclosure, noting the worst-case pid sensitivity flips F3/F4 while the record-weighted cluster bootstrap does not. Installs: none.
