writer: KengakuR29-2.FPreserveR28-2

# FPreserveR28 — round-28 preservation attack against the integrated round-29 tree

Seat: `KengakuR29-2.FPreserveR28-2` (falsify leaf, no delegation). Lane root:
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Item: preservation attack — re-run the four
r28 counting commands read-only on the integrated round-29 tree and compare against the r28
receipts in `corpus/evidence/round28-calibration/` and the round-28 rows of `SCORECARD.md`.

Independence statement: I did **not** read the production source of `plans/config_projection.py`
(only `--help`, `--summary`, `--json` executions and its sha256). I also did not read the source of
`plans/benchmark_spec_audit.py`, `plans/registry_check.py` or `plans/state_check.py`. The one
production/fixture source I did read is the r28 acceptance harness
`plans/fixtures/r28/acceptance.py` (lines 1–123), to confirm it mutates nothing in the lane before
re-running it. All comparisons below are against tool *output* and receipt bytes, not source text.

## 0. Environment, tool installs, and lane state

- Host: linux, x86_64; `python3` = CPython 3.14.8 (stdlib only).
- **Tool installs: none.** No `pacman` transaction was attempted (host-wide pacman pause honored),
  no `uv tool install`, no new binary. Nothing to record beyond "no install".
- Lane HEAD at attack time: `56fd949a6478342531e61f4feecb4a685d831640`
  (`git rev-parse HEAD`; `git log --oneline -1` → "round-29: freeze knowledge candidate v1 for
  falsification"). This equals the revision label the task asked me to census, so the census label
  names the real HEAD commit.
- `git status --porcelain` at 16:48Z showed only untracked entries:
  `.ufo/waves/round-29/{falsify-assignments.json,falsify-dispatch-attempts.json,falsify-dispatch.json,falsify-registry-record.txt,falsify-spawn-response.txt,falsify-spec.json,falsify/,scratch/}` and
  `corpus/lessons/round-29.md`. No tracked file is modified (M3 below concerns that untracked file).
- `git diff --name-status ed26bdf5d924755697cd6812129be2fa441c42a3..56fd949a` — the only tracked
  changes are `corpus/SOURCES.md` (+4 rows) and 6 new files under
  `corpus/evidence/round29-calibration/`. **`plans/benchmark_spec_audit.py`,
  `plans/registry_check.py`, `plans/state_check.py`, `plans/round28_census.py`, `SCORECARD.md` and
  `PROVINCE.md` are byte-unchanged between the round-28 pin and HEAD** (absent from the diff).

## 1. The attack (commands, exits, and where the output was captured)

All four commands were run read-only from the lane root; no lane file was written by them. My own
scratch dir: `.ufo/waves/round-29/scratch/falsify/FPreserveR28-2/`.

| # | command (cwd = lane root) | exit | captured at |
|---|---|---|---|
| A1 | `python3 plans/benchmark_spec_audit.py --summary` | 0 | `scratch/…/audit-current.txt` |
| A2 | `python3 plans/benchmark_spec_audit.py --selftest` | 0 | `scratch/…/audit-selftest-current.txt` |
| A3 | `python3 plans/registry_check.py --summary` | 0 | `scratch/…/registry-current.txt` |
| A4 | `python3 plans/registry_check.py --selftest` | 0 | `scratch/…/registry-selftest-current.txt` |
| A5 | `python3 plans/state_check.py --summary` | 0 | terminal (`VERDICT: PASS — all comparable frozen assertions match`) |
| A6 | `python3 plans/state_check.py --json` | 0 | `scratch/…/state-current.json` (186 167 B) |
| A7 | `python3 plans/round28_census.py --revision 56fd949a6478342531e61f4feecb4a685d831640` | 0 | `scratch/…/census-final.json` (sha256 `c3fb39703301e51b…`) |
| A8 | `python3 plans/fixtures/r28/acceptance.py --root <lane> --out <scratch>/r28-acceptance` | 0 | `scratch/…/r28-acceptance/` |

A8 is the r28 author's own 11-stage acceptance harness. I read it first to confirm safety: it
writes only to `--out` and to a `tempfile.TemporaryDirectory` baseline export, and it obtains the
baseline with `git archive` (read-only). It makes no lane VCS mutation and no lane file write, so
re-running it is within the read-only leaf contract.

## 2. Preservation result per r28 claim (observed values, not inferences)

### 2.1 C1 (SCORECARD.md:890, :914–915) — 812/5/27/16/651 — PRESERVED

`SCORECARD.md:890` claims the instrument "inventories812 tasks/5 evaluator-type sets/27 strata/16
selected case audits/651 page targets, exit0"; `SCORECARD.md:914–915` repeats it as
"812 tasks/812 IDs/5 type sets/27 strata/16 cases/651 targets/0 findings".

Observed now (A1, exit 0):
`TOTAL task_count=812 distinct_task_ids=812 site_eval_strata=27 selected_count=16 program_html_targets=651 findings=0 exit=0`
and `EVAL_TYPE_SETS` carries exactly 5 keys (`program_html` 282, `program_html,url_match` 129,
`string_match` 325, `string_match,url_match` 10, `url_match` 66) — the "5" of 812/5/27/16/651 is the
evaluator-type-set count, and it is 5.

Byte-level preservation against the r28 receipts:

| artifact | current sha256 (first 16) | r28 receipt | identical |
|---|---|---|---|
| `benchmark_spec_audit.py --json` (1 900 693 B) | `ad53df24c06e58d9` | `round28-calibration/final-acceptance/audit-current.stdout` and `…/complete-acceptance/audit-current.stdout` | **True** (both) |
| `benchmark_spec_audit.py --selftest` (`cases=67`) | `c3d54a97b46c6c86` | `…/final-acceptance/audit-selftest.stdout` | **True** |
| `benchmark_spec_audit.py --summary` | `dbbffbe818e1f5ad` | `…/audit-summary-final.txt` | True except the receipt's own trailing blank line + `exit=0` line (1 505 B vs 1 513 B) |
| `benchmark_spec_audit.py` source bytes | `b7524c2f316f5ba8…` | `round28-calibration/complete-acceptance/acceptance.json` → `instrument_sha256` | **True** |

### 2.2 C2 (SCORECARD.md:891, :914–915) — 13/35/12/0 — PRESERVED

`SCORECARD.md:891` claims "13 rows/35 paths/12 reference links"; `:914–915` claims
"13 rows/35 paths/12 links/0 mismatched rows".

Observed now (A3, exit 0):
`TOTAL source_rows_checked=13 knowledge_files_expected=35 reference_links=12 mismatch_sources=0 finding_count=0 exit=0`.

Byte-level: `registry_check.py --json` (4 176 B) sha256 `f6f53dc28d406a37` is **identical** to
`round28-calibration/{build,complete,final}-acceptance/registry-current.stdout`;
`registry_check.py --selftest` (`cases=15`) sha256 `06700d9ae79af2cd` is **identical** to
`…/final-acceptance/registry-selftest.stdout`; `--summary` is identical to
`registry-summary-final.txt` except the receipt's trailing `exit=0` line (230 B vs 238 B);
`registry_check.py` source sha256 `fc388c332d4e37f8…` matches r28's `acceptance.json` binding.

### 2.3 Selftest counts (SCORECARD.md:915 "fixed selftests67/15 exit0") — PRESERVED

A2 → `SELFTEST clean cases=67 …` (exit 0); A4 → `SELFTEST clean cases=15 …` (exit 0).

### 2.4 Historical state (SCORECARD.md:903, :941–942) — 329/318/0/6/5 — PRESERVED

`SCORECARD.md:903` claims all 329 historical checked IDs preserve 318 MATCH / 0 MISMATCH /
6 SUPERSEDED / 5 offline, with the original 26 OUT_OF_POPULATION IDs retained.

Observed now (A5/A6, exit 0): `assertions=329 match=318 mismatch=0 superseded=6
offline_unverifiable=5`, and the census `historical_state.summary` (A7) is
`{assertions:329, match:318, mismatch:0, superseded:6, offline_unverifiable:5, out_of_population:31}`.

Per-ID diff, current `state_check.py --json` vs the r28 final receipt
`round28-calibration/final-acceptance/historical-state-current.stdout` (357 IDs) and vs
`round28-calibration/historical-scope-restored.txt` (358 IDs):

- IDs removed: **0**.
- Verdict changes: **0** (no MATCH↔SUPERSEDED↔OFFLINE reclassification, no new MISMATCH).
- IDs added: exactly 2, both OUT_OF_POPULATION disclosures created by round 29 itself —
  `P2e.out-of-population.file.evidence/round29-calibration/` and
  `P2e.out-of-population.file.lessons/round-29.md`.
- OOP breakdown of the current 31: **26 old + 3 round-28 + 2 round-29** — the 26 original IDs
  named at `SCORECARD.md:903` are all still present with the same verdict; the 3 round-28 ones are
  `…/file.evidence/round28-calibration/`, `…/file.knowledge/webarena-task-spec-audit.md`,
  `…/file.lessons/round-28.md`. This is exactly the additive-disclosure mechanism r28 declared.
- Two observed-value changes only (both still MATCH): `P2c.box.2.pointer.1` `target_lines` 510→570
  (`LOG.md:7`, anchor still resolves) and `P2c.box.4.pointer.1` `target_lines` 190→202
  (`PROVINCE.md:129`, anchor still resolves). Both files grew by committed lane edits after the r28
  acceptance run; `PROVINCE.md` is unchanged between `ed26bdf` and HEAD, so its 12 extra lines came
  from the round-28 commit itself.

### 2.5 P4 subset (SCORECARD.md:942 "P4 exactly51 (48 MATCH/1 SUPERSEDED/2 offline)") — PRESERVED

Census `historical_state.p4_ids` = 51, `p4_verdicts` = `{MATCH:48, OFFLINE_UNVERIFIABLE:2,
SUPERSEDED:1}`. Independently recomputed from the current `state_check.py --json`: 51 records with
IDs starting `P4`, verdicts `{MATCH:48, OFFLINE_UNVERIFIABLE:2, SUPERSEDED:1}`, and the P4 ID set is
**identical** to the r28 final receipt's P4 ID set.

### 2.6 Sources / knowledge census — r28 rows intact

Census `sources`: `rows=73, malformed=0, mined=57, queued=12, rejected=4, tiers A=67/B=4/C=2`;
`knowledge`: `files=36, index_rows=36, dangling=[], duplicate_rows=[], unindexed=[]`.

r28's own census receipt (`actual-census-corrected.txt`, measured at 78e6df8) recorded
`rows=69, mined=57, queued=8, rejected=4, A=63/B=4/C=2, knowledge 36/36`. The delta is exactly
round 29's four new queued rows: `git diff ed26bdf..HEAD -- corpus/SOURCES.md` shows 4 added lines
and **no modification of any pre-existing row**; mined 57→57, rejected 4→4, malformed 0→0 and
knowledge 36→36 are unchanged. The r29 rows S070–S073 are `queued`, so the frozen13-row C2
population is untouched (`mismatch_sources=0`, `source_rows_checked=13`).

### 2.7 The whole r28 acceptance suite re-runs green on the integrated tree

A8 (`plans/fixtures/r28/acceptance.py`) → exit 0, `checks: 11, failed: 0`, with
`c1_metrics_equal_alternate: true` (r28's independent oracle `plans/fixtures/r28/benchmark_oracle.py`
still agrees with the instrument), `c2_projection_equal_alternate: true` (r28's
`registry_oracle.py`), `two_way_revert_counters_equal: true`,
`historical_existing_keyed_verdict_projection_unchanged: true`,
`historical_summary: {assertions:329, match:318, mismatch:0, superseded:6, offline_unverifiable:5,
out_of_population:31}` and the same three `instrument_sha256` bindings as r28. The baseline-export
red/green staging (S038/S050) reproduced inside a temp dir, so `SCORECARD.md:916–917`
("Identical checker on baseline export has2 mismatched rows, final0") still holds.

## 3. Mismatches found (exact location and value)

No r28 *numeric claim* was falsified. The mismatches are (a) two stale receipt pointers that
r28's SCORECARD still cites, and (b) two round-29 packaging gaps that leave the r28 preservation
unbound to the round-29 revision.

### M1 (moderate) — SCORECARD.md:898 cites the pre-correction C1 receipts

`SCORECARD.md:898` = `Evidence: corpus/evidence/round28-calibration/{audit-summary.txt,registry-summary.txt,build-acceptance/}.`

- `corpus/evidence/round28-calibration/audit-summary.txt` is the **pre-correction** summary: 5 LIMIT
  lines, and it has **no** `URL_RULES {"GOLD in PRED": 205}` line and **no**
  `URL_NOTE_ORIGIN {"defaulted": 9, "explicit": 196}` line, both of which the current instrument
  emits (A1). The byte-matching receipt is `audit-summary-final.txt`, which `SCORECARD.md` never
  names (`grep -n "audit-summary" SCORECARD.md` → line 898 only).
- `corpus/evidence/round28-calibration/build-acceptance/audit-selftest.stdout` records
  `SELFTEST clean cases=21` and `…/build-acceptance/registry-selftest.stdout` records
  `SELFTEST clean cases=12`, while `SCORECARD.md:915` claims "fixed selftests67/15 exit0". The
  67/15 receipts are `complete-acceptance/` and `final-acceptance/` (byte-identical to A2/A4).
- `…/build-acceptance/audit-current.stdout` (1 787 838 B, sha256 `bca99dfb199f0acf…`) differs from
  the current `--json` (1 900 693 B, sha256 `ad53df24c06e58d9…`): parsed at the JSON level, the
  build-stage capture has `limitations` length 5 vs 6, `metrics` missing the added
  `url_note_origin` key, and a different per-task `tasks` array; the other nine top-level keys
  (`contract_anchors` 34, `duplicate_task_ids`, `findings`, `missing_task_ids`, `scorer_contract`,
  `selected_task_ids` 16, `source_sha256`, `unexpected_task_ids`, `upstream_revision`) are equal.
- `registry-summary.txt` **is** byte-equal to `registry-summary-final.txt` (both 13/35/12/0), so the
  C2 half of the same pointer is sound.

Impact: a reader following `SCORECARD.md:898` sees 21/12 selftest cases and a summary missing the
URL-rule lines, and cannot reconcile them with `:915`. No claimed value is false; the final
receipts exist and reproduce byte-for-byte.

### M2 (moderate) — the round-29 evidence package contains no r28-preservation receipt

`corpus/evidence/round29-calibration/` contains exactly six files: `build-json-sha256.txt`,
`build-selftest.txt`, `build-summary.txt`, `instrument-before.txt`, `mutation-witness.txt`,
`sources-before.txt`. There is **no** audit summary, no registry summary, no historical-state
JSON/stdout, no census capture and no acceptance JSON — i.e. nothing binding the preserved
329/318/0/6/5, P4 51 (48/1/2), 13/35/12/0, 67/15 and 812/5/27/16/651 to the round-29 revision.
Round 28 shipped exactly these (`audit-summary.txt`, `registry-summary.txt`, `actual-census*.txt`,
`historical-scope-restored.txt`, `complete-acceptance/`, `final-acceptance/`). The preservation
demonstrated in §2 is currently attested only by this report, not by a landed receipt.

### M3 (moderate) — the census label is not byte-bound to a revision, and its numbers moved during this wave

`plans/round28_census.py --revision …` prints
`"revision_authority": "caller-supplied; see export/byte-equality receipt"`, but the round-29
calibration directory contains **no export/byte-equality receipt** (M2); the only digest file,
`build-json-sha256.txt`, binds the instrument's `--json` stream, not the census. The census
measures the **working tree**, so its population numbers move while the wave is running:

- 16:45Z census run → `out_of_population: 30`, `total_json_records: 359`;
- 16:48Z `state_check.py --json` → `out_of_population: 31`, 360 records;
- 16:49Z and 16:52Z census runs → `out_of_population: 31`, `total_json_records: 360`.

The single trigger is the untracked file `corpus/lessons/round-29.md`, created
2026-10-21T16:47:54Z (mtime=ctime) by the coordinator seat during the falsify wave; it is now
disclosed as `P2e.out-of-population.file.lessons/round-29.md`. Round 28 avoided this by capturing
`actual-final-byte-proof.json` (with `measured_commit`, per-file sha256 and `actual_census_exit`).

### M4 (minor) — r28's own receipt set carries two different OOP counts, and the SCORECARD quotes only one

Current OOP count is 31. r28's receipts disagree with each other because they were captured at
different moments: `build-preservation-corrected.json` → `out_of_population: 28`;
`final-acceptance/historical-state-current.stdout` → 28 (pre-admission, before
`corpus/knowledge/webarena-task-spec-audit.md` existed);
`complete-acceptance/historical-state-current.stdout` → 29;
`historical-scope-restored.txt` → 29; `actual-census-corrected.txt` → 29;
`SCORECARD.md:942` → "29 OOP disclosures (26 old+3 round28)". The 28-valued receipts are the
pre-admission measurement, the 29-valued ones the post-admission measurement. The current tree is
26 old + 3 round-28 + **2 round-29** = 31, so the string "29" at `SCORECARD.md:942` is true only for
the revision-scoped statement at :940 and must not be quoted as the current-tree value. No
pre-existing ID was reclassified, so this is a citation-hygiene issue, not a preservation break.

## 4. Cross-checks that came out clean (observed)

- `plans/config_projection.py` source sha256 `5673405e79a0445c…` equals
  `corpus/evidence/round29-calibration/mutation-witness.txt` ("control sha256 5673405e…") and
  `.ufo/waves/round-29/candidate-freeze-v1.json` → `instrument`.
- `python3 plans/config_projection.py --json` streamed digest = `c8da0c5a2d3110efbcd1880839c0036f11f22e32eb2c25f72105e8f355b34630`,
  identical to `corpus/evidence/round29-calibration/build-json-sha256.txt` and to
  `candidate-freeze-v1.json` → `json_output_sha256` (the r29 build receipt is fresh, not stale).
- `python3 plans/config_projection.py --summary` reproduces `corpus/evidence/round29-calibration/build-summary.txt`
  line-for-line (47 of 47 content lines; the receipt adds one trailing `exit=0` line).
- Round-29 candidate not yet admitted: `corpus/knowledge/` still has 36 files and 36 index rows;
  the candidate sits at `.ufo/waves/round-29/drafts/webarena-config-projection.md`
  (sha256 `7006b93dcacff387…`, as frozen in `candidate-freeze-v1.json`).

## 5. Residual risk and verification gaps

- **Not re-executed at its own revision.** I could not re-run the r28 census at revision
  78e6df8 (no checkout/worktree is permitted for this leaf), so `SCORECARD.md:940–942` is verified
  through its captured receipts (`actual-census-corrected.txt`) and through the current-tree
  equivalence, not by re-execution at that commit. Same for the df33fc83 red state: it is preserved
  only as captured evidence.
- **Independent-oracle scope.** r28's oracles (`plans/fixtures/r28/benchmark_oracle.py`,
  `registry_oracle.py`) are r28's own; I ran them only through r28's acceptance harness, so oracle
  independence from r28's *author* is a property I did not re-litigate.
- **Concurrent mutation during measurement.** The tree changed under me twice (M3). Any r29
  measurement that cites a population count must either bind the tree by digest or be re-measured
  after the wave's writes settle; the numbers I report (31 OOP / 360 records) are those of
  2026-10-21T16:52:19Z on the tree as it stood then, and `corpus/lessons/round-29.md` is the only
  untracked corpus file at that moment.
- **Not my scope.** I did not audit the config-projection instrument's own claim (r29 C1 semantics,
  the 2436 projections, the prereg text, the knowledge candidate text). My finding M2/M3 concern only
  the *preservation* evidence bound to the r29 revision.
- **Quotes.** Every quoted string above is a command output line, a receipt field or a SCORECARD
  line; each is far below the 25-word limit except where the receipt itself is a single long line
  (e.g. the `EVAL_TYPE_SETS`/`SOURCES.md` rows, which are tool output, not prose quotation).

## 6. Scoped verdict

The round-28 capability and calibration claims are **not falsified**: every r28 numeric value in
`SCORECARD.md:888–947` reproduces on the integrated round-29 tree (812/5/27/16/651; 13/35/12/0;
67/15; 329/318/0/6/5; P4 51 = 48 MATCH/1 SUPERSEDED/2 offline; 26 original OOP IDs retained),
the r28 instrument bytes are unchanged (3/3 sha256 match), the r28 `--json`/`--selftest`/summary
outputs are byte-identical to the r28 final receipts, and the r28 11-stage acceptance harness
re-runs green (exit 0, 11/11) with both r28 independent oracles still agreeing. The only
historical-state deltas are two additive OUT_OF_POPULATION disclosures created by round 29 itself,
with 0 ID removals and 0 verdict changes. The attack does, however, expose three concrete
defects: a stale evidence pointer at `SCORECARD.md:898` that names the pre-correction C1 receipts
(M1), a round-29 evidence package that carries no preservation/byte-equality receipt of its own
(M2), and a census whose label is not byte-bound while its population counts moved twice during
this wave (M3), plus a minor OOP-count citation inconsistency inside r28's own receipt set (M4).
Preservation holds; the round-29 package is not yet self-attesting.

VERDICT: PARTIAL
