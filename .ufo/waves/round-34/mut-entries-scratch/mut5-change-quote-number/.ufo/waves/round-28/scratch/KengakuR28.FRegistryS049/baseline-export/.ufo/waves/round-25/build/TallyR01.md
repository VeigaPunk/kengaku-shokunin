# TallyR01 — independent oracle tally, attrib-r21-ds-trials.log (C1)

Method: grep/sed/awk only, directly on the committed receipt; no python, no lane scripts, no
journal/GT read, no endpoint contacted. Every claim below is a quoted command output.

## 1. Scoring-block inventory (P1 rule)
- `grep -c '^## GT + scoring at close' corpus/evidence/attrib-r21-ds-trials.log` -> 0. Blocks: none.
- Only `##` heading in the file: L130 `## Trial-runner-A addendum (2026-10-16T10:26Z, ...)`.
- No `AUTHORITATIVE SCORING SECTION` note, no `score_summary` JSON, no `gt_counts` key.
- P1 rule (plans/round-25-claims.md:28-30): scored block = LAST `## GT + scoring at close` block;
  "files with no such block contribute 0 scored trials and are reported as trial-only".
- => TRIAL-ONLY. Authoritative block: none. Scored trials contributed to C1: 0.
- Consequence: this receipt adds nothing to overall-accuracy / per-leg recall / per-leg specificity
  denominators, to the Rogan–Gladen inputs, or to the n>=17 power ask. It can only supply unscored context.

## 2. Trial tally (no GT in file, so no confusion table can exist)
- 20 trials, all class `std`, err=0 — own summary L128: `n=20 (std=20 err=0)`.
- Excluded trials: none (no GT, no exclusion mechanism fired).
- All 20: status 200, echo=requested, pt=48, body_len=221, span_class=burst, id_class=chatcmpl-uuid,
  hdr_tells = 7-token istio-envoy family, usage_tells = text_tokens+cached_tokens, wall 1.331-1.7561 s.
- Predictions: alibaba-token-plan x20; confidence 0.538 x20; scores 10.5/4.0/5.0 identical x20.
- Per-leg confusion (rows=GT leg, cols=prediction): EMPTY — the receipt stores prediction only; no GT
  leg column exists, so hyper / opencode-go columns are unobserved (0 GT trials each), not zero-correct.

## 3. Window and stamp integrity
- First request T01 2026-10-16T10:23:45.360Z (header L8 / record L13).
- Last request T20 2026-10-16T10:24:59.792Z (header L122 / record L127); +wall 1.420 s = 10:25:01.212Z,
  consistent with the file's own `last_request_utc=2026-10-16T10:25:01Z` (L128).
- Header stamp == record `t0_utc` for 20/20 (`paste` diff: ok=20 bad=0); trial_id sequence 1..20 in order.

## 4. Stored verdict lines
- NONE. No `ACCURACY:`, `TARGET:`, `BODY:`, or `STREAM TARGET:` line exists anywhere in the file.
- Only textual occurrence of "verdict"/"scored" is prose inside DEFECT-A (L152).

## 5. Trial ids + request UTC (duplication check)
```
T01 L8  10:23:45.360Z   T02 L14 10:23:49.424Z   T03 L20 10:23:53.319Z   T04 L26 10:23:57.248Z
T05 L32 10:24:01.156Z   T06 L38 10:24:05.030Z   T07 L44 10:24:08.889Z   T08 L50 10:24:13.145Z
T09 L56 10:24:17.005Z   T10 L62 10:24:20.867Z   T11 L68 10:24:24.811Z   T12 L74 10:24:28.730Z
T13 L80 10:24:32.563Z   T14 L86 10:24:36.471Z   T15 L92 10:24:40.349Z   T16 L98 10:24:44.181Z
T17 L104 10:24:48.014Z  T18 L110 10:24:52.075Z  T19 L116 10:24:55.924Z  T20 L122 10:24:59.792Z
```
- All 238 `t0_utc` stamps across the 9 P1 files are unique: `sort | uniq -d | wc -l` -> 0.
- Same-shim sibling attrib-r21-impl-ds-trials.log spans 10:21:04.575Z-10:22:19.434Z; this file starts
  10:23:45.360Z -> 85.926 s clear gap, zero overlap. Min intra-file spacing 3.832 s, no duplicate stamps.
- Identity caveat: L1 header text reads "attrib-r21-impl-ds-trials — instrument-impl seat" although the
  filename is attrib-r21-ds-trials.log; addendum L130-141 identifies it as trial-runner-A's run and the
  instrument-impl ds run as a separate file. A header-keyed P1 parse would double-count; filename-keyed
  parse (as P1 specifies) does not.

Frontier: no external source was opened this round (all evidence is local repo files, lines cited above),
so no SOURCES rows are emitted.

Installs: none.
VERDICT: trial-only receipt — 20 std trials, 0 scored, 0 GT rows, 0 stored verdict lines; contributes 0 scored trials to C1 and must not enter any accuracy/interval denominator.
