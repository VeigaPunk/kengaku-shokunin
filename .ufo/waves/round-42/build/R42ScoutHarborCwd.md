# R42ScoutHarborCwd — where does Harbor run `tests/test.sh` (cwd, user, /tests timing)?

Seat: scout, kengaku r42 wave 1. Question: the probe assumes cwd `/app`; can the real verifier's cwd differ, and which receipt cases change?

## 0. Answer (one paragraph)

For `circuit-fibsqrt` (task.toml has no `[environment].workdir`; prebuilt image `alexgshaw/circuit-fibsqrt:20251031` has `WorkingDir=/app`, `User=None`), Harbor's Docker verifier does `docker compose exec` with **no `-w`** and no `-u`, so `test.sh` runs as **root** (image default) in the image **WORKDIR `/app`**, in the **same container the agent used (shared mode)**, with `/tests` **uploaded after the agent finished**. The probe's cwd=/app assumption holds for the default configuration. The cwd can differ only if a task sets `[environment].workdir` (this one does not), a non-Docker provider ignores the image WORKDIR (none found for the providers read), or a local re-run is started from another directory. If cwd were another writable dir `X` (not `/`), **9 of 16** receipt cases would change (measured, §4): 8 pass→fail or PFP→PFF, 1 fail→pass. Seven are unchanged. cwd `/` is refused by `test.sh` itself.

## 1. Pins

- Harbor HEAD cloned 2026-10-26: https://github.com/harbor-framework/harbor (the old URL github.com/laude-institute/harbor redirects/was renamed; the API fetch of the old URL returned `harbor-framework/harbor`) at `c080078c6b8a8a1db9a781380e15ed14189ad8d1` (2026-10-26T13:10:19-07:00, "fix(vercel): support vercel-sandbox >= 0.7 (#3872)").
- TB2-release-era Harbor: `60676c3120f98985583e834118e532620586441c` (2025-11-07T23:01:18-08:00, "Fix test.sh in example task (#105)"), the last commit before 2025-11-08; TB2 pin `2fd12b88…` is the dataset commit, not Harbor.
- Harbor README names the harness: "Harbor is the official harness for [Terminal-Bench-2.0](https://github.com/laude-institute/terminal-bench-2)" (README.md, "Example: Running Terminal-Bench-2.0").
- Captured task files (lane `corpus/evidence/round42/tb2-circuit-fibsqrt/`): `Dockerfile:3` `WORKDIR /app`; `task.toml:27-29` `[environment] … docker_image = "alexgshaw/circuit-fibsqrt:20251031"`; no `workdir` key anywhere in task.toml (lines 1-41 read); `test.sh:13` `if [ "$PWD" = "/" ]; then … exit 1`.
- Image config read from Docker Hub (anonymous token; manifest `alexgshaw/circuit-fibsqrt:20251031` → config blob `sha256:133688d2a04ad9fd39267badd3d61ac22c91c09162d682e44d4396b3445123ab`, saved as `R42ScoutHarborCwd/cfg.json`, sha256 equal to the digest): `User: None`, `WorkingDir: '/app'`, `Cmd: ['python3']`, `Entrypoint: None`, `created 2025-09-13T18:39:18Z`. History tail: `WORKDIR /app`, `RUN apt-get install -y gcc`, `COPY tests/sim.c /app`, `COPY gates.txt /app`. (So the image holds `/app/sim.c`, `/app/gates.txt`, **no** `/app/sim`.)

## 2. How the verifier runs `test.sh` (HEAD `c080078c`)

Flow (single-step task, default mode shared): `src/harbor/trial/single_step.py`
- `:40` `await self._run_agent()` … `:51` `await self._run_verifier()` — the agent phase and artifact collection precede the verifier.
- `:95` `user = self.task.config.verifier.user`; `:105` `self.result.verifier_result = await self._run_shared_verifier(`.
- Mode default: `src/harbor/models/task/verifier_mode.py:31` `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED`. Separate mode only when a verifier `environment` is set (`src/harbor/models/task/config.py:~590`, `environment_mode` description "defaults to 'separate' if a verifier 'environment' is set").
- `src/harbor/trial/trial.py:992` `with self.agent_environment.with_default_user(user):` — the **agent's own environment** (same container) runs the verifier.
- `src/harbor/models/task/config.py:583-587` (`VerifierConfig.user`): "Username or UID to run the verifier as. None uses the environment's default USER (e.g., root)." task.toml has `[verifier] timeout_sec = 3600.0` only → `user=None`.

`src/harbor/verifier/verifier.py`:
- `:209-227` upload of `tests_dir` to `env_paths.tests_dir` (`/tests`) happens inside `verify()`, i.e. after the agent finished.
- `:245-248` `test_script_path = str(env_paths.tests_dir / host_test_path.relative_to(tests_source_dir).as_posix())` → `/tests/test.sh`.
- `:255-259` `command = build_execution_command(test_script_path, stdout_path=test_stdout_path, task_os=…)`.
- `:261-265` `needs_chmod` → `chmod +x … ` with `user="root"`.
- `:267-272` "# Runs as ``environment.default_user``, which the caller must set …" then `await self.environment.exec(command=command, env=env,)` — **no `cwd=` argument**.

`src/harbor/environments/docker/docker.py`:
- `:1366` `cwd=cwd or self.task_env_config.workdir,` (None when task.toml sets no workdir); `:1369` `user=self._resolve_user(user),`.
- `:1415-1416` `if cwd: exec_command.extend(["-w", cwd])` — with cwd None no `-w`, so `docker compose exec main …` starts in the image's `WorkingDir` (`/app`).
- `src/harbor/environments/base.py:569` `return user if user is not None else self.default_user` → None → no `-u` (image USER = root).
- `src/harbor/environments/docker/docker-compose-prebuilt.yaml` (HEAD lines 1-4 read; at `60676c31` lines 1-14): service `main`, `image: ${PREBUILT_IMAGE_NAME}`, `command: [ "sh", "-c", "sleep infinity" ]`, no `working_dir`/`user` keys. (`grep working_dir src/harbor/environments/docker/*` empty.)

Config knob that *can* change cwd: `src/harbor/models/task/config.py:479-483` `workdir: str | None … "Default working directory for command execution. Overrides the container's WORKDIR when set."`; docs `docs-mintlify/tasks/configuration.mdx:277-278` and `docs-mintlify/tasks/verifier.mdx:6` ("`tests/test.sh` is executed in the task's working directory"; `:20` "We recommend using **absolute paths** inside the script to avoid `cwd` surprises."). This task sets none.

Other providers (HEAD, read where the exec cwd is chosen): `src/harbor/environments/definition.py:167-172` `effective_exec_cwd(cwd, config_workdir, dockerfile_workdir)` returns `cwd or config_workdir or dockerfile_workdir`; modal.py:1564-1568 uses it with `parse_dockerfile_workdir` (definition.py:138) — for a Dockerfile `WORKDIR /app` that is still `/app`. beam/blaxel/prime similar (blaxel defaults `"/"` when it finds no Dockerfile WORKDIR; prime.py:499 `cwd or ("/" if self._compose else workdir)`). Not exercised; named as unverified for the real leaderboard providers.

## 3. At the TB2-release-era Harbor (`60676c31`, 2025-11-07)

`src/harbor/verifier/verifier.py`:
- `:82-85` `await self.environment.upload_dir(source_dir=self.task.paths.tests_dir, target_dir="/tests",)` (inside `verify()`, after the agent).
- `:91-112` `await self.environment.exec(command=" ".join(["bash", str(Path("/tests")/…), "|", "tee", …, "2>&1"]))` — no cwd, no user.
`src/harbor/environments/docker/docker.py:242-259` (that commit): `if cwd: exec_command.extend(["-w", cwd])` … `exec_command.extend(["bash", "-ic", command])` — no `-w` without cwd; interactive `bash -ic`, still the image WORKDIR. No `user` concept existed; root.

Same answer at both pins: cwd = image WORKDIR = `/app`, user = root, `/tests` uploaded at verify time.

## 4. Which receipt cases change if cwd ≠ /app (measured)

Mechanism: `test_outputs.py:65-66` compiles `["gcc","-O3","/tests/sim.c","-o","sim"]` into the **cwd**, then `:119` runs `["/app/sim", N]`; `sim.c:101,319` `fopen("gates.txt")` / `parse_gates("gates.txt")` is cwd-relative. With cwd `X ≠ /app`: the fresh binary lands in `X/sim`, but the grader runs `/app/sim` — which does not exist in the image/probe end state (only `/app/sim.c`) unless the agent built it — and any `/app/sim` would read `X/gates.txt`.

Experiment (scratch copy of the frozen probe, **not** the frozen file: `probe_cwd.py` = `fibsqrt_probe.py` + `os.chdir($GRADE_CWD)` after the recipe stage and `--dir /w` in the sandbox; the recipe still runs in /app; sha256 of the copy `4a3bd94c…`, in `R42ScoutHarborCwd/`). Three runs in the host-safety envelope (`envelope.txt`):

| GRADE_CWD | output | sha256 | result line |
|---|---|---|---|
| `/app` (control) | `out_app.txt` | `1b475e56…` | `cases=16 observed_pass=7 observed_fail=9 mismatches=0`; with the trailing `rc=0` stripped it is **byte-identical** to the frozen receipt `corpus/evidence/round42/fibsqrt-probe.txt` (`diff` printed APP-IDENTICAL-TO-RECEIPT) |
| `/w` (empty writable dir) | `out_w.txt` | `f19cf3ad…` | `cases=16 observed_pass=1 observed_fail=15 mismatches=9` |
| `/tests` (a sandbox dir, writable — `--dir /tests` is on the sandbox tmpfs, not read-only) | `out_tests.txt` | `f19cf3ad…` (same bytes) | same as `/w` |

The nine cases that change (tests letters: receipt → other cwd; error text `test_sqrt_fib:error=FileNotFoundError` on every case that reaches test 3 without `/app/sim`):
1. `oracle-solve-sh` PPP → PPF
2. `lookup-28` PPP → PPF
3. `lookup-28-plus-examples` PPP → PPF
4. `lookup-28-padded-31999` PPP → PPF
5. `lookup-28-comment-lines` PPP → PPF
6. `lookup-28-reversed-lines` PPP → PPF
7. `lookup-28-crlf` PPP → PPF
8. `lookup-28-padded-32000` PFP → PFF
9. `fake-sim-script` PPF → **PPP** (the executable `/app/sim` script is no longer overwritten by the grader's compile, so it prints the right answers: a fail→pass flip; the `fake-sim-script` PPF verdict exists only because cwd = /app).

Unchanged (7): `nop` PPF, `no-gates-file` FFF, `empty-gates-file` PPF, `lookup-27-drop-48401` PPF, `lookup-28-bitflip-41` PPF, `lookup-28-trailing-space` PPF, `gates-is-directory` PFF. Tests 1-2 never depend on cwd (absolute `/app/gates.txt`, `:9,:16`).

cwd `/`: `test.sh:13-16` exits 1 before pytest runs (no verdicts at all, reward not written to 1; `reward.txt` never created → Harbor `RewardFileNotFoundError`, verifier.py:304) — none of the 16 receipt rows exist in that regime.

Limits: (a) the experiment varies the grader cwd only; if an agent had compiled `/app/sim` itself, the non-/app cwd outcomes would differ again (that `/app/sim` would read `X/gates.txt`); (b) docker/prebuilt provider read in full at both pins, other providers only by grep of the cwd-selection line; (c) the image was not pulled, only its manifest/config read; (d) the unmodified-run claim "cwd=/app" is derived from source + image config, no live Harbor run (no Docker pull attempted). Host python/gcc stand in for the image's, as the claims file already names.

## 5. Suggested entry text (for the L1)

"Harbor runs `/tests/test.sh` via `docker compose exec` with no `-w`/`-u` (verifier.py:267-272 @ c080078c; docker.py:1415-1416), so cwd is the image WORKDIR `/app` (image config `WorkingDir=/app`, `User=None`) and `/tests` is uploaded after the agent (verifier.py:209-227). The receipt's pass/fail map is valid for that cwd only: with any other writable cwd nine of sixteen verdicts change (the grader compiles `./sim` in the cwd but runs `/app/sim`)."

## 6. Q32 evidence

- Envelope line (`envelope.txt`, sha256 `1530d35f…`): `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` wrapping `run.sh`.
- `date +%T` before/after the three runs: 17:23:32 / 17:24:46 (job); report-time check 17:21:39 at seat start, 17:25:14 at end.
- `ls -A /home/vgpnk/.local/bin | sha256sum` before (17:21:39) and after (17:25:14): `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` both.
- Files in `.ufo/waves/round-42/build/R42ScoutHarborCwd/`: out_app.txt, out_w.txt, out_tests.txt, probe_cwd.py, run.sh, envelope.txt, cfg.json (all <1 MiB). Nothing in the lane was edited; the Harbor clone lived in scratch `/fast/scratch/hyaku/kengaku-r42/R42ScoutHarborCwd`.

VERDICT: harbor-cwd-app
