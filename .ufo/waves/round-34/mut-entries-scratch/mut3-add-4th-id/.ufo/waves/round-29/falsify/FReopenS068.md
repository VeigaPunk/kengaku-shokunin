writer: KengakuR29-2.FReopenS068-2

# FReopenS068 — live reopen of S068 for a used-by addition

**Seat:** `KengakuR29-2.FReopenS068-2` (actual writer: same)
**Target:** `corpus/SOURCES.md:90` (S068), the raw-task row reopened for a round-29 used-by addition.
**Lane state read:** `56fd949a6478342531e61f4feecb4a685d831640`; `corpus/SOURCES.md` is unmodified in the working tree (`git status --porcelain` shows it untracked-free).
**Axes this seat moves:** novelty — does S068's declared authority actually cover the round-29 use (raw-task input pin)? Fidelity — do the live bytes equal the pin and the frozen fixture? Observability — are the anchor lines, quote and word count exact and re-runnable?
**Production-source disclosure:** I did **not** read or import `plans/config_projection.py` to derive any cell. I ran one read-only `grep -n` against it only to see which paths it pins; no cell below depends on that file.
**Tool installs/updates:** none (no pacman, no service restart; stdlib Python 3.14 and curl only).

## 1. Live opening (observed)

URL: `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`

| Field | Observed value |
|---|---|
| Access date (local / UTC) | 2026-10-21 13:52 -03 / 2026-10-21T16:52:20Z |
| HTTP Date header | `Wed, 21 Oct 2026 16:49:05 GMT` |
| HTTP status | `200` |
| Content-Type | `text/plain; charset=utf-8` |
| Content-Length | `880776` |
| Bytes on disk (`wc -c`, `stat`) | `880776` |
| SHA-256 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| ETag | `"e6f6671b396a513c165c6ae06e21995bd5bb8e8637b339455ae5f17bd3ddd724"` |
| Effective URL | identical to the requested URL (no redirect) |
| Second fetch (`curl` again, 16:49Z) | `200`; `cmp` with first fetch → `IDENTICAL_REFETCH` |
| Frozen fixture `plans/fixtures/r28/webarena/config_files/test.raw.json` | 880776 bytes; same SHA-256; `cmp` → `IDENTICAL_PINNED_FIXTURE` |
| `plans/fixtures/r28/webarena/manifest.json:5–8` | `sha256` 7b50386f…; `bytes` 880776 |
| `plans/fixtures/r29/manifest.json:10–12` | same `sha256` 7b50386f… (no `bytes` field on this entry) |

Commands (lane root and `/tmp/s068probe`; writes confined to `/tmp`):

```text
$ curl -sS -o test.raw.json -w 'http_status=%{http_code}\nsize=%{size_download}\neffective_url=%{url_effective}\n' \
    'https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json'
http_status=200
size=880776
effective_url=https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json

$ sha256sum test.raw.json
7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652  test.raw.json

$ cmp test.raw.json plans/fixtures/r28/webarena/config_files/test.raw.json && echo IDENTICAL_PINNED_FIXTURE
IDENTICAL_PINNED_FIXTURE
```

Byte-level shape: first bytes `b'[\n  '`, 29604 LF, 0 CR, no BOM, final byte `\n`, 812 parsed records, 812 distinct `task_id` values (0–811), `index == task_id` true for all 812. These are census facts about the pinned bytes, not a runtime or validity claim.

## 2. Cell-by-cell verification against the live bytes

Row at `corpus/SOURCES.md:90`. Six cells named in the assignment (scope, anchor, teaches) plus the bookkeeping cells:

| Cell | Cell text (fragments ≤25 words) | Live evidence | Result |
|---|---|---|---|
| id/source | `S068` … `WebArena raw-task anchor and quote correction` + the dce04686 URL | URL served 200 at the pinned revision; bytes equal the pin | supported |
| kind | `dataset` | the file is the authored task JSON array; 812 records | supported |
| tier | `A` | `corpus/SOURCES.md:7–8`: primary/authoritative for the row's scope; a pinned upstream source artifact | supported |
| scope | `this snapshot's intent and complete eval fields, not runtime validity` | 812/812 tasks have a nonempty `intent`; 812/812 have an `eval` object carrying the four core keys (`eval_types`, `reference_answers`, `reference_url`, `program_html`); no runtime validity is claimed | supported (see Q3 reading note) |
| anchor | `dce04686, task0 intent16, eval object18–29, eval_types19–21, references22–24, program_html26; manifest byte pin` | every range rechecked below; both manifests pin the SHA; r28 manifest carries `bytes` 880776 | supported (see Q2 label note) |
| teaches | `supersedes S061's abbreviated anchor — eval_types is a multiline field at19–21, not the complete eval object`; `authored intent and predicate fields are explicit, separate data` | S061 at `corpus/SOURCES.md:83` says `task0 eval:18–21`; live line 19–21 is the multiline `eval_types`, while the eval object closes at line 29; `intent` (16) and the eval fields are separate authored keys | supported |
| status | `mined` | `corpus/knowledge/webarena-task-spec-audit.md` exists, is tracked, and cites S068 at lines 1 and 26 (`S061/S068 are authoritative for authored specs`) | supported |
| opened | `2026-10-21` | round-28 Gate records the S068 opening on 2026-10-21 (`corpus/lessons/round-28.md:208`); evidence JSON `accessed` 2026-10-21 (`source-correction-quotes.json:15`) | supported |
| recheck | `on-release` | commit-pinned snapshot; matches S061–S063/S069 practice (`corpus/SOURCES.md:83–91`) | supported as policy |
| used-by | `corpus/lessons/round-28.md, corpus/knowledge/webarena-task-spec-audit.md` | both paths exist and are tracked; both cite S068 (`round-28.md:169,208,217,242`; knowledge file lines 1, 26) | supported |

### Anchor line numbers (live file)

| Anchor claim | Live line(s) | Exact observed text |
|---|---|---|
| `intent16` | 16 | `    "intent": "What is the top-1 best-selling product in 2022",` |
| `eval object18–29` | 18–29 | line 18 `    "eval": {`; line 29 `    },` (line 30 is `intent_template_id`, line 31 closes task0) |
| `eval_types19–21` | 19–21 | 19 `      "eval_types": [`, 20 `        "string_match"`, 21 `      ],` |
| `references22–24` | 22–24 | 22 `      "reference_answers": {`, 23 `        "exact_match": "Quest Lumaflex\u2122 Band"`, 24 `      },` |
| `program_html26` | 26 | `      "program_html": [],` |

The line numbers are physical lines after UTF-8 decode; the file has no CR and no BOM, so `nl -ba` and Python `split('\n')` agree. Task0 occupies lines 2–31; line 1 is `[` and the last line is `]` + newline (implicitly line 29605 after the final LF).

## 3. Quote re-location and programmatic count

### 3.1 The assignment's named build locus is empty

The target says the build seat's ≤25-word quote is in `.ufo/waves/round-29/build/R29Source*.md`. It is not. Observed counts:

```text
R29SourceCaller.md    eval_types=0  S068=1  exact-quote=0
R29SourceGenerator.md eval_types=0  S068=3  exact-quote=0
R29SourceJsonDocs.md  eval_types=0  S068=1  exact-quote=0
R29SourceWorkflow.md  eval_types=0  S068=0  exact-quote=0

$ grep -rn '"eval_types": \[' .ufo/waves/round-29/build/
(no output; rc=1)
```

The round-29 build report that examined S068's row status is `build/R29DraftEntry.md`: it confirms the pinned SHA at line 20 and states at line 29: `S068: existing row; its pinned raw file sha is confirmed above. Used-by link deferred.` (The other S068 mentions, `R29SourceGenerator.md:107` and `R29SourceCaller.md:97`, are supersession/practice notes, not openings.) No round-29 build seat wrote an S068 located quote. `build-dead-seats.json` contains no S068 seat.

### 3.2 The actual located quote (round-28 evidence) re-located and counted

The only S068 quote record is `corpus/evidence/round28-calibration/source-correction-quotes.json:11–16`:

```text
"id": "S068",
"location": "task0 test.raw.json:19",
"quote": "\"eval_types\": [",
"whitespace_words": 2
```

The round-28 Gate record `corpus/lessons/round-28.md:208` displays it with presentation backslashes; the erratum at `corpus/lessons/round-28.md:238–242` corrects the display to `"eval_types": [`, source line 19, 2 whitespace-delimited words.

Live verification:

| Check | Observed |
|---|---|
| Line 19 exact bytes | `      "eval_types": [` |
| Quote occurrences in the whole file | 812 (one per task's `eval_types` field) |
| Occurrences on line 19 | 1 |
| First five line numbers carrying the quote | 19, 49, 79, 109, 142 |
| `len(quote.split())` | 2 |
| `len(re.findall(r'\S+', quote))` | 2 |
| Escaped display form `\"eval_types\": [` | also splits to 2 whitespace words |
| Declared count in the evidence JSON | 2 |
| ≤25 constraint | satisfied (2 ≤ 25) |

The quote is a field-opening shape, not a unique value; the `task0` locator plus line 19 disambiguates it. The locator is needed because the same text occurs 812 times.

## 4. Mismatches and qualifiers (exact locations and values)

None of these invalidates an S068 cell; they are recorded because the assignment asks for every mismatch.

**Q1 — assignment's build-quote pointer.** No `"eval_types": [` occurs anywhere under `.ufo/waves/round-29/build/` (`grep` rc=1), and none of the four `R29Source*.md` files contains `eval_types` at all. The quote exists only in the round-28 evidence JSON and the Gate/erratum. The pointer `R29Source*.md` is wrong; the quote itself is verified above.

**Q2 — anchor label `references22–24`.** The live literal key at lines 22–24 is `reference_answers`; the string `"references"` occurs **0** times in the file, while `"reference_answers"` occurs 812 times. The range 22–24 is exact, and the lane's prior re-read (`corpus/lessons/round-28.md:208`; `.ufo/waves/round-28/falsify/FSourceS061.md` addendum) also treats `references` as short for `reference_answers`. This is shorthand, not a line-range error; a literal reader cannot grep `references` in the JSON.

**Q3 — scope reading.** `this snapshot's intent and complete eval fields` is supported for the complete eval object and for the four core keys (812/812 each). It is **not** a complete inventory of optional eval keys: the snapshot's eval-key union is eight keys, and task0 lacks `url_note` (present in 196 tasks) and `annotation_note` (present in 1 task). If a reader takes `complete eval fields` as "every key that appears anywhere in the snapshot", the cell overstates; under the intended reading "the eval object in full, not just `eval_types`", it is supported. The anchor's `eval object18–29` is the load-bearing evidence.

**Q4 — used-by addition basis.** Only the round-29 candidate cites S068: `.ufo/waves/round-29/drafts/webarena-config-projection.md:1` says `S068 raw-task input pin` with the raw URL. That use is the pinned file identity, which the anchor's URL + manifest byte pin support. The candidate's substantive projection claims come from S070/S071/S072/S073, not from S068's intent/eval scope. By contrast, `corpus/lessons/round-29.md` contains **zero** source IDs (`grep -c 'S0'` → 0), so adding the lesson to S068's used-by would not be supported by the lesson text. At admission, add only the canonical entry path (`corpus/knowledge/webarena-config-projection.md`), never the draft path; do not add the lesson unless it later cites S068.

**Q5 — manifest ambiguity (minor).** The anchor says `manifest byte pin` without naming a manifest. Two manifests pin the same SHA: `plans/fixtures/r28/webarena/manifest.json:5–8` (SHA + `bytes` 880776) and `plans/fixtures/r29/manifest.json:10–12` (SHA only). Both match the live bytes; only the r28 manifest actually carries a byte count, so `byte pin` is literal only against the r28 manifest.

## 5. Observed vs inference and remaining unknowns

**Observed:** the HTTP status, headers, byte count, SHA-256, refetch identity, fixture identity, manifest pins, line texts and line numbers, task count/distinct IDs, eval-key census, quote occurrences and word counts, and the grep counts in the build reports. Every number above came from a command or a parsed byte read, not from a prior report.

**`[INFERENCE]`:** that the candidate's `raw-task input pin` is its only S068 reliance (from a single occurrence of `S068` at draft line 1); that `references` is lane shorthand rather than a mistaken key name (supported by the prior lane usage, but not defined in the row); that the used-by addition is admission-conditional (from `plans/round-29-claims.md:88` and the fact that the candidate is still a draft).

**Unresolved:** the assignment's named build-quote locus cannot be satisfied as written; the quote was recovered from the round-28 evidence instead. No S068 byte, line or cell is unresolved.

**Scope of this verdict:** S068's live byte identity, every registry cell, the anchor line numbers, and the quote relocation/word count. It is not a round admission, not a Q10 second-seat pass on the candidate, and not a judgment of the projection's behavior.

VERDICT: PASS
