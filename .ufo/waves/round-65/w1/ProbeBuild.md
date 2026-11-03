# ProbeBuild — R65-C1 instrument (round 65, w1)

Seat: `ProbeBuild` (build lane). Scope: build and run the R65-C1 offline probe of the
pinned TB2 `sqlite-with-gcov` grader. Claim rules are frozen in
`kengaku-shokunin/plans/round-65-claims.md`; this seat changed none of them.

## Deliverables

| artifact | path | sha256 |
|---|---|---|
| probe | `kengaku-shokunin/.ufo/waves/round-65/w1/ProbeBuild/round65_c1_sqlite_probe.py` | `f44b72834d8662cb6986e192dfbdf236daf6c99a174768294e504f7b634db4eb` |
| receipt of record | `kengaku-shokunin/.ufo/waves/round-65/w1/ProbeBuild/sqlite-gcov-probe.txt` | `25c7cab7da00c44b32ab2a939ca9b1626dc0539e870ce9759654bea1535b3ba0` |
| battery run log (same invocation, stdout) | `.../ProbeBuild/battery-run.txt` | — |
| checker | `.../ProbeBuild/check-receipt.txt` (`CHECK ok cases=5`, `PREDICATE R65-C1 pass`, rc 0) | — |
| selftest | `.../ProbeBuild/selftest.txt` (`SELFTEST pass`, rc 0) | — |
| frozen table | `.../ProbeBuild/render-table.txt` | — |

The probe is lane-authored and written from the r64 house skeleton
(`plans/round64_c1_kvstore_probe.py`): docstring with design notes + exit map, frozen
vectors, SETUP refusals, derive-then-compare. It runs the grader's own three test
functions, never a copy: `corpus/evidence/round52/graders/sqlite-with-gcov/tests/test_outputs.py`
is bound read-only at `/tests/test_outputs.py` after a run-time sha256 check against
`b165f8504bb93a901451b80c4ea73344b71b6af377ebdabef745fbcdd1d2993b` and a `def test_`
order check (`test_sqlite_compiled`, `test_sqlite_in_path`, `test_gcov_enabled`).
Amalgamation read from the byte-pinned wave copy
`.ufo/waves/round-65/w1/sqlite-amalgamation-3540100.zip`, re-hashed at run time
(`0a9c8e34…d1f9`, 2990966 bytes); no download was made this seat.

## Observed (commands run, values as printed)

Battery (exit 0, 10.5 s):

```
python3 .../ProbeBuild/round65_c1_sqlite_probe.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --work /fast/scratch/hyaku/kengaku-r65/ProbeBuild/run \
  --receipt .../ProbeBuild/sqlite-gcov-probe.txt
```

Five LEGS lines, each equal to the frozen vector:

| case | build / mask / PATH | observed | gcda/gcno left | leg-3 or leg-2 fragment |
|---|---|---|---|---|
| G1 | `--coverage`, masked, `/app/sqlite:/usr/local/bin:/usr/bin` | `P P P` | 2 / 2 | — |
| G2 | none, masked, `/usr/local/bin:/usr/bin` | `F F F` | 0 / 0 | leg2 `sqlite3 not found in PATH` |
| G3 | plain `-O0 -g`, masked | `P P F` | 0 / 0 | leg3 `No .gcda files found` |
| G4 | `-fprofile-arcs` only, masked | `P P F` | 2 / 0 | leg3 `No .gcno files found` |
| G5 | none, **no mask** | `P P F` | 0 / 0 | leg3 `No .gcda files found` |

Attribution (live ENV lines): G1/G3/G4 `which_sqlite3=/app/sqlite/sqlite3`,
version `3.54.1 2026-10-16 …`; G2 `which_sqlite3=None`, `PermissionError [Errno 13]`;
G5 `which_sqlite3=/usr/bin/sqlite3`, host version `3.54.0 2026-10-09 …` (the host
binary's own string ends `…bcalt1 (64-bit)`; verified verbatim against
`/usr/bin/sqlite3 --version`, not a driver artifact). Mechanism separation is
therefore not inferred from the silhouette: G3 (no instrumentation) leaves no
instrument files at all, G4 leaves `.gcda` but no `.gcno`, G5 reports the host binary.

Checker (exit 0):

```
python3 .../ProbeBuild/round65_c1_sqlite_probe.py --check-receipt .../sqlite-gcov-probe.txt
CHECK ok cases=5
PREDICATE R65-C1 pass
```

Selftest (exit 0, run with `--work /fast/scratch/hyaku/kengaku-r65/ProbeBuild/selftest`):
`render-table`, `predict-legs` (derivation == freeze in every cell), valid receipt 0;
tampered vector, dropped G4 FRAGMENT, dropped G2 leg fragment, drifted amalgamation
sha, dropped per-case NOBIND, empty receipt → 1; missing receipt → 2.

No-bind observation: `ss -ltnH` listener count 35 before and after the battery and
before/after every case (delta 0 for all five), and the probe process itself holds 0
listening sockets (`ss -ltnpH`, `probe_listening=0`). No server started, no PID
signalled, no port bound. No tool installs were needed or made; pacman untouched; no
network call made (the zip was already committed at the freeze).

## Integration notes for the L1

- The claims doc and its counting command name `plans/round65_c1_sqlite_probe.py`;
  this seat is scoped to its own dir, so the file must be landed at
  `kengaku-shokunin/plans/round65_c1_sqlite_probe.py` byte-identically (sha above).
- The receipt must be landed at `kengaku-shokunin/corpus/evidence/round65/sqlite-gcov-probe.txt`
  (sha above) for `--check-receipt corpus/evidence/round65/sqlite-gcov-probe.txt` to
  reproduce `PREDICATE R65-C1 pass` from the lane root. Both files are self-contained;
  they reference each other by relative paths only in prose, not at run time.

## Risks / blockers

- None to report. Named limitation carried unchanged: `--check-receipt` re-derives
  text fields only and cannot prove a live run; the live evidence is the per-case
  BUILD/RUN/FILES/ENV lines in the receipt (compile command, elapsed ms, sandbox argv
  digest, emitted `.gcda`/`.gcno` lists) plus `battery-run.txt`.
- Instrument note (not a claim change): the amalgamation is extracted with the stdlib
  `zipfile` module instead of `/usr/bin/unzip`, so member names and sizes are checked
  in-process; the four expected members are required or the battery refuses (exit 2).
- G5's `listeners` counts are a whole-host observation and can move under other
  work on this box; the predicate clause is that the observation is recorded per case,
  which the checker enforces. The per-host-count equality is recorded, not graded.
