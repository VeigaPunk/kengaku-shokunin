# R30SimplGate — YAGNI review of the C3 quote gate

Seat: `R30SimplGate` (simplifier, axis operability). Claim reviewed: **C3** of
`plans/round-30-claims.md`. Date 2026-10-25.

**Artifact reviewed:** `plans/sources_adopt.py` as integrated in the lane,
`sha256=47e60021966318c9f36d4cab8e1464a8cd333db114eca3c1689d206cdfef7922`, 815 lines.
All line numbers below are that file, verified line by line against it. The lane file
moved twice while this seat ran: `e9b6bc04` (811 lines) is the executor snapshot plus
20 mutation-survivor assertion lines, and `47e60021` adds a 6-line mode-exclusivity
guard at `766–769` — after every line I cite. Production bytes up to line 750 are
identical to `/tmp/r30-GateQuote/sources_adopt.py`
(`sha256=f26ed9bb94086e9e9a7c3d7812608870e3fd1de441d5fe10fcff380f7b14609d`, 791
lines). Pre-change comparison target:
`sha256=6fe6e762ab0c61da4ddbf029a2aa1a38cb64732ebd1ccbee4773c5eadcf7ead2`, 478
lines, `git show 30ee3b5:plans/sources_adopt.py`.

Snapshot warning for Main: the scratch path was rewritten four times while this seat
ran (`6fe6e762` → `7e81511c` → `93ee7f7c` → `f26ed9bb`), and at 04:22 it held bytes
*identical* to the pre-change tool. The lane copy moved twice more (`e9b6bc04` →
`47e60021`). A seat that reads either path early reviews a different file; this
review is keyed by hash, and every number below was re-checked against `47e60021`.

## 1. Verdict

The extension is **needed in its two refusal classes and its four cases, and carries
about half again as much speculation as it needs**. Added surface: 341 lines — 199 in
the quote section, 16 in the CLI (including the 6-line mode-exclusivity guard the
regression seat added), 126 in the selftest. Lines this review deletes: **86
production and 29 selftest = 115 removed, 55 added back** where the reduction needs a
different shape. Net: file 815 → 755 (−60), the production region 447 → 394 (−53, a
27% cut of the added production surface), and the suite still prints
`SELFTEST cases=14 failed=0`.

The pre-change CLI surface **is preserved**: five functional invocations on real lane
bytes are byte-identical in stdout, stderr and exit code; exit codes 0/3/4/5 and the
first ten selftest case names are unchanged; no previously unique long-option
abbreviation becomes ambiguous.

## 2. What C3 actually asks for (the litmus)

Frozen predicate, decomposed into the only things it can observe:

| # | Predicate clause | What must exist |
|---|---|---|
| P1 | `--selftest` prints `SELFTEST cases=14 failed=0`, exit 0 | four new cases, old ten keep name and verdict |
| P2 | a 26-word quote is refused | word cap at exactly 25, inclusive at 25 |
| P3 | a quote absent from the supplied artifact bytes is refused | byte-substring test against artifact bytes |
| P4 | distinct non-zero exit codes | two codes, one per refusal class |
| P5 | pre-change bytes reject `--quote-file/--artifact` with argparse exit 2 | the new tool must *accept* those two flags, else the control and the target are the same |

Everything in the extension that no clause above can see is speculation. Note the
sharp edge: the counting command is `--selftest` **alone**. Nothing in the round's
receipts runs `--quote-file/--artifact` on the *new* tool — the control runs the old
one. So the mode's CLI path has zero positive coverage and must stay thin (P5 is its
only justification).

## 3. Keep list — every line tied to a clause

| Keep | Lines (`47e60021`) | Clause | Why it cannot go |
|---|---|---|---|
| `EXIT_QUOTE_TOO_LONG = 6`, `EXIT_QUOTE_ABSENT = 7` | 49–50 | P4 | the two separable refusal classes |
| `QUOTE_WORDS = 25`, `words()` | 265, 272–273 | P2 | the cap and the counter; `words` is byte-for-byte the same rule as `plans/round30_defects.py:38-39` (`return len(text.split())`) — verified, so the claim's comment is true |
| `ANCHOR_COLUMN`, `QUOTE_SPAN_RE`, `quoted_spans` | 268–269, 281–293 | P2–P4 | "its anchor cell's quoted text"; the `no-quote` / `unbalanced-quote` reasons reuse the existing structural code 4, so they cost one branch, not a new class |
| `normalize_text`, `locates` (single-file form) | 276–278, 328–337 | P3 | "byte substring of the supplied artifact", UTF-8, newline-normalised per the seat spec; case 13 proves CRLF identity |
| `quote_check` body: cap first, then substring, exit 4 → 6 → 7 | 340–421 | P2–P4 | the mode itself |
| `--quote-file`, `--artifact` (both required together), dispatch after `--selftest`, `return code` | 741–750, 763–772 | P5 | without the flags the control's own invocation exits 2 on both tools |
| `print_quote_report`, reduced to summary + refusal lines | 426–445 | operability | an operator must see which span and how many words; the summary already carries `located=` |
| cases 11–14 (`quote-overlong-refused`, `quote-absent-refused`, `quote-located-accepted`, `quote-boundary-25-accepted`) | 600–716 | P1 | 10 → 14; names match the four mandated subjects |
| `quote_row` helper | 474–476 | P1 | 3-line fixture used by four cases, not a code path |

## 4. Delete list — unexercised additions, with the line that goes

Each item names the lines in `47e60021` and why no counting command can see it.
Every production line number below is unchanged from the executor snapshot
`f26ed9bb`; only selftest line numbers from 615 on are shifted +20 by integration,
and the mode-exclusivity guard sits after all of them at `766–769`.

### D1 — the unreadable-artifact "problem" channel (21 production lines)
Goes: `45` (`EXIT_QUOTE_UNREADABLE = 2`), `311` (`--artifact names no file or
directory`), `313` (`skipped: list[str]`), `316–320` (skip-on-OSError/UnicodeDecodeError),
`322–324` (`if not loaded: detail = …`), `351` (`loaded, problem = …`), `361–366`
(`artifacts`/`problem` keys and `if problem: return`), `427–429` (problem branch in
`print_quote_report`).

Unexercised: `grep -n EXIT_QUOTE_UNREADABLE` returns exactly two sites — the
definition and the return that uses it. No selftest case builds an absent,
non-UTF-8, or non-file artifact, and the count is frozen at 14, so none can be added.
Keep the exit-2 class, not the channel: a 3-line guard at the dispatch site
`except (OSError, UnicodeDecodeError) as exc: parser.error(...)`. That is argparse's
own caller-error path (the same class the deleted constant's comment claimed), so it
is the existing convention rather than a second one.

### D2 — directory artifacts (25 production lines, 5 selftest fixture lines)
Goes: `304–311` (`if path.is_file(): … elif path.is_dir(): … rglob … else`), `312–315`
(`loaded` list and the `item.parent == root` name computation), `328–337`
(`locates` returning a name over a list), `361` (`"artifacts"`), `431` and `441`
(`found=`/`artifacts=` in the summary), `649` (`qreport["artifacts"] ==
["capture.txt", "notes.md"]`), and the fixture at `621–624` plus the five
`quote_check(…, art_dir)` calls at `626`, `632`, `637`, `640`, `642`.

Unexercised by the claim: the counting command never passes `--artifact` at all. The
only exercise is case 12's directory fixture, whose frozen subject is *"a ≤25-word
quote absent from the artifact refused"*, plus the two mutation-survivor probes
folded into the same case. The directory is an extra axis inside a case the spec
mandated for another reason; re-pointing those five calls at single files costs four
lines and loses nothing. Six sources is six invocations, or one shell loop. The two
survivor assertions survive the cut verbatim (they compare against one file), and
they still kill mutants m2 and m4 in §6.

### D3 — the `cap` parameter and its echoed copy (5 lines, one of them partial)
Goes: `340` (`cap: int = QUOTE_WORDS` in the signature), `353` (`"cap": cap`),
`395` (`cap={cap}` in the detail), `440` (`cap=report["cap"]`), `715`
(`qreport["cap"] == 25`), and the `cap` wording at `343`/`348`.

No caller passes a non-default cap; case 14 asserts a copy of a module constant back
to itself. The cap is frozen at 25 by P2. Print `QUOTE_WORDS` directly.

### D4 — the `found` list (18 production lines, 5 selftest assertions)
Goes: `357`, `369`, `384–389` (the three-line rationale and `if where:
found.append(...)`), the `at {where or "nowhere"}` arm at `396`, `410`, `431`/`436`,
and the five assertions at `614` (case 11), `664–665` (case 12), `694–695` (case 13),
`713` (case 14).

Unexercised *need*: P4 requires two refusals separable by exit code and nothing more;
locatedness-of-an-overlong-span is a third fact that no counting command prints. The
one assertion that wanted it (case 11: "the refusal is the length, not absence") is
kept by asking the helper directly — `and locates(over, load_artifact(art))` — which
is what the reduced patch does. This is the one deletion that removes a *true* fact,
so the tradeoff is stated: the operator loses "was the overlong quote also present?"
in the summary line; the two entries in `refused` still name the span and its count.

### D5 — accepted-span receipt lines and the `(label, detail)` tuple (16 lines)
Goes: `363` (`"quotes": []`), `373` (`details: list[tuple[str, str]]`), `379`,
`392–398`, `400–401`, `404`, `414`, `444–445`.

No case asserts `report["quotes"]`. The file's own receipt convention (`print_report`
in the pre-change `plans/sources_adopt.py:228-251`) prints the summary line and
*failures only*; echoing each accepted span is a second convention. The reduced report
keeps `located=N` in the summary and prints refusals from one `refused: list[str]`.

### D6 — nothing else
Docstring capability 5 (`17–20`) and the `Scope:` sentence reword (`21–23`) match
what the tool now does and follow the existing per-capability convention: keep.
Nothing in the used-by/recheck/collision code was touched: `diff` shows the only
non-additive change in that region is the `4. refusal …` sentence's trailing `;`.

**Reconciliation.** The per-item targets sum to 21+25+5+18+16 = **85 production
lines**, plus one docstring line inside D3 — the applied reduction
(`diff -u lane2.py minlane2.py`) removes **86 production and 29 selftest lines and adds
back 55**, which lands the file at 755 and the production region at 394. All five
items were applied together in `minlane2.py` (§6) and the suite re-run green; I did
not bisect them item by item.

## 5. Is the pre-change CLI surface preserved?

**Yes.** Evidence, run from `/tmp/r30-R30SimplGate/A` (pre-change,
`6fe6e762`) and `…/F` (the lane file `47e60021`, copied byte-for-byte), same basename
so `prog` matches in both, on live lane bytes
(`corpus/SOURCES.md`, `/home/vgpnk/Projects/shokuknow/merge/kengaku/SOURCES.append.md`,
`plans/round-30-claims.md`):

| Invocation | pre exit | new exit | stdout | stderr |
|---|---|---|---|---|
| `--registry … --package SOURCES.append.md` | 3 | 3 | identical | identical |
| `… --scope-to-admit --admit-ids S081 --access-date 2026-10-25 --entries …` | 3 | 3 | identical | identical |
| `--registry … --package round-30-claims.md` | 0 | 0 | identical | identical |
| `… --admit-ids S081,S999 …` | 3 | 3 | identical | identical |
| `… --admit-ids S081` (no date) | 3 | 3 | identical | identical |

(Exit values moved from 5 to 3 between my two runs because C1 seats are appending rows
to `corpus/SOURCES.md` concurrently — both tools report the same number each time.)

A fixture pair (`HEADER` + one staged row) covers the codes the live tree did not
reach: escaped-pipe package → **4** on both; `--admit-ids S902` with no such row →
**5** on both; a clean append block → **0** on both, with identical stdout and stderr.
So every pre-existing exit code (0, 3, 4, 5) is behaviour-identical, not merely
unchanged in the source.

Selftest: pre `SELFTEST cases=10 failed=0`, new `cases=14 failed=0`; the first ten
case names are identical and in the same order. Control: pre-change bytes with
`--quote-file /tmp/x --artifact /tmp/y` → `error: unrecognized arguments`, exit 2.

Abbreviation regime (`argparse._get_option_tuples`, then confirmed by running):

| Prefix | pre | new |
|---|---|---|
| `--a` | ambiguous (admit-ids, access-date, attest-opened), exit 2 | ambiguous, same exit 2, candidate list gains `--artifact` |
| `--ar`, `--q` | unrecognized, exit 2 | resolve to the new flags |
| `--se` | → `--selftest`, exit 0 | → `--selftest`, exit 0 |
| `--sc`, `--at` | exit 2 (missing registry), same message | identical |
| `--re` | ambiguous (registry, recheck), exit 2 | identical |

Only two additions to the surface: two option names, and their two lines in `--help`.
`--a`'s error text changes; its exit code does not. No unique→ambiguous regression is
possible or present, because `--artifact` and `--quote-file` share a prefix only with
`--admit-ids`/`--access-date`/`--attest-opened`, which were already mutually ambiguous.

## 6. Proof that the delete list keeps the predicate green

I applied exactly D1–D5 to the integrated file on a scratch copy,
`/tmp/r30-R30SimplGate/minlane2.py` (815 → 755 lines; nothing in the lane was edited
to produce it):

- `python3 minlane2.py --selftest` → the ten old cases unchanged, then `CASE
  quote-overlong-refused PASS`, `CASE quote-absent-refused PASS`, `CASE
  quote-located-accepted PASS`, `CASE quote-boundary-25-accepted PASS`,
  `SELFTEST cases=14 failed=0`, exit 0. Production region 447 → 394 lines; the
  mode-exclusivity guard is preserved by the reduction (it is not on the delete list).
- The same five invocations as §5, run from `…/G` (reduced) against `…/A`
  (pre-change) → identical stdout, stderr and exit on every one.
- End-to-end on real registry bytes (row `S091`, the 18-word Abstract quote):
  artifact containing the quote → exit 0, `QUOTE rows=1 spans=1 located=1 overlong=0
  absent=0 malformed=0 cap=25`; paraphrase artifact (`guidelines`→`rules`) → exit **7**
  with `REFUSED S091 absent words=18`; 26-word artifact and row → exit **6** with
  `REFUSED S091 overlong words=26`. Both refusal classes are reachable through the
  CLI that P5 needs.
- Failure capability retained after the cut — four mutants on `minlane2.py` copies,
  each with the case that should kill it:
  | mutant | expected killer | tally |
  |---|---|---|
  | cap widened to 30 (`count > QUOTE_WORDS + 5`) | case 11 | `failed=1 quote-overlong-refused` |
  | substring → 10-character prefix match | cases 12 (S023) and 13 (paraphrase) | `failed=2 quote-absent-refused quote-located-accepted` |
  | absent branch returns 6 | cases 12 and 13 | `failed=2 quote-absent-refused quote-located-accepted` |
  | one-token quote wildcarded into a match (`len(quote.split()) < 2 or …`) | case 12 (S022) | `failed=1 quote-absent-refused` |

  All four exit 1. The last two rows show the mutation-tester's survivors are not
  lost when the directory fixture is removed — they are simply no longer pointed at a
  directory.

## 7. Kept on purpose, with the tradeoff named

1. **`unbalanced-quote` (`288–292`)** — no clause needs it, but it shares the
   `quoted_spans` reason channel that `no-quote` already requires, so it is two lines
   and one fixture line. If the operator wants the floor, delete it together with the
   `S021` half of case 12.
2. **`no-quote` → exit 4** — this is the difference between "validates quotes" and
   "validates the quotes it happens to find". A row with no quote passing the quote
   gate would be a laundering path; it reuses an existing code rather than inventing
   a fourth.
3. **`normalize_text`** — mandated by the seat spec and exercised by case 13; the
   `locates` docstring's "multi-line quote" phrasing is accurate (the artifact's line
   endings are normalised, the quote is not wrapped) and should survive RevGate
   question (b) unedited.
4. **The mode-exclusivity guard (`766–769`, 4 code lines + 2 comment lines)** — an
   integration-seat addition that landed after my first pass. It is not
   predicate-required and no case exercises it (the count is frozen at 14 and none of
   the four mandated subjects is mode mixing), so by my own standard it is
   speculation. It stays because it closes a real laundering path: before it,
   `--registry … --package … --quote-file … --artifact …` silently skipped the schema
   gate and could exit 0 (verified on `e9b6bc04`). It preserves the surface — all five
   pre-existing invocations are still byte-identical, and the mixed invocation now
   prints `error: --quote-file/--artifact cannot be combined with --registry/--package`,
   exit 2. Cheaper than the alternative (composing the two modes), and it is the only
   added refusal a caller can reach by accident.

## 8. Residual risks this review did not fix (no code added)

- ~~Silent mode precedence~~ — **closed** by the guard at `766–769` (see §7.4). A
  caller can no longer ask for both modes and get one silently.
- **Whole-CLI blind spot.** The mode's dispatch and formatter are exercised by no
  receipt in the round (counting command `--selftest`, control = old tool). Keeping
  them at 15 lines as shipped is the mitigation: do not add `--json`, `--cap`,
  `--artifact-url`, `--strict/--no-quote-check`, HTML stripping or entity decoding —
  none is exercised, and a `--no-quote-check` shape would let a caller disable the
  very check C3 moves.
- **Artifact↔URL binding** is unpoliceable here by construction (the caller supplies
  the bytes). C3 must not be read as claiming provenance; that belongs to the C1
  kill rule.
- **Word counting and CJK**: `len(text.split())` counts an unspaced CJK run as one
  word. State that in the docstring clause next to `QUOTE_WORDS` — documentation, no
  code; do not add a segmenter (unexercised).

## 9. Tooling

No installs, no upgrades: the review used `python3` (3.14.0, system), `diff`, `cmp`,
`sha256sum`. No pacman transactions were attempted (host pause respected). No writes
outside `/tmp/r30-R30SimplGate/` and this file.
