# ClaimFalsifier — r64 w1 seat report (attack seat)

Full per-attack ledger: `.ufo/waves/round-64/w1/ClaimFalsifier/falsify.md`. Receipts in the
same dir: `c1-forged-receipts.txt`, `c2-attacks.txt`, `c2-attacks-landed.txt`,
`c2-predicate-legs.txt`, `c2-predicate-legs-landed.txt`, `c3-attacks.txt`,
`c3-attacks-landed.txt`. No lane file edited; no server started; no port bound; no git/jj
mutation; no tool installs (none needed).

## Verdicts

- **R64-C1 (coverage): SURVIVES.**
  - (a) Independent re-derivation of all 7 legs from the grader source (sha recomputed
    `115de2e9…`, matches the freeze): my 5×7 table equals the frozen vectors cell-for-cell.
    The one conditional cell (K3 leg-6) resolves in the frozen vector's favor — the live
    receipt's K3 fragments (`SetVal returned wrong value: 43`) prove the fixture returns the
    stored +1 value. Committed controls cross-checked: K4 proto carries all five leg-1
    strings; K2/K4 captures match my derivation (leg-5 fragment exact; ModuleNotFoundError
    not swallowed by the leg-6 RpcError catch).
  - (b) Seven forged receipts vs `--check-receipt` (landed probe
    `plans/round64_c1_kvstore_probe.py`, sha `9f56d25d…`): empty file, missing fragment
    clause, vectors-without-port-lines, fragment-not-on-leg-5, flipped vector cell, wrong
    grader sha, stripped K1 PID — **all rc 1 with named findings**; only the unmodified
    receipt passes rc 0. Leg-level fragment binding held (f4).
- **R64-C2 (operability): SURVIVES.** Attacked both the GateScopePatch clone and the LANDED
  gate (`plans/round63_gate_checks.py`, sha `a98d9c0f…`): `..` token (counted shape) fails
  with `DETAIL escape=`; absolute-inside-root token fails patched rc 1 where base passes
  rc 0 (sharpest discriminator); directory-in-root and URL-in-prose do not regress; the
  committed escape fixture now fails rc 1; landed selftest 4/4 rc 0; real SKILL section
  unchanged (24/24 resolved, rc 0). Assigned example `a/../../etc/hostname` is syntactically
  not a path token (no counted suffix) — fails via the generic no-path-token rule, not the
  escape class; recorded as a scope nuance, not a defect.
- **R64-C3 (freshness): SURVIVES.** Attacked both the SweepBuild clone sweep (sha
  `56638ea1…`) and the LANDED sweep (`plans/round64_trio_sweep.py`, sha `b559b87c…`) on
  exact freeze-commit bytes (`git archive 859ac24f…`; frozen list sha `fe0498fb…`): wrong
  date (2026-11-02) stays RED; missing `recheck:` stays RED; frozen entry removed from disk
  → **SETUP frozen-list-mismatch rc 2** (not red, not pass); red=0 path with an absent
  frozen entry → **SETUP frozen-entry-missing rc 2** — a deletion can never be the repair.
  Fully-shaped forgery with a fabricated `result:` line leaves the red set but trips the
  cross-check (SETUP rc 2) while any base red remains.
- Method note: one intermediate landed-sweep run was contaminated because the live lane
  corpus gained real repair addenda while I restored victims from it; that run is superseded
  by the freeze-commit-bytes run (recorded in falsify.md for provenance).

## Sharpest finding

The C2 repair's escape class is **lexical only**: a receipt-pointer token that leaves the
root through an in-root symlink (`link/secret.md` → outside dir) resolves and the LANDED
gate passes rc 0 (T5, `c2-attacks-landed.txt`). The frozen repair's letter ("relative, no
`..`, normpath inside root") is satisfied, so this is a scope bound for a future routed
defect, not a kill: consumers that treat `resolved` as root-confined should `Path.resolve()`
physically or refuse symlinked components. Secondary residuals: suffix-less `..` tokens are
invisible to path accounting (fail via no-path-token instead of escape); the sweep prices a
`result:` line's presence, not its truth — final guard is the closure re-running named
commands (frozen kill rule).
