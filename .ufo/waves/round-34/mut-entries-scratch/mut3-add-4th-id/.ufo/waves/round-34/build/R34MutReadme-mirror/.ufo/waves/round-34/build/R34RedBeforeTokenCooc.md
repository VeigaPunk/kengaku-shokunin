# R34RedBeforeTokenCooc — token-co-occurrence false-green receipt

Assignment: calibrate the naive token-co-occurrence class only. Axis: C2 calibration.

Created `.ufo/waves/round-34/falsify/red-before/token-cooc.txt`. It records a sandbox string containing `a44b5a8` and `ae95fe0` in unrelated sentences, with 638 characters between token starts. The embedded `near()`-style width-300 probe reports `found`; the fixture explicitly makes no erratum-relation claim. Thus token co-presence/proximity alone produces a false green.

Exact evidence (command and output) is retained in `token-cooc.txt`; its probe output is `found` and `distance 638`. The round-31 source examined was `.ufo/waves/round-31/falsify/R31FxC2Survivors.md` (lines 1–10 identify the report and scope; lines 38–57 enumerate separate route outcomes). No claim is made that this receipt executes the round-34 harness or that any other round-34 acceptance criterion is complete.

Files changed: `.ufo/waves/round-34/falsify/red-before/token-cooc.txt`; this report. No tools installed. Risk: the deliberately naive probe demonstrates token co-occurrence failure only; it does not validate the production counter's implementation.

VERDICT: red-before-token-cooc false-green-proven
