# C1ScoutTaskShapes — R52-C1 population shape (read-only)

Seat: `C1ScoutTaskShapes`. Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`. Pin: `harbor-framework/terminal-bench-2` `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. Population: `plans/round52-tasks.json` (89 tasks). No grader was executed. No tool was installed (host `curl` and `python3` were enough; pacman stayed untouched).

Godspeed axes: completeness (every frozen task has a mechanism and a manifest presence bit), pin-byte fidelity (fetched blobs match the tree SHA), mechanism fidelity (reward conjunction, not file presence), classifier-gap (a shape the frozen primary-grader rules cannot speak to).

## What was fetched

Tree API (not truncated, sha equals the pin, 1446 entries = 1038 blobs + 408 trees):

```sh
curl -fsS -H "Accept: application/vnd.github+json" -H "User-Agent: kengaku-r52-C1ScoutTaskShapes" \
  "https://api.github.com/repos/harbor-framework/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1" \
  -o /fast/scratch/hyaku/kengaku-r52/C1ScoutTaskShapes/tree.json
```

Root besides the 89 task directories: `.gitignore`, `LICENSE`, `README.md`. The 89 root directories that contain `<task>/task.toml` are exactly the frozen population (`population_equals_root_dirs_that_have_task_toml: true`).

Raw fetches from `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/<path>`: every `task.toml`, `instruction.md`, `tests/test.sh`, `tests/test_outputs.py`, the five `environment/tests/test_outputs.py` shadows, `configure-git-webserver/tests/verify.sh`, `cancel-async-tasks/tests/test.py`, and `fix-code-vulnerability/environment/Dockerfile`. **364 files, 0 size mismatches, 0 git-blob SHA1 mismatches** (`blob <len>\0` + body against the tree object's `sha`).

Bottle contents API `https://api.github.com/repos/bottlepy/bottle/contents/test?ref=0207a34f0c5716cd292dd4480253ad35d3da49f3` returned HTTP 403. The second pytest target inside that checkout was **not** enumerated. That absence does not change the reward conjunction, which is in the TB2 tree.

## Histogram

Definition used (also in `shapes.json`):

- **pytest**: `tests/test.sh` writes `/logs/verifier/reward.txt` to `1` iff its **single** pytest invocation of `tests/test_outputs.py` exits 0. Path is `/tests/test_outputs.py`, or `test_outputs.py` after `cd /tests`. An `exit 1` when `PWD=/` that writes no reward is a harness precondition, not a second grader.
- **both**: reward `1` only if that pytest exits 0 **and** another command's exit status is also 0.
- **shell**: reward decided by `tests/test.sh` or `tests/verify.sh` with no pytest of `tests/test_outputs.py`.
- **neither**: none of those decide the reward.

| mechanism | tasks |
|---|---:|
| pytest `tests/test_outputs.py` | 88 |
| both (pytest on `tests/test_outputs.py` AND another status) | 1 (`fix-code-vulnerability`) |
| shell `tests/test.sh` / `tests/verify.sh` alone | 0 |
| neither | 0 |

All 89 `tests/test.sh` bodies were read. 58 unique byte-bodies; the reward tail is the same except on `fix-code-vulnerability`. Pytest path form: 87 scripts pass `/tests/test_outputs.py`; `mcmc-sampling-stan` and `rstan-to-pystan` `cd /tests` then pass `test_outputs.py` (same blob). 87 scripts `exit 1` when `PWD=/` before pytest and write no reward (`hf-model-inference` and `kv-store-grpc` have no such guard). No `task.toml` names `test.sh`, `pytest`, `reward`, `verify.sh`, or `test_outputs`. Every `[verifier]` section is only `timeout_sec` (9 distinct values; 48 are `900.0`). Every `[verifier.env]` body is empty. The entrypoint is the conventional `tests/test.sh`, not a field in the manifest.

## Manifest counts at the pin

| file | tasks | notes |
|---|---:|---|
| `<task>/task.toml` | 89 | bytes 817–1119; no zero-length; no nested copy |
| `<task>/instruction.md` | 89 | bytes 123–4365; no zero-length; no nested copy |

Both equal the frozen 89. Spot raw-check of `adaptive-rejection-sampler/instruction.md`: 2665 bytes, matches the tree object.

## Shape the frozen rules cannot speak to

**`fix-code-vulnerability`.** Frozen rules (`plans/round-52-claims.md` §C1, `primary_grader` in `plans/round52_c1_grader_audit.py`) classify only `tests/test_outputs.py`, or `environment/tests/test_outputs.py` when the task has no `tests/` grader. `primary_grader` for this task is `fix-code-vulnerability/tests/test_outputs.py`. The task tree's `tests/` contains only `test.sh` (653 bytes) and `test_outputs.py` (4010 bytes).

`tests/test.sh` lines 11–22:

```sh
# test from original repo
python -m pytest --ctrf /logs/verifier/original-repo-ctrf.json -rA
ORIGINAL_EXIT_CODE=$?
# additional test
python -m pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
ADDITIONAL_EXIT_CODE=$?

if [ $ORIGINAL_EXIT_CODE -eq 0 ] && [ $ADDITIONAL_EXIT_CODE -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
```

The path-less `python -m pytest` is a second conjunct. The script does not `cd`. `environment/Dockerfile` line 7 is `WORKDIR /app`; lines 9–11 clone `https://github.com/bottlepy/bottle.git` into `/app` and `git reset --hard 0207a34f0c5716cd292dd4480253ad35d3da49f3`. That checkout is not in the frozen population. Marker rules on `test_outputs.py` bytes have no second-suite conjunct, so they cannot speak to the whole score. (The primary file itself is not empty: six `def test_` functions, `exists(` and `open(` — the rules can still class *that file*. They cannot class the conjunction.)

## Considered, and not an unspeakable shape

- `configure-git-webserver/tests/verify.sh` (2681 bytes) prints `TEST PASSED` / `TEST FAILED` and does not write `reward.txt`. `tests/test.sh` never names it. `tests/test_outputs.py` line 11 runs `subprocess.run(["bash", "/tests/verify.sh"], ...)` and line 13 asserts `"TEST PASSED" in result.stdout`. Reward follows that pytest. `subprocess` matches the frozen behaviour marker, so the rules speak to the primary file. They do not parse `verify.sh`.
- `git-multibranch` has no `verify.sh` blob. `tests/test_outputs.py` line 8 writes a `verify.sh` string and line 96 runs `os.popen("bash verify.sh")`. `os.popen` matches the behaviour marker.
- Five `environment/tests/test_outputs.py` blobs (`break-filter-js-from-html`, `circuit-fibsqrt`, `large-scale-text-editing`, `overfull-hbox`, `schemelike-metacircular-eval`) are byte-identical to the `tests/` copies. Every task already has `tests/test_outputs.py`, so the claims-file fallback matches 0 tasks. Pytest targets the `tests/` copy.
- `fix-ocaml-gc`: `make -C testsuite one DIR=tests/basic | tee tests.txt` runs before pytest; `reward.txt` uses the pytest `$?` only.
- `cancel-async-tasks` copies `tests/test.py` to `/app/test.py`; `test_outputs.py` executes `python test.py`. Reward follows pytest. `test.py` is a driver, not a pytest module (no `def test_`).
- The `PWD=/` `exit 1` (87/89) writes no reward. Precondition, not graded assertions.

## Files

- Written then removed with the scratch tree: `/fast/scratch/hyaku/kengaku-r52/C1ScoutTaskShapes/shapes.json` (and `tree.json`, `raw/`).
- Kept: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C1ScoutTaskShapes/shapes.json` (sha256 `99e95f4b2ef049792d707c49e06f1e47a187f00fecb0113e6462d19bc90485c2`). Per-task pytest invocations, reward lines, primary grader, and shadow hashes are in that file. Member list of the 88 is `histogram_members.pytest_tests_test_outputs_py`.
