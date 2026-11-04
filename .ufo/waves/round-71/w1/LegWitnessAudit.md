# LegWitnessAudit — R71-C1 leg pricing (round 71 w1)

Seat: `LegWitnessAudit` (leaf auditor). Scope: audit what each red leg of the R71-C1 replay
actually is — the round-70 limitation (iii) question — and write the table + quotes + a verdict
per leg. Artifact: `.ufo/waves/round-71/w1/LegPricing.md` (the table and full analysis).

Writes: `W/LegPricing.md`, this report, and `/fast/scratch/hyaku/kengaku-r71/LegWitnessAudit/`
only. No commit, no port taken, no battery started by me, no case table / predicate / vector /
digest / receipt byte edited. No tool installed or upgraded.

## What I ran (commands + rc)

| # | command | rc | note |
|---|---|---|---|
| 1 | `read plans/round-71-claims.md` | 0 | frozen table and predicate (§R71-C1 lines 22–57) |
| 2 | `ls -la corpus/evidence/round71/hf/sandbox/` | 2 | capture dir did not exist yet; build battery was still running |
| 3 | `git -C L rev-parse master` / `git log --oneline -3 master` | 0 | tip `d8a77d3f` (freeze commit); read-only |
| 4 | `ls plans/ \| grep round7`; `git status --porcelain` | 0 | `plans/round71_c1_hf_probe.py` present (34974 B); only untracked wave artifacts |
| 5 | `cat .ufo/waves/round-71/c1-control.txt` | 0 | control: 8 × `FFFF`, `LEG-COVERAGE … seen_p=0 seen_f=4`, `SUMMARY … exc=16`, `PREDICATE R71-C1 fail` |
| 6 | `ps -eo pid,etimes,args \| grep round71_c1` | 0 | `HfBatteryR71`, `l1-selftest`, `HfBatteryReplicate` already running — I did not enqueue a competing battery |
| 7 | `sha256sum` + `cat -n` on `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` | 0 | `61a686d6…f87857` = pin; 107 lines; 19 assert statements |
| 8 | `cat -n corpus/evidence/round71/hf/instruction.md` | 0 | request/response/error schema |
| 9 | `cat` of `sandbox/K{1..8}/{manifest.json,sandbox-stdout.txt,sandbox-stderr.txt,app-tree.txt}` and `receipt.txt` | 0 | all eight captures present; no case needed re-running |
| 10 | eval: parse the eight manifests + receipt, rebuild the case×leg matrix, check unique `case_sha256` | 0 | 8 distinct staged digests; every `LEGS` line reproduces its `VECTOR derived` |
| 11 | eval: import `plans/round71_c1_hf_probe.py`, `prepare_work`+`stage_case`+`case_dir_sha` for all 8 cases into `S/stage` | 0 | all eight digests equal the receipt's `CASE … case_sha256`; K1↔K5 diff is only `MODE`; K1↔K2 diff is `MODE` + one `LABELS` entry; K8 `config.json` = `{"model_type": "bert", `; K7 has no `sentiment_model/` |
| 12 | eval: AST-parse the grader's `test_texts` (`:36-44`) and compare with the probe's `LABELS` | 0 | 6/6 texts and labels agree; key sets identical |
| 13 | `env \| grep -iE 'proxy\|PYTHONOPTIMIZE'` | 1 | none — no proxy could have produced K5's refusal, and asserts were live (`-O` absent from `bwrap_argv`) |
| 14 | eval: primary vs `sandbox-replicate/` manifests for all 8 cases | 0 | `case_sha256`, `detail`, `exc` identical in all 8; replicate receipt also `PREDICATE R71-C1 pass`, `SUMMARY … exc=2` |
| 15 | eval: read `ready`/`server` flags per case; enumerate the 19 assert statements | 0 | `ready` true for K1–K4/K7/K8, false for K5, null for K6 |

## What I found

**Matrix (from the manifests; full quotes in `LegPricing.md` §1–§2).**

```
K1 good/good            P P P P     K5 good/root-drops   P F P P
K2 good/wrong-label     P P F P     K6 good/none         P F E E
K3 good/int-confidence  P P F P     K7 absent/good       F P P P
K4 good/no-400          P P P F     K8 corrupt/good      F P P P
```

- All nine `F` cells are the intended mechanisms. Seven are the grader's own assertions at six
  distinct statements: `:13` (K7 "Model directory not found"), `:22` (K8 "Failed to load model
  or tokenizer: … config file … is not a valid JSON file."), `:31` (K5 and K6 "Could not connect
  to the Flask API on 0.0.0.0:5000"), `:77` (K3 "Confidence scores should be floats"), `:86`
  (K2 "Text The journey was not bad; I actually had a good time. should be classified as
  positive"), `:103` (K4 "API should return 400 for invalid request format"). The two K6 `E`
  cells are uncaught `ConnectionError`s (`[Errno 111]`) from `:47`/`:98` — those legs' assert
  code never ran.
- K8 prices a **config-JSON parse failure**, not corrupted weights: the staged corruption is
  `config.json` = `{"model_type": "bert", ` (verified by re-staging); transformers raised and
  the grader's `:21-22` converted it, which is why K8 carries no `E`.
- K5's red is a genuine assertion: the grader's `except requests.exceptions.ConnectionError`
  (`:28-31`) converted the dropped `GET /`; the harness's own probe recorded `"ready": false,
  "server": true, "server_pid": 3`, while K1–K4/K7/K8 record `true` and K6 `null`.
- **Limitation (iii) is discharged.** Six cases are single-red (K2, K3 → L3; K4 → L4; K5 → L2;
  K7, K8 → L1), so each leg is isolated at least once with the rest of the state green; K6 is
  the only whole-state multi-red case and is redundant for isolation.
- **Coverage is leg-level, not statement-level.** Of 19 assert statements, only 6 have a
  negative witness. Unpriced: L3 `:50` status, `:56/:57/:58/:61` missing fields,
  `:67-69`/`:71-73` ordering, `:76` non-str, `:80-82` negative-float, `:90-92` negative label;
  L4 `:107` error-field; L1 `:19/:20` `is not None`.
- **L2's two reds are one mechanism.** K5 and K6 produce byte-identical 66-byte detail at the
  leg's only assertion (`:31`); only staging and `ready` distinguish "no listener" from
  "listener drops". Any HTTP answer passes L2 — limitation (iv) confirmed from `:29`.
- **`EXC` separates correctly, but means "non-assertion exception escaped the leg".** The
  receipt's only `EXC` line is `EXC K6 test_api_error_handling=E test_sentiment_endpoint=E`
  (`SUMMARY … exc=2`); all other cases are `"exc": {}`. K5's connection failure is also a
  connection error but is absent from `EXC` because the grader caught it — so `EXC` must not be
  read as a connection-error tally. The harness's `except AssertionError` precedes
  `except Exception`, so the classes cannot cross. Detail strings are capped at 220 chars, which
  cuts `Connection refused` to `[Errno 111] Con`.
- Determinism: the replicate battery's eight manifests match the primary byte-for-byte on
  `case_sha256`, `detail` and `exc`; both receipts end `PREDICATE R71-C1 pass` with
  `LEG-COVERAGE legs=4 seen_p=4 seen_f=4` and `SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2`.

## Verdict

The R71-C1 reds are the intended ones **as mechanisms**: every leg is witnessed both `P` and
`F`, every F is traceable to a named grader statement (K2 label `:86`, K3 float `:77`, K4
status `:103`, K5 connection `:31`, K7 directory `:13`, K8 load `:22`), and the six single-red
cases discharge round-70 limitation (iii). The witness is narrower than "each leg's failure
mode": 13 of 19 assert statements never fail in this table, L2's two F witnesses are one
mechanism, K6's L3/L4 reds are escaped exceptions rather than assertions, and K8 prices a
config parse error rather than weight corruption. None of that contradicts the frozen predicate
— it bounds what the receipt proves.

## Evidence retained

- `corpus/evidence/round71/hf/receipt.txt` (re-verified: `LEG-COVERAGE`, `SUMMARY`,
  `PREDICATE R71-C1 pass`).
- `corpus/evidence/round71/hf/sandbox/K{1..8}/{manifest.json,sandbox-stdout.txt,sandbox-stderr.txt,app-tree.txt}`.
- `corpus/evidence/round71/hf/receipt-replicate.txt` + `sandbox-replicate/K{1..8}/manifest.json`.
- `.ufo/waves/round-71/c1-control.txt`.
- Grader: `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` (`:13`, `:22`,
  `:31`, `:47`, `:77`, `:86`, `:98`, `:103`, `:107`); probe: `plans/round71_c1_hf_probe.py`
  (`CASES`, `VECTORS`, `SERVER_TMPL`, `stage_case`, `HARNESS_SRC`).
- Re-staged case digests under `/fast/scratch/hyaku/kengaku-r71/LegWitnessAudit/stage/cases/`.

## Risks

- K8's exact exception text is library-version dependent (`transformers 5.21.0` from
  `/fast/ComfyUI/.venv`, receipt `LIBRARIES` line); the assertion mechanism is not.
- The P-side "return that made it pass" is derived from the staged server source + `ready` flag
  + absence of `detail`; the server's stdout is `DEVNULL`, so no response bodies are retained.
- My audit did not re-run the battery; it rests on the committed captures plus the replicate
  run, which agree exactly.
