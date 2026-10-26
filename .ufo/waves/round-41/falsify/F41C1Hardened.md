# F41C1Hardened — hardened re-measure of the round-41 C1 counter

Seat: `F41C1Hardened` (executor, wave 2 falsify). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
(`HEAD=d7c77895752a2a5f317fa22f2362416ada50a04b`, the wave-2 dispatch commit whose parent is the stated tip
`3d0058fbde484c9d6c23fd997d9ee09a0663bcdb`). Clean clone used for every measurement:
`/fast/scratch/hyaku/kengaku-r41/F41C1Hardened/lane` (`git rev-parse --show-toplevel` verified =
`…/F41C1Hardened/lane`, `git status --porcelain` empty, `HEAD=d7c7789`).
Envelope on every counter/battery run (orchestrator host-safety rule):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin \
      --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>
```

Nothing frozen was touched: the 11 entries of `.ufo/waves/round-41/claims/frozen-digests.txt` re-hash to
`mismatched=0`, and the lane's tracked tree is clean (`git status --porcelain` shows only the wave-2
orchestrator's own `?? .ufo/waves/round-41/falsify*`). Scratch (`/fast/scratch/hyaku/kengaku-r41/F41C1Hardened`)
deleted at the end; receipts copied next to this report.

Axes walked: **(1)** do the five named wave-1 holes actually close in a repaired counter, **(2)** does the landed
battery still measure `23/23` under that repaired counter, **(3)** what stays open after the five repairs.

---

## 1. The artifact under test

`round41_c1_verify_hardened.py` = byte copy of `plans/round41_c1_verify.py`
(`8835a94b0ad62dc1f58c861e2025b7c4bc8c0b936c202c64e01bc8b43f53eaa8`) plus five repairs
(`3e8576164b8814bb2f75384b89540366a694883498c7514e9a988e5c581bd28f`). Six hunks, 92 diff lines
(`diff -u plans/round41_c1_verify.py round41_c1_verify_hardened.py`, receipt `diff-hardened.patch`):

```diff
@@ -235,7 +235,7 @@
 def sha256(p):
     try:
-        return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
+        return file_sha256(p)
     except OSError:
         return None
@@ -314,8 +314,9 @@
-def ro_sandbox(writable=(), ro_binds=(), hide=()):
+def ro_sandbox(writable=(), ro_binds=(), hide=(), ro_data=()):
     argv = [BWRAP, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--unshare-pid", "--unshare-net",
+            "--unshare-ipc", "--tmpfs", "/run",
             "--die-with-parent", "--new-session"]
@@ -323,9 +324,20 @@
+    for fd, dst in ro_data:
+        argv += ["--ro-bind-data", str(fd), str(dst)]
     return argv
 
+def file_sha256(p):
+    """Content digest of one file, streamed: no read of the whole file into memory."""
+    h = hashlib.sha256()
+    with open(p, "rb") as fh:
+        while chunk := fh.read(1 << 20):
+            h.update(chunk)
+    return h.hexdigest()
+
 def fingerprint(d):
@@ -340,8 +352,7 @@
             if not link and os.path.isfile(p):
-                with open(p, "rb") as fh:
-                    content = hashlib.sha256(fh.read()).hexdigest()
+                content = file_sha256(p)
@@ -349,8 +360,12 @@
 def path_ok(tok, d):
     if WORK_TOKEN.match(tok):
         return ".." not in tok
+    d = d.resolve()
     for cand in (tok, tok.split("=", 1)[1] if tok.startswith("--") and "=" in tok else ""):
-        if cand.startswith("/") and not pathlib.Path(cand).resolve().is_relative_to(d.resolve()):
+        if not cand:
+            continue
+        base = pathlib.Path(cand) if cand.startswith("/") else d / cand
+        if not base.resolve().is_relative_to(d):
             return False
     return True
@@ -416,13 +431,19 @@
         slot = self.slots / f"{tool}.py"
-        cmd = ro_sandbox(writable=(work, tmp), ro_binds=((variant, slot),)) + [PY, str(slot), *argv]
+        src = open(variant, "rb")
         try:
-            r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(tmp), capture_output=True, text=True,
-                               timeout=600)
-        except subprocess.TimeoutExpired:
-            return ("timeout", frozenset())
+            cmd = ro_sandbox(writable=(work, tmp),
+                             hide=[p for p in (self.root / "variants", self.root / "slots", self.root / "bin")
+                                   if p.exists()],
+                             ro_data=((src.fileno(), slot),)) + [PY, str(slot), *argv]
+            try:
+                r = subprocess.run(cmd, cwd=str(fx["dir"]), env=self.env(tmp), capture_output=True, text=True,
+                                   timeout=600, pass_fds=(src.fileno(),))
+            except subprocess.TimeoutExpired:
+                return ("timeout", frozenset())
         finally:
+            src.close()
             shutil.rmtree(work, ignore_errors=True)
             shutil.rmtree(tmp, ignore_errors=True)
```

Repair mapping: (a) `--ro-bind-data` + `hide={root/variants, root/slots, root/bin}` in `Runner.run`;
(b) `--unshare-ipc`; (c) `--tmpfs /run`; (d) `path_ok` resolves every token against `d`; (e) streaming
`file_sha256` used by `fingerprint` **and** `sha256` (pins/variants). Mutant list, directions, predicate and
floors are untouched — segment-by-segment comparison against the frozen file:

```
MUTANTS = [                identical=True
TOTAL =                    identical=True
FLOORS =                   identical=True
def exhibits(              identical=True
def seen_directions(       identical=True
SIMPLE_DIRECTIONS =        identical=True
PAIR =                     identical=True
good = (not mism and not   identical=True
floors_ok = (              identical=True
```

---

## 2. Each repair bites — one hostile module per repair

Module-source receipts: `.ufo/waves/round-41/falsify/F41C1Hardened/hostile-modules/h_*/`. Each module is a
battery module (same `FIXTURES`/`build(ctx, d)` contract) whose fixture is written so that its **declared**
result is only reached when the vector is open. Run shape (dev mode, so the predicate is `n/a` and the signal is
the `FIXTURE`/`BATTERY` line):

```
cd <clone> && $ENV python3 <counter> --lane . --battery-dir <module dir> --only NONE --work <scratch>
```

| repair | hostile module | deployed (frozen) counter | repaired counter |
|---|---|---|---|
| (a) variant store readable | `h_var` | `FIXTURE … ok`, `BATTERY fixtures=1 wrong=0` | `FIXTURE … WRONG`, `wrong=1` |
| (b) IPC namespace shared | `h_ipc` | `… ok`, `wrong=0` | `… WRONG`, `wrong=1` |
| (c) host `/run` readable | `h_run` | `… ok`, `wrong=0` | `… WRONG`, `wrong=1` |
| (d) relative argv escape | `h_esc` | both fixtures `ok`, `wrong=0` | `SETUP fixture 'h_esc-relative-escape' … breaks the contract` |
| (e) whole-file fingerprint | `h_big` (RLIMIT_AS 2 GiB) | `MemoryError` (no verdict at all) | `… ok`, `wrong=0` |

Raw output (`matrix.txt`):

```
### module=h_var counter=frozen
FIXTURE h_var-variant-store-visible tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/r/vis-probe.txt observed_rc=0 observed=control:differ,equal:corpus/evidence/r/vis-probe.txt ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
### module=h_var counter=hardened
FIXTURE h_var-variant-store-visible tool=receipts expect=accept declared=control:differ,equal:corpus/evidence/r/vis-probe.txt observed_rc=1 observed=differ:corpus/evidence/r/vis-probe.txt WRONG
BATTERY fixtures=1 wrong=1 tampered=0 sidechannel=0

### module=h_ipc counter=frozen
FIXTURE h_ipc-build-segment-visible … observed_rc=0 observed=control:differ,equal:corpus/evidence/r/ipc-probe.txt ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=1
### module=h_ipc counter=hardened
FIXTURE h_ipc-build-segment-visible … observed_rc=1 observed=differ:corpus/evidence/r/ipc-probe.txt WRONG
BATTERY fixtures=1 wrong=1 tampered=0 sidechannel=1

### module=h_run counter=frozen
FIXTURE h_run-host-run-visible … observed_rc=0 observed=control:differ,equal:corpus/evidence/r/run-probe.txt ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=1
### module=h_run counter=hardened
FIXTURE h_run-host-run-visible … observed_rc=1 observed=differ:corpus/evidence/r/run-probe.txt WRONG
BATTERY fixtures=1 wrong=1 tampered=0 sidechannel=1

### module=h_esc counter=frozen
FIXTURE h_esc-local-tree … observed=map:corpus/evidence/r/ext-probe.txt:derived ok
FIXTURE h_esc-relative-escape … observed=map:corpus/evidence/r/ext-probe.txt:derived ok
BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=1
### module=h_esc counter=hardened
SETUP fixture 'h_esc-relative-escape' of h_esc/h_esc.py breaks the contract

### module=h_big counter=frozen (RLIMIT_AS=2GiB)
  File "…/lane/plans/round41_c1_verify.py", line 549, in main
    prints = [fingerprint(fx["dir"]) for fx in fixtures]
  File "…/lane/plans/round41_c1_verify.py", line 344, in fingerprint
    content = hashlib.sha256(fh.read()).hexdigest()
MemoryError
### module=h_big counter=hardened (RLIMIT_AS=2GiB)
FIXTURE h_big-sparse-fixture-file … observed=map:corpus/evidence/r/big-probe.txt:derived ok
BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
MUTANTS total=0 killed=0 survived=0 invalid=0 null_detected=0
```

(`sidechannel=1` on `h_ipc`/`h_run`/`h_esc` is the counter's own token scan flagging **my** module source —
`ctypes`, `socket`, …; it is the heuristic working, not a defect. `h_big` lowers `SIZE=5 GiB` sparsely; the
build had no disk cost, `du` stayed at 528 MB for the whole scratch.)

### 2.1 Primitive-level proof for (a) — the A1′ self-identification vector

A probe stub runs as a **child of the tool inside the tool's own sandbox**. Given the same layout the counter
builds (`root/{variants,slots}/`, cwd deep under `root/work/w000001/run/tip-x/tip`, `slots/receipts.py` bound to
the **T10** mutant):

```
[frozen-style sandbox]  probe inside the tool run identifies: 'SELF=T10.py'
[five-repair sandbox]   probe inside the tool run identifies: 'SELF=unknown'
```

i.e. on the deployed counter any fixture probe can name the exact mutant it is running under (compare
`slots/receipts.py` with `variants/*.py`) and steer its verdict; after the repair there is nothing to compare
against. This is the wave-1 `R41CritC1Counter.md` A1′ / `R41SentinelCounter.md` F1 vector, closed by (a).

### 2.2 Primitive-level proof for (d)

`path_ok` on the same inputs (`d = …/rep/po/f000`):

```
token                                   frozen  hardened
../f001/lane                            True    False
../../../etc/hostname                   True    False
./sub/../../f001                        True    False
--lane=../f001/lane                     True    False
/etc/hostname                           False   False
{WORK}                                  True    True
{WORK}/sub                              True    True
{WORK}/../x                             False   False
--lane=<abs path inside d>              True    True
--tamper=corpus/evidence/r/x.txt        True    True
--access-date=2026-01-01                True    True
```

The `--flag=value` shape is covered because the value is resolved too (last three rows keep working, so
non-path tokens are not over-rejected).

### 2.3 Primitive-level proof for (e)

Same digest, different memory (`fingerprint` over a directory holding one 1 GiB file and one small file,
`resource.getrusage(RUSAGE_SELF).ru_maxrss` in a child):

```
frozen   a65b139e7afde721… maxrss_kb=1067764 delta_kb=1047200
hardened a65b139e7afde721… maxrss_kb=22396   delta_kb=2048
```

Identical fingerprints (no semantics change), 1 GiB vs 2 MiB of peak RSS.

---

## 3. The landed battery under the hardened copy — unchanged

Both runs: clean clone, default battery (`plans/battery41`), predicate live.

```
$ $ENV python3 plans/round41_c1_verify.py --lane . --work …/w/landed-frozen      # receipt landed-frozen.txt
PINS total=2 mismatched=0
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass                      # rc=0   (real 5.19s)

$ $ENV python3 round41_c1_verify_hardened.py --lane . --work …/w/landed-hard        # receipt landed-hardened.txt
PINS total=2 mismatched=0
BATTERY fixtures=48 wrong=0 tampered=0 sidechannel=0
MUTANTS total=23 killed=23 survived=0 invalid=0 null_detected=0
MUTANTS-BY-TOOL receipts=13/13 sources=10/10
ADVERTISED direct=21 indirect=2 none=0
PINS-AFTER mismatched=0
PREDICATE C1 pass                      # rc=0   (real 4.58s)
```

`diff landed-frozen.txt landed-hardened.txt` → **IDENTICAL OUTPUT** (byte-equal after stripping trailing
whitespace), *including every `FIXTURE` line and every `killed by=` attribution*:

```
T01 r_setup-t01-lane-absent         T09 r_map-t09-shared-stem-separators   S01 s_modes-s01-quote-plus-package
T02 r_setup-t02-no-evidence         T10 r_map-t10-derived-mapping          S02 s_usage-02-registry-without-package
T03 r_run-t03-rc-nonzero-mixed      T11 r_map-t11-table-overrides-derived  S03 s_usage-03-dotted-access-date
T04 r_run-t04-temp-paths-masked     T12 r_map-t12-log-population           S04 s_modes-s04-url-map-with-adopt
T05 r_setup-t05-tamper-absent       T13 r_ctl-t08-derived-uv-absent        S05 s_usage-05-two-ids-without-entries
T06 r_ctl-t06-empty-equal-receipt                                          S06 s_usage-06-recheck-cadence-word
T07 r_setup-t07-lane-subdir                                                S07 s_exit-collision-admit
T08 r_ctl-t08-derived-uv-absent                                            S08 s_modes-s08-quote-file-without-artifact
                                                                           S09 s_modes-s09-url-map-nested-shape
                                                                           S11 s_exit-queued-admit
```

Non-vacuity preserved: the same hardened copy with `MUTANTS = []` prints
`MUTANTS total=0 …` then `PREDICATE C1 fail` (receipt `control-hardened-no-mutants.py`, the same edit the
freeze's `control-c1-no-mutants.txt` uses). So the 23/23 does not come from a loosened predicate.

**Answer to the wave-2 question for this seat: yes — the landed battery still prints `MUTANTS total=23
killed=23` and `PREDICATE C1 pass` under the hardened copy, with identical per-mutant attribution.**

---

## 4. Does the landed battery *use* any of the five vectors? No

Direct scan of the 7 modules (`plans/battery41/*.py`):

```
$ grep -nE 'ctypes|shmget|"/proc"|/run/|socket|__file__|inspect|variants|slots\b|sys\.path|environ' *.py
r_run.py:95:    b = "slot audit probe\nslots=5\nwindows=2\n"                 # probe *text*, not the counter slot
s_exit.py:28:        anchor='… eleven o clock slots are one hour" …'         # quoted prose
$ grep -nE "'\.\./|\"\.\./" *.py            # (no output: no dot-dot argv token anywhere)
$ grep -hoE '"--[a-z-]+", *(str\([a-z_]+\)|\{[A-Z]+\})' *.py | sort | uniq -c | sort -rn
      7 "--registry", str(reg)   7 "--package", str(pkg)   5 "--lane", str(root)   2 "--lane", str(lane)
```

Every argv path is absolute-inside-`d` or a `{WORK}` token, and the counter's own `sidechannel` scan reports `0`
for the landed battery under both counters. So the five holes are **counter-side**: the landed 23/23 does not
rest on any of them, and repairing them costs the battery nothing (section 3).

---

## 5. What still breaks after the five repairs (residuals, measured)

1. **Read-only host copies of the tool remain visible inside tool runs.** With the variant store hidden, a probe
   still finds the lane's pristine copy and can infer it is a mutant:
   `host_copies_seen=1 identical=0` inside the five-repair sandbox
   (glob `/home/vgpnk/Projects/shokunin/*/plans/tip_receipts.py`, `slots/receipts.py` = T10). This is the
   freeze's own named limit ("a module can still read other copies of the tools elsewhere on the read-only
   host").
   **Measured fix, not in the five repairs:** a sixth change (also `--tmpfs <lane>` in tool runs,
   `round41_c1_verify_hardened_plus.py`) gives `host_copies_seen=0` **and** the landed battery still prints
   `BATTERY fixtures=48 wrong=0 … MUTANTS total=23 killed=23 … PREDICATE C1 pass` (rc=0). Recommendation for the
   L1: fold this sixth change into the counter before the next freeze.
2. **AF_UNIX is not isolated.** `--unshare-net` does not cover unix sockets and `/run` is now empty, but any
   socket path visible on the read-only host is still connectable: a listener bound under the scratch dir
   accepted a connection from inside the five-repair sandbox (`AF_UNIX connected`, server got `b'HELLO'`).
   Same class as the wave-1 `F2`/`F3` limits; closing it needs a socket-blacklisting layer (seccomp/LSM), which
   this counter does not have.
3. **The counter's own scratch root stays readable to runs**: `root/fx/<module>/fNNN` siblings, `root/work/*`
   siblings and `root/rtmp/*` are visible read-only to every run (measured: `sibling_fixtures=['h_res']` from
   inside a run). A fixture can read another fixture's tree, though `path_ok` (repair d) no longer lets argv
   point at it.
4. **`/dev/shm` is per-sandbox but writable**, and `--proc /proc` is a fresh procfs: neither is a channel back
   to the host, but both are writable inside the run (bounded by the sandbox lifetime).
5. `path_ok` is a *contract* check on `build()`'s argv only; it says nothing about what a fixture writes inside
   `d` (by design — that is the fingerprint's job). A 5 GiB sparse file inside `d` is legal and, before repair
   (e), was enough to destroy the whole measurement.

---

## 6. Calibration notes and limits of this seat

- The five hostile modules run in **dev mode** (`--battery-dir … --only NONE`), so the counter prints
  `PREDICATE C1 n/a`; the red/green signal quoted above is the `FIXTURE … ok|WRONG` line, corroborated by the
  counter's exit status. Measured directly (`$ENV python3 <counter> … ; echo rc=$?`):

  ```
  h_var/frozen   rc=0  BATTERY fixtures=1 wrong=0 tampered=0 sidechannel=0
  h_var/hardened rc=1  BATTERY fixtures=1 wrong=1 tampered=0 sidechannel=0
  h_esc/frozen   rc=1  BATTERY fixtures=2 wrong=0 tampered=0 sidechannel=1
  h_esc/hardened rc=2  SETUP fixture 'h_esc-relative-escape' of h_esc/h_esc.py breaks the contract
  ```

  Note the `h_esc/frozen rc=1`: it is dev mode's `side == 0` clause, not a fixture failure — my own module source
  trips the token scan (`h_esc` contains "inspect" in prose; `h_ipc` "ctypes"; `h_run` "socket"). That is the
  heuristic firing on the reviewer's text, and it is why these modules are falsification instruments, not
  admission candidates.
- Every counter/battery run went through the mandated envelope (`--ro-bind ~/.local/bin`, `--tmpfs
  /run/user/1000`, `--unshare-pid`); nested bwrap inside it works (the counters' own sandboxes are nested one
  level deeper and still function — which is itself evidence that repair (b)/(c) compose with the envelope).
- Host touch outside my scratch/report dirs: the **deployed** counter's IPC demo left one 4 KiB SysV segment in
  the host IPC namespace until I removed it (`ipcrm -M 0x46343133`; `ipcs -m | grep -c 0x46343133` → `0`
  afterwards, re-checked at the end: `0`). That is the vector itself, on this host, and it is the reason the
  repair matters. No files were written outside `/fast/scratch/hyaku/kengaku-r41/F41C1Hardened` and
  `.ufo/waves/round-41/falsify/F41C1Hardened/`; no `~/.local/bin`, `/usr`, `/etc` or `$HOME` write; no git/jj
  mutation anywhere (the clone's `git status --porcelain` is empty, the lane's tracked tree is clean).
- `crit_git_shim.py` / `crit_ledger_selfread.py` were neither read nor used; no PATH shim was planted.
- Not measured here (other seats' question): whether the *content* of the 48 fixtures tests the advertised
  behaviour — I only attacked the counter's isolation and the battery's *use* of the holes.

Receipts next to this report: `diff-hardened.patch`, `landed-frozen.txt`, `landed-hardened.txt`, `matrix.txt`,
`round41_c1_verify_hardened.py`, `round41_c1_verify_hardened_plus.py`, `control-hardened-no-mutants.py`,
`hostile-modules/h_*/h_*.py`.

VERDICT: hardened-copy-battery-killed-23/23-repairs-biting-5/5
