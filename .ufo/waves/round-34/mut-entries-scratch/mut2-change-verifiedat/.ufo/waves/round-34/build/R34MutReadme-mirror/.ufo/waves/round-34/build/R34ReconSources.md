# R34 registry recon

`corpus/SOURCES.md` lines 103–119 are registry rows S090–S104. The requested fields are reproduced below; `source` is the row's first 80 characters (counted from the source cell), and `used-by` is verbatim.

| id | source (first 80 chars) | tier | status | opened | used-by |
|---|---|---|---|---|---|
| S090 | Terminal-Bench 2.0 and Harbor (release announcement) — https://www.tbench.ai/news/a | B | mined | 2026-10-25 | corpus/knowledge/terminal-bench-task-grader.md |
| S091 | Agentic Benchmark Checklist (ABC) — https://arxiv.org/abs/2507.02825 | A | mined | 2026-10-25 | corpus/lessons/round-29.md, corpus/knowledge/benchmark-task-validity-checklist.md |
| S081 | Benchmark Contamination: A Taxonomy Organized by Defeated Mitigation — https://a | B | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S082 | The Benchmark Ceiling: Human Judgment, Evaluation Scarcity, and the Political Eco | B | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S083 | Cards Against Contamination: TCG-Bench for Difficulty-Scalable Multilingual LLM R | A | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S084 | 数据污染评估 (Data contamination evaluation), OpenCompass 0.4.0 documentation — ht | A | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S085 | 大模型基准测试体系研究报告（2024年） (Large-Model Benchmark Testing System Repor | B | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S086 | Code LLM 事前学習時の評価データ混入への対策 (Countermeasures against evaluation- | B | mined | 2026-10-22 | corpus/knowledge/contamination-disclosure-card.md |
| S092 | Harbor harness source (verifier execution model) — https://github.com/laude-insti | A | mined | 2026-10-22 | corpus/knowledge/harbor-verifier-execution.md |
| S093 | SWE-bench Pro V2 task verifier files (tests/test.sh, parser.py, config.json) — ht | A | mined | 2026-10-22 | corpus/knowledge/swebench-task-grader-contract.md |
| S100 | Terminal-Bench 2.0 task tree (release identity and task count) — https://github.com | A | mined | 2026-10-22 | corpus/knowledge/terminal-bench-release-identity.md |
| S094 | supersedes S094 — duplicate staged row refused after registry collision; staged wo | B | rejected | 2026-10-25 | — |
| S097 | supersedes S097 — duplicate staged row refused after registry collision; staged an | B | rejected | 2026-10-25 | — |
| S101 | supersedes S101 — duplicate staged row refused after registry collision; this id al | B | rejected | 2026-10-25 | — |
| S102 | supersedes S102 — duplicate staged row refused after registry collision; this id al | B | rejected | 2026-10-25 | — |
| S103 | Toolathlon task evaluation script (tasks/finalpool/ab-testing/evaluation/main.py)  | A | mined | 2026-10-25 | corpus/knowledge/toolathlon-task-grader.md |
| S104 | LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods — https://ar | B | mined | 2026-10-25 | corpus/knowledge/llm-judge-meta-evaluation.md |

## Findings

Observed in live `corpus/SOURCES.md`: S104 is the maximum id; S105 and higher are currently unused. The live S091 is the ABC checklist (arXiv 2507.02825), not the NEC article. In the staged package `SOURCES.append.md` line 21, S091 is the NEC technical-journal article: this is an id collision. The staged S105 at line 35 is the GENIAC phase-1 performance-results page; live S105 is free.

`used-by` path audit: all paths named in the rows above are present in the lane (no nonexistent paths found). Evidence: registry path strings are at `corpus/SOURCES.md:103-119`; this audit was based on lane inventory/current file paths, not a semantic LSP lookup.

Source lines: `corpus/SOURCES.md:103-119`; staged collision evidence: `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:21,35`.

VERDICT: recon-sources (max id S104, S105+ free)
