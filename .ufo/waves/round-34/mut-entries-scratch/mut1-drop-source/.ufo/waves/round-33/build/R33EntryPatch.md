# R33EntryPatch — C1 admission patch for `corpus/knowledge/benchmark-grader-semantics.md`

Seat: `R33EntryPatch` (leaf). Date: 2026-10-25. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base: the **committed** draft at `bcd2a6c:corpus/knowledge/benchmark-grader-semantics.md`
(98 lines, blob `124c26d`). The lane working tree already carried a *partial* re-point of that
file by another seat; I did not build on it, I rebuilt the patch from the committed bytes and
diffed my result against the working-tree version separately (§5.4).

Artifact: `.ufo/waves/round-33/assimilation/entry-patched.md` — 176 lines, 13,403 bytes,
sha256 `d61b65f3ae7bbf6c23caa824ca7e043a31f8dd30d268076e0c8bd91ec5827673`.

**VERDICT: entry-patched**

---

## 1. Behavior delivered

A complete replacement entry file, ready for the L1 to land over
`corpus/knowledge/benchmark-grader-semantics.md`, with:

1. `source:` lines citing exactly the three ids **S093, S103, S104** (three distinct), by
   document, each with `accessed 2026-10-25`:
   - S093 → `https://github.com/scaleapi/SWE-bench_Pro-os`, `tests/test.sh` + `tests/parser.py`
     at `66f92766bba642462d4bbe5479e83f91f9211862`;
   - S103 → `https://github.com/hkust-nlp/Toolathlon`,
     `tasks/finalpool/ab-testing/evaluation/main.py` at
     `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`;
   - S104 → `https://arxiv.org/abs/2412.05579`, arXiv 2412.05579v2.
2. `verified-at: 2026-10-25` unchanged; `recheck:` unchanged.
3. `writer: KengakuR33 (admission patch of the round-32 draft)`.
4. The executed-tolerance claim restated as **signature default 0.1 (`main.py:58`) vs invoked
   `tolerance_pct=0.05` at the call site (`main.py:279-280`)**, with the executed comparison
   pinned to `main.py:84,91`.
5. The log-bucket claim restated as a **split**: exactly two `return True` sites — clean path
   `:214`, and the single broad `except Exception` handler `:216-218` (the only caught-exception
   True path) — while credential failure returns `(None, None)` at `:118-123`, skips the guard at
   `:176`, falls off the function as implicit `None`, and raises at `:235` (fail closed); the
   storage check's fail-closed path runs `:132 → :145-166 → :230`; `log_bucket_name.txt` is read
   outside the `try` (`:171-172` vs `:173`).
6. The survey named by its served title `LLMs-as-Judges: A Comprehensive Survey on LLM-based
   Evaluation Methods`, with a note that the abstract body writes `LLMs-as-judges` lowercase, so
   the quoted span is verbatim and the two casings are both source-faithful.
7. One `[INFERENCE]` marker, on the only assertion the bytes cannot settle: that the compared
   unit of `tolerance_pct` is a percentage point (rests on the `%` formatting at
   `main.py:86,93`, not on prose).
8. A "Reading basis" paragraph naming the three committed captures by path, size and digest, and
   recording that S093's `test.sh` is also landed (byte-identical to the bytes re-located here)
   while its `parser.py` is not captured.

## 2. Gates actually run (verbatim)

All read-only; no product counter is claimed as passing.

| Check | Command | Output |
|---|---|---|
| base bytes | `git show bcd2a6c:corpus/knowledge/benchmark-grader-semantics.md` | 98 lines, blob `124c26d` |
| capture provenance | `wc -lc` + `sha256sum` on `.ufo/waves/round-33/assimilation/captures/` | `297 14138` main.py `3bad26b6…a9b9ad`; `109 4519` retry.py `db11e66e…17f69e`; `617 43661` abs.html `44195c5f…17a660`; identical to `SHA256SUMS.txt`, and `sha256sum -c …/SHA256SUMS.txt` from the lane root prints `OK` for all three |
| landed S093 capture | `sha256sum .ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh` | `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` — byte-identical to my `/tmp` fetch of the pinned `tests/test.sh`; it is **not** listed in `SHA256SUMS.txt` and there is no `parser.py` capture |
| judge-path scan | `grep -n -i -E 'prompt\|judge\|model\|openai\|chat\|gpt\|llm\|claude\|anthropic' toolathlon-ab-testing-evaluation-main.py` | **no matching line** (exit 1) in the 297-line file |
| line anchors | `grep -n` for signature, call site, guards, raises, retry constants | `:58`, `:70`, `:72`, `:84`, `:91`, `:100`, `:118-123`, `:132`, `:164-166`, `:171-172`, `:176`, `:213-214`, `:216-218`, `:225`, `:230`, `:234-235`, `:255-265`, `:279-280`, `:293-295`; `retry.py:44-45` |
| S093 re-location | `curl -fsSL https://raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/66f92766…/v2/tasks/<instance>/tests/{test.sh,parser.py}` | `test.sh` 234 lines, sha256 `b6f26eec…976d0`; `parser.py` 157 lines, sha256 `303ceda2…0b66`; anchors `:33`, `:38`, `:43-44`, `:71`, `:207-210`, `:213-214`; `parser.py:68`, `:88-90`, `:121` all present |
| lane C1 counter (lane path, **not** this artifact) | `python3 plans/round33_c1_verify.py --lane .` | `checks=8 defects=0`, rc=0 — this reads `corpus/knowledge/benchmark-grader-semantics.md` in the working tree, i.e. the sibling's in-flight version |
| artifact preflight (my own script) | source-line regex, URL-host match per cited row, pin presence, line/byte floor, quote token counts | 3 source ids `['S093','S103','S104']`, all three URLs present, `verified-at` present, all three pins present, 176 lines / 13,403 bytes; quotes 11 / 5 / 3 / 20 whitespace tokens |

**Not run, deliberately:** `plans/adoption_check.py` (its `entries[].path` is the frozen lane
path, so it would score the working tree and not `entry-patched.md`), and `plans/round33_defects.py`
(C2's counter, separable from this item). Neither is claimed.

## 3. Touched surfaces

Written (2 paths, both assigned):

- `.ufo/waves/round-33/assimilation/entry-patched.md` (the deliverable)
- `.ufo/waves/round-33/build/R33EntryPatch.md` (this report)

Read-only: `plans/round-33-claims.md`, `git show bcd2a6c:…` for the entry and `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `corpus/knowledge/benchmark-verifier-execution-model.md`,
the wave captures, the sibling assimilation artifacts (`url-map.json`, `quotes-rows.txt`,
`append-block.md`), and `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`.

Scratch: `/tmp/r33-R33EntryPatch/` (`committed-draft.md`, `s093-test.sh`, `s093-parser.py`,
`entry.diff`, `vs-integrated.diff`, `c1.out`; ~35 KB total).

No tool installed or upgraded; no `pacman` transaction attempted (host pause respected). No git
mutation, no write to `shokuknow`, `/home/vgpnk/Projects/shokunin`, `.ufo/state`, or `MANIFEST.json`.

## 4. Out of scope (untouched, by design)

- `corpus/SOURCES.md` append, `corpus/README.md` index/coverage rows, `SCORECARD.md`, lessons,
  fleet reports — L1 integrates.
- `plans/round33_c1_verify.py`'s V7 lesson text and V8 refusal rows.
- The C3 catalog probe.

## 5. Findings

### 5.1 Every changed line, old → new (old = committed draft `bcd2a6c`)

Line re-wrapping of otherwise unchanged sentences is the only mechanical churn; every semantic
change is enumerated below. New-file line numbers are from `entry-patched.md`.

**Header**
- C1. `source: S094 — https://github.com/hkust-nlp/Toolathlon — …` → `source: S103 — …` (id
  renumbered; URL, path and commit unchanged).
- C2. `source: S097 — https://arxiv.org/abs/2412.05579 — arXiv 2412.05579v2 (preprint), accessed 2026-10-25`
  → `source: S104 — …` (same line otherwise).
- C3. `writer: KengakuR32` → `writer: KengakuR33 (admission patch of the round-32 draft)`.
- Unchanged: S093 source line, `verified-at: 2026-10-25`, `recheck:` line.

**Intro**
- C4. old: `the round-31 entry, and it discharges the README frontier bullet-1 clause "and for Toolathlon"`
  + `(`corpus/README.md:276`) **for the one task whose evaluation script is read** — the Toolathlon`
  → new: `… discharges the Toolathlon third of the README frontier bullet-1 instruction — "the primary`
  `specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro" (`corpus/README.md:276`)`
  `— **for the one task whose evaluation script is read**, the Toolathlon … at `9be8d8fe`. That is also`
  `the item the round-31 bullet leaves open by name: "and for Toolathlon" (`corpus/README.md:278`).`
  *Reason:* the string `and for Toolathlon` is **not** at `README:276` (that line is bullet-1's main
  text); it is at `README:278` (round-31 sub-bullet). A quoted span must sit where it is cited.
- C5. old: `It is not runtime task validity (`PROVINCE.md` refuses that to this lane), not`
  → new: `It is not runtime task validity (`PROVINCE.md:218-219` keeps that outside this lane: "it does`
  `not run a benchmark, certify a task, or own deployment configuration, runtime task validity"), not`
  *Reason:* PROVINCE says "does not … own" / "remain open", not "refuses"; the quote is now exact and
  line-pinned.

**Source labels**
- C6. old: `**Source labels (Q5).** S093 is a benchmark maintainer's own task-grading code at a pinned commit; S094 is Toolathlon's own task-evaluation script at a pinned commit; S097 is an arXiv preprint.`
  → new: `**Source labels (Q5; ids renumbered round 33 — the staged package's S094→S103 and S097→S104 after round-32 id collisions; the round-32 refusal rows at S094/S097/S101/S102 stand unchanged and no id is reused).** S093 … ; S103 … ; S104 is an arXiv preprint.`
- C7. **new paragraph** (no old): `**Reading basis.** …` naming the three capture paths, sizes and
  sha256 digests, and recording that S093's `test.sh` is landed in the same capture directory
  while its `parser.py` is not.

**S103 section**
- C8. `## S094 — Toolathlon's ab-testing grader …` → `## S103 — …`.
- C9. old: `case-insensitive scan … finds no such scoring path. Its non-standard imports include cloud/storage libraries and the retry wrapper; the `gcloud` CLI is a fallback for the storage check. The scoring path compares a produced `record.csv` against `groundtruth_workspace/expected_ratio.csv`:`
  → new: `… matches no line at all in the 297-line file. Its non-standard imports are cloud/storage libraries (`google.cloud` `storage` and `logging`, `google.oauth2.service_account`, `google.api_core.exceptions`, `main.py:6-8`) and the retry wrapper (`main.py:12`); the `gcloud` CLI is a fallback for the storage check (`main.py:145-166`). The scoring path compares a produced `record.csv` against `groundtruth_workspace/expected_ratio.csv` (`main.py:53-56`):`
- C10. old: `— 11 words, `main.py:58`` → `— 11 whitespace-separated tokens, `main.py:58`, the **signature default**`
  (count re-verified: 11 whitespace tokens).
- C11. old: `The signature default is 0.1%, but the executed call overrides it:`
  → `The default is not what runs. The function's single call site overrides it:`
  *Reason:* the source declares `0.1` without a unit; "0.1%" attached a unit the file does not state.
- C12. old: `— 4 words, `main.py:279`` → `— 4 words plus the `#` marker, `main.py:279`` (5 whitespace tokens total).
- C13. old: `— 5 words, `main.py:280`` → `— 3 whitespace-separated tokens, `main.py:280``
  *Reason:* the call span splits into 3 whitespace tokens, not 5.
- C14. old: `So the operative tolerance is set at the call site, not by the default: the task is graded by a comparison of conversion rates within **0.05 percentage points** per scenario, and one missing or extra scenario name fails the task (…)`
  → new: `So the operative tolerance is set at the call site, not by the default: the executed check is `diff > tolerance_pct` on each scenario's A and B conversion rate (`main.py:84`, `:91`), i.e. a difference of **0.05** in the unit the rates are printed in, and a missing or extra scenario name fails the task (…). [INFERENCE] The rates are formatted with a trailing `%` in the same message that prints the tolerance (`main.py:86`, `:93`), so the compared unit is a percentage point; the comment calls 0.05 "0.05%". The source never spells out the unit in prose, which is why this gloss is marked rather than quoted.`
- C15. old side-effect paragraph (7 lines, `main.py:134-139`; "The log check returns `True` both for a clean bucket and for some caught exceptions (`main.py:213-218`); that does not mean every inability to perform the check passes. When credentials are unavailable, the function can fall through without a truthy result and the task-completion check raises instead. A failure of that specific exception path is not the same as a failure of the grader as a whole.")
  → new (3 paragraphs):
  `Before the record comparison, and first in the process order, the script runs a side-effect check that confirms a matching storage-bucket prefix (`check_storage_bucket_exists`, `main.py:125-166`, called at `:225`) and requires the ab-testing logging bucket to contain no entries (`check_abtesting_logging_bucket_clean`, `main.py:168-218`, called at `:234`).`
  `The log check has two `return True` sites, and they are not the same path. The clean-bucket path prints and returns `True` (`main.py:213-214`). The single broad `except Exception` handler prints a warning and returns `True` too, on the line whose own comment reads `# Don't fail evaluation if we can't check logs` (`main.py:216-218`). That handler **is** a caught-exception True path: …`
  `Credential failure is not that path and does not reach that handler. `get_project_id_and_credentials` returns `(None, None)` on `FileNotFoundError` (`main.py:118-120`) and on any other exception (`:121-123`). … no `return` executes, and the function falls off its end returning an implicit `None`. … so it raises `ValueError` (`:235`). The storage check fails closed in the same direction … raising at `:230`. A missing `log_bucket_name.txt` is not caught at all — the file is opened at `:171-172`, outside the `try` that starts at `:173`. So the log check mixes one narrow fail-open caught-exception path (`:216-218`) with fail-closed credential and missing-file paths; "the log-bucket check fails open" is true only of that handler.`
- C16. old retry paragraph (`utils/evaluation/retry.py:44-45` …; "the retry wrapper applies to the task-completion side-effect check, not the later record comparison. It therefore provides at most three attempts for that check; it does not retry the full scoring path or turn an implicit-`None` result into success.")
  → new: `… The retry wrapper applies to the task-completion check, not to the later record comparison: `_check_completion` calls `validate_task_completion` and converts any exception into `(False, str(e))` (`main.py:255-260`), and `grade_with_retry(_check_completion)` is invoked at `:262` with no `max_attempts` override, so the default budget of three attempts holds. The record comparison at `:280` sits outside that wrapper; its own `try` prints the error and calls `exit(1)` (`:293-295`). Both a completion failure (`:263-265`) and a record-validation failure (`:293-295`) end the process non-zero; the retry changes only how many times the completion check is tried — at most three — never whether an implicit `None` counts as success.`

**S104 section**
- C17. `## S097 — the survey frame …` → `## S104 — …`.
- C18. old: `The field's own LLM-as-judge survey names the paradigm's parts:`
  → new: `The field's own survey is `LLMs-as-Judges: A Comprehensive Survey on LLM-based Evaluation Methods` (arXiv 2412.05579v2; title as served in the capture's `citation_title` meta tag). It names the paradigm's parts:`
  *Reason:* the served title (`…-abs.html:41`) capitalises `Judges` and pluralises `LLMs`; the draft's
  lowercase singular form was the misspelling.
- C19. old: `— 20 words, arXiv 2412.05579v2 Abstract`
  → `— 20 words, arXiv 2412.05579v2 Abstract (`…-abs.html:124`)` (count re-verified: 20).
- C20. **new paragraph** (no old): `The capitalisation differs between the two source locations
  and neither form is a transcription error: the title capitalises `Judges` (`LLMs-as-Judges`,
  `…-abs.html:41`), while the abstract body writes `LLMs-as-judges` lowercase (`:124`). The quote
  above reproduces the abstract byte-for-byte.`

**S093 section**
- C21. old: `… and that the reset restores tracked test code but not newly added fixture files.`
  → new: `… and that the reset rewrites the tracked test-code surface while a file under a data-directory parent is excluded from that rewrite.`
  *Reason:* the bytes show the reset restores tracked test code (`:71`) **and** restores a tracked
  fixture the agent edited (`:97-105`), while a DATA_DIR parent makes `is_test_code` false
  (`:38`, `:43-44`) so an agent-added file there never enters the list; an untracked file under
  `tests/` is deleted by the `U)` branch (`:72`). The old phrasing read as if fixtures were never touched.
- C22. **new paragraph** (no old): the five re-located anchors (`test.sh:213-214`, `:207-210`,
  `parser.py:68`,`:88-90`, `:121`, `test.sh:71`, `:38`/`:43-44`) plus the provenance sentence —
  `test.sh` anchors backed by the landed capture, `parser.py` anchors re-located from the pin
  because this wave captured no `parser.py`, nothing executed.

**What this does not establish**
- C23. old: `- It does not claim the `0.1` default is ever executed for this task; the executed call is the `0.05` value, and the default is read only as the function's declared signature.`
  → new: `- It does not claim the `0.1` default is ever executed for this task; the executed call passes `tolerance_pct=0.05` at `main.py:280`, and the `0.1` is read only as the function's declared signature (`:58`).`
- C24. old: `- It does not establish that the log-bucket check ever runs against a real Cloud Logging deployment; the clean path returns `True`, some caught exceptions do too, while credential failures can fall through to implicit `None` and fail the task. Those error paths differ.`
  → new: `- It does not establish that either side-effect check ever runs against a live Cloud Storage or Cloud Logging deployment; the clean log path returns `True` (`:214`), the broad caught-exception path returns `True` (`:216-218`), while credential failure falls through to implicit `None` and raises (`:234-235`). Those paths differ, and only the second is fail-open.`
- C25. **new bullet**: `- It does not establish the unit of `tolerance_pct` from prose; the percentage-point reading is marked [INFERENCE] above and rests on the `%` formatting in the failure message, not on a stated unit.`

**Falsifier**
- C26. old: `Two observations would falsify …: a scoring path … that invokes an LLM judge; or evidence that the sole `validate_record_data` call does not pass `tolerance_pct=0.05`.`
  → new: `Three observations would falsify …: a scoring path … that invokes an LLM judge; evidence that the sole `validate_record_data` call does not pass `tolerance_pct=0.05`; or a second caught-exception `return True` site in `check_abtesting_logging_bucket_clean` beyond `main.py:216-218`.`

Diff size against the committed draft: **5 hunks, 133 insertions, 55 deletions**.

### 5.2 Statements the captures did not support (all corrected in the patch)

1. **`corpus/README.md:276` did not contain the quoted clause.** The committed draft attributed
   `"and for Toolathlon"` to `:276`. Verified at `bcd2a6c`: `:276` is bullet-1's main line
   (`… the primary specs and scoring code for Terminal-Bench 2.0, Toolathlon, and SWE-bench Pro …`),
   and the phrase `and for Toolathlon` is on `:278`. Fixed by quoting `:276`'s actual span and
   citing `:278` for the clause.
2. **`PROVINCE.md` does not use "refuses".** Its own words at `:218-219` are "it does not run a
   benchmark, certify a task, or own deployment configuration, runtime task validity"; the
   frontier paragraphs say such items "remain open". The paraphrase is now a quotation.
3. **The call-site quote was miscounted** (`5 words`; actual 3 whitespace tokens). The signature
   "11 words" is correct as 11 whitespace tokens; the comment span is 5 whitespace tokens
   (4 words plus `#`).
4. **The log-check `True` sites were conflated.** `main.py:213-218` spans two semantically
   different returns: the clean path (`:214`) and the broad `except Exception` handler (`:218`).
   Only the latter is a caught-exception True path. Split in the patch.
5. **`main.py:134-139` was a narrow, misleading range** for the storage check (the function
   starts at `:125`). Widened to `:125-166` (with the call at `:225`).
6. **"restores tracked test code but not newly added fixture files"** understated and mis-stated
   the reset: a tracked *edited* fixture under a `fixtures/` path IS restored (`:97-105`), and the
   exclusion is by DATA_DIR parent (`:38`, `:43-44`), not by "newly added" per se. Sharpened.
7. **`0.05 percentage points` is an inference, not a quote.** The source prints rates with `%`
   (`:86`,`:93`) and names `0.05` in a comment, but never states the unit in prose. Marked
   `[INFERENCE]`.
8. **Survey title spelling.** Served title is `LLMs-as-Judges: A Comprehensive Survey on
   LLM-based Evaluation Methods` (capital `J`); the abstract body has `LLMs-as-judges` (lowercase).
   The draft's prose form `LLM-as-judge survey` matched neither. Fixed, and the capture's
   two-casing fact recorded. (The staged `SOURCES.append.md` S097 anchor has a separate one-`L`
   typo, `the LMs-as-judges paradigm`; the live S097 refusal row already records it, and the
   entry's quote carries two `L`s, verified against the capture.)

### 5.3 Live-tree conflicts the L1 must resolve (I could not edit these)

- **`corpus/README.md:67`** (index row, committed) says "… a log-bucket check **fails open**".
  That contradicts the corrected entry. The working tree already reworded it to "mixes fail-open
  exceptions with fail-closed credential a…" — keep that text.
- **`corpus/README.md:255`** (committed coverage bullet) cites "S093, S094, S097". Must read
  "S093, S103, S104" (the working tree already does, and also changes "round 32" to "round 33,
  admitted under renumbered ids").
- **Line drift for `README:276`/`:278`.** They hold at `bcd2a6c` and still hold in the working
  tree (the round-32 frontier sub-bullet was replaced 1:1 by a round-33 one). If any row is added
  *above* them in the index table, re-locate by the quoted spans, not the numbers.
- **`corpus/SOURCES.md` S103 row** (working tree) already reads "… caught exceptions return True
  (fail open) while absent credentials fall through to implicit None (fail closed)" — consistent
  with the patch; no action. `.ufo/waves/round-33/assimilation/append-block.md` still shows the
  shorter "(fail open)" phrasing on its visible line; prefer the registry row's fuller text.
- **S093 captures: `test.sh` landed, `parser.py` not, and the manifest lags.** The L1's commit
  `2b4cef2` landed `.ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh` with
  sha256 `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0` — **byte-identical**
  to my own fetch from the pin, so the two derivations agree. Its `parser.py` (157 lines, sha256
  `303ceda2c97816c27383b767baa9e2f28f8e9b0cebed4dd5d6159c6760770b66`) is still only in `/tmp`, so
  the three parser anchors in the entry are re-located but not backed by landed bytes; the entry
  says so. Two follow-ups: (a) if Q7/Q10 is read strictly, land `parser.py` next to `test.sh`;
  (b) `SHA256SUMS.txt` lists only the three original captures, so append
  `b6f26eecd87c1696a3702ee115d31f9d42f4704cf2116419cd879f66b60976d0  .ufo/waves/round-33/assimilation/captures/swebench-pro-tests-test.sh`
  to restore the digest binding for the landed file.
- **Staged package rows must stay unappended** (`/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`):
  the S094 row repeats the `0.1`-default framing and the S097 row has `LMs-as-judges`; both ids are
  live `rejected` rows in the lane, so re-appending would recreate the round-32 collision.

### 5.4 Divergences from the sibling's in-flight working-tree entry

The working-tree entry already passes `round33_c1_verify.py` (`checks=8 defects=0`), so these are
*substantive improvements*, not gap-filling: exact `writer` string; the README `:276`/`:278`
citation repair; the PROVINCE quotation; correct quote counts; the `[INFERENCE]` unit marker; the
split of the two `return True` sites plus the full credential fail-closed chain; the
`_check_completion`/`grade_with_retry`/`exit(1)` detail (including that the record comparison is
outside the retry); the exact survey title and the title-vs-abstract casing note; the S093
re-location paragraph; the extra non-establishment bullet; and the third falsifier. The one
benign difference: the integrated entry cites `main.py:125-140,225` for the storage check while
the patch cites `main.py:125-166,225` (function boundary, including the gcloud fallback).

### 5.5 Mid-seat commit: the L1 snapshotted this artifact, and the snapshot lags

The lane tip moved to `2b4cef2` while this seat was still writing. That commit already contains
`entry-patched.md` (git blob `1ccaf07`), but as my **pre-correction** revision; the working tree is
21 lines ahead (13 insertions, 8 deletions) with exactly two changes: (1) the `PROVINCE.md:219-220`
→ `:218-219` citation plus removal of the duplicated "contamination measurement"; (2) the S093
capture provenance rewrite forced by the `test.sh` that the same commit landed. **The L1 must
re-land the current bytes** (sha256 `d61b65f3ae7bbf6c23caa824ca7e043a31f8dd30d268076e0c8bd91ec5827673`;
the committed blob's content sha256 is `6eed24f6…`). This seat ran no `git add`/`commit`; the
commit is the L1's.

## 6. Artifacts

- Deliverable: `.ufo/waves/round-33/assimilation/entry-patched.md` (176 lines, 13,403 bytes,
  sha256 `d61b65f3ae7bbf6c23caa824ca7e043a31f8dd30d268076e0c8bd91ec5827673`).
- This report: `.ufo/waves/round-33/build/R33EntryPatch.md`.
- Scratch (not to be landed): `/tmp/r33-R33EntryPatch/{committed-draft.md,entry.diff,vs-integrated.diff,s093-test.sh,s093-parser.py,c1.out}`.

VERDICT: entry-patched
