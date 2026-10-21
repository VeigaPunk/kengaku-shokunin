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
