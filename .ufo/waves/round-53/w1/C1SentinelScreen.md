# C1SentinelScreen — adversarial security review, kengaku round 53 wave 1

Seat: `C1SentinelScreen` (sentinel). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Base tip `536925b5320fa64298030b4ee76a58fc4b82723f`; claims commit `a34838f`.
Scope (as assigned): (1) capture bytes + pin tree already committed under `corpus/evidence/round52`
and `round53`, and the archives wave-1 scouts will write under `.ufo/waves/round-53/w1/C1ScoutSrc*/fetched/`;
(2) the counters' use of `subprocess` and `git` — argv lists vs shell, paths from JSON that reach
`git -C` or `open`, and the `importlib` load of the seat-written classifier;
(3) the C2 counter executing 75 registry argvs from a committed ledger (`uv run` rows, env passthrough,
`git clone --shared` alternates). Plus a credential-shaped-string sweep.

All work was done read-only against the lane. No lane file outside my own seat directory was
created or modified. No `git`/`jj` mutating command was run in the lane or the fleet repo.

---

## 0. Executive summary

**The two frozen claims are not security-adversarially sound as instrumented.** I found and
*empirically demonstrated* (not merely reasoned about) **nine** defects: **three HIGH** (each one
defeats a stated leg of a frozen predicate, using only files the lane itself is allowed to write),
**four MEDIUM**, and **two LOW**. Two of the three HIGH findings are *re-execution* properties, not
just bookkeeping: a ledger or a freeze file can be edited so that the counter measures something
other than what it claims to measure.

Nothing here is a "the lane is malicious" accusation. Every finding is reachable by a *careless or
rushed* seat, which is precisely the failure mode a security review of a measurement instrument
should catch before wave 2 tries to falsify it.

The **good** news, stated plainly because it matters for judging this round:

- The **capture corpus is clean.** 183/183 captures match their pinned git blob SHA-1; the one
  operator-excluded file is genuinely absent; **zero** credential-shaped strings; no symlinks; no
  executable bits; no `op://`. The `PINS` leg is sound.
- The **credential sweep is clean** for the round-52/53 evidence and for the whole lane, with three
  *benign* `sk-`-prefixed false positives that are ordinary English/hyphenated words
  (`rare-high-risk-…`, `benchmark-task-…`, `disown-musk-…`) in round-28/29 evidence, not tokens.
- The **counters' subprocess discipline is good**: every `subprocess.run` uses an **argv list, never
  `shell=True`**, and no ledger-supplied string is ever interpolated into a shell command.
- **bwrap containment is feasible and I verified it works**: both counters' `--selftest` pass
  (22/22 and 12/12) under `bwrap --unshare-net` with a read-only lane and a writable scratch
  `TMPDIR`.

The problems are in **what the counters trust and how they re-execute**, not in shell hygiene.

---

## 1. HIGH severity

### H1 — C1: the freeze leg does not detect a joint edit of the classifier *and* the freeze file

**Where.** `plans/round53_c1_triage.py:124-140` (`leg_freeze`), specifically the pair
`:131` (`sha_ok = sha256_file(clf) == d.get("classifier_sha256")`) and `:132`/`:135`
(`first_add(...)` + `merge-base --is-ancestor`).

**The gap.** The counter pins the classifier's digest against a digest *stored in a file the lane
writes* (`plans/round53-c1-freeze.json`), and separately pins the *commit order* — the commit that
first added the freeze file must be an ancestor of the commit that first added the labels. But
`first_add` returns the commit that **first added** the freeze file; it says nothing about the
freeze file's **content at HEAD**. Edit the classifier and rewrite the freeze file's
`classifier_sha256` to match, in one later commit, and both sub-checks pass.

**Evidence (ran it).** A three-commit fixture: (1) classifier + freeze committed; (2) labels
committed; (3) classifier **and** freeze digest both edited. Result:

```
FREEZE classifier_sha=ok order=freeze-before-labels authors=1
leg_freeze ok = True
```

The claim text says the counter must show "the classifier is never edited after the freeze commit".
It does not: it shows the classifier's digest matches *whatever the freeze file currently says*.
The freeze file is not pinned by a digest constant in the counter (the only pinned constants are
`POP_SHA`, `PIN_TREE_SHA`, `TESTS_INDEX_SHA` — `plans/round53_c1_triage.py:29-31`), and
`plans/round53-c1-freeze.json` is not itself covered by any pin.

The counter's own selftest (`plans/round53_c1_triage.py:551-553`, case `classifier-edited-after-freeze`)
edits the classifier **without** touching the freeze file, so it passes — the selftest never
exercises the joint edit.

**Impact.** The exact anti-tuning property the round's novelty claim rests on ("labels read only
after the classifier was committed", "the classifier is never edited after the freeze commit; a
disagreement the oracle shows is a result, not a bug to repair") is **not enforced by the counter**.
A classifier that is tuned against the blind labels and re-frozen passes the FREEZE leg.

**Smallest mitigation (counter-side, but the counter is frozen — so this is an L1 decision).**
Either (a) pin `plans/round53-c1-freeze.json` by a digest constant in the counter alongside the other
three pins, so the freeze file's content is fixed at claims-freeze time; or (b) change the order leg
to compare the classifier blob **at the freeze commit** rather than at HEAD — i.e. read
`git show <freeze-commit>:plans/round53_c1_classify.py` and hash *that*, not the working-tree file.
Option (b) is strictly better: it makes the freeze meaningful even if the freeze file is rewritten.
Since the counter is frozen, (b) requires a dated amendment under PROTOCOL append-only; (a) can be
done by the L1 committing the freeze file's digest as a constant **before** any label seat is opened,
which does not change the counter at all. **Recommend (b) via amendment, (a) immediately as a stopgap.**

### H2 — C1: the counter `importlib`-executes a seat-written module *before* verifying its digest

**Where.** `plans/round53_c1_triage.py:67-72` (`load_mod` → `spec.loader.exec_module(m)` at `:71`),
called from `:165` (`v2_classes` → `plans/round53_c1_classify.py`) and `:181`
(`r52_classes` → `plans/round52_c1_grader_audit.py`).

**The gap — and this is the one the seat spec explicitly asked about.** The wave-1 classifier seat
`C1ExecClassifier` is writing `plans/round53_c1_classify.py` — a file that does not exist yet at
the base tip. The counter loads it with `importlib` and **executes its module top level** inside
the counter's own process. The digest check that decides whether that file is the frozen one lives
in a *different* leg (`leg_freeze`), and the driver's reachability condition
(`plans/round53_c1_triage.py:371`) is
`ok_pins and (lane/"plans/round53_c1_classify.py").is_file() and ... and info["authors"]` —
**`ok_fz` is not in that conjunction.** So the module is imported and executed even when
`FREEZE classifier_sha=BAD`.

**Evidence (ran it).** A fixture whose classifier's top level writes a marker file, with a freeze
file whose `classifier_sha256` is `"0"*64`:

```
leg_freeze ok = False | ['FREEZE classifier_sha=BAD order=UNPROVEN authors=1']
classifier module EXECUTED despite FREEZE digest mismatch: True
```

**What the seat-written module can do.** Everything the counter process can do: write any file the
user can write (including inside the lane), spawn processes, read the environment (which carries
`OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN`, `SSH_AUTH_SOCK` — see M3), and
reach the network. The classifier is also `importlib`-loaded **by name** into `sys.modules`
(`:70`), so it can shadow a stdlib name for the rest of the counter's run.

**The control leg is affected too.** The ORACLE-CONTROL leg's `r52_classifier_disagree` is computed
by importing `plans/round52_c1_grader_audit.py` — **the same lane-authored file the round-52 claim
is built on, unpinned by any digest constant** (grep confirms no `SHA` constant covers it). I
verified by fixture that editing that module's `classify_tests` changes the control's verdict
(`control_ok=NO(leg vacuous)` vs `control_ok=yes`). The control leg is supposed to be the thing
that *proves the leg is not vacuous*, and its input is a mutable lane file.

**Impact.** The counter's central trust model — "every input the predicate trusts is pinned by a
digest constant or by git history" (the counter's own docstring, and the round-52 closure defect
this claim is answering) — holds for three inputs and fails for two: the classifier and the
control.

**Smallest mitigation.** Two separable parts:
1. *Ordering (counter, 1 line).* Add `ok_fz` to the reachability conjunction at
   `plans/round53_c1_triage.py:371` so the module is not executed unless its digest matched the
   freeze. This is a strictly-safer ordering and, being a 1-line change, is a candidate for a dated
   amendment. Note this alone does **not** close H1 — the module could still be edited jointly with
   the freeze file.
2. *Containment (no counter change).* Run the counter under `bwrap --unshare-net` with the lane
   read-only (`--ro-bind / /`) and a writable scratch `TMPDIR`. I verified both selftests pass
   under exactly that sandbox. This is the containment the seat spec asked for, and it costs
   nothing in claim fidelity. Recommend the L1 make it the standard invocation for the counting
   command.

**Recommended invocation (verified working):**
```sh
bwrap --unshare-net --ro-bind / / --dev /dev \
      --bind /fast/scratch/hyaku/kengaku-r53/<seat>/st /tmp \
      --setenv TMPDIR /tmp --setenv HOME /tmp \
      --chdir <lane> /usr/bin/python3.14 plans/round53_c1_triage.py --lane .
```
Note `/usr/bin/python3` is a symlink to `python3.14`; under `--ro-bind / /` the symlink resolves
fine, but `bwrap` needs `/dev/null` — add `--dev /dev` (without it, `git init` inside the selftest
fails with `could not open '/dev/null'`).

### H3 — C2: the ledger's `argv` is executed as an arbitrary command; the `entry_mismatch` check
does not constrain it, so the counter can be made to "re-execute" something other than the row's
instrument

**Where.** `plans/round53_c2_tipstate.py:112` (`subprocess.run(argv, cwd=w.dir, ...)`) with `argv`
read straight from the committed ledger at `:104` (`argv = spec.get("argv")`); the static check at
`:139-141`:
```python
if (not isinstance(argv, list) or len(argv) < 2 or not all(isinstance(a, str) for a in argv)
        or script is None or script not in argv):
    res["entry_mismatch"].append(n)
```

**The gap.** The check requires only that the row's script path appear **as some element of the
argv list**. It does not require the argv to *be* that script. `["/bin/sh","-c","exit 0",
"plans/real.py"]` satisfies `script in argv` while never running `plans/real.py` at all.

**Evidence (ran it).** A one-row registry whose instrument genuinely exits **1** (RED), with a
ledger that declares it **green/0** and uses the decoy argv:

```
ROWS registry=1 ledger=1 missing=0 extra=0 entry_mismatch=0 bad_decl=0 bad_reason=0 duplicate_names=0
RUN executed=1 timeout=0 mismatched=0 evidence_missing=0
TIPSTATE declared_green=1 declared_red=0 observed_green=1 observed_red=0
PREDICATE R53-C2 pass        rc = 0
```

The honest ledger for the same instrument (`argv=["python3","plans/real.py"]`, declared red/1)
also passes — because the instrument really is red. **The forged ledger passes too, and the
counter cannot tell them apart.** The counter's own selftest has a case named
`forged-all-green` (`plans/round53_c2_tipstate.py:298-303`) — but that forgery changes the
*declaration* while keeping the *honest argv*, so it is caught by the mismatch check. **No selftest
case forges the argv.** That is the gap.

**Impact.** This is the C2 claim's core soundness property. The claim says the counter
"re-executes every argv in a scratch clone and observes exactly the declared exit code". The
counter does re-execute the argv and does compare the exit code — but the **argv is chosen by the
ledger**, and the ledger is the thing being measured. A ledger that runs `exit 0` instead of the
instrument is a *truthful-looking* ledger that the counter certifies. The round-52 lesson this
claim answers (`false-registry-cell`) is exactly this class of failure, one level up.

Note this is a *soundness* defect in the instrument, not a hostile-actor defect: a scribe who
"helpfully" writes `["bash","-c","python3 plans/x.py"]` to work around a placeholder, or who
copies an argv from the wrong row, produces the same result.

**Smallest mitigation.** Two candidate fixes, both tiny:
- *(counter, tightest).* Require the argv's **first** element to be a known interpreter and the
  **second** to be the row's script — i.e. `argv[1] == script` — instead of `script in argv`. This
  is exactly the check the claim's wording implies ("each entry's argv names the same script as its
  row's entry cell"). It rejects the decoy and still accepts `uv run --no-project --with
  biopython==1.85 python3 plans/tb2_grader_probe.py --lane .` only if the check is relaxed for
  `uv`-prefixed argvs — so the check should be "the script is the argv element immediately after
  the interpreter token", allowing an `uv run … python3 <script>` shape.
- *(no counter change, procedural).* The L1 can require that every ledger argv's non-flag
  arguments are exactly the registry cell's argv with placeholders substituted, and can verify
  this mechanically before accepting the ledger. This is weaker (it relies on a checker the lane
  writes) but touches no frozen counter.

Because the counter is frozen, both need L1 sign-off. **Recommend the counter-side tightening as a
dated amendment and the procedural check as the wave-1 stopgap.**

---

## 2. MEDIUM severity

### M1 — C2: `--source` is never compared to the lane's HEAD; a stale or wrong tree passes

**Where.** `plans/round53_c2_tipstate.py:199-202` — the source's rev is *printed* (`SOURCE rev=…`)
but never compared against the lane's HEAD, and `clean` is only "the source has no uncommitted
changes".

**Evidence (ran it).** Lane at commit `6040594…`, source at a **different** commit `959cfbb…`
containing a different instrument; the counter printed `SOURCE rev=959cfbb… clean=yes` and returned
**`PREDICATE R53-C2 pass`**.

**Impact.** The counting command is
`python3 plans/round53_c2_tipstate.py --lane . --source <clean shared clone of the landing tip>`. The
"<clean shared clone of the landing tip>" is a **prose requirement the counter does not check**. A
source clone one commit behind the tip — or of a completely different tree — is certified.

**Smallest mitigation (counter, 2 lines).** Compare
`git -C <source> rev-parse HEAD` to `git -C <lane> rev-parse HEAD` and fail on mismatch. This is a
soundness hole of exactly the kind the round's own pin philosophy targets.

### M2 — C2: a failed worker reset is silently ignored (`check=False`), so rows contaminate each other

**Where.** `plans/round53_c2_tipstate.py:97-100`:
```python
def reset(self):
    if self.git:
        subprocess.run(["git", "-C", str(self.dir), "reset", "-q", "--hard"], check=False)
        subprocess.run(["git", "-C", str(self.dir), "clean", "-q", "-fdx"], check=False)
```
Both use `check=False`, so a failed reset (stale `index.lock`, read-only worktree, full disk) is
indistinguishable from success.

**Evidence (ran it).** With `.git/index.lock` held, `git reset --hard` exits **128** ("File
exists") and the tracked file is *not* restored — while the counter proceeds. My two-row fixture
(a red row `a` that leaves an `index.lock` and mutates a tracked `gate.txt`, and a green row `b`
that reads it) shows row `b` observing the *contaminated* value: the isolation run gives
`MISMATCH b declared exit=0 observed exit=1`, and the poisoned run gives `observed_green=1` — i.e.
the row's observed exit flips because of the *previous* row.

**Impact.** With `--jobs 4` and one shared worker per job, a single row that leaves the tree dirty
(or merely trips a lock) changes the *observed exit* of a later row. The claim's kill rule is
"a single row whose observed exit differs from its declared exit … means fail" — so contamination
manufactures both false MISMATCHes (killing a truthful claim) and, via the decoy direction, false
matches. The `clean=yes` check covers only the source, not the worker.

**Smallest mitigation (counter, 2 lines).** Use `check=True` on both resets and treat a failed
reset as a hard error (or re-clone the worker). Additionally, `git clean -q -fdx` should be run
*before* the reset, or the worker should be re-cloned rather than reset.

### M3 — C2: the full parent environment is passed to all 75 rows, and row stdout is captured into
the ledger's `evidence` field — a credential exfiltration path into a committed file

**Where.** `plans/round53_c2_tipstate.py:109-112`:
```python
env = {**os.environ, "TMPDIR": str(tmp)}
p = subprocess.run(argv, cwd=w.dir, capture_output=True, text=True, timeout=t, env=env)
out = (p.stdout or "") + (p.stderr or "")
```
and the ledger schema's `evidence` is "a verbatim ≥6-character fragment of the observed output",
checked against `r["out"]` at `:255-257`.

**Evidence (ran it).** The host environment carries **9** secret-shaped variables:
`OPENAI_CODEX_TOKEN`, `XAI_OAUTH_TOKEN`, `OP_SERVICE_ACCOUNT_TOKEN`, `OPKEY_VAULT`,
`HL_INITIAL_WORKSPACE_TOKEN`, `SSH_AUTH_SOCK`, `STARSHIP_SESSION_KEY`, plus two `GUM_LOG_KEY_*`.
(I list names only; no values were read into any artifact.) A fixture row that prints
`*TOKEN*`/`*KEY*` environment variables has its stdout captured verbatim, and a ledger whose
`evidence` is a slice of that output **passes** (`PREDICATE R53-C2 pass`, `rc=0`).

**Impact.** The ledger is a **committed** file (`plans/round53-tipstate.json`). If any of the 75
row instruments — or a dependency it imports — prints its environment, a live secret can be
committed to the lane. This is the *same* failure mode that blocked the previous round's push
(a fake token inside a captured test fixture). The 6-character minimum for `evidence` means even a
short fragment of a secret qualifies.

**Smallest mitigation.** Two layers, either of which suffices:
- *(procedural, no counter change, cheapest).* Instruct the ledger scribe to never choose an
  `evidence` fragment that came from a line containing an environment dump, and add a pre-commit
  grep over `plans/round53-tipstate.json` for the credential patterns I list in §5. Since the
  ledger is lane-authored, this is a review rule the L1 can enforce at integration.
- *(counter).* Scrub the child environment (drop `*_TOKEN`, `*_KEY`, `*_SECRET`, `OP_*`,
  `SSH_AUTH_SOCK`) before `subprocess.run`, and/or redact the captured `out` before it is compared.

### M4 — C1: the CONFIRM leg's `report` path is unconstrained — an absolute path outside the repo
is accepted, and the "report names the task" check is a bare substring match

**Where.** `plans/round53_c1_triage.py:263` — `rep = lane / str(r.get("report", ""))`. Python's
`Path.__truediv__` with an **absolute** right-hand side **discards the left side**, so
`report = "/anywhere/ReaderSeat.md"` resolves outside the lane. There is no `.ufo/waves/round-53/`
prefix guard (the claim text says "a `report` path under `.ufo/waves/round-53/`", but the counter
never checks the prefix — `grep` finds no such guard). Line `:280` is
`r["task"] not in rep.read_text(...)` — a plain substring test.

**Evidence (ran it).** A fixture with `report` pointing at an absolute path outside the repo:
```
CONFIRM candidates_never_read=1 new_confirmed=1 rejected=0 target>=3
good = ['t1']
```
And separately, a report whose only mention of the task `t1` is inside the word **`t1st`**:
```
CONFIRM candidates_never_read=1 new_confirmed=1 rejected=0
good = ['t1']
```

**Impact.** The CONFIRM leg is meant to prove "a **never-read** task was confirmed by a reader
seat's report". Accepting an out-of-repo path (which could be any file on the host) and a substring
match inside an unrelated word both weaken it. The reader-name-in-path check (`:277`) is also a
substring test, so `report = "/tmp/ReaderSeat-x"` passes.

**Smallest mitigation (counter).** Require `rep` to be inside the lane and under
`.ufo/waves/round-53/`; require the task mention to be word-bounded (the counter already has a
correct word-bounded regex at `:231-233` — `seen_before` — which should be reused here).

### M5 — C1: the PRIOR-ART `fetched` path guard is a string-prefix test, so `..` escapes it

**Where.** `plans/round53_c1_triage.py:312-318`:
```python
f = lane / str(r.get(key, ""))
if not str(r.get(key, "")).startswith(f"{RUN_DIR}/fetched/") or not f.is_file():
    return None
```
The guard is a **string** prefix test on the *unresolved* path; the file is then opened at the
*resolved* path.

**Evidence (ran it).** A prior-art row whose `fetched` is
`corpus/evidence/round53/fetched/../../../../../OUTSIDE.txt` — passes the prefix guard, resolves
**outside the repository**, and is accepted:
```
PRIOR-ART rows=1 tasks_covered=1/1 known=1 new=0 urls=1 rejected=0
```
(An absolute path is rejected by the same guard, so `..` is the working escape.)

**Impact.** The PRIOR-ART leg's premise is "an archived fetch under `corpus/evidence/round53/fetched/`
whose sha256 matches, and a verbatim quote found in that archive". With `..`, the "archive" may be
any readable file on the host. Combined with the digest being self-declared in the same JSON, the
leg certifies an archive the lane never actually fetched.

**Smallest mitigation (counter).** Resolve the path and require
`Path(os.path.realpath(f)).is_relative_to(Path(os.path.realpath(lane / RUN_DIR / "fetched")))`;
i.e. replace the string-prefix test with a resolved-path containment test.

### M6 — C1: the never-read blocklist **fails open** when the base tip is unavailable

**Where.** `plans/round53_c1_triage.py:216-229` (`never_read_blocklist`) — every `git show` result
is guarded by `if rc == 0:` and a failure is **silently skipped**.

**Evidence (ran it).** With a lane whose git history lacks the base tip, `texts` is empty and
`seen_before('chess-best-move')` returns `[]` — i.e. **every** task looks never-read. I also
confirmed a `--depth 1` clone does not contain the base tag (`git rev-parse BASE` → "unknown
revision"), so a shallow clone of the landing tip silently produces an empty blocklist.

**Impact.** The CONFIRM leg's "never-read task" requirement is the leg that makes a confirmation
*new* rather than recycled from round 52. If the base tip cannot be read, every task passes the
never-read screen and the leg's distinctness is gone — silently, with no line in the output
saying so. The counter does print `never_read_blocklist` nowhere.

**Smallest mitigation (counter).** If `git show <BASE_TIP>:SCORECARD.md` fails, the CONFIRM leg
must fail (or the leg must be reported as not-evaluable), not proceed with an empty blocklist.
One line: `if not texts: return ..., "BASE_TIP unreadable"`. This is a **fail-open in a
soundness-critical leg** and is the finding I would fix first among the mediums.

---

## 3. LOW severity

### L1 — C2: `git clone --shared` alternates expose the source's object store to every worker

**Where.** `plans/round53_c2_tipstate.py:91` — `git clone -q --shared <source> <worker>`. Each
worker's `.git/objects/info/alternates` points at the source's object store.

**Evidence (ran it).** I probed the classic hazard — `git gc --prune=now` or `git repack -a -d`
inside the shared worker, which historically could prune the *source's* objects. On git **2.56.0**
the source was **not** damaged (`count-objects` unchanged, `fsck` clean, history and all branches
intact, dangling blob preserved) in every variant I tried: `gc --prune=now` in the worker, `repack
-a -d` in the worker, `prune --expire=now` in the worker, and `gc` in the source while a shared
clone existed. Modern git protects alternates from this.

**Assessment: LOW, and I could not make it land.** The residual risk is that `--shared` requires
the source to stay alive and unmoved for the whole run, so a source that is repacked *concurrently*
would break the workers. `--no-local` (or `--reference` with `--dissociate`) avoids the coupling
entirely at the cost of a slightly slower clone.

### L2 — C2: `subprocess.run(timeout=)` kills the direct child only

**Where.** `plans/round53_c2_tipstate.py:112`.

**Evidence (ran it).** A child that spawns a background grandchild and then sleeps: the timeout
fired at 3 s and I observed **0** surviving `sleep 300` processes afterwards — so on this host the
grandchild did not survive (the process group was cleaned up). The general property (only the
direct child is signalled) still holds; no orphan was observed here.

**Assessment: LOW, and the attack did not land.** Recommend the counter use `start_new_session=True`
plus `os.killpg` on timeout for defence in depth, but I have no evidence of an actual leak.

### L3 — C2: `executed == n_reg` compares against the *registry* count, but `names` is filtered, so
a row dropped by `entry_mismatch`/`bad_decl` can silently shrink the executed set

**Where.** `plans/round53_c2_tipstate.py:205-207` builds `names` excluding `entry_mismatch` and
`bad_decl` rows, while the predicate at `:268` requires `executed == n_reg`.

**Assessment: not exploitable as a forgery** — the count check then fails, which is the correct
outcome. Noted only because it means the "help-only" and "partial" selftest cases exercise the
same arithmetic. **No finding.**

---

## 4. Things I checked that are CLEAN (negative results, with the commands)

These are reported because a sentinel seat that finds nothing must say what it searched.

### 4.1 The capture corpus and the pin tree — clean

```
$ python3 - <<'EOF'   # leg_pins against the live lane
PINS population_sha=ok pin_tree_sha=ok tests_index_sha=ok captures_blob_match=183 blob_bad=0 absent=0 excluded_blob=ok files=184
leg_pins ok = True
EOF
```
183/183 captures match their pinned git blob SHA-1 (`blob_bad=0`, `absent=0`); the one
operator-excluded capture `sanitize-git-repo/tests/test_outputs.py` is genuinely absent and its
pin-tree blob `3269e74e…dacf199dda` matches (the reason is recorded in
`corpus/evidence/round52/graders/EXCLUDED.md`: a HuggingFace token pattern at line 12 of the public
upstream fixture; the bytes were excluded rather than bypassing push protection).

No symlinks and no executable bits anywhere under `corpus/evidence/round52` or `round53`:
```
$ find corpus/evidence/round52 corpus/evidence/round53 -type l -exec ls -la {} \;   # (no output)
$ find corpus/evidence/round52 corpus/evidence/round53 -type f -perm -u+x            # (no output)
```

`graders/SHA256SUMS` has 184 lines against 183 capture files — the extra line is the deliberately
absent excluded path, and `EXCLUDED.md` says so explicitly. Consistent, not a discrepancy.

### 4.2 Credential-shaped-string sweep — clean

Commands (run from the lane root; **matched bytes are never reproduced**):
```sh
grep -rInE '(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|op://[A-Za-z0-9/_-]{3,}|glpat-[A-Za-z0-9_-]{16,}|npm_[A-Za-z0-9]{30,}|-----BEGIN OPENSSH PRIVATE KEY-----)' corpus/evidence/round52 corpus/evidence/round53
```
Result over the round-52/53 evidence: **zero matches for every pattern.** The only textual hit in
the corpus was the literal string `PRIVATE KEY` inside an *assertion message* in
`corpus/evidence/round52/graders/openssl-selfsigned-cert/tests/test_outputs.py:93` — that is the
gradee's own prose, not key material. (Quoted at 8 words, within the 25-word limit.)

Swept the **whole lane** with the same patterns: the only hits are three `sk-`-prefixed strings in
`corpus/evidence/round28-calibration/` and `corpus/evidence/round29-attempt2/`, and masking the
tail shows they are ordinary hyphenated words (`rare-high-risk-…`, `benchmark-task-…`,
`disown-musk-…`) — **false positives, not tokens.** Round-28/29 evidence is also outside this
round's write scope, so it is left alone.

Also checked the specific pattern that forced the round-52 exclusion:
`grep -rInE 'hf_[A-Za-z0-9]{20,}' corpus/evidence/round52 corpus/evidence/round53` → **0 hits**,
so the wave-1 scouts' `fetched/` archives will not be re-triggering push protection *if* they avoid
that family. **Caution for the scouts:** the C1ScoutSrc seats are instructed to archive raw fetched
bytes under `.ufo/waves/round-53/w1/C1ScoutSrc*/fetched/`; those archives are untrusted web content
and are the most likely place a credential-shaped string could enter the repo. **Recommend the
L1 require a credential sweep of each `fetched/` directory *before* those bytes are copied into
`corpus/evidence/round53/fetched/`** — the corpus copy is what the counter reads and what lands in
git.

### 4.3 Subprocess hygiene — clean

Every `subprocess.run`/`Popen` call in both counters uses an **argv list**; there is no `shell=True`
anywhere in either counter, and no ledger- or JSON-supplied string is ever concatenated into a
command line. `grep -n 'shell=True' plans/round53_c1_triage.py plans/round53_c2_tipstate.py` → no
matches. (`shell=True` does appear in three *row* scripts — `plans/build_pmars_probe.py:312`,
`plans/feal_probe.py:221`, `plans/routed_open.py:148` — but those are the instruments under test,
with their own frozen literal command strings, not attacker-controlled.)

The C1 counter's `git()` helper (`:62-64`) uses `subprocess.run(["git","-C",str(lane),*a])` — argv
list, no shell. The `git -C` path is the **lane** path from the CLI, never a value from JSON. **No
JSON-to-`git -C` injection.**

### 4.4 bwrap containment — verified working

```
$ bwrap --unshare-net --ro-bind / / --dev /dev --bind <scratch>/st /tmp \
        --setenv TMPDIR /tmp --setenv HOME /tmp --chdir <lane> \
        /usr/bin/python3.14 plans/round53_c1_triage.py --selftest
SELFTEST cases=22 failures=0
$ ... plans/round53_c2_tipstate.py --selftest
SELFTEST cases=12 failures=0
```
Network isolation confirmed from inside the sandbox: a `urllib.request.urlopen("https://pypi.org/simple/")`
raises `URLError`. `--dev /dev` is required (otherwise `git init` in the C1 selftest fails on
`/dev/null`).

### 4.5 The `uv run` row — network-free given a warm cache

`tb2-grader-probe`'s registry cell is
`uv run --no-project --with biopython==1.85 python3 plans/tb2_grader_probe.py --lane .`, and
`biopython==1.85` is **already in the local uv cache**
(`~/.cache/uv/.../biopython-1.85.dist-info`). Under `bwrap --unshare-net` with a **writable** uv
cache bind-mounted and `UV_CACHE_DIR` pointed at it, `uv run --no-project --with biopython==1.85`
succeeds (`OK 1.85`) **without** `--offline`. With the cache read-only it fails on a lock file, so
the L1 must give the C2 run a **writable** uv cache (or set `UV_CACHE_DIR` to a writable copy).
Note the counter inherits `HOME` and the real uv cache path, so a plain run (no bwrap) is
already network-free for this row.

### 4.6 Network dependence of the 75 rows — mapped, one row needs the network at re-execution time

`catalog-probe`'s cell uses `--verify` (offline re-derivation from committed bytes). But
`plans/round51_surfaces.py:126` performs a **live** `urllib.request.urlopen(url, timeout=3)` for
`http`-kind manifest entries, and `plans/round51_surfaces.py` is the `round51-surfaces` row — the
very row the round's own before-state says "exits 1 (NUMBER-DRIFT SF14 row claims 171, probe says
SOURCES rows=186)". So that row's exit code can flip with network availability, and its `evidence`
fragment must therefore be chosen to be network-independent. **The L1 should tell the C2 scribe
explicitly that `round51-surfaces` is network-dependent and that its declared state must be
recorded from a run whose network status is stated.**

### 4.7 Rows that reach outside the clone — mapped

Two rows default `--fleet /home/vgpnk/Projects/shokunin` (`plans/round35_c1_verify.py:195`,
`plans/round36_c2_verify.py:212`), i.e. the **live fleet root**, not the clone under test. Their
fleet-census leg is additionally gated on `lane == (fleet/"kengaku-shokunin").resolve()`
(`round35_c1_verify.py:184`, `round36_c2_verify.py:201`), so **in a scratch clone that leg is
silently skipped** — the clone run and the live run are not the same measurement. I confirmed the
divergence: in a clone, `round35_c1_verify.py --lane .` reported 6 defects (V1–V6, all `DEFECT`);
in the live lane it reported 1 (V4 only). Same argv, different tree, materially different output.
**The L2's ledger argv for these two rows must either pin `--fleet` to a fleet copy consistent with
the clone, or accept that the row is measured against the live fleet — and then the declared exit
is not a property of the landing tip.** This is an operability finding for the scribe, and a
correctness hazard for the claim's "re-executed in a scratch clone" wording.

---

## 5. Recommended action list (smallest mitigations first)

Ordered by severity × ease.

| # | Sev | Finding | Where | Smallest mitigation | Counter frozen? |
|---|-----|---------|-------|---------------------|-----------------|
| H1 | HIGH | Joint classifier+freeze edit passes the FREEZE leg | `plans/round53_c1_triage.py:131-135` | hash the classifier **at the freeze commit** (`git show <freeze-commit>:…`), not at HEAD; or pin the freeze file by digest constant | needs amendment |
| H2 | HIGH | Seat-written module exec'd before its digest is checked; control module unpinned | `plans/round53_c1_triage.py:67-72,165,181,371` | (a) add `ok_fz` to the reachability conjunction at `:371`; (b) pin `plans/round52_c1_grader_audit.py` by digest; (c) **run the counter under `bwrap --unshare-net` with a read-only lane** | (a),(b) need amendment; (c) is free |
| H3 | HIGH | Ledger argv is an arbitrary command; `entry_mismatch` is a list-membership test | `plans/round53_c2_tipstate.py:139-141` vs `:104,112` | require the script to be the argv element **immediately after the interpreter**; add a selftest case forging the argv | needs amendment |
| M6 | MED | Never-read blocklist fails open when the base tip is unreadable | `plans/round53_c1_triage.py:216-229` | fail the CONFIRM leg when the base-tip texts are empty | needs amendment |
| M5 | MED | PRIOR-ART `fetched` path escapes the repo via `..` | `plans/round53_c1_triage.py:312-318` | resolved-path containment instead of string prefix | needs amendment |
| M4 | MED | CONFIRM `report` path unconstrained; task-name is a bare substring | `plans/round53_c1_triage.py:263,280` | require the report under `.ufo/waves/round-53/` in the lane; reuse the word-bounded regex at `:231` | needs amendment |
| M1 | MED | `--source` HEAD never compared to lane HEAD | `plans/round53_c2_tipstate.py:199-202` | compare both revs; fail on mismatch | needs amendment |
| M2 | MED | Failed worker reset silently ignored → cross-row contamination | `plans/round53_c2_tipstate.py:99-100` | `check=True`; re-clone on failure | needs amendment |
| M3 | MED | Full env passed to 75 rows; row stdout lands in a committed ledger | `plans/round53_c2_tipstate.py:109-112` | scrub the child env; **and** a pre-commit credential grep over `plans/round53-tipstate.json` | procedural (free) |
| L1 | LOW | `--shared` alternates couple workers to the source | `plans/round53_c2_tipstate.py:91` | `--no-local` / `--reference … --dissociate`; or accept (git 2.56 protected it in all my tests) | amendment |
| L2 | LOW | Timeout kills only the direct child | `plans/round53_c2_tipstate.py:112` | `start_new_session=True` + `killpg`; no orphan observed here | amendment |

**Two classes of mitigation are free and should be adopted regardless of any amendment:**
1. **Run both counters under `bwrap --unshare-net` with a read-only lane and a writable scratch
   `TMPDIR`** — verified working for both selftests (§4.4), and it is the containment the seat spec
   asked for. It bounds H2's blast radius to "can write to the scratch dir".
2. **A credential-pattern grep over every file the round lands** — the ledger
   (`plans/round53-tipstate.json`), the `fetched/` archives, and the wave-1 seat directories — using
   the pattern list in §4.2. §4.2 shows the existing corpus is clean, so this is a cheap regression
   guard on the new files, not a fix for an existing problem.

---

## 6. Files produced

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1SentinelScreen.md` —
  this report.
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-53/w1/C1SentinelScreen/` —
  created (empty) as this seat's deliverable directory.

No other file in the lane was created or modified. All fixtures and probes lived under
`/fast/scratch/hyaku/kengaku-r53/C1SentinelScreen/`, which has been **removed** (see §7).

---

## 7. Scratch discipline and tooling

- Scratch root: `/fast/scratch/hyaku/kengaku-r53/C1SentinelScreen/`. Free space at start:
  `461G` available on `/dev/nvme1n1p2` (`804G` total, `343G` used, `43%`). No ENOSPC encountered.
- **The scratch directory was removed before this report was finalised.**
- Every fixture repository was created with
  `D=$(mktemp -d -p /fast/scratch/hyaku/kengaku-r53/C1SentinelScreen) && git -C "$D" init -q`, and
  every later git call named `-C "$D"` explicitly. `git rev-parse --show-toplevel` was asserted to
  print the fixture directory before any mutation. **No commit, add, push, stash, checkout, reset,
  pull, or mutating `jj` command was run in the lane or the fleet repo.**
- The lane's own `git status --porcelain` shows only the expected untracked wave-53 artefacts
  (`.ufo/waves/round-53/controls.py`, `w1.ready`, `w1.ready.dispatched`, `w1/`) — none of them mine.

**Tools used (no installs were performed):** system `git 2.56.0`, `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5`,
`python3.14` (`/usr/bin/python3` → `python3.14`), `bubblewrap 0.13.1` (`/usr/bin/bwrap`),
`uv 0.13.0` (`/home/vgpnk/.local/bin/uv`). No tool was installed or upgraded during this seat, so
no tool/version/channel record beyond the above is owed.

**Note on the pacman guard:** no pacman transaction was attempted; the tooling directive's
"install via `uv tool` / official binary" channel was not needed.

**Blast-radius note.** `bwrap` is present and unprivileged-usable here, so the containment in §5 is
practical today. If it is unavailable on the L1's host, `unshare -n` alone would cover the network
half; the read-only-lane half would need a bind-mount or a `git worktree` copy.

---

## 8. One-line summary for the L1

> The capture corpus and the pin tree are clean and the `PINS` leg is sound, but **three HIGH
> defects let a lane-authored file change what the counters measure**: a joint classifier+freeze
> edit passes the FREEZE leg, the seat-written classifier is `importlib`-executed before its digest
> is checked (and the control module is unpinned), and the C2 ledger's `argv` — an arbitrary
> command — is only checked for *containing* the script name, so a forged argv that never runs the
> instrument is certified as `pass` (demonstrated). Containment via `bwrap --unshare-net` with a
> read-only lane is verified working for both selftests and should be the standard invocation even
> if the frozen counters are not amended.
