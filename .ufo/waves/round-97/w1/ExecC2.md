# ExecC2 — independent C2 re-run and semantic self-test audit (round 97, wave 1)

Seat: ExecC2 (leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Revisions: BASE `4992cd0e32b8db23ca20310deb7de12d485f8bcc`, P0 `5b41c1c3`, P1 `b2352135`,
P2 `e40fd0c2`, freeze F `8d9d271306c4e7e2d586e51cd546652249d286cb`, measured T
`f1083da60e7ff6b88f7420aae7424f7762d14700` (lane HEAD throughout this seat).

No production edits, no commits/pushes/jj writes in the lane, no `task` calls, no host sysctl or
service mutation, no pacman transaction. All writes are this report, the evidence directory
`.ufo/waves/round-97/w1/ExecC2/`, and scratch `/fast/scratch/hyaku/kengaku-r97/ExecC2` (removed
after copying receipts). Every measurement ran against a `git clone --shared` detached at T, and
the two official reproductions also ran from the lane root (read-only `git show` only). The lane
working tree showed sibling-seat edits during the seat (`LOG.md`, `corpus/QUALITY.md`,
`corpus/README.md` modified; `corpus/knowledge/tb2-sparql-university-grader.md`,
`corpus/lessons/round-97.md` new); none are mine and none affect these numbers.

## Verdict

| Check | Result |
|---|---|
| R97-C2 frozen predicate at T | **pass**, rc 0 — the four frozen lines print verbatim |
| R97-C2 frozen predicate at BASE | **fail**, rc 1 — `without=44`, `MISMATCH_TOTAL n=44` |
| Census self-test public CLI | **pass**, rc 0 — `SELFTEST cases=8 failed=0` |
| 44 retyped scripts really lack a self-invocation mode | **confirmed, 44/44** — AST + public CLI, both spellings |
| False positives (a retyped script that has a real mode) | **none** (0 of 44) |
| False negatives (a remaining gate whose "mode" is only a regex artifact) | **none** (0 of 84) |
| Mismatches before → after | **44 → 0** |
| Defect found in the frozen instrument | **none** |

I found no unmet clause of R97-C2 that I could measure. The calibration correction is sound on the
observed bytes; the only residual risk is the detector's text sensitivity, which no lane row
exercises (section 6).

## 1. Official predicate reproduction

From the lane root, exact contract command, `TMPDIR` set to scratch:

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round97_gate_selftest_census.py --lane . --rev 4992cd0e32b8db23ca20310deb7de12d485f8bcc
```
```
REV 4992cd0e32b8db23ca20310deb7de12d485f8bcc BASE 4992cd0e32b8db23ca20310deb7de12d485f8bcc
ROWS base=168 rev=168 removed=0 duplicate=0 cells_changed=0
GATES total=127 with_selftest=83 without=44 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=44
...
PREDICATE R97-C2 fail
```
rc 1. The 44 `MISMATCH` lines are byte-identical to `.ufo/waves/round-97/L1/c2-base.txt` (the only
difference is that the L1 receipt appends its shell `rc=1` line).

```
python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da60e7ff6b88f7420aae7424f7762d14700
```
```
REV f1083da60e7ff6b88f7420aae7424f7762d14700 BASE 4992cd0e32b8db23ca20310deb7de12d485f8bcc
ROWS base=168 rev=171 removed=0 duplicate=0 cells_changed=0
GATES total=84 with_selftest=84 without=0 demoted_with_selftest=0 scripts_changed=0
MISMATCH_TOTAL n=0
PREDICATE R97-C2 pass
```
rc 0. This is the frozen predicate verbatim. The census script's sha256 at T is
`a255e83009bc137c40ba42b02c5c4d000dc6656343417d5e4319bd3395460b7f`, equal to the frozen table.

## 2. Self-test public CLI

```
python3 plans/round97_gate_selftest_census.py --selftest --work <scratch>/lane-selftest-work
```
rc 0:
```
CASE base-red         rc=1 want_rc=1 ids=MISMATCH        ok=True
CASE retype-green     rc=0 want_rc=0 ids=-               ok=True
CASE row-removed      rc=1 want_rc=1 ids=ROW-REMOVED     ok=True
CASE demoted          rc=1 want_rc=1 ids=DEMOTED         ok=True
CASE cell-changed     rc=1 want_rc=1 ids=CELL-CHANGED    ok=True
CASE script-forged    rc=1 want_rc=1 ids=SCRIPT-CHANGED  ok=True
CASE prose-only       rc=1 want_rc=1 ids=MISMATCH        ok=True
CASE duplicate        rc=1 want_rc=1 ids=ROW-DUPLICATE   ok=True
SELFTEST cases=8 failed=0
```
The same eight cases pass with a fresh, non-existent `--work` directory (created, then emptied by
the `finally` cleanup). The self-test drives the **public CLI** (`python -I -B <script> --lane
<fixture> --rev <rev> --base <base>`) and asserts both rc and finding ids, so it is not a
helper-only check. Edge cases: `--selftest` without `--work`, missing `--rev`, unresolved rev, and
a non-repo `--lane` all return rc 2 with `DEFECT SETUP ...` and `PREDICATE R97-C2
could-not-evaluate` — the declared `2` class.

## 3. Independent semantic audit of the 44 (not a regex match)

Method (my own code, `independent_count.py` + `analyze.py`):

1. Re-parsed the registry from `git show REV:SKILL.md` (same read-only inputs, worktree never read).
2. Parsed every gate entry script with `ast` and looked for a **real** self-invocation mechanism:
   an `add_argument` option named `--selftest`/`--self-test` (constant or built from a loop tuple),
   an `add_parser("selftest")` subparser, a manual argv dispatch on either spelling, or a
   `run_selftest`/`selftest` function reached from the CLI. A subprocess invocation of *another*
   script's `--selftest` does not count.
3. Ran the public CLI of all 44 scripts inside `bwrap` (`--ro-bind / /`, `--unshare-net`, tmpfs
   `/tmp`, `-I -B`, 30 s timeout) with `--selftest`, `--self-test`, and `--help`. Ten scripts check
   required arguments before unknown ones, so those ten were re-run with dummy required arguments
   (and `pkg_gate` under all three subcommands).

Result:

- **44/44 reject both spellings.** 34 print `unrecognized arguments: --selftest` directly; the ten
  required-argument scripts print a missing-argument error first (`pkg_gate` needs its subcommand
  and then `--spec`) and then `unrecognized arguments: --selftest` once the required flags are
  supplied. The same holds for `--self-test` (44/44). `--help` exits 0 for all 44 and prints
  **zero** lines containing `self`.
- **No hidden spelling.** No script among the 44 has a `selftest` subparser or a positional that
  accepts `selftest` (`pkg_gate` subcommands are `package`/`d4-line`/`d5-line`; `round82_c2_checks`
  rejects `selftest` as an invalid choice, `u1..u7` only). The only standalone `--selftest` argv
  literal in the 44 is `round46_c2_verify.py:193`, which invokes
  `plans/anchor_line_check.py --selftest` as a leg — another script's mode, not its own
  (`round41_c1_verify.py:194` merely quotes another script's usage line containing the word).
- **84/84 T gate rows have a real mechanism** (83 BASE gates + the new `round97-gate-selftest-census`).
  Every one resolves to an argparse option, a subparser, or a manual argv dispatch; the
  `--selftest` dest is referenced in all but `round66-c1-tensor-probe`, which dispatches by
  fall-through (`cmd_selftest` is the last branch of a required mutually-exclusive group).
- **Set identity.** My independent BASE mismatch set is exactly the census's 44 `MISMATCH` names,
  and exactly the 44 rows whose `kind` changed `gate→probe`. No extra name, no missing name.
- **False positives by name: none** (0 of 44). **False negatives by name: none** (0 of 84).

The 44 (all now `probe`, all byte-identical at BASE and T):

`package-gate`, `round36-c1-battery`, `round37-c1-mutants`, `round37-c2`, `anchor-digest-check`,
`ledger-tip`, `round38-c1-mutants`, `round38-c2`, `mutant-direction-check`, `tip-receipts`,
`round39-c1-mutants`, `round39-c2`, `order-check`, `round39-c1-audit`, `round40-c1-mutants`,
`round40-c2`, `round41-c1-mutants`, `round41-c2`, `round42-c1-mutants`, `round42-c2`,
`round43-c1-mutants`, `round43-c2`, `round44-c1-mutants`, `round44-c2`, `adoption-check`,
`defect-ledger`, `round28-census`, `round35-c1-coverage`, `round35-hardening`, `round36-c2`,
`round45-c1`, `round45-c2`, `round46-c1`, `round46-c2`, `round46-c3`, `round50-c1`,
`freeze-integrity`, `round95-c2-counter`, `round96-c1-replay`, `round96-standing-battery`,
`round37-c1-attribution`, `round82-c2-checks`, `round88-c1-replay`, `round89-c1-replay`.

The two round-96 rows routed by the round-96 spot-check (defects 3 and 4) are in the set.

## 4. Counts before → after

| Measure | BASE `4992cd0e` | T `f1083da6` |
|---|---|---|
| registry rows | 168 | 171 (+3 new) |
| rows typed `gate` | 127 | 84 |
| gates with a self-test mechanism | 83 | 84 |
| gates without (mismatches) | **44** | **0** |
| predicate rc | 1 (`fail`) | 0 (`pass`) |

Both the official counter and my independent semantic counter give 44 → 0.

## 5. Cross-checks (independent of the census's own legs)

- **Only the 44 kind cells changed.** Registry parser comparison: 44 diffs, all `gate→probe`;
  **0** non-kind cell diffs. The `self-test` cells of the 44 are unchanged (many already said
  "none" or named external controls). The only other SKILL prose change is the Round-97 registry
  correction paragraph; the `file-artifact` row and the two new probe rows are C1's.
- **No old script changed.** Of the 168 scripts referenced by BASE registry rows, **0** differ at T
  (byte comparison). Three scripts are new at T (`round97_c1_replay.py`,
  `round97_gate_selftest_census.py`, `round97_sparql_probe.py`).
- **The 44 scripts are byte-identical at BASE and T** (sha256 table `sha44.tsv`, 44/44 `same`).
- **Row identity.** 168 unique names at BASE, 171 unique at T, no duplicates, no removals.
- **Freeze integrity (cross-check only).** All ten frozen-instrument shas and all three
  candidate-byte shas at T equal the F table (`frozen-and-candidate-shas.txt`).

## 6. Detector residual limitations (not present in the lane population)

The census detector is a text regex. Two spelling-texture gaps were demonstrated on isolated
fixture repos (not the lane):

| Fixture | Script | Census result | Meaning |
|---|---|---|---|
| `underscore-flag` | `add_argument("--self_test")` | rc 1 `MISMATCH` | a real mode spelled with an underscore is counted as absent (would wrongly demote) |
| `docstring-prose` | `add_argument("--selftest")` only in a docstring | rc 0 `pass` | prose is counted as a mode (would wrongly keep a gate) |
| `comment-prose` | same in a comment | rc 0 `pass` | same |
| `hyphen-flag`, `subparser` | real `--self-test` / `selftest` subparser | rc 0 `pass` | controls |

No row in the 44 or the 84 exercises either gap: I checked the actual bytes for underscore
spellings, prose-only mentions, and dynamic flag construction. This is a named residual risk for a
future round, not a defect in this round's claim.

## 7. Observations (not defects)

- 20 of the 41 BASE `probe` rows already carry a `--selftest` mode (e.g. `catalog-probe`,
  `round81-c2-checks`, the C1 replay probes). The claim is one-directional — it corrects `gate`
  rows that lack a self-test — so these are not mismatches. If a later round wants `kind` to track
  capability in both directions, those rows are the candidate set; this round does not claim it.
- `freeze-integrity` and `round95-c2-counter` run in-process batteries but expose no self-invocation
  mode; `probe` is consistent with PROTOCOL §Gate standard ("a helper-only ... self-check does not
  satisfy this clause").
- `package-gate`'s self-test cell points at `round36_c1_verify.py`; that is an external battery, not
  a self-invocation mode of `pkg_gate.py`, so `probe` is right.

## 8. Exact commands and exit codes

All from the lane root or the scratch clone; `TMPDIR=/fast/scratch/hyaku/kengaku-r97/ExecC2/tmp`.

| # | command | rc |
|---|---|---|
| 1 | `python3 plans/round97_gate_selftest_census.py --lane . --rev 4992cd0e…` (lane root) | 1 |
| 2 | `python3 plans/round97_gate_selftest_census.py --lane . --rev f1083da6…` (lane root) | 0 |
| 3 | `python3 plans/round97_gate_selftest_census.py --selftest --work …/lane-selftest-work` | 0 |
| 4 | same with a fresh non-existent `--work` | 0 |
| 5 | `--selftest` without `--work` | 2 |
| 6 | `--rev` missing | 2 |
| 7 | `--rev deadbeef` | 2 |
| 8 | `--lane /tmp --rev HEAD` | 2 |
| 9 | `python3 independent_count.py lane f1083da6…` | 0 |
| 10 | `python3 detector_probe.py ev/detector-work` | 0 |
| 11 | 44 × `bwrap … python3 -I -B <script> --selftest` | 44 × 2 |
| 12 | 44 × `bwrap … python3 -I -B <script> --self-test` | 44 × 2 |
| 13 | 44 × `bwrap … python3 -I -B <script> --help` | 44 × 0 |
| 14 | `pkg_gate` `package`/`d4-line`/`d5-line` with `--selftest` | 3 × 2 |
| 15 | `round82_c2_checks.py selftest` | 2 |

## 9. Evidence

`.ufo/waves/round-97/w1/ExecC2/`:

- `lane-census-base.txt`, `lane-census-t.txt` — official runs from the lane root.
- `census-base.txt`, `census-t.txt` — same from the detached clone.
- `lane-selftest.txt`, `census-selftest.txt`, `selftest-fresh.txt` — self-test CLI runs.
- `census-cli-edge.txt` — rc-2 edge cases.
- `independent_count.json` — independent BASE/T counts and mismatch names.
- `analysis.json` — per-row AST analysis of all 127 BASE gates; `analysis-summary.json` — trimmed.
- `sha44.tsv` — sha256 BASE/T for the 44 scripts (all `same`).
- `confirm44.tsv` — per-script public-CLI confirmation for both spellings.
- `probe44.tsv`, `probe44b.tsv`, `probe44_selftest_dash.tsv`, `probe44b_selftest_dash.tsv`,
  `help44.tsv`, `pkg_gate_probe.txt` — raw probe outputs.
- `gate-mechanisms.txt` — mechanism for each of the 84 T gate rows.
- `registry-diff.txt` — 44 kind-only diffs, 0 non-kind, 3 new rows.
- `scripts-unchanged.txt` — 168 BASE scripts, 0 changed, 3 added.
- `sha-census.txt`, `frozen-and-candidate-shas.txt` — freeze/candidate cross-check.
- `detector-probe.txt` — spelling-texture fixtures.
- `commands.txt` — the command/rc table above.

Scratch `/fast/scratch/hyaku/kengaku-r97/ExecC2` removed after the copy.

## 10. Risks and blockers

- **None blocking.** The predicate, the self-test CLI, the 44-name population, the counts and the
  byte scope all reproduce.
- Residual risk (not exercised here): the detector's text-regex sensitivity to underscore spellings
  and prose mentions (section 6). A future gate whose self-test is spelled `--self_test`, or a
  future gate that merely documents `add_argument("--selftest")`, would be mis-typed by this
  detector. No current row does.
- I did not run the full C1 replay (ExecC1's seat) or the full harm battery (ExecHarm's seat); the
  freeze/candidate sha cross-check here is a scoped confirmation, not a replacement for those.
