On Docker (the default environment), the host paths of the trial's log dirs are visible inside the container in `/proc/self/mountinfo`. They include the job name and the task name, and often the host username and checkout path. Podman and Singularity bind the same host paths, so they should show them too. kata and apple-container run the container in a VM, and I haven't checked what their mountinfo shows. Cloud environments don't leak the path: Harbor either copies the logs out, or binds `/logs/...` to the same path on the sandbox VM.

From a local docker run on macOS (OrbStack), where the agent just reads `/proc/self/mountinfo`:

```
213 204 0:37 /private/tmp/harbor-3576/probe/jobs/probe-alpine/hello-alpine__Kepx5n5/verifier /logs/verifier rw,relatime - virtiofs mac rw
214 204 0:37 /private/tmp/harbor-3576/probe/jobs/probe-alpine/hello-alpine__Kepx5n5/agent /logs/agent rw,relatime - virtiofs mac rw
```

With the default jobs dir the path is `<cwd>/jobs/<YYYY-MM-DD__HH-MM-SS>/<task>__<id>/...`. `findmnt` and `/proc/1/mountinfo` show the same thing. `mount` and `df` only show the device.

I found this while looking into #3576, but it's more than an eval-awareness cue: the task name is enough to look up the public task. Two runs in the TB2 leaderboard data ([harborframework/terminal-bench-2-leaderboard](https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard)) did that.

[`JJAgent__Multiple`, `db-wal-recovery__QqxwMqd`](https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard/blob/main/submissions/terminal-bench/2.0/JJAgent__Multiple/2026-05-04__14-46-15/db-wal-recovery__QqxwMqd/agent/trajectory.json) (step numbers are the `step_id`s in the file):

- step 43: `cat /proc/self/mountinfo` returns `/home/user/pyenv/projects/tb-eval/jobs/2026-05-04__14-46-15/db-wal-recovery__QqxwMqd/agent /logs/agent`. This is the first time the task name appears anywhere in the transcript.
- step 68: "I'm looking for the benchmark fixture or generator in the accessible filesystem."
- step 74: web search for `"db-wal-recovery" "main.db-wal"`
- step 75: opens `huggingface.co/datasets/zai-org/terminal-bench-2-verified/tree/main/db-wal-recovery/environment`
- step 78: downloads `main.db-wal.encrypted` from that repo (step 79 also downloads `main.db`, only to check it matches the local copy). It then XOR-decodes the WAL and writes `/app/recovered.json` from it.

The agent's own source (`jj_agent/codex_route.py`) also lists TB2 task names. Its search for the task name at step 69 hit that file, and at step 73 it searched its own source directly. So mountinfo was the first leak in this run, not the only one.

[`CodeBrain-1__GPT-5.3-Codex`, `db-wal-recovery__25qd4LB`](https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard/blob/main/submissions/terminal-bench/2.0/CodeBrain-1__GPT-5.3-Codex/2026-02-08__20-43-33/db-wal-recovery__25qd4LB/agent/trajectory.json): it reads mountinfo (the output is masked in the published file), then tries to `ls` the host job dir "referenced in mountinfo". It web-searches `"db-wal-recovery"`, clones `laude-institute/terminal-bench-2`, and reads the task's `solution/solve.sh` and `tests/test_outputs.py`.

This is rare. Of the 11,771 trajectories in that dataset, 9 show a host job path from mountinfo in a tool result, plus the masked CodeBrain run. All of them are db-wal-recovery runs, where agents often end up searching the whole filesystem for an intact copy of the WAL. 8 of the 9 then went through `/logs/verifier`, `/logs/agent` or `/logs/artifacts`, though several were already doing that before they read mountinfo.

Where it comes from: the bind sources are the resolved host trial dirs in [`Trial._agent_env_mounts`](https://github.com/harbor-framework/harbor/blob/862d472390c08031e3fbf944f0a253f3c2affa21/src/harbor/trial/trial.py#L1894-L1928). On docker they're written into a compose override by [`write_mounts_compose_file`](https://github.com/harbor-framework/harbor/blob/862d472390c08031e3fbf944f0a253f3c2affa21/src/harbor/environments/docker/__init__.py#L28-L33). Task compose files also get the same paths as `HOST_AGENT_LOGS_PATH` etc.

mountinfo isn't the only place the task name reaches the container. The compose project name is `<task>__<id>__env`, which shows up in reverse DNS of the container's own IP (#3223 tried to make it opaque). terminus-2 also writes a `session_id` of `<task>__<id>__agent` into `/logs/agent/trajectory.json`. Fixing mountinfo alone would still leave those.

Possible fixes (no strong preference):

1. Don't bind-mount the log dirs on docker. Keep them in the container and copy them out after each phase, the way non-mounted environments already do. #2757 (closed, not merged) proposed this as an opt-in mode. Costs: no live view of logs on the host while the agent runs; partial logs are lost if Harbor is killed; and task compose files that bind `${HOST_*_PATH}` themselves would still leak. If named volumes are used instead, they need a random name — compose prefixes volume names with the project name.
2. Bind from a staging dir whose path has no job or task name, for example by making the trial's `agent/`, `verifier/` and artifacts dirs symlinks to it during the run. Harbor already resolves the source before handing it to docker, so mountinfo would show the staging path. Where the staging dir lives matters: under the jobs dir it still exposes the checkout path, and some macOS docker setups don't share the system temp dir. Multi-step trials would need a change too, because step archiving rejects symlinked dirs.
3. Drop the task name from trial and session names. Harbor itself barely depends on it (resume matches on `config.json`), but people's scripts and published datasets do. It's the only option that also covers reverse DNS and terminus-2's `session_id`.

I'm happy to send a PR for whichever one you'd take. Related: #3576 (eval-awareness cues), #2525 (trial dirs are 0777 so that non-root agents can write to these bind mounts, which any change here has to keep working).

I used Claude Code to search the transcripts, look up the code and draft this issue.
