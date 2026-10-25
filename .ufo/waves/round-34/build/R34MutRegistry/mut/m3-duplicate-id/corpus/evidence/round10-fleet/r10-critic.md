# r10 critic — SCORECARD.md round-9 post-move falsification

Scope: every backticked command and concrete number in the **Round 9 — post-move**
table, the **Measurement proxies** block, and the **operability / coverage /
freshness** rows of the **Round 9 — pre-move** table, re-run from repo root
`/home/vgpnk/projects/shokunin/kengaku-shokunin` (HEAD `1bd17ec`, branch
`master`, working tree clean except nothing tracked: `git status --porcelain` → 0 lines).

Every verdict row below carries the exact command I ran and its output. No repo
edits were made (`git status --porcelain | wc -l` → `0` before and after all work).

**Grader prerequisite note:** `ls grader.py` → `No such file or directory` at
time of audit. This artifact is written against the SCORECARD as committed at
HEAD `1bd17ec`; the r10 grader was not yet present to be graded itself.

---

## Verdict table

### Round 9 — post-move table

| # | Claim (quoted) | Command re-run | Output | Verdict |
|---|---|---|---|---|
| 1 | operability: "Runnable files in-repo went **0 → 11** (`find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' \| wc -l` → **11**)" | `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' \| wc -l` | **12** (also `git ls-tree -r 2575be6 --name-only \| grep -cE '\.(py\|sh)$'` → **12**; same 12 files listed at both refs; at `f147a27` → **0**) | **FALSIFIED** (0→11; actual 0→12 at both HEAD and round-9 commit 2575be6 — matches L1's independent count) |
| 2 | operability: "`python3 corpus/evidence/round9-fleet/test_harness.py` → exit 0, 50 cases, `38 PASS / 12 defect candidates`" | `python3 corpus/evidence/round9-fleet/test_harness.py` | `exit=0`; `TOTAL 50 cases: 38 PASS (spec met), 12 FAIL (harness defect candidate)` (51 PASS/FAIL tokens, 50 cases + TOTAL line) | **REPRODUCES** |
| 3 | operability: "blast radius recomputed from the committed `results.jsonl` (`FIX-O` flips exactly 1 record)" | `python3 /tmp/kengaku-r10/recompute_r8.py` (independent FIX-O rule `ok ∧ over_repair` over all 268 r8 records) | `FIX-O would flip: 1 [('C-benign', 0, None)]` — exactly one flip, C-benign rep 0 | **REPRODUCES** (matches `harness-mutation.md:114` "FIX-O (ok &= not over_repair) records that would flip ok: 1 -> [('C-benign', 0)]") |
| 4 | operability: "`/tmp` → repo copy check `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`" (as an Evidence pointer, i.e. implied to pass from repo root) | `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo` | `sha256sum: predictions-r9.md: No such file or directory (os error 2)` / `predictions-r9.md: FAILED open or read` / `WARNING: 1 listed file(s) could not be read`, **exit 1** | **FALSIFIED** (pointer as-written fails from repo root; the checksum itself is correct — re-run from `corpus/evidence/round9-replication/` gives `predictions-r9.md: OK`, exit 0. Stale relative-path bug, not wrong bytes.) |
| 5 | operability ceiling: "none exits nonzero when a stored SUMMARY disagrees with a recomputed one" | `grep -nE 'sys\.exit\|exit\(' corpus/evidence/round9-fleet/*.py corpus/evidence/round9-replication/*.py corpus/evidence/round8-horizon/*.py` | only `test_harness.py` matches `sys.exit`; no analyzer exits nonzero on SUMMARY disagreement | **REPRODUCES** (ceiling statement accurate; motivates the r10 grader) |
| 6 | calibration (d): "the run artifact is landed byte-identical (`results.jsonl` `df154cb5…` with `raw` on 258/258 non-meta records, `run.log` `fc3b232f…`)" | `md5sum corpus/evidence/round8-horizon/*` | `df154cb524bf210782fb0f4a46fd1bdc  results.jsonl`; `fc3b232ffc532717e50c1d06e0549acc  run.log`; `1c157e2a5f5cd3b8516d30c3d4a9c01d  horizon.py`; `33864062dbd7314300577f38c87f97cf  critic-defects.md`; and `md5sum /tmp/bench-r8/{results.jsonl,run.log}` → **identical md5s** | **REPRODUCES** (`md5sum` byte-identical; 258/258 raw re-derived from 268 records − 10 meta) |
| 7 | calibration (b): "predictions hashed before the first request (`sha256 2a4f62ef…`, `ordering.log` 21:17:48Z, first `request_ts` 21:17:58Z)" | `cat ordering.log`; `grep -o '"request_ts"[^,]*' results-r9.jsonl \| sort \| head -2` | `2026-09-28T21:17:48Z` ×2; min request_ts = `2026-09-28T21:17:58Z`; hash in `.sha256.repo` = `2a4f62ef20a65e7a7cb3b7414b54d0f995126209c3126ae674b7cc3af2bc1099` | **REPRODUCES** |
| 8 | calibration (b): "scored at close (2/4 cell hits, mean abs error 0.094 of n, 4/4 directional falsifiers unfired, onset 5.0 predicted vs 5.8 observed)" | recompute from `predictions-r9.md` (4 point predictions) + fresh SUMMARY recompute from `results-r9.jsonl` (`/tmp/kengaku-r10/recompute_r9.py`) | hits = CKPT4710 (2/8 exact), MONO (0/8 exact) → **2/4**; MAE = (0.250+0.000+0.125+0.000)/4 = **0.09375** (rounds to 0.094); onset recompute `[None,2,7,7,3,10,None,None]` → mean(non-perfect) = **5.8** (5 non-perfect); predictions file's falsifiers all fired-conditions — none fired | **REPRODUCES** |
| 9 | calibration (c): "the r8 debt is analyzed, logged and committed — 5 L2 analyses + a fix-landing audit + a 50-case harness mutation test" | `grep -c 'holds \*\*19\*\* files' LOG.md` → 1; `grep -c '18 files' LOG.md` → 1 (superseded-then-corrected pair); `grep -n '5 L2\|five L2' LOG.md` → 0 hits; file census below | LOG round-9 entry (L14) says "10 L2s"; 19 files in `round9-fleet/` at both 2575be6 and HEAD; L2 analyses present: `probeA/probeB/probeC.md` + `critic.md` + `harness-mutation.md` (5) + `review.md` + `sibling-overlap.md` + `prior-art.md` (3 more) | **REPRODUCES with a count gap** — 3 scorer-visible analysis artifacts + critic + mutation = 5 named analyses check out; the "10 L2s" is a separate (unquoted) LOG claim, and LOG self-corrects 18→19 files in a later entry. Not falsified. |
| 10 | novelty row: "one scout L2 … graded **3 of 4** round-8 findings known/incremental and the non-iid-draws finding a *direct replication* of llama.cpp issue #7052 … 2/4 instruments" | read `corpus/knowledge/eval-prior-art-calibration.md` + `curl -s https://api.github.com/repos/ggml-org/llama.cpp/issues/7052` | verdict table has exactly 4 numbered findings; finding 4 = "known — direct replication: llama.cpp issue #7052"; live fetch confirms title "Non-deterministic output of the llama.cpp server when using multiple slots", created 2024-05-03, body: "5 and 8 unique completion texts when using 8 slots", single-slot deterministic | **REPRODUCES** (all 4 findings carry fetched URLs; phenomenon-vs-instrument split 0/4 / 2/4 matches the table) |
| 11 | novelty row: "The r9 dose cell (`A-CKPT710`) … returned a tie (2/8 = 2/8), so it bought severity resolution (`nwrong` 0.875→1.375), not a pass-rate dose response" | `/tmp/kengaku-r10/recompute_r9.py` | `A-CKPT4710: 2/8 0.875`; `A-CKPT710: 2/8 1.375` | **REPRODUCES** |
| 12 | depth row: "`SKILL.md` grew 312 → **414** lines" | `wc -l SKILL.md`; `git show f147a27:SKILL.md \| wc -l` | `414 SKILL.md`; `312` | **REPRODUCES** |
| 13 | depth row: "anti-patterns 8 → **13**, a new §'Planning-horizon & transcript-shape probes' … cited-source bullets 16 → **20**" | `git show f147a27:SKILL.md \| sed -n '/^## Benchmark anti-patterns/,/^## Research-note/p' \| grep -cE '^[0-9]+\. '` (→8) vs same at HEAD (→13); `grep -c 'Planning-horizon' SKILL.md` → ≥1 (section at `:310`); `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` | 8 → 13 numbered items; planning section present at HEAD, absent at f147a27; bullets **16 → 20** | **REPRODUCES** |
| 14 | depth row: "Three errata appended … (`bench-arena-round7-noise-n25.md` `0/12`→`0/17`, `lessons/round-5.md` flip→delta terminology, `ledger-route-telemetry.md` 7,218→7,224 drift + counting command)" | `grep -n '0/17' corpus/knowledge/bench-arena-round7-noise-n25.md`; `grep -n -i 'flip\|delta' corpus/lessons/round-5.md`; `grep -n '7,224\|7,218' corpus/knowledge/ledger-route-telemetry.md` | `:81 denominator is wrong: \`0/12\` → \`0/17\``; round-5 erratum present ("flipped" is the superseded word); `7,218→**7,224** (+6 since profiling)` | **REPRODUCES** (all three errata verified in place) |
| 15 | depth ceiling: "the 3-source digest queue (Laban ICLR 2026, Lanham 2023, llama.cpp #7052) is named but unread" | `grep -rl 'Lanham' corpus/knowledge/` | only `eval-prior-art-calibration.md`; no separate digest entry for any of the three | **REPRODUCES** |
| 16 | coverage row: "`PROVINCE.md` now enumerates **8 surfaces** (all resolving) with refusals and **3 named report-outs**" | `awk '/^## Surfaces/,/^## Refusals/' PROVINCE.md \| grep -cE '^\| [A-Z]'` → 8; path existence checks on all listed surfaces; `grep -c 'kotoba\|kasegi\|kumitate\|kagi' sibling-overlap.md` → 18; section "Report out (not absorb; at most three)" | 8 surface rows; all local paths exist (llm-wiki, bench-arena, telemetry.jsonl ×2, .bailian ×2, model index; `~/wikillm/llm-wiki` correctly documented-absent — `test -e` exit 1); 3 report-outs (kotoba / kasegi+kumitate / kagi) | **REPRODUCES** |
| 17 | coverage row: "README index completed in both directions — **21 knowledge rows = 21 files, 11 lessons rows = 11 files** … plus a new `evidence/` section covering all 3 evidence dirs" | `grep -c '^| \`knowledge/' corpus/README.md` → 21 = `ls corpus/knowledge \| wc -l` → 21; `grep -c '^| \`lessons/' → 11 = `ls corpus/lessons \| wc -l` → 11; `sed -n '45,56p'` shows all 3 evidence dirs | 21=21, 11=11, 3 evidence dirs all covered (`round8-horizon`, `round9-replication`, `round9-fleet`) | **REPRODUCES** |
| 18 | coverage ceiling: "the served-model surface (`:34113` flags: `--cont-batching`, `-np`) is documented from behaviour, never from the process cmdline" | `grep -rn 'cont-batching\|-np' corpus/ SKILL.md PROVINCE.md` | `--cont-batching` appears in `bench-arena-round7-noise-n25.md:55` (marked "Suspect") and `lessons/round-7.md:29`; `-np 1` only in `corpus/README.md:84` as a *digest-queue* item ("none read yet") | **REPRODUCES** (flags indeed behaviour-inferred; no cmdline capture in repo) |
| 19 | freshness row: "The round-9 LOG entry carries re-verification results for every claim it touches: endpoint identity (`/v1/models`, `/health` 200), evidence md5s, the r8↔r9 SUMMARY recomputation from committed bytes, and citation counts" | `sed -n '14p' LOG.md \| grep -oc` for each component | endpoint re-verification present (`curl … /v1/models` → GGUF id, `/health` 200 — re-runnable and re-verified below, #22); **evidence md5s: ABSENT from L14** (`sed -n '14p' LOG.md \| grep -oc 1c157e2a\|df154cb5\|fc3b232f\|3386406` → 0 for all four; `df154cb5` appears only in L13); **"SUMMARY recomputation from committed bytes": ABSENT** (`grep -oc 'recomput\|re-deriv\|replay\|recheck\|committed bytes\|from committed'` in L14 → 0; only the r8↔r9 ladder numbers appear, no recomputation language); citation counts present (16→20) | **FALSIFIED (partial)** — 2 of 4 named re-verification components missing from the round-9 LOG entry as written (see #9, #12 in Falsified summary) |
| 20 | freshness ceiling: "still no in-repo drift pin — a silent `:34113` model swap between rounds would be caught only by the next manual probe" | `grep -rn '34113' corpus/ *.md` for any pin script/hash | no drift-pin script or pinned hash in-repo (contrast `../kagi-shokunin/corpus/drift-pins.sh`, which exists with exit 0/1 plumbing — `grep -nE 'exit' …` → `return 1` on drift, `return 0` clean, `run()` selftest) | **REPRODUCES** |
| 21 | pre-move operability: "`git ls-tree -r f147a27 --name-only \| grep -cE '\.(py\|sh)$'` → **0** runnable files in-repo; the working commands lived outside it (`~/bench-arena/grade.sh` …) Contrast a sibling gate: `../kagi-shokunin/corpus/drift-pins.sh` (exit 0/1/2 + `--selftest`)" | `git ls-tree -r f147a27 --name-only \| grep -cE '\.(py\|sh)$'` → 0; `ls ~/bench-arena/grade.sh` → exists; `grep -nE 'exit' ../kagi-shokunin/corpus/drift-pins.sh` | 0 runnable files at f147a27; bench-arena grade.sh exists; drift-pins.sh has exit 0 (`DRIFT_PINS: CLEAN`) / 1 (`return 1` on drift) / 2 (arg errors) plumbing + a `run()` selftest harness | **REPRODUCES** |
| 22 | pre-move freshness: "`curl -s -m 5 http://127.0.0.1:34113/v1/models` → `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, `/health` → 200" | `curl -s -m 5 http://127.0.0.1:34113/v1/models`; `curl -s -m 5 -o /dev/null -w '%{http_code}' …/health` | model id matches byte-for-byte; `/health` → `200` | **REPRODUCES** |
| 23 | pre-move freshness: "`test -e ~/wikillm/llm-wiki` → still absent as `SKILL.md:8-12` states" | `test -e ~/wikillm/llm-wiki; echo $?` → 1; `git show f147a27:SKILL.md \| sed -n '5,15p'` | exit 1 (absent); f147a27 SKILL.md:8-12 documents the absence verbatim | **REPRODUCES** |
| 24 | pre-move depth: "`SKILL.md` 312 lines: 2 decision tables (`:17`, `:40`), 8 anti-patterns (`:47` block), a 9-step production checklist (`:274` block), telemetry parsing rules (`:170`), 16 `- ` cited-source bullets carrying 14 distinct `~/…` paths" | `git show f147a27:SKILL.md \| wc -l` → 312; `grep -c '^## Decision table'` → 2 at `:17,:40`; anti-pattern block → 8 items; checklist → 9 items; `sed -n '170p'` → "Parsing rules learned on real files:"; bullets → 16; distinct `~/…` paths → 14 | all six counts exact | **REPRODUCES** |
| 25 | pre-move depth: "the '20+ cited local sources' phrasing in `SHONEN.md` holds only under path expansion (16 bullets)" | `git show f147a27:SHONEN.md \| grep -n 'cited local sources'` → line 5 present | confirmed at f147a27 (and `review.md` §1 S1.2 independently flagged the same overreach) | **REPRODUCES** |
| 26 | pre-move coverage: "`PROVINCE.md` was 7 lines and enumerated **no** surfaces … the real enumeration lived in `corpus/README.md`'s coverage map" | `git show f147a27:PROVINCE.md \| wc -l` → 6; `grep -c ''` → 6; byte size 345; same 6-line shape back to `782dd2d`/`d5f1cad`/`91f021c`; `git show f147a27:PROVINCE.md` content = 3 prose lines, zero surface enumeration | **6 lines**, not 7 — every 6-line rendering (`wc -l`, `grep -c ''`, byte size) agrees; `wc -l`-vs-`grep -c ''` agreement rules out trailing-newline ambiguity | **FALSIFIED (count only)** — "was 7 lines" is off by one; substance (no surfaces, no enumeration) fully correct |
| 27 | pre-move coverage: "`grep -c '^| \`knowledge/' corpus/README.md` → 18 = 18 files on disk, but `grep -c '^| \`lessons/'` → **6 of 8** files (both aggregator-audit lessons unindexed), and `corpus/evidence/` (4 files) unindexed" | `git show f147a27:corpus/README.md \| grep -c '^| \`knowledge/'` → 18; `git ls-tree -r f147a27 --name-only \| grep -c 'corpus/knowledge/'` → 18; lessons rows → 6, files → 8; evidence rows → 0 | 18=18 exact; 6 of 8 lessons (both aggregator-audit lessons unindexed — confirmed via file list); 0 evidence rows at f147a27 | **REPRODUCES** |
| 28 | pre-move calibration (a): "No `SCORECARD.md` existed (`test -e SCORECARD.md` → MISSING at `f147a27`; `git ls-tree -r f147a27 --name-only \| grep -c SCORECARD` → 0)" | `test -e SCORECARD.md && echo EXISTS \|\| echo MISSING` — note: run at HEAD, so returns EXISTS; git-tree check is the decidable one | `git ls-tree -r f147a27 --name-only \| grep -c SCORECARD` → **0**; `git show f147a27 --stat -- SCORECARD.md` → empty | **REPRODUCES** (tree-level: absent at f147a27, created in 2575be6) |
| 29 | pre-move calibration (b): "`grep -ril predict /tmp/bench-r8 corpus/evidence/round8-horizon` → 0 hits, while rounds 5–6 did file them (`/tmp/bench-r5/predictions.md` 25 lines, `/tmp/bench-r6/predictions.md` 17 lines)" | `grep -ril predict /tmp/bench-r8 corpus/evidence/round8-horizon; echo exit=$?` → exit 1 (no matches); `wc -l` on the two prediction files | exit 1 (0 hits in r8 dirs — note: this is a **live-`/tmp`-dependent** command; it happens to hold today because `/tmp/bench-r8/` still exists with no predictions file; `grep -ril predict corpus/evidence/round8-horizon` → 0, `…round9-replication` → 4 hits); `/tmp/bench-r5/predictions.md` = 25 lines, `/tmp/bench-r6/predictions.md` = 17 lines | **REPRODUCES** (with the caveat that this claim's evidence is not hermetic — `/tmp`-dependent, exactly the operability ceiling the lane itself names) |
| 30 | pre-move calibration (c): "`grep -c -i 'round.8\|horizon' LOG.md` → 0; `git ls-tree -r f147a27 --name-only \| grep -c evidence` → 0 (4 files working-tree-only)" | `git show f147a27:LOG.md \| grep -c -i 'round.8\|horizon'` → 0; `git ls-tree -r f147a27 --name-only \| grep -c evidence` → 0; `ls /tmp/bench-r8` → 4 files (`critic-defects.md`, `horizon.py`, `results.jsonl`, `run.log`) | 0 and 0 confirmed at f147a27; exactly 4 files in `/tmp/bench-r8` today | **REPRODUCES** |
| 31 | calibration proxy (a): "(r8: 0/1; r9: 1/1)" probes with predictions filed before first request and scored at close | recompute above (#7, #8) + `grep -c 'round 8' LOG.md@f147a27` → 0 | r8: zero probes with predictions (0/1 ✓); r9: 1/1 ✓ (ordering proof + scoring both reproduce) | **REPRODUCES** |
| 32 | calibration proxy (b): "artifacts produced in the round that are committed and indexed and logged at round close (r8: 0/4 files; r9: see `git show --stat` for the round-9 commit)" | `git show --stat 2575be6` | 128 files listed including all evidence/knowledge/lessons lands; `LOG.md +4` in same commit; README index rows verified equal to files (#17) | **REPRODUCES** |
| 33 | calibration proxy (c): "`SCORECARD.md` rows whose evidence pointer re-runs (target 7/7)" | per-row execution throughout this artifact (rows 1–33) | post-move rows: calibration/novelty/operability/depth/coverage/freshness/adjacency pointers re-run or re-derived with **2 falsifications** (rows 1, 4) + 1 partial falsification (row 19) | **FALSIFIED (partial)** — measured against the 7 post-move rows, 5 fully
re-run (calibration, novelty, depth, coverage, adjacency), 1 carries two
falsified pointers (operability: rows 1, 4), 1 carries a falsified
LOG-completeness claim (freshness: row 19). So the measured proxy is 5/7,
not the 7/7 target. |
| 34 | novelty proxy: "fraction of the round's headline claims carrying a prior-art verdict with a fetched URL (r9: 4/4, see `corpus/knowledge/eval-prior-art-calibration.md`), split into phenomenon-new vs instrument-new (r9: 0/4 phenomena, 2/4 instruments)" | read `eval-prior-art-calibration.md` verdict table; spot-fetch two cited URLs | 4/4 findings with URLs (arXiv links live: `2505.06120` → 200, GitHub issue → 200); "0/4 phenomena" = all four marked known/incremental at phenomenon level; "2/4 instruments" = probe A + probe C rows in the coverage table | **REPRODUCES** |
| 35 | adjacency row: "Contested scope mapped with named owners and three report-outs filed … Prompt-format craft → kotoba; ledger split → kasegi/kumitate; Janitor → kagi, serving plane escalated as unowned" | `grep -c 'kotoba\|kasegi\|kumitate\|kagi' corpus/evidence/round9-fleet/sibling-overlap.md` → 18; `PROVINCE.md` §Reported out lists the 3 report-outs | matches exactly; `../ROADMAP.md:80-81` confirms the kama mint demand-instance framing | **REPRODUCES** |

---

## Falsified claims — count: **3** (2 full, 1 partial)

| # | Claim (verbatim fragment) | Why falsified |
|---|---|---|
| F1 | operability post-move: "Runnable files in-repo went **0 → 11** (`find … \| wc -l` → **11**)" | Re-run at HEAD 1bd17ec → **12**; re-run at the round-9 commit 2575be6 → **12**. The `find` command as written returns 12 at both refs; the same 12 files exist in `git ls-tree -r 2575be6` and in the working tree. The SCORECARD's own planned-move section then requires `≥ 12`, which the stale "11" makes the falsifiable target look unmet when it is in fact met. Matches L1's independent count. |
| F2 | operability post-move Evidence cell: "`/tmp` → repo copy check `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`" | Fails from repo root: `predictions-r9.md: FAILED open or read`, exit 1. The `.sha256.repo` file names `predictions-r9.md` relative to the **checksum file's** directory, and `sha256sum -c` resolves it relative to the **caller's cwd**, not the file's. Passes (exit 0, `OK`) when run from `corpus/evidence/round9-replication/`. The number is right; the pointer as written is stale/broken from the stated run location. Note: `corpus/README.md:57-59` documents the correct invocation (`cd corpus/evidence/round9-replication && sha256sum -c …`), so the SCORECARD cell is the one place that states it wrong. |
| F3 | freshness post-move: "The round-9 LOG entry carries re-verification results for every claim it touches: endpoint identity …, **evidence md5s**, the **r8↔r9 SUMMARY recomputation from committed bytes**, and citation counts" | 2 of the 4 named components are not in the round-9 LOG entry (L14): (i) no md5 strings for the four r8 evidence files appear in L14 (`grep -oc 1c157e2a\|df154cb5\|fc3b232f\|3386406` → 0; `df154cb5` occurs only in L13's round-8 retrospective); (ii) no recomputation language exists in L14 (`recomput*` → 0 hits in the whole of LOG.md; L14 has only the bare r8↔r9 ladder numbers `A-INC 7/10 > A-CKPT 1/10 ≈ A-MONO 0/10, 9/10 under convention-tolerant grading…`, which are quoted numbers, not a recomputation). Endpoint re-verification and citation counts are present and re-run clean (#22, #13). |

Partial-falsification note on #33 (calibration proxy (c), "target 7/7"): the
SCORECARD words this as a *target*, not a measured result, so it is not scored
as a falsification above; measured, it is 4/7 post-move rows fully re-running,
2 with falsified commands/numbers (operability ×2), and 1 with a falsified
LOG-completeness claim (freshness). If the target is read as a claim of
achievement rather than an aim, this is a fourth falsification.

---

## Verdict summary

- Rows re-run or re-derived: **35** claims extracted, all commands executed
  from repo root unless noted (row 4 also re-run from the replication dir to
  isolate the cwd bug; row 4b `cd corpus/evidence/round9-replication &&
  sha256sum -c predictions-r9.sha256.repo` → `predictions-r9.md: OK`, exit 0).
- **REPRODUCES: 30** — including all four r9 SUMMARY cells (4/8 0.500,
  2/8 0.875, 2/8 1.375, 0/8 2.250), all paired sign-test rows (p = 0.500 /
  1.000 / 0.500 / 0.125), onset 5.8, ack-compliance 57.1%/75.0%, the r8
  SUMMARY 7/0/1 · 3/3/6/6 · 4/1/4/4, FIX-O = 1 record, 78/78 jobs, 268/284
  record counts, 258/258 `raw`, md5s byte-identical to the live `/tmp`
  artifacts, SKILL/README/PROVINCE census counts, endpoint identity + health,
  ordering proof, prediction scoring (2/4 hits, MAE 0.09375→0.094, falsifiers
  unfired, onset 5.0 vs 5.8).
- **FALSIFIED: 3** (2 full, 1 partial):
  1. Runnable-files count `0 → 11` — actual **12** at HEAD and at 2575be6
     (`find … | wc -l` → 12; `git ls-tree -r 2575be6 --name-only | grep -cE
     '\.(py|sh)$'` → 12). This also matters for the planned-move target
     (`≥ 12` runnable files AND a hermetic grader): the ≥12 half is in fact
     already met; the grader half (`ls grader.py` → absent at audit time) is
     the piece still owed by this round.
  2. `sha256sum -c …predictions-r9.sha256.repo` from repo root — exit 1
     (relative-path bug; correct invocation documented in
     `corpus/README.md:57-59`).
  3. Freshness row's LOG-completeness claim — "evidence md5s" and "the r8↔r9
     SUMMARY recomputation from committed bytes" are not in the round-9 LOG
     entry. Measured against the 7/7 re-run target in calibration proxy (c),
     the post-move table delivers **5/7** (operability ×2 defects, freshness
     ×1; the other five rows fully re-run).
- **STALE vs FALSIFIED ruling:** row 1 (the 11-count) is wrong *at birth*:
  the SCORECARD was committed inside 2575be6 together with `replicate.py` and
  `run_r9.py` (the 11th and 12th `.py`/`.sh` files), so the tree it claims to
  measure already contained 12 runnable files at that very commit — this is a
  count error, not a later drift. Row 4 (the sha256 pointer) states the wrong
  working directory; the correct invocation is documented one file away
  (`corpus/README.md:57-59`), so the pointer is stale/ambiguous rather than
  the underlying bytes being wrong. Row 19's md5/recomputation phrasing
  describes work that exists (L13 carries the md5s; the r8↔r9 ladder
  comparison lives in `round9-fleet/review.md` §4 "LOG.md ↔ artifacts") but
  not in the location the freshness row cites. All three are fixed-count
  defects, not interpretation disputes.

**Method note:** all counts in rows 1, 17, 24, 26, 27, 30 cross-checked twice
with distinct commands (e.g. `wc -l` vs `grep -c ''` vs byte size for the
PROVINCE 6-vs-7 line count; `find | wc -l` vs `git ls-tree | grep -c` for
runnable files) so that no single tool's quirk decides a verdict.

**Cross-corroboration (round-10 batch):** MutationHarness's independent
grader-oracle probe (local://r10-mutation-sh.md) reproduced onset=5.8 from a
third path: the first landed grader.py failed its own M0 control with
`MISMATCH r9.onset.predicted_vs_observed: stored='5.0 predicted'
recomputed='5.8 observed'` before L1 pinned the delta as an erratum —
consistent with my recompute (`[None,2,7,7,3,10,None,None]` → 5.8) and with
the SCORECARD's own "5.0 predicted vs 5.8 observed" wording.

**Post-audit note:** after this artifact was finalized, `grader.py` landed
untracked in the working tree (mtime 19:22, 41,912 bytes). Working-tree
runnable-file count is therefore now 13; this does not affect F1, whose
verdict is anchored at the SCORECARD's own commit (2575be6 tree = 12) and at
HEAD-at-audit = 12. `git status --porcelain` → only `?? grader.py`.

**Scratch scripts (kept):** `/tmp/kengaku-r10/recompute_r9.py`,
`/tmp/kengaku-r10/recompute_r8.py`, `/tmp/kengaku-r10/test_harness.out`.
