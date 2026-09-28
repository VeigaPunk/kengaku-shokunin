# bench-arena round-6 — flip-set stability probe (n=3 per task)

Third executed eval by this domain (2026-09-28). Question: of the 8 tasks that
flipped v2→r5 (see `bench-arena-round5-battery.md`), which flips are
sampling noise vs pipeline-determined? Method: n=3 fresh generations per task
on the same endpoint/settings as r5 — direct `POST /v1/chat/completions` to
`127.0.0.1:34113` (Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS), temp 0.2,
max_tokens 4096, `enable_thinking:false`, no system prompt, graded by repo
`grade.sh` (BENCH_ROOT=/tmp/bench-r6). Probe set = all 8 flip tasks + 3
controls (01 stable PASS, 02 stable FAIL, 33 stable sha-identical FAIL).
Ex-ante predictions: `/tmp/bench-r6/predictions.md` (written before first
request).

## Status matrix (v2 × r5 × r6 reps)

| Task | v2 (opencode) | r5 (API) | r6 rep1–3 (API) | Verdict |
|---|---|---|---|---|
| 01-reverse-words | PASS | PASS | P P P | stable PASS (sha identical ×3) |
| 02-parse-log-line | FAIL | FAIL | F F F | stable FAIL |
| 03-extract-isodatetimes | PASS | FAIL | F F F | **scaffold-determined** (direct-API now 5/5 FAIL incl. r4; PASS only via opencode) |
| 06-balanced-html-regex | FAIL | HARNESS_DEFECT | HD F F | strategy-bound failure family (see below) |
| 08-sql-group-window | FAIL | PASS | P P P | **scaffold-determined** |
| 09-sql-top-n-per-group | PASS | FAIL | P P P | sampling noise |
| 12-knapsack-reconstruct | FAIL | PASS | P P P | **scaffold-determined** |
| 13-stack-min | FAIL→P | FAIL | F F F | **scaffold-determined** |
| 20-csv-group-sum | PASS | FAIL | P P P | sampling noise |
| 31-mutable-default-arg | FAIL | PASS | P P P | **scaffold-determined** (sha identical ×3) |
| 33-metaclass-shadowing | FAIL | FAIL | F F F | stable FAIL (sha identical ×3, same as v2/r5) |

## Verdict

**5/8 flips scaffold-determined, 2/8 sampling noise, 1 strategy-bound.**
Ex-ante predicted ≥5/8 non-unanimous (noise); observed 2/8. The dominant
mechanism behind a one-shot status flip between harnesses is the *scaffold*
(opencode loop + system prompt vs bare API), not temperature sampling —
even at temp 0.2 where convergent tasks already collapse to canonical
solutions. Every scaffold-determined flip was unanimous across r6 reps.

**Consequence for battery claims**: a single-run status on a scaffold-
sensitive task is a *pipeline verdict*, not a model verdict. Reporting
"model X fails 13" needs "under direct-API scaffold" appended. The two
cleanly noisy tasks (09, 20) both live on SQL/data transforms — the class
with the largest legitimate solution space in this battery.

## Status stability ≠ solution stability

`status×rep` unanimity does not imply identical output:

- Identical sha ×3: 01, 13, 31, 33 (13 identical-wrong ×3 — a second
  deterministic-FAIL case alongside 33).
- Identical status, different sha each rep: 02, 03, 08, 09, 12, 20, 06.
- 08 emitted two different shas among 3 PASSes — equivalent SQL, different
  text. Sha-identity at temp 0.2 is reserved for the smallest output spaces.

## Task 06 — strategy-bound truncation, not budget-bound

r6 evidence kills the "raise max_tokens" hypothesis from r5:

- rep1: `finish=length` at exactly 4096 tok (29.2 s) — same signature as r5.
- reps 2–3: `finish=stop` at 46/45 tok (~0.3 s) — emitted a compact regex
  (`<(?!\/?\1>)` non-backref trick); both FAIL.
- 06hi (max_tokens 8192): `finish=length` again at 8192 tok, 65.5 s — the
  literal-expansion strategy (`<tag>…|…`) is exponential in nesting depth;
  doubling budget doubled the wall-clock, not the outcome.

**Rule: `finish=length` that recurs at a doubled cap is strategy-bounded.**
The model oscillates between two failure modes (exponential expansion →
truncation; compact lookaround trick → wrong regex). No token budget fixes a
strategy that is exponential in depth. Classify 06 as a capability gap with
a bimodal failure distribution.

## Canary refresh (cross-pipeline × repetition)

| Verdict | Tasks |
|---|---|
| Deterministic PASS (status+sha stable) | 01 |
| Deterministic FAIL, identical sha | 33; add 13 (identical-wrong sha ×3 in r6, though sha differs across pipelines) |
| Stable FAIL, varying sha | 02 (capability gap, fresh wrong answer each gen) |
| Scaffold-determined | 03 (API=FAIL), 08 (API=PASS), 12 (API=PASS), 31 (API=PASS) |
| Sampling noise | 09, 20 |
| Strategy-bound bimodal | 06 |
| Semantically broken + hidden-contract hang | 27 (see `bench-arena-task27-timeout-anatomy.md`) |

## Prediction-calibration delta

- Direction correct (stability is classifiable; controls held), magnitude
  wrong: predicted ≥5/8 noisy, observed 2/8. Underestimated scaffold
  dominance — consistent with r5 finding that byte-identical solutions
  *were* the minority; should have inferred that the complement is
  scaffold-reactive.
- New prior: at temp 0.2, expect scaffold effects to dominate sampling
  effects for open-ended tasks; expect sampling to dominate only where the
  solution space is wide but shallow (SQL shape variants).

## Reproduce

```
# /tmp/bench-r6/run.py: PROBE=[11 tasks], REPS=3, same body as run.py in r5
BENCH_ROOT=/tmp/bench-r6 bash ~/bench-arena/grade.sh kq-r6-rep{1,2,3}
```

Artifacts (ephemeral): `/tmp/bench-r6/{run.py,run27_06.py,predictions.md,
telemetry-kq-r6.csv,out/,graded/,report-kq-r6-rep*.v2.csv,t27/}`.
