source: S262 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/log-summary-date-ranges/tests/test.sh — `corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh:18-27`; S263 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/nginx-request-logging/tests/test.sh — `corpus/evidence/round82/fetch/nginx-request-logging_tests_test.sh:17-22`; S264 — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pyproject.toml (rejected locator, HTTP 404)
verified-at: 2026-11-04 (round-82 sweep receipt `corpus/evidence/round82/sweep.txt`, lane tip named inside it)
recheck: 2027-01-18 — re-run `python3 plans/round82_c3_sweep.py --lane . --check` (it must print `TARGET members=26 located=26 status_lines=26 histogram_total=26 mismatches=0`), then re-fetch S262/S263 at the pin and confirm the `reward.txt` branch is still the verdict; if the entry moves, re-open this entry before the next round

# Sweep at one tip: what a lane's own replay population still reproduces

Thesis: a lane that has executed 26 unrelated benchmark graders can answer one freshness question
mechanically — *which of those replays still reproduce at the current tip?* — without re-reading 26
receipts by hand. Round 82 builds that instrument (`plans/round82_c3_sweep.py`), freezes the
member→instrument map, and compares each instrument's own output to the receipt it once produced.
The census is the deliverable; no member's divergence is smoothed into a pass.

## Why the comparison is against the receipt, not against a re-run of the benchmark

A Terminal-Bench task's verdict at the pinned revision (`2fd12b88`) is produced by the task's
`tests/test.sh`: a `uvx`-pinned pytest over the task's own `tests/test_outputs.py`, whose exit status
becomes `/logs/verifier/reward.txt` (S262). Per-task entries differ only in the pytest working set
(S263), not in that rule. The lane's replay instruments model exactly that surface — they call the
captured test functions in file order and treat a normal return as pass — so a receipt's observation
block *is* the verdict surface, and comparing an instrument's current output to its own committed
block is a comparison of the same object, not a proxy.

S264 is the round's rejected locator: the pinned tree carries no `pyproject.toml` (HTTP 404), so the
harness cannot be characterised from package metadata at that revision. A rejected locator is not
evidence that no packaging exists; it only says that path does not carry it. The flip condition is a
revision that adds the file.

## The frozen projection, and why it is the round-80 A2 rule

Both sides keep only lines matching `^(CASE |case=|TEST |VECTOR |LEG |regrade )`; then `cases=`
lines, `OBSERVED-U` lines and any line whose predicted field contains `U` are dropped. That is the
projection round 81 already used for a located receipt, reused unchanged: the dropped lines are the
ones a deterministic replay cannot promise (a timing case's observed speed grade, a total that
follows from a wall-clock bound). Everything else — every case id and every observed leg — is
compared literally, so a member that changed a verdict cannot hide behind a summary line.

## What the status classes mean

| status | meaning | what it is not |
|---|---|---|
| `reproduced` | the run's exit code equals the receipt's stamped `EXIT` and the projections are equal | not a claim that the historical *numbers* of the original round still hold — a receipt may itself carry `HISTORICAL-DIVERGENCE` |
| `diverged:<n>` | `n` projection lines differ; the first three are printed verbatim in the receipt | not a failure of the instrument and not repaired in place |
| `unrunnable:<code>` | the instrument exited non-zero, timed out, or wrote no observation line | not a pass and not a skip — it is counted in the histogram and named |

A member that embeds a pid, a port or a scratch path in a graded line will diverge; that is the
finding, not a defect of the comparison. The census separates *deterministic* replay ground from
*host-state-bearing* replay ground, which no earlier round could price.

## Determinism, stated on the classification

Two runs at one tip must agree on every member's status **and** on its divergence count. Byte
identity of stdout is deliberately not claimed: instruments that print a `server_pid` or a lock path
are expected to differ there, and claiming byte identity would force either a launder of those
fields or a false red. The classification is the object a reader can check.

## What the gate refuses

- `COMMAND-MISMATCH` — a receipt `MEMBER` line whose `argv=` is not the map-derived argv with the
  work dir substituted (the round-81 reviewer's F2, made a rule).
- `NO-RUN` — a census whose statuses were copied from the ledger instead of measured.
- `PROJECTION-UNCHECKED` — a comparison of exit codes only.
- `VERIFY-MISMATCH` — a receipt line whose observation the current instrument does not emit.
- `STAGED-WRITE` — a receipt written before every member had a status line.

## Limits

The map is a frozen artifact of round 82 and names one instrument per member; a member whose
instrument is corrected later needs a new map, not a silent re-point. The sweep runs members
sequentially because three instruments contend for port 8080, so it is a slow census (minutes, not
seconds) and not a per-commit hook. And a `reproduced` verdict says the *instrument* still matches
its receipt at this tip — it does not re-open the original grader capture, which stays S260/S261's
ground.
