source: S278 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-rust-c/tests/test_outputs.py — pinned commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`; the captured function `test_fibonacci_polyglot` from `tests/test_outputs.py:10`; sha256 `baed5e4d0cc0e5809ff41a7df1815d18c65c708a3a3f264428e1cda11ce692f9` (1638 bytes); opened 2026-11-05
verified-at: 2026-11-05, commit a9b8a1a00b6a5ab5206be4d377dba439e02f8244 — counter `plans/round89_c1_replay.py` at the tip (`TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0`, `PREDICATE R89-C1 pass`); probe receipt `corpus/evidence/round89/polyglot-rust-c-probe.txt` (TOOL_SHA `03c202f5…`, CASE_TABLE_SHA `7dff1654…`)
recheck: from the lane root, `python3 plans/round89_c1_replay.py --lane . --rev HEAD --work <scratch>`; require `TARGET executed_rows=33 member=polyglot-rust-c located=1 executed=1 cases=8 legs=8 mismatches=0 defects=0` and `PREDICATE R89-C1 pass`; any drift in the captured grader (`baed5e4d…`), the case table (`7dff1654…`), the probe (`03c202f5…`) or the receipt supersedes this entry

# Terminal-Bench 2.0 task grader, read and executed offline: `polyglot-rust-c`

## Summary

At terminal-bench-2 commit `2fd12b88` the `polyglot-rust-c` score is one pytest function, `test_fibonacci_polyglot` (`:10` — `grep -n 'def test_' corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py` 2026-11-05). It lists `/app/polyglot`, requires exactly `["main.rs"]`, compiles the file with `rustc` and with `g++ -x c++` through `os.popen`, then runs both binaries on five sizes under `subprocess.run(check=True)`.

Offline execution of that captured function against a frozen table of 8 — `grep -c '"id"' plans/round89-cases.json` 2026-11-05 — synthetic `/app/polyglot` trees matched every prediction written from the static reading before the first run: `cases=8 legs=8 mismatches=0` (`python3 plans/round89_c1_replay.py --lane . --rev a9b8a1a00b6a5ab5206be4d377dba439e02f8244 --work <scratch>` 2026-11-05). The graded artefact class is new to this lane's executed set: one source file compiled by two toolchains, judged through a subprocess whose failure can surface as an uncaught exception instead of a grader verdict.

## Source labels

S278 is the maintainers' own grader file, the primary source for what the grader checks. It is tier A for member replay only. The probe receipt is the lane's re-runnable gate output for these eight artefacts against the digest-pinned capture, inside bubblewrap; the counter re-derives it at the measured revision (leg L6).

## What the grader grades

Line numbers below: `grep -n -e 'canary' -e 'assert polyglot_files' -e 'os.popen' -e 'test_cases = ' -e 'for n, expected' -e 'subprocess.run' -e 'check=True' -e 'rust_out = ' -e 'cpp_out = ' -e 'assert rust_out' corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py` 2026-11-05.

| Step | Mechanism | Lines |
|---|---|---|
| Listing | `os.listdir("/app/polyglot")` must equal `["main.rs"]`, else AssertionError before any compile | :19 |
| Compiles | `os.popen("rustc ... -o .../main").read()` and `os.popen("g++ -x c++ ... -o .../cmain").read()`; output read and discarded, exit status never checked | :24 and :25 |
| Sizes | five `(n, expected)` pairs: (0, "1"), (1, "1"), (2, "2"), (10, "89"), (42, "433494437") | :27 |
| Rust run | `subprocess.run(["/app/polyglot/main", str(n)], check=True)`, stdout stripped | :30 call, :34 check, :36 strip |
| C++ run | `subprocess.run(["/app/polyglot/cmain", str(n)], check=True)`, stdout stripped | :37 call, :41 check, :43 strip |
| Decision | `assert rust_out == expected and cpp_out == expected` | :44 |

## Eight frozen vectors, predicted and observed

Predicted values: `"predicted"` fields in `plans/round89-cases.json` (P 2, F 5, E 1 — `grep -c '"predicted": "P"'`, and the F and E forms, 2026-11-05). Observed values: receipt `CASE` lines 15-22 (`grep -n '^CASE ' corpus/evidence/round89/polyglot-rust-c-probe.txt` 2026-11-05), all equal to predicted.

| Case | Predicted | Observed | Mechanism |
|---|---|---|---|
| exact (control) | P | P | both binaries print f(n) for 0, 1, 2, 10, 42; all five expected strings hold |
| padded-output | P | P | both print spaces around the number; `.strip()` removes them before the comparison |
| extra-file | F | F | `os.listdir` returns `main.rs` and `notes.txt`; the :19 assertion raises AssertionError before any compile |
| off-by-one-rust | F | F | the Rust `f` returns `a`, so f(0) is 0, not "1"; the :44 assertion raises AssertionError |
| cpp-exits-nonzero | E | E | the C++ block prints the right value then `return 1`; the C++ call at :37 with `check=True` at :41 raises CalledProcessError on the first size |
| rust-only | F | F | g++ fails silently and `cmain` is absent; the C++ call at :37 raises FileNotFoundError |
| cpp-only | F | F | rustc fails silently and `main` is absent; the Rust call at :30 raises FileNotFoundError |
| neither-compiles | F | F | neither compiler yields a binary; the Rust call at :30 raises FileNotFoundError |

## E versus F

The case table's prediction note names the two graded refusals. F is `AssertionError` (the grader's own checks at :19 and :44) or `FileNotFoundError` (raised by `subprocess.run` at :30 or :37 when a binary was never built). E is anything else. The one E case raises `CalledProcessError`, which `check=True` raises when a binary exits nonzero, and the grader does not catch it. The distinction is one of exception identity: in E no grader assertion runs and no grader message is written. [INFERENCE] Pytest reports an uncaught exception as a failed test, so E and F probably share a pass/fail outcome; this entry measures exception identity only, and the probe does not run pytest.

## Honest limits

- Three distinct vectors, not eight. Predicted values are P, F and E only (see counts above), so the table tests three behaviours across eight inputs.
- L6 reproduces the observation; it does not authenticate an author. A copy minted elsewhere with a correct observation block and a tip stamp is indistinguishable by observation. L2 and L3 check the stamp and ancestry; L9 pins the probe bytes to `03c202f5…` (`sha256sum plans/round89_polyglot_probe.py` 2026-11-05).
- The probe runs the grader in bubblewrap, not in a Terminal-Bench container, with the host toolchain: `rustc 1.99.1` (`rustc --version` 2026-11-05) and `g++ (GCC) 16.2.1` (`g++ --version` 2026-11-05). The vectors describe this host's toolchain.
- The capture carries the TB2 canary banner (line 2, grep above). This entry is a digest-pinned execution record, not a contamination measurement.

## Negative space

This entry does **not** establish task validity, agent or model performance, any trajectory, how Harbor consumes the verifier outcome, or how the grader behaves under a toolchain other than this host's.

## Falsifier

This entry is falsified if (a) a re-fetch of the pinned S278 URL yields bytes whose sha256 differs from `baed5e4d…`; (b) `plans/round89_c1_replay.py --lane . --rev HEAD` prints anything other than the two recheck lines; (c) a re-run of `plans/round89_polyglot_probe.py` prints observations different from the receipt; or (d) the captured grader is shown to decide by anything other than the listing, the two compiles and the five sizes.

## Connections

- `[[tb2-chess-best-move-grader]]` — the prior executed offline replay with the same digest-pinned receipt pattern; this entry adds an exception-identity class that the chess grader does not have.

## Admission state (Q13/Q14)

`second-seat re-read: pending (R3)` — admission is the L1's call; no second-seat report is cited by this entry.

Writer note: draft by ScribeR89 (round 89, wave 1); applied by the L1 only.
