# FxGateGeneric — gate timing / QUALITY Q13

Scope: generic wave-2 support, explicit-report control, unresolved-reference failure, and landing-tree timing. No production files changed. Scratch clone: `/tmp/kengaku-r26-FxGateGeneric`; integration revision `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`. `plans/gate_timing_check.py` at that commit has blob `9f7cdb9cb50a9ca00eeac8d7278cccce3c5d1bc7`, matching the reviewed lane file.

## Reproduction and observed outcomes

- `python3 /tmp/kengaku-r26-FxGateGeneric/plans/gate_timing_check.py --selftest` → exit **0**, `[selftest] ALL PASS`.
- `python3 /tmp/kengaku-r26-FxGateGeneric/plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9` → exit **1**; `FAIL line 29`, no cited report paths, generic `'wave-2 seats'`, 0 second-seat reports. Matches the specified Q10 red.
- Same command with `--commit f11bffbf` → exit **1**; line 29 fails generic support despite 87 second-seat reports in that tree. Matches the later-tip red.
- `python3 /tmp/kengaku-r26-FxGateGeneric/plans/gate_timing_check.py --lesson corpus/lessons/round-26.md --commit 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` → exit **1**, `no admit rows`; round-26 is explicitly deferred in `corpus/lessons/round-26.md:29-34`, so this is fail-closed, not a Q13 green admission.
- Setup controls: bad commit `deadbeef99` → exit **2** (`INPUT ERROR: cannot read...`); missing `--commit` → exit **2** (argparse usage error).

Scratch scenario driver: `python3 /tmp/fxgate_generic_driver.py` (exit 0 iff all expected codes match). It builds commits under `/tmp/kengaku-r26-FxGateGeneric`, and runs `plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-generic.md --commit REV --repo /tmp/kengaku-r26-FxGateGeneric`; fixture candidate uses intended target path `corpus/knowledge/grader-perturbation-audit.md`.

| Fixture commit / scenario | Exit | Decisive output |
|---|---:|---|
| `31786b279bf541dc19a650279b5ff063618e4a58` explicit good report in same commit | 0 | `PASS ... passed=1 failed=0` |
| `d1d80f885e9c36b0e93c7f5b770185310be61a1a` explicit good report + generic “wave-2 seats” | 1 | generic reference is not report evidence |
| `e8b259d53ef9c073b1c38c8cda2cdc662366cf40` generic-only “wave-2 seats” | 1 | no valid report path; generic support rejected |
| `588341a9a86d6a84a26711f4a3212e424b9ebf9f` explicit good report + unresolved `LateSeat.md` | 1 | unresolved bare report reference |
| `6df3ad68312008972a803cedc7c33991a351f9c7` cited report absent at landing | 1 | `absent from commit tree` |
| same `6df3ad...` with report added only to working tree | 1 | still `absent from commit tree` |
| `7bfdbc6d995283ffa64fb0592c5563ecf076c068` subsequent commit includes report | 0 | `PASS ... passed=1 failed=0` |

## Finding

**MEDIUM — role check accepts an untyped seat as Q13 reviewer-like support.** `load_members` converts a missing/non-string `role` to `""` (`plans/gate_timing_check.py:288-292`); `audit_admission` rejects only `scribe` and `executor` (`:326-329`). In the scratch commit `fb9b444a5fbf65e16210a4e755ffa985324cee88`, `FxEmptyProbe` was a registry member object with no `role`; its nonempty report named the candidate and had an anchored `VERDICT:`. The exact Q13 command returned **0**, `PASS ... passed=1 failed=0`. This does not establish a reviewer-like seat. Require a recognized reviewer-like role or fail closed on missing/unknown role. The same fixture driver shows a registered `scout` role also passes (`e7d62529702dcb9bd4137be2fcb57ef2e8bc1de5`); no claim is made here about whether every non-reviewer role is disallowed.

The assigned generic-reference attacks otherwise behave as documented: explicit good report alone passes; adding a generic wave-2 reference or using generic-only support fails; unresolved report names fail; and late reports/working-tree-only files cannot satisfy the earlier commit. The structural support bar is documented in `plans/round-26-claims.md:20-26,206-209`; report checks are in `plans/gate_timing_check.py:316-352`.

Verification gap: the real round-26 Gate is still deferred at the integration revision, so no real admitted candidate run could be shown green. No LSP route was exposed in the available tool inventory; no LSP status/references/definition/diagnostics were obtained. No tools installed.

VERDICT: Q13 generic-reference and commit-tree timing checks pass the assigned red/green probes; role validation has the concrete fail-open finding above.