# SentinelR85 — security review of the round-85 instruments and evidence

Seat: SentinelR85 (leaf, read-only). Item: threat-model `plans/round85_sqlite_truncate_probe.py`,
`plans/round85_c1_replay.py`, `plans/round85_c2_debt.py` and the minted receipt
`corpus/evidence/round85/sqlite-db-truncate-probe.txt`.

Reviewed worktree at lane master **`def5d0ea5fbf49389400663d30c5a2c8820e56a5`** (lane was moving during the
review: I first read the instruments at `217910c5`, then `b1e57097`, `35b1e4e0`; every finding below was
re-verified against `def5d0ea`). Digests at the reviewed revision:

```
04d5fc1a78e6bab178005c44bd722bcce1bb5d234b8178aad3b7aed9933d3538  plans/round85_sqlite_truncate_probe.py
3f4945ba5b7774489f215623644ee28f6ce60ab6aa0bc6e233797db1d5748e2d  plans/round85_c1_replay.py
7622c250327cc5eaaa4bbbee6fde18034874fb914f5817acb43d5af9dc83ae5d  plans/round85_c2_debt.py
bd98794b9d35168ccb296ad9176cf45b0b421cf961515935a814eadc40d49114  plans/round85-cases.json      (= freeze)
c046535c44c01870d645984ad58faa4448f0f2408cccab425431779ea1ef6db2  plans/round85-defects.json    (= freeze)
23dcd425d37c2100…                                             plans/round-85-claims.md      (= freeze)
8f7f4d0251d71e307f8cdce9e9e7253b52603d9110f646155a4ae2bdba0e59d7  corpus/evidence/round85/sqlite-db-truncate-probe.txt
8f5bc11018687d8c5894ebf1b4ec6fad004828e5ce442d3cc04d925ef53ef881  corpus/evidence/round52/graders/sqlite-db-truncate/tests/test_outputs.py
```

Frozen inputs are byte-identical to `1a45aeb5` and BASE `0de45354` resolves: no frozen element was edited.
The committed receipt is a **regular 100644 blob** (`git ls-tree master`) whose bytes equal the working-copy file
and whose observation block I reproduced byte-for-byte. **The findings below are about the gate, not about a
forged receipt in this round.** Review code did not edit lane production files; fixtures were confined to
my scratch and small `/tmp/r85-sentinel` files, all removed before yield. No tool was installed.

Summary: replay observations reproduce; receipt confinement and mint provenance need remediation.
Four defects: S-1, S-2, S-4 and S-6. S-3 is a trust-boundary caveat and S-5 optional hardening, not counted
as defects. The eight cases reproduce with `mismatches=0` on the pinned capture.

---

## 1. Isolation

Every flag of the real argv (captured by importing the instrument and printing `sandbox_argv`; transcript in
`evidence/isolation.txt`):

| # | flag | effect |
|---|---|---|
| 1 | `--unshare-all` | new user, pid, net, ipc, uts namespaces (`--unshare-cgroup-try` too). Verified: `ns_net net:[4026533766]` vs host `[4026531833]`, `ns_pid [4026533764]` vs `[4026531836]`, `ns_user [4026533820]` vs `[4026531837]`, `ns_mnt [4026533760]` vs `[4026531832]` |
| 2 | `--die-with-parent` | sandbox dies with the probe |
| 3 | `--new-session` | new session, no controlling tty / no `TIOCSTI` injection |
| 4 | `--ro-bind /usr /usr` | host toolchain + CPython stdlib, read-only (`write /usr` → `EROFS`) |
| 5 | `--ro-bind /etc /etc` | **whole host /etc**, read-only (see S-5) |
| 6–9 | `--symlink usr/bin /bin`, `/sbin`, `usr/lib /lib`, `usr/lib /lib64` | Arch merged-`/usr` symlinks |
| 10 | `--proc /proc` | fresh procfs on the new pid ns — only pid 1 (bwrap) and pid 2 (python) visible |
| 11 | `--dev /dev` | minimal devtmpfs: `core fd full null ptmx pts random shm stderr stdin stdout tty urandom zero`; no `/dev/mem`, no `/dev/kmsg` |
| 12 | `--bind <work>/case-*/app /app` | the **per-case temp dir**, read-write by design; this is the only writable mount besides the tmpfs root |
| 13 | `--dir /tests` | empty dir on the writable tmpfs root, then |
| 14 | `--ro-bind <work>/capture-*/test_outputs.py /tests/test_outputs.py` | the grader, read-only (`write` → `EROFS`) |
| 15 | `--ro-bind <work>/case-*/harness.py /harness.py` | the harness, read-only (`write` → `EROFS`) |
| 16 | `--clearenv` | environment dropped |
| 17–19 | `--setenv PATH /usr/bin`, `LANG C.UTF-8`, `LC_ALL C.UTF-8` | the only variables set |
| 20 | `--chdir /app` | cwd is the case dir |
| 21 | `-- /usr/bin/python3 -I -B /harness.py` | isolated mode, no bytecode writes |

Measured reachability inside a case (my own reporting harness run under the instrument's *own* `sandbox_argv`):

* **host /app — unreachable and unchanged.** Host `/app` does not exist (`ls /app` → `No such file or
  directory` before and after a probe run). Inside, `/app` is the case temp dir (`read_app_recover` returns the
  staged `recover.json`), and no element of the argv names a host `/app` path. The probe's docstring claim
  "the host `/app` is never written" holds.
* **lane tree — unreachable.** `/home` and `/fast` are absent inside (`FileNotFoundError`), and reading
  `…/corpus/evidence/round85/sqlite-db-truncate-probe.txt` from inside the sandbox gives
  `FileNotFoundError`. The only lane bytes that cross are the capture (snapshot under `--work`, ro-bound at
  `/tests/test_outputs.py`) and the generated harness.
* **network — unreachable.** `socket.create_connection(("1.1.1.1", 80))` → `OSError: [Errno 101] Network is
  unreachable`; DNS → `gaierror: [Errno -3] Temporary failure in name resolution`; loopback →
  `ConnectionRefusedError` (an empty netns with no listener, not a host service). `/etc/resolv.conf` does not
  exist in the namespace.
* **environment — empty.** Inside: exactly `{"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": "/usr/bin"}` plus
  `PWD=/app` from `--chdir`. No `HOME`, no `PYTHONPATH`, no `PYTHONSTARTUP`; `python3 -I` also ignores them.
* **privileges — none.** `CapEff: 0000000000000000`, `CapBnd: 0000000000000000`, `NoNewPrivs: 1`,
  uid/gid 1000/1000, `Seccomp: 0`.
* **host identity — readable** (S-5): `/etc/machine-id` = `432d02b544a5459ebbff9c42ec68334d` (the host's),
  `/etc/hostname` = `plazir27`, `/etc/passwd` readable; `/etc/shadow` → `PermissionError` (DAC holds, the
  sandbox keeps uid 1000).
* **writable tmpfs root** (S-5): `/tests/new.py` and `/new.py` write successfully; only the two `--ro-bind`
  files reject writes. `/tmp` does not exist inside, `/dev/shm` exists and is empty.

**Writes outside `--work`.** A probe run against a *clean clone* (so no other seat's traffic confuses the
snapshot) wrote exactly one file outside `--work`: the clone's `.git/index`, rewritten by
`worktree_state()`'s `git status --porcelain` (stat-cache refresh). Content identical
(`9123ad8a…` before and after), mtime moved `1793822427.030` → `1793822435.277`. `find -newer` shows only
`<clone>/.git` otherwise. Nothing in the lane worktree, no host `/app`, no `/tmp` (S-6).

## 2. Confidentiality

* No instrument imports or invokes any network client (`urllib`, `requests`, `http`, `socket`, `curl`, `wget`
  are absent from all three files) and none reads `os.environ`, `getenv`, `expanduser`, `~/.ssh`, cookie or
  token state. The only environment reads are the *scrubbed* `env=` arguments and bwrap's `--clearenv`.
* Child processes: the sandboxed python, the sandboxed probe re-runs and the counters' tool invocations get
  `env={"PATH": "/usr/bin", …}` (C1 adds `TMPDIR`, C2 adds `HOME=<work>`). `git` and `tar` inherit the ambient
  environment but perform no network operation (`rev-parse`, `cat-file`, `archive`, `status`) and their stdout
  never reaches a receipt except the resolved commit id.
* The only output channel out of a case is the harness's single JSON line `{"score": int, "tests": [[name,
  "P|F|D", …]]}`; the pinned capture (`import json`, a literal `soln`, one function that opens
  `/app/recover.json`) does nothing else.
* Receipts leak exactly: the work path (`--work` argument in `COMMAND`), the lane tip, host Python and OpenSSL
  versions, the fixed member/subject/table/tool digests, and the eight case lines. No environment dump, no
  username, no hostname, no credential material. `host_openssl()` runs `openssl version` with
  `env={"PATH": "/usr/bin"}` only.

## 3. Integrity

The ledger row and the receipt are plain files inside the graded tree, so a candidate *can* write both; the
question is whether the counter can tell. The observation block is protected (below), the surrounding
evidence is not.

**S-1 (High) — receipt confinement is not enforced.** `Tree.bytes()` reads the receipt through the
filesystem: symlinks are followed and worktree bytes are trusted in the default (`--lane`, no `--rev`) mode.

```
# receipt committed as mode 120000 symlink to /tmp, scored at HEAD
$ git ls-tree HEAD corpus/evidence/round85/sqlite-db-truncate-probe.txt
120000 blob 73437944…   corpus/evidence/round85/sqlite-db-truncate-probe.txt
$ git cat-file -p HEAD:corpus/evidence/round85/sqlite-db-truncate-probe.txt
/tmp/r85-sentinel/current.txt
$ python3 plans/round85_c1_replay.py --lane . --rev HEAD --work …
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass

# same tree, receipt only in the working copy (untracked), --lane without --rev
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass
# … and the same bytes at HEAD:
DEFECT RECEIPT-MISSING corpus/evidence/round85/sqlite-db-truncate-probe.txt
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=1 defects=1
```

After deleting the `/tmp` file the identical tree went `RECEIPT-MISSING`: the "located receipt" the frozen
predicate requires can live entirely outside the repository and can evaporate. Impact: `located=1` — and the
`located`/`executed` figures the population gate quotes — do not imply a tracked artefact.
Smallest remediation: when `tree.tip` is a revision, require
`git cat-file -e <tip>:<RECEIPT>` **and** an `ls-tree` mode of `100644`/`100755` **and** blob bytes equal to
the parsed receipt. In worktree mode, require the same mode/content checks against an explicit committed
revision; tracking alone does not exclude a modified working-copy receipt.

**S-2 (High) — mint-time provenance is not independently verified.** The REPRODUCE leg computes `fresh_stamp`
and discards it; only `fresh_block != block` is compared. Some stamp fields are checked against constants
(`EXIT 0`, `WORKTREE clean`, tool and subject digests), but `WORKTREE clean` remains a textual assertion rather
than proof that minting occurred on a clean tree. `LANE_TIP` and host version strings are not reproduced.

```
$ git status --porcelain          # at scoring time
 M corpus/evidence/round85/sqlite-db-truncate-probe.txt
?? untracked-dirt.txt
$ sed -i 's/^WORKTREE .*/WORKTREE clean/' <the receipt, minted dirty>   # one-line edit
$ python3 plans/round85_c1_replay.py --lane . --work …
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass
```

Related, same root: `parse_receipt` builds a dict, so duplicate keys are last-wins — a receipt carrying
`EXIT 1` immediately followed by `EXIT 0` passes `stamp.get("EXIT") == "0"`.
Smallest remediation: compare the mint-independent fields between receipt and fresh stamp (`MEMBER`,
`SUBJECT_CAPTURE`, `SUBJECT_SHA`, `CASE_TABLE_SHA`, `TOOL`, `TOOL_SHA`, `HOST_PYTHON`, `HOST_OPENSSL`, `EXIT`);
reject any duplicate stamp key; keep `LANE_TIP`/`WORKTREE`/`COMMAND` as mint-time evidence and bind the tip via
S-1.

**S-3 (Medium) — the verdict is printed by code inside the graded tree, and nothing pins that code.** The C1
and C2 counters are themselves measured artefacts; the receipt pins only the probe's digest
(`TRUSTED_TOOL_SHA`). A two-line insertion into the in-tree counter reproduces the canonical verdict with no
receipt and an `unattempted` ledger:

```
$ python3 plans/round85_c1_replay.py --lane . --work …    # receipt deleted, ledger status=unattempted, patched copy
TARGET members=1 cases=8 legs=16 mismatches=0 located=1 executed=1 defects=0
PREDICATE R85-C1 pass
```

C2's `v3` makes this worse by construction: its "REPRODUCE is unconditional" leg is a *textual* test of the
tree's `round85_c1_replay.py` (`guard >= 1`, `"reproduce: bool = True" in source`, …) and it short-circuits the
behavioural leg entirely when the receipt is absent (`receipt-absent(no behavioural leg)` still returns the
code leg's value). Both legs run candidate-authored code (`tree.root/round85_c1_replay.py`), so they cannot
witness a modified counter. Mitigation is procedural, not a code fix: publish the two counters' sha256 in the
freeze/dispatch record and have the closing seat run a digest-verified copy; treat any in-tree counter result
as advisory until then.

**S-4 (Low) — a sandbox timeout is misclassified as a fail.** `run_case` uses `timeout=60` and `main()` catches
only `SetupDefect`, so `subprocess.TimeoutExpired` escapes as a traceback with exit 1 and no `PREDICATE` line
(frozen grammar: could-not-evaluate = 2). Demonstrated on a copy with `timeout=2` and a sleeping harness:

```
subprocess.TimeoutExpired: Command '['/usr/bin/bwrap', '--unshare-all', … '--chdir', '/app', …]
rc=1   PREDICATE lines=0   receipt written: no
```

It cannot mint a receipt, so no claim can be built on it; catch `subprocess.TimeoutExpired` in the probe's
existing setup-failure handler and emit the same SETUP lines with return code 2.

**S-5 (Low; optional hardening) — broader sandbox exposure than necessary.** Whole-host `/etc` is bound
read-only, exposing machine identity and readable account metadata. `/` and `/tests` permit new files, while
the actual grader and harness files correctly reject writes. Python `-I` excludes the script directory from
the import path; no import-shadowing vulnerability was demonstrated. No credential disclosure or usable
exfiltration channel was demonstrated with this pinned capture. Consider `--remount-ro /` after mount setup
and a minimal `/etc` view, retaining any runtime-required loader/NSS files.

**S-6 (Low) — one file outside the work dir changes.** `worktree_state()`'s `git status --porcelain` rewrites
the lane's `.git/index` (stat cache; bytes identical, mtime changes — see §1). Under concurrent seats this also
contends for `.git/index.lock`. Smallest fix: `git --no-optional-locks status --porcelain`.

## 4. Refusals (exact output)

```
$ python3 plans/round85_sqlite_truncate_probe.py --lane <fixture with one byte appended to the capture> --work …
DEFECT SETUP wrong-subject sha=787a653b625c74d2
PREDICATE R85-PROBE fail                       # exit 2

$ python3 plans/round85_sqlite_truncate_probe.py --lane <fixture without plans/round85-cases.json> --work …
DEFECT SETUP no-table /…/plans/round85-cases.json
PREDICATE R85-PROBE fail                       # exit 2

$ python3 plans/round85_c1_replay.py --lane <non-git fixture without the table> --work …
DEFECT SETUP frozen-input-missing plans/round85-cases.json (no git at /…)
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=0
PREDICATE R85-C1 fail                          # exit 2

$ python3 plans/round85_c1_replay.py --lane <git fixture whose history lacks FREEZE_REV> --work …
DEFECT SETUP frozen-input-missing plans/round85-cases.json@1a45aeb5e870
TARGET members=1 cases=0 legs=0 mismatches=0 located=0 executed=0 defects=0
PREDICATE R85-C1 fail                          # exit 2
```

The freeze-anchor branch is the real one (`frozen-input-missing …@1a45aeb5e870`), reached because the anchor is
read with `git cat-file -e <FREEZE_REV>:<path>`; the non-git branch is the fallback. Note the C1 `--selftest`
case `freeze-anchor-fails-closed` exercises only the fallback (it deletes the table from a non-git fixture), so
the anchor branch itself is covered by C2's `v2`, not by that selftest.

## What I verified as sound

* Observation block is genuinely tool-produced and load-bearing: `--control-forged-receipt` →
  `CONTROL forged-receipt target_reached=False defects=1 codes=REPRODUCE-MISMATCH`; with the REPRODUCE guard
  blanked the same fixture reaches `target_reached=True`. My own run of the probe against the lane (read-only,
  receipt into scratch) reproduced the committed block **byte for byte**; only the volatile stamp fields
  (`LANE_TIP`, `WORKTREE`, `COMMAND`) differed, as expected.
* `TOOL_SHA`/`SUBJECT_SHA`/`CASE_TABLE_SHA` pinning is effective: the probe re-reads the table and refuses a
  sha mismatch, and the counter binds both; a drifted table cannot mint.
* No shell interpolation anywhere (`subprocess.run` with list argv, `shlex.join` only for the displayed
  `COMMAND`; the `COMMAND` line is parsed, never executed).
* `git archive | tar -x` extraction cannot be steered outside the tree by a committed path (git trees are
  either blobs or trees, and GNU tar strips absolute members), though a committed *directory* symlink would be
  followed on read by `copytree` — a same-uid read, no privilege boundary.
* Frozen inputs are byte-identical to the freeze commit; BASE resolves; the current receipt is a tracked
  regular blob.

## Remediation priorities

1. **S-1** — require the receipt to be a tracked regular blob at the measured revision (kills both the
   worktree-only and `/tmp`-symlink paths). One `git ls-tree`/`cat-file` pair in `check()`.
2. **S-2** — compare the fresh stamp with the receipt stamp for the mint-independent fields; reject duplicate
   stamp keys. Clean-tree mint provenance additionally needs an independently witnessed mint step.
3. **S-3** — document the counter trust assumption and publish a closing-review digest. A rewritten
   counter is not a bypass of an independently trusted counter; this finding applies only when the
   candidate's own executable is treated as authoritative. Do not modify the frozen contract.
4. **S-4** — map `subprocess.TimeoutExpired` to `SetupDefect` in the probe (`exit 2`, no traceback).
5. **S-5** — optional sandbox hardening; not a demonstrated violation of the frozen mount contract.
6. **S-6** — `git --no-optional-locks status --porcelain` in `worktree_state()`.

None of these changes what the replay measured: `cases=8 legs=16 mismatches=0` on the pinned capture is real
(I reproduced it), and the eight-case table discriminates as the claim says.

## Commands run (all read-only on the lane; fixtures under my scratch)

```
du -sh kengaku-shokunin/.git; bwrap --version; python3 -VV; ls -la /app
git -C <lane> rev-parse master; git -C <lane> status --porcelain
sha256sum plans/round85_{sqlite_truncate_probe,c1_replay,c2_debt}.py plans/round85-{cases,defects}.json \
          corpus/evidence/round85/sqlite-db-truncate-probe.txt corpus/evidence/round52/…/test_outputs.py
git -C <lane> cat-file -p 1a45aeb5:<frozen input> | sha256sum        # freeze identity ×3
git -C <lane> ls-tree master corpus/evidence/round85/sqlite-db-truncate-probe.txt
python3 -I -B plans/round85_sqlite_truncate_probe.py --lane <lane> --work <scratch> --receipt <scratch>
python3 -I -B plans/round85_sqlite_truncate_probe.py --lane <fixture> --work <scratch>   # isolation/refusals
python3 -I -B plans/round85_c1_replay.py --lane <lane>  --work <scratch> --control-forged-receipt
python3 -I -B plans/round85_c1_replay.py --lane <fixture> [--rev HEAD] --work <scratch>  # S-1/S-2 demos
importlib + probe.sandbox_argv → bwrap with reporting harness        # isolation passes 1–3
find <clone>/.git -printf '%P %s %T@'  (before/after a probe run) + sha256sum <clone>/.git/index
git clone --no-hardlinks <lane> <scratch>; git -C <clone> rm --cached; ... -c user.name=… commit
git -C <clone> fetch/reset --hard origin/master   (fixture-only, toplevel verified)
```

Artifacts: `evidence/isolation.txt`, `evidence/refusals.txt`, `evidence/integrity.txt`,
`evidence/write-audit.txt`, `evidence/controls.txt`.

SEAT SentinelR85 VERDICT FINDINGS findings=4
