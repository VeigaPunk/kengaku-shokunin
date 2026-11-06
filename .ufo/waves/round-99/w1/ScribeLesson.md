# ScribeLesson — draft-check of the round-99 knowledge entry and lesson

Seat: ScribeLesson (w1, round 99, lane `kengaku-shokunin`). Scope: read the knowledge entry
`corpus/knowledge/tb2-bn-fit-modify-grader.md` and the lesson `corpus/lessons/round-99.md`, check every
number and vector against the committed receipt, the frozen controls and the counters, and list
corrections as `claim | receipt says | fix`. No production edits; nothing was written outside this
seat's report and `w1/ScribeLesson/`.

Both documents existed when I started (knowledge entry committed in `fc65aa9a`; the lesson is in the lane
working tree with the M5 row added). I re-ran both counters and the probe independently, recomputed every
numeric claim, and diffed the BASE→T gate per row. All of that is reproducible from the receipts in
`w1/ScribeLesson/`.

## What I did (independently, not from the lane's own receipts)

- Cloned the lane `git clone --shared` into scratch, detached at T `f72a8bc7`, and at HEAD `23d58036`;
  cloned again at BASE `2233a661`.
- Built the grader venv exactly as the claims file specifies (uv venv -p 3.13; pytest 8.4.1, pandas
  2.3.2, scipy 1.16.1 → numpy 2.5.4).
- Re-ran `plans/round99_c1_replay.py` and `plans/round99_c2_rowscoped_bind.py` at T and at HEAD: both
  `PREDICATE … pass`, rc 0, with the frozen TARGET strings reproduced verbatim.
- Re-ran `plans/round99_bnfit_probe.py` standalone: the OBSERVATIONS block is byte-identical to the
  committed receipt.
- Re-ran the anchor gate at BASE and at T and diffed the DEFECT lines per row id.
- Recomputed the KS statistics of all 13 cases, the grader's true_mean/true_std, the dataset moments,
  the KS tolerance band, the seed-flip rates of the stochastic cases, and the C2 population digests.
- Re-ran the maintainer R solution (`modify_bn.R`) with R 4.4.3 + r-bnlearn 5.2.1 and compared its fit
  with the grader's constants and with the committed fixture bytes.
- Re-derived the ledger class arithmetic at BASE, the word-count cells, and the `r82c1` selftest-cell
  defect set at three revisions.
- Re-ran the source census (`scripts/sources-census.sh validate`, read-only).

Evidence: `w1/ScribeLesson/counters-at-T.txt`, `numbers-recomputed.txt`, `gate-BASE.txt`,
`gate-T.txt`, `probe-rerun.txt`.

## Verdict on the two documents

Both are **accurate**. Every number and every vector in the knowledge entry's case table is confirmed by
the receipt and by an independent recomputation; the lesson's counters, gates, word counts and class
arithmetic are confirmed likewise. I found **no correction that changes a number, a vector or a verdict**
in either document.

Corrections are listed below anyway, in the requested `claim | receipt says | fix` form. Every one is a
wording/attribution precision issue, not a wrong number.

## Corrections

| # | claim | receipt says | fix |
|---|---|---|---|
| 1 | Knowledge, header: `source: S334–S339, …tests/test_outputs.py:150` | SOURCES rows S334–S339 are the six *mined* rows; the round adds eight rows, S340 (tier A) and S341 (tier B) are *rejected*. The file's own subject sentence names the grader and the six companion sources, so the range is the mined set — but S340/S341 are round-99 rows the reader cannot see from the header. | Optional: `source: S334–S341 (S340/S341 rejected)` — or leave as is; the round-98 entry used the same convention (`S326–S330`, with S331–S333 rejected). No numeric change. |
| 2 | Knowledge, C01 row: `The fit printed by the solution equals the grader's constants: D = −12.2965135 + 0.5495886·U + 0.4485709·Y, sd 14.09165 (corpus/evidence/round99/bn-fit-modify-solution/run.log)` | The R fit is `D | U + Y` with sd **14.09165**; the grader's hard-coded `std_res_d` is **14.0916** (a truncation, the grader's literal is `14.0916`). So the fit and the grader constant agree to 5 significant digits, not identically. The R run's residual sd is also `sqrt(RSS/(n−3))` = 14.09165, while `sd(residuals)` (n−1) = 14.09024 — the grader's value is the σ̂ of the *intervened* model, not the raw residual sd. | Optional precision: "fit ≈ the grader's constants (sd 14.09165 vs the grader's literal 14.0916)". Numerically immaterial: 14.0916 vs 14.09165 changes true_std by 5e-5, far inside the ±0.0487 sd band. |
| 3 | Knowledge, C04 row: `the KS test sees D's mean shift (+0.449·E[Y])` | Recomputed: the shift is **+0.449·E[Y] = +22.588** in D-units (b_Y = 0.4485709, E[Y] = 50.354725), which is **+1.4844 sd** — a KS D of 0.516149, p = 0. | No fix needed; add the scale for a reader comparing it with the ±0.0487 sd band: "+22.6 in D units = +1.48 sd". |
| 4 | Knowledge, C12 row: `the pass/fail edge is a mean shift of about 0.048 sd` | Bisected independently on the grader venv: the edge is at **±0.048702 sd** (D = 0.019477, p = 0.001); the band is symmetric (±0.0480 → D = 0.019197, p = 0.00124218, still passing). | No fix needed — "about 0.048 sd" is correct at 3 dp. The lesson's `predictions-amendment-1.txt` numbers (0.048 → D 0.0192, p 0.00124) agree. |
| 5 | Knowledge, C03 row: `U,R,Y,M all 0.0; D drawn from the target normal` | The builder draws D from `default_rng(3)`, i.e. a *seeded random* draw, not a fixed array; it is a stochastic case (the probe's builder pins the seed, so the observed bytes are reproducible). Recomputed p = 0.640865 for seed 3; over 200 seeds the case **never** flips (0 failures, min p = 0.00912). | Optional: say "seeded draw (rng seed 3); 0/200 seeds flip" — that is the Q84-style disclosure the case's `why` field is asked to carry (QUALITY Q84). The current `why` in `plans/round99-cases.json` does not state a flip rate for C03, unlike the C11 amendment. Routed, not repaired. |
| 6 | Knowledge, C04 row: `sample from the fitted BN without the Y intervention` | Also a seeded draw (`default_rng(4)`) and it refits OLS on the committed dataset. Recomputed over 200 seeds: **0/200** seeds make `sample_data` pass. | Optional: add "0/200 seeds flip". Same Q84 disclosure gap as #5. Routed, not repaired. |
| 7 | Knowledge, C05 row: `This is a realistic R slip: write.csv defaults to row.names = TRUE` | The maintainer's `solve.sh` writes `write.csv(..., row.names = FALSE)` explicitly — the probe's builder emulates the *un-guarded* default with `sol.to_csv(index=True)`, which adds an unnamed index column. The grader's `test_sampled_csv_col_names` uses `all(col in columns)` (inclusion), so the extra column passes the names leg and fails the `len(columns) == 5` assert inside `test_sampled_data`. | No fix needed; the sentence is about the grader's tolerance, which is correct. Optional: name the inclusion-vs-equality asymmetry explicitly, since it is the mechanism. |
| 8 | Knowledge, `Limits`: `The fit equal to the grader constants is the evidence that the fixture is faithful` | Confirmed and strengthened: re-running the maintainer R script with bnlearn 5.2.1 reproduces the same fit (`D \| U + Y`: −12.2965135, 0.5495886, 0.4485709, sd 14.09165) and a byte-identical `learned_dag.csv` / `intervened_dag.csv`; the committed `final_bn_sample.csv` has D mean 15.3187212291, matching `run.log`. Its KS against the grader's constants is D = 0.009795, p = 0.290707. | No fix needed. Optional: add that the fixture's own KS p is 0.29, which is the positive control's quantitative margin. |
| 9 | Knowledge, `What this teaches`: `Y is never required to be 0 after the intervention, and U, R and M are never read (C03)` | Confirmed by the captured grader: `test_sampled_data` reads only `final_bn_sample["D"]`; the other four sample columns are checked for *presence* only. The C03 case sets U,R,Y,M to 0.0 and passes. | No fix needed. (Worth noting for a later round: `test_sampled_csv_col_names` also asserts `not final_bn_sample.empty`, so "never read" is true for the four columns but the file must be non-empty.) |
| 10 | Lesson, `## Gate`: `S334–S341 were added: 7 tier A, 1 tier B; 6 mined, 2 rejected. Rows went 325 → 333.` | Confirmed from `corpus/SOURCES.md`: the eight new rows are S334 (code/A/mined), S335 (code/A/mined), S336 (code/A/mined), S337 (docs/A/mined), S338 (code/A/mined), S339 (dataset/A/mined), S340 (code/A/**rejected**), S341 (docs/B/**rejected**) → 7 tier A, 1 tier B, 6 mined, 2 rejected ✓. Base-row count 325 ✓, tip-row count 333 ✓ (the gate's `rows=` field agrees at both tips). | No fix needed. |
| 11 | Lesson, `## Gate`: `The word counts of S334, S336, S337, S338 and S339 were typed by hand at C and were wrong: 4→5, 4→3, 11→12, 5→6 and 5→1.` | Confirmed from `b71b990a`'s diff of `corpus/SOURCES.md`, and each corrected cell now equals `len(quote.split())` exactly. `plans/anchor_line_check.py` at T prints `live=5 cells=5` rc 1; at BASE `live=0 cells=0` rc 0; in the tree now `live=0 cells=0` rc 0. | No fix needed. |
| 12 | Lesson, `## Gate`: `Gate findings went 45 → 33 at T.` | Confirmed by re-running the gate at BASE (rows=325 tokens=209 defects=45) and at T (rows=333 tokens=217 defects=33) and diffing **per row id**: cleared = exactly S173–S177, S180, S220, S225, S270, S285, S293, S306 (the 12 POP rows); newly defective = none; changed = none. So the 12-finding drop is exactly the population, with no side effect on any other row. | No fix needed — and this is stronger than the round's own `GATE defects base=45 rev=33` line, which alone could not distinguish "12 population findings cleared" from "12 findings cleared plus 12 added elsewhere". |
| 13 | Lesson, `## Gate`: `and no new file carries a URL.` | Confirmed: of the 10 committed `PROVENANCE.md` files at T, the 8 new ones (round50/59/61/79/82/92/93/95) contain **0** `://` lines; the two pre-existing ones (`corpus/evidence/PROVENANCE.md`, round 37's) still carry their URL columns and are byte-identical to BASE. | No fix needed. Optional: name the two legacy URL-bearing files so a reader knows the channel is closed only for *new* files — the round-98 M4 defect's URL column still exists in `corpus/evidence/PROVENANCE.md`. |
| 14 | Lesson, `## Gate`: `The census is finding-level, not row-level … 105 of the 313 outside rows carry no gate output at all (F7).` | Recomputed independently: BASE has 325 SOURCES rows, POP is 12, so outside = 313 ✓; exactly **105** outside rows carry no gate note at BASE, and all 105 are also defect-free, so rewriting one of them is invisible to a finding-level census ✓. | No fix needed. |
| 15 | Lesson, M4: `the thinnest classes are subprocess-exec 15/45, crypto-credential 4/12, shell-exec 2/6 and numeric-band 4/10, yet round 99 picked a file-artifact member` | Re-derived from the ledger at BASE `2233a661`: subprocess-exec 15/45 ✓, crypto-credential 4/12 ✓, shell-exec 2/6 ✓, numeric-band 4/10 ✓, filesystem-metadata 4/10 ✓, file-artifact 33/76 ✓, executed total 42 ✓. | No fix needed. (The lesson's earlier considerthese block prints `file-artifact 33/76` — the BASE value — while the Frontier block prints `34 of 76`; both are right for their stated baselines, and Q86's text quotes the older `32/76`/`41 of 88` snapshot from the considerthese file. No edit required.) |
| 16 | Lesson, M5: `BASE has 13 DEFECT and T has 17 (.ufo/waves/round-99/L1/harm/r82c1-tip-*.txt). … Re-run: 13 DEFECT, set equal to BASE.` | Confirmed by running `plans/round82_c1_plans_registry.py --tip X` at three revisions: tip=BASE → 13 DEFECT (0 round99 rows), tip=T → 17 DEFECT (the 4 extra are exactly the 4 new round99 registry rows, all `ROW-SELFTEST-UNBACKED`), tip=`3fdecf31` → 13 DEFECT with the **full defect-line set equal** to BASE. All four `round99-*` SKILL.md cells now read `none declared — no self-invocation mode; …`. | No fix needed. |
| 17 | Lesson, M5: `the L1 battery missed this because the gate defaults --tip to master, so the battery's BASE and tip logs read the same tree` | Confirmed: `plans/round82_c1_plans_registry.py` has `--tip` default `None` → `tip = tip or git rev-parse master`, and `run_harm.sh`'s r82c1 line is `python3 plans/round82_c1_plans_registry.py --lane .` with no `--tip`. So both the BASE and tip invocations read `master`. The separate `r82c1-tip-*.txt` receipts were produced with an explicit `--tip`, which is why they differ. | No fix needed; optionally say explicitly that the *receipt* receipts (`r82c1-tip-*.txt`) were run with an explicit `--tip`, so the discrepancy between the two receipt families is explained in the lesson itself. |
| 18 | Lesson header: `receipts 23d58036; dated correction after T b71b990a.` | `b71b990a` exists and is an ancestor of HEAD ✓. But the lane has **two** dated corrections after T: `b71b990a` (word counts, lesson M3) and `3fdecf31` (the four `round99-*` selftest cells, lesson M5), plus the `fc65aa9a` integration commit that added the knowledge entry. | Optional: list `3fdecf31` in the header's dated-correction list so a reader sees both post-T repairs; the lesson body already cites `3fdecf31` in M5. |
| 19 | Lesson, `## Gate`: `**Admit / reject for the closure spot-check:** admit S334 (A), reject S340 (A) and S341 (B).` | S340 is tier **A** and S341 is tier **B** ✓; their SOURCES status is `rejected` ✓; S334 is tier A, status `mined` ✓. But the SOURCES row for **S335–S339 is also `mined`** (tier A), and the lesson's admit line names only S334. | Precision: the line reads as "one admit, two rejects" while the registry admits six. Optional: `admit S334–S339 (A), reject S340 (A) and S341 (B)` — or say explicitly that only S334 is routed to the closure spot-check and S335–S339 are admitted by the round. |
| 20 | Lesson, `## Gate`: `Rows went 325 → 333.` and `executed went 42 → 43` | Both confirmed: BASE gate `rows=325`, T gate `rows=333`; BASE ledger executed 42, T ledger executed 43. | No fix needed. |
| 21 | Lesson, `## Gate`: `the diff from C onward touches only S334–S341` (SOURCES.md) | Confirmed: `git diff BASE T -- corpus/SOURCES.md` is `8 ++++++++`, 0 deletions — insert-only ✓. The two dated corrections after T (`b71b990a`) also touch only SOURCES rows S334/S336–S339, still within the eight new rows ✓. | No fix needed. |
| 22 | Lesson, `## Gate`: `the frozen anchor-digest gate binds the new rows by url-task (S339 binds by its row path)` | Confirmed from the gate's `--verbose` output at T: `BIND S334/S335/S336/S337/S338/S340/S341 … by=url-task`, `BIND S339 … by=row-path` ✓ — exactly as the lesson states, including the one exception. | No fix needed. |
| 23 | Lesson, `## Gate`: `Census: rc 0 at start (L1/census-start.txt). The end result is in L1/census-end.txt.` | Re-ran the census read-only at the current lane tip: **rc=0**, **31 W04 warnings**, the newest being S334 (duplicate URL of S181's `bn-fit-modify/tests/test_outputs.py` across scopes) — matching `census-start.txt`, `census-end.txt` and `controls/candidate/sources-validate.txt`, all of which also say 31. | No fix needed. One caveat for the record: `L1/census-end.txt` and `L1/harm/r82c1-tip-*.txt` are **untracked** in the lane working tree at the time I read them (`git status` shows them as `??`), while the lesson cites them as evidence. Not a claim error, but the evidence should be committed before the round closes. |

## Numbers that could not be verified as stated (checked, no correction)

- The knowledge entry's `recheck: on-release` and `verified-at:` header fields follow the round-97/98
  convention exactly (`tb2-regex-chess-grader.md`, `tb2-sparql-university-grader.md`); the round-99
  values are the correct dates/revision.
- `GRADER_SIDE python,pandas,scipy,pytest 3.13 2.3.2 1.16.1 8.4.1` and `BUILDER_SIDE numpy 2.5.4` in the
  receipt match the venv I built and the `test.sh` pins verbatim.
- The knowledge entry's leg names (`bn_exists, ldag_exists, ldag_cols, ldag_struct, idag_exists,
  idag_cols, idag_struct, sample_cols, sample_data, reward`) match `LEG_ORDER` in the receipt and the
  `TESTS` tuple in the probe, in file order, including the grader's own `test_intervened__data_structure`
  double underscore.
- `C2` claim: `Pop (claim-local, one rule, derived at BASE and frozen as POP)` — the frozen `POP` in
  `plans/round99_c2_rowscoped_bind.py` matches `.ufo/waves/round-99/L1/c2-pop.txt` exactly for all 12
  ids, tokens and capture paths, and every token equals the sha256 of the capture it names.

## Scope / limits of this draft-check

- I checked the knowledge entry and the lesson as they stand in the lane working tree at
  2026-11-06 ~11:45 -03. The lesson has uncommitted edits (the M5 row and the anchor-re-verification
  paragraph); I checked the working-tree version, which is the one the L1 is still editing.
- The committed `corpus/evidence/round99/bnfit-probe.txt` records `LANE_TIP 24a5a555` (the freeze commit
  F) while the file was committed at C. The OBSERVATIONS block is byte-identical to my re-run at T, so
  the receipt is faithful; the header simply names the revision the probe was *written* against. I note
  it as a fact, not a correction — C1's L3 only requires that the receipt's `LANE_TIP` be an ancestor of
  the measured revision, and F is an ancestor of T.
- No production files were edited, no commits, no push, no git mutation in the lane or the fleet repo.
  All scratch lived under `/fast/scratch/hyaku/kengaku-r99/ScribeLesson/` and was removed on exit; the
  only writes are this report and `w1/ScribeLesson/`.
- Tooling: `uv` and `uv venv`/`uv pip` (official PyPI channel) to build the grader venv; the pre-existing
  `/fast/scratch/kengaku-r99/renv/bin/Rscript` (R 4.4.3, r-bnlearn 5.2.1) for the R re-run; stock
  `git`, `python3`, `grep`, `sed`. No pacman transaction was run.

## Bottom line

The round-99 knowledge entry and lesson are numerically sound: every case vector, every KS statistic,
every counter TARGET field, the gate delta (45 → 33, exactly the 12 population rows, no side effect),
the word-count corrections, the class arithmetic and the `r82c1` defect counts reproduce independently.
The 23 items above are wording/attribution precisions and one disclosure gap (the seed flip rate for the
stochastic cases C03/C04, which QUALITY Q84 asks for and which `plans/round99-cases.json` does not
carry). Nothing here changes a claim, a number or a verdict; items 5, 6, 19 and 23 are the ones worth
an edit, and 5/6/19 are routed rather than repaired because the case table is frozen at F.
