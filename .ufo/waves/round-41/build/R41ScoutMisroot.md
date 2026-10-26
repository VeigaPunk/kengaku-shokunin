# R41ScoutMisroot — host-safety and hygiene watch (kengaku r41 wave 1)

Read-only scout. Wrote only this file. No timestamped writes outside report dir/scratch (none).

## 1. ~/.local/bin (round-40 closure R2)
Start 15:41:14, end 15:41:29 (same shell session, ~15 s apart; this is a snapshot window, not the whole wave).
- Directory mtime, start: `2026-10-26 14:05:53.386453172 -0300 /home/vgpnk/.local/bin`; end: identical. **No change in window.**
- `ls -la --time-style=full-iso` sha256 start = end = `2cb8c423cc13af1eaf1ff4ddad2f4231d6c76cf681b22ef36b4ef2af3ad4953c` (100 entries both times).
- Entries newer than 2026-10-26 00:00 (all pre-wave, legitimate-looking installs): sasquatch/sasquatch-v4be 01:22:37, pypy3.11 02:16:40, meson 04:19:49, ruff 09:46:22 (-> uv tools), OpenBot AppImage 10:49:45, openbot 10:50:01. Dir mtime 14:05:53 = last entry add/remove (not identified by name; nothing newer than 10:50:01 remains, so it was a removal or a rename-over). Nothing after 10:51.
- No shim for `git`, `python`, `python3`, `bwrap`, `sh`, `bash`, `env` (`ls: cannot access`). `jj` is the real 31 MB binary dated 2026-10-03. No crit_git_shim residue.

## 2. Fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`
Output (start and end identical): `?? .ufo/reports/round-48/tameshi.md`. No tracked modifications.
- That file belongs to tameshi round 48 (header `# tameshi — round 48 report (attempt 3, L1 TameshiR48a3)`, mtime 14:23:39). grep for kengaku/round 41 in it: no match (exit 1).
- **No kengaku r41 file in the fleet root.**

## 3. Scratch /fast/scratch/hyaku/kengaku-r41 (all owner vgpnk; du -s at 15:41:29, total 6.6G; /fast 24% used, 612G free)
L1 838M · R41BatSrcModes 524M · R41CritC1Counter 524M · R41CritClaims 1713M · R41CritEquiv 527M · R41CritIndep 524M · R41CritProbe 1M · R41PkgEntry 1M · R41PkgProse 0 · R41PkgRows 1M · R41RegistryRows 537M · R41RevC2Counter 524M · R41RoutedRider 0 · R41ScoutPriorArt 3M · R41SentinelCounter 524M · R41SentinelProbe 524M.
- 16 dirs; none non-vgpnk (`find ... ! -user vgpnk` empty). Every seat dir is a clone (~524M) as the fixture rule prescribes; R41CritClaims is 1.7G (grew from 1.2G at 15:41:11, two clones). Seats must `rm -rf` on exit; I am not one (this scout used none).
- Not-a-r41 siblings under /fast/scratch/hyaku: kaidoku-r37..r40, kasegi-r38, mado-r45, souji-r31/33, tabi-r33, tameshi-r48, tsukuroi-r41 (other lanes; left alone).

## 4. /tmp
- No name matching `*kengaku*`, `*r41*`, `*round41*`, `*round-41*` under /tmp (depth<=3). No `/tmp/kengaku-r41`-style dir.
- Content scan (files <2M modified after 15:00, `kengaku|round 41|r41`) hit three loose files; none is clearly a kengaku seat product:
  - `/tmp/null` (178980 B, 15:08:17, vgpnk): a real FILE named `null`, i.e. a mis-typed `> /tmp/null` redirect by some seat (should be /dev/null). Content is a bash selftest with `round 41 (C1 ... H5,H6,H9,H10)` btrfs "healthy rollup" checks — that is another lane's (not kengaku's) round-41 text. Owner unidentified. Note: stale-risk — anything redirecting to `/tmp/null` appends to it.
  - `/tmp/ignore-arm.sh` (4298 B, 15:15:44): contains `R41DECOY` heredoc marker; a decoy test from some other lane's r41 work. Owner unidentified.
  - `/tmp/fleet_ruling_hits.txt` (503 KB, 15:19:33): grep of fleet LOG.md ("kengaku d8f2898 ..."), a fleet-wide search artifact, not r41-authored content.
- Other /tmp debris from non-kengaku seats today (for the orchestrator): 300 dirs `/tmp/w5-mado-m52-selftest.*` (mado, 12:34-12:35), tameshi-r14 selftest dirs (15:02-15:03, ~4 dirs x 70 cases), `/tmp/tameshi-r4-2-regression.MTXWG0` (15:41), sqfs-v2-* dirs (15:23-15:25), `/tmp/neg.3438`, `/tmp/p-*.txt`, `/tmp/tmpz096a8k8/a.sqsh`. These violate the scratch-under-/fast directive for whoever made them; not identifiably kengaku r41.
- Verdict for r41 kengaku seats: no `/tmp` path attributable to them found. Attribution of /tmp/null and /tmp/ignore-arm.sh is `[INFERENCE]`-level only (content names r41 but a different lane).

## 5. Host-writes count
Host-writes by kengaku r41 seats outside report dir/scratch: **0 confirmed** (bin dir unchanged, fleet root clean of r41 content, no r41-named /tmp path). 2 unattributed r41-text files in /tmp (`/tmp/null`, `/tmp/ignore-arm.sh`) flagged for owner lookup, not counted.

VERDICT: misroot-2-host-writes-0
