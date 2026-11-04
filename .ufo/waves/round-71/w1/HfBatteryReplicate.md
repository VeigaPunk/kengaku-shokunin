# HfBatteryReplicate — independent replay of the R71-C1 battery (round 71, wave w1)

Seat: `HfBatteryReplicate` (leaf executor, no subagent used). Lane
`L=/home/vgpnk/Projects/shokunin/kengaku-shokunin`; lane tip read read-only
(`git -C L rev-parse master`) = `d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` before and after the run.
Scratch `S=/fast/scratch/hyaku/kengaku-r71/HfBatteryReplicate` (work dir `S/rep`, `TMPDIR=S/rep`).
Frozen claims read in full (all 135 lines of `plans/round-71-claims.md`). No predicate, case table,
vector, digest, kill rule or target was edited; no commit, no package install.

Scope: replay the frozen battery a second time from a separate work dir and a separate evidence
dir, then compare its receipt with the receipt of record line for line, and report
nondeterminism. I do not adjudicate the claim as a whole (the `SKILL.md` row move is the L1's
write; the do-nothing control is another seat's item).

## 1. What I ran

| # | command (cwd = L unless noted) | rc | result |
|---|---|---|---|
| 1 | `TMPDIR=S/rep python3 plans/round71_c1_hf_probe.py --lane L --work S/rep --port-lock /fast/scratch/hyaku/kengaku-r71/port-5000.lock --receipt L/corpus/evidence/round71/hf/receipt-replicate.txt --evidence-dir L/corpus/evidence/round71/hf/sandbox-replicate` | **0** | 8/8 cases, `PREDICATE R71-C1 pass`; wall 105.48 s |
| 2 | `sha256sum plans/round71_c1_hf_probe.py` | 0 | `d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e` |
| 3 | `git show master:plans/round71_c1_hf_probe.py \| sha256sum` | 0 | same `d5ce2fa5…` |
| 4 | `diff <(grep -E '^(VECTOR\|LEGS\|EXC) ' receipt.txt) <(grep -E '^(VECTOR\|LEGS\|EXC) ' receipt-replicate.txt)` | **0** | **empty output** |
| 5 | `diff receipt.txt receipt-replicate.txt` (full, 36 lines each) | **0** | **empty output** |
| 6 | `python3 plans/round71_c1_hf_probe.py --lane . --check-receipt corpus/evidence/round71/hf/receipt-replicate.txt --work S/rep/check` | **0** | `DEFECTS n=0` / `PREDICATE R71-C1 pass` |
| 7 | same for `receipt.txt` (corroboration only, not this seat's judgement) | **0** | `DEFECTS n=0` / `PREDICATE R71-C1 pass` |

Battery stdout, verbatim (captured live to `S/rep/battery.log`; scratch removed after use):

```
CASE K1 derived=PPPP rc=0 exc=[]
CASE K2 derived=PPFP rc=0 exc=[]
CASE K3 derived=PPFP rc=0 exc=[]
CASE K4 derived=PPPF rc=0 exc=[]
CASE K5 derived=PFPP rc=0 exc=[]
CASE K6 derived=PFFF rc=0 exc=['test_api_error_handling', 'test_sentiment_endpoint']
CASE K7 derived=FPPP rc=0 exc=[]
CASE K8 derived=FPPP rc=0 exc=[]
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2
PREDICATE R71-C1 pass
```

Commands 6–7 are not batteries: `check_receipt` never calls `run_case` — it only calls
`prepare_work`/`stage_case` (`plans/round71_c1_hf_probe.py:619-726`), takes no listener, and each
finished in 1.1 s. Only battery command 1 took the shared lock.

### Port-lock behaviour (observed)

Before launching, the lock file named the primary seat's process
(`cat port-5000.lock` → `759285` = `python3 plans/round71_c1_hf_probe.py … HfBatteryR71/work …`).
My battery therefore blocked on `flock` (`plans/round71_c1_hf_probe.py:345-361`, taken per case at
`:564`) until the primary finished: record receipt mtime `22:22:33.533` vs replicate receipt mtime
`22:23:39.435` = 65.9 s of case work inside a 105.48 s wall, i.e. ≈39.6 s waiting on the lock.
**Zero `SETUP` cases**, so the wait was the lock, not a busy port.

## 2. Receipt comparison — identical line for line

- `diff` over `^(VECTOR|LEGS|EXC) ` (item step 3): **empty, rc 0**.
- Full-receipt `diff` (all 36 lines, including the `CASE` lines): **empty, rc 0**.
- `sha256sum` of both files: `136ec423409cbc3031925148b0571ad6edb1cfdf209b42586addb7e2499e6067`
  for `receipt.txt` and for `receipt-replicate.txt`; both 2940 bytes, 36 lines.
- They are two distinct files, not a copy or link: inode `251666718` (record) vs `251667321`
  (replicate), `nlink 1` both, mtimes `22:22:33.532972011` and `22:23:39.434501921` (−0300),
  65.9 s apart. `sandbox/` (inode `251666134`) and `sandbox-replicate/` (`251666536`) are distinct
  trees; sample `K1/manifest.json` inodes `251666138` vs `251666540`.

Case-digest sets, identically ordered (`CASE` line `case_sha256`, 8 distinct values in both):

| case | `case_sha256` (both receipts) |
|---|---|
| K1 | `e96b30e19244973e29bca6f64f4ec7d72045a8eb92fdffd00b1180e3af2ebd9e` |
| K2 | `f030032303fd367d5aa0dc6c1517f8ef5d9c4b77eac517b6d79ceecd6032617b` |
| K3 | `6d6d14ce59b33ed13d2907025f390e344d30629666cbfabb7418d481e7e041e5` |
| K4 | `ec3e2e059766b95380ce187590627fd7908cc15257e3a579e8603f8fb8ac2e15` |
| K5 | `ae9451ae9335d23149937b2abcec7d64d96f5f90f790c71a1be3f6f36ac5a24a` |
| K6 | `6317bec0d99e7c94bc0fd169655e32ee5c43900af5c8d3c6b4e2ebd132eaf7bd` |
| K7 | `c13646e14f6ec4ce2af2151c1fc54c8c96bc8666e1b23cfbafc549d59423b9bd` |
| K8 | `82c99ab85c9f99e0d9001ccf513d00340323c361f307078b4b10e2d5e9c7dc8c` |

Equal across runs is the expected outcome, not a copied value: staging is a pure function of the
frozen case tuple (`stage_case`, `plans/round71_c1_hf_probe.py:381-410`), and command 6 re-derived
those digests from freshly staged trees (`DEFECTS n=0` includes `case-digest` / `case-digest-unique`,
`plans/round71_c1_hf_probe.py:676-678`).

## 3. Vectors from my run, recomputed independently of the probe's own comparison

Parsed the `LEGS` lines of my receipt with a throwaway reader (no probe code) and joined them in
file order `test_model_downloaded, test_flask_api_running, test_sentiment_endpoint,
test_api_error_handling` (`plans/round71_c1_hf_probe.py:76-81`; frozen order
`plans/round-71-claims.md:28-29`):

| case | model / service | frozen | derived | agree |
|---|---|---|---|---|
| K1 | good / good | `PPPP` | `PPPP` | True |
| K2 | good / wrong-label | `PPFP` | `PPFP` | True |
| K3 | good / int-confidence | `PPFP` | `PPFP` | True |
| K4 | good / no-400 | `PPPF` | `PPPF` | True |
| K5 | good / root-drops | `PFPP` | `PFPP` | True |
| K6 | good / none | `PFFF` | `PFFF` | True |
| K7 | absent / good | `FPPP` | `FPPP` | True |
| K8 | corrupt / good | `FPPP` | `FPPP` | True |

Leg witness matrix recomputed from my `LEGS` lines (identical to the matrix recomputed from the
record receipt):

| leg | P cases | F cases | both? |
|---|---|---|---|
| L1 `test_model_downloaded` | K1–K6 | K7, K8 | yes |
| L2 `test_flask_api_running` | K1–K4, K7, K8 | K5, K6 | yes |
| L3 `test_sentiment_endpoint` | K1, K4, K5, K7, K8 | K2, K3, K6 | yes |
| L4 `test_api_error_handling` | K1, K2, K3, K5, K7, K8 | K4, K6 | yes |

## 4. Digest bindings and probe identity (item step 4)

Replicate receipt, lines 1–8 (the record receipt is byte-identical):

```
REV d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0
GRADER sha256=61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857
INSTRUCTION sha256=29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1
MODEL tree_sha256=c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944 files=5
PROBE sha256=d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e
PROBE_BLOB sha256=d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e rev=d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0
LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2
SANDBOX bwrap=bwrap port=5000 net=shared
```

Independently re-derived from committed bytes at `d8a77d3f` (read-only):

- `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` →
  `61a686d6…f87857` (matches `GRADER` and `GRADER_SHA256` at
  `plans/round71_c1_hf_probe.py:59`).
- `sha256sum corpus/evidence/round71/hf/instruction.md` → `29151c5b…51dcc1` (matches `INSTRUCTION`).
- Probe's exact `tree_digest` algorithm over `corpus/evidence/round71/hf/model` (5 files:
  `config.json` `2a5cd25c…`, `model.safetensors` `17a8afc7…`, `tokenizer.json` `fab2332d…`,
  `tokenizer_config.json` `d4256a55…`, `vocab.txt` `b1291273…`) → `c5c25767…858944`, matches `MODEL`.
- `sha256sum plans/round71_c1_hf_probe.py` = `git show master:plans/round71_c1_hf_probe.py | sha256sum`
  = `d5ce2fa5…1aa82e`; both receipts record that same value on `PROBE` and `PROBE_BLOB` with
  `rev=d8a77d3f…`, and `PROBE_BLOB.rev` is the lane tip (`check_receipt` also asserts both are
  ancestors of `master`, `plans/round71_c1_hf_probe.py:653-658`).

## 5. Witness check — each `F` is caused by the staged defect, not by an accident

Failure texts from `sandbox-replicate/<case>/manifest.json` `detail` (byte-identical to
`sandbox/<case>/manifest.json` for all eight cases):

| case | leg | detail (truncated at 220 chars by the harness) |
|---|---|---|
| K2 | L3 | `AssertionError: Text The journey was not bad; I actually had a good time. should be classified as positive` |
| K3 | L3 | `AssertionError: Confidence scores should be floats` |
| K4 | L4 | `AssertionError: API should return 400 for invalid request format` |
| K5 | L2 | `AssertionError: Could not connect to the Flask API on 0.0.0.0:5000` |
| K6 | L2 | same L2 assertion; L3/L4 `ConnectionError: HTTPConnectionPool(host='localhost', port=5000): … [Errno 111]` |
| K7 | L1 | `AssertionError: Model directory not found` |
| K8 | L1 | `AssertionError: Failed to load model or tokenizer: It looks like the config file at '/app/model_cache/sentiment_model/config.json' is not a valid JSON file.` |

Each matches the frozen intent of its case (`plans/round-71-claims.md:34-41`) and the grader
source: the model-directory check and `from_pretrained` at
`corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py:12,17-18`; the
`0.0.0.0:5000` GET that catches only `ConnectionError` at `:29`; the float assertions at `:77-82`;
the 400 assertion at `:103`. K5's stdout shows a live server whose `/` refuses while `/sentiment`
answers (`sandbox-replicate/K5/sandbox-stdout.txt`):
`{"detail": {"test_flask_api_running": "AssertionError: Could not connect to the Flask API on 0.0.0.0:5000"}, "exc": {}, "legs": {"test_api_error_handling": "P", "test_flask_api_running": "F", "test_model_downloaded": "P", "test_sentiment_endpoint": "P"}, "ready": false, "server": true, "server_pid": 3}`.
`server_pid=3` in K1–K5, K7, K8 and `-` in K6 (no server staged).

## 6. Nondeterminism observed

**Exactly one difference exists anywhere between the two runs**, and it touches no reported line:
the `tqdm` weights-load progress rate written to `sandbox-stderr.txt` for **K1–K6** — the cases
where the good model is loaded (leg `test_model_downloaded`, L1, inside `bwrap` stderr). Verbatim
line 3 of each file:

| case | record (`sandbox/`) | replicate (`sandbox-replicate/`) |
|---|---|---|
| K1 | `Loading weights: 100%\|██████████\| 25/25 [00:00<00:00, 51050.44it/s]` | `…, 32214.32it/s]` |
| K2 | `…, 29772.17it/s]` | `…, 25922.77it/s]` |
| K3 | `…, 32423.50it/s]` | `…, 30010.76it/s]` |
| K4 | `…, 27011.23it/s]` | `…, 29772.17it/s]` |
| K5 | `…, 23162.71it/s]` | `…, 15727.85it/s]` |
| K6 | `…, 38807.40it/s]` | `…, 34847.99it/s]` |

K7 (`absent`) and K8 (`corrupt`) write **0-byte** stderr in both runs (no weights load) and match
exactly. All other sandbox artifacts are byte-identical for all eight cases: `manifest.json` MATCH,
`app-tree.txt` MATCH, `sandbox-stdout.txt` MATCH. So the only variance is a throughput figure in a
progress bar, and every receipt line, leg verdict, derived vector, case digest and manifest field
is invariant between the runs.

Invariant fields across the two runs: all eight `derived` vectors, all `LEGS` lines, the single
`EXC K6 test_api_error_handling=E test_sentiment_endpoint=E` line, `sandbox_rc=0` on all eight,
`server_pid=3` on seven cases (`-` on K6), `LIBRARIES`, `REV`, and all four digest lines.

Latent variance sources that were **not** triggered, named with their mechanism:

- Port contention: a foreign listener would yield `derived=SETUP`, `sandbox_rc=1`
  (`plans/round71_c1_hf_probe.py:449-451`) — prevented by the lock; `.lock` serialisation observed
  above.
- Per-case 240 s timeout (`run_case(..., timeout=240)`, `:442`): rc 124 → counted as `setup`.
  Observed case work is ~8 s/case (65.9 s / 8).
- Host library drift: `/fast/ComfyUI/.venv` versions are recorded on the `LIBRARIES` line and
  re-derived by the checker (`library_versions`, `:315-325`); both receipts record
  `python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2`.
- Shared port after exit: a listener owned by another seat's in-flight battery appeared
  (`/venv/bin/python3 /app/server.py`, pid 844614, cwd `/app`) and had exited before my next
  command. It did not overlap my battery window (22:22:33–22:23:39); K5 deriving `PFPP` and K6
  `PFFF` is the in-run proof that no foreign listener answered my `0.0.0.0:5000` probes
  (claims limitation iv, `plans/round-71-claims.md:70-71`).

## 7. Calibration observations (reported, not remediated)

1. **What identity proves.** Both runs execute the same instrument (`PROBE` = `PROBE_BLOB` =
   `d5ce2fa5…`), so byte-identical receipts establish *instrument determinism on this host and
   under the lock*, not that the eight-case table's mechanisms are sufficient to price the grader.
   The independence in this replication is: separate process tree, separate work tree, separate
   evidence tree, separate model load; and the vectors were recomputed by me from the `LEGS` lines
   rather than trusted from the probe's own `agree=` field (§3).
2. **`exc=2` with `setup=0`.** K6's L3 and L4 are witnessed `F` through `requests.ConnectionError`,
   which the harness scores `F` and records on the `EXC` line (harness branch
   `plans/round71_c1_hf_probe.py:176-181`), not through an `AssertionError`. The frozen predicate
   only requires `… setup=0` and `seen_p=seen_f=4` (`plans/round-71-claims.md:43-47`), so `pass`
   is within the rule; a successor that wants assertion-only witnesses for "no service" would need
   a different staging, since the grader's L3/L4 make no assertion when the connection fails.
3. **`server_pid=3` on both receipts** is a PID-namespace constant (`bwrap --unshare-all`,
   `:416-441`), not an additional independent witness; it is identical in both runs because the
   namespace is fresh per case.
4. **`ready=false` on K5 with a live server.** `wait_ready` probes `GET /`
   (`:140-150`), which is exactly what `root-drops` closes; the flag is informational (K5's
   `sandbox-stdout.txt` shows `"ready": false, "server": true` and L3/L4 still `P`).
5. **New untracked evidence on the lane.** `corpus/evidence/round71/hf/receipt-replicate.txt` and
   `sandbox-replicate/` (8 case dirs × 4 files) are on disk, untracked (`git status --porcelain`).
   No gate globs that directory: `grep -rn 'round71/hf' --include=*.py --include=*.sh` over the
   lane finds only the explicit paths in `plans/round-71-claims.md` and the two constants at
   `plans/round71_c1_hf_probe.py:60,62`. Their presence cannot move any C1 counter;
   commit/retain is the L1's call.
6. **Claims wording vs data.** The item note "case digests may be compared too but are not
   required to differ" is satisfied in the stronger form: all eight digests are equal between the
   runs, as staging is a pure function of the frozen case tuple; the eight values remain distinct
   from one another, so K2/K3 (both `PPFP`) price different bytes.

## 8. Verdict

**The R71-C1 battery replicates.** `VECTOR`, `LEGS` and `EXC` lines are identical line for line
between `corpus/evidence/round71/hf/receipt.txt` and my independent
`corpus/evidence/round71/hf/receipt-replicate.txt` (diff empty, rc 0; the whole 36-line receipts
are also byte-identical, sha256 `136ec423…e6067`). All eight `derived` vectors equal the frozen
table with `agree=True`; `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`; `SUMMARY cases=8 legs=32
mismatches=0 setup=0 exc=2`; `PROBE` and `PROBE_BLOB` both `d5ce2fa5…1aa82e`, re-derived from the
working tree and the committed blob at tip `d8a77d3f`; `--check-receipt` exits 0 with
`DEFECTS n=0` on both receipts. No nondeterminism observed touches any receipt line; the only
variance is the tqdm throughput figure in `sandbox-stderr.txt` for K1–K6, on the L1 model-load
path. No case diverges from the frozen table, and no rule needed a report of being wrong.

## 9. Tooling, cleanup, limits

- No tool installed or upgraded; nothing was needed (bwrap 0.13.1 and the read-only
  `/fast/ComfyUI/.venv` were already present).
- Scratch `S` removed after use (staged case trees are inputs only); all receipts and sandbox
  captures live under `L/corpus/evidence/round71/hf/`.
- Limits: the replay uses the lane's stdlib HTTP server stand-in and the host's
  `transformers`/`torch`, per the frozen named limitations; it prices the grader's logic, not a
  model's accuracy. Both receipts are untracked until the L1 commits them.
