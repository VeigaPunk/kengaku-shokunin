# S094 pinned-source findings

Source fetched from `https://raw.githubusercontent.com/hkust-nlp/Toolathlon/9be8d8fe07a497b18ee61e3f2ae694e9797f39eb/tasks/finalpool/ab-testing/evaluation/main.py` (commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`). Local capture: `/tmp/r32-R32SrcS094a/main.py`; 14,138 bytes; SHA-256 `3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad`.

(a) `main.py:58` — `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:`

(b) Verbatim excerpts (25 whitespace-words total):
- `main.py:69-72`: `if missing_scenarios:` / `validation_errors.append(f"Missing scenarios: {sorted(missing_scenarios)}")` / `if extra_scenarios:` / `validation_errors.append(f"Unexpected scenarios: {sorted(extra_scenarios)}")`
- `main.py:83-86`: `diff_A = abs(actual_A - expected_A)` / `if diff_A > tolerance_pct:` / `validation_errors.append(` / `f"Scenario '{scenario}' Version A: expected {expected_A:.3f}%±{tolerance_pct}%, got {actual_A:.3f}% (diff: {diff_A:.3f}%)"`
- `main.py:90-93`: `diff_B = abs(actual_B - expected_B)` / `if diff_B > tolerance_pct:` / `validation_errors.append(` / `f"Scenario '{scenario}' Version B: expected {expected_B:.3f}%±{tolerance_pct}%, got {actual_B:.3f}% (diff: {diff_B:.3f}%)"`

(c) `main.py:98-102`: on any validation errors it raises `ValueError(f"Record validation failed:\n{error_msg}")`; on success it prints the success message and falls through without a value, so returns `None` (also stated by the `-> None` annotation at line 58).

(d) This file establishes that its validator compares shared-scenario A/B conversion rates against an absolute `tolerance_pct` default of 0.1 and treats missing/extra scenarios as validation errors; it cannot by itself establish the benchmark's broader scientific validity or how other graders/judges score.

VERDICT: found
