# FxFrontier — round-32 frontier wording verification (C1)

Assigned: read `corpus/README.md` lines 276–279 and 253–255 (uncommitted edits); verify
(1) the round-32 sub-bullet discharges the Toolathlon clause ONLY for the one task whose
evaluation script is read, matching the entry's own scope statement, and (2) the coverage-map
row matches the entry's content (0.05 tolerance, fail-open, S097 five-part); report overclaims.

Method: quoted spans verified against bytes fetched at the pinned revisions
(`tasks/finalpool/ab-testing/evaluation/main.py` @ Toolathlon `9be8d8fe`
(` sha256 `3bad26b6…`, 297 lines), `utils/evaluation/retry.py` @ same commit (109 lines),
arXiv 2412.05579v2 abstract page, GitHub tree API at the pinned commit), and against the
entry draft `corpus/knowledge/benchmark-grader-semantics.md` and `corpus/SOURCES.md` rows
S093/S094/S097.

## 1. Round-32 sub-bullet (README:279) vs entry scope — scope-accurate

Sub-bullet: «reads the one Toolathlon task whose evaluation script this lane opens
(`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and the LLM-as-judge survey
frame (S097). The "and for Toolathlon" clause is discharged **for that one task's scoring code
only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's;
any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity».

Entry scope statement (entry:10–18): «discharges the README frontier bullet-1 clause "and
for Toolathlon" (corpus/README.md:276) **for the one task whose evaluation script is read** —
the Toolathlon `ab-testing/evaluation/main.py` at `9be8d8fe` — and for the survey frame that
separates deterministic graders from LLM judges. It is not runtime task validity
(`PROVINCE.md` refuses that to this lane), not contamination measurement, and not deployment
configuration.»

- «one task … scoring code only» ↔ «one task whose evaluation script is read» — exact.
  The pinned tree at `9be8d8fe` contains exactly one evaluation script under the ab-testing
  task dir (`tasks/finalpool/ab-testing/evaluation/main.py`; `list_storage_buckets.py` is a
  listing helper, `preprocess/main.py` is preprocessing, not grading), so the "one task"
  framing is not an under-count.
- «LLM-as-judge survey frame (S097)» ↔ «the survey frame that separates deterministic graders
  from LLM judges» — match.
- «clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any
  SWE-bench Pro V2 grader beyond the round-31 task-level one)» — a negative/still-open claim;
  the entry never claims those and its §What this does not establish explicitly declines them.
  No overclaim.
- «remains open … for runtime task validity (which PROVINCE.md refuses to this lane)» ↔ entry's
  «It is not runtime task validity (PROVINCE.md refuses that to this lane)» — match.

The sub-bullet does not claim anything for any other Toolathlon task or for the other
benchmarks. **Verdict for check 1: scope-accurate.**

## 2. Coverage-map row (README:255) vs entry content — matches, no overclaim

Row: «the grader is a deterministic state comparison — `record.csv` vs `expected_ratio.csv`
within the executed 0.05% tolerance — preceded by two side-effect checks, one of which fails
open; the S097 survey separates Meta-evaluation from methodology, so judge-based scoring owns
its validation part. Not runtime task validity (PROVINCE refuses it), not contamination
measurement, not deployment config.»

Verified against the fetched `main.py` @ `9be8d8fe`:

- Deterministic state comparison: `validate_record_data` compares `record.csv` conversion
  rates against `groundtruth_workspace/expected_ratio.csv` (main.py:56–58, :63); a
  case-insensitive scan for `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic` finds no
  LLM/judge path (0 hits). ✓
- Executed 0.05 tolerance: signature default `tolerance_pct: float = 0.1` (main.py:58); call
  site `# Validate with 0.05% tolerance` then `validate_record_data(actual_records,
  expected_records, tolerance_pct=0.05)` (main.py:279–280). The comparison is applied to
  percentage values («±{tolerance_pct}%», main.py:86/:93), so «0.05% tolerance» and the
  entry's «0.05 percentage points» are the same unit/magnitude. ✓
- Two side-effect checks, one fails open: `validate_task_completion` runs
  `check_storage_bucket_exists("promo-assets-for-b")` (prefix-existence check over the
  project-wide bucket list, main.py:125–166) and `check_abtesting_logging_bucket_clean`
  (main.py:168–218); the log-bucket check fails open on error: `return True  # Don't fail
  evaluation if we can't check logs` (main.py:217–218). The record comparison runs after both
  (`grade_with_retry(_check_completion)` first, then `validate_record_data`), so «preceded by»
  is accurate. ✓
- S097 five-part: fetched arXiv 2412.05579v2 abstract contains «This paper presents a
  comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality,
  Methodology, Applications, Meta-evaluation, and Limitations.» Meta-evaluation is distinct
  from methodology; «judge-based scoring owns its validation part» mirrors the entry's own
  framing («a deterministic comparison needs no judge meta-evaluation, while an LLM judge
  does» — entry:63–67). ✓
- The three refusals in the row reproduce the entry's refusals verbatim. ✓
- Sources cited in the row (S093, S094, S097) are exactly the entry's three `source:` lines;
  registry rows S093/S094/S097 are `mined`, `opened=2026-10-25`, and `used-by` names the
  entry (S093 `used-by` now includes both the verifier-execution and grader-semantics entries);
  the entry has exactly one knowledge-index row (README:67). ✓

**Verdict for check 2: matches; no overclaim found.**

## 3. Wording notes (non-verdict, adjacent)

- The row's «so judge-based scoring owns its validation part» compresses the entry's explicit
  caveat that the classification is the entry's own framing and the abstract «only separates
  the parts» (entry:66–67). The row does not attribute the conclusion to S097 directly, so it
  is not an overclaim, but a strict reader could misread it as the survey's own assertion.
- Entry-internal (NOT in the README lines under review): the entry and the S094 registry row
  say «the whole gate is retried up to three times five seconds apart»; in the fetched code
  only the side-effect phase is wrapped in `grade_with_retry` (`_check_completion` calls just
  `validate_task_completion`; record validation at main.py:275–281 is not retried).
  `utils/evaluation/retry.py:44-45` `DEFAULT_MAX_ATTEMPTS = 3` / `DEFAULT_POLL_S = 5` are
  confirmed at the pinned commit. This is a precision nit in the entry/SOURCES, not in the
  frontier wording this seat verifies.

VERDICT: scope-accurate
