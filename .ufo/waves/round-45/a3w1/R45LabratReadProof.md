# R45LabratReadProof — read-proof of the landed fixture fence (r45 a3w1, attempt-3 re-dispatch of wave 2)

Item: R45LabratReadProof (labrat/executor). Lane measured: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
`master` = `fbad1c56117ecaf458c94e6e0f5fb45ee5209ddc` (`git -C … rev-parse HEAD master` → both lines printed
`fbad1c56…`). All runs on a shared clone `$S/lane`; `git -C "$S/lane" rev-parse --show-toplevel` →
`/fast/scratch/hyaku/kengaku-r45/R45LabratReadProof/lane`. No lane file written.

Fence under test: `plans/fixture_fence.py` sha256 `ac65c03293084d7b25648740780b97e18f668e4fd9f08f947c09da72bce5eda6`
(counter line `FENCE plans/fixture_fence.py sha256=…`, `receipts/c1_run.txt:4`).

## 0. Envelope (QUALITY Q32)

Counter run (all 117 fixtures), `receipts/c1_run.txt:1-2,136`:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r45/R45LabratReadProof/env … -- /usr/bin/python3 …/lane/plans/round45_c1_verify.py --lane …/lane --work …/work --jobs 8
ENVELOPE start 00:22:53 cwd=/home/vgpnk/Projects/shokunin
ENVELOPE end 00:22:57 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Pathological probe, `receipts/patho_run.txt:1-2,13` and `receipts/patho_wide1m.txt:1-2,7` — same envelope, both
`exit=0 … before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`. No digest change, no invalid measurement.

## 1. Method (two independent measurements, same harness)

1. **Fidelity run.** The frozen counter itself, with `K45_KEEP_STRACE` set, so every per-fixture strace log the
   counter parses is kept byte-exact:
   `K45_KEEP_STRACE=$S/strace envelope.sh $S/env python3 $S/lane/plans/round45_c1_verify.py --lane $S/lane --work $S/work --jobs 8`
   → 117 logs `f00000.txt`…`f00116.txt` (13 refusal fixtures then 104 honest, `jobs` order). Result:
   `PINS total=33 mismatched=0`; `REFUSALS total=10 clean=10 leaked=0 read=0 hung=0 build_errors=0`;
   `HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0 build_errors=0`;
   `CALIBRATION advertised=10 contradicted=0`; `PREDICATE C1 pass` (receipts/c1_run.txt:3,132-135).
2. **Independent re-derivation.** `analyze_opens.py` / `scan_all.py` (in this subdir) re-implement the counter's
   open rule and widen it: `d` is taken from each log's decoded `AT_FDCWD<…>` (the harness cwd = the fixture dir),
   every successful `open/openat/openat2/creat` is resolved (dirfd if decoded, else cwd) and bucketed as
   `inside-d` / `SCRATCH-OUTSIDE` (<root>/fx,<root>/btmp outside d) / `root-other` (<root> but not scratch) /
   `system` / `elsewhere`. This removes the counter's dependence on its own `scratch` tuple for the classifier.

## 2. Claim decomposition (calibration)

The fence docstring scopes the claim to *the build scratch*: "the fence's whole process tree must never open a path
under the build scratch outside `d`" (`plans/fixture_fence.py:9-10`), and the counter encodes exactly that
(`plans/round45_c1_verify.py:203` `scratch = (root / "fx", root / "btmp")`). Read literally, "**zero opens outside
`d`**" is false on any run: a Python interpreter opening `/etc/ld.so.cache` is an open outside `d`. The measurable
statement, and the one I proved, is: **zero fixture-derived opens outside `d`, in particular zero opens of any
sibling fixture, sibling module dir, or file beside `d` under the build scratch, on all 117 fixtures**, plus the
pathological-tree bound. Absolute counts are reported below so the frontier wording can be made exact.

## 3. The four round-44 READ modules (f1, f4, f6, f10)

Log↔module mapping is not assumed: each log's own decoded paths name its module dir (`grep -o 'fx/[A-Za-z0-9_.-]*/f000'`
→ `fx/refusals45-f10_laneinclude/f000` for `f00000.txt`, etc.). Counter verdicts (`receipts/c1_run.txt:5-11`):

```
FENCE-RUN refusal refusals45/f10_laneinclude.py f10-lane-include-regular BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f1_gitfile.py f1-gitdir-outside BREACH opens=0 -- .git/.git is a file (gitdir redirect), not a directory
FENCE-RUN refusal refusals45/f4_fifo.py f4-fifo-include BREACH opens=0 -- lane/.git/config carries an include
FENCE-RUN refusal refusals45/f6_above.py f6-repo-above-d BREACH opens=0 -- .git exists at …/fx/refusals45-f6_above above the …
```

Independent classification of each kept log (`receipts/analyze_four.txt`; every count is successful opens only):

| module (log) | inside-d | root-other (harness) | system | SCRATCH-OUTSIDE | unresolved-rel |
|---|---|---|---|---|---|
| f10 `f00000.txt` | 11 | 3 | 101 | **0** | 0 |
| f1 `f00001.txt` | 1 | 3 | 101 | **0** | 0 |
| f4 `f00004.txt` | 4 | 3 | 101 | **0** | 0 |
| f6 `f00006.txt` | 0 | 3 | 101 | **0** | 0 |

Evidence by module (log lines quoted at `receipts/f0000*-*.txt`; sha256s in `receipts/SHA256SUMS`):

- **f10** — the only fixture file opened is inside `d`; the include target beside `d` is never opened:
  `openat(AT_FDCWD<…/f000>, "…/f000/lane/.git/config", O_RDONLY|O_CLOEXEC) = 3</…/f000/lane/.git/config>`
  (`receipts/f00000-f10.txt:123`). `grep -l 'inc10.cfg\|fifo.cfg\|/side/gitdir' $S/strace/*.txt | wc -l` → `0`: the f10
  include (`…/f000/../inc10.cfg`), the f4 FIFO (`…/f000/../fifo.cfg`) and the f1 separate git dir (`…/f000/../side/gitdir`)
  are absent from **all 117** logs.
- **f1** — refused at the walk (`.git` is a file) after opening only `d` itself; `grep -h '"\.git"' f00001-f1.txt`
  → no match (the `.git` file is judged from the walk's directory listing, never opened).
- **f4** — opens only `d`, `lane/`, `lane/.git/`, `lane/.git/config` (all inside `d`) and refuses on the include
  regex; the FIFO beside `d` is never opened (so no hang; counter `hung=0`).
- **f6** — `inside-d: 0`: it refuses in the collection pass from `os.path.lexists(d.parent/".git")` before any
  walk or git child, and no successful open anywhere under `…/fx/refusals45-f6_above` (the repo above `d`) exists
  in the log.

So: **read-proof for all four modules — 0 opens of any path outside `d` other than the 3 harness inputs and 101
interpreter-startup opens per run.** The three `root-other` opens are identical for every one of the 117 logs and
are the harness's own inputs, not the fence's: `root/harness.py` 234 (2 per run) and `root/fence/fixture_fence.py`
117 (1 per run) — verified aggregate: `root-other target names: {'harness.py': 234, 'fence/fixture_fence.py': 117}`.

## 4. Honest fixtures are admitted without reading their siblings

`HONEST fixtures=104 admitted=104 refused=0 read=0 hung=0` (`receipts/c1_run.txt`). Independent scan of all 117 logs
(`receipts/scan_all.txt`):

```
logs=117 with-d=117
inside-d: 3009 / root-other: 351 / system: 17585
scratch-outside offenders: 0
unresolved relative/dirfd opens: 0
'elsewhere' parents: (none printed → 0)
```

117 logs carry 117 distinct decoded cwds (`unique fixture cwds: 117`), i.e. each log is one fixture, and *no* log
opens a path under `<root>/fx` or `<root>/btmp` that is not its own `d` — no sibling fixture and no sibling module
dir is read on any of the 104 honest admissions (nor on the 13 refusals). Wider check of every successful open
destination's first path component across all logs:
`{'etc': 497, 'usr': 15266, 'proc': 234, 'dev': 1588, 'fast': 3360}` and
`paths outside the six system roots + /fast: 0`; `grep -h -E 'open…"(/home|/tmp|/root)…' $S/strace/*.txt | wc -l`
→ `0` (the lane clone is hidden and never touched).

## 5. Pathological tree vs ENTRY_CAP and FENCE_TIMEOUT

Probe `patho_probe.py` reuses the counter's harness text (`round45_c1_verify.HARNESS`), its exact strace argv and
the r44 counter's `ro_sandbox`/`hide_list`/`PY`; fixture runs have only the log dir writable, everything else
read-only, timeouts = `FENCE_TIMEOUT=120` as in `run_fence`. Constants printed by the probe:
`ENTRY_CAP=200000 REPO_CAP=64 CONFIG_CAP=1048576 GIT_TIMEOUT=30 FENCE_TIMEOUT=120`.

```
BUILD flat100k entries=100046 fill_seconds=0.8
PROBE flat100k fence_seconds=1.77 rc=0 hung=False opens=0 out='ADMIT'
BUILD flat199k entries=199046 fill_seconds=1.7
PROBE flat199k fence_seconds=3.31 rc=0 hung=False opens=0 out='ADMIT'
BUILD grouped201k entries=201247 fill_seconds=1.7
PROBE grouped201k fence_seconds=4.30 rc=0 hung=False opens=0 out='BREACH fixture tree exceeds 200000 entries'
BUILD wide1m entries=1000046 fill_seconds=11.6
PROBE wide1m fence_seconds=0.32 rc=0 hung=False opens=0 out='BREACH fixture tree exceeds 200000 entries'
```
(`receipts/patho_run.txt`, `receipts/patho_wide1m.txt`; logs `receipts/patho-flat100k-log.txt`,
`receipts/patho-grouped201k-log.txt`.)

Reading: a 100k-empty-file honest fixture (a real repo with claims/receipt blobs) is **admitted in 1.77 s**; the
largest admissible tree (199 046 of 200 000 entries) is admitted in **3.31 s**, a 36× margin under the 120 s
`FENCE_TIMEOUT`; 201 247 entries gets the designated refusal in 4.30 s; a 1 000 046-entry single directory is
refused in **0.32 s** because the cap is tested on the iteration's entry count before any per-file `lstat` — so the
worst single-directory shape is cheap, and the worst measured admissible walk is the flat 199k case. No HUNG, no
`opens>0`, nothing outside `d`.

## 6. Calibration findings for the L1 (no contradiction found, wording + scope limits)

1. **Wording.** `PREDICATE C1 pass`'s read leg is exact only as "zero opens under the build scratch outside `d`",
   which is what the counter counts and what I proved. Anywhere the round (lesson, SCORECARD, README, PROVINCE)
   says or implies "the fence opens nothing outside `d`" unqualified, it is false: measured 101 interpreter-startup
   system opens + 3 harness-input opens per fence decision, 17 585 system opens across the 117 runs.
2. **Counter blind spot (not exercised).** `run_fence` counts an open only if its decoded destination is under
   `root/fx` or `root/btmp`. A fence that opened the lane clone or `/home` would read as `opens=0`. My wider scan
   removed that blind spot for this run: those buckets are empty. The trace filter is also
   `trace=open,openat,openat2,creat` only — `execve`, `stat`/`statx`, `readlink` and `mmap` are unobservable, so a
   metadata read outside `d` (exactly what f6 does: the refusal message proves `lexists(d.parent/".git")`) is not
   an "open" under this predicate. The claim is therefore safe as written (opens), and must not be restated as
   "reads nothing outside `d`" without adding the stat/execve legs.
3. **Relative paths.** The counter resolves nothing; a relative-path open printed without an absolute destination
   would be dropped. My resolver handles dirfd/cwd and reports `unresolved relative/dirfd opens: 0`, so the 0 is
   not an artifact of that gap (the fence only opens absolute paths).
4. **Precision of the kept logs.** The four log files are byte-identical copies taken before the counter deletes
   `strace/sNNNNN` (K45_KEEP_STRACE), sha256 in `receipts/SHA256SUMS`; `f00000` = `48b37cc6…` etc.

No file was changed in the lane; no hostile module was needed beyond the two probe scripts in this subdir
(`analyze_opens.py`, `scan_all.py`, `patho_probe.py`), all under my own seat dir.

## 7. Tooling / cleanup

Nothing installed (existing `/usr/bin/strace`, `/usr/bin/bwrap`, `/usr/bin/python3` 3.14). Scratch
`/fast/scratch/hyaku/kengaku-r45/R45LabratReadProof` (628 MB, 1.3 M inodes) deleted at the end with
`plans/scratch_guard.py safe-rm`; receipts copied into `receipts/` here first (324 KB total, each file < 1 MiB).

VERDICT: read-proof-4-honest-clean-yes
