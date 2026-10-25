# ScoutFleetMisrootBaseline — fleet-root porcelain baseline, round 27

Seat KengakuR27.ScoutFleetMisrootBaseline · read-only · Installs: none · Snapshot 2026-10-21T08:44:20-03:00 · Scope: baseline only (C1/C2/sources builds not touched).

## 1. Porcelain result
Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 --untracked-files=all` → EXIT=0.
Untracked (`??`): 0. Modified (` M`): 11.
HEAD `1d07606` (08:42:21, protocol-shokunin, MANIFEST.json +69). Earlier HEAD `8bc70543c7eb` (08:39:30): HEAD moved during this scout. Index == HEAD (`git diff --cached --name-only` empty).

| mtime (-03:00) | path | delta | launch evidence (.ufo/watchdog.log) |
|---|---|---|---|
| 06:47:49.01 | .ufo/state/tabi.report-baseline | 19→20 | :582 (06:47:50) |
| 07:17:01.99 | .ufo/state/kama.report-baseline | 20→21 | :583 (07:17:03) |
| 07:18:04.16 | .ufo/state/mori.report-baseline | 19→20 | :584 (07:18:05) |
| 07:23:20.15 | .ufo/state/kagi.report-baseline | 24→25 | :585 (07:23:21) |
| 08:30:51.39 | .ufo/state/tameshi.report-baseline | 20→21 | :586 (08:30:53) |
| 08:31:56.15 | .ufo/state/kaidoku.report-baseline | 21→22 | :587 (08:31:57) |
| 08:31:57.72 | .ufo/state/kake.report-baseline | 23→24 | :588 (08:31:59) |
| 08:31:59.33 | .ufo/state/chousa.report-baseline | 25→26 | :589 (08:32:01) |
| 08:32:01.17 | **.ufo/state/kengaku.report-baseline** | **26→27 — FLAG** | :590 (08:32:02) |
| 08:33:48.85 | .ufo/state/souji.report-baseline | 20→21 | :591 (08:33:50) |
| 08:33:50.41 | .ufo/watchdog.log | +10 lines (582–591) | — |

Each state file is `N e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. That hash is SHA-256 of empty input (`printf '' | sha256sum`). [INFERENCE] It is an empty-report baseline marker.

## 2. Kengaku flag
- FLAG `.ufo/state/kengaku.report-baseline`: `26 e3b0…b855` → `27 e3b0…b855`. HEAD blob reads `26 …` (`git cat-file -p HEAD:.ufo/state/kengaku.report-baseline`).
- Explained, not misrooted: `.ufo/watchdog.log:590` `2026-10-21T08:32:02 launch kengaku round=27 pgid=4193025 driver=hyaku-inline attempt=1`.
- Pairing: 10 state bumps ↔ 10 launch lines, same lane and round, each bump 0.8–1.7 s before its launch. No orphan writes.
- Ignored kengaku path: `kengaku-shokunin/` (`git check-ignore -v`: `.gitignore:1 *-shokunin/`; dir mtime 2026-10-20 22:03:09). Expected; porcelain cannot see inside it.
- No lane-local `.ufo/state/` exists (glob skipped it as missing), so there is no competing baseline file.

## 3. Kengaku footprint, whole fleet tree (excluding .git and nested lanes)
- Files with "kengaku" in the name on disk: 67 (`find … -type f -iname '*kengaku*' | wc -l`). All 67 tracked.
- Breakdown: 55 lowercase (`git ls-files -- '*kengaku*'` = 57, minus run.json/spec.json which match via directory name) + 12 capitalized `Kengaku*` (`git ls-files -- '*Kengaku*'` = 13, incl. `.ufo/scopes/Shokunin12hP3Kengaku20261014/swarm-registry.json`).
- Untracked-not-ignored: 0. Ignored-untracked kengaku files: 0. Kengaku-named entries in the stray trees of section 4: 0.

## 4. Non-kengaku misroot-class items (ignored, so invisible to porcelain)
Blind spot: porcelain lists an untracked directory only if it holds a non-ignored file. Trees whose content sits under `*-shokunin/` (`.gitignore:1`) are hidden. Only `find`/glob exposes them.
- `bash: ` — literal fleet-root directory, mtime 2026-10-18 14:01:47. Its only content is `home/vgpnk/Projects/shokunin/souji-shokunin/` (porcelain: `!! "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/"`). 9 entries, 0 kengaku. Looks like a mis-quoted path that became a tree. Predates this round. Not touched.
- `tameshi-shokukin/` — typo'd parent, mtime 2026-10-21 02:50:33, nesting `tameshi-shokunin/` (mtime 2026-10-20 18:19:01; porcelain `!! tameshi-shokukin/tameshi-shokunin/`). 10 entries, 0 kengaku. Not touched.
- `reports/` — empty directory at fleet root, mtime 2026-10-18 13:05:53, 1 entry (itself). Git cannot track empty dirs. A misroot write there would surface as `?? reports/`.
- Fleet-root dir mtime 08:42:21.68 equals `MANIFEST.json` mtime (08:42:21.68), i.e. the atomic rewrite inside HEAD `1d07606`. Not a stray.
- `.git/` mtime 08:44:20.08 is a side effect of the assigned `git status` (index refresh) [INFERENCE]. No tracked content changed.

## 5. Baseline caveat
The snapshot postdates the kengaku launch (08:32:02) by 12 minutes, so it is not strictly pre-wave. The strict pre-launch baseline is HEAD `1d07606` with the 10 counters at HEAD values and `.ufo/watchdog.log` without lines 582–591. The 11-path porcelain delta equals exactly that launch burst.

## 6. Misroot tripwire for this round
Trip on any new `??` at fleet root (especially `?? .ufo/waves/round-27/`, `?? reports/`, or any kengaku-named entry), or on any change to `.ufo/state/kengaku.*` beyond 26→27. None observed at 08:44:20.

VERDICT: Fleet root is kengaku-clean: 0 untracked and one modified kengaku path (orchestrator round-27 counter, matched to watchdog.log:590). The misroot exposure is in ignored stray trees (`bash: `, `tameshi-shokukin/`), not in kengaku.
Installs: none.
