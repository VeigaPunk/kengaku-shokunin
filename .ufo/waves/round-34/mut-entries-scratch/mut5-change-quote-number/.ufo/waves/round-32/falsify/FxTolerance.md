# FxTolerance — Toolathlon tolerance review

VERDICT: confirmed

Reviewed the pinned capture `.ufo/waves/round-32/assimilation/captures/toolathlon-ab-testing-evaluation-main.py`.

- **Executed call uses 0.05:** `main.py:279-280` says `# Validate with 0.05% tolerance` and calls `validate_record_data(actual_records, expected_records, tolerance_pct=0.05)`. This is the call in the `if __name__=="__main__"` flow (`:237`) after reading actual and expected records (`:273-274`).
- **Default is not the task's executed tolerance:** `main.py:58` declares `def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1) -> None:`. The explicit keyword argument at `:280` overrides that default. In this file the function is called only at `:280`; therefore the default is not used by this main task path.
- **Missing/extra scenarios produce validation failures:** `:66-67` computes `missing_scenarios = expected_scenarios - actual_scenarios` and `extra_scenarios = actual_scenarios - expected_scenarios`; `:69-72` appends `Missing scenarios: {sorted(missing_scenarios)}` and `Unexpected scenarios: {sorted(extra_scenarios)}` when the respective sets are nonempty. `:98-100` joins `validation_errors` and raises `ValueError(f"Record validation failed:\n{error_msg}")` whenever either diff (or another validation error) exists.
- **No other differing call site:** searching the capture finds a single `validate_record_data` call, at `:280`, and no other tolerance argument. Other appearances in the capture are the definition/default (`:58`) and reads/uses of `tolerance_pct` within the function (`:84-93`, `:102`), not call sites. Repo-wide textual search also surfaced prose and reports, which are not executable call sites; this conclusion is scoped to the requested main.py capture.

No checks were run; findings are from reading the captured source.