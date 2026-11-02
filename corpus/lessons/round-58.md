# Round 58 — kengaku lesson (hyaku run 13, 2026-11-01)

author: kengaku L1 (round 58, Windows host). Base `a6b209cf`; freeze `d6bc6027`; receipts
`0e60ec31`; wave F `f58c0d6a`; wave P `c39d0e40`; wave C3 `b0b1d729`. The round's shape: the
two carried repairs (R56-F1, round50-c1) closed as frozen claims with measurements, and the
fifteenth grader read + executed as the corpus's first tolerance-band gate.

## Gate

Sources opened this round (2026-11-01, `curl` GET of the pinned raw URLs at TB2 pin
`2fd12b88`, bytes hashed on arrival, captures committed at `d6bc6027`): the full table with
quotes and sha256s is in `plans/round-58-claims.md` §Sources — S209 (task.toml, spec, A),
S210 (tests/test_outputs.py, code, A), S211 (solution/solve.sh, code, A — the maintainer
oracle), S212 (instruction.md, docs, A). All four admit tier A; no rejections; no flips of
existing rows (the S213–S217 supersessions are NEW rows under the Q34 corrections
convention — S201/S111/S112/S113/S140 keep their landed cells).

Flip check: S209–S212 are new rows (201→205 at the freeze; 205→210 with the supersessions at
wave F). The census at round end: exit 0, verdict ok, 20 W04 duplicate-url warnings (the 15
pre-existing + 5 from the supersession rows carrying their originals' URLs — the Q34
correction convention's cost, named here).

Admit/reject spot-check (LEARNING.md discernment), sampled for the outside closure: admit
S211 (the oracle — the maintainer's own solver re-run at authoring time, its accepted point
frozen as literals and confirmed elementwise), admit S210 (the executed tolerance-band
predicate), and the decision to carry ZERO U marks (a full-commitment 48-leg table — the
deterministic contrast with r57's timing gate; vindicated by 48/48 on the first run).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| freeze — the claims freeze wrote the probe's sha-refusal kill exit as 2 (house style) without measuring the exit path; measured KILL-EXIT=1 (uncaught SetupError → traceback; the refusal property itself holds — the drifted capture is never materialized nor executed) | `.ufo/waves/round-58/wavec/kl-sha-kill.txt`; dated correction appended to `plans/round-58-claims.md` | the tamper-kill receipt | predict only measured properties; when an instrument's exit map is part of a freeze prediction, exercise the error path on the toy grader BEFORE the freeze |
| landing — a wave-content script asserted mid-way after already applying two file edits (README index row + PROVINCE section); the re-run after fixing the assert DUPLICATED both; the divergence (knowledge files=61 vs index rows=62) was caught by the round36-c2 W4 leg at the tip run, not by the edit script | the tip full-counter receipt `.ufo/waves/round-58/wavec-tip/entryargv-full.txt` (`LAUNDERED round36-c2 … W6 DEFECT` era) and the W4 line in the wave-C pre-verification | the round36-c2 leg of the entry-truth counter — the designed tip capture, before any closure | content-edit scripts must be idempotent (guard on their own marker) or run once with a post-condition assert per file (counts, section counts) before the script exits |
| fixture authoring — the falsifier fixture lanes were built with doubled backslashes (`\\"` where the landed cell style is `\"`), so the first OLD-checker receipts measured a shape that exists nowhere in the lane; caught by comparing fixture bytes against the real S201 cell | scratch transcript vs `corpus/SOURCES.md` S201 cell bytes; rebuilt lanes + receipts `.ufo/waves/round-58/recon/esc-falsifier.txt` | deriving the fixture anchor from the REAL landed cell instead of re-typed escapes | fixture bytes are copied from the landed artifact they imitate; never re-typed |

## Carried → closed this round

- `round50-c1` (routed since r56): CLOSED with measurements — 125/126 deterministic drift,
  sole matcher n10-empty-repo, 0 unstable fixtures on this host; population re-pinned
  (`f41db91b`, dated), counter green.
- R56-F1 (routed twice): CLOSED — repaired with falsifier fixtures; the repair EXPOSED two
  real anchor-defect classes (R58-F1: S201's words miscount; R58-F2: unescaped/elided
  anchors S111/S112/S113/S140), both repaired by the S213–S217 supersessions.
- L0 questions `kengaku | round-25/33/51` (coverage cap) and `kengaku | round-56` (L2
  surface; ledger host column): STILL OPEN, nothing assumed answered — coverage is claimed
  predicate-met with the score held at 7 again.
