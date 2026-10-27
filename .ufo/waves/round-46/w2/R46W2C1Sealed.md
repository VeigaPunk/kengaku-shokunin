# R46W2C1Sealed — sealed46 integrity audit

## Findings (severity order)

### [P2] Two sealed modules duplicate refusals46 classes

- `plans/sealed46/s_objects_link.py:17-20` moves `.git/objects` outside `d` and symlinks it back. This is the same object-store-symlink-out class as `plans/refusals46/f15_objects_symlink_out.py:26-29`; only the outside directory name and move helper differ (`shutil.move` vs `os.rename`). The two base-fence runs independently report this class admitted/leaked (seal-store report lines 5, 9; base control line 185). Thus one of the 12 sealed slots repeats a refusal class.
- `plans/sealed46/c_core_attributes_path.py:9-19` writes `[core] attributesFile = <outside>`, the same key and outside-attributes-file behavior as `plans/refusals46/f20_attributes_file.py:14-23`. The sealed filename/fixture label says “attributes-path,” but the actual key is `attributesFile`. Both are admitted by the base fence (Config seal report lines 7, 11; base control line 204).

### [P2] Two sealed modules duplicate each other

`plans/sealed46/p_refs_redirect.py:18-21` and `plans/sealed46/s_refs_link.py:17-20` both move `.git/refs` outside the fixture and replace it with a symlink to that directory, for the same `order` tool. `os.rename` vs `shutil.move` and the destination directory names do not change the attack class. Both are counted as separate sealed modules (base control lines 197-198). This is one repeated class within the 12-module set.

**Count:** 3 duplicate-class relationships (2 cross-set, 1 within-set), affecting 4 sealed modules. I use relationship count for `k`.

## Checks that survived

- **Stage-2 pin:** `plans/round46_c1_verify.py:177-188` pins exactly the 12 `plans/sealed46/*.py` modules; the counter’s `PINS` set has 65 entries and `SEALED_FLOOR = 12` (`:73-75, :190-191`). I independently SHA-256-compared every landed module with its pin and the wave-1 retained artifact digests; all 12 matched. The C1 counter run at the assigned TIP printed `PINS total=65 mismatched=0` and `SEALED total=12 clean=12 leaked=0 read=0 hung=0 build_errors=0`, then `PREDICATE C1 pass` (receipt: `R46W2C1Sealed/audit-receipts.txt`).
- **Base-fence verdicts:** all 12 modules have base-fence `LEAKED` receipts. The four seal-seat reports list all 3 outcomes each: Config (`R46CritC1SealConfig.md:5-11`), Paths (`R46CritC1SealPaths.md:15-20,26-28`), Argv (`R46CritC1SealArgv.md:5-13`), Store (`R46CritC1SealStore.md:5-9`). The stage-2 base-fence control independently shows each sealed row `LEAKED` and `SEALED total=12 clean=0 leaked=12 read=0 hung=0` (`claims/control-c1-base-fence.txt:195-207`; measured with base fence digest `ac65c032…`).
- **Fence-seat access:** FenceA/B/C reports cite their own work and round-45 surfaces, and each says it did not read other wave-1 dirs (`R46ExecC1FenceA.md:7-8`, `FenceB.md:37-39`, `FenceC.md:8-9`). FenceC also states `plans/sealed46/` did not exist yet (`FenceC.md:292-295`). Their measured runs in the reports ended around 02:05–02:10; stage-2 added `plans/sealed46/` at commit `cf7de6a` (02:30:51). No fence-seat report cites a sealed module path. This supports no access during measurement. **Residual limit:** the fence reports were committed at 02:38:43, after stage-2; the available evidence is the seats’ explicit no-read statements and cited-path review, not an OS-level audit proving no later read while reports were being finalized.

## Residual risk and verification gaps

The duplicates reduce the number of distinct sealed attack classes represented by 12 modules. They do not invalidate the observed C1 counter result: the current fence refuses all 12 at the assigned TIP, and the base fence admitted all 12. I found no pin mismatch or missing per-module base-fence verdict. The remaining access uncertainty is limited to possible post-measurement reads during report drafting, as noted above.

VERDICT: sealed-modules-12-integrity-defects-3