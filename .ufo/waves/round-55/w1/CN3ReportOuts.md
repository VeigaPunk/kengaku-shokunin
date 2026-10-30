# CN3ReportOuts — scoped findings (kengaku round 55, w1)

Deliverable: `.ufo/waves/round-55/w1/CN3ReportOuts/routing.md` (full routing lines; this file
is the report-forward). Read-only seat; no lane file touched; no installs; no network.

## 1. Standing L0 caps — verified unanswered in `.ufo/l0-questions.md` (quotes in routing.md §1)

Ledger answer-scan: `grep -n "L0 ANSWER|ANSWER"` matches only kama-r11, tsukuroi-r12 and one
dated general answer — no kengaku row is answered.

- `kengaku | round-25` (line 72, coverage cap): > "...does a surface explicitly retired to
  PROVINCE.md §Historical ... still count as 'declared-but-unresolvable' for the coverage
  rubric cap? Until ruled, kengaku coverage stays capped at 7." → operator/integrator. UNANSWERED.
- `kengaku | round-25` (line 73, novelty conversion): > "Should verdict-only rounds be
  converted retroactively (and by whom)..." → operator/integrator. UNANSWERED.
- `kengaku | round-33` (line 163): > "what committed evidence lifts the round-25 L0 coverage
  cap... (d) the cap stays until the absent surfaces return." → operator/integrator. UNANSWERED.
- `kengaku | round-51` (line 200): > "three surfaces PROVINCE.md declared as resolving are
  absent ... Restore them, or retire them from the lane province?" → operator/integrator.
  UNANSWERED.
- `kengaku | round-52` (line 203, GH013): > "May the operator authorize GitHub's push-protection
  exception, or provide an approved history-cleaning/helper path...?" → operator. UNANSWERED;
  round-55 routes around it (in-repo pinned capture only, per the freeze).
- `kengaku | round-54` (lines 213–214, assimilation): > "...please rule whether the package
  should be re-staged against the current registry or retired." (corrected: registry rows=190,
  staged rows=175, collisions=114) → operator/integrator. UNANSWERED; freeze records
  Assimilation: none this round.

Effect: R55-C3 coverage score stays capped at 7; predicate is the counter, never the number.

## 2. Serving-plane status (not probed; standing refusal quoted)

Owner: kama + operator/integrator; kengaku refuses the surface
(`PROVINCE.md:25-26` "the model-serving plane ... no lane owns it; escalate to the integrator
instead of remediating"; `:137` kama owns serving-plane health/endpoint identity). Standing
state per unanswered L0 `kama | round-1` (2026-10-15): "8080 and 34113 refuse,
qwen-coder.service is LoadState=not-found"; kengaku §Historical (`PROVINCE.md:157`) records
:34113 "no listener" at the r13 re-dispatch. No endpoint was probed by this seat; the round
needs nothing from the plane.

## 3. Wave findings routed to another lane (named + owner)

- `/tmp` sibling-lane round-55 artifacts outside scratch roots (E12ScratchHygiene §4):
  tameshi (`census-r55*.txt`, `r55ctx.txt`, `closure-r55-tameshi.json`), mado
  (`closure-mado-r55.json`, `r55chk.py`, `r55entry.md`), kama (`kama-r55-*`) → owning lanes
  tameshi / mado / kama; recorded, not policed.
- Assignment freeze-text scope defect (R9 routed defect 1: literal frozen command returns 15
  hits, not 0) → L1/integrator.
- `plans/round55_c3_chess_probe.py` untracked at the freeze tip (E6 defect) → L1/integrator
  landing commit.
- `PROVINCE.md:557` "8 of 89 read" vs README "12 of 89 read" (R9 routed defect 3) → kengaku
  PROVINCE owner (in-lane route-out).

Verification and full command log: `.ufo/waves/round-55/w1/CN3ReportOuts/report.md`.
