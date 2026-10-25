# round-24 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-24.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `e21f9ea98`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/kengaku-review.md` and `kengaku-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | `llm-judge-calibration.md` — reviewer re-fetched 17 of 20 web rows (sha256 match; S005/S006/S023 dynamic); agree | W3ReviewKengaku | agree |
| reject | S003 rejection — agree; S023 rejection — agree on status, disagree on its reason (a non-sequitur): converted into superseding row S026 and QUALITY criteria Q9/Q10 (M21/M22) in `e21f9ea` | W3ReviewKengaku | agree |

## Adjudication

ADMITTED after post-review fixes `e21f9ea` (21 recheck cells normalized and logged; S002/S005/S012 location slips and the S009 range corrected; S026 supersedes S023; spot-check disagreements became Q9/Q10). Orchestrator ruling on the lane's L0: C2 is a calibration move under AXES ('SHONEN.md/SCORECARD entries match observed repo state') — r23 recorded NOT-ADMITTED and 6 SCORECARD-vs-repo disagreements closed; a held score is admissible when the declared observable moved. Per-axis: coverage improved (5 sourced entries; index gaps closed; 16 map rows + 5 Frontier rows; score held 7), calibration improved (score held 8), novelty/depth/freshness/operability/adjacency unchanged; capability `sources-registry` (26 rows, census ok). Trends: expansion improved, quality unchanged, discernment improved (the disagreement became grounded criteria). Grader 733/733 PASS at base and head.
