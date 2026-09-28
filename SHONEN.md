# kengaku-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2 decision tables, 14 anti-patterns, 9-step checklist, 20 cited-source bullets (`grep -c '^## Decision table' SKILL.md`; `awk '/^## Benchmark anti-patterns/,/^## Research-note/' SKILL.md | grep -cE '^[0-9]+\. '`; `awk '/^## Cited local sources/,0' SKILL.md | grep -cE '^- '`); audit `corpus/evidence/round9-fleet/review.md` §1–§2 (0 dangling citations of 129 swept); round 10 added §Hermetic grader + serving-stack process-pin paragraph (SKILL.md 472 lines)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  round-4 4-task slice, round-5 33-task battery, round-8 78-job horizon probe, round-9 pre-registered replication (`corpus/evidence/round9-replication/results-r9.jsonl`, 284 records); LOG.md rounds 4–9
- [ ] Instructions executable by an agent without oral context
  never tested: no cold-agent execution of `SKILL.md`/`corpus/` has been run or logged. Partial evidence strengthened round 10 — an in-repo gate now exists: `python3 grader.py` exits 0 hermetically (149 checks, 0 mismatches, no endpoint) and `--selftest` passes 4/4 with check-id assertions; independent mutation battery 4/4 (`corpus/evidence/round10-fleet/final-harness.log`); `python3 corpus/evidence/round9-fleet/test_harness.py` still exits 0. The probes themselves still need the live endpoint, so the box stays unmarked until a cold agent runs a checklist end-to-end
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md` §Surfaces re-verified round 10 (all paths resolve; served-model surface pinned at process level for the first time — pid 1299 argv == unit ExecStart, EXACT_MATCH; `~/wikillm/llm-wiki` still absent as documented); 21 knowledge entries cite llm-wiki notes, bench-arena/ledger/bailian surfaces, model-catalog APIs, own `corpus/evidence/`, or fetched public literature; round-9 3 report-outs (`corpus/evidence/round9-fleet/sibling-overlap.md`) + round-10 3 report-outs (`PROVINCE.md` tail: unowned serving-plane config facts → integrator; `loop.sh` telemetry-source semantics → kumitate informational; operator read-only rule re-confirmed)
