source: S245 (corpus/SOURCES.md) — Terminal-Bench 2.0 task `hf-model-inference`, task instruction at pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/instruction.md — anchor: `instruction.md:3-7,11-28` — sha256 `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`; and S246 (the grader) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/hf-model-inference/tests/test_outputs.py — anchor: `tests/test_outputs.py:8-107` — sha256 `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`
verified-at: 2026-11-03 (live re-fetch at the pin: instruction HTTP 200, 1264 bytes, sha256 `29151c5b…d1cc1`; grader HTTP 200, 4239 bytes, sha256 `61a686d6…87857`; both `cmp` byte-identical to the committed captures `corpus/evidence/round71/hf/instruction.md` and `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`; model tree `c5c25767…8944` re-derived from the five committed files)
recheck: pinned at `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (an immutable commit): `python3 plans/round71_c1_hf_probe.py --lane . --work <scratch> --port-lock <port-5000.lock> --receipt <path> --evidence-dir <path>` must reproduce the eight frozen vectors of `plans/round-71-claims.md`; `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` must print `61a686d6…87857`; `--check-receipt` prints `DEFECTS n=0` / `PREDICATE R71-C1 pass`.

writer: KnowledgeEntryDraft
admission: hold — the QUALITY Q13/Q14 second-seat re-read is not yet on record; see `corpus/lessons/round-71.md` `## Gate` (Admission status).

# TB2 `hf-model-inference` — a `network-service` grader replayed offline: four legs, eight cases, every leg witnessed green and red (R71-C1 pass)

The grader is Terminal-Bench 2.0 task `hf-model-inference`'s `tests/test_outputs.py` at pin
`2fd12b88aafdd04a52c298e3940bcb189f9766d6`: 107 lines, 4239 bytes, sha256
`61a686d6…f87857` (S246; `corpus/evidence/round52/graders/SHA256SUMS:76`). Four pytest
functions, run in file order; the whole score is those four returns. This entry records the
offline replay run in round 71 under the frozen eight-case table, the leg laws the replay
exposes, and the class-row move it carries.

## The four legs, in file order

| # | leg | lines | PASS condition (the grader's own asserts) |
|---|---|---|---|
| 1 | `test_model_downloaded` | :8-22 | `/app/model_cache/sentiment_model` exists (:12-13) **and** `AutoModelForSequenceClassification.from_pretrained` (:17) plus `AutoTokenizer.from_pretrained` (:18) both return non-`None` (:19-20); **any** exception in the `try` is converted to `assert False` (:21-22) |
| 2 | `test_flask_api_running` | :25-31 | `requests.get("http://0.0.0.0:5000")` (:29) returns a response — **no status or body check**; only `requests.exceptions.ConnectionError` is converted to a failure (:30-31) |
| 3 | `test_sentiment_endpoint` | :34-92 | for each of six hard-coded `(text, is_positive)` pairs (:36-44): status 200 (:50), the four fields `sentiment`/`confidence`/`positive`/`negative` present (:56-63), the confidence pair ordered consistently with the label (:65-73), both confidences `float` (:76-82), and the exact expected label (:84-92) |
| 4 | `test_api_error_handling` | :95-107 | a POST of `{"invalid_field": …}` (:98-101) answers 400 (:103) with an `error` key (:106-107) |

Leg 4 does not test a missing body, malformed JSON, or a wrong `Content-Type`: its one input
is a well-formed JSON object that lacks `text`.

## The six hard-coded texts — which the instruction never states

`test_sentiment_endpoint` iterates these literals (`test_outputs.py:36-44`):

| # | text (verbatim) | expected label |
|---|---|---|
| 1 | `I really enjoyed this movie, it was amazing!` (:37) | positive |
| 2 | `The service at this restaurant was terrible and the food was cold.` (:38-39) | negative |
| 3 | `This movie was not good at all; in fact, it was quite boring.` (:40) | negative |
| 4 | `I am not happy with the customer service I received.` (:41) | negative |
| 5 | `The journey was not bad; I actually had a good time.` (:42) | positive |
| 6 | `The view from the top of the mountain was horribly beautiful.` (:43) | positive |

Text 2 is one Python literal split over two source lines (implicit concatenation), so it
carries a single space after `terrible`; the grader compares the whole string, so the split
is invisible to a candidate.

**The instruction states none of them.** The instruction gives the endpoint, the request body
and the response/error schemas (`instruction.md:11-28`) but never the texts, their number, or
the label each must receive: `grep -c` on the committed instruction capture returns `0` for
`not bad`, for `horribly beautiful` and for `enjoyed this movie`. The label oracle therefore
exists only in the grader — texts 5 ("not bad") and 6 ("horribly beautiful") are traps whose
expected labels a candidate cannot read off the task.

The instruction-to-leg map, as observed:

| instruction | requirement | enforced by |
|---|---|---|
| `instruction.md:3` | download `distilbert-base-uncased-finetuned-sst-2-english` to `/app/model_cache/sentiment_model` | leg 1, path and loadability only — **the model's identity is never checked** |
| `:4` | a small Flask API at `/sentiment`, POST JSON `{"text": …}` | leg 2 (a listener only) and leg 3 (:47) — **Flask itself is never checked** |
| `:5` | return sentiment (positive/negative) with confidence scores as JSON | leg 3 (:50-82) |
| `:6` | port 5000, accessible from `0.0.0.0` | leg 2 (:29); leg 3 posts to `localhost:5000` (:47) |
| `:7` | run the service in the background | **no leg** |
| `:11-24` | the response schema, confidences typed `float` | leg 3 (:56-82) |
| `:25-28` | an `error` string with a 400 | leg 4 (:103-107) |

## `test_flask_api_running` accepts any HTTP answer

The leg is one unguarded `requests.get("http://0.0.0.0:5000")` (:29) with no
`raise_for_status`, no status assertion and no timeout. Read from the code path: any HTTP
status — 200, 404, 500 — and any body pass; the explicit red path is a `ConnectionError`
from a refused connection or one closed without a response, which lands on
`assert False, "Could not connect to the Flask API on 0.0.0.0:5000"` (:30-31). (Any other
transport exception is not caught, propagates, and also fails the leg.) Both measured reds are
that path: K5 closes `/` and K6 has no listener, and both captures record
`AssertionError: Could not connect to the Flask API on 0.0.0.0:5000`
(`corpus/evidence/round71/hf/sandbox/K5/manifest.json`,
`…/K6/manifest.json`). Nothing in the leg tests Flask: the
replay's candidate is a lane-written stdlib `ThreadingHTTPServer` bound to `("0.0.0.0", 5000)`
(`plans/round71_c1_hf_probe.py`, `SERVER_TMPL`) and the grader cannot tell the difference.

The absent timeout is the leg's latent blind spot: a listener that accepts and never answers
would hang the GET until the probe's 240 s case cap (`run_case(..., timeout=240)`) and be
scored `ERROR`, not `P`/`F`. No case in the frozen table stages that mode, so it is declared
here rather than priced.

## `test_model_downloaded` requires a loadable `transformers` model at a fixed path

The leg pins one path literal (`/app/model_cache/sentiment_model`, :12), imports
`transformers` **inside the test body** (:10 — so a missing library fails this leg rather than
erroring collection), asserts the directory exists (:13), then calls
`AutoModelForSequenceClassification.from_pretrained` (:17) and
`AutoTokenizer.from_pretrained` (:18) on it. The instruction's named model is not checked —
only that something loadable sits at that path: the replay stages a 1-layer,
`hidden_size: 8`, `vocab_size: 49` `BertForSequenceClassification` fixture
(`corpus/evidence/round71/hf/model/config.json`, five files, tree sha256 `c5c25767…8944`),
and leg 1 is `P` in six of the eight cases.

The leg's two red witnesses fail at two different points, so its red side covers both the
missing-directory and the unloadable-model modes:

- **K7 (`absent`)** fails at the existence assert: `AssertionError: Model directory not found`
  (:13).
- **K8 (`corrupt`)** passes existence and dies inside `from_pretrained`; the config file is
  invalid JSON on purpose, so the grader's `except Exception` fires and re-asserts at :22:
  `Failed to load model or tokenizer: It looks like the config file at
  '/app/model_cache/sentiment_model/config.json' is not a valid JSON file.`
  (`sandbox/K8/manifest.json`).

So the leg prices the load path — directory present, tokenizer resolvable, weights parseable
— not the model's identity, size, weights, or accuracy.

## The eight-case frozen table and the replay of record

The table is frozen in `plans/round-71-claims.md` R71-C1 and mirrored in
`plans/round71_c1_hf_probe.py` `CASES`/`VECTORS`; legs are in file order 1-4.

| case | model | service | frozen vector | observed | what it prices |
|---|---|---|---|---|---|
| K1 | good | good | `PPPP` | `PPPP` | all four legs green |
| K2 | good | wrong-label | `PPFP` | `PPFP` | leg 3 red: the "not bad" text answered negative |
| K3 | good | int-confidence | `PPFP` | `PPFP` | leg 3 red: confidence scores are ints, not floats |
| K4 | good | no-400 | `PPPF` | `PPPF` | leg 4 red: a body without `text` answered 200 |
| K5 | good | root-drops | `PFPP` | `PFPP` | leg 2 red: `/` closes the connection, `/sentiment` works |
| K6 | good | none | `PFFF` | `PFFF` | legs 2/3/4 red: no service listens |
| K7 | absent | good | `FPPP` | `FPPP` | leg 1 red: no model directory |
| K8 | corrupt | good | `FPPP` | `FPPP` | leg 1 red: `from_pretrained` raises on the staged bytes |

Per-leg witnesses, read off the `LEGS` lines: leg 1 `P` in K1-K6 / `F` in K7-K8; leg 2 `P` in
K1-K4, K7, K8 / `F` in K5, K6; leg 3 `P` in K1, K4, K5, K7, K8 / `F` in K2, K3, K6; leg 4 `P`
in K1-K3, K5, K7, K8 / `F` in K4, K6.

The receipt of record is `corpus/evidence/round71/hf/receipt.txt` (36 lines, sha256
`136ec423409cbc3031925148b0571ad6edb1cfdf209b42586addb7e2499e6067`), produced at
`REV d8a77d3f2b4c8747dbc3a5bcf458b23160a459e0` by `plans/round71_c1_hf_probe.py` (sha256
`d5ce2fa5871bb3d2b7b956f9f92d6e23ee21b7508b5da6dc113f6c3a2c1aa82e`; `PROBE_BLOB` the same
bytes from that commit):

```
VECTOR K1 expected=PPPP derived=PPPP agree=True
VECTOR K2 expected=PPFP derived=PPFP agree=True
VECTOR K3 expected=PPFP derived=PPFP agree=True
VECTOR K4 expected=PPPF derived=PPPF agree=True
VECTOR K5 expected=PFPP derived=PFPP agree=True
VECTOR K6 expected=PFFF derived=PFFF agree=True
VECTOR K7 expected=FPPP derived=FPPP agree=True
VECTOR K8 expected=FPPP derived=FPPP agree=True
LEG-COVERAGE legs=4 seen_p=4 seen_f=4
SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2
PREDICATE R71-C1 pass
```

The checker of record, `corpus/evidence/round71/hf/check.txt` (sha256
`6acbb7a13771b8ccbb3605f8593a4ea7c6ba3c764ce6ac9ffbac00ea3b205447`), prints:

```
DEFECTS n=0
PREDICATE R71-C1 pass
```

`--check-receipt` re-derives the five digest bindings from lane bytes (grader, instruction,
model tree, probe blob, probe worktree against `master`), requires the receipt's `REV` to be
an ancestor of `master`, matches the `LIBRARIES` line against the host environment at check
time, re-stages every case (when `--work` is given) and recomputes its `case_sha256`,
recomputes each vector from the `LEGS` lines, then recomputes coverage, summary and the
predicate — rc 0 only when there are no defects and the predicate is `pass`
(`plans/round71_c1_hf_probe.py:619-724`).

**Determinism, measured on two independent batteries.** `corpus/evidence/round71/hf/receipt-replicate.txt`
was produced 66 s after the receipt of record (mtimes 22:22:33 and 22:23:39, 2026-11-03) and
is byte-identical to it — `cmp` rc 0, same sha256 `136ec423…e6067`, same eight
`case_sha256` values. The staged-input digest is therefore run-independent: it is taken over
`/app` after staging and before the legs run (`stage_case`/`case_dir_sha`), and no staged
candidate writes into it. This is what round 69's nginx entry could not say — its
`case_sha256` covered a server-written access log and changed between runs.

**Do-nothing control.** `.ufo/waves/round-71/c1-control.txt` (43 lines, sha256
`c7cfa2012906988b0d0dbffa6f418607a0c9b3c0d8a950ef9fb881590e1bca0a`) stages the same eight
ids with no model and no service: every case derives `FFFF`,
`LEG-COVERAGE legs=4 seen_p=0 seen_f=4`, `SUMMARY … mismatches=8 setup=0 exc=16`, and
`PREDICATE R71-C1 fail` (:43). The pass above is therefore not obtainable by staging nothing.

**The `EXC` line prices exception class, not verdict.** Only K6 carries `EXC` entries
(`test_api_error_handling=E test_sentiment_endpoint=E`): with nothing listening, the two legs
that have no `try` block (:47, :98) raise an uncaught `ConnectionError`, while every other red
leg in the table fails an `AssertionError` and leg 2 converts its `ConnectionError` at :30.
pytest scores both as failure, so the vectors are unaffected — but a reader comparing `F`
against `F` now sees which failures were the grader's own assertions and which were
transport errors that would be red in any harness.

## The class row: `executed 3 of 8` → `executed 4 of 8`

The census already prices the member: `corpus/evidence/round62/class-survey.txt:11` —
`CLASS network-service count=8 members=filter-js-from-html,git-multibranch,headless-terminal,hf-model-inference,install-windows-3.11,kv-store-grpc,nginx-request-logging,pypi-server`
— and at base the class was uncovered
(`:21 EXECUTED-COVERAGE … classes-uncovered=network-service,process-environment,db-state,container-image`),
with `grep -c hf-model-inference corpus/evidence/round52/graders/executed17.lst` → `0` (rc 1).
The round-36 scout had refused the task as `Excluded: service + network`
(`.ufo/waves/round-36/build/R36ScoutNextTasks.md:41`); the service half is discharged by the
shim-on-loopback recipe above and the model-load half by the staged `transformers` directory.

With R71-C1 passing, the member is counted: the `network-service` row in `SKILL.md` moves from
`executed 3 of 8` to `executed 4 of 8`, `hf-model-inference` being the fourth executed member
after `kv-store-grpc` (round 64), `pypi-server` (round 68, under the corrected stderr clause)
and `nginx-request-logging` (round 70). Counting commands:
`grep -c 'executed 3 of 8' SKILL.md` → `0` and `grep -c 'executed 4 of 8' SKILL.md` → `1`.

## What this does not establish

- **Not the Flask app the task asks for.** The candidate is a lane-written stdlib
  `ThreadingHTTPServer` standing in for the Flask app (`plans/round71_c1_hf_probe.py`
  `SERVER_TMPL`); the probe supplies the end state and the grader's own `requests` calls
  decide. The replay shows the grader is satisfiable by that end state, not that the task has
  a solution, and not that an agent could produce one.
- **Not the task image's library versions.** `transformers` and `torch` come from this host's
  existing `/fast/ComfyUI/.venv`, bound read-only at `/venv` into the bubblewrap sandbox;
  the receipt records `LIBRARIES python=3.13.16 torch=2.14.1+cu130 transformers=5.21.0
  requests=2.34.2`, and the checker compares that line to the host environment **at check
  time** (a library change is a `library-drift` defect). The image's own versions are not
  reproduced, and the receipt is not portable to a host with different versions.
- **Not a model.** The staged model is a tiny fixture — the round's frozen limitation (iii)
  calls it random-weight — and the six texts and their labels are the grader's own constants.
  The replay prices the grader's logic, not sentiment accuracy, and says nothing about
  whether the instruction's named distilbert checkpoint would satisfy the six labels.
- **Not proof of a live run.** `--check-receipt` re-derives text and staged digests from
  committed bytes; it does not prove a process ran. The live witness is the per-case captures
  under `corpus/evidence/round71/hf/sandbox/K1…K8/` (`sandbox-stdout.txt`,
  `sandbox-stderr.txt`, `manifest.json`, `app-tree.txt`) written by the battery.
- **Not a hang case.** No case stages a listener that accepts and never answers; leg 2 has no
  timeout, so such a case would end at the 240 s probe cap as `ERROR` rather than as a leg
  verdict. Leg 2's observed red modes are refusal and close (K5, K6).
- **Not the model-identity requirement.** The instruction's named model is unenforced; the
  falsifier is direct: change the fixture's `hidden_size`/`num_hidden_layers` (keeping the
  directory, tokenizer and weight file loadable) and K1 stays `PPPP`.
- **Not the other `network-service` members.** `filter-js-from-html`, `git-multibranch`,
  `headless-terminal`, `install-windows-3.11` and the rest remain unexecuted;
  `pypi-server`'s R63-C1 MISS of record is unchanged.
- **Not the task's `tests/test.sh`.** Only `test_outputs.py` was read and executed here.
- **Not an independent reading of the task's validity.** S245/S246 are the maintainers' own
  task text and grader — read at a pin, not endorsed; no claim is made that the six labels are
  linguistically right or that the task measures what its instruction describes.

## Carried forward

This entry extends `corpus/knowledge/tb2-network-service-offline-grader.md` (the first
`network-service` replay, `pypi-server`, R63-C1 MISS), `corpus/knowledge/tb2-kv-store-grpc-offline.md`
(second executed member), `corpus/knowledge/tb2-nginx-request-logging-offline.md` (third:
R69-C1 MISS on leg coverage, then R70-C1 pass on the re-frozen table) and
`corpus/knowledge/tb2-grader-class-census.md` (the census that prices the member). It adds
the class's fourth executed member, and the corpus's first replayed `network-service` grader
whose model-load leg is satisfied by a staged `transformers` model directory — the leg class
the round-36 scout had refused as "service + network".
