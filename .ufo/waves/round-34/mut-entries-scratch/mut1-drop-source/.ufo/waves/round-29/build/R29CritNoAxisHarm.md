# R29CritNoAxisHarm — no-axis-harm / mapping critic (round 29, C1)

- Seat: R29CritNoAxisHarm (roster `KengakuR28.R29CritNoAxisHarm-2`), role critic, read-only leaf.
- Actual writer: R29CritNoAxisHarm. No production edits, no commits, no subagents, no installs/updates.
- Scratch (own): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/R29CritNoAxisHarm/{census.py,quotes.py}`.
- Scope: whether the round-29 preregistration/contract keeps the lowest-legacy-7 mapping and score hold, leaves the coverage cap unresolved, introduces no new axis split, and avoids domain bleed. This is author-side critique. It is not round admission or outside closure.

## Sources read (all lane-relative unless noted)

`plans/round-29-claims.md` (landed 31934e5); `SCORECARD.md` (§Round 25 revision, §Round 27, §Round 28, rubric, saturation);
`corpus/README.md` Frontier and round-28 sections; `PROVINCE.md` round-28 section; `SHONEN.md`;
`/home/vgpnk/Projects/shokunin/AXES.md`; `/home/vgpnk/Projects/shokunin/PROTOCOL.md` §Fleet-2 conventions;
`plans/fixtures/r29/{manifest.json,profiles.json,generate_test_data.py}` (as inert text);
`plans/fixtures/r28/webarena/config_files/test.raw.json` (as JSON data);
`.ufo/waves/round-29/build-spec.json` (seat targets); `.ufo/waves/round-29/drafts/webarena-config-projection.md` (grep only).
I did not execute or import any upstream code, did not access the network, and did not read host env or credentials.

## Commands and observed output

1. `sha256sum plans/fixtures/r29/*`: manifest `f6390b92…bf87`, generator `45ddba7b…21cd`, profiles `90fdc34d…94e018`. These match the pins in the prereg and manifest.
2. `python3 .ufo/waves/round-29/scratch/R29CritNoAxisHarm/quotes.py`: exit 0, `bad 0`. It checked 14 quotes for an exact substring on the stated line, with word counts from 3 to 13. Every quote below comes from that set.
3. `python3 .ufo/waves/round-29/scratch/R29CritNoAxisHarm/census.py` read the raw file once (sha256 `7b50386f…7652`, 880776 bytes, matching the pin) and printed:
   - raw occurrences, in occurrence units: GITLAB 385, REDDIT 336, SHOPPING 281, SHOPPING_ADMIN 300, **WIKIPEDIA 0**, MAP 133;
   - distinct `__[A-Z_]+__` tokens: exactly 5 (no `__WIKIPEDIA__`). The runtime markers `__last_url__` (65) and `__page__` (12) are separate;
   - occurrences of a token immediately followed by `/`: 225/232/110/125/0/5, which sum to 697 (by `python3 -c`);
   - tasks 812; positions where `task_id == index`: 812;
   - token-bearing string leaves by normalized path, as leaves/occurrences: `start_url` 812/818; `eval.program_html[].url` 338/338; `eval.reference_url` 205/217; `eval.program_html[].required_contents.must_include[]` 60/60; `eval.reference_answer_raw_annotation` 1/2. Tasks with a token in a leaf outside my heuristic URL-named set: 18. That classifier is mine and is not the contract's category scheme.
4. A follow-up stdlib check found: substring `WIKIPEDIA` 0 times; tasks whose `sites` include `wikipedia` 23. The start_url token sets for those 23 tasks are `__MAP__` 17 and `__GITLAB__` 6.
5. `rg -c -i -F` hit counts in the prereg and draft: `province` 0/0, `waiver` 0/0, `tied` 0/0, `stagnation` 0/0, `coverage cap` 0/0, `LOG.md` 0/0.
6. `test -e plans/config_projection.py` → absent in the lane root. No production projection output exists for me to inspect, so I did not run any production tool.

## Findings

### A. Lowest-legacy-7 mapping, score hold and no new split: holds (PASS on this sub-scope)

- The current axis state reads "capped, operability8, freshness8, adjacency8" (SCORECARD.md:908), with novelty7, calibration8, depth9 and coverage7 stated on the preceding lines. Novelty7 is a lowest axis, tied with coverage7. The prereg names "lowest legacy novelty7 → canonical coverage/constructs" (claims:11).
- The mapping stays what r25 recorded: "a mapping, not an AXES.md split" (SCORECARD.md:716). AXES.md:37 permits a split only after saturation ("saturates, the lane may retire it or split it into a sub-axis"). Coverage is at 7, so it is not saturated. The prereg adds a capability row, not a sub-axis. Result: no new split.
- The prereg's score hold reads "only for an offline source-faithful projection. Score7 held;" followed by "calibration8 and other axes unchanged." (claims:15–16). This matches the r26–r28 pattern (observable improved, score held). The stagnation nudge stays inactive: "the nudge is inactive while novelty sits below 8" (SCORECARD.md:569). Holding the score claims no +1, so the prior-art leg of the novelty rubric is not needed to *hold* 7. The prior-art question itself belongs to R29CritPriorArt.
- Preservation duty for the final row: PROTOCOL.md:515 says a non-AXES axis "is worked only if its row carries its mapping to one of the" six axes, in the same row. The final SCORECARD C1 row MUST carry `novelty → canonical coverage/constructs` in its axis cell, as r28's row did.

### B. Coverage cap unresolved: disclosure gap, fixable

The prereg has 0 hits for `tied`, `waiver`, `stagnation` and `coverage cap`. r28 stated "tied coverage/surfaces7 remains capped, no waiver." (SCORECARD.md:890), and r27 had an equivalent line. This does not invalidate the claim: a tie still makes novelty a lowest axis, and "other axes unchanged" covers coverage. But a reader cannot re-derive from the prereg alone why the canonical coverage number does not move while its constructs sub-mapping is being worked.
**Smallest correction:** the final round-29 SCORECARD section restates that coverage/surfaces7 is tied and capped by the still-open round-25 L0, with no waiver, and that the canonical coverage number is not moved by C1. No retroactive conversion.

### C. STRONGEST ACTUAL OBJECTION: the frontier advance has no PROVINCE accounting, which risks harming the coverage gap-line in either direction

- The prereg advances "README's generated-eval-config frontier" (claims:15). Its admitting-commit list ends "index/coverage and source-used-by links" (claims:95). PROVINCE.md is named 0 times in both the prereg and the draft entry. The draft proposes README text only, at draft §"Proposed README frontier text".
- Two live gap lines name this exact ground as open:
  - corpus/README.md:338: "generated eval-time configs, runtime DOM/helper/judge validity and contamination checks remain open."
  - PROVINCE.md:201: "generated configs, runtime task validity, hosted judges and contamination remain open."
- The coverage rubric's cap includes "a gap line contradicted by an artifact already in the repo" (SCORECARD.md:247). SHONEN.md also gates on PROVINCE.md staying accurate.
- **Bounded counterexample (two-sided):**
  1. Suppose the entry `knowledge/webarena-config-projection.md` and `plans/config_projection.py` land, README:338 gets the narrowed text, and PROVINCE.md:201 stays verbatim. The repo then carries an admitted artifact that projects generated configs while its province file says generated configs are wholly open. That trips the gap-line cap on coverage. Coverage is an axis the round declares "unchanged", so the no-harm admission rule fails on coverage rather than on C1's own metrics. r28 avoided this by appending "Round28 partial frontier admission" to PROVINCE (PROVINCE.md:192–202) alongside README:326–338.
  2. Suppose instead PROVINCE/README are edited to say generated configs are covered or closed. That is domain bleed into actual deployment configs, runtime behavior and env_config values, all of which C1 explicitly disclaims (claims:16–17, 37–40).
- **Smallest safe correction (no code):** add `PROVINCE.md` to the admitting-commit list. At admission, append one dated round-29 PROVINCE paragraph, and the same narrow text after README:338, stating:
  - core now holds an offline, source-faithful projection of the dce04686 generator over 812 raw tasks × 3 synthetic `*.invalid` profiles;
  - actual env_config-derived/deployment configs, runtime task validity, hosted judges and contamination remain open.
  Do not edit PROVINCE.md:201 or README:338 in place; append, as r28 did.
- Severity: this is a fixable defect, not a tradeoff the judge must reject. The flip condition is that the PROVINCE append lands in the admitting commit.

### D. Construct-coverage boundary from data: WIKIPEDIA is a population no-op (scope disclosure, not task invalidity)

- `__WIKIPEDIA__` occurs 0 times in the pinned raw file, yet 23 tasks list site `wikipedia`. Their start_urls carry `__MAP__` (17) or `__GITLAB__` (6). So across the 2436 task/profile projections, the WIKIPEDIA substitution never changes a byte under any of the 3 profiles. The distinct WIKIPEDIA origins in `profiles.json` cannot be observed in any projected task.
- **Counterexample to a plausible overclaim:** any final wording such as "six token replacements audited over 812 tasks/2436 projections" overstates population construct coverage. On the population, 5 of 6 tokens are exercised. The sixth is exercised only by the selftest's hand cases. F2's WIKIPEDIA component ("remaining six known tokens 0") is vacuously true.
- **Repair:** report WIKIPEDIA = 0 per profile as an *observed zero*, not an exclusion and not a hidden filter. State population construct coverage as 5/6 tokens, with 6/6 only in selftest.
- Do **not** infer that the 23 wikipedia-site tasks are invalid or unreachable. How the site is reached at runtime is unobserved and belongs to runtime scope.

### E. Domain-bleed exposure inside fields (already disclaimed; keep units apart)

- Token-bearing non-start/non-url leaves include `eval.program_html[].required_contents.must_include[]` (60 leaves) and `eval.reference_answer_raw_annotation` (1 leaf, 2 occurrences). C1 may report the projected values. Whether a changed `must_include` alters any evaluator outcome is scorer/runtime behavior outside C1. Do not claim a scoring effect.
- The trailing-slash profile yields `…/` + `/…` at 697 token-followed-by-slash occurrences. The prereg's line 40 already says sensitivity profiles are not deployment recommendations or model errors. The final text must not convert 697 into a defect count.
- Units differ (start_url 812 leaves vs 818 occurrences). This supports the prereg's ban on pooled units.

### F. Remaining axes

- **Calibration:** F1–F5 are derivable from committed bytes, and the prereg already disclaims calibration gain. F5 is guaranteed by "Score7 held" itself, so it should be scored but tagged non-informative. Score held at 8.
- **Freshness:** the prereg and draft mention `LOG.md` 0/0 times. The freshness rubric needs a round LOG entry with a re-verification result for the claims touched. Until that lands, freshness8 is held but unverified.
- **Depth and operability:** no claim, and the prereg introduces no harm. The CLI exit map 0/1/2 fits the operability rubric.
- **Adjacency:** deferred to R29ConnectScope. Excluding env_config and deployment from the projection keeps serving/deployment ownership outside this lane.

## Unknowns preserved

- No production tool output exists yet (absent in lane root), so findings D and E are pre-output data facts from my own census, not checks of the instrument.
- Whether L1 already plans a PROVINCE append outside the prereg text is unknown. The prereg and draft contain 0 references to it.
- The r28 admission is operator-reported ground truth and was not rechecked.

VERDICT: PARTIAL
