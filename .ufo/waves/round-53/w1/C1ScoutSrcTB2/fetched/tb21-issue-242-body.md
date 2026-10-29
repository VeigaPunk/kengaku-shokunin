Continuing on our sweep for potentially reward-hacked tasks. 
### Summary
The instruction asks for a pandas/pathlib/configparser rewrite plus a dependency file listing numpy, pandas and matplotlib or scipy with version constraints. The test only checks that the dependency file exists, and for the script it just regex-matches two numbers in stdout. So `touch requirements.txt` plus a script with two hardcoded `print()` calls passes.

### Details
`instruction.md` lines 16–22 require the script to use pandas with UTF-8, `pathlib.Path` and `configparser`. Lines 24–27 require the dependency file to include numpy, pandas and at least one of matplotlib/scipy, with version constraints (`>=`, `==` or `~=`).

`tests/test_outputs.py`:

* Lines 14–15 check `/app/analyze_climate_modern.py` exists.
* Line 21 runs it and lines 34–43 regex-match the station 101 and 102 means in stdout, within 0.1 of -15.49 and 30.33.
* Lines 46–50 (`test_dependency_file_exists`) check that `/app/requirements.txt` or `/app/pyproject.toml` exists. The file is never opened.

The CSV (`environment/climate_analyzer/sample_data/climate_data.csv`) is 20 rows, 10 per station, so the two means are trivial to precompute. Nothing verifies that:

* the dependency file lists numpy, pandas, or matplotlib/scipy
* any version constraints are specified
* the script uses pandas, reads the CSV, or opens it as UTF-8
* the script uses `pathlib.Path` or `configparser`
* the printed numbers were computed at all

Tested against `harbor-framework/terminal-bench-2-1` @ `7131e43`

### How to reproduce

1. `touch /app/requirements.txt` (empty file)
2. Write `/app/analyze_climate_modern.py` as two `print()` calls, -15.49 for station 101 and 30.33 for station 102, in the format from `instruction.md` line 20. No imports, no CSV read.
3. Run the verifier.

Result: All tests pass. Line 49 only calls `Path(f).exists()`, and lines 34–43 only see stdout.

Note: without the dependency file, line 50 fails with `Must create either requirements.txt or pyproject.toml in /app/`. Printing wrong numbers fails the mean check. So the file has to exist and the numbers have to be right, but nothing checks what's in the file or how the numbers were produced (ie actually achieving the task) so it can be reward-hacked. 

### Related
Nothing matching as of time of writing.