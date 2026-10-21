# Round 26 C1 — ExecPerturbCore

- Changed only `/tmp/kengaku-r26-ExecPerturbCore/plans/grader_perturb.py` in the private clone; no live lane source, index, or jj state changed.
- Observed clone base: `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d` (`git clone --no-hardlinks ... && git switch -c r26-ExecPerturbCore e0037a8da268`).
- Implements pinned four-file population, grader-derived meta truths and `want` cross-checks, exact baseline exclusion accounting, F1–F7/D1/G1/G2, CP95/bar verdicts, summary/JSON CLIs, and per-family transform selftests. Uses grader response functions and `plans/attrib_calibration.py` CP routine; C-MONO follows grader.py's `valid_latin` replay; no endpoint access.
- Source replay references: `grader.py:121-134,221-225,247-268,367-398,482-505,1006-1038,2115-2121,2269-2275,2463-2505`.

## `python3 plans/grader_perturb.py --summary` (clone)

FAMILY F1 kind=MP n=1876 k=1876 rate=1.000000 cp95=[0.998036,1.000000] verdict=PASS
FAMILY F2 kind=MP n=1819 k=1819 rate=1.000000 cp95=[0.997974,1.000000] verdict=PASS
FAMILY F3 kind=MP n=1964 k=1964 rate=1.000000 cp95=[0.998124,1.000000] verdict=PASS
FAMILY F4 kind=MP n=1720 k=1720 rate=1.000000 cp95=[0.997858,1.000000] verdict=PASS
FAMILY F5 kind=MP n=1964 k=1964 rate=1.000000 cp95=[0.998124,1.000000] verdict=PASS
FAMILY F6 kind=MP n=1964 k=1964 rate=1.000000 cp95=[0.998124,1.000000] verdict=PASS
FAMILY F7 kind=MP n=1876 k=1876 rate=1.000000 cp95=[0.998036,1.000000] verdict=PASS
FAMILY D1 kind=MP n=1948 k=931 rate=0.477926 cp95=[0.455535,0.500384] verdict=FAIL
FAMILY G1 kind=MC n=1021 k=1021 rate=1.000000 cp95=[0.996394,1.000000] verdict=PASS
FAMILY G2 kind=MC n=1021 k=1021 rate=1.000000 cp95=[0.996394,1.000000] verdict=PASS
TOTAL population=1964 excluded=0 audited_verdicts=17173 families_with_interval_verdict=10
COMMAND_EXIT_CODE=0

## `python3 plans/grader_perturb.py --selftest` (clone)

The command repeated the same 10 FAMILY lines and TOTAL line shown above, then emitted:
SELFTEST F1 PASS
SELFTEST F2 PASS
SELFTEST F3 PASS
SELFTEST F4 PASS
SELFTEST F5 PASS
SELFTEST F6 PASS
SELFTEST F7 PASS
SELFTEST D1 PASS
SELFTEST G1 PASS
SELFTEST G2 PASS
SELFTEST TOTAL checks=10 failed=0
COMMAND_EXIT_CODE=0

## Retained evidence

- Clone file written: `plans/grader_perturb.py` sha256 `d94bc87aa45f5dceb046e102b1694332410ae87600f93d9d73d51de928d9656d`.
- Frozen input pins verified by the successful runs:
  - `corpus/evidence/round8-horizon/results.jsonl` `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204`
  - `corpus/evidence/round9-replication/results-r9.jsonl` `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`
  - `corpus/evidence/round11-power/results-r11.jsonl` `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`
  - `corpus/evidence/round12-ladder/results-r12.jsonl` `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1`
- LSP was unavailable: no LSP device/API is exposed in the mounted tool inventory; symbols and replay bodies were located with `grep`/`read`.
- Risk/scope note: preregistration also calls for a separate independent oracle under `plans/fixtures/r26/`; that file was outside this seat's assigned implementation path. D1 FAIL is an observed last-block extraction sensitivity, not an execution failure.
- Installs/updates: none.

VERDICT: Scoped C1 instrument implemented in the private clone; summary and all ten family selftests exited 0.