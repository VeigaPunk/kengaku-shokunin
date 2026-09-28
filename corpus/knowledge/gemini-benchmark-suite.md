# Gemini × godspeed benchmark suite (digest)

Source: `llm-wiki/wiki/ai/agents-and-engineering/gemini-3.1-pro-godspeed-benchmarks.md`
+ `gemini-3.1-pro-godspeed-test-battery.md` (read 2026-09-28; audit gap:
pages were cited in SKILL.md round 1 but never digested into corpus).

## The four-signal suite

Each task pairs a **control expectation** (vanilla model) with a
**godspeed expectation** (directive) — the delta is the measurement, not
the absolute score:

1. **Off-path reframing** ("K2 equivalents") — tasks with an obvious
   convergent path that is structurally wrong:
   - Algorithmic trap: nested-array bottleneck → control micro-optimizes;
     godspeed reframes to spatial index / trie / Bloom filter.
   - Metric trap: "maximize accuracy" on imbalanced data → control gets
     99% via majority-class; godspeed names the trap, moves to
     PR-AUC/F1 + SMOTE/focal loss unprompted.
   - Design pattern: the prompt must *invite* the wrong axis. A task
     where the obvious path is actually right produces no signal.
2. **Variant multiplication** — frontier surveys vs single artifacts:
   - CRDT-vs-OT state sync: godspeed = 4–7 non-dominated variants with
     explicit trade-off axes (convergence/memory/partition tolerance).
   - Multi-tenancy: godspeed = crossover map of shared-pool ↔
     schema-per-tenant ↔ dedicated-instance inflection points.
3. **Discovery widening with precision parity** — more findings, no
   hallucination penalty:
   - Lock-free queue audit: control 2–3 races; godspeed 5+ incl.
     hardware reordering and false sharing.
   - AMM/flash-loan audit: control reentrancy/overflow; godspeed
     multi-block multi-actor oracle manipulation.
   - Scoring counts *validated* findings only (anti-pattern 7 in
     SKILL.md).
4. **Calibration asymmetry** (meta-test) — the framer predicts variant
   counts, bug types, execution time for both conditions *before*
   running; the delta quantifies how wrong the researcher's own model
   of the model is.

## Design rules extracted

- Every signal needs a **control expectation stated in advance** —
  otherwise the godspeed delta is unmeasurable.
- Trap tasks must be genuinely solvable on the wrong axis (accuracy on
  imbalanced data is; a broken task is just ambiguous).
- "Precision parity" is the anti-cheat: breadth gains that buy
  hallucinated findings are rejected by the judging schema, not by
  inspection.
- Calibration prediction is a first-class artifact, not a nicety —
  it is itself measured.
