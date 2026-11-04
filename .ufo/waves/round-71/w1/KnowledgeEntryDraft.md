# KnowledgeEntryDraft — round 71 w1 (R71-C1 knowledge artifact)

Seat role: scribe/leaf. No subagent dispatch, no battery run, no git write. My item: write the
round-71 knowledge entry and its `corpus/README.md` index row into the lane working tree (the
L1 commits).

## What I ran (commands + rc)

Read-only source work, all from L = `/home/vgpnk/Projects/shokunin/kengaku-shokunin`:

1. Read `plans/round-71-claims.md`, `corpus/knowledge/tb2-nginx-request-logging-offline.md`,
   `corpus/QUALITY.md` Q1-Q7, `corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py`
   (full, `cat -n`), `plans/round71_c1_hf_probe.py` (:1-95, :90-130, :150-300, :380-470, :619-724).
2. `sha256sum corpus/evidence/round52/graders/hf-model-inference/tests/test_outputs.py` → rc 0,
   `61a686d6caf833ac3c240f2a8ceddacfed82b9f392c51b48ed8359d3e0f87857`; `wc -l` → `107`.
3. Live re-fetch at the pin (S245/S246 open, `curl -sS`, scratch
   `/fast/scratch/hyaku/kengaku-r71/KnowledgeEntryDraft`):
   - `…/2fd12b88…/hf-model-inference/instruction.md` → rc 0, HTTP 200, 1264 bytes, sha256
     `29151c5b2306f522f38fa905de3d34566865829355e5ca0895f4fca04d51dcc1`, `cmp` vs
     `corpus/evidence/round71/hf/instruction.md` → **byte-identical**.
   - `…/2fd12b88…/hf-model-inference/tests/test_outputs.py` → rc 0, 4239 bytes, sha256
     `61a686d6…f87857`, `cmp` vs the round-52 capture → **byte-identical**.
4. Model tree re-derived from the five committed files (`sha256` per file, sorted
   `sha256  rel` lines, one digest) → `c5c257677d7143af56903fe5f139b1acd90eae17c337eb966fd2fe087b858944`
   = receipt line 4 `MODEL tree_sha256=…` `files=5` (rc 0).
5. Receipt of record read: `cat -n corpus/evidence/round71/hf/receipt.txt` → 36 lines, sha256
   `136ec423409cbc3031925148b0571ad6edb1cfdf209b42586addb7e2499e6067`; `check.txt` = `DEFECTS n=0` /
   `PREDICATE R71-C1 pass` (sha256 `6acbb7a1…5447`).
6. Replicate receipt: `grep -E '^(VECTOR|LEG-COVERAGE|SUMMARY|PREDICATE|REV|LIBRARIES|CASE)'`,
   `cmp`, `diff` → all lines identical; `cmp` rc 0; both sha256 `136ec423…e6067`; mtimes
   22:22:33 and 22:23:39 (2026-11-03).
7. Per-case captures: `corpus/evidence/round71/hf/sandbox/K1…K8/{manifest.json,sandbox-stdout.txt,app-tree.txt}`
   parsed for `derived`, `exc`, `detail`, `server_pid`, `sandbox_rc`.
8. Control: `.ufo/waves/round-71/c1-control.txt` → 43 lines, sha256 `c7cfa201…bca0a`,
   `LEG-COVERAGE legs=4 seen_p=0 seen_f=4` (:41), `SUMMARY … mismatches=8 setup=0 exc=16` (:42),
   `PREDICATE R71-C1 fail` (:43).
9. Counters: `grep -c 'executed 3 of 8' SKILL.md` → `0`; `grep -c 'executed 4 of 8' SKILL.md` → `1`
   (at my first check the row still read `executed 3 of 8` (1/0); a sibling landed the L1 edit to
   4 of 8 during the wave). `grep -c hf-model-inference corpus/evidence/round52/graders/executed17.lst`
   → `0` (rc 1).
10. Census/refusal pointers: `corpus/evidence/round62/class-survey.txt:11` (member list) and `:21`
    (`classes-uncovered=…,network-service,…`); `.ufo/waves/round-36/build/R36ScoutNextTasks.md:41`
    (`Excluded: service + network`).
11. Instruction-text absence: `grep -c` on the instruction capture → `0` for `not bad`, `0` for
    `horribly beautiful`, `0` for `enjoyed this movie` (rc 1 each).
12. Q1/Q21 checks on my entry: first three lines are `source:`/`verified-at:`/`recheck:`;
    `for f in …; do grep -qE '^source:.*[0-9a-f]{40}' "$f" && ! grep -qE '^recheck:.*(commit|pinned|pin|[0-9a-f]{7})' "$f" && echo "unpinned $f"; done`
    prints nothing (`Q21_OK`). No trailing-whitespace lines.
13. Wrote the entry (247 lines, sha256 `44590ebcb562b123b7123f274da098c14b79a1aa072601c9c6af3a9072b13a1a`)
    and inserted the README row (`git diff --stat corpus/README.md` → `1 insertion(+)`;
    `corpus/README.md` sha256 `97e754718c761ad404da992640206212a836042cf50092d81b3deeaad49387c7`).

No tool was installed or upgraded this seat (nothing needed).

## What I found (evidence pointers)

**R71-C1's evidence is pass-shaped on committed/working-tree bytes.** Receipt of record
`corpus/evidence/round71/hf/receipt.txt`:

```
:11 VECTOR K1 expected=PPPP derived=PPPP agree=True     :14 K2 PPFP/PPFP   :17 K3 PPFP/PPFP
:20 K4 PPPF/PPPF   :23 K5 PFPP/PFPP   :27 K6 PFFF/PFFF   :30 K7 FPPP/FPPP   :33 K8 FPPP/FPPP
:34 LEG-COVERAGE legs=4 seen_p=4 seen_f=4
:35 SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2
:36 PREDICATE R71-C1 pass
```

`corpus/evidence/round71/hf/check.txt` = `DEFECTS n=0` / `PREDICATE R71-C1 pass`. The checker
(`plans/round71_c1_hf_probe.py:619-724`) re-derives grader/instruction/model/probe digests from
lane bytes, requires `REV` an ancestor of `master`, matches `LIBRARIES` against the host env at
check time, re-stages each case and recomputes `case_sha256`, recomputes each vector from the
`LEGS` lines, and recomputes coverage/summary/predicate.

**Determinism, measured, not asserted.** The two batteries are byte-identical
(`cmp` rc 0; same sha256 `136ec423…e6067`; same eight `case_sha256` values), 66 s apart. The
staged digest is taken over `/app` after staging and before the legs run, so it is run-independent
— the opposite of round 69's finding that `case_sha256` moved with a server-written access log.

**Leg laws (quoted from the grader, file order).** Leg 1 `test_model_downloaded` :8-22 — path
literal `/app/model_cache/sentiment_model` :12, `assert os.path.exists(model_path)` :13,
`from_pretrained` :17-18, `except Exception … assert False` :21-22. Leg 2
`test_flask_api_running` :25-31 — `requests.get("http://0.0.0.0:5000")` :29 with no
`raise_for_status`/status assert/timeout; only `requests.exceptions.ConnectionError` is turned
into a failure (:30-31). Leg 3 `test_sentiment_endpoint` :34-92 — six literals :36-43, POST to
`localhost:5000` :47, status 200 :50, four fields :56-63, label/confidence ordering :65-73,
`isinstance(…, float)` :76-82, expected label :84-92. Leg 4 `test_api_error_handling` :95-107 —
400 :103 plus an `error` key :106-107.

**The six texts are grader-only constants.** `test_outputs.py:37-43`; text 2 is one literal split
over :38-39. The instruction capture has none of them (`grep -c` → 0), and its schema block
(`instruction.md:11-28`) never names a text, a count, or a label.

**Measured failure fragments** (`sandbox/K*/manifest.json`): K2
`Text The journey was not bad; I actually had a good time. should be classified as positive`;
K3 `Confidence scores should be floats`; K4 `API should return 400 for invalid request format`;
K5/K6 `Could not connect to the Flask API on 0.0.0.0:5000`; K7 `Model directory not found`; K8
`Failed to load model or tokenizer: It looks like the config file at
'/app/model_cache/sentiment_model/config.json' is not a valid JSON file.` K6 legs 3/4 are
uncaught `ConnectionError` (`EXC K6 …=E`), recorded separately from assertion failures.

**The model-identity gap (new, load-bearing).** Leg 1 passes with a staged fixture whose
`corpus/evidence/round71/hf/model/config.json` declares `num_hidden_layers: 1`, `hidden_size: 8`,
`vocab_size: 49`, `architectures: ["BertForSequenceClassification"]` — six of eight cases are
leg-1 green. The instruction's named checkpoint (`instruction.md:3`) is never checked, so the
task text's model requirement is unenforced by the grader.

**Class row.** `corpus/evidence/round62/class-survey.txt:11` lists `hf-model-inference` in the
eight `network-service` members; `executed17.lst` has zero hits; the working-tree `SKILL.md:78`
now reads `executed 4 of 8` (`grep -c 'executed 3 of 8'` → 0). The move is therefore grounded in
lane bytes, not only in the claim.

## Verdict

The knowledge artifact now rests on the pass-shaped receipt of record and on re-derived digests:
`PREDICATE R71-C1 pass` at `REV d8a77d3`, all eight vectors `agree=True`,
`LEG-COVERAGE legs=4 seen_p=4 seen_f=4`, `SUMMARY cases=8 legs=32 mismatches=0 setup=0 exc=2`;
the `network-service` class row reads `executed 4 of 8` in the working tree. The entry records
that pass, the four leg laws, the six unstated texts, the load-path-only model leg, and an
explicit `## What this does not establish` section naming the lane-written stdlib server, the
host `/fast/ComfyUI/.venv` library versions (torch 2.14.1+cu130, transformers 5.21.0, requests
2.34.2, python 3.13.16), and the tiny random-weight fixture.

## Files written

- `corpus/knowledge/tb2-hf-model-inference-offline.md` — new, 247 lines.
- `corpus/README.md` — one row inserted at line 95, immediately after
  `knowledge/tb2-torch-pipeline-parallel-offline.md` (line 94) and before `lessons/round-54.md`.

Not touched: `corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, the nginx entry, the
round report, any `plans/` file, the fleet repo, `.ufo/state/`, `.ufo/watchdog.log`. I read
`SOURCES.md:260-261` only to confirm S245/S246 exist with digests matching what my `source:` line
cites (both do, incl. 1264 B / 28 lines and 4239 B / 107 lines).

## Open items / limits of this seat

- **Q10/Q13 second-seat re-read is not mine and is not yet on record.** The locations to re-check:
  grader lines 8-22, 25-31, 34-92, 95-107; instruction `:3-7,11-28`; receipt `:11-36`; census
  `:11,:21`; scout `:41`. The admitting commit's `## Gate` must cite a reviewer-like seat report
  (Q13), and until that report exists this entry is unadmitted.
- **`corpus/README.md` coverage-map bullet for round 71** (the round-scoped block around
  `:786-800`) is not among my named files and is absent; flagged for whoever writes the round-71
  coverage narrative.
- **Receipt portability.** `--check-receipt` binds the `LIBRARIES` line to this host's
  `/fast/ComfyUI/.venv` at check time, so a re-check on a host with different `torch`/
  `transformers` reports `DEFECT library-drift`. The entry says so; any future re-run needs the
  same host library provider or a re-baselined receipt.
- **Table-shape observation, not a defect.** K7 and K8 share vector `FPPP` (leg 1 red at two
  different asserts), so the eight-case table spends two cases on one leg and none on a
  hang/accept-then-silence mode; leg 2 has no timeout, so such a case would end as `ERROR` at the
  240 s cap rather than as a verdict. Reported, not edited.
