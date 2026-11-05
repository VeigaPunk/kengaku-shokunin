# SentinelForge — scoped findings, round 92 (forgery battery)

Measured at B2 `f0018773f507f363854123856990f8ff8a87eb8c` in scratch clones only. Full recipes, verbatim outputs and FORGE lines: `.ufo/waves/round-92/w1/SentinelForge/report.md`.

## Passing forgeries (each is a finding)

**H1 — High — gate: closed-row vacuity bypass (M10 not met).** Recipes (fixture ledger, `evaluate()` at B2):
- Override row `{"status":"closed","supersedes":"OLD-1","check":"true","override_reason":"inspection","close":"closed by inspection"}` over a base row whose check is `grep -q anchor notes.md` → `freeze=admitted`, `PREDICATE R92-C3 pass`. Override branch never runs `vacuous_check`; anchoring runs only `if ovr_tokens`.
- Closed row `check:"true # grep"` → pass (FILE_OP word inside a comment).
- Closed row `check:"true 1.0"` → pass (PATH_TOKEN matches the decimal).
- Closed row `check:null` → pass (`if not command: continue`).
Expected: `closed-check-vacuous` DEFECT for each. Observed: none.

**H2 — High — gate: frozen C3 default command never returns (M8 recursion).** `python3 plans/round92_burndown.py --lane . --rev T --work DIR --freeze-round 92` does not produce a verdict: timeout rc=124 at 120 s with 950 nested `predicate-selftest` dirs still growing; a child reached nesting depth 103. Cause: the child-mode proof requires `--selftest` in the parent's argv; the default argv lacks it, so each child re-runs the whole battery. `--selftest` alone completes (10/10, rc 0). C3 cannot pass its frozen predicate at any rev.

**H3 — High — gate: M8 battery skippable by marker spoof.** With one selftest expectation flipped red, `--selftest` returns rc 1. The same copy run through a `python -c` wrapper that writes `.predicate-selftest-child` (its pid and sha256 of its own argv, whose text contains `round92_burndown.py --selftest`) returns `PREDICATE R92-C3-BATTERY pass`, rc 0, with no SELFTEST lines printed.

**H4 — High — conformance counter (`round92_c2_conformance.py`) unpinned.** The literal M7 rc-2 acceptance does not pass at BASE (`PREDICATE R92-C2 fail`, rc 1; base leg rc 1 and the M7 check also needs a `PREDICATE R91-C1 pass` string). But replacing `passed = all(...)` with `passed = True` prints `PREDICATE R92-C2 pass`, rc 0, at BASE with M7/M12/M9 each printing FAIL. No `round92_*` file is in `plans/counter-pins-r91.json` at B2.

**H5 — High (known class, new reach) — C1 passes a probe that never runs the grader.** Probe with `observed = predicted`, a receipt produced by that probe, ledger flipped to executed 36, and the tool pin rewritten, all in one commit → `TARGET executed_rows=36 ... mismatches=0 defects=0`, `PREDICATE R92-C1 pass`, rc 0. The counter's L6 reruns the same bytes, so it is not an oracle. This extends the disclosed in-tree pin residual (L0 kengaku round-91); it is not closed by this round.

**H6 — High by rule (design-level) — gate: lane-id trust root is `SHOKUNIN_ROOT`.** Blocked row owner `nobody` is refused with the fixture conf and admitted when `SHOKUNIN_ROOT` points at a conf that lists `nobody`.

**Known residual, not new — FORGE 5b.** Tampered `round91_counter_pin.py` with its pin rewritten in the same commit → `PINS checked=17 matched=17`, `SELFTEST cases=9 red-green-ok=9`, `PREDICATE R91-C2 pass`, rc 0. Without the pin rewrite it is red (`PIN-MISMATCH bytes`, rc 1).

## Forgeries that were red as required

- Fabricated receipt, invented vectors, invented TOOL_SHA/CASE_TABLE_SHA: red at L5, L6, L7, L8, L9 (FORGE 1).
- Same with stamp consistent to the real bytes: red at L5, L6, L7, L8 (FORGE 2).
- Same plus ledger flip and tool pin: red only at L5 and L6. These two legs are the sole guards against invented vectors (FORGE 2b).
- Round-91 receipt bytes copied: red at L2, L5, L6, L7, L8, L9 (FORGE 3).
- Gate closed override with names-only-absent-path (override-unanchored): red, `DEFECT override-unanchored` + `check-failed` (FORGE 12).
- Gate blocked owner `nobody` with the fixture conf: red, `DEFECT owner-not-a-lane` (FORGE 13).
- Gate closed `check:"true"` standalone with a reason: red, `DEFECT closed-check-vacuous` (FORGE 7).

## Mispredicts and lower-severity observations

- L-a: the chain-open refusal (two-level open chain, base opened 39) is correct (`freeze=refused pending=1 oldest_pending_round=39`), but the output does not name the pending id or the chain-end, unlike the brief's expectation.
- L-b: C1 L5 does not check id uniqueness; L6 is the only guard (code reading, not exercised).
- L-c: C1 L6 rerun `subprocess.run(timeout=900)` is unguarded; a timeout yields a traceback, rc 1, no PREDICATE line (code reading, not exercised). Same class as M12.
- L-d: the C1 counter does not parse receipt `PREDICATE` lines.
- L-e: the cheat probe's receipt recorded `WORKTREE dirty`; the clone was clean when checked later; cause not established.
- L-f: round92 counter bytes are absent from the pin ledger, so M9's `PINS checked=17` covers only the round-91 set.

## Install / environment

No installs or updates. No sysctl touched (`max_user_namespaces` = 122865). Only my own scratch processes were killed (pattern restricted to my scratch path).

## Checks for the main agent

- Do not rely on C3 default-path output until H2 is fixed; `--selftest` completing is not the predicate.
- Pin all round-92 instruments (C1 probe and counter, C2 counter, gate) before the official run; H4 and H5 depend on it.
- H1 needs the override and no-check paths to pass through `vacuous_check` and the anchor rule, with tests for `true # grep`, `true 1.0`, and a check-less closed row.
