# Round 56 — kengaku verifier spotcheck (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Closed 2026-11-01. Lane head verified `d834d89d95929382cf6bfcb503e0d00b5dfa64e5` (= local
`refs/heads/master` = `ls-remote origin refs/heads/master`); base `8db18e230d6f`. All
re-measurements below were run by this judge inside WSL2 Ubuntu-24.04 (python 3.12.3,
git 2.56.0, bwrap 0.9.0, biopython 1.85, gcc/sqlite3/zip/strace present, **uv absent**,
`/fast/scratch/hyaku/kengaku-r55` present) on fresh clones of the lane repo, exits captured
into receipt files per the round's own relay lesson. Nothing in the lane repo or fleet repo
was mutated; mutations for the kill re-runs were applied to judge-owned scratch clones only.

**Verdict up front: admitted.** Every declared claim verifies at its named measured revision
(`9bc20ab7`, the canonical close), no owned axis is harmed — and the lane branch tip
`d834d89d` carries one real regression the lane's own gate catches (routed defect R56-V1
below; status-neutral per the gate standard, fix routed to round 57).

## 1. Step-1 conformance

| check | command (abridged) | observed | result |
|---|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an %ae %H' -1 -- .ufo/reports/round-56/kengaku.md` | `kengaku-shokunin kengaku@shokunin.local 317a12ad39c1` | PASS |
| SHONEN heading | read report | `## SHONEN` with one `[~]` line per box (4 boxes), no `[x]` | PASS |
| cited commits exist + in-range | `rev-parse` + `merge-base --is-ancestor` for `1192e465`, `4a5dc42e`, `9bc20ab7`, `d834d89d` | all four exist, all ancestors of master, all inside `8db18e23..d834d89d` | PASS |
| branch pushed | `ls-remote origin refs/heads/master` vs local | both `d834d89d95929382cf6bfcb503e0d00b5dfa64e5` | PASS |
| erratum target commit | `git show --stat ebb233bc` | `ebb233bc` (2026-10-30 14:46:43 -0300) landed `SKILL.md +5` AFTER the r55 report commit `93fd3095` (12:54:38 -0300, "SKILL.md (unchanged this round)") | PASS — erratum accurate |
| L0 lines durable | `git -C <fleet> show HEAD:.ufo/l0-questions.md | grep -c 'kengaku | round-56'` | 2 (L2-surface question; ledger-schema-v2 host column) | PASS |
| dispatch/complete digest | orchestrator watchdog lines quoted in contract | `launch … round=56 base=8db18e23` / `complete … head=d834d89d pushed=True` | PASS |

Conformance defects (status-neutral, named): see §6 (V2 SF14 count wording, V3
"seventeen" wording, V4 findings-ledger re-encoding).

## 2. Claim re-checks (re-measured by this judge)

### R56-C1 — operability 8→9 — RE-MEASURED, verifies

Command (WSL, fresh clone, `git checkout -B master 9bc20ab75c1b8881cd915d0e3eab18bf8387ca3d`):

```
python3 plans/round56_landcheck.py --lane <clone> --work <scratch> --receipt /dev/null
```

Observed (this judge, canonical revision `9bc20ab7`, master checkout, uv-less):

```
[PASS] L-reg registry closure (MISSING 0, PREDICATE R52-C2 pass)
[PASS] L-chess chess probe re-run == committed receipt (cases=12 observed_pass=5 observed_fail=7 mismatches=0)
[PASS] L-selftest entryargv selftest (4/4 PASS)
[PASS] L-grader grader replay+selftest (CHECKS n=733 mismatches=0, ALL PASS)
LANDCHECK PASS n=4
LANDCHECK_EXIT=0
```

Checker selftest 7/7 (`[selftest] ALL PASS (7/7)`, exit 0) — re-run, matches
`integrate/c1-selftest.txt`. Three mutation kills re-run in judge-owned tampered clones at
`9bc20ab7` (registry row `adoption-check` dropped / `cases=12 observed_pass=5`→`=6` byte flip
in the committed chess receipt / one byte appended to the md5-pinned
`corpus/evidence/round9-replication/results-r9.jsonl`): each produced exactly
`LANDCHECK FAIL failed-legs=1`, `EXIT=1`, failing exactly L-reg / L-chess / L-grader.
**Every leg is killable; kill rule not fired. Verdict: improved (8→9).**

### R56-C2 — calibration 9→10 — RE-MEASURED, verifies

Command (WSL, same canonical clone; uv absent per A3.4):

```
python3 plans/round55_c2_entryargv.py --lane <clone> --source <clone> --work <scratch> --jobs 4 --timeout 900
```

Observed (this judge):

```
ROWS registry=83 ledger=83 missing=0 extra=0 argv_defect=0 wrapper_defect=0 abbrev_defect=0 bad_decl=0 duplicate_names=0 bad_table_lines=0 headings=1
BINDING l1=0 l2=0 l3=0
SOURCE rev=9bc20ab75c1b8881cd915d0e3eab18bf8387ca3d clean=yes lane_rev_equal=yes
RUN executed=83 timeout=0 mismatched=0 evidence_missing=0 laundered=0
TIPSTATE entry_declared_green=49 entry_declared_red=34 observed_green=49 observed_red=34
MIGRATION redeclared=4 r53_green_nonentry=4
PREDICATE R55-C2 pass
C2_EXIT=0
```

Byte-equivalent in every predicate field to the committed `integrate/c2-after-full.txt`.
Before-state verified from committed bytes + ledger diff: base ledger `8db18e23` declares
63 green / 20 red; head declares 49 / 34; `round54-entrytruth.json` diff shows exactly
**14 green→red flips** (round31-defects, round33-defects, round37-c2…round46-c2 ×10,
round50-c1, round51-routing), each carrying a verbatim measured fragment (old-host
`/home/vgpnk/...` path in round31-defects; `RESOLVE observed_present=11 floor=13` in
round51-surfaces; `V4 … 59/59 (want 42/42)` in round35-c1-coverage;
`POPULATION … mismatched=125` in round50-c1; `hits=860` in stage-scan) plus **2 already-red
fragment refreshes** (round35-c1-coverage, round51-surfaces) and the stage-scan argv
re-declaration — 17 red re-declarations total, matching the report's "seventeen" under that
reading (see V3). `SKILL.md` registry diff: 18 rows rewritten one-to-one = the 17
ARGV-DEFECT cells + round36-c2; ledger argv changed for exactly round-close-check (`--census`),
round36-c2 (`--fleet`), stage-scan, tb2-grader-probe — the two stay-green corrections and two
honest re-declarations the report names. No red→green flip exists. Fixture kills re-run under
the disclosed uv-scoped side-run (uv 0.13.6 installed, then uninstalled): abbreviated-selftest
→ `ARGV-DEFECT`+`ABBREV-DEFECT`, uv-decoy → `ARGV-DEFECT`+`WRAPPER-DEFECT`, both naming
`fixture-gate`, `PREDICATE R55-C2 fail`, counter exit 1, route exit 0; controls selftest 4/4.
No soundness break constructed or observed. **Verdict: improved (9→10) — the calibration move
is re-declaration discipline, not score inflation; the declared 49g/34r equals observed.**

### R56-C3 — coverage, L0-capped — RE-MEASURED + RE-OPENED, predicate met, score held 7

Re-opened both new rows at the pin `2fd12b88aafdd04a52c298e3940bcb189f9766d6` (`curl` GET,
sha256 over fetched bytes):

| file | sha256 (this judge, 2026-11-01) | matches oracle note |
|---|---|---|
| `chess-best-move/task.toml` | `d8f01d3c84ed5836edbb49c6c3b3cc7b5b96d951cf01a0987467c9206fb22f9e` (849 bytes) | YES |
| `chess-best-move/solution/solve.sh` | `53b5c5e2278ca915b0930eedfd44565ca84ef21c7346fd6601434484cf76151f` (7555 bytes) | YES |
| `chess-best-move/tests/test_outputs.py` | `a540714e0156fc14564badedcb48d1f7b69a4b457d876036535439b30cb8f286` | YES (S201 cross-check) |

Quotes re-verified byte-true at their cited locations: `task.toml:6` contains
"analyze a chess position from an image, use a chess engine to find the best move(s), and
handle multiple valid solutions" (21 words ≤ 25); `solve.sh:186` is
`best_moves.append(move.uci())` inside the `:180-189` legal-move loop; `:232` writes
`"\n".join(best_moves)`; grader `:25` is
`assert sorted(move) == sorted(["g2g4", "e2e4"])`. The oracle note's mapping (oracle emits the
complete mating multiset; grader rewards exactly that multiset) reads as correct against the
fetched code. Counting commands re-run at head: `grep -c S203 corpus/SOURCES.md` → 1,
`grep -c S204` → 1, `grep -c thirteenth PROVINCE.md` → 2 (predicate ≥1), oracle note present.
Registry rows 195 (base) → 197 (head), malformed 0. **Verdict: predicate met; score held at 7
by the claim's own L0 design — graded unchanged, honestly declared.**

### Before-receipts (do-nothing controls) — evidence-verified

`claims/c1-before.txt` (instrument absent at base `1355e84c`, exit 2), `claims/c2-before.txt`
(`argv_defect=17 wrapper_defect=1`), `claims/c3-before.txt` (`S203=0 S204=0`) — all committed,
timestamps 2026-10-30 (old host, pre-move), consistent with Amendment A2's ordering.

## 3. Census (re-run)

`bash <fleet>/scripts/sources-census.sh validate --root <fleet> kengaku` → exit 0, verdict
`ok`, the same 15 pre-existing W04 duplicate-url warnings as `integrate/census-end.txt`
(output byte-identical to the committed receipt). Manual battery on committed
`corpus/SOURCES.md` at head: **rows=197 malformed=0 dup_ids=0**, tier A=168 B=24 C=5,
status mined=176 queued=8 rejected=13, no enum violations, all mined `used-by` paths exist.

## 4. Findings, L0, SHONEN spot-checks

- **R56-F1** (r46 `anchor_line_check.py` QUOTE_RE false-positive on S201's escaped-quote
  anchor): diagnosis verified from source — `QUOTE_RE = … "(.*?)"(?=\s*(?:\(\d+\s+words?\)|[;,]|$|\s+and\s))`
  terminates the non-greedy capture at the `\"` before the `,` inside `sorted([\"g2g4\", …`,
  yielding a truncated "quote" that is not a substring of `tests/test_outputs.py:25`, while
  the row's citation is byte-true (re-fetched, sha above). **Agree with route-not-repair:**
  fixing the checker is a gate change that needs its own frozen claim with falsifier fixtures.
- **R56-F2** (measurement-environment scoping): verified *empirically against this judge's own
  first attempts* — a detached-HEAD clone at `9bc20ab7` (with `refs/heads/master` sitting at
  `d834d89d`) laundered exactly the ref-sensitive rows (`defect-ledger`, `round36-c1-battery`),
  and the same counter on a **master checkout** at the same revision reproduces the committed
  green receipt byte-for-byte. The two scoping rules are real and load-bearing.
- **L2 refusal**: the two `kengaku | round-56` L0 lines are committed at fleet HEAD
  (`3853c33f`); the refusal is disclosed in report/lesson/SCORECARD; the frozen instruments'
  falsification machinery (verified above) is the routed-around adversarial coverage. Ruling
  stays with the operator; nothing assumed answered.
- **SHONEN**: all four boxes `[~]` with resolvable pointers, no `[x]` anywhere in `SHONEN.md`.
  Spot-checks: SKILL.md = 1375 lines, 2 `## Decision table` sections, `## Gate/probe registry`
  present; LOG round-56 entry present (lines ~1744+); box 3 is evidenced by this closure itself
  (every frozen instrument ran from committed instructions alone on a fresh session + fresh
  host); PROVINCE round-56 section dated with three absent surfaces marked. All four look fully
  checkable by a non-author — operator may want to run that gate; this judge did not write `[x]`.

## 5. Spot-check table (LEARNING.md discernment — ≥1 admit + ≥1 reject-equivalent)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S203 `task.toml` | admit A (spec) | pinned raw URL re-fetched 2026-11-01, sha256 + `:6` quote verified | **agree** | machine-readable task definition, byte-true quote (21 words), identity pinned; grounds the plural reading |
| S204 `solution/solve.sh` | admit A (code) | pinned raw URL re-fetched, sha256 + `:180/:185/:186/:232` verified | **agree** | maintainer oracle read from code, not inferred; its all-mating-moves behaviour is exactly what the grader's multiset assertion rewards |
| R56-F1 | route, not repair (reject-equivalent: declined to hot-fix a gate mid-round) | `anchor_line_check.py:57` QUOTE_RE vs S201 anchor cell + re-fetched grader bytes | **agree** | the false positive is real and the row is byte-true; an unfrozen gate repair would violate the lane's own freeze discipline; correctly re-declared the riding rows red instead |
| round50-c1 | re-declared red (population pin drift 125/126) | ledger fragment `POPULATION fixtures=126 … mismatched=125`; root cause left open | **agree** | honest red on measured evidence; guessing a root cause would have been the calibration failure |

No new `corpus/SOURCES.md` rejection row this round (both opens admitted; lesson says so) —
the R56-F1 routing decision is sampled as the round's reject-equivalent per the lesson's own
offer.

## 6. Routed defects the lane must fix next round (all status-neutral)

- **R56-V1 (load-bearing).** Lane head `d834d89d` regresses the lane's own registry-closure
  gate: the SCORECARD round-56 section's R56-C1 counting-command cell advertises
  `python3 plans/round56_landcheck.py` (the only such mention in the scanned self-assessment
  files), but `SKILL.md`'s `## Gate/probe registry` holds **no row for the landcheck** (0
  mentions). Re-measured at head: `python3 plans/round52_c2_registry.py --lane <head clone>` →
  `ADVERTISED total=83 / REGISTERED total=82`, `MISSING plans/round56_landcheck.py`,
  `PREDICATE R52-C2 fail`, exit 1; consequently the entry-truth counter at head reports
  `LAUNDERED round52-c2` + `LAUNDERED routed-findings`, `laundered=2`,
  `PREDICATE R55-C2 fail`, exit 1. The canonical measured revision `9bc20ab7` is unaffected
  (the advertisement lands in `d834d89d`'s SCORECARD bytes), which is why every committed
  receipt reproduces — but the pushed branch tip is red on the lane's own gate, and the
  CLOSURE-PREP instruction "re-derive at lane head" cannot reproduce the PASS. Fix: land the
  landcheck's registry row (name, kind, entry command, verdict map, self-test spelling,
  pinned-value path, write scope, owner) in `SKILL.md`, then re-run both counters at tip.
  Until then the head-tip tree contradicts the "registry closure restored" sentence the round
  itself landed.
- **R56-V2.** PROVINCE SF14 row's in-place correction reads "195 rows … incl. S203/S204
  opened this round" — 195 is the BEFORE count; any tree containing S203/S204 counts 197
  (this judge's grep). The report and registry say 195→197 correctly; the PROVINCE row's
  number is stale on arrival. One-line dated correction.
- **R56-V3 (wording only).** "Seventeen honest green→red re-declarations": the ledger shows
  exactly **14** literal green→red state flips; the 17 counts only with the 2 already-red
  fragment refreshes (round35-c1-coverage, round51-surfaces) and stage-scan's argv
  re-declaration. Likewise "sixteen declared-green rows false here" — strictly 14 declared
  green measured false; the 2 EVIDENCE-MISSING rows were declared red at base. The data is
  honest and complete; the labels overcount by 3 (and 2) respectively.
- **R56-V4.** Appending R56-F1/F2 to `corpus/routed-findings.jsonl` re-encoded all 25
  pre-existing rows' JSON escaping (`\u2026` → literal `…`, 25 removed / 27 added lines).
  Semantically identical, but append-only ledger rows were byte-rewritten in place. Keep the
  writer byte-stable over existing rows.
- **Carried:** round50-c1 population-pin root cause (open, named); R56-F1 repair as its own
  frozen claim; the two L0 questions (L2 surface; ledger schema v2 host column).

## 7. Trend + axis verdicts (this judge)

- **expansion: unchanged** — agreed: no new coverage-map ground (the chess task was already
  read in r55; this round added depth — the oracle — and two source rows; no new knowledge
  entry class; one capability). Registry 195→197 is row growth, not new ground.
- **quality: improved** — agreed: the entry ledger states this host's truth and the whole
  landed-evidence set re-verifies from one command (both re-measured here); r54's prerequisite
  demonstrated; three instrument defects named and measured rather than papered over. V1 does
  not retract this: the regression is at the tip, after the measured close, and is itself
  caught by the lane's own machinery — the property quality-improvement claims.
- **discernment: improved** — agreed: 14 measured re-declarations (no laundering), two routed
  findings, the round's own finding-row shape defect caught by its own counter and corrected
  in place, uv-scoping disclosed rather than hidden.

Axis verdicts: operability **improved** (re-measured), calibration **improved** (re-measured),
coverage **unchanged** (score held 7 by L0 design; predicate met), depth/freshness/novelty/
adjacency **unchanged** (SCORECARD diff is append-only; evidence pointers of other axes
untouched; freshness carried the dated PROVINCE re-probes). No axis harmed.

Re-measured by this judge: C1 landcheck + selftest, C2 counter (canonical + head), 3 mutation
kills, 2 fixture kills + controls selftest, census validate + manual battery, S203/S204
re-open, ledger/SKILL/SCORECARD diffs, L-reg at head. Evidence-verified from committed bytes:
before-receipts (old host, pre-freeze), the r55 `cases=18` tb2 receipt
(`.ufo/waves/round-35/build/R35CritControls/package/tb2-grader-probe.txt`), the r55 report's
"unchanged" statement vs `ebb233bc`, L2-refusal disclosure (no dispatch artifact exists to
re-run).
