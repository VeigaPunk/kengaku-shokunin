source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` and `…/tests/parser.py` — commit `66f92766bba642462d4bbe5479e83f91f9211862`, accessed 2026-10-25
source: S094 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, accessed 2026-10-25
source: S097 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the three pinned revisions (SWE-bench_Pro-os 66f92766, Toolathlon 9be8d8fe, arXiv 2412.05579v2) and re-locate every quoted span before citing this entry (next due 2027-04-23)
writer: KengakuR32

# Benchmark grader semantics — what the grading code compares, and what it cannot see

The round-31 entry `corpus/knowledge/benchmark-verifier-execution-model.md` recorded where two
benchmarks' verifiers run and what is restored before grading. This entry records the other half
of the task-spec audit axis E ("grader integrity"): what the grading code *compares*, with what
tolerance, and whether a judge is in the path, read from the same pinned trees. It **extends**
the round-31 entry, and it discharges the README frontier bullet-1 clause "and for Toolathlon"
(`corpus/README.md:276`) **for the one task whose evaluation script is read** — the Toolathlon
`ab-testing/evaluation/main.py` at `9be8d8fe`. The abstract's taxonomy motivates this entry's
own distinction between deterministic and judge-based scoring; that causal link is not asserted
by the source. It is not runtime task validity (`PROVINCE.md` refuses that to this lane), not
contamination measurement, and not deployment configuration.

**Source labels (Q5).** S093 is a benchmark maintainer's own task-grading code at a pinned
commit; S094 is Toolathlon's own task-evaluation script at a pinned commit; S097 is an arXiv
preprint. Each is a primary artefact of the party it describes, not an independent measurement.
Nothing here was executed against either benchmark: every claim below is a reading of code and of
an abstract page, quoted byte-for-byte from the pinned revisions.

## S094 — Toolathlon's ab-testing grader is a deterministic state comparison with a call-site tolerance

`tasks/finalpool/ab-testing/evaluation/main.py` contains no model or judge call: a
case-insensitive scan for `prompt|judge|model|openai|chat|gpt|llm|claude|anthropic` finds no
such scoring path. Its non-standard imports include cloud/storage libraries and the retry
wrapper; the `gcloud` CLI is a fallback for the storage check. The scoring path compares a
produced `record.csv` against `groundtruth_workspace/expected_ratio.csv`:

> `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — 11 words, `main.py:58`

The signature default is 0.1%, but the executed call overrides it:

> `# Validate with 0.05% tolerance` — 4 words, `main.py:279`
> `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — 5 words, `main.py:280`

So the operative tolerance is set at the call site, not by the default: the task is graded by a
comparison of conversion rates within **0.05 percentage points** per scenario, and one missing or
extra scenario name fails the task (`main.py:70` `Missing scenarios:`, `:72` `Unexpected
scenarios:`, `:100` `raise ValueError(f"Record validation failed:`)`.

Before the record comparison, the script runs a side-effect check that confirms a matching
storage-bucket prefix (`main.py:134-139`) and checks whether the ab-testing logging bucket
contains unexpected entries. The log check returns `True` both for a clean bucket and for
some caught exceptions (`main.py:213-218`); that does not mean every inability to perform the
check passes. When credentials are unavailable, the function can fall through without a
truthy result and the task-completion check raises instead. A failure of that specific exception
path is not the same as a failure of the grader as a whole.

`utils/evaluation/retry.py:44-45` sets `DEFAULT_MAX_ATTEMPTS = 3` and `DEFAULT_POLL_S = 5`;
the retry wrapper applies to the task-completion side-effect check, not the later record
comparison. It therefore provides at most three attempts for that check; it does not retry
the full scoring path or turn an implicit-`None` result into success.

## S097 — the survey frame: meta-evaluation is its own part

The field's own LLM-as-judge survey names the paradigm's parts:

> `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations.` — 20 words, arXiv 2412.05579v2 Abstract

Meta-evaluation is kept distinct from methodology. This entry reads that structure as a
taxonomic hint, not as a prescription: a benchmark's grader should be classified by what it
compares before its validation protocol is chosen — a deterministic comparison needs no judge
meta-evaluation, while an LLM judge does. That classification is this entry's own framing; the
abstract itself only separates the parts.

## S093 — restated, not repeated

The round-31 entry already established, from the same pinned `tests/test.sh` and `parser.py`,
that a SWE-bench Pro V2 task's reward is binary set containment over a log-derived, last-write-
wins `PASSED` set, and that the reset restores tracked test code but not newly added fixture
files. This entry restates that result and does not repeat its derivation; the S093 row is cited
here because the binary-containment claim is the contrast case: SWE-bench Pro V2 and Toolathlon
both grade without an LLM judge, but by different mechanisms (set containment vs state comparison
with a tolerance).

## What this does not establish

- It does not establish what any Toolathlon task *outside* the `ab-testing` family uses; a
  different task directory may carry a different evaluator.
- It does not certify task validity, nor measure contamination, nor run any benchmark.
- It does not claim the `0.1` default is ever executed for this task; the executed call is the
  `0.05` value, and the default is read only as the function's declared signature.
- It does not establish that the log-bucket check ever runs against a real Cloud Logging
  deployment; the clean path returns `True`, some caught exceptions do too, while credential
  failures can fall through to implicit `None` and fail the task. Those error paths differ.

## Falsifier

Two observations would falsify this reading at the pinned revision: a scoring path in this
`main.py` that invokes an LLM judge; or evidence that the sole `validate_record_data` call
does not pass `tolerance_pct=0.05`. A behavior change in another Toolathlon task would not
falsify this entry's one-task claim; it would require a new source and a separate entry.
