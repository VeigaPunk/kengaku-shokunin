# bench-arena task 27 timeout anatomy — hidden contract + thread-exception deadlock

Instrumented post-mortem of `27-rwlock-writer-pref`'s `test_rc=124` (60 s
timeout) in both v2 and r5 — closes corpus gap "27 test-timeout:
unclear whether solvable-but-slow or algorithmically wrong". Method: rewrote
`test.sh`'s inline python as a standalone file with
`faulthandler.dump_traceback_later(25, exit=True)` + `PH(n)` markers at each
of the test's 3 phases; ran reference, r5 gen, r6 gen, and an r5-gen patch.
Verified 2026-09-28.

## Finding 1 — the timeout is a thread-exception deadlock, not slowness

The test's phase 1 reader threads read `rw._active` (a **private attribute
never specified in `prompt.md`** — prompt requires only the four public
methods). r5's generated `RWLock` names its counter `_readers`, so all six
reader threads raise `AttributeError` and die *before* reaching
`ready.wait()`. The main thread then blocks forever on `Barrier(7)` — six
dead parties never arrive. faulthandler dump:

```
Exception in thread Thread-1 (reader): AttributeError: 'RWLock' object has
no attribute '_active'  (×6 readers)
Timeout (0:00:25)!
Thread …/main: test27_instr.py line 40 in <module>  → ready.wait()
```

Mechanism: **an exception in a `threading.Thread` does not terminate the
process and does not trip the test's own `sys.exit(1)` paths** — the crashed
party just never arrives at its barrier/event, and every `join(timeout=…)`
returns quietly. `timeout 60` is the only thing that ever reports it, as an
opaque `rc=124`. The reference solution passes the whole test in 0.23 s —
nothing about a correct run is slow.

## Finding 2 — the hidden contract is load-bearing

`test.sh` line ~28: `read_counts.append(rw._active)` — needs both the name
`_active` AND reader-count semantics (asserts `max ≥ 2`, `len == 6`). The
reference stores exactly this (`self._active` = signed active count). Any
spec-faithful implementation with a different private name fails phase 1 —
**task 27 tests an underspecified private interface**. Benchmark-defect
class: prompt API ≠ tested API. A model that obeys the prompt literally has
no path to PASS unless it guesses the reference's internals.

## Finding 3 — under the hang, the r5 solution is also semantically wrong

Patching r5's sol with `@property _active → _readers` (alias only) unblocked
phase 1 and revealed real lock-semantics bugs in 0.25 s:

- `release_write()` → `RuntimeError: release unlocked lock` (its
  `_writer_lock` discipline double-releases).
- Phase 2: `late reader acquired before waiting writer` ×3 — writer
  preference not honored.

So r5's 27 was BOTH hidden-contract-hanged AND semantically incorrect;
the timeout masked the second defect entirely.

## Finding 4 — different gens produce different failure signatures

| Gen | `_active`? | Failure | Signature |
|---|---|---|---|
| r5 | no (`_readers`) | reader-attr deadlock + broken release_write | rc=124, 60 s, silent |
| r6 | no | `TypeError: Condition(condition=Lock())` at `RWLock()` | rc=1, instant |

The model invented a nonexistent `Condition(condition=…)` kwarg in r6 —
wrong-API hallucination is a third failure family on this task (neither
timeout nor logic bug).

## Rules extracted

1. `test_rc=124` + bounded joins ⇒ check for **crashed worker threads**
   before assuming slow code; instrument with `faulthandler.dump_traceback_
   later`, never re-run blind at a longer timeout.
2. A threaded test that joins with timeouts still deadlocks when a worker
   *dies* — exceptions in threads fail open toward hang, not fail.
3. Diff the test's attribute accesses against the prompt's public API:
   `grep -oE 'rw\._[a-z_]+'` on test body vs prompt terms — mismatches are
   hidden contracts; flag the task, don't credit/blame the model.
4. To isolate hidden-contract hang from semantic deadlock, patch the missing
   attr as an alias property — if it still hangs, the lock logic is wrong
   too (r5: both).

Artifacts: `/tmp/bench-r6/t27/{test27_instr.py,r5_sol.py,r5_sol_active.py,
r6_sol.py,ref_sol.py}` (ephemeral); instrumented test derived from
`~/bench-arena/tasks/27-rwlock-writer-pref/test.sh`.
