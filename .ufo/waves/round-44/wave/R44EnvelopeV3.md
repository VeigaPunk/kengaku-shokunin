# R44EnvelopeV3 — envelope v3: mode bits + stat-based records for unreadable entries

Seat: `R44EnvelopeV3` (executor, leaf), kengaku round 44 wave, 2026-10-26. Host-safety envelope used for every
counter/fixture/probe-shaped run below (host home read-only; `/home/vgpnk/.local/bin` never written, only read).
No tool installs (pacman paused host-wide; nothing needed: python3 3.14.8, bwrap, sha256sum, setfattr, shellcheck
0.11.0 already present). Scratch: `/fast/scratch/hyaku/kengaku-r44/R44EnvelopeV3` (deleted at the end).

**Routed finding under fix** (`round-43/build/R43ReviewEnvelope.md`, findings 1–2): the round-43 envelope's digest
(`find -printf '%f %y %l'` + `sha256sum` of regular files) (a) has no mode bits, so a mode-only `chmod` passes as
`unchanged`, and (b) suppresses `sha256sum` failures, so an entry at mode 000 contributes no content line and a
rewrite of it (mode restored afterwards) passes as `unchanged`. Reproduction against the round-43 script is M4 and
M5 in §3 below: `unchanged`, `rc=0`, on both.

## 1. Artifact

| what | path | sha256 | lines / bytes |
|---|---|---|---|
| **draft** (the deliverable) | `.ufo/waves/round-44/wave/R44EnvelopeV3/envelope.sh` | `a6799827b6805976dd5df0c3cec53010766dc9f5c7222accd22b22b7fc0b00b9` | 154 / 6613, mode 755 |
| consolidated evidence (all tables of this report) | `.../R44EnvelopeV3/envelope-v3-tests.txt` | `f51bfc60347b9bd49d08078353b3acfa44f29d7e3e0208fef0b8c29ec3dea242` | 8023 bytes, sections A–H |
| red/green driver (exact harness) | `.../R44EnvelopeV3/envelope-v3-driver.sh` | `6e5b4d8b2909a041b582cee9a25e8537cd3e562c1c9c511ebf6076d43a564e05` | |
| consolidated-evidence generator | `.../R44EnvelopeV3/envelope-v3-summarize.py` | `8d06dfa50c6d88e577971f5036797fd63891398fbdcd1fbb9396d74968cf6cf1` | |

Comparators: `claims/envelope.sh` (frozen, untouched — sha256 `2a484c28d5dabe45fce8d2309c6c719b0380982f5592a72848c99fe13e8912ab`,
mtime `2026-10-26 20:14:37`, i.e. before this seat started) and an **old copy with exactly one token remapped**
(sha256 `28e9904fcd42e5f12d14aaf1c2e48600a404b29f05ec294cfbd46d4833b6d127`):

```
--- claims/envelope.sh	2026-10-26 20:14:37
+++ $S/envelope-old.sh	2026-10-26 20:36:51
@@ -12,7 +12,7 @@
 bindigest() {
-  ( cd /home/vgpnk/.local/bin 2>/dev/null || exit 0
+  ( cd "${ENVELOPE_BINDIR:-/home/vgpnk/.local/bin}" 2>/dev/null || exit 0
```

so both scripts watch the same scratch fixture and neither test touches the host PATH dir. `diff` of the two
`ENV=(...)` bwrap arrays: identical (`BWRAP_ARGS_IDENTICAL`). `bash -n` clean; `shellcheck -S warning` clean (0.11.0).

## 2. What v3 does

`digest_body()` replaces `find | sha256sum`: `python3 -I - "$BINDIR"` (isolated: no PYTHONPATH/site hooks) walks the
watched tree depth-first, sorted, **without following symlinks**, and writes one tab-separated line per entry:

```
<path> <d|f|l|p|s|b|c> <perm bits, 4 octal> <nlink> <size> <mtime_ns> <ctime_ns> <ino> <link target|-> <xattr digest|-> <content sha256|unreadable:<errno>|n/a>
```

plus a header line `envelope-digest v3 root=<realpath> link=<target|-> ino=<ino> mode=<mode>`. Paths, link targets
and the root are JSON-quoted, so a name containing a tab or newline cannot forge a column (E1–E3). Xattrs are read
with `os.listxattr/getxattr(follow_symlinks=False)` and folded into one sha256 per entry. A regular file that cannot
be opened contributes `unreadable:<errno>` while its stat fields stay in the line — that is the F2 fix: an
unprivileged rewrite of a mode-000 file cannot restore `ctime`, and a rename-replace cannot restore `ino`.

Control flow: `before=$(snapshot)` → command inside bwrap → `after=$(snapshot)`; `unchanged` ⇒ command's rc
propagates; `CHANGED` ⇒ `ENVELOPE measurement INVALID (PATH dir content changed while it ran)` and **exit 4**; a
snapshot that cannot be taken (missing python3, watched path present but not a directory, python error) also prints
`INVALID (digest could not be taken: before_rc=… after_rc=…)` and exits 4 instead of silently digesting to equal
values. A watched path that does not exist at all digests as `absent` (round-43 parity: no tree, no change).

Receipt format is forward compatible with every pasted envelope line in round 43/44: the four lines keep their
shape; the start line gains `bindir=<resolved> digest=v3` (so a redirected watch is visible in the receipt).

## 3. Red/green — the six routed mutations (each on a fresh fixture, mutation executed *inside* the envelope)

Fixture per case: `real-tool` f755, `plain` f644, `secret` f000, `link-tool -> real-tool`, `sub/inner`, broken
symlink, self-loop symlink, dir-symlink, fifo. Command: `envelope.sh <scr> /bin/sh -c "cd <fixture> && <mutation>"`.

| # | mutation | v3 | round-43 (`old`) |
|---|---|---|---|
| M1 | `printf evil > real-tool` (content rewrite) | **CHANGED, rc=4** | CHANGED, rc=4 |
| M2 | `printf planted > planted-tool` (new file) | **CHANGED, rc=4** | CHANGED, rc=4 |
| M3 | `ln -sfn other-target link-tool` (symlink retarget) | **CHANGED, rc=4** | CHANGED, rc=4 |
| M4 | `chmod 700 plain` (mode-only, same bytes) | **CHANGED, rc=4** | `unchanged`, rc=0 — **missed** |
| M5 | `chmod 600 secret; printf stolen-secret > secret; chmod 000 secret` | **CHANGED, rc=4** | `unchanged`, rc=0 — **missed** |
| M6 | `setfattr -n user.tag -v evil real-tool` (xattr) | **CHANGED, rc=4** | `unchanged`, rc=0 — **missed** |

**v3 6/6, old 3/6.** Verbatim receipt lines for the three new detections (and their old counterparts, same run):

```
M4 v3   ENVELOPE end 20:40:36 exit=0 local_bin_content_before=4898e1dfa5d305f9 after=738683b3d89b0b59 CHANGED
        ENVELOPE measurement INVALID (PATH dir content changed while it ran)                              RC=4
M4 old  ENVELOPE end 20:40:36 exit=0 local_bin_content_before=f32130924e0ec7e7 after=f32130924e0ec7e7 unchanged  RC=0
M5 v3   ENVELOPE end 20:40:36 exit=0 local_bin_content_before=c6f2bdd3e2166a7e after=28841e67634b34f3 CHANGED
        ENVELOPE measurement INVALID (PATH dir content changed while it ran)                              RC=4
M5 old  ENVELOPE end 20:40:36 exit=0 local_bin_content_before=f32130924e0ec7e7 after=f32130924e0ec7e7 unchanged  RC=0
M6 v3   ENVELOPE end 20:40:36 exit=0 local_bin_content_before=ecc0545358781317 after=9c55a6994e4971d6 CHANGED
        ENVELOPE measurement INVALID (PATH dir content changed while it ran)                              RC=4
M6 old  ENVELOPE end 20:40:36 exit=0 local_bin_content_before=f32130924e0ec7e7 after=f32130924e0ec7e7 unchanged  RC=0
```

(M1/M2/M3 both scripts: `CHANGED` + `INVALID`, `RC=4`; v3 `c1206c500a2dddbd → 9ce64366bcfb160b`, `a06f59c742568c77 →
bf122dcf8f233dae`, `7bba3b94cbdf3826 → bf6f903950eacfb6`; old `f32130924e0ec7e7 → b1775135a8eae19c`,
`→ 002eea4753ad79ab`, `→ c15d100570646812`. The M-numbered v3 digests differ per case because each case gets a fresh
fixture with its own inodes/mtimes — the per-case *before → after* inequality is the measurement.)

Digest body for the M4 fixture (abridged: the `nlink/size/mtime_ns/ctime_ns/ino` columns are elided as `…`), showing
the mode-only flip on `plain` (content sha unchanged, mode `0700`) and the F2 record for the unreadable entry — the
full, unabridged body is `envelope-v3-tests.txt` §F:

```
"."          d 0755 3 131 … 1554372708 -  - n/a
"plain"      f 0700 1 13  … c246aa90bb31f55ab8b1b15706988aa920b6aeb4fc286c25d28dedc4bb666689
"secret"     f 0000 1 13  … -  - unreadable:Permission_denied
"link-tool"  l 0777 1 9   … "real-tool" - n/a
```

## 4. Negatives (nothing may fire) and v3-only extras

| control | expectation | result |
|---|---|---|
| rich fixture, no mutation (`/bin/true`) | whole digest equal | `unchanged`, rc=0 (`nc-repeat`) |
| rich fixture, `/bin/false` | rc must propagate | `exit=1 … unchanged`, rc=1 (`nc-exit`) |
| watched dir missing | old parity (`cd` fails) | `absent`, `unchanged`, rc=0 (`nc-absent`) |
| watched path is a symlink to a dir | works, link recorded | `unchanged`, rc=0 (`nc-symlinkroot`) |
| watched path is a **regular file** | loud, not silent | `DIGEST-ERROR rc=3` + `INVALID (… before_rc=1 after_rc=1)`, **rc=4** (`nc-file`) |
| watched symlink retargeted at a **byte-identical tree** | detected via header `link`/`ino` | `CHANGED`, rc=4 (`m7`) |
| broken link / self-loop / dir-symlink / fifo / mode-000 in the tree | no false positive | all of the above runs: no spurious `CHANGED` |
| names with tab / newline, two consecutive runs | deterministic, single-line | `before=after=fb9a899f818ba4ba`, rc=0 twice (E1, E2); rename → `CHANGED` (E3) |
| same bytes rewritten, `mtime` restored with `touch -d` | ctime moves ⇒ detected | `CHANGED`, rc=4 (E4) |
| digest tool missing (copy with `python3`→`python3-not-installed`) | loud INVALID | `DIGEST-ERROR rc=127`, `INVALID (… before_rc=1 after_rc=1)`, **rc=4** (E5) |

Extras beyond the six (v3 only, old missed both): **M8** new file nested under an existing subdir — v3 `CHANGED`
rc=4, old `unchanged` rc=0 (old was `-maxdepth 1`); **M9** mode flip of the watched dir itself — v3 `CHANGED` rc=4,
old `unchanged` rc=0.

## 5. The real watched dir, and cost

```
v3   ENVELOPE start 20:40:37 cwd=/home/vgpnk/Projects/shokunin bindir=/home/vgpnk/.local/bin digest=v3
     ENVELOPE end   20:40:38 exit=0 local_bin_content_before=e88c927bbd88b433 after=e88c927bbd88b433 unchanged
     wall 2252 ms (102 entries, 2.3 GB hashed)
old  ENVELOPE end   20:40:41 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
     wall 3029 ms
```

v3 is *faster* than the round-43 digest (one python walk instead of two `find`s + `sha256sum` + `sort | xargs`).
The watched dir was **not** written during this seat's window: `find /home/vgpnk/.local/bin -mindepth 1 -maxdepth 1
-newermt '2026-10-26 20:30'` prints nothing and the dir's own mtime/ctime is `18:10:45` (before the window). Digest
values observed on that dir across revisions of the draft, therefore, are *field-set* changes, not host activity:

| when | short digest | draft revision |
|---|---|---|
| 20:37:25 | `9dcabb123966a4ed` | A — no root/link header line |
| 20:38:21 | `00b8344389781596` | B — + root/link header, 4-digit mode, non-directory check |
| 20:39:38, 20:40:37, 20:40:41, 20:42:10, 20:42:14 | `e88c927bbd88b433` | C/D — + escaped labels (C) and comment-only (D) |

Determinism of the final revision: three body-level snapshots byte-identical (`sha256sum` first 16 = `e88c927bbd88b433`;
`cmp` equal, `BODY_IDENTICAL_3_RUNS`) and two envelope runs 4 s apart both `before=after=e88c927bbd88b433`
(`envelope-v3-tests.txt` §G). A live host write during a bracketed run *would* trip `CHANGED` — that is the design;
none occurred here.

## 6. Operability / integration notes for the L1

- **Do not edit `claims/envelope.sh`.** `claims/` is frozen for round 44, and 18 existing receipt files there carry
  24 `local_bin_content` lines, every one `328be01808ba022f` (the round-43 algorithm). Land this as a **new** file — e.g.
  `claims/envelope-v3.sh` — used for runs from now on; the frozen receipts stay reproducible against the frozen
  script.
- **Digest values are not comparable across versions.** `328be01808ba022f` (round 43) and `e88c927bbd88b433` (v3)
  digest different field sets by design; only `before == after` inside one run is a statement. Reviewers comparing a
  v3 receipt with a round-43 one must not read the value difference as a mutation.
- Invocation is unchanged: `envelope.sh <scratch dir> <command...>`, stdout is the receipt; same line shape as
  before (`ENVELOPE <bwrap argv> -- …`, `ENVELOPE start …`, `ENVELOPE end … exit=… local_bin_content_before=… after=…
  <unchanged|CHANGED>` `[`, `ENVELOPE measurement INVALID …`]`), exit 4 on change, command rc propagated only when
  unchanged.
- New tokens on the start line: `bindir=<resolved path> digest=v3`. `ENVELOPE_BINDIR` (default
  `/home/vgpnk/.local/bin`) exists so the guard can be rehearsed against a scratch tree; because the resolved path is
  printed in every receipt, a redirected watch is visible where it is pasted.
- Dependencies: `python3` (3.14.8 here), GNU `sha256sum`, `cut`, `bwrap`, `date`. Cost ≈ 2.2 s per run on this
  `~/.local/bin` warm (≈3.0 s for the old script); cold page cache is the dominant term.
- The script creates only `$SCR/home-cache`; it never writes the watched tree (all opens are `O_RDONLY|O_NOFOLLOW`).

## 7. Limits (named, not fixed)

1. **TOCTOU inside one run** — a mutation made and reverted between the two snapshots is invisible (same as round
   43). v3 narrows the window only by being one pass instead of four.
2. **Unreadable content is not hashed.** A mode-000 entry is covered by mode/nlink/size/mtime/ctime/ino, i.e. a
   rewrite by an unprivileged actor is always visible (ctime cannot be set back), but a root actor that writes the
   file and forges `mtime` can only be caught if `size` or `ino` also moves. Full content coverage of mode-000 files
   needs a privileged digest pass, which the envelope must not have.
3. **`absent`** watched path digests as `absent` both sides: creating and deleting the watched dir inside one run is
   invisible (round-43 parity).
4. **xattr coverage is filesystem-dependent** (xfs here; `user.*` on the fixture and inside bwrap both worked). On a
   fs without xattrs every entry shows `-` and an xattr change is invisible; the digest stays deterministic.
5. **Digest drift under fleet activity** — any authorized `uv`/binary install into `~/.local/bin` during a bracketed
   run trips `CHANGED` ⇒ `INVALID`. Correct, but it costs a re-run; none happened in this seat's window (§5), and a
   digest value is only meaningful within one revision of the script.
6. **Pathological trees** cost linear time in bytes (2.3 GB → 2.2 s); a huge tree would make the guard slow, not
   wrong. No depth cap (`sys` recursion is not used; the walk is an explicit stack), so deep trees neither crash nor
   truncate.
7. Tested on the draft itself (byte-identical to the tested copy; the fixture redirection uses `ENVELOPE_BINDIR`, not
   a patched copy) and on the one-token-remapped old copy — the remap is quoted in §1.

## 8. Safety / hygiene

- `~/.local/bin` and every other PATH dir: **read only**. Every envelope invocation in the receipt set (26 driver
  runs + 5 extras + 2 determinism runs, plus the smoke runs) printed identical `local_bin_content_before`/`after`;
  the two runs that name the real dir are quoted in §5. Mutations ran against `$S/...` scratch fixtures only.
- No `pacman`, no installs, no host service changes, no writes outside
  `.ufo/waves/round-44/wave/R44EnvelopeV3/` and `/fast/scratch/hyaku/kengaku-r44/R44EnvelopeV3`. No git/jj mutation
  anywhere (no clone was needed: every fixture is a plain directory under scratch).
- Scratch deleted with `python3 plans/scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r44 R44EnvelopeV3 "$S"`
  (result quoted in the seat result); `/fast/scratch/hyaku/kengaku-r44`, its sentinel and sibling seats untouched.

## 9. Reproduce

```
S=/fast/scratch/hyaku/kengaku-r44/R44EnvelopeV3; mkdir -p "$S"; export TMPDIR="$S"
cp .ufo/waves/round-44/claims/envelope.sh "$S/envelope-old.sh"
sed -i 's#cd /home/vgpnk/\.local/bin 2>/dev/null#cd "${ENVELOPE_BINDIR:-/home/vgpnk/.local/bin}" 2>/dev/null#' "$S/envelope-old.sh"
bash .ufo/waves/round-44/wave/R44EnvelopeV3/envelope-v3-driver.sh "$S" \
     .ufo/waves/round-44/wave/R44EnvelopeV3/envelope.sh "$S/envelope-old.sh"
python3 -I - "$S" .ufo/waves/round-44/wave/R44EnvelopeV3/envelope.sh "$S/envelope-old.sh" \
     < .ufo/waves/round-44/wave/R44EnvelopeV3/envelope-v3-summarize.py
```

VERDICT: envelope-v3-detects-6/6-old-3/6
