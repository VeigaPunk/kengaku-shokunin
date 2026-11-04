# CaseTableAudit71 — R71-C1 eight-case table audit (kengaku round 71, wave w1)

Seat: leaf auditor. Read-only session: no battery run (no port lock taken), no scratch, no
tool installs (none needed), no file writes except this report. The frozen table was NOT
edited; the add-ONE proposal below is for the L1 to rule on.

## What I ran (all rc 0 unless noted)

- `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`
  → `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857` — matches the frozen
  GRADER_SHA256 (claims §R71-C1; probe `plans/round71_c1_hf_probe.py:16`).
- `git cat-file -t 2fd12b88aafdd04a52c298e3940bcb189f9766d6` → fatal "could not get object info"
  (rc 128, expected): the pin is the upstream `harbor-framework/terminal-bench-2` commit, not a
  lane object — same convention as every prior TB2 row (S079/S100/S105; README.md:270 records the
  pin for the round-52 capture population). Identity is carried locally by the byte digest above,
  which I verified.
- `git log -1 -- <grader>` → `19bc16c4` "round-52: … land pinned TB2 captures" (capture landed
  committed; never re-fetched — consistent with the claims' offline posture).
- `rev-parse master` → `d8a77d3f`; `git merge-base --is-ancestor 1cb49cac… master` → YES: the
  freeze tip is an ancestor of the current tip; history intact, tip only moved forward.
- `sha256sum plans/round71_c1_hf_probe.py` == `git show master:plans/round71_c1_hf_probe.py | sha256sum`
  → both `d5ce2fa5871b…`; 872 lines; `git status --porcelain` on the probe → clean. No mid-session
  drift of the frozen instrument.
- Full reads with line anchors: grader `tests/test_outputs.py` (107 lines) and probe sections:
  consts/LEGS/LABELS/CASES/VECTORS (:1-118), HARNESS_SRC (:119-197), SERVER_TMPL (:199-253),
  staging/server_source/stage_case (:374-411), run_case (:437-491), battery_lines/run_battery/
  run_control (:497-586), parse_receipt/check_receipt (:600-720).

Grader line anchors (all `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`):

- L1 `test_model_downloaded` :8-22 — decisive: :13 `assert os.path.exists(model_path), "Model
  directory not found"`; :22 `assert False, f"Failed to load model or tokenizer: {e}"` (except arm).
  :19-20 (`model is not None` / `tokenizer is not None`) are practically unreachable —
  `from_pretrained` raises rather than returning None.
- L2 `test_flask_api_running` :25-31 — the only guard is
  `except requests.exceptions.ConnectionError: assert False, "Could not connect…"` (:30-31);
  the `requests.get` response at :29 is discarded: **no status check**.
- L3 `test_sentiment_endpoint` :34-92 — six texts :36-44; per text: status :50, schema fields
  :56-57, confidence keys :58-62, ordering :66-73, types :76-82, expected label :85-92.
- L4 `test_api_error_handling` :95-107 — posts `{"invalid_field": …}` :98-101; status :103-105;
  `assert "error" in error_data` :106-107.

Probe anchors: `server_source` flips `LABELS[WRONG_LABEL_TEXT]="negative"` for wrong-label
(:374-378); no-400 branch returns 200 only under `not isinstance(text, str) or not text`
(:225-230); root-drops closes the connection in do_GET only (:219-224); harness runs with argv
`"none"` for server_mode "none" (:452) and records non-assert exceptions as `F` with `exc[name]="E"`
(:159-166); `battery_lines` LEG-COVERAGE counts legs with ≥1 P / ≥1 F (:546-551); `check_receipt`
re-stages all eight cases from the committed instrument and enforces per-case `case_sha256`
equality plus all-8-distinct digests (:652-665) and recomputes derived vectors from the LEGS lines
(:680-694).

## What I found — per-case pricing (red line + aliasing)

| case | vector | exact line the red leg trips | does a different defect also produce that red? |
|---|---|---|---|
| K1 good/good | PPPP | none (green anchor) | By design: any contract-satisfying server passes; L2-L4 never touch the model, so K1's green prices the contract, not inference (declared limitation (i)/(iii)). Also the environment binder: K1's L1=P on the same LIBRARIES line disambiguates K8's library-breakage alias below. |
| K2 good/wrong-label | PPFP | L3 trips :86 `assert result["sentiment"] == "positive"` ("Text The journey was not bad… should be classified as positive") | Yes. Any positive-expected text flip trips :86 identically — the vector cannot name the text. Ordering-red (:67-73) and type-red (:77/80) defects alias into the same PPFP slot. The staged response is internally consistent (sentiment "negative", 0.96>0.04), so :50,:56-62,:66-73,:76-82 all pass first — K2 isolates the expected-label clause. |
| K3 good/int-confidence | PPFP | L3 trips :77 `assert isinstance(result["confidence"]["positive"], float)` on text 1 (ordering :67-69 passes 1>0; :76 passes) | Yes. String confidences pass string-compare ordering (:68 `"0.93">"0.04"` True) then trip :77 — same line, same vector. NaN floats pass :77/80 but trip ordering :67-69 → also PPFP. Vector-identical to K2; only `CASE case_sha256` (distinct staged bytes) and the evidence manifest's detail separate them. |
| K4 good/no-400 | PPPF | L4 trips :103 `assert response.status_code == 400` (server answers 200; probe :228-230) | Yes, and only partially staged: a 400 whose body lacks `"error"` trips :107 instead — same vector PPPF, line-distinct, NOT staged. Also any 5xx-on-invalid server aliases. K4's red is status-only; :107 never executes. |
| K5 good/root-drops | PFPP | L2 trips :31 (connection closed without response) | Yes, narrowly: RST or a garbage status line (urllib3 ProtocolError → requests ConnectionError) alias exactly. A 5xx/404/redirect root does NOT red (no status check); a hang is not a vector (rc=124, no LEGS-JSON → derived ERROR → setup=1 → predicate fail; probe :457-470). PFPP's zero collateral on L3/L4 is the point: do_POST is untouched. |
| K6 good/none | PFFF | L2 :31 (refused); L3/L4 red BEFORE any assert — ConnectionError at :47/:98, recorded `exc[name]="E"` | Yes, totally: a staged server that crashes at startup or binds another port is vector- and line-identical (harness proceeds with ready=False). K6 is the only case whose L3/L4 reds are exception-reds, hence the only legitimate `exc=2` in SUMMARY; `exc=` is recorded but not gated (:552-557) — acceptable, since any exc forces its leg F and the vector pins placement. |
| K7 absent/good | FPPP | L1 trips :13 "Model directory not found" | Yes, at vector level: identical FPPP to K8. A directory present but empty would red :22 instead — same vector. |
| K8 corrupt/good | FPPP | L1 trips :22 via :17 `from_pretrained` raising on the invalid `config.json` `{"model_type": "bert", ` (:13 passes; probe :403-407) | Yes — the dangerous alias: any `from_pretrained`/tokenizer exception, including a broken sandbox library, is line- and vector-identical. Mitigated in-design: K1's L1=P with the same bound venv in the same battery turns library breakage into a K1 mismatch (predicate fail) rather than a silent K8-style pass. |

### The three seat probes

1. **Would a 500-status root response pass `test_flask_api_running`? YES.** test_outputs.py:29
   discards the response; :30-31 catch only `ConnectionError`. Any HTTP status (200/404/500/503,
   redirects followed) is a P. So L2's live-listener red space is exactly {refused (K6),
   closed-without-response (K5), garbage status line (aliases K5)} plus hang (→ setup failure by
   the kill rule, not an F vector). Claim limitation (iv) — "K5 exercises the only failing mode a
   live listener can have" — is verified accurate for clean-F modes.
2. **Would an otherwise-correct server with `confidence` as float but wrong ordering pass? NO.**
   Ordering is asserted before types: :67-69 (positive) / :71-73 (negative) trip first. Such a
   defect is red on L3 with vector PPFP — it aliases the K2/K3 slot; no frozen case witnesses an
   ordering red (ordering is exercised only in the passing direction).
3. **Does K4's no-400 mode also break `test_sentiment_endpoint`? NO.** The 200-for-invalid branch
   (probe :225-230) fires only when `text` is missing/not-str/empty; all six L3 texts are non-empty
   strings → label path → correct 200 float JSON. L3 stays green; PPPF is exact.

### Leg-coverage arithmetic (my own count, from the eight frozen vectors)

| leg | P cases | F cases | seen |
|---|---|---|---|
| L1 test_model_downloaded | K1-K6 (6) | K7,K8 (2) | 6P/2F |
| L2 test_flask_api_running | K1-K4,K7,K8 (6) | K5,K6 (2) | 6P/2F |
| L3 test_sentiment_endpoint | K1,K4,K5,K7,K8 (5) | K2,K3,K6 (3) | 5P/3F |
| L4 test_api_error_handling | K1-K3,K5,K7,K8 (6) | K4,K6 (2) | 6P/2F |

→ `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` (probe semantics :546-551; the checker recomputes the
same from LEGS lines :696-699). Every leg has both witnesses; the line the predicate demands is
forced by the vectors and is the **ceiling** (legs=4), not a "minimum": for this grader the
minimum case count to reach seen_p=4 ∧ seen_f=4 is **2** (K1 PPPP + any all-F staging, e.g.
absent+none FFFF). The eight-case table is roughly four times the coverage minimum — the
redundancy prices defect families, and the claim's witness language is honestly saturated, not
padding presented as necessity. An extra case adds **nothing** to LEG-COVERAGE (ceiling), at most
one new vector — only FFFF is absent from {PPPP, PPFP, PPPF, PFPP, PFFF, FPPP}, and the
do-nothing control already derives FFFF on all eight ids (probe :568-586) — or one new red LINE:
exactly one grader assert is red-unreachable under the frozen modes (:107; :19-20 are practically
dead, not reachable by any staging).

### What the table fails to distinguish

1. **Vector-level aliasing pairs K2≡K3 (PPFP) and K7≡K8 (FPPP).** The receipt's VECTOR cannot
   separate them; separation rests on staged bytes — `check_receipt` re-stages all eight cases
   from the committed instrument and enforces `case_sha256` equality plus all-8-distinct
   (:652-665). That is byte-distinctness, not behavior-distinctness: a staging whose bytes are
   digest-correct but whose behavior mislabels the mode would pass every predicate clause
   (residual L1 authoring risk, frozen before data; the evidence-dir manifest detail is the live
   witness).
2. **Red-unreachable grader lines under the frozen modes:** :19-20 (practically dead),
   :50 (non-200 on a valid text), :56-62 (schema fields/keys), :67-73 (ordering), :107 (error
   body). Leg-level coverage is the claim's unit and is satisfied; per-line coverage is neither
   claimed nor achieved.
3. **The grader cannot see a label-lookup server:** L2-L4 never load the model; every server-mode
   red is a contract red, never an inference red. Declared limitation (i)/(iii) covers this; the
   table inherits it, so K1's green is not evidence of model use.
4. K6's `exc=2` in SUMMARY is expected and correctly ungated (see table above).

## Verdict per case (recommendation only — L1 rules; no edits made)

- **K1 keep** — P anchor on all four legs + environment binder against K8's alias.
- **K2 keep** — sole red witness of the expected-label clause (:86); K3 does not substitute.
- **K3 keep** — sole red witness of the float type clause (:77/80).
- **K4 keep** — sole red witness of L4's status clause (:103).
- **K5 keep** — sole clean-F live-listener red for L2 (:31) with zero collateral.
- **K6 keep** — total-outage witness; separates L2-red-with-collateral (PFFF) from K5 (PFPP);
  only exception-mode reds for L3/L4.
- **K7 keep** — absence red (:13).
- **K8 keep** — load-failure red (:22).
- **Drop: none.** Dropping one of K2/K3 or K7/K8 would preserve 4/4/4 and all six distinct
  vectors, but would lose a named defect family's only red witness.
- **ADD-ONE: K9 `("K9", "good", "400-no-error-field")`, expected `PPPF`** — server answers the
  missing-text body `400` with a JSON lacking the `"error"` key; L4 trips
  test_outputs.py:107 `assert "error" in error_data, "Error response should contain 'error'
  field"` — the only reachable grader assert no frozen case can turn red. It aliases K4's vector
  (distinguishable via `case_sha256` + manifest detail). Cost: SERVER_MODES/CASES/VECTORS edits,
  i.e. a re-freeze of the instrument — L1's decision, not mine.

**VERDICT CaseTableAudit71: the eight-case table is sound — every case prices exactly the leg its
note claims (K2:86, K3:77, K4:103, K5:31, K6:31+exception-reds, K7:13, K8:22); 4/4/4 is the
ceiling and is honestly saturated (2-case coverage minimum, 8-case defect-family table);
add-ONE K9 `400-no-error-field` (PPPF, test_outputs.py:107) is the single reachable coverage gap;
drop nothing.**
