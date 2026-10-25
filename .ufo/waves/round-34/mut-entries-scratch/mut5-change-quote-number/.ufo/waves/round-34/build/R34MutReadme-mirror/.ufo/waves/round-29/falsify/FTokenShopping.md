writer: KengakuR29-2.FTokenShopping-2
item: attack the `__SHOPPING__` census of `plans/config_projection.py`
lane root: /home/vgpnk/Projects/shokunin/kengaku-shokunin
base: lane master 56fd949a6478342531e61f4feecb4a685d831640 (read-only; no lane writes)
scratch: `.ufo/waves/round-29/scratch/falsify/FTokenShopping/`

## Independence statement (required)

I did **not** read or import `plans/config_projection.py` source. I derived every number from
the prereg text (`plans/round-29-claims.md`), the pinned generator bytes
(`plans/fixtures/r29/generate_test_data.py`), `profiles.json`, `manifest.json`, the raw
`test.raw.json`, and the instrument's **CLI stdout only** (`--summary`, `--json`, `--selftest`).
I ran `sha256sum` on the instrument file for pin identity; that is not a content read.
No linters/formatters were run. No packages were installed or upgraded (nothing needed).

## Commands (all from lane root unless noted)

| command | result |
|---|---|
| `python3 plans/config_projection.py --summary` | exit 0, `TOTAL findings=0 exit=0` |
| `python3 plans/config_projection.py --json > .../instrument.json` | exit 0, 3,881,050 bytes, sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` |
| `python3 plans/config_projection.py --selftest` | exit 0, `SELFTEST clean cases=20 …` |
| `sha256sum test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652`, 880,776 bytes = 880,776 chars (ASCII, 0 CR) |
| `python3 .../scratch/falsify/FTokenShopping/census.py` | own str.count + find-loop + leaf walk + own sequential projection |
| `python3 .../seams.py` | provenance↔leaf attribution, junction/marker/oracle seams |
| `python3 .../consistency.py` | summary↔JSON cross-path equality for every scoped line |

Pin identity observed: instrument sha256 `5673405e79a0445c76f3e67e2e30ccf7a89847e90de4a74488b995540cea12e3` and
candidate `7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc` both equal `candidate-freeze-v1.json`; manifest file sha256
`f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87`, generator
`45ddba7be49096a18919b4122a8945ff74c292ba17e36892b16e176a8bd921cd`, profiles
`90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018`, raw
`7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` all equal their manifest cells and the instrument's embedded values.

## Census result: independent vs instrument (distinct_origins profile; identical for all 3)

| unit | my independent value | `--summary` / `--json` | verdict |
|---|---|---|---|
| literal `__SHOPPING__` occurrences in raw text | **281** (`str.count`; find-loop advancing 1 char: also 281) | `ORIGINAL_OCCURRENCES_BY_TOKEN["__SHOPPING__"]` = **281** (s1.txt:9; JSON `population`) | match |
| tasks carrying it | **192** (decoded-leaf task set; equals raw-task set, no key occurrences) | `TASKS_WITH_TOKEN` = **192** (s1.txt:10) | match, and **set-equal** (`symdiff []`) |
| decoded leaves carrying it | **275** (10869 total string leaves, equal to instrument `string_leaf_count`) | `changed_leaves_by_token["__SHOPPING__"]` = **275** (s1.txt:20) | match; pointer-set and per-task multiplicity equal (distinct_origins), full-object identity (all 3) |
| applied replacements / profile | **[GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133]** each of 3 profiles | same six values (s1.txt:16, and `path_prefix`/`trailing_slash_sensitivity`) | match |
| changed tasks by token / profile | **192** | `changed_tasks_by_token["__SHOPPING__"]` = **192** (s1.txt:21) | match; task set equal (distinct_origins), counts equal (all 3) |
| `__SHOPPING__` leaves by template | start_url **192**, `eval.reference_url` **52**, `eval.program_html[].url` **31** (sum 275) | leaf-template totals for all tokens match exactly (`template_match_exact True`) | match |

Per-profile projected text digests from my own six sequential `str.replace` calls over the
original text equal the instrument byte-for-byte: `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4`,
`54cf98337dc6751d9453ee069ff26bb3836698518527cf8683c85bf66744744b`,
`49bbee2e827791b79f42858ac78637704adaa7e36f1cb3a9268563e8df3e01b2`. Stronger: for all **2436** task/profile
projections my decoded objects equal the instrument's `projected_task` objects
(`objects 812 812 IDENTICAL` ×3). Exit-0 census is therefore reproduced, not just totals.

### Unit arithmetic closes exactly

- occurrences 281 = leaves 275 + **6** duplicated-in-leaf occurrences; exactly **5** leaves hold
  ≥2: `/431/start_url` = 3, `/432..435/start_url` = 2 each ⇒ (3−1)+4·(2−1) = 6.
- per-task occurrence distribution **{1:114, 2:68, 3:9, 4:1}** ⇒ tasks 114+68+9+1 = **192**,
  occurrences 114+136+27+4 = **281**; max 4 occurrences (task 431 = 3 in `start_url` +
  1 in `eval.program_html[0].url`).
- across all tokens: 1435 raw occurrences − 1416 changed leaves = **19** extras =
  13 `__REDDIT__` + 6 `__SHOPPING__`; leaves with ≥2 occurrences = **13** = 8 + 5, equal to the
  instrument's `changed_leaves_with_multiple_occurrences=13`. No pooling of units observed.
- `TASKS_WITH_TOKEN` sums to 834 over 812 tasks: **834 − 812 = 22** tasks carry two distinct
  tokens; 790 carry exactly one; union = all 812.

### Overlap / substring logic (`__SHOPPING__` vs `__SHOPPING_ADMIN__` and others)

- No token is a substring of another: `"__SHOPPING__" in "__SHOPPING_ADMIN__"` is **False**
  (`SHOPPING__` vs `SHOPPING_A`), so the generator's `__SHOPPING__`-before-`__SHOPPING_ADMIN__`
  order cannot cascade on this text. Regex family count `__SHOPPING\w*__` yields
  `{__SHOPPING_ADMIN__: 300, __SHOPPING__: 281}` — two disjoint families.
- No single decoded leaf holds two distinct token types (`mixed_token_leaves 0`, max 1 per leaf),
  so `changed_leaves_by_token` cannot double-attribute a leaf.
- Task level: `__SHOPPING__` ∩ `__SHOPPING_ADMIN__` = **0** (192 / 182 both target-only);
  `__SHOPPING__` ∩ `__REDDIT__` = **5** (in different leaves, since no leaf is mixed); all other pairs 0.
- My own projection with the SHOPPING/ADMIN pair order swapped, and with the **full six-step
  order reversed**, produce the identical digest `2aec098e5705c98c7f7977a4eb8962aa455c2224d078dbfe4c1fc113e7c707f4` — order is inert on this
  population only because neither value string nor any token contains another token.
- Case/variant scan: lowercase forms 0; bare `SHOPPING` = 581 = 281 + 300 exactly.
- All 281 provenance offsets verify: they index literal text, are unique, ascending, in bounds
  (min 20068, max 862731), `string_role` = `value` for 281/281, and rows-per-pointer equals my
  leaf-occurrence census. Decoded-dict keys containing a token: **0**. `__last_url__` 65 and
  `__page__` 12 reproduced; tokens followed by `/` = **697** (SHOPPING share 110) = trailing-slash
  profile `value_slash_then_raw_slash_junctions=697`.

## Mismatches found

**No numeric mismatch in any scoped line.** One representational difference, and two defects of my own harness:

1. `INDEX`: summary prints `{"index_equals_task_id": 812, "violations": 0}` (s1.txt:13) while
   JSON prints `{"index_equals_task_id": 812, "output_index_rule": "enumerate position",
   "violations": []}` — 0 vs empty list, plus one extra descriptive key. Count identical (0).
2. Not an instrument difference: my first comparator omitted zero-valued map keys
   (`__WIKIPEDIA__: 0`) and my first path-template function emitted a leading `[].` root prefix.
   After fixing both, every scoped comparison is exact (`summary_vs_json_mismatches` drops to
   the INDEX shape above; `template_match_exact True`; task/leaf sets equal with `symdiff []`).

## Determinism / repeatability (attacked, held)

- `--summary` stdout sha256 `5ce5cb0f91ad279d446a475de757b9aa4a5b67a4b02df8d9aeac0d01be74636f` identical across: default env,
  `PYTHONHASHSEED=12345`, and `LC_ALL=C PYTHONHASHSEED=0`.
- `--json` under `PYTHONHASHSEED=12345` yields the same digest
  `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, which also equals `build-json-sha256.txt` and the freeze cell.
- `corpus/evidence/round29-calibration/build-summary.txt` (48 lines) matches today's `--summary`
  on all 47 instrument lines; `diff` reports only the receipt's appended shell line `exit=0`.
  `build-selftest.txt` likewise matches the `SELFTEST clean cases=20 …` line with the same
  appended `exit=0`.

## Negative controls on `/tmp` copies (census cannot be silently rebound)

Copied `plans/config_projection.py` + `plans/fixtures` to `/tmp/r29shop*`; lane untouched
(`git rev-parse HEAD` still `56fd949a6478342531e61f4feecb4a685d831640`; only my report and
scratch dir were created under the lane).

| tamper | output | exit |
|---|---|---|
| one `__SHOPPING__` → `__SHOPPINGX__` in raw | `FINDING {"id": "snapshot_tampered", "path": ".../test.raw.json"}` | 2 |
| generator SHOPPING/ADMIN replace lines swapped | `snapshot_tampered generate_test_data.py` | 2 |
| `profiles.json` SHOPPING origin altered | `snapshot_tampered profiles.json` | 2 |
| raw tampered **and** manifest raw-sha rewritten coherently | `FINDING {"id": "manifest_tampered"}`, no census emitted | 2 |

The last control is the direct attack on the claim that coherent rebinding cannot bless a new
population: it is refused before any census line is printed.

## Residual unknowns / limits of this attack

- Because the instrument reads only pinned bytes and refuses rebinding, I could not feed it
  synthetic text to probe prefix/multi-token behavior. On this population a hypothetical
  `__SHOPPING__`/`__SHOPPING_ADMIN__` confusion would be undetectable from data alone (no leaf
  holds both, and neither token is a substring of the other); its printed selftest case names
  (`six_tokens_and_non_url_field`, `units_not_pooled`) claim hand coverage that I did not verify
  — verifying it would require reading the production source, which independence forbids.
- `changed_leaves_with_multiple_occurrences=13` cannot distinguish "leaves with ≥2 occurrences of
  one token" from "leaves with ≥2 occurrences overall" here, because no leaf is mixed; both
  readings give 13. Not a mismatch, an ambiguity the frozen data cannot resolve.
- [INFERENCE] "Every occurrence is inside a string value, none in keys/structural text": keys
  with tokens = 0 (observed) and valid JSON cannot contain those literals outside strings
  (observed `json.loads` success); the claim itself is the instrument's, not independently
  re-derived beyond that.
- Scope: only the `__SHOPPING__` census and the scoped summary lines. I make no statement about
  other tokens beyond the overlap arithmetic above, and none about the candidate's admission.

VERDICT: PASS
