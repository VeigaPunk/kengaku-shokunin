# R31FxPriorArt — prior-art pricing: "the harness's verifier runs in the agent's container by default"

Scope: attack the landed entry's finding (`corpus/knowledge/benchmark-verifier-execution-model.md:35-37`, "So the default is **shared**: unless a task opts in, the verifier runs in the same container the agent worked in") as priced against statements already public and against the lane's pre-round-31 holdings S077/S078/S079/S090. Fetches: v2/README.md + GATE.md at S078's pin (cheap, per assignment), plus S077's pinned doc, S079's pinned manifest, S090's announcement, and Harbor's own pinned source/captures for support.

## Evidence (each claim carries command/path/line)

1. **S077 (lane-held, pre-round-31, public) already states the meaning of shared mode — verifier in the agent's container.**
   - Row: `corpus/SOURCES.md:99`. Doc fetched at pin: `curl https://raw.githubusercontent.com/harbor-framework/terminal-bench/e67a2cb7db4d9795c212909b3395d8c22ad60aec/docs/TASK_REVIEW_AUTOMATION.md` → `/tmp/r31fx-PriorArt/s077/TASK_REVIEW_AUTOMATION.md`.
   - Line 183: "Shared mode is leaky — the verifier inherits agent-installed packages, mutated filesystem state, and any files the agent wrote — so this check enforces isolation across the benchmark."
   - Lines 191 and 195: "shared mode's `test.sh` runs in the agent container" (twice, verbatim in both).
   - Line 175: the check "Fails if a task isn't fully configured for [separate verifier mode](https://www.harborframework.com/docs/tasks#verifier-environment-shared-vs-separate)"; condition 1 (line 177) requires `task.toml` to *declare* `[verifier] environment_mode = "separate"` — i.e. separate is opt-in, the undeclared state is shared. The default word is not printed here, but the opt-in mechanics are.

2. **The literal default rule is stated publicly by Harbor's own source (S092, public GitHub; adopted this round, not pre-round-31).**
   - `corpus/SOURCES.md:111`; captured file `.ufo/waves/round-31/assimilation/captures/config.py:588-593` (fetch: `curl .../laude-institute/harbor/6099b8cf.../src/harbor/models/task/config.py`):
     - "Whether the verifier runs in the agent's environment ('shared') or in a dedicated container ('separate'). When omitted: defaults to 'separate' if a verifier 'environment' is set, otherwise 'shared'."
   - Resolver matches: `.ufo/waves/round-31/assimilation/captures/verifier_mode.py:22-31` (`_resolve_mode` → explicit wins, else `SEPARATE` if environment set, else `None`; `resolve_task_verifier_mode` ends `or VerifierEnvironmentMode.SHARED`).

3. **S078 (lane-held, pre-round-31, public) states the *contrary* for SWE-bench Pro V2 — not the claim.**
   - Row: `corpus/SOURCES.md:100`. v2/README.md at pin 66f92766 (curl) → `/tmp/r31fx-PriorArt/s078/v2-README.md`, line 75: "**The verifier never runs in the agent's sandbox.**" Context lines 72-77 scope it to the locked protocol: agent phase offline, `git diff` captured as `model.patch`, `patch_replay:PatchReplayAgent` applies it to a pristine image and runs the unchanged verifier. GATE.md at same pin (18 lines) contains no execution-location statement.
   - So S078 does not pre-state the entry's claim; it publicly asserts the opposite for that benchmark, and the entry's reconciliation (scope S078's sentence to the locked protocol, not the mode resolution — entry `:146-148`) is the entry's own analysis, not prior art.

4. **S079 and S090 contain no execution-location statement.**
   - S079 (`corpus/SOURCES.md:101`): pinned manifest `protein-assembly/task.toml` @ 2fd12b88 (curl) has `[verifier]` with only `timeout_sec` and an empty `[verifier.env]` table; nothing about where the verifier runs.
   - S090 (`corpus/SOURCES.md:103`): tbench.ai announcement fetched (curl, `/tmp/r31fx-PriorArt/s090/announcement.html`); the 5 "verif*" hits are all dataset-quality verification ("better verified version", "LM-assisted verification"); zero hits for sandbox/isolat/separate/shared; "container" hits are generic ("Evaluating in containers is slow", "any agent that can be installed in a container").

5. **Harbor's pinned repo carries no docs page with the mode rule** — raw probes at 6099b8cf returned 404 for `docs/tasks.md`, `docs/verifier.md`, `docs/tasks/index.md` (curl -w %{http_code}); the pin's README (85 lines) has no verifier-mode text. The mode documentation lives in the code docstring (finding 2) and in the S077 maintenance doc (finding 1).

## VERDICT:

FELL (already-public): the harness-general half — "the verifier runs in the agent's container by default" — is already stated publicly: Harbor's own source docstring gives the exact default rule and the 'shared' semantics (`config.py:590-592`, public repo, quote in finding 2), and S077 (lane-held before round 31) states the shared-mode semantics, "the verifier inherits agent-installed packages, mutated filesystem state, and any files the agent wrote" with "shared mode's `test.sh` runs in the agent container" (`TASK_REVIEW_AUTOMATION.md:183,191,195`, quote in finding 1). Wave 1 conceded this itself: `plans/round-31-claims.md` §Non-claims — "the entry's finding is a reading of a published harness default".

SURVIVED (incremental): the per-benchmark application — neither Terminal-Bench 2.0 nor SWE-bench Pro V2 opts in, so both are *effectively* shared (the 731-manifest sweep is the lane's own measurement, `benchmark-verifier-execution-model.md:112-117`, not public prior art), and the reconciliation of S078's contradictory public sentence "The verifier never runs in the agent's sandbox." (`v2/README.md:75`) by scoping it to the locked protocol, plus the restore/reward-deletion mechanism reading. None of that is stated in S077/S078/S079/S090 or elsewhere public.

Flag (out of this lane): S078's public sentence vs the entry's "shared" column for SWE-bench Pro V2 sit in visible tension; the prior-art check does not resolve which reading is correct — that is a correctness matter for the C1 reviewers, not prior art.

Tools: no installs performed (curl/python3 preinstalled; nothing new recorded).
Scratch: `/tmp/r31fx-PriorArt/` (fetched docs, < 1 MB total).
