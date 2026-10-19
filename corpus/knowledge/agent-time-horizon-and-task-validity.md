source: S013 — https://arxiv.org/html/2503.14499 — Abstract, §3.1 “Computing time horizon”, §6 “Limitations and future work”; S014 — https://metr.org/time-horizons/ — “Methodological Details”, FAQ “Does ‘time horizon’ mean the length of time that current AI agents can act autonomously?”; S005 — https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ — “Too narrow and too wide tests”, “Contamination”; S006 — https://openai.com/index/separating-signal-from-noise-coding-evaluations/ — opening lede, “Discussion”
verified-at: 2026-10-19
recheck: 2027-01-17 (90d) — re-open S013/S014 and check the human-time definition, stated reliability, task-suite scope, update status and range caveat; re-open S005/S006 and check their audit scope and current task/test-validity evidence before reuse

# Agent time horizon and task validity

## Claim

A METR-style time horizon is the human completion duration associated with a stated predicted success probability on a specified task suite; it is not agent wall-clock runtime or autonomous-action duration. The lane’s r8–r12 planning-horizon instrument asks a different question: how state-emission/checkpoint schedules affect multi-turn state accuracy and error severity. Both concern sustained task performance, but their estimands and units differ. Coding-benchmark scores also depend on task, test and contamination validity, which must be audited separately from the horizon fit.

## Evidence

- S013, Abstract: “the time humans typically take to complete tasks that AI models can complete with 50% success rate” defines its 50%-task-completion horizon.
- S013, §3.1: the fitted logistic curve uses “the geometric mean time of successful human baselines” as task duration; §6 cautions that horizon depends on “a domain, task distribution, and human baseliners’ level of skill and context.”
- S014, “Methodological Details”: the estimate is the duration where “the fitted curve intersects with 50% (or 80%) success probability.”
- S014, FAQ “Does time horizon mean…”: it is “a measure of the difficulty of a task, rather than the time an AI spends to complete the task.”
- S005, “Too narrow and too wide tests”: the audited sample is stated as “an audit of 138 SWE-bench Verified problems”; OpenAI reports “at least 59.4% of the audited problems have flawed test cases that reject functionally correct submissions.”
- S005, “Contamination”: OpenAI reports “all frontier models we tested were able to reproduce the original, human-written bug fix used as the ground-truth reference.”
- S006, opening lede/“Discussion”: OpenAI says “we estimate that ~30% of SWE-bench Pro tasks are broken” and “we retract our earlier recommendation to adopt SWE-Bench Pro.”

## What this does not establish

- The METR curve is not a claim about all intellectual labor, every software task, or a model’s runtime; the cited suites and baselines bound the estimate.
- The OpenAI posts do not establish that every SWE-bench task is invalid or that their audit rates generalize to other benchmarks; they report selected audits, not independent replication.
- Falsifier: the metric claim fails if the source’s fitted duration is shown to use agent elapsed time rather than human completion time; the task-validity warning would not transfer if independent, blinded re-audits of the cited task releases found no material prompt/test mismatches or evidence of solution exposure.

## Attribution

S013 is a METR-authored study and S014 is METR’s data page, which states it is no longer actively updated; these are METR’s measurements and methodological disclosures, not independent replications. S005 and S006 are OpenAI posts auditing its own evaluations and reporting its own decision; they are lab self-reports, not independent replication.

## Extends

Extends the README coverage-map row “Multi-turn state tracking / planning horizon” and its r8–r12 evidence, without changing that local claim. Round 8 Probe A asks “is the gap scaffold or horizon?” and contrasts state-every-turn, checkpoint and final-state-only cells (r8 §Design, Probe A); round 11 names an “emission-granularity dose” (r11 §Design); round 12 tests an “emission-granularity dose as an ORDERED four-point ladder” (r12 §Design). These interventions measure state-emission/checkpoint effects on lane task errors—not human task duration at a success probability. This adds the external METR measure and coding-task validity checks without conflating the instruments.

## How kengaku applies it

| Situation | Do | Don’t |
|---|---|---|
| METR-style horizon | State the task suite, human-time baseline and target success probability; report agent wall-clock separately | Call agent runtime or a count of turns the human-duration horizon |
| Multi-turn lane result | Keep r8–r12 checkpoint/emission effects as local state-tracking evidence | Convert the local planning-horizon measure into human hours or a METR capability claim |
| Coding benchmark score | Audit a representative task/test sample and contamination risk; attribute lab audits to their authors | Treat passing tests as uncontested capability evidence or generalize one audit rate to all tasks |

## Rejected

- **SWE-bench Verified/Pro is an uncontested capability meter.** Rejected: S005 and S006 report task/test and contamination issues, and S006 retracts the recommendation to adopt Pro. Flip: independent, blinded audits of the current release find no material validity defects and clean held-out results track capability on the intended construct.
- **The r8–r12 planning-horizon instrument measures METR time horizon.** Rejected: checkpoint/emission schedules are not human-time baselines. Flip: a new lane study directly times expert completion, fits success against human task duration, and reports a stated reliability threshold.

## Corrections (round 24 post-review, 2026-10-19)

Appended after the orchestrator's non-author spot-check; the lines above stay as
landed in `94da19e`. Re-opened S005 today.

- §Evidence S005: "at least 59.4% of the audited problems have flawed test cases
  that reject functionally correct submissions" is in the post's **opening
  summary, item 1 "Tests reject correct solutions"**, not in "Too narrow and too
  wide tests". That section's own sentence is "We found that 59.4% of the 138
  problems contained material issues in test design and/or problem
  description" (the receipt in `corpus/evidence/round24-sources/gate.md`).
- §Evidence S005 "Contamination": "all frontier models we tested were able to
  reproduce the original, human-written bug fix …" is in the **opening summary,
  item 2 "Training on solutions"**; the "Contamination" section carries the
  red-teaming method and examples.
