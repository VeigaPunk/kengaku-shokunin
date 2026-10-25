# R35ProbeRerun — probe determinism rerun (kengaku r35 w1)

Seat: R35ProbeRerun (executor, leaf). Assignment: re-run frozen probe twice in lane read-only; byte-compare both with the receipt; also run in a fixture clone at the freeze commit with uncommitted captures copied in, and with Python 3.13 (the version `test.sh` pins); record any byte difference and its cause.

## Environment / tools
- uv 0.13.0 (pre-installed; no tool installs performed). uv downloaded `cpython-3.13.16-linux-x86_64-gnu` into `~/.local/share/uv/python` and packages (numpy, biopython 1.85) into the uv cache as part of the pinned invocation `uv run -p 3.13 --no-project --with biopython==1.85` (channel: uv-managed interpreter/env; reason: test.sh pins `-p 3.13`, biopython==1.85).
- Lane HEAD == freeze commit: `11d64530179b78e33ba6074fc77d63d36ee7ac31` (`git rev-parse HEAD`).
- Grader capture digest at run time: `test_outputs.py` sha256 `44a05a2482aa7a8e70de95478de6560b6188e630336fca9d02b62dc69a096582` == pinned digest in probe (`GRADER_SHA256`) == receipt line 1.

## 1. Lane read-only runs (x2)
Command (from lane root), exactly as frozen:
`uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`
redirected to `.ufo/waves/round-35/build/R35ProbeRerun/run1.txt` (run2.txt).
- `run1_exit=0`, `run2_exit=0`.
- `cmp run1.txt <receipt>` → exit 0; `cmp run2.txt <receipt>` → exit 0; `cmp run1.txt run2.txt` → exit 0.
- sha256: run1 `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` = run2 = receipt `2359d9067906f59d2c55b5802603d1ef45c376f653ad9997de1ef7da412b25b8` (21 lines each).
- Both runs report `cases=18 observed_pass=5 observed_fail=13 mismatches=0`.

## 2. Fixture clone at freeze commit + uncommitted captures
Fixture (per rule): `D=$(mktemp -d /tmp/k35-XXXX)`; `git clone -q --no-checkout --shared <lane> "$D/lane"`; `git -C "$D/lane" sparse-checkout set --no-cone 'plans/tb2_grader_probe.py' 'corpus/evidence/round35/tb2-eval/*' 'corpus/evidence/round35/tb2-grader-probe.txt'`; `git -C "$D/lane" checkout -q master`; verified `rev-parse --show-toplevel` == `$D/lane`; HEAD == `11d64530179b78e33ba6074fc77d63d36ee7ac31`.
- Note: `corpus/evidence/round35/tb2-eval/` is **untracked** in the lane (absent from the freeze tree — first fixture attempt's `cp` failed with "No such file or directory"; fixed by `mkdir -p` before copying). The probe script itself IS tracked and materialized. Captures copied: `tb2-eval/*` (incl. test_outputs.py, test.sh, instruction.md, SHA256SUMS) and `tb2-grader-probe.txt`; post-copy sha256 of `test_outputs.py` == pinned digest (above), receipt file `2359d906…` == evidence.
- Default-python run (system python 3.14): `uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` → `default_exit=0`; `cmp` vs evidence → exit 0; sha256 `2359d906…` identical.
- Python 3.13 run (pinned by test.sh): `uv run -p 3.13 --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` → `py313_exit=0`; `cmp` vs evidence → exit 0; sha256 `2359d906…` identical.
- `diff -u` of both fixture outputs vs evidence: empty (no byte difference).
- Fixture cleaned (`rm -rf "$D"`); copies of both fixture outputs retained in the seat scratch dir (`run-fixture-default.txt`, `run-fixture-py313.txt`).

## 3. Byte difference analysis
No byte differences anywhere: lane run1 = lane run2 = fixture(default) = fixture(py3.13) = evidence receipt. The probe is deterministic across (a) repeated runs in the lane, (b) a fresh sparse fixture clone at the freeze commit with the uncommitted capture copied in, and (c) interpreters (system 3.14 vs pinned 3.13). No cause to attribute; the only raster discrepancy observed during the work was the fixture's missing (untracked) capture directory, a harness/checkout artifact, not a probe output difference.

## Files changed (seat scope only)
- `.ufo/waves/round-35/build/R35ProbeRerun/run1.txt` (new), `run2.txt` (new), `run-fixture-default.txt` (new), `run-fixture-py313.txt` (new).
- `.ufo/waves/round-35/build/R35ProbeRerun.md` (this report).

## Risks / notes
- The probe output embeds only `biopython=1.85` (not the Python version); python-version identity is established via cmp over the full 21-line output, not via a version tag.
- `__pycache__` in the capture dir is not copied (directory, not a probe input); the probe loads the grader by path and is unaffected.

VERDICT: probe-deterministic-yes-py313-same
