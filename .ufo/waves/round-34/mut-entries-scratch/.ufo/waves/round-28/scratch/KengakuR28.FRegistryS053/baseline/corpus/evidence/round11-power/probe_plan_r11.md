# Round-11 probe plan — powered emission-granularity rerun (design fixed pre-run)

Closes `SCORECARD.md` §Planned (round 10): the novelty axis-move. One powered,
preregistered, prior-art-priced measurement of the construct the lane's
instrument set can see: **emission-granularity dose** on multi-turn state
tracking — dense forced-state checkpoints {4,7,10} vs sparse {7,10} on the
same problems, measuring error *severity* (wrong-key count), not just passes.

## 1. Claim under test

**Granularity–severity dose**: sparser forced-emission checkpoints increase
per-problem error severity (mean wrong keys at shared checkpoints) even where
pass rates tie (r9: passes 2/8 = 2/8, severity 0.875 → 1.375 final-turn).
Primary endpoint: **mean paired difference of per-pid mean `nwrong` at shared
checkpoints {7,10}** (710 − 4710). Power: n=64, MDE d=0.35, 80% power,
two-sided α=0.05 (`power_analysis_r11.md`).

## 2. Design

- **Cells**: `A-CKPT4710` (graded turns {4,7,10}), `A-CKPT710` (graded turns
  {7,10}). No INC/MONO anchors — the paired design is its own control; r9/r8
  anchors stay on the record for the ladder context.
- **Problems**: pids 201–264 (n=64), `gen_problem(3000 + pid*41)` — machinery
  byte-identical to r9 (`probe_r11.py` = `round9-replication/replicate.py`
  copy, only BASE/OUT env-overridable). Seeds disjoint from r8 (700+pid*13,
  pids 1–10) and r9 (2000+pid*29, pids 101–108); pre-run check proves all 64
  generate and none duplicates an r8/r9 `init+ops`.
- **Pairing**: both cells run on the same problem, adjacent in time (all 20
  requests of a pid back-to-back), cell order counterbalanced by pid parity
  (even pid: 4710 first; odd: 710 first). One filler request ("Reply with the
  single word: ready.") before each cell.
- **Turn semantics**: verbatim `run_r9.py` ladder — including the
  post-checkpoint spillover (the turn *after* a checkpoint is asked for the
  FULL state but logged as `-ack`, raw truncated to 80 chars). The quirk is
  part of the measured construct; changing it would confound r9 comparability.
- **Request settings**: temp 0.2, max_tokens 8192, system prompt verbatim
  (`probe_r11.py` SYSTEM), model field "local", bare `chat/completions`.

## 3. Experimental-unit descriptors (§Planned(b) — carried into every claim)

The first record of the run pins the serving stack at run time: served model
id from `/v1/models`, llama-server pid + full argv from `/proc/<pid>/cmdline`
(best effort; failure recorded, never fatal), temp/maxtok/system prompt, seed
scheme, pid list, counterbalance rule. Known from round 10 and expected in
argv: `--cache-type-k/v q4_0` (4-bit KV), `--kv-unified`, `--parallel 2`,
`--ctx-size 16384`, `--flash-attn on`, `--no-context-shift`, custom
non-upstream chat template `qwen-coder-godspeed.jinja`. Every derived claim
cites: *single served unit — Qwen3-Coder-30B-A3B-Instruct UD-IQ2_XXS under
this exact stack; no cross-model generalization.*

## 4. Run artifacts (schema contract — grader and recompute are built on this)

`results-r11.jsonl` (JSONL, `separators=(',',':')`, append-mode):

| record | fields |
|---|---|
| `cell:"descriptors"` (×1) | `request_ts`, `endpoint`, `models_json`, `server`, `temp`, `maxtok`, `system_prompt`, `seed_scheme`, `pids`, `n`, `counterbalance`, `machinery_sha256`, `probe_lineage` |
| `cell:"meta"` (×64) | `pid`, `init`, `ops`, `truth`, `tail_touched` (no `request_ts`) |
| `cell:"A-CKPT4710"` (×192 = 64×3) / `cell:"A-CKPT710"` (×128 = 64×2) | `pid`, `turn`, `ok`, `nwrong`, `got`, `want`, `finish`, `usage`, `wall_s`, `raw`, `request_ts` |
| `cell:"A-CKPT4710-ack"` (×448 = 64×7) / `cell:"A-CKPT710-ack"` (×512 = 64×8) | `pid`, `turn`, `raw` (≤80 chars), `finish`, `usage`, `wall_s`, `request_ts` |
| `cell:"filler"` (×128) | `finish`, `usage`, `wall_s`, `raw`, `request_ts` |
| `cell:"error"` (expected ×0) | `job`, `err` |

Totals: 1473 records, 1409 endpoint requests (1 + 64×22).

`run.log` (stdout capture): progress `[i/128] ('CELL', pid)` lines, then

```
=== SUMMARY ===
A-CKPT4710: <passes>/<n-with-turn-10-record>
A-CKPT710: <passes>/<n-with-turn-10-record>
wall_total_s: <float>
```

(the two cell lines match grader `parse_runlog_summary`'s `^(\S+): (\d+)/(\d+)$`).

## 5. Analysis contract (`analysis_r11.md`, written by `recompute_r11.py` output; stored lines are grader-pinned)

Exact stored formats (regexes the gate re-derives from committed bytes):

```
| Cell | Final passes / 64 | Mean final nwrong | Mean nwrong (all graded) |
|---|---:|---:|---:|
| A-CKPT4710 | X/64 | a.aaa | b.bbb |
| A-CKPT710 | Y/64 | c.ccc | d.ddd |
```

```
results-r11.jsonl contains 1 descriptors, 64 meta, 320 graded, 960 ack, 128 fillers, 0 error records
Paired mean difference (710 − 4710, shared checkpoints {7,10}): +m.mmm sd s.sss n=64
Paired t-test: t=±t.ttt, df=63, two-sided p=p.pppp
95% CI of mean difference: [l.lll, u.uuu]
Exact sign test: wins=W losses=L ties=T two-sided p=p.pppp
McNemar exact test on final passes: b=B c=C two-sided p=p.pppp
Finish audit at graded turns: finish=length L/320, parse fail P/320
Ack compliance (raw lowercased startswith ok): A-CKPT4710 a/b = c.c%; A-CKPT710 d/e = f.f%
PREREGISTERED VERDICT: ESTABLISHED|DIRECTIONAL|FALSIFIED
Brier score (3 probabilistic predictions): 0.bbb
Paired severity diff prediction: +0.350 predicted, ±d.ddd observed, abs error e.eee
```

plus the point-prediction scoring table (`| Quantity | Predicted | Observed | Abs error /64 |`)
and the ordering sentence (bundle hashes, ordering.log times, first `request_ts`).
Stats are stdlib-only: paired t via mean/sd of diffs with t-CDF from an
incomplete-beta continued fraction (df=63); exact binomials via `math.comb`.
Verdict rule: `predictions-r11.md` §Preregistered verdict rule (mechanical,
including the sign-agreement downgrade clause).

## 6. Ordering & smoke protocol

1. Hash the preregistration bundle (`probe_plan_r11.md`,
   `power_analysis_r11.md`, `predictions-r11.md`) → `prereg-bundle.sha256`
   (repo-relative lines, `sha256sum -c` from the repo root); `ordering.log`
   records UTC timestamps immediately before and after hashing.
2. Design-critic L2 verdict must land before the first endpoint request; a
   fatal defect → amend, re-hash (v2), append new ordering lines; the first
   request always postdates the final hash.
3. Real-endpoint smoke: `KENGAKU_R11_N=1 KENGAKU_R11_OUT=/tmp/kengaku-r11-smoke`
   — schema check only, bytes never mixed into the committed results.
4. Main run: `KENGAKU_R11_OUT` under `/tmp`, then landed byte-identical into
   `corpus/evidence/round11-power/` with md5 recorded in LOG (r9 landing
   convention; grader pins it).

## 7. Deviations from r9 (exhaustive)

1. filler before **every** cell start (r9: skipped each cell's global first) → 128 fillers;
2. new `descriptors` record;
3. `request_ts` stamped only when absent (descriptors carries its own);
4. two cells only (no INC/MONO);
5. per-pid counterbalanced cell order (r9: fixed order);
6. n=64, pids 201–264, seeds 3000+pid*41;
7. SUMMARY computed by re-reading the run's own JSONL at the end.

Prompts, turn/ask logic, grading, parsing, temp/maxtok/system prompt, and
problem generation are verbatim r9.

## 8. Threats to validity (priced)

Non-iid draw contamination (r7) — bounded by pairing/counterbalance/fillers,
residual type-I inflation possible, sign-test robustness preregistered; d
shrinkage from n=8 — MDE 0.35 chosen; single served unit under q4_0 KV +
custom template — descriptors pinned, no cross-model claims; spillover-ask
quirk — part of the construct, documented; `-ack` raw truncation (80 chars) —
ack compliance is a lower bound on full-state emission.
