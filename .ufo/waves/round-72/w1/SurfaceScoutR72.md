# SurfaceScoutR72 — per-surface reconnaissance, round 72 w1

Seat: `SurfaceScoutR72` (leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read in full before any command: `plans/round-72-claims.md` (sha256 `00faf850…29ce9c`).
Survey instant: 2026-11-03T02:09Z–02:12Z (`date -u` → `Wed 04 Nov 2026 02:12:24 AM UTC`; the lane's
clock labels this round 2026-11-03).
No predicate, case table, vector, digest, kill rule or target was edited. All writes are this file
plus one throwaway probe under my scratch, deleted before the seat ended.

**What I did not run, and therefore have not passed:** the battery, `--check-receipt`, `--selftest`,
`--mutants`, `--control`, `--stub-control`, and `round72_c2_routed_defects.py`. Every instrument
statement below is either (a) read from committed source/receipt bytes, or (b) a live host probe named
with its command. Two sibling seats own those runs (`R1Reviewer-7`, `E2Routed`); I did not duplicate
them and I do not report their verdicts as mine.

---

## 1. The class row: `network-service`, 8 members, 4 executed

### The row as it stands

`SKILL.md:78` (in `## Decision table — grader class → offline replay recipe`; the header row is the
`| class | count | executed | replay recipe | receipt pointer |` line immediately above it),
`grep -n 'executed 4 of 8' SKILL.md` → one hit, exit 0. Row fields, verbatim:

- class `network-service`, count `8`, executed `4 of 8`.
- The four are named in the row with their round and receipt: round 64 `kv-store-grpc`; round 68
  `pypi-server` (`R68-C1 pass`, corrected stderr clause; the round-63 receipt stays MISS and L0
  `kengaku round-63` stays open); round 69→70 `nginx-request-logging` (r69 MISS on leg-coverage; r70
  re-froze the table with two missing red witnesses at seven vectors, `56/56 legs`,
  `LEG-COVERAGE legs=8 seen_p=8 seen_f=8`, counted from round 70); round 71 `hf-model-inference`
  (`PREDICATE R71-C1 pass`, eight vectors, `32/32 legs`, `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`,
  `mismatches=0`, counted from round 71).
- Receipt pointers in that row: `corpus/evidence/round52/graders/kv-store-grpc/tests/test_outputs.py`,
  `corpus/evidence/round64/kvstore-probe.txt`,
  `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt`,
  `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`,
  `corpus/evidence/round71/hf/receipt.txt`.

### The eight members and the split

`corpus/evidence/round62/class-survey.txt:11` (raw):

```
CLASS network-service count=8 members=filter-js-from-html,git-multibranch,headless-terminal,hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server
```

| member | executed? | where the evidence is |
|---|---|---|
| `kv-store-grpc` | **yes**, round 64 | `corpus/evidence/round64/kvstore-probe.txt`; entry `tb2-kv-store-grpc-offline.md` |
| `pypi-server` | **yes**, round 68 | `corpus/evidence/round63/pypi-probe-run1-literal-detector-fail.txt` (the MISS of record) and the R68 corrected run; entry `tb2-network-service-offline-grader.md` |
| `nginx-request-logging` | **yes**, counted from round 70 | seven-vector table, 56/56 legs; entry `tb2-nginx-request-logging-offline.md` |
| `hf-model-inference` | **yes**, round 71 | `corpus/evidence/round71/hf/receipt.txt`; entries `tb2-hf-model-inference-offline.md`, `tb2-hf-model-inference-provenance.md` |
| `filter-js-from-html` | no | classified `subprocess-exec` + `file-artifact` + other rows; no class-replay receipt |
| `git-multibranch` | no | classified `subprocess-exec` + `shell-exec` + `file-artifact`; no class-replay receipt |
| `headless-terminal` | no | classified `subprocess-exec` + `candidate-import` + `file-artifact`; no class-replay receipt |
| `install-windows-3.11` | no | also the one recipe-unexecuted member of `process-environment` (`SKILL.md:81`), so it is blocked in two classes at once |

Corroboration independent of the row: exactly four `tb2-*-offline*.md` knowledge entries exist for
this class (`tb2-kv-store-grpc-offline.md`, `tb2-network-service-offline-grader.md` [pypi-server],
`tb2-nginx-request-logging-offline.md`, `tb2-hf-model-inference-offline.md` +
`tb2-hf-model-inference-provenance.md`), and no entry names any of the other four as replayed.
`install-windows-3.11` is named in `benchmark-task-validity-checklist.md`,
`benchmark-verifier-execution-model.md`, `tb2-grader-class-census.md` — census/triage contexts, not a
replay.

### Findings on this surface (reported, not edited)

- **F1.1 — the census receipt's own coverage line is stale and contradicts the row.**
  `class-survey.txt:22` reads `EXECUTED-COVERAGE executed=17 classified=17 classes-covered=12
  classes-uncovered=network-service,process-environment,db-state,container-image`. It is a round-62
  artifact; the row counts `network-service` as 4-of-8 from round 64 on, `process-environment` as
  2-of-3 from round 66/67, `db-state` as 1-of-2 from round 65. Anyone re-deriving class coverage
  from the census file alone gets `network-service` uncovered. The row is right; the census line is
  the round-62 snapshot and carries no supersession marker. Not a claim defect, but a successor
  reading the census first will be misled.
- **F1.2 — the row's `replay recipe` cell has no recipe for the member that moved the row.**
  The cell describes the gRPC recipe (lane-built server on `127.0.0.1:5328` under bubblewrap) and the
  PEP 503 recipe (`pypi-server` on `127.0.0.1:8080`). `hf-model-inference` contributes a receipt
  pointer and an executed-count sentence but **no recipe text** — the `bwrap --clearenv` +
  nine-variable allowlist + in-sandbox `transformers.__file__` pattern is only in the knowledge entry
  and the probe. This is the same shape as R71-R1 (registry completeness) one table over: a member
  counted as executed whose method is not stated where the class table states methods. It is not a
  C1 or C2 predicate clause and I did not touch it.

---

## 2. Assert-site inventory of `tests/test_outputs.py` — 7 priced / 19 total

File: `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`, 107 lines, 4239
bytes, `sha256sum` → `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`, which is
exactly the frozen `GRADER_SHA256` (`plans/round72_c1_hf_probe.py:79`) and the pin quoted in the
claim. `grep -c 'assert'` → **19**.

Legs run in file order and the harness marks a leg `F` on the first `AssertionError` (or on any other
exception, flagged `E`), so an assert is reachable only if every earlier assert in its leg passed.
That ordering is what makes the classification below a control-flow claim, not a text match.

`P` = some case in the frozen nine-case table can turn this site red; `U` = none can.

| line | assert (abridged) | leg | class | priced by / why unreachable |
|---|---|---|---|---|
| 13 | `os.path.exists("/app/model_cache/sentiment_model")` | 1 | **P** | K7 `absent` — manifest detail `Model directory not found` |
| 19 | `model is not None` | 1 | **U** | no frozen model mode makes `from_pretrained` *return* `None`; `corrupt` raises and lands on `:22` |
| 20 | `tokenizer is not None` | 1 | **U** | same; a corrupt tokenizer also raises into `:22` |
| 22 | `assert False` (the `except Exception`) | 1 | **P** | K8 `corrupt` — detail `… config.json is not a valid JSON file` |
| 31 | `assert False` (the `except ConnectionError`) | 2 | **P** | K5 `root-drops` and K6 `none` — both details `Could not connect to the Flask API on 0.0.0.0:5000` |
| 50 | `response.status_code == 200` | 3 | **U** | no server mode answers a non-200 status on a valid POST; K6 never reaches it (POST raises) |
| 56 | `"sentiment" in result` | 3 | **U** | no mode drops the field |
| 57 | `"confidence" in result` | 3 | **U** | no mode drops the field |
| 58 | `"positive" in result["confidence"]` | 3 | **U** | no mode drops the key |
| 61 | `"negative" in result["confidence"]` | 3 | **U** | no mode drops the key |
| 67 | `positive > negative` (label positive branch) | 3 | **U** | every staged body is internally ordered; K2's flip also flips the confidences |
| 71 | `negative > positive` (else branch) | 3 | **U** | same |
| 76 | `isinstance(result["sentiment"], str)` | 3 | **U** | no mode returns a non-string sentiment |
| 77 | `isinstance(positive, float)` | 3 | **P** | K3 `int-confidence` — detail `Confidence scores should be floats` |
| 80 | `isinstance(negative, float)` | 3 | **U** | K3 makes both ints and aborts at `:77`, so `:80` is never reached in `F` |
| 86 | `sentiment == "positive"` (is_positive) | 3 | **P** | K2 `wrong-label` — detail `Text The journey was not bad; … should be classified as positive` |
| 90 | `sentiment == "negative"` (not is_positive) | 3 | **U** | no mode answers positive for a negative-expected text |
| 103 | `status_code == 400` | 4 | **P** | K4 `no-400` — detail `API should return 400 for invalid request format` |
| 107 | `"error" in error_data` | 4 | **P** | K9 `400-no-error-field` — detail `Error response should contain 'error' field` |

**Count: 7 priced / 19 total** (36.8%). Distinct priced sites: `{13, 22, 31, 77, 86, 103, 107}`;
12 unpriced: `{19, 20, 50, 56, 57, 58, 61, 67, 71, 76, 80, 90}`.

Per-case site map (one case, one site, except K6 which prices `:31` and two exception-reds):

`K1` none · `K2 :86` · `K3 :77` · `K4 :103` · `K5 :31` · `K6 :31` (+ `E` on legs 3,4) · `K7 :13` ·
`K8 :22` · `K9 :107`.

**Cross-check.** `corpus/knowledge/tb2-hf-model-inference-provenance.md:61` states "Round 71 named 6
of 19 assert sites priced; K9 makes it 7." I re-derived both numbers independently from the file and
the manifests: round 71's eight cases price `{13, 22, 31, 77, 86, 103}` = 6; K9 adds `107` = 7. The
entry is correct.

**Finding F2.1 — two leg-witnesses in the nine-case table are exception-witnesses, not assert
witnesses.** Under K6, legs 3 and 4 are `F` via uncaught `requests.exceptions.ConnectionError`
(`sandbox/K6/manifest.json` `exc: {test_api_error_handling: E, test_sentiment_endpoint: E}`), and the
receipt's `SUMMARY` says `exc=2`. This is faithful to the real runner — `tests/test.sh` writes reward
`1` only on `pytest` exit 0, and an errored test is non-zero — but it means K6 proves "no listener ⇒
fail", not "a specific assert fired". A reader counting 36 leg-witnesses as 36 assertion-witnesses
overcounts by 2.

**Finding F2.2 — the advance is not in any headline metric.** `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`
in `corpus/evidence/round72/hf/receipt.txt` is byte-identical to round 71's, and every one of the ten
cheapest successor cases in §4 also derives `PPPF`. The ninth case's coverage move exists only in the
per-case `detail` text and in prose (the entry's 7/19). The counter cannot currently express it; see
§4.

**Finding F2.3 — the receipt has no assert-site field.** `battery_lines()` writes
`CASE/LEGS/EXC/VECTOR` only (`plans/round72_c1_hf_probe.py:591-640`); the `detail` dict with the
`AssertionError` message exists in the sandbox `manifest.json` and `sandbox-stdout.txt` but never
enters the receipt. So "K9 prices `:107`" is verifiable by a human reading
`sandbox/K9/sandbox-stdout.txt` (`AssertionError: Error response should contain 'error' field`), and
not verifiable by `--check-receipt`. The claim's limitation (v) already concedes the receipt is a
consistency check over bytes; this is the concrete consequence.

---

## 3. Host facts, re-verified live

One block, one shell, verbatim output:

```
$ date -u
Wed 04 Nov 2026 02:12:24 AM UTC
$ bwrap --version
bubblewrap 0.13.1
$ ss -ltn 'sport = :5000'
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
$ /fast/ComfyUI/.venv/bin/python3 -c "import sys, torch, transformers, requests; print(sys.version.split()[0], torch.__version__, transformers.__version__, requests.__version__)"
3.13.16 2.14.1+cu130 5.21.0 2.34.2
```

Exit 0 for the block; each command exit 0. The versions match the receipt's own
`LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0 requests=2.34.2` exactly.

### Port 5000 — four samples, it flaps

| sample | command | output |
|---|---|---|
| 1 — `02:09:04Z` | `ss -ltn 'sport = :5000'` | `LISTEN 0 5 0.0.0.0:5000 0.0.0.0:*` |
| 1 — same instant | `ss -ltnp 'sport = :5000'` | `LISTEN 0 5 0.0.0.0:5000 0.0.0.0:* users:(("python3",pid=2122758,fd=3))` |
| 2 — untimestamped, ≈`02:10:4xZ` | `ss -ltnH 'sport = :5000'` | *(no rows)* |
| 3 — `02:11:52Z` | `ss -ltnH 'sport = :5000'` | `LISTEN 0 5 0.0.0.0:5000 0.0.0.0:*` |
| 4 — `02:12:24Z` | `ss -ltn 'sport = :5000'` | header only |

At sample 1 the listener was `python3` pid 2122758; by sample 2 that pid no longer existed
(`ps -p 2122758` → rc 1, `tr < /proc/2122758/cmdline` → ENOENT). At sample 3 a **different** listener
held the port and `ps -ef | grep -c '[p]ython3 /app/server.py'` → `1`. That path is the probe's own
staged candidate (`SERVER_TMPL` writes `/app/server.py`), so samples 1 and 3 are sibling seats'
batteries holding the shared port for one case at a time.

Consequence: `--port-lock` is load-bearing and its absence is **loud, not silent** — `run_case()`
calls `wait_port_free(5000)` (20 s) and returns `derived="SETUP"`, `sandbox_rc=1`, which makes
`setup=1` and fails the predicate under the frozen kill rule. A *foreign* persistent listener would
make the battery unrunnable and would present as SETUP too; the probe cannot tell a sibling from a
foreign process, and that is a property of the shared-port design, not a bug.

### Two extra sandbox environment keys, and one bwrap fact

`corpus/evidence/round72/hf/sandbox/K1/manifest.json` `prov.env_keys` (raw, 11 comma-separated keys):

```
HF_HUB_OFFLINE,HOME,LANG,PATH,PWD,PYTHONNOUSERSITE,PYTHONPATH,PYTHONWARNINGS,TMPDIR,TORCHINDUCTOR_CACHE_DIR,TRANSFORMERS_OFFLINE
```

`ENV_ALLOW` (`plans/round72_c1_hf_probe.py:99`) declares nine:
`PATH, HOME, LANG, PYTHONPATH, PYTHONNOUSERSITE, PYTHONWARNINGS, TMPDIR, HF_HUB_OFFLINE,
TRANSFORMERS_OFFLINE`. So the sandbox sees **two keys the allowlist does not name**.

- `PWD` is bwrap's own. Measured: `bwrap --clearenv --unshare-all --ro-bind /usr /usr --ro-bind /lib
  /lib --ro-bind /lib64 /lib64 --ro-bind /bin /bin --chdir / --proc /proc --dev /dev /bin/env` →
  `PWD=/`, exit 0. With `--chdir /app` that is `PWD=/app`, matching `prov.cwd`.
- `TORCHINDUCTOR_CACHE_DIR` is created **inside** the sandbox after exec: it is absent from the parent
  shell (`env -u TORCHINDUCTOR_CACHE_DIR` and a plain read both show unset), and it is absent from
  K7's `prov.env_keys` (10 keys, no `TORCHINDUCTOR_CACHE_DIR`, model absent so
  `from_pretrained` never runs) while present in K1–K6, K8, K9. It is therefore not inherited; it is
  produced by the graded process's own import/load path. *(I did not isolate which library sets it —
  a bare `import torch`, `import transformers`, `from transformers import
  AutoModelForSequenceClassification`, and a failing `from_pretrained("/nonexistent-…")` on the host
  venv all left it unset; the sandbox's successful `from_pretrained` does. Marked `[INFERENCE]` past
  the "not inherited" step.)*

This does not break the provenance witness — `canary_seen=0` is the independent witness that the
parent environment did not leak, and it is the clause that makes the rest sound. But the metric is
named misleadingly: `allowlist_seen=9/9` is computed as
`set(env_keys) >= set(allow_names)` (`:611-613`), a **superset** test, so it can never report 10/9 or
11/9 and cannot detect an extra key. `corpus/knowledge/tb2-hf-model-inference-provenance.md:34`
says "the sandbox's environment is exactly the `--setenv` list" and then excepts `PWD`; as measured
it is the setenv list **plus `PWD` plus whatever the graded process creates** (11 keys). That is a
strictly-false sentence in a round-72 document, of the same family the round is closing as R71-R7,
though it is a paraphrase in a knowledge entry and not a freeze-doc label. Reported, not edited.

### Instrument-drift check (free, worth having)

`sha256sum plans/round72_c1_hf_probe.py` → `99867c7f080179b44f30e7887c2f0a6c434217a1ec49cd2fbc1b23981faa637e`,
which equals the receipt's `PROBE sha256` and `PROBE_BLOB sha256`; `git rev-parse HEAD` →
`b6336136e0e891522b113a94d8e0bd65e0eae8de`, which equals the receipt's `REV`. At survey time the
receipt of record was produced by the current probe bytes at the current tip: no drift.

`plans/round72_c2_routed_defects.py` sha256 `2d81ad80…c78758`; `plans/round-72-claims.md` sha256
`00faf850…29ce9c`.

### Live wave state at survey time (not verdicts)

- `corpus/evidence/round72/hf/receipt.txt` — nine `VECTOR … agree=True`, `LEG-COVERAGE legs=4 seen_p=4
  seen_f=4`, `SUMMARY cases=9 legs=36 mismatches=0 setup=0 exc=2`, `PREDICATE R72-C1 pass`,
  `PROVENANCE … canary_seen=0 … transformers_file=/venv/lib/python3.13/site-packages/transformers/__init__.py`.
- `.ufo/waves/round-72/c1-control.txt` — all nine `derived=FFFF`, `mismatches=9`, `exc=18`,
  `seen_p=0`, `PREDICATE R72-C1 fail`: the do-nothing control is red as the claim requires. Its nine
  `case_sha256` values are all `01ba4719…a546b` = `sha256("\n")`, i.e. the digest of an empty staged
  file list — the control provably staged nothing. Note it still prints a full `PROVENANCE` line with
  `transformers_file=/venv/…`, so provenance alone is necessary and **not** sufficient; the vector and
  coverage lines are what refuse it.
- `corpus/evidence/round72/hf/stub-control.txt` — **absent** (also no `*stub*` file anywhere under
  `corpus/evidence/round72/` or `.ufo/waves/round-72/`). Counting command 3 of R72-C1 has no receipt
  on disk yet, re-checked at 02:14Z.
- `corpus/evidence/round72/c1-selftest.txt` — **changed under this seat**: 0 bytes at first `ls`,
  132 bytes when read seconds later, 2814 bytes at re-read (mtime 02:12Z). Current bytes: all nine
  cases plus
  `LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `SUMMARY … exc=2`, `PREDICATE R72-C1 pass`, then eight
  refused arms — `vector_flip`, `legs_flip`, `coverage_flip`, `drop_case`, `case_digest` (re-scored
  against the staged tree, the R71-R4 fix), `drop_k9`, `provenance_env`, `provenance_path` — closing
  with `ARM accept genuine rc=0 accepted=True`, `ARM STAGED-STATE changes_on_byte=True
  PATH-INDEPENDENT sha_equal=True`, `SELFTEST red_refused=8/8 accept_ok=1 state_sensitive=1
  path_independent=1 ok=True`. Every red arm's defect output is present with its `DEFECT` lines.
- `corpus/evidence/round72/c2-green.txt` — `E1a/E1b/E1c/E2 ok`, `DEFECTS n=0`, `PREDICATE R72-C2
  pass`, `LANE_TIP b6336136…`, `EXIT=0`.
- `corpus/evidence/round72/c2-controls.txt` — **changed under this seat**: 258 bytes (mtime 02:10Z,
  selftest arms only), 1143 bytes (mtime 02:11Z). Current bytes carry both arms:
  `SELFTEST defects-in-fake=3 want=3 all-fail=True append-only-arm=True positional-arm=True
  parser-arm=True ok=True`, then seven `MUTANT` lines each with `accept_green=True escapes=1
  attribution_ok=True` (`M1-registry-columns`, `M2-registry-owner` → `E1a`; `M3-errata-labels`,
  `M4-errata-revisions` → `E1b`; `M5-errata-positional`, `M6-errata-last-section` → `E2`), the
  deliberate no-op `M7-null-comment … null=True verdict=null`, then
  `ARM accept-green=ok refuse-red=ok attribution=ok` and
  `MUTANTS total=7 killed=6 survived=0 invalid=0 null_detected=1`. That is the frozen mutant-metric
  sentence exactly, with per-mutant attribution. My earlier reading of this file (258 bytes) was a
  superseded state; the seat re-read it before writing this line.
- The four registry rows `round71-c1-hf-probe`, `round71-c2-routed-defects`, `round72-c1-hf-probe`,
  `round72-c2-routed-defects` are present at `SKILL.md:695-698`, each eight-column, kind
  `gate`/`probe`. `plans/round-71-claims.md:137` carries `## Errata — round 72 (2026-11-03)` with
  `E-R72-1` and both superseded labels kept above it. R71-R1 and R71-R7 are visibly closed in the
  committed bytes I read.

---

## 4. The remaining frontier: what a successor needs to price the 12 unpriced sites

### 4a. Grouping the 12, and reconciling the claim's "five"

`plans/round-72-claims.md:85` says "five assert groups remain red-unreachable under the frozen modes".
The asserts group naturally as follows:

| group | sites | count | priceable by a new case? |
|---|---|---|---|
| G1 loader returns `None` | `:19`, `:20` | 2 | **no** — only a `transformers` stub that returns `None` reaches them; the provenance witness exists to exclude exactly that, so this group is out of scope *by design* |
| G2 status 200 on `/sentiment` | `:50` | 1 | yes — one server mode |
| G3 response-field presence | `:56`, `:57`, `:58`, `:61` | 4 | yes — four server modes |
| G4 label/confidence consistency | `:67`, `:71` | 2 | yes — two server modes |
| G5 response typing | `:76`, `:80` | 2 | yes — two server modes (`:80` needs `:77` to pass) |
| G6 negative-expected label | `:90` | 1 | yes — one server mode |

So the honest count is **12 unpriced asserts in 6 groups**, of which **5 groups (10 sites) are reachable
by server-mode cases** and **1 group (2 sites) is reachable only by the stub control**. The claim's
"five" is correct if and only if G1 is excluded on the stated ground; the claim does not say so.
That is a one-clause imprecision, not a wrong number.

### 4b. The cheapest next cases — exact inputs, ordering guard, expected vector

Every one is a single new `SERVER_MODES` entry plus one `CASES` tuple with `model="good"`; the server
template already carries the `MODE` switch. Cost is uniform (≈3–6 lines each); what varies is the
**ordering guard** — the earlier asserts that must stay green for the target site to be reached. All
ten are `L3` reds and derive `PPPF` (`:50`–`:90` are all inside `test_sentiment_endpoint`), and all
are *new sites*, not new vectors.

| id (proposed) | server input (the POST body it answers) | must stay green or the wrong site fires | site | expected vector |
|---|---|---|---|---|
| N1 `status-500` | any valid text → `500` + `{"error": "boom"}` | nothing before `:50` | `:50` | `PPPF` |
| N2 `drop-sentiment` | `200` + `{"confidence": {"positive": 0.93, "negative": 0.07}}` | `:50` | `:56` | `PPPF` |
| N3 `no-confidence` | `200` + `{"sentiment": "positive"}` | `:56` | `:57` | `PPPF` |
| N4 `no-positive` | `200` + `{"sentiment": "positive", "confidence": {"negative": 0.07}}` | `:56`,`:57` | `:58` | `PPPF` |
| N5 `no-negative` | `200` + `{"sentiment": "positive", "confidence": {"positive": 0.93}}` | `:56`,`:57`,`:58` | `:61` | `PPPF` |
| N6 `inconsistent-pos` | `200` + sentiment `"positive"`, confidence `{"positive": 0.07, "negative": 0.93}` | `:56`–`:61` | `:67` | `PPPF` |
| N7 `inconsistent-neg` | `200` + sentiment `"negative"`, confidence `{"positive": 0.93, "negative": 0.07}` | `:56`–`:61` | `:71` | `PPPF` |
| N8 `sentiment-nonstr` | `200` + `{"sentiment": 1, "confidence": {"positive": 0.07, "negative": 0.93}}` | `:56`–`:71` — the confidence pair must be **negative-heavy** so the `else` branch passes | `:76` | `PPPF` |
| N9 `negative-int` | `200` + sentiment `"positive"`, confidence `{"positive": 1.0, "negative": 0}` | `:67` must hold (`1.0 > 0`) and `:77` must hold (`1.0` is a float) | `:80` | `PPPF` |
| N10 `negative-flipped` | `good` mode except the `"The service at this restaurant was terrible and the food was cold."` label flips to `positive` | text 1 passes; this fires on iteration 2 | `:90` | `PPPF` |

Two of these are traps a successor will hit without the guard column:

- N8 as "sentiment is an int, confidences 0.93/0.07 positive-heavy" reds `:71`, **not** `:76` —
  `if result["sentiment"] == "positive"` is false for `1`, so the `else` branch requires
  `negative > positive` before the `isinstance` check is reached.
- N9 as "negative is an int, positive 0.93" reds `:67`, **not** `:80` — `0.93 > 0` needs the negative
  to be *smaller*; use `1.0 > 0`.

And one that is not cheap and should not be attempted: G1 (`:19`, `:20`). Reaching it requires a
`transformers` whose `from_pretrained` **returns** `None` instead of raising — the exact artefact
`--stub-control` is built to prove invisible. A case that priced `:19` would have to be a stub arm
labelled as such, never a case in the provenance-witnessed table.

### 4c. What actually blocks the axis (the cheapest move is not a case)

The binding constraint is the **metric**, not the case supply.

1. `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` is saturated and was already saturated in round 71. Ten new
   cases — all `PPPF` — leave it unchanged. A reader comparing round 71 and round 72 receipts sees no
   coverage move at all, which is precisely why the claim has to carry the advance in prose and why
   the provenance entry has to say "6 of 19 → 7".
2. The receipt has no site field (F2.3). The `AssertionError` message is the only site evidence and it
   lives in `sandbox/<cid>/manifest.json`, which `--check-receipt` never reads.

Cheapest successor move, in order:

- **(i) Add `detail` to the receipt**, one line per red leg: `DETAIL <case> <leg> <message-digest>`.
  `battery_lines()` already has `r["detail"]`; this is a pure append to the writer, no new staging, no
  new case, no new run beyond the battery that already runs. It makes `:107` auditable from the
  receipt of record.
- **(ii) Add an assert-site line.** The harness catches `AssertionError as e`; `e.__traceback__` gives
  `tb_lineno` in `test_outputs.py` for free. `SITE <case> leg=<name> line=<n>` plus
  `ASSERT-COVERAGE sites_priced=<k>/19` turns the axis into a counter. Both are instrument changes and
  must be frozen *before* data by the round that adopts them — not by a seat mid-round.
- **(iii) Then** add N1–N10 as one wave, each with its guard recorded, and score `sites_priced` rather
  than `seen_f`. Ten cases move 7/19 → 17/19; G1 stays the declared 2-site residue, and the residue is
  then a *stated* exclusion instead of an unnamed gap.

Until (i)–(iii) land, adding cases is unmeasured work: the table can grow to nineteen cases and the
receipt will still say `legs=4 seen_p=4 seen_f=4`.

---

## Findings ledger (all reported, none edited)

| id | finding | severity |
|---|---|---|
| F0 | **my own instrument**: the in-shell `trap … EXIT` scratch removal did not fire; the tree survived one command and needed an explicit `rm -rf` (verified gone). A sibling running the same idiom should not trust the trap alone | self |
| F1.1 | `class-survey.txt:22` `EXECUTED-COVERAGE … classes-uncovered=network-service,…` is a stale round-62 line contradicting the round-72 row (4 of 8 executed), with no supersession marker | calibration |
| F1.2 | `SKILL.md:78` `replay recipe` cell states no recipe for `hf-model-inference` although the row counts it executed; the `--clearenv` provenance recipe lives only in the probe and the entry | coverage |
| F2.1 | K6's legs 3–4 are `E` (uncaught `ConnectionError`), not assert reds; `SUMMARY exc=2` says so, but "36 leg-witnesses" is 34 assertion-witnesses + 2 exception-witnesses | calibration |
| F2.2 | `LEG-COVERAGE` is identical to round 71 (`legs=4 seen_p=4 seen_f=4`); the ninth case's gain is expressible only in prose and `detail` | calibration |
| F2.3 | No assert-site field in the receipt; `:107` is auditable only from `sandbox/K9/manifest.json` / `sandbox-stdout.txt`, not by `--check-receipt` | coverage |
| F3.1 | Sandbox env carries 11 keys vs a 9-name allowlist (`PWD` from bwrap; `TORCHINDUCTOR_CACHE_DIR` created in-sandbox); `allowlist_seen=9/9` is a `>=` superset test that cannot detect extras | calibration |
| F3.2 | `tb2-hf-model-inference-provenance.md:34` says "the sandbox's environment is exactly the `--setenv` list"; measured, it is the list + `PWD` + process-created keys | calibration |
| F4.1 | Claim limitation (vi) says "five assert groups"; measured, 12 asserts fall in 6 groups, 5 server-priceable + 1 stub-only (`:19`,`:20`). The "five" is right only under an unstated exclusion | calibration |
| F4.2 | The 12-site residue needs a site metric before more cases; ten cheap cases are specified with their ordering guards in §4b | coverage |
| F5.1 | The wave's receipts are live-mutating during w1: `c2-controls.txt` 258→1143 B and `c1-selftest.txt` 0→132→2814 B inside my five-minute window. A seat that quotes a wave receipt must record its byte size and mtime, or it will report a superseded intermediate as the current state — I caught two of my own readings this way (both corrected above) | calibration |

## Method / scratch / tools

- Scratch: `/fast/scratch/hyaku/kengaku-r72/SurfaceScoutR72/`, one file (`probe_env.py`, 577 bytes).
  **The in-shell `trap 'rm -rf -- "$S"' EXIT` did not take effect** — the command carrying the trap
  exited 0 and the directory plus its file were still on disk at the next `ls` (23:12 mtime). Removed
  by an explicit follow-up `rm -rf -- /fast/scratch/hyaku/kengaku-r72/SurfaceScoutR72`
  (`RM_EXIT:0`), then verified absent: the parent listing has zero `SurfaceScout` entries and
  `ls /fast/scratch/hyaku/kengaku-r72/SurfaceScoutR72` → `No such file or directory` (rc 2). This is
  a defect of my own instrument and is recorded as F0 below; the seat did not end with its tree on
  disk. No clone, no work tree, no fixture, no port bind.
- Reads only under the lane; **nothing written under `corpus/`**. This report is the only lane write.
- No `git` mutation; `git -C <lane> rev-parse HEAD` was read-only.
- No tool installed or upgraded: `bwrap 0.13.1` and the `/fast/ComfyUI/.venv` interpreter were already
  present and sufficient.
