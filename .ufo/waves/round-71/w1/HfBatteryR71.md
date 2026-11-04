# HfBatteryR71 — R71-C1 battery replay (wave w1)

Seat: `HfBatteryR71` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
branch `master`. Lane tip at run (read-only `git rev-parse master`):
`d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` (freeze base was `1cb49cac`; the probe, instruction
and model fixture are committed on top of it). Scratch:
`/fast/scratch/hyaku/kengaku-r71/HfBatteryR71/` (logs kept there; staged trees removed after use).

Scope: run the frozen R71-C1 battery **once** and produce the receipt of record + checker
output. No predicate, case table, vector, digest, kill rule or target was edited; `SKILL.md` was
not written (see §4).

## 1. What I ran (commands + rc)

Port precondition (before any battery), per seat item step 2:

```
$ ss -ltn '( sport = :5000 )'
State Recv-Q Send-Q Local Address:Port Peer Address:Port
rc=0
```

→ empty table: no listener on 5000 before the run.

Battery (step 3), from the lane root, scratch `--work` under the seat scratch and the shared
port lock:

```
$ python3 plans/round71_c1_hf_probe.py \
    --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --work /fast/scratch/hyaku/kengaku-r71/HfBatteryR71/work \
    --port-lock /fast/scratch/hyaku/kengaku-r71/port-5000.lock \
    --receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round71/hf/receipt.txt \
    --evidence-dir /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round71/hf/sandbox
...
BATTERY_RC=0        (wall time 52.22 s)
```

Checker (step 4), receipt of record re-derived:

```
$ python3 plans/round71_c1_hf_probe.py \
    --lane /home/vgpnk/Projects/shokunin/kengaku-shokunin \
    --work /fast/scratch/hyaku/kengaku-r71/HfBatteryR71/check \
    --port-lock /fast/scratch/hyaku/kengaku-r71/port-5000.lock \
    --check-receipt /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round71/hf/receipt.txt
DEFECTS n=0
PREDICATE R71-C1 pass
CHECK_RC=0          (1.18 s)
```

`check.txt` in the evidence dir contains exactly those two lines.

## 2. Receipt of record — quoted lines

`corpus/evidence/round71/hf/receipt.txt` (36 lines):

```
REV d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0
GRADER sha256=61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857
INSTRUCTION sha256=29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1
MODEL tree_sha256=c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944 files=5
PROBE sha256=d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e
PROBE_BLOB sha256=d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e rev=d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0
LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2
SANDBOX bwrap=bwrap port=5000 net=shared
CASE K1 case_sha256=e96b30e19244973e29bca6f64f4ec7d72045a8eb92fdffd00b1180e3af2ebd9e server_pid=3 sandbox_rc=0
LEGS K1 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K1 expected=PPPP derived=PPPP agree=True
CASE K2 case_sha256=f030032303fd367d5aa0dc6c1517f8ef5d9c4b77eac517b6d79ceecd6032617b server_pid=3 sandbox_rc=0
LEGS K2 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=F test_api_error_handling=P
VECTOR K2 expected=PPFP derived=PPFP agree=True
CASE K3 case_sha256=6d6d14ce59b33ed13d2907025f390e344d30629666cbfabb7418d481e7e041e5 server_pid=3 sandbox_rc=0
LEGS K3 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=F test_api_error_handling=P
VECTOR K3 expected=PPFP derived=PPFP agree=True
CASE K4 case_sha256=ec3e2e059766b95380ce187590627fd7908cc15257e3a579e8603f8fb8ac2e15 server_pid=3 sandbox_rc=0
LEGS K4 test_model_downloaded=P test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=F
VECTOR K4 expected=PPPF derived=PPPF agree=True
CASE K5 case_sha256=ae9451ae9335d23149937b2abcec7d64d96f5f90f790c71a1be3f6f36ac5a24a server_pid=3 sandbox_rc=0
LEGS K5 test_model_downloaded=P test_flask_api_running=F test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K5 expected=PFPP derived=PFPP agree=True
CASE K6 case_sha256=6317bec0d99e7c94bc0fd169655e32ee5c43900af5c8d3c6b4e2ebd132eaf7bd server_pid=- sandbox_rc=0
LEGS K6 test_model_downloaded=P test_flask_api_running=F test_sentiment_endpoint=F test_api_error_handling=F
EXC K6 test_api_error_handling=E test_sentiment_endpoint=E
VECTOR K6 expected=PFFF derived=PFFF agree=True
CASE K7 case_sha256=c13646e14f6ec4ce2af2151c1fc54c8c96bc8666e1b23cfbafc549d59423b9bd server_pid=3 sandbox_rc=0
LEGS K7 test_model_downloaded=F test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K7 expected=FPPP derived=FPPP agree=True
CASE K8 case_sha256=82c99ab85c9f99e0d9001ccf513d00340323c361f307078b4b10e2d5e9c7dc8c server_pid=3 sandbox_rc=0
LEGS K8 test_model_downloaded=F test_flask_api_running=P test_sentiment_endpoint=P test_api_error_handling=P
VECTOR K8 expected=FPPP derived=FPPP agree=True
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2
PREDICATE R71-C1 pass
```

### Frozen vs derived (step 5)

| case | model | service | frozen | derived | differ? |
|---|---|---|---|---|---|
| K1 | good | good | `PPPP` | `PPPP` | no |
| K2 | good | wrong-label | `PPFP` | `PPFP` | no |
| K3 | good | int-confidence | `PPFP` | `PPFP` | no |
| K4 | good | no-400 | `PPPF` | `PPPF` | no |
| K5 | good | root-drops | `PFPP` | `PFPP` | no |
| K6 | good | none | `PFFF` | `PFFF` | no |
| K7 | absent | good | `FPPP` | `FPPP` | no |
| K8 | corrupt | good | `FPPP` | `FPPP` | no |

**No case's derived vector differs from the frozen table in
`plans/round-71-claims.md`.** All eight `agree=True`, `mismatches=0`, `setup=0`; all eight staged
`case_sha256` values are distinct (`e96b…`, `f030…`, `6d6d…`, `ec3e…`, `ae94…`, `6317…`, `c136…`,
`82c9…`), so K2/K3 (both `PPFP`) price different mechanisms from different bytes.

Per-leg witness matrix recomputed from the `LEGS` lines (this is what `LEG-COVERAGE` sums):

| leg (file order) | P cases | F cases | both? |
|---|---|---|---|
| L1 `test_model_downloaded` | K1–K6 | K7, K8 | yes |
| L2 `test_flask_api_running` | K1–K4, K7, K8 | K5, K6 | yes |
| L3 `test_sentiment_endpoint` | K1, K4, K5, K7, K8 | K2, K3, K6 | yes |
| L4 `test_api_error_handling` | K1, K2, K3, K5, K7, K8 | K4, K6 | yes |

## 3. Independent re-derivation of the digest bindings

Recomputed from committed bytes at tip `d8a77d3f` (all read-only):

```
$ sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py
61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857   # == GRADER_SHA256 in claims
$ sha256sum corpus/evidence/round71/hf/instruction.md
29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1   # == INSTRUCTION_SHA256
$ sha256sum corpus/evidence/round71/hf/model/*      # per-file digests, 5 files
2a5cd25c… config.json / 17a8afc7… model.safetensors / fab2332d… tokenizer.json
d4256a55… tokenizer_config.json / b1291273… vocab.txt
$ (probe's exact tree_digest algorithm: sha256 of sorted "<sha>  <relpath>\n")
TREE c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944 MATCH True
$ git cat-file -p master:plans/round71_c1_hf_probe.py | sha256sum
d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e   # == PROBE and PROBE_BLOB
$ git ls-tree -r --name-only d8a77d3f -- corpus/evidence/round71 corpus/evidence/round52/graders/hf-model-inference plans/round71_c1_hf_probe.py
corpus/evidence/round52/graders/hf-model-inference/tests/test.sh
corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py
corpus/evidence/round71/hf/instruction.md
corpus/evidence/round71/hf/model/{config.json,model.safetensors,tokenizer.json,tokenizer_config.json,vocab.txt}
plans/round71_c1_hf_probe.py
```

So the four digest bindings (GRADER, INSTRUCTION, MODEL tree, PROBE/PROBE_BLOB) re-derive from
bytes committed at the lane tip, and the receipt's `REV` equals that tip.

Live witnesses (`corpus/evidence/round71/hf/sandbox/`, 8 case dirs × 4 files, 32 files, 120 K):
each case has `manifest.json` (case id, `case_sha256`, model/server modes, `legs`, `exc`,
`detail`, `sandbox_rc`) plus `app-tree.txt`, `sandbox-stdout.txt`, `sandbox-stderr.txt`. Quoted
end-state details:

- K5 (`root-drops`), `sandbox-stdout.txt`:
  `{"detail": {"test_flask_api_running": "AssertionError: Could not connect to the Flask API on 0.0.0.0:5000"}, "exc": {}, "legs": {"test_api_error_handling": "P", "test_flask_api_running": "F", "test_model_downloaded": "P", "test_sentiment_endpoint": "P"}, "ready": false, "server": true, "server_pid": 3}`
  — the server is up, `/` refuses, `/sentiment` answers: exactly the one failing mode a live
  listener can have (claims §R71-C1 limitation iv).
- K6 (`none`), `sandbox-stdout.txt`: L2 `AssertionError: Could not connect to the Flask API on
  0.0.0.0:5000`; L3/L4 raise `ConnectionError … [Errno 111]` and are scored F with the `EXC`
  line recording them (the distinction round 70's limitation (iii) asked a successor to price).
- K7 (`absent`) manifest: `"detail": {"test_model_downloaded": "AssertionError: Model directory not found"}`.
- K8 (`corrupt`) manifest: `"detail": {"test_model_downloaded": "AssertionError: Failed to load model or tokenizer: It looks like the config file at '/app/model_cache/sentiment_model/config.json' is not a valid JSON file."}`.

## 4. Calibration notes / risks (reported, not remediated)

1. **SKILL.md counters are still pre-move.** `grep -c 'executed 3 of 8' SKILL.md` → `1`;
   `grep -c 'executed 4 of 8' SKILL.md` → `0` (row `| network-service | 8 | …` at `SKILL.md:78`
   still reads `executed 3 of 8`). The claim's counting command wants 0/1 *after* the row move;
   the row move is a lane edit not assigned to this seat, so I did not touch `SKILL.md`. The
   receipt above is the evidence that authorises it.
2. **`SUMMARY` carries `exc=2` beyond the predicate sentence's token** (`SUMMARY cases=8 legs=32
   mismatches=0 setup=0`). The checker recomputes that field from the `EXC` lines
   (`plans/round71_c1_hf_probe.py:709-710`, `f"… exc={exc_n}"`), so the extra field is expected,
   not drift: `exc_n = 2` is exactly K6's two connection-error legs. `DEFECTS n=0` confirms the
   checker's rule, not a tolerant substring match.
3. **Port 5000 during/after the run.** Free before the battery (empty `ss` table). During the
   battery all served cases ran inside `bwrap` with `net=shared`; K5 deriving `PFPP` and K6
   `PFFF` is the in-run proof no foreign listener answered. After my battery exited, a listener
   appeared (`ss -ltnp`: `python3 pid=807885` → `/probe/harness.py server` from
   `/venv/bin/python3 /app/server.py`, parent `/probe/harness.py`): it belongs to sibling seats
   serialised on the same lock — `ps` shows `l1-selftest` (pid 772836) and `HfBatteryReplicate`
   (pid 773320) both started 22:21:53, i.e. after my 52 s battery window ended. Not a leak from
   this seat.
4. **Untracked evidence at this moment.** `git status --porcelain` shows
   `?? corpus/evidence/round71/hf/receipt.txt`, `?? …/check.txt`, `?? …/sandbox/` (also a
   sibling's `sandbox-replicate/`): the receipt of record becomes committed bytes when the L1
   commits. The claim's "re-derive from committed bytes" bindings (GRADER, INSTRUCTION, MODEL,
   PROBE_BLOB) are already committed at `d8a77d3f`.
5. **Do-nothing control not run by this seat.** The claims file's kill rule requires the eight
   ids staged with no model/service to derive `FFFF` and the counter to print fail; that is the
   `KengakuR71` seat's item in this wave. This seat only reports the battery + checker.
6. **Tooling.** No tool installed or upgraded (nothing needed); no source, predicate, case table,
   vector or digest edited.

## 5. Verdict

`PREDICATE R71-C1 pass` holds on the receipt of record
`corpus/evidence/round71/hf/receipt.txt`: all eight `VECTOR` lines `agree=True` with
`derived` equal to the frozen table, `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`,
`SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2`, `setup=0`, and `--check-receipt` exits `0`
with `DEFECTS n=0`. **No case diverges from the frozen table.** The only remaining
round-visible step for R71-C1 is the `network-service` row move in `SKILL.md` (3 → 4 of 8),
which is the L1's write, not this seat's.
