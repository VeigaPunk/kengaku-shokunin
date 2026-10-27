# R46ScribeC3Entry — package scaffolding for the C3 `polyglot-c-py` entry

**The registry rows are NOT duplicated here.** The row artifact is `R46ScribeC3Rows/rows.md`; this file fixes
the id mapping all three C3 artifacts share, and carries the pieces only the entry seat produces (capture
manifest, README index/coverage/frontier text, PROVINCE line, spec fields).

## Converged id → file mapping (binding; `plans/pkg-spec-r46.json` is pinned to it)

| id | upstream path | capture name | sha256 |
|---|---|---|---|
| S166 | `tests/test_outputs.py` | `test_outputs.py` | `b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec` |
| S167 | `tests/test.sh` | `test.sh` | `4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334` |
| S168 | `instruction.md` | `instruction.md` | `a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96` |
| S169 | `solution/solve.sh` | `solve.sh` | `e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0` |
| S170 | `environment/Dockerfile` | `Dockerfile` | `2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a` |
| S171 | `task.toml` | `task.toml` | `d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea` |
| S172 | `README.md` | `README.md` | `591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881` |
| — | `.gitignore` | `gitignore` | `9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953` |

`.gitignore` is captured and pinned but carries no row (round-45 precedent; byte-identical to
`corpus/evidence/round45/tb2-password-recovery/gitignore`).

## Anchor cells to land (R46ExecC3Spec's set, independently re-verified here)

`R46ExecC3Spec` publishes the copy-ready cells its counter `V12` validates. I re-fetched all seven files from
the pin into a throwaway `/tmp` dir and ran the frozen `plans/anchor_line_check.py` rule plus the `V12`
extras (exactly one 64-hex after `sha256`, no straight double quote inside the quoted text, word count ==
`len(quote.split())`, range contains the cited line):

```
S166: ok [test_outputs.py:44 words=8]      S167: ok [test.sh:22 words=5]
S168: ok [instruction.md:1 words=16]       S169: ok [solve.sh:12 words=4]
S170: ok [Dockerfile:6 words=9]            S171: ok [task.toml:22 words=3]
S172: ok [README.md:4 words=12]
ANCHORCELLS checked=7 defective=0
```

Each cell's `sha256` equals the freshly fetched bytes' digest. Land these seven cells verbatim:

```
S166 -> test_outputs.py:1-46, :44 "assert python_out == expected and c_out == expected" (8 words); sha256 b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
S167 -> test.sh:1-29, :22 "pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA" (5 words); sha256 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334
S168 -> instruction.md:1-9, :1 "Write me a single file in /app/polyglot/main.py.c which is a polyglot, that is, I can run" (16 words); sha256 a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96
S169 -> solve.sh:1-57, :12 "cat <<'EOF' > polyglot/main.py.c" (4 words); sha256 e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0
S170 -> :6 "RUN apt update -y && apt install -y gcc" (9 words); sha256 2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a
S171 -> task.toml:1-41, :22 "timeout_sec = 900.0" (3 words); sha256 d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea
S172 -> README.md:1-24, :4 "This task requires the agent to create a single polyglot source file" (12 words); sha256 591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881
```

**Two row drafts exist; land one whole — never a blend.** `R46ScribeC3Rows`' final rows quote different
lines from the set above: its S166 quotes `:18` (three quotes in the cell), S171 quotes `:34`, S172 quotes
`:24`, S170 quotes `:2`. I first read that as a rule conflict and said so; that was wrong and is retracted.
`R46ExecC3Spec` measured both sets against its counter's actual `V12` and both are clean — Rows 19 quotes /
0 defects, Spec's 7 / 0 — because V12 unescapes `\"` before the line compare, iterates every quote in a cell
(there is no one-quote-per-cell rule), and imposes no word floor on registry cells (the 3-word floor is
`entry_rules.quote_words`, which `P3` applies to the entry's `## Located quotes`, not to `SOURCES.md`). My
"violations" were inferred from a prose summary of `V12`, not measured against it; only my check of Spec's
seven cells (7/7 ok, above) was a measurement.

So the choice is editorial, and the only hard constraint is internal consistency: quote text, word count and
range belong to the same cell, so taking Rows' quoted text with Spec's word count would break the cell. Land
either set whole. The L1's cheapest path is Spec's seven cells (verified here) over Rows' id/kind/tier/
status/opened/recheck/used-by cells and `teaches` sentences; Rows' own set is equally admissible if the L1
prefers one author for the whole row.

## Capture manifest `corpus/evidence/round46/tb2-polyglot-c-py/SHA256SUMS`

**Line order is not pinned and carries no meaning**: `pkg_gate.c_captures` parses the file line by line
(`^([0-9a-f]{64})\s+\*?(\S+?)\*?$`) and `sha256sum -c` is order-free, so two manifests with the same eight
pairs are equivalent. The landed bytes are the **capture seat's** file
(`R46ExecC3Capture`); its own sha256 is the value to pin in `plans/pkg-spec-r46.json`. Two other orderings
existed in wave 1 (`R46ScribeC3Rows`' C-sorted file, and this seat's id-ordered fixture copy) and are
withdrawn in its favour. The eight pairs, order-free:

```
test_outputs.py  b94a7a9882decd8114835bdf52b5bc42fc78e9fe67ecad9bd19050b11781ddec
test.sh          4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334
instruction.md   a57c0c0e1232113113cd29a154ea7e0ac9ea45e4aedc16958fbc6bc753a4ef96
solve.sh         e768453a194037b0517803fa0d99dbd3b6f820dead842e0b6161019b33456bf0
Dockerfile       2eb537f29d2bc4ab30e1b35ff352578437a08b90f91ef6360ee28d8195d5098a
task.toml        d31b9f60c47eed0d79e10d3be8fd56a23e50b3986606e3f2546863d44ac9a9ea
README.md        591e27f9c71f12f6d0f0dc506970850737f951bfdb3f582196e89bc752e92881
gitignore        9a8dd8d9b6c3adb8e9e56328df27deef859a3e98fffc9b8133c8b22207c25953
```

Eight captures, seven rows. Every digest was verified byte-identical against two independent fetches of the
pin: the per-file `raw.githubusercontent.com` URL (HTTP 200) and the `codeload.github.com` source tarball at
`2fd12b88aafdd04a52c298e3940bcb189f9766d6` (`cmp` byte-clean on the seven row files; `gitignore` matched by sha256 only, and its digest equals round-45's captured `gitignore`).

`tests/test.sh`'s digest is byte-identical to round-45's `password-recovery` `tests/test.sh` (`4770437e…`,
that package's S153): the harness script is shared TB2 boilerplate, not task-specific content. It is a
task-level fact the entry uses (`## Findings` 8, `## Limits`), but it does not make S167 the same source as
S153 — different upstream path, different row.

## Index row for `corpus/README.md`

```
| `knowledge/tb2-polyglot-c-py-grader.md` | A twelfth Terminal-Bench 2.0 task grader read and executed, and a grader class new to this lane: `polyglot-c-py` grades a **source file executed by two toolchains at grading time** — `test_outputs.py:17-18` assert `os.listdir("/app/polyglot") == ["main.py.c"]` before anything is built, `:23-25` compile the graded file with `gcc -o /app/polyglot/cmain` *into that directory* (so the instruction's own command, run as a smoke test and left behind, fails the listing assert, and a re-grade in the same container always fails), and `:27-46` require `.stdout.strip()` to equal `267914296`/`55`/`0` from both `python3` and the compiled binary with `check=True` — so a polyglot carrying a three-entry lookup table passes while `f(1)`, named in the instruction, is never exercised; the executable reading is in `## Predictor` | Pinned at terminal-bench-2 `2fd12b88`: S166, S167, S168, S169, S170, S171, S172; captures + `SHA256SUMS` in `evidence/round46/tb2-polyglot-c-py/`; probe `plans/polyglot_c_py_probe.py`, receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`, spec `plans/pkg-spec-r46.json` |
```

## Coverage bullet for `corpus/README.md` `## Coverage map`

Must start with `- `, name the entry file and the receipt path (`gate P8`).

```
- **Terminal-Bench 2.0 task grader (twelfth task, dual-runtime execution class)**: covered at source-code depth and executed offline (round 46, 2026-10-27) — knowledge/tb2-polyglot-c-py-grader.md; S166-S172; probe `plans/polyglot_c_py_probe.py`, receipt `corpus/evidence/round46/polyglot-c-py-probe.txt`. A twelfth instance of the same ground (12 of the 89 TB2 task graders; not breadth, and no quality, validity, difficulty or gameability verdict), on `polyglot-c-py` only: the graded artefact is one agent-authored source file that the grader both compiles with gcc and runs with python3; the pre-build listing assert sees the directory before the grader's own build writes `cmain` into it; the instruction's published command produces the state that assert rejects; and the score is three fixed points of stripped stdout, so a lookup-table polyglot passes and `f(1)` is never tested. Not the task image, not the oracle's generality, not a harness run, not contamination, not model or agent behaviour.
```

## Frontier bullet for `corpus/README.md` `## Frontier`

```
  - *Partly discharged round 46 (2026-10-27):* `knowledge/tb2-polyglot-c-py-grader.md` reads and executes a
    twelfth Terminal-Bench 2.0 task's scoring code (`polyglot-c-py/tests/test_outputs.py` @ `2fd12b88`; S166,
    S167, S168) against its `instruction.md` and `README.md`, probe `plans/polyglot_c_py_probe.py`, receipt
    `corpus/evidence/round46/polyglot-c-py-probe.txt`. The graded state is a class the lane had not executed
    before: **the graded artefact is a program the grader itself builds and runs twice**, so the compile leg is
    a graded requirement rather than instrumentation, the pre-build listing equality is the only structural
    gate and it is blind to a directory bearing the right name, the grader's own `-o /app/polyglot/cmain`
    writes the forbidden second entry after the assert (so the instruction's published command fails the task
    and a second grade in the same container always fails), and three fixed-point literals are all that stand
    between a lookup table and full credit. The "Terminal-Bench 2.0's" clause is **narrowed for that one task
    only**; it stays open for the remaining TB2 task graders (12 of 89 read), for any SWE-bench Pro V2 grader
    beyond the round-31 one, and for runtime task validity (which `PROVINCE.md` refuses to this lane). Not the
    task image, the oracle or a harness run, not contamination, not model or agent behaviour.
```

## PROVINCE paragraph line

```
`polyglot-c-py` — `corpus/knowledge/tb2-polyglot-c-py-grader.md`: a twelfth TB2 grader (dual-runtime execution
class); the graded artefact is a single source file the grader compiles with gcc and runs with python3, and the
score is a pre-build directory listing plus three fixed-point stdout comparisons.
```

## Spec fields (`plans/pkg-spec-r46.json`, owned by R46ExecC3Spec)

```
entry            corpus/knowledge/tb2-polyglot-c-py-grader.md
capture_dir      corpus/evidence/round46/tb2-polyglot-c-py
receipt          corpus/evidence/round46/polyglot-c-py-probe.txt
probe_cmd        ["plans/polyglot_c_py_probe.py", "--lane", "."]
raw_base         https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/polyglot-c-py/
rows             the seven-row mapping table above
entry_rules      verified_at 2026-10-27 ; min_quotes 10 ; min_distinct_locations 10 ; quote_words [3,25] ;
                 min_teaches_words 8 ; row_opened 2026-10-27 ; row_tier A ; row_status mined
frozen_instruments  plans/polyglot_c_py_probe.py (digest at stage 2), plans/pkg_gate.py @
                 ea63882240e67e9906e481f3d652f94366c288dc91991bafbfcd651a766edd41
```
