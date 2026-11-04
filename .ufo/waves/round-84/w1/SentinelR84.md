# SentinelR84 — scoped findings (round 84, w1)

Read-only. Seat: SentinelR84, role sentinel. Full method and required-check evidence:
`.ufo/waves/round-84/w1/SentinelR84/review.md`. Raw receipts:
`.ufo/waves/round-84/w1/SentinelR84/sandbox-audit.txt` and `draft-audit.txt`.

**Verdict: blocker 0, major 0, minor 3, informational 1.** The bubblewrap vector is sound — network
unshared, host home/lane absent, `/usr` and `/etc` read-only, only the per-case directory bound at `/app`,
subject and harness read-only, env cleared to an explicit allowlist, receipts parsed and never executed.
The three minors are defense-in-depth hardening with tested fixes that keep the frozen subject green.

## Reviewed bytes

| artifact | sha256 |
|---|---|
| `plans/round83_code_image_probe.py` (baseline) | `21922612c84b82c0a98a4c98a36ed9b11410841c82c89bd9556064f8868bae23` |
| `.ufo/waves/round-84/w1/ProbeR84/round84_gcode_probe.py` | `82f359e67840ec5ed876dc1904c0f69b158d2f1bc33278df3dfd64c51d528e75` |
| `.ufo/waves/round-84/w1/CounterR84/round84_c1_replay.py` | `ea8cfdda495959b5ceeac52ca2e2a8581562c89c7edacfba9cc9ae0670bb61ee` |

Both R84 drafts were **ABSENT** at the first check (2026-11-04T15:39Z); they appeared at 15:46Z. The review
is pinned to the snapshot hashes above (copies under `SentinelR84/reviewed-*.py`); live files matched at
18:53Z. A later change needs a diff re-review.

## Findings

| id | severity | file:line | evidence | fix |
|---|---|---|---|---|
| S1 | minor | `ProbeR84/round84_gcode_probe.py:176-177`; `plans/round83_code_image_probe.py:76-77` | `--dir /tests` leaves the directory writable; only `/tests/test_outputs.py` is `--ro-bind`. Diagnostic: `write_tests=ok`, `unlink_tests_file=OSError EBUSY`. The subject file cannot be replaced (mountpoint busy), and it is the only file read from `/tests`, so no integrity break today. | Stage each subject as `<dir>/test_outputs.py` and `--ro-bind <dir> /tests` (drop `--dir` + file bind; selftest fixtures need the same per-fixture staging). Verified: write and unlink → `EROFS`; subject legs `P/P`. |
| S2 | minor | `ProbeR84/round84_gcode_probe.py:170`; `plans/round83_code_image_probe.py:70` | Nested user/mount namespaces creatable inside: `unshare -U true` rc 0; `unshare -U -r -m -- mount -t tmpfs none /tests` rc 0. `CapEff 0`, `NoNewPrivs 1`, `Seccomp 0`. Containment holds (no host mounts), but the nested userns kernel surface stays open. | `--unshare-user --disable-userns --assert-userns-disabled` (the flag requires an explicit `--unshare-user`). Verified: nested unshare rc 1; harness rc 0. |
| S3 | minor | `ProbeR84/round84_gcode_probe.py:170-181`; `plans/round83_code_image_probe.py:70-81` | Writable tmpfs mounts are uncapped: 100 MiB to `/` and 100 MiB to `/dev/shm` both succeed; root mount is `rw … tmpfs`. A compromised subject can pressure host memory until the 60 s per-case timeout. | `--size 67108864 --tmpfs /` (before the `/usr` `/etc` binds; `--size` must precede `--tmpfs`) and `--size 67108864 --tmpfs /dev/shm` after `--dev /dev`. Verified: both writes → `ENOSPC`; subject `P/P` under the sized root. |
| S4 | info | `ProbeR84/round84_gcode_probe.py:175`; `plans/round83_code_image_probe.py:75` | `/proc/self/mountinfo` discloses host bind sources (`/@home/vgpnk/Projects/shokunin/kengaku-shokunin/...`, `/scratch/hyaku/...`). Disclosure only; no access. | Drop `--proc /proc` if not needed (the pinned tests use `pathlib` only), or accept. |

No blocker/major: no host home/lane bind, no network namespace, no credential passthrough, no receipt/ledger
execution, no `shell=True`, no secret-path read.

## Required-check summary

| check | result |
|---|---|
| network namespace | PASS — netns inode `4026533568` ≠ host `4026531833`; `1.1.1.1:80` → `ENETUNREACH` (`--unshare-all`, no `--share-net`) |
| host `/app` write | PASS — `/app` source is `<work>/case-*/app`; host `/app` absent; `/app/..` is the sandbox root |
| `/tests` read-only | **PARTIAL (S1)** — file `ro`, unlink `EBUSY`; directory writable |
| `/usr`, `/etc` read-only | PASS — writes `EROFS`; mountinfo `ro` |
| `$HOME` bind | PASS — `/home`, `~/.ssh`, `~/.omp`, `~/.config` absent in sandbox |
| lane/fleet-root bind | PASS — only `/usr`, `/etc`, case app, staged subject, harness; mountinfo confirms |
| env credentials | PASS — `--clearenv` + `PATH`/`LANG`/`LC_ALL`; observed env exactly those (+ bwrap `PWD=/app`) |
| `/tmp` writes | PASS — no `/tmp` in sandbox (`ENOENT`); host temps under `TemporaryDirectory(dir=work)` with `TMPDIR=work` |
| receipt/ledger code execution | PASS — probe has 0 `RECEIPT`/`LEDGER` references and executes only the pinned capture; counter parses with regex/`shlex.split`; hostile `COMMAND ...; touch <path>` matched `False` and did not create the file |
| `shell=True` | PASS — 0 occurrences in all three; list argv only |
| secret reading | PASS — 0 references to `/.ssh`, `/.omp`, `/.config`, `/home/`; `/etc/shadow` is 600 root |
| bwrap 0.13.1 options | PASS — `--help` lists `--unshare-all/-user/-net`, `--clearenv`, `--ro-bind`, `--bind`, `--dir`, `--proc`, `--dev`, `--new-session`, `--die-with-parent`, `--disable-userns`, `--assert-userns-disabled`, `--size` |

## Adjacent observations (not counted)

- `CounterR84:307` forwards the full host environment to the instrument (`env=dict(os.environ, TMPDIR=…)`);
  the sandbox stays clean because the probe runs bwrap with `env={"PATH": "/usr/bin"}` and `--clearenv`.
- `plans/round84-cases.json` is absent at BASE `4087b2f8` and FREEZE `b12a9d4`; the counter's
  `load_freeze_table` returns `None`, `validate_frozen_table` is skipped, and the table is anchored by the
  receipt `CASE_TABLE_SHA`, the `CLAIMS_CASES` vectors and the probe's sibling `FROZEN_TABLE_SHA` — a
  provenance note, not a sandbox defect.
- The `/app` bind is host-backed rw by design (allowed by the frozen claim). Both legs only read, so
  `--ro-bind` of the case app is an optional extra (verified `P/P`), not required.

Verification was read-only on production; no build/lint/test suites, no production edits, no tool installs.
