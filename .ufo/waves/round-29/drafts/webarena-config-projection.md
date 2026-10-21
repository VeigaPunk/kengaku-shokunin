source: S070 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py main8–23, replacements11–16, parse20, enumerate-index21–23; S072 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md lines79,84–92,95,97–101; S073 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh lines1–6; S071 https://docs.python.org/3/library/json.html Character Encodings §576-591, invalid-document402, duplicate names624-625; S074 https://raw.githubusercontent.com/ServiceNow/BrowserGym/4ccc72332ab9882bc9aed87264dbf60b16e426f0/browsergym/webarena/src/browsergym/webarena/task.py lines55–69,81–82; S068 raw-task input https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json manifest byte pin
verified-at: 2026-10-21 — source openings plus offline projection of pinned bytes; no upstream import/execution, live benchmark, env_config value or runtime config observed
recheck: on-release — python3 plans/config_projection.py --summary and --selftest; python3 plans/fixtures/r29/mutation_witness.py; reopen S070/S072–S074 at their pinned revisions
writer: KengakuR29-2

# WebArena generated-config projection — what the pinned generator script does to raw task specs

## What this adds and what it does not

Extends the gap left by round28 at corpus/README.md:338 (“generated eval-time configs … remain open”);
`knowledge/webarena-task-spec-audit.md` audited raw specs only. Replacing placeholders in serialized task
text is established practice: the BrowserGym loader does the same ordered replacement (S074). What the lane
acquires is an **audited, source-faithful projection**: the pinned generator over the pinned raw file under
three frozen synthetic `*.invalid` profiles, with occurrence provenance, changed-field census, per-task
output-ordinal mapping and mutation-tested tests. Seat R29DraftEntry drafted the first scope.

It is not an actual deployment config, env_config value or observed endpoint; not task validity, model
performance, browser/helper/judge runtime behaviour or contamination evidence; not a new method (novelty
score held). No profile is a baseline: “neutral” in the round's plan means synthetic and non-deployment,
and “benign” means values that keep the text JSON-safe. All three add an `http://` scheme, which the
README's examples lack, so per-profile differences are stimulus effects, never task or model errors.

## The generator's contract, read as inert source (S070)

- `from browser_env.env_config import *` (line5) supplies the values; the import never runs here.
- Lines11–16 apply six global `raw.replace` calls to the **serialized text**, in order GITLAB, REDDIT,
  SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; the whole text is written before `json.loads(raw)` (line20).
- Lines21–23 write `config_files/{idx}.json` from `enumerate(data)`: the filename is the list position,
  not `item["task_id"]`.
- S072: the README's step 2 exports seven variables as scheme-less `origin:port` examples (SHOPPING_ADMIN
  adds `/admin`, WIKIPEDIA a long path, HOMEPAGE is a placeholder the generator never replaces); step 3
  runs this script. It documents no replacement order or token inventory. S073: `prepare.sh` only creates
  `./.auth` and runs `auto_login.py`; it is not the generator call site.
- S071: `json.loads` raises on an invalid document rather than repairing it, and duplicate names keep the
  last value. A value containing `"` can therefore make the projected JSON invalid **or** parse with altered
  structure (injected keys, a duplicated `task_id` overriding the original); a value containing `\` can make
  it invalid or be decoded as a JSON escape (`\n` becomes a newline). Nothing is normalized or repaired.

## Observed projection of the pinned inputs (2026-10-21)

`python3 plans/config_projection.py --summary`, exit0, 0 findings. The three profiles agree on every count
below except their text digests and the `//` junction row:

| observable | value |
|---|---|
| input tasks / distinct IDs / profiles / task×profile projections | 812 / 812 / 3 / 2436 |
| original token occurrences (GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) | 385, 336, 281, 300, 0, 133 = 1435 |
| tasks carrying each token (not additive: 790 one-token + 22 two-token tasks = 834 rows, 812 tasks) | 204, 128, 192, 182, 0, 128 |
| changed string leaves / of all string leaves | 1416 / 10869; 13 leaves hold 32 occurrences, so 1435 = 1416 + 19 |
| changed leaves by JSON-path category | url_field 1355 (start_url 812, program_html url 338, reference_url 205); non_url_field 61 (60 `program_html[].required_contents.must_include[]` strings, 1 `reference_answer_raw_annotation`) |
| remaining six known tokens, serialized and decoded | 0 and 0 per profile |
| other `__…__` markers, not env tokens (occurrences / tasks) | `__last_url__` 65 / 55, `__page__` 12 / 9 |
| output ordinal == task_id | 812/812 tasks on the frozen order |
| value-`/` then raw-`/` junctions, occurrences (`//`) | 697 in 462 tasks under trailing_slash_sensitivity, 0 otherwise |

Occurrence offsets are Unicode codepoints in the original input text; every occurrence is inside a string
value, none in a key or structural text. The category is by JSON path, so all 61 non_url_field leaves hold
URL-shaped strings under non-URL keys. Falsification: four independently written oracles reproduced every
count, all 1435 provenance records and all 2436 projected objects and would-be file digests
(`.ufo/waves/round-29/falsify/FOracleText.md`, `FOracleLeaf.md`, `FOracleProvenance.md`, `FOracleIndex.md`);
the instrument author also wrote this entry. Receipts: `corpus/evidence/round29-calibration/`.

## What the numbers do and do not license

- **Global text replacement reaches non-URL fields.** The 61 non_url_field leaves change because the
  replacement is global; a URL-fields-only re-implementation leaves them unprojected and is killed by the
  tests (`plans/fixtures/r29/mutation_witness.py`). Whether a changed `must_include` alters any score is
  runtime/scorer scope.
- **WIKIPEDIA is unexercised by the population.** Its token occurs 0 times, so 5 of 6 tokens are exercised
  by real data; the sixth is covered only by hand cases. `sites` metadata is not used to count tokens.
- **Positional output naming is invisible on the frozen order.** index==task_id holds for all 812 tasks; a
  shuffled-ID hand witness shows the enumerate rule, and a reordered raw file would rename outputs.
- **Order is invisible on the frozen profiles.** No profile value contains a token, so a reversed-order
  mutant produces identical output on real data; only the cascade hand witness distinguishes it.
- **Profile effects are stimulus observations.** `//` junctions and `/prefix` paths are produced by design.

## Operational decision rule

Before interpreting a WebArena run whose harness reads generator output by file index, reproduce its
configs from pinned generator and raw bytes with the run's own value map, then: (1) confirm 812 parsed tasks
and zero remaining tokens; (2) account for every non-URL changed leaf as a global-replacement effect;
(3) compare per-task filenames with `task_id`; (4) reject any value containing `"`, `\`, a control character
(U+0000–U+001F) or a token string, because text replacement would break or restructure the JSON or cascade.
Harnesses that select configs by `task_id` (S074) need checks 1, 2 and 4 only. This is a reproducibility
precondition, not a validity certificate.

## Calibration and adjacent scope

Calibration and novelty scores are unchanged. Actual env_config-derived/deployment configs, runtime task
validity, hosted judges and contamination remain open. Serving-plane ownership stays outside this lane.
