# F39C2Rerun — C2 re-run on a clean clone at a6832f53 (round 39, wave 2)

Seat: F39C2Rerun, executor (leaf). Axes: coverage, calibration.
Attacks: the C2 frozen predicate and its three-times probe determinism claim, measured at lane tip
`a6832f53c1a94bb092a6cfd79fb4e449f2d4054c`. No lane file was edited; the only lane writes are this report and
`.ufo/waves/round-39/falsify/F39C2Rerun/` receipts.

## Fixture (exact)

```
S=/fast/scratch/hyaku/kengaku-r39/F39C2Rerun; mkdir -p "$S"; export TMPDIR="$S"
git clone -q --no-local /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" checkout -q a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
```
```
$ git -C $S/lane rev-parse HEAD          -> a6832f53c1a94bb092a6cfd79fb4e449f2d4054c
$ git -C $S/lane status --porcelain      -> (empty)
$ git -C $S/lane rev-parse --show-toplevel -> /fast/scratch/hyaku/kengaku-r39/F39C2Rerun/lane
```
Lane HEAD is one commit ahead of the target tip and that commit touches only wave-2 dispatch metadata:
```
$ git -C kengaku-shokunin rev-list --count a6832f53..HEAD -> 1
$ git -C kengaku-shokunin diff --stat a6832f53 HEAD
 .ufo/waves/round-39/falsify-dispatch.json | 561 ++++++
 .ufo/waves/round-39/falsify-spec.json     | 322 ++++
```
So the measurement below is at the frozen tip, not a stale or newer tree. Receipt: `F39C2Rerun/fixture-clone.txt`.

## 1. Predicate re-run (the assigned command)

```
$ cd "$S/lane" && python3 plans/round39_c2_verify.py --lane .      # exit 0, ~3 s
V1 ok listed=7 bad=0 extra=0
    gate: P1 ok pinned=2 mismatched=0
    gate: P2 ok receipt_sha256=pinned
    gate: P3 ok rows=29 distinct_quotes=29 distinct_lines=29 out_of_word_range=0
    gate: P4 ok checked=29 bad=0 first=0
    gate: P5 ok manifest_entries=7 bad=0 first=0
    gate: P6 ok rows=2 bad=0 first=0
    gate: P7 ok source_lines=2 bad=0 first=0
    gate: P8 ok index_rows=46 knowledge_files=46 bad=0 first=0
    gate: P9 ok untracked=0 first=0
    gate: P10 ok probe_rerun=byte-equal bytes=5867
    gate: defects=0
V2 ok spec=frozen gate=frozen gate_exit=0
V3 ok rows=2 bad=0
V4 ok cases=25 mismatches_named=0/0 bad=0
V5 ok probe=frozen dry_byte_equal=True
V6 ok census_exit=0
V7 ok rows=4 tags=4 bad=0
checks=7 defects=0
PREDICATE C2 pass
```
The frozen predicate (`plans/round-39-claims.md:79-80`, `plans/round39_c2_verify.py:5-7`) is met exactly:
`checks=7 defects=0`, `PREDICATE C2 pass`, exit 0. Beyond the predicate, the whole 20-line output is
**byte-identical to the L1's landing measurement** (`.ufo/waves/round-39/integrate/measure-final.txt:107-126`; my
`diff` against that 21-line block reported only the harness's own trailing `exit=0` line as extra), which used the
same counter on the same tip with an explicit `--work`; the `--work` path is not observable in output because the
probe prints no scratch path (`grep -c 'fast/scratch\|/tmp/'` on the probe output → `0`).
Receipt: `F39C2Rerun/c2-verify-output.txt`.

Determinism of the counter itself, three consecutive runs:
```
$ for i in 1 2 3; do python3 plans/round39_c2_verify.py --lane . > c2-r$i.txt; done   # all exit 0
$ sha256sum c2-r1.txt c2-r2.txt c2-r3.txt
8cbf83841a2756543b10da500a250acb9e2ce0148d64b57392b8a812690e65a4  (x3, identical)
```
Note the counter invokes the gate with `--rerun`, so each of these three runs also executed the probe once inside
P10 (`plans/pkg_gate.py:267-285`); nine probe executions in total left every byte in place.

## 2. Probe three times + byte-compare (the assigned command)

Runs, all `python3 plans/git_leak_probe.py --lane .`, all exit 0, `cases=25 observed_pass=13 observed_fail=12
mismatches=0`:

| run | condition | sha256 of stdout | vs receipt |
|---|---|---|---|
| A | plain, `--work $S` | `d7f3a465…609b5f` | byte-equal |
| B | plain, `--work $S` | `d7f3a465…609b5f` | byte-equal |
| C | `env -i PATH=/usr/bin:/bin HOME=$S` | `d7f3a465…609b5f` | byte-equal |

```
$ cmp -s probe-A.txt corpus/evidence/round39/git-leak-probe.txt   -> equal
$ cmp -s probe-B.txt <receipt>                                    -> equal
$ cmp -s probe-C.txt <receipt>                                    -> equal
$ sha256sum probe-{A,B,C}.txt <receipt>  -> d7f3a465ccc411572c96fc039235854093d1eb52ccd685b618a28a10de609b5f (4x, one value)
$ wc -c <receipt> -> 5867     (matches the gate's own P10 "bytes=5867")
```
`k = 3/3`. Receipt: `F39C2Rerun/probe-byte-equal.txt`.

Two extra determinism probes (same receipt, same value `d7f3a465…`), because "byte-equal three times" is only
strong if the probe is insulated from the caller:
- **D, hostile git environment** — `HOME` pointing at a directory with `[init] defaultBranch = trunk`,
  `GIT_CONFIG_GLOBAL` at that file, `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE=2001-01-01`, `GIT_DIR=/nonexistent`,
  `GIT_DEFAULT_HASH=sha256`, `PYTHONHASHSEED=12345` → **byte-equal**. The probe passes a closed env dict and
  neutralises git config itself (`plans/git_leak_probe.py:212-213`: `GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, `HOME=/tmp`, `LC_ALL=C.UTF-8`), so no caller git state reaches the harness.
- **E, foreign cwd** — run from `$S/elsewhere` with an absolute `--lane` and absolute script path → **byte-equal**.

`probe-D-hostile` and `probe-E-cwd` are also `d7f3a465…`; 5/5 direct runs and 9 total executions agree.

## 3. Capture manifest (the assigned command)

```
$ cd corpus/evidence/round39/tb2-git-leak-recovery && sha256sum -c SHA256SUMS
Dockerfile: OK
challenge-setup.sh: OK
instruction.md: OK
solve.sh: OK
task.toml: OK
test.sh: OK
test_outputs.py: OK            (exit=0, 7/7)
```
Cross-check of the receipt against the frozen case table, independent of the counter:
```
$ grep -c '^CASE ' git-leak-probe.txt                     -> 25
$ grep -c '^CASE ' git-leak-dry-cases-freeze.txt          -> 25
$ diff ids-receipt.txt ids-dry.txt                        -> (empty; same ids, same order)
$ grep -c 'match=NO' git-leak-probe.txt                   -> 0
$ grep '^TAG ' git-leak-dry-cases-freeze.txt
TAG recover-secret instruction.md:3
TAG secret-gone instruction.md:4
TAG files-untouched instruction.md:5
TAG messages-untouched instruction.md:5
```
All 25 predictions held on this host (predicted 13 pass/12 fail, observed 13/12, `mismatches=0`), which is the
calibration claim the receipt makes; I re-observed it, I did not take it from the receipt.

## 4. Is the counter live? Seven mutations (`$S/mut`, second clone at the same tip)

Method: mutate a copy of the tree, run the frozen counter, record which `V<n>` flips, restore from the pristine
clone (`git -C $S/mut status --porcelain` → empty after every mutation). Receipt:
`F39C2Rerun/mutation-log.txt` and `F39C2Rerun/mutation-m7-selfconsistent-receipt.txt`.

| # | mutation (what it attacks) | flipped | defects | predicate |
|---|---|---|---|---|
| M1 | one byte appended to capture `Dockerfile` (V1) | `V1 DEFECT listed=7 bad=['Dockerfile']`, plus V2 via gate P5 | 2 | fail |
| M2 | receipt CASE `echo-only` observed pass→fail (V4) | `V4 DEFECT … 'summary disagrees with the CASE lines'`, plus V2 via P4/P10 | 2 | fail |
| M3 | requirement-map label `recover-secret` enforced→unenforced (V7) | `V7 DEFECT … 'recover-secret: labelled unenforced, receipt derives enforced'` — alone | 1 | fail |
| M4 | registry anchor digest in SOURCES S117 (V3) | `V3 DEFECT rows=2 bad=['S117:anchor_digest']` — alone | 1 | fail |
| M5 | frozen dry table byte edit (V5) | `V4/V5/V7 DEFECT` / `error ValueError: dry table not at its freeze digest` | 3 | fail |
| M6 | spec `receipt_sha256` pin (V2) | `V2/V3/V4/V7` `error ValueError: spec template not at its freeze digest` | 4 | fail |
| M7 | **self-consistent** receipt forgery: CASE flipped, summary adjusted 13/12→12/13, `match=yes` kept | `V1 V3 V4 V5 V6 V7 ok`; **only** `gate: P10 DEFECT fresh probe output is not byte-equal to the receipt` → `V2 DEFECT gate_exit=1` | 1 | fail |

Readings:
- M3 and M4 isolate a single check (`defects=1`), so V3 and V7 are not riding on other clauses; M1/M2/M6 show
  duplication by design (gate re-derives V1's manifest and V2's spec digest).
- **Boundary, named not buried:** V4's receipt clauses are *not* forgery-proof on their own — M7 satisfies V4
  (`cases=25 mismatches_named=0/0 bad=0`), V1, V5, V7 and still leaves `defects=1`. Authenticity rests entirely on
  the gate re-executing the probe and byte-comparing (`plans/pkg_gate.py:283` `if r.stdout != want:`), exactly as
  the counter docstring states at `plans/round39_c2_verify.py:16-18`. That is a
  documented design decision, not a defect — but it means the receipt file is trusted only to the extent P10 can run
  (see §5).
- Error paths are fail-closed: a check that raises becomes `DEFECT error ValueError: …`, never a pass
  (`plans/round39_c2_verify.py:272` `a check that cannot run is a defect, never a pass`) — measured in M5/M6.

## 5. Dependencies of the predicate that a "clean clone" alone does not satisfy (named limits)

1. **The fleet census script is an absolute path outside the clone.** `plans/round39_c2_verify.py:65`
   `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`, used by V6 at `:201-204`. Masking it with
   `bwrap --ro-bind / / --tmpfs /home/vgpnk/Projects/shokunin/scripts …`:
   ```
   V6 DEFECT error FileNotFoundError: [Errno 2] No such file or directory: '…/scripts/sources-census.sh'
   V2 DEFECT spec=frozen gate=frozen gate_exit=1
   checks=7 defects=2 ; PREDICATE C2 fail ; exit 1
   ```
   So V6 is a *fleet-root* dependency, not a clone-local one; it still fails closed. (In that masked run V2 failed
   too, because the gate's P10 runs the probe through `uv run --no-project --with biopython==1.85` and `uv` needs a
   writable `$HOME` cache: `P10 DEFECT fresh probe exit=2 stderr='error: Could not acquire lock …'`.)
2. **Biopython is not in host python** (`python3 -c "import Bio"` → `ModuleNotFoundError`), so P10 takes the gate's
   `uv` branch (`plans/pkg_gate.py:272-276`). On this host the wheel is cached
   (`uv run --no-project --offline --with biopython==1.85 python3 -c "import Bio;print(Bio.__version__)"` →
   `Bio 1.85`), so the run is offline-capable today; on a cold host the predicate needs network once.
3. `bwrap` (`/usr/bin/bwrap`), `/usr/bin/git` and a writable `TMPDIR`/`--work` are required; missing bwrap/git makes
   the probe exit 2 (`plans/git_leak_probe.py` tool check), which P10 reports as a defect, not a pass.
4. `plans/pkg-spec-r39.json` carries `receipt_sha256: null` by design; the counter fills it from the receipt it finds
   (`plans/round39_c2_verify.py:120`), so P2 is a presence check. Running the gate directly on the raw spec shows
   `P2 DEFECT receipt_sha256=d7f3a465…` — expected under that design, recorded so nobody mistakes it for tampering.
   Receipt: `F39C2Rerun/census-dependency-masked.txt`.

## Files changed

None in the lane tree. Written (new):
- `.ufo/waves/round-39/falsify/F39C2Rerun.md` (this report)
- `.ufo/waves/round-39/falsify/F39C2Rerun/`: `fixture-clone.txt`, `c2-verify-output.txt`, `probe-byte-equal.txt`,
  `mutation-log.txt`, `mutation-m7-selfconsistent-receipt.txt`, `census-dependency-masked.txt`

No lane file, no corpus/plans tree, no clone and no lane mirror was copied into the falsify directory; the two
fixture clones lived only under `/fast/scratch/hyaku/kengaku-r39/F39C2Rerun/` and were deleted
(`rm -rf -- "$S"`) after the receipts were copied. No git/jj mutating command ran in the lane; no tool was installed
(masked-census probe needed no install; nothing was filed with pacman, which is paused host-wide).

## Risks / what this does not cover

- The probe's fidelity to the TB2 image is still the round's named limit (host git 2.56.0/bwrap stand-ins); my
  re-runs measure host behaviour, not image behaviour.
- Byte-equality is measured on one host, warm `uv` cache, one kernel. It cannot exclude a future git or bwrap change
  altering the five `git`-derived test verdicts; P10 would catch that only if the receipt were left unchanged.
- M7 shows the receipt is trusted by re-execution, so any environment where P10 cannot execute (no bwrap, no network
  on a cold cache) degrades the counter's authenticity argument to exit 1 — safe, but not "verified".
- I did not re-run the C2 probe on the Ubuntu image the task pins, and did not touch C1, the routed fixes, or any
  other wave-2 item.

VERDICT: c2-rerun-pass-probe-byte-equal-3/3
