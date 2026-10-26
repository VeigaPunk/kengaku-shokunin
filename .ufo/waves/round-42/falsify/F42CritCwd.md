# F42CritCwd — Harbor cwd claim

**Axes:** source freshness (Harbor pins), empirical coverage (16-case cwd comparison), entry accuracy.

## Result

Harbor source supports the default cwd claim for this task: its verifier calls `environment.exec(command=...)` without a `cwd`; Docker adds `-w` only when a cwd is truthy; `task.toml` has no `environment.workdir`; and the pinned image config reports `WorkingDir=/app`. Thus the task's default shared Docker verifier runs `/tests/test.sh` at `/app`. The entry's qualification “under any other writable cwd” is too broad if read literally: the tested alternative is one writable cwd, `/w`, and `/` is explicitly a non-verdict case because `test.sh` exits before grading. Also the nine-moved result depends on the stated end states and probe setup; it is not established for every possible writable directory / agent-produced filesystem state.

## Source evidence

At Harbor HEAD pin `c080078c6b8a8a1db9a781380e15ed14189ad8d1` (clone log: `2026-10-26T13:10:19-07:00`), `src/harbor/verifier/verifier.py:267-272` invokes `self.environment.exec(command=command, env=env)` with no `cwd`. `:209-227` uploads tests to `/tests` in `verify()`, after the single-step flow's `_run_agent()` (`src/harbor/trial/single_step.py:38-51`). `single_step.py:104-108` chooses shared verification for shared mode; `resolve_task_verifier_mode` defaults to shared (`src/harbor/models/task/verifier_mode.py:29-31`). `trial.py:992-1000` passes the agent environment into the shared verifier.

At HEAD, `src/harbor/environments/docker/docker.py:1366-1369` sets effective cwd to `cwd or self.task_env_config.workdir`, and `:1415-1416` adds `-w` only if cwd is truthy. The prebuilt compose service has no `working_dir` or `user` setting (`docker-compose-prebuilt.yaml:1-4`). Config docs/code say task `workdir` overrides the image WORKDIR (`config.py:479-483`); the captured `task.toml` has no workdir. Captured image config at `.ufo/waves/round-42/build/R42ScoutHarborCwd/cfg.json` says `WorkingDir=/app` and has no `User` key. Thus compose exec inherits `/app` from the image for this task. Caveat: `VerifierConfig.user=None` doesn't alone prove root in all task setups, since shared mode temporarily sets the default user to the task's agent user (`trial.py:992`); this assignment concerns cwd, not that user claim.

The second pin, Harbor `60676c3120f98985583e834118e532620586441c`, was confirmed by clone log as 2025-11-07 commit “Fix test.sh in example task (#105)”. Its `src/harbor/verifier/verifier.py:82-112` invokes `environment.exec(command=...)` with no cwd; `src/harbor/environments/docker/docker.py:242-259` adds `-w` only when cwd is set. This independently supports the no-explicit-cwd mechanism at the release-era pin. The image config is the captured task image, not a Harbor source artifact.

## Reproduction

Copied the frozen probe (`sha256 fc58bf3f1780aaefee9df1e635b01765d3fb5d9224f1958494df4e1b8ed061b3`) to `/fast/scratch/hyaku/kengaku-r42/F42CritCwd/probe_cwd2.py` (modified-copy sha256 `4a3bd94c21dcfea05c31039e2b01f671691ac918a53ba1fcbf47144cab7fde5e`). The only behavioral changes in the copy were an `os.chdir(GRADE_CWD)` after the recipe stage and a writable `/w` directory / `GRADE_CWD` setting in its bwrap setup. The probe itself grades copied pinned captures, and does not alter the lane.

Both runs used the required outer envelope:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>`

`out_app.txt`: `GRADE_CWD=/app TMPDIR=$S timeout 3000 bwrap ... python3 probe_cwd2.py --lane ... --work ...`; output `regrade cases=16 differ=0`, `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, rc=0. This matches `corpus/evidence/round42/fibsqrt-probe.txt` case-for-case.

`out_w.txt`: same command with `GRADE_CWD=/w`; output `regrade cases=16 differ=0`, `cases=16 observed_pass=1 observed_fail=15 mismatches=9`, rc=0. The output records: `oracle-solve-sh` PPP→PPF, `lookup-28` PPP→PPF, `lookup-28-plus-examples` PPP→PPF, `lookup-28-padded-31999` PPP→PPF, `lookup-28-comment-lines` PPP→PPF, `lookup-28-reversed-lines` PPP→PPF, `lookup-28-crlf` PPP→PPF, `lookup-28-padded-32000` PFP→PFF, and `fake-sim-script` PPF→PPP. The first eight fail because the grader compiles `./sim` in `/w` but executes `/app/sim`, which is absent; `fake-sim-script` flips to pass because its pre-existing `/app/sim` is no longer overwritten by the compile. Thus exactly nine *overall verdicts* move under the tested `/w` condition. The other seven overall pass/fail verdicts stay the same; some test-letter strings may differ while the overall verdict stays fail.

Envelope receipts `env_app.txt` and `env_w.txt` record date and `.local/bin` directory digest before/after. `env_app.txt` hashes were `77408cab...` before and after; final host digest was `8cf5b151...` at 18:07:26. No tools installed.

## Smallest safe correction

Keep the entry's core cwd conclusion, but replace “under any other writable cwd” with a bounded statement such as: “In the probe, changing grading cwd from `/app` to writable `/w` moves nine of sixteen overall verdicts (list the cases); this is a controlled cwd variant, not a claim about every cwd or arbitrary agent-built `/app/sim`.” The `/app` conclusion is right for this pinned task configuration. `/` is not an alternative graded cwd: captured `test.sh:13-16` exits there before pytest.

VERDICT: cwd-claim-confirmed-moved-9/16