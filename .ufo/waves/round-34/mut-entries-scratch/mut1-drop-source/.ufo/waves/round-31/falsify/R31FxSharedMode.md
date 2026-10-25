# R31FxSharedMode — falsification of "the verifier runs in the agent's container by default" (C1 S092, Harbor @ 6099b8cf)

Leaf attack on the landed entry `corpus/knowledge/benchmark-verifier-execution-model.md` (claim sentence:
"So the default is **shared**: unless a task opts in, the verifier runs in the same container the agent
worked in.", lines 35-37) and the README coverage-row phrasing "shared by default" (`corpus/README.md:66`).

Method: fetched the pinned-commit sources from GitHub raw at commit `6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5`
(repo `harbor-framework/harbor`, URL cited as `laude-institute/harbor` in S092; `read` shows GitHub 301-redirects
laude-institute → harbor-framework; raw URLs below use the canonical owner):

- `https://raw.githubusercontent.com/harbor-framework/harbor/6099b8cf.../src/harbor/trial/trial.py` (2100 lines)
- `.../src/harbor/trial/single_step.py` (110)
- `.../src/harbor/trial/multi_step.py` (425)
- `.../src/harbor/trial/regrade.py`
- `.../src/harbor/verifier/factory.py`, `.../verifier/base.py`, `.../verifier/verifier.py`
- `.../src/harbor/models/task/verifier_mode.py`, `.../models/task/config.py`

Pin identity: `sha256sum` of fetched `verifier.py` = `fc5d9fc6...` and of `models/task/config.py` =
`ac9f5d19...`, of `models/task/verifier_mode.py` = `e5893be9...` — all three equal the wave's captured
`SHA256SUMS.txt` (`.ufo/waves/round-31/assimilation/captures/`). Fetched bytes = pinned-commit bytes.

## 1. The exact lines that make the shared path share the agent's environment

Mode resolution (default):
- `models/task/verifier_mode.py:22-23` — `if verifier.environment_mode is not None: return verifier.environment_mode`
- `models/task/verifier_mode.py:24-25` — `if verifier.environment is not None: return VerifierEnvironmentMode.SEPARATE`
- `models/task/verifier_mode.py:29-31` — `resolve_task_verifier_mode` returns
  `_resolve_mode(task_cfg.verifier) or VerifierEnvironmentMode.SHARED` (fallback = SHARED).
- `models/task/verifier_mode.py:42-45` — step precedence: explicit step mode → step env → task-level → shared.
- Field default is literally `None` (`models/task/config.py:587-588`); the docstring says "When omitted: defaults
  to 'separate' if a verifier 'environment' is set, otherwise 'shared'." (`config.py:590-593`, exact bytes verified
  against the S092 quoted span).

The sharing line itself:
- `trial/trial.py:997` — inside `_run_shared_verifier` (def at `:982`):
  `environment=self.agent_environment` passed to `VerifierFactory.create_verifier_from_config` (`:993-1002`).
  This is the only environment object given to the shared verifier; `override_env`/`verifier_env` are env-var
  dicts, not environments.
- factory `verifier/factory.py:66-78,88-99` forwards `environment` unchanged (both import-path and default
  `Verifier` branches); `verifier/base.py:33` stores it; `Verifier.verify` acts on it
  (`verifier/verifier.py:181` `self.environment.exec`, `:220` `self.environment.upload_dir`).

Same object as the agent:
- Agent run uses the same attribute: `trial/trial.py:772` `environment=self.agent_environment`; setup at
  `:1886,1904`; env started once from `self.config.environment`/task env at `_init_agent_environment`
  (`:1453-1486`) and started at `_start_agent_environment` (`:1853-1860`). No re-creation between phases.
- In shared mode the container is not stopped before verification: single_step stops the agent env only when
  SEPARATE (`single_step.py:48-49`) and stops it *after* verification when SHARED (`:53-54`);
  `stop_main_before_sidecars=(mode == SEPARATE)` (`single_step.py:44-46`) means the main service keeps running
  through the shared verify. Multi-step stops only for SEPARATE on the last step (`multi_step.py:134-135`).
  The shared verifier runs on the live, still-running agent container.

Dispatch (everything non-SEPARATE → shared):
- `trial/trial.py:879-901` — `_run_step_verifier`: `if mode == SEPARATE: _run_separate_verifier(...) else:
  _reset_shared_step_verifier_dirs(); ... _run_shared_verifier(...)`
- `trial/single_step.py:94-108` — `_run_verifier`: SEPARATE → `_run_separate_verifier`, else →
  `_run_shared_verifier`
- `trial/multi_step.py:124-142` — `mode = resolve_step_verifier_mode(...)` then `_run_step_verifier(..., mode=mode)`
- Consistent with this, the multi-step reset flag is described in-code as "A shared verifier runs in the agent
  environment" (`multi_step.py:45-49`), and the dir wipe before each shared verify is executed *on* the agent env
  (`trial.py:890,944-951`; next-step sanitize at `multi_step.py:159-165`).

## 2. Branches where a shared-mode verifier still gets its own environment

None found in the trial flow. The only verifier-environment construction is `_run_separate_verifier`
(`trial.py:1013-1081`), which builds its own env (`_separate_verifier_env`, `:1083+`) — but that branch is
reachable only when mode resolution returned **SEPARATE** (i.e., the task opted out); it is not a shared-mode
execution. The other paths that bypass shared verification are mode-exclusive, not shared-with-own-env:

- `Trial._run_step_verifier` returns early if `self.config.verifier.disable` (`trial.py:870-871`); single_step
  likewise (`single_step.py:89-90`) — no verifier runs.
- `Trial.run` skips `_run()` entirely under `install_only` (`trial.py:607-609`) — no verification runs.
- Regrade is a separate product path and does the opposite of sharing: `RegradeTrial._run` calls only
  `_run_separate_verifier` (`trial/regrade.py:704-713`), `MultiStepRegradeTrial` passes
  `mode=VerifierEnvironmentMode.SEPARATE` explicitly (`regrade.py:827-831`), and the regrade gate *refuses*
  shared-mode tasks ("Task at ... resolves to a shared-mode verifier, which needs a live agent environment;
  regrade re-runs verification against recorded artifacts only", `regrade.py:115-120`; step variant at
  `:105-112`).

So within the pinned trial code there is no shared-mode verifier that receives an environment other than
`self.agent_environment`.

## 3. Precision of the entry's sentence

The sentence survives code-level falsification, with two precise qualifications the entry already mostly states:

1. "By default" is a resolver-level fallback, not a field default — the entry says this exactly
   (`benchmark-verifier-execution-model.md:29-33`). Confirmed: `VerifierConfig.environment_mode` default is
   `None` (`config.py:587-588`); SHARED enters only via `verifier_mode.py:31` / `:45`.
2. "Unless a task opts in" is per-**verify-pass**, not per task: a multi-step task may mix modes across steps
   (`resolve_step_verifier_mode` precedence, `verifier_mode.py:34-45`; multi-step dispatch `multi_step.py:124`
   resolves per step), so a single task can have both shared and separate verifier runs. The phrase "unless a
   task opts in" reads as a per-task toggle; the code's unit of opting in is the step.
3. "The same container the agent worked in" is precise for the default local Docker backend (same
   `BaseEnvironment` instance, main service not stopped, env stopped only after verification). For
   provider-backed environments (`--env ...`) the code guarantee is the same environment *object*, not an
   independently verified same-physical-container guarantee; the entry's own "no run was observed" caveat
   (`:109-111`) covers this.

No imprecision found that would flip the claim: the shared verifier demonstrably receives the agent's
environment object and no branch hands a shared-mode verifier an environment of its own.

## 4. What was checked and commands

- Fetch: `curl -sSL -o <f> "https://raw.githubusercontent.com/harbor-framework/harbor/6099b8cf2bfbbb3e7ff1eb2163bfc4524dbd9ba5/src/harbor/<path>"` (HTTP 200 each).
- Pin identity: `sha256sum verifier.py models_models_task_config.py models_models_task_verifier_mode.py` vs `.ufo/waves/round-31/assimilation/captures/SHA256SUMS.txt` (three matches).
- Line scans: `grep -n "_run_shared_verifier|agent_environment" trial.py`; `grep -n "resolve_task_verifier_mode|resolve_step_verifier_mode" single_step.py multi_step.py`; `grep -n "create_verifier_from_config" trial.py`; `grep -n "VerifierEnvironmentMode.SHARED" *.py`; `grep -n "environment=" trial.py single_step.py multi_step.py`.
- Reads: `trial.py:855-952` (dispatch), `trial.py:960-1030` (shared/separate runners), `single_step.py:1-110`, `multi_step.py:100-175`, `models_models_task_verifier_mode.py:15-46`, `models_models_task_config.py:573-629`, `factory.py:45-99`, `verifier.py:119-238` (captured), `trial_regrade.py:100-122,700-713,824-834`.

Tooling: no tools installed or upgraded (curl and python3 builtins only); pacman untouched.

## VERDICT

SURVIVED: "the verifier runs in the agent's container by default" — shared path shares `self.agent_environment`
(`trial.py:997`) by resolver fallback (`verifier_mode.py:31`), same object the agent runs on (`trial.py:772`),
no branch gives a shared-mode verifier its own environment. FELL (precision only): "unless a task opts in" is
per-step, not per-task, for multi-step tasks; "same container" is object-level for provider backends; regrade
runs are a separate path that refuses shared tasks outright.
