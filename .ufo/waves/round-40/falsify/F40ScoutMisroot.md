# F40ScoutMisroot — misroot / host-write sweep (kengaku r40 wave 2)

Swept 2026-10-26 14:26-14:28 -03, read-only (nothing deleted or edited outside this report).

## 1. Fleet-root status (misroot)
`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` (HEAD 751cc403, 13:55:36):
```
 M .scratch/goal-20261026-hyaku-run9.md
?? .ufo/reports/round-48/tameshi.md
```
- `.ufo/reports/round-48/tameshi.md` (mtime 14:23:39): `grep -iE 'kengaku|round[ -]?40|r40'` → 0 hits. It is a round-48 tameshi report, not kengaku r40. Not a misroot.
- `.scratch/goal-20261026-hyaku-run9.md`: diff is +18 lines and does name kengaku r40 (diff line 9: "Kengaku r40 critic seat `R40CritC1Counter` attacked the C1…"; line 18: "kengaku L1 was told at 14:12 never to run the modules on the host"). It is the orchestrator's own goal/incident log (tracked file, an incident write-up, not seat output). Counted as orchestrator-authored, not a seat misroot.
- No other fleet-root file (tracked or untracked) names kengaku round 40.
Seat misroot count = 0.

## 2. ~/.local/bin
`ls -la --time-style=full-iso /home/vgpnk/.local/bin` and `find /home/vgpnk/.local/bin -maxdepth 1 -newermt '2026-10-26 13:00'`:
- Only match: the directory itself, `/home/vgpnk/.local/bin` mtime `14:05:53` (type d). No regular file or symlink is newer than 13:00.
- Newest entries inside: `openbot` symlink 10:50:01, `OpenBot-0.50.0-x86_64.AppImage` 10:49:45, `ruff` 09:46:22, `meson` 04:19:49 (all pre-13:00, other work).
- `ls /home/vgpnk/.local/bin/git` → No such file. `which -a git` → `/usr/bin/git` only. No shim on PATH.
- The 14:05:53 directory mtime means an entry was created/removed then; that matches the known wave-1 crit git-shim incident (see goal-file note), and the shim is no longer present. I cannot name the writer from mtime alone [INFERENCE]. No residue now.
- Other PATH dirs: `find` over every PATH dir for entries newer than 13:00 returned only `.local/bin` itself.
Persistent host writes found = 0 (one transient dir-mtime trace at 14:05:53, residue-free).

## 3. systemd user / scheduled
`systemctl --user list-units --all --plain | grep -iE 'crit|run-|transient|.scope|.timer|kengaku|hyaku|r40|bwrap'`: no `crit-*`, `run-u*.service`, or transient units. Only app scopes (OnePassword, grok-bot, Hyprland apps, zcode) and timers `ai-usage.timer`, `cursor-shim-healthcheck.timer` (both pre-existing; units in `~/.config/systemd/user` dated Oct 16-19). `crontab`/`atq` not installed. No user unit file newer than 13:00 in `~/.config/systemd/user` (dir mtime 14:07 is a directory-level touch; no file listed at 13:/14: times).
Other 13:00+ writes in $HOME top-2 levels are unrelated app state (fcitx5, ai-usage, Grok Bot, .grokbot, .zcode, .npm/_logs, .gateguard) plus `/home/vgpnk/no-such-dir-xyz` (13:46:38, empty-path artifact, not kengaku-named). `/tmp/w5-mado-m52-selftest.BiDk40` is a mado lane tempdir (name match on "k40" is coincidental).
/usr/local and /etc: no files newer than 13:00.

## 4. Scratch under /fast/scratch/hyaku/kengaku-r40/
`ls -la`: 15 dirs (14 seat dirs + `L1`):
F40C1Rerun, F40C2Rerun, F40CritCounterLimits, F40CritNoHarmDiff (just `full.diff`), F40CritSkill, F40NoHarmC1, F40RevBatLRefuse, F40RevBatLRows, F40RevBatMan, F40RevBatOrder, F40RevBatRow, F40RevBatTok, F40RoundClose, F40SentinelBattery, L1 (orchestrator-L1 dir, 13:06-14:24 contents).
Processes with cwd under it (`/proc/*/cwd`): 3 in `F40C1Rerun` (the `bwrap … --ro-bind ~/.local/bin … --tmpfs /run/user/1000` wrapper form per ruling, plus two `plans/round40_c1_verify.py --lane . --work …/w1|w2` runs), 6 in `F40NoHarmC1`. Also nested `/usr/bin/bwrap … ledger.py` children of F40C1Rerun/w2 (battery's own inner sandbox) at sweep time. All are live seat runs (etime 34 s), not orphans; wrapping conforms to the host-safety rule.
Leftover count = 15 (dirs present now, all but L1 belong to seats still running per the roster; none is demonstrably abandoned yet; they must be removed by owners at exit, and L1 by the orchestrator).

## Summary
misroot=0 (orchestrator goal-file edit and round-48 tameshi file excluded as non-seat), host-writes=0 persistent (one residue-free `.local/bin` mtime at 14:05:53), scratch dirs present=15.

VERDICT: misroot-0-host-writes-0-scratch-left-15
