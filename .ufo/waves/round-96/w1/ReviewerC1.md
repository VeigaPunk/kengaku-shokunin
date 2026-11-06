# ReviewerC1 — R96-C1 review (multi-source-data-merger replay) at T 09717e49

**Verdict: R96-C1 verifies.** All four assigned checks pass at T. The two narrowings inherent to
the method (venv/sandbox modeling of the image and of uvx; pytest absent from the modeled grader
venv) are closed empirically at T; one temporal brittleness in counter leg L6 is routed to round 97
(F1, does not flip anything today). No frozen file changed; the frozen predicate reproduces
byte-exactly with freshly staged venvs.

## What I executed (receipts in `.ufo/waves/round-96/w1/ReviewerC1/`)

1. Independent probe run at T from the lane root (`python3 plans/round96_merger_probe.py --lane .
   --work <scratch> --env-venv E --grader-venv G`, E/G staged fresh today): 17/17 `ok=True`,
   `mismatches 0`, rc 0; `ENV_SIDE python,pandas,pyarrow,numpy 3.11.17 2.2.3 17.0.0 2.4.6` and
   `GRADER_SIDE python,pandas,pyarrow,numpy 3.13.16 2.3.3 22.0.0 2.5.4` — byte-identical to the
   official receipt `corpus/evidence/round96/merger-probe.txt` (`probe-rerun.txt`).
2. The frozen counter command from the claims (`cd` lane root; `python3 plans/round96_c1_replay.py
   --lane . --rev 09717e49… --work <scratch> --env-venv E --grader-venv G`):
   `LEGS L1=pass … L9=pass`, TARGET line exactly as frozen (executed_rows=40, cells
   file-artifact:31, serialization-schema:7, cases=17 legs=68 mismatches=0 defects=0),
   `PREDICATE R96-C1 pass`, rc 0 (`counter.txt`). The L6 rerun inside it reproduced the receipt's
   observation block and stamps from a `git archive` extract.
3. `sha256sum -c` of all 11 `frozen-instruments` rows at T: all OK (`frozen-shas.txt`).
4. All 17 `/app` trees staged with the probe's own `stage()` code (no reimplementation), then state
   dumped under both pandas sides (`state-grader.txt`, `state-env.txt`; `diff` = empty).
5. Real pytest 8.4.1 (grader venv) inside the probe's own bwrap recipe on **all 17** trees
   (`legs-vs-pytest.txt`; assignment named solve/C04/C12/C16 — I ran all).
6. The exact `tests/test.sh` stack (pytest 8.4.1 **+ pytest-json-ctrf 0.3.5**,
   `--ctrf /logs/verifier/ctrf.json`) in-sandbox on C01 and C12 (`uvx-stack.txt`).
7. `uv run -p 3.13 --no-project --with pytest==8.4.1 --with pandas==2.3.3 --with pyarrow==22.0.0
   --with pytest-json-ctrf==0.3.5` (test.sh's exact resolution set): numpy 2.5.4 — identical build
   to the receipt and to my G venv today.

No tools were installed or upgraded (uv, bwrap, pytest all already present; venvs are scratch).

## Check 1 — every variant produces the state its `why` states: 17/17 match

Solve's report (`C01` tree) holds **exactly 3 conflicts, all user 101**: `(101,name)` selected
"John Doe", `(101,email)` selected john@a.com, `(101,created_date)` selected 2024-01-15, each with
values from all three sources. Merged parquet: 4×5, `user_id int64`, `created_date` object strings,
rows 101/104 exactly as the grader asserts.

| case | state facts measured | why verified |
|---|---|---|
| C01 | both files, PAR1 magic, 3 conflicts | positive control ✓ |
| C02 | `/app` empty | existence asserts; both value tests FileNotFoundError ✓ |
| C03 | parquet intact, conflicts.json absent | merged independent of report ✓ |
| C04 | report `{total:1, [(101,name)]}` — **drops 2 of 3 conflicts** (email, created_date); `email_conflicts` empty → guarded check skipped; nothing counts conflicts | under-report passes P,P,P,1 ✓ |
| C05 | email conflict `selected=john@b.com` (source_b value) | guarded check runs and fails ✓ |
| C06 | rows 102/103 = `WRONG`/`wrong@x.com`, `status` column dropped (4 cols); 101/104 intact | only 101/104 content-checked ✓ |
| C07 | `user_id` **float64 read back from parquet** (101.0…), `set(df.user_id)=={101..104}` True, `df.user_id==101` selects 1 row | integer requirement unchecked ✓ |
| C08 | `user_id` object `'101'…`, set equality False | merged F ✓ |
| C09 | grader-side dtype **`datetime64[ns]`**, row value `2024-01-15 00:00:00`; `pd.Timestamp('2024-01-15') == '2024-01-15'` is False | datetime64 fails string equality ✓ |
| C10 | `created_date` = `2024/01/15` | exact string comparison fails ✓ |
| C11 | `total_conflicts=2`, list len 3 | length check fails ✓ |
| C12 | email conflict `values` keys `[source_b, source_c]` (source_a deleted) | grader indexes `values['source_a']` → KeyError ✓ |
| C13 | row 101 = john@b.com / 2024-01-10 (source_b) | user-101 checks fail ✓ |
| C14 | conflict `user_id` = `'101'` strings, zero int matches | conflicts F ✓ |
| C15 | 5 rows, 101 twice | row-count check fails ✓ |
| C16 | file magic `user` (CSV bytes); `ArrowInvalid: Parquet magic bytes not found in footer` | pyarrow refuses ✓ |
| C17 | `{total:0, []}` | `>= 1` check fails ✓ |

Env-side and grader-side pandas views of every tree are identical, so no dtype/round-trip
discrepancy hides between the two pinned pandas versions.

## Check 2 — harness's three direct calls equal pytest's verdicts: yes, 17/17

Real pytest 8.4.1 in the grader venv (3.13.16 / pandas 2.3.3 / pyarrow 22.0.0 / numpy 2.5.4),
inside the same bwrap recipe (`--unshare-all --clearenv`, `/app` rw, `/tests` ro), cwd `/app`,
against every staged tree:

- pytest rc 0 on exactly {C01, C04, C06, C07} — precisely the frozen reward=1 set; rc 1 on the
  other 13. Harness reward bit matches pytest rc on **17/17** (`REWARD_MISMATCHES 0`).
- Harness vector == frozen `predicted` on 17/17 (reproduces the receipt independently).
- Per-test binding (named functions, `-rA`): C02 → 3 FAILED (AssertionError + 2×FileNotFoundError);
  C04 → 3 PASSED; C07 → 3 PASSED; C09 → only `test_merged_data_exact_values` FAILED; C12 → only
  `test_conflict_report_values` FAILED (`KeyError: 'sou…'`); C16 → only
  `test_merged_data_exact_values` FAILED (`pyarrow.lib…`). Each harness leg maps to the same
  named function under pytest.
- Exact verifier stack **including pytest-json-ctrf 0.3.5** writing `/logs/verifier/ctrf.json`:
  C01 rc 0 (3 passed, 1 warning), C12 rc 1 (1 failed, 2 passed) — the plugin changes no verdict
  and no reward.

## Check 3 — agent-side venv fidelity and uvx drift

- Fresh venvs staged today match the receipt stamps byte-exactly (ENV_SIDE/GRADER_SIDE above), and
  L6 accepted them (stamp equality), so the receipt is reproducible on this host right now.
- test.sh's uvx set resolved **today** (2026-11-05) yields the identical stack (numpy 2.5.4,
  pytest 8.4.1, pandas 2.3.3, pyarrow 22.0.0). pandas/pyarrow/pytest/pytest-json-ctrf are pinned
  in test.sh; only numpy and the CPython micro float. So uvx at run time currently resolves no
  different numpy/pyarrow build; the exposure is purely temporal (see F1 for the counter's
  sensitivity to exactly this).
- Modeled-vs-image narrowings, none exercised by executed code: host `/etc` is not bound
  (solve.sh and all 15 variant scripts do pure pandas/json/parquet IO; bash runs non-login;
  `LANG=C.UTF-8`, `HOME=/tmp` set explicitly); the uv-managed CPython 3.11.17 stands in for
  python:3.11-slim's `/usr/local/bin/python` (image built 2025-10-31; nothing executed is
  micro-sensitive); the image's `PYTHONPATH=/app` and tmux/asciinema are absent (the harness
  builds `sys.path` itself; every python runs `-I`). [ANALYSIS: bounded by reading every executed
  script, not by strace-level proof — see gaps.]

## Check 4 — "the reward leg is the member's reward rule, not a narrowed scope": true

`tests/test.sh` contains exactly one verifier step: `uvx … pytest --ctrf /logs/verifier/ctrf.json
/tests/test_outputs.py -rA`, then writes `1`/`0` to `/logs/verifier/reward.txt` on pytest's rc.
The three functions in `test_outputs.py` are the entire verifier surface (no other test file is
invoked), and the probe's harness imports the captured `test_outputs.py` **unmodified** and calls
them in file order — no assertion is reimplemented. Combined with check 2 (pytest rc ≡ harness
reward on 17/17), the claims sentence stands as written.

## Counter and freeze integrity

- L1–L9 pass at T (`counter.txt`); L5 covers all 17 cases with no extras; L7 is member-set keyed
  (base set ⊆ rev set ∪ {member}, member absent at BASE) and pins `receipt`/`subject=tb2-header`/
  `verdict=cases`; ledger row measured: status executed, round 96, classes
  [file-artifact, serialization-schema], executed_total 40/88.
- `c1-tip.txt` at the live lane agrees: 9/9 legs, TARGET exact, `PREDICATE R96-C1 pass`, rc 0.

## Findings

- **FINDING R96C1-F1 minor** — L6 stamp equality is time-brittle through unpinned resolutions:
  `RERUN_STAMPS = (TOOL_SHA, CASE_TABLE_SHA, ENV_SIDE, GRADER_SIDE)` compares the full
  ENV_SIDE/GRADER_SIDE lines, which embed numpy and the CPython micro ("3.13.16 2.3.3 22.0.0
  2.5.4"), although `check_venv` pins only the python-prefix/pandas/pyarrow triples and the task
  itself leaves numpy unpinned. Any numpy or CPython micro release between measurement and a
  future fresh-venv re-verification makes `stamps_equal=False` → L6 fail → `PREDICATE R96-C1 fail`
  with zero behavioral change (the behavior-bearing pins — pandas, pyarrow, pytest — are exact).
  **Does not flip any verdict at T**: the exact frozen command passed today with venvs staged
  fresh (`counter.txt`, rc 0). Route to round 97: compare only the pinned triples in L6, or pin
  numpy/interpreter in the receipt and the stamp check.
- **FINDING R96C1-F2 info** — the `E:<ExceptionType>` leg labels are the harness's taxonomy, not
  pytest's: pytest marks C02's FileNotFoundErrors, C12's KeyError and C16's ArrowInvalid all as
  plain FAILED (per-test lines in `pytest-verbose.txt`). The predictions' wording "an error, not
  an assertion" describes harness labels; reward equivalence is unaffected (17/17 verified).
- **FINDING R96C1-F3 info** — sandbox/image modeling gap is real but unexercised: no `/etc`, no
  image interpreter, no tmux/asciinema/PYTHONPATH; inspection of every executed script shows no
  dependence on any of these.
- **FINDING R96C1-F4 info** — TARGET's `executed_rows`/`cells` are printed, not asserted (L7 is
  member-set keyed); the kill rule keys on the `PREDICATE` line and legs, so ledger growth cannot
  retro-flip C1. No action.

## Residual risks / verification gaps

- The real image (`alexgshaw/multi-source-data-merger:20251031`) and uvx-in-container were not
  executed (docker out of scope); equivalence rests on the exact pins plus the empirical pytest
  agreement above.
- The pytest-json-ctrf stack was exercised on 2 of 17 trees (one reward-1, one reward-0); the
  other 15 ran under bare pytest 8.4.1 in the grader venv.
- `/etc` absence was bounded by code inspection of executed scripts, not by syscall tracing.
