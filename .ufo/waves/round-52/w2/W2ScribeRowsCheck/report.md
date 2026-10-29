# Round 52 · wave 2 (falsify) · seat W2ScribeRowsCheck (scribe)

Lane: `kengaku-shokunin` (tip `87301ba`, branch `master`). Attack target: the 28 gate/probe registry rows added to `SKILL.md`
for R52-C2 (operability), checked independently of the row assembler, plus the two round-52 counters.

## Verdict

- **28 landed rows checked: 25 true, 3 false, 0 unverifiable.** The attack landed on 3 rows.
- **Landed text is identical to the wave-1 drafts**: 28 of 28 rows match `C2ScribeRows{A..F}` byte-for-byte (`diff` by python), no missing and no extra names.
- **The two round-52 counters have no registry row** and no draft proposes one (`round52_c1_grader_audit.py`, `round52_c2_registry.py` are cited nowhere in SKILL.md, SCORECARD.md, LOG.md, corpus/README.md or corpus/knowledge). Reported as `unverifiable` with `no_row: true`. Not a row truth claim.

### False rows (corrected cell text in `row-truth.json` → `corrected_cell`)

| row | false clause | measured | corrected clause |
|---|---|---|---|
| `round46-c3` | VERDICT: "`checks=7 defects=0` under `--filler`" | `python3 plans/round46_c3_verify.py --lane . --filler --work <scratch>` → `V3 ok`, `V4/V6/V7/V9/V10/V12 DEFECT`, `checks=7 defects=6`, `PREDICATE C3 fail`, rc=1 | "under `--filler` the do-nothing control must print `checks=7 defects=6` and `PREDICATE C3 fail` (measured at 87301ba: V4, V6, V7, V9, V10, V12 DEFECT, rc=1)" |
| `round46-c1` | SELFTEST: "the 35 controls under `.ufo/waves/round-46/claims/`" | `ls … \| grep '^control-.*\.txt$'` = **34**; `grep -i control` = 35 only because it also matches `stage2_controls.py`, a script | "the 34 control receipts (`control-*.txt`) … " |
| `round51-routing` | VERDICT: "no `2` path exists" | `python3 plans/round51_routing.py --bogus` → `unrecognized arguments: --bogus`, **rc=2** | "`2` argparse usage only (unrecognized flag, measured `--bogus` → exit 2); the script has no setup exit" |

`round46-c3`'s falsity is material: the row presents the do-nothing filler control as a pass. The filler is red by design (its default-mode V13 line reports `filler_checks=7 defects=6`), so a reader would take a control that should fail as a green.

### Caveats (verdict stays true; cell wording should change)

- `round35-hardening`: the `H6 FAIL untracked_anywhere=2` example is a volatile figure. Clean clone at `30801b4` gives `H6 ok untracked_anywhere=0` and `hardening run=6 failed=0` (exact). The live lane gave `214` at check time because other seats' untracked files count. Suggest a non-numeric example or a dated one.
- `round35-c1-coverage`: `PREDICATE C1 pass` is unreachable at `87301ba` (V4 `knowledge files=55 index rows=54 (want 42/42)`). The cell discloses this; flagged for the L1 only.
- `round51-surfaces`: probes resolve paths against the cwd. Run from another directory, the counts change (measured `present=4 absent=16`, rc=1, `RESOLVE violated`). From lane root: `present=14 absent=6`, `PREDICATE R51-C1 pass`, rc=0. The cell's `--lane .` implies lane-root cwd; saying so would prevent a false red.
- `round50-c2`: the cell's self-test command `--selftest` without `--lane` works only from lane root (default `.`); elsewhere it dies with FileNotFoundError, rc=1.
- `round50-c1`: at `87301ba` the default run prints `TREE dirty=24` and `PREDICATE R50-C1 fail` because other seats' untracked files are present; all other legs match the cell exactly (described by the cell's own dirty-tree failure line).
- `round46-c3`: `pkg-spec-r46.json` digest `560c7bfb…` is the masked-receipt digest; the raw file sha256 is `f9a0e3cc…`. Unverifiable byte-wise; not a false claim by itself.

## What was checked, per row (all 28)

Commands are run from the lane root unless `--lane <abs>` is shown; `TMPDIR` and `--work` point into scratch; `PYTHONDONTWRITEBYTECODE=1` set on every run.

1. **Entry flags.** Parsed each cell's `--flags` and compared with the script's argparse (`add_argument`) and literal strings (`flagcheck.py`). Every cited flag exists. Flags that are not in argparse are git/uv/pkg_gate arguments named in the scope cell, or self-test flags the cell says are absent (correctly).
2. **Exit map.** Static enumeration of `return`/`sys.exit`/`raise SystemExit` per script (`facts.py`), plus measured exits for every cell claim that could be run cheaply: setup/usage codes (rc=2 for missing `--revision`, `--expect`, `--lesson`, `--bogus`, `--dry` on tb2, `--selftest` where the cell says none); verdict codes on the default runs; setup refusals (`--file` missing, `--work` parent absent, `--manifest` absent).
3. **Self-test claims.** Ran every cell that names a self-test: catalog-probe, gate-flip-check (`ok=27/27`), parser_policy_compare (`cases=59 mutants=10 killed=10`), round30/31/33 defects and c1 (`checks=5/6/10/14`, `cases=11`, `CASE` line counts 11 and 14), round50-c2 (`verdict=ok`), round51-routing (`cases=11 failures=0`), round51-surfaces (`cases=9 failures=0`), routed_open (`12/12`), anchor_line_check (rc=0). Ran `--selftest` where the cell says none: rc=2 on every one.
4. **Pinned values.** `sha256` of each pinned file vs the prefix in the cell (`digests.py`, `flagcheck.py`, ad-hoc `sha256sum`): 33 digest prefixes exact, covering attrib_probe `489f938a`, grader.py `90c87c88`, round44 `6cf05323`, regex_log_probe `d58194c8`, tb2 test.sh / instruction.md / test_outputs for round35, 36, 45 and 46, the password and polyglot capture sets (setup, solve, instruction, README, test.sh, Dockerfile, task.toml), anchor_line_check `35d02dc5`, pkg_gate `ea638822`, pkg-spec-r45 `2f924ffa`, pkg-spec-r35 `e085b435`, password_recovery_probe `9363e03e`, polyglot_c_py_probe `67a8f4a6`, honest50 population `b5197f94`, password dry table `46036abe`, fixture_fence `57adce4a`, the tb2 receipt `2359d906`, shim `42d86d99`, round45_c2_verify `ab6825e3`. One digest (`pkg-spec-r46` `560c7bfb`) is over a receipt-masked form and is unverifiable byte-wise. Pinned paths: about 110 unique path tokens resolved (`pathcheck.py`); the only misses were glob shorthands (`f1`–`f20`, `plans/battery42–44`), a rolled-up `…/round-3{1,2}` absolute fleet path (both directories exist), and the self-test-generated `plans/round50_selftest_bogus.py`, which the cell names as bogus.
5. **Write scope.** Grep for every write, mkdir, copy, rm and git call in the 28 scripts (`open(…,'w'|'a')`, `write_text`, `write_bytes`, `mkdir`, `copyfile`, `rmtree`). Each write I found is inside a `mkdtemp`/`TemporaryDirectory`, a `--work`/`--out`/`--receipt` path the cell names, or the sandboxed `/app` of a bwrap case. Lane-tree writes were not found in any entry path. attrib_probe writes only `--out`/`--receipt` (append), journalctl only in `cmd_score`.

Measured numbers that matched the cell **exactly**, a sample: `ROWS total=75 open=31 blocked=1 closed=41 refused=2 routed_open=32 oldest_round=39`; `POINTERS total=292 … unresolved=0`; `TOTAL population=1964 … policies_with_flips=5`; `cases=18 observed_pass=5 observed_fail=13 mismatches=0` (uv biopython 1.85, output byte-equal to receipt); `PINS total=65`/`REFUSALS total=20`/`SEALED total=12`/`PINS total=33`; `FLIPS total=1 unresolved=1`; `cases=24 observed_pass=8 observed_fail=16`; full `password-recovery-probe` and `polyglot-c-py-probe` runs byte-equal (diff 0 lines) to their committed receipts; `stagecheck cases=16 failed=0` and `cases=18 failed=0`.

## Commands (abridged; full stdout under `receipts/`)

```
python3 plans/<script>.py <flags>        # 28 entry scripts, default and --selftest, usage cases
uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .
python3 plans/password_recovery_probe.py --lane <lane> --work <scratch>      # full run, diffed vs receipt
python3 plans/polyglot_c_py_probe.py   --lane <lane> --work <scratch>      # full run, diffed vs receipt
python3 plans/round45_c1_verify.py --lane . --work <scratch>               # PREDICATE C1 pass
python3 plans/round45_c2_verify.py --lane . --work <scratch>               # V2 DEFECT (dirty tree), checks=11 defects=1
python3 plans/round46_c1_verify.py --lane . --work <scratch>               # PREDICATE C1 pass
python3 plans/round46_c2_verify.py --lane . --work <scratch>               # PREDICATE C2 pass
python3 plans/round46_c3_verify.py --lane . --work <scratch> [--filler]    # default: checks=13 defects=3 ; filler: checks=7 defects=6
python3 plans/round50_c1_verify.py --lane . --work <scratch>               # TREE dirty=24, PREDICATE R50-C1 fail
python3 plans/round50_c2_audit.py --lane .  [--selftest]                   # pass; selftest verdict=ok
python3 plans/round51_surfaces.py --lane . [--selftest]                    # PREDICATE R51-C1 pass (from lane root)
python3 plans/round51_routing.py --lane . ; --bogus                        # pass; --bogus rc=2
python3 plans/round52_c1_grader_audit.py --lane .                          # PREDICATE R52-C1 fail, R52-C1-A5 fail (other seats' legs)
python3 plans/round52_c2_registry.py --lane .                              # PREDICATE R52-C2 pass
```

Clean-clone checks (`git clone --no-hardlinks` into scratch, `git checkout 30801b4`, base tip): `round35_hardening` → `H6 ok untracked_anywhere=0`, `run=6 failed=0`, rc=0; `round45_c2_verify` → `V2 DEFECT spec=frozen gate=frozen gate_exit=1`, `checks=11 defects=1`, rc=1.

## Lane integrity

`git --no-optional-locks status --porcelain` before (`runs/lane-status-before.txt`, 18 lines) and after (`runs/lane-status-after2.txt`): the only new entries are other seats' `.ufo/waves/round-52/w2/…` files. I created no lane file. Some ignored `__pycache__` directories exist in the lane; I checked whether any came from my runs (every run used `PYTHONDONTWRITEBYTECODE=1`; scripts run as `__main__` write no pyc) and found none attributable to me. I did not delete anything in the lane.

## Tooling

No tool installed or upgraded. `uv` (`/home/vgpnk/.local/bin/uv`) was already present and used for the TB2 probe; `git` and `python3` 3.14 are host tools.

## Files produced (absolute)

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeRowsCheck/row-truth.json` — 30 objects: 28 landed rows + the two counters (`no_row`).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeRowsCheck/report.md` (this file; also at `…/w2/W2ScribeRowsCheck.md`).
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w2/W2ScribeRowsCheck/receipts/` — the checker scripts (`facts.py`, `parse_rows.py`, `flagcheck.py`, `pathcheck.py`, `digests.py`), parsed rows (`rows-parsed.json`, `facts.json`, `new-rows.txt`), and the selftest, default, usage and heavy-run stdout that the claims rest on.

## Not verified

- Line-number citations inside cells (e.g. `:154-160`, `:226-230`) — I did not trace each one; the behaviour they describe was checked.
- Row `round46-c2` and `round45-c2` clean-clone "measured" figures were reproduced on the clone for round45 only; `round46-c2`'s base-tip leg A was not re-run on a clone (the base revision `64ba8385` exists).
- The `REFUSE grader digest` exit-2 path of `tb2_grader_probe` (requires tampering with the captured grader) was not exercised.
