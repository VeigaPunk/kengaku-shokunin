# R38MapRetro — round-38 C2 V7's derived-label rule replayed on the round-37 requirement map

Seat: executor, round 38 wave 1. Target: the round-37 closure's routed item D2
(`corpus/lessons/round-37-verifier-spotcheck.md:5` item 2) — the admitted entry
`corpus/knowledge/tb2-git-webserver-grader.md` labels `instruction.md:9` **enforced** while
`CASE token-in-body … observed=pass` serves a body that is not `hello world`.

I wrote no lane file and edited nothing: everything below is under
`.ufo/waves/round-38/build/R38MapRetro/` or in scratch (`/fast/scratch/hyaku/kengaku-r38/R38MapRetro`,
removed). The entry is append-only lane text, so the corrected table is a **draft** here for the L1.

## Axes

| axis | what moves | how measured |
|---|---|---|
| fidelity | does the driver apply round-38 V7's rule, not round-37's | same label function, same citation clause; the two rules run side by side on the same map |
| honesty of the mapping | is every `case → instruction.md lines` justified from the case's own requirement text | 22/22 cases carry a justification; 5 malformed inputs refused |
| sensitivity | does a disagreement come from the evidence, not the code | 3 label mutants on the corrected map each flip exactly one row; the ablation shows what round 37 could not see |
| reusability | can the L1 or the round-38 C2 counter take this | one 244-line stdlib script, `--entry/--receipt/--violates/--map-file` args, exit code = predicate |

## The rule being replayed

Round-38 C2 V7 (`plans/round38_c2_verify.py:31-32`) derives each label from **every** receipt case
whose `violates=` set carries the line:

> `enforced` iff all of them are observed `fail`, `unenforced` iff all are observed `pass`, `partly` otherwise

plus one citation clause: the row must cite ≥1 case id in backticks and every cited id must be one of
those violating cases (`plans/round38_c2_verify.py:213-256`). Round 37's own V7
(`plans/round37_c2_verify.py:167-205`) checked only that an `enforced` row cites *some* observed-`fail`
case, an `unenforced` row some observed-`pass` case, a `partly` row one of each — a label chosen from one
convenient witness passes it.

Two differences force a driver rather than a re-use:

1. the round-37 receipt has **no** `violates=` tag — each `CASE` line carries `-- <requirement>` prose
   (`corpus/evidence/round37/git-webserver-probe.txt`, e.g. `CASE token-in-body tools=curl predicted=pass
   observed=pass match=yes -- test_outputs.py:13 — the verdict is a substring …`), so the violates-set has
   to be derived and recorded outside the frozen receipt;
2. the round-37 map labels whole **ranges** (`instruction.md:1-6`), not single tag lines
   (`corpus/knowledge/tb2-git-webserver-grader.md:103-108`), so a row's label is derived over the union of
   cases violating any line in the range.

Deliverables: `map_label_retro.py` (driver), `violates-r37.tsv` (22 rows: case, lines, justification),
`map-corrected.md` (the corrected `## Requirement map` table, draft), six run receipts + self-tests.

## The violates mapping (`violates-r37.tsv`)

Scope rule, stated in the file header: a case's violates-set holds the instruction lines whose requirement
the case's constructed state does not meet; lines the case neither exercises nor contradicts stay out.
Every justification is grounded in the case's own `-- requirement` text and the instruction line's words
(`corpus/evidence/round37/tb2-git-webserver/instruction.md` lines 1-9; state table in
`corpus/evidence/round37/git-webserver-dry-cases-freeze.txt:1-22`).

| case | observed | lines | justification (from the case's requirement text) |
|---|---|---|---|
| `no-server` | fail | 7,8,9 | "nothing listens on :8080" → no webserver on 8080 (7), the 8 request unanswered, no output (9) |
| `static-file-no-git` | pass | 1-6,7 | requirement names `instruction.md:1-6`; "no repository, hook or push" also fails 7's push clause |
| `exact-no-newline` | pass | — | control: exactly `hello world` at the required path |
| `trailing-newlines` | pass | 9 | body is `hello world\n\n\n`, not the line's output; passes only because `:60` strips newlines |
| `capitalised` | fail | 9 | body `Hello World` |
| `leading-space` | fail | 9 | body ` hello world`; leading whitespace survives |
| `trailing-space` | fail | 9 | body `hello world ` |
| `crlf` | fail | 9 | body carries CR |
| `bom` | fail | 9 | body carries a BOM |
| `empty-200` | fail | 9 | empty body |
| `not-found` | fail | 8,9 | 404 on `/hello.html`: the 8 request is answered 404, no body seen |
| `http-500-right-body` | fail | 8,9 | the 8 request returns 500; the right body is never fetched |
| `redirect-301` | fail | 8,9 | `curl` without `-L` sees 301 |
| `catch-all-200` | pass | — | serves `hello world` at the required path; routing beyond it is **not** a clause of 8 |
| `wrong-port-8081` | fail | 7,8,9 | requirement names `instruction.md:7`; on 8081, nothing on `:8080` |
| `token-in-body` | **pass** | 9 | body `TEST PASSED`, not `hello world`; pass via the verdict-token substring |
| `status-then-content-split` | **pass** | 8,9 | first answer to the 8 request is `not the content`; only the second is right |
| `first-request-404` | fail | 8,9 | first answer to the 8 request is 404 |
| `slow-server-3s` | pass | — | control: right body on 8080 in 3 s; no mapped line bounds latency |
| `wget-static-file` | pass | 1-6,7 | same static-file state on the wget branch |
| `wget-404` | fail | 8,9 | `wget` exits nonzero on 404 |
| `wget-token-in-body` | **pass** | 9 | body `TEST PASSED` on the wget branch |

Three calls are judgments, disclosed: `trailing-newlines` is tagged 9 (extra blank lines are not the line's
output) though the entry treats it as a pass control — it changes no row's derived label; `no-server` and
`wrong-port-8081` are tagged 7 **and** 8/9 rather than 7 only (with nothing answering, both later lines
fail); `catch-all-200` is tagged with the empty set, following `F37CritC2Map` §"`instruction.md:8`", which
shows the catch-all *satisfies* line 8 as written.

## Result — the entry's map, labelled vs derived

`python3 retro/map_label_retro.py` (cwd = clean `--shared` clone of tip `2c5f4e0b`, receipt
`run-entry.txt`, exit 1):

| row | labelled | derived | agree | cited cases | why |
|---|---|---|---|---|---|
| `instruction.md:1-6` | unenforced | unenforced | yes | `static-file-no-git` | 2/2 violators pass |
| `instruction.md:7` | partly | partly | yes | `wrong-port-8081`, `static-file-no-git` | 4 violators: 2 fail, 2 pass |
| `instruction.md:8` | partly | partly | **NO** | `not-found`, `catch-all-200` | `catch-all-200` **is not a violator** of line 8 → citation clause fails |
| `instruction.md:9` | enforced | **partly** | **NO** | `capitalised`, `leading-space` | 17 violators: 13 fail, **4 pass** (`token-in-body`, `wget-token-in-body`, `status-then-content-split`, `trailing-newlines`) |

```
ROW instruction.md:8 labelled=partly derived=partly agree=NO
  violators=8 first-request-404=fail http-500-right-body=fail no-server=fail not-found=fail redirect-301=fail status-then-content-split=pass wget-404=fail wrong-port-8081=fail
  violating-but-passing=['status-then-content-split']
  cited=not-found=ok catch-all-200=NOT-A-VIOLATOR
ROW instruction.md:9 labelled=enforced derived=partly agree=NO
  violating-but-passing=['status-then-content-split', 'token-in-body', 'trailing-newlines', 'wget-token-in-body']
  cited=capitalised=ok leading-space=ok
rows=4 disagree=2 problems=0
MAP-RETRO disagree=2 rule=violating fail
```

So the closure's D2 reproduces mechanically on the frozen receipt: **2/4 rows disagree**, matching
`F37CritC2Map`'s `VERDICT: req-map-2/4` — row 9 on the label (the defect D2 names) and row 8 on the
citation (the catch-all was cited for a requirement the instruction does not make). Row 7's label survives,
confirming that D2's third item is prose-only ("the port half is enforced",
`corpus/knowledge/tb2-git-webserver-grader.md:116`) and cannot be machine-checked from the table.

## The corrected map passes

`python3 retro/map_label_retro.py --map-file retro/map-corrected.md` (`run-corrected.txt`, exit 0):

| row | label | cited cases | derived | agree |
|---|---|---|---|---|
| `instruction.md:1-6` | unenforced | `static-file-no-git` | unenforced | yes |
| `instruction.md:7` | partly | `wrong-port-8081`, `static-file-no-git` | partly | yes |
| `instruction.md:8` | partly | `not-found`, `status-then-content-split` | partly | yes |
| `instruction.md:9` | partly | `capitalised`, `leading-space`, `token-in-body` | partly | yes |

```
rows=4 disagree=0 problems=0
MAP-RETRO disagree=0 rule=violating pass
```

The corrected table is exactly the three edits `F37CritC2Map` prescribes (row 8 citation → the real
violating pass; row 9 `enforced` → `partly` with `token-in-body` added; rows 1-6/7 untouched), so the rule
and the critic agree on the fix, not just on the defect.

## Calibration — the rule sees what round 37 could not, and only what the evidence supports

| control | command | result |
|---|---|---|
| round-37 V7 replayed on the **defective** map | `--rule cited` | `disagree=0 pass` (**the blind spot**: derive from cited witnesses only, `cited-verdicts=capitalised=fail leading-space=fail` → `enforced`, "agrees") |
| row 9 label mutant (`partly` → `enforced`) on the corrected map | `--map-file mutant-row9-enforced.md` | `ROW instruction.md:9 … agree=NO`, `disagree=1` |
| row 8 mutant (`partly` → `unenforced`, cite only the split case) | `--map-file mutant-row8-unenforced.md` | `ROW instruction.md:8 labelled=unenforced derived=partly agree=NO`, `disagree=1` |
| row 7 mutant (`partly` → `enforced`) | `--map-file mutant-row7-enforced.md` | `disagree=1` |
| missing case in the violates table | `--violates st-missing-case.tsv` | exit 1, `PROBLEM receipt cases missing from the violates table: ['wget-token-in-body']` |
| invented case | `--violates st-unknown-case.tsv` | exit 1, `PROBLEM violates table names cases not in the receipt: ['ghost-case']` |
| reversed/3-part range (`8-9-1`) | `--violates st-bad-lines.tsv` | exit 1, `PROBLEM st-bad-lines.tsv:19: bad line item '8-9-1'` |
| empty justification | `--violates st-empty-justification.tsv` | exit 1, `PROBLEM …:18: empty-200 carries no justification` |
| unparsable label (`mostly`) | `--map-file st-bad-label.md` | exit 1, `PROBLEM unparsed row '| `instruction.md:9` | mostly …'` |

A label is never accepted because *some* cited case supports it; it is accepted only if it equals the
derivation over all violating cases and every citation is a violator. That is the hole D2 asks to close,
and it is the difference between the `rule=cited` row and the `rule=violating` row above.

## Evidence index

| # | command | output |
|---|---|---|
| 1 | `git -C "$S/lane" rev-parse --show-toplevel` / `HEAD` | `…/R38MapRetro/lane` / `2c5f4e0ba8e2865af4b71e337f3cde86eaf0702e` |
| 2 | `python3 retro/map_label_retro.py` (cwd clone) | `rows=4 disagree=2 problems=0` / `MAP-RETRO disagree=2 rule=violating fail`, exit 1 — `run-entry.txt` |
| 3 | same, cwd the lane (read-only, defaults) | byte-equal to #2 apart from the script dir path — `run-entry-from-lane.txt` |
| 4 | `python3 retro/map_label_retro.py --map-file retro/map-corrected.md` | `disagree=0 … pass`, exit 0 — `run-corrected.txt` |
| 5 | `python3 retro/map_label_retro.py --rule cited` | `disagree=0 … pass`, exit 0 on the **defective** map — `run-ablation-cited-rule.txt` |
| 6 | three label mutants on the corrected map | `disagree=1` each — `run-mutant-row{7,8,9}-*.txt` |
| 7 | four violates-table self-tests + one label self-test | five `PROBLEM` refusals, exit 1 — `run-selftests.txt` |
| 8 | receipt summary read by the driver | `# receipt cases=22 observed_pass=9 observed_fail=13 mismatches=0` |
| 9 | `# instruction lines=10 violates-table lines=[1,…,9] unmapped=[10]` | line 10 is the instruction's own out-of-scope line, correctly unmapped |

Artefacts: `map_label_retro.py`, `violates-r37.tsv`, `map-corrected.md`,
`run-entry.txt`, `run-entry-from-lane.txt`, `run-corrected.txt`, `run-ablation-cited-rule.txt`,
`run-mutant-row7-enforced.txt`, `run-mutant-row8-unenforced.txt`, `run-mutant-row9-enforced.txt`,
`run-selftests.txt`.

## For the L1 (not applied — append-only entry)

1. Append the erratum row set from `map-corrected.md` to
   `corpus/knowledge/tb2-git-webserver-grader.md` (or replace the four table rows and keep the old text
   quoted as the superseded reading), and add the row-7 qualifier `F37CritC2Map` drafted.
2. Reusable in round 38's C2 counter: `receipt_cases()` in `plans/round38_c2_verify.py:186-192` already
   returns the tag sets; the standalone driver here is the same derivation over a legacy map, so the
   counter needs no change — the round-37 entry only needs the erratum.
3. The lesson candidate for `QUALITY.md`: *a map label is derived from every case that violates the line,
   never from the cases a row chooses to cite; a citation must be a violator.*

## Limits and risks

- The mapping is **this seat's reading**, not a frozen artefact: the frozen receipt carries no
  `violates=` tag. Every row is justified, and the two rows that decide the verdict (9's `token-in-body`,
  8's `status-then-content-split`) rest on the entry's own text plus `F37CritC2Map`, not on judgment:
  `token-in-body` serves `TEST PASSED` and is observed pass; the split's first answer is `not the content`.
  If the L1 rejects `trailing-newlines` as a line-9 violator the row-9 label is still `partly`
  (`token-in-body`, `wget-token-in-body`, `status-then-content-split` remain).
- The driver checks the receipt summary against its `CASE` lines (so a truncated receipt is a `PROBLEM`,
  not a silent pass) but does not re-run the probe; the probe and dry table are frozen and round-37's V5
  already pins them.
- Nothing here is a verdict on the entry's admission; it reproduces one routed defect and its fix.
- No lane file, `corpus/`, `plans/`, index or jj state was written; no git command ran in the lane except
  `rev-parse`/`status`; tools installed: none (stdlib Python 3 only); scratch removed.

VERDICT: map-retro-disagree-2-rows
