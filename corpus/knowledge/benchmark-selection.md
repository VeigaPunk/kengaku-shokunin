# Benchmark selection

Source: `~/Projects/webzites/repos/llm-wiki/wiki/ai/agents-and-engineering/benchmark-shortlist-for-godspeed-research.md` (read 2026-09-28; note dated 2026-04-09).

## Facts

- SWE-Bench **Verified** is deprecated as a primary: OpenAI recommends Pro over Verified as of 2026-02-23 because Verified is "increasingly contaminated" (note, Add Now #2). Keep Verified only for historical continuity.
- Add-now set: Terminal-Bench 2.0 (convergent coding, real traces), SWE-Bench Pro (SWE baseline), OSWorld-Verified (desktop agency), WebArena-Verified (deterministic browser), MCP-Atlas (36 servers / 220 tools / 1,000 tasks — tool orchestration), Toolathlon (multi-app persistent state), BrowseComp (hard-to-find-fact persistence), GDPval (economic deliverables).
- Add-if-relevant: EVMbench (security/exploit), τ²-Bench (shared-control trajectories).
- Minimal stack: Terminal-Bench 2.0 + OSWorld-Verified + MCP-Atlas + BrowseComp + one K2-style reframe suite + one frontier-enumeration suite.

## Falsifiable claim

Public benchmarks measure single-answer convergence; they miss
off-path reframing, variant multiplication, frontier coverage, and
calibration asymmetry (note, "What Public Benchmarks Will Miss").
Counter-evidence would be a public benchmark scoring skyline size or
reframe-discovery rate.

## Decision rule

Sequencing: custom mechanism battery → 1–2 public transfer slices →
heavy public suites. Public results are transfer checks, not mechanism
proof (`godspeed-umwelt-iteration-3-alpha-shittycodex.md`, "Bottom Line").
