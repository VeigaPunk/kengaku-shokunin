# SentinelR88 — isolation and confidentiality review, round 88 evidence path

Scope: `plans/round88_fixgit_probe.py`, `plans/round88_c1_replay.py`, `plans/round88_claim_figures.py`,
`corpus/evidence/round88/fix-git-probe.txt`. Read-only against the lane; all forgery work in clones under
`/fast/scratch/hyaku/kengaku-r88/SentinelR88/` (cloned `--no-hardlinks`, toplevel asserted before each commit).
Evidence copies: `evidence/` in this directory.

Verdict: **FINDINGS**, 8 defects (2 High, 4 Medium, 2 Low). The round's measured figures reproduce at the tip;
the defects are in what the predicates can and cannot establish.

## 0. Tip figures reproduced (baseline)

| run | command (lane `L`) | result | evidence |
|---|---|---|---|
| C1 counter | `python3 L/plans/round88_c1_replay.py --lane L --rev 7fcc680b… --work S/c1` | rc 0, `TARGET executed_rows=32 member=fix-git located=1 executed=1 cases=8 legs=16 mismatches=0 defects=0`, `PREDICATE R88-C1 pass` | `c1.out` |
| C2 counter | `python3 L/plans/round88_claim_figures.py --lane L --rev 7fcc680b… --work S/c2` | rc 0, `MISMATCH KNOWN R87-C1 kv:defects claimed==7 defects claimed =7 measured 3`, `RECORDS … records=56 checked=56 matched=55 mismatches=1 prose=0`, `PREDICATE R88-C2 pass` | `c2.out` |
| C2 selftest | `… --selftest` | rc 0, five `SELFTEST … pass` lines, `PREDICATE R88-C2-SELFTEST pass` | `selftest-tip.out` |
| probe | `python3 L/plans/round88_fixgit_probe.py --lane L --work S/probe-work` | rc 0; observation block and stamp fields identical to the receipt except live-state fields | `probe.out` |

Lane writes by my runs: none. `git status --porcelain` differs from my pre-run snapshot only by
`M corpus/lessons/round-88.md` (mtime 02:43:42, inside the window of my concurrent C2 run). No counter path I read
writes that file; the diff is lesson prose from the L1. I did not write it and could not attribute it further.

## 1. Isolation (probe)

### 1.1 bwrap flags — exact `sandbox_argv` (`plans/round88_fixgit_probe.py`)

```
[BWRAP, "--unshare-all", "--die-with-parent", "--new-session",
 "--ro-bind", "/usr", "/usr", "--ro-bind", "/etc", "/etc"]
+ for link in (/bin,/sbin,/lib,/lib64) if islink: ["--symlink", readlink, link]
+ ["--proc", "/proc", "--dev", "/dev",
   "--bind", <case>/app, "/app", "--dir", "/tests",
   "--ro-bind", <staged capture>, "/tests/test_outputs.py",
   "--ro-bind", <case>/harness.py, "/harness.py",
   "--clearenv", "--setenv", "PATH", "/usr/bin",
   "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
   "--chdir", "/app", "/usr/bin/python3", "-I", "-B", "/harness.py"]
```
Host side: `subprocess.run(argv, timeout=60, env={"PATH": "/usr/bin"})`. bwrap 0.13.1 (`/usr/bin/bwrap`, root-owned).
`bwrap --help`: `--unshare-all  Unshare every namespace we support by default` (`evidence/bwrap-help.txt`).

### 1.2 What the grader reaches (observed, `evidence/isolation.txt`, run through the probe's own `sandbox_argv`)

- Reachable: `/usr`, `/etc` (read-only; `/etc/passwd` readable, `/etc/shadow` `PermissionError`; the host `/etc/ssh` has no private host key files), `/app` (= the case dir, read-write), `/tests` (an in-sandbox directory, writable; only
  `test_outputs.py` is the read-only bind), `/harness.py`.
- Not reachable: `/home`, `/root`, `/fast`, the lane path, host `/app` (`/app` in the sandbox is the case-dir bind).
- Environment: exactly `LANG LC_ALL PATH PWD`; uid 1000.
- Network: `OSError: [Errno 101] Network is unreachable`; interfaces `['lo']`.
- Writes: `/usr/probe-x` and `/etc/probe-x` `OSError`; `/app/probe-x` and `/tests/probe-x` written, the former
  lands in the host case dir only.
- Host `/app`: absent before and after (`ls -ld /app` → "No such file or directory", `app-before.txt`, `app-after.txt`).
  The bind is a mount-namespace operation; nothing was created on the host.

### 1.3 Can `stage()` write outside the case dir?

`stage()` has no guard of its own (`target = app / rel`; an absolute `rel` replaces `app`). Containment rests entirely
on `load_inputs`, which I quote:

```
if not isinstance(rel, str) or ".." in rel.split("/") or rel.startswith("/"):
    raise SetupDefect(f"wrong-table path {case_id}:{rel}")
```

Demonstrated: `stage(app, {"<abs>/abs-escape.txt": "x", "../dotdot-escape.txt": "x"})` writes both outside `app`.
Reachable today only because `replay()` always calls `load_inputs` first; the frozen table has four keys, all
plain relative paths (checked: no `""`, `"."`, `..` or absolute keys). Defence-in-depth gap, see F7.

### 1.4 Host `/app` written by a probe run — no.

## 2. Confidentiality

Grep over the three scripts and the receipt (`_grep` and `grep -n -E -i`):

- `HOME`, `token`, `secret`, `cookie`, `http`, `https?://`, `urllib`, `socket`, `curl`, `requests`: **no hits** in
  the three round-88 scripts or the receipt.
- `key` hits are dict/variable names only, e.g. `round88_c1_replay.py:110: key, value = line.split(" ", 1)`,
  `round88_claim_figures.py:224: for key, op, num in KV_RE.findall(span):`.
- Receipt contents: `MEMBER`, `SUBJECT_CAPTURE`, `SUBJECT_SHA`, `CASE_TABLE_SHA`, `TOOL`, `TOOL_SHA`,
  `HOST_PYTHON Python 3.14.8`, `HOST_OPENSSL OpenSSL 3.6.5 …`, `LANE_TIP`, `WORKTREE`, `COMMAND` (contains the work
  path `/fast/scratch/hyaku/kengaku-r88/L1/probe-work2`), `EXIT`, observations. Nothing beyond the work path, hashes
  and host version strings. Info only.
- Probe reads no env var and no file outside the lane's grader/table and `git` read-only commands. `host_openssl()`
  runs with `env={"PATH": "/usr/bin"}`.
- C1 L6 re-run env: `{"PATH": "/usr/bin", "TMPDIR": work}`. C2 counter env: `{"PATH": "/usr/bin", "TMPDIR": work}`.
  Both `git()` helpers inherit the caller's environment (no `env=`), so `GIT_*` and `~/.gitconfig` apply when the
  counter is run by a human. Code read; no network is reached by any git subcommand used.
- Historical counters run by C2 (grep at round-88 BASE `801b903a`; all 16 byte-identical to the worktree copies; none is present at its own claim BASE, see F5):
  no network imports or sockets. Hits are fixture/text literals (`round83_c2_debt.py:159`, `:203` with
  `https://example.invalid/…`), `os.environ` reads in `round80_c1_located_replay.py:389` (`FIXTURE_U` inside a fixture
  template string) and `round84_c2_admission.py:127` (env allow-list), a scrub of TOKEN/KEY/SECRET/PASSWORD names in
  `round82_c2_closure_debt.py:112`, and `HOME` set to the work dir in `round85_c2_debt.py:109`.
  `bash -lc` in `round80_c2_spotcheck_debt.py:127` and `round81_c2_spotcheck_debt.py:128`: under the instrument's env
  `bash -lc 'echo HOME=$HOME'` prints `HOME=` (`isolation.txt`), so no `~/.profile` is read. No credential is read by
  the new code.

## 3. Integrity

- **Staged content vs the eight cases.** Each case gets a fresh `TemporaryDirectory`, its own `app` bind, and its own
  harness. Staged content reaches the grader only as bytes read by `hash_file` (md5 of `strip()`), so it changes only
  the pass/fail of that case. The grader prints nothing, so content cannot corrupt the JSON protocol. No state is
  shared across cases (`/usr` and `/tests/test_outputs.py` are read-only).
- **Graded module import from the staged tree.** Not possible in the current argv. `-I` (isolated; implies `-P` on
  3.14) keeps the cwd `/app` off `sys.path`. Demonstrated: a staged `hashlib.py` containing `raise SystemExit` is not
  imported; `hashlib.__file__ == /usr/lib/python3.14/hashlib.py`, `cwd == /app`, `sys.flags.isolated == 1`.
  The grader itself imports only `hashlib` and touches only the four `/app/...` paths.
- **Capture TOCTOU.** `replay()` hashes the lane capture bytes and binds a copy written from those same bytes.
  The lane file is not re-read.
- **Harness.** `HARNESS` runs `runpy.run_path("/tests/test_outputs.py")` and calls each `test_` in source order,
  printing one JSON line. Result rows come only from the harness; grader output cannot forge them.

## 4. Fabrication surface (answer to Target 4)

An adversary who can write the lane tree controls every in-tree value the legs read. Experiments in clones (each
commit is in a scratch clone; the lane is never written):

| variant | what was forged | result |
|---|---|---|
| A | probe `observed = case["predicted"]` (grader never executed); receipt regenerated with the forged probe; commit | **C1 `PREDICATE R88-C1 pass`, executed=1, defects=0** (`A.c1.out`, `forged-probe.diff`, `forged-receipt-A.txt`) |
| B | receipt only: one `observed` flipped `F/P`→`P/P` | fails L5 and L6 (`B.c1.out`) |
| C1 | table predicted, probe `FROZEN_CASES`, counter `FROZEN` forged; receipt regenerated; `FREEZE_REV` unchanged | fails L4 only (`C1.c1.out`) |
| C2 | same as C1, then `FREEZE_REV` constant repointed to the forged commit | **passes** (`C2.c1.out`) |
| D1 | `round-87-claims.md` `defects=7`→`3` (both occurrences); no instrument change | fails `F5-missing-known` (`D1.out`) |
| D2 | D1 plus `KNOWN` emptied in the instrument | **`PREDICATE R88-C2 pass`, `matched=56 mismatches=0`** (`D2.out`) |
| D2-st | D2 tree, `--selftest` | **`PREDICATE R88-C2-SELFTEST fail`**, T1 fails (`D2st.out`) |
| E | uncommitted one-line edit to the round-87 counter's worktree bytes | `PREDICATE R88-C2 fail`, `F5-missing-known` (`E.out`) |

Which leg still refuses:

- L1 (receipt exists) refuses only a missing receipt.
- L2 (stamp) refuses stamp fields that disagree with bytes at rev, unless the forger recomputes them (A recomputes
  `TOOL_SHA`).
- L3 (`LANE_TIP` ancestor) refuses only a non-ancestor; any ancestor passes (A names the forged probe's parent).
- L4 (table = frozen) refuses an edited table only while `FREEZE_REV` is the hard-coded `0220c2f9…` (C1). The
  constant lives in the forgeable counter; repointing it passes (C2).
- L5 and L6 refuse receipt-only edits (B). They do not refuse a forged probe, because L6 re-runs the probe from the
  measured tree (A).
- L7 (ledger row) reads the ledger at rev; forgeable.
- L8 (grader sha) compares to the `SUBJECT_SHA` constant in the counter. Forgeable by the same route [INFERENCE from
  reading the line `elif sha256(capture) != SUBJECT_SHA:`; not run].
- C2: nothing anchors claims, counters, `BASES`, `CLAIMS`, `KNOWN` or the selftest to commit A. The instrument
  contains no reference to `0220c2f` or any freeze; the only "freeze" hit is a docstring comment (grep). The
  "edit to a frozen claims file" kill rule is not implemented.

The honest limit in the claims file (L6 "does not authenticate an author") understates this: L6 does not establish
that the grader ran. A forged probe passes every leg.

## 5. Findings

**F1 — High — C1 accepts a forged probe and receipt; the grader need not run.**
Evidence: variant A (`PREDICATE R88-C1 pass`, `executed=1`); `forged-probe.diff` shows the grader call removed.
Cause: L6 re-runs `tree/plans/round88_fixgit_probe.py` from the measured tree, unsandboxed, and compares the
observation block to the receipt's. Both come from the same forged file. L2 `TOOL_SHA` and L3 ancestry are
satisfied by construction.
Impact: a lane writer can mint a passing C1 with no grader execution. Round-88's `crypto-credential` movement rests
on this leg.
Route: L1/planner (predicate). In-lane mitigations: pin `TOOL_SHA`/probe blob to the frozen instrument commit
`1f267d4b` and require equality at rev; run the frozen probe from `1f267d4b` (not the measured tree) in L6. Neither
alone authenticates the output; an out-of-lane anchor (the round report's recorded blob ids) is needed for that.

**F2 — Medium — C1 anchors are constants inside forgeable files.**
`FREEZE_REV` (L4), `SUBJECT_SHA` (L8), `FROZEN` (L5, not compared to the frozen table's `predicted` fields), and the
probe's `FROZEN_CASES`. Evidence: variant C2 (repointed `FREEZE_REV` → pass).
Route: L1. In-lane fix: resolve the anchor from git objects at commit `0220c2f9` (the table blob and the capture
blob) and compare, instead of trusting a constant in the file under test. Still needs an out-of-lane record for the
commit ids.

**F3 — High — C2 has no freeze anchor; its kill rule is unimplemented; population is unpinned.**
Evidence: `grep -n -i -E 'freeze|0220c2f|1f267d4b|sha256|hashlib|commit A'` on `round88_claim_figures.py` returns one
docstring line only. D2 (two-file edit) → `PREDICATE R88-C2 pass`, `matched=56` where the claim text says
`matched=55`. The predicate never checks `records=56`; deleting records from a claims file passes once `KNOWN`
matches.
Impact: the instrument cannot detect edits to frozen claims or to its own known set, which is the purpose of the
check (Q66 counter-side figure derivation).
Route: L1. In-lane mitigation: compare the claims files at rev with their blob ids at commit A (and the instrument's
`BASES`/`CLAIMS`/`KNOWN` with a frozen table), and pin `records`. Ultimately needs an out-of-lane record.

**F4 — Medium — the emitted `PREDICATE R88-C2` line omits the selftest conjunct.**
The frozen predicate says "and the selftest battery exits 0". `run_check` never calls `selftest`; `main` runs one or
the other. Evidence: D2 prints `PREDICATE R88-C2 pass` while `--selftest` on the same tree prints
`PREDICATE R88-C2-SELFTEST fail` (`D2.out`, `D2st.out`).
Route: L1. In-lane fix: call `selftest` from `run_check` and emit `pass` only when both pass.

**F5 — Medium — C2 executes worktree bytes of each counter, and no counter exists at its claim's BASE.**
`run_rev` runs `[sys.executable, str(lane / counter)]` with `cwd=lane`, so the code is the worktree file, not the
bytes at any commit. A grep of the counters against their own BASEs shows all 16 are absent there
(`git cat-file -e <BASE>:<counter>` fails for every row; for example the round-87 counter was introduced in
`21da383b`, after `b9be6877`). Evidence: E (uncommitted edit → `PREDICATE R88-C2 fail`; the committed bytes pass).
The claim text's "re-runs that claim's own counter at that claim's own BASE" is accurate only for the data, not the
code.
Route: L1. In-lane fix: materialise each counter from a recorded commit (as `run_tree` already does for the three
round-82 counters) and record its blob id in the receipt.

**F6 — Medium — verifier code runs unsandboxed under the operator's account.**
Only the grader is in bwrap. The C1 L6 re-run executes `tree/plans/round88_fixgit_probe.py` with plain
`sys.executable -I -B` and no namespace; C2 executes worktree counters the same way. Variant A shows a lane-tree
probe executing inside C1. Impact: whoever can write the lane tree gets code execution at verification time, with
the operator's filesystem and network access.
Route: operator/out-of-lane. Not remediable inside the lane (the lane is the trust boundary). Option: run the
verifiers themselves under bwrap or in a separate account.

**F7 — Low — staging validation is in one place, and a plausible table key crashes with exit 1.**
`stage()` has no path guard (§1.3). `load_inputs` accepts `""` and `"."` keys; `stage()` then raises an uncaught
`IsADirectoryError` (traceback, empty stdout, exit 1). `{"a": …, "a/b": …}` raises `FileExistsError`. The exit code
(1) is the same as a mismatch. Demonstrated by a doctored lane (`doctor-lane`): rc 1, stdout 0 bytes,
`IsADirectoryError`. The frozen table is unaffected.
Route: L1. In-lane fix: reject empty/`.` components, catch `OSError` around staging and raise `SetupDefect`.

**F8 — Low — frozen text and instrument output differ (reported, not edited).**
(a) `round-88-claims.md` says the selftest prints "four `SELFTEST … pass` lines"; the instrument prints five
(T1 prints two checks), all pass at tip. (b) The claim quotes `MISMATCH KNOWN R87-C1 kv:defects claimed==7 measured 3`;
the output is `MISMATCH KNOWN R87-C1 kv:defects claimed==7 defects claimed =7 measured 3`. (c) "re-runs that claim's
own counter at that claim's own BASE" (see F5): no counter exists at its own BASE.

## 6. Not done / limits

- L8 forgery by constant: code-read only, not executed.
- The lesson-file modification (`corpus/lessons/round-88.md`, 02:43:42) is unexplained by my runs (see §0).
- I did not run other seats' checks, the ledger validator, or `sources-census.sh`.
- Tool installs or upgrades by this seat: none.
- The receipt's `WORKTREE` stamp is `dirty` when the probe is run in the live lane (untracked
  `.ufo/waves/round-88/w1/`), so it is not re-mintable there without a clean tree (Info).
