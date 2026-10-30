# dynamo/log-report — a repaired Terminal-Bench 2 (Harbor) task

[![Verified with Harbor](https://img.shields.io/badge/verified%20with-Harbor%200.18.0-2b6cb0)](https://github.com/harbor-framework/terminal-bench-2)
[![Oracle](https://img.shields.io/badge/oracle-reward%201.0-2f855a)](#verification-evidence)
[![Nop agent](https://img.shields.io/badge/nop%20agent-reward%200.0-c53030)](#verification-evidence)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

This repository contains a repaired [Terminal-Bench 2](https://github.com/harbor-framework/terminal-bench-2) / [Harbor](https://harborframework.com) task, produced for the Project Dynamo "Fix the Broken Terminal-Bench Task" exercise.

The underlying task is intentionally simple — parse an Apache-style access log into a small JSON report — because the exercise isn't about the domain. It's about recognizing and repairing bad **task authoring**: a task.toml that doesn't validate against the real Harbor schema, a Dockerfile that leaks the answer key into the agent's own filesystem, a verifier that rubber-stamps any output, and instructions that don't describe what's actually being graded.

Every claim in this README is backed by a real `harbor run` invocation — output is pasted verbatim, not reconstructed. See [Verification evidence](#verification-evidence).

## Table of contents

- [Repository layout](#repository-layout)
- [Defects found and fixed](#defects-found-and-fixed)
- [Confirmed non-defects (traps)](#confirmed-non-defects-traps)
- [Reproducing this locally](#reproducing-this-locally)
- [Verification evidence](#verification-evidence)
- [Proof the verifier catches a wrong solution](#proof-the-verifier-catches-a-wrong-solution)
- [Environment note: Colima and bind mounts](#environment-note-colima-and-bind-mounts)

## Repository layout

```
log-report/
├── task.toml                    # Harbor task manifest (metadata, resource limits, artifacts)
├── instruction.md               # Task prompt shown to the agent — numbered success criteria
├── environment/
│   ├── Dockerfile                # Agent's environment image (digest-pinned base, no leaked solution)
│   └── access.log                 # 6-line Apache-style access log the agent must parse
├── solution/
│   ├── solve.py                   # Reference (oracle) implementation
│   └── solve.sh                   # Entry point Harbor's `oracle` agent runs
└── tests/
    ├── test.sh                    # Verifier entry point — runs pytest, writes reward + ctrf
    └── test_outputs.py            # 5 tests, one per instruction.md success criterion
```

## Defects found and fixed

The task as delivered had **six real defects**, spanning all four axes of a correct Harbor task: format, environment, verifier, and instructions.

### 1. `task.toml` — malformed and mismatched `artifacts` field (format)

```diff
- artifacts = "/app/out.json"
+ artifacts = ["/app/report.json"]
```

TB2's schema requires `artifacts` to be an array. Beyond the type error, it pointed at `/app/out.json` — a file the task never produces. The actual output, written by `solve.py`, is `/app/report.json`. A task whose declared artifact doesn't match its real output can't be reliably archived or reviewed.

### 2. `environment/Dockerfile` — unpinned, non-reproducible base image (environment)

```diff
- FROM python:latest
+ FROM python:3.13-slim-bookworm@sha256:fcbd8dfc2605ba7c2eca646846c5e892b2931e41f6227985154a596f26ab8ed7
```

`python:latest` is a moving tag — the "same" task builds a different image every time it's rebuilt, silently, with no record of what changed. Pinned to the exact manifest-list digest for `python:3.13-slim-bookworm` (the same tag family used by other real tasks in the [terminal-bench-2](https://github.com/harbor-framework/terminal-bench-2) registry, e.g. `build-cython-ext`, `filter-js-from-html`), resolved directly against the Docker Hub registry API for full reproducibility.

### 3. `environment/solution_hint.py` — the reference solution leaked into the agent image (environment)

The original `environment/` directory contained a file that was a byte-for-byte copy of the oracle's parsing logic — its own comment admitted it: *"Reference implementation (leaked into the agent image by mistake)."* The Dockerfile then `COPY`'d it straight into `/app`, meaning any agent evaluated on this task could just read its own filesystem to find the answer.

**Fix:** deleted `solution_hint.py` entirely and removed the `COPY` line from the Dockerfile.

### 4. `tests/test_outputs.py` — gameable verifier (verifier)

The original verifier was two assertions:

```python
def test_report_exists():
    assert Path("/app/report.json").exists()

def test_report_nonempty():
    assert Path("/app/report.json").stat().st_size > 0
```

This checks that *a file was touched*, not that the task was solved. All of the following would have **passed**:
- `echo '{}' > /app/report.json` (empty object, no required keys)
- `echo 'not json' > /app/report.json` (not even valid JSON)
- `cp /app/access.log /app/report.json` (the raw log, unparsed)
- A well-formed report with every field wrong

**Fix:** rewrote as five tests, each checking one exact value against ground truth hand-computed from `environment/access.log`, and each docstring names the `instruction.md` success criterion it verifies (1:1 mapping, no missing or extra checks):

```python
def test_criterion_3_total_requests_correct():
    """instruction.md success criterion 3: total_requests equals the number
    of non-empty lines in /app/access.log."""
    data = json.loads(REPORT_PATH.read_text())
    assert data["total_requests"] == EXPECTED_TOTAL_REQUESTS, (
        f"total_requests: expected {EXPECTED_TOTAL_REQUESTS}, got {data['total_requests']!r}"
    )
```

### 5. `tests/test.sh` — reward written to the wrong path, no CTRF report (verifier)

```diff
- pytest /tests/test_outputs.py -rA
- if [ $? -eq 0 ]; then echo 1 > /app/reward.txt; else echo 0 > /app/reward.txt; fi
+ mkdir -p /logs/verifier
+ pytest /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json
+ if [ $? -eq 0 ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
```

Harbor reads the reward from `/logs/verifier/reward.txt` — the original script wrote to `/app/reward.txt`, a path Harbor never looks at, so even a *correct* verifier's signal would never reach the harness. It also never generated `ctrf.json` despite `pytest-json-ctrf` being installed in the image. Note `set -e` was deliberately **not** added: with it, a failing `pytest` would abort the script before the `if` block could write `reward.txt` at all.

### 6. `instruction.md` — ambiguous, inconsistent with the verifier (instructions)

Original, in full:

> There is an access log in the working directory. Analyze the traffic and summarize what you find — how many requests there were, the clients involved, and which pages were popular. Save your findings so they can be reviewed.

No output path, no filename, no field names, no schema, no numbered criteria. An agent had no way to converge on the exact contract the verifier checks, because the instruction and the verifier were effectively describing two different tasks.

**Fix:** rewrote with the exact output path (`/app/report.json`), the exact schema (`total_requests`, `unique_ips`, `top_path`), and five numbered success criteria that map 1:1 onto the five verifier tests.

## Confirmed non-defects (traps)

The exercise's diagnostic checklist included four options that looked plausible but were **not** real defects. Each was checked, not assumed:

| Claim | Verdict | Evidence |
|---|---|---|
| `access.log` is corrupted | False | Hand-parsed all 6 lines — well-formed Apache combined-log format, no corruption |
| Task requires network access to be solved | False | Pure local file parsing; `allow_internet` is set in `task.toml` but nothing in the solution path touches the network |
| `solve.py`/`solve.sh` computes the wrong answer | False | Hand-traced the log: 6 requests, 3 unique IPs, `/index.html` top with 3 hits vs. `/about.html`=2, `/api/login`=1 — matches the oracle's output exactly (confirmed again by the real `harbor run -a oracle` below) |
| `memory_mb = 2048` is too low for the verifier | False | A 6-line pytest run needs a small fraction of that; the real run took 12s wall-clock with no memory pressure |

## Reproducing this locally

```bash
# 1. Install Harbor (Python ≥3.12 required)
python3.13 -m venv .venv && source .venv/bin/activate
pip install harbor

# 2. Docker daemon — Docker Desktop, or on macOS without it, Colima:
brew install colima docker docker-compose
colima start
# See the Colima note below before running from a path under /tmp.

# 3. From the repo root:
harbor run -p log-report -a oracle      # expect reward 1.0
harbor run -p log-report --agent nop    # expect reward 0.0
```

## Verification evidence

All output below is copied verbatim from real `harbor run` invocations (Harbor 0.18.0, Docker Engine 29.6.1 via Colima) executed while preparing this fix.

### Oracle agent — reward 1.0

```
$ harbor run -p log-report -a oracle
  1/1 Mean: 1.000 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:12
┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 1.0    │     1 │
└────────┴───────┘
```

`/logs/verifier/reward.txt`:
```
1
```

`/logs/verifier/ctrf.json` summary:
```json
{"tests": 5, "passed": 5, "failed": 0, "skipped": 0}
```

`/logs/verifier/test-stdout.txt`:
```
collected 5 items
../tests/test_outputs.py .....                                           [100%]
============================== 5 passed in 0.01s ===============================
```

### `nop` agent — reward 0.0

```
$ harbor run -p log-report --agent nop
  1/1 Mean: 0.000 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:13
┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 0.0    │     1 │
└────────┴───────┘
```

`/logs/verifier/reward.txt`:
```
0
```

`/logs/verifier/ctrf.json` summary:
```json
{"tests": 5, "passed": 0, "failed": 5}
```

First failure in `/logs/verifier/test-stdout.txt`:
```
E       AssertionError: no report.json found at /app/report.json
E       assert False
E        +  where False = exists()
```

## Proof the verifier catches a wrong solution

To confirm the verifier checks real values rather than just structural presence, a deliberate off-by-one bug was injected into `solution/solve.py`:

```diff
  json.dump(
      {
-         "total_requests": total,
+         "total_requests": total + 1,  # BUG: off-by-one, injected to prove the verifier catches it
          "unique_ips": len(ips),
          "top_path": paths.most_common(1)[0][0],
      },
      out,
  )
```

Re-running the oracle against the bugged solution:

```
$ harbor run -p log-report -a oracle
  1/1 Mean: 0.000 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 0:00:12
┏━━━━━━━━┳━━━━━━━┓
┃ Reward ┃ Count ┃
┡━━━━━━━━╇━━━━━━━┩
│ 0.0    │     1 │
└────────┴───────┘
```

`/logs/verifier/reward.txt`: `0`. Pytest pinpoints exactly the injected defect, and only it:

```
../tests/test_outputs.py ..F..                                           [100%]
=================================== FAILURES ===================================
___________________ test_criterion_3_total_requests_correct ____________________
E       AssertionError: total_requests: expected 6, got 7
E       assert 7 == 6
========================= 1 failed, 4 passed in 0.02s ==========================
```

`test_criterion_3` (the `total_requests` check) fails; the other four criteria — file existence, valid JSON, `unique_ips`, `top_path` — still correctly pass, since the bug didn't touch them. This is the behavior a value-checking verifier should have and the original existence-only verifier could never provide, no matter what was injected.

## Environment note: Colima and bind mounts

While reproducing this on macOS without Docker Desktop (using Colima instead), `harbor run` initially failed with `RewardFileNotFoundError` even though `tests/test.sh` ran correctly inside the container. Root cause: Colima's default VM configuration does not bind-mount `/tmp` (or `/private/tmp`) into the guest, so files Harbor expects to read back via a live bind mount at `/logs/verifier/reward.txt` were invisible on the host — confirmed independently with a minimal `docker run -v /tmp/x:/y alpine ...` reproduction. Running Harbor from a working directory under `$HOME` (which Colima does mount by default) resolved it. This is a Colima/host-tooling quirk, not a defect in the task itself, and is documented here for anyone else reproducing this on Colima.

## License

[MIT](LICENSE)
