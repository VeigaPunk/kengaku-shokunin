SOURCE-URL: https://docs.harborframework.com/news/reward-hacking.md
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.harborframework.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Cracking down on reward hacking

> Infrastructure hardening, best practices, and tools to mitigate reward hacking in Harbor tasks.

[← All news](https://docs.harborframework.com/news.md)

October 28, 2026 · The Harbor Team

The world is transitioning from *hand-crafted* software to *learned* software. As the development lifecycle moves away from design & implementation and towards evaluation & optimization, the role of humans increasingly becomes reward shaping. Those rewards dictate the optimization loops that will eventually power all digital technology development.

However, designing rewards is difficult. Accurately measuring outcomes requires actively protecting against unexpected, undesired, and adversarial behavior. Preventing reward hacking is necessary to ensure that the evaluation & optimization loop is "hill-climbing" the right hill.

This new development paradigm requires new tools and best practices. We're shipping a batch of new features to mitigate reward hacking. Harbor is built to make *minimal* assumptions for *maximal* expressiveness, so some of these features are built into Harbor, some are opt-in tools, and some are example tasks.

## What counts as a reward hack

Reward hacking occurs when an agent receives a reward that doesn't reflect the intended completion of the task, by exploiting the environment, verifier, or underlying infrastructure.

Three types of reward hacks in Harbor are:

| Kind | What the agent does | Example |
| - | - | - |
| Tampering | Interferes with and subverts the grading process | Plants code that patches the grader, or a symlink that points it at the reference solution |
| Cheating | Gets the answer from somewhere it shouldn't | Looks up the benchmark's solution online |
| Loopholes | Satisfies the tests without solving the problem | Hard-codes outputs for cases the tests happen to check |

Mitigating these reward hacks requires robust infrastructure and tasks. There is no silver bullet, but the features below increase infra guarantees, enable better task creation, and improve reward-hacking-detection tooling.

## Three chances to mitigate reward hacking

We've addressed reward hacking in three stages: when a task is written, while it runs, and after it finishes.

Before the run
[harbor initnew task defaults](#separate-verifiers-by-default)
[harbor lintstatic checks](#catch-weak-spots-with-harbor-lint)
[harbor checkrubric review](#review-the-whole-task-with-harbor-check)
[.harborignoreunit test verifiers](#support-dev-files-during-task-development)
[Multiple solutionsavoid overfitting](#ship-multiple-reference-solutions)
[Non-root agentmanage permissions](#run-the-agent-as-a-non-root-user)

During the run

Agent sandbox
[Network allowlistinference host auto-added](#simplifying-network-restrictions)
[Web search offwhen network is restricted](#simplifying-network-restrictions)
[Reduce eval awarenessneutral, unbranded names](#minimizing-eval-awareness)
[No verifier mount/logs/verifier not exposed](#no-automatic-output-mounts)

Verifier sandbox
[Separate verifier sandboxuncontaminated environment](#separate-verifiers-by-default)
[Reward files resetdeleted before tests run](#clear-stale-reward-files)
[Low-trust code execRewardkit](#grade-untrusted-code-as-an-untrusted-user)
[Sanitized artifactssymlinks, FIFOs dropped](#sanitize-artifacts-before-the-verifier-reads-them)

After the run
[harbor viewtrajectory viewer](#browse-trajectories-with-harbor-view)
[harbor uploadshare on Hub](#share-trajectories-on-harbor-hub)
[harbor analyzeauto-flag hacks](#flag-suspicious-trials-with-harbor-analyze)
[harbor run --diffupdate results](#update-tasks--results-often)

## Before the run

### Separate verifiers by default

Tasks created with `harbor init` now use a separate verifier. In shared mode, the verifier runs in the same container as the agent. In separate mode, Harbor copies task-specified artifacts into a fresh verifier sandbox, so the agent never touches the tests or the reward output. Existing tasks retain their current behavior.

```toml theme={"system"}
# task.toml
artifacts = ["/app/output"] # copied into the verifier sandbox

[verifier]
environment_mode = "separate"
```

> [!NOTE]
>
> Separate verifiers have a limitation: agent performance must be embedded into stored artifacts, so in-memory state like running processes has to be materialized to files before the verifier can test it (see the [separate verifier conversion guide](https://github.com/harbor-framework/terminal-bench/blob/main/docs/SEPARATE_VERIFIER_CONVERSION.md)). Shared environments are still available for verifiers that need live state.

### Catch weak spots with `harbor lint`

Reward hacking opportunities often appear due to dependency drift or poorly configured tasks. `harbor lint` statically checks task configs and environment definitions for low-quality, unstable, or broken implementations.

A few example rules:

| Rule | What it catches |
| - | - |
| `agent-image-test-leak` | Agent Dockerfiles that copy in the solution or tests |
| `shared-verifier` | Tasks that grade inside the agent's own container |
| `compose-writable-bind-mount` | Host paths the agent can write through |
| `compose-privileged` | Containers running with `privileged: true` |
| `compose-additional-capabilities` | Services that add Linux capabilities with `cap_add` |
| `verifier-network-download` | Separate verifiers whose tests download code at grading time |
| `unpinned-image` | Images not pinned to a digest, which can change under you |

```bash theme={"system"}
harbor lint "<task-path>"
```

Most rules are on by default. Rules can be configured on a task or dataset level (Ruff-style):

```toml theme={"system"}
# task.toml
[metadata.harbor.lint]
extend-select = ["root-agent", "unpinned-image"]
ignore = ["compose-writable-bind-mount"]
```

### Review the whole task with `harbor check`

`harbor check` drops the agent into a sandbox containing the task source files and has the agent grade the task against a rubric. By default, an 11-point Terminal-Bench-inspired rubric is used, but task creators can override the rubric using `--rubric`.

```bash theme={"system"}
harbor check "<task-path>" --rubric "<rubric-path>"
```

### Support dev files during task development

Tasks sometimes need development files, like data-generation scripts or unit tests for the verifier. Until now, anything in `tests/` or `solution/` was uploaded into the live sandbox during the corresponding phase, which disincentivized their usage. Verifier unit tests in particular are one of the best ways to catch a weak verifier before an agent does.

We're introducing a new standard, `.harborignore`, so authors can version control dev files alongside the task while keeping them out of the sandbox and off Harbor Hub.

Each ignore file keeps files out of a different place:

| Keeps files out of… | `.gitignore` | `.dockerignore` | `.harborignore` |
| - | - | - | - |
| Version control | ✓ | | |
| Publishing to Harbor Hub | ✓ | | ✓ |
| The image build context | | ✓ | |
| Uploads to a live environment | | | ✓ |

### Ship multiple reference solutions

Oracle solutions are helpful when designing and debugging a verifier. However, a single solution can also lead to overfitting. We've provided an [example task](https://github.com/harbor-framework/harbor/tree/main/examples/tasks/hello-world-multiple-solutions) to show how to ship several solutions, to ensure the verifier isn't overfit to one of them.

```bash theme={"system"}
harbor run \
  -p examples/tasks/hello-world-multiple-solutions \
  -a oracle \
  --ae SOLUTION=2
```

### Run the agent as a non-root user

[`hello-world-non-root-user`](https://github.com/harbor-framework/harbor/tree/main/examples/tasks/reward-hacking/hello-world-non-root-user) shows a task where the agent runs as an unprivileged user, so it can't touch root-owned grading files. Harbor does not initialize new tasks with an agent user because managing user permissions varies widely across tasks and should be opted into.

```toml theme={"system"}
# task.toml
[agent]
user = "agent"
```

## During the run

### Grade untrusted code as an untrusted user

Many verifiers grade a submission by running the agent's code, and if that code runs inside the grader's process, it can tamper with the grader or write its own reward.

The Harbor team maintains an optional package `harbor-rewardkit` that simplifies verifier creation.

Rewardkit's new `Worker` runs submitted code as an unprivileged user that can't read the tests or write the reward. `Worker` also kills every process the code started before returning the output. See the [`secure-python-worker` example](https://github.com/harbor-framework/harbor/tree/main/examples/tasks/secure-python-worker) for a complete task.

### Clear stale reward files

In some cases, an agent using a shared environment could simply write a `/logs/verifier/reward.json` or `reward.txt` that isn't overwritten by the verifier. Harbor now deletes `reward.txt` and `reward.json` at the start of verification.

### Sanitize artifacts before the verifier reads them

With a separate verifier, artifacts are the only thing that crosses from the agent's sandbox to the verifier's. Harbor now:

* Drops symlinks that point outside the artifact, so the agent can't link its output to the reference solution
* Skips FIFOs, sockets and device files, which could hang the grader
* Clears setuid and setgid bits, so the agent can't plant a privileged program

### No automatic output mounts

Local environments like Docker used to bind-mount log and artifact directories to the host automatically, including `/logs/verifier` in the agent's container, so the agent could still write a reward file the verifier would read ([#3741](https://github.com/harbor-framework/harbor/issues/3741)). Those mounts are now opt-in, and logs and artifacts are collected without them.

```bash theme={"system"}
harbor run -p "<task-path>" --ek auto_mounting=true # opt back in
```

### Simplifying network restrictions

Agents sometimes cheat when given unrestricted internet access. Tasks and users can configure network restrictions, but allowlisting agent-specific endpoints (e.g. `api.openai.com`) historically required manual per-job configuration.

Agents can now declare default inference endpoints per provider. When a task is restricted, Harbor automatically allows those hosts, or the `base_url` you configured.

> [!NOTE]
>
> When the agent's network is restricted, Harbor also turns off built-in web search for agents that have it, such as Claude Code, Codex, Gemini CLI and OpenCode.

### Minimizing eval awareness

An agent that can tell it's in an eval harness may behave differently. Harbor-branded paths, environment variables, generated agent instructions and identities, and tool directories now use neutral names.

> [!NOTE]
>
> A smart model will probably be able to tell it's being evaluated either way, but it's good regardless to minimize the production-to-evaluation gap.

## After the run

### Browse trajectories with `harbor view`

`harbor view` starts a local web viewer for your jobs directory. Open any trial to step through its trajectory alongside its reward, cost and timing, and compare results across a job.

```bash theme={"system"}
harbor view "<jobs-path>"
```

### Share trajectories on Harbor Hub

Hacks are easier to catch with more eyes on them (as we've seen with the recent increase in attention on Terminal-Bench 🙂).

Users can upload job results to Harbor Hub to share with others.

```bash theme={"system"}
harbor run --upload # upload at runtime
harbor upload "<job-path>" # private by default
harbor upload "<job-path>" --share "<org>" # to share
harbor upload "<job-path>" --public # to make public
```

Jobs are private by default. Trust us, it's better than sharing zips on Slack.

### Flag suspicious trials with `harbor analyze`

Reading every trajectory doesn't scale to thousands of trials. `harbor analyze` puts an agent into a sandbox with the task's source files, the trial's logs and its trajectory, and has it classify the trial along two dimensions:

* **Reward hacking:** did the agent earn its reward by solving the problem, or by gaming the verifier?
* **Task specification:** was the instruction clear enough that a failure is the agent's fault?

Users can also specify their own rubrics.

```bash theme={"system"}
harbor analyze "<job-path>" \
  --rubric "<rubric-path>" \
  --agent codex \
  --model openai/gpt-6-luna
```

### Publish leaderboards backed by trajectories

Leaderboards should be *auditable* and *reproducible*.

You can create leaderboards on Harbor Hub, where each row can link to the trials behind it, so anyone reading the leaderboard can view the corresponding trajectories (and the exact config that produced the trial).

```bash theme={"system"}
harbor hub leaderboard --help
```

Leaderboards are displayed on the dataset's Harbor Hub page and are readable through the Hub API, so you can render them on your own site (e.g. click a row on [Terminal-Bench](https://tbench.ai)). Leaderboards can be public or private.

### Update tasks & results often

No task is perfect. When `harbor analyze` or the community surfaces a hack, the task should be fixed, and that's just as important as designing it well the first time.

Benchmarks should be [continuously developed and maintained](https://www.tbench.ai/news/continuous-benchmarks). But benchmarks exist for comparison, and changing a dataset means reconciling existing results with the new tasks, which can be costly. Harbor makes this cheap with semantic versioning: bump a task's patch version and existing trials are reused, bump the minor version to regrade them against the new verifier, and bump the major version to rerun them.

```bash theme={"system"}
harbor run \
  -d "<dataset>@<new-version>" \
  -a "<agent>" \
  --diff "<old-job-path>"
```

## Building robust environments

We believe all digital technology development will move towards an ML lifecycle, where the human role increasingly becomes eval builder and reward shaper. This new development lifecycle demands new tools. Harbor is our attempt at building these tools.

If you find a new hack vector, let us know on [Discord](https://discord.gg/QVvyhRw5UQ) or [open an issue](https://github.com/harbor-framework/harbor/issues) :)

(or post on X, that works too 😉)


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.