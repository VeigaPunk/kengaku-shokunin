# FrontierMapScout — placement of the interval-verdict calibration entry (r25)

Lane HEAD observed: `3f371d2` (`git rev-parse HEAD` = `3f371d2a2ce5ccf1b40b2161210f6591a8320a0a`); all line numbers are HEAD-relative. Read-only seat.

## Findings

**1. It belongs as a NEW coverage-map bullet inserted between `corpus/README.md:209` and `:210`, worded as extending the Judge calibration row — not as an edit of :209, not under :212.** Quoted rows:
- `README.md:209`: `- **Judge calibration**: covered at source-digest depth (round 24) — knowledge/llm-judge-calibration.md; sources S009–S012.`
- `README.md:212`: `- **Statistical reporting for paired evals**: covered at source-digest depth (round 24) — knowledge/paired-eval-uncertainty-reporting.md; sources S015–S019.`
- `README.md:211` is the precedent for an extending row: `... Extends the *Multi-turn state tracking / planning horizon* row ...`
Why: every row 208–212 names exactly one entry and its own `S###` set; the new entry carries new SOURCES rows (exact binomial interval, Rogan–Gladen) plus an S011 re-open. Its method lineage is S011 (`SOURCES.md:33` — "plug-in correction of judge sensitivity/specificity bias with CIs covering both test and human-calibration uncertainty"), which is exactly the inward application `README.md:236` already names as the frontier lead. `:212` is the wrong estimand (paired shared-item contrasts/MDE; C1 is one-sample accuracy + per-class recall/specificity + a corrected leg share). No attribution-instrument row exists in the map at all today, though both entries are indexed at `README.md:54-55` and the surface at `PROVINCE.md:110` — so this is also the instrument's first map row; phrase it as extending, not as a second coverage claim (`plans/round-25-claims.md:17-18`). Q6/Q7 require the entry to name the row it extends and to land file + index row + coverage row together (`corpus/QUALITY.md:50,56`).

**2. Index-table placement:** append the `knowledge/` row after `README.md:60` (`paired-eval-uncertainty-reporting.md`); `:61` starts the lessons block. Trap for P2e (`plans/round-25-claims.md:85-86`, both directions): coverage-map rows carry unbackticked `knowledge/...` (208–212) while index rows are backticked (57, 60) — a census matching one form reports a false miss. Also pin the file→row list to base bytes; if it enumerates `corpus/knowledge/` at check time, the new entry must be indexed in the same commit or the after-run turns red.

**3. Plans table:** add rows for `plans/attrib_calibration.py` and `plans/state_check.py` after `README.md:173` (table end) so existing rows at `:164-170` keep their numbers. Neither exists at HEAD (`ls plans` → only `attrib_probe.py`, three `attrib-r2*-frozen.md`, `round-25-claims.md`). No frozen line anchor points into this table (grep found only historical fleet artifacts citing older README lines, e.g. `corpus/evidence/round10-fleet/r10-critic.md:71`).

**4. PROVINCE:** append a new Core row for the two offline instruments; do not rewrite `PROVINCE.md:110` (P2d freezes the 9 Surfaces rows at base, `plans/round-25-claims.md:82`). `PROVINCE.md:119-123` states the frontier item verbatim: "judge calibration applied / to this lane's own grader/attribution outputs". Admission makes that a **partial** discharge — append a dated note under `README.md:236` and in PROVINCE's Frontier paragraph rather than rewriting either (R1/R5, `corpus/QUALITY.md:86,90`). Residual after r25: `grader.py` verdicts + the S010 perturbation audit.

**5. `corpus/knowledge/attrib-r21.md` DOES print accuracy intervals — the C1 "before" claim must be scoped, but it does NOT treat the bar as uncertain:**
- `:139` `Wilson 95% CI on 20/20: [0.839, 1.000] (this seat's computation, z = 1.96)`; `:154` repeats for 22/22 `[0.851, 1.000]`; `:156` pooled 42/42 `[0.916, 1.000]` self-labelled "a summary, not an independent n".
- `:373-378` repeats both CIs under "N is small … degenerate", lists per-leg n (alibaba 20, zai 13, devin 9, hyper 0, opencode-go 0), then concludes "the 0.80 bar was met on the 3 that served" — a point verdict; no lower-bound-vs-bar rule.
- `:166` shows only the bar's min-n mechanic: `18/18 = 1.000 FAIL` because the bar "refused the shrunken denominator (min scored n 20)".
- `:396` §8 limit 7 "Calibration reading, descriptive only" disclaims calibration of the instrument's confidence outputs (0.538–0.867) — not the bar.
Absent everywhere: Clopper–Pearson, an `INDETERMINATE` token, per-leg recall/specificity intervals, Rogan–Gladen, any n/power statement. Observed sweep: `grep -rlE 'Clopper|Wilson|confidence interval' corpus/evidence/attrib-* plans/attrib*` → no files (exit 1), so receipts/plans are interval-free; the knowledge file is not.

**6. `corpus/knowledge/attrib-prior-art-r21.md` does NOT discuss bar uncertainty:** `:110` "weights are inspectable before any trial and the 80% bar is frozen / before outcomes exist" (freeze, not uncertainty); `:128-131` "The accuracy bar (80%) sits next to AdaptPrint's 80.6% Top-1 … The bar is a pre-registered floor" (magnitude pricing only). Neither entry admits that a point PASS can be indistinguishable from FAIL.

**7. Where the rule actually bites (claim-wording guard):** zero-error CP lower = `0.025^(1/n)`; computed `n=9→0.6637, 10→0.6915, 13→0.7529, 16→0.7941, 17→0.8049, 20→0.8316, 22→0.8456` (python3, stdlib). The r21 overall 20/20 and 22/22 PASSes survive an interval rule; the r22 stored `TARGET hyper 10/10 -> PASS` (`corpus/evidence/attrib-r22-legs.log:344`, duplicated at `attrib-r22-opencode-trials.log:236`) becomes INDETERMINATE, as do per-leg n=9/10/13 blocks. "Every stored point verdict re-verdicts" must not be readable as "all PASSes flip" (Q3/Q4).

**8. Errata placement:** append the r21 correction at EOF (after `attrib-r21.md:657`) so landed `file:line` anchors into that entry stay valid (e.g. `.ufo/rounds/round-23/goal-wave/scorecard-verdict-draft.md:60,270` cite `:466-471`, `:484+`); never edit `:373-378` or `:463`.

Installs: none. No endpoint contacted, no model request.

VERDICT: place the new entry as one coverage-map bullet after `corpus/README.md:209` that names the *Judge calibration* row (S011 lineage) and `attrib-r21.md` §8 limits 3/7 as what it extends; the paired-eval row is the wrong parent; prior entries give accuracy Wilson intervals only and never treat the 0.80 bar as uncertainty-bearing, so the interval-verdict construct is new at entry level even though the lane is not interval-free.
