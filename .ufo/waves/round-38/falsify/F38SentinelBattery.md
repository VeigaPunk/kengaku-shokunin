# F38SentinelBattery — security review of what the C1/C2 counters execute

Seat: sentinel (round 38 wave 2, FALSIFY). Attacked surface: `plans/battery38/*.py` fixtures own specs whose
`probe_cmd` the gate executes; the gate and the C2 probe compile and run host-built binaries. Question asked:
host writes outside scratch, network use, leftover processes after a full C1 + C2 run in a clone.

Clone: `/fast/scratch/hyaku/kengaku-r38/F38SentinelBattery/lane` @ `8c7422d7a646515d80af44844e8ecc8a1fc1d30a`
(`git -C "$S/lane" rev-parse --show-toplevel` → `$S/lane`). `TMPDIR`/`UV_CACHE_DIR` passed explicitly; scratch
deleted at the end. No lane file, fleet-root file, jj state or Git index touched; no pacman transaction.

Baselines I reproduced before attacking (so my findings are against the same tip):

```
$ python3 plans/round38_c1_verify.py --lane . --work $S/work1        # exit=1, 66s
PINS total=14 mismatched=0
BATTERY fixtures=86 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=22 killed=21 survived=1 invalid=0 null_detected=0
PREDICATE C1 fail          (N21 D5 silence SURVIVED)
$ python3 plans/round38_c2_verify.py --lane . --work $S/w2          # exit=0, 4s
checks=7 defects=0 ; PREDICATE C2 pass
```

## F1 — HIGH — both frozen predicates need network or a warm `~/.cache/uv`; undeclared host dependency

**Exploit/failure path.** `plans/pkg_gate.py:271-278`:

```
271:    probe = list(p.spec["probe_cmd"])
273:        import Bio  # noqa: F401  (the pinned grader's dependency; host python when available)
276:        cmd = ["uv", "run", "--no-project", "--with", "biopython==1.85", "python3"] + probe
278:        r = subprocess.run(cmd, cwd=str(p.root), capture_output=True, text=True, timeout=600)
```

`Bio` is absent on this host (`python3 -c "import Bio"` → `ModuleNotFoundError: No module named 'Bio'`), so
**every** `--rerun` gate run — 90 `uv` execve per full C1 run, `c1-uv-counts.txt` — leaves the repo and resolves
`biopython==1.85` from PyPI unless the host cache is warm.

**Evidence.**

- Cold cache, network allowed: `strace -f -e trace=connect env UV_CACHE_DIR=$S/uvcold uv run --no-project
  --with biopython==1.85 python3 -c 'import Bio;print(Bio.__version__)'` → `Downloaded numpy / Installed 2
  packages in 124ms / bio 1.85`, `connect_calls=81`, `151.101.{0,64,128,192}.223` (Fastly/PyPI), cold-cache
  footprint 143M (`uv-network-cold-cache.txt`).
- Full C1, offline + cold cache: `unshare -rn env UV_OFFLINE=1 UV_CACHE_DIR=$S/uvoff python3
  plans/round38_c1_verify.py --lane . --work $S/w3` → `BATTERY fixtures=86 wrong=1 …`,
  `MUTANTS total=22 killed=18 survived=4`, survivors **N13, N14, N15, N21**; the one wrong fixture is
  `FIXTURE p10b-rerun-byte-equal-accept expect=accept … observed_rc=1 observed_defects=P10 WRONG`
  (`c1-offline.out`). The battery's own `wrong=0` invariant is therefore environment-dependent.
- Full C2, offline + cold cache: `V2 DEFECT spec=frozen gate=frozen gate_exit=1` with
  `gate: P10 DEFECT fresh probe exit=1 stderr='error: No solution found when resolving --with dependencies'`,
  `checks=7 defects=1`, `PREDICATE C2 fail` (`c2-offline.out`).

**Impact.** The landing receipts (`measure-final.txt`, `build-pmars-probe.txt`) are only reproducible where `uv`
plus biopython 1.85 are present in a cache, or with network. A reviewer on an offline/clean host measures
C1 `killed=18` and C2 `fail` — i.e. the same frozen predicate yields the opposite verdict, and the claims'
Limits never name this precondition (they name "host bash stands in for Debian dash", "host glibc `ldd`").

**Smallest remediation.** Pin the probe interpreter instead of discovering it: add a `probe_python` spec key
(or vendor the needed module) and refuse with a distinct note when it is absent; record "network or a warm
`~/.cache/uv`" as an explicit precondition in `round-38-claims.md` C1/C2 Limits and in the receipt label.

## F2 — HIGH — the 21 kills are carried by `plans/battery38/*.py`, which the counter does not pin

**Evidence.** `PINS` in `plans/round38_c1_verify.py` holds 14 entries — gate, r37 counter, r36 counter, r35
spec, r37 attribution, and **nine `plans/battery37/` modules**. `battery38 entries in PINS: 0`
(`battery38-pins.txt`, which also lists the twelve on-disk digests, e.g.
`e65f7a54…  plans/battery38/p10a.py`). The frozen predicate's first line is `PINS total=14 mismatched=0`; that
line is silent about the files that produce `killed=21`.

**Impact.** Editing one fixture (or checking out a stale/instrumented copy) keeps `PINS mismatched=0` while
`killed` silently changes; the landing receipt does not bind its own kill carriers. C2 already does the right
thing for its probe (V5 pins `PROBE_SHA256`, `DRY_SHA256`); C1 is asymmetric.

**Smallest remediation.** Add the twelve `plans/battery38/*.py` digests to `PINS` and to the frozen predicate
text. The counter already globs the dir; this is a dict addition, no rule change.

## F3 — HIGH — fixtures are arbitrary in-process code and fixture-owned specs are executed; both guards are one-line bypassable

**Exploit path.**

1. `plans/round38_c1_verify.py:158` — `spec.loader.exec_module(mod)`: every battery38 module's top level (and
   its `build(ctx, d)`) runs **inside the counter process**, full privileges, no sandbox. The counter has no
   mechanism that could confine it.
2. Spec *contents* are unconstrained (only the `--spec` path is checked). `probe_cmd` is executed with
   `cwd=root` and, because the gate passes no `env=`, the caller's whole environment: T1 measured
   `env_keys=271`, of which 9 carry secret names (`OPENAI_CODEX_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN`,
   `XAI_OAUTH_TOKEN`, `HL_INITIAL_WORKSPACE_TOKEN`, `OPKEY_VAULT`, …) (`probe-exec-orphan.txt`,
   `sidechannel-and-env.txt`). One line of probe code reads them.
3. Absolute spec paths escape the root. Spec `receipt=/etc/hostname` with the host file's digest pinned →
   `P2 ok receipt_sha256=pinned`; the same fixture's `probe_cmd` wrote outside `--root` →
   `outside_written=True : wrote outside root, cwd=…/iso2/pkg` (`spec-path-escape.txt`).
4. The `--spec` guard is bypassable: the counter inspects `argv.index("--spec")` (first occurrence,
   `:243-245`) while argparse takes the **last**. argv
   `… --spec <d>/inside.json --spec <outside>.json` → `guard PASSES` **and**
   `outside-dir spec's probe_cmd executed: executed from a spec OUTSIDE the fixture dir`
   (`spec-guard-bypass.txt`).
5. The side-channel scan is five literal tokens (`SIDECHANNEL = ("/proc", "ppid", "cmdline", "psutil",
   "environ")`, `:89`): `getattr(__import__('os'),'env'+'iron')` and `os.listdir('/'+'proc')` both score
   `[]` hits (`sidechannel-and-env.txt`).

**Impact.** `sidechannel=0` is not a containment signal. With F2, an edit to one unpinned fixture executes on
every future counter run with the reviewer's privileges and secrets. The claims' limit ("battery38 code review
by a non-author seat remains part of admission") is therefore the *only* control, and it is textual, not
structural.

**Smallest remediation.** (a) pin the fixtures (F2); (b) run `build()` in a subprocess with `cwd=d` and a
scrubbed env; (c) in `run_gate`, pass `env=` with a minimal set and reject argv with more than one `--spec` or
any non-whitelisted flag; (d) drop the token heuristic once (b)/(c) make it unnecessary.

## F4 — MEDIUM — probe execution escapes the seat's scratch and outlives the gate

**Evidence.**

- C2's probe ignores the counter's `--work`: full C2 with `--work $S/w2` and `TMPDIR` unset creates
  `"/tmp/k38-bpm-gzl40ci1"` (strace of my own pid tree, `strace-derivations.txt`). `build_pmars_probe.py:308`
  honours only its own `--work`, and `pkg_gate.py:278` never passes one.
- `cwd=root` is not write confinement (F3 item 3).
- A timeout kills only the direct child. T1 (the exact shape of `run_gate`'s `timeout=900`, `:181`) SIGKILLs
  the gate and leaves the probe running: `T1 gate_pid=… alive_after=False` and
  `T1 probe_pid=2211072 SURVIVED_after_gate_SIGKILL=True`, `ps … python3 …/probe_body.py`
  (`probe-exec-orphan.txt`). `pkg_gate.py:278`'s `timeout=600` has the same shape for the probe's own children.

**Impact.** A full C1+C2 run writes outside `--work` (the C2 build tree with gcc output); an aborted counter
leaves gcc artefacts in `/tmp` and can leave a probe (unsandboxed, secrets in env) running past the abort.

**Smallest remediation.** Pass the counter's work root to the probe (`--work <root>`), export `TMPDIR` into the
child env, and start each gate with `start_new_session=True` so the timeout path can `killpg` the whole tree.

## F5 — MEDIUM — C2's V6 executes unpinned host state at a hardcoded absolute path

**Evidence.** `plans/round38_c2_verify.py:63`: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`;
V6 accepts any `returncode == 0`. With a two-line shim at that path V6 returns `(True, 'census_exit=0')`;
with the script absent it raises `FileNotFoundError`, which `main` converts to `V6 DEFECT` →
`PREDICATE C2 fail` (`c2-v6-host-state.txt`).

**Impact.** One of the seven frozen checks — and therefore the C2 predicate — is gated by mutable state outside
the repo and outside every pin (a 35 KB bash script executed with the reviewer's privileges). It also makes
"C2 passes on a clean clone of the landing tip" untrue off this workstation.

**Smallest remediation.** Pin the census script by sha256 inside the counter (or vendor it under `plans/`) and
print the digest in the V6 note.

## F6 — LOW — `uv` and `git` are PATH-resolved inside the verified path

`pkg_gate.py:260` `subprocess.run(["git", "-C", str(p.root), "ls-files", …])` and `:276` `cmd = ["uv", …]`.
The C2 probe by contrast uses absolute `BWRAP`/`GCC`. A hostile PATH makes the gate execute an attacker-chosen
`uv`/`git`, after which every verdict is attacker-chosen. Remediation: resolve once with `shutil.which` and
refuse when the result is outside `/usr/bin` and `~/.local/bin`.

## F7 — LOW — a missing `--work` parent dies with an uncaught traceback

`python3 plans/round38_c2_verify.py --lane . --work <nonexistent>` → `FileNotFoundError: … '/…/w7/k38-c2-1a81gwv3'`,
exit 1 with a traceback and no `PREDICATE` line (C1's `tempfile.mkdtemp(prefix="k38-c1-", dir=a.work)` is the
same). Cosmetic, no verdict integrity issue. Remediation: `mkdir(parents=True, exist_ok=True)` before use.

## Attacked and not broken (positive controls)

- Clean-clone reproduction: C1 `killed=21 survived=1 PREDICATE C1 fail`; C2 `checks=7 defects=0 PREDICATE C2
  pass`, and C2 passes **after** C1 in the same clone (`gate: P9 ok untracked=0`, `__pycache__/` is gitignored;
  `c2-after-c1.out`).
- Residue after clean full runs: `procs referencing my scratch: 0`, `bwrap procs … 0`, `/tmp k38-bpm dirs: 0`,
  `/tmp k38-c1/c2 dirs: 0`, work dirs left: 0, clone modified paths: 0 (`residue-checks.txt`).
- The C2 probe's executed grader is properly boxed — net unreachable, `/app` read-only, private `/dev`, private
  pid namespace (5 pids), `$HOME` absent, `/tmp` a tmpfs (`battery38-pins.txt`); `connect_calls=0` over a full
  C2 run with a warm cache (`strace-derivations.txt`).
- Warm-cache host writes are bounded and transient: 21 `O_CREAT` files under
  `~/.cache/uv/builds-v0/.tmpXXXX/…` per `uv` invocation, removed on exit (`strace-derivations.txt`); uv's
  cold-cache download is the only persistent host write I measured.

## Limits of this check

`find ~ -newer` over the run window saw 650 touched paths, but 20+ sibling seats run the same counters
concurrently, so host-write attribution is by strace of my own pid tree, not by mtime; `ss` was not used —
`strace -e trace=connect` substitutes and is stronger. I did not attempt the kill-attribution falsification
(the 21 kills' *clause* fits) — other seats own that. No tooling installed (pacman paused; nothing needed).

Receipts: `falsify/F38SentinelBattery/` (`c1.out`, `c1-offline.out`, `c2.out`, `c2-offline.out`,
`c2-after-c1.out`, `c1-uv-counts.txt`, `strace-derivations.txt`, `uv-network-cold-cache.txt`,
`probe-exec-orphan.txt`, `spec-path-escape.txt`, `spec-guard-bypass.txt`, `c2-v6-host-state.txt`,
`sidechannel-and-env.txt`, `battery38-pins.txt`, `residue-checks.txt`).

VERDICT: sentinel-7-findings
