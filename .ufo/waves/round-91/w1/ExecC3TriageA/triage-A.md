# ExecC3TriageA — routed-findings triage, half A (drafts only)

Seat `ExecC3TriageA`, round 91, wave w1. Clone `$S/lane` at `a8de3e69` (`git clone --shared`, detached). The ledger `corpus/routed-findings.jsonl` (213 rows, all parse) was read and not edited. Resolution rows are in `resolutions.jsonl` (24 rows: 21 findings plus 3 override-reason rows). No commit, no mutating git in the lane, no subagent.

Source line check: every `source` in `resolutions.jsonl` resolves at `a8de3e69` (`git show a8de3e69:<path>` then the line is non-blank; checked by python, all 24 True).

## Supersede rule used

The gate (`plans/round91_burndown.py:175-196`, read) keys each supersede by its target id, flags a second row on the same target as `supersedes-duplicate`, and resolves one level only. Where a base id has no supersede yet, the resolution supersedes the base id (rows R83-V2, R84-V2/3/4/8/9, R85-V1..V8, R86-V1/2). Where a base id already has a supersede (R82-F1, R51-R1..R4, R42-R2, R42-R3-33, R42-R3-37), the resolution supersedes the newest existing row, to avoid a duplicate. The gate does not follow that chain (see Gate observations), so those rows are recorded but do not change the gate's effective state.

## Verdicts

### 1. R82-F1 — closed (`R82-F1-R91`, chains to open `R82-F1-R90`)

- Command: `python3 plans/round91_f1_counter.py --lane . --work .ufo/waves/round-91/gate-f1`, exit 0.
- Observed: `PARSED S260=1,S261=2,S265=1,S266=2`; `ANCHORLINE rows=274 cited=84 captured=71 uncaptured=13 defective=10 repaired=10 live=0 cells=0 rc=0`; `WRONG-LINE-CAUGHT True`; `PREDICATE R91-F1 pass`.
- Negative: the two curly-quote regexes renamed in a throwaway clone copy of `plans/anchor_line_check.py`, `python3 plans/round91_f1_counter.py ...` exit 1 with `DEFECT PARSE-ABSENT` for S260, S261, S265, S266 and `DEFECT WRONG-LINE not caught`.
- Hazard hit: the first negative rebuilt the checker's `.pyc` within the same second as the restore, so the next run read stale bytecode and exited 1 (`PARSED` empty). `rm plans/__pycache__/anchor_line_check*.pyc` cleared it; the rerun exited 0. The checker's bytes matched the pin `814a091e…` throughout (`sha256sum` = HEAD = pin).
- Gate effect: none yet. `R82-F1` is decided by `R82-F1-R90` (open), so it remains pending and the freeze stays refused on age (opened 82, threshold 90).

### 2. R83-V2 — blocked, owner kengaku (`R83-V2-R91`)

- Command: `sed -n 3p corpus/knowledge/tb2-code-from-image-offline.md`, exit 0. Observed: `recheck: 2026-11-04 … cadence monthly … pin 2fd12b88…`. Header half repaired.
- Command: `grep -c R83-V2 SCORECARD.md`, and the same for `LOG.md`. Both print `0` (grep exit 1 for zero matches). The routed report and SCORECARD supersession has no dated line.
- Decision: blocked. The routed half is open.

### 3. R84-V2 — closed (`R84-V2-R91`)

- Command: `git cat-file -e cd0c116ef8c453d076031bdf5888b1e1b83bb0be:plans/round91-cases.json && grep -q 'L4 case table not byte-identical to freeze commit' plans/round91_c1_replay.py`, exit 0.
- Negative: the same `cat-file` against base `59764383d4dd33d58faa50daad4c06d0cde410aa`, exit 128 (`path … exists on disk, but not in …`).
- Observed: leg L4 at `plans/round91_c1_replay.py:158-165` compares the measured table to the freeze blob and defects when it is absent (`a_bytes is None` makes `l4` false).
- Decision: closed. The round-84 table and counter are not edited.

### 4. R84-V3 — blocked, owner kengaku (`R84-V3-R91`)

- Command: `grep -c -i forg plans/round91_c1_replay.py`, exit 0, count 1 (the docstring "forgery 1b" reference).
- Observed: legs L1–L9 are the only checks; the L6 re-run is unconditional (`plans/round91_c1_replay.py:180-204`). A correct-vector forged receipt reproduces its observation block under L6, so no control in the counter shows it failing.
- Decision: blocked. The correct-vector control is owed by the lane.

### 5. R84-V4 — blocked, owner kengaku (`R84-V4-R91`)

- Command: `sed -n 297,299p .ufo/l0-questions.md`, exit 0. Line 297 is the `kengaku | round-84 | Q13 checker shape` question; lines 298–299 are other rounds' questions, with no answer.
- Command: `sed -n 239,245p plans/gate_timing_check.py`, exit 0. `is_second_wave` still accepts only `falsify` and `wave2`.
- Decision: blocked. The operator ruling is still unanswered.

### 6. R84-V8 — blocked, owner kengaku (`R84-V8-R91`)

- Command: `python3 plans/round82_c1_plans_registry.py --lane . --tip HEAD --work <dir>`, exit 1. Output: `DEFECTS n=4` (`ROW-SELFTEST-UNBACKED` for `round88-c1-replay`, `round88-claim-figures`, `round89-c1-replay`, `round89-claim-figures`) and `PREDICATE R82-C1 fail`.
- Observed: `SELFTEST-FLAG` is absent from the output (count 0), and `round83-c2-debt` reads `defects=none`. The specific flag the row names no longer prints. The gate is still red, so the carried red gate is not closed.
- Decision: blocked. Owner kengaku holds the registry fix.

### 7. R84-V9 — closed (`R84-V9-R91`)

- Command: `git rev-parse -q --verify 59764383d4dd33d58faa50daad4c06d0cde410aa^{commit} >/dev/null && grep -q 'Base: .59764383d4dd33d58faa50daad4c06d0cde410aa.' plans/round-91-claims.md`, exit 0.
- Negative: the same check with a nonexistent sha `0000000000000000000000000000000000000001` in place of the base, exit 1.
- Observed: `plans/round-91-claims.md:4` reads "Base: `59764383d4dd…`", an existing revision.
- Decision: closed. The prospective condition is met by the round-91 freeze.

### 8. R85-V1 — blocked, owner kengaku (`R85-V1-R91`)

- Command: `grep -rln flip_ledger plans/`, exit 0. Matches are `plans/round80_c1_located_replay.py`, `plans/round85_c1_replay.py`, `plans/round86_c1_replay.py`. None is round 91.
- Decision: blocked. No revision-bound successor battery or probe selftest was located.

### 9. R85-V2 — blocked, owner kengaku (`R85-V2-R91`)

- Command: `grep -c -i indistinguishable plans/round-91-claims.md`, exit 1, count 0.
- Observed: the round-91 claim binds revision and host stamps (L3, L8, L9), but prices no indistinguishable copies. The lesson asks for that pricing.
- Decision: blocked.

### 10. R85-V3 — blocked, owner kengaku (`R85-V3-R91`)

- Not closed. No landing for the named repairs was located in this half's pass. The seat did not re-audit each round-91 instrument against the six named items, so this verdict is "not located", not "absent after audit".
- Decision: blocked.

### 11. R85-V4 — blocked, owner kengaku (`R85-V4-R91`)

- Command: `sed -n 410,414p plans/round85_c2_debt.py`, exit 0. Line 412 still reads `tree = rev_tree(lane, args.rev, work) if args.rev else Tree(lane, "worktree", "worktree")`.
- Decision: blocked. Not landed.

### 12. R85-V5 — blocked, owner kengaku (`R85-V5-R91`)

- Command: `grep -n 'read_text' plans/round82_c1_plans_registry.py`, exit 0. Line 255 reads `bodies[rel] = (lane / rel).read_text(errors="replace")`, with no revision argument, so `--tip` does not bind instrument bytes.
- Decision: blocked.

### 13. R85-V6 — blocked, owner kengaku (`R85-V6-R91`)

- Command: `grep -c TimeoutExpired plans/round91_c1_replay.py`, exit 1, count 0.
- Observed: the L6 re-run at line 199 is `subprocess.run(..., timeout=600)` with no `TimeoutExpired` handler. A stalled sandbox raises instead of printing `DEFECT SETUP sandbox-unavailable` and `PREDICATE R91-C1 could-not-evaluate` with exit 2, which the claim requires.
- Decision: blocked.

### 14. R85-V7 — blocked, owner kengaku (`R85-V7-R91`)

- Command: `grep -rln 217910c513a46b5ff607561136e4beaac056ace0 .ufo/reports`, exit 1, no output. The same for `da463cbdc1ee9c116fe239fb24f41c99fa0807c7`.
- Observed: the round-90 report carries a counting command (`.ufo/reports/round-90/kengaku.md:55`). The round-91 report is not yet filed.
- Decision: blocked, owed in the round-91 report.

### 15. R85-V8 — blocked, owner kengaku (`R85-V8-R91`)

- Command: `grep -n -i precedence .ufo/l0-questions.md`, exit 0. Matches are lines 105 and 178 only (round-50 and round-74). No run-15 precedence question or answer exists.
- Decision: blocked. The operator clarification is still open.

### 16. R86-V1 — blocked, owner kengaku (`R86-V1-R91`)

- Command: `grep -rn ExecGatesR86 LOG.md corpus/lessons/`, exit 0. Matches are only in `corpus/lessons/round-86-verifier-spotcheck.md` lines 79, 181, 238. `LOG.md` has none.
- Command: `ls .ufo/waves/round-86/L1/outside-gates.txt`, exit 2 (absent).
- Decision: blocked. The erratum naming `W1/ExecGatesR86/gate-receipt.txt` is owed.

### 17. R86-V2 — blocked, owner kengaku (`R86-V2-R91`)

- Command: `grep -n 'zero dead seats' LOG.md`, exit 1, no output. No erratum naming report lines 7 and 242 was located.
- Decision: blocked.

### 18. R51-R1 — blocked, owner kama (`R51-R1-R91`)

- Command: `curl -s -m5 http://127.0.0.1:45669/v1/models`, exit 7 (connection refused). The row's check (`… | grep -q 'LFM3-1.7B'`) fails today.
- Decision: blocked, owner kama. The serving-plane flag authority is kama's (row next).

### 19. R51-R2 — refused (`R51-R2-R91`)

- Standing blocker quoted from `R51-R2-R90`: "the fleet schema is not decided". The owner `protocol` names no lane or seat, so the row is refused rather than parked. The base check is mis-scoped (`../*-shokunin/corpus/routed-findings.jsonl` expands to this lane's ledger only), which `R51-R2-R90` already records.
- Decision: refused.

### 20. R51-R3 — refused (`R51-R3-R91`)

- Command: `test -e ~/Projects/webzites/repos/llm-wiki; test -e ~/archive/bench-arena; test -e ~/Projects/bounties/ledger/telemetry.jsonl`, each exit 1 (absent).
- Standing blocker quoted from `R51-R3-R90`: "operator decision: restore or retire the three declared trees". Owner `unowned:integrator` names no lane or seat, so the row is refused.
- Decision: refused.

### 21. R51-R4 — blocked, owner kama (`R51-R4-R91`)

- Command: `curl -s -m5 -o /dev/null -w '%{http_code}' http://127.0.0.1:34113/health`, prints `000`.
- Decision: blocked, owner kama. Whether the qwen-coder unit is retired is kama's decision (row next). `systemctl --user` was not re-measured (no DBUS session).

## Override reasons (closed rows whose deciding check differs from the base check)

Scan of the whole ledger: exactly three closed rows have a deciding check that differs from its base check and no `override_reason`: `R42-R2-R90`, `R42-R3-33-R90`, `R42-R3-37-R90`. Each gets a supersede row (`R42-R2-R91`, `R42-R3-33-R91`, `R42-R3-37-R91`), same status (closed), with the verified reason.

- `R42-R2` — base check `cd "$LANE" && python3 plans/routed_open.py --lane . --list | grep -qE '^ROW R42-R2\.[12] status=closed' && test -f plans/scratch_guard.py`: exit 1 at tip (`routed_open.py --list` prints no `ROW R42-R2.x` lines). R90 check `test -f plans/scratch_guard.py && python3 plans/scratch_guard.py --selftest … && grep -qs 'scratch-root-guard' SKILL.md`: exit 0. New check (same predicate, relative path): exit 0. Negative (`zzz-absent` token): exit 1.
- `R42-R3-33` — base `grep -qF '9 witnessed of 20' "$LANE/plans/round-43-claims.md"` with `LANE` set: exit 0. R90 check: exit 0. New check: exit 0. Negative (`zzz witnessed`): exit 1.
- `R42-R3-37` — base `cd "${LANE:?}" && grep -q 'host="libc-rand"' … && grep -q "libc.srand" … && grep -q "host=libc-rand" …` with `LANE` set: exit 0. R90 check: exit 0. New check: exit 0. Negative (`host="zzz"`): exit 1.

Reasons (verbatim in `resolutions.jsonl`): R42-R2 — the base check fails on the instrument claim, not the work; R42-R3-33 and R42-R3-37 — the predicates are identical and only spelling differs, both checks exit 0.

## Checks for closed rows (exit codes, run from lane root)

| row | command (abridged) | exit | able-to-fail | 
|---|---|---|---|
| R82-F1-R91 | `python3 plans/round91_f1_counter.py --lane . --work .ufo/waves/round-91/gate-f1` | 0 | 1 (curly regexes renamed) |
| R84-V2-R91 | `git cat-file -e cd0c116e…:plans/round91-cases.json && grep -q 'L4 case table…' plans/round91_c1_replay.py` | 0 | 128 at base sha |
| R84-V9-R91 | `git rev-parse -q --verify 59764383…^{commit} && grep -q 'Base: .59764383….' plans/round-91-claims.md` | 0 | 1 (nonexistent sha) |
| R42-R2-R91 | `test -f plans/scratch_guard.py && … --selftest … && grep -qs 'scratch-root-guard' SKILL.md` | 0 | 1 (`zzz-absent`) |
| R42-R3-33-R91 | `grep -qF '9 witnessed of 20' plans/round-43-claims.md` | 0 | 1 (`zzz witnessed`) |
| R42-R3-37-R91 | `grep -q 'host="libc-rand"' … && grep -q 'libc.srand' … && grep -q 'host=libc-rand' …` | 0 | 1 (`host="zzz"`) |

Each negative was run by changing one token; the rows have no other check.

## Gate observations (drafts only; the ledger and gate are not edited)

Fixture route: `python3 plans/round91_burndown.py --lane . --work <dir> --freeze-round 92 --file <ledger>`.

1. Tip ledger, no rows (`--rev a8de3e69`): `freeze=refused pending=30 parked=7 unowned_blocked=0 seeds_83_91=46 checks_run=114 overrides=3`, `PREDICATE R91-C3 fail`, exit 1, with `DEFECT override-unjustified R42-R2`, `…R42-R3-33`, `…R42-R3-37` and `DEFECT check-failed R82-V8 rc=1`.
2. Base plus half A (`fixture-ledger.jsonl`): exit 1, `freeze=refused pending=16 parked=19 malformed_unresolved=0 seeds_83_91=46 resolutions=58 checks_run=116 overrides=3`. The same three `override-unjustified` defects remain, and `check-failed R82-V8` remains.
3. Base plus half A plus half B (`union-ledger.jsonl`): exit 1, `freeze=refused oldest_pending_round=82 pending=1 parked=26 unowned_blocked=0 malformed_unresolved=0 seeds_83_91=46 resolutions=74 checks_run=123 overrides=3`, four DEFECT lines.

What the gate shows:

- The supersede chain is not followed. `R82-F1` remains effective-open via `R82-F1-R90` (the one pending row in case 3), so the freeze stays refused on age. Gate code reads one level (`supersedes_by_target` is keyed by the base id, and rows that carry `supersedes` are skipped in the state loop, `plans/round91_burndown.py:200-209`).
- `override-unjustified` for `R42-R2`, `R42-R3-33`, `R42-R3-37` persists. The gate reads the `R90` row as the deciding row, which has no `override_reason`, so the appended reason rows are inert. Fixing this needs the R90 row to carry the reason (append-only, so not done here) or a gate that follows the newest supersede.
- `R82-V8` (base row, not in this half) fails from the clone cwd: `python3 plans/round83_c2_checks.py v8` prints `CHECK v8 fail`, exit 1. The C3 claim says this check must pass from a clone cwd. It is recorded for the integrator and not repaired here.
- A second `supersedes` on a base id would produce `supersedes-duplicate` (`plans/round91_burndown.py:183-196`); no such row is in this half, because the chain rule above avoids it.

## Limits

- Seat did not edit the ledger, make commits, or run mutating git in the lane. Scratch `$S` removed on exit.
- Blocked owners are lane or seat names (`kengaku`, `kama`). `protocol` and `unowned:integrator` name no lane or seat, so those rows are refused, not parked.
- Not verified: R85-V3 instrument-by-instrument (see verdict 10).
- Tooling: none installed. Used git, python3 standard library, grep, sed, curl, and the lane's own gate and counter.
