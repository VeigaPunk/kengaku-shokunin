# README delta for the C2 package (round 38)

Insert `index-row` after the `knowledge/tb2-git-webserver-grader.md` row in the index table
(`corpus/README.md`, the round-37 line), and `coverage-bullet` after the "Terminal-Bench 2.0 task grader
(third task …)" bullet in `## Coverage map`. Both lines are complete and byte-ready; nothing else in
`corpus/README.md` changes.

## index-row

| `knowledge/tb2-build-pmars-grader.md` | A fourth Terminal-Bench 2.0 task grader read and executed: `build-pmars` scores four pytest functions — binary presence, two debugger address lines, a start-anchored `Results:` match, an `ldd` string scan and a one-level `/app/pmars-*` tree — so a canned 14-line C program plus an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four tests, a `dlopen()`ed libX11 evades the X11 scan, exit 3 with output is ignored, and `Results: 12 34 78 forged` passes; no instruction line is fully enforced (`cases=22 observed_pass=7 observed_fail=15 mismatches=0`) | S115, S116 (terminal-bench-2 @ 2fd12b88) |

## coverage-bullet

- **Terminal-Bench 2.0 task grader (fourth task, build-provenance class)**: covered at source-code depth and executed offline (round 38, 2026-10-26) — knowledge/tb2-build-pmars-grader.md; S115, S116; probe `plans/build_pmars_probe.py`, receipt `evidence/round38/build-pmars-probe.txt`. A fourth instance of the same ground (4 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `build-pmars` only: its whole score is four pytest functions over an installed binary's output, an `ldd` `DT_NEEDED` string scan and a one-level `/app/pmars-*` tree; a canned C program with an empty `debian/` directory and a zero-byte `src/dummy.c` passes all four, the behaviour checks run whatever `pmars` is first on `PATH` while `ldd` reads the installed absolute path, and none of the seven instruction requirements is fully enforced. Adds the build-provenance edge class to the executed grader sample (presence, linkage string, directory shape, output regex); not a new verdict channel, and no novelty claim.
