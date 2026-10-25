ATTACKS: Join every calibration-summary CP95 line to the reference table; test endpoint discrepancies and verdict changes.
Axes: endpoint correctness; threshold/verdict stability; sample-size coverage.

- `corpus/evidence/round25-calibration/attrib-calibration-summary.txt:1-48`; `plans/fixtures/r25/cp_reference.tsv:2-862`: parsed and joined all 48 CP95 rows by (k,n); 0 missing references. The fixture contains 861 rows covering n=0..40.
- Maximum absolute displayed-endpoint/reference difference: 4.89003e-7, below 0.00000051 (six-decimal rounding allowance). Largest: summary line 46, high endpoint 0.385667 vs reference line 473, 0.385666510997. No endpoint exceeded the allowance.
- `plans/round-25-claims.md:35-45` sets the interval rule/bar 0.80. Re-evaluating all verdict-bearing rows against reference endpoints yields 0 changes: PASS=12, FAIL=0, INDETERMINATE=11, UNTESTED=12 (summary line 49 reports the same totals). The 13 share/sensitivity rows have no interval verdict.
- No summary row has n>40, so the conditional independent `fractions.Fraction` bisection was not triggered. No install or source-tree changes; only this assigned report was written. Risk: this run does not exercise n>40.

Installs: none.
VERDICT: SURVIVES — all summary CP95 values join the reference within display rounding; no interval verdict changes.