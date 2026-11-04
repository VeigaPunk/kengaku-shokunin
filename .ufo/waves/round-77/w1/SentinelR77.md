# SentinelR77 — round 77 apparatus security review

Axes: coverage (eight requested confinement probes plus typed-rule bypasses); calibration (receipt provenance versus checked bytes). No production remediation performed.

## Evidence identity and method

`git log -1 --format=%H -- plans/round-77-claims.md` returned `9ebb8ed14e0c6f304c67fd4d7125e9673c02e2fb`, rc 0. Claims were read in full before commands. Tests used counter bytes exported with read-only `git show <freeze>:<path>` into `/fast/scratch/hyaku/kengaku-r77/SentinelR77/lane`. This was a scratch snapshot, not a new git clone: its `.git` symlink referenced the source object database for read-only ancestry/object reads; `GIT_OPTIONAL_LOCKS=0` disabled optional index writes. No git mutations, battery modes, receipt-command executions, actual external requests, tool installations, or runtime dispatches were performed.

Counter references below are `plans/round77_c1_declared_surfaces.py` (C1) and `plans/round77_c2_defect_discharge.py` (C2), **at the freeze**, unless explicitly called worktree. Relevant lines were located using the grep tool (`urlopen|create_connection|read_bytes|read_text|TOOL_SHA|write_text|mkdir|rmtree|/fast|/tmp`) and read directly.

CLI shorthand actually executed by the Python subprocess driver, cwd at seat scratch root:

- `C1`: `python3 -B <scratch>/lane/plans/round77_c1_declared_surfaces.py --lane <scratch>/lane [--receipt <scratch>/receipt-c1.txt]`.
- `C2`: same command with `round77_c2_defect_discharge.py` and optional `receipt-c2.txt`.
- In-process probes imported the same frozen files with `importlib.util.spec_from_file_location`, then called the named functions below. These print returned tuples, not subprocess exit codes. Transport interceptors prevented egress; proc-content interception prevented reading secrets.

The gate fixtures modified scratch worktree records, not committed production rows. A commit does not change the relevant live network/path resolvers: these same functions process rows read from a revision. No claim is made that hostile fixture records were committed.

## Must-fix

### M1 — High: the claimed no-egress boundary is checked too late for redirects and absent for TCP

**Exploit path:** a PROVINCE HTTP row names a loopback service that redirects to an external hostname; urllib follows it before the final-host check. Alternatively a TCP row directly names a nonloopback host. `cmd` and `path` dispatch also call these resolvers for endpoint-shaped tokens.

**Evidence:** C1:246–261 calls `urlopen` at 251, then checks `resp.geturl()` at 252–254. A fake `HTTPHandler` fed urllib a 302 from `http://127.0.0.1/x` to `http://sentinel.invalid/x`, then a 200. `http_status('http://127.0.0.1/x')` returned `('remote', 'redirect=sentinel.invalid')`, but the handler recorded **two** requests: the loopback URL and the external hostname URL. Both were intercepted, not sent. Direct `http_status('http://192.0.2.1/x')` returned `('remote', 'host=192.0.2.1')` without needing a request.

C1:264–273 passes the parsed TCP hostname to `socket.create_connection` with no loopback restriction. With that transport mocked to raise OSError, `resolve_row(..., 'tcp', '`192.0.2.1:80`', 'absent ABSENT 2026-11-04', reader)` returned `('absent', 'tcp=192.0.2.1:80=closed', 'tcp', [])`; interception recorded `call(('192.0.2.1', 80), timeout=3)`.

**Impact:** committed declarations can cause off-host contact despite the frozen C1 no-egress claim; a later `remote` verdict does not undo contact. No external service access was exercised.

**Smallest remediation:** deny nonloopback TCP before connect; use a redirect handler that validates every destination before opening it (or disallow redirects). Disable ambient proxies and explicitly constrain resolution/addresses if loopback-only is a security guarantee.

### M2 — Medium: V7 does not require a digest and does not actually require a passing predicate line

**Exploit path:** replace all three V7 receipts with an ancestor stamp and claimed pass text, omitting TOOL_SHA. Frozen C2:292 tests `if m_sha and ...`, so missing SHA skips verification. Lines 294–295 search two independent substrings anywhere in the receipt.

**Evidence:** all three scratch rerun receipts contained only `LANE_TIP <freeze>`, `PREDICATE forged pass`, `EXIT 0`. Running C2 returned rc 1 overall (unrelated ledger/correction obligations remained), but printed:

```
LEG V1 ok c1-selftest.txt:tip=9ebb8ed1 c1-mutants.txt:tip=9ebb8ed1
LEG V7 ok V7-routed-open V7-r51-c1 V7-r75-c1
SCOPE ids=7 registered=0 closed=0 open=0 discharged=0 legs_passed=3 legs_pending=0 wrong=11
PREDICATE R77-C2 fail
```

Replacing each V7 receipt with `LANE_TIP <freeze>\nPREDICATE forged fail\nreview note: pass token elsewhere\n` made `leg_v7(reader, lane)` return `('ok', 'V7-routed-open V7-r51-c1 V7-r75-c1')`. A supplied all-zero SHA correctly returned `fail ... TOOL_SHA ≠ tool at tip`.

**Impact:** V7's mandatory tool-digest and passing-predicate requirements are bypassable independently of honest-run provenance. This is not the stated provenance limit.

**Smallest remediation:** require both stamp matches; anchor a required pass line for the expected predicate, and reject contradictory predicate verdicts.

**Concurrent worktree distinction:** `git diff <freeze> -- plans/round77_c1_declared_surfaces.py plans/round77_c2_defect_discharge.py` returned rc 0 and showed a C2-only V7 change: replacing the frozen substring check with mandatory `EXIT 0` plus a loop rejecting nonpassing lines that begin `PREDICATE`. That worktree version still does not require TOOL_SHA or the presence of any predicate line. This observation is source evidence, not a claimed rerun of the worktree version.

## Should-fix

### S1 — Medium: path confinement varies by kind; hash/count can read outside the lane

**Exploit path:** `path` rejects `..`, but `hash`, `count`, and receipt reads bypass that check. Absolute paths and symlinks are also allowed. Outside-lane surface existence is partly intentional given home-directory declarations; arbitrary byte reads and special files are a separate boundary.

**Evidence:** C1:276–297 rejects `..` only in `resolve_path`; `blob_bytes` at 300–311 calls `read_bytes` on absolute/expanded or lane-joined paths without normalization/confinement/type checks. `resolve_count` at 324–334 reads a lane-joined path, and falls back to worktree bytes if revision lookup fails. `resolve_exec` at 345–349 reads an arbitrary receipt path.

A synthetic sibling file `<scratch>/outside.txt` contained one source row. In-process `resolve_row` returned:

- path `../outside.txt`: `escape`, `ESCAPE-ANCHOR`;
- hash `../outside.txt`: `present`, `sha256=f52b30c1…a1566a`;
- count `../outside.txt`, rows=1: `present`, `rows=1 pin=1 path=../outside.txt`.

C1 CLI with the hash row returned rc 1 only because the one-row fixture missed the 28-row target; it printed `SURFACE 1 present hash sentinel sha256=f52b30c1…a1566a ...`, with no row defect.

`resolve_row(..., 'path', '`/proc/self/environ`', 'present', reader)` returned `present` (existence only). For the hash variant, a mocked `Path.read_bytes` returned synthetic bytes; interception counted **one read**, and the resolver returned `hashdrift`. No environment contents were read or reported. A scratch symlink `./device -> /dev/null` was `present` as both path and hash; C1 CLI printed `SURFACE 1 present hash sentinel sha256=e3b0c442…52b855 ...`, rc 1 overall.

**Impact:** untrusted rows can select outside-lane data for hashing/counting and use verdicts as a limited content oracle. [INFERENCE] unbounded reads of a FIFO or `/dev/zero` can hang/exhaust memory; these harmful reads were not run. Absolute hash paths remain live filesystem reads even with `--rev`.

**Smallest remediation:** use one typed read policy: resolve symlinks, require regular files, bound bytes, and explicitly allow intended external roots. Apply traversal policy to hash/count/receipt reads, not only existence checks; do not silently substitute worktree bytes for missing revision count blobs.

### S2 — Medium: brace cap is applied after the expansion allocation

`resolve_path('./{0,...,64}')` returned `overflow`, `brace-targets=65`. A bounded test `resolve_path(lane, './' + '{a,b}'*12)` returned `('overflow', 'brace-targets=4096')` in 0.003653 seconds. C1:182–189 recursively materializes the full product; only 283–284 compares its length to 64. [INFERENCE] larger products exhaust resources before rejection. No large denial-of-service input was executed.

**Smallest remediation:** enforce the 64-output budget while expanding, with a depth/input-length bound, before allocating excess results.

### S3 — Low: malformed loopback URL aborts instead of producing a typed defect

`http_status('http://127.0.0.1:bad/x')` raised `http.client.InvalidURL: nonnumeric port: 'bad'`. Running C1 on that row returned rc 1, stderr ended with that exception, stdout contained no `SURFACE`, `DEFECT`, or `PREDICATE` line. C1:258–261 catches several urllib/OS/value exceptions but not this exception class.

**Impact:** one declaration aborts the census and prevents its normal evidence receipt, rather than returning a machine-readable failed verdict.

**Smallest remediation:** structurally parse and validate URL/port first; convert expected malformed-URL failures into the existing malformed verdict.

## Stated limits / caller trust boundaries

### L1 — Receipt text can prove byte consistency, not an honest execution

C1 exec never executes the declared command. A scratch `never-run.py` contained only `raise RuntimeError("sentinel must never execute")`; receipt `LANE_TIP <freeze>\nrc=0\n` made its row `present`. A complete 28-row scratch fixture (26 existing local paths, this one exec, one REMOTE row) ran C1 with rc 0:

```
SURFACE 27 present exec exec receipt=fake-receipt.txt exit=0 tip=9ebb8ed1
SURFACES total=28 present=27 absent=0 remote=1
AGREE agree=28 disagree=0
DEFECTS n=0
PREDICATE R77-C1 pass
```

The fixture was synthetic, not the actual canonical inventory; this demonstrates the receipt-trust ceiling, not coverage of the real lane. Replacing its stamp with forty zeros made the exec row `execunverified` and printed `DEFECT EXEC-UNVERIFIED ... unresolved`, CLI rc 1. C1 checks script existence, claimed exit text and ancestry, **not a script digest or execution**.

For C2 V1, each fabricated receipt contained the ancestor stamp, the correct tool SHA computed by `Reader.blob_sha(freeze, R76_TOOL)`, and `FABRICATED NO RUN NO TALLIES`. V1 returned `ok` for both. An all-zero SHA returned `fail ... TOOL_SHA ≠ tool at 9ebb8ed1`. Thus a forgery with correct public object digests buys a passing receipt leg, but cannot itself satisfy missing ledger rows, correction legs, ancestry or wrong supplied digests. Overall forged-C2 gate stayed rc 1. V1 also does not independently parse receipt tallies despite its docstring wording (C2:177–197).

**Disposition:** inability to authenticate honest execution is the frozen stated limit, not a demand to execute untrusted receipt commands. Keep provenance review explicit; do not describe SHA equality as evidence that the stamped tool actually ran. The missing mandatory V7 fields remain M2, not this limit.

### L2 — `--receipt` is a wrapper-authorized arbitrary overwrite

C1:571–573 and C2:424–426 create the parent directory and call `write_text` on the caller's path, without confinement, exclusivity or symlink rejection. In two CLI runs, each `--receipt` named a scratch symlink targeting another scratch file **outside the lane**. Both returned rc 1 (failed gates still write receipts). The target marker was removed in both cases; resulting target sizes were 3078 bytes (C1) and 1946 bytes (C2). Both paths remained symlinks.

**Blast radius:** any writable target reachable by the caller-supplied pathname, including symlink destinations; no elevated privilege is acquired. Relative targets are caller-cwd-relative. A bad receipt path can overwrite inputs after they have been read.

**Disposition:** wrapper-trust boundary rather than a row-driven defect: declaration data cannot set this CLI option. A wrapper accepting an untrusted receipt path would turn it into an arbitrary-file overwrite vulnerability. Smallest wrapper fix: restrict to an owned output directory and reject symlinks/nonexclusive targets; do not forward an untrusted path.

### L3 — Scratch/write discipline is lexical and caller-controlled, not a sandbox

Static grep of both frozen counters found normal emit writes only to `--receipt`; fixture and mutant files are rooted under `--work`, and battery receipts under `--receipt`. No hardcoded `/tmp` output sink was found. C1's `/tmp/` occurrence is the input-token regex at line 80, not a write root. **Fixed defaults do exist:** C1:780 `/fast/scratch/hyaku/kengaku-r77/c1`; frozen C2:755 `/fast/scratch/hyaku/kengaku-r77/c2`. They are shared defaults, not per-seat roots. Battery cleanup recursively deletes named children (`case-*`, `mut-*`, `control*`, `git-arms`) under that caller-selected work root.

Explicit seat-owned `--work` is required for concurrent batteries; defaults risk collisions/deleting prior fixture data. Symlinks or a hostile `--work` parent defeat lexical containment. No global syscall/write trace was taken, so this is a source-backed sink inventory, **not a claim of OS sandboxing**. C2 batteries were not run because their source invokes git init/add/commit/checkout, prohibited by this seat's contract. Normal CLI probes used read-only git and explicitly set cwd to scratch. No receipt commands were executed.

## Requested confinement matrix

| Input | Observed boundary |
|---|---|
| `http://192.0.2.1/x` | `remote host=192.0.2.1`; direct HTTP URL blocked before transport |
| Loopback → hostname redirect | external second request reached intercepted urllib handler before `remote` verdict; M1 |
| `../outside.txt` | path rejects; hash/count read synthetic sibling successfully; S1 |
| 65-way brace / 12 binary brace groups | both report overflow, but second materializes 4096 outputs; S2 |
| `http://127.0.0.1:bad/x` | uncaught InvalidURL; CLI rc 1 without predicate; S3 |
| `~root/.bashrc` | `noanchor`, `NOANCHOR`; no home-user expansion/read |
| `/proc/self/environ` | path existence accepted; hash reaches intercepted byte-read; no secrets read |
| Device file | scratch symlink to `/dev/null` accepted/read for hash; no blocking device probe |

## Cleanup and handoff

`shutil.rmtree('/fast/scratch/hyaku/kengaku-r77/SentinelR77')` completed. The immediately printed check was `exists=False; source_git_exists=True`. No seat scratch remains. Only this report was written in the lane. No tools installed. No production patches or commits.

Main should remediate and exercise targeted no-egress, mandatory-receipt-field, bounded-expansion and malformed-input fixtures; this seat has not declared any implementation fixed or any landing target reproduced.

Self-evaluation: accuracy 4 (network effects deliberately transport-intercepted, not real external access); completeness 4 (all eight inputs covered, battery writes inspected statically because mutating git is forbidden); clarity 4 (freeze/worktree distinction required extra detail); actionability 4 (smallest fixes named, not implemented under read-only scope); conciseness 4 (longer evidence matrix retained for auditability). Overall 4.0. Highest-impact next action: repair pre-contact confinement and mandatory V7 validation without expanding the frozen claims.
