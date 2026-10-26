# F41ScoutMisroot — kengaku r41 wave 2 host-safety / hygiene watch

Read-only. Snapshot A 16:13:16, snapshot B 16:13:41 (-0300, 2026-10-26). Nothing created, edited or deleted except this report.

## 1. ~/.local/bin
- `stat -c '%y' /home/vgpnk/.local/bin` at A and at B: `2026-10-26 14:05:53.386453172 -0300` (unchanged; predates wave 2 and both rounds' falsify dispatch). Entry count at B: `ls -1 | wc -l` = 100.
- `find /home/vgpnk/.local/bin -maxdepth 1 -newermt '2026-10-26 12:00' -printf '%TT %p'` → only the dir itself (`14:05:53 /home/vgpnk/.local/bin`). No file/symlink in it is newer than 12:00.
- Shim check: `command -v git` = /usr/bin/git, `bwrap` = /usr/bin/bwrap, `python3` = /usr/bin/python3, `sh` = /usr/bin/sh. `jj` resolves to ~/.local/bin/jj (legitimate, dated earlier; not newer than 12:00). No `git` entry in ~/.local/bin (grep of listing for git/sh/python3/rm/bwrap/uv names: only `uv`, dated 10-09). No R40-style git shim.
- Verdict: 0 host writes to PATH dirs.

## 2. Fleet-root git status
`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` at A:
```
?? .ufo/reports/round-38/kasegi.md
?? .ufo/reports/round-48/tameshi.md
```
Filtered with `grep -iE 'kengaku|round-41|r41'`: empty. No tracked-file modifications. No kengaku r41 file untracked at fleet root. (Other-lane round-38/round-48 reports are not kengaku's.) Fleet-root files newer than 15:00 (LOG.md, SCORECARD.md 15:29; MANIFEST.json 15:57; kaidoku/tsukuroi dirs) are committed (absent from porcelain); the orchestrator's round-41 dirs/prompts are tracked.
Lane (`git -C kengaku-shokunin status --porcelain`): only `.ufo/waves/round-41/falsify.ready`, `falsify.ready.dispatched`, `falsify/swarm-registry.json` (orchestrator wave-2 bookkeeping, expected).

## 3. Scratch /fast/scratch/hyaku/kengaku-r41
Birth `2026-10-26 15:42:34`, mtime 16:13:27.
```
du -sh: F41C1Rerun 0, F41C2Rerun 0, F41CritNoHarmDiff 0, F41CritOverclaim 0, F41RevBatSrcModes 0, F41SentinelBattery 0 (all at A),
        L1 524M;  total at A not summed, at B `du -sh kengaku-r41` = 3.2G
```
(Growth to 3.2G between A and B = F41C1Rerun/F41C2Rerun counter runs building clones/work trees under their own seat dirs; live processes `round41_c1_verify.py --lane /fast/scratch/hyaku/kengaku-r41/F41C1Rerun/lane --work .../w1`, `round41_c2_verify.py --lane .../F41C2Rerun/lane` confirm.) No kengaku r41 scratch dir exists outside the round root (`ls -d /fast/scratch/*/kengaku* ...` → only the round root). L1 holds `c2int/{lane,w}` and `int1` (orchestrator integration leftovers, L1's to remove). Empty seat dirs are fresh wave-2 seats starting up.

## 4. /tmp
`ls /tmp | grep -iE 'kengaku|r41|hyaku|battery|ufo'` → empty. `grep -rIl 'kengaku-r41' /tmp` → empty. `find /tmp -maxdepth 2 -newermt '15:42'` shows only other work: `st.out/err`, `nw-gate.*`, `model_nightwire_orig.mjs`, `reruncensus-hashes.txt`, `ub*`, `mado-r36-mutants-r36/`, `tameshi-r4-2-regression.*`, `ecc-*`/`claude-tool-count-*` (harness), plus 300 `w5-mado-m52-selftest.*` dirs (13:22, mado's, left behind — mado hygiene, not kengaku). No /tmp path attributable to a kengaku r41 seat.

## 5. IPC
`ipcs` (A) and `ipcs -a | grep -c '^0x'` (B) = 0 message queues, 0 shared-memory segments, 0 semaphore arrays. No SysV residue. `/run/user/1000` listing: no kengaku-named entries (newest `tbs.tiGpKi` 15:23, other lane).

## 6. Wave-1 round-root deletion (15:42:24) — recurrence?
- Round root birth time = `15:42:34` (10 s after the 15:42:24 deletion cited in wave-1 reports, e.g. R41CritClaims.md "15:42:24 while I was working… I recreated `$S`"). Birth has not changed since; `L1` born 15:43:19; no seat dir older than that exists, consistent with a single deletion and no second one.
- At B all six wave-2 seat dirs present, round root present. No recurrence observed between A and B (25 s window); no `rm -rf` process on the round root (`ps | grep 'rm -rf'` → only a generic seat-timeout watchdog with `rm -rf -- "$tmpdir"` guarded to a seat's own tmpdir, parent already dead).
- Caveat [INFERENCE]: I can only see state from 16:13; a deletion between 15:43 and 16:13 followed by recreation would show as a later birth time, which it does not (15:42:34). Deletion cause remains unattributed in my evidence.

## 7. Live sandbox check
`ps` shows the F41C1Rerun/F41C2Rerun counter runs in `bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent …` — the mandated envelope — with inner `--unshare-net` sandboxes. Compliant.

## Summary
misroot findings: 0. host writes: 0 (PATH dirs unchanged; fleet root clean of kengaku r41 files; no /tmp or IPC residue from kengaku r41; no round-root deletion recurrence). Hygiene notes for L1 (not misroots): remove `/fast/scratch/hyaku/kengaku-r41/L1` (524M) at close; 300 mado `w5-mado-m52-selftest.*` dirs in /tmp belong to mado.

VERDICT: misroot-0-host-writes-0
