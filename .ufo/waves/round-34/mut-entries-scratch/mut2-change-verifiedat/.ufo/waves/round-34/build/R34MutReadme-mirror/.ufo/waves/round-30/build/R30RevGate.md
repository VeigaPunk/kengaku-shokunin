# R30RevGate — review of the quote-validator patch for gaming paths

Seat: L1Kengaku30.R30RevGate (leaf reviewer). Round 30, kengaku, hyaku run 6, 2026-10-25.
No lane byte was edited by this seat; this report is the only file written in the lane.

## 0. What I reviewed, and the exact bytes

| item | value |
|---|---|
| body under review (committed path) | `plans/sources_adopt.py`, sha256 `e9b6bc044bd5337565d78701c13287eba163c90b13199f4cf8610d27d191a195`, 35275 B — this is the byte the C3 predicate will be measured on |
| body named by the seat | `/tmp/r30-GateQuote/sources_adopt.py`, sha256 `f26ed9bb94086e9e9a7c3d7812608870e3fd1de441d5fe10fcff380f7b14609d`, 33956 B — **not** the same bytes: the committed file adds two anti-mutant assertions inside selftest case 12 (one-token quote; 20-character-prefix quote). Every result below was produced or re-produced on `e9b6bc04`. |
| pre-change body | `git show HEAD:plans/sources_adopt.py` → sha256 `6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2` (also what the working tree held at 04:23:31; `git status` at 04:21:40 did not list the file) |
| lane state at review | `git status` shows ` M plans/sources_adopt.py` (`git diff --stat` → `336 insertions(+), 3 deletions(-)`) and the registry already carries **88** rows (S081–S086 appended). The mtime of `plans/sources_adopt.py` is 04:33:20, i.e. the copy into `plans/` landed after the seat that wrote it was told to write `/tmp` only. Not mine to rule on; recorded because the C3 control argument depends on which bytes are which. |
| scratch | `/tmp/r30-R30RevGate/` — `attack.py`, `equiv` runs, fixtures under `fx/`, mutants. Nothing written under `plans/`, `corpus/`, or `/home/vgpnk/Projects/shokuknow`. |
| tooling installed | **none** — no pacman transaction, no `uv tool`, no download. |
| method | the bodies were snapshotted, then attacked twice over: CLI (`python3 <body> …`) and in-process (`quote_check`/`quoted_spans` imported from the snapshot). I watched the seat rewrite its file twice (`20819 B`/`7e81511c` → `33030 B`/`93ee7f7c` → `33956 B`/`f26ed9bb`) before the committed variant appeared; results below are pinned to `e9b6bc04`. |

Read-only sources used: `plans/round-30-claims.md` C3, `corpus/lessons/round-29-verifier-spotcheck.md` §5 quality,
`corpus/SOURCES.md:7`/`:11` and the S081/S084/S085/S086 rows, `corpus/QUALITY.md:32-34`,
`.ufo/waves/round-30/claims/gate-before.txt`, `/tmp/r30-BuildAppend/pre-SOURCES.md` + `SOURCES.append.r30.md`,
`/tmp/r30-R30SrcS08{1..6}/` (the seats' own fetches).

## 1. Direct answers to (a)–(e)

**(a) Can a caller pass an artifact they fetched that differs from the cited URL and still pass?** Yes, and the
tool has no instrument to notice. The artifact is a caller-supplied path; the row's `source` cell is never read by
the quote path (`quote_check` touches only `row.cell(5)`), there is no URL fetch, no sha256 pin, and no artifact
hash in the receipt. Three sharper variants all pass: the artifact may be **the row file itself** (G2), **the live
registry** (G3), or **a scratch script the seat wrote** (real, G4/S083), and a caller may substitute a rewritten
derivative for the capture (real, G17/S086).

**(b) Does newline normalisation make a quote pass that crosses a line break in the source?** It should; it does
not. `normalize_text` folds line-*ending style* only (`\r\n`→`\n`, `\r`→`\n`) on both sides, so a CRLF capture of
the same document locates (G12b: exit 0) while a quote written with a space where the source has a newline does
**not** locate (G12a: exit 7). No anchor cell can carry a literal newline — `parse_rows` splits on lines — so the
wrap case is unreachable from the CLI and is always refused. On real bytes this is a false refusal: the S085
staged quote is present in `caict.txt` but the extraction wraps it after character 20 (`…即测\n试数据标签化管理…`).
Selftest case 13 does not exercise this: its wrap assertion is `locates(f"intro\n{first}", wrapped)`, i.e. a quote
that already contains `\n`, which no row can reach.

**(c) Does the word counter treat Chinese/Japanese runs as one word, and is that stated?** Yes to the first —
`words()` is `len(text.split())`, so a CJK run with no spaces is **1 word**. It is **not stated in the tool or the
contract**: the module docstring says "≤25-word cap"; `--quote-file`/`--artifact` help say nothing about counting;
`corpus/SOURCES.md:7` says "a ≤25-word quote per row"; `corpus/QUALITY.md:32-34` says "≤25 words … the length rule
is SOURCES contract v1 rule 1", and `rule 1` exists nowhere as a numbered rule (`grep -rn "rule 1" CORPUS.md
corpus/SOURCES.md corpus/QUALITY.md corpus/README.md` → **one** hit, the QUALITY cross-reference itself). The only
statement of the unit is the code comment `words is the same counter round30_defects.words uses`, which is true
(`plans/round30_defects.py:38-39` is the same `len(text.split())`) but circular. The lane has, however, started
stating the unit **inside a row**: the appended S085 anchor reads `…“方升”… (3 whitespace tokens); … (1 whitespace
token, 23 CJK characters)`. Measured consequence of the undocumented rule: an 84-character Chinese span is
`words=1` and passes (G5); the same information in English is `words=48` and is refused (G5b, exit 6). Every CJK
row this round appended is inert under the cap — S084 `[3, 7, 1]`, S086 `[1, 3]`, S085 unquotable at all (G20).

**(d) Can a caller trivially disable the check with a flag combination?** Several ways, all silent:
`--selftest` returns 0 over a failing `--quote-file/--artifact` pair (G10a); quote flags **supersede** an admit run
and return before `--out` is written, exit 0 (G10b); the default append invocation never enters quote mode (G11);
an empty or misspelt quote file is a green `rows=0` run (G8, G9); a fabricated id is accepted without ever being
compared to `--registry` (G14); and an anchor that quotes with curly marks is refused outright rather than checked
(G20).

**(e) Are the existing exit codes and outputs unchanged?** Yes on the committed body, measured byte-for-byte —
stdout, stderr, exit code and the written append block are identical for every pre-existing invocation I could
construct, and the ten original selftest cases keep their names and verdicts. The one caveat is help/usage: the
usage line on stderr grew by the two new options (328 → 398 B), so "byte-identical for existing invocations" is
literally false for `--help`, and should be stated as "stdout, exit codes and written artefacts".

## 2. Named gaming paths

`G=/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/sources_adopt.py`; fixtures under `/tmp/r30-R30RevGate/fx/`.
Each entry is the command I ran and the first line of its observed output.

### HIGH — the artifact is unbound from the cited source

| id | path | command | observed |
|---|---|---|---|
| G1 | caller writes the artifact by hand; the row cites a real URL | `python3 $G --quote-file fx/rows_s078.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · `QUOTE rows=1 spans=2 located=2 found=2 … artifacts=art_fabricated.txt` — the row cites `raw.githubusercontent.com/scaleapi/SWE-bench_Pro-os/…/v2/README.md`; the artifact is a file I typed |
| G2 | **the row file is its own artifact** — the quote exists nowhere else | `python3 $G --quote-file fx/rows_unique.txt --artifact fx/rows_unique.txt` | `EXIT 0` · `ok S910 words=11 at rows_unique.txt quote="a unique sentence that exists only inside the supplied row file"` |
| G2b | a directory containing the row file | `python3 $G --quote-file fx/selfdir/rows_unique.txt --artifact fx/selfdir` | `EXIT 0` · same `ok` line; `artifacts=rows_s078.txt,rows_unique.txt` |
| G3 | **the live registry is the artifact** — existing rows self-validate | `python3 $G --quote-file fx/rows_s078.txt --artifact corpus/SOURCES.md` | `EXIT 0` · `located=2 … artifacts=SOURCES.md` |
| G4 | directory recursion admits the seat's own scratch files | §3, S083 | `ok S083 words=14 at verify.py` — `verify.py:6` is the seat's own script carrying the quote string |
| G17 | **a rewritten derivative replaces the capture** | `python3 $G --quote-file fx/rows_r30_S086.txt --artifact /tmp/r30-R30SrcS086/Q2-11.raw.txt` vs `…/Q2-11.unwrapped.txt` | raw: `EXIT 7`, both spans `absent`; unwrapped: `EXIT 0`, both `ok … at Q2-11.unwrapped.txt` |

G4 and G17 are this round's own ground: the S083 seat left the quote verbatim in its helper script, and the S086
seat had to build `Q2-11.unwrapped.txt` before its quotes would locate. In both cases the gate's green is evidence
about a file the lane wrote, not about the fetched bytes at the cited URL.

### HIGH — the check is not on the append path

| id | path | command | observed |
|---|---|---|---|
| G11 | the invocation that appends never validates a quote | `python3 $G --registry /tmp/r30-BuildAppend/pre-SOURCES.md --package fx/rows_r30_S081.txt --admit-ids S081 --scope-to-admit --access-date 2026-10-25 --entries corpus/knowledge/contamination-transparency-card.md --attest-opened` | `EXIT 0` · `registry=82 staged=1 collisions=0 malformed=0 duplicates=0 defects=0 prose=1` + block; **no `QUOTE` line at all** |
| G10b | adding quote flags silently **cancels** the append | the same admit run + `--out /tmp/r30-R30RevGate/should-not-exist.md --quote-file fx/rows_s078.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · only `QUOTE …`; **`--out` file does not exist** |
| G10a | `--selftest` swallows a failing quote invocation | `python3 $G --selftest --quote-file fx/rows_both.txt --artifact /nonexistent/x` | `EXIT 0` · `SELFTEST cases=14 failed=0` |

Precedence in `main` is `if args.selftest: return selftest()` then `if args.quote_file or args.artifact: … return code`
— neither combination is a parser error, so a wrapper that adds quote flags to an admit run gets a green exit and no
block, and habitually passing `--selftest` masks a broken quote pair.

### HIGH — the length rule is inert where it matters

| id | path | command | observed |
|---|---|---|---|
| G5 | CJK run = 1 word | `python3 $G --quote-file fx/rows_cjk.txt --artifact fx/art_cjk.txt` | `EXIT 0` · `ok S904 words=1` for an 84-character Chinese span |
| G5b | the same information in English | `python3 $G --quote-file fx/rows_english48.txt --artifact fx/art_english48.txt` | `EXIT 6` · `REFUSED S905 overlong words=48 cap=25` |
| G6 | zero-width joiner glues 60 repeats into one token | `python3 $G --quote-file fx/rows_zwsp.txt --artifact fx/art_zwsp.txt` | `EXIT 0` · `ok S906 words=1` |
| G18 | a one-space "quote" is words=0 and locates everywhere | `python3 $G --quote-file fx/rows_space.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · `ok S911 words=0 … quote=" "` |
| G7 | only ASCII-quoted spans are measured; cell prose is unbounded | `python3 $G --quote-file fx/rows_prose.txt --artifact fx/art_prose.txt` | `EXIT 0` · `ok S901 words=8` for a cell carrying 200 unquoted padding words |
| G19 | the printed `(N words)` annotation is never checked | `python3 $G --quote-file fx/rows_badcount.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · `ok S912 words=8` for a cell annotated `(23 words)` |

G19 is exactly the D3 class the round is closing: a receipt whose printed count disagrees with its quote stays
invisible to the gate built to price quotes. (This round the lane prints a unit — "(3 whitespace tokens)", "(1
whitespace token, 23 CJK characters)" — but the gate reads neither the count nor the unit.)

### MEDIUM — acceptance alphabet, vacuity, and refusals a caller can route around

| id | path | command | observed |
|---|---|---|---|
| G20 | **an anchor quoted with curly marks is refused, not checked** | `python3 $G --quote-file fx/live_S085.txt --artifact /tmp/r30-R30SrcS085` | `EXIT 4` · `QUOTE rows=1 spans=0 … malformed=1` — the appended S085 row quotes `“方升”`; `QUOTE_SPAN_RE` is `"([^"]+)"` (ASCII only), so the one row of the six that carries a real located CJK quote is the one the gate cannot read |
| G8 | empty quote file is green | `python3 $G --quote-file fx/rows_empty.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · `rows=0 spans=0 … malformed=0` |
| G9 | a row whose id misses the census anchor is never seen | `python3 $G --quote-file fx/rows_typo.txt --artifact fx/art_prose.txt` (`\| S99 \|`) | `EXIT 0` · `rows=0` — not even counted malformed |
| G14 | fabricated id, never cross-checked | `python3 $G --quote-file fx/rows_fake_id.txt --artifact fx/art_fabricated.txt` | `EXIT 0` · `ok S999 words=8` |
| G12a | quote crossing a source line break | `python3 $G --quote-file fx/rows_wrap.txt --artifact fx/art_wrap.txt` | `EXIT 7` · `REFUSED S903 absent` (same with an indented wrap) |
| G12b | the same document captured with CRLF | `python3 $G --quote-file fx/rows_wrap.txt --artifact fx/art_crlf.txt` | `EXIT 0` · `ok S903 words=8` |
| G15 | an anchor with no ASCII quote is structural (exit 4), and there is no `--scope-to-quote` analogue to `--scope-to-admit` | `python3 $G --quote-file fx/rows_noquote.txt --artifact fx/art_prose.txt` | `EXIT 4` · `REFUSED S902 no-quote` |
| G16 | therefore the mode cannot be pointed at the registry it guards | `python3 $G --quote-file corpus/SOURCES.md --artifact corpus/SOURCES.md` | `EXIT 4` · `rows=88 spans=23 located=23 malformed=77` — **77 of 88 live rows carry no ASCII-quoted anchor** |

### LOW — diagnostic ambiguity

| id | path | command | observed |
|---|---|---|---|
| G13 | exit 2 now means three things: argparse usage error, `--quote-file` without `--artifact`, unreadable artifact | `… --quote-file fx/rows_both.txt --artifact /nonexistent/x` → `EXIT 2` (`QUOTE cap=25 problem=--artifact names no file or directory`); `… --quote-file fx/rows_both.txt` → `EXIT 2` (`error: --quote-file and --artifact must be given together`) | both `2`; `2` is also the code C3's control uses for "the control cannot reach the target", so the control line must stay pinned to `git show <baseline>` bytes (it is) |
| — | a non-UTF-8 file inside an artifact directory is dropped silently when at least one file loads | `python3 $G --quote-file fx/rows_s078.txt --artifact fx/mixed` | `artifacts=a_good.txt`; `b_bad.bin` is never named (the skip list prints only when nothing loads) |

Exit precedence, measured: overlong+absent → 6, absent only → 7, overlong only → 6, and both refused rows are named
in the 6 receipt, so the docstring's "every refused row is still named" holds.

## 3. The round's own six rows, against the seats' own fetches

Rows extracted from the **live** `corpus/SOURCES.md` after the append; artifact = that source's fetch directory.

| id | exit | what the gate said |
|---|---|---|
| S081 | 0 | `spans=3 located=3 found=3 overlong=0` — appended words `[22, 6, 18]`. The **round-29 staged package** carries the same row with a 30-word first span and is **refused** (`EXIT 6`, `REFUSED S081 overlong words=30 cap=25`); the appended row was cut and is compliant. |
| S082 | 0 | `spans=2 located=2` (`words=11`, `words=17`, both `at s082-html.html`) |
| S083 | 0 | `spans=2 located=2`; the first — `words=14 … "a contamination-resistant design by separating the publicly released game engine from hidden card implementations"` — resolves to **`verify.py`**, the seat's own script (`verify.py:6`), not to the PDF |
| S084 | 0 | `spans=3 located=3`, words `[3, 7, 1]` |
| S085 | **4** | `spans=0 … malformed=1` — curly-quoted anchor, unreadable to the gate (G20). Against the round-29 staged row the same source produced `EXIT 7` with a 45-character CJK span priced `words=1` and refused as absent because the PDF text wraps it (`…即测\n试数据标签化管理…`). |
| S086 | 0 | `spans=2 located=2`, words `[1, 3]`; both locate **only** in the seat-built `Q2-11.unwrapped.txt` — against `Q2-11.raw.txt` the staged spans are `absent` (exit 7) |

So the gate, run on what the lane actually appended, is green on five of six rows and structurally refuses the
sixth. Its greens carry no length information for S084/S086 (1–7 tokens), and S083's green is about the lane's own
script. That is the honest reading of the receipt; a SCORECARD line that says "six rows validated" would overstate it.

## 4. Failure-capability of the new cases (on the committed body)

Mutants applied to `plans/sources_adopt.py` in `/tmp/r30-R30RevGate/mut.py`, then `--selftest`:

| mutant | result |
|---|---|
| `QUOTE_WORDS = 25` → `26` | `SELFTEST cases=14 failed=2` — `quote-overlong-refused`, `quote-boundary-25-accepted` |
| `normalize_text` → `return ""` | `SELFTEST cases=14 failed=2` — `quote-absent-refused`, `quote-located-accepted` (an empty needle would green every row) |
| `locates`: full containment → first-20-character prefix | `SELFTEST cases=14 failed=2` — `quote-absent-refused`, `quote-located-accepted` |
| `locates`: containment → `if True` (any quote locates) | `SELFTEST cases=14 failed=2` — same two |

The refusal and boundary cases are genuinely failure-capable. The committed body's two extra assertions inside
case 12 are load-bearing in a way the seat's `/tmp` artifact is not: the mutant *"a one-token quote locates
anything"* (`if len(needle.split()) <= 1: return loaded[0][0]`) **survives with `failed=0` on `f26ed9bb`** and is
**killed with `failed=1` (`quote-absent-refused`) on the committed `e9b6bc04`**. Score the committed byte. Full
mutant slate belongs to R30MutGate; this is the minimum needed to judge whether C3's new cases are decorative.
They are not.

## 5. Existing behaviour (e), measured on the committed body

Both bodies run in the same harness, same argv, temp `--out`; stdout/stderr compared as bytes.

| invocation | pre `6fe6e762` | committed `e9b6bc04` | identical |
|---|---|---|---|
| `--registry /tmp/r30-BuildAppend/pre-SOURCES.md --package …/SOURCES.append.r30.md` | `registry=82 staged=6 collisions=0 malformed=0 duplicates=0 defects=6 prose=6`, exit 4 | same line, exit 4 | stdout **yes** |
| scoped six-row admit (`--attest-opened --out`) | exit 0, block 6 rows | exit 0, block 6 rows, 6654 B, sha `2ec3a83b06c7ef2a…` | block **identical**; stdout/stderr identical after path normalisation |
| `--admit-ids S081,S777 --scope-to-admit` (missing id) | exit 5, stdout 93 B | exit 5, stdout 93 B | **yes** |
| `--selftest` | `cases=10 failed=0` | `cases=14 failed=0`; the ten original names/verdicts unchanged | names/verdicts **yes** |
| no arguments | exit 2, stderr 328 B | exit 2, stderr 398 B | exit yes; **stderr differs** by the two new option lines |

## 6. Verdict on C3

**C3's frozen predicate closes on the committed bytes. C3's stated surface does not.**

- Predicate: `python3 plans/sources_adopt.py --selftest` → `SELFTEST cases=14 failed=0`, exit 0, fourteen
  `CASE … PASS` lines. ✔ (run by me on `e9b6bc04`)
- The two required refusals are distinct, non-zero, and failure-capable: overlong → 6, absent-from-artifact → 7;
  four mutants kill their cases.
- Control: the freeze-baseline bytes (`git show HEAD:plans/sources_adopt.py`, `6fe6e762…`) with
  `--quote-file fx/rows_both.txt --artifact fx/art_both.txt` → **exit 2**, `unrecognized arguments: --quote-file …
  --artifact …`, matching `gate-before.txt` (`cases=10`, `quote_mode_exit=2`). The control cannot reach the target. ✔

**The gap, named.** The predicate is satisfied by a mode that (i) is not on the append path (G11) and is silently
cancelled by its own flags when combined with one (G10b); (ii) accepts any artifact the caller names — the row
file itself (G2), the registry (G3), a seat's scratch script (S083 `verify.py`), or a rewritten derivative
(S086 `Q2-11.unwrapped.txt`); (iii) prices CJK at one word and never reads the printed count, so three of the six
appended rows carry no length evidence (S084 `[3,7,1]`, S086 `[1,3]`, S085 unreadable — G5/G19/G20); and (iv) is
green on an empty or misspelt quote file (G8/G9) and on a fabricated id (G14). A receipt from this tool therefore
supports exactly one proposition — *"the bytes I was handed contain these strings"* — and nothing about the row's
cited URL. Round 29's routed sentence ("the gate still has no quote/word validation",
`corpus/lessons/round-29-verifier-spotcheck.md` §5 quality) is discharged **as a statement about the tool**
(exit codes 6/7 exist and fire), **not** as a statement about the admission decision. SCORECARD should say the
former; saying "the gate validates quotes" without "against a caller-supplied artifact, off the append path"
overstates the bytes.

Minimum changes that would let the sentence be written without the caveat, cheapest first:

1. Print artifact identity — `sha256` + byte count per loaded artifact — in the receipt, so a green can never be
   mistaken for a fetch (one `hashlib` call in `load_artifact`, one field in `print_quote_report`).
2. Refuse self-validation: fail when the artifact path is the quote file, is under `plans/`/`.ufo/`, or is a
   `.py`/scratch path beside a capture; or require the row's `source` cell to name the artifact/hash.
   G2/G2b/G3/G17 become refusals instead of greens.
3. Refuse a vacuous run: non-zero when `rows == 0` or `spans == 0`, and count an id that misses the row anchor as
   `malformed` (G8/G9/G14).
4. Widen the quote alphabet to `“”「」『』` **or** state that ASCII `"` is required — today a legitimate row is
   refused as `no-quote` (G20/S085).
5. State the counting rule where the rule lives (`corpus/SOURCES.md:7`, `corpus/QUALITY.md:32`) and print the CJK
   character count beside the token count; the lane already annotates rows this way, so the tool is the laggard.
6. Validate the cell's own `(N words)` annotation against the measured count (G19) — that is the D3 class.
7. Normalise wrap as well as line endings (collapse `\n` + leading whitespace to one space on the artifact side),
   or state that wrapped extractions cannot be validated and delete the unreachable wrap assertion from case 13.

## 7. Residual risk and verification gaps

- I executed only `sources_adopt.py` (subject + baseline). `adoption_check.py`, `round30_defects.py`, the census and
  the grader are outside this seat.
- No network fetch: §3's verdicts are against the seats' saved fetches under `/tmp/r30-R30SrcS08*`, not live URLs.
- The subject changed twice under me and the **committed byte is not the seat's artifact** (`e9b6bc04` vs
  `f26ed9bb`): the one-token-wildcard mutant survives `failed=0` on the seat's byte and dies on the committed one,
  so any receipt that cites the `/tmp` path as "the validated gate" is citing a weaker file than the one that ships.
- The live registry moved from 82 to 88 rows mid-review (S081–S086 appended), so G16 reads `88/77`; the same command
  on the 82-row snapshot read `82/76`. Both are the same finding.
- Untested by me: `--artifact` given a symlink, a FIFO, or a very large directory (`rglob` + full read, no size
  guard) — an operability note I did not measure; and the `--artifact`-as-relative-path behaviour from a different
  cwd.
