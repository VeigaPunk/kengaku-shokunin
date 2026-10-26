# R39LessonErrata — round-38 closure R3: errata for `corpus/lessons/round-38.md` (round 39 wave 1, 2026-10-26)

Seat: scribe, leaf (no subagents, no background jobs). Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`.
Target bytes: `corpus/lessons/round-38.md` at `ef2fba062069de4f29aea45cb2a03d29a131054b` (2026-10-26 03:22:34 -0300),
working tree equal to HEAD (`git diff --stat HEAD -- corpus/lessons/round-38.md` empty).
Method: read-only Git (`log`, `diff`, `grep`, `cat-file`, `ls-tree`) plus direct file reads; no clone, no scratch dir,
no lane write, no counter re-run. Every command and its output is in
`.ufo/waves/round-39/build/R39LessonErrata/receipts.md` (sections A–E).

Outcome: **both defects verified** (R3 as filed). Two of the finding's own citations are imprecise and are corrected
below (§4); the corrections change neither defect's verdict. The errata block is append-ready verbatim (§5); the
round-39 Mistakes rows are drafted as two lines, each naming its recurrence and its gate, and the Defect-1 gate is
shown red-before at the round-38 freeze and green-after at the round-39 freeze (§6).

## 1. Defect 1 — verified: the cited round-37 fix has two moves; the cell names one and calls the class unpreventable

The cell under test, `corpus/lessons/round-38.md:36` (`captured-by` column), verbatim:

> “round 37's fix (re-pin and re-run every counter run) does not prevent the ordering, it only makes the discarded run harmless”

The cited fix, `corpus/lessons/round-37.md:42` (landed in `21e6251`), has two moves. The first is the machinery the
cell names (digest re-pin, `--dry` byte-equality, `P10` fresh-run compare). The second is a rule forward, verbatim:

> “Rule forward: a control that executes a frozen instrument keeps the run as a receipt.”

`grep -c` for that sentence → `1` (receipts A2). The rule forward is exactly the move that would have prevented the
recurrence: had it been followed, the control-time execution would itself have been the recorded run — the run the
claims header says was “output … discarded unread; it is not the first recorded run and is not evidence”
(`plans/round-38-claims.md:10-11`). So the sentence is true of the first move and false of the fix as cited: round 38
did not follow the half that bites. The row's class, evidence pointer and fix column all stand; the misstatement is
confined to this one cell.

**Limit of the correction (kept in the errata text).** The rule forward was a lesson rule, not an enforced gate —
round 38's own row says so (“A write-up, not yet a gate”). The errata must not upgrade it to “round 37 had a gate round
38 ignored”; the accurate claim is that round 37 stated the rule, round 38 skipped it, and nothing mechanical caught
that until this errata.

## 2. Defect 2 — verified: `census-before.txt` (exit 0) sits inside “Controls, all red at the freeze”

`corpus/lessons/round-38.md:12-15` opens “Controls, all red at the freeze (`.ufo/waves/round-38/claims/`):” and its
list closes at `:15` with “`census-before.txt` (exit 0, 15 W04).” That file is the clean baseline, not a red control:

```
$ grep -c W04 .ufo/waves/round-38/claims/census-before.txt     → 15
$ tail -1 .ufo/waves/round-38/claims/census-before.txt          → exit=0
$ sed -n '15p' …                                                → kengaku	ok	…/corpus/SOURCES.md
```

The parenthetical already carries `exit 0`, so no measurement is wrong; the label “all red” is. The lesson's own
`## Census` section (`:58`) reports the same file correctly (“exit 0, `kengaku ok`, 15 W04”) — the two statements
contradict each other inside one file.

## 3. Cross-check: is the baseline separable in the claims file?

`grep -c census plans/round-38-claims.md` → `0` (rc 1): the frozen claims file never names the census baseline at all;
it only says “Controls are committed with this file under `.ufo/waves/round-38/claims/`.” So the authority for
“baseline, not control” is the lesson's §Census, not the claims file (see §4.2).

## 4. Corrections to `F38RevLesson`'s own citations (mine, not filed by that seat)

1. **Line range.** `F38RevLesson` §Defect 2 heads its quote “lines 11–13”; the quoted sentence and its census entry are
   at `corpus/lessons/round-38.md:12-15` (`:11` is blank). The errata supersedes `:12-15`, not `:11-13`.
2. **“the claims file keeps it separate” is not true.** `grep -c census plans/round-38-claims.md` → `0` (rc 1). The
   separation exists only in the lesson's own §Census; the errata text below names that source instead.
3. **Defect 1's severity wording is right; its basis is not stated sharply enough.** “Round 37's fix does not prevent
   the ordering” is defensible only about the first move; the errata states it that way, and adds the
   write-up-not-a-gate limit so a later reader does not read the rule forward as enforced in round 37.

Neither correction changes a verdict: Defect 1 (moderate) and Defect 2 (minor/wording) both hold as filed.

## 5. Draft — `## Errata (round 39)` for `corpus/lessons/round-38.md` (append verbatim, do not rewrite a cell)

```markdown
## Errata (round 39, appended 2026-10-26 — this file is append-only, so the cells above stand as written)

Two characterizations were found wrong by the round-38 non-author closure (`F38RevLesson` Defects 1–2, routed as
`corpus/lessons/round-38-verifier-spotcheck.md` §5 item R3) and re-verified against the files by round-39 seat
`R39LessonErrata` (receipts `.ufo/waves/round-39/build/R39LessonErrata/receipts.md`, §A–C). No number, exit code or
count in this lesson changes.

- **Mistakes row 2 `captured-by` cell (supersedes `:36`).** The cell reads “round 37's fix (re-pin and re-run every
  counter run) does not prevent the ordering, it only makes the discarded run harmless”. `corpus/lessons/round-37.md:42`
  fixes the class with **two** moves, and the second is a rule forward: “Rule forward: a control that executes a frozen
  instrument keeps the run as a receipt.” Round 38 did not follow that half — `plans/round-38-claims.md:10-11` records the
  control-time run's “output was discarded unread; it is not the first recorded run and is not evidence”. The cell's
  sentence is true of the first move alone; followed, the rule forward would have made the control-time execution itself
  the recorded run, and the recurrence could not have arisen. The row's class, evidence pointer and fix column stand;
  what changes is that round 37 is not the half that failed here. Limit, kept explicit: the rule forward was a lesson
  rule, not a gate — the row's own fix column says “A write-up, not yet a gate”.
- **Header “Controls, all red at the freeze” sentence (supersedes `:12-15`).** `census-before.txt` is named inside that
  sentence but is not a red control: the committed file is the clean baseline — 15 W04 lines, `kengaku ok`, `exit=0`
  (`.ufo/waves/round-38/claims/census-before.txt`), and the frozen claims file never names it
  (`grep -c census plans/round-38-claims.md` → `0`). Read the sentence as covering the four controls
  `control-c1-nothing`, `control-c1-gate-edited`, `control-c2-nothing` and `control-c2-skip`; the baseline belongs with
  §Census below (`:58`), which reports it as “exit 0, `kengaku ok`, 15 W04”. The `:15` parenthetical already carries
  `exit 0`, so no measurement is wrong — the label is.

Forward state when this was appended: `corpus/lessons/round-39.md:13` names `census-before.txt` as “a baseline, not a
control” in its own controls paragraph, and the row-2 lint was run as a pair check at the round-39 freeze — red on
`e0a37853` (`.ufo/waves/round-38/claims/control-c2-skip.txt` asserts a “fresh probe”; that commit's round-38 receipt
is absent, `git cat-file -e …` rc 128), green on `088f7c36` (no committed round-39 control asserts a run). The round-39
lesson's Mistakes table carries the recurrence.
```

## 6. Draft — 2 lines for the round-39 lesson's Mistakes table (naming recurrence and gate)

```markdown
| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **lesson prose — a cell condenses the prior fix it cites to one of its moves** (recurrence of the round-38 lesson row 2, found by a wave-2 falsifier and not by any gate) | `corpus/lessons/round-37.md:42` fix column, second move “Rule forward: a control that executes a frozen instrument keeps the run as a receipt.”; cell under test `corpus/lessons/round-38.md:36`; discarded run `plans/round-38-claims.md:10-11` | `F38RevLesson` Defect 1 (round-38 closure R3); re-verified and re-worded by `R39LessonErrata` | `round-38.md` §Errata (round 39) appended; **gate** = the pair check: for a round-N freeze C, every committed control in `.ufo/waves/round-N/claims` whose text matches `fresh probe` requires that round's receipt at C (`git grep -l "fresh probe" C -- .ufo/waves/round-N/claims` non-empty **and** `git cat-file -e C:<receipt>` failing ⇒ red). Red-before `e0a37853` (match `control-c2-skip.txt`, receipt rc 128); green-after `088f7c36` (no match, rc 1). Run by hand now; no `plans/` script — proposed as a QC row. |
| **a verdict label contradicted by its own recorded number** — `census-before.txt` (`exit=0`) inside “all red” (recurrence of the round-38 lesson row 3 witness-picked label, `round-38.md:37`; outside Q28/V7, which govern entry requirement maps, not lesson prose) | `corpus/lessons/round-38.md:12-15`; `.ufo/waves/round-38/claims/census-before.txt` (15 W04, `exit=0`, `kengaku ok`); `plans/round-38-claims.md` names no census baseline (`grep -c census` → `0`) | `F38RevLesson` Defect 2 (round-38 closure R3); re-verified by `R39LessonErrata` | `round-38.md` §Errata appended; **gate** = exit-vs-label: every `control-*.txt` named inside a sentence asserting a verdict must match that file's own `exit=` line. Red-before `round-38.md:12-15` (green baseline under “all red”); green-after `corpus/lessons/round-39.md:13` (“a baseline, not a control”). Manual read today; proposed as a QC row beside Q28. |
```

Both rows are honest about their gate status: neither is a committed `plans/` script, and the first gate's two states are
executed and receipted (§7). If the L1 prefers one row, keep the first (it carries the recurrence the round already
tracks) and fold the second into it — but the two classes are distinct: one is prose about a prior fix, the other is a
label contradicted by its own number.

## 7. Gate evidence (Defect-1 class), executed

```
# RED, round-38 freeze
$ git grep -l "fresh probe" e0a37853 -- .ufo/waves/round-38/claims
  e0a37853:.ufo/waves/round-38/claims/control-c2-skip.txt          (rc 0)
$ git cat-file -e e0a37853:corpus/evidence/round38/build-pmars-probe.txt
  fatal: path … not in 'e0a37853…'                                  (rc 128)
# GREEN, round-39 freeze
$ git grep -l "fresh probe" 088f7c36 -- .ufo/waves/round-39/claims
  (no output)                                                        (rc 1)
$ git cat-file -e 088f7c36:corpus/evidence/round39/git-leak-probe.txt
  fatal: path … not in '088f7c36…'                                  (rc 128)
```

Green at `088f7c36` is correct, not vacuous: the receipt is absent (before first recorded run `6a1eb5e1`) **and** no
committed control claims a run. The failure round 38 hit — a control asserting a run, receipt missing — would flip the
same predicate red on round 39's bytes the moment a skip-control lands before the receipt.

## 8. What I did not do (out of scope, stated)

- Did not edit any lane file: the errata block and the Mistakes rows are drafts for the L1 to append/integrate.
  Nothing frozen was touched, and no `corpus/`/`plans/` file was written.
- Did not run the C1/C2 counters or the gate; not needed to resolve a pointer, and the counters are other seats' work.
- The round-39 lesson is untracked working-tree bytes (`?? corpus/lessons/round-39.md`), so `:13` is quoted as a
  snapshot of live draft text, not as landed bytes; the errata's forward-state sentence depends on it and should be
  re-read at append time.
- Created no scratch dir (no clone or fixture was needed) — nothing to remove.
- Installed nothing.

## Axes

- **Calibration (judged).** Both defects verified against files rather than accepted from the finding; two of the
  finding's own pointers corrected (§4); the errata's one contestable sentence (the rule forward's status) bounded
  before it could overclaim; the Defect-1 gate given a real red-before state rather than a promise.
- **Evidence.** Every number and quote above has a command and its output in `receipts.md`; quotes ≤ 25 words with
  file:line.

VERDICT: lesson-errata-2-verified
