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

---

## Re-check at dbcecded (follow-up)

Seat `KengakuR29-2.FEntryNumbers-2` (same seat, same item; second-seat Q10 re-read). Lane master at
re-check time: `dbcecded4a04247cf6fd12919327af973da10bdd`. Follow-up to the section above; **the earlier
bytes of this report are unchanged** (pre-append report sha256
`b61eb6abd8742453b6a2bec6f3dc43bdfb082b8dcac85be0085d7777fd697711`, 427 lines / 31958 bytes).

**Byte identity of candidate v2 (observed)**

```
sha256sum .ufo/waves/round-29/drafts/webarena-config-projection.md
435d4bb1c7b1881d2fdc8a29f84719ec39f199bd0bc96d60fde5a647cd98f8e5
```

Full 64-hex sha256 of the bytes reviewed in this re-check:
**`435d4bb1c7b1881d2fdc8a29f84719ec39f199bd0bc96d60fde5a647cd98f8e5`** — equal to the expected value
given in the follow-up instruction and to `.ufo/waves/round-29/candidate-freeze-v2.json`'s `sha256`
field. Every line reference below is to these exact bytes. Canonical path:
**`corpus/knowledge/webarena-config-projection.md`** (still absent on disk: `test -e` → absent; the v2
freeze file names it as `canonical_path`).

**Independence (observed)**

I again did **not** read the production source `plans/config_projection.py`. I ran it only through
`--summary`, `--json` and `--selftest`, and read its *output*. My own numbers come from
`.ufo/waves/round-29/scratch/falsify/FEntryNumbers-2/derive_v2.py`, written from the S070 text contract
(six ordered `str.replace` on the whole serialized text, then `json.loads`, then `enumerate`), the
pinned raw file and `plans/fixtures/r29/profiles.json`; output saved beside it as
`derive-v2-out.txt`, with `v2-summary.txt` and `v2-out.json` holding the instrument's own output.
Scratch dir is my own: `.ufo/waves/round-29/scratch/falsify/FEntryNumbers-2/`.

Tool installs/updates: **none** (stdlib `python3` 3.14.8 sufficed; no pacman, no uv, no downloads).
Network: five `curl` GETs of public pinned upstream URLs, all written to `/tmp` for anchor verification
(upstream `README.md`, upstream `prepare.sh`, `docs.python.org/3/library/json.html`,
BrowserGym `task.py` at the pinned commit). **All six of my `/tmp` copies were deleted after use**
(`/tmp/wa_README.md`, `/tmp/wa_prepare.sh`, `/tmp/py_json.html`, `/tmp/bg_task.py`, `/tmp/v1.md`,
`/tmp/blobs.txt`), per the disk-tight instruction. No lane, corpus, fixture, SOURCES, SCORECARD or
candidate file was mutated; git was used read-only.

### 1. Verdict summary

**Every number and every source-line anchor in candidate v2 that I could check reproduces exactly under
independent re-derivation.** All four of my v1 findings N1–N4 are **resolved** in v2. One **new**
finding appears: the v2 falsification paragraph attributes oracle reproduction of *"every count"* to
four oracle reports that, on their own recorded bytes, cover none of the five task-unit counts v2 newly
introduces. That is a coverage/attribution defect in a statement about the evidence, not a wrong number
— every number itself is correct.

| # | severity | class | location | status |
|---|---|---|---|---|
| N1 | medium | location / citation | v1 line 10 | **RESOLVED in v2** — now cites `corpus/README.md:338` directly |
| N2 | low | provenance wording | v1 line 42 | **RESOLVED in v2** — the 834 bridge is now stated as 790+22 |
| N3 | low | path-label ambiguity | v1 lines 44, 56 | **RESOLVED in v2** — full template `program_html[].required_contents.must_include[]` |
| N4 | low | rationale precision | v1 lines 73–74 | **RESOLVED in v2** — reason list now covers break, restructure and cascade |
| **N5** | **medium** | **evidence coverage / attribution** | **v2 line 61** | **NEW — "reproduced every count" over-claims oracle coverage** |

Because every number and location in v2 is correct as written, and N1–N4 are resolved, but N5 is a
real defect in a factual statement inside the entry, the scoped verdict on these exact bytes is
**PARTIAL**.

### 2. Every v2 number re-derived independently (observed)

Source: `derive_v2.py` output (`derive-v2-out.txt`), computed from the pinned raw file and pinned
profiles, never from production code. Instrument values from `--summary` (`v2-summary.txt`) and `--json`
(`v2-out.json`).

| v2 table row | value as written | independent re-derivation | agrees |
|---|---|---|---|
| input tasks / distinct IDs / profiles / task×profile projections | 812 / 812 / 3 / 2436 | 812 tasks, 812 distinct IDs, 3 profiles, 812×3 = 2436 | yes |
| original token occurrences (GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) | 385, 336, 281, 300, 0, 133 = 1435 | literal text matches in the original input: 385 / 336 / 281 / 300 / 0 / 133; sum 1435 | yes |
| tasks carrying each token | 204, 128, 192, 182, 0, 128 | same six values, per-token task counts | yes |
| **NEW** "790 one-token + 22 two-token tasks = 834 rows, 812 tasks" | 790 / 22 / 834 / 812 | tasks by number of distinct tokens carried: **{1: 790, 2: 22}**; sum of per-token rows = 790 + 2×22 = **834**; distinct tasks = **812** | yes |
| changed string leaves / of all string leaves | 1416 / 10869 | changed leaves 1416; total string leaves 10869 | yes |
| **NEW** "13 leaves hold 32 occurrences, so 1435 = 1416 + 19" | 13 / 32 / 1435 / 1416 / 19 | occurrences per token-bearing leaf: **{1: 1403, 2: 8, 3: 4, 4: 1}** → 13 leaves with >1 occurrence holding 13+8×2+4×3+1×4 = **32** occurrences; 1403 + 32 = **1435**; surplus 1435 − 1416 = **19** | yes |
| url_field 1355 (start_url 812, program_html url 338, reference_url 205) | 1355 / 812 / 338 / 205 | per-path-template change counts: `start_url` 812, `eval.program_html[].url` 338, `eval.reference_url` 205; 812+338+205 = 1355 | yes |
| non_url_field 61 (60 `program_html[].required_contents.must_include[]` strings, 1 `reference_answer_raw_annotation`) | 61 / 60 / 1 | `eval.program_html[].required_contents.must_include[]` **60**; `eval.reference_answer_raw_annotation` **1**; 60+1 = 61 | yes |
| remaining six known tokens, serialized and decoded | 0 and 0 per profile | all six tokens: 0 remaining in serialized text, 0 in decoded values, all three profiles | yes |
| **NEW** other `__…__` markers (occurrences / tasks) | `__last_url__` 65 / 55, `__page__` 12 / 9 | occurrences in the original raw text: `__last_url__` **65**, `__page__` **12**; **distinct** tasks carrying each: `__last_url__` **55**, `__page__` **9** | yes |
| output ordinal == task_id | 812/812 tasks on the frozen order | `i == task_id` for all 812; `index_task_id_mismatches` 0 | yes |
| **NEW** value-`/` then raw-`/` junctions (occurrences) | 697 in 462 tasks under trailing_slash_sensitivity, 0 otherwise | token occurrences immediately followed by `/` in the original text = **697** (GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, WIKIPEDIA 0, MAP 5); **462** distinct tasks contain at least one such junction under trailing_slash_sensitivity; 0 junctions and 0 affected tasks in the other two profiles | yes |

**Instrument identity and exit codes at v2 (observed)**

| check | result |
|---|---|
| `sha256sum plans/config_projection.py` | `135cc68283e76635df913a085e6c3fcf93b8e04e83af8e9b9aac5b14876aa142` — equals the v2 freeze `instrument` field |
| `--json` output sha256 | `a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851` — equals the v2 freeze `json_output_sha256` and `corpus/evidence/round29-calibration/repair-json-sha256.txt` |
| `--summary` | exit 0, `TOTAL findings=0 exit=0` |
| `--selftest` | exit 0, `SELFTEST clean cases=28` |
| `python3 plans/fixtures/r29/mutation_witness.py` | exit 0; `"killed": 10` of 10 mutants; control `selftest` exit 0 / `summary` `TOTAL findings=0 exit=0`; `restored_sha256` equals the live instrument digest |
| `sha256sum plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` — equal to the assignment's pinned manifest digest and to `manifest_sha256` in the v2 `--json` |

**Per-profile agreement claim (v2 line 36) — now correct.** I diffed every per-profile key in the v2
`--summary`: all count-bearing fields are identical across the three profiles; only `stimulus` (a
descriptive string), `projected_text_sha256` (the digest) and `stimulus_observations` (the junction
row) differ. v2's sentence "The three profiles agree on every count below except their text digests
and the `//` junction row" is exactly right. This closes the v1 defect that sibling seats had also
flagged on the v1 wording "identical per profile except digests".

### 3. Source-line anchors in v2 (observed)

**S070** — pinned generator `plans/fixtures/r29/generate_test_data.py`, sha256
`45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`. All anchors unchanged from v1 and
all re-verified: `main8–23` (line 8 `def main()`, line 23 `json.dump(item, f, indent=2)`),
`replacements11–16` (the six `raw.replace` calls in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN,
WIKIPEDIA, MAP), `parse20` (`data = json.loads(raw)`), `enumerate-index21–23` (`for idx, item in
enumerate(data):` … `config_files/{idx}.json` … `json.dump`), body line-5 import, body line-20 parse,
body lines 21–23 per-task filenames. Correct.

**S072** — upstream `README.md` at revision dce04686, fetched to `/tmp/wa_README.md`, sha256
`081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287`, 162 lines, equal to the S072
digest in `corpus/SOURCES.md` line 94. Anchors `lines79,84–92,95,97–101` all resolve as before. v2 adds
two body claims I checked against the fetched bytes:
- "the README's step 2 exports seven variables as scheme-less `origin:port` examples" — 11 words. Lines
  86–92 export exactly seven variables: `SHOPPING`, `SHOPPING_ADMIN`, `REDDIT`, `GITLAB`, `MAP`,
  `WIKIPEDIA`, `HOMEPAGE`; all are scheme-less `origin:port` form (e.g.
  `"<your_shopping_site_domain>:7770"`). **Correct**, and v2's count of seven is right.
- "(SHOPPING_ADMIN adds `/admin`, WIKIPEDIA a long path, HOMEPAGE is a placeholder the generator never
  replaces)" — line 87 `"<your_e_commerce_cms_domain>:7780/admin"`; line 91
  `"<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"`;
  line 92 `export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder`. The generator's six
  replacements never touch `HOMEPAGE`, so "the generator never replaces" is correct. **Correct** — this
  is the completeness gap I raised in v1 (v1 named only the `/admin` suffix), now closed.
- "All three add an `http://` scheme, which the README's examples lack" — every one of the 18 profile
  values starts `http://` (checked programmatically), and no README example carries a scheme.
  **Correct.**

**S073** — upstream `prepare.sh`, sha256 `97b8671fc66518fbfed54467f9a64965bafa54d01702d922bfbb8b32c1b0c7e2`,
6 lines / 120 bytes. Anchor `lines1–6` and the body claim "`prepare.sh` only creates `./.auth` and runs
`auto_login.py`; it is not the generator call site" — commands at lines 5–6; `grep -c` for
`generate_test_data|scripts/|config_files|__GITLAB__` in the pinned copy → 0. **Correct.**

**S071** — v2 now cites the row's located anchors: "Character Encodings §576-591, invalid-document402,
duplicate names624-625". Verified against the live page with the same method the row was derived with
(`grep` on the URL, rendered-line basis):
- line 576 = `### Character Encodings` heading; the section's BOM sentence at 588–591 and the
  escaped-output sentence at 581–582 — so `§576-591` is inside the section ✓
- line 402 = `If the data being deserialized is not a valid JSON document, a JSONDecodeError will be
  raised.` ✓
- lines 624–625 = `it ignores all but / the last name-value pair for a given name:` ✓
All three v2 anchors resolve. The v1 anchor "Character Encodings and loads" (which named no lines) is
replaced by line-located anchors.

v2 body claims under S071, each verified:
- "`json.loads` raises on an invalid document rather than repairing it" ✓ (line 402, above).
- "duplicate names keep the last value" ✓ (lines 624–625; `json.loads('{"a":1,"a":2}')` → `{'a': 2}`).
- "A value containing `"` can therefore make the projected JSON invalid **or** parse with altered
  structure (injected keys, a duplicated `task_id` overriding the original)" — I reproduced both
  branches with the stdlib: substituting a value carrying `"` plus `","task_id":99,"z":"` into
  `__MAP__` yields text that *parses*, with `task_id` **99** overriding the original `0` and an injected
  key `z` present. **Correct**, and materially stronger than v1's wording.
- "a value containing `\` can make it invalid or be decoded as a JSON escape (`\n` becomes a newline)" —
  reproduced both branches: a lone `\` before a non-escape character raises `JSONDecodeError`; a
  two-character `\n` in a value decodes to a real newline. **Correct.**

**S074 (new row)** — BrowserGym WebArena loader at commit
`4ccc72332ab9882bc9aed87264dbf60b16e426f0`, fetched to `/tmp/bg_task.py`: sha256
`f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67`, 8603 bytes — both equal to
`corpus/SOURCES.md` line 96 (S074 row). Anchors and claims:
- `lines55–69` — line 55 reads the packaged `test.raw.json`; lines 58–66 are the ordered
  `all_configs_str.replace(pattern, ...)` loop over the same six tokens in the same order
  (`__GITLAB__`, `__REDDIT__`, `__SHOPPING__`, `__SHOPPING_ADMIN__`, `__WIKIPEDIA__`, `__MAP__`); line 69
  is `all_configs = json.loads(all_configs_str)`. **Correct.**
- `lines81–82` — the `task_id` selection branch:
  `elif task_id is not None:` / `task_configs = [conf for conf in all_configs if conf["task_id"] == task_id]`.
  **Correct.**
- v2 body claim "the BrowserGym loader does the same ordered replacement (S074)" ✓ — same six tokens,
  same order, on the serialized text, then parse. **Correct.**
- v2 operational claim "Harnesses that select configs by `task_id` (S074) need checks 1, 2 and 4 only" —
  consistent with lines 81–82: such a harness never relies on the enumerate ordinal, so the
  filename-vs-`task_id` comparison (check 3) is the one that drops out, while the task count, the
  non-URL-leaf accounting and the value-rejection rules still apply. **Consistent** with the cited
  lines. [INFERENCE] The rule's soundness for a harness that selects by `task_id` follows from the
  selection code shown; I did not execute BrowserGym.

**S068** — pinned raw file `plans/fixtures/r28/webarena/config_files/test.raw.json`, sha256
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, equal to the manifest entry and to
the S068 row's byte pin. v2's cite is now "S068 raw-task input … manifest byte pin" — an accurate
description of how the row is used. **Correct.**

**Corpus and prereg locations cited in v2 (observed)**
- "Extends the gap left by round28 at corpus/README.md:338" — line 338 of `corpus/README.md` reads
  "generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open."
  The quote is exact and the line number is exact. **Correct — this resolves my v1 finding N1** (v1
  attributed the phrase to the `## Frontier` section, where it does not occur: `awk 'NR>=253 && NR<=267'`
  piped to `grep -c "generated eval-time configs"` → 0).
- "`knowledge/webarena-task-spec-audit.md` audited raw specs only" — that file exists at
  `corpus/knowledge/webarena-task-spec-audit.md` (14594 bytes) and its own scope line reads "static
  task-spec observability". **Correct.**
- "No profile is a baseline: “neutral” in the round's plan means synthetic and non-deployment, and
  “benign” means values that keep the text JSON-safe." — the prereg uses "neutral substitution profiles"
  (line 13), "frozen benign profile domain" (line 44), "benign profiles" (line 80) and "all3 benign
  profiles" (line 105). The gloss "synthetic and non-deployment" for "neutral" and "values that keep the
  text JSON-safe" for "benign" are consistent with the prereg's own use (line 45: "No URL normalization,
  escaping repair or URL-only substitution is silently introduced"). **Correct.**

### 4. Finding N5 — medium — the falsification paragraph over-claims oracle coverage

**Location:** v2 line 61 — "Falsification: four independently written oracles reproduced every count,
all 1435 provenance records and all 2436 projected objects and would-be file digests" (20 words).

**Observed.** The four named reports exist and each carries `VERDICT: PASS` and an independence
statement:
`.ufo/waves/round-29/falsify/FOracleText.md` (writer `…FOracleText-2`), `FOracleLeaf.md`
(`…FOracleLeaf-2`), `FOracleProvenance.md` (`…FOracleProvenance-2`), `FOracleIndex.md`
(`…FOracleIndex-2`). Each states it did not read or import the production source; `FOracleProvenance`
adds "no production source read" in its scope line, and `FOracleLeaf`/`FOracleIndex` carry explicit
independence sections. Their recorded instrument output is the **v1** `--json` digest: both
`FOracleText`'s captured `instrument-json.json` and `FOracleProvenance`'s `instrumentjson` hash to
`c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, and `FOracleProvenance` line 19
records `instrumentjson sha256 c8da0c5a…` explicitly. The v2 `--json` digest is
`a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851` — a different byte string, and the
v2 instrument changed shape: v2's `index_mapping` keys are `unit`, `index_equals_task_id_count`,
`index_task_id_mismatches`, `output_index_rule`, whereas the captured oracle JSON has the v1 keys
`index_equals_task_id`, `output_index_rule`, `violations`. `FOracleText`'s own `diff-report.txt` scores
the v1 key `index_mapping.index_equals_task_id` as its single `DISAGREEMENTS 1` row (a unit
divergence, resolved as non-factual). The oracle file mtimes (13:56–14:00) also precede the v2
instrument's 14:23 mtime.

The coverage gap is specific. v2 newly introduces five task-unit quantities that the four reports do
not contain, and which the instrument does not emit either:
- **55** tasks carrying `__last_url__` and **9** tasks carrying `__page__` — the reports state the
  occurrence counts 65 and 12 (`FOracleText` line 29: "other markers `__last_url__` 65, `__page__` 12")
  but no report states a *task* count for either marker.
- **462** tasks containing a `//` junction — the reports state `tokens-followed-by-slash 697` and the
  instrument emits `value_slash_then_raw_slash_junctions: 697`; no report or instrument field states a
  junction *task* count. I searched all four reports and the v2 `--json` for `462`: the only hits are
  `task_index`/`task_id` values inside `occurrence_provenance` and per-task records, never a count.
- **790** one-token tasks and **22** two-token tasks — no report states the one/two-token split;
  `FOracleLeaf` line 107–109 gives the *leaf*-level split ("13 leaves with ≥2 occurrences ≠ 0 leaves
  with ≥2 distinct tokens ≠ 812 tasks. Extras 19 = repeated same-token leaves only"), which is a
  different unit and does not yield 790/22.
- **32** occurrences held by the 13 multi-occurrence leaves — the reports give 13 and 19 (the surplus),
  not the 32.
Searching all four reports for the standalone tokens `55`, `462`, `32`, `19`, `790` returns only
coincidental hits inside sha256 digests and line numbers, plus `FOracleLeaf`'s "Extras 19" sentence.

**Why it matters.** The v1 entry made no falsification claim at all; v2 adds one, and it is the
paragraph that discharges the prereg's independent-oracle leg (prereg line 79: "Independent oracle is
separately authored and does not read/import production projection code"; line 81: "Main compares
every required metric and per-task object, not only totals"). The claim as written is stronger than
the evidence supports: on the reports' own recorded bytes, the oracles did not reproduce the
task-unit counts that v2's own table newly introduces. The `repair-projection-equality.json` receipt
does bridge v1→v2 for `occurrence_provenance` and per-profile task objects
(`occurrence_provenance_equal: true`, `tasks_equal_as_objects: true` for all three profiles), but that
receipt is the instrument author's own, not an independent oracle, and it says nothing about the five
task-unit figures. The v2 numbers themselves are all correct — I re-derived every one of them — so the
defect is in the attribution, not in the arithmetic.

**Smallest fix.** Either scope the sentence to what the four reports actually verified (e.g. "reproduced
the occurrence, leaf, per-task object and would-be-file-digest census … the task-unit counts 55, 9, 462
and the 790/22 split were re-derived by the entry author, not by an oracle"), or add an independent
oracle pass over the five new task-unit figures. The entry is otherwise honest about authorship: it
states "the instrument author also wrote this entry", which is the disclosure that makes the
task-unit derivation attributable.

### 5. v1 findings N1–N4 — resolution status (observed)

| v1 finding | v1 wording | v2 wording | resolution |
|---|---|---|---|
| N1 (medium) — location | line 10: "Extends corpus/README.md Frontier “generated eval-time configs”" (10 words) — the phrase does not occur in the `## Frontier` section (253–266) | line 10: "Extends the gap left by round28 at corpus/README.md:338 (“generated eval-time configs … remain open”)" | **RESOLVED.** The line-number citation is exact and the quote is exact. |
| N2 (low) — provenance | line 42: "tasks carrying each token (not additive: sum 834, distinct 812)" — 834 appeared in no instrument output | line 42: "tasks carrying each token (not additive: 790 one-token + 22 two-token tasks = 834 rows, 812 tasks)" | **RESOLVED.** The 834 row count is now derived in-cell from a stated bridge, and the bridge is correct (790 + 2×22 = 834; 790 + 22 = 812 tasks). |
| N3 (low) — path label | line 44: "non_url_field 61 (must_include 60, …)" and line 56: "61 changed leaves are `must_include` answer strings" — `must_include` is a key under two different paths (`eval.reference_answers.must_include[]`, 396 leaves, 0 changed; `eval.program_html[].required_contents.must_include[]`, 815 leaves, 60 changed) | line 44: "non_url_field 61 (60 `program_html[].required_contents.must_include[]` strings, 1 `reference_answer_raw_annotation`)"; the "answer strings" phrasing is gone | **RESOLVED.** The path template now disambiguates the two `must_include` paths. (The word "answer" is also dropped, correctly: the changed leaves are `required_contents` entries, not `reference_answers` answers — my own leaf walk confirms 0 of the 396 `reference_answers.must_include[]` leaves carry a token.) |
| N4 (low) — rationale | lines 73–74: "reject any value carrying `"`, `\` or a token string, because text replacement would break JSON or cascade" — "cascade" holds only for a token replaced *later* in the order | lines 84–86: "(4) reject any value containing `"`, `\`, a control character (U+0000–U+001F) or a token string, because text replacement would break or restructure the JSON or cascade" | **RESOLVED.** The reason list now covers the two distinct JSON harms and the cascade. The added control-character rule is correct: a value carrying U+0001 makes the projected text invalid (`JSONDecodeError: Invalid control character`), and U+0000–U+001F is exactly the range the stdlib rejects inside strings. The cascade direction is still order-dependent, but the rule rejects on the *presence* of a token string, so the rule itself remains conservative and correct. |

Also closed since v1, in the same family: v1's "identical per profile except digests" (v1 line 36) is now
"The three profiles agree on every count below except their text digests and the `//` junction row",
which matches the per-profile diff exactly; and the v1 "S071 … Character Encodings and loads" anchor is
now line-located.

### 6. Items checked and found correct (no finding)

1. All 16 table numbers in v2, including the five newly-introduced task-unit figures (790, 22, 32, 55,
   9, 462) — independently re-derived and correct.
2. Every internal arithmetic identity in the v2 table: 812×3 = 2436; 790 + 2×22 = 834; 790 + 22 = 812;
   1403 + 32 = 1435; 1435 − 1416 = 19; 812 + 338 + 205 = 1355; 60 + 1 = 61; 1355 + 61 = 1416; 812 + 338
   + 205 + 60 + 1 = 1416.
3. "The three profiles agree on every count below except their text digests and the `//` junction row" —
   verified by diffing every per-profile key.
4. "Occurrence offsets are Unicode codepoints in the original input text; every occurrence is inside a
   string value, none in a key or structural text" — the v2 `occurrence_roles` is `{value: 1435}`, and my
   own scan finds 0 occurrences in keys and 1435 in string values.
5. "The category is by JSON path, so all 61 non_url_field leaves hold URL-shaped strings under non-URL
   keys" — verified programmatically for all three profiles: 0 of the 61 non_url_field changed leaves
   fail a `http://`/`https://` prefix test (they are `program_html[].required_contents.must_include[]`
   and `reference_answer_raw_annotation`, which hold URL-shaped text under non-URL keys). The
   instrument's own `LIMIT` line and the `category_by_value_shape` mutant (killed, selftest exit 1)
   corroborate that the category is path-based, not shape-based.
6. S070, S072, S073, S074, S068 and S071 anchors — every one resolves to the cited location (detail
   in section 3).
7. "the README's step 2 exports seven variables" — seven exports at README lines 86–92, all
   scheme-less `origin:port`; the `/admin`, WIKIPEDIA long-path and HOMEPAGE-placeholder details all
   match lines 87, 91 and 92.
8. "All three add an `http://` scheme, which the README's examples lack" — all 18 profile values carry
   `http://`; no README example carries a scheme.
9. The S071 body claims — raise-not-repair, duplicate-names-last-value, the `"`-injection branch
   (injected key and `task_id` override both reproduced), and the `\` branch (invalid vs escape-decoded)
   — all verified against the stdlib and the pinned doc lines.
10. "a URL-fields-only re-implementation leaves them unprojected and is killed by the tests
    (`plans/fixtures/r29/mutation_witness.py`)" — the witness runs, exit 0, `url_only_substitution`
    killed with `selftest_exit: 1`, `summary_exit: 1`, `TOTAL findings=6 exit=1`; the file exists at
    the cited path.
11. "No profile value contains a token, so a reversed-order mutant produces identical output on real
    data" — verified: forward and reversed replacement orders produce byte-identical projected text for
    all three profiles.
12. "index==task_id holds for all 812 tasks; a shuffled-ID hand witness shows the enumerate rule" — the
    v2 `--summary` `INDEX_WITNESS hand` row shows `config_files/0.json` carrying `task_id 1` and
    `config_files/1.json` carrying `task_id 0`, both `index_equals_task_id: false`.
13. "`sites` metadata is not used to count tokens" — the `sites` histogram (gitlab 204, reddit 129,
    shopping 192, shopping_admin 184, wikipedia 23, map 128) differs from the token task counts
    (204, 128, 192, 182, 0, 128), so the counts are demonstrably not site-derived; the instrument's
    `LIMIT` line says the same.
14. "Its token occurs 0 times, so 5 of 6 tokens are exercised by real data" — WIKIPEDIA 0 occurrences;
    the other five all non-zero.
15. "Calibration and novelty scores are unchanged" — consistent with `SCORECARD.md` ("Keep novelty7/
    coverage cap and calibration8 until independently justified").
16. "Receipts: `corpus/evidence/round29-calibration/`" — the directory exists and now holds the
    `repair-*` receipts (including `repair-json-sha256.txt` = the v2 `--json` digest and
    `repair-projection-equality.json`).

### 7. Residual risk and verification gaps

* **N5 is a defect in the entry's own falsification sentence, not in a number.** Because v2 is frozen
  at `435d4bb1…f8e5`, it cannot be repaired without changing the reviewed bytes; the remedy belongs
  to the admitting seat.
* **The five task-unit figures are correct but singly-sourced.** They are re-derivable from the pinned
  raw file and the pinned profiles (I did it), but they are not in the instrument's output and not in
  any of the four oracle reports, so within this lane they rest on the entry author's own derivation
  plus the entry author's own repair receipt. [INFERENCE] An admission that requires independent
  agreement over *every* table cell would need one more independent pass over those five figures; the
  prereg's own wording ("compares every required metric and per-task object") is satisfied by the
  per-task-object comparison the oracles did perform.
* **Coverage gap I could not close from inside this lane:** the candidate asserts the generator's
  behaviour as read from inert source. I verified the pinned bytes and reproduced the behaviour
  offline, but I did not and cannot observe upstream `env_config` values, a live `browser_env` import,
  any executed generator run, or the BrowserGym harness in execution. v2 makes no such claim
  (lines 16–18 disclaim it), so this bounds what "source-faithful" can mean here rather than
  affecting the verdict.
* **Not independently recomputed by me:** the per-task `would_be_file_sha256` values. The instrument
  emits them and `FOracleText`/`FOracleLeaf`/`FOracleIndex` each report reproducing all 2436 as
  `sha256(json.dumps(task, indent=2))`; I confirmed the formula and the oracle's agreement but did not
  re-hash all 2436 objects myself, since the upstream write path (`json.dump(item, f, indent=2)`) is
  outside this item's number set.
* **Line-number basis for the S071 anchors.** The row's numbers are the harness rendered-text
  positions (768 rendered lines), as sibling `FReopenS071.md` line 73 records. I re-verified all three
  v2 S071 anchors with the same `grep`-on-URL method and they resolve. [INFERENCE] A checker using raw
  HTML bytes rather than the rendered reader will not reproduce them; this is a basis property, already
  recorded by that sibling seat, and it is inherited here rather than introduced by v2.
* **Sibling overlap.** N5 is not in any report I read; N1–N4 were also raised independently by
  `FCritNoAxisHarm.md` (N1), `FCritUnits.md` (N2) and `FPathMustInclude.md` (N3), and the v1
  "identical per profile except digests" wording was raised by `FCritClaimMet.md` (D8) and
  `FEntryScope.md`. I reached each conclusion independently from the pinned bytes.
* **[INFERENCE]** The v1 draft bytes `7bf99d9b…` referenced by `R29DraftEntry` remain absent from the
  lane's git object store (my full-object-store blob sweep found no blob with that prefix), so that
  earlier provenance reference is still not re-readable from the lane. `R29DraftEntry.md` itself
  remains on disk.

### 8. Scope note

This verdict covers **only** the numbers and locations in
`.ufo/waves/round-29/drafts/webarena-config-projection.md` at sha256
`435d4bb1c7b1881d2fdc8a29f84719ec39f199bd0bc96d60fde5a647cd98f8e5`, and the canonical landing path
`corpus/knowledge/webarena-config-projection.md`. It is not a round-29 admission, not a claim about
task validity, deployment configuration, model performance, hosted judges or contamination, and it does
not judge the axis scores. Every number and location in these bytes reproduces; the single defect found
(N5) is in the entry's statement of what its falsification oracles covered, and is fixable by a
one-clause scope correction to that sentence.

VERDICT: PARTIAL

---

## Final re-check at v3 (follow-up)

Seat `KengakuR29-2.FEntryNumbers-2` (same seat, same item; third follow-up). Lane master at re-check
time: `dbcecded4a04247cf6fd12919327af973da10bdd`. **Earlier bytes of this report are unchanged**
(pre-append report sha256 `69aa22049f098834c6ef203733cf4fe4a444d4adbbdfa15f9ef484a6527e517d`, 799 lines
/ 63565 bytes; this section is appended at the end only).

**Byte identity of candidate v3 (observed)**

```
sha256sum .ufo/waves/round-29/drafts/webarena-config-projection.md
59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca
```

Full 64-hex sha256 of the bytes reviewed in this final re-check:
**`59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`** — equal to the expected value
given in the follow-up instruction. (There is no `candidate-freeze-v3.json` in
`.ufo/waves/round-29/`; the freeze files present are `candidate-freeze-v1.json` and
`candidate-freeze-v2.json`, the latter recording the superseded digest `435d4bb1…f8e5`.) Every line
reference below is to these exact v3 bytes. Canonical path:
**`corpus/knowledge/webarena-config-projection.md`** (still absent on disk: `test -e` → absent; the v2
freeze file names it as `canonical_path`).

**Independence (observed)**

I did **not** read the production source `plans/config_projection.py` at any point in this item. I ran
it only through `--summary`, `--json` and `--selftest` and read its *output*. My numbers come from
`.ufo/waves/round-29/scratch/falsify/FEntryNumbers-2/derive_v2.py`, written from the S070 text contract
(six ordered `str.replace` on the whole serialized text, then `json.loads`, then `enumerate`), the
pinned raw file and `plans/fixtures/r29/profiles.json`; its output is saved beside it as
`derive-v2-out.txt`. For the receipt check I additionally reconstructed the **v1** instrument under
`/tmp` from `git show 56fd949:plans/config_projection.py` and ran it in a `/tmp` copy of the lane tree
at that commit, so the oracle-comparison bytes could be reproduced without touching the lane.

Tool installs/updates: **none** (stdlib `python3` 3.14.8 sufficed; no pacman, no uv, no downloads).
Network: five `curl` GETs of public pinned upstream URLs (upstream `README.md`, upstream `prepare.sh`,
`docs.python.org/3/library/json.html`, BrowserGym `task.py` at the pinned commit). **All my `/tmp` copies
were deleted after use** (`/tmp/fen_v1/`, `/tmp/fen_lane56/`, `/tmp/v2.md`, `/tmp/a1`, `/tmp/a2`,
`/tmp/b1`, `/tmp/b2`, `/tmp/v3diff.txt`). No lane, corpus, fixture, SOURCES, SCORECARD, candidate or
git-index file was mutated; git was used read-only (`log`, `show`, `rev-parse`, `status`, `ls-files`,
`archive`, `cat-file`).

### 1. Verdict summary

**Every number and every source-line anchor in candidate v3 reproduces exactly under independent
re-derivation. My v2 finding N5 (oracle-coverage over-claim) is resolved in v3**, and the v3 wording
adds an explicit falsifiers block and an equality receipt that I verified end-to-end. I found **no new
defect** in the v3 bytes.

| # | severity | class | location | status |
|---|---|---|---|---|
| N1 | medium | location / citation | v1 line 10 | **RESOLVED in v2**, unchanged in v3 |
| N2 | low | provenance wording | v1 line 42 | **RESOLVED in v2**, unchanged in v3 |
| N3 | low | path-label ambiguity | v1 lines 44, 56 | **RESOLVED in v2**, unchanged in v3 |
| N4 | low | rationale precision | v1 lines 73–74 | **RESOLVED in v2**, unchanged in v3 |
| N5 | medium | evidence coverage / attribution | v2 line 61 | **RESOLVED in v3** — attribution now scoped, with an equality receipt I verified |
| — | — | — | v3 lines 37, 58–70 | **no defect found** — new wording verified |

Scoped verdict on these exact bytes: **PASS**.

### 2. What changed from v2 to v3, and whether each change is correct (observed)

The v3 delta is confined to lines 37 and 58–70, as the follow-up stated. Verified by diffing
`git show dbcecded:.ufo/waves/round-29/drafts/webarena-config-projection.md` against the working file:
two hunks, 14 insertions / 5 deletions, **no change to any table row**. Lines 1–36 and the last 18 lines
are byte-identical to v2 (diff of the two ranges: no output). Everything I verified for v2 in the earlier
sections of this report therefore carries over unchanged, and I re-ran my independent derivation and
the instrument against the current tree as set out below.

**Change 1 — line 37 (S071 escape wording).** v2 read "be decoded as a JSON escape (`\n` becomes a
newline)"; v3 reads "be interpreted as a JSON escape" (the parenthetical example is dropped). Both
branches of the claim are true and I reproduced both with the stdlib against the pinned doc's
`json.loads` contract: a value carrying `\n` parses and yields a real newline in the decoded string; a
value carrying `\q` raises `JSONDecodeError`. The v3 wording is the more careful of the two because it
asserts only what the stdlib does, without pinning a specific example the pinned doc does not spell out
in those terms. **Correct**, and the dropped example removes a small over-claim rather than adding one.

**Change 2 — lines 58–65 (oracle attribution, now scoped).** v2 read "Falsification: four independently
written oracles reproduced every count, all 1435 provenance records and all 2436 projected objects and
would-be file digests"; v3 reads (13 words) "Four oracles, separately written by distinct same-lane seats
(independent logic, not independent identity)" and then (18 words) "reproduced the instrument's
population/profile metrics, all 1435 provenance records and all 2436 projected objects and would-be file
digests". Three things are now stated that were not, and I checked each:

1. **"distinct same-lane seats (independent logic, not independent identity)"** — accurate. The four
   reports' `writer:` lines are `KengakuR29-2.FOracleText-2`, `…FOracleLeaf-2`, `…FOracleProvenance-2`,
   `…FOracleIndex-2`: four distinct seats, all under the same lane, each with its own independence
   statement. This is the same disclosure the r28 admitted entry makes (its line 134: "independent
   logic, not independent authorship"), so the phrasing is house-consistent. It is also the correction
   my N5 asked for: identity-independence was never claimed.
2. **The reproduced scope is now the instrument's own metrics, not "every count".** I verified what the
   four reports actually cover against their recorded bytes: `FOracleText` compares all 2436 records ×
   all fields (12,180 scalar comparisons + 2436 deep `projected_task` compares + `changed_leaves` list
   equality) plus all 1435 provenance rows and 2445 hash comparisons; `FOracleLeaf` reports
   `leaf == text == instrument` on all 2436 with 0 mismatches and all 2436 `would_be_file_sha256`
   reproduced; `FOracleProvenance` reports `multiset_exact_match=True` over all 1435 provenance records
   across all six fields plus the three population fields; `FOracleIndex` reports 2436 rows × field
   classes = 21,924 checks with zero mismatches including `would_be_file_sha256` 2436/2436. That is
   exactly the scope the v3 sentence claims: population/profile metrics, 1435 provenance records, 2436
   projected objects and would-be file digests. **Correct as written.**
3. **The task-unit bridges are now explicitly excluded from the oracle claim** — (25 words) "The
   task-unit bridges added to the table (790/22, 32, 55/9 and 462) were separately re-derived by the
   entry-review seats, not by those four oracle reports." This is precisely the gap I recorded in N5:
   the four reports pin the v1 `--json` digest `c8da0c5a…`, contain no 462 / no marker task counts / no
   790-22 split, and the v2 `--json` has a different `index_mapping` shape. The v3 sentence states that
   boundary accurately. I confirmed the bridges were in fact re-derived by entry-review seats, not by
   the oracle reports: `FEntryScope.md` lines 186–190 ("{1 token: 790, 2 tokens: 22}, 834 rows";
   "697 occurrences in 462 tasks") and `FEntryQuality.md` lines 191–194 (790/22; 13 leaves, 32
   occurrences; 65/55 and 12/9; 697 in 462 tasks) — all four bridges, each with its own census. **Correct
   as written.**

**Change 3 — line 63, authorship disclosure.** "The instrument author also wrote this entry." Accurate
and appropriately placed: the instrument's `writer` is the same seat family as the entry's
(`writer: KengakuR29-2`), and the freeze file records the same writer for the candidate and the
instrument. This is a strengthening of the disclosure, not a weakening.

**Change 4 — line 64, the equality receipt.** (10 words) "binds the repaired objects to the objects the
oracles compared". I verified this end-to-end rather than taking it on trust:
- The v1 tool at `56fd949` (`sha256 5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`,
  equal to the v1 freeze's `instrument` field) run in a `/tmp` copy of the lane tree at that commit
  reproduces `--json` sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` — the exact
  digest `FOracleText` and `FOracleProvenance` recorded as their compared instrument bytes.
- Comparing that v1 output against the current `--json` output: `occurrence_provenance` equal as a
  multiset over all six fields (1435 records each); per-profile `tasks` equal as objects (812 × 3);
  every non-`tasks` profile field equal. This reproduces, independently, all three assertions in
  `corpus/evidence/round29-calibration/repair-projection-equality.json`
  (`occurrence_provenance_equal: true`, `tasks_equal_as_objects: true` and `other_fields_equal: true`
  for all three profiles), which is a git-tracked file. **Correct as written.** The receipt is the
  right artifact to cite, because it is exactly what closes the v1→v2 gap in which the oracles'
  compared bytes differ from the current instrument's bytes.

**Change 5 — lines 67–70, the falsifiers block.** New content. Every falsifier is specific, falsifiable
and attached to a quantity the instrument actually emits:
- "a changed pinned digest withdraws this snapshot's applicability" — consistent with the manifest's
  byte pins (generator `45ddba7b…`, raw `7b50386f…`, profiles `90fdc34d…`, manifest `f6390b92…`).
- "nonzero remaining six tokens" — the instrument emits `remaining_known_tokens_text` and
  `remaining_known_tokens_decoded`, all zero for all three profiles (I re-checked on the current tree).
- "a changed 61/1355 path split" — `changed_leaves_by_category` is `{"non_url_field": 61,
  "url_field": 1355}` for all three profiles on the current tree.
- "an index/task-ID mismatch on the frozen order" — `index_equals_task_id_count` 812 with
  `index_task_id_mismatches` empty.
- "or disagreement with a separately derived projected object" — `would_be_file_sha256` and the deep
  `projected_task` comparison, the same surface the oracles exercised.
- "Agreement on this population alone does not establish general-input equivalence." — the correct
  scope limit, and it matches what the instrument's own LIMIT lines say.
**Correct**, and it is a genuine strengthening: the r28 reference entry carries a `Falsifiers:` block
and v2 did not.

### 3. Independent re-derivation of every v3 number (observed)

Source: `derive_v2.py` output (`derive-v2-out.txt`), re-run against the current tree; the pinned raw
file and pinned profiles, never production code. Instrument values from a fresh `--summary` and
`--json` on the current tree.

| v3 table row | value as written | independent re-derivation | agrees |
|---|---|---|---|
| input tasks / distinct IDs / profiles / task×profile projections | 812 / 812 / 3 / 2436 | 812 tasks, 812 distinct IDs, 3 profiles, 812×3 = 2436 | yes |
| original token occurrences (GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) | 385, 336, 281, 300, 0, 133 = 1435 | literal text matches in the original input: 385 / 336 / 281 / 300 / 0 / 133; sum 1435 | yes |
| tasks carrying each token | 204, 128, 192, 182, 0, 128 | same six per-token task counts | yes |
| 790 one-token + 22 two-token tasks = 834 rows, 812 tasks | 790 / 22 / 834 / 812 | tasks by number of distinct tokens carried: **{1: 790, 2: 22}**; rows = 790 + 2×22 = **834**; distinct tasks = **812** | yes |
| changed string leaves / of all string leaves | 1416 / 10869 | changed leaves 1416; total string leaves 10869 | yes |
| 13 leaves hold 32 occurrences, so 1435 = 1416 + 19 | 13 / 32 / 1435 / 1416 / 19 | occurrences per token-bearing leaf: **{1: 1403, 2: 8, 3: 4, 4: 1}** → 13 leaves with >1 occurrence holding 13+8×2+4×3+1×4 = **32**; 1403 + 32 = **1435**; surplus **19** | yes |
| url_field 1355 (start_url 812, program_html url 338, reference_url 205) | 1355 / 812 / 338 / 205 | per-path-template change counts: `start_url` 812, `eval.program_html[].url` 338, `eval.reference_url` 205; 812+338+205 = 1355 | yes |
| non_url_field 61 (60 `program_html[].required_contents.must_include[]` strings, 1 `reference_answer_raw_annotation`) | 61 / 60 / 1 | `eval.program_html[].required_contents.must_include[]` **60**; `eval.reference_answer_raw_annotation` **1**; 60+1 = 61 | yes |
| remaining six known tokens, serialized and decoded | 0 and 0 per profile | all six tokens: 0 remaining in serialized text, 0 in decoded values, all three profiles | yes |
| other `__…__` markers (occurrences / tasks) | `__last_url__` 65 / 55, `__page__` 12 / 9 | occurrences in the original raw text: `__last_url__` **65**, `__page__` **12**; **distinct** tasks carrying each: `__last_url__` **55**, `__page__` **9** | yes |
| output ordinal == task_id | 812/812 tasks on the frozen order | `i == task_id` for all 812; `index_task_id_mismatches` empty | yes |
| value-`/` then raw-`/` junctions, occurrences | 697 in 462 tasks under trailing_slash_sensitivity, 0 otherwise | token occurrences immediately followed by `/` in the original text = **697** (GITLAB 225, REDDIT 232, SHOPPING 110, SHOPPING_ADMIN 125, WIKIPEDIA 0, MAP 5); **462** distinct tasks contain ≥1 such junction under trailing_slash_sensitivity; 0 junctions and 0 affected tasks in the other two profiles | yes |

**Instrument identity and receipts on the current tree (observed)**

| check | result |
|---|---|
| `sha256sum plans/config_projection.py` | `d81a6af8c704ed6fce49516e54454bcea8c6e0f96e2a81b3f524b2459ec44f9f` — the live tool has moved past the v2 freeze's `135cc682…` (the follow-up stated the tool is finishing only tests/labels) |
| `--json` sha256 | `a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851` — **byte-identical to the v2 freeze `json_output_sha256` and to `repair-json-sha256.txt`**: the production objects are unchanged by the tool's test/label work, as the follow-up stated |
| `--summary` | exit 0, `TOTAL findings=0 exit=0` |
| `--selftest` | exit 0, `SELFTEST clean cases=28` |
| `python3 plans/fixtures/r29/mutation_witness.py` | exit 0; `tool_sha256` and `restored_sha256` both `d81a6af8…` (the live tool, restored after the run); `"killed": 12` of 12 mutants; control `selftest` exit 0 and `summary` `TOTAL findings=0 exit=0` |
| `sha256sum plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` — equal to the pinned manifest digest and to `manifest_sha256` in the `--json` |
| `sha256sum` of generator / raw file / profiles | `45ddba7b…21cd`, `7b50386f…7652`, `90fdc34d…e018` — equal to the manifest entries, so all three pinned inputs are unchanged |
| `git ls-files corpus/evidence/round29-calibration/` | the receipt `repair-projection-equality.json` is git-tracked (14 tracked files in that directory) |

**Arithmetic identities inside the v3 table (all hold):** 812×3 = 2436; 790 + 2×22 = 834; 790 + 22 = 812;
1403 + 32 = 1435; 1435 − 1416 = 19; 812 + 338 + 205 = 1355; 60 + 1 = 61; 1355 + 61 = 1416;
812 + 338 + 205 + 60 + 1 = 1416.

### 4. Source-line anchors in v3 (observed)

Lines 1–36 are byte-identical to v2, which I verified anchor-by-anchor in the section above. Re-confirmed
against the current tree and the pinned upstream bytes:

- **S070** — `plans/fixtures/r29/generate_test_data.py`, sha256 `45ddba7b…21cd`. `main8–23`,
  `replacements11–16`, `parse20`, `enumerate-index21–23`, body line-5 import, body line-20 parse, body
  lines 21–23 per-task filenames: all resolve to the cited lines.
- **S072** — upstream `README.md` at revision dce04686, sha256 `081c8264…9287`, 162 lines, equal to the
  S072 digest in `corpus/SOURCES.md`. `lines79,84–92,95,97–101` all resolve. Body claims: seven
  scheme-less `origin:port` exports at lines 86–92; `SHOPPING_ADMIN` adds `/admin` (line 87), WIKIPEDIA a
  long path (line 91), HOMEPAGE a placeholder the generator never replaces (line 92; the generator's six
  replacements never touch `HOMEPAGE`); step 3 runs the script (lines 97–101); no replacement order or
  token inventory is documented (a case-sensitive search for the six tokens returns no hit, and the only
  "replace" occurrence, line 142, is about intent-template keywords).
- **S073** — upstream `prepare.sh`, sha256 `97b8671f…c7e2`, 6 lines / 120 bytes. `lines1–6` resolve; the
  body claim that it only creates `./.auth` and runs `auto_login.py` (lines 5–6) and is not the generator
  call site holds (a search for `generate_test_data|scripts/|config_files|__GITLAB__` returns 0).
- **S071** — `https://docs.python.org/3/library/json.html`, the pinned Python 3.15.1 page. The v3 header
  cites the row's located anchors "Character Encodings §576-591, invalid-document402, duplicate
  names624-625"; I re-verified each against the live page with `grep` on the URL (rendered-line basis):
  line 576 = `### Character Encodings` heading, with the escaped-output sentence at 581–582 and the BOM
  sentence at 591 inside the cited span; line 402 = "If the data being deserialized is not a valid JSON
  document, a JSONDecodeError will be raised."; lines 624–625 = "it ignores all but / the last
  name-value pair for a given name:". All three anchors resolve exactly.
- **S074** — BrowserGym `task.py` at commit `4ccc72332ab9882bc9aed87264dbf60b16e426f0`, sha256
  `f996dfeef2bfb836fa79b20217cda36ecf428ed3965e3084e325626d7130fe67`, 8603 bytes, equal to
  `corpus/SOURCES.md` line 96. `lines55–69` (read of the packaged `test.raw.json` at 55; the six ordered
  `.replace` calls at 58–66; `json.loads` at 69) and `lines81–82` (the `task_id` selection branch) both
  resolve. The body claim that the loader performs the same ordered replacement holds.
- **S068** — pinned raw file, sha256 `7b50386f…7652`, equal to the manifest entry and the S068 byte pin;
  the v3 cite "S068 raw-task input … manifest byte pin" describes its use accurately.

**Corpus, prereg and receipt paths cited in v3 (observed)**

- "corpus/README.md:338" — line 338 reads "generated eval-time configs, runtime DOM/helper/judge
  validity and contamination checks remain open."; the quote and the line number are exact.
- "`knowledge/webarena-task-spec-audit.md` audited raw specs only" — the file exists at
  `corpus/knowledge/webarena-task-spec-audit.md` (14594 bytes) and its own scope line reads "static
  task-spec observability".
- "No profile is a baseline: “neutral” in the round's plan means synthetic and non-deployment, and
  “benign” means values that keep the text JSON-safe." — the prereg uses "neutral substitution profiles"
  (line 13), "frozen benign profile domain" (line 44), "benign profiles" (line 80) and "all3 benign
  profiles" (line 105); the gloss matches the prereg's own use (line 45: "No URL normalization, escaping
  repair or URL-only substitution is silently introduced").
- "`corpus/evidence/round29-calibration/repair-projection-equality.json`" — exists, is git-tracked, and
  its three assertions reproduce under my independent v1-vs-current comparison (section 2, change 4).
- "`.ufo/waves/round-29/falsify/FOracleText.md`, `FOracleLeaf.md`, `FOracleProvenance.md`,
  `FOracleIndex.md`" — all four exist with `VERDICT: PASS` and an independence statement each.

### 5. Resolution of every prior finding (observed)

| finding | status in v3 |
|---|---|
| **N1** (medium) — v1 line 10 attributed the quote "generated eval-time configs" to the `## Frontier` section, where it does not occur (253–266) | **RESOLVED** (v2, unchanged in v3): the cite is now the exact `corpus/README.md:338`, where the phrase does occur |
| **N2** (low) — v1's "sum 834" was a reader-side sum with no stated bridge | **RESOLVED** (v2): the row now derives it in-cell as "790 one-token + 22 two-token tasks = 834 rows, 812 tasks", and both figures reproduce |
| **N3** (low) — v1's bare `must_include` matched two different JSON paths | **RESOLVED** (v2): the row now gives `program_html[].required_contents.must_include[]` explicitly, and the "answer strings" phrasing is dropped (correctly: 0 of the 396 `reference_answers.must_include[]` leaves carry a token) |
| **N4** (low) — v1's rule cited only "break JSON or cascade" for a token string | **RESOLVED** (v2): the reason list now covers break, restructure and cascade, and adds the control-character (U+0000–U+001F) case, which I verified raises `JSONDecodeError: Invalid control character` |
| **N5** (medium) — v2 claimed the four oracles "reproduced every count", including task-unit counts they do not contain, without stating the identity limitation | **RESOLVED** (v3): the claim is scoped to the instrument's own metrics, the seat-level identity limitation is disclosed ("independent logic, not independent identity"), the task-unit bridges are explicitly attributed to the entry-review seats instead, the authorship of the entry by the instrument author is disclosed, and an equality receipt is cited — a receipt I reproduced end-to-end from the v1 tool in a `/tmp` copy of the lane at `56fd949` |

Also closed earlier and unchanged in v3: the v1 "identical per profile except digests" wording (now
"The three profiles agree on every count below except their text digests and the `//` junction row",
which matches my per-profile diff exactly) and the v1 "Character Encodings and loads" S071 anchor
(now line-located).

### 6. Items checked and found correct — no finding

1. All 16 table numbers in v3, re-derived independently on the current tree, including the five
   task-unit figures (790, 22, 32, 55, 9, 462).
2. Every internal arithmetic identity listed in section 3.
3. The per-profile agreement claim, by diffing every per-profile key in the `--summary`.
4. The occurrence-offset and occurrence-role claim: `occurrence_roles` is `{value: 1435}` and my own scan
   finds 0 occurrences in keys and 1435 in string values.
5. "all 61 non_url_field leaves hold URL-shaped strings under non-URL keys" — 0 of the 61 fail a
   `http://`/`https://` prefix test, in all three profiles.
6. S070, S072, S073, S074, S068 and S071 anchors — every one resolves to the cited location.
7. The v3 S071 wording: both branches (invalid, escape-interpreted) reproduce against the stdlib and
   the pinned page; the dropped `\n` example removes a claim the pinned page does not make in those terms.
8. The v3 oracle attribution: the four writers are four distinct seats of one lane; the reproduced
   scope matches the four reports' recorded coverage; the task-unit bridges are correctly attributed
   elsewhere and were in fact re-derived by entry-review seats.
9. The v3 equality receipt: reproduced independently (v1 tool at `56fd949` in a `/tmp` lane copy →
   `--json` `c8da0c5a…`, the digest the oracles compared; provenance multiset equal; per-profile task
   objects equal; all other profile fields equal).
10. The v3 falsifiers block — each falsifier names a quantity the instrument emits and I re-confirmed
    its current value on the live tree.
11. `python3 plans/fixtures/r29/mutation_witness.py` runs clean, kills 12 of 12 mutants, and restores
    the live tool byte-for-byte.
12. All pinned inputs unchanged: generator `45ddba7b…`, raw `7b50386f…`, profiles `90fdc34d…`,
    manifest `f6390b92…`.
13. The production `--json` digest is unchanged from the v2 freeze (`a4fb5d6d…`) even though the tool
    source digest has moved — so the tool's remaining work changed tests/labels only, as stated.

### 7. Residual risk and verification gaps

* **The live instrument digest has moved past the frozen one.** The v2 freeze pins instrument
  `135cc682…`; the tree now carries `d81a6af8…`. The `--json` output digest is byte-identical
  (`a4fb5d6d…`) and the mutation witness restores the live tool exactly, so no candidate-dependent
  count moved — but a future re-check that compares the *instrument* rather than its *output* against the
  v2 freeze would see a mismatch. This is a fact about the tree, not a defect in the v3 entry, which
  cites no instrument digest.
* **No `candidate-freeze-v3.json` exists.** The v3 digest I reviewed
  (`59b646a7…bca`) is attested only by the follow-up instruction and by my own `sha256sum`; the on-disk
  freeze file still records the superseded v2 digest. An admitting seat that gates on a freeze file
  would want a v3 freeze artifact recording `59b646a7…bca`.
* **The receipt is not self-reproducing from a persisted script.** `repair-projection-equality.json`
  states its three equality assertions but no generator command is committed beside it (a search for
  `occurrence_provenance_equal` / `tasks_equal_as_objects` across `*.py` and `*.sh` returns no
  generator). I reproduced the assertions by hand from the v1 tool in a `/tmp` lane copy, so the claims
  hold — but the receipt is re-derivable only by re-implementing it. [INFERENCE] This is the same
  provenance gap sibling `FCritClaimMet.md` recorded for `mutation-witness.txt` (D7); the difference is
  that the v2/v3 repair moved this particular receipt into the lane as a tracked JSON file.
* **The v3 falsifiers are stated but not wired into the instrument's exit codes.** They are readable
  conditions on the emitted fields, which is a reasonable contract for a knowledge entry, but no
  executable check enforces them. [INFERENCE] A reader wanting machine-checked falsifiers would want the
  instrument to fail on each condition; the prereg's own forecast scoring already leans on
  `TOTAL findings=N exit=1` for that.
* **Coverage gap I could not close from inside this lane:** the candidate asserts the generator's
  behaviour as read from inert source. I verified the pinned bytes and reproduced the behaviour offline,
  but I did not and cannot observe upstream `env_config` values, a live `browser_env` import, any
  executed generator run, or the BrowserGym harness in execution. The candidate makes no such claim
  (lines 16–18 disclaim it), so this bounds what "source-faithful" can mean here rather than affecting
  the verdict.
* **Not independently recomputed by me:** the per-task `would_be_file_sha256` values for all 2436
  objects. I confirmed the formula `sha256(json.dumps(task, indent=2))` and the oracles' reported
  agreement, and I confirmed the *equality* of v1 and current objects including their digests, but I did
  not re-hash all 2436 objects individually.
* **Line-number basis for the S071 anchors** is the harness rendered-text basis (768 rendered lines),
  as sibling `FReopenS071.md` records; a checker using raw HTML bytes will not reproduce them. This is
  inherited from the S071 row, not introduced by v3.
* **[INFERENCE]** The v1 draft bytes `7bf99d9b…` referenced by `R29DraftEntry` remain absent from the
  lane's git object store (my full-object-store blob sweep found no blob with that prefix), so that
  earlier provenance reference is still not re-readable from the lane. `R29DraftEntry.md` itself remains
  on disk.

### 8. Scope note

This verdict covers **only** the numbers and locations in
`.ufo/waves/round-29/drafts/webarena-config-projection.md` at sha256
`59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`, and the canonical landing path
`corpus/knowledge/webarena-config-projection.md`. It is not a round-29 admission, not a claim about
task validity, deployment configuration, model performance, hosted judges or contamination, and it does
not judge the axis scores. Every number and location in these bytes reproduces under independent
re-derivation; the v3 changes close the last open finding of this item (N5) and add an explicit
falsifiers block and an equality receipt, both verified here. No defect was found in the v3 bytes.

VERDICT: PASS

---

## Final exact-v5 re-check (locator-only confirmation)

Seat `KengakuR29-2.FEntryNumbers-2` (same seat, same item; final follow-up). Lane master at re-check
time: `dbcecded4a04247cf6fd12919327af973da10bdd`. **Earlier bytes of this report are unchanged**
(pre-append report sha256 `69aa22049f098834c6ef203733cf4fe4a444d4adbbdfa15f9ef484a6527e517d` for the
first 799 lines; the v3 section above is untouched).

**Byte identity of candidate v5 (observed)**

```
sha256sum .ufo/waves/round-29/drafts/webarena-config-projection.md
c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3
```

Full 64-hex sha256 of the bytes reviewed in this final re-check:
**`c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3`** — equal to the expected value
given in the follow-up instruction. (On-disk freeze files present: `candidate-freeze-v1.json` … `-v4.json`;
there is no `-v5.json`.) Canonical path: **`corpus/knowledge/webarena-config-projection.md`**.

**Scope.** Locator-only confirmation, as instructed: no new broad review, no new sources opened beyond
the one pinned Python-doc page needed to check the corrected locator. I re-verified the changed locator
against the pinned page and confirmed the rest of the file is byte-identical to the v3 bytes I already
passed. I again did **not** read the production source `plans/config_projection.py`; I ran it only
through `--summary` and `--json`. Tool installs/updates: **none**. Network: one `curl` GET of
`https://docs.python.org/3/library/json.html` (public pinned doc). All my `/tmp` copies were deleted
after use (`/tmp/py_json_v4.html`, `/tmp/v4.md`). No lane, corpus, fixture, SOURCES, SCORECARD, candidate
or git-index file was mutated.

### 1. Verdict

**The v5 locator correction is correct, the rest of the file is byte-identical to the v3 bytes I passed,
and no defect was found.** Scoped verdict on these exact bytes: **PASS**.

### 2. The delta is exactly one line, proven byte-exactly (observed)

I reconstructed v4 from v5 by substituting only line 1, and separately reconstructed v3 from v5 by
substituting only line 1 with the v3 header text. Both reconstructions reproduce the recorded digests
exactly, which pins the deltas with no slack:

| reconstruction | computed sha256 | expected | match |
|---|---|---|---|
| v5 with v4's line 1 | `9d11f44bf22d357758a5988b514d23cca84d4061816d3c3d65294974dd506e74` | v4 `9d11f44b…6e74` | yes |
| v5 with v3's line 1 | `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca` | v3 `59b646a7…bca` | yes |

So: **v5 differs from v4 in exactly line 1**, and **v5's body (lines 2–99) is byte-identical to the v3
body I passed** (body sha256 `9148a50351e134f13a98bfa3d4e1bd150fa144358498306ae5ace5c6cb8e4f4a`).
Every number, table row, falsifier, receipt reference and source anchor in the body is therefore the
v3 content I already verified and passed — carried over unchanged, not re-reviewed.

### 3. The corrected locator, verified against the pinned page (observed)

v5 line 1 now reads (13 words) "S071/S075/S076
`https://docs.python.org/3/library/json.html#character-encodings` ensure_ascii paragraph, `#json.load`
invalid-document exception inherited by `#json.loads` (Identical to load()),
`#repeated-names-within-an-object` opening paragraph/example". I fetched the pinned page to
`/tmp/py_json_v4.html` (HTTP 200, sha256 `8271280b…1d5`) and checked each anchor as an **HTML fragment
id** and each label as the **content actually under that anchor**:

| anchor | `id="…"` present | content under that anchor |
|---|---|---|
| `#character-encodings` | yes | the `ensure_ascii=True` escaping paragraph ("this module's serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting strings only contain printable ASCII characters") — **matches "ensure_ascii paragraph"** |
| `#json.load` | yes | the `Raises: JSONDecodeError – When the data being deserialized is not a valid JSON document.` bullet — **matches "invalid-document exception"** |
| `#json.loads` | yes | the opening clause "Identical to load(), but instead of a file-like object, deserialize s …" — **matches "inherited by #json.loads (Identical to load())"** |
| `#repeated-names-within-an-object` | yes | the opening paragraph "…this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:" plus the `weird_json` example yielding `{'x': 3}` — **matches "opening paragraph/example"** |

**Why this matters, and why v4's locator was the weaker one.** Locating the invalid-document sentence
by HTML structure is the decisive check, and it is exactly what distinguishes v4 from v5. The sentence
occurs twice on the page, and I resolved both occurrences by their nearest enclosing `<dt id=…>`:
- occurrence 1 (the `Raises: JSONDecodeError` bullet) sits inside the **`json.load`** entry, between
  `id="json.load"` and `id="json.loads"`;
- occurrence 2 (the `JSONDecoder` class prose "If the data being deserialized is not a valid JSON
  document, a JSONDecodeError will be raised.") sits inside the **`json.JSONDecoder`** class entry,
  between `id="json.JSONDecoder"` and `id="json.JSONDecoder.decode"`.

Neither occurrence lies inside the `json.loads` entry itself: the `json.loads` `<dt>` block contains
neither the phrase "not a valid JSON document" nor the token "JSONDecodeError". v4's locator therefore
pointed `#json.loads` at a fragment whose own entry does not state the exception it was cited for —
precisely the defect my locator-only medium finding flagged. v5 corrects it exactly: the exception is
cited at **`#json.load`**, and the inheritance by `loads` is carried by `loads`' own explicit
**"Identical to load()"** clause, which is a separate, verifiable statement on the same page. I
re-confirmed that clause exists under `#json.loads`. The `corpus/SOURCES.md` rows agree: S075 (line 97)
locates S071's three facts by stable section anchors, and **S076 (line 98)** — which v5's header also
cites — scopes itself to "exact API location of the invalid-document exception inherited by loads,
correcting S075 only", with the note that "the invalid-document JSONDecodeError sentence is under
json.load; json.loads inherits that contract by its explicit Identical to load() clause, rather than
repeating the sentence". The candidate and both source rows now say the same thing.

### 4. The body facts the locator still supports (observed)

The v5 body is byte-identical to the passed v3 body, so its S071 bullet (lines 34–37) is unchanged:
"`json.loads` raises on an invalid document rather than repairing it, and duplicate names keep the last
value." Both halves remain true **under the corrected locators**:
- *raises on an invalid document*: the `Raises: JSONDecodeError` bullet under `#json.load`, which
  `loads` inherits via its "Identical to load()" clause — both fragments verified present with that
  content.
- *duplicate names keep the last value*: the `#repeated-names-within-an-object` paragraph and example,
  verified above; independently reproduced against the stdlib — `json.loads('{"x":1,"x":2,"x":3}')` →
  `{'x': 3}`, and `json.loads("not json")` raises `JSONDecodeError`.

**The corrected locator is strictly stronger than the one it replaces.** It is anchored to HTML
fragment ids and section names rather than to renderer-dependent line coordinates, so it is portable
across reader renderings — which was the whole point of S075/S076 and of my locator-only finding. The
body contains **no** remaining line-coordinate references to the Python doc: a search of the candidate
for `402`, `624-625` and `576-591` returns nothing, so no stale coordinate survives anywhere in the
file, header or body.

### 5. Metrics and receipts unchanged (observed)

Re-ran against the current tree; every value is identical to what I verified and passed at v3:

| check | result |
|---|---|
| `python3 plans/config_projection.py --summary` | exit 0, `TOTAL findings=0 exit=0` |
| `python3 plans/config_projection.py --json` sha256 | `a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851` — **byte-identical to the v2/v3 freeze and to `repair-json-sha256.txt`** |
| my independent derivation | 790 one-token + 22 two-token tasks; 10869 string leaves; 1416 changed leaves; marker occurrences `__page__` 12 / `__last_url__` 65; 697 junctions; remaining six tokens 0 text and 0 decoded — all as in the passed v3 table |
| `corpus/SOURCES.md` | S075 at line 97 and **S076 at line 98** present, both tier-A `docs` rows with the anchor sets v5 cites |

The production objects are unchanged, so the v3 PASS on every number and every other location carries
over verbatim.

### 6. Items checked and found correct — no finding

1. v5 line 1 is the only changed byte; the delta to v4 and to v3 is proven byte-exactly (§2).
2. All four fragment anchors exist as HTML `id`s on the pinned page and each label matches the content
   actually under that anchor (§3).
3. The invalid-document sentence is under `json.load`, not `json.loads`; the `loads` inheritance is
   carried by its own "Identical to load()" clause — both located in the candidate and in S076 exactly
   as the page shows.
4. The body S071 bullet remains true under the corrected locators (§4).
5. No stale line coordinate survives anywhere in the file.
6. Every number, table row, falsifier and receipt reference is the passed v3 content, byte-identical.
7. Production `--json` digest unchanged; `--summary` clean; my independent derivation reproduces every
   table figure.

### 7. Residual risk and verification gaps

* **No `candidate-freeze-v5.json` exists.** The v5 digest is attested by the follow-up instruction and
  by my own `sha256sum`; the on-disk freeze chain stops at `-v4.json`. An admitting seat gating on a
  freeze artifact would want a v5 freeze recording `c4412f67…daf3`. This is unchanged from the same
  note I raised for v3.
* **The doc page is a live URL.** The Python doc page is not revision-pinned (it carries a version
  pin, Python 3.15.1, and a "Last updated" timestamp), so the fragment ids are stable anchors but the
  page bytes can move. The fragment-anchor form is nevertheless strictly more portable than the line
  coordinates it replaces, since the ids are structural rather than layout-dependent.
* **Everything outside the locator is inherited from the v3 PASS and was not re-reviewed**, as
  instructed. The v3 section of this report remains the substantive record for the numbers, the
  falsifiers, the oracle attribution and the equality receipt.
* **Unchanged from earlier sections of this report:** the receipt
  `corpus/evidence/round29-calibration/repair-projection-equality.json` still states its three equality
  assertions without a persisted generator script (the same provenance class `FCritClaimMet.md` D7
  recorded for `mutation-witness.txt`); and the live instrument digest has moved past the frozen
  `135cc682…` while the emitted `--json` digest `a4fb5d6d…` has not, so no candidate-dependent count
  moved.

### 8. Scope note

This verdict covers **only** the numbers and locations in
`.ufo/waves/round-29/drafts/webarena-config-projection.md` at sha256
`c4412f67e0b182c6230215603154271cc469801669c8629a630dfbfd07cfdaf3`, and the canonical landing path
`corpus/knowledge/webarena-config-projection.md`. It is not a round-29 admission, not a claim about
task validity, deployment configuration, model performance, hosted judges or contamination, and it does
not judge the axis scores. The v5 delta is confined to the source header's locator, which is correct:
the invalid-document exception is cited at `#json.load` with `loads`' inheritance carried by its own
"Identical to load()" clause, and the other two anchors match their content exactly. The rest of the
file is byte-identical to the v3 bytes already passed. No defect was found.

VERDICT: PASS
