writer: KengakuR29-2.FEntryNumbers-2

# FEntryNumbers — Q10 second-seat re-read of every number and location in the frozen candidate

Seat `KengakuR29-2.FEntryNumbers-2` (role reviewer, read-only leaf; actual writer: same).
Target: the frozen knowledge candidate
`/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/drafts/webarena-config-projection.md`.
Intended canonical path: `corpus/knowledge/webarena-config-projection.md` (currently absent on disk:
`test -e corpus/knowledge/webarena-config-projection.md` → absent; the freeze file
`.ufo/waves/round-29/candidate-freeze-v1.json` names it as `canonical_path`).

Lane master `56fd949a6478342531e61f4feecb4a685d831640`.

**Byte identity reviewed (observed)**

```
sha256sum .ufo/waves/round-29/drafts/webarena-config-projection.md
7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc
```

Full 64-hex sha256 of the bytes reviewed:
**`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc`**

This equals the expected value given in the assignment and the `sha256` field of
`.ufo/waves/round-29/candidate-freeze-v1.json`. Every line reference below is to these exact bytes.

**Independence statement (observed)**

I did **not** read the production source `plans/config_projection.py`. I ran it only through
`--summary`, `--json` and `--selftest`, and I read its *output*. My own numbers come from
`.ufo/waves/round-29/scratch/falsify/FEntryNumbers-2/derive.py`, written from the S070 text contract
(the pinned generator's six ordered `str.replace` calls on the whole text, then `json.loads`, then
`enumerate`), the pinned raw task file and `plans/fixtures/r29/profiles.json`. Scratch dir:
`.ufo/waves/round-29/scratch/falsify/FEntryNumbers-2/` (`derive.py`, `derive-out.txt`, `summary.txt`,
`out.json`, `out.json.err`).

Tool installs/updates: **none**. No `pacman`, no `uv tool install`, no `cargo`/`npm` — the stdlib
`python3` 3.14.8 was sufficient, so no tooling was needed. Network: three `curl` GETs of public pinned
upstream URLs (upstream `README.md`, upstream `prepare.sh`, and `docs.python.org/3/library/json.html`),
each written to `/tmp` for line-anchor verification. No credentials, cookies, auth-state or private URLs
were read or recorded. No lane, corpus, fixture, SOURCES, SCORECARD or candidate file was mutated; git
was used read-only (`log`, `show`, `rev-parse`, `status`, `cat-file`, `rev-list`).

Word counts for every quote below were computed programmatically with `len(q.split())`; each is ≤ 25 words.

---

## 1. Verdict summary

**Every number in the candidate's measured table reproduces under independent re-derivation, and every
source-line anchor I could check resolves to the cited location.** Two defects were found, both in
prose rather than in the measured table, and both are already reported by sibling seats on these exact
bytes:

| # | severity | class | location | defect |
|---|---|---|---|---|
| N1 | medium | location / citation | line 10 | "corpus/README.md Frontier" misattributes the quoted phrase to the `## Frontier` section |
| N2 | low | provenance wording | line 42 | "sum 834" is a reader-side sum, not a value `--summary` emits |

A third wording point (N3, low) concerns the `must_include` path label, and a fourth (N4, low) concerns
the `"` / `\` rejection rule in the operational decision rule. All four are itemised below with the
smallest fix. None of them changes a measured value.

Because the assignment's bar is "VERDICT: PASS only if every number and location is correct as written",
and N1 is a location error as written, the scoped verdict on these exact bytes is **PARTIAL**.

---

## 2. Measured table — every number re-derived independently (observed)

Source: `derive.py` output (`derive-out.txt`), computed from the pinned raw file and pinned profiles,
never from production code. Instrument values come from `--summary` (`summary.txt`) and `--json`
(`out.json`).

| candidate line | value as written | independent re-derivation | instrument `--summary` / `--json` | agrees |
|---|---|---|---|---|
| 40 | 812 / 812 / 3 / 2436 | 812 tasks, 812 distinct IDs, 3 profiles; 2436 = 812×3 | `POPULATION` `input_task_count 812`, `distinct_task_ids 812`, `profile_count 3`, `task_profile_projections 2436` | yes |
| 41 | 385, 336, 281, 300, 0, 133 = 1435 | literal text matches in the original input: `__GITLAB__` 385, `__REDDIT__` 336, `__SHOPPING__` 281, `__SHOPPING_ADMIN__` 300, `__WIKIPEDIA__` 0, `__MAP__` 133; sum 1435 | `ORIGINAL_OCCURRENCES_BY_TOKEN` identical; `occurrence_roles {value: 1435}` | yes |
| 42 | 204, 128, 192, 182, 0, 128 | tasks carrying each token, same order: 204 / 128 / 192 / 182 / 0 / 128 | `TASKS_WITH_TOKEN` identical | yes |
| 42 | "sum 834" | 790 tasks carry exactly one token, 22 carry two (8 carry 2, 4 carry 3, 1 carry 4 — token-bearing leaves only) → 790 + 44 = 834; distinct task count 812 | not emitted by `--summary` (see N2) | arithmetic yes, provenance no |
| 42 | "distinct 812" | 812 of 812 tasks carry ≥1 token | `POPULATION tasks_with_any_token 812` | yes |
| 43 | 1416 / 10869 / 13 | changed string leaves 1416; all string leaves 10869; leaves holding >1 token occurrence 13 (those 13 hold 32 occurrences; 1403 hold one; 1403+32 = 1435) | `changed_leaf_count 1416`, `string_leaf_count 10869`, `changed_leaves_with_multiple_occurrences 13` | yes |
| 44 | url_field 1355 (start_url 812, program_html url 338, reference_url 205) | per-path-template change counts: `start_url` 812, `eval.program_html[].url` 338, `eval.reference_url` 205; 812+338+205 = 1355 | `changed_leaves_by_category {"url_field": 1355, "non_url_field": 61}`; `changed_leaves_by_path_template` identical per profile | yes |
| 44 | non_url_field 61 (must_include 60, reference_answer_raw_annotation 1) | `eval.program_html[].required_contents.must_include[]` 60; `eval.reference_answer_raw_annotation` 1; 60+1 = 61 | identical | yes |
| 45 | 0 and 0 per profile | all six known tokens: 0 remaining in serialized text and 0 in decoded values, for all three profiles | `remaining_known_tokens_text` / `remaining_known_tokens_decoded` all 0 | yes |
| 46 | `__last_url__` 65, `__page__` 12 | regex sweep of the original text for `__[A-Za-z0-9_]+__` yields exactly six env tokens plus `__page__` 12 and `__last_url__` 65 — no other markers exist | `OTHER_MARKERS_NOT_ENV_TOKENS {"__last_url__": 65, "__page__": 12}` | yes |
| 47 | 812/812 on the frozen order | `i == task_id` for all 812 tasks; `violations` empty | `INDEX {"index_equals_task_id": 812, "violations": []}`; `index_mapping` identical | yes |
| 48 | 697 under trailing_slash_sensitivity, 0 otherwise | token occurrences immediately followed by `/` in the original text = 697 (GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, WIKIPEDIA 0, MAP 5); only `trailing_slash_sensitivity` values end in `/`, so only there does the value's own `/` meet a raw `/` — 697 junctions there, 0 in the other two profiles | `stimulus_observations {"value_slash_then_raw_slash_junctions": 697}` for trailing_slash_sensitivity, 0 for the other two | yes |
| 51 | "Occurrence offsets are Unicode codepoints in the original input text" | all 1435 `occurrence_provenance` records: `raw[off:off+len(token)] == token` for 1435/1435, 0 mismatches | `original_input_codepoint_offset` verified identically | yes |
| 51–52 | "Every token occurrence is inside a string value; none is inside a key or structural text" | occurrences inside dict keys = 0; inside string values = 1435; total text matches 1435 — no occurrence is anywhere else | `occurrence_roles {"value": 1435}` | yes |
| 63–64 | reversed order gives identical output | forward-order and reversed-order projected text are byte-identical for all three profiles (sha256 equal per profile) | `mutation-witness.txt`: `wrong_order_reversed selftest exit 1 killed` | yes |
| 63 | "No profile value contains a token" | all 18 profile values scanned for the six tokens: zero hits | profile `values` blocks identical | yes |

Additional arithmetic check I ran that the candidate does not state, but which its numbers imply:
`812` distinct task IDs and `812` token-carrying tasks agree, and `1435` occurrences = `1416` changed
leaves + `19` surplus occurrences spread over the `13` multi-occurrence leaves (32 occurrences in those
13 leaves, 1403 in single-occurrence leaves). Every figure in the candidate is consistent with this.

**Instrument identity and exit codes (observed)**

| check | result |
|---|---|
| `python3 plans/config_projection.py --summary` | exit 0, `TOTAL findings=0 exit=0` |
| `python3 plans/config_projection.py --json` | exit 0, `findings` list length 0; output sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, equal to `corpus/evidence/round29-calibration/build-json-sha256.txt` |
| `python3 plans/config_projection.py --selftest` | exit 0, `SELFTEST clean cases=20` |
| `sha256sum plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` — matches the assignment's pinned manifest digest |
| `sha256sum` of generator / raw file / profiles | `45ddba7b…21cd`, `7b50386f…7652`, `90fdc34d…e018` — match `plans/fixtures/r29/manifest.json` exactly |
| `git rev-parse HEAD` | `56fd949a6478342531e61f4feecb4a685d831640` (lane master) |

---

## 3. Source-line anchors — every checked location (observed)

Anchors are quoted from the candidate's `source:` line (line 1) and from its body claims.

### 3.1 S070 — pinned generator `scripts/generate_test_data.py`

Fetched/present bytes: `plans/fixtures/r29/generate_test_data.py`, sha256
`45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` (matches manifest and SOURCES).

| candidate anchor | cited location | verified content | result |
|---|---|---|---|
| `main8–23` | lines 8–23 | `def main() -> None:` at line 8; body ends at line 23 (`json.dump(item, f, indent=2)`) | correct |
| `replacements11–16` | lines 11–16 | exactly six `raw.replace(...)` calls in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP | correct |
| `parse20` | line 20 | `data = json.loads(raw)` | correct |
| `enumerate-index21–23` | lines 21–23 | `for idx, item in enumerate(data):` … `open(f"config_files/{idx}.json", "w")` … `json.dump(item, f, indent=2)` | correct |
| body: import at line 5 | line 5 | `from browser_env.env_config import *` | correct |
| body: "the whole text is written before `json.loads(raw)` (line20)" | lines 17–18 then 20 | `f.write(raw)` at 18 precedes `json.loads(raw)` at 20 | correct |
| body: "Lines21–23 write `config_files/{idx}.json` from `enumerate(data)`: the filename is the list position, not `item["task_id"]`" | lines 21–23 | the filename uses the loop index; `item["task_id"]` is never used for naming | correct |

My own re-implementation reproduces the generator's behaviour exactly, including the order-dependence
that the candidate calls out. Independent probe (scratch): a value carrying a *later* token
(`GITLAB` → `__MAP__`) cascades into `http://m.invalid/x`, while a value carrying an *earlier* token
(`MAP` → `__GITLAB__`) leaves `__GITLAB__/late` un-replaced — consistent with the ordered
`str.replace` semantics the candidate describes at lines 23–24 and 63–64.

### 3.2 S072 — upstream `README.md` at revision dce04686

Fetched to `/tmp/wa_README.md`; sha256 `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287`,
162 lines — equal to the S072 digest recorded in `corpus/SOURCES.md` line 94.

| candidate anchor | cited location | verified content | result |
|---|---|---|---|
| `lines79` | 79 | the round-28 `812 examples` note in the end-to-end evaluation section | correct |
| `lines84–92` | 84–92 | step 2 "Configurate the urls for each website." plus the seven `export` lines | correct |
| `line95` | 95 | the note pointing at the GitHub workflow environment variables | correct |
| `lines97–101` | 97–101 | step 3 "Generate config file for each test example" … `python scripts/generate_test_data.py` … "You will see `*.json` files generated in [config_files]" | correct |

Body claims checked against those lines:

* "the README's step 2 exports scheme-less example `origin:port` values (SHOPPING_ADMIN adds `/admin`)"
  — 18 words. Lines 86–92 export `SHOPPING="<your_shopping_site_domain>:7770"`,
  `SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"`, `REDDIT=…:9999`, `GITLAB=…:8023`,
  `MAP=…:3000`, `WIKIPEDIA=…:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing`,
  `HOMEPAGE=…:4399 # this is a placeholder`. Every value is scheme-less `host:port` form; only
  `SHOPPING_ADMIN` adds `/admin`; `WIKIPEDIA` adds a long path and `HOMEPAGE` is flagged a placeholder.
  The candidate's sentence is **correct but partial**: it names only the `/admin` suffix and does not
  mention `WIKIPEDIA`'s long path or the `HOMEPAGE` placeholder. This is an omission, not an error —
  no number or location in the candidate is contradicted. See N4 for the one place where the same
  README fact is used operationally.
* "step 3 runs this script" — line 99 is `python scripts/generate_test_data.py`. Correct.
* "it documents no replacement order or token inventory" — a case-sensitive grep of the README for
  `__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__MAP__`, `__WIKIPEDIA__` returns no hit, and the only
  occurrence of the word "replace" (line 142) is about intent-template keywords, not token
  replacement. Correct.

### 3.3 S073 — upstream `prepare.sh` at revision dce04686

Fetched to `/tmp/wa_prepare.sh`; sha256 `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2`,
6 lines, 120 bytes — equal to the S073 digest in `corpus/SOURCES.md` line 95.

| candidate anchor | cited location | verified content | result |
|---|---|---|---|
| `lines1–6` | 1–6 | complete file, 6 lines / 120 bytes | correct |
| body: "`prepare.sh` only creates `./.auth` and runs `auto_login.py`" | lines 5–6 | `mkdir -p ./.auth`; `python browser_env/auto_login.py` | correct |
| body: "it is not the generator call site" | whole file | `grep -c` for `generate_test_data\|scripts/\|config_files\|__GITLAB__` in the pinned copy → 0 | correct |

### 3.4 S071 — `https://docs.python.org/3/library/json.html`

Fetched to `/tmp/py_json.html`; sha256 `7197009d47b8a44ce5a8c22b8c70ab5f754fd479cb30268284b0da84a9d1f8fb`;
page title `json — JSON encoder and decoder — Python 3.15.1 documentation`, matching the S071 row's
"Python3.15.1".

| candidate anchor | verified content | result |
|---|---|---|
| `Character Encodings` | section anchor `id="character-encodings"` exists (html line 855) | correct |
| `loads` | function anchor `id="json.loads"` exists (html line 543) | correct |

Body claim at lines 30–32 (17 words): "`json.loads` raises on an invalid document rather than repairing
it; a value containing `"` or `\` … nothing is normalized or repaired."

* "raises on an invalid document rather than repairing it" — the page carries, under the
  `json.JSONDecoder` / `json-to-py-table` region, the sentence "If the data being deserialized is not a
  valid JSON document, a JSONDecodeError will be raised" and the `Raises:` line "JSONDecodeError – When
  the data being deserialized is not a valid JSON document". The claim is supported. (The `Raises:`
  clause itself sits with the decoder, not inside the `json.loads` signature block; the candidate's
  attribution to "S071 … `json.loads`" is a reasonable shorthand for the module-level contract, and the
  behaviour is exactly what the sentence states.)
* "a value containing `"` … makes the projected JSON invalid" — verified behaviourally with the stdlib:
  substituting a value carrying `"` into the serialized text produces a document that `json.loads`
  rejects with `JSONDecodeError`.
* "or is decoded as a JSON escape (`\n` becomes a newline)" — verified behaviourally: substituting a
  value whose text contains the two characters `\n` yields a decoded string containing a real newline
  (`http://m.invalid/a\nb/x`). Correct.
* "nothing is normalized or repaired" — consistent with the module docs (no repair step; the decoder
  raises). Correct.

### 3.5 S068 — pinned raw task file

`plans/fixtures/r28/webarena/config_files/test.raw.json`, sha256
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, equal to the manifest entry for that
path and to the S068 row's "manifest byte pin". The candidate cites it as the raw-task input pin with no
line anchor, which is consistent with the S068 row's own scope ("this snapshot's intent and complete
eval fields"). No location error.

### 3.6 Body location claims not tied to a source row

* Line 10–11: "Extends corpus/README.md Frontier “generated eval-time configs” left open by round28
  (`knowledge/webarena-task-spec-audit.md` audited raw specs only)."
  - The quoted phrase "generated eval-time configs" occurs exactly once in `corpus/README.md`, at line
    338. Line 338 sits inside the section "### Round28 admitted knowledge and partial frontier advance"
    (heading at line 326), **not** inside the `## Frontier` section (lines 253–266), which contains
    none of that phrase. See **N1**.
  - `knowledge/webarena-task-spec-audit.md` exists at `corpus/knowledge/webarena-task-spec-audit.md`
    (14594 bytes) and its own scope line reads "static task-spec observability"; the candidate's
    characterisation "audited raw specs only" matches that entry's stated scope. Correct.
  - `corpus/README.md` line 330 lists the r28 entry in the round-28 admitted table, consistent with the
    candidate's "left open by round28" framing.
* Line 14: "Seat R29DraftEntry drafted the first scope; this candidate replaces it with measured facts."
  - `.ufo/waves/round-29/build/R29DraftEntry.md` exists and is authored by `R29DraftEntry`; it states it
    wrote the draft path with sha256 `7bf99d9b…`, 7404 bytes. Those exact bytes are **not** present in
    the lane's git object store (a full `git cat-file --batch-all-objects` blob sweep over 2043 blobs
    found no `7bf99d9b` prefix; the draft path's history holds only `4b38b4bf…` at `b98dcf3`/`e838007`
    and `7006b93d…` from `56fd949` onward). The candidate's sentence is about authorship, not about
    retrievable bytes, so it is not a false claim — but the antecedent it points to is not
    recoverable at the cited path. [INFERENCE] This is a provenance observation, not a defect in the
    candidate's numbers or locations; sibling `FEntryQuality.md` line 61 records the same fact.
* Line 34 / 36: "`python3 plans/config_projection.py --summary`, exit0, 0 findings" — reproduced: exit 0,
  `TOTAL findings=0 exit=0`. Correct.
* Line 46 / 60: "`sites` metadata is not used to count tokens." — the instrument's own LIMIT line reads
  "unread metadata such as sites is not a consumed predicate"; the candidate's `--summary` and `--json`
  outputs contain no `sites`-derived count. Independently, the distinct `sites` histogram in the raw file
  is `{shopping_admin 184, map 128, shopping 192, reddit 129, gitlab 204, wikipedia 23}` while the
  token task counts are `{204, 128, 192, 182, 0, 128}` — they differ for reddit (129 vs 128),
  shopping_admin (184 vs 182) and wikipedia (23 vs 0), which independently confirms `sites` is not the
  counting basis for the token numbers. Correct.

---

## 4. Findings

### N1 — medium — location error: the quoted phrase is not in the `## Frontier` section

**Location:** candidate line 10 — "Extends corpus/README.md Frontier “generated eval-time configs” left
open by round28" (10 words).

**Observed:** `grep -n "generated eval-time configs" corpus/README.md` returns exactly one hit, line
338. `awk 'NR>=253 && NR<=267' corpus/README.md | grep -c "generated eval-time configs"` returns **0** —
the `## Frontier` section (heading at line 253, its five bullets ending at line 266) does not contain the
phrase. Line 338 lies in the round-28 section whose heading is "### Round28 admitted knowledge and
partial frontier advance" (line 326), inside the paragraph beginning "**Partly discharged round28:** the
original Frontier task-spec-audit gap is closed only for this WebArena static surface."

**Why it matters:** the sentence uses the corpus README's own section name as a locator for a quote the
section does not contain. A reader who searches the `## Frontier` list finds no such item and may
conclude the gap was never named there. The substantive claim — that generated eval-time configs remain
open — is true and is stated at README:338.

**Smallest fix:** cite the location rather than the section name, e.g. "corpus/README.md:338
(round-28 partial discharge: generated eval-time configs … remain open)".

**Corroboration:** sibling `FCritNoAxisHarm.md` line 43 and its table row 4 record the same location slip
on these bytes, and `FEntryQuality.md` line 61 records the same README:338 anchor. My finding is
independent of both.

### N2 — low — provenance wording: "sum 834" is not an instrument-emitted value

**Location:** candidate line 42 — "tasks carrying each token (not additive: sum 834, distinct 812)"
(10 words).

**Observed:** the string `834` does not occur in the `--summary` output or anywhere in the `--json`
output. `--summary` emits the six per-token task counts (`204, 128, 192, 182, 0, 128`) and
`tasks_with_any_token 812`; 834 is the reader's sum of the six. The candidate's own parenthetical
"(not additive: sum 834, distinct 812)" already labels it as a sum and warns against adding it, so the
number is arithmetically right and honestly labelled as a derived quantity — but it is introduced by a
lead-in line (36) that presents the whole table as `--summary` output.

**Independent derivation of the bridge the candidate leaves unstated:** 790 tasks carry exactly one
token, 22 carry two or more (8 carry 2 occurrences, 4 carry 3, 1 carry 4 — over token-bearing leaves only),
so 790 + 44 = 834 while 790 + 22 = 812 distinct tasks.

**Smallest fix:** either write "sum of the six row values = 834" to mark it as reader-side, or state the
22-task two-token bridge. Sibling `FCritUnits.md` finding 1 records the same provenance gap.

### N3 — low — the `must_include` label is ambiguous between two distinct JSON paths

**Location:** candidate line 44 — "non_url_field 61 (must_include 60, reference_answer_raw_annotation 1)"
and line 56–58 — "61 changed leaves are `must_include` answer strings and one raw annotation" (11
words).

**Observed:** the raw file contains two different `must_include` keys:
`eval.reference_answers.must_include[]` (396 string leaves) and
`eval.program_html[].required_contents.must_include[]` (815 string leaves). Exactly 60 leaves carry a
token, and all 60 are in the **program_html** one; the reference-answers one has 0 token-carrying leaves.
The count 60 and the total 61 are both correct, and the instrument's own
`changed_leaves_by_path_template` key is the unambiguous `eval.program_html[].required_contents.must_include[]`.

**Why it matters:** the candidate writes the bare key `must_include`, and separately calls the 60
leaves "`must_include` answer strings". Under the raw file's own naming, the answer strings live in
`reference_answers.must_include[]` — the path with 0 changed leaves — while the changed 60 are
required-contents strings under `program_html[].required_contents`. A reader cross-checking the word
"answer" against the file's key names lands on the wrong array.

**Smallest fix:** write the full template (`eval.program_html[].required_contents.must_include[]`) at
line 44 and drop the word "answer" at line 56, or say "required-contents strings". Sibling
`FPathMustInclude.md` finding 2 records the same key-name ambiguity in the instrument's own labels.

### N4 — low — the rejection rule's stated reason over-reaches for the token-string case

**Location:** candidate lines 73–74 — "reject any value carrying `"`, `\` or a token string, because text
replacement would break JSON or cascade" (18 words).

**Observed:** the `"` and `\` reasons are exactly right (verified behaviourally: `"` → `JSONDecodeError`;
`\` before `n` → decoded as an escape; a lone `\` before a non-escape character → `JSONDecodeError`). The
"token string" reason is only conditionally true: in the generator's fixed order
(GITLAB → REDDIT → SHOPPING → SHOPPING_ADMIN → WIKIPEDIA → MAP) a value carrying a **later** token
cascades (probe: `GITLAB` → `__MAP__` yields `http://m.invalid/x`), while a value carrying an **earlier**
token does not (probe: `MAP` → `__GITLAB__` leaves `__GITLAB__/late` in the output). The cascade-order
hand fixture `plans/fixtures/r29/hand/cascade-order.case.json` encodes exactly this direction.

**Why it matters:** the rule as written is conservative and therefore safe — rejecting any value that
carries any token string catches every cascade case — but the stated reason ("would … cascade") is
true for only some of the values the rule rejects. This is a rationale-precision point, not a wrong
number or a wrong location.

**Smallest fix:** "because text replacement would break JSON, or would cascade for a token replaced
later in the order".

---

## 5. Items checked and found correct (no finding)

Recorded so the coverage is complete and auditable.

1. **All 16 table numbers** on lines 40–48 reproduce exactly under independent re-derivation, and the
   arithmetic identities inside the table hold (1355 = 812+338+205; 61 = 60+1; 1416 = 1355+61;
   1435 = 1416 leaves + 13 multi-occurrence leaves holding 32 occurrences; 2436 = 812×3).
2. **"812/812 on the frozen order"** (line 47) — index equals task_id for every one of the 812 tasks;
   `violations` empty.
3. **"697 under trailing_slash_sensitivity, 0 otherwise"** (line 48) — 697 is the count of token
   occurrences immediately followed by `/` in the original text; it materialises as a junction only in
   the one profile whose values end in `/`.
4. **"Every token occurrence is inside a string value; none is inside a key or structural text"**
   (lines 51–52) — 0 occurrences in keys, 1435 in string values, 1435 total text matches.
5. **"Occurrence offsets are Unicode codepoints in the original input text"** (line 51) — all 1435
   provenance offsets slice exactly their token out of the original text.
6. **"no profile value contains a token"** (line 63) — all 18 values scanned, zero hits.
7. **"a reversed-order mutant produces identical output on real data"** (line 64) — forward and reversed
   projections are byte-identical per profile.
8. **"index==task_id holds for all 812 tasks"** (line 62) and the hand-witness pointer to
   `plans/fixtures/r29/hand/index-shuffled-ids.fixture.json` — that fixture exists and records
   `expected_index_equals_task_id: [false, false]` for a 2-task shuffled input.
9. **"its token occurs 0 times, so 5 of 6 tokens are exercised by real data"** (line 59) — WIKIPEDIA 0
   occurrences; the other five all non-zero. The cascade hand case covers WIKIPEDIA as an ordered
   replacement step.
10. **"`sites` metadata is not used to count tokens"** (line 60) — the `sites` histogram and the
    token-task histogram differ on three sites, confirming `sites` is not the counting basis.
11. **S070 anchors** `main8–23`, `replacements11–16`, `parse20`, `enumerate-index21–23` and the body's
    line-5 / line-20 / line-21–23 claims — all resolve to the cited lines of the pinned generator.
12. **S072 anchors** `lines79,84–92,95,97–101` and the step-2 / step-3 body claims — all resolve against
    the upstream README at the pinned revision, whose sha256 matches the S072 digest.
13. **S073 anchor** `lines1–6` and the "only creates `./.auth` and runs `auto_login.py`" / "not the
    generator call site" claims — verified against the pinned `prepare.sh`.
14. **S071 anchors** `Character Encodings` and `loads` — both section/function anchors exist in the
    pinned Python 3.15.1 doc page; the "raises on an invalid document" and escape-decoding behaviours
    are reproduced against the stdlib.
15. **S068 raw-task input pin** — byte-pinned in the manifest and matching the S068 row.
16. **"exit0, 0 findings"** (line 36) — reproduced; `--json` also yields 0 findings and the exact
    output digest recorded in `corpus/evidence/round29-calibration/build-json-sha256.txt`.
17. **"Calibration and novelty scores are unchanged"** (line 79) — consistent with `SCORECARD.md`
    ("Keep novelty7/coverage cap and calibration8 until independently justified") and with the lane
    master's `git diff` showing no SCORECARD change.

## 6. Residual risk and verification gaps

* **N1 is a real location error in the frozen bytes.** Because the candidate is frozen at
  `7006b93d…53dc` and the freeze file states that admission "requires returned complete second-seat
  rereads of exactly these bytes", a location defect here cannot be repaired by editing the draft
  without changing the reviewed digest. [INFERENCE] The remedy belongs to the admitting seat, not to
  this read-only leaf.
* **The `834` provenance gap (N2) is a labelling matter, not a numeric one**; the value is correct and
  the row already says "(not additive: sum 834, distinct 812)".
* **N3 and N4 are wording-level.** Neither changes a measured value; N3 could mislead a reader who
  checks the word "answer" against the raw file's key names, and N4 states a conditional as
  unconditional.
* **Coverage gap I could not close from inside this lane:** the candidate asserts the generator's
  behaviour as read from inert source. I verified the pinned bytes' content and reproduced the
  behaviour offline, but I did not and cannot observe upstream `env_config` values, a live
  `browser_env` import, or any executed generator run. The candidate makes no such claim (lines 16–18
  disclaim it), so this gap does not affect the verdict, but it bounds what "source-faithful" can mean
  here.
* **Not re-derived by me, but checked for internal consistency against the instrument:** the per-task
  `output_filename` / `output_index` records (812 per profile) and the
  `would_be_file_sha256` fields. Their presence and shape are visible in `--json`; the per-task byte
  digests themselves are produced by the instrument and were not independently recomputed, since the
  upstream write path (`json.dump(item, f, indent=2)`) is outside this item's number set.
* **Sibling coverage overlaps:** N1 is also in `FCritNoAxisHarm.md` and `FEntryQuality.md`; N2 in
  `FCritUnits.md`; N3 in `FPathMustInclude.md`; the "identical per profile except digests" wording on
  line 36 is separately reported by `FCritClaimMet.md` (D8) and `FEntryScope.md`. I reached each
  conclusion independently from the pinned bytes; I record the overlap so the admitting seat can see
  the whole defect set without double counting.
* **[INFERENCE]** `FEntryQuality.md` line 61 notes that the earlier draft bytes `7bf99d9b…` are not
  retained at this path in git history; my own full-object-store blob sweep (2043 blobs) confirms no
  blob with that prefix exists anywhere in the lane repository, so the line-14 provenance reference
  cannot be re-read from the lane.

## 7. Scope note

This verdict covers **only** the numbers and locations in
`.ufo/waves/round-29/drafts/webarena-config-projection.md` at sha256
`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc`, and the canonical landing path
`corpus/knowledge/webarena-config-projection.md`. It is not a round-29 admission, not a claim about
task validity, deployment configuration, model performance, hosted judges or contamination, and it does
not judge the axis scores. Every measured number re-derived here agrees with the instrument, and the
single location error found (N1) is fixable by a citation change.

VERDICT: PARTIAL
