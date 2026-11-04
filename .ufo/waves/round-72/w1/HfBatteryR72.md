# HfBatteryR72 — R72-C1 nine-case battery, receipt of record

Seat: `HfBatteryR72` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Tip at run: `b6336136e0e891522b113a94d8e0bd65e0eae8de` (branch `master`; `git rev-parse --show-toplevel`
printed the lane, tracked tree clean).

## Verdict

The frozen instrument ran the nine-case table, wrote the receipt of record, and the frozen checker
re-derived every clause: **`DEFECTS n=0`, `PREDICATE R72-C1 pass`, check exit code 0**. All nine
`VECTOR` lines carry `agree=True`; no `SETUP` or `ERROR` case occurred, so no retry was taken.
This seat's clause of R72-C1 holds. The `--stub-control` receipt named in the frozen predicate is
another seat's item and was not produced here (see Out-of-seat scope).

## Commands actually run (exit codes verbatim)

1. `mkdir -p /fast/scratch/hyaku/kengaku-r72/HfBatteryR72` → ok.
   `ss -ltn 'sport = :5000'` at 23:08 local, before any probe command:

   ```
   State  Recv-Q Send-Q Local Address:Port Peer Address:Port
   LISTEN 0      5            0.0.0.0:5000      0.0.0.0:*
   ```
   `ss -ltnp` attributed it to `python3`, pid 2116160, cmd `/venv/bin/python3 /app/server.py`,
   parent `/venv/bin/python3 /probe/harness.py server` — i.e. **a sibling seat's sandbox case
   mid-battery** (elapsed 16 s), not a host service. The shared
   `/fast/scratch/hyaku/kengaku-r72/port5000.lock` was stale-content (`2116109`) at read time; the
   `flock` is what serialises, not the file body.

2. Battery (cwd = lane):

   ```
   python3 plans/round72_c1_hf_probe.py --lane . \
     --work /fast/scratch/hyaku/kengaku-r72/HfBatteryR72/battery \
     --receipt corpus/evidence/round72/hf/receipt.txt \
     --evidence-dir corpus/evidence/round72/hf/sandbox \
     --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock
   BATTERY_RC=0
   ```
   stdout (verbatim), wall 49.27 s:

   ```
   CASE K1 derived=PPPP rc=0 exc=[]
   CASE K2 derived=PPFP rc=0 exc=[]
   CASE K3 derived=PPFP rc=0 exc=[]
   CASE K4 derived=PPPF rc=0 exc=[]
   CASE K5 derived=PFPP rc=0 exc=[]
   CASE K6 derived=PFFF rc=0 exc=['test_api_error_handling', 'test_sentiment_endpoint']
   CASE K7 derived=FPPP rc=0 exc=[]
   CASE K8 derived=FPPP rc=0 exc=[]
   CASE K9 derived=PPPF rc=0 exc=[]
   LEG-COVERAGE legs=4 seen_p=4 seen_f=4
   SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2
   PREDICATE R72-C1 pass
   ```

3. Check (cwd = lane, exactly as assigned):

   ```
   python3 plans/round72_c1_hf_probe.py --lane . \
     --check-receipt corpus/evidence/round72/hf/receipt.txt \
     --work /fast/scratch/hyaku/kengaku-r72/HfBatteryR72/check \
     --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock
   > corpus/evidence/round72/hf/check.txt
   RC=0
   ```
   `corpus/evidence/round72/hf/check.txt` (34 bytes) is exactly:

   ```
   DEFECTS n=0
   PREDICATE R72-C1 pass
   ```

## Receipt of record — frozen clauses

Path `corpus/evidence/round72/hf/receipt.txt`, 40 lines, 3494 bytes,
sha256 `fa060b7fa2e4adbf8f0d4de180bea2d66bc7598ed5f13dbcfcf6093b7c224087`.
`check.txt` sha256 `0e63c73f0c179191a77b94a703a58c6a2c4dc8c035e9edcbc829632ec179afe2`.

Header lines (verbatim):

```
REV b6336136e0e891522b113a94d8e0bd65e0eae8de
GRADER sha256=61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857
INSTRUCTION sha256=29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1
MODEL tree_sha256=c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944 files=5
PROBE sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e
PROBE_BLOB sha256=99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e rev=b6336136e0e891522b113a94d8e0bd65e0eae8de
LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2
SANDBOX bwrap=bwrap port=5000 net=shared cleared_env=True
```

Nine `VECTOR` lines (verbatim; each has `agree=True`):

```
VECTOR K1 expected=PPPP derived=PPPP agree=True
VECTOR K2 expected=PPFP derived=PPFP agree=True
VECTOR K3 expected=PPFP derived=PPFP agree=True
VECTOR K4 expected=PPPF derived=PPPF agree=True
VECTOR K5 expected=PFPP derived=PFPP agree=True
VECTOR K6 expected=PFFF derived=PFFF agree=True
VECTOR K7 expected=FPPP derived=FPPP agree=True
VECTOR K8 expected=FPPP derived=FPPP agree=True
VECTOR K9 expected=PPPF derived=PPPF agree=True
```

Leg/coverage lines (verbatim):

```
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2
```

`PROVENANCE` line (verbatim):

```
PROVENANCE env_cleared=True allowlist=PATH,HOME,LANG,PYTHONPATH,PYTHONNOUSERSITE,PYTHONWARNINGS,TMPDIR,HF_HUB_OFFLINE,TRANSFORMERS_OFFLINE allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0 transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py
```

Per-case captures: `corpus/evidence/round72/hf/sandbox/K1..K9/{manifest.json,sandbox-stdout.txt,
sandbox-stderr.txt,app-tree.txt}` — 36 files, all nine `case_sha256` values distinct (checker clause
`case-digest-unique` passed). Every manifest's `prov.canary` is `"ABSENT"`; every
`prov.transformers_file` is the `/venv/.../transformers/__init__.py` above; every
`prov.executable` is `/venv/bin/python3`, `cwd=/app`.

## K9 — the ninth case, assert site

K9 staged `model=good`, `server=400-no-error-field`, derived `PPPF`, `sandbox_rc=0`.
`corpus/evidence/round72/hf/sandbox/K9/manifest.json` detail (verbatim):

```
"test_api_error_handling": "AssertionError: Error response should contain 'error' field"
```

The exact line I believe reds, `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py:107`
(byte-pinned sha256 `61a686d6…87857`):

```python
107:    assert "error" in error_data, "Error response should contain 'error' field"
```

i.e. the leg passed the `status_code == 400` assert at `:103` and fell at `:107`, which is precisely
the site the round-71 eight-case table could not reach. K4 reds the earlier `:103` assert instead
(`no-400` answered 200), so the pair K4/K9 witnesses both assert sites of leg 4.

## Kill-rule accounting (frozen)

| kill clause | observed | verdict |
|---|---|---|
| any case `agree=False` | 0 of 9 | clear |
| `setup` failure / `SETUP` / `ERROR` case | `setup=0`; no case printed `SETUP`/`ERROR` | clear |
| `PROVENANCE` absent/duplicated | exactly one line | clear |
| `distinct != 1` | `distinct=1` | clear |
| `transformers_file` outside `/venv/` | `/venv/lib/python3.13/site-packages/transformers/__init__.py` | clear |
| `canary_seen > 0` | `canary_seen=0` | clear |
| `allowlist_seen != 9/9` | `9/9` | clear |
| check exit code | 0 | clear |

No retry was taken (none was needed); no case was reselected.

## Findings (report-only; no predicate, table, vector, digest, rule or target was edited)

**F1 — the sandbox's observed key set is 11, not 9; `allowlist_seen` is a superset check.**
Each manifest's `prov.env_keys` is
`HF_HUB_OFFLINE,HOME,LANG,PATH,PWD,PYTHONNOUSERSITE,PYTHONPATH,PYTHONWARNINGS,TMPDIR,TORCHINDUCTOR_CACHE_DIR,TRANSFORMERS_OFFLINE`.
Attribution measured in scratch under the same `bwrap --clearenv` argv shape (read-only binds,
nine `--setenv`, `/venv` bound):

- bwrap alone adds `PWD` (set by `--chdir /app`), so 10 keys before any library import;
- importing `transformers`/`torch` adds nothing;
- `AutoModelForSequenceClassification.from_pretrained` **inside the sandbox** adds
  `TORCHINDUCTOR_CACHE_DIR=/tmp/torchinductor_vgpnk` (empirical: `NEW_KEYS ['TORCHINDUCTOR_CACHE_DIR']`).

Consequence: the claim's mechanism sentence ("nothing in the parent environment reaches the
sandbox") is witnessed (`canary_seen=0`, parent `PYTHONPATH` value absent, one distinct file), but
the receipt does not assert an exact-set allowlist; a future instrument could print
`extra_keys=`/`env_count=` so the superset-vs-exact distinction is visible. The `TORCHINDUCTOR_CACHE_DIR`
value also leaks the host account name through the read-only `/etc` bind — out of scope here, but it
means "the sandbox sees only its own state" is not literally true at the variable-value level.

**F2 — the `SUMMARY` line carries `exc=2`, which the claim sentence does not quote.**
Frozen claim text quotes `SUMMARY cases=9 legs=36 mismatches=0 setup=0`; the receipt line is that
prefix plus ` exc=2`. The frozen checker recomputes `want_sum` **with** the exc term, so both
readings pass (`exc_n` recomputed from the `EXC K6` line), and the predicate's operative clause
(`DEFECTS n=0` + `PREDICATE … pass` + rc 0) holds. Recorded as a doc-quotation precision issue, not
a defect of the instrument. The two `exc` legs are K6's `test_sentiment_endpoint` and
`test_api_error_handling`, scored `F` as designed (ConnectionError, recorded separately on `EXC`).

**F3 — receipt `REV` binds the run tip, not the freeze base.** `REV b6336136…` and `PROBE_BLOB
rev=b6336136…`; the claims doc names freeze base `c6322972…`. The frozen predicate says "at the
round tip" and the checker re-derives ancestry (`receipt-rev` clause passed), so this is consistent;
noted so a reader does not mistake the receipt for a base-tip binding.

**F4 — `server_pid=3` is namespace-local.** `bwrap --unshare-all` unshares PID, so the staged
server's PID is only comparable inside its own sandbox; the receipt's per-case PID is not a
host-observable identity. K6 correctly prints `server_pid=-` (no service staged).

**F5 — port-5000 contention is real and the shared `flock` carried it.** A sibling sandbox
(`CounterMutateR72`) held 5000 at my start, and was again mid-case (K5) after my check completed.
Because the lock is taken **per case** (not per battery) and `wait_port_free` has a 20 s cap, a
sufficiently slow foreign listener would turn a case into `SETUP`; that did not happen here
(`setup=0`). Recorded as the observed failure mode of the shared-port protocol, not a claim defect.

**F6 — the replicate seat's receipt is byte-identical.** `receipt-replicate.txt` has the same
sha256 `fa060b7f…` and `diff` printed `IDENTICAL`. Caveat for the calibration axis: staged-input
digests are path-independent **by design** (the instrument's own selftest asserts
`PATH-INDEPENDENT sha_equal=True`), so byte identity across two sequential runs at one tip is
expected and is corroboration rather than independent variation.

## Out-of-seat scope, stated

- `--stub-control` (`corpus/evidence/round72/hf/stub-control.txt`) is named in the R72-C1 frozen
  predicate but is not in this seat's item; it was not run here. R72-C1's full predicate therefore
  is not evidenced by this seat alone.
- `--selftest` / `--control` were likewise not run by this seat (other seats' items); I did not
  rerun or widen.

## Scratch and tooling

- Scratch root `/fast/scratch/hyaku/kengaku-r72/HfBatteryR72` (battery work tree, `check`, the
  env-attribution probe, stdout log): deleted after the receipt, `check.txt` and the per-case
  sandbox captures were written into the lane; verified absent afterwards. Nothing was copied out
  of scratch except the assigned evidence paths.
- Lane footprint of this seat: `corpus/evidence/round72/hf/{receipt.txt,check.txt,sandbox/K1..K9/*}`
  only (plus this report). No tracked file, no `.ufo/state/`, no git mutation.
- No tool install or upgrade was needed or performed (bwrap 0.13.1, python 3.13.16, torch 2.14.1,
  transformers 5.21.0 as bound into the sandbox).
