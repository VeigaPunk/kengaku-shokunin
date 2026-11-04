# SourceOpen71 — live open of S245/S246 at pin `2fd12b88` (R71-C1)

Seat: `SourceOpen71`, scout, leaf (no subagent). Lane `kengaku-shokunin`, branch `master`, tip
`d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` at seat time (`git -C … rev-parse master`; frozen base
`1cb49cac` is an ancestor). Scratch `S=/fast/scratch/hyaku/kengaku-r71/SourceOpen71`.

Read-only seat. The only files I wrote are the ones my item names — `W/SourceOpen71.md`,
`W/SourceOpen71-rows.txt`, and receipts under `W/SourceOpen71/`. No predicate, case table, vector,
digest, kill rule, target, `MANIFEST.json`, `scripts/`, or sibling lane was touched. No battery ran,
so the port-5000 lock was not taken; the one socket experiment in §5-F1 binds an ephemeral port on
`127.0.0.1` only. Tooling: nothing installed — host `curl`, `python3`, read-only `git`, `awk`,
`sha256sum` sufficed.

## What I ran

| # | command | rc |
|---|---|---|
| 1 | `curl -sS -o <file> -w '%{http_code}'` on the four pin URLs under `…/2fd12b88…/hf-model-inference/` (`instruction.md`, `tests/test_outputs.py`, `tests/test.sh`, `task.toml`) | 0 (200, 200, 200, 200) |
| 2 | `curl -sSI` on the same four URLs (status/`content-length`/`etag`) | 0 |
| 3 | `wc -c`, `wc -l`, `sha256sum` on each fetched file | 0 |
| 4 | `cmp` fetched `tests/test_outputs.py` vs `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` | 0 — byte-identical |
| 5 | `cmp` fetched `instruction.md` vs `corpus/evidence/round71/hf/instruction.md` | 0 — byte-identical |
| 6 | `cmp` fetched `tests/test_outputs.py` vs `corpus/evidence/round71/hf/instruction.md` (the seat text's literal second comparison) | 1 — `differ: char 1, line 1` (different artefacts; see §3) |
| 7 | `git cat-file blob master:<capture> \| sha256sum` for both committed captures | 0 |
| 8 | `grep -n 'hf-model-inference' corpus/evidence/round52/graders/SHA256SUMS` | 0 — lines 76 (`test_outputs.py`) and 77 (`test.sh`) |
| 9 | `git clone --shared` of the lane into `S/lanecheck`; the two rows inserted after `S244` in the clone's working tree; `awk -F'\|' … NF!=13`; `python3 plans/anchor_digest_check.py --lane <clone> --verbose` | clone 0; arity `malformed=0`; checker exit **1** (44 pre-existing defects, unchanged) with both rows `BIND`+`RESOLVED` |
| 10 | `python3 plans/anchor_digest_check.py --lane .` on the lane, before and after the L1 appended the rows | 1 both times — `rows=236 tokens=127 defects=44` → `rows=238 tokens=129 defects=44` |
| 11 | absence greps on the fetched bytes (`psutil` in grader; `background`, `system-wide`, `pip` in grader; `not bad`, `horribly`, `boring`, `terrible`, `amazing` in instruction) | 1 — no match in every case |
| 12 | ephemeral-port test: `http.server` bound to `127.0.0.1:0`, then `GET http://0.0.0.0:<port>` | 0 — **HTTP 200** (see §5-F1) |
| 13 | `diff` the two lane-appended rows against `W/SourceOpen71-rows.txt:3-4` | 0 — byte-identical |

## 1. Fetch at the pin — four HTTP 200s, no 404

| path at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` | HTTP | bytes | lines | sha256 | etag |
|---|---|---|---|---|---|
| `hf-model-inference/instruction.md` | 200 | 1264 | 28 | `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1` | `"5577f32043e35652b8df798871f96a7ef2b9493342811c2abb725866f8714221"` |
| `hf-model-inference/tests/test_outputs.py` | 200 | 4239 | 107 | `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857` | `"e1c0da2cdf501f97ed7ffc326fd6a5d354cb1458fd3b3096abd62ba644ae7d26"` |
| `hf-model-inference/tests/test.sh` | 200 | 295 | 13 | `6528c4c44d46004738c57dc59709bc80fb4226d37aaf0e8d778cc08017642e8f` | `"5797848d6e1aa6baf370122e7664e35209b9c3ea02cb120fb0d559a198de07ab"` |
| `hf-model-inference/task.toml` | 200 | 943 | 41 | `a75f95a090ad0352069c6d7dc2f4de0a7b80cd12cd6b9ec1c57e59ad3956b89d` | `"ec0d8c2e5a4537aadeb5fe8d68ad77043247ada647522d08e0c20dae3f7aa5eb"` |

**`task.toml` exists at the pin** (the seat's explicit question): HTTP 200, 943 bytes, 41 lines. Its
load-bearing fields for this round are `[task] name = "terminal-bench/hf-model-inference"` (`:5`),
`[environment] docker_image = "alexgshaw/hf-model-inference:20251031"` (`:29`) and
`allow_internet = true` (`:34`) — the task's own end state is a networked image, which is why the
offline replay stages a model fixture instead of downloading one (claim limitation ii/iii).

Raw headers for all four are in `W/SourceOpen71/fetch-headers.txt`; byte copies in `W/SourceOpen71/`
(`instruction.md`, `test_outputs.py`, `test.sh`, `task.toml`).

## 2. Located quotes (each ≤25 words)

- `instruction.md:3` (16 words) — the model-download clause:
  `Download the "distilbert-base-uncased-finetuned-sst-2-english" sentiment analysis model from Hugging Face and save to the local directory '/app/model_cache/sentiment_model'.`
- `instruction.md:6` (14 words) — the binding clause:
  `The service should run on port 5000 and be accessible from any host (0.0.0.0).`
- `instruction.md:27` (15 words) — the error clause:
  `"error": string  // Error message describing what went wrong. Should return a 400 status code.`
- `tests/test_outputs.py:13` (6 words) — leg 1's existence assert:
  `assert os.path.exists(model_path), "Model directory not found"`
- `tests/test_outputs.py:29` (1 word) — leg 2's only request:
  `requests.get("http://0.0.0.0:5000")`
- `tests/test_outputs.py:31` (9 words) — leg 2's only failure text:
  `"Could not connect to the Flask API on 0.0.0.0:5000"`
- `tests/test_outputs.py:77` (3 words) — the float-type assert:
  `assert isinstance(result["confidence"]["positive"], float)`
- `tests/test_outputs.py:103` (8 words) — leg 4's status assert:
  `"API should return 400 for invalid request format"`
- `tests/test.sh:6` (5 words) — the verifier entrypoint:
  `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`

The four legs, in file order (`grep -n '^def test_'`): `:8 test_model_downloaded`,
`:25 test_flask_api_running`, `:34 test_sentiment_endpoint`, `:95 test_api_error_handling` — exactly
the leg order the frozen case table names.

Leg 2 verbatim (`:25-31`), because the round's limitation (iv) and F1 both rest on it:

```python
def test_flask_api_running():
    """Test that the Flask API is running on port 5000 and accessible from any host"""
    # Check if the API is accessible from 0.0.0.0 on port 5000
    try:
        requests.get("http://0.0.0.0:5000")
    except requests.exceptions.ConnectionError:
        assert False, "Could not connect to the Flask API on 0.0.0.0:5000"
```

## 3. `cmp` and drift vs committed captures

- **Grader — no drift.** Fetched `tests/test_outputs.py` is byte-identical to
  `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` (`cmp` rc 0), whose
  digest is the same string listed at `corpus/evidence/round52/graders/SHA256SUMS:76`. The probe pins
  it at `plans/round71_c1_hf_probe.py:59` (`GRADER_SHA256 = "61a686d6…"`) and rebinds it to that same
  committed path at `:58` (`GRADER_REL`).
- **Instruction — no drift.** Fetched `instruction.md` is byte-identical to
  `corpus/evidence/round71/hf/instruction.md` (committed blob `e1c76bad…`, `sha256sum` of the blob
  `29151c5b…`), which is `plans/round71_c1_hf_probe.py:61` (`INSTRUCTION_SHA256`).
- **The seat text's literal second `cmp`** — fetched `tests/test_outputs.py` against
  `corpus/evidence/round71/hf/instruction.md` — returns rc 1 (`differ: char 1, line 1`). It must: a
  grader and an instruction are different artefacts. The informative pairing is
  instruction↔instruction, which is identical. Recorded as a phrasing issue in the seat prompt, not
  as drift; no rule changed.
- **Capture gaps (not row-blocking, but named).** `tests/test.sh` is committed only under
  round52 (`SHA256SUMS:77`, 295 bytes, digest matches the fetch) and not under `round71/hf`.
  `task.toml` is committed in no `corpus/evidence` directory:
  `git ls-tree -r master --name-only corpus/evidence | grep task.toml` lists 15 files, none for
  `hf-model-inference`. I therefore cite **no** `task.toml` digest in a registry row — Q26 would call
  it `digest-unknown` because no committed byte backs it.

## 4. Rows S245 and S246 — written, validated, and already landed byte-for-byte

`W/SourceOpen71-rows.txt` (sha256 `95cc1c4e6d78310feda6073eed56790f0c885d9f660c2f7b8af11b26224ffbd8`)
carries the contract-v1 header line and two rows:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

- **S245** — `instruction.md` at the pin, kind `docs`, tier `A`, status `mined`, opened `2026-11-03`,
  recheck `2027-05-02`, used-by `corpus/knowledge/tb2-hf-model-inference-offline.md`. Anchor carries
  the fetch facts, the 64-hex digest and the `:3` quote.
- **S246** — `tests/test_outputs.py` at the pin, kind `code`, tier `A`, same status/open/recheck/
  used-by. Anchor carries the fetch facts, the 64-hex digest, the `:13` quote, and the `:29`
  observation that leg 2 has no status assert.

The L1 has already appended both rows at `corpus/SOURCES.md:260-261` (working tree,
`git diff --numstat corpus/SOURCES.md` → `2	0`), and `diff` of those two lines against
`W/SourceOpen71-rows.txt:3-4` is empty — **byte-identical**, so the file is the appendable record.

Gates, all re-derived (receipts `W/SourceOpen71/anchor-gate-rows.txt`, `W/SourceOpen71/census-clone.txt`):

| check | result |
|---|---|
| arity — `awk -F'\|' … NF!=13` (11 columns ⇒ NF 13) | `malformed=0` on the file and on the clone with the rows inserted |
| cells per row | 11; no literal `\|` inside a cell |
| `sha256` tokens | exactly one per row, both in the **anchor** cell (Q26 shape) |
| `anchor_digest_check.py --lane <clone> --verbose` | `BIND S245 capture=corpus/evidence/round71/hf/instruction.md by=row-path` → `RESOLVED`; `BIND S246 capture=corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py by=row-path` → `RESOLVED` |
| defects added | 0 — lane `defects=44` before (`rows=236 tokens=127`) and after (`rows=238 tokens=129`); the 44 are pre-existing across S173–S243 and untouched |
| census — duplicate ids, enum/tier | none |
| census — `mined` used-by paths exist | **fails on my two rows**: `missing: corpus/knowledge/tb2-hf-model-inference-offline.md` ×2 |

**Landing-order constraint (routed, not fixed by me).** Seat `KnowledgeEntryDraft` in this wave
targets exactly `corpus/knowledge/tb2-hf-model-inference-offline.md`; the file does not exist at seat
time. The rows are only census-clean once that entry (plus its `corpus/README.md` index row and
coverage-map row, Q7) lands in the same commit as the rows.

## 5. Findings (reported; no rule, table, vector or digest edited)

- **F1 — leg 2 is binding-blind, not merely status-blind.** Measured on this host: an HTTP server
  bound **only** to `127.0.0.1:<ephemeral>` answered `GET http://0.0.0.0:<port>` with **HTTP 200**
  (command 12). So `test_flask_api_running` cannot distinguish a `0.0.0.0` binding from a
  loopback-only one on Linux; it only distinguishes "something answered" from "connection refused".
  The claim's limitation (iv) says the leg "accepts any HTTP answer from `0.0.0.0:5000` (no status
  check)" — true, and this is a second, independent tolerance: the host in the URL is not evidence of
  the bind address. K5's `root-drops` is exercised because the connection is *closed*, not because a
  bind address is read. Scope of the measurement: `http.server` + standard kernel routing as observed
  on `linux 7.2.11-arch1-1`; a stricter check would inspect `/proc/net/tcp` or connect from a
  non-loopback address. Not a defect in the frozen table.
- **F2 — the six texts and labels are undisclosed in the task statement.** `grep -nE 'not bad|horribly|boring|terrible|amazing' instruction.md` → no match; the constants live only at
  `tests/test_outputs.py:36-44`. Supports limitation (iii): the replay prices the grader's logic, not a
  model's accuracy, and no solver could derive those labels from the instruction.
- **F3 — the verifier entrypoint installs a package the grader never imports.** `tests/test.sh:4`
  pip-installs `psutil==7.0.0`; `grep -n psutil tests/test_outputs.py` → no match. A dead dependency
  in an offline replay (one extra wheel to stage) and a mismatch between the two captured files.
- **F4 — instruction clauses the grader never checks**: `:7` "Run the service in the background."
  and `:9` system-wide install (`grep -nE 'background|system-wide|pip|install' test_outputs.py` → no
  match). Also `task.toml:34 allow_internet = true` and `:29` image pin
  `alexgshaw/hf-model-inference:20251031` — the task permits network, which the offline replay
  deliberately does not reproduce (limitation ii).
- **F5 — row-mechanics, for whoever adds captures later.** The anchor gate's upstream-URL route cannot
  bind these rows: no committed evidence directory carries a `task.toml` with
  `name = "terminal-bench/hf-model-inference"`, and for a `tests/…` subpath the route keys on the
  literal component `tests` (the same `anchor-unbound` detail S241/S243 print). Both rows therefore
  name their committed capture path, the route-3 shape S237–S239 use. If a later round commits
  `corpus/evidence/round71/hf/task.toml` with that `name`, the URL route would bind that directory's
  basename instead — worth knowing before adding captures.

## 6. Verdict

**VERDICT SourceOpen71:** S245 (instruction) and S246 (grader) are opened live at pin `2fd12b88` —
four HTTP 200s, byte counts, sha256 and located ≤25-word quotes recorded — and both fetched artefacts
are byte-identical to their committed captures (zero drift; grader also equals `SHA256SUMS:76`);
both rows pass the registry's arity and anchor-digest gates with **zero new defects** and are already
appended byte-for-byte at `corpus/SOURCES.md:260-261`. Residual, not mine to close: the used-by path
`corpus/knowledge/tb2-hf-model-inference-offline.md` does not exist yet, so the census's
missing-used-by leg stays red on exactly these two rows until the knowledge entry lands.
