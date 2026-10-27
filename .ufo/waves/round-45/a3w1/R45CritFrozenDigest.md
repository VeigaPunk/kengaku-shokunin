# R45CritFrozenDigest — frozen-digest audit (kengaku r45, wave a3w1)

Measured lane tip: `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (master). Freeze commit: `52d7486`
(ancestor of HEAD, confirmed `git merge-base --is-ancestor` → true). The digest list was re-pinned
twice after `52d7486` as recorded "freeze amendments" — last write to `frozen-digests.txt` is commit
`0ac30a1` ("w1 seat reports + counter receipts stage 1"). The audit compares the *recorded* digests
to the tip, which is the only meaningful reading of "no pinned file changed post-freeze".

## A. `frozen-digests.txt` — 18/18 rows verify

Command: `sha256sum -c .ufo/waves/round-45/claims/frozen-digests.txt` at the lane root →
every row `OK`, `rc=0`. Covered: `plans/round-45-claims.md`, `round45_c1_verify.py`,
`round45_c2_verify.py`, `password_recovery_probe.py`, `pkg-spec-r45.json`, the dry-cases freeze
file, `tb2-password-recovery/SHA256SUMS`, `claims/c2_predictor_control.py`, and all 10
`plans/refusals45/*.py` (f1–f10).

## B. C1 counter `PINS` — 33/33 verify

`plans/round45_c1_verify.py:65-99` PINS dict (extracted and recomputed at the tip):
`plans/round44_c1_verify.py` + 10 refusal modules + all 22 honest battery modules
(battery42 ×5 `*.py`, battery43 ×7, battery44 ×10 — every `*.py` the counter globs is pinned;
`plans/battery42/__pycache__/` is untracked and ignored by the `*.py` glob).
Result: `C1 PINS extracted=33 / mismatched=0`.

## C. C2 counter pins — all verify

- `CAPTURES` dict (`round45_c2_verify.py:74-84`): 9/9 files under
  `corpus/evidence/round45/tb2-password-recovery/` match. Independent cross-check:
  `sha256sum -c SHA256SUMS` inside the capture dir → all 9 `OK`, and the manifest's digests
  equal the counter's CAPTURES values.
- File constants: `SPEC_SHA256` (`pkg-spec-r45.json`), `GATE_SHA256` (`pkg_gate.py`,
  `ea638822`), `PROBE_SHA256` (`password_recovery_probe.py`), `DRY_SHA256`
  (`password-recovery-dry-cases-freeze.txt`) — all `OK` at the tip.

## D. Inherited r44 PINS

`plans/round44_c1_verify.py:130-133`: `anchor_digest_check.py` `11bb2cad…` and
`order_check.py` `948d5e1d…` — both still hold on the tip (`OK`).

## E. Post-freeze history of pinned paths

`git diff --name-status 52d7486..HEAD` on all pinned paths shows M/R/A rows — but every M/R is
one of the claims-file-documented freeze amendments (9271dda: flat capture layout R100 renames,
counter/spec re-pin, V10 quote fixes; 7d062c0: C2 package), and each re-pinned digest is what
`frozen-digests.txt` now records — verified byte-equal in §A–§C. Decisive check: commits after
the digest-file's last write — `git log --name-only 0ac30a1..HEAD -- <all pinned paths>` →
**empty**. Nothing pinned has moved since the digests were last recorded. `git status --porcelain`
on pinned paths: clean (only untracked dev-blind leftovers in `claims/`, none pinned).

## F. Fence + receipts (the unpinned-but-checked set)

- `plans/fixture_fence.py` is deliberately unpinned (authored post-freeze; the counter prints,
  not checks, its digest — `round45_c1_verify.py:269`). Live
  `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6` equals the digest printed in
  the landing receipt `corpus/evidence/round45/c1-counter-run.txt` (`FENCE ... sha256=ac65c032…`),
  and `git log 8f9a898..HEAD -- plans/fixture_fence.py` → empty: the fence has not moved since
  the measured `PREDICATE C1 pass` run.
- Receipts `c1-counter-run.txt`, `counter-a-run.txt`, `counter-b-run.txt`, `gate-call.txt`,
  `probe-run-envelope.txt`, `password-recovery-probe.txt` are not digest-pinned anywhere; the
  probe receipt is bound only semantically by C2 V4/V9 case-name checks. A byte-exact swap
  preserving those names/counts would not be caught — residual gap, mitigated by the counter's
  per-case semantic rows.
- C2 V6 executes `scripts/sources-census.sh` via an absolute fleet path
  (`round45_c2_verify.py:97`) — outside the lane, unpinnable by lane digests; last changed
  2026-10-25 (`f47ad6ba`), pre-freeze, so no observed drift.

## Findings

No drift anywhere: 18 digest rows + 33 C1 PINS + 9 captures + 4 C2 file constants + 2 inherited
r44 PINS + the fence-vs-receipt check all verify at the tip. The only gaps are instrument
coverage notes (unpinned receipts, fleet-side census script), not mutations.

VERDICT: digest-drift-0
