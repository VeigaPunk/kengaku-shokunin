# ReceiptMutate -- R67-C2 strict-gate mutation corpus (round 67, w1)

Seat: mutation tester. Scope: build the mutation corpus and runner for the R67-C2
`--strict` gate. No lane file edited; the strict mode was never run (built by another
seat, does not exist yet); no tool installed; no network used; no port lock taken
(`--check-receipt` runs no grader and opens no listener).

## Verdicts

| item | verdict | evidence |
|---|---|---|
| corpus built from committed bytes | PASS -- 9 mutants, each exactly one line changed; `base.txt`/`fab.txt` byte-identical to the committed receipt/fixture (`cmp` rc 0) | `ReceiptMutate/base.txt` sha `25c7cab7...`, `ReceiptMutate/fab.txt` sha `17436b58...`, `fixtures/`, `syntax-check.txt`, `default-mode-matrix.txt` |
| expectation table | PASS -- 11 rows (base 0, fab 1, nine mutants 1), tab-separated; fixture paths relative to the table's own directory (`../base.txt`, `../fab.txt`, `m-s*.txt`) | `ReceiptMutate/fixtures/expected.tsv` |
| runner | PASS -- `sh -n` and `bash --posix -n` rc 0; control flow exercised with a labelled non-strict stub: faithful 11/11 rc 0, survivor 10 mismatches rc 1, traceback-rc-1 row caught, missing checker rc 2, cwd-independent | `run_strict_fixtures.sh`, `selftest/` |
| calibration: does the corpus have teeth | PASS -- 5 of 9 mutants (s1-1, s1-2, s4-1, s5-1, s5-2) are accepted by the committed default mode (rc 0), so a strict mode that only forwards `receipt_failures()` cannot pass | `default-mode-matrix.txt` |
| defect reproduced | PASS -- the committed default checker still prints `CHECK ok cases=5` / `PREDICATE R65-C1 pass` / rc 0 on the byte-identical `fab.txt` copy | `default-mode-matrix.txt` |
| strict gate itself | NOT RUN -- by assignment; fixture expectation is recorded, not observed | -- |

## Fixture map (expected strict: rc 1 + `CHECK defect` naming the clause)

    m-s1-1  s1  instrument header line deleted
    m-s1-2  s1  version token r65-c1/1 -> r65-c1/9
    m-s2-1  s2  GRADER sha -> 64 zeros
    m-s3-1  s3  AMALG sha -> 64 zeros
    m-s4-1  s4  TOOLCHAIN gcc=16.2.1 -> 15.0.0 (CC line unchanged)
    m-s5-1  s5  RUN G2 rc=0 -> rc=1
    m-s5-2  s5  RUN G4 driver -> "fabricated - nothing ran"
    m-s5-3  s5  NOBIND G3 per-case line deleted
    m-s6-1  s6  VECTOR G3=P/P/F -> P/P/P
    base.txt rc 0 ; fab.txt rc 1 (violates s1, s4, s5)

Default-mode observed rc: base 0, fab 0, s1-1 0, s1-2 0, s2-1 1, s3-1 1, s4-1 0,
s5-1 0, s5-2 0, s5-3 1, s6-1 1.

## Lead action after the proposal lands

    sh .ufo/waves/round-67/w1/ReceiptMutate/run_strict_fixtures.sh <strict-capable-checker-path>

Expect `RESULT fixtures=11 mismatches=0`, rc 0. A survivor reported by this corpus is a
coverage finding; the fixtures are not narrowed to make a gate pass.

## Commands run (exit codes as observed)

    $ mkdir -p .ufo/waves/round-67/w1/ReceiptMutate/{fixtures,selftest} /fast/scratch/hyaku/kengaku-r67/ReceiptMutate
      $ cp <r65 receipt> S/base.txt; cp <r66 fabricated> S/fab.txt; cp both to seat dir          rc 0
      $ sha256sum base fab + committed originals (four identical pairs; mtimes differ, bytes equal)  rc 0
    $ python3 ReceiptMutate/gen_fixtures.py /fast/scratch/hyaku/kengaku-r67/ReceiptMutate/base.txt ReceiptMutate/fixtures
      -> GENERATOR ok mutants=9                                                                  rc 0
    $ diff -u base fixtures/m-*.txt | grep -c '^[<>]'
      -> 1 or 2 per file (one removed line, zero or one added)                                    rc 0
    $ sh -n run_strict_fixtures.sh ; sh -n <abs> ; bash --posix -n <abs>                          rc 0 0 0, no output
    $ STUB_MODE=faithful sh run_strict_fixtures.sh selftest/stub_checker.py
      -> RESULT fixtures=11 mismatches=0                                                         rc 0
    $ cd / && STUB_MODE=faithful sh <abs>/run_strict_fixtures.sh <abs>/selftest/stub_checker.py
      -> RESULT fixtures=11 mismatches=0                                                         rc 0
    $ STUB_MODE=survivor ...  -> RESULT fixtures=11 mismatches=10                                rc 1
    $ STUB_MODE=crash ...     -> RESULT fixtures=11 mismatches=1 (traceback row only)            rc 1
    $ sh run_strict_fixtures.sh does-not-exist.py  -> SETUP checker-missing                      rc 2
    $ python3 plans/round65_c1_sqlite_probe.py --check-receipt <each of 11 fixtures>             rc 0/1 matrix
    $ cmp ReceiptMutate/base.txt corpus/evidence/round65/sqlite-gcov-probe.txt                   rc 0
    $ cmp ReceiptMutate/fab.txt  corpus/evidence/round66/red/fabricated-r65.txt                  rc 0
    $ rm -rf -- /fast/scratch/hyaku/kengaku-r67/ReceiptMutate   (scratch reaped; receipts already in seat dir)

## Findings the lead must weigh (not edits to the claim)

1. s5's literal "every `NOBIND` line carries `delta=0`" is not satisfiable by the committed
   receipt read as a universal over all `NOBIND` lines: `NOBIND before-battery` /
   `NOBIND after-battery` carry no `delta` field. The only reading that keeps kill rule (b)
   is per-case `NOBIND` lines (G1-G5), which is what `m-s5-3` exercises and what the default
   mode already requires. If the proposal's strict mode implements the literal universal it
   will refuse `base.txt` and the corpus will fail on the base row.
2. Strict naming for `m-s2-1`, `m-s3-1`, `m-s5-3`, `m-s6-1` must not be only the default-mode
   text (`CHECK fail ...`): those four are already refused without `--strict`, and the run
   must still show a `CHECK defect:` line attributed to s2/s3/s5/s6. The runner gates on rc
   plus the `CHECK defect` substring and prints the checker output, so the attribution is
   visible in the transcript.
3. Five mutants are strict-only. If the strict build is a thin wrapper over
   `receipt_failures()` plus exit-code changes, those five survive and the wave must report
   a coverage miss rather than widen the corpus.

## Environment limitation

`dash`, `busybox`, `mksh`, `ksh`, `zsh` are not installed; pacman is paused host-wide and no
download channel outside the two named hosts is permitted, so no second POSIX shell was
installed. Portability was checked with `sh -n` (sh = bash 5.x here) and `bash --posix -n`;
the script uses no bash-only construct. Named as a limitation, not claimed as a dash run.
