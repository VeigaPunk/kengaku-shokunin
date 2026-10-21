# FConnector — round-28 falsification: ConnectScope / ConnectEvidence recheck

- Seat: `KengakuR28.FConnector` (connector, leaf, read-only over production). Date 2026-10-21.
- Lane root: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
- Candidate: `.ufo/waves/round-28/drafts/webarena-task-spec-audit.md`, sha256
  `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8` (matches
  `.ufo/waves/round-28/candidate-freeze.json`). Canonical candidate
  `corpus/knowledge/webarena-task-spec-audit.md` is **ABSENT** — not admitted.
- Read-only over production. Only this report and scratch evidence under
  `.ufo/waves/round-28/scratch/FConnector/` were written. No installs/updates (tools: none).
- Inputs: `build/ConnectScope.md`, `build/ConnectEvidence.md`, `build/RevURLContract.md`, the
  candidate draft, `plans/round-28-claims.md` (incl. Amendment 1), `corpus/lessons/round-28.md`,
  `corpus/evidence/round28-calibration/` receipts, the pinned r28 fixture and the delivered
  `plans/registry_check.py` / `plans/benchmark_spec_audit.py` (read as text; no imports of upstream
  code). This is author-side falsification, not outside closure and not a Q10 pass.

## Axes

- C1: legacy novelty → canonical coverage/constructs, held 7.
- C2: calibration, held 8.

Both scores stay held. Nothing below reprices either axis; the findings are disclosure and
wording gaps, not counter errors.

## Evidence and findings

### F1 — ConnectScope recheck: PASS

All pinned PROVINCE hashes still match the report table: chousa `cf7826a4…bbec`, tameshi
`cd11b529…7a44`, kotoba `c1fa9d97…e524`, kake `f71df98e…9917`, kaidoku `dbf757fe…ed97`,
souji `3a2364d7…bda8`, kengaku `eed536c4…37b1`. The lexical census reproduces: only
`kengaku-shokunin/PROVINCE.md` (10) and `kasegi-shokunin/PROVINCE.md` (1, line 47 routes
“kengaku — LLM evaluation and benchmarks”) are non-zero; chousa PROVINCE:10-11 routes
model-quality/evaluation claims to kengaku. The decisive C2 prior art is present and local:
`kagi-shokunin/PROVINCE.md:55` (`corpus/sources-census.sh`) and `:83` (“checks citations, not
vendor truth”), and `kumitate-shokunin/PROVINCE.md:15` (`sources-check.mjs`); tameshi PROVINCE:14-16 reserves
“every lane's gate … its own” and requires two independent lanes before a pattern is general.
`souji-shokunin/PROVINCE.md` still has no link-drift hit (grep exit 1). The fixture hashes match
`plans/fixtures/r28/webarena/manifest.json` (`test.raw.json 7b50386f…7652`, `evaluators.py
e23edb39…0c22`, `helper_functions.py ec758da4…e275`, LICENSE `c71d239d…0ab4`). Selected-16
minima recompute exactly (`389,590,132,173,44,552,681,791,556,356,7,377,759,424,97,399`);
composition is exact 1 / must_include 2 / fuzzy 2 / program_html 9; 36 N/A tasks, 36 nonempty
`string_note` fields all with `string_match`. No sibling claim to benchmark task-spec ground was
found at PROVINCE level; ConnectScope records no sibling file or benchmark-environment change
(this seat did not re-run a fleet-wide VCS census). ConnectScope’s proposed adjacent-routing
paragraph is present in the lesson (82-85), carrying the kagi/kumitate local-gate note; it stays
in the lesson and does not enter the candidate or C2’s frozen counts. ConnectScope’s own
limitation (PROVINCE metadata only, lexical census, no prior-art check) remains accurate.

### F2 — ConnectEvidence E1 (S050 baseline mismatch): PASS, integrated

The delivered checker reproduces the baseline red exactly: `registry-baseline-red.stdout` has
`source_rows_checked=13`, `knowledge_files_expected=35`, `reference_links=12`,
`mismatch_sources=2`, three findings — S038 `cited_not_mined`, S038 `missing_used_by`
(`corpus/knowledge/attribution-interval-calibration.md`), S050 `missing_used_by`
(`corpus/knowledge/extraction-policy-comparison.md`). `registry-s050-only-red.stdout` leaves one
mismatch (S038), and `registry-s038-only-delta-green.stdout` is clean. `registry-current.stdout`
is `0/0/12/13/35`. This is the shown-able-to-fail M65 sequence, and S050 is separately disclosed
(lesson M67), not folded into S038. The delivered `corpus/SOURCES.md` diff versus
`b9b24796…` changes only S038 status+used-by and S050 used-by among the frozen rows; the other
hunks are the new S061–S066 rows, the round28 search addendum, and append-only knowledge errata
(including S064–S066). ConnectEvidence’s E1 is integrated and the claims’ forecast F5 is
resolved false, as the receipts show.

### F3 — ConnectEvidence E2 / task247: verified, but not carried as an explicit limitation

Independently recomputed from the pinned raw JSON (stdlib `json` only):

- 812 tasks; 205 `url_match`; 607 non-`url_match`; exactly **1** non-`url_match` task has a
  nonempty `reference_url`: task **247** (`shopping_admin`, `eval_types:["string_match"]`,
  `reference_answers.fuzzy_match:"N/A"`, `reference_url` at test.raw.json:7832
  `"Valorie doesn't have a email in the system"`, `string_note` at :7834
  `"There is no negative review for Zoe products"`).
- `URLEvaluator` is the only reader of `reference_url` (evaluators.py:213), `evaluator_router`
  builds only declared `eval_types` (evaluators.py:355–374), and the N/A branch passes only
  `string_note` to `ua_match` (evaluators.py:152–163). Task 247’s `reference_url` is therefore
  unread; the two unachievability rationales cannot both be seen by the scorer.
- Controls reproduce: all 36 N/A tasks are `string_match`-only; all 36 nonempty `string_note`
  fields belong to those N/A tasks; the nine `url_match` tasks without `url_note` (174–182) use
  the implicit `"GOLD in PRED"` default, not an unread field. Task 247 is **not** in the
  selected 16; the selected sample’s only N/A task is 791, whose `reference_url` is empty.

The observation is explicit and correctly framed in the build package: `RevURLContract.md:23`
(C11 “dead fields — never read”), `:43` (607 non-url tasks, exactly one non-empty = task 247),
`:56` (S7: “report as dead-field observation, NOT a task defect”), `:93-94` (limitations 6–7),
`:104` (recommended dead-field report); ConnectEvidence E2 says “Under the prereg this is an
observation and a limitation, not a benchmark FAIL.” That is the right classification.

It is **not** in the integrated candidate or its measured limits:

- The draft contains no `247`, no `reference_url`, no “dead field”/“unconsumed” wording; its only
  nearby guard is line 127, “do not interpret field presence as validity.”
- The audit summary’s five `LIMIT` lines do not include field consumption; the JSON `tasks`
  records preserve `reference_url`, so the field is not lost — it is present but unread.
- The lesson has no task247/dead-field mention. Its M70 “unconsumed” hit is the `program_html`
  empty-list correction, not URL dead fields. The candidate’s line 61 “The whole raw
  population remains separately inventoried” and line 108 “schema findings 0” can be read as
  complete structural coverage; the dead-field fact is a structural consequence not surfaced.

Secondary build-report number notes (not integrated, no candidate effect): RevURLContract:43’s
“`reference_url`/`url_note` keys” is imprecise — 0 non-`url_match` tasks carry a `url_note` key
(196 `url_match` tasks do; 174–182 lack it). Its “REDDIT 83” is an occurrence count; 71 tasks
contain the REDDIT token and the five token counts sum to 205 tasks. The 607/1 dead-field count
and task247 observation are correct and unaffected.

### F4 — Shared reference-link analogy: not merged into C1/C2 causal proofs

The analogy appears only in `build/ConnectEvidence.md` (“a structural analogy only. The two
populations, causes and counting commands stay separate”). No candidate, lesson, checker or
audit text uses it. The candidate’s calibration section says “Shared sources/lesson bookkeeping
are partitioned by precise rows/cells, not treated as one combined improvement” (draft:138-141);
the lesson records the row/cell partition and the two mutable cells (S038 status/used-by; S050
used-by) plus new S061–S066 rows. The receipts enforce separate denominators:
`audit-without-c2.stdout` has identical `metrics`, `selected_task_ids` and `source_sha256` to
`audit-current.stdout`; `registry-only-delta.json` records only SOURCES.md cells and
`2 → 1 → 0` mismatch sources. The checker read-set is population JSON (13 IDs, 35 baseline
paths), `corpus/SOURCES.md`, those 35 files and used-by targets for existence checks; the audit
read-set is the pinned fixture. There
is no joint statistic, no cross-citation, and no causal claim. **The analogy does not merge the
proofs.**

One narrower shared-file coupling must be stated, not smoothed: `plans/registry_check.py:43,46`
appends `malformed_source_row`/`duplicate_source_id` findings for **any** Registry row, and
`:86` derives `mismatch_sources`/`finding_count` from all findings. A scratch copy of the final
tree (`.ufo/waves/round-28/scratch/FConnector/probe/`, green receipt `green.json`) exits 0 with
`0/0/12/13/35`; inserting one malformed new C1 row `| S061 | malformed extra |` inside
`## Registry` makes the same checker exit 1 with
`{"id":"malformed_source_row","source":"S061","line":90}`, `finding_count=1`,
`mismatch_sources=1` (`malformed2.json`). The delivered S061–S066 rows are well formed, so the
measured C2 green is unaffected; but claims:52’s “New rows do not enter its verdict” is exact
only for well-formed new rows. This is a parse-boundary coupling, not the reference-link
analogy and not a causal merge.

### F5 — No fleet-first method credit; scope stays benchmark evaluation

The candidate is lane-scoped: “The lane previously held … not a task-spec-to-scoring contract
inventory for this repository” (draft:10-12), “not a new scientific method” (draft:12-13),
“Scores stay novelty7 and calibration8; no coverage-cap relief or method-novelty score is
inferred” (draft:140-141). The lesson carries the sibling-gate correction explicitly:
“Registry gates already exist in kagi/kumitate: C2 is lane-local calibration, not fleet-first
methodology” (lesson:82-85). The candidate routes general research method to chousa, testing
patterns to tameshi, prompt-writing to kotoba, actual web-property operations to kake, and says
“Benchmark evaluation stays kengaku”; domain trees/benchmark environments remain read-only
(draft:143-146). No benchmark-site browser action, live benchmark contact, or general gate
ownership is claimed. The C1 task-spec and case work is static parsing/AST; the build reports
record no sibling file change (not independently re-censused here). **PASS** on this clause.

## Affected axes and proposed move (one, bounded)

The verified task247 observation is the one unintegrated item. Carry it explicitly as an
**out-of-sample whole-population limitation**, not a validity claim:

> One whole-population observation lies outside the 16 case audits: task 247 declares a nonempty
> `reference_url` but only `string_match`, so `URLEvaluator` never reads it and the N/A branch
> sees only `string_note`. This is a scorer-contract data inconsistency, not task invalidity and
> not a seventeenth case audit.

Place it in the candidate’s “Deterministic case audits and their limits” section (after
draft:64), and mirror it in the lesson’s residual-limitations text. Do not change the frozen
instrument in this admission cycle. If a dead-field metric is wanted later, add it as a separate
instrument change with a hand-expected selftest (one non-`url_match` task with nonempty
`reference_url` → 1; one with `url_match` → 0) and a new freeze. The checker-boundary wording in
claims:52 (“new rows do not enter”) should be narrowed separately to “well-formed new rows do
not enter the frozen coverage verdict,” because the scratch probe shows malformed new rows do
enter the global finding count.

Affected axes: C1 coverage/constructs gains the dead-field construct and an honest limit; C2
calibration gains exact separation wording. Scores stay held; no counter changes. No harm to
the other axis: the candidate path is outside the frozen baseline35, and the lesson is outside
frozen knowledge (claims:52), so the sentence adds no C2 literal reference and changes no
C1 metric.

## Risks

- The candidate is byte-frozen at `77e19d5b…`; adding the sentence changes its sha256, so Q10
  same-identity rereads are required before admission (claims Amendment 1 §6). The observation
  uses existing S061/fixture bytes, but the sentence’s count (1/812, task247) becomes a new
  candidate number and must be re-read under the same rule; no new source row is implied.
- Wording risk: “dead field” can be read as a benchmark defect. Keep the explicit “data
  inconsistency / limitation, not task invalidity” clause; do not add it to the 16 case reports
  or the selected-sample table.
- A metric addition would change `benchmark_spec_audit.py` and its freeze; defer it out of the
  current frozen cycle.
- The checker-boundary finding is wording-only unless `registry_check.py` is changed; changing
  the checker would alter the instrument sha256 and require a re-freeze. Prefer the wording fix.
- Scratch probe files are disposable; they are under this seat’s scratch and were not used as
  production inputs.

## Verification (read-only)

1. `sha256sum .ufo/waves/round-28/drafts/webarena-task-spec-audit.md` →
   `77e19d5b2683dbf36b87c8ca0ae36e5b19f281673c1c16e46abfb6ab08ac20a8`;
   `test -e corpus/knowledge/webarena-task-spec-audit.md` → absent.
2. Recompute task247: `json.load(test.raw.json)`; count non-`url_match` nonempty
   `reference_url` → 1 (247); count non-`url_match` → 607; N/A tasks → 36, all
   `string_match`-only; selected16 excludes 247; selected N/A is 791 with empty
   `reference_url`.
3. Re-read receipts: `registry-baseline-red.stdout` 2 mismatch/3 findings; `…s050-only-red`
   1/2; `…s038-only-delta-green` 0/0; `registry-current.stdout` 0/0/12/13/35;
   `audit-without-c2.stdout` metrics/selected/source_sha equal to `audit-current.stdout`.
4. Re-run the scratch probe if desired:
   `python3 plans/registry_check.py --root .ufo/waves/round-28/scratch/FConnector/probe --json`
   → exit 1 with S061 `malformed_source_row`; the clean pre-insert output is `green.json`.
5. `grep -n '247\|reference_url\|dead field'` over the candidate draft, lesson and
   `corpus/evidence/round28-calibration/audit-summary.txt` → no task247 limitation; the build
   reports `RevURLContract.md` and `ConnectEvidence.md` hold it. (The lesson’s M70 “unconsumed”
   line is a `program_html` empty-list correction, not a URL dead-field limitation.)
6. `grep -n 'analog'` over the candidate/lesson → no hit; only
   `build/ConnectEvidence.md` contains the bounded analogy.

## Limitations

- Author-side recheck; no non-author evidence and no Q10 authority.
- The dead-field count is a static field-consumption fact, not a runtime or task-validity
  result; the intent behind task247’s two rationales is unobserved.
- The scratch probe is a single malformed-row control, not a full mutation campaign; it proves
  the parse boundary only.
- The candidate may change after this report; the next reader must use the admitted bytes and
  the same-identity reread rule.

## Verdict

**PARTIAL.** ConnectScope, ConnectEvidence E1, the no-analogy-merge check, the no-fleet-first
check and the scope check all pass. The verified task247 dead-field observation is correctly
framed in the build evidence but is **not** carried as an explicit out-of-sample limitation in
the candidate/lesson limits, and claims:52’s new-row verdict wording is overbroad for malformed
rows. Both are disclosure/wording gaps, not counter errors and not validity claims.

VERDICT: PARTIAL
