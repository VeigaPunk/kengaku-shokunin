# R48C2TagInv — frozen-tag violation coverage

Axes: coverage (assigned); calibration/depth/other axes not evaluated.

REV measured: `a543d92083557dd9b33ee674e9b99b03411f80af` (stage-1 freeze). Confirmed committed lane HEAD was `bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`; stage-1 commit exists and is dated 2026-10-27 06:53:29 -0300. This review inspects the committed round-46 frozen table and executed receipt only; no scored counter/probe execution was run. The receipt is prior round-46 evidence, not a round-48 measurement. No stage-2 C2 freeze was verified, and this review makes no R48-C2 admission claim.

## Frozen tags → executable violating cases

Source: `corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` lines 1–7 names all seven frozen tags. Its CASE rows are committed cases; cross-check against executed receipt lines 9–28, where `observed=fail` means the probe case actually fails the grader and `observed=pass` exposes a grader blind spot.

| Frozen tag | Receipt case(s) with `violates=` | Executable evidence / result |
|---|---|---|
| `single-file` | `nop`; `extra-file`; `leftover-cmain`; `regrade-same-state` | Receipt lines 9, 14–15, 22. `nop`, `extra-file`, `leftover-cmain` observed fail; `regrade-same-state` observed pass and differs on regrade (`regrade=DIFF:F`), demonstrating grader non-idempotence rather than an initial-run failure. |
| `python-run` | `c-only` | Line 13: observed fail, `CalledProcessError` from Python syntax failure. |
| `c-build` | `python-only`; `dir-in-place` | Lines 12, 24: both observed fail with `CalledProcessError`. |
| `both-print` | **NONE** | No committed case has `violates=both-print`; V7 defect. |
| `fib-kth` | `lookup-table`; `wrong-value`; `n-parsed-differently`; `empty-file` | Lines 11, 16, 20, 23. All are executable cases. `wrong-value`, `n-parsed-differently`, `empty-file` observed fail; `lookup-table` observed pass, proving the grader accepts a lookup-table violation of the intended computation requirement. |
| `stdout-only` | `value-plus-line` | Line 26: observed fail. |
| `toolchain` | **NONE** | No committed case has `violates=toolchain`; V7 defect. |

The case table itself ends `cases=18 predicted_pass=7 predicted_fail=11`; executed receipt ends `cases=18 observed_pass=7 observed_fail=11 mismatches=0`. The specific uncovered tags are the exact V7 defect class identified in the frozen claim and round-46 spotcheck. The existing table/receipt therefore fail the requested all-tag coverage criterion: 5/7 tags have at least one executable violating case; `both-print` and `toolchain` do not. Note that `lookup-table` is still a valid violation case despite observed pass: it exercises the requirement defect by demonstrating an undetected violation, not successful detection.

## Commands and evidence

Exact shell command used to check the frozen revision:

`D=/home/vgpnk/Projects/shokunin/kengaku-shokunin; git -C "$D" log --oneline -5; echo "---tip---"; git -C "$D" rev-parse HEAD; echo "---stage1 commit check---"; git -C "$D" cat-file -t a543d92083557dd9b33ee674e9b99b03411f80af && git -C "$D" log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af`

Observed output (relevant lines):

`bf783c1 round-48: w1 ready handoff marker`
`453ddfd round-48: w1 v2 dispatch evidence (64 seats, 41 attack, policy v2 accepted)`
`a543d92 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`
`bf783c1ee4dc61a5e4fa1b12a87c6d547eba2767`
`commit`
`a543d92083557dd9b33ee674e9b99b03411f80af 2026-10-27 06:53:29 -0300 round-48: stage-1 freeze of C1 (fence over-refusal, v3 counter) and C2 (TB2 grader admission, Q40 counter) claims`

Read-only file commands used: `read` on the frozen claims, round-46 verifier spotcheck, frozen dry-case table, executed probe receipt, and committed probe implementation. No probe, counter, build, or scored evaluation command was run. Reviewer LSP status/references/definition/diagnostics were unavailable in the provided tool inventory; findings are based on direct committed artifact contents, not semantic grep claims. Scratch directory `/fast/scratch/hyaku/kengaku-r48/R48C2TagInv` was created and contains no fixture clone or evidence; it must be cleaned before yield.

## Source captures (accessed 2026-10-27)

- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round-48-claims.md` — “every frozen requirement tag is cited by at least one committed case `violates=` line” (C2 V7 delta).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/lessons/round-46-verifier-spotcheck.md` — “V7 lacks violating cases for `both-print` and `toolchain`” (C3 coverage re-check).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round46/polyglot-c-py-dry-cases-freeze.txt` — “TAG both-print instruction.md:7” (frozen tag table).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round46/polyglot-c-py-probe.txt` — “cases=18 observed_pass=7 observed_fail=11 mismatches=0” (executed result).
- `file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/polyglot_c_py_probe.py` — “Round-46 C3 probe: the pinned Terminal-Bench 2.0 `polyglot-c-py` grader, executed offline.”

VERDICT: **FAIL — frozen-tag violation coverage incomplete.** `both-print` and `toolchain` lack any committed executable violating receipt case, so the exact V7 defect remains. Stage 2 must establish per frozen tag a committed violating case before claimed work is scored; this seat did not author or change that freeze.

Limits: no stage-2 artifacts were examined; no full C2 counter/probe run; no claim about later case-table amendments or round-48 admission. Cleanup is pending.
