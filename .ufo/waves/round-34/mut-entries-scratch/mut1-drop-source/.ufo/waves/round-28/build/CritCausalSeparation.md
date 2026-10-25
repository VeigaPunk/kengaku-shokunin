# CritCausalSeparation — round 28 (author-side critic advice, not outside closure)

Writer/seat: KengakuR28.CritCausalSeparation-2. Date 2026-10-21. Read-only; only this report and
`.ufo/waves/round-28/scratch/CritCausalSeparation/literal-recompute.txt` were written.
Axes judged: novelty (legacy, mapped to canonical coverage/constructs, lowest axis 7) and calibration (8). Neither score is affected by this review.

## Dated boundaries
- Baseline b9b2479 (committed 2026-10-21 10:37:39 -0300). Prereg f0ba09b (2026-10-21 10:50:58 -0300) adds only `plans/round-28-claims.md` and `plans/fixtures/r28/**` (`git show --stat`).
- Round27 is admitted in fleet `MANIFEST.json` rounds[411] (`"round": 27, "date": "2026-10-21", "verdict": "admitted"`). Every registry fact below comes from the working tree at f0ba09b. At this review, no writer worktree (ExecBenchmark, ExecOracle, ExecRegistry) has a delivered `benchmark_spec_audit.py` or `registry_check.py`; all three sit clean at f0ba09b.

## Strongest falsifiable objection
The prereg (`plans/round-28-claims.md` line 10) claims "Distinct populations and paths make claims independently verifiable" and requires "two-way sandbox revert measurements". The populations are separate, but the paths are not.

**Counterexample.** Both claims must change `corpus/SOURCES.md`:
- C1's frontier adds rows S061, S062 and S063 "with lesson uses" (prereg line 30).
- C2 repairs S038's allowed cells (prereg line 10), and probably S050's as well (see below).

Because `SOURCES.md` belongs to neither claim alone, a path-granular revert cannot isolate either claim:
- **Reverting the C1 paths leaves C1 content in place.** The C2 measurement then still runs on a registry that contains the C1 rows S061–S063. ExecRegistry's spec allows "Whole-registry malformed rows may be detected structurally" (duplicate IDs, enum values, safe used-by paths). So C2's exit code can depend on C1 rows. If used-by is validated for every row and the C1-revert sandbox deletes the new knowledge file that S061–S063 list as used-by, C2 goes red because of the revert, not because of a C2 fault.
- **Reverting the C2 paths deletes C1 work.** If `SOURCES.md` is classed as a C2 path, the revert removes the S061–S063 rows. C1's counts survive because the audit reads only `plans/fixtures/r28/webarena/**`. C1's source and knowledge admission does not survive.
- **The "only delta" condition fails on the final tree.** The rule "repair counts only after the delivered checker fails on the baseline and passes with allowed-cell repair as the only delta" (line 33) cannot hold when the final tree is compared with baseline. The final `SOURCES.md` diff contains S061–S063 too.

**Recursive and new-artifact dependencies.**
1. **Shared new lesson file.** `corpus/lessons/round-28.md` is the likely used-by target for both S061–S063 (C1) and the M65 lesson about S038 (C2).
   - The M65 lesson must name S038 literally.
   - The prereg allows extra lesson used-by paths.
   - That makes a loop: S038's used-by points to the lesson, and the lesson cites S038.
   - The lesson belongs to both claims, so either revert breaks the other claim's used-by path.
2. **Unpinned frozen contents.** `population.json` pins the 35 paths and `base_revision` only, with no per-file digest. On the final tree, C2 reads whatever those files contain then.
   - `corpus/knowledge/benchmark-selection.md:18` already names "WebArena-Verified". That file is a natural cross-link target for C1 knowledge.
   - Any C1 edit there changes C2's input without changing the stated population.
3. **QUALITY criterion.** It is created only after the C2 checker shows a failure (line 33). If C1 also edits `corpus/QUALITY.md`, that file becomes a third shared file.
4. **Foreseen failure.** The checker is a new artifact built knowing the S038 defect (F4 p=.95, "already disclosed"). Its red baseline on S038 confirms the instrument; it is not a discovery. Its ability to catch other faults rests on the CLI selftest controls (line 26).

## Decisive local evidence (independent re-scan, not the delivered checker)
My scan used the population's own `reference_pattern` over its 35 paths. Full output is in `scratch/CritCausalSeparation/literal-recompute.txt`.
- **S038:** cited at `corpus/knowledge/attribution-interval-calibration.md:144`. Its `SOURCES.md:60` row has status `queued` and used-by `—`. This is the disclosed drift.
- **S050:** cited at `corpus/knowledge/extraction-policy-comparison.md:18` ("inspect_ai `pattern()` (S058, correcting S050) takes a first regex hit"). Its `SOURCES.md:72` used-by is only `corpus/lessons/round-27.md`.
  - Under the declared literal contract ("historical/supersession mentions included"), this is a second baseline `missing_used_by`, beyond S038. [INFERENCE until the delivered checker runs.]
  - It would falsify F5 ("S038 allowed-cell repair suffices for all 13", p=.55).
  - It needs a second `SOURCES.md` repair, which in turn needs S050 reopened first (prereg line 10).
- **Other rows:** S049 and S051–S059 used-by cells include `extraction-policy-comparison.md`. S060 is `rejected` and uncited, which is not an error.

## Impacted axes
- **Calibration (C2):** the revert-survival and "only delta" claims are not measurable as written. Two repairs are likely, not one, so F5 is at risk.
- **Novelty/coverage (C1):** C1's counts are unaffected. C1's source and knowledge admission is coupled to a C2-owned file under any path-level revert.
- No score repricing follows from this review. Both scores are held.

## Smallest safe correction (no production edit by this seat)
1. **Measure C2 in a sandbox, not on the final tree.** Run `registry_check.py` on a baseline-b9b2479 export twice: once as is (expected red) and once with only the S038/S050 allowed-cell hunks applied (expected green). The "only delta" claim then holds by construction.
2. **Revert at row/hunk granularity.** C1 owns rows S061–S063 plus its new files. C2 owns the allowed cells of the 13 frozen rows. Declare this split in the integration receipt. Shared files are `corpus/SOURCES.md`, `corpus/lessons/round-28.md` and `corpus/QUALITY.md` if touched.
3. **Restrict whole-registry checks.** Either limit used-by existence validation to the 13 frozen IDs or report it as a separate, non-gating finding class, so C1 rows cannot flip C2's exit code.
4. **Pin or forbid frozen-file edits.** Either record baseline blob digests of the 35 paths and have C2 run against them, or forbid round28 edits to those 35 files. Disclose either choice.
5. **Disclose the lesson loop.** Do not count the round-28 lesson toward C2 frozen coverage.
6. **Handle S050 under the same rule as S038.** Reopen it before repair; otherwise disclose it as an open mismatch. Do not suppress it.

## Limitations
- No delivered checker or audit existed to run, so the S050 finding is a literal re-derivation, not checker output.
- No sources were opened, so no URL quotes appear here.
- I did not inspect the selection rule or C1 per-task contents; other seats cover those.
- Commands run: `git log`, `git show --stat`, `git status`, read-only `python3` stdlib parsing of `SOURCES.md`, `population.json`, `MANIFEST.json` and the build-spec. No tools were installed or updated.

## Verdict
**PARTIAL**, scoped to C1/C2 causal separation only. The populations are separable: C1 counts read only the webarena fixtures, and C2 reads only 13 rows and 35 paths. Path and file separation fails because `SOURCES.md` and the round-28 lesson are shared and the 35 frozen files have no content pin. Corrections 1 to 4 fix this without changing any claim scope. This is not a blanket round verdict.
