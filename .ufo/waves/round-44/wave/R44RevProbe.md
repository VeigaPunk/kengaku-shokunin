# R44RevProbe — probe fidelity review (kengaku round 44 wave, v2)

Seat: `R44RevProbe` (reviewer, leaf). Scope: fidelity of
`plans/feal_linear_probe.py` (freeze `5f16ed0`) to the pinned Terminal-Bench 2.0
`feal-linear-cryptanalysis` grader (terminal-bench-2 @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`),
against the captured evidence in `corpus/evidence/round44/tb2-feal-linear-cryptanalysis/`
and the frozen dry table + receipt.

## Method

1. Read the frozen claims (`plans/round-44-claims.md`), the probe source in full
   (`plans/feal_linear_probe.py`, 343 lines), the captured grader files
   (`Dockerfile`, `test.sh`, `test_outputs.py`, `gen.py`, `solve.sh`, `decrypt.c`,
   `instruction.md`, `task.toml`, `README.md`, `SHA256SUMS`), the dry freeze table
   and the receipt.
2. Verified the pinned upstream tree (GitHub contents API at the exact pinned commit)
   for the task root, `environment/task-deps/` and `tests/`.
3. Re-ran the probe in the round-44 envelope: `--stage-check`, full `--dry`, full
   graded run; byte-diffed the reproduced outputs against the frozen evidence.
4. Independently rebuilt the image seed on the host (gcc + `python3 gen.py` +
   `./decrypt` with the public keys) and compared the 100 recovered plaintexts and
   the hash-chain replay against the pinned `soln` constants.

## Findings (by severity)

### 1. Minor — `SEED` comment mislabels the replayed Dockerfile range (`plans/feal_linear_probe.py:85`)
`# Dockerfile:6-11 replayed in /app (COPY already done by the probe).` — Dockerfile:6
is `RUN pip install setuptools==80.9.0`, which is *not* replayed; the replayed set is
Dockerfile:8-11 plus :13-14 (`COPY` line 8 is done by the host copy in `run_case`, and
line 12 is blank). The skipped `pip install` is disclosed in the docstring limits
(lines 40-42), so this is a label inaccuracy, not a hidden deviation. No measurement
impact.

### 2. Minor — `SEED` is not a literal replay of `RUN python3 gen.py` (`plans/feal_linear_probe.py:86`)
The seed runs `python3 gen.py >/dev/null`; Dockerfile:11 has no redirect. Inside the
sandbox this is behaviorally identical (the harness already discards stdout:
`stdout=subprocess.DEVNULL`), so no outcome changes — but a verbatim replay would omit
the redirect.

### 3. Minor/structural — `/tests` is visible during the agent/recipe phase (`plans/feal_linear_probe.py:203`)
The real harness mounts/copies the tests directory only at verification time, *after*
the agent finishes; the probe binds `/tests` (and `/pub`) from the start of each
sandbox. No case reads `/tests` (the knowledge channel is `/pub`), and `/tests`
contains the same file as `/pub/test_outputs.py`, so no outcome is affected and the
agent-knowledge model is unchanged. But the docstring claim that "the image state the
agent starts from is rebuilt per case" (lines 11-14) is not literally true: the
agent-phase sandbox also exposes `/tests` and `/pub`.

## Answers to the five review questions

1. **Does SEED replay Dockerfile:6-11 exactly (order, rm of orig_plaintexts.txt and gen.py)?**
   Order: yes — `gcc -O3 -o feal feal.c` → `gcc -O3 -o decrypt decrypt.c` →
   `python3 gen.py` → `rm orig_plaintexts.txt` → `rm gen.py` (Dockerfile:9,10,11,13,14).
   Both `rm`s present, in the right place. Deviations: the `>/dev/null` redirect
   (finding 2), the skipped `pip install setuptools==80.9.0` (Dockerfile:6, disclosed),
   and host gcc/`python3` standing in for the image toolchain (disclosed, lines 39-42).
   Verified empirically: rebuilt seed produces `pairs=32 ciphertexts=100 orig=100` and
   `./decrypt ciphertexts.txt 0x68e63 0x62571 0x1f61c 0xb74a5` yields exactly the 100
   pinned constants (`set_equal=True`, `replay_matches_soln=True`, `count_dup_soln=0`).

2. **Is /tests honest?** Yes on content: the pinned upstream `tests/` contains exactly
   `test.sh` + `test_outputs.py`; the probe mounts only `test_outputs.py` (the sole
   file `pytest` collects), read-only, and grades after the recipe. The only nuance is
   mount *timing* (finding 3), which no case exploits.

3. **Is reading /pub honest?** Yes. All three files are genuinely published in the
   pinned repo (`environment/task-deps/gen.py`, `solution/solve.sh`,
   `tests/test_outputs.py` — verified via GitHub tree at `2fd12b88`), and
   `task.toml:34` sets `allow_internet = true`, so an agent could fetch them. The
   probe's claim — "/pub models an agent that read the public task source" — is
   accurate; the caveat (these files are not inside the live container) is exactly
   what the model states.

4. **Is the exit-status mapping right for test.sh?** Yes. `tests/test.sh:22-28`
   writes reward 1 iff `$? -eq 0` (pytest's exit status). The harness calls
   `test_attack` directly and maps rc 0 → P, any exception (including
   `AssertionError` and `FileNotFoundError`) → F with rc 1 — each corresponds to
   pytest exit 0 vs non-zero, hence reward 1 vs 0. Verified against the captured
   `test.sh` text; `timeout=1800` per grade also matches `task.toml:22`
   (`verifier.timeout_sec = 1800.0`).

5. **Does the receipt leak host info?** No. The receipt (and `--dry` table) contain
   only deterministic content: pin digests, case rows, and totals; env is fixed
   (`ENV` dict), scratch is under `--work` and removed on exit, and no temp path,
   timing, hostname, or version is printed. The reproduced receipt is byte-identical
   to the frozen `corpus/evidence/round44/feal-linear-probe.txt`.

## Evidence

- **Stage-check reproduction** (`--stage-check --work $S`, envelope): 14/14 rc=0;
  `stagecheck cases=14 failed=0`; byte counts match the frozen run (oracle 6654,
  decrypt-keys/replay/constants 2047, one-missing 2026, hex 1895, pairs 649,
  ciphertexts 2045, nop absent).
- **Full graded reproduction** (`--work $S`, envelope): `cases=14 observed_pass=8
  observed_fail=6 mismatches=0`, `regrade cases=14 differ=0`, all `match=yes`, all
  `regrade=same` — byte-identical to `feal-linear-probe.txt` (only the envelope
  wrapper lines differ, from teeing).
- **Dry reproduction**: byte-identical to `feal-linear-dry-cases-freeze.txt`.
- **Seed-equivalence check** (host, inside envelope): `pairs=32 ciphertexts=100
  orig=100`; `soln_lines=100 mine_lines=100`, `set_equal=True`,
  `replay_matches_soln=True`, `count_dup_soln=0`.
- **Upstream tree at `2fd12b88`**: task-deps = {decrypt.c, feal.c, gen.py} only;
  tests = {test.sh, test_outputs.py} only; root contains no extra startup/harness
  files. Pin digests in the probe match `SHA256SUMS` for all 7 pinned files.
- **Envelope lines (Q32)** — stage-check: `ENVELOPE start 20:34:51 ... exit=0
  local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`; full
  run: `ENVELOPE start 20:35:05 ... exit=0 local_bin_content_before=328be01808ba022f
  after=328be01808ba022f unchanged`; seed check: `start 20:35:05 ... exit=0 ... unchanged`.

Reproduction receipts kept in `wave/R44RevProbe/`: `stagecheck-repro.txt`,
`probe-repro.txt`, `dry-repro.txt`, `seed-equivalence-check.txt` (all << 1 MiB).

## Residual risk / verification gaps

- The probe never executes the real `test.sh` pipeline (`apt-get`/curl/uvx/pytest) —
  it simulates pytest's exit status; this is disclosed in the docstring but is still a
  stand-in (e.g., a `--ctrf` plugin failure would not be observed).
- Host `python3` (3.14.8) and gcc (16.2.1) stand in for the image's python 3.13 and
  Debian gcc; deterministic here, but not the same binaries (disclosed).
- The four passing "no-attack" cases and the `-pub` model depend on the public repo
  remaining exactly as pinned; that is the intended model.

VERDICT: probe-defects-3
