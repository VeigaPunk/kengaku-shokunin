# SecurityScan — round 63 w1 (read-only security review)

Seat: `SecurityScan` (sentinel). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r63/SecurityScan/` (removed on yield).
No lane file was edited. No credential file was read (`~/.ssh`, `~/.config/gh`, `~/.netrc`,
`~/.omp`, `op://` refs: existence checked only, contents never opened).
Tool installs: none.

**VERDICT: finding(s) — 4 findings (2 medium, 2 low). No credential leakage found; the
sandbox binds no host home, no `~/.ssh`, `~/.config`, `~/.netrc`, `~/.omp` and no uv
credential directory, and pip runs with `PIP_CONFIG_FILE=/dev/null` under `env -i`.**

---

## 1. Inventory (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin status --porcelain
?? .ufo/waves/round-63/frontier/
?? .ufo/waves/round-63/w1.ready
?? .ufo/waves/round-63/w1.ready.dispatched
?? .ufo/waves/round-63/w1/
```

```
$ find /home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-63 -type f | sort
```
109 files under `w1/` at review time (recon 2 + gate 8 + build 13 + draft 4 + attack 4 + 6 seat
reports + registry + spec + dispatch + frontier census). Nothing under `corpus/`, `plans/`,
`SKILL.md` or `MANIFEST.json` was modified — the round's tracked surface is untouched.

## 2. Credential patterns

Command (one sweep over the round's new files):

```
$ grep -rnE 'op://|hf_[A-Za-z0-9]{10,}|ghp_|BEGIN (RSA|OPENSSH|PRIVATE)|AKIA[0-9A-Z]{16}|password *=|token *=' \
    plans/round-63-claims.md corpus/evidence/round63/ .ufo/waves/round-63/w1/
```

**Zero secret material.** Every hit is the pattern list quoted back inside the wave's own
dispatch spec — self-reference, not a credential:

| file:line | hit | why |
|---|---|---|
| `.ufo/waves/round-63/w1-spec.json:7`, `:27` | `op://` | the harness contract text ("never read … any op:// reference") |
| `.ufo/waves/round-63/w1-spec.json:67` | `op://`, `ghp_` | this seat's own prompt, which lists the patterns to search for |
| `.ufo/waves/round-63/w1-dispatch.json:169`, `:189` | `op://` | the same contract text |
| `.ufo/waves/round-63/w1-dispatch.json:229` | `op://`, `ghp_` | this seat's prompt |
| `.ufo/waves/round-63/w1/KnowledgeDraft.md:83` | `op://` | the sentence "No `op://` reference; no token-shaped literal" |

`corpus/evidence/round63/control-k2.txt` and `plans/round-63-claims.md`: **no match**.

Host-side scan of every readable `/proc/<pid>/cmdline` for the same patterns: **no match**.

## 3. Sandbox design — `build/round63_c1_pypi_probe.py`

The probe's `sandbox_argv()` (lines 332–347) is the only sandbox construction. Verified by
importing the probe module and running its own `sandbox_argv()`:

```
uid/gid inside sandbox: 1000 1000
host home visible: False | .ssh: False | .netrc: False | .omp: False | .config/uv: False
env var count inside: 6
HOME = <work>/home          PIP_CONFIG_FILE = /dev/null
```

- **No host credential surface bound.** The bind set is `/usr` (ro), the `/lib /lib64 /bin /sbin`
  symlinks, `--proc /proc`, `--dev /dev`, `--tmpfs /tmp`, a probe-written `/etc/hosts`,
  `/tests` (ro), the probe-owned venv (ro, site-packages re-bound rw for the install) and the
  probe-owned `HOME` (rw). No `--ro-bind` of `/home`, `~/.ssh`, `~/.config`, `~/.netrc`,
  `~/.omp` or `~/.config/uv`. `/etc` itself is not bound, so `/etc/passwd`, `/etc/shadow` and
  `/var/run/docker.sock` are all absent inside the sandbox (verified by listing).
- **Host pip config dropped.** `PIP_CONFIG_FILE=/dev/null` is in the `env -i` set
  (probe line 310), and the sandbox `HOME` is the probe's own `<work>/home`, so no user-level
  `pip.conf` is reachable. The probe's own K2 stderr evidence contains **0** occurrences of
  `/home/vgpnk` (the sibling `recon/k2-stderr.txt`, run host-side, does contain
  `/home/vgpnk/.cache/pip` — that is the recon seat's own host-side run, not the probe's).
- **`env -i` confirmed.** The environment is built by `/usr/bin/env -i` with exactly
  `PATH`, `HOME`, `PYTHONDONTWRITEBYTECODE`, `PIP_CONFIG_FILE`, `PIP_DISABLE_PIP_VERSION_CHECK`
  (probe lines 307–312); the outer `subprocess.run` also passes `env={}`.

**Gap (M-2 / L-1 below):** the sandbox does **not** `--unshare-pid` and does **not**
`--unshare-net`, so it shares the host's PID and network namespaces.

## 4. curl auth headers

```
$ grep -rn -- '-H ' .ufo/waves/round-63/w1/recon/ .ufo/waves/round-63/w1/attack/
recon/S229-pep-0503.html:108:<dt class="field-even">Post-History<span class="colon">:</span></dt>
recon/k2-stderr.txt:1:WARNING: The directory '/home/vgpnk/.cache/pip' … sudo's -H flag.
```

Neither is a curl auth header (the first is PEP 503 prose, the second is pip's own warning
text). Both curl invocations in this round (seats `PypiRecon`, `SourceReview`, read from
`history://PypiRecon` and `history://SourceReview`) are `-fsSL --max-time 60 <url> -o <file>` —
**no `-H`, no `--user`, no `--netrc`, no cookie jar, no credentials in the URL.** A whole-tree
sweep for `--netrc|--user|--cookie|--oauth2|Authorization:` found nothing.

## 5. Fetched S228 / S229 bytes — secret-shaped content

```
$ grep -nE <patterns> .ufo/waves/round-63/w1/recon/S228-pypi-test_outputs.py   -> no match
$ grep -nE <patterns> .ufo/waves/round-63/w1/recon/S229-pep-0503.html            -> no match
```

- `recon/S228-pypi-test_outputs.py` sha256 `82c6351722e9aa984ff1d701bf57df3150ce51466df2b70afa1aa62d2650be4c`
  — **byte-identical** to the lane capture `corpus/evidence/round52/graders/pypi-server/tests/test_outputs.py`
  (`cmp` → identical), so per the seat brief it is excluded from findings as a match of the
  upstream capture. Reported separately: it carries **no** secret-shaped content of any kind.
- `recon/S229-pep-0503.html` sha256 `5b97cb7e14fc1a384bdfaac70195763e0b3bfca5a4c5f70142c6e37d2c453c4f`,
  byte-identical to `attack/S229-reopen.html` (the independent re-fetch). No credential-shaped
  words (no `password`, `api_key`, `authorization`, `bearer`, `secret`, `private key`) and no
  long opaque token in the file.

---

# Findings

## M-1 — TOCTOU on 127.0.0.1:8080 lets a foreign wheel execute inside the probe's sandbox

**Severity: medium.** **Exploit path:** a foreign process binds 127.0.0.1:8080 in the window
between the probe's `require_port_free()` check and its own `http.server` child binding.
The probe's child then dies with `EADDRINUSE`, but `start_server()` (line 390) only checks
`port_listening()` — which the **foreign** listener satisfies — so it returns a proc it
believes is serving. The grader leg then runs against the foreign index and the foreign
wheel's `__init__.py` executes inside the probe's bwrap sandbox.

**Evidence** (reproduced by importing the probe module and forcing the race; full log in
`attack/security-evidence.txt`):

```
PREDICT K1=P K2=F K3=F K4=F
SERVED K1 requests=0 paths=[]
SETUP K1 confounded: own server served no /simple/vectorops request (log 0 lines)
=== probe exit code: 2
=== receipt written?: False
=== FOREIGN code executed inside probe sandbox (marker in host-visible HOME): True
    marker: FOREIGN_CODE_EXECUTED_IN_SANDBOX
```

Without the race (foreign listener already up before the run) the guard fires earlier:
`SETUP port-8080-occupied (K1 before start)`, exit 2, no receipt.

**Impact.** The *claim counter is not falsified*: the probe's own-server access-log guard
(`served_paths()`, line 430) catches it, no receipt is written and the exit code is 2. The
impact is **code execution of a foreign artifact inside the probe's sandbox**, which — per
M-2 — shares the host's network namespace (loopback services `127.0.0.1:10086`,
`127.0.0.1:1234` and public IP literals are all reachable from inside) and can read
`/proc/<host pid>/cmdline`. A foreign wheel can therefore reach host-local services and
leak argv-borne tokens out of the sandbox. The wave's own contention log
(`attack/PypiMutate/evidence/contention-log.txt`) shows this race was live in practice:
sibling seats held 8080 repeatedly during this round.

**Smallest remediation.** In `start_server()`, after the child is spawned, verify the child
still owns the port instead of trusting `port_listening()`: e.g. compare `proc.poll()` and
require the served log to show the probe's own `GET` line before the leg runs, or bind the
listening socket in-process and hand the fd to the server. Failing that, re-check
`require_port_free()` immediately after the child exits and treat a dead child as
`SETUP`.

## M-2 — The sandbox shares the host's network and PID namespaces

**Severity: medium.** **Evidence** (measured inside the probe's own `sandbox_argv`):

```
host PIDs visible: 2478
REACHABLE 127.0.0.1:10086 (host kimi-webbridge)
REACHABLE 127.0.0.1:1234  (host llama-server)
REACHABLE 1.1.1.1:443     (public IP literal)
DNS example.com: gaierror        (no /etc/resolv.conf — hosts file is loopback-only)
/proc/<host pid>/cmdline READABLE inside sandbox -> token-shaped argv leaks in
/proc/<host pid>/environ DENIED (ptrace-mode read)
```

**Impact.** The frozen claim says the sandbox has "no network beyond loopback"
(`plans/round-63-claims.md:42-43`). Shared network namespace satisfies the letter (the
grader needs the host's 8080) but the sandbox is not loopback-confined: any code executing
there (the grader's `pip install` step pulls a wheel over the network and `pip` executes its
metadata/build hooks) can connect to arbitrary host-loopback services and to public IPs by
literal. With the PID namespace shared, `/proc/<pid>/cmdline` of any same-uid host process is
readable, so a token passed as an argument (`hf_…`, `ghp_…`) on any host command line is
readable from inside the sandbox. `/proc/<pid>/environ` is denied by the kernel's ptrace-mode
check, and no `~/.ssh`, `~/.netrc`, `~/.omp` or uv credential directory is bound — so the
credential exposure is argv-scoped, not file-scoped.

**Smallest remediation.** Serve the index from a probe-owned **child** namespace instead of
sharing the host's: give the leg its own network namespace with the index reachable through a
veth/loopback pair, or add `--unshare-pid` (measured: visible PIDs drop from 2478 to 2) so
host `/proc` is not browsable. If the shared netns must stay for the 8080 hardcode, at
minimum drop `--unshare-all`-style PID sharing and document the argv-read exposure.

## L-1 — The depth gate resolves path tokens outside the lane root

**Severity: low.** **Evidence** (the gate's own code, imported and driven with a synthetic
16-row table):

```
ROWS n=16 class_match=True count_mismatch=0 paths total=2 resolved=2 share=1.00
rc: 0  ->  PREDICATE R63-C2 pass
gate._resolves(lane_root, '/home/vgpnk/.config/uv/uv-receipt.json') -> True
  resolved location: /home/vgpnk/.config/uv/uv-receipt.json ; inside lane root? False
```

`gate_checks.py:192` computes `(root / token).exists()`. `pathlib` treats an **absolute**
token as replacing `root` entirely, and `..` segments are not rejected, so a backticked
pointer to any absolute host path — including a credential-bearing one such as
`~/.config/uv/uv-receipt.json` — counts as "resolved" and inflates the ≥0.90 resolution
share that the R63-C2 predicate prices.

**Impact.** A table can satisfy the depth predicate's path clause while pointing outside
the repository, at host files the gate is supposed to be checking the repo for. The current
draft is clean (all 24 path tokens resolve to real repo files, 0 unresolved, 16/16 class
rows, counts matching the census), so this is a **latent** gate defect, not a live
misstatement.

**Smallest remediation.** In `_resolves()`, reject tokens that are absolute or contain `..`,
and require `resolved.is_relative_to(root)`.

## L-2 — The K2 stderr clause is satisfied by a *foreign* index; the probe's guard is not in the receipt

**Severity: low.** **Evidence.** The frozen predicate reads "K2's captured pip stderr names
`localhost:8080`" (`plans/round-63-claims.md:59`). Measured against a **foreign** index
that answers 200 on `/simple/vectorops/` and 404s the wheel:

```
pip stderr: 'ERROR: HTTP error 404 while getting http://localhost:8080/simple/vectorops/…whl'
literal 'localhost:8080' in stderr: True
'Errno 111' present: False | 'Connection refused' present: False
```

So the literal-string reading of the clause is satisfied by a foreign service, while the
genuinely-quiet case (nothing listening) produces **no** literal `localhost:8080` in stderr
at all — this host's pip 26.2.1 renders it as urllib3's
`host='localhost', port=8080` (5 occurrences in the committed
`build/evidence/k2-pip-stderr.txt`, literal count **0**).

The current probe handles this correctly: `stderr_names_endpoint()` (line 129) accepts both
renderings, and the K2 branch (lines 524–532) additionally requires `Errno 111` /
`Connection refused`, rejecting a foreign answer with `SETUP K2 confounded`. The finding is
that **the receipt records only the boolean** (`K2 stderr_mentions_8080=True`,
`build/pypi-probe.txt:6`), and `--check-receipt` re-derives only from the receipt's own
lines (probe line 705) — it never re-reads the stderr artifact. A hand-edited receipt
therefore still passes:

```
$ python3 build/round63_c1_pypi_probe.py --check-receipt <receipt with index_pid edited to 999999,
                                            no k2-pip-stderr.txt present>
CHECK ok cases=4 vector=P/F/F/F wheel_sha256=6fad8ea86492...
CHECK stored-predicate=pass derived=pass
PREDICATE R63-C1 pass        (rc=0)
```

**Impact.** The receipt is self-certifying for the K2 clause; the confound guard's real
evidence (the `Errno 111` / `Connection refused` markers) lives only in the sidecar file
`build/evidence/k2-pip-stderr.txt`, which the checker does not consult. The predicate is not
falsified by the round's own receipt (it was produced by a clean run), but the checker
cannot distinguish a clean K2 from a doctored one.

**Smallest remediation.** Have `--check-receipt` take the K2 stderr path and require the
refused-marker in it (or record `K2 stderr_refused=True` / the matched form in the receipt
and check that line), so the receipt's own claim is backed by a re-readable artifact.

---

## Non-findings worth recording

- **Base-tip typo in the frozen claims file** (not a security defect, but it will bite the
  next seat): `plans/round-63-claims.md:3` prints the base tip as
  `c78749a5565dfd186f10a1d8ac98e19dac2429666`, which does not exist in the repo
  (`git rev-parse` → *"unknown revision"*). The real base is
  `c78749a565dfd186f10a1d8ac98e19dac2429666` (differing in one hex digit, `556d` vs `565d`).
  Seat `PypiRecon` reported the same. No rule was edited here.
- The probe kills only processes it started: `stop_server()` calls `terminate()`/`kill()` on
  its own `Popen` child by pid; there is no `pkill`, `killall`, `fuser` or `ss`-based kill
  anywhere in the file.
- `swarm-registry.json` is mode `0600`; no credential file was opened by this seat.
- The sandbox binds `/usr` read-only and no writable host path other than the probe-owned
  `site-packages` and `HOME` — the round's lane tree is not writable from inside.

## Files written

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-63/w1/attack/security.md`
  (this file)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-63/w1/attack/security-evidence.txt`
  (raw command/output log for E1–E4)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-63/w1/SecurityScan.md`
  (seat report)
