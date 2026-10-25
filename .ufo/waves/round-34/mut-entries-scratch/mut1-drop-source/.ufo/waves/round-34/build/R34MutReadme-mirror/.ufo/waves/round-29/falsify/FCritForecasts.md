writer: KengakuR29-2.FCritForecasts-2

# FCritForecasts — adversarial scoring of informed forecasts F1–F5 (round 29, falsify)

Attacks: scoring of `plans/round-29-claims.md:103-108` (F1–F5) against observed instrument output at lane
master `56fd949a6478342531e61f4feecb4a685d831640`. Role: critic, read-only leaf. No calibration credit is
sought or granted.

- Production source `plans/config_projection.py`: **NOT read and not imported.** I compared only its
  `--summary`/`--json`/`--selftest` OUTPUT with my own census, which I derived from the generator bytes,
  the raw812 file and `profiles.json`.
- Build-wave reports were read as evidence, not proof.
- Tools installed or updated: none. I used python3 stdlib, git (read-only) and rg.
- Writes: this report, plus scratch at `.ufo/waves/round-29/scratch/falsify/FCritForecasts/`
  (`summary.txt`, `out.json`, `selftest.txt`, `forecast_census.py`, `census.out`).

## Commands and observed outputs

| command (cwd = lane root) | observed |
|---|---|
| `python3 plans/config_projection.py --summary` | exit 0; `TOTAL findings=0 exit=0` |
| `python3 plans/config_projection.py --json > scratch/out.json; sha256sum` | exit 0; `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, equal to `corpus/evidence/round29-calibration/build-json-sha256.txt` content; 3,881,050 bytes |
| `python3 plans/config_projection.py --selftest` | exit 0; `SELFTEST clean cases=20`, includes `hand_index_r29_index_shuffled_ids_1_0` |
| `python3 scratch/forecast_census.py` (independent) | exit 0; output in `scratch/census.out` |
| `sed -n '103,108p' plans/round-29-claims.md \| sha256sum` at HEAD vs at `31934e56` | both `f69146750b57…9e4`; forecasts unchanged since freeze |
| `git diff --stat ed26bdf5 HEAD -- SCORECARD.md AXES.md README.md corpus/README.md` | empty (byte-identical) |

My independent census matched the instrument output on every forecast-relevant metric, for all 3 profiles:

| metric | mine | instrument |
|---|---|---|
| parsed tasks per profile | 812 | 812 |
| residual tokens (text / decoded) | 0 / 0 | 0 / 0 |
| changed leaves | 1416 | 1416 |
| non_url / url split | 61 / 1355 | 61 / 1355 |
| index == task_id | 812/812 | 812, violations 0 |

## Resolution table

| id | p | resolution | evidence | informativeness |
|---|---|---|---|---|
| F1 | .95 | **TRUE** | 812 parsed for distinct_origins, path_prefix and trailing_slash_sensitivity (instrument and mine) | entailed by construction (O4) |
| F2 | .9 | **TRUE** | `remaining_known_tokens_text` and `_decoded` are all 0 in all 3 profiles (instrument and mine) | entailed by construction; WIKIPEDIA part vacuous (O4) |
| F3 | .7 | **UNSCORABLE as a uniquely resolved frozen forecast**; conditionally TRUE under field-role reading A and single-URL reading B, FALSE under URL-bearing reading C | A: 61 leaves; B: 13 leaves; C: 0 leaves. Task 66 witnesses A and B, not C | baseline evidence and unresolved category prevent prospective success credit (O1–O2) |
| F4 | .95 | **TRUE** | frozen input 812/812; the shuffled fixture's input IDs `[1, 0]` map to ordinals `[0, 1]`; selftest case clean | clause 2 is true by fixture construction (O5) |
| F5 | .95 | **UNSCORABLE as a forecast**; provisionally TRUE (SCORECARD unchanged) | no admission has happened yet; the prereg's own :17 fixes the outcome | set by the claimant's own policy (O6) |

## Objections

### O1 — F3 outcome evidence existed before the forecast (fixable: provenance wording)

**Counterexample.** At baseline `ed26bdf5`, before the prereg commit `31934e56` (2026-10-21 12:56:42 -0300), the
lane already contained the F3 outcome under the role reading:

- `.ufo/waves/round-28/build/Task552.md:33`. Added in `18b1922` at 11:27:16 -0300. Quote (5 words, counted
  programmatically): "`required_contents.must_include` | 5 strings, `__REDDIT__/f/space/{134164,134163,134162,134161,134160}/<slug>`".
- `.ufo/waves/round-28/scratch/FContractAstAuthority/audit-hook.stdout.json:4449`. Added in `df33fc8` at
  12:34:02 -0300. It shows `reference_answer_raw_annotation` beginning `"__REDDIT__/f/books/59396/…`. This is
  exactly the leaf that witnesses F3 under both data-dependent readings.
- The raw file itself is present at the baseline: `git cat-file -e ed26bdf5:plans/fixtures/r28/webarena/config_files/test.raw.json`
  exits 0, sha256 `7b50386f…7652`.

**Evidence of the contrary provenance claim.**

- `.ufo/waves/round-29/build/R29DraftLesson.md:59` (11 words): "Whether the pinned `test.raw.json` has placeholders
  in non-URL fields is unobserved".
- `.ufo/waves/round-29/drafts/lesson-and-mistake.md:121-122` repeats "unobserved".
- The prereg (`:108`, 13 words) says: "Score these after observed output; they are source/code-informed, not an
  independent calibration gain." It discloses source/code-informed. Existing lane evidence further limits
  any interpretation as a previously unobserved outcome; availability does not establish forecaster exposure.

**[INFERENCE]** I cannot tell whether the forecaster read `Task552.md`. The point is that the outcome was
available, not that it was read.

**Impacted axes.** Calibration (honesty of the forecast record), provenance.

**Smallest safe correction.** Tag F3 "baseline evidence available at r28 `Task552.md:33` (`18b1922`);
forecaster exposure unknown". Qualify "unobserved" in `drafts/lesson-and-mistake.md:121-122` by seat and
measurement scope. Do not infer deception or claim independent prediction success from availability alone.

### O2 — F3's category changes the truth value (fixable reporting defect; prospective ambiguity cannot be repaired retroactively)

The prereg (`:106`, 10 words) says: "F3 global replacement changes at least one non-URL-valued field, p=.7;". My
census of the 1416 changed leaves (profile distinct_origins) gives:

| reading of "non-URL-valued field" | changed leaves satisfying it | F3 |
|---|---|---|
| A: field role. The path template is not in {`start_url`, `eval.reference_url`, `eval.program_html[].url`} | 61 (`must_include[]` 60, `reference_answer_raw_annotation` 1) | TRUE |
| B: value shape. The projected value is not one absolute URL (it contains whitespace, `,` or `\|`, or has no scheme/host) | 13 (annotation 1, `eval.reference_url` 7, `start_url` 5) | TRUE |
| C: value contains no URL at all | 0 | FALSE |

- **A and B disagree on 72 of 73 witness leaves.** Twelve of reading B's 13 are labeled `url_field` by the
  instrument, for example `$[604].eval.reference_url` (three URLs joined by `|OR|`) and `$[432].start_url`
  (two URLs joined by `|AND|`). B's set is exactly the 13 multi-occurrence leaves. The only leaf under both A
  and B is `$[66].eval.reference_answer_raw_annotation` (`/66/…` in the instrument output; category
  `non_url_field`).
- **Reading C yields FALSE.** Every changed leaf begins with a token (census: 0 counterexamples), and all
  18 frozen profile values are absolute `http://` URLs. Consequently every changed leaf contains URL text
  after substitution. This reading is construction-degenerate for these changed values, but remains a
  possible interpretation of the wording. The stated p=.7 cannot authoritatively exclude an interpretation.
- **The field-level value census supports reading A.** Across all raw812 leaves, the share of each field's
  values that start with a URL or token:
  - `must_include[]`: 61/815 = 0.0748
  - `reference_answer_raw_annotation`: 2/332 = 0.0060
  - `start_url`: 812/812 = 1.0000
  - `eval.reference_url`: 205/805 = 0.2547 (599 of its values are empty)

  This supports a field-role interpretation, not a uniquely preregistered definition.

**Scorable? Not uniquely as a frozen forecast.** A and B yield TRUE; C yields FALSE. Task 66 is a common
witness for A and B only, not a reading-invariant witness. Reporting conditional outcomes is legitimate;
choosing A after observing the counts does not retroactively freeze the original event.

**Impacted axes.** Calibration/provenance; novelty only if this result is used to inflate the C1 claim.

**Smallest correction.** Mark F3 unscorable under the original unresolved wording, publish A=61, B=13,
C=0 as descriptive sensitivity, and explicitly define the three URL-role templates for future reporting.
The canonical judge must reject prospective forecast-success credit from a post-observation choice;
the offline projection capability and measured field-role counts remain independently usable.

### O3 — the instrument output carries category labels but not the category rule (fixable)

- The per-leaf records in `--json` carry `category` and `path_template`. Census for distinct_origins: 5
  templates map to 2 categories.
- The output contains no rule text: none of the strings `category_rule`, `category_definition`,
  `url_field_paths` or `URL_ROLE` occurs. The top-level non-profile keys, including all 7 `limitations`
  entries, never mention `url_field`.
- So "score after observed output" cannot determine F3's category from the output alone. The mapping is
  recoverable only for templates that changed, and the rule for any other template requires the source.

**Impacted axes.** Calibration, operability of the independent oracle comparison.

**Correction.** Add one LIMIT or metadata line to the output naming the URL-role template set. This is one line
and touches no counts.

### O4 — F1 and F2 are entailed by the frozen profiles (tradeoff: score them, but tag as non-informative)

- No profile value contains `"`, `\` or a control character, and none of the 18 values contains `_`.
- No known token occurs in any JSON key (0).
- Therefore the sequential text replacement cannot change JSON structure (F1), and cannot leave or recreate a
  `__X__` token (F2).
- `__WIKIPEDIA__` has 0 original occurrences (`ORIGINAL_OCCURRENCES_BY_TOKEN`), so that sixth part of F2 is
  vacuous. R29CritResidualMarkers.md:86 and R29CritNoAxisHarm.md:65 raised this already; it is not new here.
- These events primarily check deterministic projection correctness on authenticated bytes, not independent empirical trials.

**Correction.** Resolve both as TRUE, tagged "construction-entailed (profiles.json @31934e56)". Prereg `:108`
already disclaims calibration gain, so this is a tradeoff, not a defect.

### O5 — F4's second clause is true by fixture construction (tradeoff, plus one disclosure)

- **Clause 1** ("index==task_id for all812 frozen items"): TRUE. My census gives 812/812 with 812 distinct IDs;
  the instrument reports `index_equals_task_id: 812` and `violations: []`. It was also readable from baseline
  bytes, because the raw file is present at `ed26bdf5`.
- **Clause 2** ("but not a shuffled witness"): resolved by `plans/fixtures/r29/hand/index-shuffled-ids.fixture.json`.
  - `case_id` is `r29_index_shuffled_ids_1_0`, `writer` is `KengakuR28.R29MutIndex-2`.
  - `expected_input_task_ids` is `[1, 0]` and `expected_output_ordinals` is `[0, 1]`.
  - The fixture was adopted in `b98dcf31`, after the forecast commit, and selftest reports the case clean.
  - A two-element transposition cannot satisfy index==task_id. The clause therefore tests the instrument's
    enumerate behavior, not a forecastable event.

The prereg F4 wording is 12 words: "F4 index==task_id for all812 frozen items but not a shuffled witness, p=.95;".

**Correction.** Score F4 TRUE. Tag clause 2 "constructed witness (b98dcf31), tests the instrument".

### O6 — F5 is provisionally true now; final resolution event is unspecified (fixable reporting boundary)

- **Wording** (`:107`, 6 words): "F5 no method-novelty score increase, p=.95."
- **No resolution event is stated.** No admission has happened. `SCORECARD.md` is byte-identical between
  `ed26bdf5` and HEAD, so F5 is provisionally TRUE at observation time only.
- **The quantity named is not a SCORECARD row.** `SCORECARD.md:661` (8 words) says: "`novelty` is a recorded
  sub-axis of canonical **coverage**". No separate "method-novelty" score exists.
- **The outcome is fixed by the claim itself.** Prereg `:17` (7 words) says: "Score7 held; calibration8 and
  other axes unchanged."
- R29CritNoAxisHarm.md:77 already called F5 "guaranteed". The new points here are the missing resolution event
  and the mismatch between the named term and the SCORECARD.

**Correction.** Record F5 as "pending; resolve against the admitting commit's SCORECARD novelty row (legacy
sub-axis of coverage/constructs); non-informative, declared at :17".

### O7 — misquotation narrows F3 (fixable)

- `.ufo/waves/round-29/drafts/lesson-and-mistake.md:100` puts F3 in quotation marks as "global replacement
  changes at least one non-URL field".
- Prereg `:106` says "non-URL-valued field".
- Dropping "-valued" silently resolves O2 toward reading A.

**Correction.** Quote `:106` verbatim.

### O8 — no integrated artifact scores F1–F5 (open obligation, not a defect yet)

- `rg -i 'F[1-5]\b|forecast'` over `.ufo/waves/round-29/drafts`, `candidate-freeze-v1.json` and
  `corpus/evidence/round29-calibration` finds 2 lines, both in `lesson-and-mistake.md` (:100, :121). Both
  describe the forecasts as unobserved.
- The candidate `drafts/webarena-config-projection.md` (sha256 `7006b93d…53dc`, matching the freeze) has 0
  forecast mentions.
- The prereg `:108` scoring duty is therefore still unmet at `56fd949a`.

## Scoring sensitivity (informational only, no calibration credit)

These Brier values use the stated probabilities.

| scenario | Brier |
|---|---|
| all five TRUE | 0.0215 |
| F3 FALSE (reading C) | 0.1015 (4.72× the all-TRUE value) |
| F5 excluded, all TRUE | 0.0263 |
| F5 excluded, F3 FALSE | 0.1262 |
| hypothetical F3 probability replaced with 1 (not the preregistered probability) | 0.0035 |

- F3's ambiguity changes these illustrative arithmetic values materially; F5 remains pending.
- Deterministic, policy-constrained and dependent events do not establish independent model calibration.
- No calibration credit follows. The hypothetical replacement of p=.7 with p=1 is sensitivity only:
  baseline availability does not justify rewriting the registered probability.

## Mismatch list (exact location → value)

1. `R29DraftLesson.md:59` and `drafts/lesson-and-mistake.md:121-122` say "unobserved". Baseline
   `ed26bdf5:.ufo/waves/round-28/build/Task552.md:33` already records 5 `must_include` values starting with
   `__REDDIT__/f/space/…`.
2. `drafts/lesson-and-mistake.md:100` quotes "non-URL field". Prereg `:106` says "non-URL-valued field".
3. Instrument category vs reading B: 12 leaves labeled `url_field` are not single-URL values
   (`eval.reference_url` 7, `start_url` 5; for example `$[604]`, `$[431]`–`$[435]`).
4. Instrument `--json`: category rule absent; only labels present.
5. F5's term "method-novelty score" vs `SCORECARD.md:661`, where `novelty` is a legacy sub-axis of coverage
   and no method-novelty row exists.

There were no numeric mismatches between instrument output and my independent census for F1–F4 metrics.

## Facts vs [INFERENCE]

**Observed:** every count, hash, commit, timestamp, line and exit code above.

**[INFERENCE]:**
- Whether the forecaster consulted the r28 evidence before writing F3.
- Which F3 category the forecaster intended. Neither probability .7 nor post-observation category counts
  establish that intent. The conditional outcomes above must remain distinct.

VERDICT: PARTIAL
