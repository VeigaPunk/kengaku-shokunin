ATTACKS: C1 one-vs-rest specificity definition (attrib_calibration.py:443-445) and its PASS verdicts for never-predicted legs (r21-ds specificity:opencode-go/hyper 20/20 PASS; r22 specificity:opencode-go 20/20 PASS; r23 specificity:opencode-go 30/30 PASS; r21-ds specificity:hyper 20/20 PASS).

# Findings

F1 — For a never-predicted leg, specificity is the exact complement of the already-reported share estimate.
`neg = GT!=L; k = pred!=L among neg`. If `share:L = 0` then k=n identically for any predictions. It is not merely "no evidence" — it is the same evidence restated, so the PASS adds zero information over `share:L 0/n`.
Evidence: `plans/attrib_calibration.py:443-445`; summary `corpus/evidence/round25-calibration/attrib-calibration-summary.txt:9,31,44` (share 0/20, 0/30 beside the PASSes).

F2 — Vacuous-PASS mutation 1: a never-selected scorer key manufactures a PASS from nothing.
I copied `attrib-r22-opencode-trials.log` to /tmp, added `"ghost": 0.1` to every `scores={...}` dict, re-ran `python3 plans/attrib_calibration.py --root /tmp/k25w2-CritSpecificity/rootA --summary`:
`specificity:ghost 20/20 point=1.000000 cp95=[0.831567,1.000000] interval=PASS`, `recall:ghost 0/0 UNTESTED`, `share:ghost 0/20`. Any roster key that never wins argmax auto-earns a PASS; `legs` is built from `set(roster)` at `attrib_calibration.py:438`.

F3 — Vacuous-PASS mutation 2: the PASS survives total classifier failure.
Same receipt, all 20 predictions flipped to the wrong leg, `correct` cells set NO: `accuracy 0/20 interval=FAIL`, `recall:* FAIL`, `specificity:alibaba-token-plan/hyper 0/10 FAIL` — but `specificity:opencode-go 20/20 PASS` unchanged. A 0%-accurate instrument still banks a specificity PASS for the never-selected leg.

F4 — Verdict asymmetry against the receipts' own honesty rule.
r22 block prints `per-leg GT counts mean honesty note: legs with 0 GT trials are UNTESTED by this run` and stored `TARGET opencode-go 0/0 -> FAIL` (re-verdicts UNTESTED, Amendment 1 item 5). Same trials: `recall:opencode-go UNTESTED`, `target:opencode-go UNTESTED`, `specificity:opencode-go PASS`, `share:opencode-go rg95=[0,1] unidentified`. A leg declared untested earns a PASS in the same output.

F5 — Inflation of the claimed headline count.
TOTAL `PASS=12` decomposes as 4 accuracy + 2 recall + 6 specificity. Of the 6 specificity PASSes, **5 are legs never predicted** (share 0): opencode-go in all three scored blocks, hyper in r21-ds and r21-glm — only r23 `specificity:alibaba-token-plan` 24/24 is substantive (leg predicted 6/30). SCORECARD.md:667 and `corpus/knowledge/attribution-interval-calibration.md:38-44` quote PASS=12 without the vacuity flag; the entry's caveat (:89-90) covers non-simultaneity, not non-selection tautology.

F6 — Harmless downstream: rg95 for these legs is [0,1] because `se_lo+sp_lo<=1` short-circuits (`attrib_calibration.py:180-181`), so the vacuous PASS never propagates into share bounds.

# Verdict impact

The interval math is correct; CP on a 1.0 point estimate is honest. The defect is verdict semantics: "PASS" for a non-selection tautology contradicts the instrument's own UNTESTED honesty convention and pads the headline PASS count (12 -> 7 substantive). Knowledge entry is candid about RG non-identification but silent on the tautology. Fixable; the novelty construct itself survives.

Smallest safe correction: in `block_estimates`, legs with predicted share 0 emit `specificity` with interval `-`/non-verdict (like shares) or a `non-firing` tag; footnote PASS=12 in the knowledge entry/SCORECARD row as 5 non-selection tautologies.

VERDICT: PARTIAL — specificity statistic is standard and correctly intervalled, but 5/12 claimed PASSes are share-0 tautologies that PASS even under 0% accuracy or a fabricated roster leg; PASS=12 and the knowledge/SCORECARD citations are inflated, not broken.

Installs: none (system python3 only; pacman paused, nothing needed).
