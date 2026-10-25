# FMisroot — fleet-root misroot check, round 27 falsify

Seat KengakuR27.FMisroot · read-only on fleet/driver state · Installs: none · 2026-10-21 ~09:40-03:00.
Scope: fleet-root `git status --porcelain`, untracked round27 kengaku-shaped files only. No lanes/driver runtime files touched.

## 1. Baseline used (path note for L1)
Falsify prompt cites lane-relative `build/ScoutFleetMisrootBaseline.md` — that path does not exist
(`read` → `Path '/home/vgpnk/Projects/shokunin/kengaku-shokunin/build/ScoutFleetMisrootBaseline.md' not found`;
lane has no `build/` dir). Actual baseline: `.ufo/waves/round-27/build/ScoutFleetMisrootBaseline.md`
(snapshot 2026-10-21T08:44:20-03:00, HEAD `1d07606`, 11 ` M` paths, 0 `??`). Compared against it.

## 2. Current porcelain
Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 --untracked-files=all` → EXIT=0.
Untracked (`??`): 0 (twice: plain `--porcelain` and `-uall`). Modified (` M`): 13.
Baseline had 11. Delta = 2 new modified paths, both tracked driver runtime, neither kengaku-named:
- `.ufo/l0-questions.md` — mtime 2026-10-21 09:36:41.37 -0300.
- `.ufo/state/tsukuroi.report-baseline` — mtime 09:32:29.01; content `21 e3b0c442…b855` (lane counter bump 20→21 class, same empty-SHA-256 marker as baseline §1).
Remaining 11 paths identical to baseline set (10 `.ufo/state/*.report-baseline` incl. kengaku + `.ufo/watchdog.log`).

## 3. Tripwire checks (baseline §6)
- New `??` at fleet root: NONE. Trip `?? .ufo/waves/round-27/`: absent
  (`ls -d .ufo/waves/round-27*` → "No such file or directory"; `git ls-files -- '.ufo/waves/round-27*' | wc -l` = 0;
  `git status --porcelain -uall -- .ufo/waves/` → empty, EXIT=0). Fleet `.ufo/waves/` holds rounds 1–25, 89, train dirs only.
- `.ufo/state/kengaku.*` beyond 26→27: NO. `cat .ufo/state/kengaku.report-baseline` →
  `27 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (still round 27).
- watchdog.log now 594 lines (baseline ended :591); latest `launch kengaku` line still `.ufo/watchdog.log:590`
  `2026-10-21T08:32:02-03:00 launch kengaku round=27 pgid=4193025 driver=hyaku-inline attempt=1`. No round=28 line.
- HEAD moved `1d07606` → `a28c80c` (2026-10-21T09:33:08-03:00, "round-21: kama late wave evidence appendix") — driver commit; runtime-file class, no kengaku path in the porcelain delta.

## 4. Ignored stray trees (baseline §4 recheck — not porcelain-visible)
- `bash: ` and `tameshi-shokukin/` both still exist at fleet root (`ls -d` OK).
- `git check-ignore -v 'bash: ' 'tameshi-shokukin'` → no output, EXIT=1: the top dirs match no rule.
  Consistent with baseline: they are invisible to normal porcelain because their contents sit under
  `*-shokunin/` (`.gitignore:1`), surfacing only as `!!` under `--ignored`. No kengaku-named content claimed
  there at baseline; nothing new surfaced (still 0 `??`).
- Consequence kept: `kengaku-shokunin/` itself is ignored by the same rule, so wave/falsify writes inside the
  lane can never misroot onto fleet porcelain. Scope of this check = fleet root only, per assignment.

## 5. Misroot findings
Untracked round27 kengaku-shaped files at fleet root: **none** (0 `??` anywhere at fleet root).
No file for L1 to relocate. The 2 new ` M` paths are driver-owned tracked runtime files
(tsukuroi counter bump, l0-questions refresh); outside my write scope, listed in §2 for L1's delta record only.

VERDICT: no misroot — fleet root holds 0 untracked files (round27 kengaku-shaped or otherwise), the kengaku
counter stays at round 27 with no launch line beyond watchdog.log:590, and the only porcelain change since the
08:44:20 baseline is two driver-runtime tracked files. Baseline confirmed accurate; its stray-tree and
ignore-rule claims re-verified. Baseline path in the falsify prompt is stale (actual: `.ufo/waves/round-27/build/ScoutFleetMisrootBaseline.md`) — relocation is L1's call.
Installs: none.
