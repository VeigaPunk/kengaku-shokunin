# R46ScribeC3Index — kengaku round 46 wave 1, C3 index lines (`polyglot-c-py`)

Seat: scribe (leaf; no subagents, no counter/fixture/probe run, no lane write). C3 prose surfaces only: README
index row, README coverage-map bullet, README §Frontier narrowing (`11 of 89` → `12 of 89`), PROVINCE paragraph.
Frozen inputs were read first and left untouched: `plans/round-46-claims.md` (C3, `:92-129`), base tip `fd4129e`,
round-45 closure `64ba838`, and the round-45 precedent commit `7d062c0`.

**No instrument ran.** No counter, fixture build or probe was executed, so **no ENVELOPE lines apply** — the
envelope gates counter/fixture/probe runs, and this seat ran none. No file outside
`.ufo/waves/round-46/w1/R46ScribeC3Index{,.md}/` was written; scratch was created only to hold eight `curl`
downloads of the pinned upstream task and was deleted at the end.

## Axes named (before drafting)

| axis | this seat can move | how it moved |
|---|---|---|
| **coverage** | C3's claim is coverage; these four lines are the surface a reader lands on | 4 paste-ready insertions, each anchored at a byte-verified line, carrying `file:line` facts and no adjectives |
| **adjacency** | each insertion must sit where the round-45 landing put its twin, so the pattern stays visible | anchors chosen at `README:78` (row 11 → row 12), `README:306` (bullet 11 → 12), `README:430` (sub-bullet 45 → 46), `PROVINCE:646` (EOF) |
| calibration / depth / novelty / operability / freshness | not this seat's | untouched: no counter run, no claim upgraded, no admission stated |

## Deliverables (4 assigned + 1 optional proposal)

| # | item | draft file (under `.ufo/waves/round-46/w1/R46ScribeC3Index/`) | sha256 |
|---|---|---|---|
| 1 | `corpus/README.md` knowledge **index row** (eleventh → twelfth) | `01-readme-index-row.md` | `27b8fdbf8c264bfe61af8dd2b50ffd7a10fab7b1a7bc76c8677becec0af40377` |
| 2 | `corpus/README.md` **§Frontier** sub-bullet (`11 of 89` → `12 of 89`) | `02-frontier-bullet.md` | `c6a251c34e8a74aa70a7e9c2853de1d816988afb27a59e27a42ccc11cf74007e` |
| 3 | `corpus/README.md` **§Coverage map** bullet (twelfth task) | `03-coverage-map-bullet.md` | `c8dd8ccfec8c621606042bbcd9171a53ee373ce9e2d929a8f501c2e27db35b13` |
| 4 | `PROVINCE.md` round-46 paragraph | `04-province-paragraph.md` | `fa288175350002102c33b274193612794d9512e107ed222fcc3e19c4c82884db` |
| (5) | `corpus/README.md` `### Round-46 evidence` section — **not assigned, L1's call** | `05-readme-round46-evidence-OPTIONAL.md` | `64b717cae2cedbf0785128c0adc83dc2d39448959d55efda55b018f1770142df` |

Each draft file carries: the anchor (line, `wc -c`, sha256, neighbour line), the unified diff, the gate check the
text is written against, and the paste preconditions. The pinned-read receipt is `PINNED-READS.txt`.

## Anchors found (read-only; every hash recomputed)

```
cd /home/vgpnk/Projects/shokunin/kengaku-shokunin
for n in 78 79 306 307 430 431 432 635; do printf "README:%s " $n; sed -n "${n}p" corpus/README.md | wc -c; \
  sed -n "${n}p" corpus/README.md | sha256sum | cut -d' ' -f1; done
sed -n '646p' PROVINCE.md | wc -c; sed -n '646p' PROVINCE.md | sha256sum
```

| surface | line | `wc -c` (incl. `\n`) | sha256 | neighbour |
|---|---|---|---|---|
| README knowledge index, last knowledge row (`tb2-password-recovery-grader.md`) | 78 | 1044 | `654488e4fee37ed7f3f8981ef17a52586d57f7b7b88fded8d470b9562ed6c4b4` | `:79` = `\| \`lessons/round-1.md\` …` (`3307072e…`) |
| README §Coverage map, eleventh-task bullet (last bullet) | 306 | 430 | `056c9c05c983ab8c7e93a1d180eb9ffe475c37cc7c46937621729b6f0f889ef8` | `:307` = `## Open gaps` (`3d89f2ee…`) |
| README §Frontier, round-45 sub-bullet (last of its parent) | 430 | 1109 | `4612310021695ee3a9a581522ab44b7b1d995fbd0225ab0798c687e8337f114f` | `:431` empty (`01ba4719…`), `:432` = `- **Contamination transparency cards**` (`ff515a86…`) |
| README EOF (last line, `refusals45` evidence bullet) | 635 | 302 | `eb445306a48109521becc73a4bd864cd083b6bba9268a15860a315ae4c8f4d99` | file ends at 635 |
| PROVINCE round-45 paragraph (last line of file) | 646 | 744 | `ca1542cf2f8327274164baceff20227dce35cad0db581a93fce1b90d3c54ac1f` | file ends at 646 (no trailing section) |

Section geometry: `## Coverage map` at `:269`, bullets `:271-306`, `## Open gaps` at `:307`; `## Frontier` at
`:322`, its five top-level bullets at `:327`, `:432`, `:434`, `:439`, `:440`; round-44/45 discharge entries are
already inside the `:327` chain.

## The insertion texts (each one physical line)

### 1 — `corpus/README.md`, insert after `:78`

```
| `knowledge/tb2-polyglot-c-py-grader.md` | A twelfth Terminal-Bench 2.0 task grader read and executed, and the first exemplar of the dual-runtime single-source class: `polyglot-c-py` grades **one file run two ways** — `python3 /app/polyglot/main.py.c N` and `gcc /app/polyglot/main.py.c -o /app/polyglot/cmain && /app/polyglot/cmain N` — both invocations `check=True`, both stdouts `.strip()`ped and compared to one literal at N in {42, 10, 0} (`test_outputs.py:27,30-46`), only after `os.listdir("/app/polyglot") == ["main.py.c"]` exactly (`:17-20`); the listing runs before the grader's own compile (`:23-25`) writes `cmain` into that same directory, so a second grading pass in one container fails on the grader's own artefact; no other N, no timing, no source inspection, and the `instruction.md:9` version pins are unasserted (`environment/Dockerfile:6` installs `gcc` unpinned); `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`; the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: <<IDS>>; captures + `SHA256SUMS` in `evidence/round46/tb2-polyglot-c-py/`; receipt `evidence/round46/polyglot-c-py-probe.txt`; executed under `bwrap` |
```

### 2 — `corpus/README.md`, insert after `:430` (two-space indent, inside the `:327` parent chain)

```
  - *Partly discharged round 46 (2026-10-27):* `knowledge/tb2-polyglot-c-py-grader.md` reads and executes a twelfth Terminal-Bench 2.0 task's scoring code (`polyglot-c-py/tests/test_outputs.py` @ `2fd12b88`; <<IDS>>) against its `instruction.md`, probe `plans/polyglot_c_py_probe.py`, receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`. The graded artefact is one source file executed by two toolchains — `python3 main.py.c N` and `gcc main.py.c -o cmain` then `./cmain N` — with both stdouts compared to one literal at three fixed inputs, the first dual-runtime class in this lane, and the first whose exact-directory check the grader's own compile invalidates on a second pass. `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`. The "Terminal-Bench 2.0's" clause is **narrowed for that one task only**; it stays open for the remaining TB2 task graders (12 of 89 read), for any SWE-bench Pro V2 grader beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the task image (never pulled) or a harness run, not contamination, not model or agent behaviour.
```

### 3 — `corpus/README.md`, insert after `:306`

```
- **Terminal-Bench 2.0 task grader (twelfth task, dual-runtime single-source class)**: covered at source-code depth and executed offline (round 46, 2026-10-27) — knowledge/tb2-polyglot-c-py-grader.md; <<IDS>>; probe `plans/polyglot_c_py_probe.py`, receipt `evidence/round46/polyglot-c-py-probe.txt`. A twelfth instance of the same ground (12 of the 89 TB2 task graders; not breadth, and no quality claim), on `polyglot-c-py` only: the graded artefact is a single source file that must run as a Python script and compile and run as C, both printing the same literal at three fixed inputs, so the grader's whole verdict is one listing equality plus three doubly-executed comparisons; the listing check (`tests/test_outputs.py:17-20`) runs **before** the grader's own `gcc -o /app/polyglot/cmain` (`:23-25`) writes a second directory entry, so the grader is not idempotent in one container and its own second pass fails; `cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`. Not the task image (never pulled), not a harness run, not contamination.
```

### 4 — `PROVINCE.md`, append after `:646` (blank line first, one physical line, no trailing blank)

```
**Round 46 (2026-10-27).** `knowledge/tb2-polyglot-c-py-grader.md` reads and executes a twelfth Terminal-Bench 2.0 task's scoring code — `polyglot-c-py/tests/test_outputs.py` @ `2fd12b88` with `tests/test.sh`, `instruction.md`, `environment/Dockerfile`, `README.md`, `solution/solve.sh`, `task.toml` and `.gitignore` (<<IDS>>) — over <<C>> frozen end states (`cases=<<C>> observed_pass=<<P>> observed_fail=<<F>> mismatches=0`, `regrade cases=<<C>> differ=0`), run under the `bwrap` envelope. The graded artefact is one polyglot source file that must run as a Python script and compile as C, each printing the same literal at three fixed inputs, after an exact-directory listing the grader's own compile then invalidates: the first dual-runtime exemplar in this lane. Polyglot construction as a technique, and how an agent should build the file, stay the task's and the authors' business — not this lane's.
```

## The one substitution, three files, five slots

`corpus/evidence/round46/polyglot-c-py-probe.txt` does not exist at draft time (`ls corpus/evidence/round46/` →
absent), and `plans/pkg-spec-r46.json` does not exist either, so **no draft states an observed count or an id range**.
Placeholders, all mechanical, none guessable:

| placeholder | source | rule |
|---|---|---|
| `<<C>>`, `<<P>>`, `<<F>>` | the probe receipt's summary line | copied, not re-typed; `cases=`/`observed_pass=`/`observed_fail=`; the `--dry` table's `predicted_*` values are **not** observations |
| `<<IDS>>` | `plans/pkg-spec-r46.json` → `rows` keys | the enumerated comma list (`S166, S167, …`) in id order, every key once |

`mismatches=0` is fixed text: a non-zero `mismatches` makes the receipt defective by the frozen kill rule, and then
none of the four insertions may be pasted.

## Findings (evidence-bearing; each cheap to act on before integration)

1. **V9 forces the PROVINCE paragraph onto one physical line.** `plans/round45_c2_verify.py:326`:
   `any(TASK in l and name in l for l in province.splitlines())` — `polyglot-c-py` and
   `tb2-polyglot-c-py-grader.md` must share a `splitlines()` element. Rounds 35–43 wrote wrapped PROVINCE prose
   (`:570`-style), so a writer copying that style fails with text that reads identically. Item 4 is one line.
2. **The §Frontier move is an append, not an in-place rewrite.** `corpus/README.md:425` records round 44's own
   count (`9 of 89 read`); `:430` records round 45's (`11 of 89 read`). Editing `:425` would rewrite round 44's
   observed record. Item 2 appends a round-46 sub-bullet whose clause reads `(12 of 89 read)`, matching
   `plans/round-46-claims.md:94` ("§Frontier narrowing (11 → 12 of 89)"). Same reading as round-45 seat
   `R45PkgProse` finding 3; reported, not silently chosen.
3. **The coverage map is already out of chronological order, so §Coverage map takes the insert at the end.**
   `sed -n '303,306p'` yields eighth, tenth, ninth, eleventh task. Inserting after `:306` keeps tenth/eleventh/twelfth
   adjacent at the tail; inserting anywhere else gives 8, 10, 9, 12, 11.
4. **`c_readme` (gate P8) constrains two of the four lines more tightly than prose suggests.**
   `plans/pkg_gate.py:31` `INDEX_ROW = ^\|\s*`(knowledge/[^`]+\.md)`\s*\|` → the row must be one unwrapped line;
   `elif not all(sid in rows[0] for sid in p.spec["rows"])` → **every** registry id in that one row; and
   `receipt_rel = p.spec["receipt"].split("/", 1)[1]` with
   `l.startswith("- ") and entry_name in l and receipt_rel in l` → the coverage bullet must carry
   `evidence/round46/polyglot-c-py-probe.txt` **without** the `corpus/` prefix, and the indented §Frontier
   sub-bullet (`  - `) is correctly **not** matched. Failure texts to expect if it is wrong:
   `index rows for knowledge/tb2-polyglot-c-py-grader.md=0`, `index row does not cite every registry row`,
   `no coverage bullet naming the entry and its receipt`.
5. **The entry file and the index row must land in the same commit.** `c_readme` ends with
   `files != indexed` → `knowledge files=N index rows=N`; adding `tb2-polyglot-c-py-grader.md` without item 1 fails
   it, and item 1 without the entry fails it the other way. Round 45's P8 failed exactly this way before the L1
   landed the row (`.ufo/waves/round-45/w1/R45PkgEntry.md:118`).
6. **`R46ScoutC3Grader.md`'s line numbers are off by three against the pinned file.** The scout cites
   `test_outputs.py:7` for `def test_fibonacci_polyglot()`, `:14-15` for the listing assert, `:26` for `test_cases`,
   `:32` for the combined assert. The file at that URL (sha256 `b94a7a98…`, 46 lines, re-fetched twice) has them at
   `:10`, `:17-20`, `:27`, `:44-46`. Any knowledge entry or SOURCES row quoting the scout's numbers is wrong by
   three; my drafts use the verified numbers (`PINNED-READS.txt`).
7. **The grader is non-idempotent in one container, by construction.** `test_outputs.py:17-20` asserts
   `os.listdir("/app/polyglot") == ["main.py.c"]`; `:23-25` then runs `gcc … -o /app/polyglot/cmain`, writing the
   second entry the assertion forbids. A second grading pass over the same directory fails on the grader's own
   artefact. This is the class point the row states — and a design constraint on the C3 probe: its `regrade` leg must
   re-stage a clean `/app/polyglot` per pass, or `differ≠0` will be the grader's property, not a probe defect.
8. **`tests/test.sh` is byte-identical to round 45's.** sha256 `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334`
   for both `polyglot-c-py/tests/test.sh` and `password-recovery/tests/test.sh` (`corpus/SOURCES.md:168`, S153).
   It is harness boilerplate: `uvx -p 3.13 … pytest /tests/test_outputs.py` (`:17-21`) then
   `echo 1|0 > /logs/verifier/reward.txt` (`:23-27`). A C3 SOURCES row that presents it as task-specific evidence
   overstates distinctness — it grades nothing on its own.
9. **The version pins the instruction states are unenforced, and the pytest interpreter is a third one.**
   `instruction.md:9` says "python3 3.12.3 and gcc 13.2.0"; `environment/Dockerfile:6` is
   `RUN apt update -y && apt install -y gcc` (unpinned), `:2` is `FROM ubuntu:24.04`, and `tests/test.sh:17` runs
   pytest under `uvx -p 3.13` — distinct from the graded `python3` subprocess at `test_outputs.py:31`. No assertion
   reads a version; the index row says so in six words.
10. **`solution/solve.sh` is cwd-dependent.** `:10` `mkdir -p polyglot` and `:11` `cat <<'EOF' > polyglot/main.py.c`
    use relative paths; the oracle lands at the graded path only because `environment/Dockerfile:4` sets
    `WORKDIR /app`. Same shape as round 45's `solve.sh` defect, so the probe needs a cwd control if it executes the
    oracle.
11. **`task.toml` sets `allow_internet = true` (`:34`)** with the published image `alexgshaw/polyglot-c-py:20251031`
    (`:29`) and a 900 s verifier timeout (`:22`) — the same internet-reachability fact round 45 recorded for
    `password-recovery`, and material if the entry discusses leakage.

## Touched surfaces

Written: `.ufo/waves/round-46/w1/R46ScribeC3Index.md` (this report) and
`.ufo/waves/round-46/w1/R46ScribeC3Index/{01..05}-*.md` + `PINNED-READS.txt` (6 files, ~18 KB). Nothing in
`corpus/`, `plans/`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md` or any other lane file; no git/jj command of any kind
(the two `git` invocations were `git show` and `git log`, both read-only, and one was `git status --short`).
Scratch `/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Index` held eight `curl` downloads and was deleted with
`plans/scratch_guard.py safe-rm`. No tool installed or upgraded; `~/.local/bin` untouched (no run under the
envelope, because no counter/fixture/probe ran).

## Out of scope, deliberately

- `corpus/knowledge/tb2-polyglot-c-py-grader.md` itself (another seat) and its `## Predictor` section, which
  items 1 names and item 3 relies on.
- `corpus/SOURCES.md` rows from S166 — my `<<IDS>>` is the only coupling; if that seat's row set is 8 rows
  `S166`–`S173`, enumerate them, otherwise enumerate the spec's list. If it renumbers, recut the id list, not the
  sentences.
- `plans/polyglot_c_py_probe.py`, `plans/pkg-spec-r46.json`, `plans/round46_c3_verify.py`, the capture dir and the
  receipt — all wave-1 build work owned by other seats; my four texts name them and must not precede them.
- The LOG/SCORECARD round-46 bullets, and the `### Round-46 evidence` README section (proposed, not assigned — item 5).

## Needs the L1's decision (not mine)

1. Whether the §Frontier count is delivered as an appended sub-bullet (item 2, my reading of `:425`/`:430`) or as an
   in-place edit of `:430`'s `11`→`12` (which would rewrite round 45's record).
2. Whether the optional `### Round-46 evidence` section (item 5) lands at all, and whether its bullets merge with C1's
   and C2's under one heading.
3. Whether "twelfth" is the vocabulary the entry uses (`corpus/README.md:68-78` counts eleventh at round 45); if the
   entry self-describes differently, all four texts move together.

VERDICT: c3-index-lines-4
