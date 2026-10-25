# R29ConnectPattern — cross-round provenance pattern: r28 raw/effective URL-note vs r29 serialized-config projection

- **Seat / actual writer:** `KengakuR28.R29ConnectPattern-2` (connector; leaf, no subagents). Author-side advice only; not outside closure and not a Q10 source/number re-read.
- **Lane root:** `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Measurement revision for this seat: working tree at `31934e5660f1814326c6472eefdfa0c41e642a2f` plus untracked `.ufo/waves/round-29/`; no commits made.
- **Reads (sha256, observed):** `plans/round-29-claims.md` `6b4ffee3…e92c1`; `plans/fixtures/r29/manifest.json` `f6390b92…17bf87`; `plans/fixtures/r29/profiles.json` `90fdc34d…94e018`; `plans/fixtures/r29/generate_test_data.py` `45ddba7b…921cd` (838 bytes); `plans/fixtures/r28/webarena/config_files/test.raw.json` `7b50386f…37652` (880,776 bytes); `plans/fixtures/r28/webarena/evaluation_harness/evaluators.py` `e23edb39…00c22`; `plans/benchmark_spec_audit.py` `b7524c2f…cca36`.
- **Method:** stdlib JSON/text decoding of the pinned raw file as data, plus in-place reading of the pinned generator/evaluator text. No upstream code imported/executed/eval'd; no browser/endpoint/profile/credential access; no production edit; no install or update (none needed). Scratch: `.ufo/waves/round-29/scratch/KengakuR28.R29ConnectPattern-2/pattern_census.py` (`b45afc36…c9f837`) and `.out` (`ed10a588…3ef39a`).
- **Scope statement:** the numbers below are **input-side census predictions** from pinned bytes, not results of the not-yet-delivered `plans/config_projection.py`. No production projection, CLI run, exit0 or selftest pass is claimed. One scratch text-level consistency check with this seat's own stdlib code was run (E6); it is neither the delivered instrument nor the round's independent oracle.

## Axes

- **novelty** (C1, lowest legacy 7 → canonical coverage/constructs). The claim holds score 7; nothing here argues for repricing.
- **calibration 8** is untouched by this seat and by the proposed move.
- **methodology / temporal validity** must not be harmed: the move adds no new scientific method and no runtime/deployment evidence.

## Evidence

### E1 — r28's "effective" URL rule is a consumer-side default, counted apart from presence

Pinned evaluator line 215: `matching_rule = configs["eval"].get("url_note", "GOLD in PRED")` (6 whitespace tokens, line 215). The audit keeps three distinct states per task: raw `url_note` value, `url_note_present`, and `effective_url_rule` (`plans/benchmark_spec_audit.py:157`), and counts `url_note_origin` as `explicit` vs `defaulted` (`:104`, `:117`; selftest asserts a defaulted-only witness at `:352–354`). Frozen population: 205 `url_match` tasks; **196 explicit + 9 defaulted**; the r28 knowledge row records `205 GOLD in PRED;196 explicit url_note fields +9 defaulted` (`corpus/knowledge/webarena-task-spec-audit.md:117`). Dead-field census: 607 non-`url_match` tasks carry URL fields, exactly 1 non-empty `reference_url` (task 247, prose, not read by the pinned scorer).

So r28 measures a **field → consumer-rule** hop: absence is turned into a value only where the consumer source declares one, and defaulted is never folded into explicit. No token occurrence lies in `eval.url_note` or `eval.eval_types` (E2 class census), so the 196/9 provenance and the evaluator-set strata are **invariant across all three r29 profiles**, whereas r29's changed-leaf values are profile-specific. The two measurements cannot share a denominator.

### E2 — r29's provenance is a producer-side text → field hop, over a different representation

Pinned generator performs six ordered global text replacements (`generate_test_data.py:11–16`; e.g. `raw = raw.replace("__GITLAB__", GITLAB)`, 4 whitespace tokens, line 11), writes that projected text **before** parsing (`raw = f.read()` 3 tokens line 10; `data = json.loads(raw)` 3 tokens line 20), then emits per-position files from `for idx, item in enumerate(data):` (5 tokens line 21) and `with open(f"config_files/{idx}.json", "w") as f:` (5 tokens line 22); `json.dump(item, f, indent=2)` re-serializes (line 23).

Read-only census of the pinned text (no substitution executed):

| unit | value |
|---|---|
| serialized-text token occurrences | **1435** (GITLAB 385, REDDIT 336, SHOPPING_ADMIN 300, SHOPPING 281, WIKIPEDIA **0**, MAP 133) |
| distinct changed string leaves | **1416** |
| tasks containing ≥1 occurrence | **812 / 812**; leaves/task 1–12 |
| multi-occurrence leaves | 13 leaves holding 19 extra occurrences (e.g. tasks 431–435 `start_url`, 604/608/609/625 OR `reference_url`, task 66 annotation) |
| token occurrences in object keys | 0; other upper-case `__…__` markers: 0 |
| decoded-leaf occurrences | 1435, equal to serialized count (tokens are literal, escape-free, and appear in no keys) |

Reach partition (occurrence / leaf):

| field class | occ | leaves | scorer status under pinned r28 source |
|---|---|---|---|
| `top.start_url` | 818 | 812 | not read by pinned evaluator; consumer outside pinned set |
| `eval.program_html[*].url` | 338 | 338 | navigation/target URL for `program_html` |
| `eval.reference_url` | 217 | 205 | read only when `url_match`; all 205 token-bearing |
| `eval.program_html[*].required_contents` | 60 | 60 | content predicate (`must_include`); all 60 values are token-prefixed relative paths |
| `eval.reference_answer_raw_annotation` | 2 | 1 | no read in pinned evaluator set |

Class totals reconcile exactly: 818+338+217+60+2 = 1435 occurrences; 812+338+205+60+1 = 1416 leaves. By task evaluator set: 435 occurrences in the 205 `url_match` tasks; 1000 in the 607 non-`url_match` tasks. `string_match` `reference_answers` carry 0 occurrences.

This is a **different predicate** from E1: r28 asked which declared fields a routed evaluator reads; r29 asks which serialized text spans a producer rewrites and which decoded paths they land in. The raw JSON is the shared object, not a shared measurement.

### E3 — ordinal identity is positional in source, coincidentally equal on the frozen population

Pinned raw: task IDs are 0–811 in list order, `task_id == index` for **812/812**. Source writes `config_files/{idx}.json` from `enumerate` position (lines 21–22), so filename identity is ordinal, not ID-derived. r28 has no output-ordinal observable at all (its record exposes array position only in finding details, `benchmark_spec_audit.py:49`; no `start_url`, no ordinal). On this population an implementation that merely echoes `task_id` would reproduce the filename set exactly; only a shuffled-ID witness discriminates positional from ID identity.

### E4 — which provenance distinctions the production population can actually exercise

| distinction the instrument must keep | production status | only witness |
|---|---|---|
| explicit vs defaulted `url_note` (r28) | exercised: 196 / 9 | pinned raw + audit |
| field present but unread (r28 task 247) | exercised: 1 of 607 | pinned raw |
| six-token contract vs occurring tokens | partial: 5 of 6; WIKIPEDIA 0 | serialized census |
| occurrences vs changed leaves | exercised: 1435 vs 1416 | serialized census |
| occurrence → field-class reach | exercised: 5 classes | decoded-path census |
| Unicode-codepoint vs byte offsets | **not exercised**: 0 non-ASCII; 880,776 codepoints = 880,776 bytes; 0/1435 divergences | UTF-8 selftest fixture only |
| quote/backslash breaking serialized JSON | **not exercised**: all 3 profiles contain no `"` or `\` | selftest only |
| ordinal ≠ task_id | **not exercised**: 812/812 equality | shuffled-ID witness only |
| profile sensitivity for WIKIPEDIA | **not exercised**: 0 occurrences | synthetic fixture only |
| non-URL-valued field change (forecast F3) | input-determined: 61 leaves / 62 occurrences (60 `required_contents` + 1 annotation leaf) | delivered output must confirm execution |

### E5 — profiles are uniform-length families; total size is nearly token-blind

Each profile's six values add a constant codepoint count to its token: distinct_origins +17 each, path_prefix +24 each, trailing_slash +18 each. In GITLAB/SHOPPING/SHOPPING_ADMIN/MAP order, distinct_origins values 27/29/35/24 sit against token lengths 10/12/18/7; REDDIT is 27 against 10. The same +17/+24/+18 constant holds for every token in each profile respectively. Hence total projected-text growth is occurrences × constant: **24,395 / 34,440 / 25,830** codepoints, with WIKIPEDIA contributing 0 in all three. A digest or total-length comparison therefore distinguishes profiles but does not verify per-token correctness; per-token occurrence counts and per-task objects remain primary.

### E6 — scratch consistency check (not the delivered tool, not the official oracle)

`scratch_projection_check.py` (`7a1bdd3d…7bc06`) applies the six ordered replacements to the retained text with my own stdlib loop, parses each result, and walks pre/post leaves; output in `scratch_projection_check.out` (`9d75068f…3274`). Per profile: `tasks 812`, `changed_leaves 1416`, `len_delta 24,395 / 34,440 / 25,830`, `residual 0`. This corroborates E2/E5's invariants. It is a census consistency check, not the round's independent oracle (which must be separately authored without reading production code), and it does not score forecasts F1/F2 or stand in for the delivered instrument's observed output.

## Cross-axis pattern (one synthesis, no claim merge)

The two rounds measure one **three-hop provenance chain**: (1) serialized text span → (2) decoded JSON path → (3) consumer rule. r28 supplied hop 2→3 for URL fields, including the source-declared default and the unread-field boundary. r29 supplies hop 1→2 and the emitted ordinal; it does **not** re-measure hop 3. The invariant both instruments share is a discipline, not a fact: *an absent value becomes effective only where a consumer source declares a default; otherwise absence is could-not-evaluate.* r28's declaration is `evaluators.py:215`; r29's generator imports profile names from `browser_env.env_config` with no in-script fallback (line 5) and applies them at 11–16, so a missing profile key must be `profile_missing_key`/exit 2, never a silent default. The new mechanism measures the materialization r28 deliberately left as unresolved templates (`__SITE__`); it is the same offline source-faithful audit discipline extended one representation layer, **not a new scientific method**, and its facts (text occurrence, leaf reach, ordinal) are not r28's facts (scorer-read set, default rule).

C1 is the only live claim. r28's C1/C2 are prior admitted claims used here only as instrument precedent; this report creates no second claim, no pooled denominator, and cites no outside approval.

## Proposed move (one, bounded)

**Reach-partition + distinction-status grid in the projection evidence, not in the score.**

1. Give the prereg-required "changed string leaves by JSON path and category" a source-anchored category set: `eval.reference_url`, `eval.program_html[*].url`, `eval.program_html[*].required_contents`, `top.start_url`, `eval.reference_answer_raw_annotation`, and a mandatory `other` bucket that must be **0** on the frozen input (nonzero = finding, not silent exclusion).
2. Emit, per profile, the invariant `Σ category occurrences = serialized-text occurrences = decoded-leaf occurrences = 1435`, `changed leaves = 1416`, `changed tasks = 812`, `residual known tokens = 0`. These are input-derived expectations to be **compared after** the delivered run, not preclaimed results.
3. Accompany the run with a distinction-status grid (E4): each prereg distinction is marked `exercised_by_population` with its count or `fixture_only` with the named selftest. Label the 812/812 ordinal equality `population_coincidence`; delegate positional correctness solely to the shuffled witness.
4. Join to r28 only at category labels (field classes), never by pooling counts: r28's 196/9 stay consumer facts; r29's 1435/1416/812 stay producer facts.

Why it improves **novelty**: it makes the acquired capability's coverage precise and observable (5 field classes, 5-of-6 tokens, 3 counting units, one ordinal coincidence) and blocks the three overclaims the raw population invites. Why it harms none: no score change, no calibration input, no new method, no runtime/deployment claim; it uses only already-required per-task changed-leaf paths. If the delivered interface cannot derive categories from those paths, the grid stays report-level and must not expand the frozen tool contract mid-flight.

## Contradictions and risks

1. **`start_url` is rewritten in all 812 tasks but is not an evaluator field.** "Not scorer-readable" ≠ inert: it likely supplies initial navigation, but the pinned r28 fixture set contains no runner, so its consumer is unknown. Do not label it harmless; carry it as unscored-by-pinned-evaluator.
2. **`required_contents` is non-URL-valued by schema, yet its 60 token values are URL-text** (all token-prefixed relative paths). Forecast F3's category therefore mixes a genuine text predicate with URL-shaped strings; observing F3 in output confirms execution, not a surprising semantic reach. Do not update F3 before the run.
3. **Codepoint-vs-byte units are untestable on the pinned input.** A byte-offset implementation passes the full 2436 projection; only a UTF-8/escaped selftest witness can discriminate. The 2436 run must not be cited as codepoint-unit evidence.
4. **Ordinal correctness is untestable on the frozen input** for the same reason: 812/812 equality is consistent with echoing `task_id`.
5. **WIKIPEDIA sensitivity is unobservable.** A wrong WIKIPEDIA value yields zero output delta and still exits 0; no per-token sensitivity claim may include it.
6. **Profile totals are uniform-length** (E5); text size/digest alone cannot validate per-token replacement. Using them as primary evidence would weaken verification.
7. **`eval.reference_answer_raw_annotation` (2 occurrences, task 66) has no reader in the pinned evaluator set**; treat as annotation metadata, not a scorer predicate. Its rewrite is a preserved change, not a scored change.
8. **Scope risk of the move:** if treated as a new required output mid-build, it becomes scope creep and can harm the schedule/verification axis. It is admissible only as a comparison/report grid over existing required fields.

## Verification

- Reproduce input census: `python3 .ufo/waves/round-29/scratch/KengakuR28.R29ConnectPattern-2/pattern_census.py` → 1435 occurrences, 1416 leaves, 812 tasks, class totals above; compare to the delivered `python3 plans/config_projection.py --summary` per-class counts and per-task objects after the run (L1-owned).
- Independent oracle must reproduce the same five class totals from pinned text without importing production code; disagreement is a cross-implementation finding, not a silent adjustment.
- Selftest witnesses this seat requires to exist (not run here): UTF-8 token following a multibyte codepoint (offset unit), one-token-in-two-OR-alternatives leaf (occurrence vs leaf), WIKIPEDIA-bearing synthetic input (unexercised token), quote/backslash input (JSON decode failure, no repair), shuffled IDs (ordinal vs ID), and a token in a non-url_match `reference_url` (dead-field category).
- Do not cite this report as evidence that the projection runs, exits 0, or passes selftests; those are unobserved until L1’s run. No actual `config_files` output was created in-lane.

## Unknowns and source-vs-runtime boundary

- Whether upstream actually produces the same projection on a deployment is outside this seat: `env_config` values, locale/encoding of the real `open()`, and runner consumption of `start_url` are not in the pinned set.
- All profile values are synthetic `*.invalid` fixtures; they are not endpoints, deployment evidence, or model errors.
- The 0-WIKIPEDIA and pure-ASCII properties are properties of this frozen population only; they do not generalize to other WebArena revisions or other configs.

VERDICT: PASS (scoped) — grounded cross-round provenance synthesis (consumer-side default vs producer-side text→field reach, ordinal identity), one bounded reach-partition/distinction-status move that does not change score, method or runtime claims; production results, selftests and admission remain unobserved and unclaimed.
