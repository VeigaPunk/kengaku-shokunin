# R46ScribeC3Entry — dossier draft for `corpus/knowledge/tb2-polyglot-c-py-grader.md`

Seat: scribe, C3 (coverage), round 46 wave 1. Nothing here is landed: the draft lives in this seat's `w1`
subdirectory and the L1 integrates. No graded case of the task was executed (QUALITY Q30); the probe has not
been run by any seat I can see, and I did not run it.

## Behaviour of this seat

Read the pin, drafted the entry in the frozen section order, drafted the package scaffolding the L1 needs, and
verified the draft against the round-45 gate's own clauses plus the round-45 counter's own regexes on a scratch
fixture. Everything below is a measured result or a quoted line; no graded execution took place.

Frozen inputs read in full before writing: `plans/round-46-claims.md` (§C3 and §Separability),
`corpus/knowledge/tb2-password-recovery-grader.md` (the structural exemplar),
`corpus/evidence/round45/password-recovery-dry-cases-freeze.txt` (the `TAG`/`CASE` dry-table shape),
`plans/round45_c2_verify.py` (V1-V11: `PRED_SECTION`, `PRED_BLOCK`, `PRED_LINT_TOKENS`, `CASE_ROW`, `MAP_ROW`,
`MECH_ROW`, `derive`), `plans/pkg_gate.py` (`c_quote_shape`, `c_quote_verbatim`, `c_captures`, `c_sources`,
`c_provenance`, `c_readme`), `plans/anchor_line_check.py` (`QUOTE_RE`, `RANGE_RE`, `WORDS_RE`, `row_defects`),
pinned by `plans/pkg-spec-r45.json`. `plans/round46_c2_verify.py` and `plans/round46_c1_verify.py` were not read
(C2 whole-frozen and C1 not this seat's surface).

## What the pin contains, measured

The task directory at terminal-bench-2 `2fd12b88aafdd04a52c298e3940bcb189f9766d6` holds **eight** files:
`.gitignore`, `README.md`, `environment/Dockerfile`, `instruction.md`, `solution/solve.sh`, `task.toml`,
`tests/test.sh`, `tests/test_outputs.py`. There is **no** `environment/setup.sh` (that file exists for round 45's
`password-recovery`; a direct fetch here returns 404), so the round-45 capture layout of nine files becomes eight.

Commands and outcomes (all against the pin, in scratch, no writes outside it):

```
curl -sS --max-time 40 -o <name> <raw_base><path>      # 7 files: HTTP 200; environment/setup.sh -> 404, 14 bytes
curl -sS -o cap/tb2.tar.gz https://codeload.github.com/harbor-framework/terminal-bench-2/tar.gz/2fd12b88...
                                                       # HTTP 200, 40357259 bytes; tar -tzf -> 1447 entries
tar -xzf ... --strip-components=1 .../polyglot-c-py    # 8 files, same tree as the raw fetches
cmp <raw fetch> <tarball copy>                         # byte-identical for all seven row files
sha256sum .gitignore README.md environment/Dockerfile instruction.md solution/solve.sh task.toml tests/test.sh tests/test_outputs.py
  9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953  .gitignore
  591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881  README.md
  2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a  environment/Dockerfile
  a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96  instruction.md
  e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0  solution/solve.sh
  d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea  task.toml
  4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334  tests/test.sh
  b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec  tests/test_outputs.py
python3 -c "len(open(f).read().splitlines())"          # 46, 24, 6, 9, 57, 41, 29, 23 -> range ends are exact
```

`tests/test.sh`'s digest `4770437e…` is the same as round-45's `password-recovery` `tests/test.sh`
(`corpus/evidence/round45/tb2-password-recovery/test.sh`): shared TB2 harness boilerplate.

## The draft

`w1/R46ScribeC3Entry/tb2-polyglot-c-py-grader.md`, sha256
`76318ca848199cf3b49688fad4bbc48a3748ff9c1ec6093b681122fac8466f4c`, 26327 bytes. Structure is the exemplar's,
in order, with the provenance trio first:

| # | section | state |
|---|---|---|
| — | 7 × `source:` + `verified-at: 2026-10-27` + `recheck:` | complete, one URL per line, all seven upstreams |
| 1 | `## Summary` | complete; names the class against the eleven exemplars |
| 2 | `## Located quotes` | **20** quotes, 20 distinct lines, all 3-25 words, all verbatim |
| 3 | `## Requirement map` | 7 tags on 4 instruction lines; labels marked as draft predictions |
| 4 | `## Case table` | **16** rows, `Observed` = `TBD` on every row (QUALITY Q30) |
| 5 | `## Mechanism` | 16 rows, one per case, predicted decisive line + verbatim fragment |
| 6 | `## Findings` | 8 numbered findings, each citing its cases |
| 7 | `## Negative space` | the non-claims, then a 6-clause falsifier |
| 8 | `## Predictor` | one ```python block, `predict(listing, source)`, 483 bytes, lint-clean |
| 9 | `## Limits` | 5 named limits incl. the V11 bypass limit |

**Class, named against the eleven.** `polyglot-c-py` is the **dual-runtime execution** class: the graded
artefact is an agent-authored **source file that the grader compiles with `gcc` and also runs with `python3` at
grading time**, and the score is a pre-build `os.listdir` equality plus three fixed-point `stdout.strip()`
comparisons in both runtimes. Its nearest neighbour among the eleven is `circuit-fibsqrt` (also compiles at
grading time) — but there the compiled object is the *task's own simulator* and the graded artefact is a data
file; here the compiled object *is* the graded artefact. Against the other ten (`protein-assembly`,
`regex-log`, `configure-git-webserver`, `build-pmars`, `git-leak-recovery`, `db-wal-recovery`,
`constraints-scheduling`, `feal-differential`, `feal-linear`, `password-recovery`) the distinction is that every
one of them *reads* a state; none of them *executes* the graded bytes as a program, and none of them mutates the
graded directory in the middle of its own test.

**The frozen case set** (16, ids for the probe's `--dry` table and the receipt):

```
nop  empty-dir  oracle-solve-sh  extra-file  precompiled-cmain  dotfile  wrong-name  dir-at-source
python-only  c-only  lookup-print  stderr-noise  exit-nonzero  extra-stdout  padded-stdout  fib-wrong
```

Predicted verdicts in that order: `F F P F F F F F F F P P F F P F` — 4 passes, 12 fails. `Tests` carries one
letter because `test_outputs.py` holds exactly one test function; no `-` appears anywhere.

**Requirement map.** Seven tags on four of the nine instruction lines: `single-file`, `path` (`:1`);
`python-run` (`:3`); `c-compile`, `c-run` (`:5`); `stdout`, `fib` (`:7`). Predicted labels: six `enforced`,
`fib` **`partly`** (`lookup-print` passes while violating it, `fib-wrong` fails). Line `:9` carries no tag and
the map says why.

**Predictor.** `predict(listing, source)`: `listing` is `os.listdir("/app/polyglot")` at test entry (or `None`),
`source` is the file's text (or `None`), True = the grader passes. It decides the listing leg exactly, the
dual-runtime leg as a structural question (`#include`/`int main(`/`printf(` on the C side, `def `/`argv` on the
Python side), and the newline encoding — a bare-CR-only source is predicted `fail` because it is one logical
line to the C preprocessor. It does **not** decide arithmetic, and the entry says so: a valid polyglot computing
the wrong value is predicted `pass`. That state is out of the declared domain and lives in the case table.

## Gates

Both runs below were made inside the round-46 envelope; the PATH-dir content digest is unchanged in both, so
both measurements count.

### Gate P3-P8 + entry shape + predictor units

`$S/pkg` is a scratch fixture: the eight captures + `SHA256SUMS`, the seven rows renumbered to the converged
mapping, the entry draft, a minimal `corpus/README.md` carrying this seat's index row and coverage bullet, and
`plans/pkg-spec-r46.json`. `verify_gate.py` loads the lane's `plans/pkg_gate.py` and `plans/round45_c2_verify.py`
by path (no copy) and calls their clauses.

```
ENVELOPE /usr/bin/bwrap --dev-bind / / --ro-bind /home/vgpnk /home/vgpnk --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/env /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/env --bind /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/env/home-cache /home/vgpnk/.cache --tmpfs /run/user/1000 --proc /proc --unshare-pid --die-with-parent -- python3 /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/verify_gate.py /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/pkg
ENVELOPE start 02:16:18 cwd=/home/vgpnk/Projects/shokunin
FIXTURE /fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry/pkg
P3 quote_shape: ok rows=20 distinct_quotes=20 distinct_lines=20 out_of_word_range=0
P4 quote_verbatim: ok checked=20 bad=0 first=0
P5 captures: ok manifest_entries=8 bad=0 first=0
P6 sources: ok rows=7 bad=0 first=0
P7 provenance: ok source_lines=7 bad=0 first=0
P8 readme: ok index_rows=1 knowledge_files=1 bad=0 first=0
GATE clauses=6 defects=0
SECTIONS n=9 ['Summary', 'Located quotes', 'Requirement map', 'Case table', 'Mechanism', 'Findings', 'Negative space', 'Predictor', 'Limits']
CASETABLE tbd=16
PREDICTOR blocks=1
PREDICTOR bytes=483 lint=clean
  ok  oracle-exact-listing: got=True want=True
  ok  oracle-tuple-listing: got=True want=True
  ok  oracle-crlf-source: got=True want=True
  ok  oracle-cr-only-source: got=False want=False
  ok  listing-cmain-present: got=False want=False
  ok  listing-dotfile: got=False want=False
  ok  listing-empty: got=False want=False
  ok  listing-absent: got=False want=False
  ok  source-absent: got=False want=False
  ok  source-wrong-name: got=False want=False
  ok  source-python-only: got=False want=False
  ok  source-c-only: got=False want=False
  ok  source-empty: got=False want=False
  ok  source-whitespace: got=False want=False
PREDICTOR unit_cases=14 mismatches=0
PREDICATE SCRIBE-C3 pass
ENVELOPE end 02:16:20 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

Pasted verbatim from `w1/R46ScribeC3Entry/gate-run.txt` (the authoritative receipt). The 14 predictor cases are hand-built end states exercised against **my
own** function only — the captured grader was never invoked, so no graded case ran.

### Anchor-line rule on the seven rows, using the tool's own rule

`plans/anchor_line_check.py:evidence_index` needs `git ls-files corpus/evidence`, and the fixture is not a git
repo, so `anchor_rule.py` rebuilds the digest→capture index over the fixture and calls the tool's own
`parse_rows`/`row_defects`.

```
ENVELOPE start 02:17:06 cwd=/home/vgpnk/Projects/shokunin
ROW S166 cited=True capture=.../test_outputs.py defects=none
ROW S167 cited=True capture=.../test.sh defects=none
ROW S168 cited=True capture=.../instruction.md defects=none
ROW S169 cited=True capture=.../solve.sh defects=none
ROW S170 cited=True capture=.../Dockerfile defects=none
ROW S171 cited=True capture=.../task.toml defects=none
ROW S172 cited=True capture=.../README.md defects=none
ANCHORRULE rows=7 defective=0
ENVELOPE end 02:17:08 exit=0 local_bin_content_before=ff187bb5c98aa6b5 after=ff187bb5c98aa6b5 unchanged
```

### V9 row-id presence

```
python3: body = entry minus `source:` lines; missing = [sid for sid in spec.rows if sid not in body]
row ids missing from body: none
```

## Findings (the coverage payload; each tied to captured lines)

1. **The grader's own build mutates the directory it just asserted on.** `:17` lists `/app/polyglot`, `:18`
   compares to `["main.py.c"]`, and `:24` then runs `gcc … -o /app/polyglot/cmain` — writing the second entry
   into that directory. So the test is **not idempotent**: the first run in a fresh container passes, any
   re-grade in the same container fails at `:18`. Nothing in `tests/test.sh` re-creates the directory.
2. **The instruction's published command produces the failing state.** `instruction.md:5` tells the agent to
   build to `/app/polyglot/cmain`; an agent that smoke-tests exactly that and leaves the binary behind fails.
   This is the round-45 `under-varsea` shape again — the task's own advice lands the agent in the rejected
   state — with the difference that here the *grader* also writes that file.
3. **The listing equality is blind to a directory.** `os.listdir` returns names, so a *directory* named
   `main.py.c` satisfies `== ["main.py.c"]`; only the `gcc` call rejects it. The check is "no other name",
   never "a readable file".
4. **Six of nine instruction lines are graded, and one of the three ungraded ones is a promise the image does
   not keep in code.** `:9` names python 3.12.3 / gcc 13.2.0; the test asserts no version, `Dockerfile:2-6`
   pins neither (ubuntu 24.04 defaults happen to match), and `test.sh:19` runs pytest under a *different*
   interpreter (`-p 3.13`) from the one the test invokes.
5. **Three fixed points are not a Fibonacci definition.** `:27` pins `(42,"267914296"), (10,"55"), (0,"0")`;
   `f(1)` — named in `instruction.md:7` — is never exercised, and a lookup-table polyglot passes
   (`lookup-print`). The three literals are also published in `README.md:24`, and `task.toml:34` allows
   internet.
6. **Both runtimes must clear their exit status, and both must agree.** Every subprocess has `check=True`
   (`:24`, `:34`, `:41`) and `:44` is one `and` over four comparisons, so a correct print followed by exit 1
   fails, a one-language file dies at the other leg, and there is no per-runtime partial credit.
7. **Only stdout is compared, stripped at both ends.** `stderr` is captured and never read (`:32-33`,`:36`);
   `strip()` forgives symmetric padding but not an interior newline, so `padded-stdout` passes and
   `extra-stdout` fails.
8. **`tests/test.sh` is shared boilerplate, not task content** (digest equal to round-45's, above) — so its
   `-p 3.13` is a harness-wide fact about this benchmark family, not a fact about this task.

## Coordination done (and one correction I owe)

- **Row-id mapping, converged.** Three artefacts need one `sid → upstream` map. `R46ExecC3Spec` pinned it in
  `plans/pkg-spec-r46.json`; I adopted it and told `R46ScribeC3Rows`, who renumbered and re-gated their rows to
  it. Final: `S166` test_outputs.py, `S167` test.sh, `S168` instruction.md, `S169` solve.sh, `S170` Dockerfile,
  `S171` task.toml, `S172` README.md; `gitignore` is a capture with no row. My entry's provenance lines and
  Falsifier cite exactly this.
- **`SHA256SUMS` divergence.** Three orderings of the same eight digest/name pairs existed. Line order is not a
  gate input (`c_captures` parses line by line; `sha256sum -c` is order-free), so I withdrew mine and told
  `R46ScribeC3Rows` to land `R46ExecC3Capture`'s bytes and pin that file's digest in the spec.
- **Correction to `R46ScoutC3Grader.md`** (read as input, not adopted): its line numbers are wrong with at
  least three different offsets — `|7|`→`:10`, `|14|`→`:17`, `|15|`→`:18` (+3), `|22–24|`→`:23-25` (+1),
  `|26|`→`:27` (+1), its "combined assert" `|32|`→`:44` (+12), and its prose `tests/test.sh:17` for "invoke
  pytest" where pytest is `:18-22`. It also calls the listing check "ordering-sensitive": it is not, since with
  one expected element `os.listdir` order cannot matter and any two-entry listing fails regardless of order. I
  told `R46ScribeC3Rows` all of this; the "+3" phrasing in my first message was itself an overclaim and is
  retracted there.

## Touched surfaces

Written, all of them mine:

```
.ufo/waves/round-46/w1/R46ScribeC3Entry.md                        this report
.ufo/waves/round-46/w1/R46ScribeC3Entry/tb2-polyglot-c-py-grader.md   the entry draft to land at
                                                                     corpus/knowledge/
.ufo/waves/round-46/w1/R46ScribeC3Entry/sources-rows-S166-S172.md    id map, manifest statement, index row,
                                                                     coverage bullet, frontier bullet, PROVINCE
                                                                     line, spec fields
.ufo/waves/round-46/w1/R46ScribeC3Entry/gate-run.txt               P3-P8 + shape + predictor receipt
.ufo/waves/round-46/w1/R46ScribeC3Entry/anchor-run.txt             anchor-line rule receipt
.ufo/waves/round-46/w1/R46ScribeC3Entry/verify_gate.py             the harness behind gate-run.txt
.ufo/waves/round-46/w1/R46ScribeC3Entry/anchor_rule.py             the harness behind anchor-run.txt
```

Not touched: `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `PROVINCE.md`, `SKILL.md`, `SHONEN.md`,
the jj state, the Git index, the fleet root, sibling lanes. One incidental artefact was created and removed:
importing `plans/pkg_gate.py` wrote `plans/__pycache__/pkg_gate.cpython-314.pyc`; I deleted it and every later
run sets `sys.dont_write_bytecode` and runs under the envelope with `/home/vgpnk` read-only. No
`git`/`jj` command that mutates anything was run; `git status` was read twice, read-only.

## Out of scope for this seat (for the L1)

- The captured grader has **not** been executed on any end state. The 16 `Observed` cells, the derived
  requirement labels and the receipt are owed to `plans/polyglot_c_py_probe.py` after the stage-2 freeze.
- `plans/polyglot_c_py_probe.py`, `plans/round46_c3_verify.py`, `plans/pkg-spec-r46.json`, the capture
  directory and its `SHA256SUMS`, and the SOURCES rows are other seats' artifacts; this seat supplies only the
  entry and the scaffolding text for the README/PROVINCE lines.
- No V1-V13 counter was written or run, and no `pkg_gate.py package --rerun` was run (that would execute the
  probe; forbidden before stage 2). The six clauses I did run are the gate's read-only clauses P3-P8.
- The `lookup-print` and `fib-wrong` end states are **described, not built**. Their verdicts are predictions
  until the receipt exists.

## Known limits of the draft

- The requirement-map labels are predictions from the frozen case set, not receipt-derived. `fib` is the cell
  most likely to move; the entry says so in a paragraph the L1 must delete after re-deriving.
- The `## Case table` `Tests` letters are the same predictions; the `Observed` column is `TBD` everywhere, so
  `V9`-style byte-equality with the receipt is a stage-2 fill, not a state this draft can reach.
- The predictor's domain is `(listing × polyglot-or-not)`. If the counter's held-out set contains a semantic
  mutant, the predictor will disagree with the grader and the counter will report a defect — that is a domain
  violation on the counter's side, and the entry says so in `## Limits` and `## Predictor`.
- Two facts are read off the source and not executed: the non-idempotence in finding 1, and the claim that a
  bare-CR-only source cannot compile. Both are falsifiable from the receipt.

Artifact digests: entry `76318ca8…46f4c`, scaffolding `0ea888eb…567f`, `gate-run.txt` `030819ff…6b86d`,
`anchor-run.txt` `934ee4f0…3334a8d`. Scratch `/fast/scratch/hyaku/kengaku-r46/R46ScribeC3Entry` is removed on exit;
`R46ScribeC3Entry/` under `w1` holds the receipts that matter.


## Addendum after yield — anchor cells verified, and a divergence to resolve

`R46ExecC3Spec` published the seven copy-ready anchor cells its `V12` validates; I re-fetched the seven files
from the pin into a throwaway `/tmp` dir and ran the frozen `anchor_line_check` rule plus `V12`'s extras
(exactly one 64-hex per cell, no straight double quote inside the quoted text, word count ==
`len(quote.split())`, range contains the cited line, cell `sha256` == the fetched bytes):

```
S166 ok [test_outputs.py:44 words=8]   S167 ok [test.sh:22 words=5]    S168 ok [instruction.md:1 words=16]
S169 ok [solve.sh:12 words=4]          S170 ok [Dockerfile:6 words=9]  S171 ok [task.toml:22 words=3]
S172 ok [README.md:4 words=12]         ANCHORCELLS checked=7 defective=0
```

**Two row drafts exist; land one whole — never a blend. Retraction.** `R46ScribeC3Rows`' final rows quote
different lines from Spec's set (its S166 quotes `:18` with three quotes in the cell, S171 `:34`, S172 `:24`,
S170 `:2`). I first reported that as a `V12` violation; that was an inference from a prose summary of `V12`,
not a measurement, and it is wrong. `R46ExecC3Spec` then measured both sets against the counter's actual `V12`
and both are clean (Rows 19 quotes / 0 defects; Spec 7 / 0), because `V12` unescapes `\"` before the line
compare, iterates every quote in a cell, and imposes no word floor on registry cells — the 3-word floor is
`entry_rules.quote_words`, which `P3` applies to this entry's `## Located quotes`. The only observation that
survives is editorial: quote text, word count and range belong to one cell, so land one set whole and never
mix them. Spec's seven cells are copied verbatim in
`w1/R46ScribeC3Entry/sources-rows-S166-S172.md` §"Anchor cells to land" and were independently verified here
(7/7 ok); Rows' set is equally admissible. `S170` stays range-less, `S172` keeps `1-24`.

One consequence worth recording, because it decides *which* set the L1 should prefer without costing the
package any evidence: two claims that Rows' `teaches` cells assert are **not** carried by Spec's anchor cells —
the instruction's own `gcc` command producing the forbidden second entry (needs `instruction.md:5`, Spec quotes
`:1`) and the published case table (needs `README.md:24`, Spec quotes `:4`). Neither is a gate failure: no rule
ties `teaches` to its row's anchor. And the entry is self-evidencing for both — `## Located quotes` carries
`instruction.md:5` (7 words) and `README.md:24` (5 words), verified verbatim by the gate's `P4`. So either set
leaves the package sound; a set whose anchors *do* carry the `teaches` claims only makes each row readable on
its own.

This addendum changes no measured number above and no verdict: the entry draft is unchanged
(`76318ca8…46f4c`), and the scaffolding file is now `0ea888eb…567f`.

VERDICT: c3-entry-sections-9-tbd-16
