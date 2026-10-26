# F39SentinelAudit — trusted-boundary review of the round-39 C1 audit and `plans/order_check.py`

Round 39 wave 2, seat `F39SentinelAudit` (sentinel). Target: the three new/changed tools —
`plans/round39_c1_audit.py` (child processes, nonce, fixture table), `plans/order_check.py` (git reads) — and
the wave-1 sentinel's C1 findings (`.ufo/waves/round-39/build/R39SentinelProbe.md`, F1–F6). Question: which
of F1–F6 remain open at the tip, and which does the audit close?

Measured in a clone of the lane at **`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`** (the tip named in this
ticket), scratch `S=/fast/scratch/hyaku/kengaku-r39/F39SentinelAudit` (removed at exit), `TMPDIR="$S"`:

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane" \
  && git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/kengaku-r39/F39SentinelAudit/lane
$ git -C "$S/lane" rev-parse HEAD
a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
```

Every git call in this seat named `-C "$S/lane"` (or `-C "$D"` for fixture repos); nothing was committed. No
lane file was edited: the attack modules and fixture trees exist only in the clone. The lane's `master` has
since moved to `acf4375`; `git -C <lane> diff --stat a6832f5 acf4375 -- plans/round39_c1_audit.py
plans/order_check.py plans/pkg_gate.py` is empty, so every finding below applies to master too.

## Axes named

1. **Does the audit's `AUDIT C1 clean` mean what the docstring says** (`round39_c1_audit.py:3-12`)?
2. **Is the audit's verdict load-bearing** — can a receipt carry `PREDICATE C1 pass` while the audit itself
   says `dirty`?
3. **Are the child-process boundaries real** (env, namespaces, process group, nonce secrecy)?
4. **Does `order_check.py` read the history it was told to read, and every blob shape in it?** (the tool's
   own claim: "Read-only by construction … It writes nothing, touches no network", `order_check.py:29-31`).

## 0. Baseline — the audit reproduces clean at the tip

```
$ cd "$S/lane" && python3 plans/round39_c1_audit.py --lane . --work "$S/w"
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
exit=0
```
(`run-baseline.txt`, 41 s.) So each result below is attributable to its module. Control: with
`plans/battery39/*.py` moved out of the clone, the audit prints `BATTERY fixtures=86 … MUTANTS total=7
killed=3 survived=4 invalid=0 null_detected=0`, `AUDIT C1 clean`, `PREDICATE C1 fail` (`run-ctl-empty.txt`)
— same four survivors as `plans/round-39-claims.md`'s do-nothing control.

---

## 1. S1 (High) — the A1 repair is defeated by a flip keyed to *which gate is running*; four fabricated kills on the real tip

`round39_c1_audit.py:394-399` re-runs the reference and the mutant on the killing fixture:

```
if exhibits(clause, direction, fx, ref[j], mut):
    again_ref = run_gate(ref_gate, ctx.spec_path, argv)
    again_mut = run_gate(mg, ctx.spec_path, argv)
    if again_ref != ref[j] or again_mut != mut:
```

Both replays are run with the same `argv` and against the same fixture tree, so they distinguish only an
input that is *different at replay time* from one that was the same all along — not an input that differs
**per phase**. The build child is unsandboxed (§5), so it can read the process table and pick the phase.

**Attack.** One new file, `plans/battery39/aa_sa_phasekey.py` (an executor's own write surface): it imports
the four wave-1 fixtures from `R39CritC1Counter/crit_a1_flip.py` unchanged, and replaces that module's daemon
with one that polls the process table every 2 ms and writes the *swap* spec into each fixture's live `--spec`
while a `gates/M0*.py` process is alive, and the *normal* spec back while `gates/ref.py` is alive. Reference
pass, renamed pass and `again_ref` therefore see the normal spec; every mutant run sees the swapped one.

On the real tip (all four honest battery39 modules present; the module sorts first, and the mutant loop breaks
at the first exhibiting fixture):

```
FIXTURE a1b-p1-second-instrument expect=reject declared=P1 observed_rc=1 observed_defects=P1 ok
FIXTURE a1b-p3-word-bound expect=reject declared=P3 observed_rc=1 observed_defects=P3 ok
FIXTURE a1b-p7-two-source-lines expect=reject declared=P7 observed_rc=1 observed_defects=P7 ok
FIXTURE a1b-d5-quote-swapped expect=accept declared=- observed_rc=0 observed_defects=- ok
BATTERY fixtures=94 wrong=0 renamed_disagree=0 sidechannel=0
MUTANT M02 P1 silence killed by=a1b-p1-second-instrument
MUTANT M03 P3 silence killed by=a1b-p3-word-bound
MUTANT M04 P7 silence killed by=a1b-p7-two-source-lines
MUTANT M07 D5 mirror killed by=a1b-d5-quote-swapped
...
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=0
AUDIT nondeterministic_kills=0
AUDIT C1 clean
PREDICATE C1 pass
exit=0
```
(`run-A1phase-tip2.txt`.) The awarded `killed by=` cells are fixtures whose reference leg is produced by one
input and whose mutant leg by another; the honest fixtures that do demonstrate the behaviours were never
reached. With the honest modules moved aside (the "battery39 only" surface), the same module alone gives
`BATTERY fixtures=90 … killed=7 … AUDIT C1 clean … PREDICATE C1 pass` (`run-A1phase3.txt`).

**It is exactly the repair that fails, not the flip.** The same four fixtures with the wave-1 *static* flip
(one permanent `os.replace`, module `crit_a1_flip.py` unmodified) are caught:

```
MUTANT M02 P1 silence SURVIVED ... MUTANT M07 D5 mirror SURVIVED exhibits=none
MUTANTS total=7 killed=3 survived=4 invalid=0 null_detected=0
AUDIT nondeterministic_kills=4 first=M02:a1b-p1-second-instrument
AUDIT C1 dirty
PREDICATE C1 fail
```
(`run-A1static.txt`.) So the docstring's claim (`round39_c1_audit.py:5-7`, "the reference gate is re-run on
the killing fixture AFTER the mutant run and must reproduce its first result") holds only against flips that
are still in place when the replay starts.

**Impact.** `AUDIT C1 clean` + `PREDICATE C1 pass` is not evidence that the four survivors were earned. The
audit adds no protection over the frozen counter for an adversary who can see which binary is executing —
which every battery module can, because it runs with `uid=1000` in the operator's environment.

**Smallest remediation.** Bind the fixture to *one* input for the whole run: copy each fixture directory to an
immutable snapshot before the reference pass (chmod a-w or a per-run read-only bind) and run both passes from
the snapshot, or hash the fixture tree (and any `--spec` inside it) before the reference pass and again before
each mutant run and again at replay, counting any drift as `invalid`, as wave-1 F2 asked. Failing that, run
the child under the existing bwrap recipe so the process table of the parent is not readable.

---

## 2. S2 (High for the audit's purpose) — `AUDIT C1 dirty` and `PREDICATE C1 pass` can be printed together, exit 0

`audit_clean` is computed at `:419-420` and printed at `:420`; the acceptance predicate at `:425-428` is built
from the *pre-run* `mism` and does not mention `final`, `nondet` or `audit_clean`:

```
419  audit_clean = not final and not nondet and not mism
420  print(f"AUDIT C1 {'clean' if audit_clean else 'dirty'}")
425  good = (not mism and len(PINS) == 26 and ... killed == TOTAL and survived == 0 ...)
428  return 0 if good else 1
```

A battery39 module that contributes no fixtures but appends one line to two pinned files in its build child
runs *after* `mism` is computed (`:279`) and before the final re-hash (`:416`):

```
PINS total=26 mismatched=0
BATTERY fixtures=90 wrong=0 renamed_disagree=0 sidechannel=0
MUTANTS total=7 killed=7 survived=0 invalid=0 null_detected=0
PINS final total=26 mismatched=2 first=plans/pkg_gate.py
AUDIT nondeterministic_kills=0
AUDIT C1 dirty
PREDICATE C1 pass
exit=0
```
(`run-P-pinwrite.txt`, module `zz_pinwrite.py`; the module is 12 lines and adds no fixture, so every other
number of the receipt is untouched.) After the run:

```
$ sha256sum plans/pkg_gate.py plans/round37_c1_attribution.py
bc2870f1...cffa6  plans/pkg_gate.py                     (pin ea638822…c541)
ffee63e3...01e9  plans/round37_c1_attribution.py        (pin 7064cf1a…b147)
```

The pin set is `plans/round39_c1_audit.py:76-104`; `ea638822…` is the gate digest the claims call "unedited".

**Impact.** The C1 kill rule is explicit — "a pin mismatch at landing → C1 not admitted"
(`plans/round-39-claims.md:60`). The audit's own repair A4 now *detects* that state and still prints the
frozen predicate's pass line and exits 0, so a reader who compares only the four predicate lines (the
documented comparison, `round39_c1_audit.py:13`) admits a landing whose gate is not the frozen gate. This is
wave-1 F2 narrowed to one line of code that was not written.

**Smallest remediation.** `good = (audit_clean and not final and not nondet and ...)` — three words — and
`AUDIT C1 clean` as the line the receipt is judged on.

---

## 3. S3 (Medium) — wave-1 F3 is open in the audit: a fixture-supplied `--rerun` still reaches P10's arbitrary code

The audit validates only `argv[0]` and that `--root`/`--spec` resolve inside the fixture dir
(`round39_c1_audit.py:318-325`). `--rerun` is not excluded, and `plans/pkg_gate.py:308` runs P10 whenever it is
present (`if (n != "P9" …) and (n != "P10" or args.rerun)`) — P10 executes `spec["probe_cmd"]`
(`pkg_gate.py:267-278`). A fixture may derive its own spec from a deep copy of `ctx.spec`
(`plans/round-39-claims.md`, module contract), so `probe_cmd` is attacker-chosen.

A 27-line module whose `build` copies `ctx.spec`, sets

```
probe_cmd = ["-c", "…open(sys.argv[1],'a').write('ran cwd=… home=…')…", "<marker>"], receipt = "rerun.out"
```

and returns `["package","--root",…,"--spec",…,"--rerun"]` is admitted by the audit:

```
FIXTURE sa-rerun-probe-exec expect=reject declared=P1,P2,P3,P4,P5,P6,P7,P8 observed_rc=1 observed_defects=P1,P2,P3,P4,P5,P6,P7,P8 ok
BATTERY fixtures=92 wrong=0 renamed_disagree=0 sidechannel=1
```
(`run-F3A5.txt`; declared set copied from a standalone gate run on the same tree, which prints
`P10 ok probe_rerun=byte-equal bytes=0`.) The marker shows the payload ran **three times inside the audit**
(reference pass, renamed pass, null pass), each time with the audit's own environment:

```
$ wc -l < "$S/rerun-marker.txt"
3
ran cwd=…/w/k39-c1a-spfdecbb/fx/battery39-zz_sa_rerun/f000/root home=/home/vgpnk
```
(`rerun-marker.txt`.) `P10` never appears as a DEFECT — the gate *accepted* the rerun, so nothing in the
receipt names the execution. (`sidechannel=1` here is the token heuristic firing on the word "environment" in
my module's docstring, and `PREDICATE C1 fail` follows from it — an illustration of §5, not of this finding.)

**Impact.** A battery module can execute arbitrary code with the operator's uid, environment, cwd and network
during the run that certifies the battery, without a single token in its source (`round39_c1_verify.py`'s scan
reads `/proc`, `ppid`, `cmdline`, `psutil`, `environ`; the payload here is JSON). A fixture's `P10 ok` also
stops meaning "the lane's probe reproduces".

**Smallest remediation.** Reject `--rerun` in a fixture argv (and whitelist the flags a fixture may pass:
`--root`, `--spec`, `--require-clean-tree`, `--file`, `--capture-dir`), or require a fixture spec to be
byte-identical to the frozen spec for a `package` argv. If P10 must stay reachable, run the probe under the
bwrap recipe too.

---

## 4. S4 (Medium, contract) — the A5 nonce is in the child's own argv, so the child still authors the fixture table

`--nonce` is passed on the child's command line (`round39_c1_audit.py:215-217`), the module is imported *in
that child* (`:187-196`), and the parent accepts the table if exactly one line starts with `BUILT <nonce> `
(`:218-220`). The nonce is therefore readable by the code it is meant to authenticate:

```
$ python3 plans/round39_c1_audit.py --build-module "$S/probe-child.py" --dest "$S/fgd3" --lane "$S/lane" --nonce deadbeefcafe0002
PROBE {"argv": [...,"--nonce","deadbeefcafe0002"], ...}
BUILT deadbeefcafe0002 []
```
(`child-capability.txt`.) A module that prints its own `BUILT <nonce> …` line and `os._exit(0)` before
`build_module_child` reaches its own `sys.stdout.write` gets that table graded:

```
FIXTURE sa-nonce-forged-row expect=reject declared=P1,P2,P3,P4,P5,P6,P7,P8 observed_rc=1 observed_defects=P1,P2,P3,P4,P5,P6,P7,P8 ok
BATTERY fixtures=92 …
```
(`run-F3A5.txt`; the row was produced by `plans/battery39/zz_sa_nonce.py`, which defines no `FIXTURES` at all
and computes its own declared set by running the gate once.)

**Impact.** The docstring's A5 sentence (`round39_c1_audit.py:12`, "the child's JSON line must carry a per-run
nonce") reads as a boundary and is a lint. What the child can gain is bounded — `dir` is overridden by the
parent (`:222`), and `expect`/`defects` are bound to the reference result (`:337-345`) — so this is not a false
pass by itself; it matters because it removes the last reason to trust the *shape* of the table, and it is the
loader that §1's attack rides on.

**Smallest remediation.** Send the nonce on the child's **stdin** (or in an environment variable) and require
the child to *close* stdout after the line; or drop the nonce and read the table only from a file the parent
names, with the child forbidden to write anywhere else.

---

## 5. S5 (High, capability — wave-1 F1/F4 still open) — the audit's children are as unsandboxed as the counter's

Both spawn sites still pass no `env=`, no namespace and no `start_new_session`
(`round39_c1_audit.py:215-217` for the build child, `:231` for every gate run), exactly the shape wave-1
F1/F4 reported for `round39_c1_verify.py:199-201/210-219`. Running the audit's own `--build-module` entry with
a probe module:

```
"home": "/home/vgpnk", "ssh_key_readable": true, "lane_git_head_readable": true,
"lane_file_writable": true, "env_keys": 268,
"env_agentish": ["DISPLAY", "SSH_AUTH_SOCK", "XDG_RUNTIME_DIR"], "net": "REACHED",
"grandchild_pid": 1391997
```
(`child-capability.txt`; the module wrote `$S/child-escape.txt` outside its `dest`, and the `SIDECHANNEL`
tokens it does not contain — `/proc`, `ppid`, `cmdline`, `psutil`, `environ` — are the only thing the counter
scans, `:115`.) After the child returned:

```
PID     PPID  SID     COMMAND
1391997 1535  1391997 /usr/bin/python3 -c import time; time.sleep(90)
```
— the grandchild outlives the child, the audit and (as wave-1 showed) every subsequent run. Killed by this
seat; `pgrep -af 'time.sleep(90)'` → `(none)`.

**Impact.** Every wave-1 statement about the counter's children holds for the audit that is supposed to repair
it: a battery module reads `~/.ssh/id_ed25519`, reads and writes the lane's `.git` and files, reaches the
network, and leaves processes behind. The audit's `sidechannel=0` is the same five-substring heuristic — in
this seat it fired on the word "environment" in a docstring (§3) and missed every capability above.

**Smallest remediation.** Same as wave-1 F1/F4, and now cheap because the audit is the file to change:
`env={"PATH":…, "HOME":<scratch>, "LANG":"C.UTF-8"}`, `start_new_session=True`, `os.killpg` on timeout, and —
for the build child — the existing bwrap recipe (`git_leak_probe.py:191-203`) with the lane read-only and
`--unshare-net`.

---

## 6. S6 (Low, operability — wave-1 F6 shape) — a missing `--work` parent is a traceback

`tempfile.mkdtemp(prefix="k39-c1a-", dir=a.work)` (`round39_c1_audit.py:293`) does not create `--work`:

```
$ python3 plans/round39_c1_audit.py --lane . --work "$S/nope"
  File "/usr/lib/python3.14/tempfile.py", line 381, in mkdtemp
FileNotFoundError: … '/fast/scratch/…/nope/k39-c1a-39lfcu1n'
exit=1
```
(`work-parent.txt`.) No `SETUP` line, no receipt. The same seat's wave-1 F6 found this in the C2 probe; the
audit copies it.

**Smallest remediation.** `pathlib.Path(a.work).mkdir(parents=True, exist_ok=True)` before `mkdtemp`, or
catch `OSError` and print `SETUP --work parent missing` with exit 2.

---

## 7. `plans/order_check.py` — four false passes, all cheap

The tool's contract is "Read-only by construction … the only commands issued are `rev-parse`, `log`,
`rev-list`, `ls-tree`, `cat-file` and `merge-base --is-ancestor`. It writes nothing, touches no network"
(`order_check.py:29-31`). What held: every git invocation is an argv list (no shell), every path argument is
preceded by `--`, refusals are `SetupError` → exit 2, and the lane path is resolved and confined by
`repo_path` (`:86-93`). What does not hold:

### O1 (High for this tool) — the repository it reads is taken from the environment

`Git.run` and `rc` (`:72`, `:81`), the `rev-parse --show-toplevel` probe (`:152`) and `cat-file` (`:132`) all
inherit the process environment. `GIT_DIR` therefore redirects the whole check to another repository, and the
tool prints a *pass* for the lane it was told to read:

```
$ GIT_DIR="$S/oc-decoy/.git" python3 plans/order_check.py --lane "$S/lane" \
    --claims plans/round-38-claims.md --receipt corpus/evidence/round38/build-pmars-probe.txt
ORDER freeze=afa799805ac3c5d7d5610372c5c3b76469afa347
ORDER scanned commits=1 file_entries=1 distinct_blobs=1
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
exit=0
```
(`oc-gitdir-decoy.txt`; the decoy is a two-commit repo with the same paths and a clean claims dir.) The same
command with a clean environment on the same lane and the same two paths:

```
ORDER HIT .ufo/waves/round-38/claims/control-c2-skip.txt@e0a378539a45:11 kind=gate-p10 `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt`
ORDER FAIL probe-executed-before-receipt hits=1
ORDER RESULT FAIL
exit=1
```
(`oc-gitdir-clean.txt`, reproduced from `measure-final.txt`.) The probe tool already models the fix
(`git_leak_probe.py:213`: `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null`); `order_check.py` sets
nothing and does not strip `GIT_DIR`/`GIT_WORK_TREE`/`GIT_OBJECT_DIRECTORY`/`GIT_INDEX_FILE`/`GIT_CONFIG_*`.

**Smallest remediation.** Pass `env=` to every git call with those variables removed (keep `PATH`), or fail
loudly when any `GIT_*` variable that changes repository selection is set.

### O2 (Medium) — a symlinked claims entry hides the evidence it points at

`scan_claims` collects every `ls-tree -r` entry whose type is `blob` (`:121-129`) and reads it with
`cat-file blob` (`:132`). A symlink is a `blob` whose content is the *target path*, so the evidence is never
read:

```
$ git -C "$S/oc-link" ls-tree -r HEAD~1 -- .ufo/waves/round-39/claims/
100644 blob b94412e8…  .ufo/waves/round-39/claims/note.md
120000 blob 4e035086…  .ufo/waves/round-39/claims/receipt.md
$ git -C "$S/oc-link" cat-file -p HEAD~1:.ufo/waves/round-39/claims/receipt.md
../../../../evidence/ran.txt
$ cat "$S/oc-link/evidence/ran.txt"
gate: P10 DEFECT fresh probe output is not byte-equal to the receipt
$ python3 plans/order_check.py --lane "$S/oc-link" …
ORDER scanned commits=2 file_entries=3 distinct_blobs=2
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
exit=0
```
(`oc-symlink-claims.txt`.) The plain-text control with the same line in a regular claims file is caught:
`ORDER HIT … kind=gate-p10`, `ORDER RESULT FAIL`, exit 1 (`oc-control-plain.txt`).

### O3 (Medium) — a UTF-16 claims blob is invisible to a line regex

`blob_hits` matches `^\s*(?:gate:\s*)?P10\s+…` line by line over `bytes.decode("utf-8", "replace")`
(`:132-136`, `:100-112`). UTF-16LE text decodes to NUL-separated characters and never matches:

```
$ python3 plans/order_check.py --lane "$S/oc-utf16" …
ORDER ok no claims file committed at or before the receipt shows the frozen probe executed
ORDER RESULT PASS
exit=0
```
(`oc-utf16-claims.txt`; the blob is the same sentence encoded `utf-16`.)

### O4 (Low) — a gitlink under `claims/` is skipped without a word

`if len(parts) != 3 or parts[1] != "blob": continue` (`:126`) drops `mode 160000 commit` entries:

```
$ git -C "$S/oc-gitlink" ls-tree -r HEAD -- .ufo/waves/round-39/claims/
160000 commit 242b3943…  .ufo/waves/round-39/claims/sub
ORDER scanned commits=2 file_entries=1 distinct_blobs=1
ORDER RESULT PASS
exit=0
```
(`oc-gitlink-claims.txt`.) Unlike O2/O3 this hides nothing at the tip (a submodule's content is another
repository), but the file-entry count silently changes and no line says so — the tool should count and report
"skipped non-blob entries".

**One remediation for O2–O4.** Decode as UTF-8, then also as UTF-16 when the byte stream contains NULs; follow
a `120000` entry by resolving its target *within the commit's tree* and scanning that blob; and print a
`ORDER SKIP <path> mode=<mode>` line, or fail, for any non-blob entry under `claims/`.

---

## 8. Wave-1 ledger — what the audit closes, what is still open

| Wave-1 | Status at `a6832f5` | Receipt |
|---|---|---|
| F1 child process unsandboxed (network, `~/.ssh`, lane `.git`, leftover processes) | **OPEN** — identical in the audit | §5, `child-capability.txt` |
| F2 pins hashed once | **PARTIAL** — `PINS final` exists, but the predicate ignores it | §2, `run-P-pinwrite.txt` |
| F3 fixture-supplied `--spec` + `--rerun` executes code | **OPEN** — `--rerun` not excluded | §3, `run-F3A5.txt`, `rerun-marker.txt` |
| F4 inherited environment, unreaped grandchildren | **OPEN** — 268 env keys incl. `SSH_AUTH_SOCK`; survivor | §5 |
| F5 C2 bwrap gaps (host `/etc`, no quota, no `--unshare-uts`) | **OPEN** — `plans/git_leak_probe.py` unchanged this round (`sha256 4961a50f…cf68c`, the pinned digest) | not re-tested; out of this seat's surface |
| F6 probe crashes on timeout / missing `--work` parent | **OPEN** (same shape in the audit) | §6, `work-parent.txt` |
| — (new this round) A1 replay | **CLOSED for static flips, OPEN for phase-keyed flips** | `run-A1static.txt` vs `run-A1phase-tip2.txt` |
| — A3 added battery37/38 file | **CLOSED** — refused before import | `A3-dropin.txt`: `PINS total=26 mismatched=1 first=plans/battery37/zz_drop.py`, stderr `AUDIT unpinned battery module present; refusing to import it`, `exit=2` |
| — A5 `dir` taken from the child | **CLOSED** for `dir` (`:222`), `--root`/`--spec` confinement (`:318-325`); the nonce half is not a boundary | §4 |
| — A2 duplicate `fid` | closed as in the frozen counter (`SETUP duplicate fixture id`, exit 2) | inherited code, not re-attacked |

## 9. What held (checked, not assumed)

* The audit's own A3 repair runs **before** any import: the refusal is printed and the run exits 2 with no
  fixture built (`A3-dropin.txt`), so an added `plans/battery37` file no longer executes in-process.
* Gate copies are still digest-checked after every mutant (`round39_c1_audit.py:404-410`); a mutated gate file
  cannot survive a mutant.
* `run_gate` catches `TimeoutExpired` and reports `("timeout", …)` (`:230-233`) instead of raising.
* `--root`/`--spec` confinement and the parent-supplied `dir` do prevent a fixture from grading an arbitrary
  tree — the wave-1 A5 `dir="/"` `copytree` hazard is gone (`:318-325`, `:222`).
* `order_check.py` issues only read-only git commands, uses argv lists and `--` separators, confines the lane
  path, and answers `ORDER ERROR … RESULTS ERROR` (exit 2) rather than a silent pass when it cannot run.

## 10. Limits

* Host: python 3.14, git 2.56.0, bwrap present; the uid/capability numbers are host-specific, the
  `subprocess` semantics are not.
* §1's attack needs the phase-detection race to be won; it was won on both runs that used the final module
  (`run-A1phase3.txt`, `run-A1phase-tip2.txt`). The two earlier attempts failed for two diagnosable reasons —
  a self-match on the daemon's own `/proc` cmdline, and a sibling daemon left by the previous run — both fixed
  by skipping the scanning process's pid and any process carrying the daemon signature (`run-A1phase.txt`,
  `run-A1phase2.txt` are kept as those attempts).
* No kernel/userns escape, no seccomp work; §5 is an observed-capability review, not a fuzzer.
* `dir="/"` and other destructive `copytree` variants were not run (read from `:328`, `:352`).
* Nothing installed or upgraded this seat; no pacman transaction attempted.

## Artifacts (`F39SentinelAudit/` beside this file)

Top level: `run-baseline.txt` (+`.err`), `run-ctl-empty.txt`, `run-P-pinwrite.txt`, `run-F3A5.txt`,
`rerun-marker.txt`, `run-A1static.txt`, `run-A1phase.txt`, `run-A1phase2.txt`, `run-A1phase3.txt`,
`run-A1phase-tip2.txt`. `receipts/`: `A3-dropin.txt`, `work-parent.txt`, `child-capability.txt`,
`oc-{control-plain,symlink,utf16,gitlink}.txt`, `oc-gitdir-{clean,decoy}.txt`. `modules/`: `zz_pinwrite.py`,
`zz_sa_rerun.py`, `zz_sa_nonce.py`, `aa_sa_phasekey.py`, `probe-child.py`. Each audit run is replayed by
dropping its module into `plans/battery39/` of a clean clone at the tip and running
`python3 plans/round39_c1_audit.py --lane . --work <scratch>`; `aa_sa_phasekey.py` also imports
`crit_a1_flip.py` from `.ufo/waves/round-39/build/R39CritC1Counter/` unchanged.

VERDICT: sentinel-10-open
