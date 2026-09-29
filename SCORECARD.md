# kengaku-shokunin — Scorecard

Domain: LLM/model research & evaluation (`~/Projects/webzites/repos/llm-wiki`,
route telemetry, local eval harnesses). Lane axes per `../MISSION.md`:
**novelty + calibration**. The six `../AXES.md` axes are scored in the same
table because every round-move so far has been an eval-artifact move; the owned
pair is listed first and drives the round.

**Recorded sub-axis mapping** (required because `grep -n novelty ../AXES.md` →
0 hits while `../MISSION.md:14` assigns it, per
`corpus/lessons/round-6-aggregator-audit.md` defect 5): `novelty` is scored here
as *does this lane produce a measurement no other province can, whose instrument
is inspectable in-repo, and whose claim survives a prior-art check with a
fetched URL?* — operationalized by the fixed novelty proxy below, so the score
is re-derivable rather than a vibe. Routed to the protocol lane: either add
`novelty` to `../AXES.md` or ratify this mapping; until then the mapping in this
file is the definition of record for this repo.

Scoring method (matches `../kagi-shokunin/SCORECARD.md`, the most complete
fleet example per `corpus/evidence/round9-fleet/sibling-overlap.md` §3): a
score is the strength of a *verifiable* claim about this repo, not a feeling
about the domain. Every cell carries a re-runnable command or a committed path,
and names its own ceiling — an unqualified high score is the calibration
failure this file exists to prevent.

Measurement proxies (fixed so before→after is re-derivable, per
`../kasegi-shokunin/SCORECARD.md`):

- **calibration proxy** — three counts: (a) probes run in the round with
  predictions filed *before the first request* **and** scored at close
  (r8: 0/1; r9: 1/1; r10: 0/0 — hermetic round, no probe ran; r11: **1/1** —
  bundle hashed 23:10:20Z, run scripts hashed post-fix 23:28:37Z, first
  `request_ts` 23:28:57Z; scored at close: point abs-errors 0.219/0.125/0.002,
  Brier 0.153); (b) artifacts produced in the round that are committed
  **and** indexed **and** logged at round close (r8: 0/4 files; r9: see
  `git show --stat` for the round-9 commit; r10: `grader.py` + 22 files under
  `corpus/evidence/round10-fleet/`; r11: `round11-power/` (12 files) +
  `round11-fleet/` (17 files) + 2 corpus entries + the extended `grader.py`,
  all indexed in `corpus/README.md` and logged — see the round-11 commit
  stat); (c) `SCORECARD.md` rows whose evidence pointer re-runs (target 7/7;
  r10 critic: 30/35 → 3 errata filed; r11 wave-2 critic: landed numbers
  10/10 REPRODUCE).
- **novelty proxy** — fraction of the round's headline claims carrying a
  prior-art verdict with a fetched URL (r9: 4/4, see
  `corpus/knowledge/eval-prior-art-calibration.md`; r10: 0/0 — a hermetic
  round made no model-behaviour claims; r11: **7/7** — C1–C4 + M1–M3,
  `corpus/evidence/round11-fleet/r11-prior-art-{granularity,prereg}.md`),
  split into phenomenon-new vs instrument-new (r9: 0/4 phenomena, 2/4
  instruments; r10: n/a; r11: 0/4 phenomena, **1/4 instruments novel** — C3
  density-ablation instrument; C4 prereg+gate composition INCREMENTAL).

## Round 9 — pre-move (measured against `HEAD` `f147a27` "round-7")

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| **novelty** *(owned)* | 7 (unpriced) | Round 8 opened a construct the 33-task bench-arena battery cannot see — multi-turn state maintenance — with a new instrument, not a re-run: `corpus/evidence/round8-horizon/horizon.py` (349 lines, md5 `1c157e2a…`) carrying a checkpoint protocol that removes the self-copy scaffold (`:126-162`), a 2×2 hint×clean grid (`:178-223`), and a `C-norule` baseline (`:246-262`). 78/78 jobs ran (`run.log:1-78`), 268 records. **Ceiling: unpriced** — before round 9 the lane had never checked any finding against public literature, so "novel" meant "not in this corpus". | round 8 |
| **calibration** *(owned)* | **2** | Four re-runnable breaches. **(a)** No `SCORECARD.md` existed (`test -e SCORECARD.md` → MISSING at `f147a27`; `git ls-tree -r f147a27 --name-only \| grep -c SCORECARD` → 0) although `../AXES.md:26-32` makes it a per-repo contract — 8 rounds of prose self-assessment, none scored. **(b)** Round 8 ran a 78-job probe with **no ex-ante predictions**: `grep -ril predict /tmp/bench-r8 corpus/evidence/round8-horizon` → 0 hits, while rounds 5–6 did file them (`/tmp/bench-r5/predictions.md` 25 lines, `/tmp/bench-r6/predictions.md` 17 lines) and `SKILL.md` checklist item 1 + anti-pattern 4 require them — a regression against the lane's own written rule. **(c)** The r8 probe was never analyzed, logged or committed: `grep -c -i 'round.8\|horizon' LOG.md` → 0; `git ls-tree -r f147a27 --name-only \| grep -c evidence` → 0 (4 files working-tree-only). **(d)** The landed evidence copy had the `raw` field stripped from all 258 non-meta records (md5 `01547cfa…` vs run artifact `df154cb5…`), destroying the failure-class evidence while graded fields looked intact. Credit keeping it above 0: LOG.md rounds 4–7 do record negative results and prediction errors (`03` PASS→FAIL, "1/4 PASS vs predicted 2/4"). | rounds 1–8 |
| depth | 7 | `SKILL.md` 312 lines: 2 decision tables (`:17`, `:40`), 8 anti-patterns (`:47` block), a 9-step production checklist (`:274` block), telemetry parsing rules (`:170`), 16 `- ` cited-source bullets carrying 14 distinct `~/…` paths (commands: `awk '/^## Cited local sources/,0' SKILL.md \| grep -cE '^- '` → 16; `… \| grep -oE '~/[A-Za-z0-9_./{}*,+-]+' \| sort -u \| wc -l` → 14). 18 `corpus/knowledge/` entries, each opening with a source line. **Ceiling:** no planning-horizon/transcript-shape section despite r8 having run one; the "20+ cited local sources" phrasing in `SHONEN.md` holds only under path expansion (16 bullets). | round 7 |
| coverage | 5 | `PROVINCE.md` was 7 lines and enumerated **no** surfaces, while `../AXES.md:12` names "PROVINCE.md lists every surface" as the coverage signal; the real enumeration lived in `corpus/README.md`'s coverage map. Index completeness: `grep -c '^| \`knowledge/' corpus/README.md` → 18 = 18 files on disk, but `grep -c '^| \`lessons/'` → **6 of 8** files (both aggregator-audit lessons unindexed), and `corpus/evidence/` (4 files) unindexed. README's open-gap line "Planning-horizon coverage … unmeasured locally" was already false (78/78 ran). | round 7 |
| operability | 3 | **No gate, only probes.** `git ls-tree -r f147a27 --name-only \| grep -cE '\.(py\|sh)$'` → **0** runnable files in-repo; the working commands lived outside it (`~/bench-arena/grade.sh`, and the probe itself at `/tmp/bench-r8/horizon.py` — ephemeral, labelled debt), and the 9-step checklist is operator judgement with no exit code. Contrast a sibling gate: `../kagi-shokunin/corpus/drift-pins.sh` (exit 0/1/2 + `--selftest`). **Ceiling:** nothing in-repo could be run by a fresh agent to produce a verdict. | round 7 |
| freshness | 4 | Endpoint and host-path claims were re-verified by hand each round (`grep -o 34113 LOG.md \| wc -l` → 4 rounds), and re-verified again in round 9: `curl -s -m 5 http://127.0.0.1:34113/v1/models` → `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, `/health` → 200 (no drift since r4, per `corpus/evidence/round9-fleet/review.md` §3); `test -e ~/wikillm/llm-wiki` → still absent as `SKILL.md:8-12` states. **Ceiling:** round 8 recorded *no* re-verification (`grep -c 'round 8' LOG.md` → 0), and no in-repo pin exists to catch a silent `:34113` move. | round 7 |
| adjacency | 7 | `PROVINCE.md` names what it owns and refuses; cross-domain evidence was routed, not absorbed — the r4 endpoint-drift discovery is listed in `../ROADMAP.md` as one of two demand instances behind the **kama** mint candidate. **Ceiling:** the r8 C-cells (rule integration over fabricated transcripts) and the r7 scaffold ablation are prompt-craft evidence belonging partly to kotoba, and that overlap was unnamed anywhere in-repo. | round 4 |

## Round 9 — post-move (calibration axis-move landed)

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **calibration** | 2 → **6** | All four breaches closed: (a) this file exists with fixed proxies, a written ±1 rubric and re-runnable pointers; (b) the predict→observe→score loop is restored *with a mechanical ordering proof* — predictions hashed before the first request (`sha256 2a4f62ef…`, `ordering.log` 21:17:48Z, first `request_ts` 21:17:58Z) and scored at close (2/4 cell hits, mean abs error 0.094 of n, 4/4 directional falsifiers unfired, onset 5.0 predicted vs 5.8 observed); (c) the r8 debt is analyzed, logged and committed — 5 L2 analyses + a fix-landing audit + a 50-case harness mutation test; (d) the run artifact is landed byte-identical (`results.jsonl` `df154cb5…` with `raw` on 258/258 non-meta records, `run.log` `fc3b232f…`). Self-assessment was also downgraded where the evidence demanded it: novelty 7→5 after prior-art pricing, and the replication verdict is reported as **indeterminate** because the pre-registered threshold (INC ≥5/8) missed by one problem. **Ceilings:** forecasts are still point counts, not probabilities, so no Brier score exists yet (the lane has digested Tetlock scoring and did not use it — `corpus/knowledge/eval-design-digest-3.md`); nothing *enforces* the prediction gate, it is prose + a two-command ritual; all `SHONEN.md` boxes are `[~]` author-asserted because no non-author verifier exists (a dispatched subagent is still the lane, `../PROTOCOL.md` promotion gates); rounds 1–7 have no scored predictions retroactively. | this file; `corpus/knowledge/bench-arena-round9-replication.md`; `corpus/evidence/round9-replication/{predictions-r9.md,predictions-r9.sha256.repo,ordering.log,results-r9.jsonl}`; `corpus/knowledge/bench-arena-round8-horizon.md`; `md5sum corpus/evidence/round8-horizon/*` |
| **novelty** | 7 → **5** | Priced against public literature for the first time: one scout L2 with in-session fetches of every primary graded **3 of 4** round-8 findings known/incremental and the non-iid-draws finding a *direct replication* of llama.cpp issue #7052 (2024, same prompt + seed at temp 0 across 8 slots → 5–8 unique completions). What survives is instrument-level: no named suite ablates **emission granularity** on identical problems/seeds, and none runs a **vacuously-satisfied** late rule against matched binding/no-rule controls. The r9 dose cell (`A-CKPT710`) added a measurement r8 could not make — a 3-point granularity ladder — but it returned a tie (2/8 = 2/8), so it bought severity resolution (`nwrong` 0.875→1.375), not a pass-rate dose response. **Ceiling:** both novel instruments are under-powered (C at 4 reps / 1–2 distinct generations; B well-formed in 2/8 corruptions), so neither is publishable as a finding yet; every cell is a sub-3-bit + llama.cpp observation, not a model-capability measurement. | `corpus/knowledge/eval-prior-art-calibration.md`; `corpus/evidence/round9-fleet/prior-art.md`; `corpus/knowledge/bench-arena-round9-replication.md` §"Observed" |
| operability | 3 → 4 | Runnable files in-repo went 0 → 11 (`find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' \| wc -l` → 11), and one self-verifies offline: `python3 corpus/evidence/round9-fleet/test_harness.py` → exit 0, 50 cases, `38 PASS / 12 defect candidates`, blast radius recomputed from the committed `results.jsonl` (`FIX-O` flips exactly 1 record). **Ceiling:** these are evidence scripts, not gates — none exits nonzero when a stored SUMMARY disagrees with a recomputed one, and the probes still require the live endpoint. | `corpus/evidence/round9-fleet/test_harness.py`; `/tmp` → repo copy check `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo` |
| depth | 7 → 8 | Three sourced knowledge entries added (r8 probe analysis with per-cell tables, failure-class splits and a 16-defect fix-landing audit; r9 pre-registered replication with scored predictions; prior-art calibration with fetched URLs), and `SKILL.md` grew 312 → **414** lines: anti-patterns 8 → **13**, a new §"Planning-horizon & transcript-shape probes" (cell-semantics table + 9 measurement rules), the prediction-ordering gate in checklist item 1, cited-source bullets 16 → **20**. Three errata appended in place of in-place rewrites (`bench-arena-round7-noise-n25.md` `0/12`→`0/17`, `lessons/round-5.md` flip→delta terminology, `ledger-route-telemetry.md` 7,218→7,224 drift + counting command). **Ceiling:** the 3-source digest queue (Laban ICLR 2026, Lanham 2023, llama.cpp #7052) is named but unread. | `corpus/knowledge/bench-arena-round8-horizon.md`, `…round9-replication.md`, `…eval-prior-art-calibration.md`; `SKILL.md` §Planning-horizon; `grep -c '^## Decision table' SKILL.md` → 2 |
| coverage | 5 → 6 | `PROVINCE.md` now enumerates 8 surfaces (all resolving) with refusals and 3 named report-outs; README index completed in both directions — 21 knowledge rows = 21 files, 11 lessons rows = 11 files (the 11th, `round-6-aggregator-audit.md`, is aggregator-owned and committed by the aggregator per `../PROTOCOL.md`; this lane writes only the index row) — plus a new `evidence/` section covering all 3 evidence dirs; the false "planning-horizon unmeasured" gap line replaced with the measured state and its limits. **Ceiling:** the non-karpathy `wiki/ai/` topics beyond eval scope remain undigested, and the served-model surface (`:34113` flags: `--cont-batching`, `-np`) is documented from behaviour, never from the process cmdline. | `PROVINCE.md`; `corpus/README.md` §§What's here / evidence / Coverage map / Open gaps; `grep -c '^| \`lessons/' corpus/README.md` → 11 = `ls corpus/lessons \| wc -l` |
| freshness | 4 → 5 | The round-9 LOG entry carries re-verification results for every claim it touches: endpoint identity (`/v1/models`, `/health` 200), evidence md5s, the r8↔r9 SUMMARY recomputation from committed bytes, and citation counts. The r8 hole is closed retrospectively rather than left as a silent gap. **Ceiling:** still no in-repo drift pin — a silent `:34113` model swap between rounds would be caught only by the next manual probe. | `LOG.md` round-8/round-9 entries; `corpus/evidence/round9-fleet/review.md` §3 |
| adjacency | 7 → 8 | Contested scope mapped with named owners and three report-outs filed instead of absorbed: prompt-format craft implications → kotoba; ledger semantics split (mission-state → kasegi, route resolution/failure taxonomy → kumitate) → those lanes; Janitor consumer endpoint config → kagi, with the serving plane escalated as unowned. Kengaku keeps model/endpoint capability interpretation and eval design. **Ceiling:** the ruling is this lane's reading of sibling provinces plus the round-3/4 aggregator precedents; the integrator has not arbitrated it in round 9. | `corpus/evidence/round9-fleet/sibling-overlap.md`; `PROVINCE.md` §Reported out |

## Round 10 — errata to round-9 rows (measured against `HEAD` `1bd17ec`; critic L2 adversarial re-run)

The round-10 critic re-ran 35 backticked pointers/numbers from the round-9
tables: **30 REPRODUCE, 3 falsified** (2 full + 1 partial). All three are
recorded here as errata, never patched in place
(`corpus/evidence/round10-fleet/r10-critic.md`):

- **F1 — operability row "Runnable files in-repo went 0 → 11".**
  `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` →
  **12** at HEAD *and* at the round-9 commit `2575be6`
  (`git ls-tree -r 2575be6 --name-only | grep -cE '\.(py|sh)$'` → 12; → 0 at
  `f147a27`, so the row's *before* half was right). Wrong at birth: `2575be6`
  committed `replicate.py` + `run_r9.py` in the same commit as this scorecard;
  which file was the 12th past the "11" measurement is unrecorded.
  Consequence: the `≥ 12` half of the old §Planned target was satisfied before
  round 10 began; the binding half was the exit-code pair.
- **F2 — operability evidence cell
  `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo`**
  exits **1** from the repo root (`predictions-r9.md: FAILED open or read`) —
  the `.repo` file names a bare relative path and `sha256sum -c` resolves
  against the caller's cwd. From `corpus/evidence/round9-replication/` it
  exits 0 (the README documents that invocation; this file's cell was the one
  wrong statement of it). Bytes were never in doubt (sha256 `2a4f62ef…`
  matches). The check is now hermetic and cwd-independent inside `grader.py`
  (`r9.ordering.prediction_sha256`).
- **F3 (partial) — freshness row "the round-9 LOG entry carries … evidence
  md5s, the r8↔r9 SUMMARY recomputation".** LOG.md L14 carries the endpoint
  identity and citation counts, but the evidence md5s sit in L13 and
  `recomput*` has 0 hits in all of LOG.md (the SUMMARY recomputation lives in
  `corpus/evidence/round9-fleet/review.md` §4) — the row over-claimed *where*
  the re-verification lived. The round-10 LOG entry carries the recomputation
  itself (grader checks `r8.summary.*`, `r9.observed.*`).
- **Path drift in the same cell**: the old §Planned named the grader source as
  `corpus/evidence/analyze.py` — `test -e` → absent; the analyzer on disk is
  `corpus/evidence/round9-fleet/analyze.py`, and the promoted gate landed at
  repo root as `grader.py` (lineage in its docstring).
- **Adjudicated evidence erratum found while building the grader**:
  `replication.md` §Onset-and-failures stores state errors "12/32" at the r9
  final graded turn; recomputation from the committed `results-r9.jsonl` gives
  **24/32** (final passes 4+2+2+0 = 8/32, parse failures 0/32). `grader.py`
  pins the pair as `ERRATA["r9.failure_classes.state_error"]` — the check
  passes iff the stored text still shows 12/32 AND the recomputation equals
  24/32, so editing either side without a recorded ruling fails the gate.
  `replication.md` gained an appended §Errata; its md5 pin moved
  `a70980a5…` → `d9235e41…` (appendix-only change, recorded in LOG). The "12"
  provenance (checkpoint cells' 6+6 over the all-cells denominator) is
  conjectural; the corrected value is arithmetic on committed bytes.

## Round 10 — post-move (operability axis-move landed)

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **operability** | 4 → **6** | The repo now produces verdicts. `grader.py` (repo root, 936 lines, sha256 `ce64f16a…`, stdlib only, no endpoint, byte-identical output under `PYTHONHASHSEED` 1/99/unset) replays both committed probe trees offline: metas regenerate from their seeds (r8 `700+pid*13` 10/10; r9 `2000+pid*29` 8/8, incl. the `+977` retry chain); every graded record (r8: 140 A + 32 B + 16 C; r9: 128 A) is re-parsed from its stored `raw` through the shipped `extract_json_block` — including the brace-regex fallback that 2 r9 records need — and re-graded against meta-derived truth (A/B/C graders ported verbatim from `horizon.py`); all 11 `run.log` SUMMARY lines and every stored number in `replication.md` recompute (observed table, 284-record census, exact-binomial sign tests, onset ladder, failure classes, ack compliance, cross-round table, prediction-scoring table vs `predictions-r9.md`, sha256 chain, ordering proof). `python3 grader.py` → **exit 0, `CHECKS n=149 mismatches=0`**; `--selftest` → 4/4 PASS asserting exit code **and** expected check-id (kagi convention per the connector survey); the independent mutation battery (written by an L2 *before* the grader existed, `mutate_test.sh` sha256 `ad0511f2…`) → M0 control exit 0, M1 stored-`ok` flip exit 1 with exactly `r8.replay.A-INC.ok` firing (layer isolation proven: the flip is summary-insensitive because SUMMARY counts last-graded-turn oks), M2 SUMMARY edit exit 1, M3 `raw` corruption exit 1 → **4/4**. md5 pins on the 4 evidence files fire on default paths only. **Ceiling:** the gate covers the two *committed* runs, not future probes — nothing yet forces a new run to land gradeable; `test_harness.py`'s 12 defect candidates stay open; the probes themselves still need the live endpoint. | `grader.py`; `corpus/evidence/round10-fleet/{final-harness.log,mutate_test.sh,r10-critic.md,r10-connector.md,INTEGRATOR-NOTES.md}`; `LOG.md` round-10 entry |
| **calibration** | 6 → **7** | The loop bit its own tail honestly. (a) The critic re-run falsified 3 round-9 pointers (F1/F2/F3 above) and all three were filed as errata in-round instead of patched in place; 30/35 reproduced, including every r9 SUMMARY cell, sign test, onset 5.8, ordering proof, r8 SUMMARY, FIX-O blast radius (=1 flip), and md5 identity with the live `/tmp/bench-r8` bytes. (b) The grader's *first landed version failed its own M0 control* (a bogus `predicted_vs_observed` equality check treating a predicted miss as a mismatch) — caught by the independent harness, failing-before evidence committed (`r10-mutation-sh.md` §7.1, `INTEGRATOR-NOTES.md` §2), fixed by replacing it with a preregistration-anchor check. (c) A stored number no one had ever recomputed (state error 12/32) was recomputed, adjudicated defective, appended as `replication.md` §Errata and pinned as an erratum pair that cannot silently drift in either direction. (d) No probe ran, so the ex-ante-prediction proxy is 0/0 — vacuous, not virtuous. **Ceiling:** proxies (a)/(b) only bite on probe-running rounds; the ±1 rubric is two rounds old and still judgement-anchored. | `corpus/evidence/round10-fleet/{r10-critic.md,r10-mutation-sh.md,INTEGRATOR-NOTES.md}`; `grader.py` `ERRATA`; `replication.md` §Errata |
| freshness | 5 → **6** | Every surface re-verified **with committed captures**: endpoint `/v1/models` + `/health` 200 plus the first process-level pin (pid 1299, `/proc/<pid>/cmdline` == `qwen-coder.service` ExecStart, 41 tokens EXACT_MATCH; `--cache-type-k/v q4_0`, `--kv-unified`, `--parallel 2`, `--no-context-shift`, custom non-upstream chat template — closing the PROVINCE "documented from behaviour, never from the process cmdline" ceiling); bench-arena frozen since 2026-08-29 (`find -newermt '2026-09-28 18:00'` → empty) with its 3 load-bearing claims re-derived — 2 REPRODUCE, the telemetry-NULL causal chain DRIFTED (`loop.sh` 5-fields-into-6-vars bug makes `source=journal` unconditional; `curl -fsS :8080/metrics` exits 0 today) and the "97 label dirs" count stale (125) → errata appended to both knowledge files; llm-wiki unchanged (git `e66e614`; mtimes wholesale-touched, unusable); 23/23 corpus URLs HTTP 200; expected values now pinned **in-repo** (`grader.py` `PINS`) — closing the "expected values pinned outside the repo" cap. **Ceiling:** pins cover the 4 evidence files, not surface states; no automatic re-run schedule exists. | `corpus/evidence/round10-fleet/{r10-scout-endpoint.md,models-34113.json,props.json,slots.json,r10-scout-bench.md,r10-scout-wiki.md,url-status.txt}`; `PROVINCE.md` served-model row; knowledge-file errata |
| coverage | 6 → **7** | `PROVINCE.md` enumerates **9 surfaces** (new In-repo-gate row) and all resolve; the served-model row carries the process-level pin; the round-10 fleet dir is indexed (README evidence table, 4th row: 22 files). The digest-queue ceiling was reclassified by evidence, not by work: the 3 queued sources are **external** (arXiv 2505.06120, arXiv 2307.13702, llama.cpp #7052), already fetched-and-cited in `eval-prior-art-calibration.md` (zero-trace grep proves they were never llm-wiki-resident), and llm-wiki itself gained no eval-relevant file since round 9 — so the queue is "fetched, partially digested, precisely classed", not "named-but-unread in the wiki". **Ceiling:** non-karpathy `wiki/ai/` topics beyond eval scope remain undigested; the queue's full digestion is still owed. | `PROVINCE.md`; `corpus/README.md` evidence rows; `corpus/evidence/round10-fleet/r10-scout-wiki.md` |
| **novelty** | 5 → **5** | No move — deliberately. A hermetic round measures the corpus, not the model: the grader is instrument *infrastructure* (it makes future novel measurements auditable and caught one real defective number), but adds no new construct and no prior-art verdicts (proxy 0/0). Stays the table's floor and the next move. | this table; §Planned |
| depth | 8 → **8** | Held, no bump — anti-double-count ruling: SKILL.md grew 414 → **472** lines (§Hermetic grader, anti-pattern **14**, serving-stack process-pin paragraph), but those bytes document this round's operability artifact; counting them under depth too would reward the same landing twice. Citation resolution re-measured **91.2% strict / 98.0% repo-convention — the ≥90% rubric floor holds** (20 cited-source bullets reproduce; the "14 distinct paths" figure ruled convention-bound: 58 distinct local paths under the finer extractor, 57 resolve, 1 documented-absent). Two knowledge entries lack a first-line source (`bench-arena-round7-scaffold-ablation.md`, `eval-design-digest-3.md`) — named, unfixed. **Ceiling:** the depth rubric's +1 wants new *sourced claims*; round 11's probe should supply them. | `corpus/evidence/round10-fleet/r10-review-cites.md`; `SKILL.md` |
| adjacency | 8 → **8** | The connector survey ruled the gate space: **no sibling owns an evidence-replay gate** (kagi `drift-pins.sh`/`transcript-scan.sh` = live-host drift + runtime hygiene; kotoba `verify_harness_claims.py` = live-baseline; kumitate `scripts/cite-check.mjs` = citation pins — adjacent, different data, ruled non-duplicate); a fleet-wide gate *standard* would belong to protocol/integrator — referred in the round report, not imposed. Three round-10 report-outs filed (`PROVINCE.md` tail): serving-plane config facts (q4_0 KV, `--kv-unified`, `--no-context-shift`) → integrator, unowned plane; `loop.sh` telemetry-source semantics → kumitate (informational; fix stays in-lane backlog); operator read-only rule for domain repos re-confirmed and absorbed. **Ceiling:** the integrator has still arbitrated neither the round-9 nor the round-10 rulings. | `corpus/evidence/round10-fleet/r10-connector.md`; `PROVINCE.md` tail |

## Round 11 — post-move (novelty axis-move landed)

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** | 5 → **6** | The floor moved for the first time. r9's indeterminate granularity reading (pass-rate tie 2/8=2/8, weak severity signal, underpowered by its own report) is now a **powered, preregistered, priced** result: the emission-granularity severity dose is **ESTABLISHED** — paired Δ mean `nwrong` at shared checkpoints {7,10} = **+0.352** (sd 0.820, n=64), t=+3.431, df=63, two-sided p=0.0011, 95% CI [+0.147, +0.556]; exact sign test 26W/7L/31T p=0.0013 (direction agrees → mechanical verdict-rule branch 1, no downgrade). All three novelty-rubric +1 legs: a construct r9 could only call indeterminate, now measured at the filed power (n=64, MDE d=0.35); the instrument inspectable in-repo (`probe_r11.py`, `run_r11.py`, `recompute_r11.py`, grader extension); prior-art verdicts with fetched URLs for every headline claim (proxy 7/7 — C1 severity-only dose INCREMENTAL-low: no source FOUND in the search set manipulates emission density with severity as the response; C3 instrument NOVEL ruling stands strengthened; C4 INCREMENTAL). Pass-rate dose **not** established (McNemar b=13 c=5, exact p=0.0963 — reported as the honest null). **Ceiling:** one instrument family (third-generation ladder), one served stack (q4_0 KV + custom template, descriptors-pinned in-band), one task family (inventory ledger); the phenomenon stays adjacent to published decoupling results (StageIF 2609.08589); "no published density manipulation" is a search-set verdict, not an exhaustive negative. | `corpus/evidence/round11-power/analysis_r11.md` (`PREREGISTERED VERDICT: ESTABLISHED`); `python3 grader.py` → exit 0, n=280; `round11-fleet/r11-{critic-landed,prior-art-granularity,prior-art-prereg}.md` |
| **calibration** | 7 → **8** | The full loop ran under its own gate. (a) Predictions filed before the first request and scored at close: bundle (plan+power+predictions) hashed **23:10:20Z**, run scripts hashed post-fix **23:28:37Z**, first `request_ts` **23:28:57Z** — the ordering chain covers the code that ran, not just the text. (b) Probabilistic predictions filed for the first time, lifting the rubric's "point forecasts where probabilities are feasible" cap: 3 events, **Brier 0.153**, dominated by the honest 0.50 on significance (outcome 1 → 0.25 term). (c) The shrunk primary-endpoint point prediction landed near-exact (+0.350 predicted → +0.352 observed, abs err **0.002**); pass-level predictions missed high (0.219/0.125) and the miss is filed as a lesson (levels are batch-variable, contrasts travel). (d) Defects recorded, not hidden: the runner's missing `import json` (mock-smoke caught it pre-run; failing-before evidence preserved), the draft ordering check's over-strict first-request form (failed on real bytes; granularity-independent fix adjudicated in INTEGRATOR-NOTES delta 2), and six critic design-MINORs ruled as errata instead of editing the hashed bundle (incl. the power-table ceil breach: exact n=64.07, power at 64 = 0.7996 not ≥0.80). (e) Landed bytes `cmp`-identical to the run bytes, md5-pinned in `PINS`. Conditional-MAJOR contingency (error-record rule) never materialized: 0 errors. **Ceiling:** Brier over only 3 events; 0–10 anchors remain medium-confidence; P(significance)=0.50 was underconfident against p=0.0011. | `round11-power/{ordering.log,predictions-r11.md,analysis_r11.md}`; `round11-fleet/{INTEGRATOR-NOTES.md,r11-critic-design.md,r11-mock-smoke.md,r11-critic-landed.md}` |
| operability | 6 → **7** | The gate tripled scope in the same round the new bytes landed (closing round-10 §Planned clause (c) — recomputable AT landing, not a round later): `grader.py` 936 → **1709** lines, 149 → **280** checks, replaying **three** trees. r11 adds: meta regeneration 64/64 seeds (`3000+pid*41`), raw re-parse/re-grade of all 320 graded records (want==truth[turn−1]), the §4 census (1473/1409/0-errors), both `run.log` SUMMARY lines, every stored `analysis_r11.md` line (observed table, paired diff/sd, t/p via NR betai, CI, exact sign + McNemar, verdict-rule consistency incl. the downgrade clause, Brier, scoring table), descriptors serving-stack pins, and the bundle sha256 chain + ordering proof. `--selftest` grew S0–S3 → **S0–S6** (r11 ok-flip, r11 SUMMARY edit, stats anchors) → exit 0. Independent mutation battery: **11/11 killed**, incl. cross-tree isolation (r9-only mutation fires r9 ids, zero r11 ids) and guarded in-place swaps with md5-verified restore; stdout byte-identical under PYTHONHASHSEED unset/42. A committed mock server (`round11-fleet/mock_server_r11.py`) lets a stranger schema-smoke the probe with no endpoint. **Ceiling:** new data still requires the live endpoint; the gate grades committed bytes only. | `python3 grader.py` → `CHECKS n=280 mismatches=0 errata_pinned=1`; `--selftest` → S0–S6 ALL PASS; `round11-fleet/{r11-mutation.md,mutate_r11.sh,mock_server_r11.py}` |
| depth | 8 → **9** | New sourced, actionable content beyond this round's probe bytes: measurement rule **10** (report paired contrasts, never raw levels across batches — derived from committed r8/r9/r11 numbers on an unchanged stack), anti-pattern **15** (causal-order checks keyed on timestamp uniqueness false-fail at second resolution), checklist item 1 extended (filed power analysis + mock-smoked runner + in-band descriptors), §Hermetic grader rewritten for three trees/280 checks/S0–S6, cited-source bullets 20 → **23**; two new corpus entries (powered-rerun knowledge, round-11 lessons); three of the aggregator cold-run's four break points closed in SKILL (B1 cite path `models/models.jsonl`, B3 durable-descriptors pin note, B4 `min_stack` defined). Citation resolution **92.9%** under the round-10 convention (13/14; the 1 = documented-absent ledger path) — ≥90% floor holds; strict count 71.4% (convention-bound per the round-10 ruling). **Ceiling:** two knowledge entries still lack a first-line source (named r10, unfixed); strict-vs-convention spread persists. | `SKILL.md` (518 lines, 15 anti-patterns, 23 bullets, 10 measurement rules); `round11-fleet/r11-review-index.md` §5 |
| coverage | 7 → **7** | Held, no bump — a maintenance round with one honest negative. Index both-directions completed/extended: knowledge 22 rows = 22 files, lessons **13 rows = 13 files** (the missing 13th was the aggregator's box-3 cold-run lesson, committed `06cdc98` without an index row — this lane writes only the row, per the round-6 convention), evidence dirs 6 = 6; the stale "No in-repo gate" open-gap line (landed r10, never closed in README) fixed. PROVINCE enumerates both round-11 dirs. BUT the route-telemetry surface **no longer resolves**: `~/Projects/bounties/` went absent mid-round (resolved 23:32Z with a live count of 7,226 lines; gone by the review pass; no relocation found). A declared-but-unresolvable surface is a coverage cap — marking it ABSENT and routing it to kasegi keeps the file truthful, not covered. | `round11-fleet/r11-review-index.md` §1/§4; `corpus/README.md` rows; `PROVINCE.md` surfaces + report-out (4) |
| freshness | 6 → **7** | Every claim this round touched carries a re-verification: endpoint identity at round start AND **in-band at run time** (the `descriptors` record pins model id + pid 1299 + 41-token argv + temp/maxtok/system prompt inside committed bytes — the durable form of the r10 process pin, closing cold-run break B3); ReviewerBaseline re-ran **41 committed pointers → BASELINE GREEN** pre-landing (grader n=149 control, r9 ordering chain incl. the F2 cwd caveat, pid/argv EXACT_MATCH, bench-arena frozen); the ledger surface's mid-round disappearance was caught **within minutes** (23:32Z resolving → absent), documented with its timeline, and routed instead of left stale; landed md5s recorded at copy time and pinned. **Ceiling:** the disappearance is un-root-caused (operator-side host state, outside the province); bench-arena/llm-wiki drift checks remain manual per round. | `round11-power/results-r11.jsonl` descriptors record; `round11-fleet/r11-review-{baseline,index}.md`; `PROVINCE.md` row 15 |
| adjacency | 8 → **8** | Held, no bump — the mechanism ran, nothing was newly arbitrated. Connector re-verified the r10 no-duplicate ruling at current sibling HEADs (no sibling operates a hashed preregistration, power analysis, or Brier scoring; no sibling owns an evidence-replay gate). Four report-outs filed, evidence sent not absorbed: protocol (fleet preregistration-standard referral), kotoba (ack-compliance 49–65% under checkpoint schedules + spillover-ask craft evidence), integrator (q4_0-KV materiality for ANY cross-model number from :34113, with fetched PR #21038 tables), kasegi (bounty-ledger tree absence). **Ceiling:** the integrator has arbitrated none of the standing referrals (unchanged since r10). | `round11-fleet/r11-connector.md`; `PROVINCE.md` round-11 report-outs (1)–(4) |


## Rounds 12–14 — round-14 debt landing (novelty axis-move)

Rounds 12 and 13 produced work but did not commit, index, score, or log it.
Round 14 lands those bytes and independently re-measures the claims. Scores
move only when the evidence becomes durable; lateness remains a calibration
breach rather than being erased by the catch-up commit.

| Axis | Before → After | What moved | Evidence |
|---|---|---|---|
| **novelty** *(owned)* | 6 → **7** | The written +1 rule's three legs fire. **New construct:** one powered four-arm ordered density ladder returned `L=1773.0`, `z=+9.452`, `LADDER ESTABLISHED`; adding `A-CKPT10` separated emission sparsity from up-front batching (`MONO-CKPT10=+0.656`, `DISSOCIATION ESTABLISHED`). The second-family contrast is only `TRANSPORT DIRECTIONAL` at a 2/48 floor and is corroboration, not a separate novelty basis. **Inspectable instrument:** hashed plan/power/prediction bundle, `probe_r12.py`, `run_r12.py`, `recompute_r12.py` (165/165 selftest), and `grader.py` replay. **Priced:** C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument; all six carry fetched URLs and round-14 re-fetched 14 load-bearing URLs. Independent critic: 25/28 REPRODUCE, 3 PARTIAL, 0 FALSIFY. | `corpus/evidence/round12-ladder/`; `corpus/evidence/round14-fleet/{r14-critic-landed,r14-review-priorart,r14-landing-gate}.md`; `corpus/knowledge/bench-arena-round12-ladder.md` |
| **calibration** *(owned)* | 8 → **8 (held — breach recorded)** | The r12 loop itself was strong: predictions and run machinery hashed at 01:16:08Z before first request 01:19:59Z; 416 pass probabilities scored at close (Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`); point prediction `+0.3520 → +0.297` (abs error `0.055`). But rubric clause (d) requires analysis/index/LOG **in the round it ran**; r12 sat uncommitted through r13. Round 13 also omitted prior-art, connector, durable analysis, lesson, and closeout rows (G1–G6). Late landing does not buy the point. | `ordering.log`; `analysis_r12.md`; `r14-revenger-r13.md`; `lessons/round-14.md` |
| operability | 7 → **8** | The gate now replays four trees: 733 checks, 0 mismatches, S0–S7 all pass. It regenerates both r12 problem families, re-parses/re-grades 1,328 records, recomputes E1–E6 and forecast tables, verifies ordering/bundle hashes, and md5-pins r12 results, run log, and analysis. Round-14 mutation pass killed 4/4 fresh corruptions; r12's earlier fixture battery killed 18/18. | `grader.py`; `r14-mutation.md`; `python3 grader.py` |
| coverage | 7 → **7 (held)** | Index parity is restored: knowledge 23/23, lessons 17/17, evidence dirs 10/10; PROVINCE enumerates the r12–r14 trees and the benchmark relocation. No bump: the declared route-telemetry surface remains absent, so the rubric's unresolvable-surface cap still fires. | `corpus/README.md`; `PROVINCE.md`; `r14-scout-surfaces.md` |
| freshness | 7 → **8** | Round-14 re-verified every live surface it touched: model id and `/health` match; pid 1299 owns `:34113`; 41/41 argv tokens match the unit and r12 descriptors; q4_0 KV / `--kv-unified` / `--parallel 2` unchanged. The sweep also falsified the old `~/bench-arena` path and found the intact relocation at `~/archive/bench-arena`; living pointers were corrected. Bounties remains absent. | `r14-scout-surfaces.md`; `PROVINCE.md`; LOG round 14 |
| adjacency | 8 → **8 (held)** | Current sibling HEADs own none of the Page-trend instrument, per-problem Brier/BSS, hashed study bundle, checkpoint ladder, or four-tree replay gate. Ack-intent craft is routed to kotoba; closeout carry-over is routed to aggregator/protocol; no new serving-plane claim is absorbed. No integrator arbitration, so no bump. | `r14-connector.md`; `PROVINCE.md` report-outs |
| depth | 9 → **9 (held — anti-double-count)** | SKILL grew to 19 anti-patterns and 13 measurement rules, but those lines document this same probe. Counting them again would reward one landing twice. | `SKILL.md`; rubric |

### Round-12/14 errata and limits

- `analysis_r12.md` regeneration differs in exactly one provenance line
  (`/home/vgpnk/projects/...` stored vs `/home/vgpnk/Projects/...` current);
  every statistic matches. Its landed md5 is now pinned (`029c3bcd…`).
- The design hash strictly predates the first request. `main-run-launch` and
  first `request_ts` both serialize to `01:19:59Z`, so strict launch-before-
  request ordering is not observable at one-second resolution; only
  `launch <= first request` is proven.
- E2's stored McNemar `b=12,c=5` is transposed under the critic's explicit
  convention (`b=710 pass / 4710 fail` gives `b=5,c=12`). The unordered counts,
  p=`0.1435`, and verdict are unchanged.
- `r12-prior-art-transport.md` says “448 pass events” five times; the hashed
  plan amendment, prediction file, and analysis establish **416**.
- `r12-review-citations.md` calls a `/tmp` mock JSONL “committed”; only
  `mock_server_r12.py` landed. The real run and its mock/real endpoint
  separation remain independently verified.
## Scoring rubric

A move is ±1 per axis-move; the anchors below are what make a pointer true or
false, fixed here so later rounds score the same way instead of drifting.

| Axis | +1 when | Capped below 10 by |
|---|---|---|
| novelty | a probe measures a construct the lane could not previously observe, the instrument is inspectable in-repo, **and** the claim carries a prior-art verdict with a fetched URL | re-runs of known-shot batteries; a phenomenon already published (keep as replication, not contribution); a new construct measured below its own critic's pre-registered power ask |
| calibration | (a) predictions filed before the first request for every probe, (b) predictions scored against observed at close, (c) this file exists and every row's pointer re-runs, (d) every probe analyzed, indexed and logged in the round it ran, (e) landed artifact bytes match the run artifact | any unscored probe; any artifact that never reaches `LOG.md`/README; a landed copy whose bytes differ from the run without a recorded reason; point forecasts where probabilities are feasible; a claim reported as replicated when the pre-registered rule returned indeterminate |
| depth | a decision table/threshold is derived from a read source and a reader can act on `SKILL.md` alone; citation resolution stays ≥90% | counts growing without new sourced claims; a named-but-unread digest queue; scope explicitly declared unmapped |
| coverage | every surface the corpus *describes* is indexed **and** every index row exists on disk (both directions); `PROVINCE.md` enumerates surfaces that resolve | unindexed files on disk; declared-but-unresolvable surfaces; a gap line contradicted by an artifact already in the repo |
| operability | a command in the repo exits 0/1 with a verdict a stranger can run | operator-judgement steps producing no exit code; artifacts that live only in `/tmp`; scripts that need the live endpoint to say anything |
| freshness | each round's `LOG.md` entry carries a re-verification result for the claims it touched; host-path and endpoint citations re-resolve | a round with no re-verification line; expected values pinned outside the repo |
| adjacency | cross-domain evidence is named with its owner and routed, not absorbed | unruled overlaps; foreign scope silently pinned into this corpus |

## Planned (next axis-move)

The lowest owned axis is **novelty (7)**; advisory coverage is also 7 but is
held by an operator-side absent surface. Next novelty move: turn round 13's
clip-bounded ack-state observation into an uncapped, matched instrument for
**response-contract compliance versus state fidelity**. File a hashed design,
power analysis, per-problem probabilities, prior-art verdicts, and raw-capture
policy before traffic; compare matched ack-only and full-state asks on the same
problem/turn schedule; preserve uncapped raw so exact-state incidence is a
point estimate rather than `[0.047,0.125]`. Extend `grader.py` in the same
round. No novelty bump if prior art prices the construct as known, the filed
power floor is missed, or capture ambiguity remains. Coverage's independent
next action is not a probe: keep the route surface marked absent until an
operator restores or retires it.

## Retired

None. No cell scores 10 and no axis is a wrong fit.
Round-12–14 movement (landed round 14): novelty 6→7, operability 7→8,
freshness 7→8; calibration held at 8 because the work missed its in-round
landing contract; coverage held at 7 because route telemetry remains absent;
depth held at 9 by anti-double-count; adjacency held at 8 without integrator
arbitration.

## Confidence

- **Round 8 filed no ex-ante predictions** — high. `grep -ril predict` over
  both r8 probe dirs → 0 hits; `test -e /tmp/bench-r8/predictions.md` →
  MISSING; the r5/r6 prediction files exist (25 and 17 lines).
- **The landed r8 `results.jsonl` was a `raw`-stripped copy of the same run,
  now re-landed byte-identical** — high. Field-level diff: key-set delta
  exactly `{raw}`, 0 semantic differences over 268 records, measured
  independently three times (`round9-fleet/probeC.md`,
  `round9-fleet/harness-mutation.md`, L1). The stripped copy was
  working-tree-only (`git ls-tree -r f147a27 --name-only | grep -c evidence`
  → 0), so no committed byte-image of it exists; its md5 (`01547cfa…`) is
  recorded in `LOG.md`'s round-9 entry. `round9-fleet/probeB.md` §7 read the
  md5 mismatch as "a different execution" — falsified by that diff.
- **Round 9 predictions preceded the first request** — high. Hash + before/after
  timestamps + first `request_ts`, all committed; re-checkable without `/tmp`
  via `predictions-r9.sha256.repo`.
- **Citation and count proxies (16 source bullets / 14 distinct `~/…` paths;
  18+6 README rows vs 18+8 files pre-move)** — high for the commands as
  written, medium for comparability: the denominators are
  counting-convention-defined (`round9-fleet/review.md` §1 reports 21 distinct
  local paths under a finer extractor), so cross-round comparison must reuse
  the same command.
- **All 0–10 anchors** — medium. Each row rests on a re-runnable command, but
  the anchoring itself is judgement; the rubric above is its first written
  statement, so the pre-move numbers are calibrated against nothing earlier.
- **"kama mint rests partly on this lane's r4 evidence"** — medium. Quoted from
  `../ROADMAP.md`; the mint decision is integrator-pending, so it is adjacency
  evidence, not a ruling.
- **Grader PASS means the corpus agrees with itself, not that the model was
  good** — high. All 149 checks recompute stored-vs-derived from committed
  bytes; no check touches the endpoint or re-runs the model.
- **Erratum 12/32 → 24/32** — high for the arithmetic (passes 8/32, parse
  failures 0/32; reproduced independently by the critic's `recompute_r9.py`
  and by `grader.py`), conjectural for the *provenance* of the stored 12
  (checkpoint-cells 6+6 hypothesis, labelled conjectural in both pin sites).
- **Process-level endpoint pin** — high at capture time (argv == unit
  ExecStart EXACT_MATCH; `ss -ltnp` listener ownership). It is host state: a
  restart changes the pid; the committed captures are a round-10 fact, not a
  live guarantee, and the gate deliberately never reads `/proc`.
- **F1's cause ("wrong at birth; which file was 12th is unrecorded")** —
  medium. The count 12 at `2575be6` is git-verifiable; the instant the "11"
  was measured is not reconstructible from any record.
- **Bench-arena causal-chain erratum** — high for the mechanism (the `mok`
  field-count bug proven by running `loop.sh`'s own functions verbatim; 33/33
  journal rows; scrape exits 0 today); the *historical* state of port 8080 at
  r4 run time is not re-derivable, and the erratum claims only today's facts.
- **Unverified, carried open**: the endpoint scout's gguf-size Δ (on-disk
  10,333,691,040 B vs `meta.size` 10,327,717,888 B, Δ 5,973,152 B) — cause
  not proven, no 10 GB hash run (`r10-scout-endpoint.md` gaps).
- **r11 severity-dose ESTABLISHED verdict** — high. Three independent
  recomputations agree: the landed `recompute_r11.py`, the `grader.py` replay
  (280 checks, exit 0), and CriticLanded's fresh implementation (10/10
  REPRODUCE incl. a 40/40 raw re-parse spot check). The verdict is the
  mechanical application of the pre-request rule to the recomputed numbers.
- **Pass-level batch variability (r8 1/10, r9 2/8+2/8, r11 29/64+21/64 on the
  same pid-1299 stack)** — high for the observation (committed bytes, argv
  re-pinned in-band); medium for the attribution (burst/sampling state vs
  unmodeled drift; the stack's argv is identical across all three).
- **"No published density→severity manipulation" (C1/C3)** — medium. A
  search-set verdict (~45 queries, ~50 fetched sources across two scouts),
  not an exhaustive negative; wording scoped accordingly post-critic.
- **Brier 0.153** — high as arithmetic, low as a calibration measure: 3
  events, one term (the honest 0.50 on significance) dominates.
- **Ledger-tree absence** — high (`test -e` × paths + `find ~ -maxdepth 4`
  sweep, both this round); cause unknown — operator-side host state.
- **Novelty 6 anchor** — medium: it rests on the scouts' verdict taxonomy and
  the powered ESTABLISHED result, both single-round instruments.

- **Round-12 ladder verdict** — high for the stored arithmetic: promoted
  recompute, 733-check gate, CorpusDrafter's fresh implementation, and
  CriticLanded's independent implementation agree. CriticLanded scored 25/28
  REPRODUCE, 3 PARTIAL, 0 FALSIFY; partials are path-byte reproducibility,
  timestamp resolution, and McNemar b/c orientation, not the ladder verdict.
- **Novelty 7 anchor** — medium. The construct and instrument legs are powered
  and replayable; C3's NOVEL-instrument label is a bounded negative-search
  verdict, not registry proof. Fourteen load-bearing URLs re-fetched in round
  14 support the wording.
- **Round-12 ordering** — high for hash-before-request
  (`01:16:08Z < 01:19:59Z`), medium for launch ordering: one-second timestamps
  prove `launch <= first request`, not strict `<`.
- **Round-13 ack audit** — high for schedule-derived counts (two scripts,
  selftests 4/4 and 8/8, nine independent re-derivations); low as a novelty
  claim because prior-art and connector artifacts were absent in that round.
- **Live surface sweep** — high at 2026-09-29 capture time. Endpoint/process
  identity was exact; benchmark relocation is path drift with content
  no-drift; bounty-tree cause remains unknown.
