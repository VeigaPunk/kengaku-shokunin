# R46W2C3Entry — C3 entry review

Reviewed at landing `42d5043afac952fcb43bf4798757785dd258cf85` (clone command: `git -C "$S/lane" rev-parse HEAD`; output: `42d5043afac952fcb43bf4798757785dd258cf85`). Compared the entry with its eight pinned captures, probe receipt and the lane's executed exemplars. No fresh probe was run.

## Findings

1. **The class comparison overstates the contrast with the other exemplars.** The entry says that “none of them executes the graded bytes as a program” (entry §Summary, lines 33–35), while its own cited closest distinction is merely that `circuit-fibsqrt` compiles a task-owned simulator. The round-43 `tb2-feal-differential-cryptanalysis-grader.md` describes an agent-authored Python module being imported (`test_outputs.py:24`) and its `attack` function called (`:29–30`); importing/calling that graded module executes the graded bytes as code. Thus the blanket negative is false, even though the narrower claimed difference—one same source file tested through both Python and C toolchains—is supported. The entry should distinguish dual-toolchain execution from in-process module execution rather than claim the latter does not execute graded bytes.

Evidence: `read` of `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` lines 10–30 reports the import/call sites; `corpus/README.md` lines 76 and 79 identify the module-import exemplar and this dual-runtime exemplar. No numerical measurement involved.

## What survives / residual risk

The inspected grader source supports the three-step mechanism: listing and exact one-name comparison precede gcc output to `/app/polyglot/cmain` (`captured test_outputs.py:17–25`); then the test loops over the three literal values and runs Python and C with `check=True`, comparing stripped stdout (`:27–46`). The receipt itself reports `cases=18 observed_pass=7 observed_fail=11 mismatches=0` and `regrade cases=18 differ=7` (command recorded in the receipt: `python3 plans/polyglot_c_py_probe.py --lane .`; this seat did not rerun it). The receipt case table agrees with the entry's case descriptions and mechanism lines on inspected examples, including `leftover-cmain`, `nonzero-exit`, and `value-plus-line`.

The requirement-map treatment of `both-print` and `toolchain` is transparent: it explicitly calls them “not exercised,” has no violating case to support a derived label, and discloses that V7 reports the missing violation as a defect. This is honest negative space, not evidence of a derived enforcement label. I did not independently replay the 18 cases or verify every captured digest; those remain verification gaps.

VERDICT: c3-entry-defects-1
