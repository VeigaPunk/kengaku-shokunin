# FxP3ECorrections — state_check.py v3

Scope: integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`, exported with base `f11bffbf9caa9c9e286fb32c568b81b97719656a` to `/tmp/kengaku-r26-fxp3ec-{integration,base}`; all mutations were in `/tmp` only.
Axes exercised: P3 false-positive resistance; correction-lineage integrity; P2 frozen-population stability; integrated C2 result.

## Findings (severity ordered)

- **HIGH — A misplaced or semantically contradictory correction can falsely supersede a stale assertion.** `plans/state_check.py:456-468` scans the entire document and retains the last matching line; it does not enforce append position. `:1153-1161` accepts equality of extracted code spans without validating the correction prose. On a base-derived scratch tree with the registered P3a 14→17 mutation, an R26-E1 inserted at `SCORECARD.md:2` yielded `P3a.capability.interval-reverdict.selftest-checks=SUPERSEDED` (`correction_line=2`). A second scratch row at line 731 literally said “now 17 checks” but placed the derived tokens `18 checks` and `0 failed` in unrelated text; it too yielded `SUPERSEDED`. These are false closures of a stale claim, not merely missing coverage.
- **MEDIUM — Duplicate correction IDs/rows are silently accepted.** Two identical `R26-E1` rows for the same P3a assertion at scratch `SCORECARD.md:731-732` produced `SUPERSEDED` from line 732. A duplicate pair whose last row said “now 17 checks” but carried the unrelated `18 checks`/`0 failed` spans also produced `SUPERSEDED`. The last-match behavior (`:463-467`) neither detects duplicate IDs nor rejects conflicting duplicate rows.
- **MEDIUM — The recorded integration does not meet its registered C2 result.** `python3 plans/state_check.py --summary` at the exported integration returned `assertions=275 match=267 mismatch=2 superseded=3 offline_unverifiable=3`, exit **1**. The mismatches are `P3b.province.public-literature-registry.rows` and `P3b.province.round25-correction.rows`: `state_check.py:1353-1358,1366-1371` requires `rows=42` plus `id_set=exact`, while `PROVINCE.md:180-185`'s R26-E3a/b/E7/E8 rows carry only `rows=42`. The checker correctly refuses these partial restatements; the integration claim in `round-26-claims.md:143-147` predicts mismatch=0.

## Targeted checks

Every case used `python3 /tmp/kengaku-r26-fxp3ec-integration/plans/state_check.py --json --root /tmp/kengaku-r26-fxp3ec-case-<case> > /tmp/kengaku-r26-fxp3ec-<case>.json`; each checker process exited **1** because the base-derived tree retains other registered P3 mismatches. `jq` selected the named assertion:

- `partial` (`supersede-partial.patch`): `P3a.capability.interval-reverdict.selftest-checks=MISMATCH`, tokens `['18 checks']`; exit 1.
- `full` (P3a mutation + `supersede-full-control.patch`): same assertion `SUPERSEDED`, tokens `['18 checks','0 failed']`; exit 1.
- `frozen` (`supersede-frozen-restatement.patch`): `P3e.row-to-file.lessons/round-25.md=MISMATCH`, `P3c.box.4.pointer.1=MISMATCH`; exit 1. The paired `rederived` fixture made both `SUPERSEDED`; exit 1.
- `arbitrary`: P3a assertion `SUPERSEDED`, `correction_line=2`; exit 1.
- `prose`, `duplicate`, `duplicate-false`: P3a assertion `SUPERSEDED`, respectively at lines 731, 732, 732; exit 1.
- `citation`: P3a assertion `MISMATCH`, tokens include the extra `corpus/evidence/round25-calibration/attrib-calibration-selftest-v2.txt` span; exit 1.
- `python3 plans/state_check.py --selftest` in the integration export printed `[selftest] ALL PASS`, exit **0**; it misses the misplaced, prose-contradiction, and duplicate-row attacks above.

## Preservation and verification gaps

- P2 preservation check: v2 `python3 plans/state_check.py --json` on the base exited **0**; v3 `--root /tmp/kengaku-r26-fxp3ec-base --json` exited **1** on P3. `jq` full-object comparison of non-P3 assertion records: `p2_v2_count=247`, `p2_v3_count=247`, `p2_objects_identical=true`, no P2 mismatches; sole P2 supersession remains `P2a.capability.sources-registry`.
- LSP was unavailable: `write xd://lsp` returned “No such tool”; therefore no LSP status/references/definition/diagnostics were possible. Source review used selected `read` ranges; no grep was used as semantic proof. No tool was installed.
- Residual risk: this seat tested state_check P3 supersession only; it did not assess C1 families, Q13, source quotes, or the draft entry.

VERDICT: FALSIFY — v3 has reproducible false-positive P3 supersession paths, and the recorded integration still has two P3b mismatches; do not rely on its supersession safety or C2 PASS claim.
