source: S228 — TB2 pypi-server grader at pin 2fd12b88 (https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/pypi-server/tests/test_outputs.py), tier A code
verified-at: 2026-11-03 (base c78749a5; the freeze commit is named in the round report)
recheck: python3 plans/round63_c1_pypi_probe.py --check-receipt corpus/evidence/round63/pypi-probe.txt

# TB2 `pypi-server` — a network-service grader replayed offline against a lane-built PEP 503 index

## What the grader asserts

The grader is Terminal-Bench 2.0 task `pypi-server`'s `tests/test_outputs.py` at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6`: sha256 `82c63517…650be4c` — `corpus/evidence/round52/graders/SHA256SUMS` line 134 (the row `./pypi-server/tests/test_outputs.py`); the wrapper `tests/test.sh` is line 135, `d2b1220e…86e7784e`. The lane's committed capture `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py` and this round's re-fetch `.ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py` (3177 bytes) carry that same digest. `test_api()` (S228 line 66) calls `install()` (line 13) then asserts on the imported package. `install()` runs three commands of interest:

```
python -m pip uninstall -y vectorops                                              # S228 line 23
python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0  # S228 lines 24-32
python -m pip show vectorops                                                      # S228 line 58
```

The `--index-url` is the hardcoded literal `"http://localhost:8080/simple"` (S228 line 30) and the version pin the literal `"vectorops==0.1.0"` (S228 line 31). The four assertions are, verbatim, S228 lines 85-88:

```
assert v.dotproduct([1, 1], [0, 1]) == 1
assert v.dotproduct([1, 1, 0], [1, 1, 0]) == 2
assert v.dotproduct([1, 1, 0, 0], [1, 0, 0, 21.2]) == 1
assert v.dotproduct([1, -1, 0, 0.01], [0, 0, 10, 0]) == 0
```

with `import vectorops as v` at S228 line 83. The contract has three separable parts: the package must install from a **loopback index on port 8080** at exactly version **0.1.0**, and the installed module must expose `dotproduct` with exactly the semantics above.

## Why this is `network-service` class

The round-62 census receipt prices `pypi-server` into the `network-service` class: `corpus/evidence/round62/class-survey.txt` line 11 — `CLASS network-service count=8 members=filter-js-from-html,git-multibranch,headless-terminal,hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server` (`CLASS container-image count=0` is line 18). The class is not a judgement call: the census's frozen detector is the regex `\bsocket\.|\brequests\.(get|post)\b|\burllib\b|http\.client|\burlopen\b|localhost:[0-9]|127\.0\.0\.1` (`plans/round62_c1_class_survey.py` line 93), and the grader's own line 30 carries the literal `localhost:8080`. It cannot be replayed as a file-artifact grader: its install step reaches a served endpoint, and that endpoint's content — the wheel it serves — decides whether the grader passes. At base, `network-service` had **no executed grader**: the coverage line (`corpus/evidence/round62/class-survey.txt` line 21) reads `EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12 classes-uncovered=network-service,process-environment,db-state,container-image`, and the roster `corpus/evidence/round52/graders/executed17.lst` holds 17 names, `pypi-server` not among them (`grep -c pypi-server corpus/evidence/round52/graders/executed17.lst` → 0).

## The do-nothing control (K2), run before the freeze

Before the freeze the lane ran the grader's `test_api` with the venv on PATH and **nothing listening on 8080**. Receipt: `corpus/evidence/round63/control-k2.txt` (sha256 `73f1fa33…59100c9`), line 5:

```
CONTROL-LEG test_api F CalledProcessError Command '['python', '-m', 'pip', 'install', '--index-url', 'http://localhost:8080/simple', 'vectorops==0.1.0']' returned non-zero exit status 1.
```

last line `rc=0` (the capture run succeeded; the grader leg inside it failed). The control's meaning is narrow and load-bearing: with no index the install step fails with `CalledProcessError`, so `test_api` is **F** for a reason that names `localhost:8080` in the captured pip stderr. The round's counter is therefore not already met by the control — the control demonstrates the failure mode, not the capability.

## The probe's sandbox design

`plans/round63_c1_pypi_probe.py` (frozen design at `plans/round-63-claims.md` lines 39-43; the instrument landed this wave at `.ufo/waves/round-63/w1/build/round63_c1_pypi_probe.py`) runs the grader's **own** `test_api()` — never a copy, never a rewrite — inside a **bwrap** sandbox against a **lane-built simple index**:

- the grader is byte-verified at run time against `GRADER_SHA256` and bound read-only at `/tests/test_outputs.py`; a byte drift is a SETUP error, never a run;
- the index is a PEP 503 layout (`/simple/<normalized-name>/`) served by the probe itself on `127.0.0.1:8080`, carrying exactly one wheel, `vectorops-0.1.0`, built by the probe from frozen literal sources — the probe owns the bytes the grader installs, so the leg is a replay, not a download;
- the sandbox's `python` is a **probe-owned venv**: the venv is bound read-only (interpreter and pip immutable) with its `site-packages` re-bound writable (the install target is not), under `env -i` with `PIP_CONFIG_FILE=/dev/null` — no host pip config, no host credentials, no host site-packages enter the graded process; a **loopback-only `/etc/hosts`** is written and bound, so the sandbox has no host resolver;
- network is **shared, not unshared**, because the leg must reach `127.0.0.1:8080`. The probe bind-tests the port before every server start and refuses (`SETUP port-8080-occupied`, exit 2) rather than grading against a foreign service; it kills only the PID it started, and only after recording it; and K2 is refused as confounded unless pip's own words are "Connection refused", so a foreign index answering and 404-ing cannot pass for the quiet window;
- the expected leg vector is **derived at run time** from the case declarations (served versions, math correctness) and compared to the frozen vector, never retyped as a literal.

## The frozen leg vector

`plans/round-63-claims.md` lines 45-54 freeze four cases and the leg rule (P iff `test_api()` returns normally; F on any exception):

| case | setup | frozen leg |
|---|---|---|
| K1 compliant | index on 127.0.0.1:8080 serves `vectorops-0.1.0` with a correct `dotproduct` | **P** |
| K2 do-nothing control | nothing listening on 8080; no index | **F** |
| K3 wrong math | index serves `vectorops-0.1.0` whose `dotproduct` returns `sum(a*b)+1` | **F** (AssertionError) |
| K4 wrong version | index serves only `vectorops-0.2.0` | **F** (`CalledProcessError` from install) |

Frozen leg vector over K1–K4: **P/F/F/F**. The predicate (`plans/round-63-claims.md` lines 56-59) is pass iff the observed vector equals P/F/F/F **and** K2's captured pip stderr names `localhost:8080` **and** K1's receipt records the index server's own PID and the served wheel's sha256. The kill rules are equally frozen: K2 returning P kills the claim (the target is reachable with nothing listening — the counter or the grader reading is wrong; the claim is reported dead, not patched); K1 returning F is an honest miss with no re-freeze this round.

## The index layout is PEP 503, and the spec says so in the open

The layout is not an ad-hoc convention; it is **S229 — PEP 503 "Simple Repository API"**, `https://peps.python.org/pep-0503/`, tier A (spec; scope: the `/simple/<name>/` index layout the probe serves — `plans/round-63-claims.md` line 142). The spec's own words, located in this round's own copy of the bytes (`.ufo/waves/round-63/w1/recon/S229-pep-0503.html`, sha256 `5b97cb7e…2c453c4f`), line 165:

> Below the root URL is another URL for each individual project contained within

and line 167:

> is replaced by the normalized name for that project, so a project named

with line 166's `The format of this URL is /<project>/`. That is the layout contract the probe's index implements: a root URL, then one URL per project, named by the project's **normalized** name — here the single segment `vectorops`, served at `/simple/vectorops/`.

## NOT claimed

- **No claim about the unfetched upstream `test.py` simulator.** The lane captured `tests/test_outputs.py` and `tests/test.sh` (SHA256SUMS lines 134-135); the task's own `test.py` simulator — the harness the grader is meant to run against — was not fetched, not opened, and is not characterized here.
- **No claim that the grader is solvable by any model.** This entry prices a **replay**: the probe stands up the index the grader expects and reads the grader's verdict. It says nothing about whether a model can pass `pypi-server`, and no solvability judgement is implied by the K1 leg being P.
- **No claim about the host's 8080 beyond the bind test.** The only host facts used are the round-start measurement that no listener occupied 8080 and the probe's own bind of that port. What the grader's index would have reached had the probe not bound the port is out of scope.
- **No claim that the census's other seven `network-service` graders are replayable.** Only `pypi-server` was executed; the other seven remain unexecuted.

## Results

The probe receipt (written by the build seat) is `.ufo/waves/round-63/w1/build/pypi-probe.txt` (sha256 `b3d3ec1f…c5038db9eb`). Its CASE lines, quoted verbatim:

```
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=795645 wheel_sha256=6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6
CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=none wheel_sha256=none
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=959703 wheel_sha256=df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=967177 wheel_sha256=b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92
```

and its PREDICATE line, quoted verbatim:

```
PREDICATE R63-C1 pass
```

The observed leg vector over K1–K4 is therefore **P/F/F/F**, equal to the frozen vector, and
the frozen predicate line reads `PREDICATE R63-C1 pass`. The receipt's own supporting lines
record `K2 stderr_mentions_8080=True` (the K2 pip stderr names the endpoint), the coverage
counter line `CLASS network-service executed=1`, and
`PREDICTION-VECTOR P/F/F/F derived=P/F/F/F`.

**One rendering fact, measured, that a re-checker needs.** The K2 clause is satisfied by pip's
**urllib3 host/port rendering**, not by the contiguous literal. The captured K2 pip stderr
names the endpoint as `NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed
to establish a new connection: [Errno 111] Connection refused")` — `host='localhost'` and
`port=8080` as two separate fields, with the literal string `localhost:8080` appearing **0**
times in that stderr. pip 26.2.1 writes the index URL to **stdout**
(`Looking in indexes: http://localhost:8080/simple`), not stderr. The probe therefore matches
two endpoint forms (`ENDPOINT_PATTERNS`, `url` and `urllib3-host-port`); the requirement — the
captured pip stderr names localhost port 8080 — is unchanged, only its rendering is. Recorded
because a re-check that greps the **stderr** alone for the contiguous literal will read
`False` here and mis-report a passing predicate as failing. Measured first-hand in this seat:
`grep -c 'localhost:8080'` → 0 on the stderr, `grep -c 'port=8080'` → 5, and the URL present
once on stdout (evidence kept beside this entry as `corpus/evidence/round63/k2-pip-stderr.txt`
and `k2-pip-stdout-repro.txt`).

The receipt's PIDs are from one battery run and differ between runs (later runs of the same
probe produced different `index_pid` values, the same wheel digests); the verdict lines were
identical across every run observed this round.
