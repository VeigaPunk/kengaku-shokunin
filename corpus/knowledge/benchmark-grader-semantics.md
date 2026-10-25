source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` and `…/tests/parser.py` — commit `66f92766bba642462d4bbe5479e83f91f9211862`, accessed 2026-10-25
source: S103 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, accessed 2026-10-25
source: S104 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the three pinned revisions (SWE-bench_Pro-os 66f92766, Toolathlon 9be8d8fe, arXiv 2412.05579v2) and re-locate every quoted span before citing this entry (next due 2027-04-23)
writer: KengakuR33 (admission patch of the round-32 draft)

# Benchmark grader semantics — what the grading code compares, and what it cannot see

The round-31 entry `corpus/knowledge/benchmark-verifier-execution-model.md` recorded where two
benchmarks' verifiers run and what is restored before grading. This entry records the other half
of the task-spec audit axis E ("grader integrity"): what the grading code *compares*, with what
tolerance, and whether a judge is in the path, read from the same pinned trees. It **extends**
the round-31 entry, and it discharges the Toolathlon third of the README frontier bullet-1
instruction — "the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and
SWE-bench Pro" (`corpus/README.md:276`) — **for the one task whose evaluation script is read**,
the Toolathlon `ab-testing/evaluation/main.py` at `9be8d8fe`. That is also the item the round-31
bullet leaves open by name: "and for Toolathlon" (`corpus/README.md:278`). The abstract's taxonomy
motivates this entry's own distinction between deterministic and judge-based scoring; that causal
link is not asserted by the source. It is not runtime task validity (`PROVINCE.md:219-220` keeps
that outside this lane: "it does not run a benchmark, certify a task, or own deployment
configuration, runtime task validity, hosted judges, contamination measurement"), not
contamination measurement, and not deployment configuration.

**Source labels (Q5; ids renumbered round 33 — the staged package's S094→S103 and S097→S104 after
round-32 id collisions; the round-32 refusal rows at S094/S097/S101/S102 stand unchanged and no
id is reused).** S093 is a benchmark maintainer's own task-grading code at a pinned commit; S103
is Toolathlon's own task-evaluation script at a pinned commit; S104 is an arXiv preprint. Each is
a primary artefact of the party it describes, not an independent measurement. Nothing here was
executed against either benchmark: every claim below is a reading of code and of an abstract page,
quoted byte-for-byte from the pinned revisions.

**Reading basis.** This round's committed captures are
`.ufo/waves/round-33/assimilation/captures/toolathlon-ab-testing-evaluation-main.py` (14,138
bytes, sha256 `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`),
`…/toolathlon-utils-evaluation-retry.py` (4,519 bytes, sha256
`db11e66ec241e1c5d00327b0bf7209c20323c4582c827e62b7a261235c17f69e`) and
`…/arxiv-2412.05579v2-abs.html` (43,661 bytes, sha256
`44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660`); the directory's
`SHA256SUMS.txt` carries the same three digests. No S093 file is in this wave's capture set: the
S093 section below is a restatement of the round-31 entry, whose quotes resolve at the same pin,
and its anchors were re-located against `test.sh` and `parser.py` at `66f92766` this round
without re-execution.

## S103 — Toolathlon's ab-testing grader is a deterministic state comparison with a call-site tolerance

`tasks/finalpool/ab-testing/evaluation/main.py` contains no model or judge call: a
case-insensitive scan for `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic` matches no
line at all in the 297-line file. Its non-standard imports are cloud/storage libraries
(`google.cloud` `storage` and `logging`, `google.oauth2.service_account`,
`google.api_core.exceptions`, `main.py:6-8`) and the retry wrapper (`main.py:12`); the `gcloud`
CLI is a fallback for the storage check (`main.py:145-166`). The scoring path compares a produced
`record.csv` against `groundtruth_workspace/expected_ratio.csv` (`main.py:53-56`):

> `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — 11 whitespace-separated tokens, `main.py:58`, the **signature default**

The default is not what runs. The function's single call site overrides it:

> `# Validate with 0.05% tolerance` — 4 words plus the `#` marker, `main.py:279`
> `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — 3 whitespace-separated tokens, `main.py:280`

So the operative tolerance is set at the call site, not by the default: the executed check is
`diff > tolerance_pct` on each scenario's A and B conversion rate (`main.py:84`, `:91`), i.e. a
difference of **0.05** in the unit the rates are printed in, and a missing or extra scenario name
fails the task (`main.py:70` `Missing scenarios:`, `:72` `Unexpected scenarios:`, `:100` `raise
ValueError(f"Record validation failed:`)`. [INFERENCE] The rates are formatted with a trailing
`%` in the same message that prints the tolerance (`main.py:86`, `:93`), so the compared unit is a
percentage point; the comment calls 0.05 "0.05%". The source never spells out the unit in prose,
which is why this gloss is marked rather than quoted.

Before the record comparison, and first in the process order, the script runs a side-effect check
that confirms a matching storage-bucket prefix (`check_storage_bucket_exists`, `main.py:125-166`,
called at `:225`) and requires the ab-testing logging bucket to contain no entries
(`check_abtesting_logging_bucket_clean`, `main.py:168-218`, called at `:234`).

The log check has two `return True` sites, and they are not the same path. The clean-bucket path
prints and returns `True` (`main.py:213-214`). The single broad `except Exception` handler prints
a warning and returns `True` too, on the line whose own comment reads `# Don't fail evaluation if
we can't check logs` (`main.py:216-218`). That handler **is** a caught-exception True path: any
failure raised inside the guarded block after credentials exist — client construction,
`list_entries`, payload inspection — is caught there and read as a clean bucket.

Credential failure is not that path and does not reach that handler. `get_project_id_and_credentials`
returns `(None, None)` on `FileNotFoundError` (`main.py:118-120`) and on any other exception
(`:121-123`). The log check then tests `if project_id_from_creds and credentials:` (`:176`); with
`(None, None)` the guard is false, the guarded block never runs, no `return` executes, and the
function falls off its end returning an implicit `None`. `validate_task_completion` tests `if not
check_abtesting_logging_bucket_clean(...)` (`:234`), and `not None` is true, so it raises
`ValueError` (`:235`). The storage check fails closed in the same direction: with no credentials
its guard at `:132` is false and control falls to the `gcloud` fallback (`:145-166`), which
returns `False` when the CLI is unavailable (`:164-166`), raising at `:230`. A missing
`log_bucket_name.txt` is not caught at all — the file is opened at `:171-172`, outside the `try`
that starts at `:173`. So the log check mixes one narrow fail-open caught-exception path
(`:216-218`) with fail-closed credential and missing-file paths; "the log-bucket check fails
open" is true only of that handler.

`utils/evaluation/retry.py:44-45` sets `DEFAULT_MAX_ATTEMPTS = 3` and `DEFAULT_POLL_S = 5`. The
retry wrapper applies to the task-completion check, not to the later record comparison:
`_check_completion` calls `validate_task_completion` and converts any exception into
`(False, str(e))` (`main.py:255-260`), and `grade_with_retry(_check_completion)` is invoked at
`:262` with no `max_attempts` override, so the default budget of three attempts holds. The record
comparison at `:280` sits outside that wrapper; its own `try` prints the error and calls `exit(1)`
(`:293-295`). Both a completion failure (`:263-265`) and a record-validation failure (`:293-295`)
end the process non-zero; the retry changes only how many times the completion check is tried —
at most three — never whether an implicit `None` counts as success.

## S104 — the survey frame: meta-evaluation is its own part

The field's own survey is `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation
Methods` (arXiv 2412.05579v2; title as served in the capture's `citation_title` meta tag). It
names the paradigm's parts:

> `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` — 20 words, arXiv 2412.05579v2 Abstract (`…-abs.html:124`)

The capitalisation differs between the two source locations and neither form is a transcription
error: the title capitalises `Judges` (`LLMs-as-Judges`, `…-abs.html:41`), while the abstract body
writes `LLMs-as-judges` lowercase (`:124`). The quote above reproduces the abstract
byte-for-byte.

Meta-evaluation is kept distinct from methodology. This entry reads that structure as a
taxonomic hint, not as a prescription: a benchmark's grader should be classified by what it
compares before its validation protocol is chosen — a deterministic comparison needs no judge
meta-evaluation, while an LLM judge does. That classification is this entry's own framing; the
abstract itself only separates the parts.

## S093 — restated, not repeated

The round-31 entry already established, from the same pinned `tests/test.sh` and `parser.py`,
that a SWE-bench Pro V2 task's reward is binary set containment over a log-derived, last-write-
wins `PASSED` set, and that the reset rewrites the tracked test-code surface while a file under a
data-directory parent is excluded from that rewrite. This entry restates that result and does not
repeat its derivation; the S093 row is cited here because the binary-containment claim is the
contrast case: SWE-bench Pro V2 and Toolathlon both grade without an LLM judge, but by different
mechanisms (set containment vs state comparison with a tolerance).

The restated anchors were re-located against the pinned bytes this round: `all_required =
fail_to_pass | pass_to_pass` then `success = all_required <= passed_tests` (`test.sh:213-214`);
the passed side is built by keeping only tests whose parsed status is `PASSED` (`test.sh:207-210`)
from a log scan whose record pattern is `^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR)`
applied to stdout and again to stderr (`parser.py:68`, `:88-90`), deduped by name with
`unique_results = {result.name: result for result in results}.values()` (`parser.py:121`), i.e.
last write wins; and the reset's `git checkout HEAD -- "$path"` restores tracked test code
(`test.sh:71`) while `is_test_code` returns false whenever a parent directory is in `DATA_DIRS`
(`testdata`, `test_data`, `fixtures`, `fixture`, `mocks`, `mock`, `__snapshots__`,
`test.sh:38`, guard at `:43-44`), so a file the agent adds under one of those parents never enters
the reset list.

## What this does not establish

- It does not establish what any Toolathlon task *outside* the `ab-testing` family uses; a
  different task directory may carry a different evaluator.
- It does not certify task validity, nor measure contamination, nor run any benchmark.
- It does not claim the `0.1` default is ever executed for this task; the executed call passes
  `tolerance_pct=0.05` at `main.py:280`, and the `0.1` is read only as the function's declared
  signature (`:58`).
- It does not establish that either side-effect check ever runs against a live Cloud Storage or
  Cloud Logging deployment; the clean log path returns `True` (`:214`), the broad
  caught-exception path returns `True` (`:216-218`), while credential failure falls through to
  implicit `None` and raises (`:234-235`). Those paths differ, and only the second is fail-open.
- It does not establish the unit of `tolerance_pct` from prose; the percentage-point reading is
  marked [INFERENCE] above and rests on the `%` formatting in the failure message, not on a
  stated unit.

## Falsifier

Three observations would falsify this reading at the pinned revision: a scoring path in this
`main.py` that invokes an LLM judge; evidence that the sole `validate_record_data` call does not
pass `tolerance_pct=0.05`; or a second caught-exception `return True` site in
`check_abtesting_logging_bucket_clean` beyond `main.py:216-218`. A behavior change in another
Toolathlon task would not falsify this entry's one-task claim; it would require a new source and
a separate entry.
