# Eval-design digest 3 — scaling retrospective + ReAct paper

Third wiki digest (2026-09-28). Closes the WikiSweeper findings: the last two
un-excluded files under `wiki/ai/` plus the strongest residual paper note.

Sources read in full 2026-09-28:

- `wiki/ai/scaling-and-forecasting/scaling-hypothesis-revisited.md` (Gwern
  retrospective, compiled 2026-04-06)
- `wiki/ai/agents-and-engineering/papers/react-reasoning-acting.md`
  (ReAct paper note, compiled 2026-04-08)

## Scaling retrospective — eval-relevant extractions

1. **Construct-validity gap, quantified by history**: GPT-3 was called
   "disappointing" on benchmark numbers while crossing qualitative
   thresholds (few-shot, code-gen) that the measured benchmarks didn't
   cover — the note's lesson (L30–34): domain-specific benchmarks miss
   emergent capabilities. Matches `eval-theory-notes.md`'s diversity-
   blindness pattern: the metric set lags the capability surface.
2. **Contamination ≡ p-hacking** (L120): "benchmark contamination and
   p-hacking share the same root: researchers optimize for the measured
   variable." Same Goodhart mechanism named in SKILL anti-pattern 1 — cite
   this as the general version of the SWE-bench retirement example.
3. **Ex-ante prediction discipline is a named methodology** (L24, L112):
   the note frames itself as a Tetlock-style scored prediction review —
   "write the prediction down, return with the score." Corpus's
   predictions-before-runs rule (SKILL checklist #1/#4) is this exact
   discipline; the note is the citation for why.
4. **Obsolescence rate** (L38): "2015 papers now seem Stone Age" —
   AI-specific half-life. Operational rule: re-baseline catalog/index
   entries per generation; a 30-day-old verdict (like v2) may already
   describe a different artifact (confirmed empirically this round by
   skills-catalog drift).
5. **Deployment gap ≠ capability gap** (L59–62, L85–87): inner-monologue /
   CoT remain underdeployed despite demonstrated gains; organizational
   friction binds short-horizon forecasts. For battery work: don't infer
   capability absence from deployment absence.
6. **Parameter count misleading for capability** (L72): Chinchilla ≈20
   tok/param — use compute/data when comparing model families, not raw
   params. Reinforces `local-model-index` caution when comparing families.

## ReAct paper note — eval-protocol extractions

1. **3-annotation protocol** (L97): ALFWorld ReAct used 3 trajectories per
   task type with sparse commonsense thoughts — minimal exemplar budget
   vs 10³–10⁵ baseline demonstrations. Transferable: few-shot harness
   fairness = compare prompting-vs-training on *equal information* axes.
2. **Failure-mode table is the correct report shape** (L56–63): the note
   reports CoT vs ReAct by *failure class* (hallucination 56%→0%, reasoning
   loops 16%→47%, search derail 23%), not just accuracy. Same pattern as
   bench-arena's status×sha×finish decomposition — per-failure-class
   reporting beats aggregate rate.
3. **Composition beats selection** (L69–89): ReAct↔CoT-SC hybrid hits
   35.1 EM / 64.6 Fever, better than either alone; each branch covers the
   other's failure mode. Eval corollary: when two scaffolds produce
   near-disjoint win-sets (v2 19 vs qlocal 21, near-disjoint per-task wins
   in `local-bench-arena.md`), composition/routing is the design lever.
4. **Reasoning loops as a named failure class** (L60, 47%): repetition of
   the same thought-action pair. bench-arena has no trace-level loop
   metric — future harnesses scoring multi-step tasks should add
   thought-pair dedup counting.
5. **Finetune inversion** (L120): finetuned ReAct 8B > all 62B prompting;
   finetuned 62B > all 540B prompting. Prompt-method rankings don't
   extrapolate across training regimes — don't cite few-shot orderings for
   finetuned models.

## Net corpus delta

- New citable eval-theory material: construct-validity gap, Goodhart root
  cause, Tetlock scoring discipline, failure-class reporting, composition
  rule. These slot into SKILL's eval-theory rules and anti-patterns as
  grounded citations, not new hypotheses.
- Wiki `ai/` sweep is now complete: all 6 subdirs either digested
  (agents-and-engineering, foundations, books, alignment-and-training,
  scaling-and-forecasting) or verified empty of eval signal
  (adoption-and-diffusion — 0 hits, out of scope).
