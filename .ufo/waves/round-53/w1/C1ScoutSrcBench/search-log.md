# Search log — C1ScoutSrcBench (R53-C1 prior-art leg, source scout)

Date: 2026-10-28. Seat: C1ScoutSrcBench (leaf, no subagents). Topic: agent-benchmark test-quality
audits — SWE-bench test-patch insufficiency (UTBoost, SWE-bench+, SWE-bench Verified follow-ups),
Terminal-Bench / Harbor issue trackers and PRs reporting tests that "let any solution pass" or only
check artefact presence, and published counts of such tasks.

Registry check (rule 1, no re-row): `grep https?:// corpus/SOURCES.md` plus two full reads of all
S001–S193 rows. Already-registered URLs excluded from candidature up front, notably: PR #53
"let any solution pass" (S184), TB2.1 announcement (S185), zai-org verified card (S186), ABA audit
(S187), "Solved Issues ... Really Solved Correctly?" (S188), tsDetect (S189), TB paper + §2.3
Specificity (S020/S190), TB2.0 announcement (S090), OpenAI Verified retirement + Pro retraction
(S005/S006), TB2.1 issue #133 (S114), PR #3 (S121), PR #245 (S124), legacy issue #1387 (S192,
rejected), June Kim TB-frame blog (S191, rejected), Snorkel leaderboard (S193, rejected).

Note: the seat brief cites "SOURCES contract v1, CORPUS.md rules 1/5/6"; no CORPUS.md was found at
`corpus/CORPUS.md` or the lane root (checked 2026-10-28; unresolved path). The registry-first,
archive-everything-you-open, stop-rationale and rejected-row conventions above were followed as
summarized in the seat brief and in existing SOURCES.md practice.

## Queries (web_search, 2026-10-28)

- Q1 `UTBoost SWE-bench test patch insufficient arXiv` → 10 results.
- Q2 `"SWE-bench+" OR "SWE-bench Verified" follow-up audit tests insufficient pass without solution` → 10 results.
- Q3 `terminal-bench github issue tests "pass" "file exists" grader weak verifier` → 10 results.
- Q4 `"terminal-bench" 2.0 task grader audit "test_outputs.py" existence check too lenient` → 10 results.
- Q5 `terminal-bench issue verifier "only checks" file exists OR "existence" test_outputs empty artifact passes` → 10 results.
- Q6 `moogician trustworthy-env Terminal-Bench portfolio C extension task name` → 8 results.

## Funnel

- Identified (unique candidate sources across Q1–Q6, after registry de-duplication): 33.
- Screened (opened and bytes archived under `fetched/`): 15 files / 14 distinct sources
  (trustworthy-env README archived as corroboration for the RDI row, not counted as a source).
- Included: 6 kept draft rows (S901–S906 placeholders; L1 to renumber S194+ on commit).
- Excluded: 8 rejected draft rows, each with reason + flip condition (see report).
- Unopenable: 1 — the OpenAgentsInc `2026-09-25-literal-artifact-checks.md` raw fetch returned
  HTTP 404; demoted to an unopened lead (no row, nothing claimed as read).
- Unopened leads (identified, not screened, not rowed): cero753/swe-bench-audit;
  kimjune01/swebench-verified; snowflake.com SnowPR blog; swebench.com/verified.html;
  aiwiki.ai SWE-bench Verified page; agentmarketcap.ai BenchJack post; moltbook integrity post;
  mattWoolly/agent-arena; OpenAgentsInc/openagents issue #9588; harbor-framework/terminal-bench-1
  issue #809; Scribd TB2 tasking guidelines; arXiv 2610.37283 (BenchMeUp); arXiv 2610.36589
  (InfraDev); hub.harborframework.com path-tracing task page; github.com/MukulGupta005 profile;
  SilverWhite/orz index; tbench.ai registry pages. None of these was opened, so none is claimed
  as read; they remain leads.

## Exclusion reasons (rejected rows carry the same text)

1. SWE-Gate (arXiv 2609.04167): measures review-constraint compliance, a different defect axis;
   its functional tests are not the broken element.
2. june.kim "A Determinacy Audit of SWE-bench Pro": measures underdetermined specifications on
   SWE-bench Pro, not weak/presence-only graders; page itself buckets "tests that accept
   incomplete solutions" as other audits' findings.
3. terminal-bench issue #1634: grader input-injection (sympify on submitted text), not presence-only.
4. terminal-bench issue #1636: forged per-test pass bytes via writable verifier channel — a channel
   attack, not a test-strength defect.
5. bohrin docs/WEAKNESSES.md: unrefereed in-repo weaknesses note for its own harness; names no
   benchmark task or grader bytes.
6. howardism.dev benchmark-integrity-maintenance: methodology essay; no task-level grader evidence.
7. MihirBindu/dynamo-log-report-fix: third-party repair fork of a TB task; original grader checked
   existence + size>0 (so `echo '{}'` passes), close to but not the presence-only class (size is a
   value per the frozen p1-spec), and the task's identity in the 2.0 pin is unverified.
8. preferencemodel.com Terminal-Bench 4 issues: measured on TB4, not the 2.0 pin (same pin-mismatch
   reason the registry used to reject S191); the JS-rendered page yielded no located per-task
   grader statement within the 1 MiB cap.

## Stop rationale (saturation)

The six kept rows cover all three topic clauses with published counts: SWE-bench test-patch
insufficiency (UTBoost 36 instances / 345 mislabeled patches; SWE-bench+ 31.08% suspicious;
Probe-to-Generate 77% of Verified instances admit a surviving variant, 211 instances augmented;
SWE-ABS rejects 19.71% of previously passing patches), a Terminal-Bench/Harbor tracker item naming
existence-only verifier checks (tb-2-1 #156), and a benchmark-audit demonstrating the literal
"artefact merely exists" pass with a count (UC Berkeley RDI: 45 confirmed hacks across 13
benchmarks including Terminal-Bench). Later queries (Q5, Q6) returned only re-reportings of the
same phenomenon classes, off-pin benchmarks (TB4), or channel-security rather than test-strength
defects; no new phenomenon class appeared, so the sweep stops here per the saturation rule.
