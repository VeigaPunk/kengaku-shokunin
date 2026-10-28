# C1ScoutTaskShapes

Read-only shape census of the frozen 89-task population at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`. No grader run. Full command log, quotes, and the per-task table live in `.ufo/waves/round-52/w1/C1ScoutTaskShapes/report.md` and `shapes.json` (sha256 `99e95f4b2ef049792d707c49e06f1e47a187f00fecb0113e6462d19bc90485c2`).

## Histogram (how the score is decided)

| mechanism | n |
|---|---:|
| pytest `tests/test_outputs.py` (single invocation; `tests/test.sh` copies its exit status to `/logs/verifier/reward.txt`) | 88 |
| both: pytest on `tests/test_outputs.py` **and** a path-less `python -m pytest` must both exit 0 | 1 — `fix-code-vulnerability` |
| shell `tests/test.sh` or `tests/verify.sh` alone | 0 |
| neither | 0 |

87 of the 88 pass `/tests/test_outputs.py`; `mcmc-sampling-stan` and `rstan-to-pystan` `cd /tests` then pass `test_outputs.py` (same file). No `task.toml` names the entrypoint: all 89 `[verifier]` sections set only `timeout_sec`; all 89 `[verifier.env]` bodies are empty.

## Manifest

89/89 have a non-empty `<task>/task.toml` (817–1119 bytes). 89/89 have a non-empty `<task>/instruction.md` (123–4365 bytes). Those 89 directories are exactly the frozen population. Tree API returned sha `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, `truncated: false`, 1446 entries. 364 raw files matched git-blob SHA1 with 0 mismatches.

## Unspeakable for the frozen classifier

`fix-code-vulnerability`. `primary_grader` is `tests/test_outputs.py`. `tests/test.sh` lines 12–19 require **both** `python -m pytest` with no test path (`ORIGINAL_EXIT_CODE`, ctrf `original-repo-ctrf.json`, comment "test from original repo") and `python -m pytest /tests/test_outputs.py` to exit 0 before writing reward `1`. The task tree's `tests/` is only those two files. `environment/Dockerfile` sets `WORKDIR /app` and clones `bottlepy/bottle` at `0207a34f0c5716cd292dd4480253ad35d3da49f3` into `/app` (not in the population). Rules that read only the primary grader have no second-suite conjunct. Bottle's `test/` listing was not fetched (contents API HTTP 403); the conjunction itself is in the pin.

Not unspeakable: `configure-git-webserver/tests/verify.sh` is a subprocess probe from `test_outputs.py` (behaviour marker), not a second reward writer; `git-multibranch` embeds its shell in `test_outputs.py` (`os.popen`); five `environment/tests/test_outputs.py` copies are byte-identical to `tests/` and are not the pytest target (environment fallback matches 0 tasks).
