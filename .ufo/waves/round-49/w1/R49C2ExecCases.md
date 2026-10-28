# R49C2ExecCases — R49-C2 V7 case-table repair (both-print + toolchain violating cases)

seat: R49C2ExecCases (executor) · round 49 · hyaku run 10 · lane repo `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
item: author the amended case table so `both-print` and `toolchain` each carry >=1 committed violating case
(probe CASES extended in a scratch copy, `--dry` printed, all 7 tags verified). No admission is claimed here.

## 1. Axes named

- **coverage** — R49-C2, the frozen V7 repair leg (`.ufo/... plans/round-49-claims.md` §C2 (a)): a frozen tag with no
  violating case is an unsatisfiable leg (round-48 routed defect 3; `corpus/lessons/round-48-verifier-spotcheck.md`
  §2 R48-C2: "`both-print` and `toolchain` have **NONE**"). No other axis is touched; no C1 file is read or written.

## 2. Freeze precondition (stage-1 commit exists and predates the measurement)

Measured revision, printed by git in the lane:

```
$ git log -1 --format='%H %ci %an %s' 9d2900af41e4d1fc6022eff99010436fde6dbd93
9d2900af41e4d1fc6022eff99010436fde6dbd93 2026-10-28 09:14:40 -0300 kengaku-shokunin round-49: stage-1 freeze of C1 (fence over-refusal, v3 counter + mutant floor) and C2 (TB2 grader admission, Q40 counter, receipt ordering) claims
```

Lane porcelain before any work (`git status --porcelain`): only `?? .ufo/waves/round-49/w1.ready.partial` and
`?? .ufo/waves/round-49/w1/` — wave scaffolding, no tracked-file edit. Lane HEAD at that moment was
`af88aab193e6034cb9b386472064e3c18fa90128`, a descendant of the freeze; every run below was made in a clone checked
out **at** the freeze commit, so the freeze predates the measurement.

**REV 9d2900af41e4d1fc6022eff99010436fde6dbd93** (clone at the frozen base, `git -C probe-clone rev-parse
--show-toplevel` → `/fast/scratch/hyaku/kengaku-r49/R49C2ExecCases/probe-clone`, `rev-parse HEAD` → the same 40-hex).
**TREE-BYTES 36398** = the measured inputs of the two permitted runs: `plans/polyglot_c_py_probe.py` 29360 B (amended,
uncommitted; sha256 `f6a543bee132ba3dc5f41f37e771b67b22e13250e4b3c22387c467b21ce83be0`) + the capture dir
`corpus/evidence/round46/tb2-polyglot-c-py/` 7038 B.

Ordering rule (Q30) honoured: **no full probe run and no counter run was made**. Only `--dry` and `--stage-check`,
the two pre-receipt operations the claims allow.

## 3. What was changed (scratch-only candidate; L1 transcribes/lands)

Candidate file: `probe-clone/plans/polyglot_c_py_probe.py` (clone at REV 9d2900af, single file modified).

1. **New case `both-print-c-silent`** — `Case("both-print-c-silent", "F", "F", ("both-print",), …)`:
   `recipe=emit(poly(c="    (void)a;  /* C side: no printf, nothing on stdout */"))`. The python3 side is the
   template's `print(fib(_k))` (correct for every graded N); the C side compiles, returns 0 and writes nothing to
   stdout. Grounding: captured grader `test_outputs.py:44` is
   `assert python_out == expected and c_out == expected, (` — the C stdout is compared, so an empty C stdout fails
   the test while the python3 run matched. Predicted `tests=F`, `regrade=same` (the first grade's own gcc writes
   `cmain`, so the second grade fails on `test_outputs.py:17-20`'s listing).
2. **New case `toolchain-c23-bool`** — `Case("toolchain-c23-bool", "P", "F", ("toolchain",), …)`:
   `recipe=emit(poly(c='    bool emit = true;\n    if (emit) {\n        printf("%llu\\n", a);\n    }'))`. The C side
   declares `bool`/`true` with no `#include <stdbool.h>`: C23 makes both keywords, so this host's gcc default
   (`-std=gnu23`, `__STDC_VERSION__ 202311L`) builds it and it prints the right value, while the documented gcc
   13.2.0 default dialect (`-std=gnu17`, `__STDC_VERSION__ 201710L`) rejects it — predicted to fail the documented
   toolchain contract. Predicted host verdict `tests=P`, `regrade=DIFF:F`.
3. **Docstring limits sentence amended** so the now load-bearing divergence is disclosed, not silent: the named
   gcc-version divergence previously said only "warnings do not decide the verdict"; it now also says the newer
   gcc's C23 default dialect *does* decide `toolchain-c23-bool`, whose predicted verdict is this host's and is the
   opposite under gnu17.

No tag name in `TAGS` was re-worded; no existing case was re-worded, re-predicted or reordered (both new cases
append after `value-plus-line`).

## 4. Commands run and observed output

### 4.1 `--dry` (amended table)

```
$ cd /fast/scratch/hyaku/kengaku-r49/R49C2ExecCases/probe-clone
$ TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2ExecCases python3 plans/polyglot_c_py_probe.py --lane . --dry
rc=0
…
CASE both-print-c-silent predicted=fail tests=F regrade=same violates=both-print end=recipe -- a valid polyglot whose python3 side prints the right value for every graded N while its C side compiles, returns 0 and writes nothing to stdout (the printf is replaced by a discarded-value statement): instruction.md:7 requires both runtimes to print, and the grader fails on the empty C stdout even though the python3 run matched - the C side's silence is the violation, which no earlier case made observable
CASE toolchain-c23-bool predicted=pass tests=P regrade=DIFF:F violates=toolchain end=recipe -- a correct polyglot whose C side declares `bool emit = true;` without #include <stdbool.h>: C23 makes bool a keyword, so this host's gcc default (-std=gnu23) compiles it and it prints the right value, while the image's gcc 13.2.0 default (-std=gnu17) rejects the type as an unknown name - the verdict turns on a toolchain the instruction fixes at gcc 13.2.0 / python 3.12.3 and the grader never checks
cases=20 predicted_pass=8 predicted_fail=12
```

Full 28-line table: `w1/R49C2ExecCases/polyglot-c-py-dry-cases.txt` (6355 B, sha256
`905e04a1aa0434275b27d6cb1a910ce5a17d0c7fbc102b54b1fadb168189d944`); transcribed in §6.

### 4.2 Tag coverage tally (all 7 tags, computed from the dry table above)

```
$ python3 - <<'EOF'   # tally violates= tokens per TAG line of the dry output
…
single-file  cases=4
python-run   cases=1
c-build      cases=2
both-print   cases=1
fib-kth      cases=4
stdout-only  cases=1
toolchain    cases=1
all7covered = True tags = 7
EOF
```

### 4.3 `--stage-check` (permitted pre-receipt control, 20 cases)

```
$ TMPDIR=/fast/scratch/hyaku/kengaku-r49/R49C2ExecCases python3 plans/polyglot_c_py_probe.py --lane . --stage-check
rc=0
STAGECHECK both-print-c-silent rc=0 expect=src file=bytes=522 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
STAGECHECK toolchain-c23-bool rc=0 expect=src file=bytes=538 dir=main.py.c pycheck=ok ccheck=ok cwarn=1 match=yes
stagecheck cases=20 failed=0
```

Full output: `w1/R49C2ExecCases/stagecheck-amended.txt`. The pre-existing 18 rows are byte-identical in shape to the
round-46 freeze (no case regressed); `cwarn=1` is the polyglot skeleton's own `#define pgtail """` warning, which the
control case `oracle-solve-sh` also carries. No prlimit is used by this base revision, so the round-48
`RLIMIT_NPROC=48` failure mode does not appear; bwrap created every sandbox under this host's uid thread load.

### 4.4 Toolchain-divergence evidence for `toolchain-c23-bool` (compiler facts, not a case verdict)

Rendered source (from the recipe, `w1/R49C2ExecCases/toolchain-c23-bool.py.c`, sha256 `4ba7293d…`, 538 B) and the
verbatim transcript in `w1/R49C2ExecCases/gcc-gnu17-divergence.txt`:

```
$ gcc -fsyntax-only toolchain-c23-bool.py.c            # host default: __STDC_VERSION__ 202311L
rc=0
$ gcc -std=gnu17 -fsyntax-only toolchain-c23-bool.py.c  # gcc 13.2.0 default dialect
toolchain-c23-bool.py.c:21:5: error: unknown type name ‘bool’
toolchain-c23-bool.py.c:21:17: error: ‘true’ undeclared (first use in this function)
rc=1
$ gcc -std=gnu17 -fsyntax-only control-plain.py.c       # plain correct polyglot, same dialect
rc=0
$ gcc -std=gnu17 -fsyntax-only both-print-c-silent.py.c
rc=0
```

The rejection is isolated to the two C23 tokens: the same dialect accepts a plain correct polyglot
(`control-plain.py.c`, sha256 `251a9b6b…`) and the other new case (`both-print-c-silent.py.c`, sha256 `621c46a1…`).

## 5. Transcribed CASES diff (`cases.diff`, 3059 B, against REV 9d2900af)

```diff
@@ -48,8 +48,10 @@ (docstring limits)
-verdict); the task image is never pulled and its `apt install gcc` is not replayed (the sandbox binds host /usr; gcc
-and python3 are checked before any case); pytest is not run; recipes run as the probing user, not root; no network;
+verdict, but the newer gcc's C23 default dialect does decide `toolchain-c23-bool` - its predicted verdict is this
+host's, and under gcc 13.2.0's gnu17 default it is the opposite); the task image is never pulled and its
+`apt install gcc` is not replayed (the sandbox binds host /usr; gcc and python3 are checked before any case);
+pytest is not run; recipes run as the probing user, not root; no network;
@@ -287,6 +289,18 @@ (CASES tail)
+    Case("both-print-c-silent", "F", "F", ("both-print",),
+         "a valid polyglot whose python3 side prints the right value for every graded N while its C side compiles, "
+         "returns 0 and writes nothing to stdout (the printf is replaced by a discarded-value statement): "
+         "instruction.md:7 requires both runtimes to print, and the grader fails on the empty C stdout even though "
+         "the python3 run matched - the C side's silence is the violation, which no earlier case made observable",
+         recipe=emit(poly(c="    (void)a;  /* C side: no printf, nothing on stdout */"))),
+    Case("toolchain-c23-bool", "P", "F", ("toolchain",),
+         "a correct polyglot whose C side declares `bool emit = true;` without #include <stdbool.h>: C23 makes bool "
+         "a keyword, so this host's gcc default (-std=gnu23) compiles it and it prints the right value, while the "
+         "image's gcc 13.2.0 default (-std=gnu17) rejects the type as an unknown name - the verdict turns on a "
+         "toolchain the instruction fixes at gcc 13.2.0 / python 3.12.3 and the grader never checks",
+         recipe=emit(poly(c='    bool emit = true;\n    if (emit) {\n        printf("%llu\\n", a);\n    }'))),
 ]
```

The verbatim unified diff (with headers, index `f384711..b5a28f2`) is `w1/R49C2ExecCases/cases.diff`; apply it with
`git apply` in a lane clone at the freeze (it is a scratch-candidate diff, not a commit).

## 6. New dry table — stage-2 target `corpus/evidence/round49/polyglot-c-py-dry-cases.txt`

```
TAG single-file instruction.md:1
TAG python-run instruction.md:3
TAG c-build instruction.md:5
TAG both-print instruction.md:7
TAG fib-kth instruction.md:7
TAG stdout-only instruction.md:7
TAG toolchain instruction.md:9
CASE nop predicted=fail tests=F regrade=same violates=single-file end=absent -- the image seed only: WORKDIR /app exists, /app/polyglot does not - os.listdir raises FileNotFoundError before any assert
CASE oracle-solve-sh predicted=pass tests=P regrade=DIFF:F violates= end=recipe -- the task's published solution/solve.sh run verbatim with cwd /app (it creates polyglot/ relatively): a real polyglot whose Fibonacci loop both runtimes run
CASE lookup-table predicted=pass tests=P regrade=DIFF:F violates=fib-kth end=recipe -- a polyglot that hardcodes the three graded outputs, read out of the PUBLIC tests/test_outputs.py at recipe time and turned into a print table: the grader has exactly three fixed points and never inspects the source, so a lookup table is indistinguishable from computing
CASE python-only predicted=fail tests=F regrade=same violates=c-build end=recipe -- valid Python that is not C (a plain import/def/raise program): python3 runs it, gcc fails with a parse error and check=True raises CalledProcessError
CASE c-only predicted=fail tests=F regrade=same violates=python-run end=recipe -- valid C that is not Python (no # comment line, no Python expression): gcc builds it and it prints the right value, python3 aborts with a SyntaxError before the first expected value is compared
CASE extra-file predicted=fail tests=F regrade=same violates=single-file end=recipe -- the oracle polyglot plus one unrelated file (NOTES.md) in /app/polyglot: the listing assert compares the whole list to ["main.py.c"], so a harmless extra file fails before gcc runs
CASE leftover-cmain predicted=fail tests=F regrade=same violates=single-file end=recipe -- the oracle polyglot plus the binary that instruction.md:5 itself tells the agent to build (`gcc ... -o /app/polyglot/cmain && ./cmain N`): following the instruction leaves the second entry the grader's listing forbids - instruction and grader contradict each other
CASE wrong-value predicted=fail tests=F regrade=same violates=fib-kth end=recipe -- a real polyglot whose f(42) is off by one (both runtimes print fib(n)+1 when N is 42): the value, not the shape, decides; the C loop also writes cmain, so the re-grade is what the listing sees
CASE trailing-ws predicted=pass tests=P regrade=DIFF:F violates= end=recipe -- a correct polyglot that pads its output with leading and trailing spaces and blank lines in both runtimes: the grader compares stdout.strip(), which erases whitespace on both ends
CASE nonzero-exit predicted=fail tests=F regrade=same violates= end=recipe -- a correct polyglot that prints the right value and then exits non-zero (python sys.exit(3) / C return 3): the grader runs both runtimes with check=True, so a non-zero status fails a run whose stdout matched - the instruction never says the exit status must be 0
CASE stderr-noise predicted=pass tests=P regrade=DIFF:F violates= end=recipe -- a correct polyglot that also writes to stderr in both runtimes (python print(..., file=sys.stderr), C fprintf(stderr, ...)): the grader captures stderr and compares only stdout, so noise is invisible
CASE n-parsed-differently predicted=fail tests=F regrade=same violates=fib-kth end=recipe -- a polyglot whose two sides read N differently - Python int(argv[1]), C the first digit only (argv[1][0]-'0') - so 42 and 10 disagree while 0 happens to match; no case proves both runtimes parsed N
CASE compile-warning predicted=pass tests=P regrade=DIFF:F violates= end=recipe -- a correct polyglot carrying an explicit `#warning` line (a Python comment, a C preprocessing warning): gcc exits 0 with a diagnostic on stderr, and check=True only reads the exit status
CASE regrade-same-state predicted=pass tests=P regrade=DIFF:F violates=single-file end=recipe -- the oracle's end state, graded and then graded again: the first grade's own gcc writes /app/polyglot/cmain, so the same untouched state fails the second time - the grader is not idempotent (this row is the deliberate re-grade of oracle-solve-sh's state; the per-case `regrade` column is its measurement)
CASE empty-file predicted=fail tests=F regrade=same violates=fib-kth end=recipe -- a zero-byte /app/polyglot/main.py.c: the listing passes, python3 prints nothing, and gcc links nothing with a main - both runtimes are wrong before any value is compared
CASE dir-in-place predicted=fail tests=F regrade=same violates=c-build end=recipe -- a DIRECTORY at /app/polyglot/main.py.c: the listing is exactly ["main.py.c"] so the precondition passes, then gcc is handed a directory and check=True raises CalledProcessError
CASE crlf-source predicted=pass tests=P regrade=DIFF:F violates= end=recipe -- a correct polyglot whose whole source uses CRLF line endings: CPython's tokenizer and gcc both accept CRLF, so the newline style of the source is invisible to this grader
CASE value-plus-line predicted=fail tests=F regrade=same violates=stdout-only end=recipe -- a polyglot that prints the right value followed by a second line of output in both runtimes: strip() trims only the ends, so the compared string is two lines and no case fires the equality
CASE both-print-c-silent predicted=fail tests=F regrade=same violates=both-print end=recipe -- a valid polyglot whose python3 side prints the right value for every graded N while its C side compiles, returns 0 and writes nothing to stdout (the printf is replaced by a discarded-value statement): instruction.md:7 requires both runtimes to print, and the grader fails on the empty C stdout even though the python3 run matched - the C side's silence is the violation, which no earlier case made observable
CASE toolchain-c23-bool predicted=pass tests=P regrade=DIFF:F violates=toolchain end=recipe -- a correct polyglot whose C side declares `bool emit = true;` without #include <stdbool.h>: C23 makes bool a keyword, so this host's gcc default (-std=gnu23) compiles it and it prints the right value, while the image's gcc 13.2.0 default (-std=gnu17) rejects the type as an unknown name - the verdict turns on a toolchain the instruction fixes at gcc 13.2.0 / python 3.12.3 and the grader never checks
cases=20 predicted_pass=8 predicted_fail=12
```

## 7. V7 repair status per frozen tag

| tag | violating case id(s) | host predicted | note |
|---|---|---|---|
| single-file | `nop`, `extra-file`, `leftover-cmain`, `regrade-same-state` | fail ×4 (only `regrade-same-state` passes first) | unchanged |
| python-run | `c-only` | fail | unchanged |
| c-build | `python-only`, `dir-in-place` | fail | unchanged |
| both-print | **`both-print-c-silent`** | fail | **new** — C side silent, python3 prints |
| fib-kth | `lookup-table` (pass), `wrong-value`, `n-parsed-differently`, `empty-file` | mixed | unchanged |
| stdout-only | `value-plus-line` | fail | unchanged |
| toolchain | **`toolchain-c23-bool`** | pass on host, fail under gcc 13.2.0 | **new** — C23 keyword reliance |

Both previously empty tags now carry at least one case whose `violates=` token is the tag, and every cited id is a
`[a-z0-9_-]+` case id in the amended table (matching `R49C2ScribeEntry`'s requirement-map citation rule; the ids and
predictions were sent to that seat on request).

## 8. Sources opened (URL, access date, located quote)

No URL was opened by this seat. The grader text read is the **committed capture**
`corpus/evidence/round46/tb2-polyglot-c-py/test_outputs.py` in the clone at REV `9d2900af…` (pin digest
`b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec`, checked by the probe before any run). Located
quotes (≤25 words): `test_cases = [(42, "267914296"), (10, "55"), (0, "0")]` (line 27) and
`assert python_out == expected and c_out == expected,` (line 44). The claims' S166 URL was not re-fetched here.

## 9. Limits

- **Predictions are not observations.** Under the Q30 ordering rule no full probe run was made, so the two new cases'
  grade-path outcomes are predictions derived from the captured asserts; `--stage-check` proves only end-state shape
  (`file=bytes=…`) and parse-only checks (`pycheck`, `ccheck`).
- **Toolchain divergence is emulated, not replayed.** The host is gcc 16.2.1 / python 3.14.8; `gcc 13.2.0`'s default
  dialect is reproduced as `-std=gnu17` (`__STDC_VERSION__ 201710L`). `toolchain-c23-bool`'s documented-toolchain
  verdict (compile error → fail) therefore rests on that emulation plus GCC's documented default-std change in GCC 15,
  not on a 13.2.0 binary on this host.
- `regrade` for the new cases (`same` / `DIFF:F`) follows the same listing-broken-by-first-grade mechanism as the
  frozen rows; it is reported, never used for the verdict.
- The round-49 C2 counter (`plans/round49_c2_verify.py`) does not exist at the freeze; whether its V7 implementation
  reads this table, and how it weighs a *passing* `toolchain` case, is that seat's/L1's call — I did not author or
  verify it.
- Scratch `/fast/scratch/hyaku/kengaku-r49/R49C2ExecCases` was removed before yield (artifacts first copied here);
  no `/tmp` path is cited.
- No tool was installed or upgraded; nothing in `~/.local/bin`, the fleet root, or the lane tracked tree was written
  (only this report and the artifact dir under `.ufo/waves/round-49/w1/`).

## 10. Risks / blockers

- If the stage-2 probe lands without both `Case` rows, V7 still fails (the repair is the diff in §5, not the report).
- A counter that requires a *failing* case for every tag would reject `toolchain-c23-bool` (host predicted pass).
  Mitigation if L1 wants a failing toolchain row: the same source with `printf` removed *and* `bool` used would fail
  on host for the both-print reason too — but that double-tagging would blur the leg, so it was not done.
- `both-print-c-silent`'s C side is intentionally assertion-fodder (`(void)a;`); if the entry requirement map needs a
  named instruction line for it, `instruction.md:7` is the line the `both-print` tag already cites.
- No blockers: the item is complete as specified.

VERDICT: **complete (candidate, not an admission)** — `both-print` and `toolchain` each gain one violating case with
distinct mechanisms; amended `--dry` prints `cases=20`, all 7 tags covered; `--stage-check cases=20 failed=0`;
R49-C2 admission remains unclaimed and is L1's to score.
