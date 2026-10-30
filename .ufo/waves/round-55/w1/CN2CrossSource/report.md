# CN2CrossSource — seat report (kengaku round 55, wave 1)

Seat: CN2CrossSource (connector). Assignment: cross-source pattern — the 13 TB2 grader entries
as one dataset; build the class table; place chess-best-move; recommend the fleet-level routing.
Bounds honored: read-only + this wave dir; no subagent dispatch; no mutating git; no sibling files.

## What I ran

1. Read the frozen claims `plans/round-55-claims.md` (commit `80afa613`) — predicates, counters,
   kill rules confirmed before any data work.
2. Read all 13 task-grader knowledge entries in `corpus/knowledge/`: the 12 held (rounds 35–46:
   protein-assembly, regex-log, configure-git-webserver, build-pmars, git-leak-recovery,
   db-wal-recovery, constraints-scheduling, circuit-fibsqrt, feal-differential, feal-linear,
   password-recovery, polyglot-c-py) plus `tb2-chess-best-move-grader.md` (landed 2026-10-30
   12:41). Read pattern: front-matter + Summary + "What the grader checks" + requirement-map
   sections of each (full read for the chess and password entries; sectioned reads for the rest,
   all conclusions cross-checked against receipts).
3. Read both TB2 meta-entries (`tb2-presence-only-triage.md`, `tb2-grader-vacuity-triage.md`),
   `corpus/lessons/round-55.md` (gate/S201/S202/amendment-A1 state), and the wave-1 critic ruling
   `w1/C4ClassNovelty/ruling.md` (multiset-vs-membership novelty).
4. Verified every receipt's case line from committed bytes under `corpus/evidence/`
   (13 `grep -h -m1 -E '^cases='` + regrade lines; all 13 receipts present, counts in the table).
5. Checked fleet sibling scopes for the routing: `tameshi-shokunin/SKILL.md` + `PROVINCE.md`
   (verification-fixture craft; owns the probe method), prior fleet routing precedent for kotoba
   (r11–r14 connectors: prompt/output-contract craft → kotoba).

## Commands and exit codes

- `mkdir -p /fast/scratch/hyaku/kengaku-r55/CN2CrossSource .ufo/waves/round-55/w1/CN2CrossSource` → 0
- `grep -h -m1 -E '^cases=' corpus/evidence/<round>/<probe>.txt` ×13 → 0, all lines captured
- `grep -h -m1 -E '^cases='` re-run anchored `^cases=` ×7 (regrade-first files) → 0
- `ls -d /home/vgpnk/Projects/shokunin/*/` → 0 (sibling census; `tameshi-shokunin` present)
- `head`/`read` on the 13 entries, 2 triage entries, round-55 lesson, C4 ruling, tameshi
  SKILL/PROVINCE → 0
- No installs, no network fetches (all evidence already committed in-repo at the freeze).

## Files written (all under this seat's wave dir)

- `.ufo/waves/round-55/w1/CN2CrossSource/class-table.md` — the 13-row class table
  (task | graded artefact | grader operation | partial credit | receipt cases), cross-row
  structure, chess placement, routing recommendation, observed anomalies.
- `.ufo/waves/round-55/w1/CN2CrossSource/report.md` — this report.
- `.ufo/waves/round-55/w1/CN2CrossSource.md` — scoped findings at the Report-trailer path.

## Findings (summary; full detail in class-table.md)

- **13-row table built.** Operation mix across the dataset: literal ×6 (protein-assembly,
  regex-log, git-webserver, db-wal-recovery, feal-differential, + build-pmars companion legs),
  membership ×2 (feal-linear, password-recovery — the F1 constant-compare family),
  ldd-scan ×1 (build-pmars, class new at r38), chain-compare ×4 (git-leak-recovery,
  constraints-scheduling, circuit-fibsqrt, polyglot-c-py), multiset ×1 (chess-best-move,
  class new at r55). 269 receipt cases total; 12/13 receipts mismatches=0; 12/13 regrade differ=0.
- **Partial credit: uniformly none.** All 13 map pytest exit → single reward bit; per-test
  texture in multi-fn graders collapses to one bit.
- **Chess sits at the strict pole of the constant-compare family**: order-free like r45
  membership but multiplicity-exact and any-whitespace-token; its `extra-decoy-move` F is the
  state r45's `decoys-1000` P measures — the two rules genuinely cross (C4 ruling: NOVEL,
  combinatorially). It is also the simplest grader in the set (one file, one assert, one pair).
- **Routing recommendation: kotoba (primary)** — the fleet-level pattern is the
  instruction-vs-grader gap operationalized as receipt-derived requirement maps (12/13 headline
  cases pass while violating stated requirements; gaps run both directions). Craft rule for the
  referral: every advertised requirement needs a violating test state or it is unenforced.
  Tameshi already owns the probe method; only the class table as fixture-discrimination taxonomy
  is an optional secondary tameshi copy.

## Defects found (reported, not fixed — sibling-owned)

- `corpus/evidence/round41/constraints-probe.txt` carries mismatches=2 (carried r40 pilot
  errors; disclosed in-entry — not an instrument defect, noted for calibration honesty).
- `corpus/evidence/round46/polyglot-c-py-probe.txt` records `regrade differ=7` — same-process
  regrade instability unique in the dataset (all other rows differ=0). Calibration-relevant if
  regrade legs ever gate a predicate.
- `corpus/knowledge/tb2-chess-best-move-grader.md` front-matter still records
  `second-seat re-read: pending (R3)`; Q13/Q14 admission re-read outstanding at read time.

## Dead ends / not done

- No live clone was needed: the assignment is cross-source reading of committed entries and
  receipts; all evidence was already committed at the freeze. Scratch dir
  `/fast/scratch/hyaku/kengaku-r55/CN2CrossSource/` was created per contract and deleted unused.
- The two TB2 triage meta-entries were read for context but are population-level instruments,
  not task grader entries, so they sit outside the 13-row dataset (noted, not conflated).
- No upstream re-fetch this seat (network budget); chess byte-identity was already
  receipt-verified by sibling seats (`E14CaptureIdentity`, claims receipt).
