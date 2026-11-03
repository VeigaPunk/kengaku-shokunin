# Terminal-Bench 2.0 `cancel-async-tasks` — the corpus's first signal-propagated cancellation-semantics grader

source: S224 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/cancel-async-tasks/tests/test_outputs.py — the executed scoring predicate (six legs: run.py existence, two-tasks-concurrent inside a 5 s window, a serialized elapsed >= 6 s bound, three SIGINT cancellation legs counting started/cleanup markers in captured stdout)
source: S225 — https://encoding.spec.whatwg.org/index-windows-1252.txt — the encoding index grounding this round's SECOND claim (R61-C2, the round-60 mirror byte-fidelity correction); listed here because the round's lesson binds both rows

## The class, worded narrowly

The decisive legs spawn the candidate as a child process, deliver SIGINT to it mid-flight
(`time.sleep(0.5)`, then `proc.send_signal(signal.SIGINT)` — capture :92-93/:125-126/:161-162),
and price its shutdown discipline by counting lines in the captured stdout: the three cancel
legs require exactly two `Task started.` markers (:102/:135/:171) and exactly two
`Cleaned up.` markers (:103/:136/:172) within a `communicate(timeout=5)` window
(:96/:129/:165). The non-signal legs bound the happy path from both sides: two 3 s tasks
must finish inside `timeout=5` (:28) — concurrency is measured by the clock, not by thread
inspection — while `--max-concurrent 1` must serialize them so the wall-clock elapsed is
`>= 6` (:68, measured around the child with `time.monotonic`). This is the corpus's first
**signal-propagated cancellation-semantics gate**: no executed grader sends a signal to the
candidate process (the sixteen executed graders assert on files, tool output, timing walls,
numeric bands, crypto credentials or filesystem metadata; a grep of all 184 round-52
captures names exactly this grader for `send_signal`). The grader's own docstrings name the
two implementation traps it was built around: a ThreadPoolExecutor that does not propagate
cancellation (:75) and the asyncio.gather queued-task trap (:144-145).

## Probe findings (honest: the first run failed on four author defects; the corrected re-freeze ran 72/72)

The instrument (`plans/round61_c1_cancel_probe.py`, the r58/r59 sandbox shape: bwrap
`--unshare-all`, /usr+/etc ro, /app writable, probe-owned `python` shim at /stub; capture
byte-pinned at /tests; the task's reference `test.py` simulator is NOT in the capture
population — the round-52 program took `tests/test_outputs.py` + `tests/test.sh` per task,
so the builder writes a lane-authored simulator per declared case) ran its 12-case × 6-leg
battery TWICE. The first run (receipt of record
`.ufo/waves/round-61/recon/c1-first-run-FAIL.txt`, at `b9920576`, instrument
`7d448487…f9f59`) failed 2 cases on author defects — the simulator never read the declared
`handler` property and `premature_start` double-printed its marker — and the author's own
pre-run review caught two more (the model's asyncio else-branch never checked `handler`
either; one hand-transcribed freeze-table row). All four are dated in
`plans/round-61-claims.md` Amendment 1 and mined in `corpus/lessons/round-61.md`. The
corrected re-freeze (Amendment 1, instrument `92facdc7…fe7f87`) ran the second receipt of
record (`corpus/evidence/round61/cancel-async-probe.txt`, at `0e62b479`): `cases=12
legs=72 mismatches=0 setup=0 predicted_u=0`, `PREDICATE R61-C1 pass`, exit 0 —
DETERMINISTIC, zero U marks, full commitment (every cell is a fixed function of the
declared candidate behavior plus the capture's fixed timing constants).

Confirmed structure, from the 72 confirmed legs:

- The **compliant shape** is narrow: install a loop-level SIGINT handler that cancels the
  running tasks (their `finally` blocks print the cleanup marker), cancel queued tasks
  before they ever start, and exit — every leg passes (case `compliant-signal-handler`).
- The **above-max leg is the sharp one**: exactly two started + two cleaned markers out of
  `--n-tasks 3 --max-concurrent 2` fails for a premature started marker (an accounting
  wart prints three), for an unenforced or SIG_IGN-swallowed third task, for a
  partial-cancel handler, and for the ThreadPoolExecutor's uncancelled queued work — five
  distinct defects, one leg.
- **The capture's own ThreadPoolExecutor warning is only half-visible to the grader**
  (class observation 1): after SIGINT the pool's non-daemon workers survive and run
  UNcancelled to completion, so the n=2 cancel legs see started=2/cleaned=2 inside the 5 s
  window and PASS — the counts cannot distinguish cancellation from an ignored signal
  whose work happens to finish in time. The defect surfaces only at above-max (the queued
  third task starts and blows the window). The docstring names the trap; the assertion
  prices it only in one of three cancel legs.
- **SIG_IGN is indistinguishable from success at n=2** (class observation 2, same
  mechanism as observation 1): a candidate that swallows SIGINT passes both n=2 cancel
  legs whenever the work fits the window, and fails only above-max on the window. A
  grader that wanted to price "the signal was honored" would need either work longer than
  the communicate window or an observable cancellation side effect (exit code, timing).
- **Threads and asyncio fail differently under the same neglect** (class observation 3):
  with NO handler, an asyncio candidate's pending tasks die with the loop (zero cleanup
  markers — the raw KeyboardInterrupt kills `run_until_complete` and `loop.close()`
  destroys pending tasks), while a ThreadPoolExecutor candidate's OS threads survive and
  complete, printing their cleanup markers late. Same missing-handler defect, two
  different visible signatures — the class prices engine-specific signal semantics, not
  just "did cleanup run".

Round-61 verified-at: `corpus/evidence/round61/cancel-async-probe.txt` (probe
`plans/round61_c1_cancel_probe.py --lane .`, cases=12 legs=72 mismatches=0 setup=0
predicted_u=0, PREDICATE R61-C1 pass, exit 0, at tip `0e62b479`; the first run's fail
receipt and the four dated defects are part of this entry's record, not errata to it).

recheck: 180d — from the lane root re-run `python3 plans/round61_c1_cancel_probe.py
--lane . --work <scratch>` and compare the CASE lines with the receipt (any drift is a
mismatch line); re-open S224 at the pin if the receipt's capture sha refuses.

## Sources

S224 (the grader, tier A code, opened live 2026-11-02 at the pin, byte-identical to the
round-52 population capture `corpus/evidence/round52/graders/cancel-async-tasks/tests/test_outputs.py`,
sha256 `d6f510b5…60ee7`); S225 (the WHATWG windows-1252 index, tier A docs, opened live
2026-11-02) grounds the round's other claim, not this grader.

## Freshness addendum (round 64)
verified-at: 2026-11-03 (observed 2026-11-03T19:13:08Z (round-64 freshness sweep; clean shared clone at 859ac24f4106))
recheck: sha256sum plans/round61_c1_cancel_probe.py corpus/evidence/round52/graders/cancel-async-tasks/tests/test_outputs.py; grep -c 'PREDICATE R61-C1 pass' corpus/evidence/round61/cancel-async-probe.txt
result: instrument plans/round61_c1_cancel_probe.py sha256=92facdc762bdb29c581eb92b5951f0855bec0de7dc56c8d2308136c889fe7f87 (matches the entry's 92facdc7…fe7f87); pinned grader capture cancel-async-tasks/tests/test_outputs.py sha256=d6f510b5…4de460ee7 (= SHA256SUMS row); 'PREDICATE R61-C1 pass' occurrences=1
