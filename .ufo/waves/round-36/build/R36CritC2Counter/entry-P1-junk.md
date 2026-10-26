source: S108 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test_outputs.py
source: S109 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/tests/test.sh
source: S110 https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/regex-log/instruction.md
verified-at: 2026-10-25
recheck: 30d

# regex-log grader

cases=24 observed_pass=8 observed_fail=16 mismatches=0

## Negative space

Something could falsify this.

## Located quotes

| n | quote | where |
|---|---|---|
| 1 | “Write a regex” | `instruction.md:1` |
| 2 | “a regex expression” | `instruction.md:1-2` |
| 3 | “regex expression that” | `instruction.md:1-3` |
| 4 | “expression that matches” | `instruction.md:1-4` |
| 5 | “that matches dates” | `instruction.md:1-5` |
| 6 | “matches dates in” | `instruction.md:1-6` |
| 7 | “dates in the” | `instruction.md:1-7` |
| 8 | “in the format” | `instruction.md:1-8` |
