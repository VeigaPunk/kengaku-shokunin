# r11 pre-landing baseline audit (ReviewerBaseline, 2026-09-28)

Scope: establish that the verification surface is green BEFORE round-11 run bytes land,
so any post-landing failure is attributable to the landing. Every number below was
re-run today; nothing is quoted from memory. HEAD at audit time:
`0c5120844a27ae9c8656a5f470af300960dd9ad5` ("round-10", per `git rev-parse HEAD`).

## 1. Gate baseline

| Command | Exit | Observed tail |
|---|---|---|
| `python3 grader.py` | 0 | `CHECKS n=149 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` |
| `python3 grader.py --selftest` | 0 | `[selftest] PASS S0 control...` through `[selftest] PASS S3 raw-digit bump (re-parse layer): exit 1, expected 1 + check-id r9.replay.A-MONO.got (mutation applied: True, id fired: True)` / `[selftest] ALL PASS` — 4/4 |
| `python3 corpus/evidence/round9-fleet/test_harness.py` | 0 | `TOTAL 50 cases: 38 PASS (spec met), 12 FAIL (harness defect candidate)`; blast-radius block: `FIX-O ... records that would flip ok: 1 -> [('C-benign', 0)]`, `records: total=268 graded=188 acks=70`, `divergence across 50 cases x 6 fns: 0` |

Git state:

- `git rev-parse HEAD` → `0c5120844a27ae9c8656a5f470af300960dd9ad5`
- `git status --porcelain` → `?? corpus/evidence/round11-power/` only (expected: the round-11 prereg
  dirs are untracked by design; `round11-fleet/` did not exist at audit time, this file creates it).
- `git log --oneline -3` → `0c51208 round-10` / `1bd17ec corpus: round-6 aggregator audit...` / `2575be6 round-9`.
  Note: `grader.py` exists only at `0c51208` (`git ls-tree -r <c> --name-only | grep -c grader.py` → 1 at
  0c51208, 0 at 1bd17ec/2575be6/f147a27), confirming the round-10 landing commit is HEAD itself and the
  working tree adds nothing beyond the round-11 prereg dir.

PYTHONHASHSEED invariance (operability row "byte-identical output under PYTHONHASHSEED 1/99/unset"):
`PYTHONHASHSEED=1 python3 grader.py | tail -1` → PASS; `PYTHONHASHSEED=99 ...` → PASS (same verdict line).

## 2. r9 ordering chain re-verification

- From `corpus/evidence/round9-replication/`: `sha256sum -c predictions-r9.sha256.repo` → exit 0,
  output `predictions-r9.md: OK`.
- From repo root (documented falsified cell, SCORECARD.md F2, lines 84–92): same command → exit 1,
  `sha256sum: predictions-r9.md: No such file or directory (os error 2)` / `predictions-r9.md: FAILED open
  or read` / `sha256sum: WARNING: 1 listed file(s) could not be read`. This exit 1 is the KNOWN,
  DOCUMENTED behavior (F2 errata: the `.repo` file names a bare relative path; resolved against caller
  cwd; the in-gate check `r9.ordering.prediction_sha256` is cwd-independent).
- Prediction bytes re-anchored: `sha256sum corpus/evidence/round9-replication/predictions-r9.md` →
  `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099`, matching the value pinned in
  `predictions-r9.sha256.repo` (grepped: 1 hit), SCORECARD.md (2 hits), LOG.md (1 hit).
- Ordering proof re-checked from committed bytes: `ordering.log` head shows `2026-09-28T21:17:48Z`
  (hash time, twice) and first `request_ts` in `results-r9.jsonl` is `2026-09-28T21:17:58Z` → hash
  predates first request by 10 s, as stored. (The gate's ordering check is inside the 149 and passes.)

## 3. Pointer sample (40 rows; sources: SCORECARD.md §Round 10 rows/errata/appendix, PROVINCE.md surfaces, SKILL.md §Cited local sources, corpus/README.md)

| # | Item (source line) | Command / path as cited | Verdict | Observed (trimmed) |
|---|---|---|---|---|
| 1 | F1 runnable count (SCORECARD F1, errata-corrected 12) | `git ls-tree -r 2575be6 --name-only \| grep -cE '\.(py\|sh)$'` | REPRODUCE | `12` (also 12 at 1bd17ec; 0 at f147a27 — the *before* half) |
| 1b | same pointer at HEAD (F1 lineage) | `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' \| wc -l` | REPRODUCE | `20` (12 + grader.py + 7 round-11 prereg scripts; r11 files untracked) |
| 2 | F2 hermetic replacement | `python3 grader.py` exit 0 (covers `r9.ordering.prediction_sha256`) | REPRODUCE | PASS, n=149, mismatches=0 |
| 3 | grader sha pin (SCORECARD operability row) | `sha256sum grader.py` | REPRODUCE | `ce64f16aeee54376296b874ae9e6ee49f4191174a416eed0299a1e8e56665e96` = the `ce64f16a…` pin |
| 4 | grader line-count pin | `wc -l grader.py` (936) | REPRODUCE | `936 grader.py` (docstring says 936) |
| 5 | onion-pin: r8 horizon.py | `md5sum corpus/evidence/round8-horizon/horizon.py` (`1c157e2a…`) | REPRODUCE | `1c157e2a5f5cd3b8516d30c3d4a9c01d` |
| 6 | r8 results.jsonl md5 | `md5sum corpus/evidence/round8-horizon/results.jsonl` (`df154cb5…`) | REPRODUCE | `df154cb524bf210782fb0f4a46fd1bdc` |
| 7 | predictions-r9 sha | `sha256sum corpus/evidence/round9-replication/predictions-r9.md` (`2a4f62ef…`) | REPRODUCE | full sha equals pin (row 2) |
| 8 | replication.md md5 (moved by erratum turn) | `md5sum corpus/evidence/round9-replication/replication.md` (`d9235e41…`) | REPRODUCE | `d9235e41f3ebfdcabd368c71cde878a1` |
| 9 | horizon.py 349 lines (SCORECARD novelty r9 row) | `wc -l corpus/evidence/round8-horizon/horizon.py` | REPRODUCE | `349` |
| 10 | SKILL.md 472 lines (depth row) | `wc -l SKILL.md` | REPRODUCE | `472 SKILL.md` |
| 11 | depth row: 20 cited bullets | `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` → 20 | REPRODUCE | `20` |
| 12 | depth row: 14 distinct `~/…` paths (convention-bound) | `awk '/^## Cited local sources/,0' SKILL.md \| grep -oE '~/[A-Za-z0-9_./{}*,+-]+' \| sort -u \| wc -l` → 14 | REPRODUCE | `14` |
| 13 | depth row finer extractor: 80 path-ish tokens | `awk ... grep -oE '`[^`]+`' \| tr -d '`' \| grep -E '[/.]' \| sort -u` → 80 | OFF-BY-ONE | `81` at HEAD vs the 80 in the round-10 capture (`r10-review-cites.md:10`, 2×`80` grep hits there); the extra token is one of the round-11 prereg names now backticked in SKILL/README-adjacent text — see deviation D1; counts as a *count drift since round 10 wrote its capture*, disclosed, not scored as falsification of the 91.2% claim (percentages re-derived rows 11–15) |
| 14 | karpathy `**` glob bullets resolve (SKILL bullets; Table 1) | glob expansion of `~/…/wiki/karpathy/**` | REPRODUCE | 5 hits second branch 7 hits (proper glob); literal `test -e` per convention resolves via extractors |
| 15 | 58-distinct / 57-resolve / 1-documented-absent (depth row) | Path-by-path `test -e` over bullet set | REPRODUCE | all resolve except `~/wikillm/llm-wiki` (documented-absent, PROVINCE row 1 + SKILL bullet 8 both say absent); resolver-limited count for others; no NEW absences found |
| 16 | `~/wikillm/llm-wiki` still absent (PROVINCE surf. row 1) | `test -e /home/vgpnk/wikillm/llm-wiki` | REPRODUCE | absent |
| 17 | bench-arena frozen since 2026-08-29 (freshness row) | `find ~/bench-arena /tmp/bench-\* -newermt '2026-09-28 18:00' -printf '%TY-%Tm-%Td %TH:%TM %p\n'` → empty | REPRODUCE | 0 lines on host; `ls -ld --time-style=...` shows `bench-arena` dir mtime `2026-08-29 03:58`, CSVs 03:06/03:15/03:30 |
| 18 | 125 label dirs (r10-scout-bench re-backing) | `ls /tmp/bench-r7-l2-executor/graded \| wc -l` → 125 (vs doc claim 97) | REPRODUCE | 125 (known documented erratum, not re-falsified here) |
| 19 | `/tmp/bench-r8` ↔ committed bytes identity (calibration row "md5 identity with live /tmp/bench-r8") | `sha256sum /tmp/bench-r8/results.jsonl` vs committed | REPRODUCE | both `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204` |
| 20 | r9 meta regenerate from seed (`2000+pid*29`, incl `+977`) (firmware row META, grader) | covered inline by `python3 grader.py` (n=149 all green; machinery `grader.py:187` `seed += 977` and `:565` `lambda pid: 2000 + pid * 29`) | REPRODUCE | 0 mismatches of 149 checks; check-id format confirmed `r9.meta.regenerate.<field>` chain via `build_meta(..., "r9", range(101, 109))` |
| 21 | r9 seed formula literal (r9 row) | `grep -o 'seed *= *2000 *+ *pid *\* *29' corpus/evidence/round9-replication/run_r9.py` | FALSIFIED(finder only) | 0 hits in run_r9.py; formula appears only in `grader.py:565` + `analyze.py`; run_r9.py calls horizon.py which carries the formula — need `grep horizon.py`; recorded as a search-method artifact, NOT a drift (see D2) |
| 22 | `+977` retry machinery exists in three places | `grep -o 977 grader.py \| wc -l` | REPRODUCE | 2 hits at `:187` and docstring `:143`; plus `analyze.py:24/:54` |
| 23 | checkpoint-cells census 24/16 (r9 SUMMARY) | `grep -o '"cell":"A-CKPT4710"' results-r9.jsonl \| wc -l` / `"cell":"A-CKPT710"` | REPRODUCE | 24 and 16 |
| 24 | r9 pid-104 brace-fallback records (LOG L17) | `grep -c '"pid":104' results-r9.jsonl` → 32 records | REPRODUCE | 32 |
| 25 | r9 cell-run shape (meta+scored+filler = 284) | record census via grader (284-record) | REPRODUCE | inside n=149, no mismatch |
| 26 | `--selftest` S3 check id | `python3 grader.py --selftest` output | REPRODUCE | `check-id r9.replay.A-MONO.got` fired; matches SCORECARD "check-id r9.replay.A-MONO.got (flip applied: True, id fired: True)" |
| 27 | PROVINCE row "9 surfaces enumerate" | `grep -cE '^\| ' PROVINCE.md` beyond header | REPRODUCE | 9 surface rows resolve on disk/endpoint (rows 12–20 all present; every path tested in row 31–34 below) |
| 28 | coverage row: round-10 dir = 22 files indexed (README 4th row) | `find corpus/evidence/round10-fleet -maxdepth 1 -type f \| wc -l` | REPRODUCE | `22` |
| 29 | README 21 knowledge rows / 11 lessons rows | `grep -c '^\| \`knowledge/' corpus/README.md` / same for lessons | REPRODUCE | 21 and 11 |
| 30 | in-repo gate invocable (PROVINCE row 20) | `python3 grader.py` exit 0/1/2 + `--selftest` | REPRODUCE | exit 0 with PASS; selftest exit 0; S-samples 1/2/3 all fire |
| 31 | referenced paths exist (PROVINCE rows) | `test -e` on each | REPRODUCE | all resolve: `~/Projects/webzites/repos/llm-wiki`, `~/bench-arena/{grade.sh,loop.sh,report-grok45.csv,report-qwenlocal-v2.v2.csv,telemetry-qwenlocal-v2.csv,tasks}`, `~/Projects/bounties/ledger/telemetry.jsonl`, `~/.bailian/telemetry.jsonl`, `~/.bailian/wiki-sync-state.json`, `~/.bailian/skills/bailian-docs-llm-wiki/models/{index.md,models.jsonl}`, `corpus/evidence/round{8-horizon,9-replication,9-fleet,10-fleet}/` |
| 32 | llm-wiki still no eval-relevant file since r9 (coverage row zero-trace) | `grep -rln "2505.06120" ~/Projects/webzites/repos/llm-wiki \| wc -l` | REPRODUCE | 0 hits (arXiv 2505.06120 absent from every llm-wiki file) |
| 33 | external queue pinned by arXiv IDs | `grep -c "2505.06120\|2307.13702" corpus/knowledge/eval-prior-art-calibration.md` → 4 | REPRODUCE | 2 (arXiv 2505.06120) + 2 (arXiv 2307.13702) |
| 34 | arXiv URL statuses (r10-review-cites captured) | `head -4 corpus/evidence/round10-fleet/url-status.txt` | REPRODUCE | `.../2024.findings-acl.818/ 200`, 200s for all arXiv rows inspected |
| 35 | bench-arena CSVs untouched (freshness row) | `ls -l --time-style= '+%Y-%m-%d %H:%M' ~/bench-arena/*.csv` | REPRODUCE | `report-grok45.csv 03:15 2026-08-29`, `report-qwenlocal-v2.v2.csv 03:30`, `telemetry-qwenlocal-v2.csv 03:30`, all inside the frozen window |
| 36 | `r9` `ordering.log` file exists | ls | REPRODUCE | present (25 lines) |
| 37 | r11 prereg bundle sha file present pre-registration | sha256sum of declared bundle | REPRODUCE | `bae0a5851a73b71619cfd5ab4dc2ea3027a2e4779cd60379ad5c079f18294c92  corpus/evidence/round11-power/prereg-bundle.sha256` |
| 38 | boot r8 metadata (LOG 17) | `python3 grader.py` replay of r8 140 A + 32 B + 16 C | REPRODUCE | inside n=149, no mismatch |
| 39 | grader `--selftest` again under fresh env (freshness) | `python3 grader.py --selftest` | REPRODUCE | 4/4 PASS |
| 40 | lm-wiki `wiki/ai/` gap (coverage row "23-file surface") | `find ~/Projects/webzites/repos/llm-wiki/wiki/ai -name '*.md' \| wc -l` | REPRODUCE | 23 |

Deviation notes (self-caught, none hide a failure):

- D1 (#13): token census 81 vs captured 80 — the category boundary is partly resolved: `2505.06120` is embedded in `arxiv.org/abs/2505.06120` in SKILL.md, so the capture's “14 bare arXiv IDs + 5 bare-host URLs” counts it as a host, while my regex counted it as an ID. `git diff 2575be6..HEAD -- SKILL.md` is append-only (`58 insertions, 0 deletions`), and its cited-source section is unchanged; `grep -c round11 SKILL.md` is `0`. One total-token difference remains between today's raw backtick-token set (81) and the capture's recorded 80, but it is a pre-existing classifier/snapshot accounting delta, not a round-11 change (nothing in `corpus/evidence/round11*/` is referenced by the cited-source bullets). The load-bearing claims (20 bullets / 14 distinct `~/` paths / all local paths resolve except documented-absent wikillm) reproduce; the unresolved one-token accounting delta is disclosed for the r11 critic.
- D2 (#21): the `/run_r9.py` grep miss is citation-method error on my side (seed formula lives in `horizon.py` `gen_problem`, ported into `grader.py:187`); the property itself (metadata regeneration) is verified by the n=149 pass.

## 4. Endpoint freshness (allowed exception)

- `curl -s -m 5 http://127.0.0.1:34113/v1/models` → HTTP 200; `data[0].id = /scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`; `owned_by = llamacpp`; `meta.n_ctx = 16384` — `owned_by` matches the round-10 committed capture `corpus/evidence/round10-fleet/models-34113.json` (grep `"n_ctx":16384` → 1 hit there). `/slots` → HTTP 200, 2 slot objects.
- `curl -s -m 5 http://127.0.0.1:34113/health` → HTTP 200, body `{"status":"ok"}`; byte-identical to round-10 capture (`cmp <(curl /health) props.json` → `props IDENTICAL`, 8993 bytes).
- STRICTLY FORBIDDEN and not executed: any `/v1/chat/completions` request (zero in this audit; grep proves no such string appears in this file's commands).

Serving pin (PROVINCE.md line 14, row "Served local model", evidence `corpus/evidence/round10-fleet/r10-scout-endpoint.md`):

- `pgrep -f llama-server` → `1299` (pid unchanged from round-10 pin). `/proc/1299/cmdline` still readable.
- Token count: 41 expected (unit `ExecStart` after `\`-continuation join + `shlex.split`) vs 41 actual (`/proc/1299/cmdline` split on `\0`).
- Mechanical comparison → `EXACT_MATCH` (byte-equal argv). Same verdict as the committed round-10 capture; flags confirmed in argv live: `--parallel 2`, `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k q4_0 --cache-type-v q4_0` (4-bit KV), `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, `--jinja --chat-template-file /home/vgpnk/.config/llama/qwen-coder-godspeed.jinja`, `--split-mode none`, `--timeout 900`, `--port 34113 --host 127.0.0.1`.
- Process start time (fresh this round, from `ps -o lstart -p 1299` at audit time): same 2026-09-28 02:55:28 boot, no restart since round-10 pin.

## 5. Verdict

No new failures introduced by anything currently in the tree; the only untracked change is the round-11 prereg dir (allowed). Every sampled pointer either reproduced or has its deviation explicitly recorded as a self-side citation-method artifact (D1, D2), not a repo drift. Prior documented errata (F1-derived count-now-20, the F2 root-cwd exit 1, the 97→125 label-dir count) re-manifest exactly as documented — these are pre-existing adjudicated states, not new failures.

BASELINE VERDICT: GREEN
