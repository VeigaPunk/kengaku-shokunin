# SecurityScan — round 64 w1 (read-only security review)

Seat: `SecurityScan` (sentinel). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r64/SecurityScan/` (removed on yield).
No lane file was edited by this seat. No credential file was opened (`~/.ssh`,
`~/.config/gh`, `~/.netrc`, `~/.omp` — existence checked only, contents never read;
no `op://` reference resolved). Tool installs: none.

**VERDICT: findings — 5 findings (1 high, 2 medium, 2 low). No credential leakage:
the credential sweep returns **8 hits over the round's instrument files** (23 over
the whole wave directory), every one a self-reference — a Python local named
`token`, or the R64-C2 escape fixture's path string. The probe's sandbox binds no
host HOME, no `~/.ssh`, no `~/.config`, no `~/.netrc`, no `~/.omp`, no
`~/.config/uv`; its environment is `--clearenv` + 4 `--setenv`; and its port
discipline checks 5328 free before every case and kills only its own recorded PID.
The write scope is clean.**

The high finding is not a leak: it is a **grammar mismatch between the round's own
two C3 instruments** that makes R64-C3's predicate fail on the bytes the wave
produced. It is reported, not edited — the frozen claim says a seat that thinks a
rule is wrong reports it.

---

## 1. Inventory (read-only)

Bounded wait for the five instruments, 20 checks × 60 s (`poll.sh` in this seat's
scratch); all five landed by check 6 (300 s):

```
$ bash /fast/scratch/hyaku/kengaku-r64/SecurityScan/poll.sh
check=1 probe=0 patch=0 sweep=1 addA=0 addB=1 probe_plan=0 sweep_plan=0
check=2 probe=0 patch=0 sweep=1 addA=0 addB=1 probe_plan=0 sweep_plan=0
check=3 probe=1 patch=0 sweep=1 addA=0 addB=1 probe_plan=0 sweep_plan=0
check=4 probe=1 patch=0 sweep=1 addA=0 addB=1 probe_plan=0 sweep_plan=0
check=5 probe=1 patch=1 sweep=1 addA=0 addB=1 probe_plan=0 sweep_plan=0
check=6 probe=1 patch=1 sweep=1 addA=1 addB=1 probe_plan=0 sweep_plan=0
ALL_PRESENT
```

| instrument | path | sha256 |
|---|---|---|
| R64-C1 probe | `.ufo/waves/round-64/w1/ProbeBuild/round64_c1_kvstore_probe.py` | `9f56d25ddb33e14474c6439c16f25dd5545da99e542a051d342113a88b306843` |
| R64-C2 patch | `.ufo/waves/round-64/w1/GateScopePatch/gate-scope.patch` | `2b3282cc69515493313b6bc35320a65df6e351799bb83eaf9783e29cec0c54b7` |
| R64-C2 patched gate | `.ufo/waves/round-64/w1/GateScopePatch/patched-round63_gate_checks.py` | `a98d9c0f75600ea4f99573d2ca291b1ffd97cffc18a53a3a65dce7b7941dfe17` |
| R64-C3 sweep | `.ufo/waves/round-64/w1/SweepBuild/round64_trio_sweep.py` | `56638ea1dfc0ca47ee91dfc0afec9c9fcbbefa9b15d3e163ad423b7f8dbf8bb0` |
| R64-C3 addenda A (15) | `.ufo/waves/round-64/w1/SweepRepairA/*.addendum.txt` | — |
| R64-C3 addenda B (14) | `.ufo/waves/round-64/w1/SweepRepairB/*.addendum.txt` | — |

The sweep is **byte-identical** to the L1-landed `plans/round64_trio_sweep.py`
(same sha256) — every C3 finding below is measured against the integrated file.

## 2. Credential sweep

Command, full output, and the host credential-surface existence check:
**`.ufo/waves/round-64/w1/SecurityScan/receipts/cred-sweep.txt`**.

```
$ grep -rnEI 'op://|hf_[A-Za-z0-9]{10,}|ghp_|...|password[[:space:]]*=|token[[:space:]]*=|...' \
    .ufo/waves/round-64/w1/{ProbeBuild,GateScopePatch,SweepBuild,SweepRepairA,SweepRepairB} \
    plans/round64_trio_sweep.py plans/round64_c1_kvstore_probe.py plans/round63_gate_checks.py
```

**8 hits over the instrument files (23 over the whole wave directory, the extra 15
being this seat's own report/receipt text quoting the pattern list). All 8 are
self-references:**

| file:line | hit | why it is not a secret |
|---|---|---|
| `ProbeBuild/round64_c1_kvstore_probe.py:707,709` | `token =` | Python local `log_token`; the pattern matched the identifier |
| `SweepBuild/round64_trio_sweep.py:146` (= `plans/` copy, both paths counted) | `token =` | Python local `token` holding a frozen-list line |
| `GateScopePatch/red/escape_red_repro{,_head}.py:28`, `receipts/escape-{after,red-repro}.txt` | `/home/vgpnk/.config/uv/uv-receipt.json` | the R64-C2 escape **fixture path string**; no byte of that file was read, copied or embedded |

Over the whole wave directory (`grep -rnEI "$PAT" .ufo/waves/round-64/w1/`,
excluding this seat's own files) the 23 hits break down as: 8 in the four
instrument dirs, 8 in `ProbeMutate/`'s preserved pristine/mutant copies of the same
two instruments, 4 in `GateScopePatch/`'s escape fixture, 2 in `ClaimFalsifier/`
and 1 in `GateScopePatch.md` (the same fixture path). No hit is outside these
self-reference forms.

The 5 ambient credential-shaped env vars (`UV_*`/`PIP_*`/`HF_*`/`GITHUB_*`/`AWS_*`,
incl. `OPENAI_CODEX_TOKEN`) were **counted only; values never printed**. No secret
material is in any wave artifact.

## 3. Sandbox audit of the probe's bwrap argv

Full evidence: **`.ufo/waves/round-64/w1/SecurityScan/receipts/sandbox-audit.txt`**.
The probe's own `sandbox_argv()` (lines 496–517) was reproduced byte-for-byte in a
bwrap run with an instrumented driver.

```
HOME= /tmp
env keys: ['HOME','LC_ALL','PATH','PWD','PYTHONDONTWRITEBYTECODE']   (--clearenv honoured)
exists /home/vgpnk   False      exists /home/vgpnk/.ssh    False
exists /home/vgpnk/.config False exists /home/vgpnk/.netrc  False
exists /home/vgpnk/.omp  False  exists /home/vgpnk/.config/uv False
exists /root         False
```

- **No host credential surface is bound.** `/usr` (ro), the four `/bin /sbin /lib
  /lib64` symlinks, `/etc` (ro), `--proc /proc`, `--dev /dev`, `--tmpfs /tmp`, and
  four `--ro-bind`/`--bind` of probe-owned paths (`/app`, `/tests/test_outputs.py`,
  `/venv`, `/ctl/driver.py`). `/etc/passwd` is world-readable inside; `/etc/shadow`,
  `/etc/gshadow`, `/etc/sudoers` are **not** (PermissionError) and no ssh host key
  is present.
- **Process cleanup verified, not assumed.** `kill -9` on the bwrap parent left the
  sandbox child **gone** and its listening socket **free** — `--die-with-parent
  --new-session` reaps the tree. No orphaned listener survives the probe.
- **Port discipline holds.** 5328 is checked free (`ss -ltn` scan **and** a real
  `bind()` test) at `battery start` and before **every** case; a K2 leg-5 `P` while
  the port was observed free raises `SetupError` and refuses to grade.
  `release_port()` kills **only** the recorded PID and **only** after
  `pid_is_our_server()` reads `/proc/<pid>/cmdline` and finds `/app/server.py` — it
  never kills a foreign listener, never by name or pattern.
- **This seat never bound 5328.** The single TOCTOU experiment was run on
  `127.0.0.1:15328` against a port-rewritten copy of the probe; the foreign process
  was started and stopped by this seat.

## 4. Write-scope audit

Full evidence: **`.ufo/waves/round-64/w1/SecurityScan/receipts/write-scope-audit.txt`**.

- `git status --porcelain corpus/` → **empty**. No seat edited a corpus, lesson or
  knowledge file; the 29 addenda blocks exist only as `.addendum.txt` inside the
  two repair seats' dirs, so the append-only integration remains the L1's job.
- The two modified tracked files (`SKILL.md`, `plans/round54-entrytruth.json`,
  mtimes 16:18:28 / 16:18:57) are the **L1's round-64 round-start registry repair**
  — the diff's own `reason` fields say so, and the L1's own round-start receipts
  (`.ufo/waves/round-64/frontier/{landcheck-start,gates-at-start}.txt`, 16:12–16:13)
  are the measurements behind them. No w1 seat claims either file.
- Every instrument writes only inside its `--work` dir (both selftests use
  `tempfile.mkdtemp(dir=work)` and remove it in a `finally`); the sweep's `--sweep`
  mode writes nothing at all; the probe's `--receipt` path is caller-supplied and
  the probe never chooses a lane path on its own.

---

# Findings

## H-1 — The sweep's two anchored regexes reject every addendum both repair seats produced; R64-C3's predicate fails on the wave's own bytes

**Severity: high (blocks C3; correctness/provenance, not a leak).**

**Exploit path.** A reader trusts `PREDICATE R64-C3 pass` as "29 provenance-trio
repairs re-verified". The instrument's `TRIO-ADDENDUM` classification is decided by
exactly two line-anchored regexes:

```
VERIFIED_RE = re.compile(r"^verified-at:[ \t]*2026-11-03(?:[ \t]|$)")
RECHECK_RE  = re.compile(r"^recheck:[ \t]*\S")
```

The repair seats' bytes do not match them:

- `SweepRepairA/emit.py:138-141` emits `- verified-at: 2026-11-03 (…)` and
  `- recheck: <cmd>` — **markdown bullets**. `^` rejects both.
- `SweepRepairB`'s 14 blocks emit `verified-at: 2026-11-03T19:12:56Z (…)` — the
  date is followed by `T`, but the regex demands `[ \t]` or end-of-line, so it fails.

**Evidence** (landed `plans/round64_trio_sweep.py`, imported and driven on the real
blocks; full log in `receipts/c3-addendum-grammar.txt`):

```
SweepRepairA: ADDENDUM=0  RED=15
SweepRepairB: ADDENDUM=0  RED=14
applied real addenda: 29
LANDED SWEEP on real addenda -> rc=1
  SWEEP files=29 trio_open=0 addendum=0 red=29
  PREDICATE R64-C3 fail
  first NOTE: NOTE addendum-incomplete missing=verified-at: 2026-11-03,recheck: file=corpus/knowledge/attrib-prior-art-r21.md
```

**Impact.** The L1's natural integration — append the repair seats' blocks verbatim
to the 29 frozen entries — yields `red=29` and `PREDICATE R64-C3 fail`. Coverage
is complete (15 + 14 = 29, disjoint halves, `comm -12` empty) and the frozen claim's
words are met by the seats' bytes ("a block containing `verified-at: 2026-11-03` and
a `recheck:` line"); it is the **instrument's** regexes that disagree with them. The
frozen claim cannot be edited by a seat, and this report does not edit it — the
fix belongs to the tool or to the addenda emitter, and it must be dated.

**Smallest remediation.** Either (a) loosen the two regexes to accept the two
emitters' actual shapes — anchor-tolerant (`^[ \t]*-?[ \t]*verified-at:`) and
date-tolerant (`2026-11-03(?:[T \t]|$)`) — or (b) have both emitters write the
canonical shape the tool already accepts (`verified-at: 2026-11-03` at line start,
then `recheck:` at line start). (b) is smaller and keeps the tool's grammar strict;
either way the two must agree, and the wave's own selftest should carry one real
addendum block so the grammar cannot drift again unnoticed.

**Note (not a finding, but adjacent):** the tool also accepts a **one-character**
`recheck:` value — `recheck: x` classifies as `TRIO-ADDENDUM` and flips a red
entry green. Measured: 29 boilerplate addenda (`recheck: x`) → `rc=0`,
`SWEEP ... addendum=29 red=0`, `PREDICATE R64-C3 pass`, indistinguishable from 29
well-formed ones. The tool never executes the recheck command and never checks a
`result:` line, so the claim's "re-verification" is asserted by the addendum's prose.
The claims doc requires "its re-verification command and the observed one-line
result" to be named, and requires the *closure* to re-run it — that remains a
closure duty, but the instrument's own green/red line should not read as proof.

## M-1 — The probe's `uv pip install` inherits the whole ambient environment and the host credential surface

**Severity: medium.**

**Exploit path.** `install_grpc()` (probe lines 408–425) is the round's one named
network open:

```python
proc = subprocess.run([uv, "pip", "install", "--python", str(py),
                       "grpcio", "grpcio-tools"],
                      capture_output=True, text=True)
```

No `env=` kwarg, no `--index-url` pin, no `PIP_CONFIG_FILE=/dev/null`, no
`UV_NO_CONFIG`, no `HOME` override. The install therefore runs with the seat's full
ambient environment and the host's home directory — the same shape the r63 probe
closed (`PIP_CONFIG_FILE=/dev/null` under `env -i`) and the r63 review flagged.

**Evidence** (measured, isolated; receipt `sandbox-audit.txt`):

```
$ env | grep -icE '^(UV_|PIP_|HF_|GITHUB_|GH_|AWS_)'      -> 5   (values never printed)
$ for p in ~/.netrc ~/.config/pip/pip.conf ~/.config/uv/uv.toml; do ... done
absent   /home/vgpnk/.netrc
absent   /home/vgpnk/.config/pip/pip.conf
absent   /home/vgpnk/.config/uv/uv.toml
```

The mechanisms are live on this uv (0.13.0), demonstrated against a local echo
index this seat started:

```
$ HOME=<scratch>/home2  uv pip install --index-url http://127.0.0.1:18099/simple grpcio
REQ /simple/grpcio/ auth=(none)
REQ /simple/grpcio/ auth=Basic TkVUUkNVU0VSOk5FVFJDUEFTUw==      <- netrc credential sent
$ UV_INDEX_URL=http://SECRETUSER:SECRETPASS@127.0.0.1:9/secret/ uv pip install ...
  cause: Failed to fetch: http://127.0.0.1:9/secret/grpcio/          <- UV_INDEX_URL honoured
```

(The base64 above decodes to the *synthetic* `NETRCUSER:NETRCPASS` this seat wrote
into its own scratch `.netrc` — it is not a real credential. `PIP_INDEX_URL` is
**not** honoured by uv; `UV_INDEX_URL` and `.netrc` are.)

**Impact.** On **this** host nothing leaks: `~/.netrc` and `~/.config/uv/uv.toml`
are absent, and no `UV_INDEX_*` var is set. The exposure is the *mechanism*, not a
present breach — a host (or a future lane runner) that has `~/.netrc` for pypi.org,
or a `UV_INDEX_URL` carrying a token, would have that credential attached to the
probe's install request, and `uv`'s cache under the host `HOME` would persist the
resolved artifacts outside the probe's scratch.

**Smallest remediation.** Run the install with a scrubbed environment, as the r63
probe did inside its sandbox: pass `env={"PATH": ..., "HOME": <probe-owned dir>,
"UV_NO_CONFIG": "1", "UV_INDEX_URL": "https://pypi.org/simple"}` (or
`PIP_INDEX_URL` + `PIP_CONFIG_FILE=/dev/null` for pip), and set `UV_CACHE_DIR` to
the probe's `--work` dir so nothing is written to the host cache.

## M-2 — The sweep resolves its frozen list by an **absolute out-of-root path**, the exact shape R64-C2 forbids the gate to accept

**Severity: medium.**

**Exploit path.** `resolve_frozen_list()` falls back to a hard-coded absolute path
outside the lane when the lane-local copy is missing:

```python
FROZEN_LIST_ABS = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round64/trio-red-at-base.txt")
```

Measured on a scratch lane with no local list:

```
resolve_frozen_list -> /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/evidence/round64/trio-red-at-base.txt
inside lane? False
```

**Impact.** The round's own C2 repair makes an absolute out-of-root path token a
named finding (`DETAIL escape=`) in the depth gate; the round's own new C3
instrument accepts exactly such a token as a fallback source of truth. A sweep run
against a clone, a partial tree, or any lane whose `corpus/evidence/round64/` copy
is missing silently grades against the **live lane's** file instead of failing
closed — so the instrument can certify a tree it was not pointed at. It also
hard-codes a host path into an otherwise lane-relative tool, which breaks the
"clean shared clone" measurement the other seats perform.

**Smallest remediation.** Drop the absolute fallback: if the lane-local
`corpus/evidence/round64/trio-red-at-base.txt` is absent, exit 2 with
`SETUP frozen-list-unreadable` — the same "never a vacuous pass" rule the gate
already applies to an unreadable `--receipt`. If a fallback is genuinely wanted,
gate it behind an explicit `--frozen-list` argument (which exists) rather than an
implicit absolute path.

## L-1 — The sweep prints the frozen list's sha256 but never compares it to the committed pin, so a substituted list passes

**Severity: low.**

**Exploit path.** `measure()` computes `frozen_sha` and prints it in the `INFO`
stderr line, but no constant is compared against it — the tool has no pinned sha
of the frozen list at all (`grep -n "fe0498fb\|expected_sha" round64_trio_sweep.py`
→ no match). The cross-check the tool *does* perform compares the observed red set
to the **contents** of whatever list it was handed. Substitute the list and the
cross-check agrees with the substitute.

**Evidence.**

```
# 29 entries all carrying a well-formed addendum, frozen list REPLACED by an empty file:
$ sweep --lane <scratch> --frozen-list frozen-empty.txt
rc=0
SWEEP files=29 trio_open=0 addendum=29 red=0
PREDICATE R64-C3 pass
INFO frozen-list=frozen-empty.txt sha256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 entries=0
```

The committed list's sha is `fe0498fb20b5102b50d80a3eca1258784cdf9d66edf4d9654b10fa99653a080a`
and is printed in the seat's own receipts, so the pin exists on paper — the tool
just does not enforce it.

**Impact.** The `SETUP frozen-list-mismatch` guard only fires when the red set
disagrees with the list *it was given*. A substituted list that matches the
observed red set makes the guard vacuous. This is the same class as the r63
"fabricated readiness" finding and the same class the gate patch closes for path
tokens.

**Smallest remediation.** Pin the frozen list's sha256 as a module constant
(`FROZEN_LIST_SHA256 = "fe0498fb..."`) and treat a mismatch as
`SETUP frozen-list-sha-mismatch` (exit 2), alongside the existing mismatch and
absent-entry guards. One line plus one comparison; it also converts the currently
decorative `sha256=` field into a check.

## L-2 — The probe's sandbox shares the host's PID and network namespaces (carried r63 M-2, still open)

**Severity: low (carried; the round's own claims declare the shared netns).**

**Evidence** (inside the probe's own argv shape):

```
host PIDs visible inside sandbox: 1523
/proc/<host pid>/cmdline  READABLE   (host argv, e.g. /home/vgpnk/.config/Codex/artifact-sessions/... node ...)
/proc/<host pid>/environ  DENIED     (ptrace-mode check)
REACHABLE 127.0.0.1:1234 / :7456 / :39101   True    (host loopback services)
REACHABLE 1.1.1.1:443                         True    (public IP literal)
DNS pypi.org                          gaierror (no /run, so /etc/resolv.conf is a dangling symlink)
```

**Impact.** The frozen claim accepts the shared netns as a necessary cost (the
grader's server must be reachable on loopback) and the shared PID ns follows from
the house shape. The residual exposure is argv-scoped, not file-scoped: no host
credential file is bound, and `/proc/<pid>/environ` is kernel-denied — but any
token passed as a **command-line argument** on any same-uid host process is
readable from inside the sandbox, and host loopback services (plus public IPs by
literal) are reachable. This is the r63 review's M-2, carried, not a new defect.

**Smallest remediation.** Add `--unshare-pid` to the probe's argv (r63 measured
visible host PIDs dropping from thousands to 2) and, if the netns must stay
shared for the loopback server, keep it but document the argv-read exposure in the
receipt the way r63 did.

---

## Notes for the L1 (not findings — no remediation proposed by this seat)

1. **The C2 gate patch is sound for the defect it targets.** The patched
   `_escape_reason()` rejects absolute (`/home/vgpnk/.config/uv/uv-receipt.json` →
   `absolute`), `..`-bearing (`../x.json` → `dotdot`) and out-of-root tokens, prints
   `DETAIL escape=`, and fails the predicate on a nonempty escape set. Measured:
   `SELFTEST GOOD/BAD-COUNT/NO-SECTION/BAD-ESCAPE` 4/4 `finding=ok`, `SELFTEST pass`
   rc 0; the real SKILL section still passes (`ROWS n=16 … paths total=24
   resolved=24 share=1.00`, `PREDICATE R63-C2 pass` rc 0). The escape fixture fails
   with `DETAIL escape=/home/vgpnk/.config/uv/uv-receipt.json`, rc 1.
2. **Residual, lower-severity than H-1, for the L1 to weigh:** the patched gate's
   escape rule is **lexical**. A relative token that traverses a symlink *inside*
   the root to a target outside it is not caught — measured with a symlink
   `root/link -> /home/vgpnk/.config/uv`: `link/uv-receipt.json` → `escape=None`,
   `resolves=True`, target outside the root. The frozen repair text specifies
   exactly the lexical rule (`normpath` + `is_relative_to`), so the patch is
   **conformant**; a symlink-based escape is therefore outside the frozen rule's
   scope, not a deviation from it. Recorded for the claims doc's dated amendment
   section, not as a patch defect.
3. **`plans/round64_trio_sweep.py` is already landed** (byte-identical to
   `SweepBuild/`'s copy, sha `56638ea1…`), so H-1 and L-1 are properties of the
   integrated instrument, not of a draft.

## Receipts written by this seat

- `.ufo/waves/round-64/w1/SecurityScan.md` (this report)
- `.ufo/waves/round-64/w1/SecurityScan/receipts/cred-sweep.txt`
- `.ufo/waves/round-64/w1/SecurityScan/receipts/sandbox-audit.txt`
- `.ufo/waves/round-64/w1/SecurityScan/receipts/c3-addendum-grammar.txt`
- `.ufo/waves/round-64/w1/SecurityScan/receipts/write-scope-audit.txt`

Tool installs: none. No package was installed; no pacman transaction was run.
