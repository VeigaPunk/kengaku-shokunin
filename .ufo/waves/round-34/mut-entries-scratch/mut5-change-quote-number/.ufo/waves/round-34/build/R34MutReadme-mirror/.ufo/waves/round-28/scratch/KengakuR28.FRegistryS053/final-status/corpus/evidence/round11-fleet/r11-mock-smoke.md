# Round-11 MOCK schema smoke — run_r11.py vs mock_server_r11.py (2026-09-28)

Empirical schema smoke of the round-11 runner against a stdlib mock endpoint on
`127.0.0.1:18113`, n=2 (pids 201–202), per `probe_plan_r11.md` §4 scaled to n=2.
The real served endpoint (`127.0.0.1:34113`) received **zero requests** —
guarantee mechanism in §"Zero real-endpoint requests" below.

## 1. Commands executed

Mock (started and killed inside the same shell as the run — background processes
are reaped across shell sessions here; an earlier cross-call attempt died and
produced 4× `ConnectionRefused` error records before this discipline):

```sh
python3 corpus/evidence/round11-fleet/mock_server_r11.py 18113 > /tmp/r11-mock/mock.log 2>&1 &
sleep 0.7
KENGAKU_R11_BASE=http://127.0.0.1:18113/v1/chat/completions KENGAKU_R11_N=2 \
  KENGAKU_R11_OUT=/tmp/r11-mock python3 corpus/evidence/round11-power/run_r11.py \
  > /tmp/r11-mock/run.log 2>&1
kill $MPID
```

**Attempt 1 (task's literal command): exit=1 — DEFECT FOUND.** The committed
`run_r11.py` uses `json.dumps`/`json.load` (its `log()` wrapper, `descriptors()`,
`ladder()`, SUMMARY re-read) but never imports `json` (import block is lines
19–25: `importlib.util, hashlib, os, subprocess, sys, time, urllib.request`).
It aborts on its very first record:

```
File "corpus/evidence/round11-power/run_r11.py", line 51, in log
    p.LOGF.write(json.dumps(rec, separators=(",", ":")) + "\n")
NameError: name 'json' is not defined. Did you forget to import 'json'?
```

Census of attempt 1: 0 records. Preserved at `/tmp/r11-mock/run.log.unshimmed`.

**Attempt 2 (schema exercise): exit=0**, identical env plus a runtime-only shim
that adds the missing import WITHOUT touching the committed file:

```sh
env KENGAKU_R11_BASE=http://127.0.0.1:18113/v1/chat/completions KENGAKU_R11_N=2 \
  KENGAKU_R11_OUT=/tmp/r11-mock http_proxy=http://127.0.0.1:18113 no_proxy= \
  python3 -c "import builtins, json, runpy; builtins.json = json; \
              runpy.run_path('corpus/evidence/round11-power/run_r11.py', run_name='__main__')"
```

All §4 criteria below are evaluated on attempt 2's bytes
(`/tmp/r11-mock/results-r11.jsonl`, 47 lines; run.log copied to
`mock-run.log`; first 20 jsonl lines copied to `mock-results-head.jsonl`).

## 2. Census — observed vs expected (§4 scaled to n=2)

Source: `python3 /tmp/r11-mock/check_r11.py` (throwaway checker, since deleted)
over `/tmp/r11-mock/results-r11.jsonl`.

| record class | expected | observed | |
|---|---:|---:|---|
| `cell:"descriptors"` | 1 | 1 | PASS |
| `cell:"meta"` | 2 | 2 | PASS |
| graded `A-CKPT4710` (2 pid × 3 turns) + `A-CKPT710` (2 × 2) | 6 + 4 = 10 | 6 + 4 = 10 | PASS |
| ack `A-CKPT4710-ack` (2 × 7) + `A-CKPT710-ack` (2 × 8) | 14 + 16 = 30 | 14 + 16 = 30 | PASS |
| `cell:"filler"` | 4 | 4 | PASS |
| `cell:"error"` | 0 | 0 | PASS |
| **total records** | **47** | **47** | PASS |
| endpoint requests (1 models GET + 2×22 POST) | 45 | GET=1 POST=44 | PASS |

## 3. §4 criterion-by-criterion

All verified by the checker output (30 checks, 30 PASS after fixing the
checker's own compactness heuristic — see note at the end):

| §4 criterion | verdict | evidence |
|---|---|---|
| census (table above) | PASS ×7 | checker `census.*` |
| request count 45 | PASS | `grep -c POST mock.log` = 44; models GET = 1 |
| every non-meta record has `request_ts`; metas do NOT | PASS | `request_ts.nonmeta` / `request_ts.meta_absent`; format `^\d{4}-..T..:..:..Z$` all match |
| graded carry ok/nwrong/got/want/finish/usage/wall_s/raw | PASS | exact key-set equality `set(r)=={cell,pid,turn,ok,nwrong,got,want,finish,usage,wall_s,raw,request_ts}` for all 10 |
| ack records exact keys {cell,pid,turn,raw,finish,usage,wall_s,request_ts}, raw ≤80 chars | PASS | maxlen=80 (spillover truncation fired) |
| filler exact keys {cell,finish,usage,wall_s,raw,request_ts}, raw="ready" | PASS | all 4 raws "ready" |
| meta exact keys {cell,pid,init,ops,truth,tail_touched} | PASS | exact-set check ×2 |
| `want == meta.truth[turn−1]` for every graded record | PASS | 10/10, mismatches=[] |
| SUMMARY exactly 2 lines matching `^(A-CKPT4710|A-CKPT710): \d+/2$` | PASS | `A-CKPT4710: 0/2` / `A-CKPT710: 0/2` (denominator = with-turn-10 records = 2 ✓; passes 0 because the mock emits a fixed state, not problem-correct state) |
| counterbalance in run.log job order (201 odd → 710 first; 202 even → 4710 first) | PASS | `[1/4] ('A-CKPT710', 201) [2/4] ('A-CKPT4710', 201) [3/4] ('A-CKPT4710', 202) [4/4] ('A-CKPT710', 202)` |
| ≥1 graded record parsed via brace-fallback (no fence in raw, got is dict) | PASS | 3 records: (710,201,t10), (710,202,t10), (4710,201,t10); e.g. raw=`{"nails": 12, "bolts": 3, ...}` fenceless → got=parsed dict |
| ≥1 parse-fail (got null), nwrong=len(want) | PASS | 3 records: (4710,201,t4) nwrong=5=len(want), (4710,202,t4) nwrong=6, (710,202,t7) nwrong=6; raw=`'{"nails": 12, "screws": }'` |
| fenced-parse path also exercised | PASS | 4 fenced graded records (mock modulo c%3==0) |
| descriptors has `server` + `machinery_sha256` (64 hex) | PASS | server={pid:1299, argv:[~/.local/bin/llama-server, …]} from /proc; machinery_sha256=`cf754d78e9065d67…` (64 hex) == recomputed sha256 of probe_r11.py |
| models_json captured from GET /v1/models | PASS | `{"data": [{"id": "mock-model"}]}` |
| JSONL compact `separators=(',',':')` | PASS | round-trip `json.dumps(json.loads(l), separators=(',',':')) == l` for all 47 lines (a naive `'": ' not in line` grep false-fails on spaces inside string VALUES) |
| finish/usage sane (finish="stop", usage.total_tokens>0) | PASS | all 44 chat records |

## 4. Zero real-endpoint requests — guarantee

`run_r11.py` hardcodes `HOST = "http://127.0.0.1:34113"` (line 26) for the
descriptors' `GET /v1/models`; `KENGAKU_R11_BASE` only redirects
`probe_r11.call`. Since editing `run_r11.py` is out of scope for this smoke,
ALL urllib traffic was routed through the mock by setting
`http_proxy=http://127.0.0.1:18113 no_proxy=` on the run process. Verified
mechanics:

- `urllib.request.proxy_bypass('127.0.0.1')` → `False` under this env, so no
  bypass path exists;
- decoy probe before the run: `GET http://127.0.0.1:9/v1/models` (port 9 has no
  listener) returned `{"data":[{"id":"mock-model"}]}` and produced
  `20:20:33 INTERCEPT GET 127.0.0.1:9/v1/models` in mock.log — interception
  proven without touching 34113;
- during attempt 2, mock.log line 2:
  `20:22:57 INTERCEPT GET 127.0.0.1:34113/v1/models -> models` — the would-be
  real-endpoint request landed on the mock and was answered there; the other 44
  requests are `DIRECT POST 127.0.0.1:18113/...`. No socket to 34113 was ever
  opened by this smoke (structurally impossible: every urllib connection from
  the run process terminated at the proxy/mock).

## 5. Mock server quirks

1. **Content policy** keys on the LAST user message: `'ready'` → "ready";
   `"Reply 'ok'"` → "ok"; `'CHECKPOINT'` (graded turns only — the ask text
   distinguishes them) → fixed modulo c%3: fenced / bare / malformed;
   otherwise (turn-1 and post-checkpoint spillover FULL asks) → full-state
   emit alternating fence/bare. All tags visible in `mock.log`.
2. Fixed emitted state `{"nails": 12, "bolts": 3, "screws": 7, "washers": 0,
   "hinges": 5}` is intentionally NOT problem-correct → all graded ok=False,
   SUMMARY `0/2` twice; graders still fully exercised (nwrong distribution,
   parse-fail nwrong=len(want)).
3. Answers absolute-form (proxy) request lines by stripping `scheme://host`;
   tags non-self targets `INTERCEPT`.
4. Usage: prompt_tokens=100, completion_tokens=len(content)//4 (≥1).
5. HTTP/1.1 with Content-Length; ThreadingHTTPServer; stdlib only.

## 6. Runner quirks observed (not introduced by the mock)

- **BLOCKER:** missing `import json` (§1, attempt 1) — main run would die at
  descriptors before any graded request.
- `probe_r11.py` opens `{OUT}/results.jsonl` at import time → stray empty file
  next to `results-r11.jsonl` (pre-existing r9 lineage behavior, harmless).
- descriptors `endpoint` field records the intended real URL string
  (`http://127.0.0.1:34113`) even though models_json was captured from the
  mock via proxy interception — faithful to what the code does; do not read
  that field as proof of endpoint contact.
- `server` argv comes from `pgrep -f llama-server` + `/proc/<pid>/cmdline` — it
  pinned the REAL llama-server process (read-only); expected on the real run.

## 7. Verdict

Schema contract: 30/30 criteria PASS on the mock (§2–§3). Runner as committed:
FAIL — aborts at first record without the one-line `import json` fix.

MOCK SMOKE: FAIL (run_r11.py missing `import json` → NameError exit 1 at descriptors/first record; all §4 schema criteria PASS under the documented builtins.json runtime shim — main run is blocked until the import is added to corpus/evidence/round11-power/run_r11.py)
