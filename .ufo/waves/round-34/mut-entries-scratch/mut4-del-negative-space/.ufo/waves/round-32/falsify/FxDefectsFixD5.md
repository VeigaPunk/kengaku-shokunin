# D5 planned repair: dead-seat record

## Evidence

The R31 registry entry at `.ufo/waves/round-31/falsify/swarm-registry.json:239-249` names `R31FxEntryBar`, with `agentId` `L1Kengaku31.R31FxEntryBar` (lines 239-242). The specific entry has no `reportFile` field (lines 239-249); the registry excerpt identifies its role and assignment only. The expected report path `.ufo/waves/round-31/falsify/R31FxEntryBar.md` is absent in the current filesystem (`test -e` returned `report-absent`). The draft's D5 receipt reports `members: 36`, `reports: 35`, and `registry-not-reported: ['R31FxEntryBar']` (`.ufo/waves/round-32/build/R32DraftMistakes.md:184-190`). For the historical committed-tip assertion, draft §4 cites its read-only set-difference result at round-31 tip `87f0d32` (same lines). This supports saying no report was found/landed, not claiming an observed absence of runtime output: no output evidence is supplied by the registry entry or filesystem check.

## R5 proposed-line simulation

Draft §6 proposes this single line (`R32DraftMistakes.md:338-345`):

`| falsify | 36 dispatched | `R31FxEntryBar` — dead: no report committed at round-31 tip `87f0d32` (35 of 36 landed); recorded per routed defect D5 | 0 |`

The R5 implementation (`plans/round32_defects.py:134-141`) requires the lesson file to exist and calls `near(text, "R31FxEntryBar", "dead", width=160)`. `near()` checks either token ordering with at most 160 characters between them (`:64-69`; default case-insensitive regex). In the proposed line the tokens occur on the same physical line with only ` — ` between them; therefore the near-text predicate passes. The report is a simulation of that predicate only; the lesson itself does not yet exist per draft §5 (`:325-327`), so this does not establish an end-to-end R5 run.

## Evidence to cite for `dead`

Cite the R31 registry entry for member identity, cite the missing report path/check for no report file, and cite the draft's `36`/`35`/set-difference receipt for the unreported status. Do not claim “no output” as a separately verified fact absent an output capture; phrase the basis as no report file/committed report found. The proposed dead-seat wording is calibrationally supported as absence of a report, rather than proof the seat produced no transient output.

VERDICT: d5-closable
