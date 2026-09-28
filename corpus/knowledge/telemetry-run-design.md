# Telemetry & run design

Source: `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/godspeed-umwelt-iteration-3-alpha-shittycodex.md` (read 2026-09-28; dated 2026-04-09, status: plan).

## Per-run artifacts and fields

10 telemetry fields per run (Phase 0 "Artifacts to record"):

1. final answer quality
2. correctness or validity
3. number of variants
4. number of non-dominated variants
5. axis vocabulary count
6. unique findings
7. tool calls
8. wall-clock
9. token usage
10. framer prediction error

Artifact set per run dir (iteration-3 note): `response.md` +
`telemetry.json` + `judge.json` adjacent.

## Phase gates (hard stops)

- **Phase 0 freeze** before scored runs: ex-ante predictions, godspeed text, judge schema, telemetry capture.
- **Phase 1 smoke**: 2 tasks × 2 conditions = 4 runs (one trivial convergent, one K2-style). Promotion rules: broken telemetry → fix harness; zero shape difference → tighten task design; correctness collapse → stop, inspect prompt contamination.
- **Phase 2 core**: 12 tasks × 2 conditions = 24 runs across K2-reframe (4), frontier enumeration (4), discovery (4).
- **Phase 3 transfer**: 8–12 runs public slices only after mechanism visible.
- **Floor**: 36–40 runs total.

## Judging schema

One schema all tasks: correctness, frontier breadth, frontier quality,
unique insight count, tool efficiency, wall-clock cost. Discovery tasks
score *validated* findings, not raw accusations.

## Interpretation table (from "Analysis Plan")

Breadth↑+correctness flat → keep expanding. Breadth↑+precision↓ → narrow
directive/task. Public flat + custom moving → iteration-2 thesis
supported. Public moving strongly → broader claim needed.
