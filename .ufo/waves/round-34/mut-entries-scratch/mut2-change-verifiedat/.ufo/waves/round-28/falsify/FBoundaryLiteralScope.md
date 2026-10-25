# FBoundaryLiteralScope — C2 literal coverage vs semantic support; S050 corrective index vs S058 authority

seat: KengakuR28.FBoundaryLiteralScope (critic, author-side; not outside/non-author evidence)
date: 2026-10-21
candidate (frozen draft): `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`
SHA256 `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (writer KengakuR28), complete re-read.
Canonical candidate path `corpus/knowledge/webarena-task-spec-audit.md` is absent (not admitted); this report is not about those bytes.

Inputs I read, with their digests at read time: `plans/round-28-claims.md` d406d222…9afb (prereg + Amendment 1),
`corpus/lessons/round-28.md` 19ccfe2c…2f2b, `corpus/SOURCES.md` 014175dd…19a1, `plans/registry_check.py`
41561dfb…a79a4, `corpus/knowledge/extraction-policy-comparison.md` 17df54f9…9eb9d77, population.json 1a5073fc…3014,
round-27 lesson, QUALITY Q17, build OpenS050/OpenS058/CritCausalSeparation, build-acceptance receipts.
Pinned `_pattern.py` scratch copies under OpenS050/OpenS058: both 7974ddb4…aba79a4 (the same bytes).

Axes: calibration (primary), novelty/coverage (unchanged). No production file was edited.
Scratch: `.ufo/waves/round-28/scratch/FBoundaryLiteralScope/` (census.py, sources.diff, probe/). The probe ran with bytecode
disabled; it wrote 0 `__pycache__` directories.

## Independent replay (passes, my own code)

I wrote `census.py` from scratch; it does not import `registry_check.py` or the oracle.
- Baseline export `b9b24796` gives 12 row-file links, with findings S038 status=queued, S038 missing used-by
  attribution-interval-calibration.md, and S050 missing used-by extraction-policy-comparison.md. That is 2 rows and 3 findings,
  equal to `registry-baseline-red.stdout`.
- The current tree gives 12 links and 0 findings. The citing-file sets equal the baseline sets: the round28 errata add
  no new row-file edge for any of the 13 frozen IDs, which satisfies Amendment 1 §5.
- The 35 population paths are exactly the 35 files in `git ls-tree b9b24796 corpus/knowledge/`, so no frozen-population
  file is silently excluded.
- A variant-form search (`S 50`, `S-050`, `S50`, ranges such as `S049–S059`, `source 50`) found one hit,
  bench-arena-round12-ladder.md:58 "draft's 56/42". That is a false positive, so the literal regex misses no reference.
- A cell-level diff of SOURCES against the baseline shows only these changes: S038 status queued→mined and used-by
  —→attribution-interval-calibration.md, and S050 used-by plus extraction-policy-comparison.md. New rows are S061–S066
  only, and no immutable cell changed. `registry-only-delta.json` original_sources_sha256 b1a74eb5…c62e equals
  `git show b9b24796:corpus/SOURCES.md | sha256sum`.
- Both knowledge errata are append-only (0 deleted lines: +24 and +16). Line 18 "(S058, correcting S050)" is the same as
  the baseline, which satisfies R1.
- Lesson numbers check out: 12 links across 2 files, 13 rows / 35 paths, 33 zero-reference paths, S060 uncited (M72),
  baseline red 2/3, S050-only still red on S038 alone, S038-only delta green, selftest12.

## Findings

### F1 — the candidate's adjacent-claim wording is contradicted: new rows outside the 13 do enter C2's verdict (fixable, calibration)

Candidate lines 137–138 say C2 "reads only its frozen baseline knowledge paths and source rows". Amendment 1 §4 says
"New rows do not enter its verdict." But `registry_check.py:25–49` parses every row under `## Registry`, and it raises
`malformed_source_row` / `duplicate_source_id` for any ID. Line 151 makes any finding exit 1, and `mismatch_sources`
counts every finding that carries a `source` key.

Counterexample, on a scratch copy with the population pin intact:
- Control: `source_rows_checked=13 … reference_links=12 mismatch_sources=0 finding_count=0 exit=0`.
- Drop the used-by cell from the new C1-owned row S064 (outside the 13): `FINDING malformed_source_row S064 line 86`,
  `mismatch_sources=1 exit=1`.
- Duplicate the new row S061: `FINDING duplicate_source_id S061 line 84`, `mismatch_sources=1 exit=1`.

So a defect in a C1 row turns C2 red, and the "mismatched rows" count can name a row outside the 13. The duplicate
check over the whole registry is preregistered ("Validate no duplicate IDs"), so the behaviour is defensible. The wording
"reads only" and "new rows do not enter its verdict" is what overclaims. The current measured values are unaffected,
because the tree is clean and the two-way revert receipts ran on the baseline export without new rows.

Smallest safe correction (L1 decides): reword the candidate's sentence, for example "checks status/used-by only for the
frozen 13 IDs across the 35 baseline paths; it parses the whole Registry table for row shape and duplicate IDs, so a
malformed or duplicate row anywhere still exits 1". Or scope those two findings to population IDs and add a selftest
case. Either way, the "row/cell partition" statement should say that row-shape validity is shared.

### F2 — the first-hit clause on line 18 rests on S050's anchor, not on S058's (pre-existing provenance-scope gap, non-blocking)

The header of extraction-policy-comparison.md:1 gives `_pattern.py:62–79,119–124` to **S058**. S058's registry anchor is
`pattern :86,:119–124 and scorer/_common.py:16–30`, and its teaches cell says "first-hit/no-fallback scope unchanged",
which defers first-hit to S050. Only S050's anchor holds `:62–64, :77–79`. In the pinned bytes, line 77 is
`match = re.search(`, the first-hit call.

OpenS058.md:29 and :56 also call 77–79 the "first-hit scope that is unchanged from S050". Line 18 attributes "takes a
first regex hit" to S058 alone. The round28 erratum (lines 122–126) adds "S050 occurs above only as the superseded reason
corrected by S058 … S058 remains the authority for that behavior". "That behavior" means the no-hit reason, so the
sentence is literally accurate. But it leaves a reader treating S058 as the only authority for line 18, while the only
registry row that anchors first-hit is S050.

This is not bogus provenance in the byte sense: it is the same file at the same commit, and S058's opener read it. It is
a row-anchor/claim mismatch inherited from round27. Round28 did not introduce it, and C2's literal contract cannot see it.
- Impacted axis: calibration (citation scope), not a C2 counter.
- Correction: one append-only erratum sentence, for example "line 18's first-hit clause and the header's 62–79 range are
  anchored by S050's accurate first-hit cells; S058 governs only the no-hit reason". This adds no new frozen-ID edge,
  because S050 is already cited in that file. Immutable anchor cells stay unchanged.

### F3 — the S050 row reads as provenance when taken alone (accepted tradeoff, bounded no-objection)

S050 is `mined`, tier A. Its teaches cell still says "no hit is invalid_response_format", the blanket reason, and its
used-by now names a knowledge file. Nothing in the S050 row points forward to S058; only S058's source cell says
"(corrects S050 blanket reason)". Before round28 the only S050 edge was the lesson, where it is labelled superseded
(round-27 lesson:159/203).

There is no cell-local fix within the contract:
- teaches is immutable (R1, prereg).
- A used-by annotation would break the checker: `safe_path`/`is_file` fails, raising `used_by_missing`.
- The lane's supersession convention is a forward-naming superseding row (S039/S040/S042, now S058/S064/S066).

The reversal is explicitly bounded to literal discoverability in Amendment 1 §3, lesson M67 and lines 55–57 and 70–72,
QUALITY Q17 ("never revives the superseded teaching"), and erratum lines 122–126. S058's used-by covers the same file.
Within the final wording I find no statement that turns S050 into support for the blanket reason.

Residual risk, which I record and do not convert into acceptance: any future consumer that treats `used-by`, or
`mined` plus `used-by`, as Q2 load-bearing support would read S050's inaccurate teaching as supporting
extraction-policy-comparison.md. corpus/README.md:105 defines used-by only as "pointers".

### F4 — ownership of S064–S066 is ambiguous (observation, low)

Amendment 1 §4 says "C1 owns new source rows", which includes S064–S066. CritCausalSeparation.md:51 says
"C1 owns rows S061–S063". S064–S066 are cited only by calibration errata inside the 35 baseline paths, and Amendment 1 §5
says those errata are separate from C1.

C2 does not check them; that exclusion is declared. So if C1-only rows were reverted, two of C2's own population files
would cite registry-absent IDs while C2 stays green. That is consistent with "literal coverage of 13 IDs only", but the
partition sentence should name the owner of S064–S066 explicitly.

## Bounded no-objections (my exact scope)

- The C2 counters, the red/green ordering and the S050-separate disclosure are reproduced, with no hidden S038-only
  credit.
- "Literal, not semantic" is stated consistently in the claims C2, the lesson Gate row, Q17, the checker scope string
  and the candidate.
- The S050 reversal is limited to indexing; S058 is still the stated no-hit authority, and no immutable cell changed.
- The candidate (draft bytes above) makes no S050/S058 or semantic-support claim. Its header cites only S061–S063.

## Tool installs

None.

VERDICT: PARTIAL — the C2 numbers and the S050/S058 boundary are supported. F1 is a factual overclaim in the frozen
candidate's adjacent-claim sentence (lines 137–138), contradicted by the scratch counterexample. F2 is an un-disclosed
first-hit anchor-scope gap. Neither changes any measured counter. Same-identity reread required if the candidate bytes change.

---

## v2 — same-identity re-read after repair (2026-10-21, appended; v1 above is preserved)

This v2 section re-reads the following bytes (digests verified at read time):
- candidate `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, SHA256
  `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182` (writer KengakuR28), complete re-read of the
  C2/partition/boundary text, lines 1–30 and 153–158;
- freeze `.ufo/waves/round-28/candidate-freeze-v2.json`, which pins that candidate and `registry_check.py` `fc388c33…379b`;
  both equal the on-disk digests;
- `plans/round-28-claims.md` 3079133b…4168 (Amendment 2), `corpus/lessons/round-28.md` bb989eb0…29d1 (M80 and the
  partition correction), `corpus/SOURCES.md` 255105f3…f8bf, `corpus/knowledge/extraction-policy-comparison.md`
  4d1882fa…5cfb.

The canonical `corpus/knowledge/webarena-task-spec-audit.md` is still absent.

### F1 → resolved (instrument and wording)

`registry_check.py:42–43` now drops IDs outside the 13 before the shape and duplicate checks. I reran the outside-row
witnesses on a fresh scratch copy (`scratch/FBoundaryLiteralScope/probe2`, bytecode disabled):

| mutation | result |
|---|---|
| none (control) | 13/35, links 12, mismatch 0, exit 0 |
| S064 drop used-by cell (v1 witness) | exit 0, 0 findings (was exit 1) |
| S061 duplicate (v1 witness) | exit 0, 0 findings (was exit 1) |
| S069 drop cell; S067 duplicate (new rows) | exit 0, 0 findings |
| frozen S050 drop cell (control) | `malformed_source_row` + `source_missing`, exit 1 |
| frozen S058 duplicate (control) | `duplicate_source_id`, exit 1 |
| unpaired fence after S061 / `## ` heading after S061 | exit 0 |
| unpaired fence after S037 (before frozen rows) | 13× `source_missing`, exit 1, fails closed |
| fenced fake S050 queued row after S069 | exit 0, ignored |

The `--selftest` gives 15 cases, exit 0, including `outside_duplicate_excluded` and `outside_malformed_excluded`.

I reran the baseline sequence with the new checker on a fresh `git archive b9b24796` root:
- the original baseline is red with 2 rows / 3 findings;
- the S050-only change is red on S038 alone;
- adding the S038 change makes it green.

My reconstructed final SOURCES hashes to `66e2235e…00fc`, equal to `both_sources_sha256` in the receipt. The
final-acceptance receipts and `commands.json` show the same exits. My independent `census.py` again gives baseline
12 links / 3 findings and current 12 / 0. The citing-file sets are unchanged, so the new erratum appends add no new
edge for any of the 13 frozen IDs.

The candidate's "reads only its frozen baseline knowledge paths and source rows" now holds at the verdict level. The one
remaining dependency is on non-row structural bytes: a fence or heading placed before the frozen rows. It fails closed
(red), never a false green. Amendment 2's "malformed/duplicate outside rows cannot enter its verdict" is exact. Lesson
M80 also discloses that whole-registry conformance stays with the separate fleet census.

### F2 → resolved (disclosed)

`extraction-policy-comparison.md` has an append-only clarification (+6/−0). It anchors first-hit at `_pattern.py:77–79`
(the pinned line 77 is `match = re.search(`). It states that S058's registry anchor "alone is not a line-level anchor for
the earlier search call" and that S050's ordering observation remains true, with only its blanket no-hit reason
superseded.

This matches the registry cells: S058 is `:86,:119–124`, S050 is `:62–64, :77–79, :119–124`. It does not contradict the
earlier erratum, because "occurs above only as the superseded reason" describes where S050 is mentioned, not its truth.
S058 is still the stated no-hit authority, and no immutable cell changed.

### F3 → bounded no-objection retained, residual risk now disclosed in-entry

The same clarification adds "Literal used-by discoverability does not endorse every sentence of a source row." With
that, Q17, M67 and Amendment 1 §3, the S050 index reads as corrective only. The structural limitation still exists:
there is no back-pointer cell in S050. It is now explicitly disclosed, so I make no further objection.

### F4 → resolved

Amendment 2 and the lesson's partition correction now say:
- C1 owns S061–S063, S068/S069 and the S005/S006 bookkeeping;
- calibration owns S064–S067, the older-entry appends and the S038/S050 cells.

SOURCES is consistent with this. S067's used-by is the lesson plus `attribution-interval-calibration.md`, and S068/S069
list only the lesson. New rows do not enter the C2 verdict (witnessed above).

### Remaining limits (not converted into acceptance)

- Every reader is author-side.
- C2 remains literal coverage only, not semantic support.
- The S005/S006 used-by edges into the lesson are outside the 13 and outside my scope.
- I did not audit the other v2 candidate edits (C1 predicate wording, Task247, the 67-case selftest, the URL-rule
  counts); they need their own lanes' re-reads.

Tool installs: none. Production edits: none. Scratch: `probe2/`, `base/`.

VERDICT (v2, scope = C2 literal-vs-semantic boundary and the S050/S058 corrective index, candidate 3eb2afe5): PASS —
all v1 findings are resolved or disclosed, the outside-row witnesses now clear, the frozen-row controls still fire, and the
identical-checker red/red/green reproduces. This is bounded author-side review; it gives no admission, no outside
closure and no approval of the C1 edits I did not audit.
