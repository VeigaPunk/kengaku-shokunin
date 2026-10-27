# R48-C2 no-package control review

Axes named: **coverage** (R48-C2). This is a design-time critic review only; I did not measure or admit C2.

## Verdict

**VERDICT: NOT YET EXECUTABLE / CONTROL SPECIFICATION NEEDS A PINNED TREE RECIPE.** The stage-1 freeze is committed and predates this review, but the v4 counter is absent at the measured revision, so the frozen C2 predicate cannot be scored yet. I made no counter or probe execution. The no-package control is structurally capable of failing if stage 2 runs the v4 counter on a stage-2-derived tree with the probe removed and records the V5/V15 defects; that outcome is not observed evidence. The phrase “base tree (no `plans/polyglot_c_py_probe.py`)” must not be implemented by simply using the historical baseline tip: that tip already has the probe.

## Evidence

- Freeze commit: `a543d92083557dd9b33ee674e9b99b03411f80af`, commit time `2026-10-27T06:53:29-03:00`; its tree contains `plans/round-48-claims.md` blob `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`. The same blob is at master. The clean scratch clone's `REV` was `a543d92083557dd9b33ee674e9b99b03411f80af`. Thus the freeze predates this review. **Measured revision (REV): `a543d92083557dd9b33ee674e9b99b03411f80af`.**
- At that revision, `plans/round48_c2_verify.py` is absent (`git cat-file -e HEAD:plans/round48_c2_verify.py` → `fatal: path ... does not exist in 'HEAD'`). The frozen predicate therefore cannot be run yet.
- The no-package identity is ambiguous if “base tree” means a historical commit. `plans/polyglot_c_py_probe.py` entered at `cf7de6a`; it is present both at the claims' baseline `0f77f9b27931b3c76b3d095fc0fa70edb79556d9` and at the stage-1 freeze. No historical baseline implied by the claims is the stated no-probe state. The stage-1 tree has these C2 inputs: probe, `plans/pkg-spec-r46.json`, `plans/pkg_gate.py`, `plans/round46_c3_verify.py`, `plans/order_check.py`, frozen dry table, receipt and entry.
- Freeze-tree SHA-256: committed probe `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; dry table `99adfea6bd404b469a58a7fe8a6f44a3cc0a5b035fc589d1f5a4e58cb9489536`. The inherited r46 counter pins the probe at `67a8f4a6…` and defines V5 as checking both probe digest and dry-output equality. The claims' surface description instead says the wave artifact with digest `22b7779e…` was integrated verbatim. `sha256sum` confirms that wave artifact is `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`, but it is not byte-identical to the committed probe (diff shows different sandbox/process and grading implementation). This is a package-identity/provenance discrepancy relevant to what the control removes; stage 2 must pin the actual committed input identity and document the discrepancy, not silently substitute the artifact.
- Static evidence that the intended failure is implementable: the frozen r46 counter's `run_legs` catches a check exception as “a check that cannot run is a defect, never a pass”; its `main` prints `PREDICATE C3 fail` on leg defects. V5 rejects a missing or mismatched probe. R48's V15 explicitly requires a missing/tamper-pinned input to become that leg's DEFECT rather than crash. This supports reachability, not a result from the unwritten v4 counter.
- Round-46 precedent (`.ufo/waves/round-46/claims/control-c3-base.txt`, committed): “control control-c3-base: stage-2 tree, no package”; the receipt records V1–V13, `checks=13 defects=8`, `PREDICATE C3 fail`, exit 1. The report's control was a transformed stage-2 tree, not merely an unqualified historical base commit. Its exact receipt also shows per-leg findings, which is the right evidence style for R48.

## Counterexample / smallest safe correction

The strongest counterexample to treating “base tree” as a literal historical base is `0f77f9b`: it already contains the probe (`cf7de6a` introduced it), and so cannot test absence. Running v4 against that tree would not establish the no-package control; it could fail for unrelated pre-amendment/pin defects and falsely appear to reach the target. The smallest safe correction is to have stage 2 pin a reproducible control construction: start from the same stage-2 counter/input tree used for the other controls, remove only `plans/polyglot_c_py_probe.py` (unless the frozen control is explicitly meant to remove more), record the resulting tree REV, and capture per-leg output showing the missing-probe V5/V15 defect and the exact `PREDICATE R48-C2 fail` line. A crash or failure only on unrelated legs is not a successful control receipt.

## Commands run

1. `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log --oneline -8 master` and `git -C ... log -1 --format='%H %cI %s' a543d92083557dd9b33ee674e9b99b03411f80af`.
2. `git -C ... ls-tree -r --name-only a543d92083557dd9b33ee674e9b99b03411f80af` with round48/polyglot filters; `git -C ... ls-tree` for the claims, base and C2 files; `git -C ... log --oneline -- plans/polyglot_c_py_probe.py`.
3. `mkdir -p /fast/scratch/hyaku/kengaku-r48/R48C2CritDoNothing`; `git clone --shared --no-checkout ... /fast/scratch/hyaku/kengaku-r48/R48C2CritDoNothing/lane`; checkout `a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse --show-toplevel`, `git rev-parse HEAD`; `git cat-file -e` for the frozen counter and input paths; `git show` + `sha256sum` for probe and dry table.
4. `sha256sum` for committed probe and round-46 wave-artifact probe; `diff` between those two files.
5. Read-only inspection of `plans/round46_c3_verify.py` (V5 pin and V5 code, `run_legs` exception path, `main` verdict path), plus `git show` of `.ufo/waves/round-46/claims/control-c3-base.txt` and round-46 C3 landing evidence; inventory of frozen dry table, receipt and spec.
6. `mkdir -p` report directory and `rm -rf /fast/scratch/hyaku/kengaku-r48/R48C2CritDoNothing` after copying evidence into this report. No tool was installed or updated.

## Limits

No v4 counter exists at REV, so no R48 predicate result or exact R48 control receipt exists. I did not run the round-46 verifier, `--dry`, a full probe, or any scored execution. The frozen claims and the round-46 spot-check document were read first. No external sources were opened (no URL/access-date/quote applicable). Scratch tree was removed before report completion.
