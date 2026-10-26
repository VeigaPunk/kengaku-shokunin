# R42CritIndep — independent re-derivation of the tb2 `circuit-fibsqrt` grader (C2)

Seat: R42CritIndep (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Scratch: `/fast/scratch/hyaku/kengaku-r42/R42CritIndep` (kept). Nothing in `plans/`, `corpus/` or any
lane file was read-modified or written; no git/jj mutation was run in any repo; no subagent, no
background job.

**Method.** I wrote my own Python model of the captured `sim.c` (parse + event-driven step + output
window) and of the captured `test_outputs.py` (three tests), from the captured sources only —
`corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c` (sha256 `700645ac…`) and
`…/test_outputs.py` (sha256 `6117b8ed…`). I never imported the grader, never compiled or ran `sim.c`,
never imported or ran `plans/fibsqrt_probe.py`, and rebuilt every case end state with my own circuit
generator. `model.py` / `predict.py` / `extras_gen.py` are in this directory (my authorship).

## 1. The model — rules I derived from the captured C, with citations

Parse (`sim.c`):
- `fgets(line, 256)` (:107-108): a physical line is cut at **255 bytes**; the remainder becomes the
  next "line".
- `sscanf(line, "out%d = %[^\n]", &out_idx, op) != 2 → continue` (:113). `%[^\n]` needs ≥1
  non-newline char and **captures `\r`**.
- `if (out_idx >= num_signals) num_signals = out_idx + 1;` (:117-118) runs **before** the op is
  classified, so a line whose op cannot be parsed still moves the printed window.
- op classes in this order: `"0"` (:122), `"1"` (:124), prefix `out` **and no literal space**
  (`!strstr(op," ")`) → copy (:126-129), `~out` → not (:139-142), `sscanf(op,"out%d %c out%d")==3`
  → and/or/xor (:156), else **dropped**: the gate keeps the zero-initialised global type = `CONST_0`
  and no dependency edge is registered.
- Consequence table (all confirmed by my model on real case bytes):
  | line style | LF | CRLF | one trailing space |
  |---|---|---|---|
  | `outA = outB` (copy) | copy | copy (`%d` stops at `\r`) | **dropped** → CONST_0 |
  | `outA = ~outB` | not | not | not (branch does not test for spaces) |
  | `outA = outB & outC` | binary | binary | binary (`%d %c %d` tolerates it) |
  | `outA = 0` | 0 | **dropped** → 0 (value-identical) | **dropped** → 0 (value-identical) |
  | `outA = 1` | 1 | **dropped** → 0 (**breaks the value**) | **dropped** → 0 (**breaks the value**) |
  | `# anything` | skipped | skipped | skipped |
- Step (`simulate_step`, :205-300): step 0 seeds **every** signal into a min-heap (:205-210); a changed
  signal queues dependents in the *current* queue only when `!did[dep] && dep > sig` (:291) and always
  in the *next* queue. 32000 steps (:335) is therefore a fixpoint iteration.
- Output (:342-343): `values[num_signals-32+i]`, i.e. the **32 highest-indexed** signals — not the
  file's last 32 lines, and not `instruction.md:9`'s "last 32 lines".
- `MAX_SIGNALS` is 32000 (:5): `gates[32000]` is an out-of-bounds write, `values[32000]` an OOB read.

Grader model (`test_outputs.py`): T1 `Path("/app/gates.txt").exists()` (true for a directory too);
T2 `sum(1 for line in f) < 32000` in **text mode** (:23) — newline counting, CRLF collapsed, a
`>255`-byte line is *one* line; T3 compiles `sim.c` with `gcc -O3 … -o sim` in the cwd (:66),
so a pre-existing `/app/sim` is overwritten, runs `/app/sim N` for the 28 fixed N (:73-101),
`int(result.stdout.strip())` (:127) — `ValueError` is a fail — and compares with
`fibonacci(isqrt(N)) % 2**32`. Any rc≠0, any mismatch ⇒ T3 = F.

Calibration of the model against facts independent of the grader:
- Shipped example (`gates.txt`, 33 lines, sha256 `032786f9…`): `num_signals=33`; model prints
  N=1→0, 8→4, 209→104, i.e. `N>>1`, matching `instruction.md`'s "prints outputs argv[1]/2".
- The oracle: ran the captured `solve.sh` in my scratch (`bash solve.sh` → `gates.txt`, 20104 lines,
  sha256 `39478a8f…`); model prints N=1→1, 41→8, 208→377, 20000→1407432322, 48401→3361931507 —
  all equal to `answer(N)`, and 377 / 1407432322 are the two numbers instruction.md names.
- My own lookup generator's line counts equal the frozen dry table's `gates_lines` for every shaped
  case: 1195 (L28), 1151 (L27), 1279 (L30), 1196 (bitflip), 31999, 32000, 2390 (comments).
- L28 class census: 1195 lines = 64 copies (32 input self-copies + 32 output copies), 32 NOT,
  868 AND, 231 OR, no constants — so every one of the 32 answer bits has a contributing value.
- `lookup-28` prints **0** for 208 and for 20000 (instruction requires 377 / 1407432322), so its
  `violates=example-208,example-20000` tag is correct; it passes only because grading stops at 48401.

## 2. The 16 frozen cases, re-derived (not run)

Command: `python3 predict.py` in my scratch (model only; 339 s). Predicted letters vs the receipt's
`tests=` field in `corpus/evidence/round42/fibsqrt-probe.txt`:

| # | case | my model | receipt `tests=` | same as frozen `predicted_tests` |
|---|---|---|---|---|
| 1 | nop | PPF | PPF | yes |
| 2 | oracle-solve-sh | PPP | PPP | yes |
| 3 | no-gates-file | FFF | FFF | yes |
| 4 | empty-gates-file | PPF | PPF | yes |
| 5 | lookup-28 | PPP | PPP | yes |
| 6 | lookup-27-drop-48401 | PPF | PPF | yes |
| 7 | lookup-28-plus-examples | PPP | PPP | yes |
| 8 | lookup-28-bitflip-41 | PPF | PPF | yes |
| 9 | lookup-28-padded-31999 | PPP | PPP | yes |
| 10 | lookup-28-padded-32000 | PFP | PFP | yes |
| 11 | lookup-28-comment-lines | PPP | PPP | yes |
| 12 | lookup-28-reversed-lines | PPP | PPP | yes |
| 13 | lookup-28-crlf | PPP | PPP | yes |
| 14 | lookup-28-trailing-space | PPF | PPF | yes |
| 15 | fake-sim-script | PPF | PPF | yes |
| 16 | gates-is-directory | PFF | PFF | yes |

`indep_agree=16/16`. Mechanism notes behind the three interesting letters:
- #10 PFP: 32000 blank lines — T2 fails on the count, T3 passes because blanks never scan
  (`num_signals` stays 1195).
- #14 PPF: my model drops exactly **64** lines = the 32 input self-copies **and** the 32 output
  copies; the inputs are zeroed at step 0 *and* the final copies (the printed window) become
  CONST_0, so every N prints 0.
- #16 PFF: T1 passes because `Path.exists()` is true for a directory; T2 raises `IsADirectoryError`;
  T3 fails (my model: `fopen`/`fgets` yield no lines → `num_signals==0` → no stdout → `ValueError`).
- #12 PPP: reversing lines cannot change anything because every line names its own `out<idx>`; the
  printed window is by index, not by position.

## 3. My three cases (task's own suggestions) — predictions frozen before the run

Byte-identical case files, predicted with `extras_gen.py` **before** the probe run
(`extras.json`, sha256 of each end-state `gates.txt`):

| case | mechanism | predicted | observed | lines | num_signals | sha256 |
|---|---|---|---|---|---|---|
| `dup-gate-definition` | L28 + a second definition `out0 = out31` (duplicate index) | **PPF** | **PPF** | 1196 | 1195 | `c01b7ffe…b7706` |
| `out32000-line` | L28 + `out32000 = 0` (index == `MAX_SIGNALS`) | **PPF** | **PPF** | 1196 | 32001 (model flags OOB write & read at 32000) | `7b9d1021…b99d9` |
| `wrong-above-48401` | the reference circuit + an 89-gate guard `out = ref_out & ~(N > 48401)` | **PPP** | **PPP** | 20193 | 20193 | `c3d0f85d…dd131` |

Plus two more of my own (reported but not counted in the verdict):

| case | mechanism | predicted | observed | sha256 |
|---|---|---|---|---|
| `long-line-window` | L28 + one 261-byte line `out31999 = 0`+250 spaces | **PPF** | **PPF** | `915ae77d…61650` |
| `oracle-crlf` (control) | the reference circuit with CRLF line ends | **PPF** | **PPF** | `6bb47b83…d301` |

What each measured:
- `dup-gate-definition` PPF: the last definition of an index wins and the stale dependency edge from
  the first definition is harmless (it only causes a re-evaluation). `out0 = out31` makes input bit 0
  read bit 31, every odd graded N is missed (`N=1` prints 0, expected 1; `N=48401` still right).
- `out32000-line` PPF: `num_signals` becomes 32001 with only 1196 physical lines, so T2 passes and the
  printed window moves to `values[31969..32000]` — 31 in-bounds CONST_0 signals and one OOB read.
  Observed F exactly as predicted; bit 31 of the output comes from memory past `values[]`.
- `wrong-above-48401` PPP: right on all 28 graded inputs and on 208/20000/48401, prints 0 for
  48402/65536/4000000000 — i.e. **wrong for all 4294918894 inputs above 48401** and still 3/3.
- `long-line-window` PPF: `fgets` cuts the line at 255 bytes, the gate is dropped, `num_signals`
  still reaches 32000, the window is all zeros; the grader counts the same physical line **once**.
- `oracle-crlf` control PPF: the reference circuit has 250 `= 1` lines; my model drops 2048 lines
  under CRLF (250 `= 1` — the only semantically harmful class — plus 1798 `= 0`, value-neutral), and
  the circuit prints 0 for every N. CRLF is therefore **conditional**, not benign.

## 4. What the entry must carry (falsifiers this seat adds)

1. Output is the **32 highest-indexed signals**, not the file's last 32 lines, and `num_signals` grows
   even from a line whose op fails to parse (`sim.c:117-118` before the class chain). One stray
   high-index line re-points the output window and zeroes the result (`long-line-window`,
   `out32000-line`) — a failure mode no receipt case covers.
2. `CRLF passes` (receipt case 13) is **circuit-specific**: it holds because no L28 line is `= 1`.
   The reference circuit has 250 such lines, so CRLF turns `oracle-solve-sh` PPP into PPF.
3. Trailing spaces damage exactly the copy lines and the `= 1` lines; NOT and binary lines tolerate
   them. For L28 that is 64 lines (32 input self-copies + 32 output copies) — measured `dropped=64`.
4. A physical line over 255 bytes is truncated by `fgets` while the grader's size test counts it as
   one line: the size test and the parser disagree about what a line is.
5. `out32000` (index == `MAX_SIGNALS`) is unguarded: OOB write into `gates[]`/`values[]` and an OOB
   read for output bit 31. Observed PPF, `regrade=same`.
6. Duplicate definitions are last-wins with harmless stale edges (PPF when the duplicate rewires an
   input copy).
7. The grader certifies "correct on these 28 inputs", not "computes fib(isqrt(N))": `lookup-28`
   passes while printing 0 for the instruction's own examples, and `wrong-above-48401` passes while
   being wrong for every N > 48401.
8. `test_gates_file_exists` is vacuous on a directory (`Path.exists()`), so a `gates.txt` directory is
   PFF, not FFF.

## 5. Evidence

Probe run of my modified **copy** (`/fast/scratch/…/R42CritIndep/probe_copy.py` = the frozen probe
verbatim + the 5 cases above appended; the frozen `plans/fibsqrt_probe.py` was never executed or
modified — its 16 case objects run unchanged inside the copy). Receipt:
`probe_extra_run.txt` (sha256 `8a63888f…7301`), quoted head/tail:

```
ENVELOPE bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent /usr/bin/python3 …/probe_copy.py --lane …/kengaku-shokunin --work …/probework
T0 17:41:24
PATHBIN0 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
# tb2 circuit-fibsqrt grader probe (kengaku round 42) @ terminal-bench-2 2fd12b88
# capture gates.txt sha256=032786f9…  (all five captures verified at their pinned digests)
…
CASE dup-gate-definition predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same …
CASE long-line-window predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same …
CASE out32000-line predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same …
CASE wrong-above-48401 predicted=pass observed=pass tests=PPP predicted_tests=PPP match=yes regrade=same violates= …
CASE oracle-crlf predicted=fail observed=fail tests=PPF predicted_tests=PPF match=yes regrade=same …
regrade cases=21 differ=0
cases=21 observed_pass=8 observed_fail=13 mismatches=0
rc=0
T1 17:44:30
PATHBIN1 436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -
```

- Host guard: the envelope above is the mandated one; `ls -A /home/vgpnk/.local/bin | sha256sum` is
  identical before and after (`436b361f…fc18`), `date +%T` 17:41:24 → 17:44:30, wall 3m06s, rc=0.
  The probe's own inner sandbox (`--unshare-net/pid/ipc`, `/usr` and `/etc` read-only, `/app` fresh)
  nests inside it. No writes outside my scratch and this directory.
- Model runs wrote only inside my scratch; `TMPDIR` was my scratch, never `/tmp`.
- Tooling: nothing installed, nothing upgraded (python3 3.14.8, gcc 16.2.1 inside the sandbox, bwrap
  already present). No pacman transaction was attempted.
- Files in this directory: `model.py` (`e5d6c602…`), `predict.py` (`d21fae6c…`), `extras_gen.py`
  (`a0252f0d…`), `predictions.json` (`d9fe357e…`, per-case letters, line counts, sha256, model output
  on N=1/41/208/20000/48401), `extras.json` (`76e0852b…`, same for my 5 cases), `probe_extra_run.txt`
  (`8a63888f…`).

Risks / limits, stated: my model is a re-derivation, not the binary. It agrees with all 21 observed
case verdicts, with the frozen predictions, with the dry table's line counts, with the shipped
example's `N/2`, and with the oracle's 28 answers — but a semantic disagreement in a region no case
exercises would not be visible. The `out32000-line` letter is F for a reason that survives C's UB
(bits 0-30 of the window are in-bounds zeros and no graded answer is 0 or 2^31), yet the exact printed
integer there is not predictable from the source.

VERDICT: indep-agree-16/16-extra-3/3
