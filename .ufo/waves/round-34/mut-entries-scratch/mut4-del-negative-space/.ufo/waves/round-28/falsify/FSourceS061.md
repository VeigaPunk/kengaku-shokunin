# FSourceS061 — S061 source reopen: URL, date and digest hold; the quoted fragment is a normalized rendering and the "eval object" anchor range is wrong

Identity: `KengakuR28.FSourceS061` (scout, read-only, author-side). Candidate writer `KengakuR28`.
This report is a source-row/draft-source-use falsification, not a complete Q10 candidate re-read and
not an admission. No production edit, build, test, linter, formatter or install was performed.

## Frozen revision and canonical path

- Candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, sha256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (re-hashed 2026-10-21; equals
  `.ufo/waves/round-28/candidate-freeze.json`).
- Proposed canonical path: `corpus/knowledge/webarena-task-spec-audit.md`. It does **not** exist on
  disk (`ls` → "No such file or directory"); the candidate is not admitted.

## What the row, Gate and draft actually say

| location | text observed |
|---|---|
| `corpus/SOURCES.md:83` (admitted production row S061) | kind `dataset`, tier `A`; scope "this repository snapshot's authored task fields, not runtime task validity or paper-era scores"; anchor "dce04686 (2025-11-26), task0 eval:18–21; sha256 in plans/fixtures/r28/webarena/manifest.json"; teaches "task intent, evaluator selection and literal scoring targets are separately authored data; static inventory does not validate the live task or contamination"; status `mined`; opened `2026-10-21`; recheck `on-release`; used-by `corpus/lessons/round-28.md` |
| `corpus/lessons/round-28.md:40` (Gate) | URL `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json`; accessed `2026-10-21`; quote ``"eval_types": [ "string_match" ]`` — "task0 eval object:18–21; complete pinned raw task specification, not runtime validity. build/OpenTasks.md independently opened byte-equal source." |
| `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md:1` | `source: S061 <same URL> task0:18–28 and selected task IDs below` |
| `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md:21` | "S061 is authoritative for authored specs; S062/S063 for their own code behavior, **not** actual browser state or judge correctness." |

## Independent observations

Opened the pinned local bytes. The lane fixture and the separately downloaded OpenTasks copy are
byte-equal; I did not re-fetch the live URL, so the access date below is the manifest/OpenTasks
observation, not a new network fetch:

- URL: `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json` (exact 40-hex commit; no typo).
- Access date: `2026-10-21` — manifest `opened` (`plans/fixtures/r28/webarena/manifest.json:3`); OpenTasks recorded its opening at `2026-10-21 (UTC 13:57)` (`build/OpenTasks.md:4`).
- Bytes/digest: `880776` bytes, sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`; `cmp` against `.ufo/waves/round-28/scratch/OpenTasks/pinned-test.raw.json` exit 0; matches manifest `files["config_files/test.raw.json"]`.
- Actual location of the quoted field: task0 record `:2–31`; `"intent"` `:16`; `"eval": {` `:18`; `"eval_types": [` `:19`; `"string_match"` `:20`; `]:` `:21`; `reference_answers` `:22–24`; `program_html` `:26`; eval block closes `:29`; `intent_template_id` `:30`.
- Literal quote test: `grep -c -F '"eval_types": [ "string_match" ]'` over the 880,776-byte file → **0**. The source fragment is three lines (19–21). Whitespace-collapsing the actual bytes yields `"eval_types": [ "string_match" ],` — the displayed quote drops the trailing comma at line 21 and inserts spaces after `[` and before `]`.
- Displayed quote length: 4 whitespace tokens / 2 identifier words (`eval_types`, `string_match`); far below 25. The omission is exactness, not length.
- Independent stdlib `json` census (no production/alternate oracle imported): 812 entries, 812 unique IDs (0–811, no gaps/duplicates), 5 evaluator-type sets, 27 (site-set, evaluator-type-set) strata, 651 `program_html` targets, 684 non-null `storage_state`, 10 site sets, all `require_login=true`, all `require_reset=false`. Task0 `eval_types == ["string_match"]`; top-level key tuples = 2 (the singleton tuple adds `string_note`, as OpenTasks states). These match the draft counters (`draft:101–105`) and the C1 summary.
- Tier/scope: tier `A` is defensible under `corpus/SOURCES.md:11–16` (primary source data at the pin); the row's scope is genuinely narrow. The Gate's scope sentence omits two exclusions present elsewhere: the row's "not … paper-era scores" and the draft's explicit "not WebArena-Verified" (`draft:15–16`). The Gate's word "complete" is defensible only for the pinned file (812/812 records, digest-pinned), not for the quoted fragment. That is an omission/ambiguity of a boundary, not a false claim; the URL commit pin already scopes the source.
- Teaches: each clause is qualitatively supported by the file — intent (`:16`), evaluator selection (`:19–21`), reference/scoring targets (`:22–28`) — and the negative boundary is a limitation, not a source finding. The row does not record the 812/5/651 census; the draft does, via the instrument.
- Draft source use: S061 appears only in the source header and the authority sentence. The draft uses it for authored specs, not runtime validity, and explicitly denies paper-era/Verified coverage. No overreach. The header's `task0:18–28` is a third, non-identical range: it spans the eval block through its last field but omits the closing `},` at `:29`; if read as the whole task0 record it omits `:2–17` and `:29–31`.
- Status/used-by: `mined` with `corpus/lessons/round-28.md` only matches the Gate's stated initial state ("new rows S061–S066 initially enter mined with the paths listed in their actual cells"); no S061 old→new cell delta is recorded. The draft's use is not yet a used-by because the candidate is unadmitted.
- Old-knowledge correction: no S061 mention exists under `corpus/knowledge/`. I found no existing knowledge entry that makes a claim about this repository's 812 tasks or evaluator-type sets; the only WebArena mention in existing knowledge is `corpus/knowledge/benchmark-selection.md:18`, "WebArena-Verified (deterministic browser)" — a different repository/product, not contradicted by S061. Therefore **S061 supports no append-only correction to existing knowledge**; inventing one would exceed tier/scope.
- Corroboration boundary: `build/OpenTasks.md:9–19` is a separate author-side seat that downloaded the same URL and `cmp`-verified byte equality. That supports the opening, but it is not Q10 second-seat independence and not outside non-author evidence (the Gate itself calls all build seats author-side).
- Instrument blind spot: the C2 frozen population/contract contain no S061/S062/S063 (`plans/fixtures/r28/registry/population.json`, `contract-expected.json`; Amendment 1.4 excludes new rows). The delivered C2 checker therefore cannot catch an anchor error in a new row; this seat's report is an observed check, not a production checker.

## Findings

**F1 — anchor object range is wrong (observed, high confidence).** The Gate says "task0 eval object:18–21" and SOURCES repeats "task0 eval:18–21". The eval block begins `:18` and closes `:29`; the quoted `eval_types` field itself is `:19–21`. As written, `18–21` stops before `reference_answers`, `reference_url`, `program_html`, `string_note` and `reference_answer_raw_annotation`, so it cannot be the eval object. If it is meant as a quote locator, it still includes the `"eval": {` line and is off by one at the start; the exact field locator is `:19–21`.

**F2 — the quote is not a literal quote (observed, high confidence).** The displayed text does not occur in the pinned bytes (`grep -F` count 0). The tokens and value are exact, but the rendering folds three lines and drops the comma after `]`. In a table that presents quotes in backticks and claims "every listed quote", this needs either an exact single-line quote (e.g. `"string_match"` at `:20`) or an explicit fold/elision marker.

**F3 — the anchor under-covers the row's own teaches (observed, medium confidence as a curation gap).** The teaches cell names "task intent" and "literal scoring targets", but the anchor cites only the eval/eval_types region; `"intent"` is at `:16`, `reference_answers` at `:22–24`, and task0's `program_html` field is at `:26` (empty for task0; the 651 targets are elsewhere in the file). The sha256 pins the whole file, so the claims are reachable, but the located anchor does not itself show the fields the teaches cell asserts.

**F4 — no old-knowledge correction is supported (observed).** I found no existing knowledge entry that makes a claim about this repository's 812 tasks or evaluator-type sets; `benchmark-selection.md:18` refers to WebArena-Verified, which S061 does not cover. The row correctly has no knowledge-path used-by yet. [INFERENCE] At admission, `corpus/knowledge/webarena-task-spec-audit.md` will need to be added to S061's used-by (the Gate says later used-by changes are separately recorded); leaving it out would understate actual use, though C2 will not see it because new rows are excluded.

**F5 — OpenTasks corroboration is real but not independent authorship (observed).** The downloaded copy is byte-equal and its digest matches; the Gate's word "independently" is defensible only as "a separate author-side seat", not as outside/Q10 independence. The Gate's outside spot-check section already concedes this.

## Adjacent S066 publisher boundary (checked, not my row)

`corpus/lessons/round-28.md:74–76` states the live DOI/publisher fetches returned 429, that OpenS038
opened an "authenticated Wayback capture" of the publisher PDF dated 2026-10-04 with sha256
`fc935f40…e82e8c`, and that live publisher HTML through WebFetch was corroborating and possibly cached,
"not called a live PDF fetch." This matches `build/OpenS038.md:15–20,25`: three 429 attempts; Wayback
raw capture HTTP 200, 108614 bytes, sha256 `fc935f40a6f58cb7fea9407490a768fd63078eaf46ccd3b40b260d109de82e8c`,
CDX SHA-1 match; disclosure "not a live publisher download from this network, which is rate-limited."
The scratch PDF matches that hash and size. The Gate does **not** call the cached/archived copy live.
"Authenticated" here is content-digest authentication against the archive CDX (no credentials or
login); a wording such as "digest-verified archive capture" would be less ambiguous, but the access
limitation is explicit and correct. The S066 paper caveat is at `wb.txt:244–245` under DISCUSSION
(page 1677 header at `:217`): the rendered Gate quote normalizes a hyphen/ligature line break and is
11 whitespace tokens, ≤25; location "Discussion p.1677" is correct. Adjacent only — no effect on the
S061 verdict.

## Verdict

**PARTIAL.** Every substantive S061 source claim I could check is supported: exact URL/commit, access
date, 880,776-byte source with matching sha256, task0 `eval_types == ["string_match"]`, tier A, narrow
scope, supported teaches, draft use bounded to authored specs, no old-knowledge correction owed, and a
matching independent census (812/812, 5 sets, 27 strata, 651 targets). The exactness test fails in two
independent ways: the displayed quote is not byte-present (three-line fold, dropped comma) and the
anchored "eval object:18–21" is not the eval object (`:18–29`) nor even the exact `eval_types` field
(`:19–21`); the draft header adds a third range (`task0:18–28`). These are citation-precision defects
in an admitted production row plus the Gate, not fabricated source content, so this is not FAIL. It is
not PASS because the assignment's requirement is exact quote/anchor metadata, and the C2 checker covers
only its frozen13 rows, not new ones.

Suggested L1 resolution (not applied; production is read-only here): use `eval object:18–29` or
`eval_types:19–21` in `corpus/SOURCES.md:83` and `corpus/lessons/round-28.md:40`; display `"string_match"`
at `:20` or mark the fold; align `draft:1` to `task0 eval:18–29` (or the record `:2–31`); add
`corpus/knowledge/webarena-task-spec-audit.md` to S061 used-by at admission. Any candidate byte change
requires a same-identity Q10 re-read.

Remaining unknowns: I did not verify the commit's 2025-11-26 date independently (only OpenTasks' GitHub
API observation and the round context); I did not re-run any production checker; I did not assess S062/
S063 or the rest of the candidate. The `xd://lsp` device is not mounted (`No such tool: xd://lsp`), so
no semantic definition/reference server was available for these Markdown/JSON targets; all structural
claims above are direct byte/line observations, and literal `grep -F` is reported only as a
byte-presence test, not semantic proof.

VERDICT: PARTIAL

## Addendum — v2 S068/S061 correction reread (2026-10-21; scoped final verdict)

Response to KengakuR28's IRC. Read `corpus/SOURCES.md:90` (S068), `corpus/lessons/round-28.md:169`
(M78), the corrective Gate section `corpus/lessons/round-28.md:199–217`, the S068 quote evidence
`corpus/evidence/round28-calibration/source-correction-quotes.json:11–16`, and the v2 candidate. Pinned
source bytes are unchanged (`7b50386f…02537652`, 880,776 B); I made no production edit. The v2 candidate
is `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, sha256
`3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182` (matches the IRC); canonical
`corpus/knowledge/webarena-task-spec-audit.md` is still absent.

### S068 row verified

- `corpus/SOURCES.md:90`: dataset, tier `A`, scope "this snapshot's intent and complete eval fields, not
  runtime validity"; anchor `dce04686, task0 intent16, eval object18–29, eval_types19–21,
  references22–24, program_html26; manifest byte pin`; teaches "supersedes S061's abbreviated anchor —
  eval_types is a multiline field at19–21, not the complete eval object; authored intent and predicate
  fields are explicit, separate data"; status `mined`; opened `2026-10-21`; used-by
  `corpus/lessons/round-28.md`.
- Every anchor range rechecked against the pinned bytes: task0 `"intent"` `:16`; eval block `:18–29`;
  `eval_types` field `:19–21`; `reference_answers` `:22–24`; `program_html` `:26`. All exact.
- Quote evidence parsed from `source-correction-quotes.json`: `"eval_types": [` — exactly present at
  `test.raw.json:19`, 2 whitespace tokens, declared count 2. It occurs 812 times in the file (once per
  eval-types field), so the quote is a field-opening shape, not a unique value; the `:19` locator plus
  task0 scope disambiguates it. As a correction to the multiline-field claim, it is exact.

### Remaining exactness defect: the Gate's displayed quote is escaped

`corpus/lessons/round-28.md:208` contains literal backslashes:

`| S068, corrects S061 quote/anchor | … | 2026-10-21 | `\"eval_types\": [` — single source line19;2 words. … |`

The raw file bytes are `\"eval_types\": [` (Python `repr` shows `'… `\\"eval_types\\": [` …'`). The pinned
source line 19 is `      "eval_types": [`, with no backslashes. `cmark` rendering the code span produces
`<code>\&quot;eval_types\&quot;: [</code>` — the backslashes survive inside a code span. Therefore the
Gate's rendered "exact located quote" is `\"eval_types\": [`, not the source's `"eval_types": [`. This is
a one-line transcription/escaping defect in the Gate record; the evidence JSON, the S068 row anchor and
the candidate are correct. Removing the two backslashes makes the displayed quote byte-exact.

### Supersession and v1 preservation

- S061's filed row (`corpus/SOURCES.md:83`) is unchanged; the old Gate opening row
  (`corpus/lessons/round-28.md:40`) still carries the folded quote and `18–21` anchor. M78 (`:169`) and
  the corrective Gate section (`:199–217`) explicitly supersede it, and `:216–217` states "S061's
  full-object range18–21 was not right; S068 supplies18–29." The correction is append-only, as claimed,
  and no source row is silently rewritten. The old wrong line remains discoverable; a reader must reach
  the supersession note. That matches the declared "without rewriting filed source rows" policy but is
  not an in-place correction of the old opening row.
- `S068` initially has only the lesson used-by; the v2 candidate is unadmitted, so adding
  `corpus/knowledge/webarena-task-spec-audit.md` to its used-by remains an admission-time obligation
  [INFERENCE], same as v1.
- No S068 mention exists under `corpus/knowledge/`; S068 is a source-row/anchor correction, not an
  old-knowledge erratum. No new old-knowledge correction is supported.

### v2 candidate use

- `draft:1`: `source: S061/S068 … task0 intent16 and eval18–29 (S068 corrects S061's anchor)`.
- `draft:26`: `S061/S068 are authoritative for authored specs; …`.
- No `eval_types` quote remains in the candidate; the folded excerpt is gone. The full task0 range matches
  S068. Exact.

### Scoped verdict

The v2 correction fixes v1's two substantive defects: the S068 full-range anchor is exact, the evidence
quote is exact/single-line/2 words at `:19`, and the candidate uses the exact `intent16`/`eval18–29`
range. The remaining failure is the Gate's displayed quote carrying literal backslashes, so the Gate
record's own "exact located quote" claim is not byte-true. Under the assignment's exact-metadata
standard this scoped v2 check is **PARTIAL**, not PASS; it is not FAIL because no source content,
number, range or candidate use is false and the fix is a one-line unescape. If the evidence JSON is
treated as authoritative and the Gate display as non-substantive rendering, the row would pass; I do
not take that reading because the Gate row itself labels the display "exact" and a code-span copy is
not source-literal.

The v1 section above is preserved; this addendum supersedes only the S061 quote/anchor findings it
names. Pinned bytes remain unchanged; no production edits were made.

VERDICT: PARTIAL

## Final scoped verdict — S068 transcription erratum (v3)

Bounded read of `corpus/lessons/round-28.md:238–242` only. The erratum states: "final exact located quote
is **`"eval_types": [`**, source line19 (2 whitespace-delimited words)" and "This line supersedes only
that escaped display; the S068 registry anchor and JSON evidence were right." The code span contains no
backslashes; `cmark` renders `<code>&quot;eval_types&quot;: [</code>` (rendered text `"eval_types": [`).
The pinned source line 19 is `      "eval_types": [`; the quote is an exact substring and 2 whitespace
tokens. The prior escaped display at `:208` is explicitly superseded. This fixes the only remaining
exactness defect identified in the v2 addendum.

Freeze observation: the lane file is `.ufo/waves/round-28/candidate-freeze-v2.json`, not the literal
`Freeze-v2.json` named in the IRC. It exists (968 B), pins candidate `3eb2afe5…`, supersedes
`.ufo/waves/round-28/candidate-freeze.json` (v1 retained), and records the canonical candidate as absent
plus the instrument hashes. No file literally named `Freeze-v2.json` exists under the wave directory.
If that literal filename is required, it is a naming gap; the v2 freeze artifact itself is present and
content-correct. This does not change the source quote/anchor verdict.

Pinned source bytes remain `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (880,776 B);
the v2 candidate remains `3eb2afe5ddff41f322b7131bbc658583e5a8ee8e2dc8c68b974039fdc02ff182`; canonical
`corpus/knowledge/webarena-task-spec-audit.md` remains absent. No production edits.

This is the final scoped verdict for the S068 erratum/quote/anchor/candidate-v2 use. The earlier v1 and
v2 PARTIAL verdicts remain historical records and are superseded for this scope only.

VERDICT: PASS
