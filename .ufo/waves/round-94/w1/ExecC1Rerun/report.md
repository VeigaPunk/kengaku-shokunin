# ExecC1Rerun — independent re-measurement of R94-C1 (round 94, w1)

Seat: ExecC1Rerun (leaf executor, `/skill:godspeed`). Lane untouched: all reads are `git rev-parse`/`log`/`show`/`cat-file` against
`/home/vgpnk/Projects/shokunin/kengaku-shokunin`; all runs used a `git clone --shared` in scratch
(`/fast/scratch/hyaku/kengaku-r94/ExecC1Rerun/lane`, detached at T `90c7677f0ba95d0930d93bda6a14aa50605ebe2e`, `git rev-parse --show-toplevel` = that path).
Host: kernel 7.2.11-arch1-1, `/proc/sys/user/max_user_namespaces` = 122865 (read only, not changed), `/usr/bin/bwrap`, gcc 16.2.1, clang 23.1.3, rustc 1.99.1, Python 3.14.8.
Tool installs/updates: none. No sysctl or PATH change. No git mutation in the lane.

## Verdict

- Re-measured R94-C1 at T: **pass**, rc 0, all nine legs pass, 8 cases × 4 legs, `executed_rows=38`. Matches the L1's `c1-tip.txt`.
- At BASE `0cbb9279` the counter is rc 1 (no receipt, ledger member unexecuted, 37 executed rows, 9 defects). At F `844c504e` it is rc 1 (L1, L2, L3, L5, L7, L9 fail: no receipt; L4 and L8 pass, i.e. the table and probe bytes at F are the frozen ones).
- The probe is deterministic across four full runs at the pinned compile: OBSERVATIONS blocks byte-identical, `REFERENCE_COMP_SHA` identical.
- Portability (report-only, never a claim leg): the frozen vectors **are not compile-robust**. A `gcc -O3` decode of `environment/decomp.c` flips 3 of 8 vectors, including the C01 positive control. A clang-compiled grader flips C07 (flaky). The frozen R94-C1 verdict is not flipped at the pinned invocation (`gcc -o decomp2 decomp.c`, default `-O0`), but the root cause is undefined behaviour in the captured environment decoder. Details below.

## Raw receipts (this directory)

| file | what it is |
|---|---|
| `c1-rerun.txt` | counter at T, stdout + rc |
| `c1-base.txt` | counter at BASE `0cbb9279`, stdout + rc |
| `c1-freeze.txt` | counter at F `844c504e`, stdout + rc |
| `probe-run1.txt`, `probe-run2.txt` | `round94_compressor_probe.py --lane <T clone> --work <scratch>` run twice more, stdout + rc |
| `variant-driver.py` | scratch-only driver: imports the frozen probe read-only, monkeypatches the reference build (`rustc -O`) and/or the grader's compile (`clang`, `gcc -O3`); lane and PINS untouched |
| `variant-rustcO.txt`, `variant-clang.txt`, `variant-gcc-O3.txt`, `variant-rustcO+clang.txt` | the four portability runs |
| `mechanism-decoder.txt` | decoder experiments (gcc/clang -O0..-O3, ASLR on, x200; empty stdin histogram) |

### 1. Counter at T (`c1-rerun.txt`, verbatim)

```
# cmd: python3 plans/round94_c1_replay.py --lane "$S/lane" --rev 90c7677f0ba95d0930d93bda6a14aa50605ebe2e --work "$S/w"  (shared clone detached at T; host seat ExecC1Rerun; 2026-11-05T19:05:35-03:00)
LEGS L1=pass L2=pass L3=pass L4=pass L5=pass L6=pass L7=pass L8=pass L9=pass
TARGET executed_rows=38 member=write-compressor located=1 executed=1 cases=8 legs=32 mismatches=0 defects=0
PREDICATE R94-C1 pass
rc=0
```

The L6 leg re-runs the probe from `git archive 90c7677f` inside the counter (wall 24.3 s for the whole counter).

### 2. Counter at BASE and at F (`c1-base.txt`, `c1-freeze.txt`, verbatim essentials)

```
BASE 0cbb927914e07818e1aaee7e72d8b3c90a2d21c2
LEGS L1=fail L2=fail L3=fail L4=fail L5=fail L6=fail L7=fail L8=fail L9=fail
TARGET executed_rows=37 member=write-compressor located=0 executed=0 cases=0 legs=0 mismatches=0 defects=9
DEFECT L7 ledger member=unexecuted round=None executed_total=37 cells={'file-artifact': 28, 'stdout-inspection': 12, 'subprocess-exec': 14} set_added=[] set_removed=[]
PREDICATE R94-C1 fail
rc=1

F 844c504e5147ce767a146af98e4d9b2cacb4258d
LEGS L1=fail L2=fail L3=fail L4=pass L5=fail L6=fail L7=fail L8=pass L9=fail
TARGET executed_rows=37 member=write-compressor located=1 executed=0 cases=8 legs=0 mismatches=0 defects=7
DEFECT L6 rerun rc=0 obs=8 want=0 equal=False
PREDICATE R94-C1 fail
rc=1
```

Expected: rc 1 at both. At F the probe re-run from the archive succeeds (rc 0, 8 observations), but there is no receipt to compare with.

### 3. Determinism (`probe-run1.txt`, `probe-run2.txt`)

- `diff` of the OBSERVATIONS_BEGIN..END blocks run1 vs run2: **empty**. `REFERENCE_COMP_SHA` run1 = run2 = `3a905a56e8f2937983412e6d3077cf2cec3eeb945c05b62502bb138d195b9131`, `REFERENCE_COMP_BYTES 2264`.
- Run 1 observation block (identical to run 2 and to the committed receipt `corpus/evidence/round94/compressor-probe.txt` apart from the stamp `LANE_TIP`, which the committed receipt carries as F `844c504e`; fresh runs stamp T `90c7677f`; the counter's L3 accepts either as an ancestor):

```
CASE C01 predicted=P,P,P,2264 observed=P,P,P,2264 ok=True
CASE C02 predicted=F,F,F,- observed=F,F,F,- ok=True
CASE C03 predicted=P,F,F,4868 observed=P,F,F,4868 ok=True
CASE C04 predicted=P,P,P,2264 observed=P,P,P,2264 ok=True
CASE C05 predicted=P,F,P,2000 observed=P,F,P,2000 ok=True
CASE C06 predicted=P,P,F,2564 observed=P,P,F,2564 ok=True
CASE C07 predicted=P,F,P,0 observed=P,F,P,0 ok=True
CASE C08 predicted=P,E:UnicodeDecodeError,P,2264 observed=P,E:UnicodeDecodeError,P,2264 ok=True
mismatches 0
```

Four full pinned-compile runs in total this seat (two probe runs, the L6 re-run inside the T counter, the L6 re-run inside the F counter): all identical in observations. Plus 200 ASLR-on decoder runs with `gcc -O0` and `clang -O0` on the reference artifact: all exact (see §5).

### 4. Portability variants (report-only; `variant-*.txt`, driver `variant-driver.py`)

Reference rebuilt with `rustc -O` and/or the grader's own compile call (`gcc -o decomp2 decomp.c` inside the captured `test_outputs.py`) swapped in scratch. Only the two named calls changed; PINS and the lane are unchanged.

| variant | REFERENCE_COMP_SHA | 8 vectors | verdict-level effect |
|---|---|---|---|
| baseline (pinned: rustc default, `gcc` default `-O0`) | `3a905a…9131` | 8/8 as predicted | none (the claim) |
| `rustc -O` reference | `3a905a…9131` (identical) | 8/8 identical | none |
| `rustc -O` + clang grader compile | `3a905a…9131` | 7/8: C07 → `P,E:UnicodeDecodeError,P,0` | test still fails (E or F), no pass/fail change |
| clang grader compile (`clang -o decomp2 decomp.c`) | `3a905a…9131` | 7/8: same C07 flip | C07 flaky (see §5); no pass/fail change |
| `gcc -O3` grader compile | `3a905a…9131` | **3/8**: C01 → `P,F,P,2264` (positive control FAILS); C04 → `P,E:UnicodeDecodeError,P,2264`; C06 → `P,F,F,2564` | the reference artifact fails the grader; the frozen claim's C01 pass is not compile-robust |

Verbatim `variant-gcc-O3.txt` lines:

```
CASE C01 predicted=P,P,P,2264 observed=P,F,P,2264 ok=False
CASE C04 predicted=P,P,P,2264 observed=P,E:UnicodeDecodeError,P,2264 ok=False
CASE C06 predicted=P,P,F,2564 observed=P,F,F,2564 ok=False
mismatches 3
```

Verbatim `variant-clang.txt` line: `CASE C07 predicted=P,F,P,0 observed=P,E:UnicodeDecodeError,P,0 ok=False` / `mismatches 1`.

The `rustc -O` reference is byte-identical: the debug build exits 0 with `assert_eq!` and no arithmetic-overflow panic on this input, and the code uses no floating-point fast-math, so optimised semantics should coincide. [INFERENCE from the identical sha; the shas are measured.]

### 5. Mechanism (`mechanism-decoder.txt`)

The captured `environment/decomp.c` ends with `printf("%s", buf);` on `char buf[10000]`, which is never terminated. The decoder writes exactly 4868 bytes for the reference artifact, so `printf` reads past them into uninitialised stack until it meets a NUL. Whether that byte is zero is a property of the compiled frame, not of the decoder's logic:

```
d_gcc-O0  one run: rc=0 bytes=4868 EQUAL tail=[]   ; x200 ASLR-on: 200 exact / 0 / 0
d_gcc-O1  x200: 200 / 0 / 0
d_gcc-O2  x200: 200 / 0 / 0
d_gcc-O3  one run: rc=0 bytes=4870 DIFF tail=[a0 7f] ; x200: 0 exact / 200 not-equal / 200 longer
d_clang-O0 x200: 200 / 0 / 0
d_clang-O2 x200: 200 / 0 / 0
empty stdin, gcc -O0 x20: 20 × 0 bytes
empty stdin, clang -O0 x20: 2 × 0 bytes, 18 × 6 bytes (garbage, non-UTF-8 values varying run to run)
```

The `gcc -O3` tail bytes differ run to run (`375 ~` then `c9 7f` then `a0 7f`), i.e. they are stack addresses/canaries. So C01 under `-O3` fails with roundtrip F, not nondeterministically. Under `-O0` (the pinned compile) the byte has been zero in every run here, including with `env -i`, 3000 B and 9000 B environment padding, and `setarch -R`.

Explanation of the captured Dockerfile: `RUN gcc -O3 decomp.c -o /app/decomp` (captured `environment/Dockerfile`). The image's own `/app/decomp`, the binary an agent is told to test against, therefore emits 2 trailing garbage bytes for the reference `data.comp` (4870 bytes). The grader does not use `/app/decomp`; it compiles `decomp2` itself with the pinned call.

## Findings

FINDING ExecC1Rerun-1 major The R94-C1 pass re-measures at T (rc 0, 9/9 legs, 38 executed rows), but the C01 positive control and C04/C06 pass only because `environment/decomp.c` reads an unterminated stack buffer; under `gcc -O3` the same reference artifact fails the grader (C01 P,F,P,2264; C04 E; C06 P,F,F,2564). This does not flip the frozen verdict at the pinned `gcc -o decomp2 decomp.c` (default -O0; 200/200 exact runs at -O0/-O1/-O2 and clang -O0/-O2), but "positive control" is not a robust property of the grader. Route to round 95; the claim's wording should say "at the pinned default-optimisation compile".

FINDING ExecC1Rerun-2 minor C07 (empty `data.comp`) is not stable under a clang-compiled grader: empty stdin under clang `-O0` yields 0 bytes in 2/20 runs and 6 garbage bytes in 18/20, so the round-trip leg is E or F depending on the stack. Under the pinned gcc it is 0 bytes in 20/20. Verdict unchanged (both fail the test).

FINDING ExecC1Rerun-3 info Determinism of the pinned probe is measured: four full runs at T/F identical; `REFERENCE_COMP_SHA` `3a905a56e8f2937983412e6d3077cf2cec3eeb945c05b62502bb138d195b9131`, 2264 bytes; the committed receipt matches a fresh run apart from its `LANE_TIP` stamp (F `844c504e`).

FINDING ExecC1Rerun-4 info Not measured, route to round 95 or an L0 note: (a) the real verifier's gcc is the Ubuntu 24.04 image's gcc (the captured Dockerfile installs `gcc`, `rustc`; the image tag is `alexgshaw/write-compressor:20251031`), not host gcc 16.2.1; -O0 stack contents on that toolchain are unmeasured, and that is the only plausible way C01 could differ in the real verifier. (b) The reference was built with host rustc 1.99.1, not the image's apt `rustc`; [INFERENCE] no effect, from the `rustc -O` identity, but unmeasured against an older rustc. No older toolchain was installed: the claim does not need one, and reproducing the Ubuntu toolchain would mean a container or chroot that this seat did not set up.

FINDING ExecC1Rerun-5 info Capture hygiene: `environment/main.rs` (24564 B, sha256 `fa53d657…ab389`) is byte-identical to the solve.sh heredoc but is not among the 11 frozen rows; the probe does not read it. `environment/Dockerfile` and `tests/test.sh` are captured and not pinned (the claim already rejects them as replay inputs). No verdict effect.

FINDING ExecC1Rerun-6 info The counter's `located` field is `cap is not None` (the test file exists at rev); it does not check the ledger's `located` column. The field is cosmetic; no leg depends on it.

FINDING ExecC1Rerun-7 info Lane worktree is not clean for reasons outside this seat: `git status` in the lane shows modified `SCORECARD.md`, `SKILL.md` and untracked round-94 L1/w1 files. I did not touch them. The frozen table covers none of these paths.

FINDING none beyond the above for the R94-C1 claim verdict itself: re-measured pass at T; BASE and F fail as expected.

## Not done / carried
- No `pacman`, `uv`, `npm` or any other install. No sysctl change (the user-namespace count was read only).
- `Dockerfile`, `tests/test.sh`: not executed (claim rejects them as inputs).
- Sibling overlap, C2 counter and source re-fetch: out of this item.

## Cleanup
Scratch `/fast/scratch/hyaku/kengaku-r94/ExecC1Rerun` (shared clone, probe work dirs, variant dirs, mechanism files) removed before yield; everything citable is copied into this directory.
