# C2ControlsR72 — round 72 w1 (controls: both self-tests + C2 mutant matrix)

- Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- Tip at every run: `b6336136e0e891522b113a94d8e0bd65e0eae8de` (freeze commit; `git diff --quiet HEAD -- <instruments, SKILL.md, round-71-claims.md>` rc 0)
- Instruments (working-tree sha256 == `HEAD` blob sha256, verified by piping `git cat-file -p HEAD:<path>` through sha256sum):
  - `plans/round72_c2_routed_defects.py` = `2d81ad806cb3177463f013d5a5390cf7c4162fc99bd19dd86a1ceec437c78758`
  - `plans/round72_c1_hf_probe.py` = `99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e`
- Tool installs/upgrades: **none** (no need; bwrap 0.13.1, python 3.13.16, `/fast/ComfyUI/.venv` present as pinned by the instrument).

## Assignment executed

1. Scratch created at `/fast/scratch/hyaku/kengaku-r72/C2ControlsR72` (`mkdir -p`; removed at end, see §Scratch).
2. `python3 plans/round72_c2_routed_defects.py --selftest --work <S>/st > corpus/evidence/round72/c2-controls.txt 2>&1` → **RC=0**
3. `python3 plans/round72_c2_routed_defects.py --mutants --work <S>/mu >> corpus/evidence/round72/c2-controls.txt 2>&1` → **RC=0** (wall 2.68 s)
4. `python3 plans/round72_c1_hf_probe.py --lane . --selftest --work <S>/c1st --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock > corpus/evidence/round72/c1-selftest.txt 2>&1` → **RC=0** (wall 2 m 38.766 s)
5. `python3 plans/round72_c1_hf_probe.py --lane . --work <S>/ctl --receipt <S>/c1-control-replicate.txt --control --port-lock …/port5000.lock` → **RC=0** (wall 81.00 s)
6. Diffed the replicate control receipt against `.ufo/waves/round-72/c1-control.txt` (L1's `--control` receipt).

All commands ran from the lane cwd. Port 5000 was observed held by another seat's `python3` at 23:09; every battery call passed `--port-lock`, and the selftest's green battery reported `setup=0`.

## The four tallies, verbatim

| # | source | line as printed | RC |
|---|---|---|---|
| 1 | `corpus/evidence/round72/c2-controls.txt` | `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True parser-arm=True ok=True` | 0 |
| 2 | same file (mutant section) | `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1` | 0 |
| 3 | `corpus/evidence/round72/c1-selftest.txt` | `SELFTEST red_refused=8/8 accept_ok=1 state_sensitive=1 path_independent=1 ok=True` | 0 |
| 4 | replicate control run | `CONTROL cases=9 derived_set=FFFF predicate=fail counter_refuses_do_nothing=True` | 0 |

Also printed, verbatim: `MUTANTS` ARM line `ARM accept-green=ok refuse-red=ok attribution=ok`; C2 `DEFECTS-RED n=3 codes=E1a,E1b,E2 want=E1a,E1b,E2`; C1 control's `PREDICATE R72-C1 fail`.

**No required arm failed to print.** C1 selftest printed all eight refusal arms (`vector_flip`, `legs_flip`, `coverage_flip`, `drop_case`, `case_digest`, `drop_k9`, `provenance_env`, `provenance_path`), `ARM accept genuine rc=0 accepted=True`, and `ARM STAGED-STATE changes_on_byte=True PATH-INDEPENDENT sha_equal=True`. C2 printed all seven `MUTANT` lines plus `ARM` and totals.

## Evidence artifacts (written, then verified)

| path | sha256 | size |
|---|---|---|
| `corpus/evidence/round72/c2-controls.txt` | `f8e7fa370a52710b08c100f5cadf0f9efd6da74b7961a0c114208f54bbc61bcd` | 25 lines / 1143 B |
| `corpus/evidence/round72/c1-selftest.txt` | `e24edb7054efeba12f41c3e7fecd50c6632d1b6107af32e8f94675f06fafd69b` | 62 lines / 2814 B |
| scratch green receipt (deleted with scratch; content summarised below) | `fa060b7fa2e4adbf8f0d4de180bea2d66bc7598ed5f13dbcfcf6093b7c224087` | 3494 B |
| scratch control replicate (deleted with scratch; byte-identical to the wave file below) | `16d78eaed2934b0baf5b2324b20212317ebde376fa79a5e9aae44747bb7893e7` | 48 lines / 3976 B |

### C1 selftest — green battery inside the arm

All nine frozen vectors matched before the tamper arms ran:

```
CASE K1 derived=PPPP rc=0 exc=[]     CASE K6 derived=PFFF rc=0 exc=['test_api_error_handling', 'test_sentiment_endpoint']
CASE K2 derived=PPFP rc=0 exc=[]     CASE K7 derived=FPPP rc=0 exc=[]
CASE K3 derived=PPFP rc=0 exc=[]     CASE K8 derived=FPPP rc=0 exc=[]
CASE K4 derived=PPPF rc=0 exc=[]     CASE K9 derived=PPPF rc=0 exc=[]
CASE K5 derived=PFPP rc=0 exc=[]
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2
PREDICATE R72-C1 pass
```

Provenance and binding lines in that green receipt:

```
REV b6336136e0e891522b113a94d8e0bd65e0eae8de
PROBE sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e
PROBE_BLOB sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e rev=b6336136e0e891522b113a94d8e0bd65e0eae8de
LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2
PROVENANCE env_cleared=True allowlist=PATH,HOME,LANG,PYTHONPATH,PYTHONNOUSERSITE,PYTHONWARNINGS,TMPDIR,HF_HUB_OFFLINE,TRANSFORMERS_OFFLINE allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0 transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py
```

Each refusal arm was substantive, not a stub rejection: the checker printed `DEFECTS n=` 4, 1, 1, 5, 1, 5, 2, 2 for `vector_flip`, `legs_flip`, `coverage_flip`, `drop_case`, `case_digest`, `drop_k9`, `provenance_env`, `provenance_path` respectively; the genuine receipt gave `DEFECTS n=0` / `PREDICATE R72-C1 pass` and was accepted (`rc=0`). The `case_digest` arm ran with `--work` (R71-R4's repair) and produced a one-defect digest mismatch.

### C1 control replication vs L1's receipt

`diff -u .ufo/waves/round-72/c1-control.txt <replicate>` → **empty, diff rc 0**. Both files: 48 lines, 3976 bytes, sha256 `16d78eaed2934b0baf5b2324b20212317ebde376fa79a5e9aae44747bb7893e7`. The replicate therefore reproduces the L1 control **byte-for-byte**: nine `VECTOR … derived=FFFF agree=False`, `LEG-COVERAGE legs=4 seen_p=0 seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=9 setup=0 exc=18`, `PROVENANCE … allowlist_seen=9/9 distinct=1 canary_seen=0 transformers_file=/venv/…`, `PREDICATE R72-C1 fail`.

Note the control receipt carries the *same* provenance witness as a real battery (the sandbox is exercised even when the app is do-nothing), which is the intended separation: provenance tests the harness, vectors test the case.

### Supplementary cross-check (not an assigned receipt)

`python3 plans/round72_c2_routed_defects.py --lane .` at the same tip printed `E1a ok / E1b ok / E1c ok / E2 ok / DEFECTS n=0 / PREDICATE R72-C2 pass`, **RC=0** (captured to scratch only, reported here). This confirms the live lane the fixtures imitate is the passing lane.

## Supplementary measurement — C2 mutant × fixture sensitivity matrix

The instrument prints only `escapes=1` per killed mutant. I reconstructed the full matrix from the instrument's own `MUTANTS`/`build_reds`/`fixture_verdict` in scratch (no instrument edit; rc 0 = fixture accepted, 1 = refused):

```
FIXTURES     GREEN E1a-cols E1a-owner E1b-paraphrase E1b-norev E2-top E2-trailing E2-moved
PRISTINE     0     1        1         1              1         1      1           1
M1-columns   0     0        1         1              1         1      1           1   escapes=['E1a-cols']
M2-owner     0     1        0         1              1         1      1           1   escapes=['E1a-owner']
M3-labels    0     1        1         0              1         1      1           1   escapes=['E1b-paraphrase']
M4-revisions 0     1        1         1              0         1      1           1   escapes=['E1b-norev']
M5-position  0     1        1         1              1         1      1           0   escapes=['E2-moved']
M6-last-sec  0     1        1         1              1         1      0           1   escapes=['E2-trailing']
M7-null      0     1        1         1              1         1      1           1   escapes=[] null=True
```

Attribution (fixtures still refused per check group) is untouched for unrelated checks:

```
M1 E1a:1/2 E1b:2/2 E2:3/3     M4 E1a:2/2 E1b:1/2 E2:3/3
M2 E1a:1/2 E1b:2/2 E2:3/3     M5 E1a:2/2 E1b:2/2 E2:2/3
M3 E1a:2/2 E1b:1/2 E2:3/3     M6 E1a:2/2 E1b:2/2 E2:2/3
                              M7 E1a:2/2 E1b:2/2 E2:3/3
```

Each semantic mutant has exactly one witness fixture, and the six witnesses are distinct; no mutant perturbs a fixture outside its target check. This is stronger than the printed `escapes=1` conveys and directly supports "attributes every kill".

## Findings (report-only; no frozen rule, case, vector, digest or target was edited)

1. **C2 `ARM` line is partly a constant, not a measurement (display defect).** `run_mutants` prints `accept-green=ok` and `attribution=ok` as literals; only `refuse-red` is conditional (`ok` if killed else `none`). The underlying accept-green/attribution measurements are enforced only through `invalid=0` (each failed sub-arm increments `invalid`, drops `killed` below 6, and fails the totals predicate). So the metric is fail-closed, but the ARM line alone cannot evidence an accept-green or attribution failure — the same overclaim shape R71-R7 was routed for. Suggested successor: derive all three tokens from the counters.
2. **C2 "killed" means "at least one target red escaped".** With multiple reds per target (E1a 2, E1b 2, E2 3) `killed` fires on one escape. My matrix shows the metric is nonetheless fully attributed here because each mutant rewrites one clause and exactly one fixture witnesses it. A mutant that changed a check while leaving *all* its target reds red would count `survived` only if its verdict vector differs from pristine somewhere; if the vector is identical everywhere it is counted `null`, i.e. indistinguishable from the deliberate no-op. The predicate (`null_detected==1`) fails in that case, so this is fail-closed but mislabels an undetected semantic mutant as null.
3. **C1 `env_cleared=True` / `cleared_env=True` are format-string constants, not re-derived measurements.** Evidence: `battery_lines` writes both unconditionally; the selftest's `provenance_env` arm only proves the *checker* reads the field when a receipt is tampered. Actual isolation evidence is `canary_seen=0` (planted `R72_CANARY` is invisible) plus `allowlist_seen=9/9`, `distinct=1`, `transformers_file` under `/venv/`. Dropping `--clearenv` alone would be caught by the canary; dropping `--clearenv` *and* `canary_env()` would still print `env_cleared=True`. This is the R71-R7 class in the witness field, not in the predicate.
4. **C1 `SUMMARY` clause is prefix-matched, so the `exc=` tail is unconstrained.** `check_receipt` requires the substring `SUMMARY cases=9 legs=36 mismatches=0 setup=0`; the green battery's `exc=2` (K6 connection exceptions) rides along. A receipt with any other `exc=` value would still satisfy the summary clause and the predicate does not count `exc`. Fine for the frozen predicate as written; a successor should decide whether exception count is a clause.
5. **C1 `allowlist_seen` numerator is all-or-none.** `all_allow` is one boolean ("every case's env keys ⊇ every allowlisted name"); the numerator is therefore 9 or 0. It is a conservative (fail-closed) encoding, but it cannot express "8 of 9 names seen" and the printed `9/9` reads as per-variable-per-case granularity it does not measure.
6. **C2 gate has no self-blob binding (unlike C1's `PROBE_BLOB`).** C1's receipt binds its own source to `HEAD` (`PROBE sha == PROBE_BLOB sha == 99867c7f…`). C2's gate re-reads lane files but never digests `plans/round72_c2_routed_defects.py` against the commit, and `--mutants` mutates its own *working-tree* text. At my run the tree was clean and file sha equals the `HEAD` blob, so this run is sound; a future dirty tree would score uncommitted bytes with no receipt clause catching it.
7. **Control byte-identity is deterministic but not self-evidencing of independence.** The replicate equals L1's receipt exactly, including `server_pid=-` in all nine cases and no timestamp/seed field. The receipt alone therefore cannot distinguish a second execution from a copy; the independence witness is the shell record (separate `--work` tree, separate receipt path, 81 s wall) plus the scratch tree's mtimes. This is a limitation of the comparison, not a defect in the control.
8. **No staging escape or `/tmp` use observed.** The sandbox binds `--tmpfs /tmp`; neither instrument calls `tempfile`; all fixtures/receipts landed under `--work` in my scratch (`du` 1.3 MB before deletion). Port 5000 was contended at start but every case ran under the shared flock with `setup=0`.

## Arms and calibration verdict for this seat

- C2 self-test: fake lane reds all three fixture-driven checks (`defects-in-fake=3`), corrected fake passes (`all-fail=True`), append-only, positional and parser arms all true → the gate distinguishes the two routed defect shapes and the R71-R5 false-red class. RC 0.
- C2 mutant matrix: 7 mutants, 6 semantic kills with distinct one-fixture witnesses, 0 survivors, 0 invalid, no-op detected as null → the R71-R5-invariant metric is replaced by a discriminating one. RC 0.
- C1 self-test: 8/8 tampered receipts refused with substantive defect counts, genuine accepted, staged digest state-sensitive and path-independent → R71-R4's dead arms are live. RC 0.
- C1 control: nine do-nothing cases all `FFFF`, counter refuses (`fail`), and the receipt reproduces L1's byte-for-byte. RC 0.

No arm is red; the tallies match the frozen predicate strings in `plans/round-72-claims.md` exactly.

## Scratch and write scope

- Scratch used: `/fast/scratch/hyaku/kengaku-r72/C2ControlsR72` (`st/`, `mu/`, `c1st/`, `ctl/`, `matrix/`, replicate receipt, logs); **deleted** before this report was finalised. Shared `port5000.lock` and sibling seat directories under `/fast/scratch/hyaku/kengaku-r72` were left untouched (not mine).
- Lane writes: only `corpus/evidence/round72/c2-controls.txt`, `corpus/evidence/round72/c1-selftest.txt` (both assigned) and this report. No fleet-root tracked file, no `.ufo/state/`, no `.scratch/`, no `corpus/` path outside the two assigned receipts, no git/jj mutation, no `agent://all`.
- `/tmp`: nothing written by this seat (sandbox `/tmp` is a bwrap tmpfs; no `tempfile` use).

## Blockers

None.
