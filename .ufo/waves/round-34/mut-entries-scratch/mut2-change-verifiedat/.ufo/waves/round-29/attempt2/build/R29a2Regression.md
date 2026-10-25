# R29a2Regression — the lane's four gates at the frozen base and at the landed attempt-2 tip

Seat: `L1Kengaku29.R29a2Regression` (leaf). Round 29 attempt 2 (hyaku run 6), 2026-10-25.
Scope: run the four named read-only gates, report exact exit codes and key summary lines, and
decide whether any non-zero exit is a regression introduced by this attempt's new files.
No judgement of C1/C2, no edits outside this file. Nothing was written inside the lane by this
seat; all scratch is `/tmp/r29a2-regression/`.

Axes named: **coverage** (does the existing gate population still cover the tree after the
additions) and **operability** (do the standing gates still run green and return the same bytes).

## 1. Headline

| # | Command (exact) | Exit at frozen base `1f3b0f1` | Exit at landed tip | Verdict |
|---|---|---|---|---|
| 1 | `python3 grader.py` | **0** | **0** | no change |
| 2 | `python3 plans/round28_census.py --revision 6baa3090b6cf2d50e56b94b806a69f41220081df` | **0** | **0** | no change |
| 3 | `python3 plans/config_projection.py --summary` | **0** | **0** | no change (byte-identical output) |
| 4 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | **0** | **0** | no change (identical finding set) |

**Regression statement: no. None of the four gates is non-zero at the landed state, and none moved
from the frozen base.** The single non-zero exit I observed among the four was a *transient*
census exit 1 during an in-flight window when the new knowledge entry existed on disk without its
`corpus/README.md` index row (§5, S1b). It is caused by the census's own clean rule
(`plans/round28_census.py:43-47`), disappeared the moment the index row landed, and is an ordering
artifact of the landing, not a defect in the new files.

One adjacent read-only mode *is* non-zero and *is* caused by this attempt's new registry rows:
`sources-census.sh overdue` (baseline 0 → landed 1, §6.1). It is not one of the four gates.

## 2. Method and pinning

The working tree was live: sibling seats landed the C1 entry, its five registry rows and its README
index row *while* I was measuring, and `plans/sources_adopt.py` / `plans/adoption_check.py` were
being edited under me. I therefore measured three pinned states and report all three rather than
one unlabelled number.

| State | Tree | How obtained | Measured (UTC) |
|---|---|---|---|
| **S0** | base revision `1f3b0f1ec41ec297130e8944ff97968d32324632` | read-only export: `git archive 1f3b0f1… \| tar -x -C /tmp/r29a2-regression/base` (no `.git`/`.jj` in the export) | 06:41–06:43Z |
| **S1** | `HEAD=8c14a5d`, tracked tree clean, C1 entry **not yet on disk** | live lane | 06:41–06:43Z |
| **S1b** | `HEAD=8c14a5d`, `corpus/knowledge/benchmark-task-validity-checklist.md` present, index row + registry rows **absent** | live lane (in-flight) | ~06:45Z |
| **S2** | `HEAD=8c14a5d` + sibling working-tree landing (`corpus/SOURCES.md` 81 rows, `corpus/README.md` 38 index rows, entry present) | live lane | 06:46:04Z and 06:46:55Z |

S2 hashes actually measured in the final consolidated run (`MEASURED_AT=2026-10-25T06:46:55Z`,
`HEAD=8c14a5dcd15ac364a352d544660c69f521c3a6af`):

```
3c051a6cc1792e1b71fc18a08ed40921e3fb6d2771c307f4f2bf4d413e4eb0f9  corpus/SOURCES.md
119c99b62058b4d5940ebd1993afb300d57ef4e18d4e610bf0b25198e65e9386  corpus/README.md
4769ce2e2dc632f8d4eb685a8e3590ce107a87dd0767c35c7f7fd05fd5e20df0  corpus/knowledge/benchmark-task-validity-checklist.md
458a850b09942c76c85825487ab0402c8bc0164fa35f3e6cabb3b8af743dc4c2  plans/sources_adopt.py
704b6544a334117e529428d5f93c5360fcb26c3dc37ca80f83b86706fbd84d56  plans/adoption_check.py
90c87c8865022681b1249a42ea580726932d2e97ec0de43e0c89efe0e5ae941f  grader.py
d6e2b0c804c3551de8aac249f633ac5c9130a298d29827c99365def597f45a40  plans/round28_census.py
cb9104264a82e5c6794a3d1a88a5e51445060f8c8e4708740ad0871b1d04fc3c  plans/config_projection.py
```

`corpus/SOURCES.md` changed again between 06:46:04Z (`ffb73d5a…`) and 06:46:55Z (`3c051a6c…`);
the numbers in §4 are the 06:46:55Z run. A reader re-running later must hash first.

Read-only proof: `git status --porcelain` immediately before and immediately after the consolidated
run is identical apart from files that sibling seats created in the interval
(`corpus/evidence/round29-attempt2/`, `gate-*.txt`, `adopt-block.md`, `adoption-measured.txt`);
none of the four commands appears in either diff. The three Python entry points write only to
`tempfile` scratch on their selftest paths (`grader.py:5526`, `plans/config_projection.py:590`), and
the two non-selftest paths taken here (`audit()`, the census's `subprocess` children with
`PYTHONDONTWRITEBYTECODE=1`, `plans/round28_census.py:20`) write nothing.

## 3. S0 — the four gates at the frozen base `1f3b0f1`

Verbatim summary lines and exits, on the `git archive` export:

1. `python3 grader.py` → **exit 0**
   ```
   CHECKS n=733 mismatches=0 errata_pinned=1
   VERDICT: PASS — stored evidence fully re-derives offline
   ```
   (2 stdout lines, empty stderr)
2. `python3 plans/round28_census.py --revision 1f3b0f1…` → **exit 0**
   ```
   c1.exit 0 c2.exit 0 state.exit 0
   sources {'malformed': 0, 'rows': 76, 'statuses': {'mined': 64, 'queued': 8, 'rejected': 4}, 'tiers': {'A': 70, 'B': 4, 'C': 2}}
   knowledge {'dangling': [], 'duplicate_rows': [], 'files': 37, 'index_rows': 37, 'unindexed': []}
   ```
   `historical_state`: 329 assertions, match 316, mismatch 0, offline_unverifiable 7,
   out_of_population 34, superseded 6.
3. `python3 plans/config_projection.py --summary` → **exit 0**, last line verbatim:
   ```
   TOTAL findings=0 exit=0
   ```
   (54 lines, 33 `PROFILE` lines, 10 `LIMIT` lines, `POPULATION {"distinct_task_ids": 812, …, "task_profile_projections": 2436}`)
4. `sources-census.sh validate` → **exit 0**, last line verbatim (run at S0 with
   `--file /tmp/r29a2-regression/base/corpus/SOURCES.md`, because the lane-id form needs a live
   lane dir):
   ```
   file	ok	/tmp/r29a2-regression/base/corpus/SOURCES.md
   ```
   plus 14 × `W04` duplicate-URL warnings (S040 S048 S057 S058 S059 S064 S065 S066 S067 S068 S069
   S071 S075 S076), unchanged from the live run's warning set.

## 4. S1/S1b/S2 — the four gates at the tip

### 4.1 S1 — tip `8c14a5d`, C1 artifacts not yet on disk (`git status --porcelain` = only `.ufo/…` untracked)

| Command | Exit | Key line |
|---|---|---|
| `grader.py` | **0** | `CHECKS n=733 mismatches=0 errata_pinned=1` / `VERDICT: PASS — stored evidence fully re-derives offline` |
| `round28_census.py --revision 6baa3090…` | **0** | `sources {'malformed': 0, 'rows': 76, 'statuses': {'mined': 64, 'queued': 8, 'rejected': 4}, 'tiers': {'A': 70, 'B': 4, 'C': 2}}`, `knowledge {'dangling': [], 'duplicate_rows': [], 'files': 37, 'index_rows': 37, 'unindexed': []}` |
| `config_projection.py --summary` | **0** | `TOTAL findings=0 exit=0` |
| `sources-census.sh validate --root … kengaku` | **0** | `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` + 14 `W04` |

Tip-vs-base identity, measured, not assumed:

- `diff grader.out tip.out` → **no output** (`GRADER_IDENTICAL`).
- `diff base-proj.out tip-proj.out` → **0 diff lines** (`PROJ_IDENTICAL_ALL_LINES`).
- `diff <(cut -f2- base-fleet.out) <(cut -f2- tip-fleet.out)` → only the `ok` row's path column
  differs (export path vs lane path); the 14 `W04` rows are identical.
- census payload (all keys except `revision_label`/`measurement_root`) is identical between S1 and
  S0 *except* the two VCS-tree assertions `P4c.r25.raw-tree-entries` and `P4c.r25.markdown-reports`,
  which are `OFFLINE_UNVERIFIABLE` in the `.git`-less export and `MATCH` in the lane
  (`plans/state_check.py:110`, "read-only Git tree counts at the three cited revisions"). That is
  an environment difference of my export, not tree content; exit stays 0 either way.

### 4.2 S1b — in-flight: entry on disk, index row and registry rows absent

```
POST_CENSUS_EXIT=1
sources {'malformed': 0, 'rows': 76, 'statuses': {'mined': 64, 'queued': 8, 'rejected': 4}, 'tiers': {'A': 70, 'B': 4, 'C': 2}}
knowledge {'dangling': [], 'duplicate_rows': [], 'files': 38, 'index_rows': 37, 'unindexed': ['knowledge/benchmark-task-validity-checklist.md']}
```

Cause is the clean rule itself (`plans/round28_census.py:43-47`: `unindexed` non-empty ⇒
`return 1`). This window closed when the README index row landed (S2 below). Recorded because the
task asked for every non-zero exit: this one is **not** a defect in the new files and does not
persist, but it shows the landing order is load-bearing — the entry file alone reds the census.

### 4.3 S2 — landed state (the answer set)

| # | Command | Exit | Key summary line (verbatim) |
|---|---|---|---|
| 1 | `python3 grader.py` | **0** | `CHECKS n=733 mismatches=0 errata_pinned=1` · `VERDICT: PASS — stored evidence fully re-derives offline` |
| 2 | `python3 plans/round28_census.py --revision 6baa3090b6cf2d50e56b94b806a69f41220081df` | **0** | `c1.exit=0 c2.exit=0 state.exit=0` · `sources={"malformed": 0, "rows": 81, "statuses": {"mined": 69, "queued": 8, "rejected": 4}, "tiers": {"A": 75, "B": 4, "C": 2}}` · `knowledge={"dangling": [], "duplicate_rows": [], "files": 38, "index_rows": 38, "unindexed": []}` |
| 3 | `python3 plans/config_projection.py --summary` | **0** | `TOTAL findings=0 exit=0` (output byte-identical to the base run: `diff` → 0 lines) |
| 4 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kengaku` | **0** | `kengaku	ok	/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/SOURCES.md` + 14 `W04` |

Delta base→landed, all explained by the five admitted rows and the one entry:

- `sources.rows` 76 → 81 (+5: `S077 S078 S079 S080 S090`, appended inside `## Registry`,
  lines 100–104, `## Paths` now at 106 — so `E12` (row outside Registry) is not triggered);
  `statuses.mined` 64 → 69; `tiers` A 70 → 75, B 4, C 2.
- The five rows are all `tier=A` (S090 was `tier=B` in the merge floor
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md:20`, re-tiered in the landing) with
  `opened=2026-10-25`, `recheck=2026-10-25`, 11 columns, `used-by` = the entry path only.
- `knowledge.files` 37 → 38 and `index_rows` 37 → 38 (`corpus/README.md:64`), `unindexed=[]`.
- `grader.py` check population unchanged at **n=733** and byte-identical output: the new entry,
  `plans/sources_adopt.py` and `plans/adoption_check.py` are outside grader's coverage (see §6.3).

## 5. Why the green state is not luck: causal separability

- Tracked delta base→`HEAD`: **9 files, all additions**, `git diff --stat 1f3b0f1..HEAD` shows
  `.ufo/waves/round-29/attempt2/{adoption-expect.json,control.nothing.txt,package-gate.txt}`,
  `considerthese/2026-10-{22,23,24}.md`, `plans/adoption_check.py`,
  `plans/round-29-attempt2-claims.md`, `plans/sources_adopt.py`. No `corpus/` file, no `grader.py`,
  no census or projection source. (`git diff --stat HEAD` empty ⇒ the tracked tree was clean.)
- No gate entry point references the new tools: `grep -c 'sources_adopt\|adoption_check'` = **0**
  for `grader.py`, `plans/round28_census.py`, `plans/config_projection.py` and
  `scripts/sources-census.sh`. The gates cannot be perturbed by the new files except through
  `corpus/` bytes, which is exactly what S2 measures.
- S0 and S2 agree on all four exits and on grader/projection bytes; the only payload movement is
  the five registry rows and the one index row, both visible in the census output above.

## 6. Adjacent observations (not part of the four-gate verdict)

**6.1 `overdue` is now non-zero because of these rows.** Same read-only script, adjacent mode:

```
$ sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-25 kengaku
kengaku	overdue	S090 0d recheck=2026-10-25 opened=2026-10-25
kengaku	overdue	S080 0d recheck=2026-10-25 opened=2026-10-25
kengaku	overdue	S079 0d recheck=2026-10-25 opened=2026-10-25
kengaku	overdue	S078 0d recheck=2026-10-25 opened=2026-10-25
kengaku	overdue	S077 0d recheck=2026-10-25 opened=2026-10-25
exit=1
```

At S0: `overdue` exit **0**, **0** overdue rows (only `cadence` lines, which never change status
per the script header `scripts/sources-census.sh:35-36`). So anyone running the fleet recheck queue
now gets 5 rows due at `0d` and a non-zero exit. This is the direct consequence of the frozen C2
rule "prose `recheck` cells are normalized to the frozen access date"
(`plans/round-29-attempt2-claims.md` §C2 item 3) applied to `opened=2026-10-25`: `recheck == opened`.
It is a spec consequence, not a defect I am entitled to call, but it does move a read-only fleet
mode from 0 to 1 and the L1 should decide whether that is the intended recheck semantic.

**6.2 The census revision label does not name the measured tree.** `--revision` is documented as
caller-supplied (`plans/round28_census.py:2,14`, and the JSON carries
`"revision_authority": "caller-supplied; see export/byte-equality receipt"`). As given, the label
`6baa3090…` is a commit 13 files behind the frozen base (`git diff --stat 6baa3090..1f3b0f1` = 13
files, 334 insertions) and further behind the tip; no byte-equality export accompanies this
attempt's artifacts. The green exit is real, but the `revision_label` must not be cited as
"measured at 6baa3090" without that receipt.

**6.3 Coverage gap, measured.** `grader.py` prints `n=733` before and after the landing, with a
byte-identical two-line verdict. So the corpus's newest entry and the two new `plans/` tools are
covered by *no* grader check; the only gates that see them are the census's index/registry block
and the fleet `validate` row grammar. A malformed `sources_adopt.py` or a wrong quote inside the
entry would not red any of the four gates.

**6.4 Not mine to judge (cited only).** Sibling receipt
`.ufo/waves/round-29/attempt2/gate-postappend-rerun.txt` reads
`registry=81 staged=173 collisions=5 … collisions: S077 S078 S079 S080 S090` — i.e. re-running the
C2 gate on the same staged block after the append reports the committed ids as collisions. That
follows the frozen contract (item 4 refuses on a nonempty collision set); I did not re-run the tool
(it can write) and record this as a pointer only.

## 7. Limits of this report

- Only the four commands above were exercised as gates. I did **not** run
  `plans/sources_adopt.py --selftest` or `plans/adoption_check.py` (other seats' scope, and the
  latter plus the append path can write); my green numbers say nothing about C2's ten cases or C1's
  `entries=1 …` target.
- `overdue` (§6.1) and the `P4c.r25` flip (§4.1) are the only excursions; both are labelled with
  their cause and neither is in the four-gate set.
- S0 numbers come from a `git archive` export, so `.git`-backed assertions degrade to
  `OFFLINE_UNVERIFIABLE`; no exit changes. An in-repo checkout of `1f3b0f1` was not made (it would
  be a write to the lane).
- The tree is live; a later reader must re-hash `corpus/SOURCES.md`, `corpus/README.md` and the
  entry against the §2 hashes before comparing numbers.

## 8. Tooling

No tool was installed, upgraded or removed by this seat (all four commands use the existing
`python3` and the fleet `sources-census.sh`). Scratch: `/tmp/r29a2-regression/{base,sim,*.out,*.json}`
(`base/` = `git archive` export of `1f3b0f1`; `sim/` = a scratch projection used in §6 only, never
applied to the lane).
