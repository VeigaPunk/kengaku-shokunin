The adaptive-rejection-sampler verifier rejects column-aligned result lines such as `standard_normal:                 PASS | mean=0.01 sd=1.02`. It currently requires the literal substring `: PASS` or `: FAIL`, so padding added by R's `sprintf("%-32s %s", ...)` makes an otherwise valid report fail verification.

Recognize named result lines with flexible horizontal whitespace, while requiring complete `PASS`/`FAIL` tokens and keeping the existing mean-statistics check. Check the test process exit code as well, so a valid-looking line printed before a crash cannot satisfy this assertion. This remains a report-format check: both PASS and FAIL labels are supported as specified by the task.

Add a separate verifier regression suite and read-only PR/push CI for changes to task verifier files. The suite calls the real verifier with synthetic subprocess output and tests spacing, tabs, indentation, LF/CRLF, malformed records, missing statistics, and process errors. The README gives a reusable pattern for adding other task-specific verifier regressions; current coverage is explicitly limited to this reporting contract.

Validation:
- 81 verifier regressions pass; the column-alignment regression fails against the unchanged verifier.
- A reconstructed R implementation that passed 8/9 existing task checks now passes 9/9 with only the verifier changed (isolated R 4.5.0 / Python 3.12 environment).
- No solution code, private trajectory, historical reward, or leaderboard entry is changed or included.
