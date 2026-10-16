# Godspeed eval findings (iteration 2)

Source: `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` (read 2026-09-28; dated 2026-04-09). ~125 agents, 21 experiments, 8 domains, 3×2 factorial (model × prompt regime).

**Source availability annotation (round-13 re-dispatch, additive only — numbers above remain "as published in note", not re-verified):**

```
source-status: historical-unavailable
original-source: ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md (read 2026-09-28; note dated 2026-04-09)
availability-evidence: corpus/evidence/round13-coverage/surface-receipt.json observed 2026-10-15T04:49:50Z — ~/Projects/webzites/repos/llm-wiki root absent (exact-path scope)
retained-evidence: baseline 3f31e54 digest of this entry sha256=f381fbe4fcea9d0a7087ad223ccb37f9430ba71604c8f97c2a113c8146193bd9; the published numbers are a historical transcription; no original note bytes retained in-corpus
recheck: test -e ~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md && echo present || echo absent
```

## Falsifiable findings (numbers as published in note)

- **K2 clean split**: 0/3 control found log-target transform on skewed regression; 3/3 godspeed found it. RMSE 135,367 → 117,791 (~13% lift). Opus-UT control missed it; Sonnet godspeed found it — not a capability gap.
- **Variant multiplier**: control produced 1 design; godspeed produced 4–9× non-dominated variants (rate limiter 4–9, bug fix 5–6, LRU 4, BFT 5–8, type systems 6–7). Model-independent.
- **T2 review gradient**: findings 7 (Sonnet-C) → 9 (Sonnet-G) → 13 (Sonnet-UT-G) → 17 (Opus-UT-C) → 19 (Opus-UT-G). Three independent additive levers: model, thinking budget, convergence suppression.
- **Calibration asymmetry**: framer under-predicted control breadth (predicted 5–7 axes, actual 19) and under-predicted godspeed divergence on convergent tasks (predicted 2–4 variants, actual 6).
- **Cost**: tool calls ~1.5×, wall-clock ~1.5× convergent / ~2× divergent, correctness errors 0→0.
- **Negative result**: ultrathink alone does not replicate K2 — deeper convergent path ≠ off-path.
- **Complementarity**: control produces implementation-ready artifacts (named protocols: Helios, HZBC, HYDRA, AURORA; type systems DLST, VERI-LANG, ΛDSL); godspeed produces frontier surveys and meta-results (impossibility theorem for full inference on combined Presburger+unification system).

## Opinion (marked)

The 6× median variant multiplier is the single most reusable headline
number; the K2 split is the single most decisive binary evidence. When
only one datum survives to a report, prefer K2 — binary splits resist
effect-size disputes better than medians.
