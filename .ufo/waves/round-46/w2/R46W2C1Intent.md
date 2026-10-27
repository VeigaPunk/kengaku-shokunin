# R46W2C1Intent — source review

**Axes:** calibration (claimed refusal boundary vs actual fence); counter integrity (module-specific recognition vs property testing).

Reviewed at lane TIP `42d5043afac952fcb43bf4798757785dd258cf85` (scratch clone HEAD matched the required revision).

## Finding — medium: mount points defeat the stated containment proof

`plans/fixture_fence.py:19-29` says the fixture walk proves the tree contains no symlink or special file and that the store allowlist proves paths stay under `d`. But `_tree` checks entries with `lstat` and rejects symlinks/special files only (`:183-220`); it never checks device/mount identity or otherwise rejects mounted directories. A bind-mounted directory below `d` is an ordinary directory to these checks. `_store` then follows it during `scandir`/`open` (`:453-525`, via `_entries`/`_read` at `:100-130`) and can inspect a mounted `.git` store whose backing content is outside `d`; lexical containment is not backing-store containment. Thus it does not refuse every fixture whose discovered store cannot be proven inside `d`, contrary to the docstring's whole-tree/allowlist proof (`:1-3`, `:22-29`) and SCORECARD advertisement (`SCORECARD.md:2065`). This is a source-level counterexample; I did not attempt a privileged mount test.

The fence does substantially invert the prior named-escape strategy: it uses an allowlist for `.git` entries and config keys (`fixture_fence.py:64-78,226-275,453-525`) rather than branches for CR/BOM/includeIf/alternates/etc. (`:12-16`). However, the structural proof does not include mount boundaries, so its “provably” claim is broader than the implemented check.

## Module-keying check

I found no fence branch keyed to a refusal/sealed module name: the fence receives only `d`, argv and tool (`:531-575`), and classifies filesystem properties. The verifier does pin specific module paths/digests and exact corpus totals (`round46_c1_verify.py:123-189,464-471,613-620`); those are frozen test-input integrity/non-vacuity checks, not decisions based on a module's identity or expected verdict. Its rollup evaluates each built module's observed admission/touches (`:564-585`).

## Verification limits

No counter, fixture, or probe was run. No report-subdirectory receipt was needed; clone identity is recorded above. The mount-point issue is based on source inspection, not an observed counter run.

VERDICT: fence-intent-defects-1
