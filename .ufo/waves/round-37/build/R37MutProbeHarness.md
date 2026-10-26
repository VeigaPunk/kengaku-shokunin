# R37MutProbeHarness — mutation probe of the frozen C2 harness `plans/git_webserver_probe.py`

kengaku round 37, wave 1, 2026-10-26. Seat: mutation-tester (leaf). Target: the frozen probe
`plans/git_webserver_probe.py` (sha256 `63cb75cf…5eedf`) and its captured grader inputs.

## Method and isolation

- Every run used a **copy** under `/fast/scratch/hyaku/kengaku-r37/R37MutProbeHarness/` as a mini lane tree
  (`plans/git_webserver_probe.py` + `corpus/evidence/round37/tb2-git-webserver/{verify.sh,test_outputs.py,instruction.md}`).
  The lane itself was **never written**: all four lane files hash identically before and after every run (see Restoration).
- Detector: full probe run `python3 plans/git_webserver_probe.py --lane <scratch-lane> --work <scratch>`; the receipt is
  compared byte-wise against the pristine baseline. Scratch was rebuilt from pristine bytes per mutant, and removed at the end.
- No tool installs were needed (bwrap already at `/usr/bin/bwrap`; `expect` absent on host, which the probe itself relies on).

## Baseline (pristine)

Command: `python3 $S/lane/plans/git_webserver_probe.py --lane $S/lane --work $S/w` (S = scratch root).
Output: exit 0, 52.7 s, tail `cases=22 observed_pass=9 observed_fail=13 mismatches=0`.
`diff corpus/evidence/round37/git-webserver-probe.txt <baseline>` → **empty** ("IDENTICAL to frozen receipt").
So the detector's green state is byte-equality with the frozen receipt; any mutant is judged by its diff against that.

## Mutants

| id | mutation (copy only) | expected detector | observed | verdict |
|----|----------------------|-------------------|----------|---------|
| M-a | flip one case's prediction: `static-file-no-git` `pass`→`fail` | `mismatches=1`, CASE line `match=NO` | exit 0; line 7: `CASE static-file-no-git tools=curl predicted=fail observed=pass match=NO`; tail `cases=22 observed_pass=9 observed_fail=13 mismatches=1`; diff vs baseline = exactly those 2 lines | **detected** |
| M-b | tamper 1 byte of the copied `verify.sh` (offset 14, `T`→`X` in the header comment `# This script tests`; tampered sha256 `545fcdf5719fab85e03791026da1c5d27b8855221926680992e1efa8ffd9e986`) | refusal before any case | exit 2; stdout 0 bytes (no case ran); stderr: `SETUP capture verify.sh missing or not at its pinned digest` | **detected** |
| M-c | drop `--unshare-net` from `sandbox_argv` | verdicts unchanged on this host; leak channel possible | exit 0; receipt **identical** to baseline (`mismatches=0`) | **undetected** (invariant holds today; see leak analysis) |
| M-d | stub `apt-get` and stub `expect` (`#!/usr/bin/bash\nexit 0`) written into every case's `/work/bin` | verdicts unchanged | exit 0; receipt **identical** to baseline | **undetected** (invariant holds) |
| M-e | `SERVER_PY` writes `/work/ready` **before** `srv = S((...))` (bind) | possible flake: curl before `listen()` | run1 + run2: exit 0, receipt identical to baseline; clean reruns: see §M-e below | **undetected over the clean runs** (race window real but masked) |
| M-f | HOME override removed: `"HOME": "/work/home"` → `"HOME": os.environ["HOME"]`, driver run with `HOME=$S/fakehome` (throwaway; real HOME never used) | verdicts unchanged; write target moves | see §M-f: verdict rc unchanged; `verify.sh` writes `$HOME/.ssh/config` wherever HOME points | **undetected** (write-target invariant confirmed) |

**Tally: detected 2/6 (M-a, M-b); undetected 4/6 (M-c, M-d, M-e, M-f).**

## M-c: `--unshare-net` dropped — verdicts unchanged, leak channel proven

- Full 22-case run with shared network namespace: exit 0, `cases=22 observed_pass=9 observed_fail=13 mismatches=0`,
  `diff` vs baseline → empty ("IDENTICAL receipt to baseline").
- Host check first (`ss -ltn`): listeners on :53 (x3), :631, :34701, :44385, :8793, :8787–:8791, :8795–:8796, :5355 —
  **no listener on :8080** (`ss -ltn | grep -c ':8080 '` → `0`). Nothing was started on the host's :8080.
- Leak channel demonstrated without touching :8080 — same bwrap argv, curl to a service that does exist on the host loopback:
  - with `--unshare-net` (as frozen): `host CUPS on 127.0.0.1:631 -> 000` (unreachable — isolated);
  - with `--unshare-net` dropped: `host CUPS on 127.0.0.1:631 -> 200` (reachable — loopback is shared).
- So **yes, a host service on :8080 would leak into every case**: the case's own server would fail to bind
  (`Address already in use`) and `curl http://localhost:8080/hello.html` would hit the host's service instead. On this host
  today nothing listens there, so no verdict changes — the probe has **no internal detection** of a missing `--unshare-net`;
  case isolation rests entirely on that one flag.
- Why the shared net still changes nothing here: `apt-get` is not on the case PATH at all — inside a shared-net case sandbox,
  `command -v apt-get` → rc 1 (not found), `apt-get update` → rc 127. The cases' only network use is curl/wget to
  `127.0.0.1:8080` (and :8081 for `wrong-port-8081`), so there is no other network-dependent behavior to perturb.

## M-d: stub `apt-get` + stub `expect` (exit 0) on the case PATH

Full 22-case run: exit 0, receipt **identical** to baseline (byte-equal). The stubs make verify.sh's install step
(`apt-get update`, `apt-get install -y expect`, verify.sh:10–11) "succeed" and put an `expect` on PATH, and no verdict moves —
confirming the docstring's claim: nothing in verify.sh reads those exit statuses, and the expect script `git_test.exp` is
invoked via its absolute shebang `#!/usr/bin/expect -f` (verify.sh:15), which stays absent from the sandbox regardless of PATH.

## M-e: ready file written before bind — flakiness over repeated runs

Mutation: in `SERVER_PY`, `pathlib.Path("/work/ready").write_text("1")` moved above `srv = S(("127.0.0.1", cfg["port"]), H)`.
The wait loop in `run.sh` then breaks immediately, before the server has bound — the race the probe's ordering exists to avoid.

- First batch: run1 exit 0, receipt identical to baseline; run2 exit 0, receipt identical to baseline (background job
  bg_1707, byte-compared with `cmp`: `run1 == baseline`, `run2 == baseline`).
- First-attempt run3 of that batch ended nonzero while my own concurrent detector probes (M-f variants) were running bwrap at
  the same time; its output file was copied mid-run (partial, 18/22 CASE lines, no SETUP line) and the original was lost with
  the scratch cleanup — **not attributable** to the mutant. Kept as `m-e-run3-first-attempt-partial.txt`.
- Clean sequential reruns (no concurrent load), 4 runs (bg_1893): rerun1–rerun4 all `exit=0`,
  `cases=22 observed_pass=9 observed_fail=13 mismatches=0`, each byte-identical to baseline (`cmp`), no `match=NO`,
  no `SETUP` failures. Total evidence: **6 clean full runs under the mutant, zero flakes**. The race window is real
  (the wait loop breaks before `listen()`), but it is masked in practice by verify.sh's `sleep 2` (verify.sh:53) and the
  failed-`apt-get` attempt that precede the first curl — the server binds within milliseconds of writing the ready file.

## M-f: HOME override removed — where does verify.sh's `~/.ssh/config` go?

Mutation: `env` in `run_case` passes `os.environ["HOME"]` through instead of pinning `/work/home`. Driver run with
`HOME=$S/fakehome` (throwaway under scratch; the real HOME was never used in any sandbox env). Inspection harness runs
`/usr/bin/bash /tests/verify.sh` exactly as `test_outputs.py` does, then reports `$HOME/.ssh/config`.

- **f1, pure mutant** (no other change): inside the sandbox `HOME=/fast/scratch/.../fakehome`,
  `sshconfig-exists True`, content `'Host localhost\n    StrictHostKeyChecking no\n    UserKnownHostsFile=/dev/null\n'`
  (verify.sh:14–17). Host-side `$S/fakehome` **empty** after the run — the write landed in the sandbox's private root
  (the sandbox root is writable: `mkdir -p /fast-probe/x` succeeds inside), so nothing leaked out.
- **f2, mutant + detector bind** (fakehome bound into the sandbox at its host path — detector instrumentation, not a probe
  change): same inside view, and host-side `$S/fakehome/.ssh/config` **present on the host** — direct confirmation that
  verify.sh writes `<HOME>/.ssh/config` wherever HOME points.
- **Pristine control** (same inspection): `HOME=/work/home`, `/work/home/.ssh/config` exists with the same content;
  the throwaway home untouched.
- Verdicts: `VERIFY rc 0` in all three variants — the verdict path never reads the config, so the mutant is undetected by
  verdicts; the confirmed invariant is that **the override is what pins verify.sh's write to `/work/home`** (a scratch dir the
  probe deletes after the case), and without it the target is whatever HOME the probe inherits.
- Real-HOME safety: `/home/vgpnk/.ssh/config` mtime `2026-10-11 10:33:49` — predates every run today; no sandbox env ever
  contained the real HOME.

## Restoration evidence

Lane files, sha256 before all runs == after all runs (never written; every mutant ran on a scratch copy):

```
63cb75cfcd1c224a38eef34b99b66c9ec837261ca8c369577b23601ed3a5eedf  plans/git_webserver_probe.py
1dc44c923b797ed24ca423c9b9efcd9c1eed4d7261007139b0a724f4e2f53d05  corpus/evidence/round37/tb2-git-webserver/verify.sh
526aee3dfe952cc4c7574361012712e389d6fba7222c005fc3e939fc53346b37  corpus/evidence/round37/tb2-git-webserver/test_outputs.py
62151b7371bc364277a3c118bba755334c640fb0cefc7a5af106e6e763cf1d97  corpus/evidence/round37/tb2-git-webserver/instruction.md
```

Scratch `/fast/scratch/hyaku/kengaku-r37/R37MutProbeHarness/` removed after receipts were copied to
`.ufo/waves/round-37/build/R37MutProbeHarness/` (baseline.txt, m-a.txt, m-b.txt/.err, m-c.txt, m-d.txt, m-e-run1/2.txt,
m-e-run3-first-attempt-partial.txt, m-e-rerun1..4.txt).

## Findings for the lane

1. The probe's two hard guarantees (capture digests, prediction accounting) are **detected-mutation-proof**: a flipped
   prediction shows up as `match=NO` + `mismatches=1` in the receipt (exit code stays 0 — downstream checkers must read the
   receipt, not the exit code), and a one-byte capture tamper is refused with exit 2 before any case runs.
2. The one real coverage finding is **M-c**: nothing in the probe detects a missing `--unshare-net`; on a host that does run
   something on :8080, every case's verdict could be silently shaped by that host service. The frozen `--unshare-net` is
   load-bearing and undetected if absent.
3. M-d/M-f confirm the docstring's stated independence claims (statuses of `apt-get`/`expect` unread; HOME pin controls the
   write target of `~/.ssh/config`). M-e shows the ready-before-bind race is masked in practice by verify.sh's `sleep 2`
   (verify.sh:53) before the first curl — no flake observed in the clean runs.

VERDICT: probe-harness-mutants-2/6
