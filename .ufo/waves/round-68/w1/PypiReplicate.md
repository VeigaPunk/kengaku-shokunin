# PypiReplicate — round 68, w1: second fresh battery against the frozen R68-C1 receipt of record

Seat: `PypiReplicate` (executor, wave `kengaku-r68-w1`). Claim exercised: **R68-C1** (coverage,
L0-capped at 7). This is the round-65 replication precedent applied to the round-68 re-freeze: one
independent second battery, in scratch, compared field-by-field against
`corpus/evidence/round68/pypi/receipt.txt`. The claims were read in full first; nothing in
`plans/round-68-claims.md` or any frozen file was edited, and no rule was changed.

## Binding identities (re-hashed from committed bytes at run time)

| artifact | sha256 |
|---|---|
| instrument `plans/round68_c1_pypi_finish.py` (PROBE) | `4a6fae5328e1cacd3b667fb59f50622d1602574a5763f741bda7dc0293b3fdfc` |
| base probe `plans/round63_c1_pypi_probe.py` (BASE-PROBE) | `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929` |
| grader `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` | `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c` (pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`) |
| receipt of record | `corpus/evidence/round68/pypi/receipt.txt`, sha256 `c6ed306e80bf01a36a35b8f0c38f0f9e13fdff276d53444ca03caecf20a665de` |
| replication receipt (this run) | `PypiReplicate-evidence/receipt-replicate.txt`, sha256 `b72a40e47964bfee3026f74ceac53c77547eb661651d7460d0159dbf71080f72` |

Frozen vector: `P/F/F/F`. All three shas above equal the values the receipt of record carries, and
all three were recomputed from committed bytes in this seat, not copied.

## Run conditions (measured, not assumed)

- Python 3.14.8 (`/usr/bin/python3`), bubblewrap 0.13.1 (`/usr/bin/bwrap`), uv 0.13.0 — same host
  state as the freeze. **No tool installed or upgraded by this seat**; nothing needed.
- Port 8080 precheck before the run: no listener (`ss -ltn | grep -c 8080` → 0). After the run: 0.
  The battery was run exactly once; no retry, no second start.
- Work dir: `/fast/scratch/hyaku/kengaku-r68/PypiReplicate/replicate` (14 MB, removed before yield).
- Scratch-only outputs: `--evidence-dir` pointed into scratch, so **nothing under
  `L/corpus/evidence/round68/pypi/` was written** — the record's receipt, battery-run, four captures
  and server log re-hash to the same shas before and after this seat (mtimes still 19:58–19:59).

## Command and in-runner exit

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
python3 plans/round68_c1_pypi_finish.py \
  --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
  --work /fast/scratch/hyaku/kengaku-r68/PypiReplicate/replicate \
  --receipt /fast/scratch/hyaku/kengaku-r68/PypiReplicate/replicate/receipt-replicate.txt \
  --evidence-dir /fast/scratch/hyaku/kengaku-r68/PypiReplicate/replicate/evidence
rc=$?   # → 0   (echoed as CLASS-PROBE-RC=0 into the run log: PypiReplicate-evidence/battery-run.txt)
```

Wall time 18.6 s. Output: `PREDICT K1=P K2=F K3=F K4=F`, `PREDICATE R68-C1 pass`,
`CLASS-PROBE-EXIT=0`, runner `rc=0`. No `SETUP` line was emitted.

## Comparison against the receipt of record

Full shas, as carried by the two receipts:

| receipt line | receipt of record | replication | equal |
|---|---|---|---|
| `PROBE sha256` | `4a6fae53…fdfc` | `4a6fae53…fdfc` | yes |
| `BASE-PROBE sha256` | `2ebaf54e…b929` | `2ebaf54e…b929` | yes |
| `GRADER sha256/pin` | `82c63517…0be4c` / `2fd12b88…6d6` | same / same | yes |
| K1 leg | `test_api` | `test_api` | yes |
| K1 observed / expected | `P` / `P` | `P` / `P` | yes |
| K1 exception | `none` | `none` | yes |
| K1 index_pid | `1323016` | `1402567` | **differs — expected (ephemeral pid, not a defect)** |
| K1 wheel_sha256 | `6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6` | same | yes |
| K1 stderr_sha256 | `268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3` | `83ed698ee0215e4067cec1e764470751a40923698a60011fbee8ffd3f1288f8a` | **NO — F2** |
| K2 leg / observed / expected | `test_api` / `F` / `F` | same | yes |
| K2 exception | `CalledProcessError` | `CalledProcessError` | yes |
| K2 index_pid | `none` | `none` | yes |
| K2 wheel_sha256 | `none` | `none` | yes |
| K2 stderr_sha256 | `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d` | same | yes |
| K3 leg / observed / expected | `test_api` / `F` / `F` | same | yes |
| K3 exception | `AssertionError` | `AssertionError` | yes |
| K3 index_pid | `1367817` | `1404174` | differs — expected |
| K3 wheel_sha256 | `df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa` | same | yes |
| K3 stderr_sha256 | `9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58` | `fe6f951b79b1162ba174e926d316f301abde00a9f3403b4fe84efc1599399caa` | **NO — F2** |
| K4 leg / observed / expected | `test_api` / `F` / `F` | same | yes |
| K4 exception | `CalledProcessError` | `CalledProcessError` | yes |
| K4 index_pid | `1369862` | `1404598` | differs — expected |
| K4 wheel_sha256 | `b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92` | same | yes |
| K4 stderr_sha256 | `6a0ccd86a8b5606aa190add39cd8095eb5346b71d2a39eb08200b77e58e777ef` | same | yes |
| `K1 server-log sha256` | `574c3a2f7594d05d45ab06526baa61fc36bcc3ee60ec04cc6716e88f1c47af28` | `5c5e424104a74c72be24ab3a7bbc5e4d7ededd1fbe12b63d40c173400a7242bb` | **NO — F3 (timestamp only)** |
| `served_simple` / `served_wheel` | `True` / `True` | `True` / `True` | yes |
| `K2 stderr-names-endpoint` | `True` | `True` | yes |
| `CLASS network-service executed` | `2` | `2` | yes |
| `PREDICTION-VECTOR` | `P/F/F/F derived=P/F/F/F` | `P/F/F/F derived=P/F/F/F` | yes |
| `PREDICATE R68-C1` | `pass` | `pass` | yes |
| `CLASS-PROBE-EXIT` | `0` | `0` (in-runner `rc=0`) | yes |

Beyond the receipt, the two run logs also agree on the request side: `SERVED K1 requests=2
paths=['/simple/vectorops/', '/packages/vectorops-0.1.0-py3-none-any.whl']` and `SERVED K4
requests=1 paths=['/simple/vectorops/']` are identical in both `battery-run.txt` files, and K2's
endpoint form is `urllib3-host-port` with `stderr_bytes=1526` in both.

## Findings

**F1 — the semantic core of the frozen predicate replicates exactly.** The `PREDICTION-VECTOR`
(including its re-derived `derived=` half) and all four `CASE` `observed`/`expected`/`leg`/
`exception` fields are identical, as are the K1 pid/wheel proof (pid present, 64-hex wheel) and the
wheel sha256 of every case that serves one. The frozen vector is reproduced by an independent
battery, not retyped: both runs print `PREDICT K1=P K2=F K3=F K4=F` from the same committed
`predict_legs()`.

**F2 — K1 and K3 stderr captures are not byte-stable across work paths; the divergence is one line,
and its cause is the grader's own printed `pip show` output.** `diff -u` of record vs replication
shows exactly one hunk with one `-`/`+` pair in each case:

```
-Location: /fast/scratch/hyaku/kengaku-r68/scored/venv/lib/python3.14/site-packages
+Location: /fast/scratch/hyaku/kengaku-r68/PypiReplicate/replicate/venv/lib/python3.14/site-packages
```

Capture sizes move 668→685 B (K1) and 1071→1088 B (K3), i.e. +17 B = the length delta between
`scored` (6 chars) and `PypiReplicate/replicate` (23 chars). Mechanism, from committed bytes:
`corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py:59-65` runs
`python -m pip show vectorops` inside `install()` and prints `Package info: {stdout}`; pip renders
`Location:` as the absolute site-packages path of the sandbox venv the probe created under `--work`.
The instrument captures the leg's combined output, so the capture is a function of the work path.
K2 stays byte-identical because its capture is pip's own stderr from `pip_install_stderr` (no
`pip show`), and K4 stays byte-identical because its leg fails inside `install()` before `pip show`
is reached. Diffs retained: `PypiReplicate-evidence/diff-K1.txt`, `diff-K3.txt`.

**F3 — the K1 server log is likewise single-run by construction.** Both logs are exactly 243 B and
carry the same three lines; masking the `http.server` timestamp field (`[...]`) makes the two
byte-identical (`diff` rc 0). Only the clock differs (`19:58:58` vs `20:00:38`). So the predicate's
`K1 server-log sha256` clause binds a clock-dependent artifact and can only ever match its own run.

**F4 — consequence for the checker: it refuses a replication receipt, on exactly the three path/clock
bindings, and on nothing else.** `python3 plans/round68_c1_pypi_finish.py --check-receipt
<PypiReplicate-evidence/receipt-replicate.txt>` exits 1 with:

```
CHECK defect server-log-sha  receipt 5c5e4241…42bb != committed 574c3a2f…af28
CHECK defect K1-stderr-sha   receipt 83ed698e…8f8a != committed 268c02ef…ecb3
CHECK defect K3-stderr-sha   receipt fe6f951b…9caa != committed 9c7014b3…4a58
CHECK defect exit-agreement  CLASS-PROBE-EXIT=0 want CLASS-PROBE-EXIT=1
CHECK defect stored-predicate pass != derived
CHECK stored-predicate=pass derived=fail
PREDICATE R68-C1 fail        (rc 1; full capture: PypiReplicate-evidence/check-on-replicate.txt)
```

Everything else in the strict checker passes on the replication receipt — PROBE, BASE-PROBE, GRADER
bytes/pin, the four CASE legs and vectors, the K1 pid and wheel, the K2 clause line, the CLASS line,
and the re-derived prediction vector. The last two defects are cascades of the first three (`derived`
is `fail` precisely because `failures` is non-empty), not independent disagreements. So this is not a
counter discrepancy: the receipt of record is consistent with its own bytes; the byte bindings are
simply bound to *a* work path and *a* clock. Reported, not fixed (claims are frozen; a seat that
thinks a rule is wrong reports it).

**F5 — the seat's stated expectation ("byte-stable captures") is true only in part.** Measured split:
K2 and K4 byte-identical; K1 and K3 differ by one path line each; the server log differs by the
timestamp alone. Any future replication precedent for this claim should expect `vector=match,
stderr-shas=diff` unless it reuses the record's exact work path.

## Limitation of this seat (named, not hidden)

`[INFERENCE]` A replication run whose `--work` path equals the record's (`…/kengaku-r68/scored`)
would reproduce the K1/K3 capture bytes exactly: the diffs show no difference other than the venv
path, and every other byte in those captures is deterministic (fixed-date hand-built wheel, pinned
pip, `PIP_CONFIG_FILE=/dev/null`). This was **not** tested: the seat spec allows exactly one battery
run, and running there would overwrite the L1's scored work dir. K2/K4 byte equality is measured, not
inferred.

## Drafts for the L1 (integrate, do not treat as edits)

Draft named-limitation addendum for R68-C1 (append-only, dated), if the L1 wants the replication
result on the record:

> **Replication (measured 2026-11-03, PypiReplicate, round-68 w1).** A second fresh battery of the
> frozen four cases reproduces the receipt of record's `PREDICTION-VECTOR` and all four `CASE`
> observed/expected/exception fields, and the K2/K4 stderr captures byte-for-byte. The K1/K3 stderr
> captures and the K1 server log do **not** re-hash equal outside the record's own work path, because
> the grader's `install()` prints `pip show` output carrying the sandbox venv's absolute `Location:`
> path and `http.server` stamps the log: byte equality of those three artifacts holds only for the
> run's own path and clock. `--check-receipt` consequently refuses a receipt produced at a different
> work path (three byte-binding defects plus their two cascades,
> `.ufo/waves/round-68/w1/PypiReplicate-evidence/check-on-replicate.txt`). The semantic clauses —
> vector, case legs, K1 pid/wheel proof, K2 endpoint clause, class line — are unaffected.

Draft row for the F2 mistakes ledger (`corpus/lessons/round-68.md` `## Mistakes`):

> byte-binding to environment-dependent output · the R68-C1 evidence binds three artifacts whose
> bytes encode the run's work path (K1/K3 captures via the grader's `pip show` `Location:`) and clock
> (K1 server log timestamps), so a replication receipt cannot satisfy `--check-receipt` elsewhere ·
> captured by `PypiReplicate`, `.ufo/waves/round-68/w1/PypiReplicate-evidence/{diff-K1,diff-K3}.txt` ·
> fix: bind normalized bytes (mask the venv path and log timestamps) or scope the clause to the
> semantic fields in a dated re-freeze.

## Compliance

- One battery run, exactly as specified; no retry (no `SETUP port-8080-occupied` occurred; port was
  free before and after).
- No writes in L except this report and `PypiReplicate-evidence/`; no writes at all under
  `corpus/evidence/round68/pypi/` (verified by sha256 before and after).
- No git/jj mutation, no `/tmp` use, no pacman, no installs, no delegation, no background jobs.
- Scratch `/fast/scratch/hyaku/kengaku-r68/PypiReplicate` deleted before yield; the receipts the L1
  needs were copied into `PypiReplicate-evidence/` first.

VERDICT: `REPLICATION vector=match stderr-shas=diff`
(vector and all CASE observed/expected fields identical; K2/K4 stderr byte-identical; K1/K3 differ by
exactly one `Location:` line each, explained by the grader's `pip show` on the run's venv path; K1
server log differs by timestamp only; index_pids differ as expected.)
