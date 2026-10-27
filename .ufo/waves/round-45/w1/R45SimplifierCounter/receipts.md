# R45SimplifierCounter receipts

Frozen lane file under review: `plans/round45_c1_verify.py`, sha256
`7745eb0a4bdf281acf46cde6e6a4c280a17d02f9668ea309d1020fff9ce1150d` (331 lines). Clone used for every run:
`/fast/scratch/hyaku/kengaku-r45/R45SimplifierCounter/lane`, `git -C ... rev-parse --show-toplevel` =
that dir, HEAD `05b02e2b7894a9c83219685f2374905e11c1beda`; the counter's own pin table re-checked on the
clone → `clone pins mismatched: 0 []`, 10 refusal modules, 22 honest modules. Nothing in the shared lane
was written: `sha256sum` of the lane file equals the clone's (above), lane mtime unchanged
`2026-10-26_23:00:38`.

Deliverable patch: `round45_c1_verify.simplify.patch`, sha256
`3396cbbae824b911cde1700d635e947e65dc5f81520512f476f629e0059a9324` (7 hunks, +32/−19 lines);
`git -C "$S/lane" apply --check --verbose` → `Checking patch plans/round45_c1_verify.py...` rc 0.
Proof harness `equiv.py` → `equiv.txt`, sha256 `a07745cf4fef839e90f07df26b07264b619cc7eec87b936b16d1704c5942c2c9`.

## 1. Static pass (AST)

```
IMPORTS: argparse, concurrent, hashlib, importlib, json, os, pathlib, re, shutil, subprocess, sys, tempfile
UNUSED IMPORTS: [('annotations', 46)]      # from __future__, not unused
`first`: stores at [197, 214, 221], loads at [214, 221] (both inside their own assignment RHS), return lines [230, 229, 189]
```

## 2. Expression-level equivalence (`equiv.py`, exit 0, `FAILURES: [] total 0`)

```
outside(): 729 path triples, mismatches=0
DONE_RE rc class: 477 tokens in the regex language, non-language samples=['?', '0x1', 'E', '-', '', '3 <unfinished ...>'], mismatches=0
count(): 1885 row multisets over 12 verdict/open kinds (len 0-3), mismatches=0
honest pool: old=['a', 'b', 'c'] new=['a', 'b', 'c'] equal=True
K44 pin guard: 5 mism lists, truthiness mismatches=0
`first`: stores at [197, 214, 221], loads at [214, 221] (both inside their own assignment RHS), return lines [230, 229, 189]
`first` in patched source: False
FAILURES: [] total 0
```

`count()` was compared against the four original comprehensions on every multiset of the 12
(verdict ∈ {ADMIT,BREACH,HUNG,ERROR} × opens ∈ {0,1,2}) kinds of length 0–3, returning exactly the six
`(n_admit, n_hung, n_open)` / `(h_adm, h_ref, h_read, h_hung)` tuples *and* the refusal verdict chain.

## 3. End-to-end runs (all inside `claims/envelope.sh`; `unchanged` every time)

Condition A — clone with `plans/fixture_fence.py` ABSENT (the frozen `control-c1-nothing` state, 117 fence runs):

| run | command | ENVELOPE end |
|---|---|---|
| orig | `python3 "$S/lane/plans/round45_c1_verify.py" --lane "$S/lane" --work "$S/work-orig" --jobs 6` | `ENVELOPE end 23:32:48 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` |
| patched (final bytes) | `... "$S/patched/round45_c1_verify.py" --lane "$S/lane" --work "$S/work-p4" --jobs 6` | `ENVELOPE end 23:36:35 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` |

```
297748129f21cf074e7c6122bd69f42a25ee82c62d57e96b85580f7085b9331a  control-body.txt   (frozen claims/control-c1-nothing.txt, PINS..PREDICATE)
297748129f21cf074e7c6122bd69f42a25ee82c62d57e96b85580f7085b9331a  A3-body.txt        (final patched bytes, same slice)
A3: FINAL PATCHED == FROZEN CONTROL control-c1-nothing.txt byte-identical
```

Condition B — clone with a synthetic fence that OPENS a directory under the build scratch but outside `d`
(the path the deleted `first` chain and the duplicated predicate touched; 117 fence runs):

```python
"""Synthetic fence (R45SimplifierCounter scratch clone ONLY): exercises the counter's outside-open path."""
import os


def breach(d, argv, tool):
    if "refusals45-" not in str(d):
        return None                      # honest fixture: admit, no open outside d
    fd = os.open(str(d.parents[1]), os.O_RDONLY)   # opens the build-scratch root/fx dir: under scratch, outside d
    os.close(fd)
    if any(t in str(d) for t in ("f1_gitfile", "f2_deep", "f4_fifo", "f9_nodescribe")):
        return "synthetic: outside open, then refuse"
    return None                          # one fixture admitted after an outside open
```
sha256 `27809b26efaba91367b4c77e81c7c317bd3dfafaeba3fb4944fce8fb705aa820`.

| run | ENVELOPE end |
|---|---|
| orig `--work "$S/work-orig-syn"` | `ENVELOPE end 23:33:47 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` |
| patched `--work "$S/work-patched-syn"` | `ENVELOPE end 23:33:56 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged` |
| orig (repeat, pre-mkdir bytes) | `ENVELOPE end 23:34:59 ... unchanged` |
| patched final bytes `--work "$S/work-p3"` | `ENVELOPE end 23:36:17 ... unchanged` |

```
4503c32c84bd761af67d8b0cdc5e0965be7d9188d8406a375f2d7829b5bed315  orig-syn-body.txt
4503c32c84bd761af67d8b0cdc5e0965be7d9188d8406a375f2d7829b5bed315  A2-patched-body.txt   (final bytes)
syn: ORIG == PATCHED byte-identical (READ+LEAKED+opens path)
REFUSAL f1_gitfile.py READ fixtures=1 admitted=0 hung=0 opens=1
...
REFUSALS total=10 clean=0 leaked=6 read=4 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
CALIBRATION advertised=10 contradicted=10
PREDICATE C1 fail
```

So both branches the patch touched (an outside open that refuses → `READ`, an outside open that admits →
`LEAKED`, and the honest `admitted opens=0` path) emit identical bytes and identical `opens=` counts.

## 4. The keep-log hook

Documented? **No.** The module docstring lists `--work` and `--jobs` only; `--help` has no flag for it. It
*is* relied on by a scheduled wave-2 seat: `make_wave2_spec.py:176-177` tells `R45LabratReadProof` to
"strace each under the counter's own harness (set K45_KEEP_STRACE to keep logs), cite the log lines".

Un-hardened, it kills the measurement (missing DIR):

```
K45_KEEP_STRACE="$S/keep-missing" ... python3 "$S/lane/plans/round45_c1_verify.py" --lane ... --work ... 
    shutil.copy(log, pathlib.Path(keep) / f'f{n:05d}.txt')
FileNotFoundError: [Errno 2] No such file or directory: '/fast/.../keep-missing/f00000.txt'
ENVELOPE end 23:35:15 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
```
(39 output lines: no `PINS`/`REFUSALS`/`PREDICATE` line at all, rc 1 — the wave-2 seat's `--jobs` run would
have died with a traceback instead of a receipt.)

With the patch's `mkdir`:

```
ENVELOPE end 23:35:24 exit=1 local_bin_content_before=c263b11afb1cccf6 after=c263b11afb1cccf6 unchanged
REFUSALS total=10 clean=0 leaked=6 read=4 hung=0 build_errors=0
HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0
PREDICATE C1 fail
117 files kept in keep-missing/ (f00000.txt, f00001.txt, f00002.txt, ...)
```
117 = 13 refusal fixtures + 104 honest fixtures = the 117 `FENCE-RUN` lines.
