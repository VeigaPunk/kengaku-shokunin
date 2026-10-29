# C2MutCounter — round 53 wave 1: mutation test of `plans/round53_c2_tipstate.py --selftest`

Seat: C2MutCounter (mutation-tester, leaf, no subagents). Lane: `kengaku-shokunin`, base tip `536925b`, claims commit `a34838f`,
wave-1 spec commit `1373b6c`. Deliverables: `.ufo/waves/round-53/w1/C2MutCounter/`.

## Verdict

- **Frozen selftest (12 cases) is weak.** It kills 28 of 69 mutants (68 mutants plus one null). 41 survive.
  Of the 41: 1 null (by design), 5 equivalent (argued below), 1 crash-equivalent (M20), 3 verdict-equivalent or
  diagnostic-only (M39, M53, M54; a fixture can still expose the last two), 1 killable only by a child run (M66),
  and **30 are real gaps** in the selftest's coverage.
- **Augmented selftest (41 cases: the 12 frozen plus 29 proposed) kills 60 of 69.** The 9 that remain are the null, the 5
  equivalents, M39 (verdict-equivalent), M20 (crash-equivalent) and M66 (killed only when the poison child runs with
  `R53C2_POISON=1`, which I verified: pristine exits 1, M66 exits 0).
- **New defect in the frozen counter (not fixed; amendment needed):** a red row whose `evidence` is `null` makes
  `evaluate()` raise an uncaught `TypeError` at line 240 (`sp["evidence"] not in r["out"]`). The run exits 1 with a
  traceback, with no `PREDICATE` or `TIPSTATE` line. The exit code is correct only by accident; the `BAD-REASON` diagnosis
  is lost. Reproduced on a demo lane; the stderr is kept.
- **Operability:** the frozen selftest prints `cases=12 failures=0` and runs in ~2.5 s. Its predicate is never exercised in
  `--dry` mode (no dry case), and the git source-clean leg is never exercised at all.

## Commands run (exact)

Setup (scratch only; the lane was only read):
```
S=/fast/scratch/hyaku/kengaku-r53/C2MutCounter
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane rev-parse --show-toplevel        # -> $S/lane  (top-level verified)
git -C $S/lane diff --stat a34838f HEAD -- plans/round53_c2_tipstate.py plans/round53-tipstate.json   # empty: unchanged since freeze
sha256sum $S/lane/plans/round53_c2_tipstate.py                 # 859ec38d3d39d7b33ca91a1a33269606e8c174e4fbaf40eeaa28280f1dfccfc7
git -C $S/lane show a34838f:plans/round53_c2_tipstate.py | sha256sum   # same digest
cd $S/lane && TMPDIR=$S/tmp python3 plans/round53_c2_tipstate.py --selftest   # SELFTEST cases=12 failures=0, rc=0
```

Mutation battery (driver kept at `.ufo/waves/round-53/w1/C2MutCounter/mutate_c2.py`):
```
python3 .../C2MutCounter/mutate_c2.py                                                     # pristine source
C2_SOURCE=$S/aug/plans/round53_c2_tipstate.py C2_TAG=-augmented python3 .../C2MutCounter/mutate_c2.py   # augmented source
```

Method. Each mutant is one exact-string replacement (first occurrence; the driver refuses a missing pattern). The mutated
file is written to its own scratch directory `$S/m/<id>/plans/round53_c2_tipstate.py`, and `--selftest` runs there with
`TMPDIR=$S/tmp/<id>`. The lane was never written: the pristine sha256 was checked before and after (`pristine_unchanged=True`),
and a restored baseline run gave `rc=0 SELFTEST cases=12 failures=0`. A mutant is **killed** iff its exit code differs from
the baseline, or its `SELFTEST cases=` line differs (or it crashes or fails to compile). Every mutant was predicted before
it ran: **69 of 69 predictions matched** the measured verdict. Battery time: 40–110 s wall with 8 workers.

Two measurement notes. The first pristine battery's bash `time` reported `user 51m36s`; a second identical battery reported
`user 7m10s` and per-selftest child CPU of ~2 s (RUSAGE deltas). The verdicts were identical across both runs (28 killed, 41
survived); I did not isolate the first figure. The `_bash` tool also hid stdout whenever the final exit status was 1 (after
`diff` with differences, after `grep -c` with zero matches, and after a selftest that exits 1); I re-read those outputs with `read`.

## Measured numbers

| run | total | killed | survived | driver errors | baseline | restored |
|---|---|---|---|---|---|---|
| pristine (`mutation-results.json`) | 69 (68 + null) | 28 | 41 | 0 | rc 0, `cases=12 failures=0` | rc 0, `cases=12 failures=0`, pristine unchanged |
| augmented (`mutation-results-augmented.json`) | 69 | 60 | 9 | 0 | rc 0, `cases=41 failures=0` | rc 0, `cases=41 failures=0`, pristine unchanged |

Pristine kills: 23 by fixture-level assertion (M03 M06 M12 M15 M16 M18 M23 M26 M29 M32 M33 M34 M35 M36 M42 M48 M49 M50 M52
M56 M58 M60 M63), 4 by crash (M09 M10 M55 M59, `KeyError: 'evidence'`), and 1 trivially (M67, the cases-line text itself).

Full table of all 69 rows, with the pristine and augmented verdicts and the killing fixture: `.ufo/waves/round-53/w1/C2MutCounter/mutation-table.md`.
Per-mutant stdout and stderr: `.../C2MutCounter/mutants/<id>.txt` (pristine) and `.../C2MutCounter/mutants-augmented/<id>.txt`.

## The 41 pristine survivors and the missing fixture

The proposed selftest additions are in `selftest-augment.diff` (unified diff, `plans/round53_c2_tipstate.py` against the
augmented copy; 116 added lines and one changed line, `cases=12` to `cases=41`). The augmented copy
is `round53_c2_tipstate.augmented.py`. **These fixtures are proposals only.** The counter is frozen, so they must enter as a
dated amendment; I did not edit the counter. Each row names the new fixture that kills the mutant in the augmented run.

| id | mutant | class | missing fixture (augmented) |
|---|---|---|---|
| M00 | null: comment appended | null | none (by design) |
| M01 | ledger absent: missing list emptied | survivor | `ledger-absent`: expects `missing=2` |
| M02 | argv length floor 2 -> 1 | survivor | `argv-one-element`: `argv=["plans/a.py"]` expects `ENTRY-MISMATCH a` |
| M04 | argv all-str check disabled | survivor | `argv-nonstring-element`: `argv=["python3","plans/a.py",7]` |
| M05 | script-None guard removed | equivalent | — |
| M07 | exit bool exclusion removed | survivor | `exit-is-bool`: `exit=True` expects `BAD-DECL b` |
| M08 | state domain check removed | survivor | `state-outside-domain`: `state="amber"` expects `BAD-DECL b` |
| M11 | kind domain check removed | survivor | `kind-outside-domain`: `kind="bogus"` expects `BAD-DECL a` |
| M13 | reason floor `<` -> `<=` | survivor | `reason-exactly-10-words`: expects PASS |
| M14 | MIN_REASON_WORDS 10 -> 9 | survivor | `reason-9-words`: expects `BAD-REASON b` |
| M17 | evidence floor 6 -> 5 | survivor | `evidence-5-chars` (`DEFEC`): expects `BAD-REASON b` |
| M19 | evidence `strip()` dropped | survivor | `evidence-padded-short` (`   ab   `): expects `BAD-REASON b` |
| M20 | evidence `str` check removed | crash-equivalent | none possible: see finding F1 (both paths exit 1 via traceback) |
| M21 | help limit `<=` -> `<` | survivor | `help-at-exact-limit` (1 of 10 = 1.0): expects PASS |
| M22 | MAX_HELP_FRACTION 0.10 -> 0.50 | survivor | `help-fraction-quarter` (1 of 4): expects `help=1 help_limit=0.4` |
| M24 | kind-count guard removed | survivor | `kind-outside-domain` (mutant raises `KeyError: 'bogus'`) |
| M25 | static_ok missing term removed | survivor (masked) | `dry-missing-row` (dry mode only) |
| M27 | static_ok entry_mismatch term removed | survivor (masked) | `dry-entry-mismatch` (dry only) |
| M28 | static_ok bad_decl term removed | survivor (masked) | `dry-bad-decl` (dry only) |
| M30 | static_ok dups term removed | survivor | `duplicate-row-name`: expects `DUPLICATE a` |
| M31 | static_ok ledger_err term removed | survivor | `ledger-absent-no-rows`: expects `LEDGER ledger absent` |
| M37 | entry regex loses `corpus/` prefix | survivor | `corpus-entry-script`: expects PASS |
| M38 | duplicate name not recorded | survivor | `duplicate-row-name` |
| M39 | duplicate first-wins | verdict-equivalent | — (dups already fail the predicate; only the validated line changes) |
| M40 | ledger schema check removed | survivor | `ledger-schema-foreign`: expects `ledger schema mismatch` |
| M41 | dry-run exit inverted | survivor | `dry-truthful`: expects rc 0 |
| M43 | help limit `max(1,n_reg)` -> `n_reg` | equivalent | — |
| M44 | clean `in (True,None)` -> `is not False` | equivalent | — |
| M45 | clean test widened to admit dirty | survivor | `git-dirty`: dirty source clone expects rc 1 and `clean=no` |
| M46 | `executed == n_reg` -> `>=` | equivalent | — |
| M47 | `executed == n_reg` dropped | equivalent (argued) | — |
| M51 | only-is-None term dropped | survivor | `only-every-row` (`only={a,b}`) expects FAIL |
| M53 | `--only` filter disabled | diagnostic-only | `only-one-row-count`: expects `RUN executed=1` |
| M54 | entry_mismatch rows executed | diagnostic-only | `entry-mismatch-not-executed`: `want_out` `MISMATCH a declared` |
| M57 | per-row `timeout_s` ignored | survivor | `timeout-default-ignored` (3 s hang, `timeout_s=2`) |
| M61 | observed-green counter inverted | survivor | `tally-two-green-one-red`: expects `observed_green=2 observed_red=1` |
| M62 | declared-green count reads red | survivor | `tally-two-green-one-red`: expects `declared_green=2 declared_red=1` |
| M64 | selftest `want_out` check removed | survivor (meta) | `neg-want-out`: a negative control the harness must reject |
| M65 | selftest `want_in` check removed | survivor (meta) | `neg-want-in`: negative control |
| M66 | selftest exit always 0 | survivor (default run) | `poison-child`, env-gated: `R53C2_POISON=1` must exit 1 (verified) |
| M68 | selftest `rc` check vacuous | survivor (meta) | `neg-want-rc`: negative control |

Pristine survivors M24 and M45 are listed above; the git-dirty fixture is the only test of the source-clean leg.

### Equivalent mutants (argued)
- **M05** `script is None or script not in argv`: `argv` is all strings (checked just before), so `None not in argv` is
  already True; the `script is None` term is redundant.
- **M43** `max(1, n_reg)` -> `n_reg`: when `n_reg == 0`, `kinds` are all zero, so `0 <= 0` and `0 <= 0.1` agree.
- **M44** `clean in (True, None)` -> `clean is not False`: `clean` only takes `None`, `True` or `False`.
- **M46** `executed == n_reg` -> `>=`: `executed <= len(names) <= n_reg` always.
- **M47** `executed == n_reg` dropped: when `static_ok` holds (no missing, extra, entry_mismatch, bad_decl, dups, ledger_err)
  and `only is None`, `names` is every row, so `executed == n_reg` always holds; in every other case the `only is None` or
  `static_ok` conjunct already fails. The conjunct is redundant.

### Verdict-equivalent or diagnostic-only
- **M39** (first-wins on duplicate names): dups already make the predicate fail, so the verdict is the same either way.
- **M53** and **M54**: the verdict is the same (`--only` or entry_mismatch rows already fail the predicate), but the
  diagnostic output differs. The augmented run catches them only by checking the printed line (`RUN executed=1`, or the
  absence of `MISMATCH a declared`). Under the frozen kill rule these survive, so I report them as survivors on diagnostics.

### Crash-equivalent
- **M20**: with `evidence` null, the pristine counter raises `TypeError` in `evaluate` (line 240) and M20 raises
  `AttributeError` in `static_legs`. Both exit 1 with a traceback and no `cases=` line, so the kill rule cannot tell them
  apart. Stderr for both is kept: `crash-evidence-null-pristine.stderr.txt` and `crash-evidence-null-M20.stderr.txt`.

## Findings for the L1 (none fixed; each needs a dated amendment because the counter is frozen)

- **F1. Crash instead of diagnosis on non-string red evidence.** Demo: a lane whose red row `b` has `"evidence": null`
  (`$S/demo/`). Pristine: `TypeError: 'in <string>' requires string as left operand, not NoneType`, exit 1, no `PREDICATE`
  line. The static leg already classifies such a row as `BAD-REASON` (`not isinstance(ev, str)`), but `evaluate` still
  executes the row and dereferences `evidence`. A fix would route bad-reason rows around the evidence check, or guard it with
  `isinstance`. Not applied.
- **F2. Predicate-mode masking.** `executed == n_reg` hides the static terms `missing`, `entry_mismatch`, `bad_decl`, dups and
  ledger_err in predicate mode, because those rows are not executed. Those terms can only be seen with `--dry`, and the
  frozen selftest has **no** `--dry` case. Survivors M25, M27, M28 and M41 are all dry-mode.
- **F3. Untested legs.** The frozen 12 cases do not exercise: ledger absent (only via `ledger_err`), zero rows, duplicate names,
  non-string argv, bool exit, state and kind domains, the 10-word and 6-char boundaries, the help fraction at its limit, the
  git source-clean leg (`clean=no`), `--only` with every row, the per-row `timeout_s`, the TIPSTATE tallies (`observed_green`,
  `declared_green`), and the selftest's own `want_out`, `want_in` and `rc` clauses.
- **F4. Harness self-checks are unverified.** Removing the `want_out` check (M64), the `want_in` check (M65), or the `rc`
  check (M68) survives. The exit mapping (M66) survives. `main()` cannot be tested in-process; only a child run shows it.
  The selftest also has no `try/finally`, so a raising case leaves its `TMPDIR` tree behind (code reading; not exercised).
- **F5. Kill rule blind spot.** Crash-driven kills (M09, M10, M55, M59 pristine; M24 augmented) count as killed because the exit code and the
  cases line change, but they do not show the counter reports the right failure. Fixture-level kills are what matter for
  calibration; the crash kills are weaker.

## Files (absolute paths)

Seat deliverables, all under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C2MutCounter/`:
- `mutate_c2.py` (the driver: replacement table of 69 mutants plus the runner)
- `mutation-results.json` (pristine: per mutant rc, cases line, verdict, wall time, crash tail)
- `mutation-results-augmented.json` (same, against the augmented source)
- `mutation-table.md` (69-row table: pristine and augmented verdict and killing fixture)
- `selftest-augment.diff` (unified diff, the proposed fixtures against the frozen `selftest()`)
- `round53_c2_tipstate.augmented.py` (the augmented copy, 41 cases)
- `mutants/` (69 per-mutant outputs, pristine) and `mutants-augmented/` (69, augmented)
- `run-pristine.txt`, `run-augmented.txt` (battery logs), `aug-base.out` (augmented pristine selftest output)
- `crash-evidence-null-pristine.stderr.txt`, `crash-evidence-null-M20.stderr.txt` (finding F1 evidence)
- `poison-child-augmented.stdout.txt`, `poison-child-M66.stdout.txt` (M66 poison-child evidence: augmented exits 1, M66 exits 0)

Scratch under `/fast/scratch/hyaku/kengaku-r53/C2MutCounter/` (lane clone, mutant dirs, demo) is removed before yield.

## Tooling

No tool installed or updated. Used stock `python3`, `git` (clone and read-only queries against the lane), `sha256sum`,
`diff`. pacman not used. No credential-shaped strings are in any output; fixture email is `c2@example.invalid`.

tool: `_bash` hid stdout whenever the command's final exit status was 1 (diff with changes, grep with no match, a selftest that exits 1). Output must be re-read with `read`.

## Blindness

This seat never read or ran a label seat file, `plans/round53_c1_classify.py`, `.ufo/waves/round-53/w1/C1ExecClassifier*`,
or any `C1Label*` directory. It read `plans/round-53-claims.md` and `plans/round53_c2_tipstate.py`, plus read-only git metadata
of the lane. No blindness violation.
