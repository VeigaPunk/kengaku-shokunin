# C1 population-rule review

Axes reviewed: novelty (coverage of the stored-response grader behavior).

## Finding — Medium: baseline-gated exclusions are a selected subset

- The frozen rule starts from records with both `raw` and stored `ok`, then excludes any whose baseline re-grade does not reproduce stored `ok` (`plans/round-26-claims.md:46-52`). Those mismatches are not random missingness: they are exactly cases where the grader/parser no longer reproduces a committed verdict, so they may be unusually fragile. Family CP intervals conditional on the survivors cannot be generalized to all stored graded responses. The prereg's nonzero exit on baseline inconsistency (`:75-78`) is appropriate; preserve that as a red preflight, not as a reason to silently report the survivor intervals as the full-population result.
- Report these outcomes separately: (1) total source rows; (2) raw+stored-ok candidate count; (3) baseline matches; (4) mismatches split stored `ok=true`→regraded false and stored false→regraded true; (5) baseline exceptions/missing truth; and (6) rows outside eligibility (missing `raw` or `ok`). For each baseline exclusion, retain file, JSONL line, cell, pid, turn, grader, stored/current verdict, parse status, and reason. Include file×cell×grader rollups in `--summary` and row-level detail in `--json`; preserve each family’s applicable and not-applicable counts/reasons. Label rates explicitly as conditional on baseline-matched records, and do not fold baseline mismatches into MP/MC family denominators.
- Current frozen records illustrate why this accounting matters: a read-only census found raw+ok candidates of r8=188, r9=128, r11=320, r12=1328 (1,964 total); many other source rows have raw but no `ok` and are outside the stated cohort, not baseline exclusions. A narrow parse/regrade against stored `want` found no parse failures or `ok` mismatches, but this was not the absent instrument's full meta-truth cross-check and is not a C1 result.

## Implementation constraint / residual risk

- Do not treat every r8 C record as an ordinary dict-state `want`: the 16 C records have `want=None`. Canonical replay uses `grade_c` for C-conflict/C-benign/C-norule, but C-MONO has a separate `valid_latin` path (`grader.py:482-504`; definitions at `:247-268, :232-238`). Route and count those 4 C-MONO records explicitly; a generic `grade_state`/`grade_c` fallback could error or manufacture baseline mismatches and thereby drop a meaningful stratum.
- The current lane tree has no `plans/grader_perturb.py` (read returned not found; `git status --short` listed no such path), so implementation-side exclusion behavior and emitted detail could not be reviewed. The status output showed only `PROVINCE.md`, `corpus/QUALITY.md`, `.ufo/waves/round-26/`, and `plans/state_check.cover` changes.

## Verification gaps

- LSP device unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices without LSP. No LSP diagnostics/references were available; literal grep was used only to locate grader code, with claims grounded in direct source reads above.
- No builds/tests or perturbation instrument run. The counts above are exploratory read-only population inspection, not verification of the missing instrument. No tools installed.

VERDICT: The baseline-matching rule is defensible only as an explicit conditional estimand with baseline mismatches treated as a red, separately reported outcome; aggregate `excluded=<x>` alone is insufficient to assess selection bias.
