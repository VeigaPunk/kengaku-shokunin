# R45 C1 instrument review

Review scope: `plans/round45_c1_verify.py`, pinned inputs and the stated counter contract. LSP was unavailable in this seat's device set; findings below are based on direct source inspection, not semantic-reference claims. No counter, fixture build, fence run, or probe was run.

## Findings (severity order)

1. **HIGH — fence can tamper with its own trace log.** `run_fence` makes `logdir` writable in the bwrap sandbox (`round45_c1_verify.py:177-180`), then gives the fence process the fixture path `d` and runs it with cwd `d`. The fence can climb from `d` to the scratch root, locate `strace/sNNNNN/log`, and open/truncate/replace that file while strace is recording. The trace parser later trusts `log.read_text()` (`:192-222`); a fence could erase evidence of outside opens, yielding a false `opens=0` and potentially changing C1's pass predicate. Read-only for everything except that log directory is therefore not a true read-only fence sandbox. Keep trace output inaccessible to the child (e.g. separate namespace/descriptor arrangement) and parse an immutable parent-held trace.

2. **MEDIUM — traced outside-open region omits module copies.** `build_module` puts module copies at `<root>/mods/mod_...` (`:116-117`), while `run_fence` defines the only scratch roots it counts as `(root / "fx", root / "btmp")` (`:210-213,217-221`). A malicious fixture/fence can resolve the common scratch root by walking up from `d` and access a module source under `mods/`; such successful or blocked opens are outside `d` but invisible to the `opens` counter. This undercounts the advertised “whole process tree opens no path outside the fixture directory” property for files in its own build scratch. Include all scratch subtrees in the path classification (or narrow and accurately name the measured region).

## Questions checked

- **Pinned lane paths:** all 33 `PINS` keys are present as files in the lane. Command: Python AST extraction of the counter's `PINS`, followed by `Path(x).is_file()` for each key; output: `PINS 33 missing []`. This is existence only, not a digest/predicate run.
- **HONEST_TOTAL:** the hard-coded 104 is checked against `len(hrows)`, i.e. fixtures actually built and handed to `run_fence`, not the number of `fid` textual occurrences. The requested shell expression `find plans/battery4* ...` also includes battery40/41 and counts `fid` lines, so it is not the right measurement for this counter's three pinned honest directories; the counter uses battery42/43/44. There are 22 source modules in those directories (same AST/path counting command). A separate attempt to calculate declaration lengths statically failed because fixture declarations contain non-literal names; no claim that 104 was independently re-counted. The frozen claim says 104; the counter's literal makes a mismatch fail closed if built fixture count differs.
- **Hostile fixture authenticity:** the instrument invokes the pinned round-44 `builder_source()` on pinned refusal modules and checks the returned fixture contract, but does not independently prove that each hostile build actually exercises the named real vulnerability. That remains a quality/fixture-design limitation rather than a direct counter bug; the frozen claim itself bounds its ten modules and source digests.

VERDICT: instrument-review-defects-2-predicate-changing-1
