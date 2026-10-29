# W2CritRoundHonesty — kengaku round 52, wave 2 (falsify), critic, axis: calibration

Seat: `W2CritRoundHonesty` (critic, leaf). Read-only attack on the round's honesty: frozen claims, Amendments A1–A5, the A1 observation receipt, the wave-1 seat reports, the two frozen counters, the lane's SCORECARD/LOG/SKILL registry, and the 28 new registry rows. Attacked state: lane `master` at `87301ba` plus the uncommitted round-52 working files; measured 2026-10-28. **Wave-2 seats were still writing** (`confirmations.json`, `prior-art.md`, `labels.json` and the control receipts were absent at my run). Every verdict below is on that state and must be re-checked at the landing tip.

## Bottom line

1. **R52-C1 is not admitted at the attacked state.** The literal predicate fails (`CONFIRMED new=0`, `PRIOR-ART urls=0`, `CAPTURES present=183`, `classified=88`). Novelty stays 8 by the frozen kill rule. Neither a prior-art verdict nor the instrument's existence can move novelty at this state.
2. **The frozen score rule cannot be satisfied by the instrument's existence.** It needs at least one confirmed finding priced phenomenon-new, per finding. Even then "phenomenon-new" is not established at population level: a fetched secondary reports a 28-of-89 population audit of TB2 by Buchanan, Linderman and Ré (OpenReview `AhXMZPnOPS`, DL4C @ ICML 2026). The primary was not readable to the scout or to me.
3. **The A1 amendment does not survive its own example.** The committed per-test classifier does not class two of the three tests A1 cites as presence-only (`pytorch-model-recovery::test_model_file_exists` → P3; `torch-tensor-parallelism::test_parallel_linear_exists` → P2). Two of the 29 candidates (`pytorch-model-recovery`, `torch-tensor-parallelism`) enter the queue only through the file-level V1 rule that A1 declares false for them. The P1 count is classifier-dependent (33 committed; 46 after stripping comments and docstrings).
4. **R52-C2's structural predicate passes (`PREDICATE R52-C2 pass`, exit 0), but "truthful row" is not measured.** The counter checks cell presence, entry-file existence and a substring flag match. W1 `C2CritPadding` showed it passes 28 padding rows, a duplicated row and an inverted verdict map. I reproduced two further escapes (a negation exemption and a comment-substring match). The registry also has a duplicated `gate-flip-check` row that the counter cannot see.
5. **Several statements in the frozen claims or receipts are false as recorded:** wave shape (`64 seats`; dispatched 35 + 33 = 68), A1 receipt figures (`9249 B` for `pytorch-model-recovery`, actual 5591 B; `308` test functions, measured 305), "the L1 confirmed by hand" (self-confirmation), "not tuned to enlarge the pool" (pool 2 → 29 under the amendment), and the `c1-after` / `c2-after` receipts, which are pre-landing snapshots. The eight `c1-control-*` / `c2-control-*` receipts the claims require do not exist.
6. **Admissible positives:** the A5 digest pin for the excluded capture is genuine (I fetched the upstream bytes read-only at the pin: sha256 `57e49041…b59e`, 2687 B); the D2 LOG erratum is present; the census validates (exit 0); C1 and C2 are causally separable as claimed.

## Commands run (read-only against the lane; outputs in receipts)

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=/fast/scratch/hyaku/kengaku-r52/w2-W2CritRoundHonesty
python3 plans/round52_c1_grader_audit.py --lane .        # exit 1
python3 plans/round52_c2_registry.py --lane .            # exit 0
# upstream digest of the excluded capture (read-only fetch into scratch, not the lane)
curl -fsS -m 60 -o upstream-sanitize-test_outputs.py \
  "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sanitize-git-repo/tests/test_outputs.py"
sha256sum upstream-sanitize-test_outputs.py              # 57e49041…b59e, 2687 B
# secondary prior-art summary and the OpenReview forum page (read-only)
curl -fsS -m 60 -o lacuna.html "https://lacuna.tiptreesystems.com/work/benchmarks-as-software-a-case-study-on-terminal"
curl -fsS -m 30 -o ob.html "https://openreview.net/forum?id=AhXMZPnOPS"   # HTTP 200; title not in HTML (client-rendered)
# census, read-only (writes only stdout)
cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku   # exit 0
# importlib load of the frozen counters (no bytecode written) for classify_test / split_tests / prior_art / selftest_unbacked
# fixture probes in scratch: prior_art() on one URL in three spellings; selftest_unbacked() on three cells
# SKILL.md duplicate-row check (cell split by pipe, and by the counter's parser)
# result counts: w1-spec.json 35 items; w2-spec.json 33 items; round-52 w1-results.json 35 entries; round-51 w1-results.json 64 entries
```

## Measured state at attack time

**`plans/round52_c1_grader_audit.py --lane .` → exit 1**

```
TASKS total=89 records=89 classified=88
CAPTURES expected=184 present=183 mismatched=0
CLASS V1=2 V4=0 V2=53 V3=31 V0=3
TESTCLASS presence_only_tests=33 tasks_with_presence_only=27
CANDIDATES total=29
CONFIRMED new=0 []
PRIOR-ART ok=False urls=0
LABELS agree=0 of 0
PREDICATE R52-C1 fail
A5 EXCLUDED listed=1 digest_pinned=1 tasks=['sanitize-git-repo']
A5 CAPTURES present+pinned_excluded=184 of 184
A5 TASKS classified+excluded=89 of 89
PREDICATE R52-C1-A5 fail
```

**`plans/round52_c2_registry.py --lane .` → exit 0**

```
ADVERTISED total=72
REGISTERED total=72 rows=74        (rows=74 includes the header row; 73 eight-cell data rows parsed)
MISSING 0
INCOMPLETE 0
ENTRY-MISSING 0
SELFTEST-UNBACKED 0
PREDICATE R52-C2 pass
```

Other state: no `corpus/evidence/round52/confirmations.json`, `prior-art.md` or `labels.json` in the lane; no `corpus/lessons/round-52.md`; no round-52 SCORECARD row (`grep -c` for round-52 in SCORECARD → 0); LOG.md has only the round-51 erratum (`LOG.md:1598–1606`, D2, present).

## Attacks, with result

Result key: **LANDED** = the attack produced a measured defect or unsupported statement against the state; **NOT LANDED** = the attack was tried and the artefact holds.

**A-1 — A5 exclusion digest (NOT LANDED).** Upstream bytes for `sanitize-git-repo/tests/test_outputs.py` at the pin hash to `57e4904177acac5807b51f7c32444bde1968ba0445855fa4333d9eb73865b59e`, 2687 B, matching `EXCLUDED.md` and `SHA256SUMS:158`. The "digest-pinned" bit of A5 is genuine, so A5 does not launder a miss in that respect. Its risk is reporting: `PREDICATE R52-C1-A5` is an additive line that also prints `fail` at this state, and it must never be cited as the C1 verdict. The literal verdict is fail.

**A-2 — A1's cited examples are not reproduced by the committed per-test classifier (LANDED).** Measured with `classify_test` / `split_tests` imported from the frozen counter:

| test (A1 receipt cites it as presence-only) | committed class | why |
|---|---|---|
| `bn-fit-modify::test_bn_sample_exists` | P1 | reproduces |
| `pytorch-model-recovery::test_model_file_exists` | **P3** | `VALUE` matches `\bin\b` in the comment `# Reference the directory the agent operated in (…)` |
| `torch-tensor-parallelism::test_parallel_linear_exists` | **P2** | the block runs until the next `def test_`, so it folds in helpers `_setup_process_group` / `_cleanup_process_group`, which contain `dist.` (`BEHAV_T`) |

So one of three cited examples reproduces. The disclosure's central per-test claim is therefore not what the committed instrument computes.

**A-3 — the candidate predicate is not A1's predicate (LANDED).** A1 says "a task is a vacuity candidate when ≥1 of its tests is P1". The counter computes `candidate = bool(p1) or cls in ("V1","V4")`. Output: `CANDIDATE pytorch-model-recovery class=V1 presence_only=-` and `CANDIDATE torch-tensor-parallelism class=V1 presence_only=-`. Both are candidates with zero P1 tests. Their candidacy comes from the file-level V1 rule that A1 says "is FALSE of those graders as a whole". This is an unannounced change of the candidate definition, and it leaves a disavowed rule in the queue.

**A-4 — the P1 count is classifier-dependent (LANDED).** [INFERENCE on method; measured on output] My probe removed `#` comments and docstrings from the same 305 test blocks and re-ran the committed `classify_test`. P1 rises from **33 to 46**; 13 tests flip P3 → P1, including `pytorch-model-recovery::test_model_file_exists`, `sparql-university` ×2, `video-processing` ×2, `financial-document-processor::test_summary_csv_exists` and `gcode-to-text::test_hello_file_exists`. The 33 is a property of the committed text-processing rules, not of the population. It must be reported with that sensitivity, or not as a population fact.

**A-5 — A1 receipt figures are wrong or unreproduced (LANDED).** `.ufo/waves/round-52/claims/a1-observation.txt`:
- `pytorch-model-recovery/tests/test_outputs.py … 9249 B`: actual **5591 B** (`wc -c`). 9249 B is `adaptive-rejection-sampler`'s file size. No erratum is appended to the receipt.
- `308 test functions`: measured **305** (`def test_` at any indent and the top-level split agree on 305 over the 88 primary graders present).
- `54 presence-only / 42 tasks`: retracted by A4 (measured 33/27). A4 is correctly appended, but the receipt carries no erratum line. The claims text says the figure "must not be used in the report". The W1 critic `C1CritRoundShape` F-D already named the 9249 B error, and it is still uncorrected.

**A-6 — "The L1 confirmed by hand" is self-confirmation (LANDED).** The A1 receipt says the L1 "confirmed by hand, in two never-read tasks" (`pytorch-model-recovery`, `torch-tensor-parallelism`) and read `bn-fit-modify`. Those are the author's own reads, made during this round after freezing and before the scored after-run. They are not an "independent second reader". `bn-fit-modify` is also the first candidate the counter prints (alphabetical), so the first confirmation slot is the author's own pick.

**A-7 — the CONFIRMED leg is forgeable by the author (LANDED; measured by W1, not re-run by me).** `C1CritTrustBoundary` built four fixtures on real pin bytes. A self-dealt reader (`reader` = the author's id on both rows), forged captures under a self-referential `SHA256SUMS`, a vacuous located quote (the canary comment line), and truthy-string fields (`confirmed: "false"`, `reader: " "`) each produced `PREDICATE R52-C1 pass`, exit 0. The counter checks only `not c.get("reader")` and substring membership. `CONFIRMED ≥ 2` is therefore not evidence of independent confirmation until reader receipts are checked against the named reader seat's own committed bytes.

**A-8 — the PRIOR-ART leg is a text count (LANDED; measured by me).** `prior_art()` counts distinct URL strings. A file with `https://example.org/paper`, `https://example.org/paper.` and `<https://example.org/paper>` returns `(True, 3)`. The leg is satisfied by one URL. Its only protection is the scout's receipts, which are not in the lane.

**A-9 — "phenomenon-new" is not established at population level (LANDED).** The scout (`C1ScoutPriorArt`) fetched 22 URLs (20 × 200) and quoted 10 substrings. Its verdict is "phenomenon-new **relative to this fetch**". It records that the OpenReview primary (`AhXMZPnOPS`, "Benchmarks as Software") returned a challenge page, and that "Lacuna … summarizes the OpenReview paper … including a 28-of-89 defect rate. Those figures stay out of the findings." I fetched the secondary summary (`lacuna.tiptreesystems.com`, HTTP 200). It states: "Benchmarks as Software: A Case Study on Terminal-Bench", E. Kelly Buchanan, Scott Linderman, Christopher Ré, DL4C @ ICML 2026; "audits Terminal-Bench 2.0, finds defects in 31% of its tasks"; "Defect Rate: 28 out of 89 tasks (31%) had task-side defects". The primary is unread, and the secondary is unverified against it. That is a published population audit of the same 89-task benchmark. The scout's fetched set also includes arXiv `2605.26079` (a trajectory audit recovering "14 of these 21 issues" against TB2 PR #53) and PR #53 itself ("Tests were updated when they over-specified or let any solution pass"). Per-finding "phenomenon-new" can be claimed only as "not documented in the fetched primaries; Buchanan et al. not read". Unqualified "novel" is not supportable.

**A-10 — the prior-art verdict is per-finding in the frozen rule, not per-instrument (LANDED as a constraint).** The scout's verdict is instrument-level (`A whole-benchmark grader-vacuity triage … is phenomenon-new relative to this fetch`). The frozen score rule and `C1RevPriorArtProtocol` require a per-confirmed-finding verdict. The eight tasks the scout priced phenomenon-known are priced for different defects, and no confirmed finding exists yet. So today there is **no** per-finding phenomenon-new verdict.

**A-11 — SOURCES rows do not cover the prior-art primaries (LANDED).** `grep` of `corpus/SOURCES.md` for the scout's primaries finds rows for only two of them: `S020` (arXiv `2601.11868`) and `S090` (tbench announcement 2.0). Nine fetched primaries have no row: arXiv `2605.26079`; PR #53 (`pull/53`); the tbench 2.1 news page; the Z.ai HF dataset card; `june.kim`; testsmells.org (catalogue and FSE 2020 PDF); the snorkel leaderboard; `issues/1387`; arXiv `2503.15223`. The frozen frontier step (`claims §Frontier step` 1 and 3) says C1 "rests on SOURCES rows opened this round (the TB2 pin and the prior-art primaries)". The S105–S112 and S157 rows cover the TB2 pin. S179 (the population tree) is still "ADMIT, to insert", not inserted. Census (`receipts/census-validate.txt`): exit 0, final line `ok`, with **15 `W04` duplicate-URL warnings**. Exit 0 is structural only.

**A-12 — the labels are not blind and not a reliability measure (LANDED).** `C1ExecBlindLabels` read the counter's regex source ("I did read the counter *source* (regex definitions only) to disambiguate marker vocabulary") and labelled 30 tasks at file level (`V1..V0`) with the same vocabulary. "Agreement 30/30" is regex-versus-regex on file-level classes, which A1 says misdescribe two of the tasks. The file also has 30 rows, not the 24 the seat item asked for (`labels-prefix24.json` is a truncation). The counter's `LABELS agree/total` reads `corpus/evidence/round52/labels.json`, which is not in the lane yet.

**A-13 — "never read by this lane before this round" is checked against knowledge filenames only (LANDED for the disclosure).** `lane_read_tasks()` returns the 12 `corpus/knowledge/tb2-*-grader.md` ids. It does not see execution history. The lane's SCORECARD records a 26-case pilot on `openssl-selfsigned-cert` with a measured oracle outcome ("nop 0/6, oracle 5/6 on host OpenSSL 3.6.5"; `SCORECARD.md:1604`, and `:1716`, `:1801`). That is an earlier execution of this task's grader. `openssl-selfsigned-cert` is a candidate (V2, `test_directory_structure`). If it is chosen as a confirmation, the report must say the lane executed it earlier. The counter cannot.

**A-14 — the control receipts the claims require are absent (LANDED).** `ls .ufo/waves/round-52/claims/` shows `a1-observation.txt`, `c1-before/after/after-a2-pre/selftest.txt`, `c2-before/after/a3-pre/after-w1rows-pre-scorecard/selftest.txt` and `c2_before_probe.py`. There is no `c1-control-{nothing,name-only,blind-class,drop-capture}.txt` and no `c2-control-{nothing,empty-cells,drop-row,false-selftest}.txt`. Measured defects in the frozen controls, from W1 and my own reading:
- `c1-control-drop-capture` documents `present=183 mismatched=1`. The counter gives `present=183 mismatched=0` for a removed file (W1 `C1CritRoundShape` F-B). The control fails on `present`, so it does not isolate the mismatch leg. `C1MutCounters` shows the mismatch-leg mutant survives that control and is killed only by an isolated digest-only fixture.
- `c1-control-blind-class` ("force every task to V0") does not zero the candidate count under A1: `CANDIDATES total=29` survives (W1 F-C; the per-test flags are not cleared).
- The `C2 MISSING only under plans/` mutant survives all exercised controls (`C1MutCounters`).

**A-15 — the "after" receipts are pre-landing snapshots (LANDED).** `c1-after.txt` shows `CAPTURES present=89` (the state before the capture landing). `c2-after-w1rows-pre-scorecard.txt` predates the SCORECARD. Neither can be cited as the scored after-run. The claims require a regeneration at the landing tip, in a clean clone, after SCORECARD/LOG are written. Adding `python3 plans/round52_c1_grader_audit.py` or `round52_c2_registry.py` to SCORECARD/LOG makes both advertised, so C2 goes red unless rows exist (W1 F-A). The after-run must come after those edits.

**A-16 — the wave shape claim is false as built (LANDED).** Frozen `claims §Wave shape`: "total **64 seats**: wave 1 build (32) and wave 2 falsify (32)". Dispatched: `w1-spec.json` has **35** items, and `w1-results.json` has 35 entries; `w2-spec.json` has **33** items. Total 68. Attack roles (reviewer, critic and mutation-tester, by the claims' own list): wave 1 = 5 + 3 + 1 = **9 / 35 = 25.7%** (meets the ≥25% floor by 0.7 points); wave 2 = 7 + 3 + 2 = **12 / 33 = 36.4%**. The round report must disclose the deviation from the frozen shape. The claims text is not amended.

**A-17 — the C2 structural predicate can be satisfied by padding (LANDED; reproduced by W1, mechanism confirmed by my code reading).** `parse_rows()` accepts any 8-cell line; no cell's meaning is checked. `C2CritPadding` inserted 28 rows whose seven non-entry cells are `x`: `PREDICATE R52-C2 pass`. Changing `order-check`'s self-test cell to `x` also passes. A 29-row variant (a duplicate row, an inverted verdict map for `round28-census`, and a two-script self-test cell) still reports only the known `order-check` item. The landed rows are not padded by length: no new row has a cell under 12 characters, and the three sub-12-character cells are kind or owner labels (`gate`, `probe`, `kengaku`). That is an observation about the current table, not about what the counter verifies.

**A-18 — the self-test check is substring-based and has a negation exemption (LANDED; measured by me).**
- Negation: `selftest_unbacked` on the cell `` `python3 plans/tool_a.py --selftest` (fixtures; no `--summary` flag) `` is **not flagged**. The same claim without the negation phrase is `UNBACKED`. A cell can claim a flag the script lacks and be exempt because it also negates a different flag. This is the A3 parser change. A3 is disclosed as a parser correction, but it changes the predicate's verdict on unchanged bytes (`order-check`: baseline `SELFTEST-UNBACKED 1` → `0`), and it widens acceptance.
- Substring: the check is `f not in body`. A flag that appears only in a comment (`# TODO: add --selftest later`) backs a claim. The check does not look at argparse.
- Coverage: 17 rows have self-test cells the counter cannot evaluate at all (no `plans/` script path in the cell, or a negation). For the ones I checked, the flag string is present in the entry script. That is existence in source, not an execution of the self-test.

**A-19 — the advertised universe and the registry have holes (LANDED; measured).**
- The frozen regex excludes hyphenated evidence directories (`[A-Za-z0-9_]+`) in both the advertised and the registry extraction. Four scripts named `python3 corpus/evidence/<hyphen-dir>/…py` in SCORECARD/SKILL/LOG/README/knowledge are outside `ADVERTISED`: `round9-fleet/test_harness.py`, `round11-power/recompute_r11.py`, `round12-ladder/recompute_r12.py`, `round13-coverage/coverage_census.py`. Of these, the SKILL registry names only `coverage-census`, and its entry path is hyphenated, so it is outside both sets. The other three have no SKILL row at all (checked by grep). `ADVERTISED 72` therefore counts a universe that excludes four advertised scripts.
- Nine depth-1 `plans/*.py` scripts are not named in any self-assessment file (e.g., `plans/fixture_fence.py`, `plans/policy_cases.py`, `plans/round32_defects.py`). They are outside the universe by design, but the report must not say "every script the lane owns is registered".
- A widened regex gives `ADVERTISED 79` (`C1MutCounters`). The "72 advertised instruments" is a regex-defined count.

**A-20 — the registry has a duplicated row that the counter cannot see (LANDED; measured).** `SKILL.md:609` and `SKILL.md:614` are both `gate-flip-check` rows. Line 609 contains `fired\|not fired`. The `\|` is a GFM-escaped pipe, but the counter's `split('|')` does not honour it, so the row splits into **9** cells and `parse_rows()` skips it. Line 614 is the 8-cell row the counter parses. W1 `C2ExecRowRuns` said the row "should be repaired in place, not duplicated"; the landed table has both. The counter reports `MISSING 0` and `PREDICATE pass` with the duplicate present. `C2CritPadding`'s duplicate-row variant also passed.

**A-21 — row truthfulness is not verified by any receipt (LANDED as "unverified"; not as "false").** `C2ExecRowRuns` ran 28 instruments in clones and recorded exits and final lines. Four were red at base or tip (`round35_c1_verify` exit 1, `round36_c2_verify` exit 1, `round45_c2_verify` exit 1, `round46_c3_verify` exit 1), plus `round28_census` exit 1 and `adoption_check` exit 1 in the clone layout. The rows' verdict-map arms describe these outcomes, so the rows are not false on those points. But no receipt maps each row's arm (`0`/`1`/`2`) to an observed exit or output, and no row's pinned values are re-derived against the tip. The counter checks neither. The claim "every advertised verdict instrument has a truthful row" is not supported.

**A-22 — candidate selection by alphabetical order (NOT LANDED; disclose).** `candidates` are sorted alphabetically, and the W2 confirmer seats were told to take the first five printed candidates. That fixes the confirmation set by alphabet, not by weakness. Disclose the selection rule. This is not a fabrication.

**A-23 — causal separability (NOT LANDED; admissible).** `round52_c1_grader_audit.py` reads `plans/round52-tasks.json`, `corpus/evidence/round52/**` and `corpus/knowledge/tb2-*-grader.md`. `round52_c2_registry.py` reads the self-assessment files (SCORECARD, SKILL, LOG, corpus/README, knowledge). Neither reads the other's artefacts. The claim holds as written.

## Per-claim verdicts

Verdict key: **ADMISSIBLE** = may be written as stated (with the qualifier shown); **NOT ADMISSIBLE** = must not be written as stated.

| # | Claim (where it is made) | Verdict | Reason (measured unless marked) |
|---|---|---|---|
| 1 | R52-C1 landed; novelty 8 → 9 (claims §Claim 1) | **NOT ADMISSIBLE** | `PREDICATE R52-C1 fail`; CONFIRMED 0; PRIOR-ART 0 urls; kill rule → novelty 8 |
| 2 | Novelty bump justified by the prior-art verdict | **NOT ADMISSIBLE** (no per-finding verdict exists) | A-10. The only verdict is instrument-level and "relative to this fetch" |
| 3 | Novelty bump justified by the instrument's existence | **NOT ADMISSIBLE** | Frozen score rule requires a phenomenon-new confirmed finding; claims and `C1RevPriorArtProtocol` say instrument-new alone does not satisfy it |
| 4 | "Whole-benchmark grader-vacuity triage for TB2 is new / first / no prior art" | **NOT ADMISSIBLE** | A-9: Buchanan et al. population audit (secondary: 28/89), arXiv 2605.26079 audit of TB2 issues, PR #53 |
| 5 | "The lane's first population-level static instrument over the TB2 graders; no fetched primary documents this marker triage" | **ADMISSIBLE** with "relative to the ten fetched pages; OpenReview primary not read" | Scout's own scope; the counter output is real |
| 6 | Counter numbers: 89/89 records; 184 frozen captures, 183 present (1 excluded); 88/89 classified | **ADMISSIBLE** | Measured; the exclusion is stated (A-1, A5) |
| 7 | "33 presence-only tests across 27 tasks" as a population fact | **NOT ADMISSIBLE** as a fact; **ADMISSIBLE** as "committed classifier output" | A-4: 33 → 46 with comments and docstrings stripped |
| 8 | "29 vacuity candidates" | **ADMISSIBLE** only as "triage queue under the union rule (≥1 P1 or file-level V1/V4)" | A-3: two candidates have zero P1 tests |
| 9 | A1 per-test amendment is "the mechanical split", "not tuned to enlarge the pool" | **NOT ADMISSIBLE** unqualified | Pool 2 (file-level V1/V4 under the frozen rule) → 29; A1 was written after the L1 saw the marker statistics. A1 does disclose "far larger"; "not tuned" is unverifiable intent |
| 10 | A1's cited examples are presence-only (P1) | **NOT ADMISSIBLE** | A-2: 1 of 3 reproduces |
| 11 | pytorch-model-recovery and torch-tensor-parallelism are vacuity findings | **NOT ADMISSIBLE** | A1 says V1 is false for them; per-test they are P3 / P2 on the committed instrument; their queue entry is the disavowed file-level rule |
| 12 | "L1 confirmed by hand" bn-fit-modify, pytorch-model-recovery, torch-tensor-parallelism | **NOT ADMISSIBLE** as confirmation | A-6: the author's own reads, not an independent second reader |
| 13 | A1 receipt: 54 P1 / 42 tasks | **NOT ADMISSIBLE** | Retracted by A4; measured 33/27 |
| 14 | A1 receipt: pytorch-model-recovery 9249 B; 308 test functions | **NOT ADMISSIBLE** | A-5: 5591 B; 305 measured |
| 15 | CONFIRMED ≥ 2 (future) | **NOT ADMISSIBLE** until reader receipts are verified | A-7; the counter accepts self-dealt and forged rows |
| 16 | PRIOR-ART `ok` (≥3 fetched URLs) | **NOT ADMISSIBLE** as a pricing claim | A-8: textual count; one URL in three spellings passes |
| 17 | Scout's per-URL fetch table (22 requests, 20 × 200, 10 quoted substrings) | **ADMISSIBLE** as scout evidence (its own receipts) | Scout receipts; I did not re-verify the quotes |
| 18 | "C1 rests on SOURCES rows opened this round (the TB2 pin and the prior-art primaries)" | **NOT ADMISSIBLE** as stated | A-11: nine scout primaries have no row; S179 not inserted. The TB2 pin rows (S105–S112, S157) are admissible |
| 19 | Census validates, exit 0 | **ADMISSIBLE** as "structurally valid at attack time" | `receipts/census-validate.txt`; the 15 `W04` warnings must be reported; the frozen end-of-round census has not run |
| 20 | Labels agree 30/30, "blind" | **NOT ADMISSIBLE** as "blind agreement" | A-12. Admissible only as "file-level hand reading vs the same regex vocabulary, 30/30; not blind; not a leg" |
| 21 | Candidates were "never read by this lane before this round" | **NOT ADMISSIBLE** unqualified | A-13: `openssl-selfsigned-cert` executed in an earlier pilot; this round's L1 read three tasks |
| 22 | Each C1 control fails the predicate; receipts under `claims/` | **NOT ADMISSIBLE** | A-14: receipts absent; documented signatures wrong; two controls do not isolate their leg |
| 23 | `claims/c1-after.txt`, `c2-after.txt` are the scored after-runs | **NOT ADMISSIBLE** | A-15: pre-landing snapshots |
| 24 | A5: additive `PREDICATE R52-C1-A5` | **ADMISSIBLE** only as a labelled additive line; **NOT ADMISSIBLE** as a C1 pass | A-1; prints fail now; the literal verdict governs |
| 25 | A5 exclusion digest is pinned and genuine | **ADMISSIBLE** | A-1: upstream sha256 `57e49041…` at the pin, 2687 B, matches `EXCLUDED.md` and `SHA256SUMS:158` |
| 26 | 183/184 and 88/89 reflect the operator's exclusion, not a lane defect | **ADMISSIBLE** as stated in `EXCLUDED.md` | The lane tree does not contain the bytes; the digest is genuine |
| 27 | R52-C2 structural predicate passes at the attacked tree | **ADMISSIBLE** as "frozen structural predicate passes" | `PREDICATE R52-C2 pass`, exit 0 |
| 28 | Operability 8 → 9 justified by the C2 pass | **ADMISSIBLE** only under the frozen structural rule, with the caveats of A-17–A-21 stated | Counter is gameable; rows unverified |
| 29 | "Every advertised verdict instrument has a truthful row" / "registry rows verified" | **NOT ADMISSIBLE** | A-17, A-18, A-19, A-20, A-21 |
| 30 | "All 72 advertised instruments are registered" | **NOT ADMISSIBLE** as written | Four hyphen-dir advertised scripts sit outside the frozen universe; `coverage-census` uncounted; duplicate `gate-flip-check` row |
| 31 | "The 28 new rows: 8 non-empty cells each" | **ADMISSIBLE** | `INCOMPLETE 0`; table rows 46 → 74 (+28, header-inclusive) |
| 32 | Self-tests "exist and are truthful" | **NOT ADMISSIBLE** as "truthful"; **ADMISSIBLE** as "flag string present in the entry script for the rows checked" | A-18 |
| 33 | `order-check` row truthful after A3 | **ADMISSIBLE** for that row (no `--selftest` in the script, confirmed) | A3 changed the parser; the report must show both the baseline (`1`) and the A3 (`0`) numbers and disclose the negation exemption |
| 34 | A3 is "without changing C2's frozen predicate" | **NOT ADMISSIBLE** as written | Same cell, different verdict; the parser exemption is a predicate change, disclosed as a correction |
| 35 | Wave shape "64 seats (32 + 32)" | **NOT ADMISSIBLE** | A-16: 35 + 33 = 68 |
| 36 | ≥25% attack seats per wave | **ADMISSIBLE** with counts | 9/35 = 25.7%; 12/33 = 36.4% |
| 37 | D2 LOG correction (round-51 "63 of 64" → 64) | **ADMISSIBLE** | `LOG.md:1598–1606`; `.ufo/waves/round-51/w1-results.json` has 64 entries (measured). The round-52 results file has 35 entries and is not the subject of D2 |
| 38 | Coverage 7 not claimed; stagnation nudge not invoked | **ADMISSIBLE** | Frozen text; the `AXES.md` rule per the W1 critic |
| 39 | C1 and C2 causally separable | **ADMISSIBLE** | A-23 |
| 40 | C1 "closes the population gap" / "closes the remaining TB2 task graders (12 of 89 read)" open clause | **NOT ADMISSIBLE** as "closes" | `corpus/README.md:433` also names runtime task validity and SWE-bench as still open; C1 runs no grader |
| 41 | `corpus/lessons/round-52.md` mistakes/gate, knowledge entry, SCORECARD rows, LOG round-52 entry | **NOT ADMISSIBLE** (not yet landed) | Absent in the lane at attack time |

## Sentences the round report must not write

1. "R52-C1 passes" / "`PREDICATE R52-C1 pass`" / "novelty 8 → 9" / "novelty raised by the triage".
2. "This is the first (or only) whole-benchmark grader triage of Terminal-Bench 2.0" or "no prior art" without "relative to the ten fetched pages; the Buchanan–Linderman–Ré audit (secondary: 28/89) was not read".
3. "phenomenon-new" for any finding not priced per finding against a fetched primary with a located quote.
4. "N findings confirmed by an independent second reader" unless each reader's receipt is in that seat's committed bytes and a non-author has checked it.
5. "bn-fit-modify / pytorch-model-recovery / torch-tensor-parallelism are confirmed vacuous" or "independently confirmed by the L1".
6. "The per-test classifier identifies 33 presence-only tests" as a population property (write "committed classifier output; 46 with comments and docstrings stripped").
7. "The A1 disclosure reproduces" or "the amendment's examples are presence-only" (one of three is).
8. "The amendment was not tuned to enlarge the pool" (write "the pool grew from 2 to 29 under A1, which was written after the L1 saw the marker statistics").
9. Any A1 figure: "54 presence-only tests", "42 tasks", "308 test functions", "9249 B".
10. "Blind label agreement", "30/30 blind agreement", or the label count as reliability.
11. "`openssl-selfsigned-cert` was never read by the lane" (it was executed in an earlier pilot).
12. "Every advertised verdict instrument has a truthful row", "the registry rows are verified", "the verdict maps are checked".
13. "`SELFTEST-UNBACKED 0` means the self-tests exist and work".
14. "All 72 advertised instruments are registered" or "every script the lane owns is registered".
15. "The registry has no duplicates."
16. "A3 left the C2 predicate unchanged."
17. "64 seats" or "wave 2 = 32 seats" for round 52.
18. "`c1-after` / `c2-after` are the scored after-run" or any count from those files as the after-run.
19. "`PREDICATE R52-C1-A5 pass`" or "C1 passes under A5".
20. "The control set fails as frozen" (no control receipts exist; two controls do not isolate their leg; one documented signature is wrong).
21. "The census is clean" without "15 W04 duplicate-URL warnings".
22. "C1 closes the TB2 grader population" or "closes README:433" (runtime validity and SWE-bench remain open).
23. "The lane has read 12 of 89 graders by hand" as a measured fact (it is the lane's own count of knowledge entries; I did not re-read the 12).

## Claims the round must report as unprovable or harmed

**Unprovable at this state (say so):**
- Population-level novelty (`phenomenon-new` across TB2): the Buchanan et al. primary is unread, and a secondary attributes a 28/89 population audit to it.
- Independent second readers: no receipts, and the counter cannot verify independence.
- Blind-labelling reliability: the labeller read the regex; labels are file-level.
- Registry truthfulness (verdict maps, pinned values, write scope): no receipt maps arms to observations, and the counter does not check.
- The per-test P1 count as a population property: classifier-dependent (33 vs 46).
- "Never read by the lane" for the candidate set: execution history is not checked (`openssl-selfsigned-cert`).

**Harmed (the evidence against the claim is in the round's own artefacts):**
- **A1 amendment:** its motivating example does not reproduce on the committed instrument, and its candidate union keeps the file-level rule it disavows. The amendment's central claim is harmed.
- **C1 candidate pool:** 2 of 29 candidates enter through a disavowed rule.
- **Novelty:** harmed by the Buchanan et al. population audit (secondary) and by TB2 PR #53 and arXiv `2605.26079`, which document weakness in TB2 graders at population or task level.
- **Operability / "truthful":** harmed by the padding, duplicate, inverted-map and negation escapes; by four advertised scripts outside the universe; and by the duplicated `gate-flip-check` row.
- **Wave-shape claim:** harmed (68 seats, not 64).
- **Control claim:** harmed (receipts absent; one documented signature wrong; the mismatch-leg control does not isolate its leg).
- **Receipt hygiene:** harmed by the A1 receipt's uncorrected 9249 B and 308 figures, and by pre-landing "after" snapshots that carry the after-run name.

## Smallest corrections for the L1 (ranked; none is my decision)

1. Make the candidate predicate equal A1's text (`≥1 P1` only), or append an amendment that states the union and its effect on `pytorch-model-recovery` and `torch-tensor-parallelism`.
2. Report the classifier sensitivity (33 committed; 46 stripped). Either fix the two defects (prose tokens in `VALUE`; helper folding in `split_tests`) under an append-only amendment, or report them as open.
3. Require each confirmation row to carry a receipt path inside the named reader seat's committed wave-report dir, with the quote located there, and have the counter check it. Exclude the L1's own reads from the confirmation set.
4. Replace the textual `PRIOR-ART ok` with a per-URL fetch receipt (status, body digest) plus a per-finding verdict list that the counter can check against `FINDING <task> verdict=…` lines.
5. Add `SOURCES.md` rows for the nine scout primaries opened this round, and insert S179.
6. Write the eight control receipts at the landing tip; correct the documented `c1-control-drop-capture` signature; clear the per-test flags in the blind-class control.
7. Delete the duplicate `gate-flip-check` row (keep one of SKILL.md:609 or :614) and make the counter honour `\|` escapes. Add rows for the four hyphen-dir scripts or state them as outside the universe.
8. Remove the negation exemption from `selftest_unbacked` (or restrict it to cells whose only flag is negated), and match flags with argparse rather than substring.
9. Append an erratum to `a1-observation.txt` (9249 → 5591 B; 308 → 305; cross-reference A4).
10. Disclose the wave shape (68 seats) as an append-only deviation from `§Wave shape`.
11. Regenerate `c1-after` / `c2-after` at the landing tip in a clean clone after SCORECARD/LOG edits, and only then cite them.

## Limits of this attack

- The attacked state is pre-landing. The wave-2 confirmers, the prior-art file, the labels, the lesson and the control receipts were still in progress. Re-run after they land.
- I did not re-run the W1 critics' fixtures (`C1CritTrustBoundary`, `C2CritPadding`). I cite their measurements, and I verified their mechanism by code reading and by my own fixtures (A-8, A-18).
- I did not verify each of the 74 registry rows' verdict-map arms. I checked the self-test cells, the duplicates and the parser, and read `C2ExecRowRuns`.
- The Buchanan et al. figure comes from a fetched secondary summary (`lacuna.tiptreesystems.com`), unverified against the primary. The OpenReview forum page returned HTTP 200 but its title and abstract are client-rendered and not recoverable from the HTML.
- The stripped-prose P1 count (46) is my probe, not the frozen rule. It bounds sensitivity and is not a proposed count.
- I did not examine the 28 new rows' pinned values against the tip.

## Files, receipts, cleanup, tool record

- Report (this file): `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritRoundHonesty/report.md`; the same text at `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritRoundHonesty.md` (the item's named path).
- Receipts kept under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2CritRoundHonesty/receipts/`: `census-validate.txt`; `upstream-sanitize-git-repo-test_outputs.py.fetched-readonly` (the excluded capture, read-only, **not** added to the lane); `lacuna-secondary-summary.html`; `SHA256SUMS`.
- Scratch: `/fast/scratch/hyaku/kengaku-r52/w2-W2CritRoundHonesty/` (removed before yield).
- Lane writes: none. No `git` mutation. Nothing in `plans/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/state/`, `templates/`, `scripts/`, `MANIFEST.json` or the fleet root was written.
- Tools: none installed or upgraded. Used host `python3` (stdlib), `curl`, `sha256sum`, `grep`, `wc`. No pacman, no `uv`.
