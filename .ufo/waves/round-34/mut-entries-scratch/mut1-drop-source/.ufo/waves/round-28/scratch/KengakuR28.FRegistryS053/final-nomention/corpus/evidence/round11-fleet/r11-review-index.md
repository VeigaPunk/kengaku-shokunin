# Round-11 landing-integrity review index

Review commands were run against the working tree; no corpus evidence, LOG, SCORECARD, README, or PROVINCE file was edited. The only allowed endpoint requests were `GET /v1/models` and `GET /health`.

## 1. Bidirectional corpus index

| Index | Disk | README rows | Result |
|---|---:|---:|---|
| `corpus/knowledge/` | 22 | 22 (`grep -c '^| \`knowledge/' corpus/README.md`) | MATCH; both sorted set differences empty |
| `corpus/lessons/` | 13 | 12 (`grep -c '^| \`lessons/' corpus/README.md`) | **MISMATCH**: `round-8-aggregator-box3-coldrun.md` has no README row |
| `corpus/evidence/*/` | 6 | 6 | MATCH; every disk directory and README row resolves |

The evidence directories checked were round8-horizon, round9-replication, round9-fleet, round10-fleet, round11-power, and round11-fleet. The lessons mismatch is a non-blocking index defect.

## 2. New-entry source and number audit

Both new entries carry a source on their first non-heading line: `bench-arena-round11-power.md` names both round11-power and round11-fleet; `lessons/round-11.md` names LOG.md plus both evidence directories. Spot audit (commands: `grep -n` against `analysis_r11.md`, `power_analysis_r11.md`, `probe_plan_r11.md`, `INTEGRATOR-NOTES.md`, and the named prior-art artifacts) follows:

| Entry number | Source line/artifact | Verdict |
|---|---|---|
| 29/64 and 21/64 final passes | `analysis_r11.md` Observed-results table | MATCH |
| 0.750, 1.078, 0.693, 1.062 | `analysis_r11.md` Observed-results table | MATCH |
| +0.352, sd 0.820, n=64 | `analysis_r11.md` primary endpoint | MATCH |
| t=+3.431, df=63, p=0.0011 | `analysis_r11.md` primary endpoint | MATCH |
| CI [+0.147,+0.556] | `analysis_r11.md` primary endpoint | MATCH |
| sign 26/7/31, p=0.0013 | `analysis_r11.md` primary endpoint | MATCH |
| McNemar b=13, c=5, p=0.0963 | `analysis_r11.md` secondary tests | MATCH |
| finish 0/320, parse 0/320 | `analysis_r11.md` secondary tests | MATCH |
| ack 220/448=49.1%, 330/512=64.5% | `analysis_r11.md` secondary tests | MATCH |
| 1473 records / 1409 requests / 259 s | `analysis_r11.md` census plus `INTEGRATOR-NOTES.md` landing record | MATCH (259.1 s rounded) |
| predicted 15/64, 13/64; errors 0.219, 0.125 | `analysis_r11.md` prediction table | MATCH |
| +0.350→+0.352, absolute error 0.002 | `analysis_r11.md` prediction scoring | MATCH |
| Brier 0.153 and probabilities 0.78/0.50/0.60 | `analysis_r11.md` Brier table | MATCH |
| r9 d=0.519; MDE d=0.35; n=64 | `power_analysis_r11.md` lines 29, 51, 57 | MATCH |
| exact n≈64.07 and power 0.7996/0.79955 | `power_analysis_r11.md` and `INTEGRATOR-NOTES.md` adjudication | MATCH (rounded; honest ≈80%) |
| pids 201–264 and seeds 3000+pid*41 | `probe_plan_r11.md` lines 23, 131 | MATCH |
| 23:10:20Z, 23:28:37Z, 23:28:57Z | `ordering.log` | MATCH |
| pid 1299, 41-token argv, q4_0 KV, `--kv-unified` | descriptors JSONL record and PROVINCE | MATCH; live argv exact |
| r9 2/8=2/8 and 0.125 prediction error | `bench-arena-round9-replication.md` lines 68 and prediction table | MATCH |
| 0.50→0.35, +0.352, 0.002; 45%/33% | analysis and prediction tables | MATCH (45%/33% rounded from 29/64 and 21/64) |
| 8/64 gap and p=0.0963; Brier 0.153 | `analysis_r11.md` secondary/Brier sections | MATCH |
| 64.07, 0.7996, Φ(2.191)→2.192, 0.9858 | `power_analysis_r11.md` plus `INTEGRATOR-NOTES.md` errata | MATCH (adjudicated typo; bundle unchanged) |
| 0 errors; ~5 req/s | `analysis_r11.md` census and `INTEGRATOR-NOTES.md` timing | MATCH (1409/259.1≈5.4) |
| prior-art IDs 2609.08589, 2605.30233, 2606.11217, 2603.10044, 2411.00640, 2503.01747; #7052/#21038 | `r11-prior-art-granularity.md` and `r11-prior-art-prereg.md` | MATCH |

The only rounding imprecision is lessons’ “0.13–0.22”: the exact errors are 0.125 and 0.219, so the lower endpoint is rounded to two decimals.

## 3. Fleet-artifact citation and hash sweep

`INTEGRATOR-NOTES.md`-named artifacts were checked with `test -e`; all cited committed files exist, including `r11-mock-smoke.md`, the draft grader/recompute scripts, `prereg-precheck.log`, all listed prior-art/review/connector artifacts, and the round11-power scripts and run bytes. The explicitly marked ephemeral `/tmp/r11-mock/run.log.unshimmed` also existed at review time.

Observed commands and outputs:

- `sha256sum -c corpus/evidence/round11-power/prereg-bundle.sha256` → all three entries `OK`, exit 0.
- `sha256sum probe_r11.py run_r11.py` → `cf754d78e9065d679aa64872766be748a9d349fc13acdc5d03c5ba41447bdaa7`, `f012ab6e1fa206d59b28bce9d1058e557220c9c9ddbb7bc85c04199765dd3734`; both MATCH `ordering.log`.
- `md5sum` landed bytes → results `c42fe3d10b6d7a1ed14c4485af03357b`, run.log `281cb530702995854f162e807ee66ff3`, analysis `146633599d66257d47320fbc8a6bf4f4`; all MATCH `INTEGRATOR-NOTES.md`.

## 4. PROVINCE surface resolution

Commands: `test -e` for each local path, `curl -sS http://127.0.0.1:34113/v1/models`, `curl -sS http://127.0.0.1:34113/health`, and exact argv diff against the stored descriptors record.

- Research wiki paths, benchmark battery paths (including `report-qwenlocal*.csv` and `telemetry-qwenlocal-v2.csv`), Bailian telemetry/catalog paths, all six evidence directories, and `grader.py`: resolve.
- `/v1/models` → model JSON naming `Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`; `/health` → `{"status":"ok"}`.
- Stored descriptor `server.pid=1299`, 41 argv tokens; `/proc/1299/cmdline` → 41 tokens; `diff` → `ARGV-EXACT-MATCH`.
- **DEFECT:** `~/Projects/bounties/ledger/telemetry.jsonl` and its parent `~/Projects/bounties/ledger/` are absent (`test -e` → false). This is a non-blocking stale PROVINCE surface (and also affects the SKILL citation measure).
- `~/wikillm/llm-wiki` is absent as explicitly documented by PROVINCE, so it is not counted as an unexpected defect. External public-literature URLs were not fetched; the only permitted HTTP calls were the two local GETs above.

## 5. SKILL.md citation-resolution re-measure

The round-10 command convention was reused exactly for the requested finer measure. At the final stable measurement, `SKILL.md` had 511 lines, `## Cited local sources` began at line 487, and `md5sum` before/after the measure was identically `1b98b3d0238877cbca12f180fc6c1dd6`.

- `awk '/^## Cited local sources/,0' SKILL.md | grep -cE '^- '` → **23 bullets**.
- The requested extractor found **14 unique `~/` paths**. Literal `test -e` resolution was **10/14 = 71.4% strict**, below the required 90% floor.
- Under the round-10 repo convention (expand `**`/brace-style directory references and honor explicitly documented absence), the Karpathy glob paths and `~/wikillm/llm-wiki` resolve as conventionally intended; the ledger path remains genuinely absent. Thus **13/14 = 92.9% repo-convention**, above the 90% floor.
- **DEFECT:** strict resolution is below the stated floor because the ledger citation is stale and glob/documented-absence tokens are not literal `test -e` paths. **DEFECT (review integrity):** SKILL.md changed during this review: initial md5 `c75d3dea21212512364d44cd68cb4b59`, final stable md5 `1b98b3d0238877cbca12f180fc6c1dd6`; the final count above was rerun after the change and was stable before/after.

## 6. LOG.md discipline

Commands `git diff --stat -- LOG.md`, `git status --porcelain LOG.md`, and `grep` for round-11/r11 entries produced empty diff/status and zero existing round-11 matches. Observed result: **NO round-11 LOG entry exists yet; LOG.md is clean/unmodified**, consistent with L1 writing it last.

## Defect table

| ID | Defect | Severity | Blocking round-11 commit/push? |
|---|---|---|---|
| D1 | `round-8-aggregator-box3-coldrun.md` lacks a `corpus/README.md` lesson row | non-blocking | No |
| D2 | PROVINCE route-telemetry path `~/Projects/bounties/ledger/telemetry.jsonl` is absent | non-blocking | No |
| D3 | Strict requested SKILL `~/` extraction resolves only 10/14 (71.4%), below 90%; ledger citation is stale | non-blocking | No |
| D4 | SKILL.md changed during review (md5 c75d3dea…→1b98b3d0…); final measurement was rerun stable at 511 lines/23 bullets | non-blocking | No |

INDEX VERDICT: 4 defects
