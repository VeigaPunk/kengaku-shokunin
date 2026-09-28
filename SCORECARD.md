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
  (r8: 0/1; r9: 1/1); (b) artifacts produced in the round that are committed
  **and** indexed **and** logged at round close (r8: 0/4 files; r9: see
  `git show --stat` for the round-9 commit); (c) `SCORECARD.md` rows whose
  evidence pointer re-runs (target 7/7).
- **novelty proxy** — fraction of the round's headline claims carrying a
  prior-art verdict with a fetched URL (r9: 4/4, see
  `corpus/knowledge/eval-prior-art-calibration.md`), split into
  phenomenon-new vs instrument-new (r9: 0/4 phenomena, 2/4 instruments).

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

Lowest post-move axis is **operability (4)**: nothing in this repo produces a
verdict. The move is a hermetic in-repo grader —
`corpus/evidence/analyze.py` promoted to a committed script that (a) replays
the stored `results.jsonl` / `results-r9.jsonl` through the parser and graders
offline (no endpoint), (b) recomputes every SUMMARY count, and (c) exits 1
when a recomputed count disagrees with the stored one. Falsifiable target:
`find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` ≥ 12
**and** the grader exits 0 on the committed files while exiting 1 on a
deliberately corrupted copy (one flipped `ok` field), with both runs recorded
in `LOG.md`.

## Retired

None. No cell scores 10 (the saturation floor) and no axis is a wrong fit:
calibration sits at 6 with three named ceilings, novelty was *lowered* by
evidence this round (7→5) rather than retired, and operability at 4 is the
next move. Retiring an axis here would hide the round-8 debt that motivated
round 9.

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
