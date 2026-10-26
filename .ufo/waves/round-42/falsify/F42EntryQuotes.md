# F42EntryQuotes — quote / requirement-map / case-table audit of `tb2-circuit-fibsqrt-grader.md`

Seat: F42EntryQuotes (reviewer), kengaku r42 wave 2 (FALSIFY), 2026-10-26.
Target: `corpus/knowledge/tb2-circuit-fibsqrt-grader.md` (sha256 `b692435aa5aa8c1659a7e14884fe809d73ae738b15f85f77e081a5c8919da0f8`).
Evidence: `corpus/evidence/round42/tb2-circuit-fibsqrt/` (all nine captures `sha256sum -c SHA256SUMS` → 9× OK, this seat), `corpus/evidence/round42/fibsqrt-probe.txt` (sha256 `2a54ca8a76619a173280727938441fcf129ddcd482cc0a4d55f65b38d41ad92a`), `plans/fibsqrt_probe.py`, wave-1 reports under `.ufo/waves/round-42/build/` (`R42CritProbe`, `R42ScoutHarborCwd`, `R42ScoutPriorArt`, `R42CritPytest`) and `.ufo/waves/round-41/build/R41PlanNext.md`.

Envelope note: this seat ran no battery, counter or fixture build — read-only verification plus in-kernel computation, no writes outside this report and `falsify/F42EntryQuotes/`; the bwrap envelope did not apply. No scratch used, nothing over 50 MB, no tool installed (nothing needed; no pacman use).

Method: (a) parse the entry's `## Located quotes` table and compare each quote byte-for-byte against the cited capture line (whitespace-split word count); (b) parse the receipt's 16 `CASE` rows, derive every tag's violator set and label (`enforced` iff all violators fail, `unenforced` iff all pass, `partly` otherwise — the V7 rule, confirmed identical at `plans/round42_c2_verify.py:224-228`), and diff against the entry's `## Requirement map`; (c) diff the `## Case table` row by row against the receipt; (d) check every factual sentence of `## Findings` and `## Wave-1 integration` against the captures, the receipt, the frozen probe builder (imported read-only: `sys.modules` pre-registration then `exec_module`), and the cited wave-1 reports.

## 1. Located quotes — 24/24 verbatim, all within 3-25 words

Parsed 24 rows (entry:125-148). Every quote is byte-exact at its cited `capture:line` (13 are the full line, 11 are contiguous substrings of that line — e.g. entry:125's quote is a suffix of `instruction.md:1`, which begins "The file /app/sim.c is a logic-gate simulator:"). Word counts (whitespace tokens), in row order:

13, 13, 16, 7, 9, 7, 7, 15, 7, 3, 9, 6, 10, 3, 5, 10, 5, 13, 8, 11, 6, 14, 13, 7 — all in [3,25]. Minimum 3 (`fib_n = fibonacci(isqrt(n))`, `#define MAX_SIGNALS 32000`), maximum 16.

**Result: 24/24 good.** No quote edited, no line mis-cited, no word count out of range.

## 2. Requirement map — 7/7 labels derive from the receipt; cited case sets exact

Derived from the receipt (`violates=` × `observed`), all seven tags:

| tag | receipt violators (pass/fail) | derived label | entry label | cited set = derived set |
|---|---|---|---|---|
| `line-form` | comment-lines (P) — 1 | unenforced | unenforced | yes |
| `last-32-lines` | reversed-lines (P) — 1 | unenforced | unenforced | yes |
| `gates-file` | no-gates-file (F), gates-is-directory (F) — 2 | enforced | enforced | yes |
| `line-limit` | padded-32000 (F) — 1 | enforced | enforced | yes |
| `output-function` | 15 cases, 6 pass / 9 fail | partly | partly | yes |
| `example-208` | 14 cases, 5 pass / 9 fail | partly | partly | yes |
| `example-20000` | 14 cases, 5 pass / 9 fail | partly | partly | yes |

Zero extra and zero missing cases in every cited list (oracle-solve-sh, the only untagged case, is the only case absent from `output-function`). The map's prose counts all check: two enforced / five not; single-witness `line-form`, `last-32-lines`; `gates-file` twice-witnessed; 15/14/14 wide-partly counts; seven tags on five instruction lines; lines 8 and 10 carry no tag (`TAGS`, `fibsqrt_probe.py:76-84`); "every tag has at least one violating case" holds. **Result: 7/7 rows correct, no defect.**

## 3. Case table — 16/16 rows match the receipt, in receipt order

Row-by-row diff of case id, `tests=` letters and `observed` against `fibsqrt-probe.txt`: 16/16 equal, order identical, `match=yes` and `regrade=same` on every receipt row; receipt footer `cases=16 observed_pass=7 observed_fail=9 mismatches=0`, `regrade cases=16 differ=0` matches the table's 7 pass / 9 fail. The per-row "What the end state is" paraphrases agree with the receipt's case text and with the frozen builder (`Case` list, `fibsqrt_probe.py:160-197`: e.g. trailing-space = `[x+" " for x in L28]`, padded rows = `L28 + [""]*n` appended after the gates). **Result: 16/16 correct, no defect.**

## 4. Findings and Wave-1 integration — 4 bad sentences (+1 citation nit)

Verified and held up: finding 1 (28-value list `test_outputs.py:73-102` = `GRADED`; circuit composition **re-derived by importing the frozen probe**: `len(L28)=1195` = 32 self-copies + 32 NOT + 868 AND + 231 OR (= 1099 binary) + 32 final copies, 0 constant lines — exactly as entry:244 states; `violates=example-208,example-20000` on a pass is receipt line 5; round-41 cross-ref R41PlanNext §3.2:154-163 has `./sim 208 → 0 ; ./sim 20000 → 0`, grader 3/3, `wc -l 1195`). Finding 2 (gates.txt is 33 lines = 32 self-copies + `out32 = 0`; `sim.c:340` prints nothing at `num_signals==0`; `int("")` at `:127` caught `:128-131`; constraints-scheduling entry:220 has `nop, FFF`). Finding 3 (30804 = 31999−1195). Finding 4 (`sim.c:117-118`, `:343`; `# note` skipped at `:113-115` before the index is read). Finding 5 (mechanism matches sim.c bytes: `:122-126`, `:156`, zero-init `OP_CONST_0` at `:9`; "one trailing space on the last line clears exactly bit 31" and "binary gates keep working" are both in R42CritProbe D1's measured table verbatim; 0-constants scope confirmed by my import; the CRLF `[INFERENCE]` is correctly labelled and matches `strcmp` at `:122-125`). Finding 6 (`:66` relative `-o sim`, `:119` `/app/sim`, `Dockerfile:3` = `WORKDIR /app`; probe docstring does fix cwd `/app`; inference labelled). Finding 8 (receipt carries `test_gates_file_size:error=IsADirectoryError`; `:20`, `:126-131`, `sim.c:340`). Finding 10's core (`instruction.md:8`; `sim.c:322-331` argv seed; `:328` comment vs `:330` `(input_value >> (i)) & 1`; `sim.c` contains no stdin/scanf/getchar/gets/fgetc/fread/read token — grep, 0 matches). Wave-1 integration bullets D1 (docstring phrase quoted verbatim, `fibsqrt_probe.py:27`), D3 (no line-8 tag in `TAGS`, no case in receipt), D4 (R42ScoutHarborCwd §4: nine of sixteen move, `fake-sim-script` PPF→PPP, measured `mismatches=9`), D5 (probe `PINS` = 5 of 9 captures; the C2 counter's `CAPTURES` at `round42_c2_verify.py:58-68` covers the other four; V1 checks SHA256SUMS + bytes), prior art (six findings, audit.txt:460 quote, S128 issue #9645 closed 2026-09-25, TB2.1 main nine files byte-identical — all present in R42ScoutPriorArt; S128 row present in `corpus/SOURCES.md:143`), and the pytest-parity bullet (R42CritPytest: 16/16, pytest 8.4.1 / Python 3.13.16).

### Bad sentences (wrong / unsupported / overclaim)

1. **entry:297 — wrong.** "maximum, 48401 = 220²+1, is the only reach above 2^15" (finding 7). Six of the 28 graded inputs lie above 2^15 = 32768: 43680, 43681, 43682 (x=209 family) and 48399, 48400, 48401 (x=220 family). Derived from `test_outputs.py:73-102` via the frozen `GRADED` list (28 values, max 48401). 48401 is the maximum, not the only large input.
2. **entry:311 — wrong (fact and locator).** "the probe runs every case with stdin on `/dev/null` (probe docstring — the oracle case's own `solve.sh` recipe included)" (finding 10). Only the case recipe gets `stdin=subprocess.DEVNULL` (`fibsqrt_probe.py:201`); the graded `/app/sim` calls (`test_outputs.py:119`) inherit the harness's stdin, which inherits the probe caller's stdin (`run_case`'s `subprocess.run` sets no stdin). The probe docstring contains no `/dev/null`/DEVNULL statement (its only stdin mention, `:27-28`, is that sim.c reads argv) — and wave-1 R42CritProbe D3 documents exactly this gap ("stdin is not pinned where it would matter"). The finding's conclusion survives on "sim.c never reads stdin" (grep 0 matches), not on this sentence.
3. **entry:431 — overclaim.** "`lookup-28-padded-31999` and `lookup-28-padded-32000` … so they too pass only because the print window is the 32 highest-indexed signals" (integration, D2 bullet). `lookup-28-padded-32000` is observed `fail` (`PFP`, receipt row 10); only its value test passes for that reason. True for padded-31999 alone.
4. **entry:433-434 — wrong under the bullet's own counterfactual.** "they would carry `last-32-lines` and `line-form` as well … Neither changes a requirement-map label (`last-32-lines` and `line-form` stay `unenforced`)". If both padded rows carried those tags, `padded-32000` (observed fail) enters both violator sets and both labels become `partly`, not `unenforced`. They stay `unenforced` only because the frozen receipt omits the tags. The error originates in wave-1 `R42CritProbe` D2 ("all tagged cases pass" — false for padded-32000); the entry repeats it.

### Citation nit (not counted above; content is supported)

- entry:306 (finding 9): the asserts of existence are at `test_outputs.py:11` (test 1) and `:18` (test 2); the cited `(:9, :16, :18)` names two `Path` assignments and only test 2's assert, omitting `:11`.

## 5. Residual risk and verification gaps

- I did not re-execute the probe or its 16 sandboxes; the receipt is taken as frozen (wave-1 R42CritProbe re-ran it byte-identical and the landing re-run is byte-equal per the claims file). My composition check imports the builder and re-derives the circuits; it does not re-grade them.
- The external prior-art quotes (audit.txt:460, issue #9645 body) are taken from the wave-1 scout's report, not re-fetched; S128's SOURCES row corroborates the issue's existence, dates and closed state.
- `R42CritPytest`'s parity run and `R42ScoutHarborCwd`'s cwd experiment are taken from their reports (both carry Q32 envelopes and artifact digests); not re-run here.
- The `2^15` sentence's fix is one word deep (e.g. "the largest of six inputs above 2^15") and the stdin sentence should be reworded to the D3-accurate form ("the recipe's stdin is /dev/null; sim.c never reads stdin, so the graded channel is argv regardless"); both are L1 edits, none frozen was touched by this seat.

VERDICT: entry-quotes-ok-24/24-bad-sentences-4
