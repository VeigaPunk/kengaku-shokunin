# R46ScribeC3Rows — C3 SOURCES rows S166–S172 (kengaku round 46, wave 1, scribe)

## Behaviour

Drafted seven SOURCES registry rows, S166–S172, for the pinned TB2 `polyglot-c-py` package at
`terminal-bench-2` @ `2fd12b88aafdd04a52c298e3940bcb189f9766d6`, in the 11-cell schema of S149–S156: tier `A`,
status `mined`, opened `2026-10-27`, recheck `180d`, used-by `corpus/knowledge/tb2-polyglot-c-py-grader.md`;
kind `code` for the grader/harness/image/oracle, `docs` for instruction.md / README.md / task.toml (precedent
S139/S143/S146; the S156 `code`→`docs` correction is the same rule, C2 row defect 12).

**Id assignment follows the map pinned in `plans/pkg-spec-r46.json`** as drafted at
`.ufo/waves/round-46/w1/R46ExecC3Spec/pkg-spec-r46.json` and cited by the C3 entry seat — S166 test_outputs.py,
S167 test.sh, S168 instruction.md, S169 solve.sh, S170 Dockerfile, S171 task.toml, S172 README.md. My first draft used
a different order (instruction before test.sh); the rows were renumbered and re-gated, and only the `| S1NN |` id field
moved. Row bodies, anchors, digests and kinds are unchanged.

The package inventory was proven from the repository's own tree listings, not guessed: root
`.gitignore, instruction.md, README.md, task.toml` plus `environment/`, `solution/`, `tests/`, and each of the three
subdirectory listings returns exactly one file — so the complete content set is 8 captures, 7 of which carry a row.

| row | capture | upstream path | bytes | lines | sha256 | quotes (line:words) |
|---|---|---|---|---|---|---|
| S166 | test_outputs.py | tests/test_outputs.py | 1564 | 46 | `b94a7a98…81ddec` | 18:5, 27:8, 44:9 |
| S167 | test.sh | tests/test.sh | 608 | 29 | `4770437e…16e6c334` | 19:2, 26:4 |
| S168 | instruction.md | instruction.md | 339 | 9 | `a57c0c0e…a4ef96` | 3:3, 5:7, 9:7 |
| S169 | solve.sh | solution/solve.sh | 1386 | 57 | `e768453a…56bf0` | 12:4, 14:4, 46:6 |
| S170 | Dockerfile | environment/Dockerfile | 195 | 6 | `2eb537f2…5d5098a` | 2:2, 6:9 |
| S171 | task.toml | task.toml | 850 | 41 | `d31b9f60…ac9a9ea` | 19:3, 29:3, 34:3 |
| S172 | README.md | README.md | 1302 | 24 | `591e27f9…e92881` | 21:9, 22:7, 24:6 |

`.gitignore` (177 B, 23 lines, `9a8dd8d9…`) is captured but has **no row**, exactly as round 45 captured the
password-recovery `gitignore` without one: it is not task content, it is the shared Harbor template (see F2).

Every URL was re-opened live today; all eight returned `200` and the body bytes hash to the row's `sha256`:

```
instruction.md        200 339   sha256=a57c0c0e…  .../polyglot-c-py/instruction.md
task.toml             200 850   sha256=d31b9f60…  .../polyglot-c-py/task.toml
README.md             200 1302  sha256=591e27f9…  .../polyglot-c-py/README.md
.gitignore            200 177   sha256=9a8dd8d9…  .../polyglot-c-py/.gitignore
environment/Dockerfile 200 195  sha256=2eb537f2…  .../polyglot-c-py/environment/Dockerfile
tests/test_outputs.py 200 1564  sha256=b94a7a98…  .../polyglot-c-py/tests/test_outputs.py
tests/test.sh         200 608   sha256=4770437e…  .../polyglot-c-py/tests/test.sh
solution/solve.sh     200 1386  sha256=e768453a…  .../polyglot-c-py/solution/solve.sh
```

Full receipt (complete 64-hex digests and URLs): `R46ScribeC3Rows/fetch-receipt.txt`. A second, independent fetch
after the renumbering returned the same eight digests byte for byte.

## Gate — `plans/anchor_line_check.py` on a scratch clone with the rows appended

Method: `git clone -q --shared` of the lane into scratch (verified `rev-parse --show-toplevel` = the clone), captures
placed at `corpus/evidence/round46/tb2-polyglot-c-py/` with a round-45-format `SHA256SUMS`, the seven rows appended in
id order after S156, both `git add`ed (no commit) so the tool's `git ls-files` census sees them. Runner: the round-46
envelope. Tool sha256 `35d02dc5…` (matches the C2 claims line).

With the rows appended — final, renumbered run:

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/lane/plans/anchor_line_check.py --lane /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/lane
ENVELOPE start 02:14:51 cwd=/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows
UNCAPTURED S093
UNCAPTURED S103
UNCAPTURED S104
UNCAPTURED S110
ROW S108 state=live defects=words:1
ROW S149 state=live defects=range:1
ROW S150 state=live defects=words:1
ROW S151 state=live defects=range:1,words:1
ROW S152 state=live defects=line:1,words:1
ROW S153 state=live defects=line:1,range:1,words:1
ROW S154 state=live defects=line:1,range:1
ROW S155 state=live defects=range:1,words:1
ANCHORLINE rows=156 cited=46 captured=42 uncaptured=4 defective=8 repaired=0 live=8 cells=14
ENVELOPE end 02:14:53 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

**No row S166–S172 appears in any `ROW … state=live` line** — none of the seven is defective on line, range or words.
The eight live rows are the round-45 rows C2 owns (S108, S149–S155), unchanged in count and cell count (`cells=14`).
The pre-renumbering run (02:10:26–02:10:29, `lane` clone #1) printed the same `ANCHORLINE` line and the same envelope
digest; the renumber did not change any measurement.

Before value, same tool, pristine clone of the lane at `fd4129eb` (`R46ScribeC3Rows/gate-base.txt`):

```
ANCHORLINE rows=149 cited=39 captured=35 uncaptured=4 defective=8 repaired=0 live=8 cells=14
ENVELOPE end 02:10:49 exit=1 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Delta = +7 rows, +7 cited, +7 captured, defective 8→8, live 8→8. Tool liveness, `--selftest`
(`R46ScribeC3Rows/gate-selftest.txt`):

```
SELFTEST RED rc=1 want_rc=1 ok :: ANCHORLINE rows=1 cited=1 captured=1 uncaptured=0 defective=1 repaired=0 live=1 cells=2
SELFTEST GREEN rc=0 want_rc=0 ok :: ANCHORLINE rows=2 cited=2 captured=2 uncaptured=0 defective=1 repaired=1 live=0 cells=0
SELFTEST JUNK rc=1 want_rc=1 ok :: ANCHORLINE rows=2 cited=2 captured=2 uncaptured=0 defective=2 repaired=0 live=2 cells=4
SELFTEST pass
ENVELOPE end 02:15:17 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

## V12 — the landed C3 counter over the same seven rows

`plans/round46_c3_verify.py` landed after my first gate run, so I measured its own anchor rule against these rows
instead of relying on anyone's summary: I imported the counter module itself (from the lane, read-only), built its
`Pkg` over the spec's row map (`R46ExecC3Spec/pkg-spec-r46.json`), a capture dir holding the eight files, and
`rows.md` as the registry, then called its `v1` and `v12` functions. Driver: `R46ScribeC3Rows/v12-run.txt`.

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/v12check.py /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows
ENVELOPE start 02:32:28 cwd=/home/vgpnk/Projects/shokunin
V1 ok listed=8 wrong=0 extra=0
V12 ok rows=7 defective=0 live=0
ENVELOPE end 02:32:30 exit=0 local_bin_content_before=7747d38e2042d398 after=7747d38e2042d398 unchanged
```

What that run establishes, and what it rules out. `v12` (`plans/round46_c3_verify.py:522-575`) iterates **every**
quote in a cell with the same `:N "quote" (K words)` regex as the grade tool, unescapes `\"` before comparing, checks
one `<file>:<a>-<b>` range against the file's `splitlines` length, checks the word count, and requires exactly one
`sha256 <hex>` token in the row line that resolves to exactly the spec row's capture name. There is **no**
one-quote-per-cell clause, **no** ban on inner double quotes and **no** word floor for registry cells — the `(3, 25)`
floor is `entry_rules.quote_words` in the spec (`pkg-spec-r46.json:61`) and applies to the entry's located quotes, not
to these anchors. The strict reading I was warned about does not exist in the code that scores C3; both my cells and
the spec seat's alternative set pass. A blend of the two would not: quote text, word count and range belong to one
cell, so the L1 lands one whole set.

## Independent re-derivation of every anchor (not trusting the gate)

Line, substring and word count re-checked by hand per quote with `sed -n Np`, `grep -F` and `wc -w`
(`R46ScribeC3Rows/quotes.tsv`, 19 quotes, `FAILS=0`, re-run after the renumbering):

```
S166 test_outputs.py:18 words=5/5 hit=1 ok        S169 solve.sh:46 words=6/6 hit=1 ok
S166 test_outputs.py:27 words=8/8 hit=1 ok        S170 Dockerfile:2 words=2/2 hit=1 ok
S166 test_outputs.py:44 words=9/9 hit=1 ok        S170 Dockerfile:6 words=9/9 hit=1 ok
S167 test.sh:19 words=2/2 hit=1 ok                S171 task.toml:19 words=3/3 hit=1 ok
S167 test.sh:26 words=4/4 hit=1 ok                S171 task.toml:29 words=3/3 hit=1 ok
S168 instruction.md:3 words=3/3 hit=1 ok          S171 task.toml:34 words=3/3 hit=1 ok
S168 instruction.md:5 words=7/7 hit=1 ok          S172 README.md:21 words=9/9 hit=1 ok
S168 instruction.md:9 words=7/7 hit=1 ok          S172 README.md:22 words=7/7 hit=1 ok
S169 solve.sh:12 words=4/4 hit=1 ok               S172 README.md:24 words=6/6 hit=1 ok
S169 solve.sh:14 words=4/4 hit=1 ok
FAILS=0
```

Range vs real line count (`wc -l`, `splitlines`, trailing-newline flag):

```
Dockerfile      wc -l=6  splitlines=6  cited=1-6   trailing_nl=True   <- range NOT parsed by either checker
README.md       wc -l=23 splitlines=24 cited=1-24  trailing_nl=False
instruction.md  wc -l=9  splitlines=9  cited=1-9   trailing_nl=True
solve.sh        wc -l=57 splitlines=57 cited=1-57  trailing_nl=True
task.toml       wc -l=41 splitlines=41 cited=1-41  trailing_nl=True
test.sh         wc -l=29 splitlines=29 cited=1-29  trailing_nl=True
test_outputs.py wc -l=46 splitlines=46 cited=1-46  trailing_nl=True
```

Measured, not assumed: the range regex in both checkers (`anchor_line_check.py:28`, `round46_c3_verify.py:146`) is
`[\w./-]+\.[A-Za-z0-9]+:(\d+)-(\d+)`, which needs a `name.ext:` token. `RANGE.search("Dockerfile:1-6")` → `None`
(measured), so **S170's range leg is skipped by both** while `test.sh:1-29` and `README.md:1-24` parse and are
checked. The token stays in the cell because it is true and human-readable, and because round 45's S152 Dockerfile row
has the same shape (its defect report is `line:1,words:1`, no range cell); but no one should read "range verified" for
S170.

README.md is the only non-newline-terminated capture: 24 lines of content, `wc -l` reports 23 because the last line
(`4. Test cases: …`) has no newline. The cited range is `1-24`, the only range that contains a `:24` quote under the
gate's `splitlines` rule; the gate accepts it (row not defective). The C3 entry seat reached the same conclusion
independently.

## Cross-check with the capture seat (independent second fetch)

`R46ExecC3Capture` fetched the same eight files independently and reports 8/8 agreement with my digests and byte
counts, plus legs I did not run: 8/8 capture == `git cat-file blob` at the pin, 8/8 refetch identical, tree = exactly
eight `100644` blobs (no symlink, submodule or exec bit, and no `environment/setup.sh`), and `main` == the pin at
access time (drift 0/8 — degenerate, the pin is the current tip). Those are **their** measurements, quoted as
reported; my own evidence is the `curl -w`/sha256 table above. Their capture table:
`.ufo/waves/round-46/w1/R46ExecC3Capture/capture-table.txt`.

One artefact diverges and the L1 must pick one: the two independently generated `SHA256SUMS` carry the **same eight
digests** but different line order — mine is C-sorted (`Dockerfile, README.md, gitignore, …`, sha256 `59e473bc…`,
matching the round-45 file's ordering), theirs is locale-sorted (`gitignore, README.md, …`, sha256 `a44b38ea…`). The
gate is order-free (`c_captures` at `pkg_gate.py:152-176` builds a name→digest dict), so the two files are
gate-equivalent and the L1 may land either — but exactly one, with its digest pinned once in `plans/pkg-spec-r46.json`.
The entry seat proposes the capture seat's file as canonical; that is a coordination choice, not a measurement. They
also confirm 24 logical lines in README.md and LF-only bytes (0 CRLF, 0 lone CR) across all eight captures.

## Candidate-line check on the round-46 C3 scout report

`R46ScoutC3Grader.md` cites line numbers in a table column and in prose. Checked against the pinned capture, the
column is wrong at **three different offsets** — so no single correction fixes it:

| scout cite | scout's quote | real line | offset |
|---|---|---|---|
| `| 7 |` | `def test_fibonacci_polyglot():` | 10 | +3 |
| `| 14 |` | `polyglot_files = os.listdir("/app/polyglot")` | 17 | +3 |
| `| 15 |` | `assert polyglot_files == ["main.py.c"]` | 18 | +3 |
| `| 22–24 |` | the `gcc … -o /app/polyglot/cmain` subprocess | 23–25 | +1 |
| `| 26 |` | `test_cases = [(42, …), (10, …), (0, …)]` | 27 | +1 |
| `| 32 |` | `assert python_out == expected and c_out == expected` | 44 | +12 |
| prose `test.sh:17–21` | "lines 17–21 invoke pytest" | pytest runs at 22; 17 is blank and 18–21 are the `uvx` flags | range stops one line short, and the reward writes (:26/:28) sit outside it |

Its `environment/Dockerfile` cites are wrong too: `:33` says `:3–5` holds `FROM ubuntu:24.04`, `WORKDIR /app` and
`apt install -y gcc`, but `FROM` is line 2, `WORKDIR` line 4 and the install line 6; `:28` says `Dockerfile:1-5`
"starts Ubuntu 24.04 and installs gcc", a range that excludes line 6. My rows cite `:2` and `:6`.

Its `| 15 |` decision text ("Exact listing/order equality") is also wrong on order: the expected value is a
one-element list, so `os.listdir` order cannot matter and any two-entry listing fails wherever the entry sits. The
real edge is a *directory* named `main.py.c`, which satisfies the assert and is rejected only by the `gcc` call.

Conclusion: adopt none of the scout's line numbers; my rows' cites were re-derived from the capture and are in the
table above.

## Gate table

| candidate | verdict | reason + flip | URL | accessed | located quote |
|---|---|---|---|---|---|
| tests/test_outputs.py | ACCEPT S166 (code, A) | the executed predicate itself | `…2fd12b88…/polyglot-c-py/tests/test_outputs.py` | 2026-10-27 | `:27 "test_cases = [(42, \"267914296\"), (10, \"55\"), (0, \"0\")]"` |
| tests/test.sh | ACCEPT S167 (code, A) | the reward mapping + 3.13 interpreter pin | `…/polyglot-c-py/tests/test.sh` | 2026-10-27 | `:26 "echo 1 > /logs/verifier/reward.txt"` |
| instruction.md | ACCEPT S168 (docs, A) | the request the grader is mapped against | `…/polyglot-c-py/instruction.md` | 2026-10-27 | `:9 "I'm using python3 3.12.3 and gcc 13.2.0."` |
| solution/solve.sh | ACCEPT S169 (code, A) | the oracle; names the polyglot mechanism | `…/polyglot-c-py/solution/solve.sh` | 2026-10-27 | `:14 "#define sdf b /*"` |
| environment/Dockerfile | ACCEPT S170 (code, A) | the image recipe; unpinned toolchain | `…/polyglot-c-py/environment/Dockerfile` | 2026-10-27 | `:6 "RUN apt update -y && apt install -y gcc"` |
| task.toml | ACCEPT S171 (docs, A) | author metadata: budgets, image tag, internet flag | `…/polyglot-c-py/task.toml` | 2026-10-27 | `:34 "allow_internet = true"` |
| README.md | ACCEPT S172 (docs, A) | author prose; publishes the case table | `…/polyglot-c-py/README.md` | 2026-10-27 | `:22 "2. The file compiles successfully with gcc"` |
| Docker Hub tag page `alexgshaw/polyglot-c-py` | **REJECT** | the page states no gcc/python version and the tag is mutable, so it cannot evidence the toolchain the task promises; flip: a digest-pinned manifest inspection at the page's own digest `sha256:43f9d558…dc4c04` (152153707 B) listing the installed versions | https://hub.docker.com/r/alexgshaw/polyglot-c-py | 2026-10-27 | no document text; nearest token in the hydrated JSON: `"digest","sha256:43f9d55805dfcfaeb7875c620b9313bde9cd263a2d75362d730710c935dc4c04"` |
| unpinned `main` ref of the same files | **REJECT** | `main` serves the same 339 bytes today (and currently equals the pin, 0 drift), but a branch ref moves, so a 180-day recheck has no anchor; flip: cite `main` only with a recorded commit id and a byte-identical re-fetch | `…/terminal-bench-2/main/polyglot-c-py/instruction.md` | 2026-10-27 | `200, 339 bytes, byte-identical to the pinned capture` |

`…2fd12b88…` abbreviates `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6`.

## Findings (for the L1 / entry writer; not verified beyond what is quoted)

- **F1 — the harness is a shared template, and its interpreter is not the promised one.** `tests/test.sh` sha256
  `4770437e…` is byte-identical to the password-recovery `tests/test.sh` (S153), and it runs pytest through
  `uvx -p 3.13` (`test.sh:18-19`) while `instruction.md:9` tells the agent it has "python3 3.12.3". [`INFERENCE`] the
  graded `subprocess.run(["python3", …])` at `test_outputs.py:31` resolves through the PATH uvx builds, so the
  interpreter that executes the graded Python leg is chosen by the harness, not by the image.
- **F2 — the `.gitignore` is shared boilerplate.** Its sha256 `9a8dd8d9…` equals the round-45 password-recovery
  `gitignore` byte for byte; it carries no task content and therefore no row.
- **F3 — the toolchain is promised but not pinned.** `environment/Dockerfile` is six lines: `FROM ubuntu:24.04` plus
  `RUN apt update -y && apt install -y gcc`, with no `/app/polyglot` created; gcc comes from the base image's apt
  pocket, so "gcc 13.2.0" is a base-image property, not a recipe fact.
- **F4 — the README publishes the answer key's fixed points.** `README.md:24` names `f(0)=0, f(10)=55, f(42)=267914296`,
  the same three constants as `test_outputs.py:27`; it also names the toolchain and the 15-minute budget.
- **F5 — the grader is single-shot.** `test_outputs.py:17-18` asserts `os.listdir("/app/polyglot") == ["main.py.c"]`
  *before* `:23-24` compiles to `/app/polyglot/cmain`; a second execution of the same test file therefore sees two
  entries and fails at the first assert. A counter that re-grades in place is measuring the assertion order, not the
  agent — the probe must run against a fresh copy per case. The entry seat adds that the comparison itself is not
  order-sensitive (a one-element list) and that the sharper edge is a *directory* named `main.py.c`, which satisfies
  the listing and is rejected only by `gcc`. (`[INFERENCE]` from the cited lines; no re-run performed — C3's order
  rule forbids executing a graded case before stage 2.)
- **F6 — the image tag carries a digest.** The Docker Hub page exposes tag `20251031` at
  `sha256:43f9d55805dfcfaeb7875c620b9313bde9cd263a2d75362d730710c935dc4c04`, 152153707 bytes — a citable immutable
  anchor if a later round needs to evidence image contents (the flip on the REJECT above).
- **F7 — the scout's line cites are unusable** (section above): its table column is off by +3, +1 and +12 on
  different rows, its `test.sh:17–21` prose range stops one line before the pytest call, and its two Dockerfile ranges
  miss the lines they claim. Do not copy those citations into the entry or the probe.
- **F8 — manifest order is not a gate input.** `pkg_gate.py:152-176` (`c_captures`) parses `SHA256SUMS` line by line
  into a name→digest dict and compares each digest with the bytes and with the spec pin, so a differently ordered
  manifest of the same eight pairs is gate-equivalent; the L1 can land either file but must pin exactly one digest.
  The same leg requires **every** file in `capture_dir` to be listed, which is why the eight-entry manifest (including
  `gitignore`) is mandatory even though `gitignore` has no row.
- **F10 — two admissible anchor sets exist; only one may land.** `R46ExecC3Spec` publishes a different cell set
  (`anchors.json`, quoted in the entry seat's `sources-rows-S166-S172.md`): S166 `:44`, S167 `:22`, S168 `:1`,
  S169 `:12`, S170 `:6` **without a range token**, S171 `:22`, S172 `:4`. Every cell of mine and every cell of theirs
  measures 0 defects under both the grade tool and V12 (my measurement: `V12 ok rows=7 defective=0`); the two sets
  quote different lines and cannot be blended, because the quote text, the word count and the range belong to one
  cell. Two notes if the L1 prefers theirs: its S170 cell drops `Dockerfile:1-6`, so the row would carry no range at
  all (the seat format asks for one), and its S168/S172 cells anchor the request's first line rather than the version
  promise and the case table. The entry seat's earlier alarm that my cells violate V12 was withdrawn by its author
  after the measurement; my rows were not changed.
- **F11 — the S170 range token is unverified by construction.** Both checkers' range regex needs a `name.ext:` token,
  so `Dockerfile:1-6` parses as nothing (`RANGE.search` → `None`, measured) and S170 is certified on line and word
  count only; the round-45 S152 Dockerfile row has the same shape. A row cannot fix this by rewording — `Dockerfile`
  has no extension — so the honest statement is that six of the seven rows are range-checked and S170 is not. The
  token stays because it is true and readable to a human; it is not a claim that a checker verified it.

## Touched surfaces

Written (all inside my own report area, plus scratch):

- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ScribeC3Rows.md` (this report)
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-46/w1/R46ScribeC3Rows/` — `rows.md` (the 7 row
  lines verbatim, in id order, ready to paste after S156), `gate-anchorline.txt`, `gate-base.txt`,
  `gate-selftest.txt`, `quotes.tsv`, `fetch-receipt.txt`, `v12-run.txt`, `SHA256SUMS`
- scratch only: `/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows/{lane,env,…}` (two `--shared` clones across the two
  drafting passes; rows appended and `git add`ed, never committed; neither clone is the lane) — removed after the
  receipts were copied out (`scratch_guard.py safe-rm`)

Not touched: `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/evidence/`, `corpus/README.md`, `SCORECARD.md`,
`LOG.md`, `PROVINCE.md`, `plans/` (no counter, no probe, no spec), the lane's jj/Git state, the fleet root.

## Out of scope (left for the integrating seats)

- landing the rows, the captures, `SHA256SUMS` and the README index/coverage/PROVINCE lines;
- `corpus/knowledge/tb2-polyglot-c-py-grader.md` (owned by the C3 entry seat — row map and facts sent by message);
- `plans/pkg-spec-r46.json`, `plans/polyglot_c_py_probe.py`, `plans/round46_c3_verify.py` and any probe run: the
  C3 order rule (Q30) forbids executing a graded case before the stage-2 freeze, so nothing here was run, and
  `pkg_gate.py --rerun` was not invoked;
- C2's rows S157–S165 and the entry's errata (other seats).

## Host safety

Every counter/gate run went through `.ufo/waves/round-46/claims/envelope.sh "$S/env" …`. Four measured runs in this
seat: the two grade-tool runs and the selftest report
`local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged`; the V12 run reports
`7747d38e2042d398` unchanged on both sides. The two digests differ because `~/.local/bin` changed **between** my
runs (a sibling seat's install under the operator's tooling authorization), not during any of them — each measurement
is bracketed by an unchanged digest and therefore stands, and none of the change is mine. Exit codes 1, 1, 0, 0 are
the tools' own. No installs, no upgrades, no pacman transaction, no host service restart; nothing written outside my
two report paths and `/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Rows`.

## Known limits

- I verified the captures and the rows, not the grader's semantics: F1/F5 are inferences from cited lines, and no
  polyglot case was executed (order rule Q30).
- The README range is stated as `1-24` (`splitlines`, the gate's rule) although `wc -l` prints 23; the discrepancy is
  the missing trailing newline, and both numbers are in the receipts.
- `.gitignore` is captured without a row by round-45 precedent; if the stage-2 spec requires every capture to map to a
  row, that is a one-line addition (`docs`, tier A) — not made here to avoid inventing a claim with no teaching value.
- S170's `Dockerfile:1-6` cannot be range-checked by either checker (no `name.ext:` token), so that row rests on its
  two line-cited quotes and word counts; the other six rows are checked on all three legs (F11).

VERDICT: c3-rows-7-anchorline-defective-0-census-exit-1
