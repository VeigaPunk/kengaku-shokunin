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

## Round 28 — WebArena task-spec observability and bounded reference consistency (2026-10-21)

Lowest axis legacy novelty7 mapped to canonical coverage/constructs, tied capped coverage/surfaces7;
tie-break new task-spec ground, no stagnation waiver. C1 static WebArena snapshot audit and C2 calibration8
literal-reference check are causally separate; scores held. Base b9b24796277020d1b9b01923b45313d6a565e664;
preregistration f0ba09be0f3066daba2134b943d973ad1588f34a, followed by disclosed Amendment1.

- C1: absent instrument→812 structurally inventoried tasks/812 distinct IDs, five evaluator-type sets,
  27 site/evaluator strata,16 separately source-audited deterministic cases,651 page targets.
  `python3 plans/benchmark_spec_audit.py --summary` exit0; selftest21 cases exit0. Not task validity,
  model ability, contamination freedom, paper-era release, WebArena-Verified or method novelty.
  Sources S061–S063 opened before registry addition; canonical knowledge remains deferred outside corpus.
  Evidence: corpus/evidence/round28-calibration/audit-summary.txt; build-acceptance/audit-current.stdout;
  .ufo/waves/round-28/build/Task*.md and OpenTasks/OpenScorer/OpenHelpers.md.
- C2: frozen13 source rows over35 baseline knowledge paths,12 literal row-file links in2 files;
  same delivered checker on baseline export finds2 source rows mismatched (S038 andS050), final0.
  Baseline+S050-only correction remains red onS038; adding onlyS038 status/used-by yields green0.
  Sources reopened first. S050 addition indexes a corrective mention, explicitly reverses round27's
  lesson-only indexing, never restores its superseded blanket reason. F5 misses.
  Evidence: corpus/evidence/round28-calibration/build-acceptance/registry-only-delta.json and
  registry-{baseline-red,s050-only-red,s038-only-delta-green}.stdout; registry-summary.txt.
- Build64 seats returned59, provider deaths5, never replaced; L1 authored missing code/prose with actual
  writer identity. Alternate oracles are independent logic, not independent authorship.
  Specs/dispatch/registry/attempts/deaths: .ufo/waves/round-28/. First whole-batch refusal spawned none;
  unchanged retry after180s succeeded. Unused isolated writer clones were removed after all3 writers died.
- Main acceptance's11 command stages had expected exits; its initial final assertion was overbroad:
  it rejected two newly disclosed OUT_OF_POPULATION records while all355 existing IDs and all329
  checked verdicts remained unchanged. Red receipt and exact delta retained; corrected invariant applies
  to unchanged captured output, not a duplicate state-check run. Checked tuple remains329/318/0/6/5;
  original26 outside IDs retained plus2 new disclosures, not a hidden new checked population.
  Evidence: build-acceptance-run.txt, build-preservation-delta.json, build-preservation-corrected.json.
- Calibration-source errata append (not rewrite): S049 header27 corrects erroneous round27 reviewer25;
  S064 clarifies minimum closing-fence length; S065 supplies Python-side numeric-extension authority;
  S066 limits exact test inversion to known diagnostic properties. Historical numeric probe results and
  state_check.py remain unchanged. Sources/lesson record every mutable-cell old→new.

Build measurements grade the prospective working tree, not falsely the detached Git HEAD. Fresh falsifiers
will re-open source rows, independently replay final counts, attack code/gates and read the byte-frozen
candidate before actual admission. Outside non-author closure remains separate from lane-dispatched advice.

### Round28 — falsification-driven repairs and measured fixed package

Wave2 returned64/64, dead0; total128 seats,5 build deaths,0 replacements. Distinct task/source/metric/
schema/mutation attacks are preserved under `.ufo/waves/round-28/falsify/`, not treated as approval votes.

- C1 now parses the same retained bytes it authenticated; raw/presence/effective URL-note fields and
  invalid projections are explicit. New source-proof shapes, precedence and race controls take the
  observed selftest21→67, exit0. C2's unconditional frozen-row-presence control and outside-row exclusion
  take12→15, exit0. These are instrument repairs, not new model trials or new benchmark-invalidity counts.
- `python3 plans/fixtures/r28/acceptance.py --root . --out corpus/evidence/round28-calibration/final-acceptance`
  exits0:11 expected-exit command stages, complete alternate metric/projection agreement, two-way revert
  counters unchanged,355 existing verdict IDs preserved. Historical checked329/318/0/6/5 unchanged;
 26 old OOP IDs retained plus2 round28 disclosures. Exact run: final-acceptance-run.txt.
- Final counting commands: `python3 plans/benchmark_spec_audit.py --summary` still812/812 IDs,5 sets,
  27 strata,16 cases,651 targets,0 findings; URL provenance205=196 explicit+9 defaulted. C2 summary
  still13 rows/35 paths/12 links/0 mismatched rows. Source inventory60→69, malformed0,9 added A rows;
  this is not9 new publications. `source-inventory-{before,after}.json` retain actual commands/exits.
- Source metadata corrections append S067/S068/S069 rather than overwrite committed S066/S061/S062;
  older knowledge entries receive named append-only clarifications. S005/S006 are reopened as bounded
  task/test-audit precedents, not WebArena validity evidence. Whole-registry conformance is separate from
  C2; new-entry source-use red/green fixture is separate too.
- Original case writers appended corrections for bibliographic slips, false universal statements and
  runtime assumptions. Original bytes and initial falsifications remain; task validity stays unobserved.
  The falsifier's own S052 token-unit and Task377 column-order errors are also explicitly corrected.
- Corrected candidate freeze v2 is `.ufo/waves/round-28/candidate-freeze-v2.json`, digest
  3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182. Complete same-identity Q10
  re-reads and targeted repair probes are requested against these exact bytes; no canonical admission
  or non-author approval is preclaimed here.

### Round28 — exact reviewed knowledge admission

FContractEntry and FFullEntry returned complete v4 PASS judgments for
50589759b82b26a7199d157035c852260ab1b10b59815f7b57e7534eccfd2ead.
The canonical entry is copied byte-exact; index/coverage/partial-frontier rows, seven source-use links,
specific SKILL workflow and PROVINCE boundaries ship together. V1–v3 findings/digests remain historical.
Both demonstrated capabilities enter the round28 repertoire; scores stay7/8, no other axis changes.
Actual commit-tree timing/byte proof and clean-lane measurement follow the lane helper's landed revision.

### Round28 — actual-commit findings corrected without rerolling history

Admission df33fc83764975fd808b0945097b5d0c7aca3901's actual Gate/census each exited1; receipts remain.
FFullEntry appended its already-returned v4 PASS in the required plain marker format. The census exposed
a real legacy scope bug: round26 revision_text ran through EOF and consumed round28 score prose.
Bound it at the next H2; a permanent fixture is red1 before / green0 after that production-line change.
The restored JSON is329/318/0/6/5, P4 two offline groups and one superseded ID retained. See
historical-scope-selftest-{red,green}.txt, historical-scope-restored.txt and state-check-scope-fix.json.
This is an explicit, bounded exception to the prior state-check byte-preservation statement, not a
numeric/data rewrite or a conversion of uncertainty into MATCH. Candidate and new C1/C2 code are unchanged.

### Round28 — corrected measured revision and final evidence

Landed/pushed measured revision **78e6df8171edf8afbb85e7345aea97f6cb2c7228** has actual Gate
admissions1/passed1/failed0 and census exit0, with69 conformant source rows and36/36 knowledge/index.
All old355 verdict IDs persist;329 checked318 MATCH/0 MISMATCH/6 SUPERSEDED/5 offline plus29 OOP;
P4 retains48 MATCH/1 SUPERSEDED/2 offline. Exact candidate50589759… and review/code bytes are
verified from that commit's tree (actual-final-byte-proof.json).
Final complete acceptance exits0 with11 expected-exit stages, actual source-use links clean,
alternate/revert equality and the intentional historical-scope code pin. No model/site execution or
new-method score credit. Scores7/8 held; outside closure remains separate. All first-red evidence stays.

## Round 29 — WebArena generated-config projection (2026-10-21)

### Round29 — post-crash integration, falsification and repair

The host session died during the build wave (23 of 64 seats dead, all three executors; build-dead-seats.json).
Replacement L1 KengakuR29-2 integrated `plans/config_projection.py` from landed build reports and adopted
three seat-authored hand fixtures byte-exact (b98dcf31). One fresh 77-seat post-crash falsify wave re-ran every
counting command: four independent oracles reproduced all 2436 projected objects, 1435 provenance records and
every count (812/812/3/2436; 1435 occurrences, 1416 changed leaves, 61 non-URL-path leaves, 697 `//` junctions).
Re-verification result for C1's counts: unchanged. Survivors and defects were repaired, not hidden: value
normalization and value-shape category mutants survived (FMutNormalize/FMutCategoryShape), the AST contract
accepted 14 semantically different generators (FReviewAstContract), python -O silently stripped the selftest,
unexpected errors exited 1 with no finding, and `--json` key-sorted projected tasks. After repair the persisted
witness kills 10/10 mutants, the projections are object-equal to the pre-repair output, and the JSON digest is
identical on CPython 3.9–3.15 (repair-*.txt). Candidate v1 was superseded by v2 on falsify findings.

### Round29 — final negative controls and entry scope

The second re-check exposed two more test survivors: narrowing URL_FIELD_TEMPLATES and forcing the real
audit's exit to zero. Explicit URL-path and real-audit-finding fixtures now kill both (12 persisted mutants).
The final entry v3 qualifies same-lane oracle independence, separates review-only task-count bridges,
and records falsifiers. It does not change any projection count or promote an offline disclosure to MATCH.
The admitting tree must contain returned exact-v3 PASS reviews, registry, source-use links, index/coverage,
PROVINCE/SKILL boundaries and byte pins. Trial/actual commit receipts record that requirement separately.

### Round29 — locator corrections and scratch safety

Final source re-read found renderer-dependent Python-document coordinates, then the load/loads inheritance
hop. S075/S076 correct those locators append-only; entry v5 changes only that header after v3. Downloaded
FRevEnumerate source copies flagged by FSentinelSecrets were removed before final admission, including
an accidental credential-bearing env_config snapshot in the earlier scratch commit. No history rewrite
or claim of historical-object purge. Evidence: credential-copy-removal.txt, final source/safety re-reads.

### Round29 — actual landed-tree evidence

Landed measurement revision6baa3090b6cf2d50e56b94b806a69f41220081df equals the pre-landing trial tree
33d75ccd8be05c941045f00e05b12ce9ee0cd4af. Actual structural Gate and separate digest/final-PASS checks
both exit0; source76, knowledge/index37/37, historical329/318/0/6/5, P4 unchanged. Corpus v5 exact digest
c4412f67… binds both returned complete final re-reads in the admitting tree. Measurement receipt paths:
corpus/evidence/round29-calibration/actual-*, trial-landed-tree-proof.json. No outside closure is claimed.

### Round29 — current-tree source-copy containment correction (2026-10-21)

The earlier safety follow-up proved absence of five loose paths only. A non-author opaque archive
check found the same flagged module still compressed in the tracked scratch wheel
`.ufo/waves/round-29/scratch/falsify/FCritNovelty/fetch/libwebarena-0.0.5-py3-none-any.whl`
at baseline `6a2c2df788a4fdb216dd5790f9ae6dd326169f47`. Its archive SHA-256 is
`5cfdf8abc2b40cc4442905a29af1c45c5fd0ed57bbfe8e3a6421a2e53cb6cb1b`; member
`webarena/browser_env/env_config.py` has Git blob identity
`81cf52de7d998c90abb3741416e2c8ab9b434758`, identical to the removed loose module.
The parent integrated a single-file current-tree removal after exact identity/size/inode checks,
with a sanitized lesson and index row. No production instrument or unique projection fixture
depends on this fetched wheel; the fetch receipt stays as a receipt, not a presence claim.
No module values were printed or used, no package or gate was executed, and no benchmark endpoint
was contacted. This is not a history purge, credential rotation, outside admission or global-clean
claim; retained history and other possible carriers remain unresolved under the operator hold.
Full bounds and reproducible opaque identities: `corpus/lessons/round-29-source-copy-containment.md`.
The appended fleet-report erratum identifies the actual landed containment commit.

## Round 29 attempt 2 — shokuknow assimilation and a standing adoption gate (hyaku run 6, 2026-10-25)

Attempt 1 of round 29 (above, 2026-10-21) is unchanged history. Run 6 re-dispatched the same round;
this attempt carries two new claims and never re-claims the generated-config projection. Baseline
`1f3b0f1ec41ec297130e8944ff97968d32324632`; frozen prereg `plans/round-29-attempt2-claims.md`;
freeze commit `8c14a5dcd15ac364a352d544660c69f521c3a6af`.

**C1 — shokuknow assimilation (coverage, lowest non-retired axis).** Adopted one entry under one
theme — published per-task validity instruments — `corpus/knowledge/benchmark-task-validity-checklist.md`
citing S077, S078, S079, S080, S090, every source re-opened 2026-10-25 with a located ≤25-word quote.
Registry 76 → 82 rows (six tier-A additions; S090 upgraded from the package's B to A because a
first-party maintainer statement is tier A and the "no visible date" reason is page-scoped — the
publisher's news index dates the post 2025-11-07). Three staged entries rejected with reasons and
flip conditions; 168 uncited rows and 64 uncited entries not appended (CORPUS rule 4).

**C2 — standing source-adoption gate (operability, capability acquisition).** `plans/sources_adopt.py`
(collision detection under the census's own 0–3-space anchor, staged-row schema, prose-`recheck`
normalization, `used-by` projection; ten-case selftest) and `plans/adoption_check.py` (the
one-command adoption counter). Ten mutants applied by a mutation-tester seat; the two that survived
the first pass (an unescaped 12-cell row, and an invalid nonempty `recheck` escaping `check()`)
were killed by added assertions in existing cases 5 and 10.

**Measured (author-side).** `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`
→ `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0;
do-nothing control at freeze → `entries=0 …` exit 1. `python3 plans/sources_adopt.py --selftest` →
`SELFTEST cases=10 failed=0`, exit 0; re-append of the five landed ids → `collisions=5`, exit 3;
pre-append registry build → exit 0. Census exit 0 at both ends.

**Re-verification (freshness).** `python3 grader.py` → `CHECKS n=733 mismatches=0 errata_pinned=1`,
`VERDICT: PASS`, exit 0. `python3 plans/round28_census.py --revision 6baa3090…` exit 0.
`python3 plans/config_projection.py --summary` → `TOTAL findings=0 exit=0`. Fleet source census
exit 0 (14 known cross-scope duplicate-URL warnings retained, none suppressed).

**Waves.** One 36-seat v1 wave (`kengaku-r29a2-build`, band 32–64, policy
`scripts/hyaku/ufo-wave-policy.json`), roles: scout 10, reviewer 10, scribe 3, executor 3, critic 3,
connector 2, simplifier 2, mutation-tester 1, revenger 1, sentinel 1; 14 attack seats (39%). L1
holds the canonical planner seat. No dead seats. No pacman or tool installs.

**L0:** none new. The two inherited round-25 coverage-cap/novelty-conversion questions remain open;
C1 does not move the canonical coverage number and says so.

**Safety:** `shokuknow/` was read only (no campaign tool run, no write, no fetch, no push); the fleet
root, sibling lanes and `.ufo/state` untouched; the lane's own new bytes carry no credentials.

**Round 29 attempt-2 corrections (appended 2026-10-25, append-only).** The wave's own attack seats
found five defects after the first landing commit; all are repaired and re-measured, and none
changes a frozen target:

1. **`recheck` semantics.** Normalizing a prose `recheck` to the *access date* made every adopted row
   0 days overdue (fleet `sources-census.sh overdue` reported 5 rows at `0d`, exit 1; five of the six rows — `round28_census.py` carries no overdue field). Rows now carry `180d` (due 2027-04-23) and the
   tool takes `--recheck` (default `180d`); the stripped prose stays in this lesson's Gate block.
2. **Strict vs targeted gate modes.** `sources_adopt.py` is strict by default (any staged defect
   refuses: `exit 3`, 2 escaped-pipe rows + 6 collisions on the landed registry) and offers
   `--scope-to-admit` for a targeted append (exit 0 on the pre-append registry). Receipts:
   `corpus/evidence/round29-attempt2/gate-strict.txt` and `gate-scoped.txt`.
3. **Counter repairs.** `adoption_check.py` now prints exactly the frozen seven fields, gates
   `cited_rows`/`usedby_ok` per entry (a 3-of-5 entry and a 1-of-5 linkage both fail), anchors the
   README index row and `verified-at` to lines, treats an unrun census as a failure
   (`census=skipped` → exit 1), and refuses an empty expectation.
4. **Selftest repair.** Two mutants that survived the first pass (a 12-cell row with no escape; an
   invalid nonempty `recheck` bypassing `check()`) and one raised by a later audit (deleting the
   recheck normalization) are killed by assertions added to existing cases 5 and 6; the suite stays
   at ten cases. Re-run after the fix: `no-recheck-normalize`, `twelve-cell-accepted`,
   `anchor-column-zero`, `drop-dupe-check` all die.
5. **Prior-art pricing.** S091 (Agentic Benchmark Checklist, arXiv 2507.02825) was opened and added,
   and the entry now states it is INCREMENTAL; `novelty` holds at 7 with no credit taken. Registry
   82 rows (S001–S080 + S090 + S091), tiers A 76 / B 4 / C 2. `adoption_check.py` still counts the
   five cited ids, unchanged.

Final measured state: `python3 plans/adoption_check.py --expect .ufo/waves/round-29/attempt2/adoption-expect.json --census`
→ `entries=1 indexed=1 cited_rows=5 rows_present=5 rows_mined=5 usedby_ok=1 census=ok`, exit 0;
`python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=10 failed=0`, exit 0; fleet census
exit 0; `grader.py` exit 0; `round28_census.py` exit 0; `config_projection.py --summary` exit 0.

**Round 29 attempt-2 corrections, second batch (appended 2026-10-25).** Three more attack seats scored
the landed state and each finding was repaired:

6. **Entry widenings removed (six).** Axis A no longer claims that every behaviour the tests check is
   described in the instruction (S077 checks file references only); F names the top-level `cheat/`
   directory it actually rejects; G is scoped to the maintainer's *own* repository and now records
   that Harbor's literal canary string occurs in 0 files of the pinned Terminal-Bench 2.0 tree; H says
   88 of 89 directories; J says the gate is dated and hardware-stated, not cheaply re-runnable; the
   S090 line quotes the maintainers' own admission instead of asserting a pass/fail history. The
   negative space gains "not synthetic replication" and "canary presence is detectability, never
   proof of exclusion".
7. **`used-by` must name the citing entry exactly.** `adoption_check.py` compares whole path
   components, so `…-checklist.md.bak` fails (`usedby_ok=0`, exit 1) where a substring match passed.
8. **An unrun census is not a pass.** `ok` now requires `--census` and a zero census exit; the
   no-census run prints `census=skipped` and exits 1, so only the full invocation can print the
   frozen target line.
9. **`plans/round28_census.py` row anchor widened to 0–3 leading spaces** — its column-zero-only
   pattern silently under-counted an indented row (`rows` would read 81 against a live 82). Now 82,
   exit 0.
10. **Counts corrected in the lesson**: registry 76 → 82 rows, tiers A 70 → 76 (S091 landed after the
    first paragraph was written).

Final state re-measured after the second batch: counter `entries=1 indexed=1 cited_rows=5
rows_present=5 rows_mined=5 usedby_ok=1 census=ok` exit 0; `--selftest` 10/10 exit 0; fleet census
exit 0; `round28_census.py` exit 0; no-census control exit 1.

**Round 29 attempt-2 corrections, third batch (appended 2026-10-25).** A residual critic re-attacked
the landed gate and found that `build_block` stamped `opened`/`status` onto whatever row it was handed,
so a stale or fabricated row could be laundered into the registry with every exit code green. Repairs:

11. **No silent stamping.** `build_block` refuses a staged row that is not `mined`, and refuses a row
    whose `opened` is not the round's access date. Re-dating requires the explicit `--attest-opened`
    flag, which prints the attestation into the receipt (`gate-scoped.txt`). The gate cannot verify a
    fetch; the attestation is the honest boundary, and C1's re-grounding duty rests on it plus the six
    reviewer seats that re-fetched the five sources independently.
12. **Argument validation.** `--access-date` must be ISO, `--recheck` must be an ISO date / `<N>d` /
    symbolic cadence, and a repeated id in `--admit-ids` is refused (`duplicate-request`).
13. Selftest case 6 also proves the stale-row refusal and the attested re-dating, so the laundering
    path cannot reopen without turning the suite red.

Re-measured after batch 3: `--selftest` 10/10 exit 0; targeted build exit 0 with five rows and the
attestation line; strict package run exit 3; C1 counter unchanged (`entries=1 … census=ok`, exit 0).

**Round 29 attempt-2 corrections, fourth batch (appended 2026-10-25).** A residual entry reviewer read
the landed entry against the fetched bytes and found four claims to correct:

14. **Axis D quote.** The cell quoted a span that crossed a `<code>` element (`download-youtube`), so
    it was not a byte run. The quote is now the 18-word sentence after the slug.
15. **"Applies ABC to itself".** The entry asserted it of the benchmark behind S077; S077 contains no
    ABC mention, and the paper that does is not among this entry's rows. Removed, and the ABC item
    coverage is now stated as weak for C, F and G (reporting items, not trials).
16. **Canary completeness.** "0 files" was true but incomplete: 275 files across 88 of 89 task
    directories carry a `terminal-bench-canary` string with the same GUID, and one task carries
    neither. Both facts are now recorded, and they are the sharper axis-G evidence.
17. **S090 post-publication claim.** Restated as the maintainers' own admission of a defect, with an
    explicit note that S090 does not say the task passed oracle and nop before release.

S091's `used-by` now names the entry it prices (the entry's §Prior art quotes it); its id is
deliberately not a sixth `source:` line, so C1's five-row expectation is unchanged.

**Round 29 attempt-2 corrections, fifth batch (appended 2026-10-25).** The residual calibration seat
re-derived 32 claims from committed bytes and found five mismatches; three were live and are repaired:

18. **Registry count in the SCORECARD C1 cell and the LOG entry** said "76 → 81" against a landed 82.
    Both now read 82 (S077–S080, S090, S091), matching `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`.
19. **The overdue blast radius** was written against the wrong instrument and unit: the fleet
    `sources-census.sh overdue` reports **5 rows at 0d, exit 1** on the pre-repair registry;
    `plans/round28_census.py` carries no overdue field at all (my "0 → 1" read the exit code as a count).
20. **The prose-`recheck` count** in the round gate table said 171; 171 was the freeze tool's
    *total* defect count. The cell count is **167** (2 escaped-pipe rows make up the rest).

The two remaining mismatches are not live errors: a mutant count ("five" in the SCORECARD versus
"four" named in the correction) is numbering across two attack seats, and the axis scores themselves
are not command-derivable — the report already labels them held judgments with their cap premise.

## Round 30 — assimilation round 2, routed-defect closure, quote-validating gate (2026-10-25, hyaku run 6)

Baseline `363a4ebf`; frozen prereg `plans/round-30-claims.md`. Three claims on three axes:
C1 coverage (lowest non-retired, tie-break over novelty), C2 calibration, C3 operability.
Round shape: v1 wave 1 build (36 seats) + v1 wave 2 falsify (33 seats) = 69 seats.

1. **C1 — the contamination-transparency card admitted as an amendment.** The staged package entry
   was refused at round 29 as "a fourth card design"; the recorded flip was to land it as an
   amendment to the tabulated designs. This round re-opened all six of its sources on 2026-10-25
   (S081 arXiv 2608.29463, S082 arXiv 2607.01254v2 full text, S083 Findings of EACL 2026, S084
   OpenCompass 0.4.0 docs, S085 the CAICT 2024 report — round 29's HTTP 000 did not recur — S086
   the ANLP 2025 paper), replaced every anchor with a located quote from this round's own fetch,
   mapped the field list into the round-6 union table's own columns, declared the delta (two new
   fields, one new value set), renamed the entry's own answerability questions **CG1–CG8** to stop
   colliding with `QUALITY.md` Q1–Q8, and wrote an `Extends` section naming both the lane entry it
   extends and the staged tabulation (labelled unlanded, so no load-bearing claim rests on it).
   Registry 82 → 88 rows; knowledge 38 → 39; index 38 → 39. Counter (frozen):
   `entries=1 indexed=1 cited_rows=6 rows_present=6 rows_mined=6 usedby_ok=1 census=ok`, exit 0;
   the do-nothing control is `entries=0 …` exit 1.
2. **C2 — the five routed defects closed.** D1: the receipt now exists at the path the round-29
   report cites, carrying the report's seven-field quoted line *and* the wave file's eight-field
   variant beside it. D2: the kappa sweep is narrowed to the scope its command measured, with both
   counts (65 at the round-29 tip, 66 at round 30) and the line-vs-occurrence unit stated. D3: the
   lesson's S078 line-75 quote is priced 8, matching `wc -w` and the registry. D4: the +22-line
   critic addendum is committed. D5: the S091 `used-by` asymmetry is recorded in the round-29
   expect file without moving its seven printed fields (re-ran: `cited_rows=5`, exit 0).
   `python3 plans/round30_defects.py --lane .` → `defects=5` exit 1 at freeze → `defects=0` exit 0
   after the landing commit.
3. **C3 — the adoption gate now validates quotes.** `plans/sources_adopt.py` gains a quote mode
   (`--quote-file`/`--artifact`): every quoted span in a row's anchor cell must be ≤25 words and a
   byte substring of a named capture, with exit 6 (over-long), 7 (absent), 4 (structural), 2
   (unreadable artifact) beside the existing 3/4/5. Selftest 10 → 14 cases; the ten original cases
   keep their names and verdicts and the five pre-existing invocations are stdout/exit identical.
   Scope stated where it cannot be overstated: the gate proves the bytes it was handed contain the
   strings — it does not bind the artifact to the cited URL, its 25-word cap is inert for CJK (a
   46-character Chinese span counts 1 word), and PDF text layers need extraction first.
4. **Frontier step.** Census before → after: exit 0 both ends, 82 → 88 rows, the same 14 `W04`
   duplicate-URL warnings (`corpus/evidence/round30/census-before.txt`, `census-after.txt`).
   Id-collision check before any append: 82 registry ids vs 175 staged ids → 6 collisions
   (S077–S080, S090, S091), resolved by adopting only ids the registry did not hold
   (`.ufo/waves/round-30/assimilation/`). Quarantine slice re-derived: 2 rows (S091 quote-present,
   S105 unverifiable). One considerthese proposal landed as `QUALITY.md` Q20 (out-of-band gate run
   on gate-touching landings), with its three measured limits.
5. **Mistakes mined** (`corpus/lessons/round-30.md` §Mistakes): a repair that printed green while
   making D2's check unsatisfiable (markdown-emphasis strip deleting the `*` of the glob), caught by
   a falsify seat rather than the counter; and an adjacent D1 repair that recorded the quoted-line
   mismatch instead of answering it. Both fixes are in the landed counter, which now judges the
   committed HEAD blob and re-derives the kappa count in `grep -rn` line units.

**Re-verified this round:** fleet census exit 0 (both ends); round-29 counter unchanged
(`cited_rows=5`, `corpus/evidence/round30/r29-counter-unchanged.txt`); gate selftest
`cases=14 failed=0`; six sources re-opened with sha256 and byte counts recorded per row; the
round-29 receipts (`grader.py` 733/0 PASS, `plans/config_projection.py`, `plans/round28_census.py`)
re-run in the round's build seats and reported unchanged there.

**Waves.** Wave 1 build 36 seats (10 scout, 7 reviewer, 6 executor, 4 scribe, 3 critic, 2 connector,
2 mutation-tester, 1 revenger, 1 simplifier). Wave 2 falsify 33 seats (12 scout, 8 reviewer, 5
critic, 5 executor, 1 mutation-tester, 1 connector, 1 revenger) — 16/33 attack roles (48%).
Yield per seat: `.ufo/waves/yield.tsv` round-30 rows. No seat died before the falsify wave; the
wave-2 dispatch was refused twice at the host job limit and resent unchanged once a slot settled.
**L0 questions:** none opened this round. **Safety:** no pacman transaction (host pause respected),
no tool installed, no write outside the lane repo, the report and the round's own wave directory;
`/home/vgpnk/Projects/shokuknow` read-only throughout.

## Round 31 — correction to the round-30 C1 entry above (appended 2026-10-25, not rewritten)

Superseded text, quoted from the round-30 entry above at `LOG.md:792-793` (this file is append-only, so
those bytes stand as filed): the card entry "declared the delta (two new fields, one new value set)".
Both halves of that parenthetical are wrong against the entry's own current bytes:

- **"two new fields"** is the first reading the entry retracts, named as retracted at
  `corpus/knowledge/contamination-transparency-card.md:82-84` ("Two earlier readings of this paragraph
  (\"two new fields\", then \"one field, one placement, one value set\") overclaimed; this is the
  corrected one").
- **"one new value set"** is wrong for the same reason: the entry's strata value set is inherited, not new —
  `contamination-transparency-card.md:78-81` ("strata is a value set this entry inherits from two
  cited-or-tabulated sources, not a discovery").
- **The admitted reading** is `contamination-transparency-card.md:72-75`: "So the delta is one field, and
  the rest is not a delta at all. **The only field this entry adds to the union table is S2, and what it
  adds is the field — a state recorded for the card itself rather than for a contamination type. Its values
  are not new …**". S1 is carried by the CTC v1.1 form's run-side column and is a rename rather than a new
  field, and this lane has not admitted that form, so the hedge in the entry (`:76-78`) travels with the
  correction.

Routed by round 30's non-author closure (`corpus/lessons/round-30-verifier-spotcheck.md` §5 item 1);
re-derived by `plans/round31_defects.py` check R1. The same reading is corrected in
`corpus/lessons/round-30.md` §Errata (Q6 basis) in this round. Locators above were re-read after the
entry's own R4/R5/R7 repairs moved its line numbers, and after the R1 reviewer showed an earlier draft of
this block cited a window that contained neither sentence.

## Round 31 — verifier execution model, routed-defect closure, citation-bound gate (2026-10-25, hyaku run 6)

Baseline `0883e72`; frozen prereg `plans/round-31-claims.md`; landed round work `dbb07364`. Three claims on
three axes: C1 coverage (lowest non-retired, tie-break over novelty), C2 calibration, C3 operability. Round
shape: v1 wave 1 build (36 seats) + v1 wave 2 falsify (36 seats) = 72 seats.

1. **C1 — the benchmark verifier execution model admitted.** The staged package entry was re-grounded on
   three sources opened this round at their pinned revisions: Harbor commit `6099b8cf` (the verifier-mode
   resolver, `Verifier.verify`, the bundled-tests flag), SWE-bench Pro V2 commit `66f92766` (the task's own
   test-space reset, its `DATA_DIRS` exclusion, and the log-scan parser behind its PASSED set), and
   terminal-bench-2 commit `2fd12b88` (92 top-level entries, 89 task directories, and the README line that
   names the dataset). The finding: the harness resolves a per-task verifier mode and **shared is the
   default**, so both benchmarks grade inside the agent's container; what holds anyway is narrower than
   isolation — stale rewards are deleted first, and `/tests` is re-uploaded unless the verifier image owns it
   — and SWE-bench Pro additionally restores test *code* from the container's own git HEAD while leaving
   anything under a fixture directory untouched. Registry 88 → 91 rows (S092, S093, S100), knowledge 39 → 40,
   index 40/40. Counter (frozen): `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1
   census=ok`, exit 0; the do-nothing control is `entries=0 …`, exit 1, hardened with the expect digest.
   Second receipt `plans/round31_c1_verify.py` → `checks=6 defects=0`, closing the frozen counter's
   content-blindness that a wave-1 critic demonstrated with a 63-byte stub.
2. **C2 — the ten routed defects R1–R10 closed.** R1: a named correction appended to `LOG.md` (the round-30
   entry's "two new fields, one new value set" is retracted by the entry's own bytes). R2/R3/R10: an
   append-only `## Errata (round 31 …)` block in `corpus/lessons/round-30.md` correcting the Q6 basis, the Q2
   tier cell (`S086 B`, re-derived from the registry) and the falsify seat count (`33`, re-derived from the
   committed registry). R4/R5/R6/R7/R8: entry copyedits — the duplicated "reconciled truth" sentence, the
   duplicated falsifier clause, the staged-source count (`two of its three`, re-derived by document key), the
   S2 claim narrowed to the card-level field, and the ungrounded "CC0" adjective dropped. R9: the five
   round-30 seat reports committed as authored. Counter: `checks=10 defects=10` exit 1 before → `checks=10
   defects=0` exit 0 after; the counter itself was corrected four times when seats proved each gap, and the
   survivors that remain (`R31MutCounter.md`) are disclosed debt.
3. **C3 — the adoption gate binds a capture to the row's citation.** `plans/sources_adopt.py` gained
   `--url-map`: a located quote whose artifact is not mapped to a URL the row cites is refused with exit 8
   (mismatch) or 9 (unmapped), bound on any containing artifact against any cited URL, with the unbound
   summary line left byte-identical to round 30's receipts. Selftest 14 → 17 cases, the three new ones
   failure-capable (the binding removed → `cases=17 failed=2`), and the CLI exercised end-to-end (0 / 8 / 9 /
   2). Scope, stated: this is citation membership, not fetch provenance — the map is caller-authored and a
   row citing a repository root is satisfied by any capture declared against that root.

Also landed: `QUALITY.md` Q21 (a pinned source names its pin in `recheck:` — the one criterion this round
draws from `considerthese/2026-10-24.md` proposal 2, measured absence 5 of 40 entries), `corpus/README.md`
index + coverage + frontier rows, the round lesson `corpus/lessons/round-31.md`, and the Q20 out-of-band gate
receipt `.ufo/waves/round-31/gate-receipt.txt` (`CHECKS n=733 mismatches=0`, `VERDICT: PASS`, every roster
selftest green). Census 14 → 15 `W04`, exit 0 both ends; the 15th is S100↔S079, the same repository read for
a different scope, disclosed in the row and the report.

## Round 33 — 2026-10-25 (hyaku run 7)

Re-grounded the merge package `merge/kengaku/` (benchmark grader semantics) through the lane's own
adoption gate: the round-32 staged rows collided on ids, so the corrected package was restaged under
**S103** (Toolathlon `tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`, tier A — executed
tolerance 0.05 at `:280` vs signature default 0.1 at `:58`; the log-bucket check fails open on caught
exceptions but fails closed on absent credentials via implicit `None`) and **S104** (arXiv
2412.05579v2, tier B preprint — meta-evaluation is its own part of the judge paradigm). S093 stays
`mined` and gains the entry in `used-by`; the four round-32 refusal rows stand unchanged (ids never
reused). Registry 95 → 97, knowledge 41 (unchanged count — the entry already existed unadmitted),
index 41/41. Counters (frozen): adoption gate `collisions=0 defects=0` + quote gate 4/4 located exit 0;
`adoption_check` `entries=1 indexed=1 cited_rows=3 rows_present=3 rows_mined=3 usedby_ok=1 census=ok`
exit 0; `round33_c1_verify` `checks=8 defects=0` exit 0.

Closed the six round-32 routed defects N1–N6 (wave evidence committed; N2 scorecard section; N3/N4
errata appended to rounds 30/31 lessons naming `ae95fe0`/phantom `a44b5a8`; N5/N6 errata at the two
round-31 correction rows). Counter `plans/round33_defects.py` → `checks=6 defects=0` exit 0; receipt
`corpus/evidence/round33/defects-after.txt`.

Re-probed HF + OpenRouter live with committed bounded receipts: `hf_models=50 or_models=467
hf_schema_delta=4 or_schema_delta=0`. OpenRouter's response was fetched with `?limit=10` and
the complete bounded JSON response carries `total_count=467`; `catalog_probe.py --verify`
re-derives the counts and schema deltas from the committed raw bytes, exit 0.

Wave: build 36 seats + falsify 36 seats via the orchestrator's inline OMP bridge (v1).
QUALITY.md gains Q22 (receipt-is-evidence-only-if-re-run). considerthese/2026-10-25 proposal 3
landed as an L0 append (`22d28422`); proposal 1 noted operator-side. Lane tip after landing: see
git. Fleet report: `.ufo/reports/round-33/kengaku.md`.

## Round 33 integration corrections (after the falsify wave)

- The frozen C1 narrative's S093 `used-by` transition is false: its cell already named the draft at
  freeze (the pointer was added by round-32 commit `bcd2a6c`); no S093 cell changed in round 33.
  The frozen control also prints `entries=1`, not `entries=0`; the final-state C1 transition is
  `rows_mined=1 → 3`, `usedby_ok=0 → 1`, while the source registry alone grows 95 → 97.
- Independent `git ls-tree` and README counting at `112091c2` show 41 knowledge files / 41 index
  rows, not the freeze file's 40/40. They remain 41/41 after admission: the existing draft was
  admitted and its source ids re-pointed; no knowledge file or index row was added in this round.
- The final S103 citation is blob-only at Toolathlon `9be8d8fe`; S104 is pinned to
  `https://arxiv.org/abs/2412.05579v2`. `append-rows.md`, `append-block.md`, `landed-rows.md`,
  and SOURCES rows are byte-identical; final quote gate 8/8, `cmp` clean, capture manifests verify.
- The source entry was corrected for the S093 capture statement, diagnostic-log carve-out,
  percentage-point support, PROVINCE locator, additions-vs-edits reset path, one-task scope and
  survey spellings. S093 `test.sh` is now in the capture SHA256 manifest.
- The C1 V8 second receipt was corrected from anchor cell `row[5]` to teaches cell `row[6]`;
  regression selftest now includes a green refusal-row fixture and an erased-teaches red case
  (`SELFTEST cases=11 failed=0`), while its frozen lane output remains `checks=8 defects=0`.
- C2's `defects-after.txt` revision pointer is corrected to the repair commit `7895588`; the
  count re-derives at the final tip. The falsify wave found the counter's semantic blind spots,
  so calibration remains 8 rather than taking a score increase.
- C3 raw capture stores complete response bodies under 64 KiB (`HF 27,698 B`, OpenRouter
  `?limit=10` 16,010 B). Its 467 count is parsed from the API's raw `total_count` field; the
  offline verifier proves internal consistency, not endpoint authenticity, so the frozen
  "no fabricated bytes" kill-rule assurance is not supported.
- Swarm shape was 36 build + 53 falsify = 89 seats (0 dead, no residual call). One falsify report
  (`R33FCensus.md`) was misrooted into the fleet wave tree, then copied byte-exact into the lane
  and removed from the fleet root. No tools were installed.
- A direct Git commit briefly parked the C1/C3 payload on detached orphan `2b4cef2e`; it was abandoned and the changes were re-landed through `jj-lane.sh`. Final branch/remote equality is recorded in the report.

## Round 34 — 2026-10-25 (hyaku run 7; honest stop)

Declared C1 coverage (lowest tied axis 7): open the pinned Terminal-Bench 2.0 `protein-assembly` evaluator and ground its comparison against the task artifacts. Declared C2 calibration (8): harden the round-33 counter against four mutant classes. Claims frozen at `plans/round-34-claims.md` (freeze `adaf25dfd27dedfc1bf25f308576a6f2c8ad64ae`); before values and controls in `.ufo/waves/round-34/claims/`.

One v2 wave, 64/64 spawned, no residual call. Seat mix and statuses: `.ufo/waves/round-34/build-results.json`; captured evidence and seat reports under `.ufo/waves/round-34/build/` and `.ufo/waves/round-34/assimilation/`.

C1 honest stop: pinned evaluator captured at `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, but no sourced corpus admission landed; `R34ReviewCounterC1.md` identifies V3–V8 counter gaps including V7 red against the truthful frozen control and V8 accepting an external checksum path. Score coverage remains 7, held. The expected-artifact files were read, but the output test embeds expected sequences rather than reading those files (`R34CriticEntryTB2.md`); entry wording is scoped accordingly in the report.

C2 honest stop: `R34ReviewClaimsFile.md`, `R34CriticC2.md`, `R34MutC2Harness.md` show the frozen clean-tree/harness predicate unsatisfied, N3/N4/N7 baseline failures in the candidate draft, wrong mutant surfaces/labels, and incomplete width/newline red-before execution. Calibration remains 8, held; no C2 capability credited.

Quarantine: S091 refused — required NEC quote absent from 418-byte Access Denied response (`assimilation/quarantine-verdicts.txt`); S105 quote located in METI archive, but no S109 row appended because no admitted entry cites it. Package screen: zero entries admitted, six refused/held as staged (`R34ReconPackage.md`). Considerthese proposal 2 was mined as a Q23 draft only (`R34Considerthese.md`), not landed as criterion after C2 failed.

Frontier census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` — before and after exit 0, 15 W04 each; SOURCES 97→97, tier A/B/C additions 0/0/0, rows touched 0, frontier rows advanced 0. Receipts: `corpus/evidence/round34/census-{before,after}.txt`.
No tools installed. No round-34 corpus capability entered. Fresh non-author round closure is pending.

## Round 35 — 2026-10-25 (hyaku run 7)

Declared C1 coverage (lowest, tied 7): admit the pinned Terminal-Bench 2.0 `protein-assembly` grader
(S105 `tests/test_outputs.py`, S106 `tests/test.sh`, S107 `instruction.md` @ `2fd12b88`) as
`corpus/knowledge/tb2-protein-assembly-grader.md`, with an executed 18-case offline probe. Declared C2
calibration (8): move the round-34 closure's routed defects D1–D5 into a persistent ledger
(`corpus/defects.jsonl`, `plans/defect_ledger.py`) and close them. Freeze `11d64530` (claims, both
counters, probe case table with predictions, ledger rows open, four red controls).

- Re-opened the six pinned files live (curl, 2026-10-25): byte-identical to the round-34 captures;
  the round-34 `/tasks/…` URLs return 404 (`.ufo/waves/round-35/build/R35ReopenPins.md`).
- Probe: `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` →
  `cases=18 observed_pass=5 observed_fail=13 mismatches=0`; deterministic across two runs and Python
  3.13 (`R35ProbeRerun.md`); an independent re-implementation agrees 18/18 (`R35IndepGrader.md`);
  three harness mutants detected (`R35ProbeHarnessMut.md`).
- C1 landed at `4fe72a9a`: `python3 plans/round35_c1_verify.py --lane .` → `checks=6 defects=0`,
  `PREDICATE C1 pass`. C2 landed at `dfcd294c`: `python3 plans/defect_ledger.py --lane .` →
  `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`.
- D2: 109,413 committed mirror paths under `.ufo/waves/round-34/mut-entries-scratch/` and
  `build/R34MutRegistry/{mirror,mut}/` deleted at the tip (history keeps them). D1: the three
  round-34 plan drafts moved to `.ufo/waves/round-34/drafts/`; two cited scratch JSONL files
  committed; three untracked nested-repo mirrors (`R34MutReadme-*`, ~10 GB) removed.
- Wave-1 falsifiers found counter weaknesses after freeze: a junk package (`R35CritControls`), false
  but labelled D4/D5 lines (`R35CritC2`), unparsed straight-quote rows (`R35MutC1Quotes` M4). The frozen
  predicates are not changed; `plans/round35_hardening.py` is a post-hoc fix shown able to fail on all
  five counterexamples (`corpus/evidence/round35/hardening-counterexamples.txt`).
- After freeze, `corpus/defects.jsonl` row R34-D1's `recurrence_of` text was corrected from
  `R32-N2` to `R33-N1` (`plans/round-33-claims.md:87`); no check reads that field.
- Scope wording per `R35CritScope.md`: PROVINCE gains a round-35 paragraph (offline synthetic-fixture
  execution of one grader function; not task validity).
- Tool use: biopython 1.85 via `uv run --with` (ephemeral uv cache env; channel uv/PyPI; reason: the
  grader's own pinned dependency). No other installs.

### Round 35 — errata (appended after the falsify wave)

- E1 (`F35LogDraft`): the C2 green output is attributed above to `dfcd294c`; at that commit
  `corpus/lessons/round-35.md` was not yet committed, so R34-D5 reads `observed=fail` there. The
  frozen C2 predicate first holds on committed bytes at `4fe72a9a` (lesson landed), and holds at
  the final tip.
- Entry `## Errata` appended (max passing gBlock 2768 nt, not 2766; findings 1 and 3 narrowed;
  `non-acgt-base` confounded; table header overstates) from `F35MaxNt`, `F35GOnlyLinker`,
  `F35IndepWindows`, `F35CritC1`. README correction lines appended (`F35RevReadme` F1).
- S105/S107 anchor word counts corrected in place in rows added this round: S105 "(9 words)" →
  "(11 words)", S107 "(16 words)" → "(15 words)" (`F35ReopenS106S107`); quotes, locations and
  digests unchanged.

## Round 36 — 2026-10-25 (hyaku run 7)

Declared C1 calibration (8): promote the round-35 hardening clauses into one gate (`plans/pkg_gate.py`)
proven against a frozen 14-fixture junk battery and close the four round-35 routed defects R35-D1..D4
(`corpus/defects-round35.jsonl`). Declared C2 coverage (lowest, tied 7): admit the pinned Terminal-Bench
2.0 `regex-log` grader (S108 `tests/test_outputs.py`, S109 `tests/test.sh`, S110 `instruction.md` @
`2fd12b88`) as `corpus/knowledge/tb2-regex-log-grader.md` with an executed 24-case offline probe. Freeze
`3241b86c` (claims, both counters, battery, probe case table with predictions, ledger rows open, six red
controls); Amendment 1 `acbda2f3`.

- First real probe run after the freeze showed the frozen probe was not byte-deterministic (two
  assertion texts carried a `mkdtemp` path; `corpus/evidence/round36/regex-log-probe-first-run.txt:21-22`).
  One-line repair before any seat scored, `--dry` table byte-identical, all 24 predictions already matched;
  disclosed as Amendment 1 in the prereg.
- Probe: `python3 plans/regex_log_probe.py --lane .` → `cases=24 observed_pass=8 observed_fail=16
  mismatches=0`; deterministic across Python 3.11/3.12/3.13 (`R36ProbeRerun.md`); an independent
  re-implementation agrees 24/24 (`R36IndepRegexGrader.md`); five harness mutants detected
  (`R36ProbeHarnessMut.md`). Findings: a literal alternation of the nine expected dates passes; leading-zero
  octets, digit-adjacent dates, year width, month-length validity and the permitting side of Feb 29 are
  unobserved. Post-hoc, outside the frozen table: the task's own oracle admits `00`-`09` octets and is not
  line-scoped (`R36OracleRun.md`); four more requirement faces are free (`R36CritUnenforced.md`).
- Gate: four candidates from independent executor seats each scored `false_green=0 false_red=0
  unevaluated=0`; `R36GateB` was installed as `plans/pkg_gate.py`. Wave-1 attackers: an overfit gate keyed on
  fixture names/markers also scores the clean line (`R36CritBattery`, 8 cues); the battery leaves eight
  advertised clauses without a fixture (`R36RevClaims` FG1); a junk package passes the C2 counter
  (`R36CritC2Counter`). Frozen predicates and batteries are not edited; the limits are reported.
- R35-D3: the 21 committed nested round-34 attack-mirror paths removed from the tip (history keeps them; sha256
  manifest `.ufo/waves/round-36/integrate/nested-paths-removed.sha256`); 912 round-28 nested paths are cited
  by round-28 evidence and were not touched. Wave-1 scratch mirrors of `corpus/` (~22 MB) were removed
  uncommitted (`.ufo/waves/round-36/integrate/scratch-removed.txt`).
- R35-D4: erratum line in `corpus/lessons/round-36.md` `## Gate` — S130's package states denominator 38 but its rows
  recount to 13 + 23 + 1 = 37.
- Assimilation: mined `considerthese/2026-10-25.md` proposal 2(c) (tip-receipt validator): `pkg_gate.py --rerun`
  covers one receipt of 156; clause (b) is still unbuilt. `merge/kengaku/` re-screened by `R36ScoutMergePkg`.
- Tool use: biopython 1.85 via `uv run --with` (ephemeral uv cache; channel uv/PyPI; reason: the round-35
  grader's pinned dependency, used by `pkg_gate.py --rerun`). No other installs.

### Round 36 — close (appended)

- Wave 2 (34-seat falsify wave, `.ufo/waves/round-36/falsify-spec.json`) was never dispatched: the operator ended the run.
  Round shape: v1 wave 1 only, 40 seats (13 executor, 9 scribe, 5 scout, 4 critic, 3 connector, 3 reviewer, 3
  mutation-tester), 0 dead seats, below the 64-seat floor of the run-7 directive.
- Wave-1 wording fixes applied after the integration commit: the entry no longer says the log is "visible" to an agent
  (harness property, not established), README coverage bullet no longer says "extends", SKILL advice reworded
  (`R36CritScope` F1/F2/F7/F9). Open: the remaining `R36CritScope` fixes, the two confounded probe cases
  (`R36RevProbePred`), and everything wave 2 was to attack.

## Round 37 — 2026-10-26 (hyaku run 8)

Declared C1 calibration (8): make every advertised defect class of the round-36 package gate demonstrable — 55 frozen
one-branch silence mutants (`plans/round37_c1_verify.py`) against `plans/pkg_gate.py` at its freeze digest, a null mutant
and a renamed-fixture run included; survivors are advertised-but-undemonstrated clauses. Declared C2 coverage (lowest,
tied 7): admit the pinned Terminal-Bench 2.0 `configure-git-webserver` grader (S111 `tests/test_outputs.py`, S112
`tests/verify.sh`, S113 `instruction.md` @ `2fd12b88`) with an executed 22-case sandbox probe. Baseline `3ea9a1d9`; freeze
`ca790460` (claims, both counters, the probe and its case table, six captures, red controls); first recorded probe run
`5c7b34e9` (second run byte-equal).

- C1: freeze `MUTANTS total=55 killed=5 survived=50` (the round-36 battery demonstrated M01, M05, M40, M47, M54 only);
  nine wave-1 executor seats wrote `plans/battery37/` (50 single-defect fixtures, one module per clause group, battery commit
  `a3163e67`); landing `BATTERY fixtures=64 wrong=0 renamed_disagree=0`, `MUTANTS total=55 killed=55 survived=0 invalid=0
  null_detected=0`, `PREDICATE C1 pass` on a clean clone.
- C2: probe `cases=22 observed_pass=9 observed_fail=13 mismatches=0`. Observations on the pinned capture: a file served on
  :8080 with no repository, hook or push passes; a body containing `TEST PASSED` passes although the helper prints `TEST
  FAILED` (`test_outputs.py:13` reads a substring of stdout that `verify.sh:62,68` fills with the body); status and content
  come from two requests; curl runs without `-L` or a timeout; only trailing newlines are forgiven. An independent
  re-implementation (`build/R37IndepVerdicts.md`) agreed 22/22 and 3/3 extra cases; a critic ran 4 more cases (4/4 matched).
  The static-file weakness was reported upstream for TB2.1 (S114, issue #133): a replication, not a discovery.
- Frontier: `plans/anchor_digest_check.py` (round-36 routed item 1) flags S110's 63-hex digest and four true-but-uncaptured
  digests at the baseline (`defects=5`); the S110 erratum line (`corpus/lessons/round-37.md` §Gate) and byte captures of the
  four upstream files clear it. Q26 and Q27 added to `corpus/QUALITY.md`.
- Assimilation: `considerthese/2026-10-25.md` proposal 2(a) landed as `plans/ledger_tip.py` (`rows=9 closed=9
  observed_pass=9 mismatches=0` at the tip).
- Re-verification (freshness): the six captures were re-fetched at the pin by `R37ReopenPins` (6/6 identical, `main` has
  not drifted); the round-36 counters, `grader.py` and every registry gate stayed green on the pre-landing sweep
  (`build/R37TipSweep.md`, 25/25) and at the landing tip (`integrate/measure-final.txt`).
- Routed, not absorbed: a real-image run of the task (`build/R37DockerOracle.md`), outside PROVINCE's admitted instrument.
- Tool use: biopython 1.85 via `uv run --with` (ephemeral uv cache, PyPI; the round-35 probe's pinned dependency, used by
  the gate's P10 re-run). bubblewrap 0.13.1 was already installed. Docker image `alexgshaw/configure-git-webserver:20251031`
  pulled and removed by one wave-1 seat. No other installs.

## Round 38 (hyaku run 8, 2026-10-26) — gate behaviours attributed 21/22 (honest stop); fourth TB2 grader executed

L1 `KengakuR38` (planner seat). Freeze `e0a37853` (claims, both counters, the probe and its frozen case table with
`violates=` tags, five captures, red controls; a child of the round-37 L1's `21e6251`, see the lesson header); first
recorded probe run `e95cf550` (second run byte-equal). Lesson `corpus/lessons/round-38.md`.

- C1 (calibration, not admitted): 22 frozen mutants of `plans/pkg_gate.py` under an attributed kill rule; freeze
  `killed=0 survived=22`; twelve wave-1 executor seats wrote `plans/battery38/` (22 fixtures, `dc0cdb54`); landing
  `BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS total=22 killed=21 survived=1`, `PREDICATE C1
  fail`. N21 was frozen as `silence` but makes D5 stricter, so it can only be killed as a mirror (`build/R38BatD5.md`); the
  round reports the miss, does not relabel. New `plans/mutant_direction_check.py` (Q29) flags it: `N21 … MISLABELLED`.
- C2 (coverage, predicate met): TB2 `build-pmars` @ `2fd12b88`, S115/S116; probe `cases=22 observed_pass=7 observed_fail=15
  mismatches=0`. Observations on the pinned capture: a canned 21-line C program with an empty `debian/` dir and a
  zero-byte `src/dummy.c` passes all four tests; a run-time `dlopen()` of libX11 is invisible to the `ldd` string scan
  while a `-lX11` link is caught; `Results:` is a start-anchored match; exit status is ignored when output is non-empty;
  a script earlier on `PATH` answers the behaviour checks while `ldd` reads `/usr/local/bin/pmars`; `debian` may be a file
  and `src/*.c` a directory. Real pytest 8.4.1 agrees 22/22 (`R38CritPytest`), an independent re-derivation 22/22 + 3/3
  extra (`R38CritIndep`). Prior art: TB2 #59 is about the oracle's apt pins; an LLM audit names the provenance gap but
  calls `ldd` reliable; TB2.1 changed the instruction, not the grader. Coverage held at 7 (L0 cap).
- Frontier / routed: Q28 + `## Errata (round 38)` on the round-37 entry (D2; `R38MapErratum`, `R38MapRetro`); anchor check
  binds each digest to its own row's capture (D3; `R38AnchorBind`, cross-capture fixtures now `digest-wrong-capture`);
  ledger-tip binds an absent branch ref, refuses with exit 2 (D4; `R38LedgerTip`); PROVINCE sibling report-out (D6;
  `R38SiblingCite`); D1 was closed by the round-37 L1 in `21e6251`.
- Assimilation: `considerthese/2026-10-25.md` proposal 2(c) landed as `plans/tip_receipts.py` (`receipts=24 byte_equal=4
  differ=0 skipped=20`, tamper control `differ`); `merge/kengaku/` re-screen: 2 admit-candidates (card family) deferred,
  5 hold, 5 refuse (`build/R38MergeRescreen.md`); nothing appended.
- Mistakes mined: the N21 direction (freeze defect), the order-of-operations recurrence (the C2 skip-control ran the probe
  through P10 before the first recorded run, disclosed in the claims), the witness-picked map label (round-37 D2), and the
  claims' source arithmetic (13+1+6 ≠ 22).
- Re-verification (freshness): S115/S116 and three more captures equal upstream `main` and TB2.1's grader
  (`R38ScoutUpstream`); every no-harm instrument green at the landing tip (`integrate/measure-final.txt`).
- Tool use: biopython 1.85 via `uv run --with` (gate P10, ephemeral); gcc 16.2.1, bubblewrap 0.13.1, libX11 already
  installed. pytest 8.4.1 + pytest-json-ctrf 0.3.5 into scratch `uv venv -p 3.13` (PyPI via uv; `R38CritPytest`,
  `R38PlanNext`), removed with the scratch. No pacman transaction.

## Round 39 (hyaku run 8, 2026-10-26) — undemonstrated gate behaviours killed (7/7, directions witnessed); fifth TB2 grader executed

L1 `KengakuR39` (planner seat). Freeze `088f7c36` (claims, both counters, the probe and its frozen 25-case table with
`violates=` tags, seven captures, red controls including an in-process hostile module); first recorded probe run `6a1eb5e1`
(second run byte-equal). Lesson `corpus/lessons/round-39.md`.

- C1 (calibration, predicate met): 7 frozen mutants of `plans/pkg_gate.py` — round-38 N21 carried as `mirror`, six round-38
  wave-2 survivors — each with a pre-freeze direction witness; freeze `killed=3 survived=4`; four wave-1 executors wrote
  `plans/battery39/` (one fixture each); landing `BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0`, `MUTANTS
  total=7 killed=7`, `PREDICATE C1 pass`. A wave-1 critic showed the frozen counter is gameable four ways (A1/A3/A4/A5,
  `build/R39CritC1Counter.md`); the post-hoc `plans/round39_c1_audit.py` closes them for this battery (`AUDIT C1 clean`) and
  refuses the A3 replay. Advertised-only count 2 → 0 (three `adv` cells reach no sentence).
- C2 (coverage, predicate met): TB2 `git-leak-recovery` @ `2fd12b88`, S117/S118; probe `cases=25 observed_pass=13
  observed_fail=12 mismatches=0`. Observations on the pinned capture: the untouched initial repo fails only the flag test;
  writing the literal alone passes 5/5 while the reset-away secret commit stays in the object store (so do `gc` alone and a
  reflog expiry alone); a ref to the secret blob, an annotated tag message, a stash, a dot file and `.git/config` pass 5/5; a
  dangling blob or a dangling commit whose message is the secret fails test 4; git's `fsck --lost-found` ignores reflogs
  (`builtin/fsck.c:905-908`), which is why the oracle passes. Real pytest 8.4.1 agrees 25/25 (`R39CritPytest`), an
  independent re-derivation 25/25 (`R39CritIndep`). Prior art: TB's own nop-validation contract and two third-party runs
  record the task-level reject; one LLM audit names and dismisses the reflog gap; no upstream issue. Coverage held at 7 (L0 cap).
- Frontier / routed: order-of-operations gate `plans/order_check.py` + Q30 (red on rounds 37 and 38, green on 39);
  `## Errata (round 39)` on the round-38 lesson and three TB2 entries (R3, R4); anchor locator binding and ledger-tip
  provenance (R5); direction-check redundant leg (R2); PROVINCE sibling deferral of secret-removal procedure to kagi/souji.
- Assimilation: `considerthese/2026-10-25.md` proposal 2(b) → the order gate; `merge/kengaku/` unchanged, nothing adopted
  (collisions 33, admit-candidates 2 deferred).
- Mistakes mined: the order class closed by a gate; the L1's own erratum on the round-35 genuine-package entry (caught by the C1
  counter's SETUP refusal, reverted before commit); the C1 counter's isolation overclaim; the `adv`-cell count; the
  separability sentence.
- Re-verification (freshness): S117/S118 equal upstream `main` and TB2.1 (`R39ScoutUpstream`); four due SOURCES rows re-opened
  with no status change (`R39SourcesRecheck`); every no-harm instrument green at the landing tip (`integrate/measure-final.txt`).
- Tool use: no host install. Wave-1 seats: pytest 8.4.1 into scratch `uv venv -p 3.13` (PyPI via uv, removed with scratch,
  `R39CritPytest`); docker `ubuntu:24.04` base image pulled to check apt git 2.43.0 (`R39CritFsckReflog`); biopython 1.85
  via `uv run --with` for the gate's P10. No pacman transaction.
- Wave 2 (falsify, 34 seats): re-measures agree (C1 pass + audit clean, C2 pass, probe byte-equal 3/3, rows 2/2); battery39
  reviewed honest 4/4, fixture mutants 12/12; the audit is defeated by a phase-aware daemon (`F39SentinelAudit`), so C1 rests
  on the frozen predicate plus code review; advertised count corrected to 5 of 7 (2 → 0 unchanged); entry wording corrected
  by appended errata (`F39EntryQuotes`, `F39CritOverclaim`); tool defects routed to round 40 (SCORECARD `### Wave 2
  outcome`). Correction (`F39RevScorecard` M1): the four SOURCES rows re-opened above were drift-risk picks, not due rows
  (`sources-census.sh overdue` printed none).

## Round 40 (hyaku run 9, 2026-10-26) — the three tripwire tools mutation-tested (21/21 attributed); sixth TB2 grader executed

L1 `KengakuR40` (planner seat). Freeze `bbb10950` (claims, the tripwire-mutant counter with 21 mutants and witnesses, the
db-wal probe and its frozen 28-case table, spec, C2 counter, eight captures, red controls including a hostile-daemon module
with its counterfactual); first recorded probe run `055748f7` (second run byte-equal); landing `ec172168`. Lesson
`corpus/lessons/round-40.md`.

- C1 (calibration, predicate met): 21 frozen mutants of `plans/anchor_digest_check.py` (11), `plans/ledger_tip.py` (7) and
  `plans/order_check.py` (3), each `adv` cell quoting the tool's docstring at file:line; O13 withdrawn before freeze as
  equivalent. Freeze `killed=0 survived=21`; seven wave-1 executors wrote `plans/battery40/` (21 fixtures); landing `BATTERY
  fixtures=21 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=21 killed=21`, `PREDICATE C1 pass`. The counter carries the
  round-39 R4 repairs (pid-namespaced builds, no in-process battery, pins re-hashed after, counter-owned dirs); wave 1 still
  reached a dishonest `killed=21` two ways (a ledger check body reading its own program text; a PATH `git` shim —
  `R40CritC1Counter`), so admission rests also on the wave-2 battery review. Advertised count 17 (13 direct) → 0.
- C2 (coverage, predicate met): TB2 `db-wal-recovery` @ `2fd12b88`, S119/S120 (+ S121, TB2.1 PR #3, tier B); probe
  `cases=28 observed_pass=8 observed_fail=20 mismatches=0`. Observations: every test opens only `/app/recovered.json`; 22 of 33
  cells are pinned, so a hand-typed export with nine wrong values passes 7/7; "Fix the WAL file" is never read; a plain
  read-write open deletes the undecryptable WAL and the task's own `solve.sh` then fails 2 tests (published upstream: S121);
  `True` passes as an int, float ids fail only the type test, an extra key is free. Real pytest 8.4.1 28/28
  (`R40CritPytest`), independent re-derivation 28/28 (`R40CritIndep`), older SQLite same verdicts (`R40CritSqlite`). Coverage
  held at 7 (L0 cap).
- Frontier / routed: registry rows (R1), `--work` precondition declared for pinned tools (R2), R3 blocked (C1 pins the ledger
  tool), `plans/round_close.py` (Q30 wiring; red on round 38, green on 39/40), `plans/tip_receipts.py` derived mapping
  (round-39/40 receipts now `equal`), PROVINCE round-40 paragraph + adjacency (mutation method stays tameshi's).
- Assimilation: `considerthese/2026-10-26.md` proposal 3 → the `regrade=` column (a same-process determinism read) and the
  stability sweep (5 graders, 15 states, 0 verdict flips, 2 graders mutate their graded state); `merge/kengaku/` unchanged,
  nothing adopted (collisions 37, admit-candidates 2 deferred).
- Mistakes mined: reachability asserted, not witnessed (O13); the `--work` traceback recurring in a frozen counter; a tripwire
  counting receipts it cannot price (fixed); the L1 typing an unobserved exit code (re-run before commit).
- Conformance incident: wave-1 seat `R40CritC1Counter` wrote a `git` shim into the shared host PATH dir `~/.local/bin`
  (outside its write scope); other lanes' git calls hit it (~14:05–14:07 -03); the seat removed it; the L1 neutralized both
  attack modules (they exit at import) and wave 2 runs C1 only in a sandbox with `~/.local/bin` read-only.
- Re-verification (freshness): S119/S120 equal TB2 `main` and TB2.1 (`R40ScoutUpstream`, `R40ScoutPriorArt`); four drift-risk
  SOURCES rows re-opened, two locator notes (`R40SourcesRecheck`); every no-harm instrument green at the landing tip
  (`integrate/measure-final.txt`).
- Wave 2 (35 seats, 35 reports): re-measures agree (C1 byte-equal, every battery module load-bearing; C2 pass, probe
  byte-equal 3/3); battery40 honest 21/21 by non-author review, fixture mutants 21/21; 14 overclaims and 6 unsupported
  sentences in the C2 text corrected by appended errata (one wrong numeral: `plain-read-then-solve` 5 of 7); prior art
  widened (`dzhioev/bro` #659 reports the fabricated-export pass in the wild); counter, `round_close.py` and
  `tip_receipts.py` residuals routed to round 41 (SCORECARD `### Wave 2 outcome`).

## Round 41 (hyaku run 9, 2026-10-26) — two lane tools' advertised behaviours demonstrated (23/23 attributed); seventh TB2 grader executed

L1 `KengakuR41` (planner seat). Freeze `8ef8b4fc` (claims, the round-41 C1 counter with 23 mutants over
`plans/tip_receipts.py` and the `plans/sources_adopt.py` CLI and their witnesses, the constraints-scheduling probe and its
frozen 25-case table, spec, C2 counter, ten captures, red controls including an emptied-mutant-list copy and a hostile
host-write module); first recorded probe run `f774a87a` (second run byte-equal); landing `74513c06`. Lesson
`corpus/lessons/round-41.md`.

- C1 (calibration, predicate met): freeze `killed=0 survived=23`; seven wave-1 executors wrote `plans/battery41/` (48
  fixtures); landing `BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=23 killed=23`,
  `MUTANTS-BY-TOOL receipts=13/13 sources=10/10`, `PREDICATE C1 pass`. New in the counter: `TOTAL`/`FLOORS` binding
  (the round-40 plan's predicate was satisfiable by an empty list — `F40CritPlanNext` D1; the emptied-list control is
  red), exact exit-pair directions for the CLI, builds and tool runs under `bwrap --ro-bind / /` with a fixed system
  PATH. Wave 1 still forged kills two ways (a probe stub reading the bound variant; relative argv escapes —
  `R41CritC1Counter`, `R41SentinelCounter` F1–F4), so admission also rests on the wave-2 battery review.
- C2 (coverage, predicate met): TB2 `constraints-scheduling` @ `2fd12b88`, S122/S123 (+ S124, TB2.1 PR #245, closed
  unmerged, tier B); probe `cases=25 observed_pass=6 observed_fail=19 mismatches=2` (the pilot's two mispredictions
  carried verbatim). Observations: a hand-typed Wed 11:00 file passes 3/3; a decoy first `VEVENT` passes 3/3 (published,
  S124); the earliest test passes invalid earlier slots (`PFP`); rewriting the three input calendars with CRLF passes
  3/3 although the instruction says any modification fails (integrity check on decoded text; unpublished as far as
  `R41ScoutPriorArt` found); RFC 5545 forms (folding, `VALUE=` parameter, lowercase `SUMMARY`) fail the structure test.
  Real pytest 3.13 parity 25/25 (`R41CritPytest`), independent re-derivation 25/25 + 3 (`R41CritIndep`). Coverage held
  at 7 (L0 cap).
- Frontier / routed: registry rows `round41-c1-mutants`, `round41-c2`, `constraints-probe`, `round-close-check` + the
  Round-41 addendum (R3); QUALITY Q31/Q32; `considerthese/2026-10-26.md` proposal 1 → `plans/routed_open.py` +
  `corpus/routed-findings.jsonl` (`routed_open=5 oldest_round=39`); PROVINCE round-41 paragraph (calendar/RFC 5545
  conformance unowned, routed to the orchestrator).
- Assimilation: `merge/kengaku/` unchanged since round 40, nothing adopted (`R41MergeRescreen`: collisions 38, guard
  proven on an indented fixture).
- Mistakes mined: the vacuous planned predicate (fixed, shown able to fail); a seat's cleanup deleting the shared round
  scratch root at 15:42:24 (routed, not yet guarded); "no committed fixture" wording recurring; a forgeable frozen counter
  (routed to a re-frozen round-42 counter).
- Re-verification (freshness): S122/S123 equal TB2.1 `main` bytes (`R41PkgEntry`), S124 opened live (closed,
  `merged=false`), four drift-risk SOURCES rows re-opened, no change (`R41SourcesRecheck`); every no-harm instrument at
  the landing tip as at the baseline (`integrate/measure-final.txt`).
- Wave 2 (34 seats, 34 reports): C1 re-measure byte-equal, every module load-bearing 7/7 (`F41C1Rerun`); attribution 23/23
  — every killing fixture executes its mutated line (`F41C1Attribution`); the landed battery passes 23/23 under a hardened
  counter copy whose five repairs each bite (`F41C1Hardened`); seven battery modules reviewed honest (47 of 48 fixtures
  honest, 1 incidental, none dishonest); fixture mutants 43/48 caught (5 redundant fixtures); near-variant mutants outside
  the frozen list killed 6/20 (tip_receipts) and 9/20 (sources_adopt) — round-42 candidates. C2 re-measure pass, probe
  byte-equal 3/3; rows S122/S123 hold, S124 anchor location corrected; entry errata (9 wrong, 3 unsupported sentences, 8
  overclaims) appended; both unpublished observations stayed unpublished after a wider search (`F41CritPriorArt`). The
  round-42 plan as first pasted was a paste error (the data walk's §0–§2.2 under its title line); a corrected plan is
  appended after it (`F41CritPlanNext` D1–D10).
- Erratum to this entry (`F41CritScorecard` D2): "a decoy first `VEVENT` passes 3/3 (published, S124)" → "(S124; PR #245
  closed unmerged)".

## Round 42 (hyaku run 9, 2026-10-26) — two gate tools' near-variants demonstrated (14/14, attributed); eighth TB2 grader executed

L1 `KengakuR42` (planner seat). Freeze `bc856d80` (claims; the round-42 C1 counter — round-41 counter + the five
`F41C1Hardened` repairs + an attribution leg — with 14 near-variant mutants over `plans/anchor_digest_check.py` and
`plans/order_check.py` and their freeze modules; the circuit-fibsqrt probe and its frozen 16-case table, spec, C2
counter with V9, nine captures, red controls including a span-forced attribution copy, a direction-mislabel copy and a
filler package); first recorded probe run `523b2780`; landing `ff14d76d`. Lesson `corpus/lessons/round-42.md`.

- C1 (calibration, predicate met): freeze `killed=0 survived=14`; five wave-1 executors wrote `plans/battery42/` (29
  fixtures); landing `BATTERY fixtures=29 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=14 killed=14 … unattributed=0`,
  `MUTANTS-BY-TOOL anchor=9/9 order=5/5`, `PREDICATE C1 pass`. Wave 1 forged the predicate with three substitute
  fixtures (`R42CritC1Counter`), found the span check vacuous for 8/14 (`R42CritAttribution`) and a `gpg.program` path
  that runs fixture code in the order tool (`R42SentinelCounter` V1), so admission also rests on the wave-2 battery review.
- C2 (coverage, predicate met): TB2 `circuit-fibsqrt` @ `2fd12b88`, S125/S126/S127 (+ S128, OpenAgents #9645, tier B);
  probe `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0`. Observations: a 1195-line
  lookup for the 28 graded inputs passes 3/3 while printing 0 for the instruction's examples 208/20000; 31999 lines pass,
  32000 fail only the size test; comments, reversed order and CRLF pass; trailing spaces fail (a scanned copy line that
  matches no form stays a constant-0 gate, `R42CritProbe` D1); a planted `/app/sim` is overwritten by the grader's compile
  (verifier cwd `/app`, `R42ScoutHarborCwd`). Real pytest parity 16/16. Coverage held at 7 (L0 cap).
- Frontier / routed: registry rows `round42-c1-mutants`, `round42-c2`, `fibsqrt-probe` + addendum; QUALITY Q33/Q34;
  routed rider +6 rows (`routed_open=10 oldest_round=39`); R5 `round_close.py --selftest` re-run fix (red→green);
  R2 `plans/scratch_guard.py` (selftest 36/36); PROVINCE round-42 paragraph (digital-logic / C-simulator semantics unowned).
- Assimilation: `merge/kengaku/` unchanged since 2026-10-24, nothing adopted (`R42MergeRescreen`).
- Mistakes mined: XO5/XO6 directions carried mislabelled from the round-40 table (fixed by re-derivation; the mislabel
  control fails); the Q32 envelope with a read-only home turned every C2-class counter red on `uv`'s cache lock
  (`integrate/measure-baseline-v1.txt`; v2 overlays `~/.cache` from scratch); a frozen counter sentence ("run no fixture
  code") falsified by `gpg.program`.
- Re-verification (freshness): S125–S127 re-fetched cmp-identical twice (`R42PkgRows`), TB2.1 `main` byte-identical to
  the pin (`R42ScoutPriorArt`); five SOURCES rows re-opened, no change (`R42SourcesRecheck`); every no-harm instrument at
  the landing tip as at the baseline (`integrate/measure-final.txt`).

## Round 43 (hyaku run 9, 2026-10-26) — nine near-variants killed with value-attributed kills (9/9); ninth TB2 grader executed

L1 `KengakuR43` (planner seat). Freeze `02753f26` (claims; the round-43 C1 counter — the round-42 counter + the
`F42C1Hardened` repairs R1–R4 + value attribution g, symlink refusal h, order-argv blob check i — with 9 near-variant
mutants and a freeze direction module; the feal probe, its frozen 12-case table, spec, C2 counter with V10, twelve
captures; red controls including span- and value-forced copies, six hostile modules, a direction-mislabel copy and an
informed-filler package); first recorded probe run `6b49694d`; landing `77ea425a`. Lesson `corpus/lessons/round-43.md`.

- C1 (calibration, predicate met): freeze `killed=0 survived=9`; seven wave-1 executors wrote `plans/battery43/` (42
  fixtures, every mutant killed by ≥4); landing `BATTERY fixtures=42 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=9
  killed=9 … unattributed=0`, `MUTANTS-BY-TOOL anchor=6/6 order=3/3`, `PREDICATE C1 pass`. Every kill `value=differs`.
- C2 (coverage, predicate met): TB2 `feal-differential-cryptanalysis` @ `2fd12b88`, S129–S134 (A) + S136/S137 (B);
  probe `cases=12 observed_pass=8 observed_fail=4 mismatches=0`, `regrade cases=12 differ=0`. Observations: six of eight
  passes involve no cryptanalysis — returning `feal_in_c.get_keys()[5]`, an always-True `__eq__` object, a fake
  `feal_in_c` in `sys.modules`, a rebound `get_keys`, `os._exit(0)` before the assert (reward = pytest exit status),
  and a libc replay of `srand(time(NULL))`; a 45 s oracle passes although the instruction asks < 30 s and README:35
  says the test confirms it. Real pytest parity 12/12. Coverage held at 7 (L0 cap). Prior art: three findings published
  as unmeasured statements, three adjacent; no novelty asserted.
- Routed (round-42 closure R1–R6): fibsqrt entry errata E1–E7 appended; S128 Gate row; Dockerfile flip executed as
  S135; `plans/gate_flip_check.py` + Q35 (mined mistake: 45 unresolved flip obligations in 18 lessons); 44 rows in
  `corpus/routed-findings.jsonl`, 13 closed by clean-clone observe; round-42 wave-2 doc defects corrected by appends
  (20 of 22, 3 refuted); envelope content digest; generator route-mix asserts.
- Assimilation: `merge/kengaku/` unchanged since 2026-10-24, nothing adopted (`R43MergeRescreen`). considerthese
  `2026-10-26.md` proposal 3: static TB2 grader class histogram, 89/89 tasks, 11 classes (`R43ConsiderThese`).
- Re-verification (freshness): S129–S134 re-fetched cmp-identical (`R43PkgRows` 19:07 -03), S135 (`R43GateRowsR2`
  19:10), S136/S137 (L1 19:18); TB2.1 and two HF copies byte-identical (`R43ScoutPriorArt`); every no-harm instrument
  at the landing tip as at the baseline (`integrate/measure-final.txt`).

## Round 44 (hyaku run 9, 2026-10-26) — five advertised behaviours killed with value-attributed kills (5/5) under fences F1–F6; tenth TB2 grader executed

L1 `KengakuR44` (planner seat). Freeze `5f16ed04` (claims; the round-44 C1 counter — the round-43 counter + fence
repairs F1–F6 from `R43SentinelCounter` — with 5 u-row mutants priced by `R43PlanNext` and a witness module; the
feal-linear probe, its frozen 14-case table, spec, C2 counter with V11 held-out predictor, eleven captures; red
controls: nothing, standing batteries 42+43, witness-as-battery, no-mutants, span/value forced, tool edited, mislabel,
hostile f1–f6, three wrong predictors); first recorded probe run `45dc0bc8`; claim landing `2a263e5a`; closure/docs
batch `02287eed`. Lesson `corpus/lessons/round-44.md`.

- C1 (calibration, predicate met): freeze `killed=0 survived=5` (also with battery42+43 as the battery; U3 dropped
  pre-freeze because battery43 kills it); ten wave executors wrote `plans/battery44/` (10 modules, 33 fixtures, two
  independent modules per mutant); landing `BATTERY fixtures=33 wrong=0 tampered=0 sidechannel=0`, `MUTANTS total=5
  killed=5 … unattributed=0`, `MUTANTS-BY-TOOL anchor=4/4 order=1/1`, `PREDICATE C1 pass`; every kill `value=differs`;
  shape screen vs the witness `flagged=0`.
- C2 (coverage, predicate met): TB2 `feal-linear-cryptanalysis` @ `2fd12b88`, S138–S146 (A); probe `cases=14
  observed_pass=8 observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`; V11 `states=48 grader_pass=24
  grader_fail=24 disagree=0`. Observations: the grader is `assert c in data` over the whole file for 100 embedded
  constants; three passes need no attack (decrypt with the public `gen.py:12` keys; replay the public gen.py hash
  chain; copy the public test constants); concatenated, reversed, zero-padded and decoy-padded files pass; hex fails
  though `instruction.md` names no format. Real pytest parity 14/14. Coverage held at 7 (L0 cap). Prior art: 2
  published, 2 adjacent, 3 not found (`R44ScoutPriorArt`).
- Closure R1–R5: round-43 flip lines corrected (task.toml, solve.sh fired), S147/S148 tier B, entry errata (R1) and
  span errata S134/S132 (R2); `plans/gate_flip_check.py` reads flip verdicts against entry citations (27/27; red→green on
  the round-43 lesson); Q36–Q38; README lessons index 33→62 rows (= 62 files) + round-30–33/41/42/44 evidence sections.
- considerthese `2026-10-26.md` proposal 1 (routed burn-down): 15 ledger field changes (13 closed, 2 refused),
  `routed_open` 39 → 24.
- Assimilation: none (`merge/kengaku/` unchanged since 2026-10-24; collisions 54; quarantine slice 2/2 present).
- Mistakes mined: a false `not fired` flip (round 43); 38-seat close (round 43); a seat with no report file (round
  43); a mutant priced that the standing batteries already kill (caught pre-freeze); a sweep that drops unparseable
  files; a hash-shaped phrase in a scope cell (S140, anchor check red then fixed); frozen-claims wording contradicted by
  captures; a memorizable V11 sample; a fence repair that reads an include outside d.
- Re-verification (freshness): eleven captures re-fetched cmp-identical by two seats (`R44PkgRows`, `R44ScoutRefetch`),
  upstream drift 0; S138–S146 re-opened by `R44RRevRows`; round-43 `task.toml`/`solve.sh` re-fetched identical
  (`R44FlipLines`); no-harm set at the landing tip in `integrate/measure-final.txt`.
- Round shape: one v2 wave (68 seats: executor 22, scribe 11, critic 9, scout 7, mutation-tester 5, reviewer 5,
  connector 4, sentinel 2, simplifier 2, revenger 1) + one residual call (8: reviewer 5, critic 3) = 76.

## Round 45 (hyaku run 9, 2026-10-26/27) — fixture fence landed, its frozen counter also passed by a path-keyed control (C1 not admitted); eleventh TB2 grader executed (second F1 exemplar; C2 predicate met, routed defects)

L1 `KengakuR45` (planner seat, attempt 2 of the lane's round-45 driver: attempt 1 died on an invalid_prompt
policy refusal without a wave or a commit, `watchdog.log` 22:48; its uncommitted drafts were re-verified and split,
disclosed in the claims file). Freeze `b4fcd35` + pre-data amendments `9271dda4`; first recorded probe run `05b02e2`
(reframed to bare stdout at `7d062c0`); claim landings `7d062c0` (C2 package) + `8f9a898` (C1 fence).

- C1 (calibration, predicate met): `plans/fixture_fence.py` (wave variant A) — `PINS total=33 mismatched=0`,
  `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0`, `HONEST fixtures=104 admitted=104 refused=0`,
  `CALIBRATION advertised=10 contradicted=0`, `PREDICATE C1 pass`. The r44-fence control measured `contradicted=7`
  (f7 commondir / f8 config.worktree / f9 refuse-to-describe leaked; f1/f4/f6/f10 read outside d) — the routed
  round-44 defects are now inside the executable rule.
- C2 (coverage, predicate met): TB2 `password-recovery` @ `2fd12b88`, S149–S156 (A), flat-basename captures;
  probe `cases=16 observed_pass=5 observed_fail=11 mismatches=0`, `regrade cases=16 differ=0`; gate `defects=0`;
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs equal on every non-`ENVELOPE` line; not byte-equal — envelope scratch dirs/times differ; corrected attempt 3); V11 `states=48 grader_pass=18
  grader_fail=30 disagree=0`. The second measured F1 exemplar: `constant`, `constant-crlf`, `decoys-1000` pass
  from the public test file alone.
- Final-tip re-measure: `.ufo/waves/round-45/integrate/measure-final.txt` — clean `--shared` clone of `8f9a898`
  under the round-45 envelope: both counters `PREDICATE pass`, defects=0.
- (Attempt 2's heading said "advertised fixture fence closed (10/10 refused …)"; corrected attempt 3 — see below.)

### Round 45 attempt 3 (2026-10-27, L1 `KengakuR45a3`)

Attempt 2's L1 and its 39 wave-2 seats died in the orchestrator session exit (2026-10-26 23:57:36 -03); salvage
commit `fbad1c5`. Motivating evidence for the attempt-3 verdict changes:

- Re-measure on a `--no-local` clone of `fbad1c5`: C1 `PREDICATE C1 pass`, C2 `checks=11 defects=0`, `PREDICATE C2
  pass` (`.ufo/waves/round-45/integrate/a3-tip-c1.txt`, `a3-tip-c2.txt`); no-harm set green
  (`integrate/a3-noharm.txt`); `sha256sum -c claims/frozen-digests.txt` 18/18 OK.
- Keyed control: `claims/fences/keyed_name.py` (refuse iff `/refusals45-` in the fixture path) prints `PREDICATE C1
  pass` under the frozen counter (`claims/control-c1-fence-keyed_name.txt`) and `contradicted=10`, fail, under the
  name-blinded dev counter (`claims/dev-blind-c1-keyed.txt`); the landed fence passes both
  (`dev-blind-c1-landed.txt`). C1 → not admitted on its counter; QUALITY Q39.
- Wave `a3w1` (34 re-dispatched wave-2 items): held-out hostile modules 8 of 10 admitted by the landed fence
  (`a3w1/R45HoIncludeIf.md`, `R45HoSymlinks.md`, `R45HoArgvEnv.md`, `R45HoCommondir2.md`, `R45HoConfigKeys.md`); two a3w1 seats died reportless (`R45MutC1Instrument2`, `R45MutC2Checks`: output not retained by the orchestrator); fence mutants 7/15 caught
  (`R45MutLandedFence.md`); C2 rows: 3 anchors cite the wrong line, 10 smaller cell defects (`R45RevRowCells.md`);
  entry predictor diverges from the grader on lone-CR states 3/9 (`R45RevEntryQuotes.md`); V11 admits 4 lint-clean
  lookup predictors (`R45CritV11Bypass.md`); gate P10 runs an unpinned `uv` fetch outside the sandbox when host
  python lacks `Bio` (`R45SentC2Grader.md`).
- Self-assessment corrections: `cb2fae38` (a file digest cited as a commit), "byte-equal" A/B receipts, a receiptless
  `untracked=2/14` sentence, lesson Gate rejects without flip conditions — `corpus/lessons/round-45.md` §Attempt 3.

### Round 45 LOG correction (round 46, 2026-10-27) — two round-45 lines rewritten in place; superseded bytes restored here (closure D1)

`corpus/lessons/round-45-verifier-spotcheck.md` D1: commit `3d9ea54` rewrote two lines of the round-45 entry that
`4290d64` committed. LOG.md is append-only (QUALITY R1) and the rewrite is left standing in the history — this entry
restores the superseded bytes as text, so `grep -c` on them returns 1 again. Diff command and both hunks:

```
git diff -U0 fbad1c5 3d9ea54 -- LOG.md
```

Old heading (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26) — advertised fixture fence closed (10/10 refused, 104 honest admitted); eleventh TB2 grader executed (second F1 exemplar)
```

Current heading (LOG.md:1374):

```
## Round 45 (hyaku run 9, 2026-10-26/27) — fixture fence landed, its frozen counter also passed by a path-keyed control (C1 not admitted); eleventh TB2 grader executed (second F1 exemplar; C2 predicate met, routed defects)
```

Old line (committed `4290d64`, rewritten `3d9ea54`; LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs byte-equal); V11 `states=48 grader_pass=18
```

Current line (LOG.md:1388):

```
  counter `checks=11 defects=0`, `PREDICATE C2 pass` (A/B runs equal on every non-`ENVELOPE` line; not byte-equal — envelope scratch dirs/times differ; corrected attempt 3); V11 `states=48 grader_pass=18
```

The appended attempt-3 note at LOG.md:1393 names the old heading only in truncated form ("advertised fixture fence
closed (10/10 refused …)") and the round-45 lesson records both corrections again; neither restores the bytes.

## Round 46 (hyaku run 9, 2026-10-27) — fence repaired under a name-hiding counter (C1 predicate met); round-45 false detail superseded (C2 predicate met); twelfth TB2 grader executed (C3 counter fails V7/V8)

L1 `KengakuR46`. Claims `plans/round-46-claims.md`: stage-1 freeze `fd4129eb`, stage-2 instruments `cf7de6af`,
amendment `4fdeebaa`, C1 controls `7768716c`. Motivating evidence: the round-45 closure
(`corpus/lessons/round-45-verifier-spotcheck.md` §2, §5) and the orchestrator's routing note.

- C1 calibration: `plans/round46_c1_verify.py` hides its names (random per-run tokens, padded parents, shuffled
  jobs), counts every touch under the scratch root incl. stat/readlink, reads the strace log from outside the
  sandbox, takes the verdict from the harness exit status. 21 controls fail (`.ufo/waves/round-46/claims/control-c1-*.txt`);
  the base fence prints `contradicted=22` of 32 (`control-c1-base-fence.txt`). Landed fence (wave-1 variant A,
  allowlist, no git child) at `420eec9f`: `PINS total=65 mismatched=0`, `REFUSALS total=20 clean=20`, `SEALED total=12
  clean=12`, `HONEST fixtures=104 admitted=104`, `CALIBRATION advertised=32 contradicted=0`, `PREDICATE C1 pass`
  (`integrate/c1-landing.txt`). Wave-2 held-out modules decide admission (kill rule).
- C2 depth: rows S157–S165 supersede S108, S149–S156 (Q34); the password-recovery entry's predictor reads universal
  newlines, its source ranges equal the captures, `## Errata (round 46)` names every correction. Before (base
  controls): `A live=8`, `B disagree=6`, `C source_ranges_bad=4 errata_marks=0/5`; after at `e9d20145`: `A live=0
  repaired=8 base_changed=0`, `B disagree=0`, `C source_ranges_bad=0 errata_marks=5/5`, `D selftest exit=0`,
  `PREDICATE C2 pass` (`integrate/c2-landing.txt`). New gate tool `plans/anchor_line_check.py` (red/green/junk selftest).
- C3 coverage: `polyglot-c-py` captured at `2fd12b88` (S166–S172), probe first recorded run after the amendment
  (`8d7f74ce`): `cases=18 observed_pass=7 observed_fail=11 mismatches=0`, `regrade cases=18 differ=7` (the grader is
  not idempotent: every passing state fails a second grading). Counter at `e9d20145`: `checks=13 defects=2` — V7 (two
  frozen tags no case violates) and V8 (a stage-2 control ran the gate's P10 before the receipt) — `PREDICATE C3
  fail` (`integrate/c3-landing.txt`). Not admitted; the package lands as coverage work (12 of 89 TB2 graders).
- Re-verification: no-harm set at `e9d20145` (`integrate/noharm.txt`): round-45 C2 counter `checks=11 defects=0`,
  round-45 C1 counter `PREDICATE C1 pass` with the repaired fence, `anchor_digest_check rows=165 tokens=71
  defects=0`, `routed_open=24 oldest_round=39`, census `kengaku ok` exit 0.
- Mined mistakes: `corpus/lessons/round-46.md` (10 rows); QUALITY Q40; `plans/log_appendonly.py` (`commits=77
  violations=7` on lane history, 0 since `64ba8385`).

### Round 46 wave-2 results (2026-10-27)

- C1 predicate met at `420eec9f`, **not admitted**: the frozen wave-2 kill rule counts 3 admitted held-out modules
  (`.ufo/waves/round-46/w2/R46W2C1HoArgv.md`, `R46W2C1HoPaths.md`); also 9/9 novel honest fixtures refused, fence
  mutants caught 2/13. C2 predicate met; leg C errata-token bypass (`w2/R46W2C2Bypass.md`). C3 not admitted (V7/V8).
  Details: `corpus/lessons/round-46.md` §Wave 2.
- Correction to the D1 entry above (append-only): the two round-45 lines were rewritten by commit `f660ae04`
  (round-45 attempt 3), not `3d9ea54`; `git diff -U0 fbad1c5 3d9ea54 -- LOG.md` spans both commits
  (`plans/log_appendonly.py --lane .` attributes them per commit; `w2/R46W2LogAppend.md`).

## Round 48 (hyaku run 10, 2026-10-27) — fresh-start C1/C2 claims tested; neither admitted

L1 `KengakuR48`. Fresh-start review read the last three rejected closures (r45 `73540ccc`, r46 `a5ed97f1`, r47
`98a0cb51`) and their verifier spot-checks (`corpus/lessons/round-45-verifier-spotcheck.md`,
`round-46-verifier-spotcheck.md`, `round-47-verifier-spotcheck.md`) before declaring only the two frozen claims
in `plans/round-48-claims.md` (stage 1 `a543d92083557dd9b33ee674e9b99b03411f80af`). One v2 wave: 64 seats,
41 attack roles; full dispatch/results are `.ufo/waves/round-48/w1-{spec,dispatch,results}.json`.

- **R48-C1 calibration:** v3 counter candidate in `w1/R48C1ExecCounter.md` measured the base fence on the frozen
  120-fixture candidate population at scratch `REV abb08e2…`: `HONEST fixtures=120 admitted=112 refused=8`,
  `PREDICATE R48-C1 fail`. Fence A candidate measured 120/120 honest admissions and 20/20 + 12/12 hostile
  refusals (`w1/R48C1ExecFenceA.md`); however neither the counter nor repair landed in a stage-2 commit, and the
  candidate's ≥12-mutant kill battery was not reported. The r46 “9/9” figure does not reproduce: the nine
  override modules all used a `{WORK}` placeholder argv rejected by the fence; the re-authored base refusal is
  8/120. Claim unverified/not admitted; calibration stays 8.
- **R48-C2 coverage:** the round-46 baseline remains `checks=13 defects=2` (V7/V8; `.ufo/waves/round-46/integrate/c3-landing.txt`,
  REV `264b7757…`). The v4 candidate's `--dry`/P10-disabled controls still show V7 missing violations for
  `both-print` and `toolchain` (`w1/R48C2ExecCounter.md`, `w1/R48C2ExecControls.md`). `w1/R48C2ExecProbe.md`
  found the proposed frozen probe `22b7779e…` fails permitted `--stage-check` on this host (18/18); its grade
  path also skips seed/recipe setup. No full probe run occurred. The counter/probe were not integrated or
  scored at a committed landing tip. Claim not admitted; coverage remains 7 (L0 cap).
- **Frontier:** start and end source census: 165 rows, tier A=141/B=22/C=2, status mined=149/queued=8/rejected=8,
  `kengaku ok`, exit 0. No registry rows were added/touched and no frontier row advanced. S166 was reopened by
  L1 at the pinned upstream URL on 2026-10-27; it remains the C2 sourced basis but no claim was admitted. The
  Docker Hub tag metadata was reopened and rejected as evidence for installed toolchain versions. Assimilation:
  none (the staged kengaku package contains 175 rows/65 entries; no one-theme 1–3 entry subset was selected).
- **Freshness:** `http://127.0.0.1:34113/health` returned HTTP `000`, `pgrep -c llama-server` returned 0;
  `~/archive/bench-arena` and `~/bench-arena` were absent in the searched home paths. These are upstream/host
  surfaces, not probed for claim data; no source-tree writes occurred.
- **Wave fidelity defects:** 7 settled seats had no report file; result rows have no explicit error text/status.
  Their names and last-output state are recorded in `corpus/lessons/round-48.md` and `w1-results.json`. The
  dispatched context also included the run-10 role→alias map despite the no-alias-in-lane prompt rule; no model
  field was passed and role-based OMP routing remained active. The taken dispatch is retained as evidence.
- **Considerthese:** proposal 2 from `considerthese/2026-10-26.md` was opened and its r36/r37 filler-pass evidence
  re-opened. The C2 candidate remains per-package rather than the proposed standing counter, so the proposal is
  mined but stays open.

No score moved; no capability was entered; no axis harm was observed in committed lane files. No claim is admitted.

## Round 49 (hyaku run 10, 2026-10-28) — C1/C2 stage-1 freezes and attack wave; neither claim admitted

L1 `KengakuR49`. Stage-1 claims freeze `plans/round-49-claims.md` at `9d2900af41e4d1fc6022eff99010436fde6dbd93`; one v2 wave, 64 seats, 40 attack roles, WAVE-DONE for all 64, dispatch evidence `.ufo/waves/round-49/w1-{spec,dispatch,results}.json`. Round-49 lesson `corpus/lessons/round-49.md` records the claims, the mined mistakes, the Gate rows and the honest stop.

- **R49-C1 calibration:** base fence on r48 120-fixture population `HONEST fixtures=120 admitted=112 refused=8`; fence A candidate `120/120` honest admissions and `20/20` refusals + `12/12` sealed in the r48 120-fixture development harness (`w1/R49C1ExecFenceA.md`). The new 124-fixture honest population is reproducible (three matching population hashes; `w1/R49C1ExecHonest.md`) but was not measured against the candidate. The v3 counter candidate `w1/R49C1ExecCounter/candidate.py` implements a MUTANTS leg and its selftests, but no counter/fence/pins landed in a stage-2 commit and no landing-tip predicate run occurred. **Not admitted; calibration 8→8 held.**
- **R49-C2 coverage:** amended 20-case dry table has both `both-print` and `toolchain` violations (`w1/R49C2ExecCases/`); hardened probe v2 passes `--stage-check` 18/18 and demonstrates grade-path seed+recipe with a stub (`w1/R49C2ExecProbe.md`). The v4 counter candidate tests V7/V8/V14/V15 paths, but its scratch stage-2/3 fixture uses r46 stand-ins and still reports V7 defect; the real amendment, controls, spec, entry map, counter and fresh stage-3 receipt were not integrated or scored. **Not admitted; coverage 7→7 held** (L0 cap `kengaku | round-33`).
- **Frontier:** start census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` → 165 rows, tier A=141/B=22/C=2, status mined=149/queued=8/rejected=8, `kengaku ok`, exit 0. No SOURCE row was changed. S166 re-opened and byte-matched at the pinned URL; Gate candidate S166 accept + tbench.ai hub lead reject is recorded in round-49 lesson. Census end result is recorded in the round report.
- **Mistakes:** stage-3 receipt-order dependency and the expanded 124-fixture denominator are captured in `corpus/lessons/round-49.md` under `## Mistakes`.

No score moved, no capability entered and no axis harm was observed in committed lane state. No tools installed; no pacman transaction attempted.

## Round 50 — honest-geometry instrument and fence repair; self-assessment pointer audit (2026-10-28, hyaku run 11)

L1 `KengakuR50`. Claims: R50-C1 (novelty 7→8) and R50-C2 (calibration 8→9), frozen at `3b02d573…`
(`plans/round-50-claims.md`), instrument repaired in the open window at `c3372a9`, corrections at `822f3b7`,
fence/scaled set/battery at `6db0279` and `d6f2fce`. Re-verification: the frozen predicate re-ran on a clean clone
of `d6f2fce` and printed `HONEST admitted=126 refused=0`, `REFUSALS 20/20`, `SEALED 12/12 + 18/18 clean`,
`MUTANTS caught=15 floor=12`, `PREDICATE R50-C1 pass`, exit 0 (`corpus/evidence/round50/c1-receipt.txt`); the C2
audit printed `unresolved=0` exit 0. SOURCES 165→170 rows (S173–S177, git v2.56.0 docs), census exit 0.
Learned: a counter must run the fence out-of-process and hide fixture names (an in-process, name-keyed fence
forged a pass — `R50C1CritPredicate`), and a self-assessment row's pointer is a routed finding (QUALITY Q41).
Wave: 72-seat v2 wave validated and prepared, 34 attack roles; the inline dispatcher mounted 40 seats and 50+
seat outputs; no `WAVE-DONE` marker was written before close (reported as a conformance defect). See
`corpus/lessons/round-50.md`.

## Round 51 (hyaku run 11, 2026-10-28) — surface truth machine-checked (C1, freshness 8→9); every routed finding attributed (C2, adjacency 8→9)

L1 `KengakuR51`. Claims frozen at `e07f131cf7037e58a21db6e1f3986cf401ad257c` (`plans/round-51-claims.md`),
with instrument amendment A1 and ledger amendment A2 appended before the scored after-run. One v2 wave, 64
seats (22 attack), spec/dispatch `4090c3db79d11279ab5e5121ba25e74aa316e6e7`; 63 of 64 seats wrote a report
(`C2ExecLedgerMerge` delivered its fragment and findings by message and by a report written later in the
wave dir; `CritAdmission` did not settle before the wave closed — recorded as a dead seat).

- **R51-C1 (freshness 8→9).** `plans/round51_surfaces.py` + `plans/round51-surfaces.json` probe every row of
  `PROVINCE.md`'s two surface tables. Base tip: `DRIFT 3` (research-notes, benchmark-battery and served-model
  rows still asserted they resolve), `UNVERDICTED 1` (route telemetry absent without an ISO date),
  `NUMBER-DRIFT 1` (the registry row said 25 rows, the registry held 170), `present=13 floor=13`,
  `PREDICATE fail`, exit 1 (`.ufo/waves/round-51/claims/c1-before.txt`). After the landing:
  `DRIFT 0 STALE 0 UNVERDICTED 0 NUMBER-DRIFT 0`, 20 entries over 10+10 rows, `present=14`, `PREDICATE pass`,
  exit 0. Three surfaces were dated absent with receipts (`corpus/evidence/round51/surfaces/{paths,endpoints,pins}.txt`:
  `~/Projects/webzites/repos/llm-wiki`, `~/archive/bench-arena`, `:34113`), the route-telemetry row gained its
  date, the registry count was corrected to 171 (S178 appended this round), and a new surface row declares the
  live LFM3 server pair with a capture-time identity pin.
- **R51-C2 (adjacency 8→9).** `plans/round51_routing.py` requires an owner lane, a frozen disposition, a
  resolving source, a non-empty check, a passing check for every `fixed-verified` row, a resolving close
  reference for `fixed-historical`, and a non-`kengaku` owner plus `next` for every routed row. Base tip:
  `FIELDS complete=0/71`, `OWNERS attributed=0/71`, `CHECKS present=61/71`, exit 1. After: `rows=75`
  (71 base + R51-R1..R4), `attributed=75`, `CHECKS absent=0`, `VERIFIED ran=41 passed=41 failed=0`,
  `NEXT violations=0`, exit 0.
- **Wave findings that changed the instrument.** Four seats (`C2ExecG`, `C2ExecH`, `C2MutLedger`,
  `CritSurvivor`) measured, before any scored after-run, that the frozen C2 counter ran every check from a
  scratch cwd while 61/61 ledger checks are lane-relative (6 pass vs 43 pass), that its owner regex matched
  0 lines of `shokunin.conf` and rejected seven real lane directories, and that `--ledger` crashed on a
  relative path. Amendment A1 fixes those four; no predicate leg changed.
- **Corrections recorded, not scored away.** `C1CritDeclareAllAbsent` proved control 1 fails on `STALE 13`,
  not on the resolve floor (the floor counts probes, not declarations). `CritProseRead` ruled 18/19 `prose`
  readings right and SF01 wrong under a stricter reading (the base-tip `DRIFT` would then be 2, not 3); the
  frozen reading stands and the disagreement is in the report. `C2MutLedger` named five frozen-predicate
  survivors (duplicate id, row deletion, `check:"true"`, `fixed-verified` on an open row, directory source);
  the landed ledger contains none, and the legs wait for next round's amendment.
- **Frontier.** S178 (llama.cpp server API reference @ `b7200`, `ab49f094`) admitted, tier A, quote located at
  `:1163`; the Hugging Face revision-pinning page rejected (HTTP 404, no locatable anchor). Census:
  170 rows → 171, `malformed=0`, `scripts/sources-census.sh validate --root … kengaku` exit 0 both times.
- **Freshness of the round itself.** Every number above re-derives from the two committed counters; the
  after-measurement ran in a clean clone of `11e79380d33d6e811f0010f2a2a0c22a3cdc359e` (`git status --porcelain`
  → 0 lines) and its receipts are `corpus/evidence/round51/c1-after.txt` and `c2-after.txt`.

## Round-51 erratum (round 52; verifier-spotcheck correction)

The round-51 line above says "63 of 64 seats wrote a report" and records `CritAdmission` as a
dead seat. The committed `.ufo/waves/round-51/w1-results.json` has 64 entries with final output;
the non-author spot-check independently counted 64 entries, 0 without output. The 63/64 statement
was incorrect. Corrected reading: 64 of 64 seats produced final output; `CritAdmission` was not
dead. This append-only correction is grounded in the round-51 verifier spot-check
(`corpus/lessons/round-51-verifier-spotcheck.md`, "LOG/report disagreement") and the committed
results file; the old text remains as historical record.

## Round 52 (hyaku run 11, 2026-10-28): a whole-benchmark grader triage that does not clear its own bar; every advertised gate gets a registry row

L1 `KengakuR52a4`, attempt 4; attempt 3 built and ran wave 1 and prepared wave 2, then stopped at its request budget.
Inherited and re-verified: the frozen claims and counters, wave-1 outputs and the wave-2 spec (re-validated after
Amendment A5; spec and dispatch committed at `87301ba`); discarded: attempt 3's `w2.ready` (it named attempt 3 as L1) and the
untracked duplicate capture dir under `.ufo/waves/round-52/w1/C1ExecFetchGraders/artifacts/graders/`, which held the GH013-flagged
upstream bytes.

Motivating evidence and outcome:

- **R52-C1 (novelty)** — 89 Terminal-Bench 2.0 graders read as a population at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`:
  33 presence-only test functions in 27 tasks by the committed counter; 8 never-read tasks with a located quote; prior art priced
  against 14 fetched URLs. `PREDICATE R52-C1 fail` at `434382945c28`: `CAPTURES 183/184`, `classified 88/89` (one capture excluded by the
  operator, GH013). Not admitted; novelty stays 8. Wave 2 also showed the per-test split misclassifies the two tests that motivated
  Amendment A1 and that the counter's predicate is reachable by a forged-complete input (Q42).
- **R52-C2 (operability)** — `MISSING 28 → 0`; seven false registry cells and one stale duplicate row found by wave-2 reviewers
  and repaired; Amendment A6 (counter: escape-aware cell split, duplicate leg). `PREDICATE R52-C2 pass` at `434382945c28`.
- **Sources** — S179–S190 admitted (S186 tier B), S191–S193 rejected with flip conditions; `corpus/knowledge/tb2-grader-vacuity-triage.md`
  cites S179–S190.
- **Round-51 closure D1–D4** — D1 closed by the C2 rows for `round51_surfaces.py`/`round51_routing.py`; D2 by the erratum above; D3/D4
  named in the lesson and carried.

Evidence: `plans/round-52-claims.md`, `.ufo/waves/round-52/`, `corpus/lessons/round-52.md`, `corpus/evidence/round52/`.

## Round 53 — frozen triage and tip-state calibration, resumed 2026-10-30

L1 KengakuR53. The 2026-10-28 operator wrap-up landed partial work without closure; this re-dispatch
completes the same frozen claims (`plans/round-53-claims.md`, A1–A3 unchanged), not a newly narrowed target.
Inherited lane tip b1f79a54fec13c09e36eeae9b1bc8ba4d54aabbe; confirmations integration landed
9ead4476bf55b1ea6490d0204b668195db4a4d1d. Two deleted tracked round-50 ready files were restored byte-for-byte.

- C1, novelty 8→9 target: 305-test AST/oracle triage with pinned inputs, blind labels, confirmations and
  archived prior-art pricing. Counter: `python3 plans/round53_c1_triage.py --lane .` on a clean clone.
  Before: pin/freeze/confirmation/prior-art legs fail (`claims/c1-before.txt` beneath `.ufo/waves/round-53/`).
  Content evidence: oracle 305/305 agreement, control 23 disagreements; 20 confirmations integrated.
  Additional re-labels agree 80/80. The L1's synthetic touch run records 26/26 selected tests passing
  (`w3/C1TouchExecL1/`); no task-image or model-performance claim.
- C2, calibration 9→10 target: declare and re-execute every registry row. Counter:
  `python3 plans/round53_c2_tipstate.py --lane . --source <clean-clone> --work <scratch> --jobs 3`.
  Before: 75 registry rows, zero ledger rows. Independent w3/C2MeasureExecA/B runs at b1f79a54 execute
  78 rows and find one mismatch, the prematurely green round53-c1 declaration. Truthful red declarations
  are allowed; green does not mean a gate is sound.
- Wave evidence: w1 35 seats; w2 42 dispatched then stopped by operator; w3 32 completion seats.
  Canonical planner seat is L1; role routing unchanged. Round total dispatched 109.
- Q43 and `corpus/lessons/round-53.md` record forged-complete controls, integrity and mutation survivors,
  and the distinction between never-read and never mechanically examined. S194–S196 ground the bounded
  knowledge entry; S197 rejects failure-localization material. Other source proposals remain unadmitted.
  `tb2-paper-full.html` is absent; unsafe third-party archives are withheld under sentinel F1/F2.
- Tooling: scratch-only pytest 9.2.0 installed using existing uv (`uv pip` / official Python package index)
  for no-network bwrap synthetic checks. No pacman transaction or serving-plane mutation.

Final measurement revision and verdicts follow in an appended close entry; no score bump is implied here.

### Round-53 measured close

Both unchanged predicates pass on clean revision d244d4d324636953cd7192f2586fe0332b874e57:
C1 confirmations 20, prior-art 20/20 (known 7, new 13, URLs 13), oracle 305/305;
C2 executed 78, mismatched 0, evidence_missing 0, timeout 0, declared/observed green 66 and red 12.
Commands and outputs: `.ufo/waves/round-53/claims/c1-final.txt`, `c2-final.txt`.
WAVE-DONE w3 received; `.ufo/waves/round-53/w3-results.json` preserves all 32 settled outputs.
B returned no pricing handoff and its wake failed HTTP 429 (retry-after-ms 13394000);
the L1 completed that bounded source work directly, without a replacement seat. Touch B returned
an error without mechanical results; mutation-counter output remained partial. None counts as clearance.

The literal predicates are met, but novelty/calibration scores are held at 8/9: integrity,
prior-examination and argv-laundering findings remain (`w3/C1CritOracle2.md`, `C1CritNeverRead.md`,
`C2CritPredicate2.md`). Outside closure decides admission; no classifier or counter was changed
to bury those findings. Final census 190 rows, exit 0; before 186, exit 0
(`claims/census-round53.txt`). No new capability or coverage-score move is claimed.

## Round 54 — externally anchored freeze and entry truth, both honestly stopped (2026-10-30)

Claims: R54-C1 novelty 8→9, R54-C2 calibration 9→10; both **not admitted**, scores held at 8/9.
Freeze `17f90355c3ec17dcf15f7980d83f1943ae428fe5`; ledger `6e0a1915`; dispatch `62e9bba5`.
Before commands and exits are committed in `corpus/evidence/round54/c1-before.txt`,
`c2-before-dry.txt`; after commands, measured revision and exits are in
`.ufo/waves/round-54/integrate/c1-after.txt`, `c2-after.txt`.

- C1 stamp digest is recorded in `corpus/evidence/round54/anchor/anchor.json`; no completed
  externally validated freeze is claimed. R1 proves incompatible reader/walker APIs and an
  invalid identity condition; the frozen instrument stays unchanged (`w1/R1C1Counter.md`).
- C2 ledger declares 78 entries (62 green, 16 red), four formerly selftest-only green rows now
  red at entry. Original toy laundering control closes, but reviewer reproduces two different
  laundering routes against the unchanged counter; frozen kill rule fires (`w1/R2C2Counter.md`).
  Scratch-root-guard exit and unstable evidence fragments corrected as data, not a rule change.
- WAVE-DONE w1: 66 seats settled, one v2 wave; terminal results retained in `w1-results.json`.
  Missing/empty outputs are not clearance. No replacement or residual wave.
- S198/S199 source the bounded interpretation entry; S200 rejects merkle-root matching as sole
  chain-membership evidence. Census before 190 rows, end receipt `integrate/census-end.txt`.
  Q44 and lesson `corpus/lessons/round-54.md` retain mistakes and the considerthese proposal-2
  filler-control criterion. Assimilation none: 114 collisions of 190 registry/175 staged IDs;
  L0 question and count correction filed. No staged row appended.
- R52 patch proposal refused: R4 demonstrates order-check regression and a confounded K7 case.
  No prior frozen counter or SKILL registry was edited; E8 reproduces r53 C2 at 62e9bba5
  (78 executed, no mismatches, green66/red12).
- Tools: opentimestamps-client 0.8.0 and opentimestamps 0.5.0, uv pip official Python index,
  scratch venv for timestamp experiment; E9 also installed the same client via uv tool and
  isolated uv execution. No pacman. Failed demonstration is not a capability-table entry.

### Round-54 measured close

Clean revision `9a0746bec7c809e1eca2a88070d1fc6a941c39a7`: C1 exit1, header absent;
C2 exit1, executed78, evidence_missing1, laundered1, green61/red17, redeclared4.
Receipts `.ufo/waves/round-54/integrate/c1-after.txt`, `c2-after.txt`.
Registry closure regressed: two new counter paths advertised without rows
(`integrate/round52-c2-regression.txt`). Operability9→8 harmed; all other axis scores
held, no capability. Quality harmed, expansion/discernment unchanged; rejected-harmed
honest-stop. Strict attack share16/66=24.24% missed the floor; 15 empty terminal outputs
and a partial output are not clearance. Census end exit0, rows193, A164/B24/C5,
mined172/rejected13/queued8 (`integrate/census-end.txt`). No fleet-root misroot found.

## Round 55 — frozen claims, one wave dispatched, honest stop at operator wrap-up (2026-10-30)

Claims frozen before data (`plans/round-55-claims.md`, commit `80afa613`): R55-C1 operability 8→9
(registry closure under the round-52 counter), R55-C2 calibration 9→10 (entry-argv binding, new
counter `plans/round55_c2_entryargv.py` built in-wave), R55-C3 coverage attempt (13th TB2 grader
`chess-best-move` executed offline; coverage L0-capped). Before-receipts committed under
`.ufo/waves/round-55/claims/`: C1 `MISSING 2`, `PREDICATE R52-C2 fail`, exit 1; C2 both laundering
fixtures `PREDICATE R54-C2 pass` exit 0 while the true registry entry exits 1; C3 absent.

Wave w1 (one v2 wave, 70 seats; executor16 scribe7 scout7 reviewer12 critic10 mutation-tester6
sentinel4 revenger3 connector3 simplifier2; strict attack 28/70 = 40%) validated under
`ufo-wave-policy-v2.json`, dispatched, and all 70 seats spawned (`inline-dispatcher.log` 12:45:01).
The operator wrap-up (run 12) arrived before WAVE-DONE: the wave was released un-settled. No
results were integrated, no claim was measured after the freeze, and no score moved. Scores held:
operability 8, calibration 9, coverage 7. Un-settled seat residue is named in the report and is
not committed as landed work.

Lesson `corpus/lessons/round-55.md` records the mined mistakes (r54 entry-mode leg computed and not
wired; registry drift of two advertised counters; a wave-build sizing refusal) and the honest-stop
Gate. Assimilation none (L0 `kengaku | round-54` unanswered). considerthese not mined this round.
