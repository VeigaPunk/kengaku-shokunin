# FNoLeak — round 27 parser leakage audit

Identity: `KengakuR27.FNoLeak` (reviewer), **not** candidate writer `KengakuR27`. Axes: novelty (trustworthy fixed-response parser comparison) and calibration (no outcome leakage).
Observed private clone: `/tmp/kengaku-r27-FNoLeak`, HEAD `b5f62e5e637b34a1549e3475fc58b4227ed87e5a` (clone/switch/rev-parse command exited 0). I reread the whole 114-line draft `.ufo/waves/round-27/drafts/extraction-policy-comparison.md` and `plans/round-27-claims.md` including Amendment 1. Proposed canonical `corpus/knowledge/extraction-policy-comparison.md` is absent at the pinned revision; this is not an admission review.

## Diff and scope

`git diff --name-status b5719440e5eee46c1886fddbdf7bdc1624829454 b5f62e5e637b34a1549e3475fc58b4227ed87e5a -- plans/parser_policy_compare.py plans/policy_cases.py plans/fixtures/r27/policy_oracle.py plans/grader_perturb.py plans/state_check.py corpus/knowledge/extraction-policy-comparison.md` → `A plans/fixtures/r27/policy_oracle.py`, `A plans/parser_policy_compare.py`, `A plans/policy_cases.py`, `M plans/state_check.py`; `grader_perturb.py` is unchanged and canonical entry is absent. No production files changed by this review.

## Finding — LOW: oracle C-trio grading is score-cached, limiting independent regrade authority

`plans/fixtures/r27/policy_oracle.py:130-135` returns `got == record.get("got") and record["ok"] is True` for C-conflict/benign/norule; this reads stored truth after extraction, but does not independently run the C grader for an exact recorded answer. `count_policy` orders `extract` → `regrade` → stored-verdict comparison at `:166-179`. The draft's oracle disclosure at `.ufo/waves/round-27/drafts/extraction-policy-comparison.md:104-108` notes separate implementation and source reading, but not this C-trio shortcut. Qualify the oracle's independence for those rows if relying on it as independent grading support. This is not a policy/extraction leak and did not change the pinned counts: `PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/kengaku-r27-FNoLeak/oracle_grader_compare.py` → exit 0, `ORACLE-GRADE PASS pairs=17676 extraction_differences=0 verdict_differences=0 c_trio_pairs=108 c_trio_recorded-got-shortcuts=96 first_difference=None`.

## Leakage, ordering, and restoration results

- Source: `plans/parser_policy_compare.py:40-147` defines `_loads`, `_bare_last`, and E0–E8 (registry at :137-147); all policy signatures are `raw`. `plans/fixtures/r27/policy_oracle.py:91-110` has the separate extraction dispatch. Neither extraction call graph reads `want`, `stored_ok`/row `ok`, a record grader, or frame state. `gp` attributes in instrument extraction are only `BARE_RE` and `FENCED_RE`. Local parser `ok` variables are JSON-parse-success booleans.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B /tmp/kengaku-r27-FNoLeak/no_leak_probe.py` → exit 0:
  `STATIC PASS parser_policies=9 parser_helpers=2 oracle_extract_helpers=7 sensitive_refs=0 frame_refs=0 gp_attrs=['BARE_RE', 'FENCED_RE']`
  `POISON PASS records=1964 policies=9 calls=17676 extraction_differences=0 policy_poison_hits=0 negative_control=BLOCKED field=want`
  `ORDER PASS events=raw,extract,grader,want,grade`
  `RESTORE PASS exception=RuntimeError wrapper_restored=true events=raw,extract,grader,want,grade-raises`
- The probe asserts `build_population` returned all 1964 pinned records with no loader errors; each non-raw record field is poisoned/guarded while all nine policies run, and a caller-frame `rec.want` negative control is blocked. `parser_policy_compare.py:249-265` extracts via `policy(rec.raw)` before `grade_value`; `:169-175` restores `gp._GRADER` in `finally`. `grader_perturb.py:259-275` extracts before reading `rec.grader`/`rec.want`; `parser_policy_compare.py:191-205` reads `stored_ok` only in post-grade tally. The oracle's C shortcut is the sole noted post-extraction stored-`ok` use.
- On this pinned clone, `PYTHONDONTWRITEBYTECODE=1 python3 -B plans/fixtures/r27/policy_oracle.py --root /tmp/kengaku-r27-FNoLeak` exited 0 and emitted the registered per-policy counts: E0 1964/0/0/0; E1 1947/17/0/0; E2 1964/0/0/0; E3 1947/17/0/0; E4 952/1012/0/1876; E5 1938/26/0/145; E6 1964/0/0/0; E7 1947/17/0/0; E8 1964/0/0/0 (`agree/flip_pf/flip_fp/none`).

## Residual risk and verification gaps

No LSP device is mounted (`read xd://lsp` returned “No such tool”); references/definition/diagnostics were unavailable. No grep result is used as semantic proof. This offline Python slice has no canonical model runtime, rerouting, or saturation claim. I did not run P4 state-check or Q15 gate tests; this report grants no P4/Q15 or admission authority. No build, lint, formatter, model/endpoint call, or tool install/update.

Installs/updates: none.
VERDICT: Scoped no-leak / extraction-before-grading / exception-restoration checks PASS on b5f62e5e637b34a1549e3475fc58b4227ed87e5a; no parser leakage or pinned-count discrepancy found. LOW residual: disclose the oracle's post-extraction C-trio stored-ok shortcut when describing independent grading support; no global or admission verdict.