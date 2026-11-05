# ExecProbeR89 — probe reproducibility and containment

Scope: read-only at the lane; probe run with `--lane` pointing at the lane and `--work` under the seat scratch
`/fast/scratch/hyaku/kengaku-r89/ExecProbeR89/`. No production file, index, or git state was written. No
subagent was dispatched; no tool was installed or upgraded. Transcripts: `transcripts/` in this directory.

## State at run time (read-only)

Commands and verbatim output:

```
$ git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kengaku-shokunin
$ git -C .../kengaku-shokunin rev-parse HEAD
63d61d0f8db90016f5f4fafdadbcf3af87020004
$ git merge-base --is-ancestor a9b8a1a00b6a5ab5206be4d377dba439e02f8244 HEAD && echo "a9b8a1a ancestor of HEAD"
a9b8a1a ancestor of HEAD
$ git merge-base --is-ancestor d1c4f1b04bb39d18967075974b5984238b7c97f7 HEAD && echo "d1c4f1b ancestor of HEAD"
d1c4f1b ancestor of HEAD
$ git diff --stat HEAD -- plans/round89_polyglot_probe.py plans/round89_c1_replay.py plans/round89_claim_figures.py plans/round89-cases.json plans/round89-q66-records.json
(no output: all five instrument/frozen files identical to HEAD)
$ git diff --stat -- SKILL.md
 SKILL.md | 6 ++++++
 1 file changed, 6 insertions(+)
$ ls -l /usr/bin/bwrap
-rwxr-xr-x 1 root root 84464 Oct 14 19:06 /usr/bin/bwrap
$ sha256sum plans/round89_polyglot_probe.py
03c202f5072e8aa55636592fed9c2fb64b6a7684ec853f8968428e73d50df898  .../plans/round89_polyglot_probe.py
$ grep -n TRUSTED_TOOL_SHA plans/round89_c1_replay.py   (first hits)
46:TRUSTED_TOOL_SHA = "03c202f5072e8aa55636592fed9c2fb64b6a7684ec853f8968428e73d50df898"
```

Note: the lane HEAD is `63d61d0f` (round-89 wave-1 spec), a descendant of both `a9b8a1a` (measured tip) and
`d1c4f1b` (freeze). The lane carries one uncommitted change, `SKILL.md` (+6 lines), which is not this seat's
and was not touched. The probe's `WORKTREE` stamp reads `dirty` because of it (see Observations).

## 1. Three runs at the tip — OBSERVATIONS block

```
$ time python3 .../plans/round89_polyglot_probe.py --lane .../kengaku-shokunin --work "$S/run$i"   (i = 1, 2, 3)
run 1: real 0m0.685s  exit=0
run 2: real 0m0.680s  exit=0
run 3: real 0m0.694s  exit=0
$ sed -n '/^OBSERVATIONS_BEGIN$/,/^OBSERVATIONS_END$/p' run$i.out > obs$i.txt ; wc -l obs$i.txt
12 / 12 / 12
$ cmp obs1.txt obs2.txt && echo "cmp obs1 obs2: identical"
cmp obs1 obs2: identical
$ cmp obs1.txt obs3.txt && echo "cmp obs1 obs3: identical"
cmp obs1 obs3: identical
$ cmp obs2.txt obs3.txt && echo "cmp obs2 obs3: identical"
cmp obs2 obs3: identical
```

OBSERVATIONS block (identical in all runs, and in a fourth run; see step 2):

```
OBSERVATIONS_BEGIN
CASE exact predicted=P observed=P
CASE padded-output predicted=P observed=P
CASE extra-file predicted=F observed=F
CASE off-by-one-rust predicted=F observed=F
CASE cpp-exits-nonzero predicted=E observed=E
CASE rust-only predicted=F observed=F
CASE cpp-only predicted=F observed=F
CASE neither-compiles predicted=F observed=F
cases=8 legs=8 mismatches=0
PREDICATE R89-PROBE pass
OBSERVATIONS_END
```

Stamp-only differences between runs (expected: the `COMMAND` line carries the `--work` path):

```
$ diff run1.out run2.out
12c12
< COMMAND python3 plans/round89_polyglot_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r89/ExecProbeR89/run1
---
> COMMAND python3 plans/round89_polyglot_probe.py --lane . --work /fast/scratch/hyaku/kengaku-r89/ExecProbeR89/run2
```

(run 2 vs run 3 differs the same way.) `cmp` of the run-1 observation block against the committed receipt
`corpus/evidence/round89/polyglot-rust-c-probe.txt` observation block: identical.

Stamp differences from the committed receipt (informational): the receipt says `LANE_TIP d1c4f1b…` and
`WORKTREE clean`; runs here say `LANE_TIP 63d61d0f…` and `WORKTREE dirty` (SKILL.md). `TOOL_SHA`,
`SUBJECT_SHA` and `CASE_TABLE_SHA` are identical to the receipt (`03c202f5…`, `baed5e4d…`, `7dff1654…`).

## 2. `/app` and `/tmp` around one run (run 4)

```
$ ls -ld /app 2>&1                       (before)
ls: cannot access '/app': No such file or directory
$ ls /tmp | wc -l                        (before)
3922
$ python3 .../round89_polyglot_probe.py --lane .../kengaku-shokunin --work "$S/run4" ; echo "run4 exit=$?"
run4 exit=0
$ ls -ld /app 2>&1                       (after)
ls: cannot access '/app': No such file or directory
$ ls /tmp | wc -l                        (after)
3922
$ cmp <(obs of run4) obs1.txt && echo "run4 obs identical to run1"
run4 obs identical to run1
```

`/app` does not exist on the host and is not created. `/tmp` count is informational: it was 3917 before the first
probe batch and 3923 later, driven by other seats; the probe itself leaves no `case-*`/`capture-*` entry in `/tmp`
(`ls /tmp | grep -E '^(case-|capture-)' | wc -l` → `0`).

## 3. TMPDIR containment

```
$ ls -ld /nonexistent 2>&1
ls: cannot access '/nonexistent': No such file or directory
$ TMPDIR=/nonexistent/x python3 .../round89_polyglot_probe.py --lane .../kengaku-shokunin --work "$S/tmpdir-run"; echo exit=$?
exit=0
(stderr empty)
...
OBSERVATIONS_END
PREDICATE R89-PROBE pass            (identical OBSERVATIONS block to run 1)
$ ls -ld /nonexistent/x 2>&1
ls: cannot access '/nonexistent/x': No such file or directory
$ find "$S/tmpdir-run"
.../tmpdir-run          (empty after exit: TemporaryDirectory cleaned up)
```

Result: the probe does **not** fail at setup and does **not** consult TMPDIR: both `tempfile.TemporaryDirectory`
calls pass `dir=work` explicitly. Exit code 0.

Audit-hook confirmation (scratch wrapper `transcripts/audit_wrap.py`, `sys.addaudithook` in-process, same env
`TMPDIR=/nonexistent/x`, `--work $S/audit-run`):

```
$ TMPDIR=/nonexistent/x AUDIT_LOG=$S/audit.log python3 $S/audit_wrap.py .../round89_polyglot_probe.py --lane ... --work $S/audit-run
audit exit=0          (OBSERVATIONS identical to run 1)
322 audit events
$ grep -E "^(open \(.*'(w|a|x|r\+|w\+|a\+|wb|ab|xb)'|os\.(mkdir|rename|symlink))" audit.log | grep -v "$S/audit-run" | wc -l
0
$ grep -c -E '/tmp|/nonexistent|/home/vgpnk/\.' audit.log
0
```

Write-mode opens (18) and mkdir events (27) all fall under `$S/audit-run` (the `--work` tree). Read opens outside
system paths are exactly: `plans/round89_polyglot_probe.py`, `corpus/evidence/round52/graders/polyglot-rust-c/tests/test_outputs.py`,
`plans/round89-cases.json` (all lane reads). Subprocesses: 8 × `/usr/bin/bwrap` (one per case), `openssl version`
(env `PATH=/usr/bin` only), `git -C <lane> rev-parse HEAD`, `git -C <lane> status --porcelain --untracked-files=no`
(both inherit the environment). `.git/index` mtime is `2026-11-05 05:09:45.769319004 -0300` before and after the
probe batch: the probe's `git status` did not rewrite the lane index.

## 4. Containment grep (`_grep` over the three instruments, equivalent to `grep -n`)

Pattern `/tmp|HOME|environ|shell=True|os\.popen|curl|http`, files `plans/round89_polyglot_probe.py`,
`plans/round89_c1_replay.py`, `plans/round89_claim_figures.py`:

```
plans/round89_polyglot_probe.py:12   "No assertion is reimplemented and no `os.popen`, `subprocess` or `open` is patched..."   docstring prose, not code
plans/round89_polyglot_probe.py:259  parser.add_argument("--work", ..., help="scratch directory (never /tmp for large trees)")   help text, not a path read
plans/round89_c1_replay.py:23        "...L9 pins the probe, not the grader's execution environment."   matches "environ" inside "environment"; prose
plans/round89_claim_figures.py       no hits
```

Classification: no hit reads `HOME`, `os.environ`, `/tmp`, `shell=True`, `curl` or `http`. `os.popen` appears only in
the docstring (the grader's own call, executed inside the bubblewrap sandbox, is not in the instrument's code).
`subprocess.run` calls use argv lists with no shell; the only non-argv-list env is `{"PATH": "/usr/bin"}` for the
sandbox and `openssl`. The probe does not depend on `HOME` or `TMPDIR`.

## 5. Wall time

`time` of one run (run 1): `real 0m0.685s user 0m0.217s sys 0m0.159s`. Runs 2 and 3: real 0.680 s and 0.694 s.
The audit-hook run took 1.49 s wall (`Wall time` by the tool, including the wrapper's audit logging).
A host sanity compile (`rustc` hello-world, `real 0m0.031s`) is consistent with 16 compiles plus 8 bwrap launches fitting in
well under one second; the grader's `P` observations for `exact` and `padded-output` mean the compile and run did occur
inside the sandbox.

## Acceptance

- Observation blocks identical across the three runs: **met** (`cmp` returned identical for all three pairs; run 4 and the TMPDIR and audit runs also identical).
- Host `/app` untouched: **met** (absent before and after; never created).
- No `/tmp` path or `HOME` read in the instruments: **met** (see step 4; the three hits are prose/help text, classified above).

## Observations (not defects)

1. The lane is at HEAD `63d61d0f`, not the measured tip `a9b8a1a` or the freeze `d1c4f1b`; both are ancestors. The
   probe's observation block does not depend on HEAD, so the replay result is unaffected; the stamps differ as
   expected for a re-minted receipt.
2. The lane has an uncommitted `SKILL.md` edit (+6 lines). The probe stamps `WORKTREE dirty`, whereas the committed
   receipt says `clean`. The probe's `git status --untracked-files=no` makes this visible in the stamp only; it does not
   enter the observation block. The edit is not this seat's and was not touched.
3. The committed receipt's stamp is not what this lane state reproduces. The observation block is reproducible; the
   stamp is a function of lane state at run time.
4. The probe's `tempfile` calls pass `dir=` explicitly, so `TMPDIR` is inert: a containment property, not a defect.

## Frozen elements

None judged wrong in this item. Nothing edited.

## Installs

None. No tool was installed, upgraded or changed on the host. Scratch removed at the end of this seat.
