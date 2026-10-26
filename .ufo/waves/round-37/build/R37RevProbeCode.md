# R37RevProbeCode — code review of the frozen C2 probe `plans/git_webserver_probe.py`

Seat: reviewer, kengaku round 37 wave 1 (hyaku run 8) · 2026-10-26.
Object reviewed: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/git_webserver_probe.py`,
sha256 `63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf` — measured
`sha256sum plans/git_webserver_probe.py` → matches the pin in `plans/round37_c2_verify.py`
(`PROBE_SHA256`) and `plans/pkg-spec-r37.json` `frozen_instruments`. The file was reviewed as
frozen; nothing in the lane was edited or written. Captures re-verified before use:
`sha256sum -c SHA256SUMS` in `corpus/evidence/round37/tb2-git-webserver/` → all six `OK`.

Scope (the four assigned questions): (a) does the bubblewrap sandbox isolate the host; (b) is the
harness's direct call of `test_hello_html_exists()` equivalent to pytest's verdict; (c) is the
receipt deterministic by construction; (d) can a case's server race the grader.
Method: every claim is either an executed command with its output (run in scratch
`/fast/scratch/hyaku/kengaku-r37/R37RevProbeCode`, deleted afterwards; artifacts kept in
`.ufo/waves/round-37/build/R37RevProbeCode/`) or a `file:line` citation. `probe:` = the frozen
probe file.

## 1. Sandbox isolation — verified on every asked axis

Executed via the probe's own unmodified `run_case`/`sandbox_argv` with an introspection script
plus a host-side canary HTTP listener on 127.0.0.1:8080 (`driver_introspect.py`,
`introspect-output.txt`):

| Axis | Evidence | Result |
|---|---|---|
| network namespace | host canary listening on 127.0.0.1:8080 while the sandboxed case ran; inside: `socket.create_connection(("127.0.0.1", 8080))` | `NET-8080 ConnectionRefusedError` — `--unshare-net` (probe:204) effective; grader curl can never see a host service and a case server can never take a host port |
| HOME | probe:236 sets `HOME=/work/home`; introspect | `HOME=/work/home`, `HOME-SSH-WRITE ok` — verify.sh:8-10's `> ~/.ssh/config` lands in scratch |
| `~/.ssh/config` untouched | `sha256sum ~/.ssh/config` + `stat` before and after two full 22-case runs and the introspection run | `eb75d8b02cd91b6d703c6d768c2063732c18b5205c2f7704be5be547b10d9f77`, `size=139 mtime=1791725629 ctime=1791725629` — identical before/after |
| /tmp | `--tmpfs /tmp` (probe:209); introspect | `TMP=` (empty, fresh tmpfs), `TMP-WRITE ok`; a canary written inside was absent from host `/tmp` afterwards |
| /tests read-only | ro-binds probe:210-212; introspect append attempt | `TESTS-WRITE OSError`; also `ETC-WRITE PermissionError`, `USR-WRITE PermissionError`, `PROC-WRITE PermissionError` |
| root filesystem | introspect | `ROOT=bin,dev,etc,lib,lib64,proc,sbin,tests,tmp,usr,work` — no `/home`, `/fast`, `/var`, `/run`; only `/usr`+`/etc` (ro) and `/work` (rw scratch) are host-backed |
| environment | probe:236 passes a fixed 6-key env via `subprocess.run(env=…)` (full replacement) | `ENVKEYS=HOME,LANG,LC_ALL,OLDPWD,PATH,PWD,PYTHONDONTWRITEBYTECODE,PYTHONUTF8,SHLVL` — `OLDPWD/PWD/SHLVL` are set by run.sh's bash; no host env leak |
| PID namespace | `--unshare-pid` (probe:204) | `PROC_PIDS=2` inside; after both full runs and at idle, `pgrep -af server.py` → none (see §7 for the transient hits) |

Residual boundary (R1): grader code can *read* host `/usr` and `/etc` (ro) and write `/work`
(scratch) plus its own `/tmp` and `/dev`; it has no host-write path, no host network, no host
processes or home. That is hygiene-grade namespace isolation — appropriate for executing captured
third-party benchmark code, and worth stating precisely rather than as "isolated".

## 2. Harness vs pytest — verdict-equivalent for this capture; one latent divergence

The captured grader is exactly one fixture-less test function: `test_outputs.py:9-13`, module top
level is only `import subprocess` (:5); no fixtures, no skips, no second test. The real reward
mapping is pytest's exit code (`test.sh:14-18` runs `uvx -p 3.13 -w pytest==8.4.1 pytest
/tests/test_outputs.py`; `test.sh:21-25` writes reward 1 iff pytest exits 0).

The probe harness (probe:163-184) monkeypatches `subprocess.run` to tee stdout (:166-171) *before*
`exec_module` (:174), calls `mod.test_hello_html_exists()` (:176), and maps: return → `pass`
(:177), `AssertionError` → `fail` (:178-179), any other exception → `fail error=<class>` (:180-181).
That is pytest's verdict direction for this file. Assertion rewriting changes only the failure
*message*, not the truth value; the receipt instead records verify.sh's own stdout lines
(:182-183), which carry the human-readable reason — nothing evidentiary is lost.

Empirical cross-check (`driver_pytest2.py`, `pytest-equivalence.txt`): real pytest 8.4.1 on
CPython 3.13.16 (uv venv; matches `test.sh:15-16`) inside the same sandbox, on 5 contrasted cases:

| case | frozen receipt | probe VERDICT | pytest rc → verdict |
|---|---|---|---|
| exact-no-newline | pass | pass | 0 → pass |
| capitalised | fail | fail | 1 → fail |
| token-in-body | pass | pass | 0 → pass |
| crlf | fail | fail | 1 → fail |
| empty-200 | fail | fail | 1 → fail |

5/5 agree; pytest's own failure text independently corroborates the probe's mechanism claims
(e.g. it shows verify.sh's `apt-get`/`expect` failures with their statuses unread).

**D2 (defect, latent wrong-verdict).** The harness never registers the imported module in
`sys.modules`: `module_from_spec` + `exec_module` (probe:172-174) with no
`sys.modules["tb2_cgw_grader"] = mod`. On CPython 3.14, a module whose top level uses
`@dataclasses.dataclass` raises `AttributeError: 'NoneType' object has no attribute '__dict__'`
inside `exec_module` (dataclasses `_is_type` looks up `sys.modules[cls.__module__]`). Reproduced
twice while importing this very probe file with importlib in my drivers. If a future capture used
a dataclass, the probe would print `VERDICT fail error=AttributeError` where real pytest would
**pass** — a wrong verdict, not a fail-fast. Unreachable at the frozen capture digests
(`PINS` probe:44-48; counter V1/V5 pin the bytes), so it is a limit of this freeze, not a threat
to the round-37 predicate.

**D1 (defect, operability).** `run_case` returns only `(returncode, stdout)` — `r.stderr` is
captured and dropped (probe:237-239), and main's fail-fast path prints stdout only (probe:289-291).
Demonstrated: my first pytest-driver run failed *inside* the sandbox and the cause
(`FileNotFoundError … '/work/venv/bin/python'`) was invisible until I re-implemented `run_case`
with stderr. On a host where bwrap or the setup fails, the operator sees only
`SETUP case … did not yield one verdict (rc=N)`. The frozen run is unaffected (both full runs had
0 bytes of stderr).

## 3. Receipt determinism — verified by construction and by execution

Executed: two fresh full runs, then diffs —
`python3 plans/git_webserver_probe.py --lane <lane> --work $S` (×2, exits 0, 0-byte stderr,
105 s total) → `RUN1-RUN2 byte-equal`, `RUN1-FROZEN byte-equal` (against
`corpus/evidence/round37/git-webserver-probe.txt`); `--dry` output byte-equal to
`corpus/evidence/round37/git-webserver-dry-cases-freeze.txt` (counter V5 replicates this).
Scratch fully removed afterwards (0 `cgw-*` work dirs, no `k37-cgw-*` root).

By construction: the header prints only pinned digests (probe:282-284); per-case lines print
static fields plus the case's own requirement string (probe:298-300); `grader-stdout` is
verify.sh's echo order joined with ` | ` (probe:302); the footer is counts (probe:303). No
timestamp, no mkdtemp path, and no host python/curl/bwrap version is printed anywhere. The child
env pins `LANG`/`LC_ALL=C.UTF-8` and `PYTHONUTF8=1` (probe:236).

BOM/CRLF repr lines: the harness prints `repr()` of each `splitlines()` line (probe:182-183).
BOM: `\ufeff` is escaped by repr → receipt shows `Content: \ufeffhello world`, deterministic; and
the parent-side decode is UTF-8 even under `LC_ALL=C` on CPython 3.14 (locale coercion — measured:
`LC_ALL=C python3` reports `pref=utf-8 utf8mode=1` and still decodes `\ufeff`). CRLF:
`str.splitlines()` treats the CR as a line boundary *before* repr, so the receipt shows
`"Got: 'hello world"` and a dangling `'` on the next STDOUT line — the CR itself never appears
(R6). Deterministic (byte-equal across runs), but the printed evidence for the CR is indirect.

This determinism is load-bearing: the gate's P10 re-runs the probe fresh and requires
byte-equality with the receipt (`pkg_gate.py:271-285`).

## 4. Server/grader race — none

`SERVER_PY`: `srv = S(("127.0.0.1", cfg["port"]), H)` (probe:158) — `TCPServer.__init__` binds
*and listens*; `/work/ready` is written after that (probe:159); `serve_forever()` is last
(probe:160). `RUN_SH` starts the grader only after `/work/ready` exists (40 × 0.1 s budget,
probe:188-194), so the grader can never run before the socket is listening. The only window
(listen → serve_forever) is covered by the accept backlog (`request_queue_size` 5 ≥ the 2
sequential curls): a request arriving there is answered, in order, once `serve_forever` starts
(single-threaded `TCPServer`). Empirically, `status-then-content-split` (two in-order requests)
and `slow-server-3s` (first request holds the server 3 s, second queues) match their predictions
in both fresh runs and the frozen receipt; 22/22 cases yielded exactly one `VERDICT`. Failure is
fail-fast, not silent: no ready file → run.sh exits 3 (probe:193) → main returns 2 with no receipt
(probe:289-292) → P10 sees a nonzero exit.

## 5. Defects (frozen file — reported as limits of this freeze, nothing edited)

- **D1** — `run_case` discards `r.stderr` (probe:237-239); fail-fast diagnostics print stdout
  only (probe:289-291). Low severity; demonstrated above.
- **D2** — harness imports the capture without `sys.modules` registration (probe:172-174); on
  CPython 3.14 a dataclass-using capture would yield a wrong `fail` verdict instead of pytest's
  `pass`. Latent; unreachable at the frozen digests. Low severity.

## 6. Risks

- **R1** — residual sandbox boundary: `/usr` and `/etc` readable (ro) by third-party grader code;
  `/work` (scratch), sandbox `/tmp` and `/dev` writable. No host-write or host-net path exists
  (verified §1).
- **R2** — `timeout=180` (probe:238) raises `TimeoutExpired` uncaught → traceback, exit ≠ 0, no
  receipt. Fail-fast; frozen cases bound the server at 3 s.
- **R3** — 4 s ready budget (probe:189-193) is a hard fail-fast ceiling under pathological load
  (observed startup ≪ 1 s; 22/22 ready in both runs).
- **R4** — the gate re-runs the probe via `probe_cmd` without `--work`
  (`plans/pkg-spec-r37.json`: `["plans/git_webserver_probe.py", "--lane", "."]`;
  `pkg_gate.py:274-278`), so gate-time scratch goes to `$TMPDIR`/`/tmp`, not the operator scratch;
  the probe self-cleans (probe:305-306). Hygiene note, not a seat-rule violation (the rule binds
  seats).
- **R5** — `--work` pointing at a nonexistent directory raises `FileNotFoundError` at probe:271
  (`mkdtemp(dir=…)`); no friendly error.
- **R6** — the CRLF case's CR is invisible in the receipt (`splitlines()` before repr,
  probe:182-183); the dangling quote is the only trace. Verdict unaffected; pytest cross-check
  confirms it.
- **R7** — the `/bin`,`/sbin`,`/lib`,`/lib64` symlink loop (probe:206-208) is merged-usr-shaped:
  on a host where `/bin` is a real directory nothing is bound there and dynamic execs fail
  ENOENT. I hit exactly this in bare bwrap bisects (`bwrap --ro-bind /usr /usr -- /usr/bin/ls /`
  → `execvp /usr/bin/ls: No such file or directory`) — the loop is load-bearing on Arch, absent
  elsewhere. Fine on this host.
- **R8** — receipt reproducibility is proven on *this* host (byte-equal ×2 + frozen); cross-host
  byte-equality is not claimed and would depend on the host's curl/wget behavior. Consistent with
  the docstring's claim (about printing, not portability).

## 7. Verified non-issues (observations I had to resolve)

- **"Two leftover servers"** — bg-run `pgrep -af server.py` after both full runs showed two
  `/usr/bin/python3 /work/server.py` processes. Root-caused to *sibling seats running the same
  probe concurrently*: the live example's bwrap argv carries
  `--bind /fast/scratch/hyaku/kengaku-r37/R37MutC2Counter/work/… /work`, its harness (PPid) still
  alive, `NSpid: 2755769 3` (PID 3 of its private ns). My own cases' servers provably close their
  stdio before `run_case` returns (`subprocess.run` returns only at pipe EOF, so every writer —
  including the server — has exited), and idle-host pgrep is clean. **No leak; teardown at case
  end.** (`driver_leak.py` kept for reproduction.)
- **expect masking branch** (probe:214-215) is inert on this host (no `expect` installed); the
  downstream failure is deterministic either way — pytest's captured verify.sh output shows
  `./git_test.exp: /usr/bin/expect: bad interpreter`, and verify.sh never reads that status.
- **`--die-with-parent` + SIGKILL of the probe** would skip the `finally` cleanup (probe:305-306)
  and leave scratch; not observed, low impact.

## 8. Verification gaps

- The oracle `solve.sh` is not executed and no real git push is exercised — the probe's own stated
  limit (docstring; claims file); out of scope for a review to change.
- The pytest cross-check covered 5 of 22 cases — the verdict-relevant contrast classes (exact
  match, case sensitivity, substring token, CR, empty body); the remaining cases differ only in
  status codes the harness maps identically.
- The transient sibling-seat servers were inspected live once; they were gone before deeper
  inspection, so their full lifecycle is inferred from the live sample plus EOF semantics.

## Tooling record (operator rule 2026-10-19)

- `uv 0.13.0` (already installed at `~/.local/bin/uv`) — used to create a CPython 3.13.16 venv and
  install `pytest==8.4.1` (uv pip, official PyPI) *inside scratch*, reason: empirical
  pytest-equivalence check matching `test.sh:15-16`. No pacman; nothing installed host-wide; the
  venv was deleted with the scratch.

## Artifacts kept

`.ufo/waves/round-37/build/R37RevProbeCode/`: `receipt-run1.txt` (byte-equal reproduction of the
frozen receipt), `introspect-output.txt` (isolation evidence), `pytest-equivalence.txt`
(5-case pytest agreement), `driver_introspect.py`, `driver_pytest2.py`, `driver_leak.py`
(reproduction scripts; they import the frozen probe and call its own functions unmodified).

VERDICT: probe-review-2-defects-8-risks
