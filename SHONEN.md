# kengaku-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2 decision tables, 13 anti-patterns, 9-step checklist, 20 cited-source bullets (`grep -c '^## Decision table' SKILL.md`; `awk '/^## Benchmark anti-patterns/,/^## Research-note/' SKILL.md | grep -cE '^[0-9]+\. '`; `awk '/^## Cited local sources/,0' SKILL.md | grep -cE '^- '`); audit `corpus/evidence/round9-fleet/review.md` §1–§2 (0 dangling citations of 129 swept)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  round-4 4-task slice, round-5 33-task battery, round-8 78-job horizon probe, round-9 pre-registered replication (`corpus/evidence/round9-replication/results-r9.jsonl`, 284 records); LOG.md rounds 4–9
- [ ] Instructions executable by an agent without oral context
  never tested: no cold-agent execution of `SKILL.md`/`corpus/` has been run or logged. Partial evidence only — `python3 corpus/evidence/round9-fleet/test_harness.py` exits 0 hermetically, but the probes need the live endpoint and no in-repo gate exists yet (`SCORECARD.md` operability 4, planned move)
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md` §Surfaces re-verified round 9 (all paths resolve; `~/wikillm/llm-wiki` still absent as documented); 21 knowledge entries cite llm-wiki notes, bench-arena/ledger/bailian surfaces, model-catalog APIs, own `corpus/evidence/`, or fetched public literature; 3 cross-domain items reported out, not absorbed (`corpus/evidence/round9-fleet/sibling-overlap.md`)
