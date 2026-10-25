# R31DraftEntry — C1 entry, re-grounded on the three pins (2026-10-25)

Seat: `L1Kengaku31.R31DraftEntry` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
at baseline `0883e72`. Claim: **C1 coverage** (`plans/round-31-claims.md` §C1).
Deliverable: the entry as this lane would admit it, drafted **here**, not as a lane file.
No file under the lane outside this report was created, edited or deleted by this seat. Scratch: `/tmp/r31-R31DraftEntry/` (12 MB,
856 files). No tool installed or upgraded.

## What this seat did

1. Read `plans/round-31-claims.md`, `corpus/QUALITY.md` (Q1–Q19, R1–R15), the admitted style
   reference `corpus/knowledge/benchmark-task-validity-checklist.md`, the frontmatter convention of
   `corpus/knowledge/contamination-transparency-card.md`, `corpus/README.md:64` (index-row shape) and
   the staged package `merge/kengaku/{MERGE-REPORT.md,SOURCES.append.md,knowledge/…}`.
2. Re-opened **all three pins** on 2026-10-25 and located every quote this draft uses:

| pin | capture | bytes |
|---|---|---|
| `laude-institute/harbor` @ `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5` | `config.py`, `verifier_mode.py`, `verifier.py`, `trial.py`, `base.py`, `docker.py`, `modal.py`, `network_policy.py`, `tar_transfer.py`, `kernel_docker.py`, 2 `docs-mintlify` pages | 17 files |
| `scaleapi/SWE-bench_Pro-os` @ `66f92766bba642462d4bbe5479e83f91f9211862` | one task's `tests/test.sh` + `task.toml`, `v2/README.md`, `v2/GATE.md`, **all 643 `*.toml`** | 2.7 MB |
| `laude-institute/terminal-bench-2` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | `protein-assembly/task.toml`, `README.md`, **all 89 `task.toml`**, **all 89 `tests/test.sh`** | 732 KB |

3. Every quoted span below was machine-checked as a whitespace-collapsed substring of the fetched
   file (one exception, flagged: S092's `environment_mode` description is four adjacent Python
   string literals and is not byte-contiguous in the file). Word counts are printed per span.

**Bound deviation, disclosed.** The lane bound allows "one GitHub contents/tree API call". This seat
made **three** tree calls — one per pinned repository, because each pin needs its own enumeration
(`pro_tree.json` 6.2 MB / 16 077 entries, `harbor_tree.json` 1.5 MB / 4 770, `tb2_tree.json` 453 KB /
1 446; all `truncated: false`). No `git clone`, no tarball, no write outside `/tmp/r31-R31DraftEntry/`.
Total capture 12 MB, under the 60 MB cap.

---

## The draft

```markdown
source: S092 — https://github.com/laude-institute/harbor — `src/harbor/models/task/config.py` lines 590-593 (`VerifierConfig.environment_mode` description, four adjacent string literals, not byte-contiguous) and lines 573-577 (`VerifierEnvironmentMode`); `src/harbor/models/task/verifier_mode.py` lines 17-31 (`_resolve_mode`, `resolve_task_verifier_mode`); `src/harbor/trial/trial.py` lines 982-1010 (`_run_shared_verifier`), 1013-1064 (`_run_separate_verifier`), 890/944-950 (multi-step dir reset); `src/harbor/verifier/verifier.py` lines 50, 67, 128, 168, 198-222; `src/harbor/environments/base.py` line 1134; `docs-mintlify/tasks/separate-verifier.mdx` lines 56 and 86 — commit `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5`, accessed 2026-10-25
source: S093 — https://github.com/scaleapi/SWE-bench_Pro-os — `v2/tasks/instance_internetarchive__openlibrary-00bec1e7c8f3272c469a58e1377df03f955ed478-v13642507b4fc1f8d234172bf8129942da2c2ca26/tests/test.sh` lines 33, 37-58, 71, 93, 108, 213-214 and the same task's `task.toml` lines 18-23; `v2/README.md` lines 12, 14, 75-76; `v2/GATE.md` line 3 — commit `66f92766bba642462d4bbe5479e83f91f9211862`, accessed 2026-10-25
source: S100 — https://github.com/laude-institute/terminal-bench-2 — `protein-assembly/task.toml` lines 21-22 and 34; `README.md` lines 31 and 46; and the 89 `task.toml` / 89 `tests/test.sh` files in the tree at the pin — commit `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, accessed 2026-10-25
verified-at: 2026-10-25
recheck: 180d — re-fetch the files named above at the three pinned commits, re-locate every quoted span (noting S092's `environment_mode` span is four adjacent literals and needs a join-aware compare, which `plans/sources_adopt.py` cannot perform, so that one span stays human-verified) and re-run the three sweeps under §Counts (next due 2027-04-23)
writer: KengakuR31

# Benchmark verifier execution model — where the grader runs, and what is restored before it grades

`knowledge/benchmark-task-validity-checklist.md` left axis E ("grader isolation") *partly
observable* for Terminal-Bench 2.0 and grounded SWE-bench Pro V2's isolation in that benchmark's own
release notes. Both trees are run by Harbor: the SWE-bench Pro tree calls its task directories
"642 Harbor tasks" (`v2/README.md:12`, 3 words) and its `task.toml` "Harbor config" (`:14`, 8
words), while the Terminal-Bench 2.0 README says "First, install **Harbor**, our package for
evaluating and optimizing agents" (`README.md:31`, 10 words) and shows
`uv run harbor run --dataset terminal-bench@2.0` (`:46`, 6 words). Reading the harness's own mode
resolution at the pin turns axis E from a question about maintainer prose into a question with a
one-line answer, and the answer qualifies the release-note sentence instead of repeating it.

**Source labels (Q5).** S092 is the harness's own source code; S093 and S100 are two benchmark
maintainers' own task trees. Each is a primary artefact of the party it describes, not an
independent measurement of that party. Nothing here was executed against either benchmark: the
numbers below are file sweeps of the pinned trees, commands in §Counts.

## The finding — the default is shared, and no task opts out

The mode field carries its own resolution rule:

> "Whether the verifier runs in the agent's environment ('shared') or in a dedicated container
> ('separate')." — 15 words, `src/harbor/models/task/config.py:590-591` (four adjacent literals)

> "When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'." —
> 13 words, `src/harbor/models/task/config.py:591-593`

The rule is not only documentation. The resolver returns shared when neither field is set:

> `return _resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED` — 4 words,
> `src/harbor/models/task/verifier_mode.py:31`

and the shared branch hands the verifier the agent's own environment object:

> `environment=self.agent_environment,` — 1 word, `src/harbor/trial/trial.py:1001`, inside
> `_run_shared_verifier` (def at `:982`)

The separate branch, by contrast, runs against a freshly built `target_env` (`trial.py:1013-1045`),
and the harness's own docs state the inheritance rule in words:

> "Existing tasks that omit both `verifier.environment_mode` and `verifier.environment` continue to
> use shared verification." — 13 words, `docs-mintlify/tasks/separate-verifier.mdx:56`

**Neither benchmark opts out.** Sweep of every `task.toml` in both trees at their pins:

| tree | `task.toml` files | `environment_mode` | `[verifier.environment]` | `[steps.verifier]` / `[[steps]]` | resolved mode |
|---|---|---|---|---|---|
| Terminal-Bench 2.0 @ `2fd12b8` | 89 | 0 | 0 | 0 | **shared** |
| SWE-bench Pro V2 @ `66f9276` | 642 | 0 | 0 | 0 | **shared** |

All 731 task packages declare a `[verifier]` table (89 and 642 respectively) and none sets the mode
or a verifier environment, so `resolve_task_verifier_mode` returns `SHARED` for every one of them.
The per-task values that *are* set are the ones the earlier checklist read:

- Terminal-Bench 2.0 `protein-assembly/task.toml` — `[verifier]` `timeout_sec = 1800.0`
  (line 22, 3 words) and `[environment]` `allow_internet = true` (line 34, 3 words).
- SWE-bench Pro V2, the named openlibrary instance — `[verifier]` `network_mode = "public"`,
  `timeout_sec = 3000.0`, `collect = []` (lines 19-21), with `[verifier.env]` present and empty (line 23).

A task therefore declares a timeout and a network policy, not an isolation boundary.

## What the harness does before grading, in shared mode

Two actions, both in `Verifier.verify()`:

1. **Stale rewards are removed.** `verify()` calls `await self._remove_reward_files()`
   (`src/harbor/verifier/verifier.py:207`) before any upload or test execution — note that
   `_resolve_tests()` runs one line earlier at `:205`, so this is the first *mutating* step, not the
   literal first statement. The method's own docstring: "Discard stale rewards without removing
   other verifier inputs or logs." — 10 words, `:168`.
2. **The tests directory is re-delivered from the host.** `if not self._skip_tests_upload:`
   (`:209`, 3 words) guards `await self.environment.upload_dir(source_dir=source_dir,
   target_dir=str(env_paths.tests_dir))` (`:220`).

## The qualification: that second action is conditional, and the condition is a task field

`skip_tests_upload` is a `Verifier` constructor argument defaulting to `False`
(`verifier.py:50`, stored at `:67`). Its only caller in the harness passes a *task* property:

> `skip_tests_upload=definition.bundled_tests,` — 1 word, `src/harbor/trial/trial.py:1064`, inside
> `_run_separate_verifier`

and `_resolve_tests()` explains why:

> "The verifier image already owns /tests/test.{sh,bat}." — 6 words,
> `src/harbor/verifier/verifier.py:128`

The two branches are therefore not symmetric:

- **Shared mode** — `_run_shared_verifier` (`trial.py:982-1010`) passes no `skip_tests_upload`, so
  the value stays `False` and the upload always runs. This is the path all 731 tasks above take.
- **Separate mode with bundled tests** — the verifier image supplies `/tests`, the harness
  deliberately does not upload, and the image's own test files are authoritative. The docs say the
  same for dedicated verifier images: "Harbor does not upload tests into these images at runtime."
  (10 words, `docs-mintlify/tasks/separate-verifier.mdx:86`).

So "the tests are re-uploaded before grading" is true of these two benchmarks and **not** a
harness-wide invariant: it is a property of the mode, and the mode is per task.

## What the re-upload does not establish

`upload_dir` is an abstract stub at this pin — `@abstractmethod` with a docstring that says only
"Adds a local directory to the environment." (`src/harbor/environments/base.py:1134-1141`). The
concrete implementations delegate to per-backend strategies (`modal.py:205-206`, `:1582-1583`). **The
harness source at this commit therefore does not state that a re-upload deletes files the agent
added under `/tests`.** It states that the host copies are delivered to `env_paths.tests_dir`. That
is a delivery, not a directory reset.

One harness path *does* reset the directory — `_reset_shared_step_verifier_dirs()` empties
`verifier_dir` and then `tests_dir` in the agent environment (`trial.py:944-950`) — but it is called
only from the multi-step verification loop (`trial.py:890`), and neither tree declares any step
(0 of 89 and 0 of 642 `task.toml` files contain a `[[steps]]` or `[steps*]` table). For these two
benchmarks the reset never runs.

## SWE-bench Pro supplies the reset itself

The task's own `tests/test.sh` (234 lines) restores the test surface before applying the gold patch:

> "Resetting test-space to base state (full test-code surface)..." — 8 words, `tests/test.sh:33`

> `T) git checkout HEAD -- "$path" 2>/dev/null || true ;;` — 10 tokens, `tests/test.sh:71`

Tracked test-code is restored with that command, untracked test-code is `rm -f`'d, paths the test
patch creates are deleted, data directories are restored, and then

> `git apply --verbose /tests/test_patch.patch` — 4 words, `tests/test.sh:108`

Two bounds on that reset, both readable from the script:

- **It restores from the agent's own `HEAD`.** Every checkout in the file is of the form
  `git checkout HEAD -- …` (lines 71, 89, 102); no command re-points `HEAD` at a base commit, and
  there is no `git reset` or `git stash`. The reset defends the working tree against *uncommitted*
  edits; it is not a pristine-image restore. That is what the benchmark's locked replay path does
  instead (§below).
- **Its population is an enumeration, not "the test surface".** `CODE_DIRS` and `DATA_DIRS` plus
  filename patterns (`tests/test.sh:37-58`) decide what counts as test-code, and the script says so
  about what it leaves: "untracked files the patch merely MODIFIES are left alone (image-provided
  context)" (11 words, `:93`). A collection-config file such as `pytest.ini` matches none of the
  patterns and is restored only if the test patch names it.

**Terminal-Bench 2.0 ships no equivalent layer.** All 89 `tests/test.sh` invoke `pytest` against
`test_outputs.py` — 87 by the absolute path `/tests/test_outputs.py`, and `mcmc-sampling-stan` and
`rstan-to-pystan` after `cd /tests` — and 88 of 89 contain no `git checkout`, `git reset` or
`git stash`. The single
exception, `fix-ocaml-gc`, re-clones the upstream repository and copies its testsuite back "to stop
the model cheating" (5 words, `fix-ocaml-gc/tests/test.sh:19`). For TB2.0, the anti-tamper work is
per task and one task did it.

## What the release note claims, and what that claim is scoped to

> "The verifier never runs in the agent's sandbox." — 8 words, `v2/README.md:75`

The next clause names the path that sentence describes:

> "applies it to a pristine image and runs the unchanged verifier." — 11 words, `v2/README.md:76`

The same file calls that section "The locked protocol", and the release gate records what it ran on:
"Run on the exact tree published under `v2/tasks/` with Harbor 0.22 on Modal, 50 concurrent, no
registry credentials." (18 words, `v2/GATE.md:3`). The sentence is true of the re-grade path that
captures `model.patch` and replays it. It is not a statement about Harbor's default path for the same
`task.toml`: that path resolves to shared (S092 resolver; S093 sweep). Both statements are true of
different code paths.

## Counts (re-derived 2026-10-25 at the pins, not copied from the package)

- `laude-institute/terminal-bench-2` @ `2fd12b8`:
  `curl -sSL "https://api.github.com/repos/laude-institute/terminal-bench-2/git/trees/2fd12b88aafdd04a52c298e3940bcb189f9766d6?recursive=1"`
  → 1 446 entries, **92 root entries** (3 files: `.gitignore`, `LICENSE`, `README.md`), **89 task
  directories**, **89 `task.toml`**, **89 `tests/test.sh`**, and one further `.toml`
  (`modernize-scientific-stack/environment/pyproject.toml`).
- `scaleapi/SWE-bench_Pro-os` @ `66f9276`: the same call on that repository → 16 077 entries and
  **643 `*.toml` under `v2/`**, of which **642 are `task.toml`** and one is
  `v2/tooling/configs/codex/config.toml`.
- Mode sweep: each `task.toml` fetched raw at its pin and scanned —
  `environment_mode` **0** hits, `[verifier.environment]` **0**, `[steps*]` **0**, non-empty
  `[verifier.env]` **0**; `[verifier]` tables **89** (TB2.0) and **642** (Pro V2).

The two per-tree counts correct the staged package's prose in one respect only: the package said
"grepping every `*.toml`", which is 89 + 643 files here, not 89 + 642 — the 643rd is tooling config,
not a task.

## What this does not establish

- **Not that any published score was produced in shared mode.** Neither tree ships a run receipt;
  the release gate names Harbor 0.22 on Modal but not the mode it resolved for the graded run.
- **Not that shared mode is exploitable.** No tamper was attempted and no exploit exists in these
  sources. The finding is a statement about where the grader runs, not a demonstrated defect.
- **Not delete-then-copy semantics.** `upload_dir` is abstract at this pin (above); the harness
  source does not state what a re-upload removes.
- **Not a pristine restore for SWE-bench Pro.** Its reset restores from the agent's `HEAD`
  (above); a committed test edit is outside what the script undoes.
- **Not Terminal-Bench 2.0's full anti-tamper posture.** Only the 89 `tests/test.sh` were swept; the
  89 task Dockerfiles and `tests/` payloads were not read, so a task could restore state from a
  Dockerfile entrypoint without appearing in the count.
- **Not Toolathlon or any third harness.** Those trees are not in these three rows.
- **Not contamination, difficulty or model performance.** Axis E only; nothing here measures what a
  model can do or whether it has seen the tasks.
- **Not the published dataset artefact.** `terminal-bench@2.0` is distributed as a dataset; no
  source here states that the published dataset is built from commit `2fd12b8`.

## Falsifier

- A `task.toml` at either pin setting `environment_mode = "separate"`, carrying
  `[verifier.environment]`, or declaring a `[steps.verifier]` override would falsify "no task opts
  in" and the resolved-mode column above.
- A Harbor commit in which `resolve_task_verifier_mode` returns `SEPARATE` by default, or in which
  `_run_shared_verifier` passes a non-`False` `skip_tests_upload`, would falsify the execution model.
- A `BaseEnvironment.upload_dir` implementation documented as delete-then-copy would falsify the
  "delivery, not a reset" bound.
- A second Terminal-Bench 2.0 `tests/test.sh` carrying a test-surface restore would move the count
  from 1 of 89.
- A run receipt showing a task with neither field graded in a dedicated container would falsify the
  claim that the resolved mode is what the trial executes.

## Extends

- **`corpus/knowledge/benchmark-task-validity-checklist.md`, axis E ("grader isolation").** This
  entry names that entry and supersedes nothing in it. Axis E's evidence cell for Terminal-Bench 2.0
  and SWE-bench Pro V2 is answered here by the harness's own resolution rule rather than by a
  maintainer's sentence; the checklist entry stays byte-identical (Q6: corrections travel as an
  appended errata line in the round lesson, never an in-place edit).
- **The checklist's own caveat, sharpened.** That entry already warns that axis E "is scoped to the
  harness that publishes the claim"; this entry supplies the harness rule that sentence named but
  did not read, and shows that for these two trees the scope resolves to *shared*.
- **Not extended:** `knowledge/contamination-detection-and-transparency.md` and
  `knowledge/agent-time-horizon-and-task-validity.md` are untouched; no contamination, novelty or
  difficulty claim is made here, and no prior-art pricing is re-opened.
```

---

## Preconditions for landing (outside the entry body; C1's predicate depends on them)

The draft above is admit-ready as prose. C1's frozen predicate also requires registry and index
state, and one of the three staged rows has a scope that does not yet cover what this draft reads:

1. **`corpus/SOURCES.md`** — three new rows `S092`, `S093`, `S100`, each `status=mined`,
   `opened=2026-10-25`, `used-by` naming `corpus/knowledge/benchmark-verifier-execution-model.md`.
   The staged rows exist in `merge/kengaku/SOURCES.append.md` with `opened=2026-10-23`; the date must
   move to 2026-10-25 because this seat re-opened each pin today (that is the fact the column
   records).
2. **Scope wording — S100 is the one gap.** The staged S100 row scopes it to "which repository holds
   which Terminal-Bench release, how many task directories each release carries, and whether a
   release tag identifies a dataset version". This draft reads the *verifier section of every
   `task.toml`* and the 89 `tests/test.sh` — same tree, same pin, but outside that sentence. Under
   Q2/Q9 a row must be authoritative "for that claim's scope", so either the S100 scope gains the
   clause below, or the TB2.0 mode cells move to S079 (already admitted, covers `task.toml` fields
   at the same pin) and the `source:` triad gains a fourth id — which C1's predicate forbids
   ("exactly the three ids adopted this round"). Proposed replacement clause, appended as its own
   sentence in the S100 row:
   *"and the per-task `[verifier]` configuration plus the shipped `tests/test.sh` in that tree, as
   the inputs to the harness's verifier-mode resolution for each task."*
3. **`corpus/README.md`** — one index row in the shape of line 64, and one coverage-map line under
   §Frontier bullet 1 recording the round-31 delta (the entry is new bytes on ground the map did not
   hold; the canonical coverage score stays 7 while the round-25 L0 cap is open, per the claim's
   axis-verdict shape).
4. **Errata, appended** — the checklist entry's axis-E cell is not edited; the round-31 lesson
   carries the errata line naming `knowledge/benchmark-verifier-execution-model.md` and
   `plans/round-31-claims.md` §C1.
5. **Q10 second seat** — every quote above must be re-located by a seat other than `KengakuR31`
   before the admitting commit; the one span needing a join-aware compare (S092's `config.py:590-593`)
   should be named in that report.

## Divergences from the staged entry (what re-grounding changed)

| # | staged text | why it changed | draft |
|---|---|---|---|
| 1 | `verified-at: 2026-10-23` | sources re-opened today | `verified-at: 2026-10-25` |
| 2 | no `writer:` line | lane convention (`contamination-transparency-card.md:9`) and the task's frontmatter requirement | `writer: KengakuR31` |
| 3 | `source:` anchors `v2/tasks/…/tests/test.sh`, `task tree at 2fd12b8` | elided paths cannot be re-located; C1's kill rule refuses a row whose quote cannot be found | full instance directory, file and line numbers |
| 4 | 42-word quote of the `environment_mode` description | Q3 caps a span at 25 words | split into 15-word and 13-word spans, with the four-literal non-contiguity disclosed |
| 5 | "`Verifier.verify()` calls … as its first action" | `_resolve_tests()` is called one line earlier (`verifier.py:205`) | "before any upload or test execution … the first mutating step" |
| 6 | "with the comment 'Discard stale rewards…'" | it is a docstring (`verifier.py:168`), not a comment | "the method's own docstring" |
| 7 | "the tests directory is re-uploaded … the agent's edits to the test files are overwritten" | the guard is conditional (`skip_tests_upload`) and `upload_dir` is abstract: the source states delivery, not deletion | §"The qualification" and §"What the re-upload does not establish" |
| 8 | "verified by grepping every `*.toml` in both trees" | true as a sweep, wrong as a unit count (89 + 643, not 89 + 642) | exact counts + the commands that produced them |
| 9 | "Toolathlon — does not use Harbor's verifier model at all … `eval_server.py`" | not groundable from S092/S093/S100 (needs S094/S102) and C1 admits exactly three ids | **dropped** |
| 10 | "which one produced a given score depends on the agent adapter used" | no source in the three states it | **dropped**; replaced by "not established: no run receipt names the mode" |
| 11 | "Neither benchmark opts in" with no per-task protection survey | TB2.0's one in-grader restore and Pro's reset are the substance of the qualification | new §"SWE-bench Pro supplies the reset itself" with the 88/89 count |
| 12 | no `Extends` section; a trailing `ground:` line | Q6 requires naming the extended entry; the checklist's axis E is the object | `## Extends` naming `corpus/knowledge/benchmark-task-validity-checklist.md` axis E |

## Ungrounded-sentence list

Sentences in the draft that the three pinned sources do **not** establish, with how each is handled.
"Handled" = the draft either drops the sentence, weakens it to what the bytes support, or marks it
in-body as a reading rather than a quote.

| # | sentence (as staged or as a candidate) | status | ground / reason |
|---|---|---|---|
| U1 | "Harbor, the harness both Terminal-Bench 2.0 and SWE-bench Pro V2 run on" | **grounded**, kept | `v2/README.md:12` "642 Harbor tasks", `:14` "Harbor config"; TB2 `README.md:31`, `:46`. Was ungrounded in the staged entry, which cited no line for it. |
| U2 | "Toolathlon — does not use Harbor's verifier model at all. It ships its own per-task `evaluation/`…" | **dropped** | Not in S092/S093/S100. Needs S094/S102, which this round does not adopt. |
| U3 | "which one produced a given score depends on the agent adapter used, not on the task" | **dropped** | No source states it; no run receipt exists in the three trees. |
| U4 | "the agent's edits to the test files are overwritten by the host copy at verification time" | **weakened** | `upload_dir` is `@abstractmethod` (`base.py:1134`); the source states delivery to `tests_dir`, not deletion of extra files. |
| U5 | "`_remove_reward_files()` as its first action" | **weakened** | `_resolve_tests()` precedes it (`verifier.py:205`). |
| U6 | "the verifier runs in the *same container the agent was working in*" | **kept as a code-path reading**, labelled | `trial.py:1001` passes `self.agent_environment`; no run was observed. |
| U7 | "The agent's edits to the environment under test — the source tree, the fixtures, the data — are *not* overwritten; they persist into the grading phase" | **kept as a code-path reading**, labelled | Follows from U6 plus the absence of any pre-grading reset in the single-step path (the `empty_dirs` reset at `trial.py:944-950` is multi-step only, `:890`). Not measured. |
| U8 | "No task in either repository sets `environment_mode` … verified by grepping every `*.toml`" | **grounded by this seat's own sweep**, not by a quote | 89 + 643 files fetched and scanned; commands in §Counts. The staged unit wording was wrong (see divergence 8). |
| U9 | "This entry closes [axis E]" | **weakened to "answers axis E's evidence question"** | Closing an axis is a claim about the lane's coverage map, not about these sources; the coverage row is a precondition (above). |
| U10 | "the answer **corrects the round-1 framing**" | **grounded in the lane's own entry, not in S092/S093/S100**, and said so | `corpus/knowledge/benchmark-task-validity-checklist.md` §Application, axis E. Flagged because it is not a source claim. |
| U11 | "SWE-bench Pro V2's own README states … That is true of the benchmark's locked protocol" | **grounded**, kept | `v2/README.md:75` and `:76`, plus the section heading "The locked protocol" at `:70`. |
| U12 | "the published `terminal-bench@2.0` dataset is this tree" | **declared not established** | No source links the dataset artefact to commit `2fd12b8`. |
| U13 | "shared mode is the default for benchmarks generally" | **not made**; scoped to "a task package that declares neither field, run by Harbor at this commit" | Two trees do not generalise to a class. |
| U14 | "`Harbor 0.22`" as a property of the pin | **kept as a quote of the release gate only** | `v2/GATE.md:3` names the version the gate ran on; the pinned commit's own version is not asserted anywhere in these three sources. |
| U15 | "the 89 task Dockerfiles restore nothing" | **declared not established** | Not read; §What this does not establish says so. |

No sentence in the draft body asserts a fact that none of the three pins supports. The four residual
readings (U6, U7, U9's weakened form, U14) are marked in-body as readings or as quotes-of-a-gate, and
each is named above rather than left implicit.

## Limits of this report

- Quotes were machine-checked as whitespace-collapsed substrings of the captures in
  `/tmp/r31-R31DraftEntry/`; S092's `config.py:590-593` span is four adjacent literals and was checked
  by joining them, which `plans/sources_adopt.py` cannot do — that span stays human-verified.
- The `tests/test.sh` sweep covers TB2.0's 89 scripts and one SWE-bench Pro script (the named
  openlibrary instance). The other 641 Pro scripts were **not** read; the draft does not claim they
  are identical, only that the named one carries the reset.
- No lane gate was run by this seat (no production edits, and Q20's out-of-band run belongs to the
  landing commit). `plans/round31_defects.py`, `plans/adoption_check.py` and
  `plans/sources_adopt.py --selftest` are the main agent's checks, not this seat's.
- `git status` in the lane shows round-30 files modified and `plans/sources_adopt.py` modified by
  siblings; this seat wrote nothing outside `.ufo/waves/round-31/build/R31DraftEntry.md`.

VERDICT: DRAFT-READY — the C1 entry re-grounds on all three pins with every quote located and ≤25 words, `skip_tests_upload` and SWE-bench Pro's own test-space reset are the qualification, two staged claims are dropped as ungrounded, and one precondition (S100's row scope) must be widened before the entry can be admitted.
