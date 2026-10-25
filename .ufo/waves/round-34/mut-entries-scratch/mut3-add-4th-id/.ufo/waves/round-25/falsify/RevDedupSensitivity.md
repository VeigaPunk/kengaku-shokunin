ATTACKS: r22 dedup — `attrib-r22-legs.log:312-362` ≡ `attrib-r22-opencode-trials.log:204-254`, kept-vs-dropped TARGET equality, and the pooled-if-distinct `40/40 CP95 [0.911903,1]` sensitivity line (tip 8ea41f9ed; pristine copy /tmp/k25w2-RevDedupSensitivity)

Reproduction: `python3 plans/attrib_calibration.py --summary` in the pristine copy → exit 0; output is byte-identical to `corpus/evidence/round25-calibration/attrib-calibration-summary.txt:1-49` (empty `diff`). Report mode prints `duplicate: …legs.log:312-362 == …opencode-trials.log:204-254 (counted once; header fields differ: stamp,journal,frozen_sha256)`.

**S1 (SURVIVES): the two tables are identical.** A line-by-line diff of the two 51-line blocks finds exactly 6 differing lines, none of them a table row or stored verdict line:
- 312/204 stamp (11:57:39Z vs 11:52:23Z); 313/205 journal window (@1792151616..737 vs @1792151440..562); 314/206 request-lines (37 vs 68)
- 315/207 frozen pin (77b8d4a0 vs 3d7861f8); 349/241 `loo:hdr_tells` (19/20 vs 18/20); 362/254 score_summary (only the `ablations` and `frozen_sha256` keys differ)

Rows legs:320-339 equal opencode:212-231 in all 7 columns (`parse_receipt` rows `==` True, `_table_key` equal). GT counts (341/233) and ACCURACY (342/234) are byte-equal. The awk oracle computes the same table_md5 71b4c55b… for both blocks on its own (oracle:16,23,37). Info: the oracle cites the spans as 312-363/204-255, an end-line convention different from the instrument's; lines 362/254 are the score_summary lines.

**S2 (SURVIVES on this data; the instrument does not enforce it): kept TARGET lines equal the dropped block's.** The kept block is opencode:204-254, chosen as the earliest stamp (`plans/attrib_calibration.py:561-562`). Byte-equal pairs: TARGET hyper legs:344 = opencode:236 and TARGET opencode-go legs:345 = opencode:237; `target_stats` is also equal. The dropped block is still re-derived (`:536-549`; 13 checks, 0 failed). Mutation M3 changed legs:344 `-> PASS` to `-> FAIL` → exit 1, `MISMATCH attrib-r22-legs.log:344 target:hyper: stored=[…'FAIL'…] recomputed=[…'PASS'…]`.
- LOW L1: no code compares the kept block's TARGET lines with the dropped block's. `_table_key` (`:511-512`) is (trial, prediction, GT, chain): it leaves out the class column and the stored bar/min-n, matching claims:31-32 word for word.
- M2: swapped the dropped block's T01 class and rewrote legs:344 to `n=9 … 9/9 … -> FAIL` plus target_stats, so the block stays self-consistent. Result: exit 0, mismatches=0, dedup still fires, and the dropped stored FAIL disappears without a warning.
- M2b: changed the dropped block's TARGET bar 0.80 → 0.95 → exit 0, dedup fires, the different bar is ignored. r22 is safe only because these columns happen to be equal.

**S3 (SURVIVES): the sensitivity arithmetic is right.** `:570-571` computes 2×(dropped k) / 2×(dropped n) = 40/40. This is valid because equal keys mean an identical (pred, GT) multiset, so kept 20/20 + dropped 20/20 = 40/40.
- CP lower bound at k=n is (α/2)^(1/n). Python Decimal at 50 digits: 0.025^(1/40) = 0.911902697121, and p^40 = 0.0250000000000000000. Wilson lower bound: 40/(40+z²) = 0.912378398802.
- scipy 1.18.1 `binomtest(40,40)`: exact [0.911903,1], wilson [0.912378,1]. statsmodels 0.15.0 beta: (0.911903,1.0). The printed line `summary:24` is correct to 6 dp.

**B1 (BREAKS, MEDIUM): the sensitivity line reports the one r22 estimate the dedup choice cannot change.** I pooled both executions through the instrument's own `block_estimates` (`python3 /tmp/k25w2-RevDedupSensitivity/_scratch/pooled.py`).
- 5 estimates flip from 10/10 [0.691503,1] INDETERMINATE to 20/20 [0.831567,1] PASS (n=20 meets the power ask of 17): `target:hyper`, `recall:hyper`, `recall:alibaba-token-plan`, `specificity:hyper`, `specificity:alibaba-token-plan`. Accuracy stays PASS (20/20 → 40/40).
- Totals under dedup: PASS 12 / INDET 11 / UNTESTED 12; transitions FAIL>UNTESTED 2, PASS>INDETERMINATE 1, PASS>PASS 4 (matches summary:49). Pooled: PASS 17 / INDET 6 / UNTESTED 12; FAIL>UNTESTED 2, PASS>PASS 5.
- Two results exist only because of the dedup choice: the round's only PASS→non-PASS transition (`summary:32`, `SCORECARD.md:667`, knowledge `attribution-interval-calibration.md:15-16,23`, "one stored PASS does not survive") and P1's YES outcome (claims:52; Brier 0.0025).
- Knowledge `:91-93` says "the pooled 40/40 line shows what counting them separately would give. No verdict rests on that line." The second sentence is true; the first is false, because counting them separately also gives TARGET hyper 20/20 PASS.
- The "conservative direction" (claims:131) is conservative for PASS claims. It is also the direction that creates C1's headline finding, and no output line marks target:hyper as dependent on the dedup choice.

**B2 (BREAKS, LOW-MEDIUM): P2 is scored as occurred, against the lane's own finding.** P2 (claims:53) is "authoritative blocks are the same sample (dedup fires)". It is scored outcome 1 (`SCORECARD.md:671-672`, Brier 0.2025). Yet claims:129-131, knowledge:91-92 ("two executions with disjoint request windows") and `DupR22Scout.md:52` ("its gloss 'same sample' is false") all say the blocks are not the same sample. Scored on the main clause, the outcome is 0: Brier 0.3025, mean 0.0452 → 0.0652. No calibration credit is taken from this score (`:673`), so the effect is on reporting consistency only.

**LOW L2: no check guards the sensitivity line.** Mutation M1 (`:571` `2 * len(` → `3 * len(`): `--selftest` → "selftest: 14 checks, 0 failed", exit 0; lane `--summary` → `sensitivity:pooled-if-distinct 40/60 … cp95=[0.533127,0.783131]`, exit 0, TOTAL unchanged.
- Why it goes unnoticed: `_fixture_failures` (`:815-822`) checks only `res["estimates"]` and FX_TOTALS (`:811-812`), while the sensitivity line lives in `res["shares"]` (`:573`). `sensitivity_lines` is not among the TOTAL keys (`:639-641`), and the oracle prints no pooled interval.
- The fixture does produce a sensitivity line (fx-dup `:767-768`), but nothing asserts its value.

**LOW L3: pooling only handles pairs.** M4 added a third execution with an identical table. Output: two `pooled-if-distinct 40/40` lines instead of one 60/60 (the factor 2 is hardcoded at `:570-571`). Not live for r22.

Live-tree note (read-only `git diff 8ea41f9ed`): the uncommitted live `SCORECARD.md` already adds B2's two readings with the same numbers (0.3025 / 0.0652). The live `attrib_calibration.py` diff adds selftest A8 (the key separates tables that differ in a prediction). Neither change touches B1, L1, L2 or L3.

Residual risk (outside this item):
- The tie-break keeps the block whose journal window carried more foreign traffic: opencode extra_req=48 vs legs extra_req=17 (oracle:16,23). No numeric effect here, because the tables are identical.
- The last-block supersede rule plus dedup leave legs.log contributing 0 trials. That includes run-1 T03 (legs:270), r22's only opencode-go GT serve.

Verification gaps: the GT journal join was not re-opened; no live requests were made. Mutations: `/tmp/k25w2-RevDedupSensitivity/_scratch/mutate.py` (M0 control exit 0, then M1–M4).

VERDICT: PARTIAL — the identical tables, the TARGET equality and the 40/40 CP95 [0.911903,1] arithmetic survive. The sensitivity line leaves out the 5 pooled estimates that flip INDETERMINATE→PASS, including TARGET hyper (the only PASS>INDETERMINATE transition, and P1's outcome). P2 is scored "same sample" against the lane's own finding of two executions.
Installs: scipy 1.18.1 + statsmodels 0.15.0 via `uv run --no-project --with scipy --with statsmodels` (PyPI, temporary environment in the uv cache, nothing installed globally), as an independent CP/Wilson reference. No pacman.
