writer: KengakuR29-2.FMutCategoryShape-2

# FMutCategoryShape: mutation test of changed-leaf category decided by value shape

Seat: KengakuR29-2.FMutCategoryShape-2 (actual writer: this seat). Round 29 post-crash falsify wave. Lane root `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; lane master `56fd949a6478342531e61f4feecb4a685d831640` (`git rev-parse HEAD`, read-only). Lane writes: this report and the scratch dir only; no lane production, fixture, corpus or git state was written. All experiments ran on copies under `/tmp/r29-falsify-FMutCategoryShape-2/`.

## 1. Result (scoped)

- Assigned mutant M1 (category = projected value starts with `http://` or `https://`, instead of the JSON path) **SURVIVED** the instrument's own checks. `--selftest` exit 0 (`SELFTEST clean cases=20`, 599 bytes, byte-identical to control). `--summary` exit 0 (`findings: []`, `TOTAL findings=0 exit=0`).
- **Frozen real data alone cannot detect M1** under the instrument's exit and finding contract. The `--summary` category census changes on 3 lines, and 61 leaf locations per profile (183 leaf-profile records over 18 tasks) change category. No exit code, finding or assertion reads that census. The selftest, which also loads the frozen hand fixtures, is equally blind to M1.
- The discriminating leaves exist in the frozen real data and in the frozen hand fixture `plans/fixtures/r29/hand/url-only.fixture.json`. The only category assertion in the selftest (line 397) is a synthetic 12-leaf case that M1 satisfies by construction.
- Sensitivity variants (not the assigned mutant): M2 (`"://" in after`) and M3 (`before.startswith(...)`) are **killed**, each only by the line-397 assertion. Both summaries still exit 0.
- Control reproduces the author's receipts (section 8).
- Verdict scope: the instrument's tests do not kill this category-shape mutant. That is a test-adequacy failure. No production output is shown to be wrong.

## 2. Target and mutant

Production rule, `plans/config_projection.py` line 314 (inside `audit_text`, changed-leaf loop):

```
"category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",
```

Documented contract, line 38: "Category is strictly the JSON path, never the value shape or the `sites` metadata." (14 words)

M1, one line in the copy `/tmp/r29-falsify-FMutCategoryShape-2/mut/plans/config_projection.py` (hashline edit tool; diff saved as `mutant-m1.diff`):

```
-                                     "category": "url_field" if template(path) in URL_FIELD_TEMPLATES else "non_url_field",
+                                     "category": "url_field" if after.startswith(("http://", "https://")) else "non_url_field",
```

`diff -u` rc 1, one changed line, hunk `@@ -311,7 +311,7 @@`. `after` is the projected string of the changed leaf. Nothing else in the file changed.

Sensitivity variants (same family, one line each; `mutant-m2.diff`, `mutant-m3.diff`):
- M2: `"url_field" if "://" in after else "non_url_field"`
- M3: `"url_field" if before.startswith(("http://", "https://")) else "non_url_field"`

## 3. Method and commands

1. `cp -a` of the lane `plans/` into `/tmp/r29-falsify-FMutCategoryShape-2/base/`. Copies `mut/`, `mut1-recheck/`, `mut2-value-contains-scheme/` and `mut3-raw-value-prefix/` were made from `base/`. A `cp` issued before its target directory existed left a stray top-level duplicate in `mut2-value-contains-scheme/`. It was removed in the same batch as the M2 and M3 runs; those runs read only `plans/`, so the stray files could not affect them.
2. Control runs on `base/`, CPython 3.14.8 via `sys.executable`, subprocess with stdout, stderr and exit captured: `python3 .../base/plans/config_projection.py --root .../base --selftest` (then `--summary`, `--json`).
3. M1 applied to `mut/plans/config_projection.py` line 314 with the edit tool (tag 1E43 to 4EF8).
4. `python3 .../mut/plans/config_projection.py --root .../mut --selftest`, then `--summary`, then `--json`.
5. Comparison: `difflib` on summary text against control. JSON leaves keyed by (profile, output_index, json_pointer). `strip()` removes `category` and `changed_leaves_by_category`, and the stripped documents are compared for equality. Mismatches are control category differing from mutant category.
6. Revert: `cp base/plans/config_projection.py mut/plans/config_projection.py`. Result: sha256 `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3`, and `diff -rq base/plans mut/plans` empty (rc 0).
7. Recheck: fresh `mut1-recheck/` with M1 re-applied (same tag 4EF8). Its `--selftest`, `--summary` and `--json` outputs are byte-identical to step 4 (JSON 3,880,261 bytes, sha256 `8367f8f48b47bb6df08871316d28115ed2624d8a9a2ba53693df7561897dfac4`).
8. Hand fixture: loaded each copy's module from `/tmp` with `importlib` and `sys.dont_write_bytecode = True`, then called `audit_text` on `url-only.fixture.json` values for `distinct_origins`, printing each changed leaf's category. Note: my first M1 hand pass ran in the same batch as the revert and read the reverted file. That output is discarded; the M1 hand result comes from `mut1-recheck/`.
9. Reverted `mut1-recheck/`, `mut2-value-contains-scheme/` and `mut3-raw-value-prefix/` the same way. All five copies have sha `5673405e...` and empty diffs against `base/plans`.

Tooling: nothing installed, updated or upgraded. `~/.omp/agent/RULES.md` was read; stdlib Python sufficed. Used coreutils and read-only git (`rev-parse`, `status`). No pacman, no service restarts, no REA devices. No subagent or labrat was dispatched (contract: no subagents).

Independence: this is a mutation item, not an oracle or re-derivation item. I read `plans/config_projection.py` (read-only, lines 1 to 548 by ranges and grep) to find the rule and the tests. Expected categories are taken from the control run's own output, not from production source.

## 4. Results

| Run | `--selftest` exit; output | `--summary` exit; findings | Category census, each of 3 profiles (changed string leaves) | Leaf records with category differing from control | Verdict |
|---|---|---|---|---|---|
| control (`base/`) | 0; `SELFTEST clean cases=20 ...` (599 B) | 0; `[]` | `{"non_url_field": 61, "url_field": 1355}` | none (reference) | reference |
| **M1 (assigned)** | **0**; identical 599 B | **0**; `[]` | `{"url_field": 1416}` | 183 (61 leaves x 3 profiles) | **SURVIVED** |
| M2 (sensitivity) | 1; AssertionError at line 397 | 0; `[]` | `{"url_field": 1416}` | 183 | KILLED (line 397) |
| M3 (sensitivity) | 1; AssertionError at line 397 | 0; `[]` | `{"non_url_field": 1416}` | 4065 (1355 x 3) | KILLED (line 397) |

Failing assertion for M2 and M3 (traceback in `config_projection.py`, line 397, `in selftest`, `AssertionError`):

`assert record["changed_leaf_count"] == 12 and record["changed_leaves_by_category"] == {"non_url_field": 6, "url_field": 6}`

Why M1 passes line 397: the synthetic values are `http://<host>.invalid:1`. `start_url` projects to `http://.../p`, which is url under M1 as under control. `intent` projects to `see http://...`, which does not start with a scheme, so it is non_url under M1. The 6/6 split is reproduced.

Additional M1 observations:
- Under `--json`, the documents equal control once `category` and `changed_leaves_by_category` are removed (stripped equality True). Both have 4,248 changed-leaf records and `findings: []`.
- Summary diff is 11 lines: a header pair plus three hunks at summary lines 18, 29 and 40. Example: `-PROFILE distinct_origins changed_leaves_by_category={"non_url_field": 61, "url_field": 1355}` becomes `+PROFILE distinct_origins changed_leaves_by_category={"url_field": 1416}`. The path_prefix and trailing_slash_sensitivity lines change the same way. Summary size 6,914 bytes becomes 6,851.
- Per path template, leaf-profile records, control to M1: `start_url` 2436 url to url; `eval.reference_url` 615 url to url; `eval.program_html[].url` 1014 url to url; `eval.reference_answer_raw_annotation` 3 non_url to url; `eval.program_html[].required_contents.must_include[]` 180 non_url to url.
- Control census is path-determined: each path template maps to exactly one category.

## 5. Can frozen real data alone detect M1? No (under the instrument's contract)

- `--summary` on the frozen 812-task input under three profiles exits 0 under M1 with `findings: []`. The only exit signal is `int(bool(findings))` (`audit`, line 359). No finding reads category.
- Uses of category in the lane file (grep `(?i)categor`): line 38 (comment), 314 (decides), 324 (counts), 379 and 380 (print in summary), 397 (the only assertion). Nothing else.
- The real data does carry the discriminator: 61 leaf locations per profile whose path category is `non_url_field` but whose projected value begins with `http://` (section 7). A census-against-path check would flag them. No such check exists.
- Observed consequence: `--summary` prints `exit=0` while its per-profile category census disagrees with the documented path rule for 61 leaves.
- [INFERENCE] The independent oracle that the prereg requires (`plans/round-29-claims.md` lines 79 to 81, "Main compares every required metric") might compare categories and would then catch M1. I did not read or run it (independence), so this is unverified.

## 6. Hand fixture: a second, unasserted witness

`plans/fixtures/r29/hand/url-only.fixture.json` (case `R29-URL-ONLY-UNREAD-METADATA-01`, "Own-work hand case derived from raw task66 metadata"). Changed leaves, distinct_origins profile, control to each variant:

| pointer | path | control | M1 | M2 | M3 |
|---|---|---|---|---|---|
| `/0/start_url` | start_url | url_field | url_field | url_field | **non_url_field** |
| `/0/intent` | intent | non_url_field | non_url_field | **url_field** | non_url_field |
| `/0/eval/reference_answer_raw_annotation` | eval.reference_answer_raw_annotation | non_url_field | **url_field** | **url_field** | non_url_field |

The `intent` value reads "Literal http://reddit.invalid:10102 is task text, not a URL-valued leaf." (9 words). The `reference_answer_raw_annotation` raw value is identical to the real task-66 leaf: `__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter`.

The selftest checks this fixture's projected tasks, changed-leaf paths, occurrence counts and markers (lines 446 to 451). It never checks `category`. Each value-shape variant tested flips at least one leaf here.

[INFERENCE] A category assertion on this fixture would kill M1 and M2. I did not write or run one; that is outside this item.

## 7. Mismatch register: every mismatch

M1 against control: 183 leaf-profile records, which is 61 unique locations x 3 profiles. The location set is the same in every profile (`M1_SAME_LOCATIONS_ACROSS_PROFILES True`). They span 18 distinct tasks. All 183 flip `non_url_field` to `url_field`; none flips the other way.

M2 has the same 183 locations (checked). M3 has 4,065 records, which is 1,355 unique locations x 3: `start_url` 2436, `eval.reference_url` 615, `eval.program_html[].url` 1014. All flip `url_field` to `non_url_field`.

Full registers in the scratch dir, with `original_json` and `projected_json` for every profile:
- `m1-category-mismatches.tsv`: 183 rows
- `m2-category-mismatches.tsv`: 183 rows
- `m3-category-mismatches.tsv`: 4,065 rows
- `m1-unique-mismatch-leaves.tsv`: 61 rows

Projected-value check: for all 61 locations, the distinct_origins projected value equals the raw value with `__REDDIT__` replaced by `http://reddit.invalid:10102` and `__GITLAB__` replaced by `http://gitlab.invalid:10101`. 61 of 61 match, 0 bad.

Legend: output index equals task_id for every row. Pointers are shown in full. The `path` column is `MI` for `eval.program_html[].required_contents.must_include[]` (60 rows) and `RAW` for `eval.reference_answer_raw_annotation` (1 row).

| # | idx=task_id | json_pointer | path | original (raw, exact) |
|---|---|---|---|---|
| 1 | 66 | /66/eval/reference_answer_raw_annotation | RAW | `__REDDIT__/f/books/59396/apple-books-has-a-free-audiobook-of-a-christmas-carol, __REDDIT__/f/books/17445/i-just-finished-reading-the-hobbit-to-my-6-year-old-daughter` |
| 2 | 552 | /552/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/space/134164/scientists-erupt-at-nasa-gutting-funding-for-crucial-venus` |
| 3 | 552 | /552/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/space/134163/virgin-orbit-fails-to-secure-funding-will-cease-operations` |
| 4 | 552 | /552/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/space/134162/nasa-to-name-artemis-2-crew-next-week-the-first-moon` |
| 5 | 552 | /552/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/space/134161/bent-light-in-deep-space-reveals-one-of-the-biggest-black` |
| 6 | 552 | /552/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/space/134160/seti-s-new-machine-learning-algorithm-works-like-google-s` |
| 7 | 553 | /553/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/news/129905/ohio-man-charged-for-using-molotov-cocktails-to-attack` |
| 8 | 553 | /553/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/news/129904/in-a-loss-for-fox-news-judge-allows-dominion-s-defamation` |
| 9 | 553 | /553/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/news/129903/theater-group-sues-to-block-tennessee-s-new-anti-drag-law` |
| 10 | 553 | /553/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/news/129902/andrew-tate-released-from-jail-in-romania-and-placed-under` |
| 11 | 553 | /553/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/news/129901/rare-high-risk-storm-alert-issued-for-parts-of-midwest-and` |
| 12 | 554 | /554/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/movies/128825/scenes-in-film-that-feel-off-or-wrong-in-some-way-and-make` |
| 13 | 554 | /554/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/movies/128824/disney-s-live-action-lilo-amp-stitch-movie-finds-its-lilo-in` |
| 14 | 554 | /554/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/movies/128823/fantastic-four-movie-gets-new-writer-with-avatar-the-way-of` |
| 15 | 554 | /554/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/movies/128822/can-someone-explain-what-made-steven-seagal-so-appealing-for` |
| 16 | 554 | /554/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/movies/128821/ban-on-fetish-sex-depictions-in-film-should-end-australia` |
| 17 | 555 | /555/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/memes/127991/it-do-be-like-that-tho` |
| 18 | 555 | /555/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/memes/127990/thank-you-memers-this-wouldn-t-be-possible-without-you` |
| 19 | 555 | /555/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/memes/127989/if-you-have-no-other-choice` |
| 20 | 555 | /555/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/memes/127988/yes-yes-yes` |
| 21 | 555 | /555/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/memes/127987/shagadelic-baby` |
| 22 | 562 | /562/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/DIY/118903/separate-glued-plastic-parts` |
| 23 | 562 | /562/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/DIY/118923/how-would-you-fix-this-dryer-vent-mess` |
| 24 | 562 | /562/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/DIY/118935/basement-bulkhead-soffit-wall-framing` |
| 25 | 562 | /562/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit` |
| 26 | 562 | /562/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/DIY/118960/attempting-to-move-a-wall-outlet-in-my-basement-a-few-inches` |
| 27 | 562 | /562/eval/program_html/0/required_contents/must_include/5 | MI | `__REDDIT__/f/DIY/118931/afci-outlet-question` |
| 28 | 563 | /563/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/DIY/118903/separate-glued-plastic-parts` |
| 29 | 563 | /563/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/DIY/118923/how-would-you-fix-this-dryer-vent-mess` |
| 30 | 563 | /563/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/DIY/118935/basement-bulkhead-soffit-wall-framing` |
| 31 | 563 | /563/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit` |
| 32 | 563 | /563/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/DIY/118960/attempting-to-move-a-wall-outlet-in-my-basement-a-few-inches` |
| 33 | 564 | /564/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/DIY/118903/separate-glued-plastic-parts` |
| 34 | 564 | /564/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/DIY/118923/how-would-you-fix-this-dryer-vent-mess` |
| 35 | 564 | /564/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/DIY/118935/basement-bulkhead-soffit-wall-framing` |
| 36 | 565 | /565/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/DIY/118903/separate-glued-plastic-parts` |
| 37 | 565 | /565/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/DIY/118923/how-would-you-fix-this-dryer-vent-mess` |
| 38 | 565 | /565/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/DIY/118935/basement-bulkhead-soffit-wall-framing` |
| 39 | 565 | /565/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit` |
| 40 | 565 | /565/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/DIY/118960/attempting-to-move-a-wall-outlet-in-my-basement-a-few-inches` |
| 41 | 565 | /565/eval/program_html/0/required_contents/must_include/5 | MI | `__REDDIT__/f/DIY/118931/afci-outlet-question` |
| 42 | 565 | /565/eval/program_html/0/required_contents/must_include/6 | MI | `__REDDIT__/f/DIY/118824/teflon-tape-to-attach-washing-machine-drain-hose-to-pipe` |
| 43 | 565 | /565/eval/program_html/0/required_contents/must_include/7 | MI | `__REDDIT__/f/DIY/118866/paver-base-for-shed` |
| 44 | 565 | /565/eval/program_html/0/required_contents/must_include/8 | MI | `__REDDIT__/f/DIY/118820/ways-to-locate-our-buried-electrical-service` |
| 45 | 565 | /565/eval/program_html/0/required_contents/must_include/9 | MI | `__REDDIT__/f/DIY/118836/how-to-eliminate-transitions-for-disability-mobility-reasons` |
| 46 | 566 | /566/eval/program_html/0/required_contents/must_include/0 | MI | `__REDDIT__/f/DIY/118903/separate-glued-plastic-parts` |
| 47 | 566 | /566/eval/program_html/0/required_contents/must_include/1 | MI | `__REDDIT__/f/DIY/118923/how-would-you-fix-this-dryer-vent-mess` |
| 48 | 566 | /566/eval/program_html/0/required_contents/must_include/2 | MI | `__REDDIT__/f/DIY/118935/basement-bulkhead-soffit-wall-framing` |
| 49 | 566 | /566/eval/program_html/0/required_contents/must_include/3 | MI | `__REDDIT__/f/DIY/118904/ge-water-heater-pilot-light-won-t-stay-lit` |
| 50 | 566 | /566/eval/program_html/0/required_contents/must_include/4 | MI | `__REDDIT__/f/DIY/118960/attempting-to-move-a-wall-outlet-in-my-basement-a-few-inches` |
| 51 | 566 | /566/eval/program_html/0/required_contents/must_include/5 | MI | `__REDDIT__/f/DIY/118931/afci-outlet-question` |
| 52 | 566 | /566/eval/program_html/0/required_contents/must_include/6 | MI | `__REDDIT__/f/DIY/118824/teflon-tape-to-attach-washing-machine-drain-hose-to-pipe` |
| 53 | 566 | /566/eval/program_html/0/required_contents/must_include/7 | MI | `__REDDIT__/f/DIY/118866/paver-base-for-shed` |
| 54 | 681 | /681/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/eriklindernoren/PyTorch-GAN` |
| 55 | 682 | /682/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/convexegg/chatgpt` |
| 56 | 683 | /683/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/root/metaseq` |
| 57 | 684 | /684/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/byteblaze/cloud-to-butt` |
| 58 | 685 | /685/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/byteblaze/dotfiles` |
| 59 | 686 | /686/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/auth0/angular-storage` |
| 60 | 687 | /687/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/koush/AndroidAsync` |
| 61 | 688 | /688/eval/program_html/0/required_contents/must_include/1 | MI | `__GITLAB__/lahwaacz/arch-wiki-docs` |

## 8. Reference receipts: control reproduction

- Control `plans/config_projection.py` sha256 `5673405e...` equals `corpus/evidence/round29-calibration/mutation-witness.txt` line 1.
- Control `--selftest` exit 0 with `SELFTEST clean cases=20` equals witness line 2.
- Control `--json` sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` (3,881,050 bytes) equals `corpus/evidence/round29-calibration/build-json-sha256.txt`.
- Control `--summary` stdout equals `build-summary.txt` except for the receipt's trailing `exit=0` line. `diff` rc 1, sole difference `48d47 < exit=0`.
- The author's witness lists three mutants (`wrong_order_reversed`, `url_only_substitution`, `index_by_task_id`, lines 3 to 5). None is a category-label mutant. I did not re-run those three; they are outside this item.

## 9. What this adds (novelty)

1. An executed category-label mutant. The author's witness file has none (section 8). Sibling falsify reports reason about value-shape predicates analytically: `FPathRefUrl.md` lines 127 to 129, `FCritForecasts.md` O2, `FPathStartUrl.md` caveat 1. In the sibling reports my grep matched (`categor|value.shape|startswith|url_field`; output was truncated), none reports running a category-label mutant through `--selftest` or `--summary`. [INFERENCE] This claim is bounded by the truncation.
2. The survival is structural. One synthetic assertion (line 397) is the only category check, and the scheme-prefix predicate satisfies it.
3. The real frozen data carries 61 discriminating leaves per profile, and the exit contract never reads them (section 5).
4. Predicate dependence, executed: the scheme-prefix (M1) and `"://"` substring (M2) predicates both give 1,416 url and 0 non_url on the real census. The raw-value prefix (M3) gives 0 url and 1,416 non_url. `FPathRefUrl.md` lines 127 to 129 give an analytic counterfactual of 1,415 url and 1 non_url. That matches a single-URL predicate, not the prefix predicate. I did not execute a single-URL predicate.

## 10. Limitations

- One assigned mutant and two sensitivity variants. Other value-shape predicates were not run. [INFERENCE] Some other predicate may be killed by the line-397 assertion, and some may be killed by none.
- No tests were written, and the lane was not modified. The hand-fixture claims rest on observed categories and on reading lines 436 to 451.
- The independent oracle was not read or run (section 5).
- FAIL applies to this item only: the assigned mutant survived. It is not a round admission.

## 11. Lane notes (observed, not this item)

- `.ufo/waves/round-29/falsify/swarm-registry.json` lines 358 to 361 list this seat with `"role": "executor"`. Flagged for the planner; not changed.

## 12. Files

- Report: `.ufo/waves/round-29/falsify/FMutCategoryShape.md` (this file).
- Scratch: `.ufo/waves/round-29/scratch/falsify/FMutCategoryShape/`. Contents: `base-selftest.stdout.txt`, `base-selftest.stderr.txt`, `base-summary.stdout.txt`, `base-summary.stderr.txt`, `base-json.json-sha256.txt`, `base-json.stderr.txt`; `m1-selftest.stdout.txt`, `m1-selftest.stderr.txt`, `m1-summary.stdout.txt`, `m1-summary.stderr.txt`, `m1-json.json-sha256.txt`, `m1-json.stderr.txt`; `m1r-*` (recheck, same pattern); `m2-*` and `m3-*` (same pattern); `mutant-m1.diff`, `mutant-m2.diff`, `mutant-m3.diff`; `m1-category-mismatches.tsv`, `m2-category-mismatches.tsv`, `m3-category-mismatches.tsv`; `m1-unique-mismatch-leaves.tsv`; `hand-url-only-categories.txt`. JSON stdout files are in `/tmp` (next bullet).
- `/tmp/r29-falsify-FMutCategoryShape-2/`: copies, all reverted. JSON stdout files (about 3.9 MB each) are kept there, not in the lane.
- Lane integrity at end: `plans/config_projection.py` sha256 `5673405e...`; `plans/fixtures/r29/manifest.json` `f6390b92...`; `plans/fixtures/r29/generate_test_data.py` `45ddba7b...`; `plans/fixtures/r29/profiles.json` `90fdc34d...`; `plans/fixtures/r28/webarena/config_files/test.raw.json` `7b50386f...`. All unchanged from the start. `git status --porcelain -- plans` empty. HEAD `56fd949a...`.

VERDICT: FAIL
