# R40MutProbe — mutation test of the frozen C2 probe's sensitivity (round 40, wave 1)

Seat: R40MutProbe (leaf). Frozen bytes under test: `plans/db_wal_probe.py` @ `69af65dfe4e2ecab9aec534c68a0bb2b071faf845f09b9ccff4a92e213e19ff3`
(= counter pin `PROBE_SHA256`, plans/round40_c2_verify.py:57). Eight mutants, each a one-point edit of a
scratch copy; the lane file was never touched.

## 1. Setup and baseline

Scratch: `S=/fast/scratch/hyaku/kengaku-r40/R40MutProbe`, `TMPDIR=$S`, `git clone -q --shared <lane> "$S/lane"`,
`git -C "$S/lane" rev-parse --show-toplevel` → `$S/lane`. Mutant copies `$S/mut/m1..m8.py` were hashed before
editing: all eight `69af65df…` (sha256sum, §5). Scratch was deleted after the artifacts below were copied out.

Detector (bounded behavioral detector, one full grade run):

```
python3 <probe-copy> --lane "$S/lane" --work "$S/w"      # rc + stdout = the receipt
python3 <probe-copy> --lane "$S/lane" --dry              # V5's dry half
```

Baseline (pristine bytes, lane copy): `python3 "$S/lane/plans/db_wal_probe.py" --lane "$S/lane" --work "$S/w"`
→ `rc=0 elapsed=2s`, stderr empty, and
`diff "$S/rec/frozen-receipt.txt" "$S/rec/pristine-receipt.txt"` → byte-identical (35 lines, ends
`cases=28 observed_pass=8 observed_fail=20 mismatches=0`). The detector reproduces the frozen receipt
`corpus/evidence/round40/db-wal-probe.txt` exactly, so every mutant result below is conclusive (no baseline
failure). Mutant runs (loop over m1..m8, same argv): m1/m4/m6/m7/m8 `rc=0 elapsed=2-3s`; m2/m3/m5 `rc=2`.

## 2. Mutants, observed output, verdicts

Diff basis: `diff frozen-receipt m<i>.txt`. "dry" = `--dry` stdout vs the pristine `--dry` (all eight BYTE-EQUAL,
so V5's dry-table half catches none of them; `db-wal-dry-cases-freeze.txt` pins predictions, not behavior).

| id | mutation (probe file:line) | receipt | detector output | V4 | V2-P10 | V5 | verdict |
|----|----------------------------|---------|-----------------|----|--------|----|---------|
| m1 | HARNESS maps non-assert exceptions to P (db_wal_probe.py:252-253) | differs, 6 cases | `FPPPPPP` for empty-app/untouched/decrypt-in-place-no-json/truth-wrong-path, `PPPPPPP` for truth-trailing-garbage (observed=pass), `PFFPFPF` for truth-wrapped-object; `error=` class tokens gone; summary `observed_pass=9 observed_fail=19 mismatches=6` | FAILS: 6 `match=NO` unnamed in a pristine-receipt entry (round40_c2_verify.py:175-190) | catches: fresh output ≠ pristine receipt (pkg_gate.py:284) | digest only | caught |
| m2 | seeding skipped for every case (db_wal_probe.py:282) | none | `rc=2`, stderr `SETUP case oracle-solve-sh did not yield seven test verdicts twice (rc=3)` / `STAGE recipe rc=1` (solve.sh cannot run on an empty /app) | n/a — no receipt possible | catches: `fresh probe exit=2` (pkg_gate.py:282) | digest only | caught (crash) |
| m3 | seeding writes `main.db-wal.enc` (db_wal_probe.py:284) | none | `rc=2` at `xor-wrong-key`: DECRYPT cannot read `/app/main.db-wal`, same SETUP pair. Notable: `base-only-ro` and `plain-read-then-solve` still grade identically — the grader cannot tell a missing WAL from an undecryptable one | n/a — no receipt possible | catches: fresh exit=2 | digest only | caught (crash) |
| m4 | harness ignores recipe rc (db_wal_probe.py:240) | BYTE-EQUAL | all 28 frozen recipes exit 0, so dropping the rc gate changes nothing; rc=0, 35/35 lines equal | blind | blind: rerun byte-equal | digest only | **survived** |
| m5 | `/app` bound `--ro-bind` (db_wal_probe.py:268) | none | `rc=2` at `oracle-solve-sh` (solve.sh writes /app); same SETUP pair. empty-app/untouched still graded before the crash | n/a — no receipt possible | catches: fresh exit=2 | digest only | caught (crash) |
| m6 | regrade copies the first grading (`letters2 = letters`, db_wal_probe.py:366) | BYTE-EQUAL | frozen corpus has `regrade cases=28 differ=0`, so a self-comparing regrade prints the same receipt; rc=0 | blind | blind: rerun byte-equal | digest only | **survived** |
| m7 | recipes of `untouched` ↔ `oracle-solve-sh` swapped (db_wal_probe.py:170-173) | differs, 3 lines | untouched `predicted=fail observed=pass … match=NO`; oracle-solve-sh `predicted=pass observed=fail … match=NO`; summary still 8/20 but `mismatches=2` | FAILS: 2 `match=NO` unnamed | catches: output ≠ receipt | digest only | caught |
| m8 | TRUTH id 1 value 150→1500 (db_wal_probe.py:86) | differs, 11 lines | 10 cases flip to `match=NO` (e.g. truth-value-id3-wrong and truth-bool-value-id5 `observed=pass`→`fail`); summary `observed_pass=5 observed_fail=23 mismatches=10`. My static prediction (values never graded) was wrong — the run falsifies it, exactly the round-40 lesson "reachability asserted, not witnessed" | FAILS: 10 `match=NO` unnamed | catches: output ≠ receipt | digest only | caught |

Layer notes, grounded in the frozen code:
- **V2-P10** (counter v2 at round40_c2_verify.py:118-124 runs `pkg_gate.py package --rerun --require-clean-tree`;
  gate `c_rerun` at pkg_gate.py:267-285) re-runs the *lane's* probe and byte-compares to the receipt. It therefore
  catches every mutant whose output or exit differs **only while the pristine receipt is on disk**. If mutant probe
  and mutant receipt were frozen together (digest re-pinned), P10 is self-consistent and blind by construction —
  that scenario is what V4/V7 must carry.
- **V4** (round40_c2_verify.py:164-192) never compares observed letters to the frozen predictions; its only frozen
  anchors are the case-id order and the entry-naming rule for `match=NO`. The predictions themselves are protected
  by V5's dry-table pin, not by V4. The receipt's `error=<Class>` tokens are parsed by no check (m1 deletes them
  unnoticed by V4/V7).
- **V7** (label derivation) adds catches the task didn't ask about but worth recording: m1 flips truth-trailing-garbage
  to pass → `json-at-path` derives `partly` (was `enforced`); m7 flips untouched to pass → same tag drift; m8 flips
  value-id3-wrong/bool-id5/extra-field to fail → `extract-all` and `record-format` derive `enforced` (was `partly`).
  An entry written for the pristine receipt fails V7 for m1, m7, m8 even if its prose named the new mismatches.
- **V5** (round40_c2_verify.py:194-199) catches all eight trivially through the digest pin (`69af65df…` vs the eight
  post-edit hashes in §5); its behavioral half (dry byte-equality) catches none, see table header.

## 3. Answer to the task question, per mutant

"Does the receipt change, and would C2 V4/V5/V2-P10 catch it?"

- m1 exception→P: **yes** (6 cases, summary 9/19 mismatches=6); caught by V4 + P10 (+V7), V5 by digest.
- m2 seeding skipped: **no receipt** (probe exit 2); caught by P10 exit code, V5 by digest.
- m3 wrong WAL name: **no receipt** (exit 2 at xor-wrong-key); caught by P10, V5 by digest.
- m4 recipe failures ignored: **no** (byte-equal — no frozen recipe fails); V4/P10/V5-dry all blind; caught only by
  V5's file digest. Coverage finding: the docstring promise "a recipe that exits non-zero is a probe error (exit 2),
  never a verdict" (db_wal_probe.py:14-15) has no frozen witness; one counter case with a failing recipe would kill it.
- m5 /app read-only: **no receipt** (exit 2 at oracle-solve-sh); caught by P10, V5 by digest.
- m6 regrade self-compare: **no** (byte-equal — differ=0 is genuine on this corpus); V4/P10/V5-dry all blind; only
  the digest pin. Coverage finding: `regrade=same`/`differ=0` is a self-report; no frozen check can distinguish a
  second grading from a copy. The claims file's informed-filler limit covers this class, but naming it per-instrument
  here costs nothing.
- m7 recipe swap: **yes** (2 mismatches, counts unchanged 8/20); caught by V4 + P10 (+V7).
- m8 TRUTH id-1 value changed: **yes** (10 mismatches, 5/23) — statically unexpected, empirically confirmed; caught
  by V4 + P10 (+V7).

Count (behavioral catch by any of V4/V2-P10, with the rest of the package frozen): **6 of 8**; adding V5's
file-digest pin: 8 of 8. Survivors m4, m6 are reported as coverage findings, not contract changes.

## 4. Restoration evidence

- Lane probe before and after all runs: `sha256sum` → `69af65dfe4e2ecab9aec534c68a0bb2b071faf845f09b9ccff4a92e213e19ff3`
  (both `/home/…/kengaku-shokunin/plans/db_wal_probe.py` and the clone copy); lane file never edited.
- Clone working tree clean after all runs: `git -C "$S/lane" status --porcelain` → empty.
- Mutant copies lived only in scratch; post-edit digests (all ≠ frozen):
  m1 `8e0a76b737211f9e`, m2 `e6bdb19deb972d3d`, m3 `af15b366e88c1ccc`, m4 `3b179bd6361bf04b`,
  m5 `3602b6e9de2ded18`, m6 `905cbc02ca24922e`, m7 `8e6b96836afc466f`, m8 `b57bff9aa2f51f5b` (first 16 hex).
- Artifacts copied to `.ufo/waves/round-40/build/R40MutProbe/` before scratch deletion: `frozen-receipt.txt`,
  `pristine-receipt.txt`, `m1.txt`…`m8.txt` (mutant receipts / partial stdout), `m2.err`, `m3.err`, `m5.err`.
  `rm -rf -- "$S"` executed after the copy (scratch directive 2026-10-25).

## 5. Commands (evidence for every number above)

- Baseline: `python3 "$S/lane/plans/db_wal_probe.py" --lane "$S/lane" --work "$S/w"` → rc=0, 2s; `diff` vs frozen
  receipt → no output (byte-identical).
- Mutants: `for i in 1..8: python3 "$S/mut/m$i.py" --lane "$S/lane" --work "$S/w" > "$S/rec/m$i.txt" 2> "$S/rec/m$i.err"`
  → rc: m1 0, m2 2, m3 2, m4 0, m5 2, m6 0, m7 0, m8 0; `diff frozen m<i>.txt | grep -c '^[<>]'` → 14, 28, 27, 0, 28, 0, 6, 22.
- Dry: `python3 "$S/mut/m$i.py" --lane "$S/lane" --dry` diffed against pristine `--dry` → BYTE-EQUAL for all eight.
- Layer cites: plans/round40_c2_verify.py:118-124 (v2), :164-192 (v4), :194-199 (v5), :209-211 (derive);
  plans/pkg_gate.py:267-285 (c_rerun); plans/db_wal_probe.py:240, :252-253, :268, :282-284, :362, :366.

VERDICT: probe-mutants-6/8
