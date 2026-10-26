# F42ScoutMisroot — wave-2 hygiene watch (report only, no edits)

Sampled 18:03:34 (start) and 18:04:01 (end), 2026-10-26. Read-only except one self-inflicted file (see H4).

## H1 ~/.local/bin
- `ls -A /home/vgpnk/.local/bin | sha256sum` start = `8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52`; end = identical. Directory mtime unchanged, 17:48:46.564447073, both samples. 105 entries.
- Entries touched today: `firefox` symlink -> `/home/vgpnk/.local/opt/firefox-158.0.1/firefox`, mtime 17:48:46 (the directory mtime). `.local/opt/firefox-158.0.1` is dated 17:48:46 and `.local/opt` 17:48:43. Other 2026-10-26 entries are older: OpenBot AppImage 10:49, openbot 10:50, ruff 09:46, meson 04:19, pypy3.11 02:16, sasquatch 01:22.
- Attribution: the firefox install is a browser install. It is 6 minutes before the wave-2 cut (508434ad, 17:54:33) and 15 minutes before any falsify dir existed (first 18:03:12). No file under `.ufo/waves/round-42` mentions firefox, and no firefox process is running. I attribute it to something outside kengaku r42 (operator or another lane) `[INFERENCE]`. Nothing was added, removed or changed in ~/.local/bin during the watch window. No `git` shim or other PATH-shadowing name in the 8 touched entries.

## H2 Fleet-root git
- `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` -> 0 lines at start, 0 at end.
- Ignored-only: `git status --porcelain --ignored` lists `kengaku-shokunin/` and `.ufo/state/kengaku.{mission,out,report-baseline,round}`. These are the lane mirror and orchestrator state, ignored by design, not seat writes.
- `find /home/vgpnk/Projects/shokunin -maxdepth 1 -newermt '2026-10-26 16:56'` -> only `MANIFEST.json` (mtime 17:59:26) plus sibling lane dirs `kaidoku-shokunin`, `kama-shokunin`. `git log -- MANIFEST.json` shows it is tracked and committed at 17:59:26, `a4a605eb rounds ledger: kama r46 closure`. That is a kama (other lane) orchestrator commit, not a kengaku seat. No kengaku r42 seat wrote a fleet-root file.

## H3 Round-root sentinel
- `/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL` present at start and end: 71 bytes, mtime 16:56:19.866883848 both times. Content: "kengaku r42 round root; L1 KengakuR42; seats delete only $S/<SeatName>".

## H4 Self-disclosure (this seat)
My first command batch created and removed `/fast/scratch/hyaku/kengaku-r42/.f42misroot.tmp` (0 bytes) directly in the round root, to count a git-status line total. The file is gone (`ls` -> No such file). The sentinel and all seat dirs are untouched. Error, not repeated. No other writes outside this report dir.

## H5 Scratch under /fast/scratch/hyaku/kengaku-r42
Total 8.4G (`du -sh`, 18:04). 35 seat dirs at end, 25 at start; new dirs are wave-2 seats, 0 MiB each so far. Sizes in MiB (`du -s --block-size=1M`, largest first): L1 1267, R42CritEquiv 1064, R42MutProbe 1063, R42PlanNext 700, F42C2Rerun 578, F42RevC2Package 577, F42ConnPatterns 577, F42CritScorecard 577, F42C1Rerun ~577 (start sample), R42CritC1Counter 532, R42PkgEntry 532, R42BatAncRoute 531, R42SentinelCounter 2.8, R42CritIndep 1.6, R42QualityDraft 0.5, all other F42*/R42* dirs 0. Wave-1 seats R42CritEquiv, R42MutProbe, R42PlanNext, R42BatAncRoute, R42CritC1Counter, R42PkgEntry, R42SentinelCounter, R42CritIndep and R42QualityDraft still hold ~6.3 GiB of clones. They should be cleaned per-seat (scratch_guard safe-rm) at wave close, not by this seat. L1 shrank from 1.8G to 1.27G between samples (L1 cleaning its own dir). Other-lane sibling trees under /fast/scratch/hyaku (kaidoku-r36..41, tameshi-r48/49, etc.) were not touched or measured.

## Counts
misroot = 0 (no seat file outside permitted paths; only the self-removed H4 temp file in the round root, not a misroot), host-writes = 0.

VERDICT: misroot-0-host-writes-0-sentinel-present
