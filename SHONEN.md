# kengaku-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  2 decision tables, 19 anti-patterns, 13 planning-horizon measurement rules, 9-step checklist, 23 cited-source bullets, SKILL.md 578 lines; round-12 additions cover ordered tests, measured power floors, event-class-specific forecast scoring, mean-preserving probability tilts, and repeatability wording. Round-14 citation review re-fetched 14 load-bearing public URLs; all verdicts reproduced.
- [~] At least one end-to-end domain task executed and logged in LOG.md
  round-4 4-task slice, round-5 33-task battery, round-8 78-job horizon probe, round-9 preregistered replication (284 records), round-11 powered rerun (1,473 records), round-12 powered four-point ladder + transport probe (**4,114 records / 4,002 HTTP calls**, `LADDER ESTABLISHED`); LOG.md rounds 4–14. The r12/r13 entries landed one round late and the calibration breach is recorded.
- [x] Instructions executable by an agent without oral context
  tested 2026-09-28T23:31–23:33Z at HEAD `0c51208` by the aggregator's non-author cold run (`corpus/lessons/round-8-aggregator-box3-coldrun.md`, commits `06cdc98` + `d8f2898`): 20/20 read-only commands reproduced. The hermetic gate now replays four trees (`python3 grader.py` → 733 checks, 0 mismatches; S0–S7 selftest all pass). Live probes still require the endpoint; the cold-verdict path is hermetic.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md` surfaces re-verified round 14: endpoint/process pin EXACT_MATCH; route telemetry remains ABSENT; benchmark tree relocated intact to `~/archive/bench-arena`; 23 knowledge entries cite llm-wiki notes, benchmark/Bailian surfaces, in-repo evidence, or fetched literature. Round-14 report-outs route ack-prompt craft to kotoba and the closeout-carryover gate to aggregator/protocol; no serving-plane authority is absorbed.
