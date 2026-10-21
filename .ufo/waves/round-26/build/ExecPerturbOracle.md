# Round 26 independent perturbation oracle

## Scope and source evidence
- Read pre-registration `plans/round-26-claims.md:37-79`; extractor regex spec read only at `grader.py:121-134` (`grader.py` grader functions were not read or imported; `grader_perturb.py` was not read or imported).
- Private clone: `/tmp/kengaku-r26-KengakuR26-2.ExecPerturbOracle-4`, branch `r26-KengakuR26-2.ExecPerturbOracle-4`; observed checkout base `e0037a8da26850fcf4c4b6ba40f14a017b3ecf2d`.
- Confirmed the pre-registered revision exists at `f11bffbf9caa9c9e286fb32c568b81b97719656a`; its four input hashes match the clone:
  - `round8-horizon/results.jsonl` `bd986e5e8c9b415aa2b0073fa8fed784282c9dbeb19055d34475e662792e2204`
  - `round9-replication/results-r9.jsonl` `c20158bdef148b322501341e539b2383d84de4179618fd46b801379c11affbcb`
  - `round11-power/results-r11.jsonl` `918bf7aa3030baa954c16a20830f078738147ce7cc002768e5ab922ad38f51ad`
  - `round12-ladder/results-r12.jsonl` `ad9c88e79068fa2833c90f071ec6da4035ff37371ff95d84f581dd4e8db842f1`

## Independent oracle output
Command: `python3 /tmp/kengaku-r26-KengakuR26-2.ExecPerturbOracle-4/plans/fixtures/r26/perturb_oracle.py --root /tmp/kengaku-r26-KengakuR26-2.ExecPerturbOracle-4`
```text
POPULATION candidates=1964 included=1964 excluded=0
EXCLUDED baseline=0 missing_want=0 meta_truth=0
F1 kind=MP n=1819 k=1802
F2 kind=MP n=1819 k=1802
F3 kind=MP n=1964 k=1964
F4 kind=MP n=1720 k=1720
F5 kind=MP n=1964 k=1964
F6 kind=MP n=1964 k=1964
F7 kind=MP n=1876 k=1876
D1 kind=PC n=909 k=909
G1 kind=MC n=1021 k=1021
G2 kind=MC n=1021 k=1021
```
`k` means MP invariance, MC baseline-PASS-to-FAIL, or PC extraction of the appended previous truth. Applied L1 Amendment 1: F1/F2 touch only the last matched answer fence; D1 is limited to baseline-PASS state/sequence operation records with `turn > 1`, excluding A-MONO/B/C and cases where previous truth equals `want`. D1 has `n=909`, `k=909`.

Post-output edge corrections: F1/F2 require a valid JSON last matched fence (not fallback extraction); F3 toggles indentation of the trimmed selected JSON span while preserving surrounding bytes; F4 requires a dict with at least two keys; F7 requires bare LF and preserves existing CRLF. Bounded controls: `python3 /tmp/kengaku-r26-KengakuR26-2.ExecPerturbOracle-4/plans/fixtures/r26/perturb_oracle.py --selftest` → `selftest: 13 checks, 0 failed`.

State/sequence baselines compare parsed answers with stored `want`, cross-checked against meta truth. C-cell baseline uses stored `parse`/`viol_ok`/`square_valid`/`preserved` facts because the pre-registration does not spell out the C grader predicate; G1/G2 mutations change the violation witness or invalidate/remove square structure. No external model or endpoint was contacted.

## Changed files and handoff
- Clone only: `plans/fixtures/r26/perturb_oracle.py` — SHA-256 `df0edaec33070713317dc4b80f82eb284cfd825dfd701fbb25b4fec7bcce33be`.
- Lane report only: `.ufo/waves/round-26/build/ExecPerturbOracle.md`.
- Risks: C-cell parity depends on the recorded diagnostics described above; compare counts with the core implementation before using them as its validation. No tool installs.

VERDICT: Updated oracle and 13 bounded edge controls ran; frozen population confirmed with counts unchanged and no exclusions.
