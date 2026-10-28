# R50C1ExecCounterHygiene — scratch-hygiene audit of `plans/round50_c1_verify.py`

Seat: R50C1ExecCounterHygiene (executor, leaf) · round 50 (hyaku run 11) · wave `round-50/w1`
Serves: **R50-C1** (novelty). Item: audit the frozen C1 counter for scratch hygiene per the operator
directive of 2026-10-25. Nothing here claims or scores R50-C1; the predicate was run only as the subject
under observation.

## Axes named (before measuring)

| axis | question |
|---|---|
| A1 literal paths | does the tool carry a `/tmp` (or other absolute host) literal? |
| A2 `--work` contract | is `--work` honoured, is `tempfile.mkdtemp` created *under* it, is it removed, what happens when it is absent or missing? |
| A3 write containment | do any write syscalls land outside the work dir (traced, per-pid)? |
| A4 lane containment | does the tool write into the lane tree it measures (files, `.git`)? |
| A5 child isolation | do the harness/fixture children write anywhere (HOME, TMPDIR, inherited cwd)? |
| A6 runtime | per-leg wall time, and which leg dominates |
| A7 dead code | scratch-related code that reads as a guard but does nothing |

## Revision measured (REV)

- Freeze `3b02d573d58cc6d2e0d27ef92ac0815354912252` verified ancestor of the lane tip **before** any
  measurement: `git -C <lane> merge-base --is-ancestor 3b02d5… HEAD && echo ANCESTOR_OK` → `ANCESTOR_OK`
  at `d52243afab26962c4ba2f469bf7917a491ce3870` and again at `297e17927ba9342a87ba27a48cc5270a001de7cb`.
- Instrument under audit, byte-identical at every tip I measured:
  `plans/round50_c1_verify.py` sha256 `850ec7906e9658344b66e319a5c902ed4403519a55f33605b6f008ae90912999`
  (= the digest the claims file records for open-window repair 2). Fence under test at those tips:
  `plans/fixture_fence.py` sha256 `57adce4a598e1ca8a365114b35047f20afdce9459aa83adc0c551712966383a1`.
  Population pin `b5197f941a9f523eaedae6bd7be39531a0f80e10c6b05030687dbeacfb3fae69` (126 rows) matched in
  every run.
- All runs were against `git clone --shared` clones of the lane (`lane`, `lane2`, `lane3`, `lane5`,
  `lane6`, `lane7`, `lane8`) inside my scratch root. The live checkout was only ever read (`sha256sum`,
  `git rev-parse`, `find`).
- Tooling: no installs were needed or performed. `strace` 7.2, `python3` 3.14.8, `git` 2.56.0,
  host `linux 7.2.11-arch1-1`.

## Exact commands (abridged to the load-bearing ones)

```bash
S=/fast/scratch/hyaku/kengaku-r50/R50C1ExecCounterHygiene        # exported as TMPDIR for every run
git clone --shared <lane> "$S/lane3"                              # fresh clone per cold-cache measurement
grep -n "/tmp" "$S/lane5/plans/round50_c1_verify.py"               # A1
grep -n "/fast/\|/home/\|/tmp" "$S/lane5/plans/round50_c1_verify.py"
# A3/A4/A5: per-pid trace, one output file per process (no interleaving), dirfd-resolved paths
( cd "$S/canary" && strace -ff -ttt -y -qq -s 300 \
    -e trace=openat,mkdir,mkdirat,unlink,unlinkat,rmdir,rename,renameat,renameat2,chdir,fchdir \
    -o "$S/tr/t" python3 "$S/lane3/plans/round50_c1_verify.py" --lane "$S/lane3" --work "$S/w9" --skip-mutants )
find "$S/lane3" -newer "$S/marker4" -not -path "$S/lane3/.git/*"   # on-disk truth
# A2: work-dir contract
python3 … --work "$S/nope/deeper" --skip-mutants                   # missing parent
( cd "$S/canary" && python3 … --work relwork --skip-mutants )      # relative --work
TMPDIR="$S/tdir" python3 … --skip-mutants                          # no --work at all
# A6: line-timestamped plain run (per-leg wall time)
python3 "$S/linetime.py" "$S" "$S/lane5"                           # full run, prints +T per output line
# candidate repair (scratch only): sys.dont_write_bytecode = True  +  harness "-I" -> "-I", "-B"
GIT_OPTIONAL_LOCKS=0 python3 "$S/cand/round50_c1_verify.py" --lane "$S/lane8" --work "$S/w14" --skip-mutants
```

The trace analyser (`$S/parse2.py`, scratch-only) resolves each path against the call's dirfd
(`N<path>` / `AT_FDCWD<cwd>`) with `chdir`/`fchdir` tracking, classifies `WORK` / `LANE-TREE` / `LANE-GIT` /
`TMP` / `HOME` / `CANARY` / `OTHER`, and drops failed (`= -1`) and `<unfinished>` calls. A first pass that
resolved dirfd-relative paths against the *process* cwd produced 15,902 phantom writes; that pass is
discarded and not cited.

## Trace summary (verbatim numbers)

Fresh clone, one `--skip-mutants` run (cold `__pycache__`), traced as above:

```
WORKDIR .../w9/k50-c1-7m5v2hw9
span 35.57s  write-class syscalls 51847  relative 30844  out-of-work successful 212
leg honest            start=+  0.56s  window= 21.19s
leg harness           start=+ 21.75s  window=  5.54s
leg plans-refusals46  start=+ 27.29s  window=  2.25s
leg plans-sealed46    start=+ 29.54s  window=  0.72s
leg plans-sealed50    start=+ 30.26s  window=  5.31s
--- out-of-work successful writes   (top of the distribution)
    40  LANE-TREE    …/lane3/plans/refusals46/__pycache__
    40  LANE-TREE    …/lane3/plans/sealed50/__pycache__
    24  LANE-TREE    …/lane3/plans/sealed46/__pycache__
    20  LANE-TREE    …/lane3/plans/battery44/__pycache__
    …
     2  LANE-GIT     …/lane3/.git/index.lock
TOTAL 212
```

Breakdown of those 212: **12** `mkdir` of `__pycache__` dirs in the lane, **99** create+rename pairs for
`.pyc` files in the lane (= 198 syscalls), **2** on `<lane>/.git/index.lock`. **Zero** writes to `/tmp`,
`$HOME`, the inherited cwd (`$S/canary`, empty afterwards: `find $S/canary -mindepth 1 | wc -l` → `0`), or
anywhere else on the host. 2,245 per-pid trace files; no path resolved against an unknown cwd.

On-disk truth, fresh clone + one run (`find … -newer marker`):

```
99 .pyc files written, 578220 bytes, 12 __pycache__ dirs
…/lane3/.git/index mtime 2026-10-28 14:59:48.975  > marker 14:59:47.366   (index rewritten)
git -C lane3 status --porcelain | wc -l  →  0     (hidden: .gitignore carries "__pycache__/")
```

Unique pyc targets: 98 parent-side module caches (`plans/battery42|43|44`, `plans/honest50/modules/r46novel|
novel48|novel49|novel50`, `plans/honest50/build_honest_population.pyc`, `plans/round44_c1_verify.pyc`,
`plans/refusals46`, `plans/sealed46`, `plans/sealed50`) plus `plans/__pycache__/fixture_fence.pyc` written by
the harness child.

Full run (`--work`, no strace) leaves nothing outside the work dir either — only the same 99 pyc + 12 dirs.

## Runtime per leg (plain, no strace, warm `__pycache__`, full run, one output line per leg)

```
+   0.05s  REV / TREE / FENCE
+   1.87s  (+  1.82s)  POPULATION fixtures=126 … mismatched=0 build_errors=0
+   3.97s  (+  2.10s)  HONEST fixtures=126 admitted=126 refused=0 error=0
+   5.26s  (+  1.30s)  REFUSALS total=20 clean=20 leaked=0 build_errors=0
+   5.48s  (+  0.22s)  SEALED total=12 clean=12 leaked=0 build_errors=0
+   5.88s  (+  0.40s)  SEALED total=20 clean=20 leaked=0 build_errors=0
+  53.28s  (+ 47.40s)  MUTANTS total=15 caught=15 broken=0 floor=12 verdict=met
+  53.28s  (+  0.00s)  PREDICATE R50-C1 pass
EXIT 0 TOTAL 53.49s
```

Cold-clone totals for reference: `--skip-mutants` 8.69 s (6.57 s with the cache suppressed), full run
74.07 s (63.96 s under a size sampler). The **mutant leg is 88.6 % of the full run**; the four non-mutant
legs together cost 5.83 s. Peak work-dir footprint, sampled at 250 ms during the full run:
**7,835,012 bytes (7.5 MiB)**.

## Findings

### Passes

- **A1 — no `/tmp` literal.** `grep -n "/tmp"` → no match; `grep -n "/fast/\|/home/\|/tmp"` → `NONE`. The
  only temp mechanism is `tempfile.mkdtemp(prefix="k50-c1-", dir=a.work)` (line 209).
- **A2 — `--work` honoured, `mkdtemp` under it, cleaned.** Every run with `--work DIR` created exactly
  `DIR/k50-c1-<8>` and nothing else in `DIR`; `finally: shutil.rmtree(work)` (line 340) removed it and left
  the caller's directory in place: `w1 w2 w4 w5 w6 w7 w8 w9 w10 w11 w12 w13 w14` all had `0` entries
  afterwards. With `--work` omitted the work dir follows `TMPDIR` (`TMPDIR=$S/tdir` run passed, `tdir`
  left `0` entries) — no `/tmp` assumption. Peak footprint 7.5 MiB, well under the 50 MB `/tmp` rule.
- **A5 — children isolated.** The harness env pins `PATH`, `HOME=/nonexistent`, `LANG`/`LC_ALL=C.UTF-8`,
  `PYTHONHASHSEED=0`, runs `cwd=<fixture dir>` and `-I`; fixture builds write only inside their `gen` dir.
  Traced: zero writes to `$HOME`, `/tmp`, or the inherited cwd.
- **A3/A4 — nothing outside the work dir except the two items below.** Zero writes to any host path other
  than the lane tree.

### Defects

**D1 (medium) — the counter writes `.pyc` files into the lane it measures.** `load()` (lines 87–91) imports
lane modules in-process via `importlib` and the counter never sets `sys.dont_write_bytecode`, so a cold run
writes one cache per imported lane module: **99 `.pyc`, 578,220 bytes, 12 `__pycache__` dirs**, in
`plans/`, `plans/battery42|43|44`, `plans/honest50/…`, `plans/refusals46`, `plans/sealed46`,
`plans/sealed50`. This is a write outside the work dir and a write into the lane, contrary to the operator
directive; it is invisible to the counter's own `TREE dirty=` gate because the lane's `.gitignore` carries
`__pycache__/` (`git status --porcelain` → `0` after the run). It changes no verdict (all runs printed the
same predicate), and on a read-only tree the cache write fails silently inside `importlib`, so it degrades
into a best-effort write rather than an error. Witness: cold clone + one run → 99 pyc newer than the marker;
`-ff` trace → the 12 `mkdir` + 198 pyc syscalls above.

**D2 (low, dead guard) — `PYTHONDONTWRITEBYTECODE` in the harness env is nullified by `-I`.** `verdicts()`
sets `PYTHONDONTWRITEBYTECODE=1` in the child env (line 159–161) but launches
`sys.executable -I …` (line 166); isolated mode implies `-E`, which ignores every `PYTHON*` variable. So the
key reads as a guard and does nothing, and each harness child writes `plans/__pycache__/fixture_fence.pyc`
into the lane. Witness: with `PYTHONDONTWRITEBYTECODE=1` exported for the whole run, the parent's 98 caches
disappeared but exactly one remained — `plans/__pycache__/fixture_fence.cpython-314.pyc`.

**D3 (low) — the counter rewrites the measured tree's git index.** `git -C <lane> rev-parse` /
`git status --porcelain` (lines ~215–220) run without `GIT_OPTIONAL_LOCKS=0`, so git refreshes the index:
2 successful write syscalls on `<lane>/.git/index.lock` and the index is rewritten (mtime newer than the
marker after a run on a fresh clone; no `index.lock` left behind). Not a content change, but it is a write
into the lane, and it fails on a read-only checkout.

**D4 (low, contract) — `--work` must already exist; failure is a traceback with the wrong exit code.**
`--work $S/nope/deeper` and `--work relwork` both end in
`FileNotFoundError: [Errno 2] … '<path>/k50-c1-…'` with **exit 1**, while the docstring promises
`2 setup error`. A relative `--work` is not resolved against anything stable — it is used as given, so a
caller who does not `cd` aims it at its own cwd (the fleet root for this wave's harness).

**D5 (nit, dead code) — `verdicts()` computes a log path and never writes it.** `log = work / "harness" /
f"{i:05d}.err"` plus `log.parent.mkdir(parents=True, exist_ok=True)` (lines 163–164) creates
`work/harness/` and then never writes a file there; no `.err` file appears in any trace.

### Candidate repair (scratch-only, not applied to the lane)

```diff
--- a/plans/round50_c1_verify.py
+++ b/plans/round50_c1_verify.py
@@ -59,6 +59,8 @@ import sys
 import tempfile
 
+sys.dont_write_bytecode = True   # never write .pyc into the lane this counter measures
+
 FENCE_TIMEOUT = 120
@@ -163,7 +165,7 @@ def verdicts(...):
-            p = subprocess.run([sys.executable, "-I", str(harness), str(fence_path), str(f["dir"]),
+            p = subprocess.run([sys.executable, "-I", "-B", str(harness), str(fence_path), str(f["dir"]),
```

Measured on a fresh clone with `--skip-mutants`:
`RC=0`, output byte-identical (`HONEST fixtures=126 admitted=126 refused=0 error=0`,
`PREDICATE R50-C1 pass`), `0` `.pyc`, `0` `__pycache__` dirs, and the only remaining lane churn is `L/.git`.
With `GIT_OPTIONAL_LOCKS=0` additionally exported (which also closes D3 without a code change):
`index newer than marker? 0`, `anything newer outside .git? 0` — a fresh-clone run then leaves the measured
tree completely untouched. Two lines plus one env var, no predicate change.

## Limits

- Measurements are on `git clone --shared` clones of the lane, never on the live checkout; the live lane was
  read only (`find`, `sha256sum`, `git rev-parse`). The live lane currently carries **14 `__pycache__` dirs
  and 103 `.pyc` under `plans/`** (one dated 2026-10-28 15:02, `round51_surfaces.cpython-314.pyc`), which is
  the same class of write; I do not attribute all of it to this counter — other tools in the wave family
  import lane modules too.
- `strace` observes `openat/mkdir/mkdirat/unlink/unlinkat/rmdir/rename/renameat/renameat2/chdir/fchdir`
  only. `io_uring`, `mmap`-mediated writes, `write()` to an already-open fd outside the work dir, and writes
  by processes that escape the traced tree are not observed. Relative paths are resolved from dirfd
  annotations plus `chdir`/`fchdir` tracking; no path resolved against an unknown cwd in the cited run.
- The mutant leg was timed but not traced (23 rows in the carried battery became 15 in `plans/mutants50/`;
  `MUTANTS total=15 caught=15 broken=0` in every run). The on-disk marker check after a full run shows the
  mutant leg adds no lane write either (`patch` writes into `work/mutants`).
- Runtime figures are for this host (`linux 7.2.11-arch1-1`, NVMe scratch); the traced windows are
  strace-inflated (35.57 s traced vs 8.69 s plain for the same `--skip-mutants` leg) and are quoted only as
  shape, the per-leg table above being the plain-run numbers.
- Nothing here judges R50-C1: the predicate passed in every run, but admission is the L1's call.

## Scratch

Scratch root `/fast/scratch/hyaku/kengaku-r50/R50C1ExecCounterHygiene` (7 clones: `lane`, `lane2`,
`lane3`, `lane5`, `lane6`, `lane7`, `lane8`; 14 work dirs; traces `trace1–6`, `tr/` with 2,245 per-pid
files; analysers `parse.py`, `parse2.py`, `linetime.py`, `sampler.py`; `cand/` with the candidate repair).
Every work dir it created is empty and every run's `mkdtemp` child was removed by the tool itself. The
scratch tree was removed before this seat yielded.

VERDICT: **FAIL on the item's containment clauses** — no `/tmp` literal (pass), `--work` honoured and
`mkdtemp` created under it and cleaned (pass), but writes do leave the work dir: 99 `.pyc` / 578,220 bytes /
12 `__pycache__` dirs into the measured lane tree (D1, hidden by `.gitignore`) and 2 write syscalls on
`<lane>/.git/index.lock` (D3). Both are repairable in two lines plus `GIT_OPTIONAL_LOCKS=0`, with identical
predicate output measured on a fresh clone. Five defects listed (D1 medium, D2–D4 low, D5 nit); runtime per
leg: POPULATION 1.82 s, HONEST 2.10 s, REFUSALS 1.30 s, SEALED46 0.22 s, SEALED50 0.40 s, MUTANTS 47.40 s,
total 53.49 s, peak work footprint 7.5 MiB.
