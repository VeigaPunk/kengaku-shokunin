# Round-12 probe plan — powered emission-granularity LADDER + transport (design fixed pre-run)

Closes `SCORECARD.md` §Planned (round 11): the novelty axis-move (floor, 6).
One powered, preregistered, prior-art-priced run that turns r11's single
powered pairwise contrast into (a) a **four-point density ladder** with a
confirmatory ordered-trend test, (b) a **batching dissociation** that
decomposes the eight-round-old `A-MONO 0/10` finding, (c) a **second task
family** so the dose is not inventory-ledger-only, and (d) **per-problem
probabilistic forecasts** scored by Brier + skill + calibration slope.

Nothing in this file may be edited after the bundle hash; corrections are
appended as a numbered amendment in `round12-fleet/INTEGRATOR-NOTES.md` and, if
they touch the design, the bundle is re-hashed (v2) with new `ordering.log`
lines. The first endpoint request always postdates the final hash.

## 1. Claims under test

| # | Claim | Instrument | Status before r12 |
|---|---|---|---|
| **C1** | **Ladder monotonicity**: per-problem error severity at the final forced emission increases monotonically as forced-emission density falls across four arms on the *same* problems — `A-INC` (10 checkpoints) → `A-CKPT4710` (3) → `A-CKPT710` (2) → `A-CKPT10` (1) | Page's ordered-trend test on within-problem ranks (n=64 blocks × 4 ordered arms), one confirmatory p | r9: directional only (n=8, tie at pass level); r11: priced the *middle* contrast only (+0.352, p=0.0011). No round has tested the ladder as an ordered whole |
| **C2** | **Within-run repeatability of the r11 dose** (wording constrained by the prior-art ruling: same unit, same problems, same seeds ⇒ repeatability, **not** independent replication): the paired severity diff `A-CKPT710 − A-CKPT4710` at shared checkpoints {7,10} reproduces r11's +0.352 on *identical problems and seeds* | paired t + exact sign test, predicted point value filed pre-request | r11 ESTABLISHED once, on a different run day; never re-measured within a later run |
| **C3** | **Batching dissociation**: r8's `A-MONO 0/10` collapse is driven by *up-front op batching*, not by emission sparsity — a one-checkpoint incremental arm (`A-CKPT10`) should beat `A-MONO` on final-state severity | paired diff `A-MONO − A-CKPT10` on final-state `nwrong` (n=64) | r8 recorded MONO 0/10 vs INC 7/10 vs CKPT4710 1/10 at n=10 and attributed the spread to emission granularity; the two mechanisms were never separated |
| **C4** | **Transport**: the dense-vs-sparse severity dose transports to a structurally different task family (positional token-sequence editing: no integer arithmetic, no key set, order-carrying state) | paired diff `T-SPARSE − T-DENSE` at shared checkpoints {7,10}, n=48 | never tested; every prior severity number is inventory-ledger-only |
| **C5** | **Per-problem forecast skill**: a mechanical predictor (`predict_r12.py`, hashed) fitted on r11's committed per-problem bytes forecasts r12 pass outcomes better than arm-level climatology | Brier over **416** pass events (7 arms × their own n), BSS per event set and pooled, calibration slope/intercept, 5-bin reliability; plus 304 sign events and 7 run-level events (727 scored total) | r11 filed 3 event-level probabilities (Brier 0.153, self-admittedly dominated by one term); the lane's own checklist prefers per-problem probabilities and has never filed them |
| **C6** | **Dose magnitude ordering**: the adjacent severity gaps are ordered by *checkpoint count removed*, i.e. the INC→4710 gap (7 checkpoints removed) and the 710→10 gap (1 removed) are both ≥0 and the ladder's total spread exceeds each adjacent gap | three adjacent paired contrasts at their shared turns, reported with the global test | never measured; r11 measured one adjacent gap |

Every derived claim carries the descriptor sentence verbatim: *single served
unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under the stack pinned in the
run's `descriptors` record (q4_0 KV cache, `--kv-unified`, `--parallel 2`,
custom non-upstream chat template); no cross-model generalization.*

## 2. Design

### 2.1 Family 1 — inventory ledger (verbatim r8/r9/r11 machinery)

- **Problems**: pids **201–264** (n=64), `gen_problem(3000 + pid*41)` —
  byte-identical generator, byte-identical problems and seeds to r11
  (deliberate: makes C2 a repeated-measures *repeatability* test and lets the C5
  predictor use r11 per-problem outcomes as legitimate prior information
  rather than a leak across arms).
- **Arms** (5), all on every problem, run back-to-back within a pid:

| cell | graded turns | requests | ask wording |
|---|---|---:|---|
| `A-INC` | {1..10} | 10 | verbatim r8 `run_inc(proto='INC')`: every ask is `Output the FULL state after applying it.` |
| `A-CKPT4710` | {4,7,10} | 10 | verbatim r11 `ladder()` (acks `Reply 'ok'.`, pre-checkpoint `CHECKPOINT — output the FULL state now.`) |
| `A-CKPT710` | {7,10} | 10 | verbatim r11 `ladder()` |
| `A-CKPT10` | {10} | 10 | verbatim r11 `ladder()` |
| `A-MONO` | single shot (logged turn 1) | 1 | verbatim r8 `run_mono()` — all 10 ops listed up front, FINAL state only |

  The `A-CKPT10` arm is new. It isolates *emission sparsity* (one forced
  emission at the end) from *op batching* (`A-MONO`), which r8 confounded.
  Turn-1 quirk: the opening message always asks for the full state, so every
  CKPT arm logs turn 1 as `-ack` (raw truncated to 80 chars) even though a
  full state was requested — identical to r9/r11 and part of the measured
  construct; comparability is worth more than tidiness.
- **Arm order**: rotated by pid to balance first-order position —
  `order = ARMS[(pid - 201) % 5:] + ARMS[:(pid - 201) % 5]` where
  `ARMS = ["A-INC","A-CKPT4710","A-CKPT710","A-CKPT10","A-MONO"]` (a
  rotation Latin square; every arm occupies every position exactly 12 or 13
  times across the 64 pids, recorded in `descriptors.arm_order_counts`).
- **Filler**: one `Reply with the single word: ready.` request before each
  cell start (r11 deviation 1), i.e. 5 per pid.
- **Request settings**: temp 0.2, max_tokens 8192, system prompt verbatim
  `probe_r12.py:SYSTEM`, model field `"local"`, bare `chat/completions`,
  sequential (no concurrency; the served unit runs `--parallel 2` but the run
  never opens a second slot, so burst state is uniform with r11).

### 2.2 Family 2 — positional token-sequence editing (new machinery, same ladder)

A structurally different state-tracking task: the state is an **ordered list
of tokens**, not a key→integer map. No arithmetic, no key set to track; the
demand is positional (indices shift under insert/delete/move) and
order-carrying.

- **Problems**: pids **401–448** (n=48), `gen_seq_problem(5000 + pid*37)`:
  initial list = 6 tokens sampled without replacement from
  `["alpha","beta","gamma","delta","eps","zeta","kappa","lambda"]`; 10 ops
  sampled with a fixed distribution (see `probe_r12.py:gen_seq_problem`),
  regenerated at `seed+977` (same retry convention as family 1) until the
  op-kind set contains `DEL` and `MOV` and `REV`, and the last 3 ops touch
  ≥2 distinct positions. Pre-hash check proves 48/48 generate and that no
  family-2 `(init,ops)` duplicates another.
- **Ops** (0-based indices, operands always in range by construction):

| op | semantics |
|---|---|
| `APP t` | append token `t` |
| `INS i t` | insert token `t` at index `i` |
| `DEL i` | remove index `i` |
| `SET i t` | replace index `i` with `t` |
| `MOV i j` | remove index `i`, insert that token at index `j` (of the shortened list) |
| `SWP i j` | swap indices `i`,`j` |
| `REV i j` | reverse the inclusive slice `i..j` (requires `i<j`) |

- **Arms** (2): `T-DENSE` graded {4,7,10}; `T-SPARSE` graded {7,10}. Ladder
  wording, filler policy, ack truncation, temp/maxtok/system prompt identical
  to family 1's CKPT arms; only `RULES2` and the state type differ. Order
  counterbalanced by pid parity (even: DENSE first).
- **Output contract**: the FULL token list as a fenced ```json array.
- **Grading**: `got` must be a list; `ok = (got == want)`;
  `nwrong = |len(got) - len(want)| + #{i < min(len) : got[i] != want[i]}`
  (length error counted once per missing/extra token). Non-list or parse
  failure → `ok=False`, `nwrong = len(want)` — the same convention family 1
  uses for non-dict (`grade_state`), so a parse failure is maximally severe
  in both families.

### 2.3 Endpoints and verdict rules (mechanical, no judgement at analysis time)

Shared-turn convention: a paired contrast uses only turns graded in **both**
arms; the per-problem value is the mean `nwrong` over those turns.

| id | endpoint | statistic |
|---|---|---|
| **E1 (primary, C1)** | per-pid final-turn (`turn=10`) `nwrong` across the 4 ordered arms INC ≺ 4710 ≺ 710 ≺ 10 | **Page's trend test** for ordered treatments in randomized blocks, pinned exactly: within each pid rank the 4 arm values ascending (ties → midranks); `L = Σ_j (j+1)·R_j` for arms j=0..3 in dense→sparse order, `R_j` = the sum of that arm's ranks over all blocks; `E_L = n·k(k+1)²/4` (k=4); per-block null variance `coef·S²_block` with `coef = Σ_j j² − (Σ_j j)²/k = 5` at k=4 and `S²_block` the block's midrank sample variance `(1/(k−1))·Σ(r − r̄)²` — at k=4 this is the design critic's `(5/3)·Σ(r − 2.5)²`, the exact conditional variance of a random permutation of that block's midrank multiset; `Var_L = Σ_blocks`; `z = (L − E_L)/sqrt(Var_L)`; two-sided normal p. **Direction is defined as `L > E_L` (equivalently z > 0) = increasing severity with decreasing density** — not prose |
| **E2 (C2)** | per-pid mean `nwrong` at {7,10}, `A-CKPT710 − A-CKPT4710` | paired t (df=n−1), 95% CI, exact sign test, McNemar on final passes |
| **E3 (C6)** | adjacent gaps at shared turns: `4710 − INC` at {4,7,10}; `710 − 4710` at {7,10} (=E2); `10 − 710` at {10} | each: paired mean diff, sd, t, p, exact sign |
| **E4 (C3)** | final-state `nwrong`, `A-MONO − A-CKPT10` | paired t + exact sign + McNemar on passes |
| **E5 (C4)** | per-pid mean `nwrong` at {7,10}, `T-SPARSE − T-DENSE` (n=48) | paired t (df=n−1), 95% CI, exact sign |
| **E6 (C5)** | **three scored event sets**, each reported separately (design critic D6): **416 pass events** (5 family-1 arms × 64 + 2 family-2 arms × 48 — *not* 448; the earlier figure was an L1 arithmetic slip, §9), **304 per-problem sign events** (E3a/E3b/E3c/E4 × 64 + E5 × 48), **7 run-level events** (RL1–RL7 in `predictions-r12.md` §5) — 727 events total | Brier per set + per arm, pooled Brier, BSS against each event's own group climatology (per-arm observed pass rate; per-contrast observed win rate; per-event observed rate for RL), calibration slope + intercept by damped Newton on `logit(p)` (≤50 iters, tol 1e-10; `p` clipped to [1e-6, 1−1e-6] before the logit — critic D5), 5-bin reliability with `pred=n/a obs=n/a n=0` for an empty bin (critic D8). Calibration reported on the 416 pass events (primary) and on all 727 (secondary). **The pooled pass-event BSS is labelled `persistence + arm-rate transport`, never generic forecast skill** |

Verdict rules (applied verbatim by `recompute_r12.py`; the analysis prints the
fired branch as a comment line so the gate can re-check the rule against the
numbers). Branch labels for R2 say **REPEATS**, not REPLICATES: the prior-art
pricing (`round12-fleet/r12-prior-art-ladder.md`, C2) rules that a same-unit,
same-problem, same-seed re-measurement is *within-run repeatability*, not
independent replication — llama.cpp documents that multi-slot output is not
bit-reproducible and r8/r9 already measured batch-level variability on this
stack.

```
R1 ladder (E1):   Page p < 0.05 AND L > E_L (z > 0)  -> LADDER ESTABLISHED
                  Page p >= 0.05 AND all three adjacent diffs (E3) > 0
                                                     -> LADDER DIRECTIONAL
                  otherwise                          -> LADDER NOT SUPPORTED
R2 repeat (E2):   diff > 0 AND p < 0.05 AND sign test direction = +1 (wins > losses)
                                                     -> REPEATS-r11
                  diff > 0 AND p < 0.05 AND sign test direction != +1
                  (includes NEUTRAL, wins == losses; critic D4 pins neutral as
                   disagreement, never as agreement)  -> REPEATS-DOWNGRADED
                  diff > 0 AND p >= 0.05              -> DIRECTIONAL
                  diff <= 0                           -> DOES-NOT-REPEAT
                  |diff - 0.352| <= 0.15              -> additionally POINT-MATCHES-r11
R3 batching (E4): diff(MONO - CKPT10) > 0 AND p < 0.05
                                                     -> DISSOCIATION ESTABLISHED
                  diff > 0 AND p >= 0.05              -> DISSOCIATION DIRECTIONAL
                  diff <= 0                           -> DISSOCIATION FALSIFIED
R4 transport(E5): diff > 0 AND p < 0.05               -> TRANSPORTS
                  diff > 0 AND p >= 0.05              -> TRANSPORT DIRECTIONAL
                  diff <= 0                           -> TRANSPORT NOT SUPPORTED
R5 forecast (E6): BSS(pass events) > 0 AND calibration slope(pass events) in [0.5, 2.0]
                                                     -> FORECAST SKILLED
                  BSS(pass events) > 0                -> FORECAST SKILLED-MISCALIBRATED
                  BSS(pass events) <= 0               -> FORECAST UNSKILLED
                  (R5 is decided on the 416 pass events alone; the sign-event and
                   run-level Briers are reported but never change the branch)
```

**Degenerate-input conventions (critic D9 — pinned so no stored line can ever
be NaN/inf):** `sd(diffs) = 0` → print `t=+0.000`, `p=1.0000`, CI `[+0.000,
+0.000]`, plus a `NOTE degenerate: zero-variance paired diffs` line;
`Var_L = 0` (every block fully tied) → `z=+0.000`, `p=1.0000`; sign test with
wins = losses = 0 → `p=1.0000`, direction NEUTRAL; McNemar with b = c = 0 →
`p=1.0000`. A degenerate case never satisfies a `< 0.05` branch, so every rule
falls through to its non-established branch deterministically.

**Error-record contingency (inside the bundle, per lesson 7):** any
`cell:"error"` record removes that pid from *all* paired statistics of its
family (listwise deletion, which keeps Page's blocks complete and the pairs
balanced); the excluded pids, the resulting n, and the **realized arm-position
counts after deletion** are printed in `analysis_r12.md` (critic: deletion can
unbalance the rotation). Excluded pids' prediction events are dropped from both
the Brier numerator and its climatology, never scored as failures. If family-1
n < **44** or family-2 n < **44** — the filed power floors, derived in
`power_analysis_r12.md` as the smallest n whose Monte-Carlo exact-t power
reaches 0.80 at the r11-observed dz = 0.4288 (n=44 → 0.810; n=42 → 0.791) —
every verdict above is reported as `UNDERPOWERED-INDETERMINATE` regardless of
its p-value, and the run is not re-analyzed with a smaller MDE. A
partial/interrupted run is never analyzed: a re-run writes a fresh
`KENGAKU_R12_OUT` directory and only one complete run is landed.

## 3. Experimental-unit descriptors

The first record of the run pins, at run time: served model id (`/v1/models`),
llama-server pid + full argv (`/proc/<pid>/cmdline`, best effort; failure
recorded, never fatal), temp/maxtok/system prompt, both seed schemes, both pid
lists, arm-order rule + realized position counts, counterbalance rule for
family 2, `sha256` of `probe_r12.py` and `run_r12.py`, `sha256` of the prereg
bundle and of `predict_r12.py`, and the probe lineage string. Expected in argv
from rounds 10–11: `--cache-type-k/v q4_0`, `--kv-unified`, `--parallel 2`,
`--ctx-size 16384`, `--flash-attn on`, `--no-context-shift`, custom
non-upstream chat template `qwen-coder-godspeed.jinja`.

## 4. Run artifacts (schema contract — recompute and gate are built on this)

`results-r12.jsonl` (JSONL, `separators=(',',':')`, append-mode, one run):

| record | count | fields |
|---|---:|---|
| `cell:"descriptors"` | 1 | §3 fields (run start) |
| `cell:"meta"` | 64 | `pid`,`seed`,`init`,`ops`,`truth`,`tail_touched` |
| `cell:"meta2"` | 48 | `pid`,`seed`,`init`,`ops`,`truth`,`features` |
| `cell:"A-INC"` | 640 = 64×10 | `pid`,`turn`,`ok`,`nwrong`,`got`,`want`,`finish`,`usage`,`wall_s`,`raw`,`request_ts` |
| `cell:"A-CKPT4710"` / `"A-CKPT710"` / `"A-CKPT10"` | 192 = 64×3 / 128 = 64×2 / 64 = 64×1 | same graded fields |
| `cell:"A-MONO"` | 64 | same graded fields (`turn`=1; the single shot is the final state) |
| `cell:"A-INC-ack"` | **0** | INC grades every turn, so it emits no ack records by construction |
| `cell:"A-CKPT4710-ack"` / `"A-CKPT710-ack"` / `"A-CKPT10-ack"` | 448 = 64×7 / 512 = 64×8 / 576 = 64×9 | `pid`,`turn`,`raw`(≤80 chars),`finish`,`usage`,`wall_s`,`request_ts` |
| `cell:"T-DENSE"` / `"T-SPARSE"` | 144 = 48×3 / 96 = 48×2 | graded fields, family-2 semantics (`got`/`want` are token lists) |
| `cell:"T-DENSE-ack"` / `"T-SPARSE-ack"` | 336 = 48×7 / 384 = 48×8 | ack fields |
| `cell:"filler"` | 416 = 64×5 + 48×2 | `finish`,`usage`,`wall_s`,`raw`,`request_ts` |
| `cell:"descriptors_end"` | 1 | re-read of `/v1/models` + pid/argv at run end (§8 mid-run-drift mitigation) |
| `cell:"error"` | 0 expected | `job`,`err`,`request_ts` |

**Pinned totals** (the two numbers the gate recomputes; every other figure in
this table is descriptive):

- **records = 4 114** = 2 descriptors + 64 meta + 48 meta2 + 1 328 graded
  (640+192+128+64+64+144+96) + 2 256 ack (448+512+576+336+384) + 416 fillers
  + 0 errors.
- **HTTP calls = 4 002** = 4 000 `chat/completions` + 2 `/v1/models` GETs, where
  chat = family 1 `64×(10+10+10+10+1) + 64×5 fillers = 2 624 + 320 = 2 944`
  plus family 2 `48×(10+10) + 48×2 fillers = 960 + 96 = 1 056`.
  `meta`/`meta2`/`descriptors` records carry no request, hence records ≠ calls.
- Estimated wall time from r11's measured 0.184 s/request: **12–25 min**
  (`A-INC` emits a full state on all 10 turns, so output tokens per request
  exceed r11's mix).

`run.log` (stdout capture): progress `[i/N] ('CELL', pid)` lines, then

```
=== SUMMARY ===
A-INC: <passes>/<n-with-turn-10>
A-CKPT4710: <passes>/<n>
A-CKPT710: <passes>/<n>
A-CKPT10: <passes>/<n>
A-MONO: <passes>/<n>
T-DENSE: <passes>/<n>
T-SPARSE: <passes>/<n>
wall_total_s: <float>
```

(cell lines match `grader.parse_runlog_summary`'s `^(\S+): (\d+)/(\d+)$`).

## 5. Analysis contract (`analysis_r12.md`, written by `recompute_r12.py`)

Every stored line below is gate-pinned (the gate re-derives it from committed
bytes and fails on mismatch):

```
results-r12.jsonl contains 2 descriptors, 64 meta, 48 meta2, G graded, A ack, F fillers, E error records

| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |
|---|---:|---:|---:|            (one row per arm, 7 rows, §4 order)

E1 Page trend: L=<f.1> E_L=<f.1> var_L=<f.3> z=<±f.fff> two-sided p=<f.pppp> direction=<increasing|decreasing|neutral>
E2 paired diff (710 - 4710, {7,10}): <±d.ddd> sd <s.ddd> n=<n>
E2 paired t: t=<±t.ttt>, df=<n-1>, two-sided p=<p.pppp>
E2 95% CI: [<l.lll>, <u.uuu>]
E2 exact sign: wins=<W> losses=<L> ties=<T> two-sided p=<p.pppp> direction=<+1|-1|NEUTRAL>
E2 McNemar final passes: b=<B> c=<C> two-sided p=<p.pppp>
E3 adjacent gaps: 4710-INC {4,7,10} <±d.ddd> p=<p.pppp>; 710-4710 {7,10} <±d.ddd> p=<p.pppp>; 10-710 {10} <±d.ddd> p=<p.pppp>
E4 batching diff (MONO - CKPT10, final): <±d.ddd> sd <s.ddd> n=<n> t=<±t.ttt> p=<p.pppp> sign W/L/T=<W>/<L>/<T>
E5 transport diff (SPARSE - DENSE, {7,10}): <±d.ddd> sd <s.ddd> n=<n> t=<±t.ttt> p=<p.pppp> sign W/L/T=<W>/<L>/<T>
E6 events: pass=<n> sign=<n> runlevel=<n> total=<n> (excluded pids dropped from score and climatology)
E6 Brier pass: pooled=<f.ffff> (N=<n>); per-arm A-INC=<f.ffff> A-CKPT4710=<f.ffff> A-CKPT710=<f.ffff> A-CKPT10=<f.ffff> A-MONO=<f.ffff> T-DENSE=<f.ffff> T-SPARSE=<f.ffff>
E6 Brier sign: pooled=<f.ffff> (N=<n>); per-contrast E3a=<f.ffff> E3b=<f.ffff> E3c=<f.ffff> E4=<f.ffff> E5=<f.ffff>
E6 Brier runlevel: pooled=<f.ffff> (N=7)
E6 BSS pass vs arm climatology: pooled=<±f.ffff> [persistence + arm-rate transport]; family1-replicate=<±f.ffff> (N=<n>); family1-novel=<±f.ffff> (N=<n>); family2=<±f.ffff> (N=<n>)
E6 BSS sign=<±f.ffff> runlevel=<±f.ffff> pooled-all-727=<±f.ffff>
E6 calibration (pass events): slope=<±f.ffff> intercept=<±f.ffff> (damped Newton on logit(p) clipped to [1e-06, 0.999999], <n> events)
E6 calibration (all events): slope=<±f.ffff> intercept=<±f.ffff> (<n> events)
E6 reliability (5 bins, pass events): <lo-hi>: pred=<f.fff|n/a> obs=<f.fff|n/a> n=<int>   (×5)
Finish audit at graded turns: finish=length <L>/<G>, parse fail <P>/<G>
Ack compliance (raw lowercased startswith ok): <cell> <a>/<b> = <c.c>%   (×5: A-CKPT4710-ack, A-CKPT710-ack, A-CKPT10-ack, T-DENSE-ack, T-SPARSE-ack — A-INC has no ack cell by construction)
Excluded pids: family1 <list|none> family2 <list|none>
Realized arm positions after deletion: <arm>:<count per position 1..5> (×5)

VERDICT R1 ladder: <branch text>
VERDICT R2 repeat: <branch text>
VERDICT R3 batching: <branch text>
VERDICT R4 transport: <branch text>
VERDICT R5 forecast: <branch text>
```

plus the point-prediction scoring table
(`| Quantity | Predicted | Observed | Abs error |`, one row per filed point
prediction in `predictions-r12.md` §4 **and one row per arm's predicted pass
count** from §2 of that file), the ordering sentence (bundle hashes,
`ordering.log` times, first `request_ts`), the descriptor sentence from §1, and
a `NOTE degenerate: ...` line whenever a §2.3 degenerate convention fired.

Statistics are stdlib-only: paired t via mean/sd of diffs with the t-CDF from
the incomplete-beta continued fraction already in `grader.py` (`betai`);
exact binomials via `math.comb`; Page's L exactly as pinned in §2.3 E1
(within-block midranks, per-block conditional null variance `5·S²_block` at
k=4, normal approximation for p); logistic recalibration via damped Newton
(max 50 iterations, tol 1e-10, deterministic); Brier/BSS by direct summation.

## 6. Ordering & smoke protocol

1. Write the bundle: this file, `power_analysis_r12.md`,
   `predictions-r12.md` (point + per-problem probabilities, generated by
   `predict_r12.py` from **committed r11 bytes only** — never from any r12
   request), `predict_r12.py`.
2. `prereg-precheck.log`: prove both families generate (64/64, 48/48), no
   duplicate `(init,ops)` within or across families, no family-1 problem
   duplicates an r8/r9/r11 `init+ops` (seeds are r11's by design — the check
   asserts *identity* with r11's metas, not disjointness), arm-order rotation
   realizes the filed position counts.
3. Hash the bundle → `prereg-bundle.sha256` (repo-relative lines,
   `sha256sum -c` from the repo root); `ordering.log` records UTC timestamps
   immediately before and after hashing.
4. Design-critic L2 verdict must land **before** the first endpoint request; a
   fatal defect → amend, re-hash (v2), append new ordering lines. **Round-12
   fact:** the critic (`round12-fleet/r12-critic-design.md`, verdict
   DO-NOT-RUN, 1 FATAL + 5 MAJOR + 4 MINOR) landed while no bundle hash
   existed, so every defect was absorbed *in place* and this file is hashed
   once as v1 — there is no v2 chain. §9 lists each absorbed defect.
5. Hash the run scripts (`probe_r12.py`, `run_r12.py`) + `predict_r12.py`
   post-fix, appended to `ordering.log`; the first `request_ts` must postdate
   the last hash line.
6. Mock smoke: `mock_server_r12.py` on 127.0.0.1:18114 (family-1 + family-2
   content policy, exercises fenced/bare/malformed parse paths); run
   `KENGAKU_R12_N=2 KENGAKU_R12_N2=2 KENGAKU_R12_OUT=/tmp/kengaku-r12-mock`
   and check the record census against §4's ratios. No mock byte is ever
   mixed into the committed results.
7. Real-endpoint smoke: `KENGAKU_R12_N=1 KENGAKU_R12_N2=1
   KENGAKU_R12_OUT=/tmp/kengaku-r12-smoke` — schema check only.
8. Main run into `/tmp/kengaku-r12-main`, then landed **byte-identical** into
   `corpus/evidence/round12-ladder/` with md5 recorded in `LOG.md` (r9/r11
   landing convention; the gate pins it).

## 7. Deviations from r11 (exhaustive)

1. three new family-1 arms (`A-INC`, `A-CKPT10`, `A-MONO`); r11 ran two;
2. `A-INC` ask wording taken from r8 `run_inc(proto='INC')`, not from
   `ladder()`'s CHECKPOINT wording (documented in §2.1);
3. new family 2 (`T-DENSE`/`T-SPARSE`) with new generator, rules, ops,
   grading, `meta2` records;
4. arm order by 5-rotation instead of pid parity (family 1); parity retained
   for family 2;
5. n: family 1 stays 64 (same pids/seeds as r11); family 2 adds 48 new pids;
6. new `descriptors` fields (both seed schemes, arm-order counts, bundle +
   predictor hashes);
7. per-problem probabilistic predictions generated by a committed script from
   r11 bytes (r11 filed 3 hand-written event probabilities);
8. analysis emits 5 verdicts (R1–R5) instead of 1;
9. SUMMARY lists 7 cells instead of 2;
10. a `descriptors_end` record re-reads `/v1/models` + pid/argv at run end
    (mid-run drift detection; r11 pinned the stack only at start);
11. the two families are **interleaved pid-block by pid-block** (family-1 block
    k, then family-2 block k) so a slow host drift cannot align with a family;
    recorded in `descriptors.schedule`;
12. `probe_r12.py`'s round-8 A/B/C `main()` is deleted and replaced by a
    die-guard — importing the machinery module can no longer fire an off-design
    request at the served endpoint (critic D1).

Prompts for the shared arms, turn/ask logic, family-1 grading, JSON parsing,
temp/maxtok/system prompt, filler policy and problem generation are verbatim
r11 (which is verbatim r9 ← r8).

## 8. Threats to validity (priced)

- **Non-iid draw contamination** (r7/llama.cpp #7052): bounded by pairing,
  rotation, one filler before every cell, sequential single-slot use; residual
  type-I inflation possible. The sign test and Page's rank test are the
  distribution-robust companions; both preregistered.
- **Same problems as r11** (family 1): C2 is a repeated-measures *repeatability*
  test on identical problems and seeds,
  not an independent draw; C1/C3/C6 inherit r11's problem sample, so they
  generalize to *this* problem population only. Family 2 is a fresh sample.
- **A-MONO differs on two axes by construction** (batched ops + single
  emission) — that is exactly what C3/E4 decomposes against `A-CKPT10`.
- **Single served unit** under q4_0 KV + custom template: no cross-model
  claims; descriptors pinned in-band.
- **Family-2 severity metric** (positional mismatch + length error) is not the
  same scale as family-1 key mismatch: C4 compares *within* family 2 only;
  cross-family comparison is limited to the effect-size ratio, reported
  descriptively and never as a pooled estimate.
- **Forecast informativeness**: the C5 predictor uses r11 outcomes on the same
  problems, so its skill is *persistence* skill, not cold forecasting; family-2
  forecasts are constant per arm by design (a no-information comparator).
- **Spillover-ask quirk** and 80-char `-ack` truncation: unchanged from r9/r11;
  ack compliance is a lower bound on full-state emission.
- **Run length** (4 000 chat/completions + 2 model GETs = 4 002 HTTP calls, est.
  12–25 min from r11's measured 0.184 s/request; `A-INC` emits a full state on
  all 10 turns so output tokens exceed r11's mix):
  a mid-run host event (server restart, KV/flag change) would silently split
  the sample. Mitigation: `descriptors` pins the stack at start; the runner
  re-reads `/v1/models` at the end and writes a `cell:"descriptors_end"`
  record; a mismatch is a recorded deviation and the run is re-executed rather
  than analyzed.

## 9. Pre-hash amendment log (design critic D1–D10 + L1 arithmetic fix)

Absorbed in place before the first bundle hash, so the hashed v1 already
carries them. Source: `corpus/evidence/round12-fleet/r12-critic-design.md`
(DO-NOT-RUN) and two independent L2 findings on the E6 denominator.

| id | defect | absorbed as |
|---|---|---|
| D1 (FATAL) | the landed runner was still an r11 two-arm copy and `probe_r12.py` kept the r8 A/B/C `main()`, so §2/§4 could not be produced | `run_r12.py` rewritten (5 family-1 arms + 2 family-2 arms, rotation order, interleaved schedule, `descriptors_end`); `probe_r12.py:main()` replaced by a die-guard (§7 deviation 12); precheck + mock census re-run before hashing |
| D2 | Page's `L` is half-integral under ties, so `L=<int>` was unrepresentable | §5 stores `L=<f.1>`, `E_L=<f.1>`, `var_L=<f.3>` |
| D3 | the filed power floors (56/42) were asserted, and 42 is below 80% power at the filed dz | floors **derived** by `power_r12.py` (MC exact-t at dz=0.4288: n=44 → 0.810, n=42 → 0.791) → both floors = **44**; `power_analysis_r12.md` pastes the run output |
| D4 | R2's "sign test agrees" was undefined at wins == losses | neutral sign pinned as DISAGREEMENT → `REPEATS-DOWNGRADED`; §5 stores `direction=<+1\|-1\|NEUTRAL>` |
| D5 | `logit(0)`/`logit(1)` → NaN in the calibration fit | probabilities clipped to [1e-6, 1−1e-6] before the logit, pinned in §2.3 E6 and §5 |
| D6 | one pooled BSS over mixed event classes is not interpretable as skill | three event sets scored and reported separately; BSS split into family1-replicate / family1-novel / family2; pooled pass BSS labelled `persistence + arm-rate transport`; excluded pids dropped from score **and** climatology; realized arm positions after deletion printed |
| D7 | §5 asked for 6 ack-compliance lines; only 5 ack cells can be non-empty | §5 pins **×5** and names them |
| D8 | an empty reliability bin has no defined `obs` | `pred=n/a obs=n/a n=0` pinned |
| D9 | zero-variance diffs / fully tied blocks make t and z undefined | degenerate conventions pinned in §2.3 (`t=+0.000 p=1.0000`, `z=+0.000 p=1.0000`, `NOTE degenerate:` line); no branch can fire on a degenerate input |
| D10 | §8's "~3.7k requests, 12–20 min" disagreed with §4's pinned totals | §8 now quotes §4: 4 000 chat calls / 4 002 HTTP calls, 12–25 min |
| L1-E6 | **E6 denominator was arithmetically wrong**: "448 pass events (5×64 + 2×48)" — 5×64+2×48 = **416** (448 is 7×64, and also the `A-CKPT4710-ack` count, the likely copy/paste origin). Found independently by ScribeDrafts and ExecutorRecompute | 416 everywhere (C5 row, E6 row, §5 `E6 events:` line); total scored events 416+304+7 = **727** |
| L1-C2 | C2 was worded as "replication", which the prior-art scout rules impermissible for a same-unit/same-problem/same-seed re-measurement | C2 reworded to *within-run repeatability*; R2 branch labels renamed `REPEATS-r11` / `REPEATS-DOWNGRADED` / `DOES-NOT-REPEAT`; §8 threat updated |
| L1-tilt | the fitted difficulty slope (c = −5.03) saturates the sigmoid, so arm-mean predicted probability drifted from its base rate (A-MONO 0.372 vs 0.143) | `predict_r12.py` now solves a per-arm mean-preserving logit offset `delta_arm` by bisection (clip inside the target), so each arm's mean p equals its base rate exactly and predicted pass counts = base × n |
