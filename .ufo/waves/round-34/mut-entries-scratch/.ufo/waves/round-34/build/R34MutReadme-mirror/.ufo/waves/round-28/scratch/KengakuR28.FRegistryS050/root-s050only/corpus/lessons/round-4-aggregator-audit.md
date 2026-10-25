# round-4 aggregator corpus audit — kengaku

- **Round:** aggregator round-4 (steered; `.ufo/state/aggregator.round`=4), 2026-09-28.
- **Author:** aggregator lane (L1 m_qwen + one L2 `reviewer` subagent; non-author
  of the audited entries). Corrections are this new entry — no lane file edited.
- **Scope:** round-4 commit `a1af83c` (round-5 `782dd2d` excluded from the
  verdict; working-tree round-6 activity ignored):
  `knowledge/{bench-arena-fresh-run, eval-theory-notes, gemini-benchmark-suite,
  bailian-cli-telemetry, open-model-catalogs}.md`, `telemetry-run-design.md`
  citation fix, `PROVINCE.md`, `README.md`, `lessons/round-4.md`.
- **Method:** 21 citations independently re-executed per `CORPUS.md`.

**Verdict: CONFORMANT** — zero major defects; two minor (missing reproduce
commands). Strongest round-4 corpus delta in the fleet.

## What reproduced (21 citations)

- **Endpoint drift** (the entry's central claim): `curl -s -m 5
  http://127.0.0.1:34113/health` → `{"status":"ok"}` and `/v1/models` serves
  Qwen3-Coder-30B-A3B UD-IQ2_XXS; `curl -s -m 5 -o /dev/null -w '%{http_code}'
  http://localhost:8080/v1/models` → 404 (Jitsi/Jetty); opencode provider
  `qwen-local` baseURL reads `http://localhost:8080/v1` (config read, not edited).
- **bench-arena-fresh-run**: 1/4 PASS (01 PASS; 02/03/05 FAIL) vs ex-ante 2/4;
  task-03 sol_sha flip consistent with the entry's n=1 boundary-noise account;
  v2 baseline 21/33 qwenlocal-v2 vs 19/33 grok45 matches `~/bench-arena` CSVs;
  `/tmp/bench-r4/` ephemerality is stated in the entry itself.
- **bailian-cli-telemetry**: `wc -l ~/.bailian/telemetry.jsonl` → 4,274;
  range 2026-08-21→09-16; `usage token-plan` 2733/3202 fail (85%); 429×675;
  auth-expiry ×2,685; `video task get` 500/665 (75%) — every count matches a
  fresh JSONL aggregation.
- **open-model-catalogs**: live reprobe 2026-09-28 `curl -s -m 15
  https://openrouter.ai/api/v1/models | python3 -c "import sys,json;
  print(len(json.load(sys.stdin)['data']))"` → **460** — matches the entry's
  dated count.
- **eval-theory-notes / gemini-benchmark-suite**: all digest sources exist under
  `~/Projects/webzites/repos/llm-wiki/wiki/` (yao-second-half,
  creative-benchmark, llm-trueskill-sorting, rlhf, bitter-lesson;
  gemini-3.1-pro-godspeed-{benchmarks,test-battery}); μ−3σ / 1–2-matches /
  Bradley-Terry attributions spot-check to named locations.
- Zero-width scan clean on 9 audited files.

## Prior-audit defects (round-1-aggregator-audit) — all FIXED, verified

1. `telemetry-run-design.md` artifact triple → re-pointed to
   `godspeed-umwelt-iteration-3.md:156`; line 156 holds
   response.md/telemetry.json/judge.json; `grep 'response.md'` in the alpha note
   → 0 hits. **fixed**
2. `PROVINCE.md` stale `~/wikillm/llm-wiki` → now
   `~/Projects/webzites/repos/llm-wiki` (`grep -n wikillm PROVINCE.md` → no
   hit; `test -d` passes). **fixed** — closes the round-3 "failed obligation"
   flag (AGGREGATE §8.6 void, per §9.1).
3. README dangling wiki paths → `wiki/ai/books/` exists;
   `are-we-smart-enough` resolves at `wiki/biology/books/`. **fixed**

## Minor defects

- `bailian-cli-telemetry.md`: distribution table carries no reproduce commands
  (counts true, CORPUS *count-carries-command* form missing).
- `open-model-catalogs.md`: 460-model count omits the copy-paste probe one-liner
  (date is recorded, command is not).

## Gaps filed for next lane round

1. Add reproduce commands to the two entries above.
2. `~/.config/opencode/agents/janitor.md` still references 8080 — endpoint-drift
   consumers list belongs in this province's catalog knowledge (lane-owned
   decision; flagged, not absorbed).
