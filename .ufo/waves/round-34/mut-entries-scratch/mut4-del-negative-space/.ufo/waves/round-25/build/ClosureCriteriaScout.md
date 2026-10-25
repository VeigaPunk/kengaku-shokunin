# ClosureCriteriaScout — are R1–R10 mechanically runnable, and what do they return at base?

Base: lane HEAD `3f371d2` (pre-registration); round base master `6180e4f`. Read-only; only this file written.
Commands run in `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; no endpoint, no network, no installs.
Legend: RUN = the literal Check executes today and returns a determinate pass/fail after binding in-tree
arguments; PARTIAL = needs an artifact/comparator that does not exist or has two conflicting readings.

| R | Runnable? | Base result | Command output / location |
|---|---|---|---|
| R1 | RUN (bind one instance) | **RED** | `grep -c 'All 149 checks' SCORECARD.md` → `2` (old text `:307`, errata quotes it `:618`), not 1. Errata command/date present (`:618-620`). Second instance: `grep -c '0/12' corpus/knowledge/bench-arena-round7-noise-n25.md` → `4` (`:24` old, `:80-81` errata, `:104` quote). |
| R2 | PARTIAL | **RED** | `grep -c '^## Round 24' LOG.md SCORECARD.md` → `LOG.md:1` / `SCORECARD.md:1` (not the asserted `1 1`). `test -f .ufo/reports/round-24/kengaku.md` → 1; no lane r24 report exists (rounds 19–22 use `.ufo/rounds/round-N/kengaku.md`, 23–24 have none). `git status --porcelain` → `?? .ufo/waves/`; scoped r24 paths clean. No pathspec-limited commit list exists anywhere → third clause unbound. |
| R3 | RUN | **RED** (r21,r22) / **GREEN** (r23) | r23 LOG `:208-230` names `corpus/evidence/attrib-r23-stream.log` + `-> FAIL` → green. r22 LOG `:184-207`: 0 hits for `attrib-r22`/`.log` (token `PASS` only) → red. r21 LOG `:167-183`: no receipt path, no `PASS`/`FAIL` token → red. |
| R4 | RUN, wrong scope | **RED** | Literal awk → 11 rows, all from §Province map Historical `:148-158`, **zero** from §Surfaces `:12-20` ($2 there is the surface name, not the path); rows `:153,156,157` carry 2–3 paths, so not “one path per row”. Substantive `test -e` on §Surfaces: `~/Projects/webzites/repos/llm-wiki` (`:12`), `~/archive/bench-arena/` (`:13`), `~/.bailian/telemetry.jsonl` (`:16`), `~/.bailian/…models` (`:17`) all miss with no `ABSENT` on the row; only `:15` has it. |
| R5 | RUN (needs whitespace normalization) | **RED** | `grep -n 'no round-23 artifact has landed' corpus/lessons/2026-10-16-round23-stream-surface.md` → no hit (sentence wraps at `:9-10`); `grep -n 'round-23 artifact has landed'` → `:10`. `grep -nE 'erratum\|superseded'` on the note → exit 1, 0 hits; the stale premise stands. |
| R6 | PARTIAL (root ambiguous) | **RED** clause 1, green clause 2 | Lane root `.ufo/prompts/` absent → literal `grep -rn … .ufo/prompts/` exits 2. Fleet root `/home/vgpnk/Projects/shokunin/.ufo/prompts/` exists; `grep -rl 'W3ReviewKengaku'` → 0 files (green). Clause 1: no r24 report and no `non-author:` line (`grep -n '^non-author\|non-author:' corpus/lessons/round-24-verifier-spotcheck.md` → exit 1); the id appears only in table cells `:12-13`. |
| R7 | PARTIAL (disjunctive comparator) | **RED** under last-FROZEN / first-commit; green under receipt-stated FROZEN | `request_ts` field: 0/9 receipts. FROZEN vs first POST: r21 `10:20:08 < 10:21:04`; r22 legs `11:49:01 < 11:50:06`; r22-opencode `11:47:59 < 11:50:45`; r23 `13:45:47 < 13:46:41` → green. But live pin = last `FROZEN:` (`plans/attrib-r22-frozen.md:245` `11:53:12Z`) is **after** r22-legs run-1 requests `11:50:06-11:51:49Z` and `unscored` count is 0. First commits (`0d23c61 11:26:22Z`, `8a08483 13:31:08Z`, `6f31d23 14:25:10Z`) all postdate first requests → red. r22-legs also cites anchor `3d7861f8` whose `FROZEN:` line is absent from the table (only 2 FROZEN lines; pin mentioned inline `:75`). |
| R8 | RUN | **GREEN** | Section-scoped: `Lowest axis:` at section line 3, `tie-break` line 4, `waiver` line 5 (`LOG.md:233-235`). Caveats: literal lowercase `lowest axis` does not match (`Lowest axis`); whole-file grep cannot prove section membership. |
| R9 | RUN | **RED** | `grep -rliE 'pre.?flight' corpus/evidence/attrib-*.log \| wc -l` → `0`. On-target count and verdict do agree where present: `attrib-r23-stream.log:303` `on-target GT n=0 … -> FAIL`; `:336-337` confirms clause not met. |
| R10 | RUN | **RED** on equality | Anchored `grep -lE '^## Gate$' corpus/lessons/*.md \| wc -l` → `2` (`round-13-coverage.md`, `round-24.md:56`); unanchored → `3` (adds `round-8-aggregator-box3-coldrun.md:33` `## Gated steps`, named at `round-24.md:30`). Reported number in M20 is “true 1” → 2 ≠ 1. |

## Findings

1. **R1 is unsatisfiable with append-only errata that quote the superseded value** — the errata itself is a
   second grep hit (`SCORECARD.md:618`; knowledge `:80-81`). The check needs “count occurrences before the
   errata date”, not `grep -c`. The D14 errata also anchors `:305` while the stale phrase is `:307`.
2. **R2/R3 violate R10's own anchoring rule**: `grep -c '^## Round 2' LOG.md SCORECARD.md` → `5` / `5`
   (matches Rounds 20–24). For N=2 the census is inflated 5×; `$`/word-boundary anchoring is missing.
3. **R2 asserts a text format `grep -c` never emits** (`LOG.md:1` vs `1 1`) and a report path that holds
   only for round 17; rounds 19–22 live in `.ufo/rounds/`, rounds 23–24 have no lane report at all.
4. **R4's awk enumerates the Historical table, not `## Surfaces`** — the rule it claims to enforce (ABSENT on
   failing surface rows) is never applied; four surface rows fail `test -e` without `ABSENT`.
5. **R5's own named instance was not repaired** — `corpus/lessons/2026-10-16-round23-stream-surface.md:9-10`
   still says “no round-23 artifact has landed”, with 0 erratum/superseded hits; the literal grep misses the
   line-wrapped sentence even before that.
6. **R6 cannot run from the lane root** (`.ufo/prompts/` absent, exit 2) and clause 1 has no artifact.
7. **R7 has no single comparator**: “first commit **or** FROZEN line” yields opposite verdicts (all green
   vs all red); a mid-file re-freeze (`attrib-r22-frozen.md:245`) straddles r22 requests with no `unscored`
   tag, a case the check does not cover.
8. **R10 is self-referential**: the round-24 lesson that reports Gate count 1 adds the second `## Gate`
   (`round-24.md:56`), so the criterion's equality is stale the moment it lands.

Installs: none. Scratch: none.

VERDICT: 10/10 checks were executed at base; only R8 is green cleanly (R3 green for r23, red for r21/r22; R6 clause 2 green at fleet root), while R1, R2, R4, R5, R9, R10 and R3-on-r21/r22 are red; R2, R6, R7 are not mechanically decisive as written — each r24 closure fix that can fail, demonstrably does at base.
