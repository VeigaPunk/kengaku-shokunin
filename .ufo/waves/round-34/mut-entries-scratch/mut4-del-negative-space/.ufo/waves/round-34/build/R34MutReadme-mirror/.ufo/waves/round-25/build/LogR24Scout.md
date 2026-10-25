# LogR24Scout — round-24 LOG / SCORECARD / fleet report / closure cross-check

Read-only. Four surfaces compared for every number, verdict and commit hash:
A = `kengaku-shokunin/LOG.md:231-267` (§Round 24; :208-229 §Round 23)
B = `kengaku-shokunin/SCORECARD.md:582-638` (§Round 24; :569-580 §Round 23)
C = `.ufo/reports/round-24/kengaku.md`
D = `kengaku-shokunin/corpus/lessons/round-24-verifier-spotcheck.md`
Tiebreak = repo bytes (read-only), because two documents can share one stale value.

## Disagreements (7)

1. **SOURCES row total 25 vs 26.**
   25: A:244 "25 rows"; B:557 "rows 25"; B:596 "absent → 25"; C:26, C:113 (`sources_rows | absent | 25`), C:172.
   26: D:17 "capability `sources-registry` (26 rows, census ok)"; C:276 "`sources_rows` 25 → 26".
   Measured 26: `grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md` → 26. D and C:276 match; A:244, B:557, B:596, C:26/113/172 are stale.

2. **Tier/status counts.** Stated `A=24 C=1`, `rejected=2`: A:244-245; B:557; C:114. Measured: tier.A=24 tier.C=2, mined=18 queued=5 rejected=3 — S026 (`corpus/SOURCES.md:48`) is a third rejected tier-C row beside S003 (`:25`) and S023 (`:45`). C:276 "unchanged except `sources_rows` 25 → 26" cannot hold: 26 rows with A=24 forces C=2, and the added row is `rejected`, so rejected 2→3. C:180 "2 rows" is stale too.

3. **`lesson_mistake_rows` 20 vs 22.**
   20: A:252; B:597; C:120; C:159 (class split PRED3 LAND7 MEAS3 PROC4 STOP2 DISC1).
   22: C:276 "20 → 22"; D:17 (M21/M22 landed in `e21f9ea`).
   Measured 22: exact census awk → 22; final classes MEAS=4, DISC=2 (`corpus/lessons/round-24.md:31-32`), so C:159 is stale on two class counts as well.

4. **Criteria added 18 vs 20.** C:163 "Criteria added: 18" = Q1–Q8 + R1–R10 (A:242-243 names the same sets). D:17 adds Q9/Q10; `corpus/QUALITY.md:67,75`; measured Q=10 + R=10 = 20. (Key `closure_criteria_citing_round24` stays 10 — its awk counts only `R` rows — so B:597/C:121 are not wrong on that key.)

5. **Round-24 admission: pending vs ADMITTED.**
   Pending: B:594 "Self-verdict (pending non-author check)"; B:597 "score held"; B:599-603 "the operator rules on whether C2 admits"; C:198 "Verdicts (self, pending non-author verification)"; C:203-207 "That dissent stands unresolved … the operator rules".
   ADMITTED: D:17 "ADMITTED after post-review fixes `e21f9ea` … C2 is a calibration move"; C:246-248 "the orchestrator's adjudication … C2 ruled a real calibration move".
   A (:231-267) and B contain no `e21f9ea` and no r24 ADMITTED record (`grep -c e21f9ea` → 0/0). D is the integrator record; A/B/C §Verdicts are pre-adjudication text.

6. **Quality trend verdict.** C:173 "**Quality: improved.**" (evidence :174-178) vs D:17 "Trends: expansion improved, quality unchanged, discernment improved". Direct contradiction on the same trend scale; C's post-review section (:281) updates discernment only and never retracts quality.

7. **Discernment trend.** C:179 "**Discernment: unchanged, pending.**" vs C:281 "discernment moves from unchanged to improved" and D:17 "discernment improved". Stale section inside C.

## Checked, no disagreement
- **Hashes:** `94da19eea7b9…`, `06872d4dbf6c…`, `e21f9ea989…` all resolve (`git rev-parse`); D:5 "e21f9ea98" is a valid 9-char prefix; `corpus/evidence/round24-census/after.txt:1,3` records HEAD `94da19e`, matching C:96. A names no r24 lane commit (only base `99cf615`, A:267) — omission, not contradiction.
- **Gate:** `n=733 mismatches=0 errata_pinned=1` at A:261, B:555, B:619, C:129; D:17 "733/733 PASS".
- **Axis/state numbers:** 7/7/8/9/8/8/8, 6/6→0/6, 16 map rows, 5 frontier, 4 province sections, 28/28, 10/10, 3 capabilities, saturation 8/4 — A, B, C consistent.
- **Anchors:** A:208 ↔ B:569 ↔ C:43/85 (r23 NOT-ADMITTED) both resolve; C:85 `LOG.md:208` and C:43 `SCORECARD.md:569` correct.

## Adjacent calibration notes
- B:618 D14 errata cites `SCORECARD.md:305` for "All 149 checks"; the phrase is at B:306 (B:305 is the bullet's first line). Off-by-one anchor — matters to C2 P2b anchor resolution.
- D:12 "re-fetched 17 of 20 web rows" vs C:174 "23 web sources": registry is 26 rows / 25 unique URLs / 23 non-own-work; 20 = 23−3 dynamic (S005/S006/S023) is plausible but unstated — left as a gap, not counted as a disagreement.
- `bash scripts/sources-census.sh validate kengaku-shokunin` → `ok`, exit 0; it does not catch stale prose counts, so items 1–4 survive a "census clean" claim.

VERDICT: the four surfaces agree on hash chain, gate counts and axis numbers, but diverge on 7 live items — SOURCES 25/26 with tier C 1/2 and rejected 2/3, mistakes 20/22, criteria 18/20, admission pending/ADMITTED, and the quality/discernment trend labels; repo bytes side with the closure on 1–4 and with the closure on 5, so SCORECARD:557/:594-603 and report:159/173/179 are the stale sides a mechanical state check will flag.
Installs: none (no tool added or updated).
