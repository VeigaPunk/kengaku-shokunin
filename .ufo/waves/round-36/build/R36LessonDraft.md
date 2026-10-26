# R36LessonDraft — report (scribe, wave 1)

## Behavior

Drafted the round-36 lane lesson at
`.ufo/waves/round-36/build/R36LessonDraft/round-36.md` (14,620 bytes,
sha256 `43e87794e5bbc2972f3928d2c80f05ce76dd0501a71ea8819c2e694df841e774`). It is a draft for the L1;
no lane file was edited, staged, committed or checked out, and no jj command was run.

Sections delivered in the requested order:

1. **Header** — baseline `b662a5d6dd370491049e4206818373c61be44816`, freeze
   `3241b86cde0e9a3b9363a0d4c7fff12ec5d5f5e2`, Amendment 1
   `acbda2f3936838ba4849f14937fbecb8aed461e5`; controls red before any gate write, probe run or repair.
   Commit identities checked with `git cat-file -t <sha>` → `commit` for both, and `git log --oneline -3`
   → `f9efce3` (wave-1 spec), `acbda2f` (amendment 1), `3241b86` (freeze).
2. **`## Gate`** — 10 table rows: the C2 entry as **Admit-candidate** (freeze state `checks=6 defects=4`);
   S108/S109/S110 as **Admit-candidate (mined)** with pinned URL, access date 2026-10-25 and a located
   verbatim quote (5, 4 and 19 words — all ≤25); the `considerthese/2026-10-25.md` proposal 2(c)
   assimilation row mined as a lesson/QUALITY criterion with file and date; five merge/kengaku rows —
   one admit-direction row left `<scout verdict: R36ScoutMergePkg>` (`grader-fixture-probe-stage3.md`,
   row-level S171 only) and three **Refused** plus one **Held**.
3. **`Erratum (round 36):`** — exactly one line, inside `## Gate`, carrying `S130`, the recount
   `13 + 23 + 1 = 37` and `denominator 38`. `build/R36ToolathlonRecount.md` did not exist at drafting
   time (`ls` → "No such file or directory"), so the line was written to the exact requested form.
4. **`## Mistakes`** — 4-column markdown table (`class | evidence pointer | captured-by | fix`) with the
   four required rows: _vacuous_ (round-35 frozen counters accepted junk; `round-35-verifier-spotcheck.md:86`,
   `plans/round35_hardening.py:10-15`, red-before `claims/control-c1-legacy.txt` `LEGACY accepted=7/7`,
   captured-by none), _reference-drift_ (`regex-log-probe-first-run.txt:21-22`, Amendment 1, captured-by
   none), _working-tree / token-cooccurrence_ (round-34 D1, ledger `R35-D2`), _scope_ (ledger split per
   opened round — `corpus/defects.jsonl` 5 `R34-D*` rows beside `corpus/defects-round35.jsonl`
   4 `R35-D*` rows, and `plans/defect_ledger.py` requires `closed == len(rows)`).
5. **Disposition table** for the six §5 routed items of `round-35-verifier-spotcheck.md`: items 1-4
   marked closing/closed with the measurement that will decide them, item 5 (S091 live leg) carried,
   item 6 (SHONEN) carried and operator-owned.
6. **`## Census`** — before from `claims/census-before.txt` (15 W04, `kengaku ok`, exit 0, the 15 rows
   listed); after marked `<TBD at landing>`; draft-time counts recorded (registry 100, knowledge files 42,
   README index rows 42, so landing both C2 surfaces gives index parity 43/43).
7. **`## Spot-check`** — `<TBD at landing>` placeholder listing the six checks the non-author closure
   must run.

No result that wave 1 has not measured is asserted: every landing-time number is `<TBD at landing>`,
including the C1 `FIXTURES …` line, the C2 `checks=6 defects=0` line and the nested-path count `21 → 0`.

## Gates

- **C1 / `r35_d4` (the erratum check) — simulated green on the draft.** The check in
  `plans/round36_c1_verify.py` (`r35_d4`) was replayed against the draft file with its own expressions:

  ```
  python3 - <<'EOF'   # replayed r35_d4: parts from toolathlon-package.md, Gate-section scan of the draft
  ...
  EOF
  → gate_section_found True
  → errs 1
  → r35_d4 would return: True (recount=13 + 23 + 1 = 37, stated=38)
  ```

  The recount is taken from the committed copy, not from the merge package:
  `| isolated and callable | 13 | 38 |`, `| isolated but not callable … | 23 | 38 |`,
  `| exec failed in isolation | 1 | 38 |`, `| Outcome | Count | of 38 |` in
  `corpus/evidence/round36/toolathlon-package.md`; 13 + 23 + 1 = 37 ≠ 38. The four callable sub-rows
  (4 + 9) are nested under the 13 and are not counted twice.
- **C2 W2/W3/W5 are untouched by this draft** — the entry, the three registry rows and the README row are
  other seats' artefacts; this lesson does not write into `corpus/`.
- **Table well-formedness** — every table row parses with a consistent cell count
  (`bad_pipe_rows []`); no cell carries an unescaped `|`. The Gate table has 10 candidate rows; the
  Mistakes table has 4 columns; the disposition table has 3.
- **Quotes verified verbatim against the cited lines** (not from memory):

  ```
  test_outputs.py 87 True   "matches = re.findall(pattern_text, log_text, re.MULTILINE)"
  test.sh 26 True           "echo 1 > /logs/verifier/reward.txt"
  instruction.md 2 True     "If multiple dates are present in a line, the regex should match only the last date in that line." (19 words)
  ```

  Capture digests from `sha256(capture)` → `345c3bd0…8f72`, `4770437e…c334`, `4f7ac05e…f9c`, matching
  `corpus/evidence/round36/tb2-regex-log/SHA256SUMS` and the frozen `FILES` table in
  `plans/round36_c2_verify.py`. The considerthese 2(c) quote is verbatim only with the line break and
  indentation normalised (`considerthese/2026-10-25.md:44-45`), and the row says so.

## Touched surfaces

- Written: `.ufo/waves/round-36/build/R36LessonDraft/round-36.md` (draft) and this report at
  `.ufo/waves/round-36/build/R36LessonDraft.md`.
- Directory created: `.ufo/waves/round-36/build/R36LessonDraft/`.
- Nothing else: no `corpus/`, `plans/`, `SCORECARD.md`, `LOG.md`, `README.md`, `SKILL.md`, `PROVINCE.md`,
  `SHONEN.md`; no git index or jj state; no `/tmp` clone was needed (all reads were in-lane and
  read-only). No tool was installed or upgraded, so the tooling record is empty.

## Out of scope (not done by this seat)

- Not landed: the file is a draft; `corpus/lessons/round-36.md` does not exist yet
  (`ls` → "No such file or directory"), so `r35_d4` still reads `round-36 lesson absent` at the tip.
- Not verified: any C1 or C2 counter run, the nested-path count going to 0, the census after, the
  non-author spot-check. This seat ran no counter and no probe.
- Not decided: the final verdict for `grader-fixture-probe-stage3.md` (left as
  `<scout verdict: R36ScoutMergePkg>`) and the merge-set admit/reject facts the scout holds.
- Not attempted: the S091 live leg (no fetch made; the row makes no live claim) and the SHONEN boxes.

## Findings

1. **S130 denominator is one larger than its rows support.** The merge/kengaku package and its byte copy
   state `of 38` on every row, while the non-nested rows are 13 + 23 + 1 = 37. The erratum line lands the
   arithmetic the C1 counter recomputes, and the refusal row for the package now cites both the own-work
   locator reason and this denominator.
2. **Why the ledger split exists (the `scope` class).** `plans/defect_ledger.py` treats a row as agreed
   only when `closed == len(rows)` over `corpus/defects.jsonl` and round 35 froze `rows=5 closed=5`;
   appending the four **open** `R35-D*` rows to that file would have turned `r35_d4`'s parent predicate
   red. The rows therefore live in `corpus/defects-round35.jsonl`, and the round-36 counter reads that
   file for its own `rows=4 …` label. This is a scoping choice, not a fix, and the lesson says so.
3. **Merge/kengaku screening, static facts only** — `grep -c academic-pdf-report corpus/SOURCES.md` → 0,
   `grep -c 'S143' corpus/SOURCES.md` → 0, `grep -c 'S144' corpus/SOURCES.md` → 0, while S100 and S092 are
   present with `used-by` = `corpus/knowledge/benchmark-verifier-execution-model.md` (11 cells each).
   Three packages are refused on grounds this seat can establish without the scout: S155 and S130 are
   own-work locators with no lane receipt, and the release-identity package adds no ground the registry
   lacks. One row is admitted in direction only (S171, a real pinned upstream module) and keeps the
   placeholder.
4. **The draft is a hypothesis about the counter, not a measurement.** The replay above shows the
   `r35_d4` clause would pass on these bytes; whether `round36_c1_verify.py` prints `rows=4 closed=4 …`
   depends on the gate and the other three checks, which this seat did not run.

## Artifact paths

- Draft lesson: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36LessonDraft/round-36.md`
- This report: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-36/build/R36LessonDraft.md`
- Read-only inputs used: `plans/round-36-claims.md`, `corpus/lessons/round-35.md`,
  `corpus/lessons/round-35-verifier-spotcheck.md` (§5), `corpus/defects-round35.jsonl`,
  `corpus/defects.jsonl`, `plans/defect_ledger.py`, `plans/round35_hardening.py`,
  `plans/round36_c1_verify.py`, `plans/round36_c2_verify.py`, `plans/pkg-spec-r35.json`,
  `corpus/evidence/round36/toolathlon-package.md`, `corpus/evidence/round36/tb2-regex-log/`
  (five files + `SHA256SUMS`), `corpus/evidence/round36/regex-log-probe.txt`,
  `corpus/evidence/round36/regex-log-probe-first-run.txt`, `considerthese/2026-10-25.md`,
  `.ufo/waves/round-36/claims/control-c1-legacy.txt`, `control-c1-nothing.txt`, `control-c2-nothing.txt`,
  `census-before.txt`, `corpus/SOURCES.md`, `corpus/README.md`,
  `/home/vgpnk/Projects/shokuknow/merge/kengaku/MERGE-REPORT.md` and five merge knowledge files.

VERDICT: lesson-drafted
