source: S092 — Harbor harness source (verifier execution model) — https://github.com/laude-institute/harbor — `VerifierConfig.environment_mode`, `Verifier.verify`, `VerifierEnvironmentDefinition.bundled_tests` — commit 6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5
source: S093 — SWE-bench Pro V2 task verifier files (`tests/test.sh`) — https://github.com/scaleapi/SWE-bench_Pro-os — `tests/test.sh` test-space reset and reward block — commit 66f92766bba642462d4bbe5479e83f91f9211862
source: S100 — Terminal-Bench 2.0 task tree (release identity and task count) — https://github.com/laude-institute/terminal-bench-2 — repository root at commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6
verified-at: 2026-10-25
recheck: 180d — re-run the three pinned fetches (harbor 6099b8cf, SWE-bench_Pro-os 66f92766, terminal-bench-2 2fd12b88) and re-read the mode-resolution rule before citing this entry
writer: KengakuR31

# Benchmark verifier execution model — where the verifier runs, and what it restores before grading

Harbor is the harness both Terminal-Bench 2.0 and SWE-bench Pro V2 run on. This entry records what that
harness guarantees about the *grading* phase, read from its own code at a pinned commit, and what two of
its benchmarks' manifests do with the one switch that decides where grading happens. It is not a
measurement of any benchmark's scores and it is not a runtime task-validity instrument; it settles the
*execution* half of axis E ("grader integrity") that
`corpus/knowledge/benchmark-task-validity-checklist.md` left open for Terminal-Bench 2.0, and it corrects
the framing that axis was written under.

## The finding

The verifier's location is a per-task resolution with three inputs, not a harness-wide constant:

1. an explicit `environment_mode` wins (`verifier_mode.py:22-23`, "Returns the explicit mode when set");
2. otherwise a `[verifier.environment]` section implies `SEPARATE` (`verifier_mode.py:24-25`);
3. otherwise the mode is `SHARED` — `resolve_task_verifier_mode` ends
   `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED` (`verifier_mode.py:31`).

The field's own documentation states the same rule in one sentence:
"When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'."
(`config.py:590-593`, 13 words). The declared default is `None` (`config.py:588`), an *unspecified*
sentinel that only `verifier_mode.py` resolves — so "the default is shared" is a statement about the
resolver, never about the field alone. For multi-step tasks the precedence is spelled out at
`verifier_mode.py:35-38`: explicit step mode, then step environment, then the task-level resolution, then
shared.

So the default is **shared**: unless a task opts in, the verifier runs in the same container the agent
worked in. Isolation is opt-in by writing `environment_mode = "separate"` or a `[verifier.environment]`
section.

Neither benchmark opts in — on a sample, not exhaustively (see §What this does not establish):

| Task manifest | `[verifier]` keys present | `environment_mode` | effective mode |
|---|---|---|---|
| Terminal-Bench 2.0 `protein-assembly/task.toml` | `env` (empty table), `timeout_sec` | absent | **shared** |
| Terminal-Bench 2.0 `headless-terminal/task.toml` | `env` (empty table), `timeout_sec` | absent | **shared** |
| SWE-bench Pro V2 `instance_internetarchive__openlibrary-00bec1e7…/task.toml` | `collect`, `env`, `network_mode`, `timeout_sec` | absent | **shared** |

## What the harness guarantees anyway

Two protections hold regardless of mode, and they are narrower than "isolated":

- **Stale reward files are deleted before the test command runs.** `Verifier.verify()` awaits
  `self._remove_reward_files()` (`verifier.py:207`) as its first environment-mutating statement — not
  literally its first statement, which is path resolution. The method's docstring is the guarantee:
  "Discard stale rewards without removing other verifier inputs or logs." (`verifier.py:168`, 10 words).
  A missing or empty reward is an error, not a zero.
- **The tests directory is re-uploaded from the host** — `upload_dir(source_dir=…, target_dir=str(env_paths.tests_dir))`
  (`verifier.py:220-223`), i.e. into `/tests` — **unless the task's verifier image already owns it.** The
  guard is `if not self._skip_tests_upload:` (`verifier.py:209`); the flag is wired from
  `skip_tests_upload=definition.bundled_tests` (`trial.py:1064`) and set `True` when the resolved verifier
  environment names a `docker_image` or its tests directory holds a `Dockerfile`/`docker-compose.yaml`
  (`verifier_mode.py:110-119`), `False` only on the `environment_dir` fallback (`:122-133`). In shared mode
  no verifier environment is resolved at all, so the flag keeps its `False` default and the upload happens.
  The conditional matters as a harness fact even where it is inert for these two benchmarks: the comment at
  `verifier.py:128` is "The verifier image already owns /tests/test.{sh,bat}."

What the agent's edits to the *environment under test* get is nothing: the source tree and data persist
into grading. Only the test-code surface is restored, and for SWE-bench Pro V2 that restore is the task's
own script, not the harness upload: `test.sh` prints "Resetting test-space to base state (full test-code
surface)..." (`test.sh:33`) and restores each tracked test-code path with `T) git checkout HEAD -- "$path"`
(`test.sh:71`), deleting patch-created untracked files and leaving untracked fixtures alone. So for that
benchmark the test files are reset by **two independent mechanisms** — the harness upload and the task's git
restore — while the environment under test is reset by neither.

The task's own reset has a hole, and it is written in the classifier that builds the list: a path whose
parent directory is in `DATA_DIRS = {'testdata', 'test_data', 'fixtures', 'fixture', 'mocks', 'mock',
'__snapshots__'}` (`test.sh:38`) returns `False` from `is_test_code` (`:43-44`) and is therefore absent from
both the tracked list (`:60`) and the untracked list (`:63`) the reset walks. A fixture or snapshot an agent
edits — or adds — is neither restored from `HEAD` nor deleted, and reaches grading. The reset is scoped to
test *code*, and the declaration that says so is the one place the scope can be checked.

Terminal-Bench 2.0 ships no equivalent script: of its 89 `tests/test.sh` files at the pinned commit, 88
contain no reset block (wave seat `R31DraftEntry`, report `.ufo/waves/round-31/build/R31DraftEntry.md`), so
for that benchmark the harness upload is the only protection of the test surface.

## What the grader is, and what it reads

SWE-bench Pro V2's reward is set containment over two declared test sets:
`all_required = fail_to_pass | pass_to_pass` then `success = all_required <= passed_tests`
(`test.sh:213-214`), with `fail_to_pass`/`pass_to_pass` read from `/tests/config.json` and coerced through
`set()` before the union.

The *passed* side is not a test-runner verdict but a log scan: `parser.py` applies
`^([^\s]+\.py::[^\s]+)\s+(PASSED|FAILED|SKIPPED|ERROR)` with `re.match` on each `line.strip()`
(`parser.py:68,71`) to **stdout and stderr** (`:88-90`), keeps only `PASSED`, and dedupes by test name with
`unique_results = {result.name: result for result in results}.values()` (`:121`) — i.e. **last write wins**.
So the set the reward is contained in is derived from agent-writable log text, and a line beginning
`<test id> PASSED` printed by a *failing* test's own captured output is read as a passing record. Round 31
executed that path on this parser and the grader's own shell logic (wave seat `R31SrcS093b`, committed at
`.ufo/waves/round-31/build/R31SrcS093b.md`): with all twenty required tests reported `FAILED`, the captured
output minted twenty `PASSED` records and the reward came out `PASSED`, exit 0.

A grader of that shape cannot see a test the task never named, cannot tell a runner's verdict from a log
line, and cannot see whether the agent edited the environment under test on the way to a green run — which
is why the reward-deletion and test-restore facts above are load-bearing for how much the number is worth,
and why "the verifier is isolated" is not among them.

## What this does not establish

- **No run was observed.** Every claim here is read from code and manifests at pinned commits; no harness
  was executed, no trial log was read, and the mode-resolution rule is therefore a *documented and coded*
  rule, not an observed behaviour.
- **The "neither benchmark opts in" sweep is a seat's, not mine.** I read six `task.toml` manifests myself
  (three of Terminal-Bench 2.0's 89, three of SWE-bench Pro V2's 642). A wave seat then fetched and parsed
  all 731 (`R31DraftEntry`, committed at `.ufo/waves/round-31/build/R31DraftEntry.md`) and found
  `environment_mode`, `[verifier.environment]` and any `[steps.verifier]` section in **none** of them; the
  six-manifest sample and the 731-manifest sweep agree. The sweep is re-runnable and its scope is stated;
  what it cannot do is read a task added after the pin.
- **A directory count is not a validity count.** The pinned Terminal-Bench 2.0 root holds 92 top-level
  entries: 89 directories and 3 files (`.gitignore`, `LICENSE`, `README.md`). Nothing here says the 89
  directories are valid, graded or uncontaminated tasks.
- **`bundled_tests` is inert for these two benchmarks and not inert in general.** No claim is made about a
  benchmark whose verifier image owns `/tests`; for such a task the upload guarantee does not apply.
- **This is not runtime task validity.** It does not audit whether a task is well-posed, whether its tests
  are the right tests, or whether its reward is meaningful. It records where grading happens and what is
  restored first.
- **The manifests are read at one pin.** A later release can set `environment_mode` without touching this
  entry; the `recheck` line names the three fetches to re-run.

## Falsifier

A task in either pinned tree that sets `environment_mode = "separate"` or a `[verifier.environment]`
section (falsifies the "shared" column for that task), or a trial log showing a shared-mode run whose
`/tests` was not re-uploaded and whose task carries no verifier image (falsifies the upload guarantee), or
a `verify()` path that grades without deleting the previous reward (falsifies the first guarantee), or a
SWE-bench Pro V2 trial whose reward file contradicts `parser.py`'s log scan — e.g. a required test that
failed and was still counted as passed (falsifies the log-scan reading, and would mean some other path
writes the reward).

## Extends

- `corpus/knowledge/benchmark-task-validity-checklist.md` — its axis E ("grader isolation") states the
  rule this entry now has evidence for: "Axis E is scoped to the harness that publishes the claim … a
  harness that runs the verifier in a shared environment by default does not inherit that property"
  (`:71-74`). The checklist states that rule and, for Terminal-Bench 2.0, lists axes A, B, C, D, F, G with
  **E absent** (`:94-95`); this entry supplies the harness default and TB2's E cell, and it corrects the
  checklist's own framing where S078's "The verifier never runs in the agent's sandbox." (`:38`) is a
  property of SWE-bench Pro's locked release, not of the harness. It does not revise the checklist's
  SWE-bench Pro row (`:96`), which already credits E to S078.
- `corpus/README.md` coverage map — the round-29 row *Benchmark task-validity instruments* carries the
  bound "Not deployment config, not runtime task validity, not contamination measurement"; the frontier
  bullet above it carries "their scoring code was not read and stays open". This entry discharges the
  scoring-code clause for verifier execution only, and does not claim runtime task validity.
- `corpus/knowledge/contamination-transparency-card.md` — the card's "grader evidence" row; a card that
  records "grader: harness verifier" inherits the mode and restore facts above.

## How kengaku applies it

| Situation | Do | Don't |
|---|---|---|
| Comparing two benchmark scores | Ask which harness and which verifier mode produced them, and whether the test surface was host-restored or task-restored | Assume a green score means the agent never touched the tests |
| Reading a task's `task.toml` | Read `[verifier]` for `environment_mode`/`[verifier.environment]`; absence means **shared** | Read the harness docs' "isolated verifier" phrasing as a default |
| Writing a task-validity review | Record the restore mechanism (host upload vs task script) beside the reward rule | Record only "the grader passes/fails" |
| Citing a harness guarantee | Quote the `verify()` statement that implements it, with its line | Quote a docstring's aspiration as behaviour |
