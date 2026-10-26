# F39ScoutMisroot — misroot and scratch audit (kengaku r39 wave 2)

Read-only scout. Nothing deleted, nothing written outside this report dir. Commands: `F39ScoutMisroot/commands.txt`.
Sampled ~04:43–04:46 -0300 on 2026-10-26; the fleet is live (26 seat dirs, peers still running), so "leftover" is judged by seat liveness.

## 1. Misroot: fleet-root `git status` (`/home/vgpnk/Projects/shokunin`)
`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` → 178 lines (2 `??`, 157 ` A` intent-to-add, 19 ` M`).
- 111 are `.tower/comms/*` (r18/r100 tower mail), 41 `.tower/quarantine/kaika-fleetroot-20261019/*`, plus `.ufo/state/*.report-baseline` (M), `.ufo/watchdog.log`, `.scratch/goal-20261026-hyaku-run8.md`, `demo-cwd.txt`, `scripts/hyaku/hyaku.env`, `lane-addendum.md`, `.ufo/waves/round-30/wave1/ScribeLesson.md`, `.ufo/prompts/closure/kengaku-round-37.md`.
- Content grep for kengaku r39 markers (`kengaku…r39|round-39|kengaku-r39|k39-`) across all 178 paths hits exactly two files:
  - `.ufo/state/inline-dispatcher.log` — harness dispatcher output (lines 821, 834, 972–1004 name `kengaku-shokunin/.ufo/waves/round-39/build.ready` as dispatch targets). Not seat-written.
  - `.ufo/reports/round-40/tsukuroi.md` (untracked, 04:40:45) — authored by `TsukuroiR40`; mentions "round-39" only as tsukuroi's own cross-references. Not a kengaku seat.
- No fleet-root path contains `F39*`, `R39*` seat names (grep for `F39[A-Z]…|kengaku-r39` over fleet root excluding other lane trees hits only harness prompts/reports: `.ufo/prompts/kengaku-round-39.md`, `.gitignore`, `.scratch/goal…`, older round reports).
- Kengaku-adjacent changes at fleet root are harness-written, not seat misroots: `.ufo/state/kengaku.report-baseline` (M, `32 e3b0…`→`39 e3b0…`, mtime 03:23:51, same second as `.ufo/prompts/kengaku-round-39.md`, committed as 5c263b30 "kengaku dispatch evidence").
- `kengaku-shokunin/` is ignored (`!!`) at fleet root; its tree is out of scope here.
- Fleet-root files newer than 02:00 outside other lanes' trees and state logs: only reports/prompts/closure files of other lanes; none kengaku-r39 seat output.

**misroot = 0**

## 2. Scratch: `/fast/scratch/hyaku/kengaku-r39/*` (26 dirs; /fast 804G, 226G used, 29%)
Sizes (`du -sh`, first sample): F39AnchorFix 556M, F39C1Rerun 557M, F39C2Rerun 1.1G, F39CritAudit 556M, F39CritC1Count 556M, F39CritPriorArt 404K, F39CritQ30 556M, F39CritSkill 556M, F39EntryQuotes 556M, F39IndepProbe 556M, F39LedgerTip 556M, F39MutDirection 725M, F39NoHarmC1 1.9G, F39ReopenRows 8K, F39RevBatD5 556M, F39RevBatP1 559M, F39RevBatP3 605M, F39RevBatP7 556M, F39XMut 556M, L1 1.6G, R39MergeRescreen 808K; plus F39ConnFrontier, F39CritNoHarmDiff, F39CritOverclaim, F39RevLesson, F39RevScorecard created later.
Liveness per dir (mtime within the last ~3 min or processes whose args name the dir):
- Live processes: F39C1Rerun(2), F39MutDirection(6), F39NoHarmC1(4), F39RevBatP3(2).
- Wave-2 seats still active by mtime/roster (writing at 04:39–04:43): all other `F39*` dirs — in-flight, not leftovers.
- **Stale (wave-1 residue, owner finished, 0 processes, report already filed):**
  - `R39MergeRescreen` — 808K, mtime 03:54:55; wave-1 report `build/R39MergeRescreen.md` exists.
  - `L1` — 1.6G, mtime 04:38:01; L1 integrator landing clone; landing measurement already at `integrate/measure-final.txt`.
- Not seat-leftovers: none under `/tmp` (`ls -d /tmp/*k39* /tmp/*kengaku*` → no such file).
Note: after wave 2 ends every `F39*` dir (~15 GB total) becomes leftover unless its seat's EXIT trap fires; re-run this `du` at close.

**scratch leftovers = 2** (`L1`, `R39MergeRescreen`)

## 3. Processes: `ps -eo pid,etime,cmd | grep -E 'kengaku-r39|k39-'`
First sample (9): pids 2703421 (round37_c1_verify, F39NoHarmC1/w37, etime 01:50), 3499873 (mutant_direction_check, F39MutDirection), 3534687 (round38_c1_verify, w38tip), 3549998 (round37_c1_verify, w37base), 3605079 (F39RevBatP3/driver.py), 3610651 (git clone F39CritNoHarmDiff), 3612148/3612179 (gate scripts under F39NoHarmC1). Second sample: also 3616272 (round39_c1_verify, F39C1Rerun/w-v-a4). All etimes ≤ 2 min, all parented under currently-running wave-2 seats' work dirs (F39NoHarmC1 is running three C1 counters back to back); they come and go between samples.
- `ps … | grep sleep` → only transient `sleep 1`; the wave-1 `sleep 5311` survivors are **gone** (no sleep with a long etime; none matching `F39|kengaku|k39`).
- No process older than 2 min references kengaku-r39 or k39-.

**leftover procs = 0** (9–10 live children of running wave-2 seats are in use, not leftovers)

## Gaps
- Cannot distinguish a seat that crashed without cleanup from one idle between commands for the F39 dirs with 0 processes; I used mtime (≤ ~5 min) and the roster. Re-run at wave close.
- Fleet-root status lines are harness/other-lane state; I did not attribute each of the 178 individually beyond the content grep and path classes above.

VERDICT: misroot-0-scratch-leftovers-2-procs-0
