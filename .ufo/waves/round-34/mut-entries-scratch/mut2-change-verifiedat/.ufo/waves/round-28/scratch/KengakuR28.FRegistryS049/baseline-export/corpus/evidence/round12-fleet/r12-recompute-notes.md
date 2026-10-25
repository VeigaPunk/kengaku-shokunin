# r12-recompute-notes — decisions, formulas and §5 ambiguities

Agent: **ExecutorRecompute** (executor, wave 1). Task restatement: draft the
round-12 analysis engine `corpus/evidence/round12-fleet/recompute_r12_draft.py`
(one stdlib-only, offline, deterministic file) which emits every
`probe_plan_r12.md` §5 stored line byte-exactly, applies R1–R5 mechanically,
scores the filed predictions, handles the error-record contingency and
self-tests on synthetic fixtures — plus this note.

Artifact reviewed by L1 before promotion:

    cp corpus/evidence/round12-fleet/recompute_r12_draft.py \
       corpus/evidence/round12-ladder/recompute_r12.py

Draft state at hand-off: `sha256 =
7d76224395716259d65b9e3ec2981a6e8e0c3f6cb30b118a859a5e22f9434d76`,
2722 lines, `python3 …/recompute_r12_draft.py --selftest` → `SELFTEST 127/127
PASS`, exit 0.

**L1 adjudicates every ambiguity below; nothing here redefines the contract.**
Each item states (a) what §5/§2.3 does not pin, (b) the choice implemented,
(c) the alternative(s) and what changes if L1 rules the other way. Decision-
relevant ambiguities are marked **[R1-safe]** when the alternative reading
cannot change any verdict.

---

## 1. Page's ordered-trend test (E1) — formula and tie correction

§2.3 (`probe_plan_r12.md:115`) pins: "within each pid rank the 4 arm values
(ties → midranks), `L = Σ_j j·R̄_j` over arms j=1..4; normal approximation with
the tie-corrected variance; one two-sided p reported with the signed
direction", and §5 line 235 pins the print shape.

**Implemented** (`page_test`, `midranks`):

* Within-block ranks are **1-based midranks** (`midranks()`): equal values share
  the average of the ranks they span, so `[1,1,2,0] → [2.5,2.5,4.0,1.0]`.
  Ties are detected by exact equality on the `nwrong` values.
* The block statistic is `s_i = Σ_j j·r_ij` and
  **`L = Σ_i s_i`** (the sum-of-ranks reading),
  **`E_L = n·k·(k+1)²/4`** (k = 4 → `E_L = 25n`).
* **Tie-corrected variance, derived per block.** Under the null the block's
  rank vector is a uniformly random permutation of its *fixed* midrank
  multiset onto the fixed coefficients `c_j = j`, and the standard
  random-permutation variance identity gives

      Var(Σ_j c_j r_j) = SS_c · SS_r / (k − 1)
      SS_c = Σ_j (j − (k+1)/2)²          (same for every block)
      SS_r = Σ_j (r_j − (k+1)/2)²        (shrinks with ties)

  and `var_L = Σ_i SS_c·SS_r^(i)/(k−1)`. With no ties `SS_r = k(k²−1)/12`, so
  `var_L` reduces **exactly** to the classical `n·k²(k+1)(k²−1)/144`
  (`k=4`: `25n/3`) — asserted in the selftest. Ties shrink the variance;
  `E_L` is unchanged because midranks preserve the block rank sum.
* `z = (L − E_L)/√var_L`; two-sided `p = 2(1−Φ(|z|)) = math.erfc(|z|/√2)`
  (`normal_two_sided_p`, no scipy).
* `direction = increasing` iff `L > E_L` (severity rises as density falls:
  arm order j=1..4 is INC ≺ 4710 ≺ 710 ≺ 10), else `decreasing`.

### Toy hand-computation asserted in the selftest (3 blocks × 4 arms, no ties)

Arm order INC, 4710, 710, 10; ranks 1..4 ascending by severity, so a block with
values `[3,2,1,0]` has ranks `(4,3,2,1)` and contributes
`s = 1·4 + 2·3 + 3·2 + 4·1 = 20`.

| block | values | ranks | s |
|---|---|---:|---:|
| b1 | `[3,2,1,0]` | (4,3,2,1) | 20 |
| b2 | `[0,1,2,3]` | (1,2,3,4) | 30 |
| b3 | `[2,3,1,0]` | (3,4,2,1) | 21 |

`L = 71`, `E_L = n·k(k+1)²/4 = 3·25 = 75`,
`var_L = 3 · (SS_c·SS_r/(k−1)) = 3 · (5·5/3) = 25`,
`z = (71−75)/5 = −0.8`, `p = erfc(0.8/√2) = 0.4237107971667933`,
`direction = decreasing`. All six values are asserted to 1e-12.

Tied toy (2 blocks): `[1,1,2,0] →` midranks `(2.5,2.5,4,1)`, `s = 23.5`,
`SS_r = 4.5`, `var_b = 7.5`; `[0,2,2,2] →` midranks `(1,3,3,3)`, `s = 28`,
`SS_r = 3.0`, `var_b = 5.0` ⇒ `L = 51.5`, `E_L = 50`, `var_L = 12.5`,
`z = 1.5/√12.5 = 0.4242640687`, `direction = increasing`. Asserted separately.

### Ambiguity 1a — sum-of-ranks vs mean-rank scaling **[R1-safe]**

§2.3 writes `R̄_j` (bar = mean rank across blocks) while §5 pins `L=<int>`,
which only fits a sum. The engine prints the **sum** form (`L = 1692`-style
integers, or one decimal when midranks make it a half-integer) and additionally
prints, in the audit section, the mean-rank equivalents
(`Page scaling note: … mean-rank scaling L=… E_L=25.000 var_L=…`) so the gate
can check either reading. `z`, `p` and `direction` are **identical** under both
scalings (`L/n`, `var_L/n²`), so **no verdict can depend on this choice** — the
toy assertions cover both. If L1 prefers the mean-rank print, only the
`E1 Page trend:` L/E_L/var_L literals change. The sibling `page_L` also prints
the sum form (`L = Σ (t+1)·R_j`), so engine and gate agree on this point too.

### Independent corroboration of 1a and 1b (another agent's implementation)

`corpus/evidence/round12-ladder/power_r12.py` (a sibling's power-analysis
generator, sha256 `7816b9638dab31213e08ab397df8226f06c9040f24415c00a340dd1ade200690`,
219 lines at hand-off) contains its **own** `page_L` written from the same §2.3
text. It independently uses the *sum-of-ranks* convention
(`L = Σ (t+1)·R_j`, `E_L = n·k(k+1)²/4`) and a per-block tie-corrected variance
`coef · S²` with `coef = Σj² − (Σj)²/k` and `S²` = the block's midrank sample
variance — algebraically **identical** to this engine's `SS_c·SS_r/(k−1)` at
`k = 4` (`coef ≡ SS_c = 5`). Verified numerically on nine shared cases — both
hand-computed toys, a strict 64-block ladder, four random tie-heavy matrices,
this engine's own 64-block synthetic fixture, and the exhaustive 81-block
`{0,1,2}⁴` matrix — with `L`, `E_L`, `var_L` and `z` equal to < 1e-9 in every
case (`9/9 MATCH`). Reproduce: import both modules and call
`power_r12.page_L(blocks)` / `recompute_r12_draft.page_test(blocks)` on the same
block list. Two independent readings of §2.3 agreeing is the strongest
available evidence that 1a/1b are the intended readings; if L1 must still
adjudicate, this is a tie-breaker *for* the implemented form.

### Ambiguity 1b — tie correction

§2.3/§5 say "tie-corrected" without a formula. The engine uses the
permutation-variance derivation above (exact classical reduction; no tuning
constant). Alternatives seen in the literature (e.g. a `Σ(t³−t)` divisor form)
differ numerically and would change `var_L`, `z` and `p`. The choice is
documented, derived, and asserted against the classical formula; L1 may
substitute another if the gate pins one.

### Ambiguity 1c — blocks with missing arms

A pid enters the E1 blocks only if it has final-turn records in **all four**
ladder arms (listwise). §2.3 does not say; a partial pid cannot be ranked.

---

## 2. Logistic recalibration (E6 calibration) — Newton criterion

§5 line 246 pins the print; §2.3 (`probe_plan_r12.md:266-267`) pins
"logistic recalibration via damped Newton (max 50 iterations, tol 1e-10,
deterministic)". `calibrate()` implements exactly that:

* Model `logit(p̂) = a + b·logit(p)`; covariate `x = logit(p)` with `p` clipped
  to `[1e-6, 1−1e-6]` (`LOGIT_EPS`) so a filed 0 or 1 stays finite.
* **Start `(a, b) = (0, 1)`** — the identity-calibration prior (mild, and it
  makes the converged optimum a locally-attracting fixed point for the
  exactly-calibrated case).
* Each iteration forms the gradient `g = Σ (y − p̂)·(1, x)` and the Hessian
  `H = −Σ p̂(1−p̂)·[[1,x],[x,x²]]`, solves the 2×2 Newton system
  `δ = H⁻¹g`, then **halves the step `λ ∈ {1, ½, ¼, …}` until
  `ℓ(θ+λδ) ≥ ℓ(θ)`** (monotone damping; the log-likelihood is strictly
  concave so this terminates).
* **Convergence criterion: `max(|δ_a|, |δ_b|) < 1e-10` on the *undamped* Newton
  step, evaluated after applying the damped step**, or 50 iterations,
  whichever first. `iters` and `converged` are printed in the audit
  (`Calibration solver: iters=… converged=…`) so a non-converged fit is visible
  rather than silently reported as a number.
* Degenerate inputs return `n/a` with `note ∈ {insufficient variation,
  singular Hessian, non-finite step, no probabilities}` — fewer than 3 events,
  a single outcome class, or zero variance in `logit(p)` (e.g. the constant
  per-arm family-2 forecasts alone). §5 gives no rule for this; printing `n/a`
  is the honest reading and R5 then reports
  `FORECAST UNPOWERED/UNSCORED`-style text only via its own rules (see 4d).
* Determinism: no RNG, fixed iteration order, `math.log1p`/`math.exp` only.
  The selftest asserts byte-identical re-runs and that the fit is exactly
  `slope = 1, intercept = 0` on the exactly-calibrated construction below, and
  `slope < 1` for a deliberately over-confident forecast.

**Exactly-calibrated construction used in the selftest.** For `p_j = 0.1…0.9`
with `n_j = 100` replicates each and `k_j = round(100·p_j)` exact successes,
*both* score equations vanish at `(a,b) = (0,1)`:
`Σ(y−p) = Σ_j (k_j − 100 p_j) = 0` and `Σ x_j(y−p) = 0` with
`x_j = logit(p_j)`. With no separation and a full-rank design the MLE is
unique, so the fitted slope is exactly 1 and the intercept exactly 0 (asserted
to 1e-6).

### Ambiguity 2a — `p` clipping epsilon
1e-6 chosen; any `eps` changes the fitted slope only for forecasts filed at
exactly 0/1. Alternative: drop such events. Flagged, not hidden.

### Ambiguity 2b — `E6 calibration` argument order
§5 line 246 prints `slope=… intercept=…`; the engine prints slope first
(`b`), then intercept (`a`) — matching the literal.

---

## 3. Brier / BSS / reliability

* `Brier` = mean `(p − y)²` over the events **that carry a filed probability**
  (never recomputed post hoc, per the brief): `brier()`.
* `BSS = 1 − BS/BS_clim` where `BS_clim` uses **the run's own per-arm observed
  pass rate** as the constant forecast for each event (`per_arm_clim`), exactly
  as §2.3 (`:120`) describes. Perfect forecast ⇒ `BSS → 1` (asserted);
  climatology ⇒ `0` (asserted); worse-than-climatology ⇒ `< 0` (asserted).
  `BS_ref = 0` (no outcome variation) ⇒ `n/a`.
* Reliability: fixed edges `[0, 0.2, 0.4, 0.6, 0.8, 1.0]`, inclusive lower /
  exclusive upper, **last bin closed**; labels printed `0.0-0.2 … 0.8-1.0`.
  Empty bins still print with `pred=n/a obs=n/a n=0` (five lines always, so the
  `(×5)` in §5 line 247 holds).

### Ambiguity 3a — reliability bin edges and labels **[verdict-safe]**
§5 pins only `<lo-hi>` and `(×5)`. The engine uses quintiles-by-fixed-edge
(`%.1f-%.1f` labels). Alternatives (deciles? `[0,0.2)` glyph style?) would
change the labels only. **No verdict depends on the reliability table.**

### Ambiguity 3b — event set for E6
§2.3 says "448 pass events (5 arms × 64 + 2 arms × 48)" but **that arithmetic
is 320 + 96 = 416** (`probe_plan_r12.md:120`; the same "448" appears at `:24`
as "Brier over 448 pass events (7 arms)" — 448 = 7×64 — and at `:187` as
`A-CKPT4710-ack = 448 = 64×7`, the plausible copy/paste origin). The engine
takes each arm's **final-turn graded record** as its event (one per arm × pid:
`A-MONO`'s logged turn 1 is its final state, §2.1) and prints the true count
`E6 events: 416 final-turn graded events` on the full design — 416, not 448.
**L1 adjudicates** (the engine never prints a fabricated count); the gate should
pin whatever the landed `recompute_r12.py` emits. Independent agreement:
`ScribeDrafts` flagged the identical defect pre-run
(`corpus/evidence/round12-fleet/r12-report-draft.md:266`, sha256 `a9b74aa5…`
at hand-off) and the sibling skeleton's `{{E6_N}}` is left as a fill-in
(`:39`, `:88`) — so nothing on the page depends on 448.

### Ambiguity 3c — are error-excluded pids dropped from E6?
§2.3's contingency says listwise deletion applies to "all paired statistics";
E6's Brier is not a paired statistic. The engine applies family-level listwise
deletion **uniformly** (E6 too) so one pid is never in one endpoint and out of
another. If L1 rules E6 inclusion, N rises by the excluded pids' events
(≤ 7 per excluded pid).

---

## 4. Ambiguities in §5's stored lines (the list for L1)

| # | §5 anchor | Not pinned | Engine's choice | Alternative / blast radius |
|---|---|---|---|---|
| 4a | `:232` arm table col 4 "Mean nwrong (shared turns)" | what "shared turns" means per arm | the graded turns that participate in that arm's **paired contrasts**: E3 gaps + E4 + E5 ⇒ `A-INC [4,7,10]`, `A-CKPT4710 [4,7,10]`, `A-CKPT710 [7,10]`, `A-CKPT10 [10]`, `A-MONO [1]` (its logged turn 1 **is** its final state), `T-DENSE [7,10]`, `T-SPARSE [7,10]`; printed in the audit as `Shared-turn sets used: …` | data-derived intersection with other arms (would add turn 1 for A-INC, since A-MONO grades turn 1) or "turns shared by *all* arms" (= {10} only). Affects column 4 of the 7-row table only — no verdict |
| 4b | `:232` table header/separator | whether a `\|---:\|---:\|---:\|` separator row is present | separator emitted (markdown-correct, r11 precedent) | drop it |
| 4c | `:249` ack compliance `(×6)` | only **five** ack cells can be non-empty, `A-INC-ack` is 0 by construction (`:186`) | six lines in §4 order, the empty cell as `A-INC-ack 0/0 = n/a` | (i) five lines only; (ii) `0/0 = 0.0%`. A numeric-only gate regex must accept `n/a` under the engine's choice |
| 4d | `:244` `E6 Brier: pooled=… (N=<n>)` | what to print when the probability file is missing/partial | `n/a` for unavailable numerics everywhere (uniform convention), `E6 events: <k>/<n> carried a filed probability` in the audit, and **R5 → `UNDERPOWERED-INDETERMINATE`** with the coverage shortfall in its comment | score only the covered events and let R5 fire; or fail hard. Needs `predict_r12.py`'s real schema (see §5) |
| 4e | `:235` `L=<int>` | L is a **half-integer** whenever midranks tie | integral L printed as an integer, otherwise `%.1f` (e.g. `L=67.5`) | print the full float — the gate's regex should be `-?\d+(\.\d+)?` |
| 4f | `:235` `E_L=<float>` / `var_L=<float>` | decimal places | `%.3f` for both (both are exact multiples of 1/3 or 1/12 in practice: `E_L=1600.000`, `var_L=533.333`) | any other precision |
| 4g | `:230` census line | actual vs expected literals | **actual counts from the bytes** (r11 convention), so the line reads `1 descriptors, 64 meta, 48 meta2, 1328 graded, 2256 ack, 416 fillers, E error records` on a complete run | hard-code `1 / 64 / 48`. Note the sibling skeleton expects exactly this literal (`r12-report-draft.md:171` — a moving target; it has moved once already this round) |
| 4h | `:230` "1 descriptors" | `descriptors_end` (`result` schema §4) is a **second** descriptor record | counted out of the census field; an audit line appears only when it is not exactly 1 | fold `descriptors_end` into the count (would print `2 descriptors`) |
| 4i | `:252-256` verdicts | R2's "additionally POINT-MATCHES-r11" (`:138`) — same line or a second line? | **same line**, appended: `REPLICATED; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.066 <= 0.15)`; the rule comment above it states the condition | emit a separate `VERDICT R2 …: POINT-MATCHES-r11` line |
| 4j | §2.3 contingency (`:152-158`) | `n` used for the 56/42 minima; §4's error schema has **no `pid` field** | `n1 = |meta pids| − excluded`, `n2 = |meta2 pids| − excluded`; **plus a conservative guard**: the family's primary paired n (E2, E5) below its minimum also forces `UNDERPOWERED-INDETERMINATE` | looser reading: only the meta-derived n. Family attribution of an error record is inferred from a `pid` field or from the `job` string; unattributable records are printed (`ERROR RECORD UNATTRIBUTED …`), never silently dropped |
| 4k | §5 ordering sentence | which hashes/times | r11's shape: `Ordering proof: prereg-bundle.sha256 (vN) — <file> <sha>, …; ordering.log pre-hash T / post-hash T; first request_ts T.` plus a `Predictions file:` line | — |
| 4l | §5 scoring table | unit of "Abs error" for count predictions | r11's convention: observed shown as `<passes>/<n>` and the error computed on proportions, so a filed `15/64` and a filed bare `15` both compare against the arm's **observed** denominator | pure `|pred − obs|/64` against the preregistered 64 |

*Citation caveat:* `r12-report-draft.md` is another agent's live artifact — it
was edited during this round (its census line moved from 163 to 171), so its
line numbers here are anchored to sha256 `a9b74aa5…`; the quoted strings are
the stable part.

**Deliberately not invented:** `VERDICT R1..R5` branch **texts** are the plan's
own words (LADDER ESTABLISHED / LADDER DIRECTIONAL / LADDER NOT SUPPORTED /
REPLICATED / REPLICATED-DOWNGRADED / DIRECTIONAL / NOT REPLICATED /
DISSOCIATION ESTABLISHED / DISSOCIATION DIRECTIONAL / DISSOCIATION FALSIFIED /
TRANSPORTS / TRANSPORT DIRECTIONAL / TRANSPORT NOT SUPPORTED / FORECAST SKILLED
/ FORECAST SKILLED-MISCALIBRATED / FORECAST UNSKILLED), with
`UNDERPOWERED-INDETERMINATE` overriding all five when the contingency fires
(`:152-158`).

---

## 5. Interfaces this engine consumes (so `predict_r12.py` can match)

The per-problem probability file is **not named or schema'd anywhere** in the
plan (`predict_r12.py` is not in the tree). Resolution order:
`--probs` flag → `KENGAKU_R12_PROBS` → the first of
`probs-r12.jsonl`, `predictions-r12-probs.jsonl`, `predict-r12-probs.jsonl`,
`predict_r12_probs.jsonl`, `probabilities-r12.jsonl`,
`per-problem-probs-r12.jsonl` in `round12-ladder/`, else
`round12-ladder/probs-r12.jsonl`.

Accepted record shapes (`read_probability_file`):

```jsonl
{"pid": 231, "cell": "A-CKPT10", "p": 0.42}          # key also read: prob | p_pass |
                                                      # probability | pred_pass_prob | p_ok
{"pid": 231, "probs": {"A-INC": 0.9, "A-CKPT710": 0.3}}
```

also a whole-file flat JSON map `{"A-INC:231": 0.9, …}` or nested
`{"A-INC": {"231": 0.9}}`, and — as a fallback — a fenced ```jsonl block
embedded inside `predictions-r12.md`. Unmappable records are reported
(`PROB RECORD UNMAPPED …`) rather than dropped. **The filed probabilities are
used as-is for E6; the engine never regenerates them.** If `predict_r12.py`
lands a different schema, either extend `read_probability_file` or rename to
one of the candidates — the E6 lines and R5 depend on the coverage line
`E6 events: k/n`.

`predictions-r12.md` point rows are parsed as markdown table rows whose second
cell is a number (`+0.350`, `15/64`, `**+0.350**`); labels are matched by
substring (mono+batch → E4, sparse/dense/transport → E5, diff/severity/gap →
E2, page/trend/monotonic/ladder → E1 p, passes+arm → final passes). Unmatched
labels render `n/a` and are counted in
`Point-prediction rows parsed: k (m matched …)`.

---

## 6. Reused machinery (provenance)

Stats helpers are ports of `corpus/evidence/round11-power/recompute_r11.py`
(`_betacf` `:134`, `betai` `:170`, `t_two_sided_p` `:183`, `t_crit` `:198`,
`binom_two_sided` `:239`, `mcnemar_exact` `:250`, `extract_json_block` `:103`)
— identical to `grader.py`'s r11 block (`:862-953`). Grading conventions:
family 1 verbatim `grade_state` (non-dict → `(False, len(want))`), family 2
verbatim `grade_seq` semantics (`probe_r12.py:358`).

**Generator loading.** `load_generators()` parses `round12-ladder/probe_r12.py`
with `ast`, executes only its **side-effect-free top level** (function/class/
import nodes plus constant-valued assignments — this skips
`LOGF = open(...)` and `os.makedirs(OUT)`), and prefers its
`gen_problem`/`gen_seq_problem`; the in-file ports are used when the file is
absent or unreadable, and the generator provenance + sha256 are printed in the
audit. The port is **byte-exact**: `--selftest` asserts that this file's
`gen_problem` reproduces `probe_r12.py`'s for all 64 family-1 seeds and this
file's `gen_seq_problem` for all 48 family-2 seeds (when the shipped file is
present; the check is skipped otherwise), and that `grade_seq` agrees on six
got/want shapes. Verified in situ against `probe_r12.py` sha256
`1871697f…`: a full-scale synthetic run reports
`Truth rebuild: family1 64/64 verified (probe_r12.py), family2 48/48 verified
(probe_r12.py)` with **0** `TRUTH MISMATCH` lines.

The family-2 generator only exists because a sibling landed it mid-round; when
this draft was first written `probe_r12.py` was still a stale copy of
`probe_r11.py` (no `gen_seq_problem`), which is why the fallback port exists.

---

## 7. Determinism, offline-ness, and what remains unverified

* No network, no `/proc`, no endpoint, no `/tmp` dependence at analysis time;
  the only filesystem reads are the paths named above plus the two ports.
* No `set`/`dict` iteration reaches the output; all pid/cell/turn traversal is
  sorted; floats use fixed precision. Re-run proof (both commands are verbatim
  reproducible against a fixture built by `fixture_records`):

      # the selftest asserts this internally, on its own fixture:
      PYTHONHASHSEED=1  … recompute_r12_draft.py --results F --out o1 …
      PYTHONHASHSEED=99 … recompute_r12_draft.py --results F --out o99 …
      sha256sum o1 o99   # equal

  Observed on a full-scale synthetic fixture (4116 records, 1328 graded, drive
  script `/tmp/r12-verify/gen.py`, which calls
  `fixture_records(n1=64, n2=48, parse_fail=[(231,"A-INC",5)],
  seq_len_mismatch=(430,"T-DENSE",10), error_pids=[(1,264),(2,448)],
  tamper={(222,"A-CKPT710",10):99})`): `sha256
  c1e49add92b7b682dd88c99093070555ea93fbe0cb7a01d21e6784ba9de23f77` for **both**
  seeds. (The literal moves with any edit to the engine; the *equality* is what
  is asserted inside `--selftest`, so the guarantee does not depend on it.)
* **Still unverified (needs the real run; also listed in the engine's docstring
  REPORT):** every E1–E6 value, the census literals on real bytes, the real
  `predictions-r12.md`/probability-file schema and coverage, the §4 ratio
  checks against `run.log`, the descriptor/registration pins (bundle hashes,
  `ordering.log` times, first `request_ts` order), and anything about the
  served unit. Nothing in this file is a measurement.
* **Self-test scope:** 127 assertions covering the r11 statistical anchors, the
  Page toys (no-tie and tied, both hand-computed above), the paired-t hand
  vector (`+0.25 / sd 0.6454972244 / t 0.7745966692 / p 0.4950253461 /
  CI [−0.7771301284, +1.2771301284]`), Brier by hand and the BSS limit cases,
  the exactly-calibrated slope, family-2 grading conventions, the census
  arithmetic (including a full-scale fixture that reproduces §4's
  `1328 graded, 2256 ack, 416 fillers` from the engine's own counting), the
  contingency branch (both firing at n < minima and **not** firing at
  n1=56/n2=42), every §5 line's format regex and multiplicity, a **mutant-style
  corruption check** (a tampered stored `nwrong` must appear as
  `REGRADE MISMATCH`; a parse failure and a family-2 length-mismatched answer
  must re-grade without a stored-field mismatch), and the parser/loader paths.