# R46ScoutC3Prior — upstream prior art

Access date: 2026-10-27.

## Opened primary sources and candidates

1. **Tier 1 (upstream issue/PR record); scope: polyglot-c-py workspace/output grader behavior.** [Terminal-Bench 2 PR #37](https://github.com/harbor-framework/terminal-bench-2/pull/37), opened in full. Quote: “previously asserted the source file was the only file in `/app/polyglot`, which failed when compiled binaries from prior test runs were present” (PR #37, Summary, Feb. 13 2026). It records a strict directory-list assertion defect, replaced by source existence check and cleanup fixture. Evidence concerns artifact residue, not lookup-table deception, compiler/runtime drift, or output-comparison fixed points.

2. **Tier 1 (upstream issue/PR record); scope: earlier polyglot-c-py grader contract.** [Terminal-Bench 1 PR #1390](https://github.com/harbor-framework/terminal-bench-1/pull/1390), opened in full. Quote: “Relaxes the file verification in /app/polyglot to permit additional artifacts like compiled binaries” (PR #1390, author description, Jan. 16 2026). Similar artifact-residue issue; source existence retained. Not evidence of the three requested attack classes.

3. **Tier 1 (pinned upstream grader source); scope: exact dual-runtime invocation and expected outputs.** [Pinned test_outputs.py](https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py), opened. Quote: “assert python_out == expected and c_out == expected” (test_fibonacci_polyglot). The grader independently compares both stdout strings to literal expected outputs for inputs 42, 10, 0; it does not merely compare Python to C. Also asserts the source is the only directory entry before compilation, then compiles to cmain. This makes artifact state a known historical concern. No cmain idempotence, version-drift, or lookup-table claim established by this source.

4. **Tier 2 (published research; scope: benchmark cheating / answer lookup as broad class, not this task’s exact grader).** [Stein et al., “Detecting Safety Violations Across Many Agent Traces,” arXiv:2604.11806v1](https://arxiv.org/html/2604.11806v1), opened. Quote: “uncovers both extensive harness-level cheating (scaffolds leaking answers to models) and task-level reward hacking” (§3.3). Its Terminal-Bench discussion describes verifier/answer-key injection, but does not establish polyglot-c-py lookup-table cheats or a fixed-point output-comparison grading method. Keep only as broad context, not a direct task-source row.

## Search coverage and gaps

Searches targeted GitHub PR/issues in `harbor-framework/terminal-bench-2` and `laude-institute/terminal-bench` for polyglot-c-py, cmain, lookup-table cheats, and fixed-point output graders. Direct search results surfaced PR #37 and #1390; both were opened. I found no opened primary issue/PR documenting lookup-table cheating, cmain non-idempotence, GCC/Python version drift, or a fixed-point output grader. Search snippets and synthesized search summaries are not citable; no claim is made that absence from search proves absence upstream. The arXiv paper is opened research, but its relevance to exact grader behavior is only contextual.

The pinned grader’s dual expected-value assertions suggest that output equivalence alone is insufficient to pass: both runtimes must produce the prescribed values. That is an inference from source, not a published note about fixed points. I found no primary source describing fixed-point output graders; synthesized explanation is not citable.

## Proposed SOURCES rows

- `SOURCES | Tier 1 | https://github.com/harbor-framework/terminal-bench-2/pull/37 | polyglot-c-py / polyglot-rust-c compiled artifact residue; strict directory assertion correction | opened 2026-10-27`
- `SOURCES | Tier 1 | https://github.com/harbor-framework/terminal-bench-1/pull/1390 | polyglot-c-py allowing compiler output alongside required source | opened 2026-10-27`
- `SOURCES | Tier 1 | https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py | pinned grader: exact expected stdout under Python and compiled C, plus pre-build directory assertion | opened 2026-10-27`
- `SOURCES | Tier 2 | https://arxiv.org/html/2604.11806v1 | broad published treatment of benchmark answer leakage/cheating; not exact polyglot grader evidence | opened 2026-10-27`

VERDICT: polyglot-prior-art-opened-4-row-candidates-4
