# FxP3AState — P3a state-assertion base mismatch

Axes: calibration only. Scope: P3a `state-assertion-check`, historical base mismatch, recorded exits, R26-E6 supersession, and partial-token rejection. Advisory review; no admission judgment.

## Evidence

- Read `plans/round-26-claims.md` including Amendments 1–2 and `corpus/lessons/round-26.md`. Frozen base: `f11bffbf9caa9c9e286fb32c568b81b97719656a`; integration: `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8` (`integration-revision.txt`).
- LSP unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices. No LSP status/references/definition/diagnostics were available; source/diff reads and runtime outputs below are not semantic caller proof.
- Read-only diff captured: `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin diff --no-ext-diff --unified=3 f11bffbf9caa9c9e286fb32c568b81b97719656a 3a2aeb15e6494a695d1a950ceea69b0cc9a154f8 -- plans/state_check.py` → exit 0; saved at `/tmp/kengaku-r26-FxP3AState.xeExzw/state_check.diff`.
- Scratch exports only: `git archive` of base and integration into `/tmp/kengaku-r26-FxP3AState.xeExzw/{base,integration}` → both exit 0. No lane files/state/index were changed.

## P3a results

- Frozen receipt `corpus/evidence/round25-calibration/state-check-before-6180e4f-v2.txt:2,14`: base `mismatch=10`, `exit=1`. The old capability cell `SCORECARD.md:559` says `mismatch=11`. The `state-check-after-v2.txt:1,14` records landed `mismatch=0`, `superseded=1`, `exit=0`; `state-check-selftest-v2.txt:1-2` records ALL PASS, `exit=0`.
- Command: `python3 -B /tmp/kengaku-r26-FxP3AState.xeExzw/integration/plans/state_check.py --root /tmp/kengaku-r26-FxP3AState.xeExzw/base --summary` → exit 1 as expected for the frozen base. `P3a.capability.state-assertion-check.base-mismatch` is MISMATCH: claim `["11"]`, receipt `["10"]`, derived correction token `["mismatch=10"]`.
- Command: same checker with `--root /tmp/kengaku-r26-FxP3AState.xeExzw/integration --json` → exit 1 overall; parsed P3a state IDs: `base-mismatch=SUPERSEDED` (claim 11, receipt 10, `correction_line=749`, `correction_tokens=["mismatch=10"]`); `base-exit=MATCH` (1); `landed-mismatch=MATCH` (0); `landed-superseded=MATCH` (1); `landed-exit=MATCH` (0). Source: `plans/state_check.py:1258-1285`; exact-token gate: `:1153-1161`; E6: `SCORECARD.md:749`.
- Partial-token counterexample, scratch only: copied integration to `/tmp/kengaku-r26-FxP3AState.xeExzw/partial-token`, changed only its E6 line 749 from `mismatch=10` to `mismatch=1`. `python3 -B /tmp/kengaku-r26-FxP3AState.xeExzw/partial-token/plans/state_check.py --root /tmp/kengaku-r26-FxP3AState.xeExzw/partial-token --json` → checker exit 1; parsed `P3a.capability.state-assertion-check.base-mismatch=MISMATCH`, `derived_tokens=["mismatch=10"]`, `correction_tokens=["mismatch=1"]`. Thus an incomplete/wrong token does not supersede; the unchanged integrated E6 exact token does.
- P2 preservation: v2 and v3 `--json` on the exported base each contained 247 P2 assertion records; exact filtered records were identical (`P2_IDENTICAL=True`, comparison exit 0). Commands were `python3 -B .../base/plans/state_check.py --root .../base --json` and `python3 -B .../integration/plans/state_check.py --root .../base --json`; v2 exit 0, v3 exit 1 from expected P3 reds.
- `python3 -B /tmp/kengaku-r26-FxP3AState.xeExzw/integration/plans/state_check.py --selftest` → exit 0, `[selftest] ALL PASS`. Its P3a case targets `P3a.capability.interval-reverdict.selftest-checks` (`plans/state_check.py:1965-1994`), not the state-base-mismatch ID; the state-mismatch branch was independently exercised above.

## Residual risk / verification gaps

- The integrated checker is not globally green: its exit 1 has two remaining mismatches, `P3b.province.public-literature-registry.rows` and `P3b.province.round25-correction.rows` (integration JSON summary: `mismatch=2`). These are outside this P3a assignment; do not treat this report as an overall C2 pass.
- No LSP-backed caller/diagnostic proof was possible. No tools were installed; no build, lint, or formatter was run.

VERDICT: Scoped P3a state-mismatch, recorded-exit, exact R26-E6 supersession, partial-token rejection, and unchanged P2 population are evidenced in exported scratch trees; no actionable P3a defect found. Advisory only, not an admission.