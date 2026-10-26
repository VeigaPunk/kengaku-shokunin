# R43PytestParity — real-pytest parity for the C2 feal probe (kengaku round 43, wave 1)

Seat: R43PytestParity (executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(freeze commit `02753f26`, first probe run `6b49694d`). 2026-10-26.
Question: the frozen receipt `corpus/evidence/round43/feal-probe.txt` was produced by the probe's
own harness (host python 3.14, imports the test function, no pytest). Does the pinned grader reach
the SAME 12 verdicts when the real `tests/test.sh` line runs REAL pytest on the same end states?

## Method

- Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r43/R43PytestParity/lane`;
  `git -C "$S/lane" rev-parse --show-toplevel` = `$S/lane`, HEAD `d33350fdb01ce2…`, `git status --porcelain` empty.
  The probe imported is that clone's copy: sha256 `17d694ba…`, identical to the canonical
  `plans/feal_probe.py`; receipt copy sha256 `8c987463…`, identical to the canonical receipt.
- Reuse: the driver (`driver.py`, sha256 `a3f549d6…`) loads the probe copy and reuses its `CASES`, its
  `run_case` staging (copies `feal.py` into /app, the five grader files into /tests, writes the case's
  `attack.py`/recipe) and its `sandbox_argv`. Only `probe.harness(cap, work, "grade")` is replaced: it
  runs `/tests/test_outputs.py` under real pytest in the SAME bwrap argv (cwd /app, /app and /tests
  writable binds, /cap with solve.sh, `--unshare-net --unshare-pid --unshare-ipc`, /tmp tmpfs), then
  records the process exit status — exactly what `tests/test.sh:25` rewards. The probe's recipe step
  (`probe.harness(..., "recipe")`) still runs unchanged before grading.
- Interpreter/wheels fetched OUTSIDE the case sandbox (host network, before any bwrap):
  `uv venv --python 3.13 $S/tools/venv` then
  `uv pip install --python $S/tools/venv/bin/python pytest==8.4.1 setuptools==80.9.0`.
  Inside the case sandbox the scratch tree and the uv python tree are `--ro-bind`-ed at their own
  absolute paths, and `PATH` starts with the venv `bin` (so `test_outputs.py:20`'s subprocess `python`
  is the same 3.13.16). Command, run twice per case:
  `$VENV/bin/pytest /tests/test_outputs.py -v -rA`.
- Versions actually used: **python 3.13.16** (uv-managed CPython, `[Clang 22.1.3]`), **setuptools
  80.9.0**, **pytest 8.4.1**, pluggy 1.7.0, **gcc 16.2.1** (GNU ld 2.47), glibc 2.44 (ldd),
  bubblewrap 0.13.1, uv 0.13.0, kernel 7.2.11-arch1-1.

## Result: 12/12 parity, 0 mismatches, 0 regrade differences

24 real-pytest runs (2 fresh runs per case). `receipt` = `observed`/`tests` column of
`corpus/evidence/round43/feal-probe.txt`; `rc` is pytest's exit status (`0` → test.sh writes reward 1).

| case | receipt observed | receipt test | pytest rc r1/r2 | pytest letter r1/r2 | parity | wall s | pytest outcome line |
|---|---|---|---|---|---|---|---|
| nop | fail | F | 1 / 1 | F/F | same | 0.75 | 1 failed in 0.28s |
| oracle-solve-sh | pass | P | 0 / 0 | P/P | same | 1.15 | 1 passed in 0.48s |
| wrong-key | fail | F | 1 / 1 | F/F | same | 0.78 | 1 failed in 0.28s |
| oracle-off-by-one | fail | F | 1 / 1 | F/F | same | 1.17 | 1 failed in 0.49s |
| return-str | fail | F | 1 / 1 | F/F | same | 1.17 | 1 failed in 0.48s |
| cheat-import-get_keys | pass | P | 0 / 0 | P/P | same | 0.76 | 1 passed in 0.26s |
| cheat-always-equal | pass | P | 0 / 0 | P/P | same | 0.88 | 1 passed in 0.29s |
| cheat-sysmodules-shadow | pass | P | 0 / 0 | P/P | same | 0.79 | 1 passed in 0.29s |
| cheat-patch-get_keys | pass | P | 0 / 0 | P/P | same | 0.67 | 1 passed in 0.26s |
| cheat-exit-zero | pass | P | 0 / 0 | P/P | same | 0.60 | (no verdict line, see below) |
| cheat-clock-seed | pass | P | 0 / 0 | P/P | same | 0.76 | 1 passed in 0.29s |
| slow-oracle-45s | pass | P | 0 / 0 | P/P | same | 91.05 | 1 passed in 45.48s |

A separate re-run of the slow case (log capture) gave rc 0/0 at 45.53 s / 45.41 s, `1 passed in
45.41s` and `1 passed in 45.26s` — the 30 s instruction limit (`instruction.md:3`) is not enforced,
nothing times the call, exactly as the receipt's `violates=time-30s` pass says.

`table.tsv` is the machine copy; last line `PARITY same=12/12`. Per-run rc/elapsed/marker and the
first/last lines of each pytest run: `full-run.txt` (JSON). Wall includes staging + extension build.

## The three flagged cheats, under real pytest

- **cheat-exit-zero** — rc=0 in both runs, and the process dies mid-run: the captured log is 388 bytes
  and its last line is `../tests/test_outputs.py::test_feal_differential_cryptanalysis_attack`
  (`out/cheat-exit-zero.0.log`). `tests/test.sh:25` sees `$? -eq 0` and writes reward 1 → P, same as
  the receipt's `exit=no-verdict-line` P. pytest's own "1 passed" never prints; the verdict is
  carried solely by the exit status.
- **cheat-always-equal** — `1 passed`, rc 0. Assertion rewriting IS active in the run — the
  wrong-key/return-str logs show rewritten comparisons (`E assert 1108641166 == 0`,
  `E AssertionError: assert 3401275676 == '3401275676'`) — but rewriting only builds an explanation
  after the comparison is false; `Anything.__eq__` returns True, so `assert feal_in_c.get_keys()[5]
  == stolen` (`test_outputs.py:30`) is never false. Same verdict as the in-process harness.
- **cheat-sysmodules-shadow** — `1 passed`, rc 0. Decisive: `test_outputs.py:20` really rebuilt
  `/tests/feal_in_c*.so` in every run, and `test_outputs.py:27` calls `create_random_keys()`; if the
  extension had been imported, key[5] would be non-zero and `attack()` returning 0 would fail. Passing
  proves the fake `sys.modules["feal_in_c"]` installed while `import attack` (line 24) won over the
  extension import at line 25 — pytest's earlier `sys.path` insertion of /tests does not change this.

Failing cases agree for the same reasons the probe recorded: `nop` → `ModuleNotFoundError: No module
named 'attack'` (test_outputs.py:24), return-str/wrong-key → rewritten `assert` failure at line 30.

## Extra parity leg: the full test.sh argv (with the ctrf plugin)

`tests/test.sh:17-22` also passes `-w pytest-json-ctrf==0.3.5` and `--ctrf /logs/verifier/ctrf.json`.
A second venv (same pytest/setuptools pins + `pytest-json-ctrf==0.3.5`) re-ran three cases with
`--ctrf /tmp/ctrf.json` (the image's `/logs` does not exist here): wrong-key rc 1, cheat-always-equal
rc 0, cheat-exit-zero rc 0 — verdicts unchanged, and the run reports `plugins: json-ctrf-0.3.5`
(`out/wrong-key.0.log:5`). Logs: `ctrf-run.txt`.

## ENVELOPE receipts (all `unchanged`; Q32)

Main 12-case run:
```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r43/R43PytestParity/env /fast/scratch/hyaku/kengaku-r43/R43PytestParity/env --bind /fast/scratch/hyaku/kengaku-r43/R43PytestParity/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r43/R43PytestParity/driver.py
ENVELOPE start 19:09:31 cwd=/fast/scratch/hyaku/kengaku-r43/R43PytestParity
ENVELOPE end 19:11:13 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Detail re-run (6 cases, full logs saved):
```
ENVELOPE start 19:11:30 cwd=/fast/scratch/hyaku/kengaku-r43/R43PytestParity
ENVELOPE end 19:11:36 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
ctrf-parity run (3 cases):
```
ENVELOPE start 19:12:06 cwd=/fast/scratch/hyaku/kengaku-r43/R43PytestParity
ENVELOPE end 19:12:10 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```
Slow-case re-run (log capture, 2 runs):
```
ENVELOPE start 19:13:09 cwd=/fast/scratch/hyaku/kengaku-r43/R43PytestParity
ENVELOPE end 19:14:42 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

## Limits (stated, not worked around)

- Not the task image: host Arch glibc 2.44 / gcc 16.2.1 stand in for Debian bookworm's glibc/gcc; the
  uv-managed CPython 3.13.16 stands in for the image's python:3.13-slim interpreter; uv 0.13.0 stands
  in for test.sh's 0.9.5. `cheat-clock-seed` depends on glibc `rand()` and passed here as in the receipt.
- `/logs/verifier` is absent, so the ctrf leg writes /tmp/ctrf.json; the main leg omits ctrf, per the
  assigned invocation. `apt-get`/`curl` are not run (no network inside the case sandbox; the real
  test.sh installs gcc/uv over the network).
- Recipes run as the probing user, not root. The probe's own harness step uses host python 3.14; that
  difference is exactly the property under test, and it changes no verdict.
- 38 pytest invocations total (24 main + 6 detail + 6 ctrf + 2 slow re-run, four 45 s sleeps);
  every verdict stable.

## Evidence files (this directory)

`driver.py` a3f549d6…, `full-run.txt` 1c86e755…, `table.tsv` 369f3e0c…, `detail-run.txt` d0d9c67c…,
`ctrf-run.txt` bfb19243…, `slow-run.txt` 4656e621…, `out/{nop,wrong-key,return-str,
cheat-always-equal,cheat-sysmodules-shadow,cheat-exit-zero}.0.log` plus `out/slow-oracle-45s.{0,1}.log`,
`SHA256SUMS`.
Scratch `/fast/scratch/hyaku/kengaku-r43/R43PytestParity` removed after the report.

VERDICT: pytest-parity-12/12
