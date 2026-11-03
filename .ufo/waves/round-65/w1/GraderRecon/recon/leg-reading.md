# Leg reading — `sqlite-with-gcov/tests/test_outputs.py` at TB2 pin `2fd12b8`

Source of every claim below: the committed bytes at
`corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py`,
sha256 `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b`, 2166 bytes — byte-identical
to the live re-fetch at the pin (`cmp` rc 0, `sha-verdict.txt`). Line numbers are the file's own.
Module imports `os`, `shutil`, `subprocess` only; no fixture, no `conftest.py` (probe of
`sqlite-with-gcov/tests/conftest.py` and `sqlite-with-gcov/conftest.py` at the pin → HTTP 404,
`conftest-probe.txt`). Three functions, definition order = file order, lines 8, 21, 36.

## Leg 1 — `test_sqlite_compiled` (lines 8–18)

PASS iff `subprocess.run(["sqlite3", ":memory:", "SELECT sqlite_version();"], capture_output=True,
text=True)` returns `returncode == 0` (line 17) **and** `len(result.stdout.strip()) > 0` (line 18).
There is no `shutil.which` pre-check and no exception guard: any exec failure leaves the function as
an exception, not as an assert. Three surfaces are therefore distinguishable and must be recorded by
kind — `PermissionError [Errno 13]` when the PATH entry exists but is not executable (the masked
`/dev/null` case, confirmed at `masking-mechanism.txt`), `FileNotFoundError [Errno 2]` when no PATH
entry resolves, and `AssertionError` when the process ran but exited non-zero or printed nothing. The
non-empty-stdout clause is separately load-bearing: `SELECT sqlite_version();` prints one version
line, so a zero-exit/no-output wrapper fails leg 1 while a real binary passes; conversely the printed
version is the only per-leg witness of *which* binary answered (G1's pre-freeze capture records
`3.54.1` from the lane build against the host's `3.54.0`).

## Leg 2 — `test_sqlite_in_path` (lines 21–33)

PASS iff `shutil.which("sqlite3") is not None` (line 24, asserted line 25 with the fragment
`sqlite3 not found in PATH`) **and** `subprocess.run(["sqlite3", ":memory:", "SELECT 1;"])` returns
`returncode == 0` (line 33). `which` never executes anything: it walks `PATH` and accepts the first
entry whose target satisfies `os.access(..., os.X_OK)`. `/dev/null` is `crw-rw-rw-` octal `666`
(`host-state.txt` / `masking-mechanism.txt`), so the `X_OK` test fails, `which` skips the masked
entry, and with no further `sqlite3` on `PATH` it returns `None` — measured directly under an
isolated `PATH` containing only the masked entry: `which_sqlite3 = None`. That is the exact
mechanism behind G2's leg-2 `F`. Two cautions: the converse does not hold — an entry that is
`X_OK` but not `execve`-able passes `which` and then dies at line 33 (or raises), so "`which`
non-`None`" is not evidence of a working candidate; and `which` returning `None` is the *only* leg
whose failure is an `AssertionError` rather than an exception in the masked case, which is why the
frozen G2 predicate names this fragment.

## Leg 3 — `test_gcov_enabled` (lines 36–61)

PASS iff, in this order: (a) the grader's own `subprocess.run(["sqlite3", ":memory:", "SELECT 1;"])`
returns 0 (line 43, unguarded — any exception escapes here and no walk is ever reached); (b)
`os.walk("/app/sqlite")` accumulates ≥1 path ending `.gcda` (lines 47–48) and the assert at line 50
holds, whose message is `No .gcda files found, gcov instrumentation may not be enabled`; (c) a second
`os.walk("/app/sqlite")` accumulates ≥1 path ending `.gcno` (lines 56–57) and the assert at line 59
holds, message `No .gcno files found, gcov instrumentation may not be enabled`. The two asserts are
sequential, so exactly one message is printed per failing case: a build with `.gcno` but no `.gcda`
(G3, and G5's host binary) fails at line 50 and a build with `.gcda` but no `.gcno` (G4's arcs-only
build) fails at line 59 — the fragment is a mechanism fingerprint, not decoration. (a) precedes both
walks, so a masked or absent binary yields `PermissionError` / `FileNotFoundError` here instead of an
assert, which is why G2's leg 3 is `F` *without* either fragment.

## Flags — what could make a frozen vector cell ambiguous

1. **The grader's own run regenerates `.gcda` (load-bearing, must not be "simplified").** Line 40
   executes the instrumented binary *before* the walk. libgcov writes `.gcda` at process exit to the
   absolute directory recorded at compile time, so if that directory is writable inside the sandbox,
   the grader's own invocation — and leg 1's, and leg 2's — create the very files leg 3 asserts on.
   Two consequences. First, "P on the `.gcda` assert" does not prove `.gcda` existed before the
   grader ran; only the `.gcno` assert (a compile-time artifact never written at run time) proves the
   build was instrumented. Second, the dual bind is essential: a binary compiled in host dir `X` but
   reachable only at `/app/sqlite` inside the sandbox writes nothing when `X` is absent or read-only
   (libgcov fails silently, no `.gcda`), so a compliant G1 build would land `P P F`. The claims' rule
   — compile in place per case, bind the case dir at **both** `/app` and its host path, both writable
   — is what makes G1 `P P P` attributable; a receiving seat must keep it and the receipt must print,
   per case, the compile dir and the emitted `.gcda`/`.gcno` file list (otherwise leg-3 `P` is
   unattributable between "candidate build" and "grader's own run").

2. **`os.walk` on a missing `/app/sqlite` is silent, not an error.** Measured on this host's
   `/usr/bin/python3`: `list(os.walk("/app/sqlite-does-not-exist-65"))` → `[]`, function returns
   normally, rc 0; the contrast `os.listdir` on the same path raises `FileNotFoundError`
   (`mechanism-extra.txt`). With no `onerror` callback the grader cannot tell an empty `PATH`-absent
   `/app` from an existing but empty `/app/sqlite` from a missing one: all three fall through to the
   line-50 assert with the identical `No .gcda files found` message. That is exactly why G5 (`P P F`,
   host binary answering both exec legs, empty `/app`) and G2's environment must be separated by the
   leg-1/2 exception *kind*, not by leg 3.

3. **The masked-file `PermissionError` surface is an exception, not a failed assert.** With
   `--ro-bind /dev/null /usr/bin/sqlite3`, legs 1 and 3 raise `PermissionError [Errno 13]` out of
   `subprocess.run` (measured without bwrap by exec'ing a symlink to `/dev/null`: same errno,
   `masking-mechanism.txt`), while leg 2 returns `None` from `which` and fails as `AssertionError`.
   Two requirements follow for the probe. (i) The per-leg rule "P iff the function returns normally,
   F on any exception" is the only classifier that keeps `F F F` honest, and the receipt must record
   the exception **class plus message head** per leg; a bare `F` makes G2's `PermissionError` legs
   indistinguishable from G3/G4/G5's `AssertionError` legs. (ii) **Leg isolation is mandatory**:
   `pytest` is not importable from the sandbox interpreter (`import pytest` →
   `ModuleNotFoundError`, rc 1, `mechanism-extra.txt`), so a driver that imports the module and calls
   the three functions straight-line loses legs 2–3 the moment leg 1 raises — G2 would then never
   yield the leg-2 `sqlite3 not found in PATH` fragment its predicate demands. Each leg needs its own
   `try/except` (or its own subprocess). The claims' "one sandbox process per case" is compatible
   only with per-function `try/except`; the receipt should state which it used.

4. **Leg order is definition order, and it is observable.** Lines 8 / 21 / 36; no `conftest.py` at
   the pin (both probed paths 404), stdlib-only imports, so nothing at that path reorders or
   parametrizes. A `def test_` order drift check (as the claims' exit-2 setup refusal requires) should
   compare the ordered list `[test_sqlite_compiled, test_sqlite_in_path, test_gcov_enabled]` extracted
   from this sha, not just a count of three.
