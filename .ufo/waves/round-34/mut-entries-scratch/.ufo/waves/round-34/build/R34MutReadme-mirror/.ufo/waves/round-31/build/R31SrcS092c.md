# R31SrcS092c — `skip_tests_upload` in Harbor at 6099b8cf

Seat: leaf scout (C1, S092 re-grounding). Access date **2026-10-25**.
Pinned revision for every Harbor byte below: `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5`
(`https://raw.githubusercontent.com/laude-institute/harbor/<commit>/<path>`).

## Capture inventory (bytes actually fetched, `/tmp/r31-R31SrcS092c/`)

| file (local name) | remote path | bytes | sha256 |
|---|---|---|---|
| `src_harbor_verifier_verifier.py` | `src/harbor/verifier/verifier.py` | 11910 | `fc5d9fc6d27ac6eca57a3504f6853e094b0c50f4d965708e72d9c237ad30da34` |
| `src_harbor_trial_trial.py` | `src/harbor/trial/trial.py` | 83558 | `d6ab11b45f5d90d5cb898c5eaf1fb5aec113860c041f35034109ad464939ca96` |
| `src_harbor_models_task_verifier_mode.py` | `src/harbor/models/task/verifier_mode.py` | 5142 | `e5893be9cf98b8ea133abe5d2456d80ab995ebac12627d798bfab41b4b8a6f2d` |
| `src_harbor_verifier_factory.py` | `src/harbor/verifier/factory.py` | 3310 | `b4b470efe8ce84c0774b836a8992a09c2abf105ed5d35abf3640a317ab6ccac3` |

Total capture 108 KB. The last two files were fetched only to trace the flag's definition and
its threading to the constructor (the assigned question names an object attribute; naming it
without its origin would be a guess). No repository clone; no file outside `/tmp/r31-R31SrcS092c/`
was written. Tool installs/upgrades: **none** (no package needed; `curl`, `awk`, `sha256sum` sufficed).

## Answer — the exact condition

`Verifier.verify()` skips the tests-directory re-upload **iff `self._skip_tests_upload` is truthy**,
and at the only production construction site that attribute is assigned from
**`definition.bundled_tests`** — the `VerifierEnvironmentDefinition` field that is `True` when the
resolved *separate* verifier environment brings its own image or its own build recipe for the tests
directory.

### 1. The guard itself — `src/harbor/verifier/verifier.py:209`

```
209	        if not self._skip_tests_upload:
210	            self.task.file_filter.require_included(host_test_path)
```
The whole upload block (`:209`–`:227`) is inside that `if`. The upload call the staged entry quotes is
at `:220-223`:
```
220	                        await self.environment.upload_dir(
221	                            source_dir=source_dir,
222	                            target_dir=str(env_paths.tests_dir),
223	                        )
```

### 2. Constructor wiring — `src/harbor/verifier/verifier.py:50` and `:67`

```
50	        skip_tests_upload: bool = False,
```
```
67	        self._skip_tests_upload = skip_tests_upload
```
Note `:56-66`: the `super().__init__(...)` call does **not** forward the flag — it is `Verifier`-local
state, not a `BaseVerifier` contract.

The production caller, `src/harbor/trial/trial.py:1064` (inside `_run_separate_verifier`, `:1013`):

```
1064	                    skip_tests_upload=definition.bundled_tests,
```
`definition` is bound at `:1024-1026`:
```
1024	        definition = resolve_verifier_environment_definition(
1025	            self.task.config, self.task.paths, step_cfg
1026	        )
```
and forwarded unmodified by `src/harbor/verifier/factory.py:57` → `:96`:
```
57	        skip_tests_upload: bool = False,
```
```
96	            skip_tests_upload=skip_tests_upload,
```

### 3. The `_resolve_tests()` branch comment — `src/harbor/verifier/verifier.py:126-133`

```
126	    def _resolve_tests(self) -> tuple[list[Path], Path, Path]:
127	        if self._skip_tests_upload:
128	            # The verifier image already owns /tests/test.{sh,bat}.
129	            return (
130	                [],
131	                self.task.paths.tests_dir,
132	                self.task.paths.test_path_for(self.environment.os),
133	            )
```
Three consequences of that branch, all visible in the same bytes:
- source-dir list is empty (`:130`), so even if the guard at `:209` were removed nothing would upload;
- it returns `test_path_for(os)` **without** calling `discovered_test_path_for`, i.e. it bypasses the
  `FileNotFoundError("No test script found in: …")` that the non-skip path raises at `:137-143`;
- the executed script path is still composed from `env_paths.tests_dir` at `:245-248`:
  ```
  245	        test_script_path = str(
  246	            env_paths.tests_dir
  247	            / host_test_path.relative_to(tests_source_dir).as_posix()
  248	        )
  ```
  so in skip mode the harness runs the image's `/tests/<name>` and never the host copy.

### 4. The object attribute and its origin

Attribute: **`Verifier._skip_tests_upload`** (`verifier.py:67`).
Value at the only production site: **`definition.bundled_tests`**, a field of the frozen dataclass
`VerifierEnvironmentDefinition` (`src/harbor/models/task/verifier_mode.py:82-86`):
```
82	@dataclass(frozen=True)
83	class VerifierEnvironmentDefinition:
84	    config: EnvironmentConfig
85	    directory: Path
86	    bundled_tests: bool
```
`bundled_tests` is **computed, not declared** — no task config field sets it. It is `True` in the two
image-owning branches of `resolve_verifier_environment_definition` and `False` only in the fallback:

- `verifier_mode.py:107-111` — a step or task verifier environment with `docker_image` set → `True`:
  ```
  107	            return VerifierEnvironmentDefinition(
  108	                config.model_copy(update={"docker_image": environment.docker_image}),
  109	                directory,
  110	                True,
  111	            )
  ```
- `verifier_mode.py:112-119` — `Dockerfile` or `docker-compose.yaml` present in that candidate tests
  directory → `True` (`:112-115` is the test, `:118` the third field).
- `verifier_mode.py:122-133` — fallback to `paths.environment_dir` → `False` (third field at `:132`).

So the operative condition in words: **the tests directory is not re-uploaded when the task (or step)
resolves to a *separate* verifier environment whose definition ships its own Docker image, or whose
candidate tests directory carries a `Dockerfile` / `docker-compose.yaml`** — i.e. the tests are baked
into the verifier image. `bundled_tests` is only reachable at all in separate mode: `_resolve` returns
`None` for shared mode (`verifier_mode.py:93-95`) and `trial.py:1028-1032` raises
`RuntimeError("Separate verifier mode did not resolve an environment config")` on `None`.

### 5. The shared path never sets the flag

Mode dispatch, `trial.py:879-895`:
```
879	            if mode == VerifierEnvironmentMode.SEPARATE:
880	                step_result.verifier_result = await self._run_separate_verifier(
```
```
895	                step_result.verifier_result = await self._run_shared_verifier(
```
and `_run_shared_verifier` (`:982`) constructs the verifier at `:993-1002` **without**
`skip_tests_upload`, so the `:50` default `False` applies and the upload always runs in shared mode:
```
993	            verifier = VerifierFactory.create_verifier_from_config(
994	                self.config.verifier,
995	                task=self.task,
996	                trial_paths=self.paths,
997	                environment=self.agent_environment,
...
1002	            )
```

Secondary suppression even when the guard is open (`verifier.py:216-218`):
```
216	                for selection in selections:
217	                    if not selection.relative_paths:
218	                        continue
```
A file filter that leaves a selection empty skips that source dir — the upload is per-selection, so
"the tests directory is re-uploaded" can also be vacuously true for one of two dirs.

## Verdict on the staged entry's wording

Staged entry: `/home/vgpnk/Projects/shokuknow/merge/kengaku/knowledge/corpus/knowledge/benchmark-verifier-execution-model.md`
(5150 bytes, sha256 `643094482733795f8b656ff9b32a3dd95ae32603c36b0162cf0f5c50ee1c0517`, read-only).

- `:45-47` states it flatly:
  ```
  45	2. **The tests directory is re-uploaded from the host into the environment.** `verify()`
  46	   resolves `test_source_dirs`, then for each selection calls
  47	   `await self.environment.upload_dir(source_dir=source_dir, target_dir=str(env_paths.tests_dir))`.
  ```
- `:65-66` escalates it to a framework-level guarantee:
  ```
  65	- **Terminal-Bench 2.0** — axis E is **shared by default**. The unconditional
  66	  protections are the stale-reward deletion and the tests-directory re-upload. The
  ```
- `:49-50` draws the inference:
  ```
  49	So the agent's edits to the **test files** are overwritten by the host copy at
  50	verification time, even in shared mode. The agent's edits to the **environment under
  ```

Classification, on the assigned three-way choice:

- **"unconditional" — FALSE as a framework statement.** `verify()` has an explicit opt-out
  (`verifier.py:209`) that a task can reach through ordinary config (a verifier `docker_image`, or a
  `Dockerfile` in the tests dir), and in that configuration the host copy is never uploaded.
- **"conditional" — TRUE.** Exact condition: `self._skip_tests_upload` truthy, i.e.
  `definition.bundled_tests` true, i.e. separate-mode verifier whose definition owns its image or whose
  tests directory contains `Dockerfile`/`docker-compose.yaml`.
- **"false as written" — TRUE of the entry's *unconditional* phrasing** (`:45` bare, `:66` literally
  "unconditional"), and of `:49` insofar as it presents the overwrite as holding in every mode.
  It is **not** false for the two benchmarks the entry audits: neither sets `environment_mode` nor a
  `[verifier.environment]` section, so both resolve shared (`verifier_mode.py:29-31` → `SHARED`;
  `:93-95` → `None`; `trial.py:895` → `_run_shared_verifier` → `:993-1002` omits the flag → default
  `False` at `verifier.py:50`), and the upload does run there. The entry is right by accident of its
  subjects' config, wrong as a statement about the harness.

Placement matters for admission: the missing qualification is **inside the span the entry cites** —
`source:` at `:2` claims `# Verifier.verify` for S092, and the guard sits in `verify()` at
`verifier.py:209`, three lines below the `_resolve_tests()` call the entry does quote. This is not an
out-of-scope gap; it is an omission from quoted material.

Minimum repair shape (one clause, no restructuring): in `:45` add "when the verifier is not built with
its own tests (`skip_tests_upload` / `VerifierEnvironmentDefinition.bundled_tests`)", and in `:66`
replace "unconditional protections" with a per-benchmark statement ("holds for both tasks audited here
because both resolve shared mode"), since `bundled_tests` is unreachable in shared mode at all.

## Adjacent finding outside this seat's question (for C1's frozen predicate)

`benchmark-verifier-execution-model.md:5` reads `verified-at: 2026-10-23` (and `:6` `(ran 2026-10-23)`),
while C1's frozen predicate requires "a `verified-at: 2026-10-25` line". The staged bytes therefore fail
that clause as shipped. Reported, not repaired (no production edits in this seat).

## Unknowns / not observed

- Constructors of `Verifier` outside `src/harbor/trial/trial.py` were not enumerated: only two raw files
  were fetched, and GitHub code search needs auth. Within `trial.py` there is exactly one site passing
  the flag (`:1064`) and one that omits it (`:993`); a test or CLI caller passing `True` directly would
  widen the condition but cannot narrow it.
- The file-filter/`selected_directory` machinery (`verifier.py:212-223`) was not read past the guard;
  its interaction is reported only as the `:217-218` empty-selection skip.
- Whether any TB2.0 / SWE-bench Pro V2 task declares a verifier `docker_image` was not re-checked here
  (that is the S093/S100 seats' ground, and the entry asserts "No task … sets `environment_mode` or a
  `[verifier.environment]` section").

VERDICT: CONDITIONAL — `verify()` re-uploads the tests directory only when `Verifier._skip_tests_upload` (set from `definition.bundled_tests` at `trial.py:1064`) is false, and it is true whenever the separate-mode verifier definition supplies its own `docker_image` or its tests dir contains a `Dockerfile`/`docker-compose.yaml`, so the staged entry's "unconditional" wording at `benchmark-verifier-execution-model.md:45,66` is FALSE as a harness-level claim while accidentally true for the two shared-mode benchmarks it audits.
