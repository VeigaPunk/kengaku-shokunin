# R49C2ScoutEntry — polyglot knowledge-entry scope review

**Axes:** coverage (assigned); entry/source fidelity and scope discipline (review dimensions).
**REV measured:** `9d2900af41e4d1fc6022eff99010436fde6dbd93` (stage-1 freeze, commit dated 2026-10-28T09:14:40-03:00; verified before any scored execution). No scored counter or probe was run.

## Finding

**Overreach found in the comparative class teaching, but not in the task-specific grader mechanics.** All eight captured files in `corpus/evidence/round46/tb2-polyglot-c-py/` pass `sha256sum -c SHA256SUMS`, and all eight pinned upstream files re-fetched at commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6` have matching SHA-256 digests. The entry's descriptions of S166–S172, located quotes, grader order, three tested inputs, `check=True`, stripped-stdout comparison, receipt outcomes, requirement-map derivation, and explicitly stated limits are supported by those captures and the pinned receipt/dry table. The `pkg-spec-r46.json` capture and instrument pins also match their files' digests.

The entry's original broad wording remains false: summary lines 34–35 says none of the other exemplars “executes the graded bytes as a program,” and Finding 7 repeats this contrast. At least two cited-lane exemplars contradict it: `tb2-feal-differential-cryptanalysis-grader.md` says the grader imports `/app/attack.py` and calls `attack.attack(...)`; `tb2-build-pmars-grader.md` says the grader runs `/usr/local/bin/pmars` and checks its output. The appended Errata 1 acknowledges the FEAL counterexample and narrows the intended distinction to compiling the graded artefact or running the same bytes under two language runtimes. That narrower distinction is consistent with the reviewed examples, but the erratum does not mention the separate build-pmars execution counterexample, and the original wording remains in place. This is residual comparative overreach, not an issue with the pinned TB2 task facts.

No other clear overreach found within the C2 entry's declared limits. In particular, it expressly limits toolchain conclusions to host gcc/python, says pytest/image/agent were not run, and does not extrapolate to Harbor retries/restoration or task validity. Receipt says exactly `regrade cases=18 differ=7` and `cases=18 observed_pass=7 observed_fail=11 mismatches=0`; all listed case verdicts and `violates=` tokens agree with the entry and frozen table. V7's round-46 defect output is consistent with the two non-exercised, unparsed rows.

## Evidence / commands

Commands run (read-only unless stated):

- `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin cat-file -t 9d2900af41e4d1fc6022eff99010436fde6dbd93` → `commit`; `git -C ... log -1 --format='%H %cI %s' ...` → `9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28T09:14:40-03:00 round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims`.
- `git clone --shared --no-checkout ... lane`, then `git -C lane checkout -q 9d2900af41e4d1fc6022eff99010436fde6dbd93`; `git -C lane rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C2ScoutEntry/lane`; `git -C lane rev-parse HEAD` → `9d2900af41e4d1fc6022eff99010436fde6dbd93`.
- `(cd .../corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` output, verbatim: `gitignore: OK`, `README.md: OK`, `Dockerfile: OK`, `instruction.md: OK`, `solve.sh: OK`, `task.toml: OK`, `test.sh: OK`, `test_outputs.py: OK`.
- `curl -sf --max-time 20 <pinned raw URL> -o <scratch file> && sha256sum <scratch file>` for the eight S166–S172 sources; observed digests matched the eight manifest values (including `test_outputs.py` `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`).
- Read `corpus/evidence/round46/polyglot-c-py-probe.txt`, `...-dry-cases-freeze.txt`, `plans/pkg-spec-r46.json`, `plans/round46_c3_verify.py`, `corpus/SOURCES.md` S166–S172 rows, and sibling knowledge entries cited above. Relevant observed receipt tail: `regrade cases=18 differ=7` / `cases=18 observed_pass=7 observed_fail=11 mismatches=0`.
- No probe/counter execution, build, test, lint, or mutation performed.

## Source access record

All eight upstream sources below were fetched on **2026-10-28** from the immutable pinned commit. Located quotes are exact excerpts of at most 25 words; digests match committed capture manifest:

- S166 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py` — `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` (line 27; 8 words).
- S167 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test.sh` — “-p 3.13” (line 19; 2 words).
- S168 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md` — “Both of these should print to stdout the kth Fibonacci number” (line 7; 11 words).
- S169 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/solution/solve.sh` — “cat <<'EOF' > polyglot/main.py.c” (line 12; 4 words).
- S170 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/environment/Dockerfile` — “RUN apt update -y && apt install -y gcc” (line 6; 9 words).
- S171 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/task.toml` — “allow_internet = true” (line 34; 3 words).
- S172 `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/README.md` — “Test cases: f(0)=0, f(10)=55, f(42)=267914296” (line 24; 6 words).

**Limits:** This is a source-and-capture scope review only. I did not re-run the round-46 probe, independently execute sibling graders, or fetch the unrelated sibling exemplars' upstream sources. Lane-wide comparative wording is therefore based on their committed knowledge entries, not fresh upstream revalidation. No R49-C1/C2 admission claim.

**VERDICT: OVERREACH — original cross-exemplar claim that no earlier exemplar executes graded bytes is contradicted by FEAL differential and build-pmars entries; pinned task-level teachings otherwise supported within stated limits.**