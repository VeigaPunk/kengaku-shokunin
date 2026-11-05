# SentinelProbe — round-93 safety & fail-closed review (T `22972a317185216596b3dfe1c189e98d1eb86787`)

Seat SentinelProbe (leaf), 2026-11-05. Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`,
branch master. Method: `git clone --shared` into
`/fast/scratch/hyaku/kengaku-r93/SentinelProbe/lane`, `checkout -q --detach T`; all reads,
runs and fixtures against that clone; the real lane was never written. Instrument bytes at T
match the frozen-instruments table exactly (probe `6fad5d52…`, counter `89153db6…`, cases
`078b04d2…`), so everything below audits the frozen bytes. Raw receipts:
`.ufo/waves/round-93/w1/SentinelProbe/receipts/` (16 files, including the full 15.4 MB strace
log). `resume_continuity_v1` does not occur in any round-93 instrument (lane-wide grep hits only
historical wave docs and round-13 prose); the nearest analogue — a rejection must mutate nothing —
is exercised in §2.

## 1. Main run: isolation evidence (probe run once, under strace)

Command: `strace -f -e trace=file,network -o receipts/strace-main.log /usr/bin/python3
plans/round93_scheme_probe.py --lane <clone> --work <S>/work` → rc 0, `mismatches 0`, 279.7 s
wall; all 8 case vectors equal the committed official receipt's observation block byte-for-byte
(`probe-main.stdout.txt` vs `corpus/evidence/round93/scheme-probe.txt`). The committed receipt
stamps `LANE_TIP d8d0a4b8` (freeze commit F) and my clone run stamps `LANE_TIP 22972a31` (T):
F is an ancestor of T, which is the round's designed P1→P2→F→official-run→T ordering, not a
tamper signal.

- **bwrap argv (8 runs, identical shape; `bwrap-argv.txt`)**: `--die-with-parent --unshare-all
  --tmpfs / --ro-bind /usr /usr --ro-bind /etc /etc --symlink usr/bin /bin … --dev /dev --proc
  /proc --tmpfs /tmp --bind <work>/cases/<id>/app /app --ro-bind <work>/…/tests /tests
  --ro-bind <work>/harness.py /harness.py --setenv PATH /usr/bin --chdir /app
  /usr/bin/python3 -I -B /harness.py`. `--unshare-all` in all 8. Every bind source lives under
  `--work`; host `/app` and `/tests` are only shadowed inside the tmpfs root. (strace `-s` 32
  truncates the long bind paths with `…"`, the tail is evidenced by the inner execve lines.)
- **No write outside `--work`** (`strace-write-audit.txt`): host probe pid 795723 made 416
  successful write-flag file ops, **all** under `<S>/work`; 2156 writes to `/tmp` are sandbox
  tmpfs (inner pids). The 117 ops outside those classes are fully attributed: 40 are bwrap
  writing `uid_map`/`gid_map`/`setgroups` of the *new* user namespace (procfs of the sandbox),
  76 are dirfd/cwd-relative creations populating the sandbox tmpfs (`/dev` nodes,
  `harness.py`) or inner cwd-relative writes with cwd = sandbox `/app` (the bind of
  `work/cases/<id>/app`), 1 is `/dev/null` opened O_RDWR by the probe's git subprocess (null
  device, no filesystem effect). UNCLASSIFIED: 0. Host-probe-pid writes outside `--work`: 0.
- **No host `/app`/`/tests` writes**: sorted `find /app -xdev` hash before and after run A is
  identical (`b7c9eed8…`, empty root-owned dir; uid 1000 could not write it anyway); `/tests`
  does not exist before or after (`host-baseline.txt`).
- **No network** (`strace-network.txt`): 0 AF_INET/AF_INET6 syscalls. All 56 network-class
  syscalls are 8× the same bwrap setup pattern (AF_UNIX DGRAM sync socket + AF_NETLINK ROUTE
  socket bound nl_pid=1 with two RTM send/recv pairs), i.e. sandbox setup only.
- **Scratch self-clean**: the probe removes `work/cases` at exit; only `harness.py` remains.
  The lane clone stayed porcelain-clean through every run of this seat.

## 2. Fail-closed matrix (seat criterion: host-probe failures must degrade to `DEFECT SETUP` rc 2, never a pass)

| probe input | rc | outcome | receipt |
|---|---|---|---|
| `--bwrap /nonexistent/bwrap` | 2 | `DEFECT SETUP sandbox-unavailable` | `probe-nobwrap.stdout.txt` |
| `--bwrap /bin/false` (present, broken) | **1** | 8× `NOPAYLOAD(rc=1)`, mismatches 8 — **not rc 2** | `probe-false.stdout.txt` |
| userns sysctl unreadable — empirical, nested bwrap with tmpfs (and ro-bind-emptydir variant) over `/proc/sys/user`; **host sysctl never touched** | 2 | `DEFECT SETUP user namespaces unavailable (absent)` (both variants) | `probe-sysctl-absent*.stdout.txt` |
| userns sysctl `0`/garbage | 2 | code line `if not userns.isdigit() or int(userns) <= 0: return 2` (code reading) | — |
| capture sha mismatch (doctored byte in scratch fixture lane) | 2 | `DEFECT SETUP capture sha mismatch` | `probe-shamismatch.stdout.txt` |
| git absent from PATH (full run) | **0** | `LANE_TIP absent`, mismatches 0 — pass-shaped receipt, **not rc 2** | `probe-nogit.stdout.txt` |
| counter with git absent from PATH | **1** | uncaught `FileNotFoundError: 'git'` traceback | `counter-nogit.stdout.txt` |
| unknown eval kind / tests selector | 1 | `SystemExit("SETUP …")` → rc 1, not 2 (code reading) | — |
| case timeout beyond `CASE_TIMEOUT=1200` | 1 | uncaught `TimeoutExpired` traceback (code reading) | — |

**Verdict-flip analysis (frozen rule):** none of the deviations can turn a fail into a pass at
the frozen predicates. The rc-0 no-git receipt is caught by counter leg L3 (`LANE_TIP` must be
an ancestor of `--rev`; "absent" fails it) → predicate fail rc 1. The `/bin/false` rc 1 rerun
fails counter leg L6 → predicate fail rc 1. The gitless counter crashes rc 1 (never 0). SP-1
and SP-2 therefore change *how* a broken environment fails (mismatch-classified instead of
could-not-evaluate), never *whether*.

## 3. C1 counter git-archive extraction (`extraction-audit.txt`)

`plans/round93_c1_replay.py` L6 uses `tar.extractall(extract, filter="data")` — the explicit
stdlib safe filter (rejects absolute paths, `..`, escaping links, special files; strips
setuid/setgid/sticky). Empirically reproduced on `git archive` of T: 673,187,840-byte archive,
29472 members (25870 file + 3602 dir, 0 symlink/special), pre-extract audit found 0 unsafe
members; extraction reproduced all 25870 blobs (the only ls-list delta is `core.quotePath`
octal-escaping of one CJK filename — same file); extracted probe/counter/case-table shas equal
the frozen table; a hostile control tar (`../../escape.sh`) was rejected with
`OutsideDestinationError` and created nothing outside. Resource notes: a successful counter run
leaves `work/extract` (full lane tree) + `work/rerun` behind (no cleanup code — scratch-reaper
backstop), buffers the ~673 MB archive fully in RAM, and executes the extracted probe (L6)
*before* the L8 frozen-sha check (defense-in-depth ordering only; the bytes at the rev are the
round's own frozen history and produced the receipt under verification).

## 4. Hygiene

- **My scratch** lived only at `/fast/scratch/hyaku/kengaku-r93/SentinelProbe` and is removed
  before this yield (receipts copied out first). Sibling scratch census: ~18:19 showed 10
  round-93 dirs (ConnectorOverlap, ExecC1Rerun, ExecC2Rerun, ExecFreezeCensus, MutTesterGate,
  ReviewerC1, ReviewerC2, ScoutSources, ScribeQuality, SentinelProbe); at ~18:31 five siblings
  remained (CriticClaims, ExecC1Rerun, ReviewerC1, ReviewerC2, ScoutSources) — normal churn of
  an active wave, none stale beyond the 45-minute reaper window at either observation. The
  probe leaves only `harness.py` in its `--work`; the counter's on-success leftovers are SP-7.
- **Fleet root (report only, touched nothing)**: `git -C /home/vgpnk/Projects/shokunin status
  --porcelain` showed ` M .scratch/run15-kernel.py`, ` M .scratch/run15-state.json`,
  ` M .ufo/l0-questions.md`, `?? w4lines.txt` — tracked fleet-root files modified and an
  untracked file misrooted at the fleet root by some sibling process; attribution not attempted.
- **`resume_continuity_v1`**: zero-mutation analogue verified — every rc-2 path exits before
  any staging (bwrap check, userns check, sha check all precede `stage()`), and every rc-1
  path stages/writes only under `--work` (clone porcelain-clean after all six probe/counter
  runs of this seat).
- **Installs**: none (strace 7.2-1 and bubblewrap 0.13.1-1 already present from repos; pacman
  left untouched per the pause).

## 5. Findings

- **SP-1 minor** — probe with git absent from PATH prints a green `mismatches 0` receipt with
  `LANE_TIP absent` and exits 0 (`env -i PATH=<empty> /usr/bin/python3
  plans/round93_scheme_probe.py --lane <clone> --work <S>/work-nogit` → rc 0, 244 s), instead
  of `DEFECT SETUP` rc 2; `guarded()` swallows the OSError and the probe has no git gate.
  Integrated pipeline still fails closed (counter L3). Smallest remediation (round 94): treat
  `rev-parse` failure as setup defect, return 2 before the case loop.
- **SP-2 minor** — a present-but-broken sandbox (`--bwrap /bin/false`) passes the
  `is_file()+X_OK` gate and degrades to 8× `NOPAYLOAD(rc=1)` mismatches, rc 1 — not
  `DEFECT SETUP` rc 2 / could-not-evaluate. The committed P2 control only covers
  `/nonexistent/bwrap`. Fail-closed (counter L6 → rc 1). Smallest remediation: one sandbox
  liveness probe (e.g. `bwrap --true`) before the case loop.
- **SP-3 minor** — counter with git absent from PATH exits rc 1 via uncaught
  `FileNotFoundError` traceback (`git()` has no OSError guard); the docstring promises rc 2
  could-not-evaluate for evaluation blockers, so a crash is conflated with "a leg failed".
  Fail-closed. Smallest remediation: wrap the exec failure into `CouldNotEvaluate`.
- **SP-4 minor** — fleet-root misroots observed (report-only): modified tracked
  `.scratch/run15-kernel.py`, `.scratch/run15-state.json`, `.ufo/l0-questions.md` and untracked
  `w4lines.txt` at `/home/vgpnk/Projects/shokunin` (porcelain 2026-11-05 ~18:19 and ~18:29).
- **SP-5 info** — counter L6 executes the rev's probe bytes before L8 verifies them against the
  frozen-instruments sha (ordering/defense-in-depth note; no flip on this round's history).
- **SP-6 info** — probe `SETUP` aborts (unknown eval kind, unknown tests selector, mutant
  anchor count) exit rc 1 via `SystemExit(str)`, not the docstring's rc 2. Fail-closed.
- **SP-7 info** — successful counter runs leave `work/extract` + `work/rerun` (lane-sized,
  ~673 MB-class on this tree) in `--work` with no cleanup, and buffer the whole archive in RAM.
- **SP-8 info** — a case exceeding `CASE_TIMEOUT=1200` raises uncaught `TimeoutExpired` → rc 1
  traceback, conflating hang with mismatch. Fail-closed.

Not verified (scope limits): C2 counter/forgeries and the freeze gate battery (other seats);
no end-to-end counter L6 rerun (extraction reproduced standalone instead); fleet-root writer
attribution; host `/app` is empty so the find-hash sensitivity is coarse (compensated by
root-ownership, the strace write census, and the bwrap argv).

Files written by this seat: this report, its copy
`.ufo/waves/round-93/w1/SentinelProbe/report.md`, and the 16 receipts under
`.ufo/waves/round-93/w1/SentinelProbe/receipts/`. No lane file edited; no tool installed.
