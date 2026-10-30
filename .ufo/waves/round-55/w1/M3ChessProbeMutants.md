# M3ChessProbeMutants — scoped findings (kengaku round 55, wave 1, v2 build+attack)

Seat `M3ChessProbeMutants`, 2026-10-30. Lane `kengaku-shokunin` @ `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb`;
frozen claims `plans/round-55-claims.md` read first; no predicate, counter, kill rule or target changed.
Target: `plans/round55_c3_chess_probe.py` (R55-C3, coverage attempt) — **scratch copies only**.

**Verdict: the probe is sound on all three mandated mutants — one mutant killed, one null confirmed,
one survives on the frozen table and yields a coverage finding (the mismatch leg is real but the
committed battery never exercises it).**

## Mutants (all on scratch copies; pristine file sha256 `7bd2863c…d60`, lane file unchanged)

| id | mutation | observed output | verdict |
|---|---|---|---|
| M1 | verdict mapping inverted (P↔F) in `run_in_sandbox` | `mismatches=12`, `PREDICATE R55-C3 fail`, exit **1**; all 12 case lines flip, `rc` values unchanged | **KILLED** — receipt flips to `mismatches>0` / PREDICATE fail exactly as the kill rule requires |
| M2 | mismatch counter increment deleted in `run_battery` | on the frozen table: receipt **byte-identical** to baseline (sha `de082669…`), exit 0, `mismatches=0`, PREDICATE pass | **SURVIVES on the frozen table** — see finding |
| M2b (control) | one frozen prediction mispredicted (F→P), counter intact | `mismatches=1`, `PREDICATE R55-C3 fail`, exit **1** | negative control that arms the counter |
| M2c | same misprediction + counter deleted | `mismatches=0`, `PREDICATE R55-C3 pass`, exit **0** | counter is **load-bearing**: deleting it turns fail→pass |
| M3 | null mutant: `for … in CASES` → `reversed(CASES)` | summary `cases=12 observed_pass=5 observed_fail=7 mismatches=0` and `PREDICATE R55-C3 pass` **identical**; sorted case-line sets identical; only line *order* differs | **NULL CONFIRMED** — summary order-insensitive, no order-dependent state |

Auxiliary probes (all fail closed, exit 2, distinct SETUP output): broken `BWRAP` path; zeroed
`GRADER_SHA256` pin (`SETUP grader sha256 a540714e… != frozen pin 0000…`); `timeout=0`
(`timeout after 0s`); duplicate-token case body → `mismatches=1`, PREDICATE fail, exit 1 (the
grader's full-multiset semantics are genuinely exercised).

**Baseline:** pristine run → exit 0, `cases=12 observed_pass=5 observed_fail=7 mismatches=0`,
`PREDICATE R55-C3 pass`; two runs byte-identical; and the pristine receipt is byte-identical to the
lane's `corpus/evidence/round55/chess-best-move-probe.txt` (sha256 `de082669…8aaca`) — the probe
reproduces the round's committed evidence exactly. Wall 0.40 s, MAXRSS 20.5 MB.

## Defects found (reported, not fixed — not this seat's files)

1. **Coverage finding: the mismatch leg is unexercised by the frozen case table.** Every one of the
   12 frozen predictions is correct, so the committed `mismatches=0` receipt is byte-identical
   whether the counter runs or is deleted. The counter is real (M2b→M2c: `mismatches=1 /
   PREDICATE fail / exit 1` → `mismatches=0 / PREDICATE pass / exit 0`), but only my scratch
   negative control proves it; the case lines alone do **not** expose its absence (M2c still prints
   `CASE single-move-only predicted=P observed=F rc=1` while the summary says `mismatches=0`). The
   round's kill rule (a) is therefore not exercised by the shipped battery, and the summary counter
   is the only guard against a false `PREDICATE R55-C3 pass`. Closing this needs amendment data
   (a deliberately mispredicted case or a negative-control case) — the L1's call.
2. **Receipt bytes are order-sensitive; the summary is order-insensitive.** M3 leaves the summary and
   predicate identical but reorders the `CASE …` lines, changing the receipt's sha256. The
   round's after-predicate quotes the summary form (consistent), but a byte-hash pin on the receipt
   is brittle under a case-table reordering.
3. **Pin-resolution note (upstream identity):** the pin `2fd12b88…66d6` is a commit in
   `harbor-framework/terminal-bench-2`; it 404/422s in `laude-institute/terminal-bench`,
   `terminal-bench/terminal-bench` and `-terminal-bench-datasets`. Re-verifiers must use the
   harbor-framework repo (named in the lane's own `corpus/evidence/round53/pin-tree-2fd12b88.json`).

## Independent upstream re-verification (read-only GETs, no auth/POST)

- `harbor-framework/terminal-bench-2` @ pin: tree HTTP 200, 1446 entries, `truncated:false`;
  `chess-best-move/tests/test_outputs.py` blob `6ec2300a…0a75` (971 B); raw sha256
  `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` — byte-identical to the lane
  capture and to the probe's frozen pin. `laude-institute/terminal-bench@main` yields the same
  sha256 (file unchanged since the pin).
- Upstream assertion read directly: `assert sorted(move) == sorted(["g2g4", "e2e4"]), "File is wrong"`
  → the oracle derives only from the captured grader's own assertion (kill rule (b)).
- A1 amendment verified: upstream `chess-best-move/tests/test.sh` @ pin = `4770437e…6c334` = the lane's
  captured chess-best-move `test.sh` = `round52/graders/regex-log/tests/test.sh` = S109's file → dropping
  the third SOURCES row is correct (no duplicate ground).

Full record with every diff and hash: `.ufo/waves/round-55/w1/M3ChessProbeMutants/mutants.md`;
receipts, diffs and SHA256SUMS: `.ufo/waves/round-55/w1/M3ChessProbeMutants/receipts/`.

## Hygiene

Scratch root `/fast/scratch/hyaku/kengaku-r55/M3ChessProbeMutants/` created, used, receipts copied
into the seat output dir, then deleted. Lane read-only: `plans/round55_c3_chess_probe.py` sha256
`7bd2863c…d60` identical before and after, `git status` unchanged (`??`). No mutating git/jj command;
no fleet-root tracked file written; no tool installed.
