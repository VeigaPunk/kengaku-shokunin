source: S070 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/scripts/generate_test_data.py main8–23, replacements11–16, parse20, enumerate-index21–23; S072 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/README.md lines79,84–92,95,97–101; S073 https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/prepare.sh lines1–6; S071 https://docs.python.org/3/library/json.html Character Encodings and loads; S068 raw-task input pin https://raw.githubusercontent.com/web-arena-x/webarena/dce04686a56253aefba7b18a4fa0937cf1dc987b/config_files/test.raw.json
verified-at: 2026-10-21 — source openings plus offline projection of pinned bytes; no upstream import/execution, live benchmark, env_config value or runtime config observed
recheck: on-release — python3 plans/config_projection.py --summary and --selftest; reopen S070/S072/S073 at the pinned revision
writer: KengakuR29-2

# WebArena generated-config projection — what the generator does to task specs before any agent runs

## What this adds and what it does not

Extends corpus/README.md Frontier “generated eval-time configs” left open by round28
(`knowledge/webarena-task-spec-audit.md` audited raw specs only). The acquired repertoire is an
**offline, source-faithful projection** of the pinned generator over the pinned raw task file, under three
frozen synthetic `*.invalid` profiles, with per-task output-ordinal mapping and changed-field provenance.
Seat R29DraftEntry drafted the first scope; this candidate replaces it with measured facts.

It is not an actual deployment config, env_config value or observed endpoint; not task validity, model
performance, browser/helper/judge runtime behaviour or contamination evidence; not a new method (novelty
score held). The three profiles are controlled sensitivity stimuli, not deployment recommendations.

## The generator's contract, read as inert source (S070)

- `from browser_env.env_config import *` (line5) supplies the six values; the import never runs here.
- Lines11–16 apply six global `raw.replace` calls to the **serialized text**, in order GITLAB, REDDIT,
  SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP; the whole text is written before `json.loads(raw)` (line20).
- Lines21–23 write `config_files/{idx}.json` from `enumerate(data)`: the filename is the list position,
  not `item["task_id"]`.
- S072: the README's step 2 exports scheme-less example `origin:port` values (SHOPPING_ADMIN adds
  `/admin`) and step 3 runs this script; it documents no replacement order or token inventory.
  S073: `prepare.sh` only creates `./.auth` and runs `auto_login.py`; it is not the generator call site.
- S071: `json.loads` raises on an invalid document rather than repairing it; a value containing `"` or `\`
  therefore makes the projected JSON invalid or is decoded as a JSON escape (`\n` becomes a newline);
  nothing is normalized or repaired.

## Observed projection of the pinned inputs (2026-10-21)

`python3 plans/config_projection.py --summary`, exit0, 0 findings, identical per profile except digests:

| unit | value |
|---|---|
| input tasks / distinct IDs / profiles / task×profile projections | 812 / 812 / 3 / 2436 |
| original token occurrences (GITLAB, REDDIT, SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP) | 385, 336, 281, 300, 0, 133 = 1435 |
| tasks carrying each token (not additive: sum 834, distinct 812) | 204, 128, 192, 182, 0, 128 |
| changed string leaves / of all string leaves / with >1 occurrence | 1416 / 10869 / 13 |
| changed leaves by JSON-path category | url_field 1355 (start_url 812, program_html url 338, reference_url 205); non_url_field 61 (must_include 60, reference_answer_raw_annotation 1) |
| remaining six known tokens, serialized and decoded | 0 and 0 per profile |
| other `__…__` markers, not env tokens | `__last_url__` 65, `__page__` 12 |
| output ordinal == task_id | 812/812 on the frozen order |
| value-`/` then raw-`/` junctions (`//`) | 697 under trailing_slash_sensitivity, 0 otherwise |

Units are distinct: an occurrence is a text match, a leaf is a decoded string value, a task is one of 812.
Occurrence offsets are Unicode codepoints in the original input text. Every token occurrence is inside a
string value; none is inside a key or structural text.

## What the numbers do and do not license

- **Global text replacement reaches non-URL fields.** 61 changed leaves are `must_include` answer strings
  and one raw annotation; a URL-fields-only re-implementation would leave them unprojected (hand witness
  `url-only` and its mutant fail). Whether a changed `must_include` changes any score is runtime/scorer scope.
- **WIKIPEDIA is unexercised by the population.** Its token occurs 0 times, so 5 of 6 tokens are exercised
  by real data; the sixth is covered only by hand cases. `sites` metadata is not used to count tokens.
- **Positional output naming is invisible on the frozen order.** index==task_id holds for all 812 tasks, so
  only the shuffled-ID hand witness shows the enumerate rule; a reordered raw file would rename outputs.
- **Order is invisible on the frozen profiles.** No profile value contains a token, so a reversed-order
  mutant produces identical output on real data; only the cascade hand case distinguishes the order.
- **Profile effects are stimulus observations.** `//` junctions and `/prefix` paths are produced by design
  and are never counted as defects, model errors or task invalidity.

## Operational decision rule

Before interpreting a WebArena run, reproduce its generated configs from pinned generator and raw bytes
with the run's own value map, then: (1) confirm 812 parsed tasks and zero remaining tokens; (2) check every
non-URL changed leaf (`must_include`, annotations) is intended; (3) compare per-task filenames with
`task_id` whenever the raw order may differ; (4) reject any value carrying `"`, `\` or a token string,
because text replacement would break JSON or cascade. This is a reproducibility precondition, not a
validity certificate.

## Calibration and adjacent scope

Calibration and novelty scores are unchanged. Actual env_config-derived/deployment configs, runtime task
validity, hosted judges and contamination remain open. Serving-plane ownership stays outside this lane.
