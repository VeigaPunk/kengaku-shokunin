writer: KengakuR29-2.FPathHtmlUrl-2

# FPathHtmlUrl — attack on changed-leaf count and JSON-path category at `eval.program_html[].url`

Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; read-only leaf. No production,
fixture, corpus, SOURCES, SCORECARD, candidate, git-index or jj state was written. All
scratch lives under
`.ufo/waves/round-29/scratch/falsify/FPathHtmlUrl/`.

## Independence disclosure

I did **not** read, import or inspect `plans/config_projection.py` source at any point. I ran
it only through its CLI (`--summary`, `--json`, `--selftest`) and treated stdout as the thing
under test. My oracle was derived from
(1) the prereg text `plans/round-29-claims.md` (six sequential global Python-text replacements
in order GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP, then JSON parse; URL-field
set declared by JSON path),
(2) the pinned generator bytes `plans/fixtures/r29/generate_test_data.py` (838 bytes, sha256
`45ddba7b…21cd`, six `raw.replace` statements — e.g. word-count 4 fragment
`raw = raw.replace("__GITLAB__", GITLAB)`),
(3) the pinned data bytes `plans/fixtures/r28/webarena/config_files/test.raw.json` (880776
bytes, sha256 `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`) and
`plans/fixtures/r29/profiles.json` (sha256 `90fdc34d…e018`).

I also re-read `plans/fixtures/r29/manifest.json` (sha256 `f6390b92…bf87`) and confirmed all
four hashes above by `sha256sum`. Lane HEAD = `56fd949a6478342531e61f4feecb4a685d831640`.

## Attack

Target: the instrument's claims for template `eval.program_html[].url` —
`changed_leaves_by_path_template` (338) and its `url_field`/`non_url_field` category split
(1355/61) — plus the per-leaf original→projected values in `--json`. Method: independently
enumerate every leaf at that path in the raw task file, count those containing one of the six
tokens, project every profile by the upstream ordered text replacement, diff decoded leaves,
and compare counts, categories, pointers, values and tokens against instrument output.

## Method (commands, units)

    python3 plans/config_projection.py --summary     # stdout 47 lines, TOTAL findings=0, exit 0
    python3 plans/config_projection.py --json        # 3881050 bytes, findings [], exit 0
    python3 plans/config_projection.py --selftest    # exit 0, "SELFTEST clean cases=20"
    python3 .ufo/waves/round-29/scratch/falsify/FPathHtmlUrl/oracle.py   # independent

Oracle (`oracle.py`, sha256 `31a9e9d2…7cc6`, stdlib only): read raw text once, apply the six
`str.replace` calls in pinned order per profile, `json.loads`, walk every leaf by RFC-6901
pointer, compare `original` vs `projected` for the identical pointer set, and template
array indices as `[]` (task-relative). Category rule taken verbatim from the prereg's declared
field set:
`url_field = start_url, eval.reference_url, eval.program_html[].url; everything else non_url_field, strictly by JSON path`
(whitespace word count 12, computed programmatically).

Units: leaves, token occurrences, leaves-per-profile, tasks. Counts are never pooled across
profiles or occurrences.

## Observed facts (independent census)

- Base file: 812 tasks, 15574 leaves, 10869 string leaves, ASCII, no CR.
- `eval.program_html[]` entries: 651 total, all with a string `url`. Entries per task:
  0→401 tasks, 1→291, 2→57, 3→44, 4→2, 5→9, 6→2, 7→3, 8→1, 10→2.
- Leaves at `eval.program_html[].url`: **651**. Those containing a token: **338**
  (GITLAB 132, REDDIT 85, SHOPPING_ADMIN 90, SHOPPING 31; WIKIPEDIA/MAP 0). Each of the 338
  contains exactly one token occurrence, and in all 338 that occurrence is followed by `/`.
- The other 313 leaves are exactly three shapes and never change: literal `last` (238),
  `func:reddit_get_post_url('__last_url__')` (65), `func:shopping_get_latest_order_url()` (10).
  `__last_url__` is not one of the six env tokens, so leaving it is correct under the claim.
- No token appears in a leaf key, in `program_html[].locator`, in `program_html[].prep_actions`
  or in `required_contents` keys other than `must_include`; my scan over all 812 tasks found
  zero such leaves. (This matters: a token in a key would move a path rather than change a
  value, and a text-based census could miss it.)

## Comparison with instrument output

`--summary` lines 18–19, 29–30, 40–41 (and the same keys in `--json`
`profiles.<profile>.changed_leaves_by_path_template` / `…_by_category`), all three profiles:

| metric | instrument | independent | match |
|---|---|---|---|
| `eval.program_html[].url` changed leaves | 338 ×3 | 338 ×3 | yes |
| `url_field` changed leaves | 1355 ×3 | 1355 ×3 | yes |
| `non_url_field` changed leaves | 61 ×3 | 61 ×3 | yes |
| `changed_leaf_count` | 1416 ×3 | 1416 ×3 | yes |
| per-path dict (5 templates) | 60/338/1/205/812 ×3 | identical ×3 | yes |
| `changed_leaves_with_multiple_occurrences` | 13 ×3 | 13 ×3 | yes |
| `string_leaf_count` | 10869 ×3 | 10869 | yes |
| `projected_text_sha256` | 2aec098e…, 54cf9833…, 49bbee2e… | identical ×3 | yes |

Category arithmetic closes exactly as declared: `url_field` 1355 = 812 (`start_url`) + 205
(`eval.reference_url`) + 338 (`eval.program_html[].url`); `non_url_field` 61 = 60
(`…required_contents.must_include[]`) + 1 (`eval.reference_answer_raw_annotation`). No
template outside the declared three is classed `url_field`.

Mechanical checks against `--json` (all pass, 0 mismatches each):

- 1014 per-leaf records (338 × 3 profiles) compared one-to-one with the oracle on pointer
  set, `original`, `projected`, `category`, `tokens`: pointer sets equal, no duplicate
  pointers, no value mismatch, no category mismatch, no token-list mismatch.
- All 1014 pointers match `^/<i>/eval/program_html/<j>/url$`; `<i>` equals both the enclosing
  task record's `task_id` and `output_index`, and `<j>` is in range of that task's
  `projected_task.eval.program_html`.
- Every `projected_task` object (2436/2436) is deep-equal to my independent projection, and
  each profile's projected `program_html` entry total is 651 (no entry added or dropped).
- The 338 changed leaves sit in 237 distinct tasks; leaves-per-task distribution
  {1:185, 2:32, 3:11, 4:2, 5:4, 8:1, 10:2} (= 338).
- `--summary` and `--json` agree on all compared profile metrics (programmatically checked).

## Sample: 5 changed leaves per profile, re-derived by hand

Pointers are `--json` `json_pointer` values; "hand" = literal `str.replace` of the one token
present in the original by that profile's value, then string compare to the instrument's
`projected`. All 15 hand derivations match; unit for every row is one leaf.

| profile | pointer | original | instrument projected | hand |
|---|---|---|---|---|
| distinct_origins | `/389/eval/program_html/0/url` | `__GITLAB__/primer/design/-/merge_requests/450` | `http://gitlab.invalid:10101/primer/design/-/merge_requests/450` | equal |
| distinct_origins | `/464/eval/program_html/0/url` | `__SHOPPING_ADMIN__/../antonia-racer-tank.html` | `http://shopping-admin.invalid:10104/../antonia-racer-tank.html` | equal |
| distinct_origins | `/574/eval/program_html/0/url` | `__SHOPPING__/customer/address` | `http://shopping.invalid:10103/customer/address` | equal |
| distinct_origins | `/748/eval/program_html/2/url` | `__GITLAB__/byteblaze/web_agent_android_xl/-/project_members` | `http://gitlab.invalid:10101/byteblaze/web_agent_android_xl/-/project_members` | equal |
| distinct_origins | `/811/eval/program_html/0/url` | `__GITLAB__/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | `http://gitlab.invalid:10101/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | equal |
| path_prefix | `/389/eval/program_html/0/url` | as above | `http://gitlab.invalid:10201/prefix/primer/design/-/merge_requests/450` | equal |
| path_prefix | `/464/eval/program_html/0/url` | as above | `http://shopping-admin.invalid:10204/prefix/../antonia-racer-tank.html` | equal |
| path_prefix | `/574/eval/program_html/0/url` | as above | `http://shopping.invalid:10203/prefix/customer/address` | equal |
| path_prefix | `/748/eval/program_html/2/url` | as above | `http://gitlab.invalid:10201/prefix/byteblaze/web_agent_android_xl/-/project_members` | equal |
| path_prefix | `/811/eval/program_html/0/url` | as above | `http://gitlab.invalid:10201/prefix/dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | equal |
| trailing_slash_sensitivity | `/389/eval/program_html/0/url` | as above | `http://gitlab.invalid:10301//primer/design/-/merge_requests/450` | equal |
| trailing_slash_sensitivity | `/464/eval/program_html/0/url` | as above | `http://shopping-admin.invalid:10304//../antonia-racer-tank.html` | equal |
| trailing_slash_sensitivity | `/574/eval/program_html/0/url` | as above | `http://shopping.invalid:10303//customer/address` | equal |
| trailing_slash_sensitivity | `/748/eval/program_html/2/url` | as above | `http://gitlab.invalid:10301//byteblaze/web_agent_android_xl/-/project_members` | equal |
| trailing_slash_sensitivity | `/811/eval/program_html/0/url` | as above | `http://gitlab.invalid:10301//dashboard/issues?scope=all&state=opened&assignee_username=byteblaze` | equal |

The doubled `/` in the trailing-slash rows is the discriminating evidence that no URL
normalisation or escaping repair happens on this path: the profile value already ends in `/`
and the raw leaf continues with `/`, and the instrument emits both slashes verbatim.

Raw-bytes binding for the sampled originals: each sampled value occurs **only** at
`eval.program_html[].url` leaves, and its raw-text JSON-encoded occurrence count equals its
leaf count: `…450` 1/1, `…tank.html` 1/1, `__SHOPPING__/customer/address` 10/10 (ten distinct
leaves, one occurrence each — not one leaf with ten occurrences), `…project_members` 1/1,
`…dashboard/issues…` 3/3. No sampled value needed decoding repair.

## Mismatches

**None.** No count, category, pointer, token list, per-leaf value or per-task object at
`eval.program_html[].url` diverged from the independent re-derivation, in any of the three
profiles.

## Non-mismatch observations and limits of this check

- The 60 changed `must_include[]` leaves are URL-shaped after projection (e.g.
  `__REDDIT__/f/space/134164/…` → `http://reddit.invalid:10102/f/space/134164/…`), yet are
  `non_url_field`. That is exactly what the prereg's declared strict-path rule requires, so it
  is consistent, not a defect. [INFERENCE] A value-based classifier (is the projected string a
  URL?) would instead report 1415 url_field / 1 non_url_field; that alternative was not run,
  only derived by arithmetic from the observed 60/1 split.
- Test power: this path has zero multi-occurrence leaves (all 13 multi-occurrence leaves are
  at `eval.reference_url` 7, `start_url` 5, `eval.reference_answer_raw_annotation` 1;
  1435 occurrences − 1416 leaves = 19 extra occurrences), so at this path a leaf count and an
  occurrence count coincide at 338. This item therefore cannot distinguish leaf-vs-occurrence
  counting; the discriminating evidence is on the sibling paths, whose 323/275 by-token leaf
  counts I also reproduced exactly.
- On this frozen input `output_index == task_id` for all 812 items, so the pointer's first
  component cannot be told apart from `task_id` from output alone; I verified it equals both,
  and the instrument's own `--selftest` (exit 0, cases=20, includes the shuffled-index hand
  case) is the only evidence about the separated case. That is instrument-internal and not
  independently re-verified here.
- `--selftest` exit 0 is the instrument checking itself; I ran it once for completeness and do
  not count it as independent verification.
- Scope of this pass: it covers the changed-leaf count, the category split and the per-leaf
  original→projected values for this one template. `--json`'s `findings: []` is not evidence
  for those; the equality checks above are. Exit code was 0 in all three modes.
- No tool was installed or updated (nothing needed; python3 stdlib sufficed, pacman paused).

Witness hashes (scratch): `summary.json` `c8da0c5a…4630`, `summary.txt` `5ce5cb0f…636f`,
`oracle.py` `31a9e9d2…7cc6`, `oracle_counts.json` `efbff928…78d6`, `oracle_ph.json`
`84848dca…c9a`.

VERDICT: PASS
