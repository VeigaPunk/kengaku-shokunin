# Round-14 mutation battery: does the extended grader gate bite on the round-12 tree?

Battery date: 2026-09-29. Target: prove the promoted `grader.py` r12 gate (732
checks at dispatch) detects real-byte mutations of `corpus/evidence/round12-ladder/`,
and adjudicate the r12-mutation.md report of a promoted-engine selftest defect.
Every command below was executed from repo root
(`/home/vgpnk/Projects/shokunin/kengaku-shokunin`) unless noted; observed output is
copied verbatim from stdout/stderr. Repo bytes were mutated in place only for
cases (c) and (d) (sidecars resolve from hardcoded `R12_DIR`,
`grader.py:1504-1511`); a tar backup (`tar -C corpus/evidence -cf
/tmp/r14-fleet-work/round12-ladder-backup.tar round12-ladder`, 19 members) plus a
per-file `/tmp/orig-*` copy was taken first, and per-file restore + md5 verify ran
immediately after each case.

## Claim 1 — selftest census: 8 cases (S0-S7), all PASS, exit 0

Command: `python3 grader.py --selftest`

Observed (exit 0, wall ~1.9 s):

```text
[selftest] PASS S0 control (clean copies): exit 0, expected 0
[selftest] PASS S1 stored-ok flip (record layer): exit 1, expected 1 + check-id r8.replay.A-INC.ok (flip applied: True, id fired: True)
[selftest] PASS S2 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r8.summary.A-INC (id fired: True)
[selftest] PASS S3 raw-digit bump (re-parse layer): exit 1, expected 1 + check-id r9.replay.A-MONO.got (mutation applied: True, id fired: True)
[selftest] PASS S4 r11 stored-ok flip (record layer): exit 1, expected 1 + check-id r11.replay.A-CKPT4710.ok (flip applied: True, id fired: True)
[selftest] PASS S5 r11 run.log SUMMARY edit (summary layer): exit 1, expected 1 + check-id r11.summary.A-CKPT4710 (id fired: True)
[selftest] PASS S6 stats anchors (betai/t_crit known values): all known-value assertions hold
[selftest] PASS S7 r12 stats anchors (Page L / grade_seq / Brier-BSS / Newton): all known-value assertions hold
[selftest] ALL PASS
```

Census: exactly 8 cases, S0 through S7. S0 also exercises the committed r12 tree:
its subprocess run passes no `--r12-*` overrides, so r12 defaults
(`DEFAULTS["r12_*"]`, `grader.py:74-76`) point at the real landed bytes. S7
re-proves the round-12 analytic anchors.

Also observed: `python3 grader.py --selftest-r12` → `ALL PASS (106 scenarios)`,
exit 0 (fixture battery incl. M36 runlog-cell edit, M84-M90 probability-file
sha/content mutations, M91-M95 ordering/bundle corruptions, M96 pin mismatch —
the draft-battery detectors now live in the root gate). Full clean run
`python3 grader.py` → `CHECKS n=732 mismatches=0 errata_pinned=1`,
`VERDICT: PASS`, exit 0.

## Claim 2 — four fresh real-byte mutations, all KILLED

Mutation (a): copy `run.log` to `/tmp/r14-mut-a/`, edit SUMMARY cell
`A-CKPT710: 21/64` → `A-CKPT710: 22/64`.

| mode | command | observed | result |
|---|---|---|---|
| path override | `python3 grader.py --r12-runlog /tmp/r14-mut-a/run.log` | `[pin] r12_runlog: SKIPPED (overridden path, treated as mutated copy)`; `MISMATCH r12.runlog.A-CKPT710: stored=(22, 64) recomputed=(21, 64)`; `CHECKS n=731 mismatches=1`; `VERDICT: FAIL` | KILLED (exit 1) |
| in place | `python3 grader.py` with mutated `run.log` | `MISMATCH pin.r12_runlog.md5: stored='700d1ddd…' recomputed='72cdbbe7…'`; `MISMATCH r12.runlog.A-CKPT710`; `CHECKS n=732 mismatches=2`; `VERDICT: FAIL` | KILLED (exit 1) |

Mutation (b): copy `results-r12.jsonl` to `/tmp/r14-mut-b/`, one byte inside the
`raw` fenced-JSON of A-INC pid 201 turn 1: `"washers": 0` → `"washers": 9`
(stored `got`/`ok`/`nwrong` untouched — re-parse layer must catch it).

| mode | command | observed | result |
|---|---|---|---|
| path override | `python3 grader.py --r12-jsonl /tmp/r14-mut-b/results-r12.jsonl` | `[pin] r12_jsonl: SKIPPED`; `MISMATCH r12.replay.A-INC.got: 1/640 records differ (first: (201, 1, 'got'))`; `.ok` and `.nwrong` likewise; `CHECKS n=731 mismatches=3`; `VERDICT: FAIL` | KILLED (exit 1) |
| in place | `python3 grader.py` with mutated jsonl | `MISMATCH pin.r12_jsonl.md5: stored='9dd8aa2b…' recomputed='4a7a0300…'`; same three `r12.replay.A-INC.{got,ok,nwrong}` mismatches; `CHECKS n=732 mismatches=4`; `VERDICT: FAIL` | KILLED (exit 1) |

Mutation (c): in place, flip one digit inside `predictions-r12-perproblem.jsonl`:
`"p_pass":0.601944,"pid":201` → `"p_pass":0.601945,"pid":201` (the bundle sha and
the sha stated in `predictions-r12.md:102` are left stale — the pinned-hash
family must catch it).

Command: `python3 grader.py`. Observed:

```text
MISMATCH r12.pred.probs_sha256: stored='bac550c7fc5e887da93e81369c63f839be080a52e1dfd211b7072446ef825e24' recomputed='1ce7396b8bbbfd81e89a0f6d4cee7540b3771d86a070079dd2c2b9fd2bb06da4'
MISMATCH r12.pred.probs_sha256_stated: stored='bac550c7…' recomputed='1ce7396b…'
MISMATCH r12.ordering.sha256.predictions-r12-perproblem.jsonl: stored='bac550c7…' recomputed='1ce7396b…'
CHECKS n=732 mismatches=3 errata_pinned=1
VERDICT: FAIL
```

KILLED (exit 1). Three independent sha pins fired: the prereg bundle line, the
digest stated inside `predictions-r12.md`, and the provenance digest used by
`_check_prob_sources`. Note: the +1e-6 probability shift did NOT move the
printed `analysis.e6.brier_*` values (recomputed Brier rounds back to the stored
text), so the sha family was the sole detector here — which is exactly the layer
this mutation targeted.

Mutation (d): in place, `rm ordering.log` (restored from `/tmp/orig-ordering.log`
immediately after; md5 `44f1b6700b3e801113fb1e276557c6ea` before and after).

Command: `python3 grader.py`. Observed:

```text
grader: INPUT ERROR: missing sidecar file: /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round12-ladder/ordering.log
```

KILLED (exit 2). The file-presence gate in `main()` (`grader.py:5699-5702`,
`die` → exit 2) fires before any check runs; the named artifact is the ordering
chain itself. Mechanism differs from cases (a)-(c) (INPUT ERROR vs MISMATCH),
but nonzero exit naming the right sidecar is unconditional — a deleted
ordering.log cannot reach VERDICT: PASS.

Mutation score: 4/4 KILLED (100%). Zero survivors.

## Claim 3 — RL3-defect adjudication: FIXED IN TREE, post-mutation-report

`corpus/evidence/round12-fleet/r12-mutation.md` (mtime 2026-09-28 22:48:33)
reports: `recompute_r12.py --selftest` exit 1 with
`AssertionError: no line with prefix 'VERDICT R2 replication'`; full run exit 2
`RL3: unparsed P 'diff - 0.352'`. Current tree, same commands:

```text
$ python3 corpus/evidence/round12-ladder/recompute_r12.py --selftest
SELFTEST 165/165 PASS        (exit 0)
```

`recompute-run.log` (mtime 2026-09-28 23:01:05) shows a successful full run:
`wrote …/analysis_r12.md from 4114 records` / `VERDICT R1 ladder: LADDER
ESTABLISHED`, and `analysis_r12.md` now exists on disk (md5
`029c3bcdcf11209d575734742bf239f6`, mtime 2026-09-29 00:28:13 — regenerated
after `recompute_r12.py`'s final edit, so the pinned analysis is the output of
the FIXED engine, not the broken one).

Root cause and fix, directly from the two files:

- `corpus/evidence/round12-fleet/recompute_r12_draft.py` (mtime 22:07, predates
  the report): `read_runlevel` at line 1072 splits on `|` and takes `cells[2]`
  as P; the real RL3 row is
  `| RL3 | E2 additionally POINT-MATCHES-r11 (|diff - 0.352| <= 0.15) | 0.45 | y |`
  (now embedded in the promoted selftest at `recompute_r12.py:2999`), whose own
  cell text contains raw pipes, so `cells[2]` lands on `diff - 0.352` → the
  observed `unparsed P` error. Same parser shape would produce the selftest
  assertion failure the report quotes.
- `corpus/evidence/round12-ladder/recompute_r12.py` (mtime 2026-09-28 23:08:13,
  ~20 min AFTER the report file): `read_runlevel` at line 1144 documents the
  hazard — "The RL3 event cell itself embeds raw `|` characters … probability is
  taken as the UNIQUE cell that looks like a bare probability, scanning from the
  right and skipping the trailing justification cell. Zero or two-or-more
  candidates is a hard failure" — and implements it (`_P_CELL_RE` candidate scan,
  `PredictionError` if `len(cands) != 1`, lines 1165-1169). The selftest gained a
  pinned regression: `chk("RL row with two embedded pipes still yields P=0.45
  for RL3", …)` (line 3005) plus two negative-parse checks (3011-3014).

Adjudication: the r12-mutation.md finding was TRUE at write time (draft engine
still in place / promoted engine mid-fix) and is FALSE against the current
bytes. The defect was repaired in-tree between the report (22:48) and
`recompute_r12.py`'s final mtime (23:08); the 165/165 PASS observed by L1 at
dispatch is reproduced above. Caveat [INFERENCE]: mtimes order the fix after the
report, but `recompute-run.log` (23:01) predates the final 23:08 mtime — the last
edit touched the selftest/hardening after the successful full-run artifact was
already written; either way the shipped parser is the pipe-aware one and both
failure modes are gone.

## Claim 4 — byte integrity after the battery

Baseline taken before any mutation: `cd corpus/evidence/round12-ladder && md5sum
* | sort > /tmp/r14-md5-baseline.txt` (18 entries — the dir contains exactly 18
files). After all four mutations and restores:

```text
$ md5sum -c /tmp/r14-md5-baseline.txt   # all 18 lines: OK
$ md5sum results-r12.jsonl run.log
9dd8aa2b6a7aa7890aa802c37d5af0f9  results-r12.jsonl   (matches R12_PINS)
700d1ddd2ece50d7bdedd55859c59f3a  run.log             (matches R12_PINS)
```

Final clean run after restore: `python3 grader.py` → `CHECKS n=732 mismatches=0
errata_pinned=1`, `VERDICT: PASS`, exit 0. `git status --short` still shows only
the pre-existing ` M grader.py`, ` M SKILL.md`, `?? corpus/evidence/round12-*/`,
`?? round13-ack-state/` plus this new artifact dir; no r12 byte was left
mutated. `/tmp/r14-mut-a/`, `/tmp/r14-mut-b/`, `/tmp/orig-*` hold only mutated or
backup copies — no repo path points at them.

## Gaps and notes

- Override-mode runs skip the landed-byte pin by design (`check_r12_pins`
  prints `SKIPPED (overridden path, treated as mutated copy)`), so the in-place
  runs are the ones proving `pin.r12_*.md5` bites; both modes are recorded above.
- Case (d) kills via `die()` (exit 2, INPUT ERROR) rather than a MISMATCH line —
  a missing sidecar is an input-contract violation, not a graded discrepancy.
  SURVIVED-class gap: none found; if a policy requires a MISMATCH for missing
  files, that is a convention question, not a coverage hole.
- The promoted gate does NOT pin `analysis_r12.md` in `R12_PINS`
  (`grader.py:1533-1536` pins only jsonl + runlog); the md is re-verified
  line-by-line against recomputation instead (~200 `r12.analysis.*` checks per
  the fixture battery's M40-M83 mutants), which is the stronger guarantee.
- `--selftest` covers r8/r9/r11 record+summary+reparse mutations plus stats
  anchors; it does not itself corrupt r12 bytes — r12 mutation coverage lives in
  `--selftest-r12` (106 scenarios) and in this battery's 4 real-byte cases.
