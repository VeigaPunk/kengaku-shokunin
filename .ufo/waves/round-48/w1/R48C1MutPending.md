# R48C1MutPending — blocked/pending/never-returned accounting

## Scope and freeze gate

Axes: **calibration** (C1 trace-accounting sensitivity) and the requested **control false-pass** check.

`REV a543d92083557dd9b33ee674e9b99b03411f80af` — the isolated scratch clone was checked out at the specified stage-1 freeze. `plans/round-48-claims.md` exists at that revision; `git merge-base --is-ancestor a543d92083557dd9b33ee674e9b99b03411f80af bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767` succeeded (`FREEZE-ANCESTOR-OK`). The committed claim-file digest and lane copy both printed `87e6075ff2c0748be0b087a4d6d6a2dd9b7a0891691fcec70dc6239978768672`.

Stage 2 is **not present** at this revision (`test -f plans/round48_c1_verify.py; echo "round48_c1_verify exists: $?"` → `round48_c1_verify exists: 1`). Therefore I ran no scored C1 counter or control on claimed work. The probe below is a bounded unit detector against the inherited round-46 trace-accounting helper only; it is not a C1 predicate/control receipt.

## Detector and mutant results

The detector supplies 16 synthetic strace cases to `round46_c1_verify.py::analyse()`: successful and EACCES opens, ENOENT, blocked and successful `access`, file/directory/symlink stats, resumed and EOF-pending calls, `? ERESTARTSYS`, dirfd-relative path resolution, paths inside `d`/`ctl`/outside the scratch root, and a failed write-family call. It asserts the exact touch paths. The first draft used an incorrect oracle for `access(...)=EACCES` and failed pristine; inspection showed the frozen helper intentionally counts this blocked access as a touch. I corrected the oracle before scoring mutants; that initial detector failure is not counted as a killed mutant.

Exact detector commands and observed outputs:

```text
python3 probe_accounting.py lane/plans/round46_c1_verify.py
DETECTOR baseline-ok cases=16 flips=0
PRISTINE_EXIT=0

python3 run_mutants.py lane/plans/round46_c1_verify.py counter-mutant.py mutant-results.json
M1-never-returned-none-ignored: killed flips=['open_pending_never_returned']
M2-restart-blocked-ignored: killed flips=['open_eretart_blocked']
M3-access-blocked-negated: killed flips=['access_eacces_outside_blocked_touch']
M4-open-error-set-inverted: killed flips=['open_eacces_outside', 'open_enoent_ignored']
M5-pending-eof-loop-dropped: killed flips=['open_pending_never_returned']
M6-ctl-carveout-dropped: killed flips=['open_under_ctl']
M7-resumed-call-ignored: killed flips=['open_pending_resumed']
M8-dirfd-resolution-dropped: killed flips=['open_dirfd_relative']
RESTORED ok ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508

python3 probe_accounting.py counter-mutant.py
DETECTOR baseline-ok cases=16 flips=0
RESTORED_DETECTOR_EXIT=0
sha256sum lane/plans/round46_c1_verify.py counter-mutant.py
 ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  lane/plans/round46_c1_verify.py
 ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508  counter-mutant.py
RESTORE_BYTES_IDENTICAL True
```

Mutant hashes (all single-point scratch edits):

| Mutant | SHA-256 | Detector verdict |
|---|---|---|
| M1 EOF-pending `res is None` ignored | `62a39dadb601114866b02d499a08fe89c90782fb33103927ecb5914769460e7e` | killed |
| M2 `?` restart/interruption ignored | `7e7891ff376e3680ebc8e314bfd477f72616debfbcf91f9a73b554491e11427e` | killed |
| M3 ACCESS EACCES condition negated | `4a687637c3a78114687aee25ba571ffd53707e45491dd475224e1c5ebe7a73a1` | killed |
| M4 OPEN errno set inverted | `71ad58d5b69bcdbdf617d139e3fe83fe71ed21c9786334edcee6cb288331b33a` | killed |
| M5 pending-at-EOF loop dropped | `d2eb00ef78b0ee8d335473a766f471b5207c649844ce387ca9b8bca83717a289` | killed |
| M6 `ctl` path exclusion dropped | `c37c195ec4f70aa883876438c5e256ab20ce6d02753ea151858caafdb870b21b` | killed |
| M7 resumed call ignored | `16badaa0e6dcafae087948578ccb9b35c0bf79a79fbc6713b90d6e572aec5cea` | killed |
| M8 dirfd annotation ignored | `e38df3159bdb0af68231ac3aa5d2bdd188709f4e22c5ae0de84f5f9f97f218b4` | killed |

Pristine and restored bytes both hash to `ef19380e862e0a6d21e2e7f7c47d72f578564202fb98aa4a2c554696e3d16508`; restored bytes are identical and the restored detector passes. The final run imports source bytes directly to avoid pyc cache reuse between equal-size mutations.

## Controls and limits

**No control false-pass verdict can be established in this seat:** stage-2 counter/control pins and receipts are absent, and I did not run scored controls. The frozen v3 control set is no-fence, base fence, round-45 keyed fence, admit-all, and refuse-all. Static reading of the inherited round-46 aggregation shows that `ERROR`/`ADMIT` contributes to refusal/sealed `LEAKED`, while hit accounting distinguishes `READ` from `clean`; the honest leg likewise uses traced hits. Thus suppressing blocked/pending hits is a plausible false-pass path for a fence that accesses outside `d` and then refuses (and for an admitted hostile case whose trace hit is suppressed), even though this bounded detector kills the eight tested accounting mutants. The named controls' actual v3 outputs, especially the keyed-fence control, remain unmeasured until stage 2; no absence-of-false-pass claim is made.

Limits: synthetic traces test the parser/accounting helper, not live strace formatting, the unreleased v3 counter, repaired fence, or stage-2 controls. No external sources were fetched; no tools were installed.

## Sources opened (accessed 2026-10-27)

- Local `plans/round-48-claims.md` at stage-1 revision `a543d920…`; URL: not applicable (lane file). Quote: “Claims/counters/controls are frozen before scored evaluation.”
- Local `corpus/lessons/round-46-verifier-spotcheck.md`; URL: not applicable (lane file). Quote: “C1's frozen kill rule is met: wave-2 reports count 3 admitted held-outs.”
- Local `plans/round46_c1_verify.py` at `a543d920…`; URL: not applicable (lane file). Quote: “never returned: the path was touched”.
- `skill://godspeed`; URL: not applicable (installed skill). Quote: “Iterate cheap, in parallel.”

**VERDICT:** mutation probe killed 8/8 accounting mutants; pristine/restored detector passed and scratch counter bytes were restored exactly. Control false-pass status is **inconclusive pending stage 2**; no scored run or C1/C2 admission claim.