# Round 63 w1 — ClaimFalsifier critic (attacks on R63-C1, R63-C2, trio gate)

Lane: /home/vgpnk/Projects/shokunin/kengaku-shokunin. Lane HEAD `9ebde3a7`. Base commit `c78749a5`.
Frozen claims: `plans/round-63-claims.md`. Probe: `.ufo/waves/round-63/w1/build/round63_c1_pypi_probe.py`.
Gate: `.ufo/waves/round-63/w1/gate/gate_checks.py`. Drafted section: `.ufo/waves/round-63/w1/draft/depth/section.md`.
Evidence copies: `attack/evidence/` (c1/, c2/, trio/).

Host notes (observed, commands in the attacks below):
- Base hash. `git rev-parse --verify c78749a5` → `c78749a565dfd186f10a1d8ac98e19dac2429666` (40 hex).
  The frozen doc writes `c78749a5565dfd186f10a1d8ac98e19dac2429666` (41 hex, one extra `5`). The base
  bytes were taken from the 40-hex commit. The frozen doc has a typo; not edited (seat rule).
- No tools installed. No pacman. No git mutation. Scratch `/fast/scratch/hyaku/kengaku-r63/ClaimFalsifier`,
  removed at yield.
- Wait rule: all three targets present at the first check after the wait loop (build/pypi-probe.txt,
  gate/depth-before.txt, draft/depth/section.md); the loop ended on its own, exit 0.
- Port 8080: 0 listeners at start and after every attack I ran, except a transient occupant during
  one of my battery runs (see C1-A4).

---------------------------------------------------------------------------
## R63-C1 — probe attacks

### C1-A1 — foreign 404 listener on 8080, full battery
Setup: `python3 -m http.server 8080 --bind 127.0.0.1 --directory <empty dir>` as my service
`c1-foreign-404` (listener pid 1810998, child of my service shell 1810895). `curl` → `404`.
Command: `python3 <probe> --lane <L> --work <S>/c1/battery-under-404`
Output:
```
PREDICT K1=P K2=F K3=F K4=F
SETUP port-8080-occupied (K1 before start)
PROBE-RC=2
```
No receipt written. Listener killed via `proc://c1-foreign-404/kill`; `ss -ltn | grep :8080` → 0.
Verdict: **survives**. The probe refuses the battery (exit 2) rather than grading against a foreign service.

### C1-A2 — K2 leg itself under the 404 listener
Command: in-process call of the probe's own functions (`materialize_grader`, `ensure_venv`, `make_stub`,
`write_hosts`, `pip_install_stderr`, `stderr_names_endpoint`), with the 404 listener up.
Output:
```
port_listening() = True
pip rc = 1
stderr_names_endpoint = None
has Errno 111 = False | has Connection refused = False
probe K2 verdict would be: CONFOUNDED (SETUP exit 2)
stderr: ERROR: Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: none)
```
Verdict: **survives**. Two independent guards (endpoint name, `Errno 111`/`Connection refused`) would
each reject the 404 index as K2. The probe does not report K2 as P.

### C1-A3 — K1 pass from a pre-seeded venv (index not reached)
Attack: pre-install a correct `vectorops-0.1.0` wheel into the probe-owned venv, then run the full battery.
Command: `build_wheel(...)` + `pip install --no-index <wheel>` into `<S>/c1/preseed/venv`, then the probe battery.
Output (relevant lines):
```
preseed install rc: 0 ['Successfully installed vectorops-0.1.0']
CASE K1 ... observed=P ... index_pid=3976084 ...
SERVED K1 requests=2 paths=['/simple/vectorops/', '/packages/vectorops-0.1.0-py3-none-any.whl']
K2 ENDPOINT form=not-named stderr_bytes=0
SETUP K2 confounded: pip install SUCCEEDED during the quiet window -- a foreign service answered on 8080
RC=2   receipt written: no
```
Observation: pip still requested the probe's own index for K1 (2 served requests), so the K1 pass was
served by the lane index. The served-log guard (code lines 504-511) would raise
`K1 confounded` if no `/simple/vectorops` or `/packages/vectorops-0.1.0-` request had been served.
Verdict: **survives**. K1 P cannot come from the pre-seeded package without the lane index being contacted.
The run then aborted at K2 (see C1-A4), with no receipt.

### C1-A4 — intermittent K2 refusal (pip "succeeded" with no listener)
Runs and outcomes (all via `python3 <probe> --lane <L> --work <dir> [--receipt <file>]`):
- `repeat1-work`, `repeat2-work` (fresh dirs): `PREDICATE R63-C1 pass`, rc 0; K2 `F CalledProcessError`,
  `K2 ENDPOINT form=urllib3-host-port stderr_bytes=1526`. Receipts: `evidence/c1/repeat{1,2}-receipt.txt`.
- `rerun-work` (fresh dir): `SETUP K2 confounded: pip install SUCCEEDED during the quiet window`, rc 2, no receipt.
  stderr_bytes=0. The K2 CASE line was not printed before the abort.
- preseed run (C1-A3): same K2 abort, rc 2, no receipt.
- instrumented run `instr` (fresh module): `SETUP port-8080-occupied (K1 before start)`, rc 2.
  Immediately after, `ss -ltnp | grep :8080` → none, and no `http.server` process was visible (`ps`).
- instrumented run `instr3` (fresh module, `--work` new): full pass, `PREDICATE R63-C1 pass`, K2 `F`
  with `[pip-K2] rc=1 listening-at-call=False`, `Connection refused` in pip's stderr; venv emptied by uninstall after every case.
- earlier (executor's) runs in `build/`: `pypi-probe-attempt1.txt` → fail (K2 stderr names no endpoint;
  the probe now matches a second endpoint form); `pypi-probe-rerun.txt` and `pypi-probe.txt` → pass.

Analysis: a K2 pip success with empty stderr needs a correct `vectorops` reachable at the moment of the
call. My replay of K1 then uninstall (`k1-replay`) and the instrumented run showed the venv clean after
K1, so a stale install is ruled out for `instr3`. The refusals coincide with a port occupant seen
in `instr` (transient). **[INFERENCE]**: a transient foreign index on 8080, probably from a sibling seat
(the roster lists peers coordinating 8080). I did not confirm the owner (no process attribution available).
Verdict: **survives** on the predicate (no false P; each abort writes no receipt and exits 2), but the
probe is **not repeatable** across runs: 3 of 6 non-deliberate full-battery attempts in this seat refused with SETUP (two K2 aborts, one port-8080-occupied at K1 start).
Defect: an abort is reported as "a foreign service answered", which the probe cannot attribute.

### C1-A5 — index served from the probe's own directory; index_pid is a probe-started PID (code read)
Code: `build_case_index(case, case_dir)` writes into `case_dir/index`; `start_server(index_dir)` runs
`[sys.executable, -m, http.server, 8080, --bind, 127.0.0.1, --directory, index_dir]` via `Popen`
(lines 399-403); `index_pid = str(proc.pid)` (line 490); `stop_server(proc)` kills only that `proc`
(lines 415-428). `require_port_free` before every server start (line 488).
Verdict: **survives** (code). Confirmed by observed `index_pid=` values that match the PIDs of
the servers started in each run.

### C1-A6 — forged receipt through `--check-receipt` (the counting command)
Attack: copy a real receipt, set `index_pid=1` and `wheel_sha256=aaaa…` (64 a's), and check it.
Command: `python3 <probe> --check-receipt <forge1-fake-pid-and-sha.txt>`
Output:
```
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=aaaaaaaaaaaa...
CHECK stored-predicate=pass derived=pass
PREDICATE R63-C1 pass
rc=0
```
Controls, same command: `forge2-k2-observed-P.txt` → `CHECK fail K2 observed P != F`, rc 1;
`forge3-no-k2-stderr-line.txt` → `CHECK fail k2-stderr (line missing)`, rc 1;
`forge4-short-sha.txt` → `CHECK fail K1 wheel_sha256 not a sha256: abc`, rc 1.
Verdict: **falsified** for the counting command. `--check-receipt` re-derives text fields only: it does
not check that `index_pid` is a live probe-started PID, nor that the wheel sha matches the served bytes.
The live run path is sound (C1-A5); the receipt re-check is not evidence of a run by itself.

### C1-A7 — probe built-in selftest
Command: `python3 <probe> --selftest --work <S>/c1/selftest`
Output: `SELFTEST toy=correct observed=P expected=P exception=none` / `SELFTEST toy=absent observed=F
expected=F exception=CalledProcessError` / `SELFTEST pass`, rc 0. Verdict: **survives**.

### C1-A8 — committed receipt at the path the predicate names
Command: `test -e corpus/evidence/round63/pypi-probe.txt`. Output: absent (only `control-k2.txt` present in that dir).
Verdict: **not-run** (committed receipt not yet integrated by L1).

---------------------------------------------------------------------------
## R63-C2 — depth table attacks

### C2-A1 — drafted section on base + section.md
Command: `python3 .ufo/waves/round-63/w1/gate/gate_checks.py depth --skill <S>/c2/SKILL.md --receipt corpus/evidence/round62/class-survey.txt --root <L>`
(`SKILL.md` = `git show c78749a5:SKILL.md` + `section.md`.)
Output:
```
ROWS n=16 class_match=True count_mismatch=0 paths total=24 resolved=24 share=1.00
PREDICATE R63-C2 pass
```
Verdict: **survives** on the frozen predicate.

### C2-A2 — degenerate path cell `./` (and `/`) on every row
Command: rewrite the last cell of all 16 rows of section.md to `` `./` `` (and separately `` `/` ``), gate as in C2-A1.
Output:
```
=== i-root-pointer-all-rows rc=0: ROWS n=16 class_match=True count_mismatch=0 paths total=3 resolved=3 share=1.00 | PREDICATE R63-C2 pass
=== i-slash-pointer-all-rows rc=0: (same) PREDICATE R63-C2 pass
```
Also `` `.` `` (bare dot, no `/`) → `rc=1 ... row-pointer=...:no-path-token ... PREDICATE R63-C2 fail` (correct).
Verdict: **falsified**. A table whose receipt pointers all name the lane root passes: the path check
accepts directory tokens that resolve trivially, and the share check then only sees 3 prose tokens.
The predicate does not require a receipt file. Not a listed kill rule (every row still carries a
resolving pointer token), but the claim's "a resolvable receipt path" is not what the gate measures.

### C2-A3 — one count off by one (`signal-delivery` 1 → 2)
Command: replace `| signal-delivery | 1 |` with `| signal-delivery | 2 |`, gate.
Output: `ROWS n=16 class_match=True count_mismatch=1 ... DETAIL count-mismatch=signal-delivery:got=2,want=1 ... PREDICATE R63-C2 fail`, rc 1.
Verdict: **survives** (kill rule "count cell mismatch → miss" fires as designed).

### C2-A4 — all 16 rows named `file-artifact` (count 76)
Command: rewrite each row's class/count cells.
Output: `ROWS n=16 class_match=False count_mismatch=0 ... DETAIL missing-classes=candidate-import,...,+5more ... PREDICATE R63-C2 fail`, rc 1.
Verdict: **survives**.

### C2-A5 — row contents against `executed17.lst` and the census members
Command: per row, `members ∩ corpus/evidence/round52/graders/executed17.lst` vs the executed column.
Output: 16/16 rows consistent with the frozen rule (executed ⇔ ≥1 member on the list), except
`network-service`, which has 0 members on the list (pypi-server only: the frozen rule's C1 branch).
Verdict: **survives**, with the `network-service` executed label valid only if C1 passes (which holds
in my runs, C1-A4).

### C2-A6 — receipt pointers resolve, and are committed
Command: for each pointer token: `git -C <L> ls-files --error-unmatch <token>`.
Output: 23 of 24 tokens tracked. `.ufo/waves/round-63/w1/build/pypi-probe.txt` (the `network-service`
pointer) → `tracked=False` (it is an untracked wave file).
Verdict: **falsified** for that row. The pointer resolves only in the working tree and is a wave file,
not the committed receipt the claim names (`corpus/evidence/round63/pypi-probe.txt`, not yet present).
Fix for L1: point the row at the committed receipt once it lands.

### C2-A7 — base SKILL.md (before) and the gate's own selftest
Commands: `gate_checks.py depth --skill <S>/SKILL.base.md ...` → `ROWS n=0 ... section-absent ... PREDICATE R63-C2 fail`, rc 1.
`gate_checks.py selftest --work <S>/selftest` → `SELFTEST GOOD rc=0 ... SELFTEST BAD-COUNT rc=1 ... SELFTEST NO-SECTION rc=1 ... SELFTEST pass`, rc 0.
Verdict: **survives** (before-state matches `depth-before.txt`, the selftest passes).

---------------------------------------------------------------------------
## Trio gate attacks

### T-A1 — `verified-at:` before `source:` (requested fixture 1)
Command: `gate_checks.py trio <S>/trio/t1-verified-before-source.md` → `TRIO fail missing=verified-at`, rc 1.
Verdict: **survives** (expected fail).

### T-A2 — three keys after a `## ` heading (requested fixture 2)
Command: `gate_checks.py trio <S>/trio/t2-keys-after-heading.md` → `TRIO fail missing=source,verified-at,recheck`, rc 1.
Verdict: **survives** (expected fail).

### T-A3 — correct file (requested fixture 3)
Command: `gate_checks.py trio <S>/trio/t3-correct.md` → `TRIO pass`, rc 0.
Verdict: **survives** (expected pass). Requested expected verdicts fail, fail, pass: all three met.

### T-A4 — keys with empty values
Command: `gate_checks.py trio <S>/trio/a1-empty-values.md` (`source:`/`verified-at:`/`recheck:` with no values) → `TRIO pass`, rc 0.
Verdict: **falsified** (in spirit). The gate tests key presence and order only. A trio with empty values passes.
The frozen rule states presence and order, so this is literal behaviour, not a kill-rule breach.

### T-A5 — keys inside a code fence
Command: `gate_checks.py trio <S>/trio/a4-keys-in-codefence.md` → `TRIO pass`, rc 0.
Verdict: **falsified** (same class as T-A4): a fenced example passes as provenance.

### T-A6 — keys past line 12, and indented keys
Commands: `a2-keys-past-line12.md` → `TRIO fail missing=source,verified-at,recheck`, rc 1;
`a3-indented-keys.md` → `TRIO fail missing=source,verified-at,recheck`, rc 1.
Verdict: **survives** (both fail as the frozen window rule says).

### T-A7 — red on the round-62 census entry (the mistake)
Command: `gate_checks.py trio corpus/knowledge/tb2-grader-class-census.md` → `TRIO fail missing=verified-at,recheck`, rc 1.
Verdict: **survives** (red as frozen). Matches `gate/trio-red.txt`.

### T-A8 — green on the new entry
Command: `test -e corpus/knowledge/tb2-network-service-offline-grader.md` → absent.
Verdict: **not-run**. The fix counts only with both red and green; green not yet possible.

---------------------------------------------------------------------------
## Tally
- Survives: 16 (C1: A1, A2, A3, A4, A5, A7 = 6; C2: A1, A3, A4, A5, A7 = 5; trio: T-A1, A2, A3, A6, A7 = 5).
- Falsified: 5 (C1-A6; C2-A2; C2-A6; T-A4; T-A5).
- Not-run: 2 (C1-A8 committed receipt; T-A8 green on new entry).
- Total: 23 attacks (C1 8, C2 7, trio 8). C2-A7 covers the base-depth check and the gate selftest as one attack.

## Kill rules
- R63-C1 kill rule 1 (K2 returns P → claim dead): **does not fire**. No recorded K2 leg returned P.
  Two aborted runs (rerun-work, preseed) did not print the K2 leg value before SETUP; they wrote no receipt.
- R63-C1 kill rule 2 (K1 returns F → miss): **does not fire**. K1 returned P in every run that reached it
  (repeat1, repeat2, instr3, build, build-rerun, my rerun, preseed).
- R63-C1 kill rule 3 (probe reaches a foreign service on 8080 → predicate fails): **condition suspected,
  not confirmed** in the two K2 aborts (C1-A4, [INFERENCE] transient listener). The predicate did not pass in
  those runs (exit 2, no receipt). Consequence held; owner not attributed.
- R63-C2 kill rules (count mismatch; resolution < 90 %; rows without receipt pointer): **do not fire** on the
  drafted section (count_mismatch=0; share 1.00; all 16 rows carry a pointer). Defect flagged, not a listed rule:
  the `network-service` pointer is an untracked wave file (C2-A6).
- Trio: no kill rule; the fix needs the new entry, which is absent (not-run).

## Summary for L1
1. Fix the `network-service` pointer to the committed round-63 receipt once it exists (C2-A6).
2. C1 is not repeatable: 3 of 6 non-deliberate full-battery attempts here refused with SETUP (two K2 aborts, one port-8080-occupied). Investigate the
   transient 8080 occupant before counting C1 as scored; the probe's refusal is safe, but the run is unreliable.
3. `--check-receipt` is text-only (C1-A6): the counting command does not verify PID or sha. Do not cite it
   as independent evidence of a run.
4. The frozen base hash in `plans/round-63-claims.md` has 41 hex characters; the commit is `c78749a565dfd186f10a1d8ac98e19dac2429666`.
