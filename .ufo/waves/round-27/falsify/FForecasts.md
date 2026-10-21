# FForecasts — Q1–Q8 scoring

Seat: `KengakuR27.FForecasts`; reviewer identity is not candidate writer `KengakuR27`.
Observed scratch-clone base (`git rev-parse HEAD`, `/tmp/kengaku-r27-FForecasts`):
`b5f62e5e637b34a1549e3475fc58b4227ed87e5a`.
Entry reread: the complete 110-line draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md`
(including the full source header); its writer field is `KengakuR27` at line 4. Proposed canonical path is
`corpus/knowledge/extraction-policy-comparison.md`; this was a draft reread, not an admission.

## Evidence and scoring

- Ex-ante source: `git show 11a7fc8c64dc5d634331be24ccf5936f84a11f03:plans/round-27-claims.md`
  contains the Q1–Q8 events and p values at lines 91–100. `corpus/lessons/round-27.md:3–4` records
  this commit before build dispatch.
- On the frozen scratch clone, `python3 plans/parser_policy_compare.py --json >
  /tmp/kengaku-r27-FForecasts/policy-forecast.json` exited 0. The exact parsed output excerpt is
  `/tmp/kengaku-r27-FForecasts/forecast-score-inputs.txt:1–20` (derived from that JSON); the retained
  summary and independent oracle also exit 0 and agree on policy counts:
  `corpus/evidence/round27-calibration/policy-build-summary.txt:1–10,74–76`,
  `corpus/evidence/round27-calibration/policy-build-oracle.txt:1–12`.
- Scores use the committed event definitions (`plans/round-27-claims.md:91–100`) and binary Brier loss
  `(p-y)^2`. Q5 uses the raw cell counts/rates (not rounded summary tokens); Q7 excludes E4.

| Event | p | y | Full-precision outcome evidence | Brier |
|---|---:|---:|---|---:|
| Q1 | 0.85 | 1 | E1: 17/1964 disagreements (`forecast-score-inputs.txt:2`) | 0.0225 |
| Q2 | 0.70 | 1 | E4: 952/1964 agrees = 0.4847250509164969 (<0.5; line 5) | 0.0900 |
| Q3 | 0.60 | 1 | E2: 0/1964 disagreements (line 3) | 0.1600 |
| Q4 | 0.40 | 0 | E7 and E3 each disagree on 17/1964; not strictly more (lines 4,8) | 0.1600 |
| Q5 | 0.50 | 1 | B-clean-hint: E0 6/8=0.75; E1/E3/E7 0/8=0; shift 75 pp. E2/E6/E8 max shift 0 pp (lines 10–19). Thus ≥10 pp without rounding. | 0.2500 |
| Q6 | 0.70 | 1 | E6: 0/1964 disagreements (line 7) | 0.0900 |
| Q7 | 0.45 | 0 | Excluding E4: max 1021/1964=0.519857433808554; min 995/1964=0.5066191446028513; difference 26/1964 ≈ 1.3238289205702648 pp (<2; lines 1,6,9). | 0.2025 |
| Q8 | 0.55 | 1 | E5 has 26 PASS→FAIL flips (line 6) | 0.2025 |

Mean Brier = `(0.0225+0.09+0.16+0.16+0.25+0.09+0.2025+0.2025)/8`
`= 1.1775/8 = 0.1471875`.

## Timing and calibration caveat

Amendment 1 is explicitly post-output: `plans/round-27-claims.md:155–158` discloses returned build
outputs and an L1 count sanity check before it. It clarifies policy semantics and says Q5 uses unrounded
rates (`:160–172`); the ex-ante Q1–Q8 p/event table at the frozen commit remains unchanged. The scored
values above are therefore the original forecasts against the disclosed, clarified policy contract, not
post-hoc replacement probabilities. The timing audit reports the parser instrument absent from the
registration commit, while noting deleted/off-tree manual outputs cannot be absolutely excluded:
`.ufo/waves/round-27/build/RevPredictionsTiming.md:12–13,30`.

This Brier is descriptive bookkeeping, not a calibration result or calibration-axis credit: the forecasts
are explicitly code-derivable and claim no score credit (`plans/round-27-claims.md:85–89`), Amendment 1
calls Brier descriptive only (`:171–172`), and the CP95 is nominal finite-population—not a future-response
guarantee (`:50–56`).

## Residual risk and verification gaps

The stated `/build/ExecStateCheckV4.md` was located under `.ufo/waves/round-27/build/` and read; it covers
P4, not these forecast events. Q1–Q8 were independently recomputed here from the pinned instrument JSON;
no claim is made about broader calibration or P4 correctness. No tools were installed or updated.

VERDICT: Q1–Q8 score `y=(1,1,1,0,1,1,0,1)`, mean Brier `0.1471875`; no actionable scoring defect found in this scoped review.