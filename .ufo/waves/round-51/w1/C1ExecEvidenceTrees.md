# C1ExecEvidenceTrees — Core row "Own probe artifacts" completeness audit

Seat: `C1ExecEvidenceTrees` (executor, leaf). Round 51 / hyaku run 11.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin` (read-only).
Scratch: `/fast/scratch/hyaku/kengaku-r51/C1ExecEvidenceTrees` (removed before yield; `df -h /fast` showed `804G total, 553G avail, 32% used`).

## Axes named

- **Freshness (primary, C1)** — does the Core row at `PROVINCE.md:109` tell the truth about the lane's own probe artifacts, and is that truth machine-checkable by the frozen counter?
- **Surface truth (supporting)** — the row's two asserted counts (twelve dirs; 28 root receipt logs) vs the tree and vs `corpus/README.md`.
- Adjacency (C2) not touched; no production file read-modified, none written outside this report.

## Revision measured

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
```
(`git log -1 --format='%H %s'` → `4090c3db79d11279ab5e5121ba25e74aa316e6e7 round-51: v2 wave spec (64 seats) + validated dispatch payload`. Stage-1 freeze commit was `e07f131cf7037e58a21db6e1f3986cf401ad257c`; the tip has advanced by the wave-spec commit only. `git status --porcelain -- corpus/evidence` is empty: no evidence file is modified or untracked.)

## The row under test

`PROVINCE.md:109` (`### Core` table):

```
| Own probe artifacts | `for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage round14-fleet round18-kimi-routing; do test -d corpus/evidence/$d || echo missing $d; done` (prints nothing) | all present; plus 28 root receipt logs indexed in `corpus/README.md` |
```

The loop names **12** dirs and already includes `round13-coverage` and `round18-kimi-routing`; there are no dirs beyond the loop. The sibling `## Surfaces` row (`PROVINCE.md:18`) names only **10** of them (`round8-horizon round9-replication round9-fleet round10-fleet round11-power round11-fleet round12-ladder round12-fleet round13-ack-state round14-fleet`) — `round13-coverage` and `round18-kimi-routing` appear only in the Core row. All 12 exist, so this is a prose asymmetry between the two tables, not drift.

## Commands run (verbatim) and observed output

### 1. The row's own check, run exactly as written

```sh
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
for d in round8-horizon round9-replication round9-fleet round10-fleet round11-power \
         round11-fleet round12-ladder round12-fleet round13-ack-state round13-coverage \
         round14-fleet round18-kimi-routing; do
  test -d corpus/evidence/$d || echo missing $d
done
```

Observed: **no output**, `loop_exit=0`. The row's parenthetical "(prints nothing)" is true at this revision.

### 2. Per-dir existence, file count, README evidence-table index, tracked count

```sh
for d in <the twelve>; do
  test -d corpus/evidence/$d   # exists?
  find corpus/evidence/$d -type f | wc -l
  grep -c -- "$d" corpus/README.md
done
git ls-files corpus/evidence/$d | wc -l
```

| dir | exists | files (`find -type f`) | README evidence-table row | README hits | git-tracked files |
|---|---|---|---|---|---|
| `round8-horizon` | yes | 4 | line 169 | 4 | 4 |
| `round9-replication` | yes | 8 | line 170 | 5 | 8 |
| `round9-fleet` | yes | 19 | line 171 | 2 | 19 |
| `round10-fleet` | yes | 22 | line 172 | 1 | 22 |
| `round11-power` | yes | 12 | line 173 | 2 | 12 |
| `round11-fleet` | yes | 18 | line 174 | 1 | 18 |
| `round12-ladder` | yes | 18 | line 175 | 3 | 18 |
| `round12-fleet` | yes | 22 | line 176 | 1 | 22 |
| `round13-ack-state` | yes | 2 | line 177 | 2 | 2 |
| `round13-coverage` | yes | 11 | line 179 | 5 | 11 |
| `round14-fleet` | yes | 12 | line 178 | 3 | 12 |
| `round18-kimi-routing` | yes | 1 | line 180 | 2 | 1 |

All twelve are indexed: each has a dedicated `| \`evidence/<dir>/\` | ... |` row in the `### \`evidence/\` — durable run bytes and L2 analyses` table of `corpus/README.md` (rows 169–180). For every dir `find -type f` equals `git ls-files` — no untracked file inflates a count, nothing is session-only. Total across the twelve: **149 files**.

README-declared counts that can be cross-checked are exact: `round12-ladder` "18 files" = 18; `round12-fleet` "22 files" = 22; `round13-ack-state` "two stdlib audit scripts" = 2 files; `round18-kimi-routing` "Digest index … README.md" = 1 file.

### 3. The "28 root receipt logs" count

```sh
ls corpus/evidence/*.txt corpus/evidence/*.log 2>/dev/null | wc -l   # -> 28
ls corpus/evidence/*.log | wc -l                                     # -> 28
ls corpus/evidence/*.txt 2>/dev/null | wc -l                         # -> 0
git ls-files corpus/evidence | grep -E '^corpus/evidence/[^/]+\.log$' | wc -l  # -> 28
grep -cE '^\| `(probe-r19|attrib-r2)[^`]*\.log`' corpus/README.md    # -> 28
grep -oE '^\| `(probe-r19|attrib-r2)[^`]*\.log`' corpus/README.md | tr -d '|` ' | sort -u | wc -l  # -> 28 distinct
```

- On disk: **28** files, all `.log`, **0** `.txt`; all 28 are git-tracked.
- README: the "Root-level receipt logs" table has **28** rows, one per log; set difference between on-disk basenames and README row names is **empty** (`diff` → `IDENTICAL_SETS`).
- Breakdown: 19 `probe-r19-*.log` + 9 `attrib-r2[123]-*.log`.

The row's second assertion therefore holds exactly: **28 root receipt logs, all indexed**.

### 4. Frozen instrument cross-check (`plans/round51_surfaces.py` + manifest)

```sh
python3 plans/round51_surfaces.py --lane .
```

Observed (verbatim, tail):

```
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
MANIFEST plans/round51-surfaces.json entries=19 sections=2
ANCHORS total=19 dup=0 missing=0
ROWS section="## Surfaces" rows=9 entries=9 uncovered=0
ROWS section="### Core" rows=10 entries=10 uncovered=0
PROBES run=19 present=13 absent=6 errors=0
DRIFT 3
STALE 0
UNVERDICTED 1
NUMBER-DRIFT 1
  DETAIL NUMBER-DRIFT SF14 row claims 25, probe says SOURCES rows=170
ANCHOR-DUP 0
ANCHOR-MISSING 0
UNCOVERED 0
SECTION-MISSING 0
RESOLVE observed_present=13 floor=13 verdict=met
PREDICATE R51-C1 fail
ACTUAL_EXIT=1
```

(`ACTUAL_EXIT=1` captured with the pipeline removed; the earlier `EXIT=0` in a `| tail` invocation was `tail`'s status, not the counter's.)

How the instrument actually covers this row — manifest, read directly:

- `SF11` (`### Core`, anchor `| Own probe artifacts | \`for d in round8-horizon `), `state=present`, `prose=present`, `probe.kind=paths`, **7 targets**: `round9-fleet, round10-fleet, round11-power, round11-fleet, round12-fleet, round13-ack-state, round18-kimi-routing`. Its `why` reads "the Core row's loop names twelve evidence dirs" — the probe tests 7 of those 12.
- `SF07` (`## Surfaces`, anchor `` `corpus/evidence/round8-horizon/`, `round9-replication/` ``), `probe.kind=paths`, **5 targets**: `round8-horizon, round9-replication, round12-ladder, round14-fleet, round13-coverage`.
- The two target sets are disjoint and their union is exactly the twelve dirs, so **all 12 are machine-probed somewhere**, but neither entry probes its own row's full set (SF11 7/12, SF07 5/10). The Core row's row-local machine check is the shell loop, which the counter does not execute; it executes a 7-path subset.
- No manifest entry carries a `count_claim` for the "28 root receipt logs" (only `SF14` has a `count_claim`, `25`, for the SOURCES registry). The 28 is verified only by this audit and by the README table rows; `NUMBER-DRIFT` cannot see it if the count moves.

## Findings

1. **Both counts the row asserts are true at the tip.** 12/12 dirs exist (`test -d` loop prints nothing, exit 0); 28/28 root receipt logs exist and each is indexed by exactly one README table row.
2. **All twelve dirs are indexed** in `corpus/README.md`'s `### evidence/` table with dedicated rows (169–180); every dir's file count equals its git-tracked count, so the "durable run bytes … nothing … session-only storage" half of the row is supported for these dirs.
3. **Coverage asymmetry (prose, not drift):** the `## Surfaces` row names 10 dirs, the `### Core` row loops 12; `round13-coverage` and `round18-kimi-routing` are declared only in the Core row.
4. **Instrument gap (freshness-relevant):** `SF11`'s probe set is 7 of the 12 dirs its own row loops, while its `why` says twelve; the remaining 5 are probed by `SF07` under a different row. The row's "28 root receipt logs" count has no `count_claim` and is therefore outside `NUMBER-DRIFT`. The frozen counter can report `UNCOVERED 0` and `DRIFT 0` for this row while 5 of its 12 declared dirs and its 28-log count are not read by the entry that covers it. This is an observation for the L1/critic; this seat changes nothing.
5. No row-level falsehood found: nothing in this row's claim failed at `4090c3db`.

## Limits

- Point-in-time audit at `REV 4090c3db…`; only existence, file counts, git-tracked counts, and README indexing were checked — file *contents*, md5 pins quoted in the README cells (e.g. `df154cb5…`, `9dd8aa2b…`), and the `/tmp`-citation clause of the row were **not** re-verified by this seat.
- `find`/`ls` counts include dotfiles; the equality with `git ls-files` shows no hidden untracked files, but `.gitignore`d trees were not enumerated.
- The frozen counter was executed read-only; `PREDICATE R51-C1 fail` with `DRIFT 3 / UNVERDICTED 1 / NUMBER-DRIFT 1` reproduces the C1 before-state, not a new measurement of the after-state.
- Nothing was written outside this report; no commit, push, or mutating git command was issued; scratch dir was removed.

VERDICT: PASS for the audited claim — the Core row's "Own probe artifacts" assertion is true at REV 4090c3db (12/12 dirs present, 149 tracked files, all twelve indexed in `corpus/README.md`; 28/28 root receipt logs present and indexed with identical name sets); two freshness-relevant gaps recorded for the L1, not repaired here: `SF11` machine-probes only 7 of the row's 12 dirs (union with `SF07` covers 12/12) and the row's 28-log count carries no `count_claim`, so `NUMBER-DRIFT` cannot detect its movement.
REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7
