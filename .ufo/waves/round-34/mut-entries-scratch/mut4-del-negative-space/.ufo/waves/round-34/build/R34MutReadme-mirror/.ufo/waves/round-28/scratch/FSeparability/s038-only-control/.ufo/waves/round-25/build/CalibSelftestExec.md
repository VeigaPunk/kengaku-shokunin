# Kengaku round 25 — C1 calibration selftest fixtures

Axis: novelty (legacy label) → canonical coverage; this move adds interval-calibration failure fixtures. No C2/calibration assertions were changed.

## Files written
Private clone branch `r25-CalibSelftestExec`, base observed as `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a` (clone/switch command output: cloned, switched branch, printed that SHA). No lane-tree/Git-index mutation and no commit.
- `plans/fixtures/r25/attrib-cal/gt-flip.log:2-29` — one GT cell differs from the retained 20/20 PASS summary; row-derived k=19.
- `plans/fixtures/r25/attrib-cal/duplicate-block.log:2-50` — identical 16-row blocks, so frozen duplicate rule yields n=16 once.
- `plans/fixtures/r25/attrib-cal/n16-all-correct.log:2-25`; `n17-all-correct.log:2-26`; `n0-untested.log:2-9`; `upper-below-bar.log:2-26` — four interval-decision cases.
- `plans/fixtures/r25/attrib-cal/EXPECTED.tsv:1-7` — hand-derived verdicts and interval formulae.
- `plans/fixtures/r25/attrib-cal/selftest_snippet.py:1-62` — standalone function-body suggestion using `parse_receipt`, `clopper_pearson`, and `verdict`.

## Expected interval output (95% CP, bar 0.80)
```
fixture                 n   k   interval                                      verdict
gt-flip.log             20  19  [BetaInv(.025;19,2), BetaInv(.975;20,1)]     INDETERMINATE
duplicate-block.log     16  16  [0.025^(1/16)=.7941, 1]                       INDETERMINATE
n16-all-correct.log     16  16  [0.025^(1/16)=.7941, 1]                       INDETERMINATE
n17-all-correct.log     17  17  [0.025^(1/17)=.8049, 1]                       PASS
n0-untested.log          0   0  no interval                                    UNTESTED
upper-below-bar.log     17   0  [0, 1-0.025^(1/17)=.1951]                      FAIL
```

## Evidence / limits
- Frozen rules and dedup identity: `plans/round-25-claims.md:28-45` (last score block; duplicate tables count once; CP verdicts; n=16/17 threshold).
- Receipt syntax copied from `corpus/evidence/attrib-r23-stream.log:194-234`; source rendering comes from `plans/attrib_probe.py:994-1000,1008-1014`.
- The TSV values use the registered zero-error formula directly; 19/20 is bounded by the stated exact beta quantiles, with lower < .80 < upper.
- `--selftest` was not run, per the wave instruction to skip tests/builds. L1 should wire the snippet and run its own post-integration gate. The snippet checks dedup semantics locally because the shared interface does not expose a production aggregation function.
- LSP was unavailable (no LSP tool mounted); no existing-symbol refactor was needed. No network/source fetches and no installs.

Installs: none.
VERDICT: All six requested synthetic cases, expected verdicts, and an integration-ready selftest body are prepared in the private clone; runtime verification remains with L1.
