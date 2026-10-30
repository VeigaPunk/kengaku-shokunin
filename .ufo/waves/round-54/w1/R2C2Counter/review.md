# R2C2Counter — Claim 2 correctness review

Axes: calibration (primary), correctness and no-harm. Recommendation only, not admission or scoring. Frozen claims read in full before review. Reviewed all 866 added lines in the three target files against base `6c919180260ea545589c2c0a007a06f554b529d3` and Claim 2.

## Findings, by severity

### BLOCKER B1 — argparse abbreviations preserve selected-argv laundering

`plans/round54_c2_entrytruth.py:146-159` rejects only exact forbidden tokens. `--selft` is accepted, while Python argparse's default abbreviation resolves it to `--selftest`. The counter verifies script identity, not the registry's complete entry invocation (`85-89`, `228-231`).

Executed unchanged counter against a one-row committed scratch fixture: registry command `python3 plans/gate.py` exits **1**, but ledger command `python3 plans/gate.py --selft`, declared green, produces **PREDICATE R54-C2 pass**, exit **0**, with `laundered=0`. `chosen="bare"` does not prevent this: the counter never validates that metadata.

Evidence: `laundering-probes.txt`, case `abbreviated-selftest`. This satisfies the frozen kill condition at claims lines 176-178: a passing ledger row disagrees with the true registry entry. Recommendation: do not claim closure under the frozen predicate; route any instrument change through L1's amendment process, not an edit to frozen inputs.

### BLOCKER B2 — uv branch accepts a decoy script in arguments and executes unrelated Python code

`plans/round54_c2_entrytruth.py:160-164` accepts any adjacent `python3`, matching-script pair anywhere in a uv argv. It never establishes which interpreter/script uv actually executes. The shell-token check at `150-151` rejects exact `-c`, but not Python's valid combined `-cPROGRAM` form.

Executed argv:

```text
["uv", "run", "--no-project", "--offline", "python3", "-cprint('wrapper green')", "python3", "plans/gate.py"]
```

`entry_mode_ok` returned `None`; the unchanged full counter returned **PREDICATE R54-C2 pass**, exit **0**. The actual registry entry independently returned **1**. Python executes the inline print and treats the trailing interpreter/script tokens as arguments; the gate never runs.

Evidence: `laundering-probes.txt`, case `uv-decoy-script`. Existing uv version: `0.13.0`; no install/update. This is an independent surviving laundering route and frozen kill-rule trigger. Recommendation: canonical invocation parsing would need to bind the executed program, not search the argument list.

### MAJOR M1 — ENV is not a predicate leg, and its external positive control can pass with no hermeticity

Claims lines 152-155 require an internal control, identical observed exits under clean/poisoned counter environments, and a distinguishing inherited-env negative. `evaluate` at `255-361` never executes an ENV control and its final predicate at `358-359` has no ENV term. Only `--selftest` exercises a separate output-based check (`451-470`).

The standalone control is also nondiscriminating: `plans/round54_c2_controls.py:160-168` places poison only in a local `env` dictionary for the negative subprocess. It does not poison `os.environ` before calling `hermetic_env(tmp)`. Thus the supposed hermetic positive starts from the ordinary caller environment. Its fixture always exits 0 (`149-153`), and the decision examines output substrings, not the required clean-versus-poisoned exit behavior (`169-174`).

Concrete in-memory fault injection, without editing either production file: substitute a helper whose entire implementation is `return dict(os.environ)`. The standalone control still prints `ENV control holds` and exits **0**, even though that helper scrubs nothing. Evidence: `env-control-false-positive.txt`.

This does not mean the real helper currently fails to scrub Git variables; its direct scrub test passed (see leg map). It means the required control does not establish that property or gate admission.

### MINOR N1 — selected-candidate provenance is not reproducible from `chosen`

`plans/round54_build_entrytruth.py:97-118` tries inherited r53-entry/default `--lane .` and bare candidates, then chooses the numerically smallest exit. Only the winner is stored (`126-132`), not the attempted candidates and their observed exits, despite the docstring's claim that `chosen` records which candidates ran (`11-15`). It does not consult the registry's full argv or call `entry_mode_ok` during selection. Inherited `kind=entry` is therefore candidate provenance, not independent proof of canonical entry mode.

Additionally, the current committed ledger labels `round53-c2`, `sources-adopt`, and `stage-scan` as `chosen: bare` while each argv contains `--lane .` (`plans/round54-entrytruth.json:877-889,917-943`). The shown builder labels a non-r53 winner containing `--lane` as `lane-dot`, never `bare` (`130`). These records cannot be reconstructed verbatim from this builder's tag rule; later editing/provenance is not captured in the field. Counter behavior does not depend on `chosen`, so this is a provenance defect rather than another independent passing exploit.

### MINOR N2 — required migration diagnostic is absent

Claims lines 148-150 explicitly require `REDECLARED <n>` to be printed. `plans/round54_c2_entrytruth.py:342-354` computes a count but prints only `MIGRATION redeclared=<n> r53_green_nonentry=<n>`. Existing consumers looking for the frozen diagnostic cannot observe it. The count is appropriately not an admission threshold.

## Leg map: frozen claim → code → assessment

| Leg | Implementation and lines | Assessment |
|---|---|---|
| REGISTRY | counter `43-45`, `55-89`, `209-242`, `265-278` | One heading; duplicate/malformed rows; script extraction; exact ledger membership. A row lacking an extractable script fails argv validation. Full invocation is not bound: B1/B2. |
| LEDGER | counter `92-109`, `146-165`, `220-241` | Duplicate JSON keys rejected; schema and row sets checked; integer/non-bool exit and consistent green/red state; red reason ≥10 words and evidence ≥6 stripped chars. Verbatim evidence checked at `338-341`. Script-only invocation check leaves B1/B2. |
| EXEC | counter `168-206`, `287-341`, `350-360` | Worker clone, reset/clean per invocation, row execution under helper, exit/evidence comparison, all rows required. TIMEOUT increments its separate counter (`320-323`), not `mismatched`, but `tmo == 0` is mandatory (`358`): it cannot pass. Green mismatch similarly has a separate mandatory-zero laundering count. ERROR cannot equal a valid integer declaration. |
| MIGRATION | counter `112-125`, `304`, `342-354` | Sweeps r53 green selftest/help rows and counts currently red entries. With a passing EXEC leg, these reds have matching observed nonzero exits. It does not trust `chosen`. Missing r53 ledger silently produces `{}`; not an issue for the supplied committed frozen ledger, but absence is not diagnosed. Required diagnostic mismatch: N2. |
| ENV | counter `128-143`, called at `193`; controls `140-174`; selftest `451-470` | Actual helper removes every uppercase `GIT_*` variable before pinning global/system/nosystem/prompt and scratch HOME/XDG. Direct probe including `GIT_CONFIG_COUNT`, indexed key/value, `GIT_CONFIG_COUNT_`, and `GIT_DIR` left only the four intended pins. ENV control is absent from evaluate and standalone control is false-positive: M1. |
| Clean source/revision | counter `287-295`, `358-359` | Source status must be empty and source revision equal lane revision when lane has Git metadata. Worker clones use source commits. These parent Git commands and worker clone/reset commands inherit caller environment rather than helper env; the helper applies to row subprocesses. No broader parent-command hermeticity proved here. |

## Builder selection and flag boundary review

- Winner selection is outcome-dependent (smallest integer exit, tie to A), not canonical argv derivation. An inherited r53 entry or default `--lane .` can win over a failing bare command. It records the actual winning argv, so there is no hidden mismatch between the argv executed and stored; the missing guarantee is that this argv is the registry's real entry, not another mode. Noninteger results are scored 999 and then declared exit 1 (`113-129`), which is not a literal observed TIMEOUT/ERROR; subsequent counter execution still fails if timeout/error persists.
- Do not classify `--summary` alone as laundering: the registry explicitly names it for benchmark-spec-audit, registry-reference-check, config-projection and extraction-policy-compare (`SKILL.md:570-572,614`). For the first two, `benchmark_spec_audit.py:405-429` and `registry_check.py:142-168` show it does not bypass the work or alter exit selection. Config projection documents summary as the default (`649-680`). No false summary finding asserted.
- Exact forbidden flags after `--` are still rejected: the validator does not stop at the delimiter. This is conservative, potentially rejecting literal positional data, not a bypass.
- `--selftest=1` and `--SELFTEST` are accepted statically. Whether a particular gate recognizes those spellings is script-specific; no successful laundering claim is made for them. `--selft` and uv decoy execution were actually demonstrated above.
- No separate chosen-field/history check detects an argv changed away from and later restored to canonical. Only the final supplied argv is validated/executed. `chosen` is ignored, so it neither establishes continuity nor independently changes execution.

## Exercised verification

- `selftest.txt`: requested selftest, **7/7 PASS**, exit **0**. Invoked unchanged imported `main(["--selftest"])`; a subprocess wrapper asserts scratch fixture top-level before each fixture commit. TMPDIR explicitly points inside this seat's scratch root.
- `dry.txt`: `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round54_c2_entrytruth.py --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin --dry`, **78 registry / 78 ledger**, zero static defects, exit **0**. Output correctly says `DRY static legs only: no predicate`.
- `laundering-probes.txt`: two unchanged full-counter fixture evaluations pass despite the true registry entry exiting 1.
- `env-scrub.txt`: actual helper scrub/pin inspection.
- `env-control-false-positive.txt`: standalone ENV control accepts a no-scrubbing helper.

## Residual risk and verification gaps

`xd://lsp` discovery returned `No such tool`; no mounted LSP device/server was available. Definitions/callers were inspected through source and literal grep fallback, not presented as semantic reference proof. Repository search found helper consumers in the counter, builder, controls; no semantic completeness claim.

No 78-row full landing-tip execution was requested or performed; dry success is not execution truth. No claim that all summary variants are equivalent. Broader timeout descendant cleanup, inherited Python/PATH configuration, and parent Git environment behavior were not attack-tested. Canonical C2 predicate logic is `evaluate`, shared by selftest/closure controls; builder reuses `run_row`, not a second scoring runtime. No resume-continuity path or same-identity rerouting is introduced in this diff; those review concerns are inapplicable. No saturation or calibration upgrade is admitted by this review.

No production file edited, no tool installed or upgraded. Scratch fixture commit identities remain confined to this seat's scratch roots, with pre-commit top-level assertions. Disk guard reported scratch free **367.1G** (55% used); its consumer listing timed out at 30 seconds, so only its printed space result is claimed. Scratch removed before handoff; receipts retained in this directory.

Self-evaluation: accuracy 4/5 (source/receipt backed; no full registry execution), completeness 4/5 (all requested legs mapped; no semantic LSP available), clarity 4/5 (separates demonstrated blockers from provenance/control gaps), actionability 4/5 (frozen kill-rule evidence and exact code locations, no unauthorized edits), conciseness 4/5 (detail retained for reproducibility). Overall 4.0/5. Highest-impact next action is L1 disposition of the two reproduced kill-rule triggers, not treating passing selftests/dry as closure.
