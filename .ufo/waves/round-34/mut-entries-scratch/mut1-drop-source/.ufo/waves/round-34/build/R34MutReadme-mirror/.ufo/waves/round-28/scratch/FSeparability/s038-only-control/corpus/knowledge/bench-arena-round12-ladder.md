# Round-12 powered four-point ladder: severity dose ordered, batching dissociated, transport DIRECTIONAL

Source: `corpus/evidence/round12-ladder/` (18 files: run bytes `results-r12.jsonl`
md5 `9dd8aa2b…` / sha256 `ad9c88e7…`, `run.log` md5 `700d1ddd…` / sha256
`36114190…`, generated `analysis_r12.md` md5 `029c3bcd…` / sha256 `1ceebd75…`,
bundle `prereg-bundle.sha256` (9 files, v1) + `ordering.log`, machinery
`probe_r12.py` / `run_r12.py`, predictor `predict_r12.py` + `power_r12.py` +
`precheck_r12.py`, engine `recompute_r12.py`, forecast files
`predictions-r12-perproblem.jsonl` (416 lines) / `predictions-r12-signevents.jsonl`
(304 lines) / `predictions-r12.md`); fleet artifacts
`corpus/evidence/round12-fleet/` (22 files: `r12-prior-art-{ladder,transport}.md`,
`r12-critic-design.md`, `r12-mutation.md`, `r12-report-final.md`,
`r12-review-citations.md`, `INTEGRATOR-NOTES.md`). Run
2026-09-29T01:19:59Z → landed 01:32:44Z, endpoint `127.0.0.1:34113`, **4 114
records / 4 002 HTTP calls / 701.6 s**. Every headline number below is quoted
verbatim from `analysis_r12.md` with its line; §Independent verification then
re-derives all of them from the committed bytes with separate throwaway stdlib
scripts (own midranks, own incomplete-beta tails, own IRLS).

## Design (preregistered and hashed before the first request)

- Construct: **emission-granularity dose as an ORDERED four-point ladder** on
  the same problems, plus a fifth arm that holds emission count fixed, plus a
  second task family. Family 1 (inventory ledger, verbatim r8/r9/r11 machinery):

| cell | graded turns | requests | forced full-state emissions |
|---|---|---:|---:|
| `A-INC` | {1..10} | 10 | 10 |
| `A-CKPT4710` | {4,7,10} | 10 | 3 |
| `A-CKPT710` | {7,10} | 10 | 2 |
| `A-CKPT10` | {10} | 10 | 1 |
| `A-MONO` | single shot (logged turn 1) | 1 | 0 (all 10 ops listed up front) |

- Problems: pids **201–264** (n=64), `gen_problem(3000 + pid*41)` — **byte-identical
  problems and seeds to r11** (deliberate: makes the r11 contrast a repeated-measures
  *repeatability* test, and lets the predictor use r11 per-problem outcomes as
  legitimate prior information).
- `A-CKPT10` is **new in r12**: it isolates *emission sparsity* (one forced
  emission) from *op batching* (`A-MONO`), the two axes r8 confounded
  (`SKILL.md` anti-pattern 16). Arm order is a rotation Latin square
  `ARMS[(pid-201) % 5:] + ARMS[:(pid-201) % 5]`; realized positions after
  deletion are 12/13 or 13/12 per arm (`analysis_r12.md:78-82`,
  `descriptors.arm_order_counts`), one filler before each cell.
- Family 2 (**new machinery, same ladder**): positional token-sequence editing —
  the state is an ordered list of tokens (no arithmetic, no key set); pids
  **401–448** (n=48, fresh), `gen_seq_problem(5000 + pid*37)`; ops
  APP/INS/DEL/SET/MOV/SWP/REV; arms `T-DENSE` {4,7,10} vs `T-SPARSE` {7,10},
  counterbalanced by pid parity; grading is positional mismatch + length error
  (`nwrong`), a different scale from family 1's key mismatch — cross-family
  comparison is limited to the effect-size ratio and never pooled.
- Endpoints and verdict rules were fixed in `probe_plan_r12.md` §2.3 (E1–E6,
  R1–R5), the plan/power/predictions/scripts were sha256-hashed at
  `2026-09-29T01:16:08Z` (`ordering.log`), run scripts hashed the same second,
  and the run launched at `01:19:59Z` — the hash chain strictly precedes the
  first request.
- Power floors are **measured, not asserted**: `power_analysis_r12.md` §2 sets
  family-1 and family-2 floors at **n ≥ 44** after the design critic falsified
  the draft's 56/42 (MC: n=42 → 0.791, n=44 → 0.810; `r12-critic-design.md` D3).
  The error contingency was inside the hashed plan (0 error records fired it,
  `analysis_r12.md:50`).

## Result (verbatim `analysis_r12.md`; per-arm table at `:13-19`)

| Arm | Final passes / n | Mean final nwrong | Mean nwrong (shared turns) |
|---|---:|---:|---:|
| A-INC | 48/64 | 0.297 | 0.276 |
| A-CKPT4710 | 28/64 | 0.812 | 0.714 |
| A-CKPT710 | 21/64 | 1.047 | 1.039 |
| A-CKPT10 | 10/64 | 1.594 | 1.594 |
| A-MONO | 2/64 | 2.250 | 2.250 |
| T-DENSE | 2/48 | 4.583 | 4.438 |
| T-SPARSE | 2/48 | 4.771 | 4.615 |

- **E1 ladder monotonicity (primary, C1)** — `E1 Page trend: L=1773.0 E_L=1600.0
  var_L=335.000 z=+9.452 two-sided p=0.0000 direction=increasing`
  (`:21`). Ordered-trend test on within-pid midranks over
  `A-INC ≺ A-CKPT4710 ≺ A-CKPT710 ≺ A-CKPT10`; the result is scaling-invariant
  (mean-rank scaling gives the identical `z=+9.452`, `:69`).
  **Verdict R1 → `LADDER ESTABLISHED`** (`:53`) — error severity rises
  monotonically as forced full-state emissions are removed.
- **E2 repeatability of the r11 dose (C2)** — `+0.297` (sd `0.754`, n=`64`),
  t=`+3.148`, df=63, p=`0.0025`, 95% CI `[0.108, 0.485]`, exact sign
  24W/7L/33T p=`0.0033` direction=+1 (`:22-25`); McNemar on final passes
  b=12 c=5 p=`0.1435` (`:26`) — the *pass-rate* dose is again not established.
  r11's committed comparator was **+0.352** (sd 0.820, n=64, t=+3.431,
  p=0.0011, CI [+0.147, +0.556], sign 26/7/31 p=0.0013). **Verdict R2 →
  `REPEATS-r11; additionally POINT-MATCHES-r11 (|diff - 0.352| = 0.055 <= 0.15)`**
  (`:55`). Wording lock: same unit, same problems, same seeds ⇒ *within-run
  repeatability*, never "replication" (`SKILL.md` measurement rule 12;
  llama.cpp #7052).
- **E3 adjacent gaps (C6)** — `4710-INC {4,7,10} +0.438 p=0.0000; 710-4710
  {7,10} +0.297 p=0.0025; 10-710 {10} +0.547 p=0.0000` (`:27`); the middle row
  is E2 by construction.
- **E4 batching dissociation (C3)** — `MONO - CKPT10, final: +0.656` (sd
  `1.158`, n=64), t=`+4.535`, p=`0.0000`, sign W/L/T=`34/8/22` (`:28`);
  McNemar b=1 c=9 p=0.0215 (`:87`). **Verdict R3 → `DISSOCIATION
  ESTABLISHED`** (`:57`): with the forced-emission count held at one, batching
  all ten ops up front is worse than presenting them one per turn — r8's
  `A-MONO 0/10` collapse is attributable to **up-front op batching**, not to
  emission sparsity, for the first time. Directional decomposition, not a
  mechanism proof (`A-MONO` still differs on two axes by construction).
- **E5 transport (C4)** — `SPARSE - DENSE, {7,10}: +0.177` (sd `1.069`, n=`48`),
  t=`+1.147`, p=`0.2571`, sign W/L/T=`22/16/10` (`:29`). **Verdict R4 →
  `TRANSPORT DIRECTIONAL`** (`:59`): the dose points the same way on a second,
  structurally different task family — at 48 fresh problems and 0.327 power at
  a halved effect (`power_analysis_r12.md` §4), this is a direction, not a
  transport estimate — and it is a **floor-level** contrast (see caveats).
- **E6 per-problem forecast skill (C5)** — three event sets scored separately
  (`:30`): `pass=416 sign=304 runlevel=7 total=727`. Pooled pass Brier
  **`0.1288` (N=416)** with per-arm `A-INC=0.1959 A-CKPT4710=0.1294
  A-CKPT710=0.1155 A-CKPT10=0.0743 A-MONO=0.0734 T-DENSE=0.2092
  T-SPARSE=0.1220` (`:31`); sign events `0.2469` (N=304), run-level `0.2768`
  (N=7), all 727 `0.1796` (`:32-34`). BSS against each event's own group
  climatology: pooled pass **`+0.0447` [persistence + arm-rate transport]**,
  `family1-replicate=+0.4751 (N=128)`, `family1-novel=+0.0173 (N=192)`,
  `family2=-3.1474 (N=96)`; sign `-0.0106`, run-level `-1.2604`, pooled
  `+0.0049` (`:35-36`). Calibration on the 416 pass events: slope **`+0.8427`**,
  intercept `-0.7511` (`:37`); 5-bin reliability (`:39-43`) is monotone but
  over-predicts the middle bins (0.4–0.6: pred 0.457 vs obs 0.111, n=81).
  **Verdict R5 → `FORECAST SKILLED`** (`:61`), on the mechanical rule
  (BSS>0 ∧ slope ∈ [0.5, 2.0]).
- Audits: `finish=length 0/1328, parse fail 0/1328` (`:44`); `Excluded pids:
  family1 none family2 none` (`:50`); ack compliance (raw lowercased starts with
  `ok`) `A-CKPT4710-ack 212/448 = 47.3%`, `A-CKPT710-ack 324/512 = 63.3%`,
  `A-CKPT10-ack 440/576 = 76.4%`, `T-DENSE-ack 168/336 = 50.0%`,
  `T-SPARSE-ack 264/384 = 68.8%` (`:45-49`) — under checkpoint schedules the
  model still emits unrequested full states on ~1/3 to ~1/2 of ack turns.
- Point predictions (filed pre-request, scored at close, `:93-104`): the two
  largest misses are the two nobody had measured before — `E4 MONO-CKPT10`
  predicted `+0.0437` vs observed `+0.656` (abs err `0.613`) and `E3c 10-710`
  predicted `+0.3281` vs `+0.547` (abs err `0.219`); the r11-anchored row hit
  (`E2/E3b` predicted `+0.3520` vs `+0.297`, abs err `0.055`) and the transport
  row was exact (`+0.1758` vs `+0.177`, abs err `0.001`). Pass LEVELS missed on
  the new arms (`A-MONO` 9.1 → 2/64; both family-2 arms ≈21.8/15.8 → 2/48).

## Novelty pricing (fetched-URL verdicts, `corpus/evidence/round12-fleet/`)

- C1 ladder monotonicity: **INCREMENTAL (low)** — the intermediate-step/instruction
  density dose is published; manipulating **emission checkpoint count** with
  severity magnitude as the response is not (`r12-prior-art-ladder.md` §3).
- C2 within-run repeatability of the r11 dose: **INCREMENTAL** (self-replication
  design class published; the same-problem/same-seed/single-unit instantiation
  and its pre-filed point value are the added parameters).
- C3 batching dissociation: **NOVEL-instrument** with a negative-search
  certificate (24 distinct web queries + 6 arXiv API queries; no named suite or
  fetched paper decomposes a monolithic collapse into up-front op batching vs
  emission sparsity with emission count held at 1). Confidence **medium** —
  no Semantic Scholar sweep and no arXiv full-text index ⇒ absence of
  evidence, not verified absence (`r12-prior-art-ladder.md` §4/§5).
- C4 transport to a second task family: **INCREMENTAL (low)** — the multi-family
  idiom is published (39% average drop, six-task sharding; RULER 13-task length
  study) (`r12-prior-art-transport.md` §3.3). C4 must **not** restate r11's
  `NOVEL-instrument` ruling for the density instrument itself.
- C5 per-problem probabilistic forecasts: **INCREMENTAL (low)** — Brier/BSS/
  calibration slope are borrowed canon; scoring 416 events instead of r11's 3
  does not cross a novelty boundary (`r12-prior-art-transport.md` §4.3).
- C6 dose-magnitude ordering: **INCREMENTAL** (`r12-prior-art-ladder.md` §3).

## Independent verification (round 14, not the run's own scripts)

1. **Census from bytes.** Command: `python3 -` (jsonl tally). Observed: `4 114`
   records = `descriptors 1 + descriptors_end 1 + meta 64 + meta2 48 + graded
   1 328 + filler 416 + ack 2 256`; graded per cell `A-INC 640, A-CKPT4710 192,
   A-CKPT710 128, A-CKPT10 64, A-MONO 64, T-DENSE 144, T-SPARSE 96`. Matches
   `analysis_r12.md:9` and `:86`.
2. **E1 by an independent Page implementation** (fresh midranks, per-block
   `5·S²_block` variance): observed `L=1773.0 E_L=1600.0 var=335.000 z=+9.452`
   — identical to `:21`.
3. **Paired contrasts by an independent t/CI/sign implementation** (own
   incomplete-beta tail and t-crit): E2 `+0.297 sd 0.754 n=64 t=+3.148
   p=0.0025 sign 24/7/33 CI [0.108, 0.485]`; E4 `+0.656 sd 1.158 t=+4.535 sign
   34/8/22`; E5 `+0.177 sd 1.069 t=+1.147 p=0.2571 sign 22/16/10`; E3a `+0.438`;
   E3c `+0.547`. All identical to `:22-29`.
4. **Forecast scoring by an independent IRLS.** Observed pooled pass Brier
   `0.1288` (N=416), the seven per-arm Brier values identical to `:31`, BSS
   `+0.0447` pooled / `-3.1474` family 2, calibration `intercept=-0.7511
   slope=0.8427` (converged in 7 iterations) — identical to `:35-37`.
5. **Audits.** `finish=length 0/1328`, `got` null 0/1328, ack counts
   `212/448, 324/512, 440/576, 168/336, 264/384` — identical to `:44-49`.
6. **Preregistration chain.** `sha256sum` of the 9 bundle members equals
   `prereg-bundle.sha256` line-by-line; `probe_r12.py 1871697f…` and
   `run_r12.py 3beb91ea…` equal the `run-script-hash` lines in `ordering.log`;
   the `landed` lines' md5s equal the bytes on disk (`results-r12.jsonl
   9dd8aa2b…`, `run.log 700d1ddd…`); pre/post-hash and launch times are
   `01:16:08Z` < `01:19:59Z`.
7. **Replay gates.** `python3 corpus/evidence/round12-ladder/recompute_r12.py
   --selftest` → `SELFTEST 165/165 PASS`, exit 0. `python3 grader.py` (repo
   root, hermetic, offline) → `CHECKS n=733 mismatches=0 errata_pinned=1`,
   `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0; the r12
   layer is present and the round-14 landing adds an md5 pin for
   `analysis_r12.md` (four trees replayed: r8/r9/r11/r12).

## Falsifications and drift found in round 14 (both reproducible)

- **F-R12-1 — the landed `analysis_r12.md` is not byte-reproducible on this
  host.** Command: `python3 corpus/evidence/round12-ladder/recompute_r12.py
  --out /tmp/x.md && diff /tmp/x.md corpus/evidence/round12-ladder/analysis_r12.md`.
  Observed: one differing line, `:66` — landed
  `Generator source: /home/vgpnk/projects/…`, regenerated
  `/home/vgpnk/Projects/…`; `ls -ld /home/vgpnk/projects` → *No such file or
  directory*. Every statistic is identical (verification 1–5 above), so the
  divergence is a stale absolute-path token, not a number — but the report's own
  close criterion ("regeneration from committed bytes must be byte-identical")
  is **not met** by the bytes on disk. Fix at landing: normalize the path line
  (or pin the stored hash as path-insensitive).
- **F-R12-2 — the fleet drafts pin hashes the tree no longer satisfies.**
  `r12-report-final.md` §Unresolved and `r12-log-final.md` pin
  `analysis_r12.md` md5 `ddfe60d234cae732143649abe80e1ba8` / sha256 `ef1e69db…`;
  the on-disk file is md5 `029c3bcdcf11209d575734742bf239f6` / sha256
  `1ceebd7568aab4ecba694b983d7f3312c957402c7841b7597d6ed4506b6453e3`
  (mtime 2026-09-29 03:28Z, after the drafts were written; regeneration had run).
  Whatever is landed must pin the **current** bytes — copying the draft hash into
  `LOG.md`/`SCORECARD.md` would publish a hash the tree does not satisfy (the
  same defect class as the r11 `grader.py 1709 vs 1711` erratum).

## Caveats (do not generalize past these)

- **One served unit.** `Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS`, server pid
  **1299**, 41-token argv including `--cache-type-k/v q4_0`, `--kv-unified`,
  `--parallel 2`, custom non-upstream chat template, re-pinned in the run's
  `descriptors` record. No cross-model, cross-quantization or cross-stack
  claim; sub-3-bit IQ2_XXS + q4_0 KV bounds everything.
- **Family 2 landed at a floor.** Both arms are `2/48` — the transport contrast
  compares **two failing arms**, so `TRANSPORT DIRECTIONAL` is a floor-level
  direction, not evidence of a positive transported effect. The same floor
  **falsifies the transported-base-rate null** the predictor used for family 2
  (predicted ≈21.8 and ≈15.8 passes vs observed 2/48 per arm), which is why
  `family2` BSS is `-3.1474`: the pooled `+0.0447` survives only because the
  family-1 replicate events carry it (`+0.4751`).
- **Anchor validity, not power, is E1's risk.** The Page anchor's densest leg
  (INC→4710, `+0.6667`) comes from r8 at **n=10** in a different batch; measured
  Page power is 1.000 at n=44–64 *and* 0.989 at n=48 with the alternative
  halved (`power_analysis_r12.md` §3). Level comparisons across batches are
  still forbidden (`SKILL.md` measurement rule 10) — the anchor is a power input,
  never a predicted level.
- **E2 is repeatability, not replication** (same problems, seeds, unit;
  llama.cpp documents multi-slot draws as not bit-reproducible, issue #7052).
- **E4 is a directional decomposition** of a two-axis arm; it does not prove
  batching is the *only* mechanism in r8's MONO collapse.
- **Calibration slope is descriptive.** 416 pass events clear Van Calster's
  ≥200-non-event side but not reliably the ≥200-event side
  (`power_analysis_r12.md` §5); sign-event Brier `0.2469` is near the 0.25 of a
  constant 0.50 and carries almost no information.
- Standing round-10 caveat: a `grader.py` PASS means the corpus agrees with
  itself, not that the model was good — no check touches the endpoint.

## Reproduce

Run all of these from the repo root:

```
sha256sum -c corpus/evidence/round12-ladder/prereg-bundle.sha256   # 9 files: OK
python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest # SELFTEST 165/165 PASS, exit 0
python3 corpus/evidence/round12-ladder/recompute_r12.py --out /tmp/x.md \
  && diff /tmp/x.md corpus/evidence/round12-ladder/analysis_r12.md  # F-R12-1: line 66 only
python3 grader.py                                                  # CHECKS n=733 mismatches=0, exit 0
```

The independent cross-checks in §Independent verification used throwaway stdlib
scripts (own midranks / incomplete beta / IRLS) so as not to trust the run's own
engine; for a single re-runnable command per stored number, the two gates above
are equivalent and stronger — `recompute_r12.py --out` regenerates every
`analysis_r12.md` §5 line from `results-r12.jsonl`, and `grader.py` re-derives
the r12 tree offline (census, meta/meta2 regeneration, raw re-parse/re-grade of
all 1 328 graded records, both SUMMARY halves, every stored line, R1–R5, the
descriptors pins and the bundle/ordering chain).

## Open gaps

- **Cold forecasting** (the named next move): every r12 forecast is a
  *persistence* predictor on the same problems (or a constant per arm in
  family 2). Fitting on r11's bytes and scoring on **unseen** problems/arms,
  with the persistence baseline pre-registered as the comparator at a filed
  MDE, is unmeasured.
- **Family 2 needs a re-run.** At the halved transported effect, 80% power needs
  n=169 (`power_analysis_r12.md` §4); with both arms at 2/48 the family is
  currently informative only as a negative.
- **Cross-family magnitude** is unmeasured: family-1 key-mismatch and family-2
  positional+length `nwrong` are not the same scale, so only the effect-size
  ratio can be compared, and it is reported descriptively.
- **Landing debt (this entry's own round).** Rounds 12 and 13 sat uncommitted and
  unindexed until round 14 (`git status --porcelain`: `?? round12-ladder/`,
  `?? round12-fleet/`, `?? round13-ack-state/`, `M SKILL.md`, `M grader.py`;
  `LOG.md`'s newest entry was round 11). Until the round-14 landing lands, this
  entry's numbers are repo-durable but not corpus-indexed.