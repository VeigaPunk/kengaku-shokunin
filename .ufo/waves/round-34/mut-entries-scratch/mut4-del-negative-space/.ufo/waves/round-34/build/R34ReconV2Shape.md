# Validator policy v2 reconnaissance

## Observed

- The frozen claims specify a single v2 wave of 64 seats and identify `scripts/hyaku/ufo-wave-policy-v2.json` as the policy (claims file: `plans/round-34-claims.md:18-21`). Policy has `waveMinLanes: 64` and `waveMaxLanes: 128` (`/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy-v2.json:87-90`). The lane addendum documents validating the wave under policy and dispatching the validator's `taskCall` unchanged (`scripts/hyaku/lane-addendum.md:102-104`).
- Executable validator frontend exists at `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs`; shell check output: `CLI_EXECUTABLE=yes` and `CLI_FILE=yes`. It exposes `plan` and `run` commands, each requiring exactly one `--spec <wave.json|->` or `--spec-json <json>`; usage also lists plan-only `--emit-tasks` (`ufo-swarm-wave.mjs:1490-1492`, implementation `:1966-1997`). I did not run the validator.
- Policy lists these swarm roles (`.../ufo-wave-policy-v2.json:256-306`): scout, reviewer, labrat, critic, connector, executor, mutation-tester, revenger, simplifier, scribe. Implementation's accepted role set is scout, reviewer, critic, connector, sentinel, executor, mutation-tester, revenger, simplifier, scribe (`/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:263-276`). Thus `labrat` appearing in policy lane inventory does not make it a valid swarm role; use `sentinel` instead. `planner`, `distiller`, and `Main` are explicitly frozen-topology/non-swarm seats (`:263-264`).
- Names must match CamelCase, 2–32 chars (`ufo-swarm-wave.mjs:731-735`). Duplicate-name rejection is implemented in plan construction; don't reuse a member name (`:809-1430`; explanatory helper `:339-354`).
- `reportDir` is optional and must be relative, with no backslashes or empty, `.` or `..` path segments (`ufo-swarm-wave.mjs:397-414`). Use lane-relative form such as `.ufo/waves/round-34/build`; the lane addendum explicitly distinguishes absolute paths in context/items from relative `reportDir`, resolved under `UFO_PROJECT_ROOT` (`scripts/hyaku/lane-addendum.md:171-176`). Reports are rendered as `${reportDir}/${name}.md` (`ufo-swarm-wave.mjs:222-226`).

## Reconclusion

No standalone binary named `ufo-wave-validate` or `ufo-wave-validator` was found on PATH (checked with `command -v`; both produced no output). The available validator is the executable Node script above; this is a CLI script, not a separately named binary. Do not infer plan/run results until invoking it with the frozen policy/config via the operator's normal validation route.

## Pitfalls for L1

1. Keep all 64 member names unique and CamelCase 2–32 chars.
2. Use only the implementation's accepted role strings; notably policy's `labrat` is disallowed, and planner/distiller/Main are not swarm roles.
3. Set `reportDir` to a relative, clean path (no absolute prefix, backslash, `.`/`..` or empty segment), rooted at lane `UFO_PROJECT_ROOT`; don't put absolute paths in that field.
4. Invoke `ufo-swarm-wave.mjs plan` for validation/plan output or `run` for dispatch payload; supply exactly one spec source. This recon did not execute either command.

VERDICT: recon-v2-ready
