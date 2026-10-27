# R45SentC2Sandbox — audit of the round-45 C2 probe's bwrap sandbox

Seat: R45SentC2Sandbox (sentinel, leaf). Date 2026-10-26. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read `plans/round-45-claims.md` in full before any run. This seat made no lane edit; all artifacts are in
`.ufo/waves/round-45/w1/R45SentC2Sandbox/` and the scratch dir.

## 0. Audited revision (provenance, because the tree moved under this audit)

* The claims freeze commit is `b4fcd35141acda5fa0980a34dd29ab880b702ee6`. Its probe blob hashes to
  `f87a9eebe464b29d95259cae24c00b56ea58de5bf93fef10884daa673e1488b5`; its capture tree is nested
  (`tests/test_outputs.py`, `environment/setup.sh`, `solution/solve.sh`).
* The seed/audit traces were taken 23:32–23:35 against that nested-layout probe: the traced bwrap argv binds
  `.../tb2-password-recovery/ins…`, `…/tes…`, `…/sol…` for the `/pub` files (`evidence/bwrap-argv-in-trace.txt`;
  strace truncated each string at 96 bytes), i.e. the nested capture sources of the frozen probe.
* At 23:38 another seat flattened the captures and re-pointed the probe. HEAD is now `9271dda`; the claims file
  carries a declared "Freeze amendments (pre-data, attempt 2, before landing)" note (`plans/round-45-claims.md:32`).
  `git diff b4fcd35 -- plans/password_recovery_probe.py` is three hunks and **only** capture-path strings; the
  sandbox construction (`sandbox_argv`, `ENV`, `harness`) is byte-identical. Current probe sha
  `9363e03e4ae3ef12f5cdc901c707922bf472222a98eecb079fa8075ac1beb4ab`; capture bytes still match the pinned
  digests (`test_outputs.py 2dc14fc…`, `setup.sh 9fdde5d…`, `solve.sh c5f9fc7…`, `instruction.md bc4f501…`).
* The grade-mode trace (`evidence/strace-grade-excerpt.txt`) was re-run under the frozen probe blob
  (`f87a9eeb…`) with a frozen-layout cap assembled in scratch from the byte-identical flat files. Conclusions
  below therefore hold for both the frozen and the amended probe.

## 1. Runs (envelope, QUALITY Q32)

Wrapper (all runs): `claims/envelope.sh <scratch/envN> <command…>`; its ENV line is
`bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind $SCR $SCR --bind $SCR/home-cache ~/.cache
--tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent`. Full lines are in `evidence/receipts.txt`.

| run | command | ENVELOPE start → end | digest |
|---|---|---|---|
| seed under strace | `strace -f -y -o trace.seed.txt -e trace=openat,open,creat,write,execve,clone,clone3,unshare,mount,setuid,setgid,capset,prctl python3 drive.py run1 recipe.seed.sh` | 23:32:35 → 23:32:38 exit=0 | before=after=`c263b11afb1cccf6` unchanged |
| recipe audit under strace | `strace … trace.audit.txt python3 drive.py run2 recipe.audit.sh` | 23:33:14 → 23:33:18 exit=0 | `c263b11afb1cccf6` unchanged |
| host-metadata audit under strace | `strace … trace.audit3.txt python3 drive.py run3 recipe.audit3.sh` | 23:35:33 → 23:35:36 exit=0 | `c263b11afb1cccf6` unchanged |
| real-`/dev/urandom` control | `bash control.sh` (same bwrap flags, `--dev-bind /dev /dev`, no zeros bind) | 23:34:18 → 23:34:19 exit=0 | `c263b11afb1cccf6` unchanged |
| grader reach (frozen probe) | `strace … trace.grade.txt python3 drive_grade2.py run5 capf` | 23:41:10 → 23:41:12 exit=0 | `e396f23e40a69201` unchanged |

Aborted attempts, reported for completeness: 23:32:19 (my driver's dataclass import bug, no measurement);
23:38:17 and 23:38:52 (`FileNotFoundError` on `…/tb2-password-recovery/tests/test_outputs.py` — the capture
tree was flattened between runs; both envelopes internally `unchanged`, no measurement taken).
`~/.local/bin` content digest changed **between** runs 23:35:36 and 23:38:17 (`c263b11…`→`e396f23…`, another
seat's tool install; each envelope run is internally unchanged, so no measurement is invalidated). This seat
never wrote to any PATH directory or `$HOME`.

Verify/observed commands that produced the numbers below are quoted inline or in `evidence/receipts.txt`.

## 2. Escape inventory (measured, this sandbox)

Definition used for the verdict: an *escape* = a write, code execution, or access to a host path other than the
intended `<work>/app` bind and the explicitly-bound read-only `/usr`, `/etc`, `/proc`, `/tests`, `/pub` files.

| # | Surface | What was attempted | Result | Evidence |
|---|---|---|---|---|
| E1 | network | TCP `1.1.1.1:80`, `127.0.0.1:22`, abstract AF_UNIX; `/proc/net/dev` | `ENETUNREACH`, `ECONNREFUSED`, `ENOENT`; only `lo`, no listeners; payload made **0** sockets | `evidence/audit-sandbox.txt` §net, §pids; grade trace: 0 payload socket(2) |
| E2 | host filesystem | `ls /home /root /sys /var /run`; `/proc/1/root`; `mount` | `No such file or directory` ×5; `/proc/1/root` = `/` (sandbox); bind mount `EPERM` | `audit-sandbox.txt` §home, §proc pid1, §mount try |
| E3 | capabilities / namespaces | `id`, `uid_map`, `CapEff`, `NoNewPrivs` | uid 1000, `CapEff=0`, `CapBnd=0`, `NoNewPrivs=1`; user/net/mnt/pid/ipc inodes differ from host; **uts shared** | `audit-sandbox.txt` §id/§uid_map/§caps/§ns; host ns ids in `receipts.txt` §ns ids |
| E4 | host pids | `ls /proc` | only 6 in-namespace pids; `/proc/1/exe`=`/usr/bin/bwrap` | `audit-sandbox.txt` §pids, §proc pid1 |
| E5 | host writes via recipe | writes to `/app/x`, `/tmp/x`, `/evil`, `/dev/newfile`, `/pub/newfile.txt`, and `cd /app/..` | `/app` (host bind) OK; `/tmp`, `/`, `/dev`, `/pub` OK **in-sandbox only**; `/tests`, `/seed.sh`, `/recipe.sh`, `/pub/*` `EROFS`/`EBUSY` | `strace-audit-excerpt.txt`; `audit-sandbox.txt` §pub/§tests/§root tmpfs |
| E6 | grader reach | trace a grade-mode harness on a synthetic non-case state (`HELLO\n`; no CASE verdict claimed) | payload opens exactly `/tests/test_outputs.py` (import) and `/app/recovered_passwords.txt`; **0** write-mode opens; 0 sockets | `strace-grade-excerpt.txt` |
| E7 | `/proc/sys` escape classics | write `hostname`, `sysrq-trigger`, `core_pattern` | `Permission denied` ×3 | `audit-sandbox.txt` §proc sys |

**Escapes found: 0.** The sandbox is a mount/pid/net/ipc/user namespace with an empty capability set, no
`/home`, no host pids, no network, no mount rights, and one read-write host bind (`<work>/app`) that is the
intended fixture directory.

## 3. Host-reach, question by question

**Q "network unshared?"** Yes. `--unshare-net`; the payload's connects fail (`audit-sandbox.txt` §net:
`CONNECT ('1.1.1.1', 80) ERR 101 Network is unreachable`). The grade-mode payload executed no `socket(2)`
the whole run (`strace-grade-excerpt.txt`: "payload write-mode opens (pid 7): 0", no socket lines). Loopback
exists but is dead (`127.0.0.1:22` → `ECONNREFUSED`); abstract AF_UNIX connect → `ENOENT`.

**Q "/home bound?"** No. `/home` does not exist in the sandbox; `/home`, `/root`, `/sys`, `/var`, `/run` all
`ENOENT` (`audit-sandbox.txt` §home). The mount table contains only the binds the probe asks for
(`audit-sandbox.txt` §mounts).

**Q "writable paths?"** Sandbox root tmpfs (`rw,uid=1000`), `/tmp` tmpfs, `/dev` tmpfs, the `/pub` *directory*
(it is `--dir` on the root tmpfs), and `<work>/app` rw bind. Everything else is a read-only bind
(`audit-sandbox.txt` §mounts: `ro` on `/usr`, `/etc`, `/tests`, the three `/pub` files, `/seed.sh`,
`/recipe.sh`, `/harness.py`, `zeros.bin`→`/dev/urandom`). A recipe cannot create a second host mount:
`mount("/app","/mnt",MS_BIND)` = `EPERM` (`strace-audit-excerpt.txt` line 4326).

**Q "can a case recipe's writes leak outside its /app?"** No measured leak. In the audit run every
payload write-mode `openat` resolves to `/app/*`, `/tmp/*`, `/dev/*`, `/pub/*` or `/` (sandbox tmpfs) and
nothing else (`strace-audit-excerpt.txt`); the host side of that run contains only `run2/app` (plus the
probe's own `tests/`, `zeros.bin`, `seed.sh`, `recipe.sh`, `harness.py`), and the tmpfs writes never reach the
host (`evidence/receipts.txt` §host side). `/app/..` is the sandbox root, not the host.

**Q "can the grader reach the host?"** Measured no: the only grader reads are `/tests/test_outputs.py` and
`/app/recovered_passwords.txt`, matching the pinned grader's only I/O (`tests/test_outputs.py:9,14`), with no
writes and no sockets (`strace-grade-excerpt.txt`).

## 4. The zeros-for-urandom substitution (Q2)

The bind is only `/dev/urandom` (`sandbox-argv.txt`: `--ro-bind /W/zeros.bin /dev/urandom`). Measured inside:

* **Grader-visible: no.** The pinned grader reads only the guess file (`tests/test_outputs.py:9,14`); the
  receipt's 16 verdicts are unchanged (claims note (2) says the receipt is byte-identical on re-run; the
  round-45 receipt in `corpus/evidence/round45/password-recovery-probe.txt` shows `mismatches=0 regrade differ=0`).
* **Beyond file content, yes — two setup-behaviour changes:**
  1. **Image size/extent.** `setup.sh:22` is `dd if=/dev/urandom of="$IMG_PATH" bs=1M count=4 status=none`.
     From the 64 KB zeros file, `dd` reads 65536 bytes then EOF and writes 65536 bytes
     (`strace-seed-excerpt.txt` trace line 2358: `write(…, "\0…", 65536) = 65536`). The sandbox image is
     3,145,851 bytes; the real-urandom control is 4,194,304 (`receipts.txt` §image sizes). The last ~1 MB tail
     of the real image does not exist here. Fragment **offsets are identical** (1048652 and 3145728 in both),
     because they come from `secret.zip`, not from the fill.
  2. **Noise determinism / token cardinality.** The control image contains a stray `W54` at 2796239 (2
     occurrences) while the zeros image has 1 (the fragment's); the 8XD count is 1 in both in this draw.
     `strings`/`grep -aob` enumeration over the image is therefore no longer random; the docstring discloses
     this ("grep -aob therefore cannot find a stray '8XD' or 'W54' outside the fragments"), and it also makes
     the five `…-$(head -c4 /dev/urandom…)` directory suffixes constant `00000000` (`receipts.txt` §dir names).
* **Not substituted:** `/dev/random` returns real host entropy (`random: 6a aa c9 56 …`) and `getrandom(2)`
  via `os.urandom` returns real bytes (`getrandom de456a27fe90a6b3`) (`audit-sandbox.txt` §entropy). Only
  `setup.sh`'s `/dev/urandom` reads are affected; any future recipe or grader using `os.urandom`/`getrandom`
  or `/dev/random` would see host entropy.
* **Unchanged by the substitution:** `date +%s%N` and `date +%Y%m%d-%H%M%S` are live host clock reads
  (`strace-seed-excerpt.txt` lines 787/2250; `audit-sandbox.txt` §clock), so timestamp-derived names stay
  non-deterministic as the docstring says.

Conclusion on Q2: **no grader-visible change**, but the substitution is not content-only: it changes the
image's size/extent and the noise's token cardinality (both consequences of `dd`'s short read + zeros), and the
docstring's "4 MB disk image" is not what the sandbox produces.

## 5. Is `/pub` truly read-only? (Q3)

* The three pinned files are: `--ro-bind` (`audit-sandbox.txt` §mounts, `ro` entries) → overwrite
  `openat(/pub/test_outputs.py, O_WRONLY|O_CREAT|O_TRUNC)` = `EROFS`
  (`strace-audit-excerpt.txt` line 3874), `rm` = `Device or resource busy`, and their sha256 values are
  unchanged after the attempt (`audit-sandbox.txt` §pub). The pinned grader copy cannot be replaced.
* The `/pub` **directory** is writable: `--dir /pub` sits on the rw sandbox root tmpfs; the recipe created
  `/pub/newfile.txt` (`strace-audit-excerpt.txt` line 3909; digest listed in `audit-sandbox.txt` §pub). That
  file exists only for that bwrap process (each harness call is a fresh sandbox) and never on the host.
* `/tests`, `/seed.sh`, `/recipe.sh`, `/harness.py` are ro-bind and reject writes (`EROFS`,
  `strace-audit-excerpt.txt` lines 3957-3958).

So `/pub`'s *files* are read-only; its *directory* is not. No probe or grader path reads anything from `/pub`
except the recipe-supplied `PW=$(grep … /pub/test_outputs.py)` (`plans/password_recovery_probe.py:98`), which
reads a ro file.

## 6. Evidence: strace of the setup.sh run (required)

Command (seed run in §1). The frozen probe's exact bwrap argv (`sandbox-argv.txt`) and the traced run agree.
Key lines (`trace.seed.txt`, sha256 `c52fcfd423879b8b6da3eadbb94e07c68afdb946aa7a896e4ba0eddd033b019d`):

```
trace.seed.txt:738   11  openat(AT_FDCWD</app>, "/dev/urandom", O_RDONLY) = 3</dev/urandom>
trace.seed.txt:787   15  execve("/usr/sbin/date", ["date", "+%s%N"], …)
trace.seed.txt:823   16  execve("/usr/sbin/dd", ["dd","if=/dev/urandom","of=/app/varsea/tmp-00000000/…bin","bs=512","count=10","status=none"])
trace.seed.txt:2325  56  execve("/usr/sbin/dd", ["dd","if=/dev/urandom","of=/app/varsea/disks/sub1/subA/subAlpha/ae3f4c.dat","bs=1M","count=4","status=none"])
trace.seed.txt:2357  56  openat(AT_FDCWD</app>, "/app/varsea/…/ae3f4c.dat", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3
trace.seed.txt:2358  56  write(1</app/varsea/…/ae3f4c.dat>, "\0…", 65536) = 65536
trace.seed.txt:2862  64  write(1</app/varsea/…/ae3f4c.dat>, "PK\3\4…PASSWORD=8XDP5Q2RT9Z", 96) = 96      # 1 MB + 76
trace.seed.txt:2899  65  write(1</app/varsea/…/ae3f4c.dat>, "K7VB3BV4WW54\nPK\1\2…", 123) = 123  # 3 MB
trace.seed.txt:2938  66  write(1</app/varsea/…/ae3f4c.dat>, "system check ok INFO: system check ok\n", 38) = 38  # 2 MB
```

Every write target is `/app/...` (the host scratch bind); no sandbox pid has a successful access to `/home`,
`/root`, `/var`, `/sys` or `/run` (the audit's attempts return `ENOENT`, `audit-sandbox.txt` §home), and the
only host-side writes in the trace are the driver's own scratch
files before bwrap (`trace.audit.txt:178-182`) plus bwrap's mount setup. The first filter also shows the
envelope's `/home` ro-bind doing its job: Python's import of the probe tried to write
`plans/__pycache__/password_recovery_probe…pyc` and got `EROFS` (`trace.audit.txt:112`), so no lane file was
touched by this seat.

## 7. Findings (non-escape; severity, exploit path, remediation)

1. **LOW — entropy substitution is partial.** `/dev/random` and `getrandom(2)`/`os.urandom` still return real
   host entropy (`audit-sandbox.txt` §entropy). Current setup.sh only reads `/dev/urandom`, so no current
   case is affected; a future recipe/grader that seeds from `os.urandom` would be non-deterministic while the
   docs imply full determinism. Smallest remediation: state the limit in the probe docstring ("only the
   `/dev/urandom` path is zeroed") — no more is needed for this case.
2. **LOW — the "4 MB disk image" is 3,145,851 bytes** because the 64 KB zeros file short-reads
   `dd bs=1M count=4` (`strace-seed-excerpt.txt` 2358). Not grader-visible (grader reads only the guess
   file); a solver that checks image size sees a different environment. Remediation: pad the zeros file to
   ≥4 MB (bytes only; size then matches while content stays zero) and say so, or say the image is 3 MB.
3. **LOW — noise token cardinality is deterministic.** Control image: 2 × `W54`; zeros image: 1
   (`receipts.txt` §image sizes). `grep -aob`/`strings` enumeration changes, and `solve.sh` iterates every
   `W54` offset. Disclosed for the strays; the image-size effect above is not. Remediation: document both.
4. **LOW — `/pub` directory is writable** (`/pub/newfile.txt` created; `strace-audit-excerpt.txt` 3909);
   the pinned files are ro and irreplaceable. Nothing reads `/pub` except the frozen recipe's own grep, so the
   impact is nil today; a recipe could plant files for a later recipe in the same sandbox (it does not: each
   harness call is a fresh bwrap). Remediation: `--ro-bind` a directory containing the three files instead of
   `--dir /pub` + file binds.
5. **INFO — read-only host fingerprint.** `/etc/machine-id` equals the host's (`432d02b5…`), `/proc/version`
   exposes the host kernel, `/etc/hostname`/`/proc/sys/kernel/hostname` = `plazir27`, boot_id and
   `core_pattern` are readable, and uts is **not** unshared (`audit-hostmeta.txt` §etc machine-id, §proc
   version, §boot_id; `audit-sandbox.txt` §ns uts `[4026531838]` = host). Writes to those sysctls are denied
   (`audit-sandbox.txt` §proc sys). By design (`/etc` and `/usr` are ro binds); noted for completeness.
6. **INFO — mountinfo discloses host source paths** (`/home/vgpnk/Projects/...`, `/scratch/hyaku/...`,
   `audit-sandbox.txt` §mounts). Read-only strings, no access implied.
7. **INFO / design — no resource limits** [INFERENCE, not executed]: `<work>/app` is an unquota'd host disk
   bind (a recipe could fill `/fast`), the root and `/tmp` and `/dev` tmpfs are unbounded RAM (host has 30 GB,
   ~17 GB available), and there is no `RLIMIT_*`, pids cap (new pid ns, no pids.max) or seccomp filter
   (`Seccomp: 0`). Cleanup is sound (`--unshare-pid` + `--die-with-parent` + `subprocess` timeout 1800 s ⇒
   killing pid 1 of the namespace reaps it), so this is a DoS window, not data reach. Recipes and the grader
   are frozen, so the current risk is nil; do not reuse this sandbox for arbitrary agent-authored recipes
   without limits.
8. **INFO — uid mapping under the envelope.** Inside the envelope's userns the nested sandbox shows
   `uid_map "1000 0 1"`, uid 1000, `CapEff=0` (`audit-sandbox.txt` §uid_map/§caps). Relative to the host this
   is host uid 1000 with no caps; the counter runs under the same envelope, so its behaviour matches.

## 8. Limits of this audit

* Only the probe's sandbox was audited (not bwrap itself); bwrap 0.13.1, not setuid, no file caps, unprivileged
  userns enabled.
* No resource-exhaustion test was run (host-safety; §7.7 is marked INFERENCE).
* The grade-mode trace used a synthetic non-case state (`HELLO`), so it cannot and does not assert any CASE
  verdict; the 16-case receipt is the executor's.
* `/dev/urandom`-zeroed cases can hide solver bugs that depend on random noise (by design; §7.3).

## 9. Evidence files (this dir) and digests

`audit-sandbox.txt` (8.8 KB), `audit-hostmeta.txt` (993 B), `strace-seed-excerpt.txt`,
`strace-audit-excerpt.txt`, `strace-grade-excerpt.txt`, `bwrap-argv-in-trace.txt`, `sandbox-argv.txt`,
`receipts.txt` (all < 10 KB).
Trace digests are in `receipts.txt` §trace digests; the scratch traces were deleted after excerpting.
No corpus/plans tree or clone was copied here; no file exceeds 1 MiB. Scratch
`/fast/scratch/hyaku/kengaku-r45/R45SentC2Sandbox` was removed with `plans/scratch_guard.py safe-rm`.

VERDICT: probe-sandbox-escapes-0
