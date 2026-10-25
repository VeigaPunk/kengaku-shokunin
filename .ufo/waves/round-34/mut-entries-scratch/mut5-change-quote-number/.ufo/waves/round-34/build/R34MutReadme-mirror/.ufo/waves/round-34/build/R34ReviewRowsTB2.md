# Second-seat review: S105–S107

Axis: coverage. Reviewed `.ufo/waves/round-34/build/R34RowsTB2/append-rows.md` against the SOURCES v1 registry format and requested row gates.

## Row verdicts

- **S105 — defect.** Content gates pass: kind `code`, tier A is consistent with the primary evaluator source and stated grading-logic scope; the quote record is 10 words and appears at `assimilation/captures/tb2-eval/test_outputs.py:18` (`quotes.json`); status `mined`, opened `2026-10-25`, and used-by exactly `corpus/knowledge/terminal-bench-task-grader.md`. **Defect:** draft line has 11 fields, not required NF=13, because it lacks outer pipes.
- **S106 — defect.** Content gates pass: kind `code`, tier A is consistent with the primary runner source and stated runner/reward scope; quote `echo 1 > /logs/verifier/reward.txt` is 4 whitespace-delimited words and appears at `assimilation/captures/tb2-eval/test.sh:27` (`quotes.json`); status/date/used-by match the requirement. **Defect:** draft line has 11 fields, not NF=13.
- **S107 — defect.** Content gates pass: kind `dataset`, tier A is consistent with the task's primary expected-artifact files and stated artifact scope; quote `>heavy chain` is 2 words and appears at `assimilation/captures/tb2-eval/antibody.fasta:1` (`quotes.json`); its anchor also names `pdb_ids.txt:1-20`, present in the capture. Status/date/used-by match. **Defect:** draft line has 11 fields, not NF=13.

All three rows contain 11 intended cells. No literal or escaped pipe occurs within a cell (10 delimiters per line; escaped-pipe search returned 0). The required outer pipes are missing from each line, so each line has `NF=11` rather than `NF=13`; the specified registry-row grep therefore finds zero rows. Add leading and trailing `|` to each row before integration.

## Evidence

- Contract columns: `corpus/SOURCES.md:20` registry header has 11 columns; its data rows are pipe-wrapped. Contract text immediately above the header states tier is scoped to `scope`, A includes source code/primary sources, and valid statuses include `mined`.
- Command: `awk -F'|' '{print NR": NF="NF}' .ufo/waves/round-34/build/R34RowsTB2/append-rows.md` — output: `1: NF=11`, `2: NF=11`, `3: NF=11`.
- Command: `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' .ufo/waves/round-34/build/R34RowsTB2/append-rows.md` — output: `0`.
- Command: `awk -F'|' '{print "row="NR,"cells="NF,"pipes="NF-1,"start="substr($0,1,1),"end="substr($0,length($0),1)}' ...` — output for each row: `cells=11 pipes=10 start=S end=d`.
- Command: `grep -cF '\\|' .ufo/waves/round-34/build/R34RowsTB2/append-rows.md` — output: `0`. The field counts also show there are no extra literal pipe delimiters within a cell.
- `quotes.json` records S105/S106/S107 quotes and capture locations. Reads of captured `test_outputs.py:14-30`, `test.sh:14-32`, and `antibody.fasta:1-8` show the quotes at the cited locations; `pdb_ids.txt:1-20` contains the anchored identifier list.
- Command: `awk -F'|' '/^\\| S[0-9]/ {print $11}' corpus/SOURCES.md | sort | uniq -c` — observed recheck values: `180d` (38), `2027-01-17` (19), `2027-01-19` (8), `90d` (10), `on-release` (22). `annual` is not an observed recheck value; the requested checklist does not specify a recheck-value restriction, so I do not count it as a defect.
- Command: `grep -c 'S10[567]' corpus/SOURCES.md` — output: `0` (no current registry ID collision).

VERDICT: review-rows-tb2 (3/3 defect)
