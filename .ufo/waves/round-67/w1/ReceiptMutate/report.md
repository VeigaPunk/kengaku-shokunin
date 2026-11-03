# ReceiptMutate -- R67-C2 strict-gate mutation corpus

Seat: `ReceiptMutate`, round 67 wave 1. Scope: build the mutation corpus and the runner
for the R67-C2 `--strict` gate. No lane file was edited. The strict mode itself was **not
run**: it is built by another seat and does not exist yet. The committed
`plans/round65_c1_sqlite_probe.py` was used read-only, in its frozen default mode, to
record what the gate must add.

Frozen source of the clauses: `plans/round-67-claims.md` R67-C2 (s1-s6, line beginning
`Strict-mode clauses (frozen`). Both seed files are byte-identical to the committed
artifacts (`cmp` rc 0):

| seed | committed source | sha256 |
|---|---|---|
| `base.txt` | `corpus/evidence/round65/sqlite-gcov-probe.txt` | `25c7cab7da00c44b32ab2a939ca9b1626dc0539e870ce9759654bea1535b3ba0` |
| `fab.txt` | `corpus/evidence/round66/red/fabricated-r65.txt` | `17436b58893d046d9a8c0c0cc7a389c27287df135666c44755c2b61b22d5a296` |

## Corpus

Every mutant is derived from `base.txt` by exactly one change. `gen_fixtures.py` asserts
the anchor occurs once, that the byte-length delta is the declared one, and that a
`difflib` opcode diff has exactly one non-equal opcode removing one line and adding at
most one line. `diff -u base <mutant>` was run independently over all nine files and shows
one removed and zero or one added line per file (`default-mode-matrix.txt` records the
same corpus through the committed checker).

Expected strict verdict for every mutant: **exit 1** with at least one `CHECK defect:`
finding naming the clause below.

| fixture | clause | single change from `base.txt` | expected strict | committed default mode (observed) |
|---|---|---|---|---|
| `base.txt` | base | none (committed receipt) | rc 0, no defect | rc 0, `CHECK ok cases=5`, `PREDICATE R65-C1 pass` |
| `fab.txt` | s1 + s4 + s5 | none (committed fabricated fixture) | rc 1, >=1 `CHECK defect:` | rc 0, `CHECK ok cases=5` -- the round-65 defect, still open |
| `fixtures/m-s1-1.txt` | s1 | delete `# instrument plans/round65_c1_sqlite_probe.py version=r65-c1/1` | rc 1, defect s1 | rc 0 (**strict-only**) |
| `fixtures/m-s1-2.txt` | s1 | same line, `version=r65-c1/1` -> `version=r65-c1/9` | rc 1, defect s1 | rc 0 (**strict-only**) |
| `fixtures/m-s2-1.txt` | s2 | `GRADER sha256=` -> 64 zeros | rc 1, defect s2 | rc 1, `CHECK fail grader-sha ... != b165f850...` |
| `fixtures/m-s3-1.txt` | s3 | `AMALG sha256=` -> 64 zeros | rc 1, defect s3 | rc 1, `CHECK fail amalgamation-sha ... != 0a9c8e34...` |
| `fixtures/m-s4-1.txt` | s4 | `TOOLCHAIN gcc=16.2.1` -> `gcc=15.0.0` (the `CC` line still says 16.2.1) | rc 1, defect s4 | rc 0 (**strict-only**) |
| `fixtures/m-s5-1.txt` | s5 | `RUN G2 ... rc=0` -> `rc=1` | rc 1, defect s5 | rc 0 (**strict-only**) |
| `fixtures/m-s5-2.txt` | s5 | `RUN G4 driver="/usr/bin/python3 /ctl/driver.py"` -> `driver="fabricated - nothing ran"` | rc 1, defect s5 | rc 0 (**strict-only**) |
| `fixtures/m-s5-3.txt` | s5 | delete `NOBIND G3 listeners_before=35 listeners_after=35 delta=0` | rc 1, defect s5 | rc 1, `CHECK fail G3 no-bind-observation-missing` |
| `fixtures/m-s6-1.txt` | s6 | `VECTOR G3=P/P/F` -> `VECTOR G3=P/P/P` | rc 1, defect s6 | rc 1, `CHECK fail G3 vector P/P/P != P/P/F` |

Calibration consequence: **five of the nine mutants are accepted by the committed default
mode** (m-s1-1, m-s1-2, m-s4-1, m-s5-1, m-s5-2). A `--strict` mode that only forwards
`receipt_failures()` cannot pass this corpus. The other four are default-mode failures and
are present so the strict gate cannot regress them; their strict defect must still name the
clause.

Clause-attribution notes for the lead (findings, not corrections to the claim):

- `m-s5-3` deletes a per-case `NOBIND` line. The default mode already reports
  `G3 no-bind-observation-missing`; the strict mode must report it under s5. s5's literal
  "every `NOBIND` line carries `delta=0`" is a universal over surviving lines, so the
  presence requirement is what this fixture exercises (the committed receipt also carries
  `NOBIND before-battery`/`after-battery` lines with no `delta` field, so a literal
  "every line" reading would reject the committed receipt and violate kill rule b).
- `m-s2-1` and `m-s3-1` mutate values s2/s3 also bind to the committed bytes; the strict
  finding should name s2/s3 rather than only repeating the default `CHECK fail` text.
- `m-s6-1` changes only the `VECTOR` line; the `CASE ... observed=` field still says
  `P/P/F`, matching the frozen table. The defect is the vector disagreement itself.
- Every mutant keeps `PREDICATE R65-C1 pass`, so the stored-predicate cross-check in the
  default mode fires on the four default-caught mutants. That is expected: a fabricated
  receipt claims pass.

## Runner

`run_strict_fixtures.sh <path-to-strict-capable-checker>` reads
`fixtures/expected.tsv` (tab-separated: file, clause, expected_rc; fixture paths are
relative to the table's own directory -- `../base.txt`, `../fab.txt`, `m-s*.txt` -- so the
caller's cwd does not matter), and for every row runs

    python3 <checker> --check-receipt <fixture> --strict

A row passes only when the observed exit status equals `expected_rc` **and**, for a
non-zero expectation, the captured output contains `CHECK defect`. The second condition
exists because an uncaught Python traceback also exits 1 and must never be recorded as a
gate verdict. Exit 0 = all rows matched; 1 = at least one mismatch; 2 = setup error
(argument, checker, table, fixture, interpreter). The runner writes no files (all output
is held in shell variables), never uses `/tmp`, and only reads the lane.

Syntax verification (`syntax-check.txt`, `sh` is bash 5.x on this host; `dash`, `busybox`,
`mksh`, `ksh`, `zsh` are not installed and pacman is paused host-wide):

    $ sh -n run_strict_fixtures.sh                                  -> rc 0, no output
    $ sh -n <abs>/run_strict_fixtures.sh                            -> rc 0, no output
    $ bash --posix -n <abs>/run_strict_fixtures.sh                  -> rc 0, no output

The script uses only POSIX constructs (`case`, `$(( ))`, `command -v`, `IFS=<tab> read -r`,
no `[[`, arrays, `local`, `$'...'` or `+=`).

Harness self-check (control flow only): `selftest/stub_checker.py` implements none of the
s1-s6 clauses. Its runs are evidence that the runner's parsing, comparison, message gate
and exit status work; they are **not** evidence for R67-C2 and must not be cited as such.

| stub mode | intent | runner observed |
|---|---|---|
| `faithful` | base rc 0, every other fixture rc 1 + `CHECK defect:` | 11/11 PASS, `RESULT fixtures=11 mismatches=0`, rc 0 (`selftest/run-faithful.txt`) |
| `faithful`, cwd `/` | script-dir resolution independent of caller cwd | 11/11 PASS, rc 0 (`selftest/run-faithful-other-cwd.txt`) |
| `survivor` | every fixture rc 0 (gate never fires) | 10 mismatches, rc 1 (`selftest/run-survivor.txt`) |
| `crash` | `m-s4-1` raises, rc 1 with a traceback and no `CHECK defect` | exactly that row FAILs, `mismatches=1`, rc 1 (`selftest/run-crash.txt`) |
| missing checker | setup path | `SETUP checker-missing`, rc 2 (`selftest/run-missing-checker.txt`) |

## What the lead must do after the proposal lands

1. Point the runner at the strict-capable checker **path** produced by the proposal. The
   committed `plans/round65_c1_sqlite_probe.py` is frozen for this seat; s1 requires the
   strict build to read `PROBE_VERSION` from the committed probe bytes, so the checker must
   be the proposal's file, passed as the single argument.
2. Run, from any cwd:

       sh .ufo/waves/round-67/w1/ReceiptMutate/run_strict_fixtures.sh <strict-checker-path>

   Expect `RESULT fixtures=11 mismatches=0` and rc 0. On a mismatch, the printed checker
   output under each `FIXTURE` line is the evidence for the clause-naming judgement; the
   runner gates on rc plus `CHECK defect`, not on the clause token.
3. Record the run output in the lead's own seat directory. This seat's corpus is fixed;
   do not edit a fixture to make a gate pass -- a survivor is a coverage finding.

No port lock was needed: `--check-receipt` is a pure text re-derivation that starts no
listener and runs no grader (the contract's lock applies to pytest of `test_outputs.py`
and to probe runs that open 127.0.0.1:12355). No tool was installed.

## Files

    base.txt  fab.txt  run_strict_fixtures.sh  gen_fixtures.py  report.md
    fixtures/expected.tsv
    fixtures/m-s1-1.txt  fixtures/m-s1-2.txt  fixtures/m-s2-1.txt  fixtures/m-s3-1.txt
    fixtures/m-s4-1.txt  fixtures/m-s5-1.txt  fixtures/m-s5-2.txt  fixtures/m-s5-3.txt
    fixtures/m-s6-1.txt
    syntax-check.txt  default-mode-matrix.txt
    inventory.txt  (sha256 manifest of every file here except itself)
    selftest/stub_checker.py  selftest/run-{faithful,faithful-other-cwd,survivor,crash,missing-checker}.txt
