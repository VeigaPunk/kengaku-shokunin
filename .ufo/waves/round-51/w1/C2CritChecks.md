# C2CritChecks — independent re-run of 15 OPEN ledger checks

Seat: C2CritChecks (critic), kengaku round 51 (hyaku run 11), one v2 wave.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.

**Axes named.** Primary axis: **adjacency** (claim R51-C2 — a routed finding must name its owner
and its disposition, so a `fixed-verified` disposition must actually be verified). Sub-axes used to
walk the frontier cheaply: (a) *exit-code agreement* with `C2ExecOpenChecks`; (b) *determinism*
(same check, same convention, repeated); (c) *environment dependence* (check semantics under the
frozen counter's cwd vs the author's cwd); (d) *instrument robustness* (does the counter measure a
scratch candidate ledger at all). No other axis is claimed or touched.

**Revision measured.** `REV 4090c3db79d11279ab5e5121ba25e74aa316e6e7` (lane HEAD at wave time),
in a `git clone --shared` snapshot. The measured artifacts are byte-identical to the stage-1 freeze
`e07f131cf7037e58a21db6e1f3986cf401ad257c`:

```
$ git rev-parse e07f131:corpus/routed-findings.jsonl 4090c3d:corpus/routed-findings.jsonl \
               e07f131:plans/round51_routing.py     4090c3d:plans/round51_routing.py
2e819d7aa175137a43129edba932c3f853a51574
2e819d7aa175137a43129edba932c3f853a51574
043533d1a9599b8a9efda155812899d382384fbf
043533d1a9599b8a9efda155812899d382384fbf
$ git diff --stat e07f131 4090c3d -- plans/round51_routing.py corpus/routed-findings.jsonl
(empty)
```

## Method

Two execution conventions per check, three repetitions each, every run in its own fresh cwd and its
own `TMPDIR`:

- **Pass A — frozen-instrument semantics.** `cwd` = empty scratch dir, `LANE` = clone path,
  `TMPDIR` = scratch. This is what `plans/round51_routing.py` does (`subprocess.run(..., cwd=str(tmp))`,
  `plans/round51_routing.py:121-124`) and what `C2ExecOpenChecks` called pass A.
- **Pass B — author-intent semantics.** `cwd` = lane clone, same `TMPDIR`/`LANE`. This is the cwd
  every check text assumes (`plans/...`, `SKILL.md`, `corpus/...`, `.ufo/...` are all lane-relative).

15 checks chosen from the OPEN set (27 rows, 17 with a non-empty `check`), spread across the
classes present: python3 invocations, positive greps, negative greps, `test -f`, guard exit-code
and selftest-count idioms. Rows 50 (`R42-R3-32`) and 54 (`R42-R3-36`) were left out; the other 10
open rows have an empty `check` and are not runnable.

Chosen: `R39-R2, R39-R4, R42-R1, R42-R3, R42-R5, R42-R6, R42-R3-02, R42-R3-05, R42-R3-06,
R42-R3-07, R42-R3-08, R42-R3-18, R42-R3-19, R42-R3-26, R42-R3-27`.

## Commands (verbatim, abbreviated to the two fixed points)

```sh
S=/fast/scratch/hyaku/kengaku-r51/C2CritChecks; export TMPDIR=$S
git clone --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin $S/lane      # REV 4090c3d
cp -a $S/lane $S/lane2   # pass-B twin, so no pass can contaminate the other
python3 $S/run_critic.py   # 15 checks x {A,B} x {rep1,rep2}, bash -lc, 60 s, TMPDIR set
# pass A: cwd=<fresh empty dir>, LANE=$S/lane
# pass B: cwd=$S/lane2 (or $S/lane3 for rep 3), LANE=that clone
```

`git -C "$S/lane" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kengaku-r51/C2CritChecks/lane`;
`git -C "$S/lane2" status --porcelain` → empty before and after the runs (no check mutates its cwd).

## Result: exit codes

`mine_a` = A rep1/rep2, `mine_b` = B rep1/rep2 (rep 3, run in a deeper cwd and a third clone copy,
agreed with both in every row). `their_a`/`their_b` are the columns `C2ExecOpenChecks` measured
(`/fast/scratch/hyaku/kengaku-r51/C2ExecOpenChecks/results.json`, mtime `2026-10-28 15:20:22`,
sha256 `b38740b03fb4c6b8110487c151f73b68651ce4a67f2601030818fd3ddb67466a`; snapshot
`$S/sibling-results-snapshot.json`).

| row | mine_a | mine_b | their_a | their_b | disagreement |
|---|---|---|---|---|---|
| R39-R2 | 0/0 | 1/1 | 0 | 1 | none |
| R39-R4 | 2/2 | 2/2 | 2 | 2 | none |
| R42-R1 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R3 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R5 | 2/2 | 2/2 | 2 | 2 | none |
| R42-R6 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R3-02 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R3-05 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R3-06 | 2/2 | 1/1 | 2 | 1 | none |
| R42-R3-07 | 0/0 | 1/1 | 0 | 1 | none |
| R42-R3-08 | 0/0 | 1/1 | 0 | 1 | none |
| R42-R3-18 | 1/1 | 1/1 | 1 | 1 | none |
| R42-R3-19 | 1/1 | 1/1 | 1 | 1 | none |
| R42-R3-26 | 0/0 | 1/1 | 0 | 1 | none |
| R42-R3-27 | 2/2 | 1/1 | 2 | 1 | none |

**Exit-code disagreements: 0/15 on pass A, 0/15 on pass B.** Determinism: 15/15 identical across
three repetitions in each convention (a repeat in a deeper cwd and a third clone changed nothing).
So on the narrow question asked — are the reported exit codes reproducible — the reported table is
correct and the checks are deterministic in this environment.

## The disagreement that matters is semantic, not numeric

Four of the fifteen exit **0 under pass A for the wrong reason**: the check never reaches the lane,
so the idiom inverts. Verbatim pass-A stderr (empty `stderr` on the other two is because the command
redirects `2>&1` or writes nothing):

```
R39-R2     rc_a=0 err=''                                        # `[ "$rc" -eq 2 ]` matches python3's "can't open file"
R42-R3-07  rc_a=0 err='grep: SKILL.md: No such file or directory\n'      # `! grep -qF ...` inverts grep rc=2 into success
R42-R3-08  rc_a=0 err='grep: plans/pkg_gate.py: No such file or directory\n'
R42-R3-26  rc_a=0 err=''                                        # `[ "$rc" -eq 2 ]` matches python3's "can't open file"
```

The same four exit **1 in the lane cwd**, and for `R39-R2` the finding is demonstrably still live —
the probe still raises the traceback the ledger note describes:

```
$ cd $S/lane2 && d=$(mktemp -d -p "$TMPDIR") && python3 plans/git_leak_probe.py --lane . --work "$d/absent"
Traceback (most recent call last):
  File ".../lane2/plans/git_leak_probe.py", line 258, in main
    root = pathlib.Path(tempfile.mkdtemp(prefix="k39-glr-", dir=a.work))
FileNotFoundError: [Errno 2] No such file or directory: '.../tmp.BUgHmhAnFb/absent/k39-glr-es89n7__'
rc=1
```

So `C2ExecOpenChecks`'s pass-A column, read as "closable-now", would classify four still-open
findings as closable. Its pass-B column is the honest one.

## Counterexample against the C2 predicate

I built two candidate ledgers inside a lane copy (`$S/lane3`) and ran the frozen counter exactly as
frozen (`--run-checks`), marking rows `fixed-verified`:

```
$ python3 lane3/plans/round51_routing.py --lane lane3 --ledger $S/lane3/corpus/cand-all15.jsonl --run-checks
LEDGER corpus/cand-all15.jsonl rows=15
FIELDS complete=15 incomplete=0
OWNERS attributed=15 unattributed=0
DISPOSITIONS set=15 bad=0
SOURCES resolved=15 missing=0
CHECKS present=15 absent=0
VERIFIED ran=15 passed=4 failed=11
CLOSE_REFS resolved=0 missing=0
NEXT violations=0
  DETAIL CHECK_FAILED R39-R4 fixed-verified but check exits nonzero
  ... (10 more, the same 11 rows that fail in the lane cwd)
PREDICATE R51-C2 fail
exit=1
```

```
$ python3 lane3/plans/round51_routing.py --lane lane3 --ledger $S/lane3/corpus/cand-vacuous4.jsonl --run-checks
LEDGER corpus/cand-vacuous4.jsonl rows=4
...
VERIFIED ran=4 passed=4 failed=0
NEXT violations=0
PREDICATE R51-C2 pass
exit=0
```

The four rows in that passing ledger are `R39-R2, R42-R3-07, R42-R3-08, R42-R3-26` — every one of
them exits 1 in the lane cwd, and `R39-R2`'s underlying finding is still reproducible today. **The
frozen C2 predicate therefore prints `pass` over a ledger of four unverified findings.** The gap is
structural: the counter runs every `fixed-verified` check in a bare temp dir
(`plans/round51_routing.py:121-124`), so no check can resolve a lane path, and two idioms
(`[ "$rc" -eq 2 ]`, `! grep -q`) turn "target missing" into "verified". If the L1 marks any row
`fixed-verified` on the strength of the counter's own `--run-checks`, the adjacency claim is false
even though the predicate prints `pass`.

**Smallest safe correction.** Two moves, both inside the frozen claim text ("every `fixed-verified`
row's check exits 0 **in this run**"), neither touching rows or axes:

1. Run the checks where their text points: `cwd=str(lane)` with `TMPDIR` still scratch, in
   `plans/round51_routing.py:121-124` (`cwd=str(lane)` instead of `cwd=str(tmp)`). 11/15 of my sample
   flip under this change, all in the direction of author intent; the 4 vacuous passes disappear.
   If the counter must stay byte-frozen, the equivalent rule for attribution is: a row may be
   `fixed-verified` only if its check exits 0 in the **lane** cwd, and pass-B evidence per row is
   what the L1 records — the pass-A column alone is never sufficient for a negative grep or a
   `[ "$rc" -eq 2 ]` idiom.
2. `R39-R2` in particular cannot become `fixed-verified`: its check passes only because the target
   is missing. It stays open (or `routed` to whoever owns `plans/git_leak_probe.py`).

## Second defect: `--ledger` outside the lane crashes

The documented stage-2 workflow builds the merged ledger in scratch (`C2ExecLedgerMerge`), but the
counter cannot count it:

```
$ python3 lane/plans/round51_routing.py --lane lane --ledger cand-all15.jsonl --run-checks
Traceback (most recent call last):
  File ".../plans/round51_routing.py", line 77, in check
    print("LEDGER %s rows=%d" % (ledger.relative_to(lane), len(rows)))
ValueError: 'cand-all15.jsonl' is not in the subpath of '.../lane'
exit=1
```

Uncaught `ValueError`, no `PREDICATE` line, exit 1 — indistinguishable from a predicate failure to
any harness that only reads exit code and last line. Two-line fix:

```python
try:
    shown = ledger.relative_to(lane)
except ValueError:
    shown = ledger
print("LEDGER %s rows=%d" % (shown, len(rows)))
```

## Environment note (affects every seat reading the lane in place)

At 15:22:0x the lane's `corpus/routed-findings.jsonl` read back as 0 lines / 0 rows while
`stat` showed `size=48957 mtime=2026-10-28 15:22:02` — an in-place truncate-and-rewrite window. A
minute later the file again held 71 rows and `git diff --stat` against HEAD was empty (the rewrite
restored identical content; row ids unchanged). All my measurements therefore ran against the
immutable clone, never the lane worktree. Seats that read the lane ledger in place during that
window would have measured an empty ledger; `C2ExecOpenChecks` read it at 15:19-15:20, before the
window, and its 27-row set matches mine.

## Limits

- 15 of 17 runnable OPEN checks; `R42-R3-32` and `R42-R3-36` not run by me. CLOSED rows (41) are
  `C2ExecClosedChecks`'s item and were not touched.
- Endpoint/network-dependent behaviour not exercised; all 15 checks are local and none timed out.
- Pass B ran in a clone, not the live lane worktree; the two trees were byte-identical for every
  file these 15 checks read (`cmp` same for `plans/round42_c1_verify.py`, `plans/scratch_guard.py`,
  `plans/pkg_gate.py`, `plans/mutant_direction_check.py`, `SKILL.md`, `corpus/README.md`,
  `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`). `plans/sources_appendonly.py` exists in neither
  tree, which is why `R42-R3-18`/`R42-R3-19` fail in both conventions.
- `C2ExecOpenChecks` had not published its report file when this comparison was made; the comparison
  is against its measured table (path, mtime and sha256 above), not against its prose.
- Scratch `/fast/scratch/hyaku/kengaku-r51/C2CritChecks` was removed after this report was written;
  free space at setup: `804G total, 546G avail (33% used)` on `/fast`.

VERDICT: exit codes AGREE 15/15 on both conventions and are deterministic (3 reps); the reported
pass-A column is nevertheless unsafe evidence — 4/15 checks pass vacuously in the counter's cwd and
the frozen C2 predicate prints `pass` over exactly those 4 unverified findings (R39-R2 still
reproduces its traceback); plus `--ledger` outside the lane crashes with an uncaught ValueError.
Blocking for the C2 claim until the check cwd is the lane (or `fixed-verified` is gated on pass-B
evidence) and R39-R2 is not marked fixed.
