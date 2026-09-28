# Round-8 aggregator audit — box-3 non-author cold run

- verifier: aggregator-lane round-8 L2 `labrat` seat Box3Kengaku — **non-author**; author lane: kengaku
- dispatched by: `.ufo/reports/round-8/aggregator.md` (main repo `shokunin`)
- stamp: start 2026-09-28T23:31:22Z HEAD `0c5120844a27ae9c8656a5f470af300960dd9ad5` dirty 2 → end 2026-09-28T23:33:49Z HEAD `0c5120844a27ae9c8656a5f470af300960dd9ad5` dirty 2
- dirty entries: untracked `corpus/evidence/round11-fleet/`, `corpus/evidence/round11-power/` (live lane's; untouched, not committed)
- entry: `SKILL.md` only (no LOG/SHONEN/SCORECARD/PROVINCE/report read before the run); files SKILL.md itself cites were opened as an operator would

## Commands executed
| # | SKILL.md cite | Command | Exit | Result vs claim |
|---|---|---|---|---|
| 1 | :8-11 | `test -e ~/wikillm/llm-wiki && echo EXISTS \|\| echo ABSENT` | 0 | ABSENT — matches SKILL.md's own note that the PROVINCE.md path does not exist; `~/Projects/webzites/repos/llm-wiki` exists (all 6 cited wiki notes OK) |
| 2 | :459 (cited source) | `test -e ~/.bailian/skills/bailian-docs-llm-wiki/models.jsonl` | 1 | MISSING at cited path — actual: `models/models.jsonl` (subdir); see break B1 |
| 3 | :184-187 | `wc -l + grep -c` per event class on `~/Projects/bounties/ledger/telemetry.jsonl` | 0 | total 7,226 (claimed 7,218 — live-append drift); dispatcher_tick 3,680 ✓; mission_parked 1,189 (claimed 1,188); mission_dispatched 1,167 ✓; attempt_reset 68 ✓; operator_decree 64 (claimed 58); mission_done 26 ✓; mission_failed 21 ✓ |
| 4 | :195 | `wc -l ~/bench-arena/telemetry-qwenlocal-v2.csv` | 0 | 34 lines = 33 data rows ✓; header matches claimed 12-field schema exactly |
| 5 | :195-196, :199-201 | python3 csv recompute of status/latency medians | 0 | PASS median 79.5 / FAIL 60.9 ms exactly as claimed (telemetry_available=n rows excluded); NULL-string rows present ✓ |
| 6 | :462 | awk status counts on `report-grok45.csv`, `report-qwenlocal-v2.v2.csv` | 0 | grok45 19 PASS/14 FAIL, qwenlocal 21 PASS/12 FAIL → 19/33 vs 21/33 ✓ |
| 7 | :277-278 | `grep 8080 ~/.config/opencode/opencode.json` → provider dump | 0 | `qwen-local.baseURL = http://localhost:8080/v1` exactly as claimed (listening-but-wrong pin still true) |
| 8 | :278, :436 | `curl 127.0.0.1:34113/health` → `{"status":"ok"}`; `/v1/models` → UD-IQ2_XXS model; `curl :8080/` → 404 | 0 | llama-server alive at pinned port; :8080 responds 404 (Jitsi, listening-but-wrong) ✓ |
| 9 | :371-378 | `tr '\0' ' ' < /proc/1299/cmdline`; grep ExecStart unit | 0 | pid 1299 alive (start 2026-09-28 02:55:28 local); flags match unit: `--cache-type-k/v q4_0`, `--kv-unified --parallel 2 --ctx-size 16384`, `--no-context-shift`, `--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja` ✓ |
| 10 | :374-376 | `curl :34113/slots` → per-slot n_ctx | 0 | 2 slots, both n_ctx=16384 ✓ ("each slot reports the full 16384 ctx") |
| 11 | :287-288 | `grep -c think ~/.config/llama/qwen-coder-godspeed.jinja` | 1 | 0 occurrences → template has no think branch ✓ ("enable_thinking is a no-op") |
| 12 | :296-300 | `wc -l` models.jsonl/families.jsonl | 0 | 413 models / 180 families — both exact ✓ |
| 13 | :300 | `GET openrouter.ai/api/v1/models` | 0 | exactly 460 entries ✓; HF `api/models` returns `sha`/`siblings`/`pipeline_tag` schema ✓ |
| 14 | :17-39 (table) | grep Add-Now numbering in shortlist note | 0 | All 8 "Add Now" + 2 "Add If Relevant" entries present in source note; decision-table rows 1:1 with source |
| 15 | :124-134 | sed YAML front-matter of 3 cited notes | 0 | Front-matter shape (`title/branch/category/source_ids/last_compiled/related`) matches the claimed convention ✓ |
| 16 | :54-55 | sed shortlist "What Public Benchmarks Will Miss" | 0 | 4 misses + "transfer checks, not core proof" verbatim; claim "lines 87–97" accurate to within ±2 lines of the printed section ✓ |
| 17 | :121, :381-420 | `python3 grader.py --selftest` | 0 | ALL PASS: S0 control exit 0; S1 ok-flip → exit 1 + `r8.replay.A-INC.ok`; S2 SUMMARY edit → exit 1 + `r8.summary.A-INC`; S3 raw-digit bump → exit 1 + `r9.replay.A-MONO.got` — matches claimed check-ids exactly |
| 18 | :381-394, :405-407 | `python3 grader.py` | 0 | `CHECKS n=149 mismatches=0 errata_pinned=1 / VERDICT: PASS` — matches round-10 claim `CHECKS n=149 mismatches=0` |
| 19 | :396-400 | `python3 grader.py --help` | 0 | Flags `--selftest --r8-jsonl --r8-runlog --r9-jsonl --r9-md` as claimed |
| 20 | :383, :389 | `grep ERRATA/imports grader.py` | 0 | ERRATA at grader.py:83 with adjudicated ruling; imports stdlib-only (argparse/hashlib/itertools/json/math/os/random/re/sys/tempfile) ✓ |

## Gated steps (cannot cold-execute)
| SKILL.md cite | Command | Why gated |
|---|---|---|
| :279-283 | `BENCH_ROOT=<scratch> bash ~/bench-arena/grade.sh <label>` | Grading runs `tasks/<task>/test.sh` against submitted solutions — executes arbitrary task code; needs an operator-scoped scratch root and a real model run to feed it (verifier ran its interface read-only instead) |
| :273-296 | opencode `loop.sh` / direct `POST /v1/chat/completions` battery run | Live-model inference spend + mutates `~/bench-arena/out/`/`graded/` trees; prohibited mutation/external surface for a cold audit |
| :425-431 | Production checklist steps 3-6 (freeze, smoke, battery, transfer slice) | Same: requires scored model runs; checklist is a run plan, not a read-only command |

## Break points (oral context would have been required)
| # | Cite | Break | Class |
|---|---|---|---|
| B1 | SKILL.md:459 | Cited source `~/.bailian/skills/bailian-docs-llm-wiki/models.jsonl` does not exist at the cited path; the file is at `models/models.jsonl` one level deeper. A cold operator recovers by `find`, but the cite as written fails. | wrong-path |
| B2 | SKILL.md:184-187 | Event-class counts (mission_parked 1,188 → 1,189; operator_decree 58 → 64; total 7,218 → 7,226) have drifted on a live-appended ledger. No staleness stamp per number; a cold operator cannot tell "verified 2026-09-28" from "verified at round N". | claim-falsified |
| B3 | SKILL.md:371-378 | Serving-stack pin is process-pinned to `pid 1299` — a value that changes on every service restart. The paragraph itself says a hermetic gate must never read `/proc` and should pin committed bytes, yet the pin mechanism it documents is exactly the fragile one. A cold operator after any restart finds pid 1299 gone and no replacement pin. | unresolvable-cite |
| B4 | SKILL.md:245 | `observed call on repeat probe: skill(name="min_stack")` — `min_stack` is not defined anywhere in SKILL.md; the r7 ablation note it points to (`corpus/knowledge/bench-arena-round7-scaffold-ablation.md`) is not opened by any earlier step, so the term's meaning is unreachable without reading an uncited-in-flow file. | undefined-term |

## Box-3 verdict
**[x]** — decided by steps 17-18 (`SKILL.md` §Hermetic grader :381-420): the two executable gates the file itself names as its operability gate — `python3 grader.py --selftest` and `python3 grader.py` — ran cold from the SKILL.md text alone, exit 0 with the exact claimed outputs (`CHECKS n=149 mismatches=0`; 4/4 selftest with claimed check-ids), and every surrounding citation they depend on resolved from the document (25/25 cited corpus/wiki/source paths verified; only B1 is a wrong-path cite with a trivially findable file). Supporting re-executions (steps 1-16, 19-20) confirmed the remaining read-only claims; no step required oral context beyond the four recorded break points, none of which blocks a competent cold operator (all have mechanical recovery paths). The grader gate is real, hermetic, and demonstrably fails on corruption (selftest) — box 3's core demand "executable without oral context" is met by the document's own designated gate.

## Post-run comparison
`SHONEN.md` box-3 line: "- [ ] Instructions executable by an agent without oral context / never tested: no cold-agent execution of `SKILL.md`/`corpus/` has been run or logged. Partial evidence strengthened round 10 — an in-repo gate now exists: `python3 grader.py` exits 0 hermetically (149 checks, 0 mismatches, no endpoint) and `--selftest` passes 4/4 with check-id assertions; independent mutation battery 4/4 (`corpus/evidence/round10-fleet/final-harness.log`); `python3 corpus/evidence/round9-fleet/test_harness.py` still exits 0. The probes themselves still need the live endpoint, so the box stays unmarked until a cold agent runs a checklist end-to-end" (`kengaku-shokunin/SHONEN.md:9-10`).
Divergence: **yes, resolved in kengaku's favor** — this run is the cold execution the line says has never happened; the grader-gate part of the claim re-executed exactly (149 checks, 0 mismatches, 4/4 selftest). The "probes still need the live endpoint" carve-out is accurate — the r8/r9 probe *runner* path was correctly GATED here — but the box-3 demand is satisfied by the hermetic gate the line itself names. Note the grader's `--selftest` S3 fired check-id `r9.replay.A-MONO.got`, where SKILL.md's round-10 falsification narrative (:408-415) describes M3 as 7-mismatch raw corruption — consistent (a single-digit bump is one of several raw-layer mismatches; both exit 1 at the raw layer), but the narrative's specific "7 mismatches" count was not reproduced by this selftest path and should not be read as a per-run invariant.
Ledger §11.4/D-15 held kengaku's `SHONEN.md` to be a **3-box file** (box 3 absent). At HEAD `0c51208` it is a **4-box file**: checkbox lines at SHONEN.md:5 `[~]`, :7 `[~]`, :9 `[ ]`, :11 `[~]` — box 3 is present as a line (unmarked), not absent. The D-15 characterization is obsolete; the live lane evidently rewrote SHONEN.md after D-15 was recorded.

## Incidental (boxes 1/2/4 — not graded here)
- Box 1 (decision tables/error patterns/checklists/cited sources): 2 decision tables, 14 anti-patterns, 9-step production checklist, ~20 cited-source bullets — all present and source-backed (steps 14-16).
- Box 2 (≥1 logged end-to-end domain task): the committed r8/r9 evidence trees the grader replays (258 + 284 records) are themselves the logged domain tasks; LOG.md not read pre-run, not graded here.
- Box 4 (cross-domain bleed): SKILL.md stays inside LLM-eval/research province throughout; no foreign-domain instruction tables encountered.
