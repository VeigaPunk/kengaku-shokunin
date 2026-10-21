# Lessons — round 13 (ack-label prompt-intent audit)

Source: `.ufo/reports/round-13/kengaku.md` (plan only);
`corpus/evidence/round13-ack-state/{audit_ack_schedule.py,analyze_ack_state.py}`;
reconstruction and independent re-derivation in
`corpus/evidence/round14-fleet/r14-revenger-r13.md`.

1. **A logged suffix is a storage label, not prompt intent.** `-ack` rows were
   emitted for every non-checkpoint turn, including initial-state and
   post-checkpoint spillover turns whose prompts asked for full state. Intent
   must be derived from `run_r11.py:76-80` / `run_r9.py:26-28`, never inferred
   from the cell name.
2. **The schedule determines the denominator.** For checkpoint set $C$, a true
   ack-only turn satisfies `t >= 2`, `t not in C`, and `t-1 not in C`. That
   gives 384 = 64×6 rows for r11 `A-CKPT710` and 256 = 64×4 for
   `A-CKPT4710`. The intent-aware rates are 330/384 = 85.9% prefix `ok` and
   324/384 = 84.4% bare `ok`, versus the misleading label-wide 330/512 =
   64.5%.
3. **Capped captures yield bounds, not failures.** Ack raw text is clipped at
   80 characters (`run_r11.py:74`). Thirty of 384 true ack-only rows hit that
   cap; exact unsolicited states are therefore bounded at [18,48]/384 =
   [0.047,0.125]. Keep capped rows UNRESOLVED.
4. **State fidelity and response-contract compliance are separate axes.** Of
   384 true ack-only replies, 18 were unsolicited state snapshots exactly
   equal to simulator truth. They preserve state but violate `Reply 'ok'`.
5. **Instrument-only work scores nothing until its output lands.** Both scripts
   selftest and reproduce from committed r9/r11 bytes, but round 13 landed no
   durable analysis, prior-art review, connector ruling, LOG/SCORECARD row, or
   results-bearing report. Round 14 records those G1–G6 gaps rather than
   upgrading novelty from an incomplete claim package.
