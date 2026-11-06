# ExecC1Rerun — independent re-measurement of R96-C1

Seat: ExecC1Rerun. Clone: `--shared` lane clone detached at T `09717e49ff46fad5b255619d671aaaae52dfc180`, toplevel verified.

## Venvs (staged fresh this seat, not reused from L1)

- E (agent side): `python 3.11.17 pandas 2.2.3 pyarrow 17.0.0 numpy 2.4.6`
- G (grader side): `python 3.13.16 pandas 2.3.3 pyarrow 22.0.0 numpy 2.5.4`
- Matches receipt `ENV_SIDE`/`GRADER_SIDE` stamps character-for-character (including numpy — resolved by pip from the same uv cache / index state; exact resolved versions coincide with the L1 receipt).

## Counter results

| rev | rc | result |
|---|---|---|
| T `09717e49` | 0 | `LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass` / `TARGET executed_rows=40 member=multi-source-data-merger cells=file-artifact:31,serialization-schema:7 set_contains_base=1 located=1 executed=1 cases=17 legs=68 mismatches=0 defects=0` / `PREDICATE R96-C1 pass` |
| BASE `45740a61` | 1 | fails (all 9 legs fail; defects 9; no receipt/instruments at BASE) |
| F `be3ff962` | 1 | fails (7 defects; receipt absent at F, rerun obs=17 vs want=0) |

BASE and F both fail rc=1 as required. T passes rc=0.

Command used verbatim per seat spec (from cwd `$S/lane`):
`python3 "$S/lane/plans/round96_c1_replay.py" --lane "$S/lane" --rev <rev> --work "$S/w" --env-venv "$S/E" --grader-venv "$S/G"`

## Probe, 3 runs + alt-numpy

Ran `plans/round96_merger_probe.py` 3 times: all rc=0, byte-identical to each other. Observation blocks (17 `CASE` lines) identical to committed `corpus/evidence/round96/merger-probe.txt`. Full-file diff vs receipt: only `LANE_TIP` differs (T vs F — expected; receipt stamped at F before C landed, L1's c1-tip run at T re-stamps via the counter). All other stamps (shas, ENV/GRADER_SIDE, HOST_BASH/USERNS, SANDBOX, LEG_ORDER) identical.

Alt-numpy run (E numpy 2.1.3, G numpy 2.3.1): rc=0, OBS identical to the receipt's 17 vectors. Different numpy does **not** change any vector in this instrument (numpy is unpinned in the task image on both sides; the grader uses pandas/pyarrow paths unaffected here).

## Predicate character check

My c1-T output line 1+2+3 matches the frozen predicate text in `plans/round-96-claims.md` character-by-character:
- `LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass`
- `TARGET executed_rows=40 member=multi-source-data-merger cells=file-artifact:31,serialization-schema:7 set_contains_base=1 located=1 executed=1 cases=17 legs=68 mismatches=0 defects=0`
- `PREDICATE R96-C1 pass`
Also char-identical to L1's `.ufo/waves/round-96/L1/c1-tip.txt` first 3 lines (`diff` clean).

## Findings

- R96-C1 re-measured independently: **pass** at T with freshly staged venvs; rc 1 at BASE and F as frozen.
- No defect found that would flip the verdict. Numpy drift does not move any observed leg.

FINDING none

## Receipts

- `.ufo/waves/round-96/w1/ExecC1Rerun/c1-T.txt` (rc=0)
- `.ufo/waves/round-96/w1/ExecC1Rerun/c1-BASE.txt` (rc=1)
- `.ufo/waves/round-96/w1/ExecC1Rerun/c1-F.txt` (rc=1)
- `.ufo/waves/round-96/w1/ExecC1Rerun/probe-1.txt`, `probe-2.txt`, `probe-3.txt` (rc=0)
- `.ufo/waves/round-96/w1/ExecC1Rerun/probe-alt.txt` (rc=0, alt numpy)
- This report: `.ufo/waves/round-96/w1/ExecC1Rerun/report.md` (also serving as the `Report:` trailer file `.ufo/waves/round-96/w1/ExecC1Rerun.md` — see note)

Note: seat spec assigns Report trailer to `.ufo/waves/round-96/w1/ExecC1Rerun.md` and the wave-dir contents to `.../w1/ExecC1Rerun/`. This file is the wave-dir report; the trailer file is a separate path (see below).

## Tool installs

None. Used pre-installed `uv` only.
