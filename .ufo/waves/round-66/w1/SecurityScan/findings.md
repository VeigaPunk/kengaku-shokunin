# SecurityScan — R66 adversarial security review

Seat: SecurityScan (wave r66 w1, v1). Scope: the R66 C1 tensor probe, its five cases, the
proposed registry counter, and the install channel recorded in `plans/round-66-claims.md`.
Read-only: no lane file was edited; all experiments ran in `/fast/scratch/hyaku/kengaku-r66/SecurityScan`
(now removed) and in throwaway `bwrap` sandboxes under `/tmp`-free scratch paths.

Method: every line below is backed by an executed command whose output I observed. Line numbers are
from the committed bytes (`plans/round66_c1_tensor_probe.py` sha256
`c5ef1b54c89fc9023129220e2846f43b6c6c358f92dce7d74ab4e9beb08ad5f3`).

---

## M-1 — must-fix — `--check-receipt` accepts a hand-written receipt with no per-case evidence

**Exploit path.** The counting command for R66-C1 is
`python3 plans/round66_c1_tensor_probe.py --check-receipt corpus/evidence/round66/tensor/receipt.txt`.
`check_receipt` (probe lines 240–277) validates the `GRADER` line, the `PROBE` line, the five
`VECTOR` lines against the frozen table, and — only for `CASE` lines that happen to be present —
the `case_sha`/`junit_sha`. It never requires that a `CASE` line exists, and it never re-derives
the vectors from the junit XML.

Observed, with a receipt I wrote in scratch containing only the `GRADER` line, the correct `PROBE`
sha, the five frozen `VECTOR` lines and the `PREDICATE … pass` line — **no `CASE` line, no junit
file at all**:

```
CHECK ok cases=5
PREDICATE R66-C1 pass          exit 0
```

Worse: with a self-authored `junit/` directory next to that receipt, and with junit XML whose every
`<testcase>` carries `<failure message="fabricated"/>` — bytes that directly contradict the
claimed all-P vector — the check still returns:

```
CHECK ok cases=5
PREDICATE R66-C1 pass          exit 0
```

The vector is asserted by the receipt, never verified against the junit bytes. The `junit_sha` is
checked only as "the file at `<receipt.parent>/junit/<case>.xml` hashes to what the receipt says" —
self-consistent by construction, since the receipt author chooses both.

**Evidence.** Probe lines 261–273: the `CASE` loop is `for l in text:` over lines that match; a
receipt with zero `CASE` lines simply never enters the loop and adds no problems. The `VECTOR`
check (249–257) compares `vec` (parsed from the receipt text) to `FROZEN_TABLE`, never to the
parsed junit. `cmd_check` prints `CHECK ok cases=5` from a **hardcoded literal** at line 281 —
`cases=5` is not a count of anything observed. Scratch commands: forge "A" (no `CASE` lines) →
exit 0; forge "C"/"D" (self-made junit, contradictory content) → exit 0.

**Impact.** R66-C1's predicate is "the receipt … carries five `VECTOR` lines whose outcome vectors
equal the frozen table … every `case_sha` and `junit_sha` equals the committed bytes … and the
receipt ends `PREDICATE R66-C1 pass`". A receipt that carries no `case_sha`/`junit_sha` at all
satisfies the *letter* of the predicate vacuously and passes the checker. The commit
`2c1ef88a` shows the lane already knows the shape of this problem: the sibling R66-C2 claim exists
because the R65 checker accepted a fabricated receipt (`corpus/evidence/round66/red/fabricated-r65.txt`,
`red-before-r65-checker.txt`: `CHECK ok cases=5`, `PREDICATE R65-C1 pass`, exit 0). **The C1
counter has the same hole the round is fixing in C2.** The claims' "Named limitation" (line 55)
says "the C1 probe's per-case junit binding is the stronger check" — my forge D shows the binding
is only a self-consistency check, not a binding to committed bytes.

**Smallest remediation.** In `check_receipt`: (1) require exactly one `CASE` line per case and
fail on a missing one; (2) parse the junit XML at `<committed junit dir>/<case>.xml` (the
`JUNIT_DIR` constant, not `receipt.parent`) and re-derive the vector from the testcase names and
`failure`/`error` children — the same rule `run_case` uses at lines 168–176 — and require that
re-derived vector to equal both the receipt's `VECTOR` line and the frozen table; (3) replace the
hardcoded `cases=5` at line 281 with the number of cases actually validated. Then add a selftest
fixture that must be refused: a receipt whose junit contradicts its vector.

---

## M-2 — should-fix — `check_receipt` never re-hashes the grader file

**Exploit path.** `cmd_run` guards the grader with `sha256(GRADER) != GRADER_SHA256` (line 202),
but `check_receipt` only string-matches the `GRADER` line (line 243) and never re-hashes
`GRADER`. Observed: I pointed the module's `GRADER` at a tampered copy of the pinned grader
(sha `3de1539b3e21bc42…` vs pinned `4ae4285e15fba1fc…`) and called `check_receipt` on the
committed receipt:

```
check_receipt against a TAMPERED grader -> ok: True problems: []
```

**Impact.** The grader is the thing the claim is about; if the committed grader bytes drift after
the freeze, `--check-receipt` still prints `PREDICATE R66-C1 pass`. The receipt's own `GRADER`
line is a self-assertion. Combined with M-1, the receipt is not evidence-bound to the grader it
names.

**Smallest remediation.** In `check_receipt`, add
`if not GRADER.exists() or sha256(GRADER) != GRADER_SHA256: problems.append("grader bytes do not match the pinned sha")`.

---

## M-3 — should-fix — `--check-receipt` crashes (unhandled exception, exit 1) on malformed receipts

**Exploit path.** The VECTOR parser is unguarded. Observed, all with a traceback on stderr and
**no `PREDICATE` line printed at all**:

| input | result |
|---|---|
| `VECTOR S999 …` (unknown case id) | `KeyError: 'S999'`, exit 1 |
| `VECTOR k1-ref exists=P bogus frozen=match` (token without `=`) | `ValueError: dictionary update sequence element #1 has length 1; 2 is required`, exit 1 |
| `VECTOR k1-ref exists=P x=y=z frozen=match` (token with two `=`) | `ValueError: … has length 3; 2 is required`, exit 1 |

**Impact.** Exit code 1 is the right *verdict* code, but a crash is not a verdict — the claims
distinguish "could-not-evaluate (exit 2), never a verdict" (kill rule c, line 31). A malformed
receipt produces neither `CHECK defect:` nor a `PREDICATE` line, so an automated consumer
grepping for the predicate sees nothing and cannot distinguish "malformed input" from "predicate
failed". The failing check also prints a Python traceback, which is not a "named finding" in the
sense the R66-C2 predicate requires of its strict mode.

**Smallest remediation.** Wrap the `VECTOR`/`CASE` parsing in `try/except (KeyError, ValueError)`
and convert each into a `problems.append(...)` finding, so a malformed receipt yields
`CHECK defect: …` + `PREDICATE R66-C1 fail` rather than a traceback.

---

## M-4 — should-fix — the sandbox shares the host network namespace; the grader's gloo rendezvous port is host-visible

**Exploit path.** The `bwrap` argv (probe lines 140–162) has **no `--unshare-net`** and no
`--unshare-pid`. Observed with the exact argv from `run_case`:

* The sandbox's `/proc/net/route` shows the **host** interface `enp7s0` and the host default route.
* Outbound internet from inside the sandbox **succeeds**: `connect(('1.1.1.1', 443))` → `OUTBOUND INTERNET OK`.
* Host loopback is reachable from inside the sandbox. I started a host listener on
  `127.0.0.1:12987` and a sandbox process connected to it → `SANDBOX->HOST LOOPBACK REACHABLE`.
* A listener started **inside** the sandbox on `127.0.0.1:12991` appeared in the host's
  `ss -ltn` output, and the host connected to it → `HOST->SANDBOX LISTENER CONNECT OK (netns SHARED)`.
* All 788 host PIDs are visible inside the sandbox; `/proc/1505/cmdline` (a host `llama-server`
  invocation) is readable from inside.

**Impact.** The pinned grader sets `MASTER_ADDR=localhost` / `MASTER_PORT=12355` and
`dist.init_process_group(backend="gloo", …)` (grader lines 30–34). Because the netns is shared,
the rendezvous socket is a **host** socket: any local process on the host can connect to
`127.0.0.1:12355` during a run, and the sandbox can reach every host service on loopback
(`ss -ltn` shows 20+ listeners here). The probe's own `port_busy()` guard (lines 120–124) checks
only `127.0.0.1:12355`; it does not restrict who else may connect. The "offline" capability name
(`offline-torch-tensor-parallel-grader-probe`, claims line 19) is therefore not enforced by the
sandbox — a case file that wanted to could reach the network.

**Smallest remediation.** Add `--unshare-net` to the `bwrap` argv. I verified this is viable and
does not break the grader's requirement: under `--unshare-net` a bind/listen/connect on
`127.0.0.1:12355` **succeeds** (`LOOPBACK RENDEZVOUS OK inside --unshare-net`) while
`connect(('1.1.1.1', 443))` fails with `Network is unreachable`. Add `--unshare-pid` as well to
close the PID-visibility and signal-delivery gaps below.

---

## M-5 — should-fix — no PID namespace: a case can read host process command lines and kill host processes

**Exploit path.** Because `--unshare-pid` is absent, host processes are fully visible and
signallable from inside the sandbox. Observed: `os.kill(<host sleep pid>, SIGTERM)` issued from
inside the sandbox **killed the host process** (`RESULT: host process was KILLED from inside the
sandbox -> signals escape the sandbox`). `/proc/<pid>/cmdline` is readable for same-uid host
processes (observed: `llama-server --models-dir /home/vgpnk/models/lfm3 …`).

**Impact.** The five frozen cases are clean today (see M-9), so this is not currently exploited.
But the probe's own threat model treats `/app` (the case directory) as the untrusted input — the
grader imports and executes case code. Any future or tampered case gets host-process signal
delivery and host-PID command-line disclosure for free.

**Smallest remediation.** Add `--unshare-pid` to the `bwrap` argv (verified harmless: the grader
uses `mp.spawn`, which is unaffected). Verify with the same signal test I ran.

---

## M-6 — note — the receipt's `junit_sha` is checked against `receipt.parent/"junit"`, which for the canonical receipt is the *committed* directory, so a re-run overwrites committed evidence

**Exploit path.** `cmd_run` copies each junit file to `receipt.parent / "junit" / f"{case}.xml"`
(lines 221–223). For the canonical receipt path,
`corpus/evidence/round66/tensor/receipt.txt`, `receipt.parent/"junit"` **is**
`corpus/evidence/round66/tensor/junit/` — the git-tracked directory. Observed: the freeze commit
`9a07df6a` and HEAD hold **different** blobs for every junit file
(`k1-ref`: `440f49e7…` → `fe2b34c4…`), and commit `2c1ef88a`'s own message says
"junit replaced, pre-freeze junit retained at 9a07df6a". So a post-freeze `--run` with the
default receipt path **overwrote committed junit bytes**. The claims' harness-fix note (line 33)
says "the junit directory is receipt-local, so a re-run cannot overwrite committed junit bytes" —
that is true only for a receipt written outside the committed tree; for the canonical receipt path
it is false.

**Impact.** The lane's own receipt-of-record commit already absorbed this; it is visible in git and
recoverable at `9a07df6a`. But the committed `prefreeze-run2.txt` — named the **control of record**
at claims line 33 — no longer verifies: `--check-receipt …/prefreeze-run2.txt` now exits 1 with
five `junit_sha does not match committed junit bytes` defects, because its junit shas point at the
pre-freeze bytes that were replaced. The control's own bytes are only retrievable from git
(`git cat-file 9a07df6a:corpus/evidence/round66/tensor/junit/k1-ref.xml` → sha
`9c02c97350d88956…`, which **does** match the control's claim — I verified this). So the control is
verifiable against the frozen commit, not against the working tree.

**Smallest remediation.** Either (a) have `--check-receipt` resolve junit bytes against a recorded
revision (`git cat-file`) rather than the working tree, or (b) point the receipt of record at a
receipt-local junit dir and keep the committed junit dir as the run's own output, so the two never
alias. Note for the L1: this is a claims/probe-design observation, not a frozen-fact change — I
have not edited either.

---

## M-7 — note — `check_receipt` binds junit to a caller-controlled directory

**Exploit path.** `check_receipt` resolves the junit file as `receipt.parent / "junit" / f"{case}.xml"`
(line 270). The receipt path is caller-supplied (`--check-receipt <path>`), so the directory the
junit bytes come from is caller-supplied too. Observed: a forged receipt plus a self-authored
sibling `junit/` directory was accepted (M-1, forge C/D). Only the *canonical* receipt path binds
to committed bytes, and even then the binding is "hash matches", not "content implies vector".

**Impact.** Same as M-1 — this is the mechanism. Recorded separately because the fix differs:
M-1 is about *requiring* per-case evidence; this is about *where* the evidence comes from.

**Smallest remediation.** Resolve the junit file against the committed `JUNIT_DIR` constant (line 55),
not `receipt.parent`, unless the receipt is at the canonical path.

---

## M-8 — note — `check_receipt` uses `FROZEN_TABLE[case]` on an unvalidated case id

**Exploit path.** Line 251: `FROZEN_TABLE[case]` with `case` taken straight from the receipt
(`m.group(1)`), unvalidated against `CASES`. An id outside `CASES` raises `KeyError` (see M-3).
This is the same root cause as M-3 but a distinct code site; fixing M-3 with a try/except covers
it, and adding an explicit "unknown case id" finding gives a better message.

**Smallest remediation.** Validate `case in CASES` before the table lookup and emit
`CHECK defect: unknown case id <id>`.

---

## M-9 — note (clean) — the five case directories carry no extra file, no file read, no socket, no shell

**Evidence.** `find` over `corpus/evidence/round66/tensor/cases/` returns exactly four files
(`k1-ref`, `k3-stub`, `k4-col-nogather`, `k5-row-noreduce`, each one `parallel_linear.py`); `k2-none`
has no directory at all — the probe synthesises it empty at run time (lines 214–217). `ls -la` per
directory shows no hidden files. A grep across all four case files for
`open(|socket|subprocess|os\.|sys\.|urllib|requests|exec|eval|__import__|Path\(` returns **no
matches** — the cases contain only `torch`/`torch.distributed` tensor logic and the grader's own
`dist.all_gather` / `dist.all_reduce`. The mutants differ from `k1-ref` by exactly one method body
each (K4: `ColumnParallelLinear.forward` loses the all-gather; K5: `RowParallelLinear.forward` loses
the all-reduce), confirmed by diff.

**Verdict.** No finding. The case inputs are the probe's only untrusted surface and they are inert.

---

## M-10 — note (clean) — the `bwrap` bind list exposes no secret and writes the venv read-only

**Evidence.** Full bind list from probe lines 140–162, with mode:

| host path | mode | sandbox path |
|---|---|---|
| `/usr` | ro-bind (141) | `/usr` |
| `/usr/bin`, `/usr/sbin`, `/usr/lib`, `/usr/lib64` | symlink (142–145) | `/bin`, `/sbin`, `/lib`, `/lib64` |
| `/etc` | ro-bind (146) | `/etc` |
| *(new procfs)* | `--proc` (147) | `/proc` |
| *(new devtmpfs)* | `--dev` (148) | `/dev` |
| *(new tmpfs)* | `--tmpfs` (149) | `/tmp` |
| `~/.local/share/kengaku-r66/venv-torch` | **ro-bind** (150) | same path |
| case dir | ro-bind (151) | `/app` |
| `GRADER` file | ro-bind (152) | `/tests/test_outputs.py` |
| `work/ctl/<case>` | **bind (rw)** (153) | `/ctl` |
| *(new dir)* | `--dir` | `/app` (151), `/tests` (152) |

**Secrets visible inside?** No. Observed from inside the sandbox:
`/home/vgpnk/.ssh` → absent, `/home/vgpnk/.config` → absent, `/home/vgpnk/.omp` → absent,
`/root` → absent, `/home/vgpnk` lists only `.local` (the ro-bound venv path),
`/etc/shadow` → present but `PermissionError`, `/proc/<pid>/environ` → `PermissionError` for every
host process (ptrace_scope=1). The lock file `~/.local/share/kengaku-r66/port-12355.lock` is **not**
visible inside the sandbox (it lives one level above the ro-bound venv). No `~/.netrc`, no
`~/.omp` secrets, no `op://` reference is read by the probe at all — grep for
`ssh|netrc|\.omp|token|secret|credential|api_key|http|urlopen|requests|urllib|curl|wget` over the
probe returns only the `socket` import and the `download.pytorch.org` URL inside the
setup-error *message* string (line 205), which is never executed.

**Is the venv writable by a case?** No. Observed from inside the sandbox: writing to
`…/venv-torch/PWNED` and `…/venv-torch/lib/python3.14/site-packages/PWNED` both raise `OSError`
(ro-bind). Note the *parent* directory `~/.local/share/kengaku-r66/` is writable from inside the
sandbox — I wrote `EVIL` there from a sandbox process and it did **not** appear on the host
(verified: host listing shows only `port-12355.lock` and `venv-torch`), because bwrap creates that
parent path inside the sandbox's own tmpfs-backed view. No host escape via this path.

**Verdict.** No secret exposure. The one writable host bind is `/ctl` (the junit output dir), which
is the probe's own scratch, as intended.

---

## M-11 — note (clean) — subprocess discipline and credential paths

**Evidence.** The probe spawns exactly two things: `bwrap` (line 140, `subprocess.run` at 163 with
`timeout=900`, no `shell=True` — grep for `shell=True|os.system|os.popen` returns nothing) and
`bwrap --version` (line 228, for the receipt banner). Inside the sandbox the grader runs
`VENV_PY -m pytest` (line 160) plus the grader's own `mp.spawn` children. No credential path is
read: the only `Path.home()` uses are `VENV_ROOT` (54) and `LOCK` (56). The lock is
`~/.local/share/kengaku-r66/port-12355.lock`, opened `flock(LOCK_EX)` at 207–208, i.e. the
probe's own lock file exactly as the operator brief specifies — the probe never binds or connects
to port 12355 itself; only the *grader inside the sandbox* does, and only via the shared netns
(M-4).

**Verdict.** No finding on subprocess or credential handling.

---

## M-12 — note — the receipt's `TORCH version=` is a hardcoded constant, not an observation

**Evidence.** Probe line 58: `TORCH = "2.15.0+cpu"`, printed verbatim into the receipt at line 228
(`f"TORCH version={TORCH} …"`). The probe never asks the venv what torch version it has. The
installed venv does report `torch 2.15.0+cpu` (observed via
`venv-torch/bin/python -c "import torch,pytest;print(torch.__version__)"` → `torch 2.15.0+cpu pytest 9.2.0`),
so the constant is currently *true*, but it is an assertion, not a measurement — the same
fabricated-readiness pattern the round is otherwise fixing.

**Smallest remediation.** Have `run_case` capture the venv's `torch.__version__` (e.g. from the
junit/`pytest` banner or a one-line `VENV_PY -c` probe) and record the observed value.

---

## M-13 — note — the proposed registry counter: path refusal works, but the id↔capture binding and the capture-eligibility set are loose

**Evidence (all observed).**

*Path refusal — works as specified.* The counter refuses a capture outside `corpus/evidence/`:
`corpus/SOURCES.md`, `/etc/passwd`, `../../../../etc/hostname`, and
`corpus/evidence/../../../etc/hosts` each produced
`CHECK defect: quote S900… refused capture outside corpus/evidence/: …` and exit 1
(counter lines 140–142). A **symlink** planted at `corpus/evidence/link.xml` → `/etc/passwd` was
also refused (the path is `.resolve()`d at line 139 before the check, so the symlink is followed
and the resolved target falls outside `evidence`). Directory-as-capture is refused
(`capture file missing`). The `--root` default is the script's parent, which for the proposed
location is `.ufo/waves/round-66/w1/QuoteGateBuild` — no `corpus/`, so a bare invocation exits 2
`SETUP … has no corpus/ directory (pass --root)`; with `--root <lane>` it works. Selftest passes:
all 13 fixture expectations true, exit 0.

*Loose finding 1 — id↔capture binding is not checked.* A `QUOTE` line naming `S183` but pointing at
**S234's** capture file is accepted:
`QUOTE S183 capture=corpus/evidence/round66/sources/kv-store-grpc-test_outputs.py result=FOUND` →
`CHECK ok quote`, exit 0. The counter checks that the *text* is in the *named* capture; it never
checks that the capture is the one the registry row for that id names. For a gate whose purpose is
"the located quote for S### really comes from S###'s capture", this is the wrong binding.

*Loose finding 2 — capture eligibility is "any file under `corpus/evidence/`".* A `QUOTE` sourced
from the **fabricated** red fixture `corpus/evidence/round66/red/fabricated-r65.txt` is accepted
(`result=FOUND`, exit 0) — the red/ tree is under `corpus/evidence/`, so a lesson could "ground" a
quote in a file that declares itself to contain no live-run data.

*Loose finding 3 — the needle is matched as a raw byte substring of the whole file, not
line-anchored.* A mid-line fragment (`Port {port} is not listening`) is accepted as a "verbatim"
quote, and a needle that spans a line break (`listening - no real gRPC server is running`) is
accepted — `grep -F` would not match the latter. So the counter's "grep -F semantics" claim in its
own docstring (lines 7–8) is stronger than what it implements.

**Impact.** The frontier fix's *stated* checks (quote present in capture; meta phrase absent from
`teaches`) both work; these three loosenesses mean a future lesson could satisfy the gate with a
mismatched source, a red fixture, or a trimmed fragment. It does not affect R66-C1 or R66-C2,
which do not depend on this counter. Not a must-fix for the round's two claims.

**Smallest remediation.** (a) resolve the capture path for the quoted id from the registry row
(`SOURCES.md`) and require the `QUOTE` capture to equal it; (b) exclude the `red/` subtree (and
any path whose name marks it as a fixture) from capture eligibility; (c) match the needle
line-wise — require it to appear as a complete line of the capture, or at least require
`needle` to contain no newline and to be found on a single line.

---

## M-14 — note — install channel: recorded, and the venv is read-only to a case (question 5 answered)

**Evidence.** Claims line 19 records the channel: `uv` 0.13.0 at `~/.local/bin/uv`; torch
`2.15.0+cpu` installed by
`uv pip install --index-url https://download.pytorch.org/whl/cpu torch==2.15.0` into
`~/.local/share/kengaku-r66/venv-torch`; transformers 5.22.1 and pytest 9.2.0 from PyPI into the
same venv. I verified the venv on disk: `pyvenv.cfg` shows `uv = 0.13.0`, `version_info = 3.14.8`,
`include-system-site-packages = false`; `bin/python -c "import torch,pytest"` →
`torch 2.15.0+cpu pytest 9.2.0`. `uv --version` → 0.13.0.

**Is the venv path writable by a case?** No — see M-10: `--ro-bind` at line 150; writes raise
`OSError`. **Is the venv bound read-only into the sandbox?** Yes, `--ro-bind` at line 150, and
confirmed by the write attempts.

**Note on the install record.** The claims list `transformers 5.22.1` as installed into the venv.
It is genuinely irrelevant to this grader — the pinned grader imports only `pytest`, `torch`,
`torch.distributed`, `torch.multiprocessing`, `torch.nn` and `math`/`os`/`sys`/`pathlib`. I did
**not** find `transformers` importable in a way that matters here, and it is not imported by the
grader or by any of the four case files. Harmless, but it widens the venv's surface (and its
download footprint) for no benefit; worth flagging to the L1 as a cleanup, not a defect.

**No credentials in the venv.** `find` over the venv for `pip.conf|.netrc|*.token|credentials*|.env*`
returns nothing; the venv contains only `bin lib lib64 share pyvenv.cfg CACHEDIR.TAG`.

---

## M-15 — note — `resume_continuity_v1` is not present in the R66 surface (no zero-mutation obligation applies)

**Evidence.** `grep -rn "resume_continuity_v1"` across the lane hits only
`corpus/evidence/round13-coverage/r13-planner.md` (and its round-28 scratch copies). Nothing under
`plans/`, `corpus/evidence/round66/`, or `.ufo/waves/round-66/` references it. The R66 artifacts
are a pytest probe, five case files and a registry counter — none of them performs a session
resume, so the "every `resume_continuity_v1` rejection causes zero mutation" property has no
applicable instance here.

**What I checked instead.** The nearest analogue — "a rejection must mutate nothing" — I verified
directly on the checker: three consecutive `--check-receipt` runs against the committed receipt
left all 18 files under `corpus/evidence/round66/` byte-identical (sha256 manifest before/after,
diff empty), and `git status --porcelain corpus/ plans/` is empty. The `--check-receipt` path
writes nothing.

---

## Summary

| # | severity | subject | one-line |
|---|---|---|---|
| M-1 | must-fix | `check_receipt` | A receipt with no `CASE` line, or with junit that contradicts its own vector, passes: `CHECK ok cases=5 / PREDICATE R66-C1 pass`. The C1 counter has the same fabricated-receipt hole C2 exists to fix in R65. |
| M-2 | should-fix | `check_receipt` | Never re-hashes the grader file; a tampered grader passes. |
| M-3 | should-fix | `check_receipt` | Malformed receipts raise uncaught `KeyError`/`ValueError` → traceback, no `PREDICATE` line, not a named finding. |
| M-4 | should-fix | `run_case` bwrap argv | No `--unshare-net`: sandbox reaches the internet and the host loopback; the grader's gloo port 12355 is a host socket. |
| M-5 | should-fix | `run_case` bwrap argv | No `--unshare-pid`: 788 host PIDs visible, host process command lines readable, host processes killable from inside. |
| M-6 | note | `cmd_run` / claims | `receipt.parent/"junit"` aliases the committed junit dir for the canonical receipt path; a re-run overwrote committed bytes, and the control of record no longer verifies against the working tree. |
| M-7 | note | `check_receipt` | junit bytes are resolved from a caller-controlled directory. |
| M-8 | note | `check_receipt` | unvalidated case id → `KeyError`. |
| M-9 | note (clean) | cases | Only `parallel_linear.py` per case; no file read, socket, or shell. |
| M-10 | note (clean) | bwrap binds | No secret visible inside; venv read-only; `/ctl` is the only writable host bind. |
| M-11 | note (clean) | subprocess/creds | Only `bwrap` is spawned; no credential path read; lock file is the operator-specified one. |
| M-12 | note | receipt | `TORCH version=` is a hardcoded constant, not an observation. |
| M-13 | note | registry counter | Path refusal works (incl. symlink and `..` escapes); but id↔capture binding, capture eligibility (`red/` accepted), and line-anchoring of the needle are loose. |
| M-14 | note | install channel | Recorded channel verified on disk; venv read-only to a case; `transformers` is installed but unused by this grader. |
| M-15 | note | scope | `resume_continuity_v1` absent from R66; nearest analogue (rejection ⇒ zero mutation) verified on `--check-receipt`. |

**Files written by this seat:** this file and `.ufo/waves/round-66/w1/SecurityScan.md`.
**Lane files edited:** none. **Installs performed:** none (no tool needed installing; `bwrap`,
`uv`, `python3`, `git`, `ss` were already present). **Scratch:** `/fast/scratch/hyaku/kengaku-r66/SecurityScan`
removed on exit.
