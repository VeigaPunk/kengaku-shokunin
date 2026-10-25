# RevF7 — re-check of W3ReviewKengaku F7 (S025 tier A for a live-run log)

Axis: calibration. Scope: lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` at tip `3f371d2` (base `6180e4f`); read-only seat; no writes outside this report.

## Verdict on F7: OPEN (unchanged by every commit after the review)

- F7 said: `corpus/SOURCES.md:47` gives S025 (`corpus/evidence/attrib-r23-stream.log`, a recorded live-run log that needs an endpoint to re-run) tier A, whose definition at `corpus/SOURCES.md:12–14` is "primary or authoritative for the row's scope (spec, official docs, source code, original paper, maintainer statement, **the lane's own re-runnable gate output**)" — recommended downgrade to B or justification.
- S025's history: created at `94da19e` (round-24 registry, tier A), re-checked by the W3 review at `06872d4`, still tier A after the fix commit `e21f9ea`. `git diff 94da19e..3f371d2 -- corpus/SOURCES.md` shows S025's only post-review change is the recheck cell `each round`→`90d` (the F1 E09 normalization, logged old→new at `corpus/lessons/round-24.md:135`); the tier cell was never touched. `git log -S 'S025'` across the four post-review commits (`e21f9ea a42bb40 6180e4f 4e57f14 3f371d2`) confirms no S025-touching change after `94da19e`.
- No justification was appended anywhere: `git grep 'S025' 3f371d2` hits only `corpus/SOURCES.md:4,47`, `corpus/evidence/round24-sources/gate.md:33`, `corpus/lessons/round-24.md:111,135`. The post-review fix commit message, `corpus/lessons/round-24.md` §Post-review corrections (:113–142), and `corpus/lessons/round-24-verifier-spotcheck.md` enumerate the other findings (F1 as recheck normalization; F2–F5 location/range/reason fixes; Q9/Q10 lessons) but never F7. Also confirmed: F6 (the other low-severity finding in that batch) was likewise not addressed, so the low-severity tier of that review was out of the fix commit's scope.
- Receipt integrity is sound: `git show 99cf615ca:corpus/evidence/attrib-r23-stream.log | sha256sum` = `afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131` = working-tree file = `gate.md:33` receipt; anchor line 239 verbatim: "STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL". Only the tier label is wrong, not the row's content.

## Why open matters (calibration axis)

- Tier A is support-strength curation, not truth; a mislabeled tier A means any future admission citing S025 would overstate support-strength. Today `used-by` is `—` (no admitted entry cites S025), so no admitted claim is affected — the finding remains latent, exactly as the original F7 noted.
- Round-25 pre-registration `plans/round-25-claims.md` builds interval-calibrated verdicts on exactly the S025 log population (`corpus/evidence/attrib-r2[123]-*.log`): P1 predicts the stored r22 `TARGET hyper 10/10 -> PASS` re-verdicts INDETERMINATE; the frozen rule at `plans/round-25-claims.md:36` (`PASS` iff lower ≥ bar; `FAIL` iff upper < bar; `INDETERMINATE` otherwise; `UNTESTED` iff n=0) is precisely the "an untested leg is a fail, not a pass" lesson S025 teaches. With the r25 instrument about to make this log re-verdictable offline, tier B is more accurate than ever; tier A would overstate what a stranger can re-run without an endpoint.
- Cross-check: the lane already treats S025's lesson as calibration-relevant (`corpus/knowledge/attrib-r21.md:586` and the r23 NOT-ADMITTED record) — the tier cell is the only unmoved part of this finding.

## Smallest append-only fix (no history rewrite; registry rule 2)

Registry cells change in place only as status/recheck/used-by logged old→new, or via a superseding row. Tier is not in the in-place list, so the compliant smallest fix is the **superseding row** path (the same mechanism S026 used for S023):

1. Append a new registry row S027 to `corpus/SOURCES.md` after S026:
   `| S027 | corpus/evidence/attrib-r23-stream.log — round-23 stream-trial gate output | own-work | B | the lane's own measured round-23 stream result | corpus/evidence/attrib-r23-stream.log:239 @ commit 99cf615 | supersedes S025 — S025 was tiered A as "the lane's own re-runnable gate output", but attrib-r23-stream.log is a recorded live-run log (needs an endpoint to re-run), not a re-runnable gate; per kaika-w3 review F7, downgraded to B; receipt identical to S025 (sha afaae9dd…) | queued | 2026-10-20 | 90d | — |`
   S025's row itself is left untouched (append-only).
2. Append one line to `corpus/lessons/round-24.md` §Post-review corrections (or the round-25 lesson): "F7 (tier A for a live-run log): S025 tier A was wrong — a recorded live-run log is not a re-runnable gate output; superseded by S027 (tier B), receipt identical."
3. Append the S027 receipt to `corpus/evidence/round24-sources/gate.md` (or the round-25 equivalent): source = the log path, access date = fix date, quote = the same :239 line, location = `corpus/evidence/attrib-r23-stream.log:239 @ 99cf615`, sha = `afaae9dd…`.
4. Optional, zero-registry-cost alternative if the integrator prefers no new row this late in round 25: keep S025's row and instead append to the round-25 lesson a standing caveat "S025 is tiered A in the registry but should be read as tier B (F7, unadjudicated); no admitted entry cites it." This is weaker — it leaves the defect in the registry — so the superseding row is the recommended fix.

## Residual risk / verification gaps

- I did not re-run the fleet validator (`sources-census.sh validate`) this round — out of my item's scope and the host-wide pacman pause forbids no part of it, but the item did not assign it; the E09/E08 status of any S027 row would need that check at admission time.
- The F7 adjudication question (operator ruling: is "own-work log" tier B by definition?) remains an L0 for the integrator; my recommendation stands: tier B via superseding row S027.

VERDICT: F7 OPEN at 3f371d2 — S025 still tier A (`corpus/SOURCES.md:47`), never touched by e21f9ea/a42bb40/6180e4f/4e57f14/3f371d2, no justification appended; smallest append-only fix = superseding tier-B row S027 + one lesson line + gate receipt, receipt integrity verified (sha afaae9dd… = 99cf615 blob).
