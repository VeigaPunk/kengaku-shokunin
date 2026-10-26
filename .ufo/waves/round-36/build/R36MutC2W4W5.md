# R36MutC2W4W5 — C2 W1/W4/W5 mutation battery (kengaku round 36, wave 1, 2026-10-25)

Mutation-tester seat for C2 checks **W1** (capture manifest), **W4** (README index/coverage/parity),
**W5** (probe digest, receipt byte-equality, summary/naming) of
`plans/round36_c2_verify.py` (live digest `983ed65c885990f6d783abffbe21b70ab5414431b88a3b27d52fdbda65d67120`,
i.e. the post-Amendment-1 counter; claims freeze listed the pre-amendment counter as `f70e6d3a…`,
and Amendment 1 moved `PROBE_SHA256` — the one-line change — so this is the instrument of record).
Tooling installed: none (preexisting bash, git, python3 only).

## Fixture and genuine package

The C2 package (entry, S108–S110 rows, README index row + coverage bullet) is **not yet in the lane**
(`corpus/knowledge/tb2-regex-log-grader.md` absent, `grep -c 'S10[89]\|S110' corpus/SOURCES.md` → 0,
`grep -c 'tb2-regex-log-grader' corpus/README.md` → 0 at HEAD `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd`,
`git status --porcelain -- plans corpus` → 0), matching the freeze control (`control-c2-nothing.txt`,
`defects=4`). Per the tasking ("fixture clone **with a passing package**") I authored the genuine
package inside my fixture clone only — the lane was never written:

- Clone: `D=$(mktemp -d /tmp/k36-XXXX)` = `/tmp/k36-P4tu`; `git clone -q --no-checkout --shared
  /home/vgpnk/Projects/shokunin/kengaku-shokunin "$D/lane"`; `sparse-checkout set --no-cone 'plans/' 'corpus/'`;
  `checkout -q master`; `git -C "$D/lane" rev-parse --show-toplevel` = `/tmp/k36-P4tu/lane` ✓; HEAD `f9efce3` (same commit).
- Authored: `corpus/knowledge/tb2-regex-log-grader.md` (head source-lines S108/S109/S110, verified-at,
  recheck, Negative space falsifier, 12 located-quote rows — all verbatim on cited capture lines,
  12 distinct quotes 3–25 words, 12 distinct locations, receipt summary line verbatim);
  `corpus/SOURCES.md` rows S108/S109/S110 (11 cells, tier A, mined, opened 2026-10-25, pinned URLs,
  used-by = the entry, teaches ≥8 words pairwise distinct, inserted before `## Paths` so census E12 holds);
  `corpus/README.md` index row + coverage-map bullet (43 knowledge files == 43 `| `knowledge/` rows).

**Baseline (pre-mutation), command `python3 plans/round36_c2_verify.py --lane /tmp/k36-P4tu/lane` (cwd = live lane):**

```
W1 ok
W2 ok
W3 ok
W4 ok
W5 ok
W6 ok
checks=6 defects=0
PREDICATE C2 pass
exit=0
```

One authoring bug caught and fixed before baselining: five quote rows initially carried curly inner
quotes; straightened to the capture bytes (they must be verbatim substrings).

## Mutants (protocol: edit → run → restore exact bytes → hash-verify; one mutant at a time)

`P=/tmp/k36-P4tu/pristine` held pre-mutation copies of all nine mutable files
(`pristine-sha256.txt` in this directory records their SHA256s; restoration evidence per mutant is the
`cmp`-equal or grep-equal line below, plus the post-restore baseline). Full raw log: `mutants.log` here.

| # | Mutant | Target | Expected | Actual output (DEFECT lines; full run in `mutants.log`) | Verdict | Restoration evidence |
|---|---|---|---|---|---|---|
| M1 | `SHA256SUMS` line for `instruction.md` deleted | W1 | W1 red | `W1 DEFECT instruction.md not listed at pinned digest`; `checks=6 defects=1`, `PREDICATE C2 fail`, `exit=1` | **killed** | sha256 `17b5429c…10d21a` == pristine |
| M2 | `test.sh` digest in `SHA256SUMS` altered one hex char (`4770437e…`→`5770437e…`) | W1 | W1 red | `W1 DEFECT listed digest mismatch or missing file: test.sh`; `defects=1`, `exit=1` | **killed** | sha256 `17b5429c…10d21a` == pristine |
| M3 | listed capture absent (`instruction.md` moved out) | W1 | W1 red | `W1 DEFECT listed digest mismatch or missing file: instruction.md` **and** `W3 DEFECT quote cites missing capture instruction.md`; `defects=2`, `exit=1` (two independent defenses) | **killed** | sha256 `4f7ac05e…2e96f9c` == pristine |
| M4 | `test_outputs.py` one byte edited (canary GUID last char `e`→`f`, line count unchanged) | W1 | must go red | `W1 DEFECT listed digest mismatch or missing file: test_outputs.py` **and** `W5 DEFECT fresh probe output differs from receipt (exit 2)`; `defects=2`, `exit=1` — W1 red as required; W5 also fires because the probe itself refuses a grader whose sha ≠ pinned (probe exit 2) | **killed** | sha256 `345c3bd0…55e8f72` == pristine |
| M5 | index row without S109 (`S108, S109, S110` → `S108, S110`) | W4 | W4 red | `W4 DEFECT index row absent or missing S108/S109/S110`; `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M6 | coverage-map bullet removed | W4 | W4 red | `W4 DEFECT coverage-map bullet absent`; `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M7 | 44th knowledge file not indexed (`corpus/knowledge/zzz-m7-unindexed-mutant.md`) | W4 | W4 red | `W4 DEFECT knowledge files=44 index rows=43 (want equal and >=43)`; `defects=1`, `exit=1` | **killed** | file removed; `ls \| wc -l` = 43 |
| M8 | index row duplicated (two identical rows) | W4 | W4 red | `W4 DEFECT index row absent or missing S108/S109/S110` (fires on `len(idx) != 1`); `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M9 | receipt one byte changed (grader sha first hex char `3`→`4`) | W5 | W5 red | `W5 DEFECT fresh probe output differs from receipt (exit 0)`; `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M10 | receipt line order swapped (case lines 2↔3) | W5 | W5 red | `W5 DEFECT fresh probe output differs from receipt (exit 0)`; `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M11 | summary line removed from the entry | W5 | W5 red | `W5 DEFECT entry does not carry the receipt summary line verbatim`; `defects=1`, `exit=1` | **killed** | `cmp` pristine == restored |
| M12 | receipt case line `match=yes`→`match=NO`, case not named in entry | W5 | naming sub-check | `W5 DEFECT fresh probe output differs from receipt (exit 0)`; `defects=1`, `exit=1` — **killed by the byte-equality sub-check, not the naming sub-check the mutant targets** | **killed** (shadowed — see Observations) | `cmp` pristine == restored |
| M13 | probe file edited one byte (docstring) → digest off | W5 | W5 red | `W5 DEFECT probe file absent or digest differs from the frozen digest`; `defects=1`, `exit=1` | **killed** | sha256 `d58194c8…76519bc` == pristine (Amendment-1 digest) |
| M14 | probe replaced by stub printing the receipt (`sys.stdout.write(open("corpus/evidence/round36/regex-log-probe.txt").read())`) | W5 | frozen probe digest must catch | `W5 DEFECT probe file absent or digest differs from the frozen digest`; `defects=1`, `exit=1` | **killed** | sha256 `d58194c8…76519bc` == pristine |

**Kill count: 14/14.**

## Observations (coverage findings, not contract changes)

1. **M12 shadowing:** the "entry names every `match=NO` case" sub-check of W5 is unreachable for a
   *hand-edited* receipt, because byte-equality against a fresh run fires first. It is live only for
   the case the claims file reserves it for: a genuine probe run with `mismatches>0` (calibration
   data) whose entry omits a mismatching case. In this package (`mismatches=0`) it has no trigger —
   defense-in-depth, currently redundant with byte-equality.
2. **M14 sole defense:** the stub's stdout is **byte-identical to the receipt** — observed, not
   inferred: `python3 stub14.py | cmp - corpus/evidence/round36/regex-log-probe.txt` (cwd = clone)
   → `STUB-OUTPUT-BYTE-IDENTICAL-TO-RECEIPT`. So W5's byte-compare, `cases=24` summary regex and
   match=NO naming would all *pass* on the stub; the frozen `PROBE_SHA256` pin is the **only** check
   standing between a receipt-printing probe stub and a green W5. Any weakening of that one line
   (e.g. a "probe may be regenerated" allowance) reintroduces the round-35 stub-probe defect class.
3. Redundancy is healthy elsewhere: M3 and M4 are each caught by two independent checks (W1+W3, W1+W5).

## Restoration and containment evidence

- Every mutant restored from `$P` copies before the next run; per-mutant `cmp`/sha256 lines above.
- Final pass after M14 restore: all nine files `cmp`-equal to pristine (`clone-restore-check-done`,
  no DIFFERS lines); `sha256sum -c pristine-sha256.txt` → `pristine-self-check=0`.
- Baseline re-run on the fully restored clone: `checks=6 defects=0`, `PREDICATE C2 pass`, `exit=0`.
- Live lane untouched throughout: HEAD still `f9efce3beb0705ec2e04ba3f8f449d10d64cc1dd`;
  `git status --porcelain -- plans corpus` → 0. No git add/commit/checkout in the lane; no writes
  outside `/tmp/k36-P4tu`, this build directory, and no `pacman` use.
- Fixture removed: `rm -rf /tmp/k36-P4tu` → `FIXTURE-REMOVED`.

VERDICT: w1w4w5-mutants-14/14
