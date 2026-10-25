# TallyR07 — independent hand-tally: corpus/evidence/attrib-r22-opencode-trials.log
Seat KengakuR25.TallyR07, read-only. grep/sed/awk only; no python, no lane scripts. Installs: none.
## Blocks
- 364 lines; exactly one `## GT + scoring at close` block: 204–254 (255 blank, 256 next heading).
- P1 rule (plans/round-25-claims.md:28-30): authoritative = LAST block -> 204. No in-file
  `AUTHORITATIVE SCORING SECTION` note (grep -i authoritative -> no hits); last-block rule only.
- Header 204: journal read AFTER all trials 2026-10-16T11:52:23Z; window @1792151440..@1792151562,
  request-lines=68 leg-rids=68 allfail=0 (205-206).
## Rows counted (table 212–231: T01@212, T20@231, step 6)
- 20/20 table rows equal the 20 {"kind":"record"} lines on (trial_id,class,prediction): diff empty.
- classes 10 force-hyper + 10 force-opencode-go; predictions 10 hyper + 10 alibaba-token-plan;
  all 20 correct=YES.
- Confusion (rows GT leg, cols prediction; all unlisted cells 0):
    alibaba-token-plan | alibaba 10 | hyper 0 | opencode-go 0 | n=10
    hyper              | alibaba  0 | hyper 10 | opencode-go 0 | n=10
    opencode-go        | n=0
- scored n=20, correct=20 (1.000), excluded none (254 "excluded": []; every GT class `served`,
  every chain ends `OK 200`). Per-leg recall: leg1 10/10, leg2 10/10, leg3 0/0 (UNTESTED).
  One-vs-rest specificity: leg1 10/10, leg2 10/10, leg3 20/20 — vacuous, opencode-go is never
  argmax (all 20 scores= lines 82-201 rank it third). Bars: ACCURACY 0.80/min scored n 20;
  TARGET 0.80/min on-target n 10.
## Stored verdict lines (verbatim)
- 234 ACCURACY: 20/20 = 1.000 (bar 0.80, min scored n 20) -> PASS
- 236 TARGET hyper: on-target GT n=10, correct 10/10 = 1.000 (bar 0.80, min on-target n 10) -> PASS | class GT dist {'hyper': 10}
- 237 TARGET opencode-go: on-target GT n=0, correct 0/0 = 0.000 (bar 0.80, min on-target n 10) -> FAIL | class GT dist {'alibaba-token-plan': 10}
- BODY / STREAM TARGET verdict lines: ABSENT (grep -E 'BODY|STREAM TARGET' -> no hits).
- 254 score_summary repeats: accuracy 1.0, scored 20, correct 20, PASS, excluded []. Prose
  restatements at 283-286 and 311 are authored, not instrument output.
- C1 caveat: 237 says FAIL at n=0, but shared `verdict(k,n,bar)` must return UNTESTED at n=0;
  the stored FAIL is the frozen per-target "target not reached" rule, not an accuracy measure.
## Trial ids + request t0 (UTC 2026-10-16)
T01 11:50:45.244  T02 11:50:51.193  T03 11:50:55.036  T04 11:50:59.847
T05 11:51:03.677  T06 11:51:09.366  T07 11:51:13.216  T08 11:51:18.000
T09 11:51:21.828  T10 11:51:26.795  T11 11:51:31.022  T12 11:51:36.040
T13 11:51:39.929  T14 11:51:45.233  T15 11:51:49.173  T16 11:51:54.272
T17 11:51:58.350  T18 11:52:03.293  T19 11:52:07.181  T20 11:52:12.302
- anchors 82..196 step 6; footer 202 n=20 last_request_utc=11:52:13Z; gaps 3.828–5.949 s
  (> 2.5 s floor); ids file-local — legs.log reuses T01–T20 for each of its two runs.
## Cross-file duplication
- windows: this 11:50:45.244–11:52:12.302 (20); legs.log 11:50:06.945–11:55:07.542 (40 = two
  20-trial runs); legs-hyper.log 11:50:58.065–11:52:26.186 (20).
- ms-identical timestamps shared across files: 0. Pairs |dt|<=250 ms: 3 — T01 11:50:45.244 vs
  legs.log:39 T06 (126 ms); T05 11:51:03.677 vs legs.log:63 T10 (156 ms); T15 11:51:49.173 vs
  legs.log:123 T20 (3 ms). Pairs <=2 s: 7, incl. the 3 named (T15/T16/T17 vs legs-hyper
  T13/T14/T15: 1903/1876/1713 ms); the claimed "13 pairs inside 2 s" is not reproducible.
- sample identity: legs.log's authoritative block is its LAST (312–363, request-lines=37) and
  scores its second run 11:53:41.144–11:55:07.542, not this file's sample. Identical row shape,
  different requests: P2's "same sample" does not hold at receipt-row level; only traffic
  interleaves. The lone r22 leg-3 GT trial (legs.log first block T03, chain 3/opencode-go OK
  200, counts {hyper:9, alibaba:10, opencode-go:1}) is in the superseded block.
- header seam: line 1 = trial-runner-opencode, instrument 34c4fa67…, frozen 124ade67…; line 74
  re-opens as leg-coverage-impl, instrument 05da8927…, frozen 3d7861f8…; trials 82–201 and
  scoring (207-208) run under the second, so line 4's pin is stale vs the run/scoring pin.
VERDICT: sole GT block 204–254 is authoritative by the last-block rule (no in-file note);
20/20 scored, zero excluded, perfect 2-leg diagonal (hyper 10/10, alibaba 10/10; opencode-go
0 GT and never predicted), bar 0.80 at min-n 20/10; stored 234 PASS, 236 TARGET hyper PASS
(n=10 k=10 — the P1 input), 237 TARGET opencode-go FAIL at n=0 (collides with UNTESTED), no
BODY/STREAM TARGET; trials 11:50:45.244–11:52:12.302Z are a distinct sample from legs.log's
authoritative 11:53:41–11:55:07Z block despite 3 sub-250 ms interleavings; a two-seat header
seam must be resolved before crediting these rows to one seat.
