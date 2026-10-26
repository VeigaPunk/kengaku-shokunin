# R43RoutedQueue — the five drafted rows that must not be appended as-is

Measured 2026-10-26 19:2x -03 at lane worktree HEAD `d33350f…`; lane ledger sha256 at the snapshot
`c56fa2a24cd302a5eaf9a2996d6528c0c91a873f4970c2e1a0f009bca447f338` (60 rows: the 16 I inherited, three rows a
sibling seat appended, my 41).

## A. Three rows superseded by rows already in the ledger (drop mine; keep exactly one per defect)

| drafted row | F42RevRiders defect | covered by | measured state |
|---|---|---|---|
| `R42-R3-24` | D1 — R42-R4 open while its check passes | the ledger's own `R42-R4` row, now `status: "closed"` with `close: "corpus/QUALITY.md:759 (Q34 states rule 2 in-lane) + 0 removed lines …"` | `OBSERVE R42-R4` no longer appears in a `--observe` run (it did at 19:19: `rc=0 … self=open MISMATCH`) |
| `R42-R3-25` | D2 — R42-R2 clause 3 pins the uncommitted build copy | `R42-R2.1` (closed: `test -f plans/scratch_guard.py && … --selftest`) + `R42-R2.2` (open: registry visibility) | `.ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py` is now **tracked** and byte-identical to the landed tool (`sha256sum` both → `f0360e3028c79ce32fca…`), so D2's "unpassable in a clean clone" half no longer holds; the surviving half is exactly `R42-R2.1`'s check |
| `R42-R3-28` | D5 — no SKILL.md registry row for the guard | `R42-R2.2` (`check: grep -qs 'scratch-root-guard' SKILL.md`, still red) | exact duplicate; two ids for one defect |

`R42-R3-26` (D3, `check` exit 1 not 2) and `R42-R3-27` (D4, no unreadable-sentinel selftest case) are **kept**: they are
per-defect and red. The sibling's `R42-R6` merges D3+D4 into one row with a selftest-case check; keeping both pairs is
redundant, so the L1 should keep one pair or the other (my two, or `R42-R6`) — not all three.

## B. Two drafted rows whose finding is refuted (no correction is due)

Both were re-measured by this seat at `d33350f`; in each case the wave-2 reviewer was off by one line and the document it
attacked is already exact.

| drafted row | source | refutation |
|---|---|---|
| `R42-R3-14` | `F42RevLesson.md:134` (D5: cite `:326`) | `plans/round42_c2_verify.py:325-328` is `checks = [("V1"…)` / `("V4"…)` / `("V7", "V8", ("V9", lambda: v9(lane))]` / `defects = 0`. `:327` **is** the `V9` tuple, so the lesson's "R3 cites `:327`" is exact. |
| `R42-R3-16` | `F42RevLesson.md:142` (D7: cite `:10-11`) | `corpus/evidence/round42/tb2-circuit-fibsqrt/Dockerfile`: `:8` comment, `:9` `COPY tests/sim.c /app`, `:10` `COPY gates.txt /app`. The lesson's `Dockerfile:9-10` is exact. |

Both are carried in `recommended-rows.jsonl` with `check: null` and a note saying so: an open row whose demanded
correction is false would be unsatisfiable, and this seat does not claim a refusal or a close. The L1's options are a
`refused` row with the measurement as `blocker`, or dropping them. (The sibling seat `R43R42Defects` reached the same two
refutations independently — `R43R42Defects.md` §1, rows "F42RevLesson D5 / D7 → REFUTED".)
