# PypiProbeBuild — R63-C1 instrument (`plans/round63_c1_pypi_probe.py`)

Seat: PypiProbeBuild (r63 w1, build). Deliverable: the probe file only. The L1 copies it
into `plans/`; nothing else in the lane was written.

Files written (all under the seat dir):
- `.ufo/waves/round-63/w1/build/round63_c1_pypi_probe.py` — the instrument, 32897 bytes,
  sha256 `2ebaf54ea427475f2f897304b7d31f6bea26eb4e5074a759447f0f710919b929`
- `.ufo/waves/round-63/w1/build/pypi-probe.txt` — scored receipt (battery, final bytes),
  sha256 `b3d3ec1f2da5ff3fec73b47b33b4e3398391d2c4853c2320c270b4c5038db9eb`
- `.ufo/waves/round-63/w1/build/pypi-probe-rerun.txt` — second battery (final bytes),
  sha256 `fc7908686b5810a43750c8577df9e07ef37ac604c7137558854b082997df2d40`
- `.ufo/waves/round-63/w1/build/evidence/` — the raw artifacts below

## Verdicts

| check | command | result |
|---|---|---|
| selftest | `python3 …/round63_c1_pypi_probe.py --selftest --work <scratch>/selftest` | `SELFTEST toy=correct observed=P expected=P` / `toy=absent observed=F expected=F exception=CalledProcessError` / `SELFTEST pass`, **exit 0** |
| battery | `… --lane …/kengaku-shokunin --work <scratch>/battery --receipt …/pypi-probe.txt` | `PREDICT K1=P K2=F K3=F K4=F`, legs `P/F/F/F`, `PREDICATE R63-C1 pass`, **exit 0** |
| check-receipt | `… --check-receipt …/pypi-probe.txt` | `CHECK ok cases=4 vector=P/F/F/F`, `PREDICATE R63-C1 pass`, **exit 0** |
| rerun | same, `--work <scratch>/battery-rerun --receipt …/pypi-probe-rerun.txt` | identical vector `P/F/F/F`, `PREDICATE R63-C1 pass`, **exit 0**; agrees with the first |
| lane cleanliness | `git -C <lane> status --porcelain` | only the pre-existing wave untracked entries (`?? .ufo/waves/round-63/frontier/`, `?? …/w1.ready`, `?? …/w1.ready.dispatched`, `?? .ufo/waves/round-63/w1/`); nothing from the battery |

Both receipts carry the same GRADER line, the same `observed` vector and the same three wheel
shas; only `index_pid` differs (a PID is the OS's, and both runs were fresh servers). Equality
of the parts the predicate rests on, `diff`-checked:
`diff <(grep -o 'observed=[PF]' pypi-probe.txt) <(grep -o 'observed=[PF]' pypi-probe-rerun.txt)`
→ no output. The K1 and K3 wheel shas differ (`6fad8ea8…` correct vs `df8d66ab…` wrong-math)
while both were fetched from the *same* path `/packages/vectorops-0.1.0-py3-none-any.whl` — the
served bytes, not the filename, are what your grader saw. K3's access log and K1's are byte-
identical except the timestamp, which is the point: the same request path, different content.

Receipt of record (`pypi-probe.txt`):
```
GRADER sha256=82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c pin=2fd12b88aafdd04a52c298e3940bcb189f9766d6
CASE K1 leg=test_api observed=P expected=P exception=none index_pid=795645 wheel_sha256=6fad8ea86492def2ce9bb48ba80c11e2b35ce88d8d2ea3757c276754c9d0ced6
CASE K2 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=none wheel_sha256=none
CASE K3 leg=test_api observed=F expected=F exception=AssertionError index_pid=959703 wheel_sha256=df8d66ab40465261894ca5f17b354a3b079061303e12e97f9fc7d1d1393c07aa
CASE K4 leg=test_api observed=F expected=F exception=CalledProcessError index_pid=967177 wheel_sha256=b97edcfcd8870426abed8d8100aab73ad26f022ed4a32d6756b7d6b1c4f9fe92
K2 stderr_mentions_8080=True
CLASS network-service executed=1
PREDICTION-VECTOR P/F/F/F derived=P/F/F/F
PREDICATE R63-C1 pass
CLASS-PROBE-EXIT=0
```

## What the instrument does (and the four facts it had to discover)

Byte-verifies the grader against `GRADER_SHA256` (mismatch → `SETUP grader-sha-mismatch`,
exit 2), binds it read-only at `/tests/test_outputs.py` in bwrap, builds the wheel by hand
with `zipfile`, serves a PEP 503 index from `python3 -m http.server 8080 --bind 127.0.0.1
--directory <index>`, and runs `test_api()` in a probe-owned venv.

Four constraints were measured, not assumed:

1. **Resolver.** `env -i` with no `/etc` leaves libc without name resolution and pip dies on
   `NameResolutionError(... Failed to resolve 'localhost' ([Errno -3] ...))` even though the
   port is open. The probe writes a loopback-only `127.0.0.1 localhost` hosts file and binds
   it at `/etc/hosts`. No host `/etc` enters the sandbox.
2. **Writable install target.** The spec's `--ro-bind <work>/venv` alone makes the grader's own
   `pip install` fail with `OSError: [Errno 30] Read-only file system:
   .../site-packages/vectorops` — indistinguishable from a wrong-index failure. The venv is
   bound read-only and its `lib/pythonX.Y/site-packages` re-bound writable, so interpreter and
   pip are immutable while the install target is not. This is a deviation from the item's
   literal mount list, taken because the literal form cannot place a K1 P; it is declared in
   the module docstring.
3. **K2's stderr rendering.** pip 26.2.1 never prints the URL form `localhost:8080` when the
   connection is refused; it prints urllib3's endpoint form,
   `HTTPConnection(host='localhost', port=8080)`. A literal `"localhost:8080" in stderr`
   detector therefore reports a **false negative on evidence that plainly names the endpoint**
   — that is what the first battery did (`predicate fail` with all four legs correct). The
   detector now accepts either the URL form or the quoted-host/port pair on one line, prints
   which form matched (`K2 ENDPOINT form=urllib3-host-port`), and rejects host-only,
   port-only, split-line, other-host, other-port and `port=80800` strings (unit-checked).
   The receipt line stays byte-exact `K2 stderr_mentions_8080=True`.
4. **A foreign service is indistinguishable from absence without a request-side record.** The
   port is contended this wave: a foreign `python3 -m http.server 8080 --directory /tmp`
   repeatedly appeared mid-run. Two hardening steps, both with live evidence in `evidence/`:
   - K1 requires the probe's own server **access log** to contain a `/simple/vectorops` and a
     `vectorops-0.1.0` wheel fetch (200). K4's log shows only `/simple/vectorops/`, which is
     exactly why it fails.
   - K2 is refused as confounded unless pip's own words are connection-refused (`Errno 111`)
     and pip did not succeed. This caught a real confound live: a foreign index answered
     `/simple/vectorops/` with a wheel href that 404'd
     (`ERROR: HTTP error 404 while getting http://localhost:8080/simple/vectorops/…whl`).
     Without that guard that run would have recorded K2=F with "mentions 8080" — a false green.

## Negative controls (check-receipt re-derivation)

`--check-receipt` parses the receipt's own lines and re-derives; it prints the stored verdict
separately (`CHECK stored-predicate=… derived=…`) and never obeys it. Mutations of the passing
receipt, each → exit 1 with the named failure:

| mutation | failure printed |
|---|---|
| K1 → F | `K1 observed F != P`, `observed-vector F/F/F/F != P/F/F/F` |
| K2 → P (the kill rule) | `K2 observed P != F`, `observed-vector P/P/F/F != P/F/F/F` |
| K3 → P | `K3 observed P != F` |
| stderr_mentions → False | `k2-stderr K2 stderr_mentions_8080=False` |
| K1 `index_pid=none` | `K1 index_pid empty` |
| K1 `wheel_sha256=none` / 64 non-hex | `K1 wheel_sha256 not a sha256: …` |
| CLASS line deleted | `class-line-missing` |
| GRADER sha / pin wrong | `grader-sha … != 82c635…` / `grader-pin … != 2fd12b88…` |
| K4 → P | `K4 observed P != F` |
| `leg=test_other` on K1 | `K1 leg test_other != test_api` |
| unmutated (battery and rerun) | exit 0 |

Error paths: no `--work` → `SETUP work-dir-required`, exit 2; non-directory `--work` → same,
exit 2; missing receipt → `SETUP receipt-missing`, exit 2; tampered grader →
`SETUP grader-sha-mismatch <got> != <frozen>`, exit 2; absent grader →
`SETUP grader-missing`, exit 2; a socket held on 8080 before a case →
`SETUP port-8080-occupied (K1 before start)`, exit 2. `--render-table` prints the derived table
and exits 0.

## Notes for the L1

- **One earlier battery is preserved for honesty, not for scoring.**
  `evidence/first-battery-instrument-defect.txt` is the first battery this seat ran. It had the
  correct observed vector `P/F/F/F` and a correct `expected` on every case, but ended
  `PREDICATE R63-C1 fail`, because of fact 3 (literal `localhost:8080` never appears in pip
  26.2.1's stderr). The fix was a detector, not a predicate: the frozen requirement ("K2's pip
  stderr names `localhost:8080`") is unchanged, and the receipt line is byte-exact. The scored
  receipt `pypi-probe.txt` is a run of the final file whose sha is quoted above; if the L1
  prefers to treat the preserved first battery as the round's record, the claim is a **miss on
  the stderr clause only** — no leg result differed.
- **The 8080 port was contended all wave and the probe refused rather than graded through it.**
  Every refused invocation printed `SETUP port-8080-occupied …` (a listener held the port
  before a case), `K2 confounded: pip install SUCCEEDED during the quiet window`, `K2
  confounded: stderr does not say connection-refused`, or `K1 confounded: own server served
  no … request`. Not one of those is a leg verdict, and no refused run wrote a partial receipt
  (the receipt is written only after all four cases complete). Contenders, all identified from
  `/proc` and `ss`, none of them started by this seat: a `python3 -m http.server 8080 --directory
  /tmp` answering `/simple/vectorops/` with a 404'ing wheel (PypiMutate measured the same
  process independently), and the seat holding a copy of this probe under `draft/depth/`
  replaying it concurrently — its index serves a *correct* `vectorops`, so a K2 window lands on
  a successful install and the quiet premise is gone. Both clean receipts were taken in windows
  where `ss -ltn` showed no 8080 listener immediately before the run.
- The item's mount list says `--ro-bind <work>/venv`; see fact 2 for the one-line deviation
  (`--bind` on `site-packages` only). If the L1 wants the literal mount, the probe will report
  K1=F for a mount reason; the deviation is what makes K1 a real P.
- `--check-receipt` requires `K2 stderr_mentions_8080=True` verbatim, matching the freeze.
- The K1/K3/K4 access logs are in `evidence/` and show the same `/packages/…whl` path fetched
  for K1 and K3 with different served bytes, and only `/simple/vectorops/` fetched for K4 (no
  wheel is requested, which is why the leg is a `CalledProcessError` from install).

## Tools installed

None — no install or upgrade was needed or attempted, and no pacman transaction ran. Used the
host's `/usr/bin/python3` 3.14.8, `/usr/bin/bwrap`, and the venv's bundled pip 26.2.1. The only
network traffic is loopback to the probe's own 127.0.0.1:8080 (pip's index fetch, proved by the
server's access log); no credentials or secret material was read.

## Scratch

`/fast/scratch/hyaku/kengaku-r63/PypiProbeBuild/` — removed (`rm -rf`) after every artifact
above was copied into `build/`. The other seats' scratch dirs under
`/fast/scratch/hyaku/kengaku-r63/` (ControlProbe, FreezeReview, KnowledgeDraft, L1,
SecurityScan, SiblingOverlap) were left untouched.
