# Seat report — R12ShonenEvidence (kengaku round 55, w1)

**Remit:** non-author evidence for SHONEN.md's four `[~]` promotion boxes.
**Lane writes:** none outside this output dir
(`.ufo/waves/round-55/w1/R12ShonenEvidence/`). No git/jj mutation anywhere.
**Installs:** none. **Subagents:** none.

## What I ran (cwd = lane root unless noted; all 2026-10-30)

| # | Command | Exit | Purpose |
|---|---|---|---|
| 1 | `test -e` on `corpus/evidence/round9-fleet/harness-mutation.md`, `round8-horizon/run.log`, `round12-ladder/probe_plan_r12.md`, `corpus/knowledge/ledger-route-telemetry.md` | 0 | Box 1 citation resolution (4 paths) |
| 2 | `sed -n '81,83p' corpus/evidence/round8-horizon/run.log` | 0 | Box 1 cited line content == claimed figures (A-INC 7/10, A-MONO 0/10, A-CKPT 1/10) |
| 3 | `python3 grader.py --selftest` (timeout 280) | **0** | Box 1 command citation; `[selftest] ALL PASS`; 2.73 s → `grader-selftest.out` |
| 4 | `test -e` on round-54 receipts: `integrate/{c1-after,c2-after,round52-c2-regression,census-end}.txt`, `corpus/evidence/round54/{c1-before,c2-before-dry}.txt` | 0 | Box 2 receipt existence (6/6) |
| 5 | `tail`/`grep` on c1-after, c2-after, regression head, census-end | 0 | Box 2 receipt bytes == LOG round-54 measured-close claims (executed=78, laundered=1, green61/red17, redeclared=4; ADVERTISED 79 / REGISTERED 77 / MISSING 2; ROWS 193, A164/B24/C5, mined172/queued8/rejected13) |
| 6 | `python3 plans/round55_c2_controls.py --selftest` with `TMPDIR=<seat-scratch>/tmp` (timeout 240) | **0** | Box 3 cold execution; `SELFTEST cases=4 failures=0` → `controls-selftest.out` |
| 7 | `python3 plans/round55_c2_controls.py --case abbreviated-selftest --against r54` (timeout 240) | **0** | Box 3 corroboration; `ROUTE laundering demonstrated (r54 rc=0, true entry exit=1)` == frozen R55-C2 before-red shape → `case-abbrev.out` |
| 8 | `test -e grader.py && sha256sum grader.py` | 0 | Box 4 spot 1: sha `90c87c88…ae941f` == PROVINCE Core pin |
| 9 | 12-dir `test -d` loop over `corpus/evidence/round{8-horizon,…,18-kimi-routing}` | 0 | Box 4 spot 2: nothing missing |
| 10 | `test -e corpus/SOURCES.md && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 0 | Box 4 spot 3: present, live count 195 (dated row says 171@r51; r54 census-end 193) |

## Files written

- `.ufo/waves/round-55/w1/R12ShonenEvidence/boxes.md` — per-box verdicts + pointers (the deliverable)
- `.ufo/waves/round-55/w1/R12ShonenEvidence/report.md` — this report
- `.ufo/waves/round-55/w1/R12ShonenEvidence/{grader-selftest.out,controls-selftest.out,case-abbrev.out}` — raw run bytes
- `.ufo/waves/round-55/w1/R12ShonenEvidence.md` — scoped findings at the seat's Report-trailer path

## Verdicts

- **Box 1 (SKILL decision tables/error patterns/checklists + cites): SUPPORTED.**
- **Box 2 (end-to-end task executed + logged): SUPPORTED** (round 54, latest landed).
- **Box 3 (instructions executable cold): SUPPORTED** — executed two written invocations of `plans/round55_c2_controls.py` from bytes alone; both behaved exactly as the frozen claims document.
- **Box 4 (no bleed / PROVINCE accurate): SUPPORTED** — 3 Core rows re-run, all resolve; count drift is dated-snapshot growth, not bleed.

## Defects found

None blocking. Minor observations (recorded in `boxes.md` §Residual notes):
PROVINCE Core's SOURCES row count (171) is a dated round-51 snapshot while the
live registry stands at 195 (193 at the r54 census-end receipt) — the row
self-dates and cites its deriving command, so this is accuracy-preserving, but a
future seat re-deriving Core rows live should expect to restate counts.

## Dead ends

None. (Briefly considered running the full `python3 grader.py` 733-check replay
for extra box-1 weight; the `--selftest` command-citation already satisfies the
seat's run-one requirement and the full replay duplicates peer E10's no-harm
scope, so it was not run — reported as unrun, not passed.)

## Hygiene

Scratch `/fast/scratch/hyaku/kengaku-r55/R12ShonenEvidence/` deleted after
copying receipts into the output dir. No pacman transaction; no PATH writes;
no network calls beyond the lane's own files.
