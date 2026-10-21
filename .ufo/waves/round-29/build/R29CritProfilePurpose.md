# R29CritProfilePurpose — adversarial attack on profile purpose (prefix / trailing-slash stimuli)

- Seat: R29CritProfilePurpose (critic, read-only leaf). Actual writer: `KengakuR28.R29CritProfilePurpose-2`.
- Date: 2026-10-21. Scope: round-29 prereg `31934e5660f1814326c6472eefdfa0c41e642a2f`, C1 only. No code/production edits, no delegation, no tool installs.
- Author-side critique, not outside closure. It does not recheck r28 admission (operator-reported ground truth).
- Scratch (own): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29CritProfilePurpose/census.py` (sha256 `6c7f4279…88ca4`), `quotes.py` (sha256 `919f4b0b…b2d1e`). Neither imports or executes upstream code. The evaluator and helper control flow is hand-transcribed and applied only to synthetic `*.invalid` strings.

## Inputs (sha256 observed this run)

| input | sha256 |
|---|---|
| `plans/fixtures/r28/webarena/config_files/test.raw.json` | `7b50386fd69163dbc05d615d834df4c6ed2c35596e97a1b10d17451c02537652` (matches manifest) |
| `plans/fixtures/r29/profiles.json` | `90fdc34d2f33e3100a2223fdaf5fc5f1016993b8e6723710cc4661e0da94e018` (matches manifest) |
| `plans/fixtures/r29/manifest.json` | `f6390b924c69f0cc8c47b2320b092060bb344b6a5e81c0075d3eb5aab817bf87` (matches assignment) |
| `.ufo/waves/round-28/scratch/OpenTasks/pinned-README.md` | `081c826497f9b7da4952771ee128c2215ec3532379db0fe9f7fcbd899d9c9287` |

The README file's sha256 equals the value recorded in `.ufo/waves/round-29/scratch/KengakuR28.R29SourceWorkflow-2/README.meta.json` for `https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md`, accessed 2026-10-21. That scout's `README.raw.bin` disappeared from its scratch between my listings, so I quote the byte-identical round-28 copy. I made no endpoint requests.

Evaluator source used as data only: `plans/fixtures/r28/webarena/evaluation_harness/{evaluators.py,helper_functions.py}`.

## Commands and output

1. `python3 .ufo/waves/round-29/scratch/R29CritProfilePurpose/census.py`. Units are labelled in the output:
   - SHOPPING_ADMIN first path segment after `__SHOPPING_ADMIN__/` (occurrences): catalog 61, sales 24, review 12, reports 10, `..` 5, cms 5, sales_rule 5, admin 2; total 125.
   - `distinct purpose strings 1 of 3`.
   - distinct_origins: tasks=812, non-scheme `//` occurrences 0.
   - path_prefix: tasks=812, non-scheme `//` occurrences 0.
   - trailing_slash_sensitivity: tasks=812, non-scheme `//` occurrences 697 in 462 tasks.
     - By leaf path: start_url 80, eval.reference_url 217, eval.reference_answer_raw_annotation 2, eval.program_html.[].url 338, eval.program_html.[].required_contents.must_include.[] 60.
   - URL-match outcome against a slash-collapsed copy of the first reference (synthetic prediction; reference_url tasks):
     - distinct_origins: zero on 0/206.
     - path_prefix: zero on 0/206.
     - trailing_slash_sensitivity: zero on 205/206.
   - Hand-transcribed `reddit_get_post_url` control flow on `<REDDIT>/f/space/134164/x/-/comment/1`:
     - distinct_origins: NORMALIZED.
     - path_prefix: UNCHANGED.
     - trailing_slash_sensitivity: UNCHANGED.
     - Raw tasks mentioning that helper: 55.
2. Earlier inline census (same session), counting what follows and precedes each placeholder in the raw text:
   - Following character is only `"` or `/`:
     - GITLAB 385 (`/` 225)
     - REDDIT 336 (`/` 232)
     - SHOPPING 281 (`/` 110)
     - SHOPPING_ADMIN 300 (`/` 125)
     - WIKIPEDIA 0
     - MAP 133 (`/` 5)
   - Placeholders followed by `/` total 697. The raw text has 0 non-scheme `//`.
   - 19 placeholders are preceded by a space. They are all separators: ` |AND| `, ` |OR| `, `, `.
3. `python3 .ufo/waves/round-29/scratch/R29CritProfilePurpose/quotes.py`: 14/14 quotes `OK` verbatim on the cited line, with whitespace-split word counts as shown below. It also reported:
   - Claims `neutral` occurrences: 1 (line 13). `sensitivity` occurrences: 3.
   - Prereg commit subject: `round-29: freeze generated-config projection claim and neutral profiles`.
   - README `export` lines 86–92: 7 values. None ends with `/`, and 2 have a path after the port.
   - Bounded witness:
     - task 374: url_match(reference, single-slash prediction) = 1.0 for distinct_origins and path_prefix, and 0.0 for trailing_slash_sensitivity.
     - task 464 program_html url projects to `…:10104/../antonia-racer-tank.html` (distinct_origins), `…:10204/prefix/../…` (path_prefix) and `…:10304//../…` (trailing_slash_sensitivity).

## Strongest actual objection

The prereg calls all three profiles "neutral", but the frozen data does not encode which one is the baseline and which ones are sensitivity stimuli. Against the workflow's own documented environment-value shape, the "neutral" origin-only profile is not the conforming one.

- `plans/round-29-claims.md:13` (6 words): "neutral substitution profiles (2436 task/profile projections)". The `:31` line (8 words) recasts two of them as sensitivity stimuli: "own-work profiles.json: distinct origins, path-prefix sensitivity, trailing-slash sensitivity."
- All three profiles carry the identical purpose (`profiles.json:3`, 8 words): "controlled synthetic text-substitution profile, not an observed deployment". The census found 1 distinct purpose string across 3 profiles.
  - Required output must "name … profiles' synthetic purposes", but the pinned bytes cannot distinguish the baseline from the stimuli or name the workflow assumption each stimulus breaks.
- The pinned README documents a path for one token: `pinned-README.md:87` (2 words) `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"`. Origin-only is documented elsewhere, e.g. `:89` `export GITLAB="<your_gitlab_domain>:8023"`. No documented value ends in `/`.
- The raw data relies on that path. Five `__SHOPPING_ADMIN__/../<product>.html` program_html urls (tasks 464, 543–546) pop a path segment from the token. Two `__SHOPPING_ADMIN__/admin/system_design_theme/…` references (tasks 374, 375) assume the token already carries `/admin` (whether Magento routes this as `/admin/admin/…` is [INFERENCE], not observed).
  - So for the 300 SHOPPING_ADMIN occurrences, **path_prefix is structurally closest to the documented shape and distinct_origins departs from it**. That is the reverse of a "neutral baseline plus deviations" reading.
- The trailing-slash profile departs from all 7 documented example values. It is a pure stimulus: 697 `//` occurrences in 462/812 tasks, every one where a placeholder is followed by `/`.

Calling them neutral is a fixable labelling defect, not a projection-fidelity defect. The serialized-text projection is equally faithful under every profile, and the C1 count (812 × 3 = 2436) is unaffected.

## Decisive bounded counterexample: a stimulus effect, not model error

Task 374 (eval_types `url_match`, start_url `__SHOPPING_ADMIN__`) under trailing_slash_sensitivity projects its reference_url to `http://shopping-admin.invalid:10304//admin/system_design_theme/edit/id/1`.

The upstream evaluator, read as source, would score a single-slash prediction 0.0:
- It strips only trailing slashes (`evaluators.py:189`, 3 words: `url = url.rstrip("/")`).
- It compares netloc+path (`:195`, 5 words: `base_path = parsed_url.netloc + parsed_url.path`).
- It uses a substring test (`:223`, 3 words: `ref_base_path in pred_base_paths`). The `netloc+path` string `…10304//admin/…` is not a substring of `…10304/admin/…`.
- The same task scores 1.0 under distinct_origins and path_prefix. Population: 205/206 reference_url tasks score zero under trailing_slash_sensitivity; the one survivor has no placeholder in its reference.

Any downstream reading of a trailing_slash_sensitivity "failure" as agent or model error would therefore be a misattribution. The zero comes from the stimulus interacting with the evaluator's literal comparison.

The path_prefix profile also changes runtime helper control flow. `helper_functions.py:106` (4 words) `if tok_url[1] != "f":` returns the url unnormalized when a prefix occupies segment 1. Helpers also read env values directly (`:58`, 3 words: `order_url = f"{SHOPPING}/sales/order/view/order_id/{order_id}/"`), not projected config.

Source-versus-runtime boundary (preserved unknowns): I did not execute the evaluator, a browser or a site. The following are [INFERENCE] and not observed:
- whether a real browser preserves `//` in `page.url`;
- how `/../` dot segments resolve at runtime;
- whether any real deployment used a trailing slash or prefix.

No task-invalidity claim is made. The 5 `/../` urls behave identically across profiles in the projection, so they are an upstream data property, not a profile effect.

## Contract hazard tied to the objection

The prereg's exit codes are "Exit0 = audit completed with expected structural identities; exit1 =" / "projection/invariant finding" (`claims:53–54`, 10 + 2 words). It also says "No URL normalization, escaping repair or URL-only substitution" (`claims:45`, 8 words).

If an implementer adds a URL well-formedness invariant, such as "no non-scheme `//`" or "path starts at host root", then trailing_slash_sensitivity (697 occurrences) or path_prefix trips exit1. That would recast a deliberate stimulus as a projection finding. The prereg does not say these stimulus effects are *expected*.

## Impacted axes

- coverage/constructs (C1): labelling and provenance of stimulus versus baseline. Counts are unaffected.
- calibration (held at 8): unaffected, provided no F-forecast is re-scored against a "neutral" reading.
- novelty (score 7 held): unaffected. This is not a method claim.
- No runtime-validity, model-performance or task-validity axis is touched or claimed.

## Smallest safe correction (no frozen-byte edits; no rebinding)

1. Do not edit `profiles.json` or the manifest, because that would rebind the pinned population. Instead, the instrument's persisted expectations and `--summary`/`--json` output should carry one per-profile stimulus classification, keyed by profile name:
   - distinct_origins: origin-only. It departs from the README-documented SHOPPING_ADMIN `…/admin` shape and is not the documented baseline.
   - path_prefix: a synthetic prefix on all six tokens. It mirrors the documented shape for SHOPPING_ADMIN only.
   - trailing_slash_sensitivity: absent from all documented values. Expected `//` count 697 in 462 tasks.
2. State that "neutral" in claims:13 means synthetic/non-deployment, not workflow-conforming. No profile is a baseline for attributing errors.
3. Count `//` and prefix effects as expected stimulus observations under exit0. Never route them through exit1, and never repair or normalize them.
4. Any knowledge-draft prose must attribute per-profile differences to the stimulus and must not infer runtime score, model error or task invalidity. The task-374 witness above may serve as the hand case.

Flip condition: this objection is moot if L1 shows that the output and the knowledge draft already carry per-profile stimulus classes and expected-effect counts outside exit1.

VERDICT: PARTIAL
