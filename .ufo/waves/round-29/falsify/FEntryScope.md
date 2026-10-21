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

## Re-check at dbcecded (follow-up)

This is a second-seat Q10 re-read for the same item, FEntryScope. Everything above was written about
v1 (`7006b93d…`) and is left unedited. This section covers only candidate v2.

- **Candidate path:** `.ufo/waves/round-29/drafts/webarena-config-projection.md`
- **Canonical path:** `corpus/knowledge/webarena-config-projection.md`
- **sha256, printed first:** `435d4bb1c7b1881d2fdc8a29f84719ec39f199bd0bc96d60fde5a647cd98f8e5`. It
  equals `candidate-freeze-v2.json` `sha256`, and these are the exact bytes I reviewed (90 lines).
- **Lane HEAD:** `dbcecded4a04247cf6fd12919327af973da10bdd`. The instrument
  `plans/config_projection.py` has sha256 `135cc682…aa142`, equal to the freeze record.
- **Production source:** NOT read.
- **Writes:** this appended section, plus new files in my scratch directory only (`summary-v2.txt`,
  `out-v2.json`, `selftest-v2.txt`, `census_v2.py`, `census_v2.out`, `rule4_probe_v2.out`,
  `mutation-v2.txt`, `pertask_compare_v2.out`, `recheck-section.md`).
- **No lane, git or jj mutation.** Installs: none.
- **`/tmp`:** the only `/tmp` use was `mutation_witness.py`'s own auto-deleting
  `TemporaryDirectory`. Afterwards `ls -d /tmp/kengaku-r29-witness-*` counted 0. I made no `/tmp` copies of my own.
- **Quotes:** word counts are by `str.split()`, and each quote was confirmed present in the
  whitespace-flattened v2. Line numbers below are v2 lines.

### Commands re-run on v2 (observed)

| command | exit | identity |
|---|---|---|
| `python3 plans/config_projection.py --summary` | 0 | `TOTAL findings=0 exit=0`, `DUPLICATE_OBJECT_KEYS 0` |
| `python3 plans/config_projection.py --json` | 0 | sha256 `a4fb5d6dd9b7d509be55ae9d5c779dccaf9e29a7727447a30c568a174579d851` = freeze `json_output_sha256` |
| `python3 plans/config_projection.py --selftest` | 0 | `SELFTEST clean cases=28` |
| `python3 plans/fixtures/r29/mutation_witness.py` | 0 | `"killed": 10`, mutants on a `/tmp` copy; `restored_sha256` = `135cc682…`; lane tool hash unchanged |
| own `census_v2.py`, `rule4_probe.py`, v2 per-task compare | 0 | outputs listed above |

### The seven v1 objections, re-checked

| v1 objection | v2 location and text | status |
|---|---|---|
| Quote injection (lines 30–31, 74) | v2 lines 34–37 now say a `"` value "can therefore make the projected JSON invalid **or** parse with altered structure (injected keys, a duplicated `task_id` overriding the original)" (20 words). Line 83 ends "break or restructure the JSON or cascade". The S071 duplicate-name source (lines 624–625) is added to line 1. Step (3) on line 82 is now unconditional: "(3) compare per-task filenames with `task_id`;" (6 words). | **Resolved.** The re-run probe still gives 812 parsed, 0 remaining tokens and 128 tasks with `task_id` overridden. v2 now states this outcome, and the unconditional step (3) catches it. |
| "identical except digests" (line 36) | v2 lines 41–42: "The three profiles agree on every count below except their text digests and the `//` junction row" (17 words). | **Resolved.** Instrument output shows every other table count equal across profiles; the `//` count is 697 / 0 / 0. |
| "must_include answer strings" (line 56) | v2 line 50 gives the full path `program_html[].required_contents.must_include[]` (60) plus 1 raw annotation. Lines 57–58 add "all 61 non_url_field leaves hold URL-shaped strings under non-URL keys" (10 words). "answer strings" is gone. | **Resolved.** I observed 61/61 leaves where every comma-separated part starts with a token followed by `/`. |
| README summary (lines 27–28) | v2 lines 30–31: seven variables; "WIKIPEDIA a long path, HOMEPAGE is a placeholder the generator never replaces" (12 words). | **Resolved.** This matches README lines 86–92 (hash-verified bytes) and generator lines 11–16, which contain no HOMEPAGE replace. |
| Control characters (line 73) | v2 lines 82–83: "reject any value containing `"`, `\`, a control character (U+0000–U+001F) or a token string" (14 words). | **Resolved.** Re-run probe: newline and tab values raise "Invalid control character". |
| Title implying runtime order (line 6) | v2 line 6: "what the pinned generator script does to raw task specs" (10 words). | **Resolved.** The "before any agent runs" wording is gone. |
| Marker units (line 46) | v2 line 52 names the unit ("occurrences / tasks"): "`__last_url__` 65 / 55, `__page__` 12 / 9" (8 words). | **Resolved.** This matches my v1 census (65 occurrences in 55 tasks, 12 occurrences in 9 tasks). |

### New v2 claims, attacked

Each new claim was checked against observed sources or my own computation:

- **Line 48, "790 one-token + 22 two-token tasks = 834 rows, 812 tasks":** confirmed. Own census:
  {1 token: 790, 2 tokens: 22}, 834 rows.
- **Line 49, "13 leaves hold 32 occurrences, so 1435 = 1416 + 19":** confirmed. 13 leaves hold 32
  occurrences, and 32 − 13 = 19.
- **Line 54, "697 in 462 tasks":** confirmed. Token followed by `/`: 697 occurrences in 462 tasks.
- **Line 20, "All three add an `http://` scheme":** confirmed. All 18 profile values start with `http://`.
- **Lines 12 and 84, S074:**
  - The BrowserGym `task.py` copy at `scratch/falsify/FCritNovelty/fetch/bg_wa_task.py` has sha256
    `f996dfee…fe67` and 8603 bytes, equal to the S074 row.
  - Lines 55–66 run six serialized-text `replace` calls in the generator's order (GITLAB, REDDIT,
    SHOPPING, SHOPPING_ADMIN, WIKIPEDIA, MAP). Line 69 runs `json.loads`, and lines 81–82 select by
    `task_id`.
  - "Same ordered replacement" and "select configs by `task_id`" are therefore supported.
  - The rule's exemption from check 3 for `task_id` harnesses is consistent with line 82 of `task.py`.
- **Lines 58–61, four oracles:**
  - All four oracle reports end in `VERDICT: PASS` (FOracleText, FOracleLeaf, FOracleProvenance,
    FOracleIndex), and each states that production source was not read.
  - Only FOracleProvenance names an instrument output digest, and it is v1's `c8da0c5a…`.
  - I closed that gap on the v2 output (`out-v2.json`, `a4fb5d6d…`). Against my own projection,
    `projected_task` matches 2436/2436 including key order, `would_be_file_sha256` matches 2436/2436
    against sha256(`json.dumps(task, indent=2)`), and index-named filenames match 2436/2436.
  - The receipt `repair-projection-equality.json` records v1 and v2 objects as equal when key order
    is ignored.
  - Line 60 discloses that the instrument author also wrote this entry. The candidate claims
    reproduction only, not blind certification of source semantics, so the `FCritOracleIndependence`
    PARTIAL does not falsify this sentence.

### Overclaim re-screen of v2 (axes named by the assignment)

- **Deployment configs:** none. Lines 2, 17, 19 and 89 disclaim them, and line 19 says no profile is a baseline.
- **Runtime validity:** none.
  - The title is fixed.
  - Line 79 scopes the rule to a harness "that reads generator output by file index" as a condition,
    not as an observed run.
  - Lines 18 and 89–90 disclaim runtime.
- **Scoring effects:** none. Lines 67–68 defer scoring to "runtime/scorer scope".
- **Task invalidity:** none (lines 21 and 85).
- **Novelty:** no inflation.
  - Lines 18–19 and 89 hold the score.
  - Lines 11–12 now *concede* prior practice: "Replacing placeholders in serialized task text is
    established practice" (9 words). This lowers the novelty claim rather than raising it.
- **Six-token population coverage:** none. Lines 69–70 keep "5 of 6" and WIKIPEDIA at 0.

### Decision rule (lines 79–85)

- **Step (1):** supported. 812 parsed and 0 remaining tokens per profile, observed.
- **Step (2):** supported. 61 non-URL changed leaves, observed.
- **Step (3):** supported. Generator lines 21–23, the shuffled index witness, and the unconditional
  wording covering the duplicate-`task_id` case.
- **Step (4):**
  - The reason is now correct and the list now complete for every failure I observed: quote,
    backslash, control character and cascade.
  - A raw-junction cascade remains impossible on these bytes. Tokens are preceded only by `"` or
    space and followed only by `"` or `/` (v1 census).
- **S074 exemption:** "Harnesses that select configs by `task_id` (S074) need checks 1, 2 and 4 only."
  (14 words). This is supported by S074 lines 81–82.
- **Self-labelling:** the rule still calls itself "a reproducibility precondition, not a validity certificate".

### Non-blocking residuals (none is an overclaim on the assigned axes)

- **R1:**
  - Lines 11–12 say "established practice", while the S074 row says "as prior practice". The
    observed instances are the upstream generator plus one harness.
  - The wording follows `FCritNovelty`'s recommended correction, and it lowers rather than raises novelty.
  - Optional smallest fix: "is prior practice".
- **R2:** the rule assumes the run's raw task file equals the pinned bytes. Check (1) catches count
  drift but not same-count content drift.
  - `FCritNovelty` reports that BrowserGym's packaged `libwebarena-0.0.5` raw is byte-identical to the
    pin. That is its evidence; I did not re-check it.
  - Optional smallest fix: prefix the steps with "(0) confirm the run's raw task file is
    byte-identical to the pinned one".
- **R3:** three of the four oracle reports do not name the instrument output digest they compared,
  and the fourth names v1's. This is closed for v2 bytes by my per-task re-check above. Optional fix:
  cite `repair-projection-equality.json` alongside them.

### Scoped conclusion

- All seven v1 objections are resolved on the exact v2 bytes.
- Every new number and the new S074 claims reproduce or match hash-verified source bytes.
- No sentence implies deployment configs, runtime validity, scoring effects, task invalidity, novelty
  gain, or coverage of all six tokens by the population.
- The operational decision rule is supported by observed facts.
- This verdict covers this re-check only, not round admission.

VERDICT: PASS

## Final re-check of candidate v3 (follow-up)

This is a second-seat Q10 re-read for the same item, FEntryScope. Everything above is left unedited.
This section covers only v3, across source, numbers, quality and scope.

- **Candidate path:** `.ufo/waves/round-29/drafts/webarena-config-projection.md`
- **Canonical path:** `corpus/knowledge/webarena-config-projection.md`
- **sha256, printed first:** `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`,
  equal to the digest the coordinator named. I reviewed these exact 99 lines.
- **Freeze record:** `candidate-freeze-v3.json` does not exist (only v1 and v2 exist).
- **Lane HEAD:** `dbcecded4a04247cf6fd12919327af973da10bdd`. The working tree has `plans/config_projection.py`
  at sha256 `d81a6af8…4f9f`, and both it and `plans/fixtures/r29/mutation_witness.py` are uncommitted
  (`M`). These are the coordinator's changes; I did not write them. Their hashes were the same before and
  after my runs.
- **Production source:** NOT read.
- **Writes:** this appended section, plus new scratch files (`summary-v3.txt`, `out-v3.json`,
  `selftest-v3.txt`, `mutation-v3.txt`, `recheck-v3-section.md`).
- **No lane, git or jj mutation.** Installs: none.
- **`/tmp`:** used only by the witness's auto-deleting `TemporaryDirectory`. Afterwards
  `ls -d /tmp/kengaku-r29-witness-*` counted 0. I made no `/tmp` copies of my own.

### What changed from v2 (observed)

- v3 lines 2–36 are textually the same as v2 lines 2–36. v3 lines 71–99 are the same as v2 lines 62–90,
  shifted by nine lines.
- Line 1 was not byte-compared, because I kept no v2 copy. It keeps the same S070–S074 source set.
- The changes are confined to line 37 and lines 58–70, matching the coordinator's description.

### Commands re-run (observed)

| command | exit | identity |
|---|---|---|
| `--json` | 0 | sha256 `a4fb5d6d…d851`, **byte-identical** to the v2 freeze `json_output_sha256` and to my `out-v2.json` |
| `--summary` | 0 | `TOTAL findings=0 exit=0`. Diffed against v2 with `LIMIT` lines excluded, only labels differ: an added `INPUT` line (raw `7b50386f…`, manifest `f6390b92…`, revision `dce04686…`) and `index_task_id_mismatches` renamed to `index_task_id_mismatch_count`, still 0 |
| `--selftest` | 0 | `SELFTEST clean cases=30` |
| `mutation_witness.py` | 0 | tool `d81a6af8`, `killed` 12, `url_only_substitution` killed, restored `d81a6af8` |

The objects and metrics are unchanged. My v2 checks still apply to these output bytes: 2436/2436
projected objects including key order, would-be digests and filenames, plus every table number
(790/22, 32, 462, 55/9, 697, 61/1355).

### The changed sentences, attacked

- **Line 37: "a value containing `\` can make it invalid or be interpreted as a JSON escape" (15 words).**
  - Supported. My probe parses `\n` as an escape and gets a decode failure for a trailing `\`.
  - Dropping the `\n` example removes nothing a reader needs, and the `"` restructuring clause on
    lines 35–36 is intact.
- **Lines 58–59: "Four oracles, separately written by distinct same-lane seats (independent logic, not independent identity)" (13 words).**
  - Supported. The writers are four distinct seats: `KengakuR29-2.FOracleText-2`, `.FOracleLeaf-2`,
    `.FOracleProvenance-2` and `.FOracleIndex-2`.
  - All four end in `VERDICT: PASS`, and each states that production source was not read.
  - The qualifier concedes exactly what `FCritOracleIndependence` disputed.
  - The claim is now narrowed to "population/profile metrics", 1435 provenance records, 2436 objects and
    would-be digests. That fixes v2's broader "every count".
- **Lines 62–63: "were separately re-derived by the entry-review seats, not by those four oracle reports" (13 words).**
  - Supported. `FEntryNumbers.md` lines 80–96 and 288–290 re-derive 790/22 and 32.
  - My own census re-derived all four: 790/22, 32 and 462 (`census_v2.out`), and 55/9 (v1 census).
- **Lines 64–65: "binds the repaired objects to the objects the oracles compared" (10 words).**
  - Supported with one qualification. The receipt compares `56fd949:plans/config_projection.py` with
    tool `135cc682`: objects equal ignoring key order, and provenance equal.
  - FOracleProvenance pins the v1 output `c8da0c5a…`, which was produced at 56fd949. The other three
    oracle reports pin no output digest, so for them the binding rests on wave timing.
  - The gap from `135cc682` to the current `d81a6af8` is closed by the byte-identical `a4fb5d6d` output
    observed above.
  - This is non-blocking. It is the same residual R3 as before, now partly closed.
- **Lines 67–70, the "Falsifiers" paragraph:**
  - Every named falsifier is observable with the shipped instrument: changed pin digest, nonzero remaining
    tokens, changed 61/1355 split, index/task-ID mismatch, object disagreement.
  - Line 70, "Agreement on this population alone does not establish general-input equivalence" (10 words),
    removes any reading of general semantic certification. This is a scope gain with no harm.

### Final verdict by axis

- **Source:** the S070, S072 and S074 bytes I re-verified earlier support every source sentence; these
  lines are unchanged in v3.
- **Numbers:** every table and bridge number reproduces, and the output bytes are unchanged.
- **Quality:** the units are named, the oracle attribution is scoped by which seat derived what, and the
  falsifiers are explicit.
- **Scope:** no sentence implies deployment configs, runtime validity, scoring effects, task invalidity,
  novelty gain, or coverage of all six tokens by the population (re-screened lines 1–99).
- **Decision rule (lines 86–94):** byte-unchanged from v2, and still supported as assessed above.
- **My seven v1 objections:** all remain resolved.

### Non-blocking residuals

- R1 ("established practice" vs the S074 row's "prior practice") and R2 (no byte-identity check on the
  run's raw file) stand unchanged and are optional.
- R3 is partly closed, as described under lines 64–65.
- Admission bookkeeping, outside this item: there is no `candidate-freeze-v3.json`, and the current
  instrument (`d81a6af8`) is uncommitted. The candidate text names no tool hash, so this verdict does not
  depend on either.

The verdict below is scoped to this exact v3 re-read, not to round admission.

VERDICT: PASS

## Final re-check of candidate v4 (locator-only follow-up)

This is a second-seat re-read for the same item, FEntryScope. Everything above is left unedited. This
section covers only the v4 line-1 locator change, plus a byte comparison of the rest against the v3 I passed.

- **Candidate path:** `.ufo/waves/round-29/drafts/webarena-config-projection.md`
- **Canonical path:** `corpus/knowledge/webarena-config-projection.md`
- **sha256, printed first:** `9d11f44bf22d357758a5988b514d23cca84d4061816d3c3d65294974dd506e74`
  (99 lines, 8772 bytes). These are the exact bytes I reviewed.
- **Production source:** NOT read.
- **Writes:** this appended section and `scratch/.../recheck-v4-section.md`.
- **No lane, git or jj mutation.** Installs: none.
- **`/tmp`:** I used one copy, `/tmp/FEntryScope-json.html`, fetched twice and deleted both times.
  After the final delete, `test -e` returned 1 (absent).

### Byte comparison against v3 (observed)

- I kept no v3 copy, so I rebuilt v3 from v4. I put the old S071 text (`S071 https://docs.python.org/3/library/json.html Character Encodings §576-591, invalid-document402, duplicate names624-625`)
  back in place of v4's `S071/S075 …` segment in line 1, keeping everything else.
- The rebuilt line 1 hashes to `889d53f2…71ac9`, equal to the v3 line-1 hash I recorded earlier.
- The rebuilt file hashes to `59b646a74792d182dfd63cc118c40efb015db26c9c68c5a5b556a9db46579bca`, equal
  to the v3 I passed and to `candidate-freeze-v3.json`.
- **So v4 differs from v3 only in that one segment of line 1.** Lines 2–99 are byte-identical to v3
  (their sha256 is `9148a503…4f4a`). The body, numbers and decision rule are unchanged, and my v3
  findings carry over intact.

### The locator correction, reopened (observed)

I fetched `https://docs.python.org/3/library/json.html` on 2026-10-21. The page sha256 was
`8271280b…01d5`, and its title reads "Python 3.15.1 documentation", matching the S071/S075 version.

| v4 locator | anchor present | content at the anchor | status |
|---|---|---|---|
| `#character-encodings` ensure_ascii paragraph | yes | "this module's serializer sets ensure_ascii=True by default, thus escaping the output so that the resulting strings only contain printable ASCII characters" | exact |
| `#repeated-names-within-an-object` opening paragraph/example | yes | "it ignores all but the last name-value pair for a given name", with the example `json.loads('{"x": 1, "x": 2, "x": 3}')` giving `{'x': 3}` | exact; supports v3 lines 34–36 (last value wins) |
| `#json.loads` invalid-document exception | yes | the block says only "Identical to load() …"; the sentence "When the data being deserialized is not a valid JSON document" appears under `#json.load` ("Raises: JSONDecodeError") and under `#json.JSONDecoder` | fact correct, **anchor one hop off** |

**Non-blocking locator note L1.** The `#json.loads` locator in line 1 and in the S075 row does not hold
the invalid-document sentence itself. `json.loads` inherits it through "Identical to load()", so the fact
in v4 line 34 is correct and the anchor is stable.

- Smallest fix, if wanted: "#json.load invalid-document exception (json.loads: 'Identical to load()')".

This is a locator-precision issue, not an overclaim, so my scope verdict does not depend on it.

### Scoped verdict

- The single changed line is confirmed. Two of the three stable anchors are exact, and the third is a
  correct fact reached through the documented "Identical to load()" link (note L1).
- Byte-identity of lines 2–99 with v3 is proved by the hash reconstruction above.
- Every scope, source, number and decision-rule conclusion from my v3 re-check therefore holds for v4
  unchanged.
- The optional residuals R1 and R2 from earlier stand as non-blocking.
- This verdict covers this exact v4 re-read, not round admission.

VERDICT: PASS
