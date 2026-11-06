# ReviewC2 — R100-C2 correctness review (round 100, lane kengaku-shokunin)

Reviewer: ReviewC2 (leaf). Reviewed at measured tip T `dbe0cefa607cf57f7f58346fce64bcc127144ca0`
(isolated `git clone --shared` under scratch, detached at T; no lane/production mutation). Receipts:
`.ufo/waves/round-100/w1/ReviewC2/` (counter-at-T, indep-derivation, mutants, builder-repro,
live-refetch, f-rev-diff-and-shas). No tool installs were needed; none made.

Method: read the frozen claims (`plans/round-100-claims.md`, R100-C2 section), the counter
(`plans/round100_c2_rowcensus_bind.py`), the builder (`plans/round100_provenance_build.py`), the gate
(`plans/anchor_digest_check.py`), the three new PROVENANCE.md files, `c2-pop.txt`,
`c2-live-refetch.txt`, `amendment-1.txt`; then re-derived everything independently (own parser and
rule implementation, not importing the counter) and falsified two legs with mutants.

## Verdict list

- C2-R1 PASS — Independent re-derivation of the population from the BASE gate output (re-run of `plans/anchor_digest_check.py` @ BASE, bytes = `11bb2cad…`, rc 1) and the BASE tree reproduces POP exactly: 9 rows, same ids/tokens/captures, no missing or extra row — `receipts/indep-derivation.txt` (`DERIVED_POP` all OK, `SET_DIFF [] []`).
- C2-R2 PASS — Official counter at T prints `REV/REF 5220b71d (=F~1)`, `GATE defects base=33 ref=32 rev=23`, `LEGS K1..K10=pass`, the exact frozen `TARGET pop=9 cleared=9 … captures_changed=0` string, `PREDICATE R100-C2 pass`, rc 0 — `receipts/counter-at-T.txt`.
- C2-R3 PASS — Every binding is semantically right: for all 9 rows the committed capture's sha256 = the row's anchor token = a fresh HTTP-200 re-fetch of the row's pinned URL (byte counts identical to `c2-live-refetch.txt`: 2600/11386/5878/3177/2166/3034/2330/1262/24841), i.e. the bound file IS the upstream file the URL names — `receipts/live-refetch.txt`.
- C2-R4 INFO — S298 resolves cleanly: its token `7f8d9ef6…` is shared by two byte-identical BASE files (`round94/graders/write-compressor/environment/decomp.c` and `…/tests/original-decomp.c`); rule (c)'s suffix filter (c2_rowcensus_bind.py:272) admits only `…/write-compressor/tests/original-decomp.c`, the provenance line and the T gate (`BIND S298 … tests/original-decomp.c by=provenance-row`) name exactly that file — the round-99 CO-11 "wrong file's bytes" hazard is structurally excluded and moot here.
- C2-R5 INFO — S211 binds the `tb2-` directory variant (`round58/tb2-distribution-search/solution/solve.sh`), the unique BASE path matching `/(tb2-)?distribution-search/solution/solve.sh` (round52's `graders/distribution-search/` holds no `solution/solve.sh`), explicitly allowed by rule (c); live sha matches.
- C2-R6 MINOR — For S210/S219 the token matches TWO byte-identical suffix-eligible copies (round52 `graders/<task>/tests/test_outputs.py` and round58/round59 `tb2-<task>/tests/test_outputs.py`); `derive()` (c2_rowcensus_bind.py:249-281, lexicographically first) and the committed provenance lines pick the round52 copy — semantically correct either way (same upstream bytes), but the choice rests on lexicographic determinism, worth knowing if a future round binds the `tb2-` twin.
- C2-R7 PASS — The REF = F~1 amendment is sound and not a loophole: REF printed = `5220b71d` = P2 = F~1; my BASE→REF gate diff shows exactly one outside-POP delta, S295 cleared by C1's P0 capture (`BIND S295 … by=url-task` to `round100/tb2-financial-document-processor/test_outputs.py`), matching amendment 1; a C2 change cannot hide in F~1 because K10 (:466-467) requires every new PROVENANCE file to differ F..rev and hash to the frozen candidate table (mutant-verified, C2-R9), K3 (:352) byte-compares old provenance BASE..rev, K6 pins POP rows/captures, K8 pins all 333 BASE rows, K1 pins the gate bytes.
- C2-R8 PASS — K8 is genuinely row-level: every one of the 333 BASE SOURCES row lines must be byte-present at rev (:440-443); falsification mutant deleting outside row S001 (no gate output) yields `K8=fail` only, rc 1 — `receipts/mutants.txt`.
- C2-R9 PASS — K10 closes the file-set hole: mutant adding `corpus/evidence/round52/mutant-extra.txt` yields `K10=fail outside_table=[…]` only, rc 1; and the real F..T diff is exactly the 6 candidate-byte files + C1 receipt — `receipts/mutants.txt`, `receipts/f-rev-diff-and-shas.txt`.
- C2-R10 PASS — K1–K10 match the frozen text: every leg in the counter docstring maps 1:1 to the claims' R100-C2 wording (three-cells/no-URL/old-file K3, one-line/round-dir/first-path/sha-column/no-extra-id K4, BIND+RESOLVED+token-set-with-RECLASS K5, row+capture identity K6, outside census K7, receipt shape K9); all 9 frozen-instrument shas verified at T, candidate-byte shas verified at T.
- C2-R11 PASS — The frozen builder run at REF (last pre-freeze tree) reproduces the three committed PROVENANCE.md files byte-for-byte (`BUILDER==COMMITTED` for round52/58/94) — `receipts/builder-repro.txt`; the live-re-fetch receipt (12:11:48–12:11:50 -03) predates P1 12:15:45 and F 12:39:29, so "re-fetched live before the freeze" holds.
- C2-R12 MINOR — `c2-pop.txt` prints `REV fb0f125c…` (the P0 capture commit passed as `--rev`), while the derivation's gate output is always produced at BASE by construction (derive feeds `run_gate(…, BASE, …)`); the claims say "derived at BASE", so this is a cosmetic receipt-label nit only — `.ufo/waves/round-100/L1/c2-pop.txt:1`, `plans/round100_c2_rowcensus_bind.py:288-297`.
- C2-R13 MINOR — K9 (:449-455) checks http=200/sha/url/one-line-per-id but not the receipt's `bytes=` field; sha equality subsumes it, and my re-fetch reproduced the exact byte counts, so informational only.

No defect rises above MINOR; none affects the frozen predicate, which passes for the right reasons.

## S300 residuals (consistency with frozen text)

At T S300 keeps exactly its two outside findings — `fa53d657` (`abbrev-unresolved`, sharpened from
`anchor-unbound`; the prefix is `environment/main.rs`'s digest, printed as the informational `RECLASS`
line) and `3a905a56` (`token-outside-anchor`) — token set equal REF..rev, as amendment 1 and the
claims' K5 wording require. S300 enters POP only on its full `01550b7d…` solve.sh token: the
`fa53d657` path does not survive rule (c)'s suffix filter (main.rs is not `…/solution/solve.sh`).

## Residual risk / verification gaps

1. Pre-freeze bytes (BASE..F~1) sit outside C2's censuses by design; they are governed by the freeze
   contract and the frozen-instruments/candidate tables, which I verified only at T (shas) plus the
   BASE→REF S295 delta — I did not audit every pre-freeze commit.
2. K7 censuses only rows present at BASE (324 outside rows); post-BASE rows (S342–S349) are C1's
   scope and were not re-reviewed here.
3. The live re-fetch verifies the upstream bytes as of 2026-11-06; upstream drift after the freeze is
   out of scope for C2.
4. Do-nothing control (`still=9` before the change) is taken from the committed P2 receipts, not
   re-run; its logic follows from K5's `still` definition given row-path/absent bindings at REF.

Report: .ufo/waves/round-100/w1/ReviewC2.md
