# Round 24 — learning from the lane's own mistakes (kaika)

Round 24, kaika campaign; worktree base `99cf615`; every pointer re-verified 2026-10-19 against the working tree.
Inputs: STATE dossier §4–§5 (M01–M18, D01–D19), `SKILL.md`, `corpus/QUALITY.md` (untracked, parent-written), the round-23 log/drafts/lesson, and `git log`.
Line drift is corrected inline and marked `(dossier said …)`; a pointer that no longer holds is marked **not reproduced**; no row is dropped.

## Mistakes

| id | class | mistake · evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M01 | PRED | r8 ran 78 jobs with no ex-ante predictions (`SCORECARD.md:277`; `corpus/lessons/round-8.md`) | SKILL anti-pattern 4 (`:75`) + checklist item 1 (`:558`) | Predictions for every condition are written and hashed before the first request. |
| M02 | LAND | r9 count `0/12` falsified as `0/17`; the round-7 amendment rewrote `LOG.md:9` in place — the record and its diff command are at `LOG.md:15` (dossier said `:9`); `SCORECARD.md:75`; `corpus/lessons/round-9.md` carries no append-only text; the cited `85b22e3` is not in this worktree's object store (`git cat-file` → 128), so only the record is reproducible here | none (`append-only`=0 in SKILL; Q6 is entry-scoped) | Corrections are appended entries that name the superseded line and carry the recompute command; the old line is never rewritten. |
| M03 | LAND | r8 landed `results.jsonl` was a `raw`-stripped working copy (`SCORECARD.md:280-288`) | SKILL anti-pattern 14 (`:127`) + rule 9 (`:429`) | Store the complete run bytes; derive every SUMMARY from the committed file. |
| M04 | MEAS | the first `grader.py` failed its own M0 control (a bogus predicted-vs-observed check), fixed by a preregistration anchor (`SCORECARD.md:133`; `corpus/evidence/round10-fleet/INTEGRATOR-NOTES.md`) | SKILL anti-pattern 13 (`:120`) | Mutation-test the grader against a known-bogus check before it scores anything. |
| M05 | LAND | r12/r13 produced but did not commit/index/log; calibration held at 8 (`SCORECARD.md:163`; `corpus/lessons/round-14.md`) | none (`index parity`=0 in SKILL; Q7 is entry-scoped) | A round closes only when LOG + SCORECARD + index rows + report exist. |
| M06 | PROC | the r16 probe was spawned as a nested child by a seat, forbidden by the leaf contract; recorded and not relied on (`corpus/lessons/round-16-recensus.md:15-19`) | none (`leaf`=0 in SKILL) | Lane-dispatched children may advise; they never supply evidence. |
| M07 | STOP | r17 blocked at route admission: 0 native dispatches, 0 verified-round credit (`SCORECARD.md:369-414`; `.ufo/round-17/route-blocker.json`) | none in SKILL/QUALITY — protocol zero-credit rule | A blocked attempt is explicit zero credit, never progress. |
| M08 | PRED | r19 BR-1: the first freeze raced an author re-base (compute-then-write TOCTOU), repaired by a re-freeze after a double-read (`SCORECARD.md:430-433` (dossier said `:426-431`); `plans/probe-battery-r19.md`) | SKILL anti-pattern 5 (`:80`) partial — names freeze-before-runs, not the TOCTOU race (`TOCTOU`=0) | Double-read stability guard, then re-freeze before the first dependent request. |
| M09 | PROC | r19 runner-leg-opencode sent two live requests before the battery existed; self-filed and excluded (`SCORECARD.md:435-437`) | none (`pre-battery`=0 in SKILL) | No live request before the frozen battery file exists. |
| M10 | LAND | r20 `git-add` pathspec error left scorer §10 + template + lesson uncommitted; repaired `96b8962` (`LOG.md:178-180`) | none (`uncommitted`=1, not a rule) | Commit explicit paths; check `git status` at close. |
| M11 | MEAS | r21 three matcher defects, fixed pre-adjudication and recorded (`SCORECARD.md:483-518`, defects at `:497`) | SKILL anti-pattern 13 (`:120`) partial | Run a matcher mutation battery before scoring. |
| M12 | STOP | r22 opencode-go forcing starved (0 on-target) and 4 seats were lost; the gap was named, not redefined (`SCORECARD.md:519-546`) | none (no forcing pre-flight rule) | Pre-flight a forcing mechanism against the target model class; name lost seats. |
| M13 | PRED | r23 scratch-driver trials (13:38–13:39Z) predate the v3 freeze (13:45:47Z) and ran under v2; unscored characterization (`.ufo/rounds/round-23/goal-wave/scorecard-verdict-draft.md:307`) | none (same gap as M08) | Tag pre-freeze runs unscored; never cite them as coverage. |
| M14 | LAND | r23 executed and scored 30/30 with target FAIL, but no LOG/SCORECARD section, no report, and drafts with 17 `[PARENT:` occurrences (1+6+10; dossier said 22); at HEAD `99cf615` `grep -cE '^#+ .*23' SCORECARD.md LOG.md` → `0/0`; **not reproduced** as a live absence — the working tree is now `1/1` because the parent recorded it in round 24 (`SCORECARD.md:567`, `LOG.md:208`) | none | Every executed wave gets a LOG entry even on FAIL. |
| M15 | DISC | no outside non-author spot-check has ever run; `corpus/QUALITY.md` now exists (round 24) but has no non-author row (`corpus/lessons/round-13-coverage.md:42-45`) | none (`non-author`=0 in SKILL) | QUALITY bar plus a named non-author spot-check of one admit and one reject per round. |
| M16 | PROC | r19/r20 claim calibration (8, `SCORECARD.md:163`) while coverage/novelty sat at 7 (`:165`, `:10`); no stagnation waiver recorded for r19/r20 (`:416-482`; `../AXES.md:33-34` — dossier said `AXES.md`) | none (SKILL has no round-contract section) | The round header names the chosen lowest axis and any tie-break/waiver. |
| M17 | LAND | the r16 audit found 61 live citations to deleted paths; the debt is recorded at `corpus/lessons/round-16-recensus.md:26-37` and `SCORECARD.md:262` (dossier said `:305` — that line is the 149-vs-733 confidence defect, D14); `PROVINCE.md:12-17` still mixes absent and present-tense rows | SKILL `:237-242` partial (telemetry ledger marked historical; no PROVINCE rule) | Mark absent surfaces in `PROVINCE.md` in the round they are found. |
| M18 | PROC | `SHONEN.md` evidence blocks are multi-line prose; canonical form allows one indented evidence line per box; 0 `[x]` (`SHONEN.md:5-12`; `../PROTOCOL.md:417` — dossier said `PROTOCOL.md`) | none in SKILL/QUALITY — PROTOCOL.md:417 form | Regenerate verbatim; one evidence line per box. |
| M19 | LAND | the round-23 lesson's premise "no round-23 artifact has landed" (`corpus/lessons/2026-10-16-round23-stream-surface.md:9-11`) was left unmarked after the receipts landed (`corpus/evidence/attrib-r23-stream.log:233-239`); the file was committed `3358c4d` at 14:23:19Z, after the 13:49:42Z score block | none | A superseded premise gets a dated erratum in the same file; the old sentence is not left as current. |
| M20 | MEAS | the census Gate count reads 2 vs the true 1: `grep -lE '^## Gate' corpus/lessons/*.md` also matches `## Gated steps` at `corpus/lessons/round-8-aggregator-box3-coldrun.md:33` (true Gate: `corpus/lessons/round-13-coverage.md:24`; `plans/round24_census.sh` v1 key `C2.lessons_with_gate`, dropped in v2) | none | Anchor census regexes with `$`; a prefix match is not a count. |

## Classes

Captured = a `SKILL.md` rule or a `QUALITY.md` Q-row names the failure mode; partial = a rule names the family but not the mode that failed; protocol = the fleet contract covers it, not a lane file; uncaptured = no rule names it.

| class | rows | captured | partial | protocol | uncaptured |
|---|---|---|---|---|---|
| PRED | M01, M08, M13 | 1 | 1 | 0 | 1 |
| LAND | M02, M03, M05, M10, M14, M17, M19 | 1 | 1 | 0 | 5 |
| MEAS | M04, M11, M20 | 1 | 1 | 0 | 1 |
| PROC | M06, M09, M16, M18 | 0 | 0 | 1 | 3 |
| STOP | M07, M12 | 0 | 0 | 1 | 1 |
| DISC | M15 | 0 | 0 | 0 | 1 |
| **total** | 20 | 3 | 3 | 2 | 12 |

The uncaptured family is still **landing/durability** (M02, M05, M10, M14, M19) and **process closure** (M06, M09, M16), with M12 (STOP), M13 (PRED), M15 (DISC) and M20 (MEAS) as singletons. M17's partial coverage is the missing PROVINCE rule, so it is carried by a closure criterion too. The closure criteria appended to `corpus/QUALITY.md` (`## Round-closure criteria`) cover all twelve uncaptured mistakes; M07 and M18 stay protocol-captured and M08/M11 keep their partial SKILL rules with the tightening recorded in the fix column.

## Round 23 disposition

Round 23 executed on 2026-10-16: 30 stream trials 13:46:41–13:49:28Z under the v3 freeze 13:45:47Z (`corpus/evidence/attrib-r23-stream.log`; the score block is duplicated at `:297-303` with identical numbers). The log's own lines: `:233` `GT counts: {"alibaba-token-plan": 6, "hyper": 24}`; `:234` `ACCURACY: 30/30 = 1.000 (bar 0.80, min scored n 20) -> PASS`; `:239` `STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL`.

The round's one declared claim was the opencode-go coverage clause; it **FAILED**. Round 23 was never recorded in its own round; round 24 records it as **NOT-ADMITTED** (`SCORECARD.md:567`, `LOG.md:208`), with no late credit under rubric clause (d). The coverage gap stands: opencode-go has 0 on-target trials, and the 30/30 result is attribution accuracy on the served legs, not coverage of the target leg. WIP commits `a2ff634` / `f9337d5` / `6f31d23` stay as unverified history. Round 23's round-24 recording now includes the LOG/SCORECARD sections and `corpus/README.md` rows (`:89`, `:150-151`, `:166`); as of this write it still has no round report (`.ufo/reports/` holds only `round-17`), which R2 leaves open.

## Gate

Round-24 admissions against `corpus/QUALITY.md` §Admission bar (Q1–Q8, frozen
before any admission; citation wording tightened pre-commit, see
`plans/round-24-claims.md` Amendment 1). Per-entry Q1–Q8 self-checks came from
the writing L2s (KnowledgeA-3, KnowledgeB3); the L1 re-checked Q1/Q2/Q7 by
census (`C1.full_triad_knowledge 5`, `C1.expansion_entries_on_mined_rows 5`,
`C1.dead_index_rows 0`) and Q3 by the receipts below.

- **Admitted:** `corpus/knowledge/contamination-detection-and-transparency.md` — S001, S002, S004 (A); new ground: detector families/tiers/access and transparency records (extends `benchmark-selection.md` contamination status). Q1–Q8 pass.
- **Admitted:** `corpus/knowledge/llm-judge-calibration.md` — S009–S012 (A); new ground: human-label calibration of judge sens/spec with two-source intervals, rubric-order audits (extends `eval-theory-notes.md` judge/aggregator split). Q1–Q8 pass.
- **Admitted:** `corpus/knowledge/benchmark-saturation-and-lifecycle.md` — S007, S008 (A); new ground: saturation as discrimination loss near ceiling, construct validity. Q1–Q8 pass.
- **Admitted:** `corpus/knowledge/agent-time-horizon-and-task-validity.md` — S013, S014, S005, S006 (A; S005/S006 scoped to OpenAI's self-reports); extends the planning-horizon coverage row without equating r8–r12 with METR's measure. Q1–Q8 pass.
- **Admitted:** `corpus/knowledge/paired-eval-uncertainty-reporting.md` — S015–S019 (A); new ground: paired differences, MDE/resolution, clustering, multiplicity, adaptive-selection inference (extends `bench-arena-round11-power.md`). Q1–Q8 pass.
- **Rejected:** S003 (DCR factor as a general "decontaminated accuracy") — authors scope it as risk-aware, not recovered accuracy; flip: validation on frontier-scale generative tasks.
- **Rejected:** S023 (Scale SWE-Bench Pro blog) as evidence — vendor claims about its own benchmark, tier C; flip: a peer-reviewed paper or audit trail.
- **Rejected inferences (in-entry `## Rejected`):** permutation as proof of human accuracy; private split as longevity guarantee; high score = saturated; temperature-0 + seed = deterministic; SWE-bench Verified/Pro as an uncontested capability meter; r8–r12 as a METR horizon; an unadjusted significant gap as a resolved ranking.
- **Registry changes old→new:** none after creation (rule 2 applies from the
  landed file on). Pre-commit anchor corrections by SourcesGate2 on re-open:
  S006, S007, S009, S013, S014 (anchor + teaches), S015, S023 — listed in that
  seat's report and in the round report.
- **Spot-check:** none yet. Every check above is lane-dispatched and advisory
  (R6). The non-author spot-check (≥1 admit, ≥1 reject) is the orchestrator's,
  after landing.

### New-row receipts (contract rule 1)

Full receipts with byte counts and census: `corpus/evidence/round24-sources/gate.md`.

| id | URL or path | accessed | quote (≤25 words, verbatim) | location | sha256 |
|---|---|---|---|---|---|
| S001 | https://aclanthology.org/2026.gem-main.50/ | 2026-10-19 | “a comparative analysis of five detection families (string-matching, likelihood-based, membership inference, LLM-prompted detection, and benchmark auditing), including access assumptions and failure modes” | Abstract | f4b3eb7ffbf5354091117eaaad35ac528f5b7571f904fd9fec7f5f45697e2221 (47,522 bytes) |
| S002 | https://arxiv.org/html/2510.02386v1 | 2026-10-19 | “Yet, even a brief Group Relative Policy Optimization (GRPO) training can markedly conceal contamination signals that most detection methods rely on.” | Abstract | 3eef8073f4abf573ff15acbdb32a5fa062484345cdbc07084e395825430d3e27 (548,019 bytes) |
| S003 | https://arxiv.org/html/2507.11405 | 2026-10-19 | “Additionally, the current DCR framework is not yet adaptable to generative tasks such as machine translation and summarization.” | Limitations | 04ea3e11fba8a2d40f9243ed1349023af13cf929ed9e57f63d138549f14252b1 (359,691 bytes) |
| S004 | https://arxiv.org/abs/2605.19999 | 2026-10-19 | “we argue that benchmark datasets should be contamination-resistant, i.e., unlearnable, but support inference.” | Abstract | 21d842dbd317820bdf614e9da7a7d312d78f807d5caf2dd2d53d54059d516e5a (42,283 bytes) |
| S005 | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | 2026-10-19 | “We found that 59.4% of the 138 problems contained material issues in test design and/or problem description” | ## Too narrow and too wide tests | 8bd40cbc1e2caefe5c616012e52c182d59b1b9fde47f31f028966a2a11c7c1bb (9,843 bytes) |
| S006 | https://openai.com/index/separating-signal-from-noise-coding-evaluations/ | 2026-10-19 | “we estimate that ~30% of SWE-bench Pro tasks are broken”; “we retract our earlier recommendation to adopt SWE-Bench Pro” | Opening summary; Discussion | fba4c0054cf5b60a1e4190477df6eb62b4da27ed792827ab6eeac867acb0f454 (9,852 bytes) |
| S007 | https://arxiv.org/html/2602.16763 | 2026-10-19 | “We define benchmark saturation as the loss of reliable discriminative power among top-performing models under comparison.” | §2.1 Definition and Scope | ae41d64703217a0015b9ec75eb76961e1444180c6c5ed49e0364724ac789d609 (450,852 bytes) |
| S008 | https://arxiv.org/abs/2511.04703 | 2026-10-19 | “we provide eight key recommendations and detailed actionable guidance to researchers and practitioners in developing LLM benchmarks.” | Abstract | e407cba7b76a090da01247eff9c1477e582f4a9b95d17e0cbeab5f957f0dbbbb (47,021 bytes) |
| S009 | https://arxiv.org/html/2506.22316 | 2026-10-19 | “three novel, previously unstudied types: rubric order bias, score ID bias, and reference answer score bias.” | Abstract | 3aa84ebbae3bdc81714e8c4976d0bb5e20c6a0affa85be2e31310c3477ab55f3 (243,278 bytes) |
| S010 | https://arxiv.org/html/2602.02219 | 2026-10-19 | “the top-1 candidate flips on 15% to 41% of prompts.” | §5.6 Downstream Rank Reversal | a89e2256f106c2a2daa72711175b6355951636a2f76e9db2e117dcc02aa49678 (281,257 bytes) |
| S011 | https://proceedings.mlr.press/v306/lee26bl.html | 2026-10-19 | “Our framework constructs confidence intervals that account for uncertainty from both the test dataset and a human-labeled calibration dataset.” | Abstract | 33a1bcaada76e3af6c2812fb288ef831a798bb62c02c34ff7fa96adb417797ad (15,551 bytes) |
| S012 | https://arxiv.org/html/2306.05685v4 | 2026-10-19 | “Our results reveal that strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement” | Abstract | a1768d348815995e70fe3c49c1164e220a74fbd2c35211cffea1861b6ed4e30f (248,401 bytes) |
| S013 | https://arxiv.org/html/2503.14499 | 2026-10-19 | “we propose a new metric: 50%-task-completion time horizon, the time humans typically take to complete tasks that AI models can complete with 50% success rate.” | Abstract | b57bb898e37b1c954e6313e83ccac57224bb03365f41060176fa0c8f5af7ba99 (446,560 bytes) |
| S014 | https://metr.org/time-horizons/ | 2026-10-19 | “The task-completion time horizon is the task duration (measured by human expert completion time)” | Time Horizon 1.1 (Current) | c5135c54ec56954655010d57fe17ad3b121c8b289c013821fa15be30228627ba (682,272 bytes) |
| S015 | https://arxiv.org/html/2411.00640 | 2026-10-19 | “we therefore recommend using the paired version of the standard error estimate wherever practicable.” | §4.2 Paired analysis | a621e31708bc1acc5be9d683c8a6a88e11a1d78a43ef124efdf755be99cfd71e (230,425 bytes) |
| S016 | https://arxiv.org/html/2410.03492 | 2026-10-19 | “setting temperature to 0.0 with a fixed seed appears to reduce answer variability for many models” | §6 Conclusions | 1f9131c89f20cb9ed6e7a7d851c63dd4e1f092727a91c3705ba42ce7c5662189 (111,055 bytes) |
| S017 | https://aclanthology.org/2025.ijcnlp-long.125/ | 2026-10-19 | “accounting for both of them is necessary to avoid substantially underestimating the overall variability over hypothetical replications.” | Abstract | f025410d543454f08c187e973a60bf21607af3dbbf5134897af6a4f220024196 (44,758 bytes) |
| S018 | https://arxiv.org/html/2605.30315 | 2026-10-19 | “report a per-pair resolution ratio q=N/N⋆ as the primary diagnostic.” | Abstract | abc005960183d7239bce259347bfe1c6ce21d3e3c0efc76ae8a9484b211fa07a (599,163 bytes) |
| S019 | https://arxiv.org/html/2601.20251 | 2026-10-19 | “under a fixed query budget, seek tight confidence intervals (CIs) for model accuracy with valid frequentist coverage.” | Abstract | 6185caf63aaef1d3abda79a9d591bbbab03281a28e6f1be7b42f3c1f9f970cba (589,568 bytes) |
| S020 | https://arxiv.org/abs/2601.11868 | 2026-10-19 | “we present Terminal-Bench 2.0: a carefully curated hard benchmark composed of 89 tasks in computer terminal environments” | Abstract | 48056dd2c223c4510d39bd6d06fd8079f7c8e7575276c30430e0186483623d36 (53,747 bytes) |
| S021 | https://arxiv.org/abs/2510.25726v2 | 2026-10-19 | “Toolathlon spans 32 software applications and 604 tools.” | Abstract | e8b0b348a7590dda0e4a83675b87f9e80f1fb924634aee899eb36973b1de0d07 (47,041 bytes) |
| S022 | https://arxiv.org/abs/2406.19314 | 2026-10-19 | “contains frequently-updated questions from recent information sources” | Abstract | 89e8779cdc51e654d867d403eb39bb154fb04fb1e794d07c7b1ab518dceda456 (45,596 bytes) |
| S023 | https://scale.com/blog/swe-bench-pro | 2026-10-19 | “We use code that models haven't been trained on.” | A Benchmark to Meet Today’s Coding Needs → Data Contamination, The Solution | ee510e84ea4f2afea0d6ac38517ba9b184181d490f4560a5522d6d41292f756b (128,773 bytes) |
| S024 | grader.py | 2026-10-19 | `"""kengaku hermetic evidence-replay grader — the operability gate (round 10;` / `def main(argv=None):` | grader.py:2; grader.py:5664 | 90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f |
| S025 | corpus/evidence/attrib-r23-stream.log | 2026-10-19 | “STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL” | corpus/evidence/attrib-r23-stream.log:239 | afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131 |
