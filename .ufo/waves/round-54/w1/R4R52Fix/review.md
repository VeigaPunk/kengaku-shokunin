# R4R52Fix review

**Recommendation: DO-NOT-INTEGRATE.** Axes: novelty and calibration; no score/admission asserted.

## Findings (severity order)

### P1 — Existing green row becomes a false red (required no-harm check fails)

`E3R52RegistryFix/round52_c2_registry.py:74-83` still associates every surviving flag in the cell with its sole mentioned script. Removing the blanket negation exemption exposes the existing `SKILL.md:590` `order-check` cell: it explicitly disclaims `--selftest`, references external falsifier `plans/round40_c1_verify.py`, then documents `--receipt` and `--claims` controls of **order_check.py**, not flags of the external falsifier. The patch treats those as unsupported flags of round40_c1_verify.py. Actual definitions: `plans/order_check.py:143-145` accepts both; `plans/round40_c1_verify.py:443-450` declares its different options.

Independent run from scratch: old counter exits 0 with `SELFTEST-UNBACKED 0`, `PREDICATE R52-C2 pass`; patched exits 1 with `SELFTEST-UNBACKED 1`, `SELFTEST-UNBACKED \`order-check\``, `PREDICATE R52-C2 fail`. Comparing every parsed row's selftest predicate isolates exactly this changed row. These outputs also agree with the executor's old-lane.txt / patched-lane.txt: the supplied receipts themselves already show no-harm failing. Preserve this legitimate external-falsifier declaration while fixing the unrelated-flag masking; do not change frozen SKILL.md to accommodate the parser.

### P2 — New K7 selftest does not test the verdict invariant it claims

`E3R52RegistryFix/round52_c2_registry.py:199-206` replaces the registry with only a ghost row but retains advertised grader.py/tool_a.py. Thus `MISSING 2` independently forces a failing verdict. A scratch, in-memory mutation removing only `entry_missing` from the verdict's `ok` expression still returns `SELFTEST cases=6 failures=0`, exit 0, including `SELFTEST ok K7-entry-missing`. This is the precise mutation identified in controls.json, yet the new selftest does not kill it. Keep all existing advertised rows in the K7 fixture (or remove unrelated advertisements) so ENTRY-MISSING is the only failing leg. The separate fixture-k7.md describes insertion into a complete table, which avoids this confounding condition, but the implemented selftest does not follow it.

## Requested checks

- **(a) Scope:** independent difflib comparison has exactly two hunks: selftest_unbacked's docstring/negation handling and three appended selftest cases plus count 3→6. No other code moved. Full independent delta saved as `independent-delta.diff`. The added IGNORECASE also expands negation recognition; it is part of that one parsing hunk.
- **(b) Red before/after:** executor directory had no standalone mixed-negation before/after receipt at inspection. Independently built one scratch fixture with a real `plans/tool_a.py` containing no accepted flags and one complete registry row whose self-test cell is `no --selftest; python3 plans/tool_a.py --check`. Same fixture: old exits 0 / unbacked=0 / pass; patched exits 1 / unbacked=1 / fail. The targeted masking defect is genuinely caught.
- **(c) Coverage:** original three cases remain byte-identical: clean-fixture, missing-fixture, incomplete-fixture. Independent old run: cases=3 failures=0; patched run: cases=6 failures=0. Added cases: span-scoped-negation-fixture, K5-decoy-table, K7-entry-missing. K5 checks that a later heading's decoy stays outside registry_block. K7's verdict coverage is invalid for the reason above. The stale selftest docstring still says three fixtures (minor documentation debt, not an additional blocker).
- **(d) No harm:** FAIL. Neither counter implements `--dry` (main parser only has --lane and --selftest); exact requested `--dry --lane ...` calls both exit 2 with unrecognized-argument errors, not successful equivalent verdicts. The supported default read-only `--lane ...` invocation gives the differing verdicts above. Do not count matching usage failures as a no-harm pass.

## Evidence commands and receipts

All subprocesses used cwd `/fast/scratch/hyaku/kengaku-r54/R4R52Fix`, TMPDIR there, and PYTHONDONTWRITEBYTECODE=1. Let L=/home/vgpnk/Projects/shokunin/kengaku-shokunin; O=$L/plans/round52_c2_registry.py; P=$L/.ufo/waves/round-54/w1/E3R52RegistryFix/round52_c2_registry.py.

```sh
python3 "$O" --lane "$L" --selftest
python3 "$P" --lane "$L" --selftest
python3 "$O" --dry --lane "$L"
python3 "$P" --dry --lane "$L"
python3 "$O" --lane "$L"
python3 "$P" --lane "$L"
python3 "$O" --lane /fast/scratch/hyaku/kengaku-r54/R4R52Fix/negation
python3 "$P" --lane /fast/scratch/hyaku/kengaku-r54/R4R52Fix/negation
```

Fixture SKILL.md: `## Gate/probe registry` followed by `| \`t\` | gate | \`python3 plans/tool_a.py\` | 0 ok | no --selftest; python3 plans/tool_a.py --check | none | read-only | kengaku |`. tool_a.py: `# no accepted flags`.

K7 probe executed the patched source via `exec(compile(...))` after this single in-memory replacement, then called `selftest(lane)` with redirected stdout:

```python
text.replace('ok = not (missing or incomplete or entry_missing or unbacked or duplicate)',
             'ok = not (missing or incomplete or unbacked or duplicate)')
```

`evidence.json` records complete argv, exits, stdout/stderr, row-level differences, mutant output and source SHA256s. No production edits, git mutations, integrations, or alternate agent runtime. Scratch removed in finally; no tool installed. Disk guard reported scratch free 367.9G (55% used); its later top-consumer scan timed out at 30 seconds, without ENOSPC.

## Residual risk / verification gaps

`read xd://lsp` returned `No such tool`; no LSP device/server was available for status/references/definition/diagnostics. Literal grep and direct source inspection are fallback evidence, not semantic proof. Frozen r53/r54 ledger consumers invoke the supported entry command, so integrating this counter would change its observed exit unless separately reconciled by the L1; no broad entrytruth rerun was performed. No claims about saturation, external anchors or resume continuity follow from this scoped parser review.

## Self-evaluation

Accuracy 4/5: direct runs and source anchors support both findings; no semantic server available. Completeness 4/5: all four requested checks covered; broad downstream entrytruth execution is outside this review. Clarity 4/5: explicit blockers and commands; fixture setup is described rather than retained as an executable driver. Actionability 5/5: fixes target the false-red association and isolated K7 failure. Conciseness 4/5: detailed evidence retained for reproducibility. Overall 4.2/5. Highest-impact improvement is to correct those two defects and repeat the same bounded checks. User agreement: expected, since no-harm is explicitly required and demonstrably fails.
