# F42CritOverclaim — round-42 C2 prose overclaim hunt (kengaku r42 wave 2, falsify)

Seat: critic (leaf). Target: the round-42 C2 prose — `corpus/README.md` (index row 75, coverage bullet 271, §Frontier round-42 sub-bullet), `PROVINCE.md` §Round42, `SKILL.md` §Simulator-executed data-artefact TB2 grader — round 42 (1160-1204) and registry/addendum (599-601, 675-688), `SCORECARD.md` §Round 42 (1729-1777), `LOG.md` §Round 42 (1278-1307). Every number checked against `corpus/evidence/round42/fibsqrt-probe.txt` and `.ufo/waves/round-42/integrate/measure-final.txt`; every mechanism checked against `corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c` and `test_outputs.py`; every "new class"/"first" checked against the seven earlier TB2 knowledge entries.

Method: static verification only — no battery, counter or sandbox run, so no Q32 envelope receipt applies (nothing wrote outside this report dir; `ls -A /home/vgpnk/.local/bin | sha256sum` was not taken because no tool run occurred). Independent recomputation of the lookup-circuit line count and the 1195 split was done in scratch-free `eval` (pure math), and the S128 source was re-read live from GitHub.

## 1. Numbers vs the receipt and measure-final — all match

| Claim (file) | Value | Verified source |
|---|---|---|
| receipt summary `cases=16 observed_pass=7 observed_fail=9 mismatches=0` | matches | `fibsqrt-probe.txt:24` (line 24 is the summary line, as `SKILL.md:1168` says) |
| `regrade cases=16 differ=0` | matches | `fibsqrt-probe.txt:23` |
| seven pass / nine fail cases | 7 PPP (`oracle-solve-sh`, `lookup-28`, `lookup-28-plus-examples`, `lookup-28-padded-31999`, `lookup-28-comment-lines`, `lookup-28-reversed-lines`, `lookup-28-crlf`); 9 fail (`nop`, `no-gates-file`, `empty-gates-file`, `lookup-27-drop-48401`, `lookup-28-bitflip-41`, `lookup-28-padded-32000`, `lookup-28-trailing-space`, `fake-sim-script`, `gates-is-directory`) | `fibsqrt-probe.txt:7-22` |
| per-case receipt line cites in the SKILL.md decision table | :7 `nop`, :8 oracle, :9 no-gates, :10 empty-gates, :11 lookup-28, :12 lookup-27, :13 plus-examples, :14 bitflip, :15 padded-31999, :16 padded-32000, :17 comments, :18 reversed, :19 crlf, :20 trailing-space, :21 fake-sim, :22 directory — all exact | `fibsqrt-probe.txt:7-22` |
| V4 "mismatches_named=0/0", V9 "case_rows=16/16" | match | `measure-final.txt` (C2 gate V4, V9) |
| before-state `checks=9 defects=6` (V2 V3 V4 V7 V8 V9), exit 1; at `fda71ae0` `defects=5` V8 ok | matches the freeze control and the baseline | `claims/control-c2-nothing.txt`; `measure-baseline.txt`; `SCORECARD.md:1741` |
| after-state `checks=9 defects=0`, `PREDICATE C2 pass`, exit 0; P10 `probe_rerun=byte-equal bytes=4212` | matches | `measure-final.txt` |
| `8 of 89` TB2 task graders | supported: 89 task dirs at pin `2fd12b88` established in `corpus/knowledge/benchmark-task-validity-checklist.md:79` ("89 task directories and 89 task.toml files") and `LOG.md:880` (92 top-level entries → 89 task directories); the eight read graders are S105/S108/S111/S115/S117/S119/S122/S125 | knowledge entries |
| knowledge files/index rows 48→49 | README index currently has 49 `knowledge/...` rows; knowledge dir has 49 files (8 `tb2-*`) | `grep -c '^| `knowledge/' corpus/README.md` → 49 |
| SOURCES 117→121 (tier A +3, tier B +1) | S-rows currently 121; S125/S126/S127 tier A + S128 tier B | `grep -c '^| S' corpus/SOURCES.md` → 121 |
| `1195-line lookup circuit` | independently recomputed: 32 self-copies + 32 NOTs + 868 ANDs (28 values × 31) + 231 ORs + 32 final copies = 1195, 0 constant lines (all 32 answer-bit positions set) | probe builder `fibsqrt_probe.py:107-137` replicated in `eval` |

## 2. Mechanism vs sim.c / test_outputs.py — all match

- `gcc -O3 /tests/sim.c -o sim` in the cwd: `test_outputs.py:65-67` (line 66 exact). ✓
- `/app/sim N` per value: `:119`. ✓
- 28-value table, max 48401 = 220²+1: `:73-102`. ✓
- compare vs `fib(isqrt(N)) % 2**32`: `:115-117`; `all_passed` assert `:147`. ✓
- `exists()` `:7-11`; size-count `:14-23` (strict `< 32000`). ✓
- cwd-relative `parse_gates("gates.txt")` `sim.c:101,:319`; skip non-scanning lines `:113-115`; `num_signals = out_idx+1` `:117-118`; unmatched operator → zero-initialised `OP_CONST_0` `:122-182` (no final else); `strtoul(argv[1])` `:324`; seed `i < 32 && i < num_signals` `:329-331`; fixed 32000-step loop `:335`; print window `values[num_signals-32+i]` `:340-347`. ✓ (all ranges cited in SKILL.md/entry are correct)
- Shipped example `gates.txt` = 33 lines; prints `argv[1]/2` = `argv[1] >> 1` (`instruction.md:10`). ✓
- `fake-sim-script` overwrite: probe harness binds `work/app` at `/app` with cwd `/app` (`fibsqrt_probe.py:227-240`), so the compile at `:66` writes `./sim` over the planted `/app/sim`; Harbor scout confirms `docker compose exec` without `-w` keeps the image `WorkingDir=/app` for this task (`R42ScoutHarborCwd.md`, incl. the measured 9-case cwd-flip experiment where `fake-sim-script` flips to PPP). ✓
- pytest parity 16/16 under real pytest 8.4.1/py3.13 (`R42CritPytest.md`). ✓
- Probe exit-code semantics (0 = mismatch on summary line, 2 = setup) match `fibsqrt_probe.py:277-360` and the SKILL.md registry row. ✓

## 3. "New class" / "eighth" vs the seven earlier TB2 entries — honest

- Eight TB2 tasks have been read/executed (rounds 35-42, one per round); number order verified (S105/108/111/115/117/119/122/125). The "eighth" claim is correct.
- The new-class claim is carefully scoped: earlier executed graders read a fixed artefact (protein-assembly, regex-log), run a helper (git-webserver), run an agent-built binary (build-pmars), or compute an embedded model (constraints-scheduling); none compiles and runs a grader-owned interpreter over the agent's data artefact at grading time. The entry explicitly disclaims novelty and notes "grading-by-simulator is not new in general" (`tb2-circuit-fibsqrt-grader.md:380-383`). README/PROVINCE/SKILL.md/SCORECARD wording ("new to this lane/executed sample", "eighth grader class") stays inside that scope.

## 4. Findings

Wrong (1, minor):
- `corpus/lessons/round-42.md:57` cites `receipt fibsqrt-probe.txt:6` for the `lookup-28` case that "prints 0 for both 208 and 20000 and still passes 3/3". Receipt line 6 is the `# capture test_outputs.py` header; the `lookup-28` CASE line is receipt line 11. The sentence's content is correct; only the pointer is wrong. (This is in the round lesson, not in the five C2 prose files, but it is a landed round-42 surface and the only mis-location found in the round's C2 evidence trail.)

Unsourced/unsupported (0 hard; one documented nuance):
- The cwd sentence "the verifier's cwd is the image WorkingDir=/app" (README/PROVINCE/SKILL.md/LOG) rests on static reading of Harbor source + Docker image config (`R42ScoutHarborCwd`), not a live Harbor run, and the probe itself fixes cwd=/app, so the frozen receipt cannot separate the two readings. The entry carries this as `[INFERENCE]` (finding 6) and the scout lists its limits; the shorter prose surfaces state it without that hedge. Not counted as an overclaim because the mechanism is corroborated two ways (probe harness + Harbor source/image config), but worth recording.

Overclaims: 0. No number, verdict letter, percentage, or mechanism statement in the five C2 prose files contradicts the receipt, the measure, the captures, or the earlier entries. The claimed 8-of-89 denominator, the 1195-line lookup, the 48401 ceiling, the 33-line example, the 7/16 pass count, and the V7 label rule all re-derive cleanly. The "new class" claims are bounded by the entry's own negative space.

VERDICT: overclaims-0-wrong-1
