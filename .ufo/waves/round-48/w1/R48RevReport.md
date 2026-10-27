# R48RevReport — report-structure pre-check

Axes: calibration (R48-C1) and coverage (R48-C2). Scope is report contract only; no claim admission judgment.

## Sources opened

- `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` — accessed 2026-10-27. Located quote: “test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]” (round-46 spot-check lines 31–33 records reopening and quotation).
- `/home/vgpnk/Projects/shokunin/.ufo/prompts/kengaku-round-48.md` — accessed 2026-10-27. Located quote (lines 104–106): “opens by naming the round's declared claims (1–3) and their target axes or capability”.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — accessed 2026-10-27. Located quote (lines 29–32): “Every receipt this round prepends `REV <40-hex>` of the tree it measured.”
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — accessed 2026-10-27. Located quote (lines 8–11): “`## SHONEN` is present with four `[~]` lines, one per report box.”

## Defects to fix before filing

1. **Use required destination and ordered headings.** Fleet report belongs at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/kengaku.md` (prompt lines 101–102), not this lane artifact path. Sections in exact order: Work performed; Landed changes; Before → after measurements; Sources & frontier; Trend verdicts; SHONEN. Work performed must open by naming both claims and axes (C1 calibration, C2 coverage), with one evidence-linked bullet per work item.
2. **Landed changes require traceability.** Tie every reported change to its `LOG.md` entry and carrying commit; avoid unsupported or uncommitted work claims.
3. **Measurements need command and revision.** Include one before→after measurement per claim, the literal counting command, and commit measured. Every receipt cited should expose `REV <40-hex>`; distinguish stage-1 freeze `a543d920…` from stage-2 freeze and any measured landing revision. Do not imply a scored result without its frozen-stage evidence.
4. **Sources & frontier must be explicit despite marker exception.** Include SOURCES row counts before→after with census command/output and exit codes, tier additions, touched-row old→new, and frontier advances; identify the sourced C2 basis (S166) and evidence/lesson Gate pointer. This section is required for conformance even though omission is marker-neutral.
5. **Trend verdicts likewise required for conformance.** Give expansion, quality, discernment individually from the allowed verdict vocabulary with evidence; no scalar summary. Omission is not a marker predicate, but is a report defect.
6. **SHONEN must match checklist cardinality.** One line per actual `SHONEN.md` box; use `[x]` only with a named independent non-author verifier, `[~]` with resolvable evidence, `[ ]` if untouched. Round-46 precedent says four lines, but confirm current checklist count rather than assuming it remains four.
7. **Report real evidence, no placeholders.** Every work item needs path:line, command output, or commit hash; no unresolved placeholders. Report must not claim admission absent the full independent gates and integration evidence.

## Census command

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`

Contract requires start and end outputs plus exit codes; round-end exit 0 is required. The round-46 precedent reports `kengaku ok`, exit 0, with duplicate-URL W04 warnings (spot-check line 35); repeat output must be the actual round-48 observation, not copied precedent.

## Limits and verification gaps

Read frozen claims, round-46 verifier spot-check, round-48 prompt, and round-48 lesson. Did not run census, scored counter/probe, or inspect final report/integrated lane. Therefore this is a structural checklist, not confirmation of compliance or a claim verdict. Freeze state and measurement chronology were not independently verified in the committed lane tree.

VERDICT: actionable pre-filing defects listed; no admission judgment.
