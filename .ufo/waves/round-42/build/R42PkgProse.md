# R42PkgProse — C2 prose drafts (kengaku round 42 wave 1, scribe)

Seat: `R42PkgProse` · lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin` · 2026-10-26.
Assignment: four C2 prose paste blocks, drafts only. Nothing in the lane was edited. No git, no jj, no commit, no
network fetch, no tool install, no bwrap run.

Axes named (godspeed): **coverage** (the C2 axis under claim) and **adjacency** (the routing clause), with
**operability** touched only insofar as every block is mechanically checkable by the frozen V9 rules.

## 1. Behaviour — what was produced

Four standalone paste blocks, each with its exact insertion anchor and shape copied from its round-41 predecessor:

| block | target file | anchor | draft | sha256 |
|---|---|---|---|---|
| a1 | `corpus/README.md` | after `:74` (round-41 knowledge row), before `:75` | `.ufo/waves/round-42/build/R42PkgProse/a-readme-index-row.md` §a1 | `5b2388a6…` (file) |
| a2 | `corpus/README.md` | after `:269` (seventh-task coverage bullet), before `:270` `## Open gaps` | same file §a2 | `5b2388a6c621f343b353fc5d3fe4d291248b26ccbf4897477bac3c2601b041f8` |
| b | `corpus/README.md` `## Frontier` | after `:359` (end of round-41 sub-bullet), before `:360` | `.ufo/waves/round-42/build/R42PkgProse/b-readme-frontier.md` | `da2e295cad73b2614ba7bab3a4873159d2b05725a9218e36ab02b7ce92c288c1` |
| c | `PROVINCE.md` | append after `:535` (round-41 wave-2 correction) | `.ufo/waves/round-42/build/R42PkgProse/c-province-round42.md` | `d16b1aba3a4dd4e22888aa540cfcba7631282732f5619ca592fcaa06be01f811` |
| d | `SKILL.md` | append after `:1140` (end of round-41 section) | `.ufo/waves/round-42/build/R42PkgProse/d-skill-decision-table.md` | `ccec360df66f5c2c969567933317509dff1ff639af472f76677b2f8dd6fb201e` |

Content of each block:

- **a1** — one knowledge index row for `knowledge/tb2-circuit-fibsqrt-grader.md`: "An eighth Terminal-Bench 2.0 task
  grader read and executed, and a grader class new to this lane", the gate-list artefact, the grader-time compile, the
  28 fixed inputs (largest 48401), the lookup-28 pass and the 208/20000 print-0 witness, 31999-passes/32000-fails, the
  free comment/reversal/CRLF results, the trailing-space failure, the overwritten fake `/app/sim`, the gates.txt
  directory, `cases=16 observed_pass=7 observed_fail=9 mismatches=0` and `regrade cases=16 differ=0`; third column
  `S125, S126, S127 (terminal-bench-2 @ 2fd12b88)`, plus probe and receipt paths — column shape taken from
  `corpus/README.md:74`.
- **a2** — one coverage-map bullet naming the entry file and `evidence/round42/fibsqrt-probe.txt`, "An eighth instance
  of the same ground (8 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability
  verdict)", with the receipt citations inline — shape taken from `corpus/README.md:263-269`.
- **b** — one `  - *Partly discharged round 42 (2026-10-26):*` sub-bullet inside `## Frontier` naming
  `circuit-fibsqrt`, narrowed to **8 of 89 read**, keeping the three open clauses verbatim in form (remaining TB2
  graders, SWE-bench Pro V2 beyond round 31, runtime task validity) — shape taken from `:343-359`.
- **c** — a `## Round42 partial frontier admission (2026-10-26)` section: core addition, the three-test score, the
  seeding/sandbox mechanics, the simulator mechanics that diverge from `instruction.md:8-9`, every observed case with
  its receipt line, the standard "records how that captured grader answers those synthetic states only" paragraph,
  limits, ordering disclosure, adjacency — and a separate **routing clause** naming digital-logic correctness and C
  simulator semantics as **unowned**, with the exact fleet grep that shows it.
- **d** — `## Simulator-executed data-artefact TB2 grader — round 42` with a ten-row
  `### Decision table — what the grader reads, and what passes it`, a "What a green means here" paragraph, the
  seven-tag V7 label paragraph with case counts, and limits — shape taken from `SKILL.md:1059-1140`.

## 2. Gates checked (mechanically, on the drafts themselves)

- **V9(c)** (`plans/round42_c2_verify.py:309`: one physical line must name both `circuit-fibsqrt` and
  `tb2-circuit-fibsqrt-grader.md`): the `**Core addition:**` line of block c is deliberately unwrapped.
  Check: `awk '/^\*\*Core addition:\*\*/{print index($0,"circuit-fibsqrt")>0 && index($0,"tb2-circuit-fibsqrt-grader.md")>0}' c-province-round42.md`
  → `1`.
- **V9(d)** (task named inside `## Frontier`): block b is inserted inside that section; check
  `awk '/^  - \*Partly discharged round 42/{print "sub-bullet-ok"}' b-readme-frontier.md` → `sub-bullet-ok`.
- **README table well-formedness**: block a1's row has exactly 4 pipes
  (`awk '/^\| `knowledge\/tb2-circuit-fibsqrt-grader.md`/{n=gsub(/\|/,"|"); print "pipes="n}'` → `pipes=4`);
  no `|` inside a cell.
- **Coverage bullet shape**: `awk '/^- \*\*Terminal-Bench 2.0 task grader \(eighth/{print "bullet-ok"}'` → `bullet-ok`.
- **SKILL heading**: `awk '/^## Simulator-executed data-artefact TB2 grader/{print "skill-heading-ok"}'` → `skill-heading-ok`.

**V7 label derivation** (used in block d, not a counter run — the frozen counter is the L1's):
`python3 - <<'EOF'` over `corpus/evidence/round42/fibsqrt-probe.txt`, grouping each `CASE` line's `violates=` tags and
its `observed=`, label = all-fail → `enforced`, all-pass → `unenforced`, mixed → `partly`; output:

```
output-function partly n=15 pass=6 [lookup-28, lookup-28-plus-examples, lookup-28-padded-31999, lookup-28-comment-lines, lookup-28-reversed-lines, lookup-28-crlf]
example-208 partly n=14 pass=5 [5 same ids]
example-20000 partly n=14 pass=5 [5 same ids]
gates-file enforced n=2 pass=0
line-limit enforced n=1 pass=0
line-form unenforced n=1 pass=1 [lookup-28-comment-lines]
last-32-lines unenforced n=1 pass=1 [lookup-28-reversed-lines]
rows 16
```
(Abridged: the second and third rows' passing-id lists were printed in full by the command and are the first row's
list minus `lookup-28-plus-examples`; only the counts `n=`/`pass=` and the ids shown above are needed for block d.)

Frozen tag lines come from `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt:1-7`
(`line-form` `instruction.md:1`, `last-32-lines` `:9`, `gates-file` `:11`, `line-limit` `:11`,
`output-function` `:11`, `example-208` `:12`, `example-20000` `:13`).

**Q32 envelope.** This seat ran **no** battery, counter, fixture build or any sandboxed job, so the mandatory envelope
is not applicable and no `bwrap` line was executed:
`bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent <command>` **— NOT RUN this seat.**
The shared-PATH digests were still taken, at the only two timestamps this seat touched the host:
`date +%T` → `17:21:51` (first command) and `17:25:08` (last command);
`ls -A /home/vgpnk/.local/bin | sha256sum` → `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18  -` at 17:25:08. No
before/after pair is claimed because nothing this seat ran could mutate a PATH directory; the single digest is given
as the observed state at report time.

## 3. Touched surfaces

- Written: `.ufo/waves/round-42/build/R42PkgProse/{a-readme-index-row,b-readme-frontier,c-province-round42,d-skill-decision-table}.md`
  and this report. Under 1 MiB each; no receipt or tree copied into the build dir.
- Read only: `plans/round-42-claims.md` (full), `corpus/evidence/round42/fibsqrt-probe.txt`,
  `corpus/evidence/round42/fibsqrt-dry-cases-freeze.txt`, `corpus/evidence/round42/tb2-circuit-fibsqrt/{instruction.md,
  tests/test_outputs.py, sim.c, gates.txt, Dockerfile, README.md, task.toml, test.sh, SHA256SUMS}`,
  `corpus/README.md`, `PROVINCE.md`, `SKILL.md`, `plans/fibsqrt_probe.py`, `plans/round42_c2_verify.py`,
  `plans/pkg-spec-r42.json`, plus one fleet-wide read-only `grep` over `*/PROVINCE.md */SKILL.md`.
- NOT touched: `corpus/knowledge/` (the entry is another seat's), `corpus/SOURCES.md`, the lane's git index and jj
  state, every frozen instrument in the claims list, `~/.local/bin`, `/usr`, `/etc`, `$HOME`, the fleet root's tracked
  files. No scratch dir was needed: every command was a read or a write into the report subdir.

## 4. Findings an integrator should act on

1. **`corpus/SOURCES.md` has no S125–S127 rows as of this read.** `grep -n "S12[2-7]" corpus/SOURCES.md` returns
   S122 (`:137`), S123 (`:138`), S124 (`:139`) only. Blocks a/b/c cite `S125, S126, S127`; C2's V1/V2 pin them in
   `plans/pkg-spec-r42.json` (`rows.S125/.S126/.S127` with the three sha256 values). The rows must be appended (R4:
   corrections only by a new `supersedes` row) or the citations dangle.
2. **`instruction.md:8-9` are contradicted by the shipped simulator.** `:8` says the first 32 lines come from
   **stdin**; `sim.c:324` reads `argv[1]`. `:9` says "the last 32 lines"; `sim.c:340-347` prints the 32
   **highest-indexed** signals. The receipt's `lookup-28-reversed-lines` (`PPP`, receipt:18) is the executed witness
   that physical line order is irrelevant; the rest is a code read. Block d states both as code reads, not as
   executed claims.
3. **Two instruction requirements are `unenforced` by the frozen case set** — `line-form` (`instruction.md:1`) and
   `last-32-lines` (`:9`): the only case violating each is observed pass (receipt:17, :18). Block d says so with the
   counts; the entry's requirement map must agree row by row with V7.
4. **Baseline is 2 of 3, not 0 of 3**: `nop` is `PPF` (receipt:7) because the shipped example passes existence and
   size. Any "the agent must beat nothing" reading of this task is wrong; only test 3 starts unearned.
5. **The `/app/sim.c` the Dockerfile ships (`Dockerfile:8-9`) is never the compiled source** — test 3 compiles
   `/tests/sim.c` and drops `sim` into the cwd, which is why `fake-sim-script` fails (`PPF`, receipt:21). Do not write
   a bullet that says the grader runs the agent's `/app/sim`.
6. **`test_gates_file_exists` uses `exists()`, not `is_file()`** (`test_outputs.py:9-11`), so a directory passes test 1
   (`gates-is-directory` `PFF`, receipt:22, which names `test_gates_file_size:error=IsADirectoryError`). Coverage
   text that says "a directory fails the existence test" would be false.
7. **Adjacency: unowned, with a named check.** 2026-10-26 17:23:15, from `/home/vgpnk/Projects/shokunin`:
   `grep -rin "digital logic\|logic gate\|logic-gate\|gate-level\|circuit\|C simulator\|compiler semantics"
   --include=PROVINCE.md --include=SKILL.md */PROVINCE.md */SKILL.md` → one sibling hit,
   `mado-shokunin/SKILL.md:1656:  short-circuit-vs-silent-tolerance reading stays UNK.` (different sense);
   `grep -rn "gcc\|clang"` over the same files → `hits=0` outside this lane. No PROVINCE in the fleet declares a
   digital-logic, circuit or compiler/simulator-semantics domain, so block c routes such findings to the orchestrator
   and credits no sibling.
8. **Arithmetic carried forward**: 89 − 8 = 81 remaining TB2 graders, matching the round-41 paragraph's 89 − 7 = 82
   (`PROVINCE.md:507-508` reads "the remaining 82 TB2 task graders (89 carry `tests/test.sh`; 7 are read)"). Keep
   `8 of 89 read` in README §Frontier and `8 are read` in PROVINCE
   consistent at integration.

## 5. Out of scope (deliberately not done)

- `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`, its `## Case table` and `## Requirement map` rows (another seat's);
  `corpus/SOURCES.md` S125–S127 rows (see finding 1).
- Any edit to `corpus/README.md`, `PROVINCE.md`, `SKILL.md` — drafts only, for the L1 to integrate.
- Running `python3 plans/round42_c2_verify.py --lane .` or `plans/fibsqrt_probe.py`; the counter verdict is the L1's
  gate, and re-running the frozen probe would be a second observation, not evidence.
- Prior-art pricing of the lookup-circuit coverage gap (a wave-1 item elsewhere); C1/battery42 work; the round-41
  lesson §5 R1–R5 items beyond the V9 content already carried by claim C2.

## 6. Known limits of these drafts

- Every number is a receipt line or a captured-source line, and the receipts used are the frozen ones; no new
  observation of the grader was made by this seat, so the drafts inherit the probe's own limits (host python3/gcc for
  the image's python 3.13 and Debian gcc, image never pulled, recipes unprivileged, per-case staged `/app`).
- The claim that the grader's compile overwrites a planted `/app/sim` is `test_outputs.py:65-67` + `:119` +
  `Dockerfile:3` read against the `fake-sim-script` `PPF` verdict; it is not a trace of the two writes.
- Tag labels are V7's rule applied to the receipt, not a judge's reading of the instruction prose; `enforced` is a
  property of this frozen 16-case set (two of the seven tags rest on a single case).
- The "8 of 89" narrowing is arithmetic over the claims file's own count of read graders; this seat opened no TB2
  task beyond the three captured files.

## 7. Artifact paths

- `.ufo/waves/round-42/build/R42PkgProse/a-readme-index-row.md`
- `.ufo/waves/round-42/build/R42PkgProse/b-readme-frontier.md`
- `.ufo/waves/round-42/build/R42PkgProse/c-province-round42.md`
- `.ufo/waves/round-42/build/R42PkgProse/d-skill-decision-table.md`
- `.ufo/waves/round-42/build/R42PkgProse.md` (this report)

VERDICT: prose-drafted-4-blocks
