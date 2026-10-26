# F37ScoutMisroot — hygiene sweep (read-only; nothing deleted, nothing written outside this report)

Run time: ~2026-10-26T02:3x (scratch dirs ctime 02:15-02:17; disk-guard log line 02:34Z). Fleet root = /home/vgpnk/Projects/shokunin.

## 1. Fleet-root untracked entries (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, 68 lines, no `A`/staged)
Untracked (`??`) non-lane-dir, non-`*-scratch` entries:
- /home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run8.md
- /home/vgpnk/Projects/shokunin/.tower/
- /home/vgpnk/Projects/shokunin/.ufo/prompts/closure/kengaku-round-37.md
- /home/vgpnk/Projects/shokunin/.ufo/reports/round-36/kaidoku.md
- /home/vgpnk/Projects/shokunin/.ufo/state/disk-guard.log
- /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log
- /home/vgpnk/Projects/shokunin/.ufo/waves/round-30/
- /home/vgpnk/Projects/shokunin/demo-cwd.txt
- plus 16 `*-shokunin/` lane dirs (incl. kengaku-shokunin/) and 14 `.ufo/waves/shokunin-train-*/x*-scratch/` dirs (pre-existing train leftovers, not r37).
Tracked changes (` M`/` D`) are baseline/state files, none mention round 37 (`git diff --name-only | xargs grep -liE 'round[- ]37|kengaku-r37|F37'` → empty).

### Misroot candidates (content names kengaku round 37)
Command: `git ls-files --others --exclude-standard -- .scratch .tower .ufo demo-cwd.txt | grep -v -- '-scratch/' | xargs -d '\n' grep -liE 'kengaku.{0,20}(round[- ]?37|r37)|round[- ]37|kengaku-r37|F37'`
1. /home/vgpnk/Projects/shokunin/.ufo/prompts/closure/kengaku-round-37.md — closure prompt for kengaku r37 (expected L1/hyaku infrastructure at fleet root, not a stray seat write).
2. /home/vgpnk/Projects/shokunin/.ufo/state/inline-dispatcher.log — dispatcher log lines naming `kengaku-shokunin/.ufo/waves/round-37/build.ready` and `round-37/build.ready` (infrastructure log, not a stray).
3. /home/vgpnk/Projects/shokunin/.ufo/state/disk-guard.log — matched only by false positive `/tmp/tmp.5AzmAF37vM` (`AF37` substring); NOT r37.
Weaker/indirect:
4. /home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run8.md — lines 35 and 45 list "kengaku r36" / "kengaku (37)" (hyaku run 8 goal doc; infrastructure).
5. /home/vgpnk/Projects/shokunin/.ufo/waves/round-37/w1/out (empty directories, untracked-invisible to git so absent from status; `find .ufo/waves/round-37` → `round-37`, `w1`, `w1/out`, no files). Named round-37 at fleet root, content-free; owner unknown (could be any lane's round 37 or a kengaku misroot; kengaku's own waves are under kengaku-shokunin/.ufo/waves/round-37/{build,integrate,falsify}).
Not matching: demo-cwd.txt (0 hits), .ufo/reports/round-36/kaidoku.md (0 hits), .tower/ (no hits).
No stray seat-written r37 file (no seat/report/receipt/fixture named F37*/k37* or a kengaku corpus/plans file) found in the fleet root outside infrastructure files 1-2,4.

## 2. Scratch leftovers /fast/scratch/hyaku/kengaku-r37/ (22 dirs, 0 files; all ctime 02:15-02:17 on 2026-10-26 = live wave-2 seats still running; count was 21 at first listing, 22 at last)
/fast/scratch/hyaku/kengaku-r37/F37C1Rerun
/fast/scratch/hyaku/kengaku-r37/F37C1RerunPy313
/fast/scratch/hyaku/kengaku-r37/F37C2Rerun
/fast/scratch/hyaku/kengaku-r37/F37CritC2Map
/fast/scratch/hyaku/kengaku-r37/F37CritCalibStatements
/fast/scratch/hyaku/kengaku-r37/F37CritNoHarmDiff
/fast/scratch/hyaku/kengaku-r37/F37CritOverfit
/fast/scratch/hyaku/kengaku-r37/F37CritRenamed
/fast/scratch/hyaku/kengaku-r37/F37NoHarmSweep
/fast/scratch/hyaku/kengaku-r37/F37ProbeOnTip
/fast/scratch/hyaku/kengaku-r37/F37ReopenRows
/fast/scratch/hyaku/kengaku-r37/F37RevEntryQuotes
/fast/scratch/hyaku/kengaku-r37/F37RevSkillReadme
/fast/scratch/hyaku/kengaku-r37/F37XMutD4
/fast/scratch/hyaku/kengaku-r37/F37XMutD5
/fast/scratch/hyaku/kengaku-r37/F37XMutP23
/fast/scratch/hyaku/kengaku-r37/F37XMutP4
/fast/scratch/hyaku/kengaku-r37/F37XMutP5
/fast/scratch/hyaku/kengaku-r37/F37XMutP6
/fast/scratch/hyaku/kengaku-r37/F37XMutP7
/fast/scratch/hyaku/kengaku-r37/F37XMutP8
/fast/scratch/hyaku/kengaku-r37/F37XMutP910
(F37ScoutMisroot's own scratch dir was never created — I used none.) These are in-flight peers' dirs, not stale; they are "leftovers" only if still present after their seats finish.

## 3. /tmp named k37-* / cgw-*
Commands: `ls -d /tmp/k37-* /tmp/cgw-*` → "cannot access" for both. Count = 0.
Adjacent, not matching the name pattern but r37-named: /tmp/r37close-src.zCn4Sn (created 02:16; contains gh.body, gh.meta, t/{instruction.md,test_outputs.py,verify.sh}; a github-issue fetch for the C2 git-webserver source, from the CloseKengakuR37 seat). Violates the "no /tmp" scratch directive; reported, not counted.
Also in /tmp, not r37-named but arguably related: /tmp/c3counter_frozen.mjs, /tmp/kasegi-*, /tmp/kas33cl, /tmp/r33-* (kasegi r33, not kengaku).

## 4. Lane status `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain` (at run time)
```
?? .ufo/waves/round-37/falsify.ready.dispatched
?? .ufo/waves/round-37/falsify/
```
Lane HEAD = dc90676b0a01bcb278dba3b5231b504fe2a9ff03 (`git -C ... rev-parse HEAD`); the frozen tip 357deceb is an ancestor of HEAD (`merge-base --is-ancestor` → yes). No modified/staged lane files; only wave-2 untracked markers/report dir.

## Counts
- misroot (stray seat-written r37 content at fleet root): 0 seat strays; 2 infrastructure files naming r37 (items 1, 2) + 1 empty-dir candidate (item 5). Counting only genuine unexplained r37 candidates: the empty fleet-root `.ufo/waves/round-37/w1/out` = 1.
- scratch leftovers: 22 dirs under /fast/scratch/hyaku/kengaku-r37/ (live peers); 0 under /tmp k37-*/cgw-*; 1 stray r37-named /tmp dir (r37close-src.zCn4Sn, reported separately).

VERDICT: misroot-1-scratch-leftovers-22
