# kengaku-shokunin corpus

Domain memory for LLM/model research & evaluation. Per
`~/projects/shokunin/CORPUS.md`: `knowledge/` entries cite a source;
`lessons/` entries cite round + evidence; every entry falsifiable or
marked opinion.

## What's here

| Entry | Covers | Primary source |
|---|---|---|
| `knowledge/benchmark-selection.md` | Task-class → benchmark mapping; contamination status; minimal stack | `llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` |
| `knowledge/godspeed-eval-findings.md` | Iteration-2 empirical results: K2 split, variant multiplier, calibration asymmetry, cost | `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-2.md` |
| `knowledge/telemetry-run-design.md` | Per-run telemetry fields, artifact set, phase gates, run-count floor | `llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` |
| `knowledge/local-model-index.md` | Bailian structured model index layout and field semantics | `~/.bailian/skills/bailian-docs-llm-wiki/models/index.md`, `models.jsonl` |
| `knowledge/local-bench-arena.md` | On-host 33-task battery: schema, two-model results, complementarity split | `~/archive/bench-arena/` CSVs (relocated from `~/bench-arena` in round 14), analyzed 2026-09-28 |
| `knowledge/ledger-route-telemetry.md` | Live lane-routing corpus: event taxonomy, reroute signatures, model×lane counts | `~/Projects/bounties/ledger/telemetry.jsonl` (7,218 lines; now absent), profiled 2026-09-28 |
| `knowledge/bench-arena-fresh-run.md` | Round-4 authored run: endpoint drift finding, 4-task reproduction slice, prediction error | `~/archive/bench-arena/` (then `~/bench-arena`) + `127.0.0.1:34113` live run 2026-09-28 |
| `knowledge/eval-theory-notes.md` | Digest: yao-second-half, creative-benchmark, trueskill-sorting, rlhf, bitter-lesson | `llm-wiki/wiki/karpathy/*` + `ai/{foundations,alignment-and-training}/`, read 2026-09-28 |
| `knowledge/gemini-benchmark-suite.md` | Four-signal godspeed test suite: reframe traps, variant multiplication, discovery widening, calibration meta-test | `llm-wiki/.../gemini-3.1-pro-godspeed-{benchmarks,test-battery}.md`, read 2026-09-28 |
| `knowledge/bailian-cli-telemetry.md` | Client-side CLI telemetry: 4,274 records, quota-vs-auth failure split, poll-verb rule | `~/.bailian/telemetry.jsonl`, profiled 2026-09-28 |
| `knowledge/bench-arena-round5-battery.md` | Full 33-task re-run under fixed endpoint: 20/33, 8 status deltas (4 P→F, 3 F→P, 1 F→HARNESS_DEFECT), truncation class, sha-identical set | `/tmp/bench-r5/` run (ephemeral; decisive CSV-joined numbers pasted in-entry) vs `127.0.0.1:34113`, graded 2026-09-28 |
| `knowledge/open-model-catalogs.md` | HF + OpenRouter live catalog schemas, filter/sort fields, open-weight twin links | `huggingface.co/api/models`, `openrouter.ai/api/v1/models`, probed 2026-09-28 |
| `knowledge/bench-arena-round6-stability.md` | Flip-set stability probe: n=3 per task → 5/8 scaffold-determined, 2/8 noise, 06 strategy-bound | `/tmp/bench-r6/` 33-run battery vs `127.0.0.1:34113`, graded 2026-09-28 |
| `knowledge/bench-arena-task27-timeout-anatomy.md` | `test_rc=124` root cause: `_active` hidden contract → thread-exception deadlock; r5 sol also semantically broken | instrumented `test.sh` + faulthandler probe, 2026-09-28 |
| `knowledge/bench-arena-round7-scaffold-ablation.md` | Scaffold-delta ablation: verbatim opencode wire capture + component ablation → 1/5 true scaffold flips (13), tools-without-system trap, `enable_thinking` no-op | `/tmp/bench-r7/` proxy capture + 65-call graded battery, 2026-09-28 |
| `knowledge/eval-design-digest-3.md` | Scaling retrospective (construct-validity gap, Goodhart root, Tetlock scoring) + ReAct protocol (failure-class table, composition rule) | `wiki/ai/scaling-and-forecasting/` + `agents-and-engineering/papers/react-reasoning-acting.md`, read 2026-09-28 |
| `knowledge/bench-arena-round7-noise-n25.md` | Noise tasks at n=25: 09 PASS-tilted 0.68 / 20 FAIL-tilted 0.32; draws non-iid (lag-1 +0.26/+0.32, burst-state coupling) | `/tmp/bench-r7-l2-executor/` n=25 probe, graded 2026-09-28 |
| `knowledge/eval-design-digest-2.md` | Second digest: sampling-proves-presence, reference-class, autonomy slider, spec-ability tiers | 25 remaining wiki files (count corrected r7), swept+read 2026-09-28 |
| `knowledge/bench-arena-round8-horizon.md` | Round-8 planning-horizon probe **analyzed**: A-ladder INC 7/10 > CKPT 1/10 ≈ MONO 0/10 (9/10 convention-tolerant), MOV-zero failure class (15/19), B manipulation non-binding (2/8 well-formed, corrupt ≈ clean p=0.25, hint null), C vacuous-rule over-repair (0/4 strict vs conflict 4/4, norule 4/4), 16-defect fix-landing audit (9 landed / 5 partial / 2 not), claim triage (1 blocked) | `corpus/evidence/round8-horizon/` (78/78 jobs, 268 records, md5 `df154cb5…`), analyzed 2026-09-28 |
| `knowledge/bench-arena-round9-replication.md` | Pre-registered replication on fresh seeds + new checkpoint-dose cell: INC 4/8 > CKPT4710 2/8 = CKPT710 2/8 > MONO 0/8; predictions hashed before the first request and scored (2/4 cell hits, MAE 0.094, 4/4 directional falsifiers unfired); pre-registered decision rule → **indeterminate**; ack leakage 16/48 + 8/56 | `corpus/evidence/round9-replication/` (284 records, `predictions-r9.sha256.repo`), run 2026-09-28 |
| `knowledge/eval-prior-art-calibration.md` | Novelty pricing of the 4 local findings against fetched public primaries: 3 known/incremental, 1 a direct replication (llama.cpp #7052); surviving novelty is instrument-level (emission-granularity ablation, vacuous-rule triple control); sub-3-bit scope limit | 40+ fetched URLs → `corpus/evidence/round9-fleet/prior-art.md`, 2026-09-28 |
| `knowledge/bench-arena-round11-power.md` | Powered preregistered rerun (n=64, MDE d=0.35): emission-granularity severity dose **ESTABLISHED** — paired diff +0.352 (t=+3.431, p=0.0011, CI [+0.147,+0.556], sign 26/7/31 p=0.0013); passes 29/64 vs 21/64 (McNemar p=0.0963, no pass-rate dose); Brier 0.153; C1–C4 prior-art verdicts | `corpus/evidence/round11-power/` (1473 records, bundle `prereg-bundle.sha256`, verdict in `analysis_r11.md`), run 2026-09-28 |
| `knowledge/bench-arena-round12-ladder.md` | Powered four-point emission-density ladder + batching/emission dissociation + second-family transport + 416 per-problem forecasts: `LADDER ESTABLISHED`, `DISSOCIATION ESTABLISHED`, `TRANSPORT DIRECTIONAL`, Brier `0.1288` / BSS `+0.0447` | `corpus/evidence/round12-ladder/` (4,114 records, hashed preregistration bundle, 733-check gate), run 2026-09-29 |
| `knowledge/kimi-model-routing-round18.md` | Round-18 kimi model-routing digest: 17-model n=2 TTFT/TPS/pass battery + M6 opencode-go row; defects (token-plan key-2/3 quota dead, dead client fields, unclamped global effort, reasoning_key DEF-9/10, 42 of 143 entries on unservable lanes); 13-entry table outcome (opencode-go = deepseek-v4.1-flash only, zai→devin glm policy, codex fast-mode no-go) | Parent repo `research/round-18-kimi-model-routing/` merges `4738fee`+`7e2c473`+`c2174a5`+`db82042`+`bd0c690`+`fbae972`; local index `corpus/evidence/round18-kimi-routing/README.md` |
| `lessons/round-1.md` | Path-correction, replace-don't-append, zero-width char hazard | LOG.md round 1, commit `90a5ce8` |
| `lessons/round-3.md` | Filename-judging missed on-host surfaces; complementarity vs pass-rate; NULL parsing; FAIL-latency signature | LOG.md round 3, this round's analysis |
| `lessons/round-4.md` | Endpoint-drift trap; n=1 flip on 03; FAIL-latency is subset-level not per-task | LOG.md round 4, `/tmp/bench-r4` run |
| `lessons/round-1-aggregator-audit.md` | Aggregator audit: corpus verdict, 13 re-verified claims, 3 defects (all closed round 4) | Aggregator L1 + reviewer lane, 2026-09-28 |
| `lessons/round-5.md` | Aggregate-correct ≠ model-right; truncation failure class; sha-identity = scaffold insensitivity | LOG.md round 5, `/tmp/bench-r5/` run |
| `lessons/round-7.md` | Unanimity ≠ attribution; tools-without-system trap; context mass shifts strategy; `enable_thinking` no-op | LOG.md round 7, `/tmp/bench-r7/` run |
| `lessons/round-4-aggregator-audit.md` | Aggregator audit of the round-4 delta (`a1af83c`): CONFORMANT, 0 majors / 2 minors; 21 citations independently re-executed | aggregator lane (non-author), 2026-09-28 |
| `lessons/round-5-aggregator-audit.md` | Aggregator audit of round-5 (`782dd2d`): NOT conformant, 2 majors (false 22-vs-25 file count; deleted README index row) + 3 minors; SHONEN bare-`[x]` = author attestation, regeneration owed | aggregator lane (non-author), 2026-09-28 |
| `lessons/round-8.md` | Unanalyzed run ≠ result; the lane's own prediction rule was violated with no gate; "critic accepted" ≠ "critic implemented" (2/16 fixes not landed); verify a manipulation binds; grader `ok` must be the needed conjunction; never strip fields from landed evidence; burst adjacency was maximal | LOG.md round-8 (retrospective), `corpus/evidence/round8-horizon/` |
| `lessons/round-9.md` | Pre-registered rules have three outcomes — don't launder "indeterminate"; direction replicating ≠ magnitude replicating; a control arm must be verified to be the control; point predictions can't be calibration-scored; price novelty before claiming it; integrity claims need a field-level diff, not a hash comparison; a missing contract file is a standing defect; SHONEN boxes are byte-diffed against a seed | LOG.md round-9, `corpus/evidence/round9-{replication,fleet}/` |
| `lessons/round-11.md` | Mock-smoke before ordering-sensitive runs; second-resolution ts breaks unique-first-record checks; shrinkage works on paired contrasts not levels; small-n null ≠ equivalence; Brier honesty cost; hashed bundles freeze typos; contingency rules belong inside the bundle | LOG.md round-11, `corpus/evidence/round11-{power,fleet}/` |
| `lessons/round-6-aggregator-audit.md` | Aggregator audit of the rounds 5–7 tree (`f147a27`): **NOT conformant** — 5 majors (falsified `0/12` PASS denominator; `LOG.md:9` rewritten in place; orphaned `85b22e3` citation, now dangling; 2 missing lessons index rows; `SCORECARD.md` absent while `MISSION.md` assigns an axis `AXES.md` does not define) + 7 minors; cited-hash ancestry sweep via `git merge-base --is-ancestor` | aggregator lane (non-author), 2026-09-28 — **aggregator-owned file: committed by the aggregator per `../PROTOCOL.md`; this lane writes only this index row** |
| `lessons/round-8-aggregator-box3-coldrun.md` | Aggregator non-author cold run of `SKILL.md` (SHONEN box 3): 20/20 executed commands reproduced at `0c51208` (23:31–23:33Z), incl. grader n=149 pre-extension; break points + gated steps recorded; caught `models.jsonl` cite-path break B1 and live ledger drift 7,218→7,226 minutes before the tree went absent | aggregator lane (non-author), committed by the aggregator `06cdc98` per `../PROTOCOL.md`; this lane writes only this index row |
| `lessons/round-12.md` | Ordered alternative → ordered test; measured power floors; heterogeneous forecast classes; mean-preserving probability tilts; repeatability ≠ replication; a floor is a result; pin landed bytes | LOG.md round 12, `corpus/evidence/round12-{ladder,fleet}/` |
| `lessons/round-13.md` | Storage labels are not prompt intent; schedule-derived denominators; cap-aware bounds; state fidelity and response-contract compliance are separate | LOG.md round 13, `corpus/evidence/round13-ack-state/` |
| `lessons/round-14.md` | An uncommitted round is not durable; index parity, landing-time pins, and the replay gate are closure conditions | LOG.md round 14, `corpus/evidence/round14-fleet/` |
| `lessons/round-9-aggregator-corpus-verdict.md` | Aggregator corpus-verdict lesson (rule-10 re-emitted at `f09ff1f`, canonical-form + rule-8 literal findings, routed rows); aggregator-owned file, indexed here only | aggregator lane, committed `e171cdf` |

### `evidence/` — durable run bytes and L2 analyses

`../PROTOCOL.md`'s evidence standard rejects `/tmp` pointers at closure, so the
run artifacts are committed:

| Dir | Contents |
|---|---|
| `evidence/round8-horizon/` | `horizon.py` (349-line probe, md5 `1c157e2a…`), `results.jsonl` (268 records **with `raw`**, md5 `df154cb5…`), `run.log` (78/78 jobs + SUMMARY, md5 `fc3b232f…`), `critic-defects.md` (16 design defects) |
| `evidence/round9-replication/` | `predictions-r9.md` + `.sha256` + `.sha256.repo`, `ordering.log`, `run_r9.py`, `replicate.py`, `results-r9.jsonl` (284 records), `replication.md` |
| `evidence/round9-fleet/` | 10 L2 artifacts + their scripts: `probeA.md`, `probeB.md`, `probeC.md`, `critic.md`, `harness-mutation.md` + `test_harness.py` (50 cases, exit 0), `prior-art.md`, `sibling-overlap.md`, `review.md`, analysis `.py`/`.out` |
| `evidence/round10-fleet/` | 11 L2 fleet artifacts (`r10-*.md`) + their independent scripts (`mutate_test.sh` sha256 `ad0511f2…`, `probe_ref.py`, `schema_probe.py`, `recompute_r8.py`, `recompute_r9.py`), raw endpoint captures (`models-34113.json`, `props.json`, `slots.json`), `final-harness.log`, `url-status.txt`, and `INTEGRATOR-NOTES.md` (fleet map, grader first-version defect + fix, connector adoption ruling, erratum adjudication) |
| `evidence/round11-power/` | preregistration bundle (`probe_plan_r11.md`, `power_analysis_r11.md`, `predictions-r11.md`, `prereg-bundle.sha256`, `ordering.log`, `prereg-precheck.log`), probe machinery + runner (`probe_r11.py`, `run_r11.py`), run bytes (`results-r11.jsonl` md5 `c42fe3d1…`, `run.log` md5 `281cb530…`), generated `analysis_r11.md` (md5 `14663359…`), promoted `recompute_r11.py` |
| `evidence/round11-fleet/` | wave-1 L2 artifacts (`r11-critic-design.md`, `r11-prior-art-{granularity,prereg}.md`, `r11-connector.md`, `r11-review-baseline.md`, `r11-mock-smoke.md` + `mock_server_r11.py` + mock run copies, `grader_r11_draft.py`, `recompute_r11_draft.py`, `r11-log-draft.md`), wave-2 artifacts, `INTEGRATOR-NOTES.md` (integration deltas + critic adjudications + landing record) |
| `evidence/round12-ladder/` | 9-file preregistration bundle + ordering proof; probe/prediction/power machinery; 4,114-record run (`results-r12.jsonl` md5 `9dd8aa2b…`, `run.log` `700d1ddd…`); generated `analysis_r12.md` md5 `029c3bcd…`; 18 files |
| `evidence/round12-fleet/` | 16-agent design/prior-art/replay/mutation/review fleet; 22 files including `INTEGRATOR-NOTES.md`; drafts retained verbatim, with round-14 errata recorded rather than silently rewritten |
| `evidence/round13-ack-state/` | Two stdlib audit scripts: schedule-derived ack denominators (`--selftest` 4/4) and truth-aware capped-raw analysis (`--selftest` 8/8); no endpoint traffic |
| `evidence/round14-fleet/` | Nine-agent landing verification: independent recomputation (28 claims), prior-art re-fetch, live-surface drift, sibling overlap, mutation battery, round-13 reconstruction, corpus drafts, bookkeeping drafts, landing gate, and L1 adjudications |
| `evidence/round18-kimi-routing/` | Digest index for parent round 18 (census/definitions/battery/battery-opencode/fastmode/routing trees): contents, file counts, hygiene-gate results; bytes stay in the parent repo (`research/round-18-kimi-model-routing/`) |

Re-verify the round-9 ordering proof without `/tmp`:
`cd corpus/evidence/round9-replication && sha256sum -c predictions-r9.sha256.repo` → `OK`.

In-repo gate (round 10, extended rounds 11–12 and pinned at round-14
landing): `grader.py` replays four committed probe trees (r8/r9/r11/r12)
offline. `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`,
exit 0; mismatch exits 1 and unreadable input exits 2. The r12 layer
regenerates both problem families, re-parses/re-grades all 1,328 graded
records, recomputes E1–E6 and every stored verdict/forecast line, verifies the
bundle/ordering chain, and md5-pins `results-r12.jsonl`, `run.log`, and
`analysis_r12.md`. `python3 grader.py --selftest` exercises S0–S7; the
round-14 mutation pass killed 4/4 fresh r12 mutations. Stdlib only, no
endpoint. It also subsumes the r9 ordering proof hermetically; the standalone
`predictions-r9.sha256.repo` check still must run from
`corpus/evidence/round9-replication/` because its path is cwd-relative
(round-10 critic F2). One stored value remains pinned as an adjudicated
erratum (`replication.md`: r9 final-turn state errors, stored 12/32,
recomputed 24/32).

## Coverage map

- **Benchmark selection**: covered (knowledge/benchmark-selection.md).
- **Search-shape mechanism evidence**: covered at iteration-2 depth (knowledge/godspeed-eval-findings.md).
- **Run harness / telemetry spec**: covered at alpha depth (knowledge/telemetry-run-design.md).
- **Model catalog access**: Bailian index + HF/OpenRouter APIs + local GGUF inventory (knowledge/local-model-index.md, knowledge/open-model-catalogs.md).
- **Eval theory**: covered at digest depth — autonomy/IID assumptions, diversity blindness, judge-vs-aggregator split (knowledge/eval-theory-notes.md).
- **Executed eval**: covered at battery depth — authored 4-task slice (r4) + full 33-task re-run under fixed endpoint (knowledge/bench-arena-round5-battery.md).

- **Wiki branch digest**: karpathy subtree + ai/foundations + ai/books fully swept (knowledge/eval-design-digest-2.md); remaining open surface = non-karpathy `ai/` topics beyond eval scope.
- **Cross-pipeline stability**: byte-identical solution set identified (16, 25, 28, 32, 33); flip-set classified at n=3 (`knowledge/bench-arena-round6-stability.md`) and **component-ablated at r7** — of 5 "scaffold-determined" tasks only 13 is genuinely scaffold-caused; tools-without-system → `finish=tool_calls` 14/15; temp not the lever (`knowledge/bench-arena-round7-scaffold-ablation.md`).
- **Multi-turn state tracking / planning horizon**: r8 built the instrument; r9 replicated probe A; r11 powered the middle contrast (+0.352, p=0.0011); r12 established the ordered four-point ladder (Page `L=1773.0`, `z=+9.452`), repeated the middle contrast (+0.297), dissociated batching from emission sparsity (+0.656), and tested a second task family (+0.177, directional at a 2/48 floor). See `knowledge/bench-arena-round12-ladder.md`.
- **Novelty pricing**: r9 priced 4/4 findings; r11 priced C1–C4 + M1–M3; r12 prices C1–C6 with fetched URLs — C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument, phenomenon-new 0 / instrument-new 1. Round-14 reviewer re-fetched 14 load-bearing URLs and reproduced every verdict (`evidence/round14-fleet/r14-review-priorart.md`).
- **Evidence durability**: every run byte and verification artifact through round 14 is committed and indexed. The r12/r13 one-round landing debt and the r8 raw-stripping incident remain documented; no headline claim rests solely on `/tmp`.

## Open gaps

- **n≥2 on flip-capable tasks**: CLOSED round 6 — 8 flip tasks + 3 controls at n=3; flips decompose to scaffold (5), noise (2), strategy-bound (1). See `knowledge/bench-arena-round6-stability.md`. **r7 refinement: component ablation reclassified the "scaffold 5" → 1 true scaffold (13), 3 noise (03/08/31), 1 weak pull (12)** — see `knowledge/bench-arena-round7-scaffold-ablation.md`.
- **Planning-horizon coverage**: CLOSED as an instrument, OPEN as a claim — round 8 built and ran a 3-probe multi-turn instrument (`evidence/round8-horizon/`, analyzed in `knowledge/bench-arena-round8-horizon.md`), round 9 replicated probe A on fresh seeds with a checkpoint-dose cell (`knowledge/bench-arena-round9-replication.md`). What remains unmeasured: a probe B whose manipulation actually binds (2/8 well-formed corruptions in r8), probe C at n≥12 (4 reps → 1–2 distinct generations), and the arithmetic covariate the r8 critic asked for and never got (defect #2).
- **27 test-timeout**: CLOSED round 6 — hidden-contract thread-exception deadlock + semantically-broken sol, not slowness. See `knowledge/bench-arena-task27-timeout-anatomy.md`.
- **Scaffold-delta mechanism**: CLOSED round 7 — verbatim wire capture (temporary proxy provider) + component ablation. Causal inventory: system prompt (context mass) drives strategy choice; `tools`+`tool_choice:auto` without system = `finish=tool_calls` harness defect; temperature absent→0.8 not causal; `enable_thinking` no-op (template has no think branch). See `knowledge/bench-arena-round7-scaffold-ablation.md`.
- **v2-vs-today scaffold drift** (new, round 7): the captured skills catalog may differ from v2's (v2 ran 1mo ago); E1 replay reproduced v2 direction on 13 but not 03 (v2's lone 03-PASS was a lucky draw — see r7 knowledge). Exact replay fidelity vs 1-month-old scaffold is unverified — attribute v2-side drift before citing v2 sols.
- **Probabilistic forecasts**: CLOSED round 11 at event level (3 predictions, Brier 0.153) and round 12 at per-problem level (416 pass events filed pre-request; Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`). Caveat: persistence skill dominates; family-2 base-rate transport failed (`2/48` both arms, BSS `-3.1474`).
- **No in-repo gate**: CLOSED round 10; extended round 11 to 280 checks/three trees, round 12 to 732 checks/four trees, and round-14 landing to **733** by pinning `analysis_r12.md`. S0–S7 all pass; 4/4 fresh r12 mutations killed.
- **Cold-agent executability**: CLOSED round 11 — aggregator non-author cold run reproduced 20/20 read-only commands; see `lessons/round-8-aggregator-box3-coldrun.md` and SHONEN box 3.
- **Ack metric denominators** (round 13): `-ack` storage labels mix ack-only and full-state prompts. Future rates must use schedule-derived intent denominators; r11 CKPT710 is 85.9% prefix / 84.4% bare on 384 true ack prompts, not 64.5% over 512 label rows.
- **Analysis regeneration** (round 14): `analysis_r12.md` is now md5-pinned, but regeneration remains path-dependent by one absolute `Generator source` line; every statistic independently reproduces. Make future generated reports path-insensitive.
- **Bench-arena path drift** (round 14): live tree relocated from `~/bench-arena` to `~/archive/bench-arena` with content hashes unchanged and no files newer than 2026-09-28. Living surface pointers use the archive path; frozen evidence retains its historical path.
- **Prior-art digest queue**: Laban et al. ICLR 2026 (`arxiv.org/abs/2505.06120`), Lanham et al. (`2307.13702`), and llama.cpp #7052 are fetched and used in pricing artifacts; synthesis into standalone corpus digests remains open.
