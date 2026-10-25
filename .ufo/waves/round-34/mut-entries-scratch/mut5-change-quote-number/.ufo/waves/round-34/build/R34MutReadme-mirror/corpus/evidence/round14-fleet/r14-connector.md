# Round 14 connector — sibling-overlap ruling and landing

**Scope:** Read-only survey of the five sibling repos at their current HEADs, the standing referrals in `PROVINCE.md`, and the round-12/13 evidence relevant to new report-outs. No sibling or other repository files were changed. Negative ownership findings below are bounded to the inspected HEADs and the stated search vocabulary.

## 1. Current sibling HEADs

**Command:** `git -C ../<lane>-shokunin log -3 --oneline` for each of `kagi`, `kotoba`, `kumitate`, `kasegi`, `kake`.

**Observed:** first line is the HEAD used for the survey; the next two are included to make the sample point auditable.

| Sibling | Three most recent commits (newest first) |
|---|---|
| kagi | `8a6ec16`, `587fda0`, `2486643` |
| kotoba | `d85982d`, `e80f5f5`, `57f9e38` |
| kumitate | `f9f8e4d`, `d64b511`, `2f114f0` |
| kasegi | `b021dc9`, `0f2dca0`, `eb5b590` |
| kake | `ab87a48`, `88a4f4e`, `4214101` |

The tops of each sibling's `SCORECARD.md`, `PROVINCE.md`, and `SKILL.md` were read (up to line 60 only). The targeted source citations below identify the closest relevant artifacts.

## 2. HEAD-scoped instrument search

**Command:**

```sh
PAT='Page.?s (ordered|trend)|Jonckheere|Brier|BSS|calibration slope|per.problem.*(forecast|probabilit)|hashed predictions|prereg.bundle|power analysis|emission.granularity|multi.arm.{0,20}checkpoint|checkpoint.{0,20}(ladder|model|prompt|emission)|CKPT4710|CKPT710|probe.tree|evidence.replay|replay.evidence|hermetic.*replay|raw.*recompute|recompute.*raw'
for r in kagi kotoba kumitate kasegi kake; do
  git -C ../${r}-shokunin grep -n -i -E "$PAT" HEAD -- || true
done
```

**Observed:** the only match was `../kagi-shokunin/corpus/lessons/round-11.md:184`, which calls **kengaku's** `grader.py` “evidence replay” while distinguishing Kagi's own claim ledger (`:181-187`). There were no sibling-HEAD matches for Page/Jonckheere, Brier/BSS, per-problem forecasts, hashed prediction bundles, power analyses, emission-granularity/multi-arm ladder terms, or a probe-tree replay gate. Ordinary lane-local pre-registration and checkpoint/replay terms are considered separately below; the word alone is not an ownership match.

**Verdict:** no checked sibling owns any of the five requested instruments as an LLM-evaluation instrument or fleet-wide convention. The decision remains specific to these HEADs; it does not assert that no untracked/private work exists.

## 3. Per-sibling rulings

**Command for each row:** the HEAD search in §2, with the row's repo substituted. Citations are to current sibling files and lines.

| Sibling / HEAD | Closest relevant scope or near-match | Page ordered-trend test | Per-problem Brier/BSS | Preregistration-bundle convention | Multi-arm checkpoint-ladder probe | Evidence-replay gate over >3 probe trees |
|---|---|---|---|---|---|---|
| **kagi** `8a6ec16` | `../kagi-shokunin/PROVINCE.md:3-6` scopes vault/credential hygiene. `../kagi-shokunin/corpus/lessons/round-11.md:181-187` distinguishes its revision-stamped command-per-claim ledger from kengaku's evidence replay. | No | No | No | No | **No.** The sole match points to kengaku's grader; Kagi's ledger is a different claim/citation unit. |
| **kotoba** `d85982d` | `../kotoba-shokunin/SKILL.md:3-15` scopes prompt/skill-file craft and explicitly excludes general model-output prompt engineering. Nearest statistical wording is advice to record framer predictions before runs (`../kotoba-shokunin/corpus/knowledge/sibling-description-rewrites-round8.md:371-374`), not a scoring instrument. Its corpus verifier checks index/pointer integrity, not probe results (`../kotoba-shokunin/verifiers/verify_corpus_integrity.py:2-40`). | No | No — prediction advice only | No — its pre-registration is checklist outcome bands, not a research bundle (`../kotoba-shokunin/LOG.md:544-550`) | No | No — corpus/harness verification is not model-evidence replay. |
| **kumitate** `f9f8e4d` | `../kumitate-shokunin/PROVINCE.md:3-6` and `../kumitate-shokunin/SKILL.md:16-21` scope orchestration/tooling. The “checkpoint” is persisted `LoopState`/dispatch-resume state (`../kumitate-shokunin/corpus/knowledge/loop-driver.md:85-114`), and its replay-falsification probes test the runtime frontier replay (`../kumitate-shokunin/corpus/knowledge/runtime-remainder-census.md:335-347`), not saved LLM-probe results. Its pre-registration is a local coverage/registry move (`../kumitate-shokunin/LOG.md:569-580`). | No | No | No — local pre-registration is not a fleet LLM-study convention | No — orchestration checkpoint is a neighboring mechanism, not prompt-emitted state arms | No — runtime replay tests are not a multi-tree evidence-replay gate. |
| **kasegi** `b021dc9` | `../kasegi-shokunin/PROVINCE.md:1-4` scopes bounty/security research; its documented pipeline validates bounty claim packages and operator-gated submissions (`../kasegi-shokunin/SKILL.md:28-44`). | No | No | No | No | No — package validation is a different evidence object and domain. |
| **kake** `ab87a48` | `../kake-shokunin/PROVINCE.md:1-6` scopes web properties/publishing. `../kake-shokunin/scripts/probe-delta.mjs:2-26` reads webzites `probe-history.jsonl` and explicitly says exit 0 is a **report, not a gate**. | No | No | No | No | No — website sweep history is not LLM-probe evidence replay. |

**Near-match ruling:** Kotoba and Kumitate do use pre-registration for lane-local checklist/coverage changes, but neither has the searched hashed, pre-request LLM predictions + power rationale + outcome-scoring bundle. Kumitate's orchestration checkpoint and replay tests are likewise adjacent terms, not the multi-arm prompt-treatment ladder or a replay of empirical model-probe trees.

## 4. Round-13 acknowledgement audit — Kotoba report-out evidence

**Commands:**

```sh
python3 corpus/evidence/round13-ack-state/audit_ack_schedule.py
python3 corpus/evidence/round13-ack-state/analyze_ack_state.py
```

**Observed:** the audit classifies the r11 `A-CKPT710-ack` rows by prompt intent, not by the storage label. It reports six true ack-only turns (2–6, 9; 384 prompt/response rows) and turns 1 and 8 as full-state-request controls even though both were logged as `-ack` (`corpus/evidence/round13-ack-state/audit_ack_schedule.py:20-30,57-83`; `corpus/evidence/round13-ack-state/analyze_ack_state.py:55-64,153-168`). On the true ack-only turns, exactly bare `ok` is **324/384 = 84.4%**; `startswith('ok')` is 330/384 = 85.9%. Each full-state control turn had **0/64** bare-`ok` replies: turn 1 had 38 exact states, 3 nonexact states, 23 cut off at the 80-character cap; turn 8 had 14 exact, 23 nonexact, and 27 capped (analysis output; generation intent at `corpus/evidence/round11-power/run_r11.py:61,76-80`). The broader `-ack`-label denominator is 330/512 = 64.5%, so the old 49–65% figures are label-wide proxies, not the true ack-only bare-response rate.

**Verdict:** this is a concrete prompt-craft implication for benchmark authors: derive acknowledgement denominators from the requested turn intent, and label/score full-state asks separately from ack-only turns. Keep capped/unparseable outputs unresolved rather than calling them model failures; the audit is one served unit with repeated turns clustered within 64 pids, not a population or causal claim.

## 5. Standing referral status

**Command:**

```sh
for r in kagi kotoba kumitate kasegi kake; do
  git -C ../${r}-shokunin grep -n -i kengaku HEAD -- LOG.md || echo NO_LOG_MATCH
done
```

**Observed:** Kagi's matches are generic verifier adjacency (`../kagi-shokunin/LOG.md:308-310,497-499`) and a shared OpenCode surface (`:655`); Kotoba's are an older overlap, prompt-alias note, and dead-citation tally (`../kotoba-shokunin/LOG.md:46,121,763`). Kumitate, Kasegi, and Kake returned `NO_LOG_MATCH`. None of the sibling-log hits records uptake of the four referrals below. This check is deliberately limited to sibling `LOG.md` mentions of `kengaku`; it cannot rule out an unmentioned decision elsewhere.

| Standing referral from `PROVINCE.md` | Current status / evidence | Disposition |
|---|---|---|
| **Kotoba — output-contract / ack craft** (`PROVINCE.md:35-41,62-66`) | No ack-specific uptake in Kotoba's current `LOG.md`; the r13 audit above sharpens the finding and separates prompt intent from the `-ack` storage label. | Referral remains unacknowledged in the checked log; **file the r13 craft addendum** below. |
| **Integrator — unowned serving plane** (`PROVINCE.md:43-56,67-72`) | R12's connector says the q4_0/`--kv-unified` stack was pinned without an alternate-stack/cache contrast, so it cannot estimate a causal serving effect (`corpus/evidence/round12-fleet/r12-connector.md:92,100`; single-unit scope at `corpus/evidence/round12-ladder/analysis_r12.md:5`). R13 reanalyzes r11 prompt intent, not the serving stack (`corpus/evidence/round13-ack-state/analyze_ack_state.py:150-156`). | Existing authority referral stays open; **no new integrator report-out** from r12/r13. |
| **Kasegi + operator — ledger absence** (`PROVINCE.md:74-81`) | The r12 connector records Protocol's earlier split of filesystem recovery to the operator and document correction to Kasegi, but the conflicting later path/availability reports were not reconciled (`corpus/evidence/round12-fleet/r12-connector.md:82-93`). Kasegi's current `LOG.md` has no `kengaku` hit. | Ownership was referred/adjudicated; the factual location/cutoff remains unresolved. Keep as an existing reconciliation item, not a new r12/r13 report-out. |
| **Protocol — research preregistration standard** (`PROVINCE.md:58-61`) | R12's connector still finds the hashed model-study/power/forecast convention unarbitrated; the separate r12 gate-verdict interface ruling did not adopt such a standard (`corpus/evidence/round12-fleet/r12-connector.md:90`). No sibling `LOG.md` uptake surfaced. | Still a standing protocol question; no new r12/r13 evidence requires imposing the convention on other lanes. |

## 6. Round-12 replay and landing status

**Commands:**

```sh
python3 corpus/evidence/round12-ladder/recompute_r12.py --out /dev/null
git status --short -- corpus/evidence/round12-ladder corpus/evidence/round12-fleet corpus/evidence/round13-ack-state
```

**Observed:** the read-only recomputation reported `recompute_r12: wrote /dev/null from 4114 records` and `VERDICT R1 ladder: LADDER ESTABLISHED`. The filed analysis records R1 ladder established, R2 repeats r11, R3 dissociation established, R4 transport directional, and R5 forecast skilled (`corpus/evidence/round12-ladder/analysis_r12.md:52-61`); the ordering record timestamps the run launch and result landing (`corpus/evidence/round12-ladder/ordering.log:1-8`). `git status` returned all three directories as untracked: `?? corpus/evidence/round12-fleet/`, `?? corpus/evidence/round12-ladder/`, `?? corpus/evidence/round13-ack-state/`.

**Verdict:** the artifacts are present and the r12 summary is reproducible, but these evidence trees are not tracked at this r14 survey. **[INFERENCE]** A round-scoped respawn can orphan completed evidence unless closeout explicitly checks tracked status or carries unresolved artifact paths forward; the status proves their current untracked state, not by itself the duration or the cause.

## 7. Recommended new report-outs

**Recommendation:** file Kotoba and aggregator. Do not open a new integrator report-out; preserve its existing unresolved disposition. The protocol and Kasegi items remain standing matters, not new r12/r13 candidates.

| Candidate | Decision | Draft one-line wording |
|---|---|---|
| **Kotoba** | **FILE** | “Kotoba: r13 prompt-intent scoring finds bare `ok` on 324/384 (84.4%) true ack-only turns, but 0/64 on each `-ack`-logged full-state request (turns 1 and 8; capped outputs remain unresolved); please advise benchmark authors to derive compliance from prompt intent and report full-state asks separately, without changing this fixed treatment.” |
| **Integrator** | **NO NEW FILING** | “No new serving-plane report-out: r12 records one fixed q4_0/`--kv-unified` stack without a counterfactual and r13 reanalyzes r11 responses, so the existing serving-authority referral is unchanged.” |
| **Aggregator** | **FILE** | “Aggregator: the complete r12 ladder and fleet trees remain untracked in the current r14 checkout despite the recorded r12 run; **[INFERENCE]** add a round-close tracked-artifact/carry-over check so per-round respawn cannot orphan completed but unlanded evidence.” |

## Evidence digests

**Command:**

```sh
sha256sum \
  corpus/evidence/round12-ladder/results-r12.jsonl \
  corpus/evidence/round12-ladder/analysis_r12.md \
  corpus/evidence/round12-ladder/prereg-bundle.sha256 \
  corpus/evidence/round12-ladder/ordering.log \
  corpus/evidence/round12-fleet/r12-connector.md \
  corpus/evidence/round11-power/results-r11.jsonl \
  corpus/evidence/round13-ack-state/audit_ack_schedule.py \
  corpus/evidence/round13-ack-state/analyze_ack_state.py
```

**Observed SHA-256:**

| Evidence file | SHA-256 |
|---|---|
| `corpus/evidence/round12-ladder/results-r12.jsonl` | `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1` |
| `corpus/evidence/round12-ladder/analysis_r12.md` | `1ceebd7568aab4ecba694b983d7f3312c957402c7841b7597d6ed4506b6453e3` |
| `corpus/evidence/round12-ladder/prereg-bundle.sha256` | `e12b591b27795231ce51d1ea68b9aa57ddebe55a2df8bf763839e3528edf02a6` |
| `corpus/evidence/round12-ladder/ordering.log` | `d381cb873b64137fd9e35daff187ef4bd1de79395dc9b66a75c2c5cbe5a2c35a` |
| `corpus/evidence/round12-fleet/r12-connector.md` | `86bea5722c1d9aaf76f52a0fa5331b341c1cfa98b22f574f45b8bc712dcc45c5` |
| `corpus/evidence/round11-power/results-r11.jsonl` | `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad` |
| `corpus/evidence/round13-ack-state/audit_ack_schedule.py` | `f250abd518f4d7802c5c1008bedcf52603c393957b57cbb9c54e28710bba066d` |
| `corpus/evidence/round13-ack-state/analyze_ack_state.py` | `87d01584e3ab3022139b044b26dcdb16936b67b12ed413dee67f7e4c253404e4` |

The r12 preregistration manifest also pins the design, power analysis, filed predictions and predictor scripts by SHA-256 (`corpus/evidence/round12-ladder/prereg-bundle.sha256:1-9`); the r13 scripts print and verify the r11 input SHA-256 above. No `/tmp` artifact is used as evidence.

## Gaps

1. The sibling ownership ruling is a HEAD-scoped text search plus cited scope/near-match review. It cannot discover private or untracked sibling work, nor does it turn absence of a keyword hit into universal proof.
2. The `LOG.md` uptake sweep was limited to `kengaku` mentions as requested. It found no acknowledgement for these referrals, but an arbitration filed without naming kengaku may not appear in that result.
3. **[INFERENCE]** The province's replay description still says three probe trees (`PROVINCE.md:19`, r8/r9/r11), while `grader.py` now maps r12 JSONL/analysis/runlog inputs (`grader.py:74-76`) and contains an r12 replay section (`grader.py:1491-1509`). Update the declared tree count when the landing is recorded; this connector did not edit or rerun the project-wide grader.
4. The r12 replay command above reproduced the R1 ladder verdict only; the other reported verdicts are cited from the filed analysis rather than claimed as independently recomputed by this connector.
