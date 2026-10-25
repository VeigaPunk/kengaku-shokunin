# Round 12 connector — sibling instrument survey

**Agent:** ConnectorFleet — connector  
**Task:** Recheck the five sibling HEADs and protocol/aggregator records for overlap with round 12’s ordered-density test, transport task family, per-problem forecasts, and route any cross-axis implications.

## Survey boundary and current rounds

All sibling-overlap searches below use `git grep ... HEAD --`, so they inspect committed bytes rather than a sibling’s moving worktree. The one permitted endpoint scout is the only actor authorized to request `http://127.0.0.1:34113`; I sent no endpoint traffic. The round-12 ladder directory currently lists only `probe_plan_r12.md`, `probe_r12.py`, and `run_r12.py` (`glob corpus/evidence/round12-ladder/*` → those three paths); there is no committed `results-r12.jsonl`, `analysis_r12.md`, or `run.log` in that listing. Therefore, comparisons below are *prospective*: no round-12 result is asserted.

HEAD table command: `git -C /home/vgpnk/projects/shokunin/<repo>-shokunin log -1 --format='%h %ad %s'`.

| Repo | Exact HEAD command output | Latest lane round evidenced at HEAD / status note |
|---|---|---|
| `kasegi-shokunin` | `b7180b0 Mon Sep 28 20:48:33 2026 -0300 round-14: depth thin-cohort repair — checklist 28.6->106.6, anti-patterns 29.7->108.4, playbook 62.5->462.5 (pre-edit-mean bar); 3 SKILL falsifications + 2 corpus defects repaired; claim-anatomy sampling 3.6%->10.7% (D1-D13, 260/280 deviate)` | **Round 14** (HEAD subject). |
| `kake-shokunin` | `a209441 Mon Sep 28 21:42:41 2026 -0300 round-14: freshness — sweep row 78 verified identical 12/5/1 (sentinel PASS 45/47), PQ-5 publish-watch + PQ-12 re-check loop armed, scribe push-leg recovery caught in-round (9c28d29, live now 09-29 literal), 12 citation fixes, score stays 8 (armed capability != caught event)` | **Round 14** (HEAD subject). |
| `kumitate-shokunin` | `e0e5de1 Mon Sep 28 21:16:18 2026 -0300 round-12 close evidence: --close CLEAN (round=12 checks=13 errors=0)` | **Round 12** (HEAD close evidence; its preceding lane commit is `64a27e7`, `round-12: coverage 7 -> 8`). |
| `kotoba-shokunin` | `63ceba7 Mon Sep 28 21:44:36 2026 -0300 round-15: pre-registration for the checklist-execution move (operability 7.5; bands + falsifiers + scope fence, written before landing)` | **Round 15** (pre-registration at HEAD; not a round-15 outcome report). |
| `kagi-shokunin` | `4391b3b Mon Sep 28 20:39:21 2026 -0300 corpus: round-8 aggregator box-3 amendment (critic-absorbed)` | **Round 11 is the last lane-authored round in this repo HEAD** (`git -C ... log -8 --format='%h %s'` includes `301b9ec round-11: calibration axis-move...`; `git -C ... log --all --format='%h %s' --grep='round-12'` has empty output). The main-repo protocol report records kagi r12 `ok` and r13 `in-flight` (`.ufo/reports/round-12/protocol.md:56-57`); the r12 kagi report also says “Repo commit: round-12” (`.ufo/reports/round-12/kagi.md:1-5`). Thus the report/lifecycle says **r13 in-flight**, but the sibling repository HEAD is still on the r11 lane commit plus later aggregator amendments. Searches below honor the exact HEAD, not that discrepancy. |

## Instrument overlap — HEAD-pinned grep results

The commands use `git grep` rather than a worktree-only recursive grep so the negative is scoped to each committed sibling HEAD. In each row, the listed command was run once for each of `kasegi`, `kake`, `kumitate`, `kotoba`, and `kagi` with `repo="/home/vgpnk/projects/shokunin/${r}-shokunin"`. An empty result means `git grep` printed no lines (status 1).

| Instrument | Exact HEAD search pattern | Output for each of the five sibling repos | Verdict |
|---|---|---|---|
| Four-arm ordered emission-density ladder / confirmatory trend | `git -C "$repo" grep -n -i -E 'Brier|BSS|calibration slope|probabilistic forecast|per-problem forecast|Page.?s trend|Jonckheere|emission.granularity|forced.state checkpoint|ordered.trend|density.ladder|checkpoint density|hashed prereg|preregistration|power analysis' HEAD --` | `kasegi: ∅; kake: ∅; kumitate: ∅; kotoba: ∅; kagi: ∅` | **NO-DUPLICATE** |
| Second task family / transport or external validity | `git -C "$repo" grep -n -i -E 'task.?family|external.validity|transport (arm|effect|validity)|transportability|cross.task.*(validity|generaliz)|generalizability' HEAD --` | `kasegi: ∅; kake: ∅; kumitate: ∅; kotoba: ∅; kagi: ∅` | **NO-DUPLICATE** |
| Per-problem probabilities scored by Brier/BSS/calibration slope | Included in the first exact query above (`Brier|BSS|calibration slope|probabilistic forecast|per-problem forecast`); no such result in any of the five HEADs | `kasegi: ∅; kake: ∅; kumitate: ∅; kotoba: ∅; kagi: ∅` | **NO-DUPLICATE** |

The direct density-ladder sweep also returned no hits in any sibling HEAD:

```
git -C "$repo" grep -n -i -E 'emission.granularity|checkpoint scaffolding|forced.state checkpoint|CKPT4710|CKPT710|spillover.ask|post.checkpoint|checkpoint.*turn|emission.*checkpoint|ordered.trend|Jonckheere|Page.?s trend' HEAD --
```

Output: empty for all five repos. The task-family query above likewise returned empty. This is a committed-artifact search, not a claim about untracked/in-progress work or private operations.

### Near-matches and the replay-gate recheck

A broader `git grep -n -i -E 'prereg|pre.register' HEAD --` does find ordinary lane planning, but not the round-12 instrument: kumitate’s pre-registered S7 coverage/registry route (`kumitate-shokunin/LOG.md:393`, `SCORECARD.md:190,203,213,221,236,296`, `corpus/knowledge/executable-scorecard.md:178`, `corpus/lessons/round-12.md:135`) and kotoba’s pre-registered checklist outcome bands (`kotoba-shokunin/corpus/knowledge/checklist-execution-round15.md:56`). These are not hashed, before-request model studies with a power rationale and probabilistic outcome scoring. The exact outputs are visible by rerunning that command against each named `HEAD`.

One genuine adjacent idea is kotoba’s recommendation, “Skip ex-ante calibration. Record framer predictions before runs” (`git -C .../kotoba-shokunin grep -n -i -E 'ex.ante calibration|framer predictions before runs|predictions before runs|probabilistic.*(score|forecast)|Brier|BSS|calibration slope|reliability diagram|per.problem probability' HEAD --` → `HEAD:corpus/knowledge/sibling-description-rewrites-round8.md:371`). It is advice about framer predictions, not an operated per-problem probability/Brier/BSS/calibration-slope instrument; the verdict remains **NO-DUPLICATE**.

The prior round’s evidence-replay-gate negative was also rechecked. Command:

```
for r in kasegi kake kumitate kotoba kagi; do
  git -C "/home/vgpnk/projects/shokunin/${r}-shokunin" grep -n -i -E 'evidence.replay|hermetic.*replay|replay.*evidence|raw.*recompute|recompute.*raw' HEAD --
done
```

Output: the only hit is `kagi-shokunin/corpus/lessons/round-11.md:184`, which identifies **kengaku’s** `grader.py` as “evidence replay”; lines 181-188 explicitly distinguish that from kagi’s own revision-stamped command-per-claim ledger. No sibling owns that model-probe replay gate. Thus the four round-11 negatives (hashed experiment preregistration, power analysis, Brier scoring, and model-evidence replay) remain supported at the inspected HEADs.

Protocol/aggregator scope was checked separately, since those lanes live in the main repository:

```
git -C /home/vgpnk/projects/shokunin grep -n -i -E 'Brier|BSS|calibration slope|Page.?s trend|Jonckheere|per.problem forecast|second.task.family|external.validity|task.family transport|emission.granularity|preregistration.*(power|forecast)|power analysis' HEAD -- MISSION.md AXES.md PROTOCOL.md ROADMAP.md .ufo/reports/AGGREGATE.md .ufo/reports/round-10/protocol.md .ufo/reports/round-11/protocol.md .ufo/reports/round-12/protocol.md
```

Output: no matches. Protocol owns fleet-meta rules, not this lane’s model-eval measurements (`MISSION.md:11,14`); the r12 protocol decision on gate verdict vocabulary is scoped separately below.

## Round-10/11 cross-axis claims the r12 numbers can and cannot speak to

Committed-report search command and selected exact output:

```
git -C /home/vgpnk/projects/shokunin grep -n -i -E '34113|q4_0|KV cache|KV quant|telemetry_source|metrics scrape|Ack compliance|ack compliance|Brier|evidence.replay|telemetry attempts|telemetry-loss' HEAD -- .ufo/reports/round-10/kengaku.md .ufo/reports/round-10/protocol.md .ufo/reports/round-11/kengaku.md .ufo/reports/round-11/kasegi.md .ufo/reports/round-11/protocol.md
```

| Sibling report claim (grep output / line) | Relation to round 12 |
|---|---|
| Round-10 kengaku records the `:34113` `/v1/models`, `/health`, pid and cmdline surface (`.ufo/reports/round-10/kengaku.md:23`); round-10 protocol says the `8080→34113` repoint was serving and `/health` was ok (`.ufo/reports/round-10/protocol.md:223`). | R12 descriptors reread `/v1/models` and record model identity and best-effort pid/argv at both ends (`probe_plan_r12.md:164-172,191`). If the run lands, this can corroborate that run’s served-unit identity/descriptor record. Those reports are endpoint/config observations, not a behavioral result for the four-arm ladder; no r12 output is yet present. |
| Round-10 kengaku records `--cache-type-k/v q4_0`, `--kv-unified`, `--parallel 2`, context/template and pid 1299 as serving descriptors (`.ufo/reports/round-10/kengaku.md:57`). Round-11 says PR #21038’s q4_0 output perturbation is fetched prior-art context, **not** an r11 measurement (`.ufo/reports/round-11/kengaku.md:60`); its referral calls serving-plane authority unowned (`:90`). | R12 carries the same q4_0 / `--kv-unified` / `--parallel 2` stack as an experimental-unit descriptor and explicitly forbids cross-model generalization (`probe_plan_r12.md:27-30,164-172`). With no quantization/stack treatment contrast, R12 can condition its results on that stack but cannot estimate q4_0 materiality or corroborate a causal KV effect. The serving plane remains unowned and escalated to the integrator (`PROVINCE.md:24-25,43-48`). |
| Round-10 kengaku’s `loop.sh` parsing claim: five emitted fields read into six variables forced `telemetry_source=journal` for 33/33 v2 rows; it routes the operational meaning to kumitate (`.ufo/reports/round-10/kengaku.md:58`). Round-11 kasegi defines bounty mission termination using `TERMINAL` plus `telemetry attempts≥2` (`.ufo/reports/round-11/kasegi.md:20-21`). Round-10 protocol separately notes an opencode-store telemetry-loss path (`.ufo/reports/round-10/protocol.md:359-362`). | R12 stores response `finish`, `usage`, `wall_s`, and `request_ts`, and ack records carry response metadata (`probe_plan_r12.md:183-192`). It does not read `bench-arena/loop.sh`, OMP routing state, the bounty ledger, or opencode storage. These telemetry producers and meanings are not interchangeable; R12 cannot confirm or falsify their semantics. |
| Round-11 kengaku’s same-problem paired severity result is `+0.352` (`.ufo/reports/round-11/kengaku.md:45`); the report also says the first Brier value `0.153` rests on only three event-level probabilities (`:47,68,102`). | R12 preregisters a within-run replication on identical pids/seeds and the shared {7,10} turns (`probe_plan_r12.md:21,36-40,116-120`), then per-problem forecasts over 448 pass events with pooled/per-arm Brier, BSS, calibration slope/intercept and reliability (`:24,120,244-247`). This is a direct planned test of whether the paired contrast reproduces, and a larger forecast-scoring instrument—not an already-observed corroboration. |
| Round-11 kengaku reports ack compliance of 220/448 = 49.1% and 330/512 = 64.5%, attributing the spillover ask to the construct and routing reusable prompt implications to kotoba (`.ufo/reports/round-11/kengaku.md:48,89`). | R12 preserves the `Reply 'ok'`/checkpoint schedule and the turn-1 full-state ask stored as `-ack` (`probe_plan_r12.md:45-56`); its analysis contract has an ack-compliance line (`:249`). The planned result can compare compliance under the retained wording, but there is no wording ablation and no result yet. |

Two later aggregator observations are useful limits, not extra r10/r11 results: D-98 says the serving pin is pid-based and restart-fragile; D-99 says live-appended ledger totals lack per-number “as of” stamps (`.ufo/reports/AGGREGATE.md:1201-1202`, both OPEN). R12 does persist run-specific pid/argv best-effort plus per-request timestamps (`probe_plan_r12.md:164-172,183-192`), but that does not turn the pin into a persistent service identity or date the separate bounty-ledger counts.

## Status of round-11 report-outs

**Still unarbitrated as fleet decisions:** (1) whether the research-specific preregistration/power/forecast package should be an optional protocol convention; (2) kotoba’s reusable prompt-craft response to ack compliance and the spillover ask; and (3) integrator/operator disposition of q4_0 serving-stack materiality. **Not still unarbitrated as an ownership question:** (4) the kasegi tree-loss referral received a protocol ruling assigning filesystem recovery to the operator and document correction to kasegi. The factual state is nevertheless unreconciled by later committed reports.

Specific current-report check for the two “no later arbitration” rows:
`git -C /home/vgpnk/projects/shokunin grep -n -i -E 'ack compliance|spillover ask|q4_0|hashed predictions|Brier scoring|calibration slope' HEAD -- '.ufo/reports/round-12/*.md' '.ufo/reports/round-13/*.md' '.ufo/reports/round-14/*.md' .ufo/reports/AGGREGATE.md`
Output: empty (no matches; `git grep` status 1).

| Round-11 referral | Current arbitration state and evidence | Does round 12 change it? |
|---|---|---|
| **protocol — research preregistration standard** | The method standard remains unarbitrated. Protocol r12 did rule the separate r10 gate-interface question: a three-valued verdict with fleet-pinned `0/1`, declared remaining exit codes, and committed-evidence revision identity (`.ufo/reports/round-12/protocol.md:116-149`). That does not require hashed model-study bundles, power analysis, or Brier forecasts. The protocol/aggregator exact-term search above returned no hits for those statistical instruments in `MISSION.md`, `AXES.md`, `PROTOCOL.md`, `ROADMAP.md`, the aggregate ledger, or protocol r10–r12 reports. | R12 strengthens the lane’s own design and replay contract (`probe_plan_r12.md:224-268`); it does not impose a fleet standard. Keep the referral optional and ask protocol to decide scope. |
| **kotoba — ack compliance / spillover wording** | No r12–r15 protocol/aggregator report hit for “ack compliance” or “spillover ask” was found in the declared searches. Kotoba owns prompt/skill craft (`MISSION.md:17`; `PROVINCE.md:30-32`). | R12 retains the wording and measures compliance; it creates no wording variant and does not transfer the model-behavior finding to kotoba. |
| **integrator / unowned serving plane — q4_0 materiality** | No r12–r15 protocol/aggregator report hit for q4_0 was found in the declared search. Kengaku’s own boundary says the serving plane is unowned and flag changes are for integrator/operator arbitration (`PROVINCE.md:24-25,43-48`). | R12 pins, but does not vary, the same q4_0 configuration (`probe_plan_r12.md:27-30,164-172`); no causal materiality conclusion is added. |
| **kasegi + operator — bounty-ledger tree absence** | Protocol r12 explicitly says `~/Projects/bounties` is gone, assigns filesystem ownership to the operator and documents to kasegi (`.ufo/reports/round-12/protocol.md:276-280`); it rules the 86 dead pointers as tree-loss rather than fabrication and recommends a data-loss incident path (`:354-357`). But kasegi r13 reports `ledger/telemetry.jsonl` has three committed conflict markers and is in HEAD/index (`.ufo/reports/round-13/kasegi.md:56-59`), while kotoba r14 still says the root remains GONE (`.ufo/reports/round-14/kotoba.md:113-114`). Those are not reconciled to a same path/cutoff here. | R12 never reads the bounty ledger, so it neither revives nor re-verifies that surface. Ownership is adjudicated; whether the source tree is absent at a given location/time remains a cross-report reconciliation, not a kengaku measurement. |

## Contested-scope calls

- **Kotoba (prompt craft):** the `CHECKPOINT — output the FULL state now.` ask, `Reply 'ok'.` ack wording, and turn-1 full-state request stored as `-ack` are fixed benchmark conditions (`probe_plan_r12.md:45-56`). Kotoba should receive a craft recommendation for future prompt authors; kengaku retains the causal/model result and must not change the hashed treatment to make the response tidier (`PROVINCE.md:30-32`).
- **Kumitate (harness/telemetry):** the probe uses sequential direct chat-completion calls and records response fields; it does not invoke OMP routing, fallback, `loop.sh`, or kumitate’s orchestration gate (`probe_plan_r12.md:64-67,183-203`; `MISSION.md:16`). Keep `finish`/`usage`/latency as response metadata, not route-health or mission telemetry. The second-family “transport” means transfer of an eval finding across task families, not request transport or runtime orchestration (`probe_plan_r12.md:69-105`).
- **Protocol (fleet statistics):** Page’s trend test, per-problem Brier/BSS/slope, and the power/preregistration bundle are domain-specific research choices (`probe_plan_r12.md:108-149,224-268`); protocol may decide whether to offer an optional fleet convention, but kengaku owns the model-study analysis and should not universalize `nwrong`, Page’s test, or forecast scoring to lanes without such outcomes (`MISSION.md:11,14`; `AXES.md:16`). The r12 protocol gate verdict rule does not transfer the analysis implementation to protocol (`.ufo/reports/round-12/protocol.md:122-130`).
- **Integrator/operator (serving plane):** descriptor re-recording supports stack-scoped interpretation only; r12 has no q4_0 counterfactual, so do not claim a measured cache effect or adjust server flags from this result (`PROVINCE.md:24-25,43-48`; `probe_plan_r12.md:27-30`).
- **Kasegi (domain ledger):** mission/dispatcher ledger semantics remain kasegi’s; filesystem availability is operator-side (`MISSION.md:13`; `.ufo/reports/round-12/protocol.md:278-280`). Keep any renewed source census or event interpretation out of the model-probe analysis.

## PROVINCE.md report-out drafts — evidence to send, not absorb

Round-12 report-outs (evidence sent, not absorbed): (1) **protocol** — “Protocol: the current sibling HEAD search found no operator of the Page-trend density ladder, task-family transport arm, or per-problem Brier/BSS/calibration-slope package; kotoba’s framer-prediction advice is complementary, and kumitate’s pre-registered registry plan is not a model study. Protocol r12’s three-valued gate interface is useful but does not decide whether hashed model-study preregistration, power rationale, forecast scoring, and evidence replay should be an optional fleet convention. Please arbitrate that convention without imposing it on unrelated lanes.” Evidence/carry path: `corpus/evidence/round12-fleet/r12-connector.md` and `corpus/evidence/round12-ladder/probe_plan_r12.md`.

(2) **kotoba** — “Kotoba: round 12 preserves the `CHECKPOINT` full-state ask and `Reply 'ok'` acknowledgements, including the known turn-1 full-state/`-ack` quirk, while adding a six-line ack-compliance analysis contract. This is a fixed-condition measurement, not a prompt-craft fix; please advise benchmark authors whether the ask should be distinguished from an ack label, and leave this bundle unchanged.” Evidence/carry path: `corpus/evidence/round12-fleet/r12-connector.md` and `corpus/evidence/round12-ladder/probe_plan_r12.md:45-56,247-249`.

(3) **integrator / unowned serving plane** — “Integrator: round 12 re-pins the same Qwen unit and q4_0 KV / `--kv-unified` / `--parallel 2` descriptors, but contains no alternate-cache or alternate-stack arm. It can support only a result conditional on this stack, not a causal q4_0-materiality estimate; keep flag-change authority outside kengaku and require matched serving descriptors for cross-model comparisons.” Evidence/carry path: `corpus/evidence/round12-fleet/r12-connector.md` and `corpus/evidence/round12-ladder/probe_plan_r12.md:27-30,164-172`.

(4) **kasegi + operator** — “Kasegi / operator: the round-11 absence report was routed to kasegi, and protocol r12 has now assigned the `~/Projects/bounties` filesystem issue to the operator while leaving document correction with kasegi. The later kasegi r13 report says `ledger/telemetry.jsonl` is in HEAD/index with three conflict markers, while kotoba r14 still reports the root gone; please reconcile location and observation cutoff before updating the province or reusing historical counts. Round 12 does not read that ledger.” Evidence/carry path: `corpus/evidence/round12-fleet/r12-connector.md`, `.ufo/reports/round-12/protocol.md:276-280,354-357`, `.ufo/reports/round-13/kasegi.md:56-59`, and `.ufo/reports/round-14/kotoba.md:113-114`.

DUPLICATE-INSTRUMENT RISK: NONE