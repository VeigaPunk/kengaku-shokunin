# TrialVsImplScout — r21 trial-only vs scored receipts (read-only)

## Q1 relation: same frozen grid, different executions — not re-scores
- ds: trial-only T01 10:23:45.360Z, last request 10:25:01Z (`corpus/evidence/attrib-r21-ds-trials.log:8,128`) vs impl T01 10:21:04.575Z, last 10:22:20Z (`attrib-r21-impl-ds-trials.log:8,128`); 20 distinct `chatcmpl-…` ids per file, first `f2a8b266…` vs `8aaf6e71…` ⇒ distinct responses.
- Seat lives in the addendum; line 1 is a hardcoded label — `attrib-r21-ds-trials.log:132-138`: "the header line above says 'instrument-impl seat' because plans/attrib_probe.py cmd_trials hardcodes that label; this file is trial-runner-A's execution … Instrument-impl's own ds run is a SEPARATE file … the windows do not overlap".
- The trial-only file has 0 `## GT + scoring` blocks (`grep -c 'GT + scoring'` = 0); its GT was "deferred to the scorer seat" (`.ufo/rounds/round-21/goal-wave/scorecard-verdict-draft.md:158`) ⇒ no re-score of it exists.
- glm is the same pattern but overlapping: 10:21:42.025→10:24:04 (`attrib-r21-glm-trials.log:8,141`) vs 10:22:32.489→10:24:43 (`attrib-r21-impl-glm-trials.log:8,140`), ~85 s concurrent on :8793. impl-glm's GT window 10:22:27–10:25:11 (`:143`) logs `request-lines=99 leg-rids=99` for its 22 client rids / 31 leg attempts (`:144`) ⇒ foreign traffic inside that GT window.

## Q2 four blocks = append-only debug trail, not four samples
- Starts `:130,176,222,268`; ACCURACY `:159,205,251,297`. B1/B2: all 20 rows `EXCLUDED:UNMATCHED` → 0/0 FAIL; B3: T06/T10 `AMBIGUOUS(2)` (`:247-248`) → 18/18 FAIL on the min-n 20 gate; B4: no exclusions → 20/20 PASS.
- B1 ≡ B2 byte-for-byte except the read stamp: `diff` of `:130-175` vs `:176-221` returns `1c1`, 10:25:25Z→10:25:58Z. The receipt records neither fix nor no-op between them; identical all-UNMATCHED output only proves at least one zeroing defect survived, not which. [INFERENCE]
- Stated cause `:314-334`: A window start −0.5 s vs 1-s stamps; B `parse_ts` re-applied the −03 host offset → +3 h epochs; C truncation pulled the next trial's stamp into the prior window ("a first adjudication of 18/18", `:328-332`), fixed by greedy in-order 1:1.

## Q3 what frozen population P1 takes
- The LAST block (`plans/round-25-claims.md:29-30`, citing `:316`): `:268-312` → 20/20, GT all `alibaba-token-plan`, PASS.
- CP95 offline (k=n: 0.025^(1/n)) = [0.831567, 1.0] ≥ 0.80, n=20 ≥ 17 ⇒ PASS, stored verdict unchanged.
- Divergences the instrument must encode: B1/B2 stored FAIL at n=0 ⇒ UNTESTED; B3 stored FAIL at 18/18 ⇒ CP95 lower 0.814698 ⇒ PASS. B3 is outside P1's scored set (debug trail, `:318-320`), but `plans/round-25-claims.md:25-26` says "every stored point verdict re-verdicted" — unless B1-B3 are labelled non-authoritative the instrument emits an interval PASS on a stored FAIL.
- glm's last/only block (`attrib-r21-impl-glm-trials.log:173`) 22/22 ⇒ [0.845627, 1.0] PASS.

## Per-leg preview (owned axis, derived from the P1 tables)
- ds: alibaba recall 20/20 [0.831567,1] PASS; hyper and opencode-go recall 0/0 UNTESTED; hyper and opencode-go **specificity** 20/20 each [0.831567,1] (all 20 GT are negatives) — specificity is estimable where the matching recall is not.
- glm: zai recall 13/13 [0.752947,1] and devin 9/9 [0.663733,1] INDETERMINATE; zai specificity 9/9 and devin specificity 13/13 likewise. P4's event is already satisfied by r21 alone.
- No incorrect r21 scored trial (all rows `YES`, `:229-246` and `:275-294`); P5 therefore rests on r22/r23.

## C1 caveats
- impl-glm's 22/22 is the only scored glm sample and its 99-rid window makes the trial→GT binding non-unique (`plans/attrib_probe.py:909-938`, greedy earliest-candidate). Cross-run masking is plausible because both glm runs used identical bodies (215 B std / 233 B err, verified in both files), stream=True and the same shim chain, so the "22 independent scored trials" independence is weaker than the count. Dedup (`plans/round-25-claims.md:31-32`) does not fire: tables differ and the trial-only file emits no block.
- Instrument pin: receipts record `b3e18c78…` (`:3`); current `plans/attrib_probe.py` sha256 = `489f938a198e08cf8c30efc3ca24ea5fac90ef3909d80aec0b1f62c90616e06b` (r22 stream hardening `:919-923`) ⇒ re-derive offline from receipt tables, never re-run the current probe.
- No web source opened this round; no SOURCES row warranted. No installs.

VERDICT: r21 trial-only logs are independent executions of the same frozen grid (never scored), not re-scores; impl-ds's four blocks are an append-only debug trail (two 0/0 matcher failures, an 18/18 AMBIGUOUS artifact, then 20/20 after greedy 1:1), and P1 takes the last block — 20/20 PASS, CP95 [0.8316,1.0] — while the 18/18 debug block would re-verdict PASS against its stored FAIL and must be marked non-authoritative.
