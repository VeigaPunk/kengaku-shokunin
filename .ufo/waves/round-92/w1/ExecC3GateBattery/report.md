# R92-C3 gate battery — ExecC3GateBattery (round-92 / w1)

Seat: leaf executor. Scope: controls on scratch clones at B2 `f0018773`, BASE `4ba56182`.
Subagents dispatched: none. Commits, pushes, lane git mutations: none. Lane git reads only.
Ledger, overrides and gate files: not modified. Fleet root: read only (shokunin.conf; the
R82 fleet report, read by R82-V8 through SHOKUNIN_ROOT).

## Result

The R92-C3 frozen predicate is not met at B2 by these controls:

| control | expectation | actual | verdict |
|---|---|---|---|
| 1 gate-at-B2 (v3) | pending=0, no DEFECT, admitted (rc 0/1 as stated) | refused, pending=1 (malformed root R82-F1, line 125), DEFECT check-failed R82-V8; literal run crashes in the in-path selftest | FAIL (F-1, F-2, F-3) |
| 2 gate-at-BASE (v3) | rc 1, refused, three override-unjustified, pending=1 oldest 82 | refused, pending=1 oldest 10000, same two DEFECTs; no override-unjustified | MISMATCH (F-1, F-2) |
| 3 gate-v2-at-B2 | rc 1, three override-unjustified, pending=1 | exactly that, plus one extra DEFECT check-failed R82-V8 | MATCH + 1 extra (F-3) |
| 4 selftest | cases=10 red-green-ok=10, rc 0 | cases=10 red-green-ok=10, rc 0 | PASS (standalone only) |

The kill rule applies: a failing check at the tip (R82-V8) and an unmet predicate
(freeze=refused at the tip) mean the claim stops with this DEFECT list, as the claim text says.
Per the frozen text this seat does not repair anything; the findings are for the L1.

## Findings (blocking for R92-C3 at B2)

**F-1 — predicate-path selftest recurses and never completes (M8).**
`in_child_mode` (round92_burndown.py:553-567) accepts a parent only when `/proc/<ppid>/cmdline`
contains `round92_burndown.py` **and** `--selftest`. The predicate invocation (`--freeze-round 92`,
no `--selftest`) calls `selftest(work/"predicate-selftest")` at line 594. Each child is launched
by `gate()` (lines 439-453) from a non-`--selftest` parent, so the child fails the check, runs its
own selftest, and launches grandchildren. The nesting is unbounded; each level waits up to 600 s.
Observed: controls 1 and 2 raised `subprocess.TimeoutExpired` out of `main()` with rc=1 and printed
no `freeze=`, `DEFECT` summary, or `PREDICATE` line. I killed the eight orphaned gate processes
from my scratch tree and left sibling processes alone. Standalone `--selftest` (control 4) passes,
which is why the battery looked green.
Corroboration: lane master commit `a0c7438a` (E5, "battery child-proof accepts any live-gate
parent — the recursive battery hang the tip run caught") is after B2.

**F-2 — malformed root R82-F1 cannot be resolved by its supersede chain (M13).**
Ledger: line 125 `R82-F1` (source `corpus/lessons/round-82.md ## Corrections (R81-V2)` fails the
`<path>:<line>` schema) <- line 213 `R82-F1-R90` (open, supersedes R82-F1) <- line 214
`R82-F1-R91` (closed, supersedes R82-F1-R90, close = the QUOTE_RE repair).
In `evaluate()` the invalid-row branch (round92_burndown.py:261-275) computes
`end = chain_end_cache.get(sid, sid)` (line 263). `chain_end()` is only called for valid base rows
(line 255), and no valid base row's walk passes through an invalid root, so the cache misses and
`end` is `R82-F1` itself. `by_id` has no `R82-F1`, so the row is never superseded: it stays a
pending DEFECT `line 125: R82-F1` and `malformed_unresolved=1`. The fix this code needs is to call
`chain_end(sid)`; I did not apply it. Evidence type: code reading plus the observed outcome on
the real ledger [INFERENCE on mechanism until the L1 reproduces it on a one-level fixture; the
observed outcome is measured]. The selftest has a `malformed` case, but it only checks an
unresolved root, so it does not cover this path (F-4).
Corroboration: lane master (after B2) line 263 reads `end = chain_end(sid)`, and commit
`b72c83e9` (E6) says it "walks invalid-row supersede chains".

**F-3 — checks never receive SHOKUNIN_ROOT; R82-V8 fails inside the gate (M6).**
`run_check` (round92_burndown.py:153-160) runs each check with
`env={"PATH","HOME","LANE"}` only. `round83_c2_checks.py` v8 resolves the fleet from
`R83_FLEET_REPO`/`SHOKUNIN_ROOT` and otherwise `origin.parent`, where origin is the worktree root
and the fallback is the `--work` parent. That directory holds no `.ufo/reports/round-82/kengaku.md`,
so v8 fails at the tip. round91_burndown.py's check runner (line 120) has the same shape and never
mentions SHOKUNIN_ROOT, so control 3 shows the same extra DEFECT.
R82-V8 reproduction (scratch worktree at B2, removed afterwards):
- gate's environment (`env -i PATH HOME LANE`): `CHECK v8 fail`, rc 1.
- same, plus `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin`: `CHECK v8 ok`, rc 0.
- `origin.parent` under the gate env resolves to `<scratch>/r4`, which has no fleet report.
The pinned bytes match the live fleet file (sha256 5a83443d…8b0480 both for
`git show c839b658:.ufo/reports/round-82/kengaku.md` and the fleet file), so the check's data is
fine; the environment is what breaks it. The same failure reproduces on the real lane, because
the `--work` parent is not the fleet root.
Corroboration: lane master commit `b72c83e9` (E6) says it "exports SHOKUNIN_ROOT to checks", and
master line 158 has `"SHOKUNIN_ROOT": fleet_root`, and `dd48027f` (E7) takes the fleet root from the
lane's parent. Both are after B2.

**F-4 — coverage gap in the battery (M8/M13).** The selftest runs only as a top-level
invocation. It never runs the predicate-path battery to completion (F-1), and no case resolves an
invalid root (F-2). Ten-of-ten green is therefore not evidence for the predicate path.

**F-5 — environment dependence, disclosed, not a gate defect.** Without `SHOKUNIN_ROOT`, a clone
whose parent lacks `shokunin.conf` gets `DEFECT SETUP shokunin.conf unreadable` and rc 2
(control 0). The gate fails closed here, which is correct. The L1 measured tip runs at a lane
whose parent is the fleet root, so this does not bite there.

## Triage list for the L1 (row ids, B2)

- `line 125 / R82-F1` — F-2 (gate code). Chain tip R82-F1-R91 (line 214) is closed and well-formed.
- `check-failed R82-V8` — F-3 (gate and v2 environment). Not a ledger row.
- No override-unjustified, owner-not-a-lane, closed-check-vacuous, override-unanchored, or
  stale-open DEFECTs at B2 under v3. The R42-R2 / R42-R3-33 / R42-R3-37 overrides pass their
  base and override checks at the tip under v3.
- Note: `routed_open.py --list` itself prints `DEFECT line=125` (the R42-R2 base check's reason
  string says so), so the same malformed row also affects the R42-R2 base check.

## Lane master beyond B2 (read-only observation; not tested here)

`git log f0018773..master` shows commits `d1ccf56d`, `b62ea270`, `6a51ff0e`, `1d5634e3`, `801b8157`,
`5b6c00b8`, `a0c7438a` (E5), `b72c83e9` (E6), `dd48027f` (E7), `288511d8`. The gate file differs
from B2 by 10 insertions and 7 deletions. Master already contains repairs for F-1, F-2 and F-3.
Those repairs are after the pinned B2 revision, so B2 is not the measured tip for them. The L1
must decide whether T is the B2 bytes plus the freeze rules or a later revision. That is not a
call for this seat. I did not run the controls at master, which is outside the pinned scope.

## Tool installs and updates

None. Used the host's Python 3.14.8 and git 2.56.0 as found. Ran no package-manager
commands.

## Process and scratch

- Scratch `/fast/scratch/hyaku/kengaku-r92/ExecC3GateBattery` (clone `--shared`, `r2/`, `r3/`,
  `r4/` work dirs). Receipts copied to `receipts/`. The scratch tree is removed at the end of this seat.
- Orphans: eight of my own gate children from controls 1-2 were stopped with SIGTERM then
  SIGKILL (pattern restricted to my scratch clone). Sibling SentinelForge processes were untouched.
- Scratch worktrees created inside my clone were removed with `git worktree remove`; the lane's
  `.git` was not touched.

## Peer messages

ReviewerV4 sent an informational pin-verification note (no request). No reply was needed.
