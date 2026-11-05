# ExecC2Rerun — R93-C2 re-measurement and forgery extension (findings)

Measured tip T `22972a317185216596b3dfe1c189e98d1eb86787`. Full report with receipts: `ExecC2Rerun/report.md`.

Real counter at T: `PREDICATE R93-C2 pass`, W1 pass, W2 pass, W3 pass, W4 pass, `TARGET legs_passed=4 of 4`, rc 0 (`ExecC2Rerun/receipts/c2-rerun.txt`). Frozen instrument table re-verified: 9/9 sha256 match.

Committed forgeries at T (four): all rejected, rc 1 — always_broken fails W1, W2, W4; always_intact fails W1, W2 (W4 passes by construction on a clean tree); bytes_only fails W2 only; log_only fails W2 only.

New forgeries (four, `ExecC2Rerun/forgeries/x-*.py`): x-first-row-only caught (W1, W4). x-head-not-rev, x-diff-rev-minus-1, x-table-at-rev each PASS the counter 4/4 — uncaught.

FINDING F1 major — counter W2 accepts `x-diff-rev-minus-1` (rc 0, `PREDICATE R93-C2 pass`). Isolation fixture B (edit → revert → unrelated commit): honest gate rc 1 `broken:touched-after-freeze=2`, forgery rc 0 `intact`. Leg that should catch: W2 (counts-only check; no fixture past the revert commit).
Reproduce: `python3 plans/round93_c2_counter.py --lane . --rev 22972a317185216596b3dfe1c189e98d1eb86787 --work DIR --tool-file .ufo/waves/round-93/w1/ExecC2Rerun/forgeries/x-diff-rev-minus-1.py`

FINDING F2 major — counter W2 accepts `x-table-at-rev` (rc 0, `PREDICATE R93-C2 pass`). Isolation fixture C (table lied at freeze, row repaired later): honest rc 1 `broken:freeze-bytes-differ-from-table+rev-bytes-differ`, forgery rc 0 `intact`. Leg that should catch: W2 (no repaired-after-freeze fixture).
Reproduce: same command with `--tool-file .ufo/waves/round-93/w1/ExecC2Rerun/forgeries/x-table-at-rev.py`

FINDING F3 major — counter W1/W2 accept `x-head-not-rev` (rc 0, `PREDICATE R93-C2 pass`). The counter never checks that `--rev` is honoured: all W2 fixtures have `--rev` == HEAD, and W1 returns the same `intact=1 broken=3` at the tip and at T. Fixture A: honest rc 0 `intact`, forgery rc 1 `broken`. It cannot flip the real verdict at T (HEAD == T), but a HEAD-reading gate passes the counter. Leg that should catch: W2 (fixture with `--rev` earlier than HEAD).
Reproduce: same command with `--tool-file .ufo/waves/round-93/w1/ExecC2Rerun/forgeries/x-head-not-rev.py`

FINDING F4 minor — counter W3 (lines 156–159): the comment says the battery line is taken from the W1 run, but `out` is rebound by the W2 loop, so W3 reads the `w2-unrelated` output. No verdict flip; comment is wrong.

FINDING F5 info — row-count regressions are caught only by W1 and W4 (W2 fixtures have one row each).

FINDING F6 info — W4 detects only always_broken among the committed forgeries; it is a self-consistency check on this round's clean table, not a forgery detector.

Routed to round 94 per the frozen rule; no instrument was repaired in round. No tools installed. Lane untouched (HEAD still T, clean).
