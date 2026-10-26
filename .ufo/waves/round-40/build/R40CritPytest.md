# R40CritPytest — pytest parity over the 28 frozen db-wal-recovery case states

Seat: critic, round 40 wave 1. Judged on **coverage**. Scope: independently re-grade the C2 probe's 28 frozen
case end states with the REAL pytest 8.4.1 and compare per-test letters with
`corpus/evidence/round40/db-wal-probe.txt` (sha256 `c74c6b91…730e`). Nothing frozen was modified; all work ran in
`/fast/scratch/hyaku/kengaku-r40/R40CritPytest` (now removed).

## 1. Axes

| axis | move |
|---|---|
| (a) per-test letter parity, 28/28 cases | measured: 28/28 |
| (b) exception-class parity (the receipt's `error=` column) | measured: 28/28 |
| (c) aggregate verdict vs the verifier's real reward rule | measured: exit 0 exactly on the 8 all-`P` cases |
| (d) end-state construction fidelity (host sqlite3 vs image) | **not covered** — named, see §6.2 |
| (e) method transparency (raw receipts, echo control) | raw pytest text for 28 cases + permutation control 8/28 |

## 2. Setup (versions and provenance)

```
uv venv -p 3.13 /fast/scratch/hyaku/kengaku-r40/R40CritPytest/venv
  -> Using CPython 3.13.16
uv pip install --python …/venv/bin/python pytest==8.4.1            -> pytest 8.4.1
uv pip install --python …/venv/bin/python pytest-json-ctrf==0.3.5  -> pytest-json-ctrf 0.3.5
```

`uv python list --all-versions` shows `cpython-3.13.16` as the newest 3.13 uv can resolve today, so the venv
interpreter is what `uvx -p 3.13` would fetch. The toolchain matches the verifier exactly:
`test.sh:18-22` runs `uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --ctrf … /tests/test_outputs.py -rA`,
and `test.sh:25-29` writes reward 1 iff that exit is 0 — so "pytest 8.4.1 under 3.13" is the graded engine, not a
stand-in chosen by me. Captured grader digest verified before every run by the probe's own PINS:
`test_outputs.py` sha256 `88dc5c2a…ba49`.

Probe reuse: `plans/db_wal_probe.py` was copied byte-identically (`69af65df…9ff3`, unchanged since freeze commit
`bbb1095`) into scratch; only `HARNESS_PY` and `sandbox_argv` were replaced. `P.run_case` (recipe, seeding,
`--unshare-pid/net/ipc`, `/app`, `/cap`, `/k`) is the probe's own code, so the 28 end states are the probe's, not
mine. One addition inside the same bwrap: `--ro-bind <venv> /venv` and `--ro-bind ~/.local/share/uv/python <same
path>` (read-only), so the real pytest runs in the venv against the same state.

## 3. Method

Three pytest invocations per case, from the SAME end state, after the case's frozen recipe:

| tag | invocation |
|---|---|
| `PT` | `/venv/bin/python -m pytest /cap/test_outputs.py -q -rA --no-header -p no:cacheprovider` (COLUMNS=1000) |
| `REPT` | byte-identical repeat of `PT` (stability column, mirrors the receipt's `regrade=`) |
| `CTRF` | `test.sh` verbatim: `pytest --ctrf /tmp/verifier-ctrf.json /cap/test_outputs.py -rA`, cwd `/app`, no extra flags |

`/tests/test_outputs.py` → `/cap/test_outputs.py` and `/logs/verifier/ctrf.json` → `/tmp/verifier-ctrf.json` are
the only path substitutions (the grader reads only absolute `/app/...` paths; the ctrf path only selects where the
plugin writes). Command: `python3 parity.py` (full receipt with raw pytest text per case in
`R40CritPytest/pytest-parity.txt`; driver in `R40CritPytest/parity.py`, sha256 `c51d1b89…6bf`).

## 4. Result — 28/28 agree, letters and exception classes

`python3 parity.py` (exit 0):

```
parity cases=28 agree=28 disagree=0 pytest_pass=8
parity-ctrf cases=28 agree=28 disagree=0 ctrf_pass=8
```

Per case (`pytest`/`ctrf` letters, receipt letters; all agree):

| case | letters (PT = CTRF) | receipt | case | letters (PT = CTRF) | receipt |
|---|---|---|---|---|---|
| empty-app | FFFFFFF | FFFFFFF | truth-plus-duplicate-id11 | PPPPFFP | PPPPFFP |
| untouched | FFFFFFF | FFFFFFF | truth-dup-id10-no-id11 | PPPPFFP | PPPPFFP |
| oracle-solve-sh | PPPPPPP | PPPPPPP | truth-extra-field | PPPPPPP | PPPPPPP |
| base-only-ro | PPPPFPF | PPPPFPF | truth-wrapped-object | PFFFFFF | PFFFFFF |
| plain-read-then-solve | PPPPFPF | PPPPFPF | truth-ids-as-strings | PPFFFPP | PPFFFPP |
| xor-wrong-key | PPPPFPF | PPPPFPF | truth-ids-as-floats | PPFPPPP | PPFPPPP |
| decrypt-then-extract | PPPPPPP | PPPPPPP | truth-trailing-garbage | PFFFFFF | PFFFFFF |
| decrypt-checkpoint-truncate | PPPPPPP | PPPPPPP | truth-wrong-path | FFFFFFF | FFFFFFF |
| decrypt-in-place-no-json | FFFFFFF | FFFFFFF | empty-list | PFPPFPF | PFPPFPF |
| literals-never-open-db | PPPPPPP | PPPPPPP | truth-drop-id11 | PPPPFPP | PPPPFPP |
| literals-names-1-2-wrong | PPPPPPP | PPPPPPP | truth-value-id3-wrong | PPPPPPP | PPPPPPP |
| literals-id3-name-wrong | PPPPFPP | PPPPFPP | truth-bool-value-id5 | PPPPPPP | PPPPPPP |
| truth-value-float-id1 | PPFPPPP | PPFPPPP | truth-name-null-id1 | PPFPPPP | PPFPPPP |
| truth-reversed-order | PPPFFPP | PPPFFPP | truth-value-string-id4 | PPFPPPP | PPFPPPP |

Column tallies over the 28 `PYCASE` lines: `match=yes` 28, `ctrf_match=yes` 28, `errs=same` 28, `regrade=same` 28,
`pytest_rc=0` 8. All 84 pytest runs collected exactly 7 tests (`PCOUNT` = 7 × 84), and every `CTRFJSON|` line
reports `tests=7` from the plugin's own JSON — no silent empty collection.

The `errs=same` comparisons are exact maps over the receipt's non-`AssertionError` classes: 6 of 28 cases carry
classes — `FileNotFoundError` ×24 test-instances across 4 cases, `JSONDecodeError` ×6 in 1 case, `TypeError` ×2 in
1 case (`truth-wrapped-object`) — and pytest reproduced every one. The 3-of-6 split inside `untouched` is what makes
the method finding in §6.1.

Aggregate: 8 pass / 20 fail, `pytest_rc=0` on exactly the eight all-`P` cases — matching the receipt's
`cases=28 observed_pass=8 observed_fail=20` and the `test.sh:25-29` reward rule. So the probe's headline
observation survives the real runner from the runner side: `literals-never-open-db` is `PPPPPPP` — hand-typed JSON
that never opens the database passes 7/7, and "Fix the WAL file" (`instruction.md:7`) is graded only through the
export.

## 5. Non-vacuity control (comparator is not an echo)

Re-scoring the saved observations against the **next** case's receipt row (zero reruns) gives
`permuted-control cases=28 agree=8`; the 8 coincidences are exactly the adjacent rows whose letter columns are
identical (`FFFFFFF` empty-app→untouched; `PPPPFPF` base-only-ro→plain-read-then-solve→xor-wrong-key; `PPPPPPP`
×3; `PPPPFFP`; `PPFPPPP`). A comparator that echoed the receipt, or a harness that silently returned the probe's
letters, would score 28/28 here.

## 6. Falsifiers and limits (what this parity does NOT buy)

### 6.1 Text parsing of `-rA` is width-sensitive; the exception-class half of parity silently vanishes at 80 cols
First pass (no `COLUMNS`) reproduced `errs=DIFF` on `untouched` for exactly 3 of 6 exceptional tests while all
letters still matched. Re-run as a control (`R40CritPytest/truncation-control.txt`):

```
LINE|FAILED ../cap/test_outputs.py::test_recovered_json_is_valid - FileNotFoundErr...
LINE|FAILED ../cap/test_outputs.py::test_recovered_data_structure - FileNotFoundEr...
LINE|FAILED ../cap/test_outputs.py::test_recovered_data_completeness - FileNotFoun...
```

pytest truncates short-summary lines to the 80-column fallback width and cuts inside the class name. The class is
recoverable only because lines 1/4/6/7 happen to fall on a boundary. **Smallest safe correction:** any seat
parsing pytest text sets `COLUMNS` wide (done here), or reads outcomes from `--ctrf`/a `pytest_runtest_logreport`
plugin. This does not touch frozen artifacts; it is a warning for future parity work.

### 6.2 This is grader-side parity only — end-state construction is shared with the probe
Both the probe and this replica build recipes with `/usr/bin/sqlite3` 3.54.0 and `/usr/bin/python3` 3.14 on this
host, while the image is `ubuntu:24.04` (sqlite 3.45.x, python3 3.12). The parity run therefore cannot detect a
host-vs-image divergence in exactly the cases whose state depends on SQLite WAL semantics —
`plain-read-then-solve` (plain read-write open discards the undecryptable WAL), `decrypt-checkpoint-truncate`
(`PRAGMA wal_checkpoint(TRUNCATE)`), `xor-wrong-key` (invalid magic ignored). These semantics are old and stable,
but nothing in the package demonstrates them on the image. This is already a named limit of the C2 claim
("host sqlite3 3.54.0 … stand in for the image's Ubuntu 24.04 packages"), so it is a **tradeoff the canonical
judge may accept**, not a defect; closing it needs an image pull, out of scope for every round so far.

### 6.3 Outcome classes outside the 28 cases are unverified
The probe maps "any non-`AssertionError` exception → F" (`db_wal_probe.py:16`) and a case verdict is all-`P`; the
real runner maps "pytest exit 0". These coincide for PASSED/FAILED. They need not coincide for pytest `Skipped`
(a `BaseException`, which the probe's `except Exception` would not catch) or xfail — no captured case can produce
either (no fixtures, no marks, seven plain functions), so the equivalence is established only for this grader file.

### 6.4 Verifier-side risks that this run did close
`pytest-json-ctrf` sits inside `test.sh`'s exit path; a failing ctrf write could flip the reward. Measured on the
host: `--ctrf /home/vgpnk/no-such-dir-xyz/ctrf.json` still exits `rc(missing dir)=0`, so the plugin's write cannot
masquerade as a test failure. And `uvx -p 3.13` resolves to `3.13.16` today — the interpreter used here; the grader
uses only `json`, `os` and `isinstance`, so a future 3.13 patch is very unlikely to move a letter.

## 7. Impact on the frozen C2 package

None required. The receipt's `tests=` and `error=` columns are reproduced **letter-for-letter and class-for-class**
by the verifier's own toolchain (`pytest==8.4.1`, `pytest-json-ctrf==0.3.5`, CPython 3.13.16), with the same
aggregate 8 pass / 20 fail and the same `regrade=same` stability, so V7's requirement-map labels — derived from
those letters and `violates=` tags — stand. The residual exposure is §6.2 (state construction), which the claim
already names as a limit.

## 8. Receipts (in `.ufo/waves/round-40/build/R40CritPytest/`)

| file | sha256 | content |
|---|---|---|
| `pytest-parity.txt` | `7fd60039…61e7` | 28 `PYCASE` lines + raw pytest `-rA` text per case |
| `truncation-control.txt` | `d5f0d0b1…3477` | 80-column truncation artifact on `untouched` |
| `parity.py` | `c51d1b89…6bf` | driver (probe reuse, three invocations, receipt parser) |

Commands: `uv venv -p 3.13 …/venv`; `uv pip install --python …/venv/bin/python pytest==8.4.1 pytest-json-ctrf==0.3.5`;
`python3 parity.py` (19 s, exit 0); permutation control and `--ctrf` failure probe as quoted above. Scratch
`/fast/scratch/hyaku/kengaku-r40/R40CritPytest` deleted after copying these three files.

VERDICT: pytest-parity-28/28
