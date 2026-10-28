# C1CritRoundShape — round-contract critic, kengaku round 52, wave 1 (2026-10-28)

Seat role: critic (leaf, no subagent dispatch). Attacked the ROUND CONTRACT
(`/home/vgpnk/Projects/shokunin/.ufo/prompts/kengaku-round-52.md` §1–§5) against what this
round will land — not the code. Method: read the frozen claims (`plans/round-52-claims.md`
in full, including both amendments), both frozen counters byte-exact, AXES.md §stagnation
nudge, `.ufo/l0-questions.md`, SCORECARD/LOG round history (r48–r51), the round-51 report
precedent, and re-ran both counters read-only on the live tree. All numbers below are
measured today unless marked otherwise.

## Per-item verdicts

### (a) Lowest-axis obligation — CONFORMANT, with one named tension the report must carry

- Coverage 7 is the lowest non-retired axis; it is not claimed. The waiver does **not** rest
  on the stagnation nudge: `AXES.md:66-73` waives only when *every* owned axis sits at/above
  the saturation line, false here (7 < 8). The claims file says exactly this
  (`plans/round-52-claims.md` §Axis choice: "Stagnation nudge: **not** invoked") — the
  tension is disclosed, not hidden. The substantive waiver is the L0 cap: coverage's rubric
  cap is the direct subject of open L0 questions, verified still open today, unanswered, in
  `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`:
  - `kengaku | round-25` (coverage cap: does a retired surface count as declared-but-unresolvable?) — line 72;
  - `kengaku | round-25` (novelty verdict conversion) — line 73;
  - `kengaku | round-33` (what committed evidence lifts the cap) — line 163;
  - `kengaku | round-51` (three ABSENT surfaces: restore or retire) — line 200.
  None carries an inline `— L0 ANSWER` marker (unlike, e.g., kama|round-11). §6 run-10
  ("route around open L0 questions, never treat them as answered") makes a coverage claim
  unreachable this round; working the 8-band follows r50/r51 precedent, and r51's identical
  routing was non-author spot-checked and admitted (lane commit `30801b4`).
- **Smallest correction:** the round report must state this reasoning verbatim (the claims
  file already commits to "says so in the report"). Optionally an L0 line asking whether an
  L0-capped lowest axis suspends the §2 obligation — the gap is rule-vs-practice, not a
  hidden regression. Verdict: conformant.

### (b) Frontier step §2b — CONFORMANT as designated; landing pending (L1 owes the files)

- Sourced claim: C1 is designated, and the basis exists — SOURCES rows S105–S107 carry URL +
  access date + located-quote anchors at the exact pin `2fd12b88…`
  (`corpus/knowledge/tb2-protein-assembly-grader.md:1-3`); new rows are owed only for sources
  opened this round (prior-art primaries), matching claims §Frontier step.
- Mined mistake: `corpus/lessons/round-52.md` does **not exist yet** (glob: absent). The
  material is abundant and real: two frozen-counter implementation defects (capture-leg unit
  error; prose-regex read-set) found by two independent seats pre-after-run and fixed by
  Amendment A2 (commit `de616d7`), plus the A1-receipt figure errors below. The lesson's
  `## Mistakes` + a fix-shown-able-to-fail are owed.
- Census: command in the claims matches §2b's frozen text byte-for-byte; start/end receipts
  with exit codes are owed in the report (end must exit 0).
- Verdict: contract-conformant; not yet executed. See missing-items list.

### (c) Report sections — CONFORMANT mechanism; nothing filed yet (expected mid-wave)

- Report path per §4: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/kengaku.md`
  (fleet repo) — absent today (dir holds only other lanes' reports), correct for a build
  wave in flight.
- The six required sections (Work performed / Landed changes / Before → after measurements /
  Sources & frontier / Trend verdicts / SHONEN, in order) are all present in the r51
  precedent report at headings `:22, :68, :81, :126, :147, :162`
  (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-51/kengaku.md`) — the L1's section
  machinery is proven; kengaku has a `corpus/`, so the report must carry real census
  before→after numbers, not the `SOURCES: unchanged` line.
- Owed in the r52 report on top of the six: A1 + A2 amendment disclosures, wave shape +
  planner-seat mapping (§Wave shape), the D2 append-only LOG correction (63-vs-64 seats),
  and the per-seat wave fidelity statement.

### (d) Re-scoring of an already-held rule — NO. Both claims are first-of-kind instruments

- R52-C1: the lane's prior TB2 engagement is 12 single-task hand-reads (verified: exactly 12
  `corpus/knowledge/tb2-*.md` files) and r35's single-task `plans/tb2_grader_probe.py`
  (18-case probe of one grader). LOG greps for prior population/vacuity instruments over TB2
  return nothing (r26 `grader_perturb.py` population1964 is the lane's own bench-arena
  fixture population — different corpus, different instrument). A whole-benchmark manifest +
  classifier + second-reader + prior-art pricing is a new capability, and the score rule is
  honest: novelty holds at 8 unless a confirmed finding prices phenomenon-new
  (`plans/round-52-claims.md` §Score rule).
- R52-C2: first measurement of the registry-vs-advertised gap. I reproduced the frozen before
  state exactly on the live tree: `ADVERTISED total=72 / REGISTERED total=44 rows=46 /
  MISSING 28 / INCOMPLETE 0 / ENTRY-MISSING 0 / SELFTEST-UNBACKED 1 (order-check)`,
  predicate fail, exit 1 — matching the frozen block. It completes r51 routed defect D1
  under the fleet §Gate standard; it does not re-measure a held capability.
- Causal separability holds as frozen: C1's counter reads captures/receipts only; C2's reads
  self-assessment files + the SKILL.md registry only (verified in code).

## Findings (counterexamples, evidence, smallest corrections)

**F-A — BLOCKING TRAP at C2 landing: the round's own bookkeeping feeds the ADVERTISED set.**
`round52_c2_registry.py` extracts advertised commands from `SCORECARD.md`, `SKILL.md`,
`LOG.md`, `corpus/README.md`, `corpus/knowledge/*.md`. Today MISSING=28 does not include the
two round-52 counters because no self-assessment file names them yet. The moment the L1
lands SCORECARD rows / the LOG entry carrying `python3 plans/round52_c1_grader_audit.py` and
`python3 plans/round52_c2_registry.py` (§2.4 requires exactly that), both become advertised
and MISSING grows to 30 → the scored C2 after-run fails unless registry rows for both land
too. Smallest correction: add the two registry rows as part of the C2 landing and run the
scored after-run strictly **after** the SCORECARD/LOG updates (r51's clean-clone receipt
procedure).

**F-B — frozen control signature `c1-control-drop-capture → present=183 mismatched=1` is
half-unreachable under every counter version (incl. A2).** In the A2 counter, `mismatched`
increments only for present files with a wrong/missing digest; removing a file yields
`present=183 mismatched=0`. The control still fails the predicate (183 ≠ 184), so the
kill-proof works; the documented signature does not. Smallest correction: control receipt
records the measured signature; append-only erratum line to claims §Controls (or redefine
the mutation as byte-corruption, which yields `present=184 mismatched=1`).

**F-C — frozen control `c1-control-blind-class` ("force every task to V0") cannot reach
`CANDIDATES total=0` under A1/A2.** Candidate = `bool(p1) or cls in ("V1","V4")`
(`round52_c1_grader_audit.py`, `collect()`): forcing only `class` leaves CANDIDATES=29. The
control must zero the per-test flags as well. Frozen wording predates A1. Smallest
correction: the control fixture clears both; note the delta in the lesson.

**F-D — A1 disclosure receipt carries two non-reproducible figures (false provenance in a
receipt, already independently measured by `C1ExecClassifier` §F4 and re-confirmed by my
live run).** Receipt says 54 presence-only tests / 42 tasks; the committed instrument
measures `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27` (my run today, same
figures as the seat's). Receipt lists `pytorch-model-recovery/tests/test_outputs.py` at
9249 B; the pinned file is 5591 B (9249 B is `adaptive-rejection-sampler`'s). A2 did not
correct these. Smallest correction: append-only erratum on `.ufo/waves/round-52/claims/a1-observation.txt`
+ a one-line note in claims §A1 §Disclosure; wave 2 must reconcile (the claims already order
wave 2 to attack A1).

**F-E — receipt hygiene: `claims/c1-after.txt` and `claims/c2-after.txt` exist now while
both predicates still fail** (my runs: C1 fail on CONFIRMED=0/PRIOR-ART=0; C2 fail
MISSING=28). If these are pre-landing snapshots they must not be cited as the scored
after-run; regenerate both at the landing tip in a clean clone (r51 procedure) after all
evidence and the SCORECARD/LOG updates land. (Also observed: `c1-after-a2-pre.txt`,
`c2_before_probe.py` — probe work-files; fine, but keep them clearly named.)

**Verified sound (attacked, held):**
- A1/A2 amendment governance: both appended append-only, pre-after-run, disclosed with
  receipt; A1 loosens nothing (CONFIRMED ≥2 kept against a 29-wide pool; two new hardening
  checks); A2 fixes only implementation defects and was driven by two independent seats.
  Both are legitimate under PROTOCOL's "a change after scoring is a new round" (nothing has
  scored). A2 verified live: `CAPTURES expected=184 present=184 mismatched=0` with the
  landed captures; `lane_read_tasks()` returns exactly the 12 real hand-read ids
  (git-webserver → configure-git-webserver mapping correct); `capture_population` = 184
  unique paths.
- C2 advertised-universe rules match the frozen text (depth-1 `plans/*.py`,
  `corpus/evidence/<dir>/<name>.py`, `grader.py`; knowledge glob present — my initial
  suspicion that `corpus/knowledge/*.md` was omitted is withdrawn; it is appended in
  `self_assessment_files()`).
- Digest leg is no longer silently vacuous: a present capture with no SHA256SUMS entry now
  counts as mismatched, and `./`-prefixed keys are normalized.
- C1 leg reachability measured (C1ExecCounterRun R4 + my run): legs 2/3/4/5 all reachable;
  only the still-missing evidence files block.
- `db-wal-recovery` and `password-recovery` sit in both the read-set and the candidate list —
  the read-set guard correctly forces their confirmations to be rejected as not-new; the
  frozen novelty restriction is now genuinely enforced.

## Missing items the L1 must still produce

1. `corpus/evidence/round52/confirmations.json` — ≥2 never-read vacuity candidates with
   named second reader + verbatim quote (enforced against captured bytes).
2. `corpus/evidence/round52/prior-art.md` — ≥3 fetched primary URLs; per-finding
   phenomenon-new/known verdict (this decides novelty 9 vs held-at-8).
3. `corpus/evidence/round52/labels.json` + the reported agreement figure (state clearly it
   is file-level V-class agreement while CONFIRMED is per-test).
4. All eight control receipts under `.ufo/waves/round-52/claims/` (`c1-control-{nothing,
   name-only,blind-class,drop-capture}`, `c2-control-{nothing,empty-cells,drop-row,false-selftest}`),
   with measured signatures (see F-B/F-C).
5. C2 landing: 28 registry rows (8 non-empty cells each) + fix the `order-check` selftest
   cell + registry rows for both round-52 counters (F-A) + re-run after SCORECARD/LOG.
6. `corpus/lessons/round-52.md` — `## Mistakes` (mine F1/F2/F5 counter defects + F-D receipt
   figures; fix shown able to fail), `## Gate` with S-row quotes, D3's five frozen-predicate
   survivors, D4's SF01 `vacuous` class.
7. SOURCES.md updates (opened-this-round rows only) + census start/end receipts, end exit 0.
8. D2 append-only LOG correction line (63-of-64 vs 64 settled).
9. SCORECARD rows (novelty per score rule; operability per kill rule) + LOG round-52 entry +
   capability-table rows.
10. Regenerated scored after-run receipts at the landing tip, clean clone (F-E).
11. A1 receipt erratum (F-D).
12. Wave 2 dispatch (32 falsify seats) with the claims-mandated A1/A2 attack duties.
13. Round report at the §4 path with all six sections + amendment/wave disclosures; then
    commit `round-52` via jj-lane.sh and push per §5.

## Commands I ran (read-only outside my own scratch)

- `ls corpus/knowledge/tb2-*.md | wc -l` → 12 (and listed them).
- `python3 -c` census of `plans/round52-tasks.json`: `capture_file_count=184`,
  `capture_population` unique paths = 184, `grader_files=356` (support files incl. `.scm`
  fixtures account for the delta), every task has ≥1 `test_outputs.py`, files matching
  {test.sh, test_outputs.py, verify.sh} = 184 — the frozen 184 is internally consistent.
- `python3 plans/round52_c2_registry.py --lane .` → before-state reproduced exactly
  (72/44/28/0/0/1, exit 1).
- `python3 plans/round52_c1_grader_audit.py --lane .` → `TASKS 89/89/89`,
  `CAPTURES expected=184 present=184 mismatched=0`, `CLASS V1=2 V4=0 V2=53 V3=32 V0=2`,
  `TESTCLASS presence_only_tests=33 tasks_with_presence_only=27`, `CANDIDATES total=29`,
  `CONFIRMED new=0`, `PRIOR-ART ok=False urls=0`, `LABELS agree=0 of 0`, exit 1.
- `git log --oneline -8` (de616d7 → 30801b4 …), `git status --porcelain` (tracked clean).
- Import-probe of the committed counter: `lane_read_tasks()` → exactly the 12 real ids.
- Grep of `.ufo/l0-questions.md`, `AXES.md`, claims file, SKILL.md registry heading (`:560`).

## Tooling record

No tool installed or upgraded (stdlib Python 3.14.8, git, curl sufficed). No pacman
transaction attempted. Scratch hygiene note: `/fast/scratch/hyaku/kengaku-r52/C1CritRoundShape/`
used as TMPDIR/cwd and removed before yield; my import-probe had auto-written a bytecode
cache into `plans/__pycache__/` — I removed that directory (its other entries were
regenerable untracked caches left by earlier seat probes; `git status` confirms the tracked
tree is clean).
