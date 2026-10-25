# Round 34 README patches

Source read: `corpus/README.md` (snapshot E78F), current line numbers and quoted old text below. These are proposed patches only; no README edits made.

## (a) Knowledge index row — `terminal-bench-task-grader.md`

Replace at line 68, immediately before the existing `lessons/round-1.md` row.

Before (line 68 is blank):
```text

```

After:
```text
| `knowledge/terminal-bench-task-grader.md` | Terminal-Bench 2.0 `protein-assembly` task evaluator: runner/reward behavior and output grading grounded against `antibody.fasta` and `pdb_ids.txt` | S105, S106, S107 — task @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6` |
```

## (b) Knowledge index row — `provider-selfreport-eval-limits.md`

Replace at line 68, immediately before the existing `lessons/round-1.md` row.

Before (line 68 is blank):
```text

```

After:
```text
| `knowledge/provider-selfreport-eval-limits.md` | Limits of provider self-reports for evaluation: distinguish located source claims from independently verified evaluation evidence | S108, S109 — `corpus/SOURCES.md` rows |
```

## (c) Coverage-map discharge sentence

Replace line 256, the blank separator after the benchmark-grader-semantics bullet and before `## Open gaps`.

Before (line 256 is blank):
```text

```

After:
```text
- **Terminal-Bench grader semantics**: covered at source-code depth (round 34, 2026-10-25) — `knowledge/terminal-bench-task-grader.md`; S105–S107. Discharges the Terminal-Bench 2.0 scoring-code clause for the `protein-assembly` task evaluator (`tests/test.sh` and `tests/test_outputs.py` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`), grounded against `environment/antibody.fasta` and `environment/pdb_ids.txt`; other task evaluators remain open.
```

## (d) Frontier bullet narrowing

Replace line 279 only. Preserve all other clauses verbatim.

Before (line 279):
```text
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads S103's one Toolathlon task (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and S104's LLM-as-judge survey frame (arXiv 2412.05579v2). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (Terminal-Bench 2.0's; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane).
```

After:
```text
  - *Partly discharged round 33 (2026-10-25):* `knowledge/benchmark-grader-semantics.md` reads S103's one Toolathlon task (`tasks/finalpool/ab-testing/evaluation/main.py` @ `9be8d8fe`) and S104's LLM-as-judge survey frame (arXiv 2412.05579v2). The "and for Toolathlon" clause is discharged **for that one task's scoring code only**; the clause stays open for the other benchmarks' scoring code (the Terminal-Bench 2.0 `protein-assembly` task evaluator (`tests/test.sh` and `tests/test_outputs.py` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`) is now opened; any SWE-bench Pro V2 grader beyond the round-31 task-level one) and for runtime task validity (which `PROVINCE.md` refuses to this lane), hosted judges, and contamination.
  - *Partly discharged round 34 (2026-10-25):* `knowledge/terminal-bench-task-grader.md` reads the `protein-assembly` task evaluator at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` and grounds it against `environment/antibody.fasta` and `environment/pdb_ids.txt`; S105–S107. The Terminal-Bench scoring-code clause is discharged **for this one task evaluator only**; the clause stays open for any SWE-bench Pro V2 grader beyond the round-31 task-level one, runtime task validity (which `PROVINCE.md` refuses to this lane), hosted judges, and contamination.
```

VERDICT: readme-patch-drafted (4 blocks)
