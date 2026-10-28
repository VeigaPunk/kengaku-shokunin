# C2ExecRegistryAudit — round 52, wave 1

## Result

Audited the **46 actual data rows** in `SKILL.md`'s `## Gate/probe registry` at the frozen base reference `30801b479e3418c11089b8586178b6960216f364`. All 46 referenced entry files exist. Four verdict cells omit reachable exit codes; the `order-check` self-test cell triggers the frozen counter despite accurately saying the entry has no `--selftest` flag. The `gate-flip-check` row was checked separately because the counter parser drops it.

No lane source files were edited. No tools were installed. No build, lint, formatter, or test suite was run.

## Findings and corrected cells

1. **`build-pmars-probe` — omitted exit 1.** The entry advertises `--smoke`; `plans/build_pmars_probe.py:278-283,317` returns 1 when smoke output is not `Results: 12 34 78` (0 on success). Existing verdict map lists only 0 and 2.

   Corrected verdict cell:
   > `0` every case yielded four verdicts (the receipt's `match=` column carries prediction agreement) · `1` `--smoke` only: the sandbox did not produce the expected `Results: 12 34 78` output · `2` setup (capture digest, `bwrap` or `gcc` missing, a case without four verdicts)

2. **`mutant-direction-check` — omitted exits 2 and 3.** `plans/mutant_direction_check.py:104,114` return 2 for setup refusal/failure; `:176` returns 1 for a mislabel, 3 for split legs or invalid mutants, and 0 otherwise. Existing cell describes only 0 and 1.

   Corrected verdict cell:
   > `0` every frozen mutant's declared kill direction is observed or unwitnessed · `1` a `MISLABELLED` mutant · `2` usage/setup refusal or setup failure · `3` the independent legs disagree or a mutant is invalid

3. **`sources-adopt` — omitted exit 1.** `plans/sources_adopt.py:50-58` defines success 0 and exit codes 2–9. Its main dispatches `--selftest` at `:1016`; failed self-test cases return 1 at `:969`. Existing map lists 0 and 2–9.

   Corrected verdict cell:
   > `0` gates an append and prints the append block · `1` self-test failed · `2` usage error or unreadable quote artifact · `3` staged/registry id collision · `4` malformed staged row (escaped pipe, column count, quote spans) · `5` requested id absent · `6` quote over the 25-word cap · `7` quote absent from artifact bytes · `8` quote bound to a mismatched URL · `9` quote has no url-map entry

4. **`round38-c2` — omitted argparse exit 2.** `plans/round38_c2_verify.py:257-261` uses argparse and `:276` returns 0/1 for verdicts. The invocation `python3 plans/round38_c2_verify.py --bogus` returned exit 2. Existing map lists only 0 and 1.

   Corrected verdict cell:
   > `0` `checks=7 defects=0` then `PREDICATE C2 pass` · `1` any `Vn DEFECT` (a check that raises is a defect) · `2` argparse usage

5. **`order-check` — counter-triggered self-test association, not an unsupported flag on the entry.** `plans/order_check.py:143-145` accepts `--lane`, `--claims`, and `--receipt`; it has no `--selftest`. The cell explicitly says no self-test exists and correctly names external falsifiers: `plans/round40_c1_verify.py` contains O04/O12/O14 at lines 209, 215, and 219. However, the frozen C2 counter extracts that one external `.py` path and all flags in the entire cell (`--selftest`, `--receipt`, `--claims`), then checks those unrelated flags against the verifier file. All are absent, so the counter reports `SELFTEST-UNBACKED 1 (`order-check`)`. This is also inconsistent with the frozen claims' rule that a cell saying the instrument has no self-test is accepted; the counter implementation has no such exemption.

   Corrected self-test cell (makes the entry/external verifier association explicit; preserves the existing falsifiers and measurements):
   > No `--selftest` flag is defined by `plans/order_check.py`; falsifiers are external — `plans/round40_c1_verify.py` mutants `O04` (`rc-silence`), `O12` (`rc-error`), `O14` (`error`), each witnessed pre-freeze (`.ufo/waves/round-40/claims/witness/`), and the measured controls `--receipt corpus/evidence/round39/git-leak-probe.txt` → `ORDER FAIL freeze-contains-receipt receipt-before-claims hits=0`, exit 1; `--claims plans/round-99-claims.md` → `ORDER ERROR claims not committed in HEAD`, exit 2

## Counter/parser observations

- Frozen counter invocation measured: `ADVERTISED total=72`; `REGISTERED total=44 rows=46`; `MISSING 28`; `INCOMPLETE 0`; `ENTRY-MISSING 0`; `SELFTEST-UNBACKED 1` (`order-check`); predicate fail.
- `gate-flip-check` is an actual row (SKILL.md line 609), but its verdict cell includes escaped `fired\|not fired`. The counter's `split("|")` yields nine cells, so `parse_rows` drops it. Thus `rows=46` is not a count of the 46 actual data rows: it includes the table header and omits `gate-flip-check`.
- `coverage-census` points to the existing `corpus/evidence/round13-coverage/coverage_census.py`, but the counter's CMD regex only permits `[A-Za-z0-9_]+` for that directory segment; the hyphen means the entry is not extracted. The same regex is used for advertised commands, so this path is invisible to both extraction sets.
- `gate-flip-check` was checked separately: `plans/gate_flip_check.py` exists; `main` accepts `--lesson` and `--selftest` at lines 724-743; check verdict returns 0/1 at line 518, self-test returns 0/1 at 721, setup returns 2 at 743. No factual discrepancy found there.
- Other self-test cells that mention entry-probe flags alongside a separate verifier (for example `db-wal-probe`) contextualize those flags as belonging to “the probe”; they are not reported as factual errors. The C2 checker’s whole-cell regex can nevertheless associate such mentions with the other script named in the cell.

## Commands and evidence

Executed from `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

```sh
python3 plans/round52_c2_registry.py --lane .
```

Measured result: `ADVERTISED total=72`, `REGISTERED total=44 rows=46`, `MISSING 28`, `INCOMPLETE 0`, `ENTRY-MISSING 0`, `SELFTEST-UNBACKED 1` (`order-check`), `PREDICATE R52-C2 fail`.

Usage-exit measurement command (all five invocations returned 2):

```sh
export TMPDIR=/fast/scratch/hyaku/kengaku-r52/C2ExecRegistryAudit/tmp
for c in "plans/round38_c2_verify.py --bogus" "plans/round37_c2_verify.py --bogus" "plans/round39_c2_verify.py --bogus" "plans/round41_c2_verify.py --bogus" "plans/round44_c2_verify.py --bogus"; do
  printf "%-45s " "$c"; python3 $c >/dev/null 2>&1; echo "exit=$?"
done
```

Static evidence was read from the cited source line ranges (no edits): `plans/round52_c2_registry.py:20-194`, `plans/build_pmars_probe.py:278-350`, `plans/mutant_direction_check.py:86-182`, `plans/sources_adopt.py:50-58,930-975,1000-1085`, `plans/round38_c2_verify.py:256-280`, `plans/order_check.py:138-152,180-215`, `plans/round40_c1_verify.py:200-225`, and `plans/gate_flip_check.py:710-748`. Additional temporary Python extraction commands enumerated entry paths, main return expressions, registry cells, and argparse flags; their outputs were confined to this seat's scratch directory.

## Files and cleanup

- Produced `/fast/scratch/hyaku/kengaku-r52/C2ExecRegistryAudit/audit.json` (structured findings and evidence) and temporary extraction files under the same scratch directory. Per scratch discipline, the directory is removed before yield; the JSON findings are reproduced above.
- Persistent report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-52/w1/C2ExecRegistryAudit/report.md`.

No blockers. No installs or updates.