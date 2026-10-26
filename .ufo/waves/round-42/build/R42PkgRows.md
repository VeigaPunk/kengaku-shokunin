# R42PkgRows — SOURCES rows S125–S127 for C2 (round 42, wave 1)

Seat: R42PkgRows (scribe). Task: draft the three registry rows for the pinned TB2 `circuit-fibsqrt` grader in
`corpus/SOURCES.md`'s exact 11-cell schema, re-fetch the three pinned URLs and `cmp` them with the captures,
validate the rows in a scratch registry copy, run `plans/anchor_digest_check.py` on a clone after staging, and
draft the lesson `## Gate` lines. Nothing in the freeze was edited; no lane file was written.

## 0. Axes (godspeed)

- **coverage** — are S125/S126/S127 present, tier A, mined, opened, used-by the entry, and do they name what the
  capture actually does? Moved: rows drafted and validated end to end against the unmodified instruments.
- **freshness** — do the digests equal the bytes at the pin *today*, at an access time recorded in the row and in
  the lesson gate line? Moved: live re-fetch, `cmp`, digest, timestamp.
- **harm** — the three rows must not perturb any other registry finding (census E/W counts unchanged) nor any
  frozen pin. Held: baseline census E=0 W=15 → with rows E=0 W=15.

## 1. Re-fetch and capture identity

Command (scratch dir `/fast/scratch/hyaku/kengaku-r42/R42PkgRows`, captures read from the lane):

```
for f in tests/test_outputs.py instruction.md tests/sim.c; do curl -sS -o "raw_$(basename $f)" \
  "https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/$f"; done
cmp -s raw_<file> corpus/evidence/round42/tb2-circuit-fibsqrt/<file>
sha256sum raw_<file>
```

Output, first pass at **2026-10-26 17:20:09 -03** (transcript) and the recorded receipt pass at
**2026-10-26 17:24:14 -03** (`R42PkgRows/refetch.txt`, quoted verbatim):

```
access 2026-10-26 17:24:14 -0300
GET 200 tests/test_outputs.py cmp=IDENTICAL sha256=6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438
GET 200 instruction.md cmp=IDENTICAL sha256=a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea
GET 200 tests/sim.c cmp=IDENTICAL sha256=700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173
```

Three `200`s, three `cmp=IDENTICAL`, and each digest equals the capture's `SHA256SUMS` entry and the pin in
`plans/pkg-spec-r42.json` (`rows.S125.sha256`, `rows.S126.sha256`, `rows.S127.sha256`). The L1's open time in the
freeze is 2026-10-26 17:08 -03 (`plans/round-42-claims.md` §C2 Surface); this seat re-opened at 17:20:09 and
17:24:14 -03.

## 2. Drafted rows (verbatim; insert directly after the S124 line, i.e. before the blank line that precedes `## Paths`)

```
| S125 | Terminal-Bench 2.0 circuit-fibsqrt task grader (tests/test_outputs.py) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/test_outputs.py | code | A | the executed scoring predicate of this one TB2 task at a pinned commit: three pytest functions over /app/gates.txt and /app/sim on a fixed 28-value table, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, test_outputs.py:1-147, :23 "assert line_count < 32000" (4 words); sha256 6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438 | three pytest functions, not one: an /app/gates.txt existence assert, a line count strictly below 32000, and 28 inputs each graded by running /app/sim against fib(isqrt(n)) modulo 2^32; the compile writes ./sim in the cwd while the run path is /app/sim | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-circuit-fibsqrt-grader.md |
| S126 | Terminal-Bench 2.0 circuit-fibsqrt task instruction (instruction.md) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/instruction.md | docs | A | the request this one task states to the agent at a pinned commit, as the maintainer's own specification the grader is mapped against | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, instruction.md:1-13, :8 "the first 32 lines are defined by the binary representation of stdin" (12 words); sha256 a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea | a 13-line request naming a seven-form gate grammar, stdin as the source of the first 32 lines and the last 32 as printed after 32000 steps, with worked examples 208 to 377 and 20000 to 1407432322 that the 28-value grading table never exercises | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-circuit-fibsqrt-grader.md |
| S127 | Terminal-Bench 2.0 circuit-fibsqrt task simulator (tests/sim.c) — https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/sim.c | code | A | the simulator program the grader compiles and runs at a pinned commit: a gate-list interpreter over gates.txt whose print rule decides the graded integer, as this capture shows it | commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, sim.c:1-353, :319, :335 "for (int step = 0; step < 32000; step++)" (9 words); sha256 700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173 | reads gates.txt relative to the process working directory, skips lines that do not parse as outN = op, runs exactly 32000 steps, ignores unknown binary operators, and prints the 32 highest-numbered signals as a little-endian integer | mined | 2026-10-26 | 180d | corpus/knowledge/tb2-circuit-fibsqrt-grader.md |
```

Copies: `R42PkgRows/rows-S125-S127.txt` (sha256 below).

Schema facts a reviewer can check without re-deriving: 11 cells each, no `|` inside any cell, no
`sha256` token outside the anchor cell, one token per row, status/opened/recheck/used-by from the task
(`mined`, `2026-10-26`, `180d`, `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`), and the anchor quote sits on
the **last** cited line — the same rule S122/S123 follow.

Row self-check (scratch script, replicates the counter's V3 test plus quote/word checks), output verbatim:

```
S125: cells=11 quote_on_line=23 present=[23] verbatim=True quote_words=4 teaches_words=40 kind=code digest_ok=True
S126: cells=11 quote_on_line=8 present=[8] verbatim=True quote_words=12 teaches_words=43 kind=docs digest_ok=True
S127: cells=11 quote_on_line=335 present=[335] verbatim=True quote_words=9 teaches_words=36 kind=code digest_ok=True
teaches_pairwise_distinct= True scopes_pairwise_distinct= True
ALL_CHECKS_PASS
```

"`present=[n]`" is the unique line of the capture containing the quoted substring; the quote is verbatim in the
capture and `teaches` is 36–43 words (≥ 8, per `plans/pkg-spec-r42.json` `entry_rules.min_teaches_words`).

## 3. Validation

### 3.1 Census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate`)

Scratch lane trees: `regC/lane/corpus` (spliced `SOURCES.md`, `lessons/`, `evidence/`, `knowledge/` symlinked to
the lane's, entry **absent**) and `regD/lane/corpus` (same, with `knowledge/` a directory of symlinks to every real
entry file plus a one-line **scaffold stand-in** at `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` — the entry
itself is drafted by another seat and is not landed, so the stand-in exists only to exercise E11). `regE` is the
unmodified registry (baseline).

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent \
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/SOURCES.md
```

- **rows present, entry present (regD): `CENSUS_EXIT=0`**, one `file ok` line, `E=0 W=15`, `S12x=0`
  (`census-entry-present.out`):
  ```
  E=0 W=15 S12x=0
  file	ok	/fast/scratch/hyaku/kengaku-r42/R42PkgRows/regD/lane/corpus/SOURCES.md
  ```
- **rows present, entry absent (regC): `EXIT_C=1`**, and the only non-W04 findings are the three expected E11
  (`census-entry-absent.out`) — i.e. the rows themselves are clean and their sole open dependency is the entry:
  ```
  file	E11	S125 missing used-by corpus/knowledge/tb2-circuit-fibsqrt-grader.md
  file	E11	S126 missing used-by corpus/knowledge/tb2-circuit-fibsqrt-grader.md
  file	E11	S127 missing used-by corpus/knowledge/tb2-circuit-fibsqrt-grader.md
  ```
- **baseline, unmodified registry (regE): `EXIT_E_baseline=0`**, `E=0 W=15` → the 15 W04 duplicate-URL warnings are
  pre-existing and unchanged by these rows; no E-code appears with or without them.

### 3.2 Anchor digest check (`plans/anchor_digest_check.py`), clone after staging

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kengaku-shokunin "$S/lane"
git -C "$S/lane" rev-parse --show-toplevel        # /fast/scratch/hyaku/kengaku-r42/R42PkgRows/lane
<insert rows after line 139>; git -C "$S/lane" add corpus/SOURCES.md   # index-only, no commit
python3 "$S/lane/plans/anchor_digest_check.py" --lane "$S/lane" --evidence-ref index
```

```
ANCHOR_INDEX_EXIT=0   ->  rows=120 tokens=27 defects=0
ANCHOR_HEAD_EXIT=0    ->  rows=120 tokens=27 defects=0
```

Baseline on a second, unedited clone: `rows=117 tokens=24 defects=0` (`BASELINE_ANCHOR_EXIT=0`) — the delta is
exactly the three rows and their three tokens. Verbose resolution (`anchor-index-bindings.out`):

```
EVIDENCE ref=index files=461 manifest_digests=60 rows=120 paths=532 bound_rows=29 unbound_rows=91
BIND S125 capture=corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py by=url-task
BIND S126 capture=corpus/evidence/round42/tb2-circuit-fibsqrt/instruction.md by=url-task
BIND S127 capture=corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c by=url-task
RESOLVED S125 digest=6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438 via=corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py bind=url-task listed=corpus/evidence/round42/tb2-circuit-fibsqrt/test_outputs.py
RESOLVED S126 digest=a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea via=corpus/evidence/round42/tb2-circuit-fibsqrt/instruction.md bind=url-task listed=corpus/evidence/round42/tb2-circuit-fibsqrt/instruction.md
RESOLVED S127 digest=700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173 via=corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c bind=url-task listed=corpus/evidence/round42/tb2-circuit-fibsqrt/sim.c
```

Each row binds by `url-task` (the URL's task component `circuit-fibsqrt` matches the committed
`task.toml` slug `terminal-bench/circuit-fibsqrt`) to its own capture only.

### 3.3 Host envelope and Q32 readings

Every census/anchor run above used this envelope (the counter's own nesting is unaffected; none of these runs
writes inside a PATH directory):

```
bwrap --dev-bind / / --ro-bind /home/vgpnk/.local/bin /home/vgpnk/.local/bin --tmpfs /run/user/1000 \
  --proc /proc --unshare-pid --die-with-parent <command>
```

| run | start `date +%T` | end `date +%T` | `ls -A ~/.local/bin \| sha256sum` before / after |
|---|---|---|---|
| census regC/regD/regE batch | 17:22:38 | 17:22:38 | `436b361f9d1edc4ea349d01c935a37f5850860841ef5969b7af419cd7d63fc18` / same |
| census final (regD) | 17:23:40 | 17:23:41 | same / same |
| anchor index+head (fresh clone) | 17:23:47 | 17:23:47 | same / same |
| anchor verbose | 17:24:09 | 17:24:09 | same / same |

No tool installed or upgraded (nothing was needed); no pacman call; nothing written to `/usr`, `/etc`, `$HOME` or
any PATH directory.

## 4. Lesson `## Gate` lines (draft for `corpus/lessons/round-42.md`, round-41 table shape)

```
| Candidate | Verdict | Reason and flip condition |
|---|---|---|
| S125 `tests/test_outputs.py` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/test_outputs.py`; re-fetched cmp-identical 17:20:09 -03 and again 17:24:14 -03 (`R42PkgRows/refetch.txt`). Quote, `test_outputs.py:23`: "assert line_count < 32000" (4 words); sha256 `6117b8edb7d567b30e32b16a9244bec4c131ec01e9065d52f6f53f87e36f0438`. Flip: the capture's digest leaves the pin in `plans/pkg-spec-r42.json` (`rows.S125`). |
| S126 `instruction.md` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/instruction.md`; cmp-identical re-fetch 17:20:09 -03 and 17:24:14 -03. Quote, `instruction.md:8`: "the first 32 lines are defined by the binary representation of stdin" (12 words); sha256 `a7f500266a878d04ac9de39fba76220cfad216d8f6b8063bba93bebb3d4ab9ea`. The probe falsifies exactly this sentence: `sim.c:323-325` takes the value from `argv[1]`, not stdin, and `sim.c:330` puts the LSB in signal 0 although `:328`'s comment says signal 0 gets the MSB. Flip: digest leaves the pin. |
| S127 `tests/sim.c` @ `2fd12b88` | **Admitted (mined, tier A)** | Opened by the L1 2026-10-26 17:08 -03 at `https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/circuit-fibsqrt/tests/sim.c`; cmp-identical re-fetch 17:20:09 -03 and 17:24:14 -03. Quote, `sim.c:335`: "for (int step = 0; step < 32000; step++)" (9 words); sha256 `700645ac6156cdc88ec1e210f7c7d8d9969bb42aec969c410597e8efca796173`. Graded-state deciders live here: `parse_gates("gates.txt")` (`:319`, cwd-relative), `sscanf` skip (`:113-115`), highest-index print (`:340-347`). Flip: digest leaves the pin. |
```

## 5. Findings for the L1 (all located in the captures; none changes a frozen instrument)

1. **The compiled binary is not the one run, unless the cwd is `/app`.** `test_outputs.py:65-67` runs
   `gcc -O3 /tests/sim.c -o sim` (output `./sim`, cwd-relative) while `:119` executes `/app/sim`. `Dockerfile:3`
   sets `WORKDIR /app`, so the overwrite of a planted `/app/sim` happens only with that cwd; `test.sh:13` guards
   only `PWD = /`. This is the mechanical reason the `fake-sim-script` case is PPF rather than FPF.
2. **Size is counted on lines; the simulator counts gates.** `test_outputs.py:20-23` sums every line of
   `/app/gates.txt` against `< 32000`; `sim.c:113-115` drops every line that does not scan as `outN = op` before
   `num_signals` is set. Two different denominators for the same "32,000" word in `instruction.md:1` and `:11`.
3. **`sim.c` contradicts its own bit-order comment.** `:328` reads "signal 0 gets MSB, signal 31 gets LSB"; `:330`
   is `values[i] = (input_value >> (i)) & 1`, i.e. signal 0 gets the LSB, and `:342-346` reassembles the output the
   same little-endian way. `instruction.md:8` says nothing about order at all.
4. **A hard failure mode unrelated to correctness:** `MAX_DEPS` is 10000 (`:6`) and the parser `exit(1)`s when a
   signal exceeds it (`:134-138`, `:147-151`, `:167-176`), so a legal-length gate file can still abort the grader.
5. **Anchor convention used:** the quoted line is the last `:<n>` in the anchor cell (the S122/S123 style). If the
   L1 prefers ascending citation order, move the quote's line to the end rather than reordering the quote.

## 6. Integration notes

- **Placement:** rows go immediately after the `S124` line of `corpus/SOURCES.md` (line 139 at `fda71ae`); registry
  order is by id.
- **Dependency:** with the rows in place but the entry absent, `sources-census.sh validate` exits 1 with exactly
  three E11 lines (S125–S127 → `corpus/knowledge/tb2-circuit-fibsqrt-grader.md`). The rows cannot be green on their
  own; the C2 counter's V6 reads the same census, so **the entry must land with the rows** (or before them).
- **No new warnings:** W04 stays at 15 (pre-existing duplicate-URL pairs), E at 0.
- **Not drafted here** (other seats / L1): the `## Search log` paragraph for this round, the README index row and
  §Frontier bullet, the PROVINCE paragraph, the entry itself (drafted at
  `.ufo/waves/round-42/build/R42PkgEntry/tb2-circuit-fibsqrt-grader.md`; its three `source:` lines already agree with
  these rows' URLs, tiers and line ranges).

## 7. Limits

- The evidence stand-in used for the green census run is **not** the entry; the honest state of the lane today is
  "rows clean, E11 until the entry lands" (both states are pasted in §3.1).
- Tier is curation for the row's narrow scope (one task's grader/instruction/simulator at one commit); no claim is
  made about TB2 as a whole.
- Only the three named files were opened at the pin; the other six captures were re-verified only through
  `SHA256SUMS` and the counter's V1 pin table, not re-fetched by this seat.
- The quote/teaches word counts are this seat's token counts (whitespace split), not a tool's.

## 8. Artifacts

All under `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-42/build/R42PkgRows/`:

| file | bytes | content |
|---|---|---|
| `rows-S125-S127.txt` | 2791 | the three rows, verbatim; sha256 `1c5d2cbb8aeb6cc7f5effaab242b7cf337018db6ec4e2b377214cc20ed3ae643`, 3 `sha256` tokens total (one per anchor cell), `awk -F'|'` cell count 11 / 11 / 11 |
| `refetch.txt` | 364 | live re-fetch: three `200`, three `cmp=IDENTICAL`, three sha256, access time |
| `census-entry-present.out` | 1463 | census `exit 0`, `file ok`, E=0 W=15 |
| `census-entry-absent.out` | 1615 | census `exit 1`, exactly three E11 for S125–S127 |
| `census-summary.txt` | 56 | C/D E-W-S12x counts |
| `anchor-index.out` / `anchor-head.out` | 29 each | `rows=120 tokens=27 defects=0` |
| `anchor-index-bindings.out` | 1057 | BIND/RESOLVED lines for S125–S127 |

Sizes are `ls -l` bytes; the digest above is `sha256sum rows-S125-S127.txt`.

## 9. Receipt

- Environment: linux 7.2.11-arch1-1, x64; host python3 and `gawk` as installed; `bwrap` envelope above.
- Installed/upgraded: nothing.
- Wrote only `.ufo/waves/round-42/build/R42PkgRows/` (this report + 7 small receipts) and
  `/fast/scratch/hyaku/kengaku-r42/R42PkgRows/` (clones, scratch registry trees, fetched bytes).
- No lane file, no git/jj mutation in the lane, no commit or push anywhere; the two clones are read-only apart from
  the index-only `git add corpus/SOURCES.md` used to stage the rows for the anchor check.
- Every number above carries its command; every quote carries `file:line` in the capture.

VERDICT: rows-drafted-3-census-exit-0
