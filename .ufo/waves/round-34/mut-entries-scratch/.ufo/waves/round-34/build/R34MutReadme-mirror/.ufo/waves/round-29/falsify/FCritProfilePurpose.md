writer: KengakuR29-2.FCritProfilePurpose-2

# FCritProfilePurpose — persisted stimulus-class labels and "neutral" wording

- Seat: FCritProfilePurpose (critic, read-only leaf, post-crash falsify wave, round 29 only). Date 2026-10-21.
- Attacks: the persisted `STIMULUS` labels, the `purpose`/LIMIT strings, the prereg's "neutral" wording, and the knowledge candidate's profile prose. Question asked: can any output be read as a deployment baseline, or as model/task error attribution?
- Integrated state: lane `HEAD` = `56fd949a6478342531e61f4feecb4a685d831640` (from `git rev-parse HEAD`). Candidate sha256 `7006b93d…53dc` and manifest sha256 `f6390b92…7bf87` were re-observed and match the assignment.
- **Production source:** I read `plans/config_projection.py` lines 25–49 and 268–357, and grepped it for labels and finding ids. This is a critic item, not an oracle or re-derivation item. My own census scripts do not import it.
- No tools were installed or updated. No pacman was run. I did not execute upstream code or contact any network endpoint.
- Writes: this report, and scratch under `.ufo/waves/round-29/scratch/falsify/FCritProfilePurpose/`. One experiment used a copy at `/tmp/fcpp`, which I removed afterwards.

## Commands and observed output

1. `python3 plans/config_projection.py --summary | --json | --selftest`
   - Exits: 0 / 0 / 0.
   - The `--json` sha256 is `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`, which equals `corpus/evidence/round29-calibration/build-json-sha256.txt`. The output is 3881050 bytes.
   - `diff` against `build-summary.txt` differs only by the receipt's extra final line `exit=0`.
   - Selftest prints `SELFTEST clean cases=20`.
2. Raw-text census of `test.raw.json` (inline python, my own regex):
   - Token occurrences: 1435.
   - Preceding character: `"` 1416, space 19.
   - Following character: `"` 738, `/` 697.
   - Scheme-prefixed tokens (`https?://__X__`): 0.
   - My 697 equals the instrument's `population.tokens_followed_by_slash` and its `trailing_slash_sensitivity.stimulus_observations.value_slash_then_raw_slash_junctions`.
3. `scratch/.../readme_shape.py` (sha256 `9be8726e…8b08`). This is my own serialized-text replace in the upstream order plus a leaf diff. It adds one counterfactual synthetic profile shaped like README.md:86–91: scheme-less, `/admin`, and the long WIKIPEDIA path, on `*.invalid` hosts. Output is in `readme_shape.out` (sha256 `ea896643…91ea`), counted in leaves:

| profile | changed leaves | leaves with `://` | SHOPPING_ADMIN leaves containing `/admin` | non-scheme `//` leaves | `/admin/admin` leaves | start_url without scheme |
|---|---|---|---|---|---|---|
| distinct_origins | 1416 | 1416 | 2 / 300 | 0 | 0 | 0 |
| path_prefix | 1416 | 1416 | 2 / 300 | 0 | 0 | 0 |
| trailing_slash_sensitivity | 1416 | 1416 | 2 / 300 | 678 | 0 | 0 |
| readme_shape_counterfactual (mine, not frozen) | 1416 | 0 | 300 / 300 | 0 | 2 | 812 |

   - Raw `__SHOPPING_ADMIN__/admin` occurrences: 2. `__SHOPPING_ADMIN__/` occurrences: 125. `__SHOPPING_ADMIN__/../` occurrences: 5.
   - 678 is a count of leaves; 697 is a count of occurrences. These are different units.
4. Wording scan of my `--json` output (inline python, attributed by JSON path):
   - Instrument-authored text: "neutral" 0, "baseline" 0. "error" and "recommend" each appear once, both in the negated LIMIT at `/limitations/1`. The `/index_mapping/violations` key appears once.
   - All other hits are WebArena task text under `projected_task` and are not instrument wording: "neutral" ×3 (`Unable to set neutral steering`), "recommend" ×78, "error" ×15.
5. Finding ids in production (grep plus lines 268–357): `task_population_invalid`, `token_outside_string_value`, `projection_json_invalid`, `projection_structure_changed`, `leaf_change_unexplained`, `known_token_remaining`, `projection_population_changed`, `projection_count_invalid`.
   - Every per-profile finding is keyed by `profile`. None is keyed by task, and none counts junctions or prefixes.
   - `index_violations` (line 290) produces no finding.
6. `/tmp/fcpp` copy test:
   - The unmodified copy run with `--root /tmp/fcpp --summary` gave `TOTAL findings=0 exit=0`.
   - After changing one value (`distinct_origins.SHOPPING_ADMIN` → `shopping-admin.invalid:7780/admin`), it gave `FINDING {"id": "snapshot_tampered", "path": "plans/fixtures/r29/profiles.json"}` and `TOTAL findings=1 exit=2`.
7. `scratch/.../quotes.py` (sha256 `167cd561…a1da`) reported 19/19 quotes `OK` on their cited lines. Word counts below are whitespace-split.
8. `git log -1 31934e56…`: the prereg commit subject is `round-29: freeze generated-config projection claim and neutral profiles`.

## Prior state

Build-wave seat `.ufo/waves/round-29/build/R29CritProfilePurpose.md` raised the "neutral" objection and returned PARTIAL. The integrated code now carries a persisted `STIMULUS` map (`config_projection.py:33–37`) and the LIMIT at `:44`. My attack targets what survived that fix.

## Findings

### M1 — "neutral" has three meanings, and nothing that ships reconciles them (fixable disclosure defect; the frozen bytes are a tradeoff)

The same three profiles are given three different labels:

| location | quote | words |
|---|---|---|
| `plans/round-29-claims.md:13` | "neutral substitution profiles (2436 task/profile projections)" | 6 |
| `plans/fixtures/r29/manifest.json:15` | "own-work synthetic neutral profiles" | 4 |
| prereg commit subject (git log) | "… and neutral profiles" | — |
| `plans/round-29-claims.md:31` | "own-work profiles.json: distinct origins, path-prefix sensitivity, trailing-slash sensitivity." | 8 |
| `plans/round-29-claims.md:44` (also :80, :105) | "frozen benign profile domain" | 4 |
| `config_projection.py:44` (LIMIT, emitted) | "three frozen synthetic *.invalid sensitivity stimuli, not deployment recommendations" | 9 |
| candidate `:18` | "The three profiles are controlled sensitivity stimuli, not deployment recommendations." | 10 |

- **Counterexample.** A sensitivity stimulus cannot also be neutral. Table 3 shows that no frozen profile matches the documented README value shape (scheme and `/admin` both differ), so "neutral" cannot mean "workflow-conforming" either. The README examples are scheme-less: `README.md:86` `export SHOPPING="<your_shopping_site_domain>:7770"` (2 words) and `:87` `export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"` (2 words).
- The only explicit denial of a baseline is a source comment, `config_projection.py:32`: "no profile is a documented deployment baseline, and stimulus effects are never findings." (13 words). Command 4 shows "baseline" appears 0 times in the emitted output, and neither the output nor the candidate mentions or maps "neutral".
- **Classification.** The manifest and prereg bytes are pinned (manifest sha persisted in the instrument) or frozen at the landed commit, so editing them would rebind the population. That part is a tradeoff to disclose, not to fix in place. The missing reconciliation in the shipped candidate is a fixable defect.
- **Smallest safe correction.** Add one sentence to candidate `:18` with no instrument or receipt change: "No profile is a baseline or reference; prereg/manifest 'neutral' means synthetic non-deployment, and 'benign' means the decode-safe oracle domain."
- **Optional.** Also emit the `:32` sentence as a LIMIT. This changes the summary and json bytes, so the receipts would need to be re-cut.

### M2 — The P1 stimulus label names one README deviation and omits the larger one (fixable label defect)

- `config_projection.py:34`, emitted as `stimulus_class` and summary line 15: "origin-only synthetic values; not the README-documented SHOPPING_ADMIN '/admin' shape" (9 words).
- Read negatively, this label says P1 equals the README shape except for `/admin`. That is false on observed data:
  - All three profiles add `http://`. Under every frozen profile, 1416/1416 changed leaves carry `://`, against 0 under a README-shaped map.
  - The raw file has 0 scheme-prefixed tokens, so the scheme comes from the profile and is not upstream data.
- P1 also leaves 298/300 SHOPPING_ADMIN leaves without `/admin`. A reader who treats P1 as "the normal one" sees admin URLs lacking `/admin` and may blame the task URLs. In fact the raw data assumes that `/admin` comes from the value.
- No label says that `path_prefix` is the profile structurally closest to the documented SHOPPING_ADMIN shape (a path after the port).
- Candidate `:27` does say "exports scheme-less example `origin:port` values (SHOPPING_ADMIN adds" (7 words). It never connects that to the three profiles, and it omits the README WIKIPEDIA path (`README.md:91`). That omission is inert here because there are 0 WIKIPEDIA occurrences.
- **Impact.** This is a deployment-baseline misreading, not a counting error. The counts (1416 leaves, 2436 projections) are unaffected.
- **Smallest safe correction.**
  - Preferred, with no rebinding: add a candidate sentence: "All three profiles add an `http://` scheme absent from README:86–92; none is README-shaped; distinct_origins also drops SHOPPING_ADMIN's `/admin`."
  - Alternative: extend the `:34` label the same way. This changes the output bytes, so the receipts would need to be re-cut.

### M3 — The prereg's model-error disclaimer covers only P2/P3, which implies P1 is a control (prereg tradeoff; already mitigated in output)

- `plans/round-29-claims.md:40`: "P2/P3 sensitivity profiles are not deployment recommendations or model errors." (10 words). Combined with `:31`, which names only two profiles as sensitivity, P1 falls outside the disclaimer.
- The emitted LIMIT `:44` and candidate `:18` cover all three profiles, and candidate `:66` says "never counted as defects, model errors or task invalidity." (9 words).
- **Classification.** This is a tradeoff confined to the frozen prereg. The shipped artifacts already correct it. The only correction needed is the M1 sentence; nothing else.

### M4 — The candidate's operational rule prescribes a deployment-side step that the instrument refuses (fixable wording defect in the unadmitted candidate)

- Candidate `:71`: "with the run's own value map" (6 words). Command 6 shows that the instrument rejects any value map other than the frozen synthetic one, with `snapshot_tampered`, exit 2.
- So the rule cannot be run with the cited tool. A reader may instead substitute the frozen synthetic output as a stand-in baseline.
- Candidate `:72`: "non-URL changed leaf (`must_include`, annotations) is intended" (7 words). This frames a rewrite caused by upstream global replacement as a possibly unintended annotation, which leans toward attributing task error. By contrast, `:57` correctly defers score effects to runtime scope.
- Rule (4) at `:74` ("because text replacement would break JSON or cascade.", 8 words) is a value-map recommendation. It comes from S071 semantics, not from the profiles, so it does not contradict "profiles are not deployment recommendations". I classify it as an acceptable tradeoff.
- **Smallest safe correction.**
  - At `:71`, add: "via an independent re-projection; `plans/config_projection.py` audits only the three frozen synthetic profiles and exits 2 on any other map".
  - At `:72`, replace "is intended" with "is expected from global text replacement (an upstream generator property, not an annotation error)".

### M5 — The JSON key `index_mapping.violations` frames upstream-conformant naming as a violation (fixable naming defect, low)

- `config_projection.py:290`: "index_violations = [{"output_index": i, "task_id": task_id}" (6 words). The key is emitted in JSON and as `INDEX {"…", "violations": 0}`.
- Under a reordered raw file, the upstream enumerate rule is behaving correctly. The output would list those tasks as "violations", inviting a data or task error reading.
- No finding is attached (command 5), the exit code stays 0, and the frozen input has 0 such entries. The current output therefore contains no false attribution.
- **Smallest safe correction.** Rename the key to `index_task_id_mismatches`. This changes the JSON bytes and the selftest assertion at `:457`, so the receipts would need to be re-cut. Alternatively, add a LIMIT: "a mismatch is upstream enumerate-position naming, not a data or task error".

### M6 — The finding id `task_population_invalid` uses the excluded word "task validity" for an input-identity check (naming tradeoff, low)

- `config_projection.py:275`: "findings.append({"id": "task_population_invalid"})" (2 words). It fires only when the list length or id set differs from 0..811 (`:274`). It does not concern task validity, which C1 excludes at `claims:16`.
- It is not emitted on the pinned inputs.
- **Smallest safe correction.** None is required for C1. A rename to `task_population_mismatch` is optional.

## Checks that held (no counterexample found)

- All emitted per-profile effects are reported as `stimulus_observations` or counts, never as findings. The 697 `//` junctions under `trailing_slash_sensitivity` agree with my census and are routed to exit 0.
- Every finding is scoped to a profile or the population. None names a task or a model, and none appears in the per-task records.
- The per-task records (`output_index`, `task_id`, `index_equals_task_id`, `would_be_file_sha256`, `projected_task`, `changed_leaves`) carry no score, pass/fail, or error field.
- `claims:55`, "Output must name scope and profiles' synthetic purposes." (8 words), is met: `purpose` and `stimulus_class` are present per profile, alongside LIMIT `scope`. However, all three profiles share one identical `purpose` string, so `stimulus_class` alone carries the distinction (see M2).

## Impacted axes

- coverage/constructs (C1): stimulus versus baseline provenance wording only. The counts (812 / 3 / 2436, 1435 occurrences, 1416 leaves) are unaffected.
- novelty (7 held) and calibration (8 held): unaffected, as long as no F-forecast is re-scored against a "neutral equals conforming" reading.
- No model-performance, task-validity or deployment axis is claimed or touched.

## [INFERENCE] (not observed)

- Whether a runtime adds a scheme to scheme-less README-style values.
- Whether `/admin/admin` (2 leaves under the README-shaped counterfactual) routes correctly on Magento.
- Whether a browser preserves `//`.

I executed no evaluator, browser or site.

## Flip condition

M1, M2 and M4 become moot when the candidate carries the "no baseline / neutral equals synthetic non-deployment" sentence, the scheme and `/admin` disclosure, and the reworded `:71`/`:72`. M5 becomes moot with the rename or the LIMIT. None of these requires editing the pinned manifest, profiles or prereg bytes.

VERDICT: PARTIAL
