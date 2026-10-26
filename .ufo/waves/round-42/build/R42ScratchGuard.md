# R42ScratchGuard — scratch-root guard (round 42, wave 1)

Seat: `R42ScratchGuard` (executor). Lane read-only; draft for the L1 to integrate.
Round-41 closure **R2** / defect **D1** (`corpus/lessons/round-41-verifier-spotcheck.md:50` — "ran `rm -rf -- /fast/scratch/hyaku/kengaku-r41` (the shared round root)").

## What landed

| path | sha256 | bytes |
|---|---|---|
| `.ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py` | `f0360e3028c79ce32fcabf7f89f0103b88205200bce802a8b2520e1f9364aa5d` | 25643 |
| `.ufo/waves/round-42/build/R42ScratchGuard/mutate_selftest.py` (wave-1 falsifier, scratch-only driver) | `e6189f6babb9fd28b463a2b0763850d064cf3cddd1a48ae200a44fcd8981caf4` | 4023 |
| `.ufo/waves/round-42/build/R42ScratchGuard/RECEIPT.txt` (full outputs, Q32 lines) | `3cc3d5aa74d13603b4ebbeeac8f14eb9d667f08463f8775e9ff004edf0210b5f` | 9224 |

`scratch_guard.py` is stdlib only (`argparse, contextlib, io, json, os, re, shutil, stat, sys,
tempfile`), no subprocess, no network, no shell, no `/proc`, no `$HOME` read.

## Contract (as built)

| command | `0` | `1` | `2` |
|---|---|---|---|
| `check <root> [--round N] [--json]` | sentinel present and its text names the round (`kengaku r<NN> round root`); with `--round N` the named round equals N | sentinel missing, unparseable, or names another round | root is not a directory, or the sentinel cannot be read |
| `safe-rm <root> <seat> <path> [--dry-run]` | deleted, or `ABSENT` (idempotent; prints the absolute path and the seat anchor) | — | every refusal: root, sentinel, another seat, symlink escape, `..`, invalid/symlinked seat, missing seat, unguarded root, NUL/empty target, delete failed |
| `--selftest` | all 36 cases pass | at least one named case red (prints `SELFTEST failed=<names>`) | — |

Rules the delete leg enforces, in order: sentinel must name a round (`root-untrusted` otherwise);
the seat must be **one path component** (`seat-invalid`); `<root>/<seat>` must not be a symlink
(`seat-is-symlink`, so a link named after seat A can never delete seat B); any `..` component is
refused before resolution (`target-dotdot`); an **absolute** target must already be lexically at or
below the seat dir (`target-outside-seat`); the **resolved** target must be at or below the seat
dir (`target-resolves-outside-seat`) and must be neither the root (`target-is-root`) nor the
sentinel (`target-is-sentinel`). Only then is anything deleted, and `shutil.rmtree` never follows a
link while walking. A relative `<path>` is anchored to `<root>/<seat>`, never to the caller's cwd.

## Evidence

Envelope for every run (Q32):
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <cmd>`.
`ls -A /home/vgpnk/.local/bin | sha256sum` was `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18`
before and after all five runs; per-run times are in `RECEIPT.txt` §F.

### 1. `--selftest` — `SELFTEST ok=36/36`, exit 0 (`17:32:11 → 17:32:11`)

15 allow/check cases + 21 refusal cases; each refusal asserts (a) exit 2, (b) the expected
`reason=`, (c) the target still exists, (d) the target is **writable** (so only the guard stands
between it and deletion; the one exception is `refuse-fs-root`, where a non-root user cannot write
`/` at all and the case declares `expect_writable=False`), and (e) the same naive
`unlink`/`rmtree`/symlink-`unlink` **succeeds on a twin** at a legal path — i.e. each refusal is
shown able to fail, not vacuous. Full 36-line output in `RECEIPT.txt` §A; the verdict line is
`SELFTEST ok=36/36`.

### 2. The selftest can fail: 7/7 named mutants killed (`17:32:45 → 17:32:45`)

Each mutant removes exactly one named guard from a scratch copy (anchor asserted to occur once),
then the same `--selftest` runs. Control (unmutated) `exit=0 SELFTEST ok=36/36`.

| mutant (guard removed) | selftest cases that went red |
|---|---|
| `dotdot-removed` | `refuse-root-dot`, `refuse-dotdot-relative`, `refuse-dotdot-absolute` |
| `realpath-off` (no symlink resolution) | `refuse-symlink-file-escape`, `refuse-symlink-dir-escape`, `refuse-symlink-dir-rmtree`, `refuse-symlink-to-sentinel`, `refuse-symlink-to-root`, `refuse-seat-traversal` |
| `seat-symlink-ok` | `refuse-seat-symlink-root`, `refuse-seat-symlink-other`, `allow-unlink-inside-symlink` |
| `sentinel-branch-off` | `refuse-symlink-to-sentinel` |
| `root-branch-off` | `refuse-symlink-to-root` |
| `sentinel-optional` | `refuse-bare-root` |
| `containment-off` | `refuse-symlink-file-escape`, `refuse-symlink-dir-escape`, `refuse-symlink-dir-rmtree`, `refuse-seat-traversal` |

`MUTANTS total=7 killed=7 survived=0`, exit 0.

### 3. `check /fast/scratch/hyaku/kengaku-r42` — read-only, exit 0 (`17:31:46 → 17:31:47`)

```
ROOT /fast/scratch/hyaku/kengaku-r42
SENTINEL .ROUND-ROOT-SENTINEL round=42 bytes=71 text="kengaku r42 round root; L1 KengakuR42; seats delete only $S/<SeatName>"
SEAT L1 bytes=1766576265 size=1.6GiB
SEAT R42BatAncRoute bytes=525487716 size=501.1MiB
SEAT R42ConnFrontier bytes=0 size=0B
SEAT R42ConnPattern bytes=0 size=0B
SEAT R42CritC1Counter bytes=525595163 size=501.2MiB
SEAT R42CritClaims bytes=2101874810 size=2.0GiB
SEAT R42CritEquiv bytes=1051552176 size=1002.8MiB
SEAT R42CritIndep bytes=583595 size=569.9KiB
SEAT R42ExecNoHarm bytes=1576392266 size=1.5GiB
SEAT R42LessonDraft bytes=0 size=0B
SEAT R42MutC2Counter bytes=525200982 size=500.9MiB
SEAT R42MutProbe bytes=525664411 size=501.3MiB
SEAT R42PkgEntry bytes=525636510 size=501.3MiB
SEAT R42PlanNext bytes=525418386 size=501.1MiB
SEAT R42QualityDraft bytes=114756 size=112.1KiB
SEAT R42RevC2Counter bytes=525392577 size=501.1MiB
SEAT R42ScratchGuard bytes=212264 size=207.3KiB
SEAT R42SentinelCounter bytes=391165 size=382.0KiB
ROOTFILES n=1 names=.ROUND-ROOT-SENTINEL
TOTAL seats=18 bytes=10176093042 size=9.5GiB
CHECK ok round=42 want=* seats=18
```

Read-only demonstrated: sentinel sha256 `efc83fb9fc2eacbaca0225d3da8f72bd4865fcc93d70ff00377607dd944e66f2`
and the 18-entry listing are identical before and after. Sizes are apparent bytes (`lstat` sum),
not disk blocks; a symlinked seat is printed `symlink(not-walked)`.

### 4. Live behaviour on the real root (not a fixture)

```
DELETE path=/fast/scratch/hyaku/kengaku-r42/R42ScratchGuard/realdel resolved=…/R42ScratchGuard/realdel bytes=16 size=16B   exit=0
REFUSE reason=target-outside-seat seat=R42ScratchGuard … target=/fast/scratch/hyaku/kengaku-r42/R42ScoutPriorArt              exit=2
REFUSE reason=target-outside-seat seat=R42ScratchGuard … target=/fast/scratch/hyaku/kengaku-r42/.ROUND-ROOT-SENTINEL          exit=2
REFUSE reason=target-outside-seat seat=R42ScratchGuard … target=/fast/scratch/hyaku/kengaku-r42                                exit=2
SEATS_AFTER 18 sentinel_after=efc83fb9… (unchanged)
```

Operational note measured during this run: a **bare relative** name that is not inside the seat
(e.g. `safe-rm <root> R42ScratchGuard R42ScoutPriorArt`) resolves against the seat dir and prints
`ABSENT path=…/R42ScratchGuard/R42ScoutPriorArt seat_dir=…`, exit 0 — nothing is deleted, and the
printed absolute path shows the anchor. Absolute targets are the unambiguous form.

## Draft SKILL.md registry row (for the L1; not applied — SKILL.md is lane-owned)

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `scratch-root-guard` | gate | `python3 .ufo/waves/round-42/build/R42ScratchGuard/scratch_guard.py check <root> [--round N] [--json]` (gate leg, the L1 runs it before a measurement) and `… safe-rm <root> <seat> <path> [--dry-run]` (mutating leg, the only sanctioned delete) | `0` sentinel present and names the round (`safe-rm`: deleted or absent) · `1` sentinel missing, unparseable, or another round · `2` root not a directory, sentinel unreadable, or a refused delete (root, sentinel, another seat, symlink escape, `..`, invalid or symlinked seat, unguarded root) | `python3 …/scratch_guard.py --selftest` (36 cases on a throwaway root: 15 allow/check, 21 refusals, each refusal demonstrated writable and non-vacuous; 7/7 named mutants killed by `…/mutate_selftest.py`) | sentinel wording `kengaku r<NN> round root`; round-42 root sentinel sha256 `efc83fb9…`; no lane or corpus pin | `check` writes nothing; `safe-rm` deletes only at or below `<root>/<seat>`; selftest writes only under `$TMPDIR`; needs no sandbox but SHOULD run inside the Q32 envelope | kengaku |

Suggested wave-context sentence (R2's second half): *"Before any measurement run
`scratch_guard.py check /fast/scratch/hyaku/kengaku-r42 --round 42`; delete only with
`scratch_guard.py safe-rm /fast/scratch/hyaku/kengaku-r42 <YourSeatName> <path>`."*

Optional L1 edit (not made here): `integrate/measure.sh:9`'s
`grep -q 'kengaku r42 round root' "$R/.ROUND-ROOT-SENTINEL"` can become the same tool's
`check "$R" --round 42`, which also prints the seat sizes that seat `R42ScoutMisroot` reports.

## Limits (honest)

1. **It is a tool, not a kernel control.** It makes the sanctioned delete path unable to leave your
   seat and makes a missing sentinel detectable; it cannot stop a raw `rm -rf` in a shell. D1's root
   cause was an unguarded raw `rm`; the guard plus the L1's pre-measurement check is what R2 asked
   for, not an enforcement mechanism.
2. **TOCTOU.** The path is resolved with `realpath` and then deleted; a sibling that swaps a parent
   component for a symlink between those two calls could redirect the delete. The threat model is
   cooperative seats (the D1 case was an accident), not a hostile process.
3. `ABSENT` exits 0 by design so a cleanup trap is re-runnable; it never creates or deletes anything.
4. Sentinel matching is a regex on wording, not a digest; a seat that rewrites the sentinel text to
   another round number would be caught by `--round 42` only if the round differs.
5. `check` walks whole seat trees (9.5 GiB here in ~1 s); it does not hash or validate seat content.

## No-harm

Only three files were written, all under `.ufo/waves/round-42/build/R42ScratchGuard/`, plus this
report. No lane file (`corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`,
`PROVINCE.md`, `SHONEN.md`), no git/jj operation anywhere, nothing in `/home/vgpnk/.local/bin`
(listing hash unchanged), nothing in the fleet root, no other seat's directory. Scratch work stayed
in `/fast/scratch/hyaku/kengaku-r42/R42ScratchGuard`; the only deletions on the real root were
inside that seat — `realdel` (created by this seat for the demonstration) and finally the seat's own
scratch dir through the tool: `DELETE path=…/R42ScratchGuard resolved=…/R42ScratchGuard bytes=421081
size=411.2KiB`, exit 0, `seat_present=no`; the root then re-checked `CHECK ok round=42 want=42
seats=19` with the sentinel byte-identical.

VERDICT: scratch-guard-selftest-36/36
