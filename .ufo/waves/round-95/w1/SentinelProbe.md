# R95 w1 SentinelProbe — security/isolation probe of plans/round95_vuln_probe.py @ T

Audited bytes: `plans/round95_vuln_probe.py` sha256 `932e66b1e47662b687a4fe9994b09ebda8453e8dc2e0b1728569adbd9bb1c775` — equals the frozen-instruments table row (F). Lane clone at T `afe9c229e37aecc0b52b78b0e5c7dd80cf0cf239` (git clone --shared, checkout --detach). All scripts run by absolute path from inside the clone. Scratch `/fast/scratch/hyaku/kengaku-r95/SentinelProbe` was removed after receipts were copied to `receipts/` here (the 6.1 MB raw strace log was too large to keep; every cited number below is reproduced in the copied receipts). Host: bwrap 0.13.1, strace 7.2 (preinstalled — **no tools installed or upgraded**, pacman untouched), python 3.14.8, kernel 7.2.11-arch1-1. `/proc/sys/user/max_user_namespaces` read only (122865), never written. No sysctls modified.

Raw receipts (this dir, `receipts/`): `probe-stdout.txt` (honest run receipt, rc=0, 15/15 ok), `probe-stderr.txt` (0 bytes — clean), `trace-analysis.md`, `trace-bwrap-argv.txt` (23 bwrap argv heads), `trace-execve-env-sample.txt` (sandboxed solve.sh envp), `netns-receipt.txt`, `inside-env-values.txt`, `outside-env-values.txt` (synthetic env only), `env-leak-remediation-pair.txt` (redacted contrast pair), `hostile-receipts.txt`, `analyze_trace.py` (method).

## Sandbox construction (source facts, plans/round95_vuln_probe.py at T)

`sandbox()` (lines 92–104): `bwrap --die-with-parent --unshare-all --tmpfs / --ro-bind /usr /usr --ro-bind /etc /etc --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --dev /dev --proc /proc --tmpfs /tmp` + per-case binds + `--setenv PATH /usr/bin --setenv HOME /tmp --setenv LANG C.UTF-8 --chdir <dir> <argv>`. **No `--clearenv`.** `run_case`: `--bind <work>/cases/<id>/app /app` (rw), `--ro-bind tests /tests`, `--ro-bind harness.py /harness.py`, payload `python3 -I -B /harness.py`. `run_solve`: `--bind app /app`, `--ro-bind solve.sh /solution/solve.sh`, payload `bash /solution/solve.sh`. `main`: refuses `--work` inside `--lane` on resolved paths (rc 2), refuses missing/non-exec bwrap (rc 2), refuses `user.max_user_namespaces <= 0` (rc 2), sha256-verifies all four third-party capture files against `PINS` before any case, `rmtree(work/cases)` at the end.

## Check 1 — case writes: confined to scratch /app (PASS)

Command: from the T clone, `env -i TERM=dumb PATH=/usr/bin HOME=$S SENTINEL_CANARY_R95=… FAKE_AWS_SECRET_ACCESS_KEY=… FAKE_GITHUB_TOKEN=… strace -f -v -s 8000 -e trace=%file,%network,%process -o trace-full.log /usr/bin/python3 plans/round95_vuln_probe.py --lane . --work $S/work --bwrap /usr/bin/bwrap` → rc=0, `mismatches 0`, 15/15 `ok=True`, empty stderr (`receipts/probe-stdout.txt`).

Analysis of the full trace (`receipts/trace-analysis.md`, parser kept as `analyze_trace.py`): 362 write-mode openat in the whole process tree. Sandbox-view write paths are exactly: `/app/report.jsonl` (×8 solve cases), cwd-relative `./sedXXXXXX` temporaries (cwd=/app → inside the rw /app bind), relative `solve.sh`/`harness.py` opens, `/dev/null`-family devices, and bwrap's own 46 writes to `/proc/self/{uid_map,gid_map,setgroups}` inside its fresh proc. Zero EROFS, zero writes through read-only binds. Driver writes confined to `$S/work` (52 opens). **No host path outside `$S/work` is written by any process in the run.** Inside the namespace `/` and `/tmp` are tmpfs, so sandbox-relative writes elsewhere (e.g. `/root`) never touch host storage; the only host-visible case write path is the rw-bound scratch app dir.

## Check 2 — sockets: zero AF_INET/AF_INET6 in the run (PASS, with one nuance)

`grep -c 'AF_INET' trace-full.log` → **0**. Only AF_UNIX ×23 and AF_NETLINK ×23 (interpreter startup queries). Nuance: `--unshare-all`'s netns has a down `lo` and no routes — `socket(AF_INET/AF_INET6)` *creation* succeeds; `connect()` fails `ENETUNREACH`; `/proc/net/tcp` empty (`receipts/netns-receipt.txt`, exact replicated argv). "No network" holds for the workload (and nothing in it tried), but the namespace does not deny `socket(2)`; a hard no-socket property would need a seccomp filter (SP3).

## Check 3 — environment leakage: full host env reaches untrusted captured code (FAIL — SP1, major)

`sandbox()` has no `--clearenv`; `--setenv` overrides only PATH, HOME, LANG. Everything else in the invoking process's environment is inherited verbatim by the sandboxed third-party `solve.sh` and by the grader-importing harness python.

End-to-end through the real instrument: the strace'd probe was launched under a synthetic canary env; **all 107 execve lines in the trace carry the canary** — including the captured script's own exec (`receipts/trace-execve-env-sample.txt`):

```
execve("/usr/bin/bash", ["/usr/bin/bash", "/solution/solve.sh"],
  ["FAKE_AWS_SECRET_ACCESS_KEY=AKIAIOSFODNN7FAKEKEY", "FAKE_GITHUB_TOKEN=ghp_FAKEtoken12345",
   "HOME=/tmp", "PATH=/usr/bin", "SENTINEL_CANARY_R95=s3cr3t-canary-token-7f3a", "TERM=dumb",
   "LC_CTYPE=C.UTF-8", "LANG=C.UTF-8", "PWD=/app"]) = 0
```

Key-set replication with the exact base argv (`receipts/inside-env-values.txt`, `outside-env-values.txt`): 16 synthetic vars outside → inside = same set minus PATH/HOME/LANG (overridden) plus `PWD=/` and `_`; canary and both fake credentials present **with values**. This host's real session env demonstrably carries live credential-named variables (`OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN` observed on this host during testing; values deliberately not copied into any receipt) — every probe invocation hands them to the sandboxed captured code. Contrast pair with the fix, values redacted: `receipts/env-leak-remediation-pair.txt` (names-only list, ~130 host vars inside B; 4 vars inside A).

Exploit path: a hostile or drifted capture (pins re-cut on a poisoned upstream, or any future capture refresh) reads the environment inside the namespace. No network blocks direct exfil, but (a) `/app` is a real host scratch dir during the run and the SETUP abort path ("SETUP solve.sh wrote no report") skips the `cases` rmtree, leaving attacker-chosen files on host NVMe; (b) secrets can be encoded into `/app/report.jsonl`, which persists across the subsequent harness run of the same case. Exfil channels are narrow but nonzero; the confidentiality boundary is broken at the env level regardless.

**Smallest remediation, verified working on bwrap 0.13.1:** insert `"--clearenv"` immediately before the three `--setenv` in `sandbox()` (receipt A: inside env becomes exactly PATH/HOME/LANG + PWD). This does not flip R95-C1/C2 verdicts as measured (env participates in no observed vector); routes to round 96 per the frozen rule.

## Check 4 — case /app bind vs the lane tree (PASS)

All 23 bwrap execve lines (`receipts/trace-bwrap-argv.txt`) share the base argv; every per-case bind source is under `$S/work` (`/app` rw; `/tests`, `/harness.py`, `/solution/solve.sh` ro). No bind source is in the lane and `/home` is not mounted in the sandbox at all. `main()` refuses `--work` inside `--lane` on resolved paths. The 7 trace lines mentioning `/home/vgpnk/Projects` are the driver's own read-only `git -C <clone> rev-parse HEAD` walking the shared clone's alternates into the real lane's `.git/objects` (`openat O_RDONLY`/`newfstatat` only) — outside the sandbox, permitted read-only git. Info note (SP5): the guard is one-directional — `--work` that is an *ancestor* of the lane passes the check (bind sources would still be fresh scratch case dirs, so no lane write path opens); hardening only.

## Check 5 — hostile capture: refuses on sha mismatch (PASS)

Scratch fake-lane (captured tree + `plans/round95-cases.json` + probe), `--work` fresh (`receipts/hostile-receipts.txt`):
- one byte flipped in `upstream-bottle/bottle.py` (`d[100] ^= 1`) → `DEFECT SETUP capture sha mismatch upstream-bottle/bottle.py`, **rc=2**;
- restored, one byte flipped in `solution/solve.sh` (`d[50] ^= 1`) → `DEFECT SETUP capture sha mismatch solution/solve.sh`, **rc=2**;
- both refusals stage nothing: `find` over each work dir shows only the empty work dir; the only mutation of the capture tree was the intentional flip (verified by `diff -r` against a pristine copy). Pins cover all four third-party inputs the replay executes or reads; `instruction.md`/`task.toml`/`tests/test.sh` are never executed. Refusal side effect (SP4): `$WORK` itself is created before the pin check — empty otherwise; info only.

## Check 6 — other bounds

`--die-with-parent` and `--unshare-all` in all 23 sandboxes; `CASE_TIMEOUT=300` bounds each case, `guarded()` 60 s. Work-inside-lane refusal exercised by construction in Check 5 (fake lane outside work). Nothing written to the fleet root outside this wave dir; scratch removed at the end.

## Findings

- **SP1 major** — `sandbox()` runs captured third-party code with the invoking process's full environment (no `--clearenv`); canary proven end-to-end in all 107 execve lines incl. `solve.sh`; live credential-named host vars exist on this host. Smallest fix verified: one `--clearenv`. Not verdict-flipping; round 96.
- **SP2 minor** — `/etc` and `/usr` ro-bound into the untrusted-code sandbox: host-wide configuration in `/etc` is readable (`/etc/shadow` is 0600 root:root and unreadable as the mapped uid; no `/etc/netrc` present). `/etc` must stay for `ld.so.cache`; awareness or a curated subset is the remediation. Not verdict-flipping; round 96.
- **SP3 info** — AF_INET/AF_INET6 `socket()` creation succeeds inside the netns (route-less, lo down; connect ENETUNREACH); zero INET sockets in the actual run; seccomp would make it a hard deny.
- **SP4 info** — sha-refusal path mutates nothing but creates the empty `$WORK` dir (mkdir precedes the pin check).
- **SP5 info** — `--work`-inside-lane guard is one-directional (a work dir that is an ancestor of the lane passes); no lane write path opens, hardening note only.

**Verdict-flip statement:** none of SP1–SP5 flips the round-95 C1/C2 verdicts as measured at T; per the frozen rule all route to round 96.
