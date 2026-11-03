# ControlProbe — reverse-engineering the pypi-server grader install step, K2 stderr clause

Seat: ControlProbe (revenger). Round 63 wave 1. Absolute paths only. Scratch root
`/fast/scratch/hyaku/kengaku-r63/ControlProbe` (removed before yield); the receipts this note
cites were copied into this seat dir first. No tool installs were made (pacman is paused; nothing
needed uv/npx, so the tooling record is empty).

## 0. Environment and grader bytes

```
$ python3 -VV
Python 3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]
$ <scratch>/venv/bin/python -m pip --version
pip 26.2.1 from /fast/scratch/hyaku/kengaku-r63/ControlProbe/venv/lib/python3.14/site-packages/pip (python 3.14)
$ sha256sum <scratch>/tests/test_outputs.py
82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c
```

The copied grader matches the frozen value (`corpus/evidence/round52/graders/SHA256SUMS`
line 134). Source copy: `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`.

## 1. Port 8080 free at seat start

```
$ ss -ltnp | grep ':8080 ' || echo none
none
```

A sibling seat (PypiRecon, pid 2647985) transiently bound 127.0.0.1:8080 at 15:05, and another
`python3 -` at 15:11; every capture kept here was taken with 8080 free on both families at run
time (checked immediately before each run). No process I did not start was killed.

## 2. K2 — the assignment's exact command, stderr captured

```
$ env -i PATH=<venv>/bin:/usr/bin:/bin HOME=<scratch>/home PIP_DISABLE_PIP_VERSION_CHECK=1 \
    <venv>/bin/python -m pip install --index-url http://localhost:8080/simple vectorops==0.1.0 \
    > <scratch>/k2-stdout.txt 2> <scratch>/k2-stderr.txt ; echo rc=$?
rc=1
```

stdout — 49 bytes, 1 line, sha256 `ea9942beb4cf4c2a75914369e94d6f9b59857d9816a18b4dc01af734193d75d2`:

```
Looking in indexes: http://localhost:8080/simple
```

stderr — 1526 bytes, 7 lines, sha256 `dedbc20d70cc292e39eec807222312473313ee274e3a8db8476e3e0d8565375d`,
first five lines:

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new connection: [Errno 111] Connection refused")': /simple/vectorops/
```

lines 6-7:

```
ERROR: Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: none)
ERROR: No matching distribution found for vectorops==0.1.0
```

A second run reproduced the stderr byte for byte (`cmp` identical, sha256 `dedbc20d…`).

## 3. The clause: does K2's stderr name localhost:8080?

```
grep -c "localhost:8080"     0
grep -c "host='localhost'"   5
grep -c "port=8080"          5
grep -c "Errno 111"          5
grep -c "::1"                0
```

Verdict: **False for the contiguous literal, True for the host/port pair.**

pip 26.2.1 (vendored urllib3 2.7.0) renders the refused endpoint as
`NewConnectionError("HTTPConnection(host='localhost', port=8080): Failed to establish a new
connection: [Errno 111] Connection refused")`. The literal `localhost:8080` appears **0** times
in stderr and **once** in stdout (`Looking in indexes: http://localhost:8080/simple`).

The probe implements exactly this reading: `ENDPOINT_PATTERNS` carries a `url` pattern and a
`urllib3-host-port` pattern; applied to this capture it returns `urllib3-host-port`.

The committed do-nothing control `corpus/evidence/round63/control-k2.txt` has one
`localhost:8080` match, but that match is the argv echo inside the CalledProcessError message
(`Command '['python', '-m', 'pip', 'install', '--index-url', 'http://localhost:8080/simple', ...]'`);
that file carries no pip stderr at all (`grep -c port=8080` = 0, `grep -c "Errno 111"` = 0).
So the committed control never demonstrated the stderr clause; this seat's capture does.

## 4. pip also tried ::1 — measured

```
$ env … strace -f -e trace=connect -o k2-clean.trace <venv>/bin/python -m pip install …
$ grep 'htons(8080)' k2-clean.trace
connect(3, {sa_family=AF_INET,  sin_port=htons(8080), sin_addr=inet_addr("127.0.0.1")}, 16) = 0
connect(3, {sa_family=AF_INET6, sin6_port=htons(8080), … inet_pton(AF_INET6, "::1", …)}, 28) = 0
connect(3, {sa_family=AF_INET6, sin6_port=htons(8080), … inet_pton(AF_INET6, "::1", …)}, 28) = -1 EINPROGRESS
connect(3, {sa_family=AF_INET,  sin_port=htons(8080), sin_addr=inet_addr("127.0.0.1")}, 16) = -1 EINPROGRESS
```

Per attempt pip makes one UDP source-address probe and one TCP connect to each of ::1 and
127.0.0.1. Over the run: **6 v4 + 6 v6 TCP connects** (1 initial + 5 retries), all refused
(EINPROGRESS ⇒ ECONNREFUSED on poll). `getaddrinfo("localhost")` returns ::1 FIRST on this host
(`/etc/hosts` lines 3-4; `getent ahosts localhost` agrees), so ::1 is attempted first.

Inside the probe's bwrap sandbox the same command makes **only 6 v4 connects, no v6**: the
sandbox binds `/etc/hosts` (both lines) but not `/etc/host.conf`, and glibc's `multi on` from
`/etc/host.conf` is what makes it return both families. Sandboxed, `getaddrinfo("localhost")`
→ 127.0.0.1 only (measured with the probe's own `sandbox_argv`).

## 5. The grader's install step, reconstructed

```
23:    uninstallcmd = ["python", "-m", "pip", "uninstall", "-y", "vectorops"]
25:        "python",
58:        ["python", "-m", "pip", "show", "vectorops"],
```

- argv[0] is the bare word `python` in all three subprocess calls (uninstall, install, show):
  resolution goes through PATH (`subprocess.run` with no `executable=`). Verified:
  `env -i PATH=<venv>/bin:/usr/bin:/bin sh -c 'command -v python'` → `<venv>/bin/python`;
  `env -i PATH=/usr/bin:/bin …` → `/usr/bin/python`, which has no pip module.
- uninstall runs with `check=True`; the grader catches CalledProcessError and tolerates it only
  when the lower-cased stderr contains `not installed` or `no files to remove`.
- Under pip 26.2.1 (also 25.3 and 23.0.1 measured here) `pip uninstall -y vectorops` on a clean
  venv exits **0** with `WARNING: Skipping vectorops as it is not installed.` on stderr, so the
  except branch is never taken; the grader prints "Successfully uninstalled existing vectorops
  package".
- install runs with `check=True`; its stderr is what K2 reads.
- `pip show vectorops` exits 1 when absent (only reached after a successful install).

Alternate F path measured: if `python` on PATH is `/usr/bin/python` (no pip module), the
UNINSTALL raises CalledProcessError with stderr `/usr/bin/python: No module named pip`; the leg
is then F for a reason that names no endpoint (`alternate-f-path-no-pip-stderr.txt`). K2's stderr
is a discriminator only because the probe dictates PATH.

## 6. Toolchain dependence of the clause (divergence: reported, not edited)

```
pip 26.2.1 / urllib3 2.7.0    K2 stderr: host='localhost', port=8080        literal 0, pair 5
pip 25.3   / urllib3 1.26.20  K2 stderr: <…HTTPConnection object at 0x…>   literal 0, pair 0, "8080" 0
pip 23.0.1 / urllib3 1.26.14  same object-repr form
```

The grader's own `tests/test.sh` pins `-w pip==25.2` (line 21) for its uvx pytest environment.
Under the urllib3 1.26 line (pip 25.3 and 23.0.1 measured) the refused-endpoint message names
**neither** localhost nor 8080 — it prints the connection *object* repr. Under pip 26.2.1 the
host/port pair appears. So the frozen clause is satisfiable only under pip ≥ 26 (urllib3 2.x).
The probe runs the host venv's pip (26.2.1), not the grader's pinned 25.2; that is why it passes.

Second dependence: the endpoint appears only in the **retry WARNING** lines. With
`PIP_RETRIES=0` the stderr is just the two ERROR lines and names no endpoint
(`pip-retries0-stderr-sample.txt`). The probe does not set `PIP_RETRIES`, so the default 5 applies.

## 7. Port-guard blind spot and the ::1 hijack (attack evidence)

The probe's `port_free()` / `port_listening()` bind/connect 127.0.0.1 only. With a foreign
listener on `[::1]:8080` and nothing on v4, `port_free()` still returned True — the guard cannot
see a v6 holder (measured). On the bare host pip prefers ::1, so a foreign v6 listener can serve
the grader leg:

```
setup: 127.0.0.1:8080 = wrong-math index (probe-owned); [::1]:8080 = correct index (foreign)
result: LEG P; probe-owned index served 0 /simple requests; foreign index served 2
```

(For K1 the same setup with both indexes correct gives LEG P with the probe index serving 0.)
Inside the probe's bwrap sandbox this hijack is NOT reachable via `localhost` (sandbox resolution
is v4-only, §4), so the probe did pass with a v6-only foreign listener present
(`probe-run-with-foreign-v6-listener.txt`: `PREDICATE R63-C1 pass`, its own index served 2
requests). That protection is a side effect of not binding `/etc/host.conf`, not a check.

A foreign **v4** service on 127.0.0.1:8080 while the K2 driver starts nothing flips the K2 leg to
**P** (`k2-with-foreign-v4-index-leg.txt`) — the kill-rule case the probe guards with
`require_port_free` plus the "Errno 111 / Connection refused" requirement.

## 8. Receipt binding (for the L1)

`--check-receipt` on the probe's own receipt prints `CHECK ok` / `PREDICATE R63-C1 pass`, but the
receipt carries only the self-reported line `K2 stderr_mentions_8080=True`; it embeds no stderr
sha256 and no path. A copy of the receipt with no stderr file beside it still returns rc=0
(measured). So the K2 clause is not bound to committed bytes by the counting command.

## 9. Evidence-file defect in the draft (for the L1)

`corpus/evidence/round63/k2-pip-stderr.txt` as drafted is a 4-line / 1092-byte **prefix**
(sha256 `505dc930ac5f04eaa31f1957e28de2a1100f35730a762d795129975cdb2074f6`) of the 7-line /
1526-byte capture (sha256 `dedbc20d…`): it stops at `Retry(total=1)` and omits `Retry(total=0)`
and both ERROR lines. The knowledge entry says `grep -c 'port=8080'` → 5; on that 4-line file the
count is 4. The 7-line file (`k2-pip-stderr-repro.txt`, same sha as this seat's capture) is the
one that matches the entry text and the probe's own captured bytes.

## 10. Error class lines (acceptance)

```
stderr line 6: ERROR: Could not find a version that satisfies the requirement vectorops==0.1.0 (from versions: none)
stderr line 7: ERROR: No matching distribution found for vectorops==0.1.0
grader exception class: subprocess.CalledProcessError (rc 1)
```

`ERROR: No matching distribution found for vectorops==0.1.0` is pip's terminal error-class line;
the grader surfaces `CalledProcessError`.

## Files in this seat dir

| file | what |
|---|---|
| k2-pip-stderr.txt | K2 pip stderr, 7 lines, sha256 `dedbc20d70cc…` (identical to k2-pip-stderr-repro.txt and to the probe's own captured file) |
| k2-pip-stderr-repro.txt | second, byte-identical capture |
| k2-pip-stdout.txt | pip stdout: the URL literal lives here |
| k2-grader-exception.txt | the grader's own `test_api` run: exception class, stderr presence |
| k2-connect-attempts.txt | host strace: 6 v4 + 6 v6 TCP connects per K2 |
| k2-connect-attempts-sandbox.txt | same inside the probe sandbox: v4 only |
| k2-connect-attempts-unshare-net.txt | same inside `bwrap --unshare-net` |
| pip-version-matrix.txt | urllib3 2.x vs 1.26 rendering of the refused endpoint |
| pip25.3-k2-stderr-sample.txt | stderr under pip 25.3 / urllib3 1.26.20: no endpoint named |
| pip-retries0-stderr-sample.txt | `PIP_RETRIES=0` removes the endpoint lines |
| pip26-404-foreign-stderr-sample.txt | a foreign 404 service: URL literal appears 2x |
| uninstall-stderr-clean-venv.txt | pip uninstall on a clean venv: WARNING + rc 0 |
| alternate-f-path-no-pip-stderr.txt | F path with no pip on PATH: names no endpoint |
| k1-hijack-*.txt / k3-hijack-*.txt | foreign `[::1]:8080` index serves the leg while the probe index serves 0 |
| k2-with-foreign-v4-index-leg.txt | foreign v4 index flips K2 to P |
| probe-run-with-foreign-v6-listener.txt | probe run with a v6-only foreign listener present: pass |
| venv39-foreign-install.txt | pip 25.x install succeeding against a foreign index on 8080 |
