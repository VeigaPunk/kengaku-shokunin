writer: KengakuR29-2.FCritUnits-2

# FCritUnits — adversarial unit-pooling attack on integrated round-29 C1

Seat FCritUnits (critic, axis novelty), actual writer KengakuR29-2.FCritUnits-2. Read-only leaf; wrote only
this report and `.ufo/waves/round-29/scratch/falsify/FCritUnits/` (`census.py`, `census.json`,
`crosscheck.py`, `crosscheck.json`) plus `/tmp/fcu.json`, `/tmp/fcu.sum`.
**Production source not read**: `plans/config_projection.py` was only hashed (`sha256sum` →
`5673405e…12e3`, equal to the freeze pin). My census derives from the generator bytes, raw input and
profiles; the instrument was compared through its `--json`/`--summary` OUTPUT only.
Tooling: no installs or updates; python3 stdlib only.

## Attack

Target units: occurrences 1435, leaves 1416, tasks 812, per-token task sum 834, projections 2436,
would-be artifacts 2439. The attack had three parts. First, re-derive every unit independently and look for
any place where one unit is reported under another unit's name, or where units are summed across
non-additive boundaries. Second, check that each bridge between units is present in the shipped text.
Third, find the strongest counterexample in the summary, the candidate (sha256 `7006b93d…53dc`, equal to
the freeze pin), the freeze file and the build receipts.

## Commands (all exit 0)

- `python3 plans/config_projection.py --json > /tmp/fcu.json` produced sha256 `c8da0c5a…4630`, equal to
  `candidate-freeze-v1.json` `json_output_sha256` and `build-json-sha256.txt`.
- `python3 plans/config_projection.py --summary > /tmp/fcu.sum`, then `diff` against `build-summary.txt`
  minus its final `exit=0` line: identical.
- `python3 scratch/falsify/FCritUnits/census.py`: independent census of the raw text, string leaves and
  three sequential `str.replace` projections.
- `python3 scratch/falsify/FCritUnits/crosscheck.py /tmp/fcu.json`: compares the instrument JSON against
  my census at the occurrence, leaf, task, projection and artifact levels.

## Independent reconciliation (observed)

| quantity | unit | census | instrument output |
|---|---|---|---|
| tasks / distinct ids | tasks | 812 / 812 | 812 / 812 |
| token matches in raw text (G/R/S/SA/W/M) | occurrences | 385/336/281/300/0/133 = 1435 | same; `occurrence_provenance` len 1435 |
| matches inside JSON keys | occurrences | 0 | `occurrence_roles {"value":1435}` |
| token-bearing (= changed) string leaves | leaves | 1416 of 10869 | 1416; 1416 distinct `json_pointer` in provenance |
| leaves with >1 occurrence | leaves | 13, holding 32 occurrences, surplus 19 | 13; provenance pointer surplus 19 |
| leaves with ≥2 distinct tokens | leaves | 0 | not emitted |
| per-token leaves (G/R/S/SA/W/M) | leaves | 385/323/275/300/0/133 = 1416 | same |
| per-token tasks | tasks | 204/128/192/182/0/128, sum 834 | same; provenance per-token distinct tasks sum 834 |
| tasks by distinct-token count | tasks | 1 token: 790; 2 tokens: 22; 3+: 0 | 22 (GITLAB+REDDIT 17, REDDIT+SHOPPING 5) |
| 834 bridge | tasks | 790 + 2×22 = 834; 834 − 812 = 22 | not emitted |
| projections | task/profile | 3 × 812 = 2436 | 2436; 812 `tasks[]` per profile |
| per-task would-be file digests | files | 812 per profile | 812/812 match `json.dumps(item, indent=2)` UTF-8, all 3 profiles |
| whole-text would-be `test.json` | files | 1 per profile run | only as `projected_text_sha256` (matches UTF-8 projected text) |
| file writes per run / across 3 runs / distinct paths across 3 runs | writes; paths | 813 / 2439 / 813 | 813 per profile (summary line 4) |
| non-URL changed leaves | occ / leaves / tasks | 62 / 61 / 18 | 61 leaves |
| token followed by `/` (`//` junctions under trailing slash) | occ / leaves / tasks | 697 / 678 / 462 | 697 |
| `__last_url__` | occ / leaves / tasks | 65 / 65 / 55 | 65 (no unit label) |
| `__page__` | occ / leaves / tasks | 12 / 12 / 9 | 12 (no unit label) |

Every instrument number agrees with the census in its own unit. No instrument output, summary line,
candidate cell or freeze field reports one unit under another unit's name, and none sums a non-additive row.
The cross-profile figures 4305 occurrences and 4248 leaves (`R29CritCountUnit.md:41`) equal 1435×3 and 1416×3.

## Mismatches and objections

### Candidate entry (frozen bytes `7006b93d…`)

1. **834 is attributed to `--summary` but the summary never emits it.** Line 36 introduces the table with
   "`python3 plans/config_projection.py --summary`, exit0, 0 findings, identical per profile except digests:"
   (11 words). Line 42 then gives "tasks carrying each token (not additive: sum 834, distinct 812)" (10 words).
   The value 834 does not appear in either output. `rg -c '(^|[^0-9a-f])834([^0-9a-f]|$)' /tmp/fcu.sum`
   exits 1, and a recursive scan of `/tmp/fcu.json` finds no value equal to 834. It is a reader-side sum. The bridge from 834 to 812, which is 22 two-token
   tasks, is stated nowhere in the candidate, summary or JSON. Classification: **fixable defect**
   (provenance labeling). The arithmetic is correct.
2. **The 1435-to-1416 bridge is missing.** Line 43, "changed string leaves / of all string leaves / with >1
   occurrence" (12 words), gives 13. Line 41 gives 1435 and line 43 gives 1416, but 1435 − 1416 = 19 cannot be
   derived from 13. It needs 32 occurrences in those 13 leaves, which neither the candidate nor the summary
   states. Line 50, "Units are distinct: an occurrence is a text match, a leaf is a decoded string value, a task is
   one of 812." (22 words), names the units but gives no reconciliation. Classification: **fixable defect**
   (completeness). The prereg's "do not pool units" rule is still met.
3. **Two rows carry no unit.**
   - Line 46, "other `__…__` markers, not env tokens" (6 words), gives 65 and 12. These are occurrences. In
     tasks they would be 55 and 9.
   - Line 48, "value-`/` then raw-`/` junctions (`//`)" (5 words), gives 697. That is occurrences. The same row
     counted in leaves is 678 and in tasks is 462.

   Line 50 defines only occurrence, leaf and task, so these two rows are open to being read in the wrong unit.
   Classification: **fixable defect**.
4. **The 61 non-URL leaves can be misread as 62.** Lines 55–56 say "61 changed leaves are `must_include` answer
   strings and one raw annotation" (11 words, across a line break). One reading is 61 + 1 = 62. The observed
   split is 60 + 1 = 61 leaves, carrying 62 occurrences in 18 tasks. Classification: **fixable defect**
   (wording).

### Summary / build receipt `build-summary.txt`

5. **The artifact unit is ambiguous and the 2439 derivation is a write count, not a file count.** Line 4 says
   "upstream also writes one whole test.json per profile (813 would-be artifacts per profile)" (13 words). The
   generator (lines 17 and 22) writes to the fixed path `config_files/test.json` and to
   `config_files/{idx}.json`. Three profile runs into one checkout therefore make 2439 write events over
   813 distinct paths, each overwriting the previous run.
   - The 2439 figure appears only in `build/R29CritClaimScope.md:102`, "which is 813 would-be artifacts per
     profile and 2439 across the three." (12 words). It is not in the summary, the candidate or the freeze file.
   - The JSON digests 812 per-task files per profile. The 813th artifact appears only under a different
     name, `projected_text_sha256`.

   Classification: **fixable defect** (labeling). The 2436 projection unit itself is correct and is labeled at
   summary line 3.
6. **The per-token task rows carry no non-additivity guard.** Summary line 10 (`TASKS_WITH_TOKEN`) and the
   per-profile `changed_tasks_by_token` lines (21, 32, 43) give no distinct total next to the row and no
   two-token count. `R29CritCountUnit.md:101` already asked for this as a repair: "rows carrying all three
   units, plus distinct-task totals that are not sums of the per-token rows." (16 words). The distinct total
   812 exists on line 8, but the 22 that bridges 834 to 812 does not. Classification: **fixable defect**.
7. **Additivity of `changed_leaves_by_token` rests on an unemitted precondition.** The per-token leaf counts
   sum to `changed_leaf_count` 1416 only because 0 leaves carry two distinct tokens. Neither the summary nor
   the JSON emits that 0. In JSON `changed_leaves[].tokens` is a set of distinct tokens: task 431
   `/431/start_url` shows `["__SHOPPING__"]` although it holds 3 occurrences. So summing `len(tokens)` gives
   1416 leaf/token pairs, not 1435 occurrences. Classification: **fixable defect** (labeling). It is
   [INFERENCE] that a future input with a mixed-token leaf would make the by-token leaf sum exceed the leaf
   count. No such leaf was observed.

### Freeze file `candidate-freeze-v1.json`

8. **No unit defect.** The freeze carries only digests. The candidate, instrument and `json_output_sha256`
   pins all reproduced (see Commands). The freeze does not pin `build-summary.txt`, which is the output the
   candidate table cites. The rerun summary is byte-identical to that receipt, so nothing differs today.
   Classification: **tradeoff** for this review (outside the unit axis), noted for completeness.

### Build-wave reports (evidence, not proof)

9. **Wrong leaf count.** `build/R29TokenWikipedia.md:72` says "19 leaves carry two occurrences: 13 REDDIT,"
   (7 words) and `:181` says "which reconciles with 1,435 occurrences minus 19 second-occurrences;"
   (8 words). Observed: 13 leaves, not 19. REDDIT accounts for 8 of them (tasks 66, 604, 608, 609, 625, 681,
   682, 683) with surplus 13. SHOPPING accounts for 5 (tasks 431–435) with surplus 6. Leaves 431, 604, 609 and
   681 hold 3 occurrences and leaf 682 holds 4. The 19 surplus therefore splits into 13 second occurrences and
   6 third-or-fourth occurrences. Classification: **fixable defect**. The report confuses the leaf unit with
   the surplus-occurrence unit.
10. **Pooled counts presented as "not pooled."** `build/R29TokenGitlab.md:201` says "Unit accounting, not
    pooled: 385 occurrences per profile → 1155 replacement occurrences over the" (14 words). Line 203 says
    "profiles = 612 affected task/profile projections of 2436 (25.123%)." (9 words). Every per-profile count is
    identical, so ×3 adds no observation: 612/2436 = 204/812. This contradicts summary line 3, which says
    "not independent trials". Classification: **tradeoff**. The arithmetic is correct and the three-profile
    unit is named, but it should not be cited as three observations.
11. **The name `changed-leaf token counts` collides between reports.** `build/R29Task097.md:159` says
    "changed-leaf token counts sum to 1435 = whole-text counts;" (9 words). That is the occurrence unit,
    while the summary's `changed_leaves_by_token` (summary line 20) is the leaf unit and sums to 1416.
    Classification: **fixable defect** (naming) in that report only.
12. **The artifact count conflicts with the summary.** `build/R29Task399.md:157` says "artifacts 812;
    task/profile projections 2436; `test.json` texts 3;" (8 words), so per-profile artifacts are 812 there,
    but summary line 4 gives 813. Both are internally consistent, because 812 + 1 `test.json` = 813. The same
    label carries two values. Classification: **fixable defect** (labeling), resolved by correction 5.
13. **A structural fact is presented as a coincidence.** `build/R29Task399.md:72` notes "19 is also the number
    of" (6 words) space-preceded occurrences. My census shows all 19 surplus occurrences are the second-or-later
    tokens in `|AND|`/`|OR|`/`,`-joined leaves. Non-first tokens are preceded by a space, so the equality is
    structural. Classification: no defect; observation only.

## Strongest counterexample

A reader takes the candidate table at its line-36 word that the rows come from `--summary`, sees
834 on line 42, and runs `--summary` to check it. 834 is absent. A reader who tries to reconcile line 41 (1435)
with line 43 (1416, of which 13 leaves have more than one occurrence) cannot get to 19. A build-wave seat
(`R29TokenWikipedia.md:72`) made exactly this mistake and reported 19 multi-occurrence leaves. This shows that
the missing bridge has already produced a wrong unit count inside the round. The instrument and candidate
numbers stay correct, so the defect is in the frozen candidate's reconciliation and provenance text, not in
the measurement.

## Impacted axes

- **Coverage/constructs (C1):** the measurement survives. Every unit reproduces independently, including
  2436 projected objects and 2436 would-be file digests.
- **Provenance:** affected by items 1 and 5.
- **Clarity/no-pooling contract (prereg line 71):** satisfied by the output. The candidate text is weakened
  by items 2, 3, 4 and 6.
- **Novelty:** held at 7 and unaffected.

## Smallest safe correction (wording/output only, no new gate)

- **Candidate line 42:** "(not additive: sum 834 = 790 one-token + 2×22 two-token tasks; distinct 812; derived
  from TASKS_WITH_TOKEN)".
- **Candidate line 43:** append "; those 13 leaves hold 32 occurrences, so 1435 − 1416 = 19 surplus".
- **Candidate line 46:** "occurrences: `__last_url__` 65, `__page__` 12".
- **Candidate line 48:** "697 occurrences (678 leaves, 462 tasks)".
- **Candidate lines 55–56:** "61 changed leaves (60 `must_include` strings, 1 raw annotation; 62 occurrences,
  18 tasks)".
- **Summary line 4:** "813 file writes per profile run to 813 fixed paths; runs overwrite, so 3 runs ≠ 2439
  coexisting files". Optionally emit `tasks_with_multiple_distinct_tokens=22` and
  `changed_leaves_with_multiple_distinct_tokens=0`.
- **JSON:** rename `changed_leaves[].tokens` to `distinct_tokens`.

Any candidate edit changes its bytes and requires a new freeze and second-seat reread. That is a process cost,
not a correctness tradeoff. The build-report errors (items 9, 11, 12) need no production change, only
non-citation.

## Observed vs inferred

All counts above are observed from the named commands and files. [INFERENCE] items: the
future-mixed-token-leaf consequence in item 7, and the claim that reader-side recomputation would fail as
described in the counterexample. The latter is supported by `R29TokenWikipedia.md:72` but not tested on a
reader.

VERDICT: PARTIAL
