# R50C2ScribeCorrections — prose half of the C2 corrections block (scribe, R50-C2)

Seat: `R50C2ScribeCorrections` · claim served: **R50-C2 (calibration 8→9)**, pointer audit · lane
`/home/vgpnk/Projects/shokunin/kengaku-shokunin` · wave `.ufo/waves/round-50/w1` · read-only seat (no lane edit,
no commit, no push).

REV c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 (lane tip at measurement, branch `master`; clone
`/fast/scratch/hyaku/kengaku-r50/R50C2ScribeCorrections/lane` via `git clone --shared`, toplevel verified equal to
the clone dir). Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` verified an ancestor of that tip
(`git merge-base --is-ancestor` → `ANCESTOR_OK`) before any measurement; base lane tip `71f5f5f7…` also verified an
ancestor.

## Axes named

- **calibration** — the rubric's own condition (c): the self-assessment files exist and every row's pointer re-runs.
  This item supplies the explanatory prose for the corrections that make that condition true; it measures nothing
  new about the fence (novelty/coverage untouched, not claimed here).

## Deliverable — prose half, ≤25 lines (for the L1 to append inside `SCORECARD.md` §`## Round 50 — C2 corrections`, after the 12 `SUPERSEDED` rows)

Transcribed verbatim, 23 lines, ready to paste; every claim in it is backed by an evidence line in §Evidence below.

```markdown
**What they were.** `plans/round48_c1_verify.py` and `plans/round49_c1_verify.py` are one contract twice: the round-46
fence counter (`plans/round46_c1_verify.py`, digest-pinned import) plus a stage-2-frozen honest population (104 battery
fixtures + 9 r46 / 16 r48 novel classes, wave-1 classes folded into `<H>` at stage 2), a BENIGN-ADMIT rule
(`touches=0` admissions counted apart, never a leak) and Q39 name-hiding. `plans/round48_c2_verify.py` and
`plans/round49_c2_verify.py` are the package counter (`plans/round46_c3_verify.py`) plus the V7 positive precondition
(every frozen tag cited by a committed case `violates=`, violating cases for `both-print` and `toolchain`), the V8
pre-receipt controls and the V14/V15 legs; r49 also moved the dry case table into the probe at stage 2 and the receipt
to `corpus/evidence/round49/polyglot-c-py-probe.txt` at stage 3 (`plans/round-48-claims.md:46,92`;
`plans/round-49-claims.md:52,108`).
**Why the rows cited them anyway.** A row's "counting command" cell is the frozen route by which a reader re-derives
its number, so it is written before the data: both rounds named a file "written in wave 1, pinned at stage 2". Rounds
48 and 49 each closed as an honest stop before that stage, so the cell outlived the promise — SCORECARD:2104/2105 cite
the r48 paths after "no committed stage-2 landing-tip run", SCORECARD:2119/2120 cite the r49 paths "is not present at
landing". The citation was an unretired promise, not a false measurement, and it left those four rows un-rerunnable at
the tip for two rounds. `corpus/lessons/round-49.md` records it from the owning round: "The committed MUTANTS floor and
C1 stage-2 counter were not landed"; "Neither the amended probe, counter, entry map, spec, mutation battery, stage-2
controls nor stage-3 receipt was integrated or scored."
**What the correction discipline now requires.** An unresolved pointer is a routed finding with an id, a status and the
closing commit, appended and never a rewrite of the row that carried it (Q41, `corpus/QUALITY.md:1112`).
`SUPERSEDED <pointer> -> <target>` only when the target exists at the tip; `SUPERSEDED <pointer> -> never-landed` only
when `git log --all --oneline -- <pointer>` is empty — true for all four (0 lines each, measured at `c3372a9b`). The gate
is `python3 plans/round50_c2_audit.py --lane .`: `POINTERS … unresolved=0`, exit 0, before the row lands; `--selftest`
shows the check can fail; and the counter a row names exists at the tip before the row lands.
```

## Exact commands run (against the clone at REV `c3372a9b`, never the live checkout)

```
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane
git -C $S/lane rev-parse HEAD && git -C $S/lane rev-parse --show-toplevel
git -C $S/lane merge-base --is-ancestor 3b02d573d58cc6d2e0d27ef92ac0815354912252 HEAD
grep -c '^SUPERSEDED ' SCORECARD.md
python3 plans/round50_c2_audit.py --lane .
git -C $S/lane rev-parse --abbrev-ref origin/HEAD
```

Lane-side read-only provenance commands (no writes; `git log` is read-only):

```
git -C <lane> log --all --oneline -- plans/round48_c1_verify.py     # and round48_c2_verify.py,
                                                                    # round49_c1_verify.py, round49_c2_verify.py
git -C <lane> log --all --oneline -- plans/round34_c1_verify.py     # and round34_defects.py, round34_mutate.py
```

## Evidence (verbatim)

Audit at REV `c3372a9b`, 12 correction rows already committed (block at `SCORECARD.md:2136`):

```
TIP c3372a9b24d3a200946a6b37dc0a31ed5c982cc1 branch=master
POINTERS total=277 paths=218 hashes=59 resolved=277 exists=206 superseded=3 never-landed=9 unresolved=0
exit=0
origin/master
```

`12` = `grep -c '^SUPERSEDED '` → `12`; 3 rows re-point to an existing target, 9 are `never-landed`, and
`3 + 9 = 12` are exactly the `resolved → superseded=3 / never-landed=9` split the audit prints. The four counters of
this item are inside the nine.

Never-landed check (`git log --all --oneline -- <path>` line counts at the lane):

```
plans/round48_c1_verify.py  0
plans/round48_c2_verify.py  0
plans/round49_c1_verify.py  0
plans/round49_c2_verify.py  0
plans/round34_c1_verify.py  0
plans/round34_defects.py    0
plans/round34_mutate.py     0
```

Nothing the r49 counters would have produced exists either (clone at tip):

```
ls: cannot access 'corpus/evidence/round49/': No such file or directory
ls: cannot access 'plans/honest49': No such file or directory
```

The contract bases they were to extend do exist, so the absence is the counters, not their input:

```
-rwxr-xr-x 1 vgpnk vgpnk 36066 Oct 28 14:38 plans/round46_c1_verify.py
-rwxr-xr-x 1 vgpnk vgpnk 44042 Oct 28 14:38 plans/round46_c3_verify.py
```

What each was (from the claims files, not from memory):
`plans/round-48-claims.md:46` — counter = `plans/round46_c1_verify.py` digest-pinned + stage-2 honest population (104
battery + 9 r46 novel + wave-1 classes) + BENIGN-ADMIT + envelope legs; `:92` — `plans/round46_c3_verify.py` + V7
positive precondition + V8 pre-receipt controls + V15 + V14 mutation leg.
`plans/round-49-claims.md:52` — 104 battery + the 16 r48 novel classes under `plans/honest49/` + wave-1 classes,
BENIGN-ADMIT, Q39 name-hiding; `:108` — the V7 fix, case table amended in the probe at stage 2, dry table
`corpus/evidence/round49/polyglot-c-py-dry-cases.txt`, receipt `corpus/evidence/round49/polyglot-c-py-probe.txt` at
stage 3. Both files open the counter cell with "(written in wave 1, pinned at stage 2)".

Why the rows carried the path (verbatim row cells): `SCORECARD.md:2104` "Frozen command:
`python3 plans/round48_c1_verify.py --lane .`" with "No committed stage-2 landing-tip run"; `:2105` same shape;
`:2119` "frozen command `python3 plans/round49_c1_verify.py --lane .` is not present at landing"; `:2120`
"`python3 plans/round49_c2_verify.py --lane .` is not present at landing". The r49 rows stated the absence
themselves — the defect is that the pointer stayed, not that the round lied.

Round-49 lesson cited (`corpus/lessons/round-49.md:18-19`): "The committed MUTANTS floor and C1 stage-2 counter were
not landed. No axis move admitted." / "Neither the amended probe, counter, entry map, spec, mutation battery, stage-2
controls nor stage-3 receipt was integrated or scored." The round-50 lesson (`corpus/lessons/round-50.md`) already
mines the same fact as a `landing` mistake row and names Q41 plus the audit as the fix; this prose is the long form
that block points at.

Q41 text measured at `corpus/QUALITY.md:1112` ("every `plans/…` or `corpus/…` artifact path and every 40-hex hash
named in `SCORECARD.md`, `SHONEN.md` or `PROVINCE.md` resolves at the tip; a pointer that does not resolve is a routed
finding carrying an id, a status (`closed` … `never-landed` …) and the commit that added the correction — appended,
never a rewrite of the row that carried it"), with the executable check and the `unresolved=12` at `71f5f5f` / `0`
after corrections.

## Findings for the integrator (L1)

1. The block's existing one-line summary of this same fact is imprecise and should be superseded by the prose above:
   `SCORECARD.md:2165-2166` says "The four `plans/round34_*` and four `plans/round48_*`/`round49_*` counters", but
   `plans/round34_*` is **three** paths (`round34_c1_verify.py`, `round34_defects.py`, `round34_mutate.py` — the last
   two are not counters) and the r48/r49 quartet is the four counted here. Suggested minimal fix: replace that clause
   with the prose block; the 12 `SUPERSEDED` rows themselves are correct and measured (`unresolved=0`).
2. `round34_c1_verify.py` is the same mistake one round-class earlier (a `Frozen command:` cell at `SCORECARD:1168`
   for a file no commit held, 0 history lines). It is `never-landed` in the block, so the count in prose should stay
   "four" for r48–r49 and treat the round-34 trio as the same class, not as four more counters.
3. `plans/round50_c2_audit.py` builds the `SUPERSEDED` map from the **whole** of `SCORECARD.md`
   (`superseded_map` = `SUPERSEDED = re.compile(r"^\s*SUPERSEDED\s+(\S+)\s+->\s+(\S+)\s*$", re.M)` over the file
   text), not from the round-50 block alone, and a later row silently overwrites an earlier one for the same pointer.
   Consequence for landing this prose: a `SUPERSEDED`-shaped line at the start of a line anywhere in `SCORECARD.md`
   becomes a live correction, so new rows belong inside §Round 50 and nowhere else.

## Limits

- Read-only seat: no lane file, no `SCORECARD.md`, no `corpus/*` edit; the prose is delivered here for the L1 to
  land. Nothing in this report admits R50-C1 or R50-C2; the audit's `unresolved=0` at `c3372a9b` is a measurement of
  the tree as committed, not an admission.
- The audit's surface is three files and two prefixes only; a pointer written as a bare filename, a non-listed
  extension, or a path under another prefix is invisible to it, so `unresolved=0` is not "every pointer in the lane
  resolves".
- The clone is `--shared` at one revision; the lane working tree carried uncommitted C1 edits at measurement time
  (`plans/fixture_fence.py`, `plans/round50_c1_verify.py`, `plans/mutants50/c1-mutants.json`, `corpus/QUALITY.md`).
  None of them is in the audit surface or in the pointers cited here; the audit was run from the clone, so the
  numbers belong to `c3372a9b` exactly.
- No git/jj mutation, no commit, no push, no tool install (none needed). Scratch
  `/fast/scratch/hyaku/kengaku-r50/R50C2ScribeCorrections` removed before yield (verified absent:
  `SCRATCH_REMOVED`).
- Revision note: the lane tip advanced to `d6f2fce9889f429162c12f851bae41891bedf5cd` (L1 commits landing
  concurrently) between my measurement and report close. Every number in this report belongs to the measured REV
  `c3372a9b24d3a200946a6b37dc0a31ed5c982cc1`; nothing here is asserted about `d6f2fce9`. The L1 should re-run the
  audit there before scoring, which is the C2 predicate's own requirement.

VERDICT: prose half delivered (23 lines, ≤25), grounded line by line in the claims files, the SCORECARD row cells,
the round-49 lesson, Q41 and the measured audit; no lane edit; no calibration move claimed.
