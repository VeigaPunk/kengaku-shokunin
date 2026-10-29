# W2ScoutLaneReadSet — lane_read_tasks() read-set verification (R52-C1, CONFIRMED-leg novelty gate)

Date 2026-10-28 · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · read-only seat (no lane-tree or counter edits, no installs, no pacman).

## What I attacked

The post-A2 `lane_read_tasks()` in `plans/round52_c1_grader_audit.py:231-238` decides which of the
89 frozen tasks count as "read by this lane before this round" and are therefore **excluded** from
the CONFIRMED leg. The attack: find a task the lane hand-read (documented in
`corpus/knowledge/tb2-*-grader.md`) whose true task id the filename-stem derivation **misses** —
that task would stay classified as NEW, and a confirmation on it would claim novelty twice.
Secondary checks: derived ids outside the population, alias correctness
(`git-webserver` → `configure-git-webserver`), and any hand-read TB2 grader living outside the
12 conforming filenames.

## Method — exact commands

1. Hand-read all 12 `corpus/knowledge/tb2-*-grader.md` files (H1, `source:` pins, summary;
   task-id identification rests on the H1 `read and executed: \`<id>\`` line and the pinned
   raw.githubusercontent URLs, both in the first 300 lines of every entry).
2. Read the counter: lines 1-64 (regexes), 90-233 (`classify*`, `collect`, `lane_read_tasks`),
   219-345 (`verdict`, the sole consumer at :293/:298), 346-429 (printing, A5 block, `main`).
3. Mechanical run (scratch only, counter imported **unmodified**):
   `importlib.util.spec_from_file_location('c1', '<lane>/plans/round52_c1_grader_audit.py')`;
   `c1.lane_read_tasks(Path(lane))`; population ids from `plans/round52-tasks.json` (`tasks` keys);
   per-file H1 extraction `^# .*read and executed: \`([^`]+)\``; sweep of all `corpus/knowledge/*.md`
   for `harbor-framework/terminal-bench-2/<40-hex>/<task>/(tests|environment)/` URLs minus the 12.

## Measured numbers

| quantity | value |
|---|---|
| files matching `tb2-*-grader.md` | **12** |
| derived set size (`lane_read_tasks`) | **12** |
| population task ids | **89** |
| derived ∩ population (recovered) | **12 of 12** |
| hand-read true ids missed by the derivation | **0** |
| derived ids not in the population | **0** |
| H1 id vs derived-id mismatches | **0** (incl. `configure-git-webserver`: H1 + S111-S113 pin URLs all name `configure-git-webserver`, so the hardcoded alias is faithful) |
| pinned grader URLs naming another population task in any knowledge file | **0** (no 13th hand-read under a different filename) |

## Recovered set (all 12, exact)

`build-pmars`, `circuit-fibsqrt`, `configure-git-webserver`, `constraints-scheduling`,
`db-wal-recovery`, `feal-differential-cryptanalysis`, `feal-linear-cryptanalysis`,
`git-leak-recovery`, `password-recovery`, `polyglot-c-py`, `protein-assembly`, `regex-log`.

## Missed set

**Empty.** With the tree as committed, no hand-read task is treated as new; the double-novelty
path through `lane_read_tasks()` does not exist. Round mapping corroborates: r35 protein-assembly,
r36 regex-log, r37 configure-git-webserver, r38 build-pmars, r39 git-leak-recovery, r40
db-wal-recovery, r41 constraints-scheduling, r42 circuit-fibsqrt, r43 feal-differential,
r44 feal-linear, r45 password-recovery, r46 polyglot-c-py — 12 entries, one per round, each
documenting exactly one task.

## Verdict: attack FAILED to land (fix A2 verified correct on current tree)

## Residual risks and the fix I propose (counter NOT edited, per scope)

1. **Working-tree dependency (same-round landing trap).** The set is globbed from the live
   `corpus/knowledge/` at counter run time. If the round-52 landing adds a new
   `tb2-<task>-grader.md` entry (this lane's pattern is one TB2 entry per round), the counter will
   classify a **this-round** read as pre-round and reject the round's own confirmation with
   `not-a-new-task` — fail-closed, but could kill CONFIRMED for a reason unrelated to truth.
   Latent today (exactly 12 files exist); real if the landing writes a 13th entry.
2. **No freeze binding.** Nothing ties the read set to the freeze commit `30801b47`; any
   post-freeze addition to `corpus/knowledge/` silently changes the CONFIRMED leg's input.
3. **Silent alias.** The single hardcoded alias is correct today but a stale alias or a typo'd
   filename would silently yield an id outside the population (harmless) or — the dangerous
   direction — a valid id of a task never hand-read, inflating novelty by hiding a candidate.
4. **Set invisibility.** `verdict()` never prints the derived read set; `REJECTED …
   not-a-new-task` lines appear only for confirmations actually submitted, so the exclusion
   input is not auditable from counter output alone.

**Proposed fix.** (a) Derive the filename list from the freeze commit
(`git ls-tree --name-only <freeze> -- corpus/knowledge`, freeze sha stored in
`plans/round52-tasks.json` or passed as `--freeze`), not the working tree — kills 1 and 2.
(b) Validate every derived id against `pop["tasks"]`/`capture_population` and exit 2 on any
non-member — kills 3's silent paths. (c) Prefer the entry's own H1 task id (all 12 carry it),
fall back to the stem, and error on stem/H1 mismatch instead of silently trusting either.
(d) Print `LANE-READ n=12 <ids>` in `verdict()` so the CONFIRMED exclusion is visible.

## Files produced

- `/fast/scratch/hyaku/kengaku-r52/w2-W2ScoutLaneReadSet/lane-read-set.json` (measurement receipt; copy kept at `.ufo/waves/round-52/w2/W2ScoutLaneReadSet/lane-read-set.json`)
- this report at `.ufo/waves/round-52/w2/W2ScoutLaneReadSet/report.md`, duplicated verbatim at `.ufo/waves/round-52/w2/W2ScoutLaneReadSet.md` (the seat item's named path)

Scratch dir removed before yield. No `git`/`jj` mutations anywhere; lane tree untouched except my own wave-report paths.
