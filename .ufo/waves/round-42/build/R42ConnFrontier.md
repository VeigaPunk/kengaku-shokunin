# R42ConnFrontier — frontier/coverage check (kengaku round 42, wave 1)

Seat: R42ConnFrontier (connector, leaf). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Read-only seat: nothing in the lane was edited, staged or committed. Scratch `S=/fast/scratch/hyaku/kengaku-r42/R42ConnFrontier` (TMPDIR only; no fixture builds needed for this check, so no bwrap envelope runs — every command below is a read/grep on lane bytes).

**Axes named (godspeed):** coverage = did the round open ground the seven admitted TB2 graders did not hold, and which §Frontier clause narrows; calibration = how many self-assessment lines in SCORECARD/SHONEN/README now mismatch the repo state (the denominator outside C1). One bounded move: draft the narrowing text + flag the stale line.

## 1. Is the class new? Yes — "a data artefact executed by a grader-owned simulator compiled at grading time, scored on a fixed table" is ground the lane did not hold

The seven admitted TB2 task graders (corpus/knowledge/tb2-*.md, 7 files; index rows at corpus/README.md:62-74; coverage bullets at corpus/README.md:265-269) and their graded-artefact classes:

| # | task (round) | graded artefact | does the grader execute it? | scored against |
|---|---|---|---|---|
| 1 | protein-assembly (35) | gBlock FASTA (data) | never — string/regex assertions only | literal subproteins/order/FLAG/SNAP/GC windows |
| 2 | regex-log (36) | regex file (agent-authored **code**) | `re.compile`+`findall` — the language runtime, not a grader-owned compiled simulator | literal 9-date list over a fixed 25-line log |
| 3 | configure-git-webserver (37) | two live HTTP responses | helper shell script runs; no compilation, no simulator, no fixed input table | substring `TEST PASSED` |
| 4 | build-pmars (38) | **agent-built** executable + source tree | binary run — but agent-authored and agent-built; the grader never compiles | `Results:` stdout prefix, `ldd` string scan, presence, tree shape — not a fixed input table |
| 5 | git-leak-recovery (39) | git refs/object store + flag file | git plumbing over the state; artefact never executed | literal secret, `git log` greps, fsck sweep, work-tree checksum |
| 6 | db-wal-recovery (40) | JSON export | never — `json.load` + assertions | 22 of 33 pinned id/name/value cells |
| 7 | constraints-scheduling (41) | one-event ICS file | read with regexes by an embedded scheduling model; **not executed** | expectations computed from three pinned calendars |

`circuit-fibsqrt` (frozen captures `corpus/evidence/round42/tb2-circuit-fibsqrt/`, digests verified equal to the S125–S127 pins: `sha256sum` of the captures vs SHA256SUMS — test_outputs.py `6117b8ed…`, instruction.md `a7f50026…`, sim.c `700645ac…`) is the first grader where the joint triple holds, each leg grounded in the capture:

1. **The graded artefact is pure data.** A gate netlist at `/app/gates.txt` (existence test `test_outputs.py:9`; size test `:17-23`).
2. **The executor is a grader-owned simulator compiled at grading time.** `test_outputs.py:65-66` runs `gcc -O3 /tests/sim.c -o sim` with no `cwd=` — i.e. in the graded cwd, producing `/app/sim` from grader source at grading time; `:119` then executes `/app/sim N`.
3. **Scored on a fixed table.** `test_outputs.py:76-103` hard-codes 28 test values (1,4,8,12,41,42,107,220,209,366 and x², x²−1, x²+1 for x∈{12,41,42,107,220,209}; max 48401); `:104-106` computes the oracle itself: `expected = fibonacci(isqrt(n)) % 2**32` — a reference model embedded in the test file, not a literal list.

Closest neighbors and why they do not already hold the ground: regex-log (#2) has an agent-authored pattern executed by grader machinery against a fixed literal list, but the artefact is code and the executor is the Python runtime, not a grader-owned program compiled at grading time. build-pmars (#4) executes a graded binary, but the binary is agent-authored and agent-built (nothing is compiled at grade time) and scoring is a stdout prefix/presence scan, not a fixed 28-input table. constraints-scheduling (#7) has the grader own a computation that decides the verdict, but the graded artefact is read, not executed, and no compilation occurs. The joint property (pure-data artefact ∧ grader-owned simulator compiled at grade time ∧ fixed scored input table) is new to the executed sample.

Two measured behaviours are also firsts for the admitted sample:

- **The grader writes a compiled executable into the graded tree at grade time.** Case `fake-sim-script` (receipt:21): a planted executable `/app/sim` printing the right answers is overwritten by the grader's own compile; the case still fails only because `/app/gates.txt` is the shipped example. No admitted grader #1–#7 materializes a grader-built executable inside `/app` during grading.
- **The size bound counts what the simulator skips.** `test_outputs.py:21-23` counts every line (`sum(1 for line in f)` → `< 32000`); sim.c skips lines that do not scan as `out%d = <op>` (`sim.c:108-113`). Padding a wrong circuit to 31999 lines passes 3/3 (`lookup-28-padded-31999`); 32000 fails only the size test (`lookup-28-padded-32000`, tests=PFP); trailing spaces fail (`lookup-28-trailing-space`) because the copy-scan breaks (`sim.c:129`).

Receipt (first recorded run, `corpus/evidence/round42/fibsqrt-probe.txt:23-24`): `cases=16 observed_pass=7 observed_fail=9 mismatches=0`; `regrade cases=16 differ=0`. Two instruction-vs-grader gaps measured by the probe: instruction.md:8 says inputs arrive via stdin but sim.c:324 reads `argv[1]`; instruction.md:9 says "the last 32 lines" are output but sim.c:340-347 prints the 32 highest-**indexed** signals (case `lookup-28-reversed-lines` passes).

## 2. Which frontier clause narrows, and how it should read

The narrowing clause is the round-41 sub-bullet of the `**Agentic benchmark task-spec audits**` bullet in `corpus/README.md` §Frontier (§Frontier at :285; round-41 sub-bullet at :343-357). Its tail at **corpus/README.md:356** currently reads `remaining TB2 task graders (7 of 89 read)`. The coverage-map bullet at corpus/README.md:269 says `A seventh instance of the same ground (7 of the 89 TB2 task graders…)`; PROVINCE.md's Round41 paragraph (:470-507) says `remaining 82 TB2 task graders … 7 are read`.

How it should read — following the append-only pattern every round since 35 (prior sub-bullets stay byte-identical; the new sub-bullet narrows only the count):

- corpus/README.md §Frontier gains, after the round-41 sub-bullet:
  > *Partly discharged round 42 (2026-10-26):* `knowledge/tb2-circuit-fibsqrt-grader.md` reads and executes an eighth Terminal-Bench 2.0 task's scoring code (`circuit-fibsqrt/tests/test_outputs.py` @ `2fd12b88`; S125, S126, S127) against its `instruction.md`, probe `plans/fibsqrt_probe.py`, receipt `corpus/evidence/round42/fibsqrt-probe.txt` (`cases=16 observed_pass=7 observed_fail=9 mismatches=0`; `regrade cases=16 differ=0`). The graded state is a class the lane had not executed before: a data artefact — a gate netlist at `/app/gates.txt` — executed by a grader-owned simulator, `tests/sim.c`, which the grader compiles at grading time (`gcc -O3 /tests/sim.c -o sim` in the cwd) and runs as `/app/sim N` on a fixed 28-value table (max 48401) against the test file's own `fib(isqrt(n)) % 2^32` model, so a 1195-line lookup circuit for exactly the 28 graded inputs passes 3 of 3 while the instruction's own examples print 0, padding to 31999 lines passes while 32000 fails only the size test, comment lines/reversed order/CRLF pass, trailing spaces fail, a planted `/app/sim` is overwritten by the grader's compile, and a directory named `gates.txt` fails. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (8 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.

- corpus/README.md coverage map gains an eighth bullet after :269 (`Terminal-Bench 2.0 task grader (eighth task, grader-compiled-simulator class)` … `8 of the 89 TB2 task graders`), a `knowledge/tb2-circuit-fibsqrt-grader.md` index row, and a `### Round-42 evidence` section (per the frozen claims' C2 surface: README index row + coverage bullet + §Frontier narrowing (8 of 89) + PROVINCE paragraph).
- PROVINCE.md gains a `## Round42 partial frontier admission (2026-10-26)` paragraph after the Round41 block, ending `remaining 81 TB2 task graders (89 carry tests/test.sh; 8 are read)` — the C2 counter's V9 requires PROVINCE to name both `circuit-fibsqrt` and `tb2-circuit-fibsqrt-grader.md`, and README §Frontier to name `circuit-fibsqrt` (plans/round42_c2_verify.py docstring, V9).

## 3. Self-assessment mismatch count (SCORECARD / SHONEN / README vs repo state)

n = **1**:

1. **SCORECARD.md:1710-1713** (`### Planned (round 42) — corrected`, Coverage bullet). Two sub-claims on these lines no longer match the frozen repo state: `:1711` "`plans/round42_c2_verify.py` = round-41's V1–V8 re-pointed" and `:1713` "do-nothing control `checks=8 defects>=4`". The frozen counter runs **nine** checks — V1–V8 plus V9 (counter docstring `plans/round42_c2_verify.py:8` "prints `checks=9 defects=0`"; check list `:327` `("V7"…)("V8"…)("V9"…)`), and the committed do-nothing control prints `checks=9 defects=6` (`.ufo/waves/round-42/claims/control-c2-nothing.txt`). The freeze (round-41 closure R3 / considerthese proposal 2 added V9 after the plan was written) superseded this line; nothing in SCORECARD records the update. Fix at integration: one appended erratum line (the file's own rubric demands every pointer re-runs; do not rewrite the plan block).

Lines checked and found **true** at the current tip (not counted):

- SCORECARD.md:1529 heading `a seventh TB2 grader executed` — `ls corpus/knowledge/tb2-*.md | wc -l` → 7.
- SCORECARD.md:1540 (round-41 C2 row) `knowledge files/index rows 47→48, SOURCES 114→117` — `ls corpus/knowledge | wc -l` → 48; `grep -c '^| \`knowledge/' corpus/README.md` → 48; `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 117.
- SCORECARD.md:1573 `Registry 114 → 117 (tier A +2, tier B +1)` — S122/S123 tier A, S124 tier B (corpus/SOURCES.md:137-139).
- corpus/README.md:269 `7 of the 89` and :356 `7 of 89 read` — 7 tb2 knowledge entries exist; the fibsqrt entry is absent at this pre-landing tip (`test -e corpus/knowledge/tb2-circuit-fibsqrt-grader.md` → ABSENT), so both lines are accurate today and are superseded only by the appended round-42 bullets (they remain historically true).
- SHONEN.md:5,7,9,11 — all four items carry `[~]`; no state claims to mismatch.
- README.md (lane root) — 15 lines, no quantitative self-assessment.

Temporal caveat for the L1: the count n=1 is measured at the wave-1 tip (freeze `bc856d80…` landed; wave-1 integration not yet). After landing, README :269/:356-style lines stay true as history (append-only), and the new SCORECARD round-42 row must print `checks=9`, not the planned `checks=8`.

## Risks

- The new §Frontier sub-bullet must keep the standing exclusions (not the task image, not a harness run, not contamination, not model behaviour) or it overclaims beyond the frozen C2 surface.
- Count consistency: 89 − 8 = 81 "remaining"; the round-41 paragraph keeps its own historical 82/7.
- The SCORECARD fix must be an append-only erratum; rewriting the plan block would break the file's audit pattern.
- SOURCES S125–S127 are not yet in the registry at this tip (117 rows, last S124); the L1's open receipts (claims file: opened 2026-10-26 17:08 -03, digests equal to captures — re-verified against SHA256SUMS above) land with the entry.

## Verification (commands run, this seat)

- `ls corpus/knowledge/tb2-*.md | wc -l` → 7; `ls corpus/knowledge | wc -l` → 48.
- `grep -cE '^\| *S[0-9]{3,} *\|' corpus/SOURCES.md` → 117; `grep -nE '^\| *S12[5-7]' corpus/SOURCES.md` → no output (rows not yet landed).
- `grep -c '^| \`knowledge/' corpus/README.md` → 48; `grep -c '^| \`lessons/' corpus/README.md` → 33.
- `cat corpus/evidence/round42/tb2-circuit-fibsqrt/SHA256SUMS` vs `sha256sum` of the three frozen files → test_outputs.py `6117b8ed…`, instruction.md `a7f50026…`, sim.c `700645ac…` (match S125–S127 pins and the receipt header `fibsqrt-probe.txt:2-4`).
- `tail -8 .ufo/waves/round-42/claims/control-c2-nothing.txt` → `checks=9 defects=6`, `PREDICATE C2 fail`, envelope end line.
- `grep -n 'checks=9\|("V9"' plans/round42_c2_verify.py` → docstring :8, check list :327.
- Receipt `corpus/evidence/round42/fibsqrt-probe.txt:23-24` → `cases=16 observed_pass=7 observed_fail=9 mismatches=0` / `regrade cases=16 differ=0`.
- No counter/battery/fixture run was needed for this check, so the Q32 bwrap envelope was not invoked; no writes outside this report and its sibling dir.

VERDICT: frontier-new-mismatches-1
