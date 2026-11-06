# SentinelProbe — sandbox security review of `plans/round96_merger_probe.py` @ T

Seat: SentinelProbe-5 (leaf, no subagents). Date: 2026-11-05.
Target: the bubblewrap sandbox recipe of `plans/round96_merger_probe.py` at measured tip
`09717e49ff46fad5b255619d671aaaae52dfc180` (clone of the lane at T; `TOOL_SHA` of the clone copy
`78ce14ceab7156c230536e02aeb42abd2f49daaed737213a5f97a2f0ef776f17` — identical to the
frozen-instruments entry stamped in both full runs below, so no post-F drift).
bwrap: `/usr/bin/bwrap` bubblewrap 0.13.1. Kernel 7.2.11-arch1-1.

## Method

- Read the instrument in full; the sandbox is `Box.cmd`: `bwrap --die-with-parent --unshare-all
  --clearenv --tmpfs / --ro-bind /usr /usr (+ /bin,/lib,/lib64,/sbin symlinks) --dev /dev
  --proc /proc --tmpfs /tmp` + ro-binds of the two venvs and `interpreter_root()` of each
  (the uv interpreter store) + per-phase binds (`--bind <work>/cases/<id>/app /app` rw;
  `--ro-bind <capture>/environment/data /data`; grader phase adds `--ro-bind tests /tests` and
  `--ro-bind harness.py /harness.py`) + `--setenv PATH/HOME/LANG` and `--chdir`.
- All live checks reuse the probe's **own** `Box.cmd` argv builder, imported from the T clone
  (drivers copied here). Payloads print names / counts / errnos / booleans only — no environment
  values ever printed or receipted. A canary `CANARY_SENTINEL_R96` (value never printed) was set
  in the driver's host shell for the clearenv A/B.
- Venvs staged per the claims' recipe (`uv venv -p 3.11` + pandas 2.2.3/pyarrow 17.0.0;
  `uv venv -p 3.13` + pandas 2.3.3/pyarrow 22.0.0) under scratch; both venv pythons resolve into
  `/home/vgpnk/.local/share/uv/python`, which is exactly the tree `interpreter_root()` binds.
- Two independent full probe runs at T (my venvs): rc 0, `mismatches 0`, 17/17 `ok=True`
  (`receipts/r9-probe-run.txt`, `receipts/r11-incident-fullrun.txt`), matching the official
  receipt `corpus/evidence/round96/merger-probe.txt` line for line.

## Verified properties (all pass — no verdict-flipping defect found)

| # | Property | Result | Receipt |
|---|---|---|---|
| SP-1 | `--clearenv` empties the environment | host shell: 274 env names; inside: exactly 4 (`HOME`, `LANG`, `PATH`, `PWD`; the last two set by the argv/`--chdir`). Canary absent inside, present in the no-clearenv control (274 names) — the builder itself filters nothing, so clearenv is the only barrier and it holds | `r1-envnames-clearenv.txt`, `r2-envnames-no-clearenv.txt` |
| SP-2 | no network | netns has only `lo`; `connect_ex(127.0.0.1:1)`→111 ECONNREFUSED, `connect_ex(1.1.1.1:80)`→103 ECONNABORTED, `getaddrinfo`→gaierror −3; `/sys` absent; `AF_UNIX` create OK (namespaced only) | `r6-net.txt`, `r3-mountinfo.txt` |
| SP-3 | `/etc` not bound | `/etc`, `/etc/passwd`, `/etc/resolv.conf`, `/etc/hostname` all ENOENT; mountinfo has no `/etc` entry; matches the instrument's `SANDBOX … etc-bound=0` stamp | `r4-etc-home.txt`, `r3-mountinfo.txt` |
| SP-4 | host trees read-only | file-create attempts denied EROFS 36/36 across `/usr`, `/usr/local`, `/tests`, env venv, grader venv, uv store, `/data` (both interpreters, 12/12 each; `O_CREAT\|O_WRONLY` and `O_WRONLY` on existing capture file also EROFS; `O_RDONLY` of course succeeds). `/data` `mkdir`/`remove`/`chmod` all EROFS. One earlier run of my first payload observed ENOENT once on `/data` create — still a denial; the stable tally is EROFS. Writable windows: `/app` only (binds to `--work/cases/<id>/app` — a `SENTINEL` file written inside appeared host-side in scratch, nowhere else) plus the namespace-local tmpfs (an unbound `/fast/.../OUTSIDE.txt` write succeeded inside and provably never appeared host-side) | `r5-writes.txt`, `r5b-writes-granular.txt`, `r5c-errno-tally-*.txt` |
| SP-5 | no privilege/escape path | uid/gid 1000 mapped 1:1; `CapInh/Prm/Eff/Bnd/Amb` all `0000000000000000`, `NoNewPrivs 1`; `mount -o remount,rw /data` → rc 32 "must be superuser"; `unshare -m` → EPERM; `mknod` → EPERM; `/proc/sys/user/max_user_namespaces` write attempt → EACCES (DAC, root-owned 0644; no sysctl touched); no leftover bwrap processes from this seat after 15+ runs (pidns + `--die-with-parent`) | `r7-caps-uid.txt`, `r5b` |
| SP-6 | host visibility surface | in-ns mount table is exactly: tmpfs `/`, ro `/usr` (incl. `/usr/local`: only `mkinitcpio`, `man`, `wayland-sessions` — no local secrets), fresh `/dev` (null/zero/full/random/urandom/tty/pts), fresh `/proc` (2 pid entries), tmpfs `/tmp`, ro venv dirs, ro uv store, rw `/app`, ro `/data` (only the member's `source_a/b/c`), ro `/tests`, ro per-phase scripts. Credential probes all absent inside: `~/.ssh/id_rsa`, `~/.netrc`, `~/.git-credentials`, `~/.config/gh/hosts.yml`, `~/.aws/credentials`, uv-cache, `/root/.bash_history`. `/home/vgpnk` inside resolves through an empty dir chain (`.local/share/uv`) to the store bind and nothing else; the store contains only interpreter dirs + `.gitignore/.lock/.temp`. **Host credential exposure path: none found.** The conditional path — 274 host env vars flowing into every case — exists iff `--clearenv` is dropped, and the A/B proves it is doing the blocking | `r3`, `r4`, `r8-store-visibility.txt`, `r8b-usr-local.txt`, `r1`/`r2` |
| SP-8 | case `/app` tree removed after the run | `main()` ends `finally: shutil.rmtree(work/"cases", ignore_errors=True)`; post-run `work/cases` **ABSENT** in both full runs (leftovers are only `harness.py`, `tests/`, `versions.py` in the runner's own scratch); `stage()` pre-cleans each case root on rerun | `r9b-cleanup.txt`, `r11-incident-dir.txt` |
| SP-12 | lane-path guard | probe run with `--work` inside the **passed** lane prints `DEFECT SETUP path inside the lane …`, rc 2, and creates nothing (guard precedes `work.mkdir`) | `r10-lane-refusal.txt` |

## Findings (routed, never repaired in round)

- **SP-7 (minor, route to round 97).** `interpreter_root()` binds the **whole** uv interpreter
  store `/home/vgpnk/.local/share/uv/python` (15 interpreters: 3.9–3.15, pypy, freethreaded)
  read-only, because a venv's python resolves through the minor-version alias symlink that lives
  in the store root (instrument docstring says this is deliberate). Impact is bounded — the tree
  holds interpreter payloads only, no credentials or user data (verified by listing) — but every
  forged run is exposed to the host's full interpreter inventory, and any future non-interpreter
  file dropped into that directory would leak into all cases. Smallest remediation: stage the two
  pinned interpreters in a dedicated `UV_PYTHON_INSTALL_DIR`, so "the whole store" contains only
  what the replay needs; the bind scope semantics then stay unchanged.
- **SP-9 (info).** Fingerprinting: the new UTS ns is a copy of the host's — `hostname` (plazir27)
  and kernel release are visible inside; mountinfo exposes host storage topology (btrfs
  `/dev/mapper/root` subvol paths, xfs `nvme1n1p2`, peer-group ids). No credential impact.
  Cosmetic remediation: `--hostname tb2-case` in the recipe.
- **SP-10 (info).** The tmpfs root is writable, so a forged case can fabricate `/etc`, `/var`,
  `/root` — and files under the `/home/vgpnk/...` bind-point chain — **inside** the namespace
  (demonstrated: `NS_ROOT_ETC_WRITE SUCCEEDED`). This never touches the host (SP-4/SP-5) and dies
  with the namespace; nothing in the recipe consumes these paths, but "no /etc" should be read as
  "no host /etc", not "no /etc possible".
- **SP-11 (info, self-disclosure of a seat process error, not an instrument defect).** My first
  guard test passed `--lane <clone>` while pointing `--work` at
  `…/kengaku-shokunin/.ufo/waves/round-96/w1/.sentinel-guard-tmp`; the guard correctly scopes to
  the *passed* lane, so a full probe ran with work inside the real lane's untracked `w1/`. Effects:
  `versions.py`, `harness.py`, `tests/test_outputs.py` under that dir (receipted in
  `r11-incident-dir.txt`), `cases/` removed by the instrument's own `finally`. I removed the dir;
  `git status --porcelain` shows only the pre-existing untracked wave entries
  (`w1.ready`, `w1.ready.dispatched`, `w1/`) — zero tracked changes, nothing of other seats
  touched. Lesson: any probe invocation's `--work` belongs under `$S` regardless of `--lane`.

## Out-of-scope observations (not judged here)

- Live sibling processes at review time run older recipes that bind more: a round-93-style probe
  with `--ro-bind /etc /etc`, and battery-forgery harnesses with `--unshare-net --dev-bind / /`.
  Those are not the assigned round-96 instrument; the r96 recipe is the strictest of the family.
- `.ufo/waves/round-96/L1/ledger-count.txt` (named in the assignment as an L1 receipt at T) is not
  present; the closest is `L1/mistakes/M3-ledger-count-partial.txt`. Outside my surface; flagging
  for the L1 only.
- Timing: full 17-case probe run measured ~45–65 s wall under sibling load (contract says ~25 s);
  no defect implied.

## Tooling record

No tools installed or upgraded. Preexisting: bwrap 0.13.1 (`/usr/bin/bwrap`), uv 0.13.0
(`~/.local/bin/uv`). Used `uv venv`/`uv pip install` for the two pinned venvs exactly per the
claims' staging recipe. No sysctls touched; no pacman; no writes outside scratch, the seat wave
dir, and the Report file (one disclosed exception: SP-11, remediated).

## Receipts (this directory)

`r0-argv.txt` exact builder argv (agent- and grader-phase shape) · `r1`/`r2` env A/B ·
`r3` mountinfo+ns layout · `r4` /etc + credential-path probes · `r5`/`r5b`/`r5c` write denials
(coarse, granular, 12× errno tally per tree/interpreter) · `r6` network · `r7` caps/uid/remount/
unshare/mknod · `r8`/`r8b` store and /usr/local visibility · `r9` full probe run at T (my venvs) ·
`r9b` post-run work dir (cleanup) · `r10` lane-refusal guard · `r11` incident run + dir listing ·
`driver.py`, `driver2.py`, `driver3.py` (the harnesses that produced r0–r8b/r5c).
