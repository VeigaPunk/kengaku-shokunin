writer: KengakuR29-2.FPathMustInclude-2

# FPathMustInclude — changed-leaf count and JSON-path category at `eval.program_html[].required_contents.must_include[]`

Seat: KengakuR29-2 (post-crash falsify wave, fresh identity). Item attacks the summary/JSON metrics
`changed_leaves_by_path_template` and `changed_leaves_by_category` for exactly one template against an
independent raw-leaf census and an independent projection. Read-only leaf; no subagents; every write below
is confined to `.ufo/waves/round-29/scratch/falsify/FPathMustInclude-2/` plus this report.

## Independence statement

I did NOT read, import, grep or execute any source of `plans/config_projection.py`. I ran it only through
its documented CLI (`--summary`, `--json`) and treated stdout as an opaque artifact. All re-derivations use
the prereg TEXT (`plans/round-29-claims.md`), the pinned generator bytes, the pinned raw JSON and
`plans/fixtures/r29/profiles.json`. No network, no REA/MCP devices, no pacman, no tool installs; stdlib
python3 3.14.8 only.

## Pinned inputs (observed, sha256 recalculated)

| file | sha256 |
|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` (880,776 bytes) | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` |
| `plans/fixtures/r29/generate_test_data.py` (838 bytes) | `45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd` |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` |
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` |

Lane HEAD `56fd949a6478342531e61f4feecb4a685d831640`; last commit touching the instrument
`b98dcf317b6c50179ac5c70b6ba3dacc7e2976fe` (2026-10-21T13:39:10-03:00). Pins match the manifest entries.
Generator lines 11-16 perform the six ordered `raw.replace` calls; line 20 parses the projected text.
Raw parses to 812 task objects, 10,869 string leaves.

## Commands run (lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`)

| # | command | observed result |
|---|---|---|
| 1 | `python3 plans/config_projection.py --summary` | exit 0; 6,914-byte stdout; sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f`; line 47 `TOTAL findings=0 exit=0` |
| 2 | `python3 plans/config_projection.py --json` | exit 0; 3,881,050-byte stdout; sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` |
| 3 | `python3 .ufo/.../FPathMustInclude-2/enumerate.py` | independent leaf census (below) |
| 4 | `python3 .ufo/.../FPathMustInclude-2/compare.py` | full 2,436 projected objects + 32,607 leaf pairs (10,869 x 3); `MISMATCHES 0` |
| 5 | `python3 .ufo/.../FPathMustInclude-2/mustinclude.py` | template census + per-profile record comparison |
| 6 | `python3 .ufo/.../FPathMustInclude-2/sample.py` | 5 leaves x 3 profiles hand re-derivation |
| 7 | `python3 .ufo/.../FPathMustInclude-2/prov.py` | occurrence-provenance offsets |
| 8 | summary-vs-json and junction scripts (same scratch dir) | zero delta |

## A1 — Raw census at this template (independent)

Walked the parsed raw object, treating every scalar as a leaf and normalising every list index to `[]`
(template `eval.program_html[].required_contents.must_include[]`).

- 815 string leaves exist at the template (463 non-empty `must_include` lists under 651
  `required_contents` dicts; 188 `program_html` entries have no `must_include`; all 815 values are str).
- 60 leaves contain a token: `__REDDIT__` 52, `__GITLAB__` 8, the other four tokens 0. Occurrences at the
  template are also 60; every token-bearing leaf holds exactly 1 occurrence and 0 leaves hold >1.
- The 60 leaves live in 17 tasks: `{552:5, 553:5, 554:5, 555:5, 562:6, 563:5, 564:3, 565:10, 566:8,
  681:1, 682:1, 683:1, 684:1, 685:1, 686:1, 687:1, 688:1}`. REDDIT = tasks 552-566 (52 leaves),
  GITLAB = tasks 681-688 (8 leaves).
- 60 distinct concrete JSON pointers `/task/eval/program_html/j/required_contents/must_include/k`.
- After source-faithful projection (ordered text replace then `json.loads`) all 60 leaves change in each
  of the 3 profiles = 180 changed task/profile leaf rows. The changed pointer set is identical across all
  three profiles (1,416 pointers each), and each leaf's original/projected pair differs per profile.

## A2 — Instrument values compared

`--summary` lines 18/19 (distinct_origins), 29/30 (path_prefix), 40/41 (trailing_slash_sensitivity) all
report `eval.program_html[].required_contents.must_include[]": 60`, `non_url_field: 61`, `url_field: 1355`,
`changed_leaf_count=1416`. `--json` per-profile `changed_leaves_by_path_template` and
`changed_leaves_by_category` are byte-identical across profiles and equal to the summary; parsed comparison
of summary vs JSON returned zero mismatches.

Independent totals per profile (all three): `must_include[] 60`, `program_html[].url 338`,
`reference_answer_raw_annotation 1`, `reference_url 205`, `start_url 812`; categories
`non_url_field 61`, `url_field 1355`; changed leaves 1,416; occurrences 1,435; multi-occurrence leaves 13.

Category arithmetic checks: `url_field 1355 = start_url 812 + reference_url 205 + program_html.url 338`;
`non_url_field 61 = must_include 60 + reference_answer_raw_annotation 1`; total `1,416 = 1,355 + 61`.
Every one of the 60 `must_include` rows in `--json` carries `category: non_url_field`, matching the declared
strict-by-JSON-path rule. All 2,436 `projected_task` objects are deep-equal to my independent parse; every
`changed_leaves` row matches my pointer, original and projected string; per-profile `projected_text_sha256`
matches my full-text sha256 (`2aec098e…`, `54cf9833…`, `49bbee2e…`).

## A3 — Five sampled changed leaves, hand re-derived per profile

Selected from `--json` (`sample.py`): three at the target template, one `program_html[].url`, one
multi-occurrence annotation. For each I read the raw-file codepoint offset, applied the ordered token
replacement by hand, and compared with `--json` `original`/`projected` and with the projected parse.
15/15 matched (original match, projected match, parsed-value match, template match, category match).

```
S1 /552/eval/program_html/0/required_contents/must_include/0  raw offset 522329
   original: __REDDIT__/f/space/134164/scientists-erupt-at-nasa-gutting-funding-for-crucial-venus
   distinct_origins: http://reddit.invalid:10102/f/space/134164/scientists-erupt-at-nasa-gutting-funding-for-crucial-venus
   path_prefix:      http://reddit.invalid:10202/prefix/f/space/134164/scientists-erupt-at-nasa-gutting-funding-for-crucial-venus
   trailing_slash:   http://reddit.invalid:10302//f/space/134164/scientists-erupt-at-nasa-gutting-funding-for-crucial-venus
S2 /565/eval/program_html/0/required_contents/must_include/3  raw offset 536324
   original: __REDDIT__/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit
   distinct_origins: http://reddit.invalid:10102/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit
   path_prefix:      http://reddit.invalid:10202/prefix/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit
   trailing_slash:   http://reddit.invalid:10302//f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit
S3 /688/eval/program_html/0/required_contents/must_include/1  raw offset 701228
   original: __GITLAB__/lahwaacz/arch-wiki-docs
   distinct_origins: http://gitlab.invalid:10101/lahwaacz/arch-wiki-docs
   path_prefix:      http://gitlab.invalid:10201/prefix/lahwaacz/arch-wiki-docs
   trailing_slash:   http://gitlab.invalid:10301//lahwaacz/arch-wiki-docs
S4 /389/eval/program_html/0/url  raw offset 353887
   original: __GITLAB__/primer/design/-/merge_requests/450
   distinct_origins: http://gitlab.invalid:10101/primer/design/-/merge_requests/450
   path_prefix:      http://gitlab.invalid:10201/prefix/primer/design/-/merge_requests/450
   trailing_slash:   http://gitlab.invalid:10301//primer/design/-/merge_requests/450
S5 /66/eval/reference_answer_raw_annotation  raw offset 61888 (2 occurrences)
   original: __REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter
   distinct_origins: http://reddit.invalid:10102/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10102/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter
   path_prefix:      http://reddit.invalid:10202/prefix/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10202/prefix/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter
   trailing_slash:   http://reddit.invalid:10302//f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, http://reddit.invalid:10302//f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter
```

The `//` in the trailing-slash column is the declared stimulus (token followed by `/`), not a projection
error; `--summary` records 697 such junctions globally for that profile.

## A4 — Discriminating checks beyond the headline number

1. **Leaf counting vs value dedup.** The 60 token-bearing leaves hold only 38 distinct strings: 8 duplicate
   groups covering 30 leaves, all in tasks 562-566 (group sizes 5,5,5,4,4,3,2,2). A distinct-value census
   would report 38 changes and REDDIT 30, not 52. The instrument reports 60 and 52, i.e. it counts leaf
   positions, and its per-task records do list every duplicate pointer separately. This is the sharpest
   discriminating test in this item; the count is not an artifact of set semantics.
2. **The key name is ambiguous across two paths.** `must_include` occurs as a key 639 times: 463 under
   `eval.program_html[].required_contents` (815 string leaves) and 176 under `eval.reference_answers`
   (396 string leaves, 176 tasks). The latter holds 0 tokens, so a bare-key census would still yield 60
   changed; only the full template is path-faithful. Task 66 shows the two paths can disagree in value:
   its `eval.reference_answers.must_include` holds two hard-coded `http://www.reddit.com/...` URLs that are
   byte-identical in all three projected profiles, while its annotation is rewritten to reddit.invalid.
3. **`url`-named keys.** Leaf templates whose last key is `url`/`*_url`: `start_url` 812 (812 token-bearing),
   `eval.reference_url` 812 (805 str + 7 null; 205 token-bearing), `eval.program_html[].url` 651 (338
   token-bearing), `instantiation_dict.url` 5 (0 token-bearing). No token-bearing leaf exists outside the
   three declared `url_field` templates, so the declared url/non-url partition is exhaustive for changed
   leaves on this input; the "everything else" clause is exercised only by the 60 `must_include` and 1
   annotation leaves.
4. **Slash-junction decomposition.** The profile's `tokens_followed_by_slash=697` decomposes by template as
   `must_include 60 + program_html.url 338 + reference_url 217 + annotation 2 + start_url 80 = 697`
   (all 60 must_include occurrences are token-then-`/`). Raw text contains 23 `//`; projected `//` counts are
   1,458 / 1,458 / 2,155 = 23 + 1,435 occurrences, with the trailing profile adding the 697 junctions.
   This independently confirms the aggregate stimulus number and attributes 60 of it to this template.
5. **Leaf vs occurrence units.** Globally 1,416 changed leaves vs 1,435 occurrences; the 19-occurrence gap
   is the 13 multi-occurrence leaves (start_url 5, reference_url 7, annotation 1). At this template leaf
   count equals occurrence count (60 = 60; `program_html[].url` also 338 = 338), so the template number must
   not be read as an occurrence count in general even though they coincide here.
6. **Provenance.** 60 `occurrence_provenance` entries at this template (52 REDDIT, 8 GITLAB); every
   `json_pointer` resolves to a leaf containing its token; every `original_input_codepoint_offset` slices
   the token exactly in the raw text; the full 1,435-entry offset/token multiset equals the independently
   enumerated raw-text occurrence multiset (0 slice or role mismatches; role `value` for all).

## Category caveat (observed, not a numeric mismatch)

Under the declared rule the classification is exactly path-based, and it matches: `non_url_field` = the 60
template leaves + 1 annotation. But 61/61 `non_url_field` leaves are URL-valued strings after projection,
and 1,416/1,416 changed originals start with a token; the category axis therefore carries no value-shape
information on this input. Read as path membership the metric is correct; read as value semantics the
prereg F3 phrase "global replacement changes at least one non-URL-valued field" is unsupported. This
corroborates sibling findings (FCase452, FCase811) rather than adding a delta. Also, with frozen data the
exact declared path set cannot be distinguished from a looser rule such as a `url` substring test, because
no changed leaf lies at a url-named path outside the declared three; both rules would emit the same output.

## Mismatches found

**None.** Zero deltas on every check: template count 60 vs independently 60 (x3 profiles); category
61/1,355 vs 61/1,355 (x3); totals 1,416 (x3); 0/2,436 differing task records; 0/4,248 differing changed-leaf
rows (1,416 x 3); 0/15 sample derivations differing; 0/60 provenance rows differing; junction total 697 vs 697;
summary-vs-JSON mismatches 0.

## Remaining unknowns / [INFERENCE]

- [INFERENCE] Because I deliberately did not inspect the instrument implementation, equality here is
  established at CLI-output level only; I cannot state how its internals derive these numbers, only that
  their published values are reproduced exactly.
- [INFERENCE] The duplicate-value and second-`must_include`-path facts are properties of the frozen raw
  input, not of the instrument; they bound what the 60 can be read to mean (leaf positions under the
  `program_html` path only).
- Projected output still contains hard-coded, non-token real hosts inherited from the raw file (for example
  `www.reddit.com`, `web.cmoa.org`, `pages.gitlab.io`, `www.apache.org`, and an `ssh://` repository URL).
  Faithful token substitution leaves them untouched; this is outside the declared token-projection claim
  but is a scope boundary a reader of the projected config should not miss.
- No statement about runtime, deployment, task validity, model performance or contamination; profile values
  are synthetic `*.invalid` stimuli as declared.

VERDICT: PASS
