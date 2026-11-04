# SweepHarvestR82 — empirical harvest for R82-C3 (26 members at one tip)

Measured at lane tip `12f1029a45cf0097a3afd030d757bf93b87f8018` (== `master`, clean clone; base for before-states `a3a03ac31451e58f1742b9bccb73b72c2d90a95c`).
Two full passes; both completed. **Not partial.** Statuses and divergence counts agree on 26/26 members across passes (`DETERMINISM` hold); raw byte-hash agreement is 23/26 (pid/port/timing-bearing stdout is expected to differ and is not part of the determinism claim).

## Environment pin

```
$ python3 -V        -> Python 3.14.8   (command -v python3 -> /usr/bin/python3)
$ openssl version   -> OpenSSL 3.6.5 29 Sep 2026 (Library: OpenSSL 3.6.5 29 Sep 2026)
$ bwrap --version   -> bubblewrap 0.13.1
```

Tooling installs this seat: **none** (no pacman; nothing added to PATH).

## Method (exact)

- Driver: `/fast/scratch/hyaku/kengaku-r82/SweepHarvestR82/driver.py` (scratch), mirroring `plans/round82_c3_sweep.py` (in-flight at tip, read for semantics): projection regex `^(CASE |case=|TEST |VECTOR |LEG |regrade )`, drop `^cases=`/`OBSERVED-U`/`predicted=U`; run side = **stdout**; unrunnable precedence `receipt-absent` > `no-observations` > `exit!=0`; `reproduced` iff differing-lines==0 and exit equals the committed receipt's stamped `EXIT`.
- Per member: fresh `$S/work<r>/<member>/`, argv placeholders `<WORK>`->absolute work dir, `<MEMBER>`->member name; run with `cwd=<tip clone>`, `TMPDIR=<work dir>`, own process group; timeout 300 s (map declares no per-member timeout) with process-group SIGKILL on expiry (bwrap children hold pipes).
- Members ran **strictly sequentially** (pypi-server and nginx both bind port 8080); no run was parallelized.
- Clone tree reset (`git checkout -- .` + `git clean -fdq`, after `rev-parse --show-toplevel` assertion) before pass 2 and after any member that dirtied it; dirtiness after each member recorded in the JSON.

## Per-member results (pass 1; pass 2 in JSON)

| member | exit | secs r1/r2 | status draft | ndiff | obs lines | run receipt |
|---|---|---|---|---|---|---|
| build-pmars | 0 | 1.09 / 0.92 | `reproduced` | 0 | 22 | no |
| cancel-async-tasks | 0 | 161.65 / 161.63 | `reproduced` | 0 | 12 | yes |
| chess-best-move | 0 | 0.25 / 0.25 | `reproduced` | 0 | 12 | yes |
| circuit-fibsqrt | 0 | 53.21 / 53.20 | `reproduced` | 0 | 17 | no |
| configure-git-webserver | 0 | 52.71 / 52.74 | `reproduced` | 0 | 22 | no |
| constraints-scheduling | 0 | 11.38 / 11.83 | `reproduced` | 0 | 26 | no |
| db-wal-recovery | 0 | 0.87 / 1.22 | `reproduced` | 0 | 29 | no |
| distribution-search | 0 | 0.57 / 0.59 | `reproduced` | 0 | 12 | yes |
| feal-differential-cryptanalysis | 0 | 95.43 / 95.80 | `reproduced` | 0 | 13 | no |
| feal-linear-cryptanalysis | 0 | 3.21 / 3.16 | `reproduced` | 0 | 15 | no |
| git-leak-recovery | 0 | 1.15 / 1.13 | `reproduced` | 0 | 25 | no |
| hf-model-inference | 0 | 39.21 / 39.09 | `diverged:25` | 25 | 9 | yes |
| kv-store-grpc | 0 | 1.31 / 1.38 | `diverged:50` | 50 | 5 | yes |
| largest-eigenval | 0 | 2.31 / 2.41 | `reproduced` | 0 | 22 | yes |
| log-summary-date-ranges | 0 | 0.21 / 0.22 | `reproduced` | 0 | 12 | yes |
| nginx-request-logging | 0 | 16.97 / 16.97 | `unrunnable:no-observations` | 0 | 0 | yes |
| openssl-selfsigned-cert | 0 | 1.18 / 1.09 | `reproduced` | 0 | 12 | yes |
| password-recovery | 0 | 1.20 / 1.16 | `reproduced` | 0 | 17 | no |
| polyglot-c-py | 0 | 1.36 / 1.33 | `reproduced` | 0 | 19 | no |
| protein-assembly | 1 | 0.03 / 0.03 | `unrunnable:no-observations` | 0 | 0 | no |
| pypi-server | 0 | 18.54 / 18.49 | `diverged:6` | 6 | 4 | yes |
| regex-log | 0 | 0.04 / 0.03 | `reproduced` | 0 | 24 | no |
| sqlite-with-gcov | 0 | 10.51 / 10.57 | `diverged:30` | 30 | 5 | yes |
| torch-pipeline-parallelism | 0 | 41.64 / 42.30 | `unrunnable:no-observations` | 0 | 0 | yes |
| torch-tensor-parallelism | 0 | 67.84 / 64.63 | `diverged:10` | 10 | 10 | yes |
| vulnerable-secret | 0 | 0.20 / 0.20 | `reproduced` | 0 | 12 | yes |

## Status histogram (pass 1; pass 2 identical)

```
HISTOGRAM status reproduced=18 diverged=5 unrunnable=3 total=26
```

## Per-class histogram over ledger classes (executed rows, member×class)

```
HISTOGRAM-CLASS candidate-import=3 crypto-credential=2 db-state=1 file-artifact=18 filesystem-metadata=2 git-plumbing=1 network-service=4 numeric-band=2 process-environment=2 serialization-schema=1 shell-exec=1 signal-delivery=1 stdout-inspection=8 subprocess-exec=10 timing-wall=3 sum=59
```

## DETERMINISM

- Two passes at the same tip, fresh work dirs: **every member's status and divergence count agree (26/26)** — `DETERMINISM hold`.
- Divergence counts per member stable: hf-model-inference=25, kv-store-grpc=50, pypi-server=6, sqlite-with-gcov=30, torch-tensor-parallelism=10 in both passes.

## Members that did not reproduce — details

### hf-model-inference — `diverged:25` (exit=0, 39.21s)

First differing projection lines, verbatim (gate `DIFF` order: committed-receipt lines missing from the run first, then run lines absent from the receipt; no +/- markers are added):
```
CASE K1 case_sha256=e96b30e19244973e29bca6f64f4ec7d72045a8eb92fdffd00b1180e3af2ebd9e server_pid=3 sandbox_rc=0
VECTOR K1 expected=PPPP derived=PPPP agree=True
CASE K2 case_sha256=f030032303fd367d5aa0dc6c1517f8ef5d9c4b77eac517b6d79ceecd6032617b server_pid=3 sandbox_rc=0
```

Auxiliary: run receipt file projected against committed receipt: ndiff=16 (run-receipt observation lines=18).

### kv-store-grpc — `diverged:50` (exit=0, 1.31s)

First differing projection lines, verbatim (gate `DIFF` order: committed-receipt lines missing from the run first, then run lines absent from the receipt; no +/- markers are added):
```
CASE K1 observed=P/P/P/P/P/P/P expected=P/P/P/P/P/P/P server_pid=3721648 pid_before_legs=True server_ready=True server_log=SERVER_UP_5328
LEG K1 1 test_proto_file_creation P exc=- frag=-
LEG K1 2 test_grpc_tools_installation P exc=- frag=-
```

Auxiliary: run receipt file projected against committed receipt: ndiff=4 (run-receipt observation lines=45).

### nginx-request-logging — `unrunnable:no-observations` (exit=0, 16.97s)

Auxiliary: run receipt file projected against committed receipt: ndiff=12 (run-receipt observation lines=70).

### protein-assembly — `unrunnable:no-observations` (exit=1, 0.03s)

stderr tail (exact):
```
             ~~~~^^
  File "/fast/scratch/hyaku/kengaku-r82/SweepHarvestR82/clone/plans/tb2_grader_probe.py", line 145, in main
    import Bio  # noqa: F401  (fail loudly if Biopython is absent)
    ^^^^^^^^^^
ModuleNotFoundError: No module named 'Bio'
```

### pypi-server — `diverged:6` (exit=0, 18.54s)

First differing projection lines, verbatim (gate `DIFF` order: committed-receipt lines missing from the run first, then run lines absent from the receipt; no +/- markers are added):
```
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=1323016 wheel_sha256=6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6 stderr_sha256=268c02efc4bcdefb1d142a0f3e218eccf6429eaefea2f767a6dd664a90ffecb3
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=1367817 wheel_sha256=df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa stderr_sha256=9c7014b3b55bad773f6b5ac8bf950338e191a40f1ea7e002a25f7a9e1f2b4a58
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=1369862 wheel_sha256=b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92 stderr_sha256=6a0ccd86a8b5606aa190add39cd8095eb5346b71d2a39eb08200b77e58e777ef
```

Auxiliary: run receipt file projected against committed receipt: ndiff=6 (run-receipt observation lines=4).

### sqlite-with-gcov — `diverged:30` (exit=0, 10.51s)

First differing projection lines, verbatim (gate `DIFF` order: committed-receipt lines missing from the run first, then run lines absent from the receipt; no +/- markers are added):
```
CASE G1 observed=P/P/P expected=P/P/P build=coverage masked=yes gcda=2 gcno=2
LEG G1 1 test_sqlite_compiled P exc=- frag=-
LEG G1 2 test_sqlite_in_path P exc=- frag=-
```

Auxiliary: run receipt file projected against committed receipt: ndiff=0 (run-receipt observation lines=25).

### torch-pipeline-parallelism — `unrunnable:no-observations` (exit=0, 41.64s)

Auxiliary: run receipt file projected against committed receipt: ndiff=12 (run-receipt observation lines=12).

### torch-tensor-parallelism — `diverged:10` (exit=0, 67.84s)

First differing projection lines, verbatim (gate `DIFF` order: committed-receipt lines missing from the run first, then run lines absent from the receipt; no +/- markers are added):
```
CASE k1-ref case_sha=1537da2a2ea07293ec757641a0d2faee5e507518da9f96de45bebfd788193fc1 junit_sha=f05521d65e3f3415d541eccbd7041134a08c0d19b613bcf0b430e8438688946d rc=0 port_free=True
CASE k2-none case_sha=none junit_sha=8514dcb447735d7f158de5b2e71a3305b0cc3490c097223342e85cab42473caf rc=1 port_free=True
CASE k3-stub case_sha=316630cd45f0a3e2332bd38f98f4147977eba3d84aa54c5203edc5923986eadf junit_sha=eb9718c70be5d0b2c659e954f0046c6d49e7c5436467191a97bd21ee2e546303 rc=1 port_free=True
```

Auxiliary: run receipt file projected against committed receipt: ndiff=10 (run-receipt observation lines=10).

## Findings

1. **18/26 members reproduce exactly** (projection equal AND exit equals the stamped `EXIT`) — the frozen argv remain replayable at the tip for those.
2. **5 members diverge**: hf-model-inference (25 lines), kv-store-grpc (50), pypi-server (6), sqlite-with-gcov (30), torch-tensor-parallelism (10). Same counts in both passes; the divergences are byte-stable classes of difference, not flakiness. Notably `sqlite-with-gcov`'s **run receipt file** projects identical to the committed receipt (aux ndiff=0) while its stdout diverges by 30 — the stdout carries CASE/LEG lines that never reach its receipt, so for it the run-side source flips the verdict.
3. **3 members are unrunnable under the frozen projection**:
   - `protein-assembly`: exits 1 in 0.03 s — `ModuleNotFoundError: No module named 'Bio'` under bare `python3`; its committed receipt's `COMMAND` line shows the round-80 run used `uv run --no-project --with biopython python3 plans/tb2_grader_probe.py --lane .`, but the frozen map argv is the bare form. Code `unrunnable:no-observations`.
   - `nginx-request-logging` and `torch-pipeline-parallelism`: exit 0 and write a receipt file, but emit **zero** observation-form lines on stdout — their instruments print observations only into their `--receipt` file (the frozen argv redirects that into the sweep work dir). Under the gate's stdout-based projection both classify `unrunnable:no-observations`. The auxiliary receipt-file projection (`aux_receipt_file_projection` in the JSON) shows both run receipts DO carry observation lines (ndiff=12 each against the committed receipt), so the deciding factor is the gate's run-side source choice (stdout), not a dead instrument.
4. No member timed out; no member dirtied the measured tree in a way that survived the recorded reset (dirt-after counts in JSON).
5. Port 8080 collisions were avoided by the sequential order; kv-store-grpc/pypi-server/nginx all bound successfully in both passes.

## Evidence trail

```
Driver: python3 /fast/scratch/hyaku/kengaku-r82/SweepHarvestR82/driver.py   # two passes, incremental results_run{1,2}.jsonl
Clone:  git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin /fast/scratch/hyaku/kengaku-r82/SweepHarvestR82/clone  # HEAD=12f1029a45cf0097a3afd030d757bf93b87f8018
sha256(results_run1.jsonl) = fa046c4b8fb6132292c512ae00b1d86415d9e412fdae922ab006f010351e5afb  (19543 bytes)
sha256(results_run2.jsonl) = 4eb7912f21a27f274103e8a9d4f331e4f482612947ab18623f9170426ea40fec  (19541 bytes)
sha256(harvest.json) = 460140781a7811c02eb1bb0d9a78b69f20745f12ae4a9e6ea6c480f09cde135e  (53885 bytes)
```

Raw per-member records (argv, sha256 of stdout, stderr tails, aux receipt projection, determinism per member): `sweep-harvest.json` alongside this report. Scratch deleted on exit per lane rules; the two JSONL hashes above pin what was deleted.