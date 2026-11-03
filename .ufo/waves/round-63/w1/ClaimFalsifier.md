# ClaimFalsifier — round 63 w1 findings

Full attacks, commands and outputs: `.ufo/waves/round-63/w1/attack/critic.md`. Receipts: `attack/evidence/`.

Tally: 23 attacks. Survives 16. Falsified 5. Not-run 2.

## R63-C1 (offline pypi-server grader)
- Foreign 404 listener on 8080: the probe refuses (`SETUP port-8080-occupied`, exit 2, no receipt). The K2 leg under it is confounded. Survives.
- Pre-seeded probe venv: K1 still reached the lane index (2 served requests). No bypass seen. Survives.
- `index_pid` is the PID of the server the probe started (code: `Popen`, line 482-490). The served-log guard checks the lane index's requests. Survives.
- Forged receipt through `--check-receipt` (`index_pid=1`, fake sha) passes `PREDICATE R63-C1 pass`. The checker is text-only. Falsified for the counting command.
- Repeatability: 3 of 6 non-deliberate full-battery attempts refused (two K2 "pip succeeded" aborts, one transient `port-8080-occupied`). [INFERENCE] transient foreign listener; owner not attributed. The refusal is safe (no false pass).
- Independent passes: `repeat1`, `repeat2`, `instr3` all `PREDICATE R63-C1 pass`, leg vector P/F/F/F.
- Committed receipt `corpus/evidence/round63/pypi-probe.txt`: absent. Not-run.

## R63-C2 (grader-class decision table)
- Drafted section: `ROWS n=16 class_match=True count_mismatch=0 paths total=24 resolved=24 share=1.00 / PREDICATE R63-C2 pass`. Survives.
- Count off by one: fails. All 16 rows named file-artifact: fails. Survives.
- Path cells `./` or `/` on every row: passes. Falsified (the gate accepts the lane root as a pointer).
- The `network-service` row points at `.ufo/waves/round-63/w1/build/pypi-probe.txt`, which is untracked (`git ls-files --error-unmatch` fails). Falsified for that row; repoint at the committed receipt.
- Executed column: consistent with `executed17.lst` for all 16 rows (network-service rests on the C1 branch). Survives.

## Trio gate
- Fixture expectations met: verified-at before source → fail; keys after `## ` → fail; correct file → pass.
- Gate checks presence and order only: empty values pass (falsified); keys inside a code fence pass (falsified).
- Census (red) → `TRIO fail missing=verified-at,recheck`. Survives.
- Green on `corpus/knowledge/tb2-network-service-offline-grader.md`: file absent. Not-run.

## Kill rules
- None fire on the evidence I could observe.
- C1 K2-returns-P: no recorded K2 leg returned P.
- C1 K1-returns-F: K1 returned P in every run that reached it.
- C1 foreign-service rule: condition suspected in two K2 aborts (not confirmed). The predicate did not pass in those runs.
- C2 count mismatch, resolution < 90 %, rows without a pointer: none on the drafted section.

## Notes for L1
- Frozen base hash in `plans/round-63-claims.md` has 41 hex characters. The commit resolves to `c78749a565dfd186f10a1d8ac98e19dac2429666` (40). Not edited.
- The `--check-receipt` counting command should not be cited as independent proof of a run without a live re-run.
- No tools installed. No pacman. No git mutation. Scratch removed.
