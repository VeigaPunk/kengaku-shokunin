# R44SentinelSandbox — sandbox review of the round-44 C2 instruments

Seat: `R44SentinelSandbox` (sentinel, leaf, no subagents). Round 44 wave (build + attack, v2), 2026-10-26.
Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` read-only for me; all work in `S=/fast/scratch/hyaku/kengaku-r44/R44SentinelSandbox`
(clone at `$S/lane`, `git rev-parse --show-toplevel` = `$S/lane`, tip `5e3d3aa06c6b7000929ac3e62563a39159c4501f`).
No frozen byte was edited, copied into the wave dir, or re-spelled; drivers import the frozen modules read-only.

## Surface (this seat only)

- `plans/feal_linear_probe.py:196-213` `sandbox_argv()` — the per-case bwrap argv (recipe exec + grader exec).
- `plans/feal_linear_probe.py:215-218` `harness()`; `:241` cleanup; `:244-256` `letter()` (verdict from rc).
- `plans/round44_c2_verify.py:476-488` `sandboxed()` — the executor for **entry-supplied code** (V11); `:491-540` `v11`;
  `:395-397` `states()` (fixed seed); `:472` `PREDICT_PY` (one `predict(t)` call per state, in order).

Not in scope (other seats): the counter's V1–V10 content checks, C1's five mutants/fences F1–F6, the entry's prose,
the probe's case semantics. I did not judge, integrate or ship anything; I invoked no other runtime.

## Axes

1. **Boundary** — can code inside either argv write/read outside the dirs it was given (host fs, `~/.local/bin`, `$HOME`, lane)?
2. **Channel** — can it reach the network, the PID of the counter, or the counter's stdout unfiltered?
3. **Cleanup** — can it outlive the run (process, scratch residue) or defeat `--die-with-parent`'s contract?
4. **Verdict integrity** — can it make the instrument print a pass it did not earn?
5. **Operability** — does the frozen probe still work *inside* the mandatory envelope (nested bwrap), and can a genuine entry pass?

## Envelope (QUALITY Q32) — every measurement below

`envelope.sh` at `claims/envelope.sh`; **all twelve runs ended `local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged`** (no run exits 4; no measurement invalidated, none re-run):

| # | env dir | command (abbreviated) | start→end | exit |
|---|---|---|---|---|
| 1 | `$S/env` | `python3 $S/probe_attack.py $S/w/probe` (driver bug: probe module not in `sys.modules`; discarded) | 20:35:35→20:35:36 | 1 |
| 2 | `$S/env` | same, after the one-line driver fix — hostile recipe through `sandbox_argv` | 20:35:42→20:35:44 | 0 |
| 3 | `$S/env2` | `predict_probe.py` — predict-shape containment matrix | 20:36:22→20:36:24 | 0 |
| 4 | `$S/env3` | `v11_attack.py $S/lane $S/w/v11` — variants A/B/C | 20:36:44→20:36:46 | 0 |
| 5 | `$S/env4` | `fifo_hang.py` — FIFO graded artefact | 20:37:17→20:37:26 | 0 |
| 6 | `$S/env5` | `errno_probe.py` — exact errnos | 20:37:51→20:37:53 | 0 |
| 7 | `$S/env6` | gate's uv path: `uv run --no-project --with biopython==1.85 python3 plans/feal_linear_probe.py --lane . --dry` (cwd clone) | start line trimmed by `tail`; end 20:37:57 | 0 |
| 8 | `$S/env7` | **full probe under the envelope**: `sh -c TMPDIR=$S/tmp7 python3 plans/feal_linear_probe.py --lane .` | 20:38:04→20:38:09 | 0 |
| 9 | `$S/env8` | `leak_probe.py` (with `chmod 000 /app`) | 20:38:30→20:38:32 | 0 |
| 10 | `$S/env9` | `leak_probe.py` (chmod removed) | 20:38:40→20:38:42 | 0 |
| 11 | `$S/env10` | `v11_bypass.py $S/lane $S/w/bypass` — answer-key predictor | 20:39:09→20:39:11 | 0 |
| 12 | `$S/env11` | `kill_probe.py` — verdict-flip attempt | 20:39:37→20:39:39 | 0 |

Run 8's three envelope lines verbatim (`$S/out/probe-envelope.txt:1,2,27`):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind …/R44SentinelSandbox/env7 …/env7 --bind …/env7/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- sh -c TMPDIR=…/tmp7 python3 plans/feal_linear_probe.py --lane .
ENVELOPE start 20:38:04 cwd=/fast/scratch/hyaku/kengaku-r44/R44SentinelSandbox/lane
ENVELOPE end 20:38:09 exit=0 local_bin_content_before=328be01808ba022f after=328be01808ba022f unchanged
```

Every driver ran under this wrapper; none of them wrote outside `$S` (verified after each run: `~/.local/bin` digest
identical, and the lane clone's `git status --porcelain` shows only my own untracked fixture entry).

## Findings

### F1 — MEDIUM (content, not boundary): V11 prints `ok` for a `predict` that ignores its argument

*Exploit path.* V11 never checks that the verdict is a **function of `text`**. `PREDICT_PY` (`round44_c2_verify.py:472`)
calls `ns["predict"](t)` once per state, in the order of `states()` (`:395-397`, `random.Random(44)`, fixed). The author
of the entry has the lane, so it can compute the 48 verdicts once (running the captured grader through the counter's own
`GRADE_PY`) and hardcode them. A 48-element list then agrees with every state.

*Evidence* (run 11, verbatim):

```
answer_key_len= 48 pass= 24 fail= 24
V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
```

The predictor used was the whole of the block: `_KEY = [<48 bools>]`, `_i = iter(_KEY)`, `def predict(text): return next(_i)`.
Contrast: a forged stdout (`os.write(1, json.dumps([True]*48)); os._exit(0)`, run 4 variant B) is correctly rejected —
`V11 DEFECT states=48 grader_pass=24 grader_fail=24 disagree=24 at=drop-one#2,…` — so the hole is *order*, not the pipe.

*Impact.* The claim `plans/round-44-claims.md` §C2 calls V11 "the key is not in this file" and the counter docstring
(`round44_c2_verify.py:35-40`) says "The verdicts are never stored here: they exist only by executing the grader, so a
filler cannot copy them from the counter". True for the counter, false for the *state list*: the generator is public and
deterministic, so the answer key is derivable in one in-lane grader run, and the resulting entry contains no reading at
all. V11 is C2's only anti-copycat lever (closure R5); as frozen it verifies *agreement with a sequence*, not that
`predict(text)` reads the grader's substring rule. The claims' §C2 Limits half-names this ("a predictor could be tuned to
them — but only by running the grader, which is the reading V11 asks for"); the realised form is stronger than that
sentence: after tuning, nothing in the entry reads the grader or the text.

*Smallest remediation* (needs a counter edit, i.e. not this round — the counter is frozen): seed the state generator per
run (`random.Random(os.urandom(8))`) and keep the ≥8/≥8 non-vacuity guard; a hardcoded list then disagrees. A permuted
replay is **not** a fix (the counter source is readable, so the order is too) — only an unpredictable seed is. Until then
the honest wording is: V11 verifies agreement on 48 fixed states, and its answer key is derivable from the frozen counter.

### F2 — LOW/MEDIUM (evidence integrity): a failing predictor can write lines into the counter's own stdout

*Exploit path.* `sandboxed()` embeds the child's raw stderr tail — newlines included — in a `RuntimeError`
(`round44_c2_verify.py:487: raise RuntimeError(f"{script} exit={r.returncode}: {r.stderr.strip()[-200:]}")`), and `v11`
turns that into a note that `main()` prints (`print(f"{name} {'ok' if ok else 'DEFECT'} {note}")`). Any predictor that
fails can therefore emit arbitrary *lines* into the counter transcript.

*Evidence* (run 4, variant A; the driver printed exactly what `main` prints, verbatim):

```
V11 DEFECT predictor failed: predict.py exit=3: V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0
checks=11 defects=0
PREDICATE C2 pass
```

The predictor was: `sys.stderr.write("V11 ok …\nchecks=11 defects=0\nPREDICATE C2 pass\n")` then `raise SystemExit(3)`.

*Impact.* Bounded but real: the forged lines are bare and precede the genuine final `checks=…`/`PREDICATE C2 …` lines,
and the process exit stays 1, so a reader that takes the **last** occurrence or the exit code is safe; a reader (human or
`grep -q`) that takes the **first** match of the frozen predicate sentence is fooled. It requires the entry to fail V11,
so it cannot upgrade a defect into a real pass — it can only make the transcript claim one.

*Smallest remediation.* One line, never a sandbox change: collapse the tail to one line in the note,
e.g. `" ".join(r.stderr.split())[-200:]` (and/or sanitise `note` at the `print`).

### F3 — LOW (operability/cleanup): a recipe that `chmod 000 /app` defeats the probe's scratch cleanup

`run_case`'s `finally` is `shutil.rmtree(work, ignore_errors=True)` (`feal_linear_probe.py:241`); `ignore_errors=True`
also hides the failure. Evidence (run 9): `"cleanup": "rmtree FAILED PermissionError: Permission denied -> leftover scratch kept"`,
and the residue survives: `d--------- 2 vgpnk vgpnk 121 …20:38 /fast/scratch/…/w/leak/app` (mode 000, whole case tree kept).
Run 10, same recipe without the `chmod`, gives `"cleanup": "rmtree OK (no leftover)"` — so the trigger is exactly the mode
change. No escape: it is residue in the caller's own scratch, and the frozen recipes cannot do it. Impact is scratch
hygiene (a later `scratch_guard safe-rm` on that parent then needs a `chmod`). Remediation: `shutil.rmtree(work, onexc=…)`
that retries after `chmod -R u+rwX`, or report the failure instead of discarding it.

### F4 — LOW (operability/attribution): a blocking graded artefact is bounded only by two unrelated timeouts

*Exploit path.* The graded file is read by the captured grader (`open("/app/plaintexts.txt").read()`). If a recipe leaves
a FIFO there, the read blocks. `harness()`'s `timeout=1800` (`feal_linear_probe.py:217`) then raises
`subprocess.TimeoutExpired`, which **no frame in `run_case`/`main` catches** → traceback, exit 1, no CASE line; and the
gate's own `timeout=600` (`pkg_gate.py` `c_rerun`) fires first, reporting `probe could not be re-run: TimeoutExpired`.

*Evidence* (run 5, with an 8 s stand-in for the 1800 s bound):

```
"recipe": [0, "STAGE seed rc=0\nSTAGE recipe rc=0\n"],
"grade": "TimeoutExpired: grader blocked on the FIFO (harness() timeout=1800 is uncaught)",
"fifo_is_fifo": true
```

*Impact.* Fail-safe (never a pass) but unattributed: the failure surfaces as a traceback or as a P10 gate timeout, not as
a named case. Frozen recipes do not do this; it matters for the next round that adds a case. Remediation (future round):
catch `TimeoutExpired` in `harness()` and map it to a named SETUP/`F` outcome, and keep the probe's per-case bound below
the gate's.

### F5 — INFO/LOW: the sandbox's `/etc` is the host's `/etc` verbatim, and `/proc/1/cmdline` prints the lane's absolute paths

Run 10 proof (verbatim): `READ /etc/machine-id 33`, `READ /etc/hostname 9`, `READ /etc/passwd 1757`,
`DENY /etc/shadow`, `DENY /etc/NetworkManager/system-connections`, `DENY /etc/sudoers`, and the in-sandbox digests equal the
host's: `21f3fd92521639a754e508b327384a3c09a1f99b94e9e10c85ede67e48a3a12b /etc/machine-id`,
`694cd433b4212f7ed2f6b1bb23c8ef980056bf36de62d37e9f0a01c04f6fa194 /etc/hostname`. `/etc/ssh/ssh_host_ed25519_key` does
not exist on this host either. In the probe shape, `/proc/1/cmdline` (run 2) returns the full bwrap argv, i.e. every bind
source including `…/kengaku-shokunin/corpus/evidence/round44/tb2-feal-linear-cryptanalysis/gen.py` — the lane layout.
No secret is reachable (root-only files are denied), and with the network unshared and only 2 PIDs visible (run 6:
`"pid_max_visible": 2`, `"proc1_exe": "/usr/bin/bwrap"`), the only exfil channel is the transcript — which is F2.
Remediation if wanted later: bind a minimal `/etc/{passwd,group,ld.so.cache,ssl}` instead of all of `/etc`; low priority.

### F6 — NOTE: `/app` is a host-backed writable bind with no size cap (probe shape only)

Run 2: `app WRITABLE`, and `…/w/probe/app/PWN` exists on the host afterwards. `/tmp`, `/`, `/dev/shm` are RAM tmpfs and
their writes never reach the host (`/PWN` absent from `$S`; root listing inside shows `PWN` only in-sandbox). No quota
exists on the `/app` bind, so hostile recipe code could fill the scratch filesystem. The *predict* shape has no `/app` at
all (`app: DENIED:No such file or directory`, run 3). Nothing to fix this round; name it as a limit.

## What is contained (negative matrix — all measured, runs 2, 3, 6)

| attempt (from inside) | observed |
|---|---|
| write lane path, `~/.local/bin`, `~`, `/tests/PWN`, `/tests/test_outputs.py`, `/pub/gen.py`, `/harness.py`, `/seed.sh` | `No such file or directory` (no `/home` in the root) / `Read-only file system` |
| write `/etc`, `/usr` | `Read-only file system` |
| `mount -o remount,rw /pub`; `mount --bind / /app/m` | `mount: /pub: must be superuser to use mount.` (uid **1000**, not namespace-root) |
| `mknod c 1 3` | `Operation not permitted` |
| open `/proc/sys/kernel/{core_pattern,modprobe}` and `/proc/sysrq-trigger` for write | `EACCES:Permission denied` (open-only; no write issued) |
| TCP to `1.1.1.1:80`; `getent hosts example.com` | `OSError: [Errno 101] Network is unreachable`; no resolution |
| see the counter process | predict shape: `proc_pids [1,2]`, `ppid 1`; probe shape: `proc_pids=6`, pid 1 = bwrap |
| read the grader from the predict leg (`/tests/test_outputs.py`) | `DENIED:No such file or directory` |
| leftover process: detached `sleep 120` in the probe shape (`KFLP_LEFTOVER`), predictor-spawned `C2LEFTOVER`, and `FIFOKILL` after a forced kill | `NO-LEFTOVER`, `NO-LEFTOVER-C2`, `NO-LEFTOVER-FIFO` — `--unshare-pid` + ns-init death kills them |
| env of the predict leg | 7 vars only (`HOME LANG LC_ALL PATH PWD PYTHONDONTWRITEBYTECODE PYTHONUTF8`); no `PYTHONPATH`, no `TMPDIR` |

### Verdict integrity of the probe (runs 2, 12)

- `letter()` keys on rc, not on the text: `return ("P" if rc == 0 else "F"), note` (`feal_linear_probe.py:256`).
- The recipe *can* write into `/proc/1/fd/1` and gets its text into the harness's captured stdout — run 2 stdout was
  `"STAGE seed rc=0\nTEST test_attack P forged-note\nSTAGE recipe rc=0\n"`. It buys nothing: in grade mode the harness
  never runs the recipe (`HARNESS_PY` gates on `mode`), and `run_case` discards the recipe leg's stdout when rc is 0.
- Suppressing the failure does not help either (run 12): a recipe that writes `WRONG`, injects `TEST test_attack P` and
  runs `kill -9 1` gives `"harness_rc": 0` then grade `[1, "TEST test_attack F\n", ["F", ""]]` — `kill` to a PID-namespace
  init from inside is ignored by the kernel, and the grade leg is a fresh process. No flip exists.

## Operability results (the L1 needs these)

1. **The frozen probe runs unchanged inside the envelope** (nested bwrap, run 8): 6.4 s wall for 14 cases × 3 sandbox runs,
   and, after stripping the 3 `ENVELOPE` lines, its stdout is **byte-identical** to the frozen receipt:
   `stripped_sha256=40308211216be063084eb9a1f22faded5a8550d392a83f6e13545e2ddae205a0`, `receipt_sha256 =` the same,
   `byte_equal= True`. So P10 has ~94× headroom under its 600 s timeout.
2. **Consequence for P10 and the envelope:** `envelope.sh` writes to *stdout*, so a receipt regenerated by wrapping the
   probe command directly would gain 3 lines and fail P10's byte comparison. P10 itself is safe (it captures the probe's
   stdout internally); only a manual re-capture must keep the envelope lines out of the receipt stream.
3. **The gate's `uv` path works under the envelope** (run 7; `import Bio` fails on this host, so `c_rerun` takes
   `uv run --no-project --with biopython==1.85 python3 …`): it printed the frozen dry table and `cases=14 predicted_pass=8
   predicted_fail=6`, exit 0, home read-only + `~/.cache` overlay.
4. **A genuine entry can pass V11 in this environment** (run 4 variant C: the 100 constants embedded + `all(c in text …)`,
   plus a spawned process): `V11 ok states=48 grader_pass=24 grader_fail=24 disagree=0`. The sandbox does not obstruct the
   intended reading; the predict leg simply cannot read the grader it must emulate.
5. Neither instrument writes into the lane: after all twelve runs the clone's only change is my own fixture entry
   (`?? corpus/knowledge/tb2-feal-linear-cryptanalysis-grader.md`), and both write scratch only under `--work`/`$TMPDIR`
   (`round44_c2_verify.py:534` `TemporaryDirectory(prefix="k44-c2-", dir=a.work)`; `feal_linear_probe.py:330`
   `mkdtemp(prefix="k44-flp-", dir=a.work)`).

## Limits of this review

- Recipes are frozen, so for the probe shape the *attacker* is hypothetical: I substituted my own recipe through the
  instrument's own `sandbox_argv`/`harness` (no copy of the module, no edit) to test the boundary a future case would get.
- bwrap 0.13.1, host kernel 7.2.11-arch1-1, unprivileged userns enabled; a different kernel/bwrap could behave differently
  (e.g. `--ro-bind` semantics for namespace-root — here uid inside is 1000 with caps dropped, so mount/mknod/sysctl are
  denied by capability, not only by the readonly flag).
- F4's 1800 s bound was demonstrated with an 8 s stand-in; the uncaught-`TimeoutExpired` claim is from the code path
  (`harness()` has no `except`), not from a 30-minute wait.
- I did not evaluate V11's statistical strength (a 48-state, 16-kind generator) or the probe's case semantics; other seats own those.
- No tool was installed or upgraded (nothing was needed); no pacman transaction was run.

VERDICT: sandbox-escapes-0 (no write, read, network or process escape from either bwrap argv; 1 predictor-side bypass, F1, makes V11 print ok without a function of text)
