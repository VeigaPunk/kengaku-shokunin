# F35ReportEvidence — evidence table for round 35 wave 2 (falsify)

Seat: F35ReportEvidence (scribe). Task: draft the evidence table for the round report — before
receipts, after command outputs at tip, commit hashes, census before/after, and the wave-1 seat
ledger. Full table: `Report` artifact `.ufo/waves/round-35/falsify/F35ReportEvidence/table.md`
(16 data rows across four tables).

## What was verified (every number carries its command)

### 1. Claim predicates: before vs after
- C1 (coverage): frozen predicate `python3 plans/round35_c1_verify.py --lane .` →
  `checks=6 defects=0`, `PREDICATE C1 pass`, exit 0.
  - Before (freeze): `claims/control-c1-nothing.txt` → `checks=6 defects=5`, `PREDICATE C1 fail`, `exit=1` (V1–V5 DEFECT, V6 ok).
  - After @ `dfee6fff` (ran read-only in lane): `V1 ok … V6 ok`, `checks=6 defects=0`, `PREDICATE C1 pass`, `exit=0`.
- C2 (calibration): frozen predicate `python3 plans/defect_ledger.py --lane .` →
  `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, exit 0.
  - Before: `claims/control-c2-nothing.txt` → `rows=5 closed=0 observed_pass=0 mismatches=0`, `PREDICATE C2 fail`, `exit=1`.
  - After (ran read-only in lane): `rows=5 closed=5 observed_pass=5 mismatches=0`, `PREDICATE C2 pass`, `exit=0` (D1–D5 all closed/observed=pass/agree=yes; D1 untracked=0, D2 committed_mirror_paths=0, D3 listed=6, D4 correction_lines=1, D5 erratum_lines=1 r35_mistake_row=True).
- Skip/flip controls quoted from frozen receipts (`claims/control-c1-skip.txt`: `checks=6 defects=5` fail; `claims/control-c2-flip.txt`: `rows=5 closed=5 observed_pass=1 mismatches=4` fail); not rerun — they are counterexample fixtures, not the landed state.
- Counters confirmed read-only: no write ops (open w/a/r+, write_text, unlink, rmtree, os.remove, mkdir) in either script.

### 2. Commits baseline → tip
`git -C <lane> log --format='%H %s' 58a19f37..dfee6fff631ebc5f623ba4506e5c7992a215401c` → 7 commits:
`5d0c73d` (round-34 verifier spot-check), `11d64530` (freeze), `dfcd294c` (C2 close D1–D5),
`4fe72a9` (C1 admit), `6ac9611a` (SCORECARD + LOG), `056e192a` (lesson Gate + census receipts),
`dfee6fff` (wave-1 evidence). HEAD at run time = `dfee6fff` (verified `git rev-parse HEAD`).

### 3. Census before/after
Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku`.
Before (`claims/census-before.txt`) and after both exit 0 with the same 15 W04 warnings + `kengaku ok`;
after stdout is byte-identical to the before file's stdout (`diff` clean; the before file additionally
carries the runner-appended `exit=0` line). Census state unchanged freeze → tip (rows S040/S048/S057/S058/S059/S064/S065/S066/S067/S068/S069/S071/S075/S076/S100).

### 4. Wave-1 seat ledger (`build-results.json`)
- Seat count: 32 (`d["seats"]`=32, `len(d["results"])`=32; dispatch registry also 32 members).
- Role histogram (`agent` field): executor 10, scribe 6, scout 4, critic 3, mutation-tester 3, reviewer 3, connector 2, simplifier 1 (sum 32).
- Dead seats: 0 of 32 — 32/32 ledger seats have a committed report under `build/<seat>.md` (names match 1:1) and all 32 reports end with a `VERDICT:` line (`grep -l "VERDICT" build/*.md` → 32). No seat-level error text exists in the ledger; all 32 records carry `output: null` with one shared note (verbatim): "orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but not retained — read the seat report file in the wave dir".

## Limits
- The ledger stores no per-seat result payloads or error strings; dead-seat determination relies on report presence + VERDICT completion (0 dead). The shared kernel-restart note is quoted in the table.
- Skip/flip controls are quoted from freeze receipts, not rerun (they are counterexample fixtures).
- Counters ran before this scribe's writes; D1's `untracked=0` reflects the round-34-scoped check, consistent with the lesson (`corpus/lessons/round-35.md`) and `R35ConsiderMine.md`.

VERDICT: evidence-table-16-rows
