writer: KengakuR29-2.FEntryQuality-2

# FEntryQuality — candidate vs QUALITY Q1–Q16 and the r28 entry format

Seat `KengakuR29-2.FEntryQuality-2` (role critic, read-only leaf; actual writer: same). Attack target:
the frozen knowledge candidate `.ufo/waves/round-29/drafts/webarena-config-projection.md`, judged against
`corpus/QUALITY.md` Q1–Q16 and against `corpus/knowledge/webarena-task-spec-audit.md` as the format
reference. Lane master `56fd949a6478342531e61f4feecb4a685d831640`.

Production source `plans/config_projection.py` was **not read**. I ran it only through `--summary`,
`--json` and `--selftest`. My own census and probes were derived from the generator bytes, the pinned raw
file and profiles.json. They live in `.ufo/waves/round-29/scratch/falsify/FEntryQuality/` (`census.py`/`.out`,
`probe.py`/`.out`, `inject.py`/`.out`, `README.pinned.md`, `prepare.pinned.sh`).
Tool installs/updates: none (stdlib python3 only, no pacman). Network: two `curl -fsS` GETs of public pinned
upstream URLs (README.md, prepare.sh). Line numbers below are from `grep -n` on the candidate. Word counts
for quotes were computed with `len(q.split())`.

## Identity and frozen-byte checks (observed)

| check | command | observed |
|---|---|---|
| candidate bytes | `sha256sum` | `7006b93d…53dc`, equal to the freeze file |
| instrument bytes | `sha256sum plans/config_projection.py` | `5673405e…12e3`, equal to the freeze file |
| `--json` output | `--json > /tmp/FEntryQuality-2.json; sha256sum` | `c8da0c5a…4630`, equal to the freeze and to `build-json-sha256.txt` |
| `--summary` | exit code | 0, `TOTAL findings=0 exit=0` |
| `--selftest` | exit code | 0, `SELFTEST clean cases=20` |
| manifest, generator, raw file, profiles | `sha256sum` | `f6390b92…`, `45ddba7b…`, `7b50386f…`, `90fdc34d…`, all equal to the manifest/prereg |
| README at dce04686 | `curl` + `sha256sum` | `081c8264…9287`, equal to the S072 anchor |
| prepare.sh at dce04686 | `curl` + `sha256sum`, `wc -lc` | `97b8671f…c7e2`, 6 lines, 120 bytes, equal to the S073 anchor |
| canonical path | `test -e corpus/knowledge/webarena-config-projection.md` | absent (exit 1) |

## Independent number re-read (Q10 input): all 17 entry numbers reproduce

Source: `census.py`, written from the S070 text contract (six ordered `str.replace` calls on the whole
text, then `json.loads`, then `enumerate`), not from production code.

| candidate line | entry value | independent value |
|---|---|---|
| 40 | 812 / 812 / 3 / 2436 | 812 tasks, 812 distinct IDs, 3 profiles (2436 = 812×3) |
| 41 | 385, 336, 281, 300, 0, 133 = 1435 | identical; total 1435 |
| 42 | 204, 128, 192, 182, 0, 128; sum 834; distinct 812 | identical; sum 834; tasks with any token 812 |
| 43 | 1416 / 10869 / 13 | changed leaves 1416, string leaves 10869, leaves with >1 occurrence 13 |
| 44 | url 1355 (812/338/205); non-url 61 (60/1) | identical per path template |
| 45 | 0 remaining tokens per profile | 0 for all three profiles; each projection parses to 812 |
| 46 | `__last_url__` 65, `__page__` 12 | identical; no other `__x__` marker in the raw file |
| 47 | 812/812 | `index == task_id` for 812 of 812 |
| 48 | 697 under trailing-slash, 0 otherwise | 697 token-then-`/` occurrences; 2132 − 1435 = 697 extra `//` |
| 51–52 | no occurrence inside a key | 0 key hits; leaf counts equal text counts |
| 63–64 | reversed order gives identical output | reversed-order text equals forward-order text for all 3 profiles |
| — | projected text digests | first 16 hex characters equal the instrument's `projected_text_sha256` for all 3 profiles |

## Per-criterion verdicts

| criterion | verdict | evidence |
|---|---|---|
| Q1 triad | PARTIAL | Lines 1–3 are `source:`, `verified-at: 2026-10-21 —…`, `recheck: on-release — <commands>`, and line 4 is `writer:`. The S071 anchor `Character Encodings and loads` (6 words) does not match the row's located anchors (§576-591, 581-582, invalid-document 402). The S068 cite `S068 raw-task input pin` (4 words) has no anchor at all; the r28 entry gives S068 line anchors. |
| Q2 tier floor | PARTIAL | S070–S073 and S068 are all tier A, kind code/docs/dataset, none community. Exception: line 31 says `\n` decodes to a newline, but S071's scope is "serialization escaping and deserialization rejection", and no row anchors escape decoding. |
| Q3 claim inside quote | **FAIL** | Finding F1 (lines 30–32) and finding F2 (lines 27–28) below. |
| Q4 negative space | PARTIAL | The non-claims are thorough (lines 16–18, 54–66, 77–80). However, there is no falsifier statement: no "falsif" string exists in the candidate, while the r28 reference has `Falsifiers:` at line 152. Findings F3 and F4 below cover undisclosed alternative readings. |
| Q5 source labels | PARTIAL | Profiles are labelled synthetic and S070–S073 are scoped. The measured table (lines 36–48) is output of an instrument whose author (KengakuR29-2) is the entry writer, and the entry does not label it as such. No oracle or independent-agreement statement appears ("oracle" occurs 0 times), although C1 includes "independent oracle agreement". The r28 entry labels its oracle as "independent logic, not independent authorship". |
| Q6 extends | PASS | Line 10 names the README Frontier gap "generated eval-time configs", which `corpus/README.md:338` lists as open, and names the r28 entry. Nothing is duplicated. Provenance note: R29DraftEntry reported earlier draft bytes `7bf99d9b…`, but git history at this path holds only `b98dcf3` (`4b38b4bf…`) and `56fd949` (`7006b93d…`), so the line 14 "replaces it" refers to bytes not retained at this path. The earlier draft was never admitted. |
| Q7 landed together | NOT MET (pre-admission) | The canonical path is absent. `corpus/README.md` has no config-projection index or coverage row. S070–S073 have status `queued` and used-by `—`. All cited support (instrument, fixtures, hand fixtures, receipts) is git-tracked. However, the entry names no receipt path (`corpus/evidence/round29-calibration/` occurs 0 times), unlike r28 lines 103–108. |
| Q8 rejections kept | NOT YET EVALUABLE | `corpus/lessons/round-29.md` has no `## Gate` section. Gate candidates exist only in `drafts/lesson-and-mistake.md` §3. |
| Q9 rejection reason | N/A | The candidate states no rejection. |
| Q10 second-seat re-read | PARTIAL (in progress) | This seat re-derived all 17 numbers (all match). It re-fetched S072 and S073 (both hashes match) and re-read README lines 79, 84–92, 95, 97–101, all of which exist as anchored. The S071 page was not reopened by this seat. The anchor slips from Q1 and Q3 stand. |
| Q11 / Q12 interval gate | N/A (pass) | No binary-rate PASS against a bar. `812/812` is a deterministic census, not a sampled rate. |
| Q13–Q16 admission timing | NOT YET EVALUABLE | There is no Gate row or admitting commit to grade. The prerequisite `writer: KengakuR29-2` exists at line 4 and differs from this seat. |
| (Q17, outside the assigned range) | N/A | The candidate makes no source-use-consistency calibration claim. |

## Findings (counterexample, evidence, smallest safe correction)

**F1 — false two-outcome claim about quote-bearing values (Q3, Q4; strongest counterexample).**
Candidate line 30–31 says, in a 19-word quote: "a value containing `"` or `\` therefore makes the projected JSON invalid
or is decoded as a JSON escape".

Counterexample (`inject.py`, exit 0): set SHOPPING to `http://shopping.invalid","zz_injected_key":"x` and
apply the S070 order to the pinned raw text. Observed: `json_valid True parsed 812`, with
`tasks_with_injected_top_key 192`. Task 21's `start_url` is truncated to `'http://shopping.invalid'`, and its
original path moves into the new key. The same holds for SHOPPING_ADMIN (182 tasks) and MAP (128 tasks).
These three tokens occur only in object-member leaves: SHOPPING 275, SHOPPING_ADMIN 300, MAP 133, array 0.
GITLAB and REDDIT occur in arrays (8 and 52), so the same value is invalid there; that is why `probe.py`'s
GITLAB attempt printed `Expecting ',' delimiter`.

So a third outcome exists: **valid JSON with silently changed structure**. The S071 row itself teaches
"duplicate names keep the last value", which makes key-collision variants valid as well. Separately, the only
S071 located quote (`build/R29SourceJsonDocs.md`) is about `dumps` output escaping, 14 words: "thus escaping
the output so that the resulting strings only contain printable ASCII characters." It does not cover
`loads` rejection or escape decoding, so lines 30–31 widen beyond their quote.

The decision rule at lines 73–74 ("reject any value carrying `"`, `\`…") stays safe and needs no change.
Smallest correction: rewrite line 31 as "…makes the projected JSON invalid, decodes as a JSON escape, or
parses as valid JSON with altered structure (e.g. an injected key)…". Then either add a located S071 quote
for invalid-document line 402 or drop the `\n` example, or cite a row whose scope covers escape decoding.

**F2 — README exception list omits WIKIPEDIA's path (Q3).**
Candidate line 27–28 says, in a 12-word quote: "the README's step 2 exports scheme-less example `origin:port` values
(SHOPPING_ADMIN adds `/admin`)".

The pinned README line 91 is `export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"`,
and the S072 row's teaches cell says "WIKIPEDIA adds a long path, HOMEPAGE is marked placeholder". Listing
only SHOPPING_ADMIN as the exception asserts that WIKIPEDIA is origin:port, which widens beyond the source.
Correction: "(SHOPPING_ADMIN adds `/admin`, WIKIPEDIA adds a long path)".

**F3 — the "non-URL" count depends on reading categories by JSON path, and the entry does not say so (Q4).**
Observed: all 61 non-URL changed leaves start with a token (`token_prefixed 61`). Examples begin
`__REDDIT__/f/books/59396/…`. They are URL-shaped values in non-URL fields. `corpus/lessons/round-29.md`
M89 records that value-shape reading gives 0. The headline at line 56, "Global text replacement reaches
non-URL fields", is true by field. But a value-shape URL-only rule would project all 61, so line 57's
claim holds only for the narrower "URL-fields-only" rule.
Correction: add "all 61 are token-prefixed URL-shaped strings; the category is by JSON path".

**F4 — no falsifier, and some negative space is missing (Q4, format).**
The candidate has no falsifier statement. Suggested falsifiers, modelled on r28 line 152:
- a pinned digest changes;
- remaining tokens are nonzero;
- index ≠ task_id on the frozen order;
- a reversed-order run differs on the frozen profiles;
- the 61 non-URL leaves move.

Minor omissions:
- 23 tasks (97, 265–268, 424–430, 556–561, 737–741) declare `sites` wikipedia, but none carries `__WIKIPEDIA__`. Their start URLs are `__MAP__` (17 tasks) or `__GITLAB__` (6 tasks).
- None of the three profiles has the README's scheme-less shape.
- Literal hosts that the projection never touches remain in answer, intent and annotation fields: 13 occurrences across 6 hosts, none in `start_url`, `reference_url` or `program_html` URL fields (`probe.out`).

**F5 — format divergences from `webarena-task-spec-audit.md`.**
These follow the reference: the triad plus `writer:`, the H1 `Title — subtitle` pattern, and the sections
"What this adds and what it does not", "Observed … (2026-10-21)", "Operational decision rule" and
"Calibration and adjacent scope".

These diverge:
- The decision rule is inline (1)–(4) prose (lines 70–75); the reference uses a numbered list (lines 145–150).
- No `Falsifiers:` paragraph.
- No receipt paths, no selftest case count (the instrument shows 20) and no oracle or authorship line (compare reference lines 103–108 and 130–135).
- The table header reads `| unit | value |` (line 38), but its cells are observables; the reference uses `| observable | measured value |`.
- The S068 cite has no anchor, and the S071 anchor is inexact.
- There is no bounded prior-art line (reference lines 21–24). This is acceptable, because the candidate makes no novelty claim and line 80 says scores are unchanged.

## Impacted axes

Novelty is not affected: no score claim, and the frontier is named correctly. Fidelity and calibration of
the entry text are affected by F1 and F2, which are load-bearing sentence errors with reproducible
evidence. Observability is affected by F4 and F5. None of these findings touches the instrument's numbers,
which all reproduce. [INFERENCE] The selftest case name `quote_backslash_decode_failure_and_escape_semantics`
suggests the instrument's hand coverage shares F1's two-outcome model. This seat did not read the source,
so that remains unverified.

## Scope

Scoped to entry quality against Q1–Q16 and format. This is not a round admission. Q7, Q8 and Q13–Q16 are
pre-admission states, not candidate defects. The FAIL rests on Q3: F1 (with an executed counterexample)
and F2.

VERDICT: FAIL

## Re-check at dbcecded (follow-up)

Same seat `KengakuR29-2.FEntryQuality-2` (critic, read-only leaf), same item. This is a second-seat Q10
re-read of candidate v2. Lane master: `dbcecded4a04247cf6fd12919327af973da10bdd`. Canonical path:
`corpus/knowledge/webarena-config-projection.md` (still absent; `test -e` exits 1). Reviewed bytes:
`.ufo/waves/round-29/drafts/webarena-config-projection.md`, with sha256
**435d4bb1c7b1881d2fdc8a29f84719ec39f199bd0bc96d60fde5a647cd98f8e5**. I printed this digest first, and it
equals `candidate-freeze-v2.json`.

Earlier bytes of this report are unchanged: before this append the file was 13000 bytes with sha256
`d1315ad0…e31c`, and this section was added with `>>`.
Tool installs/updates: none.
Production `plans/config_projection.py` source: not read. I only ran its CLI.
Network: public GETs of the BrowserGym `task.py` at its pin and of `docs.python.org/3/library/json.html`.
All `/tmp` copies were deleted (`ls /tmp | grep -c FEQ2` → 0). The mutation witness used its own
`tempfile` directory and cleaned it up. New scratch files are `recheck_v2.py` and `recheck_v2.out` in my
scratch directory.

### Receipts re-run at dbcecded

| check | observed |
|---|---|
| instrument sha256 | `135cc682…a142`, equal to the v2 freeze |
| `--summary` | exit 0, `TOTAL findings=0 exit=0`, `DUPLICATE_OBJECT_KEYS 0` |
| `--selftest` | exit 0, `SELFTEST clean cases=28` |
| `--json` sha256 | `a4fb5d6d…d851`, equal to the v2 freeze and to `repair-json-sha256.txt` |
| `plans/fixtures/r29/mutation_witness.py` | exit 0; all 10 mutants killed (`--selftest` exit 1 for each). The frozen `--summary` notices only `url_only_substitution` and `runtime_marker_counted_as_token` (summary exit 1); the other 8 are invisible on frozen data, consistent with v2 lines 61–75. |
| would-be file digest | My source-key-order `json.dumps(task, indent=2)` digest for distinct_origins index 0 is `9533088e…`, equal to the instrument's `would_be_file_sha256` |
| S074 bytes | 8603 bytes, sha256 `f996dfee…fe67`, equal to the row. Lines 55–69 hold the six ordered `.replace` calls followed by `json.loads`; lines 81–82 select `conf["task_id"] == task_id`. |
| S071 page (Python 3.15.1) | "If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised" is present. "ignores all but the last name-value pair for a given name" (11 words) is present. |
| oracle reports cited at lines 59–60 | `FOracleText`, `FOracleLeaf`, `FOracleProvenance` and `FOracleIndex` exist and are git-tracked; each has its own seat `writer:` and ends `VERDICT: PASS` |

### New v2 numbers, independently re-derived (`recheck_v2.out`)

| v2 line | v2 value | mine |
|---|---|---|
| 47 | 790 one-token + 22 two-token tasks; 834 rows; 812 tasks | `{1: 790, 2: 22}`; 790 + 2×22 = 834 |
| 48 | 13 leaves hold 32 occurrences; 1435 = 1416 + 19 | 13 leaves, 32 occurrences |
| 52 | `__last_url__` 65 / 55 tasks; `__page__` 12 / 9 tasks | 65 / 55; 12 / 9 |
| 54 | 697 junctions in 462 tasks | 697 occurrences in 462 tasks |
| 31 | HOMEPAGE is never replaced | there is no HOMEPAGE replace call in S070 lines 11–16, and `__HOMEPAGE__` occurs 0 times in the raw file |
| 35–36 | a value containing `"` can inject keys or duplicate a `task_id` that overrides the original | MAP value `…","task_id":999999,"zz":"x` parses to 812 tasks; 128 tasks are overridden to 999999; distinct IDs fall to 685 |

All v1 numbers that are unchanged in v2 still reproduce; see the first section of this report.

### My two Q3 failures

- **F1 — RESOLVED.** v2 lines 34–37 now give three outcomes for `"`: invalid JSON, or valid JSON "with
  altered structure (injected keys, a duplicated `task_id` overriding the original)". The sentence is
  anchored to S071's invalid-document line 402 and duplicate-names lines 624–625; both sentences exist on
  the reopened page. My injection reproduces the `task_id` override (128 tasks).
- **F2 — RESOLVED.** v2 lines 30–31 now read "SHOPPING_ADMIN adds `/admin`, WIKIPEDIA a long path,
  HOMEPAGE is a placeholder…", which matches README lines 86–92 and the S072 row.

### Q1–Q16 on v2

| criterion | verdict | evidence |
|---|---|---|
| Q1 | PASS | Triad and `writer:` at lines 1–4. The S071 anchor is now numeric (§576-591, 402, 624-625), S074 is anchored (55–69, 81–82) and S068 is anchored by its manifest byte pin. |
| Q2 | PASS with one residual | S070–S074 and S068 are tier A for their scopes. Residual: "`\n` becomes a newline" (line 37) still has no anchored row; S071's anchors cover rejection and duplicates, not escape decoding. This is non-blocking because the decision rule at line 83 rejects any `\` regardless. |
| Q3 | PASS | F1 and F2 are resolved. The new S074 sentences (lines 12, 84) match `task.py:55–69,81–82`. |
| Q4 | PARTIAL | New disclosures: JSON-path category with URL-shaped values (lines 57–58), scheme difference (lines 20–21), marker task counts. Still missing: an explicit statement of the observation that would falsify the claim. The word at line 58, "Falsification:", introduces the oracle agreement that was obtained, not a falsifier (compare r28 line 152). |
| Q5 | PARTIAL | Line 61 now discloses that the instrument author wrote the entry, and S074 is labelled as prior practice. But line 58 reads "four independently written oracles reproduced every count" (7 words), unqualified. `falsify/FCritOracleIndependence.md:75` (VERDICT: PARTIAL) says "Unqualified independence/blindness … unsupported". The oracle seats share the lane identity `KengakuR29-2.*`. |
| Q6 | PASS | Extends `corpus/README.md:338`; S074 is cited as precedent, not duplicated. |
| Q7 | NOT MET (pre-admission) | Canonical file absent; `corpus/README.md:350` still names the draft; receipts are now cited (line 61). |
| Q8 | NOT YET EVALUABLE | `corpus/lessons/round-29.md` (untracked in the working copy) has no `^## Gate`. |
| Q9 | N/A | No rejection stated. |
| Q10 | PASS for this seat's scope | All numbers re-derived; S072, S073 and S074 bytes plus S071 text reopened. S070 was reopened in the first section through its pinned bytes. |
| Q11 / Q12 | N/A (pass) | No rate-versus-bar claim. |
| Q13–Q16 | NOT YET EVALUABLE | No Gate row or admitting commit. Writer `KengakuR29-2` differs from this seat. |

### Smallest corrections to clear the residuals

1. Q4: add one `Falsifiers:` line. Examples: a pinned digest changes; remaining tokens ≠ 0; index ≠ task_id on the frozen order; a reversed-order run differs on frozen profiles; the 61 non-URL / 1355 URL split moves; an oracle disagrees.
2. Q5: change "independently written oracles" to "separately written oracles by distinct same-lane seats (independent logic, not independent identity)".
3. Q2: anchor the `\n` decoding example to a located S071 line, or drop it.

Scope: this verdict covers only this re-check of v2 against Q1–Q16 and my two Q3 failures. Both Q3 failures
are resolved and every number reproduces. The candidate is not yet PASS on Q4 (no stated falsifier) or on
Q5 (oracle independence stated without qualification). Q7, Q8 and Q13–Q16 are pre-admission states.

VERDICT: PARTIAL

## Final re-read of candidate v3 (follow-up)

Same seat `KengakuR29-2.FEntryQuality-2` (critic, read-only leaf), same item. Reviewed bytes:
`.ufo/waves/round-29/drafts/webarena-config-projection.md`, with sha256
**59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca**. I printed this digest first. Canonical
path: `corpus/knowledge/webarena-config-projection.md` (still absent). Lane HEAD is `dbcecded`; the
candidate, `plans/config_projection.py` and `plans/fixtures/r29/mutation_witness.py` are modified in the
working copy, and no `candidate-freeze-v3.json` exists.

Earlier bytes of this report are unchanged: the file was 20176 bytes with sha256 `5f3788cf…b587` before
this `>>` append.
Tool installs/updates: none.
Production source: not read; CLI runs only.
`/tmp` copies deleted (`ls /tmp | grep -c FEQ3` → 0).

### Diff scope and receipts (observed)

| check | observed |
|---|---|
| v2 bytes at `dbcecded` | `git show` gives sha256 `435d4bb1…f8e5`, the v2 digest I reviewed above |
| v2→v3 diff | `git diff --unified=0` shows hunks `@@ -37 +37 @@` and `@@ -58,4 +58,13 @@` only, so every other line is byte-identical to v2 |
| working-copy instrument | sha256 `d81a6af8…4f9f`. This differs from the v2 freeze's `135cc682…`, as the coordinator announced. |
| `--json` sha256 | `a4fb5d6d…d851`, unchanged from the v2 freeze, so projected objects and metrics are unchanged |
| `--summary` against the `dbcecded` tool | exit 0, findings 0. The only differences are an added `INPUT` digest line per profile block and the rename `index_task_id_mismatches` → `index_task_id_mismatch_count`; every count is identical |
| `--selftest` | exit 0, `SELFTEST clean cases=30` |
| `mutation_witness.py` (working copy) | exit 0; 12 of 12 mutants killed; restored sha256 equals `d81a6af8…` |
| `repair-projection-equality.json` (git-tracked) | It compares `56fd949`'s tool with `135cc682…`: `occurrence_provenance_equal true`, and `tasks_equal_as_objects true` / `other_fields_equal true` for all three profiles. Its stated limit is that dict equality ignores key order. Key order is covered separately: my source-order index-0 digest `9533088e…` matched in the v2 re-check. |

### Changed lines judged

- **Line 37 (Q2 residual): resolved.** The unanchored "`\n` becomes a newline" example is gone. What
  remains, "can make it invalid or be interpreted as a JSON escape", is a generic statement that rule (4)
  makes non-load-bearing, since any `\` is rejected. I accept it without a separate anchor.
- **Lines 58–59 (my Q5 finding): resolved.** v3 now reads "separately written by distinct same-lane
  seats (independent logic, not independent identity)". This matches the correction I proposed and
  `FCritOracleIndependence.md`'s objection.
- **Lines 60–63: accurate.** The oracle scope is now "population/profile metrics, all 1435 provenance
  records and all 2436 projected objects and would-be file digests". The task-unit bridges (790/22, 32,
  55/9, 462) are now attributed to the entry-review seats. My `recheck_v2.out` contains exactly those
  four re-derivations. Line 63 keeps the authorship disclosure.
- **Lines 64–65: accurate.** The receipt is tracked and states what is claimed. The chain from oracle
  objects (v1 tool) to the `135cc682` objects is shown by the receipt; the link from `135cc682` to the
  working copy is shown by the identical JSON digest.
- **Lines 66–70 (my Q4 finding): resolved.** An explicit `**Falsifiers:**` paragraph now names a
  digest-change withdrawal plus four observation falsifiers (remaining tokens, the 61/1355 split,
  index/task-ID mismatch, and disagreement with a separately derived object). It also states the
  general-input boundary. Each falsifier is currently checkable and, per the receipts above, not triggered.

### Final Q1–Q16 on v3

| criterion | verdict | basis |
|---|---|---|
| Q1 | PASS | Lines 1–4 are unchanged from v2: triad plus `writer:`, all anchors exact. |
| Q2 | PASS | S068 and S070–S074 are tier A for their scopes; line 37's residual is removed. |
| Q3 | PASS | F1 and F2 were resolved in v2 and are unchanged; the new lines 58–70 stay within their receipts. |
| Q4 | PASS | Explicit falsifiers at lines 66–70; negative space as in v2. |
| Q5 | PASS | Same-lane independence is qualified; the author/instrument identity is disclosed; S074 is labelled as prior practice. |
| Q6 | PASS | Unchanged; extends `corpus/README.md:338`. |
| Q7 | NOT MET (pre-admission) | No canonical file or index row yet. Admission must land the entry, index and coverage rows, S070–S074 used-by links, and the final tool bytes (`d81a6af8…` or later) together. |
| Q8 | NOT YET EVALUABLE | `corpus/lessons/round-29.md` is untracked and has no `## Gate`. |
| Q9 | N/A | No rejection stated. |
| Q10 | PASS for this seat | Sources reopened: S070, S072 and S073 in the first section, S071 and S074 in the v2 re-check. Every number re-derived; v3 changes no number. |
| Q11 / Q12 | N/A (pass) | No rate-versus-bar claim. |
| Q13–Q16 | NOT YET EVALUABLE | No Gate row or admitting commit. Writer `KengakuR29-2` differs from this seat. |

Admission notes, not defects in the candidate:
- The tool bytes cited by the v2 freeze (`135cc682…`) are not the working-copy bytes (`d81a6af8…`), so the admitting commit or a v3 freeze must pin the final tool bytes.
- `falsify/FEntryNumbers.md` and `FCritOracleIndependence.md` currently end in PARTIAL; their owners must re-read v3.

Scope: this verdict covers source fidelity, numbers and entry quality (Q1–Q6, Q10) of exactly the v3 bytes
above, against the original two Q3 failures and the v2 residuals. Every candidate-quality criterion this
seat owns passes. Q7, Q8 and Q13–Q16 are admission-time obligations outside this seat's verdict and are not
satisfied by it.

VERDICT: PASS

## Exact-v4 locator re-check (follow-up)

Same seat `KengakuR29-2.FEntryQuality-2` (critic, read-only leaf), same item. The scope is only the line-1
locator change; there was no new broad review and no extra sources. Reviewed bytes:
`.ufo/waves/round-29/drafts/webarena-config-projection.md`, with sha256
**9d11f44bf22d357758a5988b514d23cca84d4061816d3c3d65294974dd506e74**. Canonical path:
`corpus/knowledge/webarena-config-projection.md`.

Earlier bytes of this report are unchanged: the file was 26021 bytes with sha256 `0105207f…d5db` before
this `>>` append.
Tool installs/updates: none.
Network: one public GET of `https://docs.python.org/3/library/json.html` per probe.
`/tmp` copies deleted (`ls /tmp | grep -c FEQ4` → 0).

Note on provenance: this seat's own anchor finding (v1 Q1, the inexact S071 cite) was already resolved in v2.
The renderer-line concern this correction answers came from another seat. I check here that the new
fragments hold the text they are cited for.

### Byte comparison against v3

- `git diff --unified=0 dbcecded` (v2) shows hunks `@@ -1 +1 @@`, `@@ -37 +37 @@` and `@@ -58,4 +58,13 @@`.
  The last two are the v3 changes I already passed.
- Reconstructing v3 as v2's line 1 followed by v4's lines 2 to the end gives sha256
  `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`. That is exactly the v3 digest I passed,
  and `candidate-freeze-v3.json` names the same digest. So **only line 1 changed** from v3, and lines 2 to
  the end are byte-identical to v3.

### Fragment check (section/entry boundaries, not renderer lines)

I extracted each `id="…"` element from the live page (Python 3.15.1) up to the next section or entry.

| v4 line-1 locator | fragment present | cited text inside that fragment |
|---|---|---|
| `#character-encodings` ensure_ascii paragraph | yes | yes: `ensure_ascii` and "printable ASCII" both appear within the section |
| `#repeated-names-within-an-object` opening paragraph/example | yes | yes: "last name-value pair" and the `weird_json` example both appear within the section |
| `#json.loads` invalid-document exception | yes | **no.** The `#json.loads` entry (561 characters, ending before `#json.JSONDecoder`) reads "Identical to load(), but instead of a file-like object, deserialize s…" and has no exception sentence. The sentence "…not a valid JSON document, a JSONDecodeError will be raised" sits in the `#json.load` entry, with a second copy under `#json.JSONDecoder`. |

The fact is correct: `json.loads` is documented as identical to `load()`, so it inherits the exception.
The **locator is not**: one of the three fragments points to an entry that lacks the cited sentence. The new
`corpus/SOURCES.md` S075 row has the same mismatch ("Basic Usage json.loads (#json.loads) invalid-document
exception").

Smallest correction, a locator-only change applied identically in v4 line 1 and in a superseding SOURCES
row (S075's cells are not edited in place): "#json.load invalid-document exception, which #json.loads
inherits ('Identical to load()')". Citing `#json.JSONDecoder` instead also works. No fact, count or body
line needs to change.

### Verdict

Lines 2 to the end are byte-identical to the v3 that passed. Two of the three new locators are correct.
The third, `#json.loads`, does not contain its cited invalid-document sentence. The locator fix therefore
does not fully hold on these exact bytes. The PASS on Q2–Q6 and Q10 for content still stands; this affects
only Q1's exact-anchor requirement and the matching Q10 location re-read.

VERDICT: PARTIAL

## Exact-v5 locator confirmation (follow-up)

Same seat `KengakuR29-2.FEntryQuality-2` (critic, read-only leaf), same item. The scope is the line-1
locator only. Reviewed bytes: `.ufo/waves/round-29/drafts/webarena-config-projection.md`, with sha256
**c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3**. Canonical path:
`corpus/knowledge/webarena-config-projection.md`.

Earlier bytes of this report are unchanged: the file was 29595 bytes with sha256 `23160389…d853` before
this `>>` append.
Tool installs/updates: none.
No network: the fragment facts come from my v4 probe of the live page earlier today.

- **Byte scope.** v2's line 1 followed by v5's lines 2 to the end gives sha256
  `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`, the v3 digest I passed. v4 equals v3
  outside line 1, as established in the v4 section. So v5 differs from v3 and v4 **only in line 1**.
- **Line-1 fix.** v5 now reads "#json.load invalid-document exception inherited by #json.loads (Identical
  to load())". This matches my v4 observations exactly:
  - the invalid-document JSONDecodeError sentence's nearest preceding `id` is `json.load`;
  - the `#json.loads` entry reads "Identical to load(), but instead of a file-like object…".

  `#character-encodings` and `#repeated-names-within-an-object` are unchanged and were already confirmed.
- **Source row.** S076 is a new superseding row that corrects only S075's `json.loads` locator; S075's cells
  were not edited. Its anchor and teaches cells agree with line 1.
- **Result.** My v4 locator finding is resolved. Q1's exact-anchor requirement and the Q10 location
  re-read now pass. Q2–Q6 and Q10 content pass carries over unchanged from v3. Q7, Q8 and Q13–Q16 remain
  admission-time obligations outside this seat's verdict.

VERDICT: PASS
