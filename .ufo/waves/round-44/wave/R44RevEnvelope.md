# R44RevEnvelope — independent blind-spot review of `.ufo/waves/round-44/claims/envelope.sh`

Reviewer seat R44RevEnvelope, 2026-10-26. Independent of any draft. All experiments in scratch
`S=/fast/scratch/hyaku/kengaku-r44/R44RevEnvelope`, envelope dir `$S/env`, receipts in
`.ufo/waves/round-44/wave/R44RevEnvelope/` (r1…r5b, baselines, `envelope-replica.sh`; total 7.6 KB, all < 1 MiB).
`envelope.sh` sits inside the frozen `claims/` dir — every mitigation below is advisory for a future revision, not a change proposal.

## Method

- Baseline: exact `bindigest` pipeline over the real `~/.local/bin` → `328be01808ba022f2317013b43f4af51e49dd440be37639b36c7e3c6b6284436` (`baseline-full-digest.txt`); demo target `codex` (1611 B, sha256 `b7441f44a1a3c263960c4312ec9970eb5caf70cdce0d4b9c62cd7e88c356ceaa`, link-count 1, mode 755, no ACL, no xattrs — `baseline-codex.txt`).
- Six real runs under the frozen `envelope.sh` (ENVELOPE lines quoted per finding).
- Where mount topology makes a real-dir attack impossible (hardlink alias, in-window mutation of the guarded dir), the same digest logic is demonstrated on a replica tree in scratch via `envelope-replica.sh` — byte-identical copy of `envelope.sh` with ONE delta, `cd /home/vgpnk/.local/bin` → `cd "${RDBIN:-/home/vgpnk/.local/bin}"` (file in receipts dir, diff stated here).

## Findings (by severity)

### B1 — HIGH: TOCTOU between before/after digests (mutate-and-restore keeps the measurement valid)
`bindigest` samples only before and after the command. Any change reverted inside the window is invisible.
Real-dir version is blocked today (see B4); demonstrated with the one-delta replica envelope on `$S/replica/bin`:

```
ENVELOPE start 20:44:23 cwd=/fast/scratch/hyaku/kengaku-r44/R44RevEnvelope
inner restored rc=0
ENVELOPE end 20:44:23 exit=0 local_bin_content_before=57270edc3fc222c5 after=57270edc3fc222c5 unchanged
```

while the mid-window snapshot (`race-mid.txt`, `r3-race.txt`) reads `pwned 20:44:23` — `cmp` vs the original:
`differ: char 1, line 1`. The guarded file really was overwritten during the measured window, and the run still reports
`unchanged`/exit 0. The positive control (change left in place) does flip the digest: replica flat `267a354dc90a1a0b` →
content-pwned `fcb63a205a8f8b0b` — so the guard catches only changes that survive past the window.

### B2 — HIGH: unpoliced writable host surface — /fast/scratch (incl. the round root), /tmp, /var/tmp, /dev/shm
`--dev-bind / /` leaves everything outside `/home/vgpnk` writable, and the digest watches only `~/.local/bin`.
Real run (`r4-scratch-writes.txt`):

```
ENVELOPE start 20:43:46 cwd=/fast/scratch/hyaku/kengaku-r44/R44RevEnvelope
inner: wrote decoy-sibling/owned.txt, /tmp probe, /var/tmp probe
ENVELOPE end 20:43:48 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

All three files existed on the host after the run (`decoy-sibling/owned.txt`, `/tmp/r44-env-probe-R44RevEnvelope`,
`/var/tmp/r44-env-probe-R44RevEnvelope`; removed afterwards). `test -w` inside: `/tmp /var/tmp /dev/shm
/fast/scratch/hyaku/kengaku-r44` all `yes`; a run can create new dirs beside sibling seats' scratch. Measured limit:
`/usr/local/bin` and `/etc` are `no` for uid 1000 — the round-40 shim-in-PATH-dir scenario does not extend to system
PATH dirs for an unprivileged run.

### B3 — MEDIUM: ~/.cache overlay writes survive the run and contaminate later runs sharing the env dir
The overlay target `$SCR/home-cache` is never inspected, rotated, or wiped. Run A planted files (`r5a-cache-plant.txt`,
exit=0, unchanged); immediately after, on the host: `$S/env/home-cache/evil/{marker,poison.sh}` present, while the real
`/home/vgpnk/.cache/evil` does not exist (overlay isolation confirmed). Run B — a different, later measurement reusing
`$S/env` (`r5b-cache-reuse.txt`):

```
ENVELOPE start 20:44:24 …
run-B sees marker: planted-by-run-A 20:43:46
run-B executes planted script:
poisoned-from-cache-overlay
ENVELOPE end 20:44:26 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

A run can leave state that changes a later run's behavior while the later run still counts as clean.

### B4 — MEDIUM: hardlink aliasing is invisible to the digest — blocked only by mount topology, not by design
The digest covers `{name, type, symlink-target, content}` of top-level entries; hardlink counts and aliases created
outside the dir are unwatched. Replica: after `ln bin/tool outside/alias` the digest is byte-identical
(`flat=267a354dc90a1a0b`, `hardlink-alias-outside=267a354dc90a1a0b`). On this host the real-dir attack fails by accident
of filesystem layout (`r2-errnos.txt`): `ln: failed to create hard link '/var/tmp/alias-vartmp' =>
'/home/vgpnk/.local/bin/codex': Invalid cross-device link` (`/home` st_dev 56; `/fast/scratch` 66309; `/var/tmp` 32).
If a uid-1000-writable same-fs directory ever appears inside the sandbox (mount reshuffle, envelope reuse on a
single-fs host), `link(2)` + write-through-alias becomes available, and with restore it degrades into B1.

### B5 — MEDIUM: ACL changes are never seen
Replica (`same digest pipeline`): `setfacl -m u:1000:rw bin/tool` applied — `getfacl` shows `user:vgpnk:rw-` + `mask::rwx`
— digest unchanged (`xattr+acl=267a354dc90a1a0b`). Real dir: refused only by the ro-bind
(`setfacl: …: Read-only file system`). Mode/owner/mtime are equally unwatched.

### B6 — MEDIUM: xattr changes are never seen
Replica: `setfattr -n user.p -v proof bin/tool` applied (`getfattr` shows `user.p="proof"` plus
`system.posix_acl_access`), digest unchanged (`xattr+acl=267a354dc90a1a0b`). Real dir: `setfattr: …: Read-only file
system`. A `security.capability`-class metadata change to a guarded binary would not trip INVALID.

### B7 — LOW: digest depth 1 — content of files inside subdirectories of ~/.local/bin is unhashed
`find -L -maxdepth 1 -type f`: replica nested copy `bin/sub/nested` rewritten `printf changed >` — digest identical
(`nested-before=nested-after=57270edc3fc222c5`). Latent: the real bin has 0 subdirectories today
(`find -mindepth 1 -maxdepth 1 -type d | wc -l` → 0); a future tool that creates `~/.local/bin/sub/` silently escapes
content hashing while only the `sub d` entry line is covered.

### B8 — LOW: no network isolation
No `--unshare-net`: `getent hosts github.com` inside the envelope → `dns-rc=0` (`r1-controls.txt`). A measured run can
phone home, pull instructions, or exfiltrate scratch content; the receipt carries no signal.

## Positive controls (what the envelope does catch, measured)

- Direct write/xattr/ACL on the real bin: `touch` → `Read-only file system`, `setfattr`/`setfacl` → `Read-only file system` (ro-bind holds).
- Left-in-place content change flips the digest (replica `fcb63a205a8f8b0b` ≠ `57270edc3fc222c5`); the CHANGED→exit 4 path is that logic.
- Name/type/symlink-target changes at top level are covered by the `%f %y %l` line.

## Minor structural notes (unnumbered)

- `date +%T` has 1-second resolution; window attribution in the receipt is coarse.
- `bindigest` swallows failures (`2>/dev/null`, `cd … || exit 0`): a failing hash pass reads as "unchanged".
- `--bind "$SCR" "$SCR"` would poke a writable hole through the ro-bind if a seat ever passed a `$SCR` under `/home/vgpnk`; current usage (scratch on /fast) is safe.
- `bindigest` hardcodes `/home/vgpnk`; fine today, but the `|| exit 0` fallback means a vanished dir hashes as empty-unchanged.

## Integrity after all probes

- Full `bindigest` recomputed: `328be01808ba022f2317013b43f4af51e49dd440be37639b36c7e3c6b6284436` — identical to baseline.
- `codex`: sha256 `b7441f44…`, `link-count=1 mode=755 size=1611` — matches baseline; no `__probe` file; no ACL/xattr residue.
- Host residue removed: `/tmp` and `/var/tmp` probe files deleted; overlay `evil/` dir deleted. `~/.local/bin` untouched throughout.

## Advisory mitigations for a future revision (envelope.sh is frozen this round)

1. Bind a fresh tmpfs over `~/.local/bin` inside the sandbox (`--tmpfs`) so in-run writes cannot reach the host inode at all; keep the before/after digest as belt.
2. Cover metadata and depth: add `stat -c '%n %h %a %U:%G'` per entry and recurse (drop `-maxdepth 1`), or `sha256sum` the whole tree.
3. Rotate the cache overlay: `mktemp -d` under `$SCR` for `home-cache` per run (or hash it into the receipt), so runs cannot influence each other.
4. Scope the writable surface: `--tmpfs /tmp --tmpfs /var/tmp --tmpfs /dev/shm`, and bind only `$SCR` (the seat's own dir) rather than `--dev-bind / /` + one ro-bind.
5. Add `--unshare-net` for payloads that need no network; treat its absence as a receipt flag otherwise.

## Residual risk / verification gaps

- No real-dir CHANGED→exit-4 run was performed (it would require actually modifying a host PATH file); the catch path is demonstrated on the replica and the refuse path on the real dir.
- EXDEV verified for `/fast/scratch` and `/var/tmp` alias targets; other mounts under `/` not enumerated exhaustively.
- Not tested: envelope killed mid-run (`--die-with-parent` cleanup), two envelopes running concurrently against the same digest.

VERDICT: envelope-blind-spots-8
