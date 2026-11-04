# ScoutFrontierR76 — per-surface reconnaissance before integration (round 76, w1)

Read-only seat. No production file edited, no git/jj mutation, no tool installed (nothing was
missing), no scratch tree needed (no clone; nothing written outside this wave dir), fleet repo
untouched. The claims file was read at its **freeze** version (`42fad48`, before Amendments A1/A2).

Observation window: 2026-11-04 01:51 → 01:59 BRT. The lane tip advanced five times inside it
(`fda63968` 01:46 → `42fad48` 01:54 → `6977019b` 01:57 → `f0d52322` 01:58 → `d76db01c` 01:59 →
`218a277b` 01:59), so every number below is stamped with the tip it was read at.

## What I ran (exact commands, exit codes)

| # | Command (cwd = lane) | rc | note |
|---|---|---|---|
| 1 | `python3 plans/round75_c1_index_parity.py --lane .` (01:5x, pre-`6977019b`) | **1** | 2 defects, `WORKTREE dirty` |
| 2 | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 0 | fleet root |
| 3 | `python3 plans/round75_c1_index_parity.py --lane .` (01:58:41, tip `6977019b`) | **1** | 1 defect, dirty |
| 4 | `python3 plans/round75_c1_index_parity.py --lane .` (01:59:40, tip `218a277b`) | **1** | 1 defect, **clean** |
| 5 | `python3 plans/round76_c1_surface_resolver.py --lane .` (tip `218a277b`) | 0 | pass |
| 6 | `python3 plans/round76_c2_defect_discharge.py --lane .` (tip `218a277b`) | 0 | pass |
| 7 | `grep -rl 'routed-findings' /home/vgpnk/Projects/shokunin/*-shokunin/plans` | 0 | siblings |
| 8 | `grep -rl 'PROVINCE' /home/vgpnk/Projects/shokunin/*-shokunin/plans` | 0 | siblings |
| 9 | `grep -rln '## Surfaces\|SURFACES\|ABSENT 20' /home/vgpnk/Projects/shokunin/*-shokunin/plans --include='*.py'` | 0 | resolvers only |
| 10 | `git ls-tree -r --name-only {fda63968,42fad48} -- corpus/evidence/round76 corpus/lessons/round-75-verifier-spotcheck.md` | 0 | provenance |
| 11 | `ls -la /home/vgpnk/Projects/shokuknow/merge/kengaku/` | 0 | presence |
| 12 | python3 one-liner: staged ids (`^\| S\d{3} \|` in `SOURCES.append.md`) ∩ lane ids (`corpus/SOURCES.md`), + `MERGE-REPORT.md` knowledge-target existence test | 0 | collision math |
| 13 | `wc -l corpus/routed-findings.jsonl`; `grep -o '"status": "[a-z]*"' … \| sort \| uniq -c` | 0 | ledger state |
| 14 | `ss -ltn 'sport = :34113'` | 0 | header only → no listener |

## Outputs that matter (verbatim)

Run 1 (pre-integration worktree):

```
LANE_TIP 42fad4827797e540c60a00821d3f2f5c18539632
WORKTREE dirty
UNIVERSE knowledge files=74 indexed=74 missing=0 orphan=0
UNIVERSE lessons files=124 indexed=123 missing=1 orphan=0
UNIVERSE evidence dirs=67 indexed=66 missing=1 orphan=0
MISSING lessons/round-75-verifier-spotcheck.md
MISSING-EVIDENCE round76
PREDICATE R75-C1 fail
```

Run 4 (clean tip):

```
LANE_TIP 218a277bc5bd4f0136ad81c0d892dc6f837eaa16
WORKTREE clean
UNIVERSE lessons files=125 indexed=124 missing=1 orphan=0
UNIVERSE evidence dirs=67 indexed=67 missing=0 orphan=0
MISSING lessons/round-76.md
PREDICATE R75-C1 fail
```

Run 5: `SURFACES total=11 present=4 absent=7 prose=0` / `AGREE agree=11 disagree=0` /
`PREDICATE R76-C1 pass`; per-row: rows 1,2,5,6,7 absent (paths), rows 3,4 absent
(`http=000`), rows 8–11 present.

Run 6: `SCOPE ids=7 registered=7 closed=7 open=0 discharged=7 legs_passed=7 legs_pending=0 wrong=0` /
`PREDICATE R76-C2 pass`; every `LEDGER R75-D1…D7 ok closed close_commit=6977019bdf56`.

Run 7: 13 files, **all** `kengaku-shokunin`. Run 8: 171 files across 10 lanes
(kagi 5, kaidoku 30, kama 5, kasegi 1, kengaku 68, kotoba 18, mado 12, tabi 9, tameshi 9,
tsukuroi 14). Run 9: only `kengaku-shokunin/plans/{round51_surfaces,round76_c1_surface_resolver,state_check}.py`.

Run 12: `staged rows: 175 unique: 175` / `lane rows: 244 range: S001 S252` /
`collisions: 167 free staged ids: ['S087','S088','S089','S095','S096','S098','S099','S235']` /
`staged knowledge targets: 65 present in lane: 4 absent: 61`.

Run 13: `79 corpus/routed-findings.jsonl`; `1 blocked, 45 closed, 31 open, 2 refused`.

Fleet root (`git -C /home/vgpnk/Projects/shokunin status --porcelain`): ` M .scratch/goal-20261103-hyaku-run15.md`,
` M .scratch/run15-state.json`, `?? .scratch/run13-state.json`, `?? .scratch/run15-kernel.py`, `?? after`
(24 B: `== SCORECARD diff base-`). `-uall` filtered for `kengaku|round-76|round76` → `NONE`.

## Findings

**F1 — HIGH — the lane's registered index gate is red at the round's own landing tip.**
At clean tip `218a277b`: `MISSING lessons/round-76.md`, `UNIVERSE lessons files=125 indexed=124 missing=1`,
rc 1. The file is committed (`git ls-tree HEAD -- corpus/lessons/round-76.md` → present, landed in
`f0d52322`), but `corpus/README.md` carries it only as a **prose bullet** at `:975`
(`- Lesson: \`corpus/lessons/round-76.md\` — Gate (S252 admit, two r…`); the gate's `FIRST_CELL`
regex requires a rendered `| \`lessons/<file>\` |` table row, and a bullet cannot index anything.
The `### \`lessons/\` — round lessons and audits (index)` table starts at `:130` and its **last row
is `:915`** (`lessons/round-75-verifier-spotcheck.md`); `:916` is blank, `:917` is
`### Knowledge index rows (3)`.
*Exact repair:* insert one row immediately after `README.md:915`:
`| \`lessons/round-76.md\` | Round 76 — … | LOG.md round 76; plans/round-76-claims.md; \`.ufo/waves/round-76/\` |`
(matching the `round-74.md` / `round-75.md` row shape). Pointer: `corpus/README.md:915-917`,
`corpus/lessons/round-76.md`, `plans/round75_c1_index_parity.py`.
*Re-confirmed at `447f177a` (02:00:24, two commits after the first read): still
`MISSING lessons/round-76.md`, still `PREDICATE R75-C1 fail`.*

**F2 — HIGH — receipts taken inside the wave window measure a tree that no longer exists.**
Five tips in eight minutes (see header). Run 1 reported two defects that were both repaired in
flight; run 3 reported one; run 4 reported a *different* one. `WORKTREE dirty` was true on runs 1
and 3 and false on run 4. The repair that run 1 named (`MISSING lessons/round-75-verifier-spotcheck.md`)
is now row `README.md:915`; the repair that run 3 named is still open (F1). Any gate receipt
committed during 01:5x must name its tip (the R74-D1 `LANE_TIP`/`WORKTREE` line) to be readable at
all. Pointer: the three parity outputs above; `plans/round75_c1_index_parity.py` `lane_tip()`.

**F3 — MEDIUM — the freeze commit itself was red under R75-C1, and only half was repaired.**
`git diff --stat fda63968 42fad48` shows `corpus/evidence/round76/` (10 files + `sources/`) and the
two instruments added with **no** `corpus/README.md` change — i.e. at the freeze commit the lane's
own index gate printed `MISSING-EVIDENCE round76`. `6977019b` ("README index rows") repaired the
evidence mention (now 3 occurrences at `README.md:947,971,973`; evidence universe 67/67) and added
the round-75 spotcheck row, but not the round-76 lesson row. Pointer: `42fad48` diffstat,
`README.md:947`.

**F4 — MEDIUM — assimilation is genuinely blocked, and now more so.**
`/home/vgpnk/Projects/shokuknow/merge/kengaku/` is still present (4 entries, all mtime
`Oct 24 23:33`: `MERGE-REPORT.md` 12 689 B, `MERGE-REPORT.json`, `SOURCES.append.md` 177 759 B,
`knowledge/`). Nothing was written into the lane by it, and it is **unadopted**:
175 staged rows vs a lane registry of 244 rows in `S001…S252` → **167 collide**; only
`S087,S088,S089,S095,S096,S098,S099,S235` are free; **61 of 65** staged knowledge targets are absent
from `corpus/knowledge/` (the 4 present ones — `benchmark-task-validity-checklist.md`,
`contamination-transparency-card.md`, `benchmark-grader-semantics.md`, … — are the lane's own
round-29/30/33 builds per `README.md` §Frontier, not package copies). `Assimilation: none` is
therefore the **honest** line for this round, with one caveat for the report: the collision count
has grown from round-65's stated "114 of 175" to 167, so the package loses adoptability every
round it sits; adoption would need re-iding, not a merge. Pointer: `MERGE-REPORT.md` (head +
`Adopt checklist`), `corpus/SOURCES.md`, `corpus/lessons/round-65.md:49`.

**F5 — MEDIUM — considerthese proposal 1 is *implemented*, not still-unimplemented; R76-C2 extends it.**
The deciding greps: `corpus/routed-findings.jsonl` exists at base with **79 rows** (31 open / 45
closed / 1 blocked / 2 refused) and `plans/routed_open.py` is a **registered gate**
(`SKILL.md:664`: `python3 plans/routed_open.py --lane .`, default `--file corpus/routed-findings.jsonl`);
`corpus/QUALITY.md:1129` and `SCORECARD.md:1571` already carry the criterion
(`routed-findings-burndown`). The lane's own round-65 lesson states it flatly:
"proposal 1 (routed-findings burn-down) → `plans/routed_open.py` (`LOG.md` rounds 40–41) … **No
still-unimplemented proposal remains in that file; none mined this round.**"
So `plans/round-76-claims.md` §Sources' sentence "proposal 1 (routed-findings burn-down) is
implemented by R76-C2" should read **extended by** R76-C2 (7 new rows + re-derived discharge legs),
because the burn-down gate predates this round by ~35 rounds. Consequence for the wave rule "only
one still-unimplemented proposal may be mined this round": **no** unimplemented proposal remains in
`considerthese/2026-10-26.md` (proposals 2 and 3 are recorded as implemented too — V9 counter/Q33,
round-62 class survey), so the round cannot satisfy that rule by mining any of the three; the
defensible framing is instrument extension, and this is the one item the connector/report must not
present as a fresh proposal. I verified proposal 1's state directly (files + registered gate);
proposals 2–3 I take from the round-65 lesson statement and did not re-derive. Pointer:
`considerthese/2026-10-26.md:37`, `plans/round-76-claims.md:111`, `corpus/lessons/round-65.md:47`.

**F6 — LOW — the new resolver is the lane's second Surfaces-table parser; nothing overlaps cross-lane.**
Within the lane, `plans/round51_surfaces.py` (15 876 B) + `plans/round51-surfaces.json` (9 183 B,
round 51) already parsed a surface declaration (a JSON list, not `PROVINCE.md`), and
`plans/state_check.py` reads PROVINCE too; `round76_c1_surface_resolver.py` is the first to parse the
`## Surfaces` table itself. That is a lane-internal supersession question for the reviewer, not a
routing one. Pointer: `plans/round51_surfaces.py:1`, `plans/round51-surfaces.json`.

**F7 — INFO — sibling overlap: nothing to route, both directions.**
`routed-findings` → 13 hits, **all** in `kengaku-shokunin/plans`; no sibling lane has a defect
ledger or a burn-down gate. `PROVINCE` → 171 files across 10 lanes' `plans/`, but these are claim and
record documents naming their own lane's `PROVINCE.md`; **zero** sibling `.py` parses a Surfaces
table (the only three such scripts are kengaku's). So R76-C1's resolver has no sibling counterpart
to route to, and R76-C2's register has no sibling implementation to defer to.

**F8 — INFO — fleet root has no round-76 seat misroot.**
Untracked/modified entries are `.scratch/*` run state plus the 24-byte stray file `after`
(`== SCORECARD diff base-`). None names kengaku or round 76 (`-uall` filter → `NONE`). Reported, not
deleted, per the seat spec.

**F9 — INFO — frontier: this round touches no frontier ground (and the claims say so correctly).**
`corpus/README.md` §Frontier (`:349-…`) lists five items; neither instrument moves any of them —
C1 makes the declaration verifiable and C2 makes the closure's defects burn down. The only frontier
*premise* now re-verified mechanically every run is the "`:34113` is absent" clause of
**Identity-verified endpoint for novelty probes**: `:34113` is `## Surfaces` row 3, so
`python3 plans/round76_c1_surface_resolver.py --lane .` prints `SURFACE 3 absent http://127.0.0.1:34113 (http=000)`
each time, and `ss -ltn 'sport = :34113'` returns header only (no listener, 01:59). That is
re-verification, not discharge — discharge needs a listener plus a re-instantiated
`plans/probe-battery-TEMPLATE.md`. The item a future round could still move is the TB2 task-spec
axis; the command that prices it today is
`ls corpus/knowledge/ | grep -cE '^tb2-.*grader'` → **20** files (28 `tb2-*` files total), and
neither C1 nor C2 discharges it because it needs grader reads (a probe), not a declaration resolver.

## What I could not verify

- **No language server was used or applicable.** Every question here is repository state
  (git objects, `test -e` semantics, README bytes), so the evidence is byte-level and none of the
  absences above is claimed from a cold index. I record the unavailability rather than pass grep
  off as semantic proof.
- I did **not** execute the C1/C2 selftest and mutant batteries
  (`corpus/evidence/round76/c1-selftest.txt`, `c1-mutants.txt`, `c2-selftest*.txt`, `c2-mutants.txt`);
  runs 5–6 are the frozen gates only, and rc 0 there is not evidence about the batteries.
- I read only `MERGE-REPORT.md` in the merge package (per the item bound); `SOURCES.append.md` was
  parsed for its id column and knowledge targets only, never read as prose, and no campaign tool was
  run.
- The 20 `tb2-*grader*` files were counted, not mapped 1:1 to the 89 tasks; the frontier's own
  "N of 89 read" figure was not re-derived.
- F1 is stamped at tip `218a277b`, clean, 01:59:40. A later commit can repair it — re-run
  `python3 plans/round75_c1_index_parity.py --lane .` and expect rc 0 with
  `lessons files=125 indexed=125 missing=0`.
