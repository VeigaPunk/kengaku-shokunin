# F38ScoutMisroot — misroot/scratch sweep (kengaku r38 wave 2), run 2026-10-26 03:14–03:16 -0300

Report only; nothing deleted, no lane/fleet file edited.

## 1. Fleet-root misroot
Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` → 178 lines
(`wc -l`). Content/name filter (`grep -iE 'kengaku|round[- _]?38|\bR38\b|F38'` per file; plus
`git status ... | grep -iE 'kengaku|38'`) leaves only 3 status lines naming kengaku:

| path | state | verdict |
|---|---|---|
| `.ufo/reports/round-38/kengaku.md` | `??`, mtime 03:08:32, 13109 B | NOT a misroot: the mandated L1 report path (`.ufo/prompts/kengaku-round-38.md:101`, `.scratch/goal-20261026-hyaku-run8.md`) |
| `.ufo/state/kengaku.report-baseline` | ` M`, diff `32 e3b0…` → `38 e3b0…` | harness baseline counter, expected |
| `.ufo/prompts/closure/kengaku-round-37.md` | ` A` (intent-to-add), mtime 02:14 | round-37 closure artefact, pre-r38 |

The other ~175 entries are older intent-to-add (` A`) `.tower/**` (r18/r100 comms, quarantine), `.ufo/state/*.report-baseline`,
`.ufo/watchdog.log`, `.ufo/state/inline-dispatcher.log`, `.ufo/state/disk-guard.log` (hyaku harness logs that mention kengaku
in lines — written by the dispatcher, not a seat), `.scratch/goal-20261026-hyaku-run8.md`, `demo-cwd.txt` (30 B, 2026-10-25 20:54, content `/home/vgpnk/Projects/shokunin`,
pre-r38), `scripts/hyaku/*`. `find` for names `*f38* *r38* *round-38* *round38* *battery38*` at depth ≤2 outside `*-shokunin/` → none.
Fleet-root files newer than 2026-10-26 00:00 outside `*-shokunin/` and `.ufo/`/`.scratch/`/`.git`: only the tracked
AGENTS/LOG/README/SCORECARD/MANIFEST (02:27–03:00, hyaku harness regeneration; no kengaku r38 content by the grep above).
`/tmp/tsk-r38-{census,live}-before.txt` (01:08) are tsukuroi r38 (grep -c kengaku|F38 = 0), not kengaku.
`kengaku-shokunin/.ufo/waves/round-38/falsify/` holds only `F38*` seat dirs + `swarm-registry.json`; no corpus/plans/lane/.git copy
(`find . -maxdepth 2 -type d ( -name corpus -o -name plans -o -name lane -o -name .git )` → empty).

**misroot count = 0.**

## 2. Scratch under /fast/scratch/hyaku/kengaku-r38/
Command: `du -sh /fast/scratch/hyaku/kengaku-r38/*` (snapshot 03:15; `du -sh` of the parent = 20G; 22 dirs):
F38AnchorFix 548M · F38C1Rerun 735M · F38C1RerunPy313 1.2G · F38CritBatD 861M · F38CritBatE 865M · F38CritBatF 725M ·
F38CritOverclaim 0 (empty dir, no files) · F38CritSeparability 1.4G · F38CritSkipControls 548M · F38CritTags 548M ·
F38LedgerTip 3.1G · F38MapV7Control 548M · F38MutC2Counter 548M · F38NoHarmSweep 549M · F38ReopenRows 528K ·
F38RevBatA 548M · F38RevBatB 548M · F38RevBatC 548M · F38RevScorecard 548M · F38SentinelBattery 548M ·
F38TipReceipts 548M · F38XMutP 548M · L1 3.7G.
(An earlier snapshot, 03:13, listed F38C2Rerun 1.7G and F38TipReceipts 1.1G and no F38CritTags/RevScorecard/SentinelBattery — the set is churning.)

Liveness: `ps -eo pid,etimes,cmd | grep -E 'kengaku-r38|F38'` shows live python/git/bwrap/clone processes in F38TipReceipts, F38C1Rerun,
F38CritBatD/E, F38C1RerunPy313, F38CritTags (clone in progress), F38CritSeparability, L1 (`round37_c1_attribution.py --work .../L1/attr/w`);
newest-file mtimes of every non-empty dir are 03:10–03:14, i.e. all are seats' in-flight scratch, not abandoned. Peer roster shows
F38RevBatB/C, F38CritSkipControls, F38MapV7Control, F38MutC2Counter, F38NoHarmSweep etc. still running. Only F38CritOverclaim
(0 bytes, newest mtime none, dir 03:11) is an empty shell with no files. None of these is deletable by this seat; each seat's own
`trap rm -rf` / the closer is owed the removal. At the instant of this sweep, leftover-owed = all 22 dirs (20G) by count; strictly
orphaned (no live process, no files) = 1 (F38CritOverclaim).

Residual disk fact: `.ufo/state/disk-guard.log` at 02:31 showed `/tmp` 89% use (soft 70%) — /tmp pressure is pre-existing and not caused by kengaku r38 (the r38 strays in /tmp are tsukuroi's two 01:08 files).

VERDICT: misroot-0-scratch-leftovers-22
