# FxGateVerdict — round 26 falsify (advisory)

Scope: `plans/gate_timing_check.py`, Q13, and the not-yet-admitted candidate `corpus/knowledge/grader-perturbation-audit.md`. All mutations were confined to `/tmp/kengaku-r26-FxGateVerdict`, cloned from integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`; no production file or lane Git state was changed. No tools installed.

## Findings, by severity

- **MEDIUM — Q13 accepts a registered seat with no declared reviewer-like role.** `plans/gate_timing_check.py:288-291` converts absent/non-string `role` to `""`; `:326-329` rejects only an unregistered seat or role `scribe`/`executor`, so `""` passes. In sandbox commit `8b72c9781605183738d2bf4ff06a2b8ecf2c7f01`, registry member `FxGateVerdictFixture` had `{}` (no role), while the nonempty report named `corpus/knowledge/grader-perturbation-audit.md` and carried `VERDICT: PASS`. The checker returned **exit 0**, `PASS line 7 Gate admit`, `passed=1 failed=0`. This does not establish a reviewer-like seat as required by Amendment 1 §8; current round-26 registry values were declared roles, so this is a fail-open checker case, not evidence of an actual roleless live report.

## Reproducible checks

Run from `/tmp/kengaku-r26-FxGateVerdict` (checker and all fixtures are in the scratch clone):

- `python3 plans/gate_timing_check.py --selftest` → **exit 0**, `[selftest] ALL PASS`.
- `python3 plans/gate_timing_check.py --lesson corpus/lessons/round-25.md --commit 8ea41f9 --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 1**; exact output: `cited seat-report paths: none`; `generic seat reference(s) (not report support): 'wave-2 seats'`; `gate_timing_check: commit=8ea41f9 lesson=corpus/lessons/round-25.md admissions=1 passed=0 failed=1 second-seat-reports=0`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-fixture.md --commit 7253c4db96062b3a3f85194771bd464df66f951c --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 1**; exact output: `invalid cited second-seat report: .ufo/waves/round-26/falsify/FxGateVerdictFixture.md (absent from commit tree)`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-fixture.md --commit 3624a9739b64c84e7f2db0d1c34394bcccd32f16 --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 1**; exact output: `invalid cited second-seat report: .ufo/waves/round-26/falsify/FxGateVerdictFixture.md (report does not name the admitted candidate path)`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-fixture.md --commit 607cbfaf02a3b98af8b4b6fac2a0897d8893c204 --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 1**; exact output: `invalid cited second-seat report: .ufo/waves/round-26/falsify/FxGateVerdictFixture.md (report has no anchored VERDICT line; return is not established)`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-same-commit.md --commit 65421152dd595dfd24624068e5947cdf1a249e0e --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 0**; exact output: `PASS line 7 Gate admit: candidate='corpus/knowledge/grader-perturbation-audit.md'`; `gate_timing_check: commit=65421152dd595dfd24624068e5947cdf1a249e0e lesson=plans/fixtures/r26/gate_timing/fxgate-same-commit.md admissions=1 passed=1 failed=0 second-seat-reports=1`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-missing-role.md --commit 8b72c9781605183738d2bf4ff06a2b8ecf2c7f01 --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 0**; exact output: `PASS line 7 Gate admit: candidate='corpus/knowledge/grader-perturbation-audit.md'`; `gate_timing_check: commit=8b72c9781605183738d2bf4ff06a2b8ecf2c7f01 lesson=plans/fixtures/r26/gate_timing/fxgate-missing-role.md admissions=1 passed=1 failed=0 second-seat-reports=1`.
- `python3 plans/gate_timing_check.py --lesson plans/fixtures/r26/gate_timing/fxgate-fixture.md --commit fedaaee1299c2662b69d4a6a73cfed19039c7331 --repo /tmp/kengaku-r26-FxGateVerdict` → **exit 0**; output `gate_timing_check: commit=fedaaee1299c2662b69d4a6a73cfed19039c7331 lesson=plans/fixtures/r26/gate_timing/fxgate-fixture.md admissions=1 passed=1 failed=0 second-seat-reports=1`; this later tree contains the report added after admission commit `7253c4d`.

The `fxgate-same-commit` result is structural acceptance only, as `corpus/lessons/round-26.md:39-41` and Q13 Amendment 1 §8 specify. It is **not** endorsement of the candidate or approval of the contradictory `VERDICT: FAIL`; do not report it as such. Missing report, missing candidate mention, and missing anchored verdict each fail as required.

## Residual risk and verification gaps

- The CLI audits only the caller-supplied `--commit` snapshot (`:568-623`); it does not establish that this is the commit where the candidate/Gate admission first landed. The fixture's admission commit `7253c4d` fails; a later descendant containing the subsequently added report (`fedaaee1299c2662b69d4a6a73cfed19039c7331`) passes. Q13 therefore depends on supplying the actual landing commit, not a later tip.
- At integration `3a2aeb15e6494a695d1a950ceea69b0cc9a154f8`, checking `corpus/lessons/round-26.md` returned **exit 1**, `no admit rows`; the candidate remains deferred, not admitted.
- LSP device unavailable (`read xd://lsp` returned `No such tool`); no status/references/definition/diagnostics were available. The Q13 locator grep was not treated as semantic evidence; findings above come from direct source lines and sandbox executions. Only assigned checker selftest/fixtures; no build/lint or unrelated tests.

VERDICT: FAIL — Q13's reviewer-role requirement is bypassable by a registered roleless seat; structural PASS on a `VERDICT: FAIL` report is not endorsement.
