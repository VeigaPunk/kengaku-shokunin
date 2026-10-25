# TallyR09 — independent oracle: `corpus/evidence/attrib-r23-stream.log` (C1/P1)
Read-only hand-tally, grep/sed/awk only (no python, no lane scripts, no journal read). Identity: sha256
`afaae9ddaf4deda0095c2e7ad39c6cb63236d72c812ca2fcd9ab18c42eef8131`, 420 lines, blob at HEAD `3f371d2a`
(worktree clean for the path); 30 `=== [T..]` headers ↔ 30 `record` lines.
## 1. Every `## GT + scoring at close` block
- Block 1 **:194–256** — heading :194 (`2026-10-16T13:49:42Z`), ends `score_summary` :256. Block 2 **:258–320** —
  heading :258 (`2026-10-16T13:51:16Z`), ends `score_summary` :320 (`grep -c` → 2; :257/:321 blank; :322–420 adjudication, no block).
## 2. Authority under P1
- Last-block rule → **Block 2 (:258–320)**; the file's own note concurs: `:341` "Block 2 is authoritative" (`:322`
  "below the authoritative blocks"). No literal `AUTHORITATIVE` token exists in this file.
- Dedup (P1): blocks 1/2 carry byte-identical 30-row tables (`diff` → IDENTICAL) → one sample; Block 1 is the named
  duplicate. Sole deltas: :194/:258 (time), :196/:260 (journal 444/req 152 vs 464/req 160), :198/:262 (instrument
  `cce53a16…` vs `489f938a…`), :256/:320 (`verdict` PASS vs FAIL). Block 2's sha ≠ run-time pin (`:3`, `cce53a16…`);
  the receipt discloses a scoring-path-only edit (:341–347), unverifiable from these bytes [INFERENCE].
## 3. Block-2 per-leg confusion table (rows :264–295; 30 rows, every row has GT)
| GT \ pred | alibaba-token-plan | hyper | opencode-go | row n |
|---|---|---|---|---|
| alibaba-token-plan | **6** | 0 | 0 | 6 |
| hyper | 0 | **24** | 0 | 24 |
| opencode-go | 0 | 0 | 0 | 0 |
- scored n=30, correct=30, accuracy 1.000. Excluded: **none** (`"excluded": []` :320; 30/30 rows have GT leg + chain;
  `gt_class` = `served` ×30; 30/30 records `status 200`, `"error_tells": []`).
- Recall: alibaba 6/6=1.000 · hyper 24/24=1.000 · opencode-go **UNTESTED** (n=0). Specificity: alibaba 24/24 · hyper
  6/6 · opencode-go 30/30 (vacuous — never predicted).
- Bar / min-n: overall bar **0.80**, min scored n **20** (:298); target bar **0.80**, min on-target n **10** (:303).
  Class split hint 3 / inspection 24 / marker 3; GT dist hint {alibaba:3}, inspection {hyper:24}, marker {alibaba:3}.
## 4. Every stored verdict line in Block 2
- `:298` `ACCURACY: 30/30 = 1.000 (bar 0.80, min scored n 20) -> PASS`
- `:299` per-leg GT honesty note (no verdict token)
- `:300` `BODY stream-hint: scored n=3, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'alibaba-token-plan': 3}`
- `:301` `BODY stream-inspection: scored n=24, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'hyper': 24}`
- `:302` `BODY stream-marker: scored n=3, on-target(opencode-go) n=0, correct 0/0 = 0.000 | GT dist {'alibaba-token-plan': 3}`
- `:303` `STREAM TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL`
- `:320` `score_summary`: `verdict "FAIL"`, `shim_level_verdict "PASS"`, `scored 30`, `correct 30`, `excluded []`.
- No plain `TARGET` line (`grep -n TARGET` → :303 only). Re-derivation: the three BODY lines and :303 are **0/0** →
  under the frozen rule (`UNTESTED` iff n=0) they re-verdict **UNTESTED**; the stored `-> FAIL` at :303 is a point-rule
  artefact, not an interval verdict.
## 5. Hand arithmetic anchors (`0.025^(1/n)`, checked with awk `exp(log(...))`)
- overall 30/30 → CP95 `[0.884297, 1.000000]` (≥0.80 → PASS; n=30 ≥ n=17 power ask). Power check: n=16 → 0.794093,
  n=17 → 0.804936 (matches `plans/round-25-claims.md`).
- Recall: alibaba 6/6 `[0.540742, 1]` (n<17, lo<0.80 → INDETERMINATE); hyper 24/24 `[0.857526, 1]` (PASS); opencode-go n=0 → UNTESTED.
## 6. Trial ids + request timestamps (all `2026-10-16T…Z`; headers = record `t0_utc` 1:1)
T01 13:46:41.501 · T02 13:46:45.386 · T03 13:46:51.621 · T04 13:46:55.678 · T05 13:46:59.808 · T06 13:47:05.236 · T07 13:47:09.348 · T08 13:47:14.245 · T09 13:47:21.169 · T10 13:47:25.113
T11 13:47:30.868 · T12 13:47:36.666 · T13 13:47:43.320 · T14 13:47:48.980 · T15 13:47:54.755 · T16 13:48:00.637 · T17 13:48:07.270 · T18 13:48:13.305 · T19 13:48:19.789 · T20 13:48:25.971
T21 13:48:31.446 · T22 13:48:37.539 · T23 13:48:43.299 · T24 13:48:49.505 · T25 13:48:55.503 · T26 13:49:01.259 · T27 13:49:07.945 · T28 13:49:13.677 · T29 13:49:19.413 · T30 13:49:24.572 (+ close :192 `last_request_utc=13:49:28Z` = T30 t0 + 4.351 s wall)
- **Near-twin run** `corpus/evidence/attrib-r23-stream-trials.log:227–418`: same v3 protocol + instrument `cce53a16…`,
  T01 13:46:18.559 → T30 13:49:00.941, 30 records, no GT block (trial-only → 0 scored trials under P1). Exact timestamp
  collisions with this file: **0**; min |t0 gap| **0.069 s** (this T24 13:48:49.505 vs twin T28 13:48:49.436) — confirms
  the twin's `:460-481` "0.07 s" claim. Both runs send the identical 269-byte inspection body and join windows
  [t0−1, t0+3] overlap → rid-level provenance mixed (twin §H landings are blind inference, no GT); leg-level GT is
  robust only because both runs landed hyper/alibaba alike.
- r21/r22 receipts: **0** trial headers in 13:46–13:49Z (`grep -c` on all seven → 0), so no other P1 file duplicates these stamps.
## 7. Remaining unknowns
- Journal not committed: "all 30 matched to journal REQUEST lines" (:332–334) is offline-unverifiable.
- `:326` claims first trial `13:46:16.559Z`; no such stamp exists here (T01 = 13:46:41.501Z). Closest is 13:46:18.559Z
  in `attrib-r23-stream-trials.log` — likely typo/merge [INFERENCE]; chain still holds (frozen 13:45:47 < 13:46:41.501
  < 13:49:24.572 < GT read 13:49:42). Whether the 0/0 lines were meant as evaluated FAILs or unevaluated is unresolved.
VERDICT: Block 2 (:258–320) is authoritative; 30/30 correct on a clean 6/24 diagonal, 0 excluded, bar 0.80 / min-20 →
interval **PASS [0.8843, 1.0]**; the opencode-go leg and every 0/0 line are **UNTESTED**, so the stored
`STREAM TARGET … -> FAIL` does not re-derive under the frozen interval rule. Installs: none.
