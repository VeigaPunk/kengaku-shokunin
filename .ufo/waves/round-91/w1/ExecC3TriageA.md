# ExecC3TriageA — round 91, wave w1 — report

Scope: routed-findings triage, half A (21 findings) plus three override-reason rows. Drafts only: the ledger, the lane and every gate were read, not edited. Full per-finding commands and output: `.ufo/waves/round-91/w1/ExecC3TriageA/triage-A.md`. Rows: `.ufo/waves/round-91/w1/ExecC3TriageA/resolutions.jsonl` (24 rows, one per line, all parse, ids unique, no pipe, every source resolves at `a8de3e69`).

## Verdicts

| finding | verdict | row | owner | decisive command, exit |
|---|---|---|---|---|
| R82-F1 | closed | R82-F1-R91 (chains to open R82-F1-R90) | kengaku | `python3 plans/round91_f1_counter.py --lane . --work .ufo/waves/round-91/gate-f1` → 0; negative (curly regexes renamed) → 1 |
| R83-V2 | blocked | R83-V2-R91 | kengaku | `grep -c R83-V2 SCORECARD.md` / `LOG.md` → 0 / 0 (routed half unevidenced) |
| R84-V2 | closed | R84-V2-R91 | kengaku | `git cat-file -e cd0c116e:plans/round91-cases.json && grep -q 'L4 case table…' plans/round91_c1_replay.py` → 0; base sha → 128 |
| R84-V3 | blocked | R84-V3-R91 | kengaku | `grep -c -i forg plans/round91_c1_replay.py` → 1 (no correct-vector control) |
| R84-V4 | blocked | R84-V4-R91 | kengaku | `sed -n 297,299p .ufo/l0-questions.md` → no answer |
| R84-V8 | blocked | R84-V8-R91 | kengaku | registry `--tip HEAD` → 1, `DEFECTS n=4` ROW-SELFTEST-UNBACKED; SELFTEST-FLAG no longer printed |
| R84-V9 | closed | R84-V9-R91 | kengaku | `git rev-parse -q --verify 59764383…^{commit} && grep -q 'Base: .59764383….' plans/round-91-claims.md` → 0; nonexistent sha → 1 |
| R85-V1 | blocked | R85-V1-R91 | kengaku | `grep -rln flip_ledger plans/` → no round-91 file |
| R85-V2 | blocked | R85-V2-R91 | kengaku | `grep -c -i indistinguishable plans/round-91-claims.md` → 0 (exit 1) |
| R85-V3 | blocked | R85-V3-R91 | kengaku | not located in this pass; not re-audited instrument by instrument |
| R85-V4 | blocked | R85-V4-R91 | kengaku | `sed -n 410,414p plans/round85_c2_debt.py` → line 412 still `Tree(lane, "worktree", "worktree")` |
| R85-V5 | blocked | R85-V5-R91 | kengaku | `grep -n read_text plans/round82_c1_plans_registry.py` → line 255 working-tree read |
| R85-V6 | blocked | R85-V6-R91 | kengaku | `grep -c TimeoutExpired plans/round91_c1_replay.py` → 0 (exit 1); L6 `subprocess.run(timeout=600)` unhandled |
| R85-V7 | blocked | R85-V7-R91 | kengaku | `grep -rln 217910c5… .ufo/reports` → none; owed in the round-91 report |
| R85-V8 | blocked | R85-V8-R91 | kengaku | `grep -n -i precedence .ufo/l0-questions.md` → round-50/74 lines only |
| R86-V1 | blocked | R86-V1-R91 | kengaku | `grep -rn ExecGatesR86 LOG.md corpus/lessons/` → lesson only; `ls .ufo/waves/round-86/L1/outside-gates.txt` → 2 |
| R86-V2 | blocked | R86-V2-R91 | kengaku | `grep -n 'zero dead seats' LOG.md` → none (exit 1) |
| R51-R1 | blocked | R51-R1-R91 | kama | `curl -s -m5 http://127.0.0.1:45669/v1/models` → 7 (connection refused) |
| R51-R2 | refused | R51-R2-R91 | — | quoted R51-R2-R90 blocker "the fleet schema is not decided"; owner `protocol` names no lane or seat |
| R51-R3 | refused | R51-R3-R91 | — | `test -e` on the three trees → 1 each; quoted "operator decision: restore or retire…"; owner `unowned:integrator` names no lane or seat |
| R51-R4 | blocked | R51-R4-R91 | kama | `curl -s -m5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health` → 000 |

Override reasons (the only closed rows whose deciding check differs from the base check; each gets a same-status supersede row): `R42-R2-R91`, `R42-R3-33-R91`, `R42-R3-37-R91`. Base check at tip: R42-R2 exit 1 (routed_open emits no ROW lines), R42-R3-33 exit 0, R42-R3-37 exit 0; R90 checks exit 0 each; the new check of each row exits 0; the token-swap negative of each exits 1.

## Gate findings (for the integrator; not repaired)

1. The gate follows one supersede level. `R82-F1` stays effective-open via `R82-F1-R90`; the appended `R82-F1-R91` is inert. Code: `plans/round91_burndown.py:206` skips supersede rows in the state loop.
2. `override-unjustified` for `R42-R2`, `R42-R3-33`, `R42-R3-37` persists, since the deciding row is the R90 row without `override_reason`; the appended reason rows are inert. Fixing this needs a gate that reads the newest supersede (or an append-only way to attach the reason to the deciding row).
3. A second supersede of an already-superseded base id would raise `supersedes-duplicate` (`plans/round91_burndown.py:195`). I avoided this by chaining; the chain rule is in `triage-A.md`.
4. `R82-V8` (not in this half) fails from a clone cwd: `python3 plans/round83_c2_checks.py v8` → `CHECK v8 fail`, exit 1. C3 requires that check to pass from a clone cwd.
5. Gate results: tip ledger alone, `--freeze-round 92` → exit 1, `freeze=refused pending=30 parked=7`. Base plus half A → exit 1, `pending=16 parked=19`. Base plus half A plus half B (`ExecC3TriageB/resolutions.jsonl`) → exit 1, `freeze=refused oldest_pending_round=82 pending=1 parked=26 malformed_unresolved=0 seeds_83_91=46 resolutions=74 checks_run=123 overrides=3`, four DEFECT lines (three override, one R82-V8).
6. Hazard seen while proving R82-F1: a negative control that rewrites a checker and restores it within the same second leaves a stale `plans/__pycache__/*.pyc` that the next run reads. Clearing the cache fixed it. Any counter whose negative test edits its own module needs `rm` of that cache or `-B` plus a cleared cache.

## Install and cleanup

- Tooling: none installed. Used git, python3 standard library, grep, sed, curl, and the lane's own counter and gate.
- Scratch `$HYAKU_SCRATCH/kengaku-r91/ExecC3TriageA` removed on exit (verified absent).
- Lane: no commit, no mutating git, no subagent, no edit to the ledger, MANIFEST, .ufo/state, scripts or templates. Files written: `.ufo/waves/round-91/w1/ExecC3TriageA.md`, `.ufo/waves/round-91/w1/ExecC3TriageA/resolutions.jsonl`, `.ufo/waves/round-91/w1/ExecC3TriageA/triage-A.md`.
