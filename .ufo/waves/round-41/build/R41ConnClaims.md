# R41ConnClaims — cross-document consistency (connector, wave 1)

Scope: plans/round-41-claims.md (full read), C1/C2 counter docstrings, `.ufo/waves/round-41/claims/*`, `.ufo/waves/round-41/first-run/`, lane git history, spec, dry table, receipt, captures, round-40 pilot and spot-check §5.

## Method
Read every named artifact in full; cross-checked every number/hash against `git -C <lane> log` and recomputed digests/counts. Read-only; nothing modified.

## Commit graph (git log)
- Freeze commit `8ef8b4fc7c6302c527db90244d69aa18f53e83bf` exists; parent = baseline tip `e50c134556b4ba48e29dc7ff364e90d6ef07a3f3` (claims.md:3 ✓). Contains 33 files: claims, counters, probe, spec, dry table, captures (10 + SHA256SUMS), controls, witnesses, s10_equivalence files (git show --stat 8ef8b4f).
- Receipt commit `f774a87ad071122acd39ba02a9901b5b56d9910a` exists; parent = freeze (order gate: `python3 plans/order_check.py --lane . --claims plans/round-41-claims.md --receipt corpus/evidence/round41/constraints-probe.txt` → `ORDER RESULT PASS`, exit 0; freeze=`8ef8b4f…` receipt_commit=`f774a87…`). Adds only `corpus/evidence/round41/constraints-probe.txt` + `.ufo/waves/round-41/first-run/first-run-exit.txt`.
- Baseline tip e50c134 = round-40 verifier spot-check ✓; `ec17216844585d0fecde9f1d4c4be0b78a3bf76f` exists (tip_receipts landed round-40, claims.md:29 ✓ — `git log -- plans/tip_receipts.py` last touch ec17216, sources_adopt last touch d6aa66e round-31, both unedited this round ✓).

## Hashes — frozen-digests vs live bytes (sha256sum, all 11 match)
claims.md `3b239b50…`, C1 `8835a94b…`, C2 `cf1632b5…`, probe `8c471fbd…`, spec `8e96421d…`, dry table `a656ce9b…`, SHA256SUMS `9aafc9a0…`, tip_receipts `e4f49714…`, sources_adopt `38492bf1…`, pkg_gate `ea638822…`, order_check `948d5e1d…` — all equal frozen-digests.txt and the counter-embedded pins (C1 PINS; C2 SPEC/GATE/PROBE/DRY constants).

## C1 numbers
- MUTANTS table (round41_c1_verify.py:128–233): T01–T13 (13) + S01–S09, S11 (10) = 23; `TOTAL=23`, `FLOORS={receipts:13,sources:10}`; no S10 (withdrawn, `s10_equivalence.txt` `ref_rc=5 mut_rc=5` ✓, file+py committed at freeze).
- adv_kind: T06 and S11 indirect, remaining 21 direct, 0 none → ADVERTISED `direct=21 indirect=2 none=0` in every control + witness-run ✓ (claims.md:36–38).
- Directions: silence×4 (T09–T12), rc-silence×2 (T03,T06), rc-mirror×3 (T04,T08,T13), error×4 (T01,T02,T05,T07); sources exact pairs 2>0×4, 2>1×2, 2>5, 2>9, 3>0, 5>0 → the six distinct pairs named at claims.md:44 ✓.
- Silence class fixed paths: T09 `skip:corpus/evidence/r/foo-probe.txt:no-committed-re-run-command`, T10 `map:corpus/evidence/r/foo-probe.txt:derived`, T11 `map:corpus/evidence/round35/tb2-grader-probe.txt:table`, T12 `skip:corpus/evidence/r/foo-probe.log:no-committed-re-run-command` ✓ (claims.md:69–72, counter table).
- Witness modules: w_receipts.py 13 fixtures (w-t02…w-t13), w_sources.py 9 (w-s01…w-s09,w-s11) = 22 ✓; witness-run.txt `BATTERY fixtures=22`, 23/23 kills, `wrong=0 tampered=0 sidechannel=0`, exit 0, PREDICATE n/a (dev mode) ✓.
- Controls: nothing → `killed=0 survived=23 receipts=0/13 sources=0/10`, exit 1 ✓; no-mutants (patch line 233a234 `MUTANTS = []`) → total=0, 22 fixtures, exit 1 ✓; witness-as-battery → pass, exit 0 ✓; tool-edited → PINS mismatched=1, receipts=0/13, invalid=13, exit 1 ✓; hostile → OSError / FileNotFoundError / sidechannel=1 (token `/home/`), no marker files, exit 1 ✓.

## C2 numbers
- Captures: 10 files + SHA256SUMS; manifest hashes equal on-disk bytes and counter CAPTURES and spec rows (test_outputs.py `1422b345…`, instruction.md `342def78…` ✓ claims.md:82–83). Capture dir mtime 15:19 matches "opened 2026-10-26 15:19 -03" ✓. Spec raw_base pins `2fd12b88aafdd04a52c298e3940bcb189f9766d6` ✓ (= TB2 pin in claims/receipt header). S122/S123 tier A, mined, opened 2026-10-26; S124 = TB2.1 PR #245 (tier B) referenced consistently (claims.md:82–83, receipt CASE decoy-first-vevent, dry table).
- Dry table: 25 CASE lines in receipt order, 11 TAG lines with line numbers verified against instruction.md (window:1, output-file/meeting-title/attendees/one-hour:10, hard-constraints/no-conflict:12, inputs-readonly:15, version-prodid:23, utc-format:25, earliest:27 ✓); `cases=25 predicted_pass=6 predicted_fail=19` ✓; tag lines: "Any modification will cause the tests to fail" at instruction.md:17–18 ✓.
- Receipt: same 25 ids in same order, `cases=25 observed_pass=6 observed_fail=19 mismatches=2`, `regrade cases=25 differ=0`, all `regrade=same` ✓; mismatch ids exactly later-valid-wed-1105 + seconds-30, carried verbatim from pilot (run1.txt `cases=16 observed_pass=3 observed_fail=13 mismatches=2`, both `match=NO` with pred E / obs C,E ✓ — first 16 cases match pilot's 16 in order and predictions).
- Second run: first-run/first-run-exit.txt (2× `exit=0` + `second run byte-equal`) ✓; stagecheck `cases=25 failed=0` with 25 STAGECHECK lines ✓.
- C2 counter V1–V8 present; V8 order gate verified live above; do-nothing control `checks=8 defects=5` (V2,V3,V4,V7,V8) and P10 `receipt unreadable` ✓ (claims.md:99–100).

## Round-40 closure §5
Spot-check §5 R1–R5 mapped 1:1 to claims.md:124–129 (R1 counter soundness, R2 host-safety envelope, R3 registry rows wave 1, R4 adv_kind split, R5 ledger-tip blocked/round40 --work traceback fixed/census W04 count) ✓.

## Result
No drift found: every number and hash agrees across claims.md, both counters, claims/*.txt, first-run/, spec, dry table, receipt, captures and git history; all frozen files byte-identical to their pinned digests.

VERDICT: drift-0
