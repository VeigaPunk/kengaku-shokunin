writer: KengakuR29-2.FEntryScope-2

# FEntryScope — overclaim attack on the round-29 knowledge candidate

Item: FEntryScope (round 29, post-crash falsify wave). Target:
`.ufo/waves/round-29/drafts/webarena-config-projection.md`, sha256
`7006b93dcacff38736cb49f2153e2b3960591887576b3e8c2ddc3519565653dc` (re-hashed 2026-10-21; matches
`candidate-freeze-v1.json`). Lane HEAD `56fd949a6478342531e61f4feecb4a685d831640`.

- Production source `plans/config_projection.py`: **NOT read**. I used only its `--summary`/`--json` output.
- I wrote only this report and files under `.ufo/waves/round-29/scratch/falsify/FEntryScope/`
  (`census.py`, `census.out`, `rule4_probe.py`, `rule4_probe.out`, `pertask_compare.out`, `summary.txt`,
  `out.json`).
- Tools installed or updated: none. I used stdlib `python3` 3.14.8 and `rg` only, so `RULES.md`
  install channels were not needed.
- Quotes below were word-counted with `str.split()`, and each was confirmed present in the
  whitespace-flattened candidate. Line numbers are candidate lines unless prefixed otherwise.

## Commands run (observed)

| command | exit | output identity |
|---|---|---|
| `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0`; saved `summary.txt` sha256 `5ce5cb0f…74636f` |
| `python3 plans/config_projection.py --json` | 0 | sha256 `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630` (= freeze `json_output_sha256`) |
| `python3 scratch/.../census.py` (own; generator L11–23 semantics from pinned bytes) | 0 | `census.out` |
| `python3 scratch/.../rule4_probe.py` (own; synthetic `*.invalid` values) | 0 | `rule4_probe.out` |
| own per-task comparison against `--json` `profiles.*.tasks` | 0 | `pertask_compare.out` |

## Independent re-derivation (observed; every candidate table number reproduces)

The raw file has sha256 `7b50386f…537652`, 880776 bytes, all ASCII, with no CR.

| quantity | measured |
|---|---|
| tasks / distinct IDs / index==task_id | 812 / 812 / 812 |
| token occurrences | GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, WIKIPEDIA 0, MAP 133; sum 1435 |
| tasks per token | 204, 128, 192, 182, 0, 128; sum 834; tasks with any token 812 |
| occurrence role | 1435 inside string values; 0 in keys; 0 in structural text |
| string leaves / changed / >1 occurrence / changed tasks | 10869 / 1416 / 13 / 812 per profile |
| changed by path | start_url 812, program_html url 338, reference_url 205, program_html must_include 60, raw annotation 1 |
| remaining six tokens | 0 per profile |
| `//` junctions | trailing_slash 697; distinct_origins 0; path_prefix 0 |
| all 720 replacement orders | byte-identical output for each of the 3 profiles |
| per-task `projected_task`, `output_index`, filename vs own projection | equal for 812/812 per profile, 2436/2436 total |

## Overclaim screen — the axes the assignment named

- **Deployment configs:** no overclaim. Lines 2, 16, 18 and 79 disclaim it explicitly.
- **Runtime validity:** one low-severity implication, the title on line 6 (mismatch M6 below).
  Everywhere else runtime validity is disclaimed (lines 17, 79–80).
- **Scoring effects:** no direct claim. Line 58 defers scoring to "runtime/scorer scope". However,
  line 56's "answer strings" mislabels the field role (mismatch M3 below).
- **Task invalidity:** no overclaim (lines 66 and 75).
- **Novelty:** no overclaim. Lines 17 and 79 hold the score, consistent with prereg L18 ("Score7 held").
  The keyword scan found no "first"/"novel" priority claim.
- **Population coverage of all six tokens:** no overclaim. Lines 59–60 state 5 of 6 exercised and
  WIKIPEDIA 0. I also observed that 23 tasks list `wikipedia` in `sites`, yet their start_urls use
  `__MAP__` (17) and `__GITLAB__` (6), so no WIKIPEDIA value reaches any frozen config.
  Minor: line 45's "remaining six known tokens … 0" is vacuous for WIKIPEDIA (0 original occurrences).

## Mismatches: exact location, value, and smallest fix

**M1 (rule-breaking counterexample) — lines 30–31 and line 74.**
- Line 31 quote (19 words): "a value containing `"` or `\` therefore makes the projected JSON invalid or is decoded as a JSON escape".
- Line 74 quote (18 words): "reject any value carrying `"`, `\` or a token string, because text replacement would break JSON or cascade."
- Counterexample (observed, `rule4_probe.out`): set the MAP value to `http://m.invalid", "task_id": 9999, "z": "` and keep the other five values from distinct_origins.
  - The projection parses: 812 tasks, 0 remaining tokens.
  - 128 tasks gain an extra key, and 128 tasks show `index_ne_task_id`. The injected duplicate `task_id` wins (last wins), because `task_id` precedes `start_url` in each object (task0 key order observed).
  - So a quote can yield **valid, silently restructured** JSON, a third outcome the two-way claim excludes.
- Rule impact: step (1) passes. Step (3) at lines 72–73 ("whenever the raw order may differ", 11 words) would skip the check, because the raw order is unchanged. Step (4) still rejects the value, so the rule's *conclusion* holds; its stated *reason* is false.
- Smallest fix:
  - line 31: "…makes the projected JSON invalid, silently adds or overrides keys (duplicate key: last wins), or is decoded as a JSON escape";
  - line 74: "…would break or restructure JSON or cascade";
  - optionally drop "whenever the raw order may differ" in step (3).

**M2 (false summary) — line 36.**
- Quote (8 words): "exit0, 0 findings, identical per profile except digests".
- Observed: `value_slash_then_raw_slash_junctions` is 697 for trailing_slash_sensitivity and 0 for the other two profiles. That appears in both the instrument summary and the candidate's own line 48.
- Smallest fix: "identical per profile except digests and the `//` junction count".

**M3 (field-role mislabel implying a scoring role) — line 56.**
- Quote (11 words): "61 changed leaves are `must_include` answer strings and one raw annotation".
- Observed:
  - All 60 changed `must_include` leaves are at `eval.program_html[].required_contents.must_include[]`. Their tasks have eval types `program_html` (52 leaves) or `url_match`+`program_html` (8 leaves).
  - 0 changed leaves are under `eval.reference_answers`.
  - The values themselves are URL strings, e.g. task 552 `__REDDIT__/f/space/…`.
- "Answer strings" attributes a reference-answer scoring role that was never observed. The sentence also reads ambiguously as 61 + 1.
- Smallest fix: "61 changed leaves are 60 `program_html` `required_contents.must_include` strings and one raw annotation".

**M4 (incomplete source summary, relevant to the six-token axis) — lines 27–28.**
- Quote (12 words): "the README's step 2 exports scheme-less example `origin:port` values (SHOPPING_ADMIN adds `/admin`)".
- Observed in README bytes (sha256 `081c8264…9c9287`, matching S072), lines 91–92:
  - the WIKIPEDIA example carries the long path `:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing`;
  - HOMEPAGE is a seventh export, which generator lines 11–16 never replace.
- The S072 row in SOURCES.md already states both facts; the candidate drops them. The only path-heavy README value belongs to the token that occurs 0 times.
- Smallest fix: append "; WIKIPEDIA adds a long path; HOMEPAGE is a seventh export the script never replaces".

**M5 (incomplete reject list) — line 73, step (4).**
- Observed: values containing a literal newline, a literal tab, or a trailing `\` raise `JSONDecodeError` ("Invalid control character"). None of them carries a token string, and the first two carry neither `"` nor `\`.
- Step (1) would still catch these, since the generator raises, so the rule's outcome is unchanged.
- Smallest fix: "reject any value carrying `"`, `\`, a control character (U+0000–U+001F) or a token string".

**M6 (runtime implication) — line 6 title.**
- Quote (11 words): "what the generator does to task specs before any agent runs".
- The ordering comes from the README workflow: step 3 generates the configs, and step 6 "Launch the evaluation" (README L105–113) comes later. The step-6 lines are outside S072's cited lines, and no run or consumer of `config_files/{idx}.json` was observed.
- Smallest fix: "what the pinned generator script does to raw task specs (README setup step 3)".

**M7 (unnamed unit, against line 50's own rule) — line 46.**
- Quote (11 words): "other `__…__` markers, not env tokens | `__last_url__` 65, `__page__` 12".
- Observed: these are occurrence counts. `__last_url__` covers 55 tasks and `__page__` covers 9 tasks.
- Smallest fix: "occurrences: `__last_url__` 65 (55 tasks), `__page__` 12 (9 tasks)".

## Is the operational decision rule (lines 70–75) supported by observed facts?

- **Step (1), 812 parsed and zero remaining tokens:** supported on the frozen domain (instrument output and census). It is scoped to the six env tokens; the 77 marker occurrences remain by design.
- **Step (2), check non-URL changed leaves:** supported. 61 such leaves exist.
- **Step (3), filenames vs `task_id`:** supported by generator L21–23 and the shuffled-ID hand witness. The `index_by_task_id` mutant survives real data (`mutation-witness.txt`: findings=0 exit=0). The "whenever" condition is too narrow (M1).
- **Step (4):**
  - The conclusion is supported by the hand cascade case and the selftest's quote/backslash cases.
  - Cascade via a raw junction is impossible on these bytes. Tokens are preceded only by `"` (1416) or space (19), and followed only by `"` (738) or `/` (697), so the token-string check suffices.
  - The stated reason is falsified (M1), and the list is incomplete (M5).
- **Preamble "with the run's own value map":** [INFERENCE] this is prescriptive. No real run or env_config value was observed, which line 75 correctly labels as "not a validity certificate".

## Adjacent observation (not a candidate overclaim)

- C1 (prereg L13) requires independent oracle agreement, but seat `R29ExecOracle` is listed dead in `build-dead-seats.json`.
- `corpus/evidence/round29-calibration/` contains no oracle receipt.
- The candidate does not claim oracle agreement, but line 12's "source-faithful" currently rests on the selftest, the mutation witness and source reading. My re-derivation agrees with the instrument on 2436/2436 per-task objects and on all aggregates. This is my falsify-item evidence, not a seat oracle.

## Impacted axes and verdict scope

- **Novelty:** unaffected. No novelty overclaim was found.
- **Coverage/constructs and calibration of wording:** affected by M1–M7. Each is a fixable wording defect, not a tradeoff the judge must reject.
- The numbers and the projection itself are not falsified. The scope disclaimers hold for deployment, scoring, task invalidity, novelty and six-token coverage.
- The verdict covers this item only, not round admission.

VERDICT: PARTIAL
