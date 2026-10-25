# Q1–Q8 prediction-honesty review

Axes: calibration (direct); novelty (no additional credit from forecast scores).

## Counterexample / assessment

- **Ex ante, but not blind.** The frozen preregistration says predictions preceded this instrument's output, while also explicitly deriving them from `grader.py` and known round-26 strata, including MULTI=31 (`plans/round-27-claims.md:85-89`). This supports temporal ex-ante status, not a claim that the author lacked outcome-relevant information. The 1964-record population, grader, stored verdicts and format audit were already available (`corpus/knowledge/grader-perturbation-audit.md:24-36,56-60`). The predictions are code-informed forecasts over a known finite corpus, not fresh-sample forecasts.
- **Q1 is highly exposed to prior knowledge, but MULTI=31 alone does not logically force it.** MULTI means more than one matching fence (`plans/grader_perturb.py:54-62`); count alone says nothing about whether first/last parsed values differ or yield different grades. However, the already-published audit says all 31 are R8 B responses with operation-8/9/10 states, and the nearby last-fence perturbation flips all 17 baseline-PASS records (`corpus/knowledge/grader-perturbation-audit.md:89-93`; prior summary `corpus/evidence/round26-calibration/grader-perturb-final.txt:3`). Since Q1 asks only for one first-fence disagreement, this makes it unusually predictable from known corpus structure. The 17 flips concern penultimate-vs-last, not a direct first-vs-last test; they do **not** by themselves prove Q1. The exact Q1 event remains a deterministic replay of records the author already possessed.
- **Brier is permissible only as descriptive bookkeeping, not a calibration result.** Q1–Q8 are eight binary predicates over the same fixed 1964 records and overlapping policy outcomes (`plans/round-27-claims.md:91-100`), not eight independent forecast trials. Prior audit documents repeated inputs/clustering and rejects iid generalization (`corpus/knowledge/grader-perturbation-audit.md:78-81,105-107`). A Brier number can faithfully score the frozen probabilities against the eventual corpus predicates, but cannot establish calibrated forecasting or earn calibration-axis credit here. The preregistration already says no such credit is taken (`plans/round-27-claims.md:87-89`).

## Smallest safe correction

Keep the frozen events and probabilities unchanged. At close, report each Q's probability and outcome plus the Brier score only if labeled **descriptive, code-informed, finite-corpus; not blind, independent, or evidence of calibration**. State explicitly that MULTI=31 and its known R8 B composition informed Q1, while not claiming the count alone entails the event. Do not convert the score into calibration credit.

## Verdict

No post-hoc rewrite of Q1–Q8 is warranted. Report Brier only with the caveat above; otherwise it risks overstating calibration evidence.

VERDICT: Ex ante in timing but informed by the known corpus; Brier is descriptive-only, and Q1 is highly predictable but not implied by MULTI=31 alone.

Installs: none.