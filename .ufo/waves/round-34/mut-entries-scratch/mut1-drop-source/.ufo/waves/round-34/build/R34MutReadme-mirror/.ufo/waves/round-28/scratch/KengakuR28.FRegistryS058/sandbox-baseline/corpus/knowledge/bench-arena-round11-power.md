# Round-11 powered rerun: emission-granularity severity dose ESTABLISHED

Source: `corpus/evidence/round11-power/` (run bytes `results-r11.jsonl` md5
`c42fe3d1…`, `run.log` md5 `281cb530…`, generated `analysis_r11.md`,
preregistration bundle `prereg-bundle.sha256` + `ordering.log`); fleet
artifacts `corpus/evidence/round11-fleet/`. Run 2026-09-28, endpoint
`127.0.0.1:34113`.

## Design (preregistered before the first request)

- Construct: **emission-granularity dose** — dense forced-state checkpoints
  (`A-CKPT4710`, graded turns {4,7,10}) vs sparse (`A-CKPT710`, {7,10}) on
  the SAME 64 problems (pids 201–264, seeds `3000+pid*41`), paired per pid,
  cell order counterbalanced by pid parity, filler before each cell. Ladder
  turn semantics verbatim from r9 (`run_r9.py`), machinery verbatim
  (`probe_r11.py` = `replicate.py` copy, env-overridable BASE/OUT only).
- Primary endpoint: mean paired difference of per-pid mean `nwrong` at shared
  checkpoints {7,10} (710 − 4710). Power: filed analysis from the committed
  r9 bytes (d=0.519 from 8 pairs, shrunk to MDE d=0.35 → n=64, two-sided
  α=0.05, ≈80% power — exact 0.7996, critic MINOR adjudicated).
- Preregistration: bundle (plan+power+predictions) sha256-hashed at
  `23:10:20Z`; run scripts hashed post-fix at `23:28:37Z`; first request
  `23:28:57Z`. Verdict rule mechanical and exclusive (ESTABLISHED /
  DIRECTIONAL / FALSIFIED + sign-agreement downgrade).
- Experimental-unit descriptors pinned at run time (first jsonl record):
  served model `Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, llama-server
  pid 1299, 41-token argv (`--cache-type-k/v q4_0`, `--kv-unified`,
  `--parallel 2`, `--ctx-size 16384`, custom jinja template). Single served
  unit — no cross-model or cross-stack generalization.

## Result

| Cell | Final passes / 64 | Mean final nwrong | Mean nwrong (all graded) |
|---|---:|---:|---:|
| A-CKPT4710 | 29/64 | 0.750 | 0.693 |
| A-CKPT710 | 21/64 | 1.078 | 1.062 |

- **Paired severity diff +0.352** (sd 0.820, n=64); t=+3.431, df=63,
  two-sided **p=0.0011**; 95% CI [+0.147, +0.556]; exact sign test 26W/7L/31T
  p=0.0013 (direction agrees). **PREREGISTERED VERDICT: ESTABLISHED** —
  sparser checkpoints increase error severity on identical problems.
- Pass-rate dose NOT established: McNemar b=13 c=5, exact p=0.0963. The 8/64
  pass gap favors dense checkpoints directionally but is not significant;
  r9's "tie at 2/8=2/8" was underpowered, not equality.
- Clean run: 0 error records, finish=length 0/320, parse fails 0/320, census
  exactly as planned (1473 records / 1409 requests / 259 s).
- Ack compliance (raw starts with "ok"): 4710 220/448 = 49.1%, 710 330/512 =
  64.5% — under checkpoint schedules the model emits unrequested full states
  on a large fraction of ack turns (r9: 57%/75%); the spillover ask after
  each checkpoint (r9-verbatim quirk) inflates this by design.

## Calibration outcomes

- Severity-diff point prediction **+0.350 → observed +0.352 (abs err 0.002)**:
  shrinking the n=8 effect (d 0.52→0.35 planning MDE) landed almost exactly.
- Pass-count predictions missed high-side: 15/64 predicted vs 29/64 observed
  (err 0.219), 13 vs 21 (err 0.125) — absolute pass LEVELS are batch-variable
  (r8 CKPT 1/10, r9 2/8+2/8, r11 29/64+21/64 on the same unchanged stack —
  pid 1299 identical), while the r11 paired contrast reproduced the r9
  direction on fresh problems and reached the preregistered power. Claim
  levels only within-batch; claim paired contrasts only within this stack.
- First probabilistic predictions scored: Brier 0.153 over 3 events
  (0.78→1, 0.50→1, 0.60→1); the 0.25 term from the honest 0.50 on
  significance dominates — underconfidence on the primary endpoint was the
  calibration cost.

## Novelty pricing (fetched-URL prior art, `round11-fleet/r11-prior-art-*.md`)

- C1 severity-only dose response to checkpoint density: **INCREMENTAL (low)**
  — the pass/severity decoupling is published (StageIF arXiv 2609.08589;
  2605.30233 last-token aggregation), but no source was FOUND (search set:
  ~45 queries, 50 fetched sources) that manipulates emission DENSITY with
  severity magnitude as the response.
- C2 ladder INC > CKPT > MONO: KNOWN (CKPT>MONO half), INCREMENTAL
  (CKPT<INC half) — unchanged from r9, additional support fetched.
- C3 instrument (density ablation on identical problems+seeds, severity graded
  apart from passes): **NOVEL-instrument** — ScoutGranularity's verdict over
  its search set (r9's gap ruling stands, strengthened); no named public suite
  found performing this ablation, 2026 newcomers are
  position/localization/taxonomy-based.
- C4 instrument (hashed preregistration + power + hermetic replay gate on a
  local served model): INCREMENTAL — agent-experiment preregistration is
  published (2606.11217 template incl. checkpoint-hash + quantization
  disclosure; 2603.10044 executed at scale with OSF DOI + 80%-power
  analysis); no found instance of the hermetic replay gate half.
- Method context (M1–M3): paired inference/power canon = Miller arXiv
  2411.00640; n=64 sits in the CLT-under-coverage zone (Bowyer 2503.01747) →
  exact sign test kept as robustness; llama.cpp #7052 closed-stale, class
  still unfixed, no batch-invariance equivalent of vLLM/SGLang fixes; as
  method context from fetched prior art (not an r11 measurement), q4_0 KV is
  reported to perturb outputs (PR #21038 PPL/KLD tables) — common-mode across
  the two paired cells, so the paired diff is defensible while absolute
  `nwrong` levels are not stack-transferable.

## Reproduce

`python3 grader.py` (repo root) → exit 0, 280 checks: replays the r11 tree
offline (meta regeneration, raw re-parse/re-grade, census, SUMMARY, every
analysis_r11.md stored line, verdict-rule consistency, bundle hash chain,
ordering). `python3 corpus/evidence/round11-power/recompute_r11.py
--selftest` → 58 checks green; regenerating `analysis_r11.md` from the
committed jsonl reproduces the pinned bytes.
