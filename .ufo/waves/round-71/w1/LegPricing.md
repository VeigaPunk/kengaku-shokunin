# R71-C1 — leg pricing audit (what each red leg actually is)

Seat: `LegWitnessAudit`. Round 71, wave w1. Read-only audit of the R71-C1 replay witnesses.
No case table, predicate, vector, digest, kill rule or receipt byte was edited.

## Inputs

- Frozen table: `plans/round-71-claims.md` (lines 22–57).
- Receipt of record: `corpus/evidence/round71/hf/receipt.txt` (sha of probe/graders as pinned).
- Per-case live witness: `corpus/evidence/round71/hf/sandbox/K{1..8}/{manifest.json,sandbox-stdout.txt,sandbox-stderr.txt,app-tree.txt}` — all eight present.
- Replicate witness: `corpus/evidence/round71/hf/sandbox-replicate/K{1..8}/` + `receipt-replicate.txt`.
- Grader bytes: `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`,
  `sha256sum` = `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857` (matches the pin).
- Do-nothing control: `.ufo/waves/round-71/c1-control.txt`.

I ran no battery (no port was taken). To confirm the captures describe the frozen staging I
re-staged all eight cases with the probe's own `prepare_work`/`stage_case`/`case_dir_sha` into
`/fast/scratch/hyaku/kengaku-r71/LegWitnessAudit/stage`; all eight digests equal the receipt's
`CASE … case_sha256=` values (e.g. K1 `e96b30e1…`, K8 `82c99ab8…`).

## 1. Matrix — case × leg → P/F/E

Legs in grader file order: **L1** `test_model_downloaded`, **L2** `test_flask_api_running`,
**L3** `test_sentiment_endpoint`, **L4** `test_api_error_handling`.
`E` = a non-`AssertionError` escaped the leg call (harness `exc`), `F` = the leg's own
`AssertionError`. Every cell below was read from that case's `manifest.json` `legs`/`exc`.

| case | model | service | L1 | L2 | L3 | L4 | derived | expected |
|---|---|---|---|---|---|---|---|---|
| K1 | good | good | P | P | P | P | `PPPP` | `PPPP` |
| K2 | good | wrong-label | P | P | **F** | P | `PPFP` | `PPFP` |
| K3 | good | int-confidence | P | P | **F** | P | `PPFP` | `PPFP` |
| K4 | good | no-400 | P | P | P | **F** | `PPPF` | `PPPF` |
| K5 | good | root-drops | P | **F** | P | P | `PFPP` | `PFPP` |
| K6 | good | none | P | **F** | **E** | **E** | `PFFF` | `PFFF` |
| K7 | absent | good | **F** | P | P | P | `FPPP` | `FPPP` |
| K8 | corrupt | good | **F** | P | P | P | `FPPP` | `FPPP` |

Six of the eight cases are *single-red* (K2, K3, K4, K5, K7, K8) — the isolation that round-70
limitation (iii) said was missing. K6 is the only whole-state multi-red case.

## 2. Every F — verbatim `detail`, grader site, mechanism

Quotes are the exact `detail` string from `manifest.json` (identical in `sandbox-stdout.txt`
and in every replicate manifest). Line numbers are in the pinned grader.

| case | leg | grader site | `detail` (verbatim) |
|---|---|---|---|
| K2 | L3 | `:86-88` `assert result["sentiment"] == "positive"` | `AssertionError: Text The journey was not bad; I actually had a good time. should be classified as positive` |
| K3 | L3 | `:77-79` `assert isinstance(result["confidence"]["positive"], float)` | `AssertionError: Confidence scores should be floats` |
| K4 | L4 | `:103-105` `assert response.status_code == 400` | `AssertionError: API should return 400 for invalid request format` |
| K5 | L2 | `:31` `assert False, "Could not connect to the Flask API on 0.0.0.0:5000"` | `AssertionError: Could not connect to the Flask API on 0.0.0.0:5000` |
| K6 | L2 | `:31` (same statement) | `AssertionError: Could not connect to the Flask API on 0.0.0.0:5000` |
| K6 | L3 | none — `:47` raised | `ConnectionError: HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded with url: /sentiment (Caused by NewConnectionError("HTTPConnection(host='localhost', port=5000): Failed to establish a new connection: [Errno 111] Con` |
| K6 | L4 | none — `:98` raised | `ConnectionError: HTTPConnectionPool(host='localhost', port=5000): … [Errno 111] Con` (same 237-byte string) |
| K7 | L1 | `:13` `assert os.path.exists(model_path)` | `AssertionError: Model directory not found` |
| K8 | L1 | `:22` `assert False, f"Failed to load model or tokenizer: {e}"` | `AssertionError: Failed to load model or tokenizer: It looks like the config file at '/app/model_cache/sentiment_model/config.json' is not a valid JSON file.` |

Mechanism notes, each verified against the staged bytes:

- **K2** — the staged `server.py` differs from K1's in exactly two lines: `MODE = 'wrong-label'`
  and one `LABELS` entry, `'The journey was not bad; I actually had a good time.': 'negative'`
  (K1: `'positive'`). The leg fails on the 5th of the six texts, at the label assertion, after
  the confidence-ordering branches (`:71`) and both `float` asserts passed. The returned body was
  `{"sentiment": "negative", "confidence": {"positive": 0.04, "negative": 0.96}}`.
- **K3** — same server except `MODE = 'int-confidence'`; `confidence()` returns JSON ints
  `{"positive": 1, "negative": 0}`. `:67-69` passes (`1 > 0`), `:76` passes, `:77` fails on
  `isinstance(1, float)`. Fails on the **first** text.
- **K4** — `MODE = 'no-400'`; the `not isinstance(text, str)` branch returns `200` with a
  negative body instead of `400`. The leg fails at `:103`; `:107` is never reached.
- **K5** — `MODE = 'root-drops'`; `do_GET` closes the connection, `do_POST` is untouched.
  The harness's own readiness probe observed it: `"ready": false` with `"server": true,
  "server_pid": 3` (K1–K4/K7/K8 are `"ready": true`; K6 is `null`). The grader's
  `except requests.exceptions.ConnectionError` converted the drop into the assertion at `:31`,
  so this is a genuine assertion red, not an `E`.
- **K6** — no `server.py` in the staged app (`app-tree.txt` lists only the five model files;
  `"server": false`, `"server_pid": null`). L2's `requests.get` raises `ConnectionError`, which
  the grader catches → assertion at `:31`. L3/L4 raise `ConnectionError` out of `:47`/`:98`
  and are recorded as `E`.
- **K7** — `app-tree.txt` is `server.py` only; `model_cache/` exists but `sentiment_model/`
  does not, so `:13` fires before any import of the staged bytes. K7's stderr is empty (no
  weight load).
- **K8** — `config.json` is the literal bytes `{"model_type": "bert", ` (invalid JSON, written
  by `stage_case`). `from_pretrained` raises, `:21-22` catches and re-asserts. K8's stderr is
  also empty (no weight load).

## 3. Every P — the return that made it pass

| leg | P cases | return that made it pass | evidence |
|---|---|---|---|
| L1 | K1, K2, K3, K4, K5, K6 | `AutoModelForSequenceClassification.from_pretrained` returned a model and `AutoTokenizer.from_pretrained` returned a tokenizer; both non-`None`; function returns `None` after `:20`. | `sandbox-stderr.txt` for K1–K6 carries the transformers progress line `Loading weights: 100%\|…\| 25/25` (bar elided; all six end `25/25 [00:00<00:00,`); K7/K8 stderr is empty. `app-tree.txt` shows the five model files. |
| L2 | K1, K2, K3, K4, K7, K8 | `requests.get("http://0.0.0.0:5000")` returned a `Response` (status never inspected); function returns `None` at `:31`'s end. | `"ready": true` in the same run — the harness's independent `urlopen("http://127.0.0.1:5000/")` returned the staged `200 {"ok": true}`. |
| L3 | K1, K4, K5, K7, K8 | six `POST /sentiment` calls each returned `200` with `{"sentiment": <label>, "confidence": {"positive": 0.93, "negative": 0.07}}` (inverted for negatives); every label equals the grader's expectation and both scores are JSON floats, so `:50`–`:92` all pass. | `detail` has no L3 key in these cases; the probe's `LABELS` dict equals the grader's six `test_texts` pairs (AST-parsed from `:36-44`, all six agree, key set identical). |
| L4 | K1, K2, K3, K5, K7, K8 | `POST /sentiment` with `{"invalid_field": …}` → `text = body.get("text")` is `None` → staged server returns `400 {"error": "missing text"}`; `:103` and `:107` pass; function returns `None`. | staged `server.py` `do_POST` `not isinstance(text, str)` branch; `detail` has no L4 key. |

Note the P side is *positive-only* witness for the staged server's good branches: the leg code
was executed end-to-end (six texts, including both confidence-ordering branches in K1: text 2
negative → `:71`, text 1 positive → `:67`), and no assertion fired.

## 4. Answers

### (a) Is every red the intended assertion?

Yes for all six named checks, with one qualification:

| claim | red | verdict |
|---|---|---|
| K2 label | `:86` "should be classified as positive" on the "not bad" text | intended assertion, exact f-string, 5th text |
| K3 float type | `:77` "Confidence scores should be floats" | intended assertion (int JSON fails `isinstance(…, float)`) |
| K4 status 400 | `:103` "API should return 400 for invalid request format" | intended assertion |
| K5 connection | `:31` "Could not connect to the Flask API on 0.0.0.0:5000" | intended assertion, produced by the grader's own `except ConnectionError` |
| K7 directory | `:13` "Model directory not found" | intended assertion |
| K8 load exception | `:22` "Failed to load model or tokenizer: … not a valid JSON file." | intended assertion **wrapper** — the raw `transformers` exception was converted by `:21-22`, which is why K8 shows no `E` |

Qualification: **K6's L3 and L4 reds are not assertions at all.** They are uncaught
`ConnectionError`s (`exc` = `E`); those legs' assert code never executed. The frozen table calls
them red and the harness scores any exception as `F`, and no leg depends on K6 for its only red
(L2 has K5, L3 has K2/K3, L4 has K4), so the vector `PFFF` is honest — but the two `E` cells
witness "exception escaped", not "the leg's rule failed".

Also: **K8 prices a config-parse failure, not corrupted weights.** The staged corruption is
malformed `config.json`; a reader who takes "corrupt" to mean bad tensors would be wrong.

### (b) Do two cases share one red mechanism, leaving a distinct failure mode unpriced?

- **L2 — yes, one mechanism, twice.** K5 and K6 produce byte-identical detail
  (`…Could not connect to the Flask API on 0.0.0.0:5000`, 66 bytes). L2 has exactly **one**
  assertion statement (`:31`) and its only guarded exception is
  `requests.exceptions.ConnectionError` (`:28-31`), so the leg cannot distinguish "no listener"
  from "listener drops the connection" in its own message; only the staging and the harness's
  `ready` flag distinguish them. L2's red is therefore "no HTTP answer", **not** "API not
  running": any response, any status, passes the leg (the claim's limitation (iv), confirmed by
  reading `:29` — the return value is never inspected). Nothing inside L2's single assert is
  left unpriced by the duplication; the leg has no other F mode that this table could show.
- **L3 — no collapse, but wide un-priced surface.** K3 hits `:77` (type) and K2 hits `:86`
  (label): two distinct statements, two distinct mechanisms. However L3 has 12 assert
  statements and only 2 of them are ever witnessed failing. Unpriced negatives: `:50` status
  200, `:56/:57/:58/:61` missing `sentiment`/`confidence`/`positive`/`negative`,
  `:67-69`/`:71-73` sentiment-vs-confidence ordering, `:76` non-str sentiment, `:80-82` a
  *negative* score delivered as int, `:90-92` the negative-label branch. A server answering
  `200 {"sentiment": "positive"}` (no confidence), or `500` on a valid text, or `"1.0"` as a
  string, would be missed by this table.
- **L4 — one of two statements priced.** `:107` (`"error" in error_data`) has no negative
  witness; a server returning `400` with a body lacking `error` would pass K4's staging and be
  caught by a case that does not exist. K4 also never reaches `:107` (it fails at `:103`).
- **L1 — both reachable statements priced** (`:13` by K7, `:22` by K8); `:19`/`:20`
  (`model/tokenizer is not None`) have no negative witness and are practically unreachable.
- **K6's E cells price nothing about L3/L4's rules** — they share the connection-refused
  mechanism with K5's L2 red, so K6 adds a whole-state shape and an `E` witness, not a new
  failure mode of L3 or L4.

Site-level tally: 19 assert statements in the grader; 6 have a negative witness
(`:13`, `:22`, `:31`, `:77`, `:86`, `:103`); 13 do not.

### (c) Does the `EXC` line separate connection errors (K6) from assertion failures?

Yes, and the evidence is exact:

- The receipt has exactly one `EXC` line in the whole battery:
  `EXC K6 test_api_error_handling=E test_sentiment_endpoint=E`, matching `SUMMARY … exc=2`.
  All seven other cases have `"exc": {}`.
- The harness classifies by `except AssertionError` **before** `except Exception`
  (`HARNESS_SRC`), so an `AssertionError` can never be recorded as `E`, and a
  `requests.exceptions.ConnectionError` (not an `AssertionError`) can never be recorded as a
  plain `F` — it becomes `E` with the exception type in `detail`.
- K6's two `E` details start with `ConnectionError:` and carry
  `NewConnectionError(…: [Errno 111] …)`; the assertion reds all start with `AssertionError:`.
- The do-nothing control (`.ufo/waves/round-71/c1-control.txt`) is the cross-check in the
  other direction: with no model and no service in all eight cases, `EXC` appears for L3 and
  L4 in every case (`SUMMARY … exc=16`), L2 stays an `F` assertion, and the counter prints
  `PREDICATE R71-C1 fail`.

Caveat on reading the line: `EXC` means "a non-assertion exception escaped the leg", not
"a connection error occurred". **K5's L2 failure is also a connection failure but has no `EXC`**
because the grader caught it and asserted at `:31`; the K5 manifest's `"ready": false` is the
tell. So the line separates K6's escaped exceptions from assertion failures correctly, but it
must not be used as a connection-error tally. A second-order nit: the harness caps the detail at
220 chars, so `[Errno 111] Con` is where `Connection refused` is cut — the exception type and
the pool/host/port survive, the last words do not.

## 5. Verdict per leg

- **L1 `test_model_downloaded` — priced.** P witnessed six times with a real 25-tensor load;
  F witnessed by two distinct statements (missing directory `:13`; load raise `:22`, here a
  config-JSON parse failure, not bad weights). Only the `is not None` statements are unpriced,
  and they are practically unreachable.
- **L2 `test_flask_api_running` — priced, single mechanism.** P witnessed by a returned
  `Response` (`ready: true`); F witnessed twice with identical text at the leg's only assertion
  (`:31`). Its red is "no HTTP answer"; a listener that answers anything passes, by design.
- **L3 `test_sentiment_endpoint` — priced at 2 of 12 sites.** P witnessed with all six labels
  and both ordering branches; F witnessed on the float-type statement (`:77`, K3) and the
  label statement (`:86`, K2). Status, missing-field, ordering, string-type, negative-label,
  and negative-float asserts have no red witness.
- **L4 `test_api_error_handling` — priced at 1 of 2 sites.** P witnessed by `400` + `error`;
  F witnessed at the status statement (`:103`, K4). The error-field statement (`:107`) is never
  seen failing.

Round-level: `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` is real — each leg has both witnesses from
a genuine assertion at least once — and round-70 limitation (iii) is discharged for all four
legs by the six single-red cases (K2/K3 → L3, K4 → L4, K5 → L2, K7/K8 → L1). K6 remains the
only whole-state multi-red case, and it is redundant for isolation.

## 6. Audit limitations

- I did not re-run a battery; my witnesses are the committed captures plus the replicate
  battery (`sandbox-replicate/`, `receipt-replicate.txt`), whose eight manifests carry identical
  `case_sha256`, `detail` and `exc` to the primary — the reds are deterministic across two
  runs, but both runs share the same host libraries (`transformers 5.21.0`, `torch 2.14.1`,
  receipt `LIBRARIES` line), so K8's exact exception text is library-version dependent.
- The staged digests I re-derived prove the captures' staged inputs; they do not prove the
  grader's behaviour (the claim's own limitation (v)).
- P-side "returns" are derived from the staged server's source plus the absence of any
  `detail` entry and the `ready` flag; the server's stdout is `DEVNULL`, so no wire capture of
  the six response bodies exists in the record.
