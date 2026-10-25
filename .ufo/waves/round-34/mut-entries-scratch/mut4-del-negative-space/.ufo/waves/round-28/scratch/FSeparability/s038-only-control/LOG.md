# kengaku-shokunin — Iteration Log

- 2026-09-28 — round 0: minted as shonen.
- 2026-09-28 — round 1: rewrote SKILL.md with eval decision tables, benchmark anti-patterns, research-note structure, route-telemetry interpretation, cited sources. Evidence: prompt path `~/wikillm/llm-wiki` absent on host (`find -maxdepth 3`, 0 hits); grounded instead on working copy at `~/Projects/webzites/repos/llm-wiki` — read `wiki/ai/agents-and-engineering/{benchmark-shortlist-for-godspeed-research,godspeed-umwelt-iteration-2,godspeed-umwelt-iteration-3-alpha-shittycodex,gemini-3.1-pro-godspeed-benchmarks,gemini-3.1-pro-godspeed-test-battery}.md` and `Home.md`; model index at `~/.bailian/skills/bailian-docs-llm-wiki/models/` (180 families, 413 models, generated 2026-09-11).
- 2026-09-28 — round 1 (corpus, operator interjection): created `corpus/` per `~/projects/shokunin/CORPUS.md` — README index/coverage/gaps, 4 knowledge entries (benchmark-selection, godspeed-eval-findings, telemetry-run-design, local-model-index) each citing wiki file paths or `head` command output, 1 lessons entry citing this round's LOG/commit/report. Verified corpus files free of zero-width chars (`grep -P '[\x{200B}-\x{200D}]'` clean).
- 2026-09-28 — round 3: closed "no executed task / no route telemetry" gaps by analyzing on-host artifacts instead of wiki notes. Evidence: `~/bench-arena/` — qwenlocal-v2 PASS 21/33 vs grok45 19/33, near-disjoint win-sets (10 vs 8), FAIL latency median 60.9ms < PASS 79.5ms, `telemetry_available=n` rows carry `"NULL"` strings; `~/Projects/bounties/ledger/telemetry.jsonl` — 7,218 events profiled, taxonomy `dispatcher_tick`/`mission_parked`/`mission_dispatched`…, reroute chains via `lane_parked`+`to`, model×lane counts. Landed as `corpus/knowledge/{local-bench-arena,ledger-route-telemetry}.md`, `corpus/lessons/round-3.md`, SKILL.md "Local telemetry surfaces" section.
- 2026-09-28 — round 4: executed first authored eval (closes SHONEN "end-to-end task" checkbox) + digested un-digested wiki branches + probed open model catalogs. Evidence: `curl 127.0.0.1:34113/v1/models` returned the served GGUF id while `localhost:8080/v1/models` 404'd against Jitsi — `qwen-local` provider config is stale, root-causing v2's `"NULL"`/`journal` telemetry; ran 4-task slice (01,02,03,05) via direct `chat/completions` + repo `grade.sh`: 1/4 PASS vs ex-ante predicted 2/4 — `03` flipped PASS→FAIL on fresh generation (sol_sha differs); read `yao-second-half`, `creative-benchmark`, `llm-trueskill-sorting`, `rlhf`, `bitter-lesson`; probed HF + OpenRouter APIs (460 models). Landed `corpus/knowledge/{bench-arena-fresh-run,eval-theory-notes,open-model-catalogs}.md`, `corpus/lessons/round-4.md`, SKILL.md battery/catalog/eval-theory sections, README index+coverage+gaps, SHONEN checkbox.
- 2026-09-28 — round 4 (aggregator audit closure): landed `corpus/lessons/round-1-aggregator-audit.md` (orchestrator-authored, uncommitted) and closed its 3 defects — evidence: `grep 'response.md'` 0 hits in alpha note vs line 156 in `godspeed-umwelt-iteration-3.md` (re-pointed `telemetry-run-design.md` citation); `PROVINCE.md` still said `~/wikillm/llm-wiki` (corrected to `~/Projects/webzites/repos/llm-wiki`); README dangling `wiki/ai/books` example reworded with verified paths (`ai/books` exists; `are-we-smart-enough` is `biology/books/`). Audit's next-round gaps also closed: gemini pages digested (`knowledge/gemini-benchmark-suite.md`), executed eval done (above), `~/.bailian/telemetry.jsonl` profiled — 4,274 CLI records, `usage token-plan` 85% fail (quota 429 ×675), auth-expiry 2,685 errors, `video task get` poll-noise rule (`knowledge/bailian-cli-telemetry.md`).
- 2026-09-28 — round 5: closed the last executable gap — full 33-task battery re-run under the fixed endpoint, plus remaining-wiki digest. Evidence: probed `127.0.0.1:34113` (`/v1/models` + `/health` 200, Qwen3-Coder-30B-A3B UD-IQ2_XXS); wrote ex-ante predictions (`/tmp/bench-r5/predictions.md`) before first request; ran all 33 tasks via direct `chat/completions` (temp 0.2, max_tokens 4096, n=1) and graded with repo `grade.sh`: **20/33 PASS vs predicted 20/33 exactly, but 8/33 status deltas vs v2** (03,09,13,20 P→F; 08,12,31 F→P; 06 F→HARNESS_DEFECT via `finish=length` @4096 tok mid-regex). 5 tasks byte-identical to v2 (16,25,28,32,33 — incl. stable-FAIL 33). FAIL slower on wall+tokens (1.71s/260 vs 0.84s/128) — inverted vs v2 signature. Digest: swept remaining 25 wiki files (count corrected round 7) (`grep -inE 'eval|benchmark|test|measur|metric|verif|correct|fail'` + targeted reads) → `corpus/knowledge/eval-design-digest-2.md`. Landed `corpus/knowledge/{bench-arena-round5-battery,eval-design-digest-2}.md`, `corpus/lessons/round-5.md`, SKILL.md telemetry-rule updates, SHONEN all-checkboxes verified.
- 2026-09-28 — round 6: closed two open gaps — flip-set n≥2 probe + task-27 timeout anatomy. Evidence: endpoint re-probed (`/v1/models`+`/health` 200); ex-ante predictions at `/tmp/bench-r6/predictions.md` before first request; 33-run battery (8 flip tasks + 3 controls × n=3, same direct-API settings as r5) graded by repo `grade.sh`: **5/8 flips scaffold-determined** (03,08,12,13,31 — all unanimous at n=3), **2/8 sampling noise** (09,20), 06 strategy-bound (`finish=length` again at max_tokens 8192, 65.5 s — exponential expansion; compact reps emitted wrong regex); predicted ≥5/8 noisy → direction right, magnitude wrong (scaffold dominance underestimated). Task 27: instrumented `test.sh` with `faulthandler.dump_traceback_later(25)` + phase markers — reference PASSes in 0.23 s; r5 sol deadlocks on `Barrier(7)` because 6 reader threads crashed on `rw._active` AttributeError (private attr never in prompt.md — hidden contract); `_active`-alias patch unblocked it to reveal real bugs (`release unlocked lock`, writer-preference violated); r6 fresh gen fails instantly on `TypeError: Condition(condition=…)` — third failure family. Landed `corpus/knowledge/bench-arena-round6-stability.md`, `bench-arena-task27-timeout-anatomy.md`; updated SKILL.md parsing rules (scaffold-vs-noise n≥2 rule, strategy-bound truncation, rc=124 crash-deadlock signature, status≠sha), r5 canary table + 27 correction, corpus README index/gaps.
- 2026-09-28 — round 7: closed the round-6 "scaffold-delta mechanism" gap by capturing the verbatim opencode wire request and ablating components. Evidence: temporary `cap34113` provider + logging proxy (`127.0.0.1:18099`→`34113`) captured the exact `raw` request (`/tmp/bench-r7/capture/001-*-req.json`) — scaffold = raw-agent system prompt + powered-by + `<env>` + `<available_skills>` (~11.9K chars, 94% skills catalog → +4.3K prompt tok) + `tools:[janitor_auth,skill]`/`tool_choice:auto` (~+400 tok template injection; total +4.7K vs bare) + no temperature (server default 0.8) + max_tokens 32000; `enable_thinking` confirmed no-op (jinja has no think branch). Ran 65-call ablation (5 flip tasks × E0 anchor + E1 replay / E2 −system / E3 −tools / E4 +temp0.2 × n=3), graded by repo `grade.sh`: **only 13-stack-min is genuinely scaffold-determined** (bare-API sorted-stack O(n) FAIL ×4 runs → canonical monotone-stack PASS 9/9 under any scaffold); **E2 = trap condition** (tools sans system → `finish=tool_calls` empty content 14/15, e.g. `skill(name="min_stack")`); **temperature not the lever under scaffold** (E4≈E1 — but see post-critic E5 amendment below: temp is a partial lever on *bare* prompts); 03/08/31 reclassify to sampling noise, 12 weak scaffold pull. Predicted decoding-dominant → wrong (system presence was the lever). Landed `corpus/knowledge/bench-arena-round7-scaffold-ablation.md`, `corpus/lessons/round-7.md`, README index/coverage/gaps, SKILL parsing rules (unanimity≠attribution, tools-without-system trap, context-mass strategy shift, enable_thinking no-op) + transport-path fix + r7 citation. opencode.json restored byte-identical post-capture.
- 2026-09-28 — round 7 (L2 fleet + post-critic amendment): dispatched 9 L2s (batched, MISSION bucket routes). Findings landed: (a) executor n=25 probe on 09/20 — noise holds but gains tilt: 09 PASS-tilted p̂=0.68 (single FAIL mode = window-fn-in-WHERE, 8/8 regex discordance-0), 20 FAIL-tilted p̂=0.32 (5 contract-handling modes; r6's 3/3 PASS was lucky, r5's FAIL was modal); **draws non-iid** — lag-1 autocorr +0.26/+0.32, permutation p≈0.01, output=f(prompt,seed,burst-state): same-seed replays differ across bursts and a 09 request interleaved into a 20 seed=42 replay changes its output (`--cont-batching --parallel 2` shared decode state). Landed `corpus/knowledge/bench-arena-round7-noise-n25.md`; r6 matrix/canary rows annotated with r7 corrections. (b) labrat: E2 trap is temperature-invariant — 9/9 `finish=tool_calls` at temp 0.2, calls `skill(name=<task-shaped>)` (`min_stack`, `datetime_extractor`, `python_debugging`). (c) revenger: 13 mechanism reconstructed — bare-API sorted-stack `d268ef61` byte-identical ×5 (r5+r6×3+E0), all scaffolded sols correct-family incl. E1-r2 **byte-identical to v2**; scaffold contains zero stack tokens → non-semantic context-mass shift; P≈0.0003 hypergeo. (d) scout: swept remaining wiki `ai/` surface — digested `scaling-hypothesis-revisited` (construct-validity gap, contamination≡p-hacking, Tetlock scoring) + `react-reasoning-acting` (failure-class table, composition rule) into `corpus/knowledge/eval-design-digest-3.md`; `ai/` sweep now complete. (e) reviewer+scribe audits: all 35 matrix cells, token deltas, capture composition verified; 7 discrepancies found and fixed (E1-vs-E0 delta is +4.7K not +4.3K; v2 input range 4,309–4,674; 'empty content' 13/15; tool-call names inferred vs observed; README drift-gap wording; stale r6 bullet). (f) sentinel: config byte-identical restore confirmed, no 18099 listener, no secret-shaped strings in captured payload. (g) critic: caught the missing {no-system × temp-0.8} cell → ran E5 (bare@0.8: 13=PFF, 08=PPP, 03=FFF) — corrected the verdict to **scaffold dominates family choice; temperature is a second, bare-prompt-only lever**; its harder claims (E1-13 sha=FAIL sha, E4/08=FFF) falsified against report CSVs.
- 2026-09-28 — round 8 (retrospective, written round 9): built and ran the planning-horizon probe; the lane was retired before analyzing it, so this entry records the debt and its evidence. `corpus/evidence/round8-horizon/` — 16-defect critic pass (`critic-defects.md`, md5 `3386406…`) applied to `horizon.py` (349 lines, md5 `1c157e2a…`), 78/78 jobs (`run.log:1-78`, md5 `fc3b232f…`), 268 records (`results.jsonl`, md5 `df154cb5…`), SUMMARY: A-INC 7/10, A-MONO 0/10, A-CKPT 1/10, B-corrupt-plain 3/8, B-corrupt-hint 3/8, B-clean-plain 6/8, B-clean-hint 6/8, C-conflict 4/4, C-benign 1/4, C-norule 4/4, C-MONO 4/4; `finish=stop` 258/258, parse failures 0/268. Three non-closures, all charged to round 9: (a) **no ex-ante predictions** — `grep -ril predict /tmp/bench-r8 corpus/evidence/round8-horizon` → 0 hits while r5/r6 filed 25- and 17-line prediction files, a regression against `SKILL.md` checklist item 1 + anti-pattern 4; (b) nothing analyzed, logged or committed — `grep -c -i 'round.8\|horizon' LOG.md` → 0 and `git ls-tree -r f147a27 --name-only | grep -c evidence` → 0 (4 files working-tree-only); (c) the landed `results.jsonl` was a `raw`-stripped duplicate (md5 `01547cfa…`, 97,023 B vs run 125,577 B; field-level diff: key-set delta exactly `{raw}`, 0 semantic differences over 268 records) — the durable copy had destroyed precisely the failure-class evidence the analysis needs.
- 2026-09-28 — round 9: **calibration axis-move** — created `SCORECARD.md`, closed the round-8 evidence debt by pre-registered analysis, restored the predict→observe→score loop with a mechanical ordering proof, and priced the lane's novelty against public literature. Evidence: (a) 10 L2s in one batched call (executors probe A/B/C, labrat replication, critic fix-landing + falsification, reviewer citation/state audit, mutation-tester harness battery, scout prior art, connector sibling overlap, scribe scorecard drafts) → all artifacts committed under `corpus/evidence/round9-fleet/` (18 files). (b) r8 analysis: ladder A-INC 7/10 > A-CKPT 1/10 ≈ A-MONO 0/10, 9/10 under convention-tolerant grading (15/19 failing INC records are the MOV-zero convention — 9 dropped zero keys, 6 left the MOV source at its pre-MOV value — and 4 are genuine drift; all 5 INC error onsets are MOV turns; model-initiated recovery 0/16); paired sign tests with problem as unit INC>CKPT 7:1 p=0.0703, INC>MONO 7:0 p=0.0156, CKPT>MONO 1:0 p=1.0 (upper bounds at ESS≈0.54·n≈5.4); probe B **did not bind** (corrupt vs clean 0:3 discordant p=0.25, `raw` byte-identical corrupt↔clean in 3/8 pids per arm, 4/8 corruptions inert to the tail ops, 2/8 fabricated `true_mid+5`, 1/8 on an untouched key → well-formed 2/8; hint null 1:1 p=1.0; the single `propagated` label is a frozen-key carry, and key-level retagging finds exactly 1 genuine propagation event, scored `other`); probe C benign **0/4 strict** vs conflict 4/4 and norule 4/4 with byte-identical final asks (476 chars, 296 prompt tok, differing only in the fabricated rows) → rule-integration cost, not transcript shape, at 1–2 distinct generations per cell; fix-landing audit of the 16 critic defects → 9 landed / 5 partial / 2 not landed (#6 corrupted-key-exercised, #15 fixed op histogram); grader mutation battery 50 cases → 12 defect candidates, **1 live** (`grade_c` computes `over_repair` then omits it from `ok`, `horizon.py:288`, and derives `preserved` from self-declared violations `:277-279` → C-benign 1/4 is 0/4); parser fidelity 188/188 re-extractions. (c) r9 pre-registered replication on fresh seeds (`2000+pid*29`, pids 101–108) with a new `A-CKPT710` dose cell and 28 filler requests (284 records, 0 errors): predictions hashed **before** the first request (sha256 `2a4f62ef…`, `ordering.log` 21:17:48Z, first `request_ts` 21:17:58Z — `corpus/evidence/round9-replication/`, re-checkable via `sha256sum -c predictions-r9.sha256.repo`), observed INC 4/8 > CKPT4710 2/8 = CKPT710 2/8 > MONO 0/8 (mean final `nwrong` 0.500/0.875/1.375/2.250; 0 parse failures, 0 `finish=length`; best paired test INC>MONO 4:0 p=0.125); prediction score 2/4 cell hits, MAE 0.094 of n, onset predicted 5.0 vs observed 5.8, all 4 directional falsifiers unfired; the critic's independent pre-registered rule (claim (i) survives iff CKPT ≤2/8 **and** INC ≥5/8) returned **indeterminate** — INC one problem short — and is reported as such; ack compliance degraded vs r8 (16/48 and 8/56 non-turn-1 ack turns emitted full states, all 8 pids) so the r9 checkpoint cells were partly INC-like, making the scaffold reading conservative. (d) novelty priced against fetched primaries: 3/4 r8 findings known/incremental (Laban ICLR 2026 SNOWBALL +15–20%; Huang ICLR 2024 self-correction null; FollowBench/Multi-IF/MultiChallenge for late rules) and the non-iid finding a **direct replication** of llama.cpp issue #7052 (same prompt + seed at temp 0 across 8 slots → 5–8 unique completions); surviving novelty is instrument-level (emission-granularity ablation; vacuous-rule triple control) → novelty scored 7→5 (`corpus/knowledge/eval-prior-art-calibration.md`). (e) contract repairs: `SCORECARD.md` created (owned pair + all six axes, fixed measurement proxies, ±1 rubric, planned/retired; calibration 2→6, operability 3→4, depth 7→8, coverage 5→6, freshness 4→5, adjacency 7→8); `SHONEN.md` regenerated byte-identical to the `../PROTOCOL.md` canonical seed — 4 boxes (the dropped "instructions executable without oral context" box restored), marks `[~] [~] [ ] [~]`, zero self-attested `[x]`, closing the round-5 aggregator audit's owed regeneration; `PROVINCE.md` now enumerates 8 surfaces + refusals + 3 report-outs (kotoba / kasegi+kumitate / kagi); `corpus/README.md` index completed in both directions (21 knowledge rows = 21 files, 10 lessons rows = 10 files, new `evidence/` section) and the false "planning-horizon … unmeasured locally" gap replaced; `SKILL.md` 312→414 lines: anti-patterns 8→13, a new planning-horizon/transcript-shape rule block (cell semantics + 9 measurement rules), the prediction-ordering gate in checklist item 1, cited-source bullets 16→20. (f) endpoint re-verified this round: `curl -s -m 5 http://127.0.0.1:34113/v1/models` → `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, `/health` → 200, no drift since r4. (g) reviewer defect triage: 7 of 8 queued defects closed above; defect 6 (SWE-Bench Pro vs the contamination anti-pattern) **rejected** — `SKILL.md:24` prefers Pro *because* Verified is contaminated, matching the shortlist note's "Add Now" #2 (`benchmark-shortlist-for-godspeed-research.md:37-38`).
- 2026-09-28 — round 9 (corrections + routed-defect closure): closed the round-6 aggregator audit's routed items (`corpus/lessons/round-6-aggregator-audit.md` — aggregator-owned, indexed by this lane, **not** committed by it per `../PROTOCOL.md`). **Major 1** (falsified count, rule 4): errata appended to `corpus/knowledge/bench-arena-round7-noise-n25.md` — `:23-24` "0/12 PASSes" → **0/17**, since the entry's own `:15` table fixes task 09 at 17/25 PASS; the `0/25` discordance figure is unchanged. **Major 2** (append-only violation, rule 9): this entry *is* the required appended note — round 7's amendment rewrote `LOG.md:9` in place (`git diff 85b22e3 f147a27 -- LOG.md` → one −/+ pair, "status flips"→"status deltas") and swept four in-tree count corrections with it; the rewrite stays as history and is named here, not undone. **Major 3** (orphaned citation): `.ufo/reports/round-7/kengaku.md:3` cites `kengaku-shokunin@85b22e3`, which the lane amended away — `git merge-base --is-ancestor 85b22e3 HEAD` → exit 1, `git rev-list HEAD | grep -c 85b22e3` → 0, `git fsck --lost-found` → dangling; **the live hash for all round-7 content is `f147a27`**, and the round-9 commit is its child. **Major 4** (index rows): 3 lessons rows added (round-4/round-5 aggregator audits + the round-6 audit) → `grep -c '^| \`lessons/' corpus/README.md` → 11 = `ls corpus/lessons | wc -l`. **Major 5** (missing axis artifact): `SCORECARD.md` created with a recorded `novelty` sub-axis mapping and fixed proxies; **routed to protocol** — `grep -n novelty ../AXES.md` → 0 hits while `../MISSION.md:14` assigns it, so either add `novelty` to `AXES.md` or ratify the mapping at `SCORECARD.md:9-17`. **Minors:** (6) flip/delta terminology swept — `corpus/README.md:22`, `SKILL.md:204,409` in place, `corpus/lessons/round-5.md` by appended errata; (7) ledger count drift 7,218 → **7,224** (`wc -l < ~/Projects/bounties/ledger/telemetry.jsonl`, re-run this round) with the counting command appended to `corpus/knowledge/ledger-route-telemetry.md`; (8) `/tmp` pointers labelled ephemeral (`SKILL.md:408`, `corpus/README.md:22`, `corpus/evidence/round9-fleet/INTEGRATOR-NOTES.md` §4) — round 9 files no claim on a `/tmp` pointer alone; (9) `SHONEN.md` regenerated byte-identical to the canonical seed (normalized diff → `True`; 4 boxes, 4 evidence lines, marks `[~] [~] [ ] [~]`, zero self-attested `[x]`); (10) commit identity configured once per the lane-authorship invariant — `git config --local user.name kengaku-shokunin` + `user.email kengaku@shokunin.local`; the round-9 commit is the first under it; (12) round-9 provenance reconciliation appended as `corpus/evidence/round9-fleet/INTEGRATOR-NOTES.md` §1 — the "different execution" reading at `probeB.md:7,130` is **falsified** (key-set delta exactly `{raw}`, 0 semantic differences over 268 records, same order), L2 artifacts committed verbatim with corrections in the notes file. Reviewer defect 6 (SWE-Bench Pro vs the contamination anti-pattern) **rejected** with evidence: `SKILL.md:24` prefers Pro *because* Verified is contaminated, matching `benchmark-shortlist-for-godspeed-research.md:37-38`.
- 2026-09-28 — round 9 (count reconciliation; supersedes two figures inside the round-9 entry above, both of which were accurate when written and were overtaken by artifacts landed minutes later in the same round): `corpus/evidence/round9-fleet/` holds **19** files (18 L2 analyses/scripts + `INTEGRATOR-NOTES.md`), and `corpus/README.md` indexes **11** lessons rows for **11** lessons files after the aggregator's `round-6-aggregator-audit.md` row was added — `grep -c '^| \`lessons/' corpus/README.md` = `ls corpus/lessons | wc -l` = 11; knowledge rows 21 = 21 files (`grep -c '^| \`knowledge/' corpus/README.md` = `ls corpus/knowledge | wc -l` = 21).
- 2026-09-28 — round 10: **operability axis-move** — landed the repo's first in-repo verdict gate and closed the round-9 §Planned target. Evidence: (a) `grader.py` (repo root, 936 lines, sha256 `ce64f16aeee54376296b874ae9e6ee49f4191174a416eed0299a1e8e56665e96`, stdlib-only, no endpoint, byte-identical output under `PYTHONHASHSEED` 1/99/unset) replays both committed probe trees offline: metas regenerate from seeds (r8 `700+pid*13` 10/10, r9 `2000+pid*29` 8/8, incl. the `+977` retry chain), every graded record (r8 140 A + 32 B + 16 C; r9 128 A) re-parsed from stored `raw` via the shipped `extract_json_block` (brace-fallback included — 2 r9 `A-CKPT710` pid-104 records parse only via it) and re-graded against meta-derived truth, all 11 `run.log` SUMMARY lines + every stored number in `replication.md` recomputed (observed table, census, exact-binomial sign tests, onset ladder, failure classes, ack compliance, cross-round + prediction-scoring tables, sha256 chain, ordering proof). **Falsification runs, both recorded here per the target:** `python3 grader.py` on the committed tree → **exit 0**, `CHECKS n=149 mismatches=0 errata_pinned=1`; on deliberately corrupted copies → **exit 1** — independent battery `/tmp/kengaku-r10/mutate_test.sh` (mutation-tester L2, written *before* the grader existed, sha256 `ad0511f2b8a49d3f9bd597afd0b99f46bf84b587af044c98150bdae92dd803f8`, committed copy + `final-harness.log` under `corpus/evidence/round10-fleet/`): M0 control exit 0; M1 one flipped stored `ok` → exit 1 with exactly `MISMATCH r8.replay.A-INC.ok: 1/100 records differ (first: (1, 1, 'ok'))` (layer isolation proven — the flip is summary-insensitive since SUMMARY counts last-graded-turn oks); M2 `A-INC: 7/10`→`8/10` in run.log → exit 1 (`r8.summary.A-INC` + 2 cross-round checks); M3 digit bump inside an A-MONO `raw` fenced block → exit 1 (7 mismatches) = **4/4**; `--selftest` → 4/4 PASS asserting exit code **and** expected check-id (kagi `drift-pins.sh` convention per the connector survey; all 5 adoption recommendations adopted, `round10-fleet/INTEGRATOR-NOTES.md` §3). Post-move `find . \( -name '*.py' -o -name '*.sh' \) -not -path './.git/*' | wc -l` → **18** (the ≥12 half was already satisfied pre-move — see erratum F1). (b) **Failing-before evidence (calibration):** the *first* landed grader version (41777 B, 19:15) failed its own M0 control — a bogus `r9.onset.predicted_vs_observed` equality check treated the preregistered onset miss (5.0 predicted vs 5.8 observed) as a mismatch; caught by the independent harness (`r10-mutation-sh.md` §7.1), fixed 19:17:54 by replacing it with `r9.onset.prediction_preregistered` (observed mean is checked against `replication.md`'s stored 5.8 only). (c) **Adjudicated erratum pinned in the gate:** `replication.md` §Onset-and-failures stored state errors "12/32"; recomputation from committed bytes gives **24/32** (final passes 4+2+2+0 = 8/32, parse failures 0/32 — same figure re-derived independently by the critic's `recompute_r9.py`); §Errata appended to `replication.md` (append-only), `grader.py` `ERRATA` pins the (stored-defective, corrected) pair so editing either side without a ruling fails the gate; `replication.md` md5 pin moved `a70980a5f465da1bedd0ffa474a0c032` → `d9235e41f3ebfdcabd368c71cde878a1` (appendix-only change — recorded reason per the landing-bytes rule); "12" provenance (checkpoint 6+6 over all-cells denominator) labelled conjectural. (d) **Critic re-run of round-9 scorecard pointers: 35 claims → 30 REPRODUCE, 3 falsified**, all filed as `SCORECARD.md` §Round-10-errata: F1 runnable-count "0 → 11" was wrong at birth (12 at `2575be6` itself: `git ls-tree -r 2575be6 --name-only | grep -cE '\.(py|sh)$'` → 12; 0 at `f147a27` — the before-half was right); F2 `sha256sum -c corpus/evidence/round9-replication/predictions-r9.sha256.repo` exits 1 from the repo root (bare relative path inside; README documents the correct cwd — the scorecard cell was the one wrong statement; now hermetic inside `grader.py` as `r9.ordering.prediction_sha256`); F3 partial — the round-9 freshness row cited evidence md5s + recomputation language as being in LOG L14; md5s sit in L13 and `recomput*` has 0 hits in LOG.md (the recomputation lived in `round9-fleet/review.md` §4) — this entry carries the recomputation itself. (e) **Fleet: 10 L2s in one batched call** (3 scouts endpoint/wiki/bench @m_flash, critic/reviewer/connector/labrat/mutation-tester @m_zfl, executor/scribe @m_flash) → 22 files committed under `corpus/evidence/round10-fleet/` (11 artifacts verbatim + independent scripts + raw endpoint captures + `INTEGRATOR-NOTES.md`; corrections only in the notes file, round-9 convention). (f) **Freshness re-verification (this round's results):** endpoint `/v1/models` → `/scratch/models/qwen3-coder-30b/Qwen3-Coder-30B-A3B-Instruct-UD-IQ2_XXS.gguf`, `/health` → 200 (no drift since r4); **first process-level pin** — `llama-server` pid 1299, `/proc/1299/cmdline` == `~/.config/systemd/user/qwen-coder.service` ExecStart (41 tokens, EXACT_MATCH), closing PROVINCE's "documented from behaviour, never from the process cmdline" ceiling: `--parallel 2` (no literal `-np`), `--cont-batching`, `--ctx-size 16384`, `--kv-unified`, `--cache-type-k/v q4_0` (**4-bit KV cache — an unstated premise of every r8/r9 number**), `--flash-attn on`, `--no-context-shift`, `--n-gpu-layers 999`, custom non-upstream chat template (`--jinja --chat-template-file ~/.config/llama/qwen-coder-godspeed.jinja`) → recorded in `PROVINCE.md` served-model row + `SKILL.md` scope-limit paragraph; UNVERIFIED carried open: on-disk gguf vs `meta.size` Δ 5,973,152 B (no 10 GB hash run). bench-arena: frozen since 2026-08-29 (`find ~/bench-arena /tmp/bench-* -newermt '2026-09-28 18:00'` → empty); claims re-derived — task-09 0/17 + task-20 rows REPRODUCE exactly, the telemetry-NULL causal chain **DRIFTED** (real mechanism: `loop.sh:32` emits 5 comma fields into `:63`'s 6 read vars → `mok` always empty → `source=journal` unconditionally, 33/33 v2 rows; and `curl -fsS :8080/metrics` exits 0 today — HTTP 200 JVB openmetrics, 0 `prompt|eval` lines, so "the metrics scrape fails" is false now) → §Errata appended to `corpus/knowledge/bench-arena-fresh-run.md`; "97 label dirs" stale (125 graded/out, 128 `.sol`; dir still on disk contra "(ephemeral)") → §Errata appended to `corpus/knowledge/bench-arena-round7-noise-n25.md`; the `loop.sh` fix is in-lane backlog (operator rule: no mid-round patching of live surfaces), semantics reported to kumitate informational. llm-wiki: unchanged (last commit `e66e614` 2026-08-08; mtimes wholesale-touched 2026-09-20 → git is the freshness oracle); digest queue reclassified — the 3 queued sources are external (arXiv 2505.06120, arXiv 2307.13702, llama.cpp #7052), fetched-and-cited in `eval-prior-art-calibration.md`, zero-trace in llm-wiki; #7052 open/closed state contested between two round-10 fetches while the quoted content verifies verbatim → §Status note appended (discipline: cite issue content + fetch date, never state, without same-round re-fetch). Citations: 23/23 corpus URLs HTTP 200; resolution 91.2% strict / 98.0% repo-convention — the ≥90% rubric floor holds; 20 cited-source bullets reproduce at HEAD ("14 distinct paths" ruled convention-bound: 58 under the finer extractor, 57 resolve, 1 documented-absent). (g) **Docs landed:** `SKILL.md` 414 → 472 lines (§Hermetic grader, anti-pattern **14**, serving-stack pin paragraph; counts re-run: 2 decision tables, 14 anti-patterns, 20 bullets); `corpus/README.md` gate note + round10-fleet row; `PROVINCE.md` 9 surfaces (new In-repo-gate row) + round-10 report-outs (serving-plane config facts → integrator; loop.sh semantics → kumitate; operator read-only rule); `SHONEN.md` boxes 1/3/4 evidence lines updated (marks unchanged `[~] [~] [ ] [~]` — box 3 stays unmarked until a cold agent runs the checklist end-to-end); `SCORECARD.md` round-10 errata + post-move sections — **operability 4→6, calibration 6→7, freshness 5→6, coverage 6→7, depth 8→8 (held, anti-double-count ruling), adjacency 8→8 (held, no new arbitration), novelty 5→5 (hermetic round adds no construct)** — next move: novelty, powered granularity-ladder re-run with filed power analysis. (h) **Operator rule received mid-round (binding, complied):** domain source repos (ufo-fsd-alpha, bounties, webzites, llm-wiki) READ-ONLY — no commit/push there; only `VeigaPunk/shokunin` (report) and `VeigaPunk/kengaku-shokunin` (this repo; `git remote -v` verified pre-push); upstream-bound findings travel in `.ufo/reports/round-10/kengaku.md`. This entry lands in the round-10 commit (child of `1bd17ec`), first parent of the round-10 fleet dir.
- 2026-09-28 — round 11: **novelty axis-move** — powered, preregistered, prior-art-priced rerun of the emission-granularity ladder; closes the round-10 §Planned target. Evidence: (a) design hashed BEFORE any request — bundle `prereg-bundle.sha256` (probe_plan `d7fbeebe…`, power_analysis `ecfe96de…`, predictions `e912085c…`) at `ordering.log` pre/post-hash **23:10:20Z**; run scripts hashed post-fix **23:28:37Z** (probe_r11.py `cf754d78…`, run_r11.py `f012ab6e…`); first `request_ts` **23:28:57Z** (descriptors record). Design critic gate landed pre-run: **CLEAR-TO-RUN, 0 FATAL**, 1 conditional MAJOR (error-record contingency — vacuous, 0 errors) + 6 MINOR adjudicated as errata (power-table ceil: exact n=64.07, power 0.7996≈80% at n=64 stands; Φ(2.191)→2.192 typo; severity-error units pinned to nwrong-units; hashed bundle never edited in place). (b) design: cells `A-CKPT4710` {4,7,10} vs `A-CKPT710` {7,10} on the SAME 64 problems (pids 201–264, seeds `3000+pid*41`, disjointness + 64/64 generation proven pre-hash in `prereg-precheck.log`), paired per pid, counterbalanced by parity, filler before each cell; machinery byte-identical to r9 (`probe_r11.py` = `replicate.py` copy, only BASE/OUT env lines differ — diff-verified); ladder semantics verbatim `run_r9.py` incl. the post-checkpoint spillover ask; n=64 from the filed power analysis (r9 paired d=0.519 recomputed from committed bytes → shrunk MDE d=0.35 → n=64, two-sided α=0.05). (c) pre-run defect caught + failing-before preserved: `run_r11.py` lacked `import json` (LabratMock mock-server smoke, exit 1 NameError at first record, `py_compile` insufficient); fixed, mock re-smoke N=1 exit 0 census 24/24, fix hashed into ordering.log before launch. (d) main run: **1409 requests / 1473 records in 259.1 s**, census exactly per plan §4 (1 descriptors / 64 meta / 192+128 graded / 448+512 ack / 128 filler / **0 error**), finish=length 0/320, parse fails 0/320, SUMMARY `A-CKPT4710: 29/64` `A-CKPT710: 21/64`; landed byte-identical (`cmp` at copy; md5 `c42fe3d1…` jsonl, `281cb530…` run.log — both pinned in grader `PINS`). (e) result: paired severity diff **+0.352** (sd 0.820, n=64), t=+3.431, df=63, **p=0.0011**, CI [+0.147,+0.556]; exact sign 26W/7L/31T p=0.0013 (agrees → no downgrade); **PREREGISTERED VERDICT: ESTABLISHED**; McNemar b=13 c=5 p=0.0963 → pass-rate dose NOT established (honest null); prediction scoring: severity diff +0.350→+0.352 (abs err **0.002**), passes 15→29 (0.219) / 13→21 (0.125) — levels batch-variable on the unchanged pid-1299 stack, contrasts travel; first probabilistic forecasts scored: **Brier 0.153** (0.78→1, 0.50→1, 0.60→1). (f) L2 fleet: **12 agents — wave 1 = 9 in ONE batched call** (critic, 2 scouts, connector, reviewer, 2 executors, scribe, labrat; MISSION route buckets), wave 2 = 3 (critic-landed, mutation-tester, reviewer-index); all 17 artifacts committed under `corpus/evidence/round11-fleet/` + `INTEGRATOR-NOTES.md` (integration deltas: grader promoted by byte-exact slice assembly — 4 diff-verified slices; ONE deviation: draft's first-request-is-descriptors check over-strict at second-resolution ts, failed on real bytes, fixed to file-order primacy; selftest basename-collision fix). (g) gate extended in-round: `grader.py` 936→**1709** lines, 149→**280** checks, three trees; `--selftest` S0–S6 ALL PASS; independent mutation battery **11/11 killed** (incl. r9-only isolation + guarded in-place swaps md5-restored); stdout md5 `a98307a2…` identical under PYTHONHASHSEED unset/1/42/99. (h) novelty priced 7/7 with fetched URLs: C1 severity-dose INCREMENTAL-low (decoupling published — StageIF 2609.08589, 2605.30233; no density-manipulation source FOUND), C2 KNOWN/INCREMENTAL, **C3 instrument NOVEL (r9 ruling stands strengthened)**, C4 INCREMENTAL (2606.11217/2603.10044), M1–M3 method context (Miller 2411.00640; Bowyer 2503.01747 CLT-coverage zone → exact sign robustness kept; #7052 closed-stale class unfixed; PR #21038 q4_0-KV perturbation = common-mode, paired diff defensible). CriticLanded post-run: **10/10 REPRODUCE** (fresh implementation, 40/40 raw re-parse) + 4 wording findings applied PRE-COMMIT to this round's own files (search-set scoping, within-stack contrast wording, prior-art-context framing; C3 objection adjudicated partly valid — attribution sharpened, verdict stands). (i) re-verification: endpoint `/v1/models`+`/health` 200 at round start AND in-band at run time (descriptors: model id + pid 1299 + 41-token argv — durable committed-byte form of the r10 pin); ReviewerBaseline 41 pointers **GREEN** pre-landing; **route-telemetry surface went ABSENT mid-round** — `~/Projects/bounties/` resolved 23:32Z (aggregator box-3 cold run counted 7,226 live lines) and was gone minutes later, no relocation found; PROVINCE row marked, routed to kasegi (report-out 4), SKILL bullet annotated historical. Aggregator's non-author cold run of SKILL.md (`lessons/round-8-aggregator-box3-coldrun.md`, aggregator-committed `06cdc98`+`d8f2898`) verdicted box 3 **[x]** (20/20 read-only reproductions; gate ran cold exit 0); this lane indexed the lesson (13=13), closed breaks B1/B3/B4 in SKILL.md (B2 mooted by the ledger absence) and flipped SHONEN box 3 citing the artifact. (j) ledger: SCORECARD novelty **5→6** (axis-move), calibration 7→8, operability 6→7, depth 8→9, freshness 6→7, coverage held 7 (unresolvable-surface cap), adjacency held 8; README both-directions (knowledge 22=22, lessons 13=13, evidence 6=6); SKILL.md 472→**518** lines (anti-pattern 15, measurement rule 10, checklist item 1 extended, 23 cited-source bullets); new `knowledge/bench-arena-round11-power.md` + `lessons/round-11.md`; next move (§Planned): powered four-arm full ladder + per-problem Brier + second-task-family transport arm.
- 2026-09-28 — round 12 (evidence committed in round 14): **novelty axis-move** — powered, preregistered, prior-art-priced four-point emission-density ladder + batching/emission dissociation + second task family + per-problem forecasts. Evidence: 9-file bundle and run machinery hashed at `2026-09-29T01:16:08Z`, before first request `01:19:59Z`; design critic's DO-NOT-RUN (1 FATAL / 5 MAJOR / 4 MINOR) was fully absorbed pre-hash; contingency and measured 44/44 power floors are inside v1. Main run: **4,114 records / 4,002 HTTP calls / 701.6 s**, zero error records, 0/1,328 parse failures; results md5 `9dd8aa2…`, run log `700d1ddd…`. Mechanical verdicts from `analysis_r12.md`: Page `L=1773.0`, `z=+9.452` → `LADDER ESTABLISHED`; CKPT710−4710 `+0.297`, p=`0.0025`, sign 24/7/33 → `REPEATS-r11` + `POINT-MATCHES-r11`; MONO−CKPT10 `+0.656`, p=`0.0000` → `DISSOCIATION ESTABLISHED`; second-family SPARSE−DENSE `+0.177`, p=`0.2571` → `TRANSPORT DIRECTIONAL` at a 2/48-per-arm floor; 416 pass forecasts Brier `0.1288`, BSS `+0.0447`, slope `+0.8427`. Prior art prices C1/C2/C4/C5/C6 INCREMENTAL, C3 NOVEL-instrument. Sixteen L2s produced 22 fleet files; the scope audit discloses one bounded violation (two read-only endpoint metadata GETs by a scout). Landing caveats recorded rather than rewritten: prior-art transport says stale 448 instead of 416; stored E2 McNemar b/c orientation is transposed but unordered counts/p=`0.1435` stand; launch and first request share one-second timestamp so strict launch-before-request is unobservable; analysis regeneration differs by one absolute-path-casing line. `recompute_r12.py --selftest` → 165/165 PASS; the round-14 gate now replays and pins the tree.
- 2026-09-28 — round 13 (evidence committed in round 14): **ack-label prompt-intent audit; hermetic, no endpoint traffic**. `corpus/evidence/round13-ack-state/{audit_ack_schedule.py,analyze_ack_state.py}` re-derive intent from runner schedules instead of the `-ack` storage suffix (selftests 4/4 + 8/8 PASS). r11 CKPT710: 512 label rows but 384 true ack-only prompts; prefix `ok` 330/384 = 85.9%, bare `ok` 324/384 = 84.4%, versus misleading label-wide 330/512 = 64.5%. Eighteen of 384 were exact unsolicited states; 30 capped raws make exact-state incidence `[18,48]/384 = [0.047,0.125]`. r11 CKPT4710 similarly gives 220/256 prefix and 216/256 bare; r9 true ack rows were 100% bare. Round 13 itself was incomplete: no durable analysis, prior-art artifact, connector result, kotoba route, lesson, or LOG/SCORECARD/README landing (G1–G6); the scripts and these limitations land one round late and earn no novelty bump.
- 2026-09-29 — round 14: **novelty debt-landing + independent verification** — committed, indexed, logged, and scored the r12 ladder/fleet and r13 audit trees that had sat untracked; novelty **6→7** on the powered ordered-ladder + C3 instrument-new ruling, calibration held 8 because lateness violates the in-round contract. Nine L2s in one batch delivered `r14-{critic-landed,review-priorart,scout-surfaces,connector,mutation,revenger-r13,scribe-drafts,landing-gate}.md` plus the r12 knowledge/lesson drafts: independent critic 25/28 REPRODUCE, 3 PARTIAL, 0 FALSIFY; 14 fetched URLs all reproduced; 4/4 fresh mutations killed; round-13 numbers independently re-derived 9/9. L1 added the missing `analysis_r12.md` md5 pin (`029c3bcd…`): `python3 grader.py` → **733 checks, 0 mismatches**, exit 0; S0–S7 all pass. Index parity at close: knowledge **23/23**, lessons **17/17**, evidence dirs **10/10**. Freshness sweep: `/v1/models` id + `/health` match; pid 1299 owns `:34113`; 41/41 argv tokens EXACT_MATCH including q4_0 KV, `--kv-unified`, `--parallel 2`; bounty route tree still absent; `~/bench-arena` was falsified as live and found relocated intact at `~/archive/bench-arena` (0 files newer than 2026-09-28), so living pointers were corrected. Routed, not absorbed: ack-intent craft → kotoba; closeout carry-over gate → aggregator/protocol; no new serving-plane report-out. Evidence: `corpus/evidence/round14-fleet/`, `SCORECARD.md` round-12–14 table, `PROVINCE.md`.
- 2026-10-14 — round 15: **OMP/ufo-fsd re-census — drift does not reach this lane**. The substrate relocated (`~/Projects/origin-work/ufo-fsd-alpha` → `~/Projects/ufo-fsd-alpha`, HEAD `964f443e`, ~50 upstream files deleted); kengaku's gate replays only in-repo committed bytes, so no `--src` repair, no re-citation, no re-derivation was needed. Survey: `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS`, exit 0; `python3 grader.py --selftest` → `[selftest] ALL PASS` (S0–S7), exit 0. Failure classification (a/b/c/d): 0/0/0/0. Host sweep recorded two new operator-side ABSENTs — `~/Projects/origin-work/` gone (r14 scout's `origin-work/open-bug-bounties` mentions now historical, erratum appended in SCORECARD §round-15) and `:34113` served model down (`curl /health` → 000; `systemctl --user status qwen-coder.service` → could not be found) — carried debt named with unblock action (operator restores unit). Resolving: `~/Projects/ufo-fsd-alpha`, `~/archive/bench-arena`, `~/Projects/webzites/repos/llm-wiki`; still absent: `~/Projects/bounties/ledger/telemetry.jsonl`. No axis-move; SCORECARD §round-15 carries the full move-log row.

## 16 — re-census round (freshness axis-move)

2026-10-14 · steered round 16 · axis: freshness · 32-lane fleet wave + parent integration.

Full round detail: `corpus/lessons/round-16-recensus.md`. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/`.

## 17 — interactive attempt blocked at route admission

2026-10-15 · attempted axis: coverage · starting commit
`3f31e54c6e7aeddef13db11985b3c7a9dad9e0cf`.

- Reconciled round-16 LOG/SCORECARD history with the stopped worker's
  non-authoritative launch counter 13. Preserved inherited domain edits,
  `corpus/evidence/round13-coverage/` and its lesson unclaimed and uncommitted.
  Initial file hashes and exclusions: `.ufo/round-17/initial-state.json`.
  Native transcript/session bodies, credential material, raw journals and
  environment values were not read or committed.
- Wrote `plans/wwkd-round-17-coverage.md` before work. The exact 32-scope audit
  spec is `.ufo/round-17/wave/spec.json`; canonical validator `plan` and `run`
  each exited 0. Full outputs: `wave/plan-execution.json` and
  `wave/run-execution.json` beneath that round directory. All 32 rendered
  tasks have the leading Godspeed invocation; registry agent IDs are null.
- **Native dispatch count 0; no specialists running; integration blocked.**
  `cfg://task/agentModelOverrides` reports global defaults, not the requested
  role aliases: reviewer/connector `@m_mid`, critic `@m_strong`;
  `m_antigravity` has no `@m_zfl` fallback. The canonical existing mission
  overlay supplies no missing binding. Exact required/actual bindings and
  the concrete operator unblock: `.ufo/round-17/route-blocker.json`.
  No substitute route, new overlay or global configuration write.
- Parent's local gate: `python3 grader.py` exited 0,
  `CHECKS n=733 mismatches=0 errata_pinned=1`,
  `VERDICT: PASS — stored evidence fully re-derives offline`.
  `python3 grader.py --selftest` exited 0, S0–S7 PASS,
  `[selftest] ALL PASS`. Full commands/stdout/stderr/exit codes and measured
  dirty-tree boundary: `.ufo/round-17/gates.json`. Validator CLI invocation
  exercised the actual changed work surface (the saved wave); no software or
  domain changes were integrated. Previously reported UFO Phase-0/self-iter
  failures were not rerun.
- Every axis and all three learning trends are **unchanged** in SCORECARD's
  round-17 record. This is blocked/non-admitted work: **zero verified-round
  credit**, no native judgment, no promotion, no outside spot-check, no
  source-restoration claim. `corpus/QUALITY.md` remains absent named debt.
  The inherited nine-seat dispatch is not relabelled a 32-seat execution.
- Only this attempt's explicit record paths are eligible for local lane-
  identity commits; inherited SCORECARD edits are excluded from staging.
  No push. Report, receipt applicability and a fresh-session continuation
  handoff are published under `.ufo/round-17/`; no Sighting completion without
  an applicable minted and validated receipt.

### Round-17 blocked-attempt delivery

Owned record work landed in
`85de57175f09d64a34b747fdb1039f68fdaf6e22` under the lane identity.
Report path: `.ufo/reports/round-17/kengaku.md`; sidecars and the fresh-session
handoff remain in `.ufo/round-17/`. This clarifies the preceding shorthand
"report ... under .ufo/round-17/" and the same shorthand in SCORECARD: the
report itself uses the canonical lane-local `.ufo/reports/round-17/` path.
The report cites the existing work commit and is committed afterward, without
amending it. No inherited domain change is claimed or swept.

## 18 — kimi secondary-model routing round: digest landing

2026-10-15 · digest landing (no axis-move claimed) · source: parent-fleet
round 18, six merged missions.

The parent repo (`../`) executed round 18 on 2026-10-15 — census (M1),
definitions audit (M2), n=2 TTFT/TPS battery over the live 17-entry
`[secondary_model.models]` pool (M3), codex fast-mode probe (M5),
opencode-go/deepseek-v4.1-flash probe (M6), routing table + apply guide +
fleet report (M4). This lane lands the digest; the bytes stay in the parent
repo.

- `corpus/knowledge/kimi-model-routing-round18.md` — digest: operator
  directives (test new models/providers, TTFT/TPS headline, the assigned
  17-model pool, codex fast mode, the opencode-go gap, the lane-policy
  revision), headline TTFT/TPS/pass table (17 M3 rows + the M6 row), key
  defects (token-plan keys 2/3 quota-dead until 10-23/10-28 16:00Z; dead
  client fields `off_effort`/`max_input_size`; unclamped global effort
  override; `reasoning_key` DEF-9/DEF-10; 42 of 143 entries on unservable
  lanes at audit time), routing outcome (13 entries: 11 retained incl. 2
  demoted, 4 quarantined, 2 dropped, 2 verify-first; opencode-go reserved
  for `deepseek-v4.1-flash` only; glm-5.3-flash zai-primary →
  devin-secondary; codex fast mode accepted-not-confirmed no-go + conditional
  protocol), and parent-repo pointers with merge commits.
- `corpus/evidence/round18-kimi-routing/README.md` — index of the six parent
  artifact trees: contents, file counts (`find` re-counted: census 68,
  definitions 25, battery 402, battery-opencode 44, fastmode 14, routing 6)
  and hygiene-gate results (all six 0 hits / exit 0).
- `corpus/README.md` — two index rows added (knowledge + evidence), staged
  with the inherited round-17 hunks excluded (index entry built as HEAD + the
  two rows only; verified with `git diff --cached` before commit). Index
  parity at close: knowledge 24/24, evidence 11/11.
- `LOG.md` — this entry.

Source verification (2026-10-15): merges present in
`git -C ../ log --oneline` — M1 `4738fee`, M2 `7e2c473`, M3 `c2174a5`,
M5 `db82042`, M6 `bd0c690`, M4 `fbae972`; `diff -q`
`../.ufo/reports/round-18/kengaku.md`
`research/round-18-kimi-model-routing/routing/kengaku-round18-report.md` →
identical (exit 0); report committed at `389ede4`. **Number note:** the
round brief said "41 of 143" for unservable lanes; the artifacts say **42**
(`definitions/ANALYSIS.md:394`, `routing/kengaku-round18-report.md` §3 —
4 `managed:kimi-code` + 19 `alibaba-token-plan-2` + 19
`alibaba-token-plan-3`); the artifact figure landed. No SCORECARD change
(inherited WIP there left untouched); no axis-move claimed.

The inherited round-17 WIP (modified SKILL/SCORECARD/SHONEN/corpus README and
knowledge entries; untracked round13-coverage tree/lesson/interactive
sessions) was not staged or committed; the only change made inside an
inherited-dirty file is the two appended `corpus/README.md` index rows, and
only those rows were staged.

## Round 19 — probe battery (goal wave; operator stopped the run here)

**Round 19 (2026-10-16).** Motivating evidence: calibration proxy
intermittency (r8-r11 0/1, 1/1, 0/0, 1/1); no standing battery. Landed
(evidence commit `0671bb0`): frozen 9-probe battery (FROZEN 07:55:58Z
`e1a86777…`), 5 executed + 15 receipts, scored at close in-round (mean Brier
0.1836/11; seat pool 0.0617/26), reusable template, note. Corrections folded:
BR-1 freeze TOCTOU breached-and-repaired (re-freeze after stability check;
stale-window runs adjudicated unaffected); runner-leg-opencode DEFECT-0
(pre-battery requests, self-filed, excluded); bookkeeping defects recorded;
premise correction — operator reordered both cascades post-r18, P4/P5
re-based pre-freeze. The operator cancelled the 10-round goal after this
round; rounds 20-28 do not run. Wave: 32 seats, zai flash bucket per the
operator routing directive.

**Boundaries held.** Small probes only; credentials untouched; corpus
sources cited; seats committed nothing; parent integrated under the kengaku
lane identity.

## Round 20 — battery grid closure (goal wave)

**Round 20 (2026-10-16).** Motivating evidence: r19 left P2/P3/P8/P9 UNRUN.
Landed (evidence commit `af0e3e6`): all four executed (9 requests, zero
retries, freeze-verified against `e1a86777…`), grid 9/9, combined mean Brier
0.0998/46; **3c falsified** (used-percent 7 > frozen <=2 — route-state drift,
a miss by design). Template guard + grid-closure lesson landed. Novelty scout
priced the latency-fingerprint example out of novelty (crowded prior art) and
proposed three r21 candidates; N1 (blind cascade-leg attribution with shim-
journal ground truth) registered for r21. Wave: 32 seats, zai flash.

## Round 21 — blind leg attribution (goal wave)

**Round 21 (2026-10-16).** Motivating evidence: the r20 scout's N1 candidate
(latency fingerprinting priced out of novelty — crowded prior art). Landed
(evidence commit `0d23c61`): `plans/attrib_probe.py` + frozen feature table
(`9f0244bb…`, freeze-before-trials, journal GT read only post-trials) — 100%
accuracy on both shims (ds 20/20; glm 22/22 with natural zai/devin diversity),
11/11 ablations, 3 matcher defects fixed pre-adjudication and recorded; prior-
art note scopes the novelty as instrument+GT-protocol; critic's adjacency pass
answered in-note. One seat (scorer) failed; its remit covered by the
instrument's adjudicated scoring + an independent recount — named. Round-20
evidence backfill `96b8962` (a git-add pathspec error had left the scorer's
§10 + template + lesson uncommitted — honest repair, content timestamps prove
r20 provenance). r22 registered: attribution coverage of the untested legs
(hyper/opencode-go) + a battery-fold (attrib as a standing probe type).
Wave: 32 seats, zai flash.

## Round 22 — forced-fallback coverage (goal wave)

**Round 22 (2026-10-16).** Motivating evidence: r21's UNTESTED hyper/
opencode-go legs. Landed (evidence commit `8a08483`): instrument v2 with
leg-forcing (content-inspection bait reliably cascades to hyper: run-2 10/10
= 1.000 PASS); opencode-go 0 on-target — the echo-marker bait starves vs
reasoning models (named gap; mechanism proven reachable via T03); v2 table
three-pin freeze (one defective pin superseded pre-request); battery probe-
type P10 fold; critic's forced-vs-natural limit named. 4 seats lost to
provider empty responses (scorer/reviewer/scribe/determinism) — scoring
covered by the instrument's authoritative blocks + ablation seat; the attrib
note's r22 addendum was integrator-written. OPERATOR ROUTING: after this wave
the operator switched the swarm fleet back to the deepseek bucket (zai
parked) — r23 dispatches on `cascade/deepseek-v4.1-flash`. r23 registered:
opencode-go forcing via the stream-path header leg-selection.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

Operator rollout of the 2026-10-16 fleet protocol amendment (fleet-root commit `84bade0`), adopting the `AXES.md` §SCORECARD.md contract fields additively.
Fields already present as real sections before this change: the axes score tables, `## Planned (next axis-move)`, `## Retired`.
Fields added by this rollout: `## Capabilities` (empty repertoire-table scaffold; rows enter only via a round that demonstrates the capability running) and `## Saturation` (saturation line + stagnation window N deferred to the lane's next round per `AXES.md` §The stagnation nudge).
No axis claim was made and no score moved; no verdict was changed.


## Round 23 — stream-path leg forcing (executed 2026-10-16; NOT-ADMITTED, recorded round 24)

**Round 23 (2026-10-16, recorded 2026-10-19 in round 24).** Registered at r22
close as "opencode-go forcing via the stream-path header leg-selection"
(`SCORECARD.md` §Round 22). Executed: v3 table `plans/attrib-r23-frozen.md:214`
`FROZEN: 2026-10-16T13:45:47Z sha256:1b2d6a01…`; 30 stream trials scored in
`corpus/evidence/attrib-r23-stream.log` — `:233` `GT counts: {"alibaba-token-plan": 6, "hyper": 24}`,
`:234` `ACCURACY: 30/30 = 1.000 … -> PASS`, `:239` `STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL`.
The round's one claim was the opencode-go coverage clause; it failed. The
dispatch then aborted: WIP commits `a2ff634` / `f9337d5` / `6f31d23` (2026-10-16
11:22–11:25 -0300) carry the instrument draft, receipts and v3 table, each
self-labelled unverified; drafts under `.ufo/rounds/round-23/goal-wave/` still
hold 17 `[PARENT:` slots (1 + 6 + 10). No LOG, SCORECARD, index row or report
was written until now.

**Disposition: NOT-ADMITTED.** `AXES.md`: "A round is admitted only if every
claim verifies"; the coverage clause did not. The attribution accuracy
(30/30) stands as a characterization of the stream path, not as coverage.
The gap stays named: opencode-go has 0 on-target GT trials across r21–r23.
No score moves for r23. The late record does not buy calibration credit
(rubric clause (d), round-14 precedent). Mining of this miss:
`corpus/lessons/round-24.md` (M13, M14). No re-run in round 24.

## Round 24 — sources registry + sourced expansion; learning from the lane's own mistakes (kaika, 2026-10-19)

**Round 24 (2026-10-19, kaika campaign, steered).** Lowest axis: coverage 7,
tied with novelty 7; tie-break to coverage because a novelty +1 needs a new
probe and none runs; no stagnation waiver. Motivating evidence: W1 STATE
dossier §4–§5 (18 mined mistakes, D01–D19 contract defects; round 23 executed
but never recorded) and W1 ART dossier (19 leads on contamination, judge
calibration, saturation, agentic horizon, paired uncertainty; `QUALITY.md`
absent, so nothing could be admitted). Pre-registered claims:
`plans/round-24-claims.md` (+ Amendment 1 after the reviewer/critic seats).

Landed: `corpus/QUALITY.md` (admission bar Q1–Q8, written before any
admission; round-closure criteria R1–R10 from the mined mistakes);
`corpus/SOURCES.md` (25 rows re-opened today, `A=24 C=1`,
`mined=18 queued=5 rejected=2`, contract census clean; receipts with quotes and
sha256 in `corpus/evidence/round24-sources/gate.md`); five knowledge entries
on uncovered ground, each opening with the source/verified-at/recheck triad;
index parity both directions (knowledge 3→0 unindexed, lessons 5→0, root
logs 0/28→28/28, plans 0/8→10/10, dead rows 0); `## Frontier` (5) and five
coverage-map rows in `corpus/README.md`; `PROVINCE.md` §Province map round 24
(Core/Frontier/Adjacent/Historical, every surface re-verified by `test -e` /
`ss` / `sha256sum`); `corpus/lessons/round-24.md` (20 mistakes, classes,
round-23 disposition, `## Gate`); SCORECARD round-24 section (re-derived axis
table, capabilities ×3, saturation line 8 / window 4, D14 errata, planned
round 25); the Round 23 NOT-ADMITTED record above.

Verdicts (self, pending non-author verification): C1 coverage 7 → 7 held by
the unresolvable-surface cap (critic's binding ruling), counts improved,
capability `sources-registry` entered; C2 calibration 8 → 8 held, counts
improved (`scorecard_state_defects_open` 6/6 → 0/6), critic dissent recorded.
Re-verification: `python3 grader.py` → `CHECKS n=733 mismatches=0
errata_pinned=1` PASS; `attrib_probe.py freeze-check` on the v3 table → OK;
shim sha256 `42d86d99…` matches the pin; `:34113` no listener. Provider
exhaustion: the first executor seats for KnowledgeB and SourcesRegistry
stalled on a rate-limited route and were re-dispatched (KnowledgeB twice; one
re-spawn failed `turn_rate_limit_exceeded`). Census: `sh plans/round24_census.sh`;
receipts `corpus/evidence/round24-census/{base-99cf615,after}.txt`.

## 2026-10-17 — README: Devin wiki link

- Operator directive (2026-10-17): insert the Devin wiki link into the README header of every repository with a generated wiki.
- Change: `README.md` created (lane-header convention) with a `**Wiki:**` link to https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/kengaku-shokunin?branch=master.
- Evidence: the org's Devin wiki index lists this repo's generated wiki; sibling lane READMEs carry the same `**Wiki:**` header.
- Documentation-only change; no round run, no axis moved, no verdict changed.

## Round 25 — interval-calibrated attribution verdicts; current-state assertions re-derived (hyaku, 2026-10-20)

- Lowest axis: novelty 7, tied with coverage 7; tie-break: coverage is capped pending the operator's coverage-cap ruling, so
  novelty carries the lowest-axis claim; no stagnation waiver. Base `6180e4f`; pre-registration `plans/round-25-claims.md`
  (`3f371d2`, Amendment 1 `710409f`, both before instrument output).
- C1 (novelty → coverage/constructs): `plans/attrib_calibration.py` re-derives all 119 stored lines of the 10 score blocks in the
  nine sha256-pinned r21–r23 receipts (0 mismatches) and re-verdicts the 4 unique samples (92/92 correct) under exact CP95:
  overall PASS holds; r22 `TARGET hyper 10/10 -> PASS` → INDETERMINATE (lower 0.691503, needs n=17); two `0/0 -> FAIL` → UNTESTED.
  Independent sh+awk parser `plans/fixtures/r25/attrib_oracle.sh` agrees. Knowledge entry
  `corpus/knowledge/attribution-interval-calibration.md` on new rows S027–S037 (receipts `corpus/evidence/round25-sources/gate.md`).
- C2 (calibration): `plans/state_check.py` on frozen P2 — base `6180e4f` `mismatch=11` (exit 1) → landed tree `mismatch=0
  superseded=1` (exit 0). Closed by: SHONEN regenerated to canonical pointer form (D17), dated ABSENT markers on five PROVINCE
  surface rows, the round-24 spot-check lesson indexed, SCORECARD R25-E1 (registry counts re-derived on S001–S026).
- Also landed: SKILL frontmatter carries quoted triggers, an anti-trigger and a sibling-arbitration note and now parses as YAML
  (D18); SKILL measurement rule 14; QUALITY Q11, R11–R13; corrections appended for kaika W3 F4 residual, F5, F6, F7 (S036), F10,
  F11, F12 and the disputed M19; `plans/l0_filed_check.sh` red on round 24 (3 unfiled L0) → those questions re-filed.
- Re-verification (freshness line): `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`, exit 0; `freeze-check
  --frozen plans/attrib-r23-frozen.md` → `stable=True -> OK`; `scripts/sources-census.sh validate --root … kengaku` → `kengaku ok`
  at round start and end; S011 re-opened (PDF sha256 `c1645e31…`), eq. (5) is the Rogan–Gladen form.
- Swarm: wave 1 build 92 seats (one validated task call); wave 2 falsify recorded in the round report. Seat misroots (3) moved into
  the lane byte-exact and logged as M29.

### Round 25 falsify-wave revision (appended 2026-10-20 ~23:25 -03; the entry above stays as landed in `8ea41f9`)

- Wave 2 (87 seats, one validated task call, `.ufo/waves/round-25/falsify/`) attacked the landed tip. Breaks fixed by
  appended corrections and instrument changes (`plans/round-25-claims.md` Amendment 2, disclosed as post-output):
  five vacuous specificity PASSes now carry no verdict (PASS 12 → 7); the share bound was conditional (`rg_cond`) and is
  vacuous with its sampling arm (`rg90`); boundary/RG/Wilson/CP/dedup selftest anchors killed the surviving mutants
  (selftest 18/18); C2's P2d now follows the registered endpoint rule (base 10 mismatches, v2 receipt — the entry above
  says 11 and stays as written), supersession requires a full-census restatement, the base id set is checked;
  `l0_filed_check.sh` no longer counts prose mentions.
- Novelty +1 withdrawn: the construct is published as tooling (cigate 0.2.0, S041). C1 records an observable move with
  the score held at 7; C2 likewise holds calibration at 8.
- The one PASS→INDETERMINATE re-verdict (r22 TARGET hyper) is population-dependent: PASS under the receipt's own
  both-blocks reading (19/19) or with the r22 pair counted as two runs (20/20).
- Two of the three round-24 report-only L0 questions were re-filed (coverage cap, novelty conversion); the third (C2
  admission) had been ruled by the round-24 closure and was not re-filed — the entry above says "those questions".
- Re-verification: `python3 plans/attrib_calibration.py --summary` exit 0 (TOTAL `PASS=7 … mismatches=0`); `--selftest`
  18/18; `python3 plans/state_check.py --summary` exit 0 (`mismatch=0 superseded=1`), `--selftest` ALL PASS.

## Round 26 — repair-first, then grader perturbations and frozen self-assertions (2026-10-21)

Lowest axis: novelty 7 tied with coverage 7; tie-break coverage remains capped by the open L0; no stagnation
waiver. Claims: C1 novelty (mapped coverage/constructs), finite-corpus grader perturbation audit; C2 calibration,
content-pinned P3 self-assertions. Pre-registration `e0037a8`; Amendment 1 explicitly post-wave-output.

- Repair-first integration: SCORECARD R26-E1/E2 supersede capability cells' 14 checks / mismatch=11 with
  18 checks / mismatch=10; PROVINCE R26-E3a/b supersede 25/37 with the dated S001–S042 census 42.
  `corpus/lessons/round-26.md` M39/R26-E4 corrects round-25's future-dated Gate evidence; Q13 and
  `plans/gate_timing_check.py` add a failure-capable structural support check. Round 25 remains rejected.
- Q13 red-before: `--lesson corpus/lessons/round-25.md --commit 8ea41f9` exits 1 (generic seat reference,
  no named report; receipt `corpus/evidence/round26-calibration/gate-timing-red-before.txt`). Timing additionally
  rests on commit-tree absence, not mutable report mtimes.
- Build wave: 72 returned reports, no replacements; three 72-seat refusal attempts before unchanged
  successful dispatch. Frozen planner L1; roles and actual ids in `.ufo/waves/round-26/build/swarm-registry.json`.
- Sources opened/curated S043–S047; S045 evalmut establishes direct tooling prior art, so novelty stays 7.
  S047 supersedes S037's stale 14-check teaching. Source receipts `corpus/evidence/round26-sources/gate.md`.
- Re-verification at round start: `grader.py` 733 checks, 0 mismatches; v2 state check 235 assertions,
  mismatch=0 on its frozen P2 (round-25 additions outside); sources census exit 0, 42 rows, one W04 warning.
  End-of-round measurement and final evidence follow as appended entries after the falsify wave.

### Round 26 — recovery and admission packaging (2026-10-21)

- Replacement L1 KengakuR26 resumes the same held attempt, inheriting remote branch tip
  `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`. Reused the pre-registration, repair-first integration,
  two validated dispatched waves, returned reviews, source corrections and patched instruments;
  no dead seat was replaced and no wave was replayed. Recovery ownership/census/misroot record:
  `corpus/evidence/round26-calibration/recovery-start.txt`.
- Falsify findings were resolved before the knowledge entry's admission: S048 supersedes S043's
  page location; Q14 narrows Q13's qualifying roles and declared-writer handling; explicit branch
  controls strengthen the perturbation and P3 selftests. Supporting findings and dispositions:
  `corpus/lessons/round-26.md` M45–M52 and `.ufo/waves/round-26/falsify/`.
- Discarded only inherited throwaway `plans/state_check.cover` (already removed by the earlier L1);
  retained the superseded pretrim registry as evidence, never as active assignments. No inherited
  operator/aggregator/outside-verifier file was edited. Round-25 rejection remains unchanged.
- The final 64-seat wave has eleven recorded provider-capacity deaths, not replacements:
  `.ufo/waves/round-26/falsify-dead-seats.json`. Three additional bounded read-only recovery seats
  inspect timing, evidence inventory and wave accounting; they are author-lane advice, not outside
  non-author spot-checks. L1 remains the planner and final measurement owner.

### Round 26 — required final measurements before admission

- Integrated the previously unlanded final state-check tail, SHA-256 `32a684ffcb3fb222b0360333f83c2e4654c19ec1c3ad6ed47016052401428089`;
  `recovery/K26IntegrateStateTail.txt` records the reviewed delta and two zero-start job-cap refusals.
- `python3 plans/grader_perturb.py --summary` reports population1964, exclusions0, audited15168,
  interval families9, policy checks909; independent oracle agrees, synthetic cases278 fail0,
  selftest catches12 mutants (`corpus/evidence/round26-calibration/*final.txt`).
- `python3 plans/state_check.py --summary` v3 on frozen `f11bffbf` reports278 assertions,5 mismatches;
  repaired tree reports278 assertions,0 mismatches,5 superseded,3 offline-unverifiable. P2's full
  keyed assertion projection is unchanged; paired S048-source addition leaves P3b records unchanged.
- Independent P3 oracle summary exits0 (63 registered,58 match,4 superseded,1 unverified);
  its inherited selftest first failed three controls because valid corrections leaked into scratch
  fixtures. The isolated fixture fix yields14/14, with both red and green receipts retained (M54).
- Two-direction separability is UNCHANGED (C1 FAMILY/TOTAL records and C2 summary/exit);
  `grader.py` retains733 checks,0 mismatches; Q13 selftest is green and r25 admission red reproduces.
  Prospective scratch-commit Q13 passes with three returned qualifying readers before actual admission;
  actual-commit measurement follows. Receipts are author-observed, never non-author closure.

### Round 26 — measured admission revision and close

- Admission package landed/pushed **`d4dfdb016c45a332d308898511e3964655629cc5`** through the lane helper.
  Entry, index, new coverage row, returned readers and the Gate admit landed in that same tree.
  Actual-commit Q13 exits0 (one admit, zero support failures, three qualifying cited reports).
- Clean-revision `sh plans/round26_census.sh` re-measures C1 audited15168 / families9 / policy909
  and C2 assertions278 / mismatch0 / superseded5, both exit0; SOURCES48, malformed0,
  knowledge/index34/34. Source-validator exit0 retains two W04 cross-scope duplicate-URL warnings.
  Pointers: `corpus/evidence/round26-calibration/{round26-census-after,gate-timing-actual-commit,sources-census-final}.txt`.
- Broad preservation census compares all base knowledge bytes and old source rows unchanged,
  and finds zero deleted/replaced base lines in LOG/SCORECARD/PROVINCE/SKILL/QUALITY/README
  (`preservation-and-source-census.json`). No owned axis score falls.
- Self trends: expansion improved (new covered finite-corpus grader construct), quality improved
  (replayed/pinned evidence and routed assertion repairs; gate-timing fix red/green), discernment improved
  (outside r25 disagreement mined into grounded Q13/Q14). Outside round26 admit/reject spot-check remains
  the orchestrator's duty; no author-lane reviewer is claimed independent. Round25 remains rejected.
- Report will cite this measured revision and the subsequent receipt/bookkeeping commit; existing L0
  coverage-cap and novelty-conversion questions remain open, with no new operator decision needed.

## Round 27 — extraction-policy comparison and frozen P4 (2026-10-21)

Lowest axis: legacy novelty7 → canonical coverage/constructs, tied coverage7 capped; no waiver.
Declared C1: fixed-response extraction-policy comparison; C2: calibration8 frozen P4 assertions. Both
score-held observables, not two claims on one axis. Pre-registration11a7fc8 precedes the82-seat build.
Round26 outside admission and its no-new-r26-assertions limitation motivate C2; four outside spotchecks
agree, so no new disagreement is invented (`corpus/lessons/round-27.md`; fleet r26 closure evidence).

C1 instrument absent at b5719440 →15712 paired verdict comparisons,1089 disagreement events over five
policies; baseline1964/1964 reproduces. E1/E3/E7 each17PF, E4 1012PF, E5 26PF; all FP0. MULTI14/31
and the75pp r8 B-clean-hint shift prevent a reassuring pooled-only interpretation. Prior art xFinder/
harness choices already covers the method in kind: novelty7 held. Draft remains unadmitted pending Q10/Q13.
Commands: `python3 plans/parser_policy_compare.py --summary`; base absence receipt
`corpus/evidence/round27-calibration/round-start.txt`; output build/ExecPolicyCore.md.

Eight tierA sources S049–S056 opened before registry insertion; lesson Gate records URLs/date/located
quotes and the narrow policy mapping. No MCQ regex is claimed an exact JSON-policy implementation.
M55 mines the commit-tree→working-copy surviving mutant; M56/M57/M58 expose schema/separability/
supersession-disclosure pitfalls. Repairs need actual red/green receipts, not green-exit assertions.

Wave1:82 seats,19 provider deaths unreplaced (six connector quota failures, thirteen Haiku429s). Partial
reports remain evidence, not successful completion. All seat-owned retained reports are committed.
L1 is integration owner; private seat clones are not production edits. Reverification touched only the
pinned offline response population, source openings and r26 assertions, never the absent model endpoint.

### Round27 — corrected package and returned falsification

- Build package `eeec929522aafde704333ab7b01a09a9fdf6e3b0` and frozen falsification candidate
  `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` landed through jj-lane. The candidate stayed outside corpus.
- Falsify64 (reviewer29/mutation14/scout11/critic5/executor2/sentinel1/connector1/simplifier1) produced
  43 completed original returns,21 provider deaths unreplaced, plus3 failed partial reports retained.
  One later S050 follow-up failed; existing FEntryNumbers independently performed the complete corrected
  source/number/contract reread and closed PARTIAL. No dispatched reader is called outside verification.
- Genuine red controls forced E6 last-fence coverage (59 cases/10 mutants), P4 comparisons/denominators/
  supersession/disclosure and historical authority, and Gate tree traversal/temp-write/--repo isolation.
  QUALITY Q15/Q16 and lesson M55–M63 preserve failures and correction evidence. Earlier source-reason/
  anchor rows stay as history; S058/S059 supersede them before admission.
- C2 final observable0→51 frozen assertion/disclosure IDs; score8 held. Base/final both0 mismatches,
  with score/adjacent-numeric limits explicitly offline-unverifiable (whole summary329/318/0/6/5).
  P2/P3 keyed298 records preserved; the failed “base mismatch≥1” forecast is not relabeled true.
- C1 remains15712 comparisons/1089 events; score7 held. Independent full numeric replay is retained at
  `plans/fixtures/r27/independent_policy_recheck.py` (only root binding relocated); all old knowledge/
  grader/input bytes remain unchanged. Candidate source/number rereads precede its admitting commit.
- Sources final additions S049–S060:12 (11A/1B), including the opened/rejected json-repair policy lead.
  Ten used-by changes are logged old→new in the lesson. Corpus knowledge/index moves34/34→35/35 with
  entry+index+coverage row together. Final exact command outputs/actual admitting revision follow below.

### Round27 — exercised final suite before packaging

Main's final integrated suite ran17 commands; each exit matched its declared0/1/2 contract.
`corpus/evidence/round27-calibration/final-suite.json` retains commands/stdout/stderr/exits:
C1 total15712/1089/five policies,59 hand cases/10 mutants; separately implemented full replay matches
all structures including9×9 matrix; C2 final/base329/318/0/6/5;5/5 independent class mutants red;
P2/P3 all298 keyed records equal; Gate three mutation controls and requested-repo isolation green;
grader733 checks/0 mismatches. Usage/missing-root failures are expected controls, not suppressed errors.

Broad preservation: all34 old knowledge files,48 old source rows and original grader/audit/interval
bytes unchanged; all base lines of six core docs remain in order. Bidirectional revert counters are
unchanged (C1 entire summary, C2 checked summary and all51 P4 id/verdicts). Properly changing new-artifact
OUT_OF_POPULATION disclosures is not counted as a checked-population change.
Receipts: `preservation-final.json`, `separability-final.json`.
Prospective sandbox admission passes1/1,46 report files in tree (includes failed-seat partials, not46
successful reviews); canonical candidate and exact two qualifying returned readers present. Sandbox
hash is explicitly not a landed hash. Actual admitting revision and clean-revision census follow.

### Round27 — actual admitting revision

Landed/pushed **6356b0bab78ee9292b7c9e112e6a414d3679dd6c** admits the byte-exact reviewed entry,
its index/coverage row and returned support together. Actual Q13 exits0: admissions1/passed1/failed0;
46 report files includes43 completed original returns and3 failed partials, never46 successful readers.
Actual byte proof equals the verified prospective code/candidate. Source census60/malformed0 and
knowledge/index35/35; actual counters C1=15712/1089/five policies, C2=329/318/0/6/5, both exit0.

Final census exposed M64: its P4a–e-only selector printed50 while JSON's full P4 inventory has51,
including the population control. Changed only that selector to include `P4.population`; retained
original50 receipt and red1 comparison, then repaired51/green0 (`census-selector-{red,green}.txt`).
This corrects report units, not the checked population or metric result. Final bookkeeping/census
revision is recorded in the scorecard/report; all actual checks remain in round27 evidence.
