# SentinelProbe — round-94 security/hygiene report (seat w1/SentinelProbe)

Scope: the four assigned checks over the round-94 instruments at T
`90c7677f0ba95d0930d93bda6a14aa50605ebe2e`, clone at
`/fast/scratch/hyaku/kengaku-r94/SentinelProbe/lane` (shared clone, detached at T).
Leaf seat: no subagents, no lane mutations (`git status --porcelain` clean after all runs).
All commands ran 2026-11-05; raw receipts in `receipts/` (index at the bottom).

## Check 1 — the probe cannot write host /app or /tests, reach the network, or leave files outside --work: **PROVEN (no escape found)**

**Static.** `plans/round94_compressor_probe.py:103-109` — every namespace is
`bwrap --die-with-parent --unshare-all --tmpfs / --ro-bind /usr /usr --ro-bind /etc /etc
--symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin
--dev /dev --proc /proc --tmpfs /tmp` plus per-leg binds. `--unshare-all` includes
`--unshare-net` (empty network namespace) and user/mount/PID/IPC/UTS namespaces. The only
read-write host paths ever exposed are the binds whose sources live under `--work`:
build leg `--bind <work>/ref /work` (line 121); case legs `--bind <work>/cases/<id>/app /app`,
`--ro-bind <work>/cases/<id>/tests /tests`, `--ro-bind <work>/harness.py /harness.py`
(line 174). The strace'd `execve("/usr/bin/bwrap", ...)` argv lines (receipt 04) show this
verbatim for the build and for C01. Host `/app` and host `/tests` are never referenced; with
`--tmpfs /` they are unreachable (root of the namespace is a fresh tmpfs, not host `/`).

**Dynamic (strace, 43,069 events, receipt 03/04).** Official run
`strace -f -qq -s 200 -e trace=file,network -o probe.strace python3 plans/round94_compressor_probe.py --lane . --work $S/work`
→ rc 0, `mismatches 0` (~21 s). Successful write-intent paths (`openat/open/creat` with
O_WRONLY/O_RDWR/O_CREAT, plus mkdir/rename/unlink/symlink/chmod/truncate/link) resolve only to:
`$S/work/*` (host, = in-ns `/work`, `/app`), in-ns `/tmp/cc*` (gcc temps, tmpfs),
in-ns `/dev/*`, `/proc/self/{uid_map,gid_map,setgroups}` (bwrap user-ns setup),
and bwrap's own `/newroot/*` pivot staging. Host-absolute write paths outside
`{$S/work, /usr ro, /etc ro, /tmp ns, /dev, /proc, /work, /app, /tests, /harness.py, /newroot}`:
**none**. Failed write-intent ops: 8 × ENXIO only (no EACCES leaks, no partial host writes).
Sockets: 9 × AF_NETLINK, 9 × AF_UNIX, **0 × AF_INET/AF_INET6** in the entire run.

**Dynamic (canary, receipt 05).** The instrument's own `sandbox()` builder was imported
unmodified (byte-exact replication, extra binds for /work /app /tests) and a shell battery run
inside: writes to `/canary` (ns tmpfs root), `/tmp`, `/work`, `/app` succeed — host leak checks
for all of them: **False**; `/home/canary`, `/root/canary`, `/fast/canary`, `/var/canary`,
`/usr/.canary`, `/etc/.canary`, `/tests/.canary` **DENIED** (ENOENT on tmpfs root / EROFS on
ro-binds); namespace root listing is exactly `app bin canary dev etc lib lib64 proc sbin tests
tmp usr work` (no /home, /root, /fast, /var, /run, /opt). Network from inside:
`AF_INET` connect → `[Errno 101] Network is unreachable`, AF_INET6 unsupported.

**Residue (receipt 07).** Host `/tmp`: zero `cc*` files newer than the run (gcc temps stayed in
the namespace tmpfs). Host `~/.cargo` mtime unchanged (2026-11-02, before the round);
`~/.rustup` absent. Probe residue in `--work` after the run: only `work/harness.py`
(`work/ref` and `work/cases` are rmtree'd by the probe itself) — inside `--work`, per design.

**Host /app note.** Host `/` has an EMPTY `app/` dir, `drwxr-xr-x root:root`, mtime
2026-11-05 05:17 (pre-existing; not created by this run). The probe running as `vgpnk` could not
write it (Unix perms) and provably never targets it (bind argv + strace). See FINDING SP-1.

## Check 2 — reference build leg (rustc inside bwrap): **no host writes**

Build command (line 120-122): `rustc main.rs -o main && cat data.txt | ./main > data.comp` in
`/work` with exactly one RW bind `<work>/ref → /work`. Environment inside: `--setenv HOME /tmp`
(tmpfs in the namespace), `PATH=/usr/bin`; canary confirmed `HOME=/tmp` with an empty home.
`main`, `data.comp` and `full.rmeta` land in `/work` (= `<work>/ref`, under `--work`); strace
shows no other rustc write target. No cargo is invoked and no cargo/rustup home exists on the
host side of the equation (Arch system rustc 1.99.1; `~/.rustup` absent; `~/.cargo` untouched).
The grader's `gcc -o decomp2 decomp.c` (case legs) emits `/tmp/cc*.s/.o` — inside the case
namespace's `--tmpfs /tmp`; host `/tmp` has no residue (receipt 07). No `/proc/sys` write
appears anywhere in the strace (host sysctls untouched).

## Check 3 — hardcoded /tmp paths and credential-shaped strings: **clean**

- `/tmp`-shaped occurrences in the five instruments: exactly two, `--tmpfs /tmp` and
  `--setenv HOME /tmp` (`round94_compressor_probe.py:106,109`) — in-namespace tmpfs by design,
  not a host-scratch path. No `tempfile`, `mkdtemp`, `TMPDIR`, no `python3 ... /tmp/...`
  anywhere in the instruments. No hardcoded absolute write target outside the bind vocabulary
  (`/usr/bin/bwrap`, in-ns `/work` `/app` `/tests` `/harness.py`, `/proc/sys/...` read-only read,
  host tool version probes).
- Credential scan over all 5 instruments + claims + 11 captured corpus files (precision pattern:
  password|passwd|secret|api_key|AKIA…|BEGIN … PRIVATE KEY|ghp_…|sk-…|Bearer …|aws_access_key_id|credential):
  **zero matches**. A looser first pass matching bare `token` hit only Rust compression-token
  identifiers (`Token`, `read_token`, `tokens_to_c_bytes`) in `solve.sh`/`main.rs` — source code,
  not credentials.

## Check 4 — frozen-instruments table vs T: **11/11 OK**

Table extracted from `git show F:plans/round-94-claims.md`; each of the 11 paths hashed at T via
`git show T:<path> | sha256sum` — all 11 equal (receipt 01). Additionally
`git diff F T -- plans/round-94-claims.md` is empty: the claims file (and its table) is
byte-identical at F and T, so "no tabled file changes after F" holds by construction at T. Files
that DID change F..T: `corpus/SOURCES.md`, `corpus/evidence/round94/compressor-probe.txt`,
`corpus/evidence/round94/decomp-opt-divergence.txt`, `plans/grader-population-ledger.json` —
none of them tabled; consistent with the frozen rule.

## Findings

No defect found that would flip a verdict; the frozen rule is not triggered.

- **SP-1 (info)** Pre-existing host state: empty `app/` at host `/`, root:root 755, mtime
  2026-11-05 05:17 — older than this seat's activity, never referenced by the probe (bind argv +
  strace + EACCES for non-root). Not an instrument defect; flagged only so the L1 does not
  mistake it for probe leakage. Smallest remediation: none (optionally `rmdir` by an admin after
  confirming no other consumer).
- **SP-2 (minor, route to round 95)** Environment passthrough into the sandbox: `subprocess.run`
  inherits the full operator environment (the traced `execve` of bwrap carries `/* 273 vars */`)
  and bwrap only overrides `PATH` and `HOME` (no `--clearenv`). Stray `TMPDIR`, `CARGO_HOME`,
  `RUSTFLAGS`, `HTTP_PROXY`, etc. reach rustc/gcc inside the namespace. Exploit path: a dirty
  operator env perturbs the reference build or grader compile *inside* the ns — unbound paths do
  not exist there, so there is **no host-write escape** and no network, and the failure mode is
  visible (build failure → `SETUP reference build failed`, rc 2 = could-not-evaluate; or a
  mismatch → honest claim failure). I identified no silent-false-pass path. Smallest remediation
  (round 95, not in-round): launch bwrap with `env={"PATH": "/usr/bin", "HOME": "/tmp"}` or add
  `--clearenv` before the `--setenv` pair. This run had `TMPDIR`/`CARGO_HOME`/`RUSTUP_HOME`
  unset and the build reproduced `REFERENCE_COMP_SHA 3a905a…9131`, 2264 B, matching the
  divergence receipt's reference line — verdicts unaffected.
- **SP-3 (info)** Host `/usr` and `/etc` are readable (read-only) by the captured grader code
  inside the namespace (toolchain/nss requirement). No exfiltration channel exists: no network,
  stdout is a 4-letter `PAYLOAD` line, writable surface is `--work`-only. Accepted trade-off;
  no action.
- **SP-4 (info)** One kernel-internal AF_NETLINK `RTM_GETLINK`/`RTM_GETADDR` exchange per
  namespace (payload shows only 127.0.0.1) — interface enumeration inside the empty netns; zero
  AF_INET/AF_INET6 sockets in the whole run. Harmless; no action.

## Tooling record

No tools installed or upgraded this seat (strace, bwrap 0.13.1, rustc/cargo, git all present;
pacman untouched). One tooling anomaly: the `grep` tool once reported matches for
`/tmp|tempfile|mkdtemp|TMPDIR` in `round94_c1_replay.py` lines 117-119; a repro on the same file
returned "No matches found" and a literal substring check confirms no `tmp` occurs in that file
— reported via the automated QA channel; all hygiene conclusions above rest on the repro'd,
consistent outputs.

## Receipts (`receipts/`)

01-frozen-table-hash-check.txt — 11/11 OK, F table vs T bytes
02-probe-run.stdout.txt / 02-probe-run.stderr.txt — official probe run under strace (rc 0, mismatches 0)
03-probe.strace.gz — full strace -f -e trace=file,network log (43,069 events)
04-strace-classification.txt — write-intent paths, host-absolute stragglers (none), socket families, bwrap argv
05-canary.txt — sandbox canary battery + network denial + host leak checks
06-claims-F-vs-T.txt — claims file identical F..T; changed-files list (none tabled)
07-host-residue.txt — host /app stat, /tmp residue (none), ~/.cargo mtime
