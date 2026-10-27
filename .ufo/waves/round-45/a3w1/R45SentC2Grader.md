# R45SentC2Grader — sentinel: host-execution audit of the round-45 C2 package path

Seat: wave `a3w1` of round 45, item R45SentC2Grader (leaf; no subagents, no background jobs).
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, measured at `master` = **fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc**.
Working tree at measurement time: `git status --porcelain` shows `M SCORECARD.md`, `M corpus/QUALITY.md`
(live sibling edits, 00:23–00:24) plus the untracked wave-evidence tree under `.ufo/` — see F3.
Tooling: nothing installed, nothing upgraded. Every run went through
`.ufo/waves/round-45/claims/envelope.sh`; the `~/.local/bin` content digest was `ff187bb5c98aa6b5` before
**and** after each of the five runs (`unchanged`), so no measurement was invalidated.
Scratch: `/fast/scratch/hyaku/kengaku-r45/R45SentC2Grader` (deleted before yield). Receipts in
`.ufo/waves/round-45/a3w1/R45SentC2Grader/`.

Question asked: does anything in the probe, the gate or the C2 counter execute upstream code on the
**host, outside bwrap** (`setup.sh`, `solve.sh`, the grader module), and does `setup.sh` carry a payload the
sandbox does not contain?

Short answer: **no upstream task code runs outside bwrap** (0 of 1 102 executions). One non-sandboxed
execution site does exist in the C2 path: the gate's Biopython fallback, which makes the C2 PASS depend on a
live PyPI fetch executed on the host (F1).

## 1. Execution map (static)

| site | what it runs | sandbox |
|---|---|---|
| `plans/password_recovery_probe.py:234` | `bwrap <sandbox_argv> /usr/bin/python3 /harness.py <mode>` | **the launcher**; host process, execs only `/usr/bin/bwrap` |
| `plans/password_recovery_probe.py:180` (inside `HARNESS_PY`) | `bash -euo pipefail /seed.sh`, `/recipe.sh`; then `importlib` loads `/tests/test_outputs.py` | **inside bwrap** (`--unshare-net --unshare-pid --unshare-ipc`) |
| `plans/round45_c2_verify.py:157` | `pkg_gate.py package --rerun --require-clean-tree` | host (parser only; its execs are P9 `git` and P10 probe) |
| `plans/round45_c2_verify.py:229` | `password_recovery_probe.py --dry` | host, stdout only — the dry branch returns before any `subprocess` |
| `plans/round45_c2_verify.py:236` | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate` | host; bash+gawk registry parser, no network, read-only |
| `plans/round45_c2_verify.py:294` | `plans/order_check.py` | host; `git cat-file`/`log`/`merge-base` read-only |
| `plans/round45_c2_verify.py:520` (`sandboxed`) | grader on 48 states; entry predictor block | **inside bwrap** (`--ro-bind /usr`, `--ro-bind /etc`, predict leg binds only `/predictor.py`) |
| `plans/pkg_gate.py:260` | `git ls-files --others --exclude-standard` | host, read-only |
| `plans/pkg_gate.py:278` | the probe re-run (P10) | host launcher → bwrap per case; **may exec `uv` first** (F1) |

The probe's own sandbox argv (`plans/password_recovery_probe.py:214-228`) binds `/usr` and `/etc`
read-only, a fresh `/proc`, a fresh `/dev`, a tmpfs `/tmp`, the scratch `app` read-write, scratch `tests`
read-only, `/pub` (three captured files), and the three generated scripts; there is **no bind of `$HOME`,
`/home`, `/fast` or the lane**, and `--chdir /app`.

## 2. Measurements

Every receipt below is in `.ufo/waves/round-45/a3w1/R45SentC2Grader/`; sha256 of each file is listed in §6.
Envelope header for all five runs (only the scratch dir differs):

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind <SCR> <SCR> --bind <SCR>/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- <command>
```

### M1 — containment of the frozen sandbox envelope (`containment.txt`)

Hostile module `.ufo/waves/round-45/a3w1/R45SentC2Grader/sandbox_containment.py` imports the **frozen**
probe read-only (`importlib` on `plans/password_recovery_probe.py`, sha256 `9363e03e…beb4ab`) and reuses its
`sandbox_argv()` verbatim, substituting only the harness payload.

```
$ TMPDIR=$S .ufo/waves/round-45/claims/envelope.sh "$S/env" /usr/bin/python3 \
    .ufo/waves/round-45/a3w1/R45SentC2Grader/sandbox_containment.py "$S/containment"
ENVELOPE start 00:23:42 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
ENVELOPE end   00:23:43 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

| payload | result |
|---|---|
| `id` | `uid=1000(vgpnk) gid=1000(vgpnk) groups=1000(vgpnk),65534(nobody)` |
| `/proc/self/status` | `CapEff: 0000000000000000`, `NoNewPrivs: 1` |
| `ls /` | `app bin dev etc harness.py lib lib64 proc pub recipe.sh sbin seed.sh tests tmp usr` |
| `ls -d /home /home/vgpnk /fast /root /sys` | all `No such file or directory` |
| `echo pwn > /etc/motd` | rc=1 `Read-only file system` |
| `echo pwn > /usr/local/bin/shim` | rc=1 `Read-only file system` (host dir is `root:root 755`, so this attempt cannot write even unsandboxed) |
| `echo HOME=$HOME; test -e /home/vgpnk/.local/bin` | `HOME=/tmp`, `NO_localbin` |
| `cp /usr/bin/true /app/x; chmod u+s /app/x` | rc=0, `-rwsr-xr-x 1 vgpnk vgpnk` — setuid bit lands only on a self-owned file under the scratch bind; no escalation |
| `curl -sS https://astral.sh/` | `curl: (6) Could not resolve host: astral.sh` |
| `getent hosts example.com` | rc=2 |
| `bash -c 'exec 3<>/dev/tcp/1.1.1.1/53'` | `Network is unreachable` |
| python `socket.create_connection(("1.1.1.1",53),3)` | exception |
| `echo pwn > /app/z.bin`, `> /tmp/t` | rc=0 (the only writable trees) |

bwrap 0.13.1, `/usr/bin/bwrap` is **not** setuid, `kernel.unprivileged_userns_clone=1` → user namespace +
`NoNewPrivs`, `CapEff=0`.

### M2 — every `execve` in the whole C2 counter, classified (`exec-classification.txt`, `argv-receipt.txt`)

```
$ TMPDIR=$S/c2-work .ufo/waves/round-45/claims/envelope.sh "$S/env3" /usr/bin/strace -f -qq -tt \
    -e trace=execve,clone,clone3,fork,vfork -o "$S/c2.trace" /usr/bin/python3 \
    plans/round45_c2_verify.py --lane . --work "$S/c2-work"
ENVELOPE start 00:25:04 cwd=/home/vgpnk/Projects/shokunin/kengaku-shokunin
ENVELOPE end   00:25:12 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
$ /usr/bin/python3 .ufo/waves/round-45/a3w1/R45SentC2Grader/classify_execs.py "$S/c2.trace"
INSIDE bwrap (probe ENV, <=10 vars): 1054 execve
OUTSIDE bwrap (host env, >10 vars): 48 execve
# 397 failed execvp candidates (ENOENT/EACCES) excluded in total
```

Classification rule: the probe passes `env=ENV` (6 vars) to every bwrap launch
(`plans/password_recovery_probe.py:229-230`), every sandboxed process inherits it, host-side processes carry the
caller's ~268-var environment; and a process tree cannot be used here because bwrap's children straddle a new
PID namespace.

Host-side 48, in full: `git` ×29, `/usr/bin/python3` ×4, `realpath` ×3, `ld-linux` ×2, `dirname` ×2,
`gawk` ×2, `/usr/bin/bash` ×1, `date` ×1, `cat` ×1 (all of the preceding are the census/order/P9 readers),
plus **`uv` ×1 and `/home/vgpnk/.cache/uv/builds-v0/.tmp95KukI/bin/python3` ×1** (F1).

Sandbox-side, by argv (`argv-receipt.txt`), i.e. the upstream code the question names:

```
  48  execve argv/path mentioning /harness.py            env_vars=[7]  [harness (grader loader)]
  16  execve argv/path mentioning /seed.sh               env_vars=[7]  [seed (upstream setup.sh)]
  16  execve argv/path mentioning /recipe.sh             env_vars=[7]  [recipe (case payload)]
   2  execve argv/path mentioning /pub/solve.sh          env_vars=[9, 10]  [oracle solve.sh]
   0  execve mention of test.sh
   0  execve mention of test_outputs.py
```

48 = 16 cases ×(1 recipe-mode sandbox + 2 grade-mode sandboxes), all under `--unshare-net`. `solve.sh` runs
twice (the `oracle-solve-sh` and `under-varsea` recipes) with 9/10 env vars, i.e. inside the sandbox.
`test_outputs.py` is never an exec target: the harness `importlib`s it inside the sandbox.

### M3 — the C2 claim, at the tip and in a clean clone (`c2-verify.txt`, `c2-verify-clone.txt`)

```
$ git clone -q --shared …/kengaku-shokunin "$S/lane"; git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r45/R45SentC2Grader/lane        # HEAD fbad1c5…, untracked=0
$ cd "$S/lane"; TMPDIR=$S/c2-clone-work .ufo/…/envelope.sh "$S/env4" /usr/bin/python3 \
    plans/round45_c2_verify.py --lane . --work "$S/c2-clone-work"
ENVELOPE start 00:25:56 cwd=…/lane
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=4659
V1 … V11 all ok
checks=11 defects=0
PREDICATE C2 pass
ENVELOPE end   00:26:01 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

At the **lane tip** the same frozen counter, same envelope (`c2-verify.txt`, `$S/env3`, 00:25:04–00:25:12):

```
    gate: P9 DEFECT untracked=30 first=.ufo/waves/round-45/a3w1-dispatch.json
    gate: defects=1
V2 DEFECT spec=frozen gate=frozen gate_exit=1
V1 V3 V4 V5 V6 V7 V8 V9 V10 V11 ok
checks=11 defects=1
PREDICATE C2 fail
```

So the wave-1 claim (`checks=11 defects=0`) reproduces — but only from a clean clone (F2).

### M4 — the gate's Biopython fallback (`gate-rerun.txt`, `gate-no-uv.txt`, `gate-rerun.trace.gz`)

```
$ /usr/bin/python3 -c "import Bio"
ModuleNotFoundError: No module named 'Bio'          # host /usr/bin/python3 is 3.14
$ grep -n "^import\|^from" corpus/evidence/round45/tb2-password-recovery/test_outputs.py
5:from pathlib import Path                            # the grader needs no Biopython at all

$ TMPDIR=$S/gate-work .ufo/…/envelope.sh "$S/env2" /usr/bin/strace -f -qq -e trace=execve \
    -o "$S/gate-rerun.trace" /usr/bin/python3 plans/pkg_gate.py package --root . \
    --spec "$S/eff-spec.json" --rerun --require-clean-tree
P10 ok probe_rerun=byte-equal bytes=4659
ENVELOPE end 00:24:18 exit=1 … unchanged                      # exit 1 is P9 only
$ grep 'execve(".*uv"' "$S/gate-rerun.trace"
execve("/home/vgpnk/.local/bin/uv", ["uv", "run", "--no-project", "--with", "biopython==1.85",
        "python3", "plans/password_recovery_probe.py", "--lane", "."], …) = 0

$ TMPDIR=$S/nouv-work PATH=/usr/bin:/bin .ufo/…/envelope.sh "$S/env5" /usr/bin/python3 \
    plans/pkg_gate.py package --root . --spec "$S/eff-spec.json" --rerun --require-clean-tree
P10 DEFECT probe could not be re-run: FileNotFoundError
defects=1
ENVELOPE end 00:26:14 exit=1 … unchanged
```

## 3. Findings

**F1 — MEDIUM (safety + reproducibility): the C2 PASS depends on unpinned remote code executed on the host.**
Trigger: run the frozen `round45_c2_verify.py` (V2) on any host whose `/usr/bin/python3` cannot
`import Bio`. `plans/pkg_gate.py:273-276`:

> `import Bio  # noqa: F401  (the pinned grader's dependency; host python when available)`
> `cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe`

Exploit path: the fallback resolves `uv` through the caller's `PATH` (measured: `/home/vgpnk/.local/bin/uv`),
then fetches `biopython==1.85` **plus a transitive `numpy`** and a **managed CPython 3.13** from PyPI and runs
them as `vgpnk`, outside bwrap, with no artifact digest (`wheels-v7/pypi/biopython/1.85-cp313-…`); the probe
is then run by that interpreter (`execve("/home/vgpnk/.cache/uv/builds-v0/.tmp95KukI/bin/python3",
["python3","plans/password_recovery_probe.py","--lane","."])`), not by `sys.executable`. Cache growth measured
in the overlaid `~/.cache`: **143 MB** per run (`du -sh $S/env{2,3,4}/home-cache` → all `143M`). A compromised
or replaced PyPI artifact therefore executes arbitrary code on the verification host and can rewrite the
receipt the gate then compares byte-for-byte. The dependency is phantom: the grader imports only `pathlib`
(`test_outputs.py:5`), and the sandboxed grading leg always uses `/usr/bin/python3` anyway, so the fallback
buys nothing. With `uv` off `PATH` the clause fails closed (`P10 DEFECT … FileNotFoundError`) — so the C2 PASS
is *host-dependent and network-dependent*, silently.
Impact: (a) supply-chain execution outside the sandbox on the very path that certifies the package;
(b) `checks=11 defects=0` is not reproducible on an offline or fresh host.
Smallest remediation (round 46; `plans/` is frozen now): drop the `import Bio` heuristic and always run
`[sys.executable] + probe` — the probe sandboxes every case itself; if a dependency probe is wanted, check the
*sandbox's* interpreter, not the host's.

**F2 — LOW (reproducibility): the C2 PASS cannot be measured at the lane tip.**
`round45_c2_verify.py` V2 passes `--require-clean-tree` to the gate, and `c_clean_tree` counts every untracked
file, so the harness's own wave evidence (`.ufo/waves/…`) turns the counter into `PREDICATE C2 fail` at the
tip (`P9 DEFECT untracked=30`, measured 00:25:12) while the identical tree cloned clean gives
`checks=11 defects=0` (M3). The claim is therefore true of a clean clone and false of the tree the L1 works in.
Smallest remediation: run the counter against `git clone --shared` (or drop `--require-clean-tree` and state
that P9's contract excludes `.ufo/`); whichever is chosen, the claim text should say which.

**F3 — LOW (integrity blind spot): "clean tree" does not see modified tracked files.**
`plans/pkg_gate.py:260` runs `git ls-files --others --exclude-standard`, which lists **untracked files only**.
Measured at 00:27 on the same tree: `git diff --stat` → `SCORECARD.md | 4 +++-`, `corpus/QUALITY.md | 30
++++++++` — modifications invisible to P9, whose name promises a clean tree. The package's own files happen to
be digest-pinned (P2/P4/P5/P6), so a modified *entry* is caught; anything else in the tree is not.
Smallest remediation: `git status --porcelain` (or `git diff --quiet && git diff --cached --quiet`).

**F4 — INFO (positive): containment holds.**
See M1: no `/home`, `/fast` or `/sys` inside; `/etc` and `/usr` read-only (`Read-only file system`); no
network (`Could not resolve host`, `Network is unreachable`); `NoNewPrivs=1`, `CapEff=0`, uid 1000; write
surface limited to the `app` scratch bind and a tmpfs `/tmp`. bwrap is not setuid.

**F5 — INFO (control): the captured `tests/test.sh` payload is never executed, and never enters a sandbox.**
`test.sh:8` carries `curl -LsSf https://astral.sh/uv/0.9.5/install.sh | sh` — exactly the round-40 shim hazard
(a `$HOME/.local/bin` install). Measured: **0** `execve` mentions of `test.sh` in the full counter trace, and
the probe binds only `instruction.md`, `test_outputs.py`, `solve.sh` from the capture
(`PUBLIC` at `plans/password_recovery_probe.py:75-76`); `tests/` receives only `test_outputs.py`. Anyone who
"just runs" the capture's `test.sh` outside bwrap would install into `$HOME/.local/bin` — do not.

**F6 — INFO (harness): every external tool is `PATH`-resolved, `~/.local/bin` included.**
The host-side execs were resolved through the caller's `PATH`; `git` had 12 candidate paths tried
(`/home/vgpnk/.local/bin/git` among them) before `/usr/bin/git` won, and `uv`/`bash` the same way. The round-40
class of accident is therefore still live for P9/order_check/census/P10; the only guard is the envelope's
content digest — which reported `unchanged` in all five runs here. Fails closed where it matters: a missing
tool becomes a DEFECT (`P10 … FileNotFoundError`), never a pass.

## 4. `setup.sh` payload audit (the capture the sandbox runs as `/seed.sh`)

`corpus/evidence/round45/tb2-password-recovery/setup.sh` (sha256 `9fdde5d9…6f2af8`, the probe's pin), every
write and every command:

- writes only under `/app`: `$BASE_DIR=/app/varsea` (`:2-12`), `$IMG_PATH=/app/varsea/disks/.../ae3f4c.dat`
  (`:16-22`), `/app/launchcode.txt` (`:25`), `/app/secret.zip` (`:26`), `/app/secret.part.aa|ab` (`:32-33`),
  `/app/logs.txt` (`:40`).
- the only `rm`: `:43` `rm /app/launchcode.txt /app/secret.zip /app/secret.part.* /app/logs.txt`.
- **no** `curl`/`wget`/`nc`/`ssh`/`apt`/`pip`/`python`, **no** `chmod`/`chmod u+s`/`chown`/`sudo`/`mknod`,
  **no** path outside `/app` (`grep -nE 'curl|wget|nc |ssh|apt|chown|chmod|sudo|mknod|pip |python|/etc|/usr|/home'
  setup.sh` → only three `dd … /app` lines, exit 0).
- tools it needs are all inside the sandbox via the read-only `/usr` bind: `mkdir dd head od tr echo date zip
  strings awk grep rm` (probe `TOOLS` also requires `python3 bash zip dd strings`, all present).
- `solve.sh` likewise writes only `window.txt`, `possible_sequences*.txt` in its cwd and appends to
  `recovered_passwords.txt` (`:22-63`); it needs no network.
- Payload the sandbox does *not* contain: none found. (The image's forensic toolchain — `extundelete`,
  `foremost`, `sleuthkit` from `Dockerfile:5-13` — is absent from the sandbox and is not referenced by
  `setup.sh` or by the grading path. `/dev/urandom` is replaced by a 64 KB zeros file, a *fidelity* limit the
  entry states at `corpus/knowledge/tb2-password-recovery-grader.md:205`, not a safety one.)

## 5. Receipts (in `.ufo/waves/round-45/a3w1/R45SentC2Grader/`)

| file | sha256 |
|---|---|
| `containment.txt` | `56ae24a59de92ff9281a401cadce4e7f8c73b357f386dd0672d5822c4b867346` |
| `c2-verify.txt` (lane tip) | `44f00670d7a99ba82c3193b9d3d19fe4b15443ddafc27efd1867e09ae3d2a460` |
| `c2-verify-clone.txt` (clean clone) | `2c875f4d130f3fb3446695f2ca234b2f03190893074a0bd8614831717f1204b3` |
| `gate-rerun.txt` | `df47e4bc8058e32bea5b75ea11d1b8c491d87696f7e910b454fd79fe8fda5339` |
| `gate-no-uv.txt` | `015eda5b625a5030e38e6c6ee542d444a728ae75c5c58b41ad07faa9a99d512a` |
| `c2.trace.gz` (754 432 B raw) | `60cda22ac5e3c0942164b468d11361b7870057e3da9a170018dc692d7faa74b9` |
| `gate-rerun.trace.gz` (460 591 B raw) | `737eb1f7f1b49f18cadbed0244c5053de9f2d7c6fbd2cb2a4477aff22eba1d13` |
| `classify_execs.py` | `294229de9d2dce77ff9b4faa62f8c24cf2ef6b08c5ef1a8f8726d499f0b7515c` |
| `sandbox_containment.py` | `(module, 3 747 B)` |
| `exec-classification.txt` | `cae9e70776c86c34bf363c3ce43c874aeb8a16bd6e325127d4fdf559ab8f8fac` |
| `argv-receipt.txt` | `0189a1be9f6d46b3584491727dea23456f75449f168da98ea9fa007b857d5d45` |

No lane file was written: `git -C "$S/lane" status --porcelain` stayed empty after the counter run, and the
lane's own `M SCORECARD.md` / `M corpus/QUALITY.md` were already modified by live siblings at 00:23–00:24
(untouched by this seat). Scratch `/fast/scratch/hyaku/kengaku-r45/R45SentC2Grader` removed before yield.

## 6. Verdict

Upstream task code outside bwrap: **0** (`setup.sh` ×16, `solve.sh` ×2, `test_outputs.py` ×48 loads — all at
env width ≤10, i.e. inside `--unshare-net`). Non-sandboxed execution sites in the C2 path that run code the
repository does not pin: **1** — the gate's `uv`/PyPI fallback (F1), which the C2 PASS silently requires.

VERDICT: c2-unsafe-execs-1
