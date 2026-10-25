# R32 Sentinel — security/safety scan of round 32 new bytes (2026-10-25)

Scope: the three new tools (`plans/round32_defects.py`, `plans/catalog_probe.py`,
`plans/round32_c1_verify.py`), the drafted rows/entry (staged package
`/home/vgpnk/Projects/shokuknow/merge/kengaku/`: `SOURCES.append.md`,
`benchmark-grader-semantics.md`), and captures (`.ufo/waves/round-32/assimilation/captures/`,
`.ufo/waves/round-32/build/R32CatProbe.md`, wave control files in
`.ufo/waves/round-32/claims/`). No tools were installed or upgraded this round.

## (a) Credential material — NONE

Scanned with regex (API keys, secrets, tokens, passwords, bearer/authorization, `op://`
refs, `AKIA`/`sk-`/`hf_`/JWT/`BEGIN ... PRIVATE KEY`, userinfo URLs, signed-URL params
`X-Amz-Signature`/`GoogleAccessId`/`Signature=`), over: the three plans, the entire
`.ufo/waves/round-32/` tree (incl. captures and all build/ seat reports), and all 68
files of the staged merge package. Only benign substring hits found: `sk-parameterised`
(hyphenated English in `SOURCES.append.md`, `MERGE-REPORT.md`), `token` as prose in
`round32_defects.py` line 15 ("the bogus token"). Captures are public source bytes
(`toolathlon-ab-testing-evaluation-main.py`, `arxiv-2412.05579v2-abs.html`) with a
`SHA256SUMS.txt` manifest; recomputed digests match the manifest exactly
(`3bad26b61448f1f0c91808435e3239c3f7a6735ab865f0c27523fb6312a9b9ad` 14138 B;
`851b03db6bf5ae74ac7abe0512a0d12be97c8d7b6f99916e7e09356ae67b043d` 43647 B).

## (b) URLs public and pinned — PASS

- C1 draft entry cites exactly: `https://github.com/scaleapi/SWE-bench_Pro-os` @ commit
  `66f92766bba642462d4bbe5479e83f91f9211862`; `https://github.com/hkust-nlp/Toolathlon`
  @ commit `9be8d8fe07a497b18ee61e3f2ae694e9797f39eb`; `https://arxiv.org/abs/2412.05579`
  v2. Verified live on 2026-10-25: GitHub trees API HTTP 200 for both pinned commits
  (SWE tree sha `66f92766…`, contains `v2/tasks/*/tests/test.sh` and `tests/parser.py`;
  Toolathlon tree sha `9be8d8fe…`, contains `tasks/finalpool/ab-testing/evaluation/main.py`);
  arXiv abs page HTTP 200, title `<title>[2412.05579v2] LLMs-as-Judges: A Comprehensive Survey
  on LLM-based Evaluation Methods</title>` (capture also carries the v2 marker).
- The Toolathlon capture is byte-identical to `raw.githubusercontent.com` at the pinned
  commit (sha256 `3bad26b6…`, diff-identical), and the staged S094 row's quote
  `"def validate_record_data(actual_records: dict, expected_records: dict, tolerance_pct: float = 0.1)"`
  is present in the capture (`toolathlon-ab-testing-evaluation-main.py:58`).
- `SOURCES.append.md` rows (S077–S251) enumerate only public hosts (github.com,
  raw.githubusercontent.com, arxiv.org, meti.go.jp, nedo.go.jp, jstage.jst.go.jp,
  web.archive.org, osf.io, docs.aws.amazon.com, storage.googleapis.com, …); no session
  URLs, no private IPs/domains, no userinfo, no signed parameters. `catalog_probe.py`
  targets the two public live endpoints (`https://huggingface.co/api/models?limit=50`,
  `https://openrouter.ai/api/v1/models`) — both returned HTTP 200 today; OpenRouter needs
  no auth.

## (c) Command injection / shell=True — NONE

`round32_defects.py` uses `subprocess.run(["git", "-C", str(lane), *args], …)` — argv
list, no `shell=True`, no `os.system`/`popen`/`eval`/`exec`. `catalog_probe.py` uses
`urllib.request` only. `round32_c1_verify.py` does pure file reads/regex. No subprocess
elsewhere.

## (d) Scripts read only declared inputs — PASS

- `round32_defects.py`: reads only R31/R32 fleet reports, `corpus/evidence/round31/gate-cli-exits.txt`,
  `SKILL.md`, `corpus/lessons/round-31.md`/`round-30.md`/`round-32.md`, and runs
  `git -C <lane> rev-parse master` — all match the R1–R7 declarations in the docstring.
- `catalog_probe.py`: probes the two fixed public URLs and reads `corpus/knowledge/open-model-catalogs.md`
  under `--lane`. Writes nothing (receipts are produced by the probe seat, not this script).
- `round32_c1_verify.py`: reads `ENTRY`, `REGISTRY`, `README`, `EXPECT`, `CONTROL` under
  `--lane` — exactly the six checks' declared inputs.
None write to the repo; all print to stdout and exit 0/1.

## (e) Resource-exhaustion hazards — NONE significant

Bounded fetches: HF `?limit=50`; OpenRouter single fixed endpoint (captured 791,130 B
today); `timeout=20`; no pagination loops, no retries, no unbounded iteration; local reads
bounded by file sizes. Note (minor): `fetch()` read the whole response body with no explicit
size cap, but both endpoints are fixed-size and small — no practical hazard.

## Non-security observations for Main (not security findings)

1. The staged draft entry `benchmark-grader-semantics.md` carries `verified-at: 2026-10-23`
   and `(ran 2026-10-23)` (lines 5–6), while the frozen C1 predicate and
   `adoption-expect.json` (`access_date: "2026-10-25"`) require a
   `verified-at: 2026-10-25` line; `round32_c1_verify.py` V1 would fail on the staged
   draft as-is.
2. Staged rows S094/S097 (and S093) currently record `opened=2026-10-23` and S094/S097 are
   **not** present in the tip registry (`corpus/SOURCES.md` holds 91 rows; only S093 exists
   there, line 112). The frozen C1 predicate expects S094/S097 as new rows with
   `opened=2026-10-25`. The append/entry update must reconcile this before the counters run.
3. `catalogs-before.txt` (freeze control) already shows the live probe succeeded today
   (`hf=ok openrouter=ok hf_models=50 or_models=467`), confirming C3's endpoints and the
   schema deltas recorded in `R32CatProbe.md`.

## VERDICT: clean
