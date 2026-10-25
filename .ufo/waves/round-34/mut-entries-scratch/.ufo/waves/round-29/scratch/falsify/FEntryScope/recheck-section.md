
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
