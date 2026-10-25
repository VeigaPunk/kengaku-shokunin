# R32DraftEntry — C1 entry draft: benchmark-grader-semantics.md (2026-10-25)

Seat: `L1Kengaku32.R32DraftEntry` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at baseline `f20a1097`, claims freeze `plans/round-32-claims.md` (0d32691d). Deliverable: the
entry as this lane would admit it, drafted here, not as a lane file. No lane file was created,
edited or deleted by this seat; scratch `/tmp/r32-R32DraftEntry/` is empty (no captures of my
own were needed beyond the seats' verified captures). No tool installed or upgraded (curl +
stdlib only; no channel change).

## Quotes' provenance

Every quote below is verbatim bytes and is attributed to the seat report that captured and
located it, with that report's file:line:

- S093 quotes: `.ufo/waves/round-31/build/R31SrcS093a.md` (scout, pin `66f92766`) and
  `.ufo/waves/round-31/build/R31SrcS093b.md` (scout, pin `66f92766`).
- S094 quotes: `.ufo/waves/round-32/build/R32SrcS094a.md` and `R32SrcS094b.md` (scouts,
  pin `9be8d8fe`), fetched capture `/tmp/r32-R32SrcS094a/main.py` (14,138 B, sha256
  `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`). I verified the
  capture is byte-identical to the pinned revision via one GitHub contents API call at
  `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` (direct comparison, sha256 equal).
- S097 quotes: `.ufo/waves/round-32/build/R32SrcS097.md` (scout, arXiv 2412.05579v2), fetched
  capture `/tmp/r32-R32SrcS097/arxiv-2412.05579v2.html` (43,661 B, sha256
  `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660`).
- Capture identity also cross-checked against `R32LearnC1.md` (digest table) and
  `R32Frontier.md` (frontier clause text).

Word counts printed per quote span.

---

## The draft

```markdown
source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` (reset + reward block) and `…/tests/parser.py` — commit `66f92766bba642462d4bbe5479e83f91f9211862`, accessed 2026-10-25
source: S094 — https://github.com/hkust-nlp/Toolathlon — `tasks/finalpool/ab-testing/evaluation/main.py` — commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`, accessed 2026-10-25
source: S097 — https://arxiv.org/abs/2412.05579v2 — `# Abstract` — arXiv 2412.05579v2 (preprint), accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the three pinned revisions (SWE-bench_Pro-os 66f92766, Toolathlon 9be8d8fe, arXiv 2412.05579v2) and re-locate every quoted span before citing this entry (next due 2027-04-23)
writer: KengakuR32

# Benchmark grader semantics — what the grading code compares, and what it cannot see

The round-31 entry `corpus/knowledge/benchmark-verifier-execution-model.md` recorded where two
benchmarks' verifiers run and what is restored before grading. This entry records the other half
of axis E ("grader integrity"): what the grading code *compares*, with what tolerance, and
whether a judge is in the path, read from the same pinned trees. It extends the round-31 entry
rather than repeating it, and it discharges the README frontier bullet-1 clause "and for
Toolathlon" (corpus/README.md:276) for **Toolathlon's scoring code** — the task evaluation
script — only. It is not runtime task validity (PROVINCE refuses that to this lane).

**Source labels (Q5).** S093 is a benchmark maintainer's own task-grading code at a pinned
commit; S094 is Toolathlon's own task-evaluation script at a pinned commit; S097 is an arXiv
preprint (see §S097). Each is a primary artefact of the party it describes, not an independent
measurement. Nothing here was executed against either benchmark: every claim below is a reading
of code and an abstract page.

## S093 — SWE-bench Pro V2's grade is set containment over a log-derived PASSED set

The task's own `tests/test.sh` restores the test surface and then computes the reward from
`tests/config.json`:

> `all_required = fail_to_pass | pass_to_pass` — 5 words, `tests/test.sh:213`
> (quoted at `R31SrcS093b.md:36`)

> `success = all_required <= passed_tests` — 5 words, `tests/test.sh:214`
> (quoted at `R31SrcS093b.md:37`)

The reward is binary: the union of `fail_to_pass` and `pass_to_pass` must be a subset of the
set of names the parser recorded as `PASSED`, with no threshold and no partial credit:

> "100 % of the required ids, no threshold, no partial credit, no weighting" — 13 words,
> `R31SrcS093b.md:136-137`

The `PASSED` set is not a test-runner verdict; it is scanned from a log the agent-modified code
writes into, deduped last-write-wins:

> "S093's reward is binary set containment (`test.sh:213-214`) over a log-derived,
> last-write-wins, agent-writable `PASSED` set" — 14 words, `R31SrcS093b.md:180`

> "it cannot distinguish a `PASSED` token emitted by pytest from one emitted by the code under
> test" — 17 words, `R31SrcS093b.md:139-141`

Round 31 executed this parser and the grader's own shell logic on a scratch copy and reproduced
the consequence:

> "I produced reward 1 with all 20 required tests failing (§4.3)." — 11 words,
> `R31SrcS093b.md:161-162`

Two scope facts keep the reading honest. The reward rule is shared across the benchmark's tasks
— a 9/10 sampled observation over 7 repositories — so "binary set containment" is
benchmark-wide; the parser, however, is per-instance, so the log-scan reading is this task's
variant, not every task's:

> ""single shared file" is a 9/10 observation (teleport differs by a 2-line environment fix
> outside the reward block)" — 18 words, `R31SrcS093b.md:177-178`

> "All 82 openlibrary tasks fetched: **21 distinct sha256** variants (largest cluster 15)." —
> 12 words, `R31SrcS093b.md:123`

The environment reset is the task's own script, not a harness re-upload; the test surface is
restored from the container's git `HEAD`, and untracked files the patch only modifies are left
alone:

> "Source of truth is the image's object store, not a harness upload." — 13 words,
> `R31SrcS093a.md:59`

> "re-uploading tests is **not** a precondition of this reset" — 9 words, `R31SrcS093a.md:95`

> `# untracked files the patch merely MODIFIES are left alone (image-provided context)` —
> 11 words, `R31SrcS093a.md:70`

## S094 — Toolathlon's ab-testing grader is a state comparison with a numeric tolerance

`tasks/finalpool/ab-testing/evaluation/main.py` at commit `9be8d8fe` is the whole scoring path
for this task. Its validator compares the agent's `record.csv` against
`groundtruth_workspace/expected_ratio.csv`:

> "compares the agent's `record.csv` conversion rates against ground-truth `expected_ratio.csv`
> within a fixed absolute numeric tolerance (0.05% in main), with no LLM/judge path." —
> 22 words, `R32SrcS094b.md:56`

The function signature declares a default tolerance of 0.1 percentage points:

> `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` — 11 tokens, `main.py:58` (quoted at `R32SrcS094a.md:5`)

The runtime call, however, passes 0.05, not the default:

> `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` — 3 tokens,
> `main.py:280` (quoted at `R32SrcS094b.md:20`)

Missing and extra scenarios are validation errors, and any conversion-rate difference beyond the
tolerance is an error:

> "This file establishes that its validator compares shared-scenario A/B conversion rates
> against an absolute tolerance_pct default of 0.1 and treats missing/extra scenarios as
> validation errors" — 25 words, `R32SrcS094a.md:14`

On any error the validator raises `ValueError`; on success it returns `None` and the script
prints a success message:

> `raise ValueError(f"Record validation failed:\n{error_msg}")` — 3 tokens, `main.py:100` (span cited at `R32SrcS094a.md:12`; byte-verified at the pinned capture)
> "on success it prints the success message and falls through without a value, so returns None" — 16 words, `R32SrcS094a.md:12`

Before the comparison, a completion gate runs. It checks infrastructure state, not model
output:

> "gates on binary infrastructure state (GCS bucket existence by prefix listing; Cloud Logging
> bucket cleanliness by entry-count within a launch-to-eval time window)" — 22 words,
> `R32SrcS094b.md:53-55`

> `bucket_exists = check_storage_bucket_exists("promo-assets-for-b")` — 4 tokens, `main.py:225`
> (quoted at `R32SrcS094b.md:26`)

> `if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` — 6 tokens,
> `main.py:234` (quoted at `R32SrcS094b.md:27`)

Execution order matters: the completion gate runs first (retry-wrapped, `main.py:257,262`),
then `record.csv` is read and compared (`main.py:273-280`) — not the reverse:

> "Main flow (`__main__`, :237-297), in execution order:" — 7 words, `R32SrcS094b.md:12`

Two nuances are readable from the same bytes and belong in the record. First, the log-bucket
cleanliness check is fail-open on infrastructure errors: its `except` branch returns `True`
("Don't fail evaluation if we can't check logs", `main.py:216-218`), so a log check that
cannot run does not fail the grade. Second, the only `subprocess` invocation in the file is the
`gcloud storage buckets list` CLI, not an LLM:

> "The only `subprocess` invocation is the `gcloud storage buckets list` CLI (:149-152), not an
> LLM." — 16 words, `R32SrcS094b.md:45`

No judge prompt, rubric, or LLM call appears anywhere in the file; the one non-stdlib,
non-google import is a pure poll-retry loop:

> "no judge prompt, rubric, or LLM call appears anywhere in the file." — 12 words,
> `R32SrcS094b.md:49`

> "is a pure poll-retry loop (`time.sleep`, max 3 attempts, no LLM calls)" — 12 words,
> `R32SrcS094b.md:46-47`

## S097 — the survey frame: deterministic graders and LLM judges are distinct kinds

S097 is the field's own LLM-as-judge survey. It is a preprint: arXiv 2412.05579v2, submitted
7 Dec 2024, last revised 10 Dec 2024, with no journal/venue affiliation on the abstract page:

> "Status: **preprint** — arXiv preprint (no journal/venue affiliation on the abstract page" —
> 13 words, `R32SrcS097.md:27`

> "the paper exists as an arXiv preprint (v2, 2024-12-10)" — 12 words, `R32SrcS097.md:32`

Its abstract names the frame that organises the field into five perspectives, keeping
meta-evaluation separate from methodology and limitations:

> "This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key
> perspectives: Functionality, Methodology, Applications, Meta-evaluation, and Limitations." —
> 20 words, `R32SrcS097.md:20`

The practical consequence for this lane: a benchmark's grader should be described by what it
compares and against what, not by the binary "is it an LLM judge?". SWE-bench Pro V2's grader
is a deterministic containment test with a binary reward (§S093); Toolathlon's ab-testing
grader is a deterministic state comparison with a stated numeric tolerance (§S094); an LLM
judge would be a third kind with its own meta-evaluation requirements, and neither of the two
graders read here is one. The lane's judge-calibration work belongs to the meta-evaluation
perspective of this frame, which the survey keeps distinct from methodology on purpose.

## What this does not establish

- **Not runtime task validity.** This entry does not audit whether either task is well-posed,
  whether its tests are the right tests, or whether its reward is meaningful
  (PROVINCE refuses runtime task validity to this lane).
- **Not the whole of Toolathlon.** S094 is one task's evaluator (`ab-testing`) among the
  benchmark's task-specific evaluators; the other evaluators are not read here, so no claim is
  made about them. A state comparison with a tolerance is a statement about this file, not a
  benchmark invariant.
- **Not an observed run.** Every claim above is read from code at pinned commits; no Toolathlon
  or SWE-bench Pro V2 trial was executed or read, so fail-closed/fail-open readings are code
  properties, not observed behaviour.
- **Not every SWE-bench Pro V2 parser.** The log-scan reading is the openlibrary instance's
  parser variant (one of 21 observed for that task family, per `R31SrcS093b.md:123-131`);
  the reward rule is shared, the parser is not.
- **Not an endorsement of the survey.** S097's five-perspective structure is used as an
  organising frame; the entry does not assert the survey's other claims, and as a preprint it
  has not passed peer review.

## Falsifier

- A Toolathlon commit at the same pin whose `ab-testing/evaluation/main.py` calls an LLM
  judge, passes a tolerance other than 0.05 in `__main__`, or returns a scalar grade unrelated
  to the `record.csv` comparison would falsify §S094. A captured ab-testing trial receipt
  showing PASS while `record.csv` contained an extra scenario — or a missing one — would
  falsify the fail-closed reading.
- A SWE-bench Pro V2 trial whose reward file contradicts `parser.py`'s log scan — e.g. a
  required test that failed and was still counted as passed — would falsify the log-scan
  reading and imply some other path writes the reward.
- A later arXiv version of 2412.05579 whose abstract no longer names the five perspectives
  would break the S097 anchor; re-checking the pin is the recheck action above.

## Extends

- **`corpus/knowledge/benchmark-verifier-execution-model.md`** — that entry settled where
  grading runs and what is restored; this entry settles what the grading code compares. It
  names that entry, supersedes nothing in it, and repeats none of its execution findings (Q6).
- **`corpus/README.md` §Frontier bullet 1** — the round-31 discharge left the clause "and for
  Toolathlon" open (line 276); this entry discharges it for Toolathlon's scoring code — the
  task evaluation script — only. The clause stays open for the other benchmarks' scoring code
  and for runtime task validity, and this entry claims neither.
- **Not extended:** contamination cards, task-validity checklist rows and judge-calibration
  entries are untouched; no contamination, novelty, difficulty or performance claim is made
  here.
```

---

## Preconditions for landing (outside the entry body; C1's predicate depends on them)

1. `corpus/SOURCES.md` — S093 exists (`opened=2026-10-25`, `status=mined`); its `used-by`
   cell gains this entry. S094 and S097 are new rows: `status=mined`, `opened=2026-10-25`,
   `used-by` naming `corpus/knowledge/benchmark-grader-semantics.md` (the staged rows carry
   `opened=2026-10-23`; the date must move to 2026-10-25 because each pin was re-opened today).
2. `corpus/README.md` — exactly one index row for the entry (the round-32 index-row wording
   and coverage-map row named in `R32Frontier.md`), landing with the entry file in the same
   commit (Q7).
3. The entry file itself lands byte-for-byte as drafted above, with the `writer:` line intact
   and the three `source:` lines exactly S093/S094/S097.

VERDICT: draft-ready
