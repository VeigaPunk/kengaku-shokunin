# SentinelR84 — security review: bubblewrap probe and R84 counter

Read-only review. No production file was edited. Seat: SentinelR84 (sentinel), round 84 wave 1.

## Reviewed bytes (pinned)

| artifact | path | sha256 |
|---|---|---|
| R83 baseline probe | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/round83_code_image_probe.py` | `21922612c84b82c0a98a4c98a36ed9b11410841c82c89bd9556064f8868bae23` |
| R84 probe draft | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py` | `82f359e67840ec5ed876dc1904c0f69b158d2f1bc33278df3dfd64c51d528e75` |
| R84 counter draft | `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-84/w1/CounterR84/round84_c1_replay.py` | `ea8cfdda495959b5ceeac52ca2e2a8581562c89c7edacfba9cc9ae0670bb61ee` |
| frozen review copies | `.ufo/waves/round-84/w1/SentinelR84/reviewed-*.py` | same two draft hashes |

Draft availability: both R84 drafts were ABSENT at the first check (2026-11-04T15:39Z, dirs empty); both were
present by 15:46Z. The review is pinned to the two snapshot hashes above; the live drafts still matched those
hashes at 2026-11-04T18:53:32Z. If either live file changes before integration, this review covers only the
pinned bytes and the diff needs re-review.

## Verdict

**No blocker. No major.** The sandbox vector is sound: network namespace unshared, host home/lane absent,
`/usr` and `/etc` read-only, only the per-case directory bound at `/app`, the subject and harness bound
read-only, environment cleared to an explicit three-variable allowlist, and the receipt's `COMMAND` is parsed,
never executed. Three minor hardening gaps remain (S1–S3), all with tested one/two-flag fixes that keep the
frozen subject green.

## Required-check results

| # | check | verdict | evidence |
|---|---|---|---|
| 1 | no network namespace escape | PASS | `--unshare-all` includes net in bwrap 0.13.1 (no `--share-net`); sandbox netns inode `4026533568` ≠ host `4026531833`; `connect(("1.1.1.1",80))` → `OSError: Network is unreachable`. There is no separate `--unshare-net` token, but `--unshare-all` is the documented superset and nothing re-shares net. |
| 2 | no host `/app` write; case dir bound only | PASS | mountinfo `/app` source is `<work>/case-*/app` on scratch (`/fast/scratch/...`), not host `/app` (host `/app` does not exist); `/app/..` lists the sandbox root, not the host case dir; no lane/fleet-root bind anywhere. |
| 3 | `/tests` read-only | **PARTIAL — S1** | `/tests/test_outputs.py` is a `ro` bind and `unlink` fails `EBUSY`; however `/tests` itself is a writable directory in the root tmpfs (`write /tests/planted.py` → ok). |
| 4 | `/usr` and `/etc` read-only | PASS | writes fail `EROFS` (`/usr/planted`, `/etc/planted`); mountinfo shows both `ro`. |
| 5 | no bind of `$HOME` | PASS | argv contains no home bind; inside the sandbox `/home`, `/home/vgpnk`, `~/.ssh`, `~/.omp`, `~/.config` all absent. |
| 6 | no bind of the lane or fleet root | PASS | only `/usr`, `/etc`, the case `app`, the staged subject and the harness appear in the sandbox; mountinfo source for the subject is the corpus file, not the lane root. |
| 7 | no environment credential passthrough | PASS | `--clearenv` + explicit `PATH=/usr/bin`, `LANG=C.UTF-8`, `LC_ALL=C.UTF-8`; observed sandbox env is exactly those three plus bwrap's `PWD=/app`. The bwrap process itself also gets `env={"PATH": "/usr/bin"}`. |
| 8 | no writes to `/tmp` outside `TMPDIR` | PASS | `/tmp` does not exist in the sandbox (`write /tmp/planted` → `ENOENT`), so no host-backed tmp path is reachable; all host temp dirs use `TemporaryDirectory(..., dir=work)` and `TMPDIR=work` is set before use. |
| 9 | probe does not execute code from receipt or ledger | PASS | Probe: zero `RECEIPT`/`LEDGER` references; it executes only the sha256-pinned capture, staged to a fresh temp path, inside bwrap. Counter: `parse_receipt` is regex/string only; `command_matches` uses `shlex.split` and compares tokens; a hostile `COMMAND ...; touch <path>` matched `False` and the touch target was not created. |
| 10 | no `shell=True` with interpolated paths | PASS | 0 occurrences of `shell=True`/`os.system`/`os.popen` in all three files; every `subprocess.run` receives a list argv with absolute or constant paths. |
| 11 | no secret reading | PASS | 0 source references to `/.ssh`, `/.omp`, `/.config`, `/home/`; the sandbox cannot see `/home`; `/etc/shadow` is mode `600 root` and is not readable as uid 1000. Host-side reads are lane-relative (`CAP`, `TABLE`, `__file__`). |
| 12 | bwrap options exist (0.13.1) | PASS | `bubblewrap 0.13.1`; `--help` lists `--unshare-all`, `--unshare-user`, `--unshare-net`, `--clearenv`, `--ro-bind`, `--bind`, `--dir`, `--proc`, `--dev`, `--new-session`, `--die-with-parent`, `--disable-userns`, `--assert-userns-disabled`, `--size`. |

## Findings

| id | severity | file:line | evidence | fix |
|---|---|---|---|---|
| S1 | minor | `.ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py:176-177`; `plans/round83_code_image_probe.py:76-77` | `--dir /tests` creates a writable directory; only `/tests/test_outputs.py` is `--ro-bind`. Diagnostic: `write_tests = ok`, `unlink_tests_file = OSError EBUSY`, mountinfo shows the file `ro`. The frozen claim's "grader read-only at /tests" holds for the file but not for the directory. | Stage each subject as `<dir>/test_outputs.py` and bind the directory read-only at `/tests` (drop `--dir /tests` + file bind): `--ro-bind <capture-dir> /tests`; the selftest fixtures need the same per-fixture staging dir. Verified with the real subject: `/tests/planted.py` → `EROFS`, unlink → `EROFS`, subject legs still `P/P`. |
| S2 | minor | `round84_gcode_probe.py:170`; `round83_code_image_probe.py:70` | Nested user and mount namespaces are creatable inside the sandbox: `unshare -U true` rc 0, `unshare -U -r -m -- mount -t tmpfs none /tests` rc 0. `CapEff 000…0`, `NoNewPrivs 1`, `Seccomp 0`. Containment still holds (no host mounts), but the nested-userns kernel surface remains open for a compromised subject. | Add `--unshare-user --disable-userns --assert-userns-disabled`. `--disable-userns` refuses without an explicit `--unshare-user` (`bwrap: --disable-userns requires --unshare-user`). Verified: nested `unshare` rc 1 (`No space left on device`) and the diagnostic harness still runs rc 0. |
| S3 | minor | `round84_gcode_probe.py:170-181`; `round83_code_image_probe.py:70-81` (no `--size`/`--tmpfs`) | All writable tmpfs mounts are uncapped: 100 MiB write to `/` → ok, 100 MiB write to `/dev/shm` → ok; root mount is `rw … tmpfs`. A compromised subject can consume tmpfs memory (host default up to ~50 % RAM) until the 60 s per-case timeout. `/dev/shm` exists via `--dev /dev`. | Cap the writable tmpfs mounts: `--size 67108864 --tmpfs /` (before the `/usr` `/etc` binds; `--size` must precede `--tmpfs`) and `--size 67108864 --tmpfs /dev/shm` after `--dev /dev`. Verified: 100 MiB root and shm writes → `ENOSPC`; subject legs `P/P` under the sized root. |
| S4 | info | `round84_gcode_probe.py:175`; `round83_code_image_probe.py:75` | `--proc /proc` exposes `/proc/self/mountinfo`, whose bind sources disclose host paths (`/@home/vgpnk/Projects/shokunin/kengaku-shokunin/...`, `/scratch/hyaku/...`, btrfs subvolume). Disclosure only; no access. | Drop `--proc /proc` if the subject does not need it (the pinned tests use `pathlib` only), or accept as low risk. |

### Exploit paths and impact

Any application of S1–S3 changes the probe's bytes and therefore its `TOOL_SHA`; the receipt and the
counter's `trusted_tool_sha`/`TOOL-UNTRUSTED` pins must be re-minted against the fixed tool before the
counter is run. The fixes preserve the frozen subject semantics (verified `P/P`), so no claim element changes.

- **S1.** A malicious or compromised grader (only reachable if the sha pin is wrong or a hostile capture is
  admitted) can create files under `/tests`, but the only path the harness parses/imports is
  `/tests/test_outputs.py`, which is a read-only mountpoint and cannot be unlinked (`EBUSY`). No host write and
  no code substitution today. It becomes an integrity risk only if the harness later loads helper files from
  `/tests`.
- **S2.** A compromised subject can create nested user/mount namespaces and mount temporary filesystems inside
  them. This does not expose host mounts (the source mounts are owned by bwrap's namespace and remain
  read-only), but it re-opens the kernel's unprivileged-userns attack surface. Impact requires a kernel bug;
  severity is hardening, not a demonstrated escape.
- **S3.** A compromised subject can allocate tmpfs memory until the per-case 60 s timeout; no persistent host
  state is created. The 64 MiB caps bound this to a nuisance. (The `/app` bind is host-backed rw by design and
  explicitly allowed by the frozen claim; both legs only read, so `--ro-bind` of the case app is an optional
  extra — verified `P/P` — but not required.)
- **S4.** Host-path disclosure only; no secret bytes are reachable (`/etc/shadow` is 600 root; `/home` is not
  mounted).

## Adjacent observations (not counted)

- **Counter forwards the full host environment to the instrument.** `CounterR84/round84_c1_replay.py:307`
  (`env = dict(os.environ, TMPDIR=str(wd))`) gives the probe process every operator environment variable; the
  probe's own `git`/`openssl` calls inherit it. The sandbox boundary is unaffected because the probe invokes
  bwrap with `env={"PATH": "/usr/bin"}` and `--clearenv`. No secret is read or printed. Tightening the
  instrument process would change the frozen `COMMAND`, so this is a note, not a requested change.
- **Freeze-table pin is conditional.** `plans/round84-cases.json` is absent at both BASE
  `4087b2f8` and FREEZE `b12a9d4` (`git cat-file -e` rc 1); `load_freeze_table` returns `None`,
  `validate_frozen_table` is skipped, and the counter prints `table=…@claims`. The measured table is then
  anchored by the receipt's `CASE_TABLE_SHA`, the `CLAIMS_CASES` vectors, and the probe's sibling
  `FROZEN_TABLE_SHA` — not by a freeze-commit artifact. Provenance note for the L1/critic; not a sandbox defect.
- **Receipt grammar is not an execution channel.** The probe emits `COMMAND` via `shlex.join` but never runs it;
  the counter only `shlex.split`s it. A hostile command string is rejected by token-count/position and is not
  executed (verified: target file absent).

## Method and evidence

- `bwrap --version` → `bubblewrap 0.13.1`; `bwrap --help` option inventory (above).
- `sentinel_sandbox_audit.py` loaded the R83 baseline module without executing its `main`, materialised its
  `sandbox_argv`, and measured the sandbox from inside: namespaces, env, host visibility, write attempts,
  mountinfo, network, capabilities, nested namespaces. Receipt: `sandbox-audit.txt` (sha256
  `3923983fef1ff92533e8da3d84d44f5f5f0b144f1e7420d6c1e79dddcbfb65f3`).
- `sentinel_draft_audit.py` pinned the two draft snapshots, proved the R84 `sandbox_argv` is byte-identical to
  the R83 baseline vector, re-ran the R84 vector against a diagnostic harness, and proved the counter parses
  but never executes a hostile `COMMAND`. Receipt: `draft-audit.txt` (sha256
  `74ad61d57759dfe51f1857dffe644f7418a11decc55e832ff46c4c88c048a470`).
- Additional targeted runs: ro-tests fix, `--disable-userns` fix, sized-root/shm fixes, ro-app variant (all in
  scratch under `$HYAKU_SCRATCH/kengaku-r84/SentinelR84`; scratch removed after copying receipts).
- Static review of the three sources in full; `grep` for `shell=True`, `os.system`, `eval(`, `exec(`, secret
  paths, receipt/ledger reads. No build, lint or general test suites were run. No production file edited.
  Tool installs: none.

## Limits

- bwrap userns is not a VM: the boundary is the user namespace + mount set; there is no seccomp filter
  (`Seccomp: 0`) and S2 shows nested namespaces remain available. The subject capture is sha256-pinned
  (`6b049dc6…`), so the threat model is a trusted capture with defense-in-depth, not arbitrary hostile code.
- The review covers only the three files above and the two pinned draft snapshots; the R84 counter's claim
  logic (receipt/ledger semantics) was read for execution channels, not re-verified as a population counter.
