# RevSeparability — round-26 pre-review

Axes: novelty, calibration. Scope: pre-registration §Separability / QUALITY R13; no implementation edit or runtime check performed.

## Findings

- **MEDIUM — P3b can count C1 SOURCES additions.** `plans/round-26-claims.md:131-133` says P3b checks PROVINCE rows against the SOURCES census “at the measured tree”; `:152-153,160-162` says C1 adds SOURCES rows. R26-E3 records 42 rows S001–S042 at the frozen base (`PROVINCE.md:175-178`). Appending C1 citations (S043+) then changes an all-current census and can make the historically scoped “42 after round 25” correction appear stale. Freeze P3b's comparison population at the round-25/base census (S001–S042); compare `PROVINCE.md:112` with its round-24 census receipt and `:119`/R26-E3 with the explicitly dated 42-row snapshot, not the landing-tree total.
- **LOW / implementation guard — P3e must not promote new README paths.** P3e is frozen to paths listed OUT_OF_POPULATION by the base run (`plans/round-26-claims.md:126-138`), but the current P2 checker parses current README rows and dynamically enumerates current `corpus/knowledge`, `corpus/lessons`, and immediate `corpus/evidence` children (`plans/state_check.py:968-1030,1074-1079`). C1's new knowledge/evidence README rows (`:152-153`; planned rows in `.ufo/waves/round-26/build/ScribeCoverageRows.md:13-16`) can leak if P3e derives its members from that live scan. Keep P3e IDs/paths exactly frozen from base; later C1 rows/files may be reported OUT_OF_POPULATION, never counted as P3 assertions. Compare frozen P3e IDs/statuses, not a raw JSON `out_of_population` total (`state_check.py:1096-1112` includes it in JSON counts).
- **No reverse SCORECARD/PROVINCE leak into C1.** C1 re-grades the four pinned result files using `grader.py` and CP math (`plans/round-26-claims.md:46-79`); it does not consume SCORECARD, PROVINCE, README, or SOURCES. C2's appended SCORECARD R26-E1/E2 and PROVINCE R26-E3 therefore cannot change C1 family counts. SCORECARD correction rows are intentionally C2/P3a inputs, not C1 inputs.

## Exact R13 revert tests

Record both baselines and exact path/row removals in the preregistered `corpus/evidence/round26-calibration/revert-test.txt`:

1. **C1 invariant under C2 removal:** compare `python3 plans/grader_perturb.py --summary` family fields and TOTAL at landing vs. a copy with only C2 changes reverted: `plans/state_check.py` (v3 diff), `plans/fixtures/r26/p3_oracle.sh`, `plans/fixtures/r26/content_pins.tsv`, `plans/fixtures/r26/state_p3/`, `SCORECARD.md` R26-E1/E2 appended corrections, and `PROVINCE.md` R26-E3 appended correction. Keep the four pinned result files, `grader.py`, and C1 fixtures untouched.
2. **C2 invariant under C1 removal:** compare `python3 plans/state_check.py --json` on the frozen P2+P3 assertion IDs/verdicts at landing vs. a copy with only C1 artifacts reverted: `plans/grader_perturb.py`; `plans/fixtures/r26/perturb_oracle.py`, `plans/fixtures/r26/perturb_population.tsv`, `plans/fixtures/r26/perturb_cases.jsonl` (and any other `plans/fixtures/r26/perturb_*`); `corpus/knowledge/grader-perturbation-audit.md`; only its `corpus/README.md` knowledge-index row and C1 evidence-index row(s); only C1-created `corpus/SOURCES.md` rows after S042; and C1-only files under `corpus/evidence/round26-calibration/` / `round26-sources/`. Preserve shared files/directories and non-C1 README rows; edit README/SOURCES by row, not by reverting the whole file. Verify the P3b census is still S001–S042 and that P3e's frozen IDs do not expand.

## Residual risk / verification gaps

Current `git status --short`/diff showed only `PROVINCE.md`, `corpus/QUALITY.md`, and untracked `.ufo/waves/round-26/`; no C1/C2 implementation, README/SOURCES/SCORECARD changes, or revert receipt had landed. LSP is unavailable (`read xd://lsp` returned “No such tool”); code citations above are direct text evidence, not semantic LSP proof. No checks run; this is pre-review only.

Installs/updates: none.

VERDICT: R13 is not yet demonstrated; freeze P3b's dated SOURCES population and P3e's exact base IDs, then run the two row-granular reversion comparisons. C2 SCORECARD/PROVINCE changes do not feed C1.