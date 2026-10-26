# F42CompilerSens — compiler/flag sensitivity of the round-42 `circuit-fibsqrt` receipt

Seat: F42CompilerSens (executor), wave 2 (FALSIFY) of kengaku round 42, 2026-10-26.
Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`; clone at docs tip `508434ad55c709337065611691c426f05875492d`
(frozen claims `bc856d80`, landing `ff14d76d`). No lane file was edited; nothing was committed, staged or pushed.

Question attacked: the grader compiles the task's own simulator at grading time
(`gcc -O3 /tests/sim.c -o sim`, `corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py:66`), while the receipt was
produced with **host** gcc. Does the receipt's result change with the compiler, the optimisation level, or the UB that
`sim.c` contains (uninitialised gates; out-of-range indices)?

## Axes named

1. Optimisation level within one compiler (`-O0 -O1 -O2 -O3 -Os`).
2. Compiler family and version: host gcc 16.2.1, host clang 23.1.3, and the **image's** compiler — gcc 12.2.0 from
   Debian bookworm (the family the task's `Dockerfile:2-6` installs into `python:3.13-slim-bookworm`).
3. Code-generation variants that expose latent UB (`-flto`, `-march=native`), and a different ABI (`-m32`).
4. Undefined-behaviour detectors (UBSan + ASan) over the same circuit × input grid.
5. Reachability: is any UB actually executed by a graded circuit or by any of the receipt's 16 frozen cases?

## Envelope receipt (QUALITY Q32)

Every compile, sim run, container run and fixture build below ran under the mandated envelope:

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
      --proc /proc --unshare-pid --die-with-parent <command>
```

`ls -A /home/vgpnk/.local/bin | sha256sum` sampled at every run boundary and **identical every time** —
`8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52` at 18:04:06, 18:05:24, 18:06:34, 18:09:07,
18:09:44, 18:10:20, 18:11:52, 18:13:42. `date +%T` pairs: matrix run 18:05:24 → 18:06:34; case-matrix run
18:10:20 → 18:11:52. Scratch `S=/fast/scratch/hyaku/kengaku-r42/F42CompilerSens` (clone, captures, circuits, binaries,
`TMPDIR=$S`), removed at the end with `plans/scratch_guard.py safe-rm`. Nothing was installed on the host (pacman is
paused host-wide); the container got `apt-get install gcc` **inside an ephemeral `--rm` container** only, recording
`gcc (Debian 12.2.0-14+deb12u1) 12.2.0`.

Capture digests in the clone match the probe's `PINS` exactly: `sim.c 700645ac…`, `solve.sh a4ffab41…`,
`gates.txt 032786f9…`, `test_outputs.py 6117b8ed…`, `instruction.md a7f50026…`.

## What was built

* 13 non-sanitizer builds of the frozen `sim.c`: `gcc16-{O0,O1,O2,O3,Os}`, `gcc16-O3-native` (`-march=native`),
  `gcc16-O3-lto`, `clang23-{O0,O2,O3}`, `bw12-{O0,O2,O3}` (bookworm gcc 12.2.0, built inside `debian:bookworm`,
  binary written to scratch); later `gcc16-m32`, `gcc16-m32-O0`.
* 30 inputs: the 28 graded inputs of `test_outputs.py:73-102` plus the instruction's examples 208 and 20000;
  expected values from the frozen probe's own `answer()` (copied `plans/fibsqrt_probe.py`, imported, not modified).
* Circuits, all byte-fixed and generated from the receipt's own code: `oracle` = captured `solve.sh` output
  (20104 lines, `num_signals` 20104, max referenced index 20071); `lookup28` = `text(L28)` (1195 lines);
  `lookup30` = `text(L30)` (1279); `trailing30` / `trailing28` = the same lines each ending in one space;
  `shipped` = the captured example `gates.txt` (33 lines).
* Report-level copies of the drivers and data are in `.ufo/waves/round-42/falsify/F42CompilerSens/`
  (`matrix.py`, `matrix.json`, `case_matrix.py`, `case_matrix.json`, `san_sweep.py`, `expected.tsv`, `adv-fixtures.txt`).

## R1 — 13 builds × 6 circuits × 30 inputs: no divergence (2340 sim invocations, 180 cells)

`python3 matrix.py` (S, envelope inside the driver) →

```
cells=180 divergent=0
matrix identical bw12-O0 vs bw12-O2 … gcc16-Os: True   (12/12 comparisons True)
oracle: mismatched_cells=0    lookup30: mismatched_cells=0    lookup28: mismatched_cells=0
```

Every `(circuit, input)` cell produced the same stdout **and** the same exit status under all 13 builds, and the
1170 expected-value cells (three circuits × 30 inputs × 13 builds) all equal `fib(isqrt(n)) % 2**32`. Two facts worth
recording because they are easy to get wrong:

* `trailing30`/`trailing28` print `0` on all 30 inputs in all builds, not nothing: the copy lines lose their parse but
  the `~outN` lines still parse and lift `num_signals` above 32, so `sim.c:340` prints a 32-bit window of zeroes. That
  is *why* the receipt's `lookup-28-trailing-space` is `PPF`, and the frozen prediction reproduces exactly.
* `shipped` prints `floor(n/2)` in all builds (`20000 → 10000`, `48401 → 24200`), matching `instruction.md:10`
  ("the provided example /app/gates.txt file prints outputs argv[1]/2").

## R2 — the image's own compiler, executed inside the image family

`bw12-O3` was built by gcc 12.2.0 inside `debian:bookworm` and then run **inside** that container over all 30 inputs of
`oracle`, `lookup30`, `trailing30`:

```
container(bw12-O3) vs host gcc16-O3 cells=90 diffs=0
```

So gcc 12.2.0 (bookworm, i.e. the image's compiler family at `-O3`) and host gcc 16.2.1 at `-O3` agree cell-for-cell on
the graded circuits. The knowledge entry's open caveat — "a difference between host gcc and the image's gcc in `-O3`
behaviour is untested" (`corpus/knowledge/tb2-circuit-fibsqrt-grader.md:349-352`) — is now measured and negative.

## R3 — every one of the receipt's 16 cases, re-derived and re-run under 15 builds

`case_matrix.py` re-materialises each `Case.gates` of the frozen probe (14 file cases, plus `no-gates-file` and
`gates-is-directory`), runs the 28 graded inputs under 13 builds **and** the 2 sanitizer builds (15 × 28 × 14 = 5880
sim invocations), and recomputes the three test letters per build:

```
nop PPF  oracle-solve-sh PPP  no-gates-file FFF  empty-gates-file PPF  lookup-28 PPP
lookup-27-drop-48401 PPF  lookup-28-plus-examples PPP  lookup-28-bitflip-41 PPF
lookup-28-padded-31999 PPP  lookup-28-padded-32000 PFP  lookup-28-comment-lines PPP
lookup-28-reversed-lines PPP  lookup-28-crlf PPP  lookup-28-trailing-space PPF
fake-sim-script PPF  gates-is-directory PFF
cases=16 cases_where_build_choice_changes_verdicts=0
   sanitizer_stderr_cells=0 rc_nonzero=0   (per case)
```

Every case's letter triple is a singleton equal to the probe's `predicted` column, under all 15 builds. The receipt's
`cases=16 observed_pass=7 observed_fail=9 mismatches=0` is therefore **build-invariant**, not an artefact of host gcc.

## R4 — sanitizers: the graded grid executes no UB

`gcc -O1 -fsanitize=undefined,address -fno-sanitize-recover=all` and the clang 23 equivalent, over 6 circuits × 30
inputs (360 cells):

```
sweep cells=360 nonzero_rc=0 san_hits=0
sanitizer_build_output_diffs_vs_gcc16-O3=0/360
```

No `runtime error:`, no `AddressSanitizer`, no leak/SEGV report; stdout equals the plain `-O3` build everywhere.

## R5 — different ABI

`-m32` multilib is present on this host; `gcc16-m32` and `gcc16-m32-O0` over the same 6 × 30 grid:
`i386(-m32) builds cells=360 diffs=0`. (Not an image property — the image is x86-64 — but it removes ABI as a variable.)

## F1 — falsified sentence: "nothing in the source is undefined by inspection"

The knowledge entry asserts that at `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:351`. It is false. `sim.c` writes
through file-controlled indices with no bound of its own:

| line (`corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c`) | code | UBSan message on the fixture |
|---|---|---|
| `:117-118` | `if (out_idx >= num_signals) { num_signals = out_idx + 1; …` | index committed before any check |
| `:123` | `gates[out_idx].type = OP_CONST_0;` | `sim.c:123:18: runtime error: index 33000 out of bounds for type 'Gate [32000]'` |
| `:134` | `if (num_deps[src] < MAX_DEPS) {` | `sim.c:134:25: runtime error: index 32000 out of bounds for type 'int [32000]'` (also `index -1` for a negative source) |
| `:135` | `dependents[src][num_deps[src]++] = out_idx;` | one full 10000-int row past the array |
| `:172` | `if (num_deps[src2] < MAX_DEPS) {` | `sim.c:172:29: runtime error: index 32000 out of bounds for type 'int [32000]'` |
| `:343` | `if (values[num_signals - 32 + i]) {` | OOB read once `num_signals > 32000` (the `oob-out-idx` fixture drives `num_signals` to 33001) |

The entry's own "does not show" list already names "a >32000 signal index (an out-of-bounds write in `sim.c:117-118`,
deliberately left unfrozen as non-deterministic)" (`:343`), so `:351` contradicts `:343`.

## F2 — that UB is compiler-visible where it is reachable, including a SIGSEGV at the grader's own `-O3`

Fixtures: 33 self-copy lines (`out0..out31`, `out32 = 0`) plus one line; `n=48401` unless stated. 5/5 repeat runs are
identical per cell, and `setarch -R` (ASLR off) does not change them, so these are code-generation effects, not layout
noise.

| fixture | extra line | gcc16-O0 | gcc16-O3 | gcc16-O3-lto | clang23 O0/O2/O3 | bw12-O0 | bw12-O3 |
|---|---|---|---|---|---|---|---|
| `control-base32` | — | 24200 | 24200 | 24200 | 24200 | 24200 | 24200 |
| `oob-src-copy` | `out33 = out32000` | 6050 | **2147495748** | 12100 | 12100 | 6050 | **2147495748** |
| `oob-src-binop` | `out33 = out1 & out32000` | 6050 | 12100 | 12100 | 12100 | 6050 | 12100 |
| `oob-src-neg` | `out33 = out-1` | 12100 | 12100 | 12100 | 12100 | 12100 | 12100 |
| `oob-out-idx` | `out33000 = 0` | 0 (rc 0) | **rc 139** | **rc 139** | **rc 139** | 0 (rc 0) | **rc 139** |
| `unparsed-op` | `out33 = out7 x` | 6050 | 6050 | 6050 | 6050 | 6050 | 6050 |

Consequence for the graded surface: a candidate `gates.txt` that mentions an output index ≥ 32000 makes the grader's own
`-O3` binary die with SIGSEGV (`-O3` on both gcc 12 and gcc 16, and clang at every level) while an `-O0` build of the
same source prints `0` — `test_outputs.py:121-123` then records a failed `returncode` and the case fails. No receipt
case and no graded circuit contains such an index.

## F3 — the "uninitialised gates" hypothesis is refuted

`Gate gates[MAX_SIGNALS];` is a file-scope object (`sim.c:24`; `nm` reports it as `B gates`, i.e. BSS), so any index the
parser never writes is a zero-initialised `Gate{OP_CONST_0, 0, 0}`, not an uninitialised read. A line whose operation
text does not parse (trailing space, junk tail) therefore leaves a deterministic constant-0 gate and nothing else: the
`unparsed-op` and `trailing*` fixtures agree across all builds, and the sanitizer sweep (R4) is clean. The only
non-determinism in `sim.c` comes from the out-of-range indices in F1/F2, all of which require a file-supplied index
outside `[0, 32000)`.

## Reachability (the decisive measurement)

Static scan of every circuit used above:

```
oracle      lines=20104 num_signals=20104 max_ref=20071 refs_ge32000=0 refs_ge_num_signals=0
lookup30    lines= 1279 num_signals= 1279 max_ref= 1246 refs_ge32000=0 refs_ge_num_signals=0
lookup28    lines= 1195 num_signals= 1195 max_ref= 1162 refs_ge32000=0 refs_ge_num_signals=0
trailing30  lines= 1279 num_signals= 1279 max_ref= 1246 refs_ge32000=0 refs_ge_num_signals=0
trailing28  lines= 1195 num_signals= 1195 max_ref= 1162 refs_ge32000=0 refs_ge_num_signals=0
shipped     lines=   33 num_signals=   33 max_ref=   31 refs_ge32000=0 refs_ge_num_signals=0
```

The receipt's remaining case shapes (padded, commented, reversed, CRLF, bitflip, drop-row) are index-preserving edits of
`L27`/`L28`, so the same bound holds, and R3 confirms them empirically (0 divergent cells, 0 sanitizer hits). No graded
input, no receipt case, and no `solve.sh`-generated circuit reaches a single UB site — which is exactly why 13 builds
agree to the last decimal.

## Costs and side observations

* `dependents[32000][10000]` is a 1.22 GiB BSS object; the oracle circuit at `-O3` runs 48401 in 1.05 s wall with
  89,696 KB maximum RSS (demand-paged rows), so the bound is not a memory hazard for a 32000-line file.
* Divergence on the UB fixtures splits by optimisation level inside gcc (`-O0` vs `-O3`) and by family across
  compilers (gcc vs clang), with gcc 12 and gcc 16 agreeing with each other on all five fixtures — so the risk is not
  "old vs new gcc" but "is the malformed-index class present at all".

## Suggested L1 edits (not applied — L1 integrates)

1. `corpus/knowledge/tb2-circuit-fibsqrt-grader.md:350-351`: replace "a difference between host gcc and the image's gcc
   in `-O3` behaviour is untested" with the measurement (gcc 12.2.0 bookworm vs gcc 16.2.1: 90/90 cells equal, 16/16
   cases identical), and replace "though nothing in the source is undefined by inspection" with the F1 line list.
2. `PROVINCE.md:557`: narrow "host python3 and host gcc stand in for the image's" for *this* grader — the compile step
   has been reproduced with the image's compiler family.
3. `SKILL.md` §Simulator-executed data-artefact TB2 grader — round 42 (`:1172-1201`): one sentence that the 16-case
   matrix is build-invariant across 13 builds, and one that a candidate gate list with an index ≥ 32000 SIGSEGVs under
   the grader's own `-O3`.
4. `corpus/lessons/round-42.md`: add the above as the round-42 limit that is now retired, keeping the UB-reachability
   limit (out-of-range indices untested by any frozen case).

## Limits of this seat

* 30 inputs per circuit and 6 representative circuits, not every one of the 14 file cases' `gates.txt`, for the
  13-build grid; R3 closes the case coverage at the 28 graded inputs.
* Uninitialised-*read* detection rests on the C standard's zero-initialisation of file-scope objects plus fixture
  agreement, not on MemorySanitizer or valgrind (valgrind is absent and pacman is paused host-wide).
* `tests/test.sh` and pytest were not run (same boundary as the probe); "verdict letters" are the three captured
  functions, recomputed here.
* Circuits are the receipt's own constructions, not agent submissions; nothing here says how an arbitrary submission
  behaves beyond the out-of-range-index result in F2.

Bottom line: for every circuit the receipt grades and every case it froze, the compiler, the optimisation level, LTO,
`-march=native` and the ABI change nothing — 2340 + 5880 + 360 + 360 + 90 invocations, zero divergent cells, zero
sanitizer diagnostics. The simulator *is* compiler-sensitive, but only on out-of-range-index circuits, which no graded
or frozen state reaches; on those, `-O3` (the grader's own flag) turns the out-of-bounds write into a SIGSEGV.

VERDICT: compiler-sensitive-no
