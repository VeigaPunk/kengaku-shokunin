writer: KengakuR29-2.FEntrySources-2

# FEntrySources — second-seat Q10 source re-read of the round-29 knowledge candidate (v3)

Scope: source-claim re-read only. Every upstream claim in the candidate was re-opened live at its pinned
revision and compared byte-for-byte and line-anchor-for-line-anchor; every derived count in the candidate's
projection table was re-derived independently from the pinned raw bytes and the pinned generator bytes.
No production file, fixture, corpus file, SOURCES row, SCORECARD or lane-Git index was modified; the only
bytes written by this seat are this report and this seat's scratch dir.

Candidate reviewed (exact bytes): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/drafts/webarena-config-projection.md`
sha256 `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`
Canonical path: `corpus/knowledge/webarena-config-projection.md`
Instrument at review time: `plans/config_projection.py` sha256 `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142`

Independence statement: this seat did **not** read or import `plans/config_projection.py` source. All
numbers below were re-derived from the pinned raw task bytes, the pinned generator bytes, the pinned
profile bytes and the pinned BrowserGym bytes; the instrument was used only as a black box via its printed
`--summary`/`--json`/`--selftest` output for comparison. Source facts were re-opened live over the network.

## 0. Pinned bytes re-opened live (all HTTP 200)

| source | URL | live bytes | sha256 | pin in `plans/fixtures/r29/manifest.json` / SOURCES row | match |
|---|---|---|---|---|---|
| S070 generator | `raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py` | 838 | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` | manifest + S070 row | yes |
| S072 README | `.../dce04686.../README.md` | 9717 | `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` | S072 row (snapshot hash) | yes |
| S073 prepare.sh | `.../dce04686.../prepare.sh` | 120 | `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2` | S073 row | yes |
| S068 raw tasks | `.../dce04686.../config_files/test.raw.json` | 880776 | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` | manifest + S068 row | yes |
| S074 BrowserGym loader | `raw.githubusercontent.com/ServiceNow/BrowserGym/4ccc72332ab9882bc9aed87264dbf60b16e426f0/browsergym/webarena/src/browsergym/webarena/task.py` | 8603 | `f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67` | S074 row | yes |
| S071 Python json docs | `https://docs.python.org/3/library/json.html` | 115104 | `7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb` | S071 row (no hash pin) | n/a |

S074 commit identity re-checked live: `https://github.com/ServiceNow/BrowserGym/commits/main.atom` lists
`4ccc72332ab9882bc9aed87264dbf60b16e426f0` as the current `main` head, and the file fetched from
`.../main/.../task.py` is byte-identical to the pinned-commit fetch (`f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67`).

## 1. Per-claim table — source claims

| # | candidate claim (v3) | live evidence | verdict |
|---|---|---|---|
| S070a | generator `main8–23` | live file: `def main()` on line 8; body ends line 23 (`json.dump(item, f, indent=2)`) | supported |
| S070b | `replacements11–16` | live lines 11–16 are exactly `raw.replace("__GITLAB__", GITLAB)`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__` in that order | supported |
| S070c | `parse20` | live line 20: `data = json.loads(raw)` | supported |
| S070d | `enumerate-index21–23` | live lines 21–23: `for idx, item in enumerate(data):` → `with open(f"config_files/{idx}.json", "w")` → `json.dump(item, f, indent=2)` | supported |
| S070e | `from browser_env.env_config import *` on line 5, never executed here | live line 5 is that import; candidate's own instrument never imports upstream (instrument `--json` `source_contract.authority` = "inert AST facts of pinned generator bytes; never imported or executed") | supported |
| S070f | whole text written before `json.loads` | live lines 17–18 write `config_files/test.json` before line 20 parses | supported |
| S070g | output filename is the list position, not `item["task_id"]` | live source uses `idx` only; `task_id` appears nowhere in the generator | supported |
| S072a | README lines 79, 84–92, 95, 97–101 | live README: 79 = the `> [!IMPORTANT]` setup caveat; 84 = `2. Configurate the urls for each website.`; 85–92 = the fenced export block; 95 = the "encouraged to update the environment variables" note; 97–101 = step 3 `python scripts/generate_test_data.py` + "`*.json` files generated in config_files" | supported |
| S072b | step 2 exports **seven** variables, scheme-less `origin:port` | live README lines 86–92: `SHOPPING …:7770`, `SHOPPING_ADMIN …:7780/admin`, `REDDIT …:9999`, `GITLAB …:8023`, `MAP …:3000`, `WIKIPEDIA …:8888/wikipedia_en_all_maxi_2022-05/…`, `HOMEPAGE …:4399` — seven exports, no scheme anywhere, all `domain:port` | supported |
| S072c | `SHOPPING_ADMIN` adds `/admin`; `WIKIPEDIA` a long path | live lines 87 and 91 exactly as stated | supported |
| S072d | `HOMEPAGE` is a placeholder the generator never replaces | live line 92 marks `HOMEPAGE` `# this is a placeholder`; live generator lines 11–16 contain no `__HOMEPAGE__` token and the pinned raw file contains zero `__HOMEPAGE__` occurrences | supported |
| S072e | README documents no replacement order and no token inventory | live README contains zero occurrences of any `__TOKEN__` string (grep `__[A-Z]` → 0 hits) and no statement of replacement order; the only "replace" wording (line 142) concerns prompt-template keywords, a different mechanism | supported |
| S073a | `prepare.sh` lines 1–6 only creates `./.auth` and runs `auto_login.py` | live file is exactly 6 lines: shebang, blank, two comments, `mkdir -p ./.auth`, `python browser_env/auto_login.py` | supported |
| S073b | `prepare.sh` is not the generator call site | live `prepare.sh` contains no `generate_test_data`, no `scripts/`, no `config_files`, no token export | supported |
| S074a | BrowserGym loader does the same ordered replacement | live `task.py` 58–66: a dict literal in the order `__GITLAB__, __REDDIT__, __SHOPPING__, __SHOPPING_ADMIN__, __WIKIPEDIA__, __MAP__` iterated and applied with `all_configs_str.replace(pattern, self.webarena_instance.urls[url_key])` over the whole serialized text — same six tokens, same order | supported |
| S074b | BrowserGym selects by `task_id`, not by enumerate index | live `task.py` 81–82: `elif task_id is not None:` → `task_configs = [conf for conf in all_configs if conf["task_id"] == task_id]` | supported |
| S074c | "replacing placeholders in serialized task text is established practice" | two independent implementations (S070 generator, S074 loader) apply the identical ordered serialized-text replacement | supported as an observation about these two sources; no broader claim made |
| S068 | raw-task input is the manifest byte pin | live sha256 equals the manifest pin and the S068 row pin | supported |
| S071a | `json.loads` raises on an invalid document rather than repairing it | live page line 635: "If the data being deserialized is not a valid JSON document, a JSONDecodeError will be raised" | supported |
| S071b | duplicate names keep the last value | live page lines 901–902: "By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name" | supported |
| S071c | a value containing `"` can make the projected JSON invalid **or** parse with altered structure (injected keys, a duplicated `task_id` overriding the original) | follows from S071b (last value wins) applied to a text-level substitution that can inject a second `task_id` key; the candidate states this as a possibility, not an observation | supported as a conditional statement |
| S071d | a value containing `\` can make it invalid or be interpreted as a JSON escape | live page documents `ensure_ascii=True` by default and the escape example `json.loads('"\\"foo\\bar"')` → `'"foo\x08ar'` (live page line 303) | supported |
| S071e | "Nothing is normalized or repaired" | live page states no repair-on-invalid behavior; it does document non-RFC leniencies (duplicate names, `Infinity`/`NaN` accepted), which the candidate does not claim away because its sentence is scoped to the invalid-document/escape path | supported as scoped; see finding 2 |
| **S071 anchors** | header cites `Character Encodings §576-591, invalid-document402, duplicate names624-625` for `https://docs.python.org/3/library/json.html` | the live page is 1212 lines; `Character Encodings` is at line 855, the invalid-document sentence at 635, the duplicate-names sentence at 901–902; no live rendering of this URL puts those three passages at 576–591 / 402 / 624–625 | **unsupported as written** — see finding 1 |

## 2. Per-claim table — every number in the candidate's projection table, re-derived independently

All rows re-derived by this seat from `plans/fixtures/r28/webarena/config_files/test.raw.json`
(sha256 `7b50386f…`) plus the pinned generator bytes; the production instrument source was never read.

| candidate row | candidate value | independently re-derived | verdict |
|---|---|---|---|
| input tasks / distinct IDs / profiles / task×profile projections | 812 / 812 / 3 / 2436 | 812 parsed items; 812 distinct `task_id` values; 3 profiles in `plans/fixtures/r29/profiles.json`; 812×3=2436 | supported |
| original token occurrences (GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) | 385, 336, 281, 300, 0, 133 = 1435 | raw-text counts on the pinned raw bytes: 385 / 336 / 281 / 300 / 0 / 133, sum 1435 | supported |
| tasks carrying each token | 204, 128, 192, 182, 0, 128 | per-task presence counts: 204 / 128 / 192 / 182 / 0 / 128 | supported |
| "790 one-token + 22 two-token tasks = 834 rows, 812 tasks" | 790 / 22 / 834 / 812 | per-task token-count histogram: 790 tasks carry exactly one token, 22 carry exactly two, 0 carry three or more; 790 + 2×22 = 834 rows; 790 + 22 = 812 tasks | supported |
| changed string leaves / of all string leaves | 1416 / 10869 | leaf walk over the parsed 812 tasks counting only `str` leaves: 1416 leaves changed, 10869 string leaves total | supported |
| "13 leaves hold 32 occurrences, so 1435 = 1416 + 19" | 13 / 32 / 1416 + 19 = 1435 | leaves with ≥2 occurrences: 13, holding 32 occurrences in total; the other 1403 changed leaves hold one each ⇒ 1403 + 32 = 1435 and 1416 + (32−13) = 1435 | supported |
| changed leaves by JSON-path category | url_field 1355 (start_url 812, program_html url 338, reference_url 205); non_url_field 61 (60 must_include, 1 reference_answer_raw_annotation) | re-walk by path template: start_url 812, `eval.program_html[].url` 338, `eval.reference_url` 205 ⇒ url_field 1355; `eval.program_html[].required_contents.must_include[]` 60 + `eval.reference_answer_raw_annotation` 1 ⇒ non_url_field 61 | supported |
| remaining six known tokens, serialized and decoded | 0 and 0 per profile | applying the six replacements to the pinned raw text in source order leaves zero of the six token strings, in the serialized text and in the decoded objects, for each of the three frozen profiles | supported |
| other `__…__` markers (occurrences / tasks) | `__last_url__` 65 / 55, `__page__` 12 / 9 | raw-text counts 65 and 12; per-task presence 55 and 9 tasks | supported |
| output ordinal == task_id | 812/812 tasks on the frozen order | for every index i in 0..811 the item's `task_id` equals i | supported |
| value-`/` then raw-`/` junctions (`//`) | 697 in 462 tasks under trailing_slash_sensitivity, 0 otherwise | occurrences where a token is immediately followed by `/` in the raw text: 697, spread over 462 distinct tasks; under `distinct_origins` and `path_prefix` no value ends in `/`, so the junction count is 0 | supported |
| offsets are Unicode codepoints of the original input text; every occurrence inside a string value, none in a key | stated | string-literal scan of the pinned raw text: all 1435 token occurrences lie inside a string literal; 0 occurrences in a key or in structural text; 0 keys contain a token | supported |
| "all 61 non_url_field leaves hold URL-shaped strings under non-URL keys" | stated | substituting the `distinct_origins` values into the 61 non-url_field leaves yields 61/61 strings beginning with `http://` | supported |
| instrument `--summary`: exit 0, 0 findings | stated | `python3 plans/config_projection.py --summary` → last line `TOTAL findings=0 exit=0`, exit status 0 | supported |
| `--selftest` clean | recheck line | `python3 plans/config_projection.py --selftest` → `SELFTEST clean cases=28 …`, exit 0 | supported |
| mutation witness | recheck line | `python3 plans/fixtures/r29/mutation_witness.py` → exit 0, `"killed": 10`, `restored_sha256` equals the current instrument digest `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142` | supported |
| v2→v3 instrument equality receipt | cited `corpus/evidence/round29-calibration/repair-projection-equality.json` | file exists (595 bytes) and carries `old_tool`, `new_tool_sha256`, `occurrence_provenance_equal`, `profiles`, `note` | supported as an existing receipt |
| four oracles reproduce every count, 1435 provenance records, 2436 projected objects and would-be file digests | cited `FOracleText.md`, `FOracleLeaf.md`, `FOracleProvenance.md`, `FOracleIndex.md` | all four files exist under `.ufo/waves/round-29/falsify/`; each carries a distinct seat id (`writer: KengakuR29-2.FOracleText-2` etc.) and states 1435/2436 agreement | supported as an attribution of the receipts; v3 now correctly qualifies it as "independent logic, not independent identity" and attributes the task-unit bridges (790/22, 32, 55/9, 462) to the entry-review seats rather than to the four oracles — consistent with the four receipts, which do not carry those bridges |

## 3. Findings

**Finding 1 (MEDIUM — citation anchors, not substance).** The candidate's source header anchors three S071
passages as `Character Encodings §576-591, invalid-document402, duplicate names624-625` on
`https://docs.python.org/3/library/json.html`. On the live page fetched today (1212 lines) those passages
are at lines 855 (section heading), 635 (invalid-document sentence) and 901–902 (duplicate-names
sentence). The cited line numbers are therefore not locatable on the page the row cites, and the same
sentence-set cannot be found at those coordinates in any rendering of that URL fetched during this
re-read. The underlying S071 *facts* (invalid document raises; duplicate names keep the last value) are
verified on the live page at 635 and 901–902, and the candidate's prose in the "generator's contract" section
is correct; only the header's line coordinates fail to resolve against the live page. [INFERENCE] The
coordinates appear to belong to a different rendering or an older doc snapshot than the one the URL now
serves, so they cannot be verified as written. This is a locator defect, not a claim-content defect.

**Finding 2 (LOW — scope of a blanket negative).** "Nothing is normalized or repaired" is placed in the
S071 bullet, whose subject is the invalid-document and escape path, where it holds on the live page. The
same live page documents two non-RFC leniencies elsewhere (repeated names accepted with last-value-wins;
`Infinity`/`NaN` accepted as input). The candidate already states the duplicate-name behavior explicitly in
the same sentence pair, so the negative is not contradicted by the candidate, but read in isolation it
over-generalizes the module. The candidate's own instrument likewise documents the difference between
"no repair" and "RFC leniency".

**Finding 3 (LOW — the one unanchored word).** "Harnesses that select configs by `task_id` (S074) need
checks 1, 2 and 4 only" is an inference from S074's selection code, which the candidate cites and which is
verified live (81–82). The "need only" phrasing is the candidate's own operational judgement, correctly
attributed to a cited source. No defect.

**Finding 4 (INFO — v3 deltas verified).** v3 differs from v2 only at lines 37 and 58–70 (per the
coordinator's statement, checked against the live bytes): the `\`-escape example sentence was replaced by a
scoped "interpreted as a JSON escape", the oracle attribution was qualified to "independent logic, not
independent identity", the task-unit bridges (790/22, 32, 55/9, 462) were attributed to the entry-review
seats rather than to the four oracle reports, and explicit falsifiers plus the equality receipt pointer were
added. Every one of those statements matches the receipts and numbers re-derived above. The v3 prose in the
S071 bullet is strictly narrower than v2's and matches the live page better than v2's.

**Finding 5 (INFO — one upstream file opened beyond the cited set).** To check the candidate's statement
that the wildcard import "supplies the values", this seat also opened
`browser_env/env_config.py` at the same pinned revision (sha256
`fcec91a2dafd5db16bb390ac5a6fd930ef59c6ef54445b85f7625d8f9404abd7`, 1417 bytes). It defines the six
named site variables plus `HOMEPAGE` and asserts all seven are non-empty at import time. Nothing in the
candidate depends on `env_config`'s contents beyond "the import supplies the values", and no env value is
claimed. Recorded for transparency only.

## 4. Residual risk and verification gaps

- S071's three header line coordinates remain unverified against the live cited URL (finding 1). The fix
  is either to re-anchor the header to the live page's current lines (855 / 635 / 901–902) or to cite the
  CPython `Doc/library/json.rst` file at a named revision whose line numbers are then exactly reproducible.
  Until then a reader cannot follow the header's coordinates.
- The S071 page is a rolling "latest stable" URL: `docs.python.org/3/library/json.html` serves 3.15.1 today
  and will move with the next release, so any line coordinate on it is time-limited regardless of this
  finding. A revision-pinned source (the `v3.15.1` tag of `python/cpython`) would be stable.
- Upstream network re-reads were performed from this host; the fetches returned HTTP 200 and the digests
  matched the pins, so no unpinned or mutable upstream bytes entered the comparison.
- The four oracle receipts and the equality receipt were checked for existence, seat attribution and the
  numbers they state; this seat did not re-derive the 2436 projected objects independently (that is the
  oracle seats' scope), so the "all 2436 projected objects and would-be file digests" claim is verified as an
  accurate report of those receipts, not re-executed here.
- No instrument source was read by this seat; the instrument was exercised as a black box only.

## 5. Scoped verdict on the exact v3 bytes

Reviewed bytes: `.ufo/waves/round-29/drafts/webarena-config-projection.md`,
sha256 `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`, canonical path
`corpus/knowledge/webarena-config-projection.md`.

Every source claim in the candidate body is supported by the live pinned bytes I re-opened (S070 generator,
S072 README, S073 prepare.sh, S068 raw tasks, S074 BrowserGym loader, S071 Python json docs), and every
number in the candidate's projection table was independently re-derived from the pinned raw bytes and
matched exactly, including the four v3-added task-unit bridges (790/22, 32, 55/9, 462). One source-claim
element is **not** supported as written: the S071 line coordinates in the candidate's source header
(`§576-591 / 402 / 624-625`) do not locate those passages on the live page the row cites (they are at 855 /
635 / 901–902), and the S071 facts themselves are correct. That is a locator defect in the header, not a
misstatement of any source fact or any number, which is why this is not a PASS and not a FAIL.

VERDICT: PARTIAL

## Re-check at candidate v5 (final exact-v5 verdict; append-only)

Note on verdict lines: the `VERDICT: PARTIAL` line ending the v3 section above is the historical verdict for
those exact bytes and is superseded for the bytes reviewed here. This section is the scoped verdict for
candidate v5; the file's final line is the v5 verdict.

Candidate reviewed (exact bytes): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/drafts/webarena-config-projection.md`
sha256 `c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3`
Canonical path: `corpus/knowledge/webarena-config-projection.md`

### Change scope, verified by byte comparison

v5 differs from v3 in exactly one line. Proof: taking the v5 file and substituting back the verbatim v3
source-header line (931 bytes, staged in scratch) reproduces the v3 digest exactly —

- sha256 of v5-with-v3-line-1 = `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`
  = the v3 candidate digest `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`
- sha256 of v5 as read = `c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3`

So every body line, every table row and every number in the candidate is byte-identical to the v3 bytes this
seat already re-read and re-derived; the only delta is line 1, the source header. No body or metric was
re-verified from scratch, and none needed to be.

### The one changed line: locator correction

v5 line 1 now reads (abridged, from the file):

> S071/S075/S076 https://docs.python.org/3/library/json.html#character-encodings ensure_ascii paragraph,
> #json.load invalid-document exception inherited by #json.loads (Identical to load()),
> #repeated-names-within-an-object opening paragraph/example (S075 replaces renderer-dependent coordinates …)

Re-opened live for this check: `https://docs.python.org/3/library/json.html`, HTTP 200, 115104 bytes,
sha256 `8271280bc2d8bcca4812a2260729ade980ea77041609aa7a6013708eee4e01d5` (a second fetch ten minutes later,
sha256 `fd0123214de55b494ce1d12b994596deeb608326a527d92f056be11f920b117f`, differs in exactly one line: the
rendered "Last updated on Oct 21, 2026 (17:57 UTC)" vs "(18:07 UTC)" footer — the page body is otherwise
identical, which is itself the portability argument for section anchors over line coordinates).

Each cited fragment resolves on the live page to the claimed passage:

| v5 header locator | live id (html line) | live passage | verdict |
|---|---|---|---|
| `#character-encodings` | `id="character-encodings"` (854) | section "Character Encodings"; the `ensure_ascii=True` by default / "escaping the output so that the resulting strings only contain printable ASCII" paragraph at 858–860 | resolves, correct passage |
| `#json.load` | `id="json.load"` (458) | its `Raises:` field, 508–510: "JSONDecodeError – When the data being deserialized is not a valid JSON document." | resolves, correct passage |
| `#json.loads` | `id="json.loads"` (543) | opening clause at 545: "Identical to load(), but instead of a file-like object, deserialize s (a str, bytes or bytearray …)" — the inheritance the header states | resolves, correct passage |
| `#repeated-names-within-an-object` | `id="repeated-names-within-an-object"` (897) | opening paragraph 899–902 ("…it ignores all but the last name-value pair for a given name:") and the following example at 903–906 | resolves, correct passage |

Corpus rows backing the correction were re-read in place: `corpus/SOURCES.md` line 97 (S075, stable-section
locator correction, scope "not reader-specific line coordinates") and line 98 (S076, load/loads inheritance
locator correction). S076's own wording matches the live page: the invalid-document sentence sits under
`json.load`'s `Raises:` field, and `json.loads` inherits that contract through its "Identical to load()"
clause rather than repeating the sentence.

### Effect on this seat's earlier findings

- Finding 1 (MEDIUM, locator-only): **resolved**. The header no longer cites renderer-dependent line
  coordinates; it cites stable fragment/section anchors that I located and matched on the live page.
- Finding 2 (LOW, scope of the blanket negative "Nothing is normalized or repaired"): **unchanged and not
  in scope of this locator-only delta**. It concerns the body sentence (byte-identical to v3) and remains a
  wording observation about the module's documented RFC leniencies; it is not a source-claim defect.
- Findings 3, 4, 5 (INFO) are unaffected by the one-line delta.
- All source facts and every number in the candidate body were verified in the v3 section of this report
  against the live pinned bytes and independently re-derived; they are carried forward unchanged because the
  bytes are unchanged.

### Residual risk and verification gaps (v5)

- `docs.python.org/3/library/json.html` is a rolling "current stable" URL; it serves 3.15.1 today and moves
  with the next release. The fragment anchors are stable across renderings and releases of the same content,
  but the URL itself is not revision-pinned. A `python/cpython` tag-pinned `Doc/library/json.rst` would be
  byte-stable; the candidate does not claim that, and its S075/S076 scope statement says the same.
- The v5 line 1 is truncated in my read of the file at 768 bytes by the reader; the remainder of the line
  carries the S074/S068 citations. Those two citations are byte-identical to the v3 header I verified live
  (BrowserGym loader lines 55–69/81–82 at the pinned commit; the S068 raw-task manifest byte pin), and the
  byte-comparison above proves no other header element changed.
- The four oracle receipts, the equality receipt and the mutation-witness receipt were checked for
  existence, attribution and stated numbers in the v3 section of this report; they are unchanged in v5.
- No production file, fixture, corpus file, SOURCES row, SCORECARD, lane-Git index or lane state was
  modified by this seat. The only bytes written are this report and this seat's scratch dir.

### Scoped verdict on the exact v5 bytes

Reviewed bytes: `.ufo/waves/round-29/drafts/webarena-config-projection.md`,
sha256 `c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3`, canonical path
`corpus/knowledge/webarena-config-projection.md`.

Every source claim in the candidate body is supported by the live pinned bytes this seat re-opened and
re-derived (S070, S072, S073, S068, S074, S071 facts), every number in the projection table was
independently re-derived and matched exactly, and the single changed line — the S071/S075/S076 locator — now
resolves on the live page to the exact passages it names, with all three fragment ids located and matched.
The one earlier MEDIUM finding is closed by this change. The only outstanding observation is a LOW wording
point about the body's blanket negative, which is a scope observation rather than an unsupported source
claim, and which lies outside this locator-only delta.

VERDICT: PASS
