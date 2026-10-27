# R48C2ScoutEntry — C2 knowledge-entry/capture comparison

## Scope and result

Axis: **coverage**. Read-only comparison of the committed `corpus/knowledge/tb2-polyglot-c-py-grader.md` at frozen base `a543d92083557dd9b33ee674e9b99b03411f80af` against the round-46 pinned capture set and receipt. No counter or probe was run; this is not an admission decision.

**VERDICT: OVERREACH FOUND.** The entry's specific grader teachings, located quotes, case outcomes, requirement-map labels, negative-space statements, and stated execution limits are supported by the committed captures/receipt, with one residual class-contrast overclaim in the prose despite an erratum that identifies it. Findings below distinguish capture-grounded content from claims about other lane exemplars.

## Freeze and revision

The claims document is present in the frozen commit: `git ls-tree a543d92083557dd9b33ee674e9b99b03411f80af plans/round-48-claims.md` returned `100644 blob 3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5 plans/round-48-claims.md`; its commit timestamp is `2026-10-27 06:53:29 -0300`. `git log --oneline a543d920..HEAD -- plans/round-48-claims.md` returned no rows. The live file hash is `3a9c71f3f437dc4b21c70bb5d4f68a379adf44f5`; the initial `git cat-file blob … | sha1sum` comparison was mistakenly SHA-1 of the blob content without Git's blob header and is not a valid comparison. The clone used for reading was checked out at the specified base; `git rev-parse HEAD` printed the full base SHA and `git rev-parse --show-toplevel` printed `/fast/scratch/hyaku/kengaku-r48/R48C2ScoutEntry/lane`.

**REV** `a543d92083557dd9b33ee674e9b99b03411f80af` (all entry/capture comparisons below are at this revision).

## Comparison findings

### Capture-grounded teachings: supported

- The entry describes the one pytest function accurately: captured `test_outputs.py:10` defines `test_fibonacci_polyglot`; lines 17–18 check the exact listing before lines 23–25 compile to `/app/polyglot/cmain`; lines 27–44 cover the three fixed points and both subprocess outputs. All lines and values cited in the entry match the pinned capture.
- Captured `test.sh:18–28` supports `uvx`, Python 3.13, pytest 8.4.1, and mapping pytest status to reward `1`/`0`. Captured `task.toml` supports the 900-second verifier timeout, the published image tag, and internet-enabled metadata. Captured `instruction.md` names toolchain versions but the grader capture contains no version assertion. Captured Dockerfile installs gcc; captured README repeats the single-file and fixed-point statements; captured `solve.sh` writes the one polyglot file.
- The source-quote table's 20 located quote rows (including the `Located quotes` table) are substrings of the cited capture lines. Each quote is within the specified 3–25 word bound. The 18 mechanism-table fragments likewise match their cited captured lines. Automated validation printed `substring=True` for every extracted located-quote row (the table header was also counted by the ad-hoc parser and correctly had no source location).
- The 18-case receipt agrees with the frozen dry table on case predictions and tags; receipt output is `regrade cases=18 differ=7` and `cases=18 observed_pass=7 observed_fail=11 mismatches=0`. Requirement-map derivations follow those outcomes: `both-print` and `toolchain` have no violating case, as explicitly called out as unexercised; other labels reflect pass/fail outcomes of their tagged cases. No overreach found in the entry's descriptions of the individual cases, Findings 1–6, or its negative-space/limits disclosures.
- The entry's claim that the grader's three points are not a complete Fibonacci definition is supported by the public fixed-point literals in `test_outputs.py:27`, and its explicit caveat that `f(1)` is named by the request but not tested is correct. Its host-toolchain/no-image/no-agent limits are explicit and consistent with the receipt's stated probe scope.

### Residual overreach: cross-exemplar comparison

1. **Summary, entry lines 34–35:** says the other ten are read-and-assert graders and “none of them executes the graded bytes as a program.” This is false: `tb2-feal-differential-cryptanalysis-grader.md` says the grader imports the agent-authored `/app/attack.py` and calls `attack.attack(feal_in_c.encrypt)`; its assertion depends on that call's returned value. The polyglot entry's own Errata §1 (line 314 onward) explicitly identifies this exact statement as false and gives the narrower accurate distinction (“no earlier exemplar *compiles* the graded artefact or runs the same bytes under two language runtimes”), but the false sentence remains in the Summary. This is a reader-visible residual overclaim.
2. **Finding 7, entry line 183:** says the other eleven exemplars decide from file contents, field values, git objects, or “a task-owned program's output.” The FEAL example instead executes agent-authored Python in the grader and uses its return value; this wording does not preserve the erratum's narrower distinction. The nearby claim about `circuit-fibsqrt` is supported by its entry: it grades `/app/gates.txt` as a data file and compiles its own simulator. The count of 12 TB2 knowledge entries (including this entry) is supported by the frozen directory listing.

The entry's own Errata is valuable mitigation, but it does not remove or replace the inaccurate body sentences. No other overreach was identified in the inspected materials.

## Pin checks and execution record

Commands run (all Git fixture/clone operations were confined to the scratch clone; no mutating fixture command was run):

- `git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin lane`; `git checkout a543d92083557dd9b33ee674e9b99b03411f80af`; `git rev-parse HEAD`; `git rev-parse --show-toplevel`.
- `git ls-tree a543d92083557dd9b33ee674e9b99b03411f80af plans/round-48-claims.md`; `git log -1 --format='%H %ci %s' a543d92083557dd9b33ee674e9b99b03411f80af -- plans/round-48-claims.md`; `git log --oneline a543d920..HEAD -- plans/round-48-claims.md`.
- `(cd corpus/evidence/round46/tb2-polyglot-c-py && sha256sum -c SHA256SUMS)` printed `gitignore: OK`, `README.md: OK`, `Dockerfile: OK`, `instruction.md: OK`, `solve.sh: OK`, `task.toml: OK`, `test.sh: OK`, `test_outputs.py: OK`, `exit=0`.
- `sha256sum plans/polyglot_c_py_probe.py` printed `67a8f4a68fcdf1904484853053e1565f95dce503105732f43102a9e64db85f26`; this matches `plans/pkg-spec-r46.json`. The round-48 claim's `22b7779e…` digest is the separate `.ufo/waves/round-46/w1/R46ExecC3Probe/polyglot_c_py_probe.py` artifact, whose measured hash is exactly `22b7779e6ccbea5f45d4ccb889f8016528932ec37ce345f1fa829e6f02986f1d`; not a mismatch.
- `sha256sum corpus/evidence/round46/polyglot-c-py-probe.txt` printed `dd0e35464bc1b19c692d45a419a33c7bcf2d8fd2753783dd13a54f059531c277`, matching `receipt_sha256` in the spec. `sha256sum plans/pkg_gate.py` printed `ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41`, matching the spec.
- `ls corpus/knowledge/ | grep -c '^tb2-'` printed `12`; total knowledge markdown count printed `53`.
- A read-only Python check extracted the entry's quote table and checked each located quote against the line in the corresponding capture. It printed `substring=True` on all 20 actual quote rows, with each count 3–18 words. No probe, counter, or scored execution was run.

An initial digest check was accidentally run from the lane root although `SHA256SUMS` uses capture-directory-relative names; it failed to open those files. It was rerun from the capture directory and passed as recorded above. No scored run was attempted.

## Sources opened, access date, located quote

All primary capture URLs are immutable commit URLs; accessed 2026-10-27. Each quote is located in the local pinned capture at the indicated line and is at most 25 words.

- S166, `test_outputs.py:27` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test_outputs.py — “test_cases = [(42, "267914296"), (10, "55"), (0, "0")]”
- S167, `test.sh:26` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/tests/test.sh — “echo 1 > /logs/verifier/reward.txt”
- S168, `instruction.md:7` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/instruction.md — “Both of these should print to stdout the kth Fibonacci number”
- S169, `solve.sh:12` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/solution/solve.sh — “cat <<'EOF' > polyglot/main.py.c”
- S170, `Dockerfile:6` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/environment/Dockerfile — “RUN apt update -y && apt install -y gcc”
- S171, `task.toml:34` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/task.toml — “allow_internet = true”
- S172, `README.md:21` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/README.md — “Only `main.py.c` exists in `/app/polyglot/` (single file requirement)”
- Captured `.gitignore` (no SOURCES row), pin in `SHA256SUMS`; its provenance follows the same pinned repository base — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/.gitignore — `gitignore:1-2`: “# Git” / “.git/”.
- FEAL comparison, secondary lane knowledge entry `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` (accessed 2026-10-27; its cited primary capture URL) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/feal-differential-cryptanalysis/tests/test_outputs.py — the opened lane entry locates the import/call at `test_outputs.py:22-30`; quote from its cited grader: “stolen = attack.attack(feal_in_c.encrypt)”.
- Circuit-fibsqrt comparison, secondary lane knowledge entry `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (accessed 2026-10-27; its cited primary capture URL) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/test_outputs.py — the opened lane entry locates its own simulator compile at line 66; quote: `"gcc", "-O3", "/tests/sim.c", "-o", "sim"`.

Other internal sources read: frozen `plans/round-48-claims.md` (entire file) and `corpus/lessons/round-46-verifier-spotcheck.md` (entire file, tool output elided long table fields); capture manifest `plans/pkg-spec-r46.json`; the dry-case freeze and executed receipt; and the two secondary knowledge entries named above. The primary external sources reopened for this scoped task are the immutable URLs listed above.

## Limits

This was a static, read-only comparison at the stage-1 frozen base. I did not re-fetch the upstream URLs, rerun the historical probe, inspect every other lane exemplar, or independently reproduce the receipt. The FEAL/circuit contrast check uses their committed lane knowledge entries; only those cited mechanisms were checked. This report neither scores nor admits C2.
