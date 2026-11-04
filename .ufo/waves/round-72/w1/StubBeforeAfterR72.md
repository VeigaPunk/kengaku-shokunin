# StubBeforeAfterR72 — R71-R6 before → after (wave w1, v1)

Seat: `StubBeforeAfterR72` · lane `kengaku-shokunin` · 2026-11-03 · round 72, wave w1.
Observed `REV` in every receipt produced here: `b6336136e0e891522b113a94d8e0bd65e0eae8de`
(the frozen claims name `c6322972…` as the freeze base; both of-record round-72 receipts and mine
cite `b6336136…`, so the round-tip predicate is consistent — I did not investigate the move).

## Verdict

**The premise is confirmed, not falsified.** The same raising `transformers` stub, injected the
same way (parent `PYTHONPATH=/app/stub` + the stub copied into every staged case's `app/stub`),
is imported in **8/8** round-71 cases and changes that table, and is **invisible** to the
round-72 probe: 9/9 vectors unchanged, `PROVENANCE … transformers_file=/venv/…`, predicate pass.

One sentence: *the stub that turns the round-71 replay red (L1 `RuntimeError` in every case,
6/8 derived vectors flipped, `PREDICATE R71-C1 fail`) is inert under the round-72 argv, where the
same nine vectors stay at their frozen values and the sandbox reports its own `/venv` copy of
`transformers`.*

## What ran (command → exit code)

1. `mkdir -p /fast/scratch/hyaku/kengaku-r72/StubBeforeAfterR72`, stub package written at
   `stub/transformers/__init__.py`, 40 bytes, sha256
   `d36712afe91100c6c0f6a9702779ee49d23330a1d32040b11ba13a5f60fb5122`:
   ```python
   raise RuntimeError('stub transformers')
   ```
2. **BEFORE** — round-71 probe, no `--clearenv`:
   ```
   cd /fast/scratch/hyaku/kengaku-r72/StubBeforeAfterR72
   python3 stub_driver.py \
     /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round71_c1_hf_probe.py \
     <scratch>/sc-before \
     /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round72/hf/stub-before-v1.txt \
     <scratch>/before.json <scratch>/ev-before
   ```
   → **exit 1** (the battery's own predicate line is `fail`, and the driver propagates it).
3. **AFTER** — round-72 probe, same stub bytes, same driver, same `PYTHONPATH=/app/stub`:
   ```
   python3 stub_driver.py \
     /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round72_c1_hf_probe.py \
     <scratch>/sc-after \
     /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round72/hf/stub-after-v2.txt \
     <scratch>/after.json <scratch>/ev-after
   ```
   → **exit 0**.
4. **Shipped control** (cwd = lane, exact invocation from the item):
   ```
   python3 plans/round72_c1_hf_probe.py --lane . \
     --work /fast/scratch/hyaku/kengaku-r72/StubBeforeAfterR72/sc \
     --receipt corpus/evidence/round72/hf/stub-control.txt --stub-control \
     --port-lock /fast/scratch/hyaku/kengaku-r72/port5000.lock
   ```
   → **exit 0**, printed:
   ```
   STUB-CONTROL exposed=False vectors_unchanged=True
   ```
5. Two mechanism witnesses (scratch-only, no probe edit): `env_witness.py` runs the round-72
   module's own `bwrap_argv()` with the trailing `VENV_PYTHON /probe/harness.py` replaced by a
   `python -c`, under the driver's parent env (`PYTHONPATH=/app/stub`, `R72_CANARY` set); and a
   stronger variant that also stages a `transformers` package at the top of `/app`.
6. The claim's own checker, run on the **injected** after receipt, both ways:
   ```
   python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/stub-after-v2.txt
   → DEFECTS n=0 / PREDICATE R72-C1 pass / rc 0
   python3 plans/round72_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round72/hf/stub-after-v2.txt --work <scratch>/checkwork
   → DEFECT case-digest K1..K9 (receipt = stub digest, derived = clean digest) / DEFECTS n=9 / PREDICATE R72-C1 fail / rc 1
   ```

Driver shape (one script, both probes; only the probe path differs):

```python
orig_stage_case, orig_run_case = mod.stage_case, mod.run_case

def stage_case_with_stub(*a, **k):                 # write the stub into each staged case
    root = Path(orig_stage_case(*a, **k))
    d = root / "app" / "stub" / "transformers"; d.mkdir(parents=True, exist_ok=True)
    (d / "__init__.py").write_text(STUB_SRC)
    return root

def run_case_recording(*a, **k):                   # keep what came back, change nothing
    r = orig_run_case(*a, **k); seen.append(r); return r

mod.stage_case, mod.run_case = stage_case_with_stub, run_case_recording
os.environ["PYTHONPATH"] = "/app/stub"             # the path the bind-mounted app dir has inside
rc = mod.run_battery(LANE, work, receipt, evidence, lock=PORT_LOCK)
```

`/app/stub` is a *sandbox-visible* path only: on the host `ls /app` is
`No such file or directory`, so the injection cannot act on the driver's own `library_versions()`
subprocess — it can only act through the bwrap bind of the case's `app` directory, which is the
round-71 attack channel.

## The two tables side by side

Baseline columns are the committed of-record receipts (`corpus/evidence/round71/hf/receipt.txt`,
`corpus/evidence/round72/hf/receipt.txt`), not my runs. `E` = leg failed by non-assertion
exception (the stub's `RuntimeError`).

| case | R71 of record (no stub) | **BEFORE: R71 + stub** | **AFTER: R72 + stub** | R72 of record (no stub) |
|---|---|---|---|---|
| K1 | `PPPP` agree | `FPPP` **mismatch**, L1 `E` | `PPPP` agree | `PPPP` agree |
| K2 | `PPFP` agree | `FPFP` **mismatch**, L1 `E` | `PPFP` agree | `PPFP` agree |
| K3 | `PPFP` agree | `FPFP` **mismatch**, L1 `E` | `PPFP` agree | `PPFP` agree |
| K4 | `PPPF` agree | `FPPF` **mismatch**, L1 `E` | `PPPF` agree | `PPPF` agree |
| K5 | `PFPP` agree | `FFPP` **mismatch**, L1 `E` | `PFPP` agree | `PFPP` agree |
| K6 | `PFFF` agree | `FFFF` **mismatch**, L1/L3/L4 `E` | `PFFF` agree | `PFFF` agree |
| K7 | `FPPP` agree | `FPPP` agree, L1 `E` (was `AssertionError`) | `FPPP` agree | `FPPP` agree |
| K8 | `FPPP` agree | `FPPP` agree, L1 `E` (was `AssertionError`) | `FPPP` agree | `FPPP` agree |
| K9 | *(no case)* | *(no case)* | `PPPF` agree | `PPPF` agree |

Tally lines, verbatim:

```
BEFORE  LEG-COVERAGE legs=4 seen_p=3 seen_f=4
BEFORE  SUMMARY cases=8 legs=32 mismatches=6 setup=0 exc=10
BEFORE  PREDICATE R71-C1 fail
AFTER   LEG-COVERAGE legs=4 seen_p=4 seen_f=4
AFTER   SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2
AFTER   PREDICATE R72-C1 pass
```

**Exactly how the before table changes.** `test_model_downloaded` is the only leg that imports
`transformers`, and the grader imports it *outside* its own `try` (`test_outputs.py:10`, try at
`:16`), so the stub's `RuntimeError` escapes as a non-assertion exception: L1 goes `P → F` in all
six cases that expected P (K1–K6), and in K7/K8 the leg stays `F` but its reason changes from the real
library's `AssertionError` to `RuntimeError: stub transformers` (the `EXC` lines grow from the
of-record `exc=2` to `exc=10`). No case becomes `ERROR`, no `SETUP` appears, and the other three
legs are untouched — the staged server is a stdlib HTTP process that never imports
`transformers`. Derived-vector equality therefore moves in **6/8** cases, while all **8/8**
cases change in `LEGS`/`EXC` content.

**Exactly what did not change after.** All nine derived vectors equal their frozen values, the
observed vector set is unchanged from the of-record battery, and
`PROVENANCE env_cleared=True allowlist_seen=9/9 cases=9 distinct=1 canary_seen=0
transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py` appears once.

## Why the after arm is blind — three independent witnesses

1. **Outcome.** 9/9 vectors unchanged, `mismatches=0`, `PREDICATE R72-C1 pass`, while the same
   stub bytes are present in the same place in each staged tree. All nine
   `CASE Kn case_sha256=` values in `stub-after-v2.txt` differ from their of-record
   counterparts (e.g. K1 `a26d8d9c…` vs `4512bfa2…`), so the injection really landed; the staged
   app trees contained `stub/transformers/__init__.py`.
2. **Provenance.** Every case's `prov.transformers_file` is the read-only `/venv` copy, the
   canary is `ABSENT` in all nine, and `distinct=1`.
3. **Filesystem.** In the before arm the per-case `app-tree.txt` shows *two* stub entries —
   `stub/transformers/__init__.py` **and** `stub/transformers/__pycache__/__init__.cpython-313.pyc`
   — i.e. CPython executed the stub inside the sandbox. In the after arm the tree shows only the
   `.py`: no `.pyc` was ever written, so the module was never imported. (These trees lived in my
   scratch evidence dirs and were removed with the scratch; the receipts above are the retained
   evidence, and the descriptor line `EXC Kn test_model_downloaded=E` ↔ its absence carries the
   same signal.)

Direct environment measurement, using the probe's own `bwrap_argv()` unchanged:

```
ARGV_CLEARENV=True
PYTHONPATH='/venv/lib/python3.13/site-packages'
CANARY='ABSENT'
SYS_PATH_0_3=['', '/venv/lib/python3.13/site-packages', '/home/vgpnk/.local/share/uv/python/cpython-3.13.16-linux-x86_64-gnu/lib/python313.zip']
ENV_N=10
TRANSFORMERS_FILE=/venv/lib/python3.13/site-packages/transformers/__init__.py
WITNESS rc=0
```

## Findings

- **F1 (confirms R71-R6).** The round-71 sandbox lets a parent
  `PYTHONPATH` module replace the solver-visible library: the driver recorded
  `detail.test_model_downloaded = "RuntimeError: stub transformers"` for all eight cases (the
  receipt retains the `EXC Kn test_model_downloaded=E` lines; the message itself lived in the
  driver log, which went with the scratch), and `stub-before-v1.txt` fails its own predicate.
  Note the calibration: this *raising* stub proves **reachability**
  (import happened), not *forgery* (outputs reproduced). The round-71 `ClaimFalsify71` §C1-b
  "8/8 vectors" result used a **designed** stub that mimics `from_pretrained`; I did not re-run
  that variant (out of item). Same channel, different strength of witness — both must not be
  conflated.
- **F2 (R72-C1 isolation is witnessed twice over).** The after arm is identical in staging,
  differs only in the probe's argv, and is blind by outcome *and* by the sandbox's self-reported
  library file. `STUB-CONTROL exposed=False vectors_unchanged=True` (shipped control) reproduces
  that independently, with the stub on a host-side `PYTHONPATH`.
- **F3 (the mechanism is the allowlist, not just `--clearenv`).** Inside the sandbox
  `PYTHONPATH` is `/venv/lib/python3.13/site-packages` even though the parent had `/app/stub`;
  `/app/stub` is bound and present but simply not on `sys.path`. A future edit that drops the
  explicit `("PYTHONPATH", VENV_SITE)` allowlist entry *and* keeps `--clearenv` would still be
  blind, but one that keeps an inherited `PYTHONPATH` would not — the entry is load-bearing.
- **F4 (adjacent surface, measured, no predicate change).** A stronger variant — a
  `transformers` package at the top of the staged `/app` instead of under `/app/stub` — is also
  invisible to the harness: `SYS_PATH_0='/probe'`, `APP_ON_PATH=False`, and the import still
  resolves to `/venv`. Residual, unmeasured by any leg: the **server** process is started as
  `/app/server.py`, so its `sys.path[0]` is `/app`; a staged server that imported
  `transformers` would take `/app/transformers`. No leg prices server internals, so this is a
  named limitation of the isolation claim, not a falsification of it.
- **F5 (provenance-line semantics, precision note).** `allowlist_seen=9/9` is a superset test
  (`set(env_keys) >= set(allow_names)`), not an equality claim: the observed sandbox environment
  has 10–11 keys — `PWD` (from bwrap `--chdir`) and `TORCHINDUCTOR_CACHE_DIR` (created by torch at
  import) are born inside. Reading `9/9` as "exactly nine inherited variables" would be wrong;
  the inheritance witness is `canary_seen=0`, and the `env_keys` field records names, not values.
  My `env_witness` measured the value.
- **F6 (digest comparability).** Both stub receipts' `case_sha256` include the injected stub, so
  they are intentionally unequal to the of-record battery digests; `case_sha256` is not a frozen
  claim value. Cross-arm sanity: the K6 digest is byte-identical in the before and after receipts
  (`727aa98d…`) — same staged app plus stub, different sandbox argv, opposite outcome.
- **F7 (`--check-receipt` is two witnesses, and only one of them is about isolation).** Run on a
  receipt produced *under an active stub injection*, the text-only arm passes it
  (`DEFECTS n=0`, `PREDICATE R72-C1 pass`, rc 0): the vectors, coverage, provenance line and
  digests bindings are all self-consistent. The `--work` arm fails it on all nine `case-digest`
  checks (rc 1). So R72-C1's limitation (v) has a measured boundary: the re-staged case digests
  are a live witness against *staged-tree* tampering specifically, and nothing else in the
  checker's text arm can distinguish a sandbox that was blind from one that was not — which is
  why the `--stub-control` run and the provenance line, not `--check-receipt`, carry the
  R71-R6 closure.

## Limits

- The before arm is the shipped round-71 `run_battery`/`stage_case`/`bwrap_argv` with only the
  stub added through `stage_case`; I edited no probe, predicate, case table, vector or digest.
- The after arm's nine-vector agreement is evidence about the *test harness's isolation*, not
  about model accuracy (limitation iii of R72-C1 still stands).
- The two `case_sha256`-based statements above are pre-run digests; the `.pyc` observation is a
  post-run tree listing, so the two are not contradictory.
- No tool was installed or upgraded; no pacman, no `uv tool`, no host service touched.
- No `git`/`jj` command was run other than the probes' own read-only `git show`/`rev-parse`
  calls during the batteries; no commits, adds or resets.

## Receipts (retained, outside scratch)

| path | bytes | sha256 |
|---|---|---|
| `corpus/evidence/round72/hf/stub-before-v1.txt` | 3188 | `0062d64cd089954a79e640f33b315708d35651db55e4d1ca93a94f07e75b7842` |
| `corpus/evidence/round72/hf/stub-after-v2.txt` | 3494 | `5d74fcdbc3775d5e8423e33cf5f97efbfe1a2a15ff69e9da2edf2d0fa60fe21f` |
| `corpus/evidence/round72/hf/stub-control.txt` | 3613 | `ed0ea7c4b5b28eec8bd0b3e3d7e101fb74f63e63cf156ea534bd53802073d350` |

Both stub receipts carry `GRADER sha256=61a686d6…87857`, `INSTRUCTION sha256=29151c5b…1dcc1`,
`MODEL tree_sha256=c5c25767…5944 files=5`, `LIBRARIES python=3.13.16 torch=2.14.1+cu130
transformers=5.21.0 requests=2.34.2`, and `PROBE sha256` / `PROBE_BLOB sha256` equal to each
other (`d5ce2fa5…` for round 71, `99867c7f…` for round 72).

## Hygiene

`/fast/scratch/hyaku/kengaku-r72/StubBeforeAfterR72` was created twice (the three batteries, then
the `--check-receipt --work` re-stage) and removed both times after the receipts were copied into
the lane (`rm -rc=0`; `ls` of the scratch parent shows no stub dir; `pgrep -af
'StubBeforeAfterR72|stub_driver'` empty; no `/tmp` file created by this seat). The shared
`/fast/scratch/hyaku/kengaku-r72/port5000.lock` was used for all three batteries; no port was
left bound.
