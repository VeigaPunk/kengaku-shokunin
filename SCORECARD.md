# kengaku-shokunin — Scorecard

Domain: LLM/model research & evaluation. The historical wiki
(`~/Projects/webzites/repos/llm-wiki`), telemetry and benchmark originals are
unavailable at the exact paths in
`corpus/evidence/round13-coverage/surface-receipt.json`; retained corpus
digests and response bytes are distinct from those originals. Lane axes per
`../MISSION.md`: **novelty + calibration**. The six `../AXES.md` axes are
also scored below. For this explicit round-13 re-dispatch, coverage and
novelty tie at 7; coverage wins the most-falsifiable-claim tie-break while
the sources needed for a new model probe remain unavailable.

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

## Round 15 — OMP/ufo-fsd re-census (hermetic round, no axis-move)

The OMP/ufo-fsd substrate relocated (`~/Projects/origin-work/ufo-fsd-alpha` →
`~/Projects/ufo-fsd-alpha`, new HEAD `964f443e`, ~50 upstream files deleted).
This lane's census: **the drift never reached us**. `grader.py` replays four
committed probe trees from in-repo bytes only — no `--src`, no origin-tree I/O —
so there is nothing to re-derive and nothing to repair.

| Check | Before → After | Verdict line |
|---|---|---|
| `python3 grader.py` (repo root) | PASS → PASS | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline`, exit 0 |
| `python3 grader.py --selftest` | PASS → PASS | `[selftest] ALL PASS` (S0–S7), exit 0 |
| `grep -rln 'origin-work' . --exclude-dir=.git` | — | 1 hit: `corpus/evidence/round14-fleet/r14-scout-surfaces.md`, which names `~/Projects/origin-work/` as a *directory-neighbour observation* and `origin-work/open-bug-bounties/` as a distinct Next.js codebase — not a ufo-fsd citation. Historical record; preserved verbatim per append-only, now marked historical below. |

Classification counts (mission taxonomy): (a) stale `--src`/default path —
**0**; (b) citation to an upstream-deleted file — **0**; (c) moved-file line
drift — **0**; (d) genuine lane defect — **0**.

**Round-15 host sweep (re-verification, two new ABSENT surfaces — both
external/operator-side, not lane defects):**

- `~/Projects/origin-work/` — **ABSENT** (`test -d` → false). The r14 scout's
  two `origin-work/` mentions are now historical pointers; erratum appended
  below rather than rewritten.
- Served model `http://127.0.0.1:34113` — **ABSENT**: `curl -s -m5 /health` →
  connection failure (000); `pgrep -a llama-server` → no rows; `systemctl
  --user status qwen-coder.service` → "could not be found". The r10/r11/r14
  process-level pins (pid 1299, 41-token argv, q4_0 KV) remain high-confidence
  historical facts, per the scorecard's own rule that they are capture-time
  host state. **Carried debt, named:** `:34113` serving plane — unblock action
  = operator restores the `qwen-coder.service` unit + llama-server; until then
  the freshness/coverage rubric treats this as a declared-but-unresolvable
  surface, joining the already-absent route-telemetry row.
- `~/Projects/ufo-fsd-alpha` — **resolves** (present at new location);
  `~/archive/bench-arena` — resolves; `~/Projects/webzites/repos/llm-wiki` —
  resolves; `~/Projects/bounties/ledger/telemetry.jsonl` — still ABSENT.

**Erratum (append-only) for `corpus/evidence/round14-fleet/r14-scout-surfaces.md`
§4 V12/V14:** `~/Projects/origin-work/` and `origin-work/open-bug-bounties/`
resolved on 2026-09-29; the whole `origin-work/` directory is now gone
(observed 2026-10-14). Both lines were accurate at capture time; they are
preserved as historical pointers.

**No axis-move:** operability held 8 (gate still green, unchanged); freshness
held 8 (re-verification ran, but two surfaces moved to ABSENT — operator-side);
coverage held 7 (a second declared surface is now unresolvable — rubric cap,
same as telemetry); calibration/depth/adjacency/novelty unchanged (hermetic
round, no probe, no new sourced content).

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

The round-13 re-dispatch selects **coverage (7)**, tied with novelty (7),
because unavailable-source annotations and index membership can be measured
locally. The historical uncapped matched-model proposal remains unexecuted;
this correction does not claim a new model result or novelty instrument.
The coverage score remains capped while declared originals are unavailable.
Next coverage move: broaden the explicitly fixed source-availability
inventory to the other living claims identified by the round-16 audit,
using a separately recorded denominator and revision. Do not subtract the
twelve-document census from that audit's 61 citation occurrences or rewrite
archival scripts to make the count fall. Model-probe work requires a restored,
identity-verified endpoint and a newly filed design before traffic.

Superseded (round 24): this round-13 plan is historical text; the active plan is §Planned (round 25).

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

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 16 | freshness | measured at HEAD (see lesson) | verdicts recorded per gate, no scalar | `corpus/lessons/round-16-recensus.md` |
| 24 | coverage | 7 | 7 (held by cap; counts moved) | `plans/round24_census.sh`; §Round 24 |
| 24 | calibration | 8 | 8 (held; counts moved) | `plans/round24_census.sh`; §Round 24 |

## Round 17 attempt — blocked before native dispatch (2026-10-15)

Starting commit: `3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`.
Round 16 is the latest recorded lane round; headless launch counter 13 is
not a verified-round count. The inherited source-status changes and nine-seat
round-13 re-dispatch artifacts remain unclaimed and uncommitted by this
attempt. Their presence does not satisfy the current 32-seat contract.

Selected axis: **coverage**, tied with novelty at the lowest legacy anchor.
Plan: `plans/wwkd-round-17-coverage.md`. Exactly 32 distinct audit scopes were
validated and rendered; both commands exited 0, with 32 Godspeed prefixes.
**Native task calls: 0; assigned agents: 0; domain integration: blocked.**
Effective reviewer/critic/connector routing and the missing connector fallback
are recorded in `.ufo/round-17/route-blocker.json`. No routing mutation or
substitution was made. A valid rendered payload is not an executed round.

| Axis | Verdict | Evidence / limit |
|---|---|---|
| coverage | unchanged | No admitted integration; inherited annotations/index work remains dirty. Lowest-axis work stays LIVE. |
| novelty | unchanged | No model experiment, external source fetch or new construct. |
| calibration | unchanged | No new assessment result; blocked attempt and inherited ownership are explicit. |
| depth | unchanged | No new domain knowledge admitted. |
| operability | unchanged | Parent replay remains `CHECKS n=733 mismatches=0 errata_pinned=1`; gate exit 0, selftest exit 0. |
| freshness | unchanged | Offline replay is not a current external-source or endpoint verification. |
| adjacency | unchanged | Route admission is operator/kumitate-owned; serving restoration stays outside kengaku. No external fix landed. |

Learning trends: **expansion unchanged; quality unchanged; discernment
unchanged**. No outside non-author admit/reject spot-check was performed.
`corpus/QUALITY.md` is absent and remains named inherited debt; this blocked
attempt does not create a substitute quality claim or change promotion marks.

Parent verification, measured on the inherited dirty working tree at the
starting HEAD: `python3 grader.py` exited 0 with full verdict
`VERDICT: PASS — stored evidence fully re-derives offline`;
`python3 grader.py --selftest` exited 0 with `[selftest] ALL PASS` (S0–S7).
Full stdout/stderr, commands, timestamps, grader digest and exit codes:
`.ufo/round-17/gates.json`. No native judge or rerun of the already-reported
UFO Phase-0/self-iter failure.

**Admission: blocked / not admitted; verified-round increment: 0.**
No saturation claim; this is one blocked attempt, not evidence of three
consecutive blocked rounds. Unblock: supply authorized effective role bindings
to the existing requested aliases and connector fallback, then continue in a
fresh interactive L1 session. Preserve historical reports and inherited dirty
work; revalidate the prepared spec before its one complete native task batch.
Report and receipt applicability are filed under `.ufo/round-17/`.

## Round 19 — probe battery (calibration axis-move, 2026-10-16)

One 32-seat flash wave (operator routing: zai bucket). Claim: the calibration
proxy's pre-registered-probe discipline was intermittent (r8-r11: 0/1, 1/1,
0/0, 1/1) with no standing battery; after: a frozen >=6-probe battery with
receipts, scored at close, plus a reusable template. Landed (evidence commit `0671bb0`): `plans/probe-battery-r19.md` — 9 falsifiable probes / 30 scored
components, FROZEN 2026-10-16T07:55:58Z sha256 `e1a86777…` (predictions
hashed before any dependent request); 5 probes executed (P2/P3/P8/P9 UNRUN —
named, not hidden), 15 receipts; scored at close in-round (first since r11):
mean Brier 0.1836 over 11 gate-passing binaries (9 hit / 2 miss — the two
zai misses carry the mass; seat-pool mean 0.0617 over 26); reliability bands
6/8, 2/2, 1/1. `plans/probe-battery-TEMPLATE.md` = the standing instrument;
`corpus/knowledge/probe-battery-r19.md` = design + scored tables + limits.

Corrections folded at admission: (1) BR-1 — the registrar's first freeze
(07:52:04Z `e3f08a09…`) raced the author's P4/P5 re-base (compute-then-write
TOCTOU); detected by the critic + receipts-auditor, repaired by a re-freeze
at 07:55:58Z after a double-read stability check; five seats ran inside the
stale window but none ran P4/P5 before the valid freeze — adjudicated
mechanically by the scorer's ordering gate. (2) runner-leg-opencode DEFECT-0:
two live requests pre-battery (07:45Z), self-filed with receipts, excluded
from scoring. (3) Bookkeeping defects (v1/v2 probe numbering in one receipt,
frozen-hash field naming) — recorded, not scoring-relevant. (4) Material
premise correction: the operator reordered both cascades post-r18
(ds: alibaba->hyper->opencode-go, devin removed; glm: zai->devin->hyper) —
P4/P5 re-based before freeze, r18 numbers kept as drift contrast.

Axis verdicts: calibration **improved** (standing battery + template +
frozen-before-request discipline + in-round scored close); depth **improved**
(the note + the TOCTOU lesson); coverage **improved narrowly** (9 probes over
the live route surface, incl. the listing-vs-chat mismatch probe
operationalized); freshness **improved narrowly** (15 receipts + frozen
timestamps); operability **unchanged** (no tool change this round);
novelty **unchanged**; adjacency **unchanged** (all probes in-province, small
requests only, credentials untouched). Admission: **ADMIT-with-correction**
(none harmed). Learning trends: expansion/quality **improved**, discernment
**unchanged** (no outside spot-check exists). Goal note: the operator
stopped the 10-round run after this round; this section closes it at one
round.

## Round 20 — battery grid closure (calibration axis-move, 2026-10-16)

One 32-seat zai-flash wave. Claim: close the r19 battery's 4 named-UNRUN
probes (P2/P3/P8/P9) against the SAME frozen predictions. Landed (evidence
commit `af0e3e6`): all 4 executed — 9 requests total, zero retries, receipts
`probe-r19-P2-servicetier.log` / `P3` / `P8-kimi-code-auth` / `P9-absent-port`;
grid 9/9 with per-round provenance; combined aggregate recomputed across all
executed binaries (r19+r20: mean Brier 0.0998 over 46 terms; the 20 binaries
scored this run 0.1495; reliability 9/12, 7/7, 1/1). **3c FALSIFIED** — frozen
`used-percent <= 2`, observed 7 (route-state drift, recorded as a MISS: the
battery working as intended). Template gained the freeze-after-last-edit
guard + unrun-completion checklist; lesson `round20-grid-closure` landed.
Etiquette audit: clean (one benign out-of-scope file disclosed; a defect
pointer numbering fix in-note).

Axis verdicts: calibration **improved** (grid closed against frozen
predictions; the 3c falsification is a calibration finding — the instrument
now shows WHERE the route drifted); coverage **improved narrowly** (service-
tier acceptance set, echo/quota signals, auth-endpoint state, absent-port
now measured); depth **improved** (template guard + lesson); freshness
**improved narrowly** (4 receipts, freeze-verified); operability **unchanged**
(no tool change); novelty **unchanged** (the r21 scout priced the latency-
fingerprint example OUT of novelty — crowded published space — and proposed
three candidates); adjacency **unchanged** (9/9 requests in-province,
credentials never read). Admission: **ADMIT** (none harmed). Learning trends:
expansion/quality **improved**, discernment **unchanged**.

## Round 21 — blind leg-attribution instrument (novelty axis-move, 2026-10-16)

One 32-seat zai-flash wave (31/32; the standalone scorer seat failed but the
instrument's receipts carry authoritative adjudicated scoring, independently
recounted by the trial-auditor). Claim: no instrument could attribute which
cascade leg served a response without operator ground truth; after: a frozen
feature-table instrument (`plans/attrib_probe.py` + `plans/attrib-r21-frozen.md`,
FROZEN 10:20:08Z `9f0244bb…`, double-read guard) attributes the serving leg
blind over >=20 trials per shim against the journal GT read ONLY post-trials.
Landed (evidence commit `0d23c61`): **100% accuracy both shims** — ds 20/20
(GT: alibaba 20), glm 22/22 (GT: zai 13 / devin 9 — the zai 429-fallback
windows produced natural leg diversity, so the fallback path is covered too);
all 11 frozen ablations (8 LOO + 3 mimicry: header-strip, latency-pad,
echo-spoof) at 1.000; ordering chain clean (frozen < trials < first journal
read); 44 small localhost requests, no credentials, three matcher defects
fixed pre-adjudication and recorded. The prior-art note (`attrib-prior-art-r21.md`)
prices the novelty honestly: model fingerprinting is crowded published space
(cited), so the claim is INSTRUMENT + GROUND-TRUTH PROTOCOL, phenomenon-
incremental; the critic's adjacency pass (mori owns observability) is answered
by the note's boundary wording — measurement of model-serving behavior, read-
only journal use, no remediation.

Axis verdicts: novelty **improved** (the lane now produces a measurement no
other province produces — blind leg attribution validated against operator-
journal GT — with the instrument inspectable in-repo and the prior-art check
on record); calibration **unchanged** (the instrument was built under the r19
freeze discipline, extending it rather than moving the axis); depth
**improved** (design + ablation + adjudication records); coverage **improved
narrowly** (hyper/opencode-go legs UNTESTED — 0 GT trials — named as the r22
candidate); freshness **improved narrowly** (4 receipts + frozen table);
operability **improved narrowly** (a stdlib-only reusable tool); adjacency
**unchanged** (boundary wording recorded). Admission: **ADMIT** (none harmed;
the failed scorer seat's remit was covered by two independent scorings —
named, not hidden). Learning trends: expansion/quality **improved**,
discernment **unchanged**.

## Round 22 — forced-fallback leg coverage + battery fold (operability/coverage, 2026-10-16)

One 32-seat zai-flash wave (22/26 seats reported; 4 provider-loss failures —
scorer/reviewer/scribe/determinism — with scoring independently covered by the
instrument's authoritative receipt blocks + the ablation seat; the r22
addendum to the attrib note was integrator-written from those). Claim: cover
the r21-UNTESTED legs (hyper/opencode-go) and fold the instrument into the
standing battery. Landed (evidence commit `8a08483`): instrument v2
(`bb6bd919…` — leg-forcing mode, v2 features, stream-flag GT join) + v2 table
(`77b8d4a0…` live; one defective pin superseded BEFORE any request) +
hyper **COVERED** (run-2: 10/10 on-target = 1.000, bar 0.80) + opencode-go
**named gap** (0 on-target — the echo-marker bait starves against reasoning
models; mechanism proven reachable once via T03; fix shipped) + battery
probe-type P10 fold (template + battery §11) + forced-vs-natural limit named
by the critic.

Axis verdicts: operability **improved** (the instrument now forces fallback
coverage and survives table evolution under the freeze discipline); coverage
**improved** (hyper validated; opencode-go gap precisely characterized —
starvation, not instrument failure); depth **improved** (the addendum +
three-pin freeze history); calibration **unchanged** (freeze discipline
extended, not moved); freshness **improved narrowly** (3 receipts); novelty
**unchanged**; adjacency **unchanged**. Admission: **ADMIT-with-correction**
(opencode-go gap + 4 failed seats named; none harmed). Learning trends:
expansion/quality **improved**, discernment **unchanged**. r23 registered:
opencode-go forcing via the stream-path header leg-selection (the v2 note
documents why stream:false was chosen and what stream:true changes).

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| offline-replay-gate | re-derive every stored probe number from committed bytes, offline, and exit 0/1/2 with a verdict | `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`, `VERDICT: PASS`, exit 0 (re-run 2026-10-19, round 24) | 10 (re-demonstrated 24) |
| frozen-table-pin-check | prove an attribution feature table is byte-stable against its FROZEN pin before any trial | `python3 plans/attrib_probe.py freeze-check --frozen plans/attrib-r23-frozen.md` → `block_sha=1b2d6a01bfa431ec pinned=1b2d6a01bfa431ec stable=True -> OK`, exit 0 (round 24) | 21 (instrument `0d23c61`; re-demonstrated 24) |
| sources-registry | keep a tiered, opened, census-clean registry of where the lane learns, with study paths and a search log | `corpus/SOURCES.md` + the SOURCES contract v1 census (rows 25, malformed 0, `A=24 C=1`, `mined=18 queued=5 rejected=2`, dup/enum/mined-path checks print nothing); receipts `corpus/evidence/round24-sources/gate.md` | 24 |
| interval-reverdict | re-derive every stored attribution verdict from committed receipts and re-verdict it with exact CP95 intervals, per-leg recall/specificity and Rogan–Gladen share bounds, offline, receipts sha256-pinned | `python3 plans/attrib_calibration.py --summary` → `unique_samples=4 … scored_trials=92 correct=92 … transitions=FAIL>UNTESTED:2,PASS>INDETERMINATE:1,PASS>PASS:4 … mismatches=0`, exit 0; `--selftest` 14 checks 0 failed (red runs R1–R6 included); receipts `corpus/evidence/round25-calibration/` | 25 |
| state-assertion-check | re-derive the lane's own current-state assertions (capability rows, axis basis anchors, SHONEN canonical form, PROVINCE surface rows, corpus index both directions) and exit 0/1/2 | `python3 plans/state_check.py --summary` → base `6180e4f` `mismatch=11` exit 1; landed tree `mismatch=0 superseded=1` exit 0; `--selftest` ALL PASS | 25 |
| grader-perturbation-audit | audit pinned stored-response verdicts under exact response-format/negative-control transformations; stratify by format and pid, separate policy capture | `python3 plans/grader_perturb.py --summary`: population1964 excluded0, audited verdicts15168, nine MP/MC interval-verdict families plus909 NOT_SCORED PC checks; independent oracle and final receipts `corpus/evidence/round26-calibration/` | 26 |
| offline-catalog-receipt-verification | Re-derive saved catalog-response metrics offline and compare each present SHA256SUMS entry; HF count is returned-page length and both schema deltas inspect the first record, while OpenRouter `or_models` reads the response's `total_count`. Not endpoint authentication or a full-catalog enumeration. | `python3 plans/catalog_probe.py --verify --lane .` → `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok`; raw responses + SHA256 in `corpus/evidence/round33/catalogs/` | 33 |
| pinned-grader-probe | Execute a benchmark task's own pinned grader offline (digest-checked capture, pinned dependency) on a frozen table of synthetic outputs, each mapped to one instruction requirement with a prediction written before the first run, and print predicted vs observed with the first failing assertion. Not task certification, not runtime inside the task image. | `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` → `cases=18 observed_pass=5 observed_fail=13 mismatches=0`; receipt `corpus/evidence/round35/tb2-grader-probe.txt`, re-run byte-equal by `plans/round35_c1_verify.py` V5 | 35 |
| routed-defect-ledger | Re-run every routed defect's check at the current tip from one ledger and count calibration mismatches (a `closed` row whose check fails, an `open` row whose check passes). Checks are per-defect functions; recurrence is recorded, not enforced. | `python3 plans/defect_ledger.py --lane .` over `corpus/defects.jsonl`; freeze receipt `rows=5 closed=0 observed_pass=0 mismatches=0` (`.ufo/waves/round-35/claims/control-c2-nothing.txt`) | 35 |
| package-gate | Accept or reject an admitted-entry package (entry, capture manifest, SOURCES rows, receipt, frozen instruments, clean tree) and the labelled D4/D5 correction lines against a spec of pinned digests: every quote row must parse and be distinct and verbatim on its cited capture line, teaches cells carry >=8 distinct words, a stub probe dies on its digest pin, `--rerun` byte-compares the receipt, `--require-clean-tree` refuses any untracked file. Exit 0 accept / 1 reject / 2 setup. Not a truth check on prose that parses. | `python3 plans/round36_c1_verify.py --lane .` on a clean clone → `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0` (freeze controls: absent gate `unevaluated=14`; round-35 counter `LEGACY accepted=7/7`) | 36 |
| pattern-valued-grader-probe | The pinned-grader-probe instrument on a grader whose graded artefact is an agent-authored regex file executed inside the grader against a fixed in-test log: 24 frozen candidate patterns, each mapped to one instruction requirement with a prediction written before the first run. Not task validity, not a regex-quality judgement. | `python3 plans/regex_log_probe.py --lane .` → `cases=24 observed_pass=8 observed_fail=16 mismatches=0`; receipt `corpus/evidence/round36/regex-log-probe.txt`, re-run byte-equal by `plans/round36_c2_verify.py` W5 | 36 |
| gate-mutation-harness | Decide which advertised defect classes of a gate its own fixture battery demonstrates: one frozen byte-level silence mutant per branch, killed iff the gate's observable result (exit code plus the set of clauses printing `DEFECT`) changes on some fixture, with a null mutant for non-determinism and a renamed run so no fixture is recognised by its directory name. Survivors are advertised-but-undemonstrated clauses. Not proof that any check is the right check. | `python3 plans/round37_c1_verify.py --lane .` on a clean clone → `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0` (freeze control `killed=5`, `.ufo/waves/round-37/claims/control-c1-nothing.txt`) | 37 |
| service-grader-probe | Execute a captured grader and its helper script offline in a per-case unprivileged bubblewrap sandbox (private network namespace, scratch HOME and /tmp, `/tests` read-only, `PATH` scoped to the named tools) against lane-built HTTP service states, and count observed verdicts against a frozen case table. Not task certification, not runtime inside the task image, not a reward measurement. | `python3 plans/git_webserver_probe.py --lane .` → `cases=22 observed_pass=9 observed_fail=13 mismatches=0` (read the summary line, not `$?`); receipt `corpus/evidence/round37/git-webserver-probe.txt`, re-run byte-equal by `plans/round37_c2_verify.py` V2/P10 | 37 |

Rows enter this table only through a round that demonstrates the capability running (`AXES.md` §Capabilities). The catalog receipt verifier entered in round 33 by passing its offline counter.
The original round-24 capabilities — offline-replay-gate, frozen-table-pin-check, and sources-registry — entered through demonstration that round (commands re-run; output in `corpus/evidence/round24-census/after.txt`). The placeholder row was the scaffold, not a claim.

## Saturation

The lane's saturation line + stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

Round 24 declaration — saturation line: 8 (every owned axis at ≥8); stagnation window N: 4 rounds (no capability row entering within 4 completed rounds). Basis: owned axes are novelty 7 / calibration 8, so the nudge is inactive while novelty sits below 8; four rounds matches r19–r22, the last stretch of verdict-only movement with demonstrated-but-unrecorded capabilities (RoundPlanner-3 proposal, round 24).


## Round 23 — stream-path leg forcing (executed 2026-10-16; NOT-ADMITTED; recorded round 24)

| Claim | Axis | Verdict | Evidence |
|---|---|---|---|
| opencode-go on-target coverage via the shim stream path (≥10 on-target GT trials at ≥0.80) | coverage | **FAIL** — 0 on-target trials | `corpus/evidence/attrib-r23-stream.log:239` `STREAM TARGET opencode-go: on-target GT n=0 … -> FAIL` |
| (characterization, not a claim) stream-path attribution accuracy | — | 30/30 = 1.000 over GT `{"alibaba-token-plan": 6, "hyper": 24}` | `:233-234`; table pin `plans/attrib-r23-frozen.md:214` |

Admission: **NOT-ADMITTED** (the one declared claim failed). Scores: no axis
moves for r23. Calibration debt: executed 2026-10-16, recorded 2026-10-19 —
the same late-landing breach rubric clause (d) recorded for r12/r13; no credit
is taken for the late record. WIP commits `a2ff634`, `f9337d5`, `6f31d23` stay
as unverified history. Mined in `corpus/lessons/round-24.md` (M13, M14).

## Round 24 — sources registry + sourced expansion (coverage) and learning from the lane's own mistakes (calibration), 2026-10-19

Steered round 24 (kaika). Lowest non-retired axis: coverage 7, tied with
novelty 7; tie-break: novelty +1 needs a new probe construct and no probe runs
this round, so coverage carries the lowest-axis claim. No stagnation waiver.
Pre-registration: `plans/round-24-claims.md` (+ Amendment 1). Counting
command for every number: `sh plans/round24_census.sh` (base receipt
`corpus/evidence/round24-census/base-99cf615.txt`; after receipt
`corpus/evidence/round24-census/after.txt`, run after the round-24 commit
with that commit checked out — its `HEAD` line names it — and landed in a
follow-up receipt commit).

| Claim | Axis / type | Before → after (census key) | Score | Self-verdict (pending non-author check) |
|---|---|---|---|---|
| C1 sources registry + 5 sourced knowledge entries on uncovered ground + index parity + province map | coverage (lowest) + capability `sources-registry` | expansion_entries_on_mined_rows 0 → 5; knowledge_unindexed 3 → 0; lessons_unindexed_excl_round24 5 → 0; root_logs_indexed 0/28 → 28/28; plans_indexed 0/8 → 10/10; dead_index_rows 0 → 0; coverage_map_rows 11 → 16; frontier_rows 0 → 5; province_map_sections 0 → 4; SOURCES rows absent → 25 (census clean) | 7 → **7 (held by the unresolvable-surface cap)** | improved (counts); capability row entered |
| C2 mistakes mined into round-closure criteria; SCORECARD made to match repo state; round 23 recorded | calibration | lesson_mistake_rows absent → 20; closure_criteria_citing_round24 absent → 10; scorecard_state_defects_open 6/6 → 0/6; round23_sections 0 0 → 1 1 | 8 → **8 (held)** | counts moved (closeout and SCORECARD state accuracy, not demonstrated discernment); score held — rubric +1 needs an in-round scored probe; late recording buys nothing |

Dissent on record (lane L2, advisory): ClaimCritic-3 ruled coverage must hold
at 7 (adopted) and judged C2 "honest closeout bookkeeping", not a calibration
axis-move; RoundPlanner-3 concurred that "improved" is unsupported for the
score. The counts are reported as measured; the operator rules on whether C2
admits.

Re-derived axis state, round 24 (closes D10: each axis is a number with a
basis, or marked verdict-only):

| Axis | Round-24 value | Basis |
|---|---|---|
| novelty | 7 | numeric anchor r14 (`:162`); r21 "improved" verdict was never converted to a number — verdict-only, unconverted; conversion needs a rubric ruling, not a late bump |
| calibration | 8 | held r14; r19/r20 "improved" verdicts verdict-only; r24 held (C2) |
| depth | 9 | held (anti-double-count); r24 adds one 2-line SKILL pointer, no new rule counted |
| coverage | 7 | held by the declared-but-unresolvable-surface cap (route telemetry, wiki, bench-arena absent — `PROVINCE.md` §Historical) |
| operability | 8 | `python3 grader.py` PASS re-run 2026-10-19; `freeze-check` OK; no new gate |
| freshness | 8 | r24 re-verified every PROVINCE surface (`test -e`/`ss`/`sha256sum`, §Province map) and re-opened 23 public sources; no claim |
| adjacency | 8 | SiblingConnector-3 report-outs to kotoba, tameshi, chousa (named in the round report); no integrator arbitration |

- **D14 errata (round 24).** `SCORECARD.md:305` "All 149 checks" is stale;
  the gate today prints `CHECKS n=733 mismatches=0 errata_pinned=1`
  (`python3 grader.py`, 2026-10-19). The old line stays as written; this row
  supersedes it.
- Round 23 recorded NOT-ADMITTED above (§Round 23); no credit taken.

## Planned (round 25)

- **C1 — calibration / discernment:** fold the orchestrator's non-author
  spot-check of round 24 (≥1 admit, ≥1 reject) into `corpus/lessons/round-25.md`
  as `agree`/`disagree` with reasons; every disagreement becomes a grounded
  `corpus/QUALITY.md` row. Before: 0 recorded non-author gate checks; after: ≥2.
  Count: `grep -cE '^- Spot-check — (admit|reject): (agree|disagree)' corpus/lessons/round-25.md`.
- **C2 — novelty (tied lowest, 7):** judge calibration applied inward — apply
  the S011 sensitivity/specificity correction to the attribution instrument's
  committed r21–r23 receipts (GT exists, no endpoint needed) and price it
  against S009–S012 with fetched URLs. Before: 0 calibrated-accuracy intervals
  for the instrument; after: 1, with an in-repo script and a prior-art verdict.
  The +1 fires only if the rubric's three legs hold.
- Coverage stays capped until an operator ruling on retired surfaces (L0) or a
  restored source.

## Corrections recorded in round 25 — current-state assertions (appended; superseded lines stay as written)

Found by `python3 plans/state_check.py` (C2) and the round-25 wave-1 scouts. Each line names what it supersedes.

- **R25-E1 (2026-10-20)** supersedes `P2a.capability.sources-registry` — now `rows 26` `malformed 0` `A=24 C=2` `mined=18 queued=5 rejected=3` (registry ids S001–S026; S026 was appended in e21f9ea after the §Capabilities sources-registry cell was written on the 25-row census; that cell's counts are stale, its capability claim stands — scripts/sources-census.sh validate exits 0).
- **R25-E2 (2026-10-20)** supersedes the §Round 24 axis-table adjacency basis "no integrator arbitration": the orchestrator adjudicated round 24 (`corpus/lessons/round-24-verifier-spotcheck.md`, commit a42bb40, "ADMITTED … Orchestrator ruling on the lane's L0"); adjacency itself was ruled unchanged. Calibration's descriptor there reads "improved, score held 8" per the same adjudication.
- **R25-E3 (2026-10-20)** supersedes the D14 erratum's anchor: the "All 149 checks" line is `SCORECARD.md:307`, not `:305` (`grep -n 'All 149 checks' SCORECARD.md`).
- **R25-E4 (2026-10-20)** supersedes the novelty mapping-of-record pointer "`../MISSION.md:14` assigns it": the kengaku axes assignment is `../MISSION.md:24` (`grep -n kengaku ../MISSION.md`).
- **R25-E5 (2026-10-20)** supersedes §Saturation's first sentence ("to be declared … on its next round"): the round-24 declaration (line 8, N = 4) directly below it is the declaration of record.

## Round 25 — interval-calibrated attribution verdicts (novelty → coverage) and current-state assertions re-derived (calibration), 2026-10-20

Hyaku block 25–34, L1 KengakuR25 (holds the planner seat). Lowest axis: novelty 7, tied with coverage 7; tie-break:
coverage is capped at 7 by the unresolvable-surface clause pending the operator's coverage-cap ruling, so the lowest-axis
claim is novelty. No stagnation waiver. Pre-registration `plans/round-25-claims.md` (landed `3f371d2`; Amendment 1 `710409f`,
both before any instrument output). Counting command for the round: `sh plans/round25_census.sh` (base receipt
`corpus/evidence/round25-calibration/round25-census-before-6180e4f.txt`).

**Legacy-axis mapping (PROTOCOL.md "Fleet-2 conventions"; Amendment 1 item 2):** `novelty` is a recorded sub-axis of
canonical **coverage** (coverage/constructs: an edge class the lane can now observe; coverage/surfaces keeps its own row
and cap). It serves the distinct-axes rule and the expansion trend only and is scored by the novelty rubric (`:244`); the
canonical coverage number is not moved by it. Dissent on record: CritAxisMapping (calibration would fit closer).

| Claim | Axis / type | Before → after (counting command, measured against) | Score | Self-verdict (pending non-author check) |
|---|---|---|---|---|
| C1 exact-interval re-verdict of the r21–r23 attribution receipts + knowledge entry on sourced rows | novelty (→ coverage/constructs; lowest) + capability `interval-reverdict` | interval-carrying verdicts 0 → 35 estimates (PASS 12, INDETERMINATE 11, UNTESTED 12); stored verdicts re-verdicted 0/7 → 7/7 with transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1, PASS>PASS 4; independent sh+awk parser agrees (`python3 plans/attrib_calibration.py --summary`; before: instrument absent at `6180e4f`; after: landed round-25 tip) | 7 → **8 claimed** (rubric legs: new construct — 0 exact/per-leg/verdict-carrying intervals before, Amendment 1 item 1; instrument in-repo and offline; prior-art verdict with fetched URLs S027–S034, S011: method and the small-n phenomenon are published, the contribution is the lane-local measured construct and one overturned stored verdict; power ask met on all 4 overall-accuracy samples, n = 20–30 ≥ 17) | improved; +1 contested in advance by CritNoveltyLegit (leg c "already published" cap) — the non-author closure rules |
| C2 frozen current-state assertions re-derived by command | calibration | mismatches on frozen P2 at base `6180e4f` 11 → 0 on the landed tree (1 superseded by R25-E1, re-derived) (`python3 plans/state_check.py --summary`; before receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f.txt`) | 8 → **8 (held)**: the rubric +1 needs a scored probe; the observable AXES.md:15 names moved | improved (observable), score held |

Separability (QUALITY R13): each count re-run with the other claim reverted is unchanged
(`corpus/evidence/round25-calibration/revert-test.txt`). Predictions P1–P5 scored: outcomes (1, 1, 1, 1, 0); Brier
P1 0.0025, P2 0.2025, P3 0.0100, P4 0.0009, P5 0.0100; mean 0.0452, of which P2 — the only forecast not derivable from
committed bytes at filing — is 89.6%; the four derivable rows average 0.0059. No calibration credit is taken from this score.

Re-derived axis state, round 25:

| Axis | Round-25 value | Basis |
|---|---|---|
| novelty (→ coverage/constructs) | 8 claimed | C1 above; contested leg (c) named; held at 7 if the closure rules the cap applies |
| calibration | 8 | C2 observable moved, score held (rubric +1 needs a scored probe) |
| depth | 9 | held (anti-double-count): SKILL measurement rule 14 documents this round's instrument |
| coverage (surfaces) | 7 | cap unchanged; five `## Surfaces` rows now carry dated ABSENT markers; cap ruling re-filed as L0 |
| operability | 8 | two new offline gates with selftests; scored under the capabilities table, no operability claim |
| freshness | 8 | round-start receipts (`.ufo/waves/round-25/build/BaseReceiptsExec.md`) and 10 sources re-opened; no claim |
| adjacency | 8 | kumitate/kotoba/kagi/souji/kaidoku/tameshi/chousa overlaps ruled by wave-1 connectors; no claim |

## Planned (round 26)

- **novelty or coverage (lowest, 7 / 8 per the closure):** extend the interval rule to `grader.py`'s stored verdicts
  (the remaining half of the "judge calibration applied inward" frontier) with a frozen population and an S010-style
  perturbation audit; before = 0 interval verdicts on grader outputs.
- **calibration:** pin content (not only range) for every SHONEN/axis-basis line anchor in `plans/state_check.py`
  (the kagi L17→L19 failure class), red-run first.
- Coverage stays capped until the operator rules the coverage-cap L0 (re-filed round 25).

### Round 25 — falsify-wave revision (appended 2026-10-20 ~23:20 -03; the rows above stay as landed in `8ea41f9`)

Wave 2 (87 seats) attacked `8ea41f9`; instrument changes are `plans/round-25-claims.md` Amendment 2. This revision
supersedes the C1/C2 rows, the Brier paragraph, the mapping paragraph, the round-25 axis table and the round-26 plan above.

| Claim | Axis / type | Before → after (re-run on the revised tree) | Score | Verdict (pending non-author closure) |
|---|---|---|---|---|
| C1 exact-interval re-verdict of the r21–r23 attribution receipts | novelty (nominally → coverage) + capability `interval-reverdict` | interval-carrying verdicts 0 → 30 (35 estimates: PASS 7, INDETERMINATE 11, UNTESTED 12, 5 non-firing specificity lines without a verdict); stored verdicts re-verdicted 0/7 → 7/7, transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1, PASS>PASS 4 (`python3 plans/attrib_calibration.py --summary`) | **7 (held)** — the +1 is withdrawn: CI-lower-bound gating of Rogan–Gladen-corrected judge rates is published as tooling (cigate 0.2.0, S041; PriorArtWeb), so the rubric's `:244` "already published" cap applies to the construct. Dissent: CritNoveltyFresh (+1 fires) | improved (observable), score held |
| C2 frozen current-state assertions re-derived by command | calibration | mismatches at base `6180e4f` **10** (v2 receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt`; v1 counted 11 by testing a `/proc` pid pin inside an endpoint row, contrary to P2d) → 0 on the revised tree (1 superseded, full-census restatement); narrowest reading of the registered P2c (without PROTOCOL.md:432's pointer-only form) gives 6 → 0 (`python3 plans/state_check.py --summary`) | 8 (held) | improved (observable), score held |

- **The one PASS→INDETERMINATE re-verdict is population-dependent** (CritAuthoritativeBlock, RevDedupSensitivity):
  under the receipt's own reading of `attrib-r22-legs.log` (both blocks authoritative) hyper is 19/19, and counting
  the deduplicated r22 pair as two executions gives 20/20 — either way CP95 lower > 0.80 (PASS). The frozen
  last-block and dedup rules stand as registered; the sensitivity lines print the pooled values.
- **Share bounds:** the landed `rg95` was conditional on the observed share; with the sampling arm (`rg90`) every P1
  share bound is vacuous or nearly so (Amendment 2 item 2).
- **Brier:** P2 scores 1 only under the literal dedup key; on its "same sample" wording it scores 0 (Brier 0.3025,
  mean 0.0652). All five events were derivable from bytes committed before filing (CritBrierHonesty): zero genuine
  forecasts; no calibration credit is taken.
- **Mapping:** `novelty` is nominally mapped to canonical coverage (constructs) — a mapping, not an AXES.md split
  (coverage is not saturated); the coverage row keeps its own number (7) and cap (CritMappingFresh).
- **R25-E6 (2026-10-20)** supersedes §Round 22's "hyper validated" (`grep -n 'hyper validated' SCORECARD.md`): under
  the exact CP95 rule the r22 TARGET hyper 10/10 is INDETERMINATE on the registered population (PASS if pooled, above).
- **Capability `state-assertion-check`:** base `mismatch=10` exit 1 (v2), revised tree `mismatch=0 superseded=1` exit 0.

Re-derived axis state, round 25 (revision): novelty 7 (held; observable recorded) · calibration 8 (held) · depth 9 ·
coverage 7 (capped) · operability 8 · freshness 8 · adjacency 8 (kumitate report-out filed in `PROVINCE.md`).

Planned (round 26), superseding the plan above:
- **novelty (7, lowest, tied with coverage 7):** a construct not already published as tooling — e.g. a journal-join
  GT audit of the attribution receipts (falsify seat ScoutJournalCaveat: GT is an unverifiable journal join), or the
  S010-style perturbation audit on `grader.py` outputs, with a tooling-registry prior-art search before claiming.
- **calibration:** content-pin every SHONEN and axis-basis line anchor in `plans/state_check.py` (the kagi L17→L19
  class) and remove its dead branches (SimplifyStateCheck), red-run first.
- Coverage stays capped until the operator rules the coverage-cap L0.

## Corrections recorded in round 26 — routed defects (appended 2026-10-21)

The round-25 closure (`corpus/lessons/round-25-verifier-spotcheck.md:152-161`) routed these against new round-25
text, outside P2. Old cells remain byte-identical. C2 extends observability to P3; these repairs were known,
not discoveries credited to the new instrument.

- **R26-E1 (2026-10-21)** supersedes `P3a.capability.interval-reverdict.selftest-checks` — now `18 checks` `0 failed` (`SCORECARD.md:558` said 14; `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt`; `python3 plans/attrib_calibration.py --selftest`).
- **R26-E2 (2026-10-21)** supersedes `P3a.capability.state-assertion-check.base-mismatch` — now `mismatch=10` (base `6180e4f`, exit 1; `SCORECARD.md:559` said 11; v2 receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt`).

R26-E3 corrects both PROVINCE registry assertions in PROVINCE itself; the dated round-25 population is
S001–S042. R26-E4 (landing-time Gate evidence) is recorded in `corpus/lessons/round-26.md` M39 and Q13;
it does not retroactively admit round 25 or reverse the outside verdict.

Parser-format addendum (2026-10-21): R26-E1/E2's extra inline code citations are not value tokens.
The exact-token v3 parser compares the entire code-span list; the following machine-readable restatements
supersede those rows' formatting, not their evidence or values. Commands and receipt pointers remain above.
- **R26-E5 (2026-10-21)** supersedes `P3a.capability.interval-reverdict.selftest-checks` — now `18 checks` `0 failed`
- **R26-E6 (2026-10-21)** supersedes `P3a.capability.state-assertion-check.base-mismatch` — now `mismatch=10`

## Round 26 — grader perturbations and frozen P3 self-assertions (2026-10-21)

Lowest non-retired: novelty7 tied with coverage7; novelty maps to canonical coverage/constructs in the C1
row below. Coverage remains capped, no stagnation waiver. Repairs R26-E1–E11 preceded knowledge admission;
pre-registration e0037a8 and disclosed post-output Amendments1/2 freeze the populations and interpretation.

| Claim | Axis | Before → after and counting command | Score / verdict |
|---|---|---|---|
| C1 finite-corpus response-format audit | novelty → canonical coverage/constructs (lowest) | instrument absent at f11bffbf; 0 → 15168 audited verdicts across9 MP/MC interval-verdict families, plus909 NOT_SCORED policy captures; `python3 plans/grader_perturb.py --summary`, independent oracle, receipts corpus/evidence/round26-calibration/ | 7 → 7 held; observable improved, no method-novelty credit (evalmut S045) |
| C2 content-pinned frozen self-assertions | calibration | v3 on f11bffbf reports5 P3 mismatches (four routed numeric repairs plus missing spotcheck index); final-tree count in state-check-final.txt; `python3 plans/state_check.py --summary` | 8 → 8 held; observability extension, not discovery credit for routed repairs |

Measurement revision and final outcomes are appended after the final run. Nothing in this section claims
all current assertions are checked: P2/P3 are frozen, and round26 additions remain outside that population.
No other axis changes: depth9, coverage7 capped, operability8, freshness8, adjacency8.

Capability demonstrated this round: **grader-perturbation-audit** — reproducibly audit pinned stored-response
verdicts with exact transform spans, conditional denominators, format strata and pid-composites; command
`python3 plans/grader_perturb.py --summary` plus selftest and independent oracle; first-working round26.
The held score does not prevent a demonstrated capability entering the repertoire.

### Round-26 capabilities table additions

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| grader-perturbation-audit | Audit the frozen stored-response population with exact transform spans, MP/MC denominators, format strata and pid composites; D1 policy capture is separate | `python3 plans/grader_perturb.py --summary`; `corpus/evidence/round26-calibration/grader-perturb-final.txt`; independent `plans/fixtures/r26/perturb_oracle.py` | 26 |

### Planned after round 26 (not a new round claim)

- Lowest novelty/coverage remains 7: separately freeze a comparison of extraction policies or audit a newly opened benchmark scoring specification; no new-method credit without tooling prior-art checks.
- Calibration remains 8: extend current-assertion content pins only against an explicitly frozen population, preserving out-of-population disclosures.
- Coverage/surfaces remains capped pending the operator's existing round-25 L0 question.

### Round-26 final measured outcomes (self, pending outside closure)

- **C1 improved observable, score7 held:** `python3 plans/grader_perturb.py --summary` → population1964,
  excluded0, audited verdicts15168, policy checks909, nine MP/MC interval-verdict families. Independent
  oracle agrees. Pooled F1/F2 1802/1819 does not erase MULTI14/31 or composite187/194 INDETERMINATE.
- **C2 improved observable, score8 held:** the same v3 `python3 plans/state_check.py --summary` measures
  frozen base `f11bffbf` mismatch5 → repaired tree mismatch0, superseded5 (278 assertions,3 offline
  unverifiable). Four numeric defects were already routed; the new instrument does not claim to discover them.
- Both claims' separability counters are unchanged under the other's revert; exact P2 keyed projection
  matches v2. Instrument selftests and independent fixtures are green after M54's scratch-setup fix;
  the failing pre-fix receipt remains. Evidence `corpus/evidence/round26-calibration/`.
- These are worktree measurements before packaging, not falsely attributed to detached HEAD.
  Actual admission revision, Q13 and frozen-commit census are appended after the lane helper lands it.

### Round-26 measured revision and structural admission result

Measured/pushed admission commit: **`d4dfdb016c45a332d308898511e3964655629cc5`**.
`sh plans/round26_census.sh` at that clean revision re-runs both claim counters:
C1 audited15168 / policy909 / families9, exit0; C2 assertions278 / match270 / mismatch0 /
superseded5 / offline-unverifiable3, exit0. `python3 plans/gate_timing_check.py --lesson
corpus/lessons/round-26.md --commit d4dfdb016c45a332d308898511e3964655629cc5` exits0:
one admit, three cited qualifying returned reports, zero failed support checks.
Knowledge/index parity34/34 and SOURCES48, malformed0; final source-validator exit0.
Receipts: `corpus/evidence/round26-calibration/round26-census-after.txt`,
`gate-timing-actual-commit.txt`, `sources-census-final.txt`, `actual-commit-byte-check.json`.
The actual commit retains the exact measured instrument and candidate bytes. Scores stay7/8;
all other axis values stay as declared. These are author measurements, not outside admission.

## Round 27 — fixed-response extraction policies and P4 (2026-10-21)

Lowest legacy novelty7 → canonical coverage/constructs, tied coverage7 capped; no stagnation waiver.
Base b5719440, preregistration11a7fc8 plus disclosed post-output Amendment1. C1/C2 are causally separate.

| Claim | Axis | Before → observed | Score/verdict |
|---|---|---|---|
| C1 extraction-policy comparison | novelty → coverage/constructs (lowest) | `git cat-file -e b5719440:plans/parser_policy_compare.py` exit128, absent; `python3 plans/parser_policy_compare.py --summary` compares1964×8=15712 verdicts,1089 disagreement events over five policies | 7→7 held; observable improved, no method novelty (xFinder and public harness prior art) |
| C2 frozen P4 assertions | calibration | v3 checks0 P4 assertions; v4 freezes round26's own assertions against their named historical evidence; final inventory/counter appended after integration | 8 held; pending final counter and mutation evidence, not preclaimed |

C1's source row S056 and S049–S055 are opened this round; draft knowledge remains outside corpus until
returned Q10 rereads. E4's large score fall is instruction-contract mismatch, not new model-error discovery.
No other axis moves: depth9, coverage7 capped, operability8, freshness8, adjacency8. Final measured revision,
capability demonstration, C2 outcomes and next frontier are appended after falsification.

### Round-27 build measured revision preparation

C2 v4 registers **49 P4 assertion IDs** (P4a9/P4b8/P4c11/P4d14/P4e6 plus one inventory control),
where v3 registered0. Delivered v4 on frozen base b5719440 and current candidate both report
`assertions=327 match=318 mismatch=0 superseded=6 offline_unverifiable=3`, exit0. P4 specifically:
48 MATCH,1 SUPERSEDED (the pre-existing exact README source-support erratum),0 MISMATCH.
This is new **observability**, not a 1→0 newly discovered defect repair: the initial implementation
wrongly ignored an already-landed erratum; that implementation defect was fixed before admission.
The base-mismatch≥1 forecast (p=.55) is false under the delivered checker. Calibration8 stays held.
Commands/revision: delivered checker SHA25629c5d716a53e77bf4a82d2155775dda3e94385e058b4700af54cb3a23d031f32,
`python3 plans/state_check.py --root <export-of-b5719440> --json` and current root; receipts
`corpus/evidence/round27-calibration/state-v4-{base,build}.{json,txt}`. Exact48+1 IDs:
`plans/fixtures/r27/p4_assertion_ids.txt`. This does not count every numeric token as an independent check.

### Round-27 falsification outcome (supersedes the49-ID build snapshot)

Delivered P4 now has **51 IDs**, adding honest score/adjacent-numeric disclosure groups rather than
silently labeling unsupported claims MATCH. P4a10/P4b8/P4c11/P4d15/P4e6 plus inventory1:
48 MATCH,1 SUPERSEDED,2 OFFLINE_UNVERIFIABLE. Whole checker author/independent working-copy replays:
`assertions=329 match=318 mismatch=0 superseded=6 offline_unverifiable=5`, exit0.
These values replace327/3 only as the extended diagnostic inventory, not a score or new-defect discovery.
The before/after observable is **0→51 registered frozen assertion/disclosure IDs**; base and final both
have0 mismatches under the final checker. Calibration8→8 held. Receipts/revision are appended at landing.

Falsifiers forced actual repairs: E6 ordering witness (59 hand cases,10 mutants); P4 denominator/comparison/
dispatch and full-token-supersession controls; summary disclosure; eight score tokens made explicitly
unverifiable; actual JSONL breakdowns; four numeric repairs plus one index repair derived from receipt;
recovery count from the committed receipt and distinct ID checks. Q16 extends the Gate fixture to two
reports, complete traversal and isolated Git contexts. Original failures and follow-up rereads are retained.
Evidence: `corpus/lessons/round-27.md`; `.ufo/waves/round-27/falsify/{FMutPolicyE6,FMutP4d,FP4Inventory,FDisclosure,FGateQ15}.md`.

### Round-27 capability addition

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| extraction-policy-comparison | Re-score the fixed1964-response population under eight alternate JSON extraction policies, publish paired flips/strata/matrix and separate contract mismatch from accuracy | `python3 plans/parser_policy_compare.py --summary`; `plans/fixtures/r27/independent_policy_recheck.py`; returned full reread FEntryNumbers |27 |

### Planned after round27 (not a new round claim)

- Lowest legacy novelty/canonical coverage-constructs remains7: move to a sourced agentic benchmark
  task-spec/scoring-validity audit, rather than claiming these known parser policies as a new method.
- Calibration8: address the explicitly disclosed S038 source-use drift with an opened-source, bounded
  registry consistency population; do not reinterpret P4 as a whole-current-tree assertion census.
- Existing L0 coverage-cap/novelty-conversion questions remain open; no retroactive numeric conversion.

### Round27 — actual admission measurement

Measured/pushed admission **6356b0bab78ee9292b7c9e112e6a414d3679dd6c**. Code and canonical entry
are byte-equal to the exercised prospective package (`actual-admission-byte-proof.json`).
`python3 plans/parser_policy_compare.py --summary`:15712 comparisons/1089 events/five policies, exit0.
`python3 plans/state_check.py --json`:329 checked assertions,318 MATCH/0 MISMATCH/6 SUPERSEDED/5
offline-unverifiable;51 P4 IDs (48 MATCH/1 SUPERSEDED/2 offline groups), exit0.
Actual-commit Gate passes1/1; knowledge/index35/35; sources60/malformed0. Main full suite17 expected
exits, independent full numeric replay,5/5 P4 class mutants,298-record P2/P3 preservation and two-way
revert counters all verify. Scores7/8 held; no axis harmed in exercised scope, outside closure pending.

M64 census-unit erratum: the original admitting-revision census printed50 because it excluded the
P4.population control. Its receipt remains unchanged. The corrected selector prints51, with red1
old-receipt-vs-JSON and green0 repaired-command evidence; the population and direct JSON counter never
changed. The later final measured census revision is named in the report.

## Round 28 — pinned WebArena task specs and literal source references (2026-10-21)

Lowest legacy novelty7→canonical coverage/constructs; tied coverage/surfaces7 remains capped, no waiver.
Baseline b9b24796277020d1b9b01923b45313d6a565e664; prereg f0ba09be plus explicit post-recon Amendment1.

| claim | axis | observed before → build after, counting command | score / verdict |
|---|---|---|---|
| C1 static benchmark task-spec audit | novelty → canonical coverage/constructs (lowest) | instrument absent at base (cat-file128); `python3 plans/benchmark_spec_audit.py --summary` inventories812 tasks/5 evaluator-type sets/27 strata/16 selected case audits/651 page targets, exit0 |7→7 held; local observability improved, no new-method/validity/leaderboard credit|
| C2 frozen literal-reference coverage | calibration | no dedicated13-row diagnostic at base; delivered `python3 plans/registry_check.py --json --root <base-export>` mismatch_sources2→final0;13 rows/35 paths/12 reference links, selftest12 cases |8→8 held; repair knownS038 drift and corrective-indexS050 gap, not source-truth or whole-tree PASS|

Evidence: corpus/evidence/round28-calibration/{audit-summary.txt,registry-summary.txt,build-acceptance/}.
Only-delta experiment: baseline red(S038/S050), S050-only correction red(S038), S038 status/used-by-only
delta green0. Two-way row/file-partitioned revert counters agree; alternate census matches but is
L1-authored, not author-independent. F5 is false and never claimed as an independent calibration trial.

All329 historical checked IDs preserve318 MATCH/0 MISMATCH/6 SUPERSEDED/5 offline; original26
OUT_OF_POPULATION IDs retained, new disclosure IDs appear as round28 artifacts are added. In P4 the
two offline groups and one superseded ID remain exactly that. Initial acceptance's equal-entire-ID-set
assertion wrongly rejected new disclosures; preserved red and corrected invariant are explicit receipts.
No historical checker code change and no endpoint restoration. No other axis moves: depth9, coverage7
capped, operability8, freshness8, adjacency8. Actual measured/pushed revision and capability demonstration
are appended after fresh falsification and admission; no preclaimed capability row.

### Round28 fixed-package outcomes and demonstrated repertoire

Counting commands/receipts: `python3 plans/benchmark_spec_audit.py --summary` →
812 tasks/812 IDs/5 type sets/27 strata/16 cases/651 targets/0 findings; `python3 plans/registry_check.py
--summary` →13 rows/35 paths/12 links/0 mismatched rows. Both exit0; fixed selftests67/15 exit0.
Identical checker on baseline export has2 mismatched rows, final0; staged only-delta and two-way
revert evidence remain in round28-calibration/final-acceptance. Scores stay7/8; other axes unchanged.
Current tests are bounded, not exhaustive mutation coverage. Actual measured/pushed revision follows.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| benchmark-task-spec-audit | Inventory pinned WebArena specs and statically trace predicates/limits without executing upstream code or claiming runtime validity | `python3 plans/benchmark_spec_audit.py --summary`; final-acceptance/audit-current.stdout; round28 Gate |28|
| frozen-reference-coverage | Check the declared13-row/35-path literal source-reference population and expose missing/status links | `python3 plans/registry_check.py --summary`; staged baseline/only-delta receipts |28|

### Planned after round28 (not a new round claim)

- Keep novelty7/coverage cap and calibration8 until independently justified; no retroactive conversion.
- Frontier: generated task configurations/runtime evidence, additional benchmark specs and semantic
  source-support checks require separately frozen populations; no all-current-tree or complete-test claim.

Round28 actual-commit erratum: df33fc83's census first exposed a legacy P4a EOF-scope bug, not a changed
score or newly verifiable group. The production slice is now bounded to the frozen round26 H2 section;
permanent selftest red1→green0 and JSON329/318/0/6/5 restore the exact declared disclosure classes.
Old/new checker pins: plans/fixtures/r28/state-check-scope-fix.json. New C1/C2 metrics and67/15 tests
remain unchanged. Final corrected measured revision is appended after landing; no red result is hidden.

### Round28 actual corrected measured revision

Measured/pushed revision **78e6df8171edf8afbb85e7345aea97f6cb2c7228**:
`python3 plans/round28_census.py --revision 78e6df8171edf8afbb85e7345aea97f6cb2c7228` exits0.
C1=812/5/27/16/651, C2=13/35/12/0, source69/malformed0, knowledge/index36/36.
Historical329/318/0/6/5, P4 exactly51 (48 MATCH/1 SUPERSEDED/2 offline),29 OOP disclosures
(26 old+3 round28). Actual Gate1/1 passes at this revision; byte proof binds entry50589759…,
both returned v4 reports and measured code. First df33fc83 red checks remain explicitly recorded.
Complete acceptance after the bounded legacy fix also exits0 with11 expected-exit stages and actual
new-entry source links clean. Receipts: round28-calibration/actual-*-corrected.txt,
actual-final-byte-proof.json, complete-acceptance/. These are author measurements, not outside admission.

## Round 29 — pinned WebArena generated-config projection (2026-10-21)

Lowest legacy novelty7→canonical coverage/constructs; tied coverage/surfaces7 remains capped by the open
round25 L0, no waiver, and C1 does not move the canonical coverage number. Baseline
ed26bdf5d924755697cd6812129be2fa441c42a3; prereg 31934e5660f1814326c6472eefdfa0c41e642a2f (KengakuR28).
Replacement L1 KengakuR29-2 after the host crash; build integrated at b98dcf31, falsify repairs at dbcecded.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 generated-config projection capability | novelty → canonical coverage/constructs (lowest) | instrument absent at base (`git cat-file -e ed26bdf5…:plans/config_projection.py` exit128) → `python3 plans/config_projection.py --summary` 812 tasks/812 IDs/3 profiles/2436 projections, 1435 occurrences, 1416 changed leaves (1355 URL-path/61 non-URL-path), 0 remaining tokens, index==task_id 812/812, exit0; four independent oracles agree on all 2436 objects | 7→7 held; local observability improved, no new-method/validity/deployment credit |

Informed forecasts (prereg F1–F5; source-informed, not calibration trials, no calibration credit):
F1 true (812×3 parse), F2 true (0 remaining), F3 unscorable (category criterion not frozen before
observation; JSON-path 61, value-shape 0), F4 true (812/812 frozen, shuffled witness maps 0→1, 1→0),
F5 true (novelty held). Calibration8 unchanged. Other axes unchanged: depth9, coverage7 capped,
operability8, freshness8 (LOG round29 entry), adjacency8; r28 instruments byte-identical (FPreserveR28).
Selftest28 cases and the persisted 10-mutant witness are bounded, not exhaustive mutation coverage.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| generated-config-projection | Reproduce a pinned benchmark generator's serialized-text config projection offline, with occurrence provenance, changed-field census and output-ordinal mapping, without executing upstream code | `python3 plans/config_projection.py --summary`; `plans/fixtures/r29/mutation_witness.py`; round29-calibration/repair-*; round29 Gate | 29 |

Round29 final-package correction: controls are31 selftest cases and12 persisted mutants, not the earlier
28/10 build-stage counts. Final source rows76 (seven additions, all tierA), knowledge/index37/37.
Independent portable oracle compares2436objects/4248changed leaves/1435provenance rows,0disagreements.
The exact final candidate is freeze-v5 (c4412f67…); v1–v4 remain historical. No score changed.

### Round29 actual measured revision

Landed measurement revision **6baa3090b6cf2d50e56b94b806a69f41220081df** has tree33d75ccd… exactly equal
to the pre-landing trial tree. Actual Gate1admission/1passed/0failed/77reports and exact-byte proof exit0.
C1 remains812/812/3/2436; selftest31, persisted mutants12/12, independent oracle0disagreements across
2436objects/4248changed leaves/1435provenance rows. Sources76/malformed0, knowledge/index37/37.
Historical329/318/0/6/5 and P4's48MATCH/1SUPERSEDED/2offline remain; OOP32 is additive, not matched.
Evidence: round29-calibration/{actual-gate.txt,actual-byte-proof.json,actual-census.json,trial-landed-tree-proof.json}.
These are author-side measurements; separate non-author closure remains pending.

## Round 29 — attempt 2 (hyaku run 6, 2026-10-25): assimilation + standing adoption gate

Baseline `1f3b0f1ec41ec297130e8944ff97968d32324632`; frozen prereg
`plans/round-29-attempt2-claims.md`, freeze commit `8c14a5dcd15ac364a352d544660c69f521c3a6af`.
Attempt 1 above is unchanged history; this attempt claims nothing it claimed.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation — one admitted task-validity instrument entry | **coverage** (lowest non-retired axis, tied at 7) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json` → `entries=0 indexed=0 cited_rows=0 …` exit 1 (do-nothing control, committed at freeze) → after: same command `--census` → `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok` exit 0. Registry 76 → 82 rows (S077–S080, S090, S091); knowledge files 37 → 38; knowledge index rows 37 → 38; SOURCES census exit 0 (`corpus/evidence/round29-attempt2/census-after.txt`) | **7 → 7 held** — expansion is real (a named frontier bullet moves from unopened lead to an admitted checklist), but the canonical coverage number stays capped by the open round-25 L0 and this entry does not move it. No waiver, no conversion. |
| C2 standing source-adoption gate (capability acquisition) | operability | before: `git cat-file -e 1f3b0f1ec41ec297130e8944ff97968d32324632:plans/sources_adopt.py` exit 128 → after: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=10 failed=0` exit 0; the tool refuses a re-append of the five landed ids (`collisions=5`, exit 3), builds the block on the pre-append registry (exit 0), and its selftest kills the five mutants the mutation-tester ran, including the two survivors found in the first round of that test | **8 → 8 held**; capability row added |

Other axes held: depth 9, novelty 7 (no prior-art or phenomenon claim), freshness 8 (census,
`grader.py`, `plans/round28_census.py` and `plans/config_projection.py` re-run this round — see
`LOG.md`), adjacency 8 (the package's card/grader material is routed as next-round candidates, not
absorbed), calibration 8 (two honest corrections recorded below). Claims measured on the landed
commit; this is an author-side measurement and separate non-author closure decides admission.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| source-adoption-gate | Validate a staged registry slice before appending — id collisions under the census's own 0–3-space anchor, 11-cell/escaped-pipe schema, prose-`recheck` normalization to the frozen access date, `used-by` projection to admitted entries — and re-derive an adoption round's landed state with one command | `python3 plans/sources_adopt.py --selftest` (10 cases, exit 0); `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`; `corpus/evidence/round29-attempt2/` | 29 |

Calibration corrections carried forward rather than smoothed: (a) the first frozen selftest
conflated two fixtures (M92); (b) the package's two count cells named the wrong unit and the round
re-derived 89 task directories / 108 `finalpool` directories (M94). Both are in
`corpus/lessons/round-29.md` §Attempt 2.

## Round 30 (hyaku run 6, 2026-10-25): assimilation round 2, routed-defect closure, quote-validating gate

Baseline `363a4ebfda0599bbc4b4b3cdc27a5f91bcaf37db`; frozen prereg `plans/round-30-claims.md`.
Lowest non-retired axis: **coverage 7**, tied with novelty 7; the tie-break is the frozen prereg's
"most falsifiable with sources an on-host tool can open" and the stagnation waiver is unavailable
(saturation line 8, novelty below it, a capability row entered at round 29). Round shape: two v1
waves, 36 build + 33 falsify seats (69 total).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation round 2 — the contamination-transparency card admitted as an amendment | **coverage** (lowest non-retired, tie-break) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-30/adoption-expect.json --census` → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` exit 1 (freeze control, `.ufo/waves/round-30/claims/control-nothing.txt`) → after: same command → `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok` exit 0 (`corpus/evidence/round30/adoption-after.txt`). Registry 82 → 88 rows (S081–S086, tier A 76→78, B 4→8); knowledge files 38 → 39; index rows 38 → 39; census exit 0 | **7 → 7 held — improved (counts)**; axis *coverage (surfaces)*, held by the open round-25 L0 cap. Counts it moves: registry 82→88, knowledge files 38→39, index rows 38→39 (parity 39/39); frontier bullet 2 **partly** discharged (card format + gate; hidden-test-governance releases stay unopened). Counts it does not move: no `PROVINCE.md` round-30 section, so the coverage/surfaces leg is unchanged. The bytes are a published four-field protocol (S081) crosswalked into the tabulated designs plus the re-grounded CG gate; S2's tri-state flag is the only surviving field delta. Not core, not real expansion. |
| C2 calibration — the five routed defects D1–D5 closed | **calibration** | before: `python3 plans/round30_defects.py --lane .` → `DEFECT D1/D2/D3/D4/D5`, `defects=5`, exit 1 (`.ufo/waves/round-30/claims/defects-before.txt`) → after: same command → `defects=0`, exit 0, with D1 judged on the committed blob, D2's count re-derived in `grep -rn` line units, D3 recomputed 9→8, D4 requiring the addendum in `HEAD:`, D5 accepting either repair branch | **8 → 8 held** — five self-assessment/repo mismatches closed; the counter itself was tightened four times after reviewers found gameable paths, and the tightening is disclosed in the lesson rather than folded into the score |
| C3 operability — the adoption gate validates quotes | **operability** | before: `git show 363a4ebf:plans/sources_adopt.py` has no quote mode (`--quote-file … --artifact …` → argparse exit 2) and `--selftest` prints `cases=10` (`.ufo/waves/round-30/claims/gate-before.txt`) → after: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=14 failed=0`, exit 0 (`corpus/evidence/round30/gate-selftest-after.txt`), with a located-quote accept path, exit 6 for over-long, exit 7 for absent-from-artifact | **8 → 8 held**; capability row added. Scope, stated so the row cannot overclaim: the gate proves *the bytes it was handed contain these strings* — it does not bind the artifact to the cited URL, its 25-word cap is inert for CJK (a 46-character Chinese span is 1 word), and PDF text layers must be extracted before quotes can locate. |

Other axes held: depth 9 (the entry adds a field mapping against a published union table, no new
instrument claim), novelty 7 (no prior-art or phenomenon claim; S091 already prices the sibling
checklist, and the card is declared an amendment to published designs), freshness 8 (census exit 0
at both ends with the same 14 `W04`; six rows re-opened 2026-10-25; the round-29 receipts re-run),
adjacency 8 (the connector found no sibling contest; the round claims no research-method or
secrets-custody surface), coverage as above.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| quote-validating adoption gate | Refuse a registry row whose anchored quote is longer than the contract's 25 words or absent from a named capture, with distinct exit codes beside the schema/collision/`used-by` checks | `python3 plans/sources_adopt.py --selftest` (14 cases, exit 0); `--quote-file <rows> --artifact <capture>` | 30 |

Calibration corrections carried this round rather than smoothed: the D2 repair first shipped a
markdown-emphasis strip that deleted the `*` in `corpus/knowledge/*.md` and made the check
unsatisfiable for any lesson bytes (caught by a falsify seat, not the counter); D1's first receipt
planted the wave file's eight-field line while the report quotes the seven-field one; the staged
S081/S082/S085 anchor quotes were respectively over the cap, pointed at a section that does not
exist, and flattened fullwidth quotes. All four are in `corpus/lessons/round-30.md` §Mistakes and
§Round 30 admission.

## Round 31 (hyaku run 6, 2026-10-25): verifier execution model, round-30 routed-defect closure, capture-to-citation binding

Baseline `0883e72ef8474ca42ac1a54eb0273079f1507035` (local = remote, `ahead=0`); frozen prereg
`plans/round-31-claims.md`. Lowest non-retired axis: **coverage 7**, tied with novelty 7; tie-break is the
frozen prereg's "most falsifiable with the sources an on-host tool can open", and no stagnation waiver is
available (saturation line 8, novelty below it, a capability row entered at round 30). Round shape: two v1
waves, 36 build + 32 falsify seats (68 total).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation round 3 — the benchmark verifier execution model admitted | **coverage** (lowest non-retired, tie-break) | before: `python3 plans/adoption_check.py --expect .ufo/waves/round-31/adoption-expect.json --census` → `entries=0 indexed=0 cited_rows=0 rows_present=0 rows_mined=0 usedby_ok=0 census=ok` exit 1 (`.ufo/waves/round-31/claims/control-nothing.txt`, hardened with the expect digest) → after: same command → `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0 (`corpus/evidence/round31/adoption-after.txt`). Registry 88 → 91 rows (S092, S093, S100); knowledge 39 → 40; index 40 → 40; second receipt `python3 plans/round31_c1_verify.py --lane .` → `checks=6 defects=0` exit 0 (`corpus/evidence/round31/c1-verify-after.txt`), closing the frozen counter's content-blindness | **7 → 7 held — improved (counts)**; coverage *surfaces* did not move (no new `PROVINCE.md` section), so the row records the ledger delta, not a raised number |
| C2 calibration — the ten routed defects R1–R10 closed | **calibration** | before: `python3 plans/round31_defects.py --lane .` → ten `DEFECT` lines, `checks=10 defects=10`, exit 1 (`.ufo/waves/round-31/claims/defects-before.txt`; re-derived from the `0883e72` blobs after R6's check was tightened, `corpus/evidence/round31/defects-before-tightened.txt`) → after: same command → `checks=10 defects=0`, exit 0 (`corpus/evidence/round31/defects-after.txt`) | **8 → 8 held** — ten self-assessment/repo mismatches closed; the counter itself was corrected four times (R2 wrap, R6 substring trap, R6 `.pdf` locator, R7 two-string guard) after seats proved each gap, and the corrections are disclosed in `corpus/lessons/round-31.md` §Mistakes rather than folded into the score |
| C3 operability — the adoption gate binds a capture to the row's citation | **operability** | before: `git show 0883e72:plans/sources_adopt.py` has no `--url-map` (argparse exit 2) and its selftest prints `cases=14` (`.ufo/waves/round-31/claims/gate-before.txt`) → after: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=17 failed=0` exit 0 (`corpus/evidence/round31/gate-selftest-after.txt`), with exit 8 for a capture mapped to a different document and exit 9 for an unmapped capture, proven end-to-end through the CLI (`corpus/evidence/round31/gate-cli-exits.txt`: 0 / 8 / 9 / 2) and failure-capable (`corpus/evidence/round31/gate-binding-neutered.txt`: the binding removed → `cases=17 failed=2`, exit 1) | **8 → 8 held**; capability row added. Scope, stated so the row cannot overclaim: the gate binds an artifact to *a URL the row cites* — it does not prove the capture was fetched from it, its map is caller-authored, and the frozen counter (`cases=17 failed=0`) is reachable by three vacuous `case(..., True)` lines, which is why the failure-capability receipt is the load-bearing evidence and not the tally |

Other axes held: depth 9 (the entry adds a code-level finding plus a reproduced grader-mechanism result,
no new instrument claim), novelty 7 (no prior-art or phenomenon claim; the finding is a reading of a
published harness default), freshness 8 (census exit 0 at both ends; 15 `W04` after the append, the 15th
being S100↔S079 disclosed below; the three sources re-opened at their pins on 2026-10-25), adjacency 8
(the connector found no sibling contest and named two report-out slivers), coverage as above.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| citation-bound adoption gate | Refuse a registry row whose located quote comes from a capture that is not the document the row cites — `--url-map` artifact→cited-URL, exit 8 on mismatch, exit 9 on unmapped, bound on any containing artifact against any cited URL, with the round-30 summary line left byte-identical when no map is supplied | `python3 plans/sources_adopt.py --selftest` (17 cases, exit 0); `--quote-file <rows> --artifact <capture> --url-map <map.json>` | 31 |
| adoption second receipt | Re-derive an adoption's *content* literals the frozen counter cannot see — frozen entry path, access-date literal, per-row citation identity, pinned revisions, index-title substance, control-receipt digest | `python3 plans/round31_c1_verify.py --lane .` → `checks=6 defects=0`; `--selftest` | 31 |

Calibration corrections carried this round rather than smoothed: the counter's R6 test first greened its
own repair (a substring trap), then mis-credited the staged `.pdf` against the registry's landing URL; R7's
first version was a two-string guard that greened while the mis-description survived; R2's first version
compared unwrapped text against a wrapped sentence; C3's first landing put the quote-mode body inside an
`elif`, making the CLI unreachable while the selftest stayed green. All five are in
`corpus/lessons/round-31.md` §Mistakes with the seat that found each.

**Corrections to earlier rows, appended (the superseded text stands as written).** (a) Round 30's C3 row
says the gate "does not bind the artifact to the cited URL" — that gap is closed by this round's
`--url-map`; the residual limits are the ones stated in the C3 row above. (b) Round 30's C1 row quotes
"S2's tri-state flag is the only surviving field delta"; the entry's field is four-valued
(`controlled`/`not_controlled`/`unknown`/`n/a`) and the surviving delta is the card-level *field*, not its
vocabulary (`corpus/knowledge/contamination-transparency-card.md:72-75`).

**Corrections to this round's own rows, appended (2026-10-25, after the falsify wave; the cells above stand
as written).** (a) The round-shape sentence says "36 build + 32 falsify seats (68 total)"; the committed
falsify registry holds **36** members (`.ufo/waves/round-31/falsify/swarm-registry.json` → `len(members)=36`),
so the shape is **36 + 36 = 72** and the round total is 72, not 68 — the "32" was a pre-dispatch estimate
that the registry supersedes. (b) The C1 row's "index 40 → 40" is wrong: the index was **39 → 40**
(`grep -c '^| \`knowledge/' corpus/README.md` → 39 at `0883e72`, 40 after the admission; knowledge files
39 → 40 likewise). (c) The C2 row cites `corpus/lessons/round-31.md` §Mistakes, which lands in `d6aa66e`,
one commit after the row's own commit `dbb07364` — the reference resolves at the round tip, not at the row's
commit, and the closure should read it there.

## Round 32 (hyaku run 6, 2026-10-25): assimilation refusal, routed-defect partial, catalog freshness failure

Baseline `f20a1097`; landed lane tip `bcd2a6c` (closure `112091c`). Frozen prereg
`plans/round-32-claims.md` (freeze `0d32691d`). Lowest non-retired axis: **coverage 7**, tied with
novelty 7; tie-break "most falsifiable with sources an on-host tool can open". Round shape: two v1
waves, 34 build + 34 falsify seats in the surviving registries. This section lands late under
round 33 — its absence at the round-32 tip is routed defect N2.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 shokuknow assimilation round 4 — grader-semantics entry under staged ids | **coverage** (lowest non-retired, tie-break) | before: `entries=0 …` exit 1 (freeze control `.ufo/waves/round-32/claims/control-nothing.txt`) → after: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=fail` exit 1 (`corpus/evidence/round32/adoption-after.txt`) — staged S094/S097 collided with live ids; staged S101/S102 identify unrelated SWE-bench sources | **7 → 7 held** — **refused as declared**; four refusal rows recorded (S094, S097, S101, S102), the committed draft stays unadmitted |
| C2 calibration — the seven routed defects D1–D7 | **calibration** | before: `checks=7 defects=7` exit 1 → after (draft-state): `checks=7 defects=5` exit 1 (`corpus/evidence/round32/defects-after.txt`); R3/R4 landed (CLI receipt regenerated, sources_adopt.py SKILL row), R1/R2/R5/R6/R7 remained red | **8 → 8 held** — **incomplete**; a partial receipt is not closure |
| C3 freshness — public model catalogs re-probed | **freshness** | before: stale entry, exit 1 → after: `hf=ok openrouter=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0` (`corpus/evidence/round32/catalogs/after.txt`) — the frozen zero-delta predicate could not honestly pass with HF's default-projection gap | **8 → 8 held** — **failed as declared**; the frozen predicate was never relabeled |

Other axes held: depth 9, novelty 7 (no prior-art claim), adjacency 8 (connector found no contest),
coverage as above. Non-author closure `corpus/lessons/round-32-verifier-spotcheck.md` confirmed all
three dispositions and recorded the residual defect: ten wave paths untracked at the pushed tip —
closed by round-33 commit `c227e486`.

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| — none — | the round landed no new capability; the C1 candidate was refused and C3 failed as declared | `corpus/lessons/round-32.md` | — |

Corrections carried: the staged S094 row misstated the executed tolerance (0.05 at the call site,
not the 0.1 signature default) and overbroadened a fail-open claim (credential failures fall through
to implicit None — fail closed); the staged S097 anchor dropped one L in "LLMs-as-judges". All three
are in `corpus/lessons/round-32.md` §Mistakes.

## Round 33 (hyaku run 7, 2026-10-25): renumbered assimilation, routed-defect closure, byte-retained catalogs

Baseline `112091c2d9`; frozen prereg `plans/round-33-claims.md` (freeze `f0b20aea` + `c227e486`).
Lowest non-retired axis: **coverage 7**, tied with **novelty 7**; no stagnation waiver (saturation
line 8, novelty below it, a capability row entered round 31). Three claims, three distinct axes;
measurements below reflect the landed counters.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 grader-semantics entry admitted under renumbered ids S103/S104 | **coverage** (lowest non-retired, tie-break) | before: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=1 usedby_ok=0 census=ok` exit 1 → after: `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok` exit 0 (`plans/adoption_check.py --expect .ufo/waves/round-33/claims/adoption-expect.json --census`) | **7 → 7 held** — admitted source coverage improved; no new knowledge/index row and S093's claimed used-by transition was already true at baseline |
| C2 six routed defects N1–N6 closed | **calibration** | before: `checks=6 defects=6` exit 1 → after: `checks=6 defects=0` exit 0 (`python3 plans/round33_defects.py --lane .`) | **8 → 8 held** — repairs are present; mutation wave found the counter's semantic blind spots, so no score raise |
| C3 catalog re-probe with committed bounded raw bytes | **freshness** | before: `raw=absent` exit 1 → after: `raw=ok hf_models=50 or_models=467 hf_schema_delta=4 or_schema_delta=0 verify=ok` exit 0 (`python3 plans/catalog_probe.py --verify --lane .`) | **8 → 8 held** — bounded raw responses and offline checks landed; OpenRouter 467 is its `total_count` field, and `--verify` does not authenticate origin |

C1 second receipt: `python3 plans/round33_c1_verify.py --lane .` → `checks=8 defects=0`, exit 0 (`corpus/evidence/round33/adoption-after.txt`).

C1 baseline correction: the frozen claim file states 40 knowledge/index rows, but `git ls-tree`
at `112091c2` and the matching README count both show **41 → 41**. The candidate entry and index
row pre-existed unadmitted; the round's additions are S103/S104 (registry 95 → 97). The frozen
`S093 used-by gains` sentence is also false as a transition; the state was already present at freeze.
The final C1 state predicate passes, but neither false transition is credited.

Capability added to the global repertoire table: `offline-catalog-receipt-verification`, first
working round 33. Its documented boundary is internal byte/count consistency, not endpoint
authentication or a full unpaginated listing.

The three counter outputs match their measured after states; C1's frozen S093/control baseline clauses are inaccurate, and C3's anti-fabrication kill-rule assurance is falsified. Round-32 C3 zero-delta remains failed; no numerical axis score changed. The lane tip and final dispositions are in the round-33 fleet report.

## Planned (round 34)

- **Coverage (7, tied lowest with novelty):** advance the remaining benchmark scoring-code frontier by opening one pinned Terminal-Bench 2.0 task evaluator and grounding its comparison against that task's expected artifact. Freeze the exact task/pin and source gate before any scoring.

- **Calibration (8):** prepare a new frozen claim to harden `round33_defects.py`'s N1–N6 counter against the measured index-vs-HEAD, heading-only, width/newline, and token-co-occurrence mutants; keep this round's frozen predicate and score unchanged.

## Round 34 — coverage attempt + calibration counter attack, 2026-10-25 (honest stop)

Baseline lane tip `5022357cc69334e83b5a2f76c34daea440077a57`; claims froze at `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`. Lowest non-retired axis: coverage 7, tied with novelty 7; coverage selected by frozen tie-break (local pinned task source vs unavailable identity-verified endpoint). No stagnation waiver.

| Claim | Axis | Frozen before → observed after | Score / verdict |
|---|---|---|---|
| C1 Terminal-Bench 2.0 `protein-assembly` evaluator coverage; counter `plans/round34_c1_verify.py --lane .` | coverage (lowest) | before: entry/counter absent at freeze, registry 97, S105+ absent; after: evaluator captured but no admissible registry/knowledge/README package; counter review finds V3–V8 false-green paths and V7 red on the truthful freeze receipt (`.ufo/waves/round-34/build/R34ReviewCounterC1.md`) | 7→7 held; not admitted; no axis score move |
| C2 counter hardening; `plans/round34_defects.py`, `plans/round34_mutate.py` | calibration | before: both tools absent, `round33_defects.py` `checks=6 defects=0`; after: candidate counter draft's selftest was not green and the 8-mutant harness did not produce `MUTANTS total=8 detected=8`; clean-tree N3/N4/N7 and mutant mapping failures (`R34ReviewClaimsFile.md`, `R34CriticC2.md`, `R34MutC2Harness.md`) | 8→8 held; not admitted |

All other recorded scores held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. C1/C2 are causally separable in their declared artifacts, but both failed frozen admission. No capability was demonstrated and entered.

### Planned (round 35)

- Lowest coverage 7 remains tied with novelty 7; choose the most falsifiable frontier move against an opened local source, with a control that the frozen counter cannot reach.
- Calibration 8: repair and mutation-test the counter/harness failure classes discovered in round 34; do not treat round-34 draft tools as landed capability.

## Corrections recorded in round 35 — routed defects from the round-34 closure (appended 2026-10-25)

- **D4 correction (round 34 C2):** the round-34 C2 row's "candidate counter draft's selftest was not green" is wrong. The counter draft's selftest was green — `R34C2CounterDraft.md:8` records `SELFTEST cases=10 failed=0`; the red selftest was the mutation harness — `R34MutC2Harness.md:12` (continued on line 13) records exit 1 with `SELFTEST green failed (1)`. Both files are under `.ufo/waves/round-34/build/`. The C2 verdict (not admitted, 8→8 held) is unchanged. Ledger row `R34-D4` in `corpus/defects.jsonl`.

## Round 35 (hyaku run 7, 2026-10-25): one TB2 grader read and executed; routed defects move into a ledger

Baseline `58a19f37312e1b22fd2a7957bdfc6bb7832aadd0`; frozen prereg `plans/round-35-claims.md` (freeze
`11d64530179b78e33ba6074fc77d63d36ee7ac31`). Lowest non-retired axis: coverage 7, tied with novelty 7;
coverage chosen by the frozen tie-break; the coverage score stays capped by the open L0 question
(`.ufo/l0-questions.md:163`). No stagnation waiver.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 pinned TB2 `protein-assembly` grader admitted with an executed 18-case probe (S105–S107) | **coverage** (lowest, tied) | `python3 plans/round35_c1_verify.py --lane .`: before `checks=6 defects=5` exit 1 (`.ufo/waves/round-35/claims/control-c1-nothing.txt`) → after `checks=6 defects=0`, `PREDICATE C1 pass`, exit 0 at `4fe72a9a` | **7 → 7 held** (L0 cap); frozen predicate met; the counter does not prove entry or teaches quality: eight one-word quotes and `junk` teaches cells pass V2/V3, and a stub that replaces the frozen probe passes V5 (`R35CritControls`, `checks=6 defects=0`) — see post-hoc `plans/round35_hardening.py` |
| C2 persistent routed-defect ledger; round-34 D1–D5 closed | **calibration** | `python3 plans/defect_ledger.py --lane .`: before `rows=5 closed=0 observed_pass=0 mismatches=0` exit 1 (`claims/control-c2-nothing.txt`) → after `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit 0 at `dfcd294c` | **8 → 8 held**; frozen predicate met; D4/D5 checks accept labelled-but-false lines (`R35CritC2`) and D1 is a working-tree check, so no score raise |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Capabilities entered:
`pinned-grader-probe`, `routed-defect-ledger` (table above, first-working round 35). Registry 97 → 100
rows (tier A +3); knowledge files / index rows 41/41 → 42/42; census exit 0 before and after (15 W04).
Post-hoc hardening (not a claim rule): `python3 plans/round35_hardening.py --lane .` passes on the
landed lane and fails on each of five seat counterexamples
(`corpus/evidence/round35/hardening-counterexamples.txt`).

### Planned (round 36)

- Calibration: promote the round-35 hardening clauses (frozen-instrument digest, directional
  correction clauses, pinned capture digests, distinct multi-word quotes, whole-tree untracked) into
  the ledger and C1-class counters under a new freeze, with an adversarial junk-package control run
  by a critic seat BEFORE any data.
- Coverage/novelty (tied 7): a second TB2 task grader, or the prior-art-checked instrument, chosen
  against the wave-1 scout reports; keep the frozen predicate and control the same sentence.

- **Round-35 erratum (falsify wave, `F35LogDraft` E1):** the C2 row's "exit 0 at `dfcd294c`" is wrong — at `dfcd294c` R34-D5 is `observed=fail` because `corpus/lessons/round-35.md` was not yet committed; the frozen C2 predicate first holds on committed bytes at `4fe72a9a` and holds at the final tip.

## Round 36 (hyaku run 7, 2026-10-25): hardened package gate, one more TB2 grader executed

Baseline `b662a5d6dd370491049e4206818373c61be44816`; frozen prereg `plans/round-36-claims.md` (freeze
`3241b86c`; Amendment 1 `acbda2f3`, a pre-scoring one-line probe repair, disclosed in the prereg). Lowest
non-retired axis: coverage 7, tied with novelty 7; coverage chosen by the frozen tie-break (a pinned local
source and a runnable instrument; novelty has no opened source and the round-35 scout priced the probe
pattern as established). Coverage stays capped by the open L0 question (`.ufo/l0-questions.md`, `kengaku |
round-33`). No stagnation waiver.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 hardened package gate `plans/pkg_gate.py`; round-35 routed defects R35-D1..D4 closed | **calibration** | `python3 plans/round36_c1_verify.py --lane .` on a clean clone: before `FIXTURES total=14 … unevaluated=14`, `rows=4 closed=0 observed_pass=0` exit 1 (`.ufo/waves/round-36/claims/control-c1-nothing.txt`); the round-35 counter accepts all seven junk packages (`control-c1-legacy.txt`, `LEGACY accepted=7/7`) → after `FIXTURES total=14 false_green=0 false_red=0 unevaluated=0`, `rows=4 closed=4 observed_pass=4 mismatches=0`, `PREDICATE C1 pass`, exit 0 (receipt `.ufo/waves/round-36/integrate/measure-final.txt`) | **8 → 8 held**; frozen predicate met; the battery is gameable (`R36CritBattery`: a gate keyed on fixture names/markers scores the same clean line, 8 cues) and leaves eight advertised clauses without a fixture (`R36RevClaims` FG1), so the gate is attacked by clause in wave 2 and the limits are reported |
| C2 pinned TB2 `regex-log` grader admitted with an executed 24-case probe (S108-S110) | **coverage** (lowest, tied) | `python3 plans/round36_c2_verify.py --lane .`: before `checks=6 defects=4` exit 1 (`control-c2-nothing.txt`) → after `checks=6 defects=0`, `PREDICATE C2 pass`, exit 0; probe `cases=24 observed_pass=8 observed_fail=16 mismatches=0` | **7 → 7 held** (L0 cap); frozen predicate met; the counter admits a junk package (`R36CritC2Counter`: `checks=6 defects=0`), so the landing rests on the wave-2 non-author re-reads of the entry, not on the counter |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Capabilities entered
(table above, first-working round 36): `package-gate`, `pattern-valued-grader-probe`. Registry 100 → 103
rows (tier A +3); knowledge files / index rows 42/42 → 43/43; census exit 0 before and after (15 W04).
Assimilation: `considerthese/2026-10-25.md` proposal 2(c) — begun (`pkg_gate.py --rerun` re-runs one
receipt), proposals 1 and 3 untouched; `merge/kengaku/` re-screened: `grader-predicate-input-types.md`
held (admit-candidate for a later claim), `grader-fixture-probe-stage3.md` refused.

### Planned (round 37)

- Calibration: attack the gate itself — one byte-level mutant per defect class run against
  `plans/pkg_gate.py` inside the frozen battery's fixture root, null mutant included; survivors are gate
  limits. Promote the `r35_d1..r35_d4` checks into one persistent ledger checker so they re-run at every
  tip (the debt `R36ConsiderMine` F1 names for proposal 2(a)).
- Coverage/novelty (tied 7): a third TB2 grader of a different class (a service/state grader), or the
  prior-art-gated requirement-class census across the two admitted graders; keep the frozen predicate and
  control the same sentence. Candidates and sizes: `.ufo/waves/round-36/build/R36ScoutNextTasks.md`,
  `R36PlanNext.md`.

### Round-36 close and errata (appended; the rows above are not rewritten)

- **Wave 2 was not dispatched.** The operator ended the run; `falsify-spec.json` (34 seats) was planned and
  committed, never taken. The round is wave 1 only: 40 seats, 40 reports, 0 dead
  (`.ufo/waves/round-36/build-results.json`). Every sentence above that says the gate, entry or battery "is attacked in
  wave 2" records the plan; the gate's clauses are tested only by the four wave-1 candidates, the frozen battery and
  the wave-1 mutation seats (`R36MutC2W2W3` 20/21, `R36MutC2W4W5` 14/14, `R36MutLedgerChecks` 24/24).
  The C2 landing therefore rests on wave-1 re-reads (`R36IndepRegexGrader` 24/24, `R36ProbeRerun`, `R36OracleRun`,
  `R36ReopenPins` 5/5) and on a counter that a seat showed admits a junk package.
- **Stale frozen-digest block** in `plans/round-36-claims.md`: corrected by the appended digest table there
  (`R36RevClaims` FG3).
- **`measure-final.txt`**: `.ufo/waves/round-36/integrate/measure-final.txt` carries the clean-clone measurement of the
  final tip, with the tip hash inside it.
- **Wave-1 findings not absorbed** (routed, open): `R36CritScope` wording fixes F3-F6, F8, F10 (oracle framing, four
  negative-space refusals, a 134-word PROVINCE rewrite at `build/R36CritScope/province-rewrite.txt`, the `coverage/surfaces`
  vs `coverage/constructs` sub-row label, capability-definition wording) — F1/F2/F7/F9 were applied; `R36RevProbePred`
  (two confounded cases, `ip-no-left-boundary` and `ip-no-right-boundary`, die on lines other than the boundary
  line they name: the entry's `What decides it` cells for those two rows are therefore not independent evidence);
  `R36CritUnenforced` findings F1-F4 are in the entry as post-hoc observations only.
- **Plan wording for novelty**: `R36ScoutPriorArt` priced the instrument `incremental` (6 hits); no novelty claim was made and the
  axis is unchanged.

## Round 37 (hyaku run 8, 2026-10-26): advertised gate classes made demonstrable, a third TB2 grader executed

Baseline `3ea9a1d9005cc07d0a5ce69f4ebf53a81fbcecdd`; frozen prereg `plans/round-37-claims.md` (freeze
`ca790460e9b74d4dc5870c878affd13cc9c4437a`; first recorded probe run `5c7b34e9223f460a440596e3a76bdae8bfdd37d8`).
Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen by the frozen tie-break (a pinned local source and
an offline sandbox exist; the round-36 planning seat priced the novelty candidate as covered by published work). Coverage
stays capped at 7 by the open L0 question (`.ufo/l0-questions.md`, `kengaku | round-33`). No stagnation waiver.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 advertised package-gate classes demonstrated by a fixture: 55 frozen one-branch silence mutants against `plans/pkg_gate.py` (freeze digest `ea638822…`, unedited) over the round-36 battery plus `plans/battery37/*.py` | **calibration** — mismatch count between what the gate's docstring, `corpus/QUALITY.md` Q24 and the `package-gate` capability row advertise and what the lane's tests show | `python3 plans/round37_c1_verify.py --lane .` on a clean clone: before `BATTERY fixtures=14 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=5 survived=50 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-37/claims/control-c1-nothing.txt`; also on committed bytes at `44b7298a`, `claims/measure-before-committed.txt`) → after `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0 (`.ufo/waves/round-37/integrate/measure-final.txt`) | **8 → 8 held**; frozen predicate met; mismatch count 50 → 0 on the frozen mutant list. No score raise: the denominator is the lane's own mutant list (branches nobody wrote a mutant for are invisible) and demonstration is observational |
| C2 pinned TB2 `configure-git-webserver` grader admitted with an executed 22-case sandbox probe (S111–S113; S114 prior report) | **coverage** (lowest, tied) — `coverage/surfaces`: one §Frontier sub-bullet narrowed for one task, one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 43→44, SOURCES 103→107; `coverage/constructs`: unchanged (the executed-sample class sentence is a property of this capture's evidence, not a construct claim) | `python3 plans/round37_c2_verify.py --lane .`: before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 (`claims/control-c2-nothing.txt`) → after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (`integrate/measure-final.txt`); probe `cases=22 observed_pass=9 observed_fail=13 mismatches=0` | **7 → 7 held** (L0 cap); frozen predicate met; the counter admits an informed filler package and its spec template is not digest-pinned by the counter (`build/R37CritC2Counter.md` v1, v4), so the landing also rests on the wave-2 non-author re-reads |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. Capabilities entered (table above,
first-working round 37): `gate-mutation-harness`, `service-grader-probe`. Registry 103 → 107 rows (tier A +3, tier B +1);
knowledge files / index rows 43/43 → 44/44; census exit 0 before and after. Assimilation: `considerthese/2026-10-25.md`
proposal 2(a) — `plans/ledger_tip.py` re-runs all nine routed-defect rows at the tip (`rows=9 closed=9 observed_pass=9
mismatches=0`); 2(b) and 2(c) stay unbuilt. `merge/kengaku/` re-screened: 0 admit, 3 hold, 7 refuse
(`build/R37ScoutMergePkg.md`). Frontier mistake: S110's 63-hex anchor digest; `plans/anchor_digest_check.py` flags it at
`3ea9a1d9` (`rows=103 tokens=11 defects=5`, with four true-but-uncaptured digests S070/S072-S074) and clears to 0 after the
appended erratum and four captures (`integrate/measure-final.txt`).

### Limits named at freeze, and found in wave 1

- C1: the excluded branches named in the claims stay unclaimed; a kill records a result difference, not a reason.
  Wave 1 showed the counter alone is uninformative: a hostile two-module battery whose `--rerun` probe detects the
  running gate copy reaches the same `killed=55` line (`build/R37CritC1Battery.md`). The landed battery passes an
  attribution audit the counter lacks — every kill removes the mutant's own clause on a fixture of the matching
  subcommand, `UNATTRIBUTED=0` (`build/R37CritC1Battery/receipts/attr-honest.txt`); the hostile one prints `UNATTRIBUTED=49`.
  The L1 re-built that audit as `plans/round37_c1_attribution.py` (post-hoc, not the frozen rule): landed battery
  `ATTRIBUTED 55/55 UNATTRIBUTED=0` (`.ufo/waves/round-37/integrate/c1-attribution.txt`); the critic's side-channel battery
  in a scratch clone reaches the frozen `PREDICATE C1 pass` but `ATTRIBUTED 6/55 UNATTRIBUTED=49`
  (`integrate/c1-attribution-hostile.txt`).
- C2: the probe never runs the oracle, the task image or a real git push; in the sandbox the git step never executes, so
  "the git step's failure is ignored" is a static reading, not an observation (`build/R37CritCases.md` §2.1); four case
  labels are weaker than they read (same section). A wave-1 seat ran the task's real image (`build/R37DockerOracle.md`);
  that run is outside PROVINCE's admitted instrument and is routed, not absorbed.
- C2 counter: V2 reads `plans/pkg-spec-r37.json` from the tree without pinning its digest, so a spec whose `probe_cmd`
  cats the receipt passes (`build/R37CritC2Counter.md` v4/v5). At the landing tip the spec equals its freeze digest
  (`.ufo/waves/round-37/claims/frozen-digests.txt`, re-checked in `integrate/measure-final.txt`); the next counter must pin it.

### Planned (round 38)

- Calibration: pin every input the C2-class counter reads (spec template, dry table, probe) inside the counter, and add the
  missing-coverage mutants wave 2 found as a new frozen list; the round-37 list is not edited.
- Coverage/novelty (tied 7): a fourth TB2 grader class (file-tree or git-state: `fix-git` or `sanitize-git-repo`), chosen
  against `.ufo/waves/round-37/build/R37PlanNext.md`; keep the frozen predicate and control in the same sentence.

### Wave 2 outcome (appended after WAVE-DONE falsify; 37 seats, 37 reports, `.ufo/waves/round-37/falsify-results.json`)

- Re-measures agree: C1 re-run `killed=55/55` (`F37C1Rerun`), same under Python 3.12/3.13 and two hash seeds (`F37C1RerunPy313`);
  C2 re-run pass and probe byte-equal (`F37C2Rerun`, `F37ProbeOnTip` 3/3 adversarial environments); S111-S113 re-opened live
  3/3 with quotes 3/3 (`F37ReopenRows`); battery code review 0 defects (`F37RevBatteryCode`); no line removed anywhere
  (`F37CritNoHarmDiff`); C2 landed-package mutants 10/10 caught (`F37MutC2Counter`); probe-case mutants 14/14 as predicted.
- Limits found (reported, nothing frozen edited): 36 non-frozen extra gate mutants, 23 killed / 13 survived across the nine
  modules (`F37XMut*`) — the frozen 55 are demonstrated, near-variants of the same clauses often are not; an overfit gate can
  match every battery declaration with 2 cues (`F37CritOverfit`) and the renamed run carries 5 content cues (`F37CritRenamed`);
  6 of the 55 mutant labels have no advertising sentence in the self-assessment texts (`F37CritC1Axis`); the anchor tool
  misses 4 of 5 code mutants of itself and 1 of 4 data mutants (`F37MutAnchorTool`, `F37AnchorRerun`); the attribution audit
  catches 1 of 4 of its own mutants (`F37MutAttribution`); `ledger_tip.py` false-reds (exit 1, not 2) when the source clone
  has no local `master` ref, because two pin checks hardcode `refs/heads/master` (`F37NoHarmSweep` N1; green on the
  measurement clone, `integrate/measure-final.txt`).
- Wording defects found, not yet repaired: requirement map 2/4 rows disputed (`F37CritC2Map`), 13 overclaim sentences
  (`F37CritC2Overclaim`), 3 quote claim cells and 4 prose sentences unsupported in the entry (`F37RevEntryQuotes`; no quote
  fabricated or mislocated), lesson 5 / QUALITY 6 / SCORECARD-LOG 2 / SKILL-README 1 / PROVINCE 1 defects, 3 of 60 self-assessment
  statements mismatched (`F37CritCalibStatements`), 20 wave-1 findings unaddressed (`F37ConnCrossCheck`). They are routed to
  round 38; the frozen predicates are unaffected.

## Round 38 (hyaku run 8, 2026-10-26): gate behaviours attributed 21/22 (honest stop), a fourth TB2 grader executed

Baseline as read `fc1174f52b150999bef91f2e81da78732ca0eb9f`; freeze `e0a378539a45cc9388c66cfba22f44275131de23` (a child of the
round-37 L1's `21e6251b`, which landed 3 s earlier — lesson header erratum); first recorded probe run `e95cf550`. Frozen
prereg `plans/round-38-claims.md`. Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen (frozen
tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No stagnation waiver. Landing measurement
`.ufo/waves/round-38/integrate/measure-final.txt` (clean `--no-local` clone of `d93b7d68`, `untracked_in_clone=0`).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 advertised gate behaviours the round-37 battery does not demonstrate: 22 frozen mutants N01–N22 of `plans/pkg_gate.py` (unedited, `ea638822…`), attributed kill rule, silence and mirror directions, over round-36 + `battery37` + `plans/battery38/*.py` | **calibration** — mismatch count between what the gate's docstring, Q24/Q27 and the `package-gate` / `gate-mutation-harness` rows advertise and what the battery shows | `python3 plans/round38_c1_verify.py --lane .`: before `BATTERY fixtures=64 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=0 survived=22`, `PREDICATE C1 fail` (`.ufo/waves/round-38/claims/control-c1-nothing.txt`) → after `PINS total=14 mismatched=0`, `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0`, `PREDICATE C1 fail`, exit 1 (`measure-final.txt`) | **8 → 8 held; NOT ADMITTED (honest stop).** The survivor N21 is frozen as `silence` but can only be killed as a mirror (it makes D5 stricter); no battery can meet the frozen predicate (`build/R38BatD5.md` §BLOCKER; `plans/mutant_direction_check.py` → `N21 … MISLABELLED`). Not relabelled after scoring. Also: 3 of 22 `adv` cells name no advertising sentence (`R38CritClaims` §1) and the counter's predicate is reachable by an in-process monkeypatch (`R38CritClaims` §2) |
| C2 pinned TB2 `build-pmars` grader admitted with an executed 22-case sandbox probe (S115 `tests/test_outputs.py`, S116 `instruction.md`) | **coverage** (lowest, tied) — `coverage/surfaces`: one §Frontier TB2 sub-bullet narrowed by one task, one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 44→45, SOURCES 107→109; one edge class new to the executed sample (graded state = a built artefact plus a source tree) | `python3 plans/round38_c2_verify.py --lane .`: before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 (`claims/control-c2-nothing.txt`) → after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, second run byte-equal | **7 → 7 held** (L0 cap). Frozen predicate met; admission also rests on non-author re-reads (`R38CritPytest` 22/22, `R38CritIndep` 22/22 + 3/3) because the counter admits an informed filler (`R38CritC2Counter` §1) |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. No-harm at the landing tip
(`measure-final.txt`): round-37 C1 `killed=55/55` pass, round-37 C2 pass, round-36 C2 pass, anchor check `rows=109 tokens=17
defects=0`, ledger-tip `rows=9 closed=9 observed_pass=9 mismatches=0`, census exit 0, frozen digests 8/8 OK.

### Round-38 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `build-provenance-grader-probe` | Execute a pinned TB2 grader whose graded state is a host-compiled artefact plus a staged source tree, per case in bubblewrap, with frozen predictions and `violates=` tags | `python3 plans/build_pmars_probe.py --lane .` → `cases=22 observed_pass=7 observed_fail=15 mismatches=0`, byte-equal re-run (`measure-final.txt` V2 P10) | 38 |
| `mutant-direction-check` | Report, per frozen gate mutant, which attributed kill directions a battery exhibits and fail on a mislabelled direction | `python3 plans/mutant_direction_check.py --lane .` → `DIRECTIONS total=22 mislabelled=1`, exit 1 on N21 (`integrate/direction-check.txt`) | 38 |
| `tip-receipt-validator` | Re-run every committed probe receipt with a committed re-run command on a clean clone and byte-compare it; tamper control | `python3 plans/tip_receipts.py --lane .` → `receipts=24 byte_equal=4 differ=0 skipped=20`; one flipped byte → `differ` | 38 |

Frontier and routed work (not claims): Q28 (map labels derived from all violating cases) + `## Errata (round 38)` on
`tb2-git-webserver-grader.md` (round-37 D2); Q29 (frozen mutant direction witnessed); `plans/anchor_digest_check.py`
binds each token to its own row's capture (D3); `plans/ledger_tip.py` binds an absent branch ref and refuses with exit 2
(D4); PROVINCE sibling report-out (D6); considerthese 2(c) landed as `plans/tip_receipts.py`. Registry 107 → 109 (tier A
+2), knowledge 44/44 → 45/45, census exit 0 before and after.

### Planned (round 39)

- Calibration (8): a new frozen gate-mutant list that carries N21 as a **mirror** plus the round-38 wave-2 extra
  survivors, every direction stated as laxer/stricter at freeze and checked with `plans/mutant_direction_check.py` at
  the first integration (Q29); the counter must run battery modules out of process so a module cannot patch
  `run_gate` (`R38CritClaims` §2). Alternative priced by `R38PlanNext` §5: mutation-test the lane's tripwire tools
  (anchor check, attribution audit, ledger-tip) — re-price after this round's D3/D4 repairs.
- Coverage/novelty (tied 7): TB2 `git-leak-recovery` @ `2fd12b88` (repository-history-state class; `R38PlanNext` §2:
  the untouched repo passes 4/5, a one-line `echo` passes 5/5), first recorded probe run before any `--rerun` control.

## Round 39 (hyaku run 8, 2026-10-26): undemonstrated gate behaviours killed with witnessed directions; a fifth TB2 grader executed

Baseline as read `b2bdd425fbc042d3075994dae60fe88a51e277ab`; freeze `088f7c36e94ce2f15e6f9aa0c5a5c5b75a1646c8` (a child of the
round-38 L1's late `ef2fba0`, which moved no frozen input — lesson header); first recorded probe run `6a1eb5e1`. Frozen prereg
`plans/round-39-claims.md`. Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen (frozen tie-break), capped
at 7 by the open L0 question `kengaku | round-33`. No stagnation waiver. Landing measurement
`.ufo/waves/round-39/integrate/measure-final.txt` (clean `--no-local` clone of the measured tip).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the gate behaviours still undemonstrated after round 38: 7 frozen mutants M01–M07 of `plans/pkg_gate.py` (unedited, `ea638822…`), N21 carried as `mirror`, round-38 wave-2 survivors, every direction witnessed before freeze, two exit-code legs, battery modules built out of process | **calibration** — mismatch count between what the gate's docstring, Q24/Q27 and the `package-gate` row advertise and what the batteries show | `python3 plans/round39_c1_verify.py --lane .` on a clean clone: before `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=3 survived=4`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-39/claims/control-c1-nothing.txt`) → after `PINS total=26 mismatched=0`, `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0`, `PREDICATE C1 pass`, exit 0 (`measure-final.txt`). Advertised-only recount (M02, M03, M05, M06 reach a sentence; M01, M04, M07 do not — `R39CritClaims` §1): 2 → 0 | **8 → 8 held**; frozen predicate met. No raise: the frozen counter is gameable by a dishonest battery (`R39CritC1Counter` A1/A3/A4/A5); admission also rests on the post-hoc `plans/round39_c1_audit.py` (`AUDIT C1 clean` on the landed battery, A3 replay refused) and on non-author review of `plans/battery39/` (wave 2) |
| C2 pinned TB2 `git-leak-recovery` grader admitted with an executed 25-case sandbox probe (S117 `tests/test_outputs.py`, S118 `instruction.md`) | **coverage** (lowest, tied) — `coverage/surfaces`: one §Frontier TB2 sub-bullet narrowed by one task, one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 45→46, SOURCES 109→111; one edge class new to the executed sample (graded state = a repository's refs, object store and dangling objects plus a flag file and a work-tree digest) | `python3 plans/round39_c2_verify.py --lane .`: before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 (`claims/control-c2-nothing.txt`) → after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, second run byte-equal | **7 → 7 held** (L0 cap); frozen predicate met |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. No-harm at the landing tip (`measure-final.txt`):
round-38 C1 `killed=21 survived=1` as landed, round-38 C2 pass, round-37 C1 `killed=55` pass, round-37 C2 pass, round-36 C2 pass,
anchor check `defects=0`, ledger-tip `mismatches=0`, census exit 0, frozen digests 9/9 OK; `order_check` round 38 exit 1, round 39
exit 0.

### Round-39 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `repo-history-grader-probe` | Execute a pinned TB2 grader whose graded state is a git repository (refs, reflog, object store, dangling objects) plus a flag file, per case in bubblewrap with the task's own setup script, frozen predictions and `violates=` tags | `python3 plans/git_leak_probe.py --lane .` → `cases=25 observed_pass=13 observed_fail=12 mismatches=0`, byte-equal re-run (`measure-final.txt`) | 39 |
| `order-of-operations-gate` | Read committed history and fail when a frozen probe executed before the round's first receipt commit (QUALITY Q30) | `python3 plans/order_check.py --lane . --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt` → `ORDER RESULT FAIL`, exit 1; round 39 → `ORDER RESULT PASS`, exit 0 | 39 |

Frontier and routed work (not claims): QUALITY Q30 (order gate; considerthese 2026-10-25 proposal 2(b)); round-38 closure R2
(N21 relabelled, rc legs, out-of-process build; direction check gains a redundant leg, `R39DirCheckLeg` 3/3), R3 (gate + `##
Errata (round 39)` on `corpus/lessons/round-38.md`), R4 (corrected recheck errata on three TB2 entries; the round-35 entry's
correction lives in the round-39 lesson because that file is fixture bytes), R5 (anchor check binds each digest to its own
locator, `R39AnchorUnion`; ledger-tip prints the audited revision and refuses a stale master, `R39LedgerProvenance`), R1 closed
by the round-38 L1 in `ef2fba0`. Registry 109 → 111 (tier A +2), knowledge 45/45 → 46/46, census exit 0 before and after.

Round-38 errata (from `R39AdvErrata`, verified against the files): N09's and N11's `adv` sentences overstate what the frozen gate
enforces (`F38CritBatE` D1/D2); 3 of the 22 round-38 `adv` cells name no advertising sentence (`R38CritClaims` §1); the round-39
list repeats the shape in M01, M04, M07 (lesson Mistakes row 4).

### Planned (round 40)

- Calibration (8): re-freeze the C1 counter with the four soundness repairs inside the frozen rule (kill re-check, closed
  battery name sets, pins re-hashed after the run, parent-owned fixture dirs — `R39CritC1Counter` §2-§5), then mutation-test the
  lane's tripwire tools: `R39PlanNext` priced 17 frozen mutants (anchor 10, ledger-tip 7) at `killed=0` for the standing
  detectors, and `order_check.py` at 4 of 13 seat-written mutants.
- Coverage/novelty (tied 7): TB2 `db-wal-recovery` @ `2fd12b88` (`R39PlanNext`: task oracle passes 7/7 offline, nop fails 7/7,
  byte-equal reruns); fallback `openssl-selfsigned-cert` with the host OpenSSL 3.6.5 limit declared. Novelty rider priced, not
  filed: grader re-run stability (`polyglot-c-py` fails its second grading).
- Carried: a separately frozen `defect_ledger` check so the order class can enter `corpus/defects.jsonl` with `recurrence=2`.

### Wave 2 outcome (appended after the falsify wave; 34 seats, `.ufo/waves/round-39/falsify/`)

- Re-measures agree: C1 re-run `killed=7` pass and audit clean under two interpreters and two hash seeds (`F39C1Rerun`); C2
  re-run pass, probe byte-equal 3/3 including `env -i` (`F39C2Rerun`); S117/S118 re-opened live 2/2, quotes 2/2
  (`F39ReopenRows`); V7 controls 25/25 red (`F39MapControl`); no-harm on the round-37/38 C1 instruments ok (`F39NoHarmC1`);
  no removed line in any lane-authored doc (`F39CritNoHarmDiff`); errata append-only and green, the round-35-entry claim
  reproduced (`F39RevErrata`).
- Battery39: all four modules reviewed honest by non-author seats (`F39RevBatP1/P3/P7/D5`); fixture-level mutants caught 12/12
  (`F39MutBattery`). Limits: extra near-variant mutants 5 killed / 6 survived, each with a witness (`F39XMut`: e.g. P1 checks
  only the first two pins) — round-40 candidates; the post-hoc audit catches the wave-1 attacks 4/4 with no false red
  (`F39CritAudit`) but a phase-aware daemon defeats it (`F39SentinelAudit`, `AUDIT C1 clean` with dishonest fixtures), so C1
  admission rests on the frozen predicate plus the code review, not on the audit.
- Calibration count corrected: advertised mutants 5 of 7 (C 2, K 3, N 2), not 4; before 2 → after 0 unchanged
  (`F39CritC1Count`; lesson `## Errata (round 39, wave 2)`).
- Wording defects found and corrected by appended errata in the entry (`## Errata (round 39, wave 2)`): 5 unsupported
  sentences and 2 claim cells (`F39EntryQuotes`), 6 overclaims (`F39CritOverclaim`; the README's "recover … enforced" and the
  SKILL row "only a dangling blob or commit is caught" are corrected there, not rewritten in place).
- Tools: `order_check.py` catches 2 of 6 mutants (`F39OrderGateMut`; the fail-open mid-scan git error is unsensed) and Q30's
  title says "closed by a gate" while nothing invokes it (`F39CritQ30`); anchor check 2 low defects in the new leg, no lost
  round-38 behaviour and no false red (`F39AnchorFix`); ledger-tip 2 defects (`F39LedgerTip` D1: two live rows cannot fail in
  clone mode); direction check 5/6 mutants caught and it cannot load the round-39 list (`F39MutDirection`); `tip_receipts.py`
  skips the new receipt (no committed re-run command it recognises, `F39TipReceipts`); SKILL rows 12/15 verified
  (`F39CritSkill`); separability partly (`F39CritSeparability`, as the lesson's Mistakes row 5 says); round-38 dispositions
  16 of 79 verifiable at the tip (`F39CritR38Dispositions`: the map records decisions, most fixes are round-40 work). All
  routed to round 40; no frozen predicate is affected.
- Misroot 0, scratch leftovers 2 seat dirs, no leftover process (`F39ScoutMisroot`); cross-document drift 1 (the wave-2
  context's tip hash vs the measured tip, `F39ConnClaims`).

## Round 40 (hyaku run 9, 2026-10-26): the three tripwire tools mutation-tested (21/21 attributed); a sixth TB2 grader executed

Baseline as read `d3a6277f188434458e1d2ce04aff59392c6f0dc6`; freeze `bbb109505670192035ef63d7c8b37733e99fa1a3`; first
recorded probe run `055748f78a3335434f2a4070bb3fb1cf8d0eba1f`; landing `ec17216844585d0fecde9f1d4c4be0b78a3bf76f`. Frozen
prereg `plans/round-40-claims.md`. Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen (frozen
tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No stagnation waiver. Landing measurement
`.ufo/waves/round-40/integrate/measure-final.txt` (clean `--no-local` clone of the landing tip).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 what `plans/anchor_digest_check.py`, `plans/ledger_tip.py` and `plans/order_check.py` advertise in their docstrings and no fixture the lane's standing counter runs demonstrates — 21 frozen mutants (anchor 11, ledger 7, order 3), every direction witnessed before freeze, counter carrying the round-39 R4 soundness repairs | **calibration** — advertised-vs-demonstrated mismatch count for the lane's own tripwires | `python3 plans/round40_c1_verify.py --lane .` on a clean clone: before `BATTERY fixtures=0`, `MUTANTS total=21 killed=0 survived=21`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-40/claims/control-c1-nothing.txt`) → after `PINS total=3 mismatched=0`, `BATTERY fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21 survived=0 invalid=0 null_detected=0`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (`measure-final.txt`). Advertised count (wave-1 `R40CritClaims` §1): 13 direct + 4 indirect = 17 advertised of 21; 17 → 0 undemonstrated by the standing counter | frozen predicate met; **8 → 8 held** (the counter is gameable by a dishonest battery — wave-1 `R40CritC1Counter` A1/A2 — so admission also rests on the non-author battery review of wave 2) |
| C2 pinned TB2 `db-wal-recovery` grader admitted with an executed 28-case sandbox probe (S119 `tests/test_outputs.py`, S120 `instruction.md`; S121 TB2.1 PR #3 tier B for prior art) | **coverage** (lowest, tied) — `coverage/surfaces`: one §Frontier TB2 sub-bullet narrowed by one task (6 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 46→47, SOURCES 111→114; one edge class new to the executed sample (graded artefact = a JSON export whose source of truth is a SQLite main database plus an XOR-encrypted WAL; the repair step is never read) | `python3 plans/round40_c2_verify.py --lane .`: before `checks=7 defects=4` (V2, V3, V4, V7), exit 1 (`claims/control-c2-nothing.txt`) → after `checks=7 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=28 observed_pass=8 observed_fail=20 mismatches=0`, byte-equal re-run | frozen predicate met; **7 → 7 held** (L0 cap) |

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. No-harm at the landing tip (`measure-final.txt`):
round-39 C1 `killed=7` pass and C2 pass, round-38 C1 `killed=21 survived=1` as landed, round-38 C2 pass, round-37 C1
`killed=55` pass, round-37 C2 pass, round-36 C2 pass, anchor check `defects=0`, ledger-tip `mismatches=0`, census exit 0,
frozen digests (rounds 39, 40) OK; `order_check` round 38 exit 1, rounds 39 and 40 exit 0.

### Round-40 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `tripwire-mutation-counter` | Mutation-test the lane's own tripwire tools with attributed, direction-declared kills; battery modules built in a dying pid namespace, tool variants run sandboxed at one fixed path, fixture trees fingerprinted, pins re-hashed after the run | `python3 plans/round40_c1_verify.py --lane .` → `MUTANTS total=21 killed=21 …`, `PREDICATE C1 pass`; hostile-daemon control `tampered=0` with a counterfactual showing the daemon writes without the namespace (`claims/control-c1-hostile-daemon.txt`) | 40 |
| `binary-db-grader-probe` | Execute a pinned TB2 grader whose graded artefact is an export of a binary database pair, per case in bubblewrap with the task's seeds, frozen predictions and `violates=` tags | `python3 plans/db_wal_probe.py --lane .` → `cases=28 observed_pass=8 observed_fail=20 mismatches=0` (`measure-final.txt`) | 40 |
| `round-close-check` | One command that runs the order gate for every receipt a round's claims name plus the sources census, exit 0 only when all pass | `python3 plans/round_close.py --lane . --round 38` → exit 1; `--round 40` → exit 0 (wave-1 `R40CloseCheck`) | 40 |

Frontier and routed work (not claims): round-39 closure R1 (registry rows for `order_check.py`, `round39_c1_audit.py`
and the five round-40 instruments), R2 declared (the probe is pinned by the round-39 counter; registry addendum), R3 blocked
(the ledger tool is pinned by this C1 and evaluates two fixed ledgers), R4 (this C1; `plans/round_close.py` wires Q30's gate;
`plans/tip_receipts.py` derives a receipt's probe from its stem, so the round-39/40 receipts compare `equal` instead of
`skip`), R5 (round-39 scratch absent). `considerthese/2026-10-26.md` proposal 3 → the probe's `regrade=` column (a same-process
second call, not re-run stability) and the stability sweep `R40RegradeSweep` (5 graders, 15 states, 0 verdict flips, 2 graders
mutate the graded state). Registry 111 → 114 (tier A +2, tier B +1), knowledge 46 → 47; S046/S052 anchor notes.

### Planned (round 41)

- **Calibration (8):** mutation-test the next undemonstrated tripwire surface — the landed `plans/tip_receipts.py` (its
  round-40 derived-mapping clause included; `R40PlanNext` §2 priced the pre-fix bytes at 51 killed / 53 survived of 104 under
  its standing detector) and the CLI half of `plans/sources_adopt.py` (`main()` killed 2 of 32) — with the round-40 counter's
  limits repaired inside the re-frozen rule (clean PATH for tool runs, read-only host fs with only the fixture root
  writable, content fingerprints, per-module isolation, a type check on `build()`'s return: wave-1 `R40CritC1Counter`,
  `R40SentinelCounter`, `R40RevCounters`). Witnesses re-derived on the landed bytes before freeze (Q29, Q30).
- **Coverage (7, capped):** TB2 `constraints-scheduling` @ `2fd12b88` (grader embeds its own constraint model over
  sha256-pinned inputs; `R40PlanNext` pilot `cases=16 … mismatches=2`, oracle 3/3, nop 0/3; first-`DTSTART` defect published
  as TB2.1 PR #245 — no novelty claimed); rows S122/S123, ids re-derived at freeze. Fallbacks `circuit-fibsqrt`,
  `schemelike-metacircular-eval`.
- **Carried:** the order class into a separately frozen ledger once battery40's ledger declarations can move (R3);
  `considerthese/2026-10-26.md` proposal 1 (routed-findings burn-down) priced as a rider (`R40PlanNext` §4: 71 routed items
  vs 5 ledger rows).

### Wave 2 outcome (appended after the falsify wave; 35 seats, 35 reports, `.ufo/waves/round-40/falsify/`)

- Re-measures agree: C1 re-run `killed=21` pass, byte-equal across two hash seeds and job counts, every module load-bearing
  (7/7 removals flip their mutants, `F40C1Rerun`); C2 re-run pass, probe byte-equal 3/3 including `env -i` (`F40C2Rerun`);
  S119/S120/S121 and the S046/S052 notes re-opened 5/5 (`F40ReopenRows`); map red controls 10/10 (`F40MapControl`);
  independent re-run of the four non-frozen cases the entry cites 4/4 (`F40IndepProbe`); C1 and C2 separable both ways
  (`F40CritSeparability`); no harm on the round-37/38/39 instruments (`F40NoHarmC1`, byte-identical receipts); 2 rewritten
  lines in lane docs, both the S046/S052 anchor notes, no harm (`F40CritNoHarmDiff`); misroot 0, host writes 0
  (`F40ScoutMisroot`).
- Battery40: all seven modules reviewed honest by non-author seats (21/21 fixtures, `F40RevBat*`); fixture-level mutants
  caught 21/21 (`F40MutBattery`); no landed module uses a wave-1 counterexample vector (`F40CritCounterLimits`: 0 of 9; 9
  counter repairs drafted for round 41); security scan of the landed modules clean, four counter-level findings
  (`F40SentinelBattery`). Near-variant tool mutants outside the frozen list: anchor 7/16 killed, ledger/order 3/14 killed —
  round-41 candidates (`F40XMutAnchor`, `F40XMutLedgerOrder`).
- Calibration count confirmed by recount: 13 direct, 4 indirect, 4 not advertised (`F40CritC1Count`). Corrections to the
  row above (`F40CritScorecard` M1/M2): the C1 *before* cell is the empty-battery control of the frozen counter; the
  committed pre-freeze witness battery kills 7 of 21 (`witness-run.txt`) — the claim's count is over the standing counter;
  and "registry rows for … the five round-40 instruments" overstates: five rows landed in total (`order-check`,
  `round39-c1-audit`, `round40-c1-mutants`, `round40-c2`, `db-wal-probe`); `round_close.py` and the tip-receipts change are
  recorded in the round-40 registry addendum, not as rows.
- Wording defects in the C2 package found and corrected by appended errata (`## Errata (round 40, wave 2)` in the entry):
  14 overclaims (`F40CritOverclaim`; one wrong numeral — `plain-read-then-solve` scores 5 of 7, not 4), 6 unsupported
  sentences (`F40EntryQuotes`), prior art widened to a second audit and an in-the-wild report (`F40CritPriorArt`); SKILL rows
  18/19 verified (`F40CritSkill`); registry commands 7/7 match (`F40RegistryRows`).
- Tools: `round_close.py` 6/14 single-line mutants caught (rule (a) and the no-claims guard survive, `F40RoundClose`);
  `tip_receipts.py` 6 defects (two false-red shapes, a green run with no tamper control possible; `F40TipReceipts`); the
  round-41 plan carries 10 defects (`F40CritPlanNext`: its predicate is reachable with zero round-41 work as written; the
  isolation repair as worded reds the landed battery). All routed to round 41; no frozen predicate is affected.

## Round 41 (hyaku run 9, 2026-10-26): two tools' advertised behaviours demonstrated (23/23 attributed); a seventh TB2 grader executed

Baseline as read `e50c134556b4ba48e29dc7ff364e90d6ef07a3f3`; freeze `8ef8b4fc7c6302c527db90244d69aa18f53e83bf`; first
recorded probe run `f774a87ad071122acd39ba02a9901b5b56d9910a`; landing `74513c0625df7886357b866074104a0cf4bf9cc1`. Frozen
prereg `plans/round-41-claims.md`. Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen (frozen
tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No stagnation waiver. Landing measurement
`.ufo/waves/round-41/integrate/measure-final.txt` (clean `--no-local` clone of the landing tip).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 what `plans/tip_receipts.py` and the `plans/sources_adopt.py` CLI advertise and no `plans/battery41` fixture demonstrates — 23 frozen mutants (receipts 13, sources 10; 21 `direct`, 2 `indirect` advertised), every direction witnessed before freeze, predicate binding `TOTAL`/`FLOORS`, builds and tool runs in read-only host sandboxes | **calibration** — advertised-vs-demonstrated mismatch count for two lane tools | `python3 plans/round41_c1_verify.py --lane .` on a clean clone: before `BATTERY fixtures=0`, `MUTANTS total=23 killed=0 survived=23`, `MUTANTS-BY-TOOL receipts=0/13 sources=0/10`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-41/claims/control-c1-nothing.txt`) → after `PINS total=2 mismatched=0`, `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0`, `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (`integrate/measure-final.txt`, TIP `74513c06`) | frozen predicate met; **8 → 8 held** (wave 1 showed the counter forgeable by a hostile stub — `R41CritC1Counter` A1′, `R41SentinelCounter` F1 — so admission also rests on the wave-2 battery review) |
| C2 pinned TB2 `constraints-scheduling` grader admitted with an executed 25-case sandbox probe (S122 `tests/test_outputs.py`, S123 `instruction.md`; S124 TB2.1 PR #245 tier B, closed unmerged) | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (7 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 47→48, SOURCES 114→117; one edge class new to the executed sample (the verdict is computed by a scheduling model embedded in the grader over sha256-pinned input calendars; the graded ICS is read with regexes) | `python3 plans/round41_c2_verify.py --lane .`: before `checks=8 defects=5` (V2, V3, V4, V7, V8), exit 1 (`claims/control-c2-nothing.txt`) → after `checks=8 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (the two pilot mispredictions carried verbatim), `regrade cases=25 differ=0` | frozen predicate met; **7 → 7 held** (L0 cap) |

Erratum to the frozen claims text (not a predicate change; `R41CritClaims` D1/D3): the C1 count is over the standing
battery `plans/battery41` (the counter's `BATTERY_REL`), not "no committed fixture" — the freeze commit's own witness
modules kill 23/23 (`claims/control-c1-witness-as-battery.txt`); and "Novelty 7 has no candidate" overstates — the
receipt's `input-crlf-rewrite` (the input-integrity check compares decoded text, so a newline rewrite of all three
inputs passes 3/3) has no publication found (`R41ScoutPriorArt` row 3), so it is a novelty candidate for a later round
with its own prior-art check; nothing is claimed for it here. C2's frozen V1–V8 do not read the PROVINCE paragraph, the
§Frontier narrowing or S124 (`R41CritClaims` D2: a filler package passes 8/8); the L1 checked those three surfaces by
hand at landing (`PROVINCE.md` §Round41 partial frontier admission, `corpus/README.md` §Frontier "7 of 89 read",
`corpus/SOURCES.md` S124) and wave 2 re-checks them.

Other axes held: novelty 7, depth 9, operability 8, freshness 8, adjacency 8. No-harm at the landing tip
(`measure-final.txt`, against the baseline `integrate/measure-baseline.txt` at `fc79f2a4`): round-40 C1 `killed=21` pass
and C2 pass, round-39 C1 `killed=7` pass and C2 pass, round-38 C1 `killed=21 survived=1` as landed, round-38 C2 pass,
round-37 C1 `killed=55` pass and C2 pass, round-36 C2 pass, anchor check `rows=117 tokens=24 defects=0`, ledger-tip
`mismatches=0`, tip receipts `byte_equal=7 differ=0`, census exit 0 (15 `W04`, unchanged), frozen digests (rounds 39,
40, 41) OK, `order_check` round 38 exit 1 (as before), rounds 39/40/41 exit 0, `round_close.py --round 41` exit 0.

### Round-41 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `cli-exit-pair-mutants` | Mutation-test a CLI tool's advertised exit-code map with exact reference→mutant exit pairs (`2>0`, `3>0`, `5>0`, `2>9`) as declared directions, under a predicate that binds the mutant total and a per-tool floor | `python3 plans/round41_c1_verify.py --lane .` → `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PREDICATE C1 pass`; emptied-list control `claims/control-c1-no-mutants.txt` → `PREDICATE C1 fail` | 41 |
| `embedded-model-grader-probe` | Execute a pinned TB2 grader that computes its verdict with an embedded scheduling model over pinned inputs, per case in bubblewrap with frozen predictions, `violates=` tags and a same-state regrade | `python3 plans/constraints_probe.py --lane .` → `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, byte-equal re-run (`measure-final.txt` `constraints_probe exit=0 byte_equal=yes`); real pytest parity 25/25 (`R41CritPytest`) | 41 |
| `routed-findings-burndown` | Track every routed spot-check finding as one append-only row with status, evidence or blocker and an optional check command; print `routed_open=<n> oldest_round=<r>` and refuse a malformed file | `python3 plans/routed_open.py --lane .` → `ROWS total=10 open=4 blocked=1 closed=5 refused=0`, `routed_open=5 oldest_round=39`; `--selftest` → `SELFTEST 12/12` | 41 |

Frontier and routed work (not claims): round-40 closure R1 partly (the counter repairs above; F1–F4 still open), R2
(host-safety envelope in every wave context; Q32), R3 (registry rows `round41-c1-mutants`, `round41-c2`,
`constraints-probe`, `round-close-check` and the derived-mapping addendum landed; the 14 residuals re-measured and
routed, `R41RoundCloseMut`), R4 (`adv_kind` and the `ADVERTISED` line), R5 (round-40 C2 `--work` traceback fixed in the
round-41 counter; order class still blocked). `considerthese/2026-10-26.md` proposal 1 → `plans/routed_open.py` and
`corpus/routed-findings.jsonl` (10 rows: round-39 and round-40 §5). QUALITY Q31 (non-vacuous mutant predicates) and Q32
(attack seats' sandbox is evidence). Registry 114 → 117 (tier A +2, tier B +1), knowledge 47 → 48.

### Planned (round 42)` data walk (kengaku r41, wave 1, scout)

Seat: R41PlanNext (scout, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; measured on a `--shared` clone of HEAD
`fc79f2a49be0221e138b3885fa0d83bc43b31a42` (`git -C $S/lane rev-parse --show-toplevel` = `$S/lane`, `S=/fast/scratch/hyaku/kengaku-r41/R41PlanNext`).
Nothing in the lane was edited, staged or committed; no frozen file was touched. Every mutant/counter/sandbox run went through
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`
(TB2 graders and the CRLF probe additionally in a `--unshare-net` sandbox with `/usr` read-only). Receipts and the harness are in
`.ufo/waves/round-41/build/R41PlanNext/` (listed in §9). The L1 holds the planner seat; this is data plus a draft (§6).

Axes named first (Godspeed): **A1** advertised-vs-demonstrated gap per surface (kill rate under the committed standing detector);
**A2** witnessability (a cheap command shows the mutant changes behaviour in a declared direction); **A3** counter cost (does the
round-41 counter machinery carry the surface); **A4** TB2 class distance from the seven graders read; **A5** offline executability
(nop/oracle run now); **A6** quote supply; **A7** prior-art clearance; **A8** do-nothing control red now. A1/A2/A5/A8 were executed;
A7 last.

## 0. Headline

1. **Calibration — price: 31 witnessed mutants over four tripwire tools, no tool edit, round-41 machinery reusable.** At tip, the 20
   round-40 wave-2 near-variants that survived battery40 still survive through the unedited round-40 counter
   (`MUTANTS total=20 killed=0 survived=20`, 21 fixtures, `exhibits=none` ×20; 14 of the 20 have a round-40 witness in a declared rc/class
   direction, 6 are text-only). Three further surfaces measured now: `state_check.py main()` (27 mutants, standing detector kills 9, **8 of
   the 18 survivors witnessed** by two fixture shapes, 4 unwitnessed), `round_close.py` (70 mutants, `--selftest` kills 40, **9 of the 30
   survivors rc-witnessed** by a 9-command set), `sources_adopt.py` library functions (109 mutants: selftest kills 74, a 46-command CLI set
   kills 21 more, 12 survive, 2 invalid). `mutant_direction_check.py` is **not recommended** (§2.5). Do-nothing control executed: red (§4).
2. **Coverage/novelty — pick `circuit-fibsqrt` (new class: agent-authored data artefact run by a grader-owned simulator, verdict from a
   28-row table) with a finding measured now**: a 1195-line lookup circuit for the grader's 28 inputs passes **3/3** while the instruction's own
   examples print `0` (`208:0 20000:0`); nop passes 2 of 3 (the shipped example `gates.txt` satisfies the existence and size tests); oracle 3/3 in
   27.8 s offline. No tracker item, no published instance (the only public statement I found says the opposite: an LLM audit, tier C, "hardcoding
   impractical"). Fallback with an existing 26-case pilot: `openssl-selfsigned-cert` (nop 0/6, oracle 5/6 on host OpenSSL 3.6.5). Refused:
   `schemelike-metacircular-eval` (gaming surface already published, #135/#235).
3. **Is any round-41 C2 finding unpublished? Yes, one: `input-crlf-rewrite`** — rewriting the three input calendars with CRLF (or bare CR, or
   one line only) passes the grader's integrity check although `instruction.md:17-18` says any modification fails; mechanism `read_text()`
   universal newlines at `test_outputs.py:90,93`. Not in PR #245 (it changes only the output reader `_r`, and its spec says "Do not change input
   integrity"), the grader blob on TB2.1 `main` is byte-identical to the pin, 0 tracker hits for CRLF/newline/integrity. Novelty candidate with
   limits (§3.4). The decoy finding is published (S124); the RFC-forms rejections are only adjacent to #245 (its fixtures expect them accepted).

## 1. Method and what was run

| piece | what | where |
|---|---|---|
| mutant harness | R40PlanNext's AST harness (`cmp`, `and/or`, `not`, `return n`, `SystemExit(n)`, `if→False`, int +1; result-difference kill; identity copy and baseline-stability checked) wrapped per surface by `run42.py` (detector sets, region limits) | `harness/` |
| kill = | `(rc, normalised stdout+stderr)` of ANY detector differs from the unmodified tool's (not an attributed kill; the counters are stricter) | |
| standing detector | what the lane commits: `--selftest` (+ `--summary` for state_check) | |
| witness detector | extra commands/fixtures a battery module could build; indices recorded per mutant in `res_*.json` `info` | |
| near-variants | `ctr/plan42_driver.py` = the **unedited** round-40 counter (sha `4d47800e…`, equal to the lane's) with `MUTANTS` swapped to the 30 wave-2 rows (`xmut_table.py` + `xmut_driver.py` from `F40XMutAnchor/`, `F40XMutLedgerOrder/`) | |

Tool pins at this tip equal the round-40 counter's: `sha256sum plans/anchor_digest_check.py plans/ledger_tip.py plans/order_check.py` →
`11bb2cad…`, `853bcb2a…`, `948d5e1d…`; `git log -3 -- <those>` stops at round-39 commits, i.e. unchanged since.

Scratch note: the whole `/fast/scratch/hyaku/kengaku-r41/` tree (every seat's dir) was removed once around 15:42 by something outside this seat; I re-cloned
and re-ran everything below it. All receipts were copied to the report dir immediately.

## 2. Candidate A — calibration

### 2.1 Surface table (all at `fc79f2a`; commands in §8)

| surface | mutants | standing detector kills | + witness-detector kills | survive | witnessed survivors | unwitnessed / limit |
|---|---|---|---|---|---|---|
| anchor+ledger+order near-variants (30, round-40 wave 2) through the frozen r40 counter | 30 | 10 (battery40) | – | **20** | 14 (X1 X3 X6 X7 X9 X12 X13 X14 X15 XO1 XO3 XO5 XO6 XO7; round-40 reports `wit/`, `wit-*.diff`) | 6 text-only (XL1–XL6: summary counters, `kind=`, REF AUDIT/BIND labels; counter `classes()` reads none of them) |
| `state_check.py main()` (L4649–4706) | 27 | 9 (`--selftest`, `--summary`) | 6 (6 error-path commands) | **12** | **8** (§2.3) | 4: L4694 `return 2` (check_all raises), L4701 ×2, L4703 (empty population) |
| `round_close.py` (whole file) | 70 | 40 (`--selftest`) | 10 (9 commands) | **20** | **9** rc-witnessed (§2.4) + 2 message-only (L164, L181: rc 2→2) | 9: L121 ×2, L144 `and→or`, L148, L179, L199, L200, L209, L291 |
| `sources_adopt.py` library fns (L1–609, `main`/selftest excluded) | 109 (2 of them invalid) | 74 (`--selftest`) | 21 (46 CLI commands) | **12** | not witnessed (guards: L87 ×2, L118, L120, L153, L156, L216, L222, L365, L430, L519, L542) | 2 invalid mutants (`not x→x` breaks the parenthesis) |
| `mutant_direction_check.py` | 28 of 70 (sample) | 19 | – | 9 | – | §2.5 |

Not re-measured: `tip_receipts.py` and the CLI half of `sources_adopt.py` (this round's C1 — wave-1 batteries are in flight; the clone has no
`plans/battery41`). The 12 sources-library survivors and the 21 CLI-only kills are for the planner to re-derive after battery41 lands (Q30): some of
the 21 may already be killed by battery41's fixtures.

### 2.2 The near-variant control, executed now
- **Counter repairs carried into the round-42 C1 counter (L1, from wave 1):** the round-41 counter's variant is readable from
  inside a tool run and two kills (T03, T04) can be credited on a dead site under a hostile stub (`R41CritC1Counter` A1′ §3,
  `R41SentinelCounter` F1); AF_UNIX sockets and SysV IPC are not isolated (F2, F3); relative argv tokens escape `d` (F4, A3);
  the fingerprint reads files whole (F6). The round-42 counter binds the variant by content (`--ro-bind-data`) or hides
  `root/variants`/`root/slots`, adds `--unshare-ipc` and `--tmpfs /run`, resolves relative tokens, and adds an attribution
  leg (the mutated line must execute on the killing fixture); each repair frozen with its own red control
  (`corpus/routed-findings.jsonl` R40-R1).
- **Hygiene (L1):** wave contexts require a seat to check its `rm -rf` target is its own `$S` (wave 1: a seat deleted the
  round root, `corpus/lessons/round-41.md` §Mistakes); unguarded until a round shows that check able to fail.

Source: `.ufo/waves/round-41/build/R41PlanNext.md` §6 (data walk at `fc79f2a4`), plus the two L1 bullets above.

### Wave 2 outcome (appended after the falsify wave; 34 seats, 34 reports, `.ufo/waves/round-41/falsify/`)

- Re-measures agree: C1 re-run byte-equal across two hash seeds and job counts, every module load-bearing 7/7
  (`F41C1Rerun`); C2 re-run pass, probe byte-equal 3/3 including `env -i` (`F41C2Rerun`); no-harm verdicts 25/25 equal
  (`F41NoHarm`); 0 removed lines outside wave dirs since `e50c1345` before the wave-2 errata (`F41CritNoHarmDiff`);
  separable both ways (`F41CritSeparability`); misroot 0, host writes 0 (`F41ScoutMisroot`).
- C1 admission evidence beyond the frozen predicate: every killing fixture executes its mutated line, 23/23
  (`F41C1Attribution`) — the wave-1 dead-site vector (T03/T04) is not used by the landed battery; the landed battery passes
  `MUTANTS total=23 killed=23` under a hardened counter copy (variant hidden, `--unshare-ipc`, `--tmpfs /run`, relative
  `path_ok`, streaming fingerprint), each repair shown biting 5/5 (`F41C1Hardened`); non-author review of all seven
  modules: 47 of 48 fixtures honest, 1 incidental (`s_usage-03-single-digit-month-duplicate-request`; S03 is also killed
  by an honest fixture), 0 dishonest (`F41RevBat*`); fixture mutants 43/48 caught, the 5 survivors are redundant fixtures
  whose mutants another fixture still kills (`F41MutBattery`); battery security findings 3 (host name service reachable,
  SysV IPC shared, `--work` check) — counter-level, routed (`F41SentinelBattery`).
- Calibration denominator (`F41CritC1Count`): `ADVERTISED direct=21 indirect=2 none=0` holds as a count of mutants; the
  two tools advertise 58 behaviour rows, the 23 mutants price 24 of them, 34 carry no mutant. The C1 claim's count is
  over its frozen list, so the 34 are the next calibration denominator, not a miss of this claim. Near-variant mutants
  outside the list: battery41 kills 6/20 of `tip_receipts.py`'s and 9/20 of the `sources_adopt.py` CLI's
  (`F41XMutReceipts`, `F41XMutSources`).
- C2: S122/S123 hold, S124's anchor named the wrong PR-body section (corrected, old→new in the lesson); the entry carries
  9 wrong and 3 unsupported sentences (`F41EntryQuotes`) and the C2 prose 8 overclaims (`F41CritOverclaim`), corrected by
  appended errata (entry `## Errata (round 41, wave 2)`, PROVINCE wave-2 correction); none reverses a finding. V7/V4 red
  controls 6/7; the survivor is S124's anchor digest, which no C2 check reads (`F41MapControl` M7). Independent re-run of
  the five non-frozen end states the entry cites 5/5 (`F41IndepProbe`); both unpublished observations stay unpublished
  after a wider search (`F41CritPriorArt`). SKILL rows 11/11 and registry commands 4/4 verified (`F41CritSkill`).
- Corrections to the round-41 rows above (`F41CritScorecard` D1/D3, N1): "Registry 114 → 117" is the SOURCES registry; the
  SKILL tool registry went 31 → 35 rows (+4); the exit-pair list is six pairs (`2>0`, `2>1`, `2>5`, `2>9`, `3>0`,
  `5>0`), not four; tip receipts are `byte_equal=7 differ=0 skipped=20` (7 of 27 compared). QUALITY Q31/Q32 errata
  appended (`F41RevQuality`); the rider's 10 rows are honest at the tip (`F41RevRider`).
- **L1 paste error:** the `### Planned (round 42)` block above (it begins with the line "`### Planned (round 42)` data walk
  (kengaku r41, wave 1, scout)") is the data walk's §0–§2.2, pasted from the report's title line instead of its §6 block;
  `F41CritPlanNext` D1–D10 measured that paste. It is superseded by the corrected plan below and is not deleted.

### Planned (round 42) — corrected (supersedes the block above; `F41CritPlanNext` D1–D10 applied)

Axis state carried: calibration 8, coverage 7 (capped by the open L0 question `kengaku | round-33`), novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. A coverage claim is
score-dead (+0) under the cap; the round's lowest-axis claim may sit on novelty only with a new construct and a dated
prior-art receipt. Source: `.ufo/waves/round-41/build/R41PlanNext.md` §0–§9 (controls in §4; receipts
`R41PlanNext/near-variants-r40-counter.txt`, `near40_survivors_only.txt`), `.ufo/waves/round-41/falsify/F41CritPlanNext.md`.

- **Calibration (8):** a re-frozen counter `plans/round42_c1_verify.py` = the round-41 counter plus the five repairs
  `F41C1Hardened` showed biting (variant hidden from tool runs, `--unshare-ipc`, `--tmpfs /run` and host socket paths
  unbound — `R41SentinelCounter` F2, relative-token `path_ok`, streaming fingerprint) and an attribution leg (the mutated
  line executes on the killing fixture, `F41C1Attribution`'s method), each repair frozen with its own red control. Mutant
  list: the near-variants battery40/battery41 leave alive — anchor X1 X3 X6 X7 X9 X12 X13 X14 X15, order XO1 XO3 XO5 XO6
  XO7 (round-40 witnesses `F40XMutAnchor`, `F40XMutLedgerOrder`; re-measured through the unsandboxed round-40 counter at
  `fc79f2a4`: `total=30 killed=10 survived=20`, `PREDICATE C1 fail`), the witnessed `state_check.py` `main()` exit-2
  survivors and `round_close.py` rc survivors (`R41PlanNext` §2; these witnesses are the seat's command sets, re-derived on
  landed bytes before freeze, Q29/Q30), or the 34 unpriced advertised rows of `tip_receipts.py`/`sources_adopt.py`
  (`F41CritC1Count` §2). Predicate: `MUTANTS total=<N> killed=<N> survived=0 invalid=0 null_detected=0`, per-tool
  `MUTANTS-BY-TOOL` floors bound to literals (Q31), `PREDICATE C1 pass`, exit 0. Controls that must be red at freeze: no
  `plans/battery42` → `killed=0 survived=<N>`; the emptied-list copy → `PREDICATE C1 fail`; the five hostile modules
  (`F41C1Hardened`) → red under the new counter.
- **Coverage (7, capped) — `circuit-fibsqrt` @ `2fd12b88`:** a data artefact run by a grader-owned simulator and scored on
  a fixed 28-row table (rows S125–S127, ids re-derived at freeze). Counter `plans/round42_c2_verify.py` = round-41's V1–V8
  re-pointed (spec, gate, probe, dry table, captures pinned; V8 order gate), dry table frozen before the first recorded
  run; do-nothing control `checks=8 defects>=4`. Plan-time controls: oracle 3/3, nop 2/3 (the shipped example satisfies
  the existence and size tests), a lookup circuit for the 28 graded inputs passes 3/3 while the instruction's own
  examples print 0. Fallback `openssl-selfsigned-cert` admissible only with its failing oracle case declared and excluded
  by id (oracle 5/6 on host OpenSSL 3.6.5).
- **Novelty (7) — carried, not a claim as drafted:** `input-crlf-rewrite` is already measured and committed, so a claim on
  it alone is do-nothing-reachable (`F41CritPlanNext` D3). A novelty claim needs a new construct with its own red control,
  e.g. a cross-grader instrument over the seven admitted TB2 graders' input-integrity checks (decoded-text vs byte
  comparison), plus a dated prior-art receipt (`F41CritPriorArt`: 2/2 still unpublished).
- **Routed, owned (`corpus/routed-findings.jsonl`, `routed_open=5 oldest_round=39`):** R39-R2 (`git_leak_probe.py --work`
  absent dir) and R39-R4 (carried residual bundle) — operability fixes, L1; R39-R3 (order class into a ledger) — blocked
  while `plans/ledger_tip.py` is pinned; R40-R1 (counter soundness) — the calibration bullet above; R40-R5 (carried
  bundle) — L1, one item per round with a check command. Rows close only with evidence and a check.
- **Hygiene (L1):** a seat checks that its `rm -rf` target is its own `$S` before deleting (wave 1: a seat deleted the
  round root; the wave-2 context carried the guard sentence); unguarded until a round shows the check able to fail. L1
  counter runs carry the envelope line (Q32 forward leg, red on the L1's receipts this round).

## Round 42 (hyaku run 9, 2026-10-26): two gate tools' near-variants demonstrated with attributed kills (14/14); an eighth TB2 grader executed

Baseline as read `d69452cfa4ea8f95a43caf3727a7c797ba390b6c`; freeze `bc856d803576e182b6c3c12afc6b23f392071c25`; first
recorded probe run `523b27806be0df26d2235089d845265a29f8cedf`; wave-1 dispatch `fda71ae0`; landing
`ff14d76d32d662f7b7073a2acb049594cb740d84`. Frozen prereg `plans/round-42-claims.md`. Lowest non-retired axis: coverage 7,
tied with novelty 7; coverage chosen (frozen tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No
stagnation waiver. Landing measurement `.ufo/waves/round-42/integrate/measure-final.txt` (clean `--no-local` clone of the
landing tip, inside the Q32 envelope v2), baseline `integrate/measure-baseline.txt` at `fda71ae0`.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 what `plans/anchor_digest_check.py` and `plans/order_check.py` advertise and battery40 leaves undemonstrated — the 14 directional round-40 near-variants (anchor 9, order 5; 13 `direct`, 1 `indirect`), directions witnessed through the frozen counter (XO5/XO6 relabelled `rc-mirror`), kills counted only when attributed (traced re-run executes the replaced span) | **calibration** — advertised-vs-demonstrated mismatch count for two lane gate tools | `python3 plans/round42_c1_verify.py --lane .`: before `BATTERY fixtures=0`, `MUTANTS total=14 killed=0 survived=14`, `MUTANTS-BY-TOOL anchor=0/9 order=0/5`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-42/claims/control-c1-nothing.txt`; `integrate/measure-baseline.txt`) → after `PINS total=2 mismatched=0`, `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (`integrate/measure-final.txt`, measured at `ff14d76d`) | frozen predicate met; **8 → 8 held**; admission also rests on the wave-2 non-author battery review (the counter is forgeable: `R42CritC1Counter` reached the predicate with three substitute fixtures; `R42CritAttribution` finds the span check vacuous for 8/14) |
| C2 pinned TB2 `circuit-fibsqrt` grader admitted with an executed 16-case sandbox probe (S125 `tests/test_outputs.py`, S126 `instruction.md`, S127 `tests/sim.c`; S128 OpenAgents #9645 tier B prior art) | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (8 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 48→49, SOURCES 117→121; one edge class new to the executed sample (a data artefact executed by a simulator the grader compiles at grading time, scored on a fixed 28-row table) | `python3 plans/round42_c2_verify.py --lane .`: before `checks=9 defects=6` (V2 V3 V4 V7 V8 V9), exit 1 (`claims/control-c2-nothing.txt`; at `fda71ae0` `defects=5`, V8 ok once the receipt landed) → after `checks=9 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`, re-run byte-equal (`fibsqrt_probe exit=0 byte_equal=yes`); real pytest 8.4.1/py3.13 parity 16/16 (`R42CritPytest`) | frozen predicate met; **7 → 7 held** (L0 cap) |

Limits found in wave 1 (frozen counters not edited; routed to round 43): `R42SentinelCounter` V1 (HIGH) — a fixture's
`.git/config` with `log.showSignature` + `gpg.program` runs a program inside the order tool's run, so the frozen sentence
"these two tools run no fixture code" is false for `order_check.py` (no fabricated kill demonstrated; battery42 carries
no such key: `grep -i 'config\|gpg\|signature\|worktree' plans/battery42/*.py` → nothing); V2/V3 (builder copy readable,
the hidden lane is a writable tmpfs); `R42CritC1Counter` V1b (`core.worktree` redirects the order tool's root outside the
fixture). V9 is a consistency check, not a content check: an informed filler that copies the receipt into a case table
passes 7 of 9 (`R42CritClaims` §1). Two frozen `adv` cells are misquoted (`R42RevMutRows`: 12/14 verbatim).

Other axes held: novelty 7 (no claim; prior art searched — of six findings one published as worded, one adjacent, S128),
depth 9, operability 8 (riders: `plans/scratch_guard.py` selftest 36/36; `round_close.py --selftest` re-run fix, red→green
`integrate/r5-round-close-check.txt`), freshness 8, adjacency 8 (PROVINCE routing: digital-logic/C-simulator semantics
unowned). No-harm at the landing tip (`diff` of verdict lines, `measure-baseline.txt` vs `measure-final.txt`): only the
round-42 counters (red → green), the anchor check (`rows=117 tokens=24` → `rows=121 tokens=27`, `defects=0` both), the
routed rider (`routed_open=5` → `10`, six rows appended) and the registry/knowledge counts differ; rounds 36–41 counters,
ledger-tip, tip receipts (`receipts=28 byte_equal=8 differ=0` — the fibsqrt receipt now re-runs byte-equal by derived
mapping), constraints/db-wal probes byte-equal, census exit 0 (15 `W04`), frozen digests (rounds 39–42) OK, `order_check`
round 38 exit 1 (as before), rounds 39–42 exit 0, `round_close.py --round 41/42` exit 0. Envelope note: under the v1
envelope (home read-only) every C2-class counter went red on `uv`'s cache lock (`integrate/measure-baseline-v1.txt`); v2
overlays `~/.cache` from scratch.

### Round-42 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `attributed-mutant-kills` | Count a mutant as killed only when a traced re-run of the mutant on the killing fixture reproduces the result and executes a line of the replaced span; print `unattributed=<n>` otherwise | `python3 plans/round42_c1_verify.py --lane .` → `unattributed=0`, `PREDICATE C1 pass`; span-forced control `claims/control-c1-attribution.txt` → `killed=0 unattributed=14`, fail | 42 |
| `compiled-simulator-grader-probe` | Execute a pinned TB2 grader that compiles its own simulator at grading time and runs it over an agent-written data artefact, per case in bubblewrap with frozen predictions, `violates=` tags and a same-state regrade | `python3 plans/fibsqrt_probe.py --lane .` → `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, byte-equal re-run (`measure-final.txt`); pytest parity 16/16 (`R42CritPytest`) | 42 |
| `scratch-root-guard` | Refuse a scratch deletion outside the caller's own seat dir (root, sentinel, sibling seat, symlink or `..` escapes) and verify the round root's sentinel | `python3 plans/scratch_guard.py --selftest` → `SELFTEST ok=36/36`; `check /fast/scratch/hyaku/kengaku-r42` → `SENTINEL … round=42` | 42 |

Frontier and routed work (not claims): round-41 closure R1 (repairs a–e + attribution frozen; a–c reachable only through
git config — V1 above, routed), R2 (sentinel + `scratch_guard.py`; guard sentence in the wave context; misroot 0, host
writes 0, `R42ScoutMisroot`), R3 (V9 + `control-c2-filler.txt`; the tier-B live-state half not built, routed), R4 (no
SOURCES cell edited in place; new rows only), R5 (`round_close.py` re-run fix landed with a red/green check).
`considerthese/2026-10-26.md` proposal 2 (filler-control half) → V9. QUALITY Q33 (carried directions re-derived through
the frozen counter) and Q34 (SOURCES non-mutable cells corrected only by a superseding row). Registry 117 → 121 (tier A +3,
tier B +1), knowledge 48 → 49. Assimilation: none (`merge/kengaku/` unchanged since 2026-10-24, `R42MergeRescreen`).

### Planned (round 43)

Axis state carried: calibration 8, coverage 7 (capped by the open L0 question `kengaku | round-33`), novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. The L1 holds the planner
seat; the round-43 data-walk seat `R42PlanNext` ended without a report (its raw files `.ufo/waves/round-42/build/R42PlanNext/`
are data, unreviewed: `res_round_close.json` `population=70 killed=50 survived=20`, `feal/feal_run1.txt`).

- **Calibration (8):** re-freeze the C1 counter as `plans/round43_c1_verify.py` with the round-42 wave-1 remediations
  inside the frozen rule, each with its own red hostile control — pin `gpg.program`/`log.showSignature` (`R42SentinelCounter`
  V1), hide the builder copy from builds (V2), a read-only lane hide (V3), refuse a fixture repo whose toplevel or
  `core.worktree` leaves d (`R42CritC1Counter` V1b) — and a **site-value** attribution leg for mutants whose span runs on
  every invocation (`R42CritAttribution`: vacuous for 8/14; wave 2 `F42C1StrongAttrib` drafts it). Mutant list: the
  rc-witnessed `plans/round_close.py` survivors (`R41PlanNext` §2.4; 20 survivors of 70 re-measured at round 42) or the
  `u = 18` advertised anchor/order behaviours with no frozen mutant (`R42CritEquiv` §3), each direction re-derived through
  the frozen counter (Q33), predicate bound to literals (Q31). Controls red at freeze: no battery43; emptied list; the four
  hostile modules; span-forced and site-forced attribution copies.
- **Coverage (7, capped) — TB2 `feal-differential-cryptanalysis` @ `2fd12b88`** (data, `R42PlanNext/feal/feal_run1.txt`,
  unreviewed): nop fails (`ModuleNotFoundError: No module named 'attack'`), the oracle passes 5/5, and two constructed
  `attack.py` shapes that do not attack the cipher pass (`cheat-import-get_keys`, `cheat-clock-seed` 5/5) — a grader that
  imports agent code in-process, a class the eight admitted TB2 graders do not cover. Re-derive every control before freeze;
  prior art (`R42PlanNext/prior-art/gh_issue_counts.txt`: one TB2.1 hit for the task name) checked by a seat before any
  sentence says "unpublished". Fallback: `openssl-selfsigned-cert` (oracle 5/6 on host OpenSSL 3.6.5, declared).
- **Novelty (7) — carried, not a claim as drafted:** round-42 C2 findings not found in print (lookup construct, stdin/argv,
  last-32-lines, cwd compile, whitespace; `R42ScoutPriorArt`) are probed instances; a novelty claim needs a new construct
  with its own red control and a dated prior-art receipt.
- **Routed (`corpus/routed-findings.jsonl`, `routed_open=10 oldest_round=39`):** R3 tier-B live-state check (S124/S128
  state words) — owned, operability; the V9 informed-filler limit (`R42CritClaims`) — a V10-style content check needs a red
  control against an informed filler; `R42MutC1Counter` counter guards caught 7/22 by committed controls.

### Wave 2 outcome (appended after the falsify wave; 33 seats, 33 results, `.ufo/waves/round-42/falsify/`)

- C1 admission evidence (non-author): battery42 reviewed honest module by module — `a_route` 6/6, `a_class` 6/6, `a_row`
  6/6, `o_clause` 5/5, `o_scan` 6/6, substitutes 0 (`F42RevBat*`); site-value attribution for the 8 span-vacuous mutants 8/8
  (`F42C1StrongAttrib`); the landed battery passes 14/14 under a hardened counter copy whose four repairs (gpg pins, builder
  hidden, read-only lane hide, toplevel/worktree check) each bite (`F42C1Hardened` 4/4); re-run byte-equal across seeds and
  job counts, every module load-bearing 5/5 (`F42C1Rerun`); `F42GpgVector`: the gpg.program vector is real but cannot change
  a verdict in any of the 14 declared directions. Every fixture is individually redundant (each mutant has two killers,
  `F42MutBattery` 0/29 single-fixture flips); near-variants outside the list killed 15/25 (`F42XMutNear`, round-43 data).
- C2: re-run pass, probe byte-equal 3/3 incl. `env -i` (`F42C2Rerun`); quotes 24/24 verbatim, 4 entry sentences flagged
  (`F42EntryQuotes`); rows re-opened 4/4, no wrong cell (`F42ReopenRows`); cwd claim confirmed, 9/16 verdicts move off `/app`
  (`F42CritCwd`); compiler flags do not move the receipt (`F42CompilerSens`); separability holds (`F42CritSeparability`);
  V9 admits 2 of 4 attack shapes and its mutants are caught 7/16 (`F42CritV9`, `F42MutC2V9`) — V9 is a consistency check.
- No harm: 277/277 verdict lines equal (`F42NoHarm`); tip re-measure at `3e8a2e5e` verdict-equal (`integrate/measure-tip3.txt`).
- Routed to round 43 (not integrated this round; reports are the evidence): entry 4 sentences, C2 package 9 defects
  (`F42RevC2Package`), lesson 8 (`F42RevLesson`), Q33/Q34 6 (`F42RevQuality`), riders 5 (`F42RevRiders`), adv errata 2
  (`F42CritAdv`), SCORECARD 1 mismatch (`F42CritScorecard`), cross-doc drift 1 (`F42ConnClaims`), overclaim review 1 wrong
  (`F42CritOverclaim`), plan-43 defects 5 (`F42CritPlanNext`). `F42ConnFrontier` returned no verdict line.

### Round-42 corrections appended in round 43

- **S1 — the envelope note is one counter too wide (`:1760`, from `F42CritScorecard` M1).** "under the v1 envelope
  (home read-only) every C2-class counter went red on `uv`'s cache lock" — `integrate/measure-baseline-v1.txt` shows
  `PREDICATE C2 fail` six times (`:51,161,239,386,522,669`) and `PREDICATE C2 pass` once (`:679`), for round 36.
  Corrected: every C2-class counter that drives the gate's `uv` leg (`plans/pkg_gate.py:276` `["uv", "run",
  "--no-project", "--with", "biopython==1.85", "python3"]`, which is the `P10` line those six report as DEFECT) went
  red; `plans/round36_c2_verify.py`'s six checks (`W1`–`W6`, `:215-216`) drive no `uv`-backed tool and stayed green.
- **S2 — two frozen C1 `adv` cells carry wrong line pins (`F42CritAdv`).** X3 cites
  `plans/anchor_digest_check.py:57-58` for a sentence that sits at `:59-61`; X7 cites `:92-93` for one at `:91-92`; both
  are carried from `F40XMutAnchor.md` §5. Display-only (`label[:90]` is echoed and never parsed, so no admission claim
  moves); the erratum is `corpus/lessons/round-42.md` E7 and the cites are to be corrected when
  `plans/round42_c1_verify.py` is next editable.
- **S3 — where the wave-2 routed defects are carried.** The lesson, QUALITY and SCORECARD corrections above live in the
  documents themselves; the ledger/rider defects live in `corpus/routed-findings.jsonl` as `R42-R2.1`, `R42-R2.2` and
  `R42-R6`, with `R42-R4` closed and `R42-R2`'s stale check cleared (drafts:
  `.ufo/waves/round-43/build/R43R42Defects.md` §2 D–E).

## Round 43 (hyaku run 9, 2026-10-26): nine near-variants of two gate tools killed with value-attributed kills (9/9); a ninth TB2 grader executed (in-process module import)

Baseline as read `317148c4b918fb2645e46ec0225cac720a8a57e9`; freeze `02753f260805e2e45b05af22145da00f91671364`; first
recorded probe run `6b49694d2ff533135fc238a8400f3e0dc1c82026`; wave-1 dispatch `d33350fd`; landing
`77ea425ac217ebe2290490b2ebb3d0a60202ca9b`. Frozen prereg `plans/round-43-claims.md`. Lowest non-retired axis: coverage
7, tied with novelty 7; coverage chosen (frozen tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No
stagnation waiver. Landing measurement `.ufo/waves/round-43/integrate/measure-final.txt` (clean `--no-local` clone of the
landing tip, inside the round-43 envelope), baseline `integrate/measure-baseline.txt` at `d33350fd`.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the nine behaviours `plans/anchor_digest_check.py` and `plans/order_check.py` advertise that battery42 leaves undemonstrated (round-42 wave-2 near-variants NA1 NA5 NA7 NA18 NA20 NA21 NO5 NO7 NO22; 8 `direct`, 1 `indirect`), directions re-derived through the frozen counter, kills counted only when attributed by span AND by a differing site record | **calibration** — advertised-vs-demonstrated mismatch count for two lane gate tools | `python3 plans/round43_c1_verify.py --lane .`: before `BATTERY fixtures=0`, `MUTANTS total=9 killed=0 survived=9`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-43/claims/control-c1-nothing.txt`; `integrate/measure-baseline.txt`) → after `PINS total=2 mismatched=0`, `BATTERY fixtures=42 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=9 killed=9 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (`integrate/measure-final.txt` @ `77ea425a`) | frozen predicate met; **8 → 8 held** (the counter cannot see intent — the freeze module copied as battery passes; admission also rests on the wave-2 battery review) |
| C2 pinned TB2 `feal-differential-cryptanalysis` grader admitted with an executed 12-case sandbox probe (S129 `tests/test_outputs.py`, S130 `instruction.md`, S131 `tests/feal_module.c`, S132 `tests/feal.c`, S133 `tests/test.sh`, S134 `README.md`, tier A; S136 `environment/Dockerfile`, S137 `environment/feal.py`, tier B by executed flips) | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (9 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 49→50, SOURCES 121→130; one graded-state class new to the executed sample (an agent-authored Python module imported into the grader's own interpreter beside the reference module that holds the answer; verdict = pytest exit status) | `python3 plans/round43_c2_verify.py --lane .`: before `checks=10 defects=7` (V2 V3 V4 V7 V8 V9 V10), exit 1 (`claims/control-c2-nothing.txt`; at `d33350fd` `defects=6`, V8 ok once the receipt landed) → after `checks=10 defects=0`, `PREDICATE C2 pass`, exit 0 (`measure-final.txt`); probe `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`, re-run byte-equal (`feal_probe exit=0 byte_equal=yes`) | frozen predicate met; **7 → 7 held** (L0 cap) |

Limits found in wave 1 (frozen counters not edited; routed to round 44): V10's DECISIVE map is readable in the counter,
so a copycat filler passes V10 (`R43CritClaims` §1); R4 does not see a `.git` FILE pointing at an outside git dir nor
repos deeper than three levels, leg i is bypassed by an absolute or abbreviated argv (`R43SentinelCounter` F1–F3,
`R43CritC1Counter` V2′) — no battery43 fixture uses these shapes (grep over `plans/battery43/*.py`: nothing); counter
guards caught 8/15 by committed controls (`R43MutC1Counter`) and V9/V10 guards 6/13 (`R43MutC2Counter`); the envelope's
content digest misses a mode-only change and a rewrite of a mode-000 file (`R43ReviewEnvelope`, 3/4 kinds caught).
Independent checks that held: real pytest 8.4.1 under `uvx -p 3.13` 12/12 equal to the receipt (`R43PytestParity`);
re-derivation 12/12 + 3 own cases (`R43CritIndep`); no dishonest battery reached the C1 predicate (9 vectors,
`R43CritC1Counter`); value leg spurious 0, vacuous 0/9 (`R43CritValueLeg`); verdict stable over 18 runs
(`R43RevSiteStable`); mutant rows 9/9, 0 misquoted (`R43RevMutRows`).

Other axes held: novelty 7 (no claim; prior art priced — three findings published, three adjacent, none measured on
this grader before, `R43ScoutPriorArt`; no novelty asserted), depth 9, operability 8 (riders: `plans/gate_flip_check.py`
selftest 19/19; the generator route-mix asserts), freshness 8 (S129–S134 re-fetched cmp-identical, S135–S137 re-opened;
TB2.1 copy byte-identical), adjacency 8 (PROVINCE routing: cryptanalysis technique and Python import-system semantics
unowned, `R43ConnSibling`). No-harm at the landing tip (`diff` of verdict lines, `measure-baseline.txt` vs
`measure-final.txt`): only the round-43 counters (red → green), the package gate's P3/P6/P8 legs, `index_rows` /
`knowledge_files` 49 → 50 in older counters' P8, the anchor check (`rows=121 tokens=27` → `rows=130 tokens=36`,
`defects=0` both), `routed_open=10` → `52` (the wave-2 queue now durable), and registry/knowledge counts differ; rounds
36–42 counters, ledger-tip, tip receipts, constraints/db-wal/fibsqrt/feal probes byte-equal, census exit 0, frozen
digests r39–r43 OK, `order_check` round 38 exit 1 and round-38 C1 `survived=1` (both as before), `round_close.py --round
41/42/43` exit 0.

### Round-43 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `value-attributed-mutant-kills` | Count a mutant as killed only when the traced re-run executes the replaced span AND the frame's next event after that span (next line + locals digest, or return value) differs from the reference's, the reference traced twice and stable | `python3 plans/round43_c1_verify.py --lane .` → `value=differs` on 9/9, `PREDICATE C1 pass`; forced-equal control `claims/control-c1-value.txt` → `unattributed=9`, fail | 43 |
| `in-process-import-grader-probe` | Execute a pinned TB2 grader that imports the agent's Python module into its own interpreter, per case in bubblewrap with a fresh harness process per grading, the verdict mapped to pytest's exit status (an `os._exit(0)` before the assert is a pass) | `python3 plans/feal_probe.py --lane .` → `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, byte-equal re-run (`measure-final.txt`); real-pytest parity 12/12 (`R43PytestParity`) | 43 |
| `gate-flip-check` | Refuse a lesson whose conditional Gate refusals carry no later `Flip check (round N): <item> — fired|not fired — <evidence>` line | `python3 plans/gate_flip_check.py --lesson corpus/lessons/round-42.md` → red before the round-43 lines (`FLIPS total=2 unresolved=2`, `R43FlipCheck/runs.txt`), `unresolved=0` after; `--selftest` `ok=19/19` | 43 |

Routed ledger at docs time: 44 rows appended (the round-42 wave-2 queue, `R43RoutedQueue` 41 + `R43R42Defects` 3), two
field changes (R42-R4 closed, R42-R2 stale check nulled), 13 rows closed because their `check` passes on a clean clone of
the landing tip (`routed_open.py --observe` → `mismatched=0`, `ROWS total=60 open=38 blocked=1 closed=21`,
`routed_open=39 oldest_round=39`).

### Planned (round 44)

Axis state carried: calibration 8, coverage 7 (capped by the open L0 question `kengaku | round-33`), novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. The L1 holds the planner
seat; the round-44 data-walk seat `R43PlanNext` is wave-1 data (`.ufo/waves/round-43/build/R43PlanNext.md` when present).

- **Calibration (8):** re-freeze the C1 counter as `plans/round44_c1_verify.py` with the round-43 fence repairs inside the
  frozen rule, each with its own red hostile control — `rev-parse --absolute-git-dir` inside d and no `.git` FILE
  (`R43SentinelCounter` F1), no depth cap on the repo walk (F2), leg i on the parsed argv incl. absolute paths and
  argparse abbreviations (F3, `R43CritC1Counter` V2′), timeouts on parent-side git calls (F4) — plus the controls the
  round-43 mutation pass drafted for its 7 surviving guards (`R43MutC1Counter`). Mutant list: the `u = 18` advertised
  anchor/order behaviours with no frozen mutant (`R43CritEquiv` §3), each direction witnessed before freeze (Q29/Q33), or
  the 9 witnessed `round_close.py` survivors (`F42CritPlanNext` D1) — choose by which a do-nothing control and a
  witness-as-battery control separate.
- **Coverage (7, capped) — the largest uncovered grader class from the round-43 histogram**: F1 constant-compare (14
  tasks, 0 read; `R43ConsiderThese` `hist.md`), one probe shape for one pinned task (write-the-constant passes, nop and a
  mutated constant fail, byte-equal re-run), prior art checked by a seat before any sentence says "unpublished".
- **C2 counter content leg (routed R5 residual):** V10's DECISIVE is readable from the counter (`R43CritClaims` §1); a
  round-44 C2 counter needs a content check whose key is not in the instrument (e.g. a blind non-author mechanism table
  compared after the fact), with a red copycat control.
- **Routed (`corpus/routed-findings.jsonl`, `routed_open=39 oldest_round=39`):** envelope v2 (mode bits, unreadable
  entries — `R43ReviewEnvelope`); `R43MutC2Counter` 7 surviving V9/V10 guards; README lessons index parity (33 rows for 60
  lesson files) and round-41/42 evidence sections.

### Round-43 close (appended)

- Wave 2 was **not dispatched**: the 33-seat falsify spec is committed and validated (`falsify-dispatch.json`), but the
  run budget ended first. Round total **38 seats** (one v1 wave), below the run-9 floor of 64 — a conformance defect,
  recorded in `corpus/lessons/round-43.md` §Mistakes added by the L1 at close. The admission evidence for C1 battery
  honesty is therefore wave-1 only (`R43CritC1Counter`, `R43CritEquiv`, `R43RevMutRows`, the L1's difflib/fence-shape
  screen); the non-author closure decides.
- Final-tip re-measure: `.ufo/waves/round-43/integrate/measure-tip.txt`. Entry/PROVINCE errata appended after landing
  (E1–E2, "ninth pass"); C2 legs V4/V7/V9/V10 unchanged by them.

## Round 44 (hyaku run 9, 2026-10-26): five advertised behaviours of two gate tools demonstrated with value-attributed kills (5/5) under fence repairs F1–F6; a tenth TB2 grader executed (constant-compare of an agent-written file)

Baseline as read `0cb2e22598a39b7cd0bf5582d86d62492b57fa12`; freeze `5f16ed04b04a80a17a5a1a060c12093d9a152a64`; first
recorded probe run `45dc0bc81e42e02ecd272712086c372c8844b108`; wave dispatch `5e3d3aa06c6b7000929ac3e62563a39159c4501f`;
claim landing `2a263e5a56ef6d48d06805e1ccd106de5de9ba66` (battery44 + the feal-linear package); docs/closure batch
`02287eeddd912268655aba4014b1e277ab434e1e`. Frozen prereg `plans/round-44-claims.md`. Lowest non-retired axis: coverage
7, tied with novelty 7; coverage chosen (frozen tie-break), capped at 7 by the open L0 question `kengaku | round-33`. No
stagnation waiver. Landing measurement `.ufo/waves/round-44/integrate/measure-final.txt` (clean `--no-local` clone of
`02287eed`, round-44 envelope), baseline `integrate/measure-baseline.txt` at `5e3d3aa0`.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the five behaviours `plans/anchor_digest_check.py` and `plans/order_check.py` advertise that no landed battery demonstrates (U5 `digest-short` label, U6 `digest-long` label, U7 twin captures not a defect, U9 lessons read from the working tree, U14c unparseable claims name is exit 2; all `direct`; U3 dropped pre-freeze because battery43 already kills it) | **calibration** — advertised-vs-demonstrated mismatch count for two lane gate tools | `python3 plans/round44_c1_verify.py --lane .`: before `BATTERY fixtures=0`, `MUTANTS total=5 killed=0 survived=5`, `PREDICATE C1 fail`, exit 1 (`.ufo/waves/round-44/claims/control-c1-nothing.txt`; standing batteries 42+43 also `killed=0 survived=5`, `control-c1-standing-batteries.txt`) → after `PINS total=2 mismatched=0`, `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=5 killed=5 survived=0 invalid=0 null_detected=0 unattributed=0`, `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, `PINS-AFTER mismatched=0`, `PREDICATE C1 pass`, exit 0 (`integrate/measure-final.txt`; independent re-measure `residual/R44RCritRemeasure.md`) | mismatch count 5 → 0; score **8 → 8 held** (the lane's own choice: one round of five demonstrated rows on two tools does not lift the calibration ceiling) |
| C2 pinned TB2 `feal-linear-cryptanalysis` grader admitted with an executed 14-case sandbox probe (S138–S146, tier A) and a held-out predictor leg V11 | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (10 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 50→51, SOURCES 130→139 (+S147/S148 tier B from closure R1 → 141); one graded-state class new to the executed sample (an agent-written text file checked by substring membership of 100 constants embedded in the test file: the round-43 histogram's F1 class, 0 of 14 read before) | `python3 plans/round44_c2_verify.py --lane .`: before `checks=11 defects=8`, `PREDICATE C2 fail`, exit 1 (`claims/control-c2-nothing.txt`) → after `checks=11 defects=0`, `PREDICATE C2 pass`, exit 0 (`integrate/measure-final.txt`) | predicate met; score **7 → 7 held** (L0 cap) |

Limits found by the wave and the residual call (frozen counters not edited; routed): `R44SentinelFences` V1 (HIGH) — a
`.git/commondir` delegates the object store outside d and both F1 fences pass; V2 an include in the second config file;
V3 a repo git refuses to describe reads as no breach (no battery44 fixture uses any: grep for `commondir|include|
alternates|gitdir` over `plans/battery44/*.py` → directory names only); `R44LabratLaneInclude` — `lane_breach` reads an
include file outside d in the parent process; `R44CritV11` — V11's fixed-seed sample is memorizable (4 of 7 lookup
predictors pass; the landed predictor is a substring reading, `R44RCritEntryOverclaim` overclaims 0);
`R44SentinelSandbox` escapes 0; `R44MutC2V11` 3/6 V11 mutants caught by the freeze control; `R44MutC2Guards` 6/13.
Independent checks that held: real pytest 8.4.1 under `uvx -p 3.13` 14/14 (`R44PytestParity`); re-derivation 14/14 + 3
own cases (`R44CritIndep`); receipt byte-equal 3/3, not `-O` sensitive (`R44LabratRerun`); refetch 11/11 identical, no
upstream drift (`R44ScoutRefetch`); C1 controls reproduce 14/14 (`R44LabratControls`); verdict stable over 30 runs
(`R44LabratSiteStable`); dishonest-battery vectors 7/7 blocked (`R44CritC1Counter`); mutant rows 5/5, equivalent 0,
older batteries kill 0 (`R44RevMutRows`, `R44CritEquivU`); shape screen `flagged=0 max=0.541` vs the witness
(`integrate/shape-diff-battery44.txt`); entry quotes 36/36, findings wrong 0 (`R44RRevEntryQuotes`).

Other axes held: novelty 7 (no claim; prior art priced — of seven findings two published, two adjacent, three not
found, `R44ScoutPriorArt`; and an F1-class leak census, 14/14 TB2 F1 graders carry their answer in published files,
10/14 recomputable from a published generator/solution, `R44LabratF1Leak` — data for a later novelty claim, not
asserted here), depth 9, operability 8 (riders: `plans/gate_flip_check.py` extended, selftest 27/27, red→green on the
round-43 lesson; routed rider fixes 4/4 red/green drafted, `R44RoutedRiders`, not landed), freshness 8 (S138–S146
re-fetched cmp-identical twice; round-43 S147/S148 re-fetched), adjacency 8 (PROVINCE routing: cryptanalysis technique
unowned, `R44ConnSibling`).

### Round-44 capabilities (demonstrated this round)

| Capability | What it can now do | Evidence / command | First-working round |
|---|---|---|---|
| `held-out-predictor-leg` | Judge an entry's stated grader rule by executing the pinned grader on generated end states and requiring an entry-supplied `predict(text)` to agree, with no verdict stored in the instrument | `python3 plans/round44_c2_verify.py --lane .` → `V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0`; control `claims/control-c2-predictor.txt` (always-True, token-set, exact-lines red; substring ok) | 44 |
| `fenced-fixture-discovery` | Refuse a battery fixture whose git store, discovered repo or argv leaves its directory (gitdir file, depth, abbreviation, hang, include/alternates, repo above d) | `python3 plans/round44_c1_verify.py` SETUP refusals on `claims/hostile/f1…f6` (`control-c1-hostile-f*.txt`), each admitted or hung under the round-43 counter | 44 |
| `flip-verdict-check` | Turn a `not fired` Gate flip red when the entry it concerns cites the refused file | `python3 plans/gate_flip_check.py --lesson <lesson>`; red/green `integrate/flip-verdict-red-green.txt`; `--selftest` 27/27 | 44 |

### Planned (round 45)

Axis state carried: calibration 8, coverage 7 (capped by the open L0 question `kengaku | round-33`), novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Lowest non-retired: coverage 7 tied with novelty 7. Data walk:
`.ufo/waves/round-44/wave/R44PlanNext.md` (calibration: 21 `round_close.py` survivors priced under the round-44
contract; coverage: `password-recovery`).

- **Calibration (8):** re-freeze the C1 counter with the round-44 fence findings inside the rule, each with a red hostile
  control — `commondir` (V1), second-config include (V2), refuse-to-describe (V3), discovery without includes
  (`R44LabratLaneInclude`) — and price the `round_close.py` survivors as a third tool (stub order tool + stub census),
  or carry them. A do-nothing control includes the standing batteries (Q37).
- **Coverage (7, capped):** `password-recovery` (R44PlanNext) or a second F1 grader of a different shape; V11 with a
  per-run seed and a predictor-source lint (`R44CritV11` §9).
- **Novelty (7):** the F1 answer-leak census (`R44LabratF1Leak`, 14/14) is a candidate construct; needs its own red
  control and a dated prior-art receipt (`R44ScoutPriorArt` found the class published for other tasks).
- **Routed:** `routed_open=24 oldest_round=39`; rider fixes R39-R2, R42-R3-26/27, R42-R6 drafted red/green in
  `R44RoutedRiders/` (not landed); envelope v3 (`R44EnvelopeV3` 6/6 vs old 3/6) not landed.

## Round 45 (hyaku run 9, 2026-10-26/27): a fixture fence landed whose frozen counter a path-keyed control also passes (C1 not admitted on its counter; 8 of 10 held-out modules admitted); an eleventh TB2 grader executed, the second F1 constant-compare exemplar (C2 predicate met, four routed package defects)

Baseline lane tip `9d5f9715ebb0343984171be312d44e681f96b9a8`; freeze `b4fcd35141acda5fa0980a34dd29ab880b702ee6`;
first recorded probe run `05b02e2b7894a9c83219685f2374905e11c1beda` (reframed at `7d062c0` — the commit carried
three ENVELOPE wrapper lines; the receipt is bare probe stdout now); freeze amendments `9271dda4`; claim landing
`7d062c0ab330b98b370459a961ecd1c6484d7664` (C2 package) + `8f9a898e6c4a5ce213d5effa62f65dda2dd3f20d` (C1 fence).
Frozen prereg `plans/round-45-claims.md` (one pre-data amendment paragraph, amendment commit `9271dda4`; the file's sha256
`cb2fae38…` is pinned in `.ufo/waves/round-45/claims/frozen-digests.txt:1` — attempt 3 corrected an earlier cell that cited
that digest as a commit: `git cat-file -t cb2fae38` → `fatal: Not a valid object name`).
Lowest non-retired axis: coverage 7, tied with novelty 7; coverage chosen (frozen tie-break), capped at 7 by the
open L0 question `kengaku | round-33`. No stagnation waiver. Landing measurement `.ufo/waves/round-45/integrate/measure-final.txt`
(clean `--shared` clone of `8f9a898`, round-45 envelope): both counters `PREDICATE pass`, defects=0.

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the advertised fixture fence vs the observed one — `plans/fixture_fence.py` refuses every fixture whose git store, discovered repo or argv leaves `d`, and does so without reading outside `d` itself | **calibration** — advertised-vs-observed contradiction count over the 10 frozen hostile classes + 104 honest battery fixtures | `python3 plans/round45_c1_verify.py --lane .`: before `PREDICATE C1 fail` (`claims/control-c1-nothing.txt` stub → `leaked` everywhere; `control-c1-fence-r44.txt` r44 fence → `REFUSALS total=10 clean=3 leaked=3 read=4`, `contradicted=7`) → after `PINS total=33 mismatched=0`, `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`, `HONEST fixtures=104 admitted=104 refused=0`, `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`, exit 0 (`corpus/evidence/round45/c1-counter-run.txt`; attempt 3 re-measure `.ufo/waves/round-45/integrate/a3-tip-c1.txt` at `fbad1c5`). Attempt-3 control: a fence that inspects nothing and keys on the counter's fixture path also prints `PREDICATE C1 pass` (`claims/control-c1-fence-keyed_name.txt`) | **not admitted — unprovable on its frozen counter** (the counter does not separate the work from a no-inspection control; held-out: 8 of 10 hostile modules admitted, `a3w1/R45Ho*.md`; mutation 7/15 caught, `a3w1/R45MutLandedFence.md`). Calibration stays 8. Attempt 2 had written `improved`; corrected attempt 3. |
| C2 pinned TB2 `password-recovery` grader admitted with an executed 16-case sandbox probe (S149–S156, tier A) and a hardened held-out predictor leg V11 | **coverage** (lowest, tied) — one §Frontier TB2 sub-bullet narrowed by one task (11 of 89), one coverage-map bullet, one PROVINCE paragraph, knowledge files/index rows 51→52, SOURCES 141→149 | `python3 plans/round45_c2_verify.py --lane .`: before `checks=11 defects=8`, `PREDICATE C2 fail` (`claims/control-c2-nothing.txt`) → after `checks=11 defects=0`, `PREDICATE C2 pass`, exit 0 (`corpus/evidence/round45/counter-a-run.txt` and `counter-b-run.txt`, equal on every non-`ENVELOPE` line — not byte-equal: the envelope lines carry different scratch dirs and times, `cmp` → differ at line 1, corrected attempt 3; gate `defects=0`, `gate-call.txt`; attempt 3 re-measure `integrate/a3-tip-c2.txt` at `fbad1c5`) | **predicate met; admission for the closure to rule** — routed package defects the counter does not check: S152/S153/S154 anchors cite a line without the quote (`a3w1/R45RevRowCells.md`); entry `## Predictor` disagrees with the grader on lone-CR states 3/9 (`R45RevEntryQuotes.md`); V11 admits 4 lint-clean lookup predictors (`R45CritV11Bypass.md`), so "V11 hardened" overclaims; gate P10 runs an unpinned `uv` fetch outside the sandbox when host python lacks `Bio` (`R45SentC2Grader.md` F1). Coverage stays capped at 7. |

Attempt-1 inheritance is disclosed in the claims file: attempt 1 died on an invalid_prompt policy refusal without a
wave or a commit; its uncommitted drafts were re-verified and split (captures, probe, c2 counter, refusals45 kept;
the do-nothing-copy C1 counter draft and the C3 census draft discarded to `.ufo/waves/round-45/attempt1-unclaimed/`).

Limits found by the waves (frozen counters not edited; routed): `R45SentinelC2Sandbox` — a probe run escapes the seat
sandbox's HOME (`/root/.local` writes in one seat run: `w1/R45SentinelC2Sandbox.md`); `w1/R45CriticPredicate.md` — six
verdict-changing bypasses of the C1 counter (strace-log erasure B1, path keying B2, uncounted regions B3, stdout spoof
B4, no-open channels B5, blocked-open accounting B6); `R45CriticSeparability`, `R45CriticC2Instrument` audits (w1).

### Round 45 attempt 3 (2026-10-27, L1 `KengakuR45a3`)

Attempt 2's L1 and wave 2 (39 seats) were killed by the orchestrator session exit (23:57:36 -03); salvage commit
`fbad1c5`. Attempt 3 re-measured both counters on a clean clone of `fbad1c5` (`integrate/a3-tip-c1.txt`, `a3-tip-c2.txt`:
both pass), re-ran the no-harm set (`integrate/a3-noharm.txt`, all green, same values as `w2/R45ExecNoHarm.md`), and
re-dispatched the 34 killed wave-2 items as wave `a3w1` (`a3w1-dispatch.json`). Verdict cells above were rewritten from
those results. Self-assessment corrections (calibration bookkeeping, not a claim): the `cb2fae38` commit citation, the
"byte-equal" A/B receipts, the receiptless `untracked=2/14` lesson sentence, and the round title's "fence closed /
10/10 hostile classes refused" — four statements, each now with the command that refutes the old text
(`corpus/lessons/round-45.md` §Attempt 3). New criterion: `corpus/QUALITY.md` Q39 (keyed control).

### Round-45 capabilities (demonstrated this round)

None admitted. `plans/fixture_fence.py` and `plans/password_recovery_probe.py` exist and run, but the fence's
counter cannot separate it from a keyed control and held-out modules leak, so it does not enter the table as
`fenced-fixture-discovery`'s successor; the round-44 row keeps its round-44 evidence (`R45CritC1Overclaim` C1-C).

### Planned (round 46)

Axis state carried: calibration 8, coverage 7 (capped by the open L0 question `kengaku | round-33`), novelty 7, depth 9,
operability 8, freshness 8, adjacency 8. Data walk: `.ufo/waves/round-45/w1/R45PlanNext.md`.

- **Calibration (8):** re-freeze the fence counter under Q39 — opaque fixture names, the strace log delivered outside the
  fence's namespace (B1), the whole scratch root counted (B3), verdict on a channel the fence cannot print to (B4) — with
  the attempt-3 held-out modules (`a3w1/R45HoIncludeIf/`, `R45HoSymlinks/`, `R45HoCommondir2/`, `R45HoArgvEnv/`) as
  frozen refusals and the keyed fence as a red control; or the ranked-first alternative, `round_close.py` as a third tool
  (`MUTANTS total=26 killed=22 survived=4`, `R45PlanNext.md` §1).
- **Coverage (7, capped):** `polyglot-c-py` (`R45PlanNext.md` §2, oracle PASS offline on host gcc), or repair the C2
  package defects as supersede rows S152–S154 under Q34 plus the gate anchor-line check.
- **Novelty (7):** the F1 answer-leak census instrument (`attempt1-unclaimed/`) — crashes on first run
  (`R45PlanNext.md` §3); needs repair, its own red control and the dated prior-art receipt (`R44ScoutPriorArt`).
- **Routed:** `R45SentC2Grader` F1 (unpinned `uv` fetch in gate P10) and F2/F3 (P9 sees untracked files only and fails on
  wave evidence at the live tip); `R45CritV11Bypass` call-order and keyed-table predictors; `R45CritIntent` brace-prefix
  bypass for non-lane path options; considerthese `2026-10-26.md` proposal 2 (standing grader-admission counter with a
  red filler package); envelope v3 (`R44EnvelopeV3`) still not landed.


## Round 46 (hyaku run 9, 2026-10-27): a fixture fence repaired and re-judged under a counter that hides its own names (C1 predicate met); round 45's false line-level detail superseded and marked (C2 predicate met); a twelfth TB2 grader executed whose frozen counter fails V7/V8 (C3 not admitted)

Baseline lane tip `64ba8385ea10af1b78d367dcb242b92d97062af7`; stage-1 freeze `fd4129eb`; stage-2 instruments `cf7de6af`;
amendment `4fdeebaa`; C1 controls `7768716c`; fence landing `420eec9f`; C2 landing `c1ec334c`; C3 receipt `8d7f74ce`, package
`e9d20145`. Lowest non-retired axis: coverage 7 tied with novelty 7; coverage worked (C3), capped at 7 by L0
`kengaku | round-33`. Every receipt below opens with the lane commit it measured (round-45 closure D3).

| claim | axis | observed before → after, counting command | score / verdict |
|---|---|---|---|
| C1 the fixture fence's advertisement (refuse any fixture whose store, discovered repo or argv leaves `d`, without reading outside `d`) vs its observed behaviour, under a counter that hides its names (Q39) | **calibration** — contradiction count over 20 frozen refusal modules + 12 sealed held-out modules, with 104 honest fixtures that must be admitted | `python3 plans/round46_c1_verify.py --lane .`: before (base fence, `.ufo/waves/round-46/claims/control-c1-base-fence.txt`, measured `cf7de6af`) `REFUSALS total=20 clean=10 leaked=10`, `SEALED total=12 clean=0 leaked=12`, `CALIBRATION advertised=32 contradicted=22`, fail; 20 further controls fail incl. the round-45 keyed fence (`contradicted=32`) and 13 forged fences → after (`integrate/c1-landing.txt`, `420eec9f`) `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20`, `SEALED total=12 clean=12`, `HONEST fixtures=104 admitted=104`, `contradicted=0`, `PREDICATE C1 pass` | 8 → 8 held pending the wave-2 kill rule (verdict appended below) |
| C2 round 45's mislocated anchors, false word counts/ranges and lone-CR predictor superseded and marked | **depth** — live defective line-cited anchors + predictor/grader disagreements + entry range defects + errata marks | `python3 plans/round46_c2_verify.py --lane .`: before (`claims/control-c2-nothing.txt`, base) `A live=8`, `B disagree=6`, `C source_ranges_bad=4 errata_marks=0/5`, fail → after (`integrate/c2-landing.txt`, `e9d20145`) `A live=0 repaired=8 base_changed=0`, `B disagree=0`, `C source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`, `PREDICATE C2 pass`; four further controls fail (in-place fix, junk supersede, splitlines predictor, errata only) | 9 → 9 (harm repaired; no new depth credit) |
| C3 pinned TB2 `polyglot-c-py` grader admitted with an executed 18-case probe (S166–S172) | **coverage** (lowest, tied) — knowledge files 52→53, SOURCES 149→165 (+9 C2, +7 C3), §Frontier 11→12 of 89 | `python3 plans/round46_c3_verify.py --lane .`: before (`claims/control-c3-base.txt`) `checks=13 defects=8`, fail → after (`integrate/c3-landing.txt`, `e9d20145`) `checks=13 defects=2` (V7: frozen tags `both-print`, `toolchain` violated by no case; V8: `control-c3-echo` ran the gate's P10 before the receipt), `PREDICATE C3 fail` | 7 → 7 (capped); **not admitted** on its counter; counted move real |

### Round-46 capabilities (demonstrated this round)

None admitted yet: `plans/fixture_fence.py` passes its frozen counter, but its capability row waits on the wave-2
held-out kill rule. `plans/anchor_line_check.py` runs (`--selftest` red/green/junk; `live=0` at the tip) and is a gate
tool, not a capability row.

### Planned (round 47)

Axis state carried: calibration 8, coverage 7 (capped by L0 `kengaku | round-33`), novelty 7, depth 9, operability 8,
freshness 8, adjacency 8.

- **Coverage (7, capped):** re-freeze C3's counter under Q40 (every frozen tag with a violating case; pre-receipt
  controls with the gate's P10 disabled) and land the hardened probe revision `22b7779e…`
  (`.ufo/waves/round-46/w1/R46ExecC3Probe/`), or the next TB2 grader by uncovered class.
- **Novelty (7):** the F1 answer-leak census instrument (still unclaimed).
- **Routed:** `corpus/routed-findings.jsonl` R45-S5-7b..7e (V11 lookup predictors, gate P10 unpinned `uv`, brace-prefix
  intent, mutation re-attacks), the wave-2 findings appended below.
