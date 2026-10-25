# R32RevEntry — Q1–Q21 review of the drafted C1 entry (`benchmark-grader-semantics.md`)

Seat: reviewer (leaf), round 32, 2026-10-25. Reviewed artifact:
`.ufo/waves/round-32/build/R32DraftEntry.md` (15,015 B; the entry body inside its ` ```markdown `
fence is **12,454 B / 215 lines**). Bar: `corpus/QUALITY.md` Q1–Q21 (admission bar Q1–Q10, Q21;
round-closure rows used only where they bind a landing). No lane file was created, edited or
deleted by this seat; scratch is `/tmp/r32-R32RevEntry/` (16,626 B: the three S093/S094 files I
fetched myself). No tool installed or upgraded
(curl + Python stdlib only).

## Sources opened for this review (my own fetches unless stated)

| id | object | pin | bytes | sha256 |
|---|---|---|---:|---|
| S093 | `v2/tasks/instance_internetarchive__openlibrary-00bec1e7…/tests/test.sh` | `66f92766bba642462d4bbe5479e83f91f9211862` | 7,864 (234 lines) | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` |
| S093 | same task `tests/parser.py` | same pin | 4,229 (157 lines) | `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66` |
| S094 | `tasks/finalpool/ab-testing/evaluation/main.py` | `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb` | 14,138 (297 lines) | `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` |
| S094 | `utils/evaluation/retry.py` | same pin | 4,519 | not re-hashed; read only |
| S097 | arXiv 2412.05579 v2 abs page | v2 (10 Dec 2024) | 43,661 | `44195c5f4c8e0ff915f5894a78e88f22a121d87d908e9ad211d611799d17a660` |

The S093 `test.sh` digest equals the round-31 capture digest recorded at
`.ufo/waves/round-31/build/R31SrcS093a.md:12`; the S094 digest equals `R32SrcS094a.md:4`,
`R32SrcS094b.md:5` and `R32LearnC1.md`. I read S094/S097 from the seats' captures under
`/tmp/r32-R32LearnC1/` and hashed them myself; S093 I fetched directly from the pinned raw URL.

## Byte-substring verification (assignment floor: ≥5; 15 checked)

| span quoted in the draft | source location | result |
|---|---|---|
| `all_required = fail_to_pass \| pass_to_pass` | `test.sh:213` | **found** |
| `success = all_required <= passed_tests` | `test.sh:214` | **found** |
| `T) git checkout HEAD -- "$path" 2>/dev/null \|\| true ;;` | `test.sh:71` | **found** |
| `# untracked files the patch merely MODIFIES are left alone (image-provided context)` | `test.sh:93` | **found** |
| `echo "Resetting test-space to base state (full test-code surface)..."` | `test.sh:33` | **found** |
| `^([^\s]+\.py::[^\s]+)\s+(PASSED\|FAILED\|SKIPPED\|ERROR)` | `parser.py:68` | **found** |
| `unique_results = {result.name: result for result in results}.values()` | `parser.py:121` | **found** |
| `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:` | `main.py:58` | **found** |
| `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)` | `main.py:280` | **found** |
| `raise ValueError(f"Record validation failed:\n{error_msg}")` | `main.py:100` | **found** |
| `bucket_exists = check_storage_bucket_exists("promo-assets-for-b")` | `main.py:225` | **found** |
| `if not check_abtesting_logging_bucket_clean(task_launch_time, task_eval_time):` | `main.py:234` | **found** |
| `return True  # Don't fail evaluation if we can't check logs` | `main.py:218` | **found** |
| `This paper presents a comprehensive survey of the LLMs-as-judges paradigm from five key perspectives: …` | abs page, `<blockquote class="abstract">` | **found** (both S097 captures) |
| `def check_storage_bucket_exists(bucket_prefix: str, project_id: str = "mcp-bench0606") -> bool:` | `main.py:125` | **found** |

Every source-file location the draft gives is correct: `test.sh:33/71/93/213/214`,
`parser.py:68/88/121`, `main.py:58/100/218/225/234/280`. The defects below are in what the draft
quotes and how it cites its *seat* reports, not in the source line numbers it states.

## Per-criterion verdicts

| Criterion | Verdict | Evidence |
|---|---|---|
| **Q1 — triad opens the entry** | **PASS** | Lines 1–3 are `source:` (S093 with task path + `tests/test.sh`/`tests/parser.py`, S094 with path, S097 with `# Abstract`), line 4 `verified-at: 2026-10-25`, line 5 `recheck: 180d — re-fetch the three pinned revisions … (next due 2027-04-23)`, line 6 `writer: KengakuR32`. Cadence **and** action present; `2026-10-25 + 180d = 2027-04-23` re-derived. |
| **Q21 — a pinned source names its pin** | **PASS** | `recheck:` names all three pins (`66f92766`, `9be8d8fe`, `2412.05579v2`); satisfies Q21's regex family (`pinned` + a 7-hex pin). |
| **Q2 — tier floor** | **PASS** | Load-bearing claims rest on S093 (A, code), S094 (A, code), S097 (B, preprint; staged row `SOURCES.append.md:27` is `B`). No tier-C or `community` row is used. S097's B is the right floor for a survey's own descriptive claim. |
| **Q3 — claim stays inside its quote** | **FAIL** | 17 of 26 quoted spans anchor on a *seat report's* prose, not on source bytes (§F1); S097 gains an intent the abstract does not state (§F6); two completeness/widening claims are unanchored (§F3). |
| **Q10 — locations and numbers re-read by a second seat** | **FAIL (locations only)** | Three seat-report line citations are off and one quote is reformatted (§F5). All numbers themselves re-derive: `0.05` at `main.py:280`, `0.1` default at `:58`, 21 variants/82 tasks (`R31SrcS093b.md:118,123-124`), 9/10 across 7 repositories (`:118`), 180d→2027-04-23. |
| **Q4 — negative space** | **PASS** | `## What this does not establish` (5 bullets: not runtime validity, not all of Toolathlon, not an observed run, not every parser, not an endorsement) + `## Falsifier` (3 source-scoped falsifiers). Each is a real non-claim. Minor gap: no falsifier for the "reward rule shared across tasks (9/10)" observation. |
| **Q5 — every source labelled for what it is** | **PASS (with §F1 tension)** | S097 labelled preprint in the `source:` line and in §S097; S093/S094 labelled the maintainers' own code, "not an independent measurement"; "Nothing here was executed against either benchmark". The tension: a seat's analysis quoted as evidence is exactly the "digest is not the original bytes" case the Q5 lesson names. |
| **Q6 — extends, never duplicates** | **FAIL** | §Extends names `corpus/knowledge/benchmark-verifier-execution-model.md` and says it "repeats none of its execution findings (Q6)" — but §S093 restates the containment reward (`:100` of that entry), the parser log scan (`:104-106`) and the test-space reset with `DATA_DIRS` (`:76-82`). §F2. |
| **Q7 — entry, index row and coverage row land together** | **FAIL (agreement)** | The entry body and the frontier's landing rows disagree twice: the row states "a project-wide bucket-prefix existence check" the entry does not carry (§F4), and the entry's "Toolathlon's scoring code" phrasing contradicts the frontier's own constraint (§F3). |
| **Q8 — rejections are kept** | **PASS (round level)** | `R32DraftLesson.md` Gate table records three rejects/defer with reasons and flip conditions (`judge-calibration-thresholds`, `card-publication-contracts`, `terminal-bench-release-identity`). The entry itself carries none, which is correct — rejections belong to the Gate. |
| **Volume** | **PASS** | 12,454 B / 215 lines (floor 40 lines). |
| **No cross-domain bleed** | **PASS** | Explicit non-claims for runtime task validity, contamination, novelty, difficulty, performance; "Not extended" bullet names the untouched entries. The only adjacent statement ("the lane's judge-calibration work belongs to the meta-evaluation perspective") is a mapping, not a calibration claim. |
| **Q11–Q20** | **N/A** | Not admission-bar rows for a knowledge entry; Q20's gate-receipt duty attaches to the landing commit, not to this draft. |

## Findings

### F1 (major, Q3/Q5) — the load-bearing anchors are seat prose, not source bytes

26 quoted spans; **9** are source bytes (`test.sh:93/213/214`, `main.py:58/100/225/234/280`, the
S097 abstract sentence — plus `main.py:218`'s comment quoted in prose), **17** are quotations of the
scouts' own analysis. Note that a span carrying a source location inline is not therefore a source
quote: "S093's reward is binary set containment (`test.sh:213-214`) over a log-derived …" is the
scout's VERDICT line (`R31SrcS093b.md:180`) with the location embedded in its prose. The sharpest cases:

- "S093's reward is binary set containment (`test.sh:213-214`) over a log-derived, last-write-wins,
  agent-writable `PASSED` set" is quoted from `R31SrcS093b.md:180` — the seat's **VERDICT** line.
  The entry's claim about the log scan is therefore supported by the seat's conclusion, not by
  `parser.py`. The source bytes exist and are re-runnable: `parser.py:68` (regex),
  `parser.py:88-90` (`# Also check stderr for any additional test results`), `parser.py:121`
  (`unique_results = …`), all verified above.
- "Source of truth is the image's object store, not a harness upload." (`R31SrcS093a.md:59`) and
  "re-uploading tests is **not** a precondition of this reset" (`R31SrcS093a.md:95`) are the
  scout's inferences; the anchorable bytes are `test.sh:71` (verified) and the in-file comment at
  `test.sh:93` (verified).
- The S094 half repeats the pattern: "gates on binary infrastructure state …"
  (`R32SrcS094b.md:53-55`), "no judge prompt, rubric, or LLM call appears anywhere in the file."
  (`:49`), "compares the agent's `record.csv` … (0.05% in main)" (`:55-56`), "is a pure poll-retry
  loop …" (`:46-47`), "This file establishes that its validator …" (`R32SrcS094a.md:14`).
- The `source:` line cites `tests/parser.py`, and the entry never quotes a byte of it.

Fix: keep the seat reports as *provenance of the capture*, not as the quoted evidence. Replace each
seat-prose span with the source byte and its `file:line` (the 15 spans in the table above cover most
of them), and keep first-person seat observations ("I produced reward 1 with all 20 required tests
failing", the 21-variant and 9/10 samplings) labelled as **lane observations**, which is what they
are.

### F2 (major, Q6) — the S093 half duplicates the round-31 entry while §Extends denies it

`corpus/knowledge/benchmark-verifier-execution-model.md` already holds, at `:100`, the exact pair
`all_required = fail_to_pass | pass_to_pass` / `success = all_required <= passed_tests`; at
`:104-106`, the `parser.py` log scan over stdout and stderr with last-write-wins dedupe; and at
`:76-82`, the `DATA_DIRS` reset hole. The draft's §S093 presents all three as its own reading and
then asserts "repeats none of its execution findings (Q6)". The frontier seat's constraint 2
(`R32Frontier.md:59-63`) says the same thing from the landing side: "The S093 half must be described
as restating round 31."

Fix: label §S093 a restatement (one sentence plus the `test.sh:213-214` bytes as a pointer), and put
the entry's new S093 content where it actually is new — the parser-variant scope (21 variants / 82
tasks) and the shared-file sampling — or drop §Extends' absolute claim.

### F3 (major, Q3/Q7) — the discharge is stated wider than the evidence and than the landing text

The entry writes: it "discharges the README frontier bullet-1 clause 'and for Toolathlon'
(corpus/README.md:276) for **Toolathlon's scoring code** — the task evaluation script — only", and
that `main.py` "is the whole scoring path for this task". `corpus/README.md:276` is the right line
(verified), but:

- the frontier's landing sub-bullet (`R32Frontier.md:50`) says the clause is "discharged for **the
  one task whose evaluation script is read**, not for the benchmark's whole scoring surface", and
  its constraint 1 (`R32Frontier.md:55-57`) forbids the phrase "Toolathlon's scoring code" outright;
- "the whole scoring path for this task" is an unanchored completeness claim: the seats read
  `evaluation/main.py` and `utils/evaluation/retry.py` only, and nothing quoted establishes that no
  other file contributes to this task's score.

Fix: adopt the frontier's wording verbatim in the intro and §Extends, and either drop "whole scoring
path" or state it as "the file this task's evaluator runs" with the invocation anchor.

### F4 (medium, Q7) — the entry omits a fact its index/coverage rows assert

`R32Frontier.md:95` (coverage row) and `:123` (index row) both say the entry adds "a project-wide
bucket-prefix existence check". The entry body carries only `bucket_exists =
check_storage_bucket_exists("promo-assets-for-b")` and "It checks infrastructure state". The fact is
true and anchorable: `main.py:125` (`bucket_prefix: str, project_id: str = "mcp-bench0606"`),
`:134` (`buckets = list(storage_client.list_buckets())`), `:136`
(`if bucket.name.startswith(bucket_prefix)`), prefix at `:225`. Because Q7 lands entry + index +
coverage row together, one side must move.

### F5 (medium, Q10) — seat-report locations off by one, and one quote reformatted

| draft says | actual |
|---|---|
| `all_required = …` "(quoted at `R31SrcS093b.md:36`)" | `R31SrcS093b.md:35`; `:36` is the `success` line |
| `success = …` "(quoted at `R31SrcS093b.md:37`)" | `R31SrcS093b.md:36`; `:37` is `test.sh:221` |
| S094 "compares the agent's `record.csv` …" "`R32SrcS094b.md:56`" | span begins on `:55`; cite `:55-56` |
| "All 82 openlibrary tasks fetched: **21 distinct sha256** variants (largest cluster 15)." "`R31SrcS093b.md:123`" | "(largest cluster 15)" is on `:124`; cite `:123-124` |
| "…agent-writable `PASSED` set" "`R31SrcS093b.md:180`" | seat text is `agent-writable PASSED set` (no backticks) — the draft's backticks make the span not a byte substring |
| "100 % of the required ids, no threshold, no partial credit, no weighting" "`R31SrcS093b.md:136-137`"; "I produced reward 1 with all 20 required tests failing (§4.3)." "`:161-162`" | both spans cross a line break and are rendered as one string; as written they are not byte substrings of the seat range |

The two "7 repositories" and "9/10" numbers are supported — at `R31SrcS093b.md:118`, not at the
cited `:177-178`; cite both lines or move the citation.

### F6 (minor, Q3) — S097 gains an intent the abstract does not state

"…which the survey keeps distinct from methodology on purpose." The verified abstract sentence
names five perspectives; it states no design intent ("on purpose"). A paraphrase may narrow a quote,
never widen it (Q3). Fix: "…names meta-evaluation as one of its five perspectives, distinct from
methodology and limitations."

### F7 (minor, Q1/Q21 consistency) — the S097 `source:` URL differs from its registry row

Entry: `https://arxiv.org/abs/2412.05579v2`. Row (`SOURCES.append.md:27`) and the quote gate's url
map: `https://arxiv.org/abs/2412.05579`. Both serve v2 (`R32LearnC1.md`, effective-URL note), but a
later `plans/sources_adopt.py --quote` run binds on the URL the row cites; entry and row should name
the same one.

### F8 (minor, provenance) — "the S097 capture" is not a single byte object

Two captures of the same v2 page differ: `/abs/2412.05579` → 43,647 B
`851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d` (`R32LearnC1.md`) and
`/abs/2412.05579v2` → 43,661 B `44195c5f…a660` (`R32SrcS097.md`). The quoted sentence is a byte
substring of **both** (verified), so no claim fails; but the entry should not imply one digest is
the page's identity, since arXiv pages carry per-request content.

## What the draft gets right (and the staged entry did not)

- The **tolerance** is correct: default `0.1` at `main.py:58` is explicitly separated from the
  executed `0.05` at `main.py:280`, which fixes the staged entry's `:69` error ("outside the
  0.1-percentage-point tolerance") and matches what the frontier requires before landing
  (`R32Frontier.md:66-68`). A draft that had repeated `0.1` would have been a kill-rule-adjacent
  defect.
- The **fail-open log-bucket check** is recorded with its anchor (`main.py:218`, "Don't fail
  evaluation if we can't check logs") — a grader-semantics fact neither the round-31 entry nor the
  staged entry carried.
- **Negative space and falsifier** are real and source-scoped, and the non-claims are specific
  enough to be falsified later.

## Residual risk and verification gaps

- I did not re-fetch S094/S097 from the network this seat; I hashed the seats' captures and matched
  the S094 digest to three independent seat records. S093 I fetched myself (digest matches round 31's).
- The `parser.py` log-scan and the `test.sh` reset are *code* facts; round 31 executed the parser path
  on a scratch copy (`R31SrcS093b.md:161-162`), and this seat did not re-execute it. The entry's
  falsifier already scopes that.
- I did not review the S094/S097 *row* text (that is `R32QuoteMode`'s and `R32MutRows`' scope); its
  known defect — the row's `LMs-as-judges` typo — is already recorded there
  (`R32QuoteMode.md`, exit 7) and must be fixed before C1's kill rule can pass. The entry quotes the
  correct `LLMs-as-judges` bytes, so the entry and its row currently disagree by one letter.
- Q13's landing-time check (`plans/gate_timing_check.py --commit <admission commit>`) can only run
  after the admit; this report is the Q10 second-seat re-read the Gate should cite by path.

VERDICT: defects
