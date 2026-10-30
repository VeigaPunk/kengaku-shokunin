# E6ChessReceipt — R55-C3 probe receipt (round 55, wave 1)

## Outcome
GREEN. Receipt landed; both runs byte-identical; acceptance line met.

Summary line (both runs): `cases=12 observed_pass=5 observed_fail=7 mismatches=0`, `PREDICATE R55-C3 pass`. P+F = 12.

## Setup
- Probe script `plans/round55_c3_chess_probe.py` was absent at start. Polled every 60 s (bounded to 25 min, one background poll). It appeared after ~6 minutes; no SETUP-absent condition.
- The script is **untracked** in the lane working tree (`?? plans/round55_c3_chess_probe.py`), not committed at tip `80afa613`. The clean clone therefore does not contain it. I copied the lane-working-tree file into my scratch clone (sha256 `7bd2863c…2d60`, identical to the lane copy). No commit or git mutation was made in the lane.
- Clone: `git clone --shared` of the lane into scratch; HEAD `80afa61314fa1bd7baa38f9afbeedb4dd0aa81eb` (current lane tip), clean status apart from the copied probe.

## Commands and exit codes
1. `command -v bwrap; ls -la /usr/bin/bwrap` → `/usr/bin/bwrap` present (root-owned, 84464 bytes).
2. `python3 plans/round55_c3_chess_probe.py --lane <clone> --receipt <scratch>/run1.txt` → exit 0.
3. Same command with `run2.txt` → exit 0.
4. `cmp run1.txt run2.txt` → exit 0 (identical). Both 694 bytes, sha256 `de082669…8aaca`.
5. Leak grep on run1 for dates, `T hh:`, `/fast/`, `/home/`, `/tmp` → no matches (grep exit 1).
6. `sha256sum` of upstream grader at `corpus/evidence/round52/graders/chess-best-move/tests/test_outputs.py` → `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286`, matching the frozen pin.
7. Landed `run1.txt` at `corpus/evidence/round55/chess-best-move-probe.txt`; `cmp` against the scratch run1 → identical.

## Per-case result (observed = predicted for all 12; mismatches=0)
| case | pred/obs | rc |
|---|---|---|
| both-lowercase-two-lines | P | 0 |
| both-space-separated | P | 0 |
| reversed-order | P | 0 |
| single-move-only | F | 1 |
| uppercase-white | F | 1 |
| extra-decoy-move | F | 1 |
| duplicate-move | F | 1 |
| whitespace-padded | P | 0 |
| empty-file | F | 1 |
| crlf-line-endings | P | 0 |
| instruction-example-h1h8 | F | 1 |
| fullwidth-unicode-digit | F | 1 |

The probe's own grader-identity check did not fail (no SETUP line), consistent with the sha match above.

## Files written
- `corpus/evidence/round55/chess-best-move-probe.txt` (run1 bytes)
- `.ufo/waves/round-55/w1/E6ChessReceipt/run1.txt`, `run2.txt`, `cmp.txt`, `report.md`
- `.ufo/waves/round-55/w1/E6ChessReceipt.md` (Report trailer path)

## Notes / defects
- Defect (lane hygiene, not fixed by me): `plans/round55_c3_chess_probe.py` is untracked at the frozen tip. The integrator must commit it before the clean-clone re-verification, or a fresh clone will lack the instrument. Its predecessor claim-table references it as a Report path, so the L1 should confirm it is included in the landing commit.
- stdout and the `--receipt` file were compared by eye, not captured separately; the receipt file (`run1.txt`) is the landed artefact.
- Not run: the probe's `--selftest` mode (not in my assignment).

## Dead ends
- None beyond the initial missing-script wait.

## Installs
- None. No tools installed or upgraded.

## Scratch
- `/fast/scratch/hyaku/kengaku-r55/E6ChessReceipt/` removed after copying receipts.
