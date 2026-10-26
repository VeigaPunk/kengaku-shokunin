# R43PkgProse — C2 prose drafts (kengaku round 43 wave 1, scribe)

Seat: `R43PkgProse` · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · 2026-10-26.
Assignment: four C2 prose paste blocks, drafts only. Nothing in the lane was edited. No git, no jj, no commit, no
network fetch, no tool install, no `bwrap` run, no `plans/` or `corpus/` instrument executed.

Axes named (godspeed): **coverage** (the C2 axis under claim) and **adjacency** (the routing clause), with
**operability** touched only insofar as every block is answerable to the frozen C2 counter's V7/V9/V10 shape.

## 1. Behaviour — what was produced

Four standalone paste blocks, each with its exact insertion anchor, copied in shape from its round-42 predecessor
(`.ufo/waves/round-42/build/R42PkgProse.md`):

| block | target file | anchor | draft | sha256 |
|---|---|---|---|---|
| a1 | `corpus/README.md` (knowledge index table) | after `:75` (round-42 `tb2-circuit-fibsqrt-grader.md` row), before `:76` (`lessons/round-1.md`) | `R43PkgProse/a-readme-index-row.md` §a1 | row inside `aef16bd5cdd7a884…` (file) |
| a2 | `corpus/README.md` (`## Coverage map`) | after `:271` (eighth-task bullet), before `:272` (`## Open gaps`) | same file §a2 | `aef16bd5cdd7a8846bdfc8c0a84f33891b93a0ed0b1a00eebb2702c0457b7e11` |
| b | `corpus/README.md` `## Frontier` | after `:378` (end of the round-42 sub-bullet), before `:379` (`- **Contamination transparency cards**`) | `R43PkgProse/b-readme-frontier.md` | `0e22247887f15dc490d7f805bbb57d86eaca6f3921031a050afc88d190d8e112` |
| c | `PROVINCE.md` | append after `:568` (end of the round-42 routing paragraph; file is 568 lines) | `R43PkgProse/c-province-round43.md` | `8b2b3681ec5e444c90fa101aeb73d60585741dd57e4f9db1e48313b6f8077fa1` |
| d | `SKILL.md` | append after `:1204` (end of the round-42 section; file is 1204 lines) | `R43PkgProse/d-skill-decision-table.md` | `de9b86fc70489c1027fd44d8f9c4b36c5614f8830439dda31b7d13ba3cb02975` |

Content of each block:

- **a1** — one knowledge index row for `knowledge/tb2-feal-differential-cryptanalysis-grader.md`: "A ninth
  Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane", the in-process module-import
  mechanism (`test_outputs.py:20` build, `:22-25` path order and imports, `:27`, `:29`, `:30`), `feal_module.c:25-51`,
  the six no-key passes with their receipt lines, the 16-bit seed schedule (`feal.c:56-67`), the untimed 45 s oracle
  against `instruction.md:3` and `README.md:35`, `task.toml:22`, the four failures, `cases=12 observed_pass=8
  observed_fail=4 mismatches=0` and `regrade cases=12 differ=0`; third column `S129, S130, S131, S132, S133, S134
  (terminal-bench-2 @ 2fd12b88); probe `plans/feal_probe.py`, receipt `evidence/round43/feal-probe.txt`` — column
  shape from `corpus/README.md:75`.
- **a2** — one coverage-map bullet naming `knowledge/tb2-feal-differential-cryptanalysis-grader.md` and
  `evidence/round43/feal-probe.txt`, "A ninth instance of the same ground (9 of the 89 TB2 task graders; not breadth,
  and no quality, validity, difficulty or gameability verdict)", with receipt citations `:10`, `:12-14`, `:15-20`,
  `:21`, `:22-23` — shape from `corpus/README.md:269-271`.
- **b** — one `  - *Partly discharged round 43 (2026-10-26):*` sub-bullet inside `## Frontier` naming
  `feal-differential-cryptanalysis`, narrowed to **9 of 89 read**, keeping the three open clauses in the round-37..42
  form (remaining TB2 graders, SWE-bench Pro V2 beyond round 31, runtime task validity) — shape from `:362-378`.
- **c** — `## Round43 partial frontier admission (2026-10-26)`: a one-line `**Core addition:**` (unwrapped, for
  V9(c)), the class statement, the mechanism with every `file:line`, the twelve cases with receipt lines, the standard
  "records how that captured grader answers those synthetic states only" paragraph, limits, disclosed ordering, and a
  separate **routing clause** naming cryptanalysis technique and Python import-system semantics as **unowned** with
  the exact sweeps and their outputs.
- **d** — `## In-process module-import TB2 grader — round 43` with the probe's exit semantics spelled out, the class
  paragraph, an **eleven-row** `### Decision table — what the grader reads, and what passes it` citing receipt lines
  10-21, the five V7 labels with counts, and limits — shape from `SKILL.md:1160-1204`.

## 2. Gates checked (mechanically, on the drafts themselves)

All checks are reads of the draft bytes plus two read-only `python3 -c` computations; no counter, probe, battery or
fixture was run (see §5 for the Q32 statement).

- **C2 V9(c)** (`plans/round43_c2_verify.py:319-321`: one physical line must name both the task and the entry file):
  `python3 -c` over `c-province-round43.md` → `c core lines: 1 names both: True`. The `**Core addition:**` line is
  deliberately unwrapped.
- **C2 V9(d)** (task named inside `## Frontier`): `python3 -c` → `b names task: True | 9 of 89: True`.
- **README table well-formedness**: `python3 -c` → `a1 rows: 1 pipes: 4` (no `|` inside a cell, so the row cannot
  split); `a1 has receipt path: True | S129-S134: True`.
- **Coverage-bullet shape**: `python3 -c` → `a2 bullet: True` (`evidence/round43/feal-probe.txt` present in §a2).
- **SKILL headings and table integrity**: `python3 -c` → `d heading: True | decision heading: True`; table rows
  `d table rows: 11 pipes min/max: 5 5` (every row four cells).
- **Receipt citations present**: `d receipt cites: ['10' … '21']`; `a receipt cites: ['10', '15-20', '21', '22-23']`.

**V7 label derivation** (used in block d; the frozen counter is the L1's, this is the same rule applied to the frozen
receipt — `python3 -c` over `corpus/evidence/round43/feal-probe.txt`, grouping each `CASE` line's `violates=` set and
`observed=`):

```
case lines: [(10,'nop'),(11,'oracle-solve-sh'),(12,'wrong-key'),(13,'oracle-off-by-one'),(14,'return-str'),
             (15,'cheat-import-get_keys'),(16,'cheat-always-equal'),(17,'cheat-sysmodules-shadow'),
             (18,'cheat-patch-get_keys'),(19,'cheat-exit-zero'),(20,'cheat-clock-seed'),(21,'slow-oracle-45s')]
TAG attack-file enforced n=1 pass=0 ids=['nop']
TAG recover-key5 partly n=7 pass=4 ids=['nop','wrong-key','oracle-off-by-one','cheat-always-equal',
    'cheat-sysmodules-shadow','cheat-patch-get_keys','cheat-exit-zero']
TAG return-uint32 partly n=2 pass=1 ids=['return-str','cheat-always-equal']
TAG chosen-plaintext unenforced n=6 pass=6 ids=['cheat-import-get_keys','cheat-always-equal',
    'cheat-sysmodules-shadow','cheat-patch-get_keys','cheat-exit-zero','cheat-clock-seed']
TAG time-30s unenforced n=1 pass=1 ids=['slow-oracle-45s']
summary: ['regrade cases=12 differ=0', 'cases=12 observed_pass=8 observed_fail=4 mismatches=0']
```

Frozen tag lines come from `corpus/evidence/round43/feal-dry-cases-freeze.txt:1-5` (`chosen-plaintext`
`instruction.md:1`, `recover-key5` `:1`, `attack-file` `:3`, `return-uint32` `:3`, `time-30s` `:3`).

## 3. Touched surfaces

- Written: `.ufo/waves/round-43/build/R43PkgProse/{a-readme-index-row,b-readme-frontier,c-province-round43,
  d-skill-decision-table}.md` and this report. Largest draft file 8276 bytes; nothing copied from `corpus/`, `plans/`
  or a lane mirror; no receipt over 1 MiB.
- Read only: `plans/round-43-claims.md` (full), `corpus/evidence/round43/feal-probe.txt`,
  `corpus/evidence/round43/feal-dry-cases-freeze.txt`, `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`
  (`SHA256SUMS`, `test_outputs.py`, `test.sh`, `instruction.md`, `feal_module.c`, `feal.c`, `feal.py`, `setup.py`,
  `README.md`, `task.toml`, `Dockerfile`, `solve.sh` in part), `corpus/README.md`, `PROVINCE.md`, `SKILL.md`,
  `plans/round43_c2_verify.py`, `plans/pkg-spec-r43.json`, `plans/feal_probe.py` (exit paths only),
  `.ufo/waves/round-42/build/R42PkgProse.md`, `.ufo/waves/round-43/claims/c2-stage-check.txt`, plus read-only
  fleet-wide `grep`s over `*/PROVINCE.md` and `*/SKILL.md`.
- NOT touched: `corpus/knowledge/` (the entry is another seat's and does not exist yet), `corpus/SOURCES.md`,
  `plans/`, the lane's git index and jj state, `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the fleet root's tracked
  files. No scratch dir was created: every write went into the report subdir, and no fixture repo was needed.

## 4. Findings an integrator should act on

1. **`corpus/SOURCES.md` has no S129–S134 rows as of this read** — `grep -c "^| S" corpus/SOURCES.md` → `121`, `grep
   -o "^| S[0-9]*" corpus/SOURCES.md | tail -3` → `| S126`, `| S127`, `| S128`, `grep -c "^| S129"` → `0`. Blocks a, b
   and c cite S129–S134 (frozen in `plans/pkg-spec-r43.json` `rows.S129…S134` with the six sha256 values, which agree
   with the capture `SHA256SUMS`). The rows must be appended or the citations dangle.
2. **README has no `### Round-41` / `### Round-42` evidence sections** (`grep -n "Round-41 evidence\|Round-42
   evidence" corpus/README.md` → no hit; the evidence list `:487-535` stops at `### Round-40 evidence`). Round 43's own
   `### Round-43 evidence` block, if wanted, is a separate integration item; the a2 coverage bullet does not depend on
   it.
3. **`corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` does not exist yet** (`ls` → absent), so a1/a2/b
   cite an unlanded entry, as in round 42. V9(c) and V9(d) are satisfied by blocks c and b the moment both land; a
   receipt with an unlanded entry still reads `receipt or entry absent` in V7/V9/V10 (`plans/round43_c2_verify.py:250`,
   `:302`, `:356`), so a1/a2 must not be landed without the entry.
4. **The 45 s oracle is the sharpest prose fact and the most likely to be softened by editing.** `instruction.md:3`
   asks under 30 s; `README.md:35` says the test "Confirms the attack completes within the time limit"; the test does
   not time the call (`test_outputs.py:29`) and the only bound is `task.toml:22`'s 1800 s. `slow-oracle-45s` passes
   (receipt:21). Keep that sentence in a1, a2, b, c and d or the entry's four unenforced/partly tags lose their
   witness.
5. **`cheat-always-equal` passes for a language reason, not a grader bug** — `int.__eq__(non-int)` returns
   `NotImplemented` and the reflected `__eq__` decides `test_outputs.py:30`. Block d says this in one clause; a
   reviewer should not "correct" it to "the assert compares loosely". This lane owns the verdict it produces, not
   Python comparison semantics generally (routing clause, block c).
6. **Two of the five V7 tags rest on a single case each** (`attack-file` n=1, `time-30s` n=1) and `return-uint32` on
   two. Block d prints the counts so a reader can see that; the entry's requirement map must agree row by row or V7
   DEFECTs.
7. **Arithmetic carried forward**: 89 − 9 = 80 remaining TB2 graders. Round-42 wrote `remaining 81` / `8 of 89`; blocks
   b and c use `9 of 89 read` and `remaining 80`. Keep them consistent at integration.
8. **Adjacency: unowned, with two named sweeps.** 2026-10-26 from `/home/vgpnk/Projects/shokunin`, per pattern
   `"cryptanalys" "cipher" "differential cryptanalysis" "sys.modules" "import system" "importlib" "python semantics"
   "interpreter semantics"`: `grep -ril "$pat" --include=PROVINCE.md */PROVINCE.md` → **0 files for every pattern**;
   `grep -rin "cryptanalys\|block cipher\|differential cryptanalysis" --include=SKILL.md */SKILL.md` → **no hits**;
   `grep -rin "sys.modules\|import system\|import machinery" --include=SKILL.md */SKILL.md` → **no hits**. Near-misses
   only: `kotodama-shokunin/SKILL.md:24` ("a cipher of English", conlang), `kaidoku-shokunin/SKILL.md:893` (pcap
   encryption), `chousa-shokunin/SKILL.md:116` (`importlib` leaving `__pycache__` beside its own harness candidate). No
   sibling is credited; block c routes such findings to the orchestrator.

## 5. Q32 envelope

This seat ran **no** battery, counter, fixture build, probe or any sandboxed job, so the mandatory envelope is not
applicable and no `bwrap` line was executed:
`.../claims/envelope.sh "$S/env" <command>` **— NOT RUN this seat** (no command this seat ran can write a file, and
none was run under a sandbox).

The shared-PATH state was still sampled at the two timestamps bracketing all work, both from `bash`:
`date +%T` → `19:08:53` and `19:10:59`; `ls -A /home/vgpnk/.local/bin | sha256sum` →
`8cf5b1516051e1918a9a8b1df305247ab67f31ec8366f20843ee83b3c2d86d52  -` at both samples (identical). The two read-only
`python3 -c` computations wrote no file (no bytecode: `-c` scripts are not cached) and imported only the standard
library.

## 6. Out of scope (deliberately not done)

- `corpus/knowledge/tb2-feal-differential-cryptanalysis-grader.md` and its `## Case table`, `## Requirement map`,
  `## Mechanism` rows (another seat's; V10's DECISIVE lines are the L1's).
- `corpus/SOURCES.md` S129–S134 rows (finding 1), any `### Round-43 evidence` README section (finding 2).
- Any edit to `corpus/README.md`, `PROVINCE.md`, `SKILL.md` — drafts only, for the L1 to integrate.
- Running `python3 plans/round43_c2_verify.py --lane .` or `plans/feal_probe.py`; the counter verdict is the L1's
  gate, and re-running the frozen probe would be a second observation, not evidence.
- C1/battery43 work, prior-art pricing of differential cryptanalysis on FEAL, the round-42 closure items R1–R6 beyond
  the prose this seat owns.

## 7. Known limits of these drafts

- Every probe number is a receipt line (`corpus/evidence/round43/feal-probe.txt:10-23`); every source-mechanics number
  is a captured-file `file:line` from `corpus/evidence/round43/tb2-feal-differential-cryptanalysis/`. No new
  observation of the grader was made by this seat, so the drafts inherit the probe's limits: host python3/gcc/
  setuptools for the image's python 3.13 under `uvx`, Debian gcc and setuptools 80.9.0; image never pulled; pytest not
  run (the harness maps the one test onto pytest's exit status); recipes unprivileged; per-case staged `/app` and
  `/tests`; the twelve cases are constructed modules, not agents.
- "six of the eight observed passes never recover a key" counts the six cheat cases against the eight `observed=pass`
  lines; it is not a claim that the other two (the oracle and the 45 s oracle) are the only genuine attacks.
- The build-failure row in block d has **no** receipt case behind it and is labelled "code read only" — `:20` prints
  the build output and never asserts it, so a failed build can only surface as an `ImportError` at `:25`.
- Tag labels are the V7 rule applied to the frozen receipt, not a judge's reading of the instruction prose;
  `enforced` is a property of this frozen 12-case set (two tags rest on one case).
- The "9 of 89" narrowing is arithmetic over the claims file's own count of read graders; this seat opened no TB2 task
  beyond the captured files.

## 8. Artifact paths

- `.ufo/waves/round-43/build/R43PkgProse/a-readme-index-row.md` (`aef16bd5cdd7a884…`)
- `.ufo/waves/round-43/build/R43PkgProse/b-readme-frontier.md` (`0e22247887f15dc4…`)
- `.ufo/waves/round-43/build/R43PkgProse/c-province-round43.md` (`8b2b3681ec5e444c…`)
- `.ufo/waves/round-43/build/R43PkgProse/d-skill-decision-table.md` (`de9b86fc70489c10…`)
- `.ufo/waves/round-43/build/R43PkgProse.md` (this report)

VERDICT: prose-drafted-4-blocks
