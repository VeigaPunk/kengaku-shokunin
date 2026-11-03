# Round 65 w1 — seat GraderRecon (read-only reconnaissance for R65-C1)

Seat: `GraderRecon`, leaf, no dispatch, no edits outside this seat dir (plus this report).
Claims of record: `plans/round-65-claims.md` (read in full, base `12a62551`). Host: Arch, kernel
7.2.11, python 3.14.8, gcc/gcov 16.2.1, bwrap 0.13.1, host sqlite3 3.54.0, uv 0.13.0.
Tools installed or upgraded: **none** (all needed binaries present; no pacman, no uv install).
Network opened: exactly the two named opens (raw.githubusercontent.com/harbor-framework/terminal-bench-2
at pin `2fd12b8…`, and sqlite.org/2026/sqlite-amalgamation-3540100.zip). No port bound by this seat.

## Verdicts

| check | observed | verdict |
|---|---|---|
| S232 live re-open at pin | sha256 `b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b`, 2166 B, `cmp` vs round52 grader **rc 0** | **MATCH** |
| S232 vs `SHA256SUMS` line 167 | line 167 byte-equal to the computed sha | **MATCH** |
| S233 live re-open | sha256 `0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9`, 2990966 B, `cmp` vs `W/sqlite-amalgamation-3540100.zip` **rc 0** | **MATCH** |
| S233 integrity + identity | `unzip -t` all 5 members OK; `sqlite3.h:149` `#define SQLITE_VERSION "3.54.1"` | **OK, 3.54.1** |
| host state | as in the claims' Known facts (3.54.0 / 16.2.1 / 16.2.1 / 0.13.1 / 3.14.8 / 0.13.0) | **MATCH** |
| no-bind | no socket created by this seat; `ss -ltn` lists host listeners only | **recorded** |

## Step 1 — S232 re-open (grader at the pin)

```
$ curl -sS -f -o test_outputs.py.live https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/sqlite-with-gcov/tests/test_outputs.py   # rc 0
$ sha256sum test_outputs.py.live
b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b  test_outputs.py.live
$ sha256sum /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py
b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b  …/sqlite-with-gcov/tests/test_outputs.py
$ cmp <committed> test_outputs.py.live          # cmp_rc=0 IDENTICAL, 2166 B both sides
```
Receipt: `GraderRecon/sha-verdict.txt`; bytes kept at `GraderRecon/test_outputs.py.live`;
SHA256SUMS cross-check at `GraderRecon/sha256sums-crosscheck.txt`. The three functions appear in file
order at lines 8 / 21 / 36, stdlib imports only, no `conftest.py` at the pin (both probed paths 404).

**Located quotes (S232, ≤25 words each, pin `2fd12b8`):**
- L25: `assert sqlite_path is not None, "sqlite3 not found in PATH"` (9 words)
- L50–52: `assert len(gcda_files) > 0, ("No .gcda files found, gcov instrumentation may not be enabled")`
- L59–61: `assert len(gcno_files) > 0, ("No .gcno files found, gcov instrumentation may not be enabled")`

## Step 2 — S233 re-open (amalgamation)

```
$ curl -sS -f -o sqlite-amalgamation-3540100.live.zip https://sqlite.org/2026/sqlite-amalgamation-3540100.zip   # rc 0
$ sha256sum <live>            -> 0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9
$ sha256sum W/sqlite-amalgamation-3540100.zip -> same
$ cmp <live> W/sqlite-amalgamation-3540100.zip  # cmp_rc=0 IDENTICAL, 2990966 B both
$ unzip -l  -> 5 entries: sqlite3.c 9582521, shell.c 1270623, sqlite3.h 695729, sqlite3ext.h 39547
$ unzip -t  -> No errors detected in compressed data
$ unzip -p … sqlite3.h | grep -n 'define SQLITE_VERSION' -> 149:#define SQLITE_VERSION        "3.54.1"
$ unzip -p … sqlite3.h | grep -n 'define SQLITE_SOURCE_ID' -> 151:"2026-10-16 14:45:20 555e07ef33f69a0957d24d8e555b702464a131d6f1607f4c3c1e4551e8e6ca76"
```
Receipt: `GraderRecon/amalgamation-listing.txt`. **Retention note:** `W/sqlite-amalgamation-3540100.zip`
is git-tracked and not gitignored (`git ls-files --error-unmatch` rc 0, `git check-ignore` rc 1), so
the byte-identical live copy was deleted after the sha/cmp/`unzip -l`/`unzip -t`/version receipts were
written — keeping a second 3 MB identical blob adds no evidence and the cmp already proves identity.
The version strings above are the attribution witness that the candidate answers `3.54.1` while the
host answers `3.54.0` (`be8d059e…`), i.e. the G1 capture's `sqlite3_version 3.54.1` is the lane build.

**Located quote (S233, artifact at the pinned sha):** `#define SQLITE_VERSION        "3.54.1"`
(`sqlite-amalgamation-3540100/sqlite3.h:149`, source id `555e07ef…`, 2026-10-16).

## Step 3 — host state

`GraderRecon/host-state.txt`, commands and first lines as run: `sqlite3 --version` → 3.54.0
2026-10-09 (`…alt1`); `gcc --version` → gcc (GCC) 16.2.1 20260810; `gcov --version` → gcov (GCC)
16.2.1 20260810; `bwrap --version` → bubblewrap 0.13.1; `python3 --version` → Python 3.14.8;
`uv --version` and `/home/vgpnk/.local/bin/uv --version` → uv 0.13.0; `which -a sqlite3 gcc gcov bwrap
python3` → all under `/usr/bin`. `ss -ltn` shows host listeners (1234, 5355, 631, …) — none owned by
this seat and none opened by the grader, whose only imports are `os`, `shutil`, `subprocess`.

## Step 4 — leg reading (`GraderRecon/recon/leg-reading.md`)

One paragraph per leg with the exact PASS condition and line anchors, plus four ambiguity flags:

1. **The grader's own run regenerates `.gcda`** (L40 before the L47 walk). `.gcda` is written at exit
   to the *compile-time absolute* dir, so leg-3 `P` does not prove the file pre-existed; only the
   `.gcno` assert proves build-time instrumentation. A binary compiled in host dir `X` but reachable
   only at `/app/sqlite` emits nothing if `X` is absent/read-only inside the sandbox → compliant G1
   would read `P P F`. The claims' in-place compile + dual bind (`/app` **and** host path, writable) is
   load-bearing and the receipt must print per case the compile dir and the emitted `.gcda`/`.gcno`
   lists, else leg-3 `P` stays unattributable.
2. **`os.walk` on a missing `/app/sqlite` is silent**: measured `list(os.walk(...)) == []`, rc 0, while
   `os.listdir` on the same path raises `FileNotFoundError` (`GraderRecon/mechanism-extra.txt`). Absent,
   empty, and missing `/app/sqlite` are indistinguishable to the grader — all three fail at L50 with
   the same `No .gcda files found` message. G5's mechanism is precisely this silence.
3. **Masked-file `PermissionError` is an exception, not a failed assert**: `/dev/null` is `crw-rw-rw-`
   (0666) so `shutil.which` fails `X_OK` → `None` (isolated-PATH check: `which_sqlite3 = None`) and leg
   2 fails as `AssertionError` "sqlite3 not found in PATH"; direct exec of the same file raises
   `PermissionError [Errno 13]` (`GraderRecon/masking-mechanism.txt`) so legs 1 and 3 die as exceptions.
   Therefore (i) the receipt must record exception **class + message head** per leg, not a bare `F`, or
   G2's `F F F` is indistinguishable in kind from G3/G4/G5; and (ii) **leg isolation is mandatory** —
   `pytest` is NOT importable from `/usr/bin/python3` (`ModuleNotFoundError`, rc 1,
   `GraderRecon/mechanism-extra.txt`), so a driver that calls the three functions straight-line loses
   legs 2–3 when leg 1 raises, and G2 would never yield its predicate-required leg-2 fragment. Per-leg
   `try/except` (or one subprocess per leg) is required; "one sandbox process per case" is compatible
   only with per-function `try/except`, and the receipt should say which was used.
4. **Order is definition order** (8/21/36, no conftest at the pin), so the setup drift check should
   compare the ordered name list `[test_sqlite_compiled, test_sqlite_in_path, test_gcov_enabled]`, not
   just a count of three.

## Remaining unknowns (not decidable from this seat's scope)

- Whether the probe driver isolates legs (per-function `try/except` vs per-leg subprocess) — the probe
  is written in this wave, not here; flag 3(iii) is the requirement to check against.
- Whether the receipt prints each case's compile dir and emitted coverage-file lists (flag 1).
- `raw.githubusercontent.com` cannot list directories: a *differently named* injection file at the pin
  (e.g. `pytest.ini`) was not enumerated. Immaterial here because pytest is absent and the driver is
  the probe's own, but stated rather than assumed.
- The TB2 task's `solution.sh`/`Dockerfile` were not fetched (not named in this seat's item); the
  predicate is defined by the grader bytes alone, which are sha-pinned and byte-verified above.

## Files written

- `.ufo/waves/round-65/w1/GraderRecon.md` (this report)
- `.ufo/waves/round-65/w1/GraderRecon/{sha-verdict.txt, sha256sums-crosscheck.txt, amalgamation-listing.txt, host-state.txt, masking-mechanism.txt, mechanism-extra.txt, conftest-probe.txt, test_outputs.py.live}`
- `.ufo/waves/round-65/w1/GraderRecon/recon/leg-reading.md`
